# 41 - Persona-introspect implementation-ready design

Scope: close the missing design from
`reports/designer-assistant/40-persona-introspect-after-111-and-153.md`
so an operator can implement the first real introspection slice without
another architecture round trip.

## 0. Decisions

### D1 - First component

Implement **terminal first**, then router.

Reason: `signal-persona-terminal` already owns the richest component
observation vocabulary: sessions, delivery attempts, terminal events,
viewer attachments, session health, and session archive. That makes it
the best first proof that the general component-observation shape works.
Router follows immediately because router observations are the fastest
way to prove message-delivery traces.

### D2 - Central contract role

`signal-persona-introspect` wraps component-owned observation replies.
It does not define component row fields.

Allowed:

```rust
ComponentObservationResult::TerminalObservations(
    signal_persona_terminal::TerminalObservationBatch
)
```

Forbidden:

```rust
// Wrong home: these fields belong in signal-persona-terminal.
struct TerminalSessionObservation { ... }
```

### D3 - Query shape

Use **target-specific queries**, not one universal filter.

`ComponentObservations` should carry a closed selector whose variants
wrap the owning component contract's query:

```rust
pub enum ComponentObservationQuery {
    TerminalObservations(signal_persona_terminal::TerminalObservationQuery),
    TerminalSessionSnapshot(signal_persona_terminal::TerminalSessionSnapshotQuery),
    RouterObservations(signal_persona_router::RouterObservationQuery),
}
```

A universal `ObservationFilter` would either underspecify the domain or
become a bag of optional fields. Each component knows what kinds and
indexes it supports.

### D4 - Cursor shape

Use component-minted observation sequences. Do not call them redb
transaction ids.

Sema currently exposes typed `Table::iter` and `Table::range`, but it
does not expose a stable redb transaction identity. Each component
therefore mints a monotone observation sequence in its own write path.
Queries may use:

- `since_sequence`
- `through_sequence`
- `since_time`
- `through_time`

The reply includes both the lower and upper sequence bounds it actually
covered, so callers can detect truncation or a narrowed result:

- `from_sequence`
- `through_sequence`

### D5 - Time windows

Time-window queries are supported by explicit secondary indexes.

`Table::range` ranges over table keys. A component that wants "records
between two timestamps" must write a time-keyed index table with a
packed key:

```text
TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
```

The primary observation record and secondary index row must be written in
the same component Sema transaction.

### D6 - Subscriptions

Do not implement polling. V1 ships one-shot observations only.

Do not add a `SubscribeComponent` wire variant in this slice. A variant
that only returns `Unimplemented` gives every consumer contract debt with
no working feature. Live subscriptions land after a component has
commit-then-emit wiring: initial snapshot, then deltas.

### D7 - Schema/catalog introspection

Implement a modest `ListRecordKinds` surface, not field-level reflection.

V1 catalog entries name:

- target component;
- component contract crate;
- observation query kind;
- observation record kind;
- whether sequence range is supported;
- whether time range is supported;
- whether live subscription is supported.

Do not hand-maintain field schemas until the derive layer can generate
truthful descriptors.

## 1. Contract changes

### 1.1 `signal-persona-terminal`

Add a terminal-owned observation relation beside the existing terminal
control relation. The existing introspection records stay in
`src/introspection.rs`.

Add these types:

