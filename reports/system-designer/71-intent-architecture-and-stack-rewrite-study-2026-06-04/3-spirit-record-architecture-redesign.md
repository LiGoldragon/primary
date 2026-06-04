# Spirit Record Architecture Redesign — concrete, implementable

System-designer-lane research sub-agent report. Read-only. Standing
constraint: `(Spirit Correction 157dwrve)` — do work properly or not
at all. Every type name and line number below is verified against the
deployed source (Spirit live at v0.5.0). Where the skills lag (v0.4.2)
the source wins and is flagged.

This report designs the next Spirit record architecture for the FOUR
coupled moves:

1. `(Spirit Decision 3awz)` — per-kind field sets.
2. `(Spirit Principle audg3)` — composite / repurposed intent.
3. `(Spirit Principle 6vsl)` — weight distinct from certainty.
4. `(Spirit Principle 73t3)` — streamlined archive with composite→source provenance.

## 1. The current record shape, exactly

### The wire contract — deployed `Entry`

`/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`:

```rust
508  pub type Certainty = Magnitude;
509  pub type Privacy = Magnitude;
510
511  #[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
512  pub struct Entry {
513      pub topics: Topics,
514      pub kind: Kind,
515      pub description: Description,
516      pub certainty: Certainty,
517      pub privacy: Privacy,
518  }
```

So EVERY record today carries all five fields. `certainty` and
`privacy` are both `Magnitude` aliases. The codec is positional,
untagged (`start_record_untagged` / `expect_positional_record_start("Entry", 5)`,
lines 537–569), and `privacy` is the only field with a decode-time
default: when the record ends early, `privacy` falls back to
`Magnitude::Zero` (lines 556–560). That existing optional-tail
behaviour is the migration seam the redesign formalizes.

### `Kind` — the five variants (lib.rs 454–463)

```rust
pub enum Kind {
    Decision,
    Principle,
    Correction,
    Clarification,
    Constraint,
}
```

### `Magnitude` — the eight-rung ladder

`/git/github.com/LiGoldragon/signal-sema/src/magnitude.rs` 14–25:
`Minimum=0, VeryLow, Low, Medium, High, VeryHigh, Maximum=6, Zero=7`.
`Zero` is physically last (rkyv-discriminant stability) but order-ranks
to 0 (lines 58–69) — so `Zero < Minimum < … < Maximum` for comparison.
`Certainty == Zero` is the removal-candidate marker
(`CertaintySelection::removal_candidates`, lib.rs 690–692).

### The daemon stamp + storage shape

`/git/github.com/LiGoldragon/persona-spirit/src/store.rs`:

- `StampedEntry { entry: Entry, date: Date, time: Time }` (73–78) —
  the daemon stamps `date`/`time`; they are NOT in the wire `Entry`.
- `StoredRecord { identifier: RecordIdentifier, entry: StampedEntry }`
  (57–61) — the stored shape with the minted 12-byte identifier.
- `RecordIdentifier` is a 12-byte (96-bit) value rendered as base36
  (lib.rs 132–270); identifiers are random-minted, not ordinal
  (`RecordIdentifierMint::next_identifier`, store.rs 787–797). This is
  exactly the "hash identity" the composite move references.

### The current archive mechanism (the thing to streamline)

`collect_removal_candidates` (store.rs 160–196): validates the query is
exactly `certainty == Zero && privacy == Zero`
(`CollectionQueryGuard`, 423–436 + `is_exact_zero_candidate_query`,
lib.rs 1195–1203), copies matching records into a SEPARATE redb/sema
file (`RemovalCandidateArchiveStore`, 480–521) as
`ArchivedRemovalCandidate { summary: RecordSummary }` (63–66), then
retracts them from the live table. The archive stores only
`RecordSummary` (no date/time, no provenance link). Wire receipt is
`RemovalCandidatesCollected { archived_records, removed_identifiers,
skipped_candidates }` (lib.rs 1266–1297). This is the ad-hoc dump the
intent calls out: it is keyed by identifier, carries no
composite→source link, and drops the daemon timestamp.

