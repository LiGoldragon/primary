# Ground: the sema storage kernel

## Scope and method

This grounds the reusable-version-control mapping in the actual `sema` kernel as it exists on disk, not in memory. Read in full: `repos/sema/src/lib.rs` (582 lines, the entire crate — `sema` is a single-file library), both test files, `ARCHITECTURE.md`, `INTENT.md`, `Cargo.toml`, `Cargo.lock`, and `schema/sema.concept.schema`. Versions confirmed from the lockfile: `redb 4.1.0`, `rkyv 0.8.16`, `sema 0.1.1`. Every signature below is quoted from the live source; the redb API claims are cross-checked against the vendored `redb-4.1.0` source in the cargo registry.

### Three corrections to the supplied ground truth

The brief carries a stale picture of `sema`. The kernel was *cleaned* in "Package A of the sema / sema-engine split" (`ARCHITECTURE.md:209-216`); several things the brief attributes to `sema` are no longer there, or never were:

- **There is no `Slot(u64)` counter in `sema`.** It was removed and is now *actively guarded against*: `tests/no_legacy_surface.rs:14-31` asserts `src/lib.rs` contains no `pub struct Slot`, no `impl From<u64> for Slot`, no `next_slot`, no `__sema_records` table, no slot-keyed iter. `ARCHITECTURE.md:201-216` lists `sema_does_not_export_slot` as a load-bearing witness and states the kernel has "no `Slot`, no legacy raw-byte store, no `reader_count`, no schema-less open." The only `u64`-counter-shaped thing left is `SchemaVersion(u32)` (`lib.rs:194`) and redb's internal `META` table mapping `&str -> u64` (`lib.rs:466`). A reusable VC library that wants a monotonic `CommitSequence` cursor must **introduce** it; `sema` no longer offers a sequence allocator, and `ARCHITECTURE.md:87-90` explicitly says any future "append-only identity or sequence allocation… lands as a typed `sema-engine` primitive… not as a raw storage surface in `sema`."
- **The commit log, `CommitLogEntry`, `SnapshotIdentifier`, the six Sema verbs, and content hashing are NOT in `sema`.** The brief cites `log.rs:63-68`, `snapshot.rs:19`, `store.rs:714-758` — none of these files exist in `sema`; `sema/src/` contains only `lib.rs`. Those live in `sema-engine` and `spirit`, which this grounding task did not cover. So the "today's commit log to generalise" lives one layer up; the *kernel* contributes only the typed-storage substrate the log would be written into.
- **redb 4.1.0's `Durability` enum has exactly two variants — `None` and `Immediate`** (`transactions.rs:360-369`, `#[non_exhaustive]`). The `Eventual` variant from redb 1.x/2.x is gone. This directly constrains the "queued-for-mirror / async RPO" durability ladder: redb gives you only *durable-on-commit* or *not-persisted-until-a-later-immediate-commit*. Any "queued-for-mirror" level is a **library/engine concept layered above redb**, not a redb durability setting.

## The on-disk format and redb usage

`sema` is a thin typed shell over one redb 4.1.0 database file per component. redb itself is a single-file mmap copy-on-write B+tree with single-writer ACID and fsync-on-commit; `sema` adds rkyv-archived values and two internal metadata tables.

The `Sema` handle owns a `redb::Database` and the file path (`lib.rs:471-474`):

```rust
pub struct Sema {
    database: Database,
    path: PathBuf,
}
```

`Sema::open_with_schema(path: &Path, schema: &Schema) -> Result<Self>` (`lib.rs:480-508`) is the *only* open path — there is no schema-less open, by intent (`INTENT.md:38-42`). On open it: creates parent dirs (`lib.rs:481-483`), records whether the file is fresh via `!path.exists()` (`lib.rs:489`), `Database::create`s it, then in one write transaction calls `ensure_database_header` and `ensure_schema_version` before committing (`lib.rs:490-503`).

Two kernel-owned internal tables, both `__sema_`-prefixed (`lib.rs:466-469`):

```rust
const META: TableDefinition<&str, u64> = TableDefinition::new("__sema_meta");
const DATABASE_HEADERS: TableDefinition<&str, &[u8]> = TableDefinition::new("__sema_headers");
const DATABASE_HEADER_KEY: &str = "database";
const SCHEMA_VERSION_KEY: &str = "schema_version";
```

`__sema_meta` holds the schema version as a `u64`; `__sema_headers` holds the rkyv-encoded `DatabaseHeader`. `ARCHITECTURE.md:100-103` constrains internal tables to the `__sema_` prefix and forbids component tables from using it. The internal-namespace invariant is tested at `tests/kernel.rs:139-157`.

