# Self-Describing Schema: Structural Help and Unified Type-Reference Vocabulary

This document consolidates the design for making the schema stack
self-describing. It covers four work areas: the Decision-A canonical-name
migration, unification of the duplicate `TypeReference` vocabularies into the
seed crate, a new type-level help renderer, and the Menchie/Mentci consumer
wiring. File paths are cited against `/home/li/primary/repos/`.

## 1. Intent and the Five Locked Decisions

The goal is a schema stack where any type-defining position can describe itself
structurally, where help lives only on the schema side, and where the
self-descriptive notation (e.g. `createdAt.Timestamp`) is reconstructed from
structure rather than authored prose. These five decisions are the settled
spine and are not to be relitigated.

1. STRUCTURAL-CONTENT-FIRST. The structural type representation is the unit of
   identity and help lookup. The global namespace (`Schema.namespace`, keyed by
   `Name`) is one named index into a universe that also includes
   anonymous/structural/positional types. An unnamed position must be able to
   self-describe.

2. HELP LIVES ONLY ON THE SCHEMA (type-definition) SIDE, never co-located with
   instance data. Instances are pure positional values; nota-next
   `InstanceSchema` only points back via `expected: TypeReference`. "Help never
   lives with the data everywhere" is structural, not a discipline.

3. HELP IS THE SCHEMA'S OWN SELF-DESCRIPTIVE NOTATION (e.g.
   `createdAt.Timestamp`), rendered/reconstructed from structure, NOT authored
   prose strings. Position-name + type-name + recursion into the referenced
   type carry the meaning.

4. DECISION A: the canonical schema-form name (camelCase, e.g. `createdAt`)
   becomes the STORED truth in the Schema AST; snake_case Rust (`created_at`)
   becomes a DERIVED PROJECTION at Rust-emit time (move `Name::field_name()`
   from lowering-time to emit-time). This re-keys every type's blake3 content
   identity — an accepted one-time migration. Field names are positional on the
   wire, so they feed only the Rust projection and help, never
   encoding/resolution.

5. PURE STRUCTURAL HELP — no prose strings, ever. The self-descriptive notation
   is the entire help; NO authored doc/description fields are added to the AST.
   Opacity is resolved structurally (clearer name, or a newtype whose own
   definition carries the meaning). The type graph IS the documentation. There
   is no new help-data to hash — the only identity change is the Decision-A
   canonical-name re-key.

## 2. Current Ground Truth

### 2.1 Dependency direction (the seed)

Confirmed from `Cargo.toml` files under `repos/`:

- `nota-next` — crate `nota` v0.5.1, deps only `nota-derive` (path) + `rkyv`.
  No schema dependency. This is the seed.
- `schema-next` — crate `schema` v0.2.0, dep `nota` (git nota-next) + blake3 +
  rkyv; build-dep `nota` same.
- `schema-rust-next` — crate `schema_rust` v0.5.3, deps `nota` (git nota-next)
  AND `schema` (git schema-next).

Direction: `nota-next <- schema-next <- schema-rust-next`. The unified
structural type-reference vocabulary MUST live in `nota-next` (or lower) so it
is visible to all three with no cycle.

### 2.2 The lossy lowering (the core defect for Decision A)

`repos/schema-next/src/source.rs`, `SourceField::to_lowered_field` (~2488-2549)
is the single place that destroys canonical casing. Four occurrences of
`name: Name::new(self.name.field_name())` (lines 2499, 2515, 2524, 2541) bake
the snake_case projection (`created_at`) into the stored `FieldDeclaration.name`
instead of keeping the camelCase canonical identifier (`createdAt`). The
`TypeReference` value already uses the original `self.name` via
`resolver.resolve_name` (casing preserved), so the field NAME is the only lossy
site.

