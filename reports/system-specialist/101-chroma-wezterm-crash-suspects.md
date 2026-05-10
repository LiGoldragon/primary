# Chroma / WezTerm Crash Suspects

## Finding

The strongest evidence does **not** point to Chroma directly sending a fatal
theme operation to WezTerm. Current Chroma no longer emits terminal OSC palette
sequences, no longer scans `/dev/pts`, and no longer writes the old
`wezterm-reload` trigger.

The crash signature points at **Niri/libwayland killing the old WezTerm GUI
client (`pid 878485`) because its Wayland connection buffer hit the 4096-byte
cap**:

```text
May 10 14:08:49.280249 niri[52455]: Data too big for buffer (4088 + 24 > 4096).
May 10 14:08:50.632479 niri[52455]: error in client communication (pid 878485)
May 10 14:08:53.881 wezterm_gui: running message loop: Io error: Connection reset by peer (os error 104); terminating
```

The most likely shape is: Chroma switched global desktop/theme state, Whisrs was
simultaneously finishing a dictation and using clipboard/uinput output against
WezTerm, and the old WezTerm GUI process hit a libwayland fd/input-buffer edge
case. Chroma is still a trigger candidate, but it is currently an **indirect**
trigger candidate, not the component that killed the terminals.

Important correction: one Codex session was also running inside WezTerm at the
time and survived. A later process check showed the surviving Codex process was
under this parent chain:

```text
codex-raw 1221023
zsh       1220694
wezterm-gui 1126815
```

The killed client was a different WezTerm GUI process, `878485`. That means
this was not a clean "all WezTerm instances die" failure, but it also was not
"one terminal window died." Li observed five terminal windows and their agents
being killed. That is compatible with one WezTerm GUI client owning multiple
windows/panes. The Niri binding for `Mod+Shift+Return` spawned the configured
terminal command, and in the WezTerm generation that command was
`${pkgs.wezterm}/bin/wezterm`. WezTerm's own launcher logs say:

```text
Spawned your command via the existing GUI instance.
Use wezterm start --always-new-process if you do not want this behavior.
```

So windows created with `Mod+Shift+Return` were not necessarily independent
Wayland GUI clients. They could be additional windows under the already-running
`wezterm-gui 878485`. Niri killing `878485` would then take out every terminal
window owned by that GUI process, while `wezterm-gui 1126815` stayed alive.
That makes the killed GUI process's local state, active windows,
clipboard/focus path, and client-side Wayland queue more important than any
global "theme switch kills every terminal" explanation.

## Timeline

- `2026-05-07 11:30:02`: systemd started
  `app-niri-wezterm-878485.scope`. This is the GUI client Niri later killed.
- `14:08:38.418`: Chroma wrote
  `/home/li/.local/state/chroma/current-mode`,
  `/home/li/.local/state/chroma/fzf-theme.sh`, and
  `/home/li/.config/ghostty/config`.
- `14:08:38.477-478`: Chroma wrote
  `/home/li/.config/gtk-3.0/settings.ini` and
  `/home/li/.config/gtk-4.0/settings.ini`.
- `14:08:43.446`: Whisrs received `Toggle`.
- `14:08:43.451`: Whisrs stopped recording and began transcribing.
- `14:08:48.153`: the kernel created `whisrs virtual keyboard`.
- `14:08:49.280`: Niri logged `Data too big for buffer (4088 + 24 > 4096)`.
- `14:08:50.632`: Niri logged `error in client communication (pid 878485)`.
- `14:08:52.092`: Whisrs logged `transcription complete: 858 chars`.
- `14:08:52.082`: the virtual keyboard was removed.
- `14:08:53.881`: WezTerm GUI `878485` logged connection reset and terminated.
  Li observed five terminal windows and their agents die in the incident. This
  should be read as "five windows under the killed GUI client" unless further
  evidence shows multiple GUI clients were also killed.
- During the incident, `wezterm-gui 1126815` survived. The active Codex process
  was later confirmed as a child of a shell under that surviving GUI process.
  This constrains the failure to the killed GUI client/window group, not the
  entire compositor or every WezTerm session.
- `14:09:21.575`: a new WezTerm scope was started manually.

