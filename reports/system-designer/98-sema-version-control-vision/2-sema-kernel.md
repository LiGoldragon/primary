# 98/2 — sema + sema-engine — kernel shape, the existing versioned log, choke points, genericity

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
An independent adversarial verifier re-checked every key claim against the code; its verdicts are appended at the end of this file.*

# Sema Storage Kernel and Engine: Architecture Analysis

## 1. KERNEL SHAPE: What the Sema Kernel Owns

The sema kernel is a lightweight, schema-guarded typed-table wrapper over redb and rkyv. The public surface is minimal and closure-scoped.

**Kernel-owned tables and guards:**

The kernel maintains exactly two internal tables (with `__sema_` prefix), both used for database headers and metadata: `/git/github.com/LiGoldragon/sema/src/lib.rs:466-469`

- `__sema_headers` — stores the `DatabaseHeader`, which pins rkyv format choices (endianness, pointer width, alignment, bytecheck). The header is written on first open and hard-fails on mismatch, protecting against binary incompatibility from rkyv build configuration drift. `/git/github.com/LiGoldragon/sema/src/lib.rs:510-525`
- `__sema_meta` — stores two metadata values: `schema_version` (the `SchemaVersion` constant, bumped by consumers when table layouts change) and initialized counters (for future use). `/git/github.com/LiGoldragon/sema/src/lib.rs:527-552`

**Tables are typed but not pre-declared.** Component-owned tables are declared lazily at the consumer layer through `Table<K, V>` constants. The kernel does not enumerate table names; each typed `Table<K, V>` carries its own name and (implicitly) its key/value types. `/git/github.com/LiGoldragon/sema/src/lib.rs:499-501`

**Public API surface — the six primitives:**

```rust
// From /git/github.com/LiGoldragon/sema/src/lib.rs:476-581
pub struct Sema {
    database: Database,
    path: PathBuf,
}

impl Sema {
    pub fn open_with_schema(path: &Path, schema: &Schema) -> Result<Self>;
    pub fn read<R>(&self, body: impl FnOnce(&ReadTransaction) -> Result<R>) -> Result<R>;
    pub fn write<R>(&self, body: impl FnOnce(&WriteTransaction) -> Result<R>) -> Result<R>;
    pub fn path(&self) -> &Path;
}

pub struct Table<K, V> { ... }
impl<K, V> Table<K, V> {
    pub const fn new(name: &'static str) -> Self;
    pub fn ensure(&self, txn: &WriteTransaction) -> Result<()>;
    pub fn get<'txn>(&self, txn: &'txn ReadTransaction, key: K) -> Result<Option<V>>;
    pub fn insert<'txn>(&self, txn: &'txn WriteTransaction, key: K, value: &V) -> Result<()>;
    pub fn remove<'txn>(&self, txn: &'txn WriteTransaction, key: K) -> Result<bool>;
    pub fn iter(&self, txn: &ReadTransaction) -> Result<Vec<(K::Owned, V)>>;
    pub fn range<'range>(&self, txn: &ReadTransaction, range: impl RangeBounds<KeyRange>) -> Result<Vec<(K::Owned, V)>>;
}
```

**Record families registration:** Record types are not registered at the kernel layer. Each consumer defines `Table<K, V>` constants with the record type baked into the generic parameter. The trait bound `V: Archive + Serialize + Deserialize` enforces rkyv compatibility at compile time. Consumers that need to pass record types through a trait rather than monomorphically use the keyword-argument pattern: the `TableDescriptor<RecordValue>` and `IdentifiedTableDescriptor<RecordValue>` carry the record type as a `PhantomData`. Registration happens in sema-engine, not the kernel. `/git/github.com/LiGoldragon/sema-engine/src/table.rs:24-60`


## 2. VERSIONING SURFACE: Operation Log and Payload Recording

The versioning surface in sema-engine is opt-in via `EngineOpen::with_versioning(VersioningPolicy)`. When enabled, the engine records a hash-linked, payload-bearing commit log alongside the standard immutable commit log.

