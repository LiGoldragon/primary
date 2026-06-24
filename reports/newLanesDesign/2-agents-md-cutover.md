---
title: 2 — AGENTS.md cutover to the session-lane model
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [lanes, disciplines, sessions, reports, AGENTS, cutover]
description: |
  Reframes /home/li/primary/AGENTS.md from the nine fixed role-lanes (plus the
  ordinal/qualifier zoo) to the session-lane model: discipline is persistent
  metadata, a lane is a throwaway session named for its intent. Updates
  required reading, the where-things-live table, the reports section (drain-and-
  retire + fresh-context pickup point), and the disciplines section. Leaves the
  ESSENCE.md / INTENT.md required-reading lines untouched (8rpu out of scope).
---

# 2 — AGENTS.md cutover to the session-lane model

## What changed in `/home/li/primary/AGENTS.md`

The file now teaches the dynamic session-lane model end to end. A
fresh-context agent reading it learns: a discipline is the persistent
identity (skills, authority, persona-mind, signing key); a lane is one
work session named for its intent; the lane carries its discipline as the
last token of its orchestrate registry role vector; reports live in a
per-session directory that drains and retires.

### (a) Disciplines and lanes section (was "Roles")

- Retitled `## Roles` to `## Disciplines and lanes`.
- Kept the nine disciplines and their one-line descriptions verbatim
  (only `counselor`'s trailing "assistant lane" became "assistant
  discipline").
- Replaced the fixed-lane preamble. A discipline is now stated as the
  persistent identity that loads skills/authority/persona-mind. A lane is
  a single session named for its intent, carrying its discipline as
  metadata via the registry role vector (`[NewLanesDesign Designer]`).
- Removed the enumerated fixed-lane zoo as the lane model: the prose now
  says `second-<role>`, `third-<role>`, `<qualifier>-<role>` are retired
  as the lane model; additional capacity is just another session lane on
  the same discipline.
- Kept specialized scope as discipline metadata, not a separate lane
  name: cluster-scoped operator session, schema-scoped operator/designer
  session, Pi-harness operator session — scope tokens precede the base
  discipline in the role vector and tune authority + reading, not lane
  identity.
- Stated how an agent knows its lane: the session identity the harness
  gives it, the intent name owning `orchestrate/<lane>.lock` and
  `reports/<lane>/`; register via the daemon `Register
  [LaneRegistrationRequest (Role LaneAuthority)]` so it lands in
  `LanesObserved`, retire via the daemon retire path on drain; pointer to
  `skills/session-lanes.md`.
- Updated the coming **auditor** note: "auditor discipline" and "session
  mechanics still open"; dropped the now-stale `reports/auditor/`
  reference.

### (b) Where-things-live table

- `reports/<role>/` row became `reports/<lane>/`: a session directory for
  one lane, the garbage-collection unit, deleted when the lane drains.
- Added a `protocols/retired-lanes.md` row: the append-only thin index of
  drained lanes (name, discipline, git revision range, transcript
  pointer, drain date, one-line decision) — the retired-lane counterpart
  to the daemon's live `LanesObserved`.
- `orchestrate/AGENTS.md` description reworded to "Discipline-and-lane
  coordination protocol."

### (c) Reports section

- `reports/<role>/<N>-<topic>.md` became `reports/<lane>/<N>-<topic>.md`
  with a note that `<lane>` is the session-intent name and numbering is
  per-lane.
- The meta-report paragraph now says the session lane's own
  `reports/<lane>/` directory is the meta-report (frame in
  `0-frame-and-method.md`, numbered sub-agent reports, synthesis
  highest-numbered) — no more `reports/<role>/<N>-<session-name>/`.
- Added the fresh-context pickup-point principle: a report is written so a
  clean-context agent can pick the work up, reason, and where
  implementable implement it; implementable work links into a bead
  dependency graph; a continuation/review report supersedes and deletes
  its predecessor in the same commit.
- Added the drain-and-retire lifecycle: run fresh over endless
  compaction; at close every idea routes to intent / work-bead / abandon;
  on drain the `reports/<lane>/` directory is deleted (git + transcript
  are the archive) and one entry is appended to
  `protocols/retired-lanes.md`.

### (d) Required reading

- Item 5 (`orchestrate/AGENTS.md`) reworded to "how disciplines and
  session lanes share this workspace."
- Inserted a new item 6 pointing at `skills/session-lanes.md` (the rename
  target of `role-lanes.md`, owned by another slice).
- Old item 6 ("Your role's `skills/<role>.md`") became item 7, reframed to
  "Your discipline's `skills/<discipline>.md`" with a note that every
  session lane loads the file for the discipline it carries.
- Old item 7 (repo `INTENT.md`) renumbered to item 8.

## Held verbatim

- The `ESSENCE.md` and `INTENT.md` required-reading lines (items 1–2) —
  the 8rpu deprecation drift is explicitly out of scope.
- Every hard override except the two-word `reports/<role>/` →
  `reports/<lane>/` and `private-repos/<role>-reports/` →
  `private-repos/<discipline>-reports/` fixes in the "No
  harness-dependent memory" override. The dispatch and code-repo
  overrides use "lane" generically for "a session in that discipline"
  and reference neither `reports/<role>/` nor the fixed-lane zoo, so they
  stand verbatim.

## Cross-slice dependency

This file now references `skills/session-lanes.md` (item 6 of required
reading and the disciplines section) and `protocols/retired-lanes.md`
(where-things-live table and reports section). Both are created by other
slices in this fleet; once they land, every AGENTS.md pointer resolves.
The `skills/skills.nota` index still lists `role-lanes` at the old path —
that index is owned by another slice and is the remaining loose pointer.
