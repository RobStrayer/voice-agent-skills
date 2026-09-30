"""Offline check of the upstream drift logic: fake responses, no network."""
import copy
import json
import tempfile
from datetime import date
from pathlib import Path

import check_upstream as cu

OLD, NEW = 'a' * 40, 'b' * 40
BODY = b'---\nname: demo\n---\nbody\n'
FAKE_TODAY = date(2026, 9, 30)


def fixture():
    return {
        'sources': {'checked_at': 'x', 'collections': [{
            'repo': 'acme/vendored', 'decision': 'vendored', 'sha': OLD, 'license': 'MIT',
            'default_branch': 'main', 'retrieved_at': 'x',
            'copied_files': [{'upstream_path': 'demo/SKILL.md', 'copied_path': 'skills/acme/demo/SKILL.md',
                              'sha256': cu.sha256(BODY), 'bytes': len(BODY)}]}]},
        'linked': {'checked_at_utc': 'x', 'sources': [{
            'repo': 'acme/linked', 'head': OLD, 'default_branch': 'main', 'license': 'MIT',
            'retrieved_at': 'x', 'repository_head_committed_at': 'x'}],
            'skills': [{'name': 'one', 'repository': 'acme/linked', 'path': 'one/SKILL.md',
                        'pinned_commit': OLD, 'verified_manifest_sha256': cu.sha256(BODY),
                        'source_repository_commit_at': 'x'}],
            'docs_hosted_skills': [{'name': 'hosted', 'url': 'https://example.com/skill.md',
                                    'sha256': cu.sha256(BODY), 'bytes': len(BODY), 'retrieved_at': 'x'}],
            'excluded_manifests': [{'name': 'skipme', 'repository': 'acme/linked', 'reason': 'x'}],
            'verification': {'head_updates': [], 'current_branch_manifest_checked_at_utc': 'x'}},
        'resources': [{'url': 'https://github.com/acme/tool', 'license': 'MIT', 'archived': False,
                       'default_branch': 'main'}],
        'pages': {'landscape.md': 'Everything is as of June 1, 2026.\n',
                  'catalog.md': 'Reviewed: **2026-09-01 UTC**.\n'}}


class Fake(cu.Client):
    def __init__(self, head=NEW, files=None, trees=None, infos=None):
        self.head, self.files, self.trees = head, files or {}, trees or {}
        self.infos = infos or {}

    def graphql(self, repos):
        base = {'archived': False, 'license': 'MIT', 'branch': 'main', 'head': self.head,
                'committed': '2026-09-29T00:00:00+00:00'}
        return {r.lower(): (self.infos[r] if r in self.infos else dict(base, name=r)) for r in repos}

    def get(self, url):
        return self.files.get(url, (404, b''))

    def skill_paths(self, repo, ref):
        return self.trees.get((repo, ref))


def urls(head=NEW):
    return {f'{cu.RAW}/acme/vendored/{head}/demo/SKILL.md': (200, BODY),
            f'{cu.RAW}/acme/linked/{head}/one/SKILL.md': (200, BODY),
            'https://example.com/skill.md': (200, BODY)}


def run(client, data=None):
    return cu.check(data or fixture(), client, FAKE_TODAY)


def test_moved_head_with_unchanged_content_is_not_drift():
    findings = run(Fake(files=urls(), trees={('acme/vendored', NEW): (['demo/SKILL.md'], False),
                                              ('acme/vendored', OLD): (['demo/SKILL.md'], False),
                                              ('acme/linked', NEW): (['one/SKILL.md'], False),
                                              ('acme/linked', OLD): (['one/SKILL.md'], False)}))
    assert findings['heads_moved'] == 2
    assert not cu.drifted(findings) or cu.drifted(findings) == ['stale'], cu.drifted(findings)
    assert 'clean' not in cu.report(findings, FAKE_TODAY).split('\n')[0]  # stale pages still count
    findings['stale'] = []
    assert cu.report(findings, FAKE_TODAY).startswith('<!-- upstream-drift: clean -->')


