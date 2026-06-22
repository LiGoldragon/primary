# Per-instance schema — examples + the data+decoder-driven mechanism

*schema-designer · report 8 · the corrected per-instance schema view (an
enum position shows the enum **name**, not the variant and not the
alternatives), worked on real values, and how it is produced generically
from data + the decoder.*

## The three views (corrected)

For one datum there are three aligned readings:

| view | at an enum position | answers |
|---|---|---|
| **value / payload** | the realized variant — `Decision` | what this *is* |
| **per-instance schema** | the enum **type name** — `Kind` | what *shape* this is |
| **help / type-schema** | `(Help Kind)` → `(Kind [Decision Principle Correction Clarification Constraint])` | what *may* be |

The per-instance schema names the type at each position; the variant is
already visible in the value, and the alternatives are one `(Help …)`
away. No variant lists in the per-instance view.

## Proposed rendering rule

The per-instance schema mirrors the **value's** structure, replacing
content with type names:

- **struct** → `{ field-schema … }` — recurse (the brace marks a struct).
- **enum** → `(EnumTypeName payload-schema)` — the **enum type name** as
  head (**not** the variant, which is in the value), plus the realized
  variant's payload schema if it has one; a payload-less variant collapses
  to just `EnumTypeName` (e.g. `Decision` → `Kind`).
- **scalar / newtype** → the type **name** (a leaf).
- **collection / optional** → *open choice, see §Open* — leaf name, or
  recurse element-wise to stay "all the way down."

"All the way down" = recurse through nested **structs**; enums, scalars,
and newtypes collapse to their name (their depth is reached with `(Help)`).

## Worked examples (real spirit types)

**1 — enum (the core correction).**
```
value :  Decision
schema:  Kind
help  :  (Help Kind) -> (Kind [Decision Principle Correction Clarification Constraint])
```

**2 — scalar / newtype.**
```
value :  [a short description]
schema:  Description
help  :  (Help Description) -> (Description String)
```

**3 — an enum with a payload (the corrected core: name, not variant).**
```
value :  (Partial [(Technology (Software (Programming CodeGeneration)))])
schema:  (DomainMatch DomainScopes)
help  :  (Help DomainMatch) -> (DomainMatch [Any Partial Full])
```
`Partial` is a **variant** of the enum **`DomainMatch`**, so the schema's
head is `DomainMatch` (the enum *type*), **not** `Partial` (the variant —
that is in the value), and it still shows the payload's type
`DomainScopes`. The variant lives in the value; the schema names the enum
and its payload type.

**4 — a struct (Entry).**
```
value :  ([(Technology (Software (Programming CodeGeneration)))] Decision [a description] Medium Medium Zero [spirit])
schema:  { Domains Kind Description Certainty Importance Privacy Referents }
```
The struct recurses to its field **type names**; `Kind`/`Certainty`/
`Importance`/`Privacy` are enums shown by name, `Domains`/`Referents` are
collections shown by name, `Description` is a scalar shown by name.

**5 — a full Record (the head is the enum, not the variant).**
```
value :  (Record (([(Technology (Software (Programming CodeGeneration)))] Decision [a description] Medium Medium Zero [spirit])
                  ([([a quote] None)] [reasoning])))
schema:  (Input { { Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning } })
```
`Record` is a **variant of `Input`** (signal-spirit's top-level request
enum), so the head is **`Input`**, not `Record` — the variant is in the
value. Record's payload `RecordRequest` is a struct →
`{ Entry Justification }`, each itself a struct → recursed to field type
names. (My earlier `(Record …)` head was wrong — it put the variant where
the enum name belongs, contradicting `Decision → Kind`.) See §Open for the
newtype question on `Certainty`/`Importance`/`Privacy`.

**6 — the collection open choice (Testimony = `(Vec VerbatimQuote)`).**
```
value :    [([a quote] None) ([another quote] (Some [an antecedent]))]
schema A:  Testimony                                  ;; collection as a name-leaf (navigate with Help)
schema B:  [ { QuoteText OptionalAntecedent } { QuoteText OptionalAntecedent } ]  ;; recurse element-wise, aligned
schema C:  (Vec VerbatimQuote)                        ;; the container type form
```
This is the main thing to pin (see §Open).

