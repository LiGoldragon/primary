# NOTA Strict-Positional Fix — Phase 3 Independent Audit

## Task and scope

Independent, read-only audit of the completed NOTA strict-positional fix. The
six claims in the Phase-3 brief are the claim set (no separate implementer
report exists in the lane directory). Verdict per claim is grounded in source
(`file:line`) plus re-run durable checks — not in the fix commit messages.

No files under audit were edited. Only this audit artifact was written.

## Repos and fix commits audited

| repo | branch | HEAD | fix commit |
|---|---|---|---|
| schema-next | main | 9af2c546 | 9af2c546 "reject Optional as an enum-variant payload" |
| schema-rust-next | main | 6218fb64 | 6218fb64 "drop the optional-variant bespoke NOTA codec" |
| signal-spirit | main | 93a0a70d | 93a0a70d "strict-positional domain taxonomy" |
| signal-mentci | criome-authorization-push | 33ff1d1e | 33ff1d1e "strict-positional NotificationProjection payload" |
| mentci | criome-authorization-push | 75b5d43d | 75b5d43d "adopt strict-positional NotificationProjection payload" |
| mentci-lib | criome-authorization-push | 8c854187 | 8c854187 "adopt strict-positional signal-mentci NotificationProjection" |
| spirit | criome-authorization-push | 202a6e24 | (untouched by this lane) |

All six named HEADs match the brief.

## Per-claim verdicts

### Claim 1 — Guard is correct and scoped: CONFIRMED

- Error variant added: `SchemaError::OptionalVariantPayload { enum_name, variant_name }`
  at `schema-next/src/engine.rs:78-84`.
- Check: `schema-next/src/schema.rs:840-845` inside `verify_enum_arities` —
  fires only when `variant.payload` is `Some(TypeReference::Optional(_))`.
- Scoped to variant payloads only. Named brace-record fields go through
  `verify_declaration_arities` → `verify_reference_arities`
  (`schema.rs:824-835,852-883`), which recurses into `Optional(inner)` and never
  rejects `Optional` itself. Newtypes go through the same non-rejecting path.
  The ~50 legit `struct X(Option<T>)` newtypes and brace-field optionals are
  unaffected.
- Unbypassable: single-path lowering. Every document/source entry point
  (`lower_source`, `lower_document*`) reparses into a `SchemaSource` and
  delegates to `lower_schema_source_with_resolver` → `source.to_schema` →
  `source.rs:190 .and_then(Schema::arities_verified)`. The doc contract at
  `engine.rs:436` ("exactly one set of lowering semantics") is the witness.
- The generator reaches the guard on the real generation path:
  `schema-rust-next/src/build.rs:652 engine.lower_schema_source_with_resolver(...)`.
  This is why both affected schemas had to be migrated — a residual Optional
  payload would fail generation.
- Test `optional_enum_variant_payload_is_rejected`
  (`schema-next/tests/lowering.rs:215-233`) lowers a real source and asserts the
  exact typed error. Genuinely exercises rejection. RAN: passes.
- Scoping proven green: `schema-next/tests/collections.rs` (brace-field Optional,
  newtype Optional, nested `Map/Vector/Optional`) and `typeref_structural_macro.rs`
  all pass under the guard.

### Claim 2 — No bespoke codec remains: CONFIRMED

- `git show 6218fb64 --stat`: `src/lib.rs` -518/+47 (net -471); the
  `RustEnumTokens` bespoke block deleted (`@@ -4818,380 +4794,6 @@`).
- Recursive grep across all `/git/github.com/LiGoldragon/**/src/*.rs`:
  `RustOptionalEnumNotaTokens`, `has_optional_payload_variant`,
  `NotaBodyDecode`/`NotaBodyEncode`, `optional_unit_arms`, `terminal_payload`,
  `is_optional_payload` — ZERO hits (all gone).
