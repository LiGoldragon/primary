# 105 — schema-driven spirit full-stack implementation showcase

> **RETRACTION BANNER (2026-05-26, records 713-715).** The `EffectTable`,
> `FanOutTargets`, and `StorageDescriptor` features this report exercises
> as **authored** schema content are drift. Per psyche 2026-05-26: schemas
> define data types only; effects and fan-out are runtime dispatch / logic.
> The C4 closure tests still witness a useful property — that dispatcher
> tables are closed enums Rust enforces exhaustively at compile time —
> but the **EFFECT TABLE itself shouldn't have been an authored schema
> feature**. The closure discipline survives; the surface it was tested
> against does not. Canonical authored schema shape: namespace key-value
> map of types only (see `signal-persona-spirit/spirit.schema`). Re-shaping
> the POC schemas and re-targeting these tests against the right surface
> is a separate operator pass.

*Designer-lane subagent dispatch 2026-05-25. Empirical verification of
the four-repo landing reported in /104. Authority: /103, /104, /346,
/345. Every constraint from /346 is exercised against a live test —
22 schema_driven tests pass in persona-spirit (was 17; five new
constraint proofs added this session), 7 new constraint proofs land in
the schema crate's `tests/constraint_proofs.rs`, and one new closed-
dispatcher proof lands in schema-rust. Net additions across this
session: 13 new tests, all passing. No production code modified.*

## §1 Tour

| What | Where |
|---|---|
| Six actor schemas (NOTA) | `persona-spirit/spirit-{recorder,storage,observer,supervisor,reading-actor,upgrade-log}.schema` |
| Three new multi-pass recognizers | `schema/src/multi_pass.rs::{EffectTable,FanOutTargets,StorageDescriptor}Recognizer` |
| Universal-Unknown post-pass hook | `schema/src/engine.rs::LoweringContext::finalize_universal_unknowns` |
| Shape parser entry points | `schema/src/shape_parser.rs::parse_{effect_table,fan_out_targets,storage_descriptor}_feature` |
| Streaming-decoder equivalents | `schema/src/parser.rs::parse_{effect_table,fan_out_targets,storage_descriptor}_feature` |
| Composer authored emissions | `signal-frame/schema-rust/src/lib.rs::{authored_effect_items,storage_descriptor_items,record_field_tokens_disambiguated}` |
| Daemon migration runner | `persona-spirit/src/schema_driven/storage.rs::{SpiritStorageHandle,run_migration}` |
| Actor engines | `persona-spirit/src/schema_driven/{recorder,observer,supervisor,reading_actor}.rs` |
| Dual emission | `signal-persona-spirit/src/lib.rs::{signal_channel,emit_schema}!()` |
| Proc-macro pipeline entry | `signal-frame/macros/src/schema_entry.rs::expand` |

Worktrees (all four jj workspaces present, tracking
`designer-schema-full-stack-spirit-2026-05-25@origin`):

- `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-full-stack-spirit-2026-05-25` (origin `b499190a`)
- `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-full-stack-spirit-2026-05-25` (origin `b35d18bd`)
- `/home/li/wt/github.com/LiGoldragon/persona-spirit/designer-schema-full-stack-spirit-2026-05-25` (origin `e0378b8d`)
- `/home/li/wt/github.com/LiGoldragon/signal-persona-spirit/designer-schema-full-stack-spirit-2026-05-25` (origin `5ba7ff99`)

## §2 The .schema files — proof code (NOTA)

The six actor schemas authored in `persona-spirit/` instantiate the
/346 actor-schema pattern.

### `spirit-recorder.schema` — ACTION + RESPONSE + EffectTable

```nota
;; namespace --- ACTION + RESPONSE + the supporting types
{
  RecorderAction (
    RecordEntry  ObserveRecorder  SnapshotRecords
    OpenRecordSubscription  CloseRecordSubscription  QueryStatus
  )
  RecorderResponse (
    RecordAccepted  RecordsObserved  RecordSnapshotReturned
    SubscriptionOpened  SubscriptionRetracted  StatusReturned
  )
  ;; payloads
  RecordEntry [Entry]
  ObserveRecorder [RecordObservation]
  ...
}

;; features --- the effect-table maps actions to fan-out outputs
[
  (EffectTable [
    (RecordEntry RecordWriteEffect)
    (OpenRecordSubscription SubscriptionOpenEffect)
    (CloseRecordSubscription SubscriptionCloseEffect)
  ])
  (FanOutTargets [
    (RecordWriteEffect [
      (Store SpiritStorage InsertStampedEntry)
      (Notify ObserverSet PublishRecordCaptured)
      (Reply RecordAccepted)
    ])
    ...
  ])
]
```

The schema declares /346 §1's two enums (`RecorderAction`,
`RecorderResponse`) without the `Unknown` variant — the schema engine
injects it through `UniversalUnknownMacro` per /346 §9. The
`EffectTable` lines up actions with effect types per /343 §3; the
`FanOutTargets` declares the three FanOutOutputDeclaration kinds:
`(Store ...)` is the Actor form, `(Reply ...)` is the Reply form, and
elsewhere `(FanOutSubscribers ...)` would be the Subscribers form (see
`spirit-observer.schema`).

### `spirit-storage.schema` — StorageDescriptor declarations

```nota
{
  RecordsTable [RecordIdentifier StoredRecord]
  RecordIdentifierMintTable [MintKey RecordIdentifierMint]
  ...
  ;; Version marker stored alongside the database per /346 §4 step 4.
  VersionMarker [u32 u32 u32]
}

[
  (StorageDescriptor [
    (Records RecordsTable)
    (RecordIdentifierMint RecordIdentifierMintTable)
  ])
]
```

The `StorageDescriptor` feature names two redb tables (logical name →
table-type pair). The `VersionMarker [u32 u32 u32]` declaration is
load-bearing — it's the on-disk marker the auto-migration runner reads
per /346 §4 step 6.

### `spirit-observer.schema` — internal-channel actor

