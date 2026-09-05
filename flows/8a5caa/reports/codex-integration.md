# Codex command integration and user-environment deployment

## Method

The approved Home producer was first integrated and pushed to its `main`, then the current CriomOS consumer was pinned to that immutable Home revision and pushed to its `main`. The deployment used only the embedded target projection, `homeConfigurations.li.activationPackage`, with the materialized UserEnvironment inputs for `goldragon/ouranos/li`; it did not use a standalone Home configuration or a Host deployment.

Before live activation, the same immutable consumer source and materialized inputs were evaluated and built separately with `--no-write-lock-file`, `--option max-jobs 0`, and `--builders @/etc/nix/machines`. The resulting `codex-remote-control.service` was compared with the active user unit. The unit bytes matched and the extracted `ExecStart` SHA-256 was `4a224837368af4433ab2e72dc07862a316459a43e7d86013b7d2dbabdbe2dafb`. The active service was observed through the host user bus before and after activation.

## Landed revisions

- CriomOS-home `main`: `c40ff0cde736a4b092b7c713571afce40361a395` (`Fix Codex remote argv fixture`). This includes the approved upstream `codex` and thin `codex-remote` command change, without a new proxy executable.
- CriomOS `main`: `a66c93816c9a0bbd0660f979b26bb9c552b0e2b0` (`Pin Codex command Home release`). It pins the Home input and records the command contract in `ARCHITECTURE.md`.

The producer's final remote check covers caller-CWD preservation, no implicit `--cd`, and forwarding an explicit caller `--cd` unchanged. It was run with `--max-jobs 0`. The Pi harness failure was baseline-confirmed: the unchanged base and candidate both lacked the same Pi model matches.

## Lojix result and live observations

Lojix deployment 202 used `UserEnvironment.Realize`, source `github:LiGoldragon/CriomOS?rev=a66c93816c9a0bbd0660f979b26bb9c552b0e2b0`, and selector `homeConfigurations.li.activationPackage`. Its terminal state was `Completed / Succeeded`.

After the continuity comparison, deployment 204 used the same source and selector with `UserEnvironment.ActivateNow`. Its terminal state was `Completed / Succeeded`.

The live user environment then showed:

- `codex` and `codex-remote` are present in the user profile and both report `codex-cli 0.153.3`.
- `direct-codex` and user-profile `codex-raw` are absent.
- Native defaults are `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.
- `codex-remote-control.service` remained `active/running` on PID `4096266`, with the same `ExecStart` hash as the pre-activation unit.

No manual service restart, reboot, or emergency mutation was performed.

## Remote-only build evidence

The active `lojix-daemon.service` was traced through its service wrapper to the installed `lojix-0.20.3` derivation. That derivation references an installed source tree whose `NixCommand::build_closure_remote` constructs `nix build --no-link --print-out-paths --option max-jobs 0 --builders <builder-spec> <drv>^*`. This establishes the remote-only local-job prohibition in the daemon actually serving deployment 204.

The pinned CriomOS lock names Lojix revision `d3c0ac9032250e0b12ade7d8c71a8fc8311ab5bf`, whose source has the same implementation. The installed daemon's source store path did not equal a fresh fetch of that pinned revision, so the deployment evidence relies on the installed derivation and its inspected command construction; it does not claim installed source-revision identity with `d3c0ac…`.

## System alias limitation

The user profile no longer publishes `codex-raw`, but the current system profile still publishes `/run/current-system/sw/bin/codex-raw`; therefore normal PATH still resolves that system alias. A Host activation would also apply an unrelated 24-commit system delta, so it was deliberately not submitted. The active user service was preserved.

## Cleanup

Orchestrate locks 827, 832, and 833 were released. The producer feature worktree and both temporary integration worktrees were each verified clean, forgotten from Jujutsu, and removed. A final workspace-list check found none of those workspace names, and the released locks no longer appeared in the lock observation.

## Sources

- `CriomOS-home` commits `c40ff0cde736a4b092b7c713571afce40361a395` and associated remote-builder validation from the producer subflow.
- `CriomOS` commit `a66c93816c9a0bbd0660f979b26bb9c552b0e2b0`.
- Typed Lojix responses: `Query.ByDeployment.(202)` and `Query.ByDeployment.(204)`.
- Local candidate/unit comparison and host-user-bus observations performed during this flow.
- Installed Lojix source: `src/schema_runtime.rs`, `NixCommand::build_closure_remote`.
