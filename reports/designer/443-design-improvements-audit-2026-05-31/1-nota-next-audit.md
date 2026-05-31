# 1 — nota-next design audit

*Kind: audit · 2026-05-31 · designer lane sub-agent*

## Scope

Read in full:

- `/git/github.com/LiGoldragon/nota-next/src/lib.rs` (29 lines)
- `/git/github.com/LiGoldragon/nota-next/src/codec.rs` (542 lines)
- `/git/github.com/LiGoldragon/nota-next/src/parser.rs` (996 lines)
- `/git/github.com/LiGoldragon/nota-next/src/macros.rs` (956 lines)
- `/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs` (438 lines)
- All four test files under `tests/`
- `nota-next` `AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`

Read partially (for consumer-side evidence of substrate gaps; not audited
themselves):

- `/git/github.com/LiGoldragon/schema-next/src/asschema.rs`,
  `declarative.rs`, `macros.rs`
- `/git/github.com/LiGoldragon/spirit-next/src/schema/lib.rs`

Out of scope: schema-next, schema-rust-next, spirit-next as a whole. Asschema
known-root encoding (covered by designer 442).

Spirit records consulted: 1263, 1278, 1279, 1280 via
`(Observe (RecordIdentifiers ((Range (1263 1280)) WithProvenance)))`.

## Finding 1 — Delimiter opening/closing text is private; consumers re-encode it

`Delimiter` carries the load-bearing knowledge "this enum maps to these two
strings" in two methods:

- `codec.rs` private `closing(self) -> char` at `parser.rs:244-252`
- `codec.rs` private `opening_text(self) -> &'static str` at `parser.rs:254-262`

Both are `fn`, not `pub fn`. They are used inside the parser, and
`opening_text` is also reached by `NotaError::Display`. They are NOT exposed
on the public `Delimiter` surface.

Result: every consumer that emits NOTA reconstructs the same 5-arm match.
Two concrete duplications observed:

- `schema-next/src/declarative.rs:1845-1862` —
  `DelimitedNotation::opening` and `closing` are pixel-identical to
  nota-next's private methods. Lives at the bottom of a 2000-line file,
  hidden as a "notation helper".
- `schema-next/src/asschema.rs:1283-1308` —
  `SchemaNodeDelimitedNotation` re-encodes the same table, plus a `wrap`
  method that does `format!("{}{}{}",...)`.

A third nearly-identical use exists inline at `schema-next/src/asschema.rs:707-710`
for `TypeReference` encoding (`format!("(Plain {})", ...)`, etc.), where
the parenthesis literal is hard-coded.

This is a layering inversion in the reverse direction: nota-next OWNS the
data (which delimiter maps to which text), but won't share it. Consumers
hand-roll the table because they have no other option.

**Missing surface**: `Delimiter::opening_text()` and
`Delimiter::closing_text()` as `pub fn`. Plus, since the pattern
`format!("{open}{children.join(" ")}{close}")` repeats, a thin
`Delimiter::wrap(&[String]) -> String` (or, better, `Delimiter::wrap(impl
IntoIterator<Item = String>) -> String`) would let consumers emit a
delimited block in one call.

Impact: kills the entire `DelimitedNotation` (32 lines) and
`SchemaNodeDelimitedNotation` (40 lines) helper structs in schema-next, plus
the inline format!s in `TypeReference::to_nota` (8 lines).

## Finding 2 — Pattern and ChildPattern are duplicated trees in macros.rs

Inside nota-next itself, `Pattern`, `PatternElement`, `DelimitedShape` have
shadow twins `ChildPattern`, `ChildPatternElement`, `ChildDelimitedShape`.

The shapes:

- `Pattern { elements: Vec<PatternElement> }` at `macros.rs:183-221`
- `ChildPattern { elements: Vec<ChildPatternElement> }` at `macros.rs:536-574`

The `matches` methods are syntactically identical except for the element
type name. The element enums:

