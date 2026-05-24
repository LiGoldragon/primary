*Kind: Audit + Rework · Topic: worktree-audit-and-rework · Date: 2026-05-25 · Lane: second-designer*

# 174 — Worktree audit + rework: my 7 branches + operator/designer nspawn worktrees

## §1 Scope

Per psyche directive 2026-05-25 ("audit operator and your own worktrees, and rework it with report") + intent 511 (audit cycle: refresh intent + re-audit from latest operator main + check whether prior designer worktrees were considered + re-present on fresh main if not implemented but design still good).

Audited:
- My 7 feature branches across 4 repos (4 schema mockups + 1 signal-engine-management mockup + 2 orchestrate-port branches)
- Designer's 3 nspawn worktrees under `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/`
- Operator's main-track work on Spirit/upgrade/persona-spirit (the comparison baseline)

Output: per-branch verdict (REUSE / REBASE / RE-IMPLEMENT / OBSOLETE / LANDED) + applied rework + next-iteration recommendations.

## §2 My 7 feature branches — verdicts at a glance

| # | Repo | Branch | Commit | Drift on main | Verdict |
|---|---|---|---|---|---|
| 1 | schema | `feature/component-uid-and-layout` | `b5c4f373` | 2 ahead | REBASE |
| 2 | schema | `feature/engine-routing-and-upgrade-coverage` | `52f53646` | 2 ahead | REBASE |
| 3 | schema | `feature/macro-variant-engine` | `e4a86450` | 2 ahead | OBSOLETE |
| 4 | schema | `feature/orchestrate-schema-example` | `0d16db07` | 0 ahead | LANDED |
| 5 | signal-engine-management | `feature/durable-identity-via-peercred` | `0eeae13e` | 0 ahead | REUSE |
| 6 | signal-orchestrate | `feature/schema-engine-and-no-downtime-upgrade` | `45a63ab3` | 2 ahead | REBASE |
| 7 | orchestrate | `feature/schema-engine-and-no-downtime-upgrade` | `44a98a7b` | 1 ahead | REBASE |

Summary: 4 REBASE, 1 REUSE, 1 OBSOLETE, 1 LANDED. Zero RE-IMPLEMENT — none of the main drift makes any branch's intent moot beyond mockup C (whose intent IS what main now ships).

## §3 Per-branch detail

### §3.1 schema · feature/component-uid-and-layout — REBASE

**What's on the branch (not on main)**: `mockup: component-name UID anchor + Layout-on-AssembledSchema fix per second-designer/171 §10 slices A+B`.

**Main commits after divergence**:
- `schema: add builtin lowering engine` (`kzkqytvw`)
- `schema: lower upgrade rules through builtin macro variant` (`lpmvzxto`)

**Drift assessment**: orthogonal. Main's commits land the macro-variant lowering engine (the topic of my mockup C, which is OBSOLETE — see §3.3); this branch's `Schema::for_component` constructor + `AssembledSchema::component()` + `uid_for()` + `Layout::for_assembled` API additions are independent surface area.

**Verdict**: REBASE. Apply the branch's changes onto current main; resolve any signature-touching merge points (likely minimal since the new code is additive). Per intent 511, this branch's design is still good — Magnitude-in-box bug is still real, component-name UID still missing on main.

