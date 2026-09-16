#!/usr/bin/env python3
"""Launch primary-psyche-medium. Dry-run by default; the live path needs a word.

    python3 claude-launch.py --cwd <independent-jj-clone>            # dry run
    python3 claude-launch.py --cwd <independent-jj-clone> --dry-run  # the same
    python3 claude-launch.py --cwd <independent-jj-clone> --launch   # starts it

Mirrors the v7 launcher of flow f55ec8 (flows/f55ec8/handoff/successors-v7/
claude-launch.py): the same artifact-hash gate, the same independent-clone
assertions, the same argv-size and modelled-daemon-record bounds, the same
detached stdin. It differs only where this flow differs: the model, the effort
flag, the name, and the explicit --dry-run and --session-id.
"""
import argparse
import hashlib
import json
import os
import subprocess
import uuid
from pathlib import Path

NAME = 'primary-psyche-medium'
MODEL = 'claude-opus-4-7[1m]'
EFFORT = 'medium'

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--cwd', required=True)
parser.add_argument('--launch', action='store_true')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--session-id', default=None)
args = parser.parse_args()
assert not (args.launch and args.dry_run), 'choose one of --launch and --dry-run'

for name, recorded in json.loads((root / 'artifact-manifest.json').read_text()).items():
    actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
    assert actual == recorded, 'hash mismatch: %s' % name

cwd = Path(args.cwd).resolve(strict=True)
repo = cwd / '.jj/repo'
assert repo.is_dir(), 'cwd must be an independent JJ clone root, not a shared workspace'
assert not repo.is_symlink(), 'shared JJ repository link refused'
assert not (cwd / '.git').is_file(), 'Git worktree indirection refused'

base = root / 'claude-base.md'
body = (root / 'first-prompt.md').read_text()
assert len(body.encode()) < 100000

# --effort exists on this CLI; probe rather than assume, as the harness skill says.
help_text = subprocess.run(['claude', '--help'], capture_output=True, text=True).stdout
effort_flag = ['--effort', EFFORT] if '--effort' in help_text else []

session_id = args.session_id or str(uuid.uuid4())
argv = (['claude', '--bg', '--session-id', session_id, '--name', NAME,
         '--remote-control', NAME, '--model', MODEL]
        + effort_flag
        + ['--system-prompt-file', str(base), '--', body])
assert all(len(v.encode()) < 100000 for v in argv)

env = os.environ.copy()
env.pop('NO_COLOR', None)
env['TERM'] = 'xterm-256color'
# Conservative envelope model with ample metadata reserve; the actual daemon
# record must still be measured after dispatch, not inferred from argv length.
modelled = len(json.dumps({'args': argv, 'cwd': str(cwd), 'env': env}).encode()) + 65536
assert modelled < 262144, 'modelled daemon record exceeds limit'

live = args.launch
print(json.dumps({'dryRun': not live, 'name': NAME, 'model': MODEL,
                  'effort': EFFORT if effort_flag else None,
                  'effortFlagPresent': bool(effort_flag),
                  'sessionId': session_id,
                  'baseBytes': base.stat().st_size,
                  'baseSha256': hashlib.sha256(base.read_bytes()).hexdigest(),
                  'userBytes': len(body.encode()),
                  'argvBytes': sum(len(v.encode()) for v in argv),
                  'artifactsVerified': True,
                  'modelledRecordBytesWithReserve': modelled,
                  'actualDaemonRecordVerified': False, 'cwd': str(cwd)}), flush=True)
if live:
    subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, check=True)
