---
variant: Audit
slice: 2 — old-stack / other component daemons (persona-spirit, mind, persona, terminal, router)
constraint: psyche record 2560 (VeryHigh) — strict, absolute triad-engine separation
branching: psyche record 2561 — main + long-lived next; designers branch in ~/wt
date: 2026-06-04
lane: designer (sub-agent)
action: blocked-needs-concept (all five components)
---

# Slice 2 — Old-stack component daemons vs strict triad-engine separation

## The constraint being audited

Per psyche record 2560 (VeryHigh): the triad-engine separation is
**strict and absolute**. The **SEMA engine** owns ALL database and
durable-state code; the **Nexus engine** owns ALL decision-making; the
**Signal engine** owns ALL communication. A component daemon contains NO
database boilerplate, NO decision-making, and NO communication code
outside its respective engine. The schema-derived pilot realizes this as
three composable engines (`SemaEngine` on `Store`, `NexusEngine` on
`Nexus`, `SignalEngine` on `SignalActor`) wired by thin scaffolding
(`engine.rs`, `daemon.rs`, `transport.rs`, `config.rs`, `bin/main`).

## Headline finding

The five components in this slice are **hand-written on the OLD stack
(Kameo actors + signal-frame), and the strict triad-engine separation is
ABSENT in every one of them.** None of them carries a `SemaEngine`,
`NexusEngine`, or `SignalEngine` (verified by grep across all five
`src/` trees: zero matches except mind's incidental
`SemaEngine(#[from] sema_engine::Error)` error variant in
`mind/src/error.rs:54`, which is the storage-kernel error type, not a
triad engine). By contrast the schema-derived `spirit` pilot DOES carry
all three (`spirit/src/store.rs`, `spirit/src/nexus.rs`,
`spirit/src/engine.rs`).

The old-stack architecture partitions concerns by **Kameo actor / module**,
not by **three engines**. State, decision, and communication are spread
across a dozen-plus fine-grained actors per daemon, and in several places
all three concerns co-locate in a single actor method or file. This is
not a leak to be patched — it is a different architecture. The fix is the
schema-derivation cutover, which is out of scope for a code fix and is
surfaced below as a per-component cutover concept.

A nuance worth recording: **persona-spirit is the closest of the five**
to the triad shape (it already runs a recognizable decision loop via the
`signal-executor` `Executor`/`Lowering`/`CommandExecutor`/`ObserverSet`
framework, and its trace vocabulary already names `SEMA_WRITER`,
`SEMA_OBSERVER`, `SIGNAL_EXECUTOR`). It is the natural first cutover
target. It is still ABSENT on strict separation because the three
concerns are not consolidated into three owning engine types — see below.

## Per-component characterization

### persona-spirit (production Spirit)

Architecture: `SpiritRoot` apex Kameo actor
(`persona-spirit/src/actors/root.rs:23`) supervises ~13 fine-grained
planes: `classifier`, `clock`, `decoder`, `dispatch`, `ingress`,
`owner`, `pipeline`, `policy`, `reply`, `state`, `store`,
`subscription`, `trace` (`persona-spirit/src/actors/mod.rs`).

- **State** is owned by `RecordStore` (`actors/store.rs:18`, holds a
  `SpiritStore` redb handle) AND `StatePlane` (`actors/state.rs`, in-memory
  presence/questions) — i.e. durable state is split across two actors, not
  one SEMA engine.
- **Decisions** are spread: the `signal-executor` `Executor` drives a real
  decision loop inside `DispatchPhase` (`actors/dispatch.rs:99-126`,
  `SpiritCommandExecutor` lowering operations to commands) — this is the
  Nexus-shaped part — BUT the **version-handover state machine
  (accept / reject / schema-validate / commit-sequence checks) lives
  directly in the root actor's `submit_upgrade_request` method**
  (`actors/root.rs:221-388`), interleaving decision logic with state reads
  (`store::ReadHandoverMarker`, `store::CaptureEntry`) and reply
  construction. That single method is the clearest three-concerns-in-one
  violation in this component.
- **Communication** is the decoder/encoder (`decoder.rs`, `reply.rs`) plus
  the daemon transport in `bin/persona-spirit-daemon.rs` — separate again,
  not a Signal engine.

Verdict: ABSENT. Decisions are NOT all in one Nexus engine (split between
the executor in dispatch and the handover machine in root); durable state
is NOT all in one SEMA engine (store + state planes); comms is NOT one
Signal engine. Closest of the five to triad shape, but still partitioned
by actor rather than by three engines.

