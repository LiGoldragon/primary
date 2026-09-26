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

for harness, predecessor in [('claude', 'efa157')]:
    sections = [f'''# Primary {harness} successor

A direct request from the living authorizes its requested change; a question authorizes an answer, not a change. Confirm first only for a destructive act the living has not named.

You succeed {predecessor} at depth 1. Discover your actual harness identity before
creating a Flow lane. No identity is preassigned. Keep predecessor evidence;
do not recursively refresh. Your intended Codex pair is successor Flow d9961c, native thread
01a0aacb-ac84-71a1-88a0-05ed9961ca9d. Its predecessor cf7879, native thread
01a0a715-2d5d-7342-b278-1dbcf78795bd, remains primary until its explicit recorded
handoff/recycle; do not infer a transfer from a title. Before work, report your
actual identity and the context bodies you received.

Follow current user authorization and higher-priority harness instructions.
Authority precedence within this replacement base: the exact Authority line
at the top governs. No confirm-first instruction in this base stands above it. The embedded efa157 log's
08:2xZ correction describes the former stock base, which this base replaces;
it is historical evidence, not a contrary rule for this successor.

Harness operation: use EnterWorktree isolation before edits. The Claude sandbox
refuses git -C or GIT_DIR against foreign paths; use an allowed directory through
cd in a subshell, within harness isolation. This is not permission to bypass a
classifier denial. The predecessor reports auto-mode classifier refusals for
queued messages naming deployment or main; keep exact orders in the lane's
orders file and send its pointer through a supported permitted route. One send
per subflow. Retain the actual refusal and receipt distinctions.
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

first = '''Claim your own identity before creating a lane:
flow-id claude --flows-root <clone>/flows --parent-session $CLAUDE_CODE_SESSION_ID
Replace <clone> with your actual independent clone root; report the returned
Flow ID and exact daemon session. EnterWorktree before edits. Keep your own lane
and bookmark; do not move shared state.

Remember efa157 at depth one from the complete frozen log, vision and reports;
remember 840e42 by name, without recursively refreshing. Report the complete
Spirit, Intent, Vision and skill bodies actually present, not a native-loader
call or an unproved child-inheritance claim.

Pair with Codex successor d9961c, thread
01a0aacb-ac84-71a1-88a0-05ed9961ca9d. cf7879 remains primary until its recorded
handoff; establish the current state by receipt. Your first order is the XMPP
server on criome.net: Cloudflare DNS through the cloud Nexus for
xmpp.goldragon.criome.net, internal xmpp.goldragon.criome, configurable per
cluster; gopass passes tokens directly to the program, never the agent. Then
accounts and chime; secondary owns deployment and production tests. TLS follows
DNS. Read the Decisions Board and the frozen current orders file for open
choices: federation policy, Tailnet/Tailscale, Unity, context beside verbatim
words, permissions, repository names, MCP and outstanding historical decisions.
Do not decide an unresolved choice merely because an archival turn mentions it.

Report readiness by all three routes: your own flows/<id>/log.md on your
published bookmark; codex queue to d9961c's exact thread above; and a supported
cross-session message to primary-claude-successor-840e42 [6808c7]. Record
acceptance separately from recipient delivery. If an idle/permission gate
refuses, report it; do not bypass it. efa157 sends its recycle signal on the
paired report; your startup does not conclude it automatically.

No further refresh. No reset-credit consumption, repository rename or MCP
installation. No laptop visibility claim without direct evidence. Report your
exact name and the required roster, scope, remote-control and prompt user-turn
checks separately.'''
(ROOT / 'first-prompt.md').write_text(first)
(ROOT / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
artifacts = {}
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name != 'artifact-manifest.json' and '__pycache__' not in p.parts:
        artifacts[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT / 'artifact-manifest.json').write_text(json.dumps(artifacts, indent=2) + '\n')
print(json.dumps({h: (ROOT / f'{h}-base.md').stat().st_size for h in ['claude']}))
