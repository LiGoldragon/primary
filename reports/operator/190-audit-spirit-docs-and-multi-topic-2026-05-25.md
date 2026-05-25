# Audit — Spirit docs and multi-topic fit

*Kind: Audit · Topic: spirit · 2026-05-25*

## Scope

This audits the documentation sweep that updated Spirit/NOTA CLI guidance to
the v0.2 shape and checks how close the current Spirit implementation is to the
latest intent around dense intent capture.

Files checked:

- `AGENTS.md`
- `skills/intent-log.md`
- `skills/spirit-cli.md`
- `skills/nota-design.md`
- `skills/component-triad.md`
- `nota/README.md`
- `nota/ARCHITECTURE.md`
- `nota-codec/README.md`
- `nota-codec/ARCHITECTURE.md`
- `persona-spirit/ARCHITECTURE.md`
- `signal-persona-spirit/ARCHITECTURE.md`
- `signal-persona-spirit/src/lib.rs`
- `persona-spirit/src/store.rs`

## Current state

The active v0.2 shape is coherent:

```nota
(Record (<topic> <Kind> [description] <Magnitude>))
(Observe (Records (<topic?> <kind?> <mode>)))
(Observe Topics)
```

The implementation matches that:

- `signal-persona-spirit::Entry` has one `topic: Topic`.
- `RecordDescription` returns one `topic: Topic`.
- `RecordQuery` filters by `Option<Topic>` and `Option<Kind>`.
- `persona-spirit::SpiritStore` stores `StampedEntry { entry, date, time }`
  and derives topic counts by reading each stored record's single topic.
- The migration from the old file-shaped/0.1 schema preserves identifiers and
  timestamps while dropping context/verbatim into the v0.2 description-only
  model.

The documentation sweep I landed is accurate for that deployed shape. The active
guidance now teaches double-quoted inline NOTA:

```sh
spirit "(Record (spirit Clarification [description] Medium))"
```

No active skill/doc surface found in the sweep still teaches `spirit '...'`,
`SummaryOnly`, or quote-delimited NOTA strings as the normal form.

## Main drift toward intent

The largest drift is not the shell quoting documentation. It is the single-topic
record shape.

Recent Spirit records already show the pressure:

- record 676: topics are user-creatable single strings;
- record 702: Spirit records may carry a vec of topics rather than a single
  topic, current shape is single topic;
- record 706: multi-topic support is worth auditing and another hard database
  migration is acceptable to consider.

The current single-topic shape forces agents to choose one routing label for
statements that naturally belong to more than one semantic area. Examples from
recent work:

```nota
(Record (spirit Correction [Spirit CLI calls should wrap the whole NOTA argument in shell double quotes...] Maximum))
```

That entry also belongs under `nota`, because the reason is bracket-string NOTA
making shell double quotes safe.

```nota
(Record (schema Clarification [Schema macro expansion needs indexed reading order with lazy resolution] Maximum))
```

That can also belong under `nota-schema-language` or `macro-library-core-vs-extension`
depending on how an agent searches later.

The single-topic model makes the agent decide one primary topic. The multi-topic
model lets the entry itself express the cross-cutting relationship.

## Recommended v0.3 shape

Use a real type boundary for the field:

```rust
pub struct Topics(Vec<Topic>);
```

Then change the public signal records:

```rust
pub struct Entry {
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Magnitude,
}

pub struct RecordDescription {
    pub identifier: RecordIdentifier,
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Magnitude,
}
```

Keep `RecordQuery` simple for the first cut:

```rust
pub struct RecordQuery {
    pub topic: Option<Topic>,
    pub kind: Option<Kind>,
    pub mode: ObservationMode,
}
```

The query semantics become: `Some(topic)` matches records whose `topics`
contains that topic. `None` still means all topics.

This avoids inventing a larger query language before need. If agents later need
multi-topic query logic, add a `TopicFilter` enum:

```rust
pub enum TopicFilter {
    Any,
    Includes(Topic),
    IncludesAny(Topics),
    IncludesAll(Topics),
}
```

But that should wait for pressure. The useful move now is multi-topic storage,
single-topic membership filtering, and topic catalog counts.

## NOTA examples

The record form becomes:

```nota
(Record ([spirit nota] Correction [Spirit CLI calls should wrap inline NOTA in shell double quotes because bracket strings free the quote character.] Maximum))
```

Single-topic records still use a vector:

```nota
(Record ([spirit] Clarification [Multi-topic support is ready for a hard migration design.] Medium))
```

