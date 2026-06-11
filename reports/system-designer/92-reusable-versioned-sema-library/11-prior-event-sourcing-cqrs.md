# Prior art: event sourcing and CQRS

## Why this cluster is the direct shape of our direction

The accepted design direction — "version the LOG, not the store; make the commit log payload-bearing, hash-linked, and authoritative; demote redb tables to a rebuildable materialized VIEW" — is, structurally, the event-sourcing + CQRS pattern. The log of immutable facts is the write model and source of truth; the queryable tables are the read model (a projection) that can always be dropped and rebuilt by replaying the log. Every problem we have already chosen to take on (schema churn across rkyv type sets, server durability with a named RPO, checkpoints to bound replay, idempotent backup of a log suffix) is a problem this community has hit, named, and partially solved over fifteen years. This report mines what worked, what failed, and what transfers — it does not pick a design.

One alignment caveat up front, because it changes which lessons transfer: our shape is **Datomic-shaped, not aggregate-shaped**. Mainstream event sourcing (EventStoreDB, Axon, cqrs-es, Marten) is organised around *aggregates* — small consistency boundaries each owning a short event stream, replayed in isolation to rebuild one entity. Our `CommitLogEntry` (`sema-engine/src/log.rs:15-19`) is a single global monotonic sequence of commits over a typed table-space, closer to Datomic's single transaction log of datoms. Aggregate-stream mechanics (per-stream optimistic concurrency, snapshot-per-aggregate, short-lived streams) are the parts that transfer *least*; the log/projection/upcasting/checkpoint mechanics transfer *most*. Keep that filter active while reading.

## Today's seed, restated against the pattern

Our current commit log is a **CQRS read-model audit trail, not an event-sourcing source of truth**. `CommitLogOperation = {operation, table_name, key}` (`log.rs:63-68`, verified — `table_name` is stored as a `String`, `key: Option<RecordKey>`) is metadata-only: it records *that* a write happened, not *what* the value was, so it cannot be replayed to reconstruct state. The redb tables ARE the authoritative state today; the log merely narrates them. The direction inverts this. In event-sourcing vocabulary, we are proposing to move the payload from the table into the log entry and make the table a projection — exactly EventStoreDB's "events are the truth, read models are derived."

`SnapshotIdentifier(u64)` (`snapshot.rs:19`, verified, sequence-addressed) plays the role every system in this cluster has under a different name: EventStoreDB's per-stream revision and global `$all` position; Kafka's per-partition offset; Marten's event `sequence` / high-water-mark; Datomic's transaction `t`. The universal lesson from all four is that the **monotonic ordered cursor and the content hash are different objects with different jobs** — which is precisely the brief's "digests sit BESIDE the monotonic markers." No system in the cluster addresses log position by content hash; offsets/sequences/`t` are always integers because they must be sortable, have a `next()`, and answer range queries. Content hashing, where present (git substrate, Datomic's optional hashing), is layered *on top* for integrity/dedup, never used as the cursor.

## EventStoreDB / KurrentDB

