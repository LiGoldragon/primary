# Spirit Private Handover Socket

Date: 2026-05-22
Lane: operator
Bead: `primary-x3ci` (Spirit v0.1.1 cutover)

## Result

I implemented the first production-owned private handover surface in
`persona-spirit`.

Repo commits:

- `/git/github.com/LiGoldragon/persona-spirit` `40c0c93e`:
  `persona-spirit: add private handover socket`
- `/git/github.com/LiGoldragon/sema-upgrade` `6aa3a311`:
  `sema-upgrade: wire Spirit next upgrade socket in sandboxes`

## What Changed

`persona-spirit-daemon` now has three socket paths in its
`DaemonConfiguration`:

- ordinary working socket for `signal-persona-spirit`;
- owner policy socket for `owner-signal-persona-spirit`;
- private upgrade socket for `signal-version-handover`.

The upgrade socket handles:

- `AskHandoverMarker` by reading the store's current sema-engine commit
  sequence and last record identifier;
- `ReadyToHandover` by comparing the submitted source marker with the local
  marker;
- `HandoverCompleted` by returning a finalization reply and removing the
  ordinary and owner socket paths.

That means the next Spirit daemon can now prove "I am at this database marker"
and can close its public surface after handover finalization. This is no
longer only an external sema-upgrade model.

`sema-upgrade` now pins to the exact Spirit commit and starts the next
`v0.1.1` sandbox daemon with the upgrade socket path. The old `v0.1.0` daemon
still uses its historical two-socket configuration.

## Verification

All Nix invocations used `--option max-jobs 0`.

In `/git/github.com/LiGoldragon/persona-spirit`:

- `CARGO_BUILD_JOBS=2 cargo fmt --check && CARGO_BUILD_JOBS=2 cargo test`
- `nix flake check --option max-jobs 0 -L`

In `/git/github.com/LiGoldragon/sema-upgrade`:

- `nix flake check --option max-jobs 0 -L`
- `nix run --option max-jobs 0 .#spirit-smart-handover-sandbox -- /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb`

The sandbox output included:

```text
(UpgradeCompleted (persona-spirit (0 1 0) (0 1 1) persona-spirit-0-1-0-to-0-1-1 218))
(SmartHandoverCompleted persona-spirit CurrentPrivateUpgradeOnly NextPublic)
(CurrentWriteBeforeSnapshotAccepted)
(LegacyHighRejected)
(MigratedCurrentWriteObservedByNext)
(NextHighWriteAfterHandoverObserved)
(CurrentDatabaseDidNotReceiveNextOnlyWrite)
```

The new Spirit daemon test
`persona_spirit_daemon_serves_version_handover_frames_through_upgrade_socket`
proves the real upgrade socket path: marker, readiness, completion, and public
socket removal.

## Still Missing

This is not the full zero-downtime production cutover yet.

Remaining work:

- retrofit the deployed `v0.1.0` Spirit daemon with the private handover
  socket, or produce an equivalent protocol-aware `v0.1.0` maintenance build;
- replace the temporary `sema-upgrade-handover-temporary` runner with real
  daemon-to-daemon `signal-version-handover` socket exchanges;
- implement mirrored write payload application on the upgrade socket;
- connect the active-version selector flip in CriomOS-home so the unversioned
  `spirit` command switches only after the handover protocol succeeds.

The current state is a stronger foundation: the next daemon now owns its
handover socket, and the latest live database copy still migrates and tests
cleanly in a Nix sandbox.
