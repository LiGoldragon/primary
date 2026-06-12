# Lojix durable state — self-resume on restart + backup discipline

Read-only reconnaissance for the lojix S3/durable-state implementation:
replacing the in-memory `Mutex<StoreState>` with sema-engine durable
backing plus self-resume on restart. Every claim is grounded in a Spirit
record, a source read, or a command run.

## The five Spirit records

- **oh9l** (Decision, durable-first) — "build the durable database backing
  now as baseline work before the real cutover: the daemon
  live-generation-set, GC-roots, and event-log state persisted on
  sema-engine with self-resume on restart, rather than running a first
  cutover on in-memory state. … Resolves the in-memory-versus-durable-first
  question in favour of durable-first." Durable-first is the mandate; the
  in-memory `Mutex<StoreState>` is the thing being replaced, not shipped.

- **fosp** (Correction, sema-engine exclusivity) — "Sema-engine is the
  exclusive interface to the database. No component daemon may make direct
  redb calls … A daemon that opens redb and runs its own transactions
  directly is wrong, even as a pilot, and counts as a fake … Components are
  dumb about storage and speak only sema-engine operations." Lojix must
  reach durability through sema-engine, never redb directly.

- **e440** (Decision, single-writer / parallel-reads) — "SEMA engine
  implements durable state as a single-writer actor: queries, writes,
  mutations, additions. Database upgrade operations flow through SEMA …
  Reads run in parallel — redb supports concurrent MVCC reads; the
  single-writer invariant applies to writes only." The current single
  `Mutex<StoreState>` serialises reads too; the durable shape keeps one
  writer but lets reads run concurrent (MVCC).

- **ur16** (Decision, VeryHigh/Maximum — bootstrap + resume) — "The daemon
  opens the store named in the `Configure`: if the store is virgin/empty it
  applies the `Configure` as first configuration; if the store is already
  populated it SELF-RESUMES from the persisted store rather than re-waiting.
  … bootstrap depends on NO manager … self-sufficient at boot from its
  argument. The same `Configure` message type is accepted live over the
  meta socket." This is the exact virgin-vs-populated branch lojix must
  implement.

- **29pb** (Constraint, High/High — backups) — "Component Sema databases,
  the daemon durable state, must be backed up to a server atomically, and
  state loss is unacceptable. Pursue native version-controlled component
  databases rather than treating the store as an opaque binary blob.
  Mechanism is under design and Dolt-informed, with the strict-typed
  hard-migration-per-schema-change shape as the core constraint to solve."
  Backup is atomic, server-side, version-controlled (Dolt-informed), not a
  blob copy.

## The precedent: spirit (agent 3) virgin-vs-populated resume

Spirit is the reference implementation. Its store opens through sema-engine
and lets the engine resume persisted state — no redb in the daemon.

- `Store::open` (`spirit/src/store.rs:244-259`) opens via
  `SemaDatabase::open(EngineOpen::new(path.clone(), SPIRIT_SCHEMA_VERSION))`
  then `database.register_table(TableDescriptor::new(ENTRIES_TABLE))` /
  `REFERENTS_TABLE`. The doc-comment states the resume contract:
  "A fresh file is created with empty engine counters; an existing file
  resumes its persisted commit sequence and record identifier counter
  through sema-engine." (`store.rs:241-243`).

- Boot uses the configured path, no manager: the daemon's `build_runtime`
  calls `Store::open(configuration.database_path())` (`spirit/src/daemon.rs:124`)
  then `engine.start()` (`daemon.rs:137`). Engine startup takes exclusive
  `&mut` once at owned construction, before the mailbox actor serialises
  later requests (`daemon.rs:105-111`).

- Virgin-vs-populated detection is a committed-record-count check, not a
  filesystem stat: `is_empty()` → `len() == 0` → `committed_record_count()`
  → `self.records()?.len()` (`store.rs:849-859`), where `records()` runs
  `self.database.match_records(QueryPlan::all(self.entries))` through
  sema-engine (`store.rs:909-915`). An empty store digests to `(0, 0)`
  (`store.rs:876-881`).

- Sequence/counter survival: spirit does not keep its own `u64` counter in
  RAM. The commit sequence is read back from sema-engine on demand —
  `commit_sequence()` → `self.database.current_commit_sequence()?.value()`
  (`store.rs:872-874`), surfaced in `database_marker()` (`store.rs:861-870`).
  Sema-engine owns the persisted monotonic sequence: `EngineOpen::new(path,
  version)` (`sema-engine/src/engine.rs:1359-1366`), `Engine::open`
  (`engine.rs:50`), `current_commit_sequence` (`engine.rs:967`), and the
  next-sequence helper `current_commit_sequence()?.next()` (`engine.rs:1089`).

## Lojix today: in-memory, no path, no resume

- `Store` is `state: Mutex<StoreState>` (`lojix/src/lib.rs:232-235`), built
  by `Store::new()` → `Self::default()` (`lib.rs:238-240`), which the daemon
  wraps as `Arc::new(Store::new())` (`lojix/src/daemon.rs:143`). Nothing in
  the construction path reads `configuration.state_directory_path`
  (the field exists at `lib.rs:124`) — the store is born empty every boot.

- `StoreState` (`lib.rs:146-155`) holds the four tables —
  `live_set: LiveSetTable`, `gc_roots: GcRootsTable`,
  `event_log: EventLogTable`, `containers: ContainerLifecycleTable` — plus
  four in-RAM sequence counters: `commit_sequence`, `deployment_sequence`,
  `generation_sequence`, `subscription_sequence`. `Default` zeroes all four
  counters and empties all four tables (`lib.rs:157-170`).

