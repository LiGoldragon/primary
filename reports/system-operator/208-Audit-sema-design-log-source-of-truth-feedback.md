# Sema Design Log Source-of-Truth Feedback

Variant: Audit.
Role: system-operator.
Source reviewed: `reports/system-designer/91-component-db-version-control/7-design-log-as-source-of-truth.md`.

## Verdict

The design move is basically right: if the workspace wants component Sema
databases to survive schema churn and be reconstructable off-machine, the
authoritative artifact has to be a typed, payload-bearing history, not a
redb current-state image plus a metadata-only audit table. The report also
correctly throws away the two weak imports from the earlier synthesis:
prolly trees for a random-edit SQL-shaped keyspace, and git as a native
content-addressing substrate.

The parts that need tightening before this becomes implementation guidance
are operational, not philosophical. A log-as-truth design still has to say
what "durable" means under crash, disk loss, server lag, schema migration,
and daemon read-after-write expectations. Without those answers it is a good
local event-sourcing proposal, but not yet the atomic server-backed database
durability design the original question asked for.

## What is strong

The report identifies the real source of the migration problem. rkyv bytes
belong to a specific type set, so a type-changing migration cannot be treated
as a byte diff between old and new table images. Moving schema identity into
the history, and making migration an explicit transition event, is the right
shape.

It also points at the right current gap in `sema-engine`: `CommitLogOperation`
is only `operation + table + key`, and `CommitLogEntry` is keyed by monotonic
sequence and snapshot identifiers. That log cannot rebuild state today. A
payload-bearing log is the smallest change that makes replay meaningful.

The other strong choice is narrowing the native design. For Spirit,
repository-ledger, attestations, deployment records, and similar component
state, append-only typed entries are the natural representation. A Merkle
B-tree over the materialized keyspace would mostly model the cache, not the
truth.

## Main corrections

### Keep monotonic markers beside content digests

The report says the head digest should replace today's
`SnapshotIdentifier(u64)` as the store identity. Do not make that replacement
in the first version.

`sema-engine` currently exposes monotonic markers as a behavioral API:
`CommitSequence` is the handover high-water mark, `SnapshotIdentifier` flows
through query snapshots, commit receipts, subscriptions, and
`commit_log_range`. A blake3 digest is an identity and integrity anchor; it is
not sortable, does not have `next()`, and cannot answer range queries without
an index.

Better shape:

- `CommitSequence` remains the ordered cursor.
- `SnapshotIdentifier` either remains as the local monotonic observation
  marker or is deliberately retired in a separate API break.
- `EntryDigest` / `HeadDigest` is added as the content-addressed identity.
- `DatabaseMarker` becomes sequence + snapshot + head digest, or sequence +
  head digest if snapshot is removed after all consumers move.

This gives sync a cheap ordered cursor and gives backup an integrity address.
Treating the digest as the only version turns every range/replay/subscription
path into an index problem.

### Define remote durability levels

The report makes local replay plausible, but the original constraint was
atomic server-backed versioned durability. "Ship the log suffix" is not enough
until the commit acknowledgement policy is explicit.

There are at least three different durability levels:

- Local committed: the entry is fsync'd locally and the materialized view is
  updated or catch-up-safe.
- Queued for mirror: the entry is in a durable local outbox, but the server has
  not accepted it.
- Server committed: the remote ingest has validated the previous head,
  appended the entry or segment, fsync'd it, and acknowledged the new head.

For state where loss is unacceptable, the component or engine policy must say
whether a write returns before or after server acknowledgement. Asynchronous
shipping is fine for some data, but then the design has a nonzero recovery
point objective and should name it honestly. If the promise is "server-backed
before success," the write path now includes network backpressure, retry,
timeout, and degraded-mode behavior.

### Same-file payload log should be the first semantic stage

The report argues for separating the authoritative log from the redb view
sooner because backup is the driving requirement. That is directionally
reasonable, but it should not be the first semantic move.

Today the log and table writes are in one redb transaction, which buys a
valuable invariant: the log entry and visible state cannot diverge. The first
implementation should keep that property while making the log payload-bearing
and replayable. A server mirror can still call `replay_from_sequence` or a new
entry-stream API and upload entries; it does not have to ship the raw redb file
or extract bytes from a B-tree as the native end state.

