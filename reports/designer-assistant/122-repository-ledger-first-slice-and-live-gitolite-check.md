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

## Readiness Boundary

This slice is locally usable as a deployed development witness, not finished as
a fully green, constraint-complete component.

What is ready:

- The local Gitolite server exists and accepts pushes.
- `repository-ledger.service` is deployed on `ouranos` through production
  CriomOS.
- The ordinary CLI can query the daemon over the ordinary socket.
- The Gitolite post-receive hook now invokes the `repository-ledger` CLI first;
  the CLI speaks the ordinary Signal contract to the daemon.
- The older spool file remains only as a fallback handoff if the CLI submission
  fails.
- Fresh pushes to the `testing` repository are visible through
  `RepositoryEventQuery`.

What is not yet ready:

- The whole constraint suite is not yet complete.
- Mirror execution is not implemented.
- The daemon runtime is synchronous threads plus one store mutex, not the final
  Kameo triad actor topology.
- Repository catalog registration is still owner-signal state; pushes are
  recorded, but repositories do not auto-register into the catalog.

So the correct status is: ready to use for local development observation of
Gitolite pushes on `ouranos`; not yet ready to call complete, green, or
production-shaped.

## Intent Captured

The workflow change was recorded in `intent/workspace.nota`:

Design-phase agents own the first implementation and test pass while the shape
is still being proven; do not hand the prototype to another agent merely
because it crossed from report into code.

Relevant intent commits in `primary`:

- `574e5bed intent: record design-agent owns first implementation`
- `9a2fa931 intent: proceed with repository ledger daemon slice`

## Created Repositories

### signal-repository-ledger

Path: `/git/github.com/LiGoldragon/signal-repository-ledger`

Remote: `gitolite@localhost:signal-repository-ledger`

Initial commit: `8f746959 signal-repository-ledger: add ordinary repository ledger contract`

Latest commits:

