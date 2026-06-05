# 316 — Feedback on designer 524 — schema pipeline

## Read

Designer report `reports/designer/524-Psyche-the-schema-pipeline.md` is the
right framing. The two-arrow model is clearer than the older
Asschema-resolution framing:

```text
schema -> deserialize into schema-in-Rust -> lower into Rust interface code
```

This matches the operator-side repo docs now pushed into `schema-next` and
`schema-rust-next`.

## What I Endorse

The report correctly kills `SchemaResolution` as a public target. The typed
Rust datatypes that `.schema` deserializes into are the schema value. Any
lookup, validation, or derived fact belongs as methods on that value and its
child nouns.

The report also correctly places Rust-specific shaping in arrow 2. Rust cannot
nest type declarations, and generated modules/visibility/import aliases are
Rust projection work. That belongs in `schema-rust-next`, not in a new schema
IR.

The migration simplification is right: make `SchemaSource` become the
schema-in-Rust value, make it rkyv-serializable, add source-owned methods, then
move `RustModule::from_source` / `RustEmitter` onto it.

## Caveats

The report should say canonical round-trip, not imply byte-identical round-trip.
`schema-in-Rust` should be a faithful typed image that re-encodes to the
canonical `.schema` projection. Formatting, whitespace, comments if the
language later grows them, and syntactic aliases can normalize. The invariant
is semantic/canonical round-trip, not original bytes.

The rkyv boundary should apply to the schema-in-Rust value, not necessarily to
every parser helper. Source spans, diagnostics, or transitional raw blocks can
remain parse-time helpers if serializing them would contaminate the durable
schema value. The rkyv value should be the clean typed schema object.

The emitter should not receive a pile of primitive getters and reconstruct
schema semantics procedurally. It should call high-level methods on the schema
datatypes: root variants with resolved payload meaning, declaration visibility,
symbol paths, scalar/type-reference classification, import ownership. The
methods live on schema nouns; the emitter remains Rust projection.

## Implementation Consequence

Do not introduce a public `SchemaResolution` type. If implementation needs a
private traversal context, name it as a context/cache and keep it private to
schema-next. The public handoff is `SchemaSource` or the eventual better-named
schema-in-Rust root noun.

After 524, the next code slice is:

1. Fix `nota-next` derive direct-decode so schema source nodes do not spread the
   current string-dispatch seam.
2. Make the schema source datatypes rkyv-ready where they form the durable
   schema-in-Rust value.
3. Add source-owned methods for the facts Asschema currently materializes.
4. Add `RustModule::from_source` and parity tests against current Asschema
   emission.

## Intent Duplication Note

Designer says the pipeline was captured as record `fkbz`; operator captured
the same direct psyche clarification as record `ydvg`. They likely overlap.
This is not urgent during implementation, but a later intent-maintenance pass
should consolidate or identify the fuller record as canonical for the schema
pipeline.

## Final Feedback

Adopt 524 as the current design framing, with two precision edits in
implementation language: "canonical round-trip" instead of byte-identical
round-trip, and "rkyv-serializable clean schema-in-Rust value" instead of
serializing every parse helper. The report is otherwise the correct north star.
