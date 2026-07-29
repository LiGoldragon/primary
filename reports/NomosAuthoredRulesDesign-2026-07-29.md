# Authored Nomos: the TextualNomos Surface and Load Path

A design proposal for how transformation rules are authored as data in text,
loaded by the protos infrastructure, and executed by the Nomos engine. This is
the missing TextualNomos surface the crate itself names as open: "TextualNomos
... remains an open design question. Nothing in this crate parses or prints a
Nomos text surface" (core-nomos lib.rs lines 8-14).

This document is a proposal. Settled law is quoted verbatim with its log and
entry. Proposal text is the designer's and marked as such. Where Nomos lives
is settled law, restored from recovery and recorded in section 8. Remaining
open decisions for the psyche are collected in section 9.

## 1. The Existing Machinery

**Terminology (ruled, 2026-07-29):** this document uses **transformer**, not
macro, as the prose name for the authored unit. **[ruled]**
(PsycheVisionReacquisition-2026-07-29.md Entry 5, "the transformer crux"):

> I'm going to use the word transformer instead of macro because I think
> macro is overloaded and it doesn't... I think agents associate it too much
> with string transformation, and this is really a type transformation.

Existing Rust identifiers (`MacroDefinition`, `MacroPackage`, `MacroIdentity`,
`MacroKind`, `NomosError::UnknownMacro`, and similar) predate this ruling and
stay accurate as code literals — they are quoted or named here exactly as they
exist in the crate, not renamed by this document. Prose below says
transformer; code-identifier references keep their actual spelling.

The production Nomos engine is already a transformers-as-data system. The design
does not start from zero.

**MacroDefinition** (core-nomos/src/definition.rs) is "one macro, entirely as
data: its stringless name, its kind, its typed input signature ... and its
result template ... a macro is a value." Its fields, all typed:

1. `name: Identifier` (positional: the transformer's stringless name)
2. `kind: MacroKind` (Named or Structural with a SectionDefault)
3. `input: InputSignature` (the `{ ... }` meta-shape as data)
4. `template: ResultTemplate` (quoted logos skeleton with escape nodes)

**The escape algebra** (template.rs) is closed at three members: `Realize`
(unquote one bound value with an optional name transform), `Invoke` (recursively
call another transformer by identity), and `Splice` (expand a bound sequence into a
vector). This is the system the psyche confirmed: **[confirmed]** "transformers
are data" (ShapeAndSliceRulings entry 8, confirmed 2026-07-27; the original
turn is unlocated).

**MacroPackage** (package.rs) is "Nomos stateful at rest": a content-identified
`MacroDefinitions` table keyed by `MacroIdentity`, plus a sibling NameTable
excluded from the content hash. The package is rename-stable by construction:
renaming a transformer edits only the sibling NameTable.

**The engine** (engine.rs) applies the package to a `WholeEthos` through
`MacroPackage::apply` / `apply_enriched`, producing `Lowering` (a
`Vec<EncodedItem>` plus a Logos NameTable). Evaluation is typed end to end; no
text crosses this path.

**What is missing:**

1. **No authoring surface.** Transformers are constructed by Rust functions in
   `fixtures.rs`. There is no file format, no text syntax, no loading from
   authored artifacts.

2. **The enriched generation surface is not data.** `GenerationClass` variants
   are dispatch tags; `generation.rs` (1,890 lines) builds method and match
   skeletons directly in hardcoded Rust, routed through string-bearing machinery
   (`name_boundary.rs`, `prelude.rs`). The compilation notes: "the no-strings
   law is honored exactly one file deep" (ProtosEngineDesign section 14).

This proposal addresses gap 1 entirely and frames gap 2 as a growth path within
the same surface.

## 2. The Transformer as an Authored Object

A transformer (a `MacroDefinition` or a `MacroPackage`) is authored data. It has
a name, and that name is a word like any other authored word. The identity
question has a standing answer:

**[ruled]** (DesignReviewRulings entry 3): "no, nothing declares the coreID, the
coreID is allocated by the translator on receiving an unallocated word."

The transformer's name is an authored word. When the translator receives it, the
translator allocates its encodedID. There is no special minting ceremony. The
word `WireNewtype` arrives at the translator, receives an encodedID in the
module's table, and becomes durably identifiable. The same mechanism that gives
`Status` or `Entry` their identities gives `WireNewtype` its identity.

The `MacroIdentity(u32)` that currently keys the package-internal table is a
package-local mint index (identity.rs line 13: "a monotonic package mint").
Under the full authored path, this local index relates to the translator's
encodedID the same way any internal representation relates to the durable
identity: the translator allocates the durable ID when the authored word first
arrives; the package-local index is implementation structure.

## 3. The TextualNomos Syntax

### 3.0 The Two-TextualForm Law

**[ruled] 2026-07-17** (textual-form-vision-design-v1.md lines 78-80, restored
by `RecoveredNomosVision-2026-07-29.md`): Nomos gets a structural table so
plain raw NOTA decodes into transformers first, with the dollar-sigil / double-angle
template spelling coming later as a second form ("we can do that"). Two
TextualForms for Nomos over one EncodedForm: a plain-NOTA base door and a
richer `$`/`<<>>` sibling. This is the founding multiple-textualforms-per-
encodedform vision (2026-07-17, session 29d00eb1 line 108, quoted in full in
section 8 below): "the vision even allowed multiple textualforms per
encodedform."

This document was previously structured the other way around — the sigil
form presented as the (only) TextualNomos design, with no base door at all.
That is corrected here. Section 3.1-3.9 below present the **base door**: the
v1 authoring surface, spelled using only the seven existing protos triggers
(no new lexer or raw-discovery work). Section 3.10-3.11 present the
sigil-rich form as the **second textualform**, marked throughout as the ruled
future refinement it is — not yet built, and not this design's v1 scope.

### 3.1 Design Constraints

The syntax is a textualform view on typed encoded data. Every syntactic element
maps to a typed position in a fully typed record. This is the strict invariant:

**[confirmed]** (SliceOneRulings entry 9): "nametree and structural tree from
the protos library drive all the decoding and encoding to/from text with DATA -
strict invariant. nothing else will do."

**[ruled]** (ShapeAndSliceRulings entry 2): "wtf is this garbage? Thats a vector
of strings, not typed data! it should be fully typed struct."

**[ruled]** (ProtosEngineDesign section 10): "in the nomos transformation
([ethos] to logos), there shall be *no string manipulation/introduction/reading
of any kind*", with walkers at the boundary ("that is necessary.").

No bare strings as rule content. Spellings are data on typed positions. Fields
are positional. The syntax must feel like the same language family as Ethos.

**What "template" means here (ruled, 2026-07-29):** every occurrence of
"template" in this document — `ResultTemplate`, `EnumerationTemplate`,
`NewtypeTemplate`, and the running examples' template bodies — means a typed
Logos skeleton: typed encoded data with typed placeholder (escape) positions,
never text. String templates are explicitly ruled out. **[ruled]**
(PsycheVisionReacquisition-2026-07-29.md Entry 5):

