# Pi Harness Extension Testing

## Scope

This report records the follow-up implementation after `reports/third-designer/21-audit-cluster-operator-6-pi-harness-2026-05-22.md`.

Intent was refreshed through Spirit first. No new durable psyche intent record was logged from the prompt itself; the prompt was an execution request to continue implementation and testing from the already-recorded Pi harness intent.

## CriomOS-home Changes

Repo: `/git/github.com/LiGoldragon/CriomOS-home`

Commit: `2701516d` — `home: harden Pi extension tests and safety guard`

Changed files:

- `flake.nix`
- `checks/pi-criomos-extension-load/default.nix`
- `checks/pi-harness-profile/default.nix`
- `packages/pi-criomos/src/extensions/operator-safety.ts`

The new `pi-criomos-extension-load` check runs Pi in an isolated temporary home with a minimal local model definition and explicitly loads:

- `theme-switcher.ts`
- `operator-safety.ts`

It verifies that Pi starts and lists the test model with both extensions loaded, without touching the user's live Pi state and without making an inference request.

The existing `pi-harness-profile` check now also asserts the theme-switcher and operator-safety extension source shape:

- the theme switcher reads the Chroma mode indicator from `XDG_STATE_HOME/chroma/current-mode`
- the theme switcher calls `context.ui.setTheme(...)`
- the operator-safety extension injects the workspace subagent discipline into Pi's system prompt
- force-push detection uses a normal whitespace-delimited `--force` matcher

## Bug Fixed

The operator-safety extension had a weak force-push matcher:

- it used `\B--force\b`
- that misses the ordinary command shape `git push --force` because a word boundary exists before `--force`

The matcher now uses whitespace or start/end anchoring around `--force` for both `git push` and `jj git push`.

The recursive `rm` matcher was also simplified to catch recursive forms by the presence of `r` or `R`, plus `--recursive` and `--force`.

## Verification

Passed:

- `nix build .#checks.x86_64-linux.pi-harness-profile .#checks.x86_64-linux.pi-criomos-extension-load --option warn-dirty false -L`
- `nix flake check --option warn-dirty false -L`
- `git diff --check`

`nix fmt` did not work as the repository-level formatter command in this checkout: it invoked `nixfmt` as if it were formatting empty standard input. I formatted the touched Nix files directly with `nixfmt`.

## Live Activation

Activated locally on `ouranos` through Lojix using the local checkout:

- build: `lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/git/github.com/LiGoldragon/CriomOS-home" Build None None)'`
- activate: `lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/git/github.com/LiGoldragon/CriomOS-home" Activate None None)'`

Live profile verified:

- packages: `packages/pi-criomos`, `packages/pi-linkup`, `packages/pi-subagents`
- theme: `criomos-dark`
- provider: `openai-codex`
- model: `gpt-5.5`
- thinking: `xhigh`
- double escape action: `tree`
- `pi-criomos` exports both extensions in `package.json`
- Chroma current mode file exists and currently reads `light`
- `pi -e theme-switcher.ts -e operator-safety.ts --list-models gpt` exits successfully and shows the expected GPT models

## Remaining Gap

The hard remaining gap is a true mid-task theme-switch witness. The theme-switcher extension is packaged, loaded, and source-shape checked, but I have not proven that an already-running interactive Pi session flips palette while a long task is in progress.

That needs either:

- a Pi UI harness that can keep a session open, mutate the Chroma mode file, and assert the visible palette changes; or
- a smaller extension-level test hook that exposes theme-change events without starting a paid model request.

The current state is strong enough for continued Pi operator testing, but not yet a complete proof of the original "switch while running" usability requirement.
