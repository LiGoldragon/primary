---
title: The Schema Language and How It Lowers — and Audit Criterion 1 (no own parser)
role: operator
variant: Psyche
date: 2026-06-06
topics: [schema-next, nota-next, structural-macro-node, schema-lowering, asschema-removal, audit]
description: |
  Plain-English walk-through of the authored .schema language as it actually
  exists in schema-next today, traced against four worked examples from
  spirit/schema (signal, nexus, sema). Covers: (1) the authored declaration
  surface and how enum-decl vs macro-application is disambiguated; (2) why a
  .schema file IS full NOTA and where the deserialize path calls into
  nota-next's parser and StructuralMacroNode codec (file:line); (3) the
  position-aware schema macros — what they are, where they live, what they
  expand; (4) the real current state of the Asschema removal (the type is
  gone; an Assembled* template-expansion family remains, which is a different
  thing). Closes with AUDIT CRITERION 1: schema-next implements NO parser of
  its own — verdict COMPLIANT, with the grep terms and file:line evidence that
  make the verdict falsifiable. Also flags two as-intended-vs-as-implemented
  divergences the psyche should know about: the n2z3 at-binder surface
  (Name@{...}) is NOT implemented anywhere, and xai7's #[derive(StructuralMacroNode)]
  is hand-written by-hand for the one node that uses it.
---

# The schema language and how it lowers

This report answers four questions about `schema-next` and closes Audit
Criterion 1. Everything below is read from the source on disk at
`/git/github.com/LiGoldragon/schema-next` (branch `HEAD`, src dated
2026-06-05) and the worked schemas at
`/git/github.com/LiGoldragon/spirit/schema/`. Where the fresh psyche intent
and the code disagree, that is called out explicitly with a line cite —
that is the most valuable part of this report.

## The one-paragraph answer

A `.schema` file is plain NOTA — three or four top-level objects, no schema
keywords. `schema-next` hands the raw text to `nota-next`'s parser, gets back
a tree of `Block` values, and then reads that tree by **position** (object 0
is imports-or-input, object 1 is input-or-output, etc.) and by **structural
shape** (a brace is a struct, a square bracket is an enum body, a bare atom is
an alias). It owns none of the character-level work: the tokenizer, the
delimiter matcher, and the structural pattern-matcher all live in `nota-next`.
The output is a typed Rust value (`Schema`) that is rkyv-serializable. This
repo deliberately stops there — it does **not** emit Rust source. That job
belongs to the separate `schema-rust-next` repo, which is present as a sibling
checkout. So the schema-next `INTENT.md` line "It does not emit Rust source
code" is accurate *for this repo*, and the Maximum-certainty intent jypw
("every schema must produce Rust") is satisfied one repo downstream — no
contradiction, once the boundary is named.

## 1. The authored schema language as it actually exists

### What a real .schema file looks like

Here is the head of the real signal contract, verbatim
(`/git/github.com/LiGoldragon/spirit/schema/signal.schema:1`):

```nota
{}
[State Record Observe Lookup Count Remove ChangeCertainty LookupStash (SubscribeIntent SubscribeIntent opens IntentEventStream)]
[RecordAccepted RecordsObserved RecordsStashed RecordFound RecordsCounted RecordRemoved CertaintyChanged SubscriptionStarted (Event IntentEvent) Error Rejected]
{
  SourcePath String
  ...
  Entry { Topics * Kind * Description * Magnitude * Privacy * }
  Kind [Decision Principle Correction Clarification Constraint]
  Magnitude [Zero Minimum VeryLow Low Medium High VeryHigh Maximum]
}
```

Read it by **position**, top to bottom — there are no field labels in the
root:

1. `{}` — the imports map. Here empty (signal imports nothing). When present
   it carries `Local crate:module:Type` pairs, as in `nexus.schema:1`
   (`SignalInput spirit:signal:Input`).
2. `[...]` — the **Input** root enum body. Each object in the bracket is one
   variant: a bare PascalCase atom (`State`, `Record`) is a unit/header
   variant whose payload is looked up in the namespace by the same name; a
   parenthesized `(SubscribeIntent SubscribeIntent opens IntentEventStream)`
   is a data-carrying variant that *also* attaches stream lifecycle metadata.
3. `[...]` — the **Output** root enum body, same shape.
4. `{ ... }` — the **namespace** map of `TypeName Value` pairs.

Inside the namespace, the value's NOTA delimiter decides the declaration kind
(this is the load-bearing structural rule):

