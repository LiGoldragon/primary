---
title: 214 - SEMA versioned-state grand design operator position
role: system-operator
variant: Refresh
date: 2026-06-12
topics: [sema, versioned-state, backup, dvcs]
description: |
  Agglomerated system-operator position after reading system-designer report
  95/8. Supersedes the recent system-operator SEMA versioned-state research,
  implementation notes, and audits by carrying forward their live constraints
  into one operator-facing report.
---

# 214 - SEMA versioned-state grand design operator position

## Intent Anchors

[Component SEMA database version-control and server-backed durability must be a reusable substrate, built once with generic types and traits, with every component able to opt in rather than reimplement the mechanism.]

[The reusable component version-control system is foundational to the meta-work and must support full database DVCS semantics: branching, forking, rebasing, and merging over typed component state, with default policy plus per-component override.]

[The version-control and backup system should use one consistent cryptographic basis: blake3 for content addressing and criome BLS for signing and attesting history.]

[Design at the post-agent capability frontier: target the best end-shape rather than old compromises, while still proving correctness with witnesses.]

[The `IntakePolicy` is a universal reusable admission interface with per-component implementations; it is not only a rebase hook.]

## Sources Absorbed

This refresh absorbs the live substance from these system-operator reports:

- `reports/system-operator/208-Audit-sema-design-log-source-of-truth-feedback.md`
- `reports/system-operator/209-Research-sema-versioned-state-prior-art-and-constraints.md`
- `reports/system-operator/210-sema-versioned-state-engine-and-mind-implementation-2026-06-11.md`
- `reports/system-operator/211-Audit-sema-versioned-log-sd-proposal.md`
- `reports/system-operator/212-Audit-sema-versioned-log-sd-response-94.md`
- `reports/system-operator/213-Audit-sd-versioned-state-grand-design-exchange.md`

It also reads the current designer synthesis:

- `reports/system-designer/95-versioned-state-grand-design/8-visual-design.md`

Retirement note: this report supersedes the conclusions of 208-213 as the
current operator surface. I am not deleting the old files in this commit because
live system-designer reports still cite several of their paths directly,
especially 208 and 211. A later cross-lane maintenance pass can update those
references and retire the old files cleanly.

## Current Verdict

System-designer report 95/8 is the strongest design surface in this arc so far.
It turns the earlier "payload log for backup" work into a coherent typed
database-DVCS design: version the log, make redb a materialized view, represent
branches as named frontiers over a commit DAG, replay suffixes through
component policy, use blake3 for content identity, and sign checkpoints/heads
with criome BLS.

The operator position is: accept report 95 as the target architecture direction,
but do not treat it as an implementation spec yet. The implementation path still
has to pass through the same hard gates identified in the earlier audits:
per-family identity, checkpoint payload, restore/import API, mirror outbox,
idempotent remote append, policy identity, and crash/read-after-write witnesses.

The core design is now clear enough that the next operator slice should stop
debating "log versus store" and start hardening the nouns.

## What Report 95 Fixed

Report 95 resolves several earlier operator cautions.

It no longer treats `IntakePolicy` as a rebase-only hook. It shows the same
admission gate on local writes, rebase, merge intake, and remote ingest. That
matches the psyche clarification and is the right reusable abstraction.

It separates `IntakePolicy` from `ConflictPolicy`. Admission answers whether an
entry may enter a branch. Conflict policy answers how concurrent writes to the
same structural key resolve. That distinction prevents the reusable core from
becoming a vague "policy" object that hides two different correctness jobs.

It narrows the structural-tree story. Prolly trees or MST-like structures are
not needed for the log, because the suffix is the diff. Structure is considered
only for distant checkpoint-state comparison and remote inclusion/consistency
proofs. This is the correct correction to the earlier Dolt-shaped temptation.

