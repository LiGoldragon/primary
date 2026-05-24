*Kind: Design · Topic: spirit-complete-schema-vision · Date: 2026-05-24*

# 326 — Spirit complete schema — header form revision + EnumIdentifier + base schema sketch

**Status:** v7 — absorbs psyche correction on /326-v6's header form. The engine annotation `(engine assert)` drops from the signal header (its purpose was unclear); the header carries pure variant declarations. The variant name is an **EnumIdentifier** — a NOTA-derived type that enforces unquoted PascalCase. Variant auto-promotion rule: a bare PascalCase name resolves to data-carrying if it matches a namespace entry, unit-variant otherwise. The base schema sketch at `§4` shows the recursive self-describing structure operator implements first.

## §1 The header form correction

The signal-side header (position 1 — `[…]` vector of variants) drops the `(engine X)` annotation. Each header variant is one of:

- **Bare PascalCase ident** — unit variant. Auto-promotes to data-carrying if the name matches a namespace entry.
- **`(VerbName PayloadType)`** — explicit data-carrying variant with separate verb + payload names.

Spirit's signal header per v7:

```nota
[
  (State Statement)
  (Record Entry)
  (Observe Observation)
  (Watch Subscription)
  (Unwatch SubscriptionToken)
]
```

Each variant uses the `(VerbName PayloadType)` explicit form because Spirit's verbs (State, Record, Observe, Watch, Unwatch) are CLI-meaningful operations distinct from their payload type names. The auto-promotion rule applies when a bare name matches a namespace entry — e.g., a future component could write `[Submission Query Subscription]` if its namespace declares those as payload types directly, dropping the redundant verb wrapper.

### §1.1 Where the engine mapping goes

Per psyche "I don't know what engine assert is doing there", the `(engine X)` annotation drops from the header. The Operation → SemaOperation mapping for Layer 3 bridge derivation can live in:

- **Position 5 (optional engine-mapping section)** — `{State Assert Record Assert Observe Match Watch Subscribe Unwatch Retract}` map from variant name → SemaOperation.
- **Convention** — verb-prefix-based default (Record/Submit/State → Assert; Observe/Query → Match; Watch/Subscribe → Subscribe; Unwatch/Close → Retract; Mutate/Update → Mutate; Validate/DryRun → Validate).

Lean: **convention for MVP** (matches verbs already in use); explicit engine-mapping section post-MVP if a verb name doesn't fit a convention prefix.

## §2 The EnumIdentifier NOTA derived type

Per psyche: variant names are "an unquoted string, actually... it has to be pascal case also."

A new derived NOTA type `EnumIdentifier` enforces:
- Bare unquoted token form (not wrapped in `[…]` bracket-string or `"…"` quote-string)
- PascalCase identifier (first character upper, no underscores or hyphens — `MyType` valid; `my_type` or `MyType_v2` rejected)
- Encoded as a bare PascalCase token; decoded with type-check

The macro for emitting NOTA codecs supports a `#[derive(NotaEnumIdentifier)]` (or similar) that wraps a `String` with these enforcement rules. Used by:
- Variant names in enum declarations
- Type names in namespace keys
- The component name (root enum identifier)
- All other PascalCase identifiers across the schema language

### §2.1 Why this matters

PascalCase identifiers are central to schemas + NOTA + Rust enum names. Making `EnumIdentifier` a derived type lets the parser type-check identifiers at decode time (a schema using `[State Record]` parses both as `EnumIdentifier`; using `["State" "Record"]` quote-strings fails the type-check). Catches typing mistakes early; makes the schema declaratively strict about its own naming.

The workspace's existing NOTA derivations (`NotaTransparent`, `NotaEnum`, `NotaRecord`, `NotaMapKey`, `NotaTryTransparent`) gain `NotaEnumIdentifier` as a peer.

## §3 The complete Spirit schema — v7