- `Topic String` — bare reference value → **alias** declaration.
- `Entry { Topics * Kind * ... }` — brace value → **struct** declaration
  (and a one-field brace collapses to a **newtype** — see below).
- `Kind [Decision Principle ...]` — square-bracket value → **enum**
  declaration.
- `Topics (Vec Topic)` — parenthesized value with a known operator head →
  composite **type reference**.

The `*` marker means "derive the field name from the type name": `Topics *`
lowers to a field `topics: Topics`. The `Entry { Topic * }` one-field form
lowers to a `Newtype`, not a one-field struct (ARCHITECTURE.md:185-190 and
`source.rs:731-735`).

The same three-or-four-object root shape is used for all three planes:
`signal.schema`, `nexus.schema`, and `sema.schema` are structurally identical;
the runtime meaning differs only after lowering (ARCHITECTURE.md:379-382).
`nexus.schema:19-20` shows the triad-engine vocabulary carried as ordinary
schema data — the Input enum is `[SignalArrived SemaWriteCompleted
SemaReadCompleted EffectCompleted]` (the four `NexusWork` cases) and the
Output enum is `[CommandSemaWrite CommandSemaRead ReplyToSignal CommandEffect
Continue]` (the five `NexusAction` cases from intent records hyng/7ca4/rpr5).

### DIVERGENCE 1 — the n2z3 at-binder surface is not implemented

Intent record **n2z3 (Decision)** settled the authored declaration surface on
the **at-binder form**: `Name@{...}` for a struct, `Name@(...)` for an enum,
`name@Type` for a field/member binder, with the root being the implicit
filename-named struct. **That form exists nowhere in the codebase.** A search
for `@{` across every real schema and every schema-next fixture returns
nothing:

```
grep -rn "@{" spirit/schema/ schema-next/schemas/ schema-next/examples/ schema-next/tests/
  → (no matches)
```

What is implemented instead is the **brace/bracket positional form** shown
above, where `{}` is a key/value map and `[]` is a vector, and the
declaration kind comes from the delimiter, not from an `@` binder. The
strongest evidence the at-binder is not even partially wired: `@` is treated
as an *invalid* character in a variant name —
`source.rs:1260` rejects any name containing `'@'`
(`!self.0.contains('@')`). So today the `@` form would be rejected, not
parsed. This is the single largest "as intended vs as implemented" gap in the
schema language: n2z3 is a Decision-level statement of the target surface, and
the surface is pre-n2z3. The exhq half (inline PascalCase field types register
in the local namespace) *is* implemented — `source.rs:809-822` and
`schema.rs:1021-1052` create a private module-local declaration and derive the
field name from the type name — but it is reached through the brace form
(`Entry { Receipt { recordIdentifier RecordIdentifier } }`), not the
`name@Type` binder.

### How enum-decl vs macro-application is disambiguated (mha3/fo38)

mha3/fo38 (Correction) say enum-declaration and macro-application share the
*identical* surface shape — a head plus one parenthesized group — and a head
discriminator (a sigil, or a known-operator vocabulary) tells them apart.
schema-next disambiguates by **known-operator vocabulary**, not by sigil. At a
type-reference position, a parenthesized `(Head Body)` is matched against a
fixed built-in operator set; anything else falls through to the user macro
registry (`schema.rs:1066-1097`):

```rust
fn from_parenthesis_objects(...) -> Result<Self, SchemaError> {
    if objects.len() == 2 {
        if let Some(head) = objects[0].demote_to_string() {
            match head {
                "Vec" | "Vector"   => return Ok(Self::Vector(...)),
                "Optional" | "Option" => return Ok(Self::Optional(...)),
                "Map" | "KeyValue" => return Self::from_grouped_map_payload(...),
                _ => {}                       // not a known operator …
            }
        }
    }
    Self::from_macro_invocation(block, registry, context)   // … so it's a macro call
}
```

`Vec`/`Vector`, `Optional`/`Option`, `Map`/`KeyValue` are the known
type-reference operators; an unknown head is dispatched to the macro registry
(which only accepts it if the node definition `accepts_tagged_invocation()`,
`schema.rs:1143`). A sigil discriminator is *available* — `SigilSpec` and
`SigilPosition` are re-exported from nota-next at `lib.rs:26` — but schema-next
does not use a sigil; the vocabulary path is the one in force. This matches the
"known-operator vocabulary" branch of fo38, not the "sigil" branch.

## 2. A .schema file IS full NOTA — the deserialize path (vez8)