- `73f7f517 signal-repository-ledger: add daemon configuration contract`
- `eb55974f signal-repository-ledger: add nix flake checks`

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
nix flake check --option substituters ''
```

Passed.

### owner-signal-repository-ledger

Path: `/git/github.com/LiGoldragon/owner-signal-repository-ledger`

Remote: `gitolite@localhost:owner-signal-repository-ledger`

Initial commit: `b92f35d3 owner-signal-repository-ledger: add owner policy contract`

Latest commits:

- `2e8d37fa owner-signal-repository-ledger: reuse ledger path contract`
- `c5f72586 owner-signal-repository-ledger: use named signal dependency`
- `f6d28873 owner-signal-repository-ledger: add nix flake checks`

Surface:

- Owner-only repository registration and retirement.
- Spool directory policy.
- Future mirror policy records.
- Reuses the ordinary contract's `RepositoryLedgerPath` so the daemon
  configuration and owner policy use one path vocabulary.

Verification:

```sh
cargo test
nix flake check --option substituters ''
```

Passed.

### repository-ledger

Path: `/git/github.com/LiGoldragon/repository-ledger`

Remote: `gitolite@localhost:repository-ledger`

Initial commit: `5c4e1465 repository-ledger: add sema-engine backed first slice`

Latest commits:

- `ff89f6fd repository-ledger: add live daemon and cli slice`
- `419367e7 repository-ledger: add flake package and named contract refs`

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
nix flake check --option substituters ''
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

Remote refs exist on the live Gitolite server. The initial ref witness was:

- `signal-repository-ledger` main -> `8f746959c542`
- `owner-signal-repository-ledger` main -> `b92f35d3d806`
- `repository-ledger` main -> `5c4e14653d7a`

Later pushes moved the same `main` bookmarks forward:

- `signal-repository-ledger` main -> `73f7f517b9e3`
- `owner-signal-repository-ledger` main -> `c5f725860ea5`
- `repository-ledger` main -> `419367e73405`

The Nix-check pushes then moved the contract repos again:

- `signal-repository-ledger` main -> `eb55974fe1a2`
- `owner-signal-repository-ledger` main -> `f6d28873566f`

The deployed ledger recorded those two pushes too:

- event 13: `owner-signal-repository-ledger` moved from `c5f725860ea5` to
  `f6d28873566f`, with `daemon_socket_present true`.
- event 14: `signal-repository-ledger` moved from `73f7f517b9e3` to
  `eb55974fe1a2`, with `daemon_socket_present true`.

That proves Gitolite accepted real pushes for all three new repos and can serve
them back to Nix as named branch references.

After CriomOS commit `49d499e4`, the deployed post-receive hook submits the
canonical `RepositoryReceiveHookNotification` through the `repository-ledger`
CLI before falling back to spool. A fresh push to `testing` produced:

- event 15: `testing` moved from `04ee09ccd97a` to `60accb6ba044`, with
  `daemon_socket_present true`.

The event was visible through `RepositoryEventQuery` immediately after the push.
The daemon's fallback spool loop runs every two seconds, so this is the runtime
witness for the direct hook -> CLI -> daemon path.

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

Production CriomOS now creates and deploys:

- `repository-ledger` system user.
- `repository-ledger` system group.
- `repository-ledger-receive` shared group containing `gitolite` and
  `repository-ledger`.
- `/var/lib/repository-ledger` as `2770 repository-ledger:repository-ledger-receive`.
- `/var/lib/repository-ledger/spool` as `2770 gitolite:repository-ledger-receive`.
- `/run/repository-ledger` as `0755 repository-ledger:nixdev`.
- `repository-ledger.service`, running
  `repository-ledger-daemon` as user `repository-ledger`, primary group
  `nixdev`, with supplementary membership in `repository-ledger` and
  `repository-ledger-receive`.
- The `repository-ledger` CLI package in the system environment, so trusted
  development users can query the ordinary socket from the shell.

The post-receive hook now writes notification files with group
`repository-ledger-receive` and mode `0640`.

Runtime witness after deploying locally on `ouranos`:

- `systemctl is-active repository-ledger.service` returned `active`.
- `/run/repository-ledger/repository-ledger.sock` exists as
  `srw-rw---- repository-ledger:nixdev`.
- `/run/repository-ledger/repository-ledger-owner.sock` exists as
  `srw------- repository-ledger:nixdev`; the group name is present but the mode
  keeps the owner socket daemon-only.
- `repository-ledger '(RepositoryCatalogQuery)'` returned
  `(RepositoryCatalogListing [])`.
- The daemon drained the existing Gitolite spool into typed Sema state.
- A fresh push to `testing` after the daemon was deployed committed event 11.
- After the runtime directory was opened to `0755`, a second fresh push to
  `testing` committed event 12 with `daemon_socket_present true`.
- After the hook was changed to call the ledger CLI first, another fresh push to
  `testing` committed event 15 immediately through the ordinary daemon socket.
- After the hook was enriched to send `RepositoryPushObservation`, a fresh push
  to `testing` committed event 18 and the new file/commit-message query
  surfaces returned the changed file and commit message for that push.

Verification:

- `lojix-cli '(FullOs goldragon ouranos ".../datom.nota" "github:LiGoldragon/CriomOS/main" Switch None [])'`
  completed successfully for the service package, the `nixdev` client socket
  correction, the runtime-directory presence correction, and the direct
  hook-to-CLI correction.
- The focused `repository-receive-role-policy` check passed through a direct
  Nix expression using the real flake inputs. A normal `checks.x86_64-linux.*`
  build still needs generated `system` and `horizon` overrides because CriomOS
  intentionally ships stub defaults for those inputs.

CriomOS commits:

- `9c28cc7c criomos: run repository ledger daemon on gitolite hosts`
- `c518d23b criomos: expose repository ledger client socket to nixdev`
- `a1a2f3ef criomos: let gitolite witness repository ledger socket presence`
- `49d499e4 criomos: submit repository hook through ledger cli`
- `349cb988 criomos: enrich repository ledger hook observations`

Repository contract/runtime commits:

- `f9420c13 signal-repository-ledger: add agent discovery query contract`
- `d52298c4 repository-ledger: add repository activity discovery queries`

## Current Ledger Entry Schema

The direct hook now submits a typed push observation. In pseudo-NOTA, the entry
shape is:

```nota
(RepositoryPushObservation
  (RepositoryReceiveHookNotification
    "testing"
    "gitolite-admin"
    "20260519T142920Z"
    true
    [(RefUpdate "old-commit" "new-commit" "refs/heads/main")])
  [(RepositoryCommitObservation
      "new-commit"
      "refs/heads/main"
      "2026-05-19T16:29:10+02:00"
      "verify repository ledger query capture"
      [(RepositoryFileChange "A" "ledger-query-live-witness.txt" None)])])
