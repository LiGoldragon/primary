# Operator Comparison — Designer vs Operator Structural Macro Node

Date: 2026-06-05

Compared surfaces:

- Designer branch: `/git/github.com/LiGoldragon/nota-next` bookmark
  `structural-macro-nodes`, commit `c2b4cc72`.
- Designer report:
  `/home/li/primary/reports/designer/517-Psyche-structural-macro-nodes-prototype.md`.
- Operator main implementation:
  - `nota-next` main commit `35786532`.
  - `schema-next` main commit `87991f83`.
  - Operator report:
    `/home/li/primary/reports/operator/312-Psyche-nota-structural-macro-node-implementation-2026-06-04.md`.

## Verdict

The two implementations are complementary, not mutually exclusive.

Designer's version is the clearer prototype. It names the missing thing very
well: `BlockShape` is a per-variant structural description, and the example
shows a real type-reference dialect with recursive parse and exact encode-back.
It is better at teaching the idea and better at exposing the next ergonomic
target: `#[derive(StructuralMacroNode)]` with per-variant shape attributes.

Operator main is the better integration base. It reuses the existing
`nota-next::MacroNodeDefinition`, `Pattern`, `MacroRegistry`, captures, nested
delimiter matching, conflict checks, and diagnostics instead of creating a
second shape system. It also wires one real `schema-next` authored source
position, `SourceVariantSignature`, through the structural node path and keeps
all `schema-next` tests green.

My recommendation: do not merge designer's branch wholesale. Instead, lift its
best pieces into the operator/main path:

1. Add a first-class `BlockShape` / shape-vocabulary builder over the existing
   `Pattern` model.
2. Add designer's runnable type-reference round-trip example, adapted to the
   main `StructuralMacroNode` trait.
3. Then implement the derive macro in `nota-next-derive`.

## Designer Strengths

Designer's prototype has a sharper noun: `BlockShape`. That is closer to the
psyche's phrase "per-variant structural description" than the operator
surface, which currently asks implementors to return a vector of
`MacroNodeDefinition` values. The operator surface is correct but mechanically
noisy; designer's shape noun is the ergonomic layer the derive macro wants.

Designer also proves recursive structure better. The example:

```text
in   : (Vec (Map (Optional RecordIdentifier)))
rust : Vector(Application(TypeName("Map"), Optional(Named(TypeName("RecordIdentifier")))))
out  : (Vec (Map (Optional RecordIdentifier)))
```

is a stronger psyche-facing demonstration than the operator's first
`schema-next` witness because it shows deep nested structural macro positions
in one line. It makes the mechanism visible.

The declaration-order proof is also better. Designer shows the same input
decoded two ways:

```text
input: (Optional Integer)
  Optional declared BEFORE Application -> Optional(Named(TypeName("Integer")))
  Application declared BEFORE Optional  -> Application(TypeName("Optional"), Named(TypeName("Integer")))
```

That is exactly the failure mode the psyche was worried about. Operator main
has a declaration-order test (`Reserved` beats generic PascalCase), but it is a
less schema-relevant example.

## Operator Strengths

Operator main keeps one structural matcher. `nota-next` already had
`MacroNodeDefinition`, `Pattern`, `PatternElement`, `DelimitedShape`,
`AtomShape`, nested child constraints, captures, and `MacroRegistry::dispatch`.
The operator implementation places `StructuralMacroNode` on that existing
mechanism instead of adding a new parallel `BlockShape::matches` matcher.

That matters because the existing pattern layer already supports things the
designer prototype names as open questions:

- delimiter checks,
- exact/even/any object counts,
- atom case checks,
- literals,
- rest captures,
- nested child patterns,
- block/body captures,
- position predicates,
- no-match diagnostics that list expected cases.

Designer's `BlockShape` currently supports only `PascalAtom`,
`HeadedParenthesis`, and `PascalHeadedParenthesis`. It is clean, but narrower.
If merged as-is, `nota-next` would have two structural languages: the older
pattern registry and the new `BlockShape` matcher. That is the wrong direction.

Operator main also proves integration with actual Schema source:

```text
Input schema source:
{}
[Reserved (Record Entry) (Inline { Topic * })]
[]
{
  Entry { Topic * }
  Topic String
}
```

`schema-next` now decodes that into typed `SourceVariantSignature` values,
encodes it back to the same schema surface, and lowers it so `Record` carries
`Entry` while `Inline` creates and carries its same-named inline declaration.
That is less visually dramatic than designer's type-reference example, but it
is more production-relevant because it exercises the real `schema-next` source
codec and test suite.

