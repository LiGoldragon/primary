# 207 — Schema local stack and generated-method workflow

## Scope

Psyche asked for a central way to test the latest local schema-stack
checkouts together, plus a stronger discipline that generated schema objects
are the method surface. This pass touched the workspace skills and the
`spirit-next` public pilot.

Relevant Spirit records captured before editing:

- 852 — central integration tests should rebuild local schema-stack checkouts
  together with local dependency overrides.
- 853 — generated schema objects are the nouns; handwritten behavior attaches
  to those objects as methods or trait impls, not free-function scaffolding.
- 855 — shape changes go through schema edits and regeneration, not
  hand-edited generated-type mirrors.
- 854 — root schema-generated signal objects should carry signal-frame
  protocol behavior for rkyv serialization and process-origin support when
  that caller library is ready.

## Workspace skills updated

- `skills/rust/methods.md` now has a schema-generated object section:
  generated types are the implementation nouns, and handwritten Rust should
  attach behavior to generated types or state-owning runtime objects.
- `skills/testing.md` now has a multi-repo local override test section:
  central consumer repos should expose a Nix witness that rebuilds the whole
  local schema stack together.
- `skills/nix-discipline.md` now documents ephemeral multi-repo overrides:
  use `nix flake check --override-input ... path:/git/...` rather than
  committing absolute local paths or mutable branch-only pins.

## `spirit-next` implementation

`spirit-next` now exposes `scripts/check-local-schema-stack`.

The script runs `nix flake check` with these source-input overrides:

- `nota-next-source` -> `NOTA_NEXT_PATH`, default
  `/git/github.com/LiGoldragon/nota-next`
- `schema-next-source` -> `SCHEMA_NEXT_PATH`, default
  `/git/github.com/LiGoldragon/schema-next`
- `schema-rust-next-source` -> `SCHEMA_RUST_NEXT_PATH`, default
  `/git/github.com/LiGoldragon/schema-rust-next`

The flake uses those inputs by copying them into the temporary Nix build
source under `vendor-sources/` and appending relative Cargo `[patch]` entries.
It also rewrites the three patched `Cargo.lock` entries from Git-source form
to path-source form inside the generated build source. That preserves Crane's
locked Cargo build without committing local checkout paths.

New Nix constraint:

- `checks.local-schema-source-patches` verifies the generated build source has
  the three relative source patches, the vendored schema source directories,
  and no remaining Git-source lock entries for those three crates.

Existing constraints still guard the intended architecture:

- `checks.no-old-signal-macro` searches only Spirit implementation surfaces,
  not copied dependency sources.
- `checks.generated-at-build-time` verifies `build.rs` still invokes the
  schema engine and Rust emitter.
- `checks.binary-boundary-test` verifies the rkyv process-boundary witness is
  still present.

## Verification

Passed:

- `nix flake check`
- `scripts/check-local-schema-stack --option max-jobs 0`

The second command proved the central script path with the latest local
`nota-next`, `schema-next`, and `schema-rust-next` checkouts. Nix reported the
three overrides and all flake checks passed.

## Remaining limits

This is still a consumer-side integration witness, not a whole-stack
orchestrator. It proves that `spirit-next` can rebuild against local schema
stack edits, regenerate Rust through `build.rs`, compile the generated types,
and cross the CLI/daemon rkyv boundary. It does not yet generate all signal
frame behavior, process-origin caller metadata, redb storage, or
signal-to-SEMA lowering from schema.
