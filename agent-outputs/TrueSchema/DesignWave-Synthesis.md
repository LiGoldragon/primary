# Design wave synthesis — True Schema

## Confirmed design commitments

- **True Schema** is the canonical decoded semantic layer for the schema language.
- Existing code is implementation terrain, not design authority. The best end-shape governs.
- The current `SpecifiedSchema` idea may be renamed/repaired/replaced by `TrueSchema`, but `TrueSchema` must not become a second parallel canonical layer.
- Authored `.schema` decodes into True Schema at schema decoding time.
- Schema-rust lowering consumes True Schema; it does not generate True Schema.
- Encoding goes through True Schema. Canonical re-encoding may be normalized explicit schema text; it does not need to preserve authored inline/sequenced sugar.
- Generated Rust is a projection from True Schema, not authority or comparable schema data.
- Schema-internal decode, encode, Rust projection, help/docs, diff, and future upgrade planning derive from True Schema.
- Lazy and eager loading use the same resolver/decoder/cache machinery. Eager loading is the lazy/session machinery driven to completion.
- Help/docs data is pure typed data. It must not store rendered strings like `(Vector Domain)`. Text appears only at the final renderer/display boundary.
- Products and help are positional and label-free.

Confirmed help example:

```nota
{ Domains EntryKind Description Referents }
(Vector Domain)
[Belief Principle Preference Constraint]
Text
(Vector Reference)
```

Semantics: first row is the immediate positional component type names for `Entry`; following rows are same-order expansions. `(Help Domain)` inspects `Domain` itself. There are no field labels, no `(Name Type)` pairs, no `Name:` headings, and no wrapper such as `(Entry ...)`.

## Core data model

`TrueSchema` is a canonical typed graph, not rendered syntax.

Suggested core nouns:

- `TrueSchema`
  - module/package identity
  - normalized imports
  - roots/operation roots
  - declarations
  - streams
  - families
  - relations
  - implementation catalog or projection metadata where needed
  - non-semantic metadata sidecar
- `SymbolPath`: canonical identity for declarations, families, streams, roots, variants, and nested positions.
- `Declaration`
  - path
  - visibility
  - parameters
  - body
- `DeclarationBody`
  - `Alias(TypeReference)`
  - `Newtype(TypeReference)`
  - `Product(ProductBody)`
  - `Sum(SumBody)`
- `TypeReference`
  - primitive
  - declared symbol
  - type parameter
  - vector
  - optional
  - map
  - scope-of
  - type application
- `ProductBody`
  - ordered `ProductComponent` list
- `ProductComponent`
  - `reference: TypeReference`
  - optional projection metadata only
- `SumBody`
  - ordered variants, each unit or payload-bearing
- `FamilyDeclaration`
  - family symbol
  - record type reference
  - key kind
  - storage coordinate sidecar
- `StreamDeclaration`
  - token/opened/event/close references
- `RelationDeclaration`
  - typed relation kind and participants

Derived duplication such as precomputed payload shape summaries should be cache/view data, not canonical True Schema data.

## Positional products and projection metadata

A product is an ordered vector of component type references. For an `Entry` shape, True Schema stores references like:

1. `Domains`
2. `EntryKind`
3. `Description`
4. `Referents`

It does not store help labels for those positions. Help uses the referenced type names. If a position needs a meaningful help name, the schema should define a meaningful type/newtype. Do not invent labels such as `Kind`.

Rust field names are projection metadata:

- derived from type names by default;
- explicitly overridable only if needed;
- excluded from data/wire/storage identity and family content hashes.

## Structured HelpValue and renderer boundary

Help is a typed projection from True Schema.

Possible types:

- `HelpCatalog`
- `HelpDocument`
- `HelpSubject`
- `HelpProjectionMode`
- `HelpRow`
- `HelpRowOrigin`
- `HelpValue`
- `HelpTypeReference`

