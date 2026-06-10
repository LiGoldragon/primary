# Spirit intent redesign — implementation guidance for operator (frame)

A light exploration, not an implementation. Purpose: hand operator grounded,
insight-dense guidance for building the redesign — based on the **actual intent
corpus** and the **current source**, not just the design in the abstract.

## Where things stand

- The design is settled in `reports/designer/578-intent-redesign-synthesis.md`,
  with operator's three review passes folded in
  (`reports/operator/352-spirit-intent-redesign-current-source-feedback.md`).
- The breaking schema pass has **already landed** in the spirit repo:
  `magnitude` renamed to `certainty`, and an `importance` axis added (the psyche
  chose to keep Importance — so all three axes exist: certainty, weight (TBC),
  importance). System-operator is deploying it now.
- Empirical baseline: `577` (deployed v0.4.0 state) and `579` (first
  agglomeration pass — 21 canonicals, 43 removal-candidates, 3 topics done, 1312
  left).

## Method

Three read-only explorations, each landing as a numbered report here, then a
synthesis (highest-numbered file) with the implementation guidance:

1. `1-corpus-patterns.md` — mine the real ~1400-record corpus for
   implementation-guiding patterns: real duplicate-cluster shapes (→ duplicate
   detection + weight-bump), real discussion-contamination in
   Corrections/Clarifications (→ kind migration + clarify trample/loses checks),
   real supersede-vs-clarify-vs-trample pairs, the natural broad-category
   clustering (→ category catalog bootstrap).
2. `2-source-vs-design.md` — current spirit source vs the `578` design and
   `352` build order: actual `Entry` fields and selection/op/schema types now,
   what substrate already exists (snapshots, weight, category, journals, lease),
   the concrete smallest-next-steps and any source↔design divergences.
3. `3-migration-and-tests.md` — migration realities grounded in real data
   (topic→category, Correction/Clarification kind migration, finishing the
   agglomeration) and a concrete fixture/test plan per `352` §7.

Synthesis: `4-synthesis.md`.

## Guardrails for the explorations

- **Read-only.** The store is mid-deploy — never mutate it (no `Remove`,
  `ChangeCertainty`, `ChangeRecord`, `CollectRemovalCandidates`), never run
  `jj`/`git` commits. Tolerate the daemon being mid-restart; fall back to
  `577`/`579` for already-gathered stats.
- Never touch `private-repos/` or private records; ordinary `spirit.sock` only.
- Guidance and insight, not code. The deliverable helps operator implement; it
  does not implement.
