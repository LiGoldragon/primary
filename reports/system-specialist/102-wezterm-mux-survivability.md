# WezTerm Mux Survivability

## Finding

Yes, WezTerm has machinery that can keep terminal sessions alive after a GUI
window goes away, but our incident path was not using that machinery in a way I
would trust for agent survival.

The dangerous path is **bare `wezterm` from a launcher**. Our logs showed bare
`wezterm` repeatedly printing:

```text
Spawned your command via the existing GUI instance.
Use wezterm start --always-new-process if you do not want this behavior.
```

That means `Mod+Shift+Return` could create new windows under an existing
`wezterm-gui` Wayland client. If that GUI client is killed by Niri/libwayland,
all windows under that GUI client die together.

The survival path is different: put the real program in a mux server, then let
GUI windows attach to that mux. In that shape, a GUI crash should disconnect the
view but leave the mux-owned panes alive, as long as the mux server itself stays
alive.

## Evidence

Local evidence:

- The killed GUI client was `wezterm-gui 878485`.
- The surviving Codex session was under a different GUI client,
  `wezterm-gui 1126815`.
- The old launcher logs show many windows being spawned through an existing GUI
  instance rather than as independent GUI clients.
- Current `wezterm cli list-clients` shows the live GUI client as the only
  client. Running with `--prefer-mux` did not reveal a separate durable client
  boundary in the current config.

WezTerm documentation:

- `wezterm start --always-new-process` avoids asking an existing GUI instance to
  start the command:
  <https://wezterm.org/cli/start.html>
- `wezterm cli` first targets a mux server only when `--prefer-mux` is passed;
  otherwise it can target a running GUI instance:
  <https://wezterm.org/cli/cli/index.html>
- `wezterm cli spawn --domain-name ... --new-window` can spawn into a named
  multiplexer domain:
  <https://wezterm.org/cli/cli/spawn.html>
- Unix domains are WezTerm's local mux boundary; docs show `unix_domains` plus
  `default_gui_startup_args = { "connect", "unix" }` so the GUI connects to the
  unix-domain mux on startup:
  <https://wezterm.org/multiplexing.html#unix-domains>
- `quit_when_all_windows_are_closed = false` keeps the GUI process running when
  all windows are closed, but that is not sufficient protection against a
  compositor killing the GUI process:
  <https://wezterm.org/config/lua/config/quit_when_all_windows_are_closed.html>

Prior art / user reports:

- A WezTerm discussion describes a tmux-like workflow built around
  `wezterm-mux-server` and `unix_domains`, with sessions staying active after
  closing the attached GUI window:
  <https://github.com/wezterm/wezterm/discussions/1322>
- A WezTerm Q&A shows users getting confused by having many WezTerm GUI windows
  but no mux server, and the maintainer suggests `wezterm cli --prefer-mux
  spawn` as a diagnostic/start path:
  <https://github.com/wezterm/wezterm/discussions/2031>
- A Reddit thread asks for exactly the "keep sessions in memory after closing
  GUI and reattach later" shape:
  <https://www.reddit.com/r/wezterm/comments/1g3gn1c/wezterm_gui_reopens_when_i_close_it/>

## Options

### Option 1: Keep Ghostty as the normal terminal

This is the containment path. It does not solve WezTerm survival, but it avoids
using the fragile GUI as the default place where agents live.

### Option 2: WezTerm isolated GUI processes

Use:

```text
wezterm start --always-new-process
```

This limits blast radius between windows because the launcher no longer reuses
one existing GUI client. It does **not** make the session survive if that
individual GUI client dies. It only turns "five agents died" into "one agent
died" when the failure is per GUI client.

### Option 3: WezTerm mux-first launcher

Use a dedicated unix-domain mux and attach GUI windows to it. The desired shape
is:

```text
wezterm cli --prefer-mux spawn --domain-name unix --new-window -- codex ...
wezterm connect unix
```

or configure WezTerm so bare GUI startup acts like:

```lua
config.unix_domains = { { name = "unix" } }
config.default_gui_startup_args = { "connect", "unix" }
```

This is the WezTerm-native answer to "window dies, session keeps running." It
needs a controlled test before trusting it with agents, because current local
evidence still shows the live setup operating through a GUI client boundary.

### Option 4: Application-owned launcher outside WezTerm

For Claude/Codex specifically, the stronger architecture is not "make WezTerm
save us"; it is "start the agent under a durable owner, then attach a terminal
view." Examples:

- `tmux new-session -d -s codex-... codex ...`, then attach from Ghostty or
  WezTerm.
- A systemd user transient unit/scope per agent with a PTY attach layer.
- The Persona terminal harness / command-line mind path, once it owns the agent
  lifecycle directly.

This is more robust because terminal GUI death is no longer the process owner.
The terminal becomes a view, not the thing keeping the agent alive.

## Recommendation

Do not make bare WezTerm the launcher again.

For immediate safety, keep Ghostty as default and use tmux/systemd/Persona-style
durable launchers for important agents. If WezTerm must be used, test a
mux-first launcher in a disposable session and prove this invariant before
deploying it:

1. Start an agent through the launcher.
2. Confirm the agent's parent is the mux server or durable supervisor, not
   `wezterm-gui`.
3. Kill only the GUI client.
4. Reconnect and confirm the agent is still alive and interactive.

Only after that test passes should WezTerm be considered a survivable agent
surface.