```rust
pub enum TerminalObservationKind {
    DeliveryAttempt,
    Event,
    ViewerAttachment,
    SessionHealthChange,
    SessionArchiveCommit,
}

pub struct TerminalObservationTimeRange {
    pub since: Option<signal_persona::TimestampNanos>,
    pub through: Option<signal_persona::TimestampNanos>,
}

pub struct TerminalObservationSequenceRange {
    pub since: Option<TerminalObservationSequence>,
    pub through: Option<TerminalObservationSequence>,
}

pub struct TerminalObservationQuery {
    pub kinds: Vec<TerminalObservationKind>,
    pub sequence_range: Option<TerminalObservationSequenceRange>,
    pub time_range: Option<TerminalObservationTimeRange>,
}

pub enum TerminalObservation {
    DeliveryAttempt(TerminalDeliveryAttemptObservation),
    Event(TerminalEventObservation),
    ViewerAttachment(TerminalViewerAttachmentObservation),
    SessionHealthChange(TerminalSessionHealthObservation),
    SessionArchiveCommit(TerminalSessionArchiveObservation),
}

pub struct TerminalObservationBatch {
    pub from_sequence: Option<TerminalObservationSequence>,
    pub through_sequence: Option<TerminalObservationSequence>,
    pub observations: Vec<TerminalObservation>,
}

pub struct TerminalSessionSnapshotQuery {
    pub terminal: Option<TerminalName>,
}

pub struct TerminalSessionSnapshot {
    pub at_sequence: TerminalObservationSequence,
    pub sessions: Vec<TerminalSessionObservation>,
}

pub struct TerminalObservationUnimplemented {
    pub reason: TerminalObservationUnimplementedReason,
}

pub enum TerminalObservationUnimplementedReason {
    NotInPrototypeScope,
    TerminalStoreUnavailable,
    TimeIndexUnavailable,
}

pub enum TerminalObservationRequest {
    Observations(TerminalObservationQuery),
    SessionSnapshot(TerminalSessionSnapshotQuery),
}

pub enum TerminalObservationReply {
    Observations(TerminalObservationBatch),
    SessionSnapshot(TerminalSessionSnapshot),
    Unimplemented(TerminalObservationUnimplemented),
}
```

The existing `TerminalIntrospectionSnapshot` should retire after the
event-log and session-snapshot relations land. It currently mixes
event-like observations with current session state; the implementation
should not keep two parallel snapshot models long term.

Add `sequence` and `observed_at` fields to event-like terminal
observations as the implementation touches them. The first three already
carry `sequence`; health/archive must grow it before they can participate
in the ordered event-log batch:

- `TerminalDeliveryAttemptObservation`
- `TerminalEventObservation`
- `TerminalViewerAttachmentObservation`
- `TerminalSessionHealthObservation`
- `TerminalSessionArchiveObservation`

`TerminalSessionObservation` may either carry `observed_at` directly or
be treated as current-state projection indexed by terminal name. In this
slice, sessions are current-state and live in `TerminalSessionSnapshot`,
not in `TerminalObservationBatch`.

### 1.2 `persona-terminal`

Add Sema support for the terminal observation relation.

Add a `signal-persona` dependency if `TimestampNanos` remains there.
There is no dependency cycle today; `signal-persona` does not depend on
`signal-persona-terminal`.

Required table shape after this slice:

```text
sessions_by_terminal: &str -> TerminalSessionObservation
delivery_attempts: u64 -> TerminalDeliveryAttemptObservation
terminal_events: u64 -> TerminalEventObservation
viewer_attachments: u64 -> TerminalViewerAttachmentObservation
session_health_changes: u64 -> TerminalSessionHealthObservation
session_archive_commits: u64 -> TerminalSessionArchiveObservation
latest_session_health_by_terminal: &str -> TerminalSessionHealthObservation
```

The current code already has sequence-keyed delivery/event/viewer tables
and string-keyed session, health, and archive tables. Do not use the
string-keyed health/archive tables as event-log primaries; they cannot
preserve multiple changes or participate in an ordered observation batch.
Either rename them as latest-state projections during the schema bump or
add new sequence-keyed event tables beside them.

Add packed-key time indexes for the event-like records:

```text
delivery_attempts_by_time: TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
terminal_events_by_time: TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
viewer_attachments_by_time: TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
session_health_changes_by_time: TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
session_archive_commits_by_time: TerminalObservationTimeKey -> TerminalObservationTimeIndexEntry
```

Use a typed packed key owned by `persona-terminal`:

```rust
TerminalObservationTimeKey::new(timestamp, sequence)
```

The value is a data-carrying reference, not `()`. A zero-sized index
value would be a conventional covering-index trick, but it conflicts with
the workspace's no-zero-sized-type direction. Use:

```rust
pub struct TerminalObservationTimeIndexEntry {
    pub sequence: TerminalObservationSequence,
}
```

Do not move this helper into Sema until a second component repeats the
pattern.

Add a read-only observation handler in the terminal supervisor path:

```text
Signal frame accepted
  -> frame demultiplexer
     -> terminal control request
     -> terminal observation request
```

The observation handler reads terminal-owned Sema state and returns a
`TerminalObservationBatch`. It does not mutate operational state.

### 1.3 `signal-persona-introspect`

Add central wrapper types:

```rust
pub enum ComponentObservationQuery {
    TerminalObservations(signal_persona_terminal::TerminalObservationQuery),
    TerminalSessionSnapshot(signal_persona_terminal::TerminalSessionSnapshotQuery),
    RouterObservations(signal_persona_router::RouterObservationQuery),
}

pub struct ComponentObservationsQuery {
    pub engine: EngineId,
    pub query: ComponentObservationQuery,
}

pub enum ComponentObservationResult {
    TerminalObservations(signal_persona_terminal::TerminalObservationBatch),
    TerminalSessionSnapshot(signal_persona_terminal::TerminalSessionSnapshot),
    RouterObservations(signal_persona_router::RouterObservationBatch),
}

pub struct ComponentObservations {
    pub engine: EngineId,
    pub result: ComponentObservationResult,
}
```

Extend the root channel:

```rust
request IntrospectionRequest {
    ...
    ComponentObservations(ComponentObservationsQuery),
    ListRecordKinds(ListRecordKindsQuery),
}

reply IntrospectionReply {
    ...
    ComponentObservations(ComponentObservations),
    RecordKinds(RecordKinds),
}
```

Add `ComponentObservations` and `ListRecordKinds` to
`IntrospectionScope`.

Do not add `SubscribeComponent` in the first implementation.

Add precise peer-failure reasons to `IntrospectionUnimplementedReason`:

```rust
PeerSocketMissing,
PeerSocketUnreachable,
```

`ComponentObservationMissing` means the component contract does not yet
support the observation relation. It should not be used when the daemon
socket is absent or refusing connections.

### 1.4 `persona-introspect`

Add `signal-persona-terminal`, `signal-persona-router`, and
`signal-persona` dependencies only when code uses them.

The first runtime implementation should do this:

1. `introspect` CLI decodes one NOTA `ComponentObservations` input.
2. CLI sends `signal-persona-introspect::ComponentObservations` to
   `persona-introspect-daemon`.
3. `IntrospectionRoot` asks `QueryPlanner` for a target plan.
4. `QueryPlanner` routes terminal queries to `TerminalClient`.
5. `TerminalClient` sends the terminal-owned observation query to
   `persona-terminal` over `terminal.sock`.
6. `persona-terminal` returns `TerminalObservationBatch`.
7. `persona-introspect` wraps it as
   `ComponentObservationResult::TerminalObservations`.
8. `NotaProjection` renders the reply at the edge.

The root should not return `Unknown` for this path. If a socket is
missing, it returns a typed unavailable/unimplemented reply.

## 2. CLI surface

Add terminal component observations to the `introspect` CLI first.

Recommended NOTA input:

```nota
(ComponentObservations
  engine "prototype"
  query (TerminalObservationQuery
    kinds (DeliveryAttempt Event)
    sequenceRange (TerminalObservationSequenceRange
      since 0)))
```

This is the only accepted shape for this slice. Do not add a shorthand
form with a bare `terminal` discriminator; that would be keyword dispatch
in disguise.

The reply should be a typed NOTA projection of
`IntrospectionReply::ComponentObservations`, not hand-written text.

## 3. Implementation order

### Package A - terminal observation relation

Repos:

- `signal-persona-terminal`
- `persona-terminal`

Work:

1. Add terminal observation query/batch/reply types.
2. Add sequence/time filtering types.
3. Add or update terminal event records with `observed_at`.
4. Split event-log observations from `TerminalSessionSnapshot`.
5. Add packed-key time-index tables in `persona-terminal`.
6. Add `TerminalTables::terminal_observations(query)` that reads real
   production tables.
7. Add `TerminalTables::terminal_session_snapshot(query)` for current
   session state.
8. Add a terminal supervisor observation handler.
9. Add round-trip and Sema-backed tests.

### Package B - central wrapper

Repos:

- `signal-persona-introspect`

Work:

1. Add `ComponentObservations`.
2. Add `ListRecordKinds`.
3. Add wrapper enum variants for TerminalObservations,
   TerminalSessionSnapshot, and RouterObservations.
4. Add round-trip tests proving the wrapper carries terminal-owned types
   without redefining them.
5. Add source-scan witness that central crate does not define terminal
   row structs.
6. Add `PeerSocketMissing` and `PeerSocketUnreachable` to
   `IntrospectionUnimplementedReason`.

### Package C - introspect runtime and CLI

Repos:

- `persona-introspect`

Work:

1. Add component-contract dependencies used by the slice.
2. Extend CLI input enum with `ComponentObservations`.
3. Teach `TargetSocketDirectory` typed peer names for terminal and router.
4. Implement `TerminalClient` as a real actor with socket state,
   component codec, and typed failure handling.
5. Route component observation requests through `QueryPlanner`.
6. Render the typed response through `NotaProjection`.
7. Add fake-peer socket tests and no-peer-redb-open tests.

### Package D - router follow-up

Repos:

- `signal-persona-router`
- `persona-router`
- `signal-persona-introspect`
- `persona-introspect`

Work:

1. Convert existing router summary/message-trace/channel-state surface into
   `RouterObservationQuery` and `RouterObservationBatch`.
2. Add router observation sequence and time indexes.
3. Add `ComponentObservationResult::RouterObservations`.
4. Implement `RouterClient` in `persona-introspect`.
5. Upgrade `DeliveryTrace` from scaffold status to correlated router and
   terminal facts.

## 4. Witnesses

### Contract witnesses

`signal-persona-terminal`:

- `terminal_observation_query_round_trips`
- `terminal_observation_batch_round_trips`
- `terminal_session_snapshot_round_trips`
- `terminal_observation_batch_preserves_event_order`
- `terminal_observation_batch_uses_terminal_owned_records`

`signal-persona-introspect`:

- `component_observations_wrap_terminal_batch`
- `component_observations_wrap_terminal_session_snapshot`
- `list_record_kinds_round_trips`
- `central_contract_does_not_define_terminal_rows`
- `peer_socket_failure_reasons_round_trip`

### Component Sema witnesses

`persona-terminal`:

- `terminal_observations_read_existing_production_tables`
- `terminal_observations_filter_by_sequence_range`
- `terminal_observations_filter_by_time_range`
- `terminal_observation_time_index_written_with_primary_record`
- `terminal_observation_time_index_value_carries_sequence`

The time-index test must call production write methods such as
`put_terminal_event`, not test-only table writes.

### Runtime witnesses

`persona-introspect`:

- `component_observations_uses_terminal_socket`
- `component_observations_does_not_open_terminal_redb`
- `terminal_client_decodes_terminal_observation_batch`
- `terminal_client_reports_peer_socket_missing`
- `terminal_client_reports_peer_socket_unreachable`
- `introspect_cli_projects_component_observations_to_nota`

Use fake terminal sockets for the first runtime slice. The fake should
decode a real `signal-persona-terminal` frame and return a real
`TerminalObservationBatch`. A fake that only sends prebuilt bytes without
checking the request does not prove the architecture.

### Prototype witness

In `persona`, add or update a Nix app/check that starts the prototype
with `persona-introspect` and a terminal observation fixture:

```text
persona-engine-introspect-terminal-observations
```

It should prove:

1. manager starts `persona-introspect`;
2. terminal writes at least one production observation record;
3. `introspect` CLI asks `persona-introspect-daemon`;
4. `persona-introspect-daemon` asks `persona-terminal`;
5. returned NOTA includes the terminal-owned observation.

## 5. What not to implement

Do not implement these in the first slice:

- a universal untyped observation filter;
- peer redb reads from `persona-introspect`;
- raw transcript fanout;
- polling subscriptions;
- field-level runtime reflection;
- a Sema-level `TimeIndexedTable` helper;
- zero-sized Sema index values such as `Table<Key, ()>`;
- a sibling `signal-persona-terminal-introspect` crate;
- duplicate terminal row structs in `signal-persona-introspect`.

## 6. Open decisions after this slice

No human decision blocks terminal-first implementation.

The next decisions after terminal and router are live:

1. Whether the next observation component is harness or mind.
2. Whether to extract the time-index helper into Sema after two
   components implement it.
3. Whether live `SubscribeComponent` should land once commit-then-emit
   exists in terminal/router, or wait until mind's subscription path is
   fully proven.
4. Whether field-level schema descriptors should be generated by
   `nota-derive` or stay out of scope.

## 7. Bottom line

This design is implementation-ready for a terminal-first
`ComponentObservations` slice.

The operator should start with terminal because its existing observation
records exercise the full shape. The path is:

```text
terminal-owned observation query/reply
  -> central introspect wrapper
  -> persona-introspect terminal client
  -> introspect CLI NOTA projection
  -> Nix witness proving the live daemon path
```

The central invariant is simple: `persona-introspect` sees widely, but
truth stays owned by each component.