## Data + decoder driven — the mechanism

The per-instance schema is **not** hand-written per type. It is one
generic walk over two pieces of **data** — the **value** and its **type
schema** — driven by the **decoder**:

```
instance_schema(value_block, type_decl):
  match type_decl:                       # type_decl is a SourceDeclaration (data)
    Struct(fields) -> "{ " + join(instance_schema(child_block, field_decl)
                                  for child_block, field_decl in zip(value_block.children, fields)) + " }"
    Enum(name, variants) ->              # head is the enum NAME, not the variant
      let (variant, payload) = read_variant(value_block)          # the value says which arm
      variants[variant].payload ? "(" name " " instance_schema(payload, variants[variant].payload) ")"
                                : name   # payload-less variant -> just the enum name
    Scalar(name)   -> name
    Newtype(name)  -> name
    Collection(elem_decl) -> ...         # §Open: name | recurse per value_block element
```

Why this is "data + decoder driven":

- The **type schema** (`SourceDeclaration`) is *data* that parameterizes
  the walk — the same schema the codec already produces/consumes.
- The **value** is *data* that supplies the realized structure (how many
  collection elements, which positions are present).
- The **decoder** already performs exactly this type-directed traversal
  of a value against a type — decoding *is* walking the value guided by
  the schema. The per-instance schema is that **same traversal in a
  projection mode**: emit the declared type's name/kind instead of
  building the value. One generic engine, no per-type code.

So it reuses everything already built: `schema-next` supplies the
`SourceDeclaration` for the type; `nota_next` supplies the value's blocks;
the projection is a fold over `(value, schema)`. This is the universal
mechanism of report 6 — `project(value, its-type-schema)` — with the
enum-collapse rule. The structural-forms thesis once more: the grammar is
data, the walk is generic, the schema falls out of folding the value
against it.

## Resolved — converged with operator (report 3)

operator's `reports/schema-operator/3-instance-schema-examples-and-decoder-driven-shape.md`
independently reached the same model — the **third** convergence after
help and the schema codec — and pins the data model plus the choices I had
left open:

- **Data model: a typed decoder trace, not a string renderer.**
  `DecodedWithSchema<T> { value, schema }`, where
  `InstanceSchema { expected: SourceReference, body }` and `body` ∈
  `Scalar | Newtype(InstanceSchema) | Struct(Vec<_>) | EnumPayload(Option<_>) |
  Vector(Vec<_>) | Optional(Option<_>) | Map(Vec<(_,_)>)`. The load-bearing
  field is `expected` — the type the decoder expected at each position.
  This is the concrete typed form of the `project(value, schema)` fold
  above; **adopt it**. The decode pass returns the value *and* the trace
  together; the renderer encodes through schema-next, never formatting
  text directly.
- **Newtypes are preserved (resolves my open #2 — no divergence).** A
  newtype is a `Newtype(InstanceSchema)` node: `Certainty` at the field
  position, `Magnitude` one level inside. Both facts kept — the role
  (`Certainty` vs `Importance` vs `Privacy`) *and* the underlying enum
  (`Magnitude`). The renderer picks the depth; example 5's
  `Certainty/Importance/Privacy` leaves are the field-level projection.
- **Collections are element-aligned (resolves my open #1).**
  `Vector(Vec<InstanceSchema>)` — one node per actual element — and the
  element type is known even for an empty vector (`[]` at `Domains` still
  yields `Domains`, `(Vec Domain)` one level down).
- **Root is a trace; display may elide.** The typed trace preserves the
  whole path `Input → Record → RecordRequest → { … }`; the *display* may
  elide wrapper levels already evident from the value, giving example 5's
  compact `(Input { … })`. The data model keeps them; the renderer chooses.

**Remaining step:** a data+decoder-driven prototype that returns
`(value, schema-trace)` from one decode pass and round-trips the trace
through schema-next — operator's report 3 §"Test shape" is the bar. Both
tracks agree on the shape; ready to build whenever you want it.
