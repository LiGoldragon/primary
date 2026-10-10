# Source Text Ontology: Defining the Block

Study ordered 2026-08-18: "we need to define the block. start with the text
source code. turn every logical aspect into a type. ontology of source code"
(protosIsTheSharedStyle.md 2026-08-18).

Framing ruling (2026-08-18): "realize isnt implemented by the same type as
textualize. if you cant find two different types, the implementation is
wrong. You dont textualize the text, and you dont realize the realized data."
(traitsAsCapabilities.md 2026-08-18).

## 1. Type Table

Every logical aspect of Protos source text, bottom up. Category:
K = Kind (value with identity), Q = quality of another type (field, not
its own type), R = role in a context, C = capability (trait).

| # | Aspect | Type | Cat | Notes |
|---|--------|------|-----|-------|
| 1 | Character | -- | Q of SourceText | Unicode scalar; atom of text |
| 2 | Whitespace | -- | consumed by scanner | Sibling separator; never stored |
| 3 | Escape | -- | Q of string carriers | `\` + char; interior to carrier scanning |
| 4 | Bare carrier | `StringCarrier::Bare` | K variant | "A string that doesnt need quotes *must not* be quoted" (datomSyntax.md 2026-08-14) |
| 5 | Paren carrier | `StringCarrier::Parenthesized` | K variant | "let the block parser balance parentheses until it reaches the final unbalanced )" (datomSyntax.md 2026-08-14) |
| 6 | Curly-quote carrier | `StringCarrier::CurlyQuoted` | K variant | Legacy: U+201C...U+201D |
| 7 | String carrier | `StringCarrier` | K (enum) | "The string forms whose lexical opacity is universally known" (code) |
| 8 | Opacity | -- | Q of string carriers | "allow some blocks, like strings, to allow other delimiters to be ignored until it closes" (datomSyntax.md 2026-08-14) |
| 9 | Delimiter pair | -- | Q of Shape variants | `()`, `[]`, `{}`, curly quotes; each pair defines a shape |
| 10 | Shape | `Shape` | K (enum, 9) | Fixed structural vocabulary; Bare + 4 delimiters x {unprefixed, dotted} |
| 11 | Dot | -- | separator | Head-to-delimiter boundary; "it opens a delimiter. everything is data" (dotOpensDelimiterEverythingIsData.md) |
| 12 | Head | `Head` | K | "I like the Head terminology actually. lets make it official"; "the dotted prefix of a delimiter must be part of its type... unprefixed blocks simply have no prefix" (datomSyntax.md 2026-08-14) |
| 13 | Colon form | -- | Q of Head (Ethos) | `Name:Transformer` (colonFormTransformerSyntax.md); protos stores as Head string content |
| 14 | Body | `SourceText` (field) | Q of Block | Interior text between delimiters or bare text |
| 15 | Byte spans | `Range<usize>` (x2) | Q of Block | body_span + span; extent in root source |
| 16 | Block | `Block` | K | "One lexical unit found by the first pass. Its body remains textual." (code) |
| 17 | Sibling sequence | `Vec<Block>` | result of Realize | Ordered blocks at one depth |
| 18 | Position | `usize` | Q of WalkFrame | Ordinal among siblings |
| 19 | Depth | `usize` | Q of walk state | Block containment recursion level |
| 20 | Source text | `SourceText` | K | "Text as data before a dialect gives it a real type" (code) |
| 21 | Shape-as-announcer | `ShapeDefined` | C (trait) | "a met shape announces a type, and that type's context takes over" (protosParsing.md Intent) |
| 22 | Block-in-context | `RealizeScope` | R | Block meeting its dialect; "the type met implements its own context" (protosIsTheSharedStyle.md 2026-08-12) |
| 23 | Scanner | `BlockScanner` | context | First-pass; retains source, assigns no dialect meaning |
| 24 | Structural transparency | -- | Q of `[]`, `{}` | Interior delimiters tracked and recursed, not suppressed |
| 25 | Load-bearing symbols in strings | -- | Q of bare/string positions | "If its a string, then it can use symbols which would be load bearing in other situations" (datomSyntax.md 2026-08-14) |

## 2. The Block

### Composition

| Field | Type | Varies by shape? | Ruling |
|-------|------|-------------------|--------|
| head | `Option<Head>` | Present iff Dotted* | "unprefixed blocks simply have no prefix" |
| shape | `Shape` | IS the discriminant | Fixed vocabulary |
| body | `SourceText` | No | Always present |
| string_carrier | `Option<StringCarrier>` | Determined by shape | Per-kind opacity |
| body_span | `Range<usize>` | No | Body extent in root source |
| span | `Range<usize>` | No | Whole-block extent |

### One struct, not enum over shapes

"it could be a universal type, and unprefixed blocks simply have no
prefix" (datomSyntax.md 2026-08-14). Block is one type whose shape
varies. An enum over shapes would eliminate illegal states (carrier
present on structural blocks) but contradicts the universal-type
framing. Shape carries discrimination; Block carries data.

### Code alignment (protos/src/block.rs, shape.rs)

| Aspect | Code | Status |
|--------|------|--------|
| head, shape, body, string_carrier, body_span, span | block.rs:26-35 | Match |
| `impl Textualize for Block` -> SourceText | block.rs:66-85 | Match: Block is real at level 0 |
| `impl Realize for SourceText` -> Vec<Block> | block.rs:110-117 | Match: SourceText is textual at level 0 |
| Shape: 9 variants with Dotted* | shape.rs:3-13 | Tension: dottedness redundant with head.is_some() |
| string_carrier: Option stored | block.rs:30 | Tension: fully determined by shape; derivable |
| ShapeDefined: select(shape, head) | shape.rs:19-24 | Match |
| ShapeHeading (walk.rs:461-486) | enforces head/shape consistency | Exists only because of the redundancy |

### Tensions

1. **Shape dottedness redundancy**: Shape::DottedBraced encodes the
   same fact as `head.is_some()`. ShapeHeading exists solely to keep
   them in sync. The ruling "the dotted prefix of a delimiter must be
   part of its type" supports encoding it in Shape, but head.is_some()
   also expresses it.

2. **StringCarrier determinism**: string_carrier is fully determined by
   shape (Bare->Bare, Paren/DottedParen->Parenthesized,
   CurlyQuoted/DottedCurlyQuoted->CurlyQuoted, structural->None). A
   method deriving it from shape would eliminate the illegal-state
   surface.

## 3. Textual Side of the Realize Pair

### Level-by-level

| Level | Textual (carries Realize) | Real (carries Textualize) |
|-------|---------------------------|---------------------------|
| 0: source | `SourceText` -> `Vec<Block>` | `Block` -> `SourceText` |
| 1: scoped | `Block`-in-context -> dialect type | dialect type -> textual emission |

Level 0 is in code and correct (form.rs, block.rs).

At level 1, Block is the textual type -- the text data the dialect
receives through RealizeScope. The dialect type is the real type.
Scoped realize belongs on the textual side (Block-in-context), scoped
textualize on the real side (dialect type).

### Fork and recommendation

**A. Block-in-context** carries scoped Realize. One universal textual
type serves all dialects. ShapeDefined + context select the real type.

**B. Per-real-type textual twins** (EntryText, GroupText...) each carry
Realize. Creates N additional types per dialect.

Recommendation: **A**. Block IS "text as data before a dialect gives it
a real type" -- creating per-type twins duplicates what Block +
ShapeDefined + RealizeScope already provide.

Trait shape on the textual side (placeholder):

```rust
// On Block-in-context (textual side); placeholder names
trait ScopedRealizing<Ctx> {
    type Real;
    fn realize_scoped(&self, ctx: &mut Ctx) -> Result<Self::Real, ...>;
}
```

### Current contradiction

The ontological map's <<BlockRealizing>> places `realize_block` on the
real type (dialect types implement both realize and textualize
directions). The ruling explicitly forbids this: "realize isnt
implemented by the same type as textualize. if you cant find two
different types, the implementation is wrong." Fix: scoped realize
moves to Block-in-context; scoped textualize stays on the dialect type.

### Dual-role note

Block implements Textualize at level 0 (it is real there) and would
carry scoped Realize at level 1 (it is textual there). These are
different trait instances at different levels. The ruling "You dont
textualize the text, and you dont realize the realized data" is
satisfied: Block is not text at level 0, and not realized data at
level 1.

## 4. Status

### Psyche-ruled (verbatim)

| # | Verbatim | Source |
|---|----------|--------|
| R1 | "realize isnt implemented by the same type as textualize. if you cant find two different types, the implementation is wrong. You dont textualize the text, and you dont realize the realized data." | traitsAsCapabilities.md 2026-08-18 |
| R2 | "we need to define the block. start with the text source code. turn every logical aspect into a type. ontology of source code" | protosIsTheSharedStyle.md 2026-08-18 |
| R3 | "the dotted prefix of a delimiter must be part of its type. it could be a universal type, and unprefixed blocks simply have no prefix" | datomSyntax.md 2026-08-14 |
| R4 | "I like the Head terminology actually. lets make it official" / "for the text block type? Head" | datomSyntax.md 2026-08-14 |
| R5 | "Im willing to increase the complexity a bit to allow some blocks, like strings, to allow other delimiters to be ignored until it closes" | datomSyntax.md 2026-08-14 |
| R6 | "A string that doesnt need quotes *must not* be quoted" | datomSyntax.md 2026-08-14 |
| R7 | "let the block parser balance parentheses until it reaches the final unbalanced )... go for balance-based, where an unbalanced parenthesis needs to be escaped" | datomSyntax.md 2026-08-14 |
| R8 | "a met shape announces a type, and that type's context takes over completely until its completing shape; then the parent context resumes" | protosParsing.md (Intent) |
| R9 | "ShapeDefined is good" | traitsAsCapabilities.md 2026-08-14 |
| R10 | "it opens a delimiter. everything is data" | dotOpensDelimiterEverythingIsData.md |
| R11 | "variants always re-emit their head" | datomSyntax.md 2026-08-14 |
| R12 | "If its a string, then it can use symbols which would be load bearing in other situations" | datomSyntax.md 2026-08-14 |

### Proposals

| # | Proposal | Basis |
|---|----------|-------|
| P1 | string_carrier derivable from shape; method replaces stored field | Eliminates illegal-state surface |
| P2 | Scoped realize on Block-in-context (textual side), not on dialect real types | R1 |
| P3 | Ontological map's <<BlockRealizing>> on real type contradicts R1; must move | R1 |

### Open questions (5)

1. Should Shape carry 9 variants (Dotted*) or 5 delimiter kinds with dottedness derived from head.is_some()? R3 supports 9, but the redundancy requires ShapeHeading enforcement.
2. At the scoped level, does Block carry scoped Realize generically (parameterized by context) or through a per-scope wrapper?
3. Does the Ethos colon form (`Name:Transformer`) warrant protos-level parsing of Head content, or is it purely Ethos-level interpretation?
4. Is body_span intrinsic to the Block-as-value, or evidence of its scanning origin? (The driver rebases it, suggesting context-dependence.)
5. Block implements Textualize (level 0) and would carry scoped Realize (level 1) -- does this dual role need architectural separation, or does level separation resolve it?
