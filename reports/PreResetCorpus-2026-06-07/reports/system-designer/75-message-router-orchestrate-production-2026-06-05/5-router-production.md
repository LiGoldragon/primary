# 5 — router production map: porting `router` onto the schema/triad-engine base

Per-component port map for the 75 session. Source-grounded against
`/git/github.com/LiGoldragon/router` (HEAD `570aaab6` "docs: add INTENT.md"),
`signal-router`, `owner-signal-router`, and the base references (`spirit` HEAD
`f7951b8`, `triad-runtime` HEAD `28d03c3`, `schema-rust-next`), all read
2026-06-05. Companion reports: `1-skills-production-rulebook.md` (rule numbers
R1-R37 referenced here), `2-intent-agglomeration.md` (intent anchors,
description-first), `3-triad-base-state.md` (the build recipe). READ-ONLY: no
edits, no commits on any repo.

The one-line finding: **router is the richest-state, richest-decision target of
the three and is entirely PRE-triad-engine.** It is a hand-written Kameo
`RouterRuntime` of six child actors over a direct `sema` (not `sema-engine`)
store; it has no `triad-runtime` / `schema-rust-next` dependency, no `build.rs`,
no three-plane schema, and no `SignalEngine`/`NexusEngine`/`SemaEngine` impl. Its
decision logic (channel authorization, one-shot retire, time-bound expiry,
delivery adjudication, parked-message retry) is exactly the internal-feature
catalog that intent `z6qu` says must become declared Nexus verbs. The port is a
near-rewrite of the runtime layer, but the domain model (channels, delivery,
adjudication, the SEMA tables) is mature and transfers almost verbatim.

## 1. Current architecture (source-grounded)

### 1.1 The crate + binary shape

`router/Cargo.toml`: one crate, `lib` (`src/lib.rs`) + one `[[bin]]`
`router-daemon` at `src/main.rs` (verified; `src/bin/` is empty). `src/main.rs`
branches: if argv[1] looks like a typed configuration source (starts with `(` or
ends `.nota`/`.rkyv`) it decodes a `RouterDaemonConfiguration` via `nota-config`
and runs `RouterDaemon::from_configuration(...)`; otherwise it runs
`RouterCommandLine::from_env()` — so the SAME binary is both daemon and CLI, and
the CLI path reads `from_env()` (an argv surface, not a single-NOTA-arg surface).