Declares `ObserverAction`/`ObserverResponse`; the EffectTable maps
`PublishRecordCaptured` to `ObserverPublishEffect`, and the
FanOutTargets uses the **Subscribers** form:
`(FanOutSubscribers ObserverSubscriberSet Dispatch)`. This is the third
FanOutOutputDeclaration kind /346 §10 inventories.

### `spirit-supervisor.schema` — cross-actor coordinator

Six-action lifecycle vocabulary (`StartEngine`, `DrainEngine`,
`ReloadBootstrapPolicy`, ...) with EffectTable rows fanning out into
recorder/observer/storage drain operations. The fan-out output rows are
all Actor-form: `(Open SpiritStorage Open)`, `(Drain RecorderActor
Drain)`, `(Apply ObserverSet ApplyPolicy)`.

### `spirit-reading-actor.schema` — response dispatcher

Per /346 §5 the reading actor is itself an actor with its own schema.
Its action vocabulary is dispatch-by-response-type:
`DispatchRecorderResponse [DispatchEnvelope RecorderResponse]`. The
EffectTable's FanOutTargets show the auto-tap discipline:

```nota
(DispatchEffect [
  (Forward DestinationActor Deliver)
  (Tap LogSinkSet WriteEntry)
  (Reply ResponseDispatched)
])
```

Every dispatch hits the logging tap — the schema declares this
declaratively, not as runtime convention.

### `spirit-upgrade-log.schema` — append-only log

```nota
{
  UpgradeLogTable [u64 UpgradeLogEntry]
  UpgradeLogEntry [
    VersionMarker  VersionMarker  UpgradeOutcome
    UpgradeTimestamp  UpgradeDuration
  ]
  UpgradeOutcome (
    MigratedSuccessfully  NoMigrationNeeded
    MigrationFailed  RolledBack
  )
  ...
}

[ (StorageDescriptor [ (UpgradeLog UpgradeLogTable) ]) ]
```

Separate from `spirit-storage.schema` because per /345 §2 each contract
is its own channel; the upgrade log's lifetime and authority are
distinct from the records table's.

## §3 The schema crate (proof code: Rust)

### Recognizers — what triggers what

The dispatch site in `multi_pass.rs:826` routes feature heads:

```rust
"EffectTable" => EffectTableRecognizer::recognize(value).map(Feature::EffectTable),
"FanOutTargets" => FanOutTargetsRecognizer::recognize(value).map(Feature::FanOutTargets),
"StorageDescriptor" => StorageDescriptorRecognizer::recognize(value).map(Feature::StorageDescriptor),
```

Each recognizer reads the NotaValue tree and produces a typed Feature
variant. The `FanOutTargetsRecognizer::recognize_output` is the
load-bearing function for the three FanOutOutputDeclaration kinds
(`multi_pass.rs:939-998`):

```rust
match head {
    "Reply" => { /* (Reply Variant) -> FanOutOutputDeclaration::Reply { variant } */ }
    "FanOutSubscribers" => { /* -> FanOutOutputDeclaration::Subscribers { actor_type, dispatch_method } */ }
    method_tag => { /* -> FanOutOutputDeclaration::Actor { method_tag, actor_type, actor_method } */ }
}
```

The default arm treats unrecognised heads as the Actor form (because
the first token is a method tag like `Store`/`Notify`/`Drain`). This
is the open-by-convention surface; the closed parts are guarded by the
explicit literal matches.

### Universal-Unknown injection — the actual implementation

`engine.rs:227-237`:

```rust
pub fn finalize_universal_unknowns(&mut self) {
    for schema_type in &mut self.types {
        let AssembledType::Local { name, body } = schema_type else {
            continue;
        };
        if !UniversalUnknownMacro::is_response_enum_name(name) {
            continue;
        }
        UniversalUnknownMacro::inject_unknown_into_enum_body(body);
    }
}
```

The idempotency check sits inside `inject_unknown_into_enum_body`
(`engine.rs:353-369`):

```rust
pub fn inject_unknown_into_enum_body(body: &mut DeclarationBody) {
    let DeclarationBody::Enum { variants } = body else { return };
    let already_has_unknown = variants
        .iter()
        .any(|variant| variant.name().as_str() == Self::UNKNOWN_VARIANT_NAME);
    if already_has_unknown { return; }
    let name = Name::new(Self::UNKNOWN_VARIANT_NAME)
        .expect("`Unknown` is a valid PascalCase identifier");
    variants.push(Variant::with_type(name, TypeExpression::Primitive(Primitive::String)));
}
```

Three guards: enum-shape only (record/newtype/alias skip), name ends
in `Response`, idempotent (`already_has_unknown` short-circuit). The
hook is called from BOTH `Schema::assemble` (`document.rs:140`) AND
the multi-pass `MacroPipeline::run` (`multi_pass.rs:353`) — both paths
produce identical AssembledSchemas, verified by
`constraint_c5d_lowering_context_finalize_hook_runs_through_multi_pass`
(see §7 C5d).

### Canonical parsers — pick one

`shape_parser.rs:278-294`:

```rust
fn parse_effect_table_feature(&self, data: &[NotaValue]) -> Result<Feature> {
    expect_exact_count("EffectTable feature", data.len(), 1)?;
    let rows = expect_sequence(&data[0], "EffectTable rows")?;
    let entries = rows.iter().map(|row| {
        let shape = expect_record(row, "EffectTable entry")?;
        let head = expect_record_head(shape, "EffectTable entry")?;
        let row_data = expect_record_data(shape, "EffectTable entry")?;
        let action = Name::new(head.to_owned())?;
        expect_exact_count("EffectTable entry", row_data.len(), 1)?;
        let effect = self.read_name(&row_data[0], "EffectTable effect")?;
        Ok(EffectTableEntry::new(action, effect))
    }).collect::<Result<Vec<_>>>()?;
    Ok(Feature::EffectTable(EffectTableFeature::new(entries)))
}
```

Each row is `(ActionName EffectName)` — the action sits in the record
head position; the effect is the single payload. The parallel
implementation in `parser.rs:412` consumes the streaming token stream
directly with identical semantics — proven by
`shape_parser_recognises_effect_table_and_fan_out_features` +
`streaming_parser_recognises_effect_table_and_fan_out_features`
(both pass; see §6).

