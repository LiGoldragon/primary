# Flow artifacts protocol

Flow 5c8be3ca (design) · 2026-08-21 · draft, revised in-session per rulings
5c8be3ca-1 through 5c8be3ca-6

## What this is, what is wanted, why

A flow is one running model session and its context. Flows produce
artifacts that have no specific home repository — research reports,
witnessed observations, handoffs, backups. Wanted: one place where every
such artifact files by its origin, so that any artifact is reachable from
its flow's short id and any claim can be walked back to the conversation
that produced it. Why: this completes the chain of origin — provenance
written at creation, never reconstructed later.

## Grounding

Psyche records this draft builds on:

- Chain of origin: the short session id beside every record lets a later
  flow verify the whole conversation (psycheLogStructure.md, 06196cc7).
- Session-scoped ids (psycheLogStructure.md, fb1008c0-1).
- The pronounced session-log statement: one file per session named by
  short id, terse opening summary, index whose tail is latest, addenda
  only from other sessions (session-log.md, 7c3f0c1d-1).
- The verified/ ledger: root `verified/`, re-verifications append; a
  ledger skill owed with deep research (verifiedInformation.md, 7c3f0c1d).
- "every concept should really have its repo" (98fbfa47).
- This session's brief: per-flow short-id directories in a dedicated
  repository, private variant, witnessed/reports kinds, subflow marking
  (sessions/design/5c8be3ca.md).
- The directory gives the flow and no artifact carries origin marks —
  subflow marking dropped since a subflow cannot see its own id; no
  handoff file — succession is the new flow reading the old; the structure
  lives in the workspace for now; context-handover renames to say what it
  is — manual prompt generation (flowArtifacts.md, 5c8be3ca-1 through -5).

## Witnessed harness facts (this session's subflows; local file evidence)

- Claude Code and Codex both share one session id across a flow's whole
  subflow tree. A Claude subagent's records carry the parent's sessionId
  plus its own `agentId`; a Codex subagent thread carries the root's
  `session_id` plus its own thread `id` and `parent_thread_id`.
- So the short session id genuinely names the whole flow tree in both
  harnesses, and each subflow has a distinct harness-native sub-identifier.
- A flow can read its own session UUID from `CLAUDE_CODE_SESSION_ID`. A
  Claude subagent cannot learn its own agentId by any witnessed mechanism;
  the parent can (spawn metadata). Confirmed in practice this session: the
  research subflow could not self-identify in its report header.

## The protocol

`flows/` at the workspace root holds one directory per flow, named by the
short id — the first 8 hex of the session UUID. The directory's shape is
the future repository's shape.

    flows/
      index.md
      <short-id>/
        log.md
        witnesses/<subject>.md
        reports/<subject>.md

`log.md` is the flow's self-witness: created at the first prompt, opening
with a very terse summary re-edited as the session goes, changing further
when asked, at handoff, or when the handoff state materially changes. The
flow's line joins `flows/index.md` as `<aspect>, <short-id>,
<description>`; the tail is the latest.

A witness goes in `witnesses/<subject>.md` with its method — `Method:
probe <command>` or `Method: code read <path>`. A report goes in
`reports/<subject>.md`, ending with `## Sources` written as the report is
made: documents and URLs for carried claims, witness records for own
inference, flows by short id.

Files are named by camelCase subject; the log holds the dates; an
artifact's body holds only its subject. A subflow's artifacts go in its
flow's directory.

Earlier work is continued by reading the flows concerned and forming a
fresh view. Another flow's artifact is built on by an addendum marked
with the building flow's short id, or by a new artifact linking it.

The subject-keyed stores — `psyche/` by topic, `verified/` by subject —
cite into flows by short id.

The refused shapes and the reasoning behind each rule live in
psyche/Vision/flowArtifacts.md (5c8be3ca-1 through -7), out of the
composition.

## Skill proposal

The `flows` skill replaces `session-log`, deployed through the skills
repository on approval. Reference collections searched: neither
superpowers nor anthropics/skills covers this situation (nearest cousin:
the managed-agents memory store, infrastructure not workflow). The
reasoning — chain of origin, the witnessed/reported ground, why a
successor pulls — goes in a parallel `flows-rationale` skill for
psyche-facing flows.

Description (the trigger):

    A session is starting, or work has produced something with no home
    repository.

