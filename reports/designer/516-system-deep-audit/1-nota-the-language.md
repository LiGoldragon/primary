---
title: "NOTA — the language: brackets, positional records, the block root, and the codec"
role: designer
variant: Psyche
date: 2026-06-04
topics: [nota, nota-codec, nota-next, nota-box, codec, rkyv, parser, lexer, deep-audit]
---

# NOTA — the language

This is mechanism report #1 of the schema-derived-stack deep audit. It
explains what NOTA *is* at the language layer and proves it runs.
Every behavioural claim below is backed by a command I actually ran in
a named repo, with verbatim output pasted in. Where I could not run
something, I say so explicitly.

The four load-bearing properties this report establishes:

1. **Strings come EXCLUSIVELY from bracket forms.** There is no
   quotation-mark string in NOTA. A leading `"` is not a string
   opener — it is a hard lexer error.
2. **Records are POSITIONAL.** Type-or-variant first, then fields in
   declared order. No keyword labels inside a record; the Rust schema
   supplies the field names by position.
3. **The block-structured root.** `{}` for maps/imports, `[]` for
   sequences/declarations, `()` for records, and a file can be a bare
   *sequence of top-level values* with no outer wrapper.
4. **The codec.** Text parses to an AST, the AST re-encodes to byte-
   identical text, and the data types round-trip. rkyv enters at a
   precise, narrow place — and I pin exactly where.

The three focus repos and their layers:

| Repo | Crate | Layer |
|---|---|---|
| `nota-codec` | `nota_codec` | Typed text codec + generic `NotaValue` AST + lexer. The production contract surface for NOTA-text ⇄ Rust values. |
| `nota-next` | `nota_next` | Structural recursion floor: `Document`/`Block` tree with source spans, a second codec, and the rkyv-archivable macro-node mechanism. |
| `nota` (`nota-box`) | `nota_box` | The boxing/framing layer: length-prefixed NOTA framing for the signal wire (compact root + body). |

## 0. Versions and environment

Both codec crates are at version `0.1.0`. The deployed CLI is
`spirit`, and it parses a single NOTA argument.

```
$ ~/.nix-profile/bin/cargo --version
cargo 1.95.0 (f2d3ce0bd 2026-03-21)

$ grep -h "^version" .../nota-codec/Cargo.toml .../nota-next/Cargo.toml
version      = "0.1.0"
version      = "0.1.0"
```

The deployed `spirit` binary accepts NOTA directly. Run in
`/home/li/primary`:

```
$ /home/li/.nix-profile/bin/spirit "(Observe (Status))"
invalid request text: unknown variant `Status` for enum `Observation`
```

That error is itself the proof the argument is NOTA: `spirit` lexed
and parsed `(Observe (Status))` as a positional record, dispatched on
the head `Observe`, descended into the inner record `(Status)`, and
rejected `Status` because it is not a declared variant of the
`Observation` enum. The binary takes one NOTA argument wrapped in shell
double quotes — and the NOTA string itself contains no `"`, which is
exactly why shell double-quoting is safe.

## 1. Strings come EXCLUSIVELY from bracket forms

NOTA has three string surfaces, all bracket-based, and **zero**
quotation-mark surface:

- `[text]` — inline bracket string. One line, content between `[` and `]`.
- `[|text|]` — block / bracket-safe string. Multi-line, dedented,
  used when the content contains `]` or newlines.
- bare `camelCase` / `kebab-case` at a `String` schema position — an
  identifier-shaped atom read as string content. PascalCase is *not*
  bare-string-eligible (it is reserved for enum variants).

### 1.1 The lexer structurally cannot read a quoted string

The strongest evidence is at the tokenizer. The lexer's byte-dispatch
has an explicit branch that *rejects* a leading `"`. Run in
`/git/github.com/LiGoldragon/nota-codec`:

```
$ grep -n "'\"'\|b'\"'\|read_quoted\|QuotedString" src/lexer.rs
162:            b'"' => Err(Error::QuoteStringDelimiter { offset: self.pos }),
```

There is no `read_quoted` / `QuotedString` path anywhere — the only
mention of `"` in the lexer is the line that errors on it. A quotation
mark at token start is `Error::QuoteStringDelimiter`, full stop.

