# Prior art: the Datomic family (Datomic, Datahike, XTDB, DataScript)

## Scope and why this family

The psyche wants a reusable library that lets any component version-control its durable Sema state — server-backed, atomic, surviving schema churn (Spirit 29pb, j487). The design direction so far is "version the LOG, not the store": make the commit log payload-bearing, hash-linked, and authoritative, and demote redb tables to a rebuildable materialized view (reports/system-designer/91/7; audit 208).

The Datomic family is the load-bearing prior art because it is the canonical realization of exactly that inversion: an immutable, accumulate-only log of facts is the system of record, and the queryable indexes are *derived materialized views* over that log. Our `CommitLogEntry { commit_sequence, snapshot, NonEmpty<operation> }` (sema-engine/src/log.rs:15-19) and `SnapshotIdentifier(u64)` (snapshot.rs:19) are a primitive, metadata-only version of the same shape — the brief is correct that today's `CommitLogOperation { operation, table_name, key }` (log.rs:63-68) is NOT replayable into state. This report maps four members and their kin against our brief; it does not choose a design.

A through-line up front: every member of this family is **schema-as-data with an open universe of attributes**, which is how they sidestep the schema-fragility problem that bites us hardest. We are the opposite — rkyv archives are byte-fragile per type set, and spirit already pays for this with eight frozen schema versions (`SpiritStoreV1Database` .. `SpiritStoreV7Database`, production_migration.rs:89-116, plus the current V8). That divergence is the single most important "does not apply" in this whole report, and it shapes which of their techniques transfer.

## Datomic (the reference design)

### What it is and its core model

Datomic is a closed-source immutable database built on the **datom**: an atomic fact `[Entity Attribute Value Transaction op]` where `op` is assert/retract. Information is only ever *accumulated* — nothing is updated or deleted in place; a "change" is a new assertion (and, for cardinality-one attributes, an automatic retraction of the prior value). A database value is an immutable snapshot you can hold, pass, and query as of any point in time.

### How it version-controls / replicates / durability

The architecture cleanly separates the three concerns our brief is trying to separate:

- **Transactor**: a single process that serializes all writes, commits log segments to storage, and broadcasts novelty (push-based) to peers. It owns no storage and serves no reads — exactly our "single-writer, server is the durability target" intuition. It is also the family's most-cited weakness: a single point of write-serialization and a bottleneck under heavy write load.
- **Log**: all datoms sorted by transaction id — **sequence-addressed by transaction**, efficient for transaction-range scans, not for queries. This is the authoritative write record. (tonsky internals guide)
- **Indexes** (EAVT, AEVT, AVET, VAET, plus Log): B-tree-like, sorted, immutable, persistent, ~1000+ branching factor, no more than three levels deep (root → directories → segment leaves). These are **materialized views derived from the log** — the literal embodiment of "demote the store to a rebuildable view."
- **Storage** is just a key-value mapping of **segment-key (UUID) → compressed segment body** (Fressian-serialized, zipped, ~50 KB / 1k–20k datoms), plus a CAS primitive for updating index-root records. Backends: DynamoDB, Cassandra, JDBC SQL, Riak, etc. Datomic requires only *two* things from storage: a KV interface and compare-and-swap on the root.
- **Read merge**: each index has three layers — durable History, durable Current, and an ephemeral in-memory novelty index (assertions + retractions) held in transactor and peer memory. Queries merge Current + in-memory to give the illusion of querying live state. When in-memory novelty exceeds a threshold, the transactor reindexes (merges current + novelty into a new durable index root), peers learn the new root and drop covered novelty, old segments become GC-able.

Durability is "write to log + write to in-memory index, then propagate." Peers read directly from storage and cache expanded segments; a peer's `db` call returns the latest value it has heard of without round-tripping the transactor.

### Schema evolution

Schema *is* data: attributes are entities with `:db/ident`, `:db/valueType`, `:db/cardinality`. Evolution is **accretion** — the "Ten Rules of Schema Growth" classify migrations as *growth* (add new attributes; production-safe; effective immediately, online, no downtime) vs *breakage* (repurpose/narrow an existing attribute; dev-only at best). Renaming an attribute is a synchronous transaction changing the `:db/ident`; the old name keeps working until repurposed, enabling incremental rollout. There is no offline "migrate the whole store" step in the growth path.

### Reusable library vs service

Split deliberately: the **peer library** (a JVM library: database value code, connection, memory index, query engine) is embeddable in every app server as a co-equal; the **transactor** is a shared service. Genericity is by *data*, not types — the open attribute universe means one engine serves every schema with no per-schema code. Datomic Cloud variant pushes more into managed infra (Ions, query groups).

### What worked / what did not

Worked: log-as-truth + derived indexes; immutable snapshots; storage-pluggability via a tiny KV+CAS contract; online additive schema growth; reading without contending on the writer.

