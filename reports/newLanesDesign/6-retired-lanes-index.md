---
title: 6 — retired-lanes thin registry
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [lanes, archival, retirement, forensics, orchestrate]
description: |
  Created protocols/retired-lanes.md, the append-only thin index of drained
  session lanes. Resolves the session's one open fork (frame report 0) in
  favor of the psyche-confirmed thin Option B: git history + session
  transcript are the archive; this registry is the discoverable pointer into
  them, holding no full reports. Documents the entry format, the add-at-drain
  protocol, and the file's complementary relation to the orchestrate daemon's
  live LanesObserved active-lane registry.
---

# 6 — retired-lanes thin registry

## What landed

Created `protocols/retired-lanes.md`. The file has a purpose header, an
add-at-drain protocol, a statement of its relation to the live active-lane
registry, and an EMPTY registry table under those sections. No git ranges
were fabricated — no lane has drained under this model yet, so the table
ships empty and grows one row per real retirement.

## The decision it manifests

The frame's open fork (report 0) was: when a session lane drains, delete
everything (Option A) or keep an in-tree archive (Option B). The psyche
confirmed (2026-06-24) the thin middle path: DELETE the lane's report
directory — git history and the transcript are the archive — and record
the retirement in this single append-only registry. This file is that
registry. It deliberately holds no reports, only pointers, so the working
report tree stays small while drained sessions remain discoverable for
regression / flow / model-behavior forensics.

## Entry format

A markdown table, one row per retired lane, columns:
`Lane | Discipline | Git revision range | Transcript pointer | Drain date | Decided`.
The git revision range is the history holding that lane's now-deleted
reports; "Decided" is a one-line statement of what the lane concluded.

## Protocol the file states

The retiring agent appends one row at session close, in the SAME commit
that deletes `reports/<lane>/`. So the deletion and its index entry are
atomic — a drained lane is never both gone-from-tree and absent-from-index.

## Relation to the daemon registry

The file documents the split: the orchestrate daemon's `Observe` ->
`LanesObserved` indexes ACTIVE lanes (live, in-flight); this file indexes
RETIRED lanes (durable, drained). A lane is in exactly one at a time. The
two are complementary halves of one lane lifecycle.

## Notes for downstream slices

- A drain-and-retire walkthrough belongs in the context-maintenance /
  reporting skill slice; this file is the destination that protocol writes
  to. The skill slice should reference appending here as the final step of
  draining a lane (same commit as the report-dir deletion).
- The table is intentionally empty; the first real row appears when the
  first lane actually drains under the new model.
