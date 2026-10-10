# Witness: datom current syntax

Date: 2026-08-26

## Repositories checked

Method: probe `ls /git/github.com/LiGoldragon/`

Present and active: `datom`, `protos`, `nota`, `dotos`, `ethos-monolith`.
No repository named `ethos` or plain `nota` under a different name was found separate from the listed ones.
`nota` and `dotos` share the same commit log tip (`d97dd5c docs: integrate Protos estate status`), suggesting they are published as a pair.

## Freshness

Method: probe `git log --format="%ad %s" --date=short` in each repo.

datom most recent: `2026-08-25 datom: expose typed external root surface`
protos most recent: `2026-08-15 protos: resolve grouped bare-self imports`

Both active as of August 2026.

## Substrate ownership (protos)

Method: code read `/git/github.com/LiGoldragon/protos/src/shape.rs`
Method: code read `/git/github.com/LiGoldragon/protos/src/block.rs`
Method: code read `/git/github.com/LiGoldragon/protos/README.md`
Method: code read `/git/github.com/LiGoldragon/protos/ARCHITECTURE.md`

Protos owns the lexical first pass. The nine shapes are the complete vocabulary:

```
Shape::Bare
Shape::Parenthesized        (...)
Shape::DottedParenthesized  Head.(...)
Shape::CurlyQuoted          "..."
Shape::DottedCurlyQuoted    Head."..."
Shape::SquareBracketed      [...]
Shape::DottedSquareBracketed Head.[...]
Shape::Braced               {...}
Shape::DottedBraced         Head.{...}
```

`shape.rs:7-21`

## Head (dotted prefix)

Method: code read `/git/github.com/LiGoldragon/protos/src/block.rs:7-10`

`Head(String)` is the dotted prefix. A bare atom that ends with `.` followed by a structural/string delimiter is a dotted block. A trailing `.` with no following delimiter is `WalkFault::InvalidHead`. A Head that is empty is also `InvalidHead`.

Code site: `block.rs:119-128`

## String forms

Method: code read `/git/github.com/LiGoldragon/protos/src/block.rs` — scanner impl.

### Bare

`StringCarrier::Bare(body)`. Body is any non-whitespace sequence that does not start or end with a structural character. Body is the string value as-is. `block.rs:167-178`

### Parenthesized `(...)`

