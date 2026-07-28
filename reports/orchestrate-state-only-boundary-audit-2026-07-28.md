# Orchestrate state-only boundary audit — 2026-07-28

## Ruled boundary

Orchestrate retains its Sema database and Unix sockets. It performs no
repository/worktree/path scanning, `/proc` inspection, ad-hoc mirror or lock
projection, VCS subprocess work, or other non-state-infrastructure filesystem
behavior. `Observe` and `Query` are pure store projections. Worktree, claim,
and repository lifecycle may remain only as typed Sema state supplied by
requests.

## Current result

The boundary is not met at source revision `390f4f86` (parent `83e09a13`).
That change removed only the `worktrees.nota` projection.

Every ordinary request, including `Observe` and `Query`, currently travels
through `CommandSemaWrite`, which reconciles state before replying.
Reconciliation reads `/proc` and checks worktree paths.

## Source behavior to remove

- Route `Observe` and `Query` through a true Sema-read path with no
  reconciliation, maintenance, timestamps, or writes.
- Remove startup and request-path `/proc` liveness and missing-worktree path
  reconciliation.
- Remove lock-file projection, legacy lock import, and role-retirement lock
  removal.
- Remove role/bootstrap filesystem reads, report-lane directory creation,
  and symlink/text-file projections.
- Remove claim-path canonicalization.
- Remove repository directory scans/projections and all `jj git remote list`
  identity probing, including migration-time probing.
- Remove checkout locking, `flock`, worktree scans, VCS operations,
  scaffolding, auto-land/push/rebase, salvage, and teardown.
- Remove `/proc`, pidfd, terminal-session, and harness-liveness discovery.
- Remove automatic worktree creation during claim contention.

Sema-only claim/worktree/repository records may remain. An absent path must
not cause a record to be forgotten.

Primary affected files include `src/execution.rs`, `src/service.rs`,
`src/worktree.rs`, `src/repository.rs`, `src/role.rs`, `src/claim.rs`,
`src/harness_liveness.rs`, `src/agent_reachability.rs`,
`src/table_reclamation.rs`, and `src/configuration.rs`.

## Deployment-coupled remainder

- Remove `workspace_root` and `git_index_root` from daemon configuration.
- Replace the configuration-writer/read-from-file startup mechanism with an
  explicit non-file configuration boundary.
- Remove workspace/git-root options and `jj`, `git`, and `gnupg` from the
  service declaration.
- Replace service checks that require those runtime tools.

Current declarations diverge: standalone CriomOS-home pins Orchestrate
`83e09a13`, while top-level CriomOS pins an older Orchestrate input
`be202b51`. This is static source evidence, not a live-runtime verdict.

## Retained infrastructure

- Sema/redb state, tables, state migrations, and state-only observations.
- Unix listener, client, upgrade, router, and Messenger socket transport,
  including verified socket lifecycle.
- Sema pre-migration preservation as database-state protection.
- `MirrorSnapshot` where it is an in-Sema handover payload rather than a
  filesystem mirror.

Client `NotaFile`/`SignalFile` request input is not resolved by this ruling
and is not part of the current removal slice.

## Strongest proof gate

Run the daemon in a namespace exposing only its Sema state and Unix-socket
paths. Do not provide `/proc`, workspace/repository/worktree roots, terminal
artifacts, or VCS executables. Deny `execve` and `flock` after startup.

Send every `Observe` variant and `Query` twice while tracing file, process,
and lock syscalls. Reject any child process, lock operation, prohibited path
access, or filesystem mutation outside the Sema/socket allowlist. Compare
logical table state before and after; do not rely only on database-file bytes,
which the storage engine may change internally.

Run a separate startup witness under the same restrictions. Startup must reach
readiness without workspace, repository, `/proc`, or child-process access.
