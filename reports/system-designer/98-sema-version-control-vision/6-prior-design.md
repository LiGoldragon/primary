# 98/6 — The prior design corpus (reports 91-97, operator 211/214/215) — decision ledger

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
This chapter reads reports/logs rather than code and was not adversarially verified.*

# Sema Version-Control System: Design Corpus Decision Ledger

## Executive Summary

The design corpus traces an evolution from operator 211's conservative same-file versioned log (current production baseline in `sema-engine` @ `c970d3f2`) through designer reports 92–94 (reusability analysis and concept validation), to reports 95–97 (grand design and first-cut implementation handoff). The arc converges on a **three-stage data-loss protection system** with deferred DVCS/crypto/federation features. The psyche has decided the kernel inversion (log as authoritative, redb as rebuildable view), targeted Spirit as the first component, and scoped the first cut to schema-centric payload-bearing backup.


## 1. DECIDED with Psyche Authority (Spirit Record IDs)

All decisions cited here are anchored to Spirit records recorded in the designer reports or operator audits.

### Core Architecture
- **`29pb` (Durability constraint):** Component Sema databases must have atomic, server-backed, native version-controlled durability; state loss is unacceptable. Pursue native version control (not opaque blob backup). *(Report 91/0, affirmed 97/0)* The atomic file snapshot floor is **not** 29pb's satisfaction on its own; 29pb demands native, which means the log.
- **`j487` (Reusability constraint):** The version-control mechanism must be built **once** as a library of generic types and traits, not reimplemented per component. Every component opts in optionally. *(Report 92/0)*
- **`i4ak` (DVCS decision):** The reusable component VC system is foundational and must support full DVCS semantics (branch, fork, rebase, merge) over typed database with per-component customizable intake/merge/rebase policy. Default + override model; Spirit's guardian mediates rebase by admitting/rejecting/transforming. *(Report 95/0)*
- **`x0ja` (Crypto constraint):** One consistent cryptographic basis: blake3 for all content addressing, criome BLS for signing and attesting history; no per-component divergence. *(Report 95/0)*
- **`jys2` (Design principle):** Design at the post-agent capability frontier; target the best end-shape, not historically-practical compromise, while still proving correctness with witnesses. *(Report 95/0)*
- **`iir4` (Kernel inversion decision, psyche-chosen):** The log is authoritative; redb is a rebuildable materialized view. Restore and daemon resume rebuild the view from the log. *(Report 97/1; psyche framing in 97/11)*
- **`dun9` (Privacy direction):** Rethink Spirit as a federation of key-scoped encrypted versioned stores on the GoPass model. *(Report 96/0)*

### First-Cut Implementation (Report 97, Psyche-Decided)
- **First target component:** Spirit (irreplaceable intent records; laptop failure must not lose them). *(Report 97/1)*
- **Server is tailnet-trusted, no per-suffix auth.** Crypto deferred. *(Report 97/1)* Gitolite/tailnet host is **ouranos** (not prometheus, which is the Btrfs storage target). *(Report 91/6 corrections; verified in 91/4 and 94)*
- **Schema-centric:** Version-control machinery is schema-defined and schema-generated (per-family identity + closed-sum decoder emitted from `.schema`). *(Report 97/4)*
- **`sema-engine` is the home layer** for versioned log + checkpoint infrastructure. Not the low-level `sema` kernel; not a new `sema-vcs` crate initially. *(Operator 214 decision, affirmed in report 97/1)* Future extraction to `sema-vcs` possible after engine nouns settle, but not now.


## 2. DESIGNED-BUT-OPEN: Grand Design (Reports 95–96) vs First-Cut Scope (Report 97)

The grand design (95, 96) is the long-term target; report 97 is the first cut. The following are designed but explicitly deferred:

### Report 95: Grand Design (DVCS + Crypto + Branch Semantics)
- Branching/forking as named movable cursors (frontiers) over commit DAG. *(95/8 §4)*
- Deterministic policy-driven merge with typed `Conflict` entry on same-key overlap; `IntakePolicy` gates every path. *(95/8 §7)*
- Rebasing: replay suffix through guardian (write-admission function invoked on replayed entries). *(95/8 §8)*
- BLS-signed checkpoints/heads: RFC-6962 Merkle history tree; `FastAggregateVerify` collapses N-witness quorum to ~48-byte signature. *(95/8 §1 move 5)*
- Migration as branch: rebuild on side branch, verify digest, post-migration checkpoint, sign head, atomic advance main. Zero-downtime. *(95/8 §1 move 7)*