`HelpDocument.subject` records what was requested; it is not rendered as a wrapper. `HelpRowOrigin` preserves same-order expansion alignment for machines, but normal display ignores it.

`HelpValue` stores structured values such as product, sum, type reference, vector, optional, map, stream, family, cycle, or depth-limit. It never stores rendered help text.

Projection modes should include at least:

- compact: one row, immediate positional shape;
- sequential one-level: compact row plus one expansion row per immediate component;
- recursive sequential with depth/cycle control;
- policies for preserving named types versus expanding aliases/newtypes;
- policies for preserving containers versus expanding their elements.

Wrong outputs to reject for `Help Entry`:

```nota
(Entry { Domains EntryKind Description Referents })
```

```text
Domains: (Vector Domain)
```

```nota
{ (Domains (Vector Domain)) (EntryKind [Belief Principle Preference Constraint]) }
```

```nota
{ Domains Kind Description Referents }
```

```nota
{ (Vector Domain) [Belief Principle Preference Constraint] Text (Vector Reference) }
```

The final renderer is the only string-producing boundary. Machine help data round-trips through normal schema/NOTA codecs before rendering.

## Canonical identity and hashing

Hash canonical semantic data, not source text.

Include in semantic hashes:

- module/package identity;
- declarations and declaration bodies;
- type parameters;
- product component order;
- sum variant order and payloads;
- primitive kinds and composite references;
- roots;
- streams;
- family record reference and key kind;
- relations when hashing whole schema;
- resolved external symbol paths and dependency content identities.

Exclude from semantic hashes:

- comments, formatting, source spans;
- authored sugar choice;
- resolver cache state;
- lazy/eager load state;
- rendered help strings;
- generated Rust text;
- Rust field-name projection overrides for data/storage identity;
- derived caches.

Use separate hashes where needed:

- whole True Schema content hash;
- family/record closure hash for storage evolution;
- optional Rust/API projection hash;
- optional storage-binding hash for table/socket/path coordinate changes.

## Lazy/eager session model

Core nouns:

- `TrueSchemaSession`: public loading boundary for one immutable schema-set snapshot.
- `SchemaSourceProvider`: content-addressed source provider.
- `PackageRegistry`: immutable package/version registry.
- `PackageKey`
- `ModuleKey`
- `SymbolKey`
- `TrueSchemaResolver`
- `TrueSchemaCache`
- `ClosureRequest`
- `LoadedModule`
- `DeclarationClosure`
- `SchemaDiagnostics`

Lazy focused loading:

1. Normalize request into module and subject keys.
2. Load source snapshot through provider.
3. Decode module into True Schema and cache it.
4. Seed a work queue with the requested symbol.
5. Follow True Schema references only as needed.
6. Resolve imports through the same session/cache.
7. Terminate cycles by `SymbolKey` visited sets.
8. Sort closure graph canonically and hash it.

Eager environment loading uses the same APIs over all selected modules/exports. It is not a separate lowering path.

Cache keys should be content/registry based, not path/mtime based: module key, source hash, schema engine hash, macro library hash, package registry hash, and closure request.

Diagnostics should be typed, including missing source, unresolved package/symbol, ambiguous package, resolution cycle, unsupported shape, malformed schema, duplicate declaration/import alias, and version-selection failure.

## Decode/encode/projection paths

Decode path:

```text
.schema text
  -> NOTA document
  -> structural macro/source decode
  -> normalize sugar/imports/shorthands
  -> TrueSchema
  -> invariant validation
```

Encoding/projection paths:

- `TrueSchema -> binary archive -> TrueSchema`
- `TrueSchema -> structured NOTA -> TrueSchema`
- `TrueSchema -> normalized .schema text -> TrueSchema`
- `TrueSchema -> RustModule -> rendered Rust`
- `TrueSchema -> HelpDocument/HelpValue -> rendered help text`
- `TrueSchema closure -> schema diff / upgrade planning`

