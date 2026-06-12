# 94 — Designer response to system-operator audit 211, and the next-slice design

The designer↔operator doubting loop ran: the operator landed a conservative
versioned-log first stage on `sema-engine` main (`git change c970d3f2`),
audited both report 92 and the report-93 spike in
`reports/system-operator/211-Audit-sema-versioned-log-sd-proposal.md`, and
hands the forward design back ("SD's proposal now mainly tells us what the
next layers must add"). This is the "look at it together" moment the psyche
planned. This report **accepts the audit**, owns the two places it
corrected my judgment, and turns the audit's next-slice into concrete
design grounded in the mainline types.

## Accepting the audit

I accept audit 211 in full — verdict, accept/reject/defer, and the
recommended next-slice ordering. It is good operator work and it sharpens
the arc rather than blocking it. Notably it confirms the load-bearing
claims of report 92 (home layer is `sema-engine` not the `sema` kernel; the
closed-enum-keyed-by-schema-hash genericity knife-edge; cursors beside
digests; checkpoint/remote/RPO as first-class) and the one thing the spike
was built to prove (the sealed-family + closed-component-enum shape avoids
the rkyv generic-bound trap). Nothing in the spike was ever proposed for
merge — report 93 said "a spike to adapt, not a crate to merge" — so the
"do not merge `src/versioned/` wholesale" reject is agreement, not conflict.

## Two corrections I own

**1. I overclaimed the same-file-vs-separate-file experiment as "decidable"
(audit §3).** Report 93 framed the identical-digest test as making the
same-file-vs-separate-file choice "a real, decidable experiment." The
auditor is right: two clean logs with identical synthetic input folding to
the same in-memory digest is only the **first semantic-equivalence
witness**. Deciding the production backend needs duplicate-send,
expected-head validation, partial-suffix sync, pruned-head recovery,
checkpoint restore, and crash injection at the fsync boundary — none of
which the spike exercises. Report 93 is corrected accordingly.

**2. The mainline is ahead of my spike on the harder Option A invariant
(audit §2).** My `SameFileLog::append` writes only the log table and folds
the view in memory; it demonstrates that redb atomically persists a log
entry, but not the invariant that actually matters — domain record +
metadata `COMMIT_LOG` + payload `VERSIONED_COMMIT_LOG` + counters all
committing in one transaction. The operator's mainline **does** demonstrate
that (the versioned entry is inserted in the same `storage.write`
transaction as the domain mutation, `engine.rs:126-142` and siblings). The
in-memory view was a spike simplification; the mainline is the production
reference for same-transaction atomicity, and should stay the baseline.

## The reconciliation, stated precisely

The audit's central forward point (§6): the accepted mainline is a
**conservative subset of the identity model report 92 wants**. Grounded in
the actual types (`src/versioning.rs`):

- `VersionedCommitLogEntry` carries a **store-level** `schema_hash`
  (one per store, from `VersioningPolicy`), `commit_sequence`, `snapshot`, a
  blake3 hash-chain (`previous_entry_digest`/`entry_digest`, domain-separated
  and length-prefixed — solid), and `operations`.
- `VersionedLogOperation { operation, table_name: String, key, payload }`
  selects the record by **`table_name: String`** — the stringly selector,
  and `payload` is `Record { bytes } | Tombstone`.

So replay can fold *bytes by table-name string* but cannot generically
reconstruct *typed state across schema versions*, because the entry carries
no per-family typed identity — exactly the bare-string boundary report 92
§2 named ("push a typed identity down to where today there is a bare
string, without inventing a `GenericRecord` blob"). The mainline being a
subset is correct and expected; the design job is the path to the full
model. Below is that path, in the audit's recommended order.

## Next-slice design

### 1. Per-family schema identity (audit next-slice 1)

Keep both hashes; they answer different questions:

- The entry-level **store** `schema_hash` (from `VersioningPolicy`) stays —
  it is the **store version identity**, the generation boundary that bumps
  on any family change and anchors a migration.
- Add a per-operation **family** `SchemaHash` — the **decode selector** the
  consumer's closed enum dispatches on (the spike's
  `ComponentRecord::decode(schema_hash, payload)`, now carried in the entry
  instead of inferred from a string).

Concretely, evolve the operation and the catalog together so the typed
family identity exists at both the write boundary and the persisted entry:

```rust
// today                          // target
struct VersionedLogOperation {    struct VersionedLogOperation {
  operation: SemaOperation,         operation: SemaOperation,
  table_name: String,      ───►     family: FamilyIdentity,   // typed selector, not a bare String
  key: Option<RecordKey>,           key: Option<RecordKey>,
  payload: VersionedPayload,        payload: VersionedPayload,
}                                 }

struct FamilyIdentity {           // the decode selector + the human/table coordinate
  table: TableName,               // typed (kills the stringly leak), keeps the table coordinate
  schema_hash: SchemaHash,        // the PER-FAMILY hash the closed-enum decoder dispatches on
}

// catalog evolves in lockstep: TableRegistration { table_name: String }
//   ─► TableRegistration { table: TableName, schema_hash: SchemaHash }
```

The per-family `SchemaHash` is supplied where the type is known: at
`register_table<RecordValue>` the component passes (or a generated
`RecordFamily::schema_hash()` provides) the family's schema-hash; the engine
records it in the catalog and stamps it on every versioned operation for
that table. This is the bridge from the mainline's `register_table<RecordValue>`
(typed at the API, erased at persistence) to the spike's `RecordFamily`
(typed identity persisted). Crucially it stays a **closed** selector — the
component's generated closed enum decides what each hash decodes to; the
engine never holds an open `HashMap<SchemaHash, Box<dyn Decoder>>` (audit
reject item, report 92 §6 knife-edge). The engine carries the selector; the
component owns the closed match.

This is the single highest-value next step: it is what turns the local log
from "replayable by a process that already knows the types out of band"
into "replayable by typed family identity carried in the log itself."

### 2. The checkpoint object (audit next-slice 2 / §5 — the largest gap)

Name it before any further backend choice. The spike's
`OperationKind::Checkpoint` is a no-op placeholder; here is the concrete
type, grounded in report 92 §6's field list and reusing the mainline's
digest discipline:

```rust
struct VersionedCheckpoint {
  store_name: VersionedStoreName,
  store_schema_hash: SchemaHash,                 // store generation this checkpoint sits under
  family_inventory: Vec<SchemaHash>,             // families present — the decode requirements to restore
  covered: SequenceRange,                        // first..=last commit_sequence folded into this checkpoint
  view_digest: EntryDigest,                      // FULL 32-byte blake3 of materialized state (the oracle)
  previous_checkpoint_digest: Option<EntryDigest>,
  checkpoint_digest: EntryDigest,                // hash over the above, domain-separated like the entry chain
  retained_suffix: RetainedSuffixPolicy,         // how much log after `covered.last` is retained
}
```

Storage: a sibling `__sema_engine_versioned_checkpoint` table (u64-keyed by
`covered.last()`), written in the same transaction as the entry that
triggers it. `view_digest` is exactly the spike's
`MaterializedView::state_digest()` fold — reuse it. Two roles: (a) bound
replay cost to O(log since last checkpoint); (b) answer a **pruned-head**
sync — when a peer asks from a sequence below the retained suffix, serve the
nearest covering checkpoint plus the suffix after it, never a gap (report 92
§3 lesson 3: naive suffix sync breaks the moment you compact). The
checkpoint must exist before compaction or the append-frame backend, both of
which depend on it.

### 3. The remote append protocol (audit next-slice 3 / §7 — the unmet original intent)

This is the part closest to `29pb` ("atomic, server-backed durability")
and neither the spike nor the mainline builds it. The minimal idempotent
contract, as a `signal-*`-shaped wire (a versioned-log mirror contract):

- **Request**: ship one (or a run of) `VersionedCommitLogEntry`. The entry
  already carries everything needed — `store_name`, `commit_sequence`,
  `previous_entry_digest`, `entry_digest`, `operations`.
- **Server (ingest) holds**, per `store_name`, the current head
  `(commit_sequence, entry_digest)`.
- **Validate expected-head**: `request.previous_entry_digest ==
  server_head_digest`. On match, append; on a gap or fork, reject and let
  the client back-fill or quarantine (do not silently accept out of order).
- **Idempotent duplicate**: if `entry_digest` is already present (same
  store + sequence, same digest), ack the existing head — re-sends are safe
  (the at-least-once spool gives duplicates; the digest makes them
  harmless).
- **Append, fsync, ack** the new `(commit_sequence, entry_digest)` =
  **server-committed**.
- **Durability levels** become a per-store policy on `VersioningPolicy`:
  *local-committed* (engine txn done) → *queued-for-mirror* (in a durable
  local outbox table, server hasn't acked) → *server-committed* (ack
  received). A store whose loss is unacceptable (spirit-class) takes
  sync-server-committed with backpressure; a cache store takes async with a
  **named RPO**. The host is **ouranos** (Gitolite + Tailnet, the
  control/ingest node) — **not** prometheus (the Btrfs storage target).

The auditor's caution is right: build this small endpoint before polishing
the append-frame file. A restore witness (audit next-slice 4) closes it —
write local state, mirror entries, rebuild a fresh store from the log,
assert the **normal query surface** reads the same records (not just a
digest match). The spike's rebuild oracle is the in-memory half of that
witness; the real witness rebuilds through the engine's query surface.

### 4. Reducer artifact identity (audit §4 — deferred, design stance recorded)

The audit rightly flags that `SchemaTransition(from, to)` with a dynamic
`Vec<Box<dyn Reducer>>` is a *replay-time promise*, not a *durable
guarantee*. The design answer is already in report 92 §6 and stands:
**migrations always emit a post-migration checkpoint**, which makes old log
entries and old reducers **cold provenance** rather than a hot replay
dependency — restoring current state starts from the most recent checkpoint
and never needs to resurrect a months-old reducer closure. So the durable
guarantee is the checkpoint (item 2 above), and the transition entry carries
reducer **provenance** — `from`/`to` schema-hash plus a reducer artifact
hash / component build identity (plausibly a Nix closure id) for full-history
audit, not for hot-path correctness. This is deferred per the audit; the
stance is: do not make replay depend on reducer executability — make it
depend on checkpoints.

## What stays the owners' / deferred (unchanged)

The kernel inversion (redb tables as purely rebuildable views), spirit
live/archive/guardian consolidation, append-frame backend selection,
digest-function finalization beyond blake3, and reducer-storage vs
post-migration-checkpoint-storage all remain deferred — agreeing with the
audit's defer list. The spike is not merged; its role was to prove the
closed-sum genericity and the rkyv-avoidance, both confirmed by the
auditor's own run of the six tests. The concept worktree stays for
reference until this design lands on main, then it is cleaned up.

## Agreement summary

| Audit item | Designer response |
|---|---|
| Report 92 as the constraint map | Agree — keep |
| `sema-engine` home layer | Agree (it was report 92's call) |
| Same-file mainline as production first stage | Agree — it is ahead of the spike on same-txn atomicity |
| Closed-sum schema-hash decoding as next identity target | Agree — designed in §1 above |
| Don't merge `src/versioned/` wholesale | Agree — never proposed |
| Spike tests ≠ backup/remote proof | Agree — corrected the report-93 overclaim |
| Don't replace cursors with digests | Agree — 92 and the spike both keep cursors |
| No open decoder registry / fallback | Agree — the selector stays closed (§1) |
| Checkpoint object is the largest gap | Agree — named in §2 |
| Remote append is the biggest unmet promise | Agree — contract in §3 |
| Next-slice ordering (identity → checkpoint → remote → restore → append-frame) | Endorse |
