# Ground: the sema-engine database engine (the genericity mechanism)

## What sema-engine is, concretely

`sema-engine` is a pure library: `Engine` composes one `sema::Sema` handle, a `Catalog`, and an in-process `SubscriptionRegistry` (`engine.rs:38-42`). No daemon, kameo, tokio, or NOTA — the crate doc and `ARCHITECTURE.md` are explicit that routing, sockets, auth, ordering, and human text are component responsibilities (`lib.rs:1-6`, `ARCHITECTURE.md:147-149`). A component links `Engine`, registers a record family, and dispatches typed requests into per-variant engine calls. This is the layer `spirit`, `mind`, `repository-ledger`, and `criome` build on.

The whole reusability question for the version-control library reduces to: **how does this crate stay generic over arbitrary record families without becoming a stringly-typed generic-record store?** The answer below is the central finding, because the VC capability has to thread the same needle.

## How genericity is achieved today

sema-engine uses **three layers of genericity, each with a different cost**, and the seam between them is exactly where a VC layer would have to insert itself.

### 1. The kernel is generic by Rust generics + a trait bound (clean, type-preserving)

`sema::Table<K, V>` is `const`-constructible and carries `PhantomData<K>` / `PhantomData<V>` (`sema/src/lib.rs:231-250`). The encode/decode bound lives on a second `impl` block requiring `V: Archive + Serialize<...> + V::Archived: Deserialize + CheckBytes` (`sema/src/lib.rs:345-353`). rkyv is hidden at the table boundary — callers see typed Rust values in and out. Critically, **sema declares no table list**: a table is identified by `(name, K, V)`, created lazily on first `get`/`insert`, and the schema declaration is just a `SchemaVersion` (`sema/src/lib.rs:166-204`, `480-508`). This is the genuinely generic, fully type-preserving layer.

sema-engine re-exports the same bound as two engine-local marker traits so consumers do not re-spell the rkyv where-clause:

```rust
// record.rs:80-106 — blanket impl: every rkyv-archivable Clone type qualifies
pub trait EngineStoredValue:
    Archive + Clone
    + for<'serialize> RkyvSerialize<Strategy<Serializer<AlignedVec, ArenaHandle<'serialize>, Share>, rancor::Error>>
where Self::Archived: RkyvDeserialize<Self, HighDeserializer<rancor::Error>>
    + for<'validation> CheckBytes<...> {}
```

`EngineStoredValue` is what binds the genericity: it is the storable-type contract, satisfied by a blanket impl over *any* `Archive + Clone` type. There is no enum of known record types — the type parameter `RecordValue` flows through every engine method (`engine.rs:60,94,276,528,681`) and reaches `sema::Table<String, RecordValue>` via `TableReference::sema_table()` (`table.rs:92-94`).

### 2. The record-family API is a phantom-typed handle, not a registry of types (type-preserving but the type only lives in the caller)

There is no `register_table(name, type)` that stores type information. Registration is two-step and the **type parameter is compile-time only**:

```rust
// engine.rs:60-72
pub fn register_table<RecordValue>(
    &mut self,
    descriptor: TableDescriptor<RecordValue>,
) -> Result<TableReference<RecordValue>>
```

`TableDescriptor<RecordValue>` is `{ name: TableName, record: PhantomData<RecordValue> }` (`table.rs:24-28`). `register_table` extracts `descriptor.name()`, builds a `TableRegistration { table_name: String }` (`catalog.rs:40-44`) — note: **the persisted catalog row is the bare table-name string, the `RecordValue` type is erased at persistence** — and hands back a `TableReference<RecordValue>`, again just `{ name, PhantomData<RecordValue> }` (`table.rs:62-66`). The caller holds the only binding from name to type. Two flavors exist: string-keyed `TableReference` → `sema::Table<String, RecordValue>` (`table.rs:92-94`) and `IdentifiedTableReference` → `sema::Table<u64, RecordValue>` with an engine-managed `RecordIdentifier(u64)` counter (`table.rs:109-111`, `engine.rs:74-92,992-1004`).

`EngineRecord` supplies the key from the record body — `fn record_key(&self) -> RecordKey` (`record.rs:76-78`); the canonical impl is one line (`tests/signal_frame_seam.rs:35-39`). The orphan-rule escape hatch is `assert_keyed`/`mutate_keyed`, which take an explicit `RecordKey` so imported contract types that cannot impl the local trait still store without a wrapper duplicate (`ARCHITECTURE.md:166-171`, `engine.rs:294`).