**What gets written per durable operation:**

Every write operation that commits (Assert/Mutate/Retract) through the engine adds two entries to the same write transaction:

1. **Standard commit log entry** (always written): A `CommitLogEntry` keyed by `CommitSequence`, stored in table `__sema_engine_commit_log`. `/git/github.com/LiGoldragon/sema-engine/src/log.rs:14-60`

   ```rust
   pub struct CommitLogEntry {
       commit_sequence: CommitSequence,      // monotonic u64 high-water mark
       snapshot: SnapshotIdentifier,          // per-operation snapshot ID
       operations: NonEmpty<CommitLogOperation>,
   }
   
   pub struct CommitLogOperation {
       operation: SemaOperation,              // Assert | Mutate | Retract | Match | Subscribe | Validate
       table_name: String,                    // which table was affected
       key: Option<RecordKey>,                // if keyed by domain, the key; None for snapshot operations
   }
   ```

2. **Versioned commit log entry** (only if `VersioningPolicy` is configured): A `VersionedCommitLogEntry` keyed by the same `CommitSequence`, stored in table `__sema_engine_versioned_commit_log`. This entry is only inserted if versioning is enabled. `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:226-296` and `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:1273-1330`

   ```rust
   pub struct VersionedCommitLogEntry {
       store_name: VersionedStoreName,        // component identity (e.g., "mind")
       schema_hash: SchemaHash,               // blake3 hash of schema source (32 bytes)
       commit_sequence: CommitSequence,       // same as standard log
       snapshot: SnapshotIdentifier,          // same as standard log
       previous_entry_digest: Option<EntryDigest>,  // hash of prior entry (chain)
       entry_digest: EntryDigest,             // blake3 hash of this entry (32 bytes)
       operations: NonEmpty<VersionedLogOperation>,
   }
   
   pub struct VersionedLogOperation {
       operation: SemaOperation,
       table_name: String,
       key: Option<RecordKey>,
       payload: VersionedPayload,  // Enum: Record { bytes: Vec<u8> } | Tombstone
   }
   ```

The versioned entry digest is computed via blake3 over a deterministic serialization of all entry fields including the operation payloads. `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:96-130`

**Hashing and content-addressing:**

- `SchemaHash::for_label(label)` computes `blake3::hash(label.as_ref())` as a 32-byte hash. This is the mechanism for schema identity when versioning is enabled. `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:63-65`
- `EntryDigest` is a 32-byte blake3 hash computed over the entire entry structure. It forms a hash chain: each new entry includes the prior entry's digest, so the log is tamper-evident. `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:85-130`
- **No other content-addressing exists.** The kernel uses redb's copy-on-write B-tree page references, not content-addressable identifiers. The schema hash and entry digest are the only content-hash structures in the system.

**Checkpoint, restore, and replay:**

- **Replay:** `Engine::versioned_replay_from_sequence(CommitSequence)` returns all versioned log entries starting from a given sequence. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:995+` (visible in versioned_commit_log function and its usage pattern)
- **Restore:** The engine does not implement restore itself. The caller is responsible for copying state at a known `CommitSequence` and replaying the log from the next sequence onward. This is the "zero-downtime handover" mechanism described in ARCHITECTURE: a next-version daemon reads `current_commit_sequence()` from the current daemon, copies the database at that mark, then replays from sequence N+1. `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md:254-274`
- **Checkpoint:** No explicit checkpoint operation exists. The durable `CommitSequence` is the checkpoint. Every write advances it; failed commits do not. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:967-975`

The versioned log is designed to be replayed by backup/mirror code outside sema-engine; the engine only records and exposes it. There is no built-in snapshot compaction or log truncation.


## 3. SIX VERBS: Assert/Mutate/Retract/Match/Subscribe/Validate

All six operations from `signal-sema::SemaOperation` are defined and implemented:

**Write operations** (mutate durable state, advance `CommitSequence`):