- `PatternElement` at `macros.rs:245-298`:
  `Any | Atom | Delimited(DelimitedShape) | Literal | Rest`
- `ChildPatternElement` at `macros.rs:587-640`:
  `Any | Atom | Delimited(ChildDelimitedShape) | Literal | Rest`

Identical variant set; the only difference is the `Delimited` payload —
`DelimitedShape` allows recursive `children: Option<ChildPattern>`,
`ChildDelimitedShape` does not.

`DelimitedShape::match_block` and `ChildDelimitedShape::match_block` are
near-identical (`macros.rs:503-523` vs `676-692`).

This forced fork is a NESTING-DEPTH limitation, not a semantic one: child
patterns can't go deeper than one level. Per intent record 1263 (macro
nodes at NOTA layer) and 1279 (NOTA extension programming is structural
matching over nodes), a full structural language should compose to any
depth. The current shape implies "one level of child constraint" because
the recursion was clipped to avoid serialization bounds problems (the
rkyv `serialize_bounds` annotation at `macros.rs:234-244` only goes one
level).

**Missing abstraction**: collapse to a single `Pattern` / `PatternElement` /
`DelimitedShape` family where `DelimitedShape` can recurse to arbitrary
depth. The rkyv bound issue is solvable with `#[rkyv(omit_bounds)]` on the
recursive position (the same trick already used in `schema-next`'s
`TypeReference` at `asschema.rs:652-657` for `Box<TypeReference>`).

Impact: kills `ChildPattern` (39 lines) and `ChildDelimitedShape` (50
lines) and `ChildPatternElement` (54 lines) — ~140 lines from `macros.rs`,
roughly 15% of the file. Unlocks arbitrary-depth structural matching for
consumers, which intent record 1280 (structural over text macros) names as
a goal.

## Finding 3 — Delimiter-typed Block destructuring repeats inside codec.rs and downstream

The destructuring pattern

```
Block::Delimited { delimiter: D, root_objects, .. } => ...,
_ => Err(NotaDecodeError::ExpectedDelimited { ... })
```

appears five times inside `codec.rs` alone:

- `NotaBlock::expect_children` at `codec.rs:206-216`
- `NotaBlock::parse_string` square-bracket branch at `codec.rs:233-247`
- `NotaCollection::parse_vector` at `codec.rs:322-332`
- `NotaCollection::parse_map` at `codec.rs:345-372`
- `NotaCollection::parse_option` indirectly (via `expect_children`)

And every consumer hand-rolls it too. Examples from schema-next/asschema.rs:

- `StructFieldMap::from_nota_block` at lines 534-545 — brace destructure
- `TypeReference::from_nota_block` at lines 674-679 — parenthesis via
  `expect_children`

The right primitive isn't `expect_children` (which adds expected-count
checking) — it's `as_delimited(delimiter) -> Option<&[Block]>` or
`Block::children_in(delimiter) -> Result<&[Block], NotaDecodeError>`,
i.e. **return the child slice if the delimiter matches, otherwise None or
typed error, without a count constraint**. That's what
`NotaCollection::parse_vector` needs (any-length square-bracket),
`NotaCollection::parse_map` needs (even-length brace, count check is
custom), and what `StructFieldMap::from_nota_block` does by hand.

Right now consumers reach for raw `Block::Delimited { .. }` destructuring
because the substrate doesn't expose the "delimited-block-without-count"
shape.

**Missing surface**: `Block::as_delimited(Delimiter) -> Option<&[Block]>`
or, more typed, `Block::expect_delimited(Delimiter, &'static str) ->
Result<&[Block], NotaDecodeError>`. Also a `Block::is_delimited_with(d) ->
bool` for the predicate-only form.

Impact: removes 5 of the destructure-and-error sites inside codec.rs
itself (replacing each with a 1-line call), and 2 in schema-next
asschema.rs (StructFieldMap decode is currently 30 lines for that one
shape), with broader reach into spirit-next.

