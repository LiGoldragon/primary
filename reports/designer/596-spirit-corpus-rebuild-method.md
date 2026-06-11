# Spirit corpus rebuild — method

How to rebuild the 1407-record store to a sane state the guardian can then maintain. This
refines report 594's plan with one structural correction: **the corpus is the guardian's
effectiveness problem, so re-domaining comes first** — not a guardian code fix.

## The state, grounded (live 0.9.3, marker 1459)

| Scope | Count | |
|---|---|---|
| Total (cert≥Min) | 1407 | the working set |
| `(Information Documentation)` | **1100** | **78% of the entire corpus in one leaf** |
| `(Information All)` | 1101 | i.e. all of Information *is* that one leaf |
| `(Technology All)` | **13** | the whole subject of this workspace — 13 records |

A workspace whose purpose is building daemons, schemas, and a NOTA stack has **13 records in
Technology and 1100 in a "Documentation" catch-all.** The catch-all is not documentation. A
raw sample of its first records:

- `0dsr` Constraint — *NOTA string delimiters are only required for strings with spaces…* →
  belongs in `(Technology (Software (Data Serialization)))` or `(Language Notation)`.
- `0dys` Decision — *Spirit operations should support a simpler-to-more-complex variant ladder…*
  → `(Technology (Software (Engineering ApplicationProgrammingInterfaces)))`.
- `19dm` Correction — *brace is always a key value map… a namespace is a DYNAMIC ENUM…* →
  `(Technology (Software (Data SchemaEvolution)))`.
- `3do3` Clarification — *all Rust production functions are methods on data-bearing types…* →
  `(Technology (Software (Engineering SoftwareDesign)))`.
- `3don` Constraint — *schema source lowering must reject duplicate declarations…* →
  `(Technology (Software (Data SchemaEvolution)))`.
- `1mhv` Principle — *writing as craft* → `(Art …)` / `(Language Writing)` (and a likely
  duplicate of poet-lane intent).

These are high-value arrows, correctly recorded, **wrongly filed**. The migration was
faithful; the *original* tagging was a single default bucket.

## Why the corpus is the guardian's problem (not a separate bug)

The guardian's retrieval scores `+30 shares_domain`. With 78% of records in one leaf, that
signal is dead: a query either collides with ~1100 records (noise) or with nothing. Keyword
and text overlap are weak by themselves, so domain is *supposed* to carry retrieval — and it
can't, because the corpus has effectively one domain. **The guardian can't dedup or admit
reliably until the corpus is re-domained.** This is why retrieval feels empty and why the one
live dedup we saw cited the wrong record. The fix is not (only) guardian code — it is the
corpus.

## The method's spine: re-domain first, then dedup

Two transformations, in a forced order:

1. **Re-domain (categorize).** Assign every record its precise recursive-enum domain from the
   live taxonomy. This *alone* restores retrieval — once records spread across the tree,
   `shares_domain` becomes meaningful again (a `(… Security AdmissionControl)` record retrieves
   the handful that are genuinely related, not 1100).
2. **Dedup + cull.** With meaningful clusters, collapse duplicates (keep one canonical, retire
   the rest with lineage), drop non-intent/task-state, supersede stale. This is the step that
   genuinely needs judgment — route it through the now-effective guardian.

The order is not a preference; step 2's reliability depends on step 1. Report 594 had this
backwards ("fix guardian finding 1 first"): the corpus *is* finding 1.

## "Sane" defined: the guardian's fixpoint

A sane corpus is the **fixpoint of the guardian** — every record would be admitted if
submitted fresh, no two are duplicates by the guardian's lights, each is correctly domained.
The elegance the psyche is reaching for: **the rebuild and the maintenance use one
mechanism.** If we build the baseline *by passing the corpus through the same gate that
guards it forever, then "sane" has a single definition and there is no gap between what we
built and what the gate enforces. The corpus becomes "everything that passes today's gate."

## Three shapes — recommend B

