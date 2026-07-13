# Logos — maps and delimiter semantics (grounding + design discussion)

An addendum analysis for the Logos design. Three parts: **A. maps, grounded**;
**B. delimiter roles, verified against code**; **C. design fold-in** (a discussion
surface, no decisions). Evidence is separated from design: Parts A and B are
worker-verified facts with citations; Part C is options and trade-offs for the psyche.

Written 2026-07-11 (session `schema-codex`, lane `logos-delimiter-semantics`). Companion:
`design-v0.md` §1.3 (the psyche statements this grounds), `syntax-mockup-v2.md` (the
reshuffle this folds into). nota source read at commit `f8de7a51` (nota 0.7.0) via
`git show f8de7a51:<path>`. rkyv is 0.8.17/0.8.16 across the repos.

## Part A — Maps, grounded [evidence]

### A.1 Which map types the corpus uses

`rg -c` over `src/` of the four surveyed repos:

| repo | BTreeMap | HashMap | IndexMap |
|---|---|---|---|
| schema-rust | 8 | 1 | 0 |
| sema-engine | 6 | 7 | 0 |
| signal-spirit | 0 | 0 | 0 |
| spirit | 0 | 7 | 0 |
| **total** | **14** | **15** | **0** |

Hand-written engine code picks `HashMap` for unordered in-memory indices/registries and
`BTreeMap` only where iteration order or a stable key-diff matters
(`sema-engine/src/fold.rs`, `engine.rs`). The **codegen surface** picks `BTreeMap`
**unconditionally** for schema map fields, specifically to force sorted (deterministic)
order for archived/wire stability — the doc comment at `schema-rust/src/lib.rs:4992-4998`
forces the key type to derive `Ord` "so `BTreeMap<Key, _>` compiles." `IndexMap`: zero
occurrences anywhere.

### A.2 How rkyv archives maps — entries PLUS an index

rkyv 0.8.17 source (`~/.cargo/registry/src/*/rkyv-0.8.17/`):

- `ArchivedHashMap` (`src/collections/swiss_table/map.rs:29-33`) wraps an
  `ArchivedHashTable` (`swiss_table/table.rs:53`) that stores **SwissTable control bytes**
  (one per bucket, group-width-16 probe/displacement layout, `table.rs:6-15,147-165`)
  alongside the bucket array — a real hash index.
- `ArchivedBTreeMap` (`src/collections/btree/map/mod.rs:165`) is a genuine node tree:
  `NodeKind` (118), `LeafNode` (139), `InnerNode` (148), with inner-node traversal
  (297-356) and explicit leaf/inner node serialization (542-656) — keys plus child
  pointers, not a flat list.

So at the archived layer a map carries index structure **beyond** the entry sequence, in
both variants. Verified from source, not inferred.

### A.3 serde / rkyv data model

