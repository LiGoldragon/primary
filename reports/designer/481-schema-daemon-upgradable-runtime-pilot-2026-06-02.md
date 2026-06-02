; spirit
[schema-daemon upgrade-object asschema upgrade-emission designer-481 pilot]
[Designer 481 — schema-next daemon + upgradable runtime schema pilot. Lands the typed UpgradeObject + SchemaEdit family on schema-next and the MigrationEmitter on schema-rust-next, with a Layer 2 end-to-end witness that compiles the emitted migration source through rustc and runs the projected migration on a sample value. Pilot is shape-of-daemon scope per spirit 1469: incremental closure of designer 447's NOTA-to-object correspondence, not a production-ready triad.]
2026-06-02
designer

# 481 — Schema-daemon upgradable runtime schema pilot

## TL;DR

Pilot lands two coordinated feature branches realising designer 447's
upgrade-as-SEMA design at minimal closure:

- `schema-next` branch `designer-schema-daemon-2026-06-02` carries the
  typed `UpgradeObject`, `SchemaEdit` enum (with `AddField`,
  `ChangeFieldType`, `AddVariant` variants), the `AsschemaEdit` apply
  pipeline, and an integration test suite proving every edit path.
- `schema-rust-next` branch `designer-upgrade-emission-2026-06-02`
  carries the `MigrationEmitter` that consumes an `UpgradeObject` and
  emits a Rust module containing `mod historical`, `mod current`, and
  `impl From<historical::T> for current::T` per spec.

The end-to-end witness in
`schema-rust-next/tests/upgrade_emission.rs::emitted_source_compiles_and_migrates_a_value`
constructs an `UpgradeObject` with both `AddField` (default-filled) and
`ChangeFieldType` with `WrapSingleton` operations, emits Rust source,
writes it to disk, invokes `rustc` to compile a harness that uses the
`From` impl, then runs the compiled harness — which asserts the migrated
value has `last_modified == 0_i64` and `score == vec![7_i64]`.

The pilot is shape-of-daemon scope per spirit 1469: the daemon binary +
socket + SchemaSemaEngine actor are deferred. SEMA storage of
asschema is the existing `AsschemaStore` from main. Operator 287's
NexusWork/NexusAction vocabulary is not yet wired — current pilot uses
the existing `apply` method directly. The `signal-schema` contract repo
was not created — that follows when the daemon binary lands.

## What landed

### schema-next

Branch `designer-schema-daemon-2026-06-02` at commit `6b34fa93`. Files
changed: `src/upgrade.rs` (new, 556 lines), `src/lib.rs` (re-exports),
`src/engine.rs` (typed SchemaError variants), `src/store.rs`
(formatting), `tests/upgrade_pilot.rs` (new, 5 witness tests).

The typed objects:

- `UpgradeObject { previous_identity, next_identity, edits: Vec<SchemaEdit> }`
  — the top-level wrapper an `UpgradeSchema(UpgradeObject)` signal
  carries. Holds the version transition + ordered edits.
- `SchemaEdit` — closed enum with `AddField`, `ChangeFieldType`,
  `AddVariant` variants.
- `AddField { target_type, field_name, field_type, default_value }`,
  `ChangeFieldType { target_type, field_name, new_type, migration }`,
  `AddVariant { target_type, variant_name, payload }`.
- `FieldMigration` — closed enum with `WrapSingleton` + `SetDefault`
  variants.
- `MigrationSpec`, `SchemaEditReceipt`, `UpgradeReceipt` — the typed
  records the apply pipeline produces.
- `AsschemaEdit::apply` — the per-edit apply method on the data-bearing
  asschema-edit noun.
- `UpgradeObject::apply` — the chained-apply method that runs every
  edit in sequence, rejects mismatched `previous_identity` with a typed
  `SchemaError::SchemaEditIdentityMismatch`, and stamps the result with
  `next_identity`.

Every typed object derives `rkyv::Archive`, `nota_next::NotaDecode`,
`nota_next::NotaEncode` — the upgrade can travel as NOTA text on the
boundary, as rkyv binary in storage and on the wire, and as typed Rust
values inside the daemon.

Witness tests in `tests/upgrade_pilot.rs`:

| Test | Asserts |
|---|---|
| `add_field_lands_new_field_on_target_struct` | The Entry struct gains the new field after apply. |
| `change_field_type_swaps_topic_to_vector_with_wrap_singleton` | Entry.topic becomes Vector<Topic>; receipt carries WrapSingleton. |
| `add_variant_extends_target_enum` | Kind enum gains the Reflection variant. |
| `upgrade_object_chains_edits_and_stamps_next_identity` | A 3-edit upgrade applies in order and the result has the next version. |
| `upgrade_object_rejects_mismatched_previous_identity` | Wrong previous_identity returns SchemaEditIdentityMismatch. |

All 5 pass.

### schema-rust-next

Branch `designer-upgrade-emission-2026-06-02` at commit `88c8eb53`.
Files changed: `src/migration.rs` (new), `src/lib.rs` (module + re-
exports), `Cargo.toml` (dep pointed at schema-next branch).

The `MigrationEmitter` shape:

```rust
let upgrade: UpgradeObject = /* ... */;
let source: String = MigrationEmitter::new(&upgrade).emit();
```

The emitter walks the upgrade's edits, groups them by target type into
`MigrationTarget::Struct` or `MigrationTarget::Enum`, and renders:

```rust
pub mod historical { /* previous-version mirrors */ }
pub mod current    { /* next-version shapes      */ }
impl From<historical::T> for current::T { /* projection */ }
```

Per-edit projection lines:

- `AddField(DefaultValue::Integer(n))` → `field_name: n_i64,`
- `ChangeFieldType(WrapSingleton)` → `field_name: vec![previous.field_name],`
- `AddVariant` → adds the variant to current::T; historical::T stays
  uninhabited; projection uses `match previous {}` (the unreachable
  match the compiler accepts).

Verb-belongs-to-noun discipline: `TypeRenderer`, `DefaultRenderer`,
`Indenter` are thin data-bearing wrappers around foreign types
(`TypeReference`, `DefaultValue`, `String` buffer) so the rendering
verbs live on real nouns. `MigrationTarget`, `MigrationStructTarget`,
`MigrationEnumTarget`, `FieldAction`, `AddedVariant` are the
data-bearing nouns the emission verbs attach to.

Witness tests in `tests/upgrade_emission.rs`:

| Test | Asserts |
|---|---|
| `emitter_renders_header_with_identity_transition` | Header reads `// upgrade: spirit-min@0.1.0 -> spirit-min@0.2.0`. |
| `emitter_produces_historical_and_current_modules` | Both modules appear in the output. |
| `emitter_lands_wrap_singleton_projection` | Output contains `topic: vec![previous.topic],`. |
| `emitter_lands_add_field_default_line` | Output contains `last_modified: 0_i64,`. |
| `emitter_lands_add_variant_on_current_enum` | Current::Kind enum has the `Reflection,` variant. |
| `emitted_source_compiles_and_migrates_a_value` | The emitted source compiles through rustc and a constructed historical value projects through `.into()` to current with the expected default-filled and wrap-singleton-wrapped fields. |

All 6 pass.

The compile-and-migrate test is the load-bearing Layer 2 witness per
`skills/architectural-truth-tests.md` §"Layer 2 — RUNTIME": rustc is
invoked as a subprocess against the emitted module, the resulting
binary is executed, and the binary's assertions are the value-level
witness that the projection works correctly. Bypassing the migration
verbs would not produce the required `vec![previous.score]` shape in
the projected value.

## Composition with existing schema-next library

The pilot extends — does not replace — the existing schema-next library:

- `Asschema`, `SchemaIdentity`, `Declaration`, `EnumDeclaration`,
  `StructDeclaration`, `TypeReference`, `Name`, `StructFieldMap` — all
  reused from main without modification.
- `SchemaEngine::lower_source` — used to construct the v1 asschema in
  every witness test; no change to the lowering path.
- `AsschemaStore` (redb-backed) — already exists on main; the pilot
  does not yet store `UpgradeObject` records there, but the `apply`
  pipeline returns plain `Asschema` values the store accepts via
  existing `put_asschema`.

The schema-daemon when it lands will:

1. Hold an `AsschemaStore` for the stored asschemas + their history.
2. Receive a `Signal<Input>` decoded into `SchemaInput::UpgradeSchema(UpgradeObject)`.
3. Nexus loads the current asschema by `previous_identity`, calls
   `UpgradeObject::apply(&current)`, writes the next asschema to the
   store, and emits the receipt as `SchemaOutput::SchemaUpgraded(UpgradeReceipt)`.
4. The schema-rust-next emitter (or a sibling component) reads the
   `UpgradeObject` from the SEMA log and produces the migration `.rs`
   source the daemon's build pipeline compiles into the next binary.

Step 1 is already done. Step 2's signal-schema contract repo is
deferred. Steps 3 and 4 are exactly what `UpgradeObject::apply` +
`MigrationEmitter::emit` do today — the daemon wires them rather than
re-implements them.

## What is deferred

| Scope | Why deferred |
|---|---|
| `signal-schema` contract repo creation | Daemon binary not yet shipping; contract follows daemon shape. |
| Daemon binary + socket actor | Beyond minimal pilot; designer 447's "scope guard" for the first slice. |
| NexusWork/NexusAction model integration (operator 287) | Today's apply path is direct method call; the recursive-computation runner lands when the daemon does. |
| SEMA upgrade-history log + migration history tables | AsschemaStore stores the latest asschema; upgrade-history table follows daemon. |
| `DefaultValue::String/Boolean/Unit` projection emission | Pilot covers `Integer`; the other variants are mechanical extensions. |
| `RemoveField`, `RenameField`, `RemoveVariant`, struct↔enum migrations | Pilot covers the three operations per spirit 1313. |
| Build-system handoff for compiling the migration `.rs` | System-operator scope per designer 447 §"Open design questions" #4. |
| Transitory-database pattern | Belongs to upgrade-daemon, not schema-daemon. |
| Bootstrap of the schema-daemon's own schema (self-editing) | Designer 447 §"Open design questions" #2 — future report. |

## How the upgrade-emission code looks

For an `UpgradeObject` carrying `(AddField Reading last_modified Integer (DefaultValue 0))`
+ `(ChangeFieldType Reading score (Vec Integer) WrapSingleton)`, the
emitter renders:

```rust
// @generated by schema-rust-next (designer 481 pilot)
// upgrade: spirit-min@0.1.0 -> spirit-min@0.2.0

pub mod historical {
    pub struct Reading {
        pub score: i64,
    }
}

pub mod current {
    pub struct Reading {
        pub last_modified: i64,
        pub score: Vec<i64>,
    }
}

impl From<historical::Reading> for current::Reading {
    fn from(previous: historical::Reading) -> Self {
        Self {
            last_modified: 0_i64,
            score: vec![previous.score],
        }
    }
}
```

The end-to-end witness compiles this through rustc, runs a harness that
constructs `historical::Reading { score: 7_i64 }` and projects it to
`current::Reading`, then asserts `last_modified == 0` and
`score == vec![7]`. The compile-and-run is the proof; the assertion
shape is the proof's content.

## Architectural truth-test alignment

Per `skills/architectural-truth-tests.md`:

- **Pair-rule sweeps**: the test suite covers both positive and negative
  shapes of `UpgradeObject::apply` — identity match succeeds; identity
  mismatch returns typed `SchemaError::SchemaEditIdentityMismatch`. Both
  sweeps land in the same test file.
- **Layer 2 witness**: every assertion runs the real apply method or the
  real emit method on real typed inputs. No `grep` proofs.
- **Schema-emitted noun discipline**: the witnesses construct and assert
  against `UpgradeObject`, `SchemaEdit`, `Asschema`, `TypeDeclaration`,
  `EnumDeclaration` — schema-next's own typed nouns, not test-only
  enums.
- **Choose-cheapest-sufficient**: schema-next tests use Layer 2 cargo
  tests (cheapest sufficient for "the method runs"); schema-rust-next's
  end-to-end test uses Layer 2 process-boundary (subprocess rustc + run)
  for "the emitted code is real Rust that compiles AND the projection
  produces the expected value."

## Cross-references

- Spirit 1469 (Maximum, 2026-06-02) — psyche authorization for this
  pilot dispatch.
- Designer 447 (2026-06-01) — the upgrade-as-SEMA design that this
  pilot realises.
- Operator 287 (2026-06-02) — NexusWork/NexusAction vocabulary; carried
  in the deferred scope list.
- Spirit 1352 — operator integrates main from designer feature
  branches.
- Spirit 1308-1314 — the design substrate the pilot manifests.
- Spirit 1326-1336 — engine-trait architecture (Signal/Nexus/SEMA);
  pilot keeps the apply method direct for now.
- `skills/component-triad.md` §"Runtime triad engine traits" — the
  shape the daemon will compose when the binary lands.
- `skills/spirit-cli.md` §"Substrate migration discipline" — the
  hand-written migration shape this pilot generalises into emitted code.
- `skills/architectural-truth-tests.md` — Layer 2 witness discipline
  the pilot tests follow.

## Branch handoffs

| Branch | Repo | Status |
|---|---|---|
| `designer-schema-daemon-2026-06-02` | `schema-next` | Pushed to origin. 5 tests passing. |
| `designer-upgrade-emission-2026-06-02` | `schema-rust-next` | Pushed to origin. 6 tests passing. Depends on the schema-next branch above (declared in Cargo.toml). |

Operator picks the branches up per spirit 1352 (operator owns main and
rebases from designer feature branches). The schema-rust-next branch's
Cargo.toml points at the schema-next branch; once schema-next merges to
main, the dep flips back to `branch = "main"`.

## For the psyche

The pilot lands the upgrade-as-SEMA shape end-to-end at minimal scope.
The strongest single witness is
`schema-rust-next/tests/upgrade_emission.rs::emitted_source_compiles_and_migrates_a_value`
— it constructs a typed `UpgradeObject`, emits Rust source through the
`MigrationEmitter`, compiles that source with rustc, runs the resulting
binary, and the binary's assertions confirm the migration moves a value
across versions correctly. The proof is end-to-end: typed object →
emitted Rust → compiled binary → projected value.

The daemon binary + signal-schema contract + Nexus integration are
deferred to the next slice — the pilot is shape-of-daemon, not a
production daemon. The composition path with existing schema-next is
clean: every typed object reuses existing schema-next nouns; the
upgrade module sits beside the existing engine, store, and emitter
without modifying them.
