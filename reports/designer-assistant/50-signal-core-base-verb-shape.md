# 50 - signal-core base verb shape

*Designer-assistant report, 2026-05-14. Responds to
`reports/designer/161-how-to-research-signal-core-verb-roots.md`.
Scope: research the best shape for `signal-core` if every operational
Signal message must fit inside one of the base Signal verbs. This is a
design report, not an implementation patch.*

## 0. Bottom line

The current twelve-name list is useful vocabulary, but it is too wide
as **root verbs**.

Recommended `signal-core` root set:

```text
Assert  Mutate  Retract  Match  Subscribe  Atomic  Validate
```

The current extra names should move out of `SemaVerb` / `SignalVerb`
and into typed read-plan vocabulary:

```text
Constrain  Project  Aggregate  Infer  Recurse
```

The distinction:

- A **root verb** changes the message's boundary behavior: durable
  write, read, stream, transaction grouping, or dry-run mode.
- A **plan operator** changes how a read is computed or shaped inside
  `Match`, `Subscribe`, or `Validate`.

So every operational Signal message still fits under a base verb:

```text
message submission                -> Assert
component status query            -> Match
terminal observation query         -> Match
live observation feed              -> Subscribe
component desired-state change     -> Mutate
record removal / tombstone         -> Retract
multi-write unit                   -> Atomic
"would this pass?"                 -> Validate
join / projection / aggregate      -> Match payload operators
inference / recursion              -> Match payload operators
```

This is not a retreat from "Signal is the database-operation language."
It is a cleaner split between **operation root** and **query algebra**.

I also recommend renaming the public root enum from `SemaVerb` to
`SignalVerb` when the code changes. The type lives in `signal-core` and
classifies Signal frames. `sema-engine` executes many of those
operations, but not every Signal boundary is literally a sema-engine
call. If the workspace keeps `SemaVerb`, the architecture should at
least define it as "Signal's database-operation verb," not as an engine
implementation type.

## 1. Evidence from current workspace code

Current canon in `/git/github.com/LiGoldragon/signal-core/src/request.rs`:

```text
Assert Subscribe Constrain Mutate Match Infer
Retract Aggregate Project Atomic Validate Recurse
```

Current Nexus grammar in `/git/github.com/LiGoldragon/nexus/spec/grammar.md`
uses the same twelve as top-level text records.

Older implemented `signal` still has the smaller shape:

```text
Assert
Mutate
Retract
AtomicBatch
Query
Subscribe
Validate
```

That older shape is not correct as-is because `Query` should become
`Match`, and `AtomicBatch` should become `Atomic`. But it is evidence
that the operational root set was originally smaller than twelve.

`reports/designer/157-sema-db-full-engine-direction.md` already points
in the same direction even while naming twelve verbs: it defines
`QueryPlan<R>` with `Project` as a plan wrapper, and treats
`AggregatePlan` and `ConstrainPlan` as read-plan extensions. That means
the design text already half-knows that `Project`, `Aggregate`, and
`Constrain` are query operators, not root message behaviors.

## 2. External model check

### GraphQL

GraphQL has three operation roots: query, mutation, subscription. Its
selection sets, fields, aliases, and fragments shape the result inside
an operation; they are not separate root operations. The GraphQL spec
defines root operation types for "query, mutation, and subscription"
and says these determine where operations begin. It separately defines
selection sets as the way a client asks for the exact information it
needs.

Signal should learn the boundary lesson, not copy the exact three
names. Roots should be few and behavior-defining; result shaping lives
inside the payload.

### Datomic

Datomic is especially relevant because it treats requests as data.
Transaction data is data structures, not strings. It has primitive
assert/retract datom forms; transactions are atomic moments; queries
contain `:find`, `:where`, rules, pull expressions, and aggregates.
Datomic also exposes transaction reports for monitoring committed
transactions.

This supports:

- `Assert` and `Retract` as true roots;
- `Atomic` as transaction grouping;
- `Subscribe` as a transaction-report / commit-feed shape;
- `Project` and `Aggregate` as query-internal shapes, not roots.

Datomic's time APIs are also instructive. `as-of`, `since`, `history`,
and filters produce database values or filtered views that existing
queries can run against. "History" is not a root verb; it is a source
or view modifier for `Match`.

### Relational algebra and Datalog

Codd's relational model introduced a universal data sublanguage over
relations; relational algebra operators such as projection and joins
transform relations. They are algebra nodes inside a query plan.

Datalog is a query language based on logic programming over relational
data. Its rules, recursion, and deductive behavior support our names
`Infer` and `Recurse`, but as parts of read evaluation. If inference
materializes a new fact, the materialization is an `Assert`. If a
caller asks for derived answers, the root behavior is `Match`.

### SQL transactions

SQL/RDBMS tradition treats a transaction as a single logical unit of
work with atomicity, consistency, isolation, and durability. That
supports keeping `Atomic` as a root because it changes commit boundary,
not because "atomic" is a record operation like assert or retract.

## 3. Root-verb criterion

A name belongs in `SignalVerb` only if it changes at least one of these
at the Signal boundary:

| Criterion | Examples |
|---|---|
| Durable effect | `Assert`, `Mutate`, `Retract` |
| Read vs write behavior | `Match` |
| Streaming lifecycle | `Subscribe` |
| Transaction boundary | `Atomic` |
| Execution mode | `Validate` |

If a name only changes how a result is computed, joined, reduced, or
shaped, it is not a root verb. It belongs inside a typed payload.

This criterion gives exactly seven roots.

## 4. Per-name classification

| Current name | Keep as root? | Better home | Reason |
|---|---:|---|---|
| `Assert` | Yes | `SignalVerb` | Inserts/appends a typed fact/event/row. Boundary-visible write. |
| `Mutate` | Yes | `SignalVerb` | Transitions a stable identity. Boundary-visible write. |
| `Retract` | Yes | `SignalVerb` | Removes/tombstones a typed fact. Boundary-visible write. |
| `Match` | Yes | `SignalVerb` | Base read operation. Payload owns key/range/pattern/filter shape. |
| `Subscribe` | Yes | `SignalVerb` | Streaming lifecycle, initial snapshot plus deltas. Not just a one-shot read. |
| `Atomic` | Yes | `SignalVerb` | Sets transaction boundary for a bundle of writes. |
| `Validate` | Yes | `SignalVerb` | Runs validators/planner without commit; useful for agents. |
| `Constrain` | No | `ReadPlan::Constrain` | Join/unification across patterns. Query algebra, not boundary behavior. |
| `Project` | No | `ReadPlan::Project` | Result shaping. GraphQL/Datomic analogues put this inside query. |
| `Aggregate` | No | `ReadPlan::Aggregate` | Reduction/grouping over matched rows. Query-internal. |
| `Infer` | No | `ReadPlan::Infer` or rule set | Derived answers from rules. If materialized, the result is `Assert`. |
| `Recurse` | No | `ReadPlan::Recurse` | Fixed-point traversal. Query-internal; if persisted, it becomes write roots. |

## 5. Proposed signal-core shape

Signal-core should own the base operation roots and generic envelope,
not every possible query algebra node as a root verb.

Shape:

```rust
pub enum SignalVerb {
    Assert,
    Mutate,
    Retract,
    Match,
    Subscribe,
    Atomic,
    Validate,
}
```

The generic request envelope remains:

```rust
pub enum Request<Payload> {
    Handshake(HandshakeRequest),
    Operation { verb: SignalVerb, payload: Payload },
}
```

But construction should stop encouraging arbitrary verb/payload pairs.
Every domain request enum should implement or derive a contract-owned
mapping:

```rust
impl MessageRequest {
    pub fn signal_verb(&self) -> SignalVerb {
        match self {
            Self::MessageSubmission(_) => SignalVerb::Assert,
            Self::InboxQuery(_) => SignalVerb::Match,
        }
    }
}
```

Then the normal constructor should be payload-first:

```rust
impl<P: SignalRequestPayload> Request<P> {
    pub fn from_payload(payload: P) -> Self {
        Self::Operation {
            verb: payload.signal_verb(),
            payload,
        }
    }
}
```

The escape hatch, if any, should be named as unchecked/internal so
source scans can find it. The current convenience constructors
`Request::assert(payload)`, `Request::match_records(payload)`, and
friends make wrong pairings too easy.

For request enums with per-variant verbs, the `signal_channel!` macro
should accept verb annotations:

```text
request MessageRequest {
    Assert MessageSubmission(MessageSubmission),
    Match InboxQuery(InboxQuery),
}
```

and generate:

- `MessageRequest::signal_verb()`;
- constructor helpers that set the right verb;
- tests/witnesses that every variant maps to exactly one root.

## 6. Where the other five names go

The five demoted names still matter. They should not disappear from the
language; they should stop being frame roots.

Possible read-plan shape:

```rust
pub enum ReadPlan<R> {
    AllRows { table: TableRef<R> },
    ByKey { table: TableRef<R>, key: R::Key },
    ByKeyRange { table: TableRef<R>, range: KeyRange<R::Key> },
    ByIndex { index: IndexRef<R>, range: KeyRange<R::IndexKey> },
    Filter { source: Box<Self>, predicate: Predicate<R> },
    Constrain { sources: Vec<ReadPlanAny>, unify: UnificationPlan },
    Project { source: Box<Self>, fields: FieldSelection<R> },
    Aggregate { source: Box<Self>, reducer: AggregatePlan<R> },
    Infer { source: Box<Self>, rules: RuleSetRef },
    Recurse { seed: Box<Self>, edge: Box<Self>, mode: RecursionMode },
}
```

Then Nexus/NOTA changes from:

```text
(Project (NodeQuery (Bind)) (Fields [name]) Any)
(Constrain [(EdgeQuery 100 (Bind) Flow) (NodeQuery (Bind))] ...)
```

to:

```text
(Match (Project (NodeQuery (Bind)) (Fields [name]) Any))
(Match (Constrain [(EdgeQuery 100 (Bind) Flow) (NodeQuery (Bind))] ...))
```

