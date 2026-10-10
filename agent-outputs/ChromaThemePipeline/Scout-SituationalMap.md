# Scout Situational Map — Chroma Theme Pipeline

Task: read-only map of Chroma theme switching and its prior Pi theme-switcher integration. Scope checked: `/git/github.com/LiGoldragon/chroma`, `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/CriomOS`, `/home/li/.pi/agent/packages`, live config/state/service paths. Commands included `rg`, `find`, `systemctl --user cat`, `spirit (PublicTextSearch [Chroma Pi theme])`.

## 1. Repo/path and relevant files

Chroma source is `/git/github.com/LiGoldragon/chroma` (also inventoried in `/home/li/primary/protocols/active-repositories.md`). Main files:

- `src/bin/chroma_daemon.rs`, `src/daemon.rs`: user daemon, UDS server, root actor, schedule/config/sleep watchers.
- `src/bin/chroma.rs`, `src/request.rs`, `src/response.rs`, `src/wire.rs`: CLI and rkyv-over-UDS request/reply (`$XDG_RUNTIME_DIR/chroma.sock`).
- `src/theme.rs`: `ThemeMode`, `ThemeConcern`, `ThemeApplier`, terminal/desktop/Ghostty/Emacs concerns.
- `src/state.rs`: redb/rkyv persistence at `$XDG_STATE_HOME/chroma/state.redb`.
- Tests: `tests/theme.rs`, `tests/config.rs`, `tests/hard_constraints.rs`.
- Deployment/config: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`, `checks/chroma-nota-config`, `checks/pi-harness-profile`, `checks/pi-criomos-extension-load`.

## 2. How Chroma decides/switches and pushes/applies

`src/daemon.rs` starts `ChromaRoot`, reads stored state with fallback from config defaults, then `ReapplyCurrentState` and `BeginSchedule`. Schedule decisions are in `src/schedule.rs`: theme schedule supports manual or waypoints (`Sunrise`, `Sunset`, civil triggers via geoclue location). CLI `Request::SetTheme { mode }` and scheduled reconciliation both call `ChromaRoot::set_theme`.

`set_theme` sets in-memory mode, persists via `RecordTheme`, then calls `enqueue_theme`. `ThemeApplier` fans `ApplyTheme` to configured native concern actors. Current concerns:

- Terminal: writes `$XDG_STATE_HOME/chroma/current-mode` and `fzf-theme.sh`.
- Desktop: uses configured `dconf` and writes GTK settings files.
- Ghostty: copies full dark/light template to `$XDG_CONFIG_HOME/ghostty/config.ghostty`, then sends Ghostty `org.gtk.Actions` `reload-config` over session DBus.
- Emacs: invokes configured `emacsclient --eval`.

Config reload is inotify (`notify::recommended_watcher`); sleep resume uses logind `PrepareForSleep`. No Chroma source-side Pi integration was found.

## 3. Old Pi extension dependency and current state file

Old/installed Pi extension is `/home/li/.pi/agent/packages/pi-criomos/src/extensions/theme-switcher.ts`; source copy exists at `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-criomos/src/extensions/theme-switcher.ts`. It reads `${XDG_STATE_HOME:-$HOME/.local/state}/chroma/current-mode`, maps `dark|light` to `criomos-dark|criomos-light`, calls `context.ui.setTheme(nextTheme)`, watches the chroma state directory, and also has a 30s polling interval plus provider/tool-call rechecks.

Chroma still writes that file in `TerminalThemeConcern::apply` (`src/theme.rs`). Live `/home/li/.local/state/chroma/current-mode` exists and currently contains `light`. Live state also contains stale-looking `wezterm-reload`; current source hard-constraint tests forbid writing WezTerm/global reload files.

## 4. Best insertion point for Pi push notifier

Best code insertion point: add a native Pi concern under `src/theme.rs` alongside terminal/desktop/Ghostty/Emacs, and include it in `ThemeApplier` fanout so every `set_theme` path (CLI, schedule, boot reapply, config reload) pushes Pi. Likely touched Chroma files: `src/theme.rs`, `src/config.rs` (`ThemeConcern::from_config_name` and any typed adapter/control config if needed), `src/lib.rs`, `tests/config.rs`, `tests/theme.rs`, `tests/hard_constraints.rs`, possibly `ARCHITECTURE.md`/`HARD-CONSTRAINTS.md`.

Likely deployment/test files: `CriomOS-home/modules/home/profiles/min/chroma.nix` (add `Pi` concern/control path if configurable), `packages/pi-criomos/default.nix` and package metadata (remove old extension when replacement is real), `checks/pi-harness-profile` and `checks/pi-criomos-extension-load` (currently assert the old extension/state-file contract), plus `checks/chroma-nota-config`.

## 5. Unknowns/risks

Unknown: Pi’s supported external control surface for changing UI theme without an in-process extension; local package grep only found `context.ui.setTheme` inside extensions, not a daemon/CLI/socket. Adding a generic configured shell apply command would conflict with Chroma guidance rejecting apply-command architecture. Need define/use a first-class Pi control path. Also beware startup ordering: Chroma can push before Pi UI exists, so the control path needs bounded failure/retry or later Pi registration without polling.