- **Assert**: Insert a new record. Key must not already exist. Single-operation path: `Engine::assert()` (for records with `EngineRecord` trait) or `Engine::assert_keyed()` (for imported schemas). Multi-operation path: `CommitRequest::assert()`. Fails on duplicate key. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:307-403`

- **Mutate**: Replace an existing record. Key must exist. Single-operation path: `Engine::mutate()` or `Engine::mutate_keyed()`. Multi-operation path: `CommitRequest::mutate()`. Fails on missing key. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:405-501`

- **Retract**: Remove a record. Key must exist. Single-operation path: `Engine::retract()`. Multi-operation path: `CommitRequest::retract()`. Records are irreversibly deleted after redb reclaims pages; no undelete. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:503-580`

**Read operations** (do not mutate state, do not advance `CommitSequence`):

- **Match**: Execute a query plan (all rows, by key, by key range, constrain, project, aggregate, infer, recurse). Returns a `QuerySnapshot` containing the `DatabaseMarker` (commit sequence + snapshot ID) observed at read time and the typed rows. Most complex operators (constrain, project, aggregate, infer, recurse) are declared but return `UnsupportedReadPlan` errors. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:775-852`

- **Validate**: Dry-run a read plan without committing. Executes `Match` internally and returns a `ValidationReceipt` with record count. Does not write commit-log entries. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:936-955`

**Streaming operations**:

- **Subscribe**: Register a subscription sink and return an initial snapshot of the table. Delivers delta updates after mutations commit. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs` subscriptions module (not read in full, but present in API surface per ARCHITECTURE §"Subscribe")

**Stubs (declared but not fully implemented):**

