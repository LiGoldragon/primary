# Chroma Ghostty And Kameo State

Role: system-specialist  
Date: 2026-05-10

## Summary

Chroma is safer than it was during the WezTerm incidents, but it is not yet the
proper Ghostty-first visual daemon.

Current state:

- Ghostty is present as a Chroma theme concern and the running Chroma config
  includes `(Concerns Terminal Desktop Ghostty Emacs)`.
- Chroma writes `~/.config/ghostty/config` on `SetTheme`.
- The written Ghostty config currently sets font, window chrome, background,
  and foreground only. It does **not** write the full 16-colour palette,
  selection colours, or cursor colour.
- Chroma does not ask running Ghostty windows to reload. New Ghostty windows can
  read the new file; already-running Ghostty windows are not guaranteed to
  change.
- Chroma no longer has the direct WezTerm live-mutation paths that caused the
  earlier freezing pattern. It does not write OSC palette sequences to live
  panes, scan `/dev/pts`, or trigger the old WezTerm reload fanout.
- The current runtime is not Kameo. It is hand-rolled Tokio tasks, unbounded
  channels, `Arc<Mutex<_>>`, and detached `tokio::spawn` work.
- Chroma parses schedules but does not run a schedule engine. It also does not
  have the architecture's promised redb state store, config watcher, or Geoclue
  subscriber.

So the answer to "is Chroma implemented for Ghostty properly?" is **no**. It
has a first Ghostty file writer, not a complete Ghostty concern actor.

## Live Evidence

Installed / running state on ouranos:

- `chroma-daemon.service` is active.
- The service binary comes from Chroma commit
  `501cb0bfcbda94778c64decd88902e2dfc4948d1`
  (`system-specialist: stop live terminal OSC theme writes`).
- `CriomOS-home/flake.lock` pins Chroma to that same commit.
- `chroma '(GetTheme)'` returns `(Theme Light)`.
- `chroma '(GetState)'` returns `(State Light 6500 100)`.
- `~/.config/chroma/config.nota` includes
  `(Concerns Terminal Desktop Ghostty Emacs)`.
- `~/.config/ghostty/config` currently contains light-mode background and
  foreground values.

There is a live Home/Niri mismatch:

- `CriomOS-home/modules/home/profiles/min/niri.nix` now says the terminal is
  Ghostty.
- The active `~/.config/niri/config.kdl` still binds `Mod+Shift+Return` to
  WezTerm.

That means the source has moved to Ghostty, but the live Niri config has not
been activated/reloaded into the compositor session.

There is also stale Chroma state:

- `~/.local/state/chroma/wezterm-reload` still exists from an older generation.
- Current Chroma source does not write it, and current WezTerm config does not
  watch it. The stale file is residue, not an active path.

## Ghostty State

Chroma's current `GhosttyThemeConcern` is in
`/git/github.com/LiGoldragon/chroma/src/theme.rs`. It writes:

```text
font-family = IosevkaTerm Nerd Font
font-size = <font point size>
window-decoration = false
gtk-titlebar = false
window-theme = ghostty
background = <base00>
foreground = <base05>
```

That is incomplete for a terminal theme. Ghostty supports explicit `palette =`
entries, and `ghostty +show-config --default` shows palette slots `0` through
`15` as the normal ANSI colour surface. Chroma already has a Base16 palette, so
the proper Ghostty concern should write at least:

- `palette = 0=<base00>`
- `palette = 1=<base08>`
- `palette = 2=<base0B>`
- `palette = 3=<base0A>`
- `palette = 4=<base0D>`
- `palette = 5=<base0E>`
- `palette = 6=<base0C>`
- `palette = 7=<base05>`
- `palette = 8=<base03>`
- `palette = 9=<base08>`
- `palette = 10=<base0B>`
- `palette = 11=<base0A>`
- `palette = 12=<base0D>`
- `palette = 13=<base0E>`
- `palette = 14=<base0C>`
- `palette = 15=<base07>`

It should also set cursor and selection colours deliberately instead of
inheriting Ghostty defaults.

Ghostty can reload configuration at runtime, but Chroma does not currently use
that path. Official Ghostty documentation says the systemd integration supports:

```sh
systemctl reload --user app-com.mitchellh.ghostty.service
```

