# Introspect area — current state, move-forward work, stability verdicts

*System-designer area-mapping report for the engine-forward exploration.
Area: the introspector — supervised inspection-plane component. Repos:
`introspect` (daemon + CLI), `signal-introspect` (wire contract),
`signal-router` (router observation wire contract that introspect consumes).
Read-only. All citations verified against source at checkout HEAD on
2026-06-05.*

Target state (Spirit Decision `mazv`): a live ORCHESTRATED system —
`persona` (the manager/supervisor) runs and supervises the introspector,
the schema daemon, and the other triad components together. This report
maps how close the introspect area is to being a supervised, live
observer of real peer daemons, and which work is safe to do now without
porting onto shifting foundation.

## 1. Current state — landed vs scaffold vs doc-only

### 1.1 What is genuinely landed and building

- **`introspect` daemon compiles clean and its tests build.** `cargo
  build` and `cargo test --no-run` both succeed (verified 2026-06-05).
  The daemon binds a Unix socket, applies the supplied socket mode,
  spawns the Kameo `IntrospectionRoot` actor tree, and serves
  `signal-introspect` frames. Evidence: `introspect/src/daemon.rs`
  `IntrospectionDaemon::bind`/`run`/`serve_forever` (lines 137-233);
  `src/bin/introspect_daemon.rs` decodes typed
  `IntrospectDaemonConfiguration` from argv via
  `nota_config::ConfigurationSource::from_argv` (no flags, single
  NOTA/rkyv arg — compliant with the single-argument rule).

- **The Kameo actor root is real, not a stub.** `IntrospectionRoot`
  (`src/runtime.rs:43-214`) spawns seven children: `TargetDirectory`,
  `QueryPlanner`, `ManagerClient`, `RouterClient`, `TerminalClient`,
  `IntrospectionStore`, `NotaProjection`. Graceful shutdown fans out to
  all children (`stop_children`, lines 171-187). Actor-discipline truth
  tests exist (`tests/actor_discipline_truth.rs`: no-ZST-actors,
  no-shared-locks).

- **`RouterClient` is a genuinely wired live client.** It opens a
  `UnixStream` to the configured router socket, sends a real
  `RouterRequest::Summary` inside a length-prefixed `RouterFrame`,
  parses the typed `RouterReply::Summary`, and composes the result into
  `PrototypeWitness.router_seen` (`src/runtime.rs:374-511`). This is the
  one peer relationship that actually crosses a daemon boundary today.

- **The router daemon serves the matching observation contract.**
  `router/src/observation.rs:38` — `RouterObservationPlane` answers
  `RouterRequest::Summary` with `RouterReply::Summary(RouterSummary)`.
  `router/src/router.rs:322` routes `RouterObservation(SignalRouterRequest)`
  on the router socket. So the wire path introspect→router is real on
  both ends, contract-aligned, and would work against a live router
  daemon — NOT only against a test fixture.

- **`introspect.redb` consumed through `sema-engine`.** `src/store.rs`:
  `IntrospectionStore::open` (lines 62-75) uses `Engine::open` +
  `register_table`; observations persist via `Engine::assert`
  (`record_observation`, lines 77-85); delivery-trace events range-query
  by the four-field `DeliveryTraceKey` join prefix
  (`delivery_trace`, lines 109-128; key builders 325-346). No direct
  `redb::Database::open` and no `sema::open_with_schema` in this repo —
  matches the ARCHITECTURE non-ownership constraint.

- **Supervision listener is real.** `src/supervision.rs`:
  `SupervisionListener::spawn` binds the supervision socket, applies the
  mode, and answers the `signal-engine-management` protocol —
  `Announce`→`Identified`, `ReadinessStatus`→`Ready`,
  `HealthStatus`→`HealthReport`, `Stop`→`StopAcknowledged`
  (`SupervisionPhase::reply`, lines 109-136). So introspect already
  speaks the supervisor handshake `persona` expects.

- **Persona ALREADY knows how to supervise introspect.**
  `persona/src/engine.rs:332-340` — `EngineComponent::Introspect` is a
  registered component. `persona/src/direct_process.rs:496` +
  `write_introspect_daemon_configuration_file` (lines 663-700) resolve
  the Router and Terminal peer sockets and write a typed
  `IntrospectDaemonConfiguration` file passed as argv. Persona's own
  tests assert the orchestration shape:
  `persona/tests/engine.rs:303-310` —
  `prototype_supervised_components()` includes Introspect and
  `operational_delivery_components()` does NOT (introspect supervised
  but out of the delivery path, exactly per the architecture); line 433
  asserts the introspect spawn-envelope carries a Router peer with an
  `introspect.sock` domain socket. **The orchestration scaffolding for
  introspect is materially in place on the persona side.**

