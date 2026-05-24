*Kind: Design · Topic: spirit-complete-schema-vision · Date: 2026-05-24*

# 326 — Spirit complete schema — namespace values without name collision

**Status:** v5 — absorbs psyche feedback on /326-v4's namespace map values. The map's KEY declares the type's name; the value MUST NOT restate it. Two value shapes: `[…]` vector for multi-variant enums, `(…)` parens for struct-shaped types (no tag inside — key IS the implicit tag). Newtype = single-field struct = `(InnerType)`. Cross-schema imports keep the `(Path …)` variant. Six structural questions from v4 §8 remain open; v5 narrows the schema-syntax dimension only.

## §1 The data type inventory — unchanged

Three layers + storage. See `/326-v4 §1`.

## §2 The Spirit schema — `signal-persona-spirit/spirit.schema`

### §2.1 The file

```nota
[
  (State (Statement (engine assert)))
  (Record (Entry (engine assert)))
  (Observe (Observation (engine match)))
  (Watch (Subscription (engine subscribe)))
  (Unwatch (SubscriptionToken (engine retract)))
]

[]

[]

{
  Magnitude (Path ../signal-sema/magnitude.schema)
  SemaOperation (Path ../signal-sema/operation.schema)
  SemaOutcome (Path ../signal-sema/outcome.schema)
  SemaObservation (Path ../signal-sema/observation.schema)
}

{
  Kind [Decision Principle Correction Clarification Constraint]
  ObservationMode [SummaryOnly WithProvenance]
  Presence [Active Absent]
  UnimplementedReason [NotBuiltYet IntegrationNotLanded]

  Topic (String)
  Summary (String)
  Context (String)
  Quote (String)
  StatementText (String)
  FocusArea (String)
  RecordIdentifier (u64)
  QuestionIdentifier (String)
  QuestionText (String)
  StateSubscriptionToken (u64)
  RecordSubscriptionToken (u64)

  Entry (Topic Kind Summary Context Magnitude Quote)
  Statement (StatementText)
  RecordQuery ([Option Topic] [Option Kind] ObservationMode)
  RecordSubscription ([Option Topic] ObservationMode)
  RecordSummary (RecordIdentifier Topic Kind Summary Magnitude)
  RecordProvenance (RecordSummary Context Date Time Quote)
  TopicCount (Topic u64)
  State (Presence [Option FocusArea])
  QuestionSummary (QuestionIdentifier QuestionText)

  RecordObservation (RecordQuery)

  Observation [State (Records RecordQuery) Topics Questions]
  Subscription [State (Records RecordSubscription)]
  SubscriptionToken [(State StateSubscriptionToken) (Records RecordSubscriptionToken)]

  StoredRecord (RecordIdentifier StampedEntry)
  StampedEntry (Entry Date Time)
  RecordIdentifierMint (u64)

  RecordAccepted (RecordIdentifier)
  StateObserved (State)
  RecordsObserved ([Vec RecordSummary])
  RecordProvenancesObserved ([Vec RecordProvenance])
  TopicsObserved ([Vec TopicCount])
  QuestionsObserved ([Vec QuestionSummary])
  SubscriptionOpened (SubscriptionToken SubscriptionSnapshot)
  SubscriptionRetracted (SubscriptionToken)
  RequestUnimplemented (UnimplementedReason)
  SubscriptionSnapshot [(State State) (Records [Vec RecordSummary])]

  StateChanged (State)
  RecordCaptured (RecordSummary)

  OperationReceived (OperationKind)
  EffectEmitted (SemaObservation)
}

[
  (Reply
    RecordAccepted
    StateObserved
    RecordsObserved
    RecordProvenancesObserved
    TopicsObserved
    QuestionsObserved
    SubscriptionOpened
    SubscriptionRetracted
    RequestUnimplemented)

  (Event (belongs DomainStream)
    StateChanged
    RecordCaptured)

  (Observable
    (filter default)
    (operation_event OperationReceived)
    (effect_event EffectEmitted))
]
```

### §2.2 The namespace value forms

Three forms only, distinguished by the FIRST token after the map key:

