# 144 — Persona-introspect design (current-state review)

*Kind: Review · Topic: persona-introspect · Date: 2026-05-22*

*Refresh of the persona-introspect design against the current
three-layer model, the Tap/Untap discipline, and the
signal-frame/signal-sema/signal-executor reshape. Carries forward
the load-bearing decisions from the prior design (which retires
in the same commit) and integrates the changes that landed since
it was written.*

## 0 · TL;DR

Persona-introspect is the cross-component observation aggregator
for the persona stack. The architectural core hasn't moved: the
central `signal-persona-introspect` contract **wraps** component-
owned observation replies; it does NOT define component schemas.
What HAS moved since the prior design:

- Component observability is now the workspace-mandatory **Tap /
  Untap** + **observable block** mechanism (intent affirmed
  2026-05-20T02:00:00Z); every persona component contract carries
  it, even if fanout is deferred.
- The wire substrate is `signal-frame` (renamed from
  `signal-core`); typed `Operation` / `Reply` / `Event` records
  travel through the `signal_channel!` macro's clean-output
  emission (post `primary-77hh`).
- Component execution flows through `signal-executor` — `Lowering`
  + `CommandExecutor` + `ObserverChannel` — with the daemon's
  effects projecting to `SemaObservation` via `ToSemaOutcome`.
- Persona-introspect is **the prerequisite consumer** for
  Tap/Untap live fanout; until it lands, spirit (and others)
  carry the placeholder `RequestUnimplemented` on Tap.

The terminal-first, then router sequencing still holds. The
implementation-readiness verdict from the prior design is no
longer current; the new substrate (signal-executor, observable
block) reshapes the package breakdown — see §3.

## 1 · Where persona-introspect sits today

Per the recent audit (`reports/second-designer/133-persona-introspect-triad-audit-2026-05-21.md`):

- `signal-persona-introspect` exists as the central wrapper
  contract. Still on `signal-core` with universal-verb shape;
  needs migration to `signal-frame` + contract-local verbs.
- `persona-introspect` daemon exists; not on `signal-executor`.
- `owner-signal-persona-introspect` does not exist; /133 §3
  proposes the shape (`Configure(Configuration)` +
  `Inspect(Inspection)`).
- Limited boundary creep: `IntrospectionTarget` duplicates
  `signal_persona::ComponentKind`; `DeliveryTraceStatus`
  duplicates `signal_persona_router::RouterDeliveryStatus`.
  Both should consolidate in `signal-persona-auth`.

The migration is bead `primary-li7a` (P1) — see §3.

## 2 · The core design (refreshed)

Six decisions carry forward from the prior design, each refreshed
against current state.

### D1 · First component is terminal, then router

Unchanged in substance. Terminal owns the richest observation
vocabulary (sessions, delivery attempts, terminal events,
viewer attachments, session health, session archive). It's the
best first proof that the cross-component observation shape
works. Router follows because router observations are the
fastest path to proving message-delivery traces.

Refreshed framing: both terminal and router need their working
contracts migrated to signal-frame + observable block + Tap/Untap
before persona-introspect consumes them. The cross-component
class-level observation stream (`OperationReceived` /
`EffectEmitted` carrying `SemaObservation`) is what introspect
subscribes to via Tap; rich domain data flows through each
component's own `Observe` query path.

### D2 · Central contract wraps, doesn't define

Unchanged. `signal-persona-introspect` carries `ComponentObservations(...)`
operation roots whose payloads wrap the component-owned observation
replies. The introspect contract does NOT carry fields from each
component's schema; it carries references.

```text
;; In signal-persona-introspect:
operation ObserveComponent(ComponentObservationQuery) opens DomainStream
operation Watch(ComponentSubscription) opens DomainStream
operation Unwatch(SubscriptionToken)

reply Reply
    ComponentObservations(ComponentObservationsBatch)
    SubscriptionOpened(SubscriptionOpened)
    SubscriptionRetracted(SubscriptionRetracted)
    RequestUnimplemented(RequestUnimplemented)
```

`ComponentObservationsBatch` is a tagged union over component-
owned reply types (terminal's, router's, etc.). Each component
owns its observation schema in its own working contract.

### D3 · Target-specific queries

Unchanged. `ComponentObservationQuery` is a closed sum over
component-owned query types:

```text
enum ComponentObservationQuery
    Terminal(signal_persona_terminal::Observation)
    Router(signal_persona_router::Observation)
    Mind(signal_persona_mind::Observation)
    ;; ... one variant per component
```

A universal `ObservationFilter` would underspecify each domain
and become a bag of optional fields. Each component knows what
kinds and indexes it supports; the sum makes that visible at the
type system.

### D4 · Component-minted observation sequences (refreshed against Sema)

The prior design specified component-minted monotone observation
sequences. Refresh: this is now the same surface as
`SemaObservation` plus a component-local sequence number on the
typed reply. Each component's `Observe(Q)` reply carries:

- The typed component-owned records (e.g., `TerminalEvent`,
  `MessageTrace`).
- A `from_sequence` / `through_sequence` pair naming the range
  the reply covers.
