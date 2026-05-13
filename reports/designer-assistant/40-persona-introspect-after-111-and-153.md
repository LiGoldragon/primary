# 40 - Persona-introspect after operator-assistant 111 and designer 153

Scope: review `reports/operator-assistant/111-persona-introspect-contract-dependency-gap.md`
and `reports/designer/153-persona-introspect-shape-and-sema-capabilities.md`
against the current code and architecture.

## 0. Position

The two reports agree on the important architectural rule:

- `signal-persona-introspect` is the central introspection envelope.
- Component-owned observation records live in the component-owned
  contracts.
- `persona-introspect` is the high-privilege runtime that depends on
  many contracts, asks live daemons over Signal, fans results in, and
  projects NOTA only at the edge.
- `persona-introspect` must not open peer redb files.

That rule is correct and should remain load-bearing.

The design still needs sharpening before implementation:

1. The central contract may wrap component observation replies, but
   it must wrap component-owned types directly. It must not define
   router, terminal, harness, mind, system, message, or manager row
   fields itself.
2. `SnapshotId` should not be described as a redb transaction id unless
   Sema exposes one. Today Sema exposes typed `iter` and `range`, not a
   stable transaction identity. Components should mint their own
   observation sequence or commit sequence.
3. Time-window queries need explicit secondary indexes. Sema's
   `Table::range` is enough only when the component table key is already
   time/sequence ordered.
4. "Every component grows an introspect action" needs to mean "every
   component contract names an observation relation." The runtime branch
   should be a read-only inspection plane beside the operational reducer,
   not another mutation path inside the domain reducer.
5. Current docs still reference deleted or historical reports. The
   architecture should point at current canonical reports or state the
   decision directly.

## 1. Current code truth

### 1.1 `signal-persona-introspect`

`/git/github.com/LiGoldragon/signal-persona-introspect/src/lib.rs`
currently owns:

- `IntrospectionTarget`
- `IntrospectionScope`
- `EngineSnapshot`
- `ComponentSnapshot`
- `DeliveryTrace`
- `PrototypeWitness`
- `IntrospectionUnimplemented`
- `IntrospectionDenied`

It does not yet own:

- `ComponentObservations`
- `SubscribeComponent`
- `ListRecordKinds`
- a snapshot/sequence cursor
- a component observation wrapper enum

That matches the current scaffold, but not the richer shape in
designer/153.

### 1.2 `persona-introspect`

`/git/github.com/LiGoldragon/persona-introspect/Cargo.toml` currently
depends on:

- `signal-core`
- `signal-persona-auth`
- `signal-persona-introspect`

It does not depend on `signal-persona`, `signal-persona-router`,
`signal-persona-terminal`, `signal-persona-harness`,
`signal-persona-system`, `signal-persona-mind`, or
`signal-persona-message`.

`/git/github.com/LiGoldragon/persona-introspect/src/runtime.rs` has
state-bearing Kameo actors, but the clients are still socket-path
holders. `IntrospectionRoot` returns scaffold values:

- `EngineSnapshot` reports only manager, router, terminal.
- `ComponentSnapshot` always returns `ComponentReadiness::Unknown`.
- `DeliveryTrace` always returns `DeliveryTraceStatus::Unknown`.
- `PrototypeWitness` always returns `Unknown` readiness/status.

The daemon can now bind and serve Signal frames. The observation graph is
not live.

### 1.3 Component contracts

`signal-persona-router` has a router-owned query/reply contract for
summary, message trace, and channel state. It is useful, but it is not
yet the time-window observation relation designer/153 describes.

`signal-persona-terminal` has terminal-owned introspection records and
`TerminalIntrospectionSnapshot`. It does not yet expose a terminal
observation request/reply relation.

The other first-stack contracts have some status/readiness records, but
the current `persona-introspect` daemon cannot consume them.

### 1.4 Stale navigation

`/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` still references
`reports/designer/146-introspection-component-and-contract-layer.md`,
but that report is no longer present in `reports/designer/`. The same
section also says `signal-persona-introspect` is "planned" even though
the repo and crate now exist.

This is not a design contradiction, but it is navigation debt. Agents
following the architecture will chase a missing report.

## 2. Review of operator-assistant 111

Operator-assistant 111 is the right implementation diagnosis.

Its strongest point is the distinction between:

- `signal-persona-introspect`: central envelope, selectors, and final
  projection wrapper.
- `persona-introspect`: runtime component that depends on many signal
  contracts.
- component contracts: owners of the actual observation records.

The recommended first implementation slice is also correct:

1. Add only the component contract dependencies the next slice uses.
2. Teach the target directory the peer sockets for that slice.
3. Make each client actor own its protocol codec and failure handling.
4. Preserve typed replies until `NotaProjection`.
5. Add architectural-truth tests proving the query crossed daemon
   sockets and did not open peer redb files.

