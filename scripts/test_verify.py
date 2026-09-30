"""Regression check: reject source tampering, mirror links, and accidental secrets."""
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from verify import ROOT, verify


if __name__ == '__main__':
    with TemporaryDirectory() as directory:
        copy = Path(directory) / 'collection'
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        verify(copy)
        sample = copy / 'skills/livekit/building-livekit-agents/SKILL.md'
        original = sample.read_bytes()
        sample.write_bytes(original + b'\nUnrecorded upstream change\n')
        try:
            verify(copy)
        except AssertionError:
            print('PASS: unrecorded upstream content changes are rejected.')
        else:
            raise AssertionError('Tampered upstream content was accepted')
        sample.write_bytes(original)
        index = copy / 'linked-skills.json'
        original_index = index.read_bytes()
        changed = json.loads(original_index)
        changed['skills'][0]['url'] = 'https://example.invalid/mirror/SKILL.md'
        index.write_text(json.dumps(changed), encoding='utf-8')
        try:
            verify(copy)
        except AssertionError as error:
            assert changed['skills'][0]['name'] in str(error), error
            print('PASS: linked skills must retain their original source URL.')
        else:
            raise AssertionError('Mirror source URL was accepted')
        index.write_bytes(original_index)
        changed = json.loads(original_index)
        changed['docs_hosted_skills'][0]['url'] = 'https://github.com/example/mirror/blob/main/SKILL.md'
        index.write_text(json.dumps(changed), encoding='utf-8')
        try:
            verify(copy)
        except AssertionError as error:
            assert changed['docs_hosted_skills'][0]['name'] in str(error), error
            print('PASS: docs-hosted skills must stay on the vendor documentation host.')
        else:
            raise AssertionError('GitHub mirror of a docs-hosted skill was accepted')
        index.write_bytes(original_index)
        changed = json.loads(original_index)
        changed['verification']['current_branch_manifest_hash_matches'] -= 1
        index.write_text(json.dumps(changed), encoding='utf-8')
        try:
            verify(copy)
        except AssertionError as error:
            assert 'Stale verification counter' in str(error), error
            print('PASS: stale manifest-verification counts are rejected.')
        else:
            raise AssertionError('Stale verification count was accepted')
        index.write_bytes(original_index)
        figure = copy / 'assets/diagrams/hero.svg'
        original_figure = figure.read_bytes()
        figure.write_bytes(original_figure.replace(b'<title', b'<image href="https://example.invalid/a.png"/><title', 1))
        try:
            verify(copy)
        except AssertionError as error:
            assert 'external resource' in str(error), error
            print('PASS: figures that load external resources are rejected.')
        else:
            raise AssertionError('Figure with an external resource was accepted')
        figure.write_bytes(original_figure)
        (copy / 'accidental-secret.txt').write_text('ghp_' + 'A' * 32, encoding='utf-8')
        try:
            verify(copy)
        except AssertionError as error:
            assert 'Credential or private-path pattern' in str(error), error
            print('PASS: accidental credential patterns are rejected without printing values.')
        else:
            raise AssertionError('Credential pattern was accepted')
