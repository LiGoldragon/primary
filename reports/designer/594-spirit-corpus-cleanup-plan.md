# Spirit corpus cleanup — action plan

The Spirit store grew to **1408 records before the guardian existed**. Those records never
passed admission, so the corpus carries what the guardian now rejects on sight: duplicates,
stale arrows superseded but never retired, non-intent that slipped in, compound records, and
~1100 records mis-filed in the `(Information Documentation)` catch-all. As the psyche put it:
*replay the database against itself and the guardian would refuse a great deal.* This plan
makes the corpus what the guardian assumes it already is — mutually consistent and
deduplicated — without losing a single genuine arrow.

## What the survey shows

| Signal | Count | Implication |
|---|---|---|
| Total (cert≥Min) | 1408 | the working set |
| Decisions + Principles | 511 + 382 = **893** | highest duplicate density — the same arrow restated as intent evolved |
| Corrections | 187 | each likely supersedes an earlier arrow that may still be live (stale) |
| Already zero-cert | 45 | cleanup half-started; collectible now |
| `(Information Documentation)` | ~1100 | the mis-filing — domain re-tag (was deferred) |

## Principles (non-negotiable)

- **Only the psyche supersedes psyche intent** (`skills/intent-maintenance.md`). Every tool
  here **proposes**; the psyche **disposes**. No automated deletion of genuine intent.
- **Conservative dispositions** — prefer *merge* (keep one canonical, retire the rest with
  lineage) and *supersede* over hard *remove*. A cluster of duplicates is a **signal of
  importance**: bump the canonical's importance, don't just discard.
- **Every change carries a justification** (`r57r`) — "duplicate of X", "superseded by Y",
  "non-intent".
- **Back up first; never lose intent.**

## Disposition vocabulary (per record / cluster)

`merge` (bump canonical + retire dups) · `supersede` (lineage-visible replacement) ·
`remove` (hard — only for genuine non-intent) · `re-tag` (domain change, keep the arrow) ·
`keep`.

## The phases

### Phase 0 — prerequisites (before touching the store)

1. **Fix guardian finding 1 first** (report 593) — the over-broad retrieval bundle currently
   makes the guardian's duplicate judgment unreliable (it just cited an unrelated record as a
   "duplicate"). Cleanup leans on dedup judgment; do it with a reliable guardian.
2. **Back up** the `.sema` store and the guardian journal.
3. **Scope decision (psyche):** public records (privacy `Zero`) only, or include elevated-
   privacy intent? Default: **public only** unless you direct otherwise (privacy override).

### Phase 1 — survey (read-only, LLM-assisted)

Fan out over the corpus **by domain-cluster** (each agent takes one domain's records, reads
them together, and returns a structured map): near-duplicate clusters, likely-stale
(superseded by a later Correction/Decision), likely-non-intent, compound, and mis-filed
(wrong/catch-all domain → proposed precise nested domain). Output is a **candidate-disposition
list** — nothing applied. This is the right unit because reviewing a topic's whole set at once
is how duplicates and mis-filings become obvious.

### Phase 2 — psyche ratification (batched)

The psyche reviews candidate dispositions **one domain-cluster at a time** — proposed
canonical, proposed merges/retirements, proposed re-tags — approving, editing, or rejecting
per batch. *This is "going through all the records again," but guided: you read a ranked,
de-duplicated, pre-dispositioned view of one topic, not 1408 raw rows.*

### Phase 3 — apply (guarded writes)

For ratified dispositions: bump canonical importance, retire/remove dups (with justification),
supersede stale, `re-tag` mis-filed (domain change preserving the arrow). All through the
fixed guardian, each with its justification.

### Phase 4 — validate

Re-survey: the store should now be deduplicated, correctly-tagged, internally consistent. A
guardian replay-consistency check on a sample should find little — the corpus now matches what
the guardian assumes.

## Choices for the psyche

1. **Dedup detection — dedicated LLM batch pass (lean) vs the live guardian.** The guardian
   only judges one-new-record-vs-bundle and catches just *exact* duplicates deterministically;
   near-duplicates across 893 Decisions/Principles need an LLM comparing within a cluster. Lean:
   batch pass for *detection*, guardian for the *apply* writes.
2. **Ratification granularity — by domain-cluster (lean)** vs by kind vs flat.
3. **Scope — public only (lean)** vs include private.
4. **Fold in the re-tag** — do the mis-filing fix (~1100 records) in the same domain-cluster
   pass (lean: yes — you're already reviewing each domain).

## Execution

Phases 1 and 3 are **scale work over 1408 records that one context can't hold** — the natural
fit is a Workflow: fan out the survey by domain-cluster → synthesize the candidate list →
(psyche ratifies) → fan out the guarded apply. I can launch the **read-only Phase 1 survey**
as soon as you approve the shape and the four choices above; it writes nothing and returns the
quantified candidate list to ground Phase 2.

## Net

The deploy was clean, but it exposed a pre-existing debt: a guardian-era store still holding
pre-guardian cruft. The fix is a conservative, psyche-ratified, domain-cluster-by-cluster pass
that dedups, retires stale, removes non-intent, and re-tags the catch-all — proposed by LLM at
scale, disposed by the psyche, applied through the (fixed) guardian. Sequence it after
finding 1's guardian fix.
