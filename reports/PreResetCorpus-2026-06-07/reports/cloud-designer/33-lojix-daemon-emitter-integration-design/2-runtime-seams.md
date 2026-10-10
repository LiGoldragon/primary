# 2 — triad-runtime daemon + concurrency seams

Ground-read of the runtime kernel the emitter consumes, to decide WHERE each of
the four lojix properties slots in: generic (belongs in `triad-runtime`) vs
component-specific (belongs in emitted code or hand-written). All paths are
`/git/github.com/LiGoldragon/triad-runtime/src/`. HEAD `f9c38e2`.

## The serial call site — the exact spot concurrency must address

The whole serialization is one line. `BoundMultiListenerDaemon::serve_streams`
(`daemon.rs:392`) loops `serve_next_stream` (`daemon.rs:382`), which loops
`try_serve_next_stream` (`daemon.rs:368`):

```rust
pub fn try_serve_next_stream(&mut self) -> Result<bool, ListenerError> {
    for index in 0..self.listeners.len() {
        let listener = self.listeners[index].listener().clone();
        if let Some(stream) = self.listeners[index].accept_next_stream()? {
            if let Err(error) = self.runtime.handle_stream(listener.clone(), stream) {
                self.request_error_log.report_for_listener(&listener, &error);
            }
            return Ok(true);
        }
    }
    Ok(false)
}
```

`handle_stream` is called INLINE on the accept thread (`daemon.rs:372`). The
listeners are non-blocking (`set_nonblocking(true)`, `daemon.rs:308`), so the
accept loop polls round-robin across listeners with a `thread::sleep` of the
poll interval (default 10 ms, `daemon.rs:173-177,387`) when none is ready. The
ENTIRE blocking cost of a request — `handle_stream`'s decode -> execute ->
encode — runs before the loop can `accept` again on EITHER socket. This is the
"serial" property the survey flagged: a multi-minute `nix` build inside
`handle_stream` freezes the accept loop on both the ordinary and owner sockets.

The single-listener path has the same shape with worse blocking semantics:
`BoundSingleListenerDaemon::serve_streams` (`daemon.rs:420`) iterates
`self.listener.incoming()` (a BLOCKING accept) and calls `handle_stream` inline
(`daemon.rs:424`). No non-blocking poll there at all.

So the concurrency seam, wherever it lands, is about making the work `handle_stream`
triggers NOT block the return of `handle_stream` itself.

## The two runtime traits — exact signatures and the `&mut self` problem

`daemon.rs:14-45`. Both daemon-shell traits take `&mut self` on `handle_stream`:

```rust
pub trait DaemonRuntime {
    type StartError;
    type StopError;
    type RequestError: Display;
    fn start(&mut self) -> Result<(), Self::StartError>;
    fn stop(&mut self) -> Result<(), Self::StopError>;
    fn handle_stream(&mut self, stream: UnixStream) -> Result<(), Self::RequestError>;
}

pub trait MultiListenerRuntime {
    type Listener: Clone + Display;
    type StartError;
    type StopError;
    type RequestError: Display;
    fn should_continue(&self) -> bool { true }   // default true
    fn start(&mut self) -> Result<(), Self::StartError>;
    fn stop(&mut self) -> Result<(), Self::StopError>;
    fn handle_stream(
        &mut self,
        listener: Self::Listener,
        stream: UnixStream,
    ) -> Result<(), Self::RequestError>;
}
```

### What `&mut self` on `handle_stream` implies for concurrency

The signature is `&mut self`, but the daemon shell calls it from ONE accept
thread (`try_serve_next_stream` holds `&mut self.runtime`). So `&mut self` is NOT
the concurrency obstacle people assume — there is only ever one caller. The
obstacle is what `handle_stream` is ALLOWED to KEEP after it returns.

