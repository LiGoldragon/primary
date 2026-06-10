# Migration realities and the fixture/test plan

Section 3 of the `580` meta-report — implementation guidance for the Spirit
intent-tool redesign (`578`). Where §1/§2 carry the design and substrate, this
section carries the **corpus-grounded migration plan** and a **testable fixture
plan** per operator `352` §7. Insight and plan, not code.

Read companions: `578` (the design — esp. §6 categories, §8 kinds/ops/events,
§9 auditor/agglomeration rule, §10 build sequence), `352` §7/§8 (fixture-files
rule + coverage list), `579` (first agglomeration pass + 4 contradictions),
`577` (corpus macro-stats).

## 0. What the live store actually says now (re-measured 2026-06-10)

The deploy moved *past* the snapshot `577`/`579` describe. Re-measured against
the running `spirit-daemon` (store `~/.local/state/spirit/spirit.sema`) this
session — several "to build" items from `578` §10 are **already deployed**, which
changes the migration plan materially.

| Fact | `577`/`579` said | Live now |
|---|---|---|
| Total records | 1400 / 1402 | **1411** (1404 public-Zero-privacy, 7 private) |
| Decision | 498 / 501 | **501** |
| Principle | 383 | **383** |
| Correction | 191 | **191** |
| Clarification | 200 | **201** |
| Constraint | 121 / 128 | **128** |
| `Entry` shape | 5 fields, `magnitude` overloaded | **6 fields** — `Topics Kind Description Certainty Importance Privacy` |
| Observe returns identifiers? | No (worked around via snapshot) | **Yes** — `ObservedRecord { RecordIdentifier * Entry * }` |
| Query shape | 3-position | **5-position** — `TopicMatch kind privacy_selection certainty_selection importance_selection` |
| Certainty selection | absent in deployed binary | **present** — `CertaintySelection`, `removal_candidate_certainty()` |

Three `578`/`352` keystones are **already in the deployed schema**, not pending:

1. **Identifier-bearing observation** (`352` §1, `578` §10 "real first build").
   `Observe` now returns `RecordsObserved` carrying `(identifier Entry)` pairs.
   Verified live: `(Observe (Any (Some Correction) ...))` → `LookupStash` returns
   `(09do ([...] Correction [...] High Minimum Zero))` etc. The `RecordSnapshot`
   the guardian/auditor/migration all need *exists in the contract today*. This
   removes the single largest blocker `352` named.

2. **Certainty / Importance split** (`578` §10 three axes). `Entry.magnitude` is
   already split into `Certainty` + `Importance` (both `Magnitude`), with
   `certainty_selection` / `importance_selection` on `Query` and a `V1→V2→V3`
   store upgrade path implemented in `src/production_migration.rs`
   (`SpiritStoreV1Entry`→`V2`→current). **Weight is NOT yet present** — `578`'s
   dedicated reaffirmation-count axis is still to add; `Importance` shipped
   instead, defaulted to `Minimum` on every migrated record.

3. **Candidate hidden-vs-visible** (`352` §7 case c). Already tested:
   `tests/collect_removal_candidates.rs::collect_removal_candidates_requires_zero_certainty`
   plus `CertaintySelection::removal_candidate_certainty()`. The query layer now
   *can* select on certainty — closing the `579` "marking did nothing" contract
   gap at the source level. The deployed binary honoring it is the only question.

Net: the substrate `352`'s implementation gate (items 1–2) lists as "build first"
is mostly **built**. The remaining migration work is the *content* migration
(kinds, categories) and the **Weight** axis — not the schema scaffolding.

One correction to carry forward: `579`'s headline "marking does NOT de-bloat
because the query ignores magnitude" was true of v0.4.0 but is **stale** —
`certainty_selection` now exists. Default observation still shows everything
(`default_observation_certainty()` is `Any`), so the *felt* behavior is
unchanged, but the mechanism to hide Zero-certainty candidates is now in the
contract.

## 1. Topic → category migration

### 1.1 The real topic distribution (the thing being migrated)

Measured from a full dump of all 1411 records this session:

- **1323 distinct topic strings**, mean **2.85 topics/record**.
- **Long tail is brutal: 914 of 1323 topics (69%) are singletons** (appear on
  exactly one record). 149 appear twice, 90 three times. Only ~25 topics appear
  ≥10 times. The "closed broad set" of `578` §6 is replacing a field that is 69%
  hapax.
- **Head** (the categories that almost write themselves): `schema` 389, `nota`
  157, `spirit` 154, `workspace` 92, `signal` 83, `component-shape` 58, `sema`
  51, `persona` 47, `schema-language` 43, `cloud` 39, `reports` 37, `privacy`
  37, `nexus` 37, `asschema` 33, `component-triad` 29, `naming` 27, `daemon` 25.
- **Multi-topic is the norm, not the exception:** 574 records have one topic,
  **837 have two or more**, up to one record with 11 topics. The category move
  is therefore *not* a 1:1 relabel.

### 1.2 The near-synonym problem is the migration's center of gravity

The `schema` family alone fragments into 20+ variant strings that all denote one
domain: `schema` 389, `schema-language` 43, `asschema` 33, `schema-rust-next`
12, `schema-next` 12, `assembled-schema` 10, `reactive-schema` 6, `schema-rust`
5, `nota-schema-language` 5, `schema-component` 4, `schema-types` 3,
`schema-macro` 3, `schema-emitted-types` 3, `schema-emission` 3,
`schema-type-traits` 2, `schema-node` 2, `schema-macros` 2, `schema-idiom` 2,
`schema-daemon` 2, `schema-vocabulary-economy` 1, … These are not separate
domains; they are one category (`schema`) plus *keywords* (`asschema`,
`reactive`, `emission`, `macro`). This is the canonical "narrow topic → broad
category + keyword" transform, and it is the bulk of the work: most of the
914 singletons are sub-`schema` / sub-`nota` / sub-`signal` shards.

### 1.3 Artifacts the migration needs

1. **Canonical category declarations** — the closed set, as typed data the
   daemon can validate against (a `meta-signal` catalog, since the daemon never
   parses NOTA: encode the blessed category list into binary config). Bootstrap
   target: **~20 categories** per `578` §6, drawn from the head above. The
   enlargement gate (§6) then governs additions; the bootstrap set is the only
   place the psyche hand-edits the whole list at once.

2. **An old-topic → category mapping file** — `1323` rows: `old-topic-string →
   {category, derived-keywords}`. This is the migration's irreplaceable artifact
   and **the psyche-approval surface**. It is generated by clustering (§1.4), but
   it must be a reviewable file (a `.nota` vector of mappings), not code, because
   the psyche edits and blesses it. Three columns per row:
   `(Mapping [old-topic] category [keyword keyword …])`. For `schema-rust-next`:
   `(Mapping [schema-rust-next] schema [rust next])`.

