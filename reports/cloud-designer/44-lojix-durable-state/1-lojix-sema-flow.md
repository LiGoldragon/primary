# lojix current SEMA flow — where durable backing plugs in

Recon for the S3/durable-state work: replace the in-memory `Mutex<StoreState>`
with durable sema-engine backing + self-resume. All citations are
`/git/github.com/LiGoldragon/lojix/<path>:<line>`.

## The state plane today: `Store` + `StoreState` (in-memory)

`StoreState` (`src/lib.rs:145-155`) holds the four SEMA tables plus four
monotonic `u64` counters, all under one lock so a write commits atomically
across tables:

```rust
pub struct StoreState {
    pub live_set: LiveSetTable,
    pub gc_roots: GcRootsTable,
    pub event_log: EventLogTable,
    pub containers: ContainerLifecycleTable,
    pub commit_sequence: u64,
    pub deployment_sequence: u64,
    pub generation_sequence: u64,
    pub subscription_sequence: u64,
}
```

`Store` (`src/lib.rs:232-251`) is the durable-state newtype — currently just
`state: Mutex<StoreState>` with `lock(&self) -> Result<MutexGuard<'_, StoreState>>`
(`:244`) and `commit_sequence(&self) -> Result<u64>` (`:248`). `Store::lock`
is THE single concurrency point: every read and write method on `SchemaRuntime`
calls `self.store.lock()` and mutates / reads the `MutexGuard` directly.

`StoreState` mutators (`src/lib.rs:172-226`): `next_commit_sequence`,
`next_deployment_identifier`, `next_generation_identifier`,
`next_event_log_position` (derives from `event_log.len()`),
`push_event_log_entry`, `push_live_generation`, `push_gc_root`,
`replace_gc_roots`, `push_container_record`, `next_subscription_token`. Each
table push is clone-into_payload-push-rebuild (`:194-198` etc.) — value tables,
not handles.

The four table types (`src/schema/sema.rs:258-317`) are `Vec`-payload newtypes
(`LiveSetTable(Vec<LiveGeneration>)` etc.) and ALL already derive
`rkyv::Archive + Serialize + Deserialize + Clone + Debug + PartialEq + Eq`
(`:258`, `:277`, `:294`, `:316`). Accessors `new/payload/into_payload`
(`src/schema/sema.rs:404-468`). So durable serialization of each table is free.

State digest is currently faked: `marker`/`sema_marker`
(`src/schema_runtime.rs:425-437`) set `state_digest = StateDigest::new(commit_sequence)`
— the digest IS the commit sequence (`StoreState::next_commit_sequence` doc,
`src/lib.rs:173-174`).

## The SemaEngine impls on `SchemaRuntime`

`SchemaRuntime` (`src/schema_runtime.rs:33-42`) is the single data-bearing
engine noun. Fields: `store: Arc<Store>`, `configuration: Arc<RuntimeConfiguration>`,
`active_deploy: Option<DeployPipeline>`, `active_operation: Option<MetaOperation>`.
The last two are PER-REQUEST in-flight cursors; only `store` is shared. Built
per request via `with_store_and_configuration(store, configuration)` (`:409-419`).

There are TWO sema entry points, both delegating to the same hand-written
`apply_sema` / `observe_sema`:

`impl sema::SemaEngine for SchemaRuntime` (`src/schema_runtime.rs:1981-1999`) —
the trait is `src/schema/sema.rs:1291-1329` (`apply_inner`/`observe_inner`
required; `apply`/`observe`/`on_start`/`on_stop`/trace hooks default):

```rust
fn apply_inner(&mut self, input: Sema<WriteInput>) -> Sema<WriteOutput> {
    let origin_route = input.origin_route();
    self.apply_sema(input.into_root()).with_origin_route(origin_route)
}
fn observe_inner(&self, input: Sema<ReadInput>) -> Sema<ReadOutput> { /* observe_sema */ }
```

`impl nexus::NexusEngine for SchemaRuntime` (`src/schema_runtime.rs:1922-1979`)
is what the daemon actually drives — `apply_sema_write(&mut self, _origin_route,
input) -> SemaWriteOutput { self.apply_sema(input) }` (`:1923-1929`),
`observe_sema_read(...) { self.observe_sema(input) }` (`:1931-1937`), plus
`run_effect` (nix IO) and `decide` (the routing brain, `:1966-1978`).

### Write side — `apply_sema` (`src/schema_runtime.rs:910-928`)

Dispatches `SemaWriteInput` to seven methods. EVERY one follows the same shape:
`match self.store.lock() { Ok(mut state) => { let commit_sequence =
state.next_commit_sequence(); ...mutate tables/counters...; build output
}, Err(_) => Self::write_rejected(0, ...) }`. Examples:
`record_deploy_submitted` (`:930-960`, bumps commit+deployment+generation seq,
sets `active_deploy`), `record_phase_transition` (`:962-981`, pushes event-log
entry at `next_event_log_position()`), `record_generation_activated`
(`:983-1029`, `push_live_generation` + `push_gc_root`), `pin/unpin/retire_generation`
(`:1031-1136`, mutate gc_roots / live_set), `record_container_transition`
(`:1138-...`). `write_rejected(commit_sequence, reason)` (`:1166-1176`) never
re-locks.

