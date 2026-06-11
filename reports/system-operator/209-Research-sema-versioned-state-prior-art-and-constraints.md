# SEMA Versioned State Research And Constraints

Variant: Research.
Role: system-operator.
Prompt source: psyche request on 2026-06-11 plus forwarded system-designer prompt.
Spirit gap-fill: Spirit record `avxy` captures the reusable-substrate constraint.

## Purpose

This report is a system-operator research pass, not an implementation choice.
The question is what a reusable SEMA version-control and backup substrate must
handle before we prototype it in `spirit` or another modern component.

The live constraint from the psyche is: SEMA state version-control and
server-backup must be reusable, probably in `sema-engine` or an adjacent
library, with minimal per-component code. Components should opt in rather than
reimplement log shipping, remote storage, restore, and history semantics.

## Current local facts

`sema` is still the storage kernel. It owns redb file lifecycle, rkyv format
guarding, schema-version guarding, typed table wrappers, and closure-scoped
transactions. It explicitly does not own operation logs, subscriptions, query
planning, or history.

`sema-engine` is the operation boundary. It owns registered record families,
write execution, `CommitSequence`, `SnapshotIdentifier`, commit log entries,
query snapshots, subscriptions, and component-facing receipts.

Today the engine log is not replayable. `CommitLogOperation` stores only
`SemaOperation`, table name, and optional key. `CommitLogEntry` stores
`CommitSequence`, `SnapshotIdentifier`, and non-empty operations. Assert and
mutate payload bytes are not logged. Retract is destructive at the storage
layer unless a caller captures prior state somewhere else.

The useful existing invariant is that the table mutation, commit-log entry,
and counters are written in one redb transaction. That should be treated as a
stage-one asset, not discarded casually.

## Prior art lessons

### Dolt

