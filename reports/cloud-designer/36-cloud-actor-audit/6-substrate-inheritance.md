# 6 — substrate inheritance: does cloud CHOOSE or INHERIT its sync/no-actor shape?

Workflow dimension `explore:substrate-inheritance`, verified by adversarial
thesis-4 (verdict **partial** — the inheritance claim is true for the SPINE only,
overreaches by packaging the actor-TREE absence as "inherited" and by attributing
the production runtime to the substrate). This is the dimension that tells us
**what can be fixed in cloud alone vs. what needs a workspace-wide change.**

## Headline (corrected)

Split the "sync/zero-kameo property" into two separable layers:

1. **The daemon SPINE** (accept loop + decode→execute→encode framing) is
   **INHERITED and structurally forced** by `triad-runtime` + the `schema-rust-next`
   emitter — both hard-synchronous, zero kameo/tokio, no branch that could emit an
   async/actor accept loop. cloud **cannot** make the spine itself actor-native
   (async accept, per-listener actor mailboxes) without a workspace-wide substrate
   change.
2. **The ACTOR TREE behind the spine** is **cloud's own CHOICE**, not forced. The
   emitted `ComponentDaemon` trait holds the engine as a component-defined
   `type Engine` accessed by `&Engine`, so cloud could make `Engine` a tree of kameo
   `ActorRef`s and bridge sync→actor inside `build_runtime`/`handle_working_input`
   **with no change to triad-runtime or the emitter**. cloud merely chose
   `type Engine = Arc<SchemaStore>` instead.

Plus a correction thesis-4 surfaced: the inheritance reasoning applies **only to the
schema-engine path**, which is NOT yet live. The runtime `cloud-daemon` actually
runs in PRODUCTION is the **hand-written** legacy `crate::daemon::Daemon`, which is
**not built on the triad substrate at all** — its sync/blocking shape is the
author's independent choice that predates and bypasses the substrate.

## Layer 1 — the SPINE is inherited and forced

`triad-runtime` (pinned `cdda1b1`) is hard-synchronous with zero room for an actor
runtime at the spine level:
- `Cargo.toml` deps: `rustix` (std net), `signal-frame`, `thiserror` only — **no
  kameo, no tokio, no futures**. `grep -rniE 'kameo|tokio|async fn|\.await'` across
  `src/` returns **none**.
- `src/daemon.rs` is `std::os::unix::net::{UnixListener,UnixStream}` throughout. The
  single-listener loop is a blocking `for stream in self.listener.incoming()`
  (`daemon.rs:421`) calling `handle_stream(stream)` **inline** (`daemon.rs:424`).
  The multi-listener loop is a non-blocking poll (`set_nonblocking(true)`
  `:308`; `WouldBlock`→`thread::sleep` `:387,451`) likewise calling
  `handle_stream(...)` **inline** (`:372`).
- The runtime traits `DaemonRuntime` (`:14-24`) and `MultiListenerRuntime` (`:26-45`)
  are **synchronous** `fn handle_stream(&mut self, …) -> Result<…>` — no async, no
  `Future`.

The emitter (`schema-rust-next`, pinned `2c3c162`) structurally emits a sync spine
and **cannot** emit an actor one:
- `Cargo.toml` deps: `prettyplease/proc-macro2/quote/syn/schema-next/thiserror` — no
  async tooling. `grep` for `kameo|tokio|async fn|spawn` across `src/` = **none**.
- `daemon_emit.rs` emits a `GeneratedDaemonRuntime` whose `impl MultiListenerRuntime`
  (`:821-846`) / `impl DaemonRuntime` (`:849-866`) is a sync `handle_stream` calling
  a sync `handle_working_stream` doing **blocking** `read_frame → decode →
  handle_working_input → encode → write_frame` (`:894-905`). Its only conditional
  branch (`:869`) is multi-vs-single listener — both synchronous. There is **no
  branch** that could produce an async/actor accept loop. Confirmed in cloud's
  emitted `src/schema/daemon.rs:198-219` + `:173-182`.