The one thing I would sharpen: "add component contract dependencies to
`persona-introspect`" is necessary, but it is not enough. The peer
component daemon must also expose a read-only observation relation in
its own contract and runtime. For example, adding
`signal-persona-terminal` to `persona-introspect` does not by itself
let `TerminalClient` ask for `TerminalIntrospectionSnapshot`; the
terminal daemon needs the request handler.

## 3. Review of designer 153

Designer 153 is the right larger shape: component observations as
typed records, Sema as raw typed database kernel, time windows in the
component daemon, and `persona-introspect` as fan-in/projection.

I would keep these parts:

- The CLI is the first user interface: one NOTA request record in, one
  NOTA reply record out.
- Sema does not own reducers, subscriptions, or event emission.
- Each component owns its own Sema tables and observation relation.
- `persona-introspect` asks live daemons and does not inspect foreign
  databases.
- Push subscriptions are eventually necessary; repeated snapshot
  polling is not acceptable.
- A `harness` CLI is a real tactical gap, separate from introspection
  but exposed by this review.

I would modify these parts before operators implement from it.

### 3.1 The central observation batch must be a wrapper, not a schema hub

Designer 153 proposes a `ComponentObservationBatch` in
`signal-persona-introspect` with variants wrapping per-component
observation vocabularies.

That can be correct, but only if it is explicitly treated as a wrapper
union:

```text
ComponentObservationBatch::Router(signal_persona_router::RouterObservations)
ComponentObservationBatch::Terminal(signal_persona_terminal::TerminalObservations)
```

The central crate should not define `RouteDecision`,
`TerminalSessionObservation`, `HarnessLifecycleObservation`, or similar
field-bearing records. The owning component contract defines those.

The dependency direction is acceptable:

- `signal-persona-introspect` may depend on component contracts for
  wrapper payloads if the CLI-facing reply needs a single typed union.
- component contracts must not depend on `signal-persona-introspect`.
- component daemons should answer their own observation relations
  without importing the central introspection envelope.

This keeps the central contract from becoming `all-engine-types.rs`.

### 3.2 The filter should be target-specific

Designer 153 sketches:

```text
ComponentObservations { engine, target, filter: ObservationFilter }
```

That is probably too generic. A single `ObservationFilter` will either
underspecify the target-specific domain or become a bag of optional
fields.

Prefer a closed target-specific selector:

```text
ComponentObservationQuery::Router(signal_persona_router::RouterObservationQuery)
ComponentObservationQuery::Terminal(signal_persona_terminal::TerminalObservationQuery)
ComponentObservationQuery::Harness(signal_persona_harness::HarnessObservationQuery)
```

Then each component owns its own kind enum, time/sequence filter, and
record batch. The central contract only chooses which component-shaped
query is being forwarded.

### 3.3 Snapshot identity should be component-minted

Designer 153 says redb read transactions are MVCC snapshots and suggests
carrying a `SnapshotId`.

The architectural point is right: introspection replies need a stable
cursor so tests and operators can tell whether two observations came from
the same component view. The implementation claim should be narrowed.
Today's Sema API exposes `read`, `write`, typed `Table::iter`, and
typed `Table::range`; it does not expose a stable redb transaction id.

The v1 cursor should therefore be component-minted:

- `ObservationSequence`
- `ComponentSnapshotSequence`
- `CommitSequence`

The component increments it in the same write transaction that records
the observation. Snapshot replies return the latest sequence included.
Follow-up queries can ask `after_sequence`, `from_sequence`, or a
sequence range.

Keep human-facing time ranges too. The user asked for time-window
inspection; replacing time with sequence would make the CLI worse. The
right shape is both:

- time range for human and agent queries;
- sequence cursor for reproducible tests and "give me what changed
  after the last reply."

### 3.4 Sema range support requires explicit indexes

Designer 153 correctly says Sema is raw and that reducers/subscriptions
belong in daemons. It should also make the indexing burden explicit.

`Table::range` ranges over the table key. If a component wants
"records between two timestamps," it needs a typed table keyed by
`(TimestampNanos, ObservationSequence)` or equivalent. If it wants
"records after cursor N," it needs a sequence-keyed table.

The component's reducer must write primary records and secondary index
records in the same Sema write transaction. The witness should prove both
tables are written by the production code, not by test-only logic.

Do not add `TimeIndexedTable` to Sema before two components have
implemented the pattern. But design terminal/router's first version so
the later extraction is obvious.

### 3.5 "Introspect action" should be a read-only control relation

Designer 153 says each first-stack component needs an `Introspect`
request variant on its own signal contract. The safer wording is:

> each component contract needs a named observation relation.

The runtime path should be a sibling read-only inspection plane. It
should not run through the same reducer that handles operational
mutations. A good component shape:

```text
Signal frame accepted
  -> frame demultiplexer
     -> operational request branch
     -> observation request branch
```

The observation branch may read the component's own Sema database or ask
the component's own store actor for a read snapshot. It must not mutate
operational state except for its own audit counters if those are
explicitly modeled.

### 3.6 `format_status` should be translated into workspace names