- The counters advance purely in memory: `next_commit_sequence`
  (`lib.rs:175-178`), `next_deployment_identifier`, `next_generation_identifier`,
  `next_subscription_token` all do `self.<field> += 1`
  (`lib.rs:180-225`); `next_event_log_position` derives from
  `event_log.payload().len()` (`lib.rs:190-192`). On restart every one of
  these resets to 0 — identifiers would be reissued, corrupting the log.

- Lojix has **no sema-engine dependency** today: `lojix/Cargo.toml`
  `[dependencies]` lists only `horizon-lib`, `nota-next`,
  `meta-signal-lojix`, `signal-lojix`, `rkyv` (run: `sed` over Cargo.toml);
  no `sema_engine`/`redb`/`SemaDatabase`/`EngineOpen` imports anywhere in
  `lojix/src/*.rs` (run: `rg`). Adding the sema-engine dependency is a
  prerequisite; doing it through redb directly would violate fosp.

## Concrete self-resume flow lojix needs

1. **Add the sema-engine dependency** and replace `Mutex<StoreState>` with a
   sema-engine-backed `Store` mirroring `spirit::Store` — `database:
   SemaDatabase` plus four `TableReference`s, one per lojix table. No redb in
   lojix (fosp).

2. **Open at the configured path at boot.** In the daemon's runtime build
   (the lojix analogue of `spirit/src/daemon.rs:124`), call
   `Store::open(configuration.state_directory_path)` instead of
   `Store::new()` (`lojix/src/daemon.rs:143`). Open is
   `SemaDatabase::open(EngineOpen::new(path, LOJIX_SCHEMA_VERSION))`
   (`sema-engine/src/engine.rs:50,1366`), then register the four tables —
   live-set, gc-roots, event-log, container-lifecycle. Self-sufficient from
   the single argument, no manager (ur16).

3. **Detect virgin vs populated** the spirit way: a committed-count check
   over the engine (`match_records(QueryPlan::all(...))`, the analogue of
   `store.rs:909`), not a filesystem stat. Branch:
   - **Virgin/empty** → apply the `Configure` as first configuration (seed
     any initial GC-roots / configured state from the binary `Configure`
     message).
   - **Populated** → self-resume: do **not** re-apply `Configure` as init;
     the four tables and the sequence counters are already in the persisted
     store (ur16).

4. **Resume the four tables and the sequence counters from the persisted
   store.** Tables come back by reading them through sema-engine on demand
   (the spirit `records()`/`referents()` pattern, `store.rs:909-923`).
   Sequence counters must move OFF the in-RAM `u64` fields onto
   sema-engine's persisted monotonic sequence: derive the next value from
   `current_commit_sequence()?.next()` (`engine.rs:967,1089`), exactly as
   spirit's `database_marker()`/`commit_sequence()` do
   (`store.rs:861-874`). Any lojix-specific counter that must survive
   (deployment / generation / subscription) becomes persisted store state
   read back at use, not a RAM field reset to 0 by `Default`. This is what
   makes restart-safe identifier issuance work (the gap at `lib.rs:175-225`).

5. **Single-writer, parallel-reads** (e440): the durable `Store` keeps one
   writer (the SEMA actor), but reads no longer serialise behind the single
   `Mutex` — they run as concurrent MVCC reads through sema-engine, matching
   spirit and the cloud precedent.

## Backup discipline (29pb)

- **Atomic, server-side, version-controlled.** The lojix `.sema` durable
  state (the four tables) must back up to a server atomically; state loss is
  unacceptable (29pb). The intended mechanism is a native
  version-controlled component database (Dolt-informed), not an opaque
  binary-blob copy — so backups carry typed, diffable history rather than a
  byte snapshot.

- **Schema-change shape is the open hard problem.** 29pb names the core
  constraint to solve as the strict-typed hard-migration-per-schema-change
  shape: each lojix schema version is a hard migration (the substrate is
  ground truth; no backward-compat — workspace `Hard overrides`,
  `spirit-cli.md:250-282` substrate-migration discipline). The
  `LOJIX_SCHEMA_VERSION` passed to `EngineOpen::new(path, version)` is the
  hook that pins which schema the durable file resumes under; a version bump
  is a deliberate hard migration, mirroring spirit's
  `SPIRIT_SCHEMA_VERSION = SchemaVersion::new(8)` (`store.rs:46`).

- **Status:** 29pb explicitly marks the backup mechanism "under design."
  Lojix's immediate durable-state work (oh9l baseline) ships the
  sema-engine backing + self-resume; the atomic server backup and the
  version-controlled-database mechanism are the named follow-on, designed so
  the `.sema` store is a typed versioned database from the start (not
  retrofitted from a blob).

## Source map

- `spirit/src/store.rs:46,241-259,840-915` — precedent open / virgin check /
  commit-sequence read-back.
- `spirit/src/daemon.rs:105-139` — precedent boot: open at configured path,
  `engine.start()`.
- `sema-engine/src/engine.rs:50,66,775,967,1089,1359-1366` — `EngineOpen`,
  `open`, `register_table`, `match_records`, `current_commit_sequence`.
- `lojix/src/lib.rs:118-251` — `DaemonConfiguration.state_directory_path`,
  `StoreState` (four tables + four counters), in-RAM `Mutex<StoreState>`.
- `lojix/src/daemon.rs:133-148` — `LojixRuntime { store: Arc<Store> }`,
  `Store::new()` at boot (no path, no resume).
- `lojix/Cargo.toml` `[dependencies]` — no sema-engine yet.
