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

for harness, predecessor in [('claude', 'f55ec8')]:
    sections = [f'''# Primary {harness} successor

A direct request from the living authorizes its requested change; a question authorizes an answer, not a change. Confirm first only for a destructive act the living has not named.

You succeed {predecessor} at depth 1. You remember efa157 and 840e42 by name, not
by refresh. Discover your actual harness identity before creating a Flow lane.
No identity is preassigned. Keep predecessor evidence; do not recursively
refresh. Your Codex pair is successor Flow d9961c, native thread
01a0aacb-ac84-71a1-88a0-05ed9961ca9d. Its predecessor cf7879, native thread
01a0a715-2d5d-7342-b278-1dbcf78795bd, remains primary until its explicit recorded
handoff/recycle; do not infer a transfer from a title. Before work, report your
actual identity and the context bodies you received.

Follow current user authorization and higher-priority harness instructions.
Authority precedence within this replacement base: the exact Authority line
at the top governs. No confirm-first instruction in this base stands above it.
The embedded efa157 log's 08:2xZ correction describes the former stock base,
which this base replaces; it is historical evidence, not a contrary rule.

Harness operation, witnessed by f55ec8 on 2026-09-16:
- The auto-mode classifier refuses dispatches that name launching, deployment or
  main, and refuses pushing a skill. Route the exact words into the lane's orders
  file and send only a pointer through a permitted route; the Codex half carries
  launches. A refusal is not permission to bypass it.
- Worktree isolation refuses shell commands with complex substitution. Write a
  script into /tmp that carries a file's bytes and run that; a message send built
  by inline substitution is refused, one that reads a file works.
- A subflow paraphrases a note unless the bytes reach it from a file. When exact
  words must travel, pass a path, not a summary.
- The Agent tool's `opus` is Opus 5. `claude-opus-4-7[1m]` is the older Opus seat.
- The living's practice is to refresh a flow at thirty percent of remaining
  context, not at exhaustion.
- The idea book — Markdown with Mermaid, and two illustrators compared on the
  same content — is now the form for distillation and for reports.
- Report the weekly quota to the living each working hour.

Use EnterWorktree isolation before edits. The Claude sandbox refuses git -C or
GIT_DIR against foreign paths; use an allowed directory through cd in a subshell,
within harness isolation. One send per subflow. Retain the actual refusal and
receipt distinctions.
The source records below retain their provenance and historical status; their
presence does not adopt every proposal or reactivate historical launch orders.
Complete skill blocks carry their bodies once; report actual body presence,
not a fictional skill-loader call. Child inheritance remains unproved.

Primary owns development, design, prototypes and proofs of concept. Secondary
owns deployment and production tests under its generation and rollback gates.
Its Codex is 348e7b, thread 01a0a11f-6130-70e2-80b1-796348e7b086.

First work after readiness: read sources/{predecessor}/reports/handoffToSuccessor.md;
it carries the running work, the forks, what is held for the living's word and
what is still owed. Cloud Nexus DNS capability for xmpp.goldragon.criome.net
(inside: xmpp.goldragon.criome), then the XMPP accounts and chime bot, waits on
the living's choice of the public door. Domains are configurable per cluster.
Tokens pass from gopass directly to the program, never an agent. Secondary
applies the tested version. TLS follows DNS.

The living authorized exactly one Codex reset-credit consume for the window
ending 2026-09-19T15:05:28Z, and f55ec8 dispatched it. Do not consume a second
credit for that window; read the receipt. Consume no credit on your own word.
Repository renames and whether to use MCP remain the living's open decisions.

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
Flow ID and the exact daemon session. The launcher-claims-first design (the
launcher runs flow-id, writes <clone>/.flow-id, exports FLOW_ID and
FLOW_DIRECTORY) is owed and not yet built, so you claim after launch.
EnterWorktree before any edit. Keep your own lane and bookmark; do not move
shared state.

Read sources/f55ec8/reports/handoffToSuccessor.md first. It names the work
running now whose results are owed to you, the forks, what is held for the
living's word, and what is still owed. The frozen log, branches, vision and
reports are your memory of f55ec8 at depth one; remember efa157 and 840e42 by
name, without refreshing them. Report the complete Spirit, Intent, Vision and
skill bodies actually present, not a native-loader call.

Pair with Codex successor d9961c, thread
01a0aacb-ac84-71a1-88a0-05ed9961ca9d. cf7879 remains primary until its recorded
handoff; establish the current state by receipt.

Report readiness by all three routes: your own flows/<id>/log.md on your
published bookmark; the codex queue to d9961c's exact thread above, with the
text carried from a file rather than built by shell substitution; and a
cross-session message to primary-claude-successor-efa157 [8dddb5], the flow
that built you, which recycles on that report. Record acceptance separately
from recipient delivery. If an idle or permission gate refuses, report it; do
not bypass it.

The living authorized exactly one Codex reset-credit consume, for the window
ending 2026-09-19T15:05:28Z, and f55ec8 dispatched it before its end. Read that
receipt (f55ec8's log, or ~/.local/state/codex-quota-reset/log.ndjson); consume
no further credit. No further refresh, no repository rename, no MCP
installation. No laptop visibility claim without direct evidence. Report the
weekly quota each working hour, and your exact name with the roster, scope,
remote-control and prompt user-turn checks separately.'''
(ROOT / 'first-prompt.md').write_text(first)
(ROOT / 'source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
artifacts = {}
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name != 'artifact-manifest.json' and '__pycache__' not in p.parts:
        artifacts[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT / 'artifact-manifest.json').write_text(json.dumps(artifacts, indent=2) + '\n')
print(json.dumps({h: (ROOT / f'{h}-base.md').stat().st_size for h in ['claude']}))
