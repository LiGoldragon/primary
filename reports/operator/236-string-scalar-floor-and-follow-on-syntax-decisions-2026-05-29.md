# 236 - String Scalar Floor and Follow-On Syntax Decisions

Date: 2026-05-29  
Lane: operator  
Repos: `schema-next`, `schema-rust-next`

## Intent Captured

Designer had not yet captured the forwarded scalar decision, so I gap-filled
record 1151:

```text
String, Integer, and Boolean are the scalar floor. Bool is not allowed. Text is
not required as a scalar floor right now; String works.
```

The later forwarded exchange also carried two durable syntax decisions, and no
recent Spirit record held them. I gap-filled them as records 1153 and 1154:

```text
Type declarations belong to schema, not to raw NOTA. Schema declarations should
live in the pipe-family forms for struct, enum, and newtype declaration.
```

```text
Roots are declared only at the schema root position. Nesting does not add more
roots to a schema; nested things are namespace datatypes used by roots.
```

The follow-up composite/scalar boundary decision landed as record 1156:

```text
NOTA owns raw delimiter structure and serialization shapes, plus the value
literal None with present values as (Some x). Schema owns the entire type-name
vocabulary: scalar names such as String, Integer, Boolean, and future scalar
names, and composite names such as Vec, Optional, Map, and future composite
names.
```

Those two are follow-on syntax constraints. I did not mix the full pipe-family
declaration migration into this scalar rename because the repo currently has a
large plain-bracket lowering surface and that change deserves its own coherent
pass.

## Implemented Now

`schema-next` now treats the reserved scalar floor as real assembled-schema
data:

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

`String`, `Integer`, and `Boolean` are reserved at namespace declaration
positions. `Text` is no longer reserved; it can be declared as a normal user
newtype later if a schema wants the domain noun.

`schema-rust-next` emits the same scalar floor into generated Rust:

```rust
pub type String = std::string::String;
pub type Integer = u64;
pub type Boolean = bool;
```

Generated NOTA support now uses `parse_string` and `NotaString`, not
`parse_text` and `NotaText`. All checked-in generated fixtures were
regenerated from real `.schema` inputs.

## Proof

The tests exercise the renamed scalar through lowering, witness snapshots,
generated Rust, NOTA round-trips, rkyv round-trips, and Nix builds.

```text
schema-next:
  cargo test
  nix flake check --print-build-logs

schema-rust-next:
  cargo test
  nix flake check --print-build-logs
```

All four passed.

Important proof points:

- `schema-next/tests/collections.rs` asserts `String`, `Integer`, and
  `Boolean` lower to scalar `TypeReference` variants and reject scalar-name
  declarations.
- `schema-next/tests/big_examples.rs` regenerates and checks large witness
  snapshots with `newtype Topic = String`, not `Text`.
- `schema-rust-next/tests/emission.rs` compiles generated Rust and round-trips
  generated objects through NOTA and rkyv.
- `schema-rust-next/tests/big_emission.rs` regenerates large Rust fixtures from
  `.schema` files and compiles the large generated Spirit surface.

## Commits

- `schema-next` `d6bf9a9b` - `schema: rename scalar text to string`
- `schema-rust-next` `51490c2b` - `schema-rust: emit string scalar floor`

## Next Syntax Pass

The next implementation pass should address records 1153, 1154, and 1156
directly:

- authored datatype declarations should move from plain namespace bodies like
  `Topic [String]` toward pipe-family declaration forms;
- root input/output positions remain the only schema root declarations;
- nested structs/enums/newtypes are namespace datatypes referenced from those
  roots, not extra roots;
- Schema docs and code should call `String`, `Integer`, `Boolean`, `Vec`,
  `Optional`, and `Map` Schema type-reference vocabulary, while NOTA docs call
  `[]`, `{}`, `None`, and `(Some x)` value serialization shapes;
- tests should keep real `.schema` files as input and compare both lowered
  `Asschema` data and emitted Rust.
