# 178 — primary-wdl6: Spirit v0.1.0 Protocol Build

## Summary

`primary-wdl6` is landed. I rebuilt Spirit's v0.1.0 line as a protocol-aware
maintenance build, kept the old Spirit working signal and database schema, tagged
the maintenance build as `v0.1.0.1`, pinned CriomOS-home's `v0.1.0` deployment
slot to that tag, and activated the home profile.

The deployed `v0.1.0` daemon now binds:

- `/home/li/.local/state/persona-spirit/v0.1.0/spirit.sock`
- `/home/li/.local/state/persona-spirit/v0.1.0/owner.sock`
- `/home/li/.local/state/persona-spirit/v0.1.0/upgrade.sock`

The `v0.1.1` daemon is still deployed separately with its ordinary and owner
sockets. The unversioned `spirit` CLI still resolves to `v0.1.0`.

## Commits And Refs

- `persona-spirit` commit: `e7a1b184f09c289eb774020e8bf4f1eaf0e2b54a`
- `persona-spirit` tag: `v0.1.0.1`
- `CriomOS-home` commit: `7bf1fed1a030817b966f85aa9213b2605f4c65ea`

The temporary push bookmark used to publish the `persona-spirit` commit was
removed after the tag was created.

## What Changed

In `persona-spirit`:

- Added `signal-version-handover` and `version-projection` dependencies.
- Added a third private upgrade socket to `DaemonConfiguration`.
- Added upgrade frame codec/client types.
- Added `AskHandoverMarker`, `ReadyToHandover`, and `HandoverCompleted`
  handling through `SpiritRoot`.
- Added handover marker reads from `RecordStore`, backed by
  `sema-engine::current_commit_sequence()`.
- Added a Nix check named `test-v0-1-0-backport-client`.
- Preserved `signal-persona-spirit` at commit
  `b89731f2ae66d56695cb3625986b9747af52a808`, so the old
  Certainty-based working signal remains intact.

In `CriomOS-home`:

- Changed the `persona-spirit-v0-1-0` flake input from tag `v0.1.0` to
  tag `v0.1.0.1`.
- Kept the deployment label and wrapper name as `v0.1.0`.
- Added `upgrade.sock` only to the `v0.1.0` daemon configuration.
- Extended the versioned deployment check to assert the v0.1.0 upgrade socket
  appears in the daemon command and startup cleanup, while v0.1.1 does not get
  the old configuration shape.

## Verification

All Nix calls used `--option max-jobs 0`.

Passed in `persona-spirit`:

- `nix --option max-jobs 0 develop -c cargo test`
- `nix --option max-jobs 0 build .#checks.x86_64-linux.test-v0-1-0-backport-client -L`
- `nix --option max-jobs 0 build .#persona-spirit-daemon -L`
- `nix --option max-jobs 0 flake check -L`

Passed in `CriomOS-home`:

- `nix --option max-jobs 0 build .#checks.x86_64-linux.persona-spirit-versioned-deployment -L`

Activated:

- `lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "github:LiGoldragon/CriomOS-home/main" Activate None None)'`
  with `NIX_CONFIG='max-jobs = 0'`

Runtime checks after activation:

- `systemctl --user is-active persona-spirit-daemon-v0.1.0.service persona-spirit-daemon-v0.1.1.service`
  returned `active` for both.
- The v0.1.0 state directory contains `spirit.sock`, `owner.sock`, and
  `upgrade.sock`.
- `spirit '(Observe (Records ((Some workspace) (Some Decision) SummaryOnly)))'`
  still queries the live v0.1.0 database.

## Designer 175 Impact

`reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md`
does not change the result for `primary-wdl6`; it clarifies the boundary.

This slice implements the marker ceremony for Spirit:

- ask marker
- readiness with echoed marker
- completion that retires old public sockets

The report's larger full protocol still has future work:

- `Mirror` for components with critical in-memory state, especially
  orchestrate.
- `Divergence` as a real abort path instead of mostly typed surface.
- `RecoverFromFailure` semantics.
- Supervisor-driven old/new daemon choreography.

For Spirit, marker-only remains coherent because the designer probe says
acked writes are durable and Spirit has no critical in-memory state that must
mirror. For orchestrate, marker-only is not enough.

## Notes

The maintenance build had to update `sema-engine` to get
`current_commit_sequence()`. That also pulled the current `nota-codec`, so text
rendering in tests moved from quote strings to bracket strings. This does not
change the old Spirit working signal or database record schema.

The NOTA schema-lowering audit in
`reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` remains
orthogonal to this bead. I did not claim schema-language coverage here; this is
only the v0.1.0 protocol-aware maintenance build.
