# Spirit Smart Handover Sandbox Test

Date: 2026-05-22
Lane: operator
Beads: `primary-x3ci`, `primary-a5hu`

## Result

I added and ran a Nix-owned smart-handover sandbox in `sema-upgrade`.

The successful command was:

```sh
nix run --option max-jobs 0 .#spirit-smart-handover-sandbox -- /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb
```

The sandbox output:

```text
(UpgradeCompleted (persona-spirit (0 1 0) (0 1 1) persona-spirit-0-1-0-to-0-1-1 217))
(SmartHandoverCompleted persona-spirit CurrentPrivateUpgradeOnly NextPublic)
(CurrentWriteBeforeSnapshotAccepted)
(LegacyHighRejected)
(MigratedCurrentWriteObservedByNext)
(NextHighWriteAfterHandoverObserved)
(CurrentDatabaseDidNotReceiveNextOnlyWrite)
(SmartHandoverSandboxSucceeded ("/home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb"))
```

## What The Sandbox Proves

The new app uses the latest deployed `v0.1.0` Spirit database as input without
mutating it. Inside a temporary sandbox it:

1. copies the current `v0.1.0` database;
2. starts the tagged `persona-spirit` `v0.1.0` daemon against that copy;
3. writes a legacy-compatible `Maximum` record through the `v0.1.0` CLI;
4. proves `v0.1.0` rejects `High`;
5. snapshots the sandbox `v0.1.0` database after that write;
6. migrates the snapshot to `v0.1.1`;
7. starts the tagged `persona-spirit` `v0.1.1` daemon against the migrated copy;
8. verifies the pre-snapshot current write is visible through `v0.1.1`;
9. runs the current `signal-version-handover` protocol prototype;
10. flips the sandbox public selector from current to next;
11. writes a `High` record through `v0.1.1`;
12. verifies the `High` record is visible through `v0.1.1`;
13. verifies the `v0.1.0` database did not receive the next-only write.

The migration converted 217 records in this run.

## Code Changed

Repo: `/git/github.com/LiGoldragon/sema-upgrade`

- Added flake input `persona-spirit-v0-1-0` pinned to tag `v0.1.0`.
- Added package/app `spirit-smart-handover-sandbox`.
- Added `sema-upgrade-handover-temporary`, a one-argument protocol runner for
  the current `PrototypeHandover::for_spirit_0_1_0_to_0_1_1` path.
- Updated `README.md` and `ARCHITECTURE.md` with the new sandbox surface.

## Verification

All Nix invocations used `--option max-jobs 0`.

- `CARGO_BUILD_JOBS=2 cargo fmt --check`
- `CARGO_BUILD_JOBS=2 cargo test`
- `nix run --option max-jobs 0 .#spirit-smart-handover-sandbox -- /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb`
- `nix flake check --option max-jobs 0 -L`

All passed.

## Important Limitation

This is the strongest sandbox we can run with the code that exists today, but
it is not yet the final production smart handover.

The two real Spirit daemons are used for the database and CLI sides. The
handover protocol itself is still exercised through
`sema-upgrade-handover-temporary`, because `persona-spirit-daemon` does not yet
bind or serve a real private `signal-version-handover` upgrade socket.

So the state is now:

- database copy/migrate from latest `v0.1.0` state: proven;
- two tagged Spirit daemon versions in one sandbox: proven;
- selector behavior current → next: proven in the sandbox script;
- next-only `High` write after handover: proven;
- old database not receiving next-only write: proven;
- production Spirit-owned private upgrade socket: still missing.

The next implementation slice should retrofit `persona-spirit` `v0.1.0` and
`v0.1.1` so each daemon owns the private handover socket directly. Then this
same sandbox should stop using `sema-upgrade-handover-temporary` and send
`signal-version-handover` frames to real daemon sockets.
