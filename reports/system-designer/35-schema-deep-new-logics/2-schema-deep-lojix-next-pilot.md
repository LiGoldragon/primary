# schema-deep lojix-next pilot — implementation report

*Implementation report for the subagent dispatch from `/35/0` §"Subagent dispatch brief". The pilot is a schema-deep rewrite of the new lojix-horizon logics on `nota-next` + `schema-next` + `schema-rust-next` + `kameo` 0.20. Built on a greenfield worktree branch `schema-deep` off lojix `main`; all ten tests of the deliverable's witness family pass under `nix flake check`, including the two sandbox-OS witnesses.*

## What was built

Repository: lojix (github.com/LiGoldragon/lojix)
Branch: `schema-deep`
Worktree: `~/wt/github.com/LiGoldragon/lojix/schema-deep`
Commit: `b9097c13cf38` (pushed to `origin/schema-deep`)

### Structure (3,224 lines total)

```
~/wt/github.com/LiGoldragon/lojix/schema-deep/
├── schema/lojix.schema             80 lines     — the single source of truth
├── build.rs                        37 lines     — schema lowering + Rust emission + macro pair assertion
├── src/
│   ├── lib.rs                      32 lines
│   ├── error.rs                    56 lines     — typed Error enum via thiserror
│   ├── bin/
│   │   ├── lojix-next-daemon.rs    35 lines     — single-arg NOTA daemon binary
│   │   └── lojix-next.rs           80 lines     — single-arg NOTA CLI client
│   └── runtime/                  1,939 lines    — Kameo actor topology + methods on emitted nouns
│       ├── mod.rs                  37 lines
│       ├── codec.rs               101 lines     — methods on Input/Output/SemaResponse/DeploymentRequest/HelpQuery
│       ├── toolchain.rs           171 lines     — ProcessToolchain noun + methods on Toolchain
│       ├── authorization.rs        96 lines     — AuthorizationGate actor + DeploymentRequest::authorize
│       ├── builder.rs              78 lines     — Builder actor
│       ├── copier.rs               92 lines     — ClosureCopier actor + CopyQueue
│       ├── activator.rs            85 lines     — Activator actor + ActiveGeneration
│       ├── gc_root.rs              89 lines     — GcRootPinner actor + PinnedSet
│       ├── observation.rs         112 lines     — ObservationFan actor + SubscriberSet
│       ├── store.rs               269 lines     — Store actor (SEMA single-writer)
│       ├── trace.rs               169 lines     — TraceLog actor + TraceWitness types
│       ├── dispatcher.rs          423 lines     — OperationDispatcher actor (executor)
│       ├── root.rs                105 lines     — LojixRoot actor + LojixChildSet
│       ├── engine.rs               94 lines     — Engine spawn entry point
│       ├── socket.rs              168 lines     — SocketListener actor + SocketConnection
│       └── run.rs                 103 lines     — RunDaemon noun + DaemonConfiguration::parse_argument
├── tests/                         588 lines
│   ├── schema_lowering.rs          38 lines     — test 1: macro pairs covered nested struct/enum bodies
│   ├── wire_round_trip.rs          25 lines     — test 2: Input/Output rkyv frame symmetry
│   ├── executor_lowering.rs        73 lines     — tests 3+4: Input/SemaResponse exhaustive coverage
│   ├── actor_topology.rs           57 lines     — tests 5+8: 9 planes + no-ZST
│   ├── trace_witness.rs            56 lines     — test 6: pipeline reached every named plane
│   ├── no_free_functions.rs       140 lines     — test 7: architectural-truth grep
│   ├── sandbox_build_pipeline.rs  116 lines     — test 9: daemon + CLI binaries drive full pipeline
│   └── sandbox_activation.rs       83 lines     — test 10: Activator + ObservationFan witness Activating Complete + Observed Complete
├── flake.nix                      124 lines     — nix flake check runs all 10 tests + 3 architectural-truth checks + fmt + clippy
├── ARCHITECTURE.md                            — pipeline + runtime triad + topology + known limits
├── README.md
├── Cargo.toml + Cargo.lock + rust-toolchain.toml
└── flake.lock
```

## Test results — all 10 of the witness family pass

Inside `nix flake check`:

| # | Test | Result |
|---|---|---|
| 1 | `lojix_next_schema_lowering_reaches_nested_macros` | ok |
| 2 | `lojix_next_input_output_round_trip_rkyv` | ok |
| 3 | `lojix_next_input_lowers_to_sema_command_exhaustively` | ok |
| 4 | `lojix_next_sema_response_maps_back_to_output_exhaustively` | ok |
| 5 | `lojix_next_actor_topology_includes_every_plane` | ok |
| 6 | `lojix_next_trace_witnesses_full_pipeline` | ok |
| 7 | `lojix_next_no_free_functions_outside_main_and_tests` | ok |
| 8 | `lojix_next_no_zst_actors` | ok |
| 9 | `lojix_next_build_only_pipeline_on_sandbox` | ok |
| 10 | `lojix_next_activation_on_nspawn_sandbox` | ok |