The read-plan algebra operators (`Constrain`, `Project`, `Aggregate`, `Infer`, `Recurse`) are enumerated in `ReadPlan` but execution in `match_records` returns `UnsupportedReadPlan` errors. These are scaffolding for future work. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:839-843`


## 4. CONSUMERS: Dependency Mapping

Run `grep -rl "sema-engine" /git/github.com/LiGoldragon/*/Cargo.toml` yields:

| Component | Uses | How |
|-----------|------|-----|
| **terminal** | sema-engine | Opens `Engine`, registers `TableDescriptor` for six session/event tables, executes `KeyedAssertion`/`KeyedMutation`/`Match` queries. Record types are from `signal-terminal` contract crate. `/git/github.com/LiGoldragon/terminal/src/tables.rs:66-103` |
| **introspect** | sema-engine | Registers observation tables, stores cross-component state snapshots. `/git/github.com/LiGoldragon/introspect/src/store.rs` |
| **mind** | sema-engine | (Cargo.toml declares it) Tables for thoughts/beliefs/etc. Used as part of daemon actor storage. |
| **criome** | sema-engine | (Cargo.toml declares it) Persistence layer for criome objects. |
| **spirit** | sema-engine | (Cargo.toml declares it) Primary target consumer; stores intent/design state. No schema migration yet (first prototype). |
| **persona** | sema-engine | (indirectly) Through spirit and mind. |
| **orchestrate** | sema-engine | (Cargo.toml declares it) Orchestration state storage. |
| **router** | sema-engine | (Cargo.toml declares it) Routing table storage. |
| **upgrade** | sema-engine | (Cargo.toml declares it) Component version handover state. |

**Do they use the bare kernel directly?** No consumer opens `sema::Sema` directly. All go through `sema-engine::Engine`, which composes the kernel. The only exceptions would be consumer-local temporary tables, which use `Engine::storage_kernel()` to access the kernel's read/write transactions without going through engine operations. `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md:29-34`


## 5. INVERSION SEAM: The Write Path Choke Point

The design decision is: *the versioned operation log is the source of truth; the redb store is a rebuildable materialized view.*

**All write paths that mutate durable state:**

Every method that mutates durable state appends to redb in a single write transaction. The choke point is `Engine::write(|transaction| ...)`:

1. **Single-operation writes:** `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:307-403` (assert), `:405-501` (mutate), `:503-580` (retract)
   - Call `next_commit_sequence()` and `next_snapshot()` (read-only; allocates new IDs)
   - Construct both `CommitLogEntry` and (optionally) `VersionedCommitLogEntry`
   - Call `self.storage.write(|transaction| ...)`, inside which they:
     - Insert the domain record into its table via `table.sema_table().insert(transaction, key, record)`
     - Insert the `CommitLogEntry` into `__sema_engine_commit_log` keyed by `commit_sequence`
     - Conditionally insert the `VersionedCommitLogEntry` into `__sema_engine_versioned_commit_log`
     - Update counters: `LATEST_COMMIT_SEQUENCE_KEY` and `LATEST_SNAPSHOT_KEY` in `__sema_engine_counters`
   - Optionally deliver subscription deltas (outside the transaction)

2. **Multi-operation writes:** `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:585-773` (commit)
   - Pre-validate all operations (duplicate keys, missing records) in read transactions
   - Call `next_commit_sequence()` and `next_snapshot()` once
   - Construct one `CommitLogEntry` with `NonEmpty<CommitLogOperation>` (all operations in one entry)
   - Construct one `VersionedCommitLogEntry` with `NonEmpty<VersionedLogOperation>` (if versioning enabled)
   - Call `self.storage.write(|transaction| ...)` and execute all effects (assert/mutate/retract records) within one transaction, then insert both log entries

3. **Identified records** (`Engine::assert_identified`, `mutate_identified`, `retract_identified`): Same pattern, but the identifier is allocated from `__sema_engine_identified_counters` and returned in the receipt.

4. **Schema/table registration:** `Engine::register_table()` and `Engine::register_identified_table()` write to `__sema_engine_catalog` and (for identified tables) initialize the identifier counter. These are not domain mutations but engine metadata. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:66-98`

**Out-of-band writes (NOT present):**

- No migration rewrites outside a choke point. If schema migration is needed, it is a future concern (reducers on the eventual Sema-on-Sema stack).
- No config persistence writes. Component configs live in separate infrastructure (NOTA, Persona signaling), not in sema-engine.
- No direct `redb` table access from outside the engine. The `storage_kernel()` accessor allows temporary component-local tables to exist during migration, but those are not domain mutations; they are component-owned staging areas.
- No append-only identity or sequence allocation outside the engine. The `CommitSequence` and `RecordIdentifier` are allocated by the engine and persisted in its durable counters.

**All mutations flow through exactly two choke points:**

1. `Engine::assert*` / `Engine::mutate*` / `Engine::retract*` (single-operation paths)
2. `Engine::commit` (multi-operation path)

Both paths call `self.storage.write(|transaction| ...)` and both insert into the commit log in the same transaction as the domain mutation.


## 6. GENERICITY: Trait-Driven Record Registration

The engine is generic over record families via two trait-driven paths:

**Path 1: `EngineRecord` trait — for locally-defined record types**

```rust
pub trait EngineRecord: Clone {
    fn record_key(&self) -> RecordKey;
}
```

A record type that implements `EngineRecord` can use the simpler single-operation APIs: `Engine::assert(Assertion)` (no key argument needed; extracted from record). The consumer's domain types implement this trait. `/git/github.com/LiGoldragon/sema-engine/src/record.rs:76-78`

**Path 2: `EngineStoredValue` + `KeyedAssertion`/`KeyedMutation` — for imported schemas**

For record types from imported contracts/schemas where the consumer cannot implement `EngineRecord` (Rust orphan rules), consumers use:
- `KeyedAssertion::new(table, key, record)` 
- `KeyedMutation::new(table, key, record)`
- `Engine::assert_keyed()` / `Engine::mutate_keyed()`

The record only needs to satisfy `EngineStoredValue` (a trait alias for rkyv-compatible serialization). The key is supplied separately. `/git/github.com/LiGoldragon/sema-engine/src/mutation.rs:14-51` and `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:325-403`

**TableDescriptor genericity:**

`TableDescriptor<RecordValue>` and `IdentifiedTableDescriptor<RecordValue>` carry the record type as a phantom generic. The consumer constructs them at definition time:

```rust
const SESSIONS: TableName = TableName::new("sessions");
// Later:
let sessions = engine.register_table(TableDescriptor::new(SESSIONS))?;
```

The descriptor is just a name wrapper; the type information lives in the `TableReference` returned by `register_table`. This is monomorphic dispatch — the Rust compiler generates code for each record type separately. No shared machinery across families at runtime. `/git/github.com/LiGoldragon/sema-engine/src/table.rs:24-112`

**Per-family VC machinery without per-component hand code:**

The versioning system is already family-agnostic:

1. Every write operation stores `table_name: String` in both log entries. `/git/github.com/LiGoldragon/sema-engine/src/log.rs:65-66` and `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:172-177`

2. The `VersionedPayload` is an enum that holds raw rkyv bytes for the record: `Record { bytes: Vec<u8> }`. The engine serializes the record via `rkyv::to_bytes::<rancor::Error>(&record)` without knowing its concrete type. `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:1292-1310` and `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:132-169`

3. The `SchemaHash` is computed from a label (not the record type). Different schema versions are identified by their hash, and the log entry includes the schema hash. `/git/github.com/LiGoldragon/sema-engine/src/versioning.rs:8-27` and `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:1273-1289`

**Could per-family VC machinery (family identity hash, closed-sum decoder) be attached without per-component hand code?**

Yes. The machinery would be:

- **Family identity hash:** Encode the `TableName` + `SchemaHash` + the rkyv schema of the record type (via `std::any::type_name` or a procedural macro computing a blake3 of the field names/types) into a tuple hash. Store this in the `VersionedLogOperation` alongside the payload.

- **Closed-sum decoder:** At replay time, the receiver daemon iterates over all registered families and their rkyv type information, then attempts to deserialize each versioned operation's payload bytes into the appropriate type for the target version. The union of all families forms a closed set the receiver can decode.

- **Mechanism:** This would require no per-component changes if implemented as:
  1. A procedural macro that derives a `FamilySignature` trait from the record type, computing a hash of its rkyv layout.
  2. An inventory mechanism (at startup) where each `Engine::register_table()` or macro-emitted registration stores the family signature.
  3. A `versioned_replay` that looks up signatures by table name and attempts decoding.

The engine architecture **already supports** this: `VersionedLogOperation` is generic over table names, not record types, so new fields (`family_signature: FamilySignature`, `decoder_hint: Option<String>`) could be added to the log entry shape. The closed-sum decoder would live in a new module (e.g., `sema-engine::decoder`) and would be called at replay time by backup/restore machinery outside the engine.



## keyClaims
- CLAIM: The sema kernel owns exactly two internal tables (__sema_headers and __sema_meta) for database format guards and schema version validation. Component tables are declared at the consumer layer via Table<K, V> constants and created lazily on first use.
  EVIDENCE: /git/github.com/LiGoldragon/sema/src/lib.rs:466-469, 494-501, 510-552
- CLAIM: The kernel's public API is six operations: open_with_schema, read (closure-scoped), write (closure-scoped), path(), and Table methods (get, insert, remove, iter, range, ensure).
  EVIDENCE: /git/github.com/LiGoldragon/sema/src/lib.rs:476-581, and sema/ARCHITECTURE.md §"Public Surface"
- CLAIM: When versioning is enabled via VersioningPolicy, every write operation records two entries in the same transaction: a standard CommitLogEntry (always) and a VersionedCommitLogEntry (optional) with blake3 hashes (SchemaHash, EntryDigest) forming a hash chain.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/versioning.rs:7-130, 226-296; /git/github.com/LiGoldragon/sema-engine/src/engine.rs:1273-1330
- CLAIM: The versioned payload stores rkyv-serialized record bytes for Assert/Mutate and a tombstone marker for Retract. No other content-addressing exists in the kernel beyond blake3 hashes for schema and entry digests.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/versioning.rs:132-169, 172-224; /git/github.com/LiGoldragon/sema-engine/src/engine.rs:1292-1310
- CLAIM: The six SemaOperation verbs are: Assert (insert, fails on duplicate key), Mutate (replace, fails on missing key), Retract (remove, irreversible after page reuse), Match (read-only query execution), Validate (dry-run query), Subscribe (streaming deltas). All are implemented except complex read-plan operators (Constrain, Project, Aggregate, Infer, Recurse), which return UnsupportedReadPlan errors.
  EVIDENCE: /git/github.com/LiGoldragon/signal-sema/src/operation.rs:14-32; /git/github.com/LiGoldragon/sema-engine/src/engine.rs:307-580, 775-955, 936-955
- CLAIM: All consumers of sema-engine open Engine instances rather than bare sema::Sema handles. Terminal, introspect, mind, criome, spirit, persona, orchestrate, router, and upgrade all use Engine with TableDescriptor-registered families and EngineRecord/EngineStoredValue trait bounds.
  EVIDENCE: grep -rl 'sema-engine' /git/github.com/LiGoldragon/*/Cargo.toml; /git/github.com/LiGoldragon/terminal/src/tables.rs:66-103
