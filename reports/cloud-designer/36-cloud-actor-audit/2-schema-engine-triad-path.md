# 2 — schema-engine triad path (the emitted future runtime)

Workflow dimension `explore:schema-triad`, verified by adversarial thesis-1
(**confirmed**). One correction folded in from thesis-1/thesis-4/completeness:
the realized path is **single-threaded serial**, not "thread-per-connection" — the
`thread::spawn` it appears to use (`triad-runtime/src/workers.rs`) is in
`BoundedWorkers`, which has **zero callers**.

## Headline

The cloud schema-engine path is end-to-end **synchronous** with zero actors, zero
mailboxes, zero supervision, zero kameo/tokio. `NexusEngine::execute` /
`SemaEngine::apply` are plain `&mut self` methods driven on the calling thread by a
synchronous `Runner::drive` continuation loop — a step machine, not an actor
scheduler. The emitted `MultiListenerDaemon` serves connections **strictly serially
on one accept-loop thread**. The shared store is one `Arc<SchemaStore>` (a single
`Mutex<SchemaStoreState>`) cloned per request. The whole path is build/socket-tested
but **NOT wired into the production binary** and does **no live Cloudflare IO** —
`run_effect` returns empty listings (stub); cutover pending.

## The engine traits are synchronous `&mut self` methods — no mailbox

`NexusEngine` / `SemaEngine` (emitted in `src/schema/nexus.rs`, `src/schema/sema.rs`)
are ordinary Rust traits with synchronous, blocking signatures — no `async`, no
`Future`, no channel, no `tell`/`ask`, no spawn.

`src/schema/nexus.rs:655-690` — `NexusEngine`:
```rust
fn apply_sema_write(&mut self, origin_route: OriginRoute, input: CommandSemaWrite) -> SemaWriteCompleted;
fn observe_sema_read(&self, origin_route: OriginRoute, input: CommandSemaRead) -> SemaReadCompleted;
fn run_effect(&mut self, input: CommandEffect) -> EffectCompleted;
fn decide(&mut self, input: nexus::Nexus<nexus::Work>) -> nexus::Nexus<nexus::Action>;
fn execute(&mut self, input: nexus::Nexus<nexus::Work>) -> nexus::Nexus<nexus::Action> where Self: Sized {
    let runner = triad_runtime::Runner::new(self.continuation_limit());
    let mut runner_adapter = NexusRunnerAdapter::new(self, origin_route);
    let reply = runner.drive(&mut runner_adapter, first_work);   // <- synchronous loop
    ...
}
```

`execute` is a default method that constructs a `triad_runtime::Runner` and calls
`runner.drive(...)`. `drive` (`triad-runtime/src/runner.rs:149-185`) is a plain
`loop { match decide_next_step(work) { Reply => return, SemaWrite => …,
SemaRead => …, RunEffect => …, Continue => … } }` — a bounded continuation step
machine (default 32 steps, `runner.rs:3`), all on one stack frame, no yielding, no
message passing. The "Nexus/SEMA" terminology is pure data routing
(`NexusWork`/`NexusAction` enums), **NOT** a concurrent process per plane.
`SemaEngine` (`sema.rs:936-974`) is likewise sync (`apply_inner(&mut self)` /
`observe_inner(&self)`).

## Per-request engine; one execute per signal

`SchemaRuntime::reply_to_signal` (`src/schema_runtime.rs:74-87`) is the per-request
entry the daemon hooks call. It builds a FRESH `SchemaRuntime` per request
(`Self::with_store(store)`), wraps the input as `NexusWork::SignalArrived(...)
.with_origin_route(OriginRoute(0))`, calls `engine.execute(work).into_root()`, and
matches the terminal `NexusAction::ReplyToSignal`. `origin_route` is hardcoded `0`
— no per-origin routing/actor identity; cloud ignores it (`_origin_route`).

## The emitted MultiListenerDaemon serves SERIALLY — BoundedWorkers is NOT used

