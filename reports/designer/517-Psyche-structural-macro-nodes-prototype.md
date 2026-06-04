---
title: 517 — Structural macro nodes in NOTA — working prototype
role: designer
variant: Psyche
date: 2026-06-04
topics: [nota, schema, structural-macro, macro-node, asschema, nota-next, schema-next, prototype]
description: |
  A working prototype of the structural macro node — a NOTA enum
  dispatched by block SHAPE, in declaration order, parsed into typed Rust
  recursively, and encoded straight back. Real run output: schema sugar
  round-trips through NOTA with no assembled-schema lowering step. The
  design surface for the back-and-forth, and the derive-macro endpoint.
---

# 517 — Structural macro nodes in NOTA — working prototype

This proves the mechanism you described: a NOTA enum whose variant is
chosen by the *shape* of the object at its position, matched in
declaration order, parsed into typed Rust recursively, and encoded back —
so a schema file is plain NOTA and no assembled-schema lowering target is
needed. The code is on the nota-next branch `structural-macro-nodes`
(`c2b4cc72`), pushed. Captured intent: records `ejvc` (the mechanism) and
`lcwu` (schema-is-NOTA / Asschema-not-needed).

## What already existed vs. what was missing

`nota-next` already has the *floor* your design needs:

- The `Block` model (`Delimited{delimiter, span, root_objects}` /
  `PipeText` / `Atom`) and the **structural methods** you named:
  `is_parenthesis`/`is_brace`/`is_square_bracket`, `holds_root_objects`
  (arity), `root_object_at`, `qualifies_as_pascal_case_symbol`,
  `demote_to_string`, `structure_shape`. NOTA even has the `@` sigil
  (`Name@{...}` / `name@(...)`) in the parser.
- A *pattern-matching* macro mechanism (`MacroRegistry::dispatch` —
  sequential, position-filtered, first-match, with named captures).

What was **missing** is exactly your point. The current mechanism matches
a pattern and hands back *block references* (captures). It does not then
drive a **typed** parse into a per-variant data type, it has **no encode
/ round-trip**, and its variants are loose registry entries keyed by an
external string `position` label — not *an enum whose variants are
matched by structure in declaration order*. So the structural dispatch
exists, but the **typed, bidirectional, enum-shaped** node — the thing
that would let schema be just-NOTA — does not. That is what the prototype
adds.

## The mechanism (`src/structural_macro.rs`)

Three pieces, all method-bearing (no free functions):

`BlockShape` — the **per-variant structural description**, reified. A
variant declares its shape; matching reads *only* the structural methods
on `Block`, never the payload:

```rust
pub enum BlockShape {
    PascalAtom,                                      // `Integer`
    HeadedParenthesis { head: HeadSymbol, arity: usize },   // `(Optional T)`
    PascalHeadedParenthesis { arity: usize },        // `(Map Entry)` — general head
}

impl BlockShape {
    pub fn matches(&self, block: &Block) -> bool {
        match self {
            Self::PascalAtom => block.qualifies_as_pascal_case_symbol(),
            Self::HeadedParenthesis { head, arity } =>
                block.is_parenthesis()
                    && block.holds_root_objects() == *arity
                    && block.root_object_at(0).is_some_and(|first| head.matches(first)),
            Self::PascalHeadedParenthesis { arity } =>
                block.is_parenthesis()
                    && block.holds_root_objects() == *arity
                    && block.root_object_at(0).is_some_and(Block::qualifies_as_pascal_case_symbol),
        }
    }
}
```

`matches` is the **contact point** between the variant axis and a block's
structure (the enum-contact-point discipline) — one named `match`, not a
scatter of `if`-chains.

