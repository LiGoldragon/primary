# Text Position Representations

Research for the structural first pass: recording where each portion begins and ends.

## Ropes — what they are and why they are not the answer here

A rope is a binary tree where each leaf holds a chunk of string and each
interior node stores the cumulative length of its left subtree. This lets a
text editor insert or delete anywhere in O(log n) without shifting the whole
buffer, and supports persistent (immutable-sharing) undo at low cost.

The problem ropes solve is *mutation of large text in memory*. They are an
editor-buffer structure, not a span representation. A parser reads text once,
left to right; it does not need to insert or delete. Whatever span coordinates
the parser records — byte offsets, line/col pairs — can be recorded the same
way regardless of whether the source text is held in a rope, a gap buffer, or
a plain string.

For datom-sized input (small documents) the question is moot twice over: the
text is tiny and read-only during parsing.

## Common span representations in parsers

**Byte offsets** are the dominant internal choice. A span is two u32 values
(start, end) measured in UTF-8 bytes from the start of the source. Eight bytes
per span; no ambiguity about encoding units; stable under UTF-8 validity.
Line/column is computed on demand by binary-searching a pre-built table of
newline positions — O(log n) per conversion, done only for diagnostics.

**Line/column pairs** (row, col) are the natural display form but an awkward
storage form. They require two numbers per position instead of one, and column
semantics vary (bytes? codepoints? grapheme clusters?). Tree-sitter uses TSPoint
(row u32, col u32 measured in bytes) as a secondary representation alongside a
primary byte offset — both are exposed in the parse callback so callers can
choose.

**Char (codepoint) offsets** appear in LSP, which uses UTF-16 code-unit offsets
at the protocol boundary. Internal tooling converts from byte offsets to
whatever the protocol requires; codepoint offsets are not stored internally.

## How the major tools do it

**rustc** stores spans as `(BytePos, BytePos)` — byte positions relative to the
crate root, encoded as u32. The `SourceMap` maps BytePos to file, line, and
column on demand. Diagnostic rendering calls into SourceMap; the parser never
touches line numbers.

**tree-sitter** records both a byte offset and a TSPoint at every node. The
dual representation is explicit in the API: `node.start_byte()` and
`node.start_point()` are distinct accessors. Column in TSPoint is byte count
from the line start, not codepoint count.

**rust-analyzer / text-size / rowan** define `TextSize` as a UTF-8 byte offset
stored as u32, and `TextRange` as a `(TextSize, TextSize)` pair. The crate
documentation describes it as "a UTF-8 bytes offset." Eight bytes per span.
The green tree in rowan stores only *widths* (token and node lengths) without
absolute positions. The red tree accumulates absolute offsets lazily as you
walk down: `red_offset = parent_offset + sum_of_preceding_siblings_widths`.
Spans are therefore not stored redundantly — each node holds its width once;
absolute position is computed from context on traversal.

## The green/red parallel

Rowan's two-layer design maps closely onto the psyche's two-step:

- **Green tree** — untyped, position-independent structural skeleton. Nodes
  store only their kind token (an opaque integer) and their children's widths.
  Identical subtrees are deduplicated. No typed interpretation, no absolute
  positions.
- **Red tree** — typed views over the green tree, with accumulated byte offsets.
  `SyntaxNode` wraps a green node and carries the running offset from the root.

The green tree is delineation without typing; the red tree is typed matching on
top of it. The offset is not intrinsic to the green structure — it is computed
when needed from the textual reading, exactly as the psyche described: "spans
are computed rather than intrinsic."

## Recommendation

*(Inference from research and flow context — not a psyche ruling.)*

Store spans as **byte-offset pairs** (start: u32, end: u32). This is what
every serious Rust parser tool uses, for good reasons: eight bytes, unambiguous,
no encoding questions, trivially composable. Line/column is a rendering concern;
build a newline offset table once after lexing and query it only for diagnostics
or display.

The structural first pass — finding where each portion begins and ends without
typing it yet — maps naturally onto the green-tree pattern: a flat or nested
record of `(kind_hint, start, end)` triples, where `kind_hint` is something
like "braced", "headed", "bare". No typed interpretation at this stage. The
typed pass (realize/match) runs over these records just as the red tree runs
over green nodes.

Ropes are not in scope. The source text for a datom is read once; mutation
structures are irrelevant.

## Sources

- https://en.wikipedia.org/wiki/Rope_(data_structure)
- https://iq.opengenus.org/rope-data-structure/
- https://docs.rs/text-size/latest/text_size/struct.TextSize.html
- https://github.com/rust-analyzer/text-size
- https://docs.rs/rowan
- https://github.com/rust-analyzer/rowan
- https://willspeak.me/2021/11/24/red-green-syntax-trees-an-overview.html
- https://doc.rust-lang.org/stable/nightly-rustc/rustc_span/index.html
- https://tree-sitter.github.io/tree-sitter/using-parsers/2-basic-parsing.html
- https://github.com/tree-sitter/tree-sitter/issues/397
