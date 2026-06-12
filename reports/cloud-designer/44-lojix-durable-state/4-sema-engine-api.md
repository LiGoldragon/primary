# sema-engine API — concrete calls to back lojix's four tables durably

Recon for replacing lojix's `Mutex<StoreState>` with a redb-backed
`sema-engine::Engine` plus self-resume on restart. Everything below is
read from `/git/github.com/LiGoldragon/sema-engine` at head change
`ryrknxwspsky` (working copy on top of `kzyyoukzlxry` "add opt-in
versioned state log"), version `0.2.3`
(`sema-engine/Cargo.toml:3`).

## What sema-engine is

A typed database-operation engine composed over the `sema` storage
kernel (`sema-engine/src/lib.rs:1-6`). `sema` is "Typed,
version-guarded database kernel over redb and rkyv"
(`sema/Cargo.toml` description; `redb = "4"` at line 11). So the durable
backing is redb-on-disk; sema-engine adds the catalog, commit log,
counters, subscriptions, and the typed assert/mutate/match/retract
verbs. Record values are any rkyv-archivable type (the
`EngineStoredValue` blanket impl, `record.rs:80-106`).

## Open a redb-backed engine at a path

`EngineOpen` is the one-arg open request; `Engine::open` consumes it
(`engine.rs:1358-1390`, `engine.rs:50-64`):

```rust
pub struct EngineOpen { path: PathBuf, schema: Schema, versioning_policy: Option<VersioningPolicy> }
impl EngineOpen {
    pub fn new(path: impl Into<PathBuf>, version: SchemaVersion) -> Self;
    pub fn with_versioning(mut self, policy: VersioningPolicy) -> Self;   // opt-in versioned log
}
pub fn Engine::open(request: EngineOpen) -> Result<Self>;
```

`Engine::open` calls `sema::Sema::open_with_schema(path, schema)`
(`engine.rs:51`; kernel signature `sema/src/lib.rs:480`), then rebuilds
the in-memory `Catalog` by iterating the persisted `__sema_engine_catalog`
table (`engine.rs:52-57`). `SchemaVersion::new(u32)` is const
(`sema/src/lib.rs` SchemaVersion block); the kernel hard-fails on schema
mismatch (no silent migration). Test fixture opens with
`EngineOpen::new(path, SchemaVersion::new(1))`
(`tests/engine.rs:67-69`).

## Register record families / tables

Two flavors, both on `&mut Engine` (`engine.rs:66-98`). Idempotent —
re-registering an already-cataloged name is a no-op that still hands back
a typed `TableReference`, which is exactly what reopen needs:

```rust
// String-keyed family (key = record's own RecordKey, via EngineRecord)
pub fn register_table<RecordValue>(&mut self, descriptor: TableDescriptor<RecordValue>)
    -> Result<TableReference<RecordValue>>;
// Auto-incrementing u64-identified family (engine assigns RecordIdentifier)
pub fn register_identified_table<RecordValue>(&mut self, descriptor: IdentifiedTableDescriptor<RecordValue>)
    -> Result<IdentifiedTableReference<RecordValue>>;
```

`TableDescriptor::new(TableName::new("toy_records"))` declares a family;
`TableName::new(&'static str)` is const (`table.rs:11`,
`table.rs:36-42`). `TableReference` is `Copy` and carries
`PhantomData<RecordValue>` (`table.rs:62-66,132-138`). `Catalog` is just
`Vec<TableRegistration>`; `TableRegistration { table_name: String }`
(`catalog.rs:5-56`). Registration writes the catalog row (and, for
identified tables, seeds the per-table `…:next_record_identifier`
counter at 1 — `engine.rs:84-95`, `table.rs:19-21`).

## Typed write (assert / mutate / retract)

All writes take `&self` (interior-mutable through the kernel), assign a
`CommitSequence` + `SnapshotIdentifier`, write the record, append a
`CommitLogEntry`, bump `__sema_engine_counters`, and (when versioning is
on) append a `VersionedCommitLogEntry` — all inside one
`storage.write` redb transaction (`engine.rs:325-403` for `assert_keyed`,
the canonical path). Key entry points (`engine.rs:307,325,405,423,503,585`):

```rust
pub fn assert<RV: EngineStoredRecord …>(&self, Assertion<RV>) -> Result<MutationReceipt>;
pub fn assert_keyed<RV>(&self, KeyedAssertion<RV>) -> Result<MutationReceipt>;  // dup key => DuplicateAssertKey
pub fn mutate<RV>(&self, Mutation<RV>) -> Result<MutationReceipt>;
pub fn mutate_keyed<RV>(&self, KeyedMutation<RV>) -> Result<MutationReceipt>;
pub fn retract<RV>(&self, Retraction<RV>) -> Result<MutationReceipt>;
pub fn commit<RV>(&self, CommitRequest<RV>) -> Result<CommitReceipt>;            // multi-op atomic batch
// identified variants:
pub fn assert_identified<RV>(&self, IdentifiedAssertion<RV>) -> Result<IdentifiedMutationReceipt>;
pub fn mutate_identified / retract_identified … -> Result<IdentifiedMutationReceipt>;
```

`CommitRequest::new(table).assert(rec).mutate(rec).retract(key)` builds a
batch that commits as one transaction (`mutation.rs:315-355`,
"atomicity is structural via the NonEmpty operations list",
`log.rs:9-13`). `MutationReceipt` exposes `commit_sequence()`,
`snapshot()`, `database_marker()` (`mutation.rs:90-130`).
`WriteOperation::operation()` maps to `signal_sema::SemaOperation`
(`Assert`/`Mutate`/`Retract`/`Match`, the operation vocabulary —
`signal-sema/src/operation.rs:19-27`, version `0.2.0`).

## Typed read (match)

```rust
pub fn match_records<RV: EngineStoredValue>(&self, QueryPlan<RV>) -> Result<QuerySnapshot<RV>>;
pub fn match_identified<RV>(&self, IdentifiedQueryPlan<RV>) -> Result<IdentifiedQuerySnapshot<RV>>;
```

Plan constructors: `QueryPlan::all(table)`, `QueryPlan::key(table, RecordKey)`,
`QueryPlan::key_range(table, KeyRange)`, plus `filtered/constrain/project/aggregate`
(`query.rs:25-74`). `QuerySnapshot::records() -> &[RV]`, `.snapshot()`,
`.database_marker()` (`query.rs:525-559`). `ReadPlanNode` variants
implemented: `AllRows`, `ByKey`, `ByKeyRange` (`query.rs:333-336`,
`engine.rs:788-834`); richer operators return `UnsupportedReadPlan`
(`error.rs:35-36`).

## Commit log + resume from persisted state

There is no explicit "resume" call — `Engine::open` IS the resume.
Every counter and table lives in redb, so reopening the same path
reconstructs the catalog from `__sema_engine_catalog` and reads
`latest_commit_sequence` / `latest_snapshot` straight from
`__sema_engine_counters` (`engine.rs:50-64,957-984`). The reopen test
`engine_reopens_registered_catalog_and_matches_existing_records`
(`tests/engine.rs:204-232`) reopens, re-registers (idempotent), and
matches a record asserted in the prior process;
`identified_record_counter_survives_reopen_and_retract_advances_sequence`
(`tests/engine.rs:329`) proves the auto-id counter survives. Log / state
read API (`engine.rs:957-1032`):

```rust
pub fn latest_snapshot(&self) -> Result<SnapshotIdentifier>;
pub fn current_commit_sequence(&self) -> Result<CommitSequence>;
pub fn current_database_marker(&self) -> Result<DatabaseMarker>;
pub fn commit_log(&self) -> Result<Vec<CommitLogEntry>>;
pub fn versioned_commit_log(&self) -> Result<Vec<VersionedCommitLogEntry>>;
pub fn replay_from_sequence(&self, start: CommitSequence) -> Result<Vec<CommitLogEntry>>;
pub fn versioned_replay_from_sequence(&self, start: CommitSequence) -> Result<Vec<VersionedCommitLogEntry>>;
pub fn commit_log_range(&self, range: SequenceRange) -> Result<Vec<CommitLogEntry>>;
pub fn subscription_registrations(&self) -> Result<Vec<SubscriptionRegistration>>;  // subscriptions persist too
```

`CommitLogEntry { commit_sequence, snapshot, operations: NonEmpty<CommitLogOperation> }`
(`log.rs:14-19`); each op carries `SemaOperation` + `table_name` +
`Option<RecordKey>` (`log.rs:63-68`). The opt-in `versioning::*` surface
adds a hash-chained, payload-carrying log:
`VersionedCommitLogEntry` chains `previous_entry_digest` → `entry_digest`
(blake3) and embeds the rkyv record bytes as `VersionedPayload::Record{bytes}`
or `Tombstone` (`versioning.rs:96-296`); enabled via
`EngineOpen::with_versioning(VersioningPolicy::new(VersionedStoreName, SchemaHash))`,
`SchemaHash::for_label(label)` (`versioning.rs:7-70`).

## Mapping lojix's four tables onto Catalog registrations

lojix today holds `StoreState { live_set, gc_roots, event_log, containers,
+ 4 sequence counters } behind Mutex` (`lojix/src/lib.rs:142-251`); the
four table fields are newtypes over `Vec<Element>`
(`lojix/src/schema/sema.rs:259,278,295,317`). The engine's own
`__sema_engine_counters` already tracks `commit_sequence`/`snapshot`, so
those two of lojix's four counters are subsumed; the deployment /
generation id counters map to `register_identified_table`'s auto-id
counter (or stay as dedicated rows). Each lojix table becomes one
registered record family keyed per element rather than one blob:

| lojix field (newtype) | element record type | suggested registration |
|---|---|---|
| `LiveSetTable(Vec<LiveGeneration>)` | `LiveGeneration` | `register_identified_table::<LiveGeneration>("live_set")` (generation id is the auto-counter) |
| `GcRootsTable(Vec<GcRoot>)` | `GcRoot` | `register_table::<GcRoot>("gc_roots")` (string-keyed via `EngineRecord`) |
| `EventLogTable(Vec<EventLogEntry>)` | `EventLogEntry` | `register_identified_table::<EventLogEntry>("event_log")` (append-only, position = id) |
| `ContainerLifecycleTable(Vec<ContainerLifecycleRecord>)` | `ContainerLifecycleRecord` | `register_table::<ContainerLifecycleRecord>("containers")` |

Each element type needs the rkyv derive set (already present in
`schema/sema.rs`) and an `impl EngineRecord { fn record_key(&self) -> RecordKey }`
for the string-keyed ones (`record.rs:76-78`). `Engine` replaces the
`Mutex<StoreState>`: `Engine` holds `sema::Sema` (its own redb txn lock),
so the `Mutex` and the hand-rolled `next_*_sequence` helpers
(`lib.rs:172-225`) drop out in favor of the engine's commit-sequenced
writes and `register_identified_table` counters.

## Dependency to add

lojix's `Cargo.toml` does not yet depend on sema-engine. Add, matching
sema-engine's own git-branch convention (it pins sibling crates by
`branch = main`, `sema-engine/Cargo.toml:18-20`):

```toml
sema-engine = { git = "https://github.com/LiGoldragon/sema-engine.git", branch = "main" }
```

`signal-sema` (for `SemaOperation` in any log inspection) and `sema`
(`SchemaVersion`, kernel error) come in transitively through
sema-engine's re-exports (`lib.rs:39-58`), so a direct add is only needed
if lojix names those types itself. lojix already carries a compatible
rkyv pin (`0.8`, same feature set — `lojix/Cargo.toml` vs
`sema-engine/Cargo.toml:2`), so no rkyv conflict.
