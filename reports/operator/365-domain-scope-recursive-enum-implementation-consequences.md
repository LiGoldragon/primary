# DomainScope recursive enum — implementation consequences

## Trigger

Designer audit `593-spirit-live-deployment-audit.md` found that deployed
Spirit `DomainScope` is still `DomainPath = (Vec String)`. That is correctly
diagnosed as a type-safety gap: misspelled path segments can parse and only
fail semantically, if they fail at all.

## What I verified

Spirit's current schema stack can express the deployed shape:

- `schema/domain.schema` declares `DomainPath (Vec String)` and
  `DomainScope DomainPath`.
- `schema-rust-next` emits `DomainScope::from_path(Vec<String>)`,
  `DomainScope::expand()`, and the relation table from `Relations`.
- Spirit's query and guardian paths do prefix matching by comparing a typed
  `Domain`'s generated path segments against that string path.

The schema/rust emitter does not currently have the type machinery for the
new desired shape:

- Named type references emit directly as the named Rust type.
- A truly recursive enum payload would therefore emit without `Box`, producing
  an infinite-size Rust type.
- `nota-next` can encode/decode `Box<T>`, so the text codec can support the
  underlying indirection, but `schema-rust-next` does not currently detect
  recursive references and box them.
- Early-terminating scopes also need a clean generated NOTA shape. A naive
  `Optional` payload would produce `None` / `Some` in the surface, which is not
  the intended typed prefix syntax.

## Consequence

Retyping `DomainScope` as "the same recursive enum, terminating early at an
internal node" is not a safe Spirit-only patch. Hand-editing generated
`src/schema/domain.rs` would violate Spirit's schema-derived contract and be
lost on regeneration. Modeling scopes as ad hoc finite string-free variants
would improve type safety but would not implement the desired recursive prefix
language.

The durable implementation belongs first in the schema stack:

1. `schema-next` needs a source-level way to declare recursive prefix enums, or
   enough ordinary enum syntax plus semantics to represent "this node may stop
   here or carry a child."
2. `schema-rust-next` needs recursive-reference detection and boxed emission
   for enum payload cycles.
3. Generated NOTA support needs to render early termination without exposing
   Rust's `Option` shape as the user-facing schema language.
4. Spirit can then replace `DomainPath (Vec String)` with the generated typed
   `DomainScope`, regenerate, and migrate the store.

## Work completed in this slice

The separate guardian retrieval finding from audit 593 was implemented in
Spirit:

- `guardian_records_for_entry` now applies `GUARDIAN_RECORD_LIMIT` on the
  sorted entry/propose path.
- same-`Kind` alone no longer contributes relevance.
- integration tests assert that same-kind-only records are absent from the
  agent prompt, equivalent-domain records remain present, and entry relevance
  is capped at 64 records.

