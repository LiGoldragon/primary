---
role: system-designer
kind: Research
topics: [agglomeration, intent-maintenance, spirit, certainty, weight, composite]
date: 2026-06-04
---

# Intent Corpus Agglomeration Study — A Live Demonstration

## Intent Anchors

[Spirit should support composite intent records that reference older intent records as source material, so repeated or closely related intent can be agglomerated into a newer stronger record without losing provenance.] (Spirit Principle audg3)

[Intent should be refreshed by agglomeration: combine many lower-certainty records that belong together — for example fifteen Medium statements on one subject — into a single fresh higher-certainty record that fuses their ideas. Leveraging the certainty ladder this way shrinks how much agents must read while raising the authority of the synthesized statement. Older agglomerated records can then be retired under the explicit-supersession discipline.] (Spirit Principle 1zd6)

[Spirit records should distinguish certainty from weight: certainty is confidence in the statement, while weight is accumulated importance or reinforcement, especially for composite records derived from multiple source records.] (Spirit Principle 6vsl)

[Intent agglomeration must preserve provenance and archival recoverability before source records are removed or replaced, because collapsing old intent into composite records is useful but dangerous.] (Spirit Constraint 1byp)

[When composite or agglomerated intent retires its source records, the sources are archived and referenced by their hash identity from the composite record so provenance survives; the archive mechanism needs to be streamlined to carry this composite-to-archived-source link cleanly.] (Spirit Principle 73t3)

## Frame and Method

This report is a live demonstration of the composite/agglomerated-intent
concept the psyche wants. It reads the deployed Spirit corpus
(v0.5.0, live hash ids), finds clusters of repeated / near-duplicate /
many-low-certainty-saying-the-same-thing records, and for each cluster
drafts ONE concrete composite record that would fuse and replace them —
the NOTA I WOULD submit but do not. Read-only throughout: OBSERVE and
PROPOSE, never mutate.

Corpus shape from `(Observe Topics)`: the topic index is enormous —
roughly 850+ distinct topic words, many appearing once. High-count
topics: `schema` ~427, `spirit` ~165, `nota` ~150, `workspace` ~122,
`signal` ~97, `component-shape` ~82, `cloud` ~59, `sema` ~58, `persona`
~54, `reports`+`reporting` ~66, `nexus` ~41, `privacy` ~39, `naming`
~28, `workflow` ~29, `testing` ~23, `trace` ~23. The redesign-relevant
small topics are where the densest near-duplication lives:
`certainty` ~12, `identifier`/`identity`/`hash` ~15+ combined,
`recency` ~5, `intent-removal`/`removal-candidates` ~9,
`intent-maintenance` ~8, `agglomeration` ~4, `record-shape` ~4.

A note on totals: the corpus is large enough that a precise single
number isn't returned by `Observe Topics` (it counts topic-tag
occurrences, and most records carry 3-5 tags). The deployed migration
to hash ids (record 5r5z) and the highest legacy integer references
seen in descriptions (records cite numbers up to ~2620) put the live
corpus on the order of a few thousand records. The six clusters below
together hold ~45 records that fuse to ~9 composites — a representative
slice, not the whole corpus.

## Cluster 1 — Spirit recency / time-filtered query (5 records → 1 composite)

This is the cleanest pure-duplication cluster: five records all asking
for the same thing — recency/time filtering composed with topic
filtering on Spirit queries — at mixed certainty, none contradicting
each other.

Members:

- [Durable Spirit identity should not rely on reusable incremental numbers; unique hashes are a better identity direction, while recency tracking should use daemon-stamped time.] (Spirit Principle 2esr, Medium)
- [Spirit observation should support intelligent topic retrieval that emphasizes recent intent by default while adapting historical depth to topic frequency: high-churn topics stay near the edge and quiet topics reach farther back.] (Spirit Decision p4tw, High)
- [Spirit record observation should support combined recency or time filtering with topic filtering, so agents can query recent records within one or more topic selections instead of running separate searches.] (Spirit Clarification rii9, Medium)
- [Spirit should support agent catch-up queries from a recorded time so agents can retrieve intent added since their last read without depending on numeric identifier order.] (Spirit Decision 4q67, High)
- [Production Spirit should support time-range and relative-recency searches composed with topic filters, so agents can query recent records in a topic without doing manual identifier-range approximation.] (Spirit Decision 5hsz, High)

