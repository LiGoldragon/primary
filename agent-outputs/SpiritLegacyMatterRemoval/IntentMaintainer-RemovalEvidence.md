# Spirit Legacy MATTER Removal — Execution Evidence (2026-06-29/30)

## Task and scope

Execute the approved archive-first removal of exactly 631 Spirit intent records
(the legacy MATTER set adjudicated from
`reports/legacy-disposition/spirit-strict-rejudge-ledger-2026-06-29.md`). Do NOT
re-judge records. Preserve a 20-id keep/repackage set plus `10pz`. Concurrent
writer on the store is expected and out of scope. Deployed Spirit 0.18.1.

## Outcome (success condition met)

- 631 / 631 records archived-then-removed. 0 resisted.
- All 20 preserve ids remain live (`RecordFound`, certainty >= VeryLow).
- `10pz` remains live.
- `346n` and `n9fl` left untouched (live).
- Live active set after op: 22 records (= 20 preserve + 346n + n9fl).
- Zero-certainty set after op: 0.

## Removal set composition (631)

From the ledger MATTER fences (620): architecture-doc 384, skill 97,
spirit-manual 76, code 33, vocabulary-doc 12, repo-intent 11, junk-remove 7.
Plus 10 borderline-out ids (q9n2 48y4 ki6i lrfa nu76 op4b qoku hu84 j81n h0bj)
and `xlfo` (the missing 98th skill id) = 631. Assembled set had 0 internal
duplicates and 0 overlap with the preserve set. All 631 verified live
(`RecordFound`) before mutation.

## Mechanism used (two-step, guardian-free, archive-first)

Confirmed by source (scout map at
`agent-outputs/SpiritNotaWireShapes/Scout-SituationalMap.md`) and empirically:

1. Soft-remove each id below the active floor via the signal socket:
   `spirit "(ChangeCertainty (<id> Zero))"` -> reply `(CertaintyChanged (<id> Zero))`.
   631/631 succeeded (zNEW9 first as a probe, then 630 batch, 0 failures).

2. GUARD: confirmed the Zero-certainty set was EXACTLY the 631 ids before the
   physical sweep. Pre-op Zero set was empty (0). After soft-remove,
   `(Count (Any Any Any Any None Any (ExactCertainty Zero) Any))` -> 631, and a
   full `Observe` of the Zero set diffed to an EXACT id-for-id match with the
   631 removal set (0 extra, 0 missing). No concurrent record sat at Zero.

3. Physical archive-then-retract via meta socket:
   `meta-spirit "(CollectRemovalCandidates (<8-field-query> (<testimony> <reasoning>)))"`
   over `(ExactCertainty Zero)`. Reply `(RemovalCandidatesCollected ...)`.
   Source: archive happens first, retract only on archive Ok
   (`store/mod.rs:637-638`); this is the only physical-deletion path and is NOT
   guardian-gated (`engine.rs:779`). A second identical run returned an empty
   collection, confirming idempotent completion. Post-op Zero count = 0.

Notes on the deployed wire shape (0.18.1), all verified live:
- Query is 8 positional fields: DomainMatch, KeywordMatch, TextMatch,
  ReferentSelection, SelectedKind (`Option<Kind>`, bare `None` for any-kind),
  PrivacySelection, CertaintySelection, ImportanceSelection.
- `Count(Query)`: `(Count (<8-field-query>))` -> `(RecordsCounted N)`.
- Certainty filter variants: `(ExactCertainty <Mag>)`, `(AtLeastCertainty <Mag>)`.
- `Remove` is NOT a wire op on this deployment. `Retire` exists (signal,
  logical only, no physical delete). Neither was used.
- CLIs set the live sockets via wrapper env: `spirit.sock` and
  `meta-spirit.sock` under `/home/li/.local/state/spirit/`.

## Backups and recovery

Pre-op backups (sha256-verified copies of the live and archive stores):
- Live store:    `/home/li/.local/state/spirit/spirit.sema.preremoval-631-20260630T000025`
- Archive store: `/home/li/.local/state/spirit/spirit.archive.sema.preremoval-631-20260630T000025`

Archived records (recoverable): the live archive store
`/home/li/.local/state/spirit/spirit.archive.sema` grew from 774144 to 1736704
bytes during the collect and now contains all 631 removed records. Spot-checked
present across every category: 06l6, zNEW9, xlfo, q9n2, h0bj, hp9n, ztX, 8dib,
1i1b.

Recovery path if a record must be restored: the full pre-op live store is the
`spirit.sema.preremoval-631-20260630T000025` snapshot (contains all 631 at their
original certainty); the post-op archive holds the archived copies. Restoring a
single record means lifting it from the archive store (or the pre-op live
snapshot) back into the live store via the deployed re-record/restore path. To
roll back the entire op, swap the live store back to the pre-op snapshot while
the daemon is stopped.

## Preserve set (verified live, never touched)

19 keep/repackage: jlo7 ty3g w312 9g07 izsf j8g6 sfy0 obo5 jys2 sj2c cam8 t5qr
zn2l (keep) + o7zt k09z c5nq hv5f gni3 qjrf (repackage sources). Plus 10pz.
All 20 returned `RecordFound` before and after the op.

## Checks run (exact results)

- Preserve liveness before: 20/20 RecordFound.
- 631 removal ids live before: 631/631 RecordFound, 0 missing.
- Soft-remove: 631/631 CertaintyChanged, 0 fail.
- GUARD: Zero-cert set == removal set EXACTLY (diff both directions empty).
- Meta collect: RemovalCandidatesCollected; second run empty (idempotent).
- Removal ids after: 631/631 gone (0 still present).
- Preserve liveness after: 20/20 RecordFound; 346n, n9fl live.
- Active count after: 22; Zero-cert count after: 0.
- Archive store contains removed records (size grew; spot-checks present).

## Blockers / follow-up

- None blocking. Removal complete and fully reconciled.
- Follow-up (separate pass, NOT done here): rehoming the removed MATTER into the
  owning durable surfaces (architecture docs, manuals, skills, repo INTENT.md),
  several homes being untracked repos requiring a psyche hold/edit-untracked
  call. This was explicitly out of scope for the removal task.
- The intent-maintainer lane on `/home/li/.local/state/spirit` should be
  released after this report.
