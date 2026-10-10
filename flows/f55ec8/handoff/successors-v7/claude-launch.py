#!/usr/bin/env python3
"""Dry-run by default. The live path requires the living's separate word."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--cwd', required=True)
parser.add_argument('--launch', action='store_true')
args = parser.parse_args()
for name, digest in json.loads((root / 'artifact-manifest.json').read_text()).items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, name
cwd = Path(args.cwd).resolve(strict=True)
repo = cwd / '.jj/repo'
assert repo.is_dir(), 'cwd must be an independent JJ clone root, not a shared workspace'
assert not repo.is_symlink(), 'shared JJ repository link refused'
git_marker = cwd / '.git'
assert not git_marker.is_file(), 'Git worktree indirection refused'
body = (root / 'first-prompt.md').read_text()
assert len(body.encode()) < 100000
argv = ['claude', '--bg', '--name', 'primary-claude-successor-f55ec8',
        '--remote-control', 'primary-claude-successor-f55ec8', '--model', 'fable',
        '--system-prompt-file', str(root / 'claude-base.md'), '--', body]
assert all(len(v.encode()) < 100000 for v in argv)
env = os.environ.copy()
env.pop('NO_COLOR', None)
env['TERM'] = 'xterm-256color'
# Conservative envelope model with ample metadata reserve; actual daemon
# record must still be measured after dispatch, not inferred from argv length.
modelled = len(json.dumps({'args': argv, 'cwd': str(cwd), 'env': env}).encode()) + 65536
assert modelled < 262144, 'modelled daemon record exceeds limit'
print(json.dumps({'dryRun': not args.launch, 'userBytes': len(body.encode()),
                  'modelledRecordBytesWithReserve': modelled,
                  'actualDaemonRecordVerified': False, 'cwd': str(cwd)}), flush=True)
if args.launch:
    subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, check=True)
