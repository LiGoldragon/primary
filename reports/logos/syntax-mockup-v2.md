# Logos + Nomos — syntax mockup v2 (psyche-authored base)

Supersedes `syntax-mockup-v1.md`. The psyche rejected v1 root-and-branch and **wrote
logos himself**; his sample is the authoritative base here. This mockup formalizes his
sample minimally, flags every deviation loudly, answers his embedded questions with
researched fact, and draws the two worked examples under both the current nota
delimiters and his proposed reshuffle. It invents no taxonomy.

Discipline: **[psyche-written]** (his exact text), **[licensed by ruling]** (cited from
`design-v0.md`), **[deviation — reason]** (any change from his sample), **[proposal]**
(mine, awaiting markup), **[evidence]** (worker-verified fact + source). Written
2026-07-11 (session `schema-codex`, lane `logos-mockup-v2`). Samples parse-checked
against nota 0.7.0 `f8de7a51`.

## 0. What changed since v1 (rulings, see design-v0.md §1.2)

- **No type proliferation** [licensed by ruling]. v1's 19 specialized struct types are
  reversed: "we dont want to create a bunch of different struct types … we use a field
  or variants for everything, like visibility." Structures are general; variance is a
  field/variant.
- **Nomos — dropped, then REINSTATED** [licensed by ruling, recorded without smoothing].
  He first said "we drop nomos … schema lowers into logos through logos macros," then
  reversed: "actually, we should keep nomos, because it is its own language syntax.
  logos is a rust-equivalent, but our macros will not be rust macros." Net: **Logos =
  the Rust-equivalent data language; Nomos = the own-syntax transformation language;
  macros are Nomos macros, not Rust macros.** Nothing is asserted about Nomos being or
  not being a separate component/daemon — he did not settle that.
- **No double colons** [licensed by ruling]. Rust paths are dotted in logos
  (`rustfmt.skip`, `rkyv.[…]`); projection owns the `.`→`::` translation.
- **Dotted-prefix pushed into nota** [licensed by ruling], superseding v1's Open
  Choice 1: "even in nota, when we expect a data variant, I would rather use
  `Variant.(Data)` (or `.[]` for vectors)."

**[evidence] The schema tuple-disallow constraint** he referenced from memory:
`schema-rust/ARCHITECTURE.md:186-197`. The schema declares only
`TypeDeclaration::{Alias, Newtype, Struct}`. A **newtype is a single-element brace
carrying just the wrapped type and no field name** — authored dotted as `Topic.{ String }`
(fixture `DecisionReceipt.{ Integer }`); a multi-field declaration is a named-field
`Struct`. There is **no multi-field tuple** — the newtype-only constraint. The schema's
landed authoring surface is already dotted-brace `.{ }`, which is what his reshuffle
(§7) aligns logos to.

## 1. The psyche-authored base, verbatim

**[psyche-written]** (exactly as he wrote it, comments and all;
`samples/v2-psyche-base.logos`):

```
Public.Newtype.(
  CommitSequence
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.(
      nota-text
      [NotaDecode NotaDecodeTraced NotaEncode])
    Derive.[rkyv.[Archive Serialize Deserialize]
            Clone Debug PartialEq Eq]]
  Integer
)

Public.Struct.(
  DatabaseMarker
  [ Literal.[[rustfmt.skip] [second.literal.thing]]
    ConfigurationAttribute.Feature.(
      nota-text
      [NotaDecode NotaDecodeTraced NotaEncode])
    Derive.[rkyv.[Archive Serialize Deserialize]
            Clone Debug PartialEq Eq]]
  [Public.CommitSequence
   Public.StateDigest
   Private.secretDigest.StateDigest]
)
```

The shapes, read out (no taxonomy invented):

- **Name first.** Payload slot 1 is the declared name (`CommitSequence`,
  `DatabaseMarker`).
- **Attributes as a typed vector** (slot 2): a `[ … ]` of attribute variants:
  - `Literal.[…]` — an escape hatch carrying verbatim foreign text.
  - `ConfigurationAttribute.Feature.(…)` — the `cfg_attr`, with `Feature` as one
    predicate-kind variant, carrying `( featureName [gatedDerives] )`.
  - `Derive.[…]` — a derive list, with dotted path-grouping `rkyv.[Archive …]`.
- **Field type / fields** (last slot): for `Newtype`, the single wrapped type
  (`Integer`); for `Struct`, a vector of fields as dotted chains
  `Visibility.name?.Type`, with an explicit name ONLY on a repeated field type —
  `Public.StateDigest` derives `state_digest`, and `Private.secretDigest.StateDigest`
  disambiguates the repeat [licensed by ruling — the established composed field-name
  rule].

