# 5c8be3ca — design — flow-artifacts protocol

Design session with the psyche, 2026-08-21. Subject: a protocol for flow
artifacts — anything a flow produces that has no specific home repository —
built on the session short-id concept: one directory per flow named by its
short id, in a dedicated flows repository (a private variant possible), with
artifact kinds beneath it (witnessed, reports, the session log), an index in
the same shape as the sessions index, and subflow artifacts filed under the
parent flow marked with the subflow's own short id.

DELIVERED: design/Flows/flowArtifactsProtocol-2026-08-21.md — the protocol
draft with merge map, awaiting pronouncement. Prior-art research at
reports/FlowArtifactsPriorArt-2026-08-21.md. Implementation (repository
creation, skill regeneration, index seeding) not started — blocked on
pronouncement.

Rulings received in-session (logged psyche/Vision/flowArtifacts.md): the
directory gives the flow, no origin line (5c8be3ca-1); no handoff file — a
new flow reads its previous flow(s) and makes its own view, since LLM flows
are non-deterministic (5c8be3ca-2); subflow marking dropped entirely, since
a subflow cannot see its own id (5c8be3ca-3); the structure lives in the
workspace for now, kept simple — dedicated repository deferred to the
workspace reset (5c8be3ca-4); context-handover is manual prompt generation
and renames to say so (5c8be3ca-5, name proposal prompt-crafting). Draft
revised after each ruling; handoffs/ moved to stays-behind in the merge
map. Open forks: kind subdirs vs flat, consumer regeneration timing,
awareness logs as views, the renamed skill's name.

## Grounding read

psyche/Vision/psycheLogStructure.md (chain of origin, 06196cc7; session-scoped
ids fb1008c0-1), session-log.md (pronounced statement 7c3f0c1d-1),
verifiedInformation.md (verified/ ledger rulings and the deep-research
directive, 7c3f0c1d), flowKnowledge.md (session files must become
searchable, e06e4c07), workspace-2.0.md, everyConceptShouldHaveItsRepo.md,
highLevelView.md.

Tension surfaced: the deployed session-log skill still prescribes
timestamp-named files with frontmatter; the later pronounced statement
(7c3f0c1d-1) and newest practice (sessions/design/e06e4c07.md) use short-id
names without frontmatter. This session follows the pronounced statement.

## Findings

Claude Code subagent identity (guide subflow, witnessed in local transcript
files): subagents do NOT get their own session UUID. They get an `agentId`
(shorter hex, e.g. 17 hex chars); every record in a subagent transcript
carries the PARENT's sessionId. Layout: `<session-uuid>.jsonl` beside
`<session-uuid>/subagents/agent-<agentId>.jsonl` plus a `.meta.json` carrying
`agentType`, `toolUseId`, `parentAgentId`, `spawnDepth`. So the psyche's
guess (subagents have different session ids) is false for Claude Code: the
session id is shared; the agentId is the distinct mark. A flow can read its
own session UUID from `CLAUDE_CODE_SESSION_ID`; a subagent cannot learn its
own agentId by any documented mechanism.

Transcript witness (local files, two Claude sessions + Codex rollouts):
confirms the above for Claude Code independently (`isSidechain:true` only in
subagent files; parent jsonl has none). Codex differs in mechanism but agrees
in structure: every thread gets its own rollout file and its own UUIDv7
thread `id`, while `session_id` stays the root's; `parent_thread_id` links to
the immediate parent, `thread_spawn` carries depth/agent_path/nickname, and
each subagent rollout embeds ancestor session_meta (full lineage in-file).
Convergent shape across both harnesses: ONE shared session id per flow tree,
plus a distinct per-subflow identifier with parent linkage. Codex rollout
files are filed by activity date, not session start.

Inventory (Explore subflow): reports/ = 101 flat dated .md (~13MB) + 46
task-named subdirs (agent-outputs-shaped); one filename already carries a
short id (spirit-vision-recovery-019fad58.md). verified/ already has a
README-as-protocol: one file per subject, each fact a ## heading with
`- <date> · session <short-id> · method:` lines — topic-keyed, citing flows.
handoffs/ = 12 cross-session context-passing files. sessions/ = index.md
(lane, short-id, description rows) + design.log (13-entry narrative journal
by short id) + per-lane files, 3 of 20 already short-id-named.
awareness/sessions/*.log = topic journals, every entry short-id-tagged.
agent-outputs/ = ~1001 task-named dirs, 147MB — filed by task/bead, not by
session; the bulk of the workspace weight. Strays: spiritbackup.nota is an
unfiled flow artifact; result* symlinks/rmeta/results.txt are build litter.

## Dispatched

- Web prior-art research (agent artifact/memory systems; witnessed vs
  reported knowledge theory; session-id-centric workflows; Codex session
  ids) → report owed in reports/.
- claude-code-guide: subagent session identity in Claude Code (docs claim).
- Local inventory of merge candidates (reports/, verified/, handoffs/,
  agent-outputs/, sessions/, protocols/, awareness/, stray result files).
- Local transcript witness: whether subagents carry their own session ids,
  in Claude Code and Codex session files.
