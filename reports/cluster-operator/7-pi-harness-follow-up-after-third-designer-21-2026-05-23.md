# Pi Harness Follow-Up After Third-Designer 21

## Result

I acted on `reports/third-designer/21-audit-cluster-operator-6-pi-harness-2026-05-22.md`.

`CriomOS-home` commit `f2e9c929` now extends the Pi harness package slice:

- `packages/pi-criomos/src/extensions/theme-switcher.ts`
  - reads Chroma's mode file at `$XDG_STATE_HOME/chroma/current-mode`,
    defaulting through `~/.local/state/chroma/current-mode`;
  - applies `criomos-dark` or `criomos-light` with Pi's
    `context.ui.setTheme(...)`;
  - applies at session start, before provider calls, before tool calls,
    and when Chroma's state directory reports `current-mode` changes;
  - keeps an interval fallback so a missed file-watch event is repaired.
- `packages/pi-criomos/src/extensions/operator-safety.ts`
  - appends a short system-prompt guard: Pi subagents require explicit
    psyche request;
  - asks confirmation for destructive shell commands;
  - asks confirmation before writes under protected paths;
  - asks confirmation before file mutation in a dirty jj repository;
  - blocks safety-sensitive tool calls when no interactive UI is
    available to confirm.
- `packages/pi-criomos/default.nix`
  - packages both extensions alongside the existing themes.
- `docs/pi-extensions.md`
  - documents `pi-criomos`, `theme-switcher.ts`,
    `operator-safety.ts`, and the Chroma state source.
- `checks/pi-harness-profile/default.nix`
  - asserts both extensions exist and are listed in package metadata.

`pi-linkup` is now documented as the external web search, web answer,
web fetch, and balance-command package. It remains packaged unchanged.

## Verification

Passed:

```sh
nix fmt -- packages/pi-criomos/default.nix checks/pi-harness-profile/default.nix modules/home/profiles/min/pi-models.nix docs/pi-extensions.md
nix build .#pi-criomos .#checks.x86_64-linux.pi-harness-profile --option warn-dirty false -L
nix flake check --option warn-dirty false -L
git diff --check
pi -e packages/pi-criomos/src/extensions/theme-switcher.ts --list-models gpt
pi -e packages/pi-criomos/src/extensions/operator-safety.ts --list-models gpt
```

The Pi extension-load probes use `--list-models`, so they verify
extension import without making an inference request.

I pushed `CriomOS-home` `main` to `f2e9c929`.

## Activation

I first tried to activate from `github:LiGoldragon/CriomOS-home/main`.
GitHub returned an unauthenticated API rate-limit response, and Nix used
its cached copy of that flake. That stale activation temporarily showed
only `packages/pi-linkup` in Pi settings and the unversioned
`persona-spirit-daemon.service`.

I corrected the live profile immediately by rebuilding and activating
from `path:/git/github.com/LiGoldragon/CriomOS-home`.

Current live checks:

- `~/.pi/agent/settings.json` packages:
  `packages/pi-criomos`, `packages/pi-linkup`, `packages/pi-subagents`;
- Pi default model: `gpt-5.5`;
- Pi default thinking: `xhigh`;
- `~/.pi/agent/packages/pi-criomos/package.json` lists both new
  extensions;
- `~/.local/state/chroma/current-mode` exists and currently says
  `light`;
- versioned Spirit services are restored:
  `persona-spirit-daemon-v0.1.0.service` and
  `persona-spirit-daemon-v0.1.1.service` are active.

## Beads

- Added a note to bead `primary-u7gc` (persona-pi architecture): the
  v2 persona-pi path should incorporate Pi headless RPC mode as the
  daemon-facing integration surface, not drive the interactive TUI when
  a typed RPC surface exists.
- Created bead `primary-m1tk` (terminal-cell smoke script): update the
  stale `terminal-cell-wait --socket` invocation in
  `persona/scripts/persona-engine-sandbox-terminal-cell-smoke`.

## Remaining Gaps

The Chroma-backed theme switcher is implemented and packaged, but I did
not prove a live mid-stream palette flip during an inference task. A
proper witness would need either a Pi UI harness that can observe active
theme changes without paid inference, or explicit permission to run a
short live Pi task while toggling Chroma.

The operator-safety extension is intentionally first-pass. It confirms
high-risk actions, protected writes, and dirty-repo writes, but it is
not a complete sandbox or policy engine. It should eventually move
toward typed owner-signal policy once Pi becomes a real persona-pi
triad component.

The GitHub-rate-limit stale activation is a deployment-path problem,
not a Pi package problem. Lojix should probably authenticate GitHub
flake resolution or prefer local path activation for the author's
workstation when testing unmerged home-profile work.
