# Federation Audit

I have enough evidence across all 16 repos to compile the ledger. Per the explicit instruction ("FINAL message IS the data ... Do NOT Write report/summary/findings/analysis .md files"), I am returning everything inline rather than writing a file.

# PERSONA FEDERATION — Completeness Audit (claimed vs actual, integration-wired?)

Method: read source directly (ARCHITECTURE claims vs dispatch/effect code) across all 16 repos at `/git/github.com/LiGoldragon/`. Every claim below is grounded in a `file:line` I inspected. I did **not** compile or run the daemons (see Verification Limits) — runtime/wiring conclusions are tagged INFERENCE, code contents are FACT.

Headline: hard stub markers (`todo!`/`unimplemented!`) are nearly absent — but the federation encodes "not done" as **typed** `RequestUnimplemented{NotBuiltYet | NotInPrototypeScope}` replies and **hardcoded rejections**, not panics. Trusting prose here would badly overstate completeness.

## Per-daemon ledger

### persona — "supervises MULTIPLE engines; SCM_RIGHTS handoff" → PARTLY SCAFFOLD
- FACT: `manager.rs:171-210` `handle_request` hardcodes rejections: `Launch → LaunchRejected(LaunchPlanRejected)`, `Retire → RetireRejected`, `Tap|Untap → ActionRejected(ComponentNotManaged)`. These ops are not implemented — they always fail.
- FACT: `Catalog` returns exactly one engine built from `self.engine` (`manager.rs:187-195`); `daemon.rs:92` hardcodes `EngineIdentifier::new("default")`. Multi-engine catalog is **not real** — one engine "default".
- FACT: `state.rs:56 start_component` only mutates `desired_state`/`health` in the catalog; the wire `Start`/`Stop` ops **do not spawn processes**.
- FACT: the live daemon wires `ManualUnitController` (`daemon.rs:83`), whose `start/stop/restart` are no-ops returning `Ok(receipt)` (`unit.rs:449-467`). The real systemd-verb machinery in `unit.rs` is unused by the daemon.
- FACT: SCM_RIGHTS handoff code is real (`transport.rs:283 receiver.send_fds(...)`, `unix_ancillary`), but `ComponentHandoffRouter::bind/handoff_one` is referenced **only in `tests/handoff.rs`** — `daemon.rs` never mentions handoff. The public-socket FD handoff is a tested library capability, **not wired into `persona-daemon`**.
- FACT: real process spawning exists (`direct_process.rs:282 command.spawn()`, `EngineSupervisor::start_prototype_supervision`), but is reachable only when `PERSONA_ENGINE_TOPOLOGY` + executable env vars resolve a launch plan (`transport.rs:468`, `daemon.rs:99`).
- FACT: persona's integration tests spawn `persona-component-fixture` (a generic health/ready/stop responder, `src/bin/persona_component_fixture.rs`), not the real message/router/harness daemons (`tests/engine.rs:96,106`).
- Verdict: engine-status catalog + conditional prototype supervision are real; Launch/Retire/Tap and multi-engine and the FD handoff are not live. INFERENCE: as shipped, persona is a single-"default"-engine state manager whose supervision is validated against fixtures.

### router — "parks + escalates unknown channels to mind; mind decides, router enforces" → ENFORCE real, ESCALATE broken
- FACT: delivery is real — `harness_delivery.rs:61,77,139` do `UnixStream::connect` to terminal/harness/component sockets and write frames; `peer_delivery.rs:110` does real `TcpStream::connect` cross-engine forwarding with attestation.
- FACT: enforce side is real — `router.rs:1794 ApplyMindChannelGrant`, `1813 ApplyMindAdjudicationDeny` mutate authorized-channel state.
- FACT (key gap): the escalation-to-mind surface `MindAdjudicationOutbox` (`adjudication.rs`) is a plain in-memory `Vec<MindAdjudicationRequest>` with `record`/`snapshot`/`clear`. It is **read only by a pull query** `ReadRouterMindAdjudicationOutbox` (`router.rs:3121`). Router imports `signal_mind` **only for type conversions**; there is **no client, no `mind.sock` connect, nothing that pushes** an adjudication to the mind daemon.
- FACT: this outbox is not persisted (in-memory Vec), unlike the channel adjudication records which are persisted to sema tables (`channel.rs:204-208`).
- Verdict: router genuinely delivers on authorized channels and applies grants/denies, but "escalates to mind" is a passive in-memory pull queue with no drain — it violates the federation's own push-not-pull rule. INFERENCE: no automatic path carries an unknown-channel decision to mind.