**This is perfect specificity at the type layer and total erasure at the persistence layer.** The catalog (`catalog.rs:6-38`) is a `Vec<TableRegistration>` whose only datum is the name string; `is_registered` is a linear name scan. The engine cannot, from persisted state alone, know what type a table holds — only that a name was registered. That is fine today because the *component* re-declares the typed `TableDescriptor` constants on every open and the kernel re-binds `(name, K, V)`. It is the crux for VC: a replay/migration layer that must decode old bytes cannot recover the type from anything sema-engine persists.

### 3. Subscriptions degrade to runtime type erasure (`Any` downcast)

The one place genericity is *not* compile-time is subscription fan-out. `SubscriptionRegistry` stores `Vec<Arc<dyn ErasedSubscription>>` and delivers a delta by passing the record as `&dyn Any`, each `ActiveSubscription<RecordValue>` doing `record.downcast_ref::<RecordValue>()` and silently returning on mismatch (`subscribe.rs:305-352`, `385-403`). This is the existing precedent for "generic over many record families inside one homogeneous container" — and it is precisely the stringly/erased pattern the discipline warns against. Any VC log that must hold operations across *all* a component's families in one ordered stream faces the same forced choice subscriptions already made: a tagged/erased container, or a sealed per-component enum.

## The commit log today (the seed to generalise) — confirmed against source

The system context's line cites are accurate:

- `CommitLogOperation { operation: SemaOperation, table_name: String, key: Option<RecordKey> }` (`log.rs:63-68`). **Metadata only — no payload, no prior value, no schema hash, not replayable into state.** Note `table_name` is a `String`, not a `TableName`, and `operation` is the `signal_sema::SemaOperation` verb.
- `CommitLogEntry { commit_sequence: CommitSequence, snapshot: SnapshotIdentifier, operations: NonEmpty<CommitLogOperation> }` (`log.rs:15-19`). Atomicity is structural via `NonEmpty`; the old top-level `Atomic` is gone.
- `SnapshotIdentifier(u64)` with `genesis()`/`next()` — sequence-addressed, not content-addressed (`snapshot.rs:19,40-56`). `CommitSequence(u64)` is the sibling monotonic cursor (`sequence.rs:17-35`). `DatabaseMarker` bundles the two (`snapshot.rs:35-38`) and is the compact observed-boundary every receipt and snapshot carries.

The log lives in the component's own `.sema` file as `const COMMIT_LOG: sema::Table<u64, CommitLogEntry>` (`engine.rs:32`) and — this is the load-bearing property — **every write path inserts the data row, the log entry, and the two counter rows in one `self.storage.write(|transaction| ...)` closure** (e.g. `engine.rs:333-347` for `assert_keyed`; identical shape in `mutate`, `retract`, `commit`). One redb transaction = one fsync-on-commit = log and view provably cannot diverge. This free atomicity is the most valuable thing the current design has and the thing "version the log, demote the store to a view" must not lose.

Replay surface today is read-only and in-memory: `commit_log()` collects the whole table, `replay_from_sequence(start)` filters by `CommitSequence >= start`, `commit_log_range(SequenceRange)` filters by snapshot range (`engine.rs:892-918`). **None of these reconstruct state** — they hand back the metadata-only entries. `ARCHITECTURE.md:91-100` frames the sequence as a "per-database high-water mark for version handover: a next-version daemon can copy state at sequence N, then replay commits from N+1 forward" — but with a payloadless log, "replay" today means re-issuing operations whose payloads must come from somewhere else (the live store), which only works for same-schema handover, not migration across rkyv type sets.

## The six verbs, the read plan, and what is real vs. placeholder

The verbs (`signal_sema::SemaOperation`: Assert/Mutate/Retract/Match/Subscribe/Validate) map to: three write methods + multi-op `commit` (`engine.rs:276-679`), `match_records`/`match_identified` (`681-840`), `subscribe` (`920-943`), `validate` (`842-861`, which is `match_records` + a count receipt). The read plan is a rich tree — `Filter/Project/Aggregate/Infer/Recurse/Constrain` nodes exist as typed variants (`query.rs:332-360`) — but **only `AllRows`, `ByKey`, `ByKeyRange` execute**; everything else returns `Error::UnsupportedReadPlan` (`engine.rs:745-749`). The advanced nodes carry stringly payloads (`PredicatePlan { expression: String }`, `AggregatePlan { reducer: String }`, `RuleSetRef { name: String }` — `query.rs:411-507`). This matters for VC scoping: the query layer is aspirational past three operators; a VC capability should not assume a working query engine to rebuild views — it has `iter`-and-filter-in-memory today (`engine.rs:694-744`).

## The public API a component links against

