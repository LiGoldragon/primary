# 7 — The actual design: version the log, not the store

The synthesis (file 6) recommended "a payload-bearing Datomic-style log under a blake3-chunk snapshot layer with prolly-tree structural sharing, shipped via the repository-ledger pattern." That names four patterns and defers the only hard question to Stage 3: **what is the unit of content-addressing for a strict-typed rkyv+redb store, and how does a version survive a type-changing migration?** This file commits to an answer and, in doing so, throws out two things the report over-imported by analogy to beads/Dolt.

## Decision: the operation log is the source of truth; the redb store is a rebuildable materialized view

Today the inversion runs the other way: the `sema` kernel treats the redb file as ground truth and the `__sema_engine_commit_log` as side metadata that records only `(operation, table_name, key)` — no payload, not replayable into state. The design decision is to **flip that**:

1. **The log carries the payload.** `CommitLogOperation` gains the rkyv record bytes (the asserted/mutated value) plus the **schema-hash** under which those bytes were produced. The log entry is now self-sufficient to reconstruct state.
2. **The log is hash-linked.** `CommitLogEntry` gains `prev_entry_digest` (blake3 of the prior entry). The log becomes a Merkle hash-chain; its **head digest is the content-addressed database version** — added *beside* today's monotonic `CommitSequence`/`SnapshotIdentifier` markers, **not** replacing them (corrected per audit 208: the digest is an identity/integrity anchor — not sortable, no `next()`, no range queries — so the sequence stays the ordered cursor for replay/range/subscription).
3. **The redb tables become a cache/index** materialized by folding the log. Lose them and you rebuild from the log; daemon resume = fold from the last checkpoint forward. The redb store stops being truth and becomes a fast read view over the authoritative log.

Backup and sync then fall out for free: **ship the log suffix since the peer's last head digest.** Append-only + content-addressed means transfer is incremental, idempotent, and atomic by construction — no diffing, no merge engine, no double-addressing.

## Why this resolves the type-migration tension