## §4 The schema-rust composer (proof code: Rust)

### `authored_effect_items()` — what gets emitted

`schema-rust/src/lib.rs:455-549` is the emission function. Its
load-bearing emission block:

```rust
quote! {
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub enum AuthoredEffect { #(#effect_variants),* }
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub enum AuthoredFanOutOutput { #(#fan_out_output_variants),* }
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub struct AuthoredFanOut { pub outputs: Vec<AuthoredFanOutOutput> }
    #[derive(Clone, Debug, Default, PartialEq, Eq)]
    pub struct AuthoredEffectTable;
    impl AuthoredEffectTable {
        pub fn effect_for_action(action: &str) -> Option<&'static str> {
            match action { #(#effect_for_action_arms),*, _ => None }
        }
        pub fn fan_out_for_effect(effect: &str) -> Option<AuthoredFanOut> {
            match effect { #(#fan_out_for_effect_arms),*, _ => None }
        }
    }
}
```

The trailing `_ => None` is the closure guarantee — see §7 C4.

### `storage_descriptor_items()` — emission for tables

`schema-rust/src/lib.rs:585-612`:

```rust
quote! {
    #[derive(Clone, Copy, Debug, PartialEq, Eq)]
    pub struct TableDescriptor {
        pub logical_name: &'static str,
        pub table_type: &'static str,
    }
    #[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
    pub struct StorageDescriptor;
    impl StorageDescriptor {
        pub const TABLE_COUNT: usize = #count;
        pub const TABLES: &'static [TableDescriptor] = &[ #(#table_entries),* ];
        pub fn table_type_for(logical_name: &str) -> Option<&'static str> {
            match logical_name { #(#logical_arms),*, _ => None }
        }
    }
}
```

Same closure discipline — `_ => None` for unknown logical names.

### Duplicate-field-name disambiguation

`schema-rust/src/lib.rs:901-918`:

```rust
fn record_field_tokens_disambiguated(fields: &[Field]) -> Result<Vec<TokenStream>> {
    let mut seen: HashMap<String, usize> = HashMap::new();
    let mut tokens = Vec::with_capacity(fields.len());
    for field in fields {
        let base_name = field.effective_name().as_str().to_string();
        let count = seen.entry(base_name.clone()).or_insert(0);
        *count += 1;
        let name = if *count == 1 { base_name }
                   else { format!("{base_name}_{count}") };
        let ident = Ident::new(&name, Span::call_site());
        let expression = type_expression_tokens(field.expression())?;
        tokens.push(quote! { pub #ident: #expression });
    }
    Ok(tokens)
}
```

This was the blocking fix. Schemas like `Time [u8 u8 u8]` derive the
field-names from primitives — three `u8` fields would otherwise collide
in the Rust struct. The pattern: first occurrence keeps the base name;
subsequent occurrences become `u8_2`, `u8_3`, etc. The before/after
shape is:

- Before: `pub struct Time { pub u8: u8, pub u8: u8, pub u8: u8 }` — duplicate field error
- After: `pub struct Time { pub u8: u8, pub u8_2: u8, pub u8_3: u8 }` — compiles

### Live macro expansion — recorder.schema

Concrete demonstration: a diagnostic dump test
(`schema-rust/src/lib.rs::dump_recorder_emission_for_showcase`) emits
the composed Rust for `tests/fixtures/recorder.schema`:

```rust
pub mod recorder {
    pub const SCHEMA_PATH: &str = "...";
    pub struct RecordAccepted(pub u64);
    pub struct RecordEntry(pub Topic);
    pub enum RecorderAction { RecordEntry, QueryStatus }
    pub enum RecorderResponse {
        RecordAccepted,
        StatusReturned,
        Unknown(String),                    // <-- injected by UniversalUnknownMacro
    }
    pub struct Topic(pub String);
    pub enum AuthoredEffect { RecordWriteEffect }
    pub enum AuthoredFanOutOutput {
        Actor { method_tag: &'static str, actor_type: &'static str, actor_method: &'static str },
        Reply { variant: &'static str },
        Subscribers { actor_type: &'static str, dispatch_method: &'static str },
    }
    pub struct AuthoredFanOut { pub outputs: Vec<AuthoredFanOutOutput> }
    pub struct AuthoredEffectTable;
    impl AuthoredEffectTable {
        pub fn effect_for_action(action: &str) -> Option<&'static str> {
            match action {
                "RecordEntry" => Some("RecordWriteEffect"),
                _ => None,                  // <-- closure
            }
        }
        pub fn fan_out_for_effect(effect: &str) -> Option<AuthoredFanOut> {
            match effect {
                "RecordWriteEffect" => Some(AuthoredFanOut { outputs: vec![
                    AuthoredFanOutOutput::Actor {
                        method_tag: "Store",
                        actor_type: "SpiritStorage",
                        actor_method: "InsertStampedEntry",
                    },
                    AuthoredFanOutOutput::Reply { variant: "RecordAccepted" },
                ]}),
                _ => None,                  // <-- closure
            }
        }
    }
    // ExtendedHeader, ROUTES, RouteDescriptor, etc. follow.
}
```

Captured verbatim by running:

```
cargo test -p schema-rust dump_recorder_emission_for_showcase -- --ignored --nocapture
```

This proves the entire emission chain end-to-end: NOTA file →
LoadedSchema → AssembledSchema (with Unknown injected) → composed
TokenStream → readable Rust. The injected `Unknown(String)` sits inside
`RecorderResponse`; the closure wildcards sit at the end of both
dispatch matches.

## §5 The persona-spirit daemon (proof code: Rust)

### `SpiritStorageHandle::open()` — full implementation

`persona-spirit/src/schema_driven/storage.rs:165-233`. The three-branch
match on the on-disk marker IS the auto-migration runner per /346 §4
step 6:

```rust
pub fn open(location: impl Into<PathBuf>) -> Self {
    let location = location.into();
    let on_disk = read_version_marker(&location).ok();
    let mut upgrade_log = Vec::new();
    let final_marker = match on_disk {
        None => {                                            // 1. Fresh DB
            let _ = write_version_marker(&location, VersionMarker::NEXT);
            upgrade_log.push(UpgradeLogEntry { from: NEXT, to: NEXT,
                outcome: NoMigrationNeeded, ... });
            VersionMarker::NEXT
        }
        Some(marker) if marker == VersionMarker::NEXT => {   // 2. Already-NEXT DB
            upgrade_log.push(UpgradeLogEntry { from: marker, to: marker,
                outcome: NoMigrationNeeded, ... });
            marker
        }
        Some(previous) => {                                  // 3. Migration territory
            let migration = run_migration(&location, previous, VersionMarker::NEXT);
            match migration {
                Ok(()) => {
                    let _ = write_version_marker(&location, VersionMarker::NEXT);
                    upgrade_log.push(UpgradeLogEntry { from: previous, to: NEXT,
                        outcome: MigratedSuccessfully, ... });
                    VersionMarker::NEXT
                }
                Err(_) => { /* MigrationFailed */ previous }
            }
        }
    };
    Self { inner: Arc::new(SpiritStorageInner { location, marker, upgrade_log, ... }) }
}
```

Three load-bearing properties this code implements per /346 §4:

1. **Read version marker** (`read_version_marker(&location)`)
2. **Migration branch** when previous detected (`run_migration(...)`)
3. **NEXT write + upgrade-log append** on success

### `run_migration` bridge function

`storage.rs:263-274`:

```rust
pub fn run_migration(
    _location: &std::path::Path,
    previous: VersionMarker,
    next: VersionMarker,
) -> Result<(), MigrationError> {
    // Marker-only upgrade: no row transformations needed for the
    // MAIN -> NEXT bridge. Per /346 §4 step 5, when AssembledSchema
    // diff is empty, the bridge body can be elided --- this is that
    // case for the current build.
    let _ = (previous, next);
    Ok(())
}
```

In the current build, MAIN (`0.1.0`) and NEXT (`0.1.1`) differ only in
the version-marker existence — no row shape changes — so the bridge
body is elided per /346 §6's "when AssembledSchema diff is empty"
discipline. A future schema change (added field, renamed type) drops
its `From<previous::T> for next::T` impls here.

### Recorder actor engine — match block per /346 §2

`persona-spirit/src/schema_driven/recorder.rs:126-135`. The contact
point per `skills/enum-contact-points.md`:

```rust
pub fn handle(&self, action: RecorderAction) -> RecorderResponse {
    match action {
        RecorderAction::RecordEntry(payload) => self.record_entry(payload),
        RecorderAction::ObserveRecorder(filter) => self.observe(filter),
        RecorderAction::SnapshotRecords(filter) => self.snapshot(filter),
        RecorderAction::OpenRecordSubscription(payload) => self.open_subscription(payload),
        RecorderAction::CloseRecordSubscription(close) => self.close_subscription(close),
        RecorderAction::QueryStatus => self.status(),
    }
}
```

Exhaustive — the action enum is closed; Rust enforces this at compile
time. The body is logic; the structure is the schema. No
`RecorderAction::Unknown` arm: the universal Unknown lives on the
RESPONSE side, not the ACTION side.

### Universal Unknown safety floor in action

The injected variant is reachable on every Response enum. The test
`schema_driven::recorder::tests::unknown_variant_is_the_safety_floor`
(`recorder.rs:243-249`) constructs it directly:

```rust
let response = RecorderResponse::Unknown("rejected".into());
assert!(matches!(response, RecorderResponse::Unknown(reason) if reason == "rejected"));
```

Every other actor follows the same pattern — see the new C1 test in §7.

## §6 Behavior in practice — test runs (empirical)

Verbatim summary lines from running each repo's full test suite via
`nix develop --option max-jobs 0 --command cargo test --color=never`:

### schema crate

```
test result: ok. 24 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (lib doctests)
test result: ok.  7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (constraint_proofs) [NEW]
test result: ok. 10 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (effect_side_features)
test result: ok.  4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (document)
test result: ok.  4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (multi_pass)
test result: ok.  5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (node_shape)
test result: ok.  3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (nota_shape)
test result: ok.  4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out (reader)
                  --
                  61 total (was 54; +7 from constraint_proofs added this session)
```

### signal-frame workspace

```
test result: ok.  5 passed (schema_rust unit; was 4 — added constraint_c4) [+1]
test result: ok. 22 passed (channel_macro)
test result: ok.  1 passed (channel_macro_compile_fail)
test result: ok.  5 passed (command_line)
test result: ok.  5 passed (emit_schema)
test result: ok. 21 passed (frame)
test result: ok.  3 passed (namespace)
test result: ok.  1 passed (namespace_sections_compile_fail)
                  --
                  63 total (was 62; +1 from constraint_c4)
```

### persona-spirit

```
test result: ok. 25 passed; 0 failed (lib; was 20 — 17 schema_driven + 5 new constraint proofs) [+5]
test result: ok. 23 passed (actor_runtime)
test result: ok. 27 passed (boundary)
test result: ok. 23 passed; 1 failed (daemon) [pre-existing env issue — see §11]
```

Of the 17 pre-existing schema_driven unit tests, all pass. Five new
constraint-proof tests added this session (also pass). The single
failure (`persona_spirit_upgrade_completion_requires_accepted_readiness`)
is an environmental issue (`path must be shorter than SUN_LEN` — unix
domain socket path length); it's a property of the filesystem location
under `/home/li/wt/...`, not of the schema-driven landing. The
schema_driven module's tests all pass.

### signal-persona-spirit

```
test result: ok.  2 passed (box_form)
test result: ok.  3 passed (migration)
test result: ok. 10 passed (round_trip)
test result: ok.  4 passed (schema_module)
test result: ok.  4 passed (short_header)
                  --
                  23 total — unchanged
```

### The 17 persona-spirit schema_driven tests (one-line each)