Split into an append-frame file after the entry envelope, digest rules,
checkpoint rules, and replay tests are stable. The separate-file design then
has a concrete format to write, not an architectural slogan.

### Authoritative replay needs a typed payload envelope

Adding `payload: rkyv bytes` is not enough by itself. `CommitLogOperation` is
not generic, while engine writes are generic over each registered record type.
The replay layer needs an envelope that records what decoder and table family
own those bytes.

Minimum envelope fields:

- operation kind: assert, mutate, retract, schema transition, checkpoint
- table name or stable table identifier
- record key or engine-assigned identifier
- schema hash / record-family hash that produced the bytes
- payload bytes for assert and mutate
- tombstone for retract
- optional prior digest or prior value if inverse time-travel/audit requires it
- entry digest over a canonical byte representation
- previous entry digest and monotonic sequence

Forward reconstruction of current state only needs new values plus retract
tombstones. Reverse time-travel, audit of replaced values, and "what exactly
changed" need either old values or a policy that old values are recovered by
replaying from an earlier checkpoint.

### Migration entries must preserve reducer executability

`SchemaTransition(v_old_hash -> v_new_hash, reducer_id)` is the right noun but
not a complete durability story. A reducer identifier is not replayable unless
the reducer artifact is preserved and addressable.

A robust transition entry needs to identify:

- old schema hash
- new schema hash
- reducer artifact hash or component release/build identity
- reducer input and output record-family mapping
- whether the transition stores only the reducer event or also stores the
  full post-migration values/checkpoint

For system deployment, this probably ties into Nix closure identity. If replay
ten months later requires the exact historical decoder and reducer, the log
must either retain that executable closure or retain enough post-migration
state that the reducer is only provenance. "spirit has historical readers" is
useful evidence, but it is not a general component-store guarantee.

### Preserve local read-after-write semantics

The separate-log version says the fsync'd append is the commit point and the
redb view is a follower that may lag. Current `Engine` callers get a stronger
local behavior: after commit succeeds, the written records are in the same
database view used by reads and subscriptions.

If the view is allowed to lag, the public semantics change. Components may see
a successful write and then fail to read it until catch-up completes. That may
be acceptable for some mirror paths, but it is probably not acceptable for the
core component-local engine.

Safer rule: local commits return only after the log is durable and the local
view has applied the entry, while crash recovery treats the log as the source
and replays any entry past the view watermark. The view can self-heal after a
crash; it should not normally lag behind the caller's successful write.

### Checkpoint and compaction are part of the design, not later cleanup

The report correctly names checkpointing, but it should promote checkpoint
format to a first-class design element. Once prefixes can be archived, sync by
"entries after digest X" only works when the peer's head is still in the
retained chain or is named by a checkpoint boundary the sender still has.

The protocol needs:

- checkpoint object identity
- included schema hashes and table-family inventory
- first and last covered sequence
- checkpoint digest and previous checkpoint digest
- retained suffix policy
- behavior when a peer asks from a pruned head

Without this, compaction can break the simple suffix protocol.

## Suggested staged implementation

Stage 1 should stay conservative: keep the current redb file and single
transaction, but make the commit log payload-bearing and hash-linked. Add
tests that delete/rebuild the materialized tables from the log in a temporary
database. Keep `CommitSequence` and `SnapshotIdentifier`; add digest fields.

Stage 2 should add a server mirror over the replayable entry stream. The
server validates sequence continuity and previous-head digest, writes
idempotently, and returns the accepted head. This stage must choose the
acknowledgement policy: async mirror, sync mirror, or per-store policy.

Stage 3 should introduce checkpoints with schema-hash inventory and replay
tests across at least one real migration. This is where the reducer artifact
identity must become concrete.

Stage 4 should split the authoritative log into an append-frame artifact if
the earlier stages prove the entry format and backup protocol. At that point
the redb view can become a pure follower with a durable applied watermark.

## Bottom line

I would accept the report as a design direction after edits, not as an
implementation spec. The central inversion is worth pursuing, and rejecting
prolly-tree/git cargo-culting is correct. The edits I would ask for are:
keep monotonic cursors beside digests, define remote acknowledgement semantics,
stage the payload log before the separate log file, specify the replay envelope,
make reducer artifacts durable, preserve read-after-write semantics, and make
checkpoint protocol part of the core design.

