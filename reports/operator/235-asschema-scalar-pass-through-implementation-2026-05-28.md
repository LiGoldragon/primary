# 235 - Asschema Scalar Pass-Through Implementation

Date: 2026-05-28  
Updated: 2026-05-29  
Lane: operator  
Scope: `schema-next` and `schema-rust-next`

## Summary

Implemented the settled part of the codec/asschema unification target:
reserved scalar references now live in asschema data before Rust emission.

The active scalar floor is:

```rust
pub enum TypeReference {
    String,
    Integer,
    Boolean,
    Plain(Name),
    Vector(Box<TypeReference>),
    Map(Box<TypeReference>, Box<TypeReference>),
    Optional(Box<TypeReference>),
}
```

`Plain(Name)` now means a declared or imported schema type. It no longer
secretly means scalar when `Name` happens to be `String` or `Integer`.
Per record 1151, `Bool` is not an accepted spelling, and `Text` is not a
reserved scalar floor right now. A schema may still declare `Text` as a normal
string newtype when it needs that domain noun.

## Code Landed

`schema-next` commit `1cbdf6d9` (`schema: add scalar type references to asschema`),
followed by commit `d6bf9a9b` (`schema: rename scalar text to string`):

- Added `TypeReference::{String,Integer,Boolean}`.
- Made bare reference atoms lower through `TypeReference::from_name`, so
  `String`, `Integer`, and `Boolean` become scalar data variants.
- Reserved scalar names at namespace declaration position.
- Updated `schemas/root.schema` so the schema-of-schema describes the scalar
  variants directly.
- Added tests proving scalar fields, nested scalar collections, and reserved
  scalar-name rejection.

`schema-rust-next` commit `a8a4f973`
(`schema-rust: emit scalar asschema references`), followed by commit `51490c2b`
(`schema-rust: emit string scalar floor`):

- Updated Rust emission to match scalar asschema variants directly.
- Added generated `Boolean = bool` plus `parse_boolean`.
- Removed scalar special casing from `Plain(Name)` emission.
- Added a Boolean field to the collection fixture so generated compiled Rust
  actually parses, formats, archives, and round-trips a scalar Boolean field.
- Regenerated checked Rust fixtures from the emitter.

## Proof

Local tests:

```text
schema-next: cargo test
schema-next: nix flake check --print-build-logs
schema-rust-next: cargo test
schema-rust-next: nix flake check --print-build-logs
```

All four passed.

The most relevant constraint tests are:

- `schema-next/tests/collections.rs`
  - `scalar_field_names_lower_to_reserved_references`
  - `scalar_references_nest_inside_collections`
  - `scalar_names_are_reserved_at_namespace_declaration_position`
- `schema-rust-next/tests/emission.rs`
  - `emits_vec_map_and_option_collection_types_with_runtime_codec`
  - `generated_collection_struct_round_trips_through_nota`

The second `schema-rust-next` test uses the generated `Cluster` type from
`tests/fixtures/collections.schema`; that schema now contains a real
`Boolean` field, and the generated fixture compiles and round-trips it.

## Still Open

This does not decide the two design forks from designer report 425:

- declaration delimiter policy: plain namespace `Entry [Topic Kind]` versus
  pipe-family declaration forms
- nesting model: multiple roots inside one asschema versus multiple schema
  files / schemas

It also does not yet implement the shared `nota-next` typed codec. Current
`schema-rust-next` still emits a local `NotaBlock` / `NotaDecodeError` support
surface. Report 234 remains accurate for that larger gap.
