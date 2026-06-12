# triad-runtime SEMA layer — what the daemon must supply for durable state

Recon for the lojix durable-state (S3) work: replacing lojix's in-memory
`Mutex<StoreState>` with durable sema-engine backing + self-resume on restart.
Repo: `/git/github.com/LiGoldragon/triad-runtime` (jj parent `6ea83162`,
`triad-runtime: rename DaemonConfiguration trait to BindingSurface`).

## Headline: the store is daemon-owned, not runtime-owned

`triad-runtime` routes typed SEMA ops; it never owns, opens, or persists a
store. Three independent confirmations:

1. **`Cargo.toml` has zero storage dependencies.** Deps are only `kameo`,
   `rustix`, `signal-frame`, `thiserror`, `tokio` (Cargo.toml:11-16). No
   sqlite/rocksdb/sled/redb/S3 crate anywhere. A runtime that owned durable
   state would carry a storage backend.

2. **The runner is fully generic over storage — it holds no state at all.**
   `Runner` is `struct Runner { continuation_limit: ContinuationLimit }`
   (`src/runner.rs:69-71`) — a `Clone, Copy` value with only a step budget.
   `Runner::drive` (runner.rs:157-197) loops over `NextStep`, and on a
   storage outcome it just calls back into the component-supplied engine:
   - `NextStep::SemaWrite(write) => work = engines.apply_sema_write(write).await;`
     (runner.rs:171-176)
   - `NextStep::SemaRead(read) => work = engines.observe_sema_read(read).await;`
     (runner.rs:177-182)
   The runner does not read or mutate any store; it sequences typed ops and
   threads `Work` back through the engine.

3. **The runtime only exposes a `database_path()` accessor — the engine opens
   it.** `BindingSurface::database_path(&self) -> &Path` is documented as
   "The durable database path **the engine opens at startup**"
   (`src/process.rs:133-134`). The trait doc says the emitted `Daemon::run`
   uses it to "open the database … without the emitter naming
   component-specific accessor methods" (process.rs:95-100). ARCHITECTURE.md
   makes the boundary explicit: the runtime "does not know about generated
   Signal roots, rkyv archives, NOTA, SEMA tables, trace configuration, or
   policy meaning" (ARCHITECTURE.md:185-188) and "does not … own component
   storage tables" (ARCHITECTURE.md:298-300).

So for lojix: triad-runtime gives you the SEMA op routing + sequencing loop.
The durable store (S3 backing, self-resume from persisted SEMA state) is
lojix's own engine to build and own. The runtime hands you the
`database_path` / configuration surface and the typed-op dispatch; everything
about *where and how* state is durable is the daemon's responsibility.

## The exact traits the daemon implements

### Plane-marker traits (`src/role.rs`)
Pure marker traits the component's generated SEMA roots implement:

```rust
pub trait SemaWriteInput {}   // role.rs:5
pub trait SemaWriteOutput {}  // role.rs:7
pub trait SemaReadInput {}    // role.rs:9
pub trait SemaReadOutput {}   // role.rs:11
```

ARCHITECTURE.md:164-167: generated roots like `CommandSemaWrite` /
`CommandSemaRead` implement `SemaWriteInput` / `SemaReadInput`; "the concrete
enum variants remain component-specific; the reusable name is the trait the
runtime sees." `std::convert::Infallible` impls all four (role.rs:35-41) so a
component with no SEMA plane can use `Infallible`.

### `NexusAction` (`src/role.rs:17-25`) — projects a typed action into a step
```rust
pub trait NexusAction: Sized {
    type Reply;
    type SemaWrite: SemaWriteInput;
    type SemaRead: SemaReadInput;
    type Effect: NexusEffectCommand;
    type Work: NexusWork;
    fn into_next_step(self) -> NexusActionNextStep<Self>;
}
```

### `RunnerEngines` (`src/runner.rs:34-58`) — the real SEMA behavior surface
This is the adapter the daemon's engine satisfies (the adapter itself is
schema-emitted glue, but it forwards to the component's hand-written engine
methods). The durable-state-bearing methods:

```rust
pub trait RunnerEngines {
    type Reply;
    type SemaWrite: SemaWriteInput;
    type SemaRead: SemaReadInput;
    type Effect: NexusEffectCommand;
    type Work: NexusWork;

    fn decide_next_step(&mut self, work: Self::Work) -> RunnerNextStep<Self> where Self: Sized;

    fn apply_sema_write(&mut self, write: Self::SemaWrite)
        -> impl Future<Output = Self::Work> + Send + '_;   // runner.rs:45-48

    fn observe_sema_read(&mut self, read: Self::SemaRead)
        -> impl Future<Output = Self::Work> + Send + '_;    // runner.rs:50-53

    fn run_effect(&mut self, effect: Self::Effect)
        -> impl Future<Output = Self::Work> + Send + '_;

    fn budget_exhausted_reply(&self, exhausted: ContinuationExhausted) -> Self::Reply;
}
```

