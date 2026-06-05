# 4 — message → production on the schema/triad-engine base

Per-component port map for the `message` component (repo
`/git/github.com/LiGoldragon/message`). Source-grounded against the actual
repo HEAD (`9f14b7a`, 2026-06-05), `signal-message` (`c87e8fd`), the
`router` consumer, and the base reference (`spirit` / `triad-runtime` /
`schema-rust-next`) via reports 1-3 of this session. Reads reports
`1-skills-production-rulebook.md` (rule citations Rxx), `2-intent-agglomeration.md`
(intent anchors), `3-triad-base-state.md` (the build recipe).

Anchoring fact (verified): `message` is PRE-triad-engine. It is a hand-written
Kameo + raw-`UnixListener` daemon carrying the OLD `signal_channel!` contract
and a `message.concept.schema` stub. It must port ONTO the spirit-pilot shape:
`schema/{signal,nexus,sema}.schema` -> `src/schema/*.rs` emitted by
`schema-rust-next`, three engine-trait impls, and the `triad-runtime` runner.

## 0. The persona-message / signal-persona-message question — RESOLVED: stale

The frame asked whether the `persona-message` + `signal-persona-message` pair is
the live/renamed line or stale. Verified:

- `/git/github.com/LiGoldragon/persona-message` and
  `/git/github.com/LiGoldragon/signal-persona-message` **do not exist** (no
  canonical checkout).
- `~/wt/github.com/LiGoldragon/persona-message/` and
  `~/wt/github.com/LiGoldragon/signal-persona-message/` exist but are **EMPTY
  worktree-container directories** (created May 16, never populated, zero files).
- `message`'s own git history settles it: commit `b85b69b`
  [message: rename from persona-message]. The rename went FROM `persona-message`
  TO `message`. The live line is `message` + `signal-message`. The
  `persona-message` names are the pre-rename ancestry; the empty `~/wt` dirs are
  abandoned scaffolds, not a future line.

Conclusion: the canonical, live, building line is **`message`** (daemon + CLI)
and **`signal-message`** (wire contract). No persona-prefixed variant is live.
A port author should ignore the empty `~/wt/.../persona-message*` scaffolds.

## 1. Current architecture (source-grounded)

### 1.1 Crate + binaries

`message/Cargo.toml`: one crate `message`, three binaries —
`message` (CLI, `src/main.rs`), `message-daemon` (`src/bin/message_daemon.rs`),
`message-validate-output` (`src/bin/message_validate_output.rs`). Dependencies
are the OLD stack: `kameo` (a `persona-lifecycle-terminal-outcome` branch),
`signal-core`, `signal-frame`, `signal-persona`, `signal-persona-origin`,
`signal-message`, `nota-codec`, `nota-config`, `rkyv`, `tokio` (rt-multi-thread),
`libc`, `thiserror`. **No `triad-runtime`, no `schema-rust-next`, no
`schema-next`, no `sema`, no `sema-engine` dependency** (verified empty grep in
Cargo.toml). `src/actors/` is an EMPTY directory — the prior actors module was
inlined into `daemon.rs` (commit `aa474bc`).

### 1.2 Daemon shape (the hand-written runtime)

`message/src/daemon.rs` (584 lines) is the whole runtime, hand-written:

- `MessageDaemon::from_configuration(MessageDaemonConfiguration)` reads typed
  config (socket paths, modes, `owner_identity`, `component_ingresses`,
  supervision socket) and `run()` is the daemon loop.
- `run()` binds via `bind_listeners()`, spawns a `SupervisionListener` (own
  thread, own `tokio::runtime::Runtime`), builds a SECOND
  `tokio::runtime::Runtime`, spawns ONE Kameo root actor
  `MessageDaemonRoot`, then a busy-poll accept loop
  (`accept_one()` -> `sleep(10ms)` on WouldBlock) gated by
  `SupervisionStopSignal`. On stop it `stop_gracefully()`s the root and asserts
  the terminal outcome.
- `MessageDaemonRoot { router: SignalRouterClient, owner_identity, forwarded_count }`
  — the one data-bearing actor (R8-compliant: real fields). Its
  `Message<ForwardMessageRequest>` handler calls `forward()` ->
  `stamp_request()`: `MessageSubmission` becomes `StampedMessageSubmission`
  (attaching `ingress.origin(&owner_identity)` + a daemon-minted
  `TimestampNanos`), then `self.router.submit(request)` opens a fresh
  `UnixStream` to `router.sock` and round-trips one frame. `StampedMessageSubmission`
  arriving from outside is rejected as `MessageRequestUnimplemented`; `InboxQuery`
  is forwarded as-is.
