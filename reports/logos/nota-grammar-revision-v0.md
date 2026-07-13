# NOTA grammar revision v0 — consolidation and go/no-go surface (draft for markup)

The accumulating Logos/Nomos rulings amount to a **second-generation nota grammar**. This
document is the psyche's single normative go/no-go surface: it consolidates every settled
and leaning grammar item in one place, each cited to its ruling/statement with date and an
**impossible-to-misread settled-vs-leaning marker**, then states the migration impact.

Status vocabulary (read this first):

- **[SETTLED]** — a psyche ruling; the design intent is fixed (implementation may not
  exist yet).
- **[LEANING]** — a psyche proposal he is leaning toward but has **not** finalized; a
  distinct go/no-go.
- **[LANDED]** — already true in nota 0.7.0 today (evidence cited).
- **[NOT PURSUED]** / **[UNKNOWN]** — explicitly dropped, or explicitly unknown to him.

All rulings are 2026-07-11 unless noted. Sources: `design-v0.md` §1.1–1.3;
`delimiter-semantics.md` (evidence). nota source at commit `f8de7a51` (0.7.0).

## 1. The grammar items, by status

### 1.1 Dotted mechanisms — SETTLED (independent of the delimiter reshuffle)

| # | Item | Source | Status |
|---|---|---|---|
| a | **Dot-application binding in the raw grammar**: `Head.Payload` binds a head to the immediately-following payload (bare atom, or a delimited block) as **one** application/variant node. | ruling 5 | **[SETTLED]** intent; **not implemented** — today the dot rides on the preceding atom (evidence §2.1). |
| b | **Dotted data variants at all layers**: a data-carrying variant is `Variant.Data` (bare-atom payload) or `Variant.( … )` / `Variant.[ … ]` / `Variant.{ … }` (bracket matches payload type), **replacing** the current headed-record `(Variant Data)`. | ruling 12 | **[SETTLED]**; the single largest encoding change. |
| c | **Dotted Rust paths, no `::`**: `rustfmt.skip`, `rkyv.[…]`; the **projection** translates `.`→`::` on emit. Foreign literal text is carried dotted, never byte-exact `::`. | ruling 7 | **[SETTLED]** |
| d | **`key.Value` dotted pair is the universal pairing mechanism**: map entries are `key.Value`; struct fields are the dotted chain `Visibility.name?.Type` (explicit name only on a repeated field type). One mechanism spans both. | rulings 3, 11 | **[SETTLED]** |
| e | **Capitalization semantics** (capitalized-leading atom = object, lowercase-leading = name) and **no space-separated pair forms** anywhere. | carried invariants | **[SETTLED — unchanged]** |

### 1.2 Map surface and representation — SETTLED

| # | Item | Source | Status |
|---|---|---|---|
| f | **Map surface is `Map.( key.Value … )`** — **no dedicated map delimiter**; `()` holds the payload, a map is one payload kind, entries are `key.Value` dotted pairs. | ruling 11 | **[SETTLED]** |
| g | **The Rust map type a schema `Map` lowers to** (`BTreeMap` / `HashMap` / vector-of-pairs) is a **Nomos-level lowering choice**, not a language-fixed fact — switchable in Nomos. | statement 13 | **[SETTLED as principle]** (codegen currently hard-picks `BTreeMap`, `delimiter-semantics.md` A.1; this moves into Nomos). |

### 1.3 Delimiter reshuffle — LEANING (a separate go/no-go)

| # | Item | Source | Status |
|---|---|---|---|
| h | **Delimiter reassignment**: `{}` = **structs**, `[]` = **vectors**, `()` = **payloads** (string / map / application payload). | ruling 6 | **[LEANING — NOT final]** |
| i | **Strings**: **bare atom when canonical**; `()` only when content forces it (spaces / forbidden chars); `(| |)` the indentation-escaped multiline form. | statement 8 | bare-when-canonical is **[LANDED]** (`reject_redundant_delimiter`, evidence §2.2); the `()`-string and `(| |)` forms are **[LEANING]** — part of the reshuffle. |

**Boundary note (do not misread):** items (a)–(g) are the settled dotted-mechanism core and
do **not** depend on the reshuffle. The reshuffle (h) is the *glyph→meaning reassignment*
and is **leaning only**. Items (b)/(f) are written with `()`/`[]`/`{}` payload brackets;
those render in their final shape only once the reshuffle (h) lands — under current nota
those glyphs still carry their old meanings. `() = payload` is the most-firmed slice of the
reshuffle (ruling 11 leans on it); `{}`=struct and `[]`=vector remain under the ruling-6
leaning banner. **The go/no-go on (h) can be taken separately from landing (a)–(g).**

### 1.4 Explicitly closed

| Item | Source | Status |
|---|---|---|
| **Accept-any-delimiter** (a parser accepting any matching pair). | statement 10, refined | **[NOT PURSUED]** — delimiters are *generative* only in schema; in NOTA/Logos the glyph associations are reader-help, and enforcement ≠ semantic impact. |
| **Nomos's own grammar/behavior.** | psyche | **[UNKNOWN]** — "I don't know about NOMOS." Not settled here; do not infer. |

