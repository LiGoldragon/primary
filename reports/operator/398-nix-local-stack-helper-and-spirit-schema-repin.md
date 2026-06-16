# Nix local stack helper and Spirit schema repin

## Result

The repeated long-form Nix override command is now captured as
`tools/nix-local-stack`. It reads a target flake's `*-source` inputs and adds
ephemeral `--override-input <name> path:/git/github.com/LiGoldragon/<repo>`
arguments for matching local checkouts.

The common Spirit command becomes:

```sh
tools/nix-local-stack build --target path:/git/github.com/LiGoldragon/spirit#default
```

The helper is documented in `skills/nix-discipline.md` under multi-repo local
stack checks.

## Mainline integration landed

The schema/codegen stack is on code-repo main through these commits:

- `schema-rust-next` `cad9ec27` — generated scalar-backed newtype standard impls
  and enabled them for wire-contract emission.
- `signal-spirit` `876c2721` — regenerated contract and removed redundant
  hand-written scalar impls.
- `meta-signal-spirit` `3283925f` — regenerated contract and fixed schema source
  inclusion in its Nix filter.
- `signal-agent` `35be3523` — repinned to mainline structural schema tooling and
  migrated schema text to current positional syntax.
- `meta-signal-agent` `4c58b216` — same mainline structural schema migration for
  the meta contract.
- `spirit` `41f11730` — repinned Cargo/Nix inputs to those commits and hardened
  production migration for the schema-10 family identity that existed before the
  standard-newtype generator repin.

## Spirit migration detail

Regenerating Spirit's SEMA schema changed the generated family identities for
`RecordsFamily`, `ReferentsFamily`, and `MigrationsFamily`. The deployed
schema-10 store can therefore be in a real half-step: schema version 10 and
layout 5, but with the pre-standard-impl schema-10 family identities.

`src/production_migration.rs` now recognizes both known schema-10 legacy-family
surfaces:

- schema-10/layout-5 stores carrying the prior schema-10 family identities;
- schema-10/layout-5 stores carrying the v9 family identities from the earlier
  production half-step.

The new witness
`migrates_version_ten_pre_standard_impl_family_to_current_family` seeds the
pre-standard-impl family identities, runs `StoreMigration`, verifies record and
referent survival, records source schema version 10, and proves a second run
reports `Current`.

## Verification

Rust and Nix gates run during the landing:

- `schema-rust-next`: `cargo test`, `cargo clippy --all-targets -- -D warnings`,
  `nix flake check --builders '' -L`.
- `signal-spirit`: regeneration check, `cargo test`, `cargo clippy --all-targets
  -- -D warnings`, `nix flake check --builders '' -L`.
- `meta-signal-spirit`: regeneration check, `cargo test`, `cargo clippy
  --all-targets -- -D warnings`, `nix flake check --builders '' -L`.
- `signal-agent`: regeneration check, `cargo test`, `cargo clippy --all-targets
  -- -D warnings`, `nix flake check --builders '' -L`.
- `meta-signal-agent`: regeneration check, `cargo test`, `cargo clippy
  --all-targets -- -D warnings`, `nix flake check --builders '' -L`.
- `spirit`: `cargo test`, `cargo test --features production-migration`, `cargo
  test --all-features`, `cargo clippy --all-targets --all-features -- -D
  warnings`.

The helper itself was exercised against Spirit:

```sh
tools/nix-local-stack build --target path:/git/github.com/LiGoldragon/spirit#default
```

That produced `/nix/store/pa1hznf4hv1px7l08dya2ds8w4nz1az6-spirit`. The
ignored daemon/CLI process-boundary suite passed against that package:

```sh
SPIRIT_NIX_BUILD_RESULT=/nix/store/pa1hznf4hv1px7l08dya2ds8w4nz1az6-spirit \
  cargo test --features nota-text --test nix_integration -- --ignored
```

Result: 9 passed.

After repinning `spirit/flake.lock`, the ordinary no-override build also
passed:

```sh
nix build --builders '' --log-format bar-with-logs --print-out-paths --no-link \
  path:/git/github.com/LiGoldragon/spirit#default
```

That produced `/nix/store/a3hznhwds2yqn9i9nr0dby7vs8m6ci6p-spirit`; the same
ignored daemon/CLI process-boundary suite passed against it. Result: 9 passed.

## Boundaries

This landing intentionally does not land the broader methods-in-schema /
composition branch. The mainline piece is the practical, shape-proven part:
standard generated scalar newtype impls, component contracts regenerated from
current schema tooling, and Spirit upgraded with a tested migration path.

The `tools/orchestrate status` helper could not run during this session because
primary's orchestrate CLI dependency graph currently points at an inaccessible
`nota-codec` revision. No code changes were made to orchestrate in this pass.
