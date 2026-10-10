# Logos → Rust lowering v1 — Rust as a form of data, projection as object-method

The structural, object-method design of the Logos → Rust lowering. The psyche's
directive: model Rust **correctly as a form of data** (to the extent the Logos
view needs it — Logos is the Rust-equivalent data language, 1-to-1 with Rust),
and express the lowering as **methods on the data-bearing CoreLogos types** (the
verb-belongs-to-noun rule), never as a free-function emitter walking a foreign
tree.

Written 2026-07-14, session `nextgen-recrystallization`, lane
`logos-rust-lowering`, generalist, Opus 4.8 (1M). Read-only on all code
repositories; the single artifact this lane writes is this file.

Provenance discipline, matching the sibling reports:

- **[observed — cite]** — a worker-verified fact about current code, cited to a
  file path (this session's schema-rust sweep) or to a sibling report's own
  citation.
- **[ruling — cite]** — a settled psyche decision, cited to `design-v0.md` or the
  session brief.
- **[interpretation]** — my reading; not the psyche's words.
- **[AGENT PROPOSAL]** — a recommendation on an open question, collected in §7.

## 0. Thesis in one paragraph

Rust, as far as Logos needs to see it, is **not a token stream to assemble** — it
is a small, closed algebra of data: items carrying visibility, attribute vectors,
and bodies; bodies made of fields, variants, types, and paths. CoreLogos already
*is* that algebra, 1-to-1 and stringless. So the lowering is not a compiler pass
that *infers* Rust shape by walking the schema tree; it is a **transcription**: a
CoreLogos value emits the Rust it already is. Under the verb-belongs-to-noun rule
that transcription is **one uniform trait, `ProjectRust`, implemented on every
CoreLogos node kind** — each item, attribute, field, type, and path node knows
how to project itself, and composes its children. Totality is mechanical: the
trait bound at every composition point and exhaustive matching on the closed item
enum make a non-projecting node a compile error. Stringlessness meets projection
at exactly one contact point — the identifier-bearing leaves take a read-only
`NameResolver` over the NameTable and realize a name at the last moment. Nothing
else is synthesized except the four ruled translations (dotted→`::`, delimiter
re-sugaring, stored-identifier realization, and prettyplease formatting). The
existing byte-exact schema-rust goldens gate the whole thing. And because the
transcription is 1-to-1, the edge is a **codec, not a one-way emitter** (§6, the
psyche's mid-flight extension): the same per-node structural description runs both
directions, so the goldens become a two-way harness — decode each into CoreLogos,
re-encode, require byte-exact — needing no hand-authored logos fixtures and giving
the mechanical migration path for harvesting the existing Rust corpus.

## 1. Rust-as-data — the Logos view (deliverable 1)

### 1.1 The correct ontology: Rust is a closed algebra of items over a shared leaf vocabulary

**[interpretation]** The Logos view of Rust needs exactly the construct set the
oracle exercises — no more (`codex-rust-construct-survey.md §1,§4`: `unsafe`,
`macro_rules!`, `union` are counted-zero exclusions; the emitted surface is
newtypes, named-field structs, unit/tuple-payload enums, generic
structs/enums, trait defs, impl blocks, `From`/constructor methods, and a
`Display`/`Error` pair). Modeled as data, that surface is a **two-layer algebra**:

- **Items** (the top layer, a closed enum `CoreItem`): `Newtype`, `Struct`,
  `Enumeration`, `Alias`, `TraitDefinition`, `ImplBlock`, `FreeMethod` (the
  constructor/factory functions). Each item is a record of *modifiers* + *body*.
- **Leaves** (the shared lower vocabulary, reused across items): `Visibility`,
  `Attribute` (a closed enum), `TypeReference`, `PathNode`, `Field`, `Variant`,
  `Generics`, `Identifier`. These are the same nodes wherever they appear — a
  `PathNode` in a derive is the same node type as a `PathNode` in a tool
  attribute or a type position.

The load-bearing correctness claim: **every token of Rust meaning is a data
node, and variance is a field or a variant on a general node — never a minted
specialized type.** [ruling — `design-v0.md §1.2 ruling 2`: "we dont want to
create a bunch of different struct types … we use a field or variants for
everything, like visibility."] So there is no `PublicStruct` vs `PrivateStruct`;
there is one `Struct` node with a `visibility: Visibility` field. This directly
supersedes the earlier "go crazy with the number of code structures" reading
(`design-v0.md §1.1`, itself marked superseded by §1.2).

### 1.2 Visibility is a modifier node, and its private case projects to nothing

**[ruling — `design-v0.md §1.2 ruling 4`; syntax audit §2.0, proposal (f)]**
Visibility is a general modifier applied by dotting it onto whatever it governs:
`Public.Newtype.{…}` parses right-associatively as `App(Public, Newtype.{…})`,
and the *same* `Public` applies to a field in `Public.CommitSequence`. In the
**text surface** this is right-associative application; in **CoreLogos-as-data**
it is a `visibility: Visibility` field on the item and on the field
(`Visibility ::= Public | Crate | Module(PathNode) | Private`).

In CoreLogos-as-data `Visibility ::= Public | Crate | Module(PathNode) | Private`,
projecting `pub ` / `pub(crate) ` / `pub(in <path>) ` / *(empty)* respectively.

**[interpretation]** The design-quality win: `Private` is a *value whose
projection is the empty token stream*, not an absent field handled by a side
branch. `Visibility::project` owns all cases including the empty one, so the item
body never asks "is there visibility?" — it always composes
`visibility.project(names)`, which is empty for `Private`. The special case
(no `pub`) dissolves into the normal case (a node that projects nothing).

**[observed — `schema-rust/src/lib.rs:1640-1645,1659-1691`]** A second
"materializes at projection" case: the current emitter **computes** visibility
rather than storing it. `visibility_tokens` maps logos `Public → pub` and logos
`Private → pub(crate)` (there is no bare-module-private path), and
`field_visibility_tokens` **downgrades** a `pub` field to `pub(crate)` at emission
when `references_private_type` finds the field's type is private. Under 1-to-1
CoreLogos the field carries its actual Rust visibility as data (so a `pub(crate)`
field stores `Crate`), and projection transcribes it — no reference-graph
computation at the projection edge. This is the same finding as the derives
(§1.3): decisions the current emitter *computes* become CoreLogos *data*.

### 1.3 Attributes are a plain ordered vector; "both derive groups" is just two entries

**[observed — `codex-rust-construct-survey.md §1`]** The oracle's dominant
attribute pattern is three attribute nodes in a fixed order on essentially every
data item: `#[rustfmt::skip]`, then a feature-gated
`#[cfg_attr(feature = "nota-text", derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode))]`,
then `#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]`
(236 plain-derive occurrences, 199 paired cfg_attr occurrences across the 9
goldens).

**[interpretation]** The two derive groups are **not** a special "there are two
derive groups" concept in the data. They are simply two entries in the item's
`attributes: Vec<Attribute>` — one `Attribute::Derive`, one
`Attribute::Configuration` wrapping a `Derive`. The `Attribute` enum's variants:

- `Derive(DeriveGroup)` where `DeriveGroup { paths: Vec<PathNode> }` →
  `#[derive(<paths joined by ", ">)]`.
- `Configuration(CfgAttr)` where `CfgAttr { predicate: CfgPredicate, inner: Box<Attribute> }`
  → `#[cfg_attr(<predicate>, <inner>)]`; the predicate here is
  `Feature(Identifier)` resolving `nota-text`.
- `ToolPath(PathNode)` → `#[<path>]`, covering `#[rustfmt::skip]` as a dotted
  path (`rustfmt.skip`), per syntax-audit proposal (h). This reuses `PathNode`;
  it is not an opaque string, because the oracle wants `rustfmt::skip` with `::`,
  which only a path produces.
- `HelperDerive(PathNode, DeriveGroup)` → `#[<path>(derive(<paths>))]`, covering
  the **third** attribute group the oracle emits: `#[rkyv(derive(PartialEq, Eq,
  PartialOrd, Ord))]`, a namespaced helper attribute that derives comparison
  traits on the generated `Archived*` type (observed:
  `schema-rust/src/lib.rs:1633-1637`; goldens `collections_generated.rs:76-93`,
  `imported-mail-consumer.generated.rs:37`).
- `Opaque(RawText)` — reserved strictly for genuinely opaque foreign attribute
  text; unused by the current oracle.

The order in the golden is the order in the vector. Projection iterates. That is
the whole of "both derive groups" (three, with the rkyv helper): **data in a
vector, transcribed in sequence.**

**[observed — the sharpest finding, `schema-rust/src/lib.rs:1596-1638`]** In the
current emitter the derive groups are **not data — they are computed at emission**
by `derive_attributes(includes_copy: bool, includes_ordering: bool)`, which
synthesizes the attribute set from two booleans plus a `NotaSurface` mode: the
NOTA cfg_attr is pushed only when the surface is `FeatureGated`; `Copy,` is
inserted only when `includes_copy`; `PartialOrd, Ord,` and the whole
`#[rkyv(derive(…))]` third group only when `includes_ordering`. This is exactly
the "materializes at projection" the 1-to-1 ruling forbids (session brief ruling
2; `design-v0.md §1.1`: "nothing materializes at projection"). Under CoreLogos the
derive set — including the conditional `Copy`/ordering derives and the rkyv helper
— is **stored as attribute-vector data and transcribed**, so `project` computes
nothing; the boolean-driven grouping logic disappears.

### 1.4 Paths are segment vectors; the dotted→:: translation lives in one method

**[ruling — `design-v0.md §1.2 ruling 7`]** "I dont want the double colon … logos
has to feel like logos." Rust paths are represented **dotted** in Logos
(`rustfmt.skip`, `rkyv.Archive`, `nota.NotaDecode`); the projection owns the
`.`→`::` translation. In CoreLogos-as-data a path is
`PathNode { segments: Vec<Identifier> }` (stringless — segments are NameTable
indices). `PathNode::project(names)` resolves each segment and joins with `::`.
**This is the single home of ruling 7's translation — nowhere else in the design
emits `::`.**

### 1.5 Generics lower by kind, and `<>` is materialized re-sugaring

**[ruling — `design-v0.md §6`: "Generics are defined by kind. Lowering dispatches
on kind, never on a string name."]** A generic application is
`TypeApplication { head: TypeReference, arguments: Vec<TypeReference> }`;
`project` emits `<head>` `<` `<args joined>` `>`. The angle brackets are
materialized at projection exactly like `::` — an allowed re-sugaring (§3),
carrying no meaning of their own. Dispatch is on the node's identity/kind, never a
string match. Generic *parameters* on a declaration
(`Plane<SignalRoot, NexusRoot, SemaRoot>`, `codex-survey §1`) are a `Generics`
node on the item, projecting the same way.

### 1.6 Finding — where the current design treats Rust as tokens to assemble, not data to transcribe

**[observed — this session's schema-rust sweep of `repos/schema-rust/src/lib.rs`]**
The current emitter is, honestly, already **two-stage and partly object-shaped**,
not a naive string builder: `TrueSchema` lowers through a `LowerToRust<RustModule>`
trait (`lib.rs:602-639`) into a **`RustModule` data value** (`lib.rs:334-345`),
which then renders to text via `RustModule::render` (`lib.rs:523-599`) driving a
`RustModuleRenderer` whose per-item emission is carried by **`ToTokens` impls on
many small owning token structs** — `RustDeclarationTokens`, `RustNewtypeTokens`
(`lib.rs:3885-3897`), `RustStructTokens` (`lib.rs:4261-4279`), `RustFieldTokens`
(`lib.rs:4302-4313`), `RustEnumTokens`, plus emission-purpose wrappers
`NewtypeInherentImplTokens`, `EnumVariantConstructorsTokens`, `SignalFrameImplTokens`
(`codex-rust-construct-survey.md §1`). Token→text is one `prettyplease::unparse`
per item with a literal `#[rustfmt::skip]\n` prepended (`RustfmtSkippedItems::render`,
`lib.rs:45-58`).

**[interpretation]** So the gap the psyche's directive targets is **not** "free
functions vs methods" in the crude sense — it is three specific, cited shortfalls
against "Rust as a form of data, projected by methods on the data node":

1. **The verb lives on an emission adapter, not on the data noun.** A
   `RustStructTokens` is a *separate* token-wrapper over the struct data; the
   projection verb is split away from the `RustModule` data it renders. Under
   verb-belongs-to-noun the projection is a method *on* the struct node
   (`impl ProjectRust for Struct`), not on a companion `…Tokens` type. The
   `…Tokens` companion is the classic `ThingData`/adapter split the rust-methods
   doctrine names as drift.
2. **The input is not stringless, not 1-to-1.** `RustModule` is a
   *rendering-oriented* lowering of `TrueSchema` whose identifiers are strings and
   whose node set is emission-shaped, not the stringless CoreLogos that is 1-to-1
   with Rust. (This is also why the current path can use std `ToTokens`: it has
   strings to emit and needs no resolver — §2.1.)
3. **Semantic content is computed at projection, not transcribed.** The two
   sharpest cases: `derive_attributes` synthesizes the derive groups from booleans
   (§1.3, `lib.rs:1596-1638`), and `field_visibility_tokens` computes field
   visibility from the type-reference graph (§1.2, `lib.rs:1659-1691`). These are
   the literal "materializes at projection" the 1-to-1 ruling forbids.

The redesign fixes all three at once by making the input Rust-as-data (CoreLogos,
stringless, 1-to-1, with every derive and visibility present as data) and moving
the verb onto the data node (`ProjectRust`, §2). The `…Tokens` adapters and the
compute-at-emission logic then **dissolve** — the node projects itself because it
already carries every Rust token as data. This is the design-quality dissolution
(special case → normal case) at the heart of the directive, and the finding
deliverable 1 asks for.

## 2. Object-method lowering — which noun owns which verb (deliverable 2)

### 2.1 One uniform trait across every node kind

The projection surface is a **single trait**, implemented once per CoreLogos node
kind:

```
trait ProjectRust {
    // Realize this node as Rust tokens, resolving any identifiers it bears
    // through the read-only NameResolver at the last moment.
    fn project(&self, names: &NameResolver) -> TokenStream;
}
```

**[interpretation]** `ProjectRust` is a **domain trait, not std `quote::ToTokens`**,
for one load-bearing reason: a stringless Core has no strings to hand `ToTokens`,
whose `to_tokens(&self, &mut TokenStream)` signature cannot carry a resolver. The
domain trait threads the `NameResolver` explicitly, which is precisely the
stringlessness contact point (§2.3). It returns a `TokenStream` (not final text)
so formatting authority stays with one prettyplease pass (§3).

The noun/verb table, compressed — every verb is a method on the node that owns
the data:

| Noun (CoreLogos node) | Data it owns | `project` verb produces |
| --- | --- | --- |
| `CoreItem` (closed enum) | one of the item variants | exhaustive match → delegates to the variant body's `project` |
| `Newtype` | visibility, attributes, name, wrapped `TypeReference` | `<attrs> <vis> struct <name>(<wrapped>);` |
| `Struct` | visibility, attributes, name, `generics`, `fields` | `<attrs> <vis> struct <name><generics> { <fields> }` |
| `Enumeration` | visibility, attributes, name, generics, `variants` | `<attrs> <vis> enum <name><generics> { <variants> }` |
| `Field` | visibility, name `Identifier`, `TypeReference` | `<vis> <name>: <ty>,` |
| `Variant` | name, payload shape (unit / tuple / named) | `<name>` \| `<name>(<types>)` \| `<name> { <fields> }` |
| `Visibility` | which of Public/Crate/Module/Private | `pub ` \| `pub(crate) ` \| `pub(in <path>) ` \| *(empty)* |
| `Attribute` (closed enum) | Derive / Configuration / ToolPath / Opaque | `#[…]` per variant |
| `DeriveGroup` | `Vec<PathNode>` | `#[derive(<paths, ", ">)]` |
| `CfgAttr` | predicate, boxed inner attribute | `#[cfg_attr(<pred>, <inner>)]` |
| `TypeReference` / `TypeApplication` | head path + optional args | `<path>` \| `<head><<args>>` |
| `PathNode` | `Vec<Identifier>` | segments joined by `::` |
| `Generics` | parameter nodes by kind | `<<params>>` or empty |
| `Identifier` | a `u32` NameTable index | `names.resolve(self)` → one ident token |

**[interpretation]** No free helper survives where a method does. There is no
`emit_newtype(item)`, no `render_field(f)`, no `RustScalarAliasTokens` adapter —
each is a method on the node whose concern it is. The only non-method entry point
is the daemon-side driver that iterates a module's items and runs the single
prettyplease pass (§3), which is the legitimate binary/entry-point exception in
the abstractions doctrine.

### 2.2 Totality — a non-projecting node is a compile error

Totality is enforced by the type system, not by convention, in two places:

1. **The closed item enum.** `impl ProjectRust for CoreItem` matches all variants
   with **no wildcard arm** (design-quality forbids the catch-all side path).
   Adding an item kind without its arm fails to compile.
2. **The trait bound at every composition point.** Every node that holds children
   holds them as `T: ProjectRust` (or as enums whose variants are all
   `ProjectRust`). A `Struct` cannot hold a `Field` that does not implement
   `ProjectRust`; the tree cannot be *constructed* with a non-projecting node.

**[interpretation]** So "every node kind projects" is not a checklist item a
future editor must remember — it is the definition of being storable in the
CoreLogos tree. This is where the method surface structurally beats a
free-function walker: a walker can silently omit a case (a missing `match` arm in
a central function, or a node the walk never visits) and fail at runtime or emit
nothing; here the omission is a type error at the node's definition site.

### 2.3 Stringlessness meets projection at one contact point — the NameResolver

**[ruling — session brief ruling 3; `design-v0.md §2`]** Every CoreLogos
identifier is a `u32` index into the logos NameTable (one continuous space
extending the schema NameTable). The Core carries **no strings**. Projection must
therefore realize names — but only at the leaves that bear an identifier.

The contact point, designed cleanly:

- `NameResolver` is a **read-only view over the NameTable**: `resolve(Identifier)
  -> &str`. It is passed *down* the `project` call tree, never held by a node.
- **Only two leaf node kinds touch it**: `Identifier::project` (a name or field
  name) and `PathNode::project` (each path segment). Every other node's `project`
  merely threads `names` to its children and composes their tokens — it never
  sees a string.
- Names are realized **at the last possible moment** — inside the leaf's
  `project`, as the ident token is minted — so a name exists as text for exactly
  the width of one `quote`/token construction and nowhere else.

**[interpretation]** This keeps the 1-to-1 binding at the Core (the identifier is
the meaning; the name is a rendering of it) and isolates the entire
string-materialization surface to two leaf methods. It also settles a subtlety
from the syntax audit (D2): the **snake_case field-name rule is a *text*
projection concern only.** CoreLogos stores every field's name as an explicit
`Identifier` (ruling 3; syntax-audit §2.3), so **Rust projection never runs
snake_case** — it resolves the stored identifier. Text projection elides the name
when it equals `snakeCase(Type)`; Rust projection always emits the stored name.
Two projections from one stringless Core, each synthesizing a different minimal
thing — and neither invents meaning.

## 3. Transcription discipline — what projection may synthesize (deliverable 3)

**[interpretation]** "Transcription" means CoreLogos → Rust adds **no meaning**.
The complete, closed list of what projection is *allowed* to synthesize — audited
against the goldens — is exactly five items:

1. **Dotted → `::`** on paths. Home: `PathNode::project` (§1.4). Nowhere else.
2. **Delimiter re-sugaring.** Logos structural brackets become the Rust surface
   the node's kind demands: a newtype body → `( … )`; a struct/enum body →
   `{ … }`; a generic argument list → `< … >`; a derive list → `( … )`. This is
   the "brace/paren re-sugaring" the syntax audit §2.5 names. Each re-sugaring
   lives in the owning node's `project`, chosen by node kind, never by lookahead.
3. **Stored-identifier realization** from the NameTable, at the two leaves (§2.3).
   Not name *invention* — resolution of an index that is already the meaning.
4. **Formatting** — whitespace, indentation, line-wrapping, trailing commas.
   Delegated entirely to **one prettyplease pass** (§3.1). No node emits final
   whitespace.
5. **The `// @generated` header**, a fixed literal per module
   (`codex-rust-construct-survey.md §1`).

Anything semantic — which derives, which visibility, struct-vs-newtype,
attribute order, cfg predicates, field names, wrapped types — is **present in
CoreLogos and transcribed**, never materialized. This is the operational meaning
of 1-to-1 (session brief ruling 2; `design-v0.md §1.1`).

### 3.1 Formatting authority stays with prettyplease — and the goldens prove it must

**[observed — `core-first-architecture-v1.md §1.5`; `codex-rust-construct-survey.md
§1`]** The current emitter produces final bytes with **one `prettyplease` pass**
over the token stream, and every item carries `#[rustfmt::skip]`. The `#[rustfmt::skip]`
in the *output* instructs any downstream consumer's rustfmt to leave the item
alone; the *generator's* own layout is prettyplease's.

**[observed — the wrapping evidence, this session's schema-rust sweep]**
prettyplease's width decisions are visible in the goldens and are **driven by
content length, not by the data's meaning**. Two witnessed cases: (i) the main
`#[derive(...)]` renders on **one line** at seven derives (binary-only,
`runner_generated.rs:82`) but **one-derive-per-line across multiple lines** once
the ordering group adds `PartialOrd, Ord` (`collections_generated.rs:81-91`) —
same node, more derives, different layout; (ii) the NOTA `#[cfg_attr(...)]` always
wraps to **four lines** because it exceeds the width
(`spirit-reactive-large.generated.rs:83-89`, `spirit_nexus_generated.rs:85-94`).
Both are prettyplease's line-breaking (~100 columns), a property of the formatter,
not of CoreLogos.

**[AGENT PROPOSAL — formatting authority]** **Keep prettyplease as the sole
formatting authority; the object-method `project` surface produces a faithful
`proc_macro2::TokenStream` and the daemon driver runs exactly one
`prettyplease::unparse` per item, with `#[rustfmt::skip]` prepended — precisely
the existing `RustfmtSkippedItems::render` shape (`lib.rs:45-58`).** Rationale: the
goldens *contain prettyplease's width-driven wrapping decisions* (the derive-count
layout switch above), which are a property of the formatter, not of CoreLogos.
Reproducing them byte-exactly by structural layout rules baked into the node
methods would mean re-implementing prettyplease's line-breaking algorithm inside
the transcription — the very "materialize formatting at projection" the
transcription discipline forbids, and a byte-exact hazard the subagent's sweep
explicitly flags ("any redesign must reproduce that prettyplease line-width
behavior to stay byte-identical"). Splitting authority cleanly — **methods own
token *structure and content* (which tokens, in what order, `::` materialized,
names realized); prettyplease owns *bytes* (whitespace, wrapping, indentation)** —
makes byte-exactness a near-tautology, because the formatter is unchanged from the
oracle. It also inherits the existing token path's parenthesization/hygiene
handling for free (`codex-rust-construct-survey.md §7.1`). The cost: a
`TokenStream` is one representation-hop between CoreLogos and text — but it carries
no new meaning (it is the same Rust, tokenized), so it does not violate
transcription; it *is* the transcription's natural intermediate.

### 3.2 The goldens gate every claim

**[ruling — `design-v0.md §4`; session brief ruling 6]** The Rust currently
generated by schema-rust (the session brief's ~9000 lines; this session's sweep
counts ~11,700 across the 9 fixture goldens, byte-exact and compiled as live
modules) is the acceptance oracle. The design reproduces them
when: CoreLogos carries the same items/attributes/fields/types the emitter would
produce, each node's `project` emits the same tokens the corresponding `…Tokens`
adapter emits, and the single prettyplease pass is byte-identical. Because
authority for the *only* non-transcribed surface (formatting) is unchanged, the
gate reduces to "does CoreLogos carry the right data and does each node emit the
right tokens" — a per-node, testable claim.

## 4. Worked example — CommitSequence and DatabaseMarker, node by node (deliverable 4)

The two oracle types (`codex-rust-construct-survey.md §3` Exhibit A, from
`signal-spirit/src/schema/signal.rs`). Schema source is one line each:
`CommitSequence.{ Integer }` and `DatabaseMarker.{ CommitSequence StateDigest }`.

### 4.1 CommitSequence — the newtype

CoreLogos value (shown with names resolved for readability; in Core each name is a
`u32` index):

```
CoreItem::Newtype(Newtype {
  visibility: Public,
  attributes: [
    ToolPath(PathNode[ rustfmt, skip ]),
    Configuration(CfgAttr {
      predicate: Feature(nota-text),
      inner: Derive(DeriveGroup[ PathNode[nota,NotaDecode], PathNode[nota,NotaDecodeTraced], PathNode[nota,NotaEncode] ]),
    }),
    Derive(DeriveGroup[ PathNode[rkyv,Archive], PathNode[rkyv,Serialize], PathNode[rkyv,Deserialize],
                        PathNode[Clone], PathNode[Debug], PathNode[PartialEq], PathNode[Eq] ]),
  ],
  name: Identifier(→ "CommitSequence"),
  wrapped: TypeReference(PathNode[ Integer ]),
})
```

Node-by-node projection (each line is one node's `project`, composed by its
parent):

- `Newtype::project` composes, in order: `attributes` (each
  `Attribute::project`), then `visibility.project`, then the literal `struct`,
  then `name.project`, then `(` `wrapped.project` `)` `;`.
- `attributes[0]` `ToolPath(PathNode[rustfmt,skip])::project` → `#[` +
  `PathNode::project` (resolves `rustfmt`, `skip`, joins with `::`) + `]` →
  `#[rustfmt::skip]`.
- `attributes[1]` `Configuration(CfgAttr…)::project` → `#[cfg_attr(` +
  predicate `feature = "nota-text"` + `, ` + `inner.project` (a `Derive`) + `)]`.
  The inner `DeriveGroup::project` resolves the three `nota.*` paths → `#[cfg_attr(feature = "nota-text", derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode))]`.
- `attributes[2]` `Derive(DeriveGroup[…])::project` → `#[derive(` + seven
  `PathNode::project` results joined by `, ` + `)]` →
  `#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]`.
- `visibility Public::project` → `pub`.
- `name Identifier::project` → `names.resolve` → `CommitSequence`.
- `wrapped TypeReference(PathNode[Integer])::project` → `Integer`.

Composed token structure, then the single `prettyplease::unparse`, yields the
verbatim golden (`spirit-reactive-large.generated.rs:83-89`; the cfg_attr wraps to
four lines by prettyplease width, §3.1):

```rust
#[rustfmt::skip]
#[cfg_attr(
    feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct CommitSequence(Integer);
```

### 4.2 DatabaseMarker — the struct

CoreLogos value (attributes identical to §4.1; the third field carries an explicit
name because it repeats a type in the full DatabaseMarker of the syntax audit; the
two-field oracle form is shown to match Exhibit A exactly):

```
CoreItem::Struct(Struct {
  visibility: Public,
  attributes: [ …identical three attribute nodes… ],
  name: Identifier(→ "DatabaseMarker"),
  generics: Generics::none,
  fields: [
    Field { visibility: Public, name: Identifier(→ "commit_sequence"), ty: TypeReference(PathNode[CommitSequence]) },
    Field { visibility: Public, name: Identifier(→ "state_digest"),    ty: TypeReference(PathNode[StateDigest]) },
  ],
})
```

Node-by-node:

- `Struct::project` composes: `attributes` (as §4.1), `visibility.project` →
  `pub`, literal `struct`, `name.project` → `DatabaseMarker`,
  `generics.project` → *(empty)*, then `{` + each `Field::project` + `}`.
- `Field[0]::project` → `visibility.project` (`pub`) + `name.project`
  (`commit_sequence`, the **stored identifier resolved — not snake_cased at
  projection**, §2.3) + `:` + `ty.project` (`CommitSequence`) + `,`.
- `Field[1]::project` → `pub state_digest : StateDigest ,`.

Composed and formatted, the verbatim golden (`signal.rs:724-733`,
`codex-rust-construct-survey.md` Exhibit A):

```rust
#[rustfmt::skip]
#[cfg_attr(
    feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)
)]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct DatabaseMarker {
    pub commit_sequence: CommitSequence,
    pub state_digest: StateDigest,
}
```

**[interpretation]** The `Configuration` node, its `project`, and its emitted
tokens are **identical** to §4.1's — the CommitSequence and DatabaseMarker
attribute preambles are the same three nodes. prettyplease alone decides the
four-line cfg_attr layout in both, width-agnostic at the node method. This is the
concrete proof that formatting authority must stay with the formatter (§3.1): one
`project` surface, one shared attribute node, byte-identical wrapping produced
downstream. (The binary-only goldens — `runner_generated.rs:85-98` — drop the
cfg_attr and render the same two types with a single-line derive; same CoreLogos
data under a different `NotaSurface`, confirming the derive/gate content is data
the surface selects, not layout the node invents.)

## 5. Evolution — adding a Rust construct, and the Phase-D self-hosting path (deliverable 5)

### 5.1 A new construct is one node + one method, zero changes elsewhere

To add, say, a `TypeAlias` with a where-clause, or a `dyn Trait` type, or a const
generic parameter:

1. Add the node type (or a variant to the relevant closed enum, e.g. a new
   `TypeReference` variant).
2. `impl ProjectRust for` it — the one method that knows its own transcription.
3. If it is a new *item* kind, add its `CoreItem` variant and the one match arm.

Nothing else changes: no central walker to thread the case through, no driver
branch, no adapter registration. Contrast the token-emitter shape, where a new
construct means a new `…Tokens` adapter *and* wiring it into the
`GenerationDriver`/`ModuleEmission` dispatch (`codex-rust-construct-survey.md §1`)
*and* extending the TrueSchema walk that decides when to invoke it. The method
design localizes the change to the node that owns the concern — the
verb-belongs-to-noun payoff, and the design-quality "special case dissolves"
property: a new construct is a new normal case, never a side path bolted onto a
central function.

### 5.2 Why this is the right shape for Phase D (Logos becomes THE Rust generator)

**[ruling — `core-first-architecture-v1.md §2.6 Phase D`; `design-v0.md §3.1`]**
The end state: Logos becomes the Rust generator; the schema-rust token lowering is
harvested as a **fixed hosted kernel**; dialects become CoreNomos macro packages
(self-hosting). The Shen/K-Lambda analogy (session brief ruling 1;
`design-v0.md §1`): Rust is the assembly language, and the fixed lowering is the
small kernel every dialect sits atop.

**[interpretation]** The `ProjectRust` impl set **is** that fixed hosted kernel —
the "K-Lambda" of the analogy. It is **dialect-agnostic by construction**: it
knows only CoreLogos node kinds, never any schema dialect. A new dialect (signal,
sema, a future one) is a CoreNomos macro package that *produces CoreLogos*
(`design-v0.md §3.1`); it adds **data** (macros), not projection code. The kernel
never grows per-dialect. This is precisely where the method surface beats the
token-emitter for self-hosting: the current `GenerationDriver` is schema-shaped
and would need per-dialect emission branches to host new dialects, but a
`ProjectRust`-over-CoreLogos kernel is a closed, fixed lowering that every dialect
reduces *into*, exactly as Shen dialects reduce into K-Lambda. The goldens gate
the kernel once; dialects are then verified by "does the macro-produced CoreLogos
lower to the same Rust," which is the oracle already ruled in `design-v0.md §4`.

## 6. The logos⇄Rust edge as a codec — two-way (psyche mid-flight extension)

**[psyche words, verbatim, typos his]** "this is also a good pattern to build on
to possibly two-way decode-encode rust (to and from logos). crazy idea, but fairly
simple even if it only works for a subset of rust (in terms of reading rust *into*
logos." The pattern he refers to is one he is shaping in a parallel lane: each
complex `Core*` type carries a **structural-expectation table entry** describing
how to handle the next block at that boundary, and the **same table drives both
decode (text→Core) and encode (Core→text)**, so round-trip coherence holds by
construction. He extends it to the logos⇄Rust edge.

### 6.1 The edge is a codec, and my one-way design is already half of it

**[interpretation]** This is not a bolt-on — it is the natural completion of the
design, and it *reinforces* the formatting-authority split (§3.1) rather than
straining it. Because Logos is 1-to-1 with Rust and projection is transcription,
the edge is inherently a **codec**: `project` (CoreLogos → Rust) is one direction;
`read` (Rust → CoreLogos) is its inverse. Everything in §2–§3 is the encode half.
The two-way move is to make **both directions run from one shared per-node-kind
structural description**, exactly his table pattern applied at the Rust text form —
not two hand-kept sides.

### 6.2 One shared `RustShape` per node kind driving both directions

**[AGENT PROPOSAL]** Give each CoreLogos node kind **one structural descriptor**,
`RustShape`, that names its Rust surface as an ordered sequence of typed
sub-components with their delimiters and the two ruled translations. A generic
codec engine runs the descriptor **forward** (encode: emit each sub-component's
tokens in order) or **backward** (decode: consume each sub-component in order from
the parsed Rust, failing loudly on mismatch). Concretely, `Newtype`'s shape is
"attributes\* · visibility · `struct` · name · `(` · type · `)` · `;`"; the engine
encodes it to tokens and decodes it from a `syn::ItemStruct` with unnamed fields.
This subsumes §2's `ProjectRust`: the node still *owns* its verb (verb-belongs-to-
noun), but the verb is now **one description** from which both `project` and `read`
derive, dissolving the "two hand-kept sides" special case — the same dissolution
the design-quality gate rewards, and the same table pattern he is already building
one layer down.

**[AGENT PROPOSAL — do not re-parse Rust ourselves; lean on `syn`.]** The decode
direction reads Rust text through **`syn::parse` → `syn` AST → map the in-subset
AST to CoreLogos**. We do *not* re-implement Rust's grammar — that would walk
straight into the context-sensitive, unbounded-lookahead complexity the syntax
audit §4.1 warns against. `syn` (with `full`) already lives in the emitter and
already round-trips through `prettyplease` on the encode side, so decode reuses
present machinery; the only new piece is the `syn`-AST→CoreLogos reader, which is
the structural inverse of the CoreLogos→tokens projector. The shared `RustShape`
is the spec both the projector and the reader are generated from; where a node's
shape needs arbitrary logic that no finite descriptor captures, it is **out of
subset** (§6.4).

### 6.3 The NameTable contact point is itself bidirectional

**[interpretation]** The stringlessness contact point (§2.3) inverts cleanly:
encode **resolves** `Identifier → &str` through the `NameResolver`; decode
**interns** `&str → Identifier` into the same NameTable, allocating identifiers as
it reads (and extending the continuous schema→logos space, session brief ruling 3).
So decoding a Rust file yields **CoreLogos + NameTable together** — the exact pair
the daemon stores. One NameTable, two directions, at the same two leaves
(`Identifier`, `PathNode`). The `.`↔`::` translation is likewise two-way and lives
in `PathNode`'s one shape: encode joins segments with `::`, decode splits a `::`
path into segment identifiers.

### 6.4 The subset boundary — stated precisely, and it fails loudly

**[AGENT PROPOSAL, grounded in `codex-rust-construct-survey.md §1,§4`]** The
principled subset is **exactly the constructs Logos models as data**, which the
survey splits into two emission shapes:

- **Cleanly two-way (the wire-contract shape):** tuple newtypes, named-field
  structs, unit/tuple-payload enums, scalar `pub type` aliases, `pub use`
  re-exports, generic parameters by kind, and the **formulaic** impls whose bodies
  are fixed patterns (`From<Payload>`, per-variant constructors like
  `Self::Variant(payload)`, newtype `new`/`payload`/`into_payload`). These have
  finite `RustShape`s; they decode and re-encode.
- **The honest frontier (the daemon-runtime shape):** `async fn` handler bodies
  with real statements, `match` with branching logic, `Display`/`Error` bodies,
  kameo `Actor` handler bodies (`codex-survey §1,§2`). Their *type/trait skeletons*
  are in-subset, but their **bodies are arbitrary Rust logic Logos does not model
  as data** (design-v0 §8 leaves method-body modeling open). So byte-exact two-way
  applies to the wire-contract goldens; the daemon-runtime goldens are only
  partially decodable until (if ever) logos models a body vocabulary.
- **Everything else fails loudly:** `unsafe`, `macro_rules!`, `union`, closures/
  iterator chains, `?`-pipelines, arbitrary expressions (all counted-zero or
  out-of-scope in `codex-survey §4`). Consistent with strictly-typed-positional
  discipline: at each boundary the decoder has an expected node kind (or a closed
  alternative set), and an unrecognized construct is a **decode error, not a silent
  skip** — the same "the parser never guesses" invariant the whole stack rests on.
  His own framing grants the subset limitation up front; this does not claim
  full-Rust parsing.

### 6.5 The bootstrap prize — the goldens become a two-way harness

**[AGENT PROPOSAL]** For every in-subset (wire-contract) golden, run
`decode(golden) → CoreLogos`, then `encode(CoreLogos) → text'`, and require
`text' == golden` **byte-exact**. This is strictly stronger than the one-way gate
(it exercises both directions and their coherence) and needs **zero hand-authored
logos fixtures** — the ~11,700 lines of existing goldens *are* the fixtures, in
both directions. Two concrete payoffs:

- **Phase-D acceptance without hand-authored logos.** When Logos becomes THE Rust
  generator (§5.2), the one-way test is "does macro-produced CoreLogos lower to the
  goldens." The two-way harness adds "does decoding the goldens produce CoreLogos
  that re-encodes identically," validating the encode kernel against real Rust
  independently of the macro pipeline.
- **The migration/harvest path made mechanical.** Decoding the current generated
  Rust into CoreLogos is *how the new system is populated from the existing corpus
  without hand-authoring logos*. And it closes the loop with my §1.2/§1.3 findings:
  the derives and visibility the current emitter **computes** at projection are
  exactly what decode **recovers as data** from the finished text — so the two-way
  codec is the mechanical answer to "how do we get 1-to-1 CoreLogos with everything
  materialized as data," by decoding the emitter's own output.

### 6.6 What stands in the way — assessed concretely

**[interpretation / AGENT PROPOSAL]** Each obstacle the extension names, checked:

1. **Formatting authority (prettyplease-owned layout).** The round-trip is
   byte-exact **only for prettyplease-canonical Rust** — but the goldens *are*
   prettyplease output (§3.1, `RustfmtSkippedItems::render`), so encode = the same
   prettyplease that made them, and decode need only recover *structure* (which
   `syn` fully preserves). Byte-exactness is therefore near-tautological **for the
   goldens specifically**; arbitrary hand-formatted Rust round-trips only up to
   prettyplease normalization, not byte-exact. This is the single most important
   caveat, and it is *why the §3.1 split matters*: structure is the shared
   invertible part, formatting is prettyplease-owned on encode and discarded on
   decode. The extension confirms §3.1 rather than conflicting with it.
2. **Comments and whitespace.** The `// @generated` header and blank-line item
   separation are **renderer-owned literals**, not Core data; `syn` discards `//`
   comments on decode. For the goldens this is fine (the header is a fixed literal
   re-emitted on encode; blank lines are the renderer's `blank`/`line` policy,
   `lib.rs:5014-5024`). Doc comments (`///`) appear only in the out-of-subset
   daemon target; `syn` would surface them as attributes if ever modeled.
3. **cfg_attr shapes and the rkyv helper.** `syn` parses `#[cfg_attr(...)]` fully
   (predicate + inner derive) and `#[rkyv(derive(...))]` as a helper attribute;
   both map to the `CfgAttr` and `HelperDerive` nodes (§1.3), and their four-line
   wrapping is reproduced by prettyplease on encode. No obstacle.
4. **Intrinsic scalars and re-exports.** `pub type Integer = u64;` and the
   `pub use … as …` blocks already round-trip through `syn::ItemUse`/type-alias
   AST in the emitter (`lib.rs:2606-2612`); decode maps them to alias/import nodes
   or the whole-file harness scopes to the declaration region.

Net: the two-way codec is **byte-exact-viable today for the wire-contract golden
corpus**, blocked only at the honestly-out-of-subset daemon-runtime method bodies,
and it turns the existing goldens into a self-supplying two-way acceptance and
migration harness. No tension with prior evidence; it strengthens the
formatting-authority proposal.

## 7. Decision points for the psyche (deliverable 6)

Each is an **[AGENT PROPOSAL]** with a one-paragraph rationale.

**Decision A — the projection trait is a domain trait, not std `ToTokens`.**
Proposal: define `ProjectRust { fn project(&self, names: &NameResolver) ->
TokenStream }` rather than implement `quote::ToTokens`. Rationale: a stringless
Core cannot satisfy `ToTokens::to_tokens(&self, &mut TokenStream)`, whose fixed
signature carries no NameResolver, so the identifiers have no way to realize; the
domain trait threads the resolver explicitly, which *is* the stringlessness
contact point and keeps it to two leaf methods. Returning a `TokenStream` (not
text) preserves single-pass prettyplease formatting authority.

**Decision B — formatting authority stays with prettyplease (§3.1).** Proposal:
methods own token structure/content; one prettyplease pass per module owns bytes.
Rationale: the goldens embed prettyplease's width-driven wrapping (the four-line
vs one-line cfg_attr, §3.1/§4), which is formatter behavior, not data; baking
layout into node methods would re-implement prettyplease inside the transcription
and risk byte-exactness. Split cleanly, byte-exactness is near-tautological
because the formatter is unchanged from the oracle.

**Decision C — visibility is stored `Visibility` data, not computed at
projection; `Private` projects to empty.** Proposal: model the right-associative
`Public.Item` *text* surface as a `visibility: Visibility` *field* in Core (ruling
2, no type proliferation), carrying the item's and field's actual Rust visibility
as data, with `Visibility::Private` projecting the empty token stream. Rationale:
this replaces the current emitter's **computed** visibility — `visibility_tokens`
mapping logos-Private→`pub(crate)` and `field_visibility_tokens` downgrading a
field via `references_private_type` (`lib.rs:1640-1691`) — with a stored value the
projection transcribes, honoring 1-to-1; it dissolves the "is there a `pub`?"
special case into a normal node whose projection happens to be empty; and it
unifies visibility at item and field level under one node (`design-v0.md §1.2
ruling 2`, syntax-audit proposal (f)). (The text↔Core equivalence — application in
text, field in Core — is the same layering the syntax audit blesses for field-name
elision.)

**Decision D — the attribute vector is a plain ordered `Vec<Attribute>`; the two
(three, with the rkyv helper) derive groups are entries, not a concept, and are
data, not computed.** Proposal: no special grouping type or logic; the gated
cfg_attr-derive, the plain derive (with any `Copy`/ordering members), and the
`#[rkyv(derive(…))]` helper are entries in the item's attribute vector,
transcribed in stored order. Rationale: this removes the emitter's
`derive_attributes(includes_copy, includes_ordering)` synthesis
(`lib.rs:1596-1638`) — the sharpest "materializes at projection" case — replacing
boolean-driven grouping with pre-materialized vector data; it keeps attributes a
uniform, order-preserving transcription; and `Attribute::ToolPath` reusing
`PathNode` (not an opaque string) is what makes `#[rustfmt::skip]` project `::`
correctly (syntax-audit proposal (h)). The `NotaSurface` distinction (feature-gated
vs binary-only vs always-enabled goldens) becomes *which attribute entries the
CoreLogos carries*, chosen upstream in Nomos, not a render-time branch.

**Decision E — snake_case field naming is a text-projection rule only; Rust
projection resolves stored identifiers.** Proposal: CoreLogos stores every field
name as an explicit `Identifier`; Rust `project` resolves it and never runs
snake_case; only the logos *text* projection elides a name when it equals
`snakeCase(Type)`. Rationale: satisfies 1-to-1 (the name is in Core, transcribed,
not invented at Rust projection — session brief ruling 2, syntax-audit D2), and
localizes the snake_case rule to one text-side method rather than duplicating it
on the Rust side.

**Decision F — totality is enforced structurally (no wildcard arm; trait bound at
every composition point).** Proposal: `impl ProjectRust for CoreItem` matches all
variants with no catch-all, and every child slot is typed `T: ProjectRust`.
Rationale: makes "every node kind projects" a compile-time property rather than a
convention a future editor must uphold; a missing projection is a type error at
the node's definition site, which is the structural advantage over a free-function
walker that can silently skip a case.

**Decision G — the logos⇄Rust edge is a two-way codec driven by one shared
`RustShape` per node kind (§6).** Proposal: give each node kind a single
structural descriptor from which both `project` (encode) and `read` (decode)
derive, with decode leaning on `syn` for parsing (never re-implementing Rust's
grammar) and interning names into the same NameTable that encode resolves from.
Rationale: completes the codec the 1-to-1 transcription implies, unifies the two
directions into one owned description (no hand-kept second side), and makes the
NameTable contact point bidirectional; the honest scope is the wire-contract
subset (§6.4), with daemon-runtime method bodies out of subset and unknown
constructs failing loudly.

**Decision H — adopt the existing goldens as a two-way acceptance and migration
harness (§6.5).** Proposal: gate the design with `decode(golden) → CoreLogos →
encode → byte-exact golden` over the wire-contract goldens, and use the same decode
to harvest the current generated-Rust corpus into CoreLogos. Rationale: needs zero
hand-authored logos fixtures, gives Phase D an acceptance mechanism independent of
the macro pipeline, and mechanically recovers as data exactly the derives/visibility
the current emitter computes at projection (§1.2/§1.3). Caveat the psyche must weigh:
byte-exact round-trip holds for prettyplease-canonical Rust (the goldens are), not
arbitrary hand-formatted Rust (§6.6).

## 8. Observations vs interpretations — separation summary

**Observed (cited, this session's schema-rust sweep of `repos/schema-rust/src/lib.rs`
unless noted):** the emitter is two-stage — `TrueSchema → LowerToRust<RustModule>`
(`:602-639`) → `RustModule` data (`:334-345`) → per-node `ToTokens` structs
(`RustNewtypeTokens :3885`, `RustStructTokens :4261`, `RustFieldTokens :4302`) →
one `prettyplease::unparse` per item with `#[rustfmt::skip]` prepended
(`RustfmtSkippedItems::render :45-58`); derive groups are **computed** by
`derive_attributes(includes_copy, includes_ordering)` from booleans + `NotaSurface`
(`:1596-1638`), including a third `#[rkyv(derive(…))]` helper group (`:1633-1637`);
field visibility is **computed** via `field_visibility_tokens`/`references_private_type`
(`:1640-1691`); the verbatim `CommitSequence`/`DatabaseMarker` goldens and their
four-line cfg_attr wrapping (`spirit-reactive-large.generated.rs:83-89`,
`spirit_nexus_generated.rs:85-94`, `signal.rs:724-733` = `codex-survey §3` Exhibit
A) and the derive-count layout switch (`runner_generated.rs:82` vs
`collections_generated.rs:81-91`); goldens are byte-exact, ~11,700 lines across 9
fixtures, compiled as modules (`core-first-architecture-v1.md §1.5`); visibility
binds right-associatively and is tested (`syntax-recrystallization-audit-v1.md
§0,§2.0`); field-name elision is a text-projection concern over a name-bearing Core
(`syntax audit §2.3, D2`).

**Interpretation (mine):** that the `…Tokens` adapters are the "Rust as tokens to
assemble" symptom of a non-Rust-shaped input (§1.6); that CoreLogos + one
`ProjectRust` trait is the "Rust as data to transcribe" replacement (§2); the
totality-by-type-system argument (§2.2); the single-contact-point NameResolver
design (§2.3); the closed five-item synthesis list (§3); the kernel-as-K-Lambda
Phase-D argument (§5.2); the whole two-way codec design (§6); and all decisions in
§7.

## 9. Sources

Design corpus (this workspace): `reports/logos/core-first-architecture-v1.md`,
`reports/logos/syntax-recrystallization-audit-v1.md`,
`reports/logos/design-v0.md`, `reports/logos/nomos-macro-model-v1.md`,
`reports/codex-rust-construct-survey.md`.

Code ground truth (read-only this session, via a scout sweep of
`repos/schema-rust`): the two-stage `TrueSchema → RustModule → ToTokens →
prettyplease` emitter (`src/lib.rs`, lines cited inline in §1, §3, §8), the
compute-at-emission derive and visibility logic (`lib.rs:1596-1691`), the
per-item `prettyplease::unparse` renderer (`lib.rs:45-58`), and the byte-exact
fixture goldens under `tests/fixtures/` (9 files, ~11,700 lines). No code was
edited and no branches were switched; repositories under `repos/` are untracked.