**What a reusable VC library needs / changes here.** A "version the log, not the store" design adds at least one more component-visible table (the payload-bearing, hash-linked commit log) plus checkpoint metadata. Two structural questions land directly on this open path: (1) is the log a `__sema_`-prefixed kernel-owned table written in the same redb transaction as the data — getting "log and view cannot diverge" for free from redb's single-writer ACID — **or** a separate file? `sema` today proves the *same-file* side is trivially available (any consumer table is already atomic with the metadata tables in one `write` closure). The *separate-file* side gets nothing from redb's atomicity and must invent its own crash-consistent ordering (write-log-then-view, fsync barriers, or a spool like `repository-ledger`'s temp-write+rename). The psyche wants **both tested**; `sema`'s single-transaction model is the baseline the same-file arm inherits and the separate-file arm forgoes. (2) Does the log table belong to the kernel (a new `__sema_` table, breaking the "kernel owns only metadata + headers" non-goal at `ARCHITECTURE.md:84-90`) or to the engine layer (a normal component table)? `ARCHITECTURE.md:87-90` already answers in the abstract: append-only identity is `sema-engine`'s, not `sema`'s.

## The typed `Table<K, V>` wrapper

`Table<K, V>` (`lib.rs:231-238`) is a zero-storage typed handle — `name: &'static str` plus two `PhantomData`. It is constructed `const` at module top (`lib.rs:244-250`) and carries the only schema information redb needs: redb identifies a table by `(name, key_type, value_type)`, so the K/V types on the constant *are* the per-table schema (`lib.rs:166-174`). Tables are created lazily on first write, never pre-declared (`lib.rs:496-501`), which is what lets a `Table<u64,V>` and a `Table<&str,V>` coexist in one file (tested at `kernel.rs:201-228`).

The value-operation impl block carries the rkyv bound that defines what is storable (`lib.rs:345-354`):

```rust
impl<K, V> Table<K, V>
where
    K: redb::Key + 'static,
    V: Archive + for<'a> Serialize<Strategy<Serializer<AlignedVec, ArenaHandle<'a>, Share>, rancor::Error>>,
    V::Archived: rkyv::Deserialize<V, HighDeserializer<rancor::Error>>
        + for<'b> CheckBytes<Strategy<Validator<ArchiveValidator<'b>, SharedValidator>, rancor::Error>>,
{
```

Core methods: `get` returns `Ok(None)` when the table doesn't exist yet (`lib.rs:358-372`); `insert` rkyv-`to_bytes` the value and stores it as a redb `&[u8]` value (`lib.rs:375-388`); `remove` returns `Ok(false)` for a missing table/key (`lib.rs:393-404`); `iter` and `range` **eagerly collect owned rows and close the read txn** before returning, via the `OwnedTableKey` trait (`lib.rs:409-454`, trait at `lib.rs:277-281`). `decode_value` is the single rkyv-`from_bytes` decode point, tagging failures with the table name (`lib.rs:456-461`).

**Implications for the VC library, and the central tension.** rkyv archives are schema-fragile: any field add/remove/reorder changes the byte layout, and `decode_value` will fail loudly (`Error::RkyvDecode { table }`, tested at `kernel.rs:335-352`). This is exactly why a schema migration cannot be a cell/byte diff and must be a typed `SchemaTransition` between two whole rkyv type sets. The `Table<K,V>` design is **perfectly specific** — the type carries meaning, there is no stringly-typed value column. A reusable VC library that wants to log *any* component's records hits the brief's central tension head-on: the log payload is the rkyv bytes of `V`, but the *decoder selector* is the K/V pair on a specific `Table` constant the library does not statically know. Today the K/V type lives in the consumer's `const TABLE: Table<K,V>`; a generic log that stores `(schema-hash, table-id, payload-bytes)` must recover the *typed* `V` to replay — either by being generic over a consumer-supplied `enum` of record families (preserving specificity, the consumer owns the dispatch) or by degenerating into a `&[u8]`-payload + stringly schema-hash store (the forbidden generic-record fallback, `skills/abstractions.md`). `Table<K,V>` shows the kernel keeps specificity by pushing K/V to the call site; the VC library must find the same trick one layer up — a typed family enum, not a string tag. This is the j487 "name the architecture" decision; `storage-and-wire.md:179` says do not spin a broad umbrella Sema crate until that name exists.

`OwnedTableKey` (`lib.rs:277-343`) maps borrowed redb keys to owned forms (`&str -> String`, `&[u8] -> Vec<u8>`, copy types to themselves). A VC library's per-entry `record key` field must use an owned key shape; this trait is the existing owned-key vocabulary to reuse rather than reinvent.

## Transaction helpers

Two closure-scoped helpers keep redb transaction lifetimes from leaking across component boundaries (`lib.rs:558-580`):

```rust
pub fn write<R>(&self, body: impl FnOnce(&WriteTransaction) -> Result<R>) -> Result<R> {
    let txn = self.database.begin_write()?;
    let result = body(&txn)?;
    txn.commit()?;
    Ok(result)
}
pub fn read<R>(&self, body: impl FnOnce(&ReadTransaction) -> Result<R>) -> Result<R> {
    let txn = self.database.begin_read()?;
    body(&txn)
}
```

`write` commits on `Ok`, rolls back (drops the txn uncommitted) on `Err` — tested at `kernel.rs:379-399`. The redb `WriteTransaction`/`ReadTransaction` types are re-exported (`lib.rs:26`) so consumers type their reducers without depending on redb directly (`INTENT.md:24-27`).

**What the VC library needs / changes.** This is the atomicity primitive the *same-file* log arm rides on: appending a log entry and updating the materialized view inside one `write` closure is a single redb commit — atomic, fsync'd, and impossible to half-apply (`ARCHITECTURE.md:53-69` boundary diagram; redb `begin_write` is single-writer). But the closure-scoped design has two frictions for VC: (1) there is no exposed `set_durability` hook — `write` always uses redb's default `Durability::Immediate` (confirmed default at `transactions.rs:1265`), so a VC library cannot ask for a cheaper durability tier through this surface; it gets full fsync-on-commit every time. (2) redb's **savepoints** (`ephemeral_savepoint`/`persistent_savepoint`/`restore_savepoint`, `transactions.rs:1011-1170`) all require `Durability::Immediate` and are not surfaced by `sema` at all — a redb-native "restore to an earlier point" exists but is unreachable through `sema`'s public API. A VC library that wanted to use redb savepoints as a rollback mechanism would need a kernel change to expose them; the design direction (rebuild the view from the authoritative log) deliberately avoids depending on them.

## The Error enum

One typed `thiserror` enum, `pub enum Error` (`lib.rs:42-95`), `#[from]`-wrapping each redb error category (`DatabaseError`, `StorageError`, `TransactionError`, `TableError`, `CommitError`), `std::io::Error`, and rkyv `rancor::Error`, plus domain variants: `RkyvEncode`/`RkyvDecode` (table-tagged), `DatabaseHeaderEncode`/`DatabaseHeaderDecode`, `DatabaseFormatMismatch { expected, found }`, `SchemaVersionMismatch { expected, found }`, and `LegacyFileLacksSchema { path, expected }`. `pub type Result<T>` aliases it (`lib.rs:103`). No `anyhow`, boundary-clean — matches the discipline constraint.

**What the VC library needs / changes.** A reusable VC layer is a *new crate* with its *own* per-crate `Error` (the typed-per-crate-Error rule). It will wrap `sema::Error` via `#[from]` but must add its own variants: log-chain-broken (prev-digest mismatch), schema-hash-unknown-on-replay, checkpoint-range-gap, remote-ack-timeout / RPO-exceeded, digest-verification-failure. `SchemaVersionMismatch` and `LegacyFileLacksSchema` are the kernel's *hard-fail* posture on skew; a VC library that does typed replay-through-migration is precisely the thing that turns those hard-fails into *recoverable* transitions one layer up — the kernel still hard-fails, the VC log carries the reducer that makes the transition legal.

## The version-skew / schema guard — it is TWO guards

The brief says "version-skew guard"; the code has two independent guards, run in sequence on every open (`lib.rs:493-495`):

1. **Database-format guard** — `ensure_database_header` (`lib.rs:510-525`). Compares the stored `DatabaseHeader` against `DatabaseHeader::current()` (`lib.rs:120-128`): `format_version: 1`, `endian: Little`, `pointer_width: PointerWidth32`, `unaligned: true`, `bytecheck: true`. This pins the *rkyv feature set* (matching `Cargo.toml:12`). Mismatch → `DatabaseFormatMismatch` (tested `kernel.rs:93-119`); undecodable header → `DatabaseHeaderDecode` (tested `kernel.rs:121-136`). This guards *byte-layout identity across builds* — if you recompile with different rkyv features, the file refuses to open.
2. **Schema-version guard** — `ensure_schema_version` (`lib.rs:527-552`). Three-way match on `(stored, is_fresh_file)`: stored-and-equal → ok; stored-and-different → `SchemaVersionMismatch` (tested `kernel.rs:159-175`); none-and-fresh → stamp the version; none-and-existing → `LegacyFileLacksSchema`, refusing to retro-stamp (tested `kernel.rs:177-199`). `SchemaVersion` is `u32` wrapped, ordered, `Display` (`lib.rs:193-210`).

**What the VC library needs / changes.** The schema guard is the seam the whole VC effort lives on. Today it is *manual and hard-fail*: bump the constant, hard-fail on mismatch, migrate by full rebuild (`ARCHITECTURE.md:224-233`). The eventual direction (`ARCHITECTURE.md:235-254`, `INTENT.md:61-69`, and the `Status [Concept Active Retired]` lifecycle in `schema/sema.concept.schema`) is **content-addressed**: schema = hash of its Sema source, a runtime holds *multiple schema versions concurrently*, migration is a typed *reducer* from v-old-records to v-new-records. This is the same shape the VC design direction names (`SchemaTransition(v_old_hash -> v_new_hash, reducer)` + checkpoint). So `SchemaVersion(u32)` is the realization-step stand-in for what becomes a *schema-hash* the VC log entry carries as its decoder selector. The format-identity guard is *orthogonal* and should stay — it protects rkyv-feature drift regardless of how schema versioning evolves; the VC library inherits it for free and must not collapse the two (a content-hash of schema source is not the same as the rkyv-build identity).

## The migration mechanism — full rewrite + fs::rename (one layer up)

The brief's `production_migration.rs` (full rewrite + `fs::rename` aside) lives in **`spirit`**, not `sema` — `sema/src/` has no migration file. The kernel's *own* migration story is the manual `SchemaVersion` bump + coordinated rebuild described at `ARCHITECTURE.md:224-233`: "delete the old database, recompile the consumer against the new schema, accept the data loss or run a one-off migrator." Crucially, the kernel offers **no in-place migration primitive at all** — and `ARCHITECTURE.md:136-171` ("Deletion durability — copy-on-write page reuse") establishes that **removal is irreversible at the kernel layer**: redb's copy-on-write page reuse overwrites freed pages within hours (empirically confirmed against the spirit store, `ARCHITECTURE.md:152-159`). There is no undelete, no tombstone, no forensic recovery. `INTENT.md:52-57` makes this a constraint: "A consumer that may need a removed record back must capture it *before* `remove`."

**What the VC library needs / changes — this is the core of the j487 case.** The kernel's posture ("removal is irreversible; migration is full-rebuild-with-data-loss; recoverable deletion is a deliberate higher-layer feature," `ARCHITECTURE.md:161-171`) is an explicit *invitation* for exactly the reusable VC library: the higher layer that makes deletion recoverable and migration non-lossy by keeping the authoritative payload-bearing log so the view is always rebuildable. The kernel will not change this — `ARCHITECTURE.md:87-90` and `INTENT.md:52-57` insist append-only identity and recoverable deletion are *not* kernel surfaces. So the VC library sits at the `sema-engine`-or-above layer, links `sema` as the typed-storage floor, and the *only* plausible kernel changes are narrow: (a) possibly exposing `set_durability` / savepoints if a design arm needs them (currently both are hidden), (b) possibly a `__sema_`-namespace concession if the log is kernel-owned (contradicting current non-goals), and (c) the eventual `SchemaVersion -> schema-hash` evolution the kernel already pre-announces. None of these is decided; the kernel inversion ("demote tables to a materialized view") is the `sema`/`sema-engine` owners' call, and nothing in the kernel today forces it.

## The same-file vs separate-file experiment seam, grounded

The kernel makes the *same-file* arm's cost concrete and cheap: it is already true that any consumer table commits atomically with `__sema_meta`/`__sema_headers` in one `write` closure (`lib.rs:568-573`), single redb writer, fsync-on-commit. A payload-bearing log table added the same way diverges from the view *never* — that is the free-atomicity argument, and it is real here. The *separate-file* arm forgoes all of it: a second file shares no redb transaction, so it needs its own crash-consistency protocol (the `repository-ledger` temp-write+rename spool is the in-workspace prior art for that shape). The tradeoff the matrix must measure: same-file binds the log's compaction/retention to redb's single-file COW reclamation (and to redb 4.1.0 having `compact(&mut self)` at `db.rs:609` but no online-snapshot/backup API, so "ship the log suffix to the server" is a read-the-log-table operation, not a file-level snapshot), while separate-file buys independent log retention and independent shipping at the cost of inventing atomicity that redb otherwise hands you.
