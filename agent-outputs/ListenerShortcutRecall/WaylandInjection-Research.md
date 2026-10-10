# Wayland Targeted Text/Keystroke Injection — Can You Pin a Destination? (2026)

Research question: On current Linux Wayland, is there a secure, *target-lockable*
mechanism to inject text/keystrokes into a *specific chosen* application / window /
surface, such that the input is guaranteed to reach only that pinned destination and
cannot leak to whatever else happens to be focused? Motivation: replace clipboard-paste
delivery of speech-to-text transcripts with something safer than focus-following
synthetic keystrokes (ydotool/wtype), which type into the wrong window, misfire
modifiers, and drop characters. The ultimate consumer is the user's own agent UI, so a
cooperative app-side receive channel is an acceptable answer.

## Verdict (short)

**No** safe compositor-level targeted-injection path exists on Wayland today. Every
synthetic-input protocol (virtual-keyboard-v1, input-method-v2/text-input-v3,
libei/EI + RemoteDesktop portal, KDE fake-input) feeds the compositor's *seat* input
pipeline and routes to whatever surface currently holds **keyboard focus**. None takes a
destination-surface argument; there is no Wayland analogue of macOS
`CGEventPostToPid` (post to a specific process regardless of focus). The only
compositor with directed keys is **Hyprland** (`sendshortcut`/`pass` with a `window:`
target) — but it is *shortcut/key-click* oriented, not arbitrary Unicode text, it has
the exact stuck-modifier bug the user already hit, and it is **not** available on this
machine (which runs **niri**). Partial at best, and not on niri.

**The safe path is a cooperative app-side receive channel**: have the agent UI expose
its own local endpoint (Unix socket / RPC / paste-into-pane) and write the transcript
directly into that specific process. This is target-locked *by construction* — you
address the process/socket/pane by identity, not by focus — so it cannot leak to any
other window and cannot misfire modifiers. Details and requirements below.

## Local system context (inspected read-only)

- Session: `XDG_SESSION_TYPE=wayland`, `XDG_CURRENT_DESKTOP=niri`, compositor
  **niri 25.11** (Nixpkgs), a smithay-based scrollable-tiling compositor — **not**
  wlroots, **not** KWin/Mutter. So wlroots-specific and KDE/GNOME-specific facilities
  do not directly apply; only what niri (via smithay) implements matters.
- `niri msg` IPC surface has actions for outputs/workspaces/windows/`action`
  (compositor keybind actions) — **no text- or keystroke-injection action**, and no
  Hyprland-style directed `pass`/`sendshortcut` dispatcher.
- niri supports `virtual-keyboard-v1` (community reports confirm `wtype` works on niri),
  which is exactly the focus-following/dangerous path. `wtype` is installed here;
  `tmux` and `nvim` are also installed (both are viable cooperative channels);
  `ydotool` is not installed.

## Mechanism-by-mechanism assessment

### 1. wlroots `virtual-keyboard-v1` / `virtual-pointer` (ydotool, wtype)

- **Target-lockable? NO.** The protocol only associates a virtual keyboard with a
  *seat* (`create_virtual_keyboard`); there is no surface/window argument. Key events
  are routed by the compositor's existing seat/focus system — i.e. to whatever surface
  currently has keyboard focus. (wayland.app protocol reference.)
- **Failure modes = exactly the user's complaint.** Because delivery follows focus, a
  focus change mid-injection (window auto-raise, notification stealing focus, a slow
  app) sends the tail of a transcript into the wrong window. Modifier key up/down events
  are real seat state, so a dropped release leaves a modifier "stuck" (closing windows,
  launching apps, locking screen). Unicode handling is fragile (wtype remaps the keymap
  per character; ydotool has incomplete non-ASCII support), which is the "dropped
  characters" symptom.
- **ydotool note:** ydotool bypasses Wayland entirely via kernel `uinput`, so it is
  even *more* global — a system-wide virtual device with zero targeting and no
  per-client trust boundary.
