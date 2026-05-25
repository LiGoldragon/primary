# 183 — schema engine 338 implementation

## Frame

Implemented the operator slice downstream of
`reports/designer/338-schema-engine-refreshed-vision-2026-05-25.md` in
`/home/li/wt/github.com/LiGoldragon/schema/operator-schema-engine-338`.

Captured psyche correction first through Spirit as record 628:
schema authored syntax uses parentheses for enum and variant forms, and
square brackets for struct field vectors.

Captured follow-up correction through Spirit as record 635: the delimiter
rule applies globally, so header root endpoint choices are enums and use
parentheses too.

## Landed / Verified Code

While this slice was open, schema `main` advanced with the delimiter
correction already landed. I rebased onto that commit and kept this branch to
the missing implementation layer instead of re-publishing the same parser
change.

The resulting schema language treats namespace declaration delimiters as:

- `Kind (Decision Principle Correction)` — enum choices.
- `Entry [Topic Kind Summary Context Magnitude Quote]` — struct fields.
- `Topic [String]` — one-field struct, represented as the newtype case.
- `RecordSummaries [(Vec RecordSummary)]` — newtype over a container type.

Header roots now use enum-shaped endpoint choices:

```nota
[
  (State (Statement Declaration))
  (Record (Entry))
  (Observe (Records))
]
```

Verified parser paths on this branch:

- `src/shape_parser.rs` primary `NotaValue` parser.
- `src/parser.rs` streaming compatibility parser.
- `src/multi_pass.rs` macro-front recognizer.
- `src/node_shape.rs` shape classifier.

The Spirit schema fixtures and parser tests are migrated to the corrected
global delimiter syntax on this branch.

## Module Names

Added the first code-generation metadata for schema-local module identity:

- `ModuleName`, derived from a `.schema` file stem.
- `QualifiedName`, rendered as `<module>::<type>`.
- `LoadedSchema::read_path` now attaches a module to `AssembledSchema`.
- `AssembledSchema::qualified_name_for` can project local and imported
  types, e.g. `spirit_v0_1_1::Entry`, `magnitude::Magnitude`,
  `shared::Source`.

This does not emit Rust modules yet. It gives the later macro/codegen layer a
tested source of truth for one-module-per-schema-file output.

## Tests

Passed:

- `cargo test`
- `nix flake check --option max-jobs 0 --print-build-logs`

The Nix check used the remote builder path and completed all schema checks.

## Open Edges

The actual proc-macro/code-emission layer is still separate work. This slice
only makes the schema crate parse and assemble the corrected authored shape
and expose qualified-name metadata.

Fixed-point user macro loading, upgrade-macro emission, and end-to-end Spirit
schema-to-signal generation remain next slices from the schema design thread.

Container field naming remains at the current implementation boundary:
inline containers derive names such as `optionTopic` and `vecTopic`. When a
more meaningful field name is needed, the schema author introduces a named
newtype such as `RecordSummaries [(Vec RecordSummary)]` and uses that type in
the field position.