### mind (central Persona state component)

Architecture: `MindRoot` apex actor (`mind/src/actors/root.rs:11`)
supervises `ingress`, `dispatch`, `domain`, `view`, `reply`,
`subscription`, `choreography`, and a `store` SUBTREE
(`mind/src/actors/store/mod.rs`: `StoreSupervisor` over `MemoryStore`,
`GraphStore`, `StoreKernel`, `persistence`, `write_trace`).

- **State** is split across the whole `store/` subtree — `MemoryStore`
  (work tables on the `sema` kernel) and `GraphStore` (typed
  Thought/Relation records on `sema-engine`). Durable state lives in
  multiple actors, not one SEMA engine. mind does correctly consume the
  `sema-engine` library (good — that is the storage kernel), but it wraps
  it in Kameo store actors rather than a single SEMA engine.
- **Decisions** live in `DispatchPhase` (`actors/dispatch.rs:45-77`,
  request-type routing) and `DomainPhase`, with a separate
  `ChoreographyAdjudicator` (`actors/choreography.rs`) making channel
  choreography decisions — decision-making is in at least three actors,
  not one Nexus engine.
- **Communication** is the `envelope`/`transport` layer plus daemon wire
  (`mind/src/transport.rs`, `mind/src/main.rs`) — separate.

Verdict: ABSENT. Decision-making spread across dispatch + domain +
choreography; state spread across the store subtree; comms in
transport/main. Partitioned by actor, not by three engines.

### persona (engine-management daemon, apex)

Architecture: host-level manager. `ManagerStore` is a **Kameo actor that
IS the redb store** (`persona/src/manager_store.rs:1-30`, opens `sema`
tables `manager.engine-records`, `manager.engine-events`, etc.) — durable
state lives INSIDE an actor. `engine.rs` mixes path/layout policy with
component-launch decisions (`PersonaDaemonPaths`,
`ResolvedComponentCommands`). `transport.rs` is the comms boundary
(`UnixListener`, length-prefixed `signal-persona` frames) but it directly
imports and drives `EngineManager`, `ManagerStore`, `EngineSupervisor`,
`UnitController` (`persona/src/transport.rs:18-25`) — i.e. the comms file
reaches straight into state and decisions.

- **State**: `ManagerStore` actor (redb-in-actor).
- **Decisions**: `EngineManager` (`manager.rs`), `EngineSupervisor`
  (`supervisor.rs`), launch/upgrade policy (`engine.rs`, `upgrade.rs`).
- **Communication**: `transport.rs` (`UnixListener` + frame protocol),
  `bin/persona_daemon.rs`, plus a fleet of `bin/wire_*.rs` helpers.

Verdict: ABSENT. State-in-actor, decisions spread across
manager/supervisor/launch, comms in transport reaching into both. This
is the apex integration daemon and is the most entangled of the five —
its job (host-level supervision of OTHER engines) does not map onto a
single component triad at all; it is a manager of triads.

### terminal (Persona-facing terminal owner)

Architecture: split between CLI-shaped request structs and a Kameo
supervisor. State owner is `TerminalTables` (`terminal/src/tables.rs`,
`sema` redb: `sessions`, `delivery_attempts`, `terminal_events`,
`viewer_attachments`, `session_health`, `session_archive`). Critically,
`registry.rs` mixes state reads with CLI decision logic in one struct:
`SessionListRequest::run` (`terminal/src/registry.rs:22-29`) directly
calls `TerminalTables::open(...).sessions()` and formats output — state
access and request-handling in the same method. `socket.rs` is the comms
primitive (`SocketMode`, `UnixListener` permissions). `supervisor.rs`
owns the `terminal-cell` actor lifecycle; `signal_control.rs` /
`signal_cli.rs` own the Signal adapter.

- **State**: `TerminalTables` (redb), read directly from request structs.
- **Decisions**: viewer-adapter policy, session resolution
  (`registry.rs`, `supervisor.rs`, `capture_validator.rs`).
- **Communication**: `socket.rs`, `signal_control.rs`, `signal_cli.rs`,
  `bin/terminal-daemon.rs`.

Verdict: ABSENT. Durable state read directly inside request/decision code
(`registry.rs`); decisions spread across registry/supervisor/validator;
comms in socket/signal modules. Partitioned by module, not by three
engines.

### router (delivery reducer + pending-delivery state)