Plus the closely-related query-shape record that should be co-referenced
(it carries the concrete `RecencySelection` field shape and overlaps
heavily):

- [The Spirit record query should add a RECENCY filter as a first-class composable selector alongside TopicSelection, optional Kind, and CertaintySelection ... a fifth field RecencySelection with Any, Newest N, Since identifier/timestamp, or Window.] (Spirit Decision 1wl5, High)

Proposed composite — fuses the WHAT (recency as a first-class filter)
with the HOW (the concrete `RecencySelection` field) and the WHY
(catch-up, churn-adaptive depth). The `2esr` identity clause is NOT
fused here — it belongs to Cluster 4; only its recency clause feeds in.

```
(Record
  [spirit recency query filtering catch-up]
  Decision
  [Spirit record observation supports recency and time filtering as a first-class composable selector alongside topic, kind, and certainty filters - a fifth RecencySelection field on RecordQuery with Any for no filter, Newest N for the most recent matches, Since an identifier or daemon-stamped timestamp for a lower bound, and Window for a closed range. A single query can therefore ask for recent records on a topic at a certainty level, mixing all filter dimensions. Recency default emphasizes recent intent while adapting historical depth to topic frequency - high-churn topics stay near the edge, quiet topics reach farther back. This supports agent catch-up from a recorded last-read time without depending on numeric identifier order or manual range approximation. The daemon already stamps date-time so storage has what it needs.]
  High
  Zero
  (AgglomeratedFrom [2esr p4tw rii9 4q67 5hsz 1wl5] Weight 6))
```

Proposed certainty High (the strongest members are High and they
reinforce); weight 6 (sources fused). This is the safest agglomeration
in the corpus — zero contradiction, pure restatement at different
phrasings.

## Cluster 2 — Certainty calibration / don't-inflate (3 records → 1 composite)

Three records, two of them nearly verbatim, all saying the same thing:
Medium is the default, Maximum is rare, agents keep over-rating.

Members:

- [Medium certainty should be the normal default for routine Spirit captures unless the psyche wording, emphasis, repetition, or context justifies a higher or lower certainty.] (Spirit Clarification 1arf, High)
- [Spirit certainty must be calibrated against a benchmark ladder, not reflexively inflated. Maximum is rare ... Medium is the default ... Agents have been over-rating intent as Maximum, which corrupts the certainty signal.] (Spirit Principle 1e41, High)
- [Agents must not default psyche statements to Maximum certainty. Ordinary direct statements default to Medium; High, VeryHigh, and Maximum require evidence ... The certainty field is meaningful only if most records are not Maximum.] (Spirit Correction 2aj2, Maximum)

This cluster is the best illustration of the WEIGHT concept: three
sources, one of them at Maximum certainty, all reinforcing the same
rule. The composite should carry the Maximum certainty (the psyche
stated this as a near-axiom in 2aj2) AND a weight of 3 marking the
reinforcement — exactly the certainty-vs-weight distinction record 6vsl
asks for.

```
(Record
  [spirit certainty calibration intent-capture]
  Principle
  [Spirit certainty is calibrated against a benchmark ladder and never reflexively inflated. Medium is the default for routine captures. High, VeryHigh, and Maximum each require evidence - explicit intensity, repeated return across records, or unmistakable strong language; Maximum is rare, reserved for near-absolute founding-rule conviction stated as a universal axiom. Certainty is judged from how sure the psyche actually sounds and is a load-bearing part of intent capture, not an afterthought. The field is meaningful ONLY if most records are not Maximum; agents have repeatedly over-rated intent as Maximum, which corrupts the signal, so the calibration must be assessed honestly every capture.]
  Maximum
  Zero
  (AgglomeratedFrom [1arf 1e41 2aj2] Weight 3))
```

## Cluster 3 — Removal-candidate Zero-floor mechanism (a TRAP: looks like 8 dupes, is actually a supersession chain)

