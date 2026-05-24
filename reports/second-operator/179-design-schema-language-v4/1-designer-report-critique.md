*Kind: Research Slice · Topic: designer-report-critique · Date: 2026-05-24 · Lane: second-operator*

# 1 — Designer /326-v4 critique

## Source

Primary source: `reports/designer/326-v4-spirit-complete-schema-vision.md`.

Intent base: Spirit records 438-445, plus nearby records 433-437 and
446-457 where they duplicate or clarify the same correction set.

## Verdict

Designer /326-v4 correctly absorbs the visible correction from /326-v3:
`.schema` files have no outer root parentheses, the file extension
supplies the schema-file type, and the first visible field is a header
vector. That is real progress.

The report still keeps too much of the old pseudo-schema model inside
the corrected surface. It now has the right outer silhouette, but many
inner examples still use tagged records, lowercase pseudo-annotations,
generic-looking vector syntax, per-type path imports, and a catch-all
optional-features bucket. Those shapes need redesign before this can be
the source of truth for a schema compiler.

## What v4 Gets Right

1. **No outer schema wrapper survives.** The example starts directly
   with top-level positional fields, not `(Schema ...)` or a root struct
   record. This matches records 438 and 440.

2. **The artifact is `.schema`.** The report correctly moves away from
   `schema.nota` and treats the file as a special schema node, matching
   record 438.

3. **Header-first is directionally right.** Field 0 is a vector of
   ordered variants and is explicitly tied to receive-side triage,
   matching records 439 and 441.

4. **Namespace-as-map survives.** The use of `{ ... }` for type-name to
   declaration bindings matches record 443's "maps are for namespaces"
   correction.

5. **Self-description survives.** The idea that the schema language has
   a base schema defining the meaning of schema files is still the right
   model. Records 430-432 reinforce that the meta-schema and concrete
   schema meet in the same format.

## What v4 Still Gets Wrong

### 1. The header entries still contain invalid pseudo-NOTA

The operation header example is:

```nota
[
  (State (Statement (engine assert)))
  (Record (Entry (engine assert)))
]
```

`(engine assert)` is not a valid schema-language shape under the current
NOTA discipline. A lowercase identifier in record-head position is not a
record variant, and `assert` is a lowercase free token where the system
already has PascalCase sema variants such as `Assert`, `Match`,
`Subscribe`, and `Retract`.

The header needs a real typed declaration shape. A corrected sketch might
look more like one of these, depending on whether sema mapping belongs in
the header:

```nota
[
  (State Statement)
  (Record Entry)
  (Observe Observation)
  (Watch Subscription)
  (Unwatch SubscriptionToken)
]
```

or:

```nota
[
  (State Statement Assert)
  (Record Entry Assert)
  (Observe Observation Match)
  (Watch Subscription Subscribe)
  (Unwatch SubscriptionToken Retract)
]
```

The open design decision is not syntax trivia. If sema class is in the
header, receive triage can classify early. If it lives elsewhere, the
header stays pure operation-shape and sema projection is a separate
relation.

### 2. The sema header cannot be empty for the reason v4 gives

V4 sets the sema header to `[]` because "Spirit doesn't add to the
universal SemaOperation set." That conflates two things:

- whether Spirit defines new sema variants;
- whether Spirit's schema declares the sema header surface it uses.

Record 444 says each component schema defines at least regular signal,
owner signal, and sema headers. If Spirit uses universal sema variants
through imports, the sema header should probably reference or expose that
imported root, not disappear. Empty may be valid only if the component has
no sema-facing surface at all, which Spirit does not.

### 3. The owner header is treated as optional by accident

The owner header is also `[]`, and /326-v4 keeps asking whether it should
exist. The component-triad rule says owner signal is one of the component
surfaces. If Spirit's owner contract has no operations yet, an empty owner
header can be a temporary content value, but the schema shape itself must
still treat owner signal as a first-class header slot.

The redesign should distinguish:

- universal schema position exists: yes;
- this component currently declares zero owner variants: maybe;
- owner-signal contract is not part of the triad: no.

### 4. Imports are per-type path aliases, not namespace imports

V4 uses:

```nota
{
  Magnitude (Path ../signal-sema/magnitude.schema)
  SemaOperation (Path ../signal-sema/operation.schema)
}
```

Records 442 and 436 point at importing another schema's namespace,
possibly selectively. That is different from binding every imported type
to its own path. The report also introduces rename-on-import, but record
436 says selection uses the same source names and no rename mechanism is
needed for the current concern model.

A better shape is an import declaration for a source schema namespace plus
an optional selection vector:

```nota
[
  (Import ../signal-sema/signal-sema.schema [Magnitude SemaOperation SemaOutcome SemaObservation])
]
```

or, if imports are intentionally a namespace map:

```nota
{
  signal-sema (Select ../signal-sema/signal-sema.schema [Magnitude SemaOperation SemaOutcome SemaObservation])
}
```