It signs heads/checkpoints rather than every hot-path entry. That keeps the
write path plausible: blake3 hash-chain locally, RFC-6962-style Merkle history
tree for remote proofs, and BLS signed notes over roots/checkpoints.

It explicitly marks new BLS quorum machinery as "to build" rather than claiming
criome already has it. That honesty matters; criome has the authorization
vocabulary, not the whole aggregation/proof-of-possession implementation.

It corrects the overstatement that disjoint-key merges are "free." They are
free of structural conflict resolution, not free of admission. A semantic
guardian can still reject or transform a disjoint-key entry because it violates
cross-record meaning.

## Operator Baseline Already Landed

The live code is not report 95 yet. The live production seed is the conservative
same-file engine work:

- `sema-engine` commit `c970d3f2` adds an opt-in versioned payload log.
- `mind` commit `7e29a4f4` opts one real component store into that log.
- The new log lives in the same `.sema` file as the component tables.
- The domain mutation, existing metadata commit log, and versioned payload log
  are written in one redb transaction.
- The engine still has a single linear commit stream, not branch frontiers or a
  commit DAG.
- There is no remote server, no checkpoint payload format, no restore/import
  API, no policy-mediated branch/rebase path, and no signed checkpoint system.

That stage remains valuable. It proves the opt-in surface can be small and that
the reusable home is `sema-engine`, not component-local journals. Report 95
should grow from this baseline, not bypass it.

## Non-Negotiable Constraints

Monotonic cursors stay beside digests. `CommitSequence` remains the ordered
cursor for range, replay, subscription, handoff, and restore. `EntryDigest` and
`HeadDigest` identify and verify content. A digest is not sortable and does not
replace ordered cursors.

The first production backend stays same-file until its witnesses are green.
Same-file redb buys atomicity: view mutation, metadata log, payload log, outbox
state, and counters can land in one local transaction. A separate append-frame
backend is worth measuring later, after crash and view-watermark tests exist.

Checkpoints must include or reference snapshot payload. A checkpoint digest,
schema inventory, and covered range can verify a reconstructed state, but cannot
restore one. The design needs `CheckpointSegment` or equivalent payload records
containing sorted family/key/payload data, content-addressed by blake3.

Server-committed durability cannot live inside the redb transaction.
`sema-engine` should write local state plus a durable mirror outbox row. A
component-owned or reusable mirror actor ships the outbox and records server
acknowledgement. If a request wants "server committed" before replying, that
wait happens after the local transaction closes and must return a typed outcome
if the mirror fails.

Family identity must be stable and semantic. A table name is a storage
coordinate. Durable replay needs a generated `FamilyIdentity` with a stable
family identifier, current table coordinate, and schema hash. Table renames,
splits, and merges cannot be mistaken for semantic family identity.

Store schema identity should be derived. A manual label like `mind-schema-v7`
is a bootstrap crutch. The durable store schema hash should be generated from a
sorted inventory of family identities plus component schema identity.

Restore needs an engine import path. Rebuilding a store cannot be ordinary
component `assert` calls if the restored store must preserve original commit
sequences, head digests, metadata logs, checkpoint rows, tombstones, and mirror
head state. The import path should be engine-owned and unavailable to ordinary
mutation handlers.

Policy decisions must be durable. If an intake policy rejects or transforms an
entry, the log needs the original lineage, target base, verdict, reason,
transformed payload if any, policy identity, and schema identity. Otherwise a
future audit cannot explain why a rebase differs from the original suffix.

Policy must be deterministic with respect to the rebuilt base. Report 95's
"pure function of base state and entry, never live head" invariant is correct.
For Spirit, an LLM guardian can still be involved, but the resulting verdict is
the durable fact. Replaying later should replay the recorded verdict or prove
the same policy identity produced it; it should not silently ask a newer
guardian to reinterpret old history.

