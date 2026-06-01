# Single-Field Wrapper Comparison With Designer 448

*Kind: comparison · Topics: rust-craft, nota-next, wrapper-types, designer-448 · 2026-06-01 · operator lane*

## Shared Conclusion

Designer 448 and operator 269 agree on the main question:
`CodecDerive { input: DeriveInput }` is valid.

The core reason is the same in both reports: `DeriveInput` is owned by
the `syn` crate, so `nota-next` cannot add inherent methods to it. The
wrapper is a local data-bearing noun that hosts `expand_decode`,
`expand_encode`, and `expand` without falling back to free functions,
one-impl extension traits, or zero-sized namespace holders.

## Useful Designer Addition

Designer 448 gives a broader taxonomy than operator 269:

- orphan-rule wrappers;
- named collection containers;
- semantic distinction newtypes;
- growth-anticipation attribute parsers;
- internal builder/parser/CLI state;
- typestate phase data.

That taxonomy is useful. Operator 269's shorter validity test maps
cleanly onto it. The phrasing I would keep for implementation review:
the question is not "does it have one field?" but "what new noun did it
create, and what methods or trait impls does that noun own?"

## Concrete Disagreement

Designer 448 says:

> None of the audited types are ZSTs; every one carries non-empty data.

That statement is true for the 28 single-field wrappers designer listed,
but it misses an adjacent production type in the exact file that prompted
the audit:

```rust
struct FieldEncode;

impl FieldEncode {
    fn body_named(field: &Field) -> Result<TokenStreamTwo, Error> { ... }
}
```

File:

- `/git/github.com/LiGoldragon/nota-next/derive/src/lib.rs`

`FieldEncode` is not a single-field wrapper. It is a zero-sized method
holder. That makes it worse than the suspicious pattern, because it owns
no data while hosting behavior. It should not be used as evidence against
`CodecDerive`; it should be cleaned up separately.

## Preferred Cleanup

Mirror the existing `FieldDecode` shape:

```rust
struct FieldEncode<'field> {
    field: &'field Field,
}

impl<'field> FieldEncode<'field> {
    fn new(field: &'field Field) -> Self {
        Self { field }
    }

    fn body_named(&self) -> Result<TokenStreamTwo, Error> {
        ...
    }
}
```

Then call:

```rust
.map(|field| FieldEncode::new(field).body_named())
```

This turns the encode side into the same kind of real workflow object as
`FieldDecode { index, field }`. It keeps the method-only discipline
without a ZST namespace.

## Operator Position

Adopt designer 448's taxonomy, with one added review check:

> After validating single-field wrappers, also grep for zero-sized method
> holders in the same area. A valid wrapper pattern can coexist with a ZST
> anti-pattern nearby.

The immediate code conclusion remains:

- keep `CodecDerive`;
- fix `FieldEncode` when touching `nota-next/derive`.
