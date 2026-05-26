# 203 — Schema-next interface implementation

## Frame

This pass implements the first concrete double-implementation baseline after
reviewing designer critiques `/359`, `/360`, `/361`, `/362`, the mid-flight
inspection `/364`, and the implementation engagement `/365`.

The closed repo decisions from Spirit records 819-821 are now reflected in
code:

- `nota-next` is the new NOTA implementation.
- `schema-next` is the new schema engine and assembled-schema repo.
- `schema-rust-next` is the Rust source emission repo.
- The three are separate repositories from the start.

Record 822 is carried as future design: forge may eventually turn generated
Rust into content-addressed crates, but the current implementation keeps an
explicit `schema-rust-next` source-emission repo.

## Designer critiques applied

The implementation applies these concrete critiques:

- From `/359`: keep NOTA as structural methods, not schema semantics.
- From `/360`: preserve declaration order with `Vec`, not a canonical map.
- From `/360` and `/362`: pass `MacroPosition` into lowering, not just shape
  matching.
- From `/361`: separate NOTA, schema macro engine, assembled schema, and Rust
  emission into layers.
- From `/362`: do not let the old signal macro be an implementation path.
- From `/364`: make the recursion floor visible in code documentation and
  seal canonical assembled-schema fields behind accessors.
- From `/365`: scope the `BTreeMap` constraint to canonical assembled-schema
  storage rather than banning legitimate derived indexes everywhere.

## Repositories created

| Repository | Local path | Remote | Commit |
|---|---|---|---|
| `nota-next` | `/git/github.com/LiGoldragon/nota-next` | `https://github.com/LiGoldragon/nota-next` | `6b4364d9` |
| `schema-next` | `/git/github.com/LiGoldragon/schema-next` | `https://github.com/LiGoldragon/schema-next` | `19591a7a` |
| `schema-rust-next` | `/git/github.com/LiGoldragon/schema-rust-next` | `https://github.com/LiGoldragon/schema-rust-next` | `f76d6483` |

Each repo has:

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `INTENT.md`,
  `ARCHITECTURE.md`;
- `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `flake.nix`;
- Nix checks on `main`;
- an operator-owned `main` baseline pushed to GitHub.

`repos/nota-next`, `repos/schema-next`, and `repos/schema-rust-next`
symlinks were added locally for workspace navigation.

## `nota-next` interfaces

Main public types:

```rust
pub struct Document;
pub enum Block;
pub enum Delimiter;
pub struct Atom;
pub enum AtomClassification;
pub struct SourceSpan;
pub struct SourcePosition;
pub enum NotaError;
```

Important methods:

```rust
Document::parse(source)
document.root_objects()
document.holds_root_objects()
document.root_object_at(index)

block.is_parenthesis()
block.is_square_bracket()
block.is_brace()
block.is_pipe_text()
block.holds_root_objects()
block.root_object_at(index)
block.reemit(source)
block.qualifies_as_symbol()
block.qualifies_as_pascal_case_symbol()
block.qualifies_as_camel_case_symbol()
block.qualifies_as_kebab_case_symbol()
block.demote_to_string()
```

Design intent applied:

- The crate docs explicitly mark `nota-next` as the hand-authored recursion
  floor. That implements `/364`'s critique that the floor should be
  witness-able in code, not only in reports.
- `is_*` means factual delimiter/source state.
- `qualifies_as_*` means structural candidate, not semantic identity.
- Pipe text `[|...|]` is preserved as square-bracket-safe text and is not
  recursively parsed.
- The parser records source spans for later macro diagnostics.

Tests:

- ordered root parsing and source re-emission;
- recursive shape predicates;
- atom classification candidates;
- pipe-text safety;
- unclosed delimiter diagnostics.

Verification:

- `cargo test` passed.
- `cargo fmt -- --check` passed.
- `nix flake check` passed.

## `schema-next` interfaces

Main assembled schema types:

```rust
pub struct Asschema {
    identity: SchemaIdentity,
    imports: Vec<ImportDeclaration>,
    surfaces: Vec<RootSurface>,
    namespace: Vec<TypeDeclaration>,
}

