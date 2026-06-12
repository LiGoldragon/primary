# 97 — Implementation handoff: server-backed version control for component Sema state (first cut)

**Audience: an implementing agent with no prior conversation context.** Read
this file plus the four references in §10. It tells you exactly what to
build, in what order, against which repos, with which types, and what is
deliberately *out of scope*. The grand design (reports 95, 96) is the
long-term target; **this handoff is the small, safe, realistic first cut**
the psyche asked to ship now.

## 0. The goal of THIS cut

**Protect component Sema state against data loss** — if the psyche's laptop
dies, restore a component's full state from a server backup. Nothing more.

In scope: a payload-bearing, replayable backup log (extend what already
exists) → checkpoint + restore → a remote mirror on a server. That chain is
the data-loss protection. Out of scope (designed, do not build now): see §9.

The psyche's framing: *"I would really like to first get at least some kind
of version control so that at least we're protected against data loss in case
of something happening to my laptop."* Privacy is *"not the absolute most
important variable right now"*; **criome stays out of this cut** (kept for
future). Everything is *"centered around schema types"* (§4).

## 1. Decided architecture (the simplest realistic shape)

These are decided — implement them, do not re-litigate:

- **Invert the kernel: the log is authoritative, redb is a rebuildable view**
  (Spirit `iir4` — the psyche chose this over the simpler log-as-backup). The
  versioned operation log is the source of truth; the redb store is a
  *materialized view folded from the log*. Restore and daemon resume **rebuild
  the view from the log**. This is bigger than the mainline's current
  parallel-log seed (§2), and it is exactly the change operator 214 deferred
  to the `sema`/`sema-engine` owners — the psyche has now decided it.
  *Correctness conditions, now load-bearing because the log IS the truth:*
  (a) **every** state change appends to the log — no out-of-band redb writes;
  the migration path (currently a full rewrite + `fs::rename`) must become a
  logged operation or that history is lost. (b) **read-after-write must not
  lag** (audit 208): a local commit returns only after the local view has
  applied the entry in the same transaction; on restart the view self-heals by
  replaying the log past its applied watermark.
- **Home layer: `sema-engine`.** Extend the mainline (§2); settle the nouns
  here; no new crate yet (operator 214).
- **First target component: Spirit** (the psyche's choice — the irreplaceable
  intent records are exactly what a laptop failure must not lose). Spirit is
  not yet opted into the versioned log, so wiring it is part of the work;
  `mind` (already opted in) is a useful second to prove the path.
- **Server: a new minimal append-ingest daemon on `ouranos`** (the
  Gitolite/tailnet host). It stores shipped log suffixes per component store,
  append-only, idempotent; validates sequence continuity + expected-head
  (the entry-digest chain); fsyncs; acks. **No decryption, no signing**
  (deferred). Trust = the tailnet (single-psyche). See §5.
- **Crypto in this cut: blake3 content addressing only** — the entry-digest
  hash chain that already exists. **No BLS, no encryption** (criome/privacy
  deferred).
- **Schema-centric:** the version-control types are schema-defined, and the
  per-family identity + closed-sum decoder are **schema-generated** (§4).

## 2. What already exists on mainline (`sema-engine` @ `c970d3f2`)

The operator landed a conservative seed; build from it, do not bypass it.

- `EngineOpen::with_versioning(VersioningPolicy { store_name, schema_hash })`
  enables an opt-in payload log. `mind` (@ `7e29a4f4`) opted in.
- `src/versioning.rs`:
  `VersionedCommitLogEntry { store_name, schema_hash, commit_sequence,
  snapshot, previous_entry_digest, entry_digest, operations }` — a
  domain-separated, length-prefixed blake3 hash-chain.
  `VersionedLogOperation { operation, table_name: String, key,
  payload: Record{bytes} | Tombstone }`. The versioned entry is inserted in
  the **same redb transaction** as the domain mutation and the metadata
  `COMMIT_LOG` (the valuable atomicity). `versioned_commit_log()` /
  `versioned_replay_from_sequence()` read it back.
- **Gaps (why there is no real backup yet):** the schema hash is
  **store-level** (not per-family); the decode selector is a
  **`table_name: String`** (not typed family identity); there is **no
  checkpoint payload**, **no restore/import path**, and **no remote/server**.
  So today there is a *log* but **no way to restore** — restore is the whole
  point and the biggest missing piece.

## 3. The build, staged (Stages 1–3 ARE the data-loss protection)

### Stage 1 — typed per-family identity
Replace the stringly selector so replay can reconstruct typed state.
- Evolve `VersionedLogOperation` to carry a typed
  `FamilyIdentity { stable_family_id, table: TableName, schema_hash }` —
  the `stable_family_id` is distinct from the *current table coordinate* so a
  table rename/split/merge cannot be mistaken for semantic identity.
