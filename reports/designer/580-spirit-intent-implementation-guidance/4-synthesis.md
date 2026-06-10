# Spirit intent redesign — implementation guidance (synthesis)

Synthesis of the three explorations — `1-corpus-patterns` (live-data mining),
`2-source-vs-design` (current source), `3-migration-and-tests` (migration +
fixtures) — all grounded in the **live v0.8.0 daemon** (store ~1410 records,
schema V3) and current source. For operator. Design reference: `578`; operator
build order: `352`.

## TL;DR

1. **One decision gates all schema work: the second axis.** `importance` shipped
   (intrinsic priority), not `weight` (reaffirmation). The duplicate-bump
   anti-bloat *engine* has no field. The live data argues for adding weight.
2. **The substrate is further along than `352`/`577` assumed.** Identifier-bearing
   observation and the certainty de-bloat keystone are **built and tested** in
   v0.8.0 — cross both off the build list.
3. **The real frontier is greenfield:** category type, keyword/full-text, the
   write-op split, typed verdicts, change events, the kind fold, and the whole
   agent/lease/harness/guardian/auditor stack.
4. **Don't start with prompts.** Substrate first — operator's standing point, and
   the live fragmentation (1323 topics, 69% singletons) makes the category spine
   the true first move, not the LLM loop.

## 1. The axis decision — gating, and now empirically answerable

Git history: `28438ae split certainty and weight` → `73cb457 rename weight to
importance` (HEAD). So `Entry` is six fields (topics, kind, description,
**certainty**, **importance**, privacy); `importance` carries intrinsic-priority
semantics (declared at capture, ranks observation), and there is **no weight
field and no weight mechanics** (no duplicate-bump, no typed weight-update, the
sort is importance-only and ignores certainty).

The fork, and why the data settles it:

- Certainty is a **near-flat ranking signal** — 81% of records are `High`
  (`1-corpus`). It can't tell load-bearing from incidental.
- Importance is **declared, not derived** — it's a human priority knob, not a
  measure of how often an intent has been independently arrived at.
- So with importance-only and no weight, the store has **no derived signal of
  what's load-bearing at all.** One arrow (the bracket-string rule) has absorbed
  8+ restatements; weight would capture exactly that, heavy-tailed.

**Recommendation: three-axis** — keep `importance` (declared priority, the psyche
chose it) *and* add `weight` (reaffirmation count, monotonic, no decay). They do
different jobs. Two-axis (rename importance→weight) loses the priority knob;
drop-weight (status quo) loses the anti-bloat engine and leaves ranking on a flat
axis. This is a Spirit-gate decision for the psyche; the schema currently encodes
drop-weight, so nothing downstream that needs weight (duplicate-bump, ranking)
can be built or tested until it's resolved.

## 2. Already shipped — do not rebuild

Verified live and in source:

- **Identifier-bearing observation.** `Observe` returns `ObservedRecord {
  RecordIdentifier, Entry }`. The `RecordSnapshot` step `352` §1 called the
  single largest blocker is effectively done — a naming nicety now.
- **Certainty/importance split + V-migration.** `Entry` is 6 fields, `Query`
  gained the parallel selector, and `production_migration.rs` implements a
  tested V1(magnitude)→V2(certainty+importance)→V3 store upgrade with V1/V2 slots
  ready for the next migrations.
- **The de-bloat keystone.** Zero-certainty records are removal-candidates;
  `CollectRemovalCandidates` collects on exact-zero and archives-then-retracts,
  tested. The `579` "marking Zero does nothing" fact was v0.4.0 and **no longer
  holds**.
- **Confirm-this discrepancy:** `1-corpus` measured the certainty floor hiding
  the 45 Zero records (1412 any vs 1367 floored) and source hides Zero from
  default observation (`store.rs:736`); `3-migration` read default observation as
  *still showing* Zero. Likely it depends on the selector (floor vs `Any`).
  **Action: make the agent-facing query default to the floor selector** so the
  guardian/auditor never see tombstones; confirm which selector is the wire
  default.

## 3. The real build frontier (greenfield)

Zero source presence today: `category` type (still free-text exact-match
`Topic`), keyword/full-text retrieval, the **write-op split** (only
`Record`/`ChangeRecord`/`ChangeCertainty` exist — no propose/clarify/supersede/
retire), typed verdicts/refusal-reasons (only structural `ValidationError`),
change **events** (`IntentEvent` has only `IntentRecorded`), the **kind fold**
(Correction/Clarification still kinds), and the entire signal-agent / lease /
harness / guardian / auditor stack (zero hits). This is where the work is.

## 4. Guardian insights from the real corpus

- **The guardian's hardest job isn't dedup — it's not trusting the agent's
  label.** Real records call themselves "refines/corrects" while *reversing*
  meaning (a trample), or "extends" while really proposing a new arrow. So the
  guardian must **independently classify the true operation** and treat the
  proposing agent's chosen op as a *hint, never a fact*. A mismatch is itself a
  refusal (you said clarify, it tramples → rejected, use supersede). Scope-widening
  defaults to a fresh propose, never a silent clarify. This elevates `578`'s
  guardian from a yes/no consistency check to a yes/no **plus operation-arbiter**.