### Read side — `observe_sema` (`src/schema_runtime.rs:1177-1183`)

Dispatches `SemaReadInput` to `query_generations` (`:1185-1202`, locks, reads
`state.live_set.payload()`, filters, projects), `read_event_log` (`:1234-1261`,
locks, scans `state.event_log.payload()` by range), `check_key_material`
(`:1263-1270`, only reads `commit_sequence`). All take `&self`, call
`self.store.lock()`, read `state.commit_sequence` + table payloads, build a
`SemaReadOutput` with a marker.

## How `Store` is threaded through the daemon

`src/daemon.rs`: `LojixRuntime` (the `AsyncMultiConnectionRuntime` realization)
owns `store: Arc<Store>` (`:134`), constructed once at `Store::new()` (`:143`).
Per connection, a `RequestHandler` holds `store: Arc<Store>` (`:220`);
`execute_request` (`:280-292`) calls `execute_with_store(self.store.clone(),
configuration.clone(), listener, signal_input)` (`:299-316`), which builds a
FRESH `SchemaRuntime::with_store_and_configuration(store, configuration)` per
request (`:305`) and drives `engine.execute(work)` — the generated Nexus
`Runner` continuation loop. `NextStep::SemaRead`/`SemaWrite` are produced by
`decide` (`src/schema_runtime.rs:1966-1978`) as `NexusAction::CommandSemaRead`/
`CommandSemaWrite`, consumed by the runner calling back into
`observe_sema_read`/`apply_sema_write`. There is NO inline per-request `Store`;
`decide` is the only routing truth (`src/daemon.rs:8-10`).

So the request path is: frame → `SignalArrived` → `decide` →
`CommandSemaRead/Write` → `observe_sema/apply_sema` → `self.store.lock()` →
read/mutate `StoreState` → `SemaRead/WriteCompleted` → `decide` → reply (or, for
deploy, a chain of `RunEffect` continuations between phase writes).

## The EXACT seam — what changes vs what stays

The entire durable surface is `Store` + `StoreState` behind `Store::lock`.
`SchemaRuntime` touches state ONLY through `self.store.lock()` (every write/read
method) and `self.store.commit_sequence()`. Make `Store` durable and nothing in
`SchemaRuntime`'s logic, `decide`, the daemon loop, or the wire contract needs
to move.

### Must change

1. `Store` internals (`src/lib.rs:232-251`): swap `Mutex<StoreState>` for a
   durable backing (S3-backed or redb-then-S3). `lib.rs:10-12,230-231` already
   flags "Sema-engine / redb persistence is a noted follow-on."
2. The commit transaction: `StoreState`'s clone-push-rebuild mutators
   (`src/lib.rs:194-226`) must become a durable atomic commit — one write that
   persists the four tables + four counters together (the "one lock so a single
   write commits atomically" invariant, `:142-144`). With S3, this is the
   put-object boundary.
3. `Store::lock` / `StoreState` access API (`:244`): a `MutexGuard` over local
   memory won't survive an S3 backing. Either keep `lock()` returning a guard
   that flushes on drop/commit, OR replace the lock-and-mutate-guard pattern
   with explicit `Store` transaction methods that all current call sites
   (`schema_runtime.rs` writes/reads) route through. The seven write methods and
   three read methods are the call sites to re-point.
4. `state_digest`: today it equals `commit_sequence` (`schema_runtime.rs:427-437`).
   Durable backing wants a real content digest of persisted state.
5. Self-resume: add a load path. Today `Store::new()` is `Default` (empty tables,
   zero counters, `src/lib.rs:157-169`). Durable `Store` must hydrate from the
   backing at construction so counters and tables resume. NOTE
   `DaemonConfiguration.state_directory_path` EXISTS (`src/lib.rs:124`) but is
   currently consumed ONLY as nix `generated_inputs_directory`
   (`schema_runtime.rs:65-68`) — it is NOT yet wired to a state DB. A durable
   `Store` needs its own state location (S3 bucket/prefix or the state dir) fed
   in at `LojixRuntime::new` (`src/daemon.rs:141-145`).
6. `SemaEngine::on_start`/`on_stop` hooks (`src/schema/sema.rs:1292-1297`)
   currently default to `Ok(())` — natural homes for resume-load and
   flush-on-stop if resume is hung off the engine rather than `Store::new`.

### Stays unchanged

- `SchemaRuntime` struct, both trait impls (`NexusEngine` `:1922`, `SemaEngine`
  `:1981`), `apply_sema`/`observe_sema` dispatch, all seven write + three read
  method BODIES' logic — only their `self.store.lock()` access verb may change.
- `decide` routing, the `NextStep::SemaRead/SemaWrite` production/consumption,
  the daemon two-socket loop, `execute_with_store` per-request engine
  construction, `Arc<Store>` sharing (`src/daemon.rs:134,220,305`).
- The four table TYPES (`src/schema/sema.rs:258-317`) — already rkyv-derived, so
  serialization to a durable store is free; no new derives needed.
- The wire contracts (`signal_lojix` / `meta_signal_lojix`), markers, and the
  per-request `active_deploy`/`active_operation` cursors (in-flight, never
  durable).
