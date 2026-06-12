# 100 — Sema version control, implementation phase 2: frame, recovery, status

Phase 2 ran twice: the first run (`wf_9da92403-3c4`) died on the session
usage limit mid-build, but both builders' worktrees survived with real
content (the schema-next family-declarations leg ~80% done and green; the
sema-engine fold leg with `checkpoint.rs`/`fold.rs` written but unwired; the
schema-rust-next leg untouched). A continuation run (`wf_948413c9-560`, 4
agents) absorbed the recovered state from precise per-worktree briefs and
finished everything. Both branches **approved by adversarial review, zero
must-fix**; reviewers re-ran every suite themselves.

| Chapter | Branches (pushed) | Verdict |
|---|---|---|
| `1-record-family-emission.md` | schema-next `storage-family-declarations` (`89fe33a9`, on `schema-content-identity`), schema-rust-next `record-family-emission` (`9892d59d`) | approve, 0 must-fix |
| `2-versioned-fold.md` | sema-engine `versioned-fold` (`39991c18`, on `versioned-family-identity`; 0.4.0, storage layout 3) | approve, 0 must-fix |

## What phase 2 establishes

- **Stored record families are schema-declared**: `EntryFamily (Family {
  record Entry table entries key Domain })` as namespace metadata on the
  stream precedent — lowered to semantic `FamilyDeclaration`, round-tripping
  source and rkyv, with typed unknown-record/duplicate errors.
- **The version-control machinery is generated from the schema** (the
  report-97 §4 deliverable, realized): per-family blake3 identity consts
  computed at generation time from the family closure, the closed
  `RecordFamily` enum whose impl owns descriptors / `versioning_policy()` /
  `decode(identity, bytes)` with typed hard errors on unknown family AND
  hash drift, referencing real `sema_engine::` paths on the signal-frame
  precedent. A schema field change moves exactly that family's emitted
  const.
- **The log is restorable** (`iir4` + `29pb` realized engine-side):
  `Engine::checkpoint()` (metadata + 1 MiB content-addressed payload
  segments, derived artifact — logs no entry), `ImportSession` (minted only
  by `Engine::begin_import` on a fresh store, `&mut Engine` borrow as the
  structural exclusivity) restoring sequences, digests, chains, tombstones,
  identified counters verbatim; `Engine::rebuild_from_log()` folding the
  view from checkpoint + log with per-entry digest recomputation (tamper
  cannot ride a stored digest); the **mirror outbox** written in the same
  transaction at the single `insert_versioned_row` choke point all seven
  write paths and import share, with idempotent head acknowledgement and
  typed `LocalCommitted / QueuedForMirror / ServerCommitted` durability.
- **Storage layout 3** hard-fails layout-2 stores typed (their versioned
  entries lack outbox rows — a mirror would ship incomplete history);
  sema-engine 0.4.0.

## Advisory follow-ups carried into phase 3

Tamper-path witnesses (doctored entry/segment/acknowledgement never
behaviorally exercised) — phase-3 agent task. Beads-worthy, filed at arc
close: `RecordKey` wants a domain-key|identifier sum (identified keys ride
decimal strings); a brace-map structural shape in nota-next would let
stream+family bodies drop their precedent-bound string-keyed field walks
(the one disclosed v0n6 residue, blocked on derive vocabulary);
`CommitLogOperation::new` typed-guard restoration; `Schema::new` wants a
parts struct (9/7 arguments).

## Status after phase 2

Nine branches pushed, all reviewed and approved, spanning nota-next,
schema-next (3), schema-rust-next, triad-runtime, sema-engine (2), mind.
Phase 3 (running): spirit's families + versioning opt-in + the v8→v9
logged-fold migration pilot (`t0tu`); the mirror triad repos (`0yx5`) with
the daemon on the tailnet listener consuming the outbox wire shape; the
end-to-end witness — component store → outbox → TCP ship → mirror store →
fresh-store restore; tamper witnesses on the fold.