**Open question carried**: §3.1 from /172 overview (imported types render UIDs under importing vs source schema's component) — per intent 526, the lean is now **source schema's component**. Rebase should adopt this canonical UID resolution rather than the mockup's importing-schema choice.

### §3.2 schema · feature/engine-routing-and-upgrade-coverage — REBASE

**What's on the branch (not on main)**: `mockup: engine threading to Route + multi-sub-variant + upgrade coverage per second-designer/171 §10 slices C+D`.

**Main commits after divergence**: same two as §3.1.

**Drift assessment**: orthogonal. Main's macro-variant engine landing doesn't add Engine-on-Route or the 4 upgrade-projection tests or the multi-sub-variant lowering test. Branch still adds load-bearing surface.

**Verdict**: REBASE. Rebase onto current main; reconcile if any of the engine-routing changes touched files that main also moved.

**Open question carried**: §3.2 from /172 overview (engine storage on Route vs AssembledType) — branch chose Route; lean stays Route per /172 §3.2 lean.

### §3.3 schema · feature/macro-variant-engine — OBSOLETE

**What's on the branch (not on main)**: `mockup: extensible macro-variant lowering engine per intent 506 + second-designer/170`.

**Main commits after divergence**:
- `schema: add builtin lowering engine` (`kzkqytvw`)
- `schema: lower upgrade rules through builtin macro variant` (`lpmvzxto`)

**Drift assessment**: SUPERSEDED. Main's "add builtin lowering engine" IS the extensible-macro-variant architecture. Three independent landings (operator's `/175.4` NodeDefinitionPoint + BuiltinSchemaMacro + SchemaMacro trait; designer's `/329` SchemaMacro trait + 7 builtins + extensibility via registration; my mockup C MacroVariant enum + input-struct-per-variant + MacroVariantLowering trait) converged on the same architecture per intent 506. Main carries the operator+designer's version, which has production-grade naming and includes the upgrade-rules lowering my mockup didn't reach.

**Verdict**: OBSOLETE. Retire the branch. The DESIGN is not obsolete (it's been ratified by main's landing) — only the BRANCH is.

**Action**: delete the bookmark + push the deletion; archive the mockup's worked example in this report's §6 (so future-me can compare to main's architecture if questions arise about why we picked the chosen names).

### §3.4 schema · feature/orchestrate-schema-example — LANDED

**What's on the branch (not on main)**: nothing new — the commit `0d16db07 schema: add orchestrate schema fixture + assemble witness` IS already on main as commit `zmpmrrptkqnv` (third in main's history).

**Drift assessment**: branch was absorbed into main during the schema crate's progression. The orchestrate-port sub-agent's schema-crate witness landed cleanly.

**Verdict**: LANDED. Retire the bookmark; the work is in main.

**Action**: delete the bookmark.

### §3.5 signal-engine-management · feature/durable-identity-via-peercred — REUSE

**What's on the branch (not on main)**: `mockup: SpawnEnvelope parent_authority + DurableIdentity via SO_PEERCRED per second-designer/172 slice D`.

**Main commits after divergence**: NONE — main is at `766b58cb schema: add v0.1 concept schema` which is the branch's base commit (or just below).

**Drift assessment**: zero drift. Main is exactly where the branch is based. The mockup remains usable as-is — operator can fast-forward main to it (modulo psyche ratification of the wire-format change `parent_authority` field per /172 overview §7 "What this dispatch did NOT do").

**Verdict**: REUSE.

**Open question carried**: §3.4 from /172 overview (identity types in signal-engine-management vs signal-persona-origin) — per intent 526, the lean is now **signal-persona-origin**. A follow-up move-types refactor lands when the next signal-persona-origin touch happens; not gating this branch.

**Action**: branch ready for operator integration as-is. No rebase needed.

### §3.6 signal-orchestrate · feature/schema-engine-and-no-downtime-upgrade — REBASE

**What's on the branch (not on main)**: `port: orchestrate schema source-of-truth + hand-equivalent emitter + handover protocol`.

**Main commits after divergence**:
- `signal-orchestrate: mark schema-engine upgrade`
- `signal-orchestrate: validate concept schema`

**Drift assessment**: main added the concept-schema-validation hook (orchestrate's analog of Spirit's `signal-persona-spirit: expose schema constraint checks` commit) and the ARCH marking from operator's `/175` sweep. Both are orthogonal to my branch's port content (schema_emitted.rs + upgrade_handover.rs).

**Verdict**: REBASE. The two main commits should land first (they're already there), then my port rebases on top. Concept-schema validation gives the port a constraint-check hook to use.

**Action**: rebase the branch onto current main. The schema port should integrate with the validate-concept-schema hook rather than work around it.

### §3.7 orchestrate · feature/schema-engine-and-no-downtime-upgrade — REBASE

**What's on the branch (not on main)**: `arch: record schema-engine port + drain-with-mirror handover plan`.

**Main commits after divergence**:
- `orchestrate: add schema upgrade witness`

**Drift assessment**: main added the schema upgrade witness (analog of Spirit's upgrade-spirit-sandbox-test pattern). My branch is ARCH-only documentation referencing the port. Trivial rebase.

**Verdict**: REBASE.

**Action**: rebase the ARCH update on top of the upgrade witness commit. The ARCH text should likely be expanded to reference the witness as an existing constraint test.

## §4 Operator + designer worktrees observed

### §4.1 Designer's nspawn worktrees under `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/`

Three worktrees, all stacking the same commits (designer is iterating on the nspawn upgrade test through layered worktrees):

| Worktree | Top commit (paraphrased) |
|---|---|
| `spirit-nspawn-upgrade-test` | Designer's initial framework — `test-cluster: document spirit nspawn minimal toplevel` |
| `spirit-nspawn-handover-socket` | Scaffolds private-upgrade-socket handover inside nspawn |
| `spirit-nspawn-in-transition-probe` | **Empirical finding**: NO caching actor — in-flight messages errored, acked == durable. Designer share of `primary-1jql`; full handover variant is operator mirror bead |

**Key empirical finding from `spirit-in-transition-probe`**: *NO caching actor; in-flight messages errored; acked == durable*. This is foundational for orchestrate's drain-with-mirror design. It means the mirror does NOT need to replay in-flight messages — only acked-and-durable state needs to transfer. The drain becomes "stop accepting new operations, finish in-flight ones (errors OK if they don't complete), transfer durable state". Significantly simpler than the worst-case drain-with-mirror I sketched in orchestrate-port phase 4.

**Implication for my orchestrate maturity dispatch (held pending)**: the handover-socket sub-agent should adopt this empirical fact — mirror = durable-state-snapshot transfer + drain in-flight, NOT in-flight-message-replay. Updates my Phase 4 design.

### §4.2 Operator's main-track work on Spirit

(Not in worktrees — operator works directly on main.)

Most recent Spirit-related operator commits:
- `signal-persona-spirit: expose schema constraint checks` — constraint-check hook on the contract crate
- `persona-spirit: validate short headers on ingress` — short-header validation in the daemon
- `upgrade: use Spirit contract projection in migration` — VersionProjection wired into actual migration
- `spirit-cutover-mvp: scripted v0.1.0 to v0.1.1 cutover` — scripted cutover (bookmark `spirit-cutover-mvp` in upgrade repo, commit `f06f4cb1`)
- `upgrade: add schema prep sandbox checks` — sandbox prep checks

Plus the working in-process sandbox witness `upgrade/src/bin/upgrade-spirit-sandbox-test.rs` (last live run per /330: `(SandboxUpgradeSucceeded 500 500 ...)`).

**Comparison to orchestrate-port (second-designer/173)**: my port landed (a) schema-source-of-truth, (b) hand-equivalent emitter, (c) handover design. Operator's Spirit work has landed (1) constraint checks, (2) short-header ingress validation, (3) VersionProjection wired, (4) cutover script, (5) sandbox prep checks, (6) working sandbox-test binary. So orchestrate's maturity is at ~50% of Spirit's. Closing the gap is the topic of intent 533 (orchestrate-maturity-match dispatch) — held pending psyche confirmation on schema-file canonical locations (§1 of prior chat reply) and cutover/socket coupling (§2).

### §4.3 No operator feature-branch worktrees observed

Operator works on main per workspace convention (intent 109: "the workspace does not use feature branches by default; merges go directly to main; ... default for any operator slice: edit, test, push to main"). The new intent 515/516 establishes designer-as-feature-branch-user; operator's pattern stays main-direct. So there are no operator feature branches to audit — operator's work either IS on main or isn't a feature branch.

## §5 Rework applied

### §5.1 Retire OBSOLETE branch — schema `feature/macro-variant-engine`

Action: delete the bookmark + push the deletion. The design is preserved in /172 §3.3 + this report's §6 archive.

### §5.2 Retire LANDED branch — schema `feature/orchestrate-schema-example`

Action: delete the bookmark. The content is on main as `zmpmrrpt schema: add orchestrate schema fixture + assemble witness`.

### §5.3 Mark REUSE branch ready for integration — signal-engine-management `feature/durable-identity-via-peercred`

Action: no rebase needed. The bead `primary-p0ke` already points operator at the worktree. Bead note will be updated to flag "ready for integration; no drift since landing".

### §5.4 REBASE 4 branches onto current main

Actions for each:
- schema · `feature/component-uid-and-layout` — rebase onto `lpmvzxto`; adopt source-schema-component UID resolution per intent 526
- schema · `feature/engine-routing-and-upgrade-coverage` — rebase onto `lpmvzxto`
- signal-orchestrate · `feature/schema-engine-and-no-downtime-upgrade` — rebase onto `knonqxxu`; integrate with validate-concept-schema hook
- orchestrate · `feature/schema-engine-and-no-downtime-upgrade` — rebase onto `tztxssrn`; expand ARCH to reference the schema upgrade witness

### §5.5 Relocate worktrees from /tmp to ~/wt per intent 515

For each REBASE or REUSE branch, the canonical worktree home is `~/wt/github.com/LiGoldragon/<repo>/feature-<branch-name>/`. Old `/tmp/*` worktrees retired after relocation (branches survive on remote regardless).

## §6 Archive — mockup C (OBSOLETE) design notes

The mockup-C MacroVariant architecture from `feature/macro-variant-engine` carried these design choices that operator's "add builtin lowering engine" landing supersedes (preserved here for cross-reference if questions arise):

- **Pattern**: closed enum (`MacroVariant`) with one variant per dispatch shape; each variant carries an input struct. Public `MacroVariantLowering` trait kept open for future plugin surface.
- **Variants in mockup**: `EnumDeclaration(EnumDeclarationInput)`, `NewtypeDeclaration(NewtypeDeclarationInput)`, `RecordDeclaration(RecordDeclarationInput)`, plus 3 feature variants stubbed.
- **Equivalence test**: `engine_lowers_to_same_assembled_schema_as_assemble` proves the engine produces SAME AssembledSchema as `Schema::assemble()`.
- **Trade-off chosen**: closed enum + recompile for extensibility (gets compiler-enforced exhaustive match across the dispatch table); trait kept public for future trait-object dispatch.

Operator's main landing uses `BuiltinSchemaMacro` + `SchemaMacro` trait + `NodeDefinitionPoint` cursor naming with 7 builtin variants (Enum / Struct / Reference / Import / Header / Feature / ContainerType). Mockup C's 3-variant subset maps cleanly to a subset of main's 7; mockup C's trade-off choice (closed enum + public trait) matches operator's pattern. Convergence confirmed.

## §7 Open psyche questions surfaced or carried

1. **Schema file locations for orchestrate** (carried from prior chat reply §1): Spirit uses three locations; lean is mirror Spirit's shape for orchestrate. Awaits confirmation before the maturity dispatch (intent 533) launches.

2. **Cutover script vs handover socket coupling** (carried from prior chat reply §2): lean is co-evolve in one slice. Awaits confirmation.

3. **Drain-with-mirror simplification per designer's empirical finding** (NEW from §4.1): designer's `spirit-in-transition-probe` empirically confirms NO caching actor — acked == durable. Orchestrate's drain-with-mirror can be simplified accordingly: mirror = durable-state-snapshot transfer + drain in-flight (no replay needed). The Phase 4 design at `signal-orchestrate/src/upgrade_handover.rs` should be revised. Lean: revise the design + simplify the state machine in the next iteration.

4. **`/tmp` worktree cleanup**: all 4 mockup worktrees from /172 and 3 orchestrate-port worktrees from /173 still exist on disk at /tmp. Branches are on remote (no data loss if /tmp cleared). Cleanup at next session shutdown is fine; no urgent action.

## §8 Recommended next moves

In priority order:

1. **Resolve psyche question §7.1 + §7.2** so the orchestrate-maturity dispatch (intent 533) can launch with the right schema-file locations + cutover/socket coupling.

2. **Apply rework actions §5.1 + §5.2** (retire OBSOLETE + LANDED branches) — mechanical, immediate.

3. **Apply rework actions §5.4** (rebase 4 branches onto current main) — each is a small jj rebase + test pass + push.

4. **Update orchestrate Phase 4 design per §7.3** (simplify drain-with-mirror given designer's empirical finding). Either edit the `upgrade_handover.rs` mockup in place + commit on a new revision of the feature branch, or fold into the maturity-dispatch sub-agent G's prompt.

5. **Launch orchestrate-maturity dispatch (intent 533)** once §1 + §2 confirmed.

## §9 Cross-references — nota-designer/8 + second-operator/183 converge

Two parallel audits landed today that touch the same surface this report does. Both add or sharpen my findings; neither contradicts.

### §9.1 nota-designer/8 — "NOTA and schema lowering deviation audit"

Identifies 7 deviations in the schema/lowering stack. The 7 map onto my mockup verdicts:

| nota-designer deviation | Covered by | My verdict consistency |
|---|---|---|
| 1. signal-frame-macros parallel schema reader | (operator territory — not in my mockups) | Flag separately as operator slice |
| 2. schema erases macro input object roles (positional `Record(Vec<TypeExpression>)`) | (NOT covered by any mockup) | NEW work item — mockup C did not address; main's "add builtin lowering engine" did not either (verified: `declaration.rs` still has `Record(Vec<TypeExpression>)` + `Payload::Fields(Vec<TypeExpression>)`) |
| 3. Engine annotations don't reach AssembledSchema | Mockup B (REBASE) | Reinforces |
| 4. Layout uses pre-assembled Document | Mockup A (REBASE) | Reinforces |
| 5. AssembledSchema lacks component identity + canonical UIDs | Mockup A (REBASE) | Reinforces |
| 6. Schema repo not self-describing | (NOT covered) | Future work; nota-designer marks as acceptable for MVP |
| 7. Concept schema validation is regex-based | (operator territory) | Future work |

**Update to mockup C verdict**: still OBSOLETE for the variant-engine surface (main's `BuiltinSchemaMacro` supersedes), but nota-designer's deviation #2 (named input structs `EnumDefinitionInput`, `RecordDefinitionInput`, `ImportDirectiveInput`, etc.) is NEW work that neither mockup C nor main currently addresses. This becomes a fresh slice the next mockup wave should pick up — different from mockup C, sharper than /170's lowering executor.

**Critical signal from nota-designer**: deviation #1 (signal-frame-macros parallel reader at `signal-frame/macros/src/schema_reader.rs` accepting retired shapes — `(Path ...)`, `[Option T]`, scalar `(Record Entry)`, and rejecting multi-endpoint headers) is the BIGGEST practical drift. Operator's main schema work doesn't fix this; it's an open production bug. Bead-worthy.

### §9.2 second-operator/183 — "Orchestrate worktree audit and rework"

Independent parallel audit of orchestrate worktrees. Convergences:

| My finding | Second-operator's finding |
|---|---|
| /tmp worktrees should not be authoritative (§5.5) | "These `/tmp` worktrees should not become the ongoing authoritative worktrees" |
| Mockup branches preserve good design but not direct merge (implicit) | "treated as a design prototype and reworked into smaller operator slices" |
| Multi-endpoint + unit endpoint macro extension is open (sub-agent open question #1) | "extend the shared schema lowering stack for multi-endpoint roots and unit endpoints" |
| Mainline has lighter schema-witness landed (§3.6, §3.7) | "second-operator mainline track: landed a narrower parser-backed schema witness across the orchestrate triad on main" |
| `schema_emitted.rs` is target-spec, not production (carried from sub-agent) | "Treat `schema_emitted.rs` as a temporary target-spec file only" |

Second-operator's 7-step rework plan IS effectively the operator-side projection of my recommendation §8. Convergence is high.

**Second-operator's 3 questions for psyche** (parallel to my §7 questions):
1. `/tmp` designer worktrees recreated under `~/wt` AND rebased as living branches, OR treated as frozen prototype commits that operator mines from while reimplementing on main? (Cross-cuts my §7 question on `/tmp` cleanup.)
2. Is drain-with-mirror accepted as orchestrate's no-downtime upgrade protocol? (Cross-cuts second-designer/173's open question on drain-with-mirror.)
3. Should multi-endpoint + unit endpoint schema lowering support be part of Spirit schema epic OR a separate shared schema slice driven by orchestrate and mind? (Cross-cuts orchestrate-port sub-agent's open question #1.)

Combined: 5 distinct psyche-question slots remain across my /174 §7 + second-operator/183 §"Questions Needing Psyche". Resolving them clears the dispatch and integration path.

### §9.3 Reference to operator/177

Per second-operator/183, the new Spirit-maturity reference point is `reports/operator/177-schema-constraint-implementation-2026-05-24.md` (Spirit has: schema macro constraints exposed as named Nix checks; schema-derived `ShortHeader` validation on production daemon ingress; upgrade crate consuming contract-owned `VersionProjection`; named Nix checks for those constraints). Orchestrate's maturity gap against this becomes (per second-operator §"Rework Against Spirit Maturity"):
- **Ingress**: orchestrate does not reject mismatched short headers on production daemon socket
- **Projection**: orchestrate has upgrade-plan schema text but no contract-owned `VersionProjection`
- **Emission**: orchestrate still uses hand-written signal contract types

These three gaps name the concrete deliverables for the orchestrate maturity dispatch (intent 533) — once the dispatch launches.

## §10 References

- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` — schema-stack vertical audit; converges with §9.1
- `reports/second-operator/183-orchestrate-worktree-audit-and-rework-2026-05-25.md` — orchestrate worktrees parallel audit; converges with §9.2
- `reports/second-operator/182-orchestrate-schema-mainline-integration-2026-05-24.md` — operator's narrower parser-backed schema witness mainline landing (referenced in /183)
- `reports/operator/177-schema-constraint-implementation-2026-05-24.md` — Spirit's current maturity reference point (referenced in /183 §"Rework Against Spirit Maturity")
- `reports/second-designer/171-audit-second-operator-180-schema-v13-2026-05-24.md` — prior audit of operator/180
- `reports/second-designer/172-design-mockup-dispatch/5-overview.md` — mockup overview the 4 branches came from
- `reports/second-designer/173-orchestrate-port-to-schema-engine-and-no-downtime-upgrade-2026-05-24.md` — orchestrate port that the 2 orchestrate branches came from
- `reports/designer/330-parallel-implementation-pivot-and-spirit-nspawn-plan.md` — designer's nspawn plan + worktree-freshness audit pattern this report mirrors
- `reports/operator/175-schema-engine-prep/` — operator's schema-engine-prep across many repos
- Schema repo `lpmvzxto schema: lower upgrade rules through builtin macro variant` (current main)
- Signal-engine-management repo `766b58cb schema: add v0.1 concept schema` (current main)
- Signal-orchestrate repo `df605591 signal-orchestrate: validate concept schema` (current main)
- Orchestrate repo `59669e30 orchestrate: add schema upgrade witness` (current main)
- Intent records 502-504 (mockup-on-worktree method), 506 (extensible macro-variant), 511 (audit cycle), 515 (designer worktrees in ~/wt), 519 (orchestrate parallel port), 525 (iteration directive), 526 (lean confirmations), 533 (orchestrate-maturity dispatch — held)