> I was originally asking, and I still want the transformation to be strictly
> through the encoded form. So there's strictly no string manipulation of any
> kind, or like if we talk about template, I think you mean string templates,
> in which case that's not at all what I'm looking for.

Transformation is strictly encoded-form to encoded-form. Encoded form may
also be called **the true form**: "All of our three languages, well, four if
we include Noto, have textual form and encoded form, which we could also
refer to as the true form." (same Entry 5 dictation). This is a naming
option, not a replacement — "encoded form" and "true form" name the same
thing; this document continues to use "encoded form" as its working term and
notes "true form" as the psyche's alternate name for it.

**Recovered note on the input-signature vocabulary:** the psyche's own working
through the newtype case (2026-07-13, nomos-macro-model-v1.md lines 67-70)
considered the input-signature words themselves as possibly shared machinery:

> so if WireNewType only takes a name and inner type, then the input field
> would be `{ Name Type }`. Name and Type could be pretty standard things,
> perhaps nomos builtins, even a concept shared with schema somehow (it is a
> schema concept after all).

Reading (proposal, not ruled): `Name`, `Type`, `Fields`, `Variants` as
`MetaType` vocabulary may be Nomos builtins that Ethos (schema) also shares
rather than a Nomos-only vocabulary invented fresh. This document does not
resolve that sharing; it is noted here so a future design round does not
reinvent the same words independently in both languages.

### 3.2 The Base Door: Escape Positions Distinguished Structurally

The base door uses only the seven triggers that already exist in every NOTA
family profile, including plain Standard (raw-discovery profile.rs lines
381-429): the three bracket boundaries `(`/`)`, `[`/`]`, `{`/`}`; the `.`
application glyph; the `(| ... |)` carrier; whitespace; and the `;;` line
comment. No new trigger, character class, or glyph is introduced. This
directly satisfies the base-door requirement in section 3.0: the plain-NOTA
form decodes first, before any sigil machinery exists.

The 2026-07-13 ruling (session 0fd2d07c line 572, restored in
`RecoveredNomosVision-2026-07-29.md`) requires escape positions to be visually
distinguished from ordinary literal content:

> we should use a structural syntax, since this will be hard to tell from
> the rest of the syntax; it just looks the same as everything else, which
> is why macros conventions use `$` or `#` type prefix.

The base door satisfies this without a prefix glyph: the three escape forms
are spelled as **reserved keyword applications** — `Realize.<binding>`,
`Splice.<binding>`, `Invoke.<transformer>` — using the same dotted-application
mechanism that already distinguishes `Structural.Enumeration` from a bare
word, or `Public`/`Private` from an ordinary identifier. At any structural
position where an escape may legally appear, the typed rule for that position
is a closed alternation between the literal-word shape and these three
keyword-application shapes; `Realize`, `Splice`, and `Invoke` are reserved
vocabulary words in the Nomos nametree at that position, exactly as
`Structural` and `Named` are reserved at the kind position. The distinguishing
signal is the reserved keyword occupying a known structural slot, not a glyph
— this is visual distinction achieved through vocabulary and position, not
through new lexer machinery. The `$`/`#` sigil convention the psyche named as
precedent is the second textualform's job (section 3.10); it is not required
to satisfy the 07-13 ruling in the base door, because the base door has its
own, different, structural means of the same end.

An input-signature binding declaration (e.g. `name.Name`) is not itself an
escape use-site — it is a plain two-field record (`binding.meta`), unconditionally
interpreted under the `InputSignature` structural position, with no ambiguity
against template-body content to resolve. Only template-body positions, where
a literal word and an escape use are both legal, need the reserved-keyword
distinction above.

### 3.3 Running Example 1: the Enumeration Structural Default

The current Rust fixture (fixtures.rs lines 199-232) builds the enumeration
structural default. Its data content:

- Name: `Enumeration`
- Kind: `Structural(SectionDefault::Enumeration)`
- Input: `{ name: Name, variants: Variants }`
- Template: an `EnumerationTemplate` with visibility Public, attributes invoking
  `EnumerationAttributes`, name realized from the `name` binding, empty generics,
  variants spliced from the `variants` binding.

**Proposed base-door textualform:**

```
Enumeration.Structural.Enumeration {
  (name.Name variants.Variants)
  Public Invoke.EnumerationAttributes Realize.name () [Splice.variants]
}
```

**Position-by-position mapping:**

| Syntax element                | Typed record position                             |
|:-------------------------------|:--------------------------------------------------|
| `Enumeration`                  | `MacroDefinition.name` (Identifier)               |
| `Structural.Enumeration`       | `MacroDefinition.kind` (MacroKind variant)        |
| `(name.Name variants.Variants)`| `MacroDefinition.input` (InputSignature)          |
| `name`                          | `InputParameter.binding` (Identifier)             |
| `Name`                          | `InputParameter.meta` (MetaType::Name)            |
| `variants`                      | `InputParameter.binding` (Identifier)             |
| `Variants`                      | `InputParameter.meta` (MetaType::Variants)        |
| `Public`                        | `EnumerationTemplate.visibility` (literal)        |
| `Invoke.EnumerationAttributes`  | `Escape::Invoke(MacroIdentity)` in attributes     |
| `Realize.name`                  | `Scalar::Escape(Realize{name, Identity})` for name|
| `()`                            | `Generics::none()`                                |
| `[Splice.variants]`             | `Sequence::of(Escape::Splice{variants, Variant})` |

The base-door vocabulary:

- `Realize.binding` — Realize escape (unquote one bound value, identity
  transform)
- `Splice.binding` — Splice escape (expand a bound sequence into the vector)
- `Invoke.TransformerName` — Invoke escape (recursively call a named transformer)
- Bare words — literal encoded values (identifiers resolved through the
  nametree)
- `.` — application (dotted declarations, as in Ethos)
- `{ ... }` — the template body delimiter
- `( ... )` — input signature delimiter, also generics and grouping
- `[ ... ]` — variant/vector positions

This corresponds to the existing closed escape set: `Realize`, `Splice`,
`Invoke`. The psyche's ruling confirmed exactly two escape primitives plus one
recursion mechanism: **[ruled]** "the escape set is closed at two primitives
(`$x` realizes, `$@xs` splices — 'agreed')" (ProtosEngineDesign section 11).
That ruling names the sigil spellings (`$x`, `$@xs`) because that is how the
question was put to the psyche at the time; the ruling is about the *count and
kind* of escapes (two primitives plus Invoke as the recursion mechanism), not
about the sigil glyphs, which the base door spells as reserved keyword
applications instead. `Invoke` is the recursion mechanism, not a third escape
primitive; the psyche ruled the closed set and `Invoke` is the recursive call
into another transformer by identity.

### 3.4 Running Example 2: the Newtype Structural Default

The production fixture (fixtures.rs lines 131-159):

```
WireNewtype.Structural.Newtype {
  (name.Name type.Type)
  Public Invoke.WireAttributes Realize.name Realize.type
}
```

Mapping: `Public` is the literal `Visibility::Public` for the produced item.
`Invoke.WireAttributes` invokes the attributes transformer. `Realize.name` realizes
the bound `name` as `Scalar::Escape(Realize{name, Identity})`. `Realize.type`
realizes the bound `type` as `Scalar::Escape(Realize{type, Identity})`.