| Form | Meaning | Example |
|---|---|---|
| `[…]` vector | multi-variant enum — elements are variants (unit `Decision` or data-carrying `(Records RecordQuery)`) | `Kind [Decision Principle …]`, `Observation [State (Records RecordQuery) Topics Questions]` |
| `(…)` parens | struct-shaped type — positional fields, no tag inside; map key IS the implicit tag | `Topic (String)`, `Entry (Topic Kind Summary Context Magnitude Quote)` |
| `(Path …)` | cross-schema import | `Magnitude (Path ../signal-sema/magnitude.schema)` |

The schema parser disambiguates by inspecting the first character: `[` → vector → enum; `(Path` → import; `(` followed by anything else → struct.

### §2.3 No name collision

The v4 form had entries like `Kind (Kind Decision Principle …)` — the outer `Kind` is the map key (declaring the type's name) AND the inner `(Kind …)` repeats `Kind` as the value's first element. Psyche pointed out this is name collision in an open namespace: same name twice, no guard, recursive declaration.

v5 fixes this by stripping the redundant tag from the value:
- `Kind [Decision Principle Correction Clarification Constraint]` — value is a vector of unit variants; key Kind names the type.
- `Topic (String)` — value is a 1-field struct; key Topic names the type.
- `Entry (Topic Kind Summary Context Magnitude Quote)` — value is a 6-field struct; key Entry names the type.

Names within the schema's namespace map are now relatable without recursion: every key appears EXACTLY ONCE.

### §2.4 Bare-token convention in Reply variants

In `(Reply RecordAccepted StateObserved …)`, each bare PascalCase token is a Reply variant whose name AND payload type are both the bare token. So `RecordAccepted` (the variant) carries a payload of type `RecordAccepted` (the namespace declaration). The convention: when the variant name matches a namespace-declared type name, the variant carries one field of that type.

This eliminates the v4 form `(RecordAccepted RecordAccepted)` redundancy.

### §2.5 Event with stream annotation

```nota
(Event (belongs DomainStream)
  StateChanged
  RecordCaptured)
```

The `(belongs DomainStream)` is an annotation at the Event-block level (all events in this Event block belong to `DomainStream`). Variants then use the bare-token convention. If different events belong to different streams, fall back to per-variant annotation: `(StateChanged belongs DomainStream)` per variant.

## §3 The base schema-for-a-schema — same form

The base schema (`nota/spirit.schema`) declares the schema-language's own vocabulary. Same shape rule applies: map values are vectors or parens, never restating keys.

```nota
[]
[]
[]
{}
{
  Schema (SignalHeader OwnerHeader SemaHeader Imports Namespace OptionalFeatures)
  SignalHeader ([Vec OperationVariant])
  OwnerHeader ([Vec OperationVariant])
  SemaHeader ([Vec SemaVariant])
  Imports ([Map Identifier Path])
  Namespace ([Map Identifier Declaration])
  OptionalFeatures ([Vec FeatureVariant])

  OperationVariant (Identifier PayloadRef EngineAnnotation)

  Declaration [(Inline TaggedRecord) (Cross Path)]

  TaggedRecord (Identifier [Vec FieldOrVariant])

  FieldOrVariant [(Field Identifier) (Variant Identifier [Option PayloadRef])]

  PayloadRef (Identifier)

  EngineAnnotation [Assert Mutate Retract Match Subscribe Validate]

  FeatureVariant [
    (Reply [Vec ReplyVariant])
    (Event [Vec EventVariant])
    (Observable ObservableDecl)
    (Storage [Vec StorageDecl])]

  ReplyVariant (Identifier Identifier)
  EventVariant (Identifier Identifier StreamRef)
  ObservableDecl (FilterMode OperationEventRef EffectEventRef)
  StorageDecl (Identifier TaggedRecord)

  FilterMode [Default (Custom Identifier)]
  StreamRef (Identifier)
  Identifier (String)
  Path (PathPrimitive)
  PathPrimitive (String)
}
[]
```

Notice: every key appears once. Struct declarations use `(fields…)` form; enum declarations use `[variants…]` form. No `Kind (Kind …)` or `Topic (Topic …)` redundancy.

## §4 What changes from v4

| Concern | v4 | v5 |
|---|---|---|
| Namespace map value for newtype `Topic` | `Topic (Topic String)` (restates Topic — name collision) | `Topic (String)` (struct with 1 field; key is implicit tag) |
| Namespace map value for leaf enum `Kind` | `Kind (Kind Decision Principle …)` (restates Kind) | `Kind [Decision Principle …]` (vector of unit variants) |
| Namespace map value for composite struct `Entry` | `Entry (Entry Topic Kind …)` (restates Entry) | `Entry (Topic Kind …)` (struct with N fields) |
| Namespace map value for multi-variant data-carrying enum `Observation` | `Observation (Observation State (Records RecordQuery) Topics Questions)` (restates) | `Observation [State (Records RecordQuery) Topics Questions]` (vector of variants) |
| Reply variants | `(RecordAccepted RecordAccepted)` (variant name + payload type both stated) | `RecordAccepted` (bare token; convention: variant name = payload type when both are namespace-declared) |
| Cross-schema import | `Magnitude (Path …)` (unchanged) | `Magnitude (Path …)` (unchanged) |
| Schema file overall structure | unchanged from v4: no outer parens, 6 positional fields | unchanged |
| Base schema | recursive self-describing in own namespace | unchanged conceptually; values cleaned up per the new rule |

## §5 Open structural questions — STILL standing from v4 §8

The v4 list of open structural questions is unaffected by v5's value-form correction. Still standing:

- **§8.1** Parser support for no-outer-parens (`.schema` parser as superset of nota-codec; lean) — needs implementation confirmation.
- **§8.2** Schema struct field count (6 is working hypothesis; alternatives 3-5 viable).
- **§8.3** Where Reply + Event live — currently in Field 5 optional-features per v4.
- **§8.4** Storage in namespace vs as feature — currently namespace per v5 (storage types like StoredRecord live in the namespace map; metadata if any goes in a feature).
- **§8.5** Owner-signal header placeholder when empty (`[]` always vs omit).
- **§8.6** File naming `<component>.schema` (lean).

Confirm any of `§8.1`-`§8.6` to land before macro library work proceeds.

## §6 New open question raised by v5

### §6.1 How does the parser distinguish struct `(fields…)` from cross-schema import `(Path …)`?

Both start with `(`. The parser disambiguates by inspecting the first identifier: `(Path …)` is a known reserved variant tag (one of the EngineAnnotation/import primitives); `(<anything-else> …)` is a struct field tuple.

Alternative: cross-schema imports get their own value-form distinct from `(Path …)` — perhaps a bracket-string `<path-to-file>` would work syntactically (the file content is interpreted as the type expected at the position), but bracket-strings are reserved for literal text per spirit 401's NOTA discipline.

**Lean: `(Path …)` as a reserved variant tag; the parser knows `Path` is the import discriminator. All other parens are struct field tuples.**

## §7 What this report supersedes

`/326-v5` SUPERSEDES `/326-v4`. This commit deletes `/326-v4` per `skills/reporting.md` v-suffix rule.

## §8 See also

- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — Spirit MVP worked-example walk
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — current canonical migration + handover state
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md` — dispatch + projection + box-form integration
- `reports/designer/320-mvp-schema-language-pilot-unblock.md` — closed-decision markers (`§2`); rest STATUS-BANNERed
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md` — schema-language v3 grammar
- `signal-persona-spirit/src/lib.rs` — current hand-written contract
- `persona-spirit/src/observation.rs` — Layer 2 hand-written today
- `persona-spirit/src/store.rs` — storage hand-written today
- `signal-sema/src/operation.rs` + `outcome.rs` — Layer 3 universal vocabulary
- `nota/example.nota` — canonical NOTA reference
- `skills/nota-design.md` — positional record + map-key + bracket-string + Path-primitive rules
- `nota-codec/tests/option_vec_struct_variant.rs`, `map_key_round_trip.rs`, `bracket_string_round_trip.rs`, `box_form.rs` — verified fixtures
- Spirit records 388-408