- Catalog: `TableRegistration { table: TableName, schema_hash }`.
- **Derive** the store schema hash from a *sorted inventory of family
  identities* — not a manual `mind-schema-v7` label.
- Tests: replay rebuilds typed state by family hash; a table rename or
  schema-label drift cannot silently corrupt replay identity.

### Stage 2 — checkpoint payload + engine-owned restore (the actual backup)
- `CheckpointMetadata { store_name, store_schema_hash, family_inventory,
  covered: CommitSequenceRange, view_digest (full 32-byte blake3),
  previous_checkpoint_digest, checkpoint_digest }`
  **plus** `CheckpointSegment` records holding **sorted (family, key,
  payload)** data, content-addressed by blake3. A digest *verifies* a state;
  a segment *restores* it.
- An **engine-owned import path** (NOT ordinary `assert` calls) that restores
  preserving original commit sequences, head digests, metadata logs,
  checkpoint rows, and tombstones; unavailable to ordinary mutation handlers.
- Test (**the data-loss-recovery proof**): restore from a checkpoint segment +
  the suffix into a *fresh* store; assert the **normal query surface** reads
  identical records.

### Stage 3 — mirror outbox + remote append (the SERVER side)
- A durable local **`MirrorOutboxRow`** written in the **same engine
  transaction** as the write (so the outbox can never miss a commit).
- A mirror actor ships the outbox suffix to the server and records the ack.
- Server (ouranos, §5): per store, holds the current head
  `(commit_sequence, entry_digest)`; validates
  `request.previous_entry_digest == server_head`; **idempotent dedup** by
  entry-digest; **fsync before ack**; rejects gaps/forks.
- **Durability levels** as a per-store policy: *local-committed* →
  *queued-for-mirror* → *server-committed*. A "server-committed before reply"
  wait happens at the **component request layer**, *after* the local
  transaction closes, returning a typed outcome if the mirror fails.
- Tests: duplicate sends are idempotent; expected-head mismatch
  rejects/quarantines; server fsyncs before ack; **crash witness** —
  interruption at each write/outbox/mirror boundary recovers to a consistent
  state with an explicit durability level.

After Stage 3 the psyche is protected against laptop loss: a fresh machine
restores from ouranos. Stages 4–7 (branch/DAG, policy, signatures,
migration-as-branch) are deferred (§9).

## 4. Schema-centricity and the schema-rust-next enhancement (the cool idea)

Per Spirit `a5tg` (Principle): *center the design around schema types* — the
schemas are the surface the psyche reads and reasons about most easily.
Realize it by **generating the version-control machinery from the `.schema`**:

- A stable `schema_hash` per record family = **blake3 of the family's
  canonical schema definition**, so a field change yields a new hash (which
  forces a migration) and **the hash is derived from the schema the psyche
  reads** — not hand-set.
- A generated `RecordFamily` impl per family: `schema_hash()`,
  `encode`/`decode` (rkyv), `record_key`.
- A generated per-component **closed enum + closed-sum decoder**:
  `decode(schema_hash, bytes) -> ComponentRecord`; an unknown hash is a hard
  error, **never a fallback** (the report 95/8 "Option E" knife-edge).

This makes "generated per component" real and schema-centric: author the
`.schema`, the generator emits family identity + the closed decoder; no
hand-written stringly selectors. It is the recommended core of Stage 1.

Implementation note for `schema-rust-next` (operator-owned `main`; a designer
works on a feature branch in `~/wt`): each schema type already renders itself
via `LowerToRust` (`quote!` / `proc-macro2` / `ToTokens`). Add a
`LowerToRecordFamily` (or a derive) that emits the impl + the `schema_hash`
const, and emit the closed enum at the component-schema root. **Emit into
`impl` blocks** (no free functions; rust-discipline).

**Honesty about "schema-centric":** the on-disk log stays binary (rkyv).
"Schema-centric" means the *types and their generation* are schema-defined,
and the human-readable surface is the `.schema` plus the **NOTA projection**
(CLI/debug dumps project a log entry to NOTA). It does **not** mean a
human-readable log file. (Confirm with the psyche whether they want more —
see §8 Q.)

## 5. The server, concretely (do not skip this)

A new minimal append-ingest daemon on **ouranos** (the Gitolite + tailnet
host — *not* prometheus, which is the Btrfs storage target). It is **dumb**:
no decryption, no guardian, no signing in this cut.

```mermaid
sequenceDiagram
    autonumber
    participant C as component (local engine txn)
    participant O as local mirror outbox (durable)
    participant M as ouranos append-ingest daemon
    C->>O: append outbox row IN THE SAME engine txn as the write
    O->>M: ship suffix (entries since the server head), prev = server_head_digest
    alt expected-head matches
        M->>M: dedup by entry-digest, append to per-store file, fsync
        M-->>O: ack new head (commit_sequence, entry_digest)
    else gap or fork
        M-->>O: reject; outbox backfills or quarantines
    end
    Note over C,M: restore (new laptop): pull the store's checkpoint + suffix from M, run the engine import (Stage 2)
```

