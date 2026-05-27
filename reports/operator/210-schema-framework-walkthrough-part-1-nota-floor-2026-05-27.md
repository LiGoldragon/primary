# 210 — Schema framework walkthrough, part 1: NOTA structural floor

## Scope

This is the first bottom-up report in the walkthrough. It covers only the
current `nota-next` floor and the immediate handoff into `schema-next`.

It answers one question: what does the system know before schema semantics
exist?

## Current layer stack

```mermaid
flowchart TD
    A[NOTA source text] --> B[nota-next Document]
    B --> C[ordered root Blocks]
    C --> D[delimiter and atom predicates]
    D --> E[schema-next MacroRegistry]
    E --> F[Asschema, the assembled schema tree]
```

`nota-next` is deliberately the hand-authored bootstrap floor. It is not yet
itself generated from schema. It parses the delimiter language into a neutral
tree and exposes methods on that tree. Higher layers decide what the tree
means.

## What `nota-next` owns

The crate is small and explicit:

- `Document` is an ordered vector of root `Block`s plus the original source
  string.
- `Block` is one of three forms: delimited object, pipe-text object, or atom.
- `SourceSpan` and `SourcePosition` preserve byte/line/column positions.
- Factual methods start with `is_`: `is_parenthesis`,
  `is_square_bracket`, `is_brace`, `is_pipe_text`, `is_atom`.
- Shape/candidate methods start with `qualifies_as_`: they say whether an
  atom could be a schema symbol, not whether it is semantically valid in a
  schema.

Current source anchors:

- `nota-next/src/lib.rs` says this crate is the structural reader and does not
  interpret schema types, fields, imports, or macros.
- `nota-next/src/parser.rs` defines `Document`, `Block`, `Delimiter`,
  `PipeText`, `Atom`, `AtomClassification`, `NotaError`, and the recursive
  parser.
- `nota-next/tests/block_queries.rs` is the proof surface for root-object
  order, recursive shape predicates, atom classification, pipe text, and
  unclosed delimiter diagnostics.

## The exact parser model

`Document::parse(source)` does this:

1. Creates a parser cursor at byte `0`, line `1`, column `1`.
2. Repeatedly skips whitespace and semicolon comments.
3. Parses one root object at a time until EOF.
4. Returns an error if a closing delimiter appears at root.
5. Preserves the original source string so every block can re-emit its exact
   source slice by span.

A root object is parsed by first character:

```text
(  -> parenthesis Block::Delimited
[| -> Block::PipeText
[  -> square-bracket Block::Delimited
{  -> brace Block::Delimited
else -> Block::Atom
```

Delimited objects recurse until their matching close delimiter. Nested objects
are stored as ordered child blocks. A mismatched or premature closing delimiter
returns `UnexpectedClose`. EOF before the matching close returns
`UnclosedDelimiter`.

Pipe text starts with `[|` and ends with `|]`. Its contents are not recursively
parsed. That is the current square-bracket-safe text island; it can contain
`]`, quotation marks, apostrophes, and newlines as literal content.

Atoms read until whitespace, comment start `;`, any opening delimiter, or any
closing delimiter. They are classified only as candidates:

- `IntegerCandidate` when the text parses as `i64`.
- `DecimalCandidate` when it parses as `f64` and contains a dot.
- `SymbolCandidate` when it is ASCII alphanumeric / `_` / `-`, and starts
  with an ASCII letter or `_`.
- `TextCandidate` otherwise.

That classification is intentionally not semantic. A PascalCase atom only
qualifies as a PascalCase symbol; it does not become an enum variant until a
schema macro sees it in a position where an enum variant is expected.

## The shape methods

These methods are the usable interface schema macros rely on:

```text
Document::holds_root_objects() -> usize
Document::root_object_at(index) -> Option<&Block>
Block::holds_root_objects() -> usize
Block::holds_single_root_object() -> bool
Block::holds_two_root_objects() -> bool
Block::root_object_at(index) -> Option<&Block>
Block::is_parenthesis() -> bool
Block::is_square_bracket() -> bool
Block::is_brace() -> bool
Block::is_pipe_text() -> bool
Block::is_atom() -> bool
Block::qualifies_as_symbol() -> bool
Block::qualifies_as_pascal_case_symbol() -> bool
Block::qualifies_as_camel_case_symbol() -> bool
Block::qualifies_as_kebab_case_symbol() -> bool
Block::demote_to_string() -> Option<&str>
Block::reemit(source) -> &str
```