- SO_PEERCRED is real: `PeerCredentials::from_stream` calls
  `libc::getsockopt(..., SO_PEERCRED, ...)` (daemon.rs:556-577) and yields a
  `UnixUserIdentifier`. `MessageIngressAuthority::origin_for_peer` maps
  (owner_identity, peer uid) to `MessageOrigin::External(Owner | NonOwnerUser)`
  or `InternalComponentInstance`.

**Multi-listener TODAY (load-bearing for the port decision).** `bind_listeners()`
binds the external `message.sock` PLUS one socket per configured
`ComponentMessageIngress` (`daemon.rs:129-142`). Each `MessageSocketBinding`
carries a distinct `MessageIngressAuthority` (`ExternalPeer` vs
`InternalComponentInstance(origin)`). So message is ALREADY a multi-socket
daemon — but the sockets are differentiated by **origin attribution** (which
stamp to apply), NOT by the meta-signal authority tier (owner-policy vs
ordinary-peer). This is a different axis than R12's two-tier split.

### 1.3 Wire / CLI

- CLI (`src/command.rs` + `src/main.rs`): `CommandLine::decode_input()` takes
  exactly ONE argv argument (inline NOTA if it `starts_with('(')` else a file
  path), `require_single_argument()` rejects a second arg. Input is the
  message-local `Input` enum `[Send Inbox]`. `Input::run` resolves the socket
  via `SignalMessageSocket::from_environment()` (reads `MESSAGE_SOCKET` or
  `PERSONA_SOCKET_PATH` env vars — `router.rs:34-38`), opens one `UnixStream`,
  round-trips one length-prefixed rkyv frame, prints one NOTA `Output`. The CLI
  has exactly one Signal peer (its daemon) and opens no database — R21-clean —
  **except** for the env-var socket resolution, which violates the
  single-argument rule's spirit (socket location must be a config field, not an
  env var — R19). INTENT/ARCHITECTURE call `from_environment` "transitional dead
  code", but it is the ONLY socket source in `Input::run` (command.rs:46-47), so
  it is LIVE on the CLI path, not dead.
- Transport: `SignalRouterFrameCodec` (router.rs) hand-wraps a 4-byte
  big-endian length prefix around `signal-message`'s
  `encode_length_prefixed`/`decode_length_prefixed`. This duplicates what
  `triad-runtime`'s `LengthPrefixedCodec` provides on the base.
- Daemon config arg: `message_daemon.rs` is 9 lines —
  `ConfigurationSource::from_argv()?.decode()` into `MessageDaemonConfiguration`,
  then `MessageDaemon::from_configuration(...).run()`. Single-argument-clean for
  the daemon (R19): the one arg is a NOTA/rkyv config file.

### 1.4 Contract repo (`signal-message`)

`signal-message/src/lib.rs` is the wire contract via the OLD `signal_channel!`
macro (not `schema-rust-next` `WireContract` emission). The request enum
`MessageRequest` declares `MessageSubmission`, `StampedMessageSubmission`,
`InboxQuery`; the reply enum `MessageReply` declares `SubmissionAccepted`,
`SubmissionRejected`, `InboxListing`, `MessageRequestUnimplemented`. It also
holds `MessageDaemonConfiguration` (the typed argv config) and
`ComponentMessageIngress`.

**R24 violation present in source (correction to report 1 D4).** Report 1 §D4
said signal-message is "cleaner on R24" because its CONCEPT SCHEMA uses domain
verbs. But the actual Rust contract uses Sema classification words as the
request-variant authority tags: the `signal_channel!` block declares
`Assert MessageSubmission`, `Assert StampedMessageSubmission`,
`Match InboxQuery` (lib.rs:271-285). `Assert`/`Match` are two of the six
forbidden Sema words. So the LIVE contract DOES carry the R24 pattern, even
though it is not on the named-six list and its `.concept.schema` looks clean.
The port must move these to domain verbs (Submit / Query — already the
concept-schema operation roots).

### 1.5 The concept schema (the pre-triad shape)

`message/schema/message.concept.schema` and
`signal-message/schema/signal-message.concept.schema` are BYTE-IDENTICAL stubs:
operation roots `[(Submit [Message StampedMessage]) (Query [Inbox])
(Validate [Output])]`, empty import/export, a flat declaration namespace with
`Message (Text)`, `StampedMessage (Message Origin)`, `Text (String)`,
trailing `[(Version 0 1) (Status Concept)]`. This is the OLD all-in-one concept
form (R1): no plane split, no Nexus feature catalog, no SemaEngine surface, and
the payloads are `Text`-stub placeholders that do NOT match the real Rust
contract (`MessageRecipient`/`MessageKind`/`MessageBody`). The concept schema is
not the source of truth for the running code; the `signal_channel!` Rust is.

