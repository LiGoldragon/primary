# Instance schema examples and decoder-driven shape

Role: schema-operator
Date: 2026-06-22

## Correction

For a per-instance schema, an enum-typed position shows the enum **type
name**, not the full variant list and not the realized variant as the
schema token.

The payload already shows the realized variant. The schema beside it
answers: what type did the decoder expect at this position?

So:

| value at position | per-instance schema at same position | type-schema / Help |
|---|---|---|
| `Decision` | `Kind` | `(Kind [Decision Principle Correction Clarification Constraint])` |
| `High` inside `Certainty` | `Magnitude` | `(Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum])` |
| `Partial` inside `DomainMatch` | `DomainMatch` | `(DomainMatch [Any Partial Full])` |
| `(Record payload)` at the signal root | `Input`, with payload schema `RecordRequest` | `(Help)` shows `(Record { Entry Justification })` as the root possibility |

This is the point designer report 6 missed when it described the
instance view as "realized arm." The instance view is not the whole type
and not the arm-as-schema; it is the **expected type name at the data
position**. The arm remains visible only in the value.

Root signal values have the same rule. `Record` is not the root enum
name; it is the chosen variant of `Input`. The schema trace can show
`Input` for the root enum position and still descend into the chosen
payload's type. For Spirit's record command, the path is:

| value node | expected type | payload type |
|---|---|---|
| `(Record ...)` | `Input` | `Record` |
| record wrapper payload | `Record` | `RecordRequest` |
| request payload | `RecordRequest` | `{ Entry Justification }` |

The user-facing Help root intentionally re-heads the payload shape as
`(Record { Entry Justification })`, because Help lists the top-level
commands. The per-instance schema trace is stricter about the enum
position: root enum is `Input`; chosen variant is visible in the value.

## Example 1: Entry

Instance value, sketched as the generated Spirit value surface:

```nota
(
  [(Technology (Software (Programming CodeGeneration)))]
  Decision
  [active entries need retrieval keys]
  High
  Minimum
  Zero
  [spirit]
)
```

Per-instance schema at the same `Entry` field positions:

```schema
{ Domains Kind Description Certainty Importance Privacy Referents }
```

Notice the enum positions:

| field | value payload | instance schema token | why |
|---|---|---|---|
| `Domains` | `[(Technology ...)]` | `Domains` | the `Entry` field type is the `Domains` newtype |
| `Kind` | `Decision` | `Kind` | the decoder expected `Kind`; `Decision` is only the payload's chosen variant |
| `Certainty` | `High` | `Certainty` | the `Entry` field type is the `Certainty` newtype |
| `Importance` | `Minimum` | `Importance` | same newtype boundary rule |
| `Privacy` | `Zero` | `Privacy` | same newtype boundary rule |

If the view is expanded one step into the newtypes, the payload schemas
are:

| newtype | value payload | payload schema |
|---|---|---|
| `Domains` | `[(Technology ...)]` | `(Vec Domain)` |
| `Description` | `[active entries need retrieval keys]` | `String` |
| `Certainty` | `High` | `Magnitude` |
| `Importance` | `Minimum` | `Magnitude` |
| `Privacy` | `Zero` | `Magnitude` |
| `Referents` | `[spirit]` | `(Vec Referent)` |

That keeps both facts: the parent field is `Certainty`, and the contained
value is a `Magnitude`. It also prevents the common bad rendering
`[Zero Minimum ...]` at every magnitude position.

## Example 2: Domain path

Value:

```nota
(Technology (Software (Programming CodeGeneration)))
```

Per-instance schema, as a decoder trace:

| value node | expected type at that node | note |
|---|---|---|
| `Technology ...` | `Domain` | `Technology` is the chosen `Domain` variant |
| `Software ...` | `Technology` | payload type of the `Technology` variant |
| `Programming ...` | `Software` | payload type of the `Software` variant |
| `CodeGeneration` | `Programming` | chosen unit variant of the `Programming` enum |

This may look confusing because Spirit's taxonomy often uses a variant
name that is also the payload type name. The rule is still simple: the
schema column is the type the decoder expected; the value column is the
variant the data actually used.

The full type schema remains one Help call away:

```schema
(Help Domain)
```

That is where the alternatives belong, not in the instance schema at each
domain value.

## Example 3: Query fragment

Schema source says:

```schema
RecordSelection { DomainMatch SelectedKind }
```

Instance value:

```nota
(Partial [(Technology (Software))])
```

Per-instance schema:

```schema
{ DomainMatch SelectedKind }
```

Expanded inside the `DomainMatch` position:

| value node | expected type |
|---|---|
| `Partial ...` | `DomainMatch` |
| `[(Technology (Software))]` | `DomainScopes` |
| `(Technology (Software))` | `DomainScope` or `Domain`, depending on the exact declared alias at that position |

