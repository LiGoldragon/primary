# Lojix realization migration

Legacy realization state, owned psyche rulings, deployment witnesses, and
completion report are represented in this flow. The legacy session and
duplicate global psyche entries are retired.

2026-08-22 — Reconstructed from the legacy realization record, targeted
transcript events, direct Lojix/profile probes, and the prior flows named
below. Parent-flow migration landed on main and was pushed; primary-d7s
remains for master review.

Remembered: 01a01a93 — depth 1
Remembered: e06e4c07 — depth 1
Remembered: 7c3f0c1d — depth 1

Final handoff: flow protocol migration is complete, committed, and pushed.
The current `ByDeployment` client failure has an unknown cause; no deployment
or runtime mutation was made during migration.

Historical child-lane consolidation: corrected parent annotations, the
deployment-27 witness, and report provenance belong with this root lane.
`primary-d7s` remains for master review; the `ByDeployment` failure cause is
still unknown.
