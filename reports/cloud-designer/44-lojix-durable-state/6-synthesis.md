# 44 · Lojix durable state (S3) — synthesis & implementation plan

Synthesis of reports 0–5. The mandate is Spirit `oh9l` (durable-first):
replace lojix's in-memory `Mutex<StoreState>` with sema-engine durable
backing and self-resume on restart, *before* the S4 activation cutover
writes live-set / GC-root / event-log mutations against it. Honoured
constraints: no direct redb calls — go through sema-engine (`fosp`);
single-writer with parallel reads (`e440`); virgin-vs-populated resume
(`ur16`); atomic version-controlled backup is the named follow-on (`29pb`).

All citations are `path:line` against jj-colocated checkouts under
`/git/github.com/LiGoldragon/`.

## The one-line shape

Lojix copies spirit verbatim: drop `Mutex<StoreState>` and the in-RAM
counters; `Store` holds a `sema_engine::Engine` plus one `TableReference`
per durable table; `Store::open(path)` opens the engine and re-runs the
same `register_table` calls every boot (fresh file → stamped + genesis
counters; populated file → catalog + counters + records read straight back
from redb). The virgin-vs-populated branch lives inside `sema`/`sema-engine`,
not in lojix. No bespoke persistence or replay code.

## What's mechanical vs what needs real design

The precedent makes most of this a transcription job, but two pieces are
genuinely new for lojix and need decisions.

### Mechanical (copy spirit/mind)

- `Store::open` open + `register_table` shape — verbatim from
  `spirit/src/store.rs:244-259`.
- Self-resume — free; `Engine::open` *is* the resume
  (`sema-engine/src/engine.rs:50-64`). No replay code.
- Commit-sequence / snapshot survival — owned by sema-engine's
  `__sema_engine_counters` (`engine.rs:967-984`); lojix's `commit_sequence`
  RAM counter just deletes.
- `database_path` wiring config → build → open — copy spirit's
  `build_runtime` arm (`spirit/src/daemon.rs:112-139`).
- Single-writer — structural already: lojix serialises through the actor
  mailbox (`daemon.rs:126-132`), not the `Mutex`; removing the `Mutex`
  loses nothing.

### Real design needed

1. **The four tables are value-blobs today, not keyed record families.**
   Each lojix table is a `Vec`-payload newtype mutated by clone-push-rebuild
   (`lib.rs:194-226`). Sema-engine stores *keyed records*, one row per
   element, not one blob per table. So each element type
   (`LiveGeneration`, `GcRoot`, `EventLogEntry`, `ContainerLifecycleRecord`)
   must get an `impl EngineRecord` (a stable `RecordKey`), and the ten
   write/read methods in `schema_runtime.rs` must be re-expressed as
   per-record `assert`/`mutate`/`retract`/`match_records` instead of
   whole-`Vec` rebuilds. This is the bulk of the real work and the main
   place a port can go wrong (key choice, append-only vs mutate semantics).

2. **Three lojix-specific counters have no sema-engine home by default.**
   `deployment_sequence`, `generation_sequence`, `subscription_sequence`
   are domain identifier issuers (`lib.rs:180-225`); the engine only owns
   `commit_sequence`/`snapshot`. Two options, decide per counter:
   `register_identified_table` (engine assigns the auto-id — natural for
   `event_log` position and `live_set` generation id), or a dedicated
   single-row counter record read-modified-write. `next_event_log_position`
   today derives from `event_log.len()` (`lib.rs:190-192`) — with an
   identified table that becomes the assigned id, restart-safe for free.

3. **`state_digest` is faked as the commit sequence** (`schema_runtime.rs:425-437`).
   Durable backing offers a real `current_database_marker()`
   (`engine.rs:984`). Whether to adopt the real marker now or keep the
   commit-sequence stand-in is a wire-contract decision (the marker rides
   `DatabaseMarker`/`StateMarker` on every reply).

4. **S3 vs local file is unresolved at the lojix layer.** The task framing
   says "S3-backed"; the precedent is a local `*.sema` via redb. The
   library API and open/register/resume shape are identical regardless of
   byte store. Whether `sema`'s redb backend points at an S3-mounted path or
   a new `sema` storage backend is needed is a **`sema`-kernel decision, not
   a lojix change** — lojix's `sema_engine::Engine` consumer code is the
   same either way. Flag to psyche; do not build an S3 backend inside lojix
   (that would also risk a direct-storage violation of `fosp`).