Dependencies (verified): `kameo` 0.20, `tokio`, `rkyv` 0.8, `thiserror`,
`nota-codec`, `nota-config`, and a wide signal-contract set — `signal-core`,
`signal-frame`, `signal-engine-management`, `signal-persona-origin`,
`signal-harness`, `signal-mind`, `signal-message`, `signal-router`,
`signal-persona`. **`sema` is depended on DIRECTLY** (`sema =
github:LiGoldragon/sema`) — NOT `sema-engine`. **No `triad-runtime`, no
`schema-rust-next`, no `sema-engine` anywhere** (verified empty grep across all
three repos' Cargo.toml). There is **no `build.rs`** in router or signal-router.

### 1.2 The daemon shape — hand-written Kameo, one socket + one supervision socket

`RouterDaemon` (`src/router.rs:74`) holds a socket path, optional `RouterTables`,
a `RouterIngressContext`, optional `SocketMode`, optional `RouterBootstrap`,
optional `SupervisionListener`. `RouterDaemon::run` (`src/router.rs:144`):
binds a raw `std::os::unix::net::UnixListener`, spawns the supervision listener on
its own thread, makes a `tokio::runtime::Runtime`, blocks on
`RouterRuntime::start_with_optional_tables`, applies bootstrap, then loops
`listener.incoming()` blocking, calling `handle_connection` per stream.

`handle_connection` (`src/router.rs:176`) reads one `RouterDaemonInput` and
routes by frame type: `SignalMessage(SignalMessageInput)` →
`router.ask(ApplySignalMessage{...})`; `RouterObservation(SignalRouterRequest)` →
`router.ask(ApplyRouterObservation{...})`. So the daemon already does
**frame-union triage** by hand (try signal-message frame, fall back to
router-observation frame) — `RouterConnection::read_input` at `src/router.rs:239`.

There are effectively **two listeners today**: the main router socket (carries
ordinary message ingress + observation traffic) and a **separate supervision
socket** on its own thread (`SupervisionListener::spawn` →
`std::thread::spawn(move || server.run())`, `src/supervision.rs:70-84`). But this
is the OLD shape: a raw `UnixListener` + a `tokio::runtime::Runtime` per thread,
not `triad-runtime`'s `MultiListenerDaemon`. There is **no owner/meta policy
socket wired into the daemon at all** — the owner channel-authority orders
(`owner-signal-router`'s `Grant`/`Extend`/`Revoke`/`Deny`) are NOT served by a
listener; they enter only as in-process `RouterInput::ApplyMindChannelGrant` /
`ApplyMindAdjudicationDeny` variants (`src/router.rs:1039-1066`) with no socket
behind them. The inbound-from-mind path is type-modeled but not socketed.

### 1.3 The runtime — six Kameo child actors, in-memory + sema-backed

`RouterRuntime` (`src/router.rs:652`) is a Kameo actor whose `on_start` spawns
six children (`start_children`, `src/router.rs:695`): `HarnessRegistry`,
`HarnessDelivery` (spawned in its own thread), `ChannelAuthority`,
`MindAdjudicationOutbox`, `RouterRoot`, `RouterObservationPlane`. `RouterRoot`
(`src/router.rs:926`) is the decision core holding `pending:
Vec<PendingRouterMessage>` (the in-memory parked-message queue), the child refs, a
`RouterTrace`, and sequence counters. This is a clean actor-system design — but it
is the wrong substrate: six bespoke actors plus a hand-rolled apply-dispatch,
where the triad base wants three engine traits + the generated runner.

The decision logic that must become the Nexus catalog lives across:

- `ChannelAuthority` (`src/channel.rs`): `authorize` (mint channel + persist),
  `retract`, `check` (the authorization decision — looks up the `ChannelTriple`,
  returns `Authorized{channel}` or `NeedsAdjudication(request)`), `mark_used`,
  `install_structural_channels`, `observe_time`, `adjudication_request`
  (dedup by triple). `ChannelRecord::is_active_at` (`src/channel.rs:284`) holds
  the **one-shot** (`use_count == 0`), **time-bound expiry** (`now < expires_at`),
  and **retracted** (`status != Active`) authorization rules.
- `RouterRoot::retry_pending` (`src/router.rs:1195`): the parked-message engine —
  for each pending message, resolve delivery target, `CheckChannel`, on
  `NeedsAdjudication` record a `RecordMindAdjudication` and re-park; on
  `Authorized` mint a delivery sequence, persist a delivery attempt, ask
  `DeliverHarness`, persist the delivery result, and on success `UseChannel` +
  `MarkHarnessDelivered` + trace. This is the heart of the engine.
- `RouterRoot::reject_pending_adjudication` (`src/router.rs:1330`): drop parked
  messages whose id matches a mind `Deny`.
- `RouterRoot::apply` (`src/router.rs:961`): the RouterInput dispatch (8 variants:
  RegisterActor, RouteMessage, Status, GrantChannel, RetractChannel,
  InstallStructuralChannels, ApplyMindChannelGrant, ApplyMindAdjudicationDeny).
- `RouterRoot::apply_stamped_message_submission` (`src/router.rs:1086`): the
  message-ingress path — mint a signal slot, build the `Message`, persist, park,
  retry. (`MessageSubmission` and non-`Send` kinds reply
  `MessageRequestUnimplemented`.)
- `RouterObservationPlane` (`src/observation.rs`): answers `Summary`,
  `MessageTrace`, `ChannelState` observation queries from facts + the store.

### 1.4 The SEMA layer — direct `sema`, seven tables

`RouterTables` (`src/tables.rs`) opens one `Sema` over a single redb file
(`router.redb` per INTENT.md) via `Sema::open_with_schema`, and declares **seven
tables**: `channels`, `channels_by_triple` (a triple→channel index),
`adjudication_pending`, `messages`, `delivery_attempts`, `delivery_results`,
`meta`. Stored types are hand-rolled rkyv structs (`StoredChannelRecord`,
`StoredAdjudicationRequest`, `StoredMessageRecord`, `StoredDeliveryAttempt`,
`StoredDeliveryResult`, `StoredChannelIndex`). **This is raw `sema` table access,
not `sema-engine`'s identified-table API** (R18 wants `sema-engine` as the
default; spirit's `Store` uses `register_identified_table` / `assert_identified`
/ `match_identified` etc.). The acceptance/commit ordering invariant
(INTENT.md: "Message acceptance commits before delivery attempt. Delivery results
update state before post-delivery subscription events") is enforced by hand-call
ordering in `retry_pending`, not by SEMA semantics.

### 1.5 The contract repos — wire types present, but with violations

`signal-router/src/lib.rs` is a real contract (not a stub): it carries
`Actor`/`EndpointTransport`/`EndpointKind`, the `RouterBootstrapOperation`
family, the observation query/reply records, and a `signal_channel!` block
`channel Router` with request `RouterRequest` (Summary / MessageTrace /
ChannelState) + reply `RouterReply`. It ALSO carries `RouterDaemonConfiguration`
(the typed daemon startup config: router socket, supervision socket, store path,
optional bootstrap path, owner identity). **R24 VIOLATION confirmed**: the
request arms use the Sema classification word `Match` on the public wire —
`Match Summary(RouterSummaryQuery)`, `Match MessageTrace(...)`, `Match
ChannelState(...)` (`signal-router/src/lib.rs:290-292`). The router daemon test
also constructs `SignalVerb::Assert` (`src/router.rs:2504`) and the observation
test `SignalVerb::Match` (`tests/observation_truth.rs:185`). These are exactly the
`signal-router` hits the skill names (R24, intent `7l7l`).

`owner-signal-router/src/lib.rs` is the policy contract and is CLEANER: a
`signal_channel!` `channel OwnerRouter` with operations `Grant(ChannelGrant)`,
`Extend(ChannelExtension)`, `Revoke(ChannelRevocation)`, `Deny(AdjudicationDenial)`
— domain verbs, no Sema vocabulary — plus a rich reply enum
(`ChannelGranted`/`ChannelExtended`/`ChannelRevoked`/`AdjudicationDenied`/
`ChannelOrderRejected`/`RequestUnimplemented`) with typed rejection reasons
(`ChannelOrderRejectionReason`). It carries a fuller channel model than the daemon
implements (`ChannelDuration::{OneShot,Permanent,TimeBound}`, a 12-variant
`ChannelMessageKind`, `ChannelEndpoint::{Internal,External}`). **R14: this repo is
named `owner-signal-router` and must rename to `meta-signal-router`** (intent
`r9qy`, the rename is "active work" naming this exact repo). Both contract repos
emit via hand-`signal_channel!` macros today, **not** via `schema-rust-next`
`WireContract` emission from a `.schema` file.

The legacy `*.concept.schema` files (`router/schema/router.concept.schema`,
`signal-router/schema/signal-router.concept.schema`,
`owner-signal-router/schema/owner-signal-router.concept.schema`) are stale
concept-form stubs (flat `[(Summary [Route]) ...]` operation lists with a single
trailing namespace, `(Status Concept)`) and are NOT the source of the actual
Rust contract types — the real types are hand-written in `src/lib.rs`. So router
carries BOTH a dead concept schema AND a hand-written contract.

### 1.6 Build / test status today

`router-daemon` build artifacts under `target/debug/` are dated Jun 5 14:49-14:51,
so **the crate builds today** (build-artifact proxy; I did not run `cargo build`
under READ-ONLY discipline). Test surface is substantial: `tests/smoke.rs` (296
lines, ~9 `#[test]` incl. `constraint_router_daemon_applies_spawn_envelope_socket_mode`,
`constraint_router_daemon_answers_component_supervision_relation`),
`tests/actor_runtime_truth.rs` (1773 lines), `tests/observation_truth.rs` (606
lines), `tests/no_shared_locks_truth.rs` (73 lines — an R34 witness against shared
locks). These are Kameo-actor-shape witnesses; **none of them drive
`SignalEngine`/`NexusEngine`/`SemaEngine`** because those traits don't exist here
yet. Persona names the pair: `persona/src/engine.rs:364` defines
`MESSAGE_ROUTER_COMPONENTS: [EngineComponent; 2]` and
`operational_delivery_components()` returns 6 — but neither message nor router
consumes `triad-runtime`, so the delivery round-trip is asserted by name only
(report 74 anchor), not exercised through the engine traits.

## 2. The gap to the base (vs the spirit-pilot recipe)

Mapped to the report-1 checklist; "MISSING" = not in source, "VIOLATION" = present
but wrong-shape.

- R1 three-plane schema: **MISSING.** No `schema/{signal,nexus,sema}.schema`, no
  `build.rs`, no `src/schema/*.rs`. Only the dead `router.concept.schema`.
- R2/R6 engine-trait split: **MISSING.** No `SignalEngine`/`NexusEngine`/
  `SemaEngine` impl; the planes are mixed across six Kameo actors. `ChannelAuthority`
  mixes decision (check) + storage (insert_channel) — a 3d5z separation breach.
- R5 Nexus feature catalog: **MISSING — the biggest gap.** Every decision feature
  (authorize, check-authorization, one-shot retire, time-bound expiry, retract,
  adjudication-request dedup, deliver, park/retry, deny-reject, use-channel) is
  inline hand-written `match`/`if` logic invisible to any schema. None is a declared
  Nexus verb+object.
- R9 NexusAction mechanism: **MISSING.** `retry_pending` does direct async
  `actor.ask(...)` calls to children; it is not a `decide → NexusAction → runner
  re-enters` loop. The Signal↔SEMA translation is hand-threaded.
- R12/R13 two authority surfaces via `MultiListenerDaemon`: **MISSING/VIOLATION.**
  router has a main socket + a supervision socket (two listeners) but NO meta
  (owner) policy socket, and both use the OLD raw-UnixListener+per-thread-tokio
  shape, not `triad-runtime::MultiListenerDaemon`. The owner contract exists in
  types but is not socketed.
- R14 meta-signal rename: **MISSING.** `owner-signal-router` exists;
  `meta-signal-router` does not.
- R18 `sema-engine`: **VIOLATION.** router uses raw `sema` table access, not
  `sema-engine`'s identified-table API.
- R19 single-argument NOTA: **PARTIAL VIOLATION.** The daemon path is single-arg
  (typed `RouterDaemonConfiguration` via `nota-config`), but the SAME binary's CLI
  path uses `from_env()` (an argv surface), and `main.rs` sniffs argv shape to
  pick — not the clean one-NOTA-arg rule. The CLI must become a separate `router`
  binary that is the daemon's first client (R21), not a dual-mode binary.
- R24 no Sema vocab on wire: **VIOLATION (named).** `signal-router` uses `Match` on
  the public request roots.
- R7 lifecycle hooks: **PARTIAL.** Kameo `on_start`/`on_stop` exist on the actors,
  but they are Kameo's, not the engine-trait `on_start`/`on_stop` with typed
  `ActorStartFailure`/`ActorStopFailure` (R7). The supervision surface
  (`SupervisionProfile::router()` answering Announce/Readiness/Health/Stop in
  `src/supervision.rs`) is GOOD and maps onto czw0; it is ahead of the base on this
  one axis.
- R25/bexd typed feedback: **MOSTLY MET.** Replies are typed enums
  (`RouterOutput`, `RouterReply`, `OwnerRouterReply` with typed rejection reasons).
  Some `Error` variants still carry `String` payloads (`ActorCall(String)`,
  `UnexpectedSignalFrame{got:String}`) — internal, not wire, but worth tightening.
- R31 redb+rkyv: **MET** for storage/wire; raw-redb is not used (it goes through
  `sema`). But `harness_delivery.rs` writes a hand-rolled `b"P"`+len+NOTA frame to
  a terminal socket (`deliver_to_terminal_socket`, `src/harness_delivery.rs:49`)
  and `message.to_nota()` on the inter-component wire — an R20 concern (NOTA on a
  live inter-component socket) for the PtySocket path; the HarnessSocket path
  correctly uses `signal-harness` length-prefixed frames.
- `7x50` bootstrap-as-binary: **VIOLATION.** `RouterBootstrap::operations` reads
  NOTA at runtime (`from_nota_lines`, `signal-router/src/lib.rs:169`) and applies it
  at startup — intent `7x50` requires a pre-encoded binary artifact, no NOTA parse
  in the live daemon.

What transfers cleanly: the domain model (channel/triple/lifetime/status, the
delivery state machine, the seven SEMA tables, the adjudication outbox), the typed
reply discipline, the supervision profile, and the inbound-from-mind authority
principle (INTENT.md). The port keeps the WHAT and rebuilds the HOW.

## 3. The port plan — ordered concrete steps

The branch `triad-engine-port` (same name across `router`, `signal-router`,
`meta-signal-router`) in `~/wt/github.com/LiGoldragon/<repo>/triad-engine-port/`
per C1-C3. Designer works on `next`/feature branch; operator integrates to main.
Per-repo `INTENT.md`/`ARCHITECTURE.md` update on the SAME branch (C4, §7).

### Step A — Author the two wire contracts (contract repos)

A1. **Rename `owner-signal-router` → `meta-signal-router`** (R14, `r9qy`). New repo
identity, crate name `meta-signal-router`, `channel MetaRouter` (or keep
`OwnerRouter` type names but rename the repo + crate). This is a fleet rename slice
shared with orchestrate; it is a PREREQUISITE for the two-listener wiring and is
NOT yet done.

A2. Convert both contracts from hand-`signal_channel!` to **`schema/signal.schema`
emitted via `schema-rust-next` `WireContract`** (the base recipe — contract repos
emit wire types + NOTA codec, NO engine traits, R4). Drop the dead
`*.concept.schema`. Author:
  - `signal-router/schema/signal.schema` — the ordinary wire contract. Operation
    roots are **domain verbs, NOT `Match`** (fixes R24): an `Input` root enum with
    `≥2` variants such as `[(Submit StampedMessageSubmission) (Observe
    RouterObservationQuery) (Query InboxQuery) (Register RegisterActor)]` and a
    `RouterObservationQuery` sub-enum `[(Summary ...) (MessageTrace ...)
    (ChannelState ...)]`. The reply root carries verb-past-tense variants
    (`Submitted`/`Observed`/`Registered`/...) + typed `*Rejected` (R25). Keep
    `RouterDeliveryStatus`/`RouterChannelStatus` closed enums (already good — no
    sentinel `Unknown`).
  - `meta-signal-router/schema/signal.schema` — the owner policy wire contract.
    Roots stay the existing domain verbs `[(Grant ChannelGrant) (Extend
    ChannelExtension) (Revoke ChannelRevocation) (Deny AdjudicationDenial)]` (these
    are already clean). Reply enum keeps the typed `ChannelOrderRejected` +
    `ChannelOrderRejectionReason`.
  - `RouterDaemonConfiguration` belongs in the daemon config surface; decide whether
    it stays in the ordinary contract or moves to a daemon-local config schema
    (it is startup config, not wire vocabulary — leaning daemon-local, see §6).

### Step B — Author the three in-daemon plane schemas (`router/schema/`)

Per `lc2r` (VeryHigh): the three plane schemas live INSIDE the daemon crate and
import the wire contract IO; they are NOT the all-in-one spirit layout.

B1. `router/schema/signal.schema` — **emits `SignalEngine`** (the daemon-local
signal plane, R4, distinct from the `signal-router` wire contract). Imports
`signal-router:signal:Input`/`Output` and `meta-signal-router:signal:Input`/`Output`.
Declares the union the daemon triages: a `SignalInput` tagging each arrival by
listener (`Ordinary(signal_router::Input)` / `Meta(meta_signal_router::Input)`) so
the `MultiListenerDaemon::Listener` tag routes into one runtime (R13 pattern).
Triage = admission + identity-stamping (mint origin route + message identifier per
`h4mn`/`z821`) + validation only — no heavy logic (`u7fj`).

B2. `router/schema/nexus.schema` — **the load-bearing one: the engine's visible
feature catalog (R5, `z6qu`).** Every router decision becomes a declared verb+object.
`NexusWork` (facts the runner re-enters): `[(SignalArrived ...) (SemaWriteCompleted
...) (SemaReadCompleted ...) (EffectCompleted ...)]`. `NexusAction` (the 5-variant
set, R9): `[(CommandSemaWrite ...) (CommandSemaRead ...) (ReplyToSignal ...)
(CommandEffect ...) (Continue ...)]`. The **router feature verbs+objects** to
declare (each is currently inline match logic, see §1.3):

  - `AuthorizeChannel(ChannelGrant)` — mint + persist a channel (from
    `ChannelAuthority::authorize`).
  - `RetractChannel(ChannelIdentifier)` — set status Retracted.
  - `ExtendChannel(ChannelExtension)` — extend a time-bound channel (from the
    owner contract's `Extend`, not yet implemented in the daemon — gap to fill).
  - `CheckChannelAuthorization(MessageRouteKey)` → an outcome object
    `ChannelAuthorizationOutcome [(Authorized ChannelIdentifier) (NeedsAdjudication
    AdjudicationRequest)]` — the central authorization decision (from
    `ChannelAuthority::check` + `is_active_at`). The one-shot / time-bound / retracted
    rules become declared predicates on the channel object, not buried in
    `is_active_at`.
  - `RetireOneShotChannel(ChannelIdentifier)` — the one-shot retire-after-one-use
    rule made an explicit verb (today implicit in `use_count == 0` +
    `mark_used`/`UseChannel`).
  - `RecordAdjudicationRequest(AdjudicationRequest)` — dedup-by-triple, persist,
    enqueue the mind outbox entry (from `adjudication_request` +
    `MindAdjudicationOutbox::record`).
  - `ParkMessage(PendingMessage)` / `RetryParkedMessages(...)` — the parked-message
    engine (`retry_pending`): the deliver-or-defer-or-fail decision per parked
    message becomes a Nexus continuation (`Continue(NexusWork)`), each delivery
    attempt a `CommandEffect(DeliverHarness)`, each persist a `CommandSemaWrite`.
  - `RejectAdjudicationDenied(AdjudicationDenial)` — drop parked messages on a mind
    `Deny` (from `reject_pending_adjudication`).
  - `InstallStructuralChannels(EngineStructuralChannels)` — bootstrap channel stack.
  - `ResolveDeliveryTarget(ActorIdentifier)` — registry lookup (from
    `HarnessRegistry::delivery_target`).

  Plus the **effect catalog** `NexusEffectCommand`/`NexusEffectResult` (router's
  effects are real I/O, not just `Stash`): `DeliverToHarness(DeliverHarness)` →
  `HarnessDeliveryCompleted{delivered: bool}` (the harness round-trip in
  `harness_delivery.rs`), and possibly `DeliverToTerminalSocket(...)` →
  `TerminalAccepted{...}`. Harness delivery is an external side-effect, so it is a
  declared effect the runner dispatches via `run_effect` (matching spirit's
  effect mechanism), re-entered as `NexusWork::EffectCompleted`.

B3. `router/schema/sema.schema` — **emits `SemaEngine`** over the seven tables.
`WriteInput [(RecordMessage ...) (RecordChannel ...) (RecordAdjudication ...)
(RecordDeliveryAttempt ...) (RecordDeliveryResult ...) (MarkChannelUsed ...)
(RetractChannel ...) (DropParkedMessage ...)]`; `ReadInput [(ObserveSummary ...)
(LookupMessageTrace MessageSlot) (LookupChannelState ChannelIdentifier)
(MatchChannel MessageRouteKey) (CountPending ...)]`; matching `WriteOutput`/
`ReadOutput`. (Sema-classification words ARE allowed HERE — they are the
daemon-internal SEMA plane, forbidden only on the public wire, R24.) The commit
ordering invariant (acceptance commits before delivery attempt; results commit
before subscription events) is expressed as the WriteInput sequencing the Nexus
issues, not as ad-hoc call ordering.

### Step C — Wire `build.rs` + emit (the recipe from report 3 §1)

`router/build.rs` declaring `GenerationPlan::new(crate_root, "router", version)`
`.with_module(ModuleEmission::signal_runtime_module("signal"))`
`.with_module(ModuleEmission::nexus_runtime())`
`.with_module(ModuleEmission::sema_runtime())`, then `GenerationDriver` +
`write_or_check("ROUTER_UPDATE_SCHEMA_ARTIFACTS")`. Contract repos get their own
`build.rs` with `ModuleEmission` at `WireContract` target. Add `triad-runtime`,
`schema-rust-next`, and `sema-engine` to `router/Cargo.toml`; drop the direct
`sema` dep.

### Step D — Hand-write the three engine impls + Store (the only hand-code)

Per `rpr5` the author writes exactly five surfaces: SignalEngine, NexusEngine,
SemaEngine, the effect handler, the budget-exhausted reply.

D1. `router/src/engine.rs` — `impl SignalEngine for <RouterSignalActor>`
(`triage_inner(Signal<Input>) -> Nexus<Work>`, `reply_inner(Nexus<Action>) ->
Signal<Output>`, typed `on_start`/`on_stop`). The data-bearing noun owns the
ingress context + the listener-tag routing (R8). Triage maps the listener tag
(Ordinary vs Meta) into the work union and stamps origin/message identity.

D2. `router/src/nexus.rs` — `impl NexusEngine for <RouterNexus>` (the data-bearing
decision core holding the in-flight state, R8). `decide(&mut self, Nexus<Work>) ->
Nexus<Action>` delegates to per-fact `step_*` deciders mirroring spirit's
`decide_signal_arrival`/`decide_sema_write_completion`/etc. The parked-message
retry becomes a `Continue` loop bounded by the continuation budget. `run_effect`
runs harness delivery. `apply_sema_write`/`observe_sema_read` forward to the
`Store`. `budget_exhausted_reply` returns a typed `Output::*Rejected`.

D3. `router/src/store.rs` — `impl SemaEngine for Store` over **`sema-engine`'s
identified-table API** (R18; the spirit `register_identified_table` /
`assert_identified` / `match_identified` / `mutate_identified` /
`retract_identified` pattern). The seven tables become identified tables; the
hand-rolled `Stored*` rkyv structs become the emitted SEMA record types. If a
table doesn't map cleanly (the `channels_by_triple` index, the delivery
attempt/result append log), the right move per `ox7e` is to IMPROVE sema-engine's
surface, not bend router.

D4. `router/src/plane.rs` — the `From` projection glue across per-plane
`OriginRoute`/`ActorStartFailure`/`ActorStopFailure` (hand-written today in
spirit; report 3 §"what a port must not assume is free" item 2).

### Step E — Daemon shell via `MultiListenerDaemon` (two sockets) + CLI

E1. `router/src/daemon.rs` implementing `triad_runtime::MultiListenerRuntime` with
`type Listener` = an `{Ordinary, Meta}` (and likely `Supervision`) tag enum,
`handle_stream(listener, UnixStream)` routing each socket's frame into the
generated `NexusEngine::execute` runner. Construction:
`MultiListenerDaemon::new([ListenerSocket::new(Ordinary, router_socket),
ListenerSocket::new(Meta, meta_socket)], runtime, RequestErrorLog::new("router-daemon"))`,
with per-socket `SocketMode` (the ordinary socket peer-readable, the meta socket
owner-only — the permission-separation witness). **This is the first real
two-socket triad-engine daemon** — `spirit` is single-listener; `MultiListenerDaemon`
is committed (R13) but unexercised by a reference daemon, so router is establishing
the pattern. The supervision socket can become a third listener tag (folding
`src/supervision.rs` into the same runtime) OR stay a side concern; decide in §6.

E2. `router/src/bin/router-daemon.rs` — 9-line `DaemonCommand::from_environment().run()`,
taking exactly one signal-encoded `Configuration` file path (R19).

E3. `router/src/bin/router.rs` — the CLI, a SEPARATE binary that is the daemon's
first client (R21): one NOTA/file arg, parse into the wire `Input`, exchange over
the router socket, print the `Output`. **Drop the dual-mode `main.rs`** that
sniffs argv to pick daemon-vs-CLI. Add `(Help Main)` / `(Help (Verb ...))` (R22).

### Step F — Bootstrap policy as pre-encoded binary (`7x50`)

Replace `RouterBootstrap::from_nota_lines` (runtime NOTA parse) with the
bootstrap-once pattern (R16/`7x50`): a pre-encoded rkyv `bootstrap-policy` artifact
consumed exactly once on first start when the policy tables are empty, recorded in
a one-shot `bootstrap-complete` meta entry, never re-read. The structural channel
stack (`EngineStructuralChannels::first_stack`, `src/channel.rs:306`) is the
policy seed. Thereafter channel policy changes enter ONLY via the meta-signal
socket. **Caveat (R17): `bootstrap-policy.nota` is not present in the spirit
reference — router is establishing this pattern, not following a worked example.**

## 4. Witness tests (specialized from the component-triad witness table)

Layer-2 runtime + Layer-1 static + Layer-3 behavioral, per R35/R36. Positive proof
must execute the real boundary — a grep is only a negative guard.

Schema-chain (R36, the strongest):
- `router-route-message-drives-signal-nexus-sema-chain` — a `Submit
  StampedMessageSubmission` flows Signal→Nexus→SEMA→Nexus→Signal through the real
  engine traits, asserted via testing-trace records (admission, decide,
  sema-write, effect, reply). Removal of the engine-trait loop loses the trace.
- `router-authorization-miss-parks-and-emits-adjudication` — a message with no
  active channel parks, records an adjudication request (effect/sema), and the
  reply reflects deferred; trace shows `NeedsAdjudication`.
- `router-channel-grant-then-retry-delivers-parked` — a meta `Grant` followed by a
  retry delivers a previously-parked message (the `ApplyMindChannelGrant +
  retry_pending` behavior, now Nexus continuations).

Authorization rules (behavioral, R35):
- `router-one-shot-channel-authorizes-exactly-once-then-retires` — second message
  on a one-shot channel needs adjudication (the `is_active_at` one-shot rule as a
  Nexus verb).
- `router-time-bound-channel-expires-after-deadline` — message after `expires_at`
  needs adjudication.
- `router-retracted-channel-cannot-authorize` — message on a retracted channel
  needs adjudication.
- `router-adjudication-deny-drops-parked-message` — a meta `Deny` removes the
  parked message (the `reject_pending_adjudication` behavior).

Two-authority / socket (R12, R13):
- `router-meta-socket-rejects-ordinary-frame` and
  `router-ordinary-socket-rejects-meta-frame` (permission-separation witnesses).
- `router-meta-socket-mode-matches-spawn-envelope` (the existing
  `constraint_router_daemon_applies_spawn_envelope_socket_mode` smoke test
  generalized to the meta socket).
- `router-multi-listener-routes-two-sockets-through-one-runtime` (mirrors the
  triad-runtime `multi_listener_daemon_routes_two_sockets_through_one_runtime_owner`
  witness, specialized).

Wire discipline (R19, R20, R21, R24):
- `router-daemon-rejects-non-signal-traffic-on-its-socket`.
- `router-cli-accepts-one-argument-and-prints-one-nota-reply` /
  `router-cli-cannot-open-any-database-or-peer-socket`.
- `router-binary-rejects-flag-style-arguments`.
- `signal-router-contract-roots-carry-no-sema-classification-word` (a STATIC
  negative guard that `Match`/`Assert`/`Mutate`/`Retract`/`Subscribe`/`Validate`
  do not appear as request-root tags — the R24 fix witness).

Durable-state (R31, the commit-ordering invariant):
- `router-message-acceptance-commits-before-delivery-attempt` and
  `router-delivery-result-commits-before-subscription-event` (the INTENT.md
  ordering invariants made into SEMA-sequence witnesses).
- `router-sema-state-persists-across-reopen` (mirrors spirit's
  `sema_store_persists_records_across_reopen`).

Push-not-pull (R37): `router-delivery-emits-deltas-without-polling` — the
observation/delivery deltas are pushed, not produced by a `sleep`/`interval` loop
(router has no polling today; this guards the port from introducing one).

Supervision (czw0): `router-on-start-failure-surfaces-typed-actor-start-failure`
(a port-bound / database-missing start failure surfaces the typed
`ActorStartFailure` persona supervision reads) — and keep the existing
`constraint_router_daemon_answers_component_supervision_relation` smoke test.

## 5. Blockers — real foundation dependencies (landed-vs-proposed honest)

- **`meta-signal-router` does not exist (must be created/renamed first).**
  `owner-signal-router` is on disk; `meta-signal-router` is not. The two-listener
  wiring (Step E) depends on the meta wire contract existing. The rename is a
  pending fleet operation (intent `r9qy` calls it active across 13 repos) — NOT
  done. PREREQUISITE GATE, shared with orchestrate.
- **No worked two-socket triad-engine daemon exists yet (R13).** `MultiListenerDaemon`
  is committed in `triad-runtime` (HEAD `28d03c3`, 2 passing witness tests) but the
  canonical `spirit` daemon is single-listener only. Router's Step E is the FIRST
  real ordinary+meta triad-engine daemon — establishing the pattern, not copying it.
  Real (small) risk the `MultiListenerRuntime` shape needs adjustment under a real
  two-contract load.
- **`triad_main!` macro does not exist (R11).** The daemon `main` + listener wiring
  is hand-written every port (verified empty grep). Budget the daemon shell as real
  code.
- **`sema-engine` surface may not express router's storage identity cleanly
  (`ox7e`).** Router has a triple-index table and append-log delivery
  attempt/result tables; spirit's `Store` registers a SINGLE identified table. The
  port may need to improve the shared `sema-engine` surface (multiple identified
  tables, an append/sequence table type) — design work, not a hard blocker, but it
  is NOT a free port-to-existing-API.
- **Payload-less dual-lowering must be checked against router's own schema (report
  3, NOT cleared).** Router has payload-less variants (`ChannelStatus::{Active,
  Retracted}`, `ChannelKind::DirectMessage`, `RouterDeliveryStatus`/`RouterChannelStatus`
  enums, `ChannelDuration::{OneShot,Permanent}`). The `primary-vllc` dual-lowering
  concern named in the frame could NOT be confirmed or denied from the base repos
  (report 3 §"primary-vllc — NOT GROUNDED"); a port author MUST verify
  schema-rust-next emits router's payload-less variants correctly before assuming
  this is unblocked. OPEN VERIFICATION ITEM.
- **`bootstrap-policy.nota` pattern is invariant-on-paper (R17).** Not present in
  the spirit reference; router's Step F establishes it.
- **`sema-upgrade` gates DEPLOY-and-iterate, not compile (`veqq`).** Router is
  stateful, so once deployed against a `router.sema`/`router.redb`, the next schema
  edit breaks restart unless `sema-upgrade` covers it or the schema is frozen. This
  gates the running-system target (`mazv`), not getting router onto the base.
- **Push/subscribe substrate is PROPOSED (`brgo`).** If router's delivery
  observation deltas need true schema-derived streaming (vs request-reply), that
  substrate is not landed. Router's current observation is request-reply, so this
  is a soft dependency only if the port adds subscribe.

## 6. Open decisions for the psyche

1. **Does the supervision socket become a third `MultiListenerDaemon` listener, or
   stay a side thread?** Router today runs supervision on its own thread with its
   own contract (`signal-engine-management`). The cleanest triad shape folds it
   into the multi-listener runtime as a third tag; but supervision is a
   cross-component protocol (`signal-engine-management`), arguably orthogonal to the
   router triad. Two reasonable shapes; the psyche should pick.
2. **Where does `RouterDaemonConfiguration` live — the ordinary wire contract, or a
   daemon-local config schema?** It is startup config (sockets, store path, owner
   identity, bootstrap path), not wire vocabulary. `yjik`/`l6zw` say the wire
   contract carries ONLY Signal IO. Leaning daemon-local, but it currently sits in
   `signal-router/src/lib.rs`.
3. **Does the agent abstraction land before or after this port (`w4jp`/`gdbf`)?**
   Intent says router should talk to a new `agent` component (backends
   persona-claude/-codex/...), not the harness directly. Router's delivery target
   (`harness_delivery.rs` → `signal-harness`) is exactly what that abstraction
   reshapes. Port router-on-the-base-as-is then re-target, or wait for `agent`? No
   record sequences these — this is the #3 open question from report 2 §E,
   specialized to router.
4. **The origin-route carrying shape (`b559`, Medium, psyche-gated).** Router
   threads correlation through three planes (`z821`); the concrete encoding
   (leading tuple element vs named struct field) is unsettled. Router's
   `ExchangeIdentifier` + per-message identifier (`h4mn`) needs a decided shape.
5. **Does router keep the in-process inbound-from-mind path, or does ALL channel
   authority now arrive over the meta socket?** Today `ApplyMindChannelGrant` /
   `ApplyMindAdjudicationDeny` are in-process RouterInput variants with no socket.
   The triad shape puts owner authority on the meta socket. Confirm mind→router
   authority flows over `meta-signal-router` (the `owner-signal-router` doc says
   "Mind-level decisions reach Router through Orchestrate, not by calling this
   contract directly" — so the caller is orchestrate, on the meta socket).
6. **Channel model reconciliation: the daemon implements a thinner channel model
   than the owner contract.** `owner-signal-router` carries
   `ChannelDuration::{OneShot,Permanent,TimeBound}`, a 12-variant
   `ChannelMessageKind`, `ChannelEndpoint::{Internal,External}`; the daemon's
   `ChannelLifetime` is `{Persistent,OneShot,ExpiresAt}` and `ChannelKind` is just
   `DirectMessage`. The port must reconcile these into one schema-emitted model —
   which is canonical?

## 7. What lands in router's INTENT.md / ARCHITECTURE.md on the port branch (C4)

On the `triad-engine-port` branch, alongside the code:

- `router/INTENT.md` — add the triad-shape statement: router is a triad component
  (daemon + `signal-router` ordinary contract + `meta-signal-router` meta contract);
  the three planes carry channel authority (Nexus decision), delivery state (SEMA),
  and message ingress/observation (Signal); owner channel authority arrives over
  the meta socket from orchestrate, not in-process. State the bootstrap-once
  channel-policy seed. Reconcile the channel model (open decision 6).
- `router/ARCHITECTURE.md` (currently 32KB, describes the Kameo `RouterRuntime`) —
  rewrite the runtime section to the engine-trait/runner shape: the three engine
  impls, the Nexus feature catalog (list the declared verbs from §3 B2), the SEMA
  table set, the `MultiListenerDaemon` two-socket wiring, the typed
  `ActorStartFailure` supervision surface. Record the known limits the port
  inherits from the base (in-memory mail ledger, mutex-held Store vs single-writer
  actor `e440`, `sema-upgrade` not yet covering router `veqq`).
- `signal-router/INTENT.md` + `ARCHITECTURE.md` — record the move from
  hand-`signal_channel!` to schema-emitted `WireContract`, and the R24 fix
  (domain-verb roots, no `Match`).
- `meta-signal-router/INTENT.md` + `ARCHITECTURE.md` — the renamed-from-owner repo;
  record the rename provenance (`r9qy`) and the owner-only policy surface.

## Sources (verified 2026-06-05, READ-ONLY)

`router/{INTENT.md,Cargo.toml,src/{main.rs,lib.rs,router.rs,channel.rs,
adjudication.rs,delivery.rs,harness_delivery.rs,harness_registry.rs,observation.rs,
supervision.rs,tables.rs,error.rs},schema/router.concept.schema,tests/*}`;
`signal-router/{src/lib.rs,schema/signal-router.concept.schema,Cargo.toml}`;
`owner-signal-router/{src/lib.rs,schema/owner-signal-router.concept.schema}`;
`spirit/src/{engine.rs,nexus.rs,store.rs}` (engine-trait signatures);
`persona/src/engine.rs` (MESSAGE_ROUTER_COMPONENTS). Reports 1-3 of this session
for the rulebook, intent anchors, and base recipe.
