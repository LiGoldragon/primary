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

Commit: `8f746959 signal-repository-ledger: add ordinary repository ledger contract`

Surface:

- `RepositoryReceiveHookNotification` matches the current CriomOS Gitolite
  post-receive spool record.
- Ordinary `signal_channel!` variants:
  - `Assert RepositoryReceiveHookNotification`
  - `Match RepositoryEventQuery`
  - `Match RepositoryCatalogQuery`
- Replies for recorded events, event listings, catalog listings, and typed
  unimplemented responses.

Verification:

```sh
cargo test
```

Passed.

### owner-signal-repository-ledger

Path: `/git/github.com/LiGoldragon/owner-signal-repository-ledger`

Remote: `gitolite@localhost:owner-signal-repository-ledger`

Commit: `b92f35d3 owner-signal-repository-ledger: add owner policy contract`

Surface:

- Owner-only repository registration and retirement.
- Spool directory policy.
- Future mirror policy records.

Verification:

```sh
cargo test
```

Passed.

### repository-ledger

Path: `/git/github.com/LiGoldragon/repository-ledger`

Remote: `gitolite@localhost:repository-ledger`

Commit: `5c4e1465 repository-ledger: add sema-engine backed first slice`

Surface:

- `RepositoryLedgerStore` opens a `sema-engine` database.
- Hook notifications commit as typed `StoredRepositoryEvent` records.
- Repository registrations commit as typed catalog records.
- Placeholder CLI and daemon binaries accept exactly one argument and report
  typed unimplemented output until socket actors land.

Verification:

```sh
cargo test
```

Passed.

## Workspace Registry Update

`protocols/active-repositories.md` now includes the three new repos.

Commit in `primary`: `9c628bfa protocols: add repository ledger repositories`.

## Live Push Verification

Remote refs exist on the live Gitolite server:

- `signal-repository-ledger` main -> `8f746959c542`
- `owner-signal-repository-ledger` main -> `b92f35d3d806`
- `repository-ledger` main -> `5c4e14653d7a`

That proves Gitolite accepted real pushes for all three new repos.

## Critical Spool Boundary Gap

The current CriomOS hook path is not yet a proven daemon handoff.

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

This matters because the component-triad / owner-signal direction points toward
a dedicated daemon identity, not running the repository ledger daemon as the
`gitolite` user.

Recommended system shape:

- Create a dedicated `repository-ledger` Unix user for the daemon.
- Create a shared receive group, for example `repository-ledger-receive`.
- Put both `gitolite` and `repository-ledger` in that group.
- Make the spool directory `2770 gitolite:repository-ledger-receive`.
- Make hook output files group-readable, either with `umask 007` or an explicit
  `chmod 0640` after writing.

Until this lands, Gitolite is live and pushable, but the hook-to-daemon spool
handoff is not yet proven under the intended OS security model.

## Not Yet Implemented

- Daemon ordinary socket actor.
- Daemon owner-signal socket actor.
- Spool consumer.
- Direct hook-to-daemon Signal submission.
- Mirror execution to GitHub or any other remote.
- Query CLI that talks to the daemon.

The implementation now has enough contract and sema-engine state shape for the
next slice to be concrete: build the daemon actor tree and consume the spool
under the corrected filesystem handoff.
