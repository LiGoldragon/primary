# Orchestrate runtime port

## Landed runtime

Orchestrate 0.31.0 is pushed on `main` at
`1bc55af1859e41a7a8310f05c6b3588b8da47a65`. The workspace has three
packages: the Datom-free `orchestrate-nexus` service, the ordinary
`orchestrate` client, and the privileged `orchestrate-meta` client. It pins
signal-orchestrate 1.0.4 at `0efc9fdada29e72cad839b2941370afadaf880fb`,
meta-signal-orchestrate 1.0.0 at
`7d81bd96b8966988a6cd1fea8ba50888ba92e85a`, and uses Ethos Zero 6.1.2 at
`daf007296a19ad2f9c8a1e67e102b2e3f09db327` for client generation.

The daemon directly restores generated `Query` Signals and signalizes generated
`Response` values. Its transport owns only a little-endian `u32` length prefix;
there is no routed envelope or compatibility decoder. Both clients explicitly
enable their signal crate's `datom` feature and actualize one inline Datom
through `Potential`, then textualize the typed response through the open
Datom/Protos chain. The daemon's normal Cargo dependency edges contain neither
Datom nor Protos.

The Nix package contains five executables:

- `orchestrate-nexus`: zero-argument long-running owner of both sockets and the
  durable store.
- `orchestrate`: ordinary Datom CLI for Lock, Release, and Observe.
- `orchestrate-meta`: privileged Datom CLI for Configure.
- `orchestrate-upgrade-preflight`: read-only retired PathLock-family check.
- `orchestrate-store-migrate`: explicit offline one-shot conversion of the old
  durable Signal archives; it is not a daemon compatibility path.

## Archive decision

The generated named records are not treated as archive-compatible with the
0.30 tuple records. The one-shot migration independently declares the audited
old `Configure`, `Lock`, and allocator layouts, reads the original Sema family
identities, writes new family identities atomically, and retracts the old rows.
Its synthetic witness writes a configuration, two locks containing every field
and multiple paths, and allocator value 9 through independent historical types.
Migration preserves every value, removes the old rows, and the next acquired
Lock receives ID 9.

The installed Sema stack exposes transactional snapshots and recovery
checkpoints inside its database, but no online file-export/backup operation
that can copy this live store while requests continue. The active store is on
plain ext4 rather than a snapshotting filesystem. Therefore this work does not
claim that the synthetic store is a current live snapshot.

At the final controlled cutover, after the declarative pin patch is authorized
and the replacement remains available, stop the old Nexus, copy the latest
store, migrate and validate that isolated copy with both clients and a restart,
then install the new package. Any migration or validation failure must leave
the original store in place and restart the old Nexus. This is the remaining
latest-state witness.

## Deployment boundary

No CriomOS-home file was edited and no production process or state was written.
The exact proposed source, lock, wrapper, and check changes are in
`reports/orchestrate-deployment.patch`. The protected `flake.nix` change still
requires the user's explicit amendment before it may be applied. Production
was read-only checked after staging and remained active as PID 2323 with its
original store.
