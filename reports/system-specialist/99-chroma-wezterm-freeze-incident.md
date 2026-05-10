# Chroma WezTerm Freeze Incident

Date: 2026-05-10
Role: system-specialist

## Summary

Chroma theme switching froze unrelated WezTerm windows because live
terminal mutation leaked into global terminal paths. The bad shape was
not just "slow work"; it was work aimed at running terminals without an
explicit per-window protocol, bounded acknowledgement, or isolation from
other agent panes.

## Bad Pattern

Do not make a theme daemon mutate running terminals by:

- enumerating `/dev/pts`;
- writing OSC palette sequences to terminals from `SetTheme`;
- touching a reload file watched by every terminal window;
- using WezTerm `window:set_config_overrides` from a reload handler to
  apply a theme across windows.

Those paths turn one user's theme request into a global WezTerm event.
Even when the CLI returns immediately, the terminal server can continue
processing queued color/reload work and freeze unrelated panes.

## Correct Shape

`SetTheme` may persist terminal theme state for future shells. It must
not mutate running terminals automatically. A future live-terminal path
must be explicit, per-window, timeout-bounded, and acknowledgement-
bounded before the next window is touched.

## Fixes Applied

- `/git/github.com/LiGoldragon/chroma`
  - `501cb0bf` `system-specialist: stop live terminal OSC theme writes`
  - Removed CLI-side OSC palette writes.
  - Removed the unused terminal OSC palette helper.
  - Added hard-constraint coverage in
    `/git/github.com/LiGoldragon/chroma/tests/hard_constraints.rs`.
  - Documented the rule in
    `/git/github.com/LiGoldragon/chroma/HARD-CONSTRAINTS.md` and
    `/git/github.com/LiGoldragon/chroma/ARCHITECTURE.md`.

- `/git/github.com/LiGoldragon/CriomOS-home`
  - `daf25c0f` `system-specialist: remove wezterm reload override fanout`
  - Removed the WezTerm `window-config-reloaded` handler that called
    `window:set_config_overrides` across windows.
  - Home lock already consumes Chroma `501cb0bf`.

- `/git/github.com/LiGoldragon/CriomOS`
  - `681ae15b` `system-specialist: bump home without wezterm reload fanout`
  - Top-level lock consumes CriomOS-home `daf25c0f`.

## Verification

- `nix develop -c cargo test` passed in
  `/git/github.com/LiGoldragon/chroma`.
- `nix flake check` passed in `/git/github.com/LiGoldragon/chroma`.
- `nix flake check` passed in `/git/github.com/LiGoldragon/CriomOS-home`.
- Plain `nix flake check` in `/git/github.com/LiGoldragon/CriomOS`
  still requires the normal `system`/`horizon` override and fails before
  building without it.
- Deployed through `lojix`:
  `nix run /git/github.com/LiGoldragon/lojix-cli# -- '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "github:LiGoldragon/CriomOS-home/main" Activate None None)'`
- Live static checks found no `terminal_osc_sequence`,
  `chroma local terminal theme error`, `window-config-reloaded`,
  `set_config_overrides`, `wezterm-reload`,
  `add_to_config_reload_watch_list`, `/dev/pts`, or
  `broadcast_terminal_colors` in the installed Chroma/WezTerm profile.

