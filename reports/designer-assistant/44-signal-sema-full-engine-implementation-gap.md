# 44 - Signal and Sema full engine implementation gap

*Designer-assistant report, 2026-05-14. Scope: compare current
implementation against the newly clarified intent: Signal is the
typed binary database-operation language in transit, and Sema should
grow into the reusable database engine that executes those operations
for state-bearing components. This report focuses on code that exists
now, the distance from intent, and the essential Sema modifications
needed for the full engine.*

## 0. Bottom line

The implementation has the correct seed, but not the full engine.

What is already real:

- `signal-core` has the twelve verb spine and a generic
  `Request { verb, payload }` envelope.
- Nexus documentation now describes explicit verb records over NOTA.
- `signal-persona` manager/supervision tests already use `Match` for
  reads and `Mutate` for lifecycle transitions.
- `sema` has a typed redb/rkyv table kernel with schema and database
  format guards.

What is still far from the clarified intent:

- Most `signal-persona-*` contracts still wrap every request as
  `Assert`, including queries and subscriptions.
- `signal_channel!` does not declare legal verbs per request variant,
  so the type system cannot prevent `InboxQuery` under `Assert`.
- The sema-ecosystem `signal` crate still has its own old
  `Request::{Assert, Query, Subscribe, ...}` enum instead of using
  `signal_core::Request { verb: SemaVerb, payload }`.
- Nexus parser code is still a compatibility adapter that parses only
  the old assert surface.
- `sema` is still a typed table kernel, not an operation engine: no
  verb executor, no query plan, no project/aggregate/constrain engine,
  no operation log, no validation pipeline, no subscription changefeed.

The full target should be stated this sharply:

> Signal is the database-operation language in transit. Every
> cross-component operation is a typed payload under a Sema verb. Sema
> is the database engine that knows how to execute those verbs over
> typed records, tables, indexes, queries, subscriptions, and durable
> transaction logs. Components still own domain policy and authorization,
> but they should not reimplement the database engine per component.

The version of `reports/designer/155-sema-db-pattern-library.md` read
during this pass gives a useful first layer if it stays narrow:
`IndexedTable`, `MonotoneSequence`, `Table::scan_range`, and named
packed keys. For the full engine, those are implementation materials,
not the destination. A narrow pattern library can be accepted only as
Layer 1 of a larger Sema engine plan.

## 1. Clarified intent

The operation stack should read like this:

```text
Nexus/NOTA at edge
  -> parse/render typed verb records
Signal in transit
  -> signal_core::Request { verb: SemaVerb, payload: ContractRequest }
Component daemon
  -> owns socket, auth, actor order, domain validation, policy
Sema full engine
  -> executes database operations over typed records and indexes
Component daemon
  -> emits typed replies, subscription deltas, and effects after commit
```

`signal-core` owns the universal operation envelope:

```text
Assert Subscribe Constrain Mutate Match Infer
Retract Aggregate Project Atomic Validate Recurse
```

Each `signal-*` contract owns the typed payload variants that are
legal under those verbs. A request variant that cannot honestly fit
one of the existing verbs is not a one-off exception. It is a design
event: either the payload is wrong-shaped, or the verb set is
incomplete.

Replies do not need a second independent verb when they are causally
tied to a request. But pushed events are only clean if they are either:

- deltas on an existing `Subscribe` stream, with an explicit
  subscription identity and sequence; or
- new observations sent as their own `Assert` operation.

The current practice of using a `Reply` enum as a general event bucket
should be treated carefully. It is acceptable for request replies and
subscription streams; it is not a clean model for independent
bidirectional traffic.

## 2. Implementation distance table