- Optional `since_time` / `through_time` for time-window queries
  (still needs the secondary index discipline from §D5).

The Sema observation stream (via Tap) is the cross-component
class-level surface; the per-component `Observe` query path is
the rich data surface. Introspect uses both:

- **Tap**: subscribe to `OperationReceived` / `EffectEmitted`
  from peers, get class-level traffic (operation kind + sema
  outcome). Lightweight, real-time, for the introspection dashboard.
- **Observe**: ask peers for typed records by query, get rich
  domain data. Heavier, on-demand, for trace correlation.

### D5 · Time windows via secondary indexes

Unchanged. A component supporting time-window queries writes a
time-keyed index table alongside the primary observation record,
in the same Sema transaction. The query layer reads the index to
find sequence boundaries, then reads the primary records by
sequence range.

This avoids walking the full primary table for every time query
and keeps the time-window cost proportional to the result size.

### D6 · Subscriptions: Tap/Untap, deferred fanout

The prior design said "no subscriptions in V1". Refresh: Tap and
Untap are now **mandatory** in every persona component contract
(intent affirmed 2026-05-20T02:00:00Z), but **fanout is
deferred** until persona-introspect lands. Today spirit (and the
other migrated components) return `RequestUnimplemented` on Tap;
the contract surface is there but the subscriber side isn't wired.

When persona-introspect lands as a real Tap subscriber, the
deferred fanout becomes load-bearing: each persona daemon's
`SpiritObserverRecorder`-equivalent gets a real
`FrameObserverBridge` composition driving subscriber sockets to
introspect.

Per `intent/persona.nota` 2026-05-20T20:00:00Z, this deferral is
intentional: Tap fanout doesn't need to ship before persona-
introspect because there's no consumer until introspect lands.

## 3 · Implementation packages (refreshed)

Two packages, sequenced by /133's audit findings + the broader
migration order in `/150`.

### Package 1 — signal-persona-introspect on the current substrate

Migrate the central wrapper contract to current foundation:

- Drop `signal-core` dependency; depend on `signal-frame`.
- Replace universal-verb shape (`Match Verb(Payload)`) with
  contract-local verbs (`ObserveComponent`, `Watch`, `Unwatch`,
  `Tap`, `Untap`).
- Lift the closed sum `ComponentObservationQuery` per D3 (one
  variant per known component).
- Add the `observable` block.
- Drop `Introspection*` ancestry prefixes (use `Query`, `Batch`,
  `Sequence` inside the crate; the crate name is the namespace).
- Drop the redundant `scope` field (intent on the duplicated
  shape; consolidate via `signal-persona-auth`).
- Add `RequestUnimplemented` carrying only `reason`.

Falsifiable witnesses per /133:

- `signal-persona-introspect` round-trips operation + reply for
  each component variant.
- Contract carries the `observable` block.
- Contract does NOT carry fields from terminal/router/etc.
  schemas (only wraps).

### Package 2 — persona-introspect daemon on signal-executor

The daemon's request path goes through `signal-executor`:

- Define `IntrospectCommand` / `IntrospectEffect` in
  `persona-introspect/src/`.
- `impl ToSemaOperation for IntrospectCommand` (likely all
  `Match` — introspect's commands are reads).
- `impl ToSemaOutcome for IntrospectEffect`.
- `impl Lowering for IntrospectLowering` mapping
  `IntrospectRequest` → `OperationPlan<IntrospectCommand>`.
- `impl CommandExecutor` over the actor mesh that talks to
  each peer component's daemon socket.
- Wire the daemon's socket actor through `Executor::execute`.

Plus introspect-specific runtime work:

- Add typed component-contract dependencies (terminal, router,
  ...) so the daemon can decode each peer's reply types.
- Implement per-peer clients (`TerminalClient`,
  `RouterClient`, ...) that hold typed sockets, codecs, and
  failure handling.
- The `QueryPlanner` routes `ComponentObservationQuery` variants
  to the right peer client.

Falsifiable witnesses:

- Daemon depends on `signal-executor`.
- `IntrospectCommand` projects to `SemaOperation`.
- `IntrospectEffect` projects to `SemaOutcome`.
- Daemon does NOT open any peer's redb (introspect inspects via
  signal sockets only).

### Package 3 — Tap subscriber wiring (defers until both peers ship Tap fanout)

