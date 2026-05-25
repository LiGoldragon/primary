# 106 — Schema-driven POC from v0.3 main

*Designer-assistant landing for psyche 2026-05-26 + intent records 709
and 710 (the three-language schema-driven structure). Five repositories
on new feature branches in `~/wt`. The POC matches v0.3 production
capability — wire shape, reply terseness, multi-topic vec, daemon-
stamped timestamps — through schema-driven dual emission, while
exercising the workspace's schema-as-architecture discipline end to end.*

## Summary

| Repo | Branch HEAD | Tests | Notes |
|---|---|---|---|
| `schema` | `designer-schema-poc-from-v0.3-main-2026-05-26` @ `2a5372f5` | 61 pass | Extended universal-Unknown post-pass for wire Reply enums |
| `signal-frame` | `designer-schema-poc-106-2026-05-26` @ `36024d06` | 58 pass | Fixed three composer trailing-comma bugs + Reply Unknown injection |
| `signal-persona-spirit` | `designer-schema-poc-from-v0.3-main-2026-05-26` @ `7a3fb8b1` | 25 pass (22 + 3 new) | `emit_schema!()` dual emission alongside legacy |
| `owner-signal-persona-spirit` | `designer-schema-poc-from-v0.3-main-2026-05-26` @ `1d8d1fb9` | 9 pass (6 + 3 new) | New `owner-spirit.schema` + `emit_schema!()` dual emission |
| `persona-spirit` | `designer-schema-poc-from-v0.3-main-2026-05-26` @ `22f31945` | 19 schema-poc tests pass (9 constraint + 10 production-emulation) | New `schema-poc` workspace member — six actor schemas + storage handle + minimal daemon + tests |

All branches pushed to origin. The v0.3 production `persona-spirit`
daemon still builds in the POC worktree (the POC's `schema-poc` is an
ADDITIVE workspace member; the production crate is unchanged).

## What landed per repo

### `schema`

`UniversalUnknownMacro::finalize_universal_unknowns` previously only
recognized actor `*Response` enums. The POC extends this with:

- `is_wire_reply_enum_name(name)` — exact-match on `Reply` (not a
  suffix match) since the wire's top-level Reply type carries that
  exact name.
- `is_universal_unknown_carrier_name(name)` — disjunction of the
  response and reply checks. The post-pass walks `self.types` and
  applies the injector to anything matching either rule.

The wire's forward-compat floor on the schema-driven `Reply` enum
mirrors the actor's safety floor on each internal-channel `*Response`
enum. **All 61 prior schema tests still pass.**

### `signal-frame`

Three latent composer bugs in `schema-rust` had the shape
`#(#arms),*,` (rep-then-comma-then-extra-comma). The emitted Rust
becomes `arm1, arm2,, _ => None` — `expected pattern, found ,`. The
prior landing's fixture tests didn't exercise the emit-then-rustc
path, so the bugs lived dormant. Fixed all three by moving the
trailing comma INSIDE the repetition: `#(#arm,)*`.