- Enum derive is now unconditional: `derive_attributes(includes_copy,
  includes_ordering)` (`lib.rs:1940`) no longer takes an `includes_nota` gate; the
  nota derive is driven solely by `NotaSurface::includes_nota_in_derive()`
  (`lib.rs:1039-1041,1947`). `RustEnumTokens::to_tokens` (`lib.rs:4790-4796`) emits
  a plain `#(#attributes)* enum … { … }` with no conditional branch.
- Regenerated contracts carry zero hand-rolled codecs: `grep 'impl nota::Nota'`
  in `signal-spirit/src/schema/domain.rs` and `signal-mentci/src/schema/lib.rs`
  → 0. Full-set recursive sweep for `impl nota::NotaBody(Decode|Encode)` → 0.
- `emits_nota` remains live (5 callers); not dead code.

### Claim 3 — signal-spirit strict behavior: CONFIRMED

- Schema source (`schema/domain.schema`): all 12 optional payloads →
  required (`(Hardware HardwareLeaf)`, `(Programming ProgrammingLeaf)`, …); each
  value-leaf enum gains `All` as first member; `Theory` stays bare; Equivalence
  footer migrated `(Technology Software Data)` → `(Technology Software Data All)`.
- Generated `src/schema/domain.rs`: `Software` (`:776-789`) has 12 required-payload
  variants + bare `Theory`; each leaf enum leads with `All`
  (`ProgrammingLeaf:806`, `DataLeaf:875`, …); zero `Option<` in the whole file.
- 6 hand-written constructors fixed (`src/lib.rs`): notably
  `Software::Programming(None)` → `Software::Programming(ProgrammingLeaf::All)`
  (correct None→All whole-category semantics); the other five drop the `Some(...)`.
- Blessing tests genuinely ASSERT the strict invariant, not merely compile:
  - `tests/generated_contract.rs` `terminal_value_domain_tags_round_trip_through_nota`:
    asserts `"(Technology (Software Data))".parse_domain().is_err()` (bare rejected),
    `(Data All)` decodes to `DataLeaf::All`, and `to_nota()` round-trips.
  - `tests/instance_schema.rs`
    `bare_leaf_variant_without_payload_is_rejected_and_all_traces_the_leaf`:
    asserts `Domain::from_nota_block_traced` of bare `Programming` `.is_err()`,
    then traces `(Programming All)` as required `ProgrammingLeaf` with
    `InstanceSchemaBody::EnumPayload(None)` (no Optional node).
  - `pure_terminal_theory_domain_round_trips_through_nota` covers bare `Theory`.
- RAN `cargo test --features nota-text`: all pass (incl. the assertions above).

### Claim 4 — mentci family: CONFIRMED

- `signal-mentci/schema/lib.schema`: adds `NotificationSlice [Empty (Present
  NotificationText)]`; `(NotificationProjection (Optional NotificationText))` →
  `(NotificationProjection NotificationSlice)`. Comment explicitly states no Mind
  restructure. No Mind-taxonomy change present in the diff.
- Daemon adapter is a method on the data-bearing type:
  `NotificationSlice::from_current(Option<NotificationText>) -> Self`
  (`signal-mentci/src/lib.rs:144-156`) — daemon keeps its own `Option`, wire form
  is the required-payload slice. Correct storage/wire split.
- Consumers compile and route through it: `mentci/src/state.rs:365-368` maps
  `NotificationSlice::from_current(self.notification.clone())`; `mentci-lib`
  needs only a pin bump (wildcard match). RAN `cargo test` on both: pass. RAN
  `cargo test --features nota-text` on signal-mentci: pass.

### Claim 5 — Scope-enum #1 (second asymmetry cannot arise): CONFIRMED