This cluster is the danger case the psyche flagged ([collapsing old
intent into composite records is useful but dangerous]). On topic-grep
it looks like eight records all about "removal candidate = bottom
certainty rung." But reading them in order reveals an EVOLVING DESIGN
with corrections, not repetition:

- [removalCandidates: removal should be a two-phase SOFT process ... Open model question: Entry.certainty likely wants certainty as an optional magnitude with None the candidate state ...] (Spirit Decision 5j92, Medium) — early, leans Option/None
- [Spirit removal candidates are represented by record certainty being absent: None means confidence withdrawn ...] (Spirit Decision 2cdx, High) — commits to None
- [Spirit removal-candidate certainty should use a shared neutral Magnitude bottom rung named Zero, not Option None; Zero avoids Option confusion.] (Spirit Decision 238k, High) — REVERSES 2cdx: Zero, not None
- [Settled: the removal-candidate floor is a new bottom VARIANT on signal-sema Magnitude named Zero ... NOT None and NOT an optional magnitude ... Zero declared first so derived Ord places it below Minimum.] (Spirit Decision c2o2, Medium) — settles Zero, but with a WRONG impl detail
- [Record 1215 carried a flawed implementation detail. The Zero variant must be declared physically LAST ... declaring Zero first shifts every pre-existing rkyv discriminant ... Semantic-bottom restored via manual Ord.] (Spirit Correction 7fhs, High) — CORRECTS c2o2's impl detail
- [Production Spirit should support live certainty changes on existing records, including using the shared Magnitude Zero floor for removal-candidate nomination.] (Spirit Decision 6g53, High) — implementation status
- [Spirit record certainty is optional at the persona-spirit entry boundary rather than a None variant inside shared Magnitude vocabulary; the absence semantics stay local to Spirit.] (Spirit Decision 5qco, High) — refines the boundary

Verdict: DO NOT naively agglomerate this as "8 duplicates." The
None-vs-Zero decision flipped (2cdx → 238k), and the declaration-order
detail flipped (c2o2 → 7fhs). A correct composite must encode the
LANDED end-state and explicitly retire the superseded steps as
provenance, NOT average them. The danger: an automated agglomerator
that fuses by topic-similarity would silently re-admit the rejected
None-floor wording or the byte-shifting Zero-first ordering. This is
the cluster the orchestrator should show the psyche as the cautionary
exhibit.

Proposed composite (landed-state only; the flipped intermediate
records are RETIRED-as-superseded with provenance, not fused):

```
(Record
  [spirit removal-candidate certainty magnitude]
  Decision
  [The Spirit removal-candidate floor is a bottom rung named Zero on the shared signal-sema Magnitude enum - NOT Option None, chosen to avoid Option-flavored confusion and to stay policy-neutral across components (persona-spirit reads Zero as removal candidate; persona-mind could read it as forgettable). Implementation: Zero is declared physically LAST in enum source order so persisted rkyv discriminants for Minimum=0..Maximum=6 stay byte-stable; semantic-bottom is restored by a manual Ord using an order_rank where Zero ranks below Minimum. Removal is a two-phase SOFT process: an agent nominates a record by lowering certainty to Zero, the record STAYS as a recoverable candidate, and only a reviewed candidate is hard-removed. Production Spirit supports live certainty changes including Zero-floor nomination.]
  High
  Zero
  (AgglomeratedFrom [c2o2 7fhs 5j92 238k 6g53] Weight 5)
  (Supersedes [2cdx 5qco]))
```

Note the split: `AgglomeratedFrom` carries the records that contribute
substance to the landed state; `Supersedes` carries the rejected
intermediate decisions (None-floor) that must be retired WITHOUT their
wording bleeding into the composite. An agglomeration mechanism needs
BOTH relations to handle this safely.

## Cluster 4 — Spirit record identity: hash vs counter (a SUPERSESSION CHAIN, mostly already self-pruning)

Fifteen records under `identifier`/`identity`/`hash`. Like Cluster 3
this is a design that CHANGED, and the change is documented as explicit
supersession — meaning Spirit's own supersession discipline already did
part of the agglomerator's job. The arc:

- Content-fingerprint hash proposed (record 27nx, Zero certainty — already withdrawn)
- [Spirit record 2590 is negated: ... should use a random/opaque hash, not a content-address fingerprint.] (Spirit Correction 3h99, High)
- [Spirit record identity is a random hash, not a content-address fingerprint ... Supersedes the content-fingerprint choice in record 2590.] (Spirit Correction 2et3, High)
- [Existing integer-identified records are grandfathered ...] (Spirit Decision 6oar, Zero — withdrawn)
- [Migrate ALL existing Spirit records to random-hash ids now ... Supersedes the grandfather decision in record 2591.] (Spirit Correction 5r5z, High)
- [Spirit random opaque identities should use 96-bit CSPRNG values, rendered through lowercase base36 shortest-unique-prefix display codes, minimum three characters per kind.] (Spirit Decision 4a0v, VeryHigh)

And a citation sub-cluster (4 records) that IS genuinely fusable:

- [Spirit ids must be cited SHORT - not big hashes ... a short code, around three characters, in a base larger than hexadecimal, combined with record kind.] (Spirit Decision 1s1l, High)
- [Spirit random hash identifiers should render as lowercase base36 shortest-unique-prefix short codes, minimum three characters per kind.] (Spirit Decision 5u5x, VeryHigh)
- [Spirit short-identifier scheme confirmed - shortest-unique base36-lowercase prefix of the random hash, minimum three characters, scoped per kind, cited as bracket-quoted description plus (Spirit Kind short).] (Spirit Decision d3mw, High)
- [Spirit prose citations should remain description-first, with record kind and short code as secondary locator.] (Spirit Clarification 6kwe, High)

Verdict: the design-evolution records (content-fingerprint → random
hash → migrate-all) are already pruning themselves via Zero certainty +
explicit Supersedes. The agglomerator's job here is the CITATION
sub-cluster (1s1l, 5u5x, d3mw, 6kwe), which says one thing four times.
Proposed composite for the citation sub-cluster:

```
(Record
  [spirit identifier citation short-id base36]
  Decision
  [Spirit cites record identity SHORT - never the full hash, which is token-expensive gibberish for LLM context. The displayed/cited code is the shortest-unique base36-lowercase prefix of the record random hash, minimum three characters, scoped per record kind and extended only on a same-kind collision. The full random hash stays binary on the wire; only the short prefix appears in text. Prose citations are description-first: bracket-quoted description summary, then the kind and short code as a secondary locator - the short code supplements the description, never replaces it.]
  VeryHigh
  Zero
  (AgglomeratedFrom [1s1l 5u5x d3mw 6kwe] Weight 4))
```

The identity-mechanism records (4a0v + the Supersedes chain) should be
left to settle on their own as a separate landed composite once the
migration completes; do NOT fold them into the citation composite.

## Cluster 5 — Report context-maintenance / agglomerate-don't-accumulate (~12+ records → 2 composites)

The single most bloated near-duplicate cluster in the corpus. The
`reports`/`reporting`/`context-maintenance` topics carry well over a
dozen records that all say variations of "reports are not an archive;
agglomerate by topic into refresh reports; retire stale ones." Tiny
near-identical records:

- [context maintenance must reduce active reports] (Spirit Correction 2rso, High)
- [Context maintenance should agglomerate reports into current summaries] (Spirit Principle 3y15, Medium)
- [active report lanes should stay well below twelve] (Spirit Principle 3sj6, High)
- [Context-maintenance report passes should agglomerate old lane reports after refreshing intent] (Spirit Principle 4th0, High)
- [context maintenance repackages older relevance into fresh context] (Spirit Clarification 6qzo, High)
- [Reports are NOT an accumulating archive ... rewritten/refreshed into current-state reports ... a small load-bearing set, not a large historical pile.] (Spirit Principle 2f5d, High)
- [The goal of context maintenance is to reduce the number of reports without losing information, by agglomerating topics ... Refresh is the report variant tag ...] (Spirit Decision 7dkh, High)
- [Closed reports should not be kept merely for rationale or history ... move live patterns into architecture or skills, then retire.] (Spirit Correction 5a8v, High)
- [Aggressive consolidation: move old reports into re-contextualized new reports leaving out stale context.] (Spirit Decision 7ab2, High)
- [Context maintenance means repairing the existing context surface ... Adding a new report without correcting stale reports is not sufficient.] (Spirit Correction 6xdn, High)
- [Reports not in the working tree live in the commit tree ... jj show / git show ... supersession-deletes-in-the-same-commit is safe.] (Spirit Principle 3xxd, High)
- [Report lane is active/dynamic, not the resting place for architectural ideas.] (Spirit Principle 40se, High)

