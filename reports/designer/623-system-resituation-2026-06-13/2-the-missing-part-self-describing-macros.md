# The missing part — the structural macro node, described in schema

First design sketch of the psyche's epiphany (Spirit `t85k`, Low certainty — an
explored possibility, not a directive). The shape, one worked example, and the
open questions. Not a committed design.

## The insight

A structural macro node is "a constructor that takes a typed, counted set of
objects." That is a *describable* thing — so the shape vocabulary that today
lives as Rust `#[shape(...)]` derive attributes can instead be a **schema**, and
each concrete macro can be a **NOTA record** conforming to it. The layer that
decodes NOTA becomes written in NOTA: the notation describes its own readers.

## The shape vocabulary, today vs. as schema

Today (nota-next `derive/src/lib.rs`, the `StructuralVariantShape` enum), the
vocabulary is Rust derive attributes: `pascal_atom`, `keyword = "x"`,
`head = "X" arity = N`, `head = "X" body`, `pascal_head arity = N`,
`pascal_head body`.

As a schema type:

```
MacroShape [
  (PascalAtom)
  (Keyword KeywordText)
  (Headed HeadText Arity)
  (HeadedAtom HeadText)
  (HeadedBody HeadText)
  (PascalHead Arity)
  (PascalHeadBody)
]
```

A whole structural macro node is then a named set of variants, each a shape plus
the field types it captures:

```
MacroVariant            { VariantName * Shape MacroShape * FieldTypes (Vec TypeReference) }
StructuralMacroNodeDefinition { NodeName * Variants (Vec MacroVariant) }
```

## One worked example — `TypeReference` as data

What is today a Rust enum with `#[shape(...)]` attributes becomes a NOTA record:

```
(TypeReference [
  (Optional    (Headed Optional 2)  [TypeReference])
  (Vector      (Headed Vector 2)    [TypeReference])
  (Map         (Headed Map 3)       [TypeReference TypeReference])
  (Application (PascalHeadBody)      [ApplicationHead (Vec TypeReference)])
])
```

That last line — `Application` via `(PascalHeadBody)` — is exactly the
`#[shape(pascal_head, body)]` derive we just shipped, but written as *data*:
readable, writable, inspectable by the psyche or an agent, no Rust recompile to
see or change it.

## What building it requires

The underlying machinery already exists: nota-next's `MacroRegistry` / `Pattern`
/ `BlockShape` API is richer than the derive surface (the derive is a convenience
layer over it). So "the missing part" is:

1. the `MacroShape` + `StructuralMacroNodeDefinition` schemas (above), and
2. a reader that lowers such a NOTA definition into the existing
   `MacroRegistry` / `Pattern` machinery — i.e. instantiate a live decoder from
   the data.

## Open design questions (for the next pass)

- **Replace or generate?** Does the NOTA definition drive a *runtime* decoder
  (read the macro def, build a `Pattern`, decode), or does it *generate* the Rust
  derive code at build time? Runtime is more "self-describing"; generation keeps
  the typed-Rust-on-the-inside discipline. Possibly both: the NOTA is the source
  of truth, codegen is one consumer.
- **Field types are recursive.** `FieldTypes` is `(Vec TypeReference)` — and
  `TypeReference` is itself one of these macro-described nodes. The description
  bottoms out in a small hand-coded core (the bootstrap).
- **The bootstrap / chicken-and-egg.** The `StructuralMacroNodeDefinition` schema
  is itself read by a structural macro node. A minimal hand-written core decodes
  the definition language; everything above it is data. Naming that core
  precisely is the first concrete task.
- **Relationship to schema-next.** A schema declaration is already "a type with a
  shape"; how much of `MacroShape` is just the existing schema-declaration
  grammar viewed through the macro lens, versus genuinely new vocabulary?

## Generics and traits are the same pattern, composed

The psyche's next move: a type *with generics (and trait) definitions* is also
"a certain type matched with a certain structure" — sketched as

```
(WhateverWeNameThis <X> <PossiblyY> <PossiblyZ> [ OrAVecOfThings ] { first Value })
```

This generalizes `MacroShape` from the flat shapes above to a **compositional**
grammar: a head, then a composition of typed parts —

- **generic-parameter slots** `<X>`, some required, some optional (`<Y?>`),
- a **sequence** part `[ … ]`,
- a **record** part `{ field Type }`,
- atoms, and so on.

The parameterized declarations + applications already shipped (steps 2–4) are the
**first instance** of exactly this: `(Plane Input Output)` is `(Name <X> <Y>)` — a
head with generic params; `(Work A B C D)` applies them. What the psyche adds:
*optional* generic params, and *composing* generics with `[…]` / `{…}` / atom
parts in one declaration — and that a **trait** definition (a head + typed method
signatures) is one of these too. So one compositional, self-describing vocabulary
covers structural macro nodes, generic types, and traits alike — they are all
"a head + a typed, possibly-optional, composed structure."

### Open: is `<>` a real delimiter?

The sketch uses `<X>` for a generic-parameter slot. Today generics ride inside
`(Name Param)` with no angle brackets. A new `<>` pair earns its place only if
marking "this is a type parameter, and possibly optional" as visually distinct
from a regular field is worth a fourth delimiter — otherwise the params stay bare
in the head and optionality is expressed structurally. A genuine fork for the
psyche (*"delimiters earn their place"*); flagged, not decided.

## Why it's worth it (the psyche's load-bearing reason)

NOTA + schema is the one substrate that is simultaneously the most legible format
for a human, for an LLM, *and* binary-encodable for the programs. Moving the
macro definitions into it makes the decode layer inspectable and editable by
agents at the same fidelity as everything else — one substrate, three readers.