## Finding 4 — Codec asymmetry: NotaBlock owns decode, but encode has nowhere to land

`NotaBlock` is a thin `&Block` wrapper exposing `expect_children`,
`parse_string`, `parse_integer`, `parse_boolean` — four DECODE methods.

There is no symmetric `encode` side. Encode is split:

- Scalars: `NotaString::format()` (one method, one struct) for strings
- Collections: `NotaCollection::format_vector / format_map / format_option`
  — but these are FREE STATIC FUNCTIONS, not methods on a noun:
  `format_vector(elements: &[Element], format) -> String`. They've been
  shoved onto `NotaCollection` as if it were a namespace but they
  don't use `&self`.

This is a method-on-noun violation (per AGENTS.md hard override + skills/rust/methods.md): `format_vector`,
`format_map`, `format_option` are associated functions on `NotaCollection<'block>`
but they don't use `self.block`. `NotaCollection<'block>` carries `&'block Block`
as its data; the encode functions don't. So the noun is wrong.

Worse, the noun-asymmetry shows in usage. To encode a vector, the consumer
writes `NotaCollection::format_vector(elements, Element::to_nota)`. To
decode a vector, `NotaCollection::new(block).parse_vector(Element::from_nota_block)`.
Different shape for the same pair of operations.

The cleaner symmetry: `NotaBlock<'block>` decodes (it owns `&Block`), and a
sibling `NotaValue` or similar trait/method owns encode. Or — more
elegantly — both decode and encode are methods on `Block` itself
(decode via `&self` returning a value, encode through `NotaEncode::to_nota`
which exists). The `NotaCollection::format_*` functions should be methods
on the encoded value or on `Delimiter` — `Delimiter::wrap(children)`
(see Finding 1) absorbs `format_vector` and `format_map` directly.

**Missing alignment**: pick one of
- decode-on-NotaBlock + encode-on-NotaString/Delimiter, with no ZST
  namespace
- or, drop NotaBlock and NotaCollection wrappers entirely; put
  `Block::expect_delimited`, `Block::parse_string`, etc. as methods on
  `Block`, and put `Delimiter::wrap` for encode.

Impact: structural — improves the substrate's discoverability and removes
the ZST-as-namespace smell. Won't directly remove lines but it removes a
WHOLE class of "where does this verb live" confusion that recurs each time
a new value shape is added.

## Finding 5 — Derive produces hand-written wrappers in consumers (schema-emitted boilerplate)

In `spirit-next/src/schema/lib.rs` lines 267-490+, the schema-emitted code
produces a stream of these wrappers, one per type:

```rust
#[cfg(feature = "nota-text")]
impl SourcePath {
    pub fn from_nota_block(block: &nota_next::Block) -> Result<Self, NotaDecodeError> {
        <Self as NotaDecode>::from_nota_block(block)
    }

    pub fn to_nota(&self) -> String {
        <Self as NotaEncode>::to_nota(self)
    }
}
```

This shorthand-impl pattern repeats ~20+ times in one file. It exists
because callers want to write `value.to_nota()` (method on value) but
the trait gives `NotaEncode::to_nota(&value)`. The trait method already IS
on `&self`, so `value.to_nota()` works as long as `NotaEncode` is in
scope. But schema-rust-next emits these wrappers because:

(a) callers in spirit-next don't always have `NotaEncode` imported, and
(b) `to_nota()` as an inherent method makes IDE discovery work.

This is the WRONG fix. The right fix is that the derive macro itself can
emit a shadow inherent impl alongside the trait impl — which means the
substrate-side change is "let the derive optionally emit both a trait
impl AND an inherent method of the same name".

Alternatively, nota-next can publish a trait-import shorthand
(`use nota_next::prelude::*;`) or a re-export pattern that gets
`to_nota()` discoverable without the trait in scope.

