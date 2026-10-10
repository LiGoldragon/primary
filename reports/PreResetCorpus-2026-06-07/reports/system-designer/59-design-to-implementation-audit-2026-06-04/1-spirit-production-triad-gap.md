# Spirit production triad: design-to-implementation gap (slice A1)

Audit of the five Spirit-engine designs (1543/1547, 1544/1548, 1549,
1550, 1474) against the deployed triad source on 2026-06-04. Read-only.
Every line number below was verified against current source before
citation.

## Intent Anchors

[Production Spirit implements an explicit collect-removal-candidates
operation that archives or emits reviewed Zero-certainty records before
retracting them from the hot store] (Spirit 1543 Maximum)

[Spirit gains an explicit CollectRemovalCandidates operation as a Signal
root collecting all Zero-certainty records and emitting their summary
form to a configurable output target; separates discovery/extraction from
the destruction concern in Remove] (Spirit 1547 High)

[Removal-candidate collection supports an explicit output target for
archive material (file path or process stream) so another component can
preserve the compact valued representation before hot-store removal]
(Spirit 1544 High)

[Operations that extract or emit content accept a customizable
output-target enum as the final field; variants Stdout, Stderr,
File(path); not an error channel; uniform across extraction operations]
(Spirit 1548 High)

[Spirit defines a small-record data type carrying core load-bearing
fields — identifier, topics, kind, description summary, magnitude,
daemon-stamped date and time — read by the variant-ladder short-form and
emitted by CollectRemovalCandidates] (Spirit 1549 High)

[Spirit gains a RecordDefault short-form recording operation taking only
fields agents commonly customize — topics, kind, description, magnitude —
with defaults injected for the rest; Record remains the canonical
full-fidelity operation] (Spirit 1550 High)

[Spirit operations should support a simpler-to-more-complex variant
ladder — short forms with summary defaults for normal operations,
complex forms with full metadata for custom operations] (Spirit 1474
High)

## Method note — which schema file is the wire contract

`signal-persona-spirit/src/lib.rs:1166` ends with `signal_channel!([schema]);`.
The `[schema]` marker makes the proc-macro read a schema file by
package-derived stem
(`signal-frame/macros/src/schema_reader.rs:36-45`): package
`signal-persona-spirit` strips to stem `spirit`, so the macro consumes
`signal-persona-spirit/spirit.schema`. That file IS the authoritative
operation/reply tree. The macro then emits the `Operation`, `Reply`,
`Event` enums plus all named types, and additionally injects the
mandatory observability verbs `Tap(ObserverFilter)` /
`Untap(ObserverSubscriptionToken)` (confirmed by the repo's own
ARCHITECTURE.md:47-53 and INTENT.md:114-115). The generated `Operation`
enum is therefore the 8 schema roots (`spirit.schema:6-15`) plus the 2
macro-injected verbs = 10 variants, which is exactly what
`persona-spirit/src/observation.rs:58-86` matches on. The contract is
internally consistent and compiles.

Honesty-about-state caveat for future auditors: the file
`signal-persona-spirit/schema/signal-persona-spirit.concept.schema` is a
STALE dead artifact. Its operation tree lists only
`State/Record/Observe/Watch/Unwatch` — no `Remove`, `ChangeCertainty`, or
`CollectRemovalCandidates`, and its `Entry` shape predates the
privacy-magnitude field. It is NOT consumed by the build (the
package-stem resolver picks `spirit.schema` first, and that file exists
so the `schema.nota` fallback never fires). Do not read `.concept.schema`
as the contract. This stale file is itself a bad pattern (logged below).

## (1) CollectRemovalCandidates operation (1543 / 1547) — IMPLEMENTED, Reading B; A-vs-B is psyche-only

The operation has fully landed end-to-end. It is a real Signal operation
root in the consumed schema:

```
(CollectRemovalCandidates (RemovalCandidateCollection))
```
(`signal-persona-spirit/spirit.schema:14`), with the matching reply
`RemovalCandidatesCollected` in the Reply tree
(`spirit.schema:115`).