That sends `SIGUSR2` to the main Ghostty process through the user service. The
same docs recommend creating new windows through Ghostty's systemd / D-Bus
integration with:

```sh
ghostty +new-window
```

Current local problem: the live Ghostty process is not owned by the
`app-com.mitchellh.ghostty.service` unit. The unit exists, but
`systemctl --user show` reports it inactive with `MainPID=0`, while the running
Ghostty process owns the `com.mitchellh.ghostty` D-Bus name from a Niri scope.

So the correct Ghostty path has two parts:

1. The launcher path should use Ghostty's D-Bus/systemd window creation path
   rather than a plain long-lived Niri-spawned process.
2. Chroma's Ghostty concern should write the full config and then ask the
   systemd-owned Ghostty process to reload, timeout-bounded and isolated from
   every other concern.

Chroma should not scan `ps` for Ghostty and should not shell-script this. If a
reload actor is added, use a native concern boundary: systemd D-Bus via `zbus`,
or an explicit typed process-command actor if we decide `systemctl reload` is an
allowed adapter binary.

## WezTerm State

Chroma does not currently try to switch running WezTerm panes.

The relevant hard constraints are present in
`/git/github.com/LiGoldragon/chroma/HARD-CONSTRAINTS.md`, and
`/git/github.com/LiGoldragon/chroma/tests/hard_constraints.rs` checks:

- no `/dev/pts` inventory fanout;
- no `wezterm-reload` trigger from Chroma;
- no live terminal OSC palette sequences from the CLI or daemon.

The active Chroma source has no `wezterm` implementation path. WezTerm remains
enabled in CriomOS-home for parity and Persona-related adapter work, but its
config only reads Chroma's `current-mode` file at startup. It does not receive a
live theme mutation from Chroma.

That is the correct conservative safety posture after the incidents in:

- `reports/system-specialist/99-chroma-wezterm-freeze-incident.md`
- `reports/system-specialist/100-wezterm-live-palette-research.md`
- `reports/system-specialist/101-chroma-wezterm-crash-suspects.md`

## Runtime And Actor State

Chroma's repo docs are now stale relative to the workspace runtime decision:

- `AGENTS.md`, `ARCHITECTURE.md`, and `skills.md` still mention ractor.
- The workspace skills now say Kameo 0.20 is the actor runtime default.
- Chroma's `Cargo.toml` depends on neither `ractor` nor `kameo`.
- `Cargo.toml` still declares `rust-version = "1.85"`, but Kameo 0.20 requires
  Rust 1.88.

The implementation today is a hand-rolled actor-like runtime:

- `ThemeApplier` owns one `ThemeActor` per concern.
- `ThemeActor` is a Tokio unbounded channel plus a detached task.
- `ThemeConcernActor` drains to the latest requested mode and aborts the
  previous apply task.
- `DaemonState` is shared with `Arc` and guarded by `tokio::sync::Mutex`.
- The socket server spawns one detached Tokio task per connection.
- Warmth and brightness ramps are detached Tokio tasks tracked by
  `AbortHandle`.

This gives useful asynchronous behavior, but it violates the current actor
discipline:

- no Kameo actor root;
- no supervision tree;
- no actor topology witness;
- no typed per-kind Kameo `Message<T>` impls;
- unbounded mailboxes;
- shared `Arc<Mutex<_>>` state between concurrent planes;
- `tokio::spawn` work outside a supervised actor boundary.

That does not mean the current code is useless. It means the current code is a
working sketch that must be rewritten before Chroma becomes the durable daemon.

## Scheduler And State Store

Chroma's architecture says it owns schedules, persistence, config reload,
Geoclue, and redb state. The source does not implement those planes yet.

Implemented:

- typed request/reply over rkyv frames;
- NOTA CLI and config parsing;
- warmth and brightness immediate set / ramps;
- native theme concern parsing and first concern appliers;
- hard constraints against legacy apply-command schemas, YAML inputs, and
  global terminal fanout.

Missing:

- `StateStore` backed by redb;
- startup restore / re-apply from persisted state;
- `ScheduleEngine`;
- `ConfigWatcher`;
- Geoclue subscription;
- schedule application at daemon startup;
- future schedule deadlines;
- current-state derivation from persisted state rather than in-memory defaults.

This directly explains bead `primary-coz`: "Chroma scheduler applies current
scheduled visual state on daemon start and future waypoints."