pub enum TypeDeclaration {
    Struct(StructDeclaration),
    Enum(EnumDeclaration),
    Newtype(StructDeclaration),
}
```

Canonical vectors are private and exposed through read-only accessors:

```rust
asschema.identity()
asschema.imports()
asschema.surfaces()
asschema.namespace()
asschema.type_named("Entry")
```

That implements `/364`'s field-visibility critique: external crates can read
the ordered assembled tree, but cannot directly mutate canonical vectors.

Position-aware macro interface:

```rust
pub trait SchemaMacro {
    fn name(&self) -> &'static str;
    fn matches(&self, object: &Block, position: MacroPosition) -> bool;
    fn lower(
        &self,
        object: &Block,
        position: MacroPosition,
        context: &mut MacroContext,
    ) -> Result<MacroOutput, SchemaError>;
}
```

The MVP schema shape is:

```nota
{}
[
  (Input (Record Entry) (Observe Query))
  (Output (RecordAccepted RecordIdentifier) (RecordsObserved RecordSet))
]
{
  Topic [Text]
  Entry [Topics Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
}
```

Delimiter discipline:

- `{}` is the root import/export or namespace map.
- `[]` is struct fields.
- `()` is enum/variant declaration.

Tests:

- Spirit-like schema lowers into ordered `Asschema`;
- square brackets lower into structs and parentheses lower into enums;
- a probe macro proves `MacroPosition` reaches `lower`;
- field names are derived from type names.

Nix constraints:

- `no-btree-canonical`: `BTreeMap` is rejected in the canonical
  assembled-schema storage module. `/365` flagged the original check as too
  broad because derived-index methods can legitimately return sorted maps; the
  check now targets the canonical storage file.
- `no-authored-features`: retracted authored features
  `EffectTable`, `FanOutTargets`, `StorageDescriptor`, and `Features` are
  rejected.

Verification:

- `cargo test` passed.
- `cargo fmt -- --check` passed.
- `nix flake check` passed.

## `schema-rust-next` interfaces

Public emission surface:

```rust
pub struct RustEmitter;
pub struct RustCode;
pub struct GeneratedFile {
    pub path: String,
    pub code: RustCode,
}
```

Primary flow:

```rust
let asschema = SchemaEngine::default().lower_source(source, identity)?;
let generated = RustEmitter::default().emit_file(&asschema);
```

Current generated Rust includes:

- newtypes;
- structs;
- enums;
- root surface enums;
- rkyv archive/serialize/deserialize derives on generated data types;
- NOTA `FromStr` / `Display` / `to_nota` / `from_nota_block` surfaces for
  generated data types;
- short-header constants derived from surface and variant order.

The emitted Spirit fixture includes:

```rust
pub enum Input {
    Record(Entry),
    Observe(Query),
}

pub enum Output {
    RecordAccepted(RecordIdentifier),
    RecordsObserved(RecordSet),
}

pub mod short_header {
    pub const INPUT_RECORD: u64 = 0x0000000000000000;
    pub const INPUT_OBSERVE: u64 = 0x0001000000000000;
    pub const OUTPUT_RECORD_ACCEPTED: u64 = 0x0100000000000000;
    pub const OUTPUT_RECORDS_OBSERVED: u64 = 0x0101000000000000;
}
```

Tests:

- emit Rust source from a schema and assert it contains the generated
  interface surfaces;
- compile and use the checked-in fixture as Rust code;
- parse a CLI-style NOTA string into generated `Input` and emit it back as
  NOTA;
- round-trip a generated `Input` value from NOTA into rkyv bytes and back.

Nix constraints:

- `no-old-signal-macro`: generated-emission repo must not use
  `signal_channel!`.
- `no-rust-macro-surface`: `src/` must not define `macro_rules!` or
  `proc_macro`; Rust emission stays separate from Rust macros.
- `generated-rkyv-boundary`: the generated fixture carries rkyv derives
  and the test suite exercises `rkyv::to_bytes` / `rkyv::from_bytes`.
- `generated-nota-boundary`: the generated fixture carries `FromStr` and
  `to_nota`, and the test suite parses a CLI-style NOTA string into
  generated `Input`.

Verification:

- `cargo test` passed.
- `cargo clippy --all-targets -- -D warnings` passed.
- `nix flake check` passed.

## What this proves

This is not full schema self-hosting yet, but it proves the intended interface
chain is real:

```text
NOTA source
  -> nota-next Document/Block
  -> schema-next SchemaEngine + position-aware macros
  -> schema-next ordered Asschema
  -> schema-rust-next Rust source emission
  -> compiled Rust fixture with NOTA + rkyv boundaries
```

The chain uses the new layers directly. It does not route through the old
signal macro.

## Known limits

- `nota-next` is a structural floor; it does not yet encode every future NOTA
  parse edge case.
- `schema-next` has only the built-in MVP lowering surface; third-party macro
  registration is still a follow-on.
- `schema-rust-next` emits source code with rkyv derives and basic NOTA
  readers/writers, but not version-projection traits or full signal
  client/server code yet.
- Header derivation is currently a simple surface-index plus variant-index
  encoding. The deeper 64-bit header namespace plan still needs expansion.
- `schema-rust-next` consumes `schema-next` by Git dependency on `main`; as
  the stack matures, forge/content-addressed generated crates may replace
  that dependency pattern.

## Next implementation slice

The next useful slice is to extend `schema-rust-next` from "data types +
headers" to "wire contract module":

- generated request/reply envelopes;
- generated short-header dispatch table;
- one generated compatibility trait pair for an adjacent schema diff.

That should stay in `schema-rust-next` until the code-generation interface is
stable enough to generate a first `signal-spirit` contract.