### 1.6 Supervision

`message/src/supervision.rs` already implements the engine-management
supervision surface: `SupervisionPhase` (Kameo actor) handles
`SupervisionRequest::{Announce -> Identified, Query(Readiness) -> Ready,
Query(Health) -> HealthReport, Stop -> StopAcknowledged}` over its own
supervision socket — the same template report 2 §C names from `mind`. So
message ALREADY exposes the persona-supervision surface (the `czw0`
on_start/on_stop equivalent), via a hand-written thread + Kameo actor rather
than the generated engine-trait lifecycle hooks.

### 1.7 Build / test status TODAY

GREEN. `cargo build --offline` compiled the whole dependency tree and produced
fresh `target/debug/message` + `target/debug/message-daemon` binaries (2m01s,
exit 0, 2026-06-05). Tests: `tests/message.rs` (38 `fn`, ~17 test fns),
`tests/actor_runtime_truth.rs` (7), `tests/actor_discipline_truth.rs` (2), plus
Nix `checks` witnesses listed in ARCHITECTURE.md. (I did not run the suites —
READ-ONLY discipline — so "tests green" is not freshly observed; the BUILD is
freshly observed green.)

### 1.8 Rust-discipline state (pre-existing, carries into the port)

- Free functions outside main/test: `surface.rs:23` `pub fn expect_end(...)` and
  `supervision.rs:378` `fn io_error(...)` — two R26 violations to fold into a
  method on a data-bearing type during the port.
- `Arc<AtomicBool>` shared stop signal (`SupervisionStopSignal`) is shared
  cross-thread, not `Arc<Mutex<T>>` between Kameo actors — not the R34 hot
  violation, but it is the kind of ad-hoc cross-thread coordination the runner
  shell replaces.
- Two `tokio::runtime::Runtime`s built per process (one for supervision thread,
  one for root) — the runner shell collapses this.
- Typed errors are R30-clean (`thiserror` `Error` enum in `error.rs`).

## 2. The gap to the base (vs the spirit-pilot recipe in report 3)

Keyed to the report-1 checklist and report-3 recipe. Everything below is NOT
DONE today.

1. Schema shape (R1, R2, R4). No `schema/signal.schema` / `nexus.schema` /
   `sema.schema`; only the dead concept stub. No emission via
   `GenerationDriver`/`ModuleEmission`. The contract still emits through
   `signal_channel!`, not `schema-rust-next`'s `WireContract` target.
2. Engine traits (R6-R8). No `impl SignalEngine`/`NexusEngine`/`SemaEngine`.
   The hand-written `MessageDaemonRoot` mixes Signal triage (PeerCred + origin
   stamp), Nexus decision (the `stamp_request` match), and the router-forward
   egress in one Kameo handler — a 3d5z separation violation.
3. Nexus feature catalog (R5, z6qu). The internal features — origin
   attribution from (owner_identity, peer uid), the
   submission/stamped/inbox triage match, the verb/payload mismatch rejection —
   are inline `match` arms, NOT declared Nexus verb+objects. None is visible in
   a schema.
4. Runner (R9-R11). Not wired to `triad-runtime`. The daemon is a hand-rolled
   busy-poll accept loop with `sleep(10ms)` (a push-not-pull R37 smell on the
   accept path) plus a second supervision thread.
5. Wire transport (R20, R31). Hand-rolled `SignalRouterFrameCodec` duplicates
   `LengthPrefixedCodec`; should move to the runner's transport.
6. Contract (R24). `Assert`/`Match` Sema words on the wire (signal-message
   `signal_channel!`).
7. CLI socket source (R19). `MESSAGE_SOCKET`/`PERSONA_SOCKET_PATH` env-var
   resolution on the live CLI path.
8. Rust discipline (R26). Two free functions to absorb into nouns.
9. The base-not-yet-landed caveats apply unchanged (report 3): no `triad_main!`
   macro (hand-write the daemon shell); `MultiListenerDaemon` committed but
   never exercised by a reference daemon; `bootstrap-policy.nota` absent from
   the reference; cross-plane `OriginRoute` `From` glue hand-written.

## 3. The port plan (ordered, concrete)

### 3.1 The defining design question — does message need a SEMA plane?