The daemon handler lives in `persona-spirit/src/store.rs:127-160`:

```rust
    pub fn collect_removal_candidates(
        &self,
        collection: RemovalCandidateCollection,
    ) -> Result<RemovalCandidatesCollected> {
        CollectionQueryGuard::new(&collection).validate()?;
        let candidates = self.records_for_query(&collection.record_query)?;
        let archive = RemovalCandidateArchive::from_stored_records(&candidates);
        if archive.write_to_target(&collection.archive_target).is_err() {
            return Ok(RemovalCandidatesCollected::new(
                Vec::new(),
                Vec::new(),
                candidates
                    .iter()
                    .map(|record| SkippedRemovalCandidate {
                        identifier: record.identifier,
                        reason: RemovalCandidateSkipReason::ArchiveFailed,
                    })
                    .collect(),
            ));
        }
        for record in &candidates {
            self.engine
                .retract(Retraction::new(
                    self.records,
                    StoredRecord::key(record.identifier),
                ))
                .map_err(Error::spirit_store)?;
        }
        Ok(RemovalCandidatesCollected::new(
            archive.records(),
            candidates.iter().map(|record| record.identifier).collect(),
            Vec::new(),
        ))
    }
```

This is unambiguously the **COMBINED archive-then-retract shape
(Reading B)**, not pure-extract (Reading A): one operation (1) queries
candidates, (2) archives them via `write_to_target`, (3) on archive
failure returns every candidate as skipped WITHOUT retracting (the
archive-first safety invariant), and (4) on archive success retracts each
candidate from the engine. Extraction and destruction are fused.

The arm is wired through the full actor chain:
`persona-spirit/src/actors/dispatch.rs:243-245` (command arm),
`dispatch.rs:329-339` (ask to the store actor),
`persona-spirit/src/actors/store.rs:263-271` (`Message<CollectRemovalCandidates>`
impl), and `persona-spirit/src/observation.rs:24,62-64,149,170`
(Command/Effect projection, Sema labels Retract→Retracted). It is proven
by the inline witness
`spirit_store_collects_only_exact_zero_candidates_before_removing_them`
(`store.rs:944-1040`): four records at certainties Zero/Minimum/High/Zero,
collect leaves the Minimum and High records and removes ids 1 and 4 — the
combined behavior verified directly. Two more witnesses guard the
invariants: `spirit_store_rejects_non_zero_collection_query_without_retracting`
(`store.rs:1042`) and `spirit_store_archive_file_failure_preserves_candidates`
(`store.rs:1090`).

The `RemovalCandidatesCollected` reply carries three vectors —
`archived_records: Vec<RecordSummary>`, `removed_identifiers:
Vec<RecordIdentifier>`, `skipped_candidates: Vec<SkippedRemovalCandidate>`
(`signal-persona-spirit/src/lib.rs:891-896`) — a richer receipt than the
design text spelled out.

**Portability: BLOCKED — Reading A vs Reading B is a psyche-only
decision.** The intent thread is genuinely ambiguous on whether
"collecting ... before retracting" (1543) means a single fused operation
(B) or a strict pure-extraction op whose destruction stays in `Remove`
(A). 1547's own words "separates discovery/extraction FROM the
destruction concern in Remove" reads toward A; the deployed code and all
three context reports land on B. Designer 57, designer 58 §"The pivotal
decision", and operator 189/190 all explicitly frame this as the
single most-important psyche decision and converge on B as the
recommendation (triple cross-lane convergence,
`reports/system-designer/57-.../3-overview.md:130-149`;
`reports/system-operator/190-...:104-114`). An auditor MUST NOT port
either direction. The precise decision the psyche owes: *"Is
CollectRemovalCandidates a single combined archive-then-retract operation
(keep the deployed handler, rename to the directed wire name), or a pure
extraction operation that emits candidates and leaves destruction to a
separate Remove call (strip the four retract lines and the
archive-failure-skip branch)?"* Everything downstream — the op name, the
reply shape, whether `skipped_candidates` survives — hangs on this.

