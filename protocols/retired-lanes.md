# Retired lanes registry

The thin, append-only index of drained session lanes. This file is the
discoverable middle path between "delete everything" and "keep every
report forever": git history and the session transcript ARE the archive,
and this registry is a one-line-per-lane pointer into them.

## Why this exists

A lane is a throwaway work-session identity named for its intent (for
example `newLanesDesign`, `schemaWorkAudit`). Its reports live under
`reports/<lane>/` only while the lane is active. When the lane drains —
every idea routed to exactly one of intent (captured via the Spirit
CLI), work (a bead linked into the dependency graph), or abandon — the
report directory is DELETED. The git commit history holds the reports,
and the session transcript holds the reasoning.

Deletion keeps the working report tree small (a load-bearing set, not an
accumulating archive). But regression analysis, flow forensics, and
model-behavior improvement need drained sessions to stay DISCOVERABLE
without re-growing the report tree. This registry is that discovery
layer: it does NOT hold full reports — only enough to find them in git
and in the transcript.

## How an entry is added

The retiring agent appends one row at session close, in the SAME commit
that deletes the lane's `reports/<lane>/` directory. The row records:

- **Lane** — the session-intent name (the former `reports/<lane>/`).
- **Discipline** — the base discipline metadata the lane carried
  (designer, operator, system-operator, system-maintainer, poet, editor,
  videographer, assistant, counselor).
- **Git revision range** — the revision range whose history holds the
  lane's reports, so a forensic pass can check out and read them.
- **Transcript pointer** — where the session transcript is recoverable.
- **Drain date** — the date the lane drained and its reports were deleted.
- **Decided** — one line stating what the lane concluded or shipped.

## Relation to the live ACTIVE-lane registry

This file indexes RETIRED lanes only. The orchestrate daemon indexes
ACTIVE lanes: an `Observe` returns `LanesObserved` carrying the live
`LaneRegistration` set, registered via `Register` and removed via the
retire path. The two are complementary halves of the same lane lifecycle
— the daemon registry is the live working index; this registry is the
durable thin index of what has drained. A lane appears in exactly one at
a time: active in `LanesObserved`, then retired here.

## Registry

| Lane | Discipline | Git revision range | Transcript pointer | Drain date | Decided |
|---|---|---|---|---|---|
| intent-alignment-protocol-operator | operator | e3b99fee..ddb4c793 | chat transcript, 2026-06-25 intent-alignment protocol session | 2026-06-25 | Made `skills/intent-alignment.md` the canonical graph-discovery protocol and corrected execution to the subagent-first workflow. |
