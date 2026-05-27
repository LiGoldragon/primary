# Audit — source staging prototype iteration (`system-operator/165`)

*Designer audit of `reports/system-operator/165-lojix-source-staging-prototype-and-full-component-critique.md`. Per psyche directive 2026-05-27 ("audit the work that the system operator has done"). The work is substantively good and follows the prototype-iteration methodology (Spirit 971-974) faithfully; this audit surfaces (1) the cross-arc collision risk with the still-running system-designer iteration-2 subagent + the parallel `operator/219` spirit-next iteration, (2) component-fullness scoring deltas vs `/35`'s baseline, (3) alignment with the workspace's Signal/Nexus/SEMA terminology refresh (records 963-970), (4) the operator's own next-iteration recommendation against the orchestrator-level alternatives.*

## What was audited

The system-operator landed commit `qpkvvxxxwrqq` ("schema-deep: add source staging actor plane", short `5145ae61`) on the `schema-deep` branch of `lojix` on top of `/35`'s baseline `rnwxqrlzmrmm`. Pushed to `origin/schema-deep`. Net diff: 26 files, +562 / −81 lines.

What landed:

- Schema additions in `schema/lojix.schema`: `SourceDigest`, `SourceRecord`, `SemaCommand::RecordSource`, `ActorRequest::StageSources`, `ActorReply::SourcesReady`, `Phase::StagingSources`. `BuildRecord` now carries the `SourceDigest` it built (typed dependency).
- New `src/runtime/source_stager.rs` (141 lines) — a real Kameo actor with non-ZST state (source artifact directory + most-recent staged source).
- Submit pipeline reshape: `PlanRecord → SourceStager → Store::RecordSource → Builder`. `Builder` + `ProcessToolchain` now consume `SourceRecord`, not `PlanRecord`.
- `Store` extended with source ledger + `SourcesSnapshot` for tests.
- Trace + observation witnesses for the new staging phase.
- Source artifact written as schema-generated NOTA (`SourceRecord::to_nota()`), not a new key/value format.
- `AGENTS.md` + `ARCHITECTURE.md` updated per record 944's continuous-manifestation discipline (no longer claims "skeleton"; ARCH includes source-staging plane).
- 1 new test: `tests/source_staging.rs::lojix_next_submit_stages_sources_before_build` — asserts staging commits before build consumes.

Self-critique in `/165` honestly enumerates remaining gaps: ARCA not used, SEMA still in-memory (DatabaseMarker placeholder), criome local enum, owner-signal absent, Horizon still `HorizonView(Text)`, nspawn still sandbox marker, source staging doesn't consume real Git refs or ARCA content-addressed objects.

## Verdict — substantively sound, methodologically aligned

The work is the right shape for an iteration under records 971-974. Three things the system-operator got right:

1. **Mined the right priors.** Read `/36` (designer audit of `/162`), `/163` (operator self-critique of `/162`), `/164` (predecessor system-operator audit), and `/35`'s baseline. The SourceStager choice traces directly to `/36 §"The repository-ledger localhost issue should be solved at the substrate layer"` + `/163` finding 4 ("Repository Source Distribution Should Be A Schema/Actor Noun, Not A Footnote"). The intellectual lineage is honored.
2. **Chose a tractable slice.** Source staging is a single deploy-pipeline plane (PlanRecord → SourceStager → Store::RecordSource → Builder) — small enough to land in one iteration, real enough to exercise schema-emitted nouns + Kameo actor + sema-emitted command + trace + observation, BroadEnoughToProve typed-noun discipline propagates through new pipeline planes.
3. **Self-critique is honest.** `/165 §"Full-Component Critique"` lists 7 specific gaps where the prototype is still partial. The "explicitly lying" framing about `DatabaseMarker::memory()` is exactly the kind of audit pressure record 973 names ("audit findings should feed implementation directly... instead of accepting a partial mock"). The recommendation to do SEMA persistence next because it's "the narrowest place where the current prototype is explicitly lying" applies record 973's discipline to itself.

Three things on execution quality:

- **Schema-first authoring.** All new nouns added to `schema/lojix.schema` first; runtime methods attach to schema-emitted nouns per `skills/abstractions.md §"Schema-emitted nouns"`. No hand-written parallel mirrors. No free functions in production code (verified by `/35`'s `no_free_functions` architectural-truth test continuing to pass).
- **Sema-emitted command for source recording.** `SemaCommand::RecordSource` is NEW — the source ledger gets first-class typed state, not an ad-hoc side channel. This is exactly the schema-deep depth that the workspace direction calls for.
- **Tests + Nix witness pass on remote builder.** `nix --max-jobs 0 flake check -L` dispatched to Prometheus per Spirit 906 constraint. Build / test / fmt / clippy / `schema-deep-build-script` / `schema-deep-actor-mailboxes` / `binary-boundary-test` all pass. Discipline followed.

## Component-fullness scoring delta

Per Spirit record 972's 8-component fullness criterion and `/37/1`'s per-component scoring of `/35`'s baseline at 5.0/8.0, the system-operator's iteration's delta:

| # | Component | `/35` baseline | After `/165` | Delta | Note |
|---|---|---|---|---|---|
| 1 | NOTA structure | 0.7 | 0.7 | 0 | Unchanged. |
| 2 | Schema macro lowering | 0.9 | 0.9 | 0 | New nouns lower cleanly through schema-next. |
| 3 | Assembled schema | 0.8 | 0.8 | 0 | Unchanged. |
| 4 | Rust emission | 0.9 | 0.9 | 0 | New types emit cleanly. |
| 5 | Generated signal | 0.3 | 0.3 | 0 | No Communicate trait, no DatabaseMarker (placeholder only). |
| 6 | Nexus mail keeper | 0.2 | 0.2 | 0 | Still `OperationDispatcher` (Executor-naming); no mail lifecycle. |
| 7 | SEMA state handling | 0.3 | 0.4 | +0.1 | New `SemaCommand::RecordSource` adds typed surface area; backing still in-memory. |
| 8 | Spirit runtime behavior | 0.9 | 0.9 | 0 | Pattern maintained. |
| | **Aggregate** | **5.0** | **5.1** | **+0.1** | Modest fullness lift. |

The `/165` iteration's primary contribution is **width** (a new pipeline plane with schema-emitted nouns) rather than **depth** on the 8 components. Component 7 (SEMA) lifts by 0.1 because new typed commands extend the surface, but the underlying durability gap is unchanged. Components 5 (Communicate, DatabaseMarker) and 6 (Nexus mail keeper, lifecycle) are the load-bearing depth gaps `/37`'s iteration was dispatched to address; `/165` does not touch them. This is not a defect — the system-operator chose a different slice.

The implication: `/165` + iteration-2 + `operator/219` together cover MORE of the 8-component fullness criterion than any single iteration. The convergence (next section) is the interesting orchestrator-level concern.

## Cross-arc collision + convergence — THREE parallel prototype tracks

Three iterations of the prototype-driven-development methodology are running in parallel this afternoon, each picking a different slice:

| Track | Lane | Branch | Slice | Component-fullness gain | Status |
|---|---|---|---|---|---|
| `/35` | system-designer (baseline) | `schema-deep` (lojix) | initial schema-deep pilot, 9 actors, 10 tests | 5.0/8.0 | shipped (2026-05-27 earlier) |
| `/165` | system-operator (this audit) | `schema-deep` (lojix) on top of `/35` | source staging actor plane | +0.1 → 5.1/8.0 | shipped (commit `5145ae61`, pushed) |
| `/37` iteration 2 | system-designer (my subagent — still running) | `schema-deep` (lojix) — same branch | Nexus mail keeper + sema-engine durable + Communicate trait + DatabaseMarker | target +1.7 → 6.7/8.0 | in flight |
| `operator/219` | operator | spirit-next branch | NexusInput/NexusOutput + SemaInput/SemaOutput + DatabaseMarker + MailLedgerEvent | parallel target on a DIFFERENT prototype (spirit-next, not lojix) | shipped (dirty file when system-operator audited; presumably committed by now) |

Three immediate cross-arc concerns:

### 1. Collision risk between `/165` and `/37` iteration 2 on the same branch

My `/37` iteration-2 subagent was dispatched while the system-operator was working. Both edit `schema-deep` branch in the SAME worktree (`~/wt/github.com/LiGoldragon/lojix/schema-deep`). Verified via `jj log`: the system-operator's commit `qpkvvxxxwrqq` landed; working copy `xvvwskwuqmmx` is empty (subagent has read files but not yet committed). If the subagent's plan was framed against `/35`'s state (commit `rnwxqrlzmrmm`), they need to incorporate `/165`'s new pipeline shape (SourceStager actor between Plan and Builder). The subagent's brief targets `dispatcher.rs` rename (Executor→Nexus) — the system-operator added 88 lines to `dispatcher.rs` per the diff stat. Manual merge / rebase work either by the subagent on completion or by me as orchestrator.

**Audit recommendation**: when the subagent returns, the synthesis (`/37/N-overview.md`) must explicitly reconcile `/165`'s SourceStager addition with whatever rename/reshape the subagent did. If the subagent missed `/165`, treat it as integration work for me to flag in the iteration-3 pickup queue.

### 2. `/165` and `/37` iteration 2 are SOLVING DIFFERENT GAPS

`/165` addresses the **horizontal-pipeline-width** gap (a new plane the deploy domain didn't yet have); `/37` iteration 2 addresses the **vertical-component-depth** gaps (Nexus mail keeper not built; SEMA in-memory; no Communicate trait; no DatabaseMarker). Both are valid responses to records 971-974. The system-operator's choice of width over depth is a reasonable orchestrator-level disagreement; their choice was made before the system-designer's iteration-2 brief landed.

**This is not a defect** — multi-track parallel iterations are the workspace's normal mode (per `skills/double-implementation-strategy.md`). The orchestrator-level reading: convergence comes at iteration 3 or later, when the depth components are wired in alongside the widened pipeline.

### 3. `/operator/219` did `/37` iteration-2's work on SPIRIT-NEXT instead

`/operator/219` (operator lane, NOT system-operator) did NEARLY IDENTICAL work to what my iteration-2 subagent is doing — but on `spirit-next`, not lojix:

- Added schema nouns for `NexusInput`, `NexusOutput`, `SemaInput`, `SemaOutput`, `DatabaseMarker`, `MailLedgerEvent`.
- Wired runtime: `Engine` records `MailLedgerEvent::Sent`/`Processed`; `Store::apply(SemaInput)` as single writer with `DatabaseMarker` reply.
- Pipeline: `Nexus mail ledger → NexusInput → NexusOutput::Sema(SemaInput) → Store → SemaOutput → NexusOutput::Signal(Output)`.
- 10-component fullness audit table covering NOTA / Schema macro lowering / Assembled schema / Rust emission / Signal / Nexus / SEMA / Import-export / Runtime Spirit / Upgrade path.

This is the spirit-next equivalent of what `/37`'s iteration-2 subagent will produce for lojix. **The shared schema-emitted nouns (DatabaseMarker, MailLedgerEvent, NexusInput/NexusOutput) likely belong in a shared `schema/core.schema` or equivalent rather than being duplicated in each component's schema.** This is exactly the kind of substrate-extraction question record 974 names: "when a designed component is too incomplete to use, develop it further rather than bypass." The pattern is repeated in two places; the next step is to extract.

**Audit recommendation for the orchestrator pickup queue**: `DatabaseMarker`, `MailLedgerEvent`, `NexusInput`, `NexusOutput`, `Import`, `Export` are CROSS-COMPONENT mail-and-runtime-triad nouns. They should live in a shared schema home (per `/392 §"Where the work actually lives"` table — natural homes: a new `schema/core.schema` in schema-next, or per `/390 §"Mail state manager"` a `persona-mail` crate, or extending signal-frame's schema to host these). Both `/165`'s `SourceRecord` (component-local) and the cross-component mail/marker nouns illustrate the schema-home-decision needs an explicit answer.

## Discipline observations (small)

Three observations; none reduce the positive substantive reading.

### 1. Workspace-direction naming partially lagged

Records 963-970 (2026-05-27) renamed **Executor → Nexus** and defined Nexus as the mail keeper. `/35`'s baseline used "Executor" naming (pre-rename). The system-operator's `/165` does NOT rename — it keeps the `OperationDispatcher` actor name and the `Engine::handle` shape. This is acceptable for `/165`'s scope (source staging slice; rename is `/37`'s territory) but is worth flagging: workspace-direction terminology drift should be tracked. The system-operator could have added a one-paragraph note to `/165 §"Full-Component Critique"` saying "naming alignment to Nexus per record 964 is iteration-N work, not this iteration's scope."

### 2. Bead-shape would help the next-iteration sequence become claimable

`/165 §"Next Prototype Slice"` is a 3-step ordered list with a clear recommendation (SEMA persistence first). Same observation as `/36 §"Discipline observations" #2`: bead-shape (per-item owner-lane suggestion + dependency graph + estimated lift) would make the sequence dispatch-ready for other lanes. Operator-class reports tend to surface findings and let claims emerge through the work loop; for an iteration whose explicit next move is to be picked up by another agent or lane, bead-shape closes the loop.

### 3. Per-repo INTENT.md/ARCHITECTURE.md manifestation is good but not comprehensive

`/165` updated `AGENTS.md` and `ARCHITECTURE.md` in the lojix repo (per record 944) — confirmed in the diff stat. Good discipline. But records 944's continuous-manifestation rule extends to EVERY substrate repo the work touches. `/165` likely touches sema-engine implicitly via the SemaCommand::RecordSource expansion (the in-memory Store needs to be redb-backed eventually); no sema-engine INTENT.md/ARCHITECTURE.md edit landed because sema-engine isn't yet consumed. Reasonable. But if `/165`'s recommended-next-step (SEMA persistence) is taken, sema-engine becomes a touched repo and its INTENT/ARCH must update per record 944. The system-operator's recommendation should note this dependency.

## Substantive observations

### Source-staging digest is derived, not content-addressed — flagged honestly

`/165 §"Full-Component Critique"` notes: "Source staging does not yet consume Git refs, ARCA objects, or content-addressed proposal artifacts. Its digest is derived from deployment identifier, Horizon text, and target node." This is correct self-criticism. The derived digest is a temporary stand-in for what should be a content-addressed hash (Blake3 of the source tree) once ARCA or git-refs land. The schema-emitted `SourceDigest` newtype IS the right type-system shape; the runtime fills it with a temporary derivation; the next iteration replaces the filler with real content-addressing.

This is the load-bearing pattern of record 973: identify the placeholder, name what should fill it, plan the next iteration to fill it. The system-operator did this for `DatabaseMarker::memory()` ("the narrowest place where the current prototype is explicitly lying") and equally applies it to `SourceDigest`. Both deserve iteration-3 work.

### Pipeline reshape preserves backwards-compatibility for Builder

`Builder` now consumes `SourceRecord` (not `PlanRecord`); `ProcessToolchain` updated accordingly. The change is breaking at the Rust API level but contained inside the daemon — the wire surface (Input/Output) is unchanged. CLI clients see no API change. This is the right boundary: internal restructuring inside the schema-deep depth, with the wire contract stable.

### Trace + observation extensions are exactly the schema-deep witness pattern

`Phase::StagingSources` was added; trace + observation witnesses fire for the new phase. This continues `/35`'s discipline that every plane is observable through a typed trace witness. The new test `lojix_next_submit_stages_sources_before_build` asserts the pipeline ordering — exactly what `skills/actor-systems.md §"Traces are required"` mandates.

## Recommendations

### For the system-operator (next iteration of `/165`'s arc)

1. **Carry record 974 forward when picking the next slice.** Their own recommendation (SEMA persistence) is correct AND `operator/219` already did it for spirit-next; consider whether to:
   - (a) Re-do SEMA persistence work in lojix specifically (duplicates spirit-next's pattern), OR
   - (b) Extract the cross-component mail/marker nouns (DatabaseMarker, MailLedgerEvent, NexusInput/NexusOutput) into a shared schema home FIRST so both lojix and spirit-next consume from the same source.
   Path (b) is more substrate-aligned per record 974's "develop the component further rather than bypass" — the missing substrate is the shared schema home, not just lojix's local store.
2. **Bead-shape the next-slice list.** Three numbered next steps in `/165` would dispatch cleanly to whichever lane picks up next, with per-step lane suggestion + dependency.
3. **Coordinate with the still-running `/37` iteration-2 subagent.** Both edit `schema-deep` branch in the same worktree. When the subagent completes, the synthesis (`/37/N-overview.md`) will reconcile. Until then, the next system-operator iteration should NOT push to `schema-deep` until the subagent's commits land or are explicitly merged.

### For the orchestrator (this lane's pickup queue)

4. **Reconcile `/165` + `/37` iteration 2 + `operator/219` in the iteration-3 frame.** Three parallel tracks need an explicit convergence story. Candidate frame: `/39-three-track-prototype-convergence-2026-05-27/` (or equivalent meta-report) mapping the cross-pollination opportunities, the shared schema-home decision, and the iteration-3 slice that aligns the tracks.
5. **Surface the shared schema-home decision to the psyche.** Both `/165` (lojix) and `/operator/219` (spirit-next) want schema-emitted nouns that are likely cross-component (DatabaseMarker, MailLedgerEvent, NexusInput/NexusOutput, Import/Export). Where do these live? Candidate homes: (a) a new `schema/core.schema` in schema-next (cross-cutting substrate); (b) a new `persona-mail` crate per `/390 §"Mail state manager"`; (c) extending signal-frame's schema with these nouns. Psyche decision unblocks iteration 3 across both prototypes.
6. **Track workspace-direction terminology drift.** `/35` + `/165` use Executor naming; records 963-970 renamed to Nexus. `/37` iteration 2 was dispatched to do the rename in lojix. `/operator/219` already uses Nexus naming for spirit-next. The rename + naming alignment across the whole schema-deep direction is a coordinated multi-repo arc — not blocked, but should be tracked.

### For the psyche (the load-bearing decisions)

7. **Decision: shared schema home for cross-component mail/marker nouns.** (a) `schema/core.schema` in schema-next, (b) new `persona-mail` crate, (c) extend signal-frame's schema. Affects iteration 3 across `/165`, `/37`, `/operator/219`. Designer-orchestrator pickup if you don't pick directly.
8. **Decision: persona-mail extraction NOW (iteration 3) or LATER.** `/37`'s frame deferred persona-mail extraction unless the subagent's design demanded it; `operator/219`'s parallel work suggests the demand is real (two consumers wanting the same primitive). Authorizing extraction now bundles cleanly with decision 7.

## Bottom line

`/165` is a substantively sound iteration of the prototype-driven-development methodology (records 971-974) — the source staging slice is the right shape, the implementation follows schema-deep discipline, the self-critique is honest. The component-fullness lift is modest (+0.1 → 5.1/8.0) because the iteration chose width over depth; complementary depth iterations (`/37` iteration 2 + `operator/219`) are running in parallel. The three-track convergence question is the most load-bearing orchestrator-level concern raised by this iteration: shared schema home for cross-component mail/marker nouns needs a psyche decision before iteration 3 can land cleanly.

## See also

- `/system-operator/165-lojix-source-staging-prototype-and-full-component-critique.md` — the report this audits.
- `/system-designer/35-schema-deep-new-logics/3-overview.md` — baseline for the `schema-deep` branch.
- `/system-designer/37-prototype-schema-deep-iteration-2-nexus-mail-sema-engine-2026-05-27/0-frame-and-method.md` + `1-prototype-target-and-component-mapping.md` — concurrent iteration 2 (still running).
- `/operator/219-schema-full-stack-prototype-completeness-audit-2026-05-27.md` — parallel iteration on spirit-next with the Nexus/SEMA/Mail work.
- `/system-designer/36-criomos-reconciliation-audit.md` — earlier audit naming the SourceStager actor sketch that `/165` realized.
- `/system-operator/163-critique-of-162-after-schema-next-refresh-2026-05-27.md` — earlier critique with the 7-noun decomposition for source distribution.
- `/designer/392-vision-schema-driven-stack-canonical-2026-05-27.md` — workspace vision; 8-component fullness criterion.
- `/designer/390-wire-runtime-canonical-direction.md` — Communicate trait + mail state manager + DatabaseMarker design.
- Spirit records 971-974 — prototype-driven-development methodology; 8-component fullness criterion; develop-rather-than-bypass constraint.
- Spirit records 944 + 920 — continuous per-repo manifestation; subagent lane inheritance.
- `skills/double-implementation-strategy.md` — parallel-track convergence framing.