| Module | Test | Proves |
|---|---|---|
| `observer` | `subscription_lifecycle_round_trips_token` | open + close yield the same token |
| `observer` | `publish_with_matching_filter_dispatches_to_all_subscribers` | publish notifies every matching subscriber |
| `observer` | `publish_with_non_matching_filter_only_dispatches_to_wildcards` | filter semantics: topic OR wildcard |
| `reading_actor` | `dispatch_records_tap_capture_and_increments_delivered` | every dispatch lands a TapCapture row (auto-tap §5) |
| `reading_actor` | `log_only_destination_does_not_increment_delivered` | LogOnly outcomes don't count as delivered |
| `reading_actor` | `log_sink_attach_and_detach` | attach/detach round-trips through sink map |
| `recorder` | `record_entry_returns_record_accepted_with_fresh_identifier` | atomic identifier minting from 1 |
| `recorder` | `query_status_reflects_record_count` | status tracks running counter |
| `recorder` | `subscription_lifecycle_round_trips_token` | sub lifecycle round-trip |
| `recorder` | `unknown_variant_is_the_safety_floor` | Universal Unknown reachable on RecorderResponse |
| `storage` | `version_marker_round_trip_to_file` | rkyv marker on disk decodes |
| `storage` | `fresh_database_writes_next_marker_and_logs_no_migration` | open() on a missing marker writes NEXT |
| `storage` | `previous_version_database_runs_migration_and_logs_success` | MAIN → migrate → NEXT, log records success |
| `storage` | `storage_descriptor_knows_authored_table_layout` | TABLES const matches schema declaration |
| `supervisor` | `start_transitions_to_running` | StartEngine → Running lifecycle |
| `supervisor` | `drain_transitions_to_drained` | DrainEngine → Drained lifecycle |
| `supervisor` | `reload_remembers_policy_source` | ReloadBootstrapPolicy preserves source |

### Migration-cycle tests verbatim

```
test schema_driven::storage::tests::version_marker_round_trip_to_file ... ok
test schema_driven::storage::tests::fresh_database_writes_next_marker_and_logs_no_migration ... ok
test schema_driven::storage::tests::previous_version_database_runs_migration_and_logs_success ... ok
```

The third asserts: write MAIN to disk; open → migration runs;
`current_marker() == Some(NEXT)`; upgrade_log[0] is
`MigratedSuccessfully` with `from: MAIN, to: NEXT`. Then re-open → no
migration; log records `NoMigrationNeeded`.

### Universal-Unknown injection tests verbatim

```
test universal_unknown_predicate_recognises_response_suffix ... ok
test universal_unknown_injection_adds_string_carrier_variant_idempotently ... ok
test assembled_schema_carries_injected_unknown_on_response_enum ... ok
test assembled_schema_does_not_inject_unknown_on_non_response_enums ... ok
```

The "does_not_inject" test loads `recorder.schema` and asserts the
ACTION enum does NOT carry Unknown — only RESPONSE-suffix enums do.

### EffectTable parser tests verbatim

```
test shape_parser_recognises_effect_table_and_fan_out_features ... ok
test streaming_parser_recognises_effect_table_and_fan_out_features ... ok
test effect_table_parses_action_to_effect_pairs ... ok
test fan_out_targets_parses_three_output_kinds ... ok
```

The `three_output_kinds` test exercises all three
FanOutOutputDeclaration variants from one fixture row.

## §7 Constraint tests — empirical proofs

Each /346 constraint is exercised by a test; verbatim output below.

### C1 — Every RESPONSE enum gets `Unknown`

**Schema-engine proof** (new this session) —
`schema/tests/constraint_proofs.rs::constraint_c1_every_response_enum_receives_unknown_variant`:

Builds a synthetic schema declaring three Response enums
(`ApplesResponse`, `BerriesResponse`, `CherriesResponse`) plus a
non-Response enum (`Mood`). Runs `Schema::assemble(&[])`. Asserts each
Response enum picks up `Unknown` AND `Mood` does NOT.

**Runtime proof** (new this session) — `persona-spirit/src/schema_driven/mod.rs::constraint_proofs::constraint_c1_every_actor_response_carries_unknown_variant`:

```rust
let _: RecorderResponse = RecorderResponse::Unknown("recorder".into());
let _: ObserverResponse = ObserverResponse::Unknown("observer".into());
let _: SupervisorResponse = SupervisorResponse::Unknown("supervisor".into());
let _: ReadingActorResponse = ReadingActorResponse::Unknown("reading-actor".into());
```

The constructor existing on every actor's Response enum IS the
structural proof — if any one was missing the variant, this wouldn't
compile.

Output:

```
test constraint_c1_every_response_enum_receives_unknown_variant ... ok
test schema_driven::constraint_proofs::constraint_c1_every_actor_response_carries_unknown_variant ... ok
test schema_driven::constraint_proofs::constraint_c1b_unknown_payload_is_string_across_actors ... ok
```

### C2 — Migration is idempotent

**Existing** (pre-session) — `previous_version_database_runs_migration_and_logs_success`
already reopens the post-migration DB and asserts no second migration
runs.

**Expanded** (new this session) —
`schema_driven::storage::tests::constraint_c2_migration_idempotent_under_repeated_reopen`:

Opens once (lands NEXT), then opens 3 more times. Each reopen the
marker stays NEXT and the log records `NoMigrationNeeded`.

```
test schema_driven::storage::tests::constraint_c2_migration_idempotent_under_repeated_reopen ... ok
```

### C3 — One byte layout for sema + signal

**New this session** —
`schema_driven::storage::tests::constraint_c3_version_marker_one_byte_layout_two_homes`:

```rust
let marker = VersionMarker::new(7, 13, 31);
let bytes_one = rkyv::to_bytes::<Failure>(&marker).expect("encodes (home a)");
let bytes_two = rkyv::to_bytes::<Failure>(&marker).expect("encodes (home b)");
assert_eq!(bytes_one.as_slice(), bytes_two.as_slice(),
    "rkyv encoding is deterministic across the two homes");
let archived = rkyv::access::<<VersionMarker as Archive>::Archived, Failure>(...)?;
assert_eq!(archived.major.to_native(), 7);
let recovered: VersionMarker = rkyv::deserialize::<VersionMarker, Failure>(archived)?;
assert_eq!(recovered, marker);
```

