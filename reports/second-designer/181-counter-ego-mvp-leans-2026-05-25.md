*Kind: MVP Proposal + Leans · Topic: counter-ego MVP slices matching intent letter-by-letter · Date: 2026-05-25 · Lane: second-designer*

# 181 — Counter-ego MVP leans — five proposals matching letter-of-intent

## §1 Frame

Per psyche directive 2026-05-25 (to designer, shared with me as instructional + parallel): "get started on where you think you would, how you would lean on solving all these to get a minimal viable product of what I've described as much to the letter of my intent as possible." Captured as intent 585 (commit + push at end of every pass) + 586 (lean on intent, propose MVP, surface only the truly-uncertain remainder).

This report is the counter-ego mirror of designer's parallel work: take the open items from my recent audits (/178, /179, /180) + the broader /176 §13 deviation table, and PROPOSE the MVP for each — leaning hard on captured intent rather than asking more questions.

Five MVP slices proposed, in priority order. Each: what + why + intent leans + concrete file/sequence + open-question-if-genuinely-unanswerable.

## §2 MVP slice 1 — `primary-602y` rebuild persona-spirit v0.1.0.1 retrofit (P0)

**What**: rebuild the deployed `persona-spirit` v0.1.0.1 maintenance build against current post-ShortHeader `signal-frame`. Bundle with the Spirit Mirror phase-ordering alignment per /178 §3 + /179 §4.

**Why** (intent leans): per /179 §3, deployed v0.1.0.1 was built BEFORE ShortHeader landed; cross-version handover with v0.1.1 cannot work because daemons can't parse each other's frames. Per intent 525 (until constraints pass full sandbox test), production cutover is blocked until this lands. Per intent 586 (propose MVP from inferable intent), the backport pattern already exists at `primary-wdl6` (operator/178); apply it to v0.1.0.1.

**Concrete sequence**:
1. Worktree `~/wt/github.com/LiGoldragon/persona-spirit/v0-1-0-1-shortheader-backport/` from main HEAD on the v0.1.0 maintenance branch (or fresh branch off v0.1.0.1 tag)
2. Pull `signal-frame` to current main (gets ShortHeader emission + consumption)
3. Re-apply v0.1.0.1's protocol-aware retrofit (upgrade socket + AskHandoverMarker/ReadyToHandover/HandoverCompleted handlers) on top
4. Bundle: align Mirror handler with /186 orchestrate pattern (Mirror in marker-to-readiness window, not post-completion). Spirit's Mirror payload remains empty per /175 §9, so the wiring change is the entire fix
5. Re-build, re-tag as `v0.1.0.2`
6. Update CriomOS-home `persona-spirit-v0-1-0` flake input to v0.1.0.2 tag; bump `versioned-deployment` check
7. Activate via `lojix-cli '(HomeOnly goldragon ouranos li ... Activate ...)'`
8. Verify: both daemons running; cross-version handover ceremony succeeds in nspawn pair test

**Open**: none. Pattern is fully inferable from operator/178 (primary-wdl6) + /186 (orchestrate Mirror placement) + /178 §3 (my prior recommendation). Operator-actionable; no design question remaining.

## §3 MVP slice 2 — Schema-derived `VersionProjection` (closes largest /176 §13 deviation)

**What**: extend the BuiltinSchemaMacro engine (currently 5 variants per operator/175.4) with an `UpgradeMacro` variant. Consumes pairs of (previous AssembledSchema, current AssembledSchema) + emits Rust `VersionProjection` impls per the 7 projection kinds (Identity / Standard / Annotated / Added / Renamed / Dropped / Untranslatable).

**Why** (intent leans): per intent 506 (data-carrying macro variants with input structs) + 569 (iterative-to-fixed-point macro application) + 571 (newtype emits Rust single-tuple struct) + nota-designer/8 §"Reusable Lowering Shape" + designer/329's `SchemaMacro` trait + /176 §4.2 schema-to-upgrade-plan derivation algorithm. The hand-written `From<v010::Certainty> for Magnitude` at `signal-persona-spirit/src/migration.rs` is the deviation; macro emission is the destination.

