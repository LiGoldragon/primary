# 31 — concurrency primitive extracted to the shared runtime (`BoundedWorkers`)

cloud-designer lane, 2026-06-06. Psyche questions: "is the logic of that
concurrency put into a reusable shared component?" and "how does this relate to
the multi-listener daemon object?" Honest answer to the first: originally no —
it was lojix-local. This report records the fix (intent `k6w1`) and the design
reasoning behind WHERE it went.

## What was wrong

The bounded thread-per-connection concurrency (report 30) lived inside lojix's
`daemon.rs` (`ConnectionPermits` + the spawn-in-`handle_stream`). Connection
concurrency is a runtime-kernel concern that every triad daemon needs, so
duplicating it per component is wrong.

## Where it went, and why not into `MultiListenerDaemon` itself

The shared daemon is `triad-runtime`'s `MultiListenerDaemon`; its accept loop
calls `MultiListenerRuntime::handle_stream(&mut self, …)` serially. The
tempting move is to push concurrency INTO the daemon — have the accept loop
offload `handle_stream` onto a worker pool. That requires `handle_stream(&self)`
+ a `Send + Sync` runtime. Surveying the THREE consumers settles it:

- **cloud** (`schema_daemon.rs`) and **lojix** already hold a shared
  `Arc<Store>` and build a per-request engine (`with_store`), so their
  `handle_stream` doesn't mutate `self` — they are `&self`-ready and want
  thread-per-connection concurrency.
- **message** (`message/src/daemon.rs`) is a tokio/actor daemon: it genuinely
  uses `&mut self` (lazy phase init, `phase_mut`) and ALREADY has its own
  concurrency model (the Kameo actor runtime). Forcing `handle_stream(&self)`
  would break it, and thread-per-connection is the wrong model for it.

So concurrency cannot be a forced property of the daemon trait. The right
shared component is the concurrency **primitive**, which the thread-per-
connection daemons opt into, while an actor daemon keeps its own model.

## The component — `triad_runtime::BoundedWorkers`

`triad-runtime/src/workers.rs` (commit `fdfd1831`): a bounded thread-per-task
dispatcher — `dispatch(task)` acquires one of `capacity` permits (Mutex+Condvar,
backpressure when full), runs the task on its own thread, releases on
completion. Unit-tested for run-every-task and never-exceeds-capacity. Exported
as `triad_runtime::BoundedWorkers`.

Relation to `MultiListenerDaemon`: it is the primitive a `MultiListenerRuntime`
offloads each `handle_stream` onto so the daemon's accept loop stays free to
poll all sockets while a long request runs. The daemon stays
concurrency-model-agnostic; the runtime chooses (BoundedWorkers, an actor
runtime, or serial).

## Adoption

- **lojix** now consumes `BoundedWorkers` (commit `f78a20f7`): `handle_stream`
  does `self.workers.dispatch(move || worker.serve(listener, stream))`; its
  local `ConnectionPermits` is deleted. Concurrency proof still holds (~4 ms
  query during a running deploy); 8 fast + 6 ignored tests green.
- **cloud** is already shaped identically (per-request engine over
  `Arc<SchemaStore>`) and can adopt `BoundedWorkers` the same one-line way —
  its `schema_daemon.rs` currently has NO connection concurrency, so adopting
  would give it the same benefit. Offered as a follow-up (a triad-runtime pin
  bump on cloud); not done here to avoid touching a second component's deps
  unprompted.
- **message** keeps its actor concurrency; it does not use `BoundedWorkers`.
