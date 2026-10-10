---
title: 64 — Concept — Spirit hash identity + time-based recency
role: system-designer
variant: Concept
date: 2026-06-04
topics: [spirit, identifier, hash, recency, time, stability, query, concept]
description: |
  Concept for the psyche's decision (Spirit 2581/2582/2583): Spirit record
  identifiers become unique hashes (stable, never reused), and recency moves to
  daemon-stamped time (agents catch up via "records since time T") instead of
  numeric id order. Grounds the current reuse bug (RecordIdentifierMint computes
  max(current records, commit_sequence)+1, so removing the highest record frees
  its id), designs the two halves (hash assigned-once-and-immutable for identity;
  time-Since queries for recency — already largely in the contract), and surfaces
  the genuine open questions the psyche invited: hash type, citation ergonomics,
  and migration of the existing integer-id corpus.
---

# 64 — Concept: Spirit hash identity + time-based recency

Kind: concept (designer concepts the chosen direction; operator implements)
Topics: spirit, identifier, hash, recency, time, stability, query
Date: 2026-06-04

## Intent Anchors

[Spirit record identifiers must not be reused after removal; reuse makes references unstable because a later record can occupy the same identifier.] (Spirit 2581 Correction High)

[Durable Spirit identity should not rely on reusable incremental numbers; unique hashes are a better identity direction, while recency tracking should use daemon-stamped time.] (Spirit 2582 Principle Medium)

[Spirit should support agent catch-up queries from a recorded time so agents can retrieve intent added since their last read without depending on numeric identifier order.] (Spirit 2583 Decision High)

[Removing a record currently frees its identifier for reuse — a Principle capture took id 2572, the freed slot of a deleted test record — so an identifier is not a stable handle across removals.] (Spirit 2580 Principle High)

## 1. The decision, in one line

Split the two jobs a sequential id was secretly doing. **Identity becomes a
unique hash** — stable, assigned once, never reused. **Recency becomes time** —
agents track what is new by daemon-stamped time, not by id order. The decision
is captured (2581/2582/2583); this concept designs it.

## 2. Why the split is the right shape

A sequential integer id quietly carried two meanings: *which record this is*
(identity) and *how recent it is* (order). That coupling is the bug. Identity
must be stable forever; recency must reflect time. When the same field does
both, you cannot make identity stable without freezing recency, and the
current allocator chose recency (derive from the live set) at the cost of
identity (reuse on removal). Splitting them lets each be correct: the hash
never moves and never repeats; time orders by when, not by a counter that
removal can rewind.

## 3. The current reuse, in code

Production `persona-spirit` mints the next id from the *current* record set:

```rust
// persona-spirit/src/store.rs:638-651
impl RecordIdentifierMint {
    fn from_records_and_commit_sequence(records: &[StoredRecord], commit_sequence: u64) -> Self {
        let last_record_identifier = records
            .iter()
            .map(|record| record.identifier.value())
            .max()
            .unwrap_or(0);
        let next = last_record_identifier.max(commit_sequence) + 1;
        Self { next }
    }
    fn next_identifier(&self) -> RecordIdentifier { RecordIdentifier::new(self.next) }
}
```

Because `last_record_identifier` is `max()` over the *live* records, deleting
the highest record lowers the max, and the next insert reuses the freed value
(2572). `commit_sequence` is a floor, not a per-id ledger, so it does not
prevent reuse of a freed top slot. `RecordIdentifier` is a `u64` newtype today.

(The schema-derived spirit had a persisted monotonic `next_identifier` counter
that does *not* reuse — but the psyche's decision moves past even monotonic
integers to hashes, because a monotonic integer still invites
recency-by-id-order, which is exactly what time is meant to own.)

## 4. Design — identity as a unique hash

- **Assigned once, immutable for life.** This is the load-bearing constraint:
  `ChangeCertainty` mutates a record's certainty without changing which record
  it is, so the identity must survive mutation. A *live* content-hash would
  change when certainty changes and break the handle. So the hash is computed
  **at creation and frozen** — never recomputed.
- **No derivation from the live set.** The mint generates the hash at creation
  (from entropy, or from a creation-fixed fingerprint — see Q1); it never reads
  the current records. Removal therefore cannot free anything — there are no
  numeric slots to free. The reuse bug becomes structurally impossible.
- **Type change.** `RecordIdentifier` becomes a fixed-width digest newtype
  (e.g. a blake3 byte array) instead of `u64`. `RecordIdentifierMint` is
  replaced by a creation-time hash mint; `last_record_identifier` /
  `next_identifier` (max-based) are deleted.

## 5. Design — recency as time

This half is largely already in the contract — it mostly needs to become the
*primary* recency surface and be deployed.

- Every record already carries daemon-stamped `Date` + `Time` (in
  `RecordProvenance`).
- `RecordedTimeSelection` already has `Since(RecordedTime)`, `Until`,
  `Between`, plus the depth shortcuts `Recent/Shallow/Deep/VeryDeep`. The
  catch-up query 2583 asks for — "records recorded since time T" — is
  `Since(T)`. So the recency-query shape exists; the work is ensuring it is
  first-class, deployed, and the default way agents track new intent.
- Agents catch up by holding their own last-read time and querying `Since(that
  time)`. Ordering is by time; the depth shortcuts return newest-N by time, not
  by id.

So the new construction work concentrates on the **hash identity**; the
**time recency** is mostly an existing capability promoted to primary + a
deploy step.

## 6. Open questions for the psyche (you invited these)

