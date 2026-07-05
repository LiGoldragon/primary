# Product Components Amendment

## 1. Superseded wording

- Supersedes any design text that models product components as only an ordered vector of type references.
- Supersedes any design text that treats Rust field names as schema projection metadata or as the source of product component identity.
- Supersedes examples that canonicalize unique product components as explicit `field.Type` pairs, such as `Entry { domains.Domains kind.EntryKind description.Description referents.Referents }`.

## 2. Correct product component model

- A product component is positional and typed, with a component identity used for canonical schema re-encoding and schema evolution.
- The preferred authored identity is implicit: a bare type name supplies the component identity derived from that type name.
- Explicit `field.Type` syntax is only for repeated use of the same type inside one product when positions need stable disambiguation, for example `TimeRange { start.Time end.Time }`.
- Explicit fields are stable component identities, not arbitrary display labels and not Rust field names.
- Product order remains semantically load-bearing for help, wire, and storage projections.

## 3. Authored syntax validity rules

- `Product { TypeA TypeB TypeC }` is valid when each referenced type appears once in that product.
- If a type appears only once in a product, any `field.Type` spelling for that component is invalid.
- If `field` equals the canonical camel/lowercase-derived identity of `Type`, `field.Type` is invalid as redundant.
- If the same type appears more than once in a product and those positions are distinct components, each repeated occurrence must use explicit non-derived field identity.
- Explicit identities for repeated occurrences of the same type must be unique within the product.
- Therefore `Entry { Domains EntryKind Description Referents }` is the canonical spelling, while `Entry { domains.Domains kind.EntryKind description.Description referents.Referents }` must be refused.

## 4. True Schema storage shape

- True Schema stores products as ordered component records, not as bare type-reference vectors.
- Each component record needs at least: position, type reference, and component identity.
- Implicit identity may be represented as derived-from-type, but canonical re-encoding must emit only the bare `Type` token for unique components.
- Explicit identity must be stored when valid `field.Type` syntax is authored, because canonical re-encoding and evolution diffs need the authored stable identity.
- True Schema must not derive product component identity from schema-rust output or Rust field names; schema-rust consumes this shape.

## 5. Help projection impact

- Help remains positional and label-free.
- Help data is pure typed data; renderer strings are produced only at the final renderer boundary.
- Help displays canonical product component syntax: bare `Type` for implicit unique components and `field.Type` only where repeated-type disambiguation requires it.
- Help must not display labels, name/type pairs, wrapper heads, or Rust field names.
- Example help spellings: `Entry { Domains EntryKind Description Referents }` and `TimeRange { start.Time end.Time }`.

## 6. Schema evolution impact

- Diff and upgrade logic must compare component identity plus position plus type, not position alone and not type alone.
- Insertion at position X should be recognized as an inserted component with later known identities shifted, not as unrelated replacements of all later positions.
- Moves should be recognized by stable component identity while still recording the positional change.
- Insertion, move, or reordering is not automatically safe for positional wire or storage formats; it requires explicit upgrade, default, backfill, or projection rules.
- Renaming an explicit component identity is an evolution event that requires an explicit mapping; it is not a harmless label change.

## 7. Proof tests to add

- Decode and canonical re-encode `Entry { Domains EntryKind Description Referents }` unchanged.
- Reject `Entry { domains.Domains kind.EntryKind description.Description referents.Referents }` because all referenced types are unique.
- Reject `domains.Domains` and `time.Time` as redundant derived identities.
- Reject repeated bare type components such as `TimeRange { Time Time }` when they represent distinct positions.
- Accept and round-trip `TimeRange { start.Time end.Time }`, preserving explicit identities in True Schema.
- Reject duplicate explicit identities for the same repeated type, such as `TimeRange { start.Time start.Time }`.
- Verify help projection emits positional components only, with `field.Type` only for valid repeated-type disambiguation.
- Verify evolution diff treats insertion before existing components as insertion plus positional shifts, not as cascading replacements, and marks it unsafe without explicit upgrade/default/backfill/projection rules.

## 8. Open questions

- What is the exact derived-identity function for type names, including acronym, namespace, and collision behavior?
- Are all repeated same-type product components considered distinct and therefore required to use explicit identities, or is there an identity-less repeated case?
- What constraints beyond uniqueness and non-redundancy apply to explicit identity names?
- Where are upgrade/default/backfill/projection rules represented in True Schema and normalized authored schema text?