### 1.2 What is scaffold / placeholder / doc-only

- **`ManagerClient` and `TerminalClient` are honest scaffolds.** They
  hold a socket `Option<PathBuf>` and supervise cleanly but have NO
  query logic — no `Message` impl that crosses the wire
  (`src/runtime.rs:333-358` Manager, `513-538` Terminal). `prototype_witness`
  hard-codes `manager_seen: None` and `terminal_seen: None`
  (`src/runtime.rs:100-106`). Confirmed by `tests/daemon.rs:120`
  (`router_seen == None` when no router socket) and
  `actor_runtime_truth.rs:141-142`.

- **`EngineSnapshot` / `ComponentSnapshot` replies are synthetic, not
  observed.** `handle_request` (`src/runtime.rs:114-132`) returns a
  hard-coded component list for `EngineSnapshot` and `readiness: None`
  for `ComponentSnapshot` — neither asks a peer. Only `PrototypeWitness`
  (via `RouterClient`) and `DeliveryTrace` (via the store) reach real
  state.

- **No push subscription anywhere.** Every observation today is a
  one-shot `Match`. The `Tap`/`Untap` subscriber side described at
  length in `signal-introspect/ARCHITECTURE.md` §"Subscriber side of the
  universal observer hook" is doc-only — no `Subscribe` wire variant
  exists (the `signal_channel!` block in `signal-introspect/src/lib.rs:297-315`
  carries only the four `Match` reads), no `Engine::subscribe` call
  exists in introspect, and the ARCHITECTURE itself states it is gated
  on `sema-engine` per-peer commit-then-emit semantics
  (`introspect/ARCHITECTURE.md:157-165`).

- **`DeliveryTrace` is populated only by direct typed ingress, never by
  peer Tap streams.** `RecordDeliveryTraceEvent` is handled by the root
  (`src/runtime.rs:254-271`) but nothing on the wire feeds it from
  router/terminal hops yet — an empty event vector is the normal state.

- **The CLI cannot reach the daemon on the production path.** The CLI
  (`src/command.rs:51-67`) only connects to a daemon if
  `PERSONA_INTROSPECT_SOCKET` / `PERSONA_SOCKET_PATH` env vars are set;
  otherwise it spins up an in-process root with EMPTY targets
  (`TargetSocketDirectory::empty()`), so the default `introspect` CLI
  invocation witnesses nothing live. There is no NOTA-arg path that
  points the CLI at the supervised daemon's socket.

- **The `schema/*.schema` files are concept stubs, not the driving
  source.** `introspect/schema/introspect.concept.schema` and
  `signal-introspect/schema/signal-introspect.concept.schema` are both
  `Status Concept`, `Version 0 1`, with a placeholder vocabulary
  (`Observe`/`Tap`/`Untap`, `Identifier (u64)`) that does NOT match the
  real wire types in `src/lib.rs`. They are forward-looking
  documentation, NOT the schema-derived build source. (Contrast the
  spirit pilot, where `schema/*.schema` builds `src/schema/*.rs`
  directly — introspect is not yet on that pipeline.)

### 1.3 The contract-migration debt (named in-tree, not done)

Both wire contracts still carry **Sema-class verb tags inside
`signal_channel!`** — the Layer-1 "drop the SignalVerb wrappers"
migration is OWED, not done. `signal-introspect/src/lib.rs:299-303`:
`Match EngineSnapshot(...)`, `Match ComponentSnapshot(...)`, etc.
`signal-router/src/lib.rs:289-293`: `Match Summary(...)`, etc. Both
ARCHITECTURE files carry a "MUST IMPLEMENT — three-layer migration"
block (signal-introspect lines 13-72; signal-router lines 20-74) and
signal-introspect's INTENT explicitly names this a "cleanup-track
holdover ... owed, not optional" (INTENT.md:63-67). The mandatory
`Tap`/`Untap` `observable { … }` block is likewise specified but absent.

### 1.4 Orchestration-drift finding (load-bearing)

**Persona and introspect-daemon compile against two different revisions
of the introspect contract.** `persona/Cargo.toml:35` depends on
`signal-persona-introspect` (the pre-rename name), and `cargo tree`
resolves it to commit `cfc1c55a` — which in the renamed repo's log is
the OLD "adopt origin identifiers" commit, predating `b8fdf67 rename
from signal-persona-introspect`. The `introspect` daemon depends on
`signal-introspect` at the post-rename `main` (`152fc0e`). The
`IntrospectDaemonConfiguration` field shape is identical across the two
revisions today, so the rkyv-encoded config file persona writes will
still decode — but this is exactly the orchestration-blocking drift that
must close before "persona supervises introspect live" is trustworthy.
Persona's source also still references `signal_persona_introspect::` and
the spawn binary name `persona-introspect-daemon`
(`persona/tests/engine.rs:59`), both stale.

