*Kind: Design · Topic: spirit-complete-schema-vision · Date: 2026-05-24*

# 326 — Spirit complete schema — uniform `(VerbName [sub-variants])` form

**Status:** v13 — absorbs psyche correction: header variants ALWAYS use the vector form `(VerbName [sub-variants])`, even when there's only one sub-variant. Unifies the prior Form 1 / Form 2 distinction into ONE uniform shape. Spirit schema shown with rich multi-variant headers throughout — each root operation has 2-5 sub-variants per the psyche's request for "examples with many variants." Namespace body declarations match header route names via the architectural seam from operator/174.

## §1 The uniform header form

```nota
(VerbName [sub-variant1 sub-variant2 …])
```

**Rule:** every header variant is parenthesized + carries a bracket-vector of sub-variants. Vector always present, even for single sub-variant. Sub-variants are bare PascalCase tokens; each auto-promotes to data-carrying via namespace lookup (per `/326-v8 §5` auto-promotion rule).

**Wire encoding:**
- byte 0 of short header = root variant discriminator (`State` / `Record` / `Observe` / etc.)
- byte 1 of short header = sub-variant discriminator within the root's sub-namespace
- For single-sub-variant case, byte 1 = 0 (trivially)
- For multi-sub-variant case, byte 1 selects among the listed sub-variants

**No more Form 1 vs Form 2** — there's only ONE form. The "single payload" case is just `(VerbName [SinglePayload])` — one-element vector. The "sub-enum" case is just `(VerbName [Sub1 Sub2 Sub3])` — multi-element vector. Same shape; different cardinality.

## §2 Spirit schema with rich multi-variant headers