- Zero `Option<` in generated `signal-spirit/src/schema/domain.rs`.
- Root scope enum `DomainScope` (`:1047-1072`) carries NO `All`. Every non-root
  scope enum carries exactly one `All` (e.g. `TechnologyScope:1080`,
  `SoftwareScope:1091`, `DataLeafScope`, …). The source leaf `All` member is
  filtered out and represented by the auto-injected `Self::All`
  (`schema-rust-next` `ScopeEnumVariantModel::is_universal` + the
  `self.model.root || !variant.is_universal()` filter in `ScopeEnumTokens`,
  `ScopeOperationImplTokens`); no duplicate `All` (would be a compile error, and
  the crate compiles).
- Uniform derive: all scope enums use the same
  `#[cfg_attr(feature="nota-text", derive(nota::NotaDecode, NotaDecodeTraced,
  NotaEncode))]` (`scope_enum_type_attributes` → `derive_attributes(false,false)`).
- The flagged second asymmetry (scope enum canonical `Some/None` vs source
  collapsed) genuinely cannot arise: `Optional` is now banned everywhere it could
  appear as a payload, so no scope enum can carry an Optional payload.
- RAN: `schema-rust-next` `emits_terminal_value_domains_as_scope_all` and
  `emits_domain_scope_equivalence_expansion_from_relations` pass; signal-spirit
  `terminal_value_domains_convert_to_scope_all` passes.

### Claim 6 — Storage-break analysis: CONFIRMED, the blocker is REAL (not over-cautious)

Independent assessment agrees the blocker is real, and on stronger grounds than
stated.

- spirit is UNTOUCHED and still pins the OLD signal-spirit:
  `spirit/Cargo.lock:1497 …signal-spirit.git?branch=main#5d0905a7…`. spirit's
  latest commit (`202a6e24`, signal-router lock) is unrelated to this lane.
- spirit persists via rkyv: `spirit/src/store/mod.rs:121,442`
  (`rkyv::from_bytes`/`to_bytes` of `VersionedCommitLogEntry`), storing `Entry`
  (which holds `Domains` = `Vec<Domain>`). Store is at `SPIRIT_SCHEMA_VERSION =
  SchemaVersion::new(10)` (`store/mod.rs:75`), with an existing versioned
  migration framework (`production_migration.rs` V7–V10).
- The new contract breaks the rkyv layout of the persisted `Domain` on TWO axes:
  1. Variant payload type `Option<Leaf>` → `Leaf`: `ArchivedOption<ArchivedLeaf>`
     vs bare `ArchivedLeaf` differ in size/layout, shifting field offsets.
  2. Each leaf enum prepends `All` as discriminant 0, shifting ALL existing leaf
     discriminants by +1 (e.g. `DataLeaf::SchemaEvolution` 4 → 5). This is a
     silent misread of live bytes, not merely a hard error — worse than the
     implementer's "fail deserialization" framing.