`&mut self` means a concurrent offload model CANNOT hand a worker thread a
borrow of `self` (the engine, the registry) — the borrow ends when `handle_stream`
returns, but the spawned thread outlives the call. This is exactly why lojix's
`LojixRuntime::handle_stream` (`lojix/triad-port/src/daemon.rs:151-166`) hands
the worker an `Arc<Store>` CLONE and a `Copy` codec, not `&self`:

```rust
fn handle_stream(&mut self, listener: Self::Listener, stream: UnixStream) -> Result<()> {
    let worker = RequestWorker { store: self.store.clone(), codec: self.codec };
    self.workers.dispatch(move || worker.serve(listener, stream));
    Ok(())   // returns immediately; the loop accepts again
}
```

The worker owns everything it touches (`'static`), so the `&mut self` borrow can
end immediately. `handle_stream` returns `Ok(())` after the (possibly
back-pressured) `dispatch`, and the accept loop is free again. This is the model
the emitter must reproduce: shared state is `Arc`-cloned INTO the worker; the
per-request engine is BUILT inside the worker from the shared store.

### The `&mut self` vs the message/actor consumer

Crucial cross-consumer constraint. The `message` daemon (Kameo actor) needs
`&mut self` on `handle_stream` AND brings its own actor concurrency. If the
concurrency offload were forced into the daemon shell (option A below), the shell
would either need `&self` (breaking `message`, which mutates) OR would
double-concurrency `message` (offloading onto `BoundedWorkers` what the actor
already concurrency-handles). Keeping `&mut self` and leaving the offload DECISION
to the runtime is what lets `message` opt OUT of `BoundedWorkers` (workers.rs:11-13
already names this: "Daemons with their own concurrency model (e.g. an actor
runtime) simply do not use it"). This is the decisive argument for option B.

## BoundedWorkers — the concurrency primitive (exact surface)

`workers.rs`. The reusable concurrency primitive, already designed for exactly
this (header lines 7-13 describe the `MultiListenerRuntime`-offload pattern):

```rust
#[derive(Clone)]
pub struct BoundedWorkers { /* Arc<WorkerPermits> */ }

impl BoundedWorkers {
    pub fn new(capacity: usize) -> Self;        // capacity.max(1)
    pub fn capacity(&self) -> usize;
    pub fn dispatch<F>(&self, task: F) where F: FnOnce() + Send + 'static;
}
```

`dispatch` ACQUIRES a permit (blocking with backpressure when at `capacity`,
`workers.rs:45`), THEN `thread::spawn`s the task holding the permit, releasing on
drop (`workers.rs:41-50,93-103`). The backpressure point is `dispatch` itself: at
the cap, `dispatch` blocks the accept thread until a worker frees a permit — this
is INTENTIONAL flood-control (the accept loop slows rather than spawning
unbounded threads). The task closure is `FnOnce() + Send + 'static` — it must own
everything (the `Arc<Store>` clone, the `Copy` codec, the `UnixStream`, the
listener tag). This is the bound the worker noun must satisfy.

