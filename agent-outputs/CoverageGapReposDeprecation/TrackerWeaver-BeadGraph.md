# Tracker Weaver — full-pipeline bead-graph reconciliation

## Task and scope

Advance the durable tracker graph under epic `primary-6obv` to match the approved
full-pipeline effort (Phase 0 discovery -> review gate -> Phase 1 coverage folding
-> Phase 2 repos/ deprecation + manifest -> Phase 3 t5vj integration). Tracker/bead
state only; no repo/doctrine work, no repo-file edits.

## Evidence consulted

- `reports/legacy-disposition/HANDOVER-2026-06-30-coverage-gap-and-repos-deprecation.md`
  (the named pipeline evidence: 43 missed repos with INTENT.md, CriomOS-test-cluster
  + signal-standard no-fold-target, repos/ deprecation intent, 31 t5vj records mapping
  to live homes with OS vs cloud/goldragon/lojix split, secrets boundary).
- `bd show primary-6obv`, `bd show primary-t5vj`, `bd show primary-ay9d` (existing state
  + sub-bead convention).
- `orchestrate "(Observe Roles)"` confirmed two active workers: system-designer on
  CriomOS/CriomOS-home (t5vj OS integration) and cloud-maintainer/cloud-operator on
  cloud/CriomOS-test-cluster.

## Commands run (mutations)

- `bd create` x9 (7 new epic children 6obv.1-.7; 2 t5vj sub-beads t5vj.1/.2).
- `bd dep --blocks` x8 (pipeline dependency edges).
- `bd update --status` for statuses (in_progress: 6obv.1, t5vj, t5vj.1, t5vj.2;
  blocked: 6obv.3-.7).
- `bd update --title` / `-d` on t5vj (reactivation reframe).
- `bd note` on t5vj and 6obv (reconciliation record).

## Resulting bead states

Newly created:
- `primary-6obv.1` Phase 0 discovery — in_progress
- `primary-6obv.2` REVIEW GATE decision — open (blocked-by 6obv.1)
- `primary-6obv.3` Phase 1 coverage folding remainder (~43-45 repos) — blocked
- `primary-6obv.4` Phase 1 author ARCHITECTURE.md CriomOS-test-cluster — blocked
- `primary-6obv.5` Phase 1 author ARCHITECTURE.md signal-standard — blocked
- `primary-6obv.6` Phase 2 repos MANIFEST rework stand-up — blocked
- `primary-6obv.7` Phase 2 repos/ deprecation execution — blocked
- `primary-t5vj.1` t5vj OS sub-effort (CriomOS/CriomOS-home) — in_progress
- `primary-t5vj.2` t5vj cloud sub-effort (cloud/goldragon/lojix) — in_progress

Reactivated:
- `primary-t5vj` — DEFERRED -> in_progress (parent of .1/.2)

Left as-is (untouched original tracks, not part of this pipeline):
- `primary-smwa` T1 (open), `primary-bvsd` T2 (open), `primary-e191` T8 (open),
  `primary-7wld` T5 (open), `primary-g28b` T6 (open), `primary-zpgw` T7 (open).

## Dependency edges

- 6obv.1 -> 6obv.2 (discovery blocks gate)
- 6obv.2 -> 6obv.3 / .4 / .5 / .6 / .7 (gate blocks all Phase 1/2)
- 6obv.1 -> 6obv.6 (discovery shape feeds manifest)
- 6obv.6 -> 6obv.7 (manifest precedes deprecation execution)
- t5vj -> t5vj.1, t5vj.2 (parent-child)

## Gated on the review checkpoint (6obv.2)

`primary-6obv.3`, `primary-6obv.4`, `primary-6obv.5`, `primary-6obv.6`,
`primary-6obv.7`. The gate itself (6obv.2) is blocked-by Phase 0 discovery (6obv.1).

## Verification

`bd show primary-6obv` (26 children, 12/26 done), `bd children primary-t5vj`
(3 issues, 3 in_progress), `bd dep list` on gate + downstream confirmed edges resolved.

## Blockers / follow-up

- None for tracker state; all mutations succeeded and read back clean.
- The review-gate decision (6obv.2) is a psyche checkpoint; Phase 1/2 beads stay
  blocked until it records per-repo disposition + manifest-shape approval.
- Coordination note carried in beads: 6obv.4 (CriomOS-test-cluster) overlaps the
  active cloud-operator lane; t5vj.1 overlaps the active system-designer lane.
