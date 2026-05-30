# 258 — Macro node structural matching implementation

*Kind: implementation report · Topics: schema, nota, macro-node, structural-matching, strict-brace · 2026-05-30 · operator lane*

## What Landed

The implicit "macro node" idea is now a real code object in `schema-next`.

Before this pass, `MacroNodeDefinition` only said which dispatch family a
position used:

```text
NamespaceDeclaration -> Structural
TypeReference -> StructuralOrTaggedInvocation
```

Now a macro node definition carries named structural cases:

```text
NamespaceDeclaration
  struct declaration  = pair(symbol key, brace value)
  enum declaration    = pair(symbol key, square-bracket value)
  newtype declaration = pair(symbol key, type-reference-like value)
```

That directly represents the design point from records 1260-1262: a strict
brace key/value pair remains two NOTA objects, but the schema layer can treat
the pair as one semantic macro-node object and match it structurally.

## Code Shape

The new nouns live in `src/macros.rs`:

```text
MacroNodeDefinition
MacroNodeCase
MacroNodeObjectConstraint
MacroNodeBlockConstraint
MacroNodePairConstraint
MacroNodeKeyConstraint
MacroNodeValueConstraint
MacroNodeDelimiter
MacroNodeObjectCount
```

They make the matching rules explicit:

```text
block constraint = optional delimiter + object-count predicate
pair constraint  = key predicate + value predicate
key predicate    = symbol / PascalCase / camelCase / suffix sigil
value predicate  = delimiter / type-reference-like / same-type marker
```

`KeyValueDeclarationMacro` now owns a `MacroNodeDefinition` and asks it whether
the namespace pair matches instead of checking only `object.pair().is_some()`.

## Behavior

This schema source:

```nota
[]
[]
{
  Entry { Topics * Kind * }
  Kind [Decision Correction]
  Topic String
}
```

is now read as three namespace macro-node cases:

```text
Entry + brace          -> struct declaration
Kind + square bracket  -> enum declaration
Topic + symbol value   -> newtype declaration
```

Malformed namespace shapes now fail with:

```text
SchemaError::UnsupportedMacroNodeStructure {
  position: "NamespaceDeclaration",
  expected: [
    "struct declaration: pair key=symbol value=brace",
    "enum declaration: pair key=symbol value=square bracket",
    "newtype declaration: pair key=symbol value=type reference",
  ],
  found: ...
}
```

Type-reference positions keep their old precise errors for unknown composite
heads, so `(HashSet (Vec Leaf))` still reports `UnknownTypeReferenceForm`
instead of being swallowed by a generic macro-node error.

## Tests

Added `design_example_macro_node_definition_lists_structural_cases` in
`tests/design_examples.rs`. It proves:

- the namespace macro node lists the three structural cases;
- symbol+brace, symbol+bracket, and symbol+reference pairs all match;
- a malformed namespace block reports `UnsupportedMacroNodeStructure`.

Updated two strict-brace rejection tests to accept the new, more specific
macro-node error.

## What This Does Not Do Yet

This is not yet the full user-declared macro-node table loaded from
schema-emitted data. It is the implementation floor for that:

```text
structural cases are now data objects
registered macros can consume those cases
bad shapes report expected macro-node structures
```

The next self-hosting step is to make the same case definitions come from the
macro table data generated out of `schemas/core.schema`, rather than being
constructed by Rust associated constructors.

The exploratory single-object sigil sugar from record 1262 is intentionally
not implemented here. The new constraint types can represent it later, but the
current target remains strict brace key/value pairs.

## Comparison With Designer 438

Designer 438 is right about the final layer split: the reusable macro-node
mechanism belongs in `nota-next`, and schema-next should become a consumer
that registers schema vocabulary and handlers.

This implementation does not pretend to finish that extraction. It makes the
schema-next bootstrap layer honest first:

```text
macro-node cases are data-bearing Rust objects
namespace declaration matching delegates to those cases
unsupported node shapes report expected structural cases
```

That is compatible with the designer target. The main future move is to lift
the generic pieces (`MacroNodeCase`, block/pair constraints, key/value
constraints, match output) down into `nota-next`, then make schema-next consume
NOTA-layer `Match { name, captures }` values instead of hosting the matcher
directly.

Designer 438 also rejects prefix-sigil arity-1 sugar such as `*Type`; this
slice matches that lean. It keeps `Type *` as the explicit two-object
same-type marker inside strict brace pairs.

## Verification

Commits:

```text
schema-next      cea81f48  schema: make macro node cases structural data
schema-rust-next 5eae04d6  schema-rust: repin macro-node schema-next
spirit-next      78cca0be  spirit: repin macro-node schema stack
```

Passed in `repos/schema-next`:

```text
cargo test
cargo clippy --all-targets -- -D warnings
nix flake check
```

Passed in `repos/schema-rust-next`:

```text
cargo test
cargo clippy --all-targets -- -D warnings
nix flake check
```

Passed in `repos/spirit-next`:

```text
cargo test
cargo clippy --all-targets -- -D warnings
nix flake check
```