Did not / pain: transactor write bottleneck and single-point-of-failure; **covering-index redundancy** (a datom in 3 indexes is stored 3×, inflating storage); AVET is the problematic index, wants monotonic values; "move all data to the client" hits a working-set ceiling and degrades on large datasets; **excision** (the only way to truly erase across history, for GDPR) is costly and triggers massive index rewrites — the accumulate-only model fights right-to-be-forgotten; explicit anti-pattern: do NOT put high-volume operational logs in Datomic (it is a system-of-record, not a log sink).

## Datahike (the open, embeddable, library-decomposed cousin)

### What it is

An open-source (Eclipse) durable Datalog DB with Datomic-compatible APIs and **git-like semantics**. Originated as DataScript (the in-memory engine) made durable by swapping its in-memory index for the **hitchhiker-tree**, persisted through **konserve**. EAVT-style datoms; immutable snapshots.

### Durability / replication and the LIBRARY DECOMPOSITION (most relevant to j487)

This is the family member whose *packaging* maps most directly onto our reusable-library goal, because Datahike is explicitly factored into independent, separately-reusable libraries:

- **hitchhiker-tree** (replikativ/datacrypt): a functional, persistent, off-heap index combining B+ tree query performance, append-log write performance, and immutable snapshots with structural sharing. Reusable on its own.
- **konserve**: a pluggable key-value store *abstraction* with backends for File, LMDB, S3, JDBC, Redis, IndexedDB. The hitchhiker-tree targets konserve; konserve targets any storage. This is the clean "generic storage trait + many backends" boundary — and it is a *separate* library, not baked into the engine.
- **kabel**: a separate transport library (WebSocket streaming, browser ↔ server) for real-time sync.
- The DB-as-value is a hitchhiker-tree of addressable nodes; replication is "ship persistent index nodes," and readers can access persistent indices directly ("read scaling without database connections").

Packaging: primarily a *library* (JVM `org.replikativ/datahike`, npm `datahike@next`, GraalVM-native `dthk` CLI, plus Java/Python/C bindings via libdatahike). Embedding is the default; there is no mandatory central service.

### Schema evolution

Schema-on-write by default ("strict schema, keep all historical data"), but a configurable **`:schema-flexibility`** knob (`:write` vs `:read`) lets you relax to schema-on-read. Same accretion philosophy as Datomic. Supports time-travel (`history`, as-of/since) and GDPR purge.

### What worked / did not

Worked: the three-library decomposition (index / storage-abstraction / transport) is the cleanest example of "build the mechanism ONCE as reusable generic pieces" in the family — directly answering j487's shape. Did not: smaller ecosystem, branching API less mature than the marketing implies, CRDT/eventual-consistency replication path (replikativ) is its own complexity; durability inherits konserve backend semantics.

## XTDB (2.x) — the schema-on-read, log-coordinated columnar variant

### What it is and core model

A bitemporal immutable SQL+Datalog database (JUXT). Tracks **system time** and **valid time** on every row automatically. 2.x is a ground-up columnar rebuild: storage/compute separated, everything stored internally as **Apache Arrow**, an object-store LSM-tree with bitemporal historical partitioning.

### Durability / replication

**The log is the central coordination point.** All nodes in a cluster are stateless replicas reading from a single shared write-ahead log; durable storage is commodity object storage holding Arrow files. This is "log as truth, nodes are derived" at cluster scale — very close to our direction, but realized over an object store rather than a single local file. Nodes can also be **embedded in-process** (JVM/Clojure/Kotlin/Java); non-JVM clients must go over HTTP.

### Schema evolution — the sharpest contrast with us

XTDB 2.x is **schema-on-read**: no upfront schema, tables asserted on the fly, arbitrarily nested data, and **dynamic self-describing type information attached per value** from a fixed range of native Arrow types. "You don't need schema migrations when your data structure evolves" — new columns appear dynamically. Columns are sparse (NULLs cheap) and wide.

This is the polar opposite of rkyv's fixed-layout archives. XTDB pays a per-value type-tag cost to buy zero migration; we pay zero per-value overhead (zero-copy) but a full-rewrite migration per schema version. The brief's `SchemaTransition(v_old_hash -> v_new_hash, reducer)` is essentially choosing to keep our cheap-read / fragile-layout tradeoff and make the *transition* a first-class typed log entry, rather than adopting XTDB's self-describing-value escape hatch.

### What worked / did not

Worked: log-as-coordination with stateless replicas; bitemporality as a built-in (no manual valid-time columns); columnar retention economics for large histories. Did not / watch: 2.x is still beta-era (v2.2.0-beta1); object-store latency characteristics; schema-on-read pushes type discipline to query time — directly contrary to our "perfect specificity, type carries meaning" rule.

## DataScript (and persistent kin: Datalevin) — the pure embeddable library