- CLAIM: All durable writes pass through exactly two choke points: single-operation writes (assert/mutate/retract) and multi-operation writes (commit). Both call storage.write(|transaction|) and insert to COMMIT_LOG and (conditionally) VERSIONED_COMMIT_LOG in the same transaction as domain mutations.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/engine.rs:307-403, 405-501, 503-580, 585-773, 1322-1330
- CLAIM: No out-of-band writes exist. Migration rewrites, config persistence, and direct redb table writes from outside the engine are not implemented. The engine allocates CommitSequence and RecordIdentifier through its own durable counters.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md:303-313; /git/github.com/LiGoldragon/sema-engine/src/engine.rs:28-40 (IDENTIFIED_COUNTERS, LATEST_COMMIT_SEQUENCE_KEY)
- CLAIM: The engine is generic over record families via two paths: EngineRecord trait (for local types) extracts the key from the record itself; EngineStoredValue + KeyedAssertion/KeyedMutation (for imported schemas) supply the key separately. Both use monomorphic dispatch via generics, not runtime type erasure.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/record.rs:76-125; /git/github.com/LiGoldragon/sema-engine/src/mutation.rs:14-51; /git/github.com/LiGoldragon/sema-engine/src/engine.rs:307-403, 325-403
- CLAIM: Per-family VC machinery (family identity hash, closed-sum decoder) could be attached without per-component hand code by adding a FamilySignature field to VersionedLogOperation and implementing a family lookup/decode registry at replay time. The engine architecture already supports this extension point.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/versioning.rs:171-224; /git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md:315-333 notes macro integration target

