# 558.7 — harness — early (effort: large)

## harness — migration assessment

**Role:** process/session-control boundary — models interactive AI harnesses (Codex / Claude / Pi / Fixture) as addressable runtime objects with lifecycle state, typed transcript observations, and terminal + Pi-RPC delivery adapters. One `harness-daemon` process may own multiple in-process harness instances.

**Repos:** `harness` ✓, `signal-harness` ✓, `meta-signal-harness` **MISSING** (confirmed seed gap).

**Headline:** harness is one of the least-migrated components. The daemon is fully hand-written — no `build.rs`, no `src/schema/`, no `schema-rust-next`/`schema-next` dependency anywhere. It is *not* on the old `MultiListenerDaemon`/`BoundedWorkers` spine and it never adopted `signal-executor` either; it rolled its own blocking `UnixListener` accept loop with a nested tokio runtime. So most axes are genuinely **not-started** rather than "old-stack hybrid." The bright spots are bare naming and the binary-NOTA boundary, both of which are clean and carry forward.

| Axis | Status | Evidence | Work |
|---|---|---|---|
| daemon-shell-actor | not-started | no `build.rs`; `main.rs:4` = `from_environment().run()`; `daemon.rs:357` hand-written `serve_forever` blocking accept loop | author schema + `build.rs` (GenerationDriver/NexusDaemonShape), reduce `main.rs` to `run_to_exit_code()` on `ActorMultiListenerDaemon`, delete bespoke accept machinery |
| execution-nexus | not-started | dispatch is a hand-written `match` in `HarnessRequestHandler::event_for_request` (`daemon.rs:530`); no `NexusWork`/`Runner` | route requests through generated `NexusWork -> NexusAction` runner via triad-runtime `Runner::drive` |
| contracts-schema-next | not-started | `signal-harness/src/lib.rs:28` `use signal_channel`, `:439` `signal_channel! { channel Harness ... }`; no schema-next dep, no `build.rs`; only bare `.concept.schema` files | re-derive `signal-harness` (and new `meta-signal-harness`) via schema-next, delete `signal_channel!` |
| contract-shape-two | partial | `signal-harness` present, but NO `meta-signal-harness`; `Cargo.toml:23` leans on shared `signal-engine-management` | create `meta-signal-harness`; fold supervision/policy surface out of `signal-engine-management` into it |
| naming-bare | **done** | `Cargo.toml:2` `name = "harness"`; `flake.nix:76-77` bare; zero `persona-*` drift | none |
| storage-sema | not-started | no `sema-engine` in `src/`; `runtime.rs:23-27` in-memory fields; `INTENT.md:53` frames Sema as future | open harness-owned `harness.sema` via sema-engine (single-writer, schema-emitted route types) when durable history is needed |
| kameo-discipline | hybrid | `Harness` is a real actor (`runtime.rs:76`), but `supervision.rs:80` leaks a raw `std::thread::spawn` supervision thread running a nested `block_on` runtime; no `RestartPolicy` on any actor (`Infallible` only) | move supervision onto a RequestGate-style task feeding `SupervisionPhase`, declare `RestartPolicy`, drop per-connection `block_on` |
| nota-binary-boundary | **done** | `command.rs:35-44` accepts only `SignalFile`, rejects `InlineNota`/`NotaFile`; `:72` rkyv decode; no flags | none |
| intent-arch-docs | hybrid | `INTENT.md` accurate and drift-free, but `ARCHITECTURE.md:58` calls the daemon a "skeleton ... supervision witness" and `:191` cites `signal-engine-management` as the supervision contract; no mention of schema-next / meta-signal / emitted-shell target | add a target/migration section declaring the new architecture as the destination |

### Kameo hazards (mirrors terminal, audit 556)

The supervision plane repeats the terminal supervisor pattern: `supervision.rs:80` spawns the supervision listener on a raw `std::thread::spawn` whose `JoinHandle` is dropped (`_thread`), and `supervision.rs:191` builds a *second* nested `tokio::runtime::Runtime` inside that thread doing `runtime.block_on` per request. No `RestartPolicy` is declared — both `Harness` (`runtime.rs:79`) and `SupervisionPhase` (`supervision.rs:146`) use `type Error = Infallible` and rely on default behavior. The core `Harness` actor itself is clean (ask-based reads via `ReadState`, lifecycle via `SetHarnessLifecycle`), so the discipline debt is concentrated in the supervision/connection plumbing, which the emitted shell would replace wholesale.

### Migration path for harness

harness needs the full ground-up rebuild, in this order. (1) **Contracts first:** author `signal-harness.schema` and a brand-new `meta-signal-harness.schema`, add `schema-(rust-)next` + `build.rs` to both, generate `src/schema/`, delete the `signal_channel!` block and the borrowed `signal-engine-management` supervision surface. (2) **Emitted daemon shell:** add the daemon schema + `build.rs` (GenerationDriver/NexusDaemonShape), collapse `main.rs` to `<HarnessDaemon>::run_to_exit_code()` on triad-runtime's `ActorMultiListenerDaemon`, and delete the hand-written `BoundHarnessDaemon`/`serve_forever`/`HarnessConnection`/`HarnessFrameCodec` accept machinery. (3) **Nexus runner:** map each `HarnessRequest` operation to a `NexusAction` and drive via `Runner` instead of the hand-written match, keeping `Harness` as the kameo state actor (now with a declared `RestartPolicy`) and moving supervision onto the actor substrate rather than a leaked OS thread. (4) **Sema** stays deferred until durable transcript history is actually required. The two things that *don't* need to change — bare naming and the one-binary-rkyv startup boundary — already meet the target. Effort: **large**; gated on schema-rust-next emission, the actor-native triad-runtime substrate, and the creation of the missing `meta-signal-harness` repo.
