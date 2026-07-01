# Pi Profile Isolation Feasibility Scout Map

## Task And Scope

Task: map whether the current local Pi setup can later support a separate `pi-testing` executable that runs Pi with isolated state, config, extension, package, session, and cache paths, and uses `@tintinweb/pi-subagents` instead of the current sub-agent extension without disturbing the current Pi setup.

Scope was read-only local inspection plus one web search for the requested package identity. I did not install, remove, update, or edit Pi extensions. The only writes were this report directory/file under `agent-outputs/PiProfileIsolationFeasibility/`.

## Feasibility

Yes, with one important implementation constraint: isolate by environment variables and by a separate settings/config tree, not by mutating the existing `~/.pi/agent`.

Pi itself exposes the needed knobs:

- `PI_CODING_AGENT_DIR` changes the global Pi config/state root from the default `~/.pi/agent`.
- `PI_CODING_AGENT_SESSION_DIR` or `--session-dir` changes session storage.
- `PI_PACKAGE_DIR` changes the Pi executable package asset root, already used by the local Nix wrapper.
- package and extension discovery comes from settings under the selected config root, project `.pi/`, and explicit CLI paths.

The current setup is already Nix/home-manager-managed enough that a `pi-testing` wrapper/derivation is feasible as a declarative sibling of the existing `pi` and `direct-pi` wrappers. The cleanest approach is to create a new wrapper that sets `PI_CODING_AGENT_DIR` to an isolated path such as `$XDG_STATE_HOME/pi-testing/agent` or `$HOME/.pi-testing/agent`, sets `PI_CODING_AGENT_SESSION_DIR` inside that tree, sets `PI_PACKAGE_DIR` to the same Pi package asset path used by `direct-pi`, and points settings at a package set containing `@tintinweb/pi-subagents` rather than `packages/pi-subagents`.

## Current Pi Invocation And Install Facts

Observed executable resolution:

- `command -v pi` returned `/home/li/.nix-profile/bin/pi`.
- `type -a pi` returned `pi is /home/li/.nix-profile/bin/pi`.
- `/home/li/.nix-profile/bin/pi` is a symlink into `/nix/store/...-home-manager-path/bin/pi`.
- `readlink -f /home/li/.nix-profile/bin/pi` resolved to the active home-manager-provided outer wrapper at `/nix/store/...-pi/bin/pi`.
- `pi --version` returned `0.80.2`.
- `nix profile list` showed `home-manager-path` in the user profile and no separate `pi` profile item.

