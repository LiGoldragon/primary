# Lojix schema-1 to schema-2 migration proposal

## Decision

Lojix is the deployed typed deploy orchestrator. It is distinct from the
unresolved term “Logics” and from the Logos family. This proposal concerns only
Lojix’s durable store at `/var/lib/lojix/lojix.sema`.

The smallest durable repair is already present in the current source line:

- Lojix `main` at `9adc6c75b8be85edc64c4eb14c27376bb0388dd7` adds the
  `lojix-migrate-store` pre-start binary, reconstruction code, and migration
  tests.
- CriomOS `main` at `475bf5c27efa` runs that binary as the first
  `lojix-daemon` `ExecStartPre` action.
- CriomOS’s locked `lojix` input already resolves to the Lojix migration
  revision above.

Consequently, no backport and no replacement/deletion of the existing store is
called for. The next lane is source verification, declarative activation, and
live proof. Source changes are only warranted if one of the explicit gates
below fails.

## What is implemented

`src/reconstruction.rs` is wired into the package and is invoked by
`src/bin/lojix-migrate-store.rs`. It accepts exactly one store path and has the
following protocol.

1. It opens the source through `redb::ReadOnlyDatabase`, checks schema version
   and the complete six-table catalog, decodes all known rows, checks keys and
   cross-table relations, and constructs an in-memory snapshot.
2. For schema 1, it creates
   `lojix.sema.schema-v1.backup` as a non-overwriting hard link, confirms its
   bytes and ownership/mode, and `fsync`s the parent directory.
3. It constructs a new schema-2 store at
   `lojix.sema.schema-v2.pending`, seeds the validated six-table snapshot as
   an atomic seed commit, restores the original ownership/mode, `fsync`s it,
   reopens it through the normal `Store` startup gate, and compares all six
   counts.
4. It atomically renames the staged schema-2 file over `lojix.sema`, syncs the
   parent directory, reopens the canonical store again, and verifies counts.
5. It returns `AlreadyCurrent` without rewriting a schema-2 store, and returns
   `NoStore` without creating one for a missing store.

The permanent backup is the original schema-1 inode. Once the atomic rename
has completed, it is independent from the new canonical schema-2 file and
remains the recovery witness. The live materialized records, including the
deployment event-log rows, are copied exactly by the fixture witness. The
schema-2 engine history is necessarily reconstructed as a new seed commit; the
original file and its original storage-level history remain available in the
permanent schema-1 backup.

The fixture is source-generated rather than a checked-in live-store sample:
`tests/schema_one_migration.rs` creates a genuine schema-1 `sema-engine`
database, with representative rows in all six families, then proves complete
row equality after migration. It also covers empty registered tables, sparse
identifier allocation, retry after tool-owned partial staging, idempotent
schema-2 rerun, corrupt input, broken relationships/keys, conflicting backup
or staging paths, metadata preservation, and the one-positional-argument CLI
contract. This is the correct fixture boundary: it contains no production
payload.

`modules/nixos/lojix.nix` declaratively orders the migration before
configuration encoding and daemon startup:

```nix
ExecStartPre = [
  "${lojixPackage}/bin/lojix-migrate-store ${storePath}"
  "${lojixPackage}/bin/lojix-write-configuration ${startupRequest}"
];
```

The package’s `Cargo.toml` includes the migration binary, so no separate Nix
package is required.

## Preservation, atomicity, and interruption

The daemon must be stopped while the migrator runs. The declared systemd
pre-start ordering provides that mutual exclusion for normal operation; no
operator should run the migrator concurrently with a manually started daemon
or another store writer.

| Interruption point | Canonical store after restart | Recovery behavior |
| --- | --- | --- |
| Before validation / backup | Original schema 1 | Nothing is replaced; startup remains stopped on validation failure. |
| After backup, before replacement | Original schema 1 plus permanent backup and possibly tool-owned staging marker | A retry validates the backup ownership marker, discards only its owned staging file, and reconstructs again. |
| During staging reconstruction | Original schema 1 plus backup | Retry removes only staging proven to be owned by the tool. Unknown staging is refused, never overwritten. |
| Atomic rename | Either the complete schema-1 canonical file or the complete schema-2 staged file | No partial canonical database is selected; the schema-1 backup remains. |
| After rename, before post-check/marker cleanup | Complete schema 2 plus permanent schema-1 backup | The next invocation observes schema 2 and does not rewrite it; normal startup may proceed after the daemon’s usual open gate. |

Two limits should remain explicit:

- The hard-link backup is deliberately byte-identical and permanent after
  replacement, but it is not an independent copy before the rename. The
  systemd service boundary is therefore the mutual-exclusion safety condition.
  The current byte-comparison after hard-linking cannot detect a concurrent
  external writer because both names refer to the same inode.
- A crash after rename may leave the harmless owned `.schema-v2.pending.owner`
  marker. Current behavior is safe and idempotent, but it does not clean that
  marker on the schema-2 fast path. A small follow-up may add proven-owned
  marker cleanup plus a fault-injection test; it is hygiene, not a blocker to
  preserving or serving the migrated store.

