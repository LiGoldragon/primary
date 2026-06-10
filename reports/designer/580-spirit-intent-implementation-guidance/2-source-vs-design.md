# Spirit source vs. the settled design — concrete gap-to-next-step map

Section 2 of the `580` meta-report. Read-only sweep of the live
`/git/github.com/LiGoldragon/spirit` source against `578` (the settled design)
and `352` (the operator's build order). Every type below is quoted from current
source with `file:line`. The daemon was down at sweep time (deploy in progress),
so source is the sole evidence; no live queries were run.

The headline finding inverts a `578`/`352` assumption: **source already has a
dedicated second magnitude axis — but it is named `importance`, not `weight`,
and it carries `weight`'s old place in the schema.** The git history is explicit:
`28438ae spirit: split certainty and weight`, then `73cb457 spirit: rename
weight to importance` (HEAD). So the field `352` asked for *exists and works*;
it simply went out under the name the design said to add *only if the psyche
explicitly wants an intrinsic-priority axis*. That naming collision is the single
most important thing the operator must resolve before touching the schema again
(§4).

## 1. Current `Entry` and the signal contract

### Entry — six fields, was five

`src/schema/signal.rs:707`:

```rust
pub struct Entry {
    pub topics: Topics,        // Vec<Topic>, Topic(String) — still free-text, still plural
    pub kind: Kind,            // Decision | Principle | Correction | Clarification | Constraint
    pub description: Description,
    pub certainty: Certainty,  // Certainty(Magnitude) — the renamed v0.4.0 `magnitude`
    pub importance: Importance,// Importance(Magnitude) — NEW field (was briefly `weight`)
    pub privacy: Privacy,      // Privacy(Magnitude)
}
```

Against `577`'s deployed five (`topics, kind, description, magnitude, privacy`):
`magnitude` → `certainty`, and `importance` is added. **Still absent: no
timestamp, no `weight`-named field, no relations, no derived keywords.** All
three magnitude-valued axes share one 8-step enum, `Magnitude { Zero, Minimum,
VeryLow, Low, Medium, High, VeryHigh, Maximum }` (`signal.rs:816`), with
`Magnitude::rank()` 0..7 (`store.rs:779`).

`StoredRecord` (`store.rs:60`) is `{ record_identifier: String, entry: Entry }`
— the identifier lives *beside* the entry in storage but is not part of `Entry`,
which is why observation can return it (see below) yet the design still wants a
named snapshot type.

### Query / selection types

`Query` (`signal.rs:766`) now has five fields — three magnitude selectors:

```rust
pub struct Query {
    pub topic_match: TopicMatch,
    pub kind: Option<Kind>,
    pub privacy_selection: PrivacySelection,
    pub certainty_selection: CertaintySelection,
    pub importance_selection: ImportanceSelection,   // NEW, parallel to the others
}
```

- `TopicMatch` (`signal.rs:446`): `Any | Partial(Topics) | Full(Topics)`. Matching
  is still exact-string set membership — `Partial` = any topic intersects,
  `Full` = all query topics present (`engine.rs:544`). Not substring, not text.
- `CertaintySelection` (`signal.rs:505`): `Any | ExactCertainty | AtMostCertainty
  | AtLeastCertainty`. Two named defaults in `store.rs`:
  `default_observation_certainty()` = `AtLeast(Minimum)` (`store.rs:736`) — this
  is the line that **hides Zero-certainty records from ordinary observation** —
  and `removal_candidate_certainty()` = `Exact(Zero)` (`store.rs:740`).
- `ImportanceSelection` (`signal.rs:530`): same four-arm shape;
  `default_observation_importance()` = `Any` (`store.rs:760`) — so importance
  never filters by default, it only *ranks* (see ordering below).
- `RecordSelection` (`signal.rs:758`, used by `PublicRecords`/`PrivateRecords`)
  is still just `{ topic_match, kind }`; it widens to a full `Query` via
  `into_public_query` / `into_private_query` (`engine.rs:496`), which inject the
  default certainty/importance/privacy selectors.

### Operations (signal tree)

Input root (`signal.rs:830`), 16 ops, unchanged in *shape* from `577` plus the
already-landed `SubscribeIntent`/`Version`:

```
State Record Observe PublicRecords PrivateRecords Lookup Count Remove
ChangeCertainty ChangeRecord LookupStash CollectRemovalCandidates
Tap Untap SubscribeIntent Version
```

Mutation/observation ops as they stand:

- `Record(Entry)` → mints a base36 identifier, asserts. (`store.rs:384`)
- `Observe(Query)` → filter + **sort by importance**, stash, returns
  `RecordsStashed { handle, count }`. (`store.rs:390`)
- `Lookup(RecordIdentifier)` → `RecordFound { record_identifier, entry, marker }`.
- `Count(Query)` → `observe(query).len()` (still no cap). (`store.rs:413`)
- `ChangeCertainty(CertaintyChange { record_identifier, certainty })` → in-place
  certainty set; the removal-candidate marker. (`store.rs:428`)
- `ChangeRecord(RecordChange { record_identifier, entry })` → wholesale replace
  the entry under a stable identifier. (`store.rs:449`)
- `CollectRemovalCandidates(RemovalCandidateCollection(Query))` → archive matches
  to a separate `*.sema`, then retract. (`store.rs:320`)
- `Tap`/`Untap` (observer taps), `SubscribeIntent(Query)` (intent stream),
  `Version`.

Output root (`signal.rs:852`) mirrors these plus `Event(IntentEvent)`, `Error`,
`Rejected`.

### Events

`IntentEvent` has **exactly one variant**, `IntentRecorded { Entry, SemaReceipt }`
(`signal.schema:71-72`, `signal.rs:384`). The stream is `IntentEventStream`
(`signal.schema:73`). No `Clarified`, `Superseded`, or `Corrected` event exists.

## 2. Substrate present vs. missing — mapped to `352`'s gate

`352`'s gate, in order: (1) identifier-bearing `RecordSnapshot` observations →
(2) Certainty/Weight vocab → (3) category catalog + migration → (4) durable
operation journal/archive → (5) `signal-agent` lease contract + harness registry
→ (6) endpoint auth + lease accounting → (7) guardian verdict integration.

| Gate step | State in source | Evidence |
|---|---|---|
| 1. Identifier-bearing observation | **Partial.** `ObservedRecord { record_identifier, entry }` (`signal.rs:305`) — observation results *do* now name the record. But there is no named `RecordSnapshot` type; the carrier is `ObservedRecord`, and `PublicRecords`/`PrivateRecords`/the agglomeration path all flow through it. The `577`/`352` complaint ("Observe returns Entry without identifier") is **already fixed** in substance. | `store.rs:544` `into_observed_record` |
| 2a. Certainty rename | **Done.** `magnitude` → `Certainty`; queries filter on it; Zero hidden by default; `CollectRemovalCandidates` collects on Exact(Zero). | `store.rs:735-757`, `collect_removal_candidates.rs:216` |
| 2b. Dedicated weight field | **Present but misnamed + semantically wrong.** The second axis exists as `Importance` (intrinsic priority, default `Any`, ranks results) — NOT as `Weight` (reaffirmation count, monotonic-under-capture, bumped on duplicate-refusal). There is **no** typed weight-update op and **no** duplicate-bump mechanic. | `signal.rs:475,530`; `store.rs:396,703` |
| 3. Category vs. topic | **Absent.** Still `Topic(String)` / `Topics(Vec<Topic>)`, free-text, exact-match. No closed `Category` type, no enlargement gate, no catalog. | `signal.rs:203,208`; `engine.rs:544` |
| 4. Durable journal/archive | **Half-present.** A removal *archive* exists — `ArchiveDatabase`, a separate `*.sema` opened on demand (`store.rs:660`). A `MailLedger` of Sent/Processed events exists in-engine (`engine.rs:79`). But there is **no operation history journal**, no clarify-prior-wording archive, no lease accounting journal. | `store.rs:320-369`; `engine.rs:366` |
| 5. signal-agent lease + harness registry | **Absent entirely.** No `signal-agent`, `harness`, `lease`, `HarnessLease`, `guardian` anywhere in `src/` or `schema/`. | grep: 0 hits |
| 6. Endpoint auth + lease accounting | **Absent.** Same. | grep: 0 hits |
| 7. Guardian verdict integration | **Absent.** No verdict type, no typed-reason enum, no propose/clarify/supersede ops. The only write gate is `Entry::validate` (empty-topic / empty-description, `engine.rs:452`) and `Input::validate`. | `engine.rs:420-465` |

### The magnitude→certainty rename's effect on queries and removal

The rename is clean and complete. `CertaintySelection::matches` (`store.rs:744`),
the default-hides-Zero rule (`store.rs:736`), and
`removal_candidate_certainty()` = Exact(Zero) (`store.rs:740`) all work as `578`
§10 wants. `CollectRemovalCandidates` archives-then-retracts (`store.rs:320`),
matching `578` §4 "archived, not destroyed." The `process_boundary` test proves
the end-to-end de-bloat path: change a record's certainty to Zero, it vanishes
from ordinary `Observe`, stays visible to an explicit `(ExactCertainty Zero)`
query (`process_boundary.rs:531-576`). **The keystone de-bloat capability `577`
called "decided but unbuilt" is now built in source** — it ships the moment the
deploy lands.

### Storage versioning

`SPIRIT_SCHEMA_VERSION = 3` (`store.rs:35`). The migration code carries the full
ladder: `SpiritStoreV1Entry { …, magnitude, privacy }` →
`SpiritStoreV2Entry { …, certainty, importance, privacy }`
(`production_migration.rs:104-127`), and both upgrade into the current `Entry`
(`production_migration.rs:420-444`). So the `magnitude→certainty+importance`
store transition is already a written, tested migration — V1 records get
`certainty = old magnitude`, `importance = Minimum`.

## 3. Smallest next steps, grounded in the real code

The abstract `352` order front-loads two steps that source already satisfies
(snapshots in substance; certainty rename). The genuinely-first *unbuilt* slices:

1. **Resolve the `importance`/`weight` naming and decide the axis count (blocks
   all schema work).** This is not code first — it is a psyche question (§4). The
   field exists; what it *means* and what it's *called* is unsettled against the
   design. Until that resolves, every guardian/auditor ranking decision is built
   on an axis whose semantics are ambiguous. Cheapest concrete slice once
   resolved: if the psyche wants `578`'s split, rename `Importance`→`Weight`
   throughout (pure rename, the migration ladder already has a slot) and add the
   duplicate-bump + typed `BumpWeight` op; if the psyche wants intrinsic
   priority, keep `Importance` and add `Weight` as a *third* axis.

2. **A named `RecordSnapshot { RecordIdentifier, Entry }` and route agent-facing
   reads through it.** `ObservedRecord` already carries both fields, so this is a
   rename/alias + making `PublicRecords`/the guardian-bundle path return it
   explicitly. Small, and it gives the guardian/auditor a stable name to refer to
   records by — the thing `352` §1 wanted. (Marginal, since the data is already
   there; do it when the guardian needs a typed bundle, not before.)

3. **Category type + the one-time topic→category migration (the real schema
   bite).** This is the first *substantial* unbuilt slice. Introduce a closed
   `Category` enum (or a curated catalog), add a `category_match` to `Query`
   parallel to `topic_match`, and write the agglomeration migration that folds
   1315 free-text topics into ~20 categories (`578` §6, `579`'s data). `352` §6
   is explicit that this must precede any guardian retrieval, or the old
   exact-match recall failure gets baked into the new gate. The migration ladder
   in `production_migration.rs` is where the topic→category fold lands.

4. **Derived-keyword + full-text retrieval over the description** (`578` §7).
   No stored field — derive on the fly from `*emphasis*` spans, case-fold,
   substring. This is the discriminator the guardian bundle needs under the
   broad category filter. Implementable as a method on `Entry`/`Description`
   independent of the daemon wire, so it can land and be unit-tested early.

5. Only then the agent-side substrate (lease contract, harness registry,
   endpoint auth) and the guardian verdict integration — none of which has any
   source footing yet, exactly as `352`'s "do not start with prompts" warns.

Steps 1, 3, 4 are the load-bearing near-term work. Steps 2 is nearly free.

## 4. Source ↔ design divergences

### A. `importance` was added; `578` says don't add `Importance`, add `Weight`

This is the central divergence and it is a real semantic conflict, not a label
nit. `578` §10 / `352` §1 specify two axes — **Certainty** (currentness) and
**Weight** (reaffirmation count: monotonic under capture, bumped on
duplicate-refusal, adjustable only by the auditor, never via `ChangeRecord`) —
and explicitly say **Importance is NOT added unless the psyche explicitly wants
an intrinsic-priority field**. Source did the opposite: it added `Importance`
(`signal.rs:475`), gave it intrinsic-priority semantics (default `Any`, set at
capture, ranks observation via `importance_rank()` at `store.rs:396,703`), and
named no `Weight` at all. The git trail shows this was deliberate — `weight` was
the working name, renamed to `importance` at HEAD.

What this means for the operator:

- **The ranking direction matches the design's *Weight* role but the field's
  *semantics* match *Importance*.** `store.rs:396` sorts observation by
  `importance_rank()` descending — i.e. the most-important records surface first.
  `578` §10 wanted "within a category, Certainty + Weight order the results."
  Source orders by importance alone, ignores certainty in the sort, and has no
  weight. So the *ranking hook exists* but is wired to the wrong axis and is
  single-axis.
- **None of `578`'s Weight *mechanics* exist:** no duplicate-detection bump, no
  monotonic-under-capture rule, no typed weight-update op (the design forbids
  doing it via `ChangeRecord`, yet `ChangeRecord` is the only entry-mutating op
  in source). Whatever the axis ends up called, these mechanics are net-new.
- **Decision needed from the psyche** (this is a Spirit-gate question for the
  dispatching designer, not something to infer): does the psyche want (a)
  `578`'s two-axis model — then `Importance` should be *renamed* to `Weight` and
  given reaffirmation semantics; or (b) a genuine three-axis model —
  Certainty + Weight + Importance — then `Importance` stays and `Weight` is added
  beside it; or (c) intrinsic-priority `Importance` *instead of* Weight — then
  `578` §10 must be amended and the guardian's duplicate-bump reweighting
  retargeted or dropped. The source currently encodes (c) by default.

### B. `578` describes parts the rename already touched, in the old vocabulary

- `578` §10 and §11 still say "Certainty (renamed `magnitude`) + dedicated
  **Weight**." Source renamed `magnitude`→`certainty` (correct) but the second
  axis is `importance` (divergent). Any `578` sentence naming `Weight` as the
  ranking force should be read against `Importance` in source until A is resolved.
- `578` §1 / `577` say "`Entry` is 5 fields (… magnitude …)." Stale: it is now 6
  (`certainty`, `importance`). Expected — `578` flags itself as describing
  deployed v0.4.0 — but the operator should not treat the 5-field shape as
  current.
- `577`/`352` §1: "`Observe` returns `Entry` without `RecordIdentifier`." Stale:
  `ObservedRecord` (`signal.rs:305`) carries the identifier today. The
  `RecordSnapshot` step is now a naming/typing nicety, not a data-recovery fix.

### C. Ops/types the design assumes that don't exist yet

- **propose / clarify / supersede** (`578` §4): none exist. The only writes are
  `Record` (≈ blind propose, no consistency check), `ChangeRecord` (wholesale
  replace — would serve clarify *and* supersede *and* trample indiscriminately,
  with no guardian judging which), `ChangeCertainty`, `Remove`,
  `CollectRemovalCandidates`. The design's three-way write split is unbuilt.
- **Typed verdict + reason enum** (`578` §4): absent. Refusals today are
  `ValidationError { EmptyTopic, EmptyDescription, EmptyQueryTopic,
  StashHandleNotFound }` (`signal.rs:400`) — structural validation only, no
  duplicate/contradiction/compound/non-intent reasons.
- **Clarified / Superseded / Corrected events** (`578` §3, §8): absent.
  `IntentEvent` has only `IntentRecorded` (`signal.rs:384`). Subscriptions exist
  (`SubscribeIntent`, the stream, the tap registry) but emit only the
  record-added event, so the "change announces itself then evaporates" stream
  model is one-third built.
- **Kinds still include `Correction` and `Clarification`** (`signal.rs:796`) —
  `578` §8 retires both (Correction→event, Clarification→operation), leaving
  Decision/Principle/Constraint. Source has not begun that migration; the
  kind-fold rewrite (`578` §8, `352` §7 fixtures) is unstarted.
- **Category, keywords, enlargement gate, lease/harness/guardian/auditor**: all
  absent, as in §2.

## Net

Source is meaningfully *ahead* of where `577`/`352` thought it was on two gate
steps (identifier-bearing reads; the certainty rename + Zero-hiding + removal
collection — the whole de-bloat keystone is built and tested, waiting only on
deploy). It is *off-design* on the second magnitude axis: the field exists and
ranks results, but it is `importance` with intrinsic-priority semantics, not
`weight` with reaffirmation semantics, and none of `578`'s weight mechanics
(duplicate-bump, typed update op, certainty+weight co-ranking) are present.
Everything from category onward — category catalog, keyword/full-text retrieval,
the three-way write split, typed verdicts, change events, the kind fold, and the
entire agent/lease/guardian/auditor stack — is greenfield. The first real
decision is the psyche call on the axis (§4.A); the first real *code* is the
topic→category migration and the keyword/full-text discriminator.
