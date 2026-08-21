# Flow artifacts protocol

Origin: flow 5c8be3ca (design) · 2026-08-21 · draft, awaiting pronouncement

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

**Repository.** `flows` — its own repository. A private sibling
`flows-private` holds private flows under the identical protocol. Each
repository carries its own index.

**Layout.**

    flows/
      index.md
      <short-id>/
        log.md                    always present
        handoff.md                when a handoff exists
        witnesses/<subject>.md    created on use
        reports/<subject>.md      created on use

Flat by short id: the lane/aspect is an index column and a log.md header
line, not a directory level. File names are camelCase subjects without
dates — the flow supplies the origin and the log supplies the dates.

**The three kinds.**

- `log.md` — the flow's self-witness. Content rules are the pronounced
  statement 7c3f0c1d-1 unchanged: terse opening summary re-edited as the
  session goes; changes only when asked, at handoff, or on material
  handoff-state change; other flows append addenda marked with their own
  short id and never alter existing text.
- `witnesses/` — observations of the thing itself: a probe run, a test
  run, code actually read. The operational test: independently
  re-verifiable from what the file states.
- `reports/` — relayed or derived material: external research,
  documentation-based or opinion-based synthesis. Claims stay claims.

There is no separate "inferred" kind. A derivation from the flow's own
observations is a report whose source list points at witness records; the
source list is what distinguishes a carried-over claim from own inference.
A witness is not a truth claim and a report is not doubt — confidence is
orthogonal to kind and is stated in the artifact when it matters.

**Origin line.** Every artifact opens, directly under its title:

    Origin: flow <short-id> [· subflow <harness sub-id>] · <ISO date>

A witness adds `· method: probe <command>` or `· method: code read <path>`,
the verified/ README convention. Markdown, never frontmatter.

**Sources.** A report ends with a `## Sources` list written at
construction time — URLs, documents, witness records, other flows by short
id — never reconstructed at read time.

**Subflows.** A subflow's artifact files under its parent flow's directory;
the session id already names the whole tree. The subflow mark in the origin
line is the harness's own identifier (Claude agentId, Codex thread id).
What a subflow cannot know about itself, the flow stamps — the flow is
liable for its subflows. `log.md` lists dispatched subflows with their ids
and one-line purposes.

**Index.** `index.md`, append-only, one line per flow, tail is latest:

    <lane>, <short-id>, <description>

The same shape as today's sessions/index.md, which seeds it.

**Supersession.** A later flow never rewrites an artifact: it appends an
addendum marked with its own short id, or writes its own artifact linking
the superseded one. Contradicted content is annotated, not erased.

**Relationship to subject-keyed stores.** The flows repository is
origin-keyed primary storage. Subject- and topic-keyed stores stand and
cite into it by short id:

- `psyche/` — topic-keyed, unchanged (ruled: classified by agent-generated
  topics).
- `verified/` — the subject-keyed fact ledger, unchanged; its
  `session <short-id>` citations resolve into flows/. This is where
  "ledgers" live; no per-flow ledger kind is needed.
- `awareness/sessions/*.log` — topic journals whose entries are already
  short-id-tagged; they stand as derived views.

## Merge map

Becomes the concept:

- `sessions/<lane>/<short-id>.md` → `flows/<short-id>/log.md`
- `sessions/index.md` → `flows/index.md` (seed rows, lane column kept)
- `handoffs/*.md` → `flows/<short-id>/handoff.md` where the origin flow is
  known
- `reports/FlowArtifactsPriorArt-2026-08-21.md` →
  `flows/5c8be3ca/reports/flowArtifactsPriorArt.md` (this session's own
  output: the first exercise of the protocol)
- `spiritbackup.nota` → its origin flow's directory

Stays behind, archived with the workspace repository at its reset:

- timestamp-named session files whose short id would need hunting
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

## Open forks for pronouncement

1. Repository names: `flows` and `flows-private`.
2. Kind subdirectories (`witnesses/`, `reports/`) versus a flat flow
   directory with kind only in the origin line. Draft chooses
   subdirectories, created on use.
3. `handoff.md` as a plain file versus a section of `log.md`. Draft
   chooses the plain file — a handoff is consumed whole by a successor.
4. When consumers regenerate: at pronouncement (draft's choice —
   replacement kills the old system) or held until the workspace reset.
5. `awareness/sessions/*.log`: stand as derived views (draft's choice) or
   regenerate from flows later.