## The Main Technical Difference

Designer implements a new direct shape matcher:

```rust
pub enum BlockShape {
    PascalAtom,
    HeadedParenthesis { head: HeadSymbol, arity: usize },
    PascalHeadedParenthesis { arity: usize },
}
```

Operator implements the typed enum bridge over the existing matcher:

```rust
pub trait StructuralMacroNode: Sized {
    type Error;

    fn structural_position() -> PositionPredicate;
    fn structural_variants() -> Vec<MacroNodeDefinition>;
    fn from_structural_match(matched: MacroMatch<'_>) -> Result<Self, Self::Error>;
    fn to_structural_nota(&self) -> String;
}
```

This is the key design tradeoff:

- Designer's API is easier to author and explain.
- Operator's API reuses the richer existing matcher and integrates with
  schema's existing macro-node case lists.

The right final shape is likely a combination: keep operator's
`MacroRegistry`/`Pattern` substrate, but add designer's `BlockShape` as a
small authoring vocabulary that lowers into `Pattern`. Then the derive macro
can expose simple per-variant attributes without losing the full matcher.

## What I Would Change In Operator Main

The operator implementation is correct but too raw. Requiring every typed node
to build `MacroNodeDefinition` manually is not the ergonomic endpoint. The next
step should add an authoring layer such as:

```rust
enum StructuralVariantShape {
    PascalAtom,
    LiteralAtom(&'static str),
    HeadedParenthesis { head: &'static str, arity: usize },
    PascalHeadedParenthesis { arity: usize },
    Delimited { delimiter: MacroDelimiter, count: MacroObjectCount },
}
```

That type should have methods that lower into `Pattern` /
`MacroNodeDefinition`. This keeps the single matcher while adopting designer's
clear "per-variant shape vocabulary" noun.

I would also add a `nota-next` example like designer's
`structural_macro_round_trip.rs`, adapted to main. Tests prove behavior for
machines; that example proves understanding for humans.

## What I Would Change In Designer's Branch

I would not keep a separate `src/structural_macro.rs` matcher as-is. It
duplicates `Pattern` and will immediately fall behind on captures, nested
patterns, body streams, no-match diagnostics, sequence positions, and
schema-position dispatch.

The designer version should become one of two things:

- a design example rewritten on top of operator main's `StructuralMacroNode`;
  or
- an ergonomic shape-builder module whose shapes lower into the existing
  `MacroNodeDefinition` model.

The `Display`-as-encode choice is elegant for examples, but the crate already
uses `NotaEncode`/`to_nota` vocabulary elsewhere. For the final API I prefer
`to_structural_nota` or an eventual `NotaEncode` integration over requiring
`fmt::Display` as the encode trait. `Display` can stay as a convenience.

## Asschema Implication

Designer says the prototype "kills Asschema." Mechanistically, I agree with
the direction but not the timing.

The prototype proves that one schema-like position can decode directly from
NOTA blocks into typed Rust and encode back without an intermediate object.
Operator main proves the same principle inside real `schema-next` source for
enum variant signatures. Together, they make the Asschema-removal path more
credible.

But `Asschema` still has live jobs today:

- macro-free endpoint for `schema-rust-next`,
- symbol paths,
- artifact tests,
- binary/text schema artifacts,
- storage and migration experiments,
- a stable comparison target while source sugar changes.

The safe sequence is:

1. Expand `SchemaSource` structural nodes across more positions.
2. Add generated/derived structural node implementations.
3. Prove `schema-rust-next` can consume the typed source/direct decoded model.
4. Then decide whether `Asschema` disappears, shrinks into a cache/artifact, or
   remains as a macro-free projection.

## Concrete Next Move

I would integrate designer's best work by doing this on main:

1. Add `StructuralVariantShape` or `BlockShape` to `nota-next`, but implement
   it as a builder into existing `Pattern` / `MacroNodeDefinition`.
2. Add designer's `TypeReference` round-trip example using the main
   `StructuralMacroNode` trait.
3. Add a declaration-order shadowing test using `Optional` versus general
   `Application`, because that is the clearest example.
4. Implement `#[derive(StructuralMacroNode)]` in `nota-next-derive` once the
   shape vocabulary is stable enough.

This preserves the operator integration while accepting designer's better
teaching model and better ergonomic endpoint.
