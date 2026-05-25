# Verification And Gaps

## Nix Verification

All commands used the remote-builder rule: `--option max-jobs 0`.

`nota-codec`:

- `nix --option max-jobs 0 develop -c cargo fmt --check`
- `nix --option max-jobs 0 develop -c cargo test`
- `nix --option max-jobs 0 develop -c cargo clippy --all-targets -- -D warnings`
- `nix --option max-jobs 0 flake check -L`

`schema`:

- `nix --option max-jobs 0 develop -c cargo fmt --check`
- `nix --option max-jobs 0 develop -c cargo test`
- `nix --option max-jobs 0 develop -c cargo clippy --all-targets -- -D warnings`
- `nix --option max-jobs 0 flake check -L`

Both flake checks passed on the remote builder.

## New Constraint Tests

`schema/tests/multi_pass.rs`:

- proves `Schema::parse_str` through the `NotaValue` path equals the old streaming decoder on the Spirit v0.1.1 fixture;
- proves the multi-pass pipeline matches canonical assembly on an import-free schema;
- proves non-uniform header shape `(State Statement)` is rejected.

`schema/tests/multi_pass_pipeline.rs`:

- lowers a live Spirit schema through the multi-pass pipeline;
- compares multi-pass assembled output to canonical `Schema::parse_str(...).assemble(...)`;
- checks macro firing counts;
- rejects unknown import directive shapes;
- rejects non-six-position documents.

Together these tests now enforce the `record 602` direction at the MVP
level: generic NOTA tree shape is one side of the match; schema-owned
macro positions are the other side. The tests do not yet expose a
public `NodeDefinitionPoint` enum, but they already prevent the old
failure mode where schema semantics were hidden in a private streaming
walker.

`nota-codec/tests/value_shape.rs`:

- now covers the added schema-macro helper vocabulary and six-position `parse_sequence`.

## Remaining Gaps

Still not implemented:

- Fixed-point macro expansion over arbitrary user macro spaces.
- User-declared macro registration and invocation.
- Schema-derived Rust emission for `VersionProjection` implementations.
- Generated upgrade code replacing hand-written Spirit migration logic.
- Full schema-language editing discipline that constrains schema changes before they become diffs.
- Cross-version Spirit MVP against old pre-ShortHeader wire without
  `primary-602y` (the signal-frame backport / compatibility bead).

The largest practical next implementation is `UpgradeMacro`: feed two assembled schemas plus authored `Upgrade` annotations into a code generator that emits historical/current projection modules.

## Intent Questions Still Worth Asking

1. Should simple `[text]` ever become a generic `NotaValue::String`, or is the current split final: `[...]` is generic sequence and `[|...|]` is generic block string?
2. Should `Upgrade` remain feature-vector-only for the MVP? Operator lean: yes, because it is whole-schema behavior, not a namespace type declaration.
3. Should `Schema::parse_str_with_streaming_decoder` remain public as a migration witness, or become private/deleted once downstream users are comfortable with the `NotaValue` parser?
4. Should the enum/tree relationship point become concrete public
   schema API now, for example `NodeDefinitionPoint` matched with
   `NotaValueKind`, or remain private recognizer code until the next
   macro slice? Operator lean: make it public as soon as one
   relationship has more than two branches.