**Concrete sequence**:
1. Worktree `~/wt/github.com/LiGoldragon/schema/feature-upgrade-macro-variant/` from main HEAD
2. Add `UpgradeRuleInput { previous_schema: AssembledSchema, current_schema: AssembledSchema, annotations: Vec<UpgradeAnnotation> }` to `schema/src/engine.rs` (per nota-designer/8 §"Reusable Lowering Shape" + designer's pending `UpgradeRule` macro variant per /334-v2 §3.4)
3. Add `UpgradeMacro` BuiltinSchemaMacro variant that consumes `UpgradeRuleInput` and produces a `LoweredUpgradePlan` (Vec of typed projection-emit instructions)
4. Hand-write the projection-emit code generator (this is the part the brilliant macro library is supposed to do; for MVP, emit Rust source as `String` that the proc_macro pastes inline)
5. Wire `signal_channel!([schema])` to consume the upgrade-rule output when the schema's `(Upgrade VersionRef [annotations])` feature variant is present (currently the feature variant has typed shape per /176 §4.1 but no emit-side consumer)
6. Test: assemble Spirit v0.1.0 + v0.1.1 schemas; run UpgradeMacro; produce equivalent `From` impls to current `signal-persona-spirit/src/migration.rs`; assert byte-equivalence with the existing hand-written code
7. After equivalence proven, DELETE `signal-persona-spirit/src/migration.rs` hand-written impls; rely entirely on macro emission

**Open**: how should the macro emit the `historical` module (the private rkyv reproduction of v0.1.0 types)? Two options: (a) macro emits inline within the migration crate; (b) macro emits a separate `historical_v0_1_0` module. **Lean: (a)** — fewer files; co-located with the projection. Confirm if you have a preference.

## §4 MVP slice 3 — Engine-on-Route landing (rebase /172 mockup B)

**What**: rebase my `/172` mockup B (`feature/engine-routing-and-upgrade-coverage` at commit `52f5364692fa`) onto current schema main + push as integration-ready. Adds `engine: Option<Engine>` to `Route` struct; `routes_by_engine(Engine) -> impl Iterator<Item = &Route>` helper.

**Why** (intent leans): per /171 §4.2 (engine annotations stored but invisible on AssembledSchema surface) + /176 §13 row "Engine annotations don't reach AssembledSchema" + intent 506. The mockup test at `tests/document.rs` already proves the wiring works; it just needs to land on current main.

**Concrete sequence**:
1. Relocate worktree from `/tmp/mockup-b-engine-routing` to `~/wt/github.com/LiGoldragon/schema/feature-engine-routing-and-upgrade-coverage/` per intent 540
2. `jj rebase --branch feature/engine-routing-and-upgrade-coverage -d main`
3. Resolve any conflicts (main has advanced via "lower upgrade rules through builtin macro variant" + "add builtin lowering engine" — likely affects `Schema::lower_header` signature where mockup B threaded engine through)
4. Run all checks: `cargo test`, `cargo fmt -- --check`, `cargo clippy --all-targets -- -D warnings`, `nix flake check --option max-jobs 0`
5. Push to remote feature branch
6. Update bead `primary-gqj6` note: "REBASED on current main; ready for operator integration as small PR on top of macro-variant landing"

**Open**: none. Mockup is tested; rebase is mechanical.

## §5 MVP slice 4 — Component name + UID landing (rebase /172 mockup A)

**What**: rebase my `/172` mockup A (`feature/component-uid-and-layout` at commit `b5c4f373`) onto current schema main + push as integration-ready. Adds `Schema::for_component(name, ...)` constructor + `AssembledSchema::component(&self) -> &Name` + `uid_for(name) -> Uid` + Layout-on-AssembledSchema fix (resolves Magnitude-in-box bug).

**Why** (intent leans): per /171 §4.1 + §4.3 (component name + UID + Layout-on-AssembledSchema gaps) + /176 §13 + intent 469 (`spirit::namespace::Topic` UID form) + intent 526 confirmed lean §3.4 (imported types render UIDs under source schema's component, not importing schema's). Foundation for downstream slices (UpgradeMacro from §3 needs UIDs; supervisor cutover from future slice needs UIDs).

**Concrete sequence**:
1. Relocate worktree from `/tmp/mockup-a-component-uid` to `~/wt/github.com/LiGoldragon/schema/feature-component-uid-and-layout/` per intent 540
2. **Adjust mockup before rebase**: per intent 526 lean confirmed by psyche, change UID resolution to chase IMPORTED types to their SOURCE schema's component, not the importing schema. Mockup currently picks importing-schema; flip to source-schema before rebase.
3. `jj rebase --branch feature/component-uid-and-layout -d main`
4. Resolve conflicts (main has advanced; Schema struct may have grown additional fields)
5. Run checks
6. Push to remote feature branch
7. Update bead `primary-5cfq` note: "REBASED on current main + UID source-schema lean applied; ready for operator integration"

**Open**: none on the rebase mechanics. The source-schema-UID lean is already confirmed; just need to apply.

## §6 MVP slice 5 — Storage feature variant (lift /179 sketch)

**What**: implement the `(Storage [...])` feature variant per second-operator/179 §"Surfaces" sketch — the long-overdue "Storage" entry in the deviation table.

**Why** (intent leans): per /176 §13 row "Storage schema descriptors not yet schema-derived" + second-operator/179's anticipated shape `(Storage [(LocalName StoredType)])` + designer/333 §13 row "(Storage ...) feature pending". The shape is already proposed; the work is to implement the macro emission of `TableDescriptor<T>` per declared storage entry.

**Concrete sequence**:
1. Worktree `~/wt/github.com/LiGoldragon/schema/feature-storage-feature-variant/` from main HEAD
2. Add `Feature::Storage(StorageFeature)` to `schema/src/feature.rs` (alongside Reply / Event / Observable / Upgrade)
3. `StorageFeature { tables: Vec<StorageTable> }` where `StorageTable { name: Name, stored_type: Name }` per /179 sketch
4. Extend BuiltinSchemaMacro engine to lower `(Storage [...])` per /329's `SchemaMacro` trait pattern
5. Emit `TableName` constants + `TableDescriptor<T>::new` calls in `signal_channel!([schema])` output per /176 §11 (current spirit `tests/short_header.rs` pattern)
6. Test: add `(Storage [(Records StoredRecord)])` to a small test schema; assert emitted code contains the `TableName::new("Records")` + `TableDescriptor::<StoredRecord>::new` shape
7. After landing, add `(Storage [...])` to `spirit.schema` per the existing `signal-persona-spirit/src/store.rs` storage shape; verify emitted code matches hand-written

**Open**: should `StorageTable.stored_type` allow only declared local types, or also imported types? **Lean: local only for MVP** — mirror how Reply/Event work (named types must resolve via namespace). Confirm if you want broader.

## §7 What's NOT in this MVP wave

Items I'm deferring because they're EITHER not inferable from current intent OR depend on slices above:

- **Cross-component cutover orchestration via typed persona-supervisor**: depends on `primary-a5hu` (persona engine epic); not bead-actionable until that lands
- **schema_short_hash in ShortHeader bytes 2-7**: design ideal per /175 §5.4; needs psyche call on hash function + bit allocation; not letter-of-intent for MVP
- **Owner signal schema coverage parity**: needs per-component work; sequence by component
- **Mirror payload extension for orchestrate dynamic_roles** (intent §3.4 lean): small slice but waiting on /186's open question #2 (contract version marker shape) resolution
- **nspawn orchestrate end-to-end test**: my sub-agent A already exercises the ceremony in-process; nspawn version is stretch per /176 §14 + the in-process test already gives the regression net
- **Divergence + Recovery executor full implementation**: needs persona-daemon supervisor; defer with the supervisor

## §8 Lean summary by intent reference

For each MVP slice, the intent corpus that justifies the lean (proving these aren't questions; they're inferable proposals):

| Slice | Load-bearing intent records |
|---|---|
| §2 primary-602y bundle | 525 (full sandbox test) + 540 (worktree relocation) + /178 §3 + /179 §3 |
| §3 UpgradeMacro | 506 (data-carrying macro variants) + 569 (iterative-to-fixed-point) + 491 (upgrade knowledge on next version) + nota-designer/8 §"Reusable Lowering Shape" + /334-v2 §3.4 |
| §4 Engine-on-Route | 506 + /171 §4.2 + /176 §13 + /172 §3.2 lean confirmed |
| §5 Component-name+UID | 469 (`spirit::namespace::Topic` UID form) + 471 (filename-driven root naming) + 526 source-schema-UID lean + /171 §4.1 + §4.3 |
| §6 Storage feature variant | second-operator/179 §"Surfaces" + /176 §13 + designer/333 §13 |

Five proposals, zero questions that block any of them, four genuinely-open follow-ups (the §3 historical module location + §6 imported-vs-local stored types + a couple of psyche-confirmable defaults that don't gate the work).

## §9 Sequencing recommendation

If operator (or a sub-agent) takes one slice at a time:

1. **§2 primary-602y bundle FIRST** — unblocks production cutover; bundles two related fixes (ShortHeader backport + Mirror phase alignment).
2. **§4 Engine-on-Route + §5 Component-name+UID in parallel** — both are rebase-only of already-tested mockups; can be picked up by anyone (operator or a small mockup-rebase sub-agent).
3. **§3 UpgradeMacro AFTER §5** — needs UIDs to address types canonically; otherwise emits ambiguous `From` impls.
4. **§6 Storage feature variant ANYTIME** — independent of others; lift the shape, land it.

Total estimated operator effort: ~3-5 sessions across the 5 slices, depending on how aggressively the mockup rebases (§4, §5) are bundled vs separated.

## §10 Open psyche questions (the truly-uncertain remainder)

Only three. Letter-of-intent leans applied to everything else.

1. **§3 historical module location** — inline within migration crate (lean) or separate `historical_v0_1_0` module? Lean (a). Confirm if you have a preference.

2. **§6 Storage table type scope** — local types only (lean) or also imported types? Lean: local for MVP. Confirm.

3. **§7 Mirror payload extension for orchestrate dynamic_roles** — blocked on /186 question #2 (contract version marker = semantic byte vs schema-derived hash). Need your call on that to unblock the dynamic_roles slice. Recommend the answer in the same response.

That's the entire surface that's not inferable from captured intent. Five MVPs proposed; three small confirmations needed.

## §11 References

- `reports/second-designer/178-audit-second-operator-186-orchestrate-upgrade-socket-2026-05-25.md` — source of §2 bundle lean + §4 Engine-on-Route relevance
- `reports/second-designer/179-audit-operator-180-schema-field-name-and-upgrade-context-2026-05-25.md` — source of §2 P0 primary-602y + Mirror phase-ordering divergence
- `reports/second-designer/180-audit-second-operator-179-design-schema-language-v4-2026-05-25.md` — source of §6 Storage feature variant lift
- `reports/second-designer/176-upgrade-mechanism-soup-to-nuts-2026-05-25.md` §13 — the deviation table being closed
- `reports/second-designer/172-design-mockup-dispatch/5-overview.md` — mockups A + B + D referenced for rebase
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` §3.4 — UpgradeRule variant proposal
- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` §"Reusable Lowering Shape" — named-input-struct pattern
- `reports/operator/178-primary-wdl6-spirit-v0-1-0-protocol-build-2026-05-25.md` — backport pattern §2 follows
- `reports/operator/180-schema-field-name-and-upgrade-context-2026-05-25/3-overview.md` — primary-602y named source
- `reports/second-operator/179-design-schema-language-v4/4-overview.md` — §6 Storage shape sketch source
- Intent records 469 (UID form), 471 (filename-driven root naming), 491 (upgrade on next version), 506 (data-carrying macro variants), 525 (full sandbox test), 526 (lean confirmations), 540 (worktree relocation), 569 (iterative-to-fixed-point), 585 (commit + push end of pass), 586 (lean on intent propose MVP)
