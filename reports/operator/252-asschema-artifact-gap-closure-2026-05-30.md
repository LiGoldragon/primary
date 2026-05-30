# 252 — Asschema Artifact Gap Closure

*Kind: implementation report · Topics: schema, asschema, rust emission, spirit-next · 2026-05-30 · operator lane*

## What Closed

Report 251 named the immediate gap correctly: `Asschema` could round-trip
through NOTA and rkyv, but the lowerer-to-emitter handoff was still a private
in-memory value. That gap is now closed across the active stack.

`schema-next` now owns the artifact noun:

```rust
pub struct AsschemaArtifact {
    asschema: Asschema,
}

impl AsschemaArtifact {
    pub fn read_nota_file(path: impl AsRef<Path>) -> Result<Self, SchemaError>;
    pub fn write_nota_file(&self, path: impl AsRef<Path>) -> Result<(), SchemaError>;
    pub fn read_binary_file(path: impl AsRef<Path>) -> Result<Self, SchemaError>;
    pub fn write_binary_file(&self, path: impl AsRef<Path>) -> Result<(), SchemaError>;
}
```

`schema-rust-next` now accepts that artifact surface:

```rust
impl RustEmitter {
    pub fn emit_file_from_artifact(&self, artifact: &AsschemaArtifact) -> GeneratedFile;
    pub fn emit_file_from_nota_path(&self, path: impl AsRef<Path>) -> Result<GeneratedFile, SchemaError>;
    pub fn emit_file_from_binary_path(&self, path: impl AsRef<Path>) -> Result<GeneratedFile, SchemaError>;
}
```

`spirit-next/build.rs` now materializes assembled schema as files before Rust
emission:

```text
schema/lib.schema
  -> SchemaEngine::lower_source
  -> AsschemaArtifact
  -> OUT_DIR/lib.asschema
  -> OUT_DIR/lib.asschema.rkyv
  -> RustEmitter::emit_file_from_nota_path
  -> compare with src/schema/lib.rs
```

It also emits from the binary artifact and asserts that the generated Rust is
identical, so both serialized forms participate in the build witness.

## Tests

- `schema-next`: `cargo fmt && cargo test`
- `schema-rust-next`: `cargo fmt && cargo test`
- `spirit-next`: `cargo fmt && cargo test`
- `spirit-next`: `cargo test --no-default-features`
- `spirit-next`: `nix flake check`

The Nix check includes the generated-schema guard, the binary-only daemon
dependency guard, socket-negative tests, runtime triad checks, no-free-function
guard, and no-production-unit-struct guard.

## Commits

- `schema-next` `f1ded8f7` — `schema: add asschema artifact file IO`
- `schema-rust-next` `f7a56402` — `schema-rust: emit from asschema artifact files`
- `spirit-next` `5a51d7af` — `spirit: emit schema from serialized asschema artifacts`

## Remaining Gaps

The artifact handoff is now real. The remaining gaps are the larger frontiers:

- Macro-table-as-data is still not fully loaded from typed serialized asschema
  data.
- Rust emission still renders strings directly rather than flowing through a
  `RustModule` data model.
- Shared support nouns such as mail/core schema are still emitted locally
  instead of imported from a schema-core substrate.
- Schema diff/upgrade remains future work.