## 2. Move-forward work items (ordered)

Ordering reflects dependency and leverage toward the live-orchestrated
target. Sizes are rough engineering estimates.

1. **Realign persona onto the renamed `signal-introspect` contract and
   binary name.** Repo: `persona` (`Cargo.toml:35`, `src/direct_process.rs`
   `signal_persona_introspect::` references, `tests/engine.rs:59`
   `persona-introspect-daemon`→`introspect-daemon`). Size: S. Depends on:
   nothing (rename already landed in the contract + daemon). This is the
   single concrete break standing between "persona spawn-config is
   written" and "persona spawns the SAME daemon the contract describes."

2. **Stand up an end-to-end orchestrated witness test: persona spawns
   introspect + router, introspect queries the live router.** Repo:
   `persona` (`tests/`), consuming real `introspect-daemon` and
   `router-daemon` binaries. Size: M. Depends on: item 1. Today the
   live-router witness (`introspect/tests/actor_runtime_truth.rs:69`)
   uses a hand-rolled fake router socket; the orchestrated target needs
   the real router daemon spawned by persona. This is the test that
   proves Decision `mazv` for this area.

3. **Wire `ManagerClient` to the persona supervision/management
   contract so `manager_seen` becomes a real observation.** Repo:
   `introspect` (`src/runtime.rs:333-358`), consuming
   `signal-engine-management` (already a dependency). Size: M. Depends
   on: deciding the manager observation read (readiness query already
   exists in the supervision protocol — introspect can ask persona for
   component readiness the same way it asks router for Summary).

4. **Add the `IntrospectDaemonConfiguration` CLI/daemon-socket discovery
   so the `introspect` CLI reaches the supervised daemon over NOTA arg,
   not env vars.** Repo: `introspect` (`src/command.rs`), contract field
   in `signal-introspect`. Size: S-M. Depends on: item 1. Removes the
   env-var fallback (`PERSONA_INTROSPECT_SOCKET`) in favour of a typed
   NOTA pointer, aligning with the single-argument rule.

5. **Land the Layer-1 contract migration: drop the `Match` Sema-verb
   tags, switch to bare contract-local `Observe` verbs, add the
   mandatory `observable { Tap/Untap }` block.** Repos:
   `signal-introspect` and `signal-router` (`src/lib.rs` `signal_channel!`),
   then update consumers in `introspect` and `router`. Size: M-L.
   Depends on: the `signal-frame` macro supporting the bare-verb +
   `observable` shape (the macro is the foundation gate here).

6. **Implement push subscriptions (Tap/Untap + `Engine::subscribe`) so
   `DeliveryTrace` and per-peer readiness arrive as deltas, not
   one-shots.** Repos: `introspect` (`src/runtime.rs`, `src/store.rs`),
   `signal-introspect` + peer contracts (new `Subscribe`/`Retract`
   variants). Size: L. Depends on: item 5 AND `sema-engine` per-peer
   commit-then-emit semantics (named blocker in
   `introspect/ARCHITECTURE.md:157-165`).

7. **Bring introspect onto the schema-derived pipeline (replace the
   concept stub with a real `schema/*.schema` that builds
   `src/schema/*.rs`).** Repos: `signal-introspect`, `introspect`. Size:
   L. Depends on: the structural-macro / schema-derive pipeline
   stabilising for contracts (it has landed for the spirit pilot but not
   generalised to these contracts yet).

8. **Extract the introspect daemon's boilerplate onto the generic triad
   runner once it exists (intent `7ca4`/`rpr5`).** Repo: `introspect`
   (the `IntrospectionDaemon`/`BoundIntrospectionDaemon` bind/serve loop
   in `src/daemon.rs`, the supervision listener, the frame codecs).
   Size: M (once the runner exists). Depends on: the generic
   Signal/Nexus/SEMA runner being extracted — which does NOT exist yet
   (no `signal-runner`/`triad-runner`/`runner` repo in the checkout).

## 3. Foundation-stability verdict per item

The load-bearing column. "Stable foundation under it" is justified
against: the wire contracts (introspect↔router is contract-aligned and
building on both ends), the supervisor handshake (`signal-engine-management`,
already implemented in introspect), asschema-removal-done, and the
plane-separation (contract crates carry no runtime; daemon carries no
peer redb). "Shifting foundation" is named explicitly where it blocks.

