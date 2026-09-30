"""Small regression check: changed upstream content must fail provenance checks."""
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
        sample.write_bytes(sample.read_bytes() + b'\nUnrecorded upstream change\n')
        try:
            verify(copy)
        except AssertionError:
            print('PASS: unrecorded upstream content changes are rejected.')
        else:
            raise AssertionError('Tampered upstream content was accepted')
