*Kind: Design · Topic: spirit-complete-schema-vision · Date: 2026-05-24*

# 326 — Spirit complete schema — import-as-distinct-variants

**Status:** v9 — corrects v8's import shape. NOTA has no optional fields; variant arity must be fixed. v8 had `(Path file)` and `(Path file [names…])` sharing the `Path` tag with different arity — not allowed. v9 uses two distinct variants: `(ImportAll Path)` for whole-namespace import + `(Import Path [Vec EnumIdentifier])` for selective. Per psyche: "Path is too obscure. It's like Import or ImportAll." The imports map is a key-map of these tagged variants.

## §1 The corrected imports shape

```nota
{
  Magnitude (ImportAll ./signal-sema/magnitude.schema)
  SemaSet (Import ./signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])
}
```

Two variants of the `ImportDirective` enum the import-map's value position takes:

| Variant | Fields | Meaning |
|---|---|---|
| `(ImportAll Path)` | 1 field | import EVERYTHING from the schema at `Path` |
| `(Import Path [Vec EnumIdentifier])` | 2 fields | import ONLY the named types from the schema at `Path` |

Each variant has FIXED arity. The map key (`Magnitude`, `SemaSet`) is the local group label; imported names go directly into the local namespace.

A future third variant could be `(FromIndex IndexName)` for index-based imports (when a schema registry/index exists per spirit 397's schema-daemon work). MVP needs only the first two.

## §2 The `ImportDirective` declaration in the base schema namespace

```nota
ImportDirective [
  (Import Path [Vec EnumIdentifier])
  (ImportAll Path)
]
```

Standard enum declaration form: `[…]` vector containing two parenthesized data-carrying variants with fixed arities. Lives in the base schema (`schema/base.schema`) namespace; every component's `.schema` parser knows the type because the base schema declares it.

## §3 The complete Spirit schema — v9

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

### §3.1 Reading the imports

`Magnitude (ImportAll ../signal-sema/magnitude.schema)` — pulls the WHOLE namespace from `magnitude.schema`. The local key `Magnitude` is the group label (also happens to be the name of the type being imported, since magnitude.schema only declares one type).

`SemaSet (Import ../signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])` — pulls the three named types selectively. The local key `SemaSet` is a group label naming this bundle of imports; the imported types are referenceable directly as `SemaOperation`, `SemaOutcome`, `SemaObservation` in the namespace.

The schema-daemon (per spirit 397 + /326-v8 §4) resolves both forms and produces the lowered binary schema with all imports inlined.

## §4 What changes from v8

| Concern | v8 | v9 |
|---|---|---|
| Import shape | `(Path file)` and `(Path file [names…])` — same tag, different arity (INVALID per NOTA) | two distinct variants: `(ImportAll Path)` (1 field) + `(Import Path [Vec EnumIdentifier])` (2 fields) |
| Variant name | `Path` (psyche: "too obscure") | `Import` and `ImportAll` (psyche: "It's like Import or ImportAll") |
| `AllOrSome` derived type | introduced in v8 | retired — replaced by two distinct variants per fixed-arity rule |
| Future expansion | `(Path file [optional names])` ambiguous | clean: add `(FromIndex IndexName)` etc. as new variant when needed |
| Header form (Form 1 + Form 2) | unchanged from v8 | unchanged |
| Schema-daemon role (§4 in v8) | unchanged | unchanged |
| Field count (6 positional) | unchanged | unchanged |
| Spirit's actual content | unchanged | unchanged (only imports section's syntax changes) |

The `AllOrSome` type from v8 was an attempt to capture "default all; specify some". Per psyche's correction, NOTA doesn't have optional fields, so the same effect is achieved with TWO DISTINCT VARIANTS instead of one variant with an optional field.

## §5 Standing open structural questions

Same as v8 §6 with one removal + one rename:

| Question | Lean | Status |
|---|---|---|
| Parser support for no-outer-parens | `.schema` parser as superset of nota-codec | open |
| Schema struct field count (6) | meta + signal + owner + sema + namespace + optional | open |
| Where Reply + Event live | Field 5 optional features | open |
| Storage in namespace vs feature | namespace | open |
| Empty header `[]` for unused legs | always `[]` | open |
| File naming `<component>/<component>.schema` | lean yes | open |
| Struct-vs-`Import`/`ImportAll` disambiguation | `Import`/`ImportAll` reserved tags | open |
| Field-name override syntax | `(field-name type)` post-MVP | open |
| UID structure | `component::namespace::type` | open |
| Library location | `nota-schema/` peer to `nota-codec` | open |
| Engine annotations location | convention for MVP; explicit Position 6 post-MVP | open |
| `EnumIdentifier` implementation | `#[derive(NotaEnumIdentifier)]` in nota-derive | open |
| Variant auto-promotion rule | bare name → namespace lookup → data-carrying or unit | open |
| Form 1 vs Form 2 trigger | sub-enum only when >1 sub-variant | open |
| `ImportDirective` variants | `Import` + `ImportAll`; future `FromIndex` | open |
| Schema daemon stores lowered form | per spirit 397-400 | open |

## §6 What this report supersedes

`/326-v9` SUPERSEDES `/326-v8`. This commit deletes `/326-v8` per `skills/reporting.md` v-suffix rule.

## §7 See also

- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md`
- `reports/designer/320-mvp-schema-language-pilot-unblock.md`
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
- `reports/second-designer/169-schema-file-shape-corrections-post-326-v3-2026-05-24.md`
- `signal-persona-spirit/src/lib.rs`
- `signal-sema/src/operation.rs` + `outcome.rs`
- `nota/example.nota`
- `nota-codec/tests/*`
- `skills/nota-design.md`
- Spirit records 388-437
