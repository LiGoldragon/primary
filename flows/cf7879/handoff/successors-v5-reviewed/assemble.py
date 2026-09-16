#!/usr/bin/env python3
"""Build complete replacement prompts from the frozen source snapshot."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
sources = sorted((ROOT / 'sources').rglob('*.md'))
manifest = []
for p in sources:
    body = p.read_bytes()
    manifest.append({'path': str(p.relative_to(ROOT)), 'bytes': len(body),
                     'sha256': hashlib.sha256(body).hexdigest()})

for harness, predecessor in [('claude', 'efa157'), ('codex', 'cf7879')]:
    sections = [f'''# Primary {harness} successor

You succeed {predecessor} at depth 1. Discover your actual harness identity before
creating a Flow lane. No identity is preassigned. Keep predecessor evidence;
do not recursively refresh. Pair with the other primary: Claude efa157 or its
confirmed successor, and Codex cf7879 or its confirmed successor. Before work,
report your actual identity and the context bodies you received. The existing
Codex primary thread is 01a0a715-2d5d-7342-b278-1dbcf78795bd.

Follow current user authorization and higher-priority harness instructions.
The source records below retain their provenance and historical status; their
presence does not adopt every proposal or reactivate historical launch orders.
Complete skill blocks carry their bodies once; report actual body presence,
not a fictional skill-loader call. Child inheritance remains unproved.

Primary owns development, design, prototypes and proofs of concept. Secondary
owns deployment and production tests under its generation and rollback gates.
Its Codex is 348e7b, thread 01a0a11f-6130-70e2-80b1-796348e7b086.

First work after readiness: Cloud Nexus DNS capability for
xmpp.goldragon.criome.net (inside: xmpp.goldragon.criome), then the XMPP accounts
and chime bot. Domains are configurable per cluster. Tokens pass from gopass
directly to the program, never an agent. Secondary applies the tested version.
TLS follows DNS. Keep the pending domain-federation policy explicit.

Report the weekly quota each working hour; the living decides when to consume
a reset credit. The prior pace hold is superseded. Do not consume a credit
yourself. Repository renames and whether to use MCP remain design decisions.

## Frozen current context
''']
    included = []
    for p, entry in zip(sources, manifest):
        if p.parent.name == 'skills' and p.stem in {'claude-harness', 'codex-harness'} and p.stem != harness + '-harness':
            continue
        body = p.read_text()
        if p.parent.name == 'skills':
            location = '/home/li/wt/github.com/LiGoldragon/Curriculum/efa157-branches/skills/' + p.name
            sections.append(f'\n<skill name="{p.stem}" location="{location}">\n' + body + '\n</skill>\n')
        else:
            sections.append(f'\n<source path="{entry["path"]}" sha256="{entry["sha256"]}">\n' + body + '\n</source>\n')
        included.append(entry['path'])
    text = ''.join(sections)
    (ROOT / f'{harness}-base.md').write_text(text)
    # Verify actual embedded bodies, including trailing newlines.
    for rel in included:
        assert (ROOT / rel).read_text() in text, rel

first = '''Discover your actual Flow identity and report readiness to your predecessor and
the paired primary through a supported route. State which complete skill bodies,
Spirit, Intent and Vision you hold. Use an independent JJ store, own lane and
bookmark; never move a shared checkout. Read the current paired report and orders
from the frozen packet, distinguishing proposals from witnessed results.
First implementation direction is Cloud Nexus DNS for xmpp.goldragon.criome.net,
with gopass-to-program secrets, followed by XMPP accounts and chime; secondary
owns activation. Do not rename repositories or install an MCP surface yet.
No further refresh. Do not claim laptop visibility until the user or a direct
desktop receipt confirms it. Report your exact thread/session and name.
'''
(ROOT / 'first-prompt.md').write_text(first)
(ROOT / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
artifacts = {}
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name != 'artifact-manifest.json' and '__pycache__' not in p.parts:
        artifacts[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT / 'artifact-manifest.json').write_text(json.dumps(artifacts, indent=2) + '\n')
print(json.dumps({h: (ROOT / f'{h}-base.md').stat().st_size for h in ['claude', 'codex']}))
