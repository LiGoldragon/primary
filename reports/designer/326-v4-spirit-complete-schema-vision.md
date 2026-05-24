*Kind: Design · Topic: spirit-complete-schema-vision · Date: 2026-05-24*

# 326 — Spirit complete schema — header-first, no-outer-parens

**Status:** v4 — absorbs psyche feedback on /326-v3's outer parens + Schema tag. Schema files have **no outer parens**: the file IS the struct, the parser knows that because it's a `.schema` file (extension rename from `.nota`). First positional field is the **header** — a vector of variants describing the signal-side root enum (Operation), driving header-byte-0 dispatch. The shape continues positionally per the base schema's `Schema` struct definition. Several structural questions are still open and listed at `§8` for ratification before the macro library work proceeds.

## §1 The data type inventory — unchanged from v3

Three layers + storage:

- **Layer 1 wire** — 5 Operation verbs + 2 macro-injected; 10 Reply variants; 2 Event variants; 4 leaf enums; 11 newtypes; 9 composites; root payloads + tokens + observable payloads.
- **Layer 2 daemon-private** — `Command` (12 variants), `Effect` (10 variants), `RecordObservation`.
- **Layer 3 sema** — `SemaOperation` / `SemaOutcome` / `SemaObservation` / `Magnitude` (cross-schema from `signal-sema`).
- **Storage** — `StoredRecord`, `StampedEntry`, `RecordIdentifierMint`.

## §2 The Spirit schema — `signal-persona-spirit/spirit.schema`

### §2.1 The file

The file extension is `.schema` per psyche directive — it's a special node format, distinct from regular `.nota` data files. The file content begins with the FIRST positional field of the schema struct — NO outer parens. The parser knows the file's type because of the `.schema` extension; it parses positionally per the base schema's struct definition.

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
  Kind (Kind Decision Principle Correction Clarification Constraint)
  ObservationMode (ObservationMode SummaryOnly WithProvenance)
  Presence (Presence Active Absent)
  UnimplementedReason (UnimplementedReason NotBuiltYet IntegrationNotLanded)

  Topic (Topic String)
  Summary (Summary String)
  Context (Context String)
  Quote (Quote String)
  StatementText (StatementText String)
  FocusArea (FocusArea String)
  RecordIdentifier (RecordIdentifier u64)
  QuestionIdentifier (QuestionIdentifier String)
  QuestionText (QuestionText String)
  StateSubscriptionToken (StateSubscriptionToken u64)
  RecordSubscriptionToken (RecordSubscriptionToken u64)

  Entry (Entry Topic Kind Summary Context Magnitude Quote)
  Statement (Statement StatementText)
  RecordQuery (RecordQuery [Option Topic] [Option Kind] ObservationMode)
  RecordSubscription (RecordSubscription [Option Topic] ObservationMode)
  RecordSummary (RecordSummary RecordIdentifier Topic Kind Summary Magnitude)
  RecordProvenance (RecordProvenance RecordSummary Context Date Time Quote)
  TopicCount (TopicCount Topic u64)
  State (State Presence [Option FocusArea])
  QuestionSummary (QuestionSummary QuestionIdentifier QuestionText)

  RecordObservation (RecordObservation RecordQuery)

  Observation (Observation State (Records RecordQuery) Topics Questions)
  Subscription (Subscription State (Records RecordSubscription))
  SubscriptionToken (SubscriptionToken (State StateSubscriptionToken) (Records RecordSubscriptionToken))

  StoredRecord (StoredRecord RecordIdentifier StampedEntry)
  StampedEntry (StampedEntry Entry Date Time)
  RecordIdentifierMint (RecordIdentifierMint u64)

  RecordAccepted (RecordAccepted RecordIdentifier)
  StateObserved (StateObserved State)
  RecordsObserved (RecordsObserved [Vec RecordSummary])
  RecordProvenancesObserved (RecordProvenancesObserved [Vec RecordProvenance])
  TopicsObserved (TopicsObserved [Vec TopicCount])
  QuestionsObserved (QuestionsObserved [Vec QuestionSummary])
  SubscriptionOpened (SubscriptionOpened SubscriptionToken SubscriptionSnapshot)
  SubscriptionRetracted (SubscriptionRetracted SubscriptionToken)
  RequestUnimplemented (RequestUnimplemented UnimplementedReason)
  SubscriptionSnapshot (SubscriptionSnapshot (State State) (Records [Vec RecordSummary]))

  StateChanged (StateChanged State)
  RecordCaptured (RecordCaptured RecordSummary)

  OperationReceived (OperationReceived OperationKind)
  EffectEmitted (EffectEmitted SemaObservation)
}