Important sequencing detail: Whisrs logs `transcription complete` after the
batch processing path has already copied output to the clipboard and attempted
keyboard output. So the virtual-keyboard interval is part of the output path,
not just idle transcription.

Important spawn-path detail: `Mod+Shift+Return` launched `wezterm`, but
`wezterm` defaults to reusing an existing GUI instance. The launcher log at
`09:39:51` returned `window_id: 48`, showing the long-lived GUI already had many
windows. Launchers at `13:05`, `13:06`, `13:07`, `13:14`, and `13:57` returned
`window_id: 1` through `5` after the separate `wezterm-gui 1126815` appeared.
So the report should distinguish "Niri launched a new terminal window" from
"Niri launched an independent Wayland GUI client"; those are not the same under
WezTerm's default behavior.

## Mechanism

The installed stack is using Niri `25.11` with libwayland `1.24.0`.
`libwayland-server.so.0.24.0` contains both strings observed in the journal:

- `Data too big for buffer (%zu + %zu > %zu).`
- `error in client communication`

In the Nix source tarball for Wayland `1.24.0`,
`src/connection.c` implements `ring_buffer_ensure_space()`. That function logs
the “Data too big” message when a connection ring buffer would exceed its
maximum. `src/wayland-util.h` defines `WL_MAX_MESSAGE_SIZE` as `4096`.

The exact `4088 + 24 > 4096` shape is significant. Normal incoming data checks
reserve one byte before `recvmsg`; the `+ 24` is more consistent with ancillary
FD-buffer pressure, where 24 bytes means six queued file descriptors. So this
does not look like “the clipboard text was 858 chars and exceeded a Wayland
message.” Wayland clipboard content normally moves through pipes/fds. It looks
more like WezTerm had a backlog of fd-bearing Wayland traffic that Niri had not
processed/cleared.

External reports show the same signature in other Wayland stacks:

- Mozilla bug 1986236 reports Firefox/Wayfire on libwayland 1.24 with
  `Data too big for buffer (4088 + 20 > 4096)` and discussion that this is
  message/buffer-size pressure, not app text size:
  <https://bugzilla.mozilla.org/show_bug.cgi?id=1986236>
- KDE bug 458469 reports KWin killing clients after the same libwayland error;
  a KWin maintainer says it comes from libwayland and the client connection is
  terminated:
  <https://bugs.kde.org/show_bug.cgi?id=458469>
- Wayland `connection.c` shows the ring-buffer cap and logging path:
  <https://chromium.googlesource.com/external/wayland/wayland/+/refs/heads/master/src/connection.c>

## Suspects

### 1. WezTerm client fd-buffer overflow under stress

Evidence:

- Niri named WezTerm GUI `pid 878485` as the client with bad communication.
- WezTerm then logged that its message loop got `Connection reset by peer`.
- WezTerm Wayland code can send fd-bearing requests through SHM/frame paths and
  clipboard/paste paths.
- The killed process was the older long-lived GUI with many active windows and
  agent sessions.

This is the primary suspect. The exact trigger is still unknown because the
available logs do not identify the Wayland request or fd source.

The surviving WezTerm-hosted Codex session strengthens this suspect in a more
specific form: the failure was likely tied to one GUI process's connection queue
or active windows, not to every WezTerm process and not to a compositor-global
terminal teardown.

That also means "WezTerm" is too coarse as a noun here. The failing noun is
specifically `wezterm-gui 878485` as one Wayland client. `wezterm-gui 1126815`
was another Wayland client and survived the same compositor, same Chroma daemon,
same Niri process, and same desktop session.

The practical failure blast radius was still large: if `878485` owned five
windows, then one Wayland client kill destroyed five terminal surfaces and five
agent sessions.

### 2. Whisrs output interacting with WezTerm

Evidence:

- Whisrs was in the output window when Niri killed WezTerm.
- It created a virtual keyboard at `14:08:48`, one second before the libwayland
  error.
- Whisrs writes successful transcripts to the clipboard and then uses uinput to
  type at the cursor. If a character is not typeable through the detected XKB
  map, Whisrs falls back to clipboard paste.
- WezTerm paste reads Wayland clipboard offers via `offer.receive(...)`, which
  sends a fd-bearing request.

This does not prove Whisrs alone can generate 1000 queued fds. It is still a
high-signal co-trigger because it was active at the exact failure time.