```nota
{
  Magnitude (Path ../signal-sema/magnitude.schema)
  SemaOperation (Path ../signal-sema/operation.schema)
  SemaOutcome (Path ../signal-sema/outcome.schema)
  SemaObservation (Path ../signal-sema/observation.schema)
}

[
  (State Statement)
  (Record Entry)
  (Observe Observation)
  (Watch Subscription)
  (Unwatch SubscriptionToken)
]

[]

[]

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

Six positional fields:
- Position 0 — meta/imports (selective cross-schema imports)
- Position 1 — signal header (Operation variants; engine annotations removed)
- Position 2 — owner-signal header (empty for Spirit)
- Position 3 — sema header (empty for Spirit; uses universal SemaOperation)
- Position 4 — namespace (type vocabulary)
- Position 5 — optional features (Reply, Event, Observable)

## §4 The base schema — `schema/base.schema` (recursive self-describing)

The schema-for-a-schema is itself a `.schema` file. Sits at `schema/base.schema` in the schema-library repo. Each component's `.schema` parser reads `base.schema` to learn what positional fields mean, then parses the component's schema.

```nota
{}

[]

[]

[]

{
  Schema (MetaImports SignalHeader OwnerHeader SemaHeader Namespace [Option OptionalFeatures])

  MetaImports ([Map EnumIdentifier Path])

  SignalHeader ([Vec HeaderVariant])
  OwnerHeader ([Vec HeaderVariant])
  SemaHeader ([Vec HeaderVariant])

  HeaderVariant [
    Unit
    (Pair EnumIdentifier EnumIdentifier)
  ]

  Namespace ([Map EnumIdentifier Declaration])

  Declaration [
    (Enum [Vec EnumVariant])
    (Struct [Vec PayloadRef])
    (Reference EnumIdentifier)
    (Import Path)
  ]

  EnumVariant [
    Unit
    (Pair EnumIdentifier PayloadRef)
    (Nested EnumIdentifier [Vec EnumVariant])
  ]

  PayloadRef [
    (Direct EnumIdentifier)
    (OptionOf EnumIdentifier)
    (VecOf EnumIdentifier)
    (MapOf EnumIdentifier EnumIdentifier)
  ]

  OptionalFeatures ([Vec Feature])

  Feature [
    (Reply [Vec EnumIdentifier])
    (Event StreamRef [Vec EnumIdentifier])
    (Observable FilterMode EnumIdentifier EnumIdentifier)
    (Storage [Vec EnumIdentifier])
  ]

  FilterMode [Default (Custom EnumIdentifier)]

  StreamRef (EnumIdentifier)

  Path (String)
  EnumIdentifier (String)
}