I exercised this live in a standalone demo crate
(`/tmp/nota-audit-demo`, depends on `nota-codec` and `nota-next` by
path; edits no repo source):

```rust
#[test]
fn quote_at_token_start_is_a_lexer_error() {
    use nota_codec::{Lexer, Error};
    let mut lexer = Lexer::new("\"not a string\"");
    let err = lexer.next_token().unwrap_err();
    assert!(matches!(err, Error::QuoteStringDelimiter { offset: 0 }), "got {err:?}");
}
```

```
$ cd /tmp/nota-audit-demo && cargo test --quiet
running 1 test
.
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

### 1.2 The encoder structurally cannot *emit* a quotation mark

The complement of the lexer: the encoder never produces a `"` as
string syntax. The inline-bracket writer escapes only backslash,
closing bracket, and the three whitespace controls — a `"` falls into
the catch-all `other` arm and is written verbatim as *content*, never
as a delimiter. Run in `/git/github.com/LiGoldragon/nota-codec`:

```
$ sed -n '/fn write_bracket_string/,/^}/p' src/encoder.rs
fn write_bracket_string(output: &mut String, value: &str) {
    output.push('[');
    for ch in value.chars() {
        match ch {
            '\\' => output.push_str(r"\\"),
            ']' => output.push_str(r"\]"),
            '\n' => output.push_str(r"\n"),
            '\t' => output.push_str(r"\t"),
            '\r' => output.push_str(r"\r"),
            other => output.push(other),
        }
    }
    output.push(']');
}
```

`write_string` (the entry point) picks one of three forms — block,
bare, or inline-bracket — and `"` never appears in any of them:

```rust
pub fn write_string(&mut self, value: &str) -> Result<()> {
    self.write_separator_if_needed();
    if should_write_block(value) {            // [| ... |]
        self.output.push_str("[|");
        self.output.push_str(value);
        self.output.push_str("|]");
    } else if Ident::new(value).is_bare_string() {   // bare camel/kebab
        self.output.push_str(value);
    } else {
        write_bracket_string(&mut self.output, value);   // [ ... ]
    }
    self.needs_space = true;
    Ok(())
}
```

### 1.3 Live witness: an apostrophe does NOT force quoting; brackets stay clean

The codec's bracket-string round-trip test pins this directly. Run in
`/git/github.com/LiGoldragon/nota-codec`, the file
`tests/bracket_string_round_trip.rs`, which decides between the three
forms. The test `apostrophe_content_does_not_force_double_quotes`:

```rust
#[test]
fn apostrophe_content_does_not_force_double_quotes() {
    let note = Note { text: "he said 'yes'".to_string() };
    let text = encoded(&note);
    assert_eq!(text, "([he said 'yes'])");
    assert!(!text.contains('"'));
}
```

And `closing_bracket_content_uses_block_form_to_avoid_escapes` shows
the form-selection escalating to `[| |]` when the content contains a
literal `]`:

```rust
let note = Note { text: "array[0]".to_string() };
assert_eq!(encoded(&note), "([|array[0]|])");
```

I reproduced the apostrophe case live in the demo
(`/tmp/nota-audit-demo`):

```
=== (2) typed round-trip through nota-codec Decoder/Encoder ===
source : ([he said 'yes'])
decoded: Note { text: "he said 'yes'" }
encoded: ([he said 'yes'])
contains a double-quote char? false
```

The whole `bracket_string_round_trip` suite passes — 15 tests, run in
`/git/github.com/LiGoldragon/nota-codec`:

```
     Running tests/bracket_string_round_trip.rs
test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

The escape-free property is *why* NOTA embeds inside any host whose
strings use double quotes (JSON, Rust, shell, env vars): a NOTA value
literally cannot contain the host's `"` delimiter, so no escaping is
ever needed. That is the same reason `spirit "(Observe (Status))"`
works with naive shell double-quoting.

## 2. Records are POSITIONAL

A NOTA record is `(Head field0 field1 …)`: a head value, then fields
in *declared order*. There are no `(key value)` labels inside a record
— that Lisp/JSON shape is explicitly rejected.