### 3. Chroma desktop concern as an indirect trigger

Evidence:

- Chroma did switch state at `14:08:38`, about 11 seconds before Niri killed
  WezTerm.
- Current Chroma concerns are independent actors. The terminal concern writes
  only `current-mode` and `fzf-theme.sh`; desktop writes dconf/GTK settings;
  Ghostty writes its config; Emacs calls `emacsclient` if configured.
- Current Chroma has hard-constraint tests ensuring no `/dev/pts` fanout,
  no `wezterm-reload`, and no CLI/daemon live terminal OSC sequence.

So Chroma may have caused redraw/focus/appearance churn, but the current code
does not have a direct path to kill WezTerm.

### 4. Stale old WezTerm GUI state

Evidence:

- The old GUI log still contains many earlier
  `Failed to apply config overrides ... {"color_scheme": ...}` errors from the
  removed live-override era.
- Those errors are timestamped `09:58`, not at the crash time, so this is not
  the direct crash event.

This is a medium/low suspect: long-lived WezTerm process state may have been
weird, but the crash itself was a Wayland connection reset from Niri.

### 5. Internal RPC palette probe

Low suspect. The earlier `SetPalette` RPC probe was run against the newer
single pane and completed quickly. The later destructive action was a full
Chroma theme switch, not that isolated pane probe.

## Tactical Fix Candidates

1. **Stop using WezTerm for active agent work.** Switching the default terminal
   to Ghostty was the right immediate containment. Keep WezTerm out of critical
   sessions until there is a disposable repro.

2. **Disable or gate the WezTerm focus clipboard workaround.** The current
   WezTerm config still runs `wl-paste -n | wl-copy` on every
   `window-focus-changed`. That external process is not the direct pid Niri
   killed, but it adds clipboard churn around focus changes. Given the incident,
   it should be treated as suspect until isolated.

3. **Test a Niri buffer-size patch.** Wayland `1.24.0` exposes
   `wl_display_set_default_max_buffer_size`; Rust `wayland_server::DisplayHandle`
   exposes `set_default_max_buffer_size`. Niri creates the display in
   `/git/github.com/YaLTeR/niri/src/main.rs`:

   ```rust
   let display = Display::new().unwrap();
   ```

   A diagnostic patch could set a larger default before clients connect, e.g.
   `display.handle().set_default_max_buffer_size(1024 * 1024)`, then test
   whether the WezTerm/Whisrs failure disappears. This would not permit
   individual Wayland messages larger than 4096, but it should help if the real
   failure is fd/input backlog rather than one illegal message.

4. **Build a disposable repro, not a production test.** The next useful test is
   a separate Niri/WezTerm session with `WAYLAND_DEBUG=client`, a clean WezTerm
   config, and controlled Whisrs/clipboard/focus steps. Do not run another full
   Chroma switch inside production WezTerm windows.

5. **If WezTerm ever becomes a direct launcher again, do not use bare
   `wezterm`.** Bare `wezterm` reuses the existing GUI instance and concentrates
   many terminal windows into one Wayland client. Use Ghostty as the default, or
   use an explicit WezTerm command such as `wezterm start --always-new-process`
   only after testing that it really limits blast radius in Niri.

## What I Would Not Conclude Yet

- I would not say “WezTerm is definitely the wrong terminal.” The direct failure
  is a Wayland/libwayland client-buffer kill, and other apps have hit similar
  errors.
- I would not say “Chroma is fixed” in the broad sense. It no longer has the
  direct WezTerm-killing paths we removed, but its desktop concern can still be
  part of a multi-component trigger.
- I would not say “clipboard text length caused the crash.” The failure shape
  points more strongly at queued fds or buffered protocol traffic.

## Next Probe

The most useful next probe is:

1. Patch or locally wrap Niri to call `set_default_max_buffer_size` before any
   clients connect.
2. Start one disposable WezTerm GUI under that Niri session with
   `WAYLAND_DEBUG=client`.
3. Reproduce only the Whisrs output path first.
4. Then add Chroma desktop switching.
5. Compare against the same sequence with the WezTerm focus clipboard workaround
   removed.

That separates the three credible axes: WezTerm fd traffic, Whisrs output, and
Chroma appearance/focus churn.