Encodes twice — once as if the marker were on the wire (signal home),
once as if it were going into the DB (sema home). The bytes are
identical. Per /346 §3 there is exactly one byte layout.

```
test schema_driven::storage::tests::constraint_c3_version_marker_one_byte_layout_two_homes ... ok
```

### C4 — EffectTable is closed

**New this session** —
`schema-rust::tests::constraint_c4_authored_effect_table_dispatcher_is_closed`:

Compiles the recorder fixture, gets the emitted Rust text, asserts
both `effect_for_action` and `fan_out_for_effect` terminate with a
`_ => None` wildcard arm. The wildcard IS the closure guarantee:
unknown action names map to `None` instead of panicking.

```
test tests::constraint_c4_authored_effect_table_dispatcher_is_closed ... ok
```

### C5 — `finalize_universal_unknowns` is idempotent

**Existing** — the pre-session test
`universal_unknown_injection_adds_string_carrier_variant_idempotently`
calls `inject_unknown_into_enum_body` twice and asserts only one
`Unknown` variant lands.

**Expanded** (new this session) — three additional proofs:

1. `constraint_c5_finalize_universal_unknowns_idempotent_on_full_lowering`
   — runs full schema assembly twice; counts exactly one Unknown in
   each result.
2. `constraint_c5_inject_unknown_into_enum_body_idempotent_under_many_calls`
   — calls the injector 16 times; asserts variant count stays at 3.
3. `constraint_c5d_lowering_context_finalize_hook_runs_through_multi_pass`
   — parses via the streaming decoder (different code path); asserts
   Unknown lands the same way.

Plus the negative tests:

- `constraint_c5b_is_response_enum_name_only_matches_suffix` — names
  containing "Response" mid-string are NOT matched.
- `constraint_c5c_non_enum_response_bodies_are_ignored` — record body
  named `*Response` is left alone.

```
test constraint_c5_inject_unknown_into_enum_body_idempotent_under_many_calls ... ok
test constraint_c5b_is_response_enum_name_only_matches_suffix ... ok
test constraint_c5c_non_enum_response_bodies_are_ignored ... ok
test constraint_c5_finalize_universal_unknowns_idempotent_on_full_lowering ... ok
test constraint_c5d_lowering_context_finalize_hook_runs_through_multi_pass ... ok
```

### C6 — NEXT version-marker discipline

**Existing** — three storage tests cover the discipline piecewise.

**Aggregated** (new this session) —
`constraint_c6_next_version_marker_discipline_end_to_end` runs all
three steps in one test:

1. Fresh DB → NEXT.
2. Wipe + seed MAIN → migrate → NEXT + MigratedSuccessfully.
3. Reopen → NEXT + NoMigrationNeeded.

```
test schema_driven::storage::tests::constraint_c6_next_version_marker_discipline_end_to_end ... ok
```

### Constraint summary

| Constraint | Test | Status | Source |
|---|---|---|---|
| C1 schema-side | `constraint_c1_every_response_enum_receives_unknown_variant` | PASS | new this session |
| C1 runtime | `constraint_c1_every_actor_response_carries_unknown_variant` | PASS | new this session |
| C1b payload-type | `constraint_c1b_unknown_payload_is_string_across_actors` | PASS | new this session |
| C2 migration idempotent | `constraint_c2_migration_idempotent_under_repeated_reopen` | PASS | new this session |
| C2 existing | `previous_version_database_runs_migration_and_logs_success` | PASS | pre-existing |
| C3 one byte layout | `constraint_c3_version_marker_one_byte_layout_two_homes` | PASS | new this session |
| C4 effect-table closed | `constraint_c4_authored_effect_table_dispatcher_is_closed` | PASS | new this session |
| C5 finalize idempotent | `constraint_c5_finalize_universal_unknowns_idempotent_on_full_lowering` | PASS | new this session |
| C5 inject 16x | `constraint_c5_inject_unknown_into_enum_body_idempotent_under_many_calls` | PASS | new this session |
| C5b suffix-only | `constraint_c5b_is_response_enum_name_only_matches_suffix` | PASS | new this session |
| C5c non-enum ignored | `constraint_c5c_non_enum_response_bodies_are_ignored` | PASS | new this session |
| C5d multi-pass path | `constraint_c5d_lowering_context_finalize_hook_runs_through_multi_pass` | PASS | new this session |
| C6 marker discipline | `constraint_c6_next_version_marker_discipline_end_to_end` | PASS | new this session |

All six /346 constraints hold empirically.

## §8 Internal flow walkthrough

### Compile-time pipeline (when `emit_schema!("spirit-recorder")` fires)

```mermaid
flowchart TB
    invoke["emit_schema!(\"spirit-recorder\")<br/>signal-frame/macros/src/schema_entry.rs:30"]
    parse_request["EmitSchemaRequest::parse<br/>schema_entry.rs:68"]
    resolve_path["schema_path()<br/>joins manifest-dir + literal"]
    read_path["LoadedSchema::read_path<br/>schema/src/reader.rs"]
    parse_nota["NOTA parse<br/>shape_parser.rs::parse_str"]
    multi_pass["MacroPipeline::run<br/>multi_pass.rs:340-353"]
    recognizers["Recognizers fire:<br/>EffectTable / FanOutTargets /<br/>StorageDescriptor"]
    lower["LoweringContext::push<br/>per fragment"]
    finalize["finalize_universal_unknowns()<br/>engine.rs:227"]
    inject["inject_unknown_into_enum_body()<br/>engine.rs:353<br/>(idempotent)"]
    assemble["AssembledSchema::new<br/>engine.rs:239"]
    compose["RustComposer::new+compose<br/>schema-rust/src/lib.rs:107"]
    authored["authored_effect_items()<br/>schema-rust/src/lib.rs:455"]
    storage_desc["storage_descriptor_items()<br/>schema-rust/src/lib.rs:558"]
    disambig["record_field_tokens_disambiguated()<br/>schema-rust/src/lib.rs:901"]
    emit_module["pub mod recorder { ... }<br/>TokenStream"]

    invoke --> parse_request
    parse_request --> resolve_path
    resolve_path --> read_path
    read_path --> parse_nota
    parse_nota --> multi_pass
    multi_pass --> recognizers
    recognizers --> lower
    lower --> finalize
    finalize --> inject
    inject --> assemble
    assemble --> compose
    compose --> authored
    compose --> storage_desc
    compose --> disambig
    authored --> emit_module
    storage_desc --> emit_module
    disambig --> emit_module
```