### mind — "channel adjudication / work-graph; mind decides" → work-graph real, ADJUDICATION unimplemented
- FACT (smoking gun): `dispatch.rs:143-145` routes `MindRequest::AdjudicationRequest(_) | MindRequest::ChannelList(_) → self.unimplemented(trace)`, which returns `MindReply::MindRequestUnimplemented{ reason: NotInPrototypeScope }` (`dispatch.rs:367-375`). The two ops that constitute "mind decides channel admission" are explicitly **not implemented**.
- FACT: mind imports no `signal_router` and never dials router — it cannot pull router's outbox or push a decision back.
- FACT: the work-graph IS real — `store/graph.rs` implements submit/query/subscribe for thoughts, relations, technical nodes, knowledge over sema (`graph.rs:107-392`); subscriptions/deltas real.
- FACT: `ChoreographyAdjudicator` (`choreography.rs:276-336`) is unrelated to channel adjudication — it forwards `OrchestrateDecision`s to a `MindOrchestrateCaller`. Don't mistake it for the router-channel adjudicator.
- FACT: meta ops return `RequestUnimplemented{NotBuiltYet}` (`meta.rs:132`).
- Verdict: mind is a real work-memory/work-graph state engine; its channel-adjudication role is a typed no-op.

### Combined control loop (message→router→mind→router): BROKEN
INFERENCE (from the three FACTs above): an already-authorized channel delivers end-to-end; an **unknown** channel is parked (persisted in router tables + copied to an unwired in-memory outbox) and **never adjudicated** — router doesn't push to mind, and mind would answer `NotInPrototypeScope` if it did. Grants can only enter router manually via its meta socket, not from mind's decision.

### harness — "live harness login / agent delivery" → delivery real, no Claude/Codex login
- FACT: Pi path is real — `pi.rs:107-164` spawns `Command::new(pi).arg("--mode").arg("rpc")` with piped stdio and delivers prompt/steer/follow_up JSONL.
- FACT: terminal path is real — `terminal.rs:150-200 deliver_to_pty` → `UnixStream::connect` terminal socket, writes a `signal-terminal` `TerminalInputRoot` frame.
- FACT: `DeliveryChannel` has only `Terminal` and `PiRpc` (`delivery.rs:9-18`), both real.
- FACT: Claude support is observation-only — `ClaudeArtifactObserver` watches `~/.claude` artifacts (`claude.rs:16-37`); there is **no Claude/Codex process spawn or "login."** A `HarnessTerminalEndpoint::FixtureOnlyHuman` no-op variant also exists (`terminal.rs:56,141`).
- FACT: non-`MessageDelivery` ops → `HarnessRequestUnimplemented{NotBuiltYet}` (`daemon.rs:202-205`).
- Verdict: real delivery to a Pi subprocess or a terminal PTY; "live login" for Claude/Codex is not implemented (Claude is observed, not driven).

### terminal-cell — "owns a PTY + transcript replay, delivers to live agent" → REAL
- FACT: real PTY via `portable-pty` — `session.rs:13` imports `native_pty_system, CommandBuilder, MasterPty`; `session.rs:1369 .openpty(...)` spawns a real child in a PTY.
- FACT: real transcript with replay — `TranscriptScriber`, `TranscriptSnapshot`, `TranscriptDelta` with sequence numbers (`session.rs:141-200`), `ChildExitWatcher`.
- FACT: full CLI surface (send/capture/wait/exit/resize/view/session-select) + separate control/data-plane listeners.
- Verdict: the most complete data-plane endpoint. It owns a real PTY+child and writes delivered input to it; the "live agent" is whatever command the session launches. This is genuine, not scaffold.