No projection should treat generated Rust or source text as authority after True Schema exists.

## Required invariants

Constructors should enforce:

- valid unique symbol paths;
- all references resolve to primitive, parameter, local declaration, or import;
- no duplicate imports/declarations;
- reserved primitives not redefined;
- stable product component order;
- meaningful product component type names for help;
- unique ordered sum variants;
- generic arity and parameter scoping;
- valid stream/family/relation references;
- storage coordinates do not masquerade as content identity;
- help expansion row counts align with product component order;
- projection names do not collide after Rust-name derivation.

## Proof-test gates

Tests should assert typed values before rendered text. Text goldens are only for final projection boundaries.

Needed gates:

- `.schema -> TrueSchema` decode.
- all decode entrypoints converge to identical True Schema.
- source-only trap: comments/formatting/sugar do not change True Schema hash.
- generated-Rust trap: schema-valid but Rust-projection-invalid input still decodes to True Schema and fails only at Rust projection.
- `TrueSchema -> canonical .schema -> TrueSchema` fixpoint.
- `TrueSchema -> binary/NOTA -> TrueSchema` round trips.
- Rust emission primary API consumes True Schema; compatibility APIs delegate.
- daemon stream detection consumes True Schema or a True Schema view.
- help rows are typed and positional; rendered `Help Entry` matches the confirmed example.
- help data contains no strings, labels, wrappers, or name/type pairs.
- diff takes True Schema values/closures, not text/generated Rust.
- formatting-only diff is empty.
- binary archive diff works without source files.
- lazy focused closure equals eager closure.
- lazy focused load does not load unrelated modules.
- repeated lazy/eager requests share cache.
- dependency fences prevent schema depending on schema-rust and prevent upgrade diff depending on schema-rust.
- projection traits are sealed or otherwise restricted to True Schema / True Schema views.

## Recommended staged vertical slices

1. **True Schema spine**
   - Introduce `TrueSchema` as the public decoded semantic type.
   - Remove `SpecifiedSchema` as an independent struct or make it a compatibility alias.
   - Add decode entrypoints returning True Schema.
   - Add binary and normalized `.schema` fixpoint tests.
   - Add Rust emission from True Schema and delegation tests.

2. **Projection hardening**
   - Move schema-rust build paths and daemon stream detection to True Schema.
   - Add bypass-catching and dependency-fence tests.

3. **Typed help pilot**
   - Implement typed `HelpValue` for declarations/root variants.
   - Add compact and one-level sequential help for products/enums/vectors/aliases.
   - Add confirmed `Entry` fixture and wrong-output rejection tests.

4. **Diff/upgrade alignment**
   - Move the schema diff adapter to compare True Schema closures.
   - Add family closure hashes and generated-Rust trap tests.

5. **Lazy/eager loader**
   - Add `TrueSchemaSession`, provider, registry, resolver, cache, closure requests.
   - Add lazy/eager parity, no duplicate lowering, focused minimal-loading, cycle, and deterministic closure hash tests.

6. **Remove transitional bypasses**
   - Retire or deprecate direct Schema/SchemaSource projection APIs.
   - Turn bypass tests into required checks.

Alternative first vertical slice if you want loader proof earlier: combine a minimal `TrueSchemaSession` in-memory provider with the spine, but keep help/diff out of that first implementation.

## Open questions

- Should current public `Schema` eventually become `TrueSchema`, with current `Schema` renamed/internalized?
- Should direct `Optional<T>` or raw composite references in product positions be allowed, or should meaningful named types be required?
- Is `Text` the canonical primitive, or is it a schema-declared alias/newtype over an existing primitive?
- How should recursive/cyclic help expansion render by default?
- Which storage-coordinate changes belong in whole-schema hash versus a separate storage-binding hash?
- Should cross-package closure hashes inline dependency nodes or record dependency closure hashes as edges?
- Does authored import syntax need version selectors, or should the registry always pin versions outside source?