The outer `pi` wrapper source is in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`. Lines around the `piWithDefaultOrchestration` wrapper show it:

- calls `piPackage = pkgs.callPackage ../../../../packages/pi { inherit inputs; };`
- installs `piWithDefaultOrchestration` as package name `pi`;
- injects default orchestration instructions via `--append-system-prompt` unless `CRIOMOS_AGENT_MODE` is `direct`, `worker`, or `non-orchestrator`, unless `PI_SUBAGENT_CHILD` is set, or unless explicit system prompt arguments are present;
- also defines `direct-pi`, which executes the package Pi binary without this orchestration-instruction injection.

The package-level Pi derivation is `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix`. It builds Pi `0.80.2` from `inputs.pi-src` and wraps the binary so that, when `PI_PACKAGE_DIR` is unset, it sets:

```sh
PI_PACKAGE_DIR="$HOME/.local/share/criomos/pi/package"
```

The live package asset symlink `/home/li/.local/share/criomos/pi/package` resolves to a Pi `0.80.2` package root. The older `/home/li/.pi/pi-source` symlink is stale: `readlink -e /home/li/.pi/pi-source` returned no path even though `ls -la` shows it points at an old store path.

## State, Config, Session, Package, And Extension Paths

Pi help output for `pi --help` lists:

- `PI_CODING_AGENT_DIR` as the config directory override, default `~/.pi/agent`;
- `PI_CODING_AGENT_SESSION_DIR` as session storage override, overridden by `--session-dir`;
- `PI_PACKAGE_DIR` as package directory override for Nix/Guix store paths;
- `--extension` / `-e`, repeatable, for explicit extension/package loading;
- `--no-extensions`, where explicit `-e` paths still work;
- `--no-skills`, `--no-prompt-templates`, `--no-themes`, and related discovery-disable flags.

Installed source evidence from `/home/li/.local/share/criomos/pi/package/src/config.ts`:

- `APP_NAME` is `pi`; `CONFIG_DIR_NAME` is `.pi` from package `piConfig`.
- `ENV_AGENT_DIR` becomes `PI_CODING_AGENT_DIR`.
- `ENV_SESSION_DIR` becomes `PI_CODING_AGENT_SESSION_DIR`.
- `getAgentDir()` returns `$PI_CODING_AGENT_DIR` if set, otherwise `join(homedir(), ".pi", "agent")`.
- `getModelsPath()`, `getAuthPath()`, `getSettingsPath()`, `getToolsDir()`, `getPromptsDir()`, and `getSessionsDir()` all derive from `getAgentDir()`.
- `getPackageDir()` returns `$PI_PACKAGE_DIR` if set, otherwise infers the package root.

Session evidence from `/home/li/.local/share/criomos/pi/package/src/core/session-manager.ts`:

- default sessions are encoded under `$agentDir/sessions/<encoded-cwd>`.
- creating/listing sessions uses that default unless an explicit session directory is supplied.

Settings evidence from `/home/li/.local/share/criomos/pi/package/src/core/settings-manager.ts`:

- global settings path is `$agentDir/settings.json`.
- project settings path is `$cwd/.pi/settings.json`.
- global and project settings are deep-merged, with project settings loaded only when trusted.

Package/extension evidence from `/home/li/.local/share/criomos/pi/package/src/core/package-manager.ts` and `src/core/resource-loader.ts`:

- package settings can be strings or objects with per-resource filters for `extensions`, `skills`, `prompts`, and `themes`.
- project package settings are considered before global package settings, and duplicate package identities prefer project scope.
- user npm installs go under `$agentDir/npm`; user git installs go under `$agentDir/git`; temporary package/extension installs go under `$agentDir/tmp/extensions`.
- auto-discovered user extensions are under `$agentDir/extensions`; user skills/prompts/themes are under `$agentDir/skills`, `$agentDir/prompts`, and `$agentDir/themes`.
- project resources are under `$cwd/.pi/extensions`, `$cwd/.pi/skills`, `$cwd/.pi/prompts`, and `$cwd/.pi/themes` when the project is trusted.
- `--no-extensions` disables discovered/settings extensions but still allows explicit CLI `-e` extension sources.

Docs evidence from `/home/li/.local/share/criomos/pi/package/docs/packages.md` and `docs/extensions.md`:

- Pi packages are installed into user settings by default at `~/.pi/agent/settings.json`; `-l` writes project `.pi/settings.json`.
- local package paths in settings are loaded without copying.
- package manifests declare resources under the `pi` key in `package.json`.
- extension auto-discovery locations are `~/.pi/agent/extensions/*.ts`, `~/.pi/agent/extensions/*/index.ts`, `.pi/extensions/*.ts`, and `.pi/extensions/*/index.ts`.

## Current Extensions And Packages Found

Global Pi settings are `/home/li/.pi/agent/settings.json`. The relevant keys are:

```json
{
  "packages": [
    "packages/pi-criomos",
    "packages/pi-linkup",
    "packages/pi-subagents",
    "packages/pi-continue"
  ],
  "extensions": null,
  "skills": null,
  "prompts": null,
  "themes": null,
  "sessionDir": null
}
```

Those package paths are Nix/home-manager symlinks under `/home/li/.pi/agent/packages/`:

- `pi-criomos`
- `pi-linkup`
- `pi-subagents`
- `pi-continue`

Package manifests show the currently configured extension set is plural:

- `/home/li/.pi/agent/packages/pi-criomos/package.json`: package `pi-criomos` `0.1.0`; Pi extension `./src/extensions/theme-switcher.ts`; skills `./skills`; themes `./themes`.
- `/home/li/.pi/agent/packages/pi-linkup/package.json`: package `@aliou/pi-linkup` `0.11.0`; Pi extensions `./src/extensions/web-search/index.ts`, `./src/extensions/web-answer/index.ts`, `./src/extensions/web-fetch/index.ts`, and `./src/extensions/command-balance/index.ts`; skills `./skills`.
- `/home/li/.pi/agent/packages/pi-subagents/package.json`: package `pi-subagents` `0.31.0`; Pi extension `./src/extension/index.ts`; skills `./skills`; prompts `./prompts`.
- `/home/li/.pi/agent/packages/pi-continue/package.json`: package `pi-continue` `0.8.2`; Pi extension `./extensions/continue/index.ts`.

Current subagent package:

- It is `pi-subagents` version `0.31.0`, packaged by `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents/default.nix`.
- That derivation extracts `inputs.pi-subagents-src` and applies `agent-chain-clarify-opt-in.patch` and `slim-parent-skill.patch`.
- Its homepage in the derivation is `https://github.com/nicobailon/pi-subagents`.
- Bundled agents under `/home/li/.pi/agent/packages/pi-subagents/agents/` are `context-builder.md`, `delegate.md`, `oracle.md`, `planner.md`, `researcher.md`, `reviewer.md`, `scout.md`, and `worker.md`.