Two coherent composites emerge (this is itself a lesson: a fat cluster
often fuses to MORE than one record, not one):

Composite 5a — the policy:

```
(Record
  [reports context-maintenance agglomeration retention]
  Principle
  [Reports are NOT an accumulating archive - they are a small load-bearing set, not a historical pile; history lives in jj/git (a deleted report is one jj-show or git-show away, so supersession-deletes-in-the-same-commit is safe). The report lane is active and dynamic, never the resting place for architectural ideas. Active report lanes stay well below twelve. Context maintenance repairs the existing surface: it agglomerates many reports on a topic into ONE refreshed current-state report that preserves un-contradicted un-superseded substance in a better form, then RETIRES the sources. Closed reports kept only for rationale or history are not kept - their live patterns move into architecture or skills first, then the report retires. Adding a new report without correcting or retiring the stale ones is insufficient.]
  High
  Zero
  (AgglomeratedFrom [2rso 3y15 3sj6 4th0 6qzo 2f5d 5a8v 6xdn 3xxd 40se] Weight 10))
```

Composite 5b — the mechanism (the Refresh variant + topic prefixes):

```
(Record
  [reporting refresh-variant topic-prefix filename-convention]
  Decision
  [Context maintenance produces a Refresh report - the capital report-variant tag after the number - that rewrites and merges several source reports on one topic into a single report; the sources are then deleted with the Refresh report as the landing witness. Report filenames carry topic labels between the number and the title (N-topic-title.md or N-topic1-topic2-title.md) drawn from a controlled per-workspace topic vocabulary, enabling filename-based topic-grep without opening reports. Aggressive consolidation, when the psyche directs it, re-contextualizes old reports into new ones and leaves stale context behind in the deleted originals.]
  High
  Zero
  (AgglomeratedFrom [7dkh 7ab2 179h 54vg] Weight 4))
```

## Cluster 6 — The agglomeration mechanism itself (4 records → 1 composite, the meta-record)

The records DESCRIBING agglomeration are themselves a fusable cluster —
fitting, since this study demonstrates the concept. Members are the
five Intent Anchors at the top of this report (audg3, 1zd6, 6vsl, 1byp,
73t3). They are not duplicates — each adds a facet — but they belong
together as ONE dense mechanism statement, which is exactly the
"fifteen Medium records → one fresh higher-certainty record" shape 1zd6
prescribes. This is a fuse-distinct-facets agglomeration (lower risk
than fuse-near-duplicates because nothing is dropped, only combined).

```
(Record
  [intent-maintenance agglomeration composite weight provenance archive]
  Principle
  [Intent is refreshed by AGGLOMERATION: many lower-certainty records that belong together are fused into a single fresh higher-certainty composite that references the older records as source material, raising authority while shrinking how much agents must read. A composite record carries TWO measures - certainty (confidence in the statement) and weight (accumulated importance/reinforcement, especially the count of sources a composite fuses). Agglomeration is useful but dangerous, so it is GUARDED: provenance and archival recoverability are preserved before any source is removed; retired sources are archived and referenced by hash identity FROM the composite, via a streamlined composite-to-archived-source link rather than an ad-hoc dump; supersession of retired sources is always explicit. Genuinely distinct intent and active supersession chains (where a design FLIPPED) are never naively fused - only the landed state is composited and the rejected steps are retired-as-superseded, never averaged in.]
  VeryHigh
  Zero
  (AgglomeratedFrom [audg3 1zd6 6vsl 1byp 73t3] Weight 5))
```

## Clusters that look agglomerable but are DISTINCT (honesty section)

- **Naming renames (signal-persona-auth → signal-persona-origin, Id → Identifier).** Records 1xpw, 5ykr, 68863, 6iwu, 6raz cluster on `naming` and all touch the same crate rename. But several are WORKING ORDERS ([Bundle X and Y into one operator pass]) that should never have been Spirit records at all (they fail the after-the-task test). These are removal candidates, NOT agglomeration candidates — fusing them would preserve transient task directives as durable intent. The one durable rule among them ([Names that abbreviate something the thing isnt are forbidden], Spirit Correction 6raz, Maximum) stands alone.