The report's sharp point was: each schema version is a different rkyv type set, so a cross-version byte diff is meaningless. Versioning the *log* sidesteps it entirely. A migration is **a first-class log entry** — `SchemaTransition(v_old_hash → v_new_hash, reducer_id)` — not a byte diff. Replaying the log applies the reducer (the existing `historical → current` From-chain) at that point; every entry *before* it decodes under `v_old`'s frozen types (spirit's `SpiritStoreV1..V6` historical readers already are exactly these), every entry *after* under `v_new`. The schema identity travels *inside the log*, which is what "schema identity must live in the commit, not as ambient global state" actually requires. Time-travel to a pre-migration state reads its entries under their own type set; there is never a moment where new code must byte-interpret old-typed bytes.

## Why prolly trees — and git — were the wrong imports

Both came from reasoning "beads version-controls a database with Dolt, so be like Dolt." The analogy doesn't hold:

- **Prolly trees solve a problem we don't have.** Dolt prolly-trees a *large, mutable keyspace* so that random cell edits diff and merge cheaply against arbitrary other versions. Our durable stores are append-only typed *events* (intent records, repo-ledger observations, attestations) — **Datomic-shaped, not Dolt-shaped.** An append-only log doesn't need a tree to diff; "ship the entries after digest X" is strictly simpler and cheaper than walking two Merkle B-trees. Prolly trees would be machinery bolted on to imitate a database whose write pattern we don't share.
- **Git was double content-addressing** (already covered in file 6): our chunks are blake3-addressed, so tunnelling them through git's object store addresses twice. Git stays a Stage-1 *floor* transport only because the auth already exists — never the native substrate.

So the honest core is narrower and sharper than the synthesis: **an event-sourced, hash-linked typed log; the redb store as its materialized view; backup = ship the log.** No prolly tree, no git in the critical path.

## Concrete shape on `sema-engine` (what actually changes)

| Surface | Today | Change |
|---|---|---|
| `CommitLogOperation` | `{operation, table_name, key}` (`log.rs:63-68`) | add `payload: rkyv bytes`, `schema_hash` |
| `CommitLogEntry` | `{commit_sequence, snapshot, NonEmpty<op>}` (`log.rs:15-19`) | add `prev_entry_digest: blake3`; head digest = DB version |
| Version identity | `SnapshotIdentifier(u64)` counter (`snapshot.rs:19`) | **add** `HeadDigest` (blake3, criome's `ObjectDigest` precedent, `signal-criome/src/lib.rs:55-57`) as content identity *beside* the monotonic markers — keep `CommitSequence` as the cursor (audit 208) |
| redb tables | source of truth | materialized view; rebuildable by folding the log |
| Migration | full rewrite + `fs::rename` aside (`production_migration.rs`) | a `SchemaTransition` log entry + the reducer; old entries retained under `v_old` |
| Resume | reopen redb, rebuild catalog | fold log from last checkpoint |
| Backup/sync | none | ship log suffix since peer head digest, over the tailnet ingest daemon |

**Checkpoint + compaction** keeps the log bounded: periodically write a content-addressed full-state object and archive the log prefix behind it (TerminusDB's delta-rollup / Dolt's journal→oldgen, the one structural lesson worth keeping). Replay cost is then O(log since last checkpoint), not O(all history).

## Should the log be its own file?

Today it isn't: `__sema_engine_commit_log` is a redb table inside the same `*.sema` file, written in the same redb transaction as the data. That co-location buys **free atomicity** — single-writer ACID over the whole file means the log entry and the materialized view commit together and can never diverge. While the log is a throwaway audit note (status quo), same-file is correct and simplest.

**Under the flip, the log should be its own append-structured artifact, separate from the redb view.** Three reasons:

1. **Opposite lifecycles** — the log is precious and append-only; the view is disposable and random-access. You want to rebuild the view from the log without touching the truth. Co-located, "rebuild the cache" means "rewrite the authoritative file."
2. **The log is the backup unit** — the whole goal is "ship the log suffix." A separate log file *is* the shippable artifact (append its new bytes); buried in the redb file, backup degrades to shipping the whole file (the blob problem) or extracting+re-encoding entries.
3. **Right structure** — an append-only hash chain wants append-optimized storage (a segmented frame log, à la Dolt's journal); a view wants a B-tree. A u64-keyed redb table is a B-tree pretending to be a log.

**The cost is losing free cross-file atomicity** (redb can't transact across two files), paid with the standard **write-ahead-log** pattern: the fsync'd append to the log is the commit point; the redb view is a *follower* holding a watermark ("applied up to entry N") and catching up; on restart it replays log entries past its watermark. The view can lag and self-heal but never gets ahead of the log — the same discipline Postgres, SQLite-WAL, and event-sourced systems use.

**Staging hedge:** the split can be deferred — keep both in one redb file first (consistency free) and break the log into its own append store when backup or write throughput forces it. Because *backup is the driving requirement here*, separating sooner is justified rather than later. Sub-choice when splitting: a second redb file (low effort, reuse rkyv/redb machinery, gains independent shippability + disposable view) versus a bespoke append-frame log (higher effort, byte-shippable, no B-tree churn — the right end state).

## What this costs — the open risks to pressure-test before committing

This is a real architectural inversion, not a free win. Before it's adopted it needs the `sema`/`sema-engine` owners to weigh:

1. **Write amplification.** Every mutate now appends the payload to the log. Fine for intent/ledger/attestation volumes; for a high-write cache-shaped store it needs aggressive checkpointing or that store opts out of event-sourcing.
2. **The kernel inversion is the big call.** `sema`'s INTENT today is "redb is the typed store." Making the log authoritative and redb a view is a genuine change to the kernel's contract — exactly the kind of thing that must not be decided by a designer alone. It is `sema`/`sema-engine` territory.
3. **Not every component may want it.** spirit clearly does (it already hand-rolls history, archiving, supersession on top of a current-state store — this absorbs that). repository-ledger already is event-shaped. A purely derived/cache store might not. So this is plausibly a *capability of `sema-engine` that a component turns on*, not a universal kernel mandate.
4. **Does this duplicate or subsume spirit's existing `state_digest` and archive DB?** spirit already computes a blake3 `state_digest` (`store.rs:714-758`) and copies retired records into a separate `*.archive.sema`. If the log is authoritative those become redundant — confirm this *replaces* them rather than sitting beside them.

## Bottom line

The substantial design is one decision with consequences, not a pattern list: **make `sema-engine`'s commit log payload-bearing, hash-linked, and authoritative; demote the redb store to a materialized view; represent migration as a typed log entry; back up by shipping the log.** It resolves the type-migration tension the report raised, it's a concrete diff against the real `sema-engine` types, and it explicitly rejects the prolly-tree and git imports that were cargo-culted from beads. It supersedes the Stage-3 "native content-addressed remote" hand-wave in file 6. The risk it carries — inverting which layer is the source of truth — is the part that genuinely needs the kernel owners, not a designer's say-so.

## Revised after system-operator audit (208)

`reports/system-operator/208-Audit-sema-design-log-source-of-truth-feedback.md` reviewed this design. Verdict: accept the central inversion and the rejection of prolly-tree/git imports; the remaining gaps are operational, not philosophical. This section integrates the audit and is **authoritative where it differs from the sections above.** Three places it corrected my judgment specifically:

- **Digests sit *beside* the monotonic markers, not replacing them.** A blake3 digest is an identity/integrity anchor — not sortable, no `next()`, no range queries. `CommitSequence` stays the ordered cursor (replay, range, subscription, handover high-water mark); `HeadDigest`/`EntryDigest` is *added* as content identity; `DatabaseMarker` becomes sequence (+ snapshot) + head digest. (Fixed inline above.)
- **Split the log into its own file *last*, not first.** I argued "separate sooner because backup is the driving requirement." Shippability does **not** require physical separation: a mirror reads entries through `replay_from_sequence` / an entry-stream API and uploads them — that *is* the shippable unit, immediately. Physical separation into an append-frame file is the final stage, justified by append-throughput and a pure-follower view, *after* the entry envelope, digest, and checkpoint formats are proven. I conflated the logical shippable unit (now) with the physical file split (later). This corrects the "separate sooner" recommendation in the "Should the log be its own file?" section above.
- **The *local* view must not lag.** My "view is a follower that may lag" applies only to the *remote mirror*. Locally, a commit returns after the log is durable **and** the local view has applied the entry (one transaction — read-after-write preserved); crash recovery replays past the view's watermark to self-heal, but a successful local write is always immediately readable. "May lag" is the remote-mirror property, not the local-engine property.

New design elements the audit specified — now core, not later cleanup:

**Typed replay envelope.** `payload: rkyv bytes` alone is insufficient: engine writes are generic over registered record types, `CommitLogOperation` is not. Each entry needs — operation kind (assert | mutate | retract | schema-transition | checkpoint); table name / stable table id; record key / engine identifier; **schema-hash / record-family-hash** (the decoder selector); payload bytes (assert/mutate); tombstone (retract); optional prior digest / prior value (only if reverse time-travel/audit is required); entry digest over a canonical byte form; previous entry digest + sequence. Forward state reconstruction needs only new values + tombstones; reverse/audit needs old values *or* replay-from-an-earlier-checkpoint.

**Remote durability levels — the actual server-backup contract.** "Ship the log suffix" is underspecified until the acknowledgement policy is explicit. Three levels: *local-committed* (fsync'd locally, view applied), *queued-for-mirror* (in a durable local outbox, server hasn't accepted), *server-committed* (remote validated prior head, appended, fsync'd, acked the new head). This is **per-store policy**, not a global mode: spirit-class state where loss is unacceptable may demand sync server-committed-before-success — and then the write path owns network backpressure, retry, timeout, degraded-mode; a high-write cache may accept async with a **named, nonzero RPO**. Naming the RPO honestly is the difference between "server-backed" and "eventually maybe server-backed." (Ties to the opt-in model: the durability level is part of a component's Sema config.) This was the gap closest to the original question — my proposal had drifted into local event-sourcing and under-specified the *server* contract.

**Reducer artifact durability + migration-always-checkpoints.** `SchemaTransition(v_old_hash → v_new_hash, reducer_id)` is not replayable if `reducer_id` names an artifact that no longer exists. A transition entry needs: old + new schema hash; reducer artifact hash / component build identity (for system deployment, plausibly a Nix closure identity); reducer input→output record-family mapping; whether it stores only the event or also the post-migration checkpoint. **My refinement on top of the audit:** make a migration *always* emit a checkpoint of post-migration state. Then old log entries + old decoders/reducers become *cold provenance*, never a hot replay dependency — restoring current state never needs to resurrect a 10-month-old executable closure, because it starts from the most recent post-migration checkpoint. Retaining the closure (the Nix way) becomes a nice-to-have for full-history audit, not a correctness requirement. "spirit has historical readers" is evidence, not a general guarantee — the checkpoint-at-migration rule is what makes it general.

**Checkpoint protocol (first-class, because compaction breaks the naive suffix sync).** Once prefixes are archived, "send entries after digest X" fails if X is pruned. A checkpoint object needs: checkpoint identity; included schema-hashes + table-family inventory; first and last covered sequence; checkpoint digest + previous checkpoint digest; retained-suffix policy; and defined behavior when a peer requests from a pruned head (serve the nearest covering checkpoint + the suffix after it).

**Adopted staging (supersedes the staging in the sections above):**
1. **Conservative** — keep the current single redb file + single transaction; make the commit log payload-bearing and hash-linked; add the typed envelope + digests; **keep `CommitSequence` and `SnapshotIdentifier`**; add tests that delete and rebuild the materialized tables from the log in a temp database.
2. **Server mirror** over the replayable entry stream — server validates sequence continuity + previous-head digest, writes idempotently, returns the accepted head; **choose the acknowledgement policy** (async / sync / per-store).
3. **Checkpoints** with schema-hash inventory; replay tests across at least one real migration; reducer artifact identity becomes concrete.
4. **Split** the authoritative log into an append-frame artifact *only after* stages 1-3 prove the entry format and backup protocol; the redb view becomes a pure follower with a durable applied watermark.

Net of the revision: the inversion stands, and the audit moves it from a direction toward an implementation spec by nailing the envelope, the ack/RPO contract, reducer durability, read-after-write, and the checkpoint/sync interaction. The kernel-inversion risk — whose call this is — is unchanged: still `sema`/`sema-engine` owners'.
