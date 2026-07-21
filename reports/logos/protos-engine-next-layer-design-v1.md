# Protos engine — the next layer down, as compiling shape (v1)

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

Status: DESIGN ARTIFACT. The concrete type surfaces one layer below the current
`protos` machinery, demonstrated as REAL, COMPILING Rust in an isolated `protos`
worktree and concluded Rejected (a design sketch, not a merge). This report is
the durable record; the worktree crate is removed on conclusion, so every
load-bearing signature is quoted here verbatim.

This layer concretizes the settled ruling in
`reports/logos/id-namespace-slicing-design-v1.md` (the identifier is a
data-carrying enum whose variant is the slice; the nametree is composable; a
table borrows slices rather than copying them). That report is the WHY; this one
is the compiling HOW, grounded line-by-line in the real code of `repos/protos`
and `repos/core-*`.

## What compiled

An illustrative crate `next-layer-sketch` was added to the protos workspace,
path-depending on the real machinery crates (`content-identity`, `name-table`,
`raw-discovery`, `structural-codec`). It builds green and its three unit tests
pass against the real crates.

Denominator, stated honestly: `cargo test -p next-layer-sketch` and
`cargo clippy -p next-layer-sketch` are GREEN on toolchain 1.85.0 — the sketch
crate plus its four real path-dependencies compile, and the concrete-type tests
run. A full `nix flake check` across the whole workspace was NOT run (not
required for a Rejected design worktree; the sketch imports and exercises the
real surfaces, which is the evidence that matters here).

## The layer, in one picture

```
  ============================  THE TWO ORGANS  ============================

     NAMETREE  (names live here)          STRUCTURETREE  (shapes live here)
     the composed NameTable               the AddressedStructuralTable
     = borrowed schema slice              = one sealed, data-driven table
     + borrowed standard slice              the ONE trusted evaluator walks
     + owned logos (home) slice             in BOTH directions

  ============================  THE TWO-WAY PIVOT  =========================

   READ                                            EMIT
   ----                                            ----
   Manifest            (explicit file list,        EncodedForm + NameTree
     |                  dependency-ordered)              |
     |  to_view                                          |  reflect -> mirror
     v                                                   v
   TextualForm         (filename -> text index)    evaluator.encode
     |                                              (structuretree, other way)
     |  recognize + evaluator.decode                     |
     v  (structuretree, one way)                         v
   StructuralValue mirror                           TextualForm
     |  reify                                            |
     v                                                   |  from_view
   EncodedForm + NameTree grown                     Manifest -> files

            \___________________  ONE structuretree  ___________________/
                         both directions, off the SAME table
```

No string crosses the pivot's interior. Text is admitted only into the manifest
files and the `TextualForm` chunks at the two ends; between them every value is a
stringless EncodedForm plus slice-tagged identifiers.

## Surface 1 — the Identifier enum (the variant IS the slice)

Delta from current code. Today `name_table::Identifier` is flat
(`name-table/src/identifier.rs:24`):

```
pub struct Identifier(u32);   // one global index into one Vec<Name>
```

The next layer lifts the partition into the type. Verbatim from the sketch:

```
pub enum Identifier {
    Schema(u16),
    Logos(u16),
    LogosStandard(u16),
}

impl Identifier {
    pub const fn slice(self) -> Slice { ... }         // variant -> slice tag
    pub const fn offset(self) -> u16 { ... }          // inner u16
    pub const fn at(slice: Slice, offset: u16) -> Self { ... }
}

pub enum Slice { Schema, Logos, LogosStandard }
```

A `Schema(7)` and a `Logos(7)` are distinct values that cannot be confused;
resolution is an exhaustive match, total by construction; the variant set IS the
namespace registry. This is the 16jw intent (enums over numbers) applied to the
id space itself — the whole class of block-arithmetic errors becomes unwritable.

### The generated standard-slice constants (the engine's reference surface)

The standard objects get compile-time constants — referring to a standard object
never touches a nametable and never allocates. Verbatim:

```
pub const STRING: Identifier = Identifier::LogosStandard(0);
pub const INTEGER: Identifier = Identifier::LogosStandard(1);
pub const BOOLEAN: Identifier = Identifier::LogosStandard(2);
pub const PATH: Identifier = Identifier::LogosStandard(3);
pub const ARCHIVE: Identifier = Identifier::LogosStandard(4);
pub const SERIALIZE: Identifier = Identifier::LogosStandard(5);
pub const DESERIALIZE: Identifier = Identifier::LogosStandard(6);
pub const CLONE: Identifier = Identifier::LogosStandard(7);
pub const DEBUG: Identifier = Identifier::LogosStandard(8);
```

Grounding note. The object spellings are drawn from REAL fixtures, not invented:
`String`/`Integer`/`Boolean`/`Path` are `core-nomos`'s fixed `scalar_aliases`
(`core-nomos/src/prelude.rs:124`); the derive names are `core-logos`'s test
golden preamble (`core-logos/tests/support/mod.rs`). The OFFSETS are illustrative
— in the real engine the constants are GENERATED from a content-identified
standard nametree (the id-slicing report's shipment lean: generated). No such
surface exists today; the standard vocabulary is re-interned by string on every
run, which is exactly what these constants retire.

## Surface 2 — the composed NameTable

Delta from current code. Today a downstream component builds its table with
`NameTable::extend_from`, which is literally `base.clone()`
(`name-table/src/table.rs:99`): a full copy of every shared name into every
component, after which the standard vocabulary is re-interned at the tail — so a
standard object's id depends on schema size (the latent special case the slicing
report dissolves). The composed table BORROWS the shared slices instead. Verbatim
shape:

```
pub struct ComposedNameTable<'shared> {
    schema: &'shared [Name],          // borrowed read-only
    logos_standard: &'shared [Name],  // borrowed read-only
    logos: Vec<Name>,                 // OWNED home slice, the append target
    logos_index: HashMap<Name, u16>,  // interning accelerator for home ALONE
}

impl<'shared> ComposedNameTable<'shared> {
    pub const HOME: Slice = Slice::Logos;
    pub fn compose(schema: &'shared [Name], logos_standard: &'shared [Name]) -> Self;
    pub fn resolve(&self, identifier: Identifier) -> Result<&Name, ComposedNameError>;
    pub fn intern(&mut self, name: Name) -> Identifier;
}
```

`resolve` dispatches on the identifier variant to the owning slice — the home
slice for `Logos`, a borrowed slice otherwise. `intern` targets the home slice
ALONE: a name already present in a borrowed slice keeps that slice's identifier
(never duplicated), and only a genuinely new name appends. This is the literal
realization of "the continuous identifier space" — continuous because a schema id
is the SAME value seen from two components, not because one copied the other's
indices.

Picture:

```
   component nametree (ONE view, the "one NameTable per component" ruling)
   +---------------------------------------------------------------+
   |   [ standard slice ]  borrowed, read-only   (LogosStandard)   |
   |   [ schema slice ]    borrowed, read-only   (Schema)          |
   |   [ logos slice ]     owned, append target  (Logos = home)    |
   +---------------------------------------------------------------+

   resolve(id)  = match id.slice() { Logos => home[o], Schema => schema[o], ... }
   intern(name) = append into the HOME slice only (borrowed slices are read-only)
```

Relation to existing code: `NameTransaction` (`name-table/src/transaction.rs`)
already embodies "stage on the side, never touch the base". The composed table
generalizes that from one staging buffer over one base to a permanent read-only
borrow of several bases at once, the owned home slice playing the staging role.

## Surface 3 — the Protos trait (the two-way pivot made concrete)

The current code already carries the single-document pivot: `Textual::view` /
`Textual::unview` (`structural-codec/src/textual_form.rs`) drive the two organs
through the one trusted evaluator. Their real signatures (verbatim from the
crate):

```
fn view(&self, expected: ScopedCoreTypeId, encoded: &Self::Encoded,
        names: &mut NameTable) -> Result<TextualForm<Self::Language>, Self::Error>;

fn unview(&self, expected: ScopedCoreTypeId, view: &TextualForm<Self::Language>,
          names: &mut NameTable) -> Result<Self::Encoded, Self::Error>;
```