Scope confirmation: only struct FIELD names are lowered lossily. Enum variant
names are cloned verbatim (`SourceVariantSignature::to_enum_variant` ~2842-2868,
`self.name().clone()` with no `field_name()`); newtype/struct/enum declaration
names flow through `self.name.qualified_under(namespace)` (~887/891,
`to_declaration_group` ~1742/2189) which only prefixes a namespace and never
lowercases. The migration is therefore scoped to field names only.

### 2.3 The three near-duplicate reference vocabularies

1. `schema-next::TypeReference` (`repos/schema-next/src/schema.rs` ~2124-2144,
   with `NotaDecode`/`NotaEncode` ~2176-2267, `StructuralMacroNode` ~2278-2348)
   — the richest: named scalar leaves + `Plain(Name)` + `ScopeOf` +
   `Application` + import-resolved heads (`ApplicationHead` ~1983-1997, variants
   `Local(Name)`/`Imported(ResolvedImport)`). Has `Path`, no
   `SignedInteger`/`Float`.
2. nota-next instance-local `TypeReference`
   (`repos/nota-next/src/instance_schema.rs` lines 26-51): `Named(&'static str)`,
   `Vector`, `Optional`, `Map`, `FixedBytes(usize)`. Compile-time `&'static str`
   names; scalars and declared types are both undifferentiated `Named`. Has
   `SignedInteger`/`Float` (i32/i64/f64) on the instance side, no `Path`.
3. `SourceReference` (`repos/schema-next/src/source.rs` ~3102-3151):
   `Plain`/`FixedBytes`/`Vector`/`Optional`/`ScopeOf`/`Map`/`Application` with
   `head: Name` — the source-parse-stage projection and the existing
   convergence point (both other vocabularies lower into it).

### 2.4 Ground-truth CORRECTION: InstanceSchema is NOT orphaned

The original brief claimed nota-next `InstanceSchema` is orphaned. It is not.
It is re-exported from `repos/nota-next/src/lib.rs:23-24`, rendered by
`repos/schema-next/src/instance.rs` as `InstanceSchemaText` (exported at
`schema-next/src/lib.rs:16`), and emitted by `schema-rust-next`
(`NotaDecodeTraced` derive ~1964, hand-emitted optional-leaf enum ~4842-4890).
The unification therefore has live consumers and must keep them compiling.

A working PER-INSTANCE renderer already exists: `instance.rs`'s
`InstanceSchemaText` (depths `::aligned` / `::expanded`) renders each reference
token through `SourceReference::from_instance_reference` (`source.rs:3180`) +
`SourceReference::rendered_schema_text` (`source.rs:3172`). The genuine gap is a
TYPE-LEVEL renderer (no instance in hand) plus the Menchie consumer.

Why a type-level renderer cannot reuse the per-instance one: an enum at type
level must fan out ALL variants, but `InstanceSchemaBody::EnumPayload` carries
only the one chosen variant; `Vector`/`Optional`/`Map` instance bodies carry
actual elements, not the declared element type. `mentci-lib/src/render.rs`
currently only calls `to_nota()` (confirmed `render.rs:78`).

### 2.5 Identity / hashing

`repos/schema-next/src/identity.rs`: `ContentHash::derive` (lines 75-79) hashes
rkyv bytes of `Schema` (whole-schema, `content_hash` ~207-210) and
`FamilyClosure`/`SpecifiedFamilyClosure` (~163-200). `FieldDeclaration.name` is
reachable in those bytes (`visit_declaration` struct field walk ~637-647).
`HashDomain` context date strings live at lines 49-50 (`schema 2026-06-12 ...`).
Generated code embeds `family_identity` `schema_hash` constants
(`schema-rust-next/src/lib.rs` ~1209-1212, ~1230, ~1250) and a runtime guard
`RecordFamily` `SchemaHashMismatch` (~5476-5484) hard-fails on mismatch.

## 3. Implementation Plan (Ordered, Sequenced)

The four areas have a hard ordering: the Decision-A migration (Area 1) must
land before help correctness (Area 3), because the renderer reads
`FieldDeclaration.name` expecting canonical camelCase. The TypeReference
unification (Area 2) re-keys identity and should be bundled into the SAME
migration as Area 1 to avoid two re-keys. Area 4 depends on Area 3.