- **Storage:** per-store append-only files (the repository-ledger atomic-spool
  pattern — temp-write + rename, commit-then-move — is the precedent).
- **Validation:** sequence continuity + expected-head digest; idempotent
  dedup by entry-digest; fsync before ack.
- **Auth (this cut):** tailnet-trusted, no per-suffix authentication (criome
  deferred). This is a named, accepted gap (§8 Q3).
- **Restore:** the daemon serves a store's checkpoint + suffix; the new
  machine runs the Stage-2 engine import.

## 6. Acceptance witnesses (the done-gate, from operator 214 — Stages 1–3)

- same-transaction: domain row + metadata log + payload log + outbox row +
  counters commit atomically;
- payload replay: delete/rebuild the materialized tables from the log → same
  query results;
- checkpoint restore: restore from checkpoint segment + suffix into a fresh
  store → normal-query-surface equivalence;
- remote append: duplicate sends idempotent; expected-head mismatch rejects;
  server fsync before ack;
- crash: interruption at each write/outbox/mirror boundary recovers to a
  consistent state with an explicit durability level.

## 7. Version discipline

Bump `sema-engine`'s storage-schema-version guard and package version on the
log-format change (Stage 1), per `skills/versioning.md`. The VC metadata
format carries its **own** format-version tag, distinct from the per-family
schema hash (report 95/8 §15 — two guards).

## 8. Greatest doubts (read before starting)

1. **There is no actual backup yet — only a log.** The mainline has the
   versioned log but no checkpoint and no restore, so today nothing can be
   recovered. **Stages 2–3 are the priority**; Stage 1 is a prerequisite, not
   the deliverable. Do not stop at "the log is richer."
2. **The log only protects you if it is a *complete* record.** Any state
   change that bypasses the logged write path (notably the current
   full-rewrite + `fs::rename` migration) makes restore silently wrong. The
   correctness crux is "every mutation is logged"; audit for bypasses.
3. **Write amplification.** Every write now writes the payload twice (redb +
   log). Fine for intent/ledger volumes; a high-write store should opt out of
   versioning (the `VersioningPolicy` opt-in is the mitigation). Decide which
   stores opt in.
4. **The inversion is a real kernel-contract change.** With the log
   authoritative and redb a view (Spirit `iir4`), restore fidelity becomes
   *structural* — the view is *defined* as the fold of the log, so there is no
   "parallel store can silently diverge" risk. The cost moves elsewhere: this
   changes `sema`'s contract (the thing 214 deferred to the kernel owners), and
   it makes read-after-write (§1) and deterministic replay load-bearing. Test
   restore by rebuilding the view and reading the *real query surface*, not
   just by matching a digest.
5. **The server has no authentication (criome deferred).** ouranos trusts the
   tailnet; a rogue device could overwrite/forge a backup. Acceptable for a
   single-psyche trusted tailnet *for now*, but it is a real gap — see §8 Q3.
6. **Schema-centric vs binary log.** The log is rkyv bytes; the schema
   readability is at the type/NOTA-projection layer, not the file. If the
   psyche expects a readable log, that is extra work (§4).

## 9. What is deferred, and where it is designed (do NOT build it now)

| Deferred | Design reference |
|---|---|
| Branching / fork / merge / rebase + the commit DAG | report 95/8 (the visual grand design) |
| `IntakePolicy` / guardian (use a trivial default-admit only) | report 95/8 §6 |
| BLS-signed + RFC-6962-verifiable history; **criome** | report 95/8 §9 (criome **out** this cut) |
| Zero-downtime migration as a branch | report 95/8 §11 |
| Privacy, encryption, multi-store federation (GoPass model) | report 96 (criome/privacy **deferred**) |

## 10. References (read these, in order)

1. This file (scope + the staged build).
2. `reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md` — the operator's non-negotiable constraints, staging, and the ten acceptance witnesses. **Authoritative on hardening.**
3. `reports/system-designer/95-versioned-state-grand-design/8-visual-design.md` — the grand design (what the deferred parts become).
4. `sema-engine` `src/versioning.rs` @ `c970d3f2` and `src/engine.rs` — the code you are extending.

## 11. Open questions for the psyche (must be answered before/early in implementation)

**Answered by the psyche** (these were the gating decisions):
(a) **invert the kernel** — the log is authoritative, redb a rebuildable view
(Spirit `iir4`); (b) first target = **Spirit**; (c) server is
**tailnet-trusted**, no per-suffix auth (criome adds real authentication
later); (d) schema-centric = **the VC machinery is schema-generated** —
per-family identity + the closed-sum decoder emitted from the `.schema` (§4).
All four are reflected above; the implementing agent builds to them.