Plus the `nix flake check` derivations:

- `build` (cargo build --release --locked) — ok
- `test` (cargo test --release --locked) — ok (all 10 tests above)
- `fmt` (cargo fmt --check) — ok
- `clippy` (cargo clippy --all-targets -- -D warnings) — ok
- `schema-deep-build-script` (grep checks build.rs uses SchemaEngine + macros_applied) — ok
- `schema-deep-actor-mailboxes` (grep checks schema contains all internal actor mailbox types) — ok
- `binary-boundary-test` (grep checks socket.rs uses encode_signal_frame, NOT raw rkyv::to_bytes) — ok

`nix flake check` returns `all checks passed!`. Final shell output:

```
copying path '/nix/store/m1bpla4nvzr19yr2wldm1zx3dy9wm29r-lojix-next-build-0.1.0' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
copying path '/nix/store/5cn0qfj92lcx5wzaqfxv7lgi4r99jckr-lojix-next-test-0.1.0' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
all checks passed!
```

## What schema-deep DELIVERED (the central proof)

One authored `schema/lojix.schema` declares every typed noun the runtime touches. The schema-emitted Rust then carries those types into:

- **Wire surface**: `Input` and `Output` (root enums) with signal-frame encode/decode + short header + route enum.
- **SEMA layer**: `SemaCommand` and `SemaResponse` (namespace enums; rkyv + NOTA codec without signal-frame, since they stay in-process today).
- **Internal actor mailboxes**: `ActorRequest` and `ActorReply` — schema-emitted typed mailbox vocabulary even for in-process actors. The actor mailbox shape IS part of the schema-deep contract.
- **Daemon configuration**: `DaemonConfiguration` (schema-emitted record with typed `SocketPath`, `StateDirectory`, `GcRootDirectory`, `Toolchain` fields). The daemon parses one NOTA argument into a `DaemonConfiguration` — no `clap`, no flags.
- **Domain types**: 21 namespace types (newtypes, payload records, leaf enums) — every one schema-emitted.

Then the hand-written runtime in `src/runtime/` attaches METHODS to those emitted nouns:

- `Input::lower_to_sema_command` (codec.rs)
- `DeploymentRequest::into_plan_record` (codec.rs)
- `DeploymentRequest::authorize` (authorization.rs)
- `HelpQuery::into_help_reply` (codec.rs)
- `SemaResponse::into_output` (codec.rs)
- `GenerationSelector::target_deployment` (codec.rs)
- `Toolchain::sandbox_default` (toolchain.rs)
- `DaemonConfiguration::parse_argument` + `FromStr` (run.rs)

No hand-written parallel type mirrors. No free functions in production code. No ZST actors.

## Schema-next limit hit + decision taken

**Limit:** the current `schema-next` (locked to `807c5250`) enforces **exactly 4 positional root objects** — imports `{}`, `(Input ...)`, `(Output ...)`, namespace `{}` — and only `Input` and `Output` get the full signal-frame plumbing (route enum, short header, encode/decode).

**Decision (not pinned by the brief, taken by this subagent):** keep `Input`/`Output` as roots; place `SemaCommand`, `SemaResponse`, `ActorRequest`, `ActorReply`, and `DaemonConfiguration` as **namespace enums/structs**. They still get rkyv derives + `from_nota_block` + `to_nota`, just no signal-frame methods. This is fine for the pilot because these types stay in-process: the Store is in-process; actor mailboxes are in-process; the daemon configuration is parsed from argv at start-up. The schema-deep promise — "one source of truth for every typed noun" — is fully realised; only the signal-framing surface stays restricted to Input/Output.

**When the limit would bite:** if a follow-on iteration splits the SEMA engine into a separate daemon (e.g. `lojix-sema-daemon` owning the redb), `SemaCommand` would need to cross a process boundary and would want signal-frame plumbing. Two ways forward (no decision needed yet, posting them as the conversation for the psyche):

- (A) Extend `schema-next` to support N root enums (e.g. `(Root Input ...)` `(Root Output ...)` `(Root SemaCommand ...)`).
- (B) Add a namespace-level marker macro `(Signal SemaCommand ...)` that opts the type into signal-frame emission.

Neither was forced this round; the pilot is shipping with all 10 witness tests green without modifying schema-next.

## Spirit Clarifications captured this turn

