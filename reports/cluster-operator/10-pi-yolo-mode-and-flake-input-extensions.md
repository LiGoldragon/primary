# Pi YOLO Mode And Flake Input Extensions

*Kind: Handover · Topic: persona-pi-yolo-mode · 2026-05-23*

## Scope

The psyche reported that the running CriomOS-home Pi still prompted:

```text
CriomOS dirty repository
Repository already has working-copy changes. Allow mutation?
```

Then the psyche clarified: "I want yolo mode."

I logged the durable intent in Spirit:

- record 333: live Pi must stop the stale dirty-repository prompt
- record 334: Pi extension sources belong in flake inputs, with hashes in `flake.lock`
- record 335: default Pi is the fully featured basic experience: `openai-codex`, highest model, highest thinking, subagents
- record 336: operator-safety must not create repeated confirmation burden during normal work
- record 337: Pi operator workflow should support YOLO mode

I also read `reports/pi-operator/1-pi-operator-safety-dirty-prompt-handoff.md`.

## Implementation

Repo: `/git/github.com/LiGoldragon/CriomOS-home`

Worktree used because the main checkout was still locked by `pi-operator`:

```text
/home/li/wt/github.com/LiGoldragon/CriomOS-home/pi-yolo-mode
```

Commit pushed to `main`:

```text
e7e33210 home: Pi yolo mode and flake-input extensions
```

What changed:

- `pi-criomos` is now theme-only:
  - keeps `theme-switcher.ts`
  - stops registering `operator-safety.ts`
  - deletes `operator-safety.ts` from the package source
- Pi default profile still enables:
  - `packages/pi-criomos`
  - `packages/pi-linkup`
  - `packages/pi-subagents`
- Pi default profile still sets:
  - provider: `openai-codex`
  - model: `gpt-5.5`
  - thinking: `xhigh`
  - double escape action: `tree`
- external Pi extension tarballs moved from `pkgs.fetchurl` hashes in package files to non-flake flake inputs:
  - `pi-linkup-src`
  - `pi-utils-ui-src`
  - `pi-subagents-src`
- `packages/pi-linkup/default.nix` and `packages/pi-subagents/default.nix` now unpack `inputs.*-src`
- `docs/pi-extensions.md` now says extension source hashes live in `flake.lock`
- `checks/pi-harness-profile/default.nix` asserts:
  - `pi-criomos` has exactly one extension, `theme-switcher.ts`
  - `operator-safety.ts` is not present in the package
  - `pi-linkup` and `pi-subagents` package files use flake inputs and do not use `fetchurl` or inline `hash = ...`

## Verification

Passed:

```sh
nix build --no-link .#packages.x86_64-linux.pi-linkup .#packages.x86_64-linux.pi-subagents .#packages.x86_64-linux.pi-criomos .#checks.x86_64-linux.pi-harness-profile .#checks.x86_64-linux.pi-criomos-extension-load --option warn-dirty false -L
nix flake check --option warn-dirty false -L
jj diff --git --color=never | rg '^\+.*[ \t]$' || true
```

The worktree is a Jujutsu workspace without a Git checkout, so `git diff --check` is not available there. The trailing-whitespace check above found no added trailing whitespace.

## Live Activation

Activated locally from the worktree path:

```sh
lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/home/li/wt/github.com/LiGoldragon/CriomOS-home/pi-yolo-mode" Build None None)'
lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/home/li/wt/github.com/LiGoldragon/CriomOS-home/pi-yolo-mode" Activate None None)'
```

Live profile verified:

- `~/.pi/agent/settings.json` packages:
  - `packages/pi-criomos`
  - `packages/pi-linkup`
  - `packages/pi-subagents`
- provider: `openai-codex`
- model: `gpt-5.5`
- thinking: `xhigh`
- double escape action: `tree`
- theme: `criomos-dark`
- `~/.pi/agent/packages/pi-criomos/package.json` extensions:
  - `./src/extensions/theme-switcher.ts`
- `~/.pi/agent/packages/pi-criomos/src/extensions/operator-safety.ts` is absent
- `pi -e ~/.pi/agent/packages/pi-criomos/src/extensions/theme-switcher.ts --list-models gpt` exits successfully and lists `gpt-5.5`

## Operational Note

An already-running Pi session that loaded the old `operator-safety.ts` extension will keep that code in memory. That session must be restarted. New Pi sessions use the activated YOLO profile and will not load the dirty-repository confirmation extension.

The main `/git/github.com/LiGoldragon/CriomOS-home` checkout still has the pi-operator's uncommitted old work and `result` symlinks. Since `main` is now at `e7e33210`, pi-operator should rebase or drop that stale working copy before continuing.

## Bead

Closed bead `primary-gtao` (pi-operator runtime dirty-repository prompt) because the default live Pi profile no longer loads the prompting extension and the durable `main` state enforces the absence of `operator-safety.ts` from `pi-criomos`.
