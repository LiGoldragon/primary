*Kind: Design · Topic: spirit-complete-schema-vision · Date: 2026-05-24*

# 326 — Spirit complete schema — container types use parens

**Status:** v10 — corrects v9's `[Vec X]` / `[Option X]` container-type syntax. Per psyche: `Option` is an enum; type expressions use parens (record form), not brackets (which are for value sequences). So `Option<Topic>` written as a type expression is `(Option Topic)`. Brackets `[…]` stay for: value-form Vec instances on the wire, enum-variant declarations in namespace values, and header vectors. Parens `(…)` for: struct fields, type expressions like `(Vec X)` / `(Option X)`, data-carrying variants.

## §1 The correction

In schema TYPE-EXPRESSION positions (e.g., struct field types), container constructors use parens:

| Type | v9 (wrong) | v10 (correct) |
|---|---|---|
| Option<Topic> | `[Option Topic]` | `(Option Topic)` |
| Vec<RecordSummary> | `[Vec RecordSummary]` | `(Vec RecordSummary)` |
| Map<K, V> (if any) | `[Map K V]` | `(Map K V)` |

The distinction:
- **Brackets `[…]`** = value-form sequence (on the wire: `[v1 v2 v3]` is a Vec) OR enum-variant declaration (in namespace: `Kind [Decision Principle …]`)
- **Parens `(…)`** = record (struct fields, data-carrying variants, type expressions)

A `(Vec Topic)` in a field-type position is the TYPE expression "Vec of Topic"; the WIRE VALUE for that field would be `[t1 t2 t3]`. Different positions; different syntax.

## §2 The complete Spirit schema — v10

