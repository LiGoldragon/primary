# WHISRS Input Safety and Targeted Insertion

Report date: 2026-05-11
Role: system-specialist

## Question

The failure mode is real: start WHISRS with `Mod+V`, stop it with `Mod+V`,
and if the physical Mod/Super key is still held while WHISRS inserts the
transcript, transcript letters can become compositor shortcuts. On this Niri
desktop that can close windows, lock the screen, move focus, move windows, or
trigger other destructive window-manager actions.

The requested question is whether there is a safer way to send the transcript
to the intended window, ideally without stealing focus, and what stands between
the wanted behavior and what Linux/Wayland/Niri can support.

## Skill And Repo Reading

I reread the primary workspace intent and system-specialist discipline before
inspecting code:

- `ESSENCE.md`
- `repos/lore/AGENTS.md`
- `protocols/orchestration.md`
- `protocols/active-repositories.md`
- `skills/system-specialist.md`
- `skills/autonomous-agent.md`
- `skills/stt-interpreter.md`
- `skills/reporting.md`
- `skills/jj.md`
- `skills/nix-discipline.md`
- `skills/testing.md`
- `skills/skill-editor.md`
- `skills/rust-discipline.md`
- `skills/actor-systems.md`
- `skills/kameo.md`
- `skills/naming.md`
- `skills/beauty.md`
- `skills/abstractions.md`
- `skills/push-not-pull.md`
- `skills/micro-components.md`
- `skills/contract-repo.md`
- `skills/repository-management.md`
- `skills/architectural-truth-tests.md`

I also read the relevant repo-local docs in `CriomOS-home`, `CriomOS`,
`terminal-cell`, and `persona-system`.

## Current Local Shape

`CriomOS-home` owns the WHISRS user service and Niri bindings:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/clipboard-mode.patch`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/transcript-recovery.patch`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/spool-recovery.patch`

`CriomOS` owns the device permission side:

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/users.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`

The current package pins `github:y0sif/whisrs/v0.1.11`. Local patches add:

- `whisrs toggle-copy`, which copies the transcript without keyboard insertion.
- transcript recovery, which copies successful direct-mode transcripts before
  typing them.
- audio spool recovery for failed transcriptions.

The active keybindings are:

- `Mod+V` -> `whisrs toggle`, direct insertion through the virtual keyboard.
- `Mod+Shift+V` -> `whisrs toggle-copy`, clipboard-only output.

This means the safer mode exists, but it is not the muscle-memory default.

## Root Cause

WHISRS remembers the focused Niri window id when recording starts. On stop, it
restores focus with `niri msg action focus-window --id <id>`, waits briefly, and
then types through a virtual keyboard created with `/dev/uinput`.

The important split:

- The Niri window id only restores focus.
- The text insertion is not addressed to that window id.
- The text insertion is seat-level keyboard input.

At WHISRS v0.1.11, the Niri backend does exactly this:

- `src/window/niri.rs` queries focus with `niri msg --json focused-window`.
- `src/window/niri.rs` restores focus with `niri msg action focus-window --id`.

At WHISRS v0.1.11, insertion does this:

- `src/daemon/main.rs` stores `recording_window_id`.
- `src/daemon/main.rs` later calls `focus_window(wid)`, sleeps 100 ms, then
  calls `type_text_at_cursor`.
- `type_text_at_cursor` creates `UinputKeyboard`.
- `UinputKeyboard::type_text` starts by calling `release_all_modifiers`, then
  emits key events for the transcript.

That `release_all_modifiers` call is not a safety proof. It releases modifier
keys on the WHISRS-created virtual keyboard device. It does not prove that the
human has released the physical keyboard's Super key, and it cannot be treated
as a reliable barrier against compositor shortcuts. The compositor still owns
the real seat state.

This matches the reported hazard exactly: if the human still holds Mod/Super
after the stop shortcut, the injected letters can be read as `Mod+letter`
actions.

## Permission Fact

The current deployed user has `/dev/uinput` access but not `/dev/input/event*`
read access. That is consistent with the system shape:

- `CriomOS` puts edge users in `uinput`.
- udev grants the `uinput` group access to `/dev/uinput`.
- `/dev/input/event*` nodes are group `input`, and the user is not in `input`.

WHISRS upstream includes an optional evdev global hotkey listener, but the
current CriomOS-home config does not enable `[hotkeys]`. Niri owns the hotkeys.
Even if WHISRS' evdev listener were enabled, it would not solve the release
barrier by itself: upstream hotkeys trigger on press, and the current user lacks
the device read permission that would let WHISRS observe physical key releases.

## Wayland And Niri Constraints

Wayland's normal keyboard model is focus-based. The core protocol sends keyboard
enter/leave events for the surface with keyboard focus, and key events are sent
against the active focused surface.

Niri gives us good focus identity and pushed focus observation:

- `niri msg --json focused-window`
- `niri msg --json windows`
- `niri msg --json event-stream`
- `niri msg action focus-window --id <id>`

But Niri IPC is not an arbitrary text-injection API. It can focus a window and
emit/observe focus state. It does not expose "send this text to window id X
without focusing it".

The xdg-desktop-portal RemoteDesktop API and Wayland virtual-keyboard protocol
also model input as remote or virtual keyboard events. They do not provide the
Mac-style "post text to this application/window while the human keeps working
elsewhere" capability as a general Wayland client API.

Text-input/input-method protocols are closer to what speech input wants, because
they commit text rather than synthesizing every key. But they are still tied to
the active text-input focus for a seat. They are a safer possible implementation
for the currently focused editable surface; they are not a general unfocused
window-targeting primitive.

macOS is different here. Apple's accessibility APIs include targeted keyboard
event posting to an application object. That is the kind of authority the Mac
desktop automation stack exposes and Wayland intentionally does not expose as a
normal app capability.

