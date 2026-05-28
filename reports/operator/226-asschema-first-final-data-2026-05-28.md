# 226 — ASSchema First: Final Data Before Sugar

## Frame

Psyche correction applied: define the assembled schema first. Authored
schema sugar and macros lower into `.asschema`; they are not the endpoint.
Square brackets remain NOTA vectors. In `.asschema`, a vector's meaning comes
from the known surrounding assembled-schema type and field position.

## What Changed

`schema-next` commit `6307e65a` (`schema: define asschema as final data`)
now makes the assembled endpoint explicit:

- Added `schemas/asschema.asschema`, a parsed `.asschema` document defining
  `Asschema`, `SchemaIdentity`, `TypeDeclaration`, `StructDeclaration`,
  `EnumDeclaration`, `Payload`, `TypeReference`, and `TypeReferencePair`.
- Added tests that parse that file through `Asschema::from_nota`.
- Added Nix guard `asschema-is-final-data`: `.asschema` files cannot contain
  `@` macro markers, `$` captures, or the old loose `Map` payload shape.
- Updated `Asschema::to_nota` / `from_nota` so final `Map` is a variant
  carrying one vector payload:

```nota
(Map [(Plain Topic) (Plain RecordIdentifier)])
```

not:

```nota
(Map (Plain Topic) (Plain RecordIdentifier))
```

`schema-rust-next` commit `f055c8e0`
(`schema-rust: consume final asschema data`) now consumes that endpoint:

- `Cargo.lock` points at `schema-next` `6307e65a`.
- Big `.asschema` fixtures use final `Map` vector payloads.
- Big emission tests reject macro markers, macro captures, and loose old
  `Map` syntax before comparing generated Rust.
- Nix guard `asschema-fixtures-final-data` enforces the same fixture rule.

## Real Endpoint Shape

The new canonical assembled-schema definition starts like this:

```nota
[
  [schema-next:asschema 0.1.0]
  []
  []
  [Input []]
  [Output []]
  [
    (Struct [Asschema [[identity (Plain SchemaIdentity)] [imports (Vector (Plain ImportDeclaration))] [resolved_imports (Vector (Plain ResolvedImport))] [input (Plain EnumDeclaration)] [output (Plain EnumDeclaration)] [namespace (Vector (Plain TypeDeclaration))]]])
    (Enum [TypeReference [[Plain (Carries (Plain Name))] [Vector (Carries (Plain TypeReference))] [Optional (Carries (Plain TypeReference))] [Map (Carries (Plain TypeReferencePair))]]])
    (Struct [TypeReferencePair [[key (Plain TypeReference)] [value (Plain TypeReference)]])
  ]
]
```

The first object is a vector. Its type is known by the file reader:
`SchemaIdentity`. The root object is also a vector. Its type is known by the
file reader: `Asschema`.

## Verification

`schema-next`:

```text
cargo fmt && cargo test
nix flake check --print-build-logs
```

Both passed. The Nix run included `schema-next-asschema-is-final-data`.

`schema-rust-next`:

```text
cargo fmt && cargo test
nix flake check --print-build-logs
```

Both passed. The Nix run included
`schema-rust-next-asschema-fixtures-final-data`.

## Remaining Gap

Macro definitions still need the same treatment next: a macro table should be
assembled as data first, serialized/deserialized, then loaded into the macro
registry. This pass fixed the endpoint language so future macro work has a
real target instead of lowering into a moving idea.