The exact form belongs to the base schema, but the unit of import should
be a schema namespace, not one file per type.

### 5. Namespace values repeat the key and bypass the declaration union

The namespace map contains entries like:

```nota
{
  Kind (Kind Decision Principle Correction Clarification Constraint)
  Entry (Entry Topic Kind Summary Context Magnitude Quote)
}
```

The map key already names the type. Repeating `Kind` and `Entry` inside
the value is at least suspicious, and probably wrong. The base schema says
namespace values are `Declaration`, but the concrete example does not use
declaration variants such as `Enum`, `Struct`, `Newtype`, `Primitive`,
`Inline`, or `Cross`.

The value side needs to say what kind of declaration the name maps to:

```nota
{
  Kind (Enum [Decision Principle Correction Clarification Constraint])
  Entry (Struct [Topic Kind Summary Context Magnitude Quote])
  Topic (Newtype String)
}
```

Names and exact variants can change, but this shape makes the map key the
type name and the value the declaration.

### 6. Generic-looking square brackets are not a type-expression grammar

V4 uses forms such as `[Option Topic]`, `[Vec RecordSummary]`, and
`[Map Identifier Path]`. In NOTA, square brackets are vectors of values.
They are not automatically generic type application. If the schema
language needs type constructors, they should be typed variants or declared
type-expression records, for example:

```nota
(Option Topic)
(Vector RecordSummary)
(Map Identifier Declaration)
```

This matters because record 441's vector rule is about ordered enum
variants in schema positions, not about reusing `[]` as angle brackets.

### 7. Reply and Event are underdesigned as "optional features"

V4 moves Reply, Event, Observable, and maybe Storage into a final feature
vector. The vector-of-variants move is compatible with record 443, but the
category is too loose. Reply and Event are not decorative features; they
are part of the signal contract that code generation must own.

The redesign needs to decide whether replies and events are:

- additional header roots next to operation headers;
- declarations in the namespace plus relations from operations;
- typed signal-surface sections after the receive header.

They should not be hidden in an optional bucket just because they are not
the first receive-side dispatch root.

## What Must Be Redesigned

1. **Base schema positional layout.** V4's six fields are plausible, but
   not settled. The corrected layout must encode: regular signal header,
   owner signal header, sema header, imports or metadata, namespace map,
   and any extension vector. It must not rely on comments to explain field
   meaning.

2. **Header declaration grammar.** Define exactly what one header vector
   element is. Unit variant is bare PascalCase. Data-carrying variant is
   parenthesized. Decide whether payload type, sema class, and sub-enum
   header slots are all part of the element.

3. **Import declaration grammar.** Import from schema namespaces with an
   optional selection list. Drop rename unless the psyche explicitly asks
   for it.

4. **Namespace declaration grammar.** Map keys are type names. Map values
   are declaration values. The declaration union needs real variants for
   enum, struct, newtype, primitive, alias, and imported references.

5. **Type-expression grammar.** Stop using `[Option T]` and `[Vec T]` as
   pseudo-generics unless the base schema explicitly defines vectors in
   that position. Prefer typed variants like `(Option T)` and `(Vector T)`.

6. **Signal surface model.** Operation, Reply, Event, Observable, owner
   operation, and sema projection need a coherent relation model. V4's
   "header plus optional features" split is a working note, not yet a
   schema language.

## Minimal Corrected Direction

A more faithful Spirit schema sketch would have this outer shape:

```nota
[
  (State Statement Assert)
  (Record Entry Assert)
  (Observe Observation Match)
  (Watch Subscription Subscribe)
  (Unwatch SubscriptionToken Retract)
]

[]

[Assert Match Subscribe Retract]

[
  (Import ../signal-sema/signal-sema.schema [Magnitude SemaOperation SemaOutcome SemaObservation])
]

{
  Kind (Enum [Decision Principle Correction Clarification Constraint])
  ObservationMode (Enum [SummaryOnly WithProvenance])
  Topic (Newtype String)
  Entry (Struct [Topic Kind Summary Context Magnitude Quote])
  RecordQuery (Struct [(Option Topic) (Option Kind) ObservationMode])
}

[
  (Reply [(RecordAccepted RecordIdentifier) (StateObserved State)])
  (Event [(StateChanged State) (RecordCaptured RecordSummary)])
]
```

This sketch is not final. Its purpose is to show the redesign pressure:
the file has no wrapper, headers lead, imports are namespace imports,
namespace is a map, declarations are real variants, and `True`/`False`
style unit-variant logic extends consistently to every enum-like surface.

## Bottom Line

/326-v4 should survive as a correction checkpoint, not as the schema
specification. The durable parts are `.schema`, no outer wrapper,
header-first ordering, namespace maps, and vector-of-variants enum
surfaces. The parts that must be replaced are the pseudo-NOTA internals:
`(engine assert)`, per-type path imports, repeated namespace wrappers,
generic-looking brackets, empty sema by rationale, and the optional-feature
bucket for contract surfaces.
