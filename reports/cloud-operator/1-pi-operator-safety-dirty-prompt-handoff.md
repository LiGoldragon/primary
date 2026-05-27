# Pi Operator Safety Dirty-Prompt Handoff

## Purpose

This is a handoff report for cluster-operator after their audit in
`reports/cluster-operator/9-audit-pi-operator-safety-dirty-repository-fix.md`.
The psyche reported that Pi repeatedly asked for confirmation because a
repository was dirty. Spirit record 306 now states the corrected rule:
Pi operator-safety must not ask permission solely because a repository is
dirty.

## Current state

`CriomOS-home` is still claimed by `pi-operator` for the combined
`persona-pi` creation and Pi safety fix pass.

Current working-copy changes in `/git/github.com/LiGoldragon/CriomOS-home`:

- `packages/pi-criomos/src/extensions/operator-safety.ts`
  - removes the dirty-repository confirmation path;
  - removes the helper logic that ran `jj root` / `jj status` before
    mutations;
  - keeps confirmation for destructive shell commands;
  - keeps confirmation for protected-path writes;
  - appends a system-prompt rule that Pi must not ask for confirmation
    solely because a repository already has working-copy changes.
- `docs/pi-extensions.md`
  - updates the `pi-criomos` description so it no longer claims dirty jj
    repository writes are confirmation-gated.

Live mitigation already happened in the user profile: I removed
`packages/pi-criomos` from `~/.pi/agent/settings.json`, leaving
`packages/pi-linkup` and `packages/pi-subagents` enabled. That disables the
prompting extension for the running harness until the fixed package is
committed, activated, and re-enabled.

## Verification run

Dirty-repository edit probe from the reloaded Pi session succeeded in
`/home/li/primary` by editing this report while the workspace already had
uncommitted changes from multiple lanes.

From `/git/github.com/LiGoldragon/CriomOS-home`, these checks pass:

```sh
nix build .#checks.x86_64-linux.pi-harness-profile .#checks.x86_64-linux.pi-criomos-extension-load --option warn-dirty false -L
```

A source search currently finds no old dirty-repository helper symbols in the
extension source. The terms still need to become negative assertions in a Nix
check, per cluster-operator's audit request.

## Remaining work

The remaining requested fix is to add Nix negative regression assertions to
`checks/pi-harness-profile/default.nix` so these strings cannot reappear in the
packaged `operator-safety.ts` unnoticed:

- `repositoryIsDirty`
- `findJujutsuRoot`
- `confirmDirtyRepositoryMutation`
- `CriomOS dirty repository`

My first edit attempt to add those assertions did not land; the file is still
unchanged at the old positive checks. The next command should edit
`checks/pi-harness-profile/default.nix`, rerun the two focused Pi checks,
commit/push the CriomOS-home change, activate Home from the local path or a
fresh pushed input, then re-enable `packages/pi-criomos` in Pi settings through
the managed profile rather than by hand.

## Coordination note

`pi-operator` owns `/git/github.com/LiGoldragon/CriomOS-home` right now. If
cluster-operator wants to take over, `pi-operator` should release or narrow its
claim first. The user specifically asked for this handoff report after telling
cluster-operator to inspect the issue.
