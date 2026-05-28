# 229 - NOTA Current Design

Date: 2026-05-28  
Lane: operator  
Component: NOTA / `nota-next`

## Current Rule

NOTA is the raw structural substrate. It parses delimiter-balanced text into
object blocks and keeps those blocks factual. It does not decide what a schema,
field, enum, macro, import, or message means.

The active code surface is `nota-next`.

## Delimiter Semantics

```nota
[A B C]
```

Square brackets are vectors at the raw NOTA layer. When the expected schema type
is `String` or a string newtype, a bracket form may be read as string text by
that higher layer. The raw parser still preserves the square-bracket object.

```nota
{ Topic [Text] Kind (Decision Principle Correction) }
```

Braces are native key/value maps. The map shape is structural, not a schema
macro. The schema layer may use this shape for namespaces and imported-name
maps, but NOTA itself only records the brace object and its root children.

```nota
(Record Entry)
```

Parentheses are raw positional records. A parenthesis object becomes a tagged
or data-carrying variant only when an expected type asks for that shape, such as
an enum body or a schema-node struct. NOTA itself does not promote the first
object to a tag.

```nota
[|text with ] and apostrophe's content|]
(| Kind (Decision Principle Correction) |)
{| Entry [Topic [Tag]] |}
```

Pipe-square is text. Pipe-parenthesis and pipe-brace are recursive delimiter
forms; they preserve inner NOTA objects for schema layers that need low-level
declaration forms.

## Code Witness

`nota-next/tests/block_queries.rs` keeps the boundary honest:

```rust
let source = "(| Kind (Decision [Reason]) |) {| Entry [Topic [Tag]] |}";
let document = Document::parse(source).expect("valid nota");
let roots = document.root_objects();

assert!(roots[0].is_pipe_parenthesis());
assert!(roots[1].is_pipe_brace());
assert!(roots[1]
    .root_object_at(1)
    .and_then(|block| block.root_object_at(1))
    .is_some_and(|block| block.is_square_bracket()));
```

That test deliberately uses `[Tag]` as native vector structure. It no longer
uses old schema collection macro call examples.

## Current Proof

Commands passed in `/git/github.com/LiGoldragon/nota-next`:

```sh
cargo fmt && cargo test
nix flake check --print-build-logs
```

Commit `d8d489dc` (`nota: remove obsolete schema syntax examples`) removed the
old schema-syntax examples from the NOTA tests.