The wrapped field's visibility (`Private`) is positional in the
`NewtypeTemplate` struct and does not appear in the syntax because it is the
fixed structural default for that position. **Open styling question (minor,
not in the section 9 list):** should the template syntax make the wrapped-field
visibility explicit (e.g.
`Public Invoke.WireAttributes Realize.name Private.Realize.type`) or should it
remain positional and implicit? The current `NewtypeTemplate` struct carries it
as an explicit field. Making it visible in the textualform is the more honest
position.

With explicit wrapped visibility:

```
WireNewtype.Structural.Newtype {
  (name.Name type.Type)
  Public Invoke.WireAttributes Realize.name Private Realize.type
}
```

### 3.5 Running Example 3: the Named Attributes Transformer

The `WireAttributes` transformer (fixtures.rs lines 108-115):

```
WireAttributes.Named {
  ()
  [
    rustfmt.skip
    (| nota-text |).[ nota.NotaDecode nota.NotaDecodeTraced nota.NotaEncode ]
    [ rkyv.Archive rkyv.Serialize rkyv.Deserialize Clone Debug PartialEq Eq ]
  ]
}
```

This is a `ResultTemplate::Attributes(Sequence<Attribute>)`. The input is unit
`()`. The body is a vector of literal attributes (no escapes at all, so this
example is identical in the base door and the second form):

- `rustfmt.skip` is `Attribute::ToolPath(PathNode{["rustfmt", "skip"]})`
- The `(| nota-text |)` carrier is a `ConfigurationAttribute` with a
  `ConfigurationPredicate::Feature("nota-text")` wrapping a derive group
- The `[ ... ]` square bracket group is a `DeriveGroup`

The syntax reuses the NOTA carriers and boundaries exactly as the existing
profile defines them — the same seven triggers listed in section 3.2, present
under both the Standard and NomosExtended glyph sets (section 3.11 corrects
what actually differs between the two).

### 3.6 Running Example 4: the Particular-Struct Default

```
ParticularStruct.Structural.Struct {
  (name.Name fields.Fields)
  Public Invoke.WireAttributes Realize.name () [Splice.fields.FieldRuleDispatch.Public]
}
```

The splice element carries the field-name rule and the per-field visibility:
`Splice.fields.FieldRuleDispatch.Public` means
`Splice{fields, SpliceElement::Field{FieldRuleDispatch, Public}}`.

### 3.7 A Complete `.nomos` File: the Wire Package

A `.nomos` file is a complete `MacroPackage`. It follows the six-slot document
structure that Ethos uses (the fixtures confirm this: `spirit-min.ethos` has six
top-level blocks). Loading such a file is one population path for the package
data, not the only one — see section 4.2 step 0 on the manifest and the
"possibly, but not necessarily" hedge. The Nomos slots carry:

```
;; Wire package revision 1
{1}
;; No interface inputs
[]
;; No interface outputs
[]
;; Transformer definitions
{
  WireAttributes.Named {
    ()
    [
      rustfmt.skip
      (| nota-text |).[ nota.NotaDecode nota.NotaDecodeTraced nota.NotaEncode ]
      [ rkyv.Archive rkyv.Serialize rkyv.Deserialize Clone Debug PartialEq Eq ]
    ]
  }

  EnumerationAttributes.Named {
    ()
    [
      rustfmt.skip
      (| nota-text |).[ nota.NotaDecode nota.NotaDecodeTraced nota.NotaEncode ]
      [ rkyv.Archive rkyv.Serialize rkyv.Deserialize Clone Copy Debug PartialEq Eq ]
    ]
  }

  WireNewtype.Structural.Newtype {
    (name.Name type.Type)
    Public Invoke.WireAttributes Realize.name Private Realize.type
  }

  ParticularStruct.Structural.Struct {
    (name.Name fields.Fields)
    Public Invoke.WireAttributes Realize.name () [Splice.fields.FieldRuleDispatch.Public]
  }

  Enumeration.Structural.Enumeration {
    (name.Name variants.Variants)
    Public Invoke.EnumerationAttributes Realize.name () [Splice.variants]
  }
}
;; No enriched generation selection (plain package)
{}
;; No capsule metadata
{}
```

### 3.8 Name Transforms in the Syntax

The `NameTransform` variants (Identity, FieldName, Screaming, PascalCase) apply
to Realize escapes. Bare `Realize.name` is identity. Transformed realizations
use a further dotted suffix:

- `Realize.name` — `NameTransform::Identity`
- `Realize.name.FieldName` — `NameTransform::FieldName`
- `Realize.name.Screaming` — `NameTransform::Screaming`
- `Realize.name.PascalCase` — `NameTransform::PascalCase`

These are data on a typed position (the `Realize.transform` field), not string
operations: "name synthesis inside `Realize` instead of becoming a fourth
escape" (template.rs line 93-94). The NameTableBoundary performs the actual
derivation at the boundary, not during evaluation.

### 3.9 Running Example 5: ScopeOf Expansion

This is the complex case. `DomainScope.ScopeOf.Domain` is a single authored
Ethos declaration that must expand into complete ordinary Logos data: 38 scope
enums mirroring the 38 domain enums, plus conversions and containment
operations.

The ScopeOf expansion is a different kind of transformation from the structural
defaults above. The structural defaults lower one Ethos declaration into one
Logos item. ScopeOf reads the entire Domain tree and produces many items. The
existing escape algebra handles per-declaration lowering. ScopeOf needs a way
to express recursive tree traversal as data.

Recursive transformer invocation itself is not open — it is a ruled requirement:
"We also need to be able to call more macros recursively." (2026-07-13,
session 0fd2d07c line 572, restored in `RecoveredNomosVision-2026-07-29.md`).
What is open is the mechanism that satisfies it for tree-shaped recursion
(Decision 1, section 9); `Invoke` already satisfies simple, non-tree-shaped
recursive calls.

**The gap in the current escape algebra:** the existing `Splice` walks a flat
vector (fields or variants) and produces one element per input. ScopeOf must
walk a tree recursively: for each payload-bearing variant in Domain, produce a
scope enum that mirrors it; for each sub-enum, recurse. The escape algebra has
no tree-fold construct today.

**Proposed extension (matter, not ruled):** a fourth escape form, `Fold`, that
expresses recursive tree traversal as data. This proposal is one candidate way
to satisfy the ruled recursion requirement for the tree-shaped case; it is not
itself something the psyche has ruled on, and Decision 1 in section 9 leaves
open whether Fold, a separate mechanism, or a deferred design is the right
shape.

```
ScopeOfExpander.Named {
  (source.Name target.Name)
  [
    Splice.target.[ All Splice.source.Variants.MirrorScope ]
    Fold.source.PayloadVariants {
      (child.Name childSource.Name)
      Splice.child.[ All Splice.childSource.Variants.MirrorScope ]
    }
  ]
}
```

Where:

- `Splice.source.Variants.MirrorScope` — a new splice element kind that mirrors
  each source variant into the scope enum (preserving the variant name,
  converting a payload-bearing variant into a scope-typed payload)
