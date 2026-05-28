# Spirit Signal Surface Bad-Pattern Audit

## Trigger

The live production query:

```sh
spirit "(Observe (RecordIdentifiers ((Exact 1053) DescriptionOnly)))"
```

returns:

```nota
(RecordsObserved ([(1053 [spirit production query by record number] Decision [Production Spirit should support querying intent records by numeric identifier, including exact identifiers and identifier ranges.] Maximum)]))
```

Two problems are visible from the user surface:

- `DescriptionOnly` is not literally description-only. It returns identifier,
  topics, kind, description, and magnitude.
- `RecordsObserved` is plural but prints as a single-field record wrapping a
  vector: `(RecordsObserved ([...]))`.

## Why The Double Delimiter Happens

This is not a NOTA requirement. It is a signal/schema implementation choice.

`signal-persona-spirit/spirit.schema` declares:

```nota
RecordsObserved [(Vec RecordDescription)]
```

and the `Reply` feature lists `RecordsObserved` by name. The current
`signal-frame` schema adapter then emits every reply variant as:

```rust
RecordsObserved(RecordsObserved)
```

That means the wire shape has two layers:

1. the reply variant record head, `RecordsObserved`;
2. the payload record, `RecordsObserved { records: Vec<_> }`.

The payload record has exactly one field, so it prints as `([...])`. The vector
inside that field prints as `[...]`. The result is:

```nota
(RecordsObserved ([...]))
```

For a plural reply, the cleaner shape would be conceptually direct:

```nota
(RecordsObserved [...])
```

or, if the reply is meant to name the projection:

```nota
(RecordSummaries [...])
```

The current production schema path cannot express that directly because the
old `Reply` feature carries only type names, and both the old
`signal_channel!([schema])` adapter and the newer schema-rust emitter map each
reply name to a same-named payload type.

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:56`
- `/git/github.com/LiGoldragon/signal-frame/macros/src/schema_reader.rs:124`
- `/git/github.com/LiGoldragon/signal-frame/schema-rust/src/lib.rs:260`

## Findings

### 1. `DescriptionOnly` Is Misnamed

`ObservationMode::DescriptionOnly` selects `RecordsObserved`, but the payload
type is `RecordDescription`, which includes record identifier, topics, kind,
description, and certainty.

This is a semantic-name bug. The mode is really "without provenance" or
"record summaries".

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:26`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:243`
- `/git/github.com/LiGoldragon/persona-spirit/src/store.rs:252`

Better names:

- `WithoutProvenance`
- `SummaryOnly`
- `RecordSummaryOnly`

`WithoutProvenance` is the most exact opposite of `WithProvenance`.
`SummaryOnly` is shorter and matches earlier schema-e2e fixture direction,
but requires renaming `RecordDescription` to `RecordSummary` to be honest.

### 2. `RecordDescription` Is Also Misnamed

The type called `RecordDescription` is not the description. It is a compact
record projection:

```rust
pub struct RecordDescription {
    pub identifier: RecordIdentifier,
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Magnitude,
}
```

This should be `RecordSummary`, `IntentRecord`, or `RecordHeader`.

`RecordSummary` is the best fit because `RecordProvenance` extends it with
date/time provenance.

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:49`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:348`

### 3. `RecordProvenance.description` Compounds The Misname

`RecordProvenance` has a field named `description`, but that field is a whole
`RecordDescription` payload. This reads as if provenance is attached only to a
description string, not to the observed record summary.

The field should be `record` or `summary`.

File:

- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:357`

### 4. All Plural Observation Replies Have The Same Wrapper Smell

The same one-field wrapper pattern appears on:

- `RecordsObserved { records: Vec<RecordDescription> }`
- `RecordProvenancesObserved { records: Vec<RecordProvenance> }`
- `TopicsObserved { topics: Vec<TopicCount> }`
- `QuestionsObserved { questions: Vec<QuestionSummary> }`

Live/expected outputs therefore have the same awkward shape:

```nota
(RecordsObserved ([...]))
(TopicsObserved ([...]))
(QuestionsObserved ([...]))
```

These should be direct plural payloads if the signal schema supports direct
variant payload types, or the payload type should be named as the noun:

```nota
(RecordSummaries [...])
(RecordProvenances [...])
(TopicCounts [...])
(QuestionSummaries [...])
```

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:432`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:437`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:442`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:447`

### 5. Singular Observation Replies Also Have Avoidable Wrapper Records

`StateObserved` is a single-field wrapper around `PresenceView`, producing:

```nota
(StateObserved ((Absent None)))
```

Conceptually cleaner:

```nota
(StateObserved (Absent None))
```

The same issue applies to event wrappers:

- `StateChanged { state: PresenceView }`
- `RecordCaptured { record: RecordDescription }`
- `OperationReceived { operation: OperationKind }`
- `EffectEmitted { observation: SemaObservation }`

This is less severe than plural vector wrappers because the event/reply head
does add a verb-like semantic, but the extra record layer is still an artifact.

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:427`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:500`

### 6. `Mode` Is Too Generic

The schema aliases:

```nota
Mode ObservationMode
```

then uses `Mode` in query records. That makes the schema less readable. The
field is not a universal mode; it is specifically an observation result mode.

Use `ObservationMode` directly, or rename the type to `RecordProjection`.

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:28`
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:40`
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:46`
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:48`

### 7. `RecordIdentifierQuery.record_identifier_selection` Is A Schema Leak

The Rust field name is:

```rust
pub record_identifier_selection: RecordIdentifierSelection
```

That likely came from schema-generated naming pressure. Inside
`RecordIdentifierQuery`, the natural field name is just `selection`. The
ancestry is already in the containing type.

File:

- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:316`

### 8. The Schema And Rust Type Definitions Can Drift

`spirit.schema` says:

```nota
PresenceView [Presence FocusArea]
```

Rust says:

```rust
pub struct PresenceView {
    pub presence: Presence,
    pub focus: Option<FocusArea>,
}
```

The Rust code is what production uses, because `signal_channel!([schema])`
currently consumes the schema for channel route shape while the domain types
are still hand-written. That means the schema can be stale and still pass
tests.

This is the deepest bad pattern in this audit: the schema is presented as a
contract but is not yet the source of truth for the actual Rust data types.

Files:

- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:52`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:370`

## Recommended Fix Order

1. **Contract names first, compatibility preserving.** Add a better mode name
   such as `WithoutProvenance` or `SummaryOnly` while deciding whether to keep
   `DescriptionOnly` as a migration alias in production.
2. **Rename the projection nouns.** Rename `RecordDescription` to
   `RecordSummary`, and `RecordProvenance.description` to `summary` or
   `record`.
3. **Fix schema drift.** Make `PresenceView` agree with Rust, or better,
   generate these domain types from the schema so drift becomes impossible.
4. **Fix the reply-shape substrate.** Extend the schema feature model so reply
   variants can carry direct payload expressions, not only same-named payload
   records. This is the structural fix for `(RecordsObserved ([...]))`.
5. **Then clean the production CLI surface.** Canonical examples should show
   the beautiful form only after the decoder accepts it and tests prove
   compatibility or a clean cutover.

## Conclusion

The user's complaint is correct. This is not just one ugly enum variant. It is
a cluster of old signal-schema limitations and naming shortcuts leaking into
the human-facing Spirit CLI.

The highest-signal immediate production fix is the naming pass:
`DescriptionOnly` and `RecordDescription` are wrong today. The delimiter shape
is a deeper schema-feature limitation and should be fixed in `signal-frame` /
schema-rust rather than hacked in `persona-spirit`.
