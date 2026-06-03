# schema-rust-next Alias Patch Plan

## Scope

Task scope was `/git/github.com/LiGoldragon/schema-rust-next`, limited to
`src/lib.rs`, tests, and generated fixtures. The requested behavior is:

- bare namespace bindings such as `Rejected SignalRejection` lower through
  `schema_next::TypeDeclaration::Alias`;
- Rust emission writes `pub type Rejected = SignalRejection;`;
- aliases do not get tuple-newtype helpers;
- genuine newtypes still come from single-field struct-body declarations and
  keep `new`, `payload`, `into_payload`, and `From<Payload>`;
- enum associated constructors do not wrap aliases as newtypes;
- keyword-safe constructor names such as `continue` -> `r#continue` stay
  preserved.

## Current Blocker

Direct editing is blocked in the checked-in dependency state. `Cargo.lock`
currently pins `schema-next` to:

`6b34fa93587645af6a380e36621b14793c18f58b`

Against that pinned dependency, `cargo test --test emission
emitter_builds_rust_module_data_before_rendering_text -- --nocapture` failed
as soon as `schema-rust-next/src/lib.rs` imported `AliasDeclaration` and
matched `TypeDeclaration::Alias`:

```text
error[E0432]: unresolved import `schema_next::AliasDeclaration`
error[E0599]: no variant or associated item named `Alias` found for enum `TypeDeclaration`
```

The local `/git/github.com/LiGoldragon/schema-next` checkout does contain the
target shape:

- `src/asschema.rs`: `TypeDeclaration::Alias(AliasDeclaration)`
- `src/asschema.rs`: `AliasDeclaration { pub name: Name, pub reference:
  TypeReference }`
- `src/source.rs`: bare source references lower to
  `TypeDeclaration::Alias(AliasDeclaration::new(...))`

So the patch should land after the `schema-rust-next` dependency is repinned
to a `schema-next` revision that exports the alias type.

## Source Patch

In `schema-rust-next/src/lib.rs`:

1. Import `AliasDeclaration` from `schema_next`.
2. Add `RustTypeDeclaration::Alias(RustAlias)`.
3. Add a data-bearing `RustAlias`:

```rust
pub struct RustAlias {
    name: Name,
    reference: TypeReference,
}
```

with `from_asschema_alias`, `name`, and `reference` methods.

4. In `RustTypeDeclaration::from_asschema_type`, add the
   `TypeDeclaration::Alias` arm.
5. In `RustWriter::emit_type`, add the alias arm before struct/newtype/enum.
6. Add `RustWriter::emit_alias`:

```rust
fn emit_alias(&mut self, visibility: Visibility, declaration: &RustAlias) {
    self.line(format!(
        "{} type {} = {};",
        self.rust_visibility(visibility),
        declaration.name(),
        self.rust_type(declaration.reference())
    ));
}
```

This emits `pub type ...` for public aliases and `pub(crate) type ...` for
private aliases.

7. Leave `emit_newtype_inherent_impls` and `emit_enum_variant_constructors`
   collecting only `RustTypeDeclaration::Newtype`. This is the important
   behavioral guard: aliases are not in the newtype lookup table, so an enum
   variant whose payload is `Rejected` emits `Self::Rejected(payload)`, not
   `Rejected::new(payload)`.
8. In `CollectionScan`, handle `TypeDeclaration::Alias` by recursing over the
   alias reference. Aliases themselves do not need derives, but an alias such
   as `Bindings (Map (Topic Entry))` still makes `Topic` a map key.
9. Replace wildcard matches over `RustTypeDeclaration` where practical so a
   future declaration variant creates an obvious compile failure.

## Focused Tests

Add a small alias-specific fixture under `tests/fixtures/`, rather than relying
only on the large Spirit fixtures. Suggested schema:

```schema
[(Reject Rejected) (Continue ContinuePayload)]
[]
{
  SignalRejection { reason String }
  Rejected SignalRejection
  ContinuePayload { String * }
}
```

Then add one focused test in `tests/emission.rs`:

- `Rejected` is `RustTypeDeclaration::Alias` with reference
  `TypeReference::Plain(SignalRejection)`.
- `ContinuePayload` is `RustTypeDeclaration::Newtype`.
- generated source contains `pub type Rejected = SignalRejection;`.
- generated source does not contain `pub struct Rejected`, `impl Rejected`,
  or `Rejected::new(payload)`.
- generated source contains `pub fn reject(payload: Rejected) -> Self` and
  `Self::Reject(payload)`.
- generated source contains `pub fn r#continue(payload: String) -> Self` and
  `ContinuePayload::new(payload)`.

That single test covers alias lowering, real-newtype helper preservation,
enum constructor non-wrapping for aliases, and the reserved-keyword constructor
fix.

## Fixture Sweep

Once the dependency is repinned, existing fixture outputs will change because
many current test schemas use bare bindings that previously acted like
newtypes:

- `tests/fixtures/spirit-min.schema`: `Topic String`, `Description String`,
  `RecordIdentifier Integer`, and similar declarations become aliases.
- `tests/fixtures/collections.schema`: `NodeName String`, `NodeConfig String`,
  `Service String`, `Query Topic`, and `Topic String` become aliases.
- `tests/fixtures/plane-triad.schema` and the big schemas have many scalar
  aliases that will lose tuple-newtype helper blocks.

For each fixture, choose explicitly:

- If the type should be a real wrapper with helper methods, change the schema
  declaration to a single-field struct body such as `Topic { String * }`.
- If the type should be an alias, update tests and expected generated source
  to use the alias directly and remove helper expectations.

After the source patch and test assertions are adjusted, regenerate checked-in
generated fixtures with the repository's existing update path:

```sh
SCHEMA_RUST_NEXT_UPDATE_FIXTURES=1 cargo test --test emission
```

Then run:

```sh
cargo test
```

or the repo's Nix check once the lockfile is allowed to move.

## Current Working Tree Note

`schema-rust-next/src/lib.rs` already has the keyword-safe constructor fix in
the working tree. I preserved it and did not leave the direct alias patch in
place because it cannot compile against the locked `schema-next` revision.