### Step 1 — Area 1: Decision-A canonical-name migration

Land these together; they are interdependent (the stored form changes, so every
reader/writer of the field name moves in lockstep).

- 1a. `repos/schema-next/src/source.rs`, `SourceField::to_lowered_field`
  (~2488-2549): replace all four `name: Name::new(self.name.field_name())`
  (lines 2499, 2515, 2524, 2541). Explicit-name path (`createdAt.Timestamp`):
  store `self.name` verbatim. Derived/PascalCase-shorthand path (atom
  `Timestamp`, `SourceFieldValue::Derived`): store a camelCase canonicalization
  (leading segment lowercased, interior caps kept) via a new
  `Name::schema_field_name()` companion.
- 1b. `repos/schema-rust-next/src/lib.rs`, `RustFieldTokens::to_tokens`
  (~4749-4760): change line 4754 from
  `RustIdentifier::new(self.field.name().as_str())` to apply the snake_case
  projection at emit, e.g. `RustIdentifier::new(self.field.name().field_name().as_str())`.
  This is the NEW derivation point. `RustField` lowering (`LowerToRust<RustField>`
  ~1471-1477) just clones `FieldDeclaration.name`, so snake_case is produced
  here at render time.
- 1c. `repos/schema-rust-next/src/lib.rs`, identifier-validation pass
  (~492-526): update `RustIdentifier::verify_field(field.name())` at line 508
  to validate the PROJECTED snake_case (`field_name()` of the stored camelCase),
  not the stored name (`verify_field`/`verify` ~2107-2111/2091). The gate must
  validate what is actually emitted.
- 1d. `repos/schema-next/src/source.rs`, `SourceField::from_type_reference`
  (~2314-2324): flip the shorthand-detection guard
  `Name::new(reference_name.field_name()) == name` so it compares the camelCase
  projection of the type name to the stored camelCase name. This reverse path
  (semantic -> `SourceField` for re-rendering `.schema` text) decides shorthand
  `Timestamp` vs explicit `createdAt.Timestamp`; the equivalence test must move
  to camelCase or round-tripping breaks.
- 1e. AUDIT + policy: `SourceReference::derived_field_name` (`source.rs`
  ~3306-3340), used at `from_positional_block` (~2385), synthesizes snake_case
  positional-field names (`work_vector`, `optional_x`, `x_by_y`). Decide:
  re-cast to camelCase (`workVector`, `optionalX`, `xByY`) for uniform
  canonical storage, or accept snake_case (idempotent under `field_name()` at
  emit) and document the inconsistency. This is an OPEN ITEM (see 5) but the
  audit happens here. It affects help-rendering uniformity and blake3 bytes.
- 1f. AUDIT — NO CHANGE: confirm enum variant names and newtype/struct/enum
  declaration names stay canonical PascalCase (per 2.2). The migration is
  field-name-only.

### Step 2 — Area 2: unify TypeReference into nota-next (seed)

Bundle with Step 1 (shared re-key). Adding variants changes the rkyv archived
layout, so it must be in the same migration.

- 2a. NEW module `repos/nota-next/src/type_reference.rs` + re-export from
  `repos/nota-next/src/lib.rs` (alongside the existing instance-TypeReference
  re-export ~23-24). Define the UNIFIED `nota::TypeReference`: dedicated scalar
  leaves `String`/`Integer`/`SignedInteger`/`Float`/`Boolean`/`Path`/`Bytes`
  (the UNION of both vocabularies — see scalar-set risk), `FixedBytes(width)`,
  `Plain(Name)`-style named leaf, `Vector`/`Optional`/`Map`/`ScopeOf` boxed
  forms, and `Application{head, arguments}`. Derive rkyv (nota already deps
  rkyv) plus the nota codec traits (`NotaDecode`/`NotaEncode`/
  `StructuralMacroNode`).
