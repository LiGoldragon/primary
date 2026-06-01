# 461.2 — Spirit fold and porting sequencing

*Kind: Review · Topics: spirit-fold, porting-waves, naming-gate, schema-core-extraction · 2026-06-01*

## Topic arc

The next-stack pivot (Spirit 1287/1290/1294 + designer 444's stack
vision) created a substrate-ready `spirit-next` pilot. The remaining
question — how to port the rest of the workspace's component fleet
onto the substrate — produced designer 446 as a three-sub-agent
meta-report converging on `spirit` fold as Phase 0 (validate the
recipe by folding the pilot back into the real repo), `cloud + upgrade
+ repository-ledger` parallel as Phase 1a, schema-core extraction
gate at Phase 1b/c, then stateful runtimes (mind/router/terminal/
orchestrate) in Phase 2.

The fold gating question — what to name the policy contract repo
when `core-signal-spirit` retires — produced designer 458 as the
explicit decision report. The recommendation: Option A
(`owner-signal-spirit`, current workspace convention) over Option B
(`meta-signal-spirit`, proposed per Spirit 290+299 but explicitly
marked tentative). The decision unblocks Phase 0.

## Current canonical surface

| Surface | What it carries |
|---|---|
| `reports/designer/446-next-stack-porting-research-2026-06-01/4-overview.md` | The convergent recommendation: spirit-fold first, wave-1 trio parallel, schema-core extraction at the gate to wave-2. Phase 0-2 sequencing. Operator-bead-shaped first action. |
| `reports/designer/458-spirit-triad-naming-gate-decision-2026-06-01.md` | The naming decision: recommend Option A `owner-signal-spirit`. Awaiting psyche ratification. |
| `reports/designer/444-stack-vision-2026-05-31/` (meta) | Foundational vision; the §5 horizon ledger names schema-core, generic SemaStore/SerializableArtifact, schema-emitted projections, CLI source helper. |
| Spirit records 1287, 1290, 1294, 1300-1314, 1326-1336, plus 290, 293, 299 (rename direction) | Primordial intent surface. |
| `skills/component-triad.md` §"Runtime triad engine traits" (newly landed) | The engine-trait pattern every port targets. |

The substance carried by 446 is sequencing intelligence and
operator-pickup specs; it's not primordially a permanent-doc
candidate — the work is in flight and the sequencing depends on
psyche decisions. The naming gate (458) is a decision request awaiting
psyche action.

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 446 — Next-stack porting research (meta) | KEEP | The substance is live sequencing for ongoing porting work. Phase 0 is gated on 458's decision; Phase 1a candidates are queued. The overview names operator-bead-shaped actions that haven't been picked up yet. Retires when Phase 0 lands AND wave-1 trio sequencing absorbs into operator's working surface. |
| 458 — Spirit triad naming gate decision | KEEP (escalate) | Decision report awaiting psyche ratification (single yes/no). Pending psyche-review items stay Keep per `skills/context-maintenance.md` §"Per item, decide" — "Pending psyche-review flags are not stale merely because they are old." Surface in the chat with the recommendation restated. |
| 447 — Upgrade-as-SEMA design | KEEP | Sole design for the upgrade mechanism (Spirit 1305-1314). Implementation has not started. Retires when an operator-implementation pickup lands the substrate AND the substance migrates into the schema-daemon's ARCHITECTURE.md when that repo is created. |

### Operator lane

| Report | Action | Reason |
|---|---|---|
| 271 — Context maintenance current state | KEEP | The "Still Unaddressed" backlog is partly addressed by designer 451's falsifiable specs (some claims have been carried into spirit-next's working-tree per operator 457). Active operator working surface; retires when the next operator context-maintenance pass supersedes. Operator-owned. |

## Landing evidence

No permanent-doc migrations from this topic this sweep. The substance
is live work-in-flight that doesn't yet fit a permanent doc:

- The porting playbook (designer 446's sub-agent 2) IS a candidate
  for a future `skills/porting-playbook.md` once the playbook has
  proven itself across two or three ports. Per
  `skills/context-maintenance.md` §"Treating reports as different
  disciplines" and the pilot principle (validate then extract), the
  playbook stays a report until enough ports prove the recipe. NOT
  migrating now.
- The naming gate (458) is a pending decision; permanent landing
  goes in `skills/component-triad.md` §"Proposed rename:
  owner-signal → meta-signal" once the psyche ratifies one option.
  Until then, the uncertainty stays carried per the
  `skills/architecture-editor.md` carry-uncertainty discipline.
- The schema-core extraction (designer 444 §5 horizon 1) is gated
  by the wave-1 evidence; no migration possible until at least two
  observed consumers exist.

## Drop ownership / handoff

**Designer lane**: no drops in this topic this sweep. Future
maintenance: when Phase 0 fold lands and the wave-1 trio starts,
designer 446 retires (the porting work absorbs the sequencing
substance; the operator-bead-shaped actions are now beads). Designer
458 retires when the psyche ratifies one option AND the chosen name
lands in `skills/component-triad.md` §"Proposed rename".

**Operator lane**: when next doing maintenance, operator 271 retires
once the falsifiable-spec branches from designer 451 land on main
and the backlog moves to bead form.

## Open psyche-review items surfaced

Per `skills/context-maintenance.md` §"Per item, decide", pending
psyche-review items stay surfaced. The chat reply should restate:

- **458's decision request**: "Ratify Option A — `owner-signal-spirit`
  for Phase 0 fold; defer fleet-wide meta-signal rename to a separate
  ratified workspace-wide pass?" Single yes/no closes the gate.
  Option A is the recommendation. Option B requires Maximum-magnitude
  psyche ratification + a dedicated multi-week rename slice.

## Cross-references

- `reports/designer/446-next-stack-porting-research-2026-06-01/4-overview.md` §"The recommended first slice" — the Phase 0-2 mermaid.
- `reports/designer/458-spirit-triad-naming-gate-decision-2026-06-01.md` §"Decision ask" — the single yes/no.
- Spirit records 290, 293, 299 — the rename direction's tentativeness.
- `skills/component-triad.md` §"Proposed rename: owner-signal → meta-signal" — the carry-uncertainty surface.