Remote ingest has two modes. A dumb backup mirror validates hash continuity,
expected head, signatures, and idempotence; it does not run Spirit's guardian.
A semantic peer importing entries into a component branch must run
`IntakePolicy`. The server role must be explicit so "remote ingest" does not
become an accidental bypass or accidental guardian.

Privacy and retention policy are part of the remote contract. Report 95 says
ouranos is append-only and never GCs. That is a defensible backup stance for
some stores, but Spirit-class or private stores still need explicit authority,
privacy class, retention, pruning, and deletion semantics. "Never GC" cannot be
an unexamined default for every component.

## Refined Architecture Shape

The target architecture has four layers:

1. Component daemon: owns semantic families and policy. It implements
   `IntakePolicy`, `ConflictPolicy`, reducer/migration policy, and
   attestation policy as needed.
2. `sema-engine`: owns reusable version-control mechanism: payload log, commit
   DAG, branch frontiers, checkpoint metadata and segments, materialized-view
   rebuild, mirror outbox, and restore/import.
3. `sema` kernel: owns redb/rkyv bytes, typed table access, transaction safety,
   and format guards.
4. Remote mirror/server: owns append-only durable copy, expected-head checks,
   idempotent duplicate handling, fsync acknowledgement, inclusion/consistency
   proofs, retention policy, and signed-head storage.

The split matters. The engine should not become a network daemon. The server
should not become a component guardian unless it is explicitly running as a
semantic peer. The kernel should not learn branch semantics.

## Implementation Order

The next operator path should be staged so each layer earns the next one.

Stage 1: typed family identity on the current same-file log.

- Replace table-name strings in versioned entries with durable family identity.
- Derive store schema hash from registered family inventory.
- Keep current redb transaction atomicity.
- Add tests proving table rename or manual schema-label drift cannot silently
  corrupt replay identity.

Stage 2: checkpoint payload and restore/import witness.

- Define `CheckpointMetadata` and `CheckpointSegment`.
- Cover a `CommitSequenceRange`, not the existing snapshot-oriented
  `SequenceRange`.
- Store sorted family/key/payload records or content-addressed segment refs.
- Add engine import that preserves original sequences, digests, tombstones, and
  checkpoint rows.
- Test fresh-store restore through the normal query surface.

Stage 3: mirror outbox and idempotent remote append.

- Add local mirror-outbox rows in the same engine transaction as the write.
- Build the smallest append server or mirror component with expected-head
  validation, duplicate entry idempotence, fsync-before-ack, and privacy/store
  authorization.
- Keep server-committed waiting at the component request layer.

Stage 4: branch frontier and commit DAG.

- Add `BranchRef` as a compare-and-swap cursor from branch name to head digest.
- Promote the hash chain to a DAG with two-parent merge entries.
- Keep single-main operation as the default path for components that only need
  backup/version history.

Stage 5: universal policy replay.

- Introduce `IntakePolicy` with enough context: base state, entry, source path
  (local, rebase, merge, remote semantic import), author/provenance, branch, and
  original lineage.
- Introduce `ConflictPolicy` only for structural same-key overlaps.
- Record `Rejected`, `Conflict`, and `Divergence` entries as typed history.
- Test that direct table import, remote semantic import, rebase, and local write
  cannot bypass admission.

Stage 6: signed proofs.

- Add RFC-6962-style Merkle history tree over entry digests for remote proofs.
- Add BLS signed checkpoint/head notes using criome's existing authorization
  vocabulary.
- Implement proof-of-possession and aggregate verification deliberately; do not
  pretend the current criome vocabulary is enough.

Stage 7: migration as branch.

- Add `SchemaTransition` with reducer identity and dual-decode window.
- Rebuild new schema on a side branch, verify state digest, emit a
  post-migration checkpoint segment, sign the new head, and atomically advance
  the live branch.
- Decide whether old reducers remain executable by build/Nix identity or become
  provenance because post-migration checkpoint payload is sufficient.

## What Not To Do

