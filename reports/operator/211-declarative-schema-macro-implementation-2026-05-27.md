# 211 — Declarative schema macro implementation pass

## Trigger

Psyche corrected the schema-stack prototype: agents were talking as if schema
already had a macro system, but the implementation still mostly behaved like
Rust shape-lowering. The specific gap was visible binding/reference syntax:
without something like `$Name` or `$*Fields`, macro-assigned symbols were not
actually referable inside schema-authored macro bodies.

Intent records captured before implementation:

- Spirit record 888 — do not pretend schema has a macro system when it is only
  ad hoc Rust shape lowering.
- Spirit record 889 — schema macro expansion must be schema-defined and run
  through generic macro-loading logic over structured NOTA nodes.
- Spirit record 890 — macro bodies need explicit binding/reference syntax; a
  sigil such as `$` is the current candidate and references must be visible in
  the schema language.

Follow-up correction, same day:

- Spirit record 891 — brace namespaces are key/value maps only; the pair-style
  `Name body` namespace is right and parenthesized namespace entries are wrong.
- Spirit record 893 — a namespace is conceptually dynamic-enum-like, but its
  authored and lowered structure is a key/value map.
- Spirit record 892 — namespace additions should move toward append-only
  discipline so future enum-like compilation can stay upgradeable.

Follow-up module-system direction, same day:

- Spirit record 895 — fully qualified schema names use a single colon as the
  namespace separator.
- Spirit record 896 — schema-derived crates carry `schema/lib.schema` as the
  entry point.
- Spirit record 897 — generated Rust should mirror the schema module layout in
  a dedicated schema module tree.
- Spirit record 898 — cross-crate imports resolve by crate name from the
  imported crate's standard schema folder.

## What changed

### `schema-next`

Initial commit: `d340433f` — `add declarative schema macro expansion`.

Correction commit: `8c821cba` — `make schema namespaces key-value only`.

Module commit: `807c5250` — `add schema package module entrypoint`.

`schema-next` now has a declarative macro layer loaded from
`schemas/builtin-macros.schema`. The current built-ins are real macro
definitions, not Rust-only special cases:

```nota
(SchemaMacro SchemaStructDefinition NamespaceDeclaration
  ($Name [$*Fields])
  (Type (Struct $Name [$*Fields])))

(SchemaMacro SchemaEnumDefinition NamespaceDeclaration
  ($Name ($*Variants))
  (Type (Enum $Name ($*Variants))))
```

The sigil rules implemented in the prototype:

- `$Name` captures one NOTA block.
- `$*Fields` / `$*Variants` capture a repeated sequence of blocks.
- The template re-emits NOTA text with those captures substituted.
- The expanded template is parsed again and lowered into assembled schema.
- Nested macro positions are still routed through the registry: struct
  definitions expand to a template that then invokes `SchemaStructFields`;
  enum definitions invoke `SchemaEnumVariants`.

The old `TypeDeclarationMacro`, `StructFieldsMacro`, and `EnumVariantsMacro`
Rust-only lowerers were removed. Root imports/root input/root output/root
namespace are still Rust bootstrap macros; the namespace body is now the first
declarative proof.

After the correction pass, `RootNamespaceMacro` no longer accepts the obsolete
parenthesized namespace-entry form. The only authored namespace form is a flat
brace map:

```nota
{
  Entry [Topic Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
}
```

The module follow-up adds `SchemaPackage` and `SchemaModuleSource`. A package
loads a crate-local `schema/lib.schema` entry point, assigns a schema identity
such as `spirit-next:lib`, and exposes module path derivation for sibling
schemas. Colon-qualified names now lower through the assembled schema `Name`
type, with field-name generation using the local part after the last colon.

### `schema-rust-next`

Initial commit: `1268af75` — `consume four-root declarative schema engine`.

Correction commit: `b5a851a1` — `consume key-value schema namespaces`.

Module commit: `5ca1c964` — `emit schema module file paths`.

The Rust emitter now consumes the four-root `schema-next` API backed by the
declarative macro engine. It still emits Rust source as a file artifact before
compilation. The generated fixture is constrained to use data-bearing helper
objects instead of module-level helper functions.

The module follow-up makes the emitted file path derive from the assembled
schema identity. For example, `spirit-next:lib` emits `schema/lib.rs`, and
`spirit-next:signal:public` emits `schema/signal/public.rs`. The first
namespace segment is treated as the crate boundary; the remaining segments
become the generated Rust module path.

New Nix constraints prove:

- production emitter source has no module-level free functions;
- production emitter source has no unit-struct method holder;
- generated Spirit fixture has no module-level free functions;
- the generated fixture uses `NotaSource` / `NotaBlock` helper objects, not the
  old `parse_nota_root` helper surface.

### `spirit-next`

Initial commit: `0a509e35` — `run spirit pilot on declarative schema macros`.

Correction commit: `8ef16bc5` — `use key-value schema namespace in spirit pilot`.

Module commit: `e004fc62` — `load spirit schema from lib entrypoint`.

The runnable Spirit pilot now uses the current four-root schema shape:

```nota
{}
(Input ((Record Entry) (Observe Query)))
(Output ((RecordAccepted RecordIdentifier) (RecordsObserved RecordSet) (Error ErrorMessage)))
{
  SemaCommand ((Record Entry) (Observe Query))
  SemaResponse ((Recorded RecordIdentifier) (Observed RecordSet) (Missed ErrorMessage))
  Entry [Topic Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
}
```

The module follow-up renames the pilot schema entry point to
`schema/lib.schema`. The build script loads that entry point through
`SchemaPackage`, lowers it with identity `spirit-next:lib`, emits generated
Rust to `OUT_DIR/schema/lib.rs`, and includes it as `spirit_next::schema::lib`.

The build script asserts the declarative macro path:

- `SchemaStructDefinition` followed by `SchemaStructFields`;
- `SchemaEnumDefinition` followed by `SchemaEnumVariants`;
- `RustEmitter::default().emit_file(...)` emits the generated Rust artifact.

I also removed production free-function surfaces from the hand-written runtime:

- CLI logic moved onto `SpiritNextCli { arguments }`.
- daemon CLI logic moved onto `SpiritNextDaemonCli { arguments }`.
- daemon runtime moved onto `Daemon { configuration }`.
- socket I/O moved onto `SignalTransport<Stream> { stream }`.
- configuration block reading moved onto `ConfigurationText { block }`.

`fn main()` remains the only module-level production free function.

## Tests

All checks are Nix checks.

- `schema-next`: `nix flake check` passed.
- `schema-rust-next`: `nix flake check` passed.
- `spirit-next`: `nix flake check` passed.

The most important new constraints:

- `schema-next-declarative-schema-macros` requires the declarative macro file,
  `$Name`, `$*Fields`, expanded-template witnesses, and absence of old Rust-only
  struct/enum macro types.
- `schema-next-namespace-braces-are-key-value` requires the explicit rejection
  test for parenthesized namespace entries, rejects the old
  `NamedTypeDefinition` compatibility branch, and rejects parenthesized
  namespace entries in the shipped schema files.
- `schema-rust-next-generated-no-free-functions` rejects generated module-level
  free functions.
- `spirit-next-no-production-free-functions` rejects production module-level
  free functions except `main`.
- `spirit-next-generated-at-build-time` requires the build script to exercise
  the declarative macro names before Rust emission.
- `schema-next-schema-module-entrypoint` proves a package loader can read a
  crate-style `schema/lib.schema`.
- `schema-rust-next-generated-schema-module-path` proves colon-qualified
  schema identities map to generated Rust module paths.
- `spirit-next-schema-lib-entrypoint` requires the Spirit pilot to load
  `schema/lib.schema` through `SchemaPackage` and include the generated
  `schema/lib.rs` module artifact.

## Remaining gaps

The macro system is now real enough to prove schema-authored struct/enum
expansion, but it is still the bootstrap slice.

- Root-file shape is still Rust-known: imports/input/output/namespace are not
  themselves declared by declarative macro definitions yet.
- `schema/lib.schema` is real, but sibling imports are not yet transitively
  loaded from declarations inside that file.
- Cross-crate import resolution by crate name is still future work.
- Generated Rust mirrors a schema module path under Cargo `OUT_DIR`; a
  reviewable development-mode `src/schema/` emission target and watch hook are
  not implemented yet.
- Macro definitions are loaded from a built-in macro file, not from a schema
  daemon or content-addressed macro library.
- The template assembler recognizes a small assembled vocabulary:
  `Type`, `Struct`, `Enum`, `Fields`, and `Variants`.
- No schema diff/upgrade derivation is implemented yet.
- `spirit-next` still has in-memory SEMA storage; no redb durability.

The next useful implementation target is to move one level lower: make the root
schema/bootstrap file describe which root positions accept macro expansion,
then have `SchemaEngine` build its default macro registry from that bootstrapped
core description instead of directly calling `DeclarativeMacroLibrary::builtin`.