**Missing derive feature**: optional inherent-method shadowing for
`NotaEncode::to_nota` / `NotaDecode::from_nota_block`. Default off; on for
schema-emitted code where consumers reach for `.to_nota()` without a use
statement.

Impact: eliminates the ~20 `impl T { pub fn from_nota_block ... pub fn
to_nota ... }` blocks per schema-emitted file. Each is 12 lines counting
the `#[cfg]` guard. ~240 lines from spirit-next/src/schema/lib.rs alone,
and similar amounts in every schema-rust-next emitted file.

## Finding 6 — Hand-rolled NotaDecode for "tagged enum with custom variant payload" (TypeReference)

`schema-next/src/asschema.rs:660-713` writes `impl NotaDecode for
TypeReference` and `impl NotaEncode for TypeReference` by hand — 50+ lines.

The shape: an enum with mix of unit variants (`String`, `Integer`,
`Boolean`, `Path`) and one-payload variants (`Plain(Name)`,
`Vector(Box<Self>)`, `Optional(Box<Self>)`) — PLUS one variant
(`Map(Box<Self>, Box<Self>)`) that takes TWO payloads.

The two-payload `Map` is what kills the derive. Looking at the derive code
at `derive/src/lib.rs:347-373` (`PayloadVariantDecode::arm`), the derive
explicitly errors:

```
NotaDecode enum payload variants must carry exactly one unnamed field
```

So `Map(Box<Self>, Box<Self>)` forces a hand impl, which forces the hand
impl for every OTHER variant on the enum too, even though all of them
would derive cleanly.

The NOTA representation chosen by the hand impl encodes `Map` as
`(Map (K V))` — a two-object tuple payload. This is the natural NOTA
encoding for an N-tuple payload: the payload is a parenthesis with N
children.

**Missing derive feature**: support enum variants with N>=2 unnamed fields,
encoding as `(VariantName (field1 field2 ...))`. Once that lands, the
TypeReference hand impl evaporates; the enum derives cleanly.

The derive ALSO doesn't support named-field enum variants (struct-like
variants). The error message is at `derive/src/lib.rs:363-368`. That's a
separate missing feature but the same family: derive supports a sub-shape
of Rust enums; consumer types that exceed that sub-shape force hand-rolling
the entire decode/encode pair.

Impact: removes the 53-line hand impl for TypeReference and unblocks
similar enums in spirit-next. Estimated 100-200 lines across the stack as
similar enums get reached for.

## Finding 7 — StructFieldMap-style "even-length brace = key/value list" pattern is BTreeMap in disguise

`schema-next/src/asschema.rs:533-573` hand-writes NotaDecode and NotaEncode
for `StructFieldMap`. The body is byte-identical to nota-next's
`NotaCollection::parse_map` and `format_map` EXCEPT that StructFieldMap
keeps insertion order via `Vec<FieldDeclaration>` instead of `BTreeMap`.

