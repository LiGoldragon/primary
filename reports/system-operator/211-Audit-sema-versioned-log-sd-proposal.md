# SEMA Versioned Log SD Proposal Critique

Variant: Audit.
Role: system-operator.
Scope reviewed:

- `reports/system-designer/92-reusable-versioned-sema-library/`
- `reports/system-designer/93-reusable-versioned-log-spike-implementation.md`
- `~/wt/github.com/LiGoldragon/sema-engine/reusable-versioned-log-spike`
- Current `sema-engine` main after `c970d3f2`.
- Current `mind` main after `7e29a4f4`.

## Verdict

SD's report 92 is strong as a constraint map. It correctly relocates the reusable
work from the `sema` kernel to `sema-engine`, identifies the central
genericity problem, preserves monotonic cursors beside digests, and treats
checkpoint/remote/RPO as first-class rather than optional cleanup. I would keep
it as the design-context report for this arc.

The spike in report 93 is useful executable evidence, but not an integration
candidate. It proves that the sealed-family plus closed-component-enum shape can
avoid the rkyv generic-bound trap, and it gives a runnable append-frame arm. It
does not prove production server-backed durability, real Engine integration,
checkpoint/compaction, crash recovery, or real component coverage. Treat it as a
reference branch to mine, not a module to merge.

The operator-landed mainline implementation is the right conservative first
stage: same `.sema` file, one write transaction, opt-in `VersioningPolicy`, and
Mind using it with minimal component code. SD's proposal now mainly tells us
what the next layers must add: per-family schema identity and generated closed
decoders, checkpoint records, remote append/ack policy, and reducer artifact
identity.

## What SD Got Right

The biggest correction is the home layer. Report 92 says the reusable seed is
`sema-engine`, not the low-level `sema` kernel, because commit sequence,
snapshot identity, registered families, log entries, replay, and subscriptions
already live in the engine. That matches the current repo architecture:
`EngineOpen::with_versioning(VersioningPolicy)` now enables the same-file
payload log, and the versioned entry is written in the same transaction as the
domain mutation and metadata commit log.

The genericity analysis is the best part of the design. Report 92 names the
actual knife-edge: a closed enum keyed by schema hash can stay typed, while an
open `HashMap<SchemaHash, Box<dyn Decoder>>` with fallback becomes the forbidden
generic-record store. The spike backs this up: `ComponentRecord::decode` is a
closed match in the demo, unknown hashes are rejected, and `cargo test --lib
versioned::spike_demo` passes the six claimed tests.

The report also keeps the operational caveats in frame. Same-file redb logging
has free atomicity and read-after-write strength; append-frame logging has
better byte shipping but loses cross-file atomicity and needs a view watermark.
Remote durability is separated into local committed, queued-for-mirror, and
server committed. That is the right language for the eventual server.

## Main Critiques

### 1. The spike proves a side module, not the engine path

The spike adds `src/versioned/` and wires `pub mod versioned` in `src/lib.rs`,
but it deliberately does not touch `Engine`, `CommitLogEntry`, registered table
execution, subscriptions, or component opt-in. Report 93 is honest about this:
no kernel inversion, no real engine rewiring, same-file stores only the log
table, and the view is in memory.

That means its strongest result is narrow: the closed-sum genericity mechanism
is tractable. It does not prove the production path that components will call.
The current mainline `Engine` implementation is the production reference for
now.

### 2. The same-file arm does not demonstrate same-transaction log plus view

`SameFileLog::append` writes only `__versioned_log`; the `MaterializedView` fold
is in memory. So the spike demonstrates redb can atomically persist a log entry,
but not the harder Option A invariant: domain table mutation, metadata log,
payload log, counters, and local view state all update in one transaction.

The mainline implementation does demonstrate the more relevant invariant:
`VERSIONED_COMMIT_LOG` is inserted in the same storage write transaction as the
domain record and `COMMIT_LOG`. That should remain the baseline until the
append-frame arm has crash and watermark witnesses.

### 3. The "both backends rebuild to the same digest" test is weaker than it sounds

The test is valuable, but it only says two clean logs with identical synthetic
inputs fold to the same in-memory digest. It does not exercise duplicate send,
expected-head validation, partial suffix sync, pruned-head recovery, checkpoint
restore, or crash injection at the fsync boundary.

