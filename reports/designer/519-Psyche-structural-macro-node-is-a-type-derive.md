---
title: 519 — The structural macro node is a TYPE — the derive
role: designer
variant: Psyche
date: 2026-06-05
topics: [nota, schema, structural-macro, macro-node, derive, nota-next, codec, asschema]
description: |
  Realizes the clarification (record i0e6): a NOTA macro node is a TYPE
  (an enum); NOTA does not parse untyped; the codec has a different,
  type-directed decode for such a type — a structural match on each
  variant. Built as #[derive(StructuralMacroNode)]: the enum and its
  per-variant #[shape] attributes ARE the whole specification. Verbatim
  derived round-trip; clippy-clean.
---

# 519 — The structural macro node is a TYPE — the derive

Your clarification (record `i0e6`) resolved the open seam: **the NOTA
macro node is a *type* — an enum — not a runtime construct.** NOTA does
not parse anything untyped; decode is always type-directed; the codec has
a *different* decode logic for a macro-node type than for ordinary
positional NOTA — a structural match on each variant. This report
realizes that as a derive. Branch `structural-macro-nodes` (`add64661`),
pushed; clippy `--all-targets -D warnings` clean.

## Two derives, two decode strategies

`nota-next` already had `#[derive(NotaDecode)]`, which decodes an enum by
**tag**: the variant name is the head atom, `(Optional X)` means "the
`Optional` variant." The structural macro node needs the *different* codec
logic you described, so it is a *second* derive:

| Derive | Variant chosen by | `(Optional X)` decodes as |
|---|---|---|
| `NotaDecode` (existing) | **tag** — the head atom equals the variant name | the `Optional` variant, because the tag says so |
| `StructuralMacroNode` (new) | **shape** — the first variant whose structural pattern matches | whichever variant's shape matches first in declaration order |

That is the heart of `i0e6`: same NOTA text, a *type-directed* decode
strategy selected by the target type.

## The type IS the specification

`#[derive(StructuralMacroNode)]` reads the enum and a per-variant
`#[shape(...)]` attribute and generates both directions. The example is
now nothing but the annotated enum:

```rust
#[derive(Clone, Debug, Eq, PartialEq, StructuralMacroNode)]
enum TypeReference {
    #[shape(pascal_atom)]                   Named(TypeName),
    #[shape(head = "Optional", arity = 2)]  Optional(Box<TypeReference>),
    #[shape(head = "Vec", arity = 2)]       Vector(Box<TypeReference>),
    #[shape(pascal_head, arity = 2)]        Application(TypeName, Box<TypeReference>),
}
```

The derive emits `from_structural_block` (the ordered shape match, each
variant's `BlockShape` tried in declaration order, then the matched
variant's fields decoded from the right slots — recursively) and
`to_structural_nota` (each arm writes its variant's shape). The trait is
the recursion seam: leaf types (a `TypeName`) and `Box<T>` implement it
too, so a variant can hold `Box<Self>` and nest. Like `NotaDecode`, the
derive macro and the trait share the name `StructuralMacroNode`.

## Verbatim derived round-trip (`cargo run`)

No hand-written codec anywhere in the example — this is the derived
output:

```
== the TYPE is the spec: #[derive(StructuralMacroNode)], no hand-written codec ==

in  : Integer
rust: Named(TypeName("Integer"))
out : Integer

in  : (Optional Integer)
rust: Optional(Named(TypeName("Integer")))
out : (Optional Integer)

in  : (Vec (Map (Optional RecordIdentifier)))
rust: Vector(Application(TypeName("Map"), Optional(Named(TypeName("RecordIdentifier")))))
out : (Vec (Map (Optional RecordIdentifier)))
```

Every input round-trips text → Rust → text exactly; re-decoding the
output yields the same value (both asserted). And declaration order is now
demonstrably the *enum's variant order*:

```
input: (Optional Integer)
  TypeReference  (Optional before Application) -> Optional(Named(TypeName("Integer")))
  Misordered     (Application before Optional) -> Application(TypeName("Optional"), Named(TypeName("Integer")))
```

Two *derived* types, identical variants, different order — different
decode of the same text. Nothing hand-written on either side.

## What this settles relative to the operator

Reports 517/518 pointed at this as the synthesis endpoint, and `i0e6`
confirms it is the right one. The decode is **type-directed**: no runtime
`MacroRegistry`, no capture-map, and no `from_structural_match` that
re-dispatches on a `macro_name()` string. The per-variant structural
description lives as a derive attribute on the type; the generated decode
fuses the structural match with the typed construction in one arm. This
is exactly the critique 518 raised, now resolved in the direction `i0e6`
specifies: the type drives the decode.

## Honest scope — what is and isn't done

- The shape vocabulary is the minimal three (`pascal_atom`, `head` +
  `arity`, `pascal_head` + `arity`) — enough for the type-reference
  position. Per-slot sub-shapes, sigil-aware shapes (`Name@{...}`),
  variable-arity bodies, and literal-unit variants are the next vocabulary
  additions.
- Leaf types hand-implement the trait (one method pair); the derive
  covers enums. Generics on the node enum are not yet handled.
- This does **not** yet move schema-next's `SourceXxx` types onto the
  derive, and does **not** delete `Asschema`. The path to "schema is just
  NOTA" is to derive the schema source node types (declarations, fields,
  type-references, enum variants) as structural macro nodes — at which
  point the authored `.schema` decodes and encodes entirely through these
  derives, and the assembled-schema lowering target is no longer load-
  bearing. That is the next slice, and it is where record `lcwu`'s
  certainty rises from High.

## Where it lives

- `nota-next` branch `structural-macro-nodes` (`add64661`), pushed:
  `src/structural_macro.rs` (trait + `BlockShape`), `derive/src/lib.rs`
  (`#[derive(StructuralMacroNode)]`), `examples/structural_macro_round_trip.rs`
  (the annotated enum + run). 18 existing tests pass; clippy clean.
- Predecessors: 517 (first prototype), 518 (designer-vs-operator).