Other user/project surfaces:

- `/home/li/.pi/agent/extensions/pi-linkup.json` exists and contains `{ "systemPromptGuidance": true }`, but Pi extension auto-discovery only loads `.ts`, `.js`, extension directories, or package manifests. A narrow search in the linkup package found no reference to `pi-linkup.json`, so I did not prove it is active.
- `/home/li/.pi/agent/extensions-disabled/` contains disabled `pi-superpowers-plus` material, including a package manifest with extensions `extensions/plan-tracker.ts`, `extensions/workflow-monitor.ts`, and `extensions/subagent/index.ts`. This is disabled by path placement, not active settings.
- `/home/li/primary/.pi/agents/` contains project role files: `general-code-implementer.md`, `intent-curator.md`, `intent-translator.md`, `nix-auditor.md`, `operating-system-implementer.md`, `repo-scaffolder.md`, `repository-closeout.md`, `rust-auditor.md`, `scout.md`, `skill-editor.md`, and `tracker-weaver.md`.
- `/home/li/primary/.pi/settings.json` does not exist, so `/home/li/primary` has project role files but no project package override.

The Home Manager source of the current settings/package symlinks is `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix`. It declares:

- `pi-criomos`, `pi-linkup`, `pi-subagents`, and `pi-continue` package derivations;
- `piSettingsConfig.packages = [ "packages/pi-criomos" "packages/pi-linkup" "packages/pi-subagents" "packages/pi-continue" ];`
- `home.file.".pi/agent/packages/<name>".source = ...`;
- managed config merges for `$HOME/.pi/agent/models.json`, `$HOME/.pi/agent/auth.json`, and `$HOME/.pi/agent/settings.json`.

## Recommended Implementation Shape For `pi-testing`

Implement this declaratively in `CriomOS-home`, likely near the existing Pi packaging:

1. Add a package derivation for `@tintinweb/pi-subagents`.

Likely file:

- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents-tintinweb/default.nix`

Shape should match the existing npm-tarball package wrappers for `pi-linkup`, `pi-subagents`, and `pi-continue`: unpack the pinned npm tarball input into `$out/share/pi-packages/pi-subagents-tintinweb`, preserving its `package.json` and `pi` manifest. The package source should be a pinned flake input, not fetched imperatively at runtime. The Pi package catalog currently advertises install command `pi install npm:@tintinweb/pi-subagents`; GitHub search result for `https://github.com/tintinweb/pi-subagents` describes the same package and its FleetView/conversation viewer.

2. Add an isolated Pi settings/config tree for the wrapper.