- **Dedup is four grades, and only one is the guardian's.** Literal restatement
  (guardian-catchable) → token-disjoint paraphrase (**conceded to the auditor by
  design**) → same-arrow-plus-nuance (borderline, stay conservative) →
  design-evolution chains (**must not collapse**). So: conservative guardian,
  auditor carries the hard cases — the two-gates split, now evidenced. Tune the
  guardian for precision, not recall.
- **retire-only is a distinct operation.** Supersede must accept a **null
  replacement** — ~45 legacy records and real ongoing intent are pure retirements
  ("record 1088 was over-captured") with no successor arrow. Model retire as its
  own op, not supersede-with-empty.
- **Constraints are supersedable** (`btio` supersedes constraint 1091) — don't
  treat any kind as immutable.

## 5. The category catalog (the true first move)

- 1323 distinct topics, **69% singletons**; the `schema` family alone fragments
  into 20+ near-synonyms. The bulk of migration is collapsing these to a broad
  category + keywords.
- A **~15-category catalog covers ~92%** of records (table in `1-corpus` for the
  psyche to bless). Collisions (`mail` = signal vs assistant; `macro`; `trace`)
  argue for **multi-membership** categories with the keyword layer as the
  discriminator.
- **Category must stay a `Vec`** — 837/1411 records are multi-topic (mean 2.85);
  migration must not flatten.
- **Pass A (topic→category clustering) precedes Pass B (record agglomeration),**
  and Pass A precedes the guardian — if guardian retrieval is built on free-text
  topic, it inherits the recall problem. The category spine is the retrieval
  foundation everything downstream needs.

## 6. Migration realities

- **Kind migration is 392 records** (191 Correction + 201 Clarification),
  ~60-70% mechanical, ~30-40% needing target-location judgment. Correction
  patterns: do-X-not-Y / names-prior-record / meta-capture-gate. Clarification
  patterns: refine-arrow / gap-fill / standalone-miscoded / exploratory-maybe.
- **It is not 1:1.** ~45 records (≈35 Corrections + 10 Clarifications) yield
  *zero* forward arrows — pure retirements or speech-to-text fixes. The rewrite
  needs **three outcomes per legacy record: forward arrow / clarify-in-place /
  retire-only.** A 1:1 transform manufactures ~45 hollow records — re-bloating in
  the migration itself.
- **Insight: the kind migration *is* an agglomeration, not a transform.** It must
  be allowed to emit fewer records than it consumes. Run it through the
  auditor/agglomeration machinery, not a dumb 1:1 mapper.
- **Contradiction landmines.** All 4 of `579`'s contradiction clusters are still
  live (verified). These are irreversibility risks — **route to the psyche, never
  auto-fold.**

## 7. Keywords — net-new, a gift not a gap

The corpus has **zero asterisk-emphasis spans** — nothing to migrate, and no
legacy keyword debt. The convention starts clean with forward authoring. So
keyword work is pure forward-validation (test the extractor), and existing
records get keywords only when rewritten. **Insight: fold keyword authoring into
the migration rewrite** — when a legacy record is rewritten to a forward arrow,
mark its keywords then; don't backfill separately.

## 8. Issues and constraints

- **Axis block (§1)** — gates schema work; psyche decision.
- **Contradiction irreversibility (§6)** — the 4 live clusters must go to the
  psyche; auto-folding loses real intent.
- **Tombstone-visibility discrepancy (§2)** — confirm the wire default selector;
  make agent-facing retrieval floor out Zero.
- **Deploy in progress** — the daemon flipped from down to up at v0.8.0 mid-
  exploration; treat live numbers as a moving baseline, source as ground truth.
- **Keyword edge-case spec** — case-folding, phrase spans, repeated spans,
  literal/unmatched asterisks, interaction with bracket-string text (per `352`
  §7); deterministic and tested.

## 9. Test plan

`3-migration` lays out a **10-case fixture plan** per `352` §7, each seeded with
real record IDs and exported as `.nota` via `include_str!` (not inline Rust
strings): the five required cases (Correction folded, Clarification converted,
removal-candidate hidden-vs-visible, narrow-topic→broad-category+keyword,
duplicate-refused+weight-bump) plus clarify-tramples, unknown-category,
supersede-target-missing, multi-topic-survival, and contradictions-route-to-psyche.
The weight-bump case is **blocked on the axis decision**.

## 10. Recommended next-step order

Revised given what's already shipped:

1. **Resolve the axis** (psyche; §1) — unblocks weight, ranking, the duplicate
   case.
2. **Category catalog + topic→category migration** (Pass A) — the retrieval
   spine; psyche blesses the ~15-category catalog.
3. **Keyword + full-text discriminator** — a method on `Entry`/`Description`,
   independent of the wire; deterministic + tested.
4. **Write-op split** (propose / clarify / supersede / retire) + typed verdicts
   and refusal reasons + change events.
5. **Durable operation journal/archive** for clarify-prior, retire, supersede.
6. **signal-agent lease contract + meta-signal harness registry**, then endpoint
   auth + lease accounting.
7. **Wire the guardian** into propose/clarify/supersede (with independent
   op-classification, §4).
8. **Kind migration** through the agglomeration machinery (Pass B), with fixtures.
9. **Only then** automate the auditor.

Prompts come last. The substrate — axis, category, ops, journals, lease — is the
work that makes the guardian's judgment trustworthy instead of bloat in a fancier
shape.