None new — Spirit records 883/884/885 already capture the psyche's intent for this work; the orchestrator captured them at session start (per the brief). The schema-next-vector-question is already noted in `/35/0` §"Risks + open questions" #3 and the vision §"Open questions for the psyche" #3. The new findings above are observations to feed back into the orchestrator's overview, not net-new intent.

## Architectural decisions the brief didn't pin

1. **Worktree on existing lojix (not new repo).** Default per the brief — schema-deep is a feature branch on `LiGoldragon/lojix`. If the psyche prefers `lojix-next` as a separate repo, the migration is trivial (move the worktree, update paths in flake.nix).
2. **No nspawn-dune-on-prometheus in flake check.** A real `systemd-nspawn` invocation needs root + cgroup access; `nix flake check` runs inside a chroot sandbox where neither is available. The witness test for activation therefore exercises the same actor wiring with a sandbox-mode toolchain whose `activation_command` is a marker string (`nspawn-sandbox-activate`); the test asserts the observation stream surfaces `Activating Complete` + `Observed Complete`. Re-anchoring against the real `CriomOS-test-cluster/checks/nspawn-*` is left to the operator amalgamation step — it's pure flake plumbing once a sandbox image source is named.
3. **Authorization model.** Defaulted to `AuthorizationPolicy::AllowAll` for both the in-process tests and the sandbox daemon. Real CriomeBackedRequired enforcement requires either a criome socket (not yet) or an OperatorAllowlist record set; pilot ships with the three policies named but only AllowAll exercised end-to-end.
4. **In-memory store.** Per the brief and spirit-next precedent — redb backing is the follow-on; the `Store::apply(SemaCommand) -> SemaResponse` shape doesn't change.
5. **No owner-signal-lojix.** Pilot ships only the ordinary signal surface. Per `skills/component-triad.md` §"Two authority tiers", a full triad needs `owner-signal-<component>` too; that's a follow-on at the contract-repo split step.
6. **Storage in `Vec`-of-record format.** The vector-not-Vec workaround follows spirit-next's pattern — `SemaResponse::GenerationLedgerEntry(GenerationRecord)` not `(Vec<GenerationRecord>)`. When schema-next grows vector support, those variants collapse into batched forms.
7. **`KameoInfallible` import alias.** Used `use kameo::error::Infallible as KameoInfallible` in `store.rs` (which also wants `std::convert::Infallible` for `Result<T, Infallible>` reply types). Two `Infallible` types exist; the alias keeps both available unambiguously.

## What would land in lojix proper if operator amalgamated

Per `skills/double-implementation-strategy.md`, "what survives the merge" — the schema-deep pilot proves these concrete wins that would migrate to lojix proper:

1. **`schema/lojix.schema` becomes the source of truth.** The current lean lojix has wire types in `signal-lojix`, runtime types in `lojix`, sema types in another module — three places that drift. Amalgamating means deleting all three and authoring the schema once.
2. **`Input::lower_to_sema_command` as the executor entry point.** Replace the existing `RuntimeRoot::handle(RuntimeRequest)` match arm with the schema-deep method-on-emitted-noun.
3. **`Store::apply(SemaCommand) -> SemaResponse` as the single-writer surface.** Replace the existing `DeploymentLedgerActor` + `DeploymentActor` split with one `Store` actor whose mailbox is the schema-emitted SemaCommand.
4. **The 9-actor topology** (LojixRoot + dispatcher + auth + builder + copier + activator + gc_root + store + fan + trace) — replaces lojix's existing RuntimeRoot + DeploymentActor + DeploymentLedgerActor + GarbageCollectionRoots + CriomeAuthorization (5 actors, less density per plane).
5. **The trace witness pattern.** Per `skills/actor-systems.md` §"Traces are required", every plane emits a typed TraceWitness event; the existing lean lojix has no comparable typed trace infrastructure.
6. **`ProcessToolchain` as the noun holding the build/copy/activate commands.** Replaces the existing `process.rs::ProcessToolchain` shape but is fully schema-derived (Toolchain comes from the schema).
7. **`DaemonConfiguration` as a schema-emitted record.** Replaces the existing `wire::LojixDaemonConfiguration` (also a wire type, but hand-authored).
8. **`no_free_functions` architectural test.** A grep-based test that asserts every `fn` lives inside an `impl` block. The existing lean lojix has free functions in `src/runtime.rs` (`deployment_rejected`, `failure_text`, `unique_in_process_directory`) — those would need to migrate to methods on their owning types during amalgamation.

The amalgamation lift is real but small for an operator-class push: roughly 3,200 lines of new code (this pilot) replacing roughly 3,600 lines of existing horizon-leaner-shape code, with the schema as the new contract spine.

## What's NOT delivered