Likely file:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix`

Recommended test root options:

- `$HOME/.pi-testing/agent`
- or `$XDG_STATE_HOME/pi-testing/agent` if the module has a clean way to expand it at runtime.

The settings file inside that root should be managed separately from `$HOME/.pi/agent/settings.json`, with a package set that keeps desired non-subagent extensions but replaces only the subagent package:

```json
{
  "packages": [
    "packages/pi-criomos",
    "packages/pi-linkup",
    "packages/pi-subagents-tintinweb",
    "packages/pi-continue"
  ]
}
```

If the test should be a narrower A/B test of only subagent behavior, use just the minimum package set required to avoid unrelated extension effects. The user corrected that extensions are plural and settings may hold them; therefore avoid copying current settings blindly unless the package list is intentionally filtered.

3. Add symlinks for the isolated package directory.

Likely declarations in `pi-models.nix` or a sibling module:

- `home.file.".pi-testing/agent/packages/pi-criomos".source = ...`
- `home.file.".pi-testing/agent/packages/pi-linkup".source = ...`
- `home.file.".pi-testing/agent/packages/pi-subagents-tintinweb".source = ...`
- `home.file.".pi-testing/agent/packages/pi-continue".source = ...`

This keeps package paths relative in settings and avoids touching `/home/li/.pi/agent/packages/pi-subagents`.

4. Add a `pi-testing` wrapper next to `pi`, `direct-pi`, and the existing agent wrappers.

Likely file:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`

Recommended wrapper behavior:

```sh
export PI_CODING_AGENT_DIR="${PI_TESTING_AGENT_DIR:-$HOME/.pi-testing/agent}"
export PI_CODING_AGENT_SESSION_DIR="${PI_TESTING_SESSION_DIR:-$PI_CODING_AGENT_DIR/sessions}"
export PI_PACKAGE_DIR="${PI_PACKAGE_DIR:-$HOME/.local/share/criomos/pi/package}"
export PI_OFFLINE="${PI_OFFLINE:-1}"
exec ${piPackage}/bin/pi "$@"
```

Decide intentionally whether `pi-testing` should include the default orchestration instruction injection. For an extension-isolation test, I recommend making `pi-testing` direct by default, like `direct-pi`, so the only behavioral variable is the isolated package/settings tree. If the test must match normal `pi`, create two wrappers: `pi-testing` with the normal orchestration injection and `direct-pi-testing` without it.

5. Add a check analogous to existing Pi checks.

Likely files:

- `/git/github.com/LiGoldragon/CriomOS-home/checks/pi-harness-profile/default.nix`
- or a new `/git/github.com/LiGoldragon/CriomOS-home/checks/pi-testing-profile/default.nix`

Check that:

- the tintinweb package derivation contains `package.json`;
- its `package.json` declares expected `pi.extensions`;
- the isolated settings file contains `packages/pi-subagents-tintinweb`;
- the isolated settings file does not contain `packages/pi-subagents`;
- the existing normal settings still contain `packages/pi-subagents`.

## Verification Commands For Later Implementation

These commands should be safe after the wrapper exists; they are read-only or no-session checks unless noted.

```sh
command -v pi-testing
pi-testing --version
PI_OFFLINE=1 pi-testing --help
jq '.packages' "$HOME/.pi-testing/agent/settings.json"
find -L "$HOME/.pi-testing/agent/packages" -maxdepth 2 -name package.json -print
PI_OFFLINE=1 pi-testing --no-session --no-extensions --no-skills --no-prompt-templates --no-themes --version
```

Be careful with `pi list`: I ran `PI_OFFLINE=1 pi list` expecting the package-list command, but in this environment it started an interactive agent prompt and asked "What would you like me to list?". I terminated it with Ctrl-C and did not use it as evidence. Prefer direct `jq`/`find` config inspection or a non-interactive code-level check until the command behavior is understood.

For live extension verification, use a deliberately isolated command with local-only/no-session settings first. Starting a real Pi session can create session files under the selected session directory by design, which is acceptable only after confirming the selected directory is the isolated test root.

## Risks And Open Questions