- **A — In-place curated pass.** ChangeRecord re-tags + retire dups in the existing store;
  keeps record identity/history. Conservative. (Report 594's shape.)
- **B — Guardian re-admission rebuild (recommended).** Build a *fresh* store by replaying:
  categorize → submit each as a fresh Record through the guardian → survivors form the
  baseline, rejects are journaled (dup-of / non-intent / stale). The baseline is
  by-construction guardian-clean; the reject ledger is the safety net (nothing silently lost —
  every drop is a verdict the psyche can override).
- **C — Re-author from canonical sources.** Discard the corpus, re-derive intent from
  ESSENCE/INTENT/reports/git. Highest quality, total provenance loss, most work, real risk of
  dropping arrows nobody remembers.

Recommend **B**. Pre-production, breaking record identity is free (no backward-compat to
protect), so the fresh-store fixpoint is the cleanest realization of "rebuild to a state the
guardian maintains." A and B converge once you accept re-domain-first; the only real
difference is fresh-store vs in-place mutation, which barely matters here.

## Apply mechanisms (they differ by step)

- **Re-domain → deterministic migration from a ratified mapping**, not 1100 guarded
  ChangeRecords. An LLM proposes the domain per record *offline*; the psyche ratifies the
  mapping at the distribution level; a batch migration applies it — exactly the shape of the
  existing `production_migration` that re-tagged the former-`Craft` records on the 0.9.0
  deploy. Operator owns that tool.
- **Dedup/cull → guardian-judged**, because "is this a duplicate / non-intent / stale" is the
  genuine per-record judgment the guardian exists to make.

## The other half: staying sane going forward

The rebuild fixes the past; the guardian keeps it sane *only if new records arrive correctly
domained*. The gate already has the lever: `GuardianRejectionReason` includes **`UnclearDomain`**
and `RetrievalInsufficient`. So the guardian can already refuse the next `(Information
Documentation)` dump. The forward-maintenance decision is whether the guardian should actively
*reject or correct* mis-domained records, so the corpus cannot re-rot into a catch-all. The
taxonomy is now precise enough that good domaining at admit time is achievable.

## Decisions for the psyche

1. **Method — B (fixpoint re-admission, recommended) / A (in-place curated) / C (re-author).**
2. **Re-domain apply — ratified-mapping migration (recommended) / guarded ChangeRecords.**
3. **Ratification cost — distribution-level + spot-check for re-domain; per-cluster for dedup.**
   This is the "go through the records again" cost, but guided: you review a proposed
   distribution and pre-dispositioned clusters, not 1407 raw rows. Confirm appetite.
4. **Scope — public (privacy `Zero`) only (recommended) / include private intent.**
5. **Forward gate — should the guardian actively reject/correct mis-domained records
   (`UnclearDomain`) so the corpus stays sane by construction?**
6. **Certainty interaction (note, not a blocker).** Most sampled records carry certainty
   `Minimum`; the certainty-floor work (system-designer report 88) is adjacent. The rebuild is
   the natural moment to set proper certainty/importance, but that is a separate axis — flag,
   don't fold in unless you want to.

## Execution

Phase 1 (categorize) is **read-only** scale work over 1407 records — the natural Workflow: fan
out the corpus, each agent reads a batch and proposes a precise domain per record, synthesize
into a mapping table + the resulting distribution for ratification. It **writes nothing**. I
can launch it the moment you pick a method and the scope (choices 1 and 4). Phases that mutate
the store wait on your ratification and on operator's apply tool.

## Net

The deploy was clean; it exposed a pre-guardian debt — 78% of intent crushed into one
catch-all, Technology near-empty. The rebuild is a forced two-step: re-domain (which by itself
revives retrieval), then dedup/cull through the now-effective guardian. Build the baseline as
the guardian's fixpoint and the same gate that built it maintains it. Supersedes 594's
sequencing; keeps 594's conservative "propose-LLM, dispose-psyche, never lose an arrow"
discipline.
