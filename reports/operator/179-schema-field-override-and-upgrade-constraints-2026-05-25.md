# 179 - Schema field override and upgrade constraints

*Kind: Implementation report. Topic: schema parser and upgrade-plan constraints. Date: 2026-05-25. Lane: operator.*

## Frame

The psyche asked for more of the designed upgrade mechanism to be implemented and for constrained tests that actually exercise the designed behavior, even when shim logic is needed. That testing constraint was captured in Spirit record 548.

I compared the work against `reports/designer/333-upgrade-mechanism-full-design-explained.md` and `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md` before editing. `/186` already closes the orchestrate private-upgrade socket gap from `/333`: orchestrate now binds the upgrade socket, serves `signal-version-handover`, restores Mirror before readiness, and has daemon tests. The non-colliding work left for this slice was in `/git/github.com/LiGoldragon/schema`.

## What I found

`/333` is stale on one important point: the schema repo already had the `UpgradeRule` builtin macro variant on `main` at commit `be6860fb` (`schema: lower upgrade rules through builtin macro variant`). I did not reimplement it.

The next useful gap was the field-name override syntax from the schema reports: `(fieldName Type)` in a record field position. This matters because the schema language needs to express the rule "field name carries the dimension, type carries the scale" without forcing fake wrapper types.

The first implementation attempt exposed a real parser ambiguity: `(Option Topic)` and `(certainty Magnitude)` both start with a record. The fix is that container heads (`Option`, `Vec`, `Map`) win in field position; otherwise the same two-item record is a named-field override.

## What changed

Repository: `/git/github.com/LiGoldragon/schema`

Changed files:

- `src/name.rs`
- `src/error.rs`
- `src/declaration.rs`
- `src/parser.rs`
- `src/document.rs`
- `src/layout.rs`
- `src/assembled.rs`
- `src/lib.rs`
- `tests/document.rs`

Implemented:

- Added `FieldName`, a validated lower-start field identifier for explicit schema field names.
- Added `Field`, carrying optional `FieldName` plus the actual `TypeExpression`.
- Changed record bodies and data-carrying variant field lists from raw `Vec<TypeExpression>` to `Vec<Field>`.
- Kept existing builder ergonomics by preserving `Declaration::record(Vec<TypeExpression>)` and `Variant::with_fields(Vec<TypeExpression>)`, which wrap fields as inferred names.
- Added parser support for `(certainty Magnitude)` style field-name overrides.
- Preserved container parsing in field position for `(Option Topic)`, `(Vec Entry)`, and `(Map Key Value)`.
- Added `bool` as an alias for the existing `Boolean` primitive.
- Added storage-shape comparison that ignores field-name-only changes, so upgrade planning treats a field rename with the same type order as `Projection::Identity`.

## Constrained tests

Added tests in `tests/document.rs`:

- `parser_accepts_bool_as_boolean_primitive_alias`
- `parser_accepts_explicit_field_names_without_changing_field_types`
- `field_name_only_change_does_not_require_storage_upgrade_annotation`

The existing reader fixture tests also became meaningful regression tests for the parser ambiguity: `spirit-v0-1-1.schema` already contains `(Option Topic)`, so the test suite would fail if named-field parsing stole container expressions.

## Verification

All commands were run through Nix with `--option max-jobs 0`:

- `nix --option max-jobs 0 develop -c cargo test`
- `nix --option max-jobs 0 develop -c cargo fmt --check`
- `nix --option max-jobs 0 develop -c cargo clippy --all-targets -- -D warnings`
- `nix --option max-jobs 0 flake check -L`

The flake check ran on the remote builder and passed all configured checks.

## Remaining gaps

The schema crate can now represent explicit field names and decide that field-name-only changes are storage-identical. It still does not emit Rust code from this metadata; that belongs to the `signal-frame` macro side.

The next high-value constrained test is in the macro consumer: prove that a schema record containing `(certainty Magnitude)` emits a Rust field named `certainty` while the wire/storage order remains positional and unchanged.

For orchestrate, `/186` leaves two design/implementation questions: whether protocol-level `Divergence` should reuse the existing orchestrate divergence table or get a dedicated handover table, and whether old-daemon process exit belongs inside orchestrate after `HandoverCompleted` or remains solely persona-daemon authority.