Do not merge the SD spike module wholesale. Its value was proving the closed-sum
genericity shape and append-frame experiment, not replacing the integrated
engine path.

Do not build append-frame first. It is attractive for byte shipping, but without
checkpoint restore, outbox, and view watermark witnesses it adds crash surface
before the semantic format is ready.

Do not implement an open generic decoder registry. The safe shape remains a
generated closed enum keyed by schema/family hash. Unknown hashes fail closed.

Do not let "post-agent frontier" excuse missing invariants. Agents reduce
rewrite cost; they do not reduce the need for deterministic replay, crash
boundaries, restore witnesses, or durable policy verdicts.

Do not assume disjoint keys mean semantic independence. Structural conflicts
are same-key. Semantic conflicts can be cross-record and belong in
`IntakePolicy`.

Do not make remote "server committed" ambiguous. A caller must know whether a
write is local committed, queued for mirror, or acknowledged after server fsync.

## Current Open Decisions

The default `ConflictPolicy` is still open. Last-writer-by-sequence is simple
for caches and low-value stores. Hard-fail-as-typed-conflict is safer for
Spirit-class state. This probably needs a per-family default rather than one
global rule.

The remote retention rule is open. "Never GC on ouranos" is the strongest
backup story, but private or high-churn stores may need classed retention and
cryptographic erasure semantics. The design needs an explicit policy matrix.

The branch/policy layer's crate boundary is open. It can land inside
`sema-engine` if the engine owns all version-control nouns, or in a neighboring
crate if policy, proofs, and remote sync grow too large. The first implementation
should avoid a premature split until the engine nouns settle.

Cross-schema merge is open. A post-migration checkpoint makes restore possible,
but branch merge across schema boundaries needs either dual decoders and
reducers or a rule that branches must migrate to the same schema before merge.

Criss-cross merge bases are open. Refusing multi-LCA merges loudly is probably
fine until a real component produces that topology. Implementing virtual merge
bases early may be unnecessary complexity.

The guardian decision cache is open. A git-rerere-like learned cache could make
repeated rebase/merge admission cheap, but it must not violate the pure
function-of-base invariant or hide policy drift.

## Operator Acceptance Tests

Before calling the design production-ready, I would want these witnesses:

- same transaction witness: domain row, metadata log, payload log, outbox row,
  and counters commit atomically;
- payload replay witness: deleting/rebuilding materialized tables from the log
  yields the same query results;
- checkpoint restore witness: restore from checkpoint segment plus suffix into a
  fresh store and verify normal query-surface equivalence;
- pruned ancestor witness: a peer asking from a pruned head receives the nearest
  covering checkpoint plus suffix, or a typed refusal;
- remote append witness: duplicate sends are idempotent, expected-head mismatch
  rejects or quarantines, server fsync happens before ack;
- admission bypass witness: local write, rebase, merge intake, and semantic
  remote import all call the same `IntakePolicy`;
- policy provenance witness: rejected/transformed entries can be audited later
  without rerunning today's guardian;
- branch CAS witness: concurrent branch-head advance with stale expected head
  fails cleanly;
- migration branch witness: reducer rebuild on a side branch produces a
  checkpoint/state digest matching the accepted new live head;
- crash witness: interruption at each write/outbox/mirror boundary recovers to a
  consistent state with an explicit durability level.

## Bottom Line

The current best design is no longer "add backup to SEMA." It is a reusable,
typed, content-addressed version-control layer for component state:
payload-bearing log as truth, redb as rebuildable view, branch heads as frontiers
over a commit DAG, universal admission through `IntakePolicy`, structural
conflict through `ConflictPolicy`, checkpoint payload for bounded restore, and
remote signed suffixes for backup and verification.

The next code should stay disciplined: strengthen the current same-file
`sema-engine` substrate first, then add checkpoint restore and remote append,
then branch/policy semantics. That sequence keeps report 95's grand design
reachable without losing the operational invariants that made the first
implementation safe.