### The schema-derived pilot (the real target surface)

Spirit is being rebuilt schema-derived. The pilot schema is
`/git/github.com/LiGoldragon/spirit/schema/lib.schema`. Its `Entry` (line 89):

```
Entry { Topics * Kind * Description * Magnitude * Privacy * }
Kind [Decision Principle Correction Clarification Constraint]
Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]
```

This is the same five-field flat record expressed in schema. The
redesign is authored HERE (schema-next), and `schema-rust-next` emits
the Rust. The new record shape must be expressed in the schema
language first, not hand-written Rust.

## 2. The redesigned record model

### Design principle: an enum of record variants

Per-kind field sets means the flat `Entry` becomes a SUM type: one
variant per kind, each carrying only the fields that kind needs. The
common fields (topics, description, certainty, weight) live inside each
variant; privacy lives ONLY on the variants that can bear private
substance. The daemon stamp (date/time) and the minted identifier stay
where they are today (store side), not in the wire record.

Common fields, by the workspace rule that names don't carry ancestry:
`topics`, `description`, `certainty`, `weight`. Privacy is NOT common —
it appears only where private substance is possible.

### The schema expression (schema-next `.schema` syntax)

Authored in `spirit/schema/lib.schema`. The enum-body form is square
brackets containing bare symbols (unit) or `(Variant Payload)` pairs
(confirmed: schema-rust-next ARCHITECTURE.md "square brackets contain
one vector element type, so unit variants are bare symbols and
data-carrying variants are parenthesized records such as
`(Record Entry)`"). Struct bodies are strict `{ field Type }` maps;
`*` after a name is the shorthand "field name = type name".

```
Topic        String
Topics       (Vec Topic)
Description  String
Certainty    Magnitude
Weight       Magnitude
Privacy      Magnitude
RecordIdentifier  Integer
SourceRecords     (Vec RecordIdentifier)

Magnitude  [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]

PublicBody   { Topics * Description * Certainty * Weight * }
PrivateBody  { Topics * Description * Certainty * Weight * Privacy * }
CompositeBody { Topics * Description * Certainty * Weight * SourceRecords * }

Entry [
  (Decision      PublicBody)
  (Principle     PublicBody)
  (Correction    PublicBody)
  (Clarification PublicBody)
  (Constraint    PublicBody)
  (PrivateNote   PrivateBody)
  (Composite     CompositeBody)
]
```

Notes on the schema choice:

- `Entry` becomes an ENUM (the record-variant set), replacing today's
  flat struct + separate `Kind` enum. The kind IS the variant tag now —
  this is the per-kind-field-sets move made structural. `Kind` as a
  standalone enum disappears from the record (it survives only in query
  filters; see migration).
- The five existing kinds carry `PublicBody` (no privacy field) because
  every deployed public intent record is privacy `Zero`. Privacy lives
  on a distinct `PrivateNote` variant carrying `PrivateBody`. This is
  the cleanest reading of `(Spirit Decision 3awz)`: "a private-bearing
  record carries a privacy field, an ordinary public record omits it."
- `Composite` is a SEVENTH variant carrying `CompositeBody`, which adds
  `SourceRecords` (a `(Vec RecordIdentifier)`) on top of the common
  fields. See the open question on whether Composite should instead
  wrap any kind rather than be its own variant.
- `Weight` and `Certainty` are both `Magnitude` aliases (see weight
  decision below). Distinct aliases keep them legible at type sites
  even though they share the ladder.

### The emitted Rust shape (what schema-rust-next produces)

Following the emitter's documented projection (newtype for single-field
brace, struct for named-field map, enum body with parenthesized
payloads → tuple-variant enum; verified against
`schema-rust-next/tests/fixtures/spirit_generated.rs` Entry/Kind/Magnitude
at lines 27–63):