| Area | Current implementation | Distance from intent | Needed correction |
|---|---|---|---|
| `signal-core` verbs | `SemaVerb` and `Request { verb, payload }` exist. | Foundation is right. Enforcement is weak because any payload can be wrapped under any verb. | Add contract-level legal verb mapping and construction helpers. |
| `signal_channel!` macro | Emits request/reply enums, frame aliases, `From` impls, and NOTA codecs. | No per-variant verb declaration. The macro cannot generate `sema_verb()` or prevent wrong wrappers. | Extend macro or require a companion trait that maps every request variant to one `SemaVerb`. |
| `signal` crate | Still has old `Request::Assert`, `Request::Query`, `Request::Subscribe`, `Request::Validate`, etc. | It is not yet rebased onto the twelve-verb `signal-core` request envelope. It uses `Query`, while current Nexus says `Query` is not a verb. | Replace old request enum with `signal_core::Request<SignalRequest>` and a domain payload enum with legal verb mapping. |
| Nexus | Spec is correct. Parser says it only accepts current Criome-specific assert surface. | Documentation leads code. Parser does not implement explicit `(Assert ...)`, `(Match ...)`, `(Subscribe ...)`, etc. | Rebase parser/renderer onto the twelve verb records and the rebased `signal` payloads. |
| `signal-persona` manager/supervision | Tests wrap status as `Match` and start/stop as `Mutate`. | This is the closest implementation to the intent. | Generalize the pattern into all contracts and tests. |
| Other `signal-persona-*` contracts | Many tests use `Request::assert(...)` for everything. | Query, subscription, control, and inspection requests are semantically collapsed into `Assert`. | Add per-variant verb mapping and rewrite tests to use it. |
| `sema` | Typed redb/rkyv table kernel with `get`, `insert`, `remove`, `iter`, `range`, `read`, `write`. | This is storage substrate, not database-operation engine. | Add operation execution, schema/catalog metadata, indexes, query plans, validation, transaction log, and subscription changefeed. |
| Components | `persona-mind`, `persona-terminal`, `persona-router` hand-roll storage/query patterns. | Components are already rebuilding small database-engine pieces. | Move repeated mechanical execution into Sema while keeping domain policy in components. |

## 3. Evidence from code

### 3.1 `signal-core` has the right envelope but not legality

`/git/github.com/LiGoldragon/signal-core/src/request.rs:5` defines
the twelve verbs, and lines 21-24 define the generic operation
envelope:

```rust
pub enum Request<Payload> {
    Handshake(HandshakeRequest),
    Operation { verb: SemaVerb, payload: Payload },
}
```

This is the right spine. The gap is that lines 32-81 expose helpers
like `Request::assert(payload)`, `Request::match_records(payload)`,
and `Request::mutate(payload)` for any `Payload`. The compiler does
not know whether `Payload` is legally assert-shaped, match-shaped, or
mutate-shaped.

`/git/github.com/LiGoldragon/signal-core/src/channel.rs:93` defines
`signal_channel!`. Lines 95-100 accept only request/reply variant
lists. There is no syntax for:

```text
MessageSubmission: Assert
InboxQuery: Match
SubscribeThoughts: Subscribe
```

The macro emits the vocabulary, not the operation mapping. That was
fine before the clarified model; it is now the main enforcement gap.

### 3.2 `signal` is still pre-renovation

`/git/github.com/LiGoldragon/signal/src/request.rs:24` defines an
older request enum:

```rust
pub enum Request {
    Handshake(HandshakeRequest),
    Assert(AssertOperation),
    Mutate(MutateOperation),
    Retract(RetractOperation),
    AtomicBatch(AtomicBatch),
    Query(QueryOperation),
    Subscribe(QueryOperation),
    Validate(ValidateOperation),
}
```

This diverges from the current operation language in two ways:

- it duplicates operation structure instead of using
  `signal_core::Request { verb, payload }`;
- it keeps `Query` as a variant, while current Nexus says `Query` is
  not a verb; read operations are `Match`, `Project`, `Aggregate`, or
  `Constrain`.

`/git/github.com/LiGoldragon/signal/src/query.rs:17` has only
`QueryOperation::{Node, Edge, Graph}`. It is a useful M0 match surface,
but not the full query language.

### 3.3 Nexus spec leads Nexus parser

`/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md:164` says the spec
is renovating toward explicit verb records and that the current parser
still carries the previous Criome-specific M0 surface until `signal`
is rebased.

The code confirms it. `/git/github.com/LiGoldragon/nexus/src/parser.rs:38`
only decodes an `AssertOperation` and returns `Request::Assert`:

```rust
Some(Token::LParen) => {
    let operation = AssertOperation::decode(&mut self.decoder)?;
    Ok(Some(Request::Assert(operation)))
}
```

So the text-side architecture is correct, but implementation is still
compatibility code.

### 3.4 Persona manager is close; most other contracts are not

`signal-persona` proves the intended shape in tests:

- `/git/github.com/LiGoldragon/signal-persona/tests/engine_manager.rs:53`
  wraps `EngineStatusQuery` as `Request::match_records`.
- `/git/github.com/LiGoldragon/signal-persona/tests/engine_manager.rs:329`
  wraps `ComponentStartup` as `Request::mutate`.
- `/git/github.com/LiGoldragon/signal-persona/tests/engine_manager.rs:405`
  checks supervision hello/readiness/health as `Match`.
- `/git/github.com/LiGoldragon/signal-persona/tests/engine_manager.rs:412`
  checks graceful stop as `Mutate`.

The other Persona contracts mostly use `Assert` as a default wrapper:

- `signal-persona-message/tests/round_trip.rs:70` wraps
  `InboxQuery` as `Request::assert`.
- `signal-persona-introspect/tests/round_trip.rs:14` wraps
  `EngineSnapshotQuery` as `Request::assert`.
- `signal-persona-router/tests/round_trip.rs:15` wraps
  `RouterSummaryQuery` as `Request::assert`.
- `signal-persona-system/tests/round_trip.rs:22` wraps all
  `SystemRequest` values through `Request::assert`.
- `signal-persona-harness/tests/round_trip.rs:19` wraps all
  `HarnessRequest` values through `Request::assert`.
- `signal-persona-terminal/tests/round_trip.rs:34` wraps all
  `TerminalRequest` values through `Request::assert`.
- `signal-persona-mind/tests/round_trip.rs:17` wraps all
  `MindRequest` values through `Request::assert`.

Several of those crates have `operation_kind()` methods, but those
return contract-local variant names like `MessageOperationKind` or
`TerminalOperationKind`, not `SemaVerb`. They help name the operation
for unimplemented replies, but they do not enforce database-operation
semantics.

### 3.5 `Reply` and pushed event vocabulary need a full-engine rule

`/git/github.com/LiGoldragon/signal-core/src/reply.rs:5` defines:

```rust
pub enum Reply<Payload> {
    Handshake(HandshakeReply),
    Operation(Payload),
}
```

This is fine for request/response. But several contracts use reply
enums as event streams:

- `signal-persona-system` documents focus observations pushed back to
  router.
- `signal-persona-terminal` has `TerminalEvent` as the reply side,
  including transcript deltas, worker lifecycle events, and exit
  events.
- `signal-persona-harness` has harness lifecycle observations as reply
  events.

The full engine needs a rule:

- If these are subscription deltas, they are causally tied to a prior
  `Subscribe` request and should carry subscription identity/sequence.
- If they are independent observations, they should travel as
  `Request { verb: Assert, payload: Observation }` in the opposite
  direction, not as unverb'd replies.

Otherwise "everything in transit is under a verb" remains false for
event-shaped traffic.

### 3.6 `sema` is a raw table kernel today

`/git/github.com/LiGoldragon/sema/src/lib.rs:267` defines
`Table<K, V>`. The typed table surface is:

- `get` at line 394;
- `insert` at line 411;
- `remove` at line 429;
- eager `iter` at line 445;
- eager `range` at line 467;
- `Sema::write` at line 648;
- `Sema::read` at line 657.

This is a solid storage kernel. It does not execute database
operations. There is no API that accepts a typed `Assert`, `Match`,
`Subscribe`, `Constrain`, or `Project` plan and runs it.

The current code also still carries a legacy raw slot-store path:
`Sema::store(&[u8])` at line 666, `Sema::get(Slot)` at line 685, and
`Sema::iter()` at line 700. That is explicitly legacy, but it is the
opposite of the full engine: raw bytes with scan-and-try-decode.

### 3.7 Components are already reimplementing database pieces

`persona-mind/src/tables.rs` hand-rolls:

- typed tables for claims, activity, memory graph, thoughts,
  relations, subscriptions;