### What it is

An immutable in-memory Datalog DB and query engine in Clojure/ClojureScript/JS, built from scratch (explicitly *not* Datomic-derived). Immutable, persistent-data-structure-backed, cheap to create, meant to be ephemeral and run in-browser. Attributes need not be pre-declared. Intentionally omits persistence, wire transfer, server sync, pluggable storage (in the classic form), full-text, partitions.

### Durability / serialization — directly relevant to our same-file-vs-separate-file experiment

DataScript's two persistence stories map onto our two experiment arms:

- **Whole-DB serialization** (`db->string` / `datascript-transit` `write-transit-str`/`read-transit-str`, or custom `:freeze-fn`/`:thaw-fn`): serialize the entire DB value to one blob — the analogue of spirit's current full-rewrite-plus-`fs::rename` migration and a "single .sema file" mental model.
- **Pluggable segment storage** (`IStorage`, added ~1.7): the DB B-tree is stored as **individually addressable nodes**, each with a 64-bit address (new nodes have null until stored). The four-method protocol is `-store [_ addr+data-seq]`, `-restore [_ addr]`, `-list-addresses [_]` (for GC), `-delete [_ addrs-seq]`. **Restore does zero reads — it is lazy**; nodes load on access (a `(first (d/datoms db))` is ~3–6 reads). Structural sharing means a write only persists changed nodes; orphans are reclaimed by `d/collect-garbage`. Addressing is **address-keyed, not content-addressed**.

This is the cleanest small contract in the family: a four-method storage trait + lazy node loading + GC. It is a concrete model for "segments as the durable unit, view rebuilt lazily," and its address-keyed (not content-addressed) choice is a useful counterpoint to our hash-linking direction.

**Datalevin** is DataScript ported onto **LMDB**: it *keeps DataScript's library property* (embedded, in-process) but adds disk durability, larger-than-memory data, LMDB ACID, and a cost-based query optimizer. It is the proof that the embeddable-library shape and server-grade durability are not mutually exclusive — the same lesson j487 is betting on. (No Rust port exists; it is JVM/Clojure.)

## Cross-cutting comparison

| Dimension | Datomic | Datahike | XTDB 2.x | DataScript / Datalevin |
|---|---|---|---|---|
| System of record | Log (txn-ordered) | hitchhiker-tree in konserve | Shared WAL + Arrow object store | DB value (mem) / LMDB |
| Indexes as | Derived materialized views | Derived (hh-tree) | Derived columnar | Derived (in DB value) |
| Log addressing | Sequence (txn id) | Tree node addresses | Log offset | Node address (64-bit) / — |
| Content-addressed? | No (segment UUID) | Node-addressed | No | No (address-keyed) |
| Schema model | Schema-as-data, accretion | Schema-on-write, flexible | Schema-on-read, dynamic | No declared schema |
| Migration story | Online additive growth | Additive + flexibility knob | None needed (self-describing) | Re-serialize / node-level |
| Library vs service | Peer lib + transactor service | Library (3 sub-libs) | Embeddable node or cluster | Pure library |
| Genericity mechanism | Open attribute universe (data, not types) | Separate konserve/hh-tree/kabel libs | Arrow self-describing values | Datom is the only type |
| Erase-across-history | Excision (costly) | GDPR purge | Bitemporal erase / valid-time | n/a |

## How this informs (not decides) our experiment matrix

The psyche wants both same-file and separate-file log tested. The family gives evidence on each side, not a verdict:

- **Same-file (log + view in one redb transaction)** — today's sema-engine design (log table inside the component's `.sema`, written in the same redb txn as data; free atomicity, view and log cannot diverge). DataScript's `db->string` whole-blob and Datalevin's single-LMDB-environment are the "everything in one durable unit" analogues. Strength: trivial atomicity, no two-store reconciliation. Tension: backup = ship the log suffix, but the log is entangled with the materialized view in the same file.
- **Separate-file log** — Datomic's clean split (log + index segments are distinct storage keys), XTDB's WAL-separate-from-Arrow-files, and DataScript's `IStorage` (log/segments as independently addressed nodes) all separate the authoritative record from the derived view. Strength: the log suffix is independently shippable; the view is freely rebuildable/prunable without touching the source of truth. Tension: cross-file atomicity must be re-established (the free atomicity of the same-redb-txn is lost); needs a checkpoint/recovery protocol like Datomic's index-root CAS.

The deepest transferable lesson for both arms: **make the log payload-bearing and replayable** (which ours is not yet — log.rs:63-68 is metadata-only), because every member of this family rebuilds its queryable view from the log. The deepest *non*-transferable lesson: their open/self-describing schema universe is what lets them avoid migration entirely; we deliberately keep fixed-layout rkyv, so we must invent the typed `SchemaTransition` log entry they never needed.