Existing query examples can remain almost identical:

```nota
(Observe (Records ((Some spirit) None DescriptionOnly)))
(Observe Topics)
```

The only semantic change is that `Some spirit` matches membership in the topic
vector, not equality with a single topic field.

`Observe Topics` should count topic memberships, not records. A record with
`[spirit nota]` increments both `spirit` and `nota`. Duplicate topics in one
record should be rejected or deduplicated before storage; my lean is reject,
because a duplicate topic in one entry is almost certainly a writer bug.

## Migration shape

This is a hard schema migration. It is still contained.

New migration step:

```text
v0.2 StoredRecord
  identifier: RecordIdentifier
  entry:
    entry:
      topic: Topic
      kind: Kind
      description: Description
      certainty: Magnitude
    date: Date
    time: Time

v0.3 StoredRecord
  identifier: RecordIdentifier
  entry:
    entry:
      topics: Topics(vec![topic])
      kind: Kind
      description: Description
      certainty: Magnitude
    date: Date
    time: Time
```

The migration preserves:

- record identifier order;
- daemon-stamped date and time;
- kind;
- description;
- magnitude.

The migration changes:

- `topic` becomes `topics` with a one-element vector;
- topic catalog counts switch from one field per record to vector membership.

Implementation belongs in the same pattern as the current
`spirit-migrate-0-1-to-0-2` tool: a one-off migration binary or sema-upgrade
module that reads a copied source database and writes an empty target database.
Do not add import/file-substrate logic to the Spirit daemon.

## Tests to add

The constraints that should gate the migration:

```text
signal-persona-spirit:
  - Entry with one topic round-trips through NOTA and rkyv.
  - Entry with many topics round-trips through NOTA and rkyv.
  - RecordDescription with many topics round-trips.
  - Existing query shape round-trips unchanged except membership semantics.

persona-spirit:
  - Record with [spirit nota] is returned by topic=spirit.
  - Same record is returned by topic=nota.
  - It is not returned by topic=schema.
  - Observe Topics counts both memberships.
  - Duplicate topic input is rejected or normalized by one explicit rule.
  - v0.2 to v0.3 migration maps topic -> [topic] and preserves identifiers/date/time.
  - The migration refuses a non-empty target.
  - The one-off migration CLI keeps the single-argument rule.
```

Run all tests through Nix with `--option max-jobs 0`.

## Difficulty

Mechanically this is medium, not deep:

- It touches the ordinary contract crate and the daemon store/read path.
- It is a breaking wire/storage schema change.
- It needs another hard migration and deployment step.
- It does not require changing the no-verbatim/no-context v0.2 simplification.
- It does not require changing daemon-stamped time.
- It does not require changing the CLI architecture.

The highest-risk part is not the code. It is choosing the query semantics before
locking the new schema. The conservative v0.3 choice is:

```text
entries store many topics;
queries still filter by one topic;
topic catalog counts memberships.
```

That gives most of the value without over-designing the read API.

## Aspects to bring closer to intent

1. **Multi-topic entries.** This is the main improvement. Single-topic routing is
   already too lossy for cross-cutting intent.
2. **Rename `certainty` in current docs/code eventually.** The type is
   `Magnitude`, but several surfaces still keep the field name `certainty`.
   That was preserved intentionally for the dimension, but the v0.2 vocabulary
   now says magnitude in user guidance. Keep only if the design wants
   "certainty: Magnitude"; otherwise change field name during a future schema
   bump.
3. **Update `INTENT.md` synthesis.** It still describes the older record shape
   with verbatim/context. Spirit v0.2 has superseded that in practice. This is a
   designer-surface update, but operator should flag it.
4. **Update `orchestrate/AGENTS.md` intent append exemption.** It still describes
   lock-free appends to `intent/*.nota`. That is historical now; Spirit is the
   normal write path. This is also designer-surface guidance.
5. **Keep hard migrations out of the daemon.** The one-off migration tool shape
   remains aligned with the explicit no-import-logic-in-Spirit intent.

## Open question

Do we want v0.3 to stop at membership filtering, or should the first multi-topic
version also introduce a richer query enum?

My lean: stop at membership filtering. The smallest schema that fulfills the
clear intent is `Entry.topics: Topics`, `RecordDescription.topics: Topics`, and
existing `Option<Topic>` query semantics changed to vector membership. Add a
larger `TopicFilter` enum only when an agent needs "records that have all of
these topics" or "any of these topics" as a real workflow.