The most explicit three-concerns-in-one-place case. `router/src/router.rs`
is one file that:

- **binds the socket and runs the frame protocol** —
  `use std::os::unix::net::{UnixListener, UnixStream}` (`router.rs:4`),
  `RouterDaemon::bind_listener` → `UnixListener::bind(&self.socket)`
  (`router.rs:161-166`), plus full inline `signal-message` /
  `signal-router` frame decode/encode (the file imports the entire
  `signal_message` and `signal_router` vocabularies, `router.rs:15-38`);
- **opens the redb store** — `RouterTables::open(...)` in
  `RouterDaemon::from_configuration` (`router.rs:88`) and again at
  `router.rs:141`; `RouterTables` wraps `sema` (`router/src/tables.rs`:
  tables `channels`, `adjudication_pending`, `messages`,
  `delivery_attempts`, `delivery_results`);
- **makes the routing decisions** — constructs and drives
  `RouterRoot`, `ChannelAuthority`, `MindAdjudicationOutbox`
  (`router.rs:653-732, 926-944`), where channel admission
  (`ChannelDecision`, `CheckChannel`) and adjudication live.

Worse for the SEMA-isolation rule: the durable `RouterTables` handle is
**threaded INTO the decision actor** — `ChannelAuthority::with_tables(tables)`
(`router.rs:701`) and `RouterRoot { tables }` (`router.rs:932`) — so state
and decisions are owned by the same actors. There is no SEMA boundary at
all; redb lives inside the channel-decision actor.

Verdict: ABSENT, and the most concentrated violation. One file
(`router.rs`) holds all three concerns; state is co-owned by the decision
actor.

## Why these are BLOCKED, not fixable in place

The strict separation cannot be reached by patching these daemons,
because the old-stack architecture is **partitioned along a different
axis** than the triad demands:

1. The unit of partition is the **Kameo actor** (or a CLI request
   struct / module), not the **engine**. There are ~13 actors in
   persona-spirit, a store subtree plus choreography in mind, a
   manager/supervisor/store fleet in persona. Collapsing N actors into 3
   engines is a re-architecture, not a refactor.

2. **State is co-owned with decisions.** In router, `RouterTables` lives
   inside `ChannelAuthority`/`RouterRoot`; in persona, `ManagerStore` IS
   the store actor. Extracting a SEMA engine means breaking every actor
   that currently holds a redb handle and re-routing its reads/writes
   through a single owning engine — that changes the actor graph.

3. **Decisions are co-located with communication.** persona's
   `transport.rs` reaches straight into `EngineManager`/`ManagerStore`;
   persona-spirit's root `submit_upgrade_request` runs a handover state
   machine inline with store reads and reply construction; router's
   `router.rs` decodes frames and makes channel decisions in the same
   file. There is no seam to cut along; the seam has to be introduced by
   re-deriving the daemon.

4. **The triad shape in the pilot is schema-EMITTED, not hand-written.**
   The `spirit` pilot's `SemaEngine`/`NexusEngine`/`SignalEngine` are
   produced by the schema-derivation chain (`schema-next` lowering +
   `schema-rust-next` emission over `schema/spirit.schema`). Hand-editing
   an old-stack daemon toward that shape produces a one-off that diverges
   from the emitter and has to be thrown away at cutover. Patching now is
   negative work.

For these reasons every component in this slice is
`action = blocked-needs-concept`. The unblock is the cutover, captured as
concepts below. Per the slice instructions, no old-stack daemon was
rewritten toward the triad pattern (that is a cutover, not a fix), and no
`next` branch was created — this slice is READ-ONLY.

## Cutover concepts (the unblock)

The general unblock is the same for all five and matches what already
worked for the `spirit` pilot: **author a `<component>.schema`, lower it
through `schema-next`, emit Rust via `schema-rust-next`, and stand the
component up as three schema-emitted engines** (`SemaEngine` on the
component `Store`, `NexusEngine` on the component `Nexus`, `SignalEngine`
on the component `SignalActor`) wired by thin scaffolding. The
component-specific concepts below name what each one needs.

The ordering recommendation: **persona-spirit first** (it already runs a
real decision loop and uses the `signal-executor` framework, so its
Nexus engine is the smallest delta), then **router** (smallest state +
clearest existing contract surface in `signal-router`/`signal-message`),
then **mind** (already on `sema-engine`, so its SEMA engine is close),
then **terminal**, and **persona last** (it is a manager-of-engines, not
a single component triad — its cutover question is different).