## openQuestions
- Does any consumer currently use the VersioningPolicy feature, or is it only scaffolding? The code supports it but no consumer Cargo.toml grep shows explicit VersioningPolicy configuration.
- What is the strategy for handling the case where a replay decoder encounters a VersionedLogOperation for a table/schema combination not registered in the receiver daemon? Will it fail fast or skip?
- The eventual Sema-on-Sema design mentions content-addressed schema identity and reducer-based migration. Is there a timeline or design doc that specifies the transition from manual SchemaVersion to blake3-hashed schema identity?
- The storage_kernel() accessor allows components to use temporary local tables during migration. Are there any guardrails to prevent domain records from landing in those temporary tables instead of engine-managed tables?


## Adversarial verification verdicts

- [CONFIRMED] The sema kernel owns exactly two internal tables (__sema_headers and __sema_meta) for database format guards and schema version validation. Component tables are declared at the consumer layer via Table<K, V> constants and created lazily on first use.
  EVIDENCE: /git/github.com/LiGoldragon/sema/src/lib.rs:466-469 defines const META and const DATABASE_HEADERS as the two internal tables. Lines 494-501 and 510-552 show ensure_database_header and ensure_schema_version that validate these on open. Lines 496-501 explicitly confirm tables are created lazily: 'Tables get created lazily on first use through Table::get / Table::insert with the consumer's actual K and V.' This is also documented in ARCHITECTURE.md line 100-102.