`StringCarrier::Parenthesized(body)`. Inner `(` increments depth; `)` at depth 0 closes. Backslash escapes: `\\` → `\`, `\(` → `(`, `\)` → `)`, any other `\x` preserves both characters. `block.rs:237-261`

### Curly-quoted `"..."`

`StringCarrier::CurlyQuoted(body)`. Unicode open/close curly quote pair (`\u{201C}` / `\u{201D}`). Backslash escape: same rule as parenthesized (only `\\` and the closer). `block.rs:263-280`. Accepted as legacy input; canonical output does not emit it.

### Blocks inside structural containers

Inside `{...}` or `[...]`, balanced nested `{`, `[`, parenthesized strings, and curly-quoted strings are kept opaque. The string scanner is called inline for `(` and `"` encountered inside a structural scan. `block.rs:283-330`

## Structs (braces `{...}`)

Method: code read `datom/src/datom.rs` — `DatomRoot::textualize_source`, `Group`, `Report`, `Serve`.

Top-level document root: `Head.{body}`. Consumer records use positional field order. Variants carry their own `Head.{payload}`. Field bodies are headless within their context.

Example from test: `Request.{ Serve.{ true curriculum-deploy [...] Map.[...] } }` `datom/tests/external_surface.rs:184`

## Enums / variants

Method: code read `datom/src/datom.rs:286-310` (`DatomRoot::textualize_source`) and `ShapeDefined for Entry`.

Variants are headed braced blocks: `VariantName.{payload}`. The root document is always `RootHead.{one-variant-body}`. `Entry` variants use `Note.(...)`, `Group.{...}`, `Tags.[...]`. `Inspect.{path}` is another example. `datom/tests/external_surface.rs:215-220`

## Maps (square-bracket with `Map.` head)

Method: code read `datom/src/datom.rs:390-445` (BTreeMap realize/textualize).

Generic map: `Map.[key.[value] key2.[value2]]` — each entry is `Key.[single-value]`.
Concrete `Report` text-map: bare `key.value` or `key.(value)` for single text values. `datom/src/datom.rs:980-1005`

Key constraints: non-empty, no dots, must parse as a valid bare head candidate. `datom/src/datom.rs:569-591`

Keys containing dots or delimited keys followed by `.` are unsupported; they return `DatomProblem::AmbiguousMapPair`. `datom/README.md` (last paragraph of Map section).

## Vectors (square brackets `[...]`)

Method: code read `datom/src/datom.rs:370-388` (`Vec<T>` realize/textualize).

Headless `[...]`. Canonical projection: `[elem elem elem]`. One space between blocks in output (protos canonical rule). `protos/README.md` ("one space between adjacent blocks").

## Booleans

Method: code read `datom/src/datom.rs:330-355`.

Bare atoms `true` and `false`. No other forms accepted. Textualizes to `true` / `false`.

## Numbers

Method: probe `grep -rn "i32\|i64\|u64\|integer\|float" datom/src/datom.rs`

Not implemented in datom or protos. No numeric `DatomRealizing` impl exists. Numbers read as bare strings only if the consumer treats them as `String`.

## Unit / absent

Method: code read `datom/src/datom.rs` — `OptionalText`.

`Option`-like is encoded as bare `None` or `Some.bare-value` / `Some.(value)`. No generic `Option<T>` impl; `OptionalText` is concrete. `datom/src/datom.rs:780-820`

No first-class unit/absent type exists in protos itself.

## Comments

Method: probe `grep -n "comment\|;;\|#" protos/src/block.rs`

No comment syntax in the scanner. Protos treats all non-whitespace tokens as block starts. Comments are not implemented.

## Whitespace / newline handling

Method: code read `protos/src/block.rs:108-116`.

All Unicode whitespace (including newlines) between blocks is consumed and discarded. Inter-block trivia is not retained. Canonical output (textualizing) emits one ASCII space between blocks.

## Round-trip (textualize)

Method: code read `datom/tests/substrate.rs:42-56` and `datom/tests/external_surface.rs:196-205`.

`textualize_source()` emits canonical form: no extra spaces, no curly-quote carriers, no trailing newline. Parenthesized projection is chosen only when bare form would be ambiguous. The round-trip test in `substrate.rs` asserts `again.textualize() == canonical` after `source.realize() → report.textualize() → canonical.realize()`.

Canonical output for the external_surface test:
`"Request.{Serve.{true curriculum-deploy [/etc/curriculum /srv/runtime] Map.[mode.[fast] source.[local]]}}"`
`datom/tests/external_surface.rs:198-203`

## Grammar / spec documents

Method: probe `find datom protos -name "*.md"`.

- `datom/README.md` — describes the typed surface and map/string rules. References `structuredStringType.md` and bead `primary-xqb.8.5` for meaning deferral.
- `datom/ARCHITECTURE.md` — single-walk design rationale.
- `protos/README.md` — trait roster and substrate boundary.
- `protos/ARCHITECTURE.md` — structural division diagram, scoping rules.

No standalone grammar file (e.g. EBNF) or `.datom`/`.dotos` example files found in either repository.

## Observations

- Numbers, explicit unit, and comments are not part of the implemented syntax.
- Curly-quote strings are accepted on input but never emitted on output (legacy carrier).
- Meaning of string contents (markup, structured types) is explicitly deferred per `datom/README.md`.
- `nota` and `dotos` are separate repos; their syntax is DOTOS, not Datom.
- Map key dot-containment and delimited-key-followed-by-dot cases are deliberately unsupported with a `DatomProblem::AmbiguousMapPair` fault.

## Unknowns

- The bead `primary-xqb.8.5` and `structuredStringType.md` that `datom/README.md` cites are not in these repositories; their content is unknown from this read.
- Whether `nota` re-uses `protos` as its substrate or is independent was not determined in this pass.