## Prognosis

For arbitrary Wayland GUI applications, clipboard-only is the safe default today.
Direct desktop insertion can be made less dangerous, but not as clean as the
wanted Mac-style targeted insertion unless we add compositor-level privileged
support or app-specific integrations.

For terminals and agent harnesses, the prognosis is much better: do not use
desktop input at all. The right target is the PTY/session, not the window.

`terminal-cell` already has the shape we want:

- a daemon-owned child process group and PTY;
- disposable visible viewers;
- raw programmatic input injection;
- one serialized PTY writer;
- an input gate that can temporarily hold human bytes while programmatic input
  is written contiguously.

That means a Codex/Claude/Pi terminal target can receive transcript bytes
through a socket into the PTY. This does not require focus, does not involve
uinput, does not involve compositor shortcuts, and does not care whether the
human still has Mod held on the physical keyboard.

`persona-system` also points in the right direction: it owns pushed focus and
target observations, with Niri state coming from `niri msg --json windows` and
`niri msg --json event-stream`. That should identify the target; it should not
move terminal bytes.

## Recommended Architecture

### 1. Immediate operational default

Make the safe path the default muscle-memory path:

- `Mod+V` should become clipboard-only until direct insertion has an explicit
  safety gate.
- direct insertion should move to a more explicit binding or be disabled.

This is a nuisance, but it prevents transcript text from becoming desktop
shortcuts.

### 2. If WHISRS keeps direct insertion, add an input safety gate

Direct insertion should be behind an explicit stateful gate:

```text
RecordingStarted(target_window_id)
StopRequested
TranscriptionReady(text)
WaitForHumanModifiersReleased
RestoreAndVerifyTargetFocus
InjectOrFallback
```

Rules:

- No fixed sleeps as correctness barriers.
- No injection while physical modifiers are known or suspected to be held.
- Unknown modifier state must fall back to clipboard.
- Focus restore must be verified through Niri focus observation before typing.
- If focus cannot be restored to the captured target, copy instead of typing.

The missing input is physical modifier release observation. Options:

- Extend WHISRS' evdev listener so it can track physical modifier releases and
  not merely trigger hotkeys.
- Add a small privileged input-observer helper with tightly scoped read access
  to keyboard event devices.
- Use a compositor-provided pushed key-state source if Niri grows one.

The current user permissions do not allow unprivileged `/dev/input/event*`
observation, so this would require a deliberate CriomOS system change if we take
the evdev path.

### 3. For terminal targets, bypass desktop input completely

The better terminal path is:

```text
WHISRS transcript
  -> Persona target resolution
  -> terminal-cell / persona-terminal target
  -> close PTY human input gate
  -> write transcript bytes to PTY
  -> reopen PTY human input gate
```

This is the highest-signal route for Codex, Claude, Pi, and other terminal
harnesses.

### 4. For GUI applications, prefer app-specific integrations

For non-terminal applications:

- clipboard remains the safe universal path;
- editor-specific RPC can be added where worth it;
- browser-specific automation can be added where worth it;
- a Wayland input-method implementation may be useful for focused text fields,
  but it should be treated as focused text input, not unfocused window control.

### 5. Do not build a full compositor just for this

Writing or forking the compositor could create a privileged "commit text to
window id" API. That would solve the general unfocused targeting problem only
inside our compositor. It is large scope, security-sensitive, and not needed for
the terminal/agent workflow. If this becomes necessary, it should be framed as a
Niri extension or a Persona desktop shell project, not as a WHISRS patch.

## Test Plan

The WHISRS direct insertion path needs Nix-wired tests before it becomes the
default again. Test names should state premises:

- `keyboard_insertion_waits_until_human_modifiers_are_released`
- `keyboard_insertion_falls_back_to_clipboard_when_modifier_state_is_unknown`
- `keyboard_insertion_falls_back_to_clipboard_when_target_focus_is_lost`
- `keyboard_insertion_verifies_niri_focus_after_restore`
- `terminal_target_uses_pty_input_instead_of_uinput`
- `terminal_input_gate_holds_human_bytes_during_transcript_injection`
- `niri_focus_observation_uses_event_stream_without_polling`

The risky tests should run in an isolated session or a Niri/systemd sandbox with
test-only windows. They should not inject desktop input into the human's live
session.

## No Live Input Testing Done

I did not toggle WHISRS or inject keys during this investigation. I also did not
quote or preserve transcript contents from WHISRS history in this report.

## Sources

Local source:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/clipboard-mode.patch`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/users.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`
- `/git/github.com/y0sif/whisrs` at tag `v0.1.11`
- `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md`

External references:

- Wayland core keyboard focus:
  `https://wayland.freedesktop.org/docs/html/apa.html`
- Linux uinput:
  `https://kernel.org/doc/html/v4.12/input/uinput.html`
- Wayland virtual keyboard protocol:
  `https://sources.debian.org/src/mir/2.20.2-2/wayland-protocols/virtual-keyboard-unstable-v1.xml`
- Wayland text-input v3:
  `https://cgit.freedesktop.org/wayland/wayland-protocols/tree/unstable/text-input/text-input-unstable-v3.xml`
- Wayland input-method v2:
  `https://sources.debian.org/src/wlroots/0.18.2-3/protocol/input-method-unstable-v2.xml`
- XDG Desktop Portal RemoteDesktop:
  `https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html`
- Niri IPC:
  `https://github.com/niri-wm/niri/wiki/IPC`
- Niri IPC crate docs:
  `https://yalter.github.io/niri/niri_ipc/`
- Apple AXUIElementPostKeyboardEvent:
  `https://developer.apple.com/documentation/applicationservices/1462057-axuielementpostkeyboardevent`