```nota
{
  Magnitude (ImportAll ../signal-sema/magnitude.schema)
  SemaSet (Import ../signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])
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
  RecordQuery ((Option Topic) (Option Kind) ObservationMode)
  RecordSubscription ((Option Topic) ObservationMode)
  RecordSummary (RecordIdentifier Topic Kind Summary Magnitude)
  RecordProvenance (RecordSummary Context Date Time Quote)
  TopicCount (Topic u64)
  State (Presence (Option FocusArea))
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
  RecordsObserved ((Vec RecordSummary))
  RecordProvenancesObserved ((Vec RecordProvenance))
  TopicsObserved ((Vec TopicCount))
  QuestionsObserved ((Vec QuestionSummary))
  SubscriptionOpened (SubscriptionToken SubscriptionSnapshot)
  SubscriptionRetracted (SubscriptionToken)
  RequestUnimplemented (UnimplementedReason)
  SubscriptionSnapshot [(State State) (Records (Vec RecordSummary))]

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

## §3 Reading the container-type fixes

- `RecordQuery ((Option Topic) (Option Kind) ObservationMode)` — RecordQuery is a 3-field struct: first field is `Option<Topic>` (type expression in parens), second is `Option<Kind>`, third is `ObservationMode` (bare name reference).
- `RecordsObserved ((Vec RecordSummary))` — RecordsObserved is a 1-field struct whose single field is `Vec<RecordSummary>`. The OUTER parens are the struct wrapper; the INNER `(Vec RecordSummary)` is the field's type expression.
- `State (Presence (Option FocusArea))` — State is a 2-field struct: first field is `Presence` (enum reference), second is `Option<FocusArea>`.
- `SubscriptionSnapshot [(State State) (Records (Vec RecordSummary))]` — SubscriptionSnapshot is an enum with two data-carrying variants: `(State State)` carrying a State value, `(Records (Vec RecordSummary))` carrying a Vec<RecordSummary>.

The pattern is consistent: `(Vec X)` and `(Option X)` are TYPE EXPRESSIONS used anywhere a type is expected (field positions, variant payloads, etc.).

## §4 The import shape — still v9's two-variant form

The imports field unchanged from v9:

```nota
{
  Magnitude (ImportAll ../signal-sema/magnitude.schema)
  SemaSet (Import ../signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])
}
```

Two distinct variants `(Import Path [Vec EnumIdentifier])` + `(ImportAll Path)` with fixed arity. Operator's /173 used `((Path X) AllOrSome)` — semantically equivalent but structurally different layering. Either form works; psyche's "Path too obscure" comment favors v9's variant naming.

If we pivot to operator's form, the imports would read:
```nota
{
  Magnitude ((Path ../signal-sema/magnitude.schema) All)
  SemaSet ((Path ../signal-sema/operation.schema) (Some [SemaOperation SemaOutcome SemaObservation]))
}
```

Open for psyche ratification per operator's /173 surface.

## §5 What changes from v9

| Concern | v9 | v10 |
|---|---|---|
| `Option<T>` in type position | `[Option T]` | `(Option T)` |
| `Vec<T>` in type position | `[Vec T]` | `(Vec T)` |
| `Map<K, V>` in type position (hypothetical) | `[Map K V]` | `(Map K V)` |
| Brackets in value-form sequences | unchanged: `[Decision Principle …]` etc. | unchanged |
| Brackets in enum-variant declarations | unchanged: `Kind [Variant Variant …]` | unchanged |
| Brackets in header vector | unchanged: `[(State Statement) (Record Entry) …]` | unchanged |
| Parens in struct fields | unchanged: `Topic (String)` | unchanged |
| Parens in data-carrying variants | unchanged: `(Records RecordQuery)` | unchanged |
| Import shape | two distinct variants | unchanged (open to pivot per operator/173) |

## §6 The bracket-vs-paren rule, sharpened

| Syntactic position | `[…]` brackets | `(…)` parens |
|---|---|---|
| Header vector (Position 1) | the vector itself | data-carrying variants inside |
| Namespace map value | enum-variant declaration | struct fields OR (Path …) import OR type expression |
| Inside a struct's field list | enum-variant sub-declaration (rare; mostly type refs) | data-carrying variant payload OR `(Vec X)` / `(Option X)` type expression |
| Inside a variant payload | sub-enum (Form 2 header) | nested struct OR type expression |
| Selective import names list | `[Name1 Name2 …]` — the list of names | not used here |
| At wire value-form decode time | `[v1 v2 v3]` — Vec value | (record / variant / struct value) |

Generalised rule: **brackets are for OPEN LISTS (one-or-more homogeneous things); parens are for FIXED-ARITY tuples (positional, possibly tagged)**. Type expressions like `(Vec X)` and `(Option X)` use parens because they're fixed-arity (2 positions: constructor + type parameter).

## §7 Standing open questions

Same as v9 with one resolved:

| Question | Lean | Status |
|---|---|---|
| Parser support for no-outer-parens | `.schema` parser as superset of nota-codec | open |
| Schema struct field count (6) | meta + signal + owner + sema + namespace + optional | open |
| Where Reply + Event live | Field 5 optional features | open |
| Storage in namespace vs feature | namespace | open |
| Empty header `[]` for unused legs | always `[]` | open |
| File naming `<component>/<component>.schema` | lean yes | open |
| Struct-vs-`Import`/`ImportAll` disambiguation | reserved tags | open |
| Field-name override syntax | `(field-name type)` post-MVP | open |
| UID structure | `component::namespace::type` | open |
| Library location | `nota-schema/` peer to `nota-codec` | open |
| Engine annotations location | convention for MVP | open |
| `EnumIdentifier` implementation | `#[derive(NotaEnumIdentifier)]` | open |
| Variant auto-promotion rule | bare name → namespace lookup | open |
| Form 1 vs Form 2 trigger | sub-enum only when >1 sub-variant | open |
| Import shape: variants vs `(Path X) AllOrSome` | v9's variants (lean) vs operator/173's outer-record-with-selector | OPEN — pick per psyche |
| Schema daemon stores lowered form | per spirit 397-400 + operator/173 SchemaMid example | open |
| **NEW: Form 2 nested depth — data-carrying sub-variants allowed?** | per operator/173: lean header-unit-only at nested level; complex data lives in body | open |
| **NEW: Container types use parens not brackets** | RESOLVED — `(Vec X)` `(Option X)` per v10 §1 | **closed** |

## §8 What this report supersedes

`/326-v10` SUPERSEDES `/326-v9`. This commit deletes `/326-v9` per `skills/reporting.md` v-suffix rule.

## §9 See also

- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md`
- `reports/designer/320-mvp-schema-language-pilot-unblock.md`
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
- `reports/second-designer/169-schema-file-shape-corrections-post-326-v3-2026-05-24.md`
- `reports/operator/173-schema-header-namespace-and-import-example-2026-05-24.md` — parallel substance + spirit 477-480 + SchemaMid lowered example + Form 2 nested-depth question
- `signal-persona-spirit/src/lib.rs`
- `signal-sema/src/operation.rs` + `outcome.rs`
- `nota/example.nota`
- `nota-codec/tests/*`
- `skills/nota-design.md`
- Spirit records 388-480
