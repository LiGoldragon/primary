# 01 — whisrs status-bar widget stuck grey: stale quickshell, not a code bug

## Symptom

The Noctalia bar widget `whisrs-level` (color-coded mic state: grey
idle / red recording / yellow transcribing, defined at
`CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/BarWidget.qml`)
stayed permanently grey on ouranos, even while the daemon was
actively recording and transcribing.

## Root cause

The running quickshell process predated the home-manager
generation that first deployed the plugin. Quickshell scans
`Settings.configDir + "plugins"` at startup
(`PluginRegistry.qml:255`) and does not auto-reload when home-
manager updates the plugin tree underneath it. The previous
quickshell instance logged
`PluginRegistry: All plugin manifests loaded. Total plugins: 0`
in `/tmp/noctalia2.log` — it had no whisrs-level widget loaded
at all; what the bar rendered was unrelated.

`kill <quickshell-pid>; setsid noctalia-shell </dev/null
>/dev/null 2>&1 & disown` (niri only spawns it at session start,
so manual relaunch is required) brought up a fresh instance that
scanned the plugin tree, registered `whisrs-level`, opened the
level.sock connection, and rendered the live state.

## What was eliminated en route

The plumbing was verified end-to-end before the restart:

- `whisrsd` is active and toggles state on every IPC command
  (`whisrs/src/daemon/main.rs:733` broadcasts `state_tx`).
- The `State` enum carries `#[serde(rename_all = "lowercase")]`
  (`whisrs/src/lib.rs:115-117`), matching the widget's
  `"recording"` / `"transcribing"` comparisons exactly. No
  Capitalized-vs-lowercase mismatch.
- The level-stream socket binds when `config.general.status_bar
  = true`; CriomOS-home's `dictation.nix` sets that.
- Quickshell did open an ESTAB connection to
  `/run/user/1001/whisrs/level.sock` on its old fd 41; the
  socket plumbing was correct.
- Reading the socket directly with `socat - UNIX-CONNECT:...`
  showed real `{"state":"recording","level":0.07…}` events with
  level values varying with mic input — i.e. the daemon-side
  emission was perfect.

The only thing not working was the QML loader, because the
plugin had never been scanned in.

## Lesson for the system-specialist surface

When home-manager activation adds, removes, or renames a
Noctalia plugin (i.e. anything under
`modules/home/profiles/min/noctalia-plugins/`, the
`programs.noctalia-shell.settings.bar.widgets` list, or the
`plugins.json` `states` map managed via `inputs.hexis.lib.mkManagedConfig`):

- A `home-manager switch` alone does not pick up the plugin.
  Quickshell scans the plugins directory only at startup.
- The standing restart procedure is to kill the running
  quickshell PID and relaunch `noctalia-shell` detached. Niri's
  `spawn-at-startup` only fires at session start; there is no
  reload IPC for the plugin scan.
- Symptom of a stale quickshell after a plugin deploy is **not**
  "widget missing" — it is "widget renders but never updates,"
  because the older `BarWidgetRegistry` may have a stale entry
  while the new plugin's socket plumbing is invisible. Treat a
  "permanently neutral" widget on a CriomOS-home deploy day as
  a stale-quickshell smell first, before suspecting the widget
  source or the daemon.

This belongs as a one-line note next to the existing
`startWhisrs` script in `CriomOS-home/modules/home/profiles/min/dictation.nix`,
or as a section in the Noctalia-related skill if one is added.
For now this report is the canonical record.

## No code change shipped

The widget code (`BarWidget.qml`), the daemon level-stream
implementation, and the Noctalia plugin wiring are all correct
as-is. No commit landed. The check at
`CriomOS-home/checks/whisrs-level-widget/default.nix` already
guards the reconnect-after-daemon-restart shape from commit
`6acc707`; it does not need to grow to cover this case because
the failure was process lifecycle, not source.
