# Lojix v1→v2 migration validation

## Scope and boundary

This validation used only committed source, an isolated temporary
materialization of Lojix `main`, synthetic test stores, and Nix build outputs.
It did not read, copy, inspect, migrate, or otherwise access
`/var/lib/lojix`; it did not restart a unit, activate a generation, deploy,
modify source, update a bead, commit, or push.

The temporary Lojix source was reconstructed file-by-file from
`jj file list -r main` and `jj file show -r main root:$source_path` into a
fresh `mktemp -d` directory. `CARGO_TARGET_DIR` was inside that directory, so
the shared checkout was not used for build artefacts.

## Coordination and exact revisions

- `bd show primary-akw --json` confirms the incident work item remains open
  and directs latest-line migration followed by declarative activation and
  live serving proof.
- `orchestrate '(Observe Lanes)'` showed an active
  `LojixOuranosActivation` lane. `orchestrate '(Observe Worktrees)'` showed
  an active Lojix `horizon-driven-intercom` worktree, so this validation did
  not reuse or alter any Lojix workspace.
- Both checked-out workspaces were clean. Lojix's checked-out parent is a
  divergent newer line (`162bb936…`) which lacks the migration files, so it
  was deliberately not tested.
- The tested source revision is Lojix `main`
  `9adc6c75b8be85edc64c4eb14c27376bb0388dd7`.
- CriomOS `main` is `475bf5c27efa`. Its `flake.nix` and `flake.lock` both pin
  Lojix to the full `9adc6c75…` revision.

## Results

| Gate | Result | Evidence |
| --- | --- | --- |
| Exact source/pin | PASS | Jujutsu revision inspection and CriomOS lock/source inspection above. |
| Migration preservation | PASS | Synthetic genuine schema-1 fixture retains all six record families, event/deployment history, metadata, and a byte-identical schema-1 backup. |
| Idempotency and permitted interruption witness | PASS, qualified | Tests cover tool-owned partial staging retry and byte-for-byte schema-2 rerun; source validates, syncs, reopens staged data, atomically renames, syncs the parent, and reopens the canonical database. |
| Invalid input/conflict protection | PASS | Corrupt rows and invalid key/relationship shapes are rejected before backup/replacement; conflicting backup and unowned staging paths are preserved and refused. |
| Startup ordering | PASS, static | The exact CriomOS module lists `lojix-migrate-store` as the first `ExecStartPre`, followed by `lojix-write-configuration`, before `lojix-daemon` `ExecStart`. |
| Locked Lojix Nix package | PASS | The exact-pin flake check passed and the built package contains executable `lojix-daemon` and `lojix-migrate-store`. |
| Exact CriomOS activation-closure evaluation/build | NOT RUN — authorization boundary | The only documented whole-OS shape needs materialized `system`, `horizon`, `deployment`, and `secrets` inputs under live Lojix state. This validation was told to stop rather than access live state. Bare evaluation correctly stops at the no-horizon stub. |
| Live pre-start, store migration, daemon serving, and history query | NOT RUN | Production actions and live-store access are outside this validation. |

## Commands and outcomes

The following were run from the isolated exact-pin materialization after the
source reconstruction described above. `$validation_root` was the fresh
temporary directory created for this run.

```sh
CARGO_TARGET_DIR="$validation_root/target" cargo test --locked --test schema_one_migration
```

Passed: 10 passed, 0 failed. The named tests cover six-table row equality and
backup metadata, empty registered tables, sparse allocator continuation,
partial-stage retry, schema-2 no-op idempotency, corrupt input, invalid
relations/keys, conflict refusal, and exact CLI arity.

```sh
CARGO_TARGET_DIR="$validation_root/target" cargo test --locked
```

Passed: all executed tests passed. The focused migration suite again passed
10/10. Network/deployment-heavy tests were explicitly ignored by the suite
(including real Nix evaluation/build and daemon deployment tests); this is not
being represented as their execution.

```sh
nix flake check --offline "path:$validation_root/source"
```

Passed: all six exact-pin flake checks evaluated and built: package/default,
daemon binary, test, daemon startup rejection, formatting, and clippy. The
first bare `nix flake check --offline` from the exported directory was not a
valid flake locator because Nix attempted Git discovery at `/tmp`; it was
immediately rerun with the explicit `path:` locator above. The successful
check used the configured remote builder only for builds/output copying; it
did not activate or deploy anything.

```sh
validation_package=$(nix build --offline --no-link --print-out-paths "path:$validation_root/source#default")
test -x "$validation_package/bin/lojix-daemon"
test -x "$validation_package/bin/lojix-migrate-store"
```

Passed: both binaries are present and executable in the locked package
closure.

```sh
nix eval --offline --raw .#nixosConfigurations.target.config.system.build.toplevel.drvPath
```

Expected non-zero result: `CriomOS: no horizon input was provided.` The
default input is intentionally a throwing stub. Supplying the real
materialized override inputs would access current live Lojix state and was not
authorized here.

## Static implementation findings

At Lojix `9adc6c75…`, `Cargo.toml` exposes `lojix-migrate-store` and
`src/lib.rs` exposes `reconstruction`. The migrator opens the source
read-only, validates the six-table catalog, row keys, and relations; for
schema 1 it creates the non-overwriting permanent
`.schema-v1.backup`, stages schema 2, preserves metadata, syncs/reopens it,
renames it atomically, syncs the parent, and reopens the canonical store.
Schema 2 returns `AlreadyCurrent` without rewrite; an absent canonical store
returns `NoStore` provided no migration artefacts remain.

At CriomOS `475bf5c2…`, the active module is:

```nix
ExecStartPre = [
  "${lojixPackage}/bin/lojix-migrate-store ${storePath}"
  "${lojixPackage}/bin/lojix-write-configuration ${startupRequest}"
];
ExecStart = "${lojixPackage}/bin/lojix-daemon ${startupArchive}";
```

This proves the declared ordering, but not a systemd execution on the live
host.

## Missing or qualified gates

- There is no dedicated test for the `NoStore` migration outcome in
  `schema_one_migration.rs`; its behavior is source-inspected, not directly
  fixture-proven by that suite.
- The tests cover interruption before replacement through a tool-owned partial
  stage. They do not fault-inject a crash after atomic rename and before marker
  removal. Source remains safe/idempotent because schema 2 is not rewritten,
  but the schema-2 fast path does not clean a leftover proven-owned marker.
- No validation here establishes that the current live store is schema 1,
  readable, or represented by the synthetic fixture. That requires an
  authorized, read-only live inspection immediately before activation.
- The whole CriomOS closure remains unproven until it is evaluated and built
  from the immutable `475bf5c2…` source with the four materialized inputs.

## Consequence for activation approval

Production activation is **not yet the only remaining step**. The source and
Lojix package gates pass, but the exact CriomOS activation closure must still
be evaluated and built from its real materialized inputs, and a fresh
read-only live-store witness must establish the precondition. Those operations
need explicit authorization because they access live Lojix state.

If approved, the activation's intended live effect is: systemd stops any old
daemon instance, invokes the pinned pre-start migrator before configuration
encoding and daemon start, retains the schema-1 backup, and either starts the
schema-2 daemon or fails the pre-start and leaves the canonical source store
unreplaced. The primary risks are the one-way canonical schema transition,
loss of any writes made after a later manual schema-1 rollback, and the need
to keep external writers excluded while migration runs. A successful service
start alone is insufficient; it still requires socket and ordinary-query proof
plus readable deployment-history confirmation before continuing the Bird
deployment.