## VSCodium And Chrome

Chroma does not directly switch VSCodium or Chrome today.

VSCodium is configured with:

- `window.autoDetectColorScheme = true`
- preferred dark and light themes

That means VSCodium follows the desktop/GTK appearance signal if the app
observes it correctly. Chroma's current desktop concern writes dconf and GTK
settings, but there is no VSCodium concern actor and no direct VSCodium reload
or settings update path.

Chrome is similar. There is no Chrome concern actor. It can only follow the
desktop/GTK/portal side if Chrome observes that state.

If direct VSCodium or Chrome behavior becomes required, each should be a
separate native concern actor with its own explicit API and tests. Do not hide
them behind a generic "apply scripts" path.

## Lojix / Logics Implication

If "logics" means `lojix-cli`, it is not blocking Chroma, but it is part of the
same runtime drift:

- `/git/github.com/LiGoldragon/lojix-cli` still depends on `ractor`.
- Its repo docs still refer to the older ractor pipeline.
- It is a transactional deploy CLI, not a long-lived desktop daemon, so the
urgency is lower than Chroma's daemon rewrite.

The current workspace rule is still clear: when we touch actor runtime code in
lojix, the new shape should be direct Kameo, data-bearing actors, no wrapper
runtime, and no ractor-era ZST/state split.

## Recommended Implementation Order

1. **Make Ghostty the actual live terminal path.**
   Activate the current CriomOS-home source so Niri stops spawning WezTerm.
   Prefer `ghostty +new-window` so Ghostty's systemd / D-Bus integration owns
   the process and Chroma can reload it through the documented path.

2. **Fix the Ghostty concern.**
   Write the full Ghostty palette, cursor, and selection settings. Add tests
   that fail if only background/foreground are written.

3. **Add a bounded Ghostty reload concern.**
   After writing the config, request a Ghostty reload through a native
   systemd/D-Bus actor, not through process scans and not through shell scripts.
   Treat failure as a concern-local error; it must not delay or block terminal,
   desktop, Emacs, warmth, or brightness concerns.

4. **Migrate Chroma to Kameo.**
   Bump Rust to 1.88, add `kameo = "0.20"`, remove ractor language from docs,
   and make `ChromaRoot` the actor root. The first actor set should be:
   `SocketServer`, `RequestDispatcher`, `ThemeApplier`, `TerminalThemeConcern`,
   `DesktopThemeConcern`, `GhosttyThemeConcern`, `EmacsThemeConcern`,
   `WarmthApplier`, `BrightnessApplier`, and `StateStore`.

5. **Land actor-truth tests.**
   Tests should assert that Chroma depends on Kameo, contains no ractor symbols,
   has no direct `tokio::spawn` in domain actors, has no `Arc<Mutex<_>>`
   shared daemon state, and routes theme changes through concern actors.

6. **Implement scheduler and persistence as actors.**
   Add `StateStore`, `ScheduleEngine`, `ConfigurationWatcher`, and
   `GeoclueSubscriber`. The scheduler should apply the current scheduled state
   on daemon start and future waypoints, satisfying `primary-coz`.

## Verification Run

- `nix flake check -L` in `/git/github.com/LiGoldragon/chroma` evaluated
  successfully.
- `nix build .#checks.x86_64-linux.default -L` in
  `/git/github.com/LiGoldragon/chroma` completed successfully.
- `chroma '(GetTheme)'` returned `(Theme Light)`.
- `chroma '(GetState)'` returned `(State Light 6500 100)`.

## Sources

- Chroma repo: `/git/github.com/LiGoldragon/chroma`
- CriomOS-home Chroma module:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`
- CriomOS-home Niri module:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix`
- Chroma incident reports:
  `reports/system-specialist/99-chroma-wezterm-freeze-incident.md`,
  `reports/system-specialist/100-wezterm-live-palette-research.md`,
  `reports/system-specialist/101-chroma-wezterm-crash-suspects.md`
- Ghostty systemd / D-Bus docs:
  <https://ghostty.org/docs/linux/systemd>
- Ghostty keybinding action reference:
  <https://ghostty.org/docs/config/keybind/reference>
- Ghostty GTK single-instance docs:
  <https://ghostty.org/docs/help/gtk-single-instance>