The emitted spine `GeneratedDaemonRuntime::handle_working_stream`
(`src/schema/daemon.rs:173-182`) is fully synchronous: build `ConnectionContext`
(SO_PEERCRED), read one length-prefixed frame, `Input::decode_signal_frame`,
`Daemon::handle_working_input(&self.engine, input, &connection)`,
`transport.write_frame(output.encode_signal_frame()?)`. Exposed through
`MultiListenerRuntime::handle_stream(&mut self, listener, stream)`
(`src/schema/daemon.rs:209-218`) — note `&mut self`, which structurally forbids
concurrent dispatch from a single runtime instance.

The driver is `triad-runtime`'s `BoundMultiListenerDaemon`. Its serve path is
strictly serial on ONE thread:
- `serve_streams` (`triad-runtime/src/daemon.rs:392-397`): `while should_continue()
  { serve_next_stream()? }`
- `serve_next_stream` (`daemon.rs:382-390`): `while should_continue() { if
  try_serve_next_stream()? { return } thread::sleep(poll_interval) }`
- `try_serve_next_stream` (`daemon.rs:368-380`): iterate listeners,
  `accept_next_stream()` (non-blocking, `daemon.rs:448-454`), and on a hit call
  `self.runtime.handle_stream(listener, stream)` **inline on the accept-loop
  thread**, then `return Ok(true)`.

One connection is fully decoded→executed→encoded before the next is accepted.
Default poll interval 10ms (`daemon.rs:175-176`); `set_nonblocking(true)` on each
listener (`daemon.rs:308`) enables the round-robin poll. **No thread-per-request,
no worker pool, no concurrency.**

`triad-runtime/src/workers.rs` DOES define `BoundedWorkers` (a bounded
thread-per-task dispatcher: `dispatch` acquires a `Mutex+Condvar` permit then
`thread::spawn`s the task, intent `k6w1`). But it is **dead weight on this path** —
`grep` of cloud `src/` finds zero `BoundedWorkers`/`dispatch`/`thread::spawn`
outside the legacy `src/daemon.rs`, and the `MultiListenerDaemon` driver never calls
`dispatch`. The `k6w1` bounded-concurrency intent is realized only as an **unused
library primitive**; the realized cloud schema daemon is single-threaded serial.
(Completeness MISS-6 confirms: BoundedWorkers is wired **nowhere** in the entire
triad stack — as un-realized as the actors.)

## Shared store: one `Arc<SchemaStore>`, cloned per request, single global Mutex

`CloudDaemon::Engine = Arc<SchemaStore>` (`src/schema_daemon.rs:56`). `build_runtime`
makes exactly one (`Arc::new(SchemaStore::new())`, `schema_daemon.rs:68-70`).
`handle_working_input` (`:76-85`) and `handle_meta_stream` (`:92-106`) both call
`SchemaRuntime::reply_to_signal(engine.clone(), ...)` — Arc-clone per request.
`SchemaStore` (`src/schema_store.rs:198-217`) is `{ state: Mutex<SchemaStoreState> }`;
every read/write takes `self.state.lock()` (one global lock covering both
`AccountPolicyTable` and `PlanTable` plus the monotonic `commit_sequence`). Because
the listener loop is serial, two requests never actually contend the mutex on this
path — the Arc/Mutex is forward-looking, not load-bearing today. In-memory only;
`redb`/durable backing is a noted follow-on (`schema_store.rs:11-14`).

## No actor/kameo/mailbox/supervision — but dead actor vocabulary is emitted

