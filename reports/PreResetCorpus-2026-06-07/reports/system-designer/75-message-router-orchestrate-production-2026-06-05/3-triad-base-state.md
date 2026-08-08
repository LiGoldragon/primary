# 3 — The triad base state: how a production triad daemon is built TODAY

Source-grounded against `spirit` (HEAD `f7951b8`), `triad-runtime` (HEAD
`28d03c3`), `schema-rust-next` (HEAD `c0a331a`), `sema-engine` (HEAD `e1aeef1`),
and the contract-repo / Spirit-record state, all read 2026-06-05. This report
documents the actual build recipe a port (message / router / orchestrate)
follows, with exact type and function names, plus an honest landed-vs-blocked
table.

## The one-sentence shape

A production triad daemon is **a component crate that (1) checks in three
`.schema` files, (2) lets `schema-rust-next`'s `build.rs` driver emit three
generated plane modules carrying the engine *traits*, (3) hand-writes the three
engine trait *impls* + a `Store` over `sema-engine`, and (4) hand-writes a tiny
daemon shell that hands its runtime to `triad-runtime`'s
`SingleListenerDaemon` (or `MultiListenerDaemon`) and a CLI that uses
`ComponentCommand` + a transport.** There is no macro that generates `main`; the
emitter stops at the engine traits + the runner adapter. `spirit` is the worked
example for every line of that recipe.

## The canonical build recipe, step by step

### Step 0 — Three plane schema files in `schema/`

