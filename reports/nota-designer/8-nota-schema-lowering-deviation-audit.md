# NOTA And Schema Lowering Deviation Audit

*Kind: Audit + Design · Topic: NOTA/schema lowering · Date: 2026-05-24 · Lane: nota-designer*

## Claim

The current `schema` crate is close to the latest schema intent, but the NOTA
schema implementation is split across two competing surfaces:

- `/git/github.com/LiGoldragon/schema` is the right home for the typed
  schema-language substrate and already models the six-position `.schema`
  document plus `AssembledSchema`.
- `/git/github.com/LiGoldragon/signal-frame/macros/src/schema_reader.rs` still
  carries a private schema reader with compatibility grammars that contradict
  current NOTA/schema intent.

The reusable shape is a schema-owned lowering engine: authored schema nodes
decode into typed macro-variant input structs, builtin lowerers assemble those
inputs into `AssembledSchema`, and proc-macros consume `AssembledSchema` rather
than parsing schema text themselves.

This report complements `reports/designer/329-schema-macro-component-extensibility.md`.
That report names the positive pattern: InputStruct-per-variant,
`SchemaMacro`, executer dispatch, builtin macro variants, and extensibility.
This report audits the current implementation against that pattern and names
the deviations that need to collapse into it.

## Current Intent Baseline

The strongest current intent says:

- `.schema` files are six fixed positional fields: imports, ordinary header,
  owner header, sema header, namespace, features. This is repeated in
  `schema/INTENT.md:9-24`, `schema/ARCHITECTURE.md:16-24`, and
  `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md:51-61`.
- Schema headers use the uniform v13 shape `(Root [SubVariant ...])`; scalar
  `(Root Payload)` is retired. This is in `schema/AGENTS.md:24-25`,
  `schema/ARCHITECTURE.md:31-34`, and `reports/designer/326-v13-spirit-complete-schema-vision.md:184-209`.
- Authored schemas lower into `AssembledSchema`, the explicit machine object
  for short-header generation, code emission, storage descriptors, and version
  projection. See `schema/INTENT.md:19-21` and `schema/ARCHITECTURE.md:41-55`.
- Schema is not only a Spirit contract format; it is the reusable macro-lowered
  declaration bedrock. See `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md:85-100`
  and Spirit records 492 and 507.

The fresh psyche clarification captured as Spirit records 505 and 507 adds one
key constraint: builtin macro-schema variants at node-definition points are
data-carrying variants. Each builtin variant needs a payload struct that
defines that macro variant's input object.

## Deviations Found

### 1. `signal-frame-macros` Has A Parallel Schema Reader

`signal-frame/macros/src/schema_reader.rs` is now the largest drift surface.
It has a private `SchemaParser`, private `ResolvedSchema`, private
`ResolvedDefinition`, private `ResolvedVariant`, and private conversion into
`ChannelSpec`. That duplicates the `schema` crate's role.

Concrete contradictions:

- `parse_import_first_schema` treats the first `{...}` as a namespace-style map
  and injects `"Operation"` directly from the next header vector
  (`schema_reader.rs:183-213`) instead of using the `schema` crate's
  `Import` / `ImportAll` directives and `AssembledSchema`.
- Tests still accept `(Path schemas/signal-sema/magnitude.schema)` as an import
  value (`schema_reader.rs:1519` and `schema_reader.rs:1587`), but the current
  import model uses explicit variants such as `Import` and `ImportAll`.
- Tests still use `[Option Topic]` / `[Option Kind]`
  (`schema_reader.rs:1528`), but current schema intent corrected container type
  expressions to `(Option Topic)` and `(Vec RecordSummary)`.
- Tests still accept scalar headers like `(Record Entry)`
  (`schema_reader.rs:1590-1593`), but scalar header form is explicitly retired.
- The private reader rejects multi-endpoint header nodes
  (`schema_reader.rs:925-930`, test at `schema_reader.rs:1629-1655`), while v13
  intent requires the exact opposite: multi-sub-variant headers are the normal
  expressive case.

This is the biggest practical problem: even if `schema` is correct, an active
macro input path can keep teaching and accepting old schema.

### 2. `schema` Erases Macro Input Object Roles

