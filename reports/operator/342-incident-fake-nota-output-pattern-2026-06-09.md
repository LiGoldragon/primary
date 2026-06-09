# Incident: Fake NOTA Output Pattern

## Trigger

While adding `spirit-migrate-production`, I manually implemented:

```rust
impl NotaEncode for ProductionMigrationCompleted {
    fn to_nota(&self) -> String {
        format!("(ProductionMigrationCompleted {})", self.record_count)
    }
}
```

The psyche correctly flagged this as false NOTA: "nota encodes types". The string was a display convention that looked like a typed NOTA object but was not derived from a real decodable codec shape.

## What Was Wrong

The bad implementation violated the codec boundary in two ways.

First, it invented a type label by hand. A printed NOTA head such as `ProductionMigrationCompleted` must correspond to a real type/variant shape the codec owns. If the value cannot be parsed back by the corresponding typed codec surface, the output is not honest NOTA.

Second, it hid a formatting decision inside an implementation that looked type-safe from the outside. The test initially matched the string exactly, which made the fake shape look intentional instead of proving decodeability.

## Corrected Shape

The corrected code introduces a real typed output enum:

```rust
#[derive(Debug, Clone, PartialEq, Eq, NotaDecode, NotaEncode)]
pub enum ProductionMigrationOutput {
    Completed(ProductionMigrationCompleted),
}
```

The binary now prints:

```rust
ProductionMigrationOutput::completed(completed).to_nota()
```

The test now parses stdout back through:

```rust
NotaSource::new(stdout.trim()).parse::<ProductionMigrationOutput>()
```

That makes the invariant falsifiable: the tool output is accepted only if it is real typed NOTA.

## Audit Pattern

Future cross-repo audit should search for these patterns:

- Manual `impl NotaEncode` blocks that contain `format!`, `push_str`, `write!`, or handcrafted delimiter text.
- Tests that assert a NOTA-looking stdout string but do not parse it back through `NotaDecode`.
- CLI or migration tools that print a named result shape without a corresponding enum/struct deriving or honestly implementing `NotaDecode`.
- `to_string()` / `Display` implementations used as if they were codec output.
- Ad hoc helpers named like `to_nota`, `render_nota`, `nota_text`, or `format_nota` outside the NOTA codec layer or generated schema code.

Not every manual `NotaEncode` implementation is automatically wrong. The legitimate case is a narrow value type whose NOTA representation is its actual codec contract and whose decode path is pinned too. But a type label must not be invented only at output time.

## Immediate Fix Status

Fixed in `spirit` by replacing the fake completion encoder with the real `ProductionMigrationOutput` enum and decode-backed test.

Fixed adjacent NOTA replay risk in `nota-next`: pipe-square string text now supports longer fences such as `[||...||]`, so bracket-bearing strings containing `|]` encode losslessly instead of being mutated.

## Verification

At the time of this report:

- `nota-next`: `cargo test --all-features` passed; `cargo clippy --all-features --all-targets -- -D warnings` passed.
- `spirit`: `cargo test --all-features` passed; `cargo clippy --all-features --all-targets -- -D warnings` passed.
- `spirit` production-copy sandbox: `SPIRIT_PRODUCTION_DATABASE="$HOME/.local/state/persona-spirit/v0.5.2/persona-spirit.redb" cargo test --all-features --test production_database_sandbox -- --ignored --test-threads=1` passed all three ignored tests, including the real `spirit-migrate-production` binary witness.