or to a more domain-specific typed query record that carries the same
plan:

```text
(Match (ProjectedNodeQuery (NodeQuery (Bind)) (Fields [name]) Any))
```

The root says "this is a read." The payload says what read.

## 7. Pressure points

### Schema introspection

Fits `Match`: query the component's catalog / record-kind relation.
No new root.

### Permission / capability probes

Fits `Validate` if asking "would this request be accepted?" Fits
`Match` if reading the current capability/policy state. No new root.

### Schema migration

Fits `Mutate` or `Atomic`: transition the schema/catalog state under a
version guard. No new root.

### History / time travel

Fits `Match` with a snapshot/log/database-view source. Datomic's
`as-of`, `since`, and `history` support this reading: time changes the
database value or source being queried, not the top-level verb.

### Consensus / coordination

No root now. Local engine messages fit `Mutate`/`Atomic`. Distributed
consensus is a component protocol or future runtime layer, not a
database-operation root until concrete traffic proves otherwise.

### Handshake

Current `Request<Payload>` has `Handshake`. That is the one exception
to "all Signal messages fit a base verb." I would phrase the rule more
precisely:

> Every operational Signal request fits one base verb. Frame-control
> records such as handshake/version negotiation are transport setup,
> not database-operation messages.

If the user wants absolutely every frame body under a verb, the
candidate root is `Negotiate`, but I do not recommend it. It pollutes
the database-operation verb set with transport lifecycle.

### Replies and subscription deltas

Replies inherit the request's root verb; they do not need a separate
root. A subscription delta is part of a `Subscribe` stream. If a delta
is detached and sent as a standalone observation, model it as an
`Assert` of an observation fact.

## 8. Implementation consequences

If accepted, the code changes are straightforward but broad:

1. Rename `SemaVerb` to `SignalVerb`, or explicitly document why the
   old name stays.
2. Shrink the root enum to seven variants.
3. Move `Constrain`, `Project`, `Aggregate`, `Infer`, and `Recurse`
   into read-plan payload types.
4. Change Nexus grammar so every top-level request is one of the seven
   roots.
5. Extend `signal_channel!` so each request variant declares a root
   verb.
6. Remove or mark unchecked the free-form per-verb constructors that
   can wrap any payload under any root.
7. Add witnesses:
   - `signal_core_roots_are_seven`;
   - `query_algebra_names_are_not_signal_roots`;
   - `every_contract_request_variant_maps_to_one_signal_verb`;
   - `read_payloads_map_to_match_or_subscribe`;
   - `write_payloads_map_to_assert_mutate_retract_or_atomic`;
   - `validate_payload_wraps_a_supported_operation`;
   - `handshake_is_frame_control_not_signal_operation`.

This should happen before more contracts harden around the twelve-root
shape. The current engine is young enough that breaking this now is
cleaner than teaching every component that `Project` is a peer of
`Assert`.

## 9. Recommendation

Shrink root verbs to seven and preserve the remaining five names as
typed read-plan operators.

This produces a base verb set that is:

- small enough to be memorable;
- complete for current Persona traffic;
- aligned with GraphQL's root-operation lesson;
- aligned with Datomic's transaction/query split;
- aligned with relational/Datalog algebra as query-internal structure;
- precise enough that all operational Signal messages fit one root.

The old twelve-name list was valuable because it recovered the full
Nexus/Sema vocabulary. The next correction is to stop confusing
vocabulary with roots.

## 10. Sources used

Workspace sources:

- `reports/designer/161-how-to-research-signal-core-verb-roots.md`
- `reports/designer-assistant/43-nexus-query-language-and-sema-engine-arc.md`
- `reports/designer/157-sema-db-full-engine-direction.md`
- `skills/contract-repo.md`
- `/git/github.com/LiGoldragon/signal-core/src/request.rs`
- `/git/github.com/LiGoldragon/nexus/spec/grammar.md`
- `/git/github.com/LiGoldragon/nexus-spec-archive/README.md`
- `/git/github.com/LiGoldragon/signal/src/request.rs`

External primary / near-primary sources:

- GraphQL October 2021 specification:
  `https://spec.graphql.org/October2021/`
- Datomic transaction data reference:
  `https://docs.datomic.com/transactions/transaction-data-reference.html`
- Datomic transaction processing:
  `https://docs.datomic.com/transactions/transaction-processing.html`
- Datomic query reference:
  `https://docs.datomic.com/query/query-data-reference.html`
- Datomic database filters:
  `https://docs.datomic.com/reference/filters.html`
- IBM Research page for Codd's "A Relational Model of Data for Large
  Shared Data Banks":
  `https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks`
- Ceri, Gottlob, Tanca, "What You Always Wanted to Know About Datalog":
  `https://www.researchgate.net/publication/3296132_What_you_Always_Wanted_to_Know_About_Datalog_And_Never_Dared_to_Ask`
- Microsoft SQL Database Engine ACID overview:
  `https://learn.microsoft.com/en-us/sql/database-engine/sql-database-engine`
