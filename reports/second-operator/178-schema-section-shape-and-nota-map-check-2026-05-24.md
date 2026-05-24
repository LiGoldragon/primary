*Kind: Implementation Report · Topic: schema section correction + NOTA map check · Date: 2026-05-24 · Lane: second-operator*

# 178 — schema section shape and NOTA map check

## Intent captured

Spirit records created from the psyche correction:

- 425 — curly-brace NOTA map is the name-value notation.
- 426 — schema files should carry structure rather than explanatory
  comments.
- 427 — top-level schema is not a flat vector of same-kind declarations.
- 428 — schema namespaces can import local type namespaces from other
  schemas; Spirit-local type definitions are a good MVP.

## What changed

The initial `schema` repo bootstrap had `Document { declarations:
Vec<Declaration> }`. That matched the designer mistake the psyche
corrected. I replaced it with `Document { sections: Vec<Section> }`.

Current model:

- `Section::Messaging(Vec<Declaration>)` — ordered messaging/channel
  declarations such as `Operation`.
- `Section::Namespace(Namespace)` — name-value definitions backed by
  `BTreeMap<Name, DeclarationBody>`.
- `Name` implements `nota_codec::NotaMapKey`, so schema names are usable as
  actual NOTA map keys.

The new schema commit is:

`c639f08adba6` — `schema: model typed sections and namespace maps`

## NOTA map verification

I checked `nota-codec` without editing it. Existing tests confirm:

- `{key value ...}` map syntax round-trips.
- PascalCase map keys are valid in key position.
- Duplicate key text is rejected on decode.
- Duplicate projected key text is rejected on encode.
- Typed map keys via `NotaMapKey` work.

Command run:

`cargo test --test map_key_round_trip` in `/git/github.com/LiGoldragon/nota-codec`

Result: 9 tests passed.

I also added a schema-side witness:

`nota_curly_map_is_usable_for_schema_namespace_names`

It decodes `{Entry 1 Operation 2}` as `BTreeMap<Name, u64>` and re-encodes
the same curly-map form.

## Verification

Ran in `/git/github.com/LiGoldragon/schema`:

- `cargo fmt`
- `cargo test` — 7 tests passed
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --option max-jobs 0` — passed on the remote builder

## Remaining questions

1. What are the exact top-level section variants beyond `Messaging` and
   `Namespace`? Current code only names the two corrected shapes I could
   implement without guessing.
2. Should imports be their own `Section::Imports`, or should imported
   definitions remain `DeclarationBody::Reference` entries inside
   `Namespace`?
3. Do schema files need a canonical section order for MVP, or is the order
   meaningful but flexible as long as validation resolves forward and
   backward references?