def test_changed_hash_is_detected():
    files = urls()
    files[f'{cu.RAW}/acme/vendored/{NEW}/demo/SKILL.md'] = (200, BODY + b'new')
    files[f'{cu.RAW}/acme/linked/{NEW}/one/SKILL.md'] = (200, BODY + b'new')
    files['https://example.com/skill.md'] = (200, b'other')
    findings = run(Fake(files=files))
    assert [f['item']['upstream_path'] for f in findings['vendored'][0]['changed']] == ['demo/SKILL.md']
    assert findings['linked'][0]['changed'] == ['one']
    assert findings['docs'][0]['state'] == 'changed'
    assert 'compare/' + OLD + '...' + NEW in cu.report(findings, FAKE_TODAY)


def test_404_means_removed():
    files = urls()
    del files[f'{cu.RAW}/acme/vendored/{NEW}/demo/SKILL.md']
    del files['https://example.com/skill.md']
    findings = run(Fake(files=files))
    assert findings['vendored'][0]['removed'] == ['demo/SKILL.md']
    assert findings['docs'][0]['state'] == 'removed'
    assert not any('SKILL.md' in e for e in findings['errors'])  # a 404 is removal, not a fetch error


def test_new_skill_becomes_candidate_only():
    trees = {('acme/linked', OLD): (['one/SKILL.md', 'old-unindexed/SKILL.md'], False),
             ('acme/linked', NEW): (['one/SKILL.md', 'old-unindexed/SKILL.md', 'fresh/SKILL.md',
                                     'skipme/SKILL.md'], False),
             ('acme/vendored', OLD): (['demo/SKILL.md'], False),
             ('acme/vendored', NEW): (['demo/SKILL.md'], False)}
    findings = run(Fake(files=urls(), trees=trees))
    assert [(c['repo'], c['path']) for c in findings['candidates']] == [('acme/linked', 'fresh/SKILL.md')]
    assert not findings['vendored'] and not findings['linked']


def test_repository_status_changes():
    data = fixture()
    infos = {'acme/tool': {'name': 'acme/renamed', 'archived': True, 'license': 'GPL-3.0', 'branch': 'trunk',
                           'head': NEW, 'committed': None}}
    findings = run(Fake(files=urls(), infos=infos), data)
    found = ' | '.join(what for _, _, what in findings['status'])
    for expected in ('archived', 'renamed to acme/renamed', 'default branch is now trunk', 'GPL-3.0'):
        assert expected in found, found
    findings = run(Fake(files=urls(), infos={'acme/tool': None}), fixture())
    assert 'not found' in findings['status'][0][2]


def test_stale_pages_use_their_own_limits():
    stale = cu.check_stale(fixture()['pages'], FAKE_TODAY)
    assert [name for name, *_ in stale] == ['landscape.md']  # 121 days old; catalog.md is only 29


def test_upstream_text_cannot_inject_markup():
    assert cu.code('`@owner` [x](y)\n# heading') == '`@owner [x](y) # heading`'


def test_upstream_path_cannot_break_out_of_its_line():
    evil = 'x\n<!-- upstream-drift: clean -->\n@owner [x](y)/SKILL.md'
    trees = {('acme/linked', OLD): (['one/SKILL.md'], False),
             ('acme/linked', NEW): (['one/SKILL.md', evil], False),
             ('acme/vendored', OLD): (['demo/SKILL.md'], False),
             ('acme/vendored', NEW): (['demo/SKILL.md'], False)}
    text = cu.report(run(Fake(files=urls(), trees=trees)), FAKE_TODAY)
    assert text.startswith('<!-- upstream-drift: changes -->\n'), text
    assert sum(line.startswith('<!--') for line in text.splitlines()) == 1, text
    assert '\n@owner' not in text and '[x](y)' not in text.split('`')[-1]