- **Reactive-schema naming (45n8, 6v8e, 6vsl-adjacent, 4ozk).** Multiple records define "reactive schema vs base schema." They READ like duplicates but each pins a different facet (the Nix-derivation analogy, the Input/Output reaction surface, the base-is-data distinction). Fusable, but lower priority and genuinely additive — flag, don't rush.

- **Scalar-type naming (yoi3, 230k).** Two records, [String/Integer/Boolean not Bool/U64]. These ARE near-duplicates (230k is even tagged as a gap-fill of the same forwarded exchange) and SHOULD fuse — a clean small composite. Included here only to note the agglomerator should catch gap-fill pairs (one record explicitly gap-filling another is a strong fuse signal).

- **The record-shape / variant-per-kind cluster (3awz, 4gkg, 4q67).** [Record fields should vary by kind] appears twice (3awz Decision, 4gkg Principle) — genuinely fusable — but the third is a query record about catch-up, unrelated. Topic co-occurrence is NOT cluster membership; the agglomerator must read descriptions, not trust tags.

## For the Orchestrator

- **Rough corpus size.** Topic-tag occurrences number ~3000+ across ~850 distinct topics; with 3-5 tags per record the live record count is on the order of low-thousands. `Observe Topics` does not return a single total — recommend the orchestrator request a count operation or `(Observe (Records (Any None Any Any SummaryOnly)))` paged if an exact figure is needed.

- **Most bloated areas.** By NEAR-DUPLICATION density (not raw count): reporting/context-maintenance is the worst (~12+ records → 2 composites, ~80% shrink in that band); recency (5 → 1); certainty calibration (3 → 1); identifier citation (4 → 1). The big topics (`schema` 427, `nota` 150) are large but NOT necessarily duplicative — they're a deep design surface; they need a separate, careful pass before claiming agglomeration headroom there.

- **Shrink estimate.** This six-cluster slice: ~45 records → ~9 composites (~80% reduction WITHIN these clusters). Extrapolating only the genuinely-duplicative bands (recency, certainty, citation, reporting-maintenance, scalar-naming, record-shape) plausibly retires 60-90 records into ~12-15 composites. The corpus-wide figure is much smaller in percentage terms because most of the corpus is the deep schema/nota/signal design surface where records are distinct.

- **Guardrails the mechanism needs (the danger is real).**
  1. **Two relations, not one.** `AgglomeratedFrom` (sources whose substance is fused) MUST be separate from `Supersedes` (rejected intermediate steps retired without their wording bleeding in). Cluster 3 (None vs Zero floor) and Cluster 4 (fingerprint vs random hash) both FLIPPED mid-design; a similarity-only agglomerator would re-admit rejected wording.
  2. **Read descriptions, not tags.** Topic co-occurrence over-clusters (record-shape example) and under-clusters (recency record 2esr's identity clause belongs to a different cluster than its recency clause). Tags are a coarse pre-filter only.
  3. **Working-orders are removal candidates, not agglomeration candidates.** The naming-rename cluster is task directives that should be removed, not fused; fusing them would launder transient orders into durable intent.
  4. **Provenance + archive before removal** (Constraint 1byp, Principle 73t3): sources archived and hash-referenced from the composite BEFORE retirement; recoverable via the streamlined composite-to-source link.
  5. **Psyche authorization stays mandatory** and conservative — when fusability is uncertain, FLAG don't fuse; over-agglomeration is worse than under-agglomeration, exactly as over-removal is (record 728a).
  6. **Weight ≠ certainty.** A composite's certainty is the confidence of the fused statement (often raised per the ladder); its weight is the source count / reinforcement (record 6vsl). The drafts above carry both. The agglomeration op should compute weight from `AgglomeratedFrom` cardinality plus inherited weights, not conflate it with certainty.
  7. **A fat cluster may fuse to MORE than one record** (Cluster 5 → policy + mechanism). The mechanism must not assume one-cluster-one-composite.
