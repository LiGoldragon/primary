# Plan — True Schema design

## 1. Scope

- Design only for True Schema, canonical decoded semantic layer for the schema language.
- No implementation/tracker decisions are made by the report.

## 2. Confirmed psyche requirements

- Name the canonical decoded semantic layer **True Schema**.
- True Schema is the better name and design for the existing `SpecifiedSchema` idea.
- Schema-internal usage should derive from True Schema.
- Authored `.schema` decodes through True Schema; encoding also goes through True Schema.
- Generated Rust is a projection from True Schema, not authority.
- Lazy and eager decoding use the same resolver/decoder/cache machinery.
- True Schema retains enough data for docs/help projections.
- Help data is pure typed data, not rendered strings. Final text is produced only at display/projection boundary, conceptually by a `HelpValue` decode/render method.
- Confirmed help example:

```nota
{ Domains EntryKind Description Referents }
(Vector Domain)
[Belief Principle Preference Constraint]
Text
(Vector Reference)
```

Semantics: first row immediate positional component type names; following rows same-order expansions; no field labels, no `(Name Type)` pairs, no `Name:` headings. `(Help Domain)` inspects the component itself.

## 3. Current-state evidence

- `SchemaSource` is typed authored source layer.
- `Schema` is semantic core/current assembly.
- `SpecifiedSchema` is closest current candidate: fully specified after authored sugar decoded/resolved/made explicit; Rust top-level emission already routes through it.
- `.schema` text encoding is currently owned by `SchemaSource`, not `SpecifiedSchema`/True Schema.
- Bypasses exist: raw parsing, source summary parsing, instance rendering, some Rust subobject lowerers, daemon stream detection.
- No shared lazy/eager loader/cache exists yet.
- Exact name True Schema was not found locally; do not create a parallel layer beside `SpecifiedSchema`.

## 4. Architecture decision

- True Schema should rename/reposition/repair `SpecifiedSchema`, not wrap it and not sit beside it as a second canonical layer.
- Keep a temporary compatibility alias `SpecifiedSchema = TrueSchema` if needed.
- Keep current `Schema` only as transitional assembly/intermediate; eventually internalize or rename it.
- Canonical path: `.schema text -> Document -> macro/source syntax -> assembly if needed -> TrueSchema -> projections`.

## 5. Lazy/eager design

- Introduce `TrueSchemaSession` or `TrueSchemaLoader` owning package/source registry, `SchemaEngine`, module cache, and resolver view over that cache.
- Lazy focused loading resolves only the requested module/root/declaration/family/help/diff closure and dependencies.
- Eager environment loading drives the same machinery to completion across manifest/modules.
- Eager is lazy driven to completion, not a separate implementation.

## 6. Encode path design

- `TrueSchema::to_binary_bytes` / `from_binary_bytes` for canonical archive.
- `TrueSchema` has structured NOTA encode/decode.
- `TrueSchema::to_schema_text` for canonical `.schema` projection.
- `.schema` decode entry should be `SchemaEngine::decode_true_schema` or similar.
- Source-facing data to retain includes identity, imports/aliases/resolved imports, declaration order, visibility, names/type parameters, positional component/type references, enum variants/payloads, streams/families/relations, impls, symbol paths, and component names needed for help.

## 7. Help design

- Add typed `HelpCatalog`, `HelpEntry`, `HelpSubject`, `HelpProjectionMode`, `HelpValue`, and `HelpRow` or equivalent.
- `HelpValue` stores structured type references/shapes/alternatives/rows, not strings.
- Rendering to NOTA text is final-boundary only.
- Compact and sequential expansion modes must preserve positional order and avoid labels.

## 8. Proof tests

- `.schema -> TrueSchema` decode.
- `TrueSchema` binary round trip.
- `TrueSchema` NOTA round trip as structured data.
- `.schema -> TrueSchema -> .schema -> TrueSchema` canonical round trip.
- Help output for Entry uses positional rows as confirmed.
- Formatting-only source changes do not affect True Schema/diff.
- Lazy and eager loading produce identical True Schema values/hashes.
- Import resolution uses cache/shared loader.
- Rust emission consumes True Schema.
- Daemon stream detection consumes True Schema.
- Tests catch or remove direct bypasses.

## 9. Recommended first implementation slice

- Introduce `TrueSchema` as the actual type currently named `SpecifiedSchema`, with compatibility alias if needed.
- Add `SchemaEngine::lower_true_schema_*`/`decode_true_schema` methods; old specified methods delegate.
- Make top-level Rust emission explicitly TrueSchema-based.
- Add canonical `TrueSchema::to_schema_text` through existing typed source codecs.
- Add a focused loader/cache pilot plus lazy/eager parity test.
- Add minimal structured help pilot for declaration subjects and the confirmed Entry shape.

## 10. Non-goals

- Do not remove `SchemaSource` yet.
- Do not force all external repos to rename immediately.
- Do not create a second canonical layer.
- Do not revive Asschema/AssembledSchema.
- Do not make generated Rust comparable data.
- Do not implement full help daemon or production upgrade execution.
- Do not preserve original formatting/spans unless needed for typed diagnostics.
- Do not implement label-pair help output.

## 11. Open questions

- Should current public `Schema` eventually become `TrueSchema`, with current `Schema` renamed/internalized?
- Should canonical `.schema` re-encoding preserve inline declaration sugar, or is normalized explicit source acceptable?
- In help output, should component names come only from type names, or is an explicit component-name concept needed?
- Is `Text` a schema-declared alias/newtype, or should the primitive remain whatever the schema declares?
- How should recursive/cyclic help expansion stop and display references?
- Where should `TrueSchema` live: rename `specified.rs`, create `true_schema.rs`, or move then alias?