### agent (Jun 9) — "LLM-API caller" → single-shot Call real, streaming unimplemented, provider feature-gated
- FACT: `Call → CallProvider` effect is real (`engine.rs:106`); `StreamCall`/`CancelStream → RequestUnimplemented{NotInPrototypeScope}` (`engine.rs:110-118`).
- FACT: the reqwest `OpenAiCompatibleProvider` is behind the **`live-provider` Cargo feature, default OFF** (`Cargo.toml`); default builds have no network provider.
- FACT: key resolution shells to `gopass` (`registry.rs:332`) — real secret source.
- Note: per psyche Spirit `iucr`/`f8k7`, agent is deliberately an API caller, **not** the interactive harness — it is orthogonal to the message-delivery chain. It IS the LLM backend that `spirit`'s guardian calls.

### spirit (Jul 1) — "active production" → mostly REAL; one confirmed limit, one superseded limit
- FACT: guardian LLM admission is real and wired to the `agent` daemon — `guardian.rs` builds a NOTA guardian prompt and calls `signal_agent::Input/Output` over the agent socket with verdict-parse retry (`guardian.rs:166-194`); feature-gated `agent-guardian` (`daemon.rs:131-139`).
- FACT: versioned SEMA commit log is real — `SPIRIT_SCHEMA_VERSION = 10`, `VersionedCommitLogEntry`, `RecordFamily::versioning_policy()`, checkpoint/restore (`store/mod.rs:67-392`).
- FACT (known-limit **superseded**): schema diff/upgrade is now implemented — `production_migration.rs` has real `StoreMigration`/`DataMigration` across versions 8→9→10 plus a `spirit-migrate-store` binary. The old "schema diff/upgrade traits unimplemented" note is out of date.
- FACT (known-limit **confirmed**): mail ledger is in-memory — `MailLedger { events: StdMutex<Vec<MailLedgerEvent>> }` (`engine.rs:356-357`), not persisted.
- FACT (known-limit **partly moot**): the store is owned by the engine which is owned by the kameo `EngineActor` (`engine.rs:330`); only two ID counters use `StdMutex`. "Store under a mutex not an actor" is now mailbox-serialized through EngineActor.
- INFERENCE: owner-only meta (incl. `Input::Retire`, `daemon.rs:227`) is enforced by a distinct owner-only meta transport/socket (`meta_transport.rs`); I found no in-process SO_PEERCRED/uid check, so the "owner-only" guarantee rests on socket ownership/mode, not a peer-cred assertion (UNKNOWN — see below).
- Verdict: genuinely the most production-ready component; "active production" is credible.

### mentci / mentci-lib / mentci-egui (Jun 18) — UI path REAL but generic + criome-scoped
- FACT: `mentci-egui/daemon_client.rs:132` does `UnixStream::connect` and exchanges real `signal-mentci` frames; `app.rs` is a real `eframe::App` rendering replies (NOTA fallback) with approval cards. The `unreachable!()` at `app.rs:290` is a `PolicyAction::New` guard, not a feature stub.
- FACT: `mentci/daemon.rs:121 handle_connection` serves requests, applies state, applies criome effects, answers parked criome requests (`daemon.rs:191`). Canonical state is in-memory (`lib.rs:4`).
- FACT: the "49 soft markers" are largely false positives — the domain noun `ScaffoldPointer/ScaffoldIdentity/ScaffoldVersion` in `preflight.rs` (agent-scaffold definitions) plus "in-memory state", not code stubs.
- Observation (INFERENCE): ARCHITECTURE frames mentci as "the programmable approval surface for the local **criome**"; the first egui surface is "intentionally generic" NOTA payload view. It is a working approval/escalation UI, **not** a polished persona chat/delivery interface. Calling it "the USER INTERFACE for Persona" overstates its current scope.