```nota
{
  Magnitude (ImportAll ../signal-sema/magnitude.schema)
  SemaSet (Import ../signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])
}

[
  (State [Utterance Declaration Reflection])
  (Record [Entry Provenance Snapshot])
  (Observe [Self Records Topics Questions])
  (Watch [Self Records Questions])
  (Unwatch [Self Records Questions])
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
  QuestionSubscriptionToken (u64)

  Utterance (Topic StatementText)
  Declaration (Topic Kind Magnitude StatementText)
  Reflection (Topic Quote StatementText)

  Entry (Topic Kind Summary Context Magnitude Quote)
  Provenance (RecordIdentifier Date Time Context Quote)
  Snapshot (Presence (Option FocusArea) Date Time)

  RecordQuery ((Option Topic) (Option Kind) ObservationMode)
  RecordSubscription ((Option Topic) ObservationMode)
  QuestionQuery ((Option QuestionIdentifier) ObservationMode)
  QuestionSubscription ((Option QuestionIdentifier) ObservationMode)
  TopicQuery (ObservationMode)
  StateQuery (ObservationMode)
  StateSubscription (ObservationMode)

  State (Presence (Option FocusArea))
  RecordSummary (RecordIdentifier Topic Kind Summary Magnitude)
  RecordProvenance (RecordSummary Context Date Time Quote)
  TopicCount (Topic u64)
  QuestionSummary (QuestionIdentifier QuestionText)

  StoredRecord (RecordIdentifier StampedEntry)
  StampedEntry (Entry Date Time)
  RecordIdentifierMint (u64)

  State [
    (Utterance Utterance)
    (Declaration Declaration)
    (Reflection Reflection)
  ]

  Record [
    (Entry Entry)
    (Provenance Provenance)
    (Snapshot Snapshot)
  ]

  Observe [
    (Self StateQuery)
    (Records RecordQuery)
    (Topics TopicQuery)
    (Questions QuestionQuery)
  ]

  Watch [
    (Self StateSubscription)
    (Records RecordSubscription)
    (Questions QuestionSubscription)
  ]

  Unwatch [
    (Self StateSubscriptionToken)
    (Records RecordSubscriptionToken)
    (Questions QuestionSubscriptionToken)
  ]

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

  SubscriptionToken [
    (Self StateSubscriptionToken)
    (Records RecordSubscriptionToken)
    (Questions QuestionSubscriptionToken)
  ]
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

### §2.1 What changed in the example

Spirit's header was previously single-variant per root; v13 shows it with multiple sub-variants:

| Root | Sub-variants | Body declarations (in namespace under same root name) |
|---|---|---|
| `(State [Utterance Declaration Reflection])` | 3 statement kinds | `State [(Utterance Utterance) (Declaration Declaration) (Reflection Reflection)]` |
| `(Record [Entry Provenance Snapshot])` | 3 record types | `Record [(Entry Entry) (Provenance Provenance) (Snapshot Snapshot)]` |
| `(Observe [Self Records Topics Questions])` | 4 observation targets | `Observe [(Self StateQuery) (Records RecordQuery) (Topics TopicQuery) (Questions QuestionQuery)]` |
| `(Watch [Self Records Questions])` | 3 subscription targets | `Watch [(Self StateSubscription) (Records RecordSubscription) (Questions QuestionSubscription)]` |
| `(Unwatch [Self Records Questions])` | 3 unsubscription targets | `Unwatch [(Self StateSubscriptionToken) (Records RecordSubscriptionToken) (Questions QuestionSubscriptionToken)]` |

The architectural seam (per operator/174 + v11): header `State` and namespace `State` are different parser objects sharing a name; lowering connects them. Same for Record/Observe/Watch/Unwatch.

### §2.2 Why this is richer than Spirit's MVP today

Spirit's deployed contract today has each operation carrying a SINGLE payload type. This v13 example shows what a richer schema looks like — each header root has 2-5 sub-variants, each with its own body shape in the namespace. Wire-side: byte 0 selects the root operation (State/Record/Observe/Watch/Unwatch); byte 1 selects the sub-variant within the root's namespace.

**For Spirit MVP**, the actual schema would use single-element vectors:

```nota
[
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
  (Watch [Subscription])
  (Unwatch [SubscriptionToken])
]
```

With matching namespace:

```nota
{
  State [(Statement Statement)]
  Record [(Entry Entry)]
  Observe [(Observation Observation)]
  Watch [(Subscription Subscription)]
  Unwatch [(SubscriptionToken SubscriptionToken)]
  ;; ... Statement, Entry, Observation, etc. declared elsewhere in namespace
}
```

This is the SAME form — vector with 1 element — and the lowering produces the same wire shape (byte 0 = root, byte 1 = 0 since single sub-variant). Operator's v10/v11/v12 simpler `(State Statement)` form COLLAPSES into v13's uniform `(State [Statement])`; the difference is just whether the vector wrapper appears for single-sub-variant cases.

The richer multi-variant example above is what Spirit COULD evolve toward as the design matures.

## §3 Lowering — the AssembledSchema is unaffected

Per operator/174's SchemaMid → v12's AssembledSchema rename: the lowered form is the same regardless of authored shape. Each Route entry carries `(Route leg root_slot root_name endpoint body_type)`. For Spirit's richer header:

```nota
(Route ordinary 0 State (Some 0 Utterance) Utterance)
(Route ordinary 0 State (Some 1 Declaration) Declaration)
(Route ordinary 0 State (Some 2 Reflection) Reflection)
(Route ordinary 1 Record (Some 0 Entry) Entry)
(Route ordinary 1 Record (Some 1 Provenance) Provenance)
(Route ordinary 1 Record (Some 2 Snapshot) Snapshot)
(Route ordinary 2 Observe (Some 0 Self) StateQuery)
(Route ordinary 2 Observe (Some 1 Records) RecordQuery)
(Route ordinary 2 Observe (Some 2 Topics) TopicQuery)
(Route ordinary 2 Observe (Some 3 Questions) QuestionQuery)
(Route ordinary 3 Watch (Some 0 Self) StateSubscription)
(Route ordinary 3 Watch (Some 1 Records) RecordSubscription)
(Route ordinary 3 Watch (Some 2 Questions) QuestionSubscription)
(Route ordinary 4 Unwatch (Some 0 Self) StateSubscriptionToken)
(Route ordinary 4 Unwatch (Some 1 Records) RecordSubscriptionToken)
(Route ordinary 4 Unwatch (Some 2 Questions) QuestionSubscriptionToken)
```

For Spirit's actual MVP single-sub-variant per root:

```nota
(Route ordinary 0 State (Some 0 Statement) Statement)
(Route ordinary 1 Record (Some 0 Entry) Entry)
(Route ordinary 2 Observe (Some 0 Observation) Observation)
(Route ordinary 3 Watch (Some 0 Subscription) Subscription)
(Route ordinary 4 Unwatch (Some 0 SubscriptionToken) SubscriptionToken)
```

Both shapes lower the same way. The wire bytes are 1-2 bytes (1 root + 0 or 1 sub-variant); the rest of the 64-bit short header is reserved for future sub-enum slots per `/305-v2` byte-1-7 universal data variants.

## §4 What changes from v12

| Concern | v12 | v13 |
|---|---|---|
| Header variant form | Form 1 `(State Statement)` (single payload) + Form 2 `(Watch [State Records …])` (sub-enum) | UNIFIED — always `(VerbName [sub-variants])` even for single |
| Spirit schema example | minimal single-sub-variant per root | RICH multi-variant per root illustrating the form's capacity |
| Form 1 / Form 2 distinction | open + documented | REMOVED — no distinction; one uniform shape |
| Vector required for single-variant case | not enforced | YES — `(State [Statement])` not `(State Statement)` |
| AssembledSchema Route entries | endpoint optional `(Some N Name)` or `None` | endpoint ALWAYS `(Some N Name)` even for single-sub-variant case (just index 0) |
| Wire byte 1 always populated | sometimes None | yes — always carries sub-variant discriminator (0 for single) |
| Operator/174 SchemaMid form | endpoint optional | now consistent: endpoint always present |

## §5 The MVP target — Spirit's actual schema

Spirit's current contract has single payload per operation; the MVP schema reflects that:

```nota
{
  Magnitude (ImportAll ../signal-sema/magnitude.schema)
  SemaSet (Import ../signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])
}

