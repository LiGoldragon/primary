# 461.5 — Operator 271 verification cluster

*Kind: Review · Topics: operator-271-verification, falsifiable-specs, branch-as-artifact, audit-cluster · 2026-06-01*

## Topic arc

Operator 271 (context maintenance — current state) named two halves
of the schema-stack working surface:

1. **"Closed Since The Earlier Gap Reports"** — five claims of closure
   that designer 450 verified by writing a positive witness per gap on
   the `verify-271-closed-claims` branch in each affected repo.
   Verdict: all five VERIFIED with live constraint tests; one
   unexpected stale flake check surfaced in schema-next and got fixed
   in passing.
2. **"Still Unaddressed"** — eight open claims that designer 451
   addressed by writing one RED-now/GREEN-when-implemented witness
   per claim on `falsifiable-specs-271-open-claims` branches across
   `nota-next`, `schema-next`, `schema-rust-next`, and `spirit-next`.
   Three claims are precise (named call sites; small single-PR
   cleanups: parser discipline pair, CLI source helper, SchemaError
   Display); five are scaffold-shaped (compile-fail against types
   that don't exist yet, marking destination shape) — those queue
   behind the architectural horizon work in designer 444 §5 +
   designer 446 + designer 447.

The branches make the operator's backlog **mechanically falsifiable**:
green means the gap is closed; red means there's still work to do.

## Current canonical surface

| Surface | What it carries |
|---|---|
| `verify-271-closed-claims` branches (nota-next + schema-next + spirit-next) | Five positive witnesses + one repaired stale flake check. Operator-pickup-ready. |
| `falsifiable-specs-271-open-claims` branches (nota-next + schema-next + schema-rust-next + spirit-next) | Eight RED witnesses; three precise, five scaffold. Operator-pickup-ready. |
| `skills/designer.md` §"Designer sub-agents land code witnesses" §"Worked instances" (newly landed) | The closed-claim verification + falsifiable-specs patterns documented as canonical sub-agent dispatch shapes. |

The branches ARE the durable substance. Per `skills/designer.md`,
"the branch IS the artifact" — once the branches integrate, the
reports retire.

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 450 — Operator 271 closed-claims verification | KEEP for now | The verify branches are pushed but not yet operator-integrated. Retires when the branches integrate onto main (witnesses become part of the standard test suite) AND the closed-claim status carries forward through operator's working surface. The repaired-stale-flake-check finding (schema-next `declarative-schema-macros` check) is independent substance — already on the branch as a fix; will absorb when the branch integrates. |
| 451 — Operator 271 falsifiable specs for open claims | KEEP for now | The eight RED witnesses are operator's mechanical falsifiability surface for the unaddressed backlog. Retires when (a) precise witnesses turn green via operator's small-PR cleanups, AND (b) scaffold witnesses absorb into the relevant horizon work (schema-core extraction, upgrade-as-SEMA, spirit fold). The 8-claim structure means partial retirement: claim-by-claim as each turns green. |

### Operator lane

| Report | Action | Reason |
|---|---|---|
| 271 — Context maintenance current state | KEEP | Active operator working surface. Listed at 461.2's spirit-fold-and-porting (operator-lane) for the broader retirement gate. The closed-claims and open-claims tracking is partially superseded by the verify/falsifiable-specs branches; the operator-side summary surface remains useful. |

## Landing evidence

The closed-claim verification + falsifiable-specs methodology IS
documented this sweep via:

- `skills/designer.md` §"Designer sub-agents land code witnesses"
  §"Worked instances" — explicit worked-instance description of:
  closed-claim verification (positive witness per gap); falsifiable
  specs for open claims (RED-now/GREEN-when-implemented per claim);
  design-fidelity audit against a commit; remnant retirement
  refactor.

This is the designer-side discipline. The operator-side
implementation pickup is by branch integration; no operator-skill
needs updating.

## Drop ownership / handoff

**Designer lane**: no drops in this topic this sweep. Partial-retirement
trajectory:

- When the verify branches integrate, 450 retires (the closed claims
  are confirmed in code; the report's job is done).
- When all 8 falsifiable specs turn green or absorb into horizon
  reports, 451 retires (claim-by-claim partial retirement preceded
  by the integration of each branch).

**Operator lane**: integration ownership. Operator picks up the
verify branches as the standard test-suite extension; the
falsifiable-spec branches as the gap-implementation guide. No
operator-side report retirement triggered by this topic; 271's
retirement is gated at the 461.2 spirit-fold-and-porting topic.

## Pattern observation

The 450 + 451 pair demonstrates a **two-sided audit pattern**:

- For an operator report naming N closed gaps, a verify dispatch
  writes positive witnesses confirming the gaps are closed.
- For the same report's M open gaps, a falsifiable-specs dispatch
  writes RED witnesses naming the destination shape.

Both branches are pushed in parallel; the operator's backlog is now
mechanically tracked (green = done, red = pending). This complements
the design-fidelity-audit pattern (which audits an operator commit
against the design's spec) and the remnant-retirement pattern (which
removes stale design surfaces from operator's code).

The four patterns together — verify-closed-claims, falsifiable-specs,
design-fidelity-audit, remnant-retirement — are the worked instances
of the sub-agent code-witness dispatch documented in
`skills/designer.md` (this sweep's addition).

## Cross-references

- `reports/designer/450-operator-271-closed-claims-verification-2026-06-01.md` §"Method" — the verification methodology.
- `reports/designer/451-operator-271-falsifiable-specs-2026-06-01.md` §"Test classification" — the three shapes (AST-static, compile-time, runtime).
- `reports/operator/271-context-maintenance-current-state-2026-06-01.md` §"Still Unaddressed" — the 8-claim backlog.
- `skills/designer.md` §"Designer sub-agents land code witnesses" §"Worked instances" — the patterns.