### message — ingress → REAL working path, meta unimplemented
- FACT: origin minting via SO_PEERCRED through `triad_runtime::ConnectionContext` (`config.rs:25`); `RouterForwarder::submit` does `UnixStream::connect(router socket)` and forwards the stamped frame (`router.rs:62-66`).
- FACT: meta `Configure → RequestUnimplemented{NotBuiltYet}` (`meta.rs:144`).
- Verdict: the submit→stamp→forward-to-router ingress is real; configuration surface is skeleton.

### listener (Jul 1) — first vertical slice REAL, meta scaffold
- FACT: `Start` spawns a real capture process (`capture.rs:267` default `parecord`, env `LISTENER_CAPTURE_PROGRAM`; `capture.rs:324 Command::new(...).spawn()`), streams PCM to durable disk; `Stop` exports PCM, calls `ConfiguredBatchTranscriber::transcribe`, delivers text to output targets/clipboard (`runtime.rs:71-125`). Start/Stop/Status all served.
- FACT: meta CLI is scaffold — `meta.rs:30 Err(Error::NotImplemented{ "meta-listener CLI" })`.
- Smell (FACT): runtime errors (e.g. `CaptureAlreadyActive`) are mapped into wire `RequestUnimplemented` replies via `error.into_unimplemented_reply(...)` (`runtime.rs:60-70`) — conflates operational failure with "unimplemented."
- Note: listener is a standalone speech-to-text tool; no dependency on / wiring into the persona message-delivery federation.

### system — OS/focus boundary → SKELETON with unwired niri backend
- FACT: only `QueryStatus` is served; **every other** `SystemRequest` → `SystemRequestUnimplemented{NotBuiltYet}` (`supervisor.rs:148-155`). The stated core purpose (focus observation) is not built at the request surface.
- FACT: `status_reply` health/readiness is **hardcoded** (`SystemBackend::Niri => Running/Ready`, `supervisor.rs:175,181`), not a live probe.
- FACT: a real niri backend exists (`niri.rs:31,54,82 Command::new(niri)`) but is **unwired** — comment at `supervisor.rs:4`: "The live Niri event-stream path attaches here on [later]."
- Verdict: scaffold that answers only status (with a constant health).

### introspect — inspection witness → REAL but narrow
- FACT: dials component sockets (`runtime.rs:412 UnixStream::connect`), aggregates typed observations, prints NOTA; handles `RouterReply::Unimplemented` (`runtime.rs:452`).
- FACT: meta ops → `RequestUnimplemented{NotBuiltYet}` (`daemon.rs:248`).
- Verdict: real for its declared "witness, not a broad UI" scope.

### orchestrate — role/claim/worktree machinery → SUBSTANTIALLY REAL, some sema ops unbuilt
- FACT: sema-backed claim/activity/worktree registry with redb (`tables.rs`), real `jj` execution (`worktree.rs:259 Command::new("jj")`), real Signal transport (`signal_transport.rs:47,68`), plus architectural truth tests (`tests/architecture.rs`).
- FACT: some sema read/write paths return `NotBuiltYet` (`schema/sema.rs:105,174`, `execution.rs:255`).
- Verdict: real component with partial sema coverage.

### upgrade — upgrade runtime leg → LARGELY SCAFFOLD
- FACT: the entire ordinary `Input` handler returns `not_built_yet_output()` (`execution.rs:183`).
- FACT: of the sema-write ops, only `AttemptUpgrade` is real; `ReadyToHandover, HandoverCompleted, Mirror, Divergence, RecoverFromFailure, Register, Allow, Block, ForceFlip, Rollback, Quarantine` all → `not_built_yet_write_output()` (`execution.rs:201-212`). Sema-read: only `Inspect`/`Report` real; `AskHandoverMarker`/`Query` → `not_built_yet_read_output()` (`execution.rs:223-230`).
- FACT: ARCHITECTURE uses future tense ("The full daemon **will** own the migration catalogue, policy state, ...").
- Verdict: binds/serves sockets but ~1 real op (attempt_upgrade) + inspect/report; the rest is typed NotBuiltYet.