vez8 (Maximum) states a `.schema` file is full NOTA and deserializes via the
structural-macro-node codec into schema-in-Rust. The code bears this out.
There are **two entry surfaces**, and both begin with the same nota-next parse
call:

- `SchemaSource::from_schema_text` (`source.rs:28-31`) → `Document::parse` →
  `from_document`. This is the typed-source-language path (the
  archive/round-trip surface).
- `SchemaEngine::lower_source` (`engine.rs:290-297`) → `Document::parse` →
  `lower_document`. This is the macro-registry path that produces semantic
  `Schema` directly.

Both call the same thing. Every `Document::parse` in the crate (6 call sites:
`raw.rs:16`, `engine.rs:295,324,425`, `source.rs:29`, `declarative.rs:44`) is
`nota_next::Document::parse` — the real NOTA parser:

```rust
// nota-next/src/parser.rs:23
pub fn parse(source: impl Into<String>) -> Result<Self, NotaError> {
    let source = source.into();
    let mut parser = Parser::new(&source);
    let root_objects = parser.parse_document()?;
    Ok(Self { source, root_objects })
}
```

That `nota-next` `parser.rs` is where the 51 character-level scanning sites
live (it owns `.chars()`, `char_indices`, cursor/peek logic). schema-next holds
**zero** of that machinery.

### The structural-macro-node codec call site

The "structural-macro-node codec" of vez8/xai7 is the `StructuralMacroNode`
trait, defined in `nota-next/src/macros.rs:1267`. schema-next consumes it for
enum-variant decoding. The one production `impl` is
`source.rs:1097` (`impl StructuralMacroNode for SourceVariantSignature`), and
its `from_structural_candidate` (`source.rs:1113-1172`) does exactly the
type-directed, declaration-order, first-match-wins decode xai7 describes:

```rust
// source.rs:1116-1123
let variants =
    StructuralVariantSet::new(Self::structural_position(), Self::structural_variants())
        .map_err(StructuralMacroError::Dispatch)?;
let matched = variants
    .dispatch(&candidate)
    .map_err(StructuralMacroError::Dispatch)?;
match matched.macro_name() {
    "unit variant"   => ...,
    "data variant"   => ...,
    "opens variant"  => ...,
    "belongs variant"=> ...,
```

The `dispatch` it calls is nota-next's, and that is where "declaration order,
first match wins" actually happens
(`nota-next/src/macros.rs:476-482`):

```rust
for variant in self.variants() {        // declaration order
    ...
    if let Some(matched) = variant.matches(candidate.blocks()) {
        return Ok(matched);              // first match wins
    }
}
```

