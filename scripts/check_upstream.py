"""Report real upstream drift for the indexed sources; standard library only.

Detection is free: one batched GraphQL query per 50 repositories, then raw file
fetches only for repositories whose head moved. Drift means tracked *content*
changed (sha256 differs, file removed), never merely that a head moved.
Upstream text is untrusted data: it is only hashed, and every upstream string
that reaches the report is neutralised first.

    GITHUB_TOKEN=... python scripts/check_upstream.py --out report.md [--apply]

--apply does the mechanical part only: re-copy changed vendored files, re-pin a
linked repository whose manifests changed, refresh changed docs-hosted hashes.
It never edits prose. Exit 0 on success, 2 on an internal error.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = 'https://api.github.com'
RAW = 'https://raw.githubusercontent.com'
FILES = ('sources.json', 'linked-skills.json', 'resources.json')
STALE_DAYS = {'landscape.md': 90}
STALE_DEFAULT = 180
LIST_CAP = 40
MAX_BYTES = 5_000_000  # largest response read; a bigger one is reported as unreachable
REPORT_CAP = 45000  # the issue body limit is 65,536 characters; link-checker text is added later


class InternalError(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def pmap(function, items):
    with ThreadPoolExecutor(8) as pool:
        return list(pool.map(function, items))


def code(text, limit=120):
    """Upstream strings go into Markdown only as inert inline code."""
    text = re.sub(r'[`\s\x00-\x1f\x7f]+', ' ', str(text)).strip()
    return '`' + (text[:limit] + '...' if len(text) > limit else text) + '`'


def compare(repo, old, new):
    return f'[{old[:7]}...{new[:7]}](https://github.com/{repo}/compare/{old}...{new})'


class Client:
    """The only code that touches the network; tests replace it."""

    def __init__(self, token):
        self.token = token

    def _open(self, url, body=None, auth=False):
        headers = {'User-Agent': 'nl-voice-skills-upkeep'}
        if auth:
            headers['Authorization'] = 'Bearer ' + self.token
        if body is not None:
            headers['Content-Type'] = 'application/json'
        result = (None, b'')
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, data=body, headers=headers)
                with urllib.request.urlopen(request, timeout=30) as response:
                    data = response.read(MAX_BYTES + 1)
                    if len(data) > MAX_BYTES:
                        print(f'Response from {url} is larger than {MAX_BYTES} bytes; skipped', file=sys.stderr)
                        return None, b''
                    return response.status, data
            except urllib.error.HTTPError as error:
                result = (error.code, error.read(MAX_BYTES))
                if error.code < 500 and error.code != 429:
                    return result
            except OSError:
                result = (None, b'')
            time.sleep(2 * attempt + 1)
        return result

    def get(self, url):
        return self._open(url)

    def graphql(self, repos):
        """{lowercase repo: info dict, or None if the repository is gone}."""
        infos = {}
        for start in range(0, len(repos), 50):
            chunk = repos[start:start + 50]
            fields = []
            for index, repo in enumerate(chunk):
                if not re.fullmatch(r'[\w.-]+/[\w.-]+', repo):
                    raise InternalError('Unexpected repository name: ' + repo)
                owner, name = repo.split('/')
                fields.append(f'r{index}: repository(owner: "{owner}", name: "{name}") '
                              '{ nameWithOwner isArchived licenseInfo { spdxId } '
                              'defaultBranchRef { name target { oid ... on Commit { committedDate } } } }')
            body = json.dumps({'query': 'query { ' + ' '.join(fields) + ' }'}).encode()
            status, raw = self._open(API + '/graphql', body, auth=True)
            if status != 200:
                raise InternalError(f'GraphQL request failed with status {status}')
            payload = json.loads(raw)
            for error in payload.get('errors') or []:
                if error.get('type') != 'NOT_FOUND':
                    raise InternalError('GraphQL error: ' + str(error.get('message')))
            for index, repo in enumerate(chunk):
                node = (payload.get('data') or {}).get(f'r{index}')
                if node is None:
                    infos[repo.lower()] = None
                    continue
                branch = node.get('defaultBranchRef') or {}
                target = branch.get('target') or {}
                infos[repo.lower()] = {
                    'name': node['nameWithOwner'], 'archived': node['isArchived'],
                    'license': (node.get('licenseInfo') or {}).get('spdxId'),
                    'branch': branch.get('name'), 'head': target.get('oid'),
                    'committed': (target.get('committedDate') or '').replace('Z', '+00:00') or None}
        return infos

    def skill_paths(self, repo, ref):
        """(SKILL.md paths in the tree at ref, truncated flag), or None on failure."""
        status, raw = self._open(f'{API}/repos/{repo}/git/trees/{ref}?recursive=1', auth=True)
        if status != 200:
            return None
        tree = json.loads(raw)
        paths = [item['path'] for item in tree['tree']
                 if item['type'] == 'blob' and item['path'].split('/')[-1] == 'SKILL.md']
        return paths, bool(tree.get('truncated'))


def fetch_hashes(client, urls):
    """[(status, sha256 or None, bytes)] for each url, in order."""
    def one(url):
        status, data = client.get(url)
        return status, (sha256(data) if status == 200 else None), data
    return pmap(one, urls)


def github_repo(url):
    match = re.match(r'https://github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?(?:[/#?]|$)', url)
    return match and f'{match[1]}/{match[2]}'


def check_vendored(data, infos, client):
    results = []
    for collection in data['sources']['collections']:
        info = infos.get(collection['repo'].lower())
        if collection['decision'] != 'vendored' or not info or info['head'] in (None, collection['sha']):
            continue
        files = collection['copied_files']
        fetched = fetch_hashes(client, [f"{RAW}/{collection['repo']}/{info['head']}/{f['upstream_path']}"
                                        for f in files])
        result = {'repo': collection['repo'], 'old': collection['sha'], 'new': info['head'],
                  'changed': [], 'removed': [], 'errors': [], 'unchanged': 0}
        for item, (status, digest, body) in zip(files, fetched):
            if status == 200 and digest == item['sha256']:
                result['unchanged'] += 1
            elif status == 200:
                result['changed'].append({'item': item, 'sha256': digest, 'body': body})
            elif status in (404, 410):
                result['removed'].append(item['upstream_path'])
            else:
                result['errors'].append(item['upstream_path'])
        results.append(result)
    return results


def check_linked(data, infos, client):
    linked = data['linked']
    results = []
    for source in linked['sources']:
        info = infos.get(source['repo'].lower())
        if not info or info['head'] in (None, source['head']):
            continue
        skills = [s for s in linked['skills'] if s['repository'] == source['repo']]
        fetched = fetch_hashes(client, [f"{RAW}/{source['repo']}/{info['head']}/{s['path']}" for s in skills])
        result = {'repo': source['repo'], 'old': source['head'], 'new': info['head'],
                  'committed': info['committed'], 'changed': [], 'removed': [], 'errors': [],
                  'unchanged': 0, 'hashes': {}}
        for skill, (status, digest, _) in zip(skills, fetched):
            if status == 200:
                result['hashes'][skill['name']] = digest
            if status == 200 and digest == skill['verified_manifest_sha256']:
                result['unchanged'] += 1
            elif status == 200:
                result['changed'].append(skill['name'])
            elif status in (404, 410):
                result['removed'].append(skill['path'])
            else:
                result['errors'].append(skill['path'])
        results.append(result)
    return results


def check_candidates(data, drifted, client):
    """SKILL.md files that appeared since the recorded head and are neither indexed nor excluded."""
    excluded = data['linked'].get('excluded_manifests', [])
    candidates, errors = [], []
    for repo, old, new in drifted:
        indexed = {s['path'] for s in data['linked']['skills'] if s['repository'] == repo}
        for collection in data['sources']['collections']:
            if collection['repo'] == repo:
                indexed |= {f['upstream_path'] for f in collection.get('copied_files', [])}
        skip = {e.get('path') for e in excluded if e.get('repository') == repo and e.get('path')}
        skip_names = {e['name'] for e in excluded if e.get('repository') == repo and not e.get('path')}
        current, before = client.skill_paths(repo, new), client.skill_paths(repo, old)
        if current is None:
            errors.append(f'file tree of {repo}')
            continue
        known = set(before[0]) if before else None  # without the old tree, every unindexed file counts
        for path in current[0]:
            parent = path.split('/')[-2] if '/' in path else ''
            if path in indexed or path in skip or parent in skip_names:
                continue
            if known is None or path not in known:
                candidates.append({'repo': repo, 'path': path, 'head': new})
        if current[1]:
            errors.append(f'file tree of {repo} was truncated')
    return candidates, errors


def check_docs(data, client):
    docs = data['linked']['docs_hosted_skills']
    results = []
    for item, (status, digest, body) in zip(docs, fetch_hashes(client, [d['url'] for d in docs])):
        if status == 200 and digest != item['sha256']:
            results.append({'item': item, 'state': 'changed', 'sha256': digest, 'bytes': len(body)})
        elif status in (404, 410):
            results.append({'item': item, 'state': 'removed'})
        elif status != 200:
            results.append({'item': item, 'state': 'unreachable'})
    return results


def check_status(data, infos):
    """Archived, renamed, removed, default-branch and licence changes for every recorded repository."""
    records = [(c['repo'], 'sources.json', c.get('license'), c['default_branch'], None)
               for c in data['sources']['collections'] if c['decision'] == 'vendored']
    records += [(s['repo'], 'linked-skills.json', s.get('license'), s['default_branch'], None)
                for s in data['linked']['sources']]
    for item in data['resources']:
        repo = github_repo(item['url'])
        if repo:
            records.append((repo, 'resources.json', item.get('license'), item.get('default_branch'),
                            item.get('archived')))
    found, seen = [], set()
    for repo, where, licence, branch, archived in records:
        info = infos.get(repo.lower())
        if info is None:
            found.append((repo, where, 'repository not found (deleted or made private)'))
        elif (repo, where) not in seen:
            seen.add((repo, where))
            if info['archived'] and not archived:
                found.append((repo, where, 'archived'))
            if info['name'].lower() != repo.lower():
                found.append((repo, where, 'renamed to ' + info['name']))
            if branch and info['branch'] and info['branch'] != branch:
                found.append((repo, where, f"default branch is now {info['branch']} (recorded {branch})"))
            if (licence and re.fullmatch(r'[\w.+-]+', licence) and info['license']
                    and info['license'] != 'NOASSERTION' and info['license'] != licence):
                found.append((repo, where, f"licence is now {info['license']} (recorded {licence})"))
    return found


def page_date(text):
    """Latest date on a Checked/Reviewed/as-of line near the top of a page."""
    found = []
    for line in text.splitlines()[:20]:
        if re.search(r'\b(?:checked|reviewed|as of)\b', line, re.I):
            for match in re.finditer(r'(\d{4})-(\d{2})-(\d{2})|([A-Z][a-z]+ \d{1,2}, \d{4})', line):
                try:
                    found.append(date(*map(int, match.groups()[:3])) if match[1] else
                                 datetime.strptime(match[4], '%B %d, %Y').date())
                except ValueError:
                    pass
    return max(found, default=None)


def check_stale(pages, today):
    stale = []
    for name, text in sorted(pages.items()):
        seen = page_date(text)
        limit = STALE_DAYS.get(name, STALE_DEFAULT)
        if seen and (today - seen).days > limit:
            stale.append((name, seen.isoformat(), (today - seen).days, limit))
    return stale


def check(data, client, today):
    """Compare recorded state with upstream. Network only through client."""
    names = {}
    for collection in data['sources']['collections']:
        if collection['decision'] == 'vendored':
            names.setdefault(collection['repo'].lower(), collection['repo'])
    for source in data['linked']['sources']:
        names.setdefault(source['repo'].lower(), source['repo'])
    for item in data['resources']:
        repo = github_repo(item['url'])
        if repo:
            names.setdefault(repo.lower(), repo)
    infos = client.graphql(list(names.values()))
    vendored = check_vendored(data, infos, client)
    linked = check_linked(data, infos, client)
    moved = list(dict.fromkeys((r['repo'], r['old'], r['new']) for r in vendored + linked))
    candidates, errors = check_candidates(data, moved, client)
    return {
        'repos_checked': len(infos), 'heads_moved': len(moved),
        'vendored': [r for r in vendored if r['changed'] or r['removed']],
        'linked': [r for r in linked if r['changed'] or r['removed']],
        'docs': check_docs(data, client), 'candidates': candidates,
        'status': check_status(data, infos), 'stale': check_stale(data['pages'], today),
        'errors': errors + [f"{r['repo']}: {p}" for r in vendored + linked for p in r['errors']],
        '_vendored_all': vendored, '_linked_all': linked, '_infos': infos}


def capped(lines):
    shown = lines[:LIST_CAP]
    if len(lines) > LIST_CAP:
        shown.append(f'- ... and {len(lines) - LIST_CAP} more')
    return shown


def drifted(findings):
    return [key for key in ('vendored', 'linked', 'docs', 'candidates', 'status', 'stale')
            if findings[key]]


def report(findings, today):
    lines = []
    if findings['vendored']:
        lines += ['## Vendored files changed upstream', '']
        for r in findings['vendored']:
            lines.append(f"- **{r['repo']}** {compare(r['repo'], r['old'], r['new'])}: "
                         f"{len(r['changed'])} changed, {len(r['removed'])} removed or moved, "
                         f"{r['unchanged']} unchanged")
            lines += [f"  - changed {code(f['item']['upstream_path'])}" for f in r['changed'][:LIST_CAP]]
            lines += [f"  - removed or moved {code(p)}" for p in r['removed'][:LIST_CAP]]
        lines.append('')
    if findings['linked']:
        lines += ['## Linked skills changed upstream', '']
        for r in findings['linked']:
            lines.append(f"- **{r['repo']}** {compare(r['repo'], r['old'], r['new'])}: "
                         f"{len(r['changed'])} manifests changed, {len(r['removed'])} removed or moved, "
                         f"{r['unchanged']} unchanged")
            lines += [f"  - changed {code(n)}" for n in r['changed'][:LIST_CAP]]
            lines += [f"  - removed or moved {code(p)}" for p in r['removed'][:LIST_CAP]]
        lines.append('')
    if findings['docs']:
        lines += ['## Docs-hosted skills', ''] + capped(
            [f"- {code(d['item']['name'])} {d['state']}: {d['item']['url']}" for d in findings['docs']]) + ['']
    if findings['candidates']:
        lines += ['## Candidate new skills (not indexed, not excluded)', '',
                  'Candidates only; nothing is added automatically.', ''] + capped(
            [f"- {code(c['repo'])} {code(c['path'])}: "
             f"https://github.com/{c['repo']}/blob/{c['head']}/{quote(c['path'])}" for c in findings['candidates']]) + ['']
    if findings['status']:
        lines += ['## Repository status', ''] + capped(
            [f"- {code(r)} ({where}): {code(what, 200)}" for r, where, what in findings['status']]) + ['']
    if findings['stale']:
        lines += ['## Stale pages', ''] + [
            f'- docs/{name}: last checked {seen} ({age} days ago, limit {limit})'
            for name, seen, age, limit in findings['stale']] + ['']
    if findings['errors']:
        lines += ['## Could not check (not counted as drift)', ''] + capped(
            [f'- {code(e)}' for e in findings['errors']]) + ['']
    clean = not drifted(findings)
    head = ['<!-- upstream-drift: ' + ('clean' if clean else 'changes') + ' -->',
            f"Checked {findings['repos_checked']} repositories on {today.isoformat()} UTC. "
            f"Heads moved: {findings['heads_moved']}; content drift: "
            f"{len(findings['vendored']) + len(findings['linked'])} repositories, "
            f"{len(findings['docs'])} docs-hosted skills; {len(findings['candidates'])} candidate skills; "
            f"{len(findings['status'])} status changes; {len(findings['stale'])} stale pages.", '']
    if clean:
        head.append('No upstream changes. A moved head with unchanged tracked content is not drift.')
    else:
        head.append('Mechanical hash and pin refreshes: `python scripts/check_upstream.py --out report.md --apply`, '
                    'then read each changed entry\'s purpose and concerns text.')
    text = '\n'.join(head + [''] + lines).rstrip() + '\n'
    if len(text) <= REPORT_CAP:
        return text
    return (text[:REPORT_CAP].rsplit('\n', 1)[0]
            + '\n\n(report truncated; the full text is in the workflow run log)\n')


def write_json(path, value):
    """Same bytes the repo's files already have: indent 2, UTF-8, LF, trailing newline."""
    Path(path).write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))