```

The daemon stores this as:

- a push event row keyed by `RepositoryEventSequence`;
- one commit-observation row per pushed commit, carrying repository name,
  received-at timestamp, event sequence, commit object id, ref name, commit
  timestamp, full commit message, and changed-file records.

The fallback spool shape remains the older `RepositoryReceiveHookNotification`.
Fallback records keep the push event but do not carry commit-message or
changed-file observations.

## Agent Queries Now Available

Recently edited repositories:

```nota
(RepositoryRecentRepositoriesQuery None 5)
```

Live reply after the enriched hook deploy included:

```nota
(RepositoryRecentRepositoriesListing
  [(RepositoryRecentRepository testing "20260519T142920Z" 18 5)
   (RepositoryRecentRepository repository-ledger "20260519T142650Z" 17 4)
   (RepositoryRecentRepository signal-repository-ledger "20260519T142503Z" 16 4)])
```

Changed files by repository, time window, and path substring:

```nota
(RepositoryChangedFileQuery testing None None ledger-query 10)
```

Live reply:

```nota
(RepositoryChangedFileListing
  [(RepositoryChangedFile
      testing
      "20260519T142920Z"
      18
      b28db60d3ee1e7ae3adc2d1538e048356ef1f56d
      "refs/heads/main"
      A
      "ledger-query-live-witness.txt"
      None)])
```

Commit-message substring search:

```nota
(RepositoryCommitMessageQuery testing None None "query capture" 10)
```

Live reply:

```nota
(RepositoryCommitListing
  [(RepositoryCommit
      testing
      "20260519T142920Z"
      18
      b28db60d3ee1e7ae3adc2d1538e048356ef1f56d
      "refs/heads/main"
      "2026-05-19T16:29:10+02:00"
      "verify repository ledger query capture")])
```

More useful query directions to consider next:

- repository activity grouped by role/class once owner catalog registration is
  ergonomic;
- "show me reports landed since timestamp X";
- "show me architecture files changed since timestamp X";
- "show me pushes that touched both a contract repo and a runtime repo";
- "show me commits whose changed files match a glob or prefix";
- "show me commits by author/committer once the hook captures those fields";
- "show me repositories with pushes not mirrored yet" after mirror execution
  lands.

One syntax gap surfaced during the live query check: the current generated
channel request parser accepts present optional query fields as bare values
(`testing`) rather than canonical `(Some "testing")`. The contract records are
still typed as `Option<T>`, but the CLI examples above show the working request
surface. This should be reconciled in the `signal_channel!` request syntax work
so generated channel CLI NOTA matches the workspace's explicit `Some` rule.

## Newly Closed In This Pass

- Daemon ordinary socket handler.
- Daemon owner-signal socket handler.
- Spool consumer for the current CriomOS receive-hook NOTA shape.
- Thin query CLI that talks to the daemon.
- Tests for ordinary Signal request/reply, owner Signal mutation, and spool
  ingestion with move-to-processed after commit.
- Tests for recent-repository, changed-file, and commit-message discovery
  queries.
- Nix flake packaging for `repository-ledger`.
- Nix flake checks for `signal-repository-ledger` and
  `owner-signal-repository-ledger`.
- Production CriomOS service packaging and local deployment on `ouranos`.
- Live post-deploy Gitolite push witness through the spool fallback and then
  through the direct hook -> CLI -> daemon path into Sema state.
- Live post-deploy Gitolite push witness proving direct hook enrichment into
  changed-file and commit-message Sema state.

## Not Yet Implemented

- Mirror execution to GitHub or any other remote.
- Kameo actor topology. The handlers are split by socket and behavior, but the
  first live runtime is synchronous threads over one store mutex. That is
  acceptable for proving the boundary and should be replaced with the standard
  triad actor layout when the service is packaged.
- Repository registration is still manual owner-signal state. Push events are
  recorded, but the catalog stays empty until an owner request registers a repo.
- Generated channel request NOTA currently accepts bare present option values
  at the CLI surface; canonical `(Some value)` should be restored or explained
  in the `signal_channel!` macro design.

The implementation now has enough contract, sema-engine state, socket, and CLI
shape for the next slice to be concrete: add owner CLI/configuration ergonomics
for repository registration, add mirror execution, and then replace the current
synchronous runtime with the standard triad actor layout.