## 2. Migration impact

### 2.1 What changes in the nota crate — raw layer [evidence]

**Dot-application binding (item a) is a raw-parser change.** Today (`f8de7a51:src/parser.rs`)
a trailing-dot atom is one atom and the following `(...)`/`[...]`/`{...}` is a **separate**
sibling `Block` — directly observed in every mockup parse-check (`Public.Newtype.` parses as
an atom, `(...)` as the next root object; `rkyv.` + `[…]` likewise). The revision must make
the parser recognize `atom.` immediately followed by a delimited block (or a bare atom) as a
**single dotted-application `Block`**, at the raw layer, expectation-agnostic. This is the
foundational change; every dotted form (a–b, f) depends on it.

### 2.2 What changes in the codecs [evidence]

- **Variant encoding (item b)** is the largest surface. Today the enum codec and
  `nota-derive` emit/read the headed-record form `(Variant Data)` — the
  `StructuralVariantShape` variants (`derive/src/lib.rs`: `Headed`, `HeadedBody`,
  `PascalHead`, …) and the codec's enum paths. The revision changes these to the dotted
  `Variant.Data` / `Variant.( … )` family. Every enum payload in every schema and hand-
  written NOTA type is affected.
- **Delimiter re-pin (item h, if go)**: the codec pins a glyph per container type today —
  `Vec`→`SquareBracket`, `BTreeMap`→`Brace`, `Option::Some`→`Parenthesis`, struct/record
  body→`Parenthesis` (`codec.rs` parse_vector/parse_map/parse_option/expect_body). Under the
  reshuffle these re-pin to: struct→`{}`, vector→`[]` (unchanged), map→`Map.( … )` payload
  (drops the brace-map), string→`()`-or-bare.
- **String codec (item i)**: delimited strings move from `[…]` to `()`; the multiline
  `(| |)` form requires **re-adding pipe-paren machinery** that was removed on the way to
  0.7.0 (evidence: the `(| |)` probe returns `UnexpectedClose` in 0.7.0 where 0.5.1 accepted
  it). The bare-when-canonical half is already enforced by `reject_redundant_delimiter`
  (`codec.rs:520`) — **[LANDED]**.

### 2.3 Corpus and golden migration

- **Generated surface** (the bulk): schema-rust's emitter + its committed goldens + every
  `src/schema/*.rs` in consumers. Update the emitter, then **regenerate**; the goldens are
  the byte-verification basis (this is the Logos acceptance-oracle discipline from
  `design-v0.md` §4).
- **Hand-authored NOTA/schema text**: a scripted rewrite (`(Variant Data)` → `Variant.Data`,
  string/record/map delimiter swaps) plus a round-trip check (`decode∘encode` identity on
  canonical text).
- **Map migration is tiny**: the brace-map form is nearly unused — **0 of 27** `.nota` data
  files, ~3 schema fixtures (`delimiter-semantics.md` A.4). Variant encoding is the pervasive
  case.

### 2.4 Rough ordering

1. **Raw dot-application binding (a)** — foundational; parse-verify against the existing
   mockup samples (`reports/logos/samples/*`).
2. **Variant encoding (b)** in `nota-derive` + codec — largest; gate behind regenerated
   goldens.
3. **Dotted paths (c)** and the `key.Value`/field pairing (d) fall out of (a)–(b).
4. **Reshuffle (h) + string forms (i)** — only on a separate **go** for the leaning items;
   codec delimiter re-pin + `(| |)` pipe-paren resurrection.
5. **Corpus/golden regeneration + round-trip** at each step.

Steps 1–3 (settled) can proceed without step 4 (leaning).

### 2.5 Precedent [evidence]

The **structural-pipe removal** (`pipe-paren` / `pipe-brace` recursive forms removed by nota
0.7.0 — directly verified: the `(| |)` probe now errors where 0.5.1 parsed it) is the
**executed precedent** for a byte-verifiable nota grammar migration on `main`. It is the
template for staging and golden-verifying this revision. Note item (i)'s `(| |)`
resurrection **reverses part of** that removal, with new (string) meaning — a concrete,
tracked reversal, not a silent one.

## 3. Go/no-go summary

- **Settled and ready to design against now (a–g):** the dotted-mechanism core — dot-
  application binding, dotted data variants replacing `(Variant Data)`, dotted no-`::` paths,
  `key.Value` universal pairing, `Map.( … )` surface, Nomos-chosen map lowering, unchanged
  capitalization/no-space-pairs. These need the raw-layer binding (2.1) and the variant-
  encoding change (2.2) but no delimiter reassignment.
- **Leaning, needs a separate go (h–i):** the delimiter reshuffle (`{}` structs / `[]`
  vectors / `()` payloads) and the `()`/`(| |)` string forms. `() = payload` is firmed by
  ruling 11; the rest of the reassignment is not final.
- **Closed:** accept-any-delimiter (not pursued). **Unknown:** Nomos's own grammar.
