*Kind: Research Slice · Topic: nota-shape-for-schema-v4 · Date: 2026-05-24 · Lane: second-operator*

# 2 — NOTA shape research for schema language v4

## Inputs

Read:

- `skills/nota-design.md`
- `skills/skills.nota`
- `reports/designer/326-v4-spirit-complete-schema-vision.md`
- `/git/github.com/LiGoldragon/nota/README.md`
- `/git/github.com/LiGoldragon/nota-codec/README.md`
- `/git/github.com/LiGoldragon/nota-codec/tests/map_key_round_trip.rs`
- `/git/github.com/LiGoldragon/nota-codec/tests/option_vec_struct_variant.rs`
- `/git/github.com/LiGoldragon/nota-codec/tests/nota_mixed_enum_round_trip.rs`
- `/git/github.com/LiGoldragon/nota-codec/tests/nota_enum_data_round_trip.rs`
- `/git/github.com/LiGoldragon/nota-codec/tests/nota_record_round_trip.rs`
- `/git/github.com/LiGoldragon/nota-codec/tests/bracket_string_round_trip.rs`
- `/git/github.com/LiGoldragon/nota-codec/tests/path_round_trip.rs`

Fresh psyche corrections used as constraints: `.schema` has no
outer wrapper; the first/header declaration is a vector of ordered
enum variants; maps are only true name-value namespaces; bare
PascalCase tokens are unit variants; parenthesized PascalCase forms
are data-carrying variants; `True` and `False` are PascalCase
because bool is a two-unit-variant enum.

## Core consequence

A `.schema` file should not be treated as ordinary one-root NOTA
data. Ordinary NOTA values still obey the same token grammar, but
the `.schema` reader has one extra responsibility: read a fixed
sequence of top-level NOTA values and bundle them into the implicit
`Schema` struct declared by the base schema.

That preserves the psyche correction "no outer wrapper" without
weakening NOTA's positional record discipline. The parser mode is:

1. Tokenize with the ordinary NOTA lexer.
2. Decode top-level position 0 as the signal header vector.
3. Decode top-level position 1 as the owner header vector.
4. Decode top-level position 2 as the sema header vector.
5. Decode top-level position 3 as the import namespace map.
6. Decode top-level position 4 as the type namespace map.
7. Decode top-level position 5 as the optional feature vector.
8. Reject extra top-level values after position 5.

This is not a new text language. It is a schema-file reader over
NOTA values, with the outer struct supplied by file type instead of
by text.

## Proposed surface

Concrete shape for a Spirit-like component:

```nota
[
  (State Statement Assert)
  (Record Entry Assert)
  (Observe Observation Match)
  (Watch Subscription Subscribe)
  (Unwatch SubscriptionToken Retract)
]

[]

[]

{
  Magnitude ../signal-sema/magnitude.schema
  SemaOperation ../signal-sema/operation.schema
  SemaOutcome ../signal-sema/outcome.schema
  SemaObservation ../signal-sema/observation.schema
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

  SubscriptionToken (Enum [
    (State StateSubscriptionToken)
    (Records RecordSubscriptionToken)
  ])

  RecordAccepted (Record [(identifier RecordIdentifier)])
  RequestUnimplemented (Record [(reason UnimplementedReason)])
}

[
  (Reply [
    (RecordAccepted RecordAccepted)
    (RequestUnimplemented RequestUnimplemented)
  ])

  (Event [
    (StateChanged State DomainStream)
    (RecordCaptured RecordSummary DomainStream)
  ])
]
```

This proposal intentionally changes several v4 report examples:

- Imports map values are bare `Path` values, not `(Path ...)`
  wrappers. `Path` is a schema-positioned scalar/newtype shape in
  NOTA, so `../signal-sema/magnitude.schema` is the dense form.
- The type namespace map does not repeat the type name as the value
  head. The map key is the local type name; the value is a
  `Declaration` variant such as `(Enum ...)`, `(Record ...)`, or
  `(Newtype ...)`.
- Record fields are ordered vectors of field structs such as
  `(topic Topic)`. This is not a map and not a labeled wire record:
  it is schema data describing the field name and field type in
  order.
- Enum variants are ordered vectors. Unit variants are bare
  PascalCase tokens; data-carrying variants are parenthesized forms.

## Header shape

The first field is a vector because ordering is semantically
load-bearing: index in the vector is the root operation dispatch
ordinal. Each element is an enum-variant declaration written in the
same shape values use:

```nota
[
  (State Statement Assert)
  (Record Entry Assert)
  (Observe Observation Match)
]
```

