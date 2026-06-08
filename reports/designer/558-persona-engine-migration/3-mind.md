# 558.3 — mind — partial (effort: large)

## mind — new-architecture migration assessment

**Role.** `mind` is Persona's central control-plane state component — work graph, typed Thought/Relation records, subscriptions, and channel-choreography policy persisted in `mind.sema`. It is the strongest real `sema-engine` consumer in the fleet and is meant to retire lock-file orchestration.

**Repos.** All three triad legs present: `mind`, `signal-mind`, `meta-signal-mind`. mind is notably ahead of message/introspect/harness/system in already carrying its own meta contract.

### Axis-by-axis

| Axis | Status | Evidence | Work |
|---|---|---|---|
| daemon-shell-actor | not-started | `main.rs:5` `MindCommand::from_env().run(...)`; no `build.rs`; `transport.rs:270` hand-written `serve_forever` accept loop; zero triad-runtime. | Lower a schema, add build.rs (GenerationDriver+NexusDaemonShape), emit the daemon shell, reduce bin to `run_to_exit_code()`, reseat on ActorMultiListenerDaemon+RequestGate. |
| execution-nexus | not-started | No signal-executor anywhere (never adopted — not on the 555 list); execution is the bespoke `root -> ingress -> dispatch -> store` ask chain (`root.rs:95`). | Route MindRequest through the emitted nexus runner (NexusWork->NexusAction, Runner::drive) once the shell lands. |
| contracts-schema-next | not-started | `signal-mind/src/lib.rs:1240` and `meta-signal-mind/src/lib.rs:218` both `signal_channel! {`; no schema-next dep; only bare `*.concept.schema` files. | Author + lower `signal-mind.schema`/`meta-signal-mind.schema`, add schema-(rust-)next dep + generated `src/schema/`, delete `signal_channel!`. |
| contract-shape-two | hybrid | Both `signal-mind` + `meta-signal-mind` exist; `meta-signal-mind/INTENT.md` confirms it is the Spirit-owned meta policy channel. Daemon also deps `signal-engine-management` (`Cargo.toml:26`) and `meta-signal-orchestrate` (`:22`). | Shape holds (those two extras are shared/peer contracts, not a mind third contract); keep it that way. |
| naming-bare | done | `Cargo.toml:2` `name = "mind"`, bin `mind`; `flake.nix` has 0 persona- references. | None; only a stale `result` symlink to `persona-mind-test` (build artifact). |
| storage-sema | hybrid | `tables.rs:143` `Engine::open(...)`, `:197` assert, `:261` subscribe; `StoreKernel` is the single writer (`store/mod.rs:200` comment). | Emit the SEMA Table/TableDescriptor + stored-record types from schema instead of hand-declaring (`tables.rs:23,150`). |
| kameo-discipline | hybrid | Real actor tree, ask-not-tell; hazards: `store/mod.rs:206` `.spawn_in_thread()` with inline redb/sema in handlers, no `RestartPolicy` declared anywhere, supervision is `tokio::spawn` aborted on Drop (`supervision.rs:109,122`). | spawn_blocking inside an async StoreKernel, declare RestartPolicy, supervise the listener actor. |
| nota-binary-boundary | partial | CLI NOTA-correct (`command.rs:130`,`:113`); daemon parses `--socket`/`--store`/`--actor` flags (`command.rs:222-229`). | Replace daemon flags with one binary rkyv startup config; NOTA stays at the CLI edge only. |
| intent-arch-docs | done | `INTENT.md` matches code; `ARCHITECTURE.md:254` honestly documents spawn_in_thread as Template-2 debt, `:228` flags trace phases awaiting actor graduation. | Refresh on the shell/nexus migration. |

### Migration path for mind

mind is a paradox: it has the **best storage and docs** in the fleet (a true single-writer sema-engine consumer with honest, current architecture notes) but is **furthest from the emitted-shell/nexus target** because the entire daemon, contracts, and execution pipeline are hand-authored and predate the schema-next era. It never touched signal-executor, so there is nothing to remove — but there is also no generated layer to inherit. The work is therefore additive and gated on shared substrate: (1) lower a `mind.schema` plus the two contract schemas; (2) once schema-rust-next can emit a NexusDaemonShape daemon, replace `main.rs`/`transport.rs`'s hand-written `MindDaemon`/`serve_forever` with the emitted shell on triad-runtime's actor-native substrate, deleting the flag parser in favor of one binary rkyv config; (3) move request execution onto the generated nexus runner, retiring the bespoke ingress/dispatch/domain phase chain; (4) regenerate the SEMA routes from schema and clean up the kameo hazards (spawn_blocking over spawn_in_thread, RestartPolicy, supervised listener). Because mind's sema layer is already correct, the migration is mostly about wrapping it in the generated shell — large in mechanical surface, low in conceptual risk.