- `Fold.source.PayloadVariants { ... }` — the recursive fold: for each
  payload-bearing variant in the source, bind `child` to the derived scope
  sub-enum name and `childSource` to the source sub-enum, then produce items
  from the body and recurse

The `Fold` construct is the recursion mechanism proposed for the ScopeOf need.
It is data: a closed binding signature and a template body that executes per
tree node. The recursion terminates when a level has no payload-bearing variants
(all variants are leaves).

**Why Fold rather than Invoke:** `Invoke` calls a named transformer by identity, but
it does not bind new parameters per recursion level. Fold binds fresh parameters
at each recursive step (the child name and child source change at each level of
the Domain tree). Making Fold a new escape variant rather than overloading Invoke
keeps the algebra honest about what it does.

The invocation from Ethos:

```
DomainScope.ScopeOf.Domain
```

This is sugar in Ethos. The Nomos engine, on encountering a `ScopeOf`
declaration, locates the `ScopeOfExpander` transformer (or a built-in transformer
handling this item kind), loads the source tree (Domain's full type structure
from the encoded Ethos), and executes the expansion template. This is the
concrete instance of the ruled shape from section 8: Ethos carries the sugar
declaration; Nomos, in its own files, carries the expansion.

Open decisions carried forward to section 9: whether `Fold` is the right
mechanism for the recursion requirement (Decision 1), and whether ScopeOf
dispatches through the transformer system or a built-in (Decision 2).

### 3.10 The Second TextualForm: the Sigil-Rich Spelling (Proposal, Ruled Future Refinement)

Section 3.0 restored the 2026-07-17 ruling that a second, sigil-rich
textualform comes later, over the same EncodedForm, once the base door exists.
This section illustrates the target spelling this document previously
presented as the (only) design. It remains useful as a sketch of what the
second form is for — terser, template-like spelling — but it is not built, and
its concrete sigil assignment is open (Decision 4, section 9). Nothing below
is machinery; section 3.11 states plainly what exists and what would need
building.

Illustrative second-form spelling of the Enumeration example (section 3.3):

```
Enumeration.Structural.Enumeration {
  ($name.Name $variants.Variants)
  Public @EnumerationAttributes $name () [$@variants]
}
```

Illustrative second-form spelling of the Newtype example (section 3.4):

```
WireNewtype.Structural.Newtype {
  ($name.Name $type.Type)
  Public @WireAttributes $name Private $type
}
```

Illustrative sigil vocabulary sketch (not ruled, not built):

- `$binding` — Realize
- `$@binding` — Splice
- `@TransformerName` — Invoke
- `$name.FieldName` / `$name.Screaming` / `$name.PascalCase` — transformed
  Realize, by the same dotted-suffix convention as the base door

### 3.11 What the Second Form Actually Requires

This document previously claimed the raw-discovery `NomosExtended` glyph set
was "pre-provisioned for this exact purpose" — built specifically to carry a
sigil escape syntax. Reading the machinery directly (raw-discovery
`src/profile.rs`) shows that claim was not accurate. The honest state:

- `GlyphSet` has exactly two variants, `Standard` and `NomosExtended`
  (profile.rs lines 40-44), and they differ by exactly one thing:
  `NomosExtended` removes `$` from the profile's `forbidden_bare_characters`
  set (profile.rs lines 430-434: Standard forbids `"` and `$`; NomosExtended
  forbids only `"`).
- `$` is **not** a trigger. It has no entry in the seven-trigger definition
  table (profile.rs lines 381-429: two boundaries, one carrier, application,
  whitespace, line comment — no `$`, no `@`). It has no capture semantics and
  never participates in longest-match trigger resolution, because it is not a
  trigger at all.
- Under `NomosExtended`, `$x` is an ordinary bare atom — a plain identifier
  whose first character happens to be `$` — with no special meaning to
  raw-discovery. Nothing downstream currently reads that leading `$` as an
  escape marker.
- There is no `$@` or `@` machinery anywhere in the codebase. Both were
  spellings this document invented for the illustration in section 3.10, not
  things raw-discovery, structural-codec, or core-nomos implement.
- "Seals cleanly" (a claim in an earlier draft) is trivially true: removing one
  character from a forbidden-bare-characters set cannot introduce a trigger
  ambiguity, because it does not touch the trigger table at all. This was not
  evidence of purpose-built provisioning; it is the necessary consequence of
  the change being that narrow.
- The crate's own documentation names what `GlyphSet` and `RawProfile` actually
  are: "compatibility selectors" (raw-discovery lib.rs line 34) — a
  compatibility-naming mechanism for the two established NOTA-family profiles,
  not an escape-syntax feature.

**What a real sigil form would require**, honestly, as second-form work — not
yet done, not scoped by this document:

- Either new trigger/character-class design in raw-discovery (a `Punctuation`
  or `LeadingCharacterClass` trigger for `$`, with the associated ambiguity
  proof against the existing seven — `can_tie` in profile.rs governs this),
  giving raw-discovery itself a notion of an escape-marked atom; or
- Handling at the structural-codec layer instead: leave raw-discovery's atom
  recognition untouched (a `$`-led atom stays an ordinary bare atom all the
  way through boundary discovery) and let the Nomos structural-codec
  vocabulary, when it resolves that atom against the nametree at an escape-
  legal position, treat a leading `$` in the atom's *text* as a second-form
  spelling of `Realize`/`Splice`/`Invoke` — a convention at the typed-parsing
  layer, not a new lexical trigger.

Which of these two shapes is right, or whether a third shape is better, is not
decided here; it is the second-form design's task, separate from and after
the base door.

## 4. The Load Path

### 4.1 Overview

The recovered load-path statement (2026-07-22 14:19 UTC, session bc636bdb
line 444, restored in `RecoveredNomosVision-2026-07-29.md`) is the controlling
account and is quoted here in full because it settles more than any single
step below:

> I think I was first designing thinking the nomos logic would be applied to
> schema text, but then later realized that it would be pure-data
> transformation (the data for this machinery is *populated* (possibly, but
> not necessarily) by parsing nomos files (with a manifest for dependency
> resolution and an entry-point file) into nomos encodedform + nametree
> data - only after the nomos data is loaded in its daemon (with a slot,
> ostensibly; it should be able to run several versions - same
> short-addressale ID concept we use so much; agent-friendly [...]) can the
> schema tranformation request use the slotted nomos transformer to send its
> encodedform + nametree [...] to generate logos encodedform + nametree, and
> probably then rust textualform

Read plainly, this settles: (1) the transformation is pure-data, not text
manipulation, confirming the strict invariant already in section 3.1; (2)
parsing `.nomos` files is **one** population path for the encoded transformer
data, not the only one — "possibly, but not necessarily" is the psyche's own
hedge, preserving an operational-editing endgame where the data is populated
or edited directly and file-parsing is bypassed; (3) file-based loading needs
a manifest for dependency resolution plus an entry-point file, not an
unordered pile of `.nomos` files; (4) the Nomos daemon runs the loaded package
in a **slot**, and can run several versions simultaneously, addressed by the
same short-addressable-ID concept used elsewhere in the engine; (5) the schema
(Ethos) transformation request uses the *slotted* Nomos transformer by
addressing it, sending its own encodedform + nametree to be transformed.

```mermaid
flowchart TD
  A[Authored .nomos text, one population path among possibly others] --> B[raw-discovery boundaries, base-door profile - no dollar sigil needed]
  B --> C[structural-codec typed parsing under protos nametree/structural-tree]
  C --> D[Typed transformer records: MacroDefinition, InputSignature, ResultTemplate]
  D --> E[Seal: translator allocates encodedIDs for transformer names and binding names]
  E --> F[MacroPackage as encoded data with content identity]
  F --> G[Nomos daemon loads the encoded MacroPackage into a slot, short-ID addressed]
  G --> H[Ethos transformation request addresses the slotted transformer with its encodedform + nametree]
  H --> I[Engine executes MacroPackage.apply against WholeEthos input]
  I --> J[WholeLogos output: encoded items plus Logos NameTable]
```

### 4.2 Step by Step

**Step 0: manifest and entry point.** Before any `.nomos` file is read, a
manifest resolves dependencies between `.nomos` files and names an entry-point
file — the same shape the recovered quote requires. This document does not
design the manifest format; it records the requirement so it is not lost
again.

**Step 1: raw-discovery boundaries.** The `.nomos` file is text. The base-door
syntax (section 3.2) needs nothing beyond the Standard profile's seven
triggers — no `$` admission is required for v1. raw-discovery's
`BoundaryReader` finds the block boundaries: the six top-level document slots
(braces, brackets), the transformer definition blocks, the template bodies,
the input signatures. No grammar is applied here; just balanced delimiters and
carrier-opaque scanning. (The `NomosExtended` profile remains relevant only to
the second textualform, section 3.10-3.11, not to this step.)

**Step 2: structural-codec typed parsing.** The structural evaluator parses each
discovered block under the typed rule vocabulary for Nomos. The rule vocabulary
for Nomos is a downstream vocabulary extending the structural-codec kernel,
exactly as the Ethos vocabulary and the Rust vocabulary extend it. The
`Position<Role, Root, Descriptor>` records define the typed positions of a
`MacroDefinition` rule (its name position, kind position, input position,
template position), using the same `SharedDescriptor` machinery that Ethos and
Rust use: `Declaration` descriptors for the transformer name, `Literal` descriptors
for fixed vocabulary words (`Structural`, `Named`, `Public`, `Private`,
`Name`, `Type`, `Fields`, `Variants`), and `Delegate` descriptors for
recursive structures.

This is the strict invariant in action: "nametree and structural tree from the
protos library drive all the decoding and encoding to/from text with DATA -
strict invariant. nothing else will do."

**Step 3: typed records.** The evaluator produces typed `MacroDefinition`
records, `InputSignature` records, and `ResultTemplate` trees. Every identifier
in the records is an `Identifier` from the nametree. No strings remain.

**Step 4: seal with translator.** The authored transformer names and binding names are
submitted to the sema-translator. The translator allocates encodedIDs for each
new word in the appropriate module table. **[ruled]** (DesignReviewRulings
entry 3): "nothing declares the coreID, the coreID is allocated by the
translator on receiving an unallocated word." Transformer names are authored words
and receive their encodedIDs by the same mechanism as any other authored name.

**Step 5: encoded MacroPackage.** The sealed definitions, their identifiers, and
the structural defaults compose into a `MacroPackage` with its sibling
NameTable. The package's `content_identity()` hashes the stringless
`MacroDefinitions` table, excluding the NameTable. The package is "Nomos
stateful at rest" — an archivable, content-addressed value.

The package is a `Capsule<NomosKind>` under the ruled generic-struct model
(**[ruled]** SliceOneRulings entry 1: "Generic struct"). The capsule kind
is a type parameter; the capsule pins the complete composition of its nametree
(**[ruled]** ShapeAndSliceRulings entry 1: "yes").

**Settled (not a decision point):** Nomos implements the protos
`Capsule`/`ShortIdentifier` traits like its siblings. **[ruled] 07-25**
(ProtosEngineDesign-2026-07-28.md section 8, "Capsule"): "capsule
and short-identifier are protos concepts — protos traits with per-engine
implementations." The 07-25 ruling's exception is rust-logos specifically
("rust-logos gets no capsule"), not Nomos; Nomos gets its own per-engine
implementation of both traits, the same as Ethos and Logos do. This document
previously listed "Nomos capsule kind" as an open decision (whether Nomos gets
its own kind or composes with the Ethos capsule); the 07-25 ruling settles it
in favor of Nomos having its own implementation, "like its siblings," which is
the own-kind shape, not composition into the Ethos capsule.

**Step 6: engine loads, slotted.** The Nomos engine daemon loads the encoded
`MacroPackage` from its sema database into a slot. Per the recovered load-path
quote, the daemon "should be able to run several versions" of a transformer
concurrently, each occupying its own slot, and each slot is addressed by the
same short-addressable-ID concept used throughout the engine ("agent-friendly").
A schema (Ethos) transformation request names the slotted transformer it wants
by that short ID and sends its own encodedform + nametree to it — this is the
addressing step the recovered quote describes as "the schema tranformation
request use[s] the slotted nomos transformer". The package is the transformer;
the engine is the executor/interpreter that applies it.

**Step 7: engine executes.** `MacroPackage::apply(ethos, ethos_names)` or
`apply_enriched(ethos, ethos_names)` runs the existing evaluation machinery:
bind the input signature, evaluate the template, realize escapes, splice
sequences, invoke recursively. The engine's role is interpreter/executor over
the data; the transformation rules live in the package.

**Step 8: WholeLogos output.** The engine produces `Lowering`: a
`Vec<EncodedItem>` (the Logos encoded form) and a Logos NameTable composed with
the Ethos compatibility slice.

### 4.3 The Engine's Role Shrinks

The engine (`engine.rs`, `Evaluator`) is already an interpreter: it walks the
template tree, matches escapes, binds inputs, and produces encoded logos values.
The authored surface does not change this role; it eliminates the fixture
constructors as the source of truth. The engine does not become smaller; it
becomes the only consumer of authored package data rather than a consumer of
Rust-constructed package data.

The enriched generation surface (`generation.rs`, 1,890 lines) is the part that
does NOT yet fit this model. Its `GenerationClass` variants are dispatch tags
that select hardcoded Rust generation logic. The path from generation classes
to authored template data is the next phase: each generation class would become
an authored transformer (or set of transformers) in the `.nomos` file, using the extended
escape algebra (including Fold for tree-walking constructs like the method-body
match skeletons). This is growth, not immediate work.

### 4.4 Nomos Runtime Scope (settled, 2026-07-29)

The Nomos engine's runtime is not scoped to one transformer's local input and
output types. **[ruled]** (PsycheVisionReacquisition-2026-07-29.md Entry 5):

> Obviously, Nomos is going to have to load all of the Logos types into its
> runtime because it has to convert into them, and it's going to have to load
> all of the Ethos type, obviously, too, because it's going to convert them.
> So the Nomos engine knows about everything. Well, not Rust, obviously, but
> it knows about the three languages.

The engine loads the **complete Ethos and Logos type universes** into its
runtime — not just the declaration a given transformer touches. It knows the
three languages (Ethos, Nomos, Logos), not Rust. Placeholders (the escape
positions in the typed skeleton, section 3.1-3.2) key the movement of typed
values from Ethos input into generated Logos output:

> it has to take the handwritten textual form Nomos and create this
> transformation logic where the placeholders with the dollar signs or
> whatever are... hold the key as to what gets put where, from the Ethos type
> into the generated Logos type that it produces, or Logos types, probably,
> plural, because some of these transformations can create quite complex code.

Two consequences for this design that were not previously stated:

- **Plural output types.** One transformer application may produce more than
  one Logos type (the running examples in section 3 each produce one item;
  this is the common case, not a universal one).
- **Positional insertion, including into vector slots.** A placeholder can key
  insertion "into a particular spot in a vector where a certain item gets
  inserted" (Entry 5) — not only whole-item production but insertion at a
  specific position within a produced sequence. The existing `Splice` escape
  (section 1) expands a bound sequence into a vector wholesale; targeted
  positional insertion into an existing or partially-built vector is a
  narrower operation than `Splice` currently expresses, and is not designed
  in this document. It is noted here as a real requirement the escape algebra
  does not yet cover, separate from the Fold proposal.

This section is settled scope, not a decision point: the runtime loading all
three languages, and placeholders keying cross-type movement (plural,
positional), is the psyche's own account of how the engine must work, not a
design choice open to alternatives.

## 5. Execution Semantics Sketch

### 5.1 What a Rule Application Is

A rule application is:

1. **Typed match over Ethos carrier positions.** The engine receives an
   `EncodedDeclaration` (an `EncodedType` with a `Visibility`). The
   `SectionDefault::of_encoded_type` dispatch selects which transformer handles which
   declaration kind. The input signature's `MetaType` vocabulary binds the
   declaration's typed positions: `Name` binds the identifier, `Type` binds a
   newtype's wrapped reference, `Fields` binds a struct's fields, `Variants`
   binds an enum's variants. This is exhaustive over declaration kinds and
   total; an unmatched meta-type is a typed error.

2. **Typed construction of Logos carriers.** The template is a quoted Logos
   skeleton where non-literal positions are escapes. `Realize` unquotes one bound
   value (an identifier or a type reference from the Ethos side) into its
   corresponding Logos position. `Splice` expands a bound vector (fields or
   variants) through a per-element production. `Invoke` recursively evaluates
   another transformer. Every produced value is a genuine `core_logos` typed value
   (`EncodedItem`, `Newtype`, `Struct`, `Enumeration`, `Field`, `Variant`,
   `TypeReference`, `Attribute`). No string is ever produced.

### 5.2 How ScopeOf's Recursion Is Expressed as Data

Under the proposed Fold extension, the ScopeOf expansion would work as follows:

1. The Ethos engine parses `DomainScope.ScopeOf.Domain` and produces an encoded
   declaration whose type is `EncodedType::ScopeOf { target: "DomainScope",
   source: "Domain" }` (or an equivalent positional carrier).

2. The Nomos engine dispatches this declaration kind to a ScopeOf structural
   default (a new `SectionDefault::ScopeOf` variant).

3. The transformer's input signature binds the target name (`DomainScope`) and the
   source tree root (`Domain`).

4. The template's Fold escape walks the Domain tree. At each level:
   - It produces a scope enum mirroring the source enum plus an `All` variant
   - For each payload-bearing variant, it recurses into the child enum
   - Recursion terminates at leaf enums (all unit variants)

5. The fold produces a flat list of `EncodedItem::Enumeration` values: one
   `DomainScope` enum at the top, and one `*Scope` enum for each intermediate
   level of the Domain tree.

6. The identity of each produced scope enum follows the ScopeOf identity
   ruling. **Note:** the psyche has not yet ruled on the ScopeOf identity
   question (see `ScopeOfIdentityBriefing-2026-07-29.md`). The two options
   (helpers as durable Universal declarations vs. helpers as implementation
   structure under the single authored identity) are open. The TextualNomos
   design works with either answer: under Option A, the Fold names its produced
   enums and submits them to the translator; under Option B, the produced
   items are implementation structure and their values are paths of existing
   source-variant encodedIDs.

### 5.3 Refusal

Refusal is typed and atomic. The existing engine already refuses loudly on
typed grounds:

- `NomosError::NoStructuralDefault(section)` — no transformer registered for a
  declaration kind
- `NomosError::UnknownMacro(identity)` — an invoke references a nonexistent
  transformer
- `NomosError::RecursionCycle(identity)` — a recursive invocation cycle
- `NomosError::MetaShape { meta }` — a meta-type does not match the
  declaration's structure
- `NomosError::UnboundInput(binding)` — a template references a binding that
  was never set
- `NomosError::EscapeShape(message)` — an escape is used in a position its
  type does not fit (splice in a scalar slot, invoke in a type position)
- `NomosError::NameTransformShape` — a name transform applied to a non-name
  binding

The authored surface adds load-time refusals (malformed `.nomos` text,
unresolvable transformer references, unknown meta-types) that are typed structural
errors, consistent with the existing conservative-refusal law: what cannot be
proven disjoint is rejected. Partial results are never produced.

For ScopeOf specifically, the expansion refuses atomically on: missing source
tree (the Domain type does not exist in the Ethos), cyclic source trees,
unsupported source structures (a source type that is not an enum tree), and
unresolvable variant references.

### 5.4 Whole-Payload Transformation (New Design Consideration, Beyond v1 Scope)

Every rule application described in section 5.1 is scoped to one Ethos
declaration producing output from that declaration's own bound input. The
psyche's Entry 5 dictation names a case this document's execution model does
not cover: a transformer whose correct output depends on **other**
declarations elsewhere in the Ethos payload, not just its own input. **[ruled,
as a requirement on the architecture]** (PsycheVisionReacquisition-2026-07-29.md
Entry 5):

> I see a quite possible scenario in which the transformation depends on
> other factors. Or in other words, the transformation happens for the entire
> payload, the entire Ethos payload. Some transformers might be affected by
> what other declarations say about objects that are involved in a particular
> transformation. Kind of like how the Rust compiler has to take so many
> things into account before it can decide that, okay, yes, the lifetimes are
> correct, the ownership is correct, the types are correct. It has to do a
> very wide spectrum of analyses before it can actually decide that, all
> right, we can start generating the assembler for this.

This is a real requirement on the architecture, not a feature this design
implements. Nothing in sections 1-5 above is described as precluding it —
section 4.4 already establishes that the engine's runtime holds the complete
Ethos and Logos type universes, which is a necessary (not sufficient)
precondition for cross-declaration analysis — but nothing in this document
designs the analysis itself: how a transformer would declare a dependency on
other declarations, how the engine would order or fix a point over the whole
payload before committing output, or what a "the lifetimes are correct, the
ownership is correct" class of check looks like for Nomos's own type system.
The rustc analogy is the psyche's own framing of the difficulty, not a
prescription to imitate rustc's specific passes.

**What this document commits to:** the running examples and load path above
(sections 3-4) are the v1, per-declaration case; nothing here should be read
as a final architecture that whole-payload analysis would have to be
retrofitted around. Whether whole-payload transformation needs its own
mechanism (a distinct transformer kind, a pre-pass over the Ethos payload
before ordinary rule application, or something else) is unscoped and left
for a future design round, explicitly marked beyond this document's v1 scope.

## 6. What Happens to slice_one.rs

`SliceOneTransformation` in `core-nomos/src/slice_one.rs` is a zero-state
hardcoded lowering of `WholeEthos` to `WholeLogos`. It is exercised only by
tests (core-nomos/tests/slice_one.rs and language-engine-witness). It has zero
production call sites.

The production path already runs `MacroPackage::enriched_fixture().apply_enriched(...)`.
`SliceOneTransformation` exists as the reference/bootstrap implementation for the
first vertical slice's limited vocabulary (enum/newtype lowering without
attributes, without enriched generation).

