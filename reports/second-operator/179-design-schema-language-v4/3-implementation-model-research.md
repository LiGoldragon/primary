*Kind: Implementation Research · Topic: schema-language-v4 implementation model · Date: 2026-05-24 · Lane: second-operator*

# 3 — Implementation model research

## Context read

Read the current v4 designer context in
`reports/designer/326-v4-spirit-complete-schema-vision.md`, the schema
repo at `/git/github.com/LiGoldragon/schema`, and the prior
second-operator reports `177` and `178`.

The important correction is that `.schema` is not ordinary one-root
NOTA data. The file is an implicit `Schema` struct: no outer wrapper,
field 0 is the regular signal header, field 1 the owner-signal header,
field 2 the sema header, field 3 imports, field 4 namespace, and field
5 optional feature variants. Maps are right for imports and namespace.
Vectors of variants are right for the headers and feature surface.

## Current code that should survive

The bootstrap code is useful as a typed substrate, not as the final v4
document shape.

- `Name` is already the right map-key nucleus. It enforces PascalCase and
  implements `NotaMapKey`, which matches namespace and import maps.
- `Namespace` as `BTreeMap<Name, DeclarationBody>` is directionally right:
  it mirrors `{Name declaration ...}` and gives deterministic ordering.
- Validation already catches duplicate declarations, duplicate variants,
  invalid names, and unknown named references before macro emission.
- `Engine` is the right starting enum for `(engine assert)` style
  annotations, although it should move into header payload metadata rather
  than live on every general-purpose `Variant`.
- `TypeExpression`, `Primitive`, and `Container` are a useful core, but
  they need the v4 grammar's type expression vocabulary: `Option`, `Vec`,
  `Map`, `Path`, imported names, and likely later fixed root/box metadata.
- `Layout` is valuable and should stay. Its current conservative rule
  for unresolved cross-schema references is the right default until
  imports are resolved.

## Model changes implied by v4

`Document { sections: Vec<Section> }` should become an explicit
`Schema` or `Document` struct with six named fields matching the
implicit file positions. Keeping `Vec<Section>` now obscures the
difference between a dispatch-driving header, an imports map, a
namespace map, and optional features.

The replacement shape should be close to:

```rust
pub struct Schema {
    signal_header: Header<OperationVariant>,
    owner_header: Header<OperationVariant>,
    sema_header: Header<SemaVariant>,
    imports: Imports,
    namespace: Namespace,
    features: Vec<Feature>,
}
```

`Section::Messaging(Vec<Declaration>)` should disappear. The v4 header is
not a declaration named `Operation`; it is the ordered root enum itself.
Its variant position is byte-0 dispatch metadata. The model should expose
that order directly through `Header`, with validation for duplicate
variant names and any header-size limits the short-header design needs.

Imports should become their own field:

```rust
pub struct Imports {
    entries: BTreeMap<Name, Import>,
}

pub enum Import {
    Path(nota_codec::Path),
    Symbolic { crate_name: String, schema: Name },
}
```

`DeclarationBody::Reference` was a useful bootstrap placeholder, but v4
puts selective cross-schema binding in field 3, not mixed into the
namespace. Name resolution should check local namespace first or according
to the ratified shadowing rule, then imported bindings. Layout can keep
imported declarations boxed until an import resolver supplies the target
schema.

Namespace declarations need one more level of shape. Today
`DeclarationBody::Local { variants }` makes everything look like an enum.
That can encode the Spirit examples, but it loses whether a declaration is
a newtype, positional record, enum, or storage record. The next model
should distinguish at least:

- unit/data enum declarations such as `Kind`;
- transparent/newtype declarations such as `Topic (Topic String)`;
- positional records such as `Entry (Entry Topic Kind Summary ...)`;
- possibly storage declarations with table metadata if storage remains in
  `Feature::Storage`.

Features should be closed variants, not extra namespace comments:

```rust
pub enum Feature {
    Reply(Vec<ReplyVariant>),
    Event(Vec<EventVariant>),
    Observable(Observable),
    Storage(Vec<StorageDeclaration>),
}
```

This keeps Reply/Event/Observable out of the signal header while still
making them part of the contract. If the psyche later ratifies putting
Reply/Event elsewhere, the type can move without changing the header and
namespace core.

## Parser consequence

No outer wrapper does not require making ordinary NOTA multi-root. The
schema crate can own a `.schema` reader that decodes exactly six
top-level NOTA values in order using `nota_codec::Decoder`, then calls
`peek_token()` to reject trailing content. Inner values still use normal
NOTA: vectors, maps, record variants, `None`/`Some`, bracket strings, and
Path positions.

That means the schema crate should add manual `Schema::parse` /
`Schema::encode` or a small `reader.rs` layer. `Schema` itself should not
derive ordinary `NotaRecord` if that would require outer parens. The
inner types can still derive or implement `NotaEncode` / `NotaDecode`.

## Validation and layout changes next

Validation should become schema-wide name resolution rather than
declaration-list scanning. It needs separate passes:

1. Validate each header's ordered variant names and payload references.
2. Validate imports as unique local bindings to `.schema` paths or symbolic
   schema names.
3. Validate namespace declarations and duplicate names.
4. Validate feature references into the namespace/import universe.
5. Build a resolved view for layout and macro consumers.

`Layout::for_variant(document, declaration, variant)` should grow a
header-aware entry point, probably `Layout::for_header_variant(schema,
HeaderKind::Signal, variant_name)`. Existing namespace-type layout remains
useful for nested records, but dispatch-root layout needs to carry the
header index as metadata.

## Recommended next patch

The next patch should be a model rewrite, not parser work:

- introduce `Schema` with the six v4 fields;
- replace `Section::Messaging` with `Header`;
- move cross-schema references out of namespace into `Imports`;
- add `Feature` variants for Reply/Event/Observable/Storage as the current
  working hypothesis;
- keep `Name`, `Namespace`, `Engine`, `TypeExpression`, and `Layout` but
  adjust them to resolve through the new schema-wide model;
- update tests to build a Spirit-shaped six-field schema and assert header
  order, import binding, namespace map decode, and conservative layout for
  imported types.

Parser work should follow after this, because the parser should lower into
the right model instead of preserving the temporary section abstraction.