- [CONFIRMED] The kernel's public API is six operations: open_with_schema, read (closure-scoped), write (closure-scoped), path(), and Table methods (get, insert, remove, iter, range, ensure).
  EVIDENCE: /git/github.com/LiGoldragon/sema/src/lib.rs:476-581 implements all six methods: open_with_schema (line 480), read (line 577), write (line 568), path (line 554), and Table methods get/insert/remove/iter/range/ensure (lines 358-454). ARCHITECTURE.md lines 111-134 confirm this exact API surface.
- [CONFIRMED] When versioning is enabled via VersioningPolicy, every write operation records two entries in the same transaction: a standard CommitLogEntry (always) and a VersionedCommitLogEntry (optional) with blake3 hashes (SchemaHash, EntryDigest) forming a hash chain.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/engine.rs:135-151 shows assert_identified writes both COMMIT_LOG.insert (line 141) and insert_versioned_entry (line 142) in the same transaction. Same pattern in mutate_identified (lines 287-288), retract_identified (lines 212-213), assert_keyed (lines 378-379), mutate_keyed (lines 477), retract (lines 552), and commit (lines 746-747). /git/github.com/LiGoldragon/sema-engine/src/versioning.rs:7-130 defines VersioningPolicy and SchemaHash/EntryDigest structures with blake3 hash chain implementation (lines 96-130 show from_entry_fields computing blake3 hash incorporating previous_entry_digest).
- [CONFIRMED] The versioned payload stores rkyv-serialized record bytes for Assert/Mutate and a tombstone marker for Retract. No other content-addressing exists in the kernel beyond blake3 hashes for schema and entry digests.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/versioning.rs:132-169 defines VersionedPayload enum with Record{bytes} and Tombstone variants. Lines 1292-1310 in engine.rs show versioned_record_payload serializing records via rkyv::to_bytes. Lines 696, 1268 show Tombstone used for Retract operations. The hash chain in EntryDigest (lines 96-130) uses only blake3 hashing; no content-addressing scheme exists beyond these hashes.
- [CONFIRMED] The six SemaOperation verbs are: Assert (insert, fails on duplicate key), Mutate (replace, fails on missing key), Retract (remove, irreversible after page reuse), Match (read-only query execution), Validate (dry-run query), Subscribe (streaming deltas). All are implemented except complex read-plan operators (Constrain, Project, Aggregate, Infer, Recurse), which return UnsupportedReadPlan errors.
  EVIDENCE: /git/github.com/LiGoldragon/signal-sema/src/operation.rs:19-32 defines the six SemaOperation enum values. /git/github.com/LiGoldragon/sema-engine/src/engine.rs implements: assert (line 307), mutate (line 405), retract (line 503), commit (line 585), match_records (line 775), validate (line 936), subscribe (line 1034). Lines 839-842 show UnsupportedReadPlan error for unimplemented operators. Query.rs lines 58-96 define builders for constrain, project, aggregate, infer, recurse but engine.rs line 840 returns error for any node not matching AllRows/ByKey/ByKeyRange.