- 2b. Move a structural `Name` (or a minimal name newtype) down to nota-next so
  the unified `Plain`/`Application` head can name declared types without
  depending up into schema-next. This forces resolving the
  `StructuralMacroNode` error-type coupling: the impls for `Name`
  (`schema.rs:108`) and `TypeReference` (`schema.rs:2279`) currently use
  `type Error = SchemaError`, and `SchemaError` lives in schema-next. Introduce
  a nota-local error type or generalize. (OPEN ITEM — see 5.)
- 2c. Application head fork: `ApplicationHead::Imported(ResolvedImport)` is
  import-resolution machinery that CANNOT descend to the seed. The unified
  `Application` head must be a plain `Name` (with schema-next keeping
  import-resolution in a side mapping) OR the unified type is generic over the
  head representation. `ScopeOf`/`Application` are never produced by the traced
  decoder, so the seed type is a superset the instance side under-uses. (OPEN
  ITEM — see 5.)
- 2d. `repos/schema-next/src/schema.rs`: replace schema-next's own
  `TypeReference` (~2124-2144 + its codec/`StructuralMacroNode` impls
  ~2176-2348) by re-exporting/aliasing the unified nota type, or keep a thin
  delegating wrapper.
- 2e. `repos/nota-next/src/instance_schema.rs`: replace the nota-local
  `TypeReference` (lines 26-51) with the unified type. Update the
  `NotaDecodeTraced` impls (`scalar_traced!` ~168-196, `ByteSequence` ~198,
  `FixedByteSequence` ~212, `Vec` ~226, `Option` ~256, `BTreeMap` ~289) to
  construct unified variants: map `Named("String"/"Integer"/...)` to unified
  scalar leaves and declared `Named(name)` to unified `Plain(name)`. Note
  `&'static str` becomes owned (one small allocation per node).
- 2f. `repos/schema-next/src/source.rs` + `repos/schema-next/src/instance.rs`:
  once both sides share one type, simplify/remove
  `SourceReference::from_instance_reference` (`source.rs` ~3180-3194) and the
  `InstanceSchemaText::reference_text` bridge (`instance.rs` ~46-48). That lift
  exists only to render nota's instance `TypeReference` through the schema
  encoder; unification makes it identity. Decide whether the third vocabulary
  `SourceReference` (`source.rs` ~3102-3151) folds in too or stays the
  parse-stage projection. (OPEN ITEM — see 5.)
- 2g. `repos/nota-next/src/lib.rs` re-exports (~23-24, 33): surface the unified
  type, keep `InstanceSchema`/`NotaDecodeTraced` exports. In
  `repos/schema-rust-next/src/lib.rs`, the emitted `NotaDecodeTraced` code
  (derive activation ~1964, hand-emitted optional-leaf enum ~4842-4890
  constructing `nota::InstanceSchema`/`InstanceSchemaBody`) and
  `instance_reference()` construction must build unified variants.

### Step 3 — Area 3: type-level help renderer (gated on Step 1)

Crate-home MUST be schema-next: it is the only crate holding both the `Schema`
namespace (for `Plain(Name)` resolution) and `SourceReference` (the shared token
encoder). nota-next has no concept of named declarations.