### Report 95: Four Open Decisions (§9)
1. **Home layer:** Recommendation: log + checkpoints in `sema-engine`; DVCS + policy + attestation in `sema-vcs`. **Operator 214 override:** keep all in `sema-engine` for now; extract later if warranted. *(95/9 Decision 1)*
2. **Default ConflictPolicy:** Recommendation: typed-conflict (never silently clobber); per-family opt-in to last-writer or CRDT. *(95/9 Decision 2)*
3. **Cross-schema merge:** Recommendation: refuse loudly first; add `Isomorphic`-reducer projection later. *(95/9 Decision 3)*
4. **Multi-LCA/criss-cross:** Recommendation: refuse loudly; build virtual merge bases when real topology appears. *(95/9 Decision 4)*

### Report 96: Federation + Privacy (Key-Gated Multistore)
- Rethink Spirit as federation of key-scoped encrypted versioned stores (GoPass model). *(96/0)*
- Per-store keys; each encrypted to recipient set; access = key possession; per-store key = erasure unit. *(96/0)*
- Two open questions to psyche: single-root nuclear option (Q3), federation key distribution (Q4). *(96/0)*


## 3. OPERATOR POSITIONS: Audits 211, 214, 215

### Audit 211 (June 12) — Operator's Audit of Spike Proposal 93

**Verdict:** Report 92 (constraint map) strong. Spike 93 (concept branch) useful proof-of-concept, not integration candidate. Operator's mainline landing (`c970d3f2`) is the right conservative first stage.

**Accept:** Report 92 as constraint map; `sema-engine` as home layer; same-file log as production first stage; closed-sum schema-hash decoding as next target.

**Reject:** Merging spike wholesale; treating spike tests as backup/remote-durability proof; replacing cursors with digests; any open decoder registry.

**Defer:** Kernel inversion; append-frame backend; reducer artifact identity. **(Later psyche-decided in report 97.)**

**Hardening push-backs:**
- Spike's same-file arm does not demonstrate same-transaction log-plus-view (in-memory view). Mainline does. **Designer accepted in 94.**
- Identical-digest test only first equivalence witness, not proof of "decidability." Needs duplicate-send, expected-head, crash injection. **Designer corrected in 94.**
- No concrete checkpoint payload. Largest gap. **Designed in 94 §2.**
- Reducer dispatch underspecified; needs artifact identity. **Recorded in 94 §4 as deferred.**
- Real consumers (mind/criome) not exercised. **Mind now opts into mainline.**

### Audit 214 (June 12) — Operator's Refresh (Supersedes 208–213)

**Verdict:** Report 95 strongest design surface. Accept as target, not implementation spec. Implementation must pass hard gates: per-family identity, checkpoint payload, restore/import API, mirror outbox, idempotent remote append, crash/read-after-write witnesses.

**Non-negotiable constraints:**
- Monotonic cursors beside digests. *(214 §Non-Negotiable)*
- Same-file until witnesses green. *(214)*
- **Checkpoints must include payload.** Checkpoint digest can *verify* but not *restore*; need `CheckpointSegment`. *(214)*
- Server-committed outside redb txn; mirror outbox in same txn; wait at request layer. *(214)*
- **Family identity stable & semantic.** Generated `FamilyIdentity` (stable id + table coord + schema hash). *(214)*
- Store schema identity derived. *(214)*
- **Restore needs engine-owned import path.** Preserves sequences, digests, tombstones, checkpoint rows. *(214)*
- Policy decisions durable. Log lineage, verdict, reason, transformed payload. *(214)*
- Policy deterministic w.r.t. rebuilt base, never live head. *(214)*
- Remote ingest two modes: dumb backup mirror vs semantic peer (runs `IntakePolicy`). *(214)*
- Privacy/retention part of remote contract. "Never GC" cannot be unexamined default. *(214)*