## (2) OutputTarget enum (1544 / 1548) — PARTIAL; per-op, missing Stdout/Stderr, not generalized

There is no shared `OutputTarget` enum. The collect op carries a
purpose-named, two-variant `ArchiveTarget`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaEnum, Debug, Clone, PartialEq, Eq)]
pub enum ArchiveTarget {
    Inline,
    File(ArchivePath),
}

impl ArchiveTarget {
    pub fn file(path: impl Into<String>) -> Self {
        Self::File(ArchivePath::new(path))
    }
}
```
(`signal-persona-spirit/src/lib.rs:802-812`). The constructors the brief
asked about are on `RemovalCandidateCollection`, not on a target enum:

```rust
    pub fn inline() -> Self {
        Self::new(
            RecordQuery::removal_candidates(ObservationMode::SummaryOnly),
            ArchiveTarget::Inline,
        )
    }

    pub fn file(path: impl Into<String>) -> Self {
        Self::new(
            RecordQuery::removal_candidates(ObservationMode::SummaryOnly),
            ArchiveTarget::file(path),
        )
    }
```
(`lib.rs:828-840`).

Three gaps against design 1548:

1. **No `Stdout` / `Stderr` variants.** Design 1548 mandates exactly
   `Stdout | Stderr | File(path)`. The deployed enum is `Inline |
   File(path)`. `Inline` is NOT a process stream — `write_to_target`
   treats it as a no-op
   (`store.rs:401-406`: `ArchiveTarget::Inline => Ok(())`) and the
   archive material instead rides back in the reply's `archived_records`
   field. The design's "process stream" target (1544: "file path or
   process stream") does not exist.
2. **The name is `ArchiveTarget`, not `OutputTarget`.** Design 1548 names
   a uniform `OutputTarget`; the design's framing ("uniform across
   extraction operations", "not an error channel") is in tension with the
   current archive-flavored name.
3. **Not generalized.** The target appears only on
   `RemovalCandidateCollection` (`lib.rs:814-818`). No other extraction
   op (the record observations) carries it; 1548's "keeps the wire
   interface uniform across extraction operations" is unmet — it is one
   ad-hoc field on one op.

Secondary observation: the File archive does not emit the
`RemovalCandidatesCollected` shape but rather re-encodes
`RecordsObserved(Vec<RecordSummary>)`
(`store.rs:408-420`), so the on-disk archive format differs from the
inline reply payload.

**Portability: BLOCKED — three open psyche parameters.** (a) Does
`Stderr` belong as an output target at all, given 1548 says "not an error
channel" yet lists `Stderr` as a variant? (b) Does `Inline` survive
alongside `Stdout` (they overlap — inline-in-reply vs. write-to-stdout
are two different delivery mechanisms), or does `Stdout` replace
`Inline`? (c) Should the rename to `OutputTarget` plus generalization
onto the record-observation ops happen now, and if so which ops count as
"extraction operations"? None of these is field-level settled. A
mechanical port that just adds `Stdout`/`Stderr` to `ArchiveTarget` would
guess at (a) and (b).

## (3) SmallRecord data type (1549) — MISSING as a distinct type; field set carries an open parameter

There is no `SmallRecord` type. Two adjacent types exist:

```rust
pub struct RecordSummary {
    pub identifier: RecordIdentifier,
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Certainty,
    pub privacy: Privacy,
}
```
(`signal-persona-spirit/src/lib.rs:856-864`) — has identifier, topics,
kind, description, certainty, privacy, but **NO date/time**.

```rust
pub struct RecordProvenance {
    pub summary: RecordSummary,
    pub date: Date,
    pub time: Time,
}
```
(`lib.rs:866-871`) — wraps a summary AND adds date+time AND (transitively)
privacy.

Design 1549 specifies "identifier, topics, kind, description summary,
**magnitude**, daemon-stamped date and time." Neither deployed type
matches: `RecordSummary` lacks the date/time, `RecordProvenance` has
date/time but bundles `privacy` (a field the designer-57 analysis
explicitly reads OUT of the small record — see
`reports/system-designer/57-.../2-designer-psyche-analysis.md:595-597`:
the small record is "RecordSummary PLUS date and time but NOT the privacy
field"). The word "magnitude" in 1549 is itself ambiguous — Spirit has
TWO magnitudes (certainty and privacy, both `= Magnitude`,
`lib.rs:375-376`), so "magnitude" could mean certainty-only,
privacy-only, or both.

**Portability: BLOCKED — the field list is not field-level decided.** The
open parameter is exactly: *does SmallRecord carry privacy, or only
certainty (which "magnitude")?* The intent text says "magnitude"
singular; the deployed `RecordProvenance` carries both; the designer
analysis recommends omitting privacy. Three readings, no psyche
ratification. Porting a `SmallRecord` would have to pick one. Per the
ask-when-unclear override, surface the question. The decision the psyche
owes: *"SmallRecord = {identifier, topics, kind, description, certainty,
date, time} with privacy omitted, or does it also carry privacy? And is
'magnitude' the certainty field, the privacy field, or both?"*

## (4) RecordDefault short-form op (1550) — MISSING as a wire op; Entry::open exists as a constructor only

`RecordDefault` does not exist anywhere in the triad — no schema root, no
generated type, no daemon handler (grep across all three repos returns
zero hits outside reports). The deployed recording surface is the single
canonical `Record(Entry)` operation (`spirit.schema:8`), where `Entry`
demands all five fields positionally.

The default-injecting constructor 1550 implies DOES exist, but only as a
Rust helper, not a wire operation:

```rust
impl Entry {
    pub fn open(
        topics: Topics,
        kind: Kind,
        description: Description,
        certainty: Certainty,
    ) -> Self {
        Self {
            topics,
            kind,
            description,
            certainty,
            privacy: Magnitude::Zero,
        }
    }
}
```
(`signal-persona-spirit/src/lib.rs:387-402`). `Entry::open` bakes
`privacy = Magnitude::Zero` (the open/public default) but still requires
the caller to pass `certainty` explicitly — it defaults privacy only, not
"magnitude." Also note the `Entry` decoder ALREADY tolerates an omitted
trailing privacy field, defaulting to Zero
(`lib.rs:416-437`: `if decoder.peek_is_record_end()? { Magnitude::Zero }
else { Magnitude::decode(decoder)? }`), so a 4-field record NOTA already
round-trips as a privacy-Zero entry at the codec layer.

**Portability: BLOCKED — two open psyche parameters.** (a) 1550 lists
"topics, kind, description, **magnitude**" as the customizable set — but
`Entry::open` keeps `certainty` customizable and defaults `privacy`,
while a literal RecordDefault might want to default `certainty` too
(common routine calls do not pick a certainty). Which fields default vs.
stay customizable is not settled — and "magnitude" again ambiguous
(certainty? privacy?). (b) Can the caller override privacy through
RecordDefault, or is privacy=Zero hard-baked (forcing any private capture
through the full `Record`)? The privacy-override question is an explicit
open parameter. A mechanical port would have to invent the field
partition. The decision the psyche owes: *"RecordDefault customizable set
= {topics, kind, description, certainty} with privacy forced Zero, or
does it also expose privacy? And is the defaulted field certainty or
privacy?"*

## (5) Variant-ladder tier-1 zero-arg shortcuts (1474) — PARTIAL; recency depths exist as filter variants, no standalone tier-1 ops, names + privacy default open

The recency words exist, but as nested `RecordQuery` FILTER variants, not
as standalone zero-arg operations:

```rust
pub enum RecordedTimeSelection {
    Any,
    Between(RecordedTimeRange),
    Since(RecordedTime),
    Until(RecordedTime),
    Recent,
    Shallow,
    Deep,
    VeryDeep,
}
```
(`signal-persona-spirit/src/lib.rs:596-606`), honored by the daemon with
concrete record caps:

```rust
    const fn from_recorded_time_selection(selection: RecordedTimeSelection) -> Option<Self> {
        match selection {
            RecordedTimeSelection::Shallow => Some(Self::new(SHALLOW_RECORD_LIMIT)),
            RecordedTimeSelection::Recent => Some(Self::new(RECENT_RECORD_LIMIT)),
            RecordedTimeSelection::Deep => Some(Self::new(DEEP_RECORD_LIMIT)),
            RecordedTimeSelection::VeryDeep => Some(Self::new(VERY_DEEP_RECORD_LIMIT)),
            _ => None,
        }
    }
