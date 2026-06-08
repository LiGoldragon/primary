# 564 — emitter actor-shell change (working / in-progress)

designer, 2026-06-08. Autonomous implementation of the psyche directive:
*"the emitter must generate real Kameo actors — implement it and test on
orchestrate."* Foundation change to `schema-rust-next` so the schema-emitted
daemon owns its engine in a kameo actor (record `zk6y`/`96mi`/`ilxh`), not a
synchronous engine shared as `&engine` forcing a component-internal `Mutex`.
This is a **live progress report** — kept current so the work is recoverable if
the session drops.

## The diagnosis (confirmed across three surfaces)

`schema-rust-next/src/daemon_emit.rs` emits `GeneratedDaemonRuntime<Daemon>` that
holds `engine: Daemon::Engine` by value and calls
`Daemon::handle_working_input(&self.engine, input, ctx)`. The runtime is held as
`Arc<Runtime>`, cloned per connection, each connection `tokio::spawn`ed, and
`AsyncConnectionRuntime::handle_connection(&self, …)` is **shared `&self`**. So N
connection tasks share one engine via `&` — any mutable engine state needs
interior mutability. `Runner::drive(&mut engines, …)` needs `&mut` across
`.await`. That is exactly why components wrap their engine in a `Mutex`
(spirit `Mutex<Nexus>`, orchestrate `Mutex<()>`/`Mutex<u64>`/`Mutex<HandoverState>`
in `OrchestrateService`). `Runner::drive` is **not** in `daemon_emit.rs` — it
runs inside the component engine via the emitted `NexusEngine::execute` default.

## The fix — emitter-generated `EngineActor` (minimal, per zk6y)

triad-runtime already provides everything: `RequestGate` is the model
(`Args = Self`, `on_start → Ok(self)`, kameo 0.20). The emitter generates a
per-daemon `EngineActor<Daemon>` owning `Daemon::Engine`; the runtime holds
`ActorRef<EngineActor<Daemon>>` and drives requests through the mailbox — which
**serializes exactly as the lock did, without holding a guard across `.await`**,
and gives the engine its `&mut self` for free.

Emitter changes (`daemon_emit.rs`):
- New `EngineActor<Daemon> { engine: Daemon::Engine }` with
  `impl triad_runtime::kameo::Actor` (`on_start` runs `Daemon::start`, `on_stop`
  runs `Daemon::stop`) and `impl Message<WorkingInput> { Reply = Result<Output,
  Daemon::Error>; handle → Daemon::handle_working_input(&mut self.engine, input,
  &ctx) }`. The component does **not** implement `Actor` — the wrapper is emitted.
- `GeneratedDaemonRuntime` holds `engine: ActorRef<EngineActor<Daemon>>`; `new`
  spawns it; `handle_working_connection` does `self.engine.ask(WorkingInput{ input,
  context }).await`; runtime `start` = `wait_for_startup`, `stop` = stop the actor.
- `ComponentDaemon::handle_working_input`: `&Self::Engine` → `&mut Self::Engine`.
- For stream daemons the actor also returns the published event
  (`WorkingOutcome { output, event: Option<StreamEvent> }`); the subscription
  *registry* (writer halves from connections) stays runtime-side plumbing for now
  (separate concern from engine state). Non-stream path (orchestrate) is the
  primary target this pass.

triad-runtime change: `pub use kameo;` so the generated daemon references
`triad_runtime::kameo::*` and components need no direct kameo dep.

## orchestrate migration (the test consumer)

- `OrchestrateService` becomes `Daemon::Engine`, owned by the generated
  `EngineActor`. Drop the three `Mutex`es — `sequence: Mutex<()>` deleted (mailbox
  serializes), `next_observation_token`/`handover` become plain `&mut` fields.
- `handle_working_input(&mut service, input, _ctx)` constructs the per-request
  `OrchestrateNexusEngine` over the owned state and runs
  `NexusEngine::execute(...).await` natively — drop the `futures::executor::block_on`
  in `execution.rs:431,503`.
- Wire `main.rs` to the schema shell (`<OrchestrateDaemon as DaemonEntry>::run_to_exit_code`),
  `impl ComponentDaemon`, `Configuration: triad_runtime::DaemonConfiguration`.
- Delete `src/daemon.rs` old `BoundedWorkers`/`MultiListenerDaemon` spine; remove
  the `OperationLowering` ZST (`src/lowering.rs`) + its `tests/ledger.rs` callers.
- Tests pinning the old shape to update: `tests/architecture.rs:76,249`
  (`BoundedWorkers`, `include_str!("../src/daemon.rs")`), `tests/ledger.rs`
  (`OperationLowering`), `tests/daemon_cli.rs` (NOTA→binary config).

### Two known complications

1. **Binary config**: the generated `DaemonCommand` rejects NOTA, requires a
   binary rkyv signal file (correct per the daemon-binary-only override). Today
   orchestrate launches with a `.nota` file. `load_configuration` decodes rkyv;
   `daemon_cli` migrates to encode binary.
2. **Upgrade tier**: orchestrate serves 3 sockets (ordinary/meta/**upgrade**); the
   generated shell has only Working+Meta. The upgrade tier (`handle_upgrade_request`
   + socket-retirement-on-handover) has no slot. Resolution options: fold upgrade
   into `handle_meta_connection`, or defer the upgrade tier. This gates the full
   `main.rs` cutover; the engine→actor proof does not depend on it.

## Test loop

Patch orchestrate to local schema-rust-next + triad-runtime, then
`ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS=1 cargo build` (regenerate), `cargo test`,
`cargo clippy`. Work on feature branches in the live `/git` checkouts.

## Status

- [x] Understood all three surfaces (workflow `ww7tzt06l`).
- [ ] triad-runtime `pub use kameo;`
- [ ] emitter `EngineActor` in `daemon_emit.rs`
- [ ] orchestrate engine→actor + main wiring
- [ ] build + test green