**The honest transition story:** `SliceOneTransformation` remains the
reference implementation until the authored TextualNomos surface can express
the same transformations it performs and the engine proves equivalence. The
proof is behavioral: the same Ethos input produces the same Logos output through
both paths. Once equivalence is proven, `SliceOneTransformation` becomes dead
code. No deletion timeline is specified here; this is a design document.

The production fixture path (`MacroPackage::wire_fixture()`,
`MacroPackage::plain_fixture()`) transitions similarly: the Rust fixture
constructors are replaced by authored `.nomos` files loaded through the
TextualNomos surface. The fixture functions become test-only equivalence
oracles.

## 7. The Generation Surface Growth Path

The enriched generation surface (`generation.rs`, `GenerationClass`) is where
"the no-strings law is honored exactly one file deep." Each `GenerationClass`
variant (NewtypeErgonomics, InterfaceErgonomics, WireContract,
WireExchangeCodec, WireExchangeEnvelope, TraceSupport) is a whole-Ethos
generator that builds impl blocks, method bodies, match arms, const modules,
and type aliases in hardcoded Rust.

The long path is to express each generation class as authored transformer data using
the same escape algebra (extended as needed). What this requires:

1. **Expression-level templates.** The current `ResultTemplate` produces items
   (newtypes, structs, enumerations) and attribute vectors. Generation classes
   produce impl blocks, functions, match expressions, and statement bodies.
   The template vocabulary would grow: `ImplBlockTemplate`,
   `FunctionTemplate`, `MatchTemplate`, `ExpressionTemplate`. Each is a quoted
   Logos skeleton with escapes, exactly like the existing item templates, but
   covering the richer `EncodedItem` and `Expression` algebra.