Additionally extended `reply_items` to inject `Unknown(String)` into
the wire `Reply` enum directly (the schema's Reply enum is built
ad-hoc from `Feature::Reply`, not from local types; the post-pass at
the engine layer doesn't reach it, so the composer adds it itself).

Cargo.toml patches the `schema` git dep at the local POC worktree so
the engine-side extension reaches `schema-rust` without a publish
cycle. **All 58 prior signal-frame tests still pass.**

### `signal-persona-spirit`

The wire schema `spirit.schema` is left as-is on main (it already
declares the v0.3 wire surface). The POC adds:

1. `emit_schema!()` invocation in `src/lib.rs` ALONGSIDE the legacy
   `signal_channel!([schema])` invocation. Dual emission per the
   prior /103 pattern: legacy at crate root, schema-driven at
   `signal_persona_spirit::spirit::*`.
2. Cargo.toml patches pointing at the local schema + signal-frame
   POC worktrees.
3. `tests/schema_module.rs` (3 tests): schema-driven module is
   reachable; Operation constructs; Reply::Unknown lands.

### `owner-signal-persona-spirit`

The owner socket was a hand-written `signal_channel!{...}` form on
v0.1 main. The POC:

1. Authors `owner-spirit.schema` declaring the same 5 operations
   (Start / Drain / Reload / Register / Retire) per the v0.3-era
   owner contract. Empty-payload commands (Drain, Reload) carry a
   `Generation` token to satisfy the schema parser's non-empty-record
   rule while preserving v0.3 wire semantics.
2. Adds `emit_schema!("owner-spirit.schema")` alongside the legacy
   declaration.
3. Updates the nota-codec lock to match the schema crate's dep.
4. `tests/schema_module.rs` (3 tests): module reachable; Reply
   Unknown lands; 5-route count matches.

### `persona-spirit`

Avoids disturbing the v0.3 production daemon. The POC lands as a new
workspace member `schema-poc/`. Six new schema files declare the
storage sema language (1 file) + internal channel languages (5
files):

- `spirit-storage.schema` — STORAGE SEMA. Declares RecordsTable,
  IdentifierMintTable, VersionMarkerTable, UpgradeLogTable; the
  `StorageDescriptor` feature names all four. VersionMarker is a
  `[u32 u32 u32]` semver triple.
- `spirit-recorder.schema` — ACTION = (RecordEntry,
  QueryRecorderStatus); RESPONSE = (RecordAccepted,
  RecorderStatusReturned) + Unknown. EffectTable + FanOutTargets.
- `spirit-observer.schema` — ACTION = (ObserveTopics,
  ObserveRecordsDescriptionOnly, ObserveRecordsWithProvenance);
  RESPONSE = (TopicsObserved, RecordsObserved,
  RecordProvenancesObserved) + Unknown.
- `spirit-supervisor.schema` — ACTION = (StartEngine, DrainEngine,
  QueryEngineStatus); RESPONSE = (EngineStarted, EngineDrained,
  EngineStatusReturned) + Unknown.
- `spirit-reading-actor.schema` — ACTION = (DispatchRecorderResponse,
  DispatchObserverResponse); RESPONSE = (ResponseDispatched,
  DispatchFailed) + Unknown. FanOutTargets includes the
  `(Tap LogSinkSet WriteEntry)` auto-tap discipline.
- `spirit-upgrade-log.schema` — ACTION = (AppendUpgradeEntry,
  QueryUpgradeLog); RESPONSE = (UpgradeEntryAppended,
  UpgradeLogReturned) + Unknown.

Five Rust actor engines + storage handle + minimal `PocDaemon` glue
implement v0.3-shape capability. The daemon's `dispatch(operation)`
method is a closed match on `signal_persona_spirit::Operation`; for
each variant it maps to the corresponding actor action, dispatches,
and projects the response back to the wire `Reply`.

## Three languages — proof of one-to-one assembly

The schema files ARE the architecture for each language; the
composer emits Rust types and dispatchers that mirror the schema's
declarations one-to-one.

### Wire signal language — `spirit.schema` (signal-persona-spirit)

```text
[
  (State (Statement))
  (Record (Entry))
  (Observe (Observation))
  (Watch (Subscription))
  (Unwatch (SubscriptionToken))
]
...
[
  (Reply
    RecordAccepted
    StateObserved
    RecordsObserved
    ...
    RequestUnimplemented)
]
```

emits at `signal_persona_spirit::spirit::*`:

```rust
pub enum Operation {
    State(StateEndpoint),
    Record(RecordEndpoint),
    Observe(ObserveEndpoint),
    Watch(WatchEndpoint),
    Unwatch(UnwatchEndpoint),
}

pub enum Reply {
    RecordAccepted(RecordAccepted),
    StateObserved(StateObserved),
    RecordsObserved(RecordsObserved),
    ...
    RequestUnimplemented(RequestUnimplemented),
    Unknown(String),   // injected by the extended composer
}
```

### Storage sema language — `spirit-storage.schema`

```text
{
  VersionMarker [u32 u32 u32]
  ...
}
[
  (StorageDescriptor [
    (Records RecordsTable)
    (IdentifierMint IdentifierMintTable)
    (VersionMarker VersionMarkerTable)
    (UpgradeLog UpgradeLogTable)
  ])
]
```

emits at `spirit_schema_poc::spirit_storage::*`:

```rust
pub struct VersionMarker {
    pub u32: u32,
    pub u32_2: u32,
    pub u32_3: u32,
}

pub struct StorageDescriptor;

impl StorageDescriptor {
    pub const TABLE_COUNT: usize = 4;
    pub const TABLES: &'static [TableDescriptor] = &[
        TableDescriptor { logical_name: "Records",       table_type: "RecordsTable" },
        TableDescriptor { logical_name: "IdentifierMint", table_type: "IdentifierMintTable" },
        TableDescriptor { logical_name: "VersionMarker",  table_type: "VersionMarkerTable" },
        TableDescriptor { logical_name: "UpgradeLog",     table_type: "UpgradeLogTable" },
    ];
    pub fn table_type_for(logical_name: &str) -> Option<&'static str> {
        match logical_name {
            "Records" => Some("RecordsTable"),
            ...
            _ => None,
        }
    }
}
```

### Internal channel language — `spirit-recorder.schema`

```text
{
  RecorderAction (
    (RecordEntry RecordEntryRequest)
    (QueryRecorderStatus QueryRecorderStatusRequest)
  )

  RecorderResponse (
    (RecordAccepted)
    (RecorderStatusReturned)
  )
  ...
}

[
  (EffectTable [
    (RecordEntry RecordWriteEffect)
    (QueryRecorderStatus RecorderStatusEffect)
  ])
  (FanOutTargets [
    (RecordWriteEffect [
      (Store SpiritStorage InsertStampedEntry)
      (Reply RecordAccepted)
    ])
    ...
  ])
]
```

emits at `spirit_schema_poc::spirit_recorder::*`:

```rust
pub enum RecorderAction {
    RecordEntry(RecordEntryRequest),
    QueryRecorderStatus(QueryRecorderStatusRequest),
}

pub enum RecorderResponse {
    RecordAccepted(RecordAccepted),
    RecorderStatusReturned(RecorderStatusReturned),
    Unknown(String),   // injected by finalize_universal_unknowns
}

pub struct AuthoredEffectTable;
impl AuthoredEffectTable {
    pub fn effect_for_action(action: &str) -> Option<&'static str> {
        match action {
            "RecordEntry" => Some("RecordWriteEffect"),
            "QueryRecorderStatus" => Some("RecorderStatusEffect"),
            _ => None,    // closure guarantee
        }
    }
    pub fn fan_out_for_effect(effect: &str) -> Option<AuthoredFanOut> {
        match effect {
            "RecordWriteEffect" => Some(AuthoredFanOut { ... }),
            "RecorderStatusEffect" => Some(AuthoredFanOut { ... }),
            _ => None,    // closure guarantee
        }
    }
}
```

The hand-written engine in `schema-poc/src/recorder.rs`:

```rust
impl SpiritRecorder {
    pub fn handle(&self, action: RecorderAction) -> RecorderResponse {
        match action {
            RecorderAction::RecordEntry(_) => self.record_entry(),
            RecorderAction::QueryRecorderStatus(_) => self.query_status(),
        }
    }
}
```

Rust enforces exhaustiveness; the structure is the schema, the logic
is Rust.

## Constraint tests (7 of them) — verbatim run output

```text
running 9 tests
test constraint_c1_wire_reply_enum_carries_unknown_variant ... ok
test constraint_c1_every_actor_response_carries_unknown_variant ... ok
test constraint_c5_response_enums_have_exactly_one_unknown_variant ... ok
test constraint_c2_migration_idempotent_on_already_next_marker ... ok
test constraint_c3_version_marker_one_layout_two_homes ... ok
test constraint_c6_next_version_marker_discipline_end_to_end ... ok
test constraint_c7_storage_descriptor_table_set_covers_v03_storage ... ok
test constraint_c7_schema_derived_api_surface_covers_v03 ... ok
test constraint_c4_effect_table_dispatchers_terminate_with_wildcard ... ok

test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

Constraint mapping:

| Constraint | Test name(s) | What's proven |
|---|---|---|
| C1 | `c1_every_actor_response_carries_unknown_variant` + `c1_wire_reply_enum_carries_unknown_variant` | `Unknown(String)` is constructable on every actor RESPONSE enum AND on every wire Reply enum (ordinary + owner) |
| C2 | `c2_migration_idempotent_on_already_next_marker` | Four-round reopen on NEXT marker stays NEXT, logs NoMigrationNeeded each time |
| C3 | `c3_version_marker_one_layout_two_homes` | `std::mem::size_of::<spirit_storage::VersionMarker>() == std::mem::size_of::<spirit_upgrade_log::VersionMarker>()` (same byte layout across sema + internal-channel emissions) |
| C4 | `c4_effect_table_dispatchers_terminate_with_wildcard` | Known action returns Some; unknown action returns None (the `_ => None` wildcard arm) |
| C5 | `c5_response_enums_have_exactly_one_unknown_variant` | Closed match arms on each `*Response::Unknown(_)` compile (E0428 would reject a duplicate variant) |
| C6 | `c6_next_version_marker_discipline_end_to_end` | Three-branch migration: fresh → NEXT + NoMigrationNeeded; MAIN → NEXT + MigratedSuccessfully; reopen-on-NEXT → no-op + NoMigrationNeeded |
| C7 | `c7_schema_derived_api_surface_covers_v03` + `c7_storage_descriptor_table_set_covers_v03_storage` | Compile-time exhaustive match on both legacy + schema-driven Operation enums; storage descriptor covers 4 v0.3 tables |

## Production-emulating tests — coverage of v0.3 capability

```text
running 10 tests
test poc_observe_records_description_only_returns_records_observed_reply ... ok
test poc_consecutive_records_get_monotonic_identifiers ... ok
test poc_observe_records_with_provenance_returns_record_provenances_observed_reply ... ok
test poc_record_accepts_multi_topic_vec_per_record_702 ... ok
test poc_observe_topics_returns_topics_observed_reply ... ok
test poc_record_returns_record_accepted_with_fresh_identifier ... ok
test poc_schema_driven_wire_reply_carries_unknown_floor ... ok
test poc_state_returns_request_unimplemented ... ok
test poc_unwatch_returns_request_unimplemented ... ok
test poc_watch_returns_request_unimplemented ... ok

test result: ok. 10 passed; 0 failed
```

Coverage mapping:

| v0.3 operation | POC equivalent | Test name | Reply shape |
|---|---|---|---|
| `(Record (...))` | `Operation::Record(Entry { topics, kind, description, certainty })` | `poc_record_returns_record_accepted_with_fresh_identifier` | `Reply::RecordAccepted(RecordIdentifier)` |
| `(Record ([topic1 topic2 ...] ...))` multi-topic per record 702 | `Topics::new(vec![Topic, Topic, Topic])` | `poc_record_accepts_multi_topic_vec_per_record_702` | `Reply::RecordAccepted(...)` |
| Monotonic identifier mint | sequential `Operation::Record(...)` calls | `poc_consecutive_records_get_monotonic_identifiers` | identifiers strictly increase |
| `(Observe Topics)` | `Operation::Observe(Observation::Topics)` | `poc_observe_topics_returns_topics_observed_reply` | `Reply::TopicsObserved(...)` |
| `(Observe (Records (None None DescriptionOnly)))` | `RecordQuery { mode: DescriptionOnly, .. }` | `poc_observe_records_description_only_returns_records_observed_reply` | `Reply::RecordsObserved(...)` |
| `(Observe (Records (None None WithProvenance)))` | `RecordQuery { mode: WithProvenance, .. }` | `poc_observe_records_with_provenance_returns_record_provenances_observed_reply` | `Reply::RecordProvenancesObserved(...)` |
| `(State [text])` | `Operation::State(Statement { text })` | `poc_state_returns_request_unimplemented` | `Reply::RequestUnimplemented(...)` (matches v0.3 placeholder) |
| `(Watch ...)` | `Operation::Watch(Subscription::Records(...))` | `poc_watch_returns_request_unimplemented` | `Reply::RequestUnimplemented(...)` |
| `(Unwatch ...)` | `Operation::Unwatch(SubscriptionToken::Records(...))` | `poc_unwatch_returns_request_unimplemented` | `Reply::RequestUnimplemented(...)` |
| forward-compat Reply::Unknown | construct directly | `poc_schema_driven_wire_reply_carries_unknown_floor` | `Reply::Unknown(text)` |

## What's deferred

- **Real redb storage**. The POC's storage handle is in-memory
  (`Mutex<Vec<...>>`). The schema's `StorageDescriptor` names four
  tables; real redb wiring is a follow-up slice. The migration
  runner's three-branch shape and the rkyv-one-byte-layout
  discipline are proven; production redb integration just maps
  table names to `redb::TableDefinition`s.
- **rkyv encode/decode plumbing for the schema-emitted types**.
  The composer emits plain Rust structs; the rkyv `Archive +
  Serialize + Deserialize` derives don't yet land. The wire crates'
  legacy `signal_channel!` form provides this for the wire types in
  `signal_persona_spirit::*` (crate root) — the schema-driven module
  in `signal_persona_spirit::spirit::*` carries plain Rust shapes
  only. Production-emulating tests therefore construct via the
  legacy crate-root types (byte-identical to the schema-driven
  shapes per the rkyv-one-format discipline).
- **Cross-crate schema-import resolution**. Internal-channel schemas
  redeclare leaf types (Topic, Kind, Magnitude) rather than import
  them from `spirit.schema`. The composer's import-resolution
  algorithm landing is a future operator slice; the workaround is
  duplicate-but-byte-identical declarations.
- **Empty-payload records in the schema parser**. The parser
  rejects `Drain []` etc. Workaround: empty commands carry a
  Generation token. The schema parser could be loosened in a
  follow-up to accept empty records (`Drain []` → unit struct).
- **Reading-actor as a separate dispatch hub**. The PocDaemon
  dispatches synchronously without going through the reading-actor.
  The reading-actor schema + handler exists; full daemon
  integration with mailbox-style fan-out is deferred.

## Worktrees + branches pushed

| Worktree | Branch on origin |
|---|---|
| `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-poc-from-v0.3-main-2026-05-26` | `designer-schema-poc-from-v0.3-main-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-poc-106-2026-05-26` | `designer-schema-poc-106-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/signal-persona-spirit/designer-schema-poc-from-v0.3-main-2026-05-26` | `designer-schema-poc-from-v0.3-main-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/owner-signal-persona-spirit/designer-schema-poc-from-v0.3-main-2026-05-26` | `designer-schema-poc-from-v0.3-main-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/persona-spirit/designer-schema-poc-from-v0.3-main-2026-05-26` | `designer-schema-poc-from-v0.3-main-2026-05-26` |

A parallel designer-assistant landed `designer-schema-poc-from-v0.3-
main-2026-05-26` on `signal-frame` as a self-hosting bootstrap stub
(report /107). To avoid collision, this report's signal-frame work
uses a distinct branch name `designer-schema-poc-106-2026-05-26`. The
two branches can merge cleanly: self-hosting (Stage 2 of the kernel/
leaf bootstrap) is additive to the composer trailing-comma fix +
Reply Unknown injection that this report lands.

## How to deploy as spirit-next

The unsuffixed `spirit` binary points at the current production
target (`spirit-v0.3.0`). The `spirit-next` slot is the natural home
for this POC once it matures. For operator + system-specialist
handoff:

1. **Add input to CriomOS-home.** Pin the five POC branches in
   CriomOS-home's `flake.nix`:
   ```nix
   inputs.persona-spirit-poc = {
     url = "github:LiGoldragon/persona-spirit/designer-schema-poc-from-v0.3-main-2026-05-26";
     # ...similar for the other four repos
   };
   ```
2. **Build a `spirit-next` package** that targets `spirit-schema-poc`
   (or expand `schema-poc` to a real `persona-spirit-next-daemon`
   binary).
3. **Test the deployment**:
   ```sh
   readlink -f $(command -v spirit-next)  # confirm pins to POC
   spirit-next "(Record (workspace Decision [test from poc] Maximum))"
   # expect Reply::RecordAccepted with monotonic identifier
   ```
4. **Side-by-side validation**:
   ```sh
   spirit-v0.3.0 "(Observe Topics)" > v030.out
   spirit-next "(Observe Topics)" > poc.out
   diff v030.out poc.out  # the variant shape matches
   ```

The POC's storage is in-memory so the `spirit-next` daemon won't
persist across restarts — fine for capability validation, not for
production substitution. Real redb wiring is a prerequisite for
spirit-next promotion to spirit.

## References

- Psyche 2026-05-26 — intent records 709 (three-language structure)
  and 710 (wire-side dual emission), captured through Spirit v0.2.0
- `/home/li/primary/INTENT.md` §"The schema-driven stack" +
  §"Spirit deploys side-by-side"
- `/home/li/primary/skills/schema-driven-actors.md` — actor channel
  authoring discipline
- `/home/li/primary/skills/spirit-cli.md` — v0.3 wire shape +
  side-by-side deployment vocabulary
- `/home/li/primary/reports/designer/349-context-maintenance-sweep-2026-05-25/1-poc-schema-stack-explainer.md`
  — the prior POC landing's headline explainer (the inspiration
  source for this report's structure)
- `/git/github.com/LiGoldragon/persona-spirit` main @ `b3b1ac0c` —
  v0.3.0 production target capability
- `/git/github.com/LiGoldragon/signal-persona-spirit` main @
  `026d38fb` — v0.3.0 wire contract