```
(`persona-spirit/src/store.rs:553-561`) with caps
`SHALLOW=5, RECENT=15, DEEP=30, VERY_DEEP=100`
(`store.rs:35-38`). The deployed query shape carries `Recent/Shallow/Deep/VeryDeep`;
the `examples/canonical.nota` exercises all four
(`(Observe (Records ((Partial [spirit]) None Any Recent ...)))` etc.).

What is MISSING vs. 1474's "short forms ... for normal operations":
- No `Today` or `ThisWeek` variant (1474's examples include `ThisWeek`).
  Only the four depth words exist.
- These are NOT zero-arg tier-1 OPERATIONS. They are deep-nested filter
  variants inside the full 6-field `RecordQuery`; a caller still composes
  `(Observe (Records ((Any []) None Any Recent (Exact Zero)
  SummaryOnly)))`. There is no `(Recent)` / `(Shallow)` top-level
  operation that lowers to the full query. The variant-ladder "tier-1
  zero-arg shortcut" idea is unrealized at the operation level. (The
  `RecordQuery` decoder does support progressive omission of trailing
  fields, `lib.rs:663-737`, which is a partial lowering — but the entry
  point is still `Observe(Records(...))`.)

**Portability: BLOCKED — naming and privacy-default open parameters.**
(a) The standalone-op names are undecided — would they be operation roots
(`Recent`, `Today`) or sugar that the codec lowers? 1474 gives examples
not a closed set; `Today`/`ThisWeek` need clock-relative bounds the daemon
does not compute today. (b) Every shortcut would bake a default
privacy-selection; the deployed shortcuts default to
`PrivacySelection::default_observation_privacy()` = `Exact(Zero)`
(`lib.rs:582-584`), but whether a tier-1 shortcut should hard-bake
Zero-privacy or expose it is unsettled. (c) The full closed name set
(does `Today`/`ThisWeek` ship?) is a psyche decision. A mechanical port
would have to invent both the name set and the clock semantics.

## Cross-cutting observations

The triad's removal vocabulary is internally consistent and well-typed:
purpose-named newtypes throughout (`RecordIdentifier`, `ArchivePath`,
`StatementText`), the archive-first safety invariant is encoded as a
control-flow branch with a typed `RemovalCandidateSkipReason` enum, and
the Sema projection cleanly labels collect as Retract→Retracted. The
designs that have landed (CollectRemovalCandidates, the recency filter
words) are landed to a higher fidelity than the bare intent text required
(three-vector receipt; per-record skip reasons). The blockers are all
genuine intent gaps, not implementation laziness.

## Portability ledger

| Design | Status | Portable? / blocked-reason |
|---|---|---|
| (1) CollectRemovalCandidates (1543/1547) | implemented (Reading B) | BLOCKED — Reading A vs B is psyche-only; deployed code + all 3 reports land on B but 1547's "separate from destruction" reads toward A |
| (2) OutputTarget enum (1544/1548) | partial (`ArchiveTarget` Inline\|File only) | BLOCKED — does Stderr belong (1548 says "not an error channel" yet lists it)? does Inline survive vs Stdout? rename + generalize now? |
| (3) SmallRecord type (1549) | missing as distinct type | BLOCKED — field set undecided: privacy in or out? which "magnitude" (certainty/privacy/both)? |
| (4) RecordDefault op (1550) | missing as wire op (`Entry::open` is a helper) | BLOCKED — which field defaults (certainty vs privacy)? can caller override privacy? |
| (5) Tier-1 zero-arg shortcuts (1474) | partial (depth words are filter variants, not ops) | BLOCKED — op name set undecided (Today/ThisWeek?); clock semantics absent; per-shortcut privacy default unsettled |
