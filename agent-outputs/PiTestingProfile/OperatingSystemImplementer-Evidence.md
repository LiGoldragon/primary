# Pi Testing Profile Evidence

## Task And Scope

Implemented a safe `pi-testing` executable/profile in `CriomOS-home` for testing an alternate Pi subagent extension without changing the normal Pi profile under `$HOME/.pi/agent`.

Target repository:

- `/git/github.com/LiGoldragon/CriomOS-home`

Scout reports read first:

- `/home/li/primary/agent-outputs/PiProfileIsolationFeasibility/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/PiIntercomSupervisorCoordination/Scout-SituationalMap.md`

Repo/context files consulted:

- `AGENTS.md`
- `ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/pi-extensions.md`
- `skills.md`
- `modules/home/profiles/min/default.nix`
- `modules/home/profiles/min/pi-models.nix`
- `packages/pi-subagents/default.nix`
- `packages/pi-linkup/default.nix`
- `checks/pi-harness-profile/default.nix`
- `checks/ai-agent-launch-orchestration/default.nix`

Coordination:

- Observed Orchestrate roles.
- Claimed `/git/github.com/LiGoldragon/CriomOS-home` as `operating-system-implementer`.
- `bd list --status open` in `CriomOS-home` failed because `.beads` exists but has no beads database.

## Changed Files

In `/git/github.com/LiGoldragon/CriomOS-home`:

- `flake.nix`
- `flake.lock`
- `packages/pi-subagents-tintinweb/default.nix`
- `modules/home/profiles/min/default.nix`
- `modules/home/profiles/min/pi-models.nix`
- `checks/pi-harness-profile/default.nix`
- `checks/ai-agent-launch-orchestration/default.nix`

## Implemented State

Added pinned flake inputs for:

- `@tintinweb/pi-subagents` `0.13.0`
- `@sinclair/typebox` `0.34.49`
- `croner` `10.0.1`
- `nanoid` `5.1.16`

Added `packages/pi-subagents-tintinweb/default.nix`, installing the tintinweb package under:

```text
share/pi-packages/pi-subagents-tintinweb
```

The derivation also installs the three npm dependencies into package-local `.pi-deps` and symlinks them under package-local `node_modules`, so Pi does not need to install them into runtime state.

Normal Pi remains configured with:

```json
[
  "packages/pi-criomos",
  "packages/pi-linkup",
  "packages/pi-subagents",
  "packages/pi-continue"
]
```

The isolated testing Pi settings use:

```json
[
  "packages/pi-criomos",
  "packages/pi-linkup",
  "packages/pi-subagents-tintinweb",
  "packages/pi-continue"
]
```

The testing Home Manager tree declares:

- `$HOME/.pi-testing/agent/settings.json`
- `$HOME/.pi-testing/agent/models.json`
- `$HOME/.pi-testing/agent/auth.json`
- `$HOME/.pi-testing/agent/packages/pi-criomos`
- `$HOME/.pi-testing/agent/packages/pi-linkup`
- `$HOME/.pi-testing/agent/packages/pi-subagents-tintinweb`
- `$HOME/.pi-testing/agent/packages/pi-continue`

Added `pi-testing` to the min profile. It runs direct Pi without the default CriomOS orchestration prompt injection and sets:

```sh
PI_CODING_AGENT_DIR="${PI_TESTING_AGENT_DIR:-$HOME/.pi-testing/agent}"
PI_CODING_AGENT_SESSION_DIR="${PI_TESTING_SESSION_DIR:-$PI_CODING_AGENT_DIR/sessions}"
PI_PACKAGE_DIR="${PI_PACKAGE_DIR:-$HOME/.local/share/criomos/pi/package}"
```

It creates only the isolated agent and session directories before launching Pi.

## Verification

Commands run in `/git/github.com/LiGoldragon/CriomOS-home`:

```sh
npm view @tintinweb/pi-subagents name version dist.tarball dependencies peerDependencies pi --json
npm view @sinclair/typebox version dist.tarball --json
npm view croner version dist.tarball --json
npm view nanoid version dist.tarball --json
curl -fsSL https://registry.npmjs.org/@tintinweb/pi-subagents/-/pi-subagents-0.13.0.tgz | tar -xOzf - package/package.json | jq '{name, version, dependencies, peerDependencies, pi}'
nix flake update pi-subagents-tintinweb-src pi-subagents-tintinweb-typebox-src pi-subagents-tintinweb-croner-src pi-subagents-tintinweb-nanoid-src
nix fmt -- flake.nix packages/pi-subagents-tintinweb/default.nix modules/home/profiles/min/default.nix modules/home/profiles/min/pi-models.nix checks/pi-harness-profile/default.nix
nix fmt -- checks/ai-agent-launch-orchestration/default.nix
nix build .#pi-subagents-tintinweb --no-link
nix build .#checks.x86_64-linux.pi-harness-profile --no-link
nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link
nix eval --raw .#packages.x86_64-linux.pi-subagents-tintinweb.drvPath >/dev/null
nix eval --json .#packages.x86_64-linux --apply 'builtins.attrNames'
nix eval --json .#homeConfigurations --apply 'builtins.attrNames'
nix flake check
```

Results:

- `@tintinweb/pi-subagents` resolved to npm version `0.13.0`.
- Dependency tarballs resolved to the versions listed above.
- `nix build .#pi-subagents-tintinweb --no-link` succeeded.
- `nix build .#checks.x86_64-linux.pi-harness-profile --no-link` succeeded.
- `nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link` succeeded.
- `nix eval --raw .#packages.x86_64-linux.pi-subagents-tintinweb.drvPath >/dev/null` succeeded.
- `nix eval --json .#packages.x86_64-linux --apply 'builtins.attrNames'` listed `pi-subagents-tintinweb`.
- `nix eval --json .#homeConfigurations --apply 'builtins.attrNames'` returned `[]` for the standalone stubbed flake.
- `nix flake check` completed successfully for `x86_64-linux`.

Repository closeout:

- Committed in `CriomOS-home` as `fa903217` with message `CriomOS-home: add isolated pi-testing profile`.
- Moved `main` to the commit.
- Pushed `main`; follow-up push check reported `main@origin` already matches `main`.
- Post-push `jj status --no-pager` in `CriomOS-home` reported no working-copy changes.

## Caveats

- No live Home Manager activation was run, so `$HOME/.pi-testing/agent` was not materialized by activation during this task.
- No interactive `pi-testing` session was started, avoiding session creation and paid model/API calls.
- `pi-testing` uses a separate Pi auth/model config path, but the managed contents intentionally mirror the normal declarative provider/auth command shape. Secret bytes remain runtime-resolved through `gopass`, not stored in Nix.
- Project-local `.pi` resources from the current working directory can still be discovered by Pi when the project is trusted; the wrapper isolates the global Pi agent root, not the process working directory.
- The `pi-testing` wrapper is direct by design so extension behavior is not mixed with the normal CriomOS orchestration prompt wrapper.
