# WezTerm Live Palette Research

Date: 2026-05-10
Role: system-specialist

## Question

Can Chroma safely switch running WezTerm windows by sending OSC palette
sequences one window at a time, and can it know that one window finished
before touching the next?

## Short Answer

Not with WezTerm's public CLI surface.

OSC palette sequences are output parsed by the terminal. `wezterm cli
send-text` sends input to the child application in a pane, so it is not
a direct way to make WezTerm parse OSC for another pane. Writing to
`/dev/pts/<n>` can target a pane's terminal stream, but that is the
global live-terminal fanout pattern already forbidden in Chroma: it is
out-of-band, has no terminal-render acknowledgement, and can disturb
agent panes.

WezTerm has an internal RPC named `set_configured_palette_for_pane`
that accepts `SetPalette` for a pane and returns `UnitResponse`, but it
is not exposed as `wezterm cli set-palette`. The response means the mux
accepted and applied the palette state; it does not mean the GUI has
finished repainting the pane/window.

Follow-up correction: the internal `SetPalette` RPC does not appear to
call the terminal-state `make_all_lines_dirty()` path directly. That
dirty-all-lines path is specific to OSC palette changes parsed by a
pane's terminal emulation state. Internal `SetPalette` still emits
`Alert::PaletteChanged`, invalidates the visible window, and has no
render-completion acknowledgement, so it is lower risk than OSC but not
proven safe for agent-heavy WezTerm sessions.

## Source Findings

Local source clone:
`/git/github.com/wezterm/wezterm`

The clone was created with `ghq get https://github.com/wezterm/wezterm.git`.
The checked-out upstream head is:

`577474d89ee61aef4a48145cdec82a638d874751 2026-03-31`

That matches the installed `wezterm 0-unstable-2026-03-31` family.

### OSC Color Changes Are Pane-State Changes

WezTerm documents OSC 4 as changing/querying palette entries, and OSC
10/11/12 as foreground/background/cursor changes:

<https://wezterm.org/escape-sequences.html#operating-system-command-sequences>

In source, OSC 4 is handled in
`/git/github.com/wezterm/wezterm/term/src/terminalstate/performer.rs`.
It mutates the pane palette and then calls `palette_did_change()`:

- `term/src/terminalstate/performer.rs:942`
- `term/src/terminalstate/performer.rs:962`

OSC 10/11/12 follow the same shape through `ChangeDynamicColors`:

- `term/src/terminalstate/performer.rs:987`
- `term/src/terminalstate/performer.rs:1038`

`palette_did_change()` calls `make_all_lines_dirty()` and emits
`Alert::PaletteChanged`:

- `term/src/terminalstate/mod.rs:927`

`make_all_lines_dirty()` iterates all physical lines in the current
screen storage:

- `term/src/terminalstate/mod.rs:935`
- `term/src/screen.rs:982`

This is the likely freeze amplifier. A palette change is not a tiny
metadata update; it invalidates terminal line state and triggers GUI
work. Since WezTerm GUI windows share one `wezterm-gui` process, enough
work in one pane can make unrelated windows appear frozen.

This statement applies to OSC palette changes, not necessarily to the
internal `SetPalette` RPC.

### `send-text` Is Not an OSC Delivery Mechanism

WezTerm's docs say `wezterm cli send-text` sends text to input in a pane:

<https://wezterm.org/cli/cli/send-text.html>

The source confirms it calls `write_to_pane` or `send_paste`:

- `wezterm/src/cli/send_text.rs:38`
- `wezterm/src/cli/send_text.rs:46`

That is child-application input, not terminal-parser output. Sending
OSC through this route would hand escape bytes to the shell/program
running inside the pane, not directly to WezTerm's OSC parser.

### `set_config_overrides` Is Per-Window But Has No Ack

WezTerm documents `window:set_config_overrides(overrides)` as a
per-window override API and warns that each call emits
`window-config-reloaded`:

<https://wezterm.org/config/lua/window/set_config_overrides.html>

The Lua binding just notifies the window and returns:

- `wezterm-gui/src/scripting/guiwin.rs:195`

The actual window handler reloads config when it later processes
`TermWindowNotif::SetConfigOverrides`:

- `wezterm-gui/src/termwindow/mod.rs:1185`

This can change one window, but there is no external CLI event for
targeting a selected window and no completion acknowledgement for
"finished rendering after reload".

### Internal Per-Pane Palette RPC Exists

There is an internal client RPC:

- `wezterm-client/src/client.rs:1381`
  `set_configured_palette_for_pane(SetPalette, UnitResponse)`

