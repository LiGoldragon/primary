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

## What changed

### `schema-next`

Commit: `d340433f` — `add declarative schema macro expansion`.

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

### `schema-rust-next`

Commit: `1268af75` — `consume four-root declarative schema engine`.

The Rust emitter now consumes the four-root `schema-next` API backed by the
declarative macro engine. It still emits Rust source as a file artifact before
compilation. The generated fixture is constrained to use data-bearing helper
objects instead of module-level helper functions.

New Nix constraints prove:

- production emitter source has no module-level free functions;
- production emitter source has no unit-struct method holder;
- generated Spirit fixture has no module-level free functions;
- the generated fixture uses `NotaSource` / `NotaBlock` helper objects, not the
  old `parse_nota_root` helper surface.

### `spirit-next`

Commit: `0a509e35` — `run spirit pilot on declarative schema macros`.

The runnable Spirit pilot now uses the current four-root schema shape:

```nota
{}
(Input ((Record Entry) (Observe Query)))
(Output ((RecordAccepted RecordIdentifier) (RecordsObserved RecordSet) (Error ErrorMessage)))
{
  (SemaCommand ((Record Entry) (Observe Query)))
  (SemaResponse ((Recorded RecordIdentifier) (Observed RecordSet) (Missed ErrorMessage)))
  (Entry [Topic Kind Description Magnitude])
  (Kind (Decision Principle Correction Clarification Constraint))
}
```

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
- `schema-rust-next-generated-no-free-functions` rejects generated module-level
  free functions.
- `spirit-next-no-production-free-functions` rejects production module-level
  free functions except `main`.
- `spirit-next-generated-at-build-time` requires the build script to exercise
  the declarative macro names before Rust emission.

## Remaining gaps

The macro system is now real enough to prove schema-authored struct/enum
expansion, but it is still the bootstrap slice.

- Root-file shape is still Rust-known: imports/input/output/namespace are not
  themselves declared by declarative macro definitions yet.
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