This is the #1 OPEN question from report 2 §E.1, restated here as the first port
decision because it shapes everything. message is a stateless boundary
(INTENT.md: "Neither carries a durable message ledger. Both are stateless
boundary surfaces"). Intent `l3k4`/`17ss` (description-first): [Router declares
message-delivered as a durable fact on harness ack; MESSAGE creates a LOG EVENT
for the existence of the message; DELIVERY truth is the router's]. So two
readings:

(a) **Pure Signal+Nexus carve-out (recommended default).** message owns no
durable state at all: identity/time/sender are MINTED per-request and forwarded;
nothing persists locally. Under this reading message ships TWO plane schemas
(`signal.schema` + `nexus.schema`) and NO `sema.schema`, with the SEMA-absence a
DELIBERATE, schema-documented carve-out — the same way R15 makes meta-signal
optional for no-owner components. The Nexus engine's `apply_sema_write` /
`observe_sema_read` hooks (which `schema-rust-next` requires on `NexusEngine`)
would have an empty SEMA target; the cleanest form is a Nexus that emits NO
`CommandSemaWrite`/`CommandSemaRead` actions, so the SEMA hooks are never called.

(b) **Thin durable log SEMA.** l3k4 says message "creates a LOG EVENT for the
existence of the message". If that log-event is meant to be DURABLE on
message's side (a forwarded-submission ledger for replay/audit), message gets a
minimal `sema.schema` with one table (`ForwardedSubmission`) and a real
`SemaEngine` over `sema-engine`. This contradicts INTENT.md's "no durable
ledger" — so reading (b) requires explicit psyche intent to override INTENT.md.

The tension is real and unresolved in intent: lc2r says a triad is "at least
three plane schema files", but a genuinely stateless component has nothing for
SEMA to own, and INTENT.md is explicit that message holds no ledger. **The
recommended path is (a) — a named stateless carve-out (Signal+Nexus only)** —
carried as an OPEN DECISION for the psyche (§6.1). The rest of this plan assumes
(a) and notes where (b) would differ.

### 3.2 Plane schemas to author

Author inside the daemon crate (`message/schema/`), deleting the concept stub:

- `message/schema/signal.schema` — but per `lc2r` (VeryHigh), the WIRE Signal IO
  is the contract repo's job, NOT the daemon's. So the daemon-local
  `signal.schema` is the one that EMITS `SignalEngine` (the `SignalRuntime`
  target, R4), importing the wire `Input`/`Output` roots from `signal-message`.
  The wire vocabulary (Submit/Query roots, payload records, reply records) lives
  in `signal-message` emitted via `WireContract`. Two different "signal schemas"
  — do not conflate (R4).
- `message/schema/nexus.schema` — the decision plane and the LOAD-BEARING file.
  It declares `NexusWork` (the runner-re-enter facts:
  `(SignalArrived ...)`, plus `(SemaWriteCompleted ...)`/`(SemaReadCompleted ...)`
  only if reading (b) is chosen, plus `(EffectCompleted ...)`), `NexusAction`
  (the 5-variant set: `ReplyToSignal`, `CommandEffect`, `Continue`, and
  `CommandSemaWrite`/`CommandSemaRead` only under (b)), and the effect catalog
  if any (§3.4).
- `message/schema/sema.schema` — OMITTED under reading (a); a minimal
  `ForwardedSubmission` table under reading (b).

### 3.3 The Nexus feature catalog — KEY verbs+objects to declare (z6qu, R5)

Every internal feature of today's hand-written `MessageDaemonRoot` must surface
as a declared Nexus verb+object BEFORE its Rust body exists. Enumerated from the
current daemon source:

- **Origin attribution.** Verb+object declaring the mapping from
  (configured `OwnerIdentity`, peer `UnixUserIdentifier`, ingress
  `MessageIngressAuthority`) to a `MessageOrigin`
  (`External(Owner)` / `External(NonOwnerUser)` / `InternalComponentInstance`).
  This is the `origin_for_peer` logic today (daemon.rs:525-543) — currently an
  invisible inline match.
- **Ingress stamping.** Verb+object: from `MessageSubmission` +
  attributed `MessageOrigin` + minted `TimestampNanos` produce
  `StampedMessageSubmission`. (The current `stamp_request`.)
- **Operation triage.** Verb+object declaring the dispatch over the three
  request kinds: stamp-and-forward `MessageSubmission`; reject an externally
  arriving `StampedMessageSubmission` as unimplemented; forward `InboxQuery`
  as-is. (The current `stamp_request` match arms.)
- **Verb/payload mismatch rejection.** Verb+object: a mismatched outer Signal
  verb vs request payload -> typed `RequestRejectionReason`. (ARCHITECTURE
  invariant; currently in the codec.)
- **Router forward.** The egress to `router.sock`. This is the most interesting
  z6qu surfacing: today `MessageDaemonRoot.router.submit()` opens a synchronous
  `UnixStream` to router INSIDE the Nexus decision — a blocking peer call from
  within a handler. On the runner, message-to-router is itself an
  inter-component Signal exchange; the cleanest model is a Nexus
  `CommandEffect(ForwardToRouter(StampedMessageSubmission))` whose effect
  handler performs the router exchange and returns
  `NexusWork::EffectCompleted(RouterReplied(MessageReply))`, keeping the Nexus
  step non-blocking (R34/R37). See §3.4.

The acceptance test (`vpi8` terseness): after the port, the hand-written Nexus
body is match-decide-route only; the attribution/stamping/triage rules read off
the nexus schema, not the Rust.

### 3.4 SEMA tables / effects

- Under reading (a): NO sema tables (stateless carve-out, §3.1). The
  `NexusEngine::apply_sema_write`/`observe_sema_read` hooks exist (the emitter
  requires them) but are never driven because the Nexus emits no Sema commands.
- **The router-forward effect.** message's one genuine effect is the outbound
  call to `router.sock`. Declare it as a component effect in `nexus.schema`
  (`NexusEffectCommand [(ForwardToRouter StampedMessageSubmission)]`,
  `NexusEffectResult [(RouterReplied MessageReply)]`), implement `run_effect`
  to perform the router Signal exchange via the `signal-message` contract
  (router is the message contract's second relation — verified: router consumes
  `signal-message` and handles `StampedMessageSubmission`, router.rs:1075-1098).
  This is the production form of the delivery path (§5 critical gap): the
  message->router exchange becomes a declared, traceable effect on the runner,
  not a hidden synchronous `UnixStream` in a Kameo handler.

### 3.5 Contract-repo work (`signal-message`)

- Re-emit `signal-message` via `schema-rust-next`'s `WireContract` target from a
  proper `signal-message/schema/signal-message.schema` (replacing the
  `signal_channel!` macro and the concept stub). Wire-only: Input roots, Output
  roots, payload/reply records, NOTA codec — NO engine traits, NO Nexus/SEMA
  (R4, l6zw, lc2r).
- **R24 cleanup (real, in source).** Drop the `Assert`/`Match` Sema-word
  authority tags from the request variants; the wire roots are domain verbs
  (Submit / Query). The Sema class is derived internally in message's nexus, not
  declared on the wire.
- **No meta-signal-message repo (R15, e2px/kvg1).** message has no owner issuing
  policy: its control-plane config arrives as a typed argv
  `MessageDaemonConfiguration`, and delivery authority/policy live entirely in
  router. So message legitimately ships TWO repos (daemon `message` + working
  contract `signal-message`), not three. There is **no owner-signal-message to
  rename** — verified absent. The owner-signal->meta-signal rename does NOT
  touch message. (The rename is router/orchestrate work; see maps 5/6.) This
  must be stated as a deliberate no-owner decision, not an unbuilt surface
  (R12/R15).
- `MessageDaemonConfiguration` (the typed argv config) stays in the contract
  crate or moves to a config module; it is consumed by the daemon, not a wire
  verb.

### 3.6 Runner wiring — SingleListener vs MultiListener

This is a genuinely interesting decision for message because of §1.2.

- The R12 two-tier axis (ordinary vs meta-signal) does NOT apply: message has
  no meta tier (§3.5). On the authority axis, message is single-listener.
- BUT message ALREADY binds multiple sockets on the ORIGIN-ATTRIBUTION axis
  (`message.sock` external + N internal `ComponentMessageIngress` sockets),
  each tagged with a `MessageIngressAuthority` that selects the stamp. This maps
  cleanly onto `triad-runtime`'s `MultiListenerDaemon`: the component supplies a
  `Listener` tag enum (`ExternalPeer` / `InternalComponentInstance(origin)`),
  and `handle_stream(listener, stream)` carries the tag into the SignalEngine so
  the origin attribution (§3.3) reads the listener tag + SO_PEERCRED. The
  supervision socket is a THIRD listener (or stays a separate concern handled by
  the runner's lifecycle, since persona supervision drives on_start/on_stop).
- **Recommendation: MultiListenerDaemon**, with the listener tag carrying the
  ingress authority. This preserves today's external/internal socket
  multiplexing on the runner. CAVEAT (report 3, R13): `MultiListenerDaemon` is
  committed in `triad-runtime` but NEVER exercised by a reference daemon —
  message would be the FIRST real `MultiListenerDaemon` consumer (orchestrate's
  two-socket precedent is the OLD thread shape, not the runner). This is a
  pattern-establishing port, not a copy of a worked example.
- If the internal `ComponentMessageIngress` sockets are deemed out-of-scope for
  the first port slice, message can start on `SingleListenerDaemon`
  (external `message.sock` only) and add internal-ingress listeners later. That
  loses today's component-instance origin stamping in the first slice — a
  functional regression to flag.

### 3.7 The CLI

- Replace `SignalMessageSocket::from_environment()` (env-var socket resolution,
  R19 violation) — the socket path is a field of the single NOTA argv argument
  or a fixed config-derived path, never an env var. The CLI remains: one NOTA
  in, exactly one Signal peer (the daemon), no database (R21). Use the runner's
  `SignalTransport` / `LengthPrefixedCodec` rather than the hand-rolled
  `SignalRouterFrameCodec`.
- Add `(Help Main)` + `(Help (Verb ...))` to the ordinary contract (R22) —
  auto-injected via the contract emission.

### 3.8 Bootstrap policy

None. message holds no policy state (reading (a)), so there is no
`bootstrap-policy.nota` and no policy-table bootstrap (R16/R17 N/A). Under
reading (b) the durable log is WORKING state, which "never bootstraps from
file" (R16) — still no bootstrap-policy file. This is a clean simplification
relative to router/orchestrate.

### 3.9 Rust-discipline fixes folded into the port

- Fold `surface.rs::expect_end` and `supervision.rs::io_error` (R26 free
  functions) into methods on data-bearing types (e.g. a `NotaDecodeCursor`
  method, an `Error` constructor).
- Collapse the two `tokio::runtime::Runtime`s and the busy-poll accept loop into
  the runner shell (the runner owns the accept loop; supervision lifecycle is
  the engine-trait `on_start`/`on_stop`).

### 3.10 Ordered step list

1. Decide §3.1 (SEMA-plane question) with the psyche — gates the schema count.
2. Branch: one feature branch name (e.g. `triad-engine-port`) across `message`
   + `signal-message`, worktrees under `~/wt/...` (C1-C3, designer-on-next).
3. Author `signal-message/schema/signal-message.schema` (wire-only, domain
   verbs, R24-clean); wire `WireContract` emission via `GenerationDriver`;
   delete the concept stub and the `signal_channel!` block.
4. Author `message/schema/signal.schema` (SignalRuntime, imports wire IO) and
   `message/schema/nexus.schema` (the §3.3 feature catalog + §3.4 effect);
   author `sema.schema` only under reading (b).
5. Wire `message/build.rs` with `ModuleEmission::signal_runtime_module("signal")`
   + `::nexus_runtime()` (+ `::sema_runtime()` under (b)); emit
   `src/schema/*.rs`.
6. Implement the engine traits: `SignalEngine` on a data-bearing
   `MessageSignalActor` (PeerCred + listener-tag triage, reply projection);
   `NexusEngine` on a `MessageNexus` (the attribution/stamping/triage decide +
   the ForwardToRouter effect + budget reply); `SemaEngine` only under (b).
   Lifecycle: `on_start` binds sockets / connects router; typed failure (R7).
7. Wire the daemon shell to `MultiListenerDaemon` (§3.6) with the
   ExternalPeer/InternalComponentInstance listener tags; hand-write `main`
   (no `triad_main!`, R11).
8. Port the CLI off env-var socket resolution onto the single NOTA argv +
   runner transport; add Help.
9. Witness tests (§4), including the live message->router delivery round-trip.
10. Update `message/INTENT.md` + `ARCHITECTURE.md` and
    `signal-message/INTENT.md` + `ARCHITECTURE.md` on the SAME branch (§7).

## 4. Witness tests (component-triad witness table, specialized)

Each constraint gets a positive witness (execute/round-trip/observe) and a
negative guard (R35); a positive grep is never proof.

Schema-chain (R36, the strongest):
- `message-signal-to-nexus-stamps-origin-through-engine-traits` — drive a
  `MessageSubmission` Signal in through `SignalEngine::triage` ->
  `NexusEngine::execute` and observe a `StampedMessageSubmission` with the
  correct `MessageOrigin` and a minted timestamp, via generated root types
  (not test-only enums). Testing-trace socket records prove the engine-trait
  methods were actually called.
- **`message-to-router-delivery-round-trip` (THE critical gap, §5)** — spawn the
  message daemon on a temp `message.sock` and a real router daemon on a temp
  `router.sock`; the message Nexus's ForwardToRouter effect performs the
  exchange; observe router commits the submission to a slot and returns
  `SubmissionAccepted`, and the CLI prints it. This is the live delivery
  assertion report 74 says nothing currently provides. Positive: the round-trip
  succeeds with a slot. Negative guard: with router absent, the effect returns a
  typed `MessageRequestUnimplemented(DependencyMissing(Router))`, not a panic or
  a silent drop.

Authority / sockets:
- `message-multi-listener-attributes-external-vs-internal-origin` — a stream on
  `message.sock` from a non-owner uid stamps `External(NonOwnerUser)`; a stream
  on a configured internal-component-ingress socket stamps
  `InternalComponentInstance(origin)`. Negative:
  `message-rejects-caller-supplied-origin-in-payload` — a payload carrying a
  fabricated origin is ignored; the daemon-minted stamp wins (provenance never
  inferred from payload).

Wire / argv:
- `message-binary-rejects-flag-style-arguments` (R19) — `message --verbose`
  fails closed.
- `message-cli-resolves-socket-from-argument-not-env` (R19) — the NEW negative
  guard replacing the env-var path: `MESSAGE_SOCKET` set but the argv carries no
  socket -> the CLI does not silently use the env var (proves the env-var path
  is gone).
- `message-daemon-rejects-non-signal-traffic-on-its-socket` (R20) — NOTA/JSON
  bytes on `message.sock` are rejected.
- `message-cli-accepts-one-argument-and-prints-one-nota-reply` (R21) +
  `message-cli-cannot-open-any-database-or-peer-socket` (R21).

Verbs / contract:
- `signal-message-contract-carries-no-sema-classification-words` (R24,
  negative) — the contract source has no `Assert`/`Match`/`Mutate`/`Retract`/
  `Subscribe`/`Validate` as request-root authority tags and no
  `AuthorizedSignalVerb` mirror.
- `message-signal-verb-mapping-covers-every-request-variant` (R23).
- `message-help-main-and-help-verb-present` (R22).

Lifecycle / supervision:
- `message-engine-lifecycle-runs-generated-trait-hooks` (R7) — `on_start` binds
  sockets / connects router; on failure returns the typed `ActorStartFailure`
  variant persona supervision reads.
- `message-graceful-stop-releases-socket-and-rejects-later-ingress` (carry the
  existing ARCHITECTURE invariant onto the engine-trait `on_stop`).

Stateless carve-out (reading (a) specific):
- `message-nexus-emits-no-sema-command` (negative) — the Nexus produces no
  `CommandSemaWrite`/`CommandSemaRead` action for any input, witnessing the
  deliberate stateless carve-out (the schema-documented SEMA absence is real,
  not an unbuilt plane).

Rust discipline:
- `message-source-has-no-free-functions-outside-main-and-test` (R26, negative
  guard) — catches the `expect_end`/`io_error` regressions.

## 5. Blockers (real foundation dependencies — honest)

Hard prerequisites that must land before, or be established by, this port:

1. **The message->router delivery round-trip is not on the runner and nothing
   asserts it (THE #1 gap, report 74).** Verified: neither message nor router
   depends on `triad-runtime`; the message->router path is a synchronous
   `UnixStream` opened inside a Kameo handler (`MessageDaemonRoot.router.submit`).
   `persona/src/engine.rs` names a `MESSAGE_ROUTER_COMPONENTS` pair and
   `operational_delivery_components()`, but the delivery round-trip is asserted
   by NAME ONLY. Porting message alone does not fix this — router must also be
   on the contract/runner at the receiving end (map 5). The delivery witness
   (§4) is a TWO-COMPONENT test; message's port is not "done"/"green" on
   delivery until router's receive side is ported too. Cross-component
   sequencing dependency.
2. **No worked `MultiListenerDaemon` reference (R13).** `MultiListenerDaemon` is
   committed in `triad-runtime` but exercised only by its own internal tests,
   never by a reference daemon. message would be the first real consumer
   (§3.6). The two-listener wiring is pattern-establishing, not copy-from-spirit
   (spirit is SingleListener-only).
3. **No `triad_main!` macro (R11).** The daemon `main` + listener wiring is
   hand-written every port (verified empty grep in `schema-rust-next`). Budget
   it as real (small) code.
4. **Cross-plane `OriginRoute` / lifecycle-error `From` glue is hand-written**
   (report 3, spirit `plane.rs`). The origin-route threading message needs for
   correlation (z821) inherits this hand-written glue until `schema-core` emits
   it.
5. **The origin-route carrying shape is OPEN (Medium, b559).** message must
   thread a correlation route through Signal->Nexus (->SEMA under (b))
   (z821, settled in principle), but whether the route is a leading tuple
   element or a named struct field is psyche-gated (report 2 §E.4). A port
   author choosing the encoding is choosing an unsettled shape.
6. **payload-less dual-lowering must be checked against message's own schema**
   (report 3): message has payload-less enum variants
   (`MessageUnimplementedReason::NotInPrototypeScope`, the `MessageKind`
   variants). report 3 could not confirm or clear the alleged `primary-vllc`
   dual-lowering defect from the base repos. Verify the emitter lowers message's
   payload-less variants correctly before assuming unblocked. Not a cleared
   blocker — an open verification item.

NOT a blocker for message specifically (clarifying honesty): the
owner-signal->meta-signal rename does NOT touch message (no owner contract
exists, §3.5); `sema-upgrade` (veqq) does NOT gate message under reading (a)
because message holds no durable redb that could drift across restart. Both
genuinely gate router/orchestrate but not a stateless message.

## 6. Open decisions for the psyche

1. **Does message get a SEMA plane, or is it a named Signal+Nexus stateless
   carve-out? (THE defining question, report 2 §E.1.)** Recommendation: the
   carve-out (reading (a)) — INTENT.md says message holds no ledger, and
   lc2r's "at least three plane schemas" reads as a default, not a mandate, for
   a genuinely stateless boundary. Reading (b) (a thin durable forwarded-log
   SEMA) would override INTENT.md and needs explicit psyche intent. This decides
   2-vs-3 plane schemas and whether the delivery witness asserts local
   durability.
2. **MultiListenerDaemon (preserve external+internal origin-attribution sockets)
   vs SingleListener-first (external `message.sock` only, internal ingress
   later)?** Recommendation: MultiListener to preserve component-instance origin
   stamping — accepting that message becomes the first real
   `MultiListenerDaemon` consumer (R13 caveat).
3. **Does the agent abstraction (w4jp/gdbf — router talks to a new `agent`
   component, not the harness) land before or after this port?** It reshapes
   router's delivery TARGET, which is the other end of message's delivery path.
   No record sequences this (report 2 §E.3). Affects whether the delivery
   witness (§4) targets harness-backed router or agent-backed router.
4. **The origin-route encoding (b559, Medium): leading tuple element vs named
   struct field?** Psyche-gated; message threads the route either way.

## 7. What lands in INTENT.md / ARCHITECTURE.md on the port branch (C4)

On the same branch as the port (continuous manifestation, spirit 944):

- `message/INTENT.md`: restate message as a triad component on the engine base —
  three execution centers (Signal triage / Nexus decide+forward / the
  stateless-SEMA carve-out under (a)); the SEMA-absence as a DELIBERATE,
  documented carve-out, not an omission; the router-forward as a declared Nexus
  effect (not a synchronous in-handler call); the two-repo (no meta-signal)
  shape as a deliberate no-owner decision. Remove the "depends on stable Persona
  Kameo lifecycle reference" framing in favor of the engine-trait lifecycle
  hooks.
- `message/ARCHITECTURE.md`: replace the Kameo-actor-topology section
  (`MessageDaemonRoot` busy-poll) with the engine-trait runtime (SignalEngine /
  NexusEngine / [SemaEngine]) on `triad-runtime`; document the
  MultiListener listener-tag -> ingress-authority -> origin-attribution mapping;
  document the Nexus feature catalog (z6qu) as the readable internal-feature
  surface; fix the stale `persona-router` references to `router`; replace the
  env-var CLI socket invariant with single-argument NOTA socket resolution;
  re-point the Constraint-Tests table at the new witnesses (§4).
- `signal-message/INTENT.md` + `ARCHITECTURE.md`: restate as a wire-only
  `WireContract`-emitted contract (no `signal_channel!`, no engine traits,
  domain-verb roots, no Sema words); note the two relations
  (CLI<->message-daemon and message-daemon<->router) the one contract serves.

## Sources (verified 2026-06-05)

`/git/github.com/LiGoldragon/message/{Cargo.toml,INTENT.md,ARCHITECTURE.md,
src/{lib,daemon,router,command,surface,supervision,error}.rs,
src/bin/message_daemon.rs,schema/message.concept.schema}`;
`/git/github.com/LiGoldragon/signal-message/{src/lib.rs,
schema/signal-message.concept.schema}` (HEAD `c87e8fd`);
`/git/github.com/LiGoldragon/router/{Cargo.toml,src/router.rs}` (the
signal-message consumer + StampedMessageSubmission handler); git history
(`b85b69b` rename-from-persona-message); empty `~/wt/.../persona-message*`
scaffolds; `cargo build --offline` GREEN (message + message-daemon, 2m01s).
Reports 1-3 of this session for rule/intent/base citations.