- 3a. NEW module `repos/schema-next/src/help.rs`. Define
  `SchemaHelp<'schema>{ schema: &'schema Schema }` with:
  - `type_help(&self, name:&str, depth:HelpDepth) -> Option<TypeHelpNode>` —
    entry by declared name via `Schema::type_named` (`schema.rs:607`).
  - `field_help(&self, field:&FieldDeclaration, depth) -> TypeHelpNode` — the
    canonical `fieldName.Type` position; `field.name.to_nota()` is the camelCase
    token after Decision A, reference resolved + recursed.
  - `help_for_instance_reference(&self, r:&nota::TypeReference, depth) -> TypeHelpNode`
    — the Menchie bridge: reuse `SourceReference::from_instance_reference`
    (`source.rs:3180`, until 2f collapses it), then resolve names against the
    namespace.
  - Core recursion `reference_node(&self, &SourceReference, depth, visited:&mut BTreeSet<String>)`:
    scalars -> `Leaf(token)`; `Plain(name)` -> at `Surface` just the name token,
    at `Depth(n>0)`/`Full` resolve `Schema::type_named` (via
    `SourceReference::plain_name`, `source.rs:3156`) and recurse into the
    `Declaration` body at depth-1 with a visited-name cycle guard;
    `Vector`/`Optional`/`Map`/`ScopeOf` -> wrap recursed child(ren);
    `Application` -> head + recursed arguments.
  - `declaration_node` walks `TypeDeclaration` (`schema.rs:1561`): `Struct` ->
    `Struct{name, fields:[field_help per FieldDeclaration in StructFieldMap order]}`;
    `Enum` -> `Enum{name, variants:[HelpVariant{name, payload: variant.payload.map(reference_node)}]}`
    (the type-level fan-out over `EnumDeclaration.variants`, `schema.rs:1758`);
    `Newtype` -> `Newtype{name, inner}`.
  - Every reference token comes from
    `SourceReference::from_type_reference(reference).rendered_schema_text()` and
    delimiters from `nota::Delimiter::{Parenthesis,Brace,SquareBracket}` —
    identical to `instance.rs` so type-level and per-instance tokens match
    exactly. Provide `TypeHelpNode::to_text()` reproducing the
    dot/paren/brace shape.
  - Types: `HelpDepth` = `Surface` (top-level meaning only: this position's
    `name.Type` plus one level of member reference tokens, never recurse into a
    referenced type's definition) / `Depth(usize)` (recurse N levels) / `Full`
    (whole graph with visited-name cycle guard); `TypeHelpNode` (`Leaf` /
    `Field{name,reference,target}` / `Struct{name,fields}` / `Enum{name,variants}`
    / `Newtype{name,inner}` / `Vector` / `Optional` / `Map`); `HelpVariant`
    (`{name, payload: Option<TypeHelpNode>}`).
- 3b. `repos/schema-next/src/lib.rs`: add `mod help;` (next to `mod instance;`
  at lib.rs:6,12) and
  `pub use help::{SchemaHelp, HelpDepth, TypeHelpNode, HelpVariant};` (next to
  `pub use instance::InstanceSchemaText;` at lib.rs:16).
- 3c. OPTIONAL `repos/schema-next/src/source.rs`: extract the `fieldName.Type`
  dot-notation token currently inlined in `SourceField::to_schema_text`
  (~2334-2353, `format!("{}.{}", name, reference)`) into a small `pub` helper so
  `help.rs` renders the field token from one place. Keeps `name.Type`
  single-sourced.

### Step 4 — Area 4: Menchie/Mentci consumer (gated on Step 3)

- 4a. `repos/mentci-lib/src/render.rs`: add a structural-walk surface beside the
  existing `RenderNota` fallback (stays as the no-schema/unknown-object path,
  render.rs:68-96). Introduce
  `trait RenderHelp{ fn render_help(&self, origin:RenderOrigin, schema:&schema_next::Schema, depth:schema_next::HelpDepth) -> RenderedHelp; }`
  with a blanket impl for `Object: nota_next::NotaDecodeTraced`: read the start
  type from `Object::instance_reference()` (`nota-next/src/instance_schema.rs:161`
  — returns `TypeReference::Named(name)` for a contract struct, no value decode)
  and call `SchemaHelp::new(schema).help_for_instance_reference(&Object::instance_reference(), depth)`.
  Add `RenderedHelp{ origin:RenderOrigin, tree:schema_next::TypeHelpNode }`
  (parallel to `RenderedObject`). The egui shell renders tree nodes recursively
  using `TypeHelpNode::to_text()` for leaf text plus the `RenderOrigin` label —
  instead of dropping a flat `to_nota()` string.
- 4b. `repos/mentci-lib/Cargo.toml`: add a schema-next git dependency, gated
  behind the existing `nota-text` feature or a new sibling `schema-help`
  feature, mirroring the existing optional gating so the no-schema build
  (`RenderNota` -> `Debug`/`to_nota`) still compiles.

## 4. Risks and Migration

### 4.1 Blake3 identity re-key (lead risk)

Changing stored field-name casing moves EVERY whole-schema blake3 hash and
every family-closure hash whose family reaches a struct
(`schema-next/src/identity.rs`, `ContentHash::derive` 75-79, whole-schema
`content_hash` ~207-210, family closures ~163-200; field name reachable via
`visit_declaration` ~637-647). Adding `TypeReference` variants in Area 2 ALSO
changes the rkyv archived layout, invalidating persisted rkyv schema blobs.
Bundle BOTH into ONE migration.

The re-key is observable at runtime through `RecordFamily` `SchemaHashMismatch`
(`schema-rust-next/src/lib.rs` ~5476-5484), which hard-fails until stored
identity and regenerated identity match. The migration tooling (no single file)
must atomically: (1) regenerate every persisted/stored schema's content hash
from the new camelCase AST; (2) re-emit the generated Rust crates so embedded
`family_identity` `schema_hash` constants (`schema-rust-next/src/lib.rs`
~1209-1212, ~1230, ~1250) match; (3) re-store any rkyv-archived schema blobs.
Optionally bump the `HashDomain` context date strings
(`identity.rs` lines 49-50) to mark the new identity scheme.

Verify `schema-next/tests/identity.rs` are relational (hash-equality/inequality)
rather than hardcoded hex; if any golden asserts lowered field names as
snake_case, update expectations to camelCase while confirming emitted Rust stays
snake_case.

### 4.2 Scalar-set mismatch

nota's instance side has `SignedInteger`/`Float` (i32/i64/f64) and NO `Path`;
schema-next's `TypeReference` has `Path` and NO `SignedInteger`/`Float`. The
unified leaf set must be the UNION or the instance trace loses fidelity (or
schema gains leaves it never emits). The union adds variants -> further identity
re-key (already inside the bundled migration).

### 4.3 ApplicationHead cannot descend

`ApplicationHead::Imported(ResolvedImport)` is import-resolution machinery;
forcing it into the seed pulls schema-next internals into nota-next
(cycle/over-coupling). The seed head must be a plain `Name` or generic, with
resolution kept in schema-next.

### 4.4 field_name() not perfectly invertible

If a stored canonical name contains characters that don't round-trip
(already-underscored derived names, dashes), the emit projection can drift from
the historical snake_case. Confirm the `derived_field_name` policy so
stored->emit is stable.

### 4.5 Error-type coupling ripple

Moving `Name` (and the `StructuralMacroNode` impls for `Name` and
`TypeReference`, both `type Error = SchemaError`) to nota-next ripples error
coupling; `SchemaError` lives in schema-next and must be generalized or replaced
with a nota-local error.

### 4.6 Mixed-casing inconsistency

`derived_field_name` synthesizes snake_case positional names; if left unchanged
while explicit fields become camelCase, the canonical stored naming is
internally inconsistent, surfacing in help rendering.

### 4.7 Help correctness gated on Decision A

The renderer reads canonical camelCase from `FieldDeclaration.name`, which only
exists after Decision A re-keys the AST. Against the current AST it would emit
`created_at.Timestamp`, not `createdAt.Timestamp`. Step 1 must land before
Step 3 (or co-ship).

### 4.8 Recursion termination

`HelpDepth::Full` needs a visited-type-name cycle guard (`BTreeSet<String>`) or
it will not terminate; `Depth(n)` bounds termination but truncates mid-graph —
the truncation token must be unambiguous (bare `Plain` name) so help stays
honest.

### 4.9 Consumer coupling

mentci-lib is content-agnostic and currently depends only optionally on
nota-next. Adding schema-next couples the client model to the heavy schema
crate. Mirror the existing `nota-text` optional-feature gating so the no-schema
build still compiles.

### 4.10 Partial-unification seam

Three near-duplicate vocabularies exist. A partial unification that merges only
two leaves the third (`SourceReference`) as an ongoing projection seam and a
source of future drift.

### 4.11 Generic Application / type parameters

`Declaration::parameters` (`schema.rs:1133`) exist. The type-level walk must
decide whether to substitute `Application` arguments into the referenced
parameterized `Declaration` or render binder names verbatim.
`InstanceSchemaText` never faced this (instances are monomorphic), so there is
no precedent to copy.

## 5. Open Items Needing Psyche Input

1. CANONICAL FIELD-NAME FORM at lowering for the three `SourceField` shapes:
   explicit (`createdAt.Timestamp` -> store `createdAt` verbatim), PascalCase
   shorthand (`Timestamp` -> `timestamp`?), and synthesized
   positional/composite (`(Vector Work)` -> `workVector` camelCase or keep
   `work_vector`?). Determines whether `derived_field_name` (`source.rs` ~3306)
   must be re-cast to camelCase.
2. UNIFIED SCALAR-LEAF SET: include nota's `SignedInteger`/`Float` and schema's
   `Path` as a union? And whether nota's instance side keeps an undifferentiated
   `Named` or adopts the dedicated scalar variants + `Plain(Name)` split.
3. APPLICATION HEAD representation in the seed (plain `Name` vs generic-over-head
   vs schema-side side-table for `ResolvedImport`) and where `ScopeOf` lives,
   given the instance decoder never produces `ScopeOf`/`Application`.
4. HASHDOMAIN DATE BUMP (`identity.rs` lines 49-50) to mark the new identity
   scheme, vs. silent re-key.
5. THIRD VOCABULARY: does `SourceReference` (`source.rs` ~3102) fold into the
   unified type or stay as the source-parse-stage projection? If it stays,
   `from_instance_reference` may still be partially needed.
6. NAME DESCENT: does `Name` itself descend to nota-next or only a minimal
   structural name newtype, and how to resolve the `StructuralMacroNode`
   `type Error = SchemaError` coupling (`Name` @schema.rs:108, `TypeReference`
   @schema.rs:2279).
7. MIGRATION TOOLING that enumerates every persisted schema, regenerates content
   hashes, re-emits generated crates with new `schema_hash` constants, and
   re-stores rkyv blobs atomically with the AST change.
8. RENDERER (a) RETURN SHAPE: a structured `TypeHelpNode` tree (Menchie lays it
   out, expand-on-click) vs a flat string matching `InstanceSchemaText`.
   Recommend the structured tree + `TypeHelpNode::to_text()` projection; confirm
   which is primary.
9. RENDEREDOBJECT SHAPE: add a parallel `RenderHelp`/`RenderedHelp` surface
   (recommended — keeps `RenderNota` fallback intact) or fold both into a
   `RenderBody` enum `{Nota(String)|Help(TypeHelpNode)}`.
10. VARIANT PAYLOAD-WRAPPER COLLAPSING: `instance.rs` collapses transparent
    variant newtype wrappers to provenance (`collapsed_reference`/
    `collapsed_expansion` ~124-156). Should the type-level renderer apply the
    same collapse for visual parity? The type-level walk has no provenance field
    to fall back on.
11. WHERE MENCHIE OBTAINS THE STORED `&Schema` AT RUNTIME. Contract objects
    expose their type NAME via `NotaDecodeTraced::instance_reference()` but carry
    no Schema handle. The shell must supply the Schema artifact (embedded
    `SchemaIdentity` blob? loaded file? passed by the daemon?). This is the
    load-bearing unresolved input for Area 4.
12. DEFAULT DEPTH for Menchie's first paint (`Surface` vs `Depth(1)`), and
    whether depth is interactive (egui expand/collapse drives `HelpDepth` per
    node) — affects whether `type_help` is called once with `Full` or lazily per
    expanded node.
