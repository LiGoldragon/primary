# Spirit corpus rebuild — meta-signal re-import, the timestamp reality, certainty re-derivation

Thinking on the psyche's direction (2026-06-12): a privileged re-import path (set timestamp,
bypass guardian) as a meta-signal contract part; split the CLI into `spirit` + `meta-spirit`;
and have the designer act as guardian over the whole corpus — finding stale/superseded intent,
working instructions, over-detailed dead designs, duplicate intent, and re-deriving the
reflexively-inflated certainty. Captured this turn: `opbj` (meta-signal Import requirement),
`nik8` (legacy certainty unreliable). The two-CLI split is held as a lean pending ratification.

## The timestamp reality — we did not keep them, and order is gone too

Checked definitively against the live store and schema:

- **`Entry` has no time field:** `{ Domains Kind Description Certainty Importance Privacy
  Referents }`. No timestamp, no creation field.
- **SEMA storage has none either.** The store is an **rkyv snapshot keyed by random 96-bit
  base36 ids**. `Observe` returns records id-sorted (`0dsr 0dys 19dm …`), i.e. random order —
  insertion order is not preserved. The only temporal datum is the database-level
  `commit_sequence` counter (the `1459`), which is **not attached to individual records**.
- **The guardian journal is append-only with a sequence**, but it only logs decisions made
  *after* the guardian existed — the ~13 recent records, not the 1100 legacy ones.

So: **wall-clock timestamps were never recorded, and per-record creation order is unrecoverable
from the store.** "Re-import with the right timestamps" has no source data to draw on for the
legacy corpus. The psyche's suspicion ("maybe we lost that data") is correct — it was never
captured.

### What this means — and a design fork

The current design is **timeless by construction**: intent evolution is meant to be encoded by
**supersession lineage** (`Supersede` retires the old arrow and points to its replacement), not
by timestamps. That is a coherent "current-state knowledge base" model — and notably, the dry
run (report 597) detected 28 supersessions **purely from content**, with no clock at all. So the
rebuild's core need ("more recent intent corrects older") is satisfiable *without* timestamps:
supersession is content-detectable.

Three ways forward, to choose from:

1. **Stay timeless (recommended).** No timestamps. Evolution lives in supersession lineage,
   which we rebuild correctly anyway. Simplest, consistent with the existing design. The
   meta-signal Import still preserves *identity* (ids) so lineage/referents survive.
2. **Add a creation-time field.** Stamp real wall-clock on new records going forward; for the
   legacy rebuild, either leave it absent (`None`) or write a coarse inferred band. Do **not**
   fabricate precise fake timestamps — that manufactures false provenance.
3. **Archaeology (high effort, partial).** Recover coarse time bands from external sources —
   `reports/` numbering, primary's git/jj history that references decisions/records. Low
   resolution, real cost; only worth it for a few load-bearing records, if at all.

Designer lean: **(1) for the rebuild**, optionally **(2) going forward** (a real
creation-timestamp on new records is cheap and honest). The "preserve timestamps" instinct is
mostly served by preserving *identity + supersession lineage*, which we will.

## Meta-signal `Import` — the privileged path (design)

The meta-signal contract today is tiny — only `Configure` (set the archive DB target). Add a
second operation:

```
[Configure Import]
[Configured Imported Rejected]
{
  Import        ImportRequest
  Imported      ImportReceipt
  Entry             spirit:signal:Entry           ;; reuse the working-signal Entry verbatim
  RecordIdentifier  spirit:signal:RecordIdentifier
  ImportedRecord    { RecordIdentifier * Entry * creation (Optional CreationMarker) }
  ImportedRecords   (Vec ImportedRecord)
  ImportRequest     { records ImportedRecords }    ;; atomic batch
  ImportReceipt     { RecordCount * DatabaseMarker * }
}
```

- **Bypasses the guardian, by design and correctly.** The guardian gates *unvetted incremental*
  writes. A bulk restore of an *already-curated* corpus must not re-litigate each record (it
  can't — running 1269 records through incremental dedup against a growing store is circular and
  would choke). Guardian-bypassing writes live **only** on the meta-signal contract; the working
  signal stays fully gated (`opbj`).
- **Preserves identity** (and optionally a creation marker) so referents and supersession
  lineage survive the move to a fresh database.
- **Atomic batch** — import the whole curated set as one transaction into a fresh DB.
- **This is the general restore/migrate path, not a rebuild one-off** — the same op serves
  disaster recovery and machine-to-machine moves. That argues for building it as a permanent
  contract member, which it is here.