[
  (Reply
    (RecordAccepted RecordAccepted)
    (StateObserved StateObserved)
    (RecordsObserved RecordsObserved)
    (RecordProvenancesObserved RecordProvenancesObserved)
    (TopicsObserved TopicsObserved)
    (QuestionsObserved QuestionsObserved)
    (SubscriptionOpened SubscriptionOpened)
    (SubscriptionRetracted SubscriptionRetracted)
    (RequestUnimplemented RequestUnimplemented))

  (Event
    (StateChanged (StateChanged belongs DomainStream))
    (RecordCaptured (RecordCaptured belongs DomainStream)))

  (Observable
    (filter default)
    (operation_event OperationReceived)
    (effect_event EffectEmitted))
]
```

### §2.2 Reading the positional fields

| Position | Type | Spirit's content |
|---|---|---|
| 0 | signal header | vector of 5 Operation variants (the wire-side root header that drives byte-0 dispatch) |
| 1 | owner-signal header | empty vector `[]` — Spirit's owner contract is minimal/none |
| 2 | sema header | empty vector `[]` — Spirit doesn't add to the universal SemaOperation set; engine annotations carry the mapping |
| 3 | imports | map of selective cross-schema imports |
| 4 | namespace | map of type-name → declaration (all Layer 1 + Layer 2 + storage types) |
| 5 | optional features | vector of variant options (Reply types, Event types, Observable block) |

The base schema defines these positions; the file fills them in. Empty fields use `[]` (empty vector) or `{}` (empty map) as natural NOTA empty containers.

### §2.3 The header is a vector of variants

The first field is a **vector of variants** — each element is a `(VariantName Payload)` record or a bare PascalCase token for unit variants. This vector IS the wire-side Operation enum; the byte-0 of the short header is the variant's positional index in this vector. Receiver dispatches by matching header byte-0 against the variant arms — header action like drop/keep/route without reading the body.

Per psyche directive — up to 7 data-carrying variants because the 64-bit short header packs 1 root byte + 7 sub-enum slots (per spirit 388 + 392). The actual maximum per-component is `100 / 156` per the golden-ratio split (spirit 327), but the practical Operation count for most components is well under 10.

### §2.4 Vectors of variants are the canonical structure

Per psyche directive: "We love enums." The schema prefers vectors-of-variants over maps. Maps are used ONLY for the namespace (which IS a name → declaration mapping) and the imports (also a name → path mapping). Everything else uses vectors-of-variants or positional records. `True` / `False` are PascalCase (2-unit-variant Bool enum); positions are inherent in vectors; data-carrying variants use `(VariantName payload)`, unit variants use bare PascalCase tokens.

## §3 The schema-for-a-schema — unchanged concept from v3

The base schema lives at `nota/spirit.schema` (or whatever the canonical name is). It declares `Schema`'s positional layout (6 fields per `§2.2`), the types each field can take, the `Declaration` union (Inline | Cross-via-Path), `Path` as a primitive, etc. The schema-for-a-schema is itself a schema file in NOTA format, defined in terms of its own namespace types — self-describing.

### §3.1 What changes in the base schema

v3's base schema declared `Schema (Schema ChannelBlock NamespaceMap)`. v4's base schema declares Schema as a 6-field positional struct:

```nota
;; nota/spirit.schema — base schema-for-a-schema
;; (using v4 form: no outer parens; the file's contents ARE the Schema struct)

[]

[]

[]

{}

{
  Schema (Schema SignalHeader OwnerHeader SemaHeader Imports Namespace OptionalFeatures)
  SignalHeader ([Vec OperationVariant])
  OwnerHeader ([Vec OperationVariant])
  SemaHeader ([Vec SemaVariant])
  Imports ([Map Identifier Path])
  Namespace ([Map Identifier Declaration])
  OptionalFeatures ([Vec FeatureVariant])

  OperationVariant
    (OperationVariant Identifier PayloadRef EngineAnnotation)

  Declaration
    (Inline TaggedRecord)
    (Cross Path)

  TaggedRecord (TaggedRecord Identifier [Vec FieldOrVariant])

  FieldOrVariant
    (Field Identifier)
    (Variant Identifier [Option PayloadRef])

  PayloadRef (PayloadRef Identifier)

  EngineAnnotation
    Assert
    Mutate
    Retract
    Match
    Subscribe
    Validate

  FeatureVariant
    (Reply [Vec ReplyVariant])
    (Event [Vec EventVariant])
    (Observable ObservableDecl)
    (Storage [Vec StorageDecl])

  ReplyVariant (ReplyVariant Identifier Identifier)
  EventVariant (EventVariant Identifier Identifier StreamRef)
  ObservableDecl (ObservableDecl FilterMode OperationEventRef EffectEventRef)
  StorageDecl (StorageDecl Identifier TaggedRecord)

  FilterMode
    Default
    (Custom Identifier)

  StreamRef (StreamRef Identifier)

  Identifier (Identifier String)
  Path (Path PathPrimitive)
  PathPrimitive (PathPrimitive String)
}

[]
```

The base schema's:
- Field 0-2 (headers): empty (base schema isn't a component)
- Field 3 (imports): empty
- Field 4 (namespace): the bulk — declares the schema-language's own vocabulary
- Field 5 (optional features): empty (base schema has no Reply/Event/Observable/Storage features)

## §4 Selective imports — Field 3

The Imports field uses a map keyed by the **local name to bind** to the imported type. Per psyche directive on selectivity:

```nota
{
  Magnitude (Path ../signal-sema/magnitude.schema)
}
```

This imports only `Magnitude` from `signal-sema`, binding it under the local name `Magnitude`. To rename on import: `LocalName (Path ../other/whatever.schema)` where `LocalName` is the local binding.

For Spirit, the imports field pulls in `Magnitude`, `SemaOperation`, `SemaOutcome`, `SemaObservation` from `signal-sema`. Other types come from Spirit's own namespace (Field 4).

This keeps concerns separate: a component only imports what it actually uses; namespace clashes with universal vocabulary (Magnitude) are explicit via the import.

## §5 The sema-message namespace bridge — unchanged from v3

`(engine X)` annotations on Field 0 (signal header) variants encode the bridge. Macro derives Command + Effect + ToSemaOperation + ToSemaOutcome.

For Spirit's verbs at Field 0: `(State (Statement (engine assert)))` → `Command::ClassifyStatement(Statement)` + `SemaOperation::Assert`. Etc. — same mapping as v3 §4.1.

## §6 Storage — Field 5 optional feature

Storage types live in Field 5's optional-features vector as a `(Storage …)` variant:

```nota
(Storage
  (StoredRecord (StoredRecord RecordIdentifier StampedEntry))
  (StampedEntry (StampedEntry Entry Date Time))
  (RecordIdentifierMint (RecordIdentifierMint u64)))
```

OR storage types could live in the namespace (Field 4) since they're just types. The optional-features Storage variant might carry metadata (table names, redb options) the namespace declarations don't naturally hold.

Open question per `§8.4`.

## §7 What changes from v3

| Concern | v3 | v4 |
|---|---|---|
| Outer wrapping | `(…)` outer parens with no tag | NO outer parens; file content IS the struct |
| File extension | `.nota` | `.schema` (per psyche directive — schema files are a special format) |
| First field | inner record `((Operation …) (Reply …) (Event …) (Observable …))` | vector `[(State …) (Record …) …]` — the signal-side header alone |
| Reply/Event/Observable | inside the first field as sub-records | moved to Field 5 (optional features) — they're outputs/streaming/observability, not the header that drives dispatch |
| Headers count | 1 (combined Operation/Reply/Event/Observable in `Channel` record) | 3 separate header fields (signal, owner-signal, sema) |
| Selective imports | no separate field; cross-schema refs mixed in the namespace | separate Field 3 imports map — selective + explicit |
| Schema struct definition | 2-field (channel + namespace) | 6-field (3 headers + imports + namespace + optional features) |
| Base schema concept | unchanged | unchanged — still recursive self-describing in its own namespace |

## §8 Open structural questions

The v4 form raises several structural questions where I should NOT guess further without psyche ratification. Each affects the base schema's struct definition and what positional fields the file carries.

### §8.1 Does NOTA support no-outer-parens parsing?

Per psyche: schema files have no outer parens because the file IS the struct (the parser knows from the `.schema` extension). Mechanically: the parser would need to read multiple top-level values from the file and bundle them into the implicit Schema struct. Today's nota-codec expects ONE root value per file (per `nota/example.nota` form). Three possible implementations:
- (a) `.schema` parser is a SUPERSET of nota-codec that strips/adds the outer parens.
- (b) nota-codec gains a multi-root reader mode for `.schema` files.
- (c) Files DO have outer parens but they're "implicit" — operator writes the parens but parser doesn't require them.

Lean: (a) — the schema parser is its own layer atop nota-codec, with the implicit-struct convention built in. Operator verifies first.

### §8.2 What positional fields does Schema have?

`§2.2` proposes 6 fields: signal-header, owner-header, sema-header, imports, namespace, optional-features. Alternatives:
- 3-field (combined headers, imports + namespace + optional)
- 4-field (signal-header, owner-header, namespace, optional)
- 5-field (signal-header, owner-header, sema-header, namespace, optional; no imports — imports merge into namespace)

The right shape depends on what's truly "header" (dispatch-driving) vs "namespace" vs "feature". Lean: 6-field is most explicit, but adds positions that may be empty for simple components. Confirm.

### §8.3 Where do Reply + Event live?

v4 puts Reply + Event in the Field 5 optional-features vector (as variants `(Reply …)` and `(Event …)`). Alternatives:
- They go in the namespace (just type declarations) — and the channel's Reply/Event surface is implicit from naming.
- They go in additional positional fields (one per output kind).
- They go in the signal-header itself somehow.

Reply + Event ARE part of the wire-side contract, just not dispatch-driving. Where best to declare?

### §8.4 Storage in namespace or as feature?

`§6` waffles. Storage types are just types (could live in namespace). But storage carries METADATA (table name, redb options) that's daemon-side not wire-side. Lean: optional feature with `(Storage (StoredRecord …) (TableName records) …)` so the metadata stays with the storage declarations.

### §8.5 Owner-signal as a separate header in Spirit's schema?

Spirit's owner contract is mostly empty today (per /322 + the deployed code — Spirit has no `owner-signal-persona-spirit` ops landed). So Field 1 is `[]`. But should the schema file even HAVE a Field 1 placeholder if it's always empty? Lean: yes — base schema's positional layout is universal; empty is `[]`.

### §8.6 Naming convention for the file

Per psyche: `.schema` extension. The file's NAME (before the extension):
- `signal-persona-spirit/spirit.schema` (lean per psyche's framing — "a .schema is a special-format node")
- OR `signal-persona-spirit/schema.nota` (current /322 + previous v1/v2/v3 form)
- OR just `signal-persona-spirit/.schema` (extension-only)

Lean: `<component>/<component>.schema` at the repo root — explicit + unambiguous.

## §9 What I'm NOT changing pending ratification

Until `§8`'s questions are answered, the following stay flexible:
- The exact positional count of Schema's fields (6 is the working hypothesis).
- Whether Reply/Event live as features or as namespace entries.
- How owner-signal headers integrate when a component has them.
- The base schema's exact name + location (`nota/spirit.schema` is a placeholder).

## §10 What this report supersedes

`/326-v4` SUPERSEDES `/326-v3`. This commit deletes `/326-v3` per `skills/reporting.md` v-suffix rule.

## §11 See also

- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — Spirit MVP worked-example walk
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — current canonical migration + handover state
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md` — dispatch + projection + box-form integration
- `reports/designer/320-mvp-schema-language-pilot-unblock.md` — closed-decision markers (`§2`); rest STATUS-BANNERed
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md` — schema-language v3 grammar
- `reports/second-designer/163-signal-sema-interaction-and-spirit-architecture-2026-05-24.md` — three-layer model
- `signal-persona-spirit/src/lib.rs` — current hand-written contract
- `persona-spirit/src/observation.rs` — Layer 2 hand-written today
- `persona-spirit/src/store.rs` — storage hand-written today
- `signal-sema/src/operation.rs` + `outcome.rs` — Layer 3 universal vocabulary
- `nota/example.nota` — canonical NOTA reference (note: nota files have outer parens; `.schema` files per psyche may not)
- `skills/nota-design.md` — positional record + map-key + bracket-string + Path-primitive rules
- `nota-codec/tests/option_vec_struct_variant.rs`, `map_key_round_trip.rs`, `bracket_string_round_trip.rs`, `box_form.rs` — verified fixtures
- Spirit records 388-408