The mux server handles `Pdu::SetPalette`, updates the pane config,
emits `Alert::PaletteChanged`, and returns `UnitResponse`:

- `wezterm-mux-server-impl/src/sessionhandler.rs:918`
- `wezterm-mux-server-impl/src/sessionhandler.rs:945`
- `wezterm-mux-server-impl/src/sessionhandler.rs:950`

This is the most promising mechanism if we are willing to depend on
WezTerm internals. It is pane-scoped and avoids writing to `/dev/pts`.
It does not go through `term/src/terminalstate/performer.rs`, so it
does not directly call `palette_did_change()` or
`make_all_lines_dirty()`. It still has only an acceptance/state-update
acknowledgement, not a render-completion acknowledgement.

On the GUI side, a `PaletteChanged` alert invalidates the window if the
pane is visible:

- `wezterm-gui/src/termwindow/mod.rs:1218`
- `wezterm-gui/src/termwindow/mod.rs:1434`

For remote/client panes, receiving `Pdu::SetPalette` marks cached
render lines stale:

- `wezterm-client/src/pane/clientpane.rs:171`
- `wezterm-client/src/pane/renderable.rs:425`

That is still repaint/render-cache work in the shared GUI process, but
it is not the same expensive terminal-state dirty-all-lines path as OSC.

## Upstream Signals

Relevant upstream docs and issues:

- WezTerm dynamic colors are officially supported through escape
  sequences:
  <https://wezterm.org/config/appearance.html#dynamic-color-escape-sequences>
- Runtime `color_scheme` changes have an open bug where active panes can
  miss theme updates:
  <https://github.com/wezterm/wezterm/issues/6664>
- There is an open request for a programmatic reload trigger like kitty
  `SIGUSR1`, which means this integration gap is known:
  <https://github.com/wezterm/wezterm/issues/5878>
- OSC 4 has at least one open bug around large palette queries:
  <https://github.com/wezterm/wezterm/issues/6124>

Issue #6664 is relevant but not a direct match for the freeze. The
maintainer identified OSC palette redefinition by an application as the
reason a pane stopped following config color-scheme changes; the
suggested recovery was `reset` or WezTerm's "reset terminal emulation
state in current pane" command. That supports this conclusion: in
WezTerm, pane-local palette mutation is sticky terminal state, not just
display style.

Issue #5878 is also relevant but not a direct match. It asks for a
programmatic config reload trigger for generated themes and has no
comments. It does not discuss all-window freezes, acknowledgement, or
per-pane sequencing.

Searches for exact upstream reports of "theme switch freezes all
windows" / "OSC palette freezes all windows" did not find a direct match
in WezTerm issues. The closest confirmed upstream reports are unreliable
runtime color-scheme propagation and sticky palette overrides.

## Current Live State

The active WezTerm GUI socket is:

`/run/user/1001/wezterm/gui-sock-878485`

`wezterm cli` without `WEZTERM_UNIX_SOCKET` tried a stale
`gui-sock-803389`. With the active socket set explicitly:

`WEZTERM_UNIX_SOCKET=/run/user/1001/wezterm/gui-sock-878485 wezterm cli --no-auto-start list --format json`

WezTerm listed seven GUI panes/windows with `tty_name` values. That
proves Chroma can discover windows/panes, but it does not provide a
safe OSC delivery or render-completion protocol.

## Design Consequences For Chroma

Do not reintroduce OSC writes from Chroma to running WezTerm panes.
There is no safe external acknowledgement for render completion, and
writing to `/dev/pts` is still the wrong layer.

The only plausible implementation path is a dedicated WezTerm concern
actor with one of these modes:

1. **Conservative default:** persist Chroma state only. New WezTerm
   windows pick it up through config. Running windows are not mutated.

2. **Experimental internal RPC:** use WezTerm's internal
   `set_configured_palette_for_pane` RPC one pane at a time. Treat
   `UnitResponse` as "mux accepted state", not "GUI rendered". Add a
   strict timeout, inter-pane delay, circuit breaker, and a hard cap per
   theme switch. Because this path does not directly call
   `make_all_lines_dirty()`, it is the only live-update route worth
   testing. Test only in an isolated disposable WezTerm instance first.

3. **Upstream-quality path:** propose or implement a real WezTerm API:
   a public `wezterm cli set-palette --pane-id/--window-id` plus an
   acknowledgement that fires after GUI invalidation has drained for the
   target window/pane.

Until option 2 is proven under load, Chroma should keep the current
safety behavior: no automatic live WezTerm mutation.
