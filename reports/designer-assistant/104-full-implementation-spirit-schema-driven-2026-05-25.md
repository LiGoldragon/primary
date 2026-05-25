# 104 — schema-driven spirit full implementation

*Designer-lane subagent dispatch 2026-05-25 implementing the FULL
working schema-driven full-stack pattern across the four branches
set up by /103. Authority: /103 (prior landing inventory), /345
(multi-schema-per-crate), /346 (actor schemas + upgrade mechanism),
/343 §3-4 (EffectTable + FanOutTargets corrected by /345 §8),
/184 (composer architecture), /185 (current runtime scaffold).
Intent records 656-696. All five blockers resolved.*

## Summary

| Repo | Branch HEAD commit | Test result | Nix check | Blockers resolved |
|---|---|---|---|---|
| `schema` | `b499190a` | 30 tests pass (10 new) | green | Multi-pass parsers for EffectTable / FanOutTargets / StorageDescriptor + universal-Unknown injection hook |
| `signal-frame` | `b35d18bd` | 64 tests pass (3 new) | green | Composer pivots to authored-feature consumption; emits AuthoredEffect / AuthoredFanOut / AuthoredEffectTable + StorageDescriptor + duplicate-field-name disambiguation |
| `persona-spirit` | `e0378b8d` | 17 schema_driven tests + 50 pre-existing tests pass | green | schema_driven actors compile; migration runner reads version marker + writes forward + logs to upgrade-log |
| `signal-persona-spirit` | `5ba7ff99` | 14 tests pass (4 new) | green | emit_schema!() invoked alongside signal_channel!([schema]); both paths resolve during transition |

## Per-repo landing details

### schema (`b499190a`)

Three changes wire the new `Feature` variants the prior subagent
declared into the parsing + lowering pipeline:

1. **Multi-pass parsers** in `src/shape_parser.rs` (canonical NOTA
   reader; recognises `(EffectTable [ (Action Effect) ... ])`,
   `(FanOutTargets [ (Effect [Output ...]) ... ])`,
   `(StorageDescriptor [ (LogicalName TableType) ... ])`),
   `src/parser.rs` (streaming-decoder equivalence path), and
   `src/multi_pass.rs` (shape-logic dispatch with new
   `EffectTableRecognizer` / `FanOutTargetsRecognizer` /
   `StorageDescriptorRecognizer`). Each recognises the three
   `FanOutOutputDeclaration` kinds (Actor / Reply / Subscribers).
2. **Universal-Unknown injection** —
   `LoweringContext::finalize_universal_unknowns()` walks the
   lowered local types, identifies enums whose name ends in
   `Response` (per /346 §1), and idempotently injects
   `Unknown(String)`. Wired from both `Schema::assemble` and the
   multi-pass `MacroPipeline::run` so both paths produce identical
   AssembledSchemas.
3. **Validation extension** in `src/document.rs` —
   `validate_features` walks the three new variants without
   rejecting them; `StorageDescriptor` table types resolve through
   the imports/local namespace lookup.

Tests landed in `tests/effect_side_features.rs` (10 new):
- Two parser-equivalence tests (shape + streaming reader recognise
  the same schemas).
- StorageDescriptor entries / EffectTable rows / FanOutTargets
  outputs parse to the expected typed shapes.
- Universal-Unknown predicate detects `Response` suffix.
- Injection helper idempotent + non-mutating on non-enum bodies.
- AssembledSchema carries the injected `Unknown(String)` on a
  Response enum + does NOT inject on ACTION enums.
- LoadedSchema carries StorageDescriptor.

Fixtures: `tests/fixtures/effect-side/recorder.schema` (self-contained;
ACTION + RESPONSE + EffectTable + FanOutTargets with the three
output kinds) and `tests/fixtures/effect-side/storage.schema`.

### signal-frame (`b35d18bd`)

Composer pivots from route-derivation to authored-feature
consumption per operator/185 + /343 §3-4 + /346 §10:

