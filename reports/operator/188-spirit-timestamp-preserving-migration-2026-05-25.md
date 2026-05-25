# 188 — Spirit timestamp-preserving v0.1 to v0.2 migration

## Scope

Implemented a one-off offline migration tool in `persona-spirit` for moving a
Spirit v0.1 database into the v0.2 description-only schema while preserving the
daemon-generated original timestamp.

This is intentionally outside the Spirit daemon request path. It is not import
logic in Spirit's working CLI. It is a migration binary that reads an old redb
store and writes a new v0.2 redb store.

## What landed

`persona-spirit` main now includes commit `0c4a3deb`:

- `src/migration.rs`
  - `MigrationConfiguration { source, target }`
  - historical v0.1 storage wrappers
  - `migrate_v010_to_v020`
  - projection through `signal_persona_spirit::migration::V010ToV011`
  - preservation of old `RecordIdentifier`, `Date`, and `Time`
  - refusal to write into a non-empty target database
- `src/bin/spirit-migrate-0-1-to-0-2.rs`
  - one NOTA argument only
  - accepts inline NOTA or a path to a NOTA file through `SingleArgument`
  - prints `(MigrationCompleted N)`
- `src/store.rs`
  - `import_migrated_record`
  - `is_empty`
- `src/error.rs`
  - migration error variant mapped to `CommitStatus::NotCommitted`
- `flake.nix`
  - package/app `spirit-migrate-0-1-to-0-2`
  - Nix check `test-migration`
  - package split test now covers the migration binary
- `tests/migration.rs`
  - fixture-built v0.1 source database
  - timestamp and identifier preservation
  - v0.2 next-record counter continuity
  - non-empty-target refusal
  - inline NOTA argument path
  - file-path argument path

## Tool shape

The migration call shape is:

```nota
([/path/to/source-v0.1.redb] [/path/to/target-v0.2.redb])
```

The first field is the source database path. The second field is the target
database path. The target must not already contain records. The source remains
read-only from the tool's perspective.

The output shape is:

```nota
(MigrationCompleted 697)
```

## Live-copy proof

I copied the deployed v0.1 production database into a temporary directory and
ran the migration tool against the copy. Production was not touched.

Result:

- source: `~/.local/state/persona-spirit/v0.1.0/persona-spirit.redb`
- migration output: `(MigrationCompleted 697)`
- started a sandbox v0.2 daemon on the migrated copy
- queried it through the v0.2 Spirit CLI
- `Observe Topics` returned the migrated topic catalog
- `Observe Records` with `WithProvenance` returned records carrying the
  preserved v0.1 `Date` and `Time`

This proved the tool against the real deployed v0.1 storage shape, not only a
synthetic fixture.

## Nix verification

All checks were run with `--option max-jobs 0`.

Passed:

```sh
nix build --option max-jobs 0 .#checks.x86_64-linux.test-migration --print-out-paths
nix build --option max-jobs 0 .#checks.x86_64-linux.test-split-packages --print-out-paths
nix flake check --option max-jobs 0
```

The first full flake check caught a Clippy issue in the migration test helper
(`too_many_arguments`). I fixed it by replacing the helper's many-argument
signature with a typed `OldRecordInput` test struct, squashed it into the code
commit, and reran the full flake check successfully.

## Boundaries

This is an offline one-off database migration tool. It does not solve live
dual-write, socket handover, or schema-derived automatic migration. Those remain
separate protocol work.

The migration preserves old timestamps by bypassing the daemon's normal
receive-time stamping path. That is correct for a historical database migration
and should not be used by ordinary agents or the Spirit CLI.
