# 395 — Standard generated newtype impls proposal branch

## Branch

Implemented and pushed a proposal branch:

- repo: `/git/github.com/LiGoldragon/schema-rust-next`
- bookmark: `operator/standard-newtype-impls`
- commit: `f265aad6` — `schema-rust-next: demonstrate schema-implied newtype trait impls`
- basis: schema-rust-next main `0a7d1db2`

## Research result

The common repeatable pattern is not "many arbitrary std methods." The safe recurring class is
**payload delegation from schema newtypes**:

- string/path newtypes: display, `AsRef<str>`, compare to `&str`;
- integer newtypes: display, compare/order against `u64`;
- boolean newtypes: display, compare against `bool`;
- wrapper/result newtypes: `Deref` to payload, already common in `signal-spirit` and `spirit`.

Examples in live code:

- `signal-spirit` manually implements `Display` for `RecordIdentifier`, `StashHandle`,
  `CommitSequence`.
- `signal-spirit` manually implements `PartialEq<&str>` for text newtypes and
  `PartialEq<u64>` / `PartialOrd<u64>` for count/token newtypes.
- `signal-spirit` and `spirit` carry many payload `Deref` impls for wrapper newtypes.

These are standard implementations because the schema shape plus scalar payload fully
determines the method body. They do not require a std-method allowlist or a general
composition interpreter.

## What the branch demonstrates

Added an opt-in emission knob:

- `RustEmissionOptions::with_standard_newtype_impls()`

When enabled, scalar-backed newtypes emit:

- `Display` for `String`, `Path`, `Integer`, and `Boolean` payloads;
- `AsRef<str>` and `PartialEq<&str>` for `String` / `Path` payloads;
- `PartialEq<u64>` and `PartialOrd<u64>` for `Integer` payloads;
- `PartialEq<bool>` for `Boolean` payloads.

It intentionally does **not** emit those impls for a newtype over another schema type. In the
fixture, `WrappedName NameText` gets `new`/`payload`/`into_payload`/`From`, but no scalar
standard impls.

## Tests

Green:

- `SCHEMA_RUST_NEXT_UPDATE_FIXTURES=1 cargo test --test standard_newtype_impls`
- `cargo test --test standard_newtype_impls`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`

The test fixture compiles generated Rust and exercises the impls at runtime:

- `NameText::new("schema").to_string()`
- `NameText::as_ref()`
- `NameText == "schema"`
- `FilePath == "/tmp/schema.nota"`
- `Count == 42`
- `Count > 10`
- `Enabled == true`

## Proposal

Treat scalar newtype trait impls as the first concrete "methods we can take as given." They
are stronger than a method allowlist because the receiver shape proves the body:

- the receiver is a newtype;
- the payload is one of the closed scalar leaves;
- the generated impl only delegates to that payload.

This should land before broader method-body composition. It deletes real boilerplate while
keeping the schema language small.

## Next gates

1. Decide whether the option should remain explicit or become the default for wire-contract
   emission.
2. Add `Deref` as a schema-implied standard impl for selected newtype categories, probably
   through explicit schema data rather than all newtypes.
3. Add enum/variant rewrap generation separately; that is the class that needs composition
   or `VariantMatch`, not scalar newtype traits.
4. Avoid a broad std leaf registry until these shape-proven impls and variant rewraps are
   exhausted.