```rust
pub type Certainty = Magnitude;
pub type Weight = Magnitude;
pub type Privacy = Magnitude;

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, NotaDecode, NotaEncode, Clone, Debug, PartialEq, Eq)]
pub struct PublicBody {
    pub topics: Topics,
    pub description: Description,
    pub certainty: Certainty,
    pub weight: Weight,
}

#[derive(/* same derives */)]
pub struct PrivateBody {
    pub topics: Topics,
    pub description: Description,
    pub certainty: Certainty,
    pub weight: Weight,
    pub privacy: Privacy,
}

#[derive(/* same derives */)]
pub struct CompositeBody {
    pub topics: Topics,
    pub description: Description,
    pub certainty: Certainty,
    pub weight: Weight,
    pub source_records: Vec<RecordIdentifier>,
}

#[derive(/* same derives */)]
pub enum Entry {
    Decision(PublicBody),
    Principle(PublicBody),
    Correction(PublicBody),
    Clarification(PublicBody),
    Constraint(PublicBody),
    PrivateNote(PrivateBody),
    Composite(CompositeBody),
}
```

`Entry` accessor methods (`topics()`, `certainty()`, `weight()`,
`privacy() -> Option<Privacy>`, `source_records() -> &[RecordIdentifier]`)
go on `impl Entry` so consumers do not match the variant everywhere —
per the method-on-noun rule. `privacy()` returns `Option` because only
`PrivateNote` bears it; non-private variants return `None` (which the
store treats as `Magnitude::Zero` for the privacy filter, preserving
today's behaviour).

### The Composite record — fields and provenance

`Composite(CompositeBody)` carries:

- `topics`, `description` — the agglomerated record's own framing.
- `certainty` — confidence in the composite statement itself.
- `weight` — accumulated importance (see below); a composite's weight
  is higher because it is composed of many sources.
- `source_records: Vec<RecordIdentifier>` — the hash identities of the
  retired source records, in declaration order. Because
  `RecordIdentifier` IS the hash identity (random-minted 96-bit,
  base36-rendered), this preserves provenance WITHOUT copying the
  source bodies into the composite. The sources move to the archive
  (below) and stay resolvable by these identifiers.

Provenance is therefore a forward link (composite names its sources)
resolved against the archive. No reverse link is stored on the archived
record in v1 — the composite is the index. See open question on whether
the archived record should also back-reference its composite.

### Weight — the decision

**Weight is a `Magnitude`** (the same eight-rung ladder as certainty),
NOT a raw integer count. Rationale grounded in the deployed stack:

- The whole Spirit vocabulary is qualitative magnitudes
  (`signal-sema::Magnitude`); certainty and privacy already ride it.
  Weight riding the same ladder keeps the record uniform, keeps
  selections expressible (a `WeightSelection` mirrors
  `CertaintySelection` — `Any/Exact/AtMost/AtLeast`), and avoids
  introducing an unbounded integer into a qualitative contract.
- `(Spirit Principle 6vsl)` says weight COMPOUNDS on top of certainty
  and a composite has HIGHER weight. With a `Magnitude`, "compounds"
  means: a composite's weight is at least the max of its sources'
  weights, bumped up one rung (saturating at `Maximum`) per the
  agglomeration. A non-composite record defaults to weight =
  `Minimum` (the lowest non-`Zero` rung) — it carries its own single
  unit of importance. This keeps weight strictly ordered and bounded.
- Reinforcement (the same intent restated/agglomerated) raises weight;
  certainty stays the author's confidence. The two axes are
  independent: a `Minimum`-certainty record can accumulate `High`
  weight if many sources reinforce the topic, and a `Maximum`-certainty
  one-off keeps `Minimum` weight.

**Default for non-composite records: `weight = Magnitude::Minimum`.**
(Not `Zero` — `Zero` is the removal marker for certainty and must not
collide with the weight axis semantically; a live record has at least
minimum weight.) See open question if the psyche prefers an integer
reinforcement counter instead.

The compounding rule, as a method on the composite builder:

```rust
impl Weight {
    // Composite weight = one rung above the strongest source, saturating.
    fn compounded(sources: &[Weight]) -> Weight {
        let strongest = sources.iter().copied().max().unwrap_or(Magnitude::Minimum);
        strongest.next_rung_saturating() // Maximum stays Maximum
    }
}
```

(`next_rung_saturating` is a new associated method on `Magnitude` in
`signal-sema` honouring the `Zero`-last-but-order-0 layout.)

### Archive — the streamlined shape

The streamlined archive carries the composite→archived-source
provenance link cleanly. Replace `ArchivedRemovalCandidate { summary:
RecordSummary }` (store.rs 63–66, which drops timestamp and provenance)
with a record that preserves full provenance AND the composite back-link:

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
struct ArchivedRecord {
    identifier: RecordIdentifier,   // the source's own hash identity (the archive key)
    entry: StampedEntry,            // full body + daemon date/time, not a lossy summary
    retired_by: RetiredBy,          // why it left the live table
}

#[derive(/* derives */)]
enum RetiredBy {
    RemovalCandidate,                       // certainty Zero, the existing path
    Composite(RecordIdentifier),            // agglomerated into this composite
}
```

Two streamlining wins:

1. **Full body, not summary.** Archiving `StampedEntry` (not
   `RecordSummary`) keeps the daemon timestamp and the complete record,
   so an archived source resolved from a composite is the real thing,
   not a lossy projection.
2. **Provenance link.** `RetiredBy::Composite(composite_id)` records
   WHICH composite swallowed the source. Combined with the composite's
   forward `source_records` vector, provenance is bidirectional and
   resolvable by hash in both directions, with no string keys.

The agglomeration flow (new daemon operation, see implementer section):
the daemon (a) writes the new `Composite` entry, getting its minted
identifier; (b) for each source, moves it to the archive as
`ArchivedRecord { entry, retired_by: Composite(composite_id) }`;
(c) retracts the source from the live table. This mirrors
`collect_removal_candidates`'s archive-then-retract ordering (store.rs
166–190) so an archive failure leaves the live records intact (the
existing `ArchiveFailed` skip-receipt discipline carries over).

The two archive paths (removal-candidate dump and composite
agglomeration) now share ONE `ArchivedRecord` type and one archive
store, distinguished by `RetiredBy` — that is the streamlining the
intent asks for, versus today's single-purpose
`RemovalCandidateArchiveStore`.

## 3. Migration

Every deployed record already has a `Kind` and a `privacy` value, so
the map onto variants is total and mechanical:

| Deployed flat `Entry`                       | New variant                       |
|---|---|
| `kind=Decision, privacy=Zero`               | `Decision(PublicBody)` (drop privacy) |
| `kind=Principle, privacy=Zero`              | `Principle(PublicBody)` |
| `kind=Correction, privacy=Zero`             | `Correction(PublicBody)` |
| `kind=Clarification, privacy=Zero`          | `Clarification(PublicBody)` |
| `kind=Constraint, privacy=Zero`             | `Constraint(PublicBody)` |
| any kind, `privacy > Zero`                  | `PrivateNote(PrivateBody)` (privacy preserved; original kind moves into description or a `kind` field on PrivateBody — see open question) |
| (no deployed records)                       | `Composite(CompositeBody)` (new) |

`weight` is synthesized at migration: every existing record gets
`weight = Magnitude::Minimum` (the single-unit default). No existing
record is a composite, so no `source_records` to backfill.

The privacy-bearing case has a wrinkle: collapsing all elevated-privacy
records into one `PrivateNote` variant LOSES the original kind. Two
honest options (open question 4): keep `kind: Kind` as a field inside
`PrivateBody`, OR keep per-kind PRIVATE variants too (doubling the kind
set). The schema above takes the simplest route (single `PrivateNote`);
the implementer must confirm with the psyche before erasing kind on
private records.

### Wire / version implication — REQUIRES PSYCHE AUTHORIZATION

`signal-persona-spirit` is a CONTRACT crate. Changing `Entry` from a
5-field flat struct to a 7-variant enum is a BREAKING wire change. Per
the deployed contract version (`SPIRIT_CONTRACT_VERSION`, store.rs
30–32, `SchemaVersion::new(5)`) this is a MAJOR contract bump (schema
version 5 → 6). Per workspace rule, a breaking change to a contract
crate needs explicit psyche authorization before it lands. The
schema-derived pilot (`spirit/`) is the right place to prototype the
new shape on a feature branch WITHOUT touching the deployed v0.5.0
contract, then cut over via the version-handover machinery
(`signal-version-handover`, already wired in store.rs 19, 292–312).
A version-handover migration (`migration.rs` already hosts per-version
`Operation` translators, lib.rs migration module 107/179/273) carries
the v5→v6 record reshape.

## 4. Open design questions (genuine forks for psyche/orchestrator)

1. **Is `Composite` a new variant or a wrapper around any kind?**
   The design makes it a seventh `Entry` variant. Alternative: a
   composite could WRAP an existing kind (`Composite { kind: Kind,
   body, source_records }`) so an agglomeration of Decisions stays a
   Decision-flavoured composite. The variant form is simpler and
   matches "a record that references older records"; the wrapper form
   preserves kind through agglomeration. RECOMMEND the variant form
   unless kind-through-agglomeration matters to the psyche.

2. **Is weight a `Magnitude` or an integer reinforcement count?**
   The design picks `Magnitude` (bounded, qualitative, query-uniform).
   An integer count is more faithful to "accumulated" but breaks the
   all-qualitative contract and needs a bounded encoding. RECOMMEND
   `Magnitude`.

3. **Should the archived source back-reference its composite, or is
   the composite's forward `source_records` enough?** The design
   stores both (`RetiredBy::Composite(id)` + composite's vector).
   Forward-only is leaner but makes "what swallowed this record?"
   a full scan. RECOMMEND keeping both (cheap, bidirectional).

4. **Does collapsing private records to one `PrivateNote` variant lose
   kind acceptably, or keep `kind` inside `PrivateBody` / keep per-kind
   private variants?** This is the only lossy spot in migration.
   RECOMMEND keeping `kind: Kind` as a field on `PrivateBody` (no loss,
   no variant explosion) — pending psyche confirmation.

5. **Does per-kind field sets change the CLI surface?** The CLI is a
   NOTA-only single-argument binary. Today an author writes
   `(Decision (...))`-style records via the flat `Entry`. With the
   variant enum, the NOTA the author types becomes
   `(Composite (...))` / `(PrivateNote (...))` etc. — the variant tag
   IS the record head. This is arguably CLEANER (the kind is the head,
   not a positional field), but it is a surface change the intent-log /
   spirit-cli skills must be updated for. Confirm whether the author-
   facing NOTA should change shape.

## 5. For the implementer — ordered edit list

All on a feature branch. Designer lanes work in `~/wt/...` per the
code-repo rule; do NOT touch deployed v0.5.0 contract until the version
bump is authorized. Prototype in the schema-derived pilot first.

1. **schema-next pilot (`spirit/schema/lib.schema`)** — replace the
   flat `Entry { Topics * Kind * Description * Magnitude * Privacy * }`
   (line 89) and standalone `Kind` (line 92) with the enum-of-variants
   `Entry` plus `PublicBody` / `PrivateBody` / `CompositeBody` structs
   and the `Weight`/`SourceRecords` aliases shown in §2. Keep
   `Magnitude` (line 93). Update `Query` (line 90) so kind filtering
   matches against the variant tag, not a record field.

2. **`signal-sema` (`src/magnitude.rs`)** — add
   `Magnitude::next_rung_saturating(self) -> Magnitude` (honour the
   `Zero=7`/order-rank layout, lines 13–25, 58–69) for weight
   compounding. Method on `Magnitude`, not a free fn.

3. **Regenerate emitted Rust** — run schema-rust-next
   (`cargo run --example emit_schema -- spirit/schema/lib.schema
   spirit-next:lib`) to refresh `spirit/src/schema/lib.rs`; confirm the
   emitted `Entry` enum, the three body structs, and the `Weight` alias
   match §2. Add `impl Entry` accessor methods
   (`topics/description/certainty/weight/privacy()->Option/source_records`).

4. **Store (`persona-spirit/src/store.rs` equivalent in the pilot)** —
   a. Replace `ArchivedRemovalCandidate { summary: RecordSummary }`
      (63–66) with `ArchivedRecord { identifier, entry: StampedEntry,
      retired_by: RetiredBy }` and the `RetiredBy` enum (§2).
   b. `RemovalCandidateArchiveStore` (480–521) becomes a single
      `ArchiveStore` storing `ArchivedRecord`; `append` takes
      `ArchivedRecord`s; keyed by `identifier.code()`.
   c. `collect_removal_candidates` (160–196) archives as
      `RetiredBy::RemovalCandidate` with the full `StampedEntry`, not a
      summary.
   d. Add `agglomerate(composite_entry, source_ids)`: mint the
      composite identifier, write the `Composite` entry, archive each
      source as `RetiredBy::Composite(composite_id)`, then retract each
      source — archive-then-retract ordering so an archive failure
      preserves the live records (mirror 166–190 + the `ArchiveFailed`
      skip receipt).

5. **Contract crate (`signal-persona-spirit/src/lib.rs`) — ONLY after
   psyche authorizes the v5→v6 bump.** Mirror the enum-of-variants
   `Entry` (replace 511–570), drop `Kind` from the record (keep it for
   `RecordQuery.kind` filtering against the variant tag), add `Weight`
   alias + `WeightSelection` (mirror `CertaintySelection`, 682–702),
   add `Composite`/agglomeration `Operation`+`Reply` arms, add the new
   archive `Reply` carrying `RetiredBy`. Bump
   `SPIRIT_SCHEMA_VERSION` / `SPIRIT_CONTRACT_VERSION` (store.rs 28–32)
   5 → 6.

6. **Migration (`signal-persona-spirit/src/migration.rs`)** — add a
   v5→v6 `Operation` translator (the module already hosts per-version
   translators at 107/179/273) mapping each flat record to its variant
   per the §3 table; synthesize `weight = Minimum`; route
   `privacy > Zero` to `PrivateNote` (decide kind-retention per open
   question 4).

7. **Skills** — update `skills/intent-log.md` (the `Entry` positional
   shape at lines 216–228), `skills/spirit-cli.md`, and
   `skills/intent-maintenance.md` (archive/agglomeration lifecycle) to
   the new variant-headed NOTA shape and the weight axis. These skills
   currently document v0.4.2 and already lag the deployed v0.5.0
   privacy field — fix both.

8. **Tests** — the store test suite (store.rs 800–1563) constructs flat
   `Entry { topics, kind, description, certainty, privacy }` literals
   throughout; every one becomes a variant constructor. Add tests for:
   weight compounding, composite agglomeration archive+retract, archive
   `RetiredBy::Composite` round-trip, and the v5→v6 migration mapping.

## Skills-vs-source discrepancies found (source wins)

- `skills/intent-log.md` (216–228) documents `Entry` as a 5-field
  positional record but frames privacy as always present; the deployed
  codec (lib.rs 556–560) treats privacy as an optional tail defaulting
  to `Zero`. The skills are at v0.4.2; deployed is v0.5.0.
- The skills describe records by `Kind` as a positional field; the
  redesign makes kind the variant tag, so the skills need a structural
  rewrite, not a field tweak.