This is the important design: NOTA gives macros objects they can ask questions
about. It does not decide the final type of those objects.

## Example: one object, no semantics yet

Source:

```nota
(Record [Entry Query])
```

Raw `nota-next` sees:

```text
Document
  root[0] = Parenthesis block
    child[0] = Atom "Record"  qualifies_as_pascal_case_symbol
    child[1] = SquareBracket block
      child[0] = Atom "Entry" qualifies_as_pascal_case_symbol
      child[1] = Atom "Query" qualifies_as_pascal_case_symbol
```

At this layer, `Record` is not yet a variant, `[Entry Query]` is not yet a
struct, and `Entry` / `Query` are not yet payload types. They are just blocks
with shape.

`schema-next` later decides what that means based on `MacroPosition`.

## Handoff into `schema-next`

The current `schema-next` root shape is a three-field implicit struct:

```nota
{}
[
  (Input (Record Entry) (Observe Query))
  (Output (RecordAccepted RecordIdentifier) (RecordsObserved RecordSet) (Error ErrorMessage))
]
{
  Topic [Text]
  Description [Text]
  Entry [Topic Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
}
```

`nota-next` only says: root object 1 is a brace block, root object 2 is a
square-bracket block, root object 3 is a brace block.

`schema-next::SchemaEngine` then requires exactly three root objects and sends
them into the macro registry:

```text
root[0] at MacroPosition::RootImports
root[1] at MacroPosition::RootSurfaces
root[2] at MacroPosition::RootNamespace
```

That position is load-bearing. The same delimiter can mean different things in
different positions because `nota-next` does not impose meaning.

## What currently follows the intent well

The good parts:

- The raw NOTA layer is a structural library of methods on real objects.
- Macro logic can ask shape questions recursively rather than doing ad hoc
  string parsing.
- Source spans are present from the floor, so later diagnostics and macro
  errors can point back to exact source locations.
- Pipe text is an honest non-recursive text island for macro bodies or text
  that contains square brackets.
- NOTA does not decide schema semantics. Schema is the next layer, as intended.

## Current mismatches and pressure points

The important gaps:

1. `nota-next` currently treats ordinary `[ ... ]` as a recursive
   square-bracket block. It does not yet have a distinct inline bracket-string
   node for `[text with spaces]`. The production Spirit skill says canonical
   NOTA strings use `[text]` and `[|text|]`; this prototype floor only gives a
   special node to `[|text|]`. That is a real semantic gap for later stack
   convergence.

2. `schema-next` currently uses square brackets both as a root surface list and
   as struct-field syntax. Since `nota-next` is neutral, this is legal, but it
   is a schema-language choice. It should be reviewed against the newer
   psyche direction that `[]` should read as struct/fields and `()` as
   enum/variants.

3. Comments are discarded by parsing. That matches the current design that
   comments do not carry data, but it means schema-level documentation is not
   present in the assembled tree unless schema later adds an explicit
   documentation object.

4. Atom classification is ASCII-only for symbol candidates. That is simple and
   useful for Rust code generation, but it is not yet the eventual
   multilingual identifier/storage story.

5. `nota-next` is not schema-derived yet. It is the bootstrap floor. That is
   acceptable now, but if the end state is “Nota itself has a schema,” that
   remains future work.

## Tests that witness this layer

Current `nota-next` tests prove:

- Multiple root objects stay ordered.
- Blocks re-emit their exact source slice from spans.
- Recursive shape predicates expose parenthesis/square/brace child structure.
- Atom candidates are classified without schema semantics.
- `[|...|]` pipe text is not recursively parsed.
- Unclosed delimiters report the opening source position.

These tests cover the structural floor. They do not yet test a full
schema-derived NOTA reader, because that layer does not exist yet.

## Bottom-line assessment

`nota-next` currently matches the intended bottom layer in one key way: it is a
thin structural object library, not a schema interpreter. That is the right
foundation for schema macros.

The main thing it does not yet match is the full canonical NOTA text model:
ordinary bracket strings are not yet represented as a distinct text object in
this prototype. The next report should climb one layer up into `schema-next`
and show exactly how the macro registry turns these neutral NOTA blocks into
assembled schema.