- Per `rust-storage-and-wire` ("changing enum discriminants … is a coordinated
  storage-schema change"), bumping spirit's pin requires a v10→v11 migration +
  redeploy. Stopping is justified and correctly gated (Design.md psyche-gated
  blocker). Not over-cautious.

## Findings (defects) by severity

### Medium — signal-spirit `nix flake check` fails on `fmt` (INTRODUCED by the fix)

- `signal-spirit/tests/generated_contract.rs:455` (hand-edited in fix 93a0a70)
  is not rustfmt-clean: the single-line
  `…Software::Data(DataLeaf::SchemaEvolution)…` must wrap. `cargo fmt --check`
  reports the diff; `nix flake check` fails on `checks.x86_64-linux.fmt`. All
  other signal-spirit checks (build, test with blessing assertions) pass.
- Risk: the repo's required flake gate is red; the work does not land green.
- Correction: run `cargo fmt` on signal-spirit and recommit the generated-test edit.

### Low — signal-mentci and mentci committed source not rustfmt-clean (INTRODUCED)

- `signal-mentci/tests/interface_readers.rs:2` and `mentci/src/state.rs:10,363`
  (both hand-edited in the fix) fail `cargo fmt --check`. These two repos have no
  `flake.nix`, so there is no per-repo fmt gate to trip, but the committed source
  is non-canonical and would fail any workspace-level fmt gate.
- Correction: `cargo fmt` on both, recommit.

## Residual risks and pre-existing (NOT caused by this fix)

- schema-next `nix flake check` fails on `clippy` (`src/schema.rs:2277`,
  `.ok_or_else` → `.ok_or`; symbol last touched by `6a12bcc`, not the guard
  commit). Pre-existing; the guard code was not the cause.
- schema-rust-next `nix flake check` fails on `no-production-free-functions`
  (`src/bin/schema-rust.rs:19 fn main`; the guard grep `flake.nix:161` does not
  exempt `main`, though workspace Rust discipline does) and `doc`
  (`EmittedRustSurface` intra-doc link to private `Self::for_schema`). Both files
  untouched by fix 6218fb64; pre-existing. The NOTA-relevant checks
  (`generated-no-legacy-helper-surface`, `generated-nota-boundary`, `test`,
  `generated-no-free-functions`) all PASS.
- mentci-lib fmt diffs (`src/observation.rs:16`, `tests/model.rs:315`) are on
  files NOT touched by fix 8c854187 (Cargo.lock-only). Pre-existing; mentci-lib
  `nix flake check` reports "all checks passed" (0 gated checks).
- These pre-existing reds mean schema-next and schema-rust-next full flakes were
  already red before this lane; worth a separate tracked fix, out of this scope.

## Checks run (exact results)

| repo | check | result |
|---|---|---|
| schema-next | `cargo test` (all binaries) | PASS (0 fail) incl. `optional_enum_variant_payload_is_rejected`, collections, typeref |
| schema-next | `nix flake check --keep-going` | FAIL: `clippy` (pre-existing, schema.rs:2277). Others build clean |
| schema-rust-next | `cargo test` (all) | PASS incl. `emits_terminal_value_domains_as_scope_all`, equivalence, `rust_emission_is_stable…round_trip` |
| schema-rust-next | `nix flake check --keep-going` | FAIL: `no-production-free-functions`, `doc` (both pre-existing). NOTA guards + `test` PASS |
| signal-spirit | `cargo test --features nota-text` | PASS (blessing tests assert bare-rejection + round trip) |
| signal-spirit | `nix flake check --keep-going` | FAIL: `fmt` (INTRODUCED). All other checks PASS |
| signal-mentci | `cargo test --features nota-text` | PASS. (no flake.nix; `cargo fmt --check` fails — introduced) |
| mentci | `cargo test` | PASS. (no flake.nix; `cargo fmt --check` fails — introduced) |
| mentci-lib | `cargo test` | PASS |
| mentci-lib | `nix flake check --keep-going` | PASS ("all checks passed", 0 gated checks) |

Toolchain: `cargo 1.96.0`, `nix 2.34.6`, remote builder prometheus.

## Overall verdict

- All 6 claims CONFIRMED from source and re-run checks.
- The forbidden pattern (Optional variant payload + bespoke per-enum codec) is
  genuinely and completely eliminated: an unbypassable single-path lowering guard
  rejects it, the generator emits zero bespoke codecs, no hand-rolled NOTA-body
  codec survives anywhere, both affected crates are migrated to required
  payloads, and the strict invariant (bare-atom rejection) is asserted by
  behavior tests that all pass.
- "To green" is qualified: the fix INTRODUCED a `fmt` gate failure in
  signal-spirit (`nix flake check` red) and left non-rustfmt-clean committed
  source in signal-mentci and mentci. The implementer verified with `cargo test`
  (which ignores formatting) but did not run `cargo fmt`/`nix flake check`. Behavior
  is green; the full flake gate is not.
- The spirit storage-break blocker is REAL and correctly gated; do not bump
  spirit's signal-spirit pin without a v10→v11 rkyv store migration + redeploy.

## Provisional status

Audit findings are provisional recommendations until the psyche or psyche-owned
guidance accepts them. The `fmt` corrections and the pre-existing clippy/doc/
free-function reds are recommendations, not accepted doctrine.