The leading PascalCase token is the operation variant name. The
remaining positions are fixed by the base schema's `HeaderVariant`
payload. In the proposal above those positions are:

1. payload type reference
2. engine operation annotation

If the header later needs more metadata, it gains another positional
field in the base schema and every header variant carries it
explicitly. It should not become a map unless the metadata is a real
name-value namespace.

Unit operation variants are possible and should be written bare:

```nota
[
  Ping
  (Record Entry Assert)
]
```

That follows the NOTA mixed-enum rule pinned by
`nota_mixed_enum_round_trip.rs`: unit variants are bare, data
variants are parenthesized, and `(Ping)` is invalid for a unit
variant.

## Namespace maps

Maps are correct in exactly two places in the working schema shape:

- Imports: local binding name -> path or import spec.
- Type namespace: local type name -> declaration.

Both are true name-value namespaces. PascalCase map keys are allowed
because map key positions are text slots, not value positions. This
is pinned by `skills/nota-design.md`, `nota/README.md`, and
`map_key_round_trip.rs`: `{Zeus 20 prometheus 10}` is valid because
inside `{}` odd positions are key text.

Maps should not encode ordered variants, ordered fields, reply arms,
event arms, or storage declaration lists. Those are vectors because
order matters and because the element shape is not a lookup table.

## Declaration values

The type namespace value should be a `Declaration` enum:

```nota
{
  Kind (Enum [Decision Principle Correction Clarification Constraint])
  Topic (Newtype String)
  Entry (Record [(topic Topic) (kind Kind) (summary Summary)])
}
```

The `Declaration` variants are ordinary data-carrying NOTA enum
variants:

- `(Enum [...])`
- `(Record [...])`
- `(Newtype TypeReference)`
- `(Alias TypeReference)` if aliases are needed
- `(External Path)` only if imports are folded into namespace values

This avoids the redundant `Entry (Entry ...)` shape. `Entry` already
appears as the namespace key; repeating it as a value head falsely
turns the type name into a declaration variant. The useful
distinction at the value position is the declaration kind, not the
type's own name.

## Fields and type references

Field declarations should be an ordered vector of structs:

```nota
(Record [
  (topic Topic)
  (kind Kind)
  (summary Summary)
])
```

The record starts with lowercase `topic`, so under NOTA's
three-case rule it is an untagged struct, not an enum variant. The
base schema gives that struct the meaning `Field { name, type }`.

Type references use PascalCase unit variants when referring to a
named type:

```nota
Topic
Magnitude
```

Parameterized type references are data-carrying variants:

```nota
(Option Topic)
(Vec RecordSummary)
(Map Identifier Declaration)
```

This exactly mirrors `Option<T>` in the codec tests: absence is
`None`, presence is `(Some inner)`, and every field still appears
explicitly.

## Bool shape

`Bool` is best modeled in the base schema as the two-unit-variant
enum whose values are:

```nota
[False True]
```

The important grammar point is not the chosen order; it is that the
values are `False` and `True`, not lowercase parser keywords. They
are bare PascalCase unit variants under the same rule as `None`,
`Apex`, and `Decision`.

If the schema compiler assigns ordinals to boolean variants, the
base schema should state the canonical order once. The value syntax
does not need a special boolean rule.

## Constraints obeyed

- No outer wrapper: the file contains the implicit `Schema` struct's
  fields directly.
- Positional records: every parenthesized struct is positional; no
  `(key value)` labeled-field record appears.
- Enum variant grammar: bare PascalCase means unit variant;
  parenthesized PascalCase means data-carrying variant.
- Vectors for ordered domains: headers, fields, enum variants,
  replies, events, and optional features are vectors.
- Maps only for namespaces: imports and type declarations are the
  map surfaces.
- Strings and paths stay schema-positioned: import paths can be bare
  `Path` tokens; PascalCase string content must be bracketed at
  ordinary string positions.
- Options are explicit: no omitted tail fields; absent values are
  `None`, present values are `(Some inner)`.

## Implementation implication

The corrected surface requires a schema parser layer above
`nota-codec`, or a narrow multi-root mode exposed by the codec. The
operator should not try to derive `NotaRecord` for the whole `.schema`
file as-is, because derive expects one root value. The clean shape is:

- keep NOTA lexer/token/value decoding rules unchanged;
- add `.schema` top-level bundling into the implicit `Schema` struct;
- parse dynamic variant declaration heads as schema AST data, not as
  Rust enum variants known at compile time;
- lower the AST into generated Rust enums/records after validation.

That keeps the syntax faithful to NOTA while honoring the
schema-file correction that the file itself is the struct.