`apply_sema_write` and `observe_sema_read` are where lojix's durable store
lives. They take `&mut self` and return a `Future` — so the engine that
implements `RunnerEngines` *is* where the durable backing belongs. This is
the seam where `Mutex<StoreState>` gets replaced: `apply_sema_write` is the
write path that must commit durably (to S3), `observe_sema_read` the read
path. Both are `async`, so DB/network IO is a first-class awaited step, not a
hidden sync callback (ARCHITECTURE.md:121-123; INTENT.md:93-94).

### Top-level lifecycle traits the daemon also implements
- `DaemonRuntime` (`src/daemon.rs`, re-exported lib.rs:35-40): `start` /
  `handle_stream` / `stop`. ARCHITECTURE.md:177-188 — `start` runs "before
  the listener begins serving," the natural place for **self-resume from
  persisted SEMA state on restart**.
- `BindingSurface` (`src/process.rs:101`, re-exported lib.rs:42) — the
  configuration surface exposing `database_path()` (process.rs:134) plus
  socket paths.
- `AsyncConnectionRuntime` / `AsyncMultiConnectionRuntime` for the async
  task-backed shell (lib.rs:26-34).

## Commit / sequencing model

The runner serializes one engine through a recursive single-loop budget
(`Runner::drive`, runner.rs:157-197). Each non-`Reply` outcome
(`SemaWrite`, `SemaRead`, `RunEffect`, `Continue`) spends one step of a typed
`ContinuationBudget` (runner.rs:172-194); default limit 32 non-reply steps
(`DEFAULT_CONTINUATION_LIMIT_COUNT`, runner.rs:5). When exhausted the runner
refuses further storage/effect steps and asks the engine for
`budget_exhausted_reply` (runner.rs:172-173, ARCHITECTURE.md:132-136).

SEMA commits are **sequenced by the `&mut self` engine actor**, not by the
runner. A single request drives a synchronous chain: `decide_next_step` →
`SemaWrite`/`SemaRead` → engine mutates/observes → returns next `Work` →
loop. Because each `RunnerEngines` method is `&mut self`, only one SEMA op of
one request executes at a time *within that engine*; ordering is the program
order of the action's `NextStep` projection. There is no
write-ahead-log/commit primitive in the runtime — durable commit semantics
(atomicity, S3 PUT, fsync, resume point) are entirely lojix's to define
inside `apply_sema_write`.

## Concurrency pattern: single-writer engine + delegated waits (Spirit e440)

ARCHITECTURE.md:35-50 and INTENT.md:20-43 describe the actor pattern (Spirit
e440, single-writer-with-parallel-reads). The runtime's expression of it:

- **One engine owner = the single writer.** INTENT.md:136-140: "the one
  runtime owner remains the component boundary for generated Nexus execution
  and **SEMA single-writer semantics**." The `RunnerEngines` `&mut self`
  methods enforce serialized writes against the engine's state.

- **The delegated-wait pattern keeps the writer's mailbox free during slow
  IO.** `RequestGate` is "a data-bearing Kameo actor that accepts permit
  requests and delegates the actual wait through `Context::spawn`"
  (ARCHITECTURE.md:41-50). The architecture explicitly calls this "the
  runtime pattern downstream schema emitters should copy **for storage** and
  child-process effects: accept the typed message, update actor state, return
  a delegated typed reply, and let the slow wait happen outside the actor
  handler" (ARCHITECTURE.md:45-50). For lojix this is the model: a slow S3
  read/write should be a delegated `DelegatedReply` (kameo, async_runtime.rs:18)
  so a long durable IO does not block the single-writer mailbox.

- **Parallel reads via per-listener admission, not runtime-managed read
  replicas.** Concurrency is capped per listener through
  `RequestConcurrencyLimit` / `RequestPermitPool` (a Tokio semaphore,
  async_runtime.rs:44-57). `BindingSurface::request_concurrency_limit`
  defaults to `one()` and notes the default "preserves single-request
  behavior for components that have not audited … parallel database access"
  (process.rs:113-118) — i.e. to get parallel reads, lojix must raise this
  limit AND make its read path safe for concurrency itself. The runtime
  gives the admission dial; it does not split reads from writes for you.

## Takeaway for lojix durable-state

1. Replace `Mutex<StoreState>` inside the engine that implements
   `RunnerEngines`: `apply_sema_write` becomes the durable (S3) commit path,
   `observe_sema_read` the read path — both already `async`/`Send`.
2. Implement self-resume in `DaemonRuntime::start` (runs before serving):
   read the persisted SEMA state from `BindingSurface::database_path()` /
   the S3 location and rebuild engine state.
3. Single-writer is structural (`&mut self` engine). For parallel reads,
   raise `request_concurrency_limit` and make the read path concurrency-safe;
   delegate slow S3 IO with kameo's `DelegatedReply` so the writer mailbox
   stays responsive (the e440 pattern).
4. triad-runtime adds no store crate — pick lojix's S3/durable backend in
   lojix's own Cargo.toml.