What is NEW at this layer is the manifest dimension: a component is many files,
resolved cargo-style, producing many EncodedForm items over ONE growing
nametree. The `Protos` trait adds exactly that wrapping and nothing else — every
per-language line still lives in the mouth's `reify`/`reflect`. Verbatim from the
sketch (default bodies compile against the real `Textual`):

```
pub trait Protos {
    type Mouth: Textual;

    fn mouth(&self) -> &Self::Mouth;
    fn root_type(&self) -> ScopedCoreTypeId;
    fn emit_path(&self, index: usize) -> SourcePath;

    // READ: manifest -> TextualForm -> (structuretree) -> EncodedForm set + NameTree
    fn read(&self, manifest: &Manifest, names: &mut NameTable)
        -> Result<Vec<<Self::Mouth as Textual>::Encoded>, <Self::Mouth as Textual>::Error>;

    // EMIT: EncodedForm set + NameTree -> (structuretree) -> TextualForm -> manifest
    fn emit(&self, items: &[<Self::Mouth as Textual>::Encoded], names: &mut NameTable)
        -> Result<Manifest, <Self::Mouth as Textual>::Error>;
}
```

The structuretree organ is the real `AddressedStructuralTable`
(`structural-codec/src/table.rs`), sealed with its own content identity stored
outside the hashed payload; the trusted `StructuralEvaluator` walks it both ways.
The seven-case kernel it carries (the StructureTree's leaf vocabulary) is the
real `StructuralForm` (`structural-codec/src/form.rs`): `Product`, `Atom`,
`Leaf`, `Literal(Identifier)`, `Application{head,payload}`, `Delimited`,
`Delegate(ScopedCoreTypeId)`.

## Surface 4 — the manifest

Delta from current code. No manifest type exists in the family today; the only
file-list mechanism is Cargo git-rev pinning in each consumer's `Cargo.toml`,
which every consumer's ARCHITECTURE.md calls a stopgap. The designed replacement,
verbatim:

```
pub struct SourcePath(pub String);

pub struct ManifestFile {
    pub path: SourcePath,
    pub content: String,   // text admitted HERE and nowhere past the read boundary
}

pub struct Manifest {
    pub files: Vec<ManifestFile>,   // already in resolved dependency order
}

impl Manifest {
    pub fn in_dependency_order(&self) -> &[ManifestFile];
    pub fn to_view<Language>(&self) -> TextualForm<Language>;    // -> real chunk index
    pub fn from_view<Language>(view: &TextualForm<Language>) -> Self;
}
```

The order IS the resolved dependency order — the resolver runs before the value
exists, so downstream never re-derives it. Per the psyche ruling (below) the
first resolver is the FULL EXPLICIT CHECKED-IN manifest, and the manifest is a
typed object end to end — never a loose file list. The typed `Manifest`/
`ManifestFile`/`SourcePath` shape here is that direction; the one residual bare
string to tighten is `SourcePath(String)`, which should become a typed path
object (`ManifestFile.content` stays text as the admitted read-boundary source).
The mapping to the real `TextualForm` (`structural-codec/src/textual_form.rs`, an
indexed set of named `TextChunk`s) is total and reversible; the sketch's
round-trip test proves `from_view(to_view(m)) == m`.

## Surface 5 — the no-strings partition, visible in the signatures

The partition is not a comment; it is where `String`/`&str` is allowed to appear.
In the whole sketch, text lives in exactly two places:

```
   ADMITTED (the two ends)                 FORBIDDEN (the interior)
   -----------------------                 ------------------------
   ManifestFile.content : String           Protos::read  returns Vec<Encoded>
   TextChunk.text       : String           Protos::emit  takes  &[Encoded]
   Name(String)  (the one home of a        ComposedNameTable::resolve -> &Name
                  name's bytes)            Identifier / Slice : no strings
```

`EncodedConversion` (`structural-codec/src/encoded_form.rs`) is the same law for
the layer-to-layer transform: its `convert` signature carries `Source`, `Target`,
and `&NameTable` and returns `Converted<Target>` — no `&str`/`String` anywhere on
the path. The schema->logos lowering through the Nomos macros is the first
instance; the composed nametree crosses the layer as ONE table.

## The two joints — SETTLED (psyche ruling, 2026-07-19)

Most of this layer was already settled in the id-slicing report; the sketch
mostly confirmed the settled shapes compile against the real code. Two genuine
joints surfaced, both narrow, and the psyche ruled both. His verbatims are
captured here as the ruling of record.

1. The two organs' nametree parameter type — SETTLED: RETYPE. Verbatim: "retype
   of course. spirit would have answered that". The mouth's organ parameters
   retype from the concrete `&mut NameTable` to the composed nametree (the sliced
   `Identifier` and the `NameInterner`/`NameResolver` boundary traits move with
   it), and they land in the ONE slicing cascade. There is NO compose-above-the-
   mouth second cascade — surfaces 1-2 and 3 are one break, not two. His
   observation to carry: Spirit intent under vjvm already answered this (no
   backward-compatibility to preserve, so the clean retype is the obvious form the
   codified intent implies); it did not need to be asked. `Textual::view`/`unview`/
   `reify`/`reflect` are the four members that retype.

2. The manifest's dependency resolver — SETTLED: full explicit checked-in
   manifest, typed end to end. Verbatim: "yes, full explicit manifest. dont ignore
   the types the machine wants - everything is typed data". The first resolver is
   the checked-in FULL EXPLICIT manifest — not an ad hoc path walk — and the
   manifest is itself TYPED DATA: a typed object end to end, never a loose file
   list. The sketch's typed `Manifest`/`ManifestFile`/`SourcePath` surface is the
   right direction and is affirmed as such. One place the sketch still treated a
   manifest part as untyped: `ManifestFile.content: String` and `SourcePath(String)`
   carry raw text. `content` is the one legitimately-admitted read-boundary text
   (the source bytes to be recognized), so it stays text; but `SourcePath` should
   be a typed path object rather than a bare `String` wrapper, and the manifest
   container as a whole is a typed object (the list, the ordering, the paths), not
   a loose list — the ruling forecloses any untyped-list shortcut. Read at surface
   4 accordingly: the typed direction is correct, the residual bare-string path
   wrapper is the one spot to tighten.

Everything else — the enum shape, the composed borrow, the generated standard
constants, the two-way pivot over one structuretree, the no-strings partition —
is the settled design made concrete and shown to compile.

## Appendix — verified code anchors

- `name-table` — `Identifier(u32)` (`src/identifier.rs:24`); `NameTable` one
  `Vec<Name>` + derived index, `intern`/`resolve`/`extend_from`=`base.clone()`
  (`src/table.rs`); `NameResolver`/`NameInterner` the two codec-boundary
  capabilities (`src/boundary.rs`); `NameTransaction` the speculative overlay
  (`src/transaction.rs`); `Name(String)` the one home of a name's bytes
  (`src/name.rs`).
- `structural-codec` — `Textual` with `view`/`unview` over the two organs and
  `reify`/`reflect` the only per-language code (`src/textual_form.rs`);
  `EncodedForm`/`EncodedConversion` the truth side (`src/encoded_form.rs`);
  `AddressedStructuralTable` the sealed structuretree (`src/table.rs`);
  `StructuralForm` the seven-case kernel (`src/form.rs`); `ScopedCoreTypeId`
  (`src/ids.rs`); `TextualForm`/`TextChunk`/`ChunkName` the chunk index
  (`src/textual_form.rs`).
- `core-nomos` — `scalar_aliases` fixes `String`/`Integer`/`Boolean`/`Path`
  (`src/prelude.rs:124`); `NameTableBoundary::new` builds the logos table via
  `extend_from(schema_names)` and re-materializes standard atoms per run
  (`src/name_boundary.rs`).
- `core-schema` — `CoreUniverseBuilder`/`FixtureFamily` intern the standard
  vocabulary one `intern("...")` call at a time (`src/universe.rs`,
  `src/fixture.rs`); no `const Identifier` anywhere.
- `core-logos` — the golden-preamble derive vocabulary
  (`Archive`/`Serialize`/`Deserialize`/`Clone`/`Debug`/`PartialEq`/`Eq`) interned
  in `tests/support/mod.rs`; no prelude/standard registry in `src/`.
```
