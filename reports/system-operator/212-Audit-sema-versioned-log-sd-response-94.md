# SEMA Versioned Log SD Response 94 Critique

Variant: Audit.
Role: system-operator.
Source reviewed: `reports/system-designer/94-response-to-audit-211-next-slice-design.md`.

## Verdict

Report 94 is a good response to audit 211. It accepts the earlier critique
without defensiveness, keeps the same-file mainline as the production baseline,
and moves the next slice toward the right axes: per-family identity,
checkpointing, remote append, restore witness, and append-frame later.

I would accept it as the next design frame after corrections. The two blocking
corrections are:

- the checkpoint object is currently only checkpoint **metadata**; it does not
  carry or reference the snapshot payload needed to restore after pruning;
- remote durability levels must not pull network/server acknowledgement into
  `sema-engine` itself; the engine can record entries/outbox state, but a
  component or mirror actor must own transport and server fsync acknowledgement.

## What Is Strong

The report correctly states the reconciliation between mainline and SD's spike:
current `sema-engine` main is a conservative local-log subset, while the full
identity model still needs per-family schema identity. That is exactly the
right framing. The operator implementation should not be treated as finished
server-backed version control; it is the first stable local substrate.

The report is also right that store-level and family-level schema hashes answer
different questions. The store hash is a generation boundary. The family hash
is the decode selector stamped onto each operation. That distinction should
survive implementation.

The remote append contract is directionally right: expected-head validation,
idempotent duplicate handling, fsync before ack, and one server head per store.
That is the minimum shape needed before append-frame polishing matters.

## Blocking Corrections

### 1. A checkpoint must include or reference snapshot payload, not just metadata

Report 94 defines:

```rust
struct VersionedCheckpoint {
  store_name: VersionedStoreName,
  store_schema_hash: SchemaHash,
  family_inventory: Vec<SchemaHash>,
  covered: SequenceRange,
  view_digest: EntryDigest,
  previous_checkpoint_digest: Option<EntryDigest>,
  checkpoint_digest: EntryDigest,
  retained_suffix: RetainedSuffixPolicy,
}
```

That proves identity and integrity, but it cannot restore state. If a peer's
requested head has been pruned, "serve the nearest covering checkpoint plus the
suffix after it" only works if the checkpoint includes the materialized record
payloads or content-addressed references to them. A digest plus family inventory
can verify a snapshot after reconstruction; it cannot reconstruct the snapshot.

The checkpoint needs one more owned noun, for example:

- `VersionedCheckpointRecord { family, key, payload }`, stored in a checkpoint
  table keyed by checkpoint digest plus record ordinal; or
- `VersionedCheckpointSegment`, a content-addressed frame/chunk containing
  sorted family/key/payload records; or
- an explicit decision that the local redb tables are the checkpoint payload,
  plus a separate export format for remote restore.

Without one of those, report 94's reducer stance also fails. "Reducers are cold
provenance because every migration emits a post-migration checkpoint" is true
only when that checkpoint carries post-migration state, not merely a
post-migration digest.

### 2. Server-committed policy cannot live as a simple `VersioningPolicy` field

Report 94 says durability levels become a per-store policy on
`VersioningPolicy`: local committed, queued-for-mirror, server committed. The
policy vocabulary is right, but placement needs care.

`sema-engine` is a library-only crate. It has no daemon, tokio runtime, actor
plane, socket, NOTA parser, or component-specific authorization surface. A
`sync-server-committed` policy cannot mean "hold the redb write transaction open
while networking happens." It also cannot mean "return an engine write as
failed after the local transaction committed but the mirror failed" unless the
caller receives a typed partially-committed outcome.

Better split:

- `sema-engine` writes the domain mutation, metadata log, versioned log, and a
  durable mirror-outbox row in one local transaction.
- A component-owned mirror actor or reusable mirror component ships outbox rows
  to the remote and records server acknowledgements.
- A synchronous durability policy is implemented at the component request layer:
  after the local engine commit, the request waits for the mirror actor to ack
  the commit sequence/head digest. The redb transaction is already closed.