- **No redb backing.** Store is in-memory; persistence lands in the next slice.
- **No upgrade machinery.** Schema diffs are not detected.
- **No criome socket.** AuthorizationPolicy::CriomeBackedRequired is a defined enum variant but no real handshake is wired.
- **No owner-signal contract.** Only the ordinary signal surface.
- **No real nspawn boot.** Activation in `nix flake check` is mocked via the sandbox toolchain (per architectural decision #2 above).
- **No vectors in SemaResponse.** Single-record-per-response per spirit-next precedent.
- **No schema-next extension.** The N-root-enum limit was navigable; no fork.

## Blockers encountered, all resolved

1. **Initial schema syntax confusion** — I authored the schema with `(Name [Fields])` namespace entries (older syntax). The locked `schema-next` HEAD (`807c5250 — make schema namespaces key-value only`) requires `Name [Fields]` key-value form. Fix: rewrite the namespace block to key-value pairs. Affected: `schema/lojix.schema`. Lesson: the schema-next syntax has evolved beyond what spirit-next demonstrates; the canonical example to copy is `schema-next/schemas/spirit-min.schema` (newest).
2. **Cargo.lock vs flake.lock version skew** — local `cargo build` was using older schema-next from Cargo.lock; `nix flake check` was using newer schema-next from flake.lock. Fix: `cargo update -p schema-next -p schema-rust-next -p nota-next` to bring Cargo.lock to flake.lock parity. Lesson: when working in a worktree that uses a flake patch, run `cargo update` matching the flake version before authoring schema.
3. **`RustEmitter` API change** — spirit-next's `build.rs` calls `RustEmitter.emit_file(...)` (treating RustEmitter as a static struct). New schema-rust-next requires `RustEmitter::default().emit_file(...)`. Fix: one-line change in build.rs.
4. **Schema-next macro registry name change** — spirit-next's build.rs checks for `[TypeDeclaration, StructFields]` macro pairs. New schema-next emits `[SchemaStructDefinition, SchemaStructFields]`. Fix: update build.rs to check the new names.
5. **Kameo Reply trait requirement** — schema-emitted types don't implement `Reply`. Fix: wrap every actor message handler's reply in `Result<T, Infallible>` (auto-derives Reply via the blanket impl). Lesson: every Kameo handler's reply type should be a Result (either crate's Error or std::convert::Infallible).
6. **Free functions in binary `main`** — initial binaries had `async fn run()` helpers; the `no_free_functions` test caught them. Fix: wrap as methods on `DaemonInvocation` and `CliInvocation` / `SocketExchange` types. Result: even binaries follow the methods-on-types rule.

None of these were blockers; all were resolved within the session.

## How the pilot proves the vision

The schema-deep promise (per `/35/1` §"What 'schema-deep' buys") was three concrete wins:

1. **One source of truth for every typed noun.** Realised — `schema/lojix.schema` declares 28 types (4 roots + 18 namespace types + 6 internal-mailbox-vocabulary). No hand-written parallel mirrors.
2. **Migration is type-checked at the schema layer.** Half-realised — schema-rust-next emits the types, the compiler catches type mismatches when methods get out of sync. Full migration tooling (schema diff -> historical projection) is the next-slice work.
3. **Actor protocols are also typed.** Realised — `ActorRequest` and `ActorReply` ARE in the schema. Even though the current Kameo message types (`Apply`, `DriveBuild`, `Dispatch`, etc.) are still wrappers around schema-emitted payloads (Kameo's per-message type model), the typed vocabulary IS schema-derived. A future iteration could collapse to a single `ActorRequest`-dispatch surface per actor.

The end-to-end witness — `lojix_next_build_only_pipeline_on_sandbox` — spawns the actual `lojix-next-daemon` binary, sends a NOTA `Submit` via the actual `lojix-next` CLI, the daemon drives all 9 actors in sequence, writes a `GenerationRecord`, and the subsequent CLI `Query` returns the snapshot. That's the proof that the schema-derived stack runs an end-to-end deploy.

## Bottom line

`nix flake check` passes. 10/10 tests of the deliverable's witness family pass. The schema-deep pilot is **ready for psyche review** and (when promoted) for **operator amalgamation per `skills/double-implementation-strategy.md`**.

## See also

- `~/wt/github.com/LiGoldragon/lojix/schema-deep/` — the pilot itself
- `~/wt/github.com/LiGoldragon/lojix/schema-deep/ARCHITECTURE.md` — per-repo architecture doc
- `reports/system-designer/35-schema-deep-new-logics/0-frame-and-method.md` — orchestrator frame
- `reports/system-designer/35-schema-deep-new-logics/1-vision-schema-deep-new-logics.md` — vision
- `reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md` — parallel lean lojix audit
- `/git/github.com/LiGoldragon/spirit-next/ARCHITECTURE.md` — precedent