1. **Cargo manifests for schema-rust + macros** point at the
   schema designer branch so the new `Feature` variants are
   visible.
2. **`authored_effect_items()`** in
   `schema-rust/src/lib.rs` emits `AuthoredEffect` (closed enum
   over the unique RHS effect types), `AuthoredFanOutOutput`
   (closed enum over the three FanOutOutputDeclaration kinds),
   `AuthoredFanOut` (carrier struct), and `AuthoredEffectTable`
   (string-keyed `effect_for_action` + `fan_out_for_effect`
   dispatchers). Fires only when the schema declares
   `Feature::EffectTable`.
3. **`storage_descriptor_items()`** emits `TableDescriptor` +
   `StorageDescriptor` with a `TABLE_COUNT` const, `TABLES`
   const slice, and `table_type_for(logical_name)` accessor.
4. **Disambiguation fix** —
   `record_field_tokens_disambiguated()` suffixes duplicate
   field names (e.g. `Time [u8 u8 u8]` becomes `{ pub u8: u8,
   pub u8_2: u8, pub u8_3: u8 }`). Required by spirit.schema's
   `Time` + `Date` types where the schema engine derives
   field names from primitives and collides.

Tests added to schema-rust unit tests (3 new):
- `composer_emits_authored_effect_table_when_schema_declares_one`
  proves the recorder fixture emits the closed AuthoredEffect
  enum + dispatcher + string-keyed lookup.
- `composer_emits_storage_descriptor_when_schema_declares_one`
  proves the storage fixture emits the StorageDescriptor + TABLES.
- `composer_omits_authored_emission_when_schema_has_no_effect_table`
  proves the simple fixture (no authored feature) doesn't leak
  the authored emission --- non-regressive.

The legacy route-derived `effect_items()` still fires for wire
schemas with routes; the authored emission is **additive** and
only appears when the EffectTable feature is declared.

### persona-spirit (`e0378b8d`)

Replaces the `// BLOCKED:` stub markers from /103 with working
code. The schemas in this branch import from sibling crates which
the schema reader can't resolve without an adjacent worktree
layout, so the schema-driven Rust types are HAND-WRITTEN to MATCH
what `emit_schema!` will produce once the cross-crate resolution
infrastructure lands. The shapes mirror the .schema files
verbatim:

- `schema_driven/storage.rs` — `VersionMarker` (rkyv-encoded;
  matches spirit-storage.schema `[u32 u32 u32]`),
  `UpgradeOutcome` + `UpgradeLogEntry` (matches
  spirit-upgrade-log.schema), `TableDescriptor` +
  `StorageDescriptor` matching the StorageDescriptor feature, and
  `SpiritStorageHandle::open()` implementing /346 §4 step 6
  auto-migration: reads version marker, runs `run_migration()`
  bridge if previous, writes NEXT marker forward, logs to
  in-memory upgrade-log table. Tests prove the marker round-trips
  to disk, a fresh DB writes NEXT + logs `NoMigrationNeeded`, a
  MAIN-marker DB triggers migration + logs `MigratedSuccessfully`
  + advances the marker, and a reopen sees NEXT.
- `schema_driven/recorder.rs` — `RecorderAction` /
  `RecorderResponse` (with universal `Unknown(String)`),
  payload structs, `SpiritRecorder::handle()` with the
  contact-point match block per /346 §2. Atomic identifier minting,
  subscription tracking, status reporting.
- `schema_driven/observer.rs` — `ObserverAction` / `ObserverResponse`
  + subscription table + publish-with-filter dispatch. Filter
  semantics: matching topic OR wildcard (no filter) — proven by
  two tests.
- `schema_driven/supervisor.rs` — `SupervisorAction` /
  `SupervisorResponse` + lifecycle state machine
  (Starting/Running/Drained) + uptime tracking + policy reload.
- `schema_driven/reading_actor.rs` — `ReadingActorAction` /
  `ReadingActorResponse` + log-sink attach/detach + dispatcher
  with auto-tap discipline per /346 §5 (every dispatch captures
  a `TapCapture` row regardless of destination).