2. **The Fold escape.** Generation classes that walk the newtype catalogue or
   variant tree to produce per-item impl blocks need the same tree-fold
   construct proposed for ScopeOf.

3. **Richer meta-types.** The current `MetaType` vocabulary (Name, Type, Fields,
   Variants) covers declarations. Generation classes read the whole Ethos
   structure: the newtype catalogue, the interface roots, the declaration
   roles. New meta-types would be needed: `NewtypeCatalogue`, `InterfaceRoots`,
   `DeclarationRoles`.

This is growth within a coherent architecture, not a redesign. Each generation
class can be migrated independently: author its template in `.nomos`, prove
equivalence against the hardcoded output, then retire the Rust generator. The
escapes, meta-types, and template kinds grow variant-by-variant, each a compile
error until handled — the existing discipline.

This question — whether generation-surface growth belongs in this design's
scope or stays deferred — is carried forward as Decision 3 in section 9, not
repeated here.

## 8. Where Nomos Lives — Settled Law

This was presented in the 2026-07-29 draft of this document as an open
decision ("Decision 1"). The psyche ruled the presentation itself wrong: this
was never open — his design existed and had been lost from the design
surface. `RecoveredNomosVision-2026-07-29.md` restores the firsthand quote
chain; it controls over this section.

**[ruled]** Nomos is its own language with its own files, its own syntax, its
own EncodedForm, its own nametable and structural table, loaded through the
same protos TextualForm mechanism that Ethos and Logos use. The chain, in the
psyche's own words:

2026-07-11 (session 0fd2d07c line 402):

> actually, we should keep nomos, because it is its own language syntax.
> logos is a rust-equivalent, but our macros will not be rust macros

2026-07-17 (session 29d00eb1 line 108, the founding TextualForm/EncodedForm
vision):

> that means a major part of the vision was lost, or ignored. I had a great
> vision for a shared abstraction around textualform and encodedform (use to
> be called true/core) ... a nametree and a structuretree ... textualform
> trait writes and reads the name and structure trees ... this drives all
> textual en/decoding, including rust ... actually, the vision even allowed
> multiple textualforms per encodedform; logos -> logos or logos -> rust ...
> even nota can take this architecture; it would be the basic/most-universal
> example.

2026-07-29 (PsycheVisionReacquisition entry 4, the triple-language dictation,
the newest and controlling anchor):

> We have three languages, ethos, nomos, and logos. And all three use the
> same mechanism to load to and from textual form into encoded form. They
> have their own syntax. Well, they look very similar. They're all protos
> family languages, like NOTA is actually, you could say, the fourth language
> in the foundation. [...] Nomos is there to create the sugar syntax, the
> beautiful syntax of ethos, and logos is there to give us a true
> representation of essentially our assembly language [...] the entire reason
> why we have nomos is so that we can modify the transformation using the
> nomos language. So if the nomos language was never implemented, then the
> entire engine is currently a failure because the whole point of creating
> nomos was to be able to modify.

Own files, not declarations riding inside `.ethos` files, and not a hybrid
where only sugar-level `ScopeOf` markers live in Ethos: Nomos is a full
sibling authored surface. The `ScopeOf` running example in section 3.9 above
is still correct under this ruling — the Ethos declaration is sugar that
names a transform; the transform itself is authored in Nomos's own files —
it was never the "hybrid" alternative this document previously offered as one
option among several; it is the only ruled shape.

**Matter, not psyche-ruled:** the `.nomos` extension itself. "Own files" is
ruled; which literal extension names those files is an agent convention, no
different from any other file-naming choice, and is not recorded as a psyche
ruling anywhere in the recovered chain. This document continues to use
`.nomos` as the working convention.

## 9. Decision Points for the Psyche

The recovery sweep settled where Nomos lives (section 8), recursive transformer
invocation as a requirement (section 3.9), and Nomos's participation as a
Capsule/ShortIdentifier implementer alongside its siblings (section 4.2, step
5). What remains genuinely open is narrower than this document previously
presented. The ScopeOf identity question is tracked separately and is not
repeated here (see `ScopeOfIdentityBriefing-2026-07-29.md`); it is pending with
the psyche independent of this design.

**Decision 1: the recursion construct's mechanics.**

