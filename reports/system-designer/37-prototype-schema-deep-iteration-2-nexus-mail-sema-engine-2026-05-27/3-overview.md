# Overview — schema-deep iteration 2 (orchestrator synthesis)

*Orchestrator synthesis of the `/37` meta-report. Iteration 2 shipped — 8-component fullness lifted from 5.0/8.0 (62.5% per `/37/1`'s baseline scoring) to 6.7/8.0 (≈84%), hitting the target. Subagent commit `twvkkpypztsr` (short `8804082fc50d`) pushed to `origin/schema-deep-iteration-2`. Critical orchestrator finding: subagent created a SEPARATE branch to avoid colliding with system-operator's parallel iteration on the original `schema-deep` branch (`/165`'s source staging) — this surfaces the multi-track-convergence question I flagged in `/38` as an immediate amalgamation concern. Iteration-3 pickup queue + three open psyche decisions land below.*

## What landed

Subagent delivered all 7 brief items + 6 new tests on commit `twvkkpypztsr` / `8804082fc50d` pushed to `origin/schema-deep-iteration-2`. 5,060 lines net across 26+ files. New worktree at `~/wt/github.com/LiGoldragon/lojix/schema-deep-iteration-2/` parallel to `/35`'s `~/wt/.../lojix/schema-deep/`. Both branches share `/35` baseline (`rnwxqrlzmrmm`) as their common parent.

Substantive structure:

- **`schema/lojix.schema`** extended from 80 → 91 lines: added `DatabaseMarker`, `MailLifecycle`, reply-shape records. Per-component nouns continue to be the source of truth.
- **`src/runtime/nexus.rs`** (745 lines, NEW) — `NexusMailKeeper` actor replacing the old `OperationDispatcher`. Carries typed `MailEntry` with `MailLifecycle::{Sent, Queued, Processing, Replied, Failed}`. Hookable events (`MessageSentHook`, `MessageProcessedHook<Output>`) fire push-style per `skills/push-not-pull.md`. `Self IS the actor` per Kameo discipline.
- **`src/runtime/store.rs`** (578 lines, REWRITTEN) — replaces in-memory `Vec` with sema-engine `Engine` + `TableReference` per record family. Schema-emitted records implement `EngineRecord` directly (no parallel mirrors per `skills/abstractions.md §"Schema-emitted nouns"`). Counters persisted via `CounterRow` table — surviving daemon restart, witnessed by test #13.
- **`src/runtime/communicate.rs`** (115 lines, NEW) — `Communicate` trait + `UnixSocketCommunicate` concrete impl. Subagent's documented decision: lives inside lojix-next for this iteration (vs `signal-frame` / `schema-rust-next` / new abstract crate per `/390 §"Open questions" #1`); promotion to permanent home is iteration-3 work.
- **`tests/`** (1,131 lines) — 16 tests total: 10 baseline carried forward (updated for new API shapes — DatabaseMarker threading, sema-engine database path, NexusMailKeeper actor) + 6 new (`nexus_is_mail_keeper`, `message_lifecycle_hooks_fire`, `sema_engine_durable_across_restart`, `communicate_trait_round_trip`, `database_marker_in_every_reply`, `database_marker_state_hash_changes_on_write`).
- **`flake.nix`** added 3 new architectural-truth checks (`schema-deep-nexus-mail-keeper`, `schema-deep-sema-engine-backed`, `schema-deep-communicate-trait`). All 16 tests + 7 architectural checks + fmt + clippy + build pass under `nix flake check` dispatched to Prometheus per Spirit 906 constraint.
- **`INTENT.md`** (new, 116 lines) + **`ARCHITECTURE.md`** (rewritten, 258 lines) per record 944's continuous-manifestation discipline. Synthesises Spirit records 882-980 that bear on the iteration.

## Orchestrator's 8-component fullness audit — confirms 6.7/8.0

Per Spirit record 972 (the audit-against-fullness mandate), I re-score each component independently of the subagent's claim:

| # | Component | Subagent's score | My audit | Evidence | Notes |
|---|---|---|---|---|---|
| 1 | NOTA structure | 0.7 | **0.7** | nota-next consumed transitively via schema-next macro engine; same as `/35` baseline | StructureHeader not yet load-bearing in lojix-next; iteration-3 candidate but not blocking |
| 2 | Schema macro lowering | 0.9 | **0.9** | `build.rs:11-27` asserts macro registry coverage; DatabaseMarker + MailLifecycle + reply-shape records lower cleanly via the same pipeline | Brace-enum sugar not used (no need at this scale) |
| 3 | Assembled schema | 0.8 | **0.8** | Asschema consumed implicitly through the lowering → emission pipeline; no direct introspection needed | No `.asschema` persistence path exercised |
| 4 | Rust emission | 0.9 → 1.0 | **1.0** | `RustEmitter::default().emit_file` emits the full schema including Nexus mail surfaces (MessageIdentifier / MessageSent / NexusMail / MessageProcessed / InputNexus / OutputNexus per schema-rust-next 9a98eedd authored by parallel operator work today) | Emission fully exercised |
| 5 | Generated signal | 0.3 → 0.7 | **0.7** | DatabaseMarker stamped on every Output (`codec.rs:111-150`); Communicate trait added (`communicate.rs:34-38`); UnixSocketCommunicate concrete (`communicate.rs:61-78`) | Full schema-derived signal-frame rewrite per `/390` deferred; Communicate trait still in-crate not in signal-frame |
| 6 | Nexus mail keeper | 0.2 → 0.85 | **0.85** | NexusMailKeeper actor (`nexus.rs:161-186`); MailEntry with typed MailLifecycle (`nexus.rs:67-104`); NexusHooks push fire (`nexus.rs:135-149`); test #11 verifies Sent→Queued→Processing→Replied; test #12 verifies hooks fire synchronously with correct correlation id | InputNexus trait not yet driven directly (subagent kept hand-written `drive` + `handle_through_codec` to thread DatabaseMarker — this is the substrate gap that triggers iteration-3 schema-derived-signal-frame work per `/390`); promotion to shared `persona-mail` crate also iteration-3 |
| 7 | SEMA state handling | 0.3 → 0.85 | **0.85** | sema-engine `Engine` (`store.rs:128-138`); per-record-family `TableReference` (`store.rs:130-136`); EngineRecord on schema-emitted records (`store.rs:81-122`); CounterRow for durable counters (`store.rs:55-73`); test #13 proves restart-survival | Subscriptions surface unused; multi-op `commit` transaction unused (single-record assert/mutate only); both iteration-3 |
| 8 | Spirit runtime behavior | 0.9 | **0.9** | Single-NOTA-arg daemon binary unchanged; CLI thin client unchanged; build.rs assertion + signal-frame plumbing carried forward | Pattern continues |

**My audit aggregate: 6.7 / 8.0 (≈84%) — confirms subagent's claim.**

Component 4 (Rust emission) earned the 0.1 bump because schema-rust-next's parallel operator work landed Nexus mail emission this turn (the `9a98eedd` commit chain) — the subagent consumed it by updating Cargo.lock + flake.lock. Components 5/6/7 are the load-bearing lifts: each moved from <0.35 to ≥0.7 by wiring in the substrate component the brief mandated. Components 1/2/3/8 are unchanged because they were already at strong scores; further lift requires either substrate evolution (StructureHeader direct use, Asschema introspection) or scale demands not yet present.

## Iteration-3 pickup queue (rank-ordered)

Per Spirit record 973's "audit findings feed implementation" rule, each gap above derives iteration-3 work. Subagent listed 9 items in `/37/2 §"What's STILL bypassed or partial"`; orchestrator's ranking:

### Rank 0 — branch convergence (unblocks every other iteration-3 item)

**I-0. Merge `schema-deep-iteration-2` (this iteration) and `schema-deep` (system-operator's `/165` source-staging iteration) into a single iteration-3 base.** Both branches share `/35` baseline. Their changes are compatible in spirit (one rewires runtime; one adds a pipeline plane) and non-overlapping in file scope (the subagent's diff touches `nexus.rs` + `store.rs` + `communicate.rs` + Cargo + tests; system-operator's touches `source_stager.rs` + `dispatcher.rs` + tests). Per `skills/double-implementation-strategy.md`, operator-class amalgamation is the right lane. The merge produces an iteration-3 baseline that has BOTH the source-staging pipeline plane AND the Nexus/sema-engine/Communicate/DatabaseMarker depth.

### Rank 1 — substrate-direction work (unblocks the depth components further)

**I-1. Schema-derived signal-frame rewrite per `/390 §"Schema-derived signal-frame"`.** Lifts component 5 from 0.7 → ~0.9. Communicate trait promotes to signal-frame; encode/decode become schema-derived rather than macro-based. Substantial work; subagent declined to start scaffolding this iteration to keep scope bounded.

**I-2. InputNexus trait used directly via schema-rust-next extension.** Lifts component 6 from 0.85 → ~0.95. The hand-written `drive` + `handle_through_codec` in `nexus.rs` becomes a trait impl. Requires schema-rust-next to grow async-orchestration support in the emitted trait — design work per `/390`.

### Rank 2 — cross-component substrate extraction

**I-3. Extract NexusMailKeeper into `persona-mail` shared crate** per `/390 §"Mail state manager"`. Triggers when at least one more component (spirit-next per `/operator/219`, or future cloud per records 914-919) demands the same mail mechanism. Already-real cross-component pressure: `/operator/219` produced `NexusInput`/`NexusOutput`/`MailLedgerEvent` for spirit-next; the SHARED schema home decision (psyche decision #1 below) bundles cleanly with extraction.

**I-4. Shared schema home for cross-component mail/marker nouns** — psyche decision #1 below. Candidates: `schema/core.schema` in schema-next, new `persona-mail` crate, or extend signal-frame schema. Affects iteration 3 across `/37 iter 2` + `/165` + `/operator/219` all at once.

### Rank 3 — feature completeness (waits for substrate)

**I-5. Schema upgrade traits per record 950.** Triggers when the first schema diff arrives (current iteration is v1.0.0 baseline). Schema-next + schema-rust-next would need to grow diff detection + emission of `UpgradeFrom`/`AcceptPrevious` impls.

**I-6. Vectors in SemaResponse per Spirit 883.** `GenerationLedger(Vec<GenerationRecord>)` replaces one-record-per-response. Schema-next vector support is psyche-authorized; subagent didn't fork schema-next this iteration because the workaround held.

**I-7. owner-signal-lojix triad leg.** Full component triad per `skills/component-triad.md §"Two authority tiers"`. Lojix-next ships only the ordinary signal surface today. Iteration when operator-tier authority work earns its iteration.

### Rank 4 — operator-amalgamation work (after pilot promotes)

**I-8. Real `systemd-nspawn` boot in `nix flake check`.** Currently a sandbox marker (`nspawn-sandbox-activate`). `nix flake check`'s chroot lacks root + cgroups; real activation needs CriomOS-test-cluster-style remote-runner plumbing. Operator amalgamation work per `skills/double-implementation-strategy.md`; not designer-pilot territory.

**I-9. sema-engine subscriptions surface used; multi-op `commit` API used.** Both lift component 7 from 0.85 → ~0.95. Reactive observation streams unify with ObservationFan; multi-op transactions batch deploy pipeline writes into one per-phase commit. Iteration when ObservationFan's `Subscribe` mechanism merges with sema-engine's subscription system.

## Three-track parallel iteration — the convergence picture

At end of 2026-05-27, four iterations of the prototype-driven-development methodology (records 971-974) are in the workspace:

| Track | Lane | Branch | Slice | Score | Status |
|---|---|---|---|---|---|
| `/35` | system-designer (baseline) | `schema-deep` (lojix) | initial schema-deep pilot, 9 actors, 10 tests | 5.0/8.0 | shipped (`rnwxqrlzmrmm`) |
| `/165` | system-operator | `schema-deep` (lojix) on top of `/35` | source-staging plane (SourceStager actor, SourceRecord schema noun) | 5.1/8.0 | shipped (`qpkvvxxxwrqq` / `5145ae61`, pushed) |
| `/37 iter 2` | system-designer (this lane) | `schema-deep-iteration-2` (lojix) on top of `/35` (NEW branch to avoid `/165` collision) | Nexus mail keeper + sema-engine + Communicate + DatabaseMarker | 6.7/8.0 | shipped (`twvkkpypztsr` / `8804082fc50d`, pushed) |
| `/operator/219` | operator | spirit-next branch | parallel Nexus/SEMA/Mail iteration on the DIFFERENT prototype (spirit-next, not lojix) | similar substrate work, different prototype | shipped (in working tree this afternoon) |

Three orchestrator-level observations:

1. **Subagent's branch-split decision was sound.** The brief expected extension on `schema-deep`; subagent observed live race against system-operator's edits and routed to `schema-deep-iteration-2`. This preserves both iterations cleanly and defers the merge to amalgamation time. Without this routing, edits would have raced or overwritten.
2. **The merge is small.** Subagent's analysis: file scopes are non-overlapping (nexus.rs + store.rs + communicate.rs vs source_stager.rs + dispatcher.rs additions). The intellectual content compose: source staging adds a pipeline plane between Plan and Builder; Nexus rename + sema-engine + Communicate + DatabaseMarker rewires the runtime around the pipeline. Operator amalgamation is plausibly a single working day.
3. **`/operator/219` did the same substrate work on a different prototype.** This is exactly the cross-pollination signal that argues for `persona-mail` extraction (I-3 above). Two prototypes asking for the same primitive is the demand condition.

## Open psyche decisions (3 load-bearing)

Restating from `/37/1` + new ones surfaced by this iteration:

### Decision A — Shared schema home for cross-component mail/marker nouns

`DatabaseMarker`, `MailLifecycle`, `NexusInput`, `NexusOutput`, `MailLedgerEvent`, `Import`, `Export` appear in BOTH `/37 iter 2` (lojix) and `/operator/219` (spirit-next). Three candidate homes:

- (a) **`schema/core.schema` in schema-next** — substrate-side, every consumer imports.
- (b) **New `persona-mail` crate** per `/390 §"Mail state manager"` — substrate-side, mail-mechanism-focused.
- (c) **Extend signal-frame's schema** — wire-side, since these are signal-protocol-flavored.

Orchestrator recommendation: **(b) `persona-mail`** if + when more than two consumers want the same primitive; **(a) `schema/core.schema`** until then for minimum-friction. Either is better than per-component duplication.

### Decision B — `persona-mail` extraction NOW (iteration 3) or LATER

`/37/1` deferred extraction unless concrete demand arose. `/operator/219` constitutes that demand. Authorize iteration-3 extraction, OR defer one more iteration to validate against a third consumer (cloud per records 914-919).

### Decision C — Branch convergence ownership

`I-0` above. Two branches (`schema-deep` carrying `/165` + `schema-deep-iteration-2` carrying this work). Three options:

- (a) **Operator amalgamates per `skills/double-implementation-strategy.md`** — the canonical path; operator-lane work.
- (b) **System-designer convenes a `/39-three-track-convergence/` meta-report** mapping the merge before operator picks up.
- (c) **Subagent dispatch** — designer-class subagent on a new merge-attempt branch.

Orchestrator recommendation: **(a) operator amalgamation** is the right lane. Designer-class clarification (b) only if the merge turns out non-mechanical (psyche decision needed on a substantive content conflict, not a syntax conflict).

## Bottom line

`nix flake check` passes on commit `twvkkpypztsr`. 16/16 tests of the deliverable's witness family pass. Iteration 2 hit the target component-fullness lift (5.0/8.0 → 6.7/8.0 = +1.7). Subagent's branch-split decision avoided collision with system-operator's parallel iteration and is the right shape for double-implementation-strategy convergence. Three iterations of the schema-deep pilot now coexist (`/35` baseline + `/165` width + `/37 iter 2` depth); plus `/operator/219` on the parallel spirit-next prototype produces the same substrate primitives, arguing for shared-schema-home extraction in iteration 3.

The three load-bearing psyche decisions above (shared schema home + persona-mail extraction + branch convergence ownership) unblock iteration 3. The pilot is **ready for psyche review** and (when promoted) for **operator amalgamation per `skills/double-implementation-strategy.md`**.

## See also

- `0-frame-and-method.md` — orchestrator frame + subagent brief (this directory).
- `1-prototype-target-and-component-mapping.md` — per-component target mapping.
- `2-iteration-2-implementation.md` — subagent's implementation report.
- `~/wt/github.com/LiGoldragon/lojix/schema-deep-iteration-2/` — the iteration-2 worktree itself.
- `~/wt/github.com/LiGoldragon/lojix/schema-deep-iteration-2/INTENT.md` + `ARCHITECTURE.md` — per-repo manifestation per record 944.
- `/system-designer/35-schema-deep-new-logics/3-overview.md` — iteration-1 baseline.
- `/system-designer/36-criomos-reconciliation-audit.md` — earlier designer audit naming the SourceStager actor sketch.
- `/system-designer/38-source-staging-prototype-audit.md` — earlier designer audit of `/165` flagging the cross-arc convergence question.
- `/system-operator/165-lojix-source-staging-prototype-and-full-component-critique.md` — parallel iteration on the same `/35` baseline (now on the `schema-deep` branch).
- `/operator/219-schema-full-stack-prototype-completeness-audit-2026-05-27.md` — parallel iteration on spirit-next with the same Nexus/SEMA/Mail substrate work.
- `/designer/392-vision-schema-driven-stack-canonical-2026-05-27.md` — workspace vision; 8-component fullness criterion source.
- `/designer/390-wire-runtime-canonical-direction.md` — Communicate trait + mail state manager + DatabaseMarker design source; iteration-3 substrate-direction work.
- `skills/double-implementation-strategy.md` — designer-pilot-vs-operator-amalgamation framing; the convergence pattern this iteration's branch split sets up.
- Spirit records 971-974 — prototype-driven-development methodology and the use-all-components-fully constraint; 980 (this lane's redundant capture).
- Spirit records 963-970 — Signal protocol naming + Nexus as mail keeper + Nexus covers IO/UI; the terminology refresh this iteration realised in code.
- Spirit records 944 + 920 — continuous per-repo manifestation; subagent lane inheritance.