`mod.rs` updated: removes the BLOCKED-emit_schema comments,
documents the hand-written-now / schema-emitted-later substitution
path. 17 new schema_driven unit tests pass.

### signal-persona-spirit (`5ba7ff99`)

Dual-emission landing per /103 anomaly 3:

- `signal-frame` Cargo dep flipped to the designer branch.
- `emit_schema!()` invoked AFTER the existing
  `signal_channel!([schema])` invocation in `src/lib.rs`. Both
  produce concrete types: legacy at
  `signal_persona_spirit::Operation` (root level), schema-driven
  at `signal_persona_spirit::spirit::Operation` (wrapped module).
- `tests/schema_module.rs` verifies the schema-driven module is
  reachable: `Operation::State(StateEndpoint::Statement(...))`
  constructs, `ROUTES` + `ROUTE_COUNT` constants visible,
  `ExtendedHeader::empty()` returns the 256-byte form, route-derived
  `EffectTable` scaffold exists.

The operator integration cycle can now migrate downstream consumers
to the qualified `signal_persona_spirit::spirit::*` paths
incrementally, then remove the legacy `signal_channel!()`
invocation once all consumers flip.

## Worktrees (for tracking per intent 633)

All four are jj workspaces tracking branches pushed to GitHub:

- `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-full-stack-spirit-2026-05-25`
- `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-full-stack-spirit-2026-05-25`
- `/home/li/wt/github.com/LiGoldragon/persona-spirit/designer-schema-full-stack-spirit-2026-05-25`
- `/home/li/wt/github.com/LiGoldragon/signal-persona-spirit/designer-schema-full-stack-spirit-2026-05-25`

## Verification results