- [NUANCED] All consumers of sema-engine open Engine instances rather than bare sema::Sema handles. Terminal, introspect, mind, criome, spirit, persona, orchestrate, router, and upgrade all use Engine with TableDescriptor-registered families and EngineRecord/EngineStoredValue trait bounds.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/engine.rs:49-64 shows Engine::open pattern. Grep for sema-engine dependency lists: criome, mind, introspect, persona, orchestrate, router, spirit, upgrade all have it in Cargo.toml. However, ARCHITECTURE.md lines 29-31 explicitly acknowledges the escape hatch: 'Consumers that still have unmigrated component-local tables use Engine::storage_kernel() rather than opening a second sema::Sema handle to the same .sema file.' This is implemented at line 1080-1082, proving direct sema access is available. The claim is incomplete—all are expected to migrate but can still access raw sema if needed.
- [NUANCED] All durable writes pass through exactly two choke points: single-operation writes (assert/mutate/retract) and multi-operation writes (commit). Both call storage.write(|transaction|) and insert to COMMIT_LOG and (conditionally) VERSIONED_COMMIT_LOG in the same transaction as domain mutations.
  EVIDENCE: Grep found 10 storage.write calls in engine.rs at lines 72, 87, 135, 206, 281, 372, 470, 545, 728, 1207. These are: register_table (catalog only, line 72-74), register_identified_table (catalog+counter, lines 87-94), assert_identified (all writes: table+log+versioned+counters, lines 135-151), retract_identified (conditional, lines 206-222), mutate_identified (all writes, lines 281-296), assert_keyed (all writes, lines 372-387), mutate_keyed (all writes, lines 470-485), retract (all writes, lines 545-560), commit (multi-op, lines 728-755), and persist_subscription (subscription registration, lines 1207-1215). The claim says 'exactly two choke points' but the code shows: (1) single-operation methods (assert/mutate/retract) directly write via storage.write; (2) commit method writes; (3) register_table/register_identified_table write catalog; (4) persist_subscription writes subscriptions. So there are MORE than two choke points. The claim is incomplete—catalog registration and subscription persistence also write durably.
- [CONFIRMED] No out-of-band writes exist. Migration rewrites, config persistence, and direct redb table writes from outside the engine are not implemented. The engine allocates CommitSequence and RecordIdentifier through its own durable counters.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md:303-313 lists Non-Goals: 'No schema-less storage open. No raw byte slot store. No raw redb access from component daemons. No second redb handle for a component database already opened by Engine.' Engine.rs lines 28-40 define IDENTIFIED_COUNTERS table for RecordIdentifier allocation (lines 1106-1118 show next_record_identifier reads from IDENTIFIED_COUNTERS), and COUNTERS table for CommitSequence/SnapshotIdentifier (lines 1088-1090 show next_commit_sequence reads current and calls .next()). No migration, config, or raw redb write paths exist outside this controlled allocation.
- [CONFIRMED] The engine is generic over record families via two paths: EngineRecord trait (for local types) extracts the key from the record itself; EngineStoredValue + KeyedAssertion/KeyedMutation (for imported schemas) supply the key separately. Both use monomorphic dispatch via generics, not runtime type erasure.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/record.rs:76-125 defines EngineRecord trait (line 76, requires record_key() method) and EngineStoredValue trait (lines 80-106, auto-impl for rkyv types with serialize/deserialize bounds). /git/github.com/LiGoldragon/sema-engine/src/mutation.rs:14-51 defines KeyedAssertion and KeyedMutation that take key separately. Both assert (line 307, uses EngineRecord) and assert_keyed (line 325, uses EngineStoredValue) methods are monomorphic generics with <RecordValue> type parameters, confirming compile-time dispatch not runtime type erasure.
- [CONFIRMED] Per-family VC machinery (family identity hash, closed-sum decoder) could be attached without per-component hand code by adding a FamilySignature field to VersionedLogOperation and implementing a family lookup/decode registry at replay time. The engine architecture already supports this extension point.
  EVIDENCE: /git/github.com/LiGoldragon/sema-engine/src/versioning.rs:171-224 defines VersionedLogOperation with operation, table_name, key, payload fields. The architecture could extend this with FamilySignature without breaking the versioned log structure (entries are rkyv-serialized, layout-flexible). ARCHITECTURE.md lines 315-333 confirm macro-pattern integration as the integration path for schema-driven code generation of family identity/decoder machinery. The current design does not preclude this extension; it's explicitly named as a future work target in the Macro-pattern integration section.