## 2. His embedded questions, answered with fact

- **"where is rustfmt::skip … Where is struct … and pub … and all the derive blocks?"**
  All represented, homed as above; nothing materializes at projection.
- **Attribute terminology** [evidence, Rust reference]: `#[ … ]` are **outer
  attributes** (they apply to the item that follows; `#![ … ]` are inner). All the
  wire attributes here are outer attributes. `rustfmt::skip` is specifically a **tool
  attribute** (rustfmt is a registered external tool; it is not a built-in attribute),
  which is why his `Literal` escape hatch is the right home for it.
- **cfg_attr = configuration (conditional) attribute** [evidence]: `cfg_attr(pred, attr)`
  applies `attr` only when the build-configuration predicate `pred` holds. `feature =
  "nota-text"` is a **`feature` predicate**; other predicate kinds include `target_os`,
  `unix`/`windows`, `test`, `debug_assertions`, and the combinators `all()`/`any()`/
  `not()`. So his **`Feature` is one predicate-kind variant among several — the variant
  set can grow.** His name `ConfigurationAttribute` matches the concept exactly.
- **Literal text carried verbatim** [licensed by ruling 7]: store the tool-attribute
  path in **dotted logos form `rustfmt.skip`** (not `rustfmt::skip`); projection
  translates `.`→`::` on emit. Quoted/escape-hatch foreign text is exempt from
  capitalization semantics, so the lowercase `skip` is fine as opaque literal text.
  **[deviation withdrawn]** an earlier draft floated storing `rustfmt::skip` byte-exact;
  ruling 7 withdraws that — dotted is canonical, so his `rustfmt.skip` is not a
  deviation.
- **Multiple attributes as a vector of literals** [psyche-written, his second example]:
  `Literal.[[rustfmt.skip] [second.literal.thing]]` — one `Literal` node carrying a
  vector of literals.

## 3. Worked example 1 — CommitSequence newtype, scheme (a): current nota delimiters

Stage 1 — schema brief (`schema-rust` newtype form): `CommitSequence.{ Integer }`.

Stage 3 — Rust oracle (verbatim): `pub struct CommitSequence(Integer);` with
`#[rustfmt::skip]`, the `cfg_attr` nota-text derive gate, and the rkyv/std derive block.

Stage 2 — TrueLogos = **his base, verbatim** (the `Public.Newtype.( … )` block above).
No deviation. Every oracle token is homed: `pub`→`Public`; `struct`(newtype)→`Newtype`;
`#[rustfmt::skip]`→`Literal.[rustfmt.skip]`; the `cfg_attr` gate→`ConfigurationAttribute.
Feature.( nota-text [ … ] )`; the derive block→`Derive.[ rkyv.[ … ] Clone … ]`; the
wrapped type→`Integer`.

**Parse (a)** [evidence]: raw-parses under nota 0.7.0 — 4 root objects for the two
declarations, because each dotted head (`Public.Newtype.`, `Literal.`,
`ConfigurationAttribute.Feature.`, `Derive.`, `rkyv.`) absorbs the trailing dot into
the atom and the following delimiter is a separate sibling. Internal dots inside one
atom (`rustfmt.skip`, `second.literal.thing`) stay a single bare atom. So it parses as
text today; the `Variant.(Data)` application binding is exactly what ruling 5 pushes
into nota (not yet implemented).

## 4. Worked example 1 — same newtype, scheme (b): proposed reshuffle

[psyche proposal — leaning, NOT final]. Mapping: `{}` = struct/record, `[]` = vector,
`()` = string, `(| |)` = indentation-escaped multiline string. His record payloads
`.( … )` become `.{ … }`; vectors keep `[]` (`samples/v2-reshuffled.logos`):

```
Public.Newtype.{
  CommitSequence
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.{ nota-text [NotaDecode NotaDecodeTraced NotaEncode] }
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ]
  Integer
}
```

**[deviation — reshuffle]** the `.( … )` → `.{ … }` payload rewrite is a deviation from
his sample's delimiters; he explicitly noted his sample uses the "wrong" delimiters if
the reshuffle proceeds. **[open]** the `Literal.[rustfmt.skip]` inner delimiter: if a
literal is a string, under scheme (b) it becomes `Literal.(rustfmt.skip)`; if a
path-segment vector, it stays `[]`. Flagged, not resolved.