- four next-slot counters (`next_activity_slot`,
  `next_thought_slot`, `next_relation_slot`,
  `next_subscription_slot`);
- scan-and-filter query paths in `persona-mind/src/graph.rs`.

`persona-terminal/src/tables.rs` hand-rolls separate tables and
eager `iter` wrappers for sessions, delivery attempts, terminal
events, viewer attachments, health, and archives.

`persona-router/src/tables.rs` already has a hand-written secondary
index shape: `CHANNELS` plus `CHANNELS_BY_TRIPLE`, both written in the
same transaction.

This is the pressure the full engine should absorb.

## 4. What Sema must become for the full engine

Designer 155's pattern library is useful as storage machinery, but the
full engine needs a larger shape. The core change is:

> Sema should not only expose typed tables. It should expose typed
> execution of the Signal/Sema verbs over a component's record
> families, indexes, validation rules, transaction log, query plans,
> and subscriptions.

That does not mean Sema becomes a policy actor, a text parser, or a
generic component runtime. Nexus/NOTA remains an edge format. Component
daemons still own sockets, actor order, authorization, delivery, and
domain policy. Sema owns the database execution mechanics those
components would otherwise rebuild locally.

The following pieces are essential.

### 4.1 Operation execution layer

Sema needs an operation executor whose input is the same operation
language Signal carries:

```rust
signal_core::Request<DomainRequest>
```

The executor should not parse Nexus and should not own domain payload
types. Instead, each component supplies a typed domain adapter that
maps its request enum to a Sema execution plan:

```rust
pub trait SemaDomain {
    type Request;
    type Reply;

    fn plan(&self, request: &Self::Request) -> Result<SemaPlan<Self>>;
}
```

The exact trait names can change. The structural requirement is that
Sema executes typed plans under the twelve verbs, while the domain
adapter owns payload interpretation.

### 4.2 Legal verb mapping at the contract boundary

Before Sema can execute operations reliably, the wire contracts must
declare legal verbs. A contract request enum needs something like:

```rust
impl MessageRequest {
    pub fn sema_verb(&self) -> SemaVerb {
        match self {
            Self::MessageSubmission(_) => SemaVerb::Assert,
            Self::StampedMessageSubmission(_) => SemaVerb::Assert,
            Self::InboxQuery(_) => SemaVerb::Match,
        }
    }
}
```

For full correctness, this should be generated or enforced by
`signal_channel!` rather than hand-written forever. Possible syntax:

```rust
signal_channel! {
    request MessageRequest {
        Assert MessageSubmission(MessageSubmission),
        Assert StampedMessageSubmission(StampedMessageSubmission),
        Match InboxQuery(InboxQuery),
    }
    reply MessageReply { ... }
}
```

The macro can then generate:

- `fn sema_verb(&self) -> SemaVerb`;
- `fn into_signal_request(self) -> signal_core::Request<Self>`;
- tests or compile-time checks that every request variant declares a
  verb;
- no default "everything is Assert" path.

The low-level `Request::operation(verb, payload)` can stay for
kernel tests, but contract consumers should use the contract-owned
constructor.

### 4.3 Record-family catalog

A database engine needs to know the record families it can execute
over. Today, each component declares plain `Table` constants. Full
Sema needs a typed catalog that says, per record family:

- primary table name;
- key/slot identity type;
- value type;
- revision/commit metadata;
- indexes;
- legal operations;
- query pattern type;
- projection type;
- validators;
- redaction/introspection class if needed.

This catalog should be code, not strings. Eventually Prism/schema-as-
records can generate it. In the near term it can be hand-written Rust
in each component's Sema layer.

### 4.4 Durable operation log

Full Sema needs a durable transition log. Tables are current state;
the log is the history of operations that produced it.

Minimum log record:

- commit sequence;
- commit timestamp or database-time authority;
- operation verb;
- affected record family;
- affected slot/key/revision;
- origin/provenance passed from the daemon;
- result summary;
- optional validation diagnostics.

This is where `Assert`, `Mutate`, `Retract`, and `Atomic` become
auditably real database operations instead of just table writes.