**Q1 — hash type: random, or creation-fixed fingerprint?** Both must be
assigned-once to survive mutation. Random/UUID is simplest and carries no
accidental meaning. A creation-time content fingerprint (hash of the original
topics+kind+description+timestamp) additionally gives content-addressing and
natural dedup of identical captures, at the cost of complexity and the
subtlety that it must be frozen at creation. **Lean: random/opaque hash** —
simpler, and Spirit records are mutable so content-addressing buys little;
dedup can be a separate concern.

**Q2 — citation ergonomics (the big one).** The entire intent culture cites
"Spirit 2543" — a short integer a human can read and type. A hash is opaque.
How do agents reference a record in prose, reports, links, and `[[ ]]`-style
intent anchors? Options: full hash; a short prefix (git-style 7-12 chars);
hash + mandatory description; or lean on time+topic instead of id in prose.
**Lean: short prefix + mandatory inline description** (already the workspace
rule for opaque ids — "bead `primary-hj63` (the README rewrite)"), with the
full hash as the canonical wire identity. This keeps citations human-skimmable
while identity stays stable.

**Q3 — migration of the existing integer-id corpus (also big).** Records
1..~2583 exist with integer ids referenced across every report, skill, and
`INTENT.md`. Re-hashing them would break the entire existing citation corpus.
Options: (a) grandfather — existing records keep their integer ids, new
records get hashes (a hybrid id space); (b) one-time migration that assigns
hashes to all and keeps an `int -> hash` map so old citations still resolve;
(c) full re-id and accept the citation break. **Lean: (a) grandfather** —
least disruptive, no broken citations, and the hybrid is honest (old records
*were* integer-identified). This interacts with Spirit 2551 (do not cut the
default daemon over to a new database until existing intent is migrated/
reachable), so the migration shape and the new-spirit cutover are coupled.

**Q4 — time-catch-up shape.** Does the existing `RecordedTimeSelection::Since`
satisfy 2583, or do you want a per-agent read-watermark/cursor the daemon
tracks? **Lean: `Since(time)` suffices** — agents hold their own last-read
time; the daemon stays stateless about per-agent cursors.

**Q5 — hash length/format.** blake3 full digest as the wire identity; the
display short-prefix length (Q2) trades skimmability against collision
probability. **Lean: full digest on the wire, ~10-12 char prefix for display.**

## 6.1 — Resolved (psyche answers, 2026-06-04)

**Q1 → random hash** (Spirit 2590 superseded by 2599). The id is a random hash
assigned once at creation and frozen — unique, never reused. The psyche struck
the content-fingerprint direction: because records are mutable (ChangeCertainty
and other edits), a content-address hash adds computation for very little value.
(This restores the section's original Q1 lean.)

**Q3 → full migration to hashes** (Spirit 2591 superseded by 2611). Migrate ALL
existing records to random-hash ids now, not grandfather. Existing integer
references may break (acceptable); a transitional dump file maps former integer
ids to the new hashes, kept around briefly so agents can resolve old references
during the transition, then retired. Yields a uniform hash id space.

**Q2 → short, not big hashes** (Spirit 2592). Cited ids must be ~3 chars in a
base larger than hex, combined with the kind — big hashes are token-expensive
gibberish in LLM context. Recommended scheme:

- **Canonical = the full random hash, binary on the wire** (rkyv) — no
  token cost there; it never appears as text unless rendered.
- **Display / citation = the shortest-unique base36-lowercase prefix of the
  hash, minimum 3 chars, scoped per kind**, extended (4, 5, …) only when
  a same-kind collision requires it (git-style shortest-unique). base36
  lowercase is beads-proven, case-safe (no A-vs-a errors), larger than hex
  (36 vs 16), and 3 chars give 46,656 values *per kind* — ample even with all
  records migrated (a few hundred per kind today; collisions extend to 4 chars). (base62/58 allow even
  shorter but case-sensitivity is error-prone; Crockford base32 is the
  alternative if excluding ambiguous characters matters more than matching
  beads.)
- **Citation form** keeps the existing cite-by-description rule (Spirit
  1533/1546): `[description summary] (Spirit <Kind> <short>)` — e.g.
  `(Spirit Decision a4f)`. The Kind word supplies semantic context and the
  partition; the 3-char code is the cheap address. With full migration, every
  record cites with a short code; a transitional integer→hash dump file bridges
  old `(Spirit 2543 …)` references until it retires.

This supersedes the Q5 "~10-12 char prefix" lean: the display prefix is ~3
base36 chars within a kind, not 10-12 hex. **Confirmed by the psyche 2026-06-04
(Spirit 2608):** base36-lowercase + per-kind 3-char minimum + kind-in-citation
is the scheme. The id design is now fully decided; the operator is unblocked.

## 7. For the operator (who is implementing)

- Replace `RecordIdentifierMint` (max+1) with a creation-time hash mint;
  change `RecordIdentifier` from `u64` to a digest newtype; delete the
  max-based `next_identifier`/`last_record_identifier`.
- Promote `RecordedTimeSelection::Since`/`Between` to the primary recency
  surface and ensure the deployed binary serves them (the recency query shape
  already exists in the contract).
- Gated on Q1 (hash type), Q2 (citation format), Q3 (existing-id migration) —
  these change the id type, the display convention, and the migration path.
  The recency half is mostly existing capability + deploy.

## See also

- `reports/system-designer/63-sema-engine-boundary-conformance-audit-2026-06-04.md` — the storage boundary these records live behind.
- `/git/github.com/LiGoldragon/persona-spirit/src/store.rs:638-651` — `RecordIdentifierMint`, the current reuse logic.
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` — `RecordIdentifier` (u64 newtype), `RecordedTimeSelection` (Since/Until/Between + depths), `RecordProvenance` (Date+Time).
- Spirit 2580 (the problem), 2581/2582/2583 (the decision), 2551 (cutover precondition coupling to the migration).
