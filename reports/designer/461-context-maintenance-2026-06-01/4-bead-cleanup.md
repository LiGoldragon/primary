# 461.4 — Bead cleanup cluster

*Kind: Review · Topics: bead-staleness, bead-sweep, persona-stack-retirement · 2026-06-01*

## Topic arc

The persona-stack pivot to the schema-derived next-stack (Spirit
1280-1319, designer 444-446) left the workspace's bead store carrying
substantial stale work. Designer 449 audited the 269 open beads
against the current intent corpus; verdict: ~110-130 of the 162 P2
beads + 35-40 of the 48 P3 + 49 of the 68 P0/P1 are wholly stale due
to supersession by the schema-emission pivot + the upgrade-as-SEMA
direction. The audit recommended bulk close-as-superseded for five
large stale arcs (persona-* migrations, `signal_channel!` macro
consolidation, persona-spirit cutover, persona-agent triad,
persona-prefix rename remnants) plus the contract-repo.md skill-update
queue.

Operator 272 (meta-report) verified designer 449 independently,
decided to implement, and ran the close-sweep: 60 stale beads closed
across the targeted clusters; open-bead queue moved from 269 to 209.
The close-sweep used family-note style — each closing note named
the current design surface where the concern should re-emerge if
still needed.

Designer 457 (operator day audit) continued the bead sweep: 72 more
P2/P3 stale beads closed across 11 family clusters; open queue moved
from 209 to 77.

## Current canonical surface

| Surface | What it carries |
|---|---|
| Beads store (`.beads/`) at 77 open beads | The live work queue. The headline P0/P1 stale arcs are closed. Remaining P2/P3 stale leftovers concentrated in signal-channel + contract-repo.md skill-update + version-handover families. |
| `skills/beads.md` | The discipline for bead authoring + periodic audit + anti-patterns. Already carries the relevant rules (anti-pattern B: design-questions-as-beads; close-with-breadcrumb; periodic-audit cadence). |

The bead audit's substantive output is in BEADS itself — the closed
beads with their closing notes, the open queue's smaller surface.
The reports are the working artifact that produced the substance.

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 449 — Bead staleness audit | KEEP for now; HANDOFF | The audit's recommendation is partially executed (operator 272 + designer 457 closed ~132 of the audit-identified stale beads). The substance is the audit-as-falsifiable-recommendation; retires when the open queue stabilises in healthy state (per `skills/beads.md` §"Periodic audit" — ~30-40 is the target). Today the queue is at 77, in-progress. |
| 457 — Operator day audit + bead sweep continuation | KEEP for now | Tracks the continued bead-sweep landings + flags 3 deferred items (`primary-9hx0`, `primary-lrf8`, `primary-54ti`). Retires when the deferred items resolve AND the next operator audit absorbs the day-audit's tracking surface. |

### Operator lane

| Report | Action | Reason |
|---|---|---|
| 272 — Bead staleness audit implementation (meta) | KEEP for now; HANDOFF | Meta-report covering the implementation + a postmortem flagging remaining open items. Retires when the deferred items resolve and the next bead-sweep meta-report supersedes. Operator-owned. |

## Landing evidence

No permanent-doc migrations from this topic this sweep. The bead
discipline is already documented in `skills/beads.md`; the audit
methodology (operator-designer convergence on bead staleness; bulk
close with family notes; recommend-don't-execute-in-one-pass) is
documented in:

- `skills/beads.md` — bead discipline + periodic-audit cadence.
- `skills/context-maintenance.md` §"Retiring a lane" mentions bead
  triage as part of lane retirement (parallel discipline).
- `skills/designer.md` §"Three-way convergence" (newly landed this
  sweep) — names this kind of convergence as correctness signal.

No new permanent surface needed; the work landed where it should
(in BEADS itself).

## Drop ownership / handoff

**Designer lane**: no drops in this topic this sweep. Future
maintenance: when the bead queue stabilises (P0 stays empty, P1
healthy, P2/P3 lean), 449 + 457 retire together as one cluster (their
substance is fully absorbed into BEADS).

**Operator lane**: when next doing maintenance, operator 272 retires
once the 3 deferred items (`primary-9hx0`, `primary-lrf8`,
`primary-54ti`) are resolved (designer rewrites `primary-9hx0` as a
designer report; source-level verification confirms `primary-lrf8`;
cluster/system-operator context re-anchors `primary-54ti`).

## Three deferred items — handoff specifics

Surfaced for the chat reply per the user-attention discipline:

- **`primary-9hx0`** — "Split lib.schema into three schema-type files
  per record 964". Anti-pattern B: design-question-in-task-form.
  Designer-lane action: convert to a designer report exploring the
  split (or close with a closing note that the question is folded
  into designer 446 + the spirit fold direction).
- **`primary-lrf8`** — close-as-shipped requires source-level
  verification of explicit queue, worker drain, multi-observer
  fanout, concurrent processing. Operator-lane action.
- **`primary-54ti`** — horizon-rs deploy-stack work; needs cluster/
  system-operator context. Operator-lane action: re-anchor or
  re-file in cluster-operator/system-operator scope.

## Cross-references

- `reports/designer/449-bead-staleness-audit-2026-06-01.md` §"Stale-bead table" — the 41-row detail.
- `reports/operator/272-bead-staleness-audit-implementation-2026-06-01/4-postmortem.md` — the execution + final state.
- `reports/designer/457-operator-day-audit-and-bead-sweep-continuation-2026-06-01.md` §"Bead sweep continuation" — the 72-bead second pass.
- `skills/beads.md` — the bead discipline.