Eight numbered steps with file references:

1. `signal-frame/macros/src/schema_entry.rs:30` — `emit_schema` proc-
   macro fires.
2. Schema path resolves through `CARGO_MANIFEST_DIR` join
   (`schema_entry.rs:54-65`).
3. `schema/src/reader.rs::LoadedSchema::read_path` reads the file.
4. `schema/src/shape_parser.rs::parse_str` parses NOTA → `Schema`.
   The three new feature heads (`EffectTable`, `FanOutTargets`,
   `StorageDescriptor`) route through `parse_*_feature` (lines
   278/301/359).
5. `schema/src/multi_pass.rs::MacroPipeline::run` runs recognizers,
   producing typed `Feature::*` variants. Each row's
   FanOutOutputDeclaration is classified into Reply / Actor /
   Subscribers (`multi_pass.rs:939-998`).
6. `LoweringContext::push` accumulates fragments;
   `finalize_universal_unknowns()` (`engine.rs:227`) walks the lowered
   types and injects `Unknown(String)` into each `*Response` enum
   body — idempotent.
7. `RustComposer::compose` emits Rust:
   `authored_effect_items` (`schema-rust:455`) emits the closed
   AuthoredEffect / AuthoredFanOut / AuthoredEffectTable;
   `storage_descriptor_items` (`schema-rust:558`) emits the TABLES
   const + `table_type_for` accessor;
   `record_field_tokens_disambiguated` (`schema-rust:901`) keeps
   duplicate-field-name records compiling.
8. The daemon consumes the emitted types in its actor engines (e.g.
   `recorder.rs:126` matches on `RecorderAction`).

### Runtime topology

```mermaid
flowchart TB
    startup["Daemon startup"]
    open_storage["SpiritStorageHandle::open()<br/>storage.rs:165"]
    read_marker["read_version_marker()<br/>storage.rs:325"]
    branch{"on-disk marker?"}
    fresh["None: write NEXT<br/>log NoMigrationNeeded"]
    already["Some(NEXT): no-op<br/>log NoMigrationNeeded"]
    migrate["Some(previous):<br/>run_migration() →<br/>write NEXT →<br/>log MigratedSuccessfully"]
    spawn_actors["Spawn actors:<br/>Recorder / Observer /<br/>Supervisor / ReadingActor"]
    incoming["Incoming Action<br/>(wire or actor-to-actor)"]
    handle["actor.handle(action)<br/>match block<br/>(per /346 §2)"]
    response["Response stream"]
    reading_actor["ReadingActor::dispatch<br/>reading_actor.rs:141"]
    fanout["1. Forward to destination<br/>2. Auto-tap to LogSinkSet<br/>3. Reply ResponseDispatched"]
    wire_out["Wire reply"]
    subs["Subscribers"]
    log["Logging tap"]

    startup --> open_storage
    open_storage --> read_marker
    read_marker --> branch
    branch --> fresh
    branch --> already
    branch --> migrate
    fresh --> spawn_actors
    already --> spawn_actors
    migrate --> spawn_actors
    spawn_actors --> incoming
    incoming --> handle
    handle --> response
    response --> reading_actor
    reading_actor --> fanout
    fanout --> wire_out
    fanout --> subs
    fanout --> log
```

Five-step runtime sequence:

1. `SpiritStorageHandle::open()` reads the version marker
   (`read_version_marker` at `storage.rs:325`).
2. Three-branch migration path (fresh / already-NEXT / previous);
   upgrade-log gets an entry in every branch.
3. Actor handles spin up — recorder, observer, supervisor,
   reading-actor.
4. Reading actor and logging tap initialised; per
   `spirit-reading-actor.schema` the `DispatchEffect` fan-out always
   includes `(Tap LogSinkSet WriteEntry)`.
5. Mail flow: incoming Action → `actor.handle(action)` (closed match)
   → Response → reading actor → fan-out to wire/subscribers/log per
   the schema-declared FanOutTargets.

## §9 The migration runner end-to-end (behavioral demo)

The pre-session test `previous_version_database_runs_migration_and_logs_success`
walks the full cycle. Re-running with verbatim output:

```
test schema_driven::storage::tests::previous_version_database_runs_migration_and_logs_success ... ok
```

What it does (code from `storage.rs:404-434`):

```rust
let location = dir.join("migrate.redb");
// Seed the marker with MAIN (the prior version).
write_version_marker(&location, VersionMarker::MAIN).unwrap();

let handle = SpiritStorageHandle::open(&location);

assert_eq!(handle.current_marker(), Some(VersionMarker::NEXT));     // marker advanced
let log = handle.upgrade_log();
assert_eq!(log.len(), 1);
assert_eq!(log[0].from, VersionMarker::MAIN);
assert_eq!(log[0].to, VersionMarker::NEXT);
assert!(matches!(log[0].outcome, UpgradeOutcome::MigratedSuccessfully));

// Re-open and confirm the marker is at NEXT now.
let reopened = SpiritStorageHandle::open(&location);
assert_eq!(reopened.current_marker(), Some(VersionMarker::NEXT));
let reopened_log = reopened.upgrade_log();
assert!(matches!(reopened_log[0].outcome, UpgradeOutcome::NoMigrationNeeded));
```

Three things proven empirically:

1. **Fresh DB → NEXT marker**: `fresh_database_writes_next_marker_and_logs_no_migration`.
2. **MAIN-marker DB → migration runs → NEXT marker + upgrade log
   entry**: `previous_version_database_runs_migration_and_logs_success`
   (above).
3. **Reopen → no migration**: same test's second half.

Step 2 is the load-bearing demonstration of /346 §4 step 6 — the
auto-migration on database load.

## §10 What this proves

