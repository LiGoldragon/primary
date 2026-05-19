# Repository Ledger First Slice And Live Gitolite Check

## Result

The live Gitolite premise is true on `ouranos`.

`ssh gitolite@localhost info` reports Gitolite 3.6.14 and now lists:

- `repository-ledger`
- `signal-repository-ledger`
- `owner-signal-repository-ledger`
- `gitolite-admin`
- `testing`

The three repository-ledger repos were created through `gitolite-admin` and
pushed with initial `main` branches.

## Intent Captured

The workflow change was recorded in `intent/workspace.nota`:

Design-phase agents own the first implementation and test pass while the shape
is still being proven; do not hand the prototype to another agent merely
because it crossed from report into code.

Commit in `primary`: `574e5bed intent: record design-agent owns first implementation`.

## Created Repositories

### signal-repository-ledger

Path: `/git/github.com/LiGoldragon/signal-repository-ledger`

Remote: `gitolite@localhost:signal-repository-ledger`

Initial commit: `8f746959 signal-repository-ledger: add ordinary repository ledger contract`

Latest commit: `73f7f517 signal-repository-ledger: add daemon configuration contract`

Surface:

- `RepositoryReceiveHookNotification` matches the current CriomOS Gitolite
  post-receive spool record.
- Ordinary `signal_channel!` variants:
  - `Assert RepositoryReceiveHookNotification`
  - `Match RepositoryEventQuery`
  - `Match RepositoryCatalogQuery`
- Replies for recorded events, event listings, catalog listings, and typed
  unimplemented responses.
- `RepositoryLedgerDaemonConfiguration`, the typed daemon startup record for
  ordinary socket, owner socket, store path, and spool directory.

Verification:

```sh
cargo test
```

Passed.

### owner-signal-repository-ledger

Path: `/git/github.com/LiGoldragon/owner-signal-repository-ledger`

Remote: `gitolite@localhost:owner-signal-repository-ledger`

Initial commit: `b92f35d3 owner-signal-repository-ledger: add owner policy contract`

Latest commit: `2e8d37fa owner-signal-repository-ledger: reuse ledger path contract`

Surface:

- Owner-only repository registration and retirement.
- Spool directory policy.
- Future mirror policy records.
- Reuses the ordinary contract's `RepositoryLedgerPath` so the daemon
  configuration and owner policy use one path vocabulary.

Verification:

```sh
cargo test
```

Passed.

### repository-ledger

Path: `/git/github.com/LiGoldragon/repository-ledger`

Remote: `gitolite@localhost:repository-ledger`

Initial commit: `5c4e1465 repository-ledger: add sema-engine backed first slice`

Latest commit: `ff89f6fd repository-ledger: add live daemon and cli slice`

Surface:

- `RepositoryLedgerStore` opens a `sema-engine` database.
- Hook notifications commit as typed `StoredRepositoryEvent` records.
- Repository registrations commit as typed catalog records.
- `repository-ledger-daemon` accepts one typed
  `RepositoryLedgerDaemonConfiguration` argument, binds ordinary and owner
  sockets, drains the current Gitolite spool projection, and answers Signal
  request frames.
- `repository-ledger` is a thin ordinary-contract client: it accepts one NOTA
  request payload, connects only to the repository-ledger daemon, wraps the
  payload in a Signal request frame, and prints the domain reply payload as
  NOTA.

Verification:

```sh
cargo test
```

Passed.

Additional live binary smoke in this pass:

```sh
repository-ledger-daemon '(RepositoryLedgerDaemonConfiguration ...)'
REPOSITORY_LEDGER_SOCKET_PATH=<ordinary-socket> repository-ledger '(RepositoryCatalogQuery)'
```

Observed reply:

```nota
(RepositoryCatalogListing [])
```

## Workspace Registry Update

`protocols/active-repositories.md` now includes the three new repos.

Commit in `primary`: `9c628bfa protocols: add repository ledger repositories`.

## Live Push Verification

Remote refs exist on the live Gitolite server:

- `signal-repository-ledger` main -> `8f746959c542`
- `owner-signal-repository-ledger` main -> `b92f35d3d806`
- `repository-ledger` main -> `5c4e14653d7a`

That proves Gitolite accepted real pushes for all three new repos.

## Original Spool Boundary Gap

Status as of CriomOS commit `717504ab`: resolved on `ouranos` for the
current production Gitolite slice.

Before the production CriomOS fix, the hook path was not a proven daemon
handoff.

Observed on `ouranos`:

```text
/var/lib/repository-ledger        mode 0750 owner gitolite group gitolite
/var/lib/repository-ledger/spool  unreadable by li
```

The CriomOS hook also sets:

```sh
umask 077
```

That means notification files are likely `0600 gitolite:gitolite`. A future
`repository-ledger-daemon` running as its own per-component Unix user will not
be able to read them unless the system layer changes the handoff boundary.

This mattered because the component-triad / owner-signal direction points toward
a dedicated daemon identity, not running the repository ledger daemon as the
`gitolite` user.

Recommended system shape, now implemented in CriomOS:

- Create a dedicated `repository-ledger` Unix user for the daemon.
- Create a shared receive group, for example `repository-ledger-receive`.
- Put both `gitolite` and `repository-ledger` in that group.
- Make the spool directory `2770 gitolite:repository-ledger-receive`.
- Make hook output files group-readable, either with `umask 007` or an explicit
  `chmod 0640` after writing.

This gap is closed for the current local production slice.

## Resolution Witness

Production CriomOS now creates:

- `repository-ledger` system user.
- `repository-ledger` system group.
- `repository-ledger-receive` shared group containing `gitolite` and
  `repository-ledger`.
- `/var/lib/repository-ledger` as `2770 repository-ledger:repository-ledger-receive`.
- `/var/lib/repository-ledger/spool` as `2770 gitolite:repository-ledger-receive`.
- `/run/repository-ledger` as `0750 repository-ledger:repository-ledger-receive`.

The post-receive hook now writes notification files with group
`repository-ledger-receive` and mode `0640`.

Runtime witness after deploying locally on `ouranos`:

- A fresh push to the `testing` Gitolite repository created a
  `RepositoryReceiveHookNotification` file.
- The file landed as `0640 gitolite:repository-ledger-receive`.
- `runuser -u repository-ledger -- test -r <latest-spool-file>` returned
  success.
- The `repository-ledger` user could read the NOTA notification content.
- The pre-existing spool files from before the fix were normalized to
  `0640 gitolite:repository-ledger-receive`, so the future daemon can read
  the whole current queue.

Verification:

- `lojix-cli '(FullOs goldragon ouranos ".../datom.nota" "github:LiGoldragon/CriomOS/main" Switch None [])'`
  completed successfully.
- `checks.x86_64-linux.repository-receive-role-policy` passed with the
  generated production `system` and `horizon` inputs.

## Newly Closed In This Pass

- Daemon ordinary socket handler.
- Daemon owner-signal socket handler.
- Spool consumer for the current CriomOS receive-hook NOTA shape.
- Thin query CLI that talks to the daemon.
- Tests for ordinary Signal request/reply, owner Signal mutation, and spool
  ingestion with move-to-processed after commit.

## Not Yet Implemented

- Direct hook-to-daemon Signal submission.
- Mirror execution to GitHub or any other remote.
- Nix flake checks for the three new repos. The current witness is `cargo test`
  plus the live binary smoke; the workspace testing discipline wants these
  surfaced as named Nix checks next.
- Production CriomOS service packaging for `repository-ledger-daemon`; the
  current production deployment has the Gitolite hook and filesystem handoff,
  not the daemon unit.
- Kameo actor topology. The handlers are split by socket and behavior, but the
  first live runtime is synchronous threads over one store mutex. That is
  acceptable for proving the boundary and should be replaced with the standard
  triad actor layout when the service is packaged.

The implementation now has enough contract, sema-engine state, socket, and CLI
shape for the next slice to be concrete: package the daemon as a local CriomOS
service on `ouranos`, add the Nix checks, then replace the temporary spool loop
with direct hook-to-daemon Signal delivery.