**Implementation order (operator's staged path):**
1. Typed family identity on same-file log.
2. Checkpoint payload + restore/import.
3. Mirror outbox + remote append.
4. Branch frontier + commit DAG.
5. Universal policy replay.
6. Signed proofs + RFC-6962 tree.
7. Migration as branch.

**Ten acceptance witnesses:** Same-transaction, payload-replay, checkpoint-restore, pruned-ancestor, remote-append, admission-bypass, policy-provenance, branch-CAS, migration-branch, crash. *(214 §Operator Acceptance Tests)*

### Audit 215 (June 12) — Privacy, Retention, Erasure Spectrum

Opens privacy/retention/erasure design that report 96 develops. Explicitly deferred from report 97's first cut. Establishes matrix of store classes (public, private, sensitive, highly-sensitive) with per-class retention/erasure rules.


## 4. WHAT 97 COMMITS AN IMPLEMENTER TO

### Staged Build: Stages 1–3 = Data-Loss Protection; 4–7 Deferred

**Stage 1 — Typed per-family identity:**
- Evolve `VersionedLogOperation` to typed `FamilyIdentity { stable_family_id, table, schema_hash }`.
- Catalog: `TableRegistration { table, schema_hash }`.
- Derive store schema hash from sorted inventory of family identities.
- Tests: replay rebuilds typed state; table rename/schema-label drift cannot silently corrupt identity.

**Stage 2 — Checkpoint payload + engine-owned restore:**
- `CheckpointMetadata { store_name, store_schema_hash, family_inventory, covered: CommitSequenceRange, view_digest (full 32-byte blake3), previous_checkpoint_digest, checkpoint_digest }`.
- `CheckpointSegment` records: sorted `(family, key, payload)` data, content-addressed by blake3.
- Engine-owned import path (NOT ordinary `assert`) preserving original sequences, head digests, metadata logs, checkpoint rows, tombstones.
- **Test (data-loss-recovery proof):** Restore from segment + suffix into fresh store; assert normal query surface reads identical records.

**Stage 3 — Mirror outbox + remote append:**
- Durable local `MirrorOutboxRow` in same engine transaction as write.
- Mirror actor ships suffix; records ack.
- Server (ouranos): holds head `(commit_sequence, entry_digest)`; validates `request.previous_entry_digest == server_head`; idempotent dedup by entry-digest; fsync before ack; rejects gaps/forks.
- **Durability levels:** local-committed → queued-for-mirror → server-committed. Server-committed wait at component request layer.
- **Tests:** Duplicates idempotent; expected-head mismatch rejects; server fsyncs before ack; crash witness at each boundary.

**After Stage 3:** Psyche protected against laptop loss. Fresh machine restores from ouranos.

### Read-After-Write & Crash Safety (Load-Bearing)
- Local commit returns only after local view applied entry in same transaction. *(97/1)*
- On restart, view self-heals by replaying log past applied watermark. *(97/1)*
- Every state change appends to log; no out-of-band redb writes. *(97/1)*
- Migration must become logged operation (not current full-rewrite + `fs::rename`). *(97/1)*

### Schema-Centric Generation
- Stable `schema_hash` per family = blake3 of canonical schema definition. *(97/4)*
- Field change → new hash → forced migration. Hash derived from schema. *(97/4)*
- Generated `RecordFamily` impl: `schema_hash()`, `encode`/`decode`, `record_key`. *(97/4)*
- Generated per-component **closed enum + closed-sum decoder:** `decode(schema_hash, bytes) -> ComponentRecord`. Unknown hash = hard error, never fallback. *(97/4)*

### Deferred (Do NOT Build Now)
- Branching/fork/merge/rebase + commit DAG. *(97/9)*
- `IntakePolicy`/guardian (use trivial default-admit only). *(97/9)*
- BLS + RFC-6962; **criome out**. *(97/9)*
- Zero-downtime migration as branch. *(97/9)*
- Privacy, encryption, multi-store federation. *(97/9)*


## 5. TENSIONS

### Grand Design (95–96) vs First-Cut Scope (97)
**Tension:** Report 95 designs full DVCS/branching/merge/crypto/federation. Report 97 is "data-loss protection only" with deferred features.
**Resolution:** **Intentional scope split by psyche's authority.** Report 95 is long-term target; report 97 is first cut. Path from 97 to 95 is clear (stages 4–7 of operator 214's implementation order). *(97/0, 95/0)* No contradiction; properly framed sequencing.

### Kernel Inversion: Deferred (211 §Defer) vs Decided (97/1 & Psyche in 97/11)
**Tension:** Audit 211 deferred kernel inversion. Report 97 states psyche decided it (Spirit `iir4`).
**Resolution:** **Psyche's decision supersedes 211's deferral.** Psyche chose `iir4` in 97/11. The `sema-engine` owners now **must implement** this (or escalate if infeasible). Load-bearing for read-after-write (97/1) and view self-healing. *(97 §1 correctness conditions)*

### Home-Layer: Operator 214 Overrides Report 95/9 Decision 1
**Tension:** Report 95 §9 recommends new `sema-vcs` crate. Operator 214 overrides: keep all in `sema-engine` now.
**Resolution:** **Operator 214's override is current decision.** Don't create new repo boundary until nouns settle. Extraction seam is documented; will be mechanical later. *(214 §Current home-layer decision; 97/1)*