Dolt version-controls SQL tables by pairing a Git-style commit graph with
Prolly Trees. Its documentation is explicit that database version control needs
storage sharing across versions; full copies per change are untenable. Prolly
Trees give content-addressed roots, fast diff, and structural sharing for table
state. Source: [Dolt storage engine](https://www.dolthub.com/docs/architecture/storage-engine/).

What applies: content-addressed roots and commit metadata are useful for
integrity, deduplication, and remote sync. Schema/data roots inside a commit
are a good precedent for storing schema identity with the version.

What does not apply cleanly: SEMA's record bytes are rkyv archives of specific
Rust type sets, not dynamically typed SQL cells. A Prolly Tree over current
state can help if we need table-level diff of a large mutable keyspace, but it
does not solve type-changing migration. For many workspace stores, the log is
more natural than the table image.

### Noms

Noms is the closer ancestor behind Dolt: immutable content-addressed chunks,
datasets as named pointers into a DAG, commits with parent links, efficient
sync when the destination already has chunks. Source: [Noms intro](https://github.com/attic-labs/noms/blob/master/doc/intro.md).

What applies: immutable chunks and optimistic update of named roots map well to
remote storage. The named-root idea is useful for "component X state head".

What does not apply cleanly: Noms is a whole data model. SEMA already has typed
records, schema-generated contracts, redb locality, and component-owned actors.
Replacing the model is unnecessary; copying the root/chunk/sync invariants is
the useful part.

### Datomic

Datomic treats the log as chronological, transactional, accessible data, not
just an implementation detail. Its log is organized for transaction-range
access, and its architecture separates durable historical facts from derived
indexes. Sources: [Datomic Log API](https://docs.datomic.com/reference/log.html)
and [Datomic Cloud architecture](https://docs.datomic.com/operation/architecture.html).

What applies: the SEMA version-control layer should make the history a typed
domain artifact. Current redb tables should be treated as materialized views
or indexes over an authoritative history when versioning is enabled.

What does not apply cleanly: Datomic's datom model and query indexes are not
SEMA's typed Rust records. We should not import entity-attribute-value shape
unless the schema language independently wants it.

### EventStoreDB

EventStoreDB models writes as events appended to streams. Its client API uses
event identifiers for idempotence and expected stream revisions for optimistic
concurrency. It also separates event data from metadata. Source: [Kurrent
EventStoreDB appending events](https://docs.kurrent.io/clients/node/legacy/v6.2/appending-events).

What applies: a SEMA remote should validate expected predecessor state:
expected sequence, expected previous digest, or both. Idempotent append needs a
stable event/entry identity, not just "try sending this blob again."

What does not apply cleanly: EventStoreDB is stream-first and JSON-friendly by
default. SEMA entries must carry binary rkyv payloads plus typed schema and
record-family identity.

### SQLite WAL and Postgres PITR

SQLite WAL shows the local shape: write changes to a log first, checkpoint
them into the main database later, and manage checkpoint growth explicitly.
Postgres continuous archiving shows the backup shape: a restore needs a base
backup plus a continuous WAL sequence reaching back far enough. Sources:
[SQLite WAL](https://sqlite.org/wal.html) and [PostgreSQL continuous archiving
and PITR](https://www.postgresql.org/docs/current/continuous-archiving.html).

What applies: checkpoint is not optional cleanup. It is part of the protocol.
If old log prefixes are pruned, the system needs checkpoint identity, covered
sequence range, schema inventory, and behavior when a peer requests a pruned
head.

What does not apply cleanly: SEMA's desired history is logical typed operation
history, not physical page redo. Physical WAL backup would be a floor, not the
native reusable version-control substrate.

### Litestream

Litestream continuously copies SQLite WAL pages to replicas as a separate
background process, giving asynchronous disaster recovery. Source:
[Litestream how it works](https://litestream.io/how-it-works/).

What applies: a sidecar or background mirror can be a pragmatic asynchronous
mode, especially when low write latency matters. It also reinforces that async
replication has a real recovery-point window.

What does not apply cleanly: Litestream copies physical WAL pages. SEMA wants a
typed logical history that survives schema interpretation and can be checked by
entry digests.

### Irmin

Irmin is a Git-like distributed database for mergeable, branchable stores, with
built-in snapshotting and storage abstraction. Source: [Irmin](https://irmin.org/).

What applies: branch/snapshot/merge vocabulary is useful if we ever allow
independent writers or offline divergent state.

What does not apply cleanly: most SEMA component stores should stay
single-writer through their daemon actor. We should not add merge semantics
unless a component explicitly needs multi-writer divergence. Versioned backup
does not imply branches.

### CouchDB and CRDT systems

CouchDB replication is incremental and can preserve conflicting document
versions after divergent updates. CRDT systems such as Automerge optimize for
automatic convergence under concurrent edits. Sources: [CouchDB replication
and conflict model](https://docs.couchdb.org/en/stable/replication/conflicts.html)
and [Automerge](https://automerge.org/).

What applies: if the SEMA remote accepts multiple writers for the same store,
conflict policy becomes a real domain problem. Both-versions-exist or
automatic merge are deliberate semantics, not side effects.

What does not apply cleanly: the current component model is not local-first
multi-writer collaboration. We should keep the first implementation
single-authoritative-writer per component store.

### redb

redb is a pure-Rust embedded ACID key-value store with copy-on-write B-trees,
MVCC, crash safety, and single-writer behavior. Sources: [redb docs.rs](https://docs.rs/redb)
and [redb repository](https://github.com/cberner/redb).

What applies: the current redb transaction boundary is a strong correctness
anchor. It can carry a payload-bearing commit log in the same file while the
entry format stabilizes.

What does not apply cleanly: redb itself is not a distributed version-control
engine. Treating its whole file as the durable artifact gives us a backup
floor, not reusable typed history.

## Constraints to preserve

The storage substrate must be reusable. Component-specific code should supply
record-family descriptors, schema hashes, remote policy, and authorization
policy; it should not write its own append log, server protocol, replay engine,
or restore logic.

The substrate must preserve the SEMA layering. `sema` remains the typed redb
kernel. `sema-engine` or an adjacent crate owns the versioned operation
history. Components remain domain actors and lower domain operations into
engine calls.

The substrate must keep monotonic cursors. Content digests identify and verify
entries or heads, but `CommitSequence` remains the cheap ordered replay cursor.
Replacing all ordered markers with hashes would make ranges and subscriptions
more expensive than necessary.

The substrate must define remote durability levels. A write can be local-only,
locally queued for mirror, or acknowledged by the remote. These are different
contracts and must be explicit per store or per operation.

The substrate must make schema identity durable. Each entry or segment needs
the schema hash and record-family identity needed to decode payload bytes under
the type set that produced them.

The substrate must preserve migration executability or store post-migration
state. A reducer id alone is not enough; replay must either be able to fetch
the exact reducer/decoder artifact, probably by Nix closure or component build
identity, or use a checkpoint containing the post-migration values.

The substrate must preserve local read-after-write semantics unless a caller
explicitly chooses a weaker mode. A successful local write should be visible to
local reads and subscriptions immediately. Crash recovery may replay from the
authoritative log to repair a lagging view.

The substrate must treat checkpointing as core protocol. Checkpoints need
identity, covered sequence range, included schema hashes, table-family
inventory, previous checkpoint digest, retained suffix policy, and restore
behavior when a requested ancestor is pruned.

The substrate must have idempotent remote append. A server should validate
component/store identity, sequence continuity, previous-head digest, entry
digest, and duplicate entry identity. Retry should be safe.

The substrate must stay compatible with daemon startup rules. Daemons still
take one binary startup argument. Remote endpoints and mirror policy arrive as
typed configuration, not inline flags or NOTA parsed by the daemon.

The substrate must respect privacy and host boundaries. Private stores cannot
be mirrored into public repositories or public logs. The remote must know the
store's privacy class and destination policy.

## Open watch-fors for implementation

Authoritative envelope shape is the first hard design point. At minimum the
entry needs operation kind, table identity, key or engine identifier, schema
hash, record-family hash, payload bytes for assert/mutate, tombstone for
retract, sequence, previous entry digest, and entry digest over canonical
bytes.

Canonical bytes are not automatic. rkyv archives are bytes, but the entry
envelope itself needs a stable digest representation. We need decide whether
the digest covers rkyv of the envelope, a custom frame format, or schema-emitted
canonical bytes.

Retries need stable identity. EventStoreDB's event-id lesson applies: if the
same write is retried, the remote should recognize the same entry rather than
double-append it.

Remote acknowledgement policy changes latency and failure behavior. A
server-acknowledged write blocks on network and server fsync. An async mirror
keeps local latency but admits a recovery-point window. This should probably
be a per-store policy, not a global rule.

Separate-log files should not be first. The first semantic prototype should
keep the current redb transaction and add replayable payload history. Splitting
into an append-frame file is valuable after the entry format and restore tests
are real.

Component opt-in needs to be tiny. A plausible component surface is "open
engine with versioning policy" plus generated record-family schema hashes. If
every component has to hand-write a mirror client, checkpoint manager, and
restore code, the design has failed the captured intent.

Server shape should be a component, not a raw file drop. It needs ordinary
append/query/restore traffic and meta policy. The existing
`repository-ledger` pattern is useful: typed daemon, Signal client, actor-owned
store, spool fallback, and meta policy. It should not become a generic
line-oriented log sink.

Restore must be tested before backup can be called real. Tests should create
state, ship entries, rebuild a fresh local view from remote history, and verify
the current query surface matches.

Migration must be tested before schema-churn claims are credible. The first
prototype should include at least one old-shape to new-shape transition or a
simulated reducer/checkpoint boundary.

Branches and merges should stay out of the first version. The first production
need is single-authoritative-writer backup/version history. Git-like branches
are useful research vocabulary but not required for one-daemon component
state.

## Research conclusion

The best reusable shape to prototype is not "put redb under git" and not
"replace SEMA with Dolt." It is a typed logical history layer over
`sema-engine`, with monotonic ordered cursors plus content digests, idempotent
remote append, explicit durability policy, and checkpointed restore.

The first code experiment should prove three things with minimal component
code: payload-bearing commit history can rebuild component state, a remote can
accept entries idempotently under expected-head checks, and a component such as
`spirit` can opt into the mechanism through shared engine/library surfaces.

