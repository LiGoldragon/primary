# 180.2 - Implementation and tests

## signal-frame

Commit: `e4e1581c`

Changed macro internals:

- Added `SchemaField { name, schema_type }` to the macro model.
- Changed schema variants from `Vec<SchemaType>` to
  `Vec<SchemaField>`.
- Updated the schema reader to preserve `schema::Field::name()`.
- Updated ShortHeader slot emission and NOTA box-form codec emission to
  use explicit schema field names first.
- Removed Spirit-specific hardcoded exceptions such as
  `Entry + Magnitude => certainty` and
  `RecordSummary + RecordIdentifier => identifier`.
- Updated validation to walk through `SchemaField.schema_type`.

The `Cargo.lock` schema pin advanced to `ddf71ce7`, because the older
schema dependency did not expose the field metadata needed by this
implementation.

## signal-persona-spirit

Commit: `03d160b5`

Changed `spirit.schema` to name fields where the generated Rust field
access cannot honestly be derived from type names alone:

- `Entry`: `topic`, `kind`, `summary`, `context`, `certainty`, `quote`
- `Statement`: `text`
- `RecordQuery`: `topic`, `kind`, `mode`
- `RecordSummary`: `identifier`, `topic`, `kind`, `summary`,
  `certainty`
- `RecordProvenance`: `summary`, `context`, `date`, `time`, `quote`
- subscription/open/retract/event payloads: `token`, `snapshot`,
  `state`, `records`, `topics`, `questions`, `operation`,
  `observation`, and related names

The contract now proves that the field-name rule lives in schema, not in
Spirit-specific macro code.

## Nix witnesses

All commands used `--option max-jobs 0`.

`signal-frame`:

- `nix develop -c cargo fmt --check`
- `nix develop -c cargo clippy --all-targets -- -D warnings`
- `nix develop -c cargo test`
- `nix flake check -L`

`signal-persona-spirit`:

- `nix develop -c cargo fmt --check`
- `nix develop -c cargo clippy --all-targets -- -D warnings`
- `nix develop -c cargo test`
- `nix develop -c cargo test --test short_header`
- `nix develop -c cargo test --test box_form`
- `nix flake check -L`

Relevant passing contract tests:

- ShortHeader generation and receive-side triage remain schema-derived.
- box-form Entry round trips still emit `(Entry Decision High)` while
  boxing the unsized text fields.
- v0.1.0 to v0.1.1 migration projection tests still pass.

## Constraint value

This pass removes one explicit anti-pattern: macro code no longer knows
that Spirit's `Magnitude` field is called `certainty`. The schema owns
that relationship, and the macro is generic again.