### What it is and its core model
A purpose-built event-native database (rebranded KurrentDB in 2024; "engineered for it, not bolted on"). Events are immutable, appended to fine-grained per-key streams, scalable to billions of streams. Strict ordering within a stream; a global `$all` ordering across streams with a monotonically increasing position per event. Reads happen via *projections*, a subsystem that runs JavaScript inside the database to fold the event log into read models, derived streams, and integration triggers. ([kurrent.io event-sourcing](https://www.kurrent.io/event-sourcing), [Projections docs](https://docs.kurrent.io/server/v22.10/projections), [Streams docs](https://docs.kurrent.io/server/v22.10/streams))

### How it makes state durable / replicates
Append-only commit to disk with a global position index. Cluster durability is a leader/follower cluster with a consensus/quorum acknowledgement before a write is considered committed — this is the prior art for the brief's *durability levels* (local-committed vs server-committed). Persistent subscriptions track consumer position server-side so consumers resume after crash. ([Exploring the main features](https://www.kurrent.io/blog/exploring-the-main-features-of-eventstoredb-2/))

### Schema evolution story
Event-type + revision metadata on each event; consumers handle versioning by mapping/upcasting at read time. The 2024-2025 releases (26.1) added SQL access, a relational sink that auto-syncs read models into Postgres/SQL Server, a Kafka source connector, and a new projection engine — i.e. the read-model side is being pushed toward "declare the projection, the engine maintains it." ([KurrentDB 26.1 release](https://www.kurrent.io/releases/kurrentdb/26-1/), [Businesswire 2025](https://www.businesswire.com/news/home/20251216380370/en/))

### Reusable library vs monolithic service
Monolithic **service/daemon**, not a linkable library. Genericity is achieved by being *schema-agnostic at the storage layer*: events are opaque blobs (JSON/binary) with type+metadata; the database never deserializes domain types. This is the opposite of our constraint — we explicitly reject the opaque-blob store (Spirit 29pb: "native VC, not opaque blob") and our redb values are typed rkyv archives the engine understands.

### Worked / pain
Worked: the projection-rebuild-from-log story is battle-tested; persistent subscriptions with server-side position tracking. Pain: in-database JavaScript projections are operationally awkward and hard to test/version; the global `$all` position couples to physical storage and complicates partitioning.

## Apache Kafka as event log (+ log compaction)

### Core model
A distributed append-only commit log, partitioned, each partition strictly ordered with permanent integer offsets. CQRS-with-Kafka: producers append domain events; consumers build materialized views/projections; current-state is republished to a second **log-compacted topic keyed by aggregate id** that acts as a snapshot store, so a rebuilding consumer reads the compacted snapshot first, then tails the live stream. ([Conduktor CQRS+Kafka](https://www.conduktor.io/glossary/cqrs-and-event-sourcing-with-kafka), [RisingWave guide](https://risingwave.com/blog/practical-guide-to-event-sourcing-with-kafka/))

### Log compaction (directly relevant to our checkpoint/compaction protocol)
Compaction guarantees that the log retains **at least the last value for each key**, turning a topic into an eventually-consistent keyed snapshot. Mechanics ([Confluent log_compaction docs](https://docs.confluent.io/kafka/design/log_compaction.html)): the log splits into a **head** (dense, all offsets, uncompacted) and a **tail** (compacted, duplicate keys removed); a background **cleaner** recopies segments by a dirty-ratio trigger without blocking reads; a **tombstone** is a key with null payload that marks deletion and is itself removed after `delete.retention.ms`. Crucially: **compaction never reorders — offsets are permanent identifiers and surviving records keep original sequence.** Limitation Confluent states outright: a compacted topic gives you *current* state per key, **not** intermediate transitions — so it is unsuitable as the *sole* source of truth for a rigorous event-sourced history.

### Schema evolution
Solved out-of-band by the **Schema Registry** + Avro/Protobuf compatibility modes (backward / forward / full). Producers register schemas; consumers resolve via writer-schema id embedded in each record. This is the cleanest separation in the cluster: the *evolution policy* (compatibility rules) is a first-class registry concern, decoupled from both producer and consumer code.

### Reusable library vs service
Service (brokers) + thin client libraries; genericity again via opaque bytes + external schema registry. Kafka Streams adds an embeddable library for stateful projections backed by local RocksDB state stores with changelog topics for recovery — the closest Kafka analogue to "an embeddable library that maintains a local materialized view backed by a durable log."

### Worked / pain
Worked: the head/tail split and tombstone semantics are an exact, proven model for our **checkpoint + retained-suffix + pruned-head** protocol; the compacted-snapshot-topic pattern is the proven way to bound replay without losing the live tail. Pain: the explicit warning that compaction loses intermediate history is a direct caution against our checkpoint protocol silently destroying the audit trail Spirit needs (Spirit keeps a separate `*.archive.sema` precisely to retain retired records — `spirit/src/store.rs:retire`, verified).

## Marten (Postgres event store + projections)

### Core model
A .NET library layering an event store and document store over PostgreSQL. Events append to a single ordered table with a global `sequence`. Projections come in three lifecycles: **Inline** (run in the *same transaction* as the event append — strong consistency, read-after-write), **Live** (folded on demand at query time, nothing persisted), and **Async** (a background "async daemon" eventual-consistency processor). ([Marten projections](https://martendb.io/events/projections/), [Async daemon](https://martendb.io/events/projections/async-daemon.html))

### Most-relevant detail: Inline projection in the same transaction
This is the precise prior art for the brief's "the local view must NOT lag (read-after-write); only the remote mirror lags" and for our existing free-atomicity property (log + data committed in one redb transaction). Marten's Inline lifecycle proves you can keep the local projection exactly in step by writing it in the same unit of work as the event — the *async* lag is reserved for secondary/remote consumers, exactly our local-view/remote-mirror split.

### Schema evolution / rebuild
Projection rebuild = replay the log to regenerate the read model. Marten 7.30+ added `UseOptimizedProjectionRebuilds` (rebuild single-stream projection docs stream-by-stream in reverse last-modified order) — but it only works correctly **if exactly one single-stream projection uses a given stream**; multiple projections over the same events forbid the optimization. ([Rebuilding docs](https://martendb.io/events/projections/rebuilding)) For projection *schema* changes the recommended path is blue/green: bump `ProjectionVersion`, build the new projection in parallel into new tables, let it catch up async, then cut over. ([Optimizing docs](https://martendb.io/events/optimizing))

### Reusable library vs service
A genuine **reusable library** (the closest cluster analogue to our j487 ask) — no separate daemon process; the async daemon runs *inside the host application* as an `IHostedService`. But its genericity is C#-generics-plus-runtime-reflection over JSON documents; events/documents are serialized JSON, again the opaque-ish path we reject.

### Worked / pain
Worked: the inline/async lifecycle distinction maps 1:1 onto our local/remote durability split; blue/green projection versioning is the proven way to migrate a projection *shape* without downtime. Pain: rebuild is slow on large logs (universal finding, below); the optimized-rebuild correctness caveat is a warning that projection-overlap assumptions are fragile.

## Axon Framework (JVM, CQRS+ES+DDD)

### Core model
A reusable JVM framework of building blocks: aggregates, command/query/event buses, sagas, event store, snapshotting. Aggregate-stream-centric. ([Axon GitHub](https://github.com/AxonFramework/AxonFramework), [Baeldung guide](https://www.baeldung.com/axon-cqrs-event-sourcing))

### Schema evolution — the best upcasting model in the cluster (directly relevant)
Axon's **upcaster chain** is the strongest prior art for our `SchemaTransition(v_old_hash -> v_new_hash, reducer)`. ([Event versioning docs](https://docs.axoniq.io/axon-framework-reference/4.12/events/event-versioning/)) Key mechanics:
- Each event class carries a `@Revision` string; the selector is **(fully-qualified type name, revision)** — i.e. type-id + version, the same selector pair our envelope proposes (table id + schema-hash).
- Upcasters operate on an **`IntermediateEventRepresentation`**, NOT the deserialized domain object — they transform the *serialized* form, lazily, only when pulled from the chain. This is a clean answer to our rkyv fragility: you transform the wire/archive bytes between schema versions without ever holding two incompatible Rust type sets live.
- The chain **stacks**: each upcaster takes revision X to X+1; output feeds the next. You write one small upcaster per version step rather than one giant N-to-latest function. "It is paramount to maintain the ordering of the upcasters."
- Four upcaster shapes: single-event (1:1), multi (1:N), and context-aware variants (carry state across the stream — needed for N-to-1 / stream-folding transforms). This is richer than our single "reducer" word implies; a schema transition may need 1:N or N:1.

### Snapshotting (relevant caveat)
Snapshots are themselves versioned events typed by the *aggregate* class name + revision. Sharp warning: **only single-event upcasters apply to snapshots** (multi-upcasters are logically incompatible because only the final snapshot reconstructs state), and a `RevisionSnapshotFilter` will *prevent snapshot events from reaching upcasters* unless overridden. Translation for us: our **checkpoint** (the snapshot analogue) must be upcastable across schema versions too, and the rules for upcasting a checkpoint differ from upcasting a normal log entry — a checkpoint is a folded state, not a fact, so a 1:N transform on it is meaningless.

### Reusable library vs service
Reusable library (Axon Framework) optionally paired with Axon Server (the durable/replicated store as a service). Genericity via Java generics + annotations + reflection. The split — *library* for the typed building blocks, *server* for shared durability/replication — is exactly the boundary the brief asks us to map (linked VC library per component + shared server/mirror infra).

### Worked / pain
Worked: incremental, ordered, lazy, serialized-form upcasting is the gold standard. Pain: upcaster chains grow unboundedly over a system's life (every historical revision must stay supported forever unless you do a copy-and-transform rewrite); ordering bugs in the chain are silent corruption.

## Rust crates: cqrs-es, esrs, eventsourcing

### Core model and genericity mechanism (THE central-tension prior art)
`cqrs-es` ([docs.rs](https://docs.rs/cqrs-es/), [crates.io](https://crates.io/crates/cqrs-es), [guide](https://doc.rust-cqrs.org/)): generic over an `Aggregate` trait with associated types `Command`, `Event`, `Error`, `Services`, plus `apply(&mut self, event)` and `handle(&self, command)`. Events implement a `DomainEvent` trait that **requires `event_type(&self) -> String` and `event_version(&self) -> String`** — i.e. the versioning selector is *stringly-typed*. Persistence uses an `EventEnvelope` carrying `aggregate_type: String`, `event_type: String`, payload, and metadata; the `EventStore` trait is generic over Postgres/MySQL/DynamoDB/SQLite backends.

`esrs` (Prima): traits `Aggregate` (+ manager), `AggregateState`, `EventStore`, `StoreEvent`. `eventsourcing`: deliberately functional `apply` (state-in / state-out), no in-place mutation, for testability.

### Why this is the most important and most cautionary item for us
This is the cluster's only set of *Rust libraries built exactly as generic-traits-over-record-families* — literally the j487 ask. And every one of them **lands on the trade-off our discipline forbids**: to be generic over arbitrary event families they use a **stringly-typed `event_type`/`aggregate_type` selector** and treat the payload as an opaque serializable blob keyed by that string. `skills/abstractions.md` (perfect specificity: "the type carries meaning, not stringly-typed metadata") and the no-stringly-typed-fallback rule prohibit exactly this. cqrs-es proves the easy genericity path *works mechanically* and is *exactly what we must not do*. Our envelope's "schema-hash (the decoder selector)" is the typed alternative to `event_type: String` — a content-addressed identity of the rkyv type set rather than a human-typed name — and the open design question is how the engine maps a schema-hash to the right `Archive` decoder without a `String` match arm or a ZST namespace of free-function decoders (which the no-free-function / no-ZST-namespace rule also forbids).

### Worked / pain
Worked: trait-driven `apply`/`handle` cleanly separates fold logic from storage; functional `apply` is testable. Pain: stringly-typed event identity; no first-class schema-hash; upcasting is hand-rolled per project (Rust crates have no Axon-grade upcaster-chain abstraction — a gap we would be filling, not borrowing).

## Datomic (the closest model to our shape)

Worth naming explicitly because the brief calls us "Datomic-shaped, not Dolt-shaped." Datomic is a single, globally-ordered, append-only log of immutable datoms; transactions get a monotonic `t`/`tx` integer (the ordered cursor) and the database value at any `t` is a function of the log. Indexes (the read side) are materialized/rebuildable from the log. Schema is itself data (schema datoms in the same log) and is **additive-only** — attributes are added, never mutated in place — which sidesteps the rkyv-fragility problem by never having incompatible "type sets," only a growing attribute set. The transactor is the single writer (our single-redb-writer matches); peers/clients read locally (our local-view-must-not-lag matches). This is the cleanest fit for our log-is-truth + rebuildable-view direction, and its **additive-only schema** is a genuinely different evolution philosophy from Axon's upcasting — worth holding as a real alternative in the experiment matrix: *evolve by adding attributes (no upcast) vs evolve by upcasting between rkyv type-set versions*.

## The empirical study (industry reality check)

"An Empirical Characterization of Event Sourced Systems and Their Schema Evolution — Lessons from Industry" (Overeem et al., JSS 2021; 19 systems, 25 engineers). ([arXiv 2104.01146](https://arxiv.org/abs/2104.01146), [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0164121221000674)) Findings that bear directly on our risk register:
- **Five evolution tactics in the wild:** versioned events, weak schema, upcasting, in-place transformation, copy-and-transform. (Maps onto our SchemaTransition reducer choices.)
- **Five top pain points:** event-system evolution (the dominant one), steep learning curve, *lack of tooling*, *rebuilding projections (slow)*, and *data privacy*. Two of these are squarely ours: rebuild cost (our checkpoint protocol exists to bound it) and data privacy (our private-by-default discipline plus Spirit privacy `Zero` records — an append-only log of immutable facts collides with the right-to-delete, and "copy-and-transform" is the industry's answer because you genuinely cannot mutate the immutable log to redact). ([event-driven.io versioning patterns](https://event-driven.io/en/simple_events_versioning_patterns/))

## Experiment matrix the psyche wants tested (same-file vs separate-file log)

The brief asks for BOTH to be tested. Prior art frames the trade cleanly; it does not decide it:

### Option A — log table lives in the same redb file as the view (today's shape)
- **For:** the log and the projection commit in one redb transaction → free atomicity, log and view structurally cannot diverge (our current property, and Marten's Inline lifecycle proves it scales as a discipline).
- **Against:** compaction/checkpoint of the log fights the single-writer copy-on-write B+tree (redb 4.x has no online-snapshot path in use); pruning the log head rewrites the same file that serves reads; backup must extract a log suffix from inside a live mmap file.

### Option B — log in a separate append-only file/segment, view in redb
- **For:** matches Kafka's head/tail segment model and Datomic's log/index split; an append-only segment file is trivially suffix-shippable to the server (the brief's "ship the log suffix since the peer's last head"), compactable by segment, and content-hashable per segment without touching the read store.
- **Against:** loses free atomicity — a crash between "append to log segment" and "apply to redb view" must be reconciled (need an idempotent replay + a recorded "view-applied-up-to sequence", i.e. Marten's high-water-mark / Kafka's committed-offset). Idempotent replay is mandatory here (universal cluster requirement).

The decision hinges on which is cheaper to make correct: **same-file pays at compaction/backup time; separate-file pays at write/crash-recovery time.** Both are proven somewhere in the cluster.

## Boundary map: linkable library vs shared server (per the constraints)

The Axon split is the template the brief should weigh: **reusable typed building blocks as a linked library** (per-component, one redb handle per component, no shared daemon — satisfies our "one redb file per component, no shared sema daemon" rule) **+ a shared durability/replication service** (the server/mirror — `ouranos` as GitoliteServer + TailnetController is the backup INGEST target; `prometheus` is a backup STORAGE target with Btrfs; do not swap). The library is linked code inside each component; the server is shared infra. The boundary is exactly: *fold/apply/upcast/checkpoint logic and the typed log envelope = library*; *suffix transport, mirror acknowledgement, durability-level tracking = client-of-shared-server*.
