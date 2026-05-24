*Kind: Design · Topic: schema-language-v4 · Date: 2026-05-24 · Lane: second-operator*

# 4 — Overview: second-operator schema design

## Verdict

`reports/designer/326-v4-spirit-complete-schema-vision.md` fixed the
largest outer-shape error: `.schema` has no outer wrapper, header comes
first, and namespace definitions are maps. It is still not the design I
would implement as the schema substrate. It keeps too many old shapes
inside the new shell: three fixed header fields, lowercase pseudo-
annotations like `(engine assert)`, `[Option T]` pseudo-generics, per-type
path imports, repeated namespace names, and a vague optional-feature
bucket.

My design is a four-field `.schema` spine:

1. `headers` — vector of header-root variants.
2. `imports` — map of source namespace to selective import.
3. `namespace` — map of local type name to declaration.
4. `surfaces` — vector of contract/runtime surface variants.

No comments are needed in the file because every position is defined by
the base schema.

## Proposed Spirit shape

```nota
[
  (Working [
    (State Statement Assert)
    (Record Entry Assert)
    (Observe Observation Match)
    (Watch Subscription Subscribe)
    (Unwatch SubscriptionToken Retract)
  ])

  (Policy [])

  (Sema [
    Assert
    Match
    Subscribe
    Retract
  ])
]

{
  signal-sema (Select ../signal-sema/signal-sema.schema [
    Magnitude
    SemaOperation
    SemaOutcome
    SemaObservation
  ])
}

{
  Kind (Enum [Decision Principle Correction Clarification Constraint])
  ObservationMode (Enum [SummaryOnly WithProvenance])
  Presence (Enum [Active Absent])
  UnimplementedReason (Enum [NotBuiltYet IntegrationNotLanded])

  Topic (Newtype String)
  Summary (Newtype String)
  Context (Newtype String)
  Quote (Newtype String)
  StatementText (Newtype String)
  FocusArea (Newtype String)
  RecordIdentifier (Newtype u64)
  StateSubscriptionToken (Newtype u64)
  RecordSubscriptionToken (Newtype u64)

  Entry (Record [
    (topic Topic)
    (kind Kind)
    (summary Summary)
    (context Context)
    (magnitude Magnitude)
    (quote Quote)
  ])

  RecordQuery (Record [
    (topic (Option Topic))
    (kind (Option Kind))
    (mode ObservationMode)
  ])

  Observation (Enum [
    State
    (Records RecordQuery)
    Topics
    Questions
  ])

  Subscription (Enum [
    State
    (Records RecordSubscription)
  ])

  SubscriptionToken (Enum [
    (State StateSubscriptionToken)
    (Records RecordSubscriptionToken)
  ])

  RecordAccepted (Record [(identifier RecordIdentifier)])
  StateObserved (Record [(state State)])
  RequestUnimplemented (Record [(reason UnimplementedReason)])
}

[
  (Reply [
    (RecordAccepted RecordAccepted)
    (StateObserved StateObserved)
    (RequestUnimplemented RequestUnimplemented)
  ])

  (Event [
    (StateChanged State DomainStream)
    (RecordCaptured RecordSummary DomainStream)
  ])

  (Observable Default OperationReceived EffectEmitted)

  (Storage [
    (Records StoredRecord)
  ])
]
```

This is a design sketch, not a final full Spirit schema. The important
shape is the top-level grammar and the removal of pseudo-NOTA.

## Why four fields, not designer v4's six

Designer v4 proposes:

1. signal header
2. owner-signal header
3. sema header
4. imports
5. namespace
6. optional features

That is workable, but it hard-codes three mostly-empty positions and makes
headers less extensible than the rest of the language. The psyche keeps
pulling the language toward enums and vectors of enum variants. The header
concern is one concern, so I would make the first top-level value a vector
of header-root variants:

```nota
[
  (Working [...])
  (Policy [...])
  (Sema [...])
]
```

This still defines the three headers first. It just makes the first object
the header set instead of spreading one concern across three top-level
slots. If a future component needs another header root, it adds another
variant to the header set instead of changing the schema struct arity.

## Header grammar

A header root is an ordered vector of variants. Its index is the dispatch
ordinal. Unit variants are bare PascalCase. Data-carrying variants are
parenthesized.

For working-signal operations, I would make each data-carrying header
variant:

```nota
(VariantName PayloadType SemaOperation)
```

Example:

```nota
(Record Entry Assert)
```

This replaces `(Record (Entry (engine assert)))`. `Assert` is a real
PascalCase sema operation variant. There is no lowercase pseudo-record
named `engine`, and no lowercase free token `assert`.

If sema classification should not be available at header time, then the
shape becomes `(Record Entry)` and sema projection moves into a separate
surface. That is one of the open questions below.

## Namespace grammar

Namespace is a map because it is truly name-value data:

```nota
{
  Entry (Record [(topic Topic) (kind Kind)])
}
```

