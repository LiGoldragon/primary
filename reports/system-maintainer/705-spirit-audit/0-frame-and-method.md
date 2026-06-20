# Spirit database deep audit — frame and method

Session: system-maintainer, 2026-06-20. Psyche directive (verbatim):

> "I want you to do a deep audit of the spirit database. I want its size
> reduced, negative guidelines removed unless absolutely necessary, and
> many records agglomerated if they obviously can be worded in a unified
> record instead of many."

That prompt is the standing authorization quote (testimony) for every
maintenance operation in this session: agglomeration (`Supersede`),
negative-guideline rewrite (`ChangeRecord`) / retirement (`Retire`),
mini-essay condensing (`ChangeRecord`), and removal
(`ChangeCertainty Zero` recoverable / `Retire` / hard `Remove`).

## Provenance snapshot

- Deployed binary `spirit 0.14.0`, user service `spirit-daemon.service`.
- Database marker at audit start: commit sequence **1432**, state digest
  `17584167288913623050`.
- Active records at start: **1323** (4 already zero-certainty; all public,
  privacy `Zero`).
- Full raw dump preserved at `raw/all-active.nota` (575 KB) and parsed to
  `raw/records.json` (the global tombstone — every record's full Entry is
  captured before any change).

## Starting shape (mechanical analysis)

| Metric | Value |
|---|---|
| Active records | 1323 |
| Kinds | Decision 551, Principle 325, Correction 171, Clarification 151, Constraint 125 |
| Total description chars | 448,485 (avg 338/record) |
| Mini-essays (≥800 chars) | 72 records, 76,153 chars |
| Records with NO referents | 1236 (93%) |
| Distinct domains | 74 (concentrated in `Technology.Software.*`) |
| Lexical near-dup pairs (Jaccard ≥0.45) | 5 — agglomeration is *semantic*, not lexical |

Two findings shaped the method: (1) the merge opportunity is semantic
(same arrow, different words), so word-overlap clustering is near-useless
and LLM judgment over topical neighborhoods is required; (2) the
referent key — the guardian's primary dedup path — is empty on 93% of
records, which is *how* the duplicates accumulated. Every rewrite in this
audit re-populates referents.

## Method

1. **Dump + parse.** Type-directed NOTA parser (`raw/parse.py`) over the
   `RecordsStashed` payload → 1323 structured records (count verified).
2. **Mechanical analysis** (`raw/analyze.py`) → domain histogram, length
   buckets, negative-keyword prefilter, near-dup clusters.
3. **Topical bucketing** (`raw/bucketize.py`) → 32 buckets, each record
   assigned once, coherent domains kept whole (Architecture 132,
   Data.Modeling 106) so intra-domain agglomeration is complete.
4. **Analysis workflow** (`spirit-db-audit`, 32 buckets × 2 stages):
   - *Analyze* — one agent per bucket reads every record and proposes
     four dispositions: agglomeration, negative-guideline reword/retire,
     mini-essay condense, removal.
   - *Verify* — an adversarial reviewer per bucket re-reads the originals
     and drops/corrects any proposal that loses a distinct arrow. Bias:
     under-merge and under-remove rather than lose intent.
5. **Render** (`raw/render.py`) — the maintainer (not the subagents)
   encodes every validated proposal into exact `spirit` NOTA, owning the
   correctness of the live-layer writes. Conflict/missing-id detection.
6. **Execute** (`raw/execute.py`) — run against the daemon with full
   guardian-reply capture; reversible operations first, hard removes held
   for explicit confirmation.

Affirmative-framing discipline (guardian Gate 6 `NegativeGuideline`) is
applied to every authored description: lead with the positive rule, never
ship a description that is itself a prohibition.

## Artifacts

- `raw/all-active.nota`, `raw/records.json` — pre-audit tombstone.
- `raw/proposals.json` — verified workflow output.
- `raw/plan.json` — rendered operations.
- `raw/exec-log.jsonl` — guardian reply per executed operation.
- Synthesis + outcome: highest-numbered file in this directory.