- **Security posture:** the protocol itself says a compositor "should present an error
  when an untrusted client requests a new keyboard," i.e. the design intent is to
  *gate who may inject at all*, not to let injectors choose a destination.
- Real-world confirmation: a 2025 "SuperWhisper-quality voice typing on Linux" writeup
  delivers transcripts by injecting "into whatever text field has focus via `wtype` or
  `ydotool`," and reports the classic misfire — a literal Enter in the transcript
  "fires off mid-sentence" in a chat app. This is the failure the user wants to escape.

### 2. `input-method-v2` / `text-input-v3` (IME typing into the focused text field)

- **Target-lockable? NO.** text-input focus *follows keyboard focus* on the seat; the
  compositor sends `enter`/`leave` to track the focused text field and an input method
  commits text to whichever client is focused (chain: input-method client → compositor →
  focused application). An input method is effectively a single per-seat global; you
  cannot bind it to a chosen client while a different client is focused.
- **Additional constraints:** the destination app must itself implement text-input-v3
  (many toolkits still lag — e.g. JetBrains only shipped text-input-v3 in 2025.3), so
  even the focus-following path silently no-ops in non-participating apps. A smithay bug
  thread also shows compositors mishandling multiple text-input instances. Not a
  targeting mechanism.

### 3. `security-context-v1` and per-client input restrictions

- **Not an injection mechanism; it is the opposite.** security-context-v1 lets a sandbox
  engine (e.g. Flatpak, which has merged support) tag a client's connection so the
  compositor can *deny* privileged interfaces (screencopy, virtual-keyboard, etc.) to
  that client. It restricts *who may inject*; it provides no way to *direct* injected
  input to a destination. Relevant only as evidence that the ecosystem's security model
  treats input injection as a privilege to be gated, not a routable, addressable action.

### 4. xdg-desktop-portal `RemoteDesktop` + libei / EI (emulated input)

- **Target-lockable? NO.** EI's own architecture states emulated events "feed into the
  input stack in the same way as input events from physical devices. To Wayland clients,
  they are indistinguishable from real devices" — i.e. they enter the seat pipeline and
  follow focus. There is no destination-window parameter.
- **The per-client control in libei is about the *source*, not the *destination*.** The
  compositor always knows *which emulating client* is injecting and can suspend/deny/
  filter *that emulator* (e.g. "no keyboard capability for you"). That is directed
  *restriction of the injector*, not directed *delivery to a chosen target*. These are
  easy to conflate; they are opposite ends.
- **Confirmed failure mode in practice:** UI-test users of xdg-desktop-portal-kde report
  that "other windows get focused and some interactions are performed on other windows,
  not on the application under test" — precisely the leak the user is trying to avoid.
- Portal `RemoteDesktop` also requires an interactive user grant per session and is
  screen-cast/remote-control shaped, adding friction without buying any targeting.

### 5. Compositor-specific directed-input facilities

