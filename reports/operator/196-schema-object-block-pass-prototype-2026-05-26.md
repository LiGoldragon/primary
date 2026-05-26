# 196 — Schema object-block pass prototype

Operator implementation report for the 2026-05-26 schema parser follow-up:
break NOTA/schema parsing down by delimiter-bounded objects with source
spans, then use those blocks as the shape surface for schema macro
recognition.

Implementation branch:
`/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`

Built on the prior prototype branch at `f9b5fdd4`.

## Intent Captured

New Spirit records:

- `770` — schema parsing needs an object-block pass with delimiter,
  source span, root-object count, and recursive child-shape predicates.
- `771` — direct source spans are preferred for now over normalizing
  each root object to one line.
- `772` — macro recognition should be recursive shape predicates over
  object blocks.
- `773` — after macro expansion, blocks are assembled and re-emitted as
  resolved schema objects.
- `778` — new clean repositories are acceptable to consider if branch
  names and old repository ancestry become too confusing, but this is
  not an immediate rename directive.

## What Changed

### `src/object_block.rs`

Added `SchemaBlockPass`, a source-oriented pass that runs before
`SchemaObjectPass`.

It scans raw NOTA text into recursive block objects:

```text
SchemaBlockPass
  roots: Vec<SchemaBlockObject>

SchemaBlockObject
  Block(SchemaBlock)
  Atom(SchemaAtom)

SchemaBlock
  delimiter: Parentheses | SquareBrackets | CurlyBraces
  span: SourceSpan
  objects: Vec<SchemaBlockObject>
  block_string: bool

SchemaAtom
  text: String
  span: SourceSpan
```

It preserves:

- byte offsets;
- line and column source positions;
- root object order;
- nested object order;
- delimiter kind;
- opaque `[|...|]` block strings;
- comments skipped outside objects.

It exposes shape methods:

- `is_parenthesis_block`
- `is_square_bracket_block`
- `is_curly_brace_block`
- `holds_single_root_object`
- `holds_two_root_objects`
- `holds_object_count`
- `second_object_is_square_bracket_block`
- `second_object_qualifies_as_symbol`
- `qualifies_as_symbol`
- `symbol_text`

This gives macro lowerers the vocabulary the psyche described:

```text
object holds two root objects
and the first qualifies as symbol
and the second is a square-bracket block
```

without pretending the delimiter itself globally means enum, struct,
or newtype.

### `src/nota_reader.rs`

`AssembledNotaSchema::from_namespace_text` now runs
`SchemaBlockPass` first, then `SchemaObjectPass`.

That means unbalanced delimiter structure fails in the source-block
layer before value lowering tries to assign schema meaning. The block
pass is not yet the full macro engine, but it is now on the prototype
path rather than sitting as a side utility.

## Tests Added

### `tests/object_block_pass.rs`

Five new tests:

1. `block_pass_preserves_root_delimiters_and_source_spans`
2. `recursive_shape_predicates_describe_macro_inputs`
3. `block_pass_keeps_block_strings_opaque`
4. `block_pass_reports_unbalanced_delimiters_with_location`
5. `block_pass_skips_comments_outside_objects`

The important test is the recursive macro-shape example:

```nota
(State [Statement Declaration])
```

The test asserts:

- the root is a parenthesis block;
- it holds exactly two objects;
- object 0 is the symbol `State`;
- object 1 is a square-bracket block;
- the bracket block holds the symbols `Statement` and `Declaration`.

That is the shape language for future schema macro dispatch.

### `tests/schema_driven_nota_reader.rs`

Added `reader_stack_runs_block_pass_before_object_lowering`.

It feeds an unbalanced namespace:

```nota
{ Topic [String]
```

and asserts the error comes from `schema object block pass` with a
missing closing delimiter. This is the constraint that keeps the
prototype honest: source structure is validated before the assembled
reader path.

## Verification

Commands run:

```sh
cargo fmt
cargo test --test object_block_pass --test schema_driven_nota_reader -- --nocapture
cargo test
nix flake check --option max-jobs 0 --print-build-logs
```

Results:

- focused object/block + reader tests: pass;
- full cargo test suite: pass;
- Nix flake check: pass.

## Review of Related Prototypes and Reports

I read:

- `reports/designer/353-schema-derived-nota-design-2026-05-26.md`
- `reports/designer-assistant/354-schema-derived-nota-prototype-2026-05-26.md`
- `reports/designer/355-critique-of-operator-195-schema-driven-nota-reader-2026-05-26.md`

The new block pass responds directly to `/355`'s strongest critique:
operator/195 was too value-tree-only and did not model macro
shape-interpretation. It does not yet reach `/354`'s full prototype
surface (`nota.schema`, five-block layout, in-process schema library),
but it moves the operator branch toward the same direction while
keeping the existing compiled-reader proof intact.

The important divergence from `/354`: designer implemented a separate
prototype crate and kernel. I stayed inside the schema crate prototype
branch and added a reusable source-block layer. That makes this branch
easier to merge into the current schema code without importing the
whole prototype crate structure.

## Repository Naming Feedback

The psyche floated creating new repositories with clean names for the
new stack. My operator read:

- This is reasonable if old repository names and branch names keep
  causing agents to wire new work through old surfaces.
- It should not happen as an incidental cleanup during the parser
  prototype.
- The strongest candidate is a clean repo boundary around the new
  schema stack once the current prototype has stable names:
  `schema`, `nota`, `nota-codec`, and `signal-frame` may not be the
  final split if `Asschema` / schema daemon / core schema library
  settle into clearer components.
- For now, feature branches remain cheaper and safer. New repos should
  follow once the assembled schema object model is stable enough to
  name.

## Gaps

The block pass does not yet normalize root objects onto single lines.
I chose source spans because they preserve authored layout and give
better diagnostics. Normalized rendering can be a separate emitter.

`SchemaBlockPass` does not yet pair each block with its corresponding
`NotaValue`. Today `AssembledNotaSchema::from_namespace_text` runs the
block pass, then separately runs `SchemaObjectPass`. A future
integrated pass should probably produce both:

```text
source span + block shape + typed value
```

for each object, so macro lowerers do not need to line up two trees by
position.

The block pass treats `[|...|]` as an opaque square-bracket block. That
matches the immediate need, but the final NOTA kernel boundary may want
a separate block-string object kind if strings are represented as
schema-derived objects rather than blocks.

The prototype still does not implement the full `/354` five-block
schema layout, precompiled core library, or schema daemon. This slice
only adds the missing object-block substrate under the previous
compiled-reader proof.

The old `EffectTable` / `FanOutTargets` / `StorageDescriptor` tests
still exist in the schema crate. This branch does not use them, but it
does not remove them.

## Next Slice

The next useful implementation step is to build a small
`SchemaMacroMatcher` over `SchemaBlockObject`:

```text
MacroPattern::Parenthesized([
  Symbol,
  SquareBracketBlock
])
```

and make `AssembledNotaSchema` lower through named macro-position
matchers instead of hard-coding namespace values in
`NamespaceTypeLowerer`.

That would turn today's block predicates into an actual macro dispatch
surface.