### 4.5 Assert, Mutate, Retract, Atomic, Validate executor

Sema needs standard semantics for the write verbs:

- `Assert`: allocate identity, validate, insert primary row, update
  indexes, append operation log, return accepted slot/revision.
- `Mutate`: check expected revision if present, validate replacement,
  replace row, update indexes, append log.
- `Retract`: tombstone or remove according to family policy, update
  indexes, append log.
- `Atomic`: execute a typed bundle in one transaction; either all rows,
  indexes, counters, and log entries commit, or none do.
- `Validate`: run the same validators and plan construction without
  committing.

Components should not reimplement those transaction patterns. They
should provide validators and domain-specific transition rules.

### 4.6 Match, Project, Aggregate, Constrain query engine

Full Sema needs a typed query engine, but not a text DSL. The query
language is typed Signal/Nexus records:

- `Match`: execute typed patterns such as `NodeQuery`,
  `TerminalObservationQuery`, `ThoughtFilter`, etc. using indexes when
  available.
- `Project`: return selected typed fields or typed view records.
- `Aggregate`: count/reduce/group matched rows.
- `Constrain`: join/unify multiple patterns with shared bindings.

The immediate internal representation can be a typed Rust plan IR, not
public text. Nexus projects to it at the edge; Rust clients can build
it directly.

The engine needs:

- query plan records;
- index selection;
- bounded scans;
- projection records;
- aggregate reducers;
- join/unification support over `PatternField<T>`;
- stable cursors/snapshot identity.

Designer 155's `scan_range` and `IndexedTable` are useful materials
inside this larger query engine, but they are not the query engine.

### 4.7 Subscribe and changefeed

The full engine should make "queries are values; they can be
subscribed to" real.

Sema should own the database mechanics:

- persist subscription query records;
- compute initial snapshot;
- on write commit, evaluate affected subscriptions;
- emit typed deltas with commit sequence and subscription id.

The component actor still owns delivery endpoints and authorization:
who gets the delta, whether the socket is still alive, whether raw
data is redacted, and how backpressure is handled. But the matching of
committed changes to persisted typed subscription queries is database
engine work and should not be reimplemented in every component.

### 4.8 Infer and Recurse layers

`Infer` and `Recurse` are real verbs and should stay in the full
language. They do not need to be prototype primitives in every
component, but the engine should reserve their execution slots:

- `Infer`: derived facts from rule/ontology records.
- `Recurse`: fixpoint traversal over graph/relation families.

In Persona, these likely land first in `persona-mind` graph work. Sema
should not fake them with ad hoc component helpers; it should accept
that they are engine layers that need explicit plan/executor design.

### 4.9 Schema and introspection

Full Sema must make its own state inspectable as typed records:

- record family catalog;
- indexes;
- query plans;
- operation log entries;
- schema version;
- format version;
- subscription registrations;
- current cursors and sequences.

This is not Nexus text in the store. It is typed binary state that
`persona-introspect` or a Nexus renderer can project outward.

## 5. Concrete modification path

### Package A - Stop semantic verb drift on the wire

1. Extend `signal_channel!` or add a required companion trait so every
   request variant declares a legal `SemaVerb`.
2. Generate `sema_verb()` and a contract-owned frame constructor.
3. Rewrite `signal-persona-*` tests so read-shaped requests use
   `Match`, subscription-shaped requests use `Subscribe`, transition
   requests use `Mutate`, and submissions/observations use `Assert`.
4. Treat any "all requests use Assert" test as a failing architectural
   witness.

This package is not Sema itself, but Sema cannot become the full engine
while the wire lies about operation class.

### Package B - Rebase `signal` and Nexus onto the twelve-verb envelope

1. Replace `signal::Request::{Assert, Query, ...}` with a domain
   payload enum under `signal_core::Request`.
2. Rename old `QueryOperation` usage into `Match` payloads where it is
   read-shaped.
3. Add placeholder payloads for `Project`, `Aggregate`, `Constrain`,
   `Infer`, and `Recurse` if their behavior is not built yet, with
   typed unimplemented diagnostics.
4. Update Nexus parser from "decode `AssertOperation` on any `(`" to
   explicit verb-record dispatch.