Designer 153 borrows Erlang/OTP's `format_status` idea. The idea is
good: each component chooses a status projection so operator views do
not depend on raw internal row shapes.

The Rust/workspace name should not be `format_status`. Use a noun such
as:

- `ComponentStatusProjection`
- `StatusProjection`
- `ObservationProjection`

The component owns this projection policy. `persona-introspect` should
render it, not invent it.

### 3.7 Schema introspection should start modestly

`ListRecordKinds` is a good addition, but it should not pretend Rust/rkyv
runtime reflection exists if it does not.

V1 should report honest contract metadata:

- component target;
- contract crate name;
- protocol/schema version;
- supported observation query variants;
- supported observation record kinds;
- whether time range, sequence range, and subscription are supported.

Field-level schemas can come later if the derive layer can generate a
truthful descriptor. Hand-maintained field schemas will drift unless they
have round-trip witnesses.

## 4. Recommended prototype landing path

### Slice A - make the current scaffold honest

Goal: replace `Unknown` with real manager/router/terminal query results
where the current envelope already has fields.

1. Add `signal-persona`, `signal-persona-router`, and
   `signal-persona-terminal` to `persona-introspect` only when their
   clients use them.
2. Extend `TargetSocketDirectory` to track the corresponding peers using
   typed component names from the spawn envelope, not string guesses.
3. Implement `ManagerClient`, `RouterClient`, and `TerminalClient` as
   real client actors with typed request messages.
4. Make `PrototypeWitness` ask those three clients and return
   component-derived replies.
5. Add tests with fake peer sockets proving `persona-introspect` sends
   Signal frames to peers.
6. Add a negative witness proving `persona-introspect` does not open
   `router.redb`, `terminal.redb`, or `mind.redb`.

This makes operator-assistant 111's tactical recommendation real.

### Slice B - add component observations without bucket drift

Goal: implement designer 153's time-window surface for one component.

1. Choose terminal as the first observation component if the goal is the
   richest state vocabulary. Choose router if the goal is fastest
   delivery-trace proof. Either is defensible; I lean terminal for the
   component-observation shape and router immediately after for delivery
   proof.
2. Add a terminal-owned observation query/reply relation to
   `signal-persona-terminal`, using existing terminal introspection
   records.
3. Add the central wrapper in `signal-persona-introspect` only as a
   wrapper around the terminal-owned reply type.
4. Implement the terminal daemon's read-only observation handler against
   terminal-owned state.
5. Implement `TerminalClient` in `persona-introspect`.
6. Add CLI input for `ComponentObservations` and render the typed reply
   to NOTA at the edge.

### Slice C - add live subscriptions after one-shot observations

Goal: obey push-not-pull without forcing every component to invent a
partial event stream immediately.

1. First support one-shot `ComponentObservations`.
2. Then add `SubscribeComponent` with "initial snapshot, then deltas."
3. If a component cannot push yet, return typed `Unimplemented`; do not
   poll in the `introspect` CLI or daemon.
4. Use `persona-mind`'s subscription path as the reference once its
   commit-time push delivery is complete.

## 5. Architecture edits I would make next

I am not editing the architecture in this report, but these are the
edits I would queue for the relevant owners.

### `persona/ARCHITECTURE.md`

- Replace references to deleted `reports/designer/146...` with current
  canonical wording or current report paths.
- Change "`signal-persona-introspect` (planned)" to "`signal-persona-introspect`
  owns..." because the repo exists.
- State that `introspect.redb`, if retained in the engine component map,
  is for introspect-owned audit/subscription/projection state only; it
  is not a mirror of peer databases.

### `signal-persona-introspect/ARCHITECTURE.md`

- Add the wrapper-union rule explicitly: this contract may wrap
  component-owned observation reply types; it must not define their row
  fields.
- Add `ComponentObservations`, `ListRecordKinds`, and later
  `SubscribeComponent` as planned relations.
- State the sequence cursor rule as component-minted, not redb-provided.

### `persona-introspect/ARCHITECTURE.md`

- Add all eventual peer client actors to the actor map, but keep the
  current manager/router/terminal slice named as the first implementation
  slice.
- Clarify that peer client actors own component-specific codecs and
  failure handling.
- Add the no-peer-redb-open witness as a non-negotiable acceptance test.

### Component contract architectures

For each state-bearing component contract, add an observation relation
section:

- query variants;
- reply variants;
- observation record kinds;
- time/sequence filter support;
- subscription support state;
- redaction/projection ownership;
- unimplemented reply shape.

## 6. Bottom line

Operator-assistant 111 is the correct tactical implementation gap
report. Designer 153 is the correct strategic shape, but it should be
tightened before operators implement from it.

The next implementation should not start with "add every dependency" or
"invent a universal observation filter." It should start with one
component-owned observation relation, one `persona-introspect` client that
uses it over Signal, and one Nix witness proving the data came through
the live daemon boundary rather than a peer database shortcut.

