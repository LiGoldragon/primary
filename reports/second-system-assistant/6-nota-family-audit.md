# NOTA Family Audit

## Scope

Audited the NOTA family against the workspace intent log and the
current implementation surfaces:

- `nota`: language/spec repo.
- `nota-codec`: runtime lexer, encoder, decoder, traits, tests.
- `nota-derive`: proc-macro derive crate.
- `nota-config`: typed configuration input crate. This checkout was
  not listed in the active repo map before the audit, but it is a
  NOTA-family component and is used by downstream binaries.
- Workspace `skills/nota-design.md`, plus the primary active/recent
  repository indexes.

The main intent anchors were:

- NOTA has no syntax exceptions: one notation means one thing.
- PascalCase has exactly three value cases: `(Variant fields...)`,
  `(fields...)`, and bare `Variant`.
- Struct records are positional and untagged; type names do not appear
  as struct tags.
- Maps use `{key value ...}`; map keys are key text by position, not
  enum values, and the map form exists for unique names.
- Rust tuples are unsupported; single-field unnamed structs are
  transparent newtypes only.
- Component binaries accept exactly one argv argument.

## Fixes Landed

### `nota-codec`

Commit `6f483741` (`reject duplicate nota map keys`) makes map
uniqueness explicit instead of accidental.

Before the fix, decoding `{alpha 1 alpha 2}` into a map silently
overwrote the first value. That contradicted the intent that maps are
the unique-name/key-value form. The runtime now has
`Error::DuplicateMapKey` and rejects duplicate key text while decoding
both `BTreeMap` and `HashMap`.

Encode now also rejects duplicate projected key text after sorting by
`NotaMapKey::as_map_key()`. That protects the wire format from a bad
manual `NotaMapKey` implementation where two distinct Rust keys render
to the same NOTA key token.

The same commit also tightens stale docs around variant tags, map key
text, path sentinels, and legacy `record_head` terminology.

### `nota`

Commit `ae7624ca` (`tighten nota syntax documentation`) removes stale
spec wording that made PascalCase look like "type / variant names" or a
"record / variant head". The spec now says PascalCase names enum
variants, structs are untagged, and a PascalCase token immediately
after `(` is a data-carrying variant tag.

It also removes horizontal-rule separators from markdown that violated
the workspace markdown rule.

### `nota-derive`

Commit `83231495` (`correct nota derive documentation`) fixes the
stale public docs for `NotaRecord`.

The derive docs used to claim records encode as `(TypeName field0
field1 ...)` and that omitted optional tail fields decode for
compatibility. Both were wrong. The docs now say `NotaRecord` emits
`(field0 field1 ...)`, with the struct type determined by schema
position, and every field position is required.

The architecture notes now also reflect that `NotaMapKey` emits only
the map-key trait, compile-fail witnesses currently live under
`nota-codec/tests/compile_fail/`, and the derive crate is working code,
not a stubbed skeleton.

### `nota-config`

Commit `b3e01ea5` (`enforce single configuration argument`) fixes a
clear single-argument-rule violation.

`ConfigurationSource::from_args` previously joined multiple argv tokens
into one inline NOTA record. That made split argv a hidden syntax
channel. The crate now requires exactly one configuration argument:
zero args return `MissingArgument`, more than one returns
`MultipleArguments`, and inline NOTA must be shell-quoted so it arrives
as one argv token.

The old `from_argv_nth(0)` entry point is kept as a compatibility alias
for downstream callers, but any index other than `0` returns
`UnsupportedArgumentIndex`.

### Primary Workspace

The active and recent repository indexes now include `nota-config`, so
future NOTA sweeps do not miss it.

`skills/nota-design.md` now removes the last harmful "top-level record
type name" wording. It explicitly says struct type names are not
written as struct tags; PascalCase immediately after `(` is an enum
variant tag.

## Residual Gaps

### Legacy `record_head` API Names

`nota-codec` still exposes names such as `expect_record_head`,
`peek_record_head`, and `ExpectedRecordHead`. Their docs now explain
that the grammar meaning is a data-carrying enum variant tag, but the
identifier names still carry the old language.

I did not rename them in this audit because that is a cross-crate API
change involving `nota-derive` and any downstream caller. The clean
future shape is likely a deliberate rename such as
`expect_variant_record` / `peek_variant_tag` plus a compatibility
period.

### Non-Finite Floats

`Encoder::write_f64` still emits `NaN`, `inf`, and `-inf` for
non-finite values, while `Decoder::read_f64` only accepts numeric
tokens. That means non-finite floats do not round-trip through NOTA
today.

I did not fix this because I did not find clear intent for the desired
wire policy. The two coherent choices are: reject non-finite floats at
encode time with a typed error, or explicitly add/spec non-finite float
tokens.

### Downstream `from_argv_nth(0)` Caller

A search found `lojix` still calls `ConfigurationSource::from_argv_nth(0)`.
The compatibility alias keeps it working, but that downstream should
eventually move to `ConfigurationSource::from_argv()` so the legacy
multi-argument selector surface can retire.

### Labeled-Field Rejection

There is already an open task, bead `primary-uy7o` (nota-codec: reject
labeled-field NOTA record shape with a typed error), for catching
`(key value)`-style record mistakes more directly. I did not implement
that in this audit because it is a separate feature-level diagnostic,
not a small documentation or intent-backed behavior correction.

## Verification

Commands run successfully:

- `cargo test` in `nota-codec`.
- `cargo test` in `nota-config`.
- `nix flake check` in `nota-codec`.
- `nix flake check` in `nota`.
- `nix flake check` in `nota-derive`.
- `nix flake check` in `nota-config`.

The primary workspace still had pre-existing uncommitted intent edits in
`intent/horizon.nota` and `intent/persona.nota`; this audit did not touch
or commit those.
