# Worked example — self-hosting macros, with schema + bootstrap Rust

The psyche asked for the whole idea explained back with examples: the schema
syntax that *defines* a structural macro node, and the bootstrap Rust — the
hand-written types that *read* the NOTA which defines those very types. Grounded
in the real nota-next types (verified), trimmed to a clean pedagogical core.

## The idea in one line

Today a structural macro node is hand-coded Rust (`#[derive(StructuralMacroNode)]`
+ `#[shape(...)]`). The move: describe the macro grammar *as schema*, write each
macro *as NOTA data*, and read it with a small hand-written **bootstrap** — after
which new macros are data, not code. The seed reads the data that re-expresses
the seed.

## What's already real (grounding)

The runtime macro vocabulary already decodes from / encodes to NOTA — these are
real, verified types in `nota-next/src/macros.rs`:

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize,
         nota_next::NotaDecode, nota_next::NotaEncode, Clone, Debug, Eq, PartialEq)]
pub enum MacroDelimiter { Parenthesis, SquareBracket, Brace, PipeParenthesis, PipeBrace }

#[derive(/* …NotaDecode, NotaEncode… */)]
pub struct MacroNodeDefinition { name: String, position: PositionPredicate, pattern: Pattern, expected: String }
```

So a `MacroNodeDefinition` *already* round-trips through NOTA. What's missing is
the surface vocabulary (the `#[shape(...)]` forms as data) and the lowering from a
data definition into a live `Pattern`. The example below fills that in.

## Part A — the schema (`macro.schema`): the macro grammar, as data

Struct declarations use `{ field Type }`, enum declarations use
`[ (Variant …) ]`, exactly as every other schema. (`Text` = string, `Arity` = a
number; `TypeReference` is the existing type-reference node.)

```
;; the closed delimiter set (verified against MacroDelimiter) — all unit variants, so bare
Delimiter [Parenthesis SquareBracket Brace PipeParenthesis PipeBrace]

;; the shape vocabulary — one variant per #[shape(...)] form.
;; Unit variants (no payload) are BARE; payload-carrying variants are parenthesized
;; (verified: signal.schema uses `Magnitude [Zero Minimum …]` for units and
;;  `DomainMatch [Any (Partial) (Full)]` for the payload-carrying ones).
MacroShape [
  PascalAtom
  (Keyword Text)
  (Headed Text Arity)
  (HeadedBody Text)
  (PascalHead Arity)
  PascalHeadBody
]

;; a macro node = a name + a list of variants, each a shape + the field types it captures
MacroVariant         { name Text  shape MacroShape  fields (Vec TypeReference) }
StructuralMacroNode  { name Text  variants (Vec MacroVariant) }
```

## Part B — the NOTA (`type-reference.macro`): a macro node, as data

This is the `TypeReference` node — the one we just made real in Rust — written
purely as data conforming to the schema above. A `StructuralMacroNode` value is
`(name variants)`; each `MacroVariant` is `(name shape fields)`; the `shape` is a
`MacroShape` enum value (`(Headed Optional 2)` headed, or bare `PascalHeadBody`
for a unit variant):

```
(TypeReference [
  (Optional    (Headed Optional 2)  [TypeReference])
  (Vector      (Headed Vector 2)    [TypeReference])
  (Map         (Headed Map 3)       [TypeReference TypeReference])
  (Application  PascalHeadBody       [ApplicationHead (Vec TypeReference)])
])
```

The last line is exactly the `#[shape(pascal_head, body)] Application(ApplicationHead, Vec<TypeReference>)`
we shipped — now data you can read, diff, and edit without a recompile.

## Part C — the bootstrap Rust: the seed that reads it

This is hand-written **once**. It uses the very derive the system is about, and
it reads the NOTA above. Note the self-reference: `MacroShape`'s own variants are
decoded by the same `Headed` / `PascalAtom` shapes it enumerates.

