# Pi Operator Safety Dirty Repository Fix Audit

*Kind: Audit · Topic: pi-operator-safety-dirty-repository-fix · 2026-05-23*

## Scope

I read `reports/system-designer/31-audit-of-cluster-operator-7-pi-harness-follow-up.md` after it was handed to the cluster-operator lane.

The system-designer audit is correct on its main implementation finding: the original Pi `operator-safety.ts` behavior in cluster-operator report 7 conflicted with Spirit workspace record 306, which says Pi operator-safety must not ask permission solely because a repository is dirty.

## Current State

`/git/github.com/LiGoldragon/CriomOS-home` is currently locked by `pi-operator`, not cluster-operator:

- lock purpose: create `persona-pi` and fix the Pi dirty-repository prompt
- overlapping repo: `/git/github.com/LiGoldragon/CriomOS-home`

I did not take the write lock or edit the repo.

The current `pi-operator` working copy already contains the intended fix:

- `operator-safety.ts` no longer imports `child_process` or `filesystem`
- the `findJujutsuRoot` helper is gone
- the `repositoryIsDirty` helper is gone
- the `confirmDirtyRepositoryMutation` helper is gone
- write/edit tool calls now only ask for confirmation when the path is protected
- the injected system-prompt guard explicitly says not to ask solely because a repository has existing working-copy changes
- `docs/pi-extensions.md` says the same thing

This matches the conservative reading of Spirit record 306: remove the dirty-repository confirmation entirely.

## Verification

I ran non-mutating checks against the dirty working copy, using `--no-link` so no result symlinks were written into the locked checkout.

Passed:

- `nix build --no-link .#checks.x86_64-linux.pi-harness-profile .#checks.x86_64-linux.pi-criomos-extension-load --option warn-dirty false -L`
- negative source check: no `repositoryIsDirty`, `findJujutsuRoot`, `confirmDirtyRepositoryMutation`, `dirty jj repository`, or `dirty repository` remains in the Pi operator-safety source/docs/check files
- positive source check: destructive command confirmation, protected path confirmation, and the "do not ask solely because dirty" instruction are present

I did not run a full `nix flake check` or live activation because the implementation is owned by `pi-operator` and still uncommitted.

## Remaining Gap

The implementation fix is present, but the check suite does not yet directly guard against the bug returning.

`checks/pi-harness-profile/default.nix` verifies that force-push detection and subagent discipline are present, but it does not explicitly fail if dirty-repository helper names or `jj root` probing come back.

The pi-operator should add a small negative source-shape assertion before committing:

```sh
! grep -R 'repositoryIsDirty\|findJujutsuRoot\|confirmDirtyRepositoryMutation' \
  "${pi-criomos}/share/pi-packages/pi-criomos/src/extensions/operator-safety.ts"
```

The exact shell can be adapted for Nix, but the invariant should be in the exported check: Pi operator-safety must not inspect repository dirtiness as a permission trigger.

## Recommendation

Let `pi-operator` finish the locked implementation. The expected completion bar is:

- add the negative regression assertion to `pi-harness-profile`
- run focused Pi checks
- run full `nix flake check`
- commit and push `CriomOS-home`
- activate locally through Lojix if this is intended to change the live Pi operator immediately

No cluster-operator code action is needed unless the `pi-operator` lane stalls or releases the lock with the fix incomplete.