[]
```

### §4.1 Reading the base schema

- **Field 0 — meta/imports `{}`** — base schema imports nothing (it's the root of the language).
- **Fields 1-3 — headers all `[]`** — base schema has no wire surface (it's a library, not a component).
- **Field 4 — namespace `{…}`** — the bulk; declares every type the schema language uses.
- **Field 5 — optional features `[]`** — base has none.

The namespace's `Schema` entry declares the 6-field positional layout that every other `.schema` file conforms to. `EnumIdentifier` declares the PascalCase-unquoted-string derived type from §2. `Declaration` is the union of enum / struct / reference / import — the four value forms the namespace map accepts. `HeaderVariant` is the union of unit-variant / pair-variant — what header vectors contain.

### §4.2 The recursive self-describing property

The base schema uses ITS OWN namespace types to declare itself: `Schema` is a struct of `MetaImports + SignalHeader + ... + Namespace + OptionalFeatures` — and each of those types is defined in the same namespace map. The parser hardcodes only the entry point: ".schema files have 6 positional fields"; from there it consults `base.schema` to recursively learn what each field is.

The base schema's own declarations (Schema, HeaderVariant, Declaration, etc.) use the same forms they describe — `Kind [Variant Variant Variant]` etc. — so the base schema is parseable BY THE PARSER IT DESCRIBES. Self-bootstrapping.

## §5 The variant auto-promotion rule

When a header vector contains a bare PascalCase name (no parens):

```nota
[Statement Entry Observation Subscription SubscriptionToken]
```

The parser looks up each name in the schema's namespace:
- **Matches a namespace entry** → variant is data-carrying with that entry's type as payload.
- **No match** → variant is a unit variant (no payload).

So a component whose verbs match payload type names (a "simpler" naming convention) can use bare-name header variants:

```nota
;; Hypothetical Component X whose verbs ARE the payload types
[Submission Query State]
```

Each name resolves to the namespace entry; auto-promoted.

Spirit's header uses the EXPLICIT `(VerbName PayloadType)` form because Spirit's verbs (State, Record, Observe…) are distinct from payload type names (Statement, Entry, Observation…). Both forms coexist; the macro accepts either.

## §6 What changes from v6

| Concern | v6 | v7 |
|---|---|---|
| Signal header variant form | `(State (Statement (engine assert)))` | `(State Statement)` — engine annotation dropped per psyche |
| Engine mapping location | inside header variants | deferred — derived from verb-name convention for MVP; explicit position 6 map post-MVP if needed |
| Variant identifier type | implicit PascalCase | NEW `EnumIdentifier` NOTA derived type enforcing unquoted PascalCase |
| Variant auto-promotion | not documented | NEW §5 — bare PascalCase name auto-resolves to data-carrying if namespace has matching entry |
| Base schema example | `§3.2` had a sketch using flat declarations | NEW §4 — full sketch with proper `HeaderVariant`/`Declaration`/`EnumVariant`/`PayloadRef` union types |
| Schema file shape | unchanged from v6 | unchanged (6 positional fields, no outer parens, `.schema` extension) |
| Four value forms | vector / parens / Path / bare-ident-alias | unchanged; bare-ident form is also the auto-promotion case |

## §7 Open structural questions — consolidated

All standing questions from v4 §8 + v5 §6.1 + v6 §10 plus new from v7:

| Question | Lean | Status |
|---|---|---|
| Parser support for no-outer-parens | `.schema` parser as superset of nota-codec | open |
| Schema struct field count | 6 (meta + signal + owner + sema + namespace + optional) | open |
| Where Reply + Event live | Field 5 optional features | open |
| Storage in namespace vs feature | namespace | open |
| Empty header `[]` for unused legs | always `[]` | open |
| File naming `<component>/<component>.schema` | lean yes | open |
| Struct-vs-Path disambiguation | `Path` reserved tag | open |
| Field-name override syntax | `(field-name type)` post-MVP | open |
| UID structure | `component::namespace::type` | open |
| Library location | `nota-schema/` peer to `nota-codec` | open |
| **NEW: Where engine annotations live** | convention for MVP; explicit Position 6 map post-MVP | open |
| **NEW: `EnumIdentifier` derived type implementation** | add `#[derive(NotaEnumIdentifier)]` to nota-derive | open |
| **NEW: Variant auto-promotion rule** | bare name lookup in namespace | open |

## §8 Recommendation — STOP iterating before ratification

This is v7 of `/326` in one session. The structural shape has been corrected six times. Each iteration has been valuable (real corrections caught real bugs), but the operator can't implement against a moving target. The 13 open questions above are NOT all hard — most have clear leans I propose. What the macro library (`primary-ezqx.1`) needs to land is a STABLE structural spec.

**Strong recommendation: pause `/326` iteration; ratify the 13 questions in batch.** I can produce a "ratification batch" report that lists each question, its lean, and asks for thumbs-up / thumbs-down / alternative on each. After ratification, /326 → /326-v8 as the final spec; operator picks up `primary-ezqx.1` against that stable target.

Alternatively, if any of the leans is wrong, point at the specific one and iterate THAT — but the schema-shape's fundamental skeleton (6 fields, no outer parens, headers as vectors of variants, namespace as map, four value forms) is stable across v4-v7.

## §9 What this report supersedes

`/326-v7` SUPERSEDES `/326-v6`. This commit deletes `/326-v6` per `skills/reporting.md` v-suffix rule.

## §10 See also

- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — Spirit MVP worked-example walk
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — current canonical migration + handover state
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md` — dispatch + projection + box-form
- `reports/designer/320-mvp-schema-language-pilot-unblock.md` — closed-decision markers
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md` — schema-language v3 grammar
- `reports/second-designer/169-schema-file-shape-corrections-post-326-v3-2026-05-24.md` — second-designer's parallel corrections (anchors 433-437)
- `signal-persona-spirit/src/lib.rs` — current hand-written contract
- `signal-sema/src/operation.rs` + `outcome.rs` — Layer 3 universal vocabulary
- `nota/example.nota` — canonical NOTA reference
- `nota-codec/tests/*` — verified fixtures (map, bracket-string, box-form all landed)
- `skills/nota-design.md` — positional record + map-key + bracket-string + Path-primitive rules
- Spirit records 388-437 (433-437 captured by second-designer per /169 — header form + selective imports + enum-or-vector preference)