The map key is the local type name. The value is a declaration. Repeating
the key inside the value as `Entry (Entry ...)` is wrong because it makes
the type name pretend to be the declaration kind. The declaration kind is
`Enum`, `Record`, `Newtype`, `Alias`, or a later explicit kind.

Record fields are ordered field structs:

```nota
(topic Topic)
```

That is a schema data record describing a field, not a labeled wire record.
The generated runtime value still follows the actual NOTA record rules.

## Type expression grammar

Square brackets are vectors, not generic application. Designer v4's
`[Option Topic]`, `[Vec RecordSummary]`, and `[Map Identifier Path]`
should become data-carrying type-expression variants:

```nota
(Option Topic)
(Vector RecordSummary)
(Map Identifier Declaration)
```

Bare PascalCase names are named type references or unit enum variants,
depending on schema position. `True` and `False` are naturally the unit
variants of Boolean.

## Import grammar

Imports should import schema namespaces, optionally selecting names. They
should not bind every type to its own file path.

The proposed import field is a map from source namespace name to import
spec:

```nota
{
  signal-sema (Select ../signal-sema/signal-sema.schema [
    Magnitude
    SemaOperation
    SemaOutcome
    SemaObservation
  ])
}
```

For MVP, selected names enter the local resolution universe under the same
names. Renaming is out of scope unless the psyche explicitly asks for it.
Duplicate local names should be a validation error.

## Surface grammar

Reply, Event, Observable, and Storage should not be lumped under a vague
`OptionalFeatures` concept. I would call the final field `surfaces`: a
vector of closed variants that define non-header contract/runtime surfaces.

```nota
[
  (Reply [...])
  (Event [...])
  (Observable ...)
  (Storage [...])
]
```

If Reply or Event need their own short-header receive tables, they should
move into `headers` as header roots. If they are emitted/observed surfaces
rather than incoming dispatch roots, `surfaces` is the right home.

## Base schema

The `schema` repo should define the base schema first. The base schema is
the meta-schema that tells a `.schema` reader how to bundle multiple
top-level NOTA values into a typed `Schema` struct. It is not ordinary
single-root NOTA, but it should reuse the ordinary NOTA lexer and value
decoders for each top-level field.

The Rust model I would implement:

```rust
pub struct Schema {
    pub headers: HeaderSet,
    pub imports: Imports,
    pub namespace: Namespace,
    pub surfaces: Vec<Surface>,
}

pub struct HeaderSet {
    pub roots: Vec<HeaderRoot>,
}

pub enum HeaderRoot {
    Working(Header),
    Policy(Header),
    Sema(Header),
}

pub struct Header {
    pub variants: Vec<HeaderVariant>,
}

pub struct Imports {
    pub entries: BTreeMap<NamespaceName, Import>,
}

pub struct Namespace {
    pub entries: BTreeMap<Name, Declaration>,
}

pub enum Declaration {
    Enum(Vec<Variant>),
    Record(Vec<Field>),
    Newtype(TypeExpression),
    Alias(TypeExpression),
}
```

The current `schema` repo should keep `Name`, `Namespace` as a map idea,
validation, `Engine`, `TypeExpression`, and layout planning. It should
replace `Document { sections: Vec<Section> }` with the explicit `Schema`
model before parser work.

## Open questions

1. **Header set vs three top-level header fields.** I lean to one
   first-position header-set vector containing `(Working [...])`,
   `(Policy [...])`, and `(Sema [...])`. Designer v4 uses three separate
   top-level fields. The tradeoff: one header-set field is more extensible
   and enum-shaped; three fields make the required triad surfaces more
   visually fixed.

2. **Header names.** I used `Working`, `Policy`, and `Sema` because they
   match the triad vocabulary: working signal, owner/policy signal, and
   sema operation. If the user wants names closer to repository names, use
   `Signal`, `Owner`, and `Sema`.

3. **Sema classification location.** I put `Assert`, `Match`, etc. in the
   working header variant so receive triage can classify early. If sema
   projection should be a separate relation, header variants should carry
   only payload type and the sema mapping should move to `surfaces`.

4. **Reply/Event location.** I put Reply and Event in `surfaces`, not
   `headers`, because they are contract surfaces but not necessarily the
   first incoming dispatch root. If clients also need short-header triage
   on replies/events, they should be header roots too.

## Implementation next

The next operator patch in `/git/github.com/LiGoldragon/schema` should be
a model rewrite, not parser work:

- introduce `Schema`, `HeaderSet`, `HeaderRoot`, `Header`, `Imports`,
  `Surface`, and `Declaration`;
- replace `Section::Messaging` with explicit header types;
- move imports out of `DeclarationBody::Reference`;
- replace generic-looking type syntax with `TypeExpression::Option`,
  `TypeExpression::Vector`, and `TypeExpression::Map`;
- keep layout conservative for imported types until import resolution
  exists;
- add tests for the exact four-field Spirit-shaped schema above.
