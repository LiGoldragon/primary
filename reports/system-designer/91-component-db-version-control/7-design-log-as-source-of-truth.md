# 7 — The actual design: version the log, not the store

The synthesis (file 6) recommended "a payload-bearing Datomic-style log under a blake3-chunk snapshot layer with prolly-tree structural sharing, shipped via the repository-ledger pattern." That names four patterns and defers the only hard question to Stage 3: **what is the unit of content-addressing for a strict-typed rkyv+redb store, and how does a version survive a type-changing migration?** This file commits to an answer and, in doing so, throws out two things the report over-imported by analogy to beads/Dolt.

## Decision: the operation log is the source of truth; the redb store is a rebuildable materialized view

Today the inversion runs the other way: the `sema` kernel treats the redb file as ground truth and the `__sema_engine_commit_log` as side metadata that records only `(operation, table_name, key)` — no payload, not replayable into state. The design decision is to **flip that**:

1. **The log carries the payload.** `CommitLogOperation` gains the rkyv record bytes (the asserted/mutated value) plus the **schema-hash** under which those bytes were produced. The log entry is now self-sufficient to reconstruct state.
2. **The log is hash-linked.** `CommitLogEntry` gains `prev_entry_digest` (blake3 of the prior entry). The log becomes a Merkle hash-chain; its **head digest is the database version** — a real content address, replacing today's monotonic `SnapshotIdentifier(u64)` counter as the store's identity.
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
| Snapshot identity | `SnapshotIdentifier(u64)` counter (`snapshot.rs:19`) | content address = head digest (criome's `ObjectDigest` precedent, `signal-criome/src/lib.rs:55-57`) |
| redb tables | source of truth | materialized view; rebuildable by folding the log |
| Migration | full rewrite + `fs::rename` aside (`production_migration.rs`) | a `SchemaTransition` log entry + the reducer; old entries retained under `v_old` |
| Resume | reopen redb, rebuild catalog | fold log from last checkpoint |
| Backup/sync | none | ship log suffix since peer head digest, over the tailnet ingest daemon |

**Checkpoint + compaction** keeps the log bounded: periodically write a content-addressed full-state object and archive the log prefix behind it (TerminusDB's delta-rollup / Dolt's journal→oldgen, the one structural lesson worth keeping). Replay cost is then O(log since last checkpoint), not O(all history).

## What this costs — the open risks to pressure-test before committing

This is a real architectural inversion, not a free win. Before it's adopted it needs the `sema`/`sema-engine` owners to weigh:

1. **Write amplification.** Every mutate now appends the payload to the log. Fine for intent/ledger/attestation volumes; for a high-write cache-shaped store it needs aggressive checkpointing or that store opts out of event-sourcing.
2. **The kernel inversion is the big call.** `sema`'s INTENT today is "redb is the typed store." Making the log authoritative and redb a view is a genuine change to the kernel's contract — exactly the kind of thing that must not be decided by a designer alone. It is `sema`/`sema-engine` territory.
3. **Not every component may want it.** spirit clearly does (it already hand-rolls history, archiving, supersession on top of a current-state store — this absorbs that). repository-ledger already is event-shaped. A purely derived/cache store might not. So this is plausibly a *capability of `sema-engine` that a component turns on*, not a universal kernel mandate.
4. **Does this duplicate or subsume spirit's existing `state_digest` and archive DB?** spirit already computes a blake3 `state_digest` (`store.rs:714-758`) and copies retired records into a separate `*.archive.sema`. If the log is authoritative those become redundant — confirm this *replaces* them rather than sitting beside them.

## Bottom line

The substantial design is one decision with consequences, not a pattern list: **make `sema-engine`'s commit log payload-bearing, hash-linked, and authoritative; demote the redb store to a materialized view; represent migration as a typed log entry; back up by shipping the log.** It resolves the type-migration tension the report raised, it's a concrete diff against the real `sema-engine` types, and it explicitly rejects the prolly-tree and git imports that were cargo-culted from beads. It supersedes the Stage-3 "native content-addressed remote" hand-wave in file 6. The risk it carries — inverting which layer is the source of truth — is the part that genuinely needs the kernel owners, not a designer's say-so.
