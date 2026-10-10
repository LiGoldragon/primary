# Pi Subagent Profile Split Evidence

## Task And Scope

Task: update `CriomOS-home` so the normal Home Manager Pi profile uses the tintinweb subagent package, isolated `pi-testing` uses `pi-ultra-subagents`, normal/test Pi state stays separated, and the updated current user profile is deployed on this machine.

Target repository:

- `/git/github.com/LiGoldragon/CriomOS-home`

Target deployment:

- cluster: `goldragon`
- node: `ouranos`
- user: `li`
- deployment shape: `Home`
- action: `Activate`
- source revision: `a8b98fb09722e8529a7e04178805638384939abb`
- builder: `None`
- rollback expectation: prior Home generation remains in the Lojix live-set and can be reactivated by deploying the prior `CriomOS-home` revision.

## Context Consulted

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/README.md`
- `/git/github.com/LiGoldragon/CriomOS-home/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/CriomOS-home/docs/pi-extensions.md`
- `/git/github.com/LiGoldragon/CriomOS-home/skills.md`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/lore/AGENTS.md`
- `/home/li/primary/agent-outputs/PiTestingProfile/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PiProfileIsolationFeasibility/Scout-SituationalMap.md`

Coordination:

- `orchestrate "(Observe Roles)"` showed no claim on `CriomOS-home`.
- Claimed `/git/github.com/LiGoldragon/CriomOS-home` as `operating-system-implementer`.
- `bd list --status open` still fails because `.beads` exists without a beads database.
- Spirit `PublicTextSearch [CriomOS-home Pi subagents home profile]` returned only general intent records, not a Pi-specific directive.

## Changed Files

In `/git/github.com/LiGoldragon/CriomOS-home`:

- `flake.nix`
- `flake.lock`
- `packages/pi-ultra-subagents/default.nix`
- `modules/home/profiles/min/pi-models.nix`
- `checks/pi-harness-profile/default.nix`

## Implemented State

Added pinned flake inputs for:

- `pi-ultra-subagents` `0.1.0`
- `typebox` `1.1.38`

Added `packages/pi-ultra-subagents/default.nix`, installing the package below:

```text
share/pi-packages/pi-ultra-subagents
```

The derivation also installs `typebox` into package-local `.pi-deps` and symlinks it under package-local `node_modules/typebox`, so Pi does not need to install it into runtime state.

Normal Pi settings now use:

```json
[
  "packages/pi-criomos",
  "packages/pi-linkup",
  "packages/pi-subagents-tintinweb",
  "packages/pi-continue"
]
```

Isolated `pi-testing` settings now use:

```json
[
  "packages/pi-criomos",
  "packages/pi-linkup",
  "packages/pi-ultra-subagents",
  "packages/pi-continue"
]
```

Home Manager now exposes:

- `$HOME/.pi/agent/packages/pi-subagents-tintinweb`
- `$HOME/.pi-testing/agent/packages/pi-ultra-subagents`

Home Manager no longer exposes:

- `$HOME/.pi/agent/packages/pi-subagents`
- `$HOME/.pi-testing/agent/packages/pi-subagents-tintinweb`

The `pi-testing` wrapper stayed isolated with:

- `PI_CODING_AGENT_DIR="${PI_TESTING_AGENT_DIR:-$HOME/.pi-testing/agent}"`
- `PI_CODING_AGENT_SESSION_DIR="${PI_TESTING_SESSION_DIR:-$PI_CODING_AGENT_DIR/sessions}"`
- `PI_PACKAGE_DIR="${PI_PACKAGE_DIR:-$HOME/.local/share/criomos/pi/package}"`

## Verification

Commands run in `/git/github.com/LiGoldragon/CriomOS-home` before commit:

```sh
npm view pi-ultra-subagents name version dist.tarball dependencies peerDependencies pi --json
npm view typebox@1.1.38 name version dist.tarball --json
curl -fsSL https://registry.npmjs.org/pi-ultra-subagents/-/pi-ultra-subagents-0.1.0.tgz | tar -xOzf - package/package.json | jq .
nix flake update pi-ultra-subagents-src pi-ultra-subagents-typebox-src
nix fmt -- flake.nix packages/pi-ultra-subagents/default.nix modules/home/profiles/min/pi-models.nix checks/pi-harness-profile/default.nix
nix eval --json .#packages.x86_64-linux --apply 'packages: builtins.filter (name: builtins.match ".*pi.*subagents.*" name != null) (builtins.attrNames packages)'
nix eval --raw .#packages.x86_64-linux.pi-ultra-subagents.drvPath >/dev/null
nix build .#pi-ultra-subagents --no-link --print-build-logs
nix build .#checks.x86_64-linux.pi-harness-profile --no-link --print-build-logs
nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link --print-build-logs
nix flake check --print-build-logs
```

Results:

- `pi-ultra-subagents` resolved to npm version `0.1.0`.
- `typebox` resolved to npm version `1.1.38`.
- Package attr evaluation listed `pi-subagents`, `pi-subagents-tintinweb`, and `pi-ultra-subagents`.
- `nix build .#pi-ultra-subagents --no-link --print-build-logs` succeeded.
- `nix build .#checks.x86_64-linux.pi-harness-profile --no-link --print-build-logs` succeeded.
- `nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link --print-build-logs` succeeded.
- `nix flake check --print-build-logs` passed for `x86_64-linux`.

Post-push reproducibility checks:

```sh
nix build github:LiGoldragon/CriomOS-home/a8b98fb09722#checks.x86_64-linux.pi-harness-profile --refresh --no-link --print-build-logs
nix build github:LiGoldragon/CriomOS-home/a8b98fb09722#pi-ultra-subagents --refresh --no-link --print-build-logs
```

Both pushed-revision builds succeeded from `github:LiGoldragon/CriomOS-home/a8b98fb09722e8529a7e04178805638384939abb`.

## Commit And Push

Committed and pushed:

```text
a8b98fb09722e8529a7e04178805638384939abb CriomOS-home: split Pi subagent profiles
```

Post-push status:

- `jj git push --bookmark main` reported `main@origin` already matches `main`.
- `jj status --no-pager` reported no working-copy changes.

## Deployment

Deployment command:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/a8b98fb09722e8529a7e04178805638384939abb Activate None [])))"
```

Admission result:

```text
(Deployed (34 (552 552)))
```

Terminal evidence:

```sh
lojix "(Query (ByGeneration 34))"
```

Result: generation `34` is `goldragon ouranos HomeOnly Switch Current`.

Live profile checks after activation:

```sh
jq -r '.packages[]' "$HOME/.pi/agent/settings.json"
jq -r '.packages[]' "$HOME/.pi-testing/agent/settings.json"
ls -l "$HOME/.pi/agent/packages/pi-subagents-tintinweb" \
  "$HOME/.pi/agent/packages/pi-subagents" \
  "$HOME/.pi-testing/agent/packages/pi-ultra-subagents" \
  "$HOME/.pi-testing/agent/packages/pi-subagents-tintinweb"
```

Results:

- Normal Pi packages are `pi-criomos`, `pi-linkup`, `pi-subagents-tintinweb`, and `pi-continue`.
- `pi-testing` packages are `pi-criomos`, `pi-linkup`, `pi-ultra-subagents`, and `pi-continue`.
- Normal `$HOME/.pi/agent/packages/pi-subagents-tintinweb` is present.
- Normal `$HOME/.pi/agent/packages/pi-subagents` is absent.
- Testing `$HOME/.pi-testing/agent/packages/pi-ultra-subagents` is present.
- Testing `$HOME/.pi-testing/agent/packages/pi-subagents-tintinweb` is absent.
- `pi-testing` remains installed at `$HOME/.nix-profile/bin/pi-testing` and its wrapper still sets the isolated Pi environment variables listed above.

## Caveats

- No interactive `pi` or `pi-testing` session was started, avoiding session creation and paid model/API calls.
- The deployed Lojix observation surface still reports the artifact/action with legacy labels `HomeOnly Switch`, even though the submission path was the current `Deploy (Home ...)` request.
- The first broad `ByNode` poll did not show generation `34` immediately; a direct `ByGeneration 34` query then confirmed it as current, and the live settings files confirmed activation.
- No Niri reload was needed because this change only touches Home-managed Pi package/config files and the `pi-testing` wrapper.
