# Mainline schema IR Help integration

schema-operator report 8. The psyche asked operator to do the
designer-recommended collapse of Help onto the schema IR along with the
designer lane, before broadening beyond Spirit.

## Result

The schema-IR Help stack is now integrated on `main` across the producer
chain and the Spirit pilot:

- `nota-next` main: `4642807e4030`
- `schema-next` main: `9219e32995bc`
- `schema-rust-next` main: `e4ac3baf3712`
- `signal-spirit` main: `99edb4873abb`

The integration uses the designer `schema-ir` branches as executable
evidence, but the accepted artifact is now the operator mainline merge.

## What Landed

`nota-next` main now carries the decoder-driven per-instance schema trait
and derive surface used by generated contracts:

- `NotaDecodeTraced`
- `InstanceSchema`
- `InstanceSchemaBody`
- `TypeReference`

`schema-next` main now carries the schema codec / source IR surfaces that
Help and instance-schema share:

- `SourceDeclaration` / `SourceDeclarations` schema text codec
- block-level declaration decode entry points
- instance-schema reference rendering through schema-next
- `SourceReference::plain_name`
- canonical `Vector` behavior; no `Vec` alias resurrection

`schema-rust-next` main now emits the traced decoder surface used by
`signal-spirit` instance-schema tests, with dependency pins updated to
producer `main`.

`signal-spirit` main now has the actual Spirit pilot:

- `src/help.rs` is a schema IR Help view, not a parallel Help AST.
- `HelpBody`, `HelpTypeExpression`, `HelpFieldTypes`,
  `HelpVariantTypes`, and `HelpTypeExpressions` are gone.
- Help text encode/decode goes through schema-next declaration codec.
- `schema/signal.schema` and `schema/domain.schema` use `(Vector T)`.
- `tests/help_instance_schema_convergence.rs` proves Help and
  per-instance schema project the same `SourceReference` for `Domains`.
- Branch-local `[patch]` path entries were removed; `signal-spirit`
  points at producer `main` branches.

## Merge Notes

`schema-next`, `schema-rust-next`, and `nota-next` were fast-forward
producer integrations plus main-pin cleanup.

`signal-spirit` was merged from current `main` plus designer `schema-ir`.
The only real conflict was generated `src/schema/signal.rs`, where current
main had `AuthorizationMode` and schema-ir had regenerated Help /
instance-schema artifacts. I resolved that by regenerating from
`schema/signal.schema` with:

```console
SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text
```

That preserved the `AuthorizationMode` schema source and regenerated the
checked Rust artifact rather than hand-editing generated code.

## Test Gates

Producer tests:

```console
cd /git/github.com/LiGoldragon/nota-next
cargo test
```

Passed.

```console
cd /git/github.com/LiGoldragon/schema-next
cargo test
```

Passed after switching `nota-next` pins to `branch = "main"`.

```console
cd /git/github.com/LiGoldragon/schema-rust-next
cargo test
```

Passed after switching `nota-next` and `schema-next` pins to
`branch = "main"`.

Spirit contract tests:

```console
cd /git/github.com/LiGoldragon/signal-spirit
SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text
cargo fmt --check
cargo test
cargo test --features nota-text
```

All passed.

The `nota-text` Spirit suite covered:

- daemon configuration: 4 passed
- dependency boundary: 2 passed
- generated contract: 16 passed
- Help / instance-schema convergence: 3 passed
- instance schema: 10 passed
- validation: 3 passed

The default Spirit suite still keeps Help and schema-next out of the
daemon dependency surface: `dependency_boundary` passes with default
features.

## Current Status

Mainline is ready for the designer audit. The next broadening step is
mentci or another signal contract consuming the same producer mains;
that work should not create a second Help tree. It should provide the
embedded schema source and call the shared schema-codec/IR projection
surface.

The earlier struct-field syntax question is intentionally not resolved in
this report. That is a separate schema-next syntax/codec task.
