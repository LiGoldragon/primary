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
- `owner-signal-persona-orchestrate`
  - Created the new owner contract repo.
  - Added `CreateRoleOrder`, `RetireRoleOrder`, and
    `RefreshRepositoryIndexOrder`.
  - Added owner replies for role creation, retirement, role-creation
    rejection, repository refresh, and unimplemented owner requests.
- `persona-orchestrate`
  - Added sema-backed `roles` and `repositories` tables.
  - Added raw owner-request handling through `OrchestrateService`.
  - Added role creation that creates a local report-repository
    directory and a workspace report-lane symlink before inserting the
    role record.
  - Added local repository-index refresh from a configured Git index
    root into workspace `repos/` symlinks.
  - Added a direct-store raw CLI in the existing
    `persona-orchestrate-daemon` target for `role create`, `role list`,
    `repository refresh`, `repository list`, `claim`, and `release`.
  - Added named Nix checks for dynamic role creation and repository
    refresh.

## Published State

- `signal-persona-orchestrate`
  - `main`: `46cb6f56 contract: make orchestrate roles dynamic`
  - bookmark: `persona-orchestrate-mvp`
- `owner-signal-persona-orchestrate`
  - `main`: `d9210f9a contract: fix owner orchestrate formatting gate`
  - bookmark: `persona-orchestrate-mvp`
- `persona-orchestrate`
  - `main`: `39f0fd05 orchestrate: repin owner signal contract`
  - bookmark: `persona-orchestrate-mvp`

## Verification

- `signal-persona-orchestrate`: `cargo test`
- `signal-persona-orchestrate`: `nix flake check`
- `owner-signal-persona-orchestrate`: `cargo test`
- `owner-signal-persona-orchestrate`: `nix flake check`
- `persona-orchestrate`: `cargo test`
- `persona-orchestrate`: `nix flake check`

The `persona-orchestrate` flake now exposes these MVP constraint
witnesses:

- `checks.<system>.test-dynamic-role-creation`
- `checks.<system>.test-repository-refresh`

## What Works

- Roles are no longer compile-time enum variants on the ordinary
  contract surface.
- Role creation is owner-only vocabulary.
- Role records carry `HarnessKind` as data.
- The service stores role records in sema state.
- Role observation lists registered roles from sema state.
- Dynamic roles can acquire claims through the same lock-equivalent
  claim table as the current workspace roles.
- Role creation creates local report-lane filesystem shape in tests.
- Repository refresh scans local checkout directories and links them
  into a workspace `repos/` directory.
- The raw CLI can exercise the MVP without the old shell topology.

## Gaps

- There is still no long-lived daemon socket. The CLI opens the store
  directly for now.
- There is no lock-file projection back to `orchestrate/*.lock`.
- Report-repository creation is local-directory creation plus a
  report-lane symlink. It does not yet create a GitHub repository or
  clone through `ghq`.
- Repository "active" metadata is currently a boolean refreshed from
  local presence. It does not yet compute recency from last edit.
- Retiring a role removes the role record but does not delete report
  repositories, report lanes, claims, or repository links.
- There are no subscriptions yet.
- The owner contract is implemented, but filesystem permissions still
  do not enforce ordinary-vs-owner access.

## Questions

1. Should report repositories be one repo per role named
   `persona-role-<role>-reports`, or should Orchestrate create a
   different repository naming shape?
2. Should `role create` create the GitHub repo immediately with `gh`
   and then `ghq get` it, or should local-only creation remain the
   default until the daemon exists?
3. What should "active repository" mean for the first repository
   index: latest working-tree edit time, latest commit time, recent
   claim/activity touch, or explicit user pin?
4. When `RetireRoleOrder` lands for real, should it preserve report
   lanes by default and only mark the role inactive, or should it
   remove links and prevent future claims?
5. Should the next slice build the daemon/socket boundary first, or
   wire compatibility lock-file projection first so the raw CLI can
   start replacing `tools/orchestrate` sooner?