def apply(data, findings, root, now):
    """Mechanical refresh of the JSON records; returns the lines to print."""
    root, printed = Path(root), []
    sources, linked = data['sources'], data['linked']
    for result in findings['_vendored_all']:
        if not result['changed'] or result['removed'] or result['errors']:
            continue
        collection = next(c for c in sources['collections'] if c['repo'] == result['repo'])
        for change in result['changed']:
            target = (root / change['item']['copied_path']).resolve()
            # Vendored copies live in skills/; their retained licenses live in licenses/.
            if not any(target.is_relative_to((root / name).resolve()) for name in ('skills', 'licenses')):
                raise InternalError('Path is outside skills/ and licenses/: ' + change['item']['copied_path'])
            target.write_bytes(change['body'])
            change['item']['sha256'], change['item']['bytes'] = change['sha256'], len(change['body'])
            printed.append(f"vendored {result['repo']}: {change['item']['copied_path']}")
        collection['sha'], collection['retrieved_at'] = result['new'], now
        sources['checked_at'] = now
    for result in findings['_linked_all']:
        if not result['changed'] or result['removed'] or result['errors']:
            continue
        source = next(s for s in linked['sources'] if s['repo'] == result['repo'])
        source['head'], source['retrieved_at'] = result['new'], now
        source['repository_head_committed_at'] = result['committed']
        for skill in linked['skills']:
            if skill['repository'] == result['repo']:
                skill['pinned_commit'] = result['new']
                skill['verified_manifest_sha256'] = result['hashes'][skill['name']]
                skill['source_repository_commit_at'] = result['committed']
        verification = linked['verification']
        verification['head_updates'] = [u for u in verification['head_updates']
                                        if u['repository'] != result['repo']] + [{
            'repository': result['repo'], 'from': result['old'], 'to': result['new'],
            'to_committed_at': result['committed'],
            'manifests_rehashed': len(result['hashes']), 'manifests_unchanged': result['unchanged']}]
        verification['current_branch_manifest_checked_at_utc'] = now
        linked['checked_at_utc'] = now
        printed += [f"linked {result['repo']}: re-pinned {len(result['hashes'])} skills; "
                    f'review purpose and concerns of {code(n)}' for n in result['changed']]
    for change in findings['docs']:
        if change['state'] == 'changed':
            change['item'].update(sha256=change['sha256'], bytes=change['bytes'], retrieved_at=now)
            linked['checked_at_utc'] = now
            printed.append(f"docs-hosted {change['item']['name']}: hash refreshed; review purpose and concerns")
    for name in FILES:
        write_json(root / name, {'sources.json': sources, 'linked-skills.json': linked,
                                 'resources.json': data['resources']}[name])
    return printed


def load(root):
    root = Path(root)
    data = {'pages': {p.name: p.read_text(encoding='utf-8') for p in (root / 'docs').glob('*.md')}}
    for key, name in zip(('sources', 'linked', 'resources'), FILES):
        data[key] = json.loads((root / name).read_text(encoding='utf-8'))
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--out', required=True, help='Markdown report path')
    parser.add_argument('--apply', action='store_true', help='refresh hashes and pins in the JSON records')
    args = parser.parse_args(argv)
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        print('GITHUB_TOKEN is required for the GraphQL query', file=sys.stderr)
        return 2
    try:
        data = load(ROOT)
        today = datetime.now(timezone.utc).date()
        findings = check(data, Client(token), today)
        Path(args.out).write_bytes(report(findings, today).encode('utf-8'))
        print(f"{findings['repos_checked']} repositories checked, {findings['heads_moved']} heads moved, "
              f"drift in: {', '.join(drifted(findings)) or 'nothing'}")
        if args.apply:
            print('\n'.join(apply(data, findings, ROOT, datetime.now(timezone.utc).isoformat())) or 'nothing to apply')
    except (InternalError, OSError, KeyError, ValueError) as error:
        print(f'check_upstream failed: {error!r}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