`spirit/schema/` holds exactly three files, each a NOTA structural document
(parsed through `nota-next`'s structural-macro-node codec, then `schema-next`):

- `signal.schema` — the wire contract. Top of file: the operation-root enum
  `[State Record Observe Lookup Count Remove ChangeCertainty LookupStash]`
  (the `Input` roots) and the reply-root enum
  `[RecordAccepted RecordsObserved ... Error Rejected]` (the `Output` roots),
  then the declaration block of every payload, receipt, validation-error enum,
  and the `Entry`/`Statement`/`Query` shapes. The header line `{}` plus the
  `Import`/`Export`/`SignalReuse` declarations show the cross-schema reuse hook.
- `nexus.schema` — the decision plane. Its declaration header **imports**
  Signal+SEMA types by single-colon path (`spirit:signal:Input`,
  `spirit:sema:ReadInput`, …). It declares the two driving enums:
  `NexusWork [(SignalArrived ...) (SemaWriteCompleted ...) (SemaReadCompleted ...) (EffectCompleted ...)]`
  (facts the runner re-enters) and
  `NexusAction [(CommandSemaWrite ...) (CommandSemaRead ...) (ReplyToSignal ...) (CommandEffect ...) (Continue ...)]`
  (actions). It also declares the component's effect catalog —
  `NexusEffectCommand [(Stash ...) (ClassifyState ...)]` and
  `NexusEffectResult [(Stashed ...) (StateClassified ...)]`. **This nexus schema
  IS the engine's visible internal-feature catalog** (intent `z6qu`, VeryHigh):
  every internal feature is a declared verb+object here.
- `sema.schema` — the storage plane. Imports Signal types, declares
  `WriteInput [(Record ...) (Remove ...) (ChangeCertainty ...)]`,
  `ReadInput [(Observe ...) (Lookup ...) (Count ...)]`, and the matching
  `WriteOutput`/`ReadOutput` reply enums.

The three files are positional NOTA records (type first, no key:value), per the
NOTA discipline. `asschema` is **gone** from `spirit`, `schema-rust-next`,
and `schema-next` (verified: empty grep) — the pipeline is now
`.schema → src/schema/*.rs` directly.

### Step 1 — `build.rs` emits the three plane modules

`spirit/build.rs` is ~38 lines. It declares `cargo:rerun-if-changed` for each
`schema/*.schema` and its emitted `src/schema/*.rs`, then:

```
let plan = GenerationPlan::new(&crate_root, "spirit", "0.1.0")
    .with_module(ModuleEmission::signal_runtime_module("signal"))
    .with_module(ModuleEmission::nexus_runtime())
    .with_module(ModuleEmission::sema_runtime());
GenerationDriver::new(plan)
    .generate()
    .expect(...)
    .write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")
    .expect("checked-in spirit schema artifacts are fresh");
```

The API surface a port copies (from `schema_rust_next::build`):
`GenerationPlan::new(crate_root, crate_name, version)`,
`ModuleEmission::signal_runtime_module(name)` /
`ModuleEmission::nexus_runtime()` / `ModuleEmission::sema_runtime()`,
`GenerationDriver::new(plan).generate()` →
`GeneratedPackage::write_or_check(UPDATE_VAR)`. `write_or_check` writes the
files when the env var is set, otherwise asserts the checked-in `src/schema/*.rs`
are byte-identical to a fresh emission (`StaleGeneratedArtifact` error
otherwise). It also round-trips the schema source through text AND binary rkyv
archive before emitting (`SourceArtifactRoundTrip::validate`), so a corrupt
schema fails the build.

`ModuleEmission` chooses an emission target. The five targets
(`RustEmissionTarget`, in `schema-rust-next/src/lib.rs`):

| Target | `runtime_planes()` | Used for |
|---|---|---|
| `WireContract` | none | contract repos (`signal-*`, `meta-signal-*`) — types + NOTA codec, no engine traits |
| `ComponentRuntime` | all | single-crate component emitting all three planes into `lib` |
| `SignalRuntime` | signal only | the per-plane signal module inside a daemon |
| `NexusRuntime` | nexus only | the per-plane nexus module |
| `SemaRuntime` | sema only | the per-plane sema module |

`spirit` uses the three per-plane targets (one module each). The generated files
land at `spirit/src/schema/{signal,nexus,sema}.rs` (signal.rs 41KB, nexus.rs
30KB, sema.rs 24KB — all checked in).

### Step 2 — What the emitter generates (the traits a port implements against)

For each plane module, `schema-rust-next` emits the wire nouns + a plane
**engine trait** with default lifecycle hooks. The three traits (emitted, not
hand-written — verified at `lib.rs` lines 3724–3925):

`SignalEngine` — admission/triage/reply. Default `on_start`/`on_stop` returning
`Ok(())`; trace hooks (`trace_signal_admitted/rejected/triaged/replied`); two
required methods the component supplies — `triage_inner(signal::Signal<Input>)
-> nexus::Nexus<Work>` and `reply_inner(nexus::Nexus<Action>) ->
signal::Signal<Output>` — wrapped by emitted `triage`/`reply` that fire the
trace hooks. (For the split-crate case it emits associated types `NexusInput`/
`NexusOutput` instead of concrete nexus types.)

`NexusEngine` — the decision plane, and the load-bearing one. Default
`on_start`/`on_stop`; `continuation_limit()` defaulting to
`ContinuationLimit::default()` (32 steps); the component-supplied required
methods:
- `decide(&mut self, nexus::Nexus<Work>) -> nexus::Nexus<Action>` — one step.
- `apply_sema_write(&mut self, origin_route: OriginRoute, input: <SemaWrite>) -> <SemaWriteOutput>`
- `observe_sema_read(&self, origin_route: OriginRoute, input: <SemaRead>) -> <SemaReadOutput>`
- `run_effect(&mut self, input: <EffectCommand>) -> <EffectResult>`
- `budget_exhausted_reply(&self, exhausted: ContinuationExhausted) -> <Reply>`

…and the **emitted, non-overridden** `execute(&mut self, nexus::Nexus<Work>) ->
nexus::Nexus<Action>` that owns the recursive runner loop. `execute` builds a
`triad_runtime::Runner::new(self.continuation_limit())`, wraps `self` in an
emitted `NexusRunnerAdapter`, and calls `runner.drive(&mut adapter,
first_work)`. **This is the entire integration point with the runner — the
author writes the five hooks; the generator writes `execute` + the adapter.**
(Intent `rpr5`: the bundled triad runner adapter is generated glue only;
authors implement the three plane engines + effect handler + budget reply.)

`SemaEngine` — storage. Default `on_start`/`on_stop`; component-supplied
`apply_inner(sema::Sema<WriteInput>) -> sema::Sema<WriteOutput>` and
`observe_inner(sema::Sema<ReadInput>) -> sema::Sema<ReadOutput>`; emitted
`apply`/`observe` wrap them with trace hooks.

The emitter also generates `ActorStartFailure`/`ActorStopFailure` enums
(`ResourceBusy`/`ConfigurationInvalid`, `ResourceLocked`/`ChildStillRunning`)
with `Display`+`Error` impls — these are the typed lifecycle error surface
persona supervision uses (intent `czw0`: minimal `on_start`/`on_stop` is the
supervision surface). The generated plane roots also `impl
triad_runtime::{NexusWork, NexusAction, SemaWriteInput, SemaReadInput, ...}`
marker/role traits, so the runner can speak through the role interfaces (intent
`jo1x`).

### Step 3 — Hand-written engine impls + Store over sema-engine

The component crate hand-writes:

- `engine.rs` — the `Engine` composer + `SignalActor` impl of `SignalEngine`.
  `Engine::handle(input)` is the full request path: `signal_actor.admit(input)`
  (mints origin route + message identifier, validates), then under the nexus
  mutex `accepted.process_with(&signal_actor, &mut nexus)` which triages →
  `NexusEngine::execute` → reply, firing the sent/processed mail-ledger hooks
  around the handoff. `Engine::start/stop` call the generated `on_start`/`on_stop`
  on nexus then signal (start) / signal then nexus (stop).
- `nexus.rs` — `Nexus` impl of `NexusEngine`. `decide` delegates to a
  hand-written `step_decide(NexusWork) -> NexusAction` match (SignalArrived →
  command, SemaWriteCompleted → reply, SemaReadCompleted → effect-or-reply,
  EffectCompleted → reply). `apply_sema_write`/`observe_sema_read` forward to
  `SemaEngine::apply`/`observe` on the `Store`. `run_effect` runs the
  component's effect set (`Stash`, `ClassifyState`). `budget_exhausted_reply`
  builds an `Output::error`. The Observe→Stash→reply recursion lives entirely
  here as schema-declared effect commands — the runner re-enters each effect
  result as `NexusWork::EffectCompleted`.
- `store.rs` — `Store` impl of `SemaEngine` over `sema-engine`. **It uses
  `sema_engine::Engine` exclusively; no raw `redb` anywhere** (verified: empty
  grep for `redb::` in `spirit/src`, no `redb` in `Cargo.toml`). It registers
  one `IdentifiedTableReference<Entry>` via `register_identified_table`, and maps
  generated SEMA roots onto `assert_identified` / `match_identified` /
  `mutate_identified` / `retract_identified` / `current_commit_sequence`. The
  `DatabaseMarker` (commit sequence + blake3 content digest of committed
  records) is computed here. This honors the `fosp` correction (sema-engine is
  the exclusive DB boundary; the pilot's earlier raw-redb bypass was wrong and
  is no longer present).
- `plane.rs` — `From` impls bridging the per-plane `OriginRoute` /
  `ActorStartFailure` / `ActorStopFailure` newtypes across the three modules.
  This is pure projection glue (it should ideally be schema-shared; see limits).

### Step 4 — Daemon shell + CLI against triad-runtime

The daemon `main` is **hand-written** (no `triad_main!` macro exists — verified
empty grep across all three repos). `spirit/src/daemon.rs` does:

- `DaemonCommand::from_environment()` → `ComponentCommand::from_environment()`
  (single-argument rule: the daemon takes exactly one arg, a signal-encoded /
  rkyv `Configuration` file path; `signal_file_argument()` rejects inline NOTA).
- `Daemon::run()` builds a `SpiritDaemonRuntime { engine: Engine }` and hands it
  to `SingleListenerDaemon::new(socket_path, runtime, RequestErrorLog::new(
  "spirit-daemon")).run()`.
- `SpiritDaemonRuntime` impls `triad_runtime::DaemonRuntime` — the **exact
  plug-in trait**: `type RequestError: Display` + `StartError` + `StopError`;
  `fn start(&mut self)` → `engine.start()`; `fn stop(&mut self)` →
  `engine.stop()`; `fn handle_stream(&mut self, UnixStream)` → read input via
  `SignalTransport`, `engine.handle(input)`, write output.

`SingleListenerDaemon::run()` is: `bind()` → `start()` → `serve_streams()`
(blocking `incoming()` loop, per-request errors logged and swallowed via
`RequestErrorLog`, not fatal) → `stop()`. Constructor signature:
`SingleListenerDaemon::new(socket_path: impl Into<PathBuf>, runtime: Runtime,
request_error_log: RequestErrorLog)`; optional `.with_socket_mode(SocketMode)`.

`transport.rs` — `SignalTransport<Stream>` wraps the generated
`encode_signal_frame`/`decode_signal_frame` (which return rkyv bytes) inside
`triad_runtime::LengthPrefixedCodec` + `FrameBody` (4-byte big-endian length
prefix). `connect`, `exchange`, `write_input`/`read_input`,
`write_output`/`read_output`.

`config.rs` — `Configuration` is an rkyv-archived struct (socket path, database
path, optional trace socket). The daemon reads the binary file; it intentionally
never parses NOTA at startup (intent `7x50`: production daemons consume a
pre-encoded typed binary bootstrap artifact).

`src/bin/spirit-daemon.rs` is 9 lines (`DaemonCommand::from_environment().run()`).
`src/bin/spirit.rs` is the CLI: `ComponentCommand::from_environment()` →
`nota_argument()` (inline-or-file), parse the NOTA into `Input` via the
generated `parse::<Input>()`, `SignalTransport::connect(socket).exchange(&input)`,
print the `Output`. The CLI is the daemon's first client, not a triad leg.

### The MultiListenerDaemon path (the two-listener / meta-signal wiring)

`triad-runtime` HEAD `28d03c3` "add multi-listener daemon shell" — the
`MultiListenerDaemon` is **committed and tested**, not an uncommitted working
copy. Intent `rcn3` (Correction, High) is explicit: an earlier refresh report
wrongly claimed triad-runtime had only single-listener; the multi-socket
primitive already ships. So a component that needs an ordinary peer socket AND a
meta-signal policy socket does NOT build a new daemon — it implements
`MultiListenerRuntime`:

- `type Listener: Clone + Display` — the component's own listener-tag enum
  (e.g. `Ordinary` / `Meta`), so the handler knows which socket a stream
  arrived on.
- `fn start/stop(&mut self)` and
  `fn handle_stream(&mut self, listener: Self::Listener, stream: UnixStream)`.

Construction: `MultiListenerDaemon::new(listener_sockets:
impl IntoIterator<Item = ListenerSocket<Listener>>, runtime, request_error_log)`,
where each `ListenerSocket::new(tag, socket_path)` optionally
`.with_socket_mode(SocketMode)`. The bound daemon polls all listeners
non-blocking (`ListenerPollInterval`, default 10ms) and routes each accepted
stream to `handle_stream` tagged with its listener. The witness test
`multi_listener_daemon_routes_two_sockets_through_one_runtime_owner` proves two
sockets feed one runtime owner with per-socket response offsets; a second test
proves per-socket file modes. The component then tags each arrival by role into
its `SignalInput` union and routes through the same generated `NexusEngine::execute`
runner (intent `rcn3`/`latq`). Daemon configuration verbs travel the meta-signal
socket (intent `cgd8`).

## LANDED vs PROPOSED vs BLOCKED — the base today

| Capability | Status | Evidence |
|---|---|---|
| `.schema → src/schema/*.rs` emission via `GenerationDriver` | LANDED | `spirit/build.rs`; checked-in `src/schema/{signal,nexus,sema}.rs`; round-trip + freshness check in `schema_rust_next::build` |
| `asschema` removed (structural-macro-node codec is the path) | LANDED | empty grep in spirit + schema-rust-next + schema-next; `nota-next` `StructuralMacroNode` is the codec; commit `b875c62` "remove asschema emitter api" |
| Three engine traits emitted with default lifecycle hooks | LANDED | `schema-rust-next/src/lib.rs` 3724–3925; spirit impls in engine.rs / nexus.rs / store.rs |
| `on_start`/`on_stop` lifecycle + typed `ActorStart/StopFailure` | LANDED | emitted at lib.rs 3928–3967; `Engine::start/stop` wires them; test `engine_lifecycle_runs_generated_trait_hooks_without_actor_mailboxes` |
| `NexusEngine::execute` recursive runner loop (Runner::drive) | LANDED | emitted `execute` + `NexusRunnerAdapter` (lib.rs 3848–3132); `runner.rs` `Runner::drive`; tests `nexus_runner_loop_routes_...`, `sema_read_miss_completion_routes_through_runner_loop_...` |
| Continuation budget + `budget_exhausted_reply` | LANDED | `ContinuationLimit`/`Budget`/`Exhausted` in runner.rs; `Nexus::budget_exhausted_reply` |
| Effects (component-declared `run_effect`) | LANDED | nexus.schema `NexusEffectCommand`/`Result`; `Nexus::run_effect` (Stash, ClassifyState); witness `full_runtime_triad_records_then_observes_through_durable_sema_with_stash` |
| SEMA write/read + persistence across reopen | LANDED | `store.rs` over `sema_engine::Engine`; test `sema_store_persists_records_across_reopen_of_the_same_sema_file` (commit ledger resumes, content digest non-zero) |
| sema-engine is the exclusive DB boundary (no raw redb) | LANDED | empty grep `redb::` in spirit/src; no redb in Cargo.toml; honors correction `fosp` |
| `SingleListenerDaemon` runner | LANDED | triad-runtime daemon.rs; spirit daemon.rs wiring; tests `single_listener_daemon_binds_socket_and_serves_one_stream`, error-isolation test |
| `MultiListenerDaemon` / two-listener (ordinary + meta socket) | LANDED | triad-runtime HEAD `28d03c3`; `MultiListenerRuntime` trait + `MultiListenerDaemon::new`; 2 passing witness tests; intent `rcn3` correction |
| Length-prefixed rkyv frame transport | LANDED | `LengthPrefixedCodec`/`FrameBody` (frame.rs); spirit transport.rs |
| Typed trace (in-process recording + socket) | LANDED behind feature | triad-runtime trace.rs (`TraceLog`/`TraceClient`/`TraceSocketListener`); spirit `testing-trace` feature; instrumentation test |
| Single-argument NOTA/signal-file argument parsing | LANDED | triad-runtime argument.rs (`ComponentCommand`, `ComponentArgument`); spirit daemon + CLI bins |
| `triad_main!` macro that emits `main`/listener wiring | NOT EMITTED (hand-written) | empty grep `triad_main`/`macro_rules` everywhere; daemon shell is hand-written per component (spirit daemon.rs) |
| `meta-signal-*` rename of the policy contracts | PROPOSED / NOT LANDED | only `owner-signal-router`/`owner-signal-orchestrate` exist on disk; no `meta-signal-router`/`-orchestrate`; intent `r9qy` calls it "active work" across 13 repos but the rename has not been run |
| Single-writer SEMA *actor* (vs mutex-held Store) | PROPOSED | spirit ARCHITECTURE "Known limits": `Store` lives in the Nexus mutex, not a kameo single-writer actor; intent `e440` is the target shape |
| Durable mail ledger | NOT LANDED (by design, for now) | ARCHITECTURE "Known limits": mail ledger is in-memory observability; resets on restart; only SEMA records + commit ledger are durable |
| Schema diff / upgrade | PROPOSED | `UpgradeFrom`/`AcceptPrevious` traits emitted but nothing implements them; migration.rs exists in schema-rust-next |
| Schema-derived streaming (push/subscribe) | PROPOSED | intent `brgo`: full schema-derived streaming is a platform project across schema-next + schema-rust-next + triad-runtime + signal-frame; not landed |
| Shared `schema-core` for `DatabaseMarker` / mail nouns | PROPOSED | ARCHITECTURE "next slice"; `MessageSent`/`MessageProcessed` are emitter support-surface, plane.rs From-glue is hand-written |

Test green proxy: spirit binaries `spirit` + `spirit-daemon` were built today
(Jun 5 14:24) and `runtime_triad` test deps compiled; #[test] counts are spirit
73, triad-runtime 31, schema-rust-next 53. (I did not run the suites — READ-ONLY
discipline — so "green" is a build-artifact + recent-commit proxy, not a fresh
`cargo test` observation.)

## The known foundation blockers a port could hit — real status

### primary-vllc payload-less-variant dual-lowering — NOT GROUNDED in these repos

The frame and prior reports name a `primary-vllc` dual-lowering bug for
payload-less variants. **I found no evidence of it in the base repos:** no
`primary-vllc` / `vllc` / `lojix` / `token` checkout under
`/git/github.com/LiGoldragon/`, and empty grep for `vllc` / `dual-lower` /
`payload-less` / `VariantLayout` across spirit, triad-runtime, schema-rust-next,
schema-next. Commit `2437413` "bump to 0.1.13 for token lowering" + `453fc65`
"lower rust through schema object traits" in schema-rust-next suggest token/role
lowering work landed recently, but I cannot confirm or deny a payload-less
dual-lowering defect from source available here. **A port author must verify
this against the actual schema-next/schema-rust-next emission of the component's
own payload-less variants (e.g. router's adjudication outcomes, orchestrate's
role-state enums) before assuming it is unblocked.** Carried as an open
verification item, not a cleared blocker.

### sema-engine persistence / emit gaps — persistence LANDED; "express real storage identity" is the open surface

Persistence is real and proven: the `sema_store_persists_records_across_reopen`
test writes, drops the handle, reopens the same `.sema` path, and observes
records survive with the commit ledger resumed (next write is commit sequence 3,
not 1) and a non-zero content digest. The sema-engine identified-table API
(`register_identified_table`, `assert_identified`, `match_identified`,
`mutate_identified`, `retract_identified`, `current_commit_sequence`) is present
and used. No `todo!`/`unimplemented!` in sema-engine src. The OPEN surface
(intent `ox7e`, Principle): a port must not "merely port to a mismatched current
sema-engine API" — when a component's storage need doesn't map cleanly (router
delivery tables, orchestrate role registry), the right move is to **improve the
shared sema-engine surface** so generated SEMA expresses the real storage
identity, not to bend the component. That is design work each port may trigger,
not a hard blocker. There is no "SEMA emit" gap in the sense of the generator
failing to emit SEMA code — `SemaRuntime` emission works and is checked in.