serde's abstract data model treats a map as `serialize_map` / a sequence of `(key,
value)` entries with a length — entries-only, index-agnostic ([knowledge]; serde source
not found locally). rkyv diverges at the archived layer (A.2): it embeds real index/tree
structure so the archived form supports zero-copy **lookup**, not just iteration.

### A.4 Is the current NOTA `{}` map syntax actually used?

nota's codec (`f8de7a51:src/codec.rs`) defines the map form: `BTreeMap<K,V>` encodes via
`Delimiter::Brace.wrap(entries)` with each entry formatted `key.value` (dotted), and
`parse_map` (codec.rs:575-599) reads a `Brace` block as a flat run of `key.value` dotted
entries — **no index in the text, just a sequence**. Usage in real data text:

- `.nota` data files across the four repos: **0 of 27 files contain a `{` at all**
  (`find -L <repo> -iname '*.nota'` then `grep -lF '{'`). The brace-map literal is
  entirely absent from real NOTA data in the corpus.
- The schema-level `Map.` type keyword (declaring a map-typed field) appears in **exactly
  3 files, all schema-rust test fixtures** (`collections.schema`, two `big-schemas/*`);
  zero in sema-engine, signal-spirit, spirit `.schema`. (A handful of `Map` uses also
  live in the separate `*-schema-dotted-syntax-pilot` repos — still a few sites, not a
  pervasive form.)
- The only exercised `BTreeMap` NOTA round-trip is nota's own Rust test
  (`f8de7a51:tests/codec.rs:245`), not a text fixture.

The psyche's belief that brace-map syntax is rare is **confirmed and understated**: it is
absent from real `.nota` data (0/27) and the schema `Map.` keyword is used in ~3 fixture
sites.

### A.5 Verdict — at which layers a map is "a vector of pairs plus an invariant"

- **NOTA-text layer**: exactly a vector-of-pairs-plus-invariant — a sorted-key sequence
  of `key.value` entries; no index is in the text; and it is nearly unused.
- **Schema-codegen layer**: vector-of-pairs plus the **sortedness invariant** (BTreeMap
  chosen deliberately for canonical order).
- **Hand-written Rust layer**: whatever the programmer picked for a runtime property
  (`HashMap` vs `BTreeMap`, ~even split) — a live decision, not a fixed shape.
- **rkyv archived/wire layer**: **more than a vector** — a real hash/B-tree index is the
  point of the representation.

So "fundamentally a vector of pairs" holds cleanly at the **text and schema** layers
(where it is also nearly unused); it does **not** hold at the archived layer. Crucially
the archived index is **derived** from the canonical sorted entry sequence, so it needs
no counterpart in the text form — the text can be a delimiter-agnostic vector of pairs
while the archived form still rebuilds its index. This directly supports the psyche's
intuition (statement 9) *for the text layer*, while being honest that the archived layer
is more.

## Part B — Delimiter roles, verified against code [evidence]

### B.1 Where the delimiter glyph is consumed, by layer

- **Raw parser (`f8de7a51:src/parser.rs`)** — glyph-preserving, not glyph-selecting. The
  `Block::Delimited { delimiter: Delimiter, … }` and the `Delimiter` enum
  (`Parenthesis`/`SquareBracket`/`Brace`, lines 235-238) retain which glyph was used;
  `as_delimited(delimiter)` (136) returns the body only on exact glyph match, but the raw
  layer itself requires nothing.
- **Codec (`src/codec.rs`)** — the glyph **is enforced per expected type**, even though
  the type is already statically known: `Vec<T>` requires `SquareBracket`
  (`parse_vector`, 557-566, errors `ExpectedDelimited{"Vec", SquareBracket}` otherwise);
  `BTreeMap` requires `Brace` (`parse_map`, 575-589); `Option` Some requires `Parenthesis`
  (`parse_option`, 603-614). `expect_body`/`expect_children` all take an explicit
  `delimiter` and error on mismatch. The one **glyph-permissive** case is `String`
  (`parse_string`, 376-394): a bare/pipe atom **or** a `SquareBracket` block.
- **Schema/macro (`src/macros.rs`, `derive/src/lib.rs`)** — glyph is **one dispatch key
  among several**. `DelimitedShape::match_block` hard-gates on glyph identity before child
  patterns, but the variant sets actually exercised (`tests/macro_nodes.rs:263-307`)
  disambiguate by **head literal** (`"Optional"`) and **atom case**, both under the same
  `Parenthesis` — so glyph is not the sole selector.

### B.2 Testing the "only schema" claim

Partially accurate, **wrong as an absolute**. The strong form — "outside schema,
delimiters are not machine-load-bearing" — **does not hold** for nota 0.7.0: the codec
enforces the glyph today, so a `Vec` field written `(a b c)` instead of `[a b c]` is a
hard decode error even though the type is fixed. But this is glyph-driven **validation /
canonicalization**, not type **selection** (the type is already pinned by the field). The
weaker form he intends — "schema/macro dispatch is the surface where delimiter identity
*selects among differently-typed alternatives*" — is well supported; and there the glyph
is still only one of several selectors. So his cognitive-value point is real, but the
current machine does lean on the glyph for canonical-form discipline, not nothing.

### B.3 Shape-union positions (a slot admitting both a string/atom and a vector)

- nota crate: **exactly 1** — `String` decode (atom or `[…]`), the "Literal" case.
- four `.schema` corpora: **0** found. The schema convention is **singular/plural
  distinct fields** (`Referent String` vs `Referents (Vector Referent)`,
  `signal.schema:106-107`), not one field admitting both shapes. (Absence after a scoped
  sample of representative `.schema` files, not an exhaustive grep of every field.)
- The **optional-paren string rule** (statement 8) resolves the *write-side* of the one
  real union: nota already enforces `reject_redundant_delimiter` (codec.rs:520) — a string
  writable as a bare atom must **not** be bracketed — so canonical text has one shape per
  value even though the decoder stays permissive on read.

## Part C — Design fold-in [design — discussion surface, no decisions]

### C.1 The optional-paren string rule

Fold statement 8 into the reshuffle: a string is a **bare atom when canonical**,
delimited (under the reshuffle, `(…)`) **only** when its content needs it (spaces /
forbidden characters). Note this rule is **already landed** in nota, not new:
`reject_redundant_delimiter` enforces exactly it today (B.3). Under the reshuffle it makes
`Literal.[rustfmt.skip]` **unambiguously a vector of one bare-atom string** — the `[…]` is
a vector because a canonical string carries no delimiter. This removes the v2 §4 open
literal-delimiter question at the write layer.

### C.2 The map delimiter — RESOLVED by ruling: `Map.( … )`

**[psyche ruling, closes this question]** "Map.() sounds reasonable then. The mental model
would be: () holds a payload; maps are one kind of payload. And I still want to stick to
the key.Value syntax for them." So:

- Maps have **no dedicated delimiter**. Under the reshuffle `()` is the **payload
  bracket**, and a **map is one payload kind** among others (a delimited **string** is
  another). A map is written **`Map.( key.Value  key.Value  … )`**.
- Entries keep the **`key.Value` dotted pair** — a lowercase key name dotted onto a
  capitalized value object — reaffirming that **no space-separated pair form exists
  anywhere**.

This is the option the grounding pointed to: at the text layer a map already IS a sorted
vector of pairs (Part A), the archived index is **derived** from those entries (so the
text-delimiter choice was orthogonal to the archived index — the map needs no delimiter of
its own to keep its rkyv index), and the brace-map form was nearly unused (A.4). The
rejected alternatives were `[]` (overloads the vector glyph) and keeping `{}` (collides
with the reshuffle's struct glyph). Recorded for the trail; the ruling settles it.

**Design-coherence point (worth stating where schemes are compared):** with this ruling,
**map entries and struct-field entries share one mechanism — the dotted pair.** A struct
field is the dotted chain `Visibility.name?.Type`; a map entry is the dotted pair
`key.Value`. One pairing mechanism spans both, and it is the same no-space-separated-pair
invariant everywhere.

### C.2.1 The settled reshuffle, in full

`{}` = structs, `[]` = vectors, `()` = **payloads**. A payload is: a **string** when its
content forces the bracket (statement 8; a canonical string stays a bare atom); a **map**
written `Map.( key.Value … )`; or any `Head.( … )` **application** payload (`Variant.(Data)`,
ruling 5). The `(| |)` form remains the indentation-escaped multiline string (which, per
Part B / v2, requires resurrecting the just-removed pipe-paren machinery).

### C.3 The accept-any-delimiter idea — what it buys and costs

The psyche's observation (statement 10): outside schema, where the next expected type is
known, a parser *could* accept any matching pair, freeing glyphs to be purely cognitive.
Weighed against the evidence (Part B), honestly:

**What it buys:**
- Glyphs become a **human/agent readability aid** rather than a machine constraint —
  authors could pick the glyph that reads best; mismatches would not be errors.
- Removes the canonicalization friction where a correctly-typed value is rejected purely
  for using the "wrong" balanced pair.
- Aligns the machine with the "expected type is always known" invariant already central
  to NOTA.

**What it costs:**
- **Error detection / resync.** Today a glyph mismatch is an *early, local* hard error
  (B.1: `ExpectedDelimited`). Redundant glyph information lets the decoder catch a
  malformed or misaligned stream at the delimiter rather than deep in a mis-typed body.
  Accept-any removes that cross-check; a shape error would surface later and less locally.
- **Canonical-encoding byte determinism.** The codec today guarantees one canonical text
  per value (one glyph per container kind; `reject_redundant_delimiter` for strings).
  Byte-deterministic round-trip (decode∘encode = identity on canonical text) underpins
  wire/archive stability. Accept-any means either encode still emits one canonical glyph
  (so the permissiveness is read-only, and authors' non-canonical glyphs are silently
  normalized — a surprise), or canonical form is abandoned (losing byte determinism).
- **Round-trip identity for hand-authored text.** If input `(a b c)` for a `Vec`
  normalizes to `[a b c]` on re-emit, the author's text is not preserved — a real
  friction for hand-edited data and diffs.

The tension is squarely between the psyche's cognitive-freedom aim and the codebase's
existing investment in canonical, byte-deterministic, early-error-checked text. A middle
design exists (accept-any on **read**, emit **canonical** on write, with the glyph
advisory) — it buys authoring freedom while keeping wire determinism, at the cost that
re-emitted text differs from authored text. Presented as options; not decided.

## Summary of the three verdicts

1. **Map layers**: a map is a vector-of-pairs-plus-invariant at the **NOTA-text** and
   **schema-codegen** layers (sorted `BTreeMap` entries, no text index — and nearly unused:
   0/27 `.nota` files use brace-map, `Map.` in ~3 schema fixtures); it is **more than a
   vector** at the **rkyv archived** layer (SwissTable / B-tree index, rkyv 0.8.17 source).
   The archived index is derived from the sorted entries, so it needs no text delimiter —
   and the psyche has now **settled** the text form as `Map.( key.Value … )`: no dedicated
   map delimiter, `()` as the payload bracket, `key.Value` dotted entries, so map entries
   and struct fields share the one dotted-pair mechanism.
2. **Where glyphs are consumed today**: raw parser preserves but does not select on glyph;
   the **codec enforces** the glyph per expected type (Vec→`[]`, BTreeMap→`{}`,
   Option-Some→`()`; String is the sole permissive shape-union) as canonical-form
   validation, not type selection; the schema/macro layer uses glyph as **one of several**
   dispatch keys. The "only schema" claim is partially accurate but wrong as an absolute —
   the glyph is machine-load-bearing at the codec layer now.
3. **Shape-union positions**: **1 confirmed** (nota's `String`: atom or `[…]`); **0** in
   the four `.schema` corpora, which use singular/plural distinct fields instead. The
   optional-paren string rule (already enforced via `reject_redundant_delimiter`) resolves
   the write-side of the one real union.