Looking at the data shape: it's an ordered list of `(Name,
TypeReference)` pairs, encoded as `{name1 ref1 name2 ref2 ...}` (brace,
even-count). This is the same brace-map encoding as `BTreeMap<K, V>` but
with ordered Vec storage.

The hand impl exists because consumers need ORDERED-map encoding (key
order matters for generated struct field order), and nota-next's
`BTreeMap` impl uses `K: Ord` which doesn't preserve insertion order.

**Missing surface**: an ordered-map codec helper. Either
- `Vec<(K, V)>` decoded as brace-map by adding `NotaDecode for Vec<(K, V)>`
  when V is in a brace context, OR
- A dedicated `OrderedMap<K, V>` wrapper type in nota-next with codec, OR
- A derive attribute that says "this Vec<Struct> is a brace-map keyed on
  field X".

Whichever is chosen, it removes the bespoke 40-line `StructFieldMap`
codec impl. The same pattern recurs in spirit-next for any
positional-tagged ordered collection.

Impact: removes 40 lines for StructFieldMap, plus prevents the next
2-3 reaching for the same pattern.

## Finding 8 — Missing surface: "outer parenthesis-or-not" tolerance for documents

`schema-next/src/asschema.rs:207-219` writes:

```rust
impl NotaDocumentDecode for Asschema {
    fn from_nota_document_body(body: &NotaDocumentBody<'_>) -> Result<Self, NotaDecodeError> {
        match body.root_objects().len() {
            1 => <Self as NotaDecode>::from_nota_block(&body.root_objects()[0]),
            6 => Self::from_nota_document_fields(body.expect_fields("Asschema", 6)?),
            found => Err(NotaDecodeError::ExpectedRootCount {
                type_name: "Asschema",
                expected: 6,
                found,
            }),
        }
    }
}
```

This is "accept either the single-root form or the 6-field document body
form". The schema gives consumers TWO valid serialisations of the same
data — and the consumer hand-rolls the disambiguation in the
NotaDocumentDecode impl.

A schema-emitted root type with K fields will have this pattern: "single
root carrying all K fields as one parenthesis OR K direct fields as
document body". That's a uniform shape derivable from the type
definition. The derive should emit it; today, no consumer can stay
inside derive land for known-root document types.

**Missing derive feature**: when a type derives both `NotaDecode` AND
`NotaDocumentDecode`, the document-decode impl is the "accept root-or-body"
disambiguator. Same for encode (which is mentioned in designer 442 already,
so I'll stop short of that side).

Impact: removes the hand `from_nota_document_fields` (16 lines) and the
hand `NotaDocumentDecode` impl (14 lines) per known-root document type.

## Finding 9 — Atom classification is fixed; consumers can't extend the case predicate

`AtomClassification` at `parser.rs:526-553` is a fixed four-variant enum:
`SymbolCandidate | IntegerCandidate | DecimalCandidate | TextCandidate`.

`AtomCase` at `macros.rs:383-399` is a fixed four-variant enum used in
macro patterns: `Symbol | PascalCase | CamelCase | KebabCase`.

These are two different enums in two different modules describing
overlapping atom shape vocabulary. `AtomCase::matches` dispatches to
`Atom::qualifies_as_*_symbol`. `AtomClassification::classify` returns the
first enum.

If a consumer wants to match "starts with capital letter" but with their
own classification (e.g., a custom case predicate for asschema with a
specific sigil grammar), they have to:

(a) accept the four built-in cases and add sigil filtering separately
    via `SigilSpec`, OR
(b) extend the source of nota-next, OR
(c) reach for `PatternElement::Any` and post-filter in their own code.

Per intent records 1263 (macro nodes are typed-enum pattern primitives) and
1279 (structural matching is the programming model), the case predicate is
likely fine as a CLOSED enum at the NOTA layer (the design rationale being
that bounded patterns serialize). But the lack of an `AtomCase::Other(&str)`
or `AtomCase::Custom(fn(&Atom) -> bool)` escape hatch means consumers
reach OUT of the pattern language whenever they need anything outside
the four cases.

**Missing surface**: probably nothing — this might be intentional. But
flagging it: as schema-next bootstraps its core.schema vocabulary, EVERY
schema-author case predicate that's not in the four-case set forces a fork
of the pattern language. Worth a design decision: do we want consumers to
add their own case predicates, or should the four-case set grow as needed?

Impact: design-time decision, not line-count. Carrying as a noted gap.

## Finding 10 — NotaError -> NotaDecodeError flattens to String

`codec.rs:70-74`:

```rust
impl From<crate::NotaError> for NotaDecodeError {
    fn from(error: crate::NotaError) -> Self {
        Self::Parse(error.to_string())
    }
}
```

`NotaError` is a typed enum (`UnexpectedClose | UnclosedDelimiter |
UnclosedPipeText`) carrying source positions. The `From` impl
stringifies it into `NotaDecodeError::Parse(String)`, throwing away the
typed position and variant.

That stringification is the LAST place position information is preserved
in a typed form. Once it hits `NotaDecodeError::Parse(String)`, any
consumer that wants to show a diagnostic (schema-next's `SchemaError` at
`engine.rs:186-188` immediately re-stringifies into another String wrapper)
loses the source position.

This is the typed-error discipline from `skills/rust/errors.md`:
per-crate `Error` enum, typed variants. Flattening NotaError to String
breaks the chain.

**Missing surface**: `NotaDecodeError::Parse(NotaError)` keeping the typed
inner — so a consumer's error chain can pull the source position back out
when needed.

Impact: structural quality, not line-count. But it's a one-line fix that
unblocks every consumer's diagnostic story.

## Top 3 broad improvements for nota-next (ordered by impact × scope)

1. **Lift `Delimiter` to a first-class public encoding surface (Finding 1
   + Finding 3 + part of Finding 4).** Make `Delimiter::opening_text`,
   `Delimiter::closing_text`, and `Delimiter::wrap(children)` public, and
   add `Block::expect_delimited(delimiter, type_name)` /
   `Block::as_delimited(delimiter)` as the canonical "give me the children
   if the delimiter matches" entry points. This single change collapses
   five destructure sites inside `codec.rs` itself, removes
   `NotaCollection::format_vector` and `format_map` as standalone
   functions (they become `Delimiter::wrap` calls), kills both
   `DelimitedNotation` (32 lines) and `SchemaNodeDelimitedNotation` (40
   lines) in schema-next, and prevents the next consumer from hand-rolling
   the same 5-arm match. Expected boilerplate eliminated: ~150 lines
   across the stack, plus restoration of the noun-method discipline on the
   encode side. Impact is high because EVERY consumer encoder reaches for
   this pattern.

2. **Make the derive cover the realistic enum shape and emit
   inherent-method shadows (Finding 5 + Finding 6).** Two derive
   extensions: (a) support enum variants with N>=2 unnamed fields,
   encoding as `(Variant (f1 f2 ...))`; (b) optionally emit inherent
   `pub fn from_nota_block` and `pub fn to_nota` methods on the type so
   callers don't need the trait in scope. The first extension kills the
   53-line `impl NotaDecode/NotaEncode for TypeReference` hand block in
   `asschema.rs` and unblocks every schema-emitted enum with a
   multi-field variant. The second extension kills the ~20 wrapper-impl
   blocks per schema-emitted module in spirit-next (~12 lines each, 240+
   lines in `spirit-next/src/schema/lib.rs` alone, similar across every
   other emitted schema). Expected boilerplate eliminated: 300-400 lines
   across schema-next, schema-rust-next, and spirit-next. Impact is high
   because the wrapper-impl pattern is per-TYPE, so it grows with the
   number of schema-defined nouns.

3. **Collapse `Pattern`/`ChildPattern` into a single recursive structural-match
   tree (Finding 2).** The current split exists because rkyv recursion
   needed `omit_bounds` annotations and the implementor stopped at one
   level. Per intent records 1263, 1279, 1280, structural matching is the
   programming model for NOTA extension — and that model needs to nest
   arbitrarily deep so a schema author can write a single pattern that
   destructures, e.g., `(Map (Key (Vec Value)))` directly rather than
   peeling layers manually. The fix is one `Box<DelimitedShape>` in the
   right place with `#[rkyv(omit_bounds)]`. Removes 140+ lines from
   `macros.rs` (about 15% of the file's enum and impl machinery) AND
   unlocks the substrate's stated purpose. Expected boilerplate
   eliminated: 140 lines inside nota-next plus 50-100 lines of consumer
   post-processing in schema-next's macro lowering, which currently has
   to walk-and-re-match because the pattern language stopped one level
   shallow.