### Report 97 §8: "No Actual Backup Yet"
**Tension:** Says "no actual backup yet — only a log." But Stage 2–3 claim data-loss protection.
**Resolution:** Stage 1 is **prerequisite**, not deliverable. **Deliverable is after Stage 2:** checkpoint + restore = actual backup. The greatest doubt is a caution: "don't stop at log; you need checkpoint and restore." *(97/8 §1)* This is **intentional signposting**, not contradiction.


## 6. STALE or OVERREACHING CLAIMS

### Report 91 (Beads Reality)
**Claim:** "Beads retired in practice" — quiet since Jun 9; agents migrated to Spirit.
**Status:** Factually correct for Jun 9 activity patterns. Beads dormant by INTENT.md design. Not contradicted; historically bounded. *(91/1, 91/1 §5)*

### Report 93 (Spike) — "Decidable Experiment"
**Claim:** Same-file vs separate-file is "a real, decidable experiment."
**Overreach:** Only **first semantic-equivalence witness**. Does not prove durability under duplicates, crashes, or pruned-head recovery. *(211 §3)* **Report 94 reframes as "first equivalence witness," not proof.** Properly corrected. *(94 §Two corrections)*

### Report 95 Grand Design — "Disjoint-Key Merges Are Free"
**Claim:** "disjoint keys eliminate the ConflictPolicy leg."
**Overreach:** Disjoint keys eliminate ConflictPolicy, **not** IntakePolicy. Guardian can still reject/transform disjoint-key entries on semantic grounds. *(95/8 §7 itself contains correction; 214)*
**Status:** **Self-corrected in report.** *(95/8 §7 "precise claim (corrected from earlier overstatement)")*



## keyClaims
- CLAIM: The psyche has decided the kernel inversion (log as authoritative, redb as rebuildable materialized view) as Spirit record `iir4`, overriding operator audit 211's deferral to the sema-engine owners.
  EVIDENCE: 97/1 'Invert the kernel...the psyche has now decided it'; 97/11 subsection 'Answered by the psyche' lists (a) as psyche decision; 97/1 correctness conditions (a) and (b) make this load-bearing for read-after-write and view self-healing.