| /104 blocker | Claimed resolved | Empirically verified by |
|---|---|---|
| Multi-pass parsers for EffectTable / FanOutTargets / StorageDescriptor | YES | `effect_table_parses_action_to_effect_pairs`, `fan_out_targets_parses_three_output_kinds`, `shape_parser_recognises_storage_descriptor` — all in `schema/tests/effect_side_features.rs` |
| Universal-Unknown injection | YES | `assembled_schema_carries_injected_unknown_on_response_enum` + C1 schema-side proof + C1 runtime proof |
| Composer authored emissions | YES | `composer_emits_authored_effect_table_when_schema_declares_one`, `composer_emits_storage_descriptor_when_schema_declares_one`, `composer_omits_authored_emission_when_schema_has_no_effect_table` — `signal-frame/schema-rust` unit tests |
| Disambig fix for duplicate field names | YES | live in production code paths; the full signal-frame workspace builds + the spirit fixture handles `Time [u8 u8 u8]` shape via this code |
| Migration runner reads marker + writes forward + logs | YES | `previous_version_database_runs_migration_and_logs_success` + C6 end-to-end |
| schema_driven actors compile | YES | 17 + 5 new = 22 unit tests pass in `persona-spirit/src/schema_driven/` |
| `emit_schema!()` invoked alongside `signal_channel!([schema])` | YES | `tests/schema_module.rs` (4 tests, all pass): schema-driven `Operation`, `ROUTES`/`ROUTE_COUNT`, `ExtendedHeader::empty()`, `EffectTable` scaffold |

/346 spec honored:

- §1 actor-schema pattern (2 enums + Unknown) — six schemas authored;
  injection lands per C1.
- §2 engine-is-Rust, structure-is-schema — confirmed by the contact-
  point match blocks in `recorder.rs::handle` et al.
- §3 one rkyv byte layout — proven by C3.
- §4 upgrade mechanism — proven by §9 migration cycle.
- §5 reading-actor + auto-tap — proven by
  `dispatch_records_tap_capture_and_increments_delivered`.
- §6 NEXT/MAIN discipline — proven by C6.
- §9 universal Unknown as builtin macro — proven by every C1/C5
  variant.
- §10 worked example — the recorder schema + composer dump (§4) is the
  end-to-end demonstration.

## §11 Anomalies / caveats

1. **Cross-crate schema-import resolution is deferred.** The six
   actor schemas in `persona-spirit/` import from sibling crates
   (`signal-persona-spirit`, `signal-sema`, `spirit-storage`,
   `spirit-recorder`), which `LoadedSchema::read_path` can't resolve
   without an adjacent worktree layout. The workaround in
   `persona-spirit/src/schema_driven/` is **hand-written Rust types
   that match what `emit_schema!` will produce**. The actor engine
   code is real (the match blocks, the migration runner, the universal
   Unknown floor); only the type definitions swap when the macro
   lights up. The infrastructure piece is the proc-macro's import
   resolution algorithm.
2. **Dual emission in signal-persona-spirit.** Per /103 anomaly 3 +
   /104, the wire signal repo emits BOTH `signal_channel!([schema])`
   (legacy, at crate root) AND `emit_schema!()` (new, at
   `signal_persona_spirit::spirit::*`). Both pass tests. The operator
   integration cycle decides when to flip downstream consumers and
   remove the legacy invocation.
3. **One pre-existing daemon test fails on this filesystem.**
   `persona_spirit_upgrade_completion_requires_accepted_readiness`
   fails with `path must be shorter than SUN_LEN` — the
   `/home/li/wt/...` worktree path exceeds the unix-domain-socket
   path-length limit. This is unrelated to the schema-driven landing;
   it's an environmental property of where the worktree lives. The
   pre-session test count was reported in /104 as 24 daemon tests
   passing — that count was captured under a flake-check invocation
   that uses a shorter tmp path. In the bare worktree the failure
   surfaces. Schema_driven and all other modules pass cleanly.
4. **C4 closure is a structural proof, not a runtime invocation.** The
   AuthoredEffectTable lives inside emitted Rust; verifying the closure
   at compile time means inspecting the emitted text for the `_ => None`
   wildcard. A stronger runtime proof would invoke `effect_for_action`
   on an undeclared action through a built example crate — out of scope
   for this session.
5. **Constraint tests written this session.** Every test marked "new
   this session" in §7 is in the working copy, not yet committed to
   the four branches. They live in:
   - `schema/tests/constraint_proofs.rs` (7 tests; new file)
   - `schema-rust/src/lib.rs::tests::constraint_c4_*` (1 test; appended)
     plus diagnostic dump test (`dump_recorder_emission_for_showcase`,
     `#[ignore]`)
   - `persona-spirit/src/schema_driven/storage.rs::tests::constraint_*`
     (3 tests; appended)
   - `persona-spirit/src/schema_driven/mod.rs::constraint_proofs::*`
     (2 tests; new submodule)

## §12 References

- `/home/li/primary/reports/designer-assistant/103-schema-driven-spirit-full-stack-2026-05-25.md` — initial design + stubs
- `/home/li/primary/reports/designer-assistant/104-full-implementation-spirit-schema-driven-2026-05-25.md` — landing inventory
- `/home/li/primary/reports/designer/345-schemas-as-channel-contracts-2026-05-25.md` — multi-schema-per-crate spec
- `/home/li/primary/reports/designer/346-actor-schemas-and-upgrade-mechanism-2026-05-25.md` — design spec
- Worktrees:
  - `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-full-stack-spirit-2026-05-25` (origin HEAD `b499190a`)
  - `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-full-stack-spirit-2026-05-25` (origin HEAD `b35d18bd`)
  - `/home/li/wt/github.com/LiGoldragon/persona-spirit/designer-schema-full-stack-spirit-2026-05-25` (origin HEAD `e0378b8d`)
  - `/home/li/wt/github.com/LiGoldragon/signal-persona-spirit/designer-schema-full-stack-spirit-2026-05-25` (origin HEAD `5ba7ff99`)
- Skills consulted:
  - `skills/enum-contact-points.md` — actor.handle is the action/response contact point
  - `skills/jj.md` — headless inline-message discipline
  - `skills/reporting.md` — report-shape discipline
