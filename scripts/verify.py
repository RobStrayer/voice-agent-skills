"""Verify the collection without dependencies, network access, or provider calls."""
import ast
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


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
        tracked = set()
        for source in sources['collections']:
            if source['decision'] != 'vendored':
                continue
            assert re.fullmatch(r'[0-9a-f]{40}', source['sha']), source['repo']
            assert source['license'], source['repo']
            for item in source['copied_files']:
                path = inside(item['copied_path'])
                data = path.read_bytes()
                assert hashlib.sha256(data).hexdigest() == item['sha256'], path
                assert len(data) == item['bytes'], path
                assert item['copied_path'] not in tracked, path
                tracked.add(item['copied_path'])
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
        resources = json.loads((ROOT / 'resources.json').read_text(encoding='utf-8'))
        assert len(resources) == len({item['name'] for item in resources}), 'Duplicate resource'
        for item in resources:
            assert isinstance(item['stars'], int) and item['stars'] >= 0, item['name']
            assert re.fullmatch(r'[0-9a-f]{40}', item['commit']), item['name']
            assert item['metadata_source'] and item['retrieved_at'], item['name']
        for path in ROOT.rglob('*.py'):
            if '.git' not in path.parts:
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
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
              f'{len(resources)} resources; names, provenance, syntax, and local paths checked.')
    finally:
        ROOT = previous


if __name__ == '__main__':
    verify()