3. **The bootstrap clustering data file** — the agent's *proposal* for the ~20
   categories, presented to the psyche as the histogram-grounded clustering
   (which old topics roll into which category, with the singleton tail attached
   to its nearest head). This is the input the psyche edits per `578` §6
   ("an agent proposes the clustering from the data; the psyche edits and
   blesses"). Distinct from artifact 2: this is the *cluster definition*
   (category → its member topics), artifact 2 is the *per-record application*.

4. **The unknown-category rejection / enlargement flow** — once the set is
   closed, a propose carrying a category not in the catalog is refused with typed
   reason `unclear-category` (already an enumerated guardian reason in `578` §4),
   routed to the enlargement gate (`578` §6): the proposed category is vetted
   against the existing ones (genuinely new vs `schema` wearing a hat). Test in
   §4 case (g).

### 1.4 How a narrow topic becomes broad-category + keyword (the rule)

For each old topic string T on a record:
- If T is (or near-synonyms to) a blessed category C → category C, and if T
  carried extra specificity beyond C (e.g. `schema-rust-next` beyond `schema`),
  emit the residue as **keywords** by marking the salient terms in the record's
  description with `*asterisk emphasis*` (`578` §7) — *not* by adding a stored
  keyword field (keywords derive on the fly, no drift).
- A multi-topic record collapses its topics through the same map, then
  **dedupes** to a small category set. A record tagged `[schema nota
  delimiters asschema pipe-delimiters]` (real: `010y`) → categories `{schema,
  nota}`, keywords `*delimiters* *asschema* *pipe*`. The five topics become two
  categories plus emphasis marks.
- **Cross-domain records are real and must survive as multi-category.** 837
  records carry ≥2 topics; e.g. `0wt5 [schema signal nota]`, `15fc [schema macro
  nota]`. These map to genuinely-multiple categories — the category field stays a
  `Vec`, the migration must not force a single-category projection. The test in
  §4 case (e) covers a multi-topic record.

### 1.5 Real edge cases (from the data, not hypothetical)

- **Near-synonym variants** (§1.2) — the dominant case; the map collapses 20+
  schema-strings to one category.
- **Singleton orphans (914 of them)** — a topic on exactly one record. Most are
  sub-domain shards (attach to nearest head); a residue are genuinely novel and
  should pull their record into the nearest category with the orphan term as a
  keyword, *never* mint a new category for a hapax (that re-creates the leak
  `578` §6 is closing).
- **Domain-spanning records** (§1.4) — keep multi-category.
- **Topics that are really keywords already** — `record-deletion`,
  `schema-language` are the `578` §6 named examples of "too specific"; the map
  demotes them to keyword under `spirit`/`schema`.
- **Capture-discipline / meta topics** — `intent`, `intent-capture`,
  `intent-maintenance`, `capture-discipline` cluster into a `spirit` (or a
  dedicated `intent` / `capture-discipline`) category; this is a psyche call
  during bootstrap, not an agent guess.

## 2. Correction / Clarification kind migration

### 2.1 How big it really is

Live: **191 Corrections + 201 Clarifications = 392 records** to reclassify
(15.3% + 14.3% of the public 1404 → ~28% of the store). Both kinds disappear from
the forward set (`578` §8: kinds become Decision / Principle / Constraint only).
This is the single largest content migration and it is *mostly mechanical with a
judgment minority*.

### 2.2 Correction patterns (sampled from the real 191)

Three patterns, by frequency-of-shape in the sample:

- **(A) Already-forward "do X, not Y" — extract the X, drop the not-Y.** The
  majority. The forward content is right there; the dialogue scaffolding ("not
  that") is the only thing to strip (`578` §8/§9 rewrite rule). Real:
  - `09do` *"Beads are coordination aids, not a substitute for implementation;
    when the psyche asks an agent to implement work, the agent should work the
    bead or code path immediately unless blocked."* → Principle, drop "not a
    substitute for".
  - `20hv` *"Landed means on main. Work on a branch has no material existence …
    Agents must never …"* → Principle (a positive law), drop "never".
  - `3nqt` *"An agent must not surface a transient … error as a terminal failure
    … It retries with backoff."* → Principle: "agents retry transient errors with
    backoff." **Mechanical.**

- **(B) Names a specific prior record by id/number — supersede target, becomes
  an archived correction event, not a stored arrow.** These are pure discussion
  ("record N is negated"). Real:
  - `3jkx` *"Spirit record 2590 is negated: Spirit record identity should use a
    random/opaque hash, not a content-address fingerprint …"*
  - `3v04` *"Record 151 (DeepSeek subsumes-into-persona-pi) is superseded; the
    real intent is a workspace-native Persona LLM client library …"*
  - `6z6t` *"Record d5s2 overstates agglomeration as a certainty-raising
    mechanism …"*
  - `783n` *"Disabling local builds … was never psyche intent — it is a
    hallucinated guard …"*
  These split: the **forward residue** ("identity uses a random opaque hash";
  "Persona is a workspace-native LLM client library") becomes/merges-into a
  Decision arrow; the **"record N is negated"** half becomes a **correction
  event + archive entry** (`578` §3/§8) — it does not live as a stored record.
  Where the named target still lives, this is a genuine `supersede` op against
  it (the §4 supersede test). **Needs judgment** — locate the target, decide
  fold-vs-supersede.

- **(C) Pure meta capture-gate corrections** — about how to capture, not domain
  intent. Real: `7hrd` *"Working orders … are NOT durable intent"*; `2vp2` *"A
  psyche statement that leans toward a choice while explicitly asking for more
  information is NOT a ratification."* These are forward Principles about the
  capture discipline once the "NOT" is inverted ("durable intent excludes working
  orders"; "ratification requires an unconditional psyche choice"). **Mechanical
  after inversion**, but the inversion needs care not to lose the boundary.

### 2.3 Clarification patterns (sampled from the real 201)

- **(A) Refines an existing arrow's wording — becomes a `clarify` op against the
  live arrow (history journaled), NOT a new stored record.** Real:
  - `114j` *"When Spirit privacy is modeled as a directional privacy magnitude,
    the no-privacy value is Zero rather than None."* — sharpens `k5y3`'s privacy
    arrow. → `clarify` on the privacy Decision; prior wording journaled.
  - `3w61` *"Spirit random identifier codes should use four characters as the
    minimum …"* — sharpens the identifier arrow.
  - `7ccc` *"Medium certainty should be the normal default for routine Spirit
    captures unless …"* — sharpens the certainty-default arrow.

- **(B) "Gap-fill" / "Formalizes record N" clarifications — fold into the named
  arrow.** Real: `1rci` *"Gap-fill from forwarded designer exchange: NOTA braces
  are the native … key-value map …"*; `2f04` *"Formalizes Spirit 1395 — an
  interface is an enum at the root with MORE THAN ONE variant …"*. These are
  `clarify`/fold against the referenced arrow (`578` §4 clarify op).

- **(C) Standalone forward statements miscoded as Clarification** — many
  "clarifications" are just forward arrows that never referenced anything. Real:
  `3do3` *"all Rust production functions are methods on non-zero-sized
  data-bearing types …"*; `5myr` *"NOTA schema namespace section is a key-value
  MAP …"*. These → straight Principle/Constraint reclassification, **mechanical**,
  no event, no fold.

- **(D) Exploratory / "may / should consider / potentially" clarifications** —
  these are tentative, not settled arrows. Real: `699n` *"Spirit search **may**
  grow beyond simple filters toward weighted keyword …"*; `6gwz` *"Spirit privacy
  design **should consider** refined access categories …"*. These are *not*
  forward arrows (they state a maybe). Either retire to archive as superseded
  exploration, or, where the maybe has since become real, fold into the arrow
  that resolved it. **Needs judgment** — and overlaps the 4 contradictions below.

### 2.4 Mechanical vs judgment — the split that sizes the work

- **Mechanical (~60-70% estimated from the sample):** Correction (A)+(C) and
  Clarification (C) — invert the "not", drop the scaffolding, reclassify to
  Decision/Principle/Constraint. A migration pass over exported records can do
  this with per-record review but no target-hunting.
- **Judgment (~30-40%):** Correction (B) and Clarification (A)+(B)+(D) — these
  reference a target (by record number or by paraphrase) that must be located in
  the live set, then folded (`clarify`) or superseded (correction event +
  archive). Target-location is exactly what identifier-bearing observation (now
  deployed) + content-match retrieval (`578` §5) enable; without them this
  half is impossible.

### 2.5 What becomes an event/archive vs a rewritten forward arrow

- **Forward residue → rewritten arrow** (the X in "do X not Y", the settled
  statement in a clarification). Stored, live.
- **"Record N is negated / superseded" → correction event + archive entry**
  (`578` §3). The discussion half evaporates as a stream event; the retired
  target moves to cold archive. Never stored as a live arrow.
- **Prior wording of a clarified arrow → clarify history (journal/archive)**
  (`578` §4). Recoverable, out of the live surface.
- **Exploratory "may/consider" with no resolution → archive** as superseded
  exploration (not destroyed — `578` §3 "nothing irrecoverably lost").

### 2.6 The 4 contradictions `579` flagged — confirmed still live, do NOT auto-migrate

All four clusters are still in the store (verified by `Lookup` this session).
They are the explicit "leave for the psyche" set; an automated kind-migration
must **route them to psyche review, never silently fold**:

1. **Identifier min-length 3 vs 4** — `qtbd`/`f36y` (min-three Decisions) vs the
   deployed daemon's min-four; `tw81` (Correction) / `rh29` (Constraint) discuss
   the shortest-collision *display* rule (a related-but-distinct axis). The
   migration must not fold `qtbd`/`f36y` into a four-char arrow until the psyche
   confirms four supersedes three.
2. **Access-classification named-tiers vs Magnitude-reuse** — `0gxx`/`fp1i`/`8ll8`
   (Open/Personal/Sensitive/Sealed tiers) vs `k5y3` (Magnitude-reuse, claims to
   supersede the tiers). Deployed schema uses `Magnitude` (now split into the
   privacy axis). The named-tier records are a live supersession the psyche must
   bless before retirement.
3. **Asschema defined-first vs REMOVED** — the `bkzd`/`av1q`/… pool vs `vez8`
   (Maximum) / `fc7l` ("do not keep the Asschema compatibility projection").
   Large live supersession; the migration leaves the whole pool for a
   psyche-confirmed sweep.
4. **`@`-sigil at-binder abandoned mid-chain** — `ilaq`→`r8da`→`skz6`→`n2z3`
   built it up; `own9` (Correction, per psyche 2026-06-06) abandons the entire
   at-binder surface; `n2z3` and `s260`/`degt` are mid-migration. The chain
   records design history; route to psyche.

These four are the **acceptance test for the migration's judgment**: a correct
pass must surface them as `requires-psyche-decision`, not resolve them.

## 3. Finishing the agglomeration (`579` left 1312 topics)

### 3.1 Are "agglomerate records" and "cluster topics for categories" the same pass?

**No — two different passes, in this order, and conflating them is a trap.**

- **Pass A — category bootstrap (topic clustering).** Operates on the *1323
  distinct topic strings*, groups them into ~20 categories + keyword residue
  (§1). One-time. Produces artifacts 2 and 3 of §1.3. Does **not** read record
  bodies for dedup — it reads topic strings and the histogram. Fast, mostly
  string-clustering, psyche-blessed.
- **Pass B — record agglomeration (the `579` work).** Operates on *record
  descriptions within a category/topic*, folds restatement clusters into
  canonicals, marks sources removal-candidate. Reads bodies, requires meaning-
  clustering (paraphrases below any token-overlap threshold — `579`'s method).
  This is the auditor's recurring job; `579` did 3 topics (690 records), 1312
  topics remain.

They feed each other but run separately: **Pass A first** (so Pass B and the
guardian operate on the clean closed category field, per `352` §6 — "category
migration should precede guardian prompt work; don't bake the old recall failure
into the new gate"), then **Pass B per category**.

### 3.2 Sequencing Pass B (the remaining 1312 topics)

`579` did the three fattest (`schema`/`nota`/`spirit`, 690 records). Sequence the
rest by **leverage = redundancy density × size**, after Pass A has collapsed the
topic field so a category sweep sees the whole domain (not one topic shard):

1. **Sweep by category, not by topic** (Pass A makes this possible). The next
   targets are the heads: `workspace` 92, `signal` 83, `component-shape` 58,
   `sema` 51, `persona` 47, `cloud` 39, `nexus` 37, `privacy` 37 — but now each
   pulls in its singleton shards (e.g. `signal` sweeps the 5 `signal-*` variant
   topics together), which `579`'s topic-by-topic method missed.
2. **The 914 singletons** are largely absorbed *into* the category sweeps once
   Pass A attaches each orphan to its head — they stop being a separate 914-item
   backlog and become part of their category's Pass B.
3. **Run it as the auditor, by hand the first time** (`577` §6 / `578` §10) —
   reaffirm one canonical at `Maximum` certainty, mark sources `Zero`, exactly as
   `579`, but now `CollectRemovalCandidates` *can* select the Zero candidates
   (the §0 contract gap is closed at source). The psyche authorizes the actual
   collection.

### 3.3 The `579` finding that still bites

`579` proved marking-without-collection didn't de-bloat the deployed v0.4.0
binary. The source now has `certainty_selection`, but **default observation is
still `Any`** — so until either (a) the deployed binary defaults observation to
hide Zero-certainty, or (b) `CollectRemovalCandidates` is run, the marked
candidates stay visible. Pass B's marking is real progress only if paired with
one of those two. Recommend: make default observation hide Zero-certainty (the
`578` "live store stays pure" invariant), keep an explicit candidate-query for
auditor review (the §4 case (c) test pins exactly this).

## 4. The fixture / test plan (per `352` §7)

### 4.1 Mechanism: exported fixture files, not inline Rust strings

`352` §7 is explicit: **use exported record fixtures or schema files checked
into the repo, not inline Rust strings.** The current tests violate this — every
`Entry` is hand-built inline (`collect_removal_candidates.rs::entry(...)`,
`tests/process_boundary.rs`). And `nix_integration.rs:375` already states the
principle: *"Schema-emitted fixture constructors — never strings as state."*

**Proposed mechanism:**
- A `tests/fixtures/` directory of checked-in **`.nota` record files** (one
  record or one record-vector per file), loaded via `include_str!` (the existing
  precedent — `operator_271_closed_claims.rs` `include_str!`s the schema files)
  and decoded through the *same* NOTA→`Entry` path the CLI uses, so a fixture
  that parses is a record the daemon would accept. Fixtures are NOTA text
  (authoring/review surface), decoded to typed `Entry` at test load — never raw
  rkyv blobs the psyche can't read.
- **Provenance:** seed the fixtures from *real exported records* (e.g. the `09do`,
  `114j`, `010y` already cited here), lightly trimmed, so the test corpus mirrors
  the real corpus's shapes rather than inventing clean cases. A small
  `spirit export <identifier>` CLI subcommand (does not exist yet — an artifact
  to build) would let the migration author pull a real record to a `.nota`
  fixture file; until then, transcribe from the `Lookup` output.
- **The migration logic under test reads exported records**, exactly as the
  real one-time migration will (`578` §8: "run as a one-time migration over
  exported records"). The test and the real migration share the input format.

### 4.2 Required cases (the `352` §7 list, with real records)

For each: a named fixture file, the operation, the asserted outcome.

**(a) Old Correction → forward record + correction event/archive.**
- Fixture `correction-supersede.nota`: real `3jkx` *"Spirit record 2590 is
  negated: Spirit record identity should use a random/opaque hash, not a
  content-address fingerprint …"* plus a `target.nota` holding the
  content-address arrow it negates.
- Assert: migration emits **one forward arrow** ("record identity uses a random
  opaque hash" — Decision), **retires the target** to archive, and **fires a
  correction event** naming the retired identifier. The "is negated" text appears
  in **neither** live arrow. Pattern (B) of §2.2.

**(b) Old Clarification → clarify history or forward record.**
- Fixture `clarification-refine.nota`: real `114j` *"… the no-privacy value is
  Zero rather than None"* plus `privacy-arrow.nota` (the `k5y3` privacy Decision
  it sharpens).
- Assert: migration applies a **`clarify` op** to the privacy arrow (identifier
  stable), **journals the prior wording** to archive, fires a **clarification
  event**. No new stored record. Pattern (A) of §2.3.
- Companion fixture `clarification-standalone.nota`: real `3do3` *"all Rust
  production functions are methods on non-zero-sized data-bearing types …"* —
  asserts the no-target case reclassifies straight to **Principle**, no event,
  no fold. Pattern (C) of §2.3.

**(c) Removal-candidate hidden from default query, visible to explicit candidate
query.** *(Partially exists — extend it.)*
- Already proven for collection by
  `collect_removal_candidates_requires_zero_certainty`. The missing test is the
  **query-visibility** half: a Zero-certainty record is *absent* from
  `default_observation_certainty()` results but *present* under
  `removal_candidate_certainty()`.
- Fixture `agglomerated-cluster.nota`: a canonical at `Maximum` + 2 sources at
  `Zero` (mirror `579`'s `kvib` + `oe2s` shape).
- Assert: default Observe returns **1** (canonical only); candidate-query Observe
  returns **2** (the Zero sources); `CollectRemovalCandidates` archives exactly
  the 2 and the canonical stays live. This is the §3.3 invariant under test.

**(d) Old narrow topic → broad category + keyword.**
- Fixture `narrow-topic.nota`: real `schema-rust-next`-tagged record (e.g. a
  `[schema-rust-next lojix]` Correction like `0dmo`).
- Assert: migration maps `schema-rust-next` → category `schema`, emits keyword
  residue `*rust* *next*` as asterisk-emphasis in the description, and the record
  is findable by `category=schema` **and** by keyword `rust`. Pattern §1.4.
- Companion `nonexistent-asterisks.nota`: a record whose description literally
  contains `*emphasis*` — asserts the asterisks round-trip through NOTA
  unchanged (closes the `578` §7 deferred "confirm asterisks inert in NOTA";
  measured this session: **zero** `*...*` spans exist in the live corpus, so this
  is forward-authoring with nothing to migrate but everything to validate).

**(e) Duplicate proposal refused + weight bump.**
- Fixture `duplicate-pair.nota`: an existing arrow + a near-restatement propose
  (mirror `579`'s `kvib`/`oe2s` multi-topic-query pair).
- Assert: the propose is **refused** with typed reason `duplicate` naming the
  existing arrow, **and** the existing arrow's **Weight increments by one**
  (`578` §10 weight mechanics). **This test cannot pass yet — Weight is not in
  the deployed schema** (§0); it pins the contract for when Weight lands. Mark it
  `#[ignore]` with a comment until the Weight axis is added, or it is the failing
  test that drives that work.

### 4.3 Additional cases the real data demands

**(f) Clarify-tramples rejection** (`578` §4, typed reason `clarify-tramples`).
- Fixture `clarify-trample.nota`: an arrow + a "clarify" that actually changes
  its meaning (e.g. clarify the privacy arrow into a statement about *certainty*
  — different axis).
- Assert: guardian **rejects** with `clarify-tramples`; the agent wanted a
  supersede. Mirror with `clarify-loses-meaning` (a clarify that drops a clause).

**(g) Unknown-category rejection / enlargement.** (§1.3 artifact 4.)
- Fixture `unknown-category.nota`: a propose carrying a category not in the
  blessed catalog.
- Assert: refused with typed reason `unclear-category`, routed to enlargement.
  Companion: a genuinely-new category passes the enlargement gate; a `schema`-
  wearing-a-hat is refused as a hat. Real seed: the `schema-vocabulary-economy`
  singleton (a hat for `schema`) vs a real new domain.

**(h) Supersede-target-missing** (`578` §4, typed reason
`supersede-target-missing`).
- Fixture `supersede-ghost.nota`: a supersede naming an identifier not in the
  store (real shape: `3jkx`'s "record 2590" — that numeric reference may not
  resolve to any live identifier).
- Assert: refused with `supersede-target-missing`. This is the **direct test of
  the §2.6 migration hazard** — a Correction naming a long-gone record must fail
  loud, not silently fold.

**(i) Multi-topic / cross-domain record survives as multi-category.** (§1.4.)
- Fixture `cross-domain.nota`: real `0wt5 [schema signal nota]` or `010y [schema
  nota delimiters asschema pipe-delimiters]`.
- Assert: migration yields **multiple categories** (`{schema, signal, nota}`),
  not a forced single, with the over-specific topics demoted to keywords. Guards
  against a migration that flattens the 837 multi-topic records.

**(j) The 4 contradictions route to psyche, not auto-fold.** (§2.6.)
- Fixture `contradiction-pair.nota`: real `qtbd` (min-three) + `rh29` (min-four).
- Assert: the migration classifies this as `requires-psyche-decision` and does
  **not** fold either into the other. The acceptance test for migration judgment.

### 4.4 Coverage summary

| Case | Real seed | New / extends | Pins which `578`/`352` decision |
|---|---|---|---|
| (a) Correction→arrow+event | `3jkx` | new | §8 kind migration, §3 events |
| (b) Clarification→clarify/forward | `114j`, `3do3` | new | §4 clarify op, §8 |
| (c) candidate hidden/visible | `579` shapes | extends existing | §3 state purity, §10 certainty query |
| (d) narrow topic→category+keyword | `0dmo` | new | §6 categories, §7 keywords |
| (e) duplicate refused + weight | `kvib`/`oe2s` | new (blocked on Weight) | §10 weight mechanics |
| (f) clarify-tramples | synthetic on real arrow | new | §4 typed reasons |
| (g) unknown-category/enlargement | `schema-vocabulary-economy` | new | §6 enlargement gate |
| (h) supersede-target-missing | `3jkx` "record 2590" | new | §4 typed reasons |
| (i) multi-topic→multi-category | `0wt5`, `010y` | new | §6 categories (Vec) |
| (j) contradictions→psyche | `qtbd`/`rh29` | new | §9 auditor, §2.6 |

## 5. Issues, constraints, and risks

- **The deploy is live and ahead of the reports.** The store is at 1411 records
  with the V3 schema (Certainty/Importance split) already deployed; `577`/`579`
  describe v0.4.0. Any migration plan written against the `577`/`579` schema is
  partly obsolete. **Re-measure before building** — do not trust the 5-field
  `Entry` or "Observe lacks identifiers" claims; both are stale (§0).

- **Data-loss / irreversibility.** The forward-content-extraction migration
  (§2) is **lossy by design** — it drops the "not Y" discussion half. That is
  intended (`578` §8/§9), but the dropped half must land in the **archive**, not
  the void (`578` §3 "nothing irrecoverably lost"). The migration must archive
  every Correction/Clarification *before* rewriting, so the dialogue scaffolding
  is recoverable. `CollectRemovalCandidates` already archives-then-retracts —
  reuse that path; do **not** use `Remove` (hard, irreversible) anywhere in the
  migration.

- **The 4 contradictions are irreversibility landmines.** §2.6 — auto-folding
  `qtbd` into a four-char arrow, or any Asschema/at-binder record, destroys the
  lineage that *is* the open question. The migration must hard-route these to
  psyche; case (j) tests exactly this.

- **Weight is not built; case (e) is blocked.** The reaffirmation-count axis
  (`578` §10) shipped as `Importance` instead (defaulted `Minimum`). The
  duplicate-refusal-bumps-weight mechanic has no field to bump. Either add Weight
  before the guardian, or the guardian's duplicate path is incomplete. Flag for
  the operator: **is `Importance` meant to be the Weight axis, or is Weight still
  to be added?** `578` §10 says no Importance axis "unless explicitly wanted" —
  yet it's deployed. This is a divergence between design and deploy worth a
  psyche confirmation.

- **Default-observation visibility.** Marking candidates `Zero` still doesn't
  hide them from default queries (default certainty selection is `Any`) — the
  `579` finding survives at the behavior level even though the *mechanism* now
  exists. Pass B's value depends on closing this (§3.3).

- **Category bootstrap is psyche-gated and blocks the guardian.** `352` §6: the
  guardian must not run on free-text topics or it bakes in the old recall
  failure. So Pass A (category bootstrap) + psyche blessing is on the critical
  path before guardian prompt work — it cannot be deferred or parallelized past
  the guardian.

- **Migration order, net.** (1) Re-confirm deployed schema (§0). (2) Pass A
  category bootstrap → psyche-blessed catalog + mapping file. (3) Kind migration
  over exported+archived records (§2), routing the 4 contradictions to psyche.
  (4) Pass B record agglomeration per category. (5) Add Weight, then guardian.
  Each step archives before it rewrites; nothing uses `Remove`.
