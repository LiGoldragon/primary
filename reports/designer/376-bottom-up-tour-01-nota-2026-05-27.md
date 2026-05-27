# 376 — Bottom-up tour, Layer 1: NOTA

*Psyche-verification tour, one layer at a time (record 868,
[verification] [explanation-discipline] Clarification, High).
This is Layer 1. The full tour: NOTA → schema-next → schema-rust-next
→ signal-frame.schema → spirit.schema (consumer) → runtime triad
(Signal/Executor/SEMA inside the daemon) → federation as design
pressure. Each layer one report; psyche reads, points at anything
that diverges from intent, then "next" for the layer up.*

## Frame

NOTA is the bottom of what we BUILT. Below NOTA is rkyv, the
zero-copy byte-level archival format upstream of everything (we
didn't write rkyv — Anthropic-unaffiliated upstream crate). Per
intent records 839-844 (Maximum), the relation is:

> **NOTA is the specification language for portable rkyv.** It is
> a superset of CapnProto with a module system, a macro system,
> and shape-driven node-type matching.

Two halves to discuss in this report:

1. **NOTA the LANGUAGE** — grammar, design rules, the bracket-
   string property, why every PascalCase token is one of three
   precise things, why positional records are the only record
   shape.
2. **`nota-next` the IMPLEMENTATION** — the structural reader at
   `/git/github.com/LiGoldragon/nota-next/`, what types it
   exposes, what it deliberately REFUSES to know, where the
   boundary to the schema layer sits.

## Part A — NOTA the language

### Why NOTA exists at all

The substrate problem NOTA solves: every Anthropic component
needs a way to carry typed data — over a wire, on disk, in a CLI
argument, in a daemon's state — in a form that round-trips
losslessly with rkyv binary and is also human-readable and
agent-greppable. JSON has too many shapes that don't map to
typed records, too many escape cascades, and no enum variant
syntax. Lisp is closer but uses `(key value)` pairs and is
verbose. NOTA picks: **positional records (no labels), three
delimiter forms, exclusively bracket strings, one shape of
list, one shape of map.**

The non-obvious design property — the one the psyche specifically
called out (your earlier statement: *"this makes nota also able
to fit most string-containing blocks in many languages — JSON,
rust nix and many more"*) — is **escape-free embedding**.
Because NOTA never emits `"` (the canonical encoder structurally
cannot), a complete NOTA expression embeds inside any host whose
string syntax uses double quotes — JSON values, Rust string
literals (including raw `r"..."`), Nix attributes, YAML scalars,
TOML strings, shell double-quote arguments, HTTP bodies, database
columns, environment variables, XML attributes — with no escape
cascade. JSON-in-JSON requires escape stacking; NOTA-in-anything-
with-double-quote-strings is escape-free. This is load-bearing,
not incidental.

### The grammar — five things

Per `nota-next/ARCHITECTURE.md` (the authoritative floor) and
`skills/nota-design.md` (the discipline):

1. **Atom** — a leaf token. PascalCase symbol, camelCase symbol,
   kebab-case symbol, integer candidate, or decimal candidate.
   Classification is the candidate's *shape*, not its type — the
   schema layer above decides what type each candidate is.
2. **Delimited object** — `(...)` parenthesis, `[...]` square,
   `{...}` brace. Three flavours, three meanings (record/enum,
   sequence, map).
3. **Pipe-text** — `[|...|]` block-safe string. The contents can
   contain `[`, `]`, `"`, newlines, apostrophes — anything except
   the closing `|]` pair. This is the *block* form of string.
4. **Inline bracket string** — `[content]` where `content` is a
   single-line string body that doesn't contain `[` or `]`.
5. **Bare-token shorthand** — at a `String` schema position, a
   bare camelCase or kebab-case token is equivalent to its
   bracket form. `nota-codec` ≡ `[nota-codec]`. PascalCase bare
   is reserved for enum variants (case 3 below) and is rejected
   at `String` positions.

There are also two sigils — `;;` for line comments, `#` for byte
literals — and that's all. `~ @ ! ? * =` are reserved at the
syntax layer (parsing them in pure NOTA is an error) — whatever
eventually claims them is outside the schema-derived stack's
concern.

**Sigils don't carry macro semantics.** Schema-next's macros are
plain NOTA records dispatched by position and shape — see Part B
below for the layer separation, and Layer 2 of this tour for the
mechanism in depth.

### PascalCase falls into exactly three cases

This is the load-bearing rule from `skills/nota-design.md` and
the canonical recurring agent-mistake fixer:

1. `(VariantName fields…)` — **data-carrying enum variant.**
   Opening `(` immediately followed by PascalCase means: this is
   an enum variant; the following tokens are its fields,
   positional.
2. `(fields…)` with no leading PascalCase — **struct.** No tag.
   The schema position tells the reader which struct this is.
3. Bare `VariantName` with no preceding `(` — **non-data-carrying
   unit variant.** Like `None`, `Maximum`, `Apex`, `Decision`,
   `High`.

The corollary: *can this position carry more than one shape?*
Yes → enum, every record needs a variant tag or is a unit. No →
struct, no tag.

Everything else is primitives, sequences `[...]` (where every
element shares one schema type — homogeneous), and maps `{...}`
(odd positions are key text, even are values).

### Strings come exclusively from brackets

Three string forms, no fourth:

- `[content]` — inline (cannot contain `[` or `]`)
- `[|content|]` — block (can contain anything but `|]`)
- bare camelCase / kebab-case token at a String position
  (rejected if PascalCase)

The encoder in `nota-codec` has three `write_string` branches and
no fourth quote branch. The lexer accepts legacy `"..."` quoted
strings as **migration input only** — explicitly named
`read_legacy_quote_string`. A legacy → canonical round-trip
SHEDS the quotation marks. Removal is authorized once all
upstream emitters migrate (bead `primary-jdzy`).

### Positional records — no `(key value)` pairs

The biggest agent-mistake-shape NOTA prevents: `(Decision
(description [text]) (magnitude Maximum))` is NOT NOTA — it's
Lisp/Clojure/JSON in NOTA syntax. The NOTA shape is
`(Decision [text] Maximum)`. Every position in the text carries
the position the schema declares; no keywords inside records;
tail omission is a typed error, not a silent zero-fill.

### Vec — one bracket per sequence

A homogeneous list is ONE `[...]`. Multiple items go INSIDE.
`[verification explanation-discipline]` is a `Vec<Topic>` of
two strings. `[verification] [explanation-discipline]` would
be TWO sequences side-by-side, which is what tripped record 868
on the first attempt — the parser saw the second `[` where the
schema expected the next field's PascalCase.

This is the kind of mistake the typed record schema catches at
the deployed daemon's parser, exactly as designed.

### Option — never tail-omission

`Option<T>` is a standard data-carrying enum. Absence is bare
`None`; presence is `(Some inner)`. The pattern `tail omission
to mean None` is forbidden by `nota/README.md`. The
`#[nota(default = ...)]` attribute is forbidden too. A record
short on tokens is a typed parse error, not a default fill.

### No tuples, no labeled fields

Tuples (`struct Pair(i32, i32)` and friends) are rejected at
serialize time — they carry position but not field names, and
field names are information. Schema-emitted Rust uses **named-
field** structs, which emit as untagged struct records (case 2
of the PascalCase rule).

## Part B — nota-next, the structural reader

### What `nota-next` is for

Per `nota-next/README.md`:

> `nota-next` is the replacement implementation of NOTA's
> structural reader. It is intentionally narrow: it reads
> delimiter-balanced NOTA into blocks, keeps source spans,
> exposes recursive object queries, and classifies atoms as
> structural candidates. Schema semantics live in `schema-next`,
> not here.

The layer separation is sharp and load-bearing: nota-next knows
NOTHING about what a type, schema, field, enum, macro, or import
is. It exposes the structure the next layer needs to compute
those things, and refuses to compute them itself.

The crate has two source files (`src/lib.rs`, `src/parser.rs`)
and one test file (`tests/block_queries.rs`). That's by design —
a narrow surface should look narrow.

### The public type surface

From `src/lib.rs:11-14`:

```rust
pub use parser::{
    Atom, AtomClassification, Block, Delimiter, Document,
    NotaError, PipeText, SourcePosition, SourceSpan,
};
```

Nine types, no traits. Let me describe each.

| Type | Role |
|------|------|
| `Document` | Top-level — ordered list of root `Block`s plus the source string for `reemit` lookups. |
| `Block` | One of: delimited object, pipe-text object, or atom. The recursive unit. |
| `Atom` | A leaf — PascalCase symbol, camelCase symbol, kebab-case symbol, integer candidate, decimal candidate. |
| `AtomClassification` | The shape-classification of an atom (`IntegerCandidate`, `DecimalCandidate`, etc.). Not a schema type. |
| `Delimiter` | Which paren shape: `(`, `[`, `{`. |
| `PipeText` | `[|...|]` block-string content + its span. |
| `SourcePosition` | `{line, column, byte}` triple. |
| `SourceSpan` | Range of `SourcePosition`s. |
| `NotaError` | `UnclosedDelimiter { position, .. }` and friends. |

### Method discipline — `is_*` vs `qualifies_as_*`

This is the verbal contract that keeps the boundary honest.
From `ARCHITECTURE.md`:

- **Factual methods use `is_*`.** They name what something
  syntactically IS at the structural floor. `is_parenthesis()`,
  `is_brace()`, `is_square_bracket()`, `is_pipe_text()`. Pure
  delimiter facts, no schema interpretation.
- **Structural candidate methods use `qualifies_as_*`.** They
  name what something could BE at the next layer up.
  `qualifies_as_pascal_case_symbol()`,
  `qualifies_as_kebab_case_symbol()`,
  `qualifies_as_camel_case_symbol()`. These don't claim
  "this IS a type name" — they claim "this token's *shape*
  is consistent with being interpreted as one."

The verbal split keeps the layer-boundary visible in the call
site. If you read `block.qualifies_as_pascal_case_symbol()`,
you know you're at the schema-decisioning boundary; if you read
`block.is_parenthesis()`, you're at the parser floor.

### Recursive shape queries

The reader exposes recursive-descent without committing to what
the descent MEANS. Methods seen in the tests:

- `document.holds_root_objects()` → count of root-level blocks
- `document.root_object_at(i)` → `Option<&Block>` for index `i`
- `document.root_objects()` → slice over root blocks
- `document.source()` → the original source string
- `block.root_object_at(i)` / `block.root_objects()` — same
  pattern, recursive into child blocks
- `block.holds_two_root_objects()` — predicate for "I have
  exactly two children" (the schema layer wants this for shape-
  testing `(VariantName payload)` records)
- `block.reemit(source)` — reproduce the original textual form
  from the span
- `block.demote_to_string()` — convert a PascalCase symbol or a
  pipe-text into its underlying `&str` content

That last verb — **`demote_to_string`** — is interesting. It's
not "get text"; it's "demote." The implication: a typed symbol
or block-string IS structurally richer than a plain string, and
flattening it to a string is *losing information* (the symbol
shape, the span). The schema layer asks for the demotion when
it needs to consume the textual content; the reader doesn't do
it automatically.

### Source spans through every block

Every `Block` carries its `SourceSpan` so two things work:

1. **Diagnostics.** When the schema layer rejects a record, it
   can point at the exact byte/line/column where the offending
   token sits.
2. **Reemit.** Macro passes (schema-next layer above) can take
   a Block and reproduce its original text — so a macro can,
   for example, splice the original source of an input argument
   into an expanded output without rebuilding it from the AST.

This second use is load-bearing for the macro engine in
schema-next; without spans, macro expansion would have to
re-serialize each argument from the AST and risk format drift.

### Pipe-text is bracket-safe AND not recursively parsed

This is one of the most important design constraints. From the
test (`tests/block_queries.rs:53-64`):

```rust
let source = "[|macro body with ] and \" and apostrophe's text|]";
let document = Document::parse(source).expect("valid nota");
let root = document.root_object_at(0).expect("root");

assert!(root.is_pipe_text());
assert_eq!(
    root.demote_to_string(),
    Some("macro body with ] and \" and apostrophe's text")
);
assert_eq!(root.reemit(document.source()), source);
```

The content of a `[|...|]` block carries `]`, `"`, and `'`
unescaped, AND the reader does NOT recurse into it. That means
a macro body that contains its own NOTA can be carried as
opaque text until the macro engine wants to re-parse it; the
reader doesn't pre-empt that decision.

### What `nota-next` REFUSES to know

This is the boundary discipline that gives the layer its
identity. Per the architecture's "Boundary" section:

> This crate does not know what a type, field, schema, enum,
> macro, or import means. It only exposes the structure needed
> by the next layer.

Concretely, nota-next does NOT:

- map `PascalCase` symbols to any specific enum variants
- know what `Record`, `Decision`, `Maximum`, etc. mean
- know that `(ImportAll [path])` is an import (it just sees a
  paren-block with two root objects, the first qualifying as
  PascalCase, the second a square-bracket containing a string)
- know that `(Macro Input+ Output)` is a macro declaration
- know what types `Vec`, `Option`, `Some`, `None` are bound to
- attempt to parse byte-level rkyv (rkyv is the upstream
  binary form NOTA SPECIFIES; the reader doesn't go BELOW its
  own grammar)
- accept legacy `"..."` quoted strings (the legacy lexer path
  lives in the OLD `nota-codec` crate, not here — the
  replacement track has no legacy compatibility)

This discipline matters because every higher layer (schema-next,
schema-rust-next, signal-frame.schema, spirit.schema, runtime
triad) builds on the assumption that nota-next IS the
delimiter-and-span surface and NOTHING MORE. If it crept into
schema decisions, the macro engine and emitter would need to
disagree with it at decision points, and the boundary would
soften.

### Worked example — what the reader sees

Source:

```
(Record [verification explanation-discipline] Clarification [psyche directive...] High)
```

What `nota-next` reports:

- 1 root object — a parenthesis-delimited block
- That root has 5 children:
  1. Atom `Record`, classified `PascalCaseCandidate`
  2. Square-bracket block holding 2 children: kebab-case atoms
     `verification` and `explanation-discipline`
  3. Atom `Clarification`, classified `PascalCaseCandidate`
  4. Square-bracket block holding 1 child: a string-content
     block with `psyche directive...`
  5. Atom `High`, classified `PascalCaseCandidate`
- Every child has its `SourceSpan` so diagnostics or reemit work

What `nota-next` does NOT report:

- That this is a `Record` operation
- That `Clarification` is a `Kind` variant
- That `High` is a `Magnitude` variant
- That the inner square-bracket is a `Vec<Topic>`
- That `psyche directive...` should be the `description` field
- That this is even an intent record — `nota-next` doesn't know
  Spirit exists

All of that interpretation is in schema-next + the consumer
schema. nota-next just produces the recursive structural tree.

## How the layer above consumes this

`schema-next` (the macro engine, Layer 2 of the tour) reads
`Document` → `root_objects()` → recursively descends through
`Block`s — classifying each into a schema node type by:

1. **What delimiter is it?** `is_parenthesis()` /
   `is_brace()` / `is_square_bracket()` / `is_pipe_text()`.
2. **Does the first child qualify as PascalCase?** That makes
   it a case-1 enum variant or case-2 macro head; if not it's
   case-2 struct or a non-tagged shape.
3. **Demote tokens to strings only where needed** — preserving
   the structured form everywhere else.

The macro engine in schema-next then walks this tree applying
fixed-point macro expansion (covered in Report 2). The Rust
emitter in schema-rust-next walks the FINAL (post-expansion)
tree and emits Rust type declarations (Report 3).

The reader's job ends at the parse-and-classify step. Every
higher layer is on top of THIS surface.

## Verification anchors

If you want to point at any specific claim in this report:

| Claim | File / Line |
|-------|-------------|
| Three string forms | `skills/nota-design.md:172-204` |
| PascalCase three cases | `skills/nota-design.md:138-167` |
| Positional records, no labels | `skills/nota-design.md:280-313` |
| Vec is ONE bracket | `skills/nota-design.md:152-167` |
| Option is `None` / `(Some ...)`, never tail | `skills/nota-design.md:258-265` |
| `nota-next` is the structural reader | `nota-next/README.md:1-9` |
| `nota-next` REFUSES schema semantics | `nota-next/ARCHITECTURE.md:15-17` |
| `is_*` factual vs `qualifies_as_*` candidate | `nota-next/ARCHITECTURE.md:11-12` |
| Pipe-text is bracket-safe and not parsed | `nota-next/tests/block_queries.rs:53-64` |
| Recursive root-object queries | `nota-next/tests/block_queries.rs:18-32` |
| Atom classifications without schema | `nota-next/tests/block_queries.rs:34-50` |
| Unclosed delimiter has source position | `nota-next/tests/block_queries.rs:66-77` |
| Embedding-safe escape-free property | `skills/nota-design.md:223-233` |
| Specification language for portable rkyv | intent records 839-844 |

## What's settled, what's drifted, what's open

**Settled in code AND in discipline:**
- Three string forms, no quote emission
- Three-case PascalCase rule
- Positional records (no labels)
- `is_*` vs `qualifies_as_*` verbal contract
- Recursive structural query API
- Source spans through every block
- Pipe-text is not recursively parsed
- The layer boundary (no schema semantics in nota-next)

**Settled in discipline but not yet enforced by code:**
- Legacy quote-removal sweep (bead `primary-jdzy`) — the OLD
  `nota-codec` still accepts `"..."`; the NEW `nota-next` does
  NOT have a legacy lexer at all. So `nota-next` itself is
  clean; the cleanup is in legacy emitters elsewhere.

**Open question that surfaced during /374:**
- The schema language's representation of `Vec<X>` was the 10%
  gap from /374 — Spirit v0.3 in design-deep-spirit emitted
  `RecordList` truncated to the first record. This is a
  schema-next / schema-rust-next concern, NOT a nota-next
  concern. nota-next's `[...]` sequence reading is fine; the
  emitter's `Vec<T>` codec is the gap.

**Not yet present:**
- A reflective schema for nota-next ITSELF (the recursion
  floor). Per /363's hybrid finding: nota-next stays HAND-
  AUTHORED in Rust; types can be emitted from a nota.schema
  but byte-level recognition must stay hand-authored. This
  layer's incumbent is by design.

## Coverage check — did this Report 1 cover "every bit"?

Of the NOTA layer specifically: yes. Below is what I claim to
have covered, so the psyche can spot anything missing:

- [x] Why NOTA exists (specification language for portable rkyv)
- [x] Embedding-safety design property
- [x] Five grammar elements (atom, paren, square, brace, pipe-text)
- [x] PascalCase three cases
- [x] Strings exclusively from brackets
- [x] Positional records
- [x] Vec / Option / no tuples / no labeled fields
- [x] nota-next type surface
- [x] is_* vs qualifies_as_* verbal contract
- [x] Recursive query API
- [x] Source spans
- [x] Pipe-text bracket-safe and not parsed
- [x] Layer boundary (what nota-next refuses to know)
- [x] How the next layer consumes the reader
- [x] Verification anchors

If anything below this layer matters (the rkyv byte form, the
nexus extensions reserved for `~ @ ! ? *`, the `=` sigil
reservation, byte literal `#`), say so and I'll go deeper.

## What's next in the tour

**Report 2 — schema-next**, the macro engine. The substrate
where `nota-next` blocks become typed schema declarations, where
`(Macro Input+ Output)` declares macros, where fixed-point
expansion resolves them, where `(ImportAll [path])` brings in
other schemas, and where the canonical `.asschema` serialization
plus Blake3 hash anchors a schema's identity. This is the layer
the /208 P1 gap closed in /375 — what was a stub a session ago
is now real engine with 21 tests.

When you're ready: "next" and I write Layer 2.