The schema does not show `[Any Partial Full]` here. That is the Help view:

```schema
(DomainMatch [Any Partial Full])
```

## Example 4: Root input command

Value:

```nota
(Record (([(Technology (Software (Programming CodeGeneration)))] Decision [a description] Medium Medium Zero [spirit])
         ([([a quote] None)] [reasoning])))
```

Per-instance schema as a root decoder trace:

```schema
(Input (Record RecordRequest { { Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning } }))
```

Read that as:

| value position | schema position |
|---|---|
| root enum position containing variant `Record` | `Input` |
| variant payload wrapper | `Record` |
| wrapper payload type | `RecordRequest` |
| first struct field payload | `{ Domains Kind Description Certainty Importance Privacy Referents }` |
| second struct field payload | `{ Testimony Reasoning }` |

If the display wants a compact aligned version, it can elide wrapper
levels that are already evident from the value, but the typed trace
should preserve them. The data model should not pretend the root schema
is `Record`; `Record` is the variant/wrapper on the path from `Input` to
`RecordRequest`.

## Data model

Do not model this as a string renderer. Model it as a typed decoder
trace:

```rust
DecodedWithSchema<T> {
    value: T,
    schema: InstanceSchema,
}

InstanceSchema {
    expected: SourceReference,
    body: InstanceSchemaBody,
}

InstanceSchemaBody =
    Scalar
  | Newtype(InstanceSchema)
  | Struct(Vec<InstanceSchema>)
  | EnumPayload(Option<Box<InstanceSchema>>)
  | Vector(Vec<InstanceSchema>)
  | Optional(Option<Box<InstanceSchema>>)
  | Map(Vec<(InstanceSchema, InstanceSchema)>)
```

The load-bearing field is `expected: SourceReference`. At every node it
names the type the decoder expected at that position. The body exists
only when the actual value has children to decode.

This lets the same tree answer both useful projections:

| projection | output |
|---|---|
| immediate aligned schema | the `expected` reference at each parent position |
| expanded schema trace | `expected` plus child bodies following the actual decoded value |

The renderer then encodes through schema-next surfaces. It should never
format schema text directly.

## Decoder-driven implementation

The generator already emits the ordinary decoder from schema. Extend that
emission so decoding can optionally collect the expected type references
it is already using:

1. Root decoder starts with the root enum reference, for example `Input`.
   The chosen root variant is read from the value and used to select the
   payload decoder, but the schema node for that position remains `Input`.
2. Struct decoder walks fields in declared order. For each field it pushes
   the declared field reference: `Entry`, `Justification`, `Domains`,
   `Kind`, and so on.
3. Newtype decoder pushes the wrapper reference at the parent position,
   then decodes the payload against the wrapped reference.
4. Enum decoder pushes the enum reference, reads the variant tag from the
   value, and uses the chosen variant only to select the payload decoder.
   The schema token remains the enum name.
5. Container decoders push the container reference once, then decode each
   actual element against the element reference. Empty vectors still know
   their element type because the decoder knows it.
6. Scalar decoders terminate with `String`, `Integer`, bytes, or the
   relevant primitive source reference.

This is data+decoder driven because the schema is captured from the same
typed path that validates the value. There is no second parser, no
inspection by string shape, and no per-type handwritten schema printer.

## Consequences

- Enum alternatives never appear in instance schema. They belong to Help.
- Unit enum variants are still visible in the value, so no information is
  lost.
- Empty containers remain typed: `[]` at a `Domains` position still
  yields `Domains` and, one level down, `(Vec Domain)`.
- Recursive static types are safe because the trace follows the finite
  decoded value, not the full recursive type graph.
- Newtype boundaries are preserved, which matters in this codebase:
  `Certainty`, `Importance`, and `Privacy` may all wrap `Magnitude`, but
  they are different roles.

## Test shape

The first POC tests should assert paired value/schema examples rather than
only rendered strings:

| case | value assertion | schema assertion |
|---|---|---|
| `Entry.kind = Decision` | decoded value is `Kind::Decision` | schema node expected type is `Kind` |
| `Entry.certainty = High` | decoded payload is `Magnitude::High` | parent node is `Certainty`; payload node is `Magnitude` |
| empty `Domains` | decoded vector length is zero | parent node is `Domains`; payload/container node is `(Vec Domain)` |
| `Domain::Technology(...)` | decoded variant path is present in value | schema trace is `Domain -> Technology -> Software -> ...` as expected types |
| `DomainMatch::Partial` | decoded variant is `Partial` | schema node expected type is `DomainMatch`, not `[Any Partial Full]` |
| `Input::Record(...)` | decoded root variant is `Record` | root schema node expected type is `Input`; payload path includes `Record` then `RecordRequest` |

This gives a clean pilot bar before touching a generated implementation:
the decoder must return the value and the schema trace together, and the
schema trace must round-trip through schema-next typed structures.
