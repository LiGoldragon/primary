# Lojix command boundary implementation checkpoint

## Source

- Isolated worktree: `/git/worktrees/criomos-f16b0a-lojix-command-boundary`
- Branch: `flow-f16b0a-lojix-command-boundary`
- Base and current HEAD: `583e727fb24701295d6a603ea34f9f1b43c504d4`
- Review diff: `/home/li/primary/flows/f16b0a/lojix-command-boundary-implementation.diff`
- No commit, push, build, publication, evaluation, deployment or runtime action has occurred.

## Implemented declaration

`services.lojix` now names five package roles: daemon, ordinary client, meta client, offline tools and bootstrap. The PersonaDevelopment consumer selects the five existing locked producer outputs. Daemon and reset unit commands use their exact role package paths. Harness update takes only the two clients it invokes.

The system aggregate contains one invariant launcher package with eight maintained entrypoints. Every launcher executes its fixed name beneath the configurable `/etc/lojix/commands` default and contains no selected package reference. One `environment.etc` directory source selects all eight exact package executables together as part of the system generation.

## Focused test

`checks/lojix-command-boundary` constructs synthetic A and B package-role sets and asserts:

- the system package list and launcher derivation remain identical;
- the generation-owned command-directory source changes;
- daemon/reset commands use exact selected role paths;
- all eight launchers contain only stable command-directory paths;
- no launcher contains either selected directory or any selected package path;
- every selected A/B executable runs and reports its expected generation and command name;
- ordinary/meta targets move together;
- a nondefault canonical command directory is honored;
- traversal, empty-component and dot-component paths are rejected; and
- selecting A again reproduces A's command-directory source (declarative rollback simulation).

Existing service/start/ownership checks now consume and assert the separate roles.

## Static validation completed

- `nix-instantiate --parse` passed for all eight changed/new Nix files.
- `nixfmt --check` passed for all eight changed/new Nix files.
- `git diff --check` passed.
- Lojix aggregate-package consumer references were removed from modules/checks.
- `flake.lock` is unchanged; Home remains `0b430341a594f1b1ee31e986c4dbd0d537e6ffe7`.

## Gates and next ordering

1. Main performs final source review of the refreshed diff.
2. Field supplies the exact accepted source-check entrypoint, builder destination and existing immutable materialized input URLs.
3. The worktree is copied once with rsync to the builder as an uncommitted WIP source tree. Field runs all four focused checks there through ordinary configured Prometheus offload: `lojix-command-boundary`, `lojix-nexus-service`, `lojix-ownership`, and the `lojix-nexus-start` VM when supported.
4. Only after those remote source checks pass does main release immutable candidate creation and push:

```sh
cd /git/worktrees/criomos-f16b0a-lojix-command-boundary
git add checks/lojix-command-boundary/default.nix checks/lojix-nexus-service/default.nix checks/lojix-nexus-start/default.nix checks/lojix-ownership/default.nix flake.nix modules/nixos/harness-update.nix modules/nixos/lojix-persona-development.nix modules/nixos/lojix.nix
git commit -m 'Separate Lojix command package ownership'
git push origin HEAD:refs/heads/flow-f16b0a-lojix-command-boundary
CANDIDATE=$(git rev-parse HEAD)
```

The exact rsync destination and remote check commands remain pending Field's ftv2 answer; none are inferred from a node name or reconstructed input path.

Field alone materializes whole-host A/B through Lojix and proves system-path/unit/restart-trigger invariance, selected executable identities, coherent command-directory switching and rollback. Those proofs, candidate publication, boot staging and runtime acceptance remain gates.
