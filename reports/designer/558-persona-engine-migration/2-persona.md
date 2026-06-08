# 558.2 — persona — early (effort: large)

## persona — new-architecture migration assessment

**Role:** the privileged engine-MANAGER daemon (`persona-daemon` + `persona` CLI) — a system daemon supervising the other component daemons, owning component upgrade/version-handover, exposing engine/component status. Today it is a hand-written kameo+tokio daemon, **not** an emitted triad shell.

**Repos:** `persona`, `signal-persona`, `meta-signal-persona`, `signal-persona-origin` present; `signal-engine-management` present but a deprecated `pub use signal_persona::*;` compat re-export; `owner-signal-persona` already gone (deprecation complete).

**Overall:** early / large effort. EngineManager is a genuine kameo state actor and storage is genuinely on sema-engine, so the data spine is sound — but the daemon shell, contracts, nexus runner, config boundary, and naming are all pre-migration.

### Axis-by-axis

| Axis | Status | Evidence (file:line) |
|---|---|---|
| daemon-shell-actor | not-started | `src/bin/persona_daemon.rs:7` `PersonaDaemonCommand::from_environment()`+`run()`; `transport.rs:533` hand-written `loop { listener.accept().await }`; no build.rs, no schema-rust-next/triad-runtime dep |
| execution-nexus | n-a | no signal-executor anywhere; dispatch is `manager.rs:174` hand-written `match request`. Never on old executor; also not yet on generated nexus runner |
| contracts-schema-next | not-started | `signal-persona/src/lib.rs:384` and `meta-signal-persona/src/lib.rs:262` both `signal_channel! {`; no schema-next dep |
| contract-shape-two | hybrid | canonical signal-persona+meta-signal-persona pair exists, but `Cargo.toml:30` still deps `signal-engine-management` (re-export) and `manager_store.rs:11` imports `ComponentName` from it |
| naming-bare | partial | code/package bare; `flake.nix:12,16,20,21,22,26,27,55,59` still wire 9 deleted `persona-*` component inputs (k1i1 drift) |
| storage-sema | hybrid | `manager_store.rs:7` real sema-engine with typed tables + single ManagerStore writer; but hand-written descriptors and inline redb I/O |
| kameo-discipline | hybrid | `manager.rs:256` real kameo EngineManager; but `manager_store.rs:562` `spawn_in_thread`, `type Error = Infallible` (no RestartPolicy), inline redb in handler |
| nota-binary-boundary | partial | no NOTA parsing, no flags (good); but `transport.rs:598` socket-path arg + `PERSONA_*` env config, not one binary rkyv startup message |
| intent-arch-docs | done | `ARCHITECTURE.md:1780` honestly labels schema migration a future 'Target'; INTENT/ARCHITECTURE accurate, no overclaim |

### What is already right

Persona avoided two whole classes of debt. It never adopted signal-executor (so execution-nexus is a clean slate, not a teardown), and its durable state is already a single-writer `ManagerStore` kameo actor over sema-engine with typed tables — substantively the storage-sema target, just not emitted or off-thread. `EngineManager` is a real ask-driven kameo actor with `on_stop` draining. Docs are honest about the gap.

### What is pre-migration

The daemon process itself is the biggest gap: `PersonaDaemon::serve` is a bespoke `loop { listener.accept() }` (`transport.rs:533`) with an env-var-driven `PersonaDaemonCommand` (`transport.rs:597`), nowhere near the emitted `<Daemon>::run_to_exit_code()` shell on triad-runtime's RequestGate/ActorMultiListenerDaemon substrate. Both contracts are hand-written `signal_channel!`. The kameo hazards from audit 556 recur verbatim: `ManagerStore::start` uses `spawn_in_thread` on the state actor (`manager_store.rs:562`), no `RestartPolicy`, and redb I/O runs inline in the async handlers. Config arrives as a positional socket path plus a wall of `PERSONA_*` env vars rather than one binary rkyv message. The flake still references nine deleted `persona-*` component repos.

### Migration path for persona

Persona is gated on the same 553 substrate every component waits for (the generated nexus runner + emitted shell), but with an extra twist: it is the engine *manager*, so the emitted daemon shell must host not just a leaf state actor but the full `EngineSupervisor` / `DirectProcessLauncher` / `ComponentHandoffRouter` process-supervision tree — heavier than the spirit reference pilot exercises. Sequence: (1) lower a real `schema/persona.schema` (the `persona.concept.schema` sketch is a stub) and emit `signal-persona` + `meta-signal-persona` from schema-next, dropping `signal_channel!`; (2) fold `signal-engine-management` into `signal-persona` (repoint imports, drop the dep, retire the repo); (3) add the schema-rust-next build.rs + emitted daemon shell and replace the hand-written `persona_daemon.rs`/`serve()` with the one-liner on triad-runtime; (4) move request dispatch onto the generated nexus runner; (5) fix the kameo hazards (drop `spawn_in_thread`, add `RestartPolicy`, `spawn_blocking` the redb I/O) and emit the SEMA descriptors; (6) replace the `PERSONA_*` env config with one binary rkyv startup message; (7) rewrite `flake.nix` inputs to bare component names. Storage and the state-actor core carry over largely intact.