Once a peer (start with spirit, since it's the migration template)
ships real Tap subscriber delivery (replacing the placeholder
`SpiritObserverRecorder` with a `FrameObserverBridge`
composition), introspect's `Watch` opens subscriptions on each
peer's working socket and aggregates the resulting
`SemaObservation` stream.

This package depends on:

- The per-peer Tap implementations (today: only placeholder).
- The cross-peer aggregation logic (introspect-side).
- An introspection-dashboard surface (CLI or future UI) for the
  psyche to view.

### Package 4 — owner contract

Per /133 §3 proposal, `owner-signal-persona-introspect` carries:

```text
operation Configure(Configuration)
    ;; retention, time-window defaults, peer endpoints
operation Inspect(Inspection)
    ;; policy read-back
```

No lifecycle verbs in v1 (introspect is engine-manager-supervised;
lifecycle enters out-of-band via spawn envelope).

## 4 · Witnesses

For Package 1 (contract):

- `signal_persona_introspect_uses_signal_frame_not_signal_core`
- `component_observations_wrap_each_component_reply_type`
- `central_contract_does_not_define_component_rows`
- `introspect_observable_block_emits_operation_and_effect_events`
- `request_unimplemented_carries_only_reason`

For Package 2 (daemon):

- `persona_introspect_uses_signal_executor`
- `introspect_command_projects_to_sema_operation`
- `introspect_effect_projects_to_sema_outcome`
- `introspect_daemon_opens_no_peer_redb`
- `terminal_client_decodes_terminal_observation_batch`
- `router_client_decodes_router_observation_batch`

For Package 3 (Tap):

- `introspect_watch_subscribes_to_peer_taps`
- `introspect_aggregates_sema_observations_across_peers`
- `peer_tap_disconnect_does_not_crash_introspect`

For Package 4 (owner):

- `owner_signal_persona_introspect_carries_configure_inspect`
- `owner_socket_rejects_working_channel_operations`

## 5 · What NOT to implement

Carried forward from the prior design, refreshed:

- A universal untyped observation filter (D3 forbids).
- Peer redb reads from `persona-introspect` (introspect inspects
  via sockets, not via filesystem).
- Raw transcript fanout (terminal-cell territory, not
  introspect's).
- Polling loops in introspect (push-not-pull discipline per
  `skills/push-not-pull.md`).
- Field-level runtime reflection (out of scope; record kinds
  are typed).
- A sibling `signal-persona-terminal-introspect` crate (D2
  forbids — terminal's introspect schema lives in
  `signal-persona-terminal`, not in a sibling crate).
- Duplicate component row structs in `signal-persona-introspect`
  (D2 forbids).

## 6 · Open questions

These are the persona-touch questions surfaced by /133 plus this
review's reshape.

- **Owner contract lifecycle verbs** — designer lean from /133:
  no, introspect is engine-manager-supervised. Confirm.
- **Default retention** — Configuration's `Retention` field:
  `KeepAllForever` / `BoundedBySequence` / `BoundedByByteSize`.
  /133 designer lean: `KeepAllForever` for the prototype.
- **Cognitive owner of introspect** — engine-manager or spirit?
  /133 designer lean: engine-manager (parallel to terminal /
  router / harness). The authority graph in
  `intent/persona.nota` 2026-05-19T15:30:00Z is explicit only
  down to router/harness/terminal; introspect isn't named.
- **First Tap subscriber pilot** — once Package 3 is ready,
  which peer ships real Tap fanout first? Designer lean: spirit
  (already the migration template; placeholder is the smallest
  delta to real).

## 7 · What this review supersedes

This Review supersedes `reports/second-designer/41-persona-introspect-implementation-ready-design.md`,
which retires in the same commit that lands this report.

The prior design's load-bearing substance carried forward:

- Terminal-first sequencing (still aligned; §2 D1).
- Central wrapper, not central schema (still aligned; §2 D2).
- Target-specific queries (still aligned; §2 D3).
- Component-minted observation sequences (now reframed against
  Sema observation stream; §2 D4).
- Time windows via secondary indexes (unchanged; §2 D5).
- No live subscriptions in V1 (now expressed as deferred Tap
  fanout; §2 D6).
- Implementation package breakdown (refreshed against
  signal-frame / signal-executor; §3).
- Falsifiable witnesses (refreshed names; §4).
- What-not-to-implement list (unchanged; §5).

What changed:

- `signal-core` → `signal-frame` rename absorbed.
- `signal-executor` exists; daemon path goes through it.
- `Tap` / `Untap` mandate absorbed; subscriptions are now
  contract-mandatory with fanout deferred.
- `observable` block + `SemaObservation` projection are the
  cross-component-class-level surface, distinct from per-
  component `Observe` query path.
- `owner-signal-persona-introspect` proposal from /133 added as
  Package 4.
- Boundary-creep findings (IntrospectionTarget,
  DeliveryTraceStatus) from /133 added to Package 1's cleanup.

## 8 · See also

- `reports/second-designer/133-persona-introspect-triad-audit-2026-05-21.md`
  — the current audit driving this Review.
- `reports/operator/150-triad-signal-sema-migration-current-state.md`
  — workspace-wide migration handoff that establishes the
  current substrate.
- `intent/persona.nota` 2026-05-20T02:00:00Z — Tap/Untap mandate
  for persona components.
- `intent/persona.nota` 2026-05-20T20:00:00Z — Tap fanout
  deferred until persona-introspect lands.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z —
  three-layer model (contract Operation / component Command /
  Sema classification).
- Bead `primary-li7a` (P1) — Migrate persona-introspect triad to
  current foundation. This Review's §3 packages map to that
  bead's work.

This Review retires when (a) Package 1 ships (the contract
migration), AND (b) Package 2 ships (the daemon on
signal-executor), OR (c) a successor Review supersedes after
intent moves again.