**Parse (b) — honest** [evidence]: scheme (b) **cannot parse today with the reshuffled
meaning.** The text raw-parses structurally (braces/brackets are balanced), but nota
0.7.0 assigns them the **old** meanings — a `{}` is a brace, not a "struct"; a `()` is
a record/application, not a "string" — so no meaningful parse results without a grammar
change. Worse, the reshuffle's multiline-string form `(| |)` **errors outright** in
0.7.0: a `(|` … `|)` probe returns `RAW-PARSE ERROR: UnexpectedClose { found: ')' }`,
because pipe-paren machinery was **removed** on the way to 0.7.0.

**What the nota grammar change concretely requires:**

1. **Delimiter reassignment**: `{}`→struct/record, `[]`→vector only (drop `[]`-as-
   string), `()`→string (drop `()`-as-record). Every existing consumer that reads a
   record as `()` or a string as `[text]` must migrate.
2. **Resurrect pipe-paren** `(| |)` with a NEW meaning (indentation-escaped string) —
   note this re-adds machinery just removed, verified above by the erroring probe.
3. **Dot-application binding** (ruling 5): `Variant.{Struct}`, `Variant.[Vector]`,
   `Variant.(String)` must bind the dotted head to the following payload as one
   expectation-driven application node, instead of the dot riding on the preceding atom.
4. **Map delimiter decision** (his open option): `()`, `[]`, or **no delimiter at all**
   — a map as a vector of pair-structs by expectation. Undecided.

**[evidence] Precedent** for a byte-verifiable grammar migration: the pipe-paren /
pipe-brace **removal** already landed by nota 0.7.0 (directly verified here — the
`(| |)` probe now errors where 0.5.1 accepted it). That removal is the template for how
this reassignment would be staged and verified against goldens; the reshuffle is the
same kind of tracked migration in reverse-and-sideways.

## 5. Visibility — two forms on the same example, trade-off stated (his pick)

**[psyche ruling — his choice to make]** he offered both.

Form A — **outer variant** (his sample): `Public.Newtype.( CommitSequence [attrs]
Integer )`. Trade-off: visibility reads first and dispatches the whole node, but it
multiplies the top-level variant set into a visibility × kind cross-product
(`Public.Newtype`, `Private.Newtype`, `Public.Struct`, `Private.Struct`, …).

Form B — **variant field** (`[Public Private]` slot on a general structure):
`Newtype.( Public CommitSequence [attrs] Integer )`, with visibility as an ordinary
field. Trade-off: keeps one general `Newtype` node and expresses visibility as a
`[Public Private]` variant field — no cross-product, aligning with ruling 2 (no type
proliferation) — at the cost that visibility is no longer the outermost dispatch key.

Not picked. (Ruling 2 leans toward Form B, but he reserved the decision "if it's easier
to deal with.")

## 6. Where the WireNewtype compression now lives — a Nomos macro sketch

[proposal, own syntax, minimal]. Not a logos type (ruling 2) and not a Rust macro
(ruling 1); a **Nomos** macro whose job is schema-side compression: expand a brief
schema newtype into the wordy `Public.Newtype.( … )` logos form with the standard
attribute vector (`samples/v2-newtype.nomos`, illustrative, NOT nota-parse-checked
because Nomos's grammar is unsettled — [open]):

```
macro wireNewtype (name Inner) -> logos {
  Public.Newtype.( name standardWireAttributes Inner )
}

let standardWireAttributes =
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[ rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq ] ]
```

The point is placement, not syntax: the constant wire attribute vector is bound once in
Nomos and spliced by the macro, so logos itself keeps ONE general `Newtype` structure
rather than a `WireNewtype` type.

## 7. Parse verdict and reproduction

**One line:** scheme (a) — the psyche's base — raw-parses under nota 0.7.0 today (dotted
heads split, awaiting the ruling-5 binding); scheme (b) parses only structurally under
nota's OLD delimiter meanings and its `(| |)` string form errors outright, so the
reshuffle requires a real, staged nota grammar migration (delimiter reassignment +
dot-application binding + pipe-paren resurrection).

Samples: `reports/logos/samples/v2-psyche-base.logos`, `v2-reshuffled.logos`,
`v2-newtype.nomos`. Harness (throwaway, not committed): `scratchpad/notaparse` against a
`git-archive/nota` worktree at `f8de7a51` (nota 0.7.0). Annotation tags per section
header above; `[licensed by ruling]` cites `design-v0.md` §1.2.