### 2.1 The AST shape, live

I parsed `(Edge 100 200 DependsOn)` through `nota_codec::parse_str` and
printed the real AST (`/tmp/nota-audit-demo`):

```
=== (1) nota-codec: text -> generic AST -> re-encode ===
source : (Edge 100 200 DependsOn)
ast    : Record([Atom(Identifier("Edge")), Atom(Integer(100)), Atom(Integer(200)), Atom(Identifier("DependsOn"))])
```

The `Record` is an *ordered* `Vec` of values. Position 0 is the head
identifier `Edge`; positions 1–3 are the fields. Nothing in the tree
carries a field name — the names live in the Rust schema the record is
decoded against. This is the `NotaValue` enum from
`nota-codec/src/value.rs`:

```rust
pub enum NotaValue {
    Record(Vec<NotaValue>),
    Sequence(Vec<NotaValue>),
    Map(Vec<NotaMapEntry>),
    Atom(NotaAtom),
}
```

`Record` and `Sequence` are both ordered `Vec<NotaValue>`; only `Map`
carries keys. Positionality is structural: a record literally has no
slot for a label.

### 2.2 The schema supplies field names by position

The typed round-trip test `multi_field_record_round_trips_with_mixed_field_types`
in `nota-codec/tests/nota_record_round_trip.rs` decodes the same
positional record into a typed `Edge` struct whose three fields are
named only in Rust:

```rust
#[derive(NotaRecord, ...)]
pub struct Edge { pub from: Slot, pub to: Slot, pub kind: RelationKind }

round_trip(Edge { from: Slot(100), to: Slot(200), kind: RelationKind::DependsOn },
           "(100 200 DependsOn)");
```

Note the wire is `(100 200 DependsOn)` — no `Edge` tag, no `from`/`to`/
`kind` labels. The struct type is fixed by the schema *position*; the
field order is fixed by declaration order.

### 2.3 Labeled-field shape is a typed error, not an alternative syntax

The decoder actively rejects the `(key value)` shape with a
diagnostic that points back at positional NOTA. From
`nota_record_round_trip.rs`:

```rust
#[test]
fn labeled_field_record_shape_display_points_to_positional_nota() {
    let mut decoder = Decoder::new("(Edge (from 100) (to 200) (kind Flow))");
    let err = Edge::decode(&mut decoder).unwrap_err();
    assert_eq!(err.to_string(),
        "NOTA records are positional; found labeled-field shape `(Edge (key value)...)`. \
         The contract declares `Edge` with 3 positional fields. \
         Did you mean `(Edge <field1> <field2> ...)`? See `skills/nota-design.md`.");
}
```

The full `nota_record_round_trip` suite passes — 8 tests, run in
`/git/github.com/LiGoldragon/nota-codec`:

```
     Running tests/nota_record_round_trip.rs
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

### 2.4 The three-case PascalCase rule

Positionality interacts with one more rule the tests pin: a bare
PascalCase token has exactly one meaning per position.

- Case 1 — `(VariantName fields…)`: PascalCase right after `(` is a
  *data-carrying enum variant tag*.
- Case 2 — `(field0 field1 …)` with no leading PascalCase: a struct
  record; type comes from position.
- Case 3 — a bare PascalCase atom (`DependsOn`, `Active`, `True`): a
  *unit enum variant*.

Because PascalCase is reserved for variants, it is **rejected at a
String position**. From `nota_record_round_trip.rs`:

```rust
#[test]
fn pascal_token_at_struct_start_is_rejected_as_string_content() {
    let mut decoder = Decoder::new("(Edge 100 200 Flow)");
    let err = Node::decode(&mut decoder).unwrap_err();
    match err {
        Error::PascalCaseAtStringPosition { content } => assert_eq!(content, "Edge"),
        ...
    }
}
```

This is why the `nota` repo's `example.nota` uses bare `nota`,
`ligoldragon` (kebab/camel content at String positions) but `Active`
and `True` as PascalCase variants.

## 3. The block-structured root

NOTA has three delimiter pairs, each with a fixed structural role, and
a file can be a *bare sequence of top-level values* with no outer
wrapper.

| Delimiter | AST node | Role |
|---|---|---|
| `( … )` | `Record(Vec<NotaValue>)` | positional record |
| `[ … ]` | `Sequence(Vec<NotaValue>)` | ordered sequence / declarations |
| `{ … }` | `Map(Vec<NotaMapEntry>)` | flat `{key value key value}` map |
| `[\| … \|]` | `Atom(String{Block})` | block string (NOT recursive) |

The pipe-square form `[| … |]` is text, not structure — it is the only
bracket form that does *not* descend into children. This is visible in
the parser dispatch (`nota-codec/src/value.rs`): an `LBracket`
immediately followed by `|` becomes a block string; a plain `LBracket`
becomes a sequence.

### 3.1 The six-value root, live

A `.schema`-shaped file is six top-level values with **no outer
record**: `{imports} [ordinary] [owner] [sema] {namespace}
[features]`. `nota_codec::parse_sequence` is the entry point that reads
a bare top-level value stream (`NotaValue::parse` rejects trailing
content after the first value; `parse_sequence` reads them all). Live
from `/tmp/nota-audit-demo`:

```
=== (1b) the six-value block-structured root of a .schema-shaped file ===
source : {serde [1]} [Active Removed] [ligoldragon] [Decision] {debug True} [v2]
count  : 6 top-level values
  [0] Map([NotaMapEntry { key: "serde", value: Sequence([Atom(Integer(1))]) }])
  [1] Sequence([Atom(Identifier("Active")), Atom(Identifier("Removed"))])
  [2] Sequence([Atom(Identifier("ligoldragon"))])
  [3] Sequence([Atom(Identifier("Decision"))])
  [4] Map([NotaMapEntry { key: "debug", value: Atom(Identifier("True")) }])
  [5] Sequence([Atom(Identifier("v2"))])
```

Six values, in order, no wrapping `( )`. Slot 0 and slot 4 are brace
*maps*; the rest are square-bracket *sequences*. The schema reader
walks these by position. The matching docstring in `value.rs` even
cites this shape: *"six top-level values
`{imports} [ordinary] [owner] [sema] {namespace} [features]` with no
outer record."*

The `value_shape` suite that pins the multi-value document path passes
— 9 tests, run in `/git/github.com/LiGoldragon/nota-codec`:

```
     Running tests/value_shape.rs
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

(notably `parse_sequence_reads_six_top_level_values_for_schema_files`
and `document_preserves_multiple_top_level_nota_values`.)

### 3.2 `nota-next`: the structural floor with source spans

`nota-codec` gives a generic value tree; `nota-next` gives a
*structural* `Document`/`Block` tree where every block carries a
`SourceSpan` (byte + line + column). This is the recursion floor that
runs *before* any schema is loaded — it recognizes delimiters and
spans without knowing what a "field" or "variant" means. Live from
`/tmp/nota-audit-demo`:

```
=== (3) nota-next: structural Document (Block tree) ===
source : "(Record\n  [Entry])"
root objects: 1
outer span start line/col/byte: 1/1/0
inner re-emitted from span: [Entry]
```

The inner `[Entry]` block is re-emitted *from its source span* — the
parser preserved the exact byte region, not a re-serialised
approximation. The `nota-next` `design_examples` suite pins this and
the at-binding/pipe-delimiter declaration syntax; the whole crate
passes:

```
$ cd /git/github.com/LiGoldragon/nota-next && cargo test
     Running tests/block_queries.rs    ... 8 passed
     Running tests/codec.rs            ... 8 passed
     Running tests/derive.rs           ... 8 passed
     Running tests/design_examples.rs  ... 7 passed
     Running tests/macro_nodes.rs      ... 5 passed
```

## 4. The codec — parse, encode, decode, and where rkyv actually lives

### 4.1 Text round-trip (the production contract)

The codec's job is: NOTA text → typed Rust value → byte-identical NOTA
text. The `round_trip` helper in every `nota_*_round_trip.rs` test
asserts *both* directions — encode produces the expected text, decode
recovers the value. I reproduced the typed leg live in
`/tmp/nota-audit-demo` (§1.3 above): `([he said 'yes'])` decodes to
`Note { text: "he said 'yes'" }` and re-encodes to the identical
string.

The whole `nota-codec` suite passes. Run in
`/git/github.com/LiGoldragon/nota-codec`:

```
$ cargo test     (per-binary results)
   unittests src/lib.rs                  ... 0 passed
   tests/box_form.rs                     ... 5 passed
   tests/bracket_string_round_trip.rs    ... 15 passed
   tests/compile_fail.rs                 ... 1 passed
   tests/horizon_rs_feedback_fixes.rs    ... 22 passed
   tests/lexer_tokens.rs                 ... 5 passed
   tests/map_key_round_trip.rs           ... 9 passed
   tests/nota_enum_data_round_trip.rs    ... 4 passed
   tests/nota_enum_round_trip.rs         ... 6 passed
   tests/nota_mixed_enum_round_trip.rs   ... 9 passed
   tests/nota_record_round_trip.rs       ... 8 passed
   tests/nota_transparent_round_trip.rs  ... 6 passed
   tests/nota_try_transparent_round_trip.rs ... 7 passed
   tests/option_vec_struct_variant.rs    ... 14 passed
   tests/path_round_trip.rs              ... 29 passed
   tests/production_primitives.rs        ... 25 passed
   tests/value_shape.rs                  ... 9 passed
```

Every binary reports `0 failed`. Total: 174 passing across the
`nota-codec` integration suite.

### 4.2 Where rkyv actually is — pinned precisely

The audit brief asks about the rkyv round-trip. Here is the honest,
verified placement, because it is easy to get wrong:

**The NOTA *text* codec does not use rkyv at all.** Parsing,
encoding, and decoding NOTA text is pure-text work in `nota-codec`,
which has no rkyv dependency in its own manifest. rkyv enters at one
narrow place in these three repos:

```
$ grep -rn "rkyv" .../nota-next/Cargo.toml
17:rkyv = { version = "0.8", default-features = false,
         features = ["std", "bytecheck", "little_endian",
                     "pointer_width_32", "unaligned"] }
```

That dependency exists so the **macro-node mechanism** types in
`nota-next/src/macros.rs` — `MacroNodeDefinition`, `PositionPredicate`,
`Pattern`, `CaptureName`, `MacroDelimiter`, etc. — derive
`rkyv::Archive + Serialize + Deserialize`. These types describe
structural patterns; making them rkyv-archivable lets a *compiled
macro registry* be serialized to the zero-copy signal wire format that
the daemon/signal crates downstream consume. The same types ALSO
derive `nota_next::NotaDecode + NotaEncode`, so they are dual-format:
NOTA text *and* rkyv bytes.

**No test in `nota-next` or `nota-codec` exercises an rkyv byte
round-trip.** I verified this — the test suites exercise NOTA *text*
round-trips, and a grep of the test directory for rkyv calls returns
nothing at all:

```
$ grep -rn "rkyv\|to_bytes\|from_bytes\|archived" .../nota-next/tests/
$
```

(zero hits — the `rkyv` dependency appears in `Cargo.toml:17`, but no
test under `tests/` exercises a byte round-trip.)

> **Correction (verification pass).** An earlier draft of this section
> pasted a single doc-comment line as the grep result here. That was a
> fabricated hit — re-running the exact command returns zero output, as
> shown above. The conclusion was and is correct (no rkyv-byte test
> exists); the invented line was removed. This is the one `partial`
> verdict in the 516 verification ledger; see `0-frame-and-method.md`
> §method.

So to *prove* the rkyv leg actually works, I exercised it myself in
the demo crate against the real `nota-next` `PositionPredicate` type —
serializing it to bytes with `rkyv::to_bytes` and deserializing with
`rkyv::from_bytes`, alongside the NOTA-text leg of the SAME value.
Live from `/tmp/nota-audit-demo`:

```
=== (4) SAME value: NOTA text codec AND rkyv byte round-trip ===
value      : Named("recordHead")
to_nota    : (Named [recordHead])
text round-trip eq? true
rkyv bytes : 19 bytes -> [72, 65, 63, 6f, 72, 64, 48, 65, 61, 64, 02, 8a, 00, 00, 00, f5, ff, ff, ff]
rkyv round-trip eq? true

ALL ASSERTS PASSED
```

Two things to read off this. First, the NOTA-text leg:
`PositionPredicate::Named("recordHead")` encodes to the positional
record `(Named [recordHead])` — head variant `Named`, one field as a
bracket string — and decodes back equal. Second, the rkyv leg: the
same value serializes to 19 bytes (note `72 65 63 6f 72 64 48 65 61 64`
is the ASCII for `recordHead`, with rkyv's relative-pointer + length
trailer) and deserializes back equal. One Rust type, two wire formats,
both round-trip.

### 4.3 The boxing/framing layer (`nota` / `nota-box`)

The `nota` repo's `nota-box` crate is the framing layer for the signal
wire: it wraps a NOTA value as a *compact root* plus a body so a reader
can find the root object's extent without parsing the whole payload.
Important correction to a natural assumption: **`nota-box`'s "binary"
form is NOT rkyv** — it is length-prefixed NOTA *text* framing, and
the crate depends only on `nota-codec`:

```
$ grep -n "rkyv\|nota-codec" .../nota/nota-box/Cargo.toml
16:nota-codec = { git = "https://github.com/LiGoldragon/nota-codec.git", branch = "main" }
```

The `round_trip.rs` test pins both legs. `entry_round_trips_binary`
goes value → `encode_binary` → bytes → `decode_binary` → value;
`entry_round_trips_text` shows the human form, a positional record
followed by bracket-string fields:

```rust
assert_eq!(text,
  "(Entry Decision Maximum) [workspace] [summary text] [context text] [verbatim quote]");
```

The whole `nota` crate passes. Run in
`/git/github.com/LiGoldragon/nota`:

```
$ cargo test
   unittests src/lib.rs            ... 0 passed
   tests/empty_boxes.rs            ... 2 passed
   tests/peek_box.rs              ... 2 passed
   tests/round_trip.rs            ... 4 passed
   tests/support.rs               ... 0 passed
```

## 5. Summary of the stack as run

```mermaid
flowchart TD
  text["NOTA text\n(Edge 100 200 DependsOn)"]
  lexer["nota-codec lexer\nrejects leading \" → QuoteStringDelimiter"]
  ast["nota-codec AST\nNotaValue::Record(Vec)\npositional, no labels"]
  typed["typed Rust value\nschema names fields by position"]
  span["nota-next Document/Block\nsource spans, recursion floor"]
  macro["nota-next macro-node types\nNotaEncode/Decode + rkyv::Archive"]
  rkyv["rkyv bytes\nsignal wire (downstream)"]
  box["nota-box framing\nlength-prefixed NOTA text\n(NOT rkyv)"]

  text --> lexer --> ast
  ast <--> typed
  text --> span
  typed --> box
  macro <--> ast
  macro <--> rkyv
```

The reading order of the evidence: the lexer forbids quotes (§1.1), the
encoder cannot emit them (§1.2), records are ordered `Vec`s with no
label slot (§2.1), the schema names fields by position (§2.2), labeled
shape is a typed error (§2.3), the root can be a bare six-value stream
(§3.1), `nota-next` adds spans as the recursion floor (§3.2), the text
codec round-trips byte-identically (§4.1), rkyv lives only on the
macro-node types and I proved its byte round-trip live (§4.2), and the
`nota-box` "binary" form is NOT rkyv but length-prefixed text (§4.3).

## 6. What I could NOT run / caveats

- **No in-repo rkyv test exists**, so the rkyv byte round-trip in §4.2
  is my own demo against the real `nota-next` type, not an existing
  repo test. I was explicit about this. The `nota-next`/`nota-codec`
  suites only round-trip NOTA *text*.
- The exact downstream consumer of the rkyv-archived macro registry
  (the signal-encoded files the brief mentions) lives in the *signal*
  crates, which are outside this report's three focus repos; I did not
  trace them here.
- `spirit "(Observe (Status))"` is a deliberate invalid-variant probe
  to show NOTA parsing — I did not construct a valid `Observe` request,
  so I show the parser reaching the schema layer, not a successful
  observation.
