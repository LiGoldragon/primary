# 5c8be3ca — design — flow-artifacts protocol

Design session with the psyche, 2026-08-21. Subject: the flow-artifacts
protocol — anything a flow produces that has no specific home repository
files under flows/<short-id>/, workspace-local for now, with kind
subdirectories (witnesses/, reports/) and log.md as the self-witness; no
origin marks — the directory gives the flow; no handoff file — a successor
reads its previous flow(s) and makes its own view.

DELIVERED: design/Flows/flowArtifactsProtocol-2026-08-21.md — the protocol
recomposed as pure composition per ruling 5c8be3ca-7 (refusals moved out to
the psyche log), with the `flows` skill proposal replacing session-log,
approval-gated. Prior-art research at
flows/5c8be3ca/reports/flowArtifactsPriorArt.md and
flowAnatomyVocabulary.md. Reference skill collections searched: no
existing skill covers the situation. LANDED (5c8be3ca-9): flows skill in
Curriculum sources (verbatim), session-log removed, context-handover
renamed prompt-crafting, design/realization dependencies repointed,
manifests updated, trees regenerated (Curriculum e307e14d, workspace
47abf454), duplicated short-id session logs deleted after byte-compare.
Witnessed live: this session's skill roster now lists flows and
prompt-crafting. sessions/design/15b67974.md diverged from its flows log
(neither a superset) — left in place, noted in
flows/15b67974/annotations.md, the first protocol-native annotation.
Still open: the pronouncement vocabulary entry; the superseded-marking of
VISION-2026-08-07.md:566; a prompt-crafting body line still says
"handover" — reword proposal owed to the psyche.

## Grounding read

psyche/Vision/psycheLogStructure.md (chain of origin, 06196cc7; session-
scoped ids fb1008c0-1), session-log.md (pronounced statement 7c3f0c1d-1),
verifiedInformation.md (verified/ ledger rulings and the deep-research
directive, 7c3f0c1d), flowKnowledge.md (session files must become
searchable, e06e4c07), workspace-2.0.md, everyConceptShouldHaveItsRepo.md,
highLevelView.md.

## Rulings received (logged psyche/Vision/flowArtifacts.md)

The directory gives the flow, no origin line (5c8be3ca-1); no handoff file
— a new flow reads its previous flow(s), LLM flows being non-deterministic
(5c8be3ca-2); subflow marking dropped — a subflow cannot see its own id
(5c8be3ca-3); workspace-local for now, kept simple (5c8be3ca-4);
context-handover is manual prompt generation and renames (5c8be3ca-5);
forks ruled: kind subdirectories, legacy topic journals stand as derived
views with "awareness" rooted out of current use, prompt-crafting name good
(5c8be3ca-6).

## Findings

Claude Code subagent identity (guide subflow + local transcript witness):
subagents do NOT get their own session UUID — every subagent record carries
the parent's sessionId plus its own agentId; layout
`<session-uuid>/subagents/agent-<agentId>.jsonl` with .meta.json
(agentType, toolUseId, parentAgentId, spawnDepth). Codex agrees in
structure: shared session_id, per-thread UUIDv7 id, parent_thread_id,
lineage embedded in each rollout. One session id names the whole flow tree
in both harnesses. A flow reads its own UUID from CLAUDE_CODE_SESSION_ID;
a Claude subagent cannot learn its own agentId.

Inventory (Explore subflow): reports/ = 101 flat dated .md (~13MB) + 46
task-named subdirs; verified/ has a README-as-protocol (subject-keyed,
citing session short ids); handoffs/ = 12 cross-session files;
awareness/sessions/*.log = topic journals, entries short-id-tagged;
agent-outputs/ = ~1001 task-named dirs, 147MB, the workspace's bulk.

Root-out survey ("awareness"): zero current-use hits in authored skill
sources, workspace instruction docs, protocols/, and manifests. All
current-use hits sit in design/ documents. The one live ruled use is
design/ProtosEngine/VISION-2026-08-07.md:566 "The awareness file supersedes
the reset bead as the session carrier" — substance superseded by this
protocol's log.md. The rest are provenance attributions (*source: awareness
record*) and verbatim psyche quotes — mentions, not uses.

Anatomy research: "pronouncement" is established in law and ecclesiastical
usage — the formal act of an authority declaring a decision and directing
it into the record — and absent from software and LLM engineering, which
name the same act acceptance (ADR), publication (IETF/W3C), or approval
(ISO). Our usage maps to the legal act; alternatives miss the moment of
authoritative declaration. flow, subflow, distillation are our coinages
(AlphaCodium's "flow" names a pipeline, not a bounded session);
witness/claim, ruling, dispatch are grounded; turn, context window,
trace/run/span are the established session-internals vocabulary (OTel
GenAI, LangSmith). No published work joins session anatomy with the
human-agent decision acts in one place.

Concurrent seed: flows/ was created and seeded by a concurrent design flow
(commits through "sessions: 15b67974 — whole-board visual published"):
per-flow log.md for 01a01b52, 15b67974, 2b34fafa, 5c8be3ca, e06e4c07; an
index.md in the ruled format; this session's prior-art report moved to
flows/5c8be3ca/reports/flowArtifactsPriorArt.md exactly as the draft's
merge map specifies. sessions/ remains alive in parallel — including a new
timestamp-named file written today (sessions/design/2026-08-21T202325.md)
under the old skill — two shapes live simultaneously; session-log skill
regeneration is urgent. This log is synced to sessions/design/5c8be3ca.md
until retirement of sessions/ is ruled. Lane registration for edit
coordination was attempted and refused twice (DOTOS shape error: "expected
LaneRegistrationRequest to be a brace block"); continuing unregistered per
the skill.

## Dispatched

- Web prior-art research → flows/5c8be3ca/reports/flowArtifactsPriorArt.md
  (landed).
- claude-code-guide subagent-identity question (landed).
- Local transcript witness, Claude + Codex (landed).
- Merge-candidate inventory (landed).
- Flow-anatomy / LLM-based-engineering vocabulary research →
  flows/5c8be3ca/reports/flowAnatomyVocabulary.md (landed).
- "awareness" current-use survey (landed).