Recursive transformer invocation is ruled required ("We also need to be able to
call more macros recursively." — 2026-07-13, session 0fd2d07c line 572). What
is open is the mechanism, not the requirement. `Invoke` (call a named transformer by
identity) already satisfies simple recursion. Whether tree-shaped recursion
(ScopeOf's walk over a variable-depth Domain tree, binding fresh parameters at
each level) needs a distinct construct is not settled:

- **(a) A fourth escape variant** (`Escape::Fold`) in the closed algebra,
  proposed in section 3.9/5.2 below and marked as proposal throughout. The
  algebra's own documentation says "a fourth escape would be a new variant and
  a compile error until handled" — this is exactly that growth path.
- **(b) A separate mechanism** outside the escape algebra — e.g. a
  `TransformationKind::TreeFold` that wraps a template but is not itself an
  escape. This keeps the escape set at the ruled three members at the cost of
  a second dispatch mechanism.
- **(c) Deferred** until ScopeOf implementation reaches the point where the
  exact recursion shape is concrete enough to design against real data.

The honest tension: the psyche ruled the escape set closed at two primitives
plus Invoke. Fold (proposal, not ruled) is a genuine new primitive under
option (a). The alternative (b) avoids growing the escape set but adds a
parallel mechanism. The psyche's call.

**Decision 2: ScopeOf as a transformer vs. a built-in.**

Should ScopeOf expansion be:

- **(a) A transformer authored in `.nomos`**, dispatched through a new
  `SectionDefault::ScopeOf` variant. This keeps ScopeOf within the transformer
  system; the engine treats it as another structural default.
- **(b) A built-in transformer** the engine recognizes from the `ScopeOf`
  keyword, with hardcoded expansion logic. This is simpler for the first
  implementation but makes ScopeOf a special case rather than an instance of
  the general mechanism.

The honest case for (b): ScopeOf's tree recursion, All-variant injection,
conversion generation, and containment operations are complex enough that
expressing them as template data may require so many escape-algebra extensions
that the template is harder to understand than the direct logic.

**Decision 3: generation surface scope and migration ordering.**

Should this design cover:

- **(a) Only the authoring surface** (TextualNomos for
  MacroDefinition/ResultTemplate), leaving the enriched generation classes as
  hardcoded Rust until they are individually migrated.
- **(b) The authoring surface plus the generation vocabulary growth path** (new
  template kinds for impl blocks, functions, expressions), designed now even if
  not implemented immediately.

Separately open: the order in which `SliceOneTransformation` (section 6) and
the fixture-constructed packages retire once the authored surface proves
equivalence, and whether any generation class migrates before the base-door
TextualNomos syntax (section 3) is itself proven against production fixtures.

**Decision 4: the second-textualform (sigil) details.**

The two-textualform shape is ruled (section 3.0): a plain-NOTA base door
first, a sigil-rich `$`/`<<>>` form second, over the same EncodedForm. What is
open is the second form's concrete spelling, since it does not yet exist as
machinery (section 3.11 below lays out honestly what building it requires):

- Whether Realize/Splice/Invoke get sigils at all, or whether the sigil form's
  value is elsewhere (e.g. compact template literals) with escapes staying
  structural even in the second form.
- If sigils are wanted: `$x` / `$@xs` / `@transformer`, or `$x` / `$@xs` / `$!transformer`,
  or `$x` / `$@xs` / `$(transformer)` — several spellings are equally plausible and
  none is ruled.
- Which layer builds it — a new trigger/character-class in raw-discovery, or a
  structural-codec-level convention over ordinary bare atoms (section 3.11) —
  is itself part of what is open, not a settled implementation detail.

## 10. Observations from the Sources

**The existing machinery is more complete than expected.** The production daemon
path already runs transformers-as-data through `MacroPackage::apply_enriched`.
The missing piece is purely the authoring surface: how a human writes a
`.nomos` file and how that file becomes a `MacroPackage`. The engine, the
template algebra, the content identity, the NameTable composition, the typed
evaluation — all of this is live.

**Correction: the NomosExtended profile is narrower than earlier drafts
claimed.** raw-discovery does carry a `GlyphSet::NomosExtended` variant
(profile.rs lines 40-49), and it is real, deliberate machinery — but it is not
"pre-provisioned for" a sigil escape syntax, as an earlier draft of this
document claimed. It differs from `Standard` by exactly one thing: removing
`$` from the forbidden-bare-characters set (profile.rs lines 430-434). `$` is
not a trigger anywhere in the seven-trigger table; it has no capture
semantics; a `$`-led atom is an ordinary bare atom with no special reading by
anything in the codebase today. The crate's own documentation calls
`GlyphSet`/`RawProfile` "compatibility selectors" (raw-discovery lib.rs line
34), not an escape-syntax feature. Section 3.11 states plainly what building a
real sigil form on top of this would require.

**The enriched generation surface is the real hard problem.** The structural
defaults (newtype, struct, enumeration lowering) are straightforward to express
as authored templates — the running examples above demonstrate this directly.
The generation classes (1,890 lines of hardcoded logic producing impl blocks,
method bodies, match arms, codec implementations) are the frontier. They require
template vocabulary growth, richer meta-types, and possibly the Fold escape.
This is where the "transformers are data" vision meets its most demanding test.

**Correction (2026-07-29): the claim of no prior design was false.** This
document originally stated that no partial authored-Nomos design existed in
the design surface and that this proposal was the first concrete design. The
psyche rejected that presentation when "where Nomos lives" was shown to him as
an open decision: his design existed and had been lost, not absent. A recovery
sweep located it — in `primary/reports/logos/nomos-macro-model-v1.md`,
`textual-form-vision-design-v1.md` and `-v2.md`, `up-close-design-v1.md`, and
in session transcripts spanning 2026-07-11 through 2026-07-22 — and restored it
to `RecoveredNomosVision-2026-07-29.md` in this design tree, which is now
controlling over this document wherever the two conflict. This document has
been corrected against that restoration; see section 3 and section 8 above for
the corrected settled/open split.

**Terminology alignment (ruled, corrected).** This document previously treated
"transformer" as this design's own preferred framing alongside the crate's
"macro." That undersold it: the psyche ruled the term directly (Entry 5,
quoted in section 1 above) — "macro" is retired from prose because it is
overloaded toward string transformation, and the unit is a type
transformation, named transformer. The crate calls its rules "macros"
throughout (`MacroDefinition`, `MacroPackage`, `MacroIdentity`, `MacroKind`);
these identifiers predate the ruling and remain accurate as code literals —
renaming the types is implementation matter, not addressed by this document.

**Long-term vision (psyche, marked explicitly long-term, Entry 5).** The
psyche framed Nomos's eventual scope beyond anything this document designs:

> we might make Nomos, or we will eventually make Nomos the most load-bearing
> part that could do all of the correctness verification or more than what
> the Rust compiler actually does today. So it has to become an extremely
> capable and extendable system. [...] we could have logos actually compile
> into assembly language through LLVM.

This is long-term direction, not a near-term design constraint: Nomos
eventually verifying correctness at or beyond rustc's level, with Logos
compiling to assembly through LLVM. The psyche paired this with an explicit
acknowledgment that the difficulty was underestimated and that he does not
yet have the answers — rulings will continue incrementally as vertical slices
reveal how the system actually behaves, and agents are invited to research
prior art on typed, placeholder-driven program transformation. Nothing in
sections 1-9 of this document should be read as resolving this long-term
scope; it orients direction, not this document's v1 decisions.