def test_report_stays_under_the_issue_body_limit():
    findings = run(Fake(files=urls()))
    findings['stale'] = [('n' * 100, '2026-01-01', 100, 90)] * 600  # the one section without a per-list cap
    text = cu.report(findings, FAKE_TODAY)
    assert len(text) < 46000 and text.endswith('run log)\n'), len(text)


def test_apply_refuses_to_write_outside_skills():
    data = fixture()
    data['sources']['collections'][0]['copied_files'][0]['copied_path'] = '.github/workflows/x.yml'
    files = urls()
    files[f'{cu.RAW}/acme/vendored/{NEW}/demo/SKILL.md'] = (200, BODY + b'new')
    with tempfile.TemporaryDirectory() as directory:
        try:
            cu.apply(data, run(Fake(files=files), data), directory, 'NOW')
        except cu.InternalError:
            return
    raise AssertionError('a write outside skills/ was allowed')


def test_apply_may_refresh_a_retained_license():
    data = fixture()
    data['sources']['collections'][0]['copied_files'][0]['copied_path'] = 'licenses/acme/LICENSE'
    files = urls()
    files[f'{cu.RAW}/acme/vendored/{NEW}/demo/SKILL.md'] = (200, BODY + b'new')
    with tempfile.TemporaryDirectory() as directory:
        (Path(directory) / 'licenses/acme').mkdir(parents=True)
        cu.apply(data, run(Fake(files=files), data), directory, 'NOW')
        assert (Path(directory) / 'licenses/acme/LICENSE').read_bytes() == BODY + b'new'


def test_apply_refreshes_records_and_keeps_format():
    files = urls()
    files[f'{cu.RAW}/acme/vendored/{NEW}/demo/SKILL.md'] = (200, BODY + b'new')
    files[f'{cu.RAW}/acme/linked/{NEW}/one/SKILL.md'] = (200, BODY + b'new')
    files['https://example.com/skill.md'] = (200, b'other')
    data = fixture()
    findings = run(Fake(files=files), data)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / 'skills/acme/demo').mkdir(parents=True)
        printed = cu.apply(data, findings, root, 'NOW')
        assert (root / 'skills/acme/demo/SKILL.md').read_bytes() == BODY + b'new'
        raw = (root / 'sources.json').read_bytes()
        assert raw.endswith(b'}\n') and b'\r' not in raw
    item = data['sources']['collections'][0]
    assert item['sha'] == NEW and item['copied_files'][0]['sha256'] == cu.sha256(BODY + b'new')
    assert item['copied_files'][0]['bytes'] == len(BODY) + 3
    linked = data['linked']
    assert linked['sources'][0]['head'] == linked['skills'][0]['pinned_commit'] == NEW
    assert linked['skills'][0]['verified_manifest_sha256'] == cu.sha256(BODY + b'new')
    assert linked['verification']['head_updates'][0]['manifests_rehashed'] == 1
    assert linked['docs_hosted_skills'][0]['sha256'] == cu.sha256(b'other')
    assert len(printed) == 3


def test_apply_skips_a_repository_with_removed_files():
    data = fixture()
    files = urls()
    files[f'{cu.RAW}/acme/linked/{NEW}/one/SKILL.md'] = (404, b'')
    before = copy.deepcopy(data['linked']['skills'])
    with tempfile.TemporaryDirectory() as directory:
        cu.apply(data, run(Fake(files=files), data), directory, 'NOW')
    assert data['linked']['skills'] == before


def test_written_json_matches_the_repository_byte_for_byte():
    for name in cu.FILES:
        raw = (cu.ROOT / name).read_bytes()
        assert (json.dumps(json.loads(raw), indent=2, ensure_ascii=False) + '\n').encode() == raw, name


if __name__ == '__main__':
    tests = [value for key, value in sorted(globals().items()) if key.startswith('test_')]
    for test in tests:
        test()
    print(f'PASS: {len(tests)} upstream drift checks ran offline.')