`StructuralMacroNode` — the trait an enum implements. `from_block` is the
structural decode; `Display` is the structural encode (each arm emits the
variant's NOTA shape), so a value round-trips to the text it came from:

```rust
pub trait StructuralMacroNode: Sized + fmt::Display {
    fn from_block(block: &Block) -> Result<Self, StructuralMacroError>;
    fn from_nota(source: &str) -> Result<Self, StructuralMacroError> { /* parse + decode single root */ }
}
```

## The demonstration — a real schema type-reference dialect

The example (`examples/structural_macro_round_trip.rs`) models the
type-reference position — real schema sugar — as a structural macro node:

```rust
enum TypeReference {
    Named(TypeName),                          // `Integer`
    Optional(Box<TypeReference>),             // `(Optional T)`   — specific head
    Vector(Box<TypeReference>),               // `(Vec T)`        — specific head
    Application(TypeName, Box<TypeReference>),// `(Map Entry)`    — general head, declared LAST
}
```

`from_block` tries the variants in declaration order; each recursion slot
is itself a `TypeReference`, so nesting decodes structurally all the way
down.

## Real run output (`cargo run --example structural_macro_round_trip`)

This is verbatim — here is what goes in, here is what comes out:

```
== round-trip: NOTA text -> Rust value -> NOTA text ==

in   : Integer
rust : Named(TypeName("Integer"))
out  : Integer

in   : (Optional Integer)
rust : Optional(Named(TypeName("Integer")))
out  : (Optional Integer)

in   : (Vec (Optional Integer))
rust : Vector(Optional(Named(TypeName("Integer"))))
out  : (Vec (Optional Integer))

in   : (Map Entry)
rust : Application(TypeName("Map"), Named(TypeName("Entry")))
out  : (Map Entry)

in   : (Vec (Map (Optional RecordIdentifier)))
rust : Vector(Application(TypeName("Map"), Optional(Named(TypeName("RecordIdentifier")))))
out  : (Vec (Map (Optional RecordIdentifier)))
```

Every input round-trips: `text -> Rust value -> text` is byte-identical,
and re-decoding the output yields the same value (both asserted in the
example; the run completes without panicking). The deep case
`(Vec (Map (Optional RecordIdentifier)))` decodes through four nested
structural-macro positions by shape alone and re-emits exactly.

**Declaration order matters — demonstrated empirically:**

```
input: (Optional Integer)
  Optional declared BEFORE Application -> Optional(Named(TypeName("Integer")))
  Application declared BEFORE Optional  -> Application(TypeName("Optional"), Named(TypeName("Integer")))
```

`(Optional Integer)` matches *both* the specific `Optional` head and the
general `Application` head. With `Optional` declared first it reads
correctly; reorder so the general head comes first and it is mis-read as
"apply a constructor named `Optional`." This is why variants are tried in
the order written — exactly the property you called out.

## Why this removes the need for assembled schema

The original stack lowers authored schema NOTA into a separate `Asschema`
object (`schema-next`), and that object is what `schema-rust-next`
consumes. The prototype shows the type-reference *sugar* decoding and
re-encoding **directly through NOTA** — `Document::parse` produces the
`Block`, the structural macro node turns it into typed Rust, and `Display`
turns it back. There is no intermediate assembled form: the typed Rust
value *is* the lowered representation, and it is recovered from, and
written back to, plain NOTA. Generalize the node set to cover the rest of
schema's positions (declarations, fields, imports/exports, visibility)
and "lower schema into Asschema" becomes "decode a NOTA document whose
positions are structural macro nodes." Schema stays NOTA the whole way —
which is what records `lcwu` asserts.

The honest scope line: this prototype demonstrates the *mechanism* on one
real position with full round-trip. It does **not** yet re-implement all
of schema's sugar, and it does not yet delete `Asschema` from
`schema-next`. It proves the claim is reachable; finishing it is the
follow-on work, and only then does `lcwu`'s certainty rise from High.

## The design surface for the back-and-forth

The one real decision is **how a variant declares its shape**. This cut
uses a small `BlockShape` vocabulary (`PascalAtom`, `HeadedParenthesis`,
`PascalHeadedParenthesis`). Open questions for us:

- **Pattern vocabulary.** Is delimiter + head + arity + symbol-case
  enough, or do we want per-slot sub-shapes (slot 1 must be a brace, slot
  2 a square bracket), sigil-aware shapes (`Name@{...}`), and
  variable-arity bodies (a brace holding *N* fields)? The current cut is
  deliberately minimal so the round-trip is unambiguous.
- **Where the body recursion is declared.** Here `inner_reference`
  hand-codes "slot 1 is the recursion point." A general node would
  declare which slots are themselves structural macro nodes, so the
  recursion is data, not hand-code.
- **Sequence positions.** Some schema sugar is a *sequence* of blocks
  (`Name { ... }` is two blocks at one position), not a single block.
  The prototype handles single-block positions; sequence positions are a
  natural extension of `from_block` to `from_blocks(&[Block])`.

## The ergonomic endpoint — a derive macro

The prototype hand-writes `from_block` and `Display`. The endpoint you
hinted at — "per variant derived macro syntax" — is a
`#[derive(StructuralMacroNode)]` reading per-variant shape attributes, e.g.

```rust
#[derive(StructuralMacroNode)]
enum TypeReference {
    #[shape(pascal_atom)]                 Named(TypeName),
    #[shape(head = "Optional", arity = 2)] Optional(Box<TypeReference>),
    #[shape(head = "Vec", arity = 2)]      Vector(Box<TypeReference>),
    #[shape(pascal_head, arity = 2)]       Application(TypeName, Box<TypeReference>),
}
```

generating both the ordered `from_block` and the `Display` encode. Its
home already exists: `nota-next-derive` (the crate that emits
`NotaDecode`/`NotaEncode` today). That is the next iteration once the
pattern vocabulary settles.

## Where it lives

- Branch `structural-macro-nodes` (`c2b4cc72`) on `nota-next`, pushed.
  `src/structural_macro.rs` (mechanism), `examples/structural_macro_round_trip.rs`
  (demonstration). 18 existing tests still pass.
- This is a designer feature branch; operator integration owns its path
  to `main`.