- `@tintinweb/pi-subagents` was verified only from public web search/catalog/GitHub snippets in this scout, not locally installed source. Before packaging, inspect its `package.json`, peer dependencies, and README/source at the pinned revision.
- Pi package-manager commands can install missing npm/git packages on startup when settings reference npm/git sources and project trust allows it. The recommended Nix shape avoids that by using local symlinked package paths under the isolated agent root.
- If `pi-testing` reuses `/home/li/primary` as cwd, project `.pi/agents` will still be discovered when the project is trusted. That is probably desired for role testing, but it means project role files are not isolated unless the wrapper runs from a separate cwd or uses `--no-context-files`/other flags as appropriate. Project `.pi/settings.json` is absent today.
- User-wide `~/.agents/skills` can still be discovered as user agent skills in Pi source. `PI_CODING_AGENT_DIR` isolates Pi's own user skills under `$agentDir/skills`, but does not change `$HOME`. If strict total isolation is required, run with a controlled `HOME` or audit whether `~/.agents/skills` affects the target test.
- Auth/model config isolation needs an explicit decision. A separate `PI_CODING_AGENT_DIR` means `auth.json` and `models.json` are also separate unless copied or separately managed. That is good for non-disturbance, but the test wrapper may need managed local-provider model/auth config analogous to the existing `$HOME/.pi/agent/models.json` and `$HOME/.pi/agent/auth.json`.
- The existing outer `pi` wrapper injects default orchestration instructions. `direct-pi` bypasses that. `pi-testing` should choose one behavior explicitly to avoid confusing extension behavior with prompt-wrapper behavior.
- `bd list --status open` in `/git/github.com/LiGoldragon/CriomOS-home` failed with "no beads database found"; I did not initialize or repair it.
- `/home/li/.local/share` traversal hit a permission denied under `waydroid/data`; this was not relevant to Pi surfaces checked.
- I did not inspect private repositories, run Nix builds, run Pi live sessions, or inspect the full `@tintinweb/pi-subagents` source locally.

## Commands And Sources Consulted

Local commands included:

- `command -v pi`
- `type -a pi`
- `readlink -f /home/li/.nix-profile/bin/pi`
- `ls -l /home/li/.nix-profile/bin/pi`
- `pi --version`
- `pi --help`
- `find /home/li/.pi -maxdepth 3 ...`
- `jq` over `/home/li/.pi/agent/settings.json`
- `jq` over package manifests under `/home/li/.pi/agent/packages/`
- `rg` for Pi package/settings references under `/home/li/primary`, `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/CriomOS`, and `/home/li/Criopolis`
- `sed` on the narrow Pi source/docs/Nix files named above
- `nix profile list`
- `bd list --status open` in `CriomOS-home`, which failed as noted above
- Spirit public query: `spirit "(PublicTextSearch [Pi profile isolation extension subagent])"` returned general agent-system records including `n9fl` and no Pi-specific durable intent record.

Local files consulted included:

- `/home/li/primary/AGENTS.md` from the prompt
- `/home/li/primary/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`
- `/git/github.com/LiGoldragon/lore/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS-home/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/pi-harness-profile/default.nix`
- `/home/li/.local/share/criomos/pi/package/src/config.ts`
- `/home/li/.local/share/criomos/pi/package/src/core/settings-manager.ts`
- `/home/li/.local/share/criomos/pi/package/src/core/session-manager.ts`
- `/home/li/.local/share/criomos/pi/package/src/core/package-manager.ts`
- `/home/li/.local/share/criomos/pi/package/src/core/resource-loader.ts`
- `/home/li/.local/share/criomos/pi/package/docs/packages.md`
- `/home/li/.local/share/criomos/pi/package/docs/extensions.md`
- prior reports `/home/li/primary/agent-outputs/PiSubagentChatSwitching/Scout-SituationalMap.md`, `/home/li/primary/agent-outputs/RoleSkillReview/Scout-PiSubagentMining.md`, and `/home/li/primary/agent-outputs/SkillDoctrineV2/Scout-PiRoleMaterialReview.md`

Web sources consulted:

- Pi package catalog search result for `@tintinweb/pi-subagents`, `https://pi.dev/packages`, which lists install command `pi install npm:@tintinweb/pi-subagents`.
- GitHub search result for `https://github.com/tintinweb/pi-subagents`, which describes FleetView, live conversation viewer, mid-run steering, and custom agent types.