So the codec is type-directed (the enum's variant list IS the spec), bidirectional
(`to_structural_nota`, `source.rs:1174`), and lives at the NOTA layer — exactly
z544/xai7. schema-next contributes only the variant *shapes*
(`MacroNodeDefinition::enum_variants`, `macros.rs:432-509`) and the
per-variant decode arms.

### DIVERGENCE 2 — xai7's #[derive(StructuralMacroNode)] is hand-written

xai7 (VeryHigh) says the structural macro node is "realized as
`#[derive(StructuralMacroNode)]` with per-variant shape attributes." The
derive macro **exists** (nota-next re-exports it: `nota_next::StructuralMacroNode`
proc-macro, nota-next `lib.rs:28`), but schema-next does **not** use it. The one
node that needs it, `SourceVariantSignature`, hand-writes the whole trait impl
(`source.rs:1097-1177`) including a hand-built `StructuralVariantSet` and a
string-keyed `match matched.macro_name()` dispatch. That string-name match
(`"unit variant"`, `"data variant"`, …) is precisely the
"string-variant-name dispatch" xai7 says the design is NOT. So the *mechanism*
(type-directed structural dispatch in declaration order) is honored, but the
*realization* (derive + per-variant attributes, no string names) is not yet
adopted for this node. This is mid-migration, not a contradiction of the
mechanism — but the psyche should know the derive is unused in schema-next.

## 3. The position-aware schema macros

These are the heart of the "position-aware schema macro engine" that
`active-repositories.md` names. They live in `src/macros.rs` and `src/engine.rs`.

**What they are.** A schema macro is a `SchemaMacroHandler` (trait at
`macros.rs:130-142`) bound to a `MacroPosition` (enum at `macros.rs:25-34`:
`RootImports`, `RootInput`, `RootOutput`, `RootNamespace`,
`NamespaceDeclaration`, `StructFields`, `EnumVariants`, `TypeReference`). The
position says *where in the schema tree* the object sits; the handler says
*how to read it there*. The registry (`MacroRegistry`, `macros.rs:234`) holds
both the handlers and the `MacroNodeDefinition` structural cases.

**Where they expand.** `SchemaEngine::lower_document_with_resolver`
(`engine.rs:352-416`) drives them by position: object at the imports index is
lowered at `RootImports` (`engine.rs:429-445`), the input/output brackets at
`RootInput`/`RootOutput` (`engine.rs:447-463`), the namespace brace at
`RootNamespace` (`engine.rs:465-481`). Each handler then recurses: the
namespace handler walks `TypeName Value` pairs and lowers each at
`NamespaceDeclaration` (`engine.rs:775-796`), a struct body lowers each pair at
`StructFields`, an enum body lowers each object at `EnumVariants`, and every
reference position lowers at `TypeReference`.

**What they expand into.** A `MacroOutput` (`macros.rs:221-232`):
`Imports`, `RootEnum`, `Types`, `Type`, `Fields`, `Variants`, `Reference` —
the typed semantic-schema fragments. The default registry wiring is
`MacroRegistry::with_schema_defaults` (`engine.rs:485-509`): it registers the
eight node definitions and five concrete handlers.

**The y1n5 NotaBody-with-outer-delimiter-stripped contract.** y1n5 (Decision)
says macro handlers receive `NotaBody` body streams with the outer delimiter
stripped. This is implemented: handlers call `object.delimited_body(...)`
(`macros.rs:92-101`) or `NotaBody::from_delimited(block, delimiter, expected)`
which returns the inner `root_objects()` with the surrounding `{ }`/`[ ]`/`( )`
already removed. Concrete sites: `engine.rs:699` (imports body),
`engine.rs:750` (namespace body), `engine.rs:950` (root enum body),
`source.rs:239,352,694,910` (source-codec bodies). The matcher itself
delegates to nota-next: `MacroNodeDefinition::matches` (`macros.rs:563-567`)
builds a `NotaMacroRegistry::unchecked(...)` and calls `.dispatch(...)`,
so the structural pattern-matching, named captures, and no-match diagnostics
are all nota-next's (ARCHITECTURE.md:11-15 and 277-310).

## 4. The Asschema removal — real current state (vez8/fc7l/av1q)

**The `Asschema` type is gone.** A search for `asschema` across src/tests/docs
returns exactly one hit, and it is a *test name asserting the absence*:

```
tests/operator_271_closed_claims.rs:286
  fn schema_source_and_semantic_schema_round_trip_without_asschema_artifacts()
```

ARCHITECTURE.md:119-130 and INTENT.md:66-73 both confirm the deletion: no
`Schema::to_nota`, no `.asschema` / `.asschema.rkyv` artifact owner, no
redb-backed schema store. The current endpoint is the semantic `Schema` value,
rkyv-serialized via `Schema::to_binary_bytes` / `from_binary_bytes`
(ARCHITECTURE.md:124). So **schema-next does deserialize toward a typed
schema-in-Rust value, not an assembled text IR** — vez8's target pipeline.

### The stale-doc question — active-repositories says "emits ordered macro-free Asschema"

That phrasing in `protocols/active-repositories.md` **is stale.** schema-next
no longer produces an Asschema or any macro-free assembled IR text artifact.
The repo's own `INTENT.md:66` ("*Asschema is removed.*") and
`ARCHITECTURE.md:119` ("it is not an Asschema compatibility projection") are
the current truth. The active-repositories line should be updated to
"deserializes NOTA into semantic schema-in-Rust (rkyv), no Asschema."

### Leftover surface vez8/fc7l would still want cleaned

There is **no `Asschema` leftover**, but there is a separate `Assembled*`
family in `src/declarative.rs` that an auditor should not mistake for Asschema:
`AssembledTemplate`, `AssembledType`, `AssembledFields`, `AssembledVariants`,
`AssembledStructBody`, `AssembledReference` (declarative.rs:1374-1605, plus
`AssembledStructBody`/`AssembledVariants` used from engine.rs:595,605,966 and
schema.rs:1027,1048). These are the **user-defined declarative-macro
template-expansion** machinery — the layer that expands a macro template into
an owned object tree before lowering (ARCHITECTURE.md:218-229). They are NOT
the old assemble/Asschema resolution step (inline-decl hoisting, visibility,
ordering) that vez8 says became methods on schema-in-Rust; that resolution now
lives as methods on the source/semantic types (`source.rs:124-146`,
`SourceLoweredNamespace` at `source.rs:1434-1492`, visibility on `Declaration`).
The naming collision is a readability hazard worth a rename, but it is not a
correctness violation and not a surviving Asschema.

One genuinely transitional seam: `SchemaSource` keeps a string projection
codec (`to_schema_text`, `source.rs:96-104`, and the `format!`-based
`*::to_schema_text` methods throughout source.rs). This is the authored-source
*text round-trip* boundary (`SchemaSourceArtifact`), explicitly described as a
canonical projection (ARCHITECTURE.md:38-48), not byte-identical preservation.
It is not Rust emission and not Asschema; it is the `.schema` text writer. It
is consistent with fz9n's "canonical round-trip, not byte-identical."

## Audit Criterion 1 — schema-next implements NO parser of its own

**VERDICT: COMPLIANT.** All structural reading rides nota-next interfaces.

### What I searched for (so the verdict is falsifiable)

```
grep -rniE "\.chars\(\)|\.bytes\(\)|tokeniz|lexer|char_indices|peekable|fn parse|scan"  src/
grep -rniE "split_whitespace|\.split\(|strip_prefix|strip_suffix|find\('|starts_with"    src/
grep -rn  "Document::parse"                                                              src/
grep -rn  "NotaBody|from_delimited"                                                       src/
```

### What I found, and why each non-NOTA-parser hit is benign

- **Parsing is delegated.** Every one of the 6 `Document::parse` call sites is
  `nota_next::Document::parse` (`raw.rs:16`, `engine.rs:295,324,425`,
  `source.rs:29`, `declarative.rs:44`). The char-level scanner (51 sites) is in
  `nota-next/src/parser.rs`, not in schema-next.
- **All `.chars()` hits operate on already-parsed atom strings**, never on raw
  NOTA source: `raw.rs:285` (file-stem → PascalCase root name),
  `source.rs:1257` (`SourceVariantName::is_valid` — first-char-uppercase check),
  `source.rs:1569` (`SourceIdentifierCase::is_type`), `schema.rs:39`
  (symbol-path validation over an already-extracted `Name`),
  `syntax.rs:252`, and `declarative.rs:1193,1631,1643,1760,1773` (identifier
  case/validity checks on captured atoms). None of these read delimiters or
  tokenize text.
- **`starts_with('$')` at `declarative.rs:854`** is `CaptureName::from_token` —
  it classifies a macro-template capture token (`$name` / `$*name`) that is
  already a parsed atom in the macro template language. It is not scanning NOTA.
- **`strip_suffix(".schema")` / `strip_prefix` at `module.rs:126,149`** are
  filesystem path-to-module-name mapping, not NOTA reading.
- **`split(':')` at `schema.rs:27`** splits an already-parsed `Name` into
  colon-qualified symbol-path segments (`crate:module:Type`). Not NOTA parsing.
- **Structural reading rides nota-next.** Delimiter discrimination is a `match`
  on `nota_next::Block` / `nota_next::Delimiter` enum variants
  (`raw.rs:91-122`, `source.rs:455-481`, `schema.rs:982-1018`,
  `engine.rs:573-585`) — schema-next never re-implements bracket matching, it
  reads the already-built tree. Body extraction is `NotaBody::from_delimited`
  (12 sites in engine.rs + source.rs + macros.rs). Pattern matching for the
  position-aware cases is `nota_next::MacroRegistry`/`StructuralVariantSet`
  `.dispatch` (`macros.rs:564`, `source.rs:1120`).
- **Cargo.toml** lists exactly one functional dependency, `nota-next` (plus
  `rkyv`). There is no `nom`, `pest`, `logos`, `chumsky`, or any parser-combinator
  / lexer-generator crate.

### Where the verdict could be challenged, and why it still holds

The honest edge case is `RawNotaDatatype::from_block` (`raw.rs:90-123`) and
`SourceReference::from_record` (`source.rs:1305-1327`): these re-classify an
*already-parsed* `Block` tree into schema-shaped enums and read a head atom
like `"Vec"`/`"Map"`. That is **semantic interpretation of nota-next's parsed
structures**, not parsing — it never touches source text, never tokenizes,
never matches a delimiter character. ARCHITECTURE.md:434 states the design
intent for exactly this: "Lowering is pure semantics over nota-next's
already-parsed blocks — not a hand-rolled text parser." The code matches that
claim. So Criterion 1 is **PASS / COMPLIANT**, with the one caveat that the
`StructuralMacroNode` *derive* is not yet adopted (Divergence 2) — that is a
codec-realization gap, not a private-parser violation.