Body:

    One directory per flow: `flows/<short-id>/`, the short id being the
    first 8 hex of the session UUID.

        flows/
          index.md
          <short-id>/
            log.md
            witnesses/<subject>.md
            reports/<subject>.md

    Create `log.md` at the first prompt and append the flow's line to
    `flows/index.md` as `<aspect>, <short-id>, <description>`; the tail
    is the latest. The log opens with a very terse summary, re-edited as
    the session goes, and changes further when asked, at handoff, or when
    the handoff state materially changes.

    A witness goes in `witnesses/<subject>.md` with its method: `Method:
    probe <command>` or `Method: code read <path>`. A report goes in
    `reports/<subject>.md` and ends with `## Sources` written as the
    report is made: documents and URLs for carried claims, witness
    records for own inference, flows by short id.

    Files are named by camelCase subject; the log holds the dates; an
    artifact's body holds only its subject. A subflow's artifacts go in
    its flow's directory.

    Earlier work is continued by reading the flows concerned and forming
    a fresh view. Another flow's artifact is built on by an addendum
    marked with the building flow's short id, or by a new artifact
    linking it.

## Merge map

Becomes the concept:

- `sessions/<lane>/<short-id>.md` → `flows/<short-id>/log.md`
- `sessions/index.md` → `flows/index.md` (seed rows, lane column kept)
- `reports/FlowArtifactsPriorArt-2026-08-21.md` →
  `flows/5c8be3ca/reports/flowArtifactsPriorArt.md` (this session's own
  output: the first exercise of the protocol)
- `spiritbackup.nota` → its origin flow's directory

Stays behind, archived with the workspace repository at its reset:

- timestamp-named session files whose short id would need hunting
- `handoffs/*.md` — artifacts of the retired handoff concept; a successor
  reads its predecessor's flow directory instead (5c8be3ca-2)
- the ~101 dated `reports/` files not cheaply traceable to an origin flow
- `reports/` task-named subdirectories and `agent-outputs/` (~147 MB):
  task-keyed subflow returns of the old scheme — the bulk of the workspace
  weight; going forward subflow output files under its parent flow
- `sessions/design.log` — a narrative view dissolved into per-flow logs

Not this concept:

- `protocols/`, `awareness/*.md`, `design/` (project-keyed ruled designs),
  `verified/`, `psyche/`, `psyche-archive/`
- `result*`, `results.txt`, `librust_out.rmeta` — build litter for disk
  hygiene, not artifacts

Migration is forward-only: seed the index and the short-id-named logs; an
old artifact moves only when a flow needs it and its origin is known. No
compatibility path: once flows/ exists, sessions/ is retired and every
consumer — the session-log skill first — is regenerated to the new shape.
The context-handover skill is not a succession mechanism to retire: it
generates prompts for other flows that the psyche pastes manually, and it
renames to `prompt-crafting` (5c8be3ca-5; name ruled good, 5c8be3ca-6).

## Prior-art anchors

reports/FlowArtifactsPriorArt-2026-08-21.md, fifteen-item shortlist.
Adopted: origin id embedded in every artifact key (1); distinct
per-subflow ids on a spawn-edge graph (2); construction-time source lists
(3, 15 — the LEDGER source-pointer requirement); the log as primary
source all else derives from (4); witnessed/reported as the universal
minimum binary from evidentiality typology (5); confidence orthogonal to
source kind (6); witnessed = independently re-verifiable as the
operational test (7); attribution permanent, never collapsing into the
author's voice on promotion (8); supersession by annotation with the
superseding source linked (13); the per-flow directory always populated
(14). Considered, not adopted now: dotted-order encoded ancestry (10) and
PROV/in-toto vocabularies (11, 12) — machinery beyond current need,
revisit when flows becomes a nexus.

## The forks, ruled (5c8be3ca-6)

1. Kind subdirectories: ruled — "subdirectories; easier to search".
2. Consumer regeneration timing: open. The psyche questioned the term
   "pronouncement" — used in psyche records but never defined in the
   vocabulary skill — and directed research to establish the anatomy of
   the flow and of LLM-based engineering; the timing question resolves
   once that vocabulary stands.
3. The legacy topic journals stand as derived views; the term "awareness"
   is rooted out of current use.
4. The context-handover skill renames to `prompt-crafting` — ruled good.