```rust
// bootstrap.rs — the irreducible seed. Everything above it is data.

#[derive(StructuralMacroNode)]
enum MacroShape {
    #[shape(pascal_atom)]                     PascalAtom,
    #[shape(head = "Keyword", arity = 2)]     Keyword(Text),
    #[shape(head = "Headed", arity = 3)]      Headed(Text, Arity),
    #[shape(head = "HeadedBody", arity = 2)]  HeadedBody(Text),
    #[shape(head = "PascalHead", arity = 2)]  PascalHead(Arity),
    #[shape(pascal_atom)]                     PascalHeadBody,   // unit
}

#[derive(StructuralMacroNode)]
enum Delimiter {
    #[shape(pascal_atom)] Parenthesis,
    #[shape(pascal_atom)] SquareBracket,
    #[shape(pascal_atom)] Brace,
    #[shape(pascal_atom)] PipeParenthesis,    // reserved for extension languages (j9du)
    #[shape(pascal_atom)] PipeBrace,          // reserved for extension languages (j9du)
}

#[derive(StructuralMacroNode)]               // structs decode positionally: (name shape fields)
struct MacroVariant { name: Text, shape: MacroShape, fields: Vec<TypeReference> }

#[derive(StructuralMacroNode)]               // (name variants)
struct StructuralMacroNode { name: Text, variants: Vec<MacroVariant> }
```

Reading the data into the seed, then lowering it to a live decoder:

```rust
// read the NOTA that *describes* TypeReference, into the hand-written type
let source = std::fs::read_to_string("type-reference.macro")?;
let node: StructuralMacroNode = StructuralMacroNode::from_structural_nota(&source)?;

// `node` is now a value describing TypeReference's grammar. Lower it to the real
// runtime Pattern (MacroNodeDefinition already NotaDecode/NotaEncode today):
let definition: MacroNodeDefinition = node.lower();   // shape -> Pattern
registry.register(definition);                         // TypeReference now decodes — from data
```

## The fixpoint (why it's a bootstrap, not a regress)

`MacroShape` is itself an enum, so it can be described by the same vocabulary.
Write its definition as data:

```
;; macro-shape.macro — MacroShape describing itself
(MacroShape [
  (PascalAtom     PascalAtom              [])
  (Keyword        (Headed Keyword 2)      [Text])
  (Headed         (Headed Headed 3)       [Text Arity])
  (HeadedBody     (Headed HeadedBody 2)   [Text])
  (PascalHead     (Headed PascalHead 2)   [Arity])
  (PascalHeadBody PascalHeadBody          [])
])
```

Read it with the hand-written `StructuralMacroNode` and you get back a value that
describes `MacroShape` — the type that just read it. The hand-written Rust (the
seed) and the data description **agree**: that's the fixpoint. From here, every
*other* macro node — `TypeReference`, the reaction frame's declarations, a new
component's contract — is added as a `.macro` data file, no Rust.

## What can't be data — the seed, named precisely

The irreducible core is small and exactly these pieces:

1. The NOTA **parser** (source bytes → `Block` tree, the `Delimiter` lexing).
2. The `StructuralMacroNode` **derive** itself (shape → decode), or a hand-written
   equivalent for the four bootstrap types above.
3. The four bootstrap types (`MacroShape`, `Delimiter`, `MacroVariant`,
   `StructuralMacroNode`) and `node.lower()` (data → runtime `Pattern`).

Everything above that line is data. Item 2 is the one genuine knot: the derive
that the data depends on is the thing the data would otherwise replace — so it
stays hand-written (or is generated from a `.macro` that the *previous* build's
derive read — a staged self-host, the harder option).

## Where structs/generics fit (from note 2 + 3)

`MacroShape` above describes enum variants. The full vocabulary also needs the
**record** part (`{ field Type }`) for structs and the **generic-parameter** part
(`<X>`, optional `<Y?>`) from note 2 — and an extension language can spend one of
the two reserved piped delimiters (`(|…|)` / `{|…|}`, note 3) on the generic
structure if it earns a distinct delimiter. The worked example here is the enum
spine; structs, generics, and traits are the same pattern with more parts.