- **Authenticated/privileged** — consistent with the meta-signal being the privileged channel
  (the hard-override "authenticated binary meta-signal").

## The `meta-spirit` CLI split (proposal — held as a lean)

Map the two-contract triad onto two clients:

- **`spirit`** — the working-signal client: the gated everyday operations (Record, Observe,
  Lookup, Count, Supersede, Retire, ChangeCertainty, …).
- **`meta-spirit`** — the meta-signal client: the privileged operations (Configure, Import). It
  folds in and supersedes the current ad-hoc `spirit-write-configuration` bin.

Both stay thin clients (the CLI is the daemon's first client, not a triad leg). `meta-spirit`
encodes NOTA → rkyv and sends the binary meta-signal frame over the privileged socket; the
daemon never parses NOTA. This is a clean realization of the split, but it is the part the psyche
floated as "thinking of" — **needs ratification before it's a Decision.**

## Certainty re-derivation — a first-class curation axis

The Magnitude scale has 8 levels — `Zero Minimum VeryLow Low Medium High VeryHigh Maximum` —
plenty of room the corpus never used (it clustered at High/Maximum reflexively). Proposed rubric
(certainty = confidence/currentness):

| Level | Use |
|---|---|
| **Maximum** | Foundational invariants / hard overrides, repeatedly ratified, stable. |
| **VeryHigh** | Ratified decisions clearly in force, no open edges. |
| **High** | Solid decisions, minor open questions. |
| **Medium** | Working decisions / design directions still settling — *the honest home for most "ticks" that got Maximum.* |
| **Low / VeryLow** | Leans, proposals, "thinking of," explicitly-pending-info. |
| **Minimum** | Weak / tentative signal. |
| **Zero** | Removal candidate (soft-deleted; default query floor excludes these). |

The curation pass re-evaluates each surviving record against this rubric — reading the kind
(Decision/Principle vs Clarification), the hedging in the language, and whether it's been
partly superseded. This is a new axis alongside re-domain and dedup, and directly answers
`nik8`.

## Method B' — extract → curate-as-guardian → re-import

The psyche's flow, integrated with 596/597:

1. **Phase 0 (operator / code):** meta-signal `Import`; `meta-spirit` CLI; (optional)
   creation-time field if we pick timestamp option (2).
2. **Phase 1 (extract):** dump all 1407 records into size-bounded files (the sim's extraction
   tooling already does this). Each carries id + full entry.
3. **Phase 2 (curate = designer-as-guardian, workflow):** per record/cluster decide — keep /
   merge-duplicate (retire with lineage) / drop non-intent (working instructions, status) /
   drop or supersede stale over-detailed dead designs / re-domain / **re-derive certainty**.
   Output: the **import manifest** (the curated record set, ids preserved, honest certainty,
   correct domains), persisted — unlike the throwaway sim.
4. **Phase 3 (psyche ratify):** review the manifest batched by domain-cluster — distribution,
   the drop/supersede ledger, the certainty changes.
5. **Phase 4 (re-import):** `meta-spirit` imports the ratified manifest into a **fresh database**.
6. **Phase 5 (cutover):** swap the fresh DB in; the guardian maintains it from there.

The fresh-DB-via-import is the clean realization of the guardian fixpoint (596): the imported
set *is* the curated baseline by construction, and the guardian gates everything after.

## Open decisions for the psyche

1. **Timestamps:** stay timeless via supersession lineage (recommended), add a creation-time
   field going forward, or invest in archaeology? My lean: timeless for the rebuild, real
   timestamps forward if you want provenance from here on.
2. **Ratify the `meta-spirit` split?** (Currently a lean — `spirit` working-signal client +
   `meta-spirit` meta-signal client, folding in `spirit-write-configuration`.)
3. **Import = atomic batch into a fresh DB, preserving original ids?** (Recommended yes — keeps
   referents/lineage intact.)
4. **Ratify the certainty rubric** above, or adjust the bands.
5. **Curation aggressiveness:** how hard to cull "working instructions" and over-detailed dead
   designs vs. keep-conservatively. The sim was very conservative (2 drops); your framing says
   there's "probably a bunch" — so a more aggressive non-intent/stale pass is warranted, with
   you ratifying the drop ledger.
6. **Run the real curation?** This is the bigger, manifest-persisting version of 597 — with
   certainty re-derivation and stale/non-intent culling as first-class. I run it; you ratify.