## Dependency to add

`lojix/Cargo.toml` has no sema-engine today (`[dependencies]` is
`horizon-lib`, `nota-next`, `meta-signal-lojix`, `signal-lojix`, `rkyv`,
`rustix`, `serde_json`, `thiserror`, `tokio`, `triad-runtime`). Add,
matching the repo's git-branch convention:

```toml
sema-engine = { git = "https://github.com/LiGoldragon/sema-engine.git", branch = "main" }
```

`sema` (`SchemaVersion`, kernel error) and `signal-sema` (`SemaOperation`,
only if lojix inspects the log) arrive transitively through sema-engine's
re-exports (`sema-engine/src/lib.rs:39-58`); add directly only if lojix
names those types itself. Lojix's rkyv pin (`0.8`, std/bytecheck/
little_endian/pointer_width_32/unaligned) matches sema-engine's — no rkyv
conflict. No redb dependency is added to lojix (fosp).

## Changes to `lib.rs` — `Store` / `StoreState`

`StoreState` (`lib.rs:146-226`) **deletes entirely**: the four `Vec`-newtype
table fields, the four `u64` counters, the `Default` impl, and all ten
mutator/derive helpers (`next_commit_sequence` … `next_subscription_token`).
Their logic moves onto `Store` as engine ops.

`Store` (`lib.rs:232-251`) changes from `state: Mutex<StoreState>` to the
spirit shape:

```rust
pub struct Store {
    database: SemaEngine,                       // = sema_engine::Engine alias
    live_set: IdentifiedTableReference<LiveGeneration>,
    gc_roots: TableReference<GcRoot>,
    event_log: IdentifiedTableReference<EventLogEntry>,
    containers: TableReference<ContainerLifecycleRecord>,
    path: PathBuf,
}
```

- Add `const LOJIX_SCHEMA_VERSION: SchemaVersion = SchemaVersion::new(1)`
  and one `const … : TableName` per table (mirrors `spirit/src/store.rs:46-48`).
- `Store::open(path) -> Result<Self>`: `Engine::open(EngineOpen::new(path,
  LOJIX_SCHEMA_VERSION))?` then four `register_table` /
  `register_identified_table` calls. Idempotent on reopen — this *is* the
  resume (no separate load path).
- `Store::new()` (`lib.rs:238-240`) goes away (or becomes a tempdir-backed
  test helper, the analogue spirit/mind keep for tests).
- `Store::lock` (`lib.rs:244`) and the `MutexGuard` API go away. Reads and
  writes are direct `&self` engine calls (the engine's redb write txn is the
  serialization point; `&self` interior mutability — `engine.rs:307-403`),
  so no interior lock and reads can run concurrent (e440 MVCC).