- CLAIM: The first-cut scope (report 97) delivers data-loss protection only (server-backed restore capability) and explicitly defers DVCS, crypto, and privacy features to stages 4+ (per operator 214's implementation order).
  EVIDENCE: 97/0 'Protect component Sema state against data loss'; 97/9 'Out of scope (designed, do not build now)': branching, IntakePolicy, BLS/criome, migration-as-branch, privacy/encryption; 214 §Implementation Order stages 4–7 enumerate the deferred features.
- CLAIM: The home layer for versioned log + checkpoint infrastructure is `sema-engine` (not a new `sema-vcs` crate initially), per operator 214's override of report 95/9's recommendation.
  EVIDENCE: 97/1 'Home layer: `sema-engine`. Extend the mainline'; 214 §What Not 'Do not create `sema-vcs` now'; 214 §Current home-layer decision 'these engine-side nouns land in `sema-engine` now...a later neighboring crate remains possible after the nouns settle.'
- CLAIM: The schema-centric design generates the version-control machinery from the `.schema` file, emitting per-family `RecordFamily` impl and a per-component closed enum + closed-sum decoder, avoiding stringly selectors and open `Box<dyn Decoder>` fallback.
  EVIDENCE: 97/4 'A generated per-component closed enum + closed-sum decoder'; 97/4 'unknown hash is a hard error, never a fallback'; report 92 §4 'Option E' (sealed trait + closed enum as the recommended candidate); 211 §What SD Got Right affirms closed-sum as the knife-edge.
- CLAIM: Checkpoint payload (CheckpointMetadata + CheckpointSegment) is non-negotiable and the largest remaining gap before remote backup can work; a checkpoint digest verifies state but cannot restore it without the segment.
  EVIDENCE: 211 §5 'Largest remaining design gap'; 214 §Non-Negotiable 'Checkpoints must include or reference snapshot payload...need `CheckpointSegment` or equivalent'; 97 Stage 2 designs concrete structure.
- CLAIM: The restore/import path must be engine-owned and distinct from ordinary `assert` calls, preserving original commit sequences, head digests, metadata logs, checkpoint rows, and tombstones to ensure fidelity.
  EVIDENCE: 214 §Non-Negotiable 'Restore needs an engine-owned import path...unavailable to ordinary mutation handlers'; 97 Stage 2 'An engine-owned import path (NOT ordinary `assert` calls)'; 97 Stage 2 test is the data-loss-recovery proof.
- CLAIM: Monotonic `CommitSequence` cursors remain the ordered primary identifier for range queries, replay, subscription, and handoff; content-addressed digests (blake3) serve identity, verification, and inclusion proofs beside them (not replacing).
  EVIDENCE: 92 §1 'Digests sit beside monotonic markers, not replacing them'; 214 §Non-Negotiable 'Monotonic cursors stay beside digests...`CommitSequence` remains the ordered cursor'; this is affirmed consistently across 211, 95/8, and 214.
- CLAIM: The remote server (ouranos, Gitolite/tailnet host) in this cut is tailnet-trusted with no per-suffix authentication; criome BLS signing and encrypted transport are deferred to the grand design.
  EVIDENCE: 97/1 'Server: a new minimal append-ingest daemon on `ouranos`...No decryption, no signing (deferred)'; 97/8 §5 'The server has no authentication (criome deferred)...acceptable for single-psyche trusted tailnet *for now*'; 97/9 defers 'BLS-signed + RFC-6962-verifiable history; criome.'
- CLAIM: The operator's ten acceptance witnesses (same-transaction, payload-replay, checkpoint-restore, pruned-ancestor, remote-append, admission-bypass, policy-provenance, branch-CAS, migration-branch, crash) are the done-gates before the design is production-ready.
  EVIDENCE: 214 §Operator Acceptance Tests lists all ten; they are cross-referenced in 97 §6 'Acceptance witnesses'; these replace the earlier six spike tests that audit 211 correctly flagged as insufficient.
- CLAIM: The grand design (reports 95–96) supports full DVCS semantics with policy-mediated branching, merging, rebasing through IntakePolicy/ConflictPolicy, and federation with key-scoped encryption, but these are deferred from the first cut.
  EVIDENCE: 95/0 frame asks for 'branching / forking', 'rebasing', 'merging', 'DVCS semantics'; 95/8 §1–§8 designs the machinery; 96/0 designs federation; 97/9 defers 'branching/fork/merge/rebase + commit DAG', 'IntakePolicy/guardian', 'BLS-signed + RFC-6962', 'migration as branch', 'privacy, encryption, multi-store federation.'
- CLAIM: The psyche has decided Spirit `dun9` (privacy direction): rethink Spirit as a federation of key-scoped encrypted versioned stores on the GoPass model, where per-store keys are the access boundary and crypto-shred erasure unit.
  EVIDENCE: 96/0 'Spirit `dun9`...break it up into multiple stores...separate private stores for separate concerns...GoPass model'; this is explicitly deferred from the first cut (97/9) but designed in report 96.

## openQuestions
- Does the psyche want the same-file log to be human-readable (NOTA projection) or only binary rkyv on disk? (97/8 §6 flags this as unclear)
- Should the post-migration checkpoint storage use explicit reducer-artifact identity in the log, or does the checkpoint payload alone suffice for durability without keeping old reducers executable? (94 §4 / 97/8 §8 defers this)
- Which component stores opt into versioning via VersioningPolicy, and which remain opted-out (accepting write amplification as a tradeoff for backup fidelity)? (97/8 §3)
- Should Spirit's three databases (live + archive + guardian) consolidate into one authoritative log, or opt into the VC library independently? (92 §2 / 94 defers this)
- For the remote server's durability levels (local-committed → queued-for-mirror → server-committed), what is the acceptable RPO when ouranos is unreachable, and should there be a degraded-mode queuing strategy? (92 §6 / 97/8 §5 names it as a real gap)
- What is the concrete behavior when a component's reducer (From-chain) needed for replay no longer exists in the running code? (211 §4 / 94 §4 / 97/8 §8 remains unsolved)
- Should the first-cut server implement Merkle inclusion/consistency proofs (RFC-6962 tree), or is plain append-only storage sufficient for the initial deployment? (97 defers this; 214 stages it as Stage 6)
- For report 95's Decision 2 (default ConflictPolicy), should each component family have a separate default (last-writer for caches, typed-conflict for Spirit), or one global rule with per-family override? (95/9 Decision 2 / 214 §Current Open Decisions)
- Should the guardian's decision cache (git-rerere-like learned merges) be implemented to make repeated rebase/merge admission cheap? (214 §Current Open Decisions notes this is open)
- What is the acceptable scope for the new `sema-vcs` crate when eventually extracted from `sema-engine`, and what criteria trigger the extraction decision? (97/1 / 214 defer this; the boundary will be mechanical later)

