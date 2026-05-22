# Spirit Versioned Daemon Cutover

## What Changed

The `persona-spirit` v0.1.0 database was migrated successfully by
`sema-upgrade`, but the running production daemon is still the old v0.1.0
binary. When the migrated v0.1.1 database was temporarily placed at the live
path, the old daemon rejected reads because it cannot interpret the new
`Magnitude`-backed record bytes.

That means the database migration is valid, but live cutover needs a deployment
shape that can run both versions side by side and then switch the user-facing
entry point.

Designer report `reports/designer/278-multi-version-daemon-coexistence.md`
lands the canonical deployment shape. This operator report records the runtime
pressure and points the system-specialist handoff at that design.

## Current Facts

CriomOS-home currently has one `persona-spirit` flake input:

```nix
persona-spirit.url = "github:LiGoldragon/persona-spirit";
```

The current Home Manager module uses that single input for both packages:

```nix
upstreamCommandLine = inputs.persona-spirit.packages.${system}.spirit;
daemon = inputs.persona-spirit.packages.${system}.persona-spirit-daemon;
```

It starts one service and uses unversioned paths:

```nix
ordinarySocketPath = "${stateDirectory}/spirit.sock";
ownerSocketPath = "${stateDirectory}/owner.sock";
storePath = "${stateDirectory}/persona-spirit.redb";
```

The live deployed lock points at `persona-spirit` commit
`694452add7734d0b00954a0d7d4d46bb5d776065`, tagged `v0.1.0`.

Operator update, 2026-05-22: the Spirit-Magnitude work is no longer branch
only. `signal-persona-spirit` main now carries
`5f7d4f4215f7ee0c82641d1dc081c9380bf0e0a1` and tag `v0.1.1`;
`persona-spirit` main now carries
`e137f5de4c663b0cb9a8b52f87d9bdadff80841f` and tag `v0.1.1`.
The former `operator/spirit-response-protocol` branches were deleted.
`sema-upgrade` now depends on `signal-persona-spirit` `branch = "main"` at
the v0.1.1 contract commit.

Terminology correction: `storePath` here is the component's runtime state
database path, not a `/nix/store` path. The Home Manager module currently names
the redb file path `storePath`; in this report, the clearer term is database
path or state path. The Nix package version is a separate surface.

The already-produced migrated database is:

```text
/home/li/.local/state/persona-spirit/persona-spirit.redb.v0.1.1.migrated-20260522075112
```

It contains 103 converted records. It should not be served by the old v0.1.0
daemon.

## Does Versioned Socket Deployment Make Sense?

Yes, with one correction: sockets and stores both need version separation.
Designer report `reports/designer/278-multi-version-daemon-coexistence.md`
picks per-version subdirectories rather than suffixing every filename:

```text
~/.local/state/persona-spirit/
  v0.1.0/
    spirit.sock
    owner.sock
    persona-spirit.redb
  v0.1.1/
    spirit.sock
    owner.sock
    persona-spirit.redb
  current -> v0.1.1
```

The old daemon reads and writes only the old store. The new daemon reads and
writes only the migrated new store. They cannot share one redb file across a
schema-changing cutover.

## CLI Shape

The CLI can follow the same version split without violating the single-argument
rule.

The versioned wrappers are concrete binaries in the user profile:

```text
spirit-v0.1.0
spirit-v0.1.1
```

Each wrapper sets the matching socket environment variables and then execs the
version's real `spirit` package:

```sh
export PERSONA_SPIRIT_SOCKET="$stateDirectory/v0.1.1/spirit.sock"
export PERSONA_SPIRIT_OWNER_SOCKET="$stateDirectory/v0.1.1/owner.sock"
exec ${spirit_v0_1_1}/bin/spirit "$@"
```

The unversioned `spirit` command is a home-managed symlink to the active
versioned wrapper:

```text
spirit -> spirit-v0.1.1
```

From the agent's perspective, `spirit` still takes exactly one NOTA argument.
The wrapper is deployment glue, not a new component protocol.

## Immediate CriomOS-home Shape

For the v0.1.0 to v0.1.1 cutover, CriomOS-home should temporarily carry two
inputs:

```nix
persona-spirit-v0_1_0.url = "github:LiGoldragon/persona-spirit?rev=694452add7734d0b00954a0d7d4d46bb5d776065";
persona-spirit-v0_1_1.url = "github:LiGoldragon/persona-spirit?ref=v0.1.1";
```

Then the module exposes a declarative selector:

```nix
persona-spirit = {
  deployedVersions = [ "v0.1.0" "v0.1.1" ];
  currentDefault = "v0.1.1";
};
```

For each version, generate:

- one daemon user service, for example
  `persona-spirit-daemon-v0.1.1.service`;
- one state directory, for example
  `~/.local/state/persona-spirit/v0.1.1/`;
- one ordinary socket path, for example `v0.1.1/spirit.sock`;
- one owner socket path, for example `v0.1.1/owner.sock`;
- one database path, for example `v0.1.1/persona-spirit.redb`;
- one CLI wrapper, for example `spirit-v0.1.1`.

Then make unversioned `spirit` a symlink to the active wrapper.

## Cutover Sequence

The safe sequence is:

1. Keep v0.1.0 daemon active on `v0.1.0/spirit.sock` and
   `v0.1.0/persona-spirit.redb`.
2. Stop or briefly freeze v0.1.0 writes.
3. Run `sema-upgrade` from the latest v0.1.0 database to a fresh
   `v0.1.1/persona-spirit.redb`.
4. Start v0.1.1 daemon on `v0.1.1/spirit.sock`.
5. Smoke-test v0.1.1 with `spirit-v0.1.1`.
6. Switch unversioned `spirit` to point at `spirit-v0.1.1`.
7. Keep v0.1.0 daemon and DB briefly for rollback.
8. Retire v0.1.0 when the v0.1.1 substrate is trusted.

Because records were added after the first migrated snapshot, the final
cutover must rerun the migration from the latest v0.1.0 database or replay
records written after the migration high-water mark.

## Work Items

Filed `primary-1h0h` for system-specialist: add the versioned Spirit daemon
deployment in CriomOS-home.

Updated `primary-x3ci`: the already-migrated database is preserved, but final
cutover waits for versioned deployment and either a fresh migration or a delta
replay.

The system-specialist should implement from
`reports/designer/278-multi-version-daemon-coexistence.md`. This report's
load-bearing contribution is the runtime finding: the migrated v0.1.1 database
works as data, but the old daemon cannot serve it, so the cutover requires
versioned daemon, socket, store, and CLI surfaces.