- `commit_sequence` (`lib.rs:248`) → `self.database.current_commit_sequence()?.value()`.
- Add an `is_empty()` / `committed_count()` for the virgin check (the
  `match_records(QueryPlan::all(...))`.len()==0` pattern,
  `spirit/src/store.rs:849-915`).
- The four element types in `schema/sema.rs` already derive the full rkyv
  set; add an `impl EngineRecord for <T>` returning `RecordKey` for the two
  string-keyed tables (`gc_roots`, `containers`). The two identified tables
  use the engine-assigned id.

`Store::new()`'s caller in the daemon (`daemon.rs:143`) and the test
constructor `SchemaRuntime::with_store` (`schema_runtime.rs:405`) are the
two repoint sites.

## Changes to `schema_runtime.rs` — the SemaEngine impl

The whole point of report 1's seam analysis: `SchemaRuntime`, both trait
impls (`NexusEngine` `:1922`, `SemaEngine` `:1981`), `apply_sema`/
`observe_sema` dispatch, `decide` routing, and the per-request
`active_deploy`/`active_operation` cursors **stay unchanged**. Only the
*access verb* inside the seven write and three read method bodies changes —
`self.store.lock()` + guard-mutate becomes a direct `self.store` engine call.

Per method, the rewrite pattern:

- **Writes** (`apply_sema` dispatch, `schema_runtime.rs:910-1166`):
  each `match self.store.lock() { Ok(mut state) => { let commit_sequence =
  state.next_commit_sequence(); state.push_*(…); } }` becomes a
  `self.store.<assert|mutate|retract>(…)?` whose `MutationReceipt` yields
  `commit_sequence()` for the reply marker (`mutation.rs:90-130`). Multi-table
  writes that today commit atomically under one lock (e.g.
  `record_generation_activated` pushes both `live_set` *and* `gc_roots`,
  `:983-1029`) must become one `CommitRequest` batch so atomicity is
  preserved (`mutation.rs:315-355`, `log.rs:9-13`) — **do not** split a
  single logical write into two engine commits.
- `write_rejected(commit_sequence, reason)` (`:1166-1176`) takes the real
  sequence from `self.store.current_commit_sequence()` instead of the
  hard-coded `0` it gets on a lock failure.
- **Reads** (`observe_sema` dispatch, `:1177-1270`): `query_generations`
  (`:1185`), `read_event_log` (`:1234`), `check_key_material` (`:1263`)
  swap `self.store.lock()` + `state.<table>.payload()` for
  `self.store.match_records(QueryPlan::all|key|key_range(…))?.records()`,
  then the same in-memory filter/project logic.
- `marker` / `sema_marker` (`:425-437`): source `commit_sequence` from
  `self.store.current_commit_sequence()`; optionally adopt the real
  `current_database_marker()` for `state_digest` (design item 3 above).

`RuntimeConfiguration` (`schema_runtime.rs:48-50`) currently keeps only
`generated_inputs_directory`. It does **not** need the state path added — the
store is opened from the raw `DaemonConfiguration.state_directory_path` in
`run` (below), and `RuntimeConfiguration` continues to carry only the
nix-materialization root.

## Changes to `daemon.rs` / `DaemonConfiguration`

`DaemonConfiguration.state_directory_path` already exists (`lib.rs:124`) and
is decoded from the binary rkyv startup file (`from_rkyv_file`,
`lib.rs:128-132`) — no NOTA parsing in the daemon, honouring binary-startup-
only. Today it feeds *only* the nix `generated_inputs_directory`
(`schema_runtime.rs:65-68`); it is **not** yet wired to a state DB.

The store open must happen where the full `DaemonConfiguration` is in scope —
`Daemon::run` at `daemon.rs:87`, which builds `LojixRuntime::new(...)`.
Change `LojixRuntime::new` to take the store (or the state path) and open it:

- `daemon.rs:87-89`: pass the state path through. The store lives under the
  state dir, parallel to the existing `generated-inputs` subdir — e.g.
  `PathBuf::from(&configuration.state_directory_path).join("lojix.sema")`.
- `LojixRuntime::new` (`daemon.rs:140-148`): replace
  `store: Arc::new(Store::new())` with
  `store: Arc::new(Store::open(state_database_path)?)`. The fn becomes
  fallible (return `Result`), propagating up through `run`'s existing
  `Result` (`:93-95`). This is the lojix analogue of spirit's
  `build_runtime` non-trace arm: `Store::open(configuration.database_path())?`
  then engine start (`spirit/src/daemon.rs:124`).
- `RequestHandler.store: Arc<Store>` (`daemon.rs:220`),
  `execute_with_store` (`:299-316`), and the per-request
  `SchemaRuntime::with_store_and_configuration` (`schema_runtime.rs:409`)
  all **stay** — they pass `Arc<Store>` by clone exactly as today; only what
  `Store` *is* changed.

Open runs once at owned `&mut` construction before the actor mailbox takes
over (matching spirit's `engine.start()` before serving,
`spirit/src/daemon.rs:105-111`), so no concurrency hazard during resume.

## Self-resume flow (virgin vs populated, `ur16`)

The branch is structural and mostly free — `Engine::open` resumes the
catalog, counters, and records from redb on a populated file and stamps a
fresh one. Lojix's explicit `ur16` obligation is the *configuration* branch
on top of that:

1. Daemon starts with its single binary argument; `from_rkyv_file` decodes
   `DaemonConfiguration` including `state_directory_path`. No manager — self-
   sufficient from the argument (`ur16`).
2. `Store::open(state_database_path)`: `Engine::open` runs the kernel's
   virgin-vs-populated branch (`sema/src/lib.rs:480-508`,
   `is_fresh_file = !path.exists()`; `create_dir_all` on parent so a missing
   dir is fine). The four `register_table` calls are idempotent
   (`engine.rs:71-77`).
3. **Virgin/empty** (committed-count == 0 via
   `match_records(QueryPlan::all(...))`, the spirit `is_empty()` analogue):
   apply the binary `Configure` as first configuration — seed any initial
   GC-roots / configured state from the startup message. Stamp the schema
   version (done by the kernel).
4. **Populated** (committed-count > 0): **do not** re-apply `Configure` as
   init. The four tables and all sequence counters are already in the
   persisted store; sema-engine hands back the resumed catalog, the last
   `current_commit_sequence()`, and the identified-table id counters
   (proven to survive reopen — `sema-engine/tests/engine.rs:204-232,329`).
   Restart-safe identifier issuance falls out for free (closes the
   `lib.rs:175-225` gap where every counter reset to 0 on restart).
5. The same `Configure` message type is accepted live over the meta socket
   (`ur16`) — the virgin-vs-populated decision is the same code path whether
   it fires at boot or from a live meta-signal config message; a virgin
   daemon may start unconfigured and wait for an authenticated binary config.

The detection is a committed-record-count check through sema-engine, **not**
a filesystem stat (spirit `store.rs:849-859`) — honouring "components are
dumb about storage and speak only sema-engine operations" (`fosp`).

## Single-writer + parallel reads (`e440`)

- Single-writer is **already structural**: lojix serialises requests through
  the actor mailbox (`daemon.rs:126-132`), and the engine's redb write txn is
  the commit point. Removing the `Mutex` removes the *read* serialization the
  old single lock imposed, without losing write ordering.
- For parallel reads to actually run concurrent, lojix must (a) keep the read
  path concurrency-safe (it is — `match_records` is `&self`, redb MVCC) and
  (b) raise `BindingSurface::request_concurrency_limit` above the default
  `one()` (`triad-runtime/src/process.rs:113-118`). Lojix already sets a
  concurrency limit (`MAXIMUM_CONCURRENT_REQUESTS`, `daemon.rs:92`) — confirm
  it admits parallel readers and that slow durable IO uses the kameo
  delegated-wait pattern so a long read/write doesn't block the single-writer
  mailbox (the e440 `RequestGate` pattern,
  `triad-runtime/ARCHITECTURE.md:41-50`).

## Backup discipline (`29pb`) — out of scope for S3, noted

The atomic, server-side, version-controlled (Dolt-informed) backup is the
named follow-on, explicitly "under design" (`29pb`). S3/oh9l ships only the
sema-engine backing + self-resume. The hook is `LOJIX_SCHEMA_VERSION` passed
to `EngineOpen::new` — each schema version is a deliberate hard migration
(no backward-compat), so the `.sema` store is a typed versioned database from
the start, not a retrofitted blob. Do not build the backup mechanism in this
stage.

## Ordered implementation steps

1. Add `sema-engine` to `lojix/Cargo.toml` (`branch = main`); confirm rkyv
   pin compatibility; `cargo metadata` to verify no redb leaks into lojix's
   direct deps (only transitive, never called).
2. In `schema/sema.rs`, add `impl EngineRecord` (stable `RecordKey`) for the
   string-keyed element types (`GcRoot`, `ContainerLifecycleRecord`); decide
   identified vs keyed per table (design item 1). rkyv derives already present.
3. Rewrite `Store` in `lib.rs`: `database: SemaEngine` + four
   `TableReference`s + `path`; add `LOJIX_SCHEMA_VERSION` + four `TableName`
   consts; implement `open`, `is_empty`/`committed_count`,
   `current_commit_sequence`, and typed `assert`/`mutate`/`retract`/`commit`/
   `match_records` wrappers for each table. Delete `StoreState`, the `Mutex`,
   the `MutexGuard` `lock`, and all in-RAM counters.
4. Repoint the ten methods in `schema_runtime.rs`
   (`apply_sema` `:910-1166`, `observe_sema` `:1177-1270`) from
   `self.store.lock()` guard-mutate to direct `self.store` engine calls;
   batch the multi-table writes (`record_generation_activated`) into one
   `CommitRequest`; source markers from `current_commit_sequence()`.
5. Wire the open path: thread `state_directory_path` into `LojixRuntime::new`
   (`daemon.rs:140-148`), call `Store::open(state_dir.join("lojix.sema"))?`,
   make `new` and `run` (`:87-95`) propagate the `Result`.
6. Implement the `ur16` virgin-vs-populated configuration branch at boot
   (and the shared path for live meta `Configure`): committed-count check →
   seed-on-virgin / resume-on-populated.
7. Raise/confirm `request_concurrency_limit` for parallel reads; confirm slow
   durable IO uses the kameo delegated-wait so the writer mailbox stays free
   (e440).
8. Update the existing tests (`SchemaRuntime::with_store` `:405`,
   `tempfile` dev-dep already present) to open a tempdir-backed store; add a
   reopen-resume test (assert a deploy, drop, reopen same path, verify the
   live-set + commit sequence + identifier counters survive — the spirit/mind
   reopen-test analogue).
9. Update `lojix/INTENT.md` / `ARCHITECTURE.md` for the durable-state shape on
   the same branch as the work.

## Risk table

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| 1 | Table-blob → keyed-record remodel chooses wrong keys / append vs mutate semantics, corrupting the live-set or event-log | Medium | High | Design item 1 up front; identified tables for append-only `event_log` + id-bearing `live_set`, keyed for `gc_roots`/`containers`; reopen-resume test in step 8 |
| 2 | Multi-table atomic write (`record_generation_activated`) split into two engine commits, losing the one-lock atomicity invariant | Medium | High | Use a single `CommitRequest` batch (`mutation.rs:315-355`); explicit step-4 callout |
| 3 | Domain id counters (deployment/generation/subscription) have no clean sema-engine home; ad-hoc handling reissues ids on restart | Medium | High | Design item 2: identified-table auto-id or dedicated counter record; reopen test asserts monotonic survival |
| 4 | S3 vs local-file substrate undecided; building an S3 path inside lojix would violate `fosp` (direct storage) | Medium | High | Treat as a `sema`-kernel decision (open question); lojix consumer code is byte-store-agnostic; do not build S3 in lojix |
| 5 | Parallel reads not actually enabled (limit stays `one()`) or slow IO blocks the single-writer mailbox | Medium | Medium | Step 7: raise `request_concurrency_limit`, adopt kameo delegated-wait (e440) |
| 6 | `state_digest` faked as commit-sequence diverges from a real durable marker on the wire | Low | Medium | Decide design item 3 explicitly; if adopting `current_database_marker()`, update both `marker`/`sema_marker` together |
| 7 | `LOJIX_SCHEMA_VERSION` bump treated as soft migration; kernel hard-fails on mismatch and a populated store won't open | Low | High | Document version bump = deliberate hard migration (no backward-compat, `29pb`); start at `new(1)` |
| 8 | Fallible `LojixRuntime::new` / `run` error path not threaded, panicking on a bad state dir at boot | Low | Medium | Step 5: propagate `Result` through `run`'s existing `Result`; `create_dir_all` handled by the kernel |

## Open questions for psyche

- **S3 substrate:** is lojix's durable store a local `*.sema` (redb) for the
  oh9l baseline with S3 deferred, or must S3 land now? If now, is that a new
  `sema`-kernel storage backend (the right layer per `fosp`), not a lojix
  change?
- **Schema version start:** begin `LOJIX_SCHEMA_VERSION` at `new(1)` and treat
  every future bump as a hard migration (confirm no backward-compat
  expectation, consistent with the workspace override)?
- **`state_digest`:** adopt sema-engine's real `current_database_marker()`
  now, or keep the commit-sequence stand-in until the marker is needed on the
  wire?
- **Configure-seed contents:** on a virgin store, what initial state does the
  binary `Configure` seed (initial GC-roots? none)? This shapes the virgin
  branch in step 6.
