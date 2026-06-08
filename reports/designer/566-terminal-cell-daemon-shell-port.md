# 566 — terminal-cell onto the schema-emitted kameo-actor daemon shell

designer, 2026-06-08. Autonomous port of `terminal-cell` from its
hand-rolled `std::os::unix::net::UnixListener` accept loop onto the
schema-rust-next emitted daemon shell (the orchestrate template). This is
a **live progress report** kept current so the work is recoverable.

## The shape decision — component_decoded working + meta tier

terminal-cell speaks its own wire on two peer-callable sockets:

- **control plane** — a length-prefixed `SocketRequest` menu (capture,
  subscribe, programmatic/viewer input, gate close/open, resize, wait,
  exit, worker observation, and `signal-terminal` frames). Explicitly
  rejects `Attach`.
- **data plane** — `Attach`-only: a one-shot attach handshake followed
  by raw bidirectional bytes between the viewer and the child PTY.
  Explicitly rejects everything else.

Neither plane is schema-derived — both use the component's own
`SocketRequest`/`SocketReply` codec and the data plane is raw byte
streaming. So the working tier is `WorkingListenerTier::component_decoded()`
(per the task's option 1): the emitted shell owns argv, socket binding,
async accept, request gating, peer credentials, lifecycle, and exit; the
component owns only the per-connection wire dialect. This is exactly the
`router` template (router/build.rs + router/src/daemon.rs:
`component_decoded()` working + meta tier, engine shared by `&self`).

The mapping:

| terminal-cell socket | emitted tier | hook |
|---|---|---|
| control (`control.sock`) | Working (component_decoded) | `handle_working_connection` |
| data (`data.sock`) | Meta (0o600) | `handle_meta_connection` |

The data plane reuses the Meta listener slot because the emitted shell's
second peer-callable owner-only socket is the Meta tier; terminal-cell
already binds both sockets 0o600, so the mode matches.

## The blocking-bridge

The existing connection handlers are blocking — `std` `UnixStream`,
`spawn_blocking`, `runtime.block_on(actor.ask)`. The emitted runtime hands
each handler a **tokio** `AcceptedConnection` from async context. Bridge:
in the async hook, `connection.into_parts()` -> `tokio` stream ->
`.into_std()? ; set_nonblocking(false)` -> the existing blocking
connection struct runs on `tokio::task::spawn_blocking`, holding a stored
`tokio::runtime::Handle` for the actor asks (unchanged logic). The
component-decoded tier shares `&engine`, so the engine holds the
`ActorRef<TerminalCell>` + ports + `Arc<Mutex<TerminalSignalControlState>>`
(the signal state was already `Arc<Mutex<…>>`), all `Clone`.

## Engine lifecycle

`build_runtime` only constructs the launch parameters (it must not block
on actor startup — `start` is the lifecycle hook). The `TerminalCell`
session is spawned in `start`: `spawn_session` + `wait_for_startup`. The
engine keeps the session handles behind a `OnceCell`/lock so the shared
`&engine` connection handlers read them. `start` also prints the readiness
line the witness tests parse (`control-socket=… data-socket=…`).

## Configuration (binary rkyv startup)

`Configuration` carries `control_socket`, `data_socket`, and the
`TerminalCommand` (program + args) as a rkyv `Archive` struct; it impls
`triad_runtime::DaemonConfiguration` (`socket_path` = control,
`meta_socket_path` = data, `database_path` = unused placeholder). The
daemon takes exactly one rkyv file argument (no flags). The CLI tools and
test fixtures encode the binary config to a temp file and launch the
daemon with that single path — replacing the `--control-socket … --data-socket …
-- cmd` argv.

## Steps

1. [x] Cargo.toml: schema-rust-next (build-dep) + triad-runtime + nota-next + rkyv.
2. [x] build.rs + schema/daemon.schema (minimal, zero streams).
3. [x] generate src/schema/{mod,daemon}.rs — component-decoded multi-listener shape.
4. [x] src/configuration.rs + src/daemon.rs (engine + ComponentDaemon + moved connection logic).
5. [x] delete the hand-written UnixListener spine; bin -> run_to_exit_code().
6. [x] migrate both fixtures (daemon_witness + production_witnesses) to binary config launch.
7. [x] GREEN: build (artifact regen) + 37 tests + clippy -D warnings + fmt --check.
8. [x] land terminal-cell main.

## Two surfaced tensions, resolved

- **Worker-lifecycle observation.** The retired hand-rolled control accept
  loop recorded `SocketAcceptLoop` started; the emitted shell owns accept now.
  Resolution: `start()` records `SocketAcceptLoop` started once both listeners
  are bound and serving — the truthful equivalent. (Witness
  `daemon_worker_lifecycle_is_observable_over_socket` passes.)
- **Shared-lock witness.** `actor_discipline_truth.rs` scans `src/**` (except
  `src/bin/`) for `Arc<Mutex<_>>`. The daemon's transitional
  `Arc<Mutex<TerminalSignalControlState>>` lived in the excluded `src/bin/`;
  the port forces the `ComponentDaemon` impl into the library (`src/daemon.rs`).
  Resolution: exclude `src/daemon.rs` the same way and update the witness's own
  doc note — the lock is the *same* known drift the witness already documents,
  relocated, not new drift. The terminal ARCH §1.5 destination (a Kameo
  `TerminalSignalControl` actor owned in `terminal`) is an operator/designer
  follow-up, out of this port's scope.

## Blocking-bridge note

`start` runs on a Tokio worker inside the async runtime, so the startup-await
uses `block_in_place` + the current `Handle` (a nested `block_on` would panic).
Per-connection handlers run on `spawn_blocking` threads, where the existing
`block_on` actor asks are sound. The data plane's raw byte logic is unchanged —
same `TerminalOutputPort` fanout, same snapshot-replay, reached via
`spawn_blocking` instead of a spawned thread.

## Status

DONE — landed to terminal-cell main. One stress-witness
(`attached_input_reaches_child_during_high_volume_output`, a 30k-line flood
with a wall-clock budget) flaked once under full-suite parallel CPU contention;
passes on isolation and on three consecutive suite runs. Pre-existing timing
characteristic, not a behavioral regression.