### signal-frame Layer-1 — the streaming/frame substrate is PROPOSED at schema level

`signal-frame` is the connection-setup + async-correlation + handshake mechanism
(intent `3got`: the Communicate trait uses signal-frame for connection setup,
async unique IDs, and handshake; the reply carries a DatabaseMarker for local
state consistency). For the *base recipe today*, the daemon transport is
`triad-runtime`'s `LengthPrefixedCodec` directly, not signal-frame. Two open
threads: (a) `maeq` (Correction) — signal-frame itself should be schema, the
frame kernel is not exempt; (b) `brgo` — schema-derived streaming should reach
the existing-but-unused `StreamingFrameBody`/`ObservableSet` machinery in
signal-frame, plus a push action + subscriber registry in the triad-runtime
runner. Neither is landed. A port that needs push/subscribe (router delivery,
orchestrate status watch) hits this; a port that only needs request-reply does
not. Status: PROPOSED platform work, partially scaffolded.

### meta-signal rename — NOT LANDED; a port's contract repos still carry owner-signal

Verified on disk: `owner-signal-router` and `owner-signal-orchestrate` exist as
`.concept.schema` stubs; `meta-signal-router` / `meta-signal-orchestrate` do
NOT exist. Intent `r9qy` (Decision, High) frames the owner→meta rename as active
work across 13 repos, and `cgd8` puts configuration verbs on the meta-signal
contract — but the rename is a pending fleet operation, not done. **Any port
plan that says "the meta-signal contract repo" is describing a repo that must
first be created/renamed.** This is a real prerequisite gate for the
two-listener (ordinary + meta) wiring on message / router / orchestrate.

## What a port must NOT assume is free

1. The daemon `main` + listener wiring is hand-written every time — there is no
   `triad_main!`. Budget that as real (small) code per component.
2. The cross-plane `OriginRoute`/lifecycle-error `From` glue (`plane.rs`) is
   hand-written today; it is repetitive and a candidate for `schema-core`, but
   it does not yet emit.
3. The mail ledger is in-memory; a port needing durable delivery accounting
   (router) must add durable state via SEMA, not rely on the ledger.
4. `Store` is mutex-held, not a single-writer actor; a port with heavy
   concurrent writes inherits that contention until the actor shape (intent
   `e440`) lands.
5. The meta-signal contract repo must exist before the two-listener wiring; the
   rename is pending.
6. The payload-less dual-lowering concern must be checked against the
   component's own schema, not assumed cleared.
