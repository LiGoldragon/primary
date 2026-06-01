# 461.1 — Engine trait architecture (Signal/Nexus/SEMA)

*Kind: Review · Topics: engine-trait-pattern, signal-nexus-sema, b53f4fc2, audit-cluster · 2026-06-01*

## Topic arc

Spirit 1326 (Constraint High, operator-addressed) named the
constraint: the spirit engine defines + uses Signal/Nexus/SEMA
interfaces in schema and conducts core logic through traits
taking + returning root types. Spirit 1327 (Principle Maximum,
designer-captured per the psyche's "adapt to the broad triad
architecture" directive) lifted that to a workspace-wide pattern.
Spirit 1330-1336 (six Decision Maximum records) refined the
per-engine role and the pipeline shape: Signal = triage only;
Nexus = heavy logic + bidirectional translator; SEMA = single-writer
durable with parallel reads via apply/observe split; full pipeline
Signal triage → Nexus execute → SEMA → Nexus → Signal reply with
origin identifiers threading through.

The session's report production around this topic spanned
**operator's b53f4fc2 implementation commit** + **designer 453 + 454
+ 455 + 459** (the latter builds on the pattern by adding the
proof-of-usage layer) + **operator 273** (parallel operator audit) +
**operator 457** (continuation in-flight as `retire-design-remnants`
branch integration with SemaEngine apply/observe split).

The substance has fully matured: it lives in `spirit-next/ARCHITECTURE.md`
+ `INTENT.md` (operator's b53f4fc2 commit), in the schema-rust-next
emitter (a588ec6), and via this sweep's migration into
`skills/component-triad.md` §"Runtime triad engine traits".

## Current canonical surface

| Surface | What it carries |
|---|---|
| `skills/component-triad.md` §"Runtime triad engine traits — Signal triage / Nexus computation / SEMA durable" | Workspace-level pattern; the three trait shapes; pipeline; origin protocol. NEWLY-LANDED in this sweep. |
| `/git/github.com/LiGoldragon/spirit-next/ARCHITECTURE.md` §"Runtime triad" | Spirit-specific implementation: pipeline shape, per-engine borrow rules, the SemaEngine apply/observe split. LANDED by operator's b53f4fc2. |
| `/git/github.com/LiGoldragon/spirit-next/INTENT.md` | Maps the engine traits to the production runtime path. LANDED by operator's b53f4fc2. |
| Spirit records 1326, 1327, 1330-1337 | Primordial intent surface; the records are the source of truth. |

The skill landing is the workspace-level distillation; the per-component
landing is in each component's ARCHITECTURE.md (today only spirit-next
carries it; other components migrate during porting waves per designer
446).

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 453 — Engine trait broad triad adaptation | DROP-CANDIDATE | Substance migrated to `skills/component-triad.md` §"Runtime triad engine traits". Spirit 1326/1327 captured. Workspace-level adaptation is now permanent. |
| 454 — Engine role pipeline refinement | DROP-CANDIDATE | Substance migrated to the same skill section (per-engine roles, pipeline shape, origin protocol). Spirit 1330-1336 captured. The apply/observe split is documented. |
| 455 — b53f4fc2 design-implementation fidelity audit | KEEP-AS-WORKING | Audit landed on `audit-b53f4fc2-design-fidelity` branch with 18 falsifiable witnesses. The witnesses ARE the substance. Retires when the audit branch integrates and the gap-witnesses turn from documented to fixed (operator 457 names this as in-flight). |
| 459 — Proof-of-usage witness research | DROP-CANDIDATE | Substance migrated to `skills/architectural-truth-tests.md` §"Proof-of-usage ladder" in this sweep. The three-layer model + worked examples are now permanent. Tool-upgrade proposals (architectural-witness cargo subcommand + assert_trait_method_called macro) can re-emerge as future operator beads. |

The DROP-CANDIDATE marking for 453 and 454 reflects the designer-lane
ownership: this dispatcher applies the drops. The migrations land in
this sweep; the drops are executed in the same commit window.

### Operator lane

| Report | Action | Reason |
|---|---|---|
| 273 — spirit-next b53f4fc2 triad runtime audit | KEEP for now; HANDOFF | Substance is live audit of operator's own commit; the recommendations feed `retire-design-remnants` branch integration (operator 457 in-flight). Retires when integration lands. Operator-owned drop. |

## Landing evidence

For each DROP-CANDIDATE:

- **453 substance** lives in `skills/component-triad.md` §"Runtime
  triad engine traits — Signal triage / Nexus computation / SEMA
  durable" — the table of three traits with roles + schema-emitted
  shapes + interface direction + pipeline + origin protocol +
  "what this pattern is and is not". Spirit 1326/1327 cited.
- **454 substance** lives in the same skill section: the per-engine
  role columns (triage only / heavy logic / durable single-writer),
  the pipeline mermaid (5 nodes, Signal→Nexus→SEMA→Nexus→Signal),
  the apply/observe split column, origin identifier protocol
  paragraph. Spirit 1330-1336 cited.
- **459 substance** lives in `skills/architectural-truth-tests.md`
  §"Proof-of-usage ladder — choose cheapest sufficient" — the
  three-layer model (STATIC / RUNTIME / BEHAVIORAL), per-layer
  witness catalogue with cost columns, the choose-cheapest-sufficient
  discipline, and three worked examples (Layer 1 emission witness,
  Layer 2 recorder, Layer 2 process boundary).

## Drop ownership / handoff

**Designer lane** (this sweep): drops 453, 454, 459 in the commit
that lands the migrations. The drops are safe because the substance
has migrated AND because spirit-next's ARCHITECTURE.md carries the
component-specific landing.

**Operator lane**: when next doing maintenance, the relevant action
is — after `retire-design-remnants` integration lands on
`spirit-next/main` and the SemaEngine apply/observe split is live in
spirit-next, operator 273 retires (its audit substance is fully
absorbed by the integrated commit). The recommendation lives in the
overview's per-lane handoff section.

## Notes on the convergence

This topic carried a strong **multi-lane convergence pattern**:
designer 455 (audit), designer 453+454 (workspace adaptation), and
operator 273 (parallel operator audit) independently produced
substantially aligned findings about the b53f4fc2 commit. The
convergence is captured as a discipline note in
`skills/designer.md` §"Three-way convergence as correctness signal"
(newly-landed in this sweep). The note generalizes the pattern from
this specific topic into a workspace-wide discipline.

## Cross-references (for verification, not for navigation)

- `spirit-next/ARCHITECTURE.md` lines ~80-160 — the per-engine borrow
  rules and pipeline.
- `spirit-next/src/engine.rs` — production composition point.
- Spirit records 1326, 1327, 1330-1336 — primordial intent.
- `skills/component-triad.md` §"Runtime triad engine traits" — the
  permanent landing this sweep added.