The full surface is the `pub use` list in `lib.rs:20-53`: `Engine`/`EngineOpen`; `Catalog`/`TableRegistration`; the log types; the mutation request/receipt family (`Assertion`, `KeyedAssertion`, `CommitRequest`, `WriteOperation`, `MutationReceipt`, `CommitReceipt`, and `Identified*` variants); the query family; `EngineRecord`/`EngineStoredValue`/`EngineStoredRecord`/`RecordIdentifier`/`RecordKey`; `CommitSequence`; `DatabaseMarker`/`SnapshotIdentifier`; the subscription family; the table-descriptor/reference family. Notably it **re-exports the sema kernel itself** — `StorageKernel`, `StorageKernelTable`, `SchemaVersion`, `StorageWriteTransaction` (`lib.rs:38-42`) — and `Engine::storage_kernel()` hands out `&sema::Sema` (`engine.rs:966-968`). So a VC library could be authored either *inside* sema-engine against `Engine`'s internals, or *beside* it against the re-exported kernel handle; both paths are already open.

## What is already generic/reusable vs. what VC would add

**Already generic and reusable (the VC layer should consume, not rebuild):**
- The storable-type contract: `EngineStoredValue` blanket impl over any `Archive + Clone` type (`record.rs:94-106`). A VC payload-bearing log entry can demand exactly this bound.
- The atomic write seam: one redb transaction wrapping data + log + counters (`engine.rs:333-347` and siblings). VC must extend the entry written here, not add a second store.
- The ordered cursor: `CommitSequence`/`SnapshotIdentifier`/`DatabaseMarker` are the sortable, `next()`-able markers. The design direction is right that digests sit *beside* these, not replacing them — the code already has no other ordering primitive.
- The kernel's version-skew guard: `Schema { version: SchemaVersion }`, hard-fail on mismatch, refuse legacy-unstamped files (`sema/src/lib.rs:527-552`). A `SchemaTransition` log entry must coordinate *with* this gate, not around it.

**What VC must ADD, and where the per-component cost falls:**
- *Payload + schema-selector in the log entry.* `CommitLogOperation` (`log.rs:63-68`) must gain a payload (the archived record bytes) and a schema-hash decoder selector. The payload type is the same `RecordValue` genericity problem as the store — and here it bites harder, because a single log stream may carry multiple families. This is generic-as-a-type-parameter only if the log is per-family; if it is one stream per component (the natural backup unit), the entry must erase the payload (bytes + schema-hash tag), which is the subscription-`Any` tension surfacing in persisted form.
- *Content addressing.* There is **no blake3 / digest anywhere in sema-engine** (grep confirms; the only first-party content hash in the workspace is criome's `ObjectDigest`, `signal-criome/src/lib.rs:55-57`). Entry-digest, prev-digest hash-linking, and content-addressed checkpoints are entirely new types — generic and reusable, owned by the VC crate.
- *A decode-by-schema-hash path.* Replay across a `SchemaTransition` needs to decode old bytes with an old type set. sema-engine persists no type information (catalog row is a bare name string, `catalog.rs:42-44`), so this cannot be generic over "the current `RecordValue`" — it needs a per-component registry mapping schema-hash → frozen archived type + reducer. That registry is the spirit `SpiritStoreV1..V6` pattern generalised; it is inherently per-component data fed into a generic mechanism (the spirit poster-child shows exactly this hand-rolled today).
- *Remote durability levels.* Nothing in the engine knows about a mirror; `Engine` owns one local file. The local-committed / queued / server-committed states and per-store ack policy are new types with no current home — a clean generic addition, and the place where the "linked library vs. shared server infra" boundary lives.

## The owning-noun problem for a "library of generic types and traits"

The discipline forbids free functions and ZST namespaces, and sema-engine honors it cleanly: every method hangs off a data-bearing noun (`Engine`, `Catalog`, `TableReference<RecordValue>`, `CommitLogEntry`, `SubscriptionRegistry`). A VC library must do the same — the temptation is a `VersionControl` ZST with helper methods (a free-function bag in disguise). The real nouns the code already suggests: a payload-bearing **`LogEntry`/`CommitLogEntry`** (extend the existing one), a **`Checkpoint`** identity type, a **`SchemaTransition`** entry variant, a **`Mirror`/`RemoteHead`** durability-state type, and a per-component **`SchemaRegistry`** (decode selector). Methods belong on those, with the generic `RecordValue` parameter flowing through exactly as it does in `Engine` today. The `EngineStoredValue` blanket-impl trait is the proven template for "generic over arbitrary record types without an enum" — but it is type-preserving only while the type parameter stays in scope; the moment the log must be one heterogeneous persisted stream, that template breaks and the design must choose erasure (bytes + schema-hash) or a sealed per-component family enum. That choice is THE tension this report flags, not resolves.

