"""Verify the collection without dependencies, network access, or provider calls."""
import ast
import hashlib
import json
import re
import xml.etree.ElementTree as ElementTree
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

# These checks catch common leaks; a human review still covers private prose/data.
SENSITIVE = [re.compile(pattern) for pattern in (
    r'gh[pousr]_[A-Za-z0-9]{20,}',
    r'github_pat_[A-Za-z0-9_]{30,}',
    r'sk-[A-Za-z0-9_-]{24,}',
    r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'(?:C:[/\\]Users[/\\]|/Users/)[A-Za-z0-9][^/\\\s]*[/\\]',
)]


def inside(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {relative}")
    return path


def verify(root=ROOT):
    # root is injected only for the isolated negative checks below.
    global ROOT
    previous, ROOT = ROOT, root.resolve()
    try:
        sources = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
        catalog = (ROOT / 'docs/catalog.md').read_text(encoding='utf-8')
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        tracked = set()
        for source in sources['collections']:
            if source['decision'] != 'vendored':
                continue
            assert re.fullmatch(r'[0-9a-f]{40}', source['sha']), source['repo']
            assert source['license'], source['repo']
            copied_paths = {item['copied_path'] for item in source['copied_files']}
            license_paths = ({'skills/openai/speech/LICENSE.txt',
                              'skills/openai/transcribe/LICENSE.txt'}
                             if source['provider'] == 'openai'
                             else {'licenses/' + source['provider'] + '/LICENSE'})
            assert license_paths <= copied_paths, 'Missing retained license: ' + source['repo']
            assert source['live_url'] == source['url'] + '/tree/' + source['default_branch']
            assert f'](skills/{source["provider"]}/' not in readme, 'Provider README links must use original sources'
            for item in source['copied_files']:
                path = inside(item['copied_path'])
                data = path.read_bytes()
                assert hashlib.sha256(data).hexdigest() == item['sha256'], path
                assert len(data) == item['bytes'], path
                assert item['copied_path'] not in tracked, path
                tracked.add(item['copied_path'])
                if item['upstream_path'].endswith('/SKILL.md') or item['upstream_path'] == 'SKILL.md':
                    original = source['url'] + '/blob/' + source['default_branch'] + '/' + item['upstream_path']
                    assert original in catalog, 'Missing original source: ' + original
        names = set()
        skills = sorted((ROOT / 'skills').rglob('SKILL.md'))
        for path in skills:
            text = path.read_text(encoding='utf-8')
            match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
            assert match, f'Missing frontmatter: {path}'
            header = match[1]
            name_match = re.search(r'^name:\s*([^\r\n]+)', header, re.M)
            assert name_match, path
            name = name_match[1].strip().strip('\"\'')
            assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name), path
            assert len(name) <= 64 and name == path.parent.name, path
            assert name not in names, f'Duplicate skill name: {name}'
            names.add(name)
            assert re.search(r'^description:\s*\S', header, re.M), path
            if path.parts[-3] != 'foundations':
                for member in path.parent.rglob('*'):
                    if member.is_file():
                        assert member.relative_to(ROOT).as_posix() in tracked, member
        assert len(skills) == sources['skill_count'], 'Skill count mismatch'
        assert len(tracked) == sources['copied_file_count'], 'Copied count mismatch'
        originals = {p.parent.relative_to(ROOT).as_posix()
                     for p in (ROOT / 'skills/foundations').rglob('SKILL.md')}
        assert originals == set(sources['original_skills']), 'Original skill index mismatch'
        linked = json.loads((ROOT / 'linked-skills.json').read_text(encoding='utf-8'))
        linked_catalog = (ROOT / 'docs/more-skills.md').read_text(encoding='utf-8')
        origins = {item['repo']: item for item in linked['sources']}
        assert len(origins) == len(linked['sources']) == linked['source_repository_count']
        entries = linked['skills']
        assert len(entries) == len({item['url'] for item in entries}) == linked['selected_skill_count']
        for key in ('current_branch_manifest_count', 'current_branch_manifest_http_200',
                    'current_branch_manifest_hash_matches'):
            assert linked['verification'][key] == len(entries), 'Stale verification counter: ' + key
        assert dict(Counter(item['repository'] for item in entries)) == linked['counts_by_repository']
        assert dict(Counter(item['selection'] for item in entries)) == linked['counts_by_selection']
        for source in origins.values():
            assert re.fullmatch(r'[0-9a-f]{40}', source['head']), source['repo']
            assert isinstance(source['stars'], int) and source['stars'] >= 0, source['repo']
            datetime.fromisoformat(source['retrieved_at'].replace('Z', '+00:00'))
            assert source['license_status'], source['repo']
            if source['license_path']:
                assert source['license_url'] == ('https://github.com/' + source['repo'] +
                       '/blob/' + source['default_branch'] + '/' + source['license_path'])
        for item in entries:
            source = origins[item['repository']]
            assert item['default_branch'] == source['default_branch'], item['name']
            assert item['pinned_commit'] == source['head'], item['name']
            assert item['path'] == 'SKILL.md' or item['path'].endswith('/SKILL.md'), item['name']
            assert item['selection'] in linked['selection_definitions'], item['name']
            original = ('https://github.com/' + item['repository'] + '/blob/' +
                        source['default_branch'] + '/' + item['path'])
            assert item['url'] == original and original in linked_catalog, item['name']
            assert re.fullmatch(r'[0-9a-f]{64}', item['verified_manifest_sha256']), item['name']
            assert item['purpose'] and item['dependencies'] and item['concerns'], item['name']
        # Docs-hosted skills have no commit: the vendor's own https file, pinned by sha256 and retrieval time.
        docs = linked['docs_hosted_skills']
        assert len(docs) == len({item['name'] for item in docs}) == len({item['url'] for item in docs}) \
            == linked['docs_hosted_skill_count'], 'Docs-hosted count mismatch'
        for key in ('docs_hosted_count', 'docs_hosted_http_200', 'docs_hosted_digest_matches'):
            assert linked['verification'][key] == len(docs), 'Stale verification counter: ' + key
        assert dict(Counter(item['selection'] for item in docs)) == linked['docs_hosted_counts_by_selection']
        for item in docs:
            url = urlsplit(item['url'])
            assert url.scheme == 'https' and url.hostname == item['host'], item['name']
            assert not re.search(r'(?:^|\.)github(?:usercontent)?\.com$', url.hostname), item['name']
            assert re.fullmatch(r'[0-9a-f]{64}', item['sha256']), item['name']
            assert isinstance(item['bytes'], int) and item['bytes'] > 0, item['name']
            datetime.fromisoformat(item['retrieved_at'].replace('Z', '+00:00'))
            assert item['selection'] in linked['selection_definitions'], item['name']
            assert item['purpose'] and item['dependencies'] and item['concerns'], item['name']
            assert item['url'] in linked_catalog, 'Missing docs-hosted link: ' + item['name']
        resources = json.loads((ROOT / 'resources.json').read_text(encoding='utf-8'))
        resource_catalog = (ROOT / 'docs/resources.md').read_text(encoding='utf-8')
        assert len(resources) == len({item['name'] for item in resources}), 'Duplicate resource'
        for item in resources:
            assert isinstance(item['stars'], int) and item['stars'] >= 0, item['name']
            assert re.fullmatch(r'[0-9a-f]{40}', item['commit']), item['name']
            assert item['metadata_source'] and item['retrieved_at'], item['name']
            assert item['url'] in resource_catalog, 'Missing resource link: ' + item['name']
        for path in ROOT.rglob('*.py'):
            if '.git' not in path.parts:
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        for path in ROOT.rglob('*'):
            if not path.is_file() or {'.git', '__pycache__', 'node_modules'} & set(path.parts):
                continue
            assert not (path.name == '.env' or
                        path.name.startswith('.env.') and path.name != '.env.example' or
                        path.name in {'id_rsa', 'id_ed25519'}), 'Private file: ' + str(path)
            try:
                content = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            assert not any(pattern.search(content) for pattern in SENSITIVE), \
                'Credential or private-path pattern in: ' + str(path)
        # Figures render through <img> on GitHub: parseable, titled, and self-contained.
        for path in ROOT.rglob('*.svg'):
            relative = path.relative_to(ROOT).as_posix()
            if '.git' in path.parts or relative in tracked:
                continue
            figure = ElementTree.parse(path).getroot()
            assert figure.find('{http://www.w3.org/2000/svg}title') is not None, 'SVG without <title>: ' + relative
            assert not re.search(r'''<script|@import|(?:href|src)\s*=\s*["']https?:|url\(\s*["']?https?:''',
                                 path.read_text(encoding='utf-8')), 'SVG loads an external resource: ' + relative
        for path in ROOT.rglob('*.md'):
            if '.git' in path.parts:
                continue
            text = path.read_text(encoding='utf-8')
            text = re.sub(r'```.*?```', '', text, flags=re.S)
            for target in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text):
                target = target.strip('<>')
                url = urlsplit(target)
                if url.scheme or target.startswith('#'):
                    continue
                local = (path.parent / unquote(url.path)).resolve()
                assert local.is_relative_to(ROOT) and local.exists(), f'{path}: {target}'
        print(f'PASS: {len(skills)} skills, {len(tracked)} upstream files, '
              f'{len(entries)} linked skills, {len(docs)} docs-hosted skills, {len(resources)} resources; '
              'names, provenance, licenses, syntax, figures, '
              'local paths, and bounded credential patterns checked.')
    finally:
        ROOT = previous


if __name__ == '__main__':
    verify()