- The reply type must distinguish local commit from server commit if the server
  path fails after local durability.

That preserves `sema-engine`'s boundary and still lets Spirit-class stores apply
backpressure for server acknowledgement.

## Major Corrections

### 3. `FamilyIdentity` needs stable family identity, not only table plus schema hash

`FamilyIdentity { table: TableName, schema_hash: SchemaHash }` is close, but
`TableName` is a storage coordinate. It is not necessarily the stable semantic
record-family identity across table renames, table splits, or table merges.

The design likely needs three fields:

- stable family name or identifier: semantic family, generated from the
  component record family;
- table name: current storage coordinate;
- schema hash: versioned decode selector for that family shape.

This avoids treating a table rename as a new ontology or, worse, treating two
different families that share a storage table as the same family.

### 4. Store schema hash should be derived, not manually asserted

Report 94 keeps the store-level schema hash from `VersioningPolicy`. That is
fine as an API surface today, but the durable design should derive the store
hash from the registered family inventory and component schema version, not from
a manually supplied label such as Mind's current `mind-schema-v7`.

Manual labels drift. If a family changes but the label does not, the log lies.
The safer shape is a generated `StoreIdentity` or `StoreSchemaIdentity` built
from sorted `FamilyIdentity` entries and stamped onto the engine after
registration. A hand-authored override can exist only as a transitional
bootstrap, not as the source of truth.

### 5. Use a commit-sequence range type, not existing `SequenceRange`

The report uses `SequenceRange` for `first..=last commit_sequence`. In current
`sema-engine`, `SequenceRange` is a subscription/log range over
`SnapshotIdentifier`, not `CommitSequence`. Reusing it here would muddle the
two monotonic markers audit 211 explicitly kept separate.

Checkpoint coverage should be `CommitSequenceRange` or another newtype whose
fields are `CommitSequence`.

### 6. Restore needs an engine API, not just a remote protocol

Report 94 says the restore witness should rebuild a fresh store and assert the
normal query surface reads the same records. That is the right witness, but the
design does not yet name the API that applies historical versioned entries into
a fresh engine.

It cannot be ordinary `assert` calls if the restored store must preserve the
original commit sequences, snapshots, head digest, tombstones, and operation
bundles. It needs a restore/import path that can write:

- domain table rows from checkpoint payload or log entries;
- versioned commit log entries with original sequence and digest;
- metadata commit log/counters to the restored high-water mark;
- checkpoint rows and mirror-head state.

This import path should be engine-owned, typed, and probably unavailable to
ordinary component mutation handlers.

## Smaller Notes

`TableName` is currently a `&'static str` wrapper and `TableRegistration` stores
a `String`. Saying `TableName` "kills the stringly leak" overstates it unless
the archived catalog stores a typed durable table-name newtype rather than a
bare string projection.

The remote append request "already carries everything needed" is true only
after per-family identity and checkpoint payload exist. Today a
`VersionedCommitLogEntry` carries store hash plus table-name strings and
payload bytes; that is not enough for typed restore across schema versions.

The remote server contract should include authorization/privacy class and
write-once retention policy soon. It does not need to block the first local
identity/checkpoint work, but server-backed Spirit-class state cannot ignore
who may append or prune a store.

## Recommended Edits To Report 94

1. Rename the checkpoint section from "checkpoint object" to "checkpoint
   metadata plus snapshot payload" and add the missing payload noun.
2. Replace `SequenceRange` with `CommitSequenceRange`.
3. Split durability policy into engine-local policy and mirror-actor policy.
4. Expand `FamilyIdentity` to include stable family identity separate from
   table name.
5. State that store schema hash is generated/derived from the family inventory,
   not manually labeled long term.
6. Add the restore/import API as a named next-slice design item before the
   restore witness.

## Bottom Line

Report 94 is the right next conversation, but it still describes a checkpoint
that cannot restore and a server-commit policy without the actor boundary that
would make it safe. Fix those two, and the next slice can move from concept to
implementation: per-family identity first, checkpoint payload second, local
outbox plus remote append third, restore/import witness fourth.

