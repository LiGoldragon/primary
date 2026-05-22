# persona-orchestrate dynamic-role MVP

## Result

Implemented a raw but typed dynamic-role MVP across the Orchestrate
triad:

- `signal-persona-orchestrate`
  - Replaced fixed role enum semantics with dynamic
    `RoleIdentifier`.
  - Kept `RoleName` as a compatibility alias.
  - Added typed `HarnessKind` (`Codex`, `Claude`).
  - Added role harness metadata to `RoleStatus`.
  - Migrated the public request surface from `signal-core`
    `SignalVerb` wrappers to `signal-frame` contract-local operation
    roots: `Claim`, `Release`, `Handoff`, `Observe`, `Submit`,
    `Query`, `Watch`, and `Unwatch`.
  - Added observer stream wire types for inbound operation and
    outbound Sema-effect introspection.
- `owner-signal-persona-orchestrate`
  - Created the new owner contract repo.
  - Added `CreateRoleOrder`, `RetireRoleOrder`, and
    `RefreshRepositoryIndexOrder`.
  - Added owner replies for role creation, retirement, role-creation
    rejection, repository refresh, and unimplemented owner requests.
  - Migrated the owner request surface to `signal-frame`
    contract-local operation roots: `Create`, `Retire`, and
    `Refresh`.
- `persona-orchestrate`
  - Added sema-backed `roles` and `repositories` tables.
  - Added raw owner-request handling through `OrchestrateService`.
  - Added role creation that creates a local report-repository
    directory and a workspace report-lane symlink before inserting the
    role record.
  - Added local repository-index refresh from a configured Git index
    root into workspace `repos/` symlinks.
  - Added compatibility lock-file projection from daemon-owned typed
    claims into `orchestrate/<role>.lock`.
  - Implemented daemon ordinary/owner Unix socket listeners that own
    the `persona-orchestrate.redb` store and dispatch Signal frames.
  - Corrected the initial direct-store CLI mistake: the CLI binary
    only encodes NOTA requests as Signal frames to the daemon sockets.
  - Added runtime-owned `OperationLowering` from contract operations
    to `signal-sema::SemaOperation` effects.
  - Added ordinary observation subscription open/close handling with
    typed observation tokens.
  - Added named Nix checks for dynamic role creation, repository
    refresh, CLI boundary, and production daemon + CLI socket flow.

## Published State

- `signal-persona-orchestrate`
  - `main`: `c48116cc signal-persona-orchestrate: align observer docs with migrated stream`
  - bookmark: `persona-orchestrate-mvp`
- `owner-signal-persona-orchestrate`
  - `main`: `169dcbfb owner-signal-persona-orchestrate: refresh migrated lockfile`
  - bookmark: `persona-orchestrate-mvp`
- `persona-orchestrate`
  - `main`: `43fd89ad persona-orchestrate: track owner contract lockfile cleanup`
  - bookmark: `persona-orchestrate-mvp`

The `main` lines include later architecture-note commits. The
`persona-orchestrate-mvp` bookmarks remain the implementation snapshot.

## Architecture Redirection

The Signal architecture redirection has landed for the Orchestrate
triad. The ordinary and owner contracts now depend on `signal-frame`
instead of `signal-core`; public operation heads are contract-local
verbs instead of lower Sema verbs; and `persona-orchestrate` owns the
runtime lowering to `signal-sema::SemaOperation`.

The Orchestrate triad `ARCHITECTURE.md` files no longer carry
`MUST IMPLEMENT` migration notes. They now record the migration
history and the current constraints: thin CLI to daemon only, separate
ordinary/owner sockets, runtime-owned lowering, and typed observation
tokens on the public surface.

## Verification

- `signal-persona-orchestrate`: `cargo test`
- `signal-persona-orchestrate`: `nix --max-jobs 0 flake check`
- `owner-signal-persona-orchestrate`: `cargo test`
- `owner-signal-persona-orchestrate`: `nix --max-jobs 0 flake check`
- `persona-orchestrate`: `cargo test`
- `persona-orchestrate`: `nix --max-jobs 0 flake check`

The `persona-orchestrate` flake now exposes these MVP constraint
witnesses:

- `checks.<system>.test-dynamic-role-creation`
- `checks.<system>.test-repository-refresh`
- `checks.<system>.test-cli-boundary`
- `checks.<system>.test-daemon-cli`

## What Works

- Roles are no longer compile-time enum variants on the ordinary
  contract surface.
- Ordinary contract operations encode as contract-local roots, not
  public `Assert` / `Retract` / `Mutate` / `Match` wrappers.
- Owner contract operations encode as `Create`, `Retire`, and
  `Refresh`.
- The runtime has deterministic lowering witnesses for ordinary and
  owner operations to lower Sema effects.
- Role creation is owner-only vocabulary.
- Role records carry `HarnessKind` as data.
- The service stores role records in sema state.
- Role observation lists registered roles from sema state.
- Dynamic roles can acquire claims through the same lock-equivalent
  claim table as the current workspace roles.
- Role creation creates local report-lane filesystem shape in tests.
- Repository refresh scans local checkout directories and links them
  into a workspace `repos/` directory.
- The daemon binds separate ordinary and owner sockets and rejects the
  wrong contract vocabulary on each socket.
- The CLI can create a dynamic role through the daemon owner socket
  and then observe it through the daemon ordinary socket.
- The daemon rejects non-Signal traffic on the ordinary socket.
- Accepted role creation creates an empty lock file, and accepted
  claims project to the lock-file text shape the old helper used.
- The CLI boundary is now guarded by a source-scan witness: it must
  not import the service, tables, store location, sema-engine, or the
  redb path.
- Observation subscriptions allocate and close typed tokens on the
  ordinary surface.

## Gaps

- Report-repository creation is local-directory creation plus a
  report-lane symlink. It does not yet create a GitHub repository or
  clone through `ghq`.
- Repository "active" metadata is currently a boolean refreshed from
  local presence. It does not yet compute recency from last edit.
- Retiring a role removes the role record but does not delete report
  repositories, report lanes, claims, or repository links.
- Observation subscriptions have wire types and open/close handling,
  but the daemon does not yet keep subscriber sockets open and emit
  live operation/Sema-effect event frames.
- The owner contract is implemented, but filesystem permissions still
  do not enforce ordinary-vs-owner access.
- The daemon is a synchronous thread-per-connection MVP, not the final
  Kameo actor tree.

## Questions

1. Should report repositories be one repo per role named
   `persona-role-<role>-reports`, or should Orchestrate create a
   different repository naming shape?
2. Should `role create` create the GitHub repo immediately with `gh`
   and then `ghq get` it, or should local-only creation remain the
   default until lock projection and supervision are in place?
3. What should "active repository" mean for the first repository
   index: latest working-tree edit time, latest commit time, recent
   claim/activity touch, or explicit user pin?
4. When `RetireRoleOrder` lands for real, should it preserve report
   lanes by default and only mark the role inactive, or should it
   remove links and prevent future claims?
5. The next slice should wire a supervised workspace launch path and
   cutover procedure so this can replace `tools/orchestrate` in normal
   agent flow.
