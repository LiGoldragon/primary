# 4 — Overview

Operator synthesis for the NOTA structural-library prototype pass.

## Intent Captured

This pass carries the earlier records listed in `0-frame-and-method.md` and
the additional records I captured before editing:

- `787` — NOTA is the structural library for delimiter/object inspection
  before final schema typing.
- `788` — qualified symbol candidates can demote to strings later; raw
  strings should not be silently promoted into symbols after the structural
  pass.
- `789` — final PascalCase / camelCase / method-name legality belongs to the
  schema or macro context, not raw NOTA structure.
- `790` — a `.schema` file is read under an implied root `Schema` struct
  supplied by file context.
- `795` — schema uses NOTA as the macro substrate: blocks are parsed
  structurally, macro actors consume shapes, and they emit resolved schema
  objects until no macros remain.
- `796` — schema imports/exports are root schema structure and need conflict
  checking across imported exports.
- `797` — the bootstrap core schema is implemented in ordinary code first and
  exposed as the macro-writing interface.
- `798` — explicitly authorized parallel subagents are part of this operator
  workflow, with the main agent responsible for integration and tests.

## What The Subagents Found

The first subagent surveyed recent reports and prototype worktrees. Its useful
finding: port concepts from the designer prototype, not the prototype crate
wholesale. The operator branch remains the best production-adjacent base
because it already compiles generated readers against a fixture and has a
source-span block pass.

The second subagent audited the code seams. Its key recommendation was narrow:
structural methods belong on the raw block layer; schema macro meaning belongs
in schema-specific matchers and lowerers. The smallest useful next slice was a
small matcher over `SchemaBlockObject`, used by `AssembledNotaSchema` before
namespace lowering.

The existing meta-report subagent files also surfaced guidance drift:
schema/NOTA guidance still teaches old quote acceptance and old six-position
schema/features in places. I did not edit those guidance files in this code
slice; they are a separate documentation cleanup.

## What Landed

Implementation branch:

`/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`

### `src/macro_pattern.rs`

Added a concrete `SchemaMacroPattern` layer over raw block objects. It can
match:

- any object;
- any qualified-symbol candidate;
- a qualified symbol by class;
- an exact delimiter block with exact child patterns;
- a delimiter block with any number of child objects.

This makes macro recognition a composition of structural predicates instead
of raw ad hoc matching in every lowerer.

### `src/object_block.rs`

The structural layer now carries:

- `QualifiedSymbol`;
- `SymbolClass`;
- symbol demotion back to string text;
- atom and object methods that say `qualifies_as_symbol` rather than deciding
  final semantic type.

That keeps raw NOTA honest: a token can qualify as a candidate, but schema
context decides whether the token becomes a type name, variant, method name,
map key, or string.

### `src/nota_reader.rs`

`AssembledNotaSchema::from_block_and_object_pass` now uses a
`NamespaceBlockMatcher` before falling through to the existing
`SchemaObjectPass` value lowering.

The matcher validates that the namespace block is structurally a sequence of
symbol/value pairs and that each value object's delimiter matches what the
decoded `NotaValue` tree sees. This is intentionally a narrow bridge: it
proves the schema reader consumes the block matcher before semantic lowering
without trying to build the full block/value zipper yet.

## Tests Added

New tests:

- `tests/macro_pattern.rs`
  - `block_matcher_recognizes_symbol_then_square_bracket_macro_shape`
  - `block_matcher_rejects_symbol_then_atom_when_square_block_required`
  - `symbol_classes_are_candidates_not_schema_type_decisions`
- `tests/schema_driven_nota_reader.rs`
  - `reader_stack_uses_block_matcher_before_namespace_lowering`
  - `namespace_type_lowering_still_uses_object_value_after_block_match`

Existing tests in `tests/object_block_pass.rs` also now cover the symbol
candidate and macro-position wording:

- `atoms_promote_to_qualified_symbols_without_final_type_semantics`
- `raw_nota_does_not_reject_pascal_case_in_string_like_positions`
- `macro_matcher_names_the_macro_position_that_consumes_shape`
- `macro_pattern_matches_parenthesized_symbol_and_vector_shape`
- `macro_pattern_can_describe_schema_struct_field_vectors`

## Verification

Commands run in the schema worktree:

```sh
cargo fmt
cargo test --test macro_pattern --test object_block_pass --test schema_driven_nota_reader -- --nocapture
cargo test
nix flake check --option max-jobs 0 --print-build-logs
```

The focused tests passed. Full `cargo test` passed.

The first two Nix runs caught clippy issues in the new matcher iterator
(`.last()` then `.next_back()`); I fixed the code to use `rfind`.
The final Nix run passed all checks.

## What This Proves

The prototype now proves the intended layer split in executable code:

```text
source NOTA
  -> delimiter/source-span block pass
  -> reusable macro-pattern matcher over block objects
  -> schema-specific namespace matcher
  -> existing object-value lowering
  -> ordered assembled declarations
  -> generated Rust reader
```

The important point is not that the namespace reader is complete. It is not.
The important point is that a schema macro position now consumes structural
NOTA block facts before it assigns schema meaning.

## Gaps

`SchemaBlockPass` still lives in the schema crate. The direction is for this
kind of API to live in NOTA proper, but the schema worktree remains the
production-adjacent prototype surface for now.

The block pass and `SchemaObjectPass` remain parallel trees. The durable API
should pair source span, block shape, qualified-symbol candidates, and typed
value for the same object so macro lowerers do not line up two trees by
position.

The old six-position schema/features surface still exists in the schema crate
and still has passing tests. This pass deliberately avoided deleting it; the
guidance-drift audit in `3-guidance-drift-audit.md` explains why that needs a
separate focused cleanup.

The `.schema` implied-root struct, imports/exports shape, input/output
structure, and `Asschema` canonical representation are still design/code
gaps. This slice only made the raw structural layer and first matcher concrete.

## New Repo Feedback

New clean repositories are a good option once boundaries are stable enough to
name. They are especially useful if old repo names keep pulling agents back to
legacy surfaces. For this slice, existing worktrees were the right tool:
`schema` already had the closest executable proof, and moving before the
structural API settles would create naming churn without reducing ambiguity.