## Exact implementation lane

No change should be made directly in a shared checkout. The implementer first
claims `primary-akw` and the exact source paths with Orchestrate. If a source
gate below fails, request isolated worktrees for Lojix and CriomOS, claim the
specific files, and keep the repair to these surfaces:

| Repository | Required mutation if the current commits are unavailable or fail a gate |
| --- | --- |
| `lojix` | Keep `src/reconstruction.rs`, `src/bin/lojix-migrate-store.rs`, `src/lib.rs`, the binary entry in `Cargo.toml`, and `tests/schema_one_migration.rs` as one migration contract. Add only a narrow recovery test/cleanup if the post-rename-marker case is chosen. |
| `CriomOS` | Pin the validated Lojix revision in `flake.lock` and retain the migration as the first `ExecStartPre` in `modules/nixos/lojix.nix`. Do not alter the runtime store manually. |
| `lojix-inspect-store` | No mutation. Its working copy is stale at its read-only-inspection commit while its `main` reference points at the migration line; it was inspected read-only and must not be used as a repair workspace. |

Existing committed source means the expected mutation set for this incident is
zero. The deployment commit must nevertheless be built from the exact locked
CriomOS revision, not from an unmanaged working copy.

## Proof gates and authorized execution order

These are commands for the follow-on activation lane, not commands executed
by this design task.

1. Confirm Lojix and CriomOS `main` contain the two revisions named above and
   that their required bookmarks are pushed. In Lojix, run the repository
   durable gate, including:

   ```sh
   cargo test --locked --test schema_one_migration
   cargo test --locked
   nix flake check
   ```

2. Evaluate and build the locked CriomOS host shape with the materialized
   `system`, `horizon`, `deployment`, and `secrets` inputs as specified by
   CriomOS’s AGENTS contract. Run evaluation and build separately, from the
   pushed source, with refresh. The package closure must contain both
   `lojix-daemon` and `lojix-migrate-store`.

3. Before activation, use only `lojix-inspect-store` against the live path if
   a fresh non-sensitive witness is needed. Record schema state, catalog
   readability, and row counts only; do not print or copy record payloads.
   The expected precondition is schema 1, not an inferred content shape.

4. Activate the declarative CriomOS generation. Systemd runs the migration
   before daemon start. Accept only a successful pre-start result naming either
   `StoreMigrated` with the permanent backup or `StoreMigrationNotNeeded` for
   schema 2. A rejected migration leaves the old canonical source in place and
   stops the daemon: investigate the explicit validation error rather than
   bypassing the unit or editing the store.

5. Prove the daemon is serving, not merely active: require an active
   `lojix-daemon.service`, both expected Unix sockets, and a successful
   ordinary query over the real socket. The source’s current NOTA fixture form
   is:

   ```sh
   lojix "(Query ((ByNode (goldragon ouranos None))))"
   ```

   The reply must be a decoded service response and must preserve readable
   prior deployment history. Socket existence, an `ExecStart` PID, or a
   `DeployAccepted` response alone is insufficient.

6. Only after gate 5, continue `primary-akw`’s Bird deployment using the
   normal owner-socket path from `li@ouranos`, an immutable CriomOS reference,
   and the materialized proposal source:

   ```sh
   meta-lojix "(Deploy (UserEnvironment (goldragon zeus bird <proposal-source> github:LiGoldragon/CriomOS?rev=<full-commit> ActivateNow RequireImmutable None [])))"
   lojix "(Query ((ByNode (goldragon zeus None))))"
   ```

   Wait for the durable generation/event result, then verify on Zeus as Bird:

   ```sh
   codium --list-extensions --show-versions
   ```

   The acceptance value is `openai.chatgpt@26.5721.30844`, or a deliberately
   later pinned version with matching extension contents. The submission reply
   admits a deployment; it is not completion evidence.

## Downgrade and rollback

The migration is one-way at the canonical path. A system rollback to a daemon
that also understands schema 2 may be operationally possible, but it is not a
tested data rollback. A daemon expecting schema 1 cannot open the migrated
canonical file.

Restoring schema 1 must be an explicit, stopped-daemon recovery operation: keep
the current schema-2 file intact under a new recovery name, restore the
permanent schema-1 backup as canonical, and run only a schema-1-capable daemon.
That restores the pre-migration state and necessarily omits writes accepted by
the schema-2 daemon after migration. It must never be embedded in ordinary
NixOS generation rollback or an automatic recovery action. Forward migration
from the retained backup remains available after the incident is understood.

## Approval statement

Approved for the narrow execution lane only: validate the already-committed
Lojix and CriomOS revisions, declaratively activate the pinned generation, and
continue to Bird/Codium only after the live schema-2 daemon serves the
ordinary query and preserves readable history. This approval does not authorize
backporting, manual store edits, deleting/replacing the store, automatic
downgrade restoration, or treating Lojix as “Logics.”