[
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
  (Watch [Subscription])
  (Unwatch [SubscriptionToken])
]

[]

[]

{
  ;; Header-route namespace body declarations
  State [(Statement Statement)]
  Record [(Entry Entry)]
  Observe [(Observation Observation)]
  Watch [(Subscription Subscription)]
  Unwatch [(SubscriptionToken SubscriptionToken)]

  ;; Type definitions (carry forward from v12 unchanged)
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

The MVP form is what `primary-ezqx.1` operator implements against — uniform header form, single-sub-variant vectors for Spirit's current operation set.

## §6 Open structural questions

Carry forward from v12 minus the now-resolved Form-1-vs-Form-2 (resolved by unification):

| Question | Lean | Status |
|---|---|---|
| Parser support for no-outer-parens | `.schema` parser as superset of nota-codec | open |
| File naming `<component>/<component>.schema` | lean yes | open |
| Engine annotations location | convention for MVP | open |
| `EnumIdentifier` NOTA derived type | `#[derive(NotaEnumIdentifier)]` | open |
| Variant auto-promotion rule | bare name → namespace lookup | open |
| UID structure | `component::namespace::type` | open |
| Library location | `nota-schema/` peer to `nota-codec` | open |
| Field-name override syntax | `(field-name type)` post-MVP | open |
| Upgrade section position | Position 5 feature variant `(Upgrade …)` | open |
| Standard inference rules | additive new field/variant + RenamedFrom | open |
| `UpgradeRejection` in signal-sema | new entry; importable per-component | open |
| Multi-version chain | single-hop with N+2 composing at handover | open |

## §7 What this report supersedes

`/326-v13` SUPERSEDES `/326-v12`. This commit deletes `/326-v12` per `skills/reporting.md` v-suffix rule.

## §8 See also

- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md`
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
- `reports/second-designer/169-schema-file-shape-corrections-post-326-v3-2026-05-24.md`
- **`reports/operator/174-schema-import-header-design-critique-2026-05-24.md`** — header/body/feature separation (carried forward in v11+v12); v13's uniform form collapses operator's Form 1/Form 2 distinction
- `signal-persona-spirit/src/lib.rs`
- `signal-sema/src/operation.rs` + `outcome.rs`
- `version-projection/src/projection.rs` — `VersionProjection` trait
- `upgrade/src/` — upgrade triad daemon
- `nota/example.nota`
- `nota-codec/tests/*`
- `skills/nota-design.md`
- Spirit records 388-489
