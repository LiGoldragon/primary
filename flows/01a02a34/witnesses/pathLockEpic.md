# Path-lock epic realization

Method: code/test read of the four isolated `epic-datom-path-locks-20260822`
workspaces, followed by an independent audit of their JJ heads, clean working
copies, remote equality, recorded Nix gates, and Orchestrate's isolated
registry scenario.

## Branch topology

| Repository | Final source head | Public version / wire |
| --- | --- | --- |
| Datom | `4435f763af57` | 0.2.0 |
| Signal Orchestrate | `a038c5c04fea` | 0.15.0 / wire 3 |
| Meta Signal Orchestrate | `f1dec7e3f7b0` | 0.9.0 / wire 2 |
| Orchestrate | `de59c3f74d7c` | 0.21.0 |

The Orchestrate bookmark subsequently advanced to `c846678319ce`, whose only
change is the Beads export recording the epic closeout. Every epic workspace
was observed clean, and each epic bookmark resolved to the same commit as its
`origin` remote bookmark.

## Carrier and frame observations

The canonical request form is:

```
PathLock.{datom [/workspace/primary /var/lock] (protect the active paths)}
```

The test normalizes repeated separators and `.` segments before canonical
textualization. It rejects a blank or multiline name or description, an empty
path list, relative paths, `..`, and duplicate normalized paths. The public
carrier is constructed through `PathLock::try_new`; its three stored concepts
are name, paths, and description.

The same native textualization surface establishes these reply forms, not a
generic report or stderr-only reason:

```
PathLockRegistered.{PathLock.{datom [/workspace/primary] (protect the active paths)}}
PathLockRegistrationRejected.{PathLock.{datom [/workspace/primary] (protect the active paths)} DuplicateActiveName.{PathLock.{other [/var/lock] (holds a conflicting path)}}}
PathLockRegistrationRejected.{PathLock.{datom [/workspace/primary] (protect the active paths)} PathOverlap.{/var/lock PathLock.{other [/var/lock] (holds a conflicting path)}}}
```

`datom@4435f763af57:tests/substrate.rs` realizes concrete instances of these
forms and checks their canonical textualization and round trips.

`signal-orchestrate@a038c5c04fea:tests/round_trip.rs` witnesses lossless
Datom-to-Signal-to-Datom conversion for the request, registered reply, and
both rejection forms, as well as the `Register` request frame and typed reply
frames. `meta-signal-orchestrate@f1dec7e3f7b0:Cargo.toml` pins that Signal
revision and retains the narrow `RefreshRepositoryIndex` privileged residual.

## Durable registry observations

`orchestrate@de59c3f74d7c:src/tables.rs` registers a valid lock only after
testing its normalized paths against every active lock; it returns either
`DuplicateActiveName` with the holder or `PathOverlap` with the conflicting
path and holder. The failure happens before insertion, so a conflict is
all-or-nothing.

`orchestrate@de59c3f74d7c:tests/path_lock_registry.rs` exercises direct
registration through temporary store and socket locations, normalized overlap
conflicts, persistence across restart, and non-mutation of the named
filesystem paths. The independent audit recorded in `orchestrate-fv7` ran the
isolated scenario with temporary store/socket locations, inotify event waits,
restart behavior, and filesystem absence/preservation checks for 25
consecutive runs. It also records successful full `nix flake check -L` gates
in all four epic workspaces.

Ethos readiness was examined but not witnessed ready; no Ethos artifact and
no legacy Schema were introduced. The remaining
`signal-orchestrate` `coordination.ethos`/bootstrap text is nonruntime,
stale, and not consumed by this epic.