1. **Realign persona onto renamed contract — [SAFE-NOW].** The rename
   is COMPLETE in the contract and the daemon; the package name and
   `IntrospectDaemonConfiguration` shape are stable. Fixing persona's
   pin is pure catch-up to a landed change — there is no foundation
   under it still moving. Not rework: it deletes drift rather than
   creating a structure that a later change would undo.

2. **End-to-end orchestrated witness test — [SAFE-NOW].** Both wire ends
   are stable and contract-aligned (verified: `RouterObservationPlane`
   answers `Summary`; `RouterClient` sends `Summary`). The supervisor
   handshake is implemented. The spawn-envelope wiring exists in
   persona. A test asserting the live path is locking in behaviour that
   already works against real daemons; it cannot be invalidated by the
   pending Layer-1 verb migration because the test asserts decoded typed
   replies, not wire-verb spelling.

3. **Wire `ManagerClient` — [PREP].** The supervision readiness query is
   stable and already implemented on introspect's own listener, so the
   shape of the call is knowable now. Mark PREP not SAFE-NOW because the
   exact manager-observation read surface (do we read via the
   management contract's readiness query, or a future introspect-owned
   command?) is a Layer-2 decision that interacts with item 5; structure
   the client now, finalise the verb after the migration.

4. **CLI NOTA socket discovery — [PREP].** The typed-config + single-arg
   discipline is stable, but the exact discovery field belongs to the
   same contract surface touched by item 5; add the daemon-socket
   pointer as a typed field now, finalise alongside the verb migration
   so it is not respelled twice.

5. **Layer-1 contract migration (bare verbs + `observable`) — [WAIT].**
   Blocker: the `signal-frame` macro must support the bare contract-local
   verb form AND the `observable { Tap/Untap }` injection. This is named
   as MUST-IMPLEMENT across multiple contracts and is a cross-cutting
   macro/foundation change still in flight. Doing it now in one contract
   risks divergence from the final macro shape — this is the canonical
   "don't port onto sand" item. Wait for the macro decision.

6. **Push subscriptions — [WAIT].** Two blockers, both explicitly named
   in-tree: (a) the Layer-1 `observable`/`Tap` macro surface (item 5),
   and (b) `sema-engine` per-peer commit-then-emit semantics
   (`introspect/ARCHITECTURE.md:157-165`,
   `signal-introspect/ARCHITECTURE.md:90-95`). Until both land, any
   subscription code is built against an undefined emit contract.

7. **Schema-derived pipeline for introspect — [WAIT].** Blocker: the
   structural-macro/schema-derive pipeline has landed for the spirit
   pilot only; generalising `schema/*.schema → src/schema/*.rs` to these
   contracts is not yet a stable, reusable path. The current
   `schema/*.schema` files are concept stubs that do not match the real
   types — porting onto them now would be porting onto sand. (Note:
   asschema removal IS done, so the OLD pipeline is gone; the NEW one is
   not yet general — this item waits on generalisation, not on asschema.)

8. **Extract onto generic triad runner — [WAIT].** Blocker: the generic
   runner does not exist yet (no runner repo in checkout). The
   intent (`7ca4`/`rpr5`) is to extract it NOW, but the extraction
   target is itself the upstream work; introspect cannot plug into a
   runner that has not been authored. introspect's current bind/serve
   loop is a CLEAN, self-contained candidate to MIGRATE later — keep it
   that way (do not invest in bespoke runtime abstractions that the
   runner will replace). This is PREP-adjacent: the right move now is to
   NOT build introspect-specific runner infrastructure, leaving the
   boilerplate thin and replaceable.

## 4. The one highest-leverage first step

**Item 1 + Item 2 together: realign persona onto the renamed
`signal-introspect` contract, then write the orchestrated witness test
where persona spawns the real `introspect-daemon` and `router-daemon`
and introspect queries the live router's `Summary`.**

Justification: everything needed for a live, supervised introspector
that observes a real peer daemon is ALREADY built and building — the
Kameo root, the real `RouterClient`, the router's matching
`RouterObservationPlane`, the supervision handshake, and persona's
spawn-envelope + typed-config writer. The ONLY thing standing between
"all the pieces exist" and "the orchestrated system demonstrably runs"
is the revision-drift between persona's pinned contract (`cfc1c55a`) and
the renamed daemon contract (`152fc0e`), plus the absence of a test that
exercises the full persona→introspect→router path with real binaries.
This is the lowest-risk, highest-truth move: it ports nothing onto
shifting foundation (it consumes only the stable wire contracts and the
implemented supervisor handshake), it deletes drift rather than adding
structure, and it converts the introspect area from "proven in-tree" to
"demonstrably live under persona" — which is precisely Decision `mazv`
for this area. The verb migration, subscriptions, schema-derive, and
runner extraction (all [WAIT]) sit downstream of moving foundation and
must not be started first.
