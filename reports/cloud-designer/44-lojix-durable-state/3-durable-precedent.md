# Durable precedent — how spirit persists SEMA state and self-resumes

Reconnaissance for the lojix durable-state work: replacing lojix's in-memory
`Mutex<StoreState>` with durable sema-engine backing + self-resume on restart.
This grounds the copyable pattern in the shipped spirit daemon (the primary
precedent with durable intent records) and confirms it against mind (the
sema-engine's first consumer).

All citations are `path:line` against jj-colocated checkouts under
`/git/github.com/LiGoldragon/`.

## Answer in one line

Spirit does NOT touch redb directly and holds NO `Mutex` over state. It opens a
`sema_engine::Engine` (the `SemaDatabase` alias) over a `*.sema` file; the
engine persists every commit (records, the catalog, the commit-sequence/snapshot
counters) into a redb-backed `sema::Sema` kernel. On restart spirit re-runs the
exact same `Engine::open` + `register_table` calls; the engine reads the
persisted catalog and counters back out of redb, so a populated file resumes its
commit sequence and record set with no replay code in spirit. Lojix copies this
three-line open shape verbatim.

## The three layers

| Layer | Repo | Role |
|---|---|---|
| `sema` | `/git/github.com/LiGoldragon/sema` | redb+rkyv kernel: "Typed, version-guarded database kernel over redb and rkyv" (`sema/Cargo.toml`, `redb = "4"`). Owns the file, the schema-version stamp, the fresh-vs-existing branch. |
| `sema-engine` | `/git/github.com/LiGoldragon/sema-engine` | Commit-log / catalog / counters / subscriptions layer over `sema::Sema`. Owns `Engine::open`, `register_table`, `current_commit_sequence`, assert/mutate/retract, `match_records`. |
| `spirit::Store` | `/git/github.com/LiGoldragon/spirit/src/store.rs` | Thin domain mapping: generated SEMA roots -> engine ops. Holds NO lock and NO in-memory record map. |

## 1. Store open + table registration (the copyable shape)

`spirit/src/store.rs:244-259` — `Store::open`:

```rust
pub fn open(path: impl Into<PathBuf>) -> Result<Self, StoreError> {
    let path = path.into();
    let mut database =
        SemaDatabase::open(EngineOpen::new(path.clone(), SPIRIT_SCHEMA_VERSION))?;
    let entries = database.register_table(TableDescriptor::new(ENTRIES_TABLE))?;
    let referents = database.register_table(TableDescriptor::new(REFERENTS_TABLE))?;
    Ok(Self { database, entries, referents, path, archive_target: ArchiveDatabaseTarget::Default, .. })
}
```

- `SemaDatabase` is `sema_engine::Engine` (import alias, `store.rs:7-8`).
- `SPIRIT_SCHEMA_VERSION = SchemaVersion::new(8)` (`store.rs:46`); table names are
  `TableName::new("records")` / `"referents"` (`store.rs:47-48`).
- `Store` fields are just `database: SemaDatabase`, two `TableReference<...>`, and
  the `path` (`store.rs:63-71`). No `Mutex`, no `Vec`/`BTreeMap` of records —
  every read goes to the engine (e.g. `records()` at `store.rs:909-915` calls
  `self.database.match_records(QueryPlan::all(self.entries))`).
- The doc comment makes the ownership explicit (`store.rs:54-62`): "sema-engine
  owns the database handle, durable commit sequence, and typed rkyv table access."

The archive (a SEPARATE `*.sema` file for retired records) uses the identical
shape (`store.rs:1264-1269`): `SemaDatabase::open(EngineOpen::new(path, SPIRIT_SCHEMA_VERSION))`
then `register_table`. So the pattern is "open one engine per durable file."

## 2. Read / write are direct engine calls (no lock)

- Write/assert (`store.rs:446-449`): `self.database.assert(Assertion::new(self.entries, StoredRecord::new(id, entry)))`.
- Update (`store.rs:746-749`): `self.database.mutate(Mutation::new(self.entries, StoredRecord::new(id, entry)))`.
- Delete (`store.rs:698-707`): `self.database.retract(Retraction::new(self.entries, RecordKey::new(id)))`,
  matching `Err(sema_engine::Error::RecordNotFound { .. }) => Ok(false)`.
- Read by key (`store.rs:684-692`): `self.database.match_records(QueryPlan::key(self.entries, RecordKey::new(id)))`.
- Read all (`store.rs:909-915`): `QueryPlan::all(self.entries)`.

Records persist as rkyv-derived structs the engine stores; spirit's
`StoredRecord` derives `rkyv::Archive/Serialize/Deserialize` and impls
`EngineRecord` to give the key (`store.rs:73-77`, `1022-1026`).

## 3. Self-resume — the virgin-vs-populated branch (Spirit ur16)

There is no hand-written replay in spirit. Resume is structural, branching at two
levels:

**Kernel level — `sema/src/lib.rs:480-508` `Sema::open_with_schema`:**

```rust
let is_fresh_file = !path.exists();
let database = Database::create(path)?;   // redb create-or-open
...
Self::ensure_schema_version(&mut meta, schema.version, is_fresh_file, path)?;
```

Fresh files get the schema version stamped; existing files are read back and a
mismatch hard-fails (`ensure_schema_version`, `sema/src/lib.rs:527+`). `create_dir_all`
on the parent means the daemon can start against a path whose directory does not
yet exist.

**Engine level — `sema-engine/src/engine.rs:50-64` `Engine::open`:** after opening
the kernel it reads the persisted catalog back:

```rust
let registrations = storage
    .read(|transaction| CATALOG.iter(transaction))?
    .into_iter().map(|(_key, registration)| registration).collect();
let catalog = Catalog::new(registrations);
```

So on a populated file the engine already knows its tables; `register_table` is
idempotent — it only writes the catalog row `if !self.catalog.is_registered(...)`
(`engine.rs:71-77`). Re-running the same registration calls on restart is a no-op
against an existing file and a create against a fresh one.

**Commit sequence resume — `sema-engine/src/engine.rs:967-975`
`current_commit_sequence`:**

```rust
COUNTERS.get(transaction, LATEST_COMMIT_SEQUENCE_KEY)?
    .map(crate::CommitSequence::new)
    .unwrap_or_else(crate::CommitSequence::genesis)
```

The counter lives in the durable `__sema_engine_counters` redb table
(`engine.rs:30-31`). Every commit persists it inside the same write transaction
that lands the record (`engine.rs:143-148`, also `214-219`): `COUNTERS.insert(.., LATEST_COMMIT_SEQUENCE_KEY, ..)`
+ `LATEST_SNAPSHOT_KEY`. So a virgin store reads `genesis()` (0); a populated
store reads the last persisted value — automatic self-resume of the counter, no
spirit code. Spirit surfaces it via `database_marker()` (`store.rs:863-874`),
reading `commit_sequence()` -> `self.database.current_commit_sequence()`
(`store.rs:872-874`).

`len()` / `is_empty()` likewise compute from live engine reads
(`store.rs:849-859`), so "how many records on restart" is answered by querying
the resumed file, never by an in-memory counter.

## 4. database_path wiring: config -> build_runtime -> Store::open

The path flows from the binary `DaemonConfiguration` into the open with no flags:

- `signal-spirit`'s archived `SpiritDaemonConfiguration` carries a
  `ConfigurationPath` for the database; spirit's runtime `Configuration` wrapper
  decodes it into a `database_path: PathBuf` (`spirit/src/config.rs:18-26`,
  populated at `config.rs:56-68` via `PathBuf::from(raw.database_path())`).
- `Configuration::from_binary_path` reads the pre-generated rkyv config file
  (`config.rs:97-106`) — the daemon never parses NOTA (matches the
  binary-startup-only daemon rule).
- The emitted daemon spine calls `build_runtime` (`spirit/src/daemon.rs:112-139`),
  whose non-trace arm is exactly:

```rust
let store = Store::open(configuration.database_path())?;
Engine::new(store)
```

  then `engine.start()` runs the SEMA -> Nexus -> Signal `on_start` chain at owned
  `&mut` construction BEFORE the engine is handed to the schema-emitted actor
  (`daemon.rs:108-138`). `configuration.database_path()` returns `&Path`
  (`config.rs:82-84`); the same accessor is exposed through `BindingSurface`
  (`config.rs:119-135`) for the spine's listener/store binding.

## 5. Confirmed against mind (second consumer, identical shape)

`mind/src/tables.rs:143-163` opens the same way:

```rust
let mut engine = Engine::open(Self::engine_open(store))?;     // EngineOpen::new(path, MIND_SCHEMA_VERSION)
...
let thoughts = engine.register_table(TableDescriptor::new(THOUGHTS))?;
let relations = engine.register_table(TableDescriptor::new(RELATIONS))?;
```

Mind's `MindEngine::open(StoreLocation::new(configuration.database_path()))`
(`mind/src/daemon.rs:115`, `configuration.rs:78`) shows the same config->path->open
wiring. Mind additionally registers a `VersioningPolicy` via
`EngineOpen::with_versioning` (`tables.rs:160-169`) — optional; spirit does not.

## Copyable pattern for lojix

1. Drop `Mutex<StoreState>` and the in-memory map entirely. Lojix's store struct
   holds `database: sema_engine::Engine` + one `TableReference<T>` per durable
   table + `path: PathBuf`. No interior lock; the engine's own write transactions
   are the serialization point. (Spirit serializes higher up via the
   schema-emitted `EngineActor` mailbox — `daemon.rs:108-111` — so the engine sees
   one request at a time; lojix should keep the same actor-mailbox discipline
   rather than reintroducing a `Mutex`.)
2. `open(path)`: `let mut database = Engine::open(EngineOpen::new(path, LOJIX_SCHEMA_VERSION))?;`
   then one `database.register_table(TableDescriptor::new(NAME))?` per table.
   Define a `const LOJIX_SCHEMA_VERSION: SchemaVersion` and `const ... : TableName`.
3. Each stored value derives `rkyv::Archive/Serialize/Deserialize` + impls
   `EngineRecord` (return the key via `RecordKey::new(...)`).
4. Writes -> `database.assert` / `database.mutate` / `database.retract`; reads ->
   `database.match_records(QueryPlan::key(...))` or `QueryPlan::all(...)`. No
   bespoke persistence code.
5. Self-resume is free: on restart call the identical `open` + `register_table`.
   Fresh file -> stamped + genesis counters; existing file -> catalog + counters +
   records read straight back from redb. The virgin-vs-populated branch lives in
   `sema`/`sema-engine`, not in lojix.
6. Wire `database_path` from lojix's binary `DaemonConfiguration` into
   `build_runtime` exactly as spirit does: decode the rkyv config, call
   `Store::open(configuration.database_path())`, run `engine.start()` at `&mut`
   construction before the actor takes over.

Note: lojix is S3-backed per the task framing, whereas this precedent is a local
`*.sema` file via redb. The library API and the open/register/resume *shape* are
identical regardless of the underlying byte store; the open question for lojix is
only whether `sema`'s redb backend is pointed at an S3-mounted path or whether a
new `sema` storage backend is needed — that is a `sema`-kernel decision, not a
change to the `sema_engine::Engine` consumer pattern spirit demonstrates.
