---
title: 498 - Persona engine state - overview
role: designer
variant: Synthesis
date: 2026-06-04
topics: [persona-engine, abandoned-work, bugs, context-maintenance, vision, beads]
description: |
  Synthesis of the five-agent persona-engine assessment and the actions
  taken. The psyche-facing vision and corrections live in report 499; this
  is the internal ledger: what each slice found, what was cleaned up this
  turn, and the operator beads filed.
---

# 498 - Persona engine state - overview

## What each slice found

- **1 — abandoned work.** Almost none hidden. Exactly two branches carry
  real unlanded work (both known, both queued): triad-runtime
  `designer-strings-at-edges-2026-06-04` and persona-spirit
  `spirit-repetition-cleanups` (integrate all 3 commits — the pushed tip
  lags the local stack by 2). Everything else is clutter: ~54 superseded
  late-May concept branches and all 63 primary push-bookmarks. Nothing
  stranded in a worktree.
- **2 — bugs and bad designs.** One correctness bug across the engine: the
  schema-next dual lowering engine (registry path drops bare-header payloads
  to None). Everything else is structural debt, none on main; the two
  keystones (RustItem token model, triad runner) are ratified-but-unbuilt.
- **3 — context maintenance.** Stale report blocks have named superseders
  and can retire per the topic-recency ledger; three live doc-drifts
  (spirit/INTENT.md:206 parity overstatement, the half-done rename,
  persona-spirit/INTENT.md missing the Medium-default heuristic); 1590 (dup
  of 1583) and 1456 (mooted) needed certainty fixes.
- **4 — vision and architecture.** The backbone (this directory's entry 4):
  persona as meta-AI, the Signal/Nexus/SEMA triad with the asymmetric
  NexusWork/NexusAction pair and Continue, the component built/partial/missing
  map, the schema-stack pipeline, and the three-stage cutover.
- **5 — misunderstandings.** Five corrections, headlined by: the rename
  doesn't make the pilot production (and it's half-done); ratified ≠ built;
  the SymbolPath structured/flat question is NOT settled (1586 was the later
  capture); the cutover mechanism is undesigned; schema-as-codec is a
  destination with a one-way implementation today.

## Actions taken this turn

- **Pruned all 63 stale push-bookmarks** (local + remote). The auto-named
  `push-<changeid>` ones confirm `jj git push -c @` misuse.
- **Filed 10 operator beads** (`primary-vllc`, `-60xf`, `-u4tl`, `-l89s`,
  `-myku`, `-f8gf`, `-ohpk`, `-kwm2`, `-oq0n`, `-tcg0`): the P1 dual-engine
  fix, the two concept-branch integrations, the runner, the token model, the
  crate rename, the production marker, thiserror, the concept-branch prune,
  and the spirit doc/discipline fixes.
- **Certainty fixes:** Zeroed 1590 (dup of 1583, missed by the 497 sweep);
  dropped 1456 to Low (over-rated four-tier privacy enum, mooted by
  1463/1571 — flagged for psyche confirmation).
- Reinforced the no-stray-push-bookmark rule in `skills/jj.md` (record 2543).

## Where the substance lives

The psyche report `reports/designer/499-Psyche-persona-engine-state-and-vision-2026-06-04.md`
carries the vision, the cutover, the missing-list, and the corrections and
decisions the psyche owes. The do-it-now work is in the ten beads above.