`BoundedWorkers` is `Clone` (it's an `Arc` inside), so the runtime holds ONE pool
and the shell-level `&mut self` borrow does not impede cloning the pool handle
into workers.

VERDICT on BoundedWorkers placement: **already correctly placed in
triad-runtime**. It is GENERIC. Nothing to move. The emitter's job is to USE it
from the generated runtime, gated by a schema flag (see option B).

## ConnectionContext — peer creds (exact surface) and the per-connection hook

`process.rs:30-78`.

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ConnectionContext { user_id: u32, group_id: u32, process_id: i32 }

impl ConnectionContext {
    pub const fn new(user_id: u32, group_id: u32, process_id: i32) -> Self;
    pub fn from_stream(stream: &UnixStream) -> std::io::Result<Self>;  // SO_PEERCRED via rustix
    pub fn user_id(&self) -> u32;
    pub fn group_id(&self) -> u32;
    pub fn process_id(&self) -> i32;
}
```

### How `from_stream` gets called per accepted connection — the answer

There is NO hook in `serve_streams` / `try_serve_next_stream` that calls
`from_stream`. The daemon shell passes a BARE `UnixStream` to `handle_stream`
(`daemon.rs:40-44`); `ConnectionContext` is NOT mentioned in `daemon.rs` at all
(confirmed: only `lib.rs`, `process.rs`, `tests/process.rs` reference it). So the
runtime — i.e. the EMITTED `GeneratedDaemonRuntime::handle_working_stream` — must
call `from_stream(&stream)` itself. It already does, on the WORKING socket only:

```rust
// daemon_emit.rs:842-843
fn handle_working_stream(&self, stream: UnixStream) -> Result<(), Daemon::Error> {
    let connection = ConnectionContext::from_stream(&stream).map_err(FrameError::Io)?;
```

The GAP for fail-closed owner auth (intent `9v7h`): the META socket is routed to
`Daemon::handle_meta_stream(&self.engine, stream)` (`daemon_emit.rs:790`) — a raw
`UnixStream`, NO `from_stream` call, NO `ConnectionContext`. So the owner tier
gets ZERO peer-credential check from the emitter today; authority rests purely on
socket file mode (lojix's `validate_owner_socket_mode`). To honor `9v7h`, the
emitted meta path must call `from_stream` and reject on uid mismatch before
dispatching to the engine.

### Should `from_stream` move into the shell?

NO. Calling `from_stream` per-connection in `serve_streams` and passing a
`ConnectionContext` into `handle_stream` would be the "generic" move, but it has
two costs: (1) it changes BOTH runtime trait signatures
(`handle_stream(&mut self, listener, stream, connection)`), a breaking change to
every consumer including `message`; (2) some daemons (a future trusted-internal
listener) may not want the `SO_PEERCRED` syscall on every accept. Keeping
`from_stream` in the emitted runtime (where it already is for the working tier)
is the lighter, non-breaking placement; the design just needs to ALSO emit it on
the meta path. So: `from_stream` itself is GENERIC (stays in `process.rs`);
CALLING it per connection is RUNTIME-LEVEL (emitted), not shell-level.

The uid-COMPARISON policy (which uid is "owner", reject vs tag) is
COMPONENT-SPECIFIC — it belongs in a component hook or the schema declaration
(the owner uid is config/runtime data), NOT hardcoded in the emitter or shell.

## DaemonConfiguration trait — the bind-input surface (exact surface)

`process.rs:89-116`. The accessors the emitted `bind` reads:

```rust
pub trait DaemonConfiguration {
    fn socket_path(&self) -> &Path;                          // required
    fn meta_socket_path(&self) -> Option<&Path> { None }
    fn database_path(&self) -> &Path;                         // required
    fn trace_socket_path(&self) -> Option<&Path> { None }
    fn meta_socket_mode(&self) -> Option<SocketMode> { None }
}
```

This is GENERIC and already the right shape for socket layout. For fail-closed
owner auth the natural extension is one accessor here — `fn owner_user_id(&self)
-> Option<u32> { None }` — so the owner uid is component CONFIG (runtime data),
read by the emitted meta path, with the comparison/reject logic emitted generically
against it. That keeps the POLICY (reject on mismatch) generic-and-emitted and
the DATUM (which uid) component-config, satisfying the discipline that the owner
uid is not a compile-time emitter constant. (Note: lojix's hand-written struct
`DaemonConfiguration` is a name collision with this trait — see survey report
32/1; carries forward.)

## ExitReport, frame codec, ListenerSocket — surfaces the seam touches

- `ExitReport` (`process.rs:125-153`): `new(&'static str)` + `from_result(Result<(),E>)
  -> ExitCode`. Generic, untouched by the four properties.
- `LengthPrefixedCodec` (`frame.rs:79-122`): `new(MaximumFrameLength)`,
  `default()` = `MaximumFrameLength::maximum_for_u32_prefix()` (u32::MAX = 4 GiB),
  `read_body(&mut impl Read) -> Result<FrameBody, FrameError>`, `write_body`. The
  emitted `WorkingTransport` (`daemon_emit.rs:574-583`) uses `LengthPrefixedCodec::default()`
  — i.e. the 4 GiB cap, NOT lojix's 8 MiB (audit R1). The cap is a `MaximumFrameLength`
  CONSTRUCTOR argument; the codec is generic. Property 3 = thread a bounded
  `MaximumFrameLength` into the emitted transport instead of `default()`.
- `MaximumFrameLength` (`frame.rs:31-47`): `new(usize)`, `maximum_for_u32_prefix()`,
  `bytes()`, `accepts(usize)`. Generic.
- There is NO read-timeout surface anywhere in triad-runtime. The read timeout is
  a `UnixStream::set_read_timeout` call (lojix does it in `serve_ordinary`/`serve_owner`,
  `lojix/.../daemon.rs:190,202`). It is a per-stream operation the emitted
  transport must perform; the bound (10 s) is a value the schema/config supplies.
- `ListenerSocket` (`daemon.rs:90-218`): `new(listener, path)`, `with_socket_mode(SocketMode)`.
  `SocketMode::new(u32)`. Generic; the emitter already uses these in `bind`.

## Where each property slots in — option A (shell) vs option B (emitted runtime)

### Option A — concurrency in `MultiListenerDaemon` (shell)

Make the shell offload `handle_stream` onto a `BoundedWorkers` it owns, so EVERY
runtime gets concurrency for free. REJECTED:
- Forces `handle_stream` to be callable from a worker thread → needs `&self` (or
  `Arc<Self>` + `Sync`), breaking the `&mut self` contract that `message`'s actor
  and lojix's `start`/`stop` rely on.
- Forces the per-request engine-build decision into the shell, but the shell does
  not know the component's Store/Engine (that is exactly what `ComponentDaemon::build_runtime`
  exists to hide).
- Double-concurrencies actor daemons (`message`) that already have their own model.
- `serve_streams`'s `should_continue()` / poll-interval lifecycle would need to
  coordinate with in-flight workers (graceful drain on stop), pushing actor-style
  lifecycle into the generic shell.

### Option B — concurrency in the generated runtime (emitted) — RECOMMENDED

Keep the shell exactly as is (`&mut self`, serial-call). Move the offload INTO
the emitted `GeneratedDaemonRuntime::handle_stream`, gated by a schema flag
(`concurrent`/per-request-engine). This is lojix's proven structure, lifted into
the emitter:

- `GeneratedDaemonRuntime` holds `Arc<Daemon::SharedState>` (or `Arc<Store>` via a
  new `ComponentDaemon` accessor), a `BoundedWorkers`, and the bounded
  `LengthPrefixedCodec` — NOT a long-lived `engine: Daemon::Engine`. (Today it
  owns `engine` directly, `daemon_emit.rs:830`; the concurrent variant instead
  owns the shared store and BUILDS a fresh engine per worker.)
- `handle_stream(&mut self, listener, stream)` clones the `Arc`, the `Copy`
  codec, and the workers handle into an owned worker noun, `dispatch`es it, and
  returns `Ok(())` immediately. The `&mut self` borrow ends at return; the worker
  is `'static`.
- The worker noun's `serve` does: `set_read_timeout(R2)`; `read_body` with the R1
  cap; for META — `ConnectionContext::from_stream` + uid compare + reject-on-mismatch
  (9v7h) BEFORE decode; decode the tier's typed `Input` into the ONE
  `nexus::SignalInput` root; build a fresh per-request engine over the `Arc`;
  `execute`; encode the reply on the SAME tier.

This is the ONLY option that simultaneously: (1) keeps `&mut self` so `message`
is untouched, (2) lets `message` opt out (it just doesn't set the concurrent
flag), (3) keeps the engine-build behind `build_runtime`/a new shared-state hook,
(4) reuses `BoundedWorkers` as-is, (5) localizes the change to the emitter + a
schema flag, with ZERO triad-runtime daemon-shell change.

## Generic vs component-specific — the placement table

| Concern | Placement | Why |
|---|---|---|
| `BoundedWorkers` primitive | GENERIC, already in `triad-runtime/workers.rs` | reusable, unchanged |
| `ConnectionContext::from_stream` | GENERIC, already in `process.rs` | reusable, unchanged |
| `LengthPrefixedCodec` + `MaximumFrameLength` | GENERIC, already in `frame.rs` | the cap is a constructor arg |
| `DaemonConfiguration` accessors | GENERIC trait in `process.rs`; ADD `owner_user_id()` | owner uid is config data |
| The serial accept shell | GENERIC, unchanged (`daemon.rs`) | concurrency is NOT moved here |
| Per-request offload onto `BoundedWorkers` | EMITTED (generated runtime), gated by schema flag | lets each component opt in/out |
| Per-request fresh engine over shared `Arc<Store>` | EMITTED, fed by a new `ComponentDaemon` shared-state/build hook | shell can't know the Store |
| `set_read_timeout` per stream | EMITTED (worker `serve`); bound from schema/config | per-stream op, bound is data |
| Frame cap value (8 MiB) | SCHEMA-DECLARED → EMITTED into the transport | component policy datum |
| uid-compare + reject-on-mismatch logic | EMITTED generically against `owner_user_id()` | policy is uniform; datum is config |
| Which uid counts as owner | COMPONENT CONFIG via `DaemonConfiguration::owner_user_id` | runtime data, not emit-time |
| Two typed contracts → one `SignalInput` root | EMITTED — meta tier becomes a TYPED decode->execute path, replacing `handle_meta_stream` | the Nexus root is schema-derived |

## The one triad-runtime change the design needs

The seams analysis says concurrency, peer-creds, codec, and bounds are ALL
already generic in triad-runtime — the change is overwhelmingly in the EMITTER
(option B) plus the SCHEMA declaration. The single triad-runtime addition worth
considering is one default accessor on the `DaemonConfiguration` trait:

```rust
/// The owner user id authorised on the meta tier. `None` leaves the meta
/// tier authorised by socket file mode only; `Some(uid)` makes the emitted
/// meta path reject any peer whose SO_PEERCRED uid differs (intent 9v7h).
fn owner_user_id(&self) -> Option<u32> { None }
```

Default `None` keeps every existing consumer source-compatible. This is the
generic datum-accessor; the reject POLICY is emitted against it. Everything else
needed for the four properties is already present in `triad-runtime` at HEAD.

## Open seam questions for the design draft (file 4)

1. The concurrent runtime owns `Arc<SharedState>` not `engine: Daemon::Engine`.
   That needs a NEW `ComponentDaemon` shape: either `type SharedState; fn
   build_shared_state(...) -> Arc<SharedState>` + `fn build_engine(&SharedState)
   -> Engine`, OR keep `build_runtime` returning an `Arc`-shareable engine the
   worker re-derives a per-request view from. The runner survey (this report)
   establishes the CONSTRAINT (worker must be `'static`, engine built inside it);
   the exact hook shape is the draft's call.
2. With concurrency, `start`/`stop` lifecycle (`MultiListenerRuntime::start`/`stop`,
   called on `&mut self` by the shell at `daemon.rs:360-366`) runs BEFORE/AFTER
   the serve loop but workers may be in flight at `stop`. Does the design need a
   drain, or is "stop after the accept loop exits, workers finish on their own
   threads" acceptable (lojix's current behavior — `stop` is a no-op,
   `lojix/.../daemon.rs:147`)? The shell does NOT join workers; `BoundedWorkers`
   has no join surface. Likely fine for lojix's model; flag for cloud.
3. The read timeout: lojix sets it per-stream inside the worker AFTER offload, so
   the timeout clock starts when the worker runs, not at accept. Under
   backpressure (all permits held) a connection waits in the accept queue without
   a timeout. Acceptable for lojix (the OS listen backlog bounds it); note it as
   a known property, not a regression vs lojix (lojix has the identical shape).