### Package C - Add Sema operation log and record-family catalog

This is the first real full-engine package in `sema`:

- typed catalog declarations;
- operation log table;
- commit sequence;
- revision records;
- typed metadata for record families and indexes.

This makes later operation execution observable and auditable.

### Package D - Implement write-verb execution

Add execution for `Assert`, `Mutate`, `Retract`, `Atomic`, and
`Validate` plans. This is where Sema begins to replace component
hand-rolled write transactions.

Designer 155's pattern-library pieces can be used here as internal
building blocks, especially `IndexedTable`, `MonotoneSequence`, and
named packed keys. But package D should expose operation execution,
not just helpers.

### Package E - Implement read/query execution

Add `Match`, `Project`, `Aggregate`, and `Constrain` plan execution.
This replaces scan-and-filter patterns like `persona-mind`'s
`ThoughtSelector` and `RelationSelector` only once their filters are
represented as typed query plans.

### Package F - Implement subscription/changefeed execution

Add persisted query subscriptions, initial snapshots, and commit-time
delta matching. The actor owns delivery; Sema owns determining what
changed and which typed subscriptions match it.

### Package G - Reserve and later implement `Infer`/`Recurse`

Do not pretend those verbs are covered by a pattern library. Keep them
as explicit full-engine tracks.

## 6. What designer 155 should become

If `reports/designer/155-sema-db-pattern-library.md` remains narrow,
it should be reframed as:

> Layer 1: storage primitives needed by the full Sema engine.

It should not be framed as the answer to "Sema as database engine."
The four primitives are useful:

- `IndexedTable` helps maintain secondary indexes;
- `MonotoneSequence` helps mint typed counters;
- `scan_range` helps bounded scans;
- `define_packed_key!` helps named compound indexes.

But the full engine also needs:

- legal verb mapping at Signal boundaries;
- operation plans;
- operation log;
- validators;
- query planner;
- projection and aggregate execution;
- constrain/join execution;
- subscription/changefeed;
- schema/catalog introspection.

If designer modifies 155 toward full engine, it should either expand
into those packages or split the current pattern-library material into
a subreport under a larger full-engine design. The unacceptable middle
position is to call the pattern library "the Sema engine" while leaving
verb execution, query planning, operation logging, and subscription
change matching in every component.

## 7. Highest-signal immediate fixes

1. **Generate legal verbs in contracts.** This is the fastest way to
   stop semantic drift. It catches `InboxQuery` under `Assert` and
   makes the new intent executable.
2. **Rewrite all "default Assert" tests.** `signal-persona-message`,
   `signal-persona-introspect`, `signal-persona-router`,
   `signal-persona-system`, `signal-persona-harness`,
   `signal-persona-terminal`, and `signal-persona-mind` all need the
   manager/supervision pattern from `signal-persona`.
3. **Decide pushed event framing.** Subscription deltas can be replies
   tied to `Subscribe`; independent observations should be `Assert`
   requests in the reverse direction.
4. **Rebase `signal` and Nexus.** The sema-ecosystem path is still the
   oldest part: old `Query`, old parser, old assert-only compatibility.
5. **Treat designer 155 as foundational only.** It can land as the
   storage primitive layer, but it does not satisfy the full-engine
   intent by itself.

## 8. Recommended wording for the architecture

Add this to the relevant Signal/Sema architecture documents:

> Signal is the typed binary database-operation language. Every
> cross-component request is a `signal_core::Request` carrying a
> `SemaVerb` and a contract-owned typed payload. Each contract request
> variant declares exactly one legal verb. If a payload does not fit
> one of the existing verbs, the design must either reshape the
> payload or add a new verb.
>
> Sema is the database engine that executes those verbs over typed
> records. It owns database mechanics: table/index maintenance,
> commit sequence, operation log, validation execution, query planning,
> projection, aggregation, joins, and subscription change matching.
> Component daemons own sockets, authorization, actor mailbox order,
> domain policy, and delivery of post-commit effects.

That wording keeps the split precise: Signal says what operation is in
transit; Sema executes the database part; components own policy and
effects.