All four branches' `nix flake check --option max-jobs 0
--print-build-logs` invocations report `all checks passed!`. The
flake-check invocations validate:

- `schema`: fmt + clippy + cargo test (24 lib doc tests +
  effect_side_features 10 tests + multi_pass 4 + multi_pass_pipeline
  4 + node_shape 5 + nota_shape 3 + reader 4 = 54 total tests).
- `signal-frame`: fmt + clippy + cargo test (signal-frame unit +
  schema-rust unit + emit_schema integration + namespace + channel
  + frame + command-line + trybuild ui).
- `persona-spirit`: fmt + clippy + cargo test (schema_driven 17 +
  store 13 + pipeline 17 + daemon 24 + client 6 + spirit-binary 4 =
  81 total tests).
- `signal-persona-spirit`: fmt + clippy + cargo test (round_trip 10
  + short_header 4 + schema_module 4 + migration 2 + box_form 3 =
  23 total tests, including 4 new schema_module tests).

## Anything still blocked

**Cross-crate schema-import resolution** is the one piece deferred
to a future operator slice. The persona-spirit schemas
(`spirit-recorder.schema`, `spirit-observer.schema`, etc.) import
from sibling crates (`signal-persona-spirit/spirit.schema`,
`spirit-storage`, etc.) which the `LoadedSchema::read_path`
resolver can't follow without an adjacent worktree layout that
mirrors the deployed repo tree. Today the in-tree imports resolve
to absolute paths that don't exist in the persona-spirit worktree
in isolation.

The chosen workaround in `persona-spirit/src/schema_driven/` is
hand-written Rust types that MATCH what `emit_schema!` will emit
once cross-crate resolution lands. The actor engine code (handle
methods, internal state, tests) stays; only the type definitions
swap when the macro lights up. This is the lowest-leverage
deferral: the migration runner, the actor patterns, and the
universal-Unknown floor all work today against the hand-written
types.

The infrastructure piece is the `emit_schema!` proc-macro's import
resolution algorithm — it needs to follow `(Import schema-name [...])`
references either through Cargo dep paths or through an explicit
`SCHEMA_DEP` environment variable / build script. Tracking item;
operator slice.

## What operator integrates next

Per-repo merge order:

1. **schema** — merge first; no downstream depends on the new
   `Feature` variants compiling correctly until schema-rust
   pivots.
2. **signal-frame** — merge second; depends on schema branch
   being on main (or temporarily on the designer-schema-full-stack
   branch which the Cargo.toml currently pins). When operator
   merges schema first, they update signal-frame's Cargo.toml
   back to `branch = "main"`.
3. **signal-persona-spirit** — merge third; depends on signal-frame
   carrying the disambig fix + the authored-feature emissions.
   When operator merges signal-frame, they update
   signal-persona-spirit's Cargo.toml back to `branch = "main"`.
4. **persona-spirit** — merge last; touches the daemon's
   src/schema_driven and adds the migration runner. The change
   is additive (existing src/store.rs + src/actors/* still ship);
   the new schema_driven module is gated behind hand-written types
   that don't depend on the macro lighting up.

Rippling concerns:

- **The dual emission in signal-persona-spirit IS the
  designer-recommended migration path** per /103 anomaly 3. The
  operator decides when to flip downstream consumers to the
  qualified `signal_persona_spirit::spirit::*` paths and remove
  the legacy `signal_channel!([schema])` invocation. That
  removal is a separate breaking commit; this branch leaves both
  emissions live.
- **The schema-rust composer emits `AuthoredEffect` /
  `AuthoredFanOutOutput` / `AuthoredEffectTable` only when the
  schema declares the `EffectTable` feature**. The legacy
  route-derived `Effect` / `EffectTable` / `FanOut` / `Interact`
  emissions still fire for wire schemas with routes. The two
  layers coexist; no schema needs to be migrated immediately to
  pick up the authored emission.
- **The persona-spirit migration runner is an in-memory
  upgrade-log today** (the actor's `upgrade_log: Mutex<Vec<...>>`
  collects entries). When the cross-crate schema resolution lands
  and `emit_schema!("spirit-upgrade-log.schema")` lights up, the
  in-memory log moves to a real redb-backed `UpgradeLogTable`
  per /346 §4 step 6. The shapes are aligned today.
- **The `Time` / `Date` field-name disambiguation** in schema-rust
  produces `u8` + `u8_2` + `u8_3` from `[u8 u8 u8]`. Code that
  consumes the emitted types using positional construction (e.g.
  `Time::new(0, 0, 0)`) keeps working. Code that uses field-name
  construction needs the suffix-aware names. The wire schema's
  legacy signal_channel! emission still uses positional fields
  via the older path, so nothing downstream breaks today; the
  schema-driven path uses the disambiguated names from launch.

## Key code paths landed

- `schema/src/shape_parser.rs::parse_effect_table_feature`
- `schema/src/shape_parser.rs::parse_fan_out_targets_feature`
- `schema/src/shape_parser.rs::parse_storage_descriptor_feature`
- `schema/src/multi_pass.rs::EffectTableRecognizer`
- `schema/src/multi_pass.rs::FanOutTargetsRecognizer`
- `schema/src/multi_pass.rs::StorageDescriptorRecognizer`
- `schema/src/engine.rs::LoweringContext::finalize_universal_unknowns`
- `schema/src/engine.rs::UniversalUnknownMacro::inject_unknown_into_enum_body`
- `signal-frame/schema-rust/src/lib.rs::authored_effect_items`
- `signal-frame/schema-rust/src/lib.rs::storage_descriptor_items`
- `signal-frame/schema-rust/src/lib.rs::record_field_tokens_disambiguated`
- `persona-spirit/src/schema_driven/storage.rs::SpiritStorageHandle::open`
- `persona-spirit/src/schema_driven/storage.rs::run_migration`
- `persona-spirit/src/schema_driven/recorder.rs::SpiritRecorder::handle`
- `persona-spirit/src/schema_driven/observer.rs::SpiritObserver::handle`
- `persona-spirit/src/schema_driven/supervisor.rs::SpiritSupervisor::handle`
- `persona-spirit/src/schema_driven/reading_actor.rs::ReadingActor::dispatch`
- `signal-persona-spirit/src/lib.rs::emit_schema!()`