`schema/src/declaration.rs:51-114` models records as
`Record(Vec<TypeExpression>)` and data-carrying variants as
`Payload::Fields(Vec<TypeExpression>)`. The parser fills those vectors in
`schema/src/parser.rs:125-155`.

That is enough to describe NOTA's final positional wire shape. It is not
enough to describe builtin macro inputs as input objects. A builtin macro
variant such as `HeaderRoot`, `ImportDirective`, `Feature`, `StorageTable`, or
future `NodeDefinition` needs a payload struct with named roles at the Rust
model layer:

```rust
pub enum NodeDefinition {
    HeaderRoot(HeaderRootInput),
    EnumDefinition(EnumDefinitionInput),
    RecordDefinition(RecordDefinitionInput),
    ImportDirective(ImportDirectiveInput),
    Feature(FeatureInput),
}
```

The field names do not appear in final NOTA value syntax. They exist in the
Rust input object so lowering can be explicit, testable, and reusable.

### 3. Engine Annotations Do Not Reach `AssembledSchema`

`Variant` stores `engine: Option<Engine>` (`schema/src/declaration.rs:60-105`),
but `Schema::assemble` lowers routes with only leg, slots, root, endpoint, and
body (`schema/src/document.rs:248-264`). `Route` does not carry the engine.

Macro emission needs to ask `AssembledSchema` which route lowers to which Sema
engine class. Today it must rediscover that information from authored
namespace data. That defeats the point of assembly.

### 4. Layout Uses Pre-Assembled `Document`

`Layout::for_declaration` and `Layout::for_variant` take `Document` rather
than `AssembledSchema` (`schema/src/layout.rs:10-25`). Imported fixed-width
types are unknown at that phase; `is_fixed_width_declaration` returns `false`
when `document.declaration_body(name)` is absent (`schema/src/layout.rs:151-153`).

The earlier second-designer audit already caught the concrete result:
imported `Magnitude` is boxed even though it is a fixed-width enum. This is a
semantic gap before storage descriptor and short-header codegen should consume
layout metadata.

### 5. `AssembledSchema` Lacks Component Identity And Canonical UIDs

The intent says the root identity comes from filename context and lowered
schema output uses fully qualified universal identifiers. Current
`AssembledSchema` has imports, routes, types, and features only
(`schema/src/assembled.rs:9-15`). It cannot mint a component-scoped UID such as
`spirit::Topic` or later a fuller namespace path.

This is not a NOTA syntax bug, but it blocks the assembled form from being the
canonical stored comparison object the schema daemon needs.

### 6. The Schema Repo Does Not Yet Self-Describe With Its Own Schema

Spirit records 476, 430, 431, and 432 say the schema language should be
specified by its own schema file and bootstrap itself through its own namespace
logic. The `/git/github.com/LiGoldragon/schema` repo currently has no
`schema/*.schema` or `schema/*.concept.schema`; it only has Rust source and
test fixtures.

That is acceptable for the current MVP implementation, but it is a documented
gap against the self-hosting/meta-schema direction.

### 7. Concept Schema Validation Is Only A Smoke Guard

`upgrade/scripts/check_concept_schemas.py` validates the broad six-section
shape, rejects comments and quote strings, checks header vectors with regex,
and requires `(Version 0 1)`. That is fine as a temporary sweep guard.

It must not become schema truth. It does not use `nota-codec`, does not resolve
imports, does not assemble, and cannot validate macro-variant input payloads.
The schema-owned reader/lowering engine should replace it for real validation.

## Reusable Lowering Shape

The reusable component should live in `schema`, not in `signal-frame-macros`.
The proc-macro can call into it, but it should not own schema semantics.
The shape below is intentionally aligned with `/329`; names may settle there,
but the ownership boundary should not move back into the macro crate.

The clean pipeline:

```text
authored .schema text
  -> SchemaDocument
  -> NodeDefinition variants
  -> BuiltinLowerer registry
  -> AssembledSchemaBuilder
  -> AssembledSchema
  -> macro adapters / runtime registry / upgrade planner
```

### Layer 1: Authoring Types

These are the sugar-facing shapes decoded from NOTA:

```rust
pub struct SchemaDocument {
    pub imports: ImportsInput,
    pub ordinary_header: HeaderInput,
    pub owner_header: HeaderInput,
    pub sema_header: HeaderInput,
    pub namespace: NamespaceInput,
    pub features: FeatureInputSet,
}

pub enum NodeDefinition {
    ImportDirective(ImportDirectiveInput),
    HeaderRoot(HeaderRootInput),
    NamespaceEntry(NamespaceEntryInput),
    TypeDefinition(TypeDefinitionInput),
    Feature(FeatureInput),
}
```

Each enum variant is data-carrying unless it is genuinely a unit marker. The
payload type is the input struct for that builtin macro variant.

### Layer 2: Builtin Macro Variants

Builtins are closed at first. Each builtin has one input object and one lowerer:

```rust
pub trait BuiltinLowerer {
    type Input;
    fn lower(
        &self,
        context: &mut LoweringContext,
        input: Self::Input,
    ) -> Result<()>;
}
```

Example builtin inputs:

```rust
pub struct HeaderRootInput {
    pub root: Name,
    pub endpoints: Vec<EndpointInput>,
}

pub struct EndpointInput {
    pub name: Name,
}

pub struct EnumDefinitionInput {
    pub name: Name,
    pub variants: Vec<VariantInput>,
}

pub struct RecordDefinitionInput {
    pub name: Name,
    pub fields: Vec<FieldInput>,
}

pub struct ImportDirectiveInput {
    pub binding: Name,
    pub directive: ImportDirective,
}
```

This is the point that resolves the user's macro-variant constraint: the
variant is data-carrying, and the carried data is a struct that defines the
macro variant's input object.

### Layer 3: Lowering Context

`LoweringContext` owns the state that must not be hidden in parser functions:

- component identity from the file path;
- current node path for diagnostics;
- namespace stack and imported bindings;
- UID minting;
- route slot allocation;
- feature and engine annotations;
- loaded imported `AssembledSchema` objects;
- duplicate detection;
- diagnostics with source span/path context when available.

The context should be reusable by both proc-macro use and later daemon/registry
use.

### Layer 4: Assembled Builder

`AssembledSchemaBuilder` is the only mutable accumulator. Builtin lowerers do
not emit Rust and do not patch macro-specific structures. They call builder
methods:

```rust
builder.insert_import(binding, source, exported_names)?;
builder.insert_type(uid, body)?;
builder.insert_route(route)?;
builder.attach_engine(route_identifier, engine)?;
builder.attach_feature(feature)?;
builder.attach_layout(type_identifier, layout)?;
```

The output is canonical `AssembledSchema`: resolved imports, component identity,
UIDs, routes, local/imported types, engine annotations, features, layout, and
upgrade hints.

### Layer 5: Adapters

Adapters are downstream:

- `signal-frame-macros`: `TryFrom<&AssembledSchema> for ChannelSpec`, then the
  existing emit path.
- `version-projection`: derive projection impls from previous/next assembled
  schemas.
- `sema-engine`: storage descriptor emission from assembled storage nodes.
- future schema daemon: store and query `AssembledSchema` values.

This prevents proc-macro code from becoming the schema authority.

## What Should Change First

1. Add `schema` support for component identity and canonical UIDs.
2. Add named input structs for builtin node definitions while keeping final
   NOTA value encoding positional.
3. Move engine metadata onto lowered `Route` or a route-indexed table in
   `AssembledSchema`.
4. Move layout planning from `Document` to `AssembledSchema`.
5. Replace `signal-frame-macros/src/schema_reader.rs` with an adapter that
   calls `schema::LoadedSchema::read_path(...).assembled()`.
6. Add compatibility-breaking tests that reject `(Path ...)`, `[Option T]`, and
   scalar `(Root Payload)` in the macro schema path.
7. Add a schema repo self-schema/meta-schema file once the builtin
   `NodeDefinition` input model is settled.

## Non-Goal

Do not introduce a second syntax or a second schema DSL. The reusable lowerer
is a NOTA/schema engine: one NOTA parser, typed schema nodes, builtin macro
variants, one assembled object. The implementation move is to consolidate
semantics into `schema`, not to spread partial schema readers across proc-macro
crates.