## End-to-end delivery path — true state
INFERENCE, grounded in the FACTs above:
- Data plane (`message → router → harness/terminal → PTY`): each hop is a real socket client (message forwards to router; router `UnixStream::connect`s harness/terminal; harness `UnixStream::connect`s terminal or spawns Pi; terminal-cell owns a real PTY). **On an already-authorized channel this can carry a message to a live PTY/Pi subprocess** if deployment wires the socket paths.
- Control plane (channel admission `router ⇄ mind`): **broken**. Router parks unknown channels in an unwired in-memory outbox; mind answers `NotInPrototypeScope`. No automatic adjudication exists; grants must be injected manually via router's meta socket.
- Supervision (`persona`): validated against fixture processes, not real component daemons; real-binary supervision is env-gated and untested in-repo.
- The one fully-real cross-daemon dependency I confirmed is `spirit → agent` (guardian LLM admission).

## Ranked federation gaps blocking a working whole
1. Channel adjudication loop is non-functional (blocks any unknown-channel delivery): mind `AdjudicationRequest/ChannelList` = `NotInPrototypeScope` (`mind dispatch.rs:143`) + router has no mind client and an in-memory pull-only outbox (`router adjudication.rs`). Highest severity for "mind decides, router enforces."
2. persona wire-management is largely non-functional: Launch/Retire/Tap hardcoded-reject, single "default" engine only, `ManualUnitController` no-op, FD handoff unwired (`manager.rs:171`, `daemon.rs:83`, `unit.rs:449`).
3. No real-daemon end-to-end integration proof: persona supervises fixtures, not real binaries; no in-repo test spans message→router→harness with the real daemons (`tests/engine.rs` + `persona_component_fixture`).
4. upgrade is scaffold — the version-handover/quarantine/mirror machinery the federation would need for durable evolution is all `not_built_yet` (`execution.rs:201-230`).
5. system focus-observation (its whole reason to exist) is unbuilt; niri backend unwired, health hardcoded (`supervisor.rs:148,175`).
6. harness has no Claude/Codex live login — only Pi is a managed subprocess; Claude is observe-only (`claude.rs`, `pi.rs`).
7. agent's real provider is default-off (`live-provider` feature) and streaming is unimplemented.
8. Pervasive meta/config surfaces unimplemented (`NotBuiltYet`): message, harness, introspect, system, mind, listener, upgrade — most daemons cannot yet be reconfigured over their meta socket.

## Components that ARE real (don't under-credit)
- terminal-cell (real PTY + transcript replay), spirit (versioned store, migration, guardian→agent), mind work-graph (thoughts/relations/knowledge/subscriptions), router data-plane delivery + grant/deny enforcement, message ingress, orchestrate claim/worktree store, listener STT slice, mentci approval UI + egui client. These are past scaffold.

## UNKNOWNS / verification limits
- FACT: I did not compile or run any daemon; conclusions about live wiring are code-grounded INFERENCE, not runtime-observed. A build won't distinguish stub-vs-real anyway (typed NotBuiltYet compiles clean).
- UNKNOWN: spirit meta "owner-only delete" enforcement mechanism — I found the separate owner meta transport but no in-process SO_PEERCRED/uid check; whether owner-only is guaranteed by peer-cred or only by socket mode/ownership needs a look at the meta socket bind + `triad-runtime` connection gating.
- UNKNOWN: production deployment wiring (nix/systemd) that would connect the real socket paths across daemons — not inspected (workspace bars `/nix/store` search); so whether the real data plane is ever wired together outside tests is unconfirmed.
- UNKNOWN: whether any producer (a CLI or mind) actually emits `ApplyMindChannelGrant` to router in practice, vs it being test-only.
- UNKNOWN: listener's `ConfiguredBatchTranscriber` concrete transcriber (whisper.cpp? env-configured command?) — not traced to its invocation.
- Not audited in depth (outside the named lead set): the many `signal-*`/`meta-signal-*`/`sema-*`/`schema-*`/`triad-runtime` support crates; I treated them as contract/support surfaces, not daemons.