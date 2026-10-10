# Path-lock epic realization

## Ruling

The path-lock boundary is now a native Datom carrier for exactly a lock name,
a nonempty normalized list of absolute paths, and a one-line description. It
is registered through the ordinary Signal contract. Session, owner,
discipline, authority, mode, release, Dotos compatibility, and generic-report
encodings do not belong to this boundary.

## Architecture

Datom 0.2.0 at `4435f763af57` owns the validated public `PathLock` carrier and
its canonical textual request/replies. Signal Orchestrate 0.15.0/wire3 at
`a038c5c04fea` carries the request as `Register(PathLock)` and has lossless
conversions for `PathLockRegistered` and
`PathLockRegistrationRejected`. Rejection is closed over
`DuplicateActiveName { holder }` and `PathOverlap { path, holder }`.

Meta Signal Orchestrate 0.9.0/wire2 at `f1dec7e3f7b0` pins the final Signal
contract and keeps only `RefreshRepositoryIndex` as its privileged residual.
Orchestrate 0.21.0 at `de59c3f74d7c` uses those types in a durable registry
and its CLI projects typed Datom replies.

## Branch topology

All four repositories carry the same pushed bookmark:
`epic-datom-path-locks-20260822`.

| Repository | Head | Role |
| --- | --- | --- |
| Datom | `4435f763af57` | native validated request and replies |
| Signal Orchestrate | `a038c5c04fea` | ordinary request/reply frames |
| Meta Signal Orchestrate | `f1dec7e3f7b0` | final Signal pin and refresh-only meta surface |
| Orchestrate | `de59c3f74d7c` | durable registry and typed CLI reply projection |

Orchestrate's branch then moved to `c846678319ce` for Beads-only completion
metadata. The audit observed all four workspaces clean and each bookmark equal
to its remote counterpart.

## Behavior and proof

The canonical request is `PathLock.{name [absolute paths] (description)}`.
The response is either `PathLockRegistered.{PathLock.{...}}` or
`PathLockRegistrationRejected.{PathLock.{...} reason}`. Both rejection
reasons retain the holder; an overlap reason additionally retains the
normalized conflicting path.

Construction rejects blank or multiline names/descriptions, empty paths,
relative paths, `..`, and duplicate paths after normalization. The registry
normalizes before conflict testing and rejects every conflicting registration
without a partial insertion. Its isolated scenario uses temporary store and
socket values, waits for inotify events, survives restart, and does not alter
the paths being locked. The independent audit recorded 25 consecutive runs of
that scenario and full `nix flake check -L` success in every epic workspace.

## Boundaries and follow-up

Ethos was deliberately omitted: readiness was not witnessed, and no legacy
Schema was added as a substitute. The unchanged
`signal-orchestrate` `coordination.ethos`/bootstrap text is a known stale,
nonruntime residual rather than part of this behavior.

Bead `orchestrate-fv7` is closed. Its discovered follow-up
`orchestrate-yjo` remains open to give daemon startup one typed configuration
object instead of raw positional paths; it is deliberately outside this epic.

## Sources

- `flows/01a02a34/witnesses/pathLockEpic.md` — code/test and independent-audit witness.
- `flows/01a02a34/vision/datum.md`, `pathLocks.md`, `sandboxedTest.md`, `ethos.md`, and `epicBranches.md` — the written-psyche direction and branch scope.
- `datom@4435f763af57:tests/substrate.rs`; `signal-orchestrate@a038c5c04fea:tests/round_trip.rs`; `meta-signal-orchestrate@f1dec7e3f7b0:Cargo.toml`; `orchestrate@de59c3f74d7c:src/tables.rs` and `tests/path_lock_registry.rs`.
- Beads `orchestrate-fv7` (closed epic) and `orchestrate-yjo` (open `discovered-from` follow-up).