**Conclusion:** making the SPINE actor-native (async accept, per-listener kameo
mailboxes, as `component-triad.md:348` "each surface gets its own typed listener
actor" envisions) requires changing triad-runtime + the emitter — a **workspace-wide**
change. cloud cannot do it alone.

## Layer 2 — the ACTOR TREE behind the spine is cloud's CHOICE

The emitted `ComponentDaemon` trait does NOT force the engine to be a plain sync
struct:
- `type Engine;` is component-chosen (`src/schema/daemon.rs:24`; emitter
  `daemon_emit.rs:422`).
- `fn build_runtime(configuration: &Self::Configuration) -> Result<Self::Engine, …>`
  — cloud constructs the engine however it wants (`daemon_emit.rs:432`).
- `fn handle_working_input(engine: &Self::Engine, input, connection) -> …` — engine
  taken by **`&Engine`** (`daemon_emit.rs:453`; called as
  `Daemon::handle_working_input(&self.engine, …)` at `:901`).

Because `Engine` is **opaque** to the spine and passed by `&`, cloud could make
`type Engine = CloudActorHandles` holding `ActorRef<CloudflareProvider>` /
`ActorRef<PlanStore>` / etc., spawn them in `build_runtime`, and inside
`handle_working_input` do a blocking `actor_ref.ask(msg).blocking_send()` (kameo's
sync bridge). The provider actors then run their own concurrency model **behind** the
listener. This is exactly the case triad-runtime's own `workers.rs:13` doc
anticipates: *"Daemons with their own concurrency model (e.g. an actor runtime)
simply do not use it [BoundedWorkers]."* The substrate **deliberately leaves a hole**
for an actor runtime behind the spine. **An actor tree IS compatible with the
emitted sync daemon spine.**

## What cloud actually built (neither path's actors)

- **Production path** (legacy `src/daemon.rs`): two `thread::spawn` listener threads
  (`:35,38`) over one global `Arc<Mutex<Store>>` (`:24`); each listener serves
  serially via blocking `for stream in listener.incoming()` (`:97,110`). No
  per-connection pool, no actors. **Not built on triad-runtime at all** — it is
  hand-written std, predating/bypassing the substrate.
- **Schema-engine path**: `type Engine = Arc<SchemaStore>` (`schema_daemon.rs:56`) —
  a plain shared store, NOT actor handles; `run_effect` returns empty listings
  (`schema_runtime.rs:458-466`). Built/socket-tested but not in the production bin.
- **`BoundedWorkers`** (triad-runtime's bounded thread-per-connection primitive,
  intent `k6w1`) is wired **NOWHERE** — not in triad-runtime's serve loops, not in
  the emitter, not in cloud. So even the emitted spine serves serially on the accept
  thread; cloud has neither the bounded-thread concurrency model NOR an actor one.

## Concurrency-model matrix

| Path | Status | Concurrency model | Actors? | Engine type |
|---|---|---|---|---|
| `src/daemon.rs` (legacy) | **production** | 2 listener threads, serial-per-listener, 1 global `Arc<Mutex<Store>>` | none | hand-written `Store` |
| emitted schema path | built/socket-tested, NOT in bin, empty IO | sync spine, serial on accept thread (no BoundedWorkers) | none | `Arc<SchemaStore>` |
| **what the emitter ALLOWS now** | available, no substrate change | sync spine bridging to a component actor tree | **yes (behind spine)** | `Engine` = kameo `ActorRef`s |
| actor-native spine | NOT available to cloud alone | async accept / per-listener actor mailboxes | yes (at spine) | requires triad-runtime + emitter rework |

## What would have to change, and where

- **Provider actors BEHIND the listener** (satisfies `ARCHITECTURE.md:30-41`):
  **CLOUD ALONE.** Make `type Engine` a struct of kameo `ActorRef`s, spawn in
  `build_runtime`, `blocking`-ask inside `handle_working_input`/`handle_meta_stream`.
  Add `kameo` to `cloud/Cargo.toml` (currently absent). No triad-runtime or emitter
  change. **This is the actor-native-where-it-matters move available today.**
- **Actor-native SPINE** (per-listener actor mailboxes, async accept):
  **WORKSPACE-WIDE.** triad-runtime's `DaemonRuntime`/`MultiListenerRuntime` traits +
  serve loops and the emitter's `GeneratedDaemonRuntime` all need an async/actor
  rework. Shared substrate; cloud cannot do it alone.

## Linkage to report-35

This is the cloud-local instance of `reports/cloud-designer/35-actor-divergence-forensics/`:
- The sync SPINE substrate deferral is **recorded/blessed** intent (Spirit `1483`
  "Workspace explicitly defers … actor mailbox/backpressure/runtime-control"; `1487`
  "minimal lifecycle hooks … full actor mailbox stays deferred" —
  `component-triad.md:1057-1094`). cloud inheriting the sync spine is consistent with
  blessed intent.
- The **total absence of an actor tree** is the **unblessed-but-consistent
  realization** report-35 flagged against `actor-systems.md:65` ("Actors all the way
  down") and `:354` ("No shared locks … `Arc<Mutex<T>>`") — and here it is **cloud's
  own choice**, NOT a substrate constraint. The substrate left the door open
  (`workers.rs:13`; opaque `&Engine`); cloud declined to walk through it. Report-35's
  "concurrency SHAPE is recorded intent (`2alg`/`k6w1`/`tj99`)" maps onto the
  bounded-thread-per-connection model cloud ALSO did not adopt (BoundedWorkers
  unused).

## Open questions raised here

- Does kameo's sync→actor bridge compose cleanly inside the emitted sync
  `handle_working_input` **without** dragging tokio into cloud's otherwise-std build,
  or would provider actors behind the spine still pull in an async runtime cloud
  currently avoids? (This is the one real engineering cost of the cloud-alone move.)
- Is the intended end state (a) provider actors behind a permanently-sync triad
  spine, or (b) a future workspace-wide rework making the spine itself actor-native?
  The records (`1483`/`1487` deferral) don't say which.
- Should the legacy `src/daemon.rs` be retired AT cutover, or does cloud carry both
  runtimes indefinitely — and which is the target for any actor-tree work?