That is acceptable for a spike, but the handoff should not phrase it as proof
that same-file versus separate-file is "decidable" yet. It is only the first
semantic equivalence witness.

### 4. Reducer dispatch is dynamic and underspecified

The report rightly warns that `Box<dyn>` is dangerous when it becomes the
decoder registry. The spike avoids `Box<dyn Decoder>`, but it still uses
`ReducerSet { reducers: Vec<Box<dyn Reducer>> }`. That may be fine for a
runtime migration catalogue, but production needs a stronger story:

- reducer artifact identity in the log or checkpoint;
- old and new decoder availability;
- Nix/component build identity for replay months later;
- behavior when a reducer exists in source today but not in the replay
  environment.

Without this, `SchemaTransition(from, to)` is a replay-time promise, not a
durable replay guarantee.

### 5. The proposal still lacks a concrete checkpoint object

Report 92 correctly says checkpoint/compaction is the danger zone. The spike
includes an `OperationKind::Checkpoint` variant, but the implementation treats
it as a no-op and defines no checkpoint payload. This is the largest remaining
design gap before remote backup can be called real.

The next design should name the checkpoint type before another backend choice:
store identity, covered sequence range, schema-hash inventory, view digest,
previous checkpoint digest, retained suffix policy, and pruned-head response.

### 6. Real consumers are still under-covered

SD already flags that `mind` and `criome` were under-grounded. That gap matters
more after the operator pass because Mind now opts into the mainline versioned
log with only `EngineOpen::with_versioning`, but not with the spike's
per-family generated closed enum. This reveals the next integration pressure:
the current mainline log has a store-level schema hash and still records table
names as strings, while SD's proposed decoder selector wants per-family schema
identity.

So the critique is not "SD is wrong"; it is that the current accepted
implementation is a conservative subset of SD's desired identity model. The
next sema-engine step should reconcile those: a versioned entry needs enough
typed family identity to replay without depending on table-name strings.

### 7. The remote/server piece remains the biggest unimplemented promise

The original intent was server-backed atomic durability. Neither SD's spike nor
the operator implementation builds the mirror server. Report 92 maps the policy
well, but the actual system still has only local authoritative history.

The next owner should not spend the next slice polishing the append-frame file
before there is at least a small idempotent remote append protocol:
store name, commit sequence, previous digest, entry digest, duplicate-entry
idempotence, server fsync ack, and queued-for-mirror state.

## Accept / Reject / Defer

Accept:

- Report 92 as the best current constraint map.
- `sema-engine` as the home layer for the first reusable substrate.
- Same-file log as the production first stage.
- Closed-sum schema-hash decoding as the next identity target.
- Append-frame as a later measured backend, not a replacement for the current
  same-file implementation.

Reject:

- Merging `src/versioned/` wholesale into main.
- Treating the six spike tests as backup or remote-durability proof.
- Replacing monotonic cursors with digests.
- Any open generic decoder registry or fallback "generic record" payload.
- Any separate-file production path without a durable view-applied watermark
  and crash harness.

Defer:

- Kernel inversion where redb tables are purely rebuildable views.
- Spirit live/archive/guardian consolidation.
- Append-frame backend selection.
- Digest-function finalization beyond blake3 as the current practical choice.
- Reducer artifact storage versus post-migration checkpoint storage.

## Recommended Next Slice

1. Extend mainline `VersionedCommitLogEntry` toward per-family identity:
   record-family schema hash, table/family descriptor, and generated decoder
   shape. Avoid a stringly `RecordKind` selector.
2. Define and test a `Checkpoint` record on the same-file log before compaction
   or append-frame work.
3. Build a tiny remote append server or component endpoint with expected-head
   validation and idempotent duplicate handling.
4. Add a restore witness: write local state, export or mirror log entries,
   rebuild a fresh store, and assert the normal query surface reads the same
   records.
5. Only after those pass, reopen the append-frame backend with crash injection
   and a durable view watermark.

## Verification

Ran on the SD spike branch:

```text
cargo test --lib versioned::spike_demo
```

Result: six spike tests passed. I did not run the full Nix suite for this audit.

