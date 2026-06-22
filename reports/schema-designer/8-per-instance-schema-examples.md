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

**5 — a full Record (nested structs, all the way down).**
```
value :  (Record (([(Technology (Software (Programming CodeGeneration)))] Decision [a description] Medium Medium Zero [spirit])
                  ([([a quote] None)] [reasoning])))
schema:  (Record { { Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning } })
```
`Record` head; `RecordRequest` struct → `{ Entry Justification }`; each of
those is itself a struct → recursed; the leaves are type names.

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
    Enum(name, _)  -> name               # collapse: variant is in value_block, alternatives in Help
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

## Open choices for the psyche

1. **Collections / optionals** (example 6): name-leaf (`Testimony`),
   element-aligned recursion (`[ { … } { … } ]`), or the container type
   form (`(Vec VerbatimQuote)`)? *Lean: element-aligned recursion* — it
   keeps "same positions, all the way down" (you see one schema slot per
   actual element), and it still collapses enums inside each element. The
   name-leaf form is simplest but loses the per-element alignment that
   makes the instance view useful.
2. **Scalar leaf**: the newtype name (`Description`) or the backing scalar
   (`String`)? *Lean: the newtype name* — it is "the field's type," and
   the scalar is one `(Help Description)` away. (Help is where `String`
   surfaces.)
3. **Does this want a prototype?** The mechanism is a generic
   `project(value, schema)` fold; I can build a small data+decoder-driven
   prototype that emits these schemas from real values once the two
   choices above are pinned, so the examples become captured output
   rather than proposals.