- **Hyprland — the only real "directed key" facility, and it is partial + buggy.**
  `sendshortcut`/`pass` dispatchers take an optional `window:` (class-regex) target and
  can deliver a key *click* to a background window without focusing it
  (e.g. `hyprctl dispatch sendshortcut ,j ,class:firefox`). But:
  - It sends **shortcuts / individual key clicks, not arbitrary Unicode text** — there
    is no "send this transcript string" primitive. Per-character key events to a
    non-focused window are an *open feature request* (issue #9488, PR #9599), i.e. not
    shipped as general text injection.
  - It exhibits **the exact modifier-stuck bug** the user described: the synthetic
    modifier can be left in a pressed state, "corrupting subsequent keyboard shortcuts"
    (discussion #14099). XWayland targets are additionally "wonky."
  - **It is Hyprland-only and does not exist on niri.**
- **niri:** no directed-input dispatcher and no IPC injection action (inspected above).
- **KDE KWin:** `kde-fake-input` is an XTest-style facility "to provide fake input
  events" (testing, KDE Connect touchpad) — global, focus-following, no target argument.
  KRdp/RemoteDesktop is remote-control shaped, again focus-following.
- **GNOME Mutter:** exposes emulated input through the RemoteDesktop portal + libei —
  same focus-following model as §4, no targeting.
- Net: **no mainstream compositor offers safe, arbitrary-text, target-locked delivery.**
  Hyprland is the closest and still fails the "no-leak, no-misfire, arbitrary text" bar,
  and is irrelevant on this niri host.

### 6. App-side programmatic input channels (cooperative receive)

This is the category that actually satisfies "target-lockable, no-leak," because the
destination is addressed by **identity** (a socket path, server address, or pane id),
never by focus. Since the consumer is the user's own agent UI, this is fully in scope.
Representative mechanisms, all target-locked by construction:

- **Neovim RPC / server socket.** `nvim --listen <sock>` exposes a msgpack-RPC server;
  another process connects with `nvim --server <sock> --remote-send '<keys>'` or
  (better for text) an `nvim_paste` / `nvim_input`/buffer API call. Text goes only to
  that specific Neovim instance; nothing reaches any other window. `neovim-remote`
  wraps this. (If the agent UI is or embeds Neovim, this is ideal.)
- **Terminal remote-control / send-text.**
  - `tmux send-keys -t <pane> -l '<text>'` (the `-l` = literal flag is essential so the
    transcript is inserted as text, not interpreted as key names) targets one pane by id.
  - `wezterm cli send-text --pane-id <id>` sends text to a specific pane.
  - `kitty @ send-text --match ...` (kitty remote control) sends text to a chosen
    window/tab.
  All three address a specific pane/window by id and cannot leak to another.
- **Bracketed-paste into a chosen pty.** Writing the transcript wrapped in
  `ESC[200~ ... ESC[201~` into the target program's pty makes it arrive as an atomic
  *paste* (not keystrokes), so embedded control chars/newlines are treated as literal
  text by paste-aware apps — removing the "literal Enter fires the message" misfire.
- **A purpose-built local endpoint on the agent UI itself.** If the agent UI is your own
  program, the cleanest answer is to give it a tiny local receive channel — a Unix-domain
  socket, a localhost HTTP/websocket endpoint, or a D-Bus method — into which the STT
  daemon writes `{ text }`. The UI inserts it into its own input box. This is
  target-locked (only that process listens on that address), leak-proof (no seat, no
  focus, no synthetic keys), modifier-safe (it's data, not key events), and lossless
  (no keymap round-trip). It is the direct analogue of macOS posting an event to a
  specific pid.

**Requirement this places on the destination app:** it must *cooperate* — expose one of
the above (RPC socket / remote-control / a small local receive endpoint) and insert
received text into its focused input field itself. For the user's own agent UI this is a
small, one-time addition and is the recommended design.

## Why compositor-level targeting is structurally absent

Wayland deliberately has no global input state and no cross-client addressing: a client
cannot name or reach another client's surface. Input is a property of the *seat*, and the
compositor is the sole authority that routes seat input to the focused surface. "Inject a
key" therefore necessarily means "inject into the seat," which necessarily means "goes to
focus." Adding destination-addressed injection would require a new privileged protocol
that lets one client name and write into another client's surface — which is exactly the
capability Wayland's security model was built to prevent. Hence the ecosystem gates
*whether* you may inject (security-context, portal grants, per-emulator control in EI)
rather than offering a *where-to* parameter. macOS can do `CGEventPostToPid` because its
window server keeps per-process event queues addressable by pid; Wayland has no
equivalent and, by design intent, is unlikely to grow one.

## Recommendation

1. **Do not adopt focus-following synthetic keystrokes** (wtype/ydotool/virtual-keyboard-
   v1, portal/libei, KDE fake-input). On niri specifically, `wtype` works but is exactly
   the unsafe focus-following path; there is no compositor-level fix for the leak/misfire.
2. **Deliver via a cooperative app-side channel into the user's own agent UI.** Order of
   preference:
   a. Add a small **local receive endpoint** to the agent UI (Unix socket / localhost
      websocket / D-Bus). Best: target-locked, leak-proof, modifier-safe, lossless.
   b. If the UI runs inside Neovim/kitty/wezterm/tmux, use that tool's **RPC / send-text /
      send-keys -l** against a fixed instance/pane id, ideally via **bracketed paste**.
3. **Keep clipboard paste as the universal fallback** for arbitrary third-party apps that
   expose no cooperative channel — it is the only method that never leaks to the wrong
   window (the user controls the paste), which is why the tool uses it today.

## Sources

- Virtual keyboard protocol (routing follows seat focus; untrusted-client trust note):
  https://wayland.app/protocols/virtual-keyboard-unstable-v1
- wtype (virtual-keyboard-v1 based text typing) and Wayland fragmentation:
  https://github.com/atx/wtype ,
  https://www.semicomplete.com/blog/xdotool-and-exploring-wayland-fragmentation/
- KDE Plasma lacks zwp_virtual_keyboard_v1; ydotool uses kernel uinput:
  https://gist.github.com/danielrosehill/d3913d4c8cc69acaf3ee7772771c2f1d
- text-input-v3 (focus-following enter/leave):
  https://wayland.app/protocols/text-input-unstable-v3 ;
  input-method-v2: https://wayland.app/protocols/input-method-unstable-v2 ;
  input-method chain + focus: https://dorotac.eu/posts/input_method/ ;
  smithay multi-instance text-input bug: https://github.com/Smithay/smithay/issues/1884
- security-context-v1 (restricts sandboxed clients; not a routing mechanism):
  https://wayland.app/protocols/security-context-v1 ;
  https://www.phoronix.com/news/Flatpak-Wayland-Security-Ctx ;
  https://blog.ce9e.org/posts/2025-10-03-wayland-security/
- libei/EI (emulated input feeds the normal input stack, indistinguishable from real
  devices; per-emulator restriction is source-side, not destination-side):
  https://libinput.pages.freedesktop.org/libei/ ;
  https://www.phoronix.com/news/libei-1.0-Emulated-Input ;
  http://who-t.blogspot.com/2020/08/libei-library-to-support-emulated-input.html
- xdg-desktop-portal RemoteDesktop / InputCapture (focus-following; wrong-window reports):
  https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html ;
  https://invent.kde.org/plasma/xdg-desktop-portal-kde/-/issues/12
- Hyprland directed keys (`sendshortcut`/`pass` with window target; text-vs-shortcut
  limit; stuck-modifier bug):
  https://wiki.hypr.land/Configuring/Basics/Binds/ ;
  https://github.com/hyprwm/Hyprland/issues/9488 ;
  https://github.com/hyprwm/Hyprland/discussions/14099
- KDE fake-input (XTest-style, global):
  https://wayland.app/protocols/kde-fake-input
- Real-world STT-on-Wayland delivery via wtype/ydotool into focused field + misfire:
  https://guillaume.id/blog/how-i-got-superwhisper-quality-voice-typing-on-linux/ ;
  https://github.com/peteonrails/voxtype/blob/main/README.md
- Cooperative app channels: Neovim remote/RPC:
  https://neovim.io/doc/user/remote.html , https://github.com/mhinz/neovim-remote ;
  wezterm send-text: https://github.com/wezterm/wezterm/discussions/4753 ;
  kitty send-text / remote control: https://sw.kovidgoyal.net/kitty/faq/
- niri (this host): scrollable-tiling smithay compositor, runs voice-typing via wtype:
  https://github.com/niri-wm/niri/wiki/Configuration:-Key-Bindings