cloud `Cargo.toml` has zero `kameo`, zero `tokio`. `triad-runtime` itself has zero
`kameo`/`tokio`/`async`. The ONLY "Actor" tokens are emitted error enums
`ActorStartFailure`/`ActorStopFailure` and lifecycle hooks `on_start`/`on_stop` on
the engine traits (`nexus.rs:578-643`, `sema.rs:899-940`). These are **dead** on
this realization: cloud never implements them, and the triad-runtime driver never
calls them. The emitter carries actor NAMING (start/stop failure phrased as "actor
resource busy") but emits a synchronous step-machine — the names are vestigial of
the actor design `ARCHITECTURE.md` mandates, not a realization of it.

## Where live Cloudflare IO would plug in — and its current stub

The effect plane is the seam: `run_effect(&mut self, input: CommandEffect) ->
EffectCompleted` (`schema_runtime.rs:458-470`). cloud's impl is a pure STUB:
```rust
CloudflareObserveZones(_)   => EffectResult::ZonesObserved(ZoneListing::new(Vec::new())),
CloudflareObserveRecords(_) => EffectResult::RecordsObserved(RecordListing::new(Vec::new())),
CloudflareApplyPlan(id)     => EffectResult::PlanApplied(PlanApplied::new(id)),
```
No `ureq`, no token, no HTTP — empty `Vec::new()` listings and an echoed plan id.
Worse, on the read path the engine never even ASKS for an effect: `observe_ordinary`
(`schema_runtime.rs:217-236`) returns empty listings directly from `decide`, so
`CommandEffect` is never emitted for ordinary observes today. Plan generation is
also stubbed: `PreparePlan`/`PrepareProjection` return `PlanGenerationFailed`
(`:267-272`), and `observe_plan` always `Missed`/`PlanUnknown` (`:238-251`) because
diff-aware plan generation still lives on the legacy `Store` path. Live IO would
land in `run_effect` (and the `decide_*` routing that emits `CommandEffect`),
calling `src/cloudflare.rs` — that cutover is pending.

## Not wired into production at all

`src/bin/cloud-daemon.rs` → `CloudDaemonCommand::run` → `Daemon::new(...).run()` —
the **legacy** `crate::daemon::Daemon`. The schema-engine entry (`CloudDaemon` ZST in
`schema_daemon.rs`) is reached only via the emitted `DaemonEntry` /
`DaemonCommand<CloudDaemon>` or the `SchemaDaemon::new(cfg).run()` wrapper
(`schema_daemon.rs:112-126`) — neither is invoked by any shipped bin; only
`tests/schema_daemon.rs` exercises it. So the emitted runtime is build-verified and
socket-test-exercised but **dormant**: zero production traffic, zero live IO.

## Emitter-controlled vs cloud-hand-written

| Surface | Owner | Evidence |
|---|---|---|
| `ComponentDaemon` trait, `DaemonBinder`, `DaemonCommand`, `GeneratedDaemonRuntime`, decode→execute→encode spine, `MultiListenerRuntime` impl, `DaemonEntry` | EMITTED | `src/schema/daemon.rs` `// @generated`, whole file |
| `NexusEngine`/`SemaEngine` traits, `execute`/`apply`/`observe` defaults, `Runner` adapter, all `Nexus*`/`Sema*` types, `run_effect` signature, actor error enums | EMITTED | `src/schema/nexus.rs:1`, `src/schema/sema.rs:1` `// @generated` |
| Daemon SHAPE (process name, two-tier working+meta listeners, meta socket 0o600) | declared by cloud in `build.rs`, consumed by emitter | `build.rs:109-117` `NexusDaemonShape::new("cloud-daemon", WorkingListenerTier::dependency("signal_cloud::schema::lib")).with_meta_tier(...)` |
| Engine TYPES (`Configuration`/`Engine=Arc<SchemaStore>`/`Error`), `build_runtime`, `load_configuration`, `handle_working_input`, `handle_meta_stream` (record-1488 escape hatches) | HAND-WRITTEN | `src/schema_daemon.rs:48-107` |
| `SchemaRuntime` engine-trait impls + routing | HAND-WRITTEN | `src/schema_runtime.rs` |
| `SchemaStore`/tables/mutex/commit sequence | HAND-WRITTEN | `src/schema_store.rs` |
| `Runner::drive` loop, `BoundMultiListenerDaemon` serial serve loop, `BoundedWorkers` (unused) | triad-runtime dependency | `triad-runtime/src/{runner,daemon,workers}.rs` |

The emitter dictates the **concurrency shape** (it chose `MultiListenerDaemon` +
synchronous spine; cloud cannot change serial-vs-threaded without changing the
emitter or triad-runtime). cloud controls only engine logic and IO seams — so the
actor-absence at the SPINE is an emitter+runtime property. (Dimension 6 shows the
actor-TREE absence behind the spine is still cloud's own choice.)
