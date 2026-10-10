# Listener Live Level And Cancel Scout Map

## Task And Scope

Tracker item: `primary-zddv.1`.

Scope: diagnose Listener live level/status responsiveness, shortcut collision risk, and cancel entry points without editing source files, reading transcript text, reading audio contents, reading secrets, deleting artifacts, or intentionally triggering transcription/API spend.

Host/date: `ouranos`, `2026-07-02T15:44:10+02:00`.

Important probe note: two bounded Listener live probes started capture through `listener start`, observed only `$XDG_RUNTIME_DIR/listener/status.sock` JSON frames, then restarted `listener.service` instead of calling `listener stop`. This avoided the transcription/clipboard path but changed runtime state and retained short capture artifacts. The artifact names/sizes were listed; contents were not read.

## Context And Commands Consulted

Required context files read:

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/OperatingSystemImplementer-LiveActivationEvidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`

Tracker/intent:

- `bd show primary-zddv.1`
- `bd show primary-zddv.1 --json`
- `spirit "(PublicTextSearch [Listener level status shortcut cancel])"` returned `(Error [no matching record])`.
- `orchestrate "(Observe Roles)"` showed no active claim on Listener or CriomOS-home; `cloud-maintainer` and `cloud-operator` had unrelated claims.

Live commands:

- `systemctl --user show listener.service whisrs.service --property=Id,ActiveState,SubState,ExecMainPID,ExecStart,FragmentPath,EnvironmentFiles,LoadState --no-pager`
- `systemctl --user cat listener.service --no-pager`
- `listener status`
- `whisrs status`
- `timeout 2s nc -U /run/user/1001/listener/status.sock`
- `timeout 2s nc -U /run/user/1001/whisrs/level.sock`
- bounded Listener `listener start` plus status-stream observation, followed by `systemctl --user restart listener.service`
- bounded Whisrs `whisrs toggle` plus level-stream observation, followed by `whisrs cancel`
- `journalctl --user -u listener.service --since '5 minutes ago' --no-pager`
- `readlink -f /home/li/.nix-profile/bin/listener`
- `pgrep -a -u "$USER" -f 'noctalia|quickshell|qs'`
- `/proc/332129/environ` and `/proc/332129/cmdline` for the running QuickShell environment
- `niri msg -j outputs` and `niri msg -j version`

Source/files inspected:

- `/git/github.com/LiGoldragon/listener/src/status.rs`
- `/git/github.com/LiGoldragon/listener/src/capture.rs`
- `/git/github.com/LiGoldragon/listener/src/runtime.rs`
- `/git/github.com/LiGoldragon/listener/src/command.rs`
- `/git/github.com/LiGoldragon/listener/src/daemon.rs`
- `/git/github.com/LiGoldragon/listener/src/configuration.rs`
- `/git/github.com/LiGoldragon/listener/src/recording_log.rs`
- `/git/github.com/LiGoldragon/listener/Cargo.toml`
- `/git/github.com/LiGoldragon/listener/Cargo.lock`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/sfwbar.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/BarWidget.qml`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/listener-dictation-bindings/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/signal-listener/schema/lib.schema`
- `/git/github.com/LiGoldragon/signal-listener/src/lib.rs`
- `/git/github.com/LiGoldragon/whisrs/src/audio/capture.rs`
- active Noctalia files under `~/.config/noctalia`

## Observed Facts

### Live Identity And Activation

- `listener.service` was active/running before probes and after abort/restart. Before the live probe it had `ExecMainPID=329096`; after the final restart it had `ExecMainPID=396942`.
- `whisrs.service` was active/running throughout and ended idle.
- `/home/li/.nix-profile/bin/listener` resolves to `/nix/store/kgg9iqj7rskbiz256jlmdlagbfvgf1a6-listener-0.4.0/bin/listener`.
- The live Listener service starts `/nix/store/hfls6dbc9i1fny7yxm295wf0gdc2lkw4-listener-daemon`; `listener-daemon --version` is not supported and returned the expected status-socket already-running error when run beside the service.
- CriomOS-home `flake.lock` pins Listener revision `4080f8e89acc173ac124d814147e13dcb971a7a5` at `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:1077-1097`.
- The checked-out Listener working copy is clean at empty change `cb2cb9da`, parent `4080f8e8 main | listener: classify actor transcription failures`.
- Active Noctalia has both plugins enabled and ordered with Listener before Whisrs:
  - `~/.config/noctalia/settings.json` has `plugin:listener-level` then `plugin:whisrs-level`.
  - `~/.config/noctalia/plugins.json` has both `listener-level` and `whisrs-level`.
  - Active plugin QML files resolve through Nix store paths.
- The running QuickShell process is PID `332129`, has `XDG_RUNTIME_DIR=/run/user/1001`, and has `QS_CONFIG_PATH=/nix/store/msd24381zn1d6vb97a2wr8vi9b3xrji7-noctalia-shell-2026-04-25_a50c921/share/noctalia-shell`.
- No recent journal lines matched Noctalia/QML/socket errors in the last 15 minutes.

### Listener Status Socket Live Behavior

Idle-only observation:

- `timeout 2s nc -U /run/user/1001/listener/status.sock` emitted one frame:
  - `{"state":"idle","level":0.0}`

First bounded recording probe:

- `pre_status=(StatusReported Idle)`
- Initial socket frame: `1782999708.989 {"state":"idle","level":0.0}`
- `listener start` returned `(Started 6)`.
- `1782999709.266 {"state":"recording","level":0.0}` arrived promptly.
- The next observed Listener level frames did not arrive until `1782999711.799`, about 2.53 seconds later.
- Eight frames then arrived within about 13 ms with levels around `0.0624..0.0642`.
- `mid_status=(StatusReported (Capturing (6 /home/li/.local/state/listener/captures/capture-6.listenerlog)))`
- The service restart aborted the capture without invoking `listener stop`; immediate `listener status` briefly hit `Connection refused`, then the service recovered to `(StatusReported Idle)`.

Second bounded recording probe:

- `pre_status=(StatusReported Idle)`
- Initial socket frame: `1782999738.939 {"state":"idle","level":0.0}`
- `listener start` returned `(Started 7)`.
- `1782999739.190 {"state":"recording","level":0.0}` arrived promptly.
- First nonzero burst started at `1782999741.750`, about 2.56 seconds after the recording frame.
- Eight frames arrived within about 17 ms, all around `0.0620..0.0651`.
- A second burst started at `1782999744.282`, about 2.53 seconds later.
- That second burst delivered eight frames within about 39 ms, all around `0.0619..0.0662`.
- `mid_status=(StatusReported (Capturing (7 /home/li/.local/state/listener/captures/capture-7.listenerlog)))`
- After `systemctl --user restart listener.service`, `post_status=(StatusReported Idle)`.

Artifact retention from probes:

- `capture-6.listenerlog` exists at `64768` bytes.
- `capture-7.listenerlog` exists at `129408` bytes.
- No artifact contents were read and no artifacts were deleted.

### Whisrs Level Feed Behavior

Idle-only Whisrs observation:

- `timeout 2s nc -U /run/user/1001/whisrs/level.sock` emitted repeated idle frames, not just the initial frame:
  - `{"state":"idle","level":0.0}`
  - `{"state":"idle","level":0.0}`
  - `{"state":"idle","level":0.0}`

Bounded Whisrs recording/cancel probe:

- `pre_whisrs_status=idle`
- `whisrs toggle` returned `recording`.
- Whisrs emitted immediate recording frames and then steady frames roughly every 50-55 ms.
- Example sequence:
  - `1782999763.830 {"state":"recording","level":0.0}`
  - `1782999763.877 {"state":"recording","level":0.06072539}`
  - `1782999763.931 {"state":"recording","level":0.06477243}`
  - `1782999763.985 {"state":"recording","level":0.063218236}`
  - continuing at the same cadence through `1782999768.322`.
- `mid_whisrs_status=recording`
- `whisrs cancel` returned `idle`.
- The socket then emitted `recording level 0.0` and `idle level 0.0`.
- `post_whisrs_status=idle`.

Whisrs source support for the observed behavior:

- `/git/github.com/LiGoldragon/whisrs/src/audio/capture.rs:197-204` computes and sends a normalized level inside the input callback.
- `/git/github.com/LiGoldragon/whisrs/src/audio/capture.rs:226-228` resets level to `0.0` on stop.
- `/git/github.com/LiGoldragon/whisrs/src/audio/capture.rs:234-253` uses the same soft-compressed RMS shape: `1.0 - exp(-rms * 18.0)`.

### Listener Runtime/Status Source Facts

- Listener status states are `idle`, `recording`, `transcribing`, `copied`, and `error` in `/git/github.com/LiGoldragon/listener/src/status.rs:20-37`.
- Listener microphone level uses RMS over s16le PCM and the same soft compression as Whisrs in `/git/github.com/LiGoldragon/listener/src/status.rs:64-79`.
- `StatusPublisher::publish_recording_level` publishes a `recording` event immediately to the status stream channel in `/git/github.com/LiGoldragon/listener/src/status.rs:177-197`.
- The status server accepts clients nonblocking, writes the current event to new clients, drains all waiting status messages, broadcasts every event to connected clients, and has a 25 ms loop delay in `/git/github.com/LiGoldragon/listener/src/status.rs:344-405`.
- The status server writes client streams with blocking `write_all` and prunes only failed writes in `/git/github.com/LiGoldragon/listener/src/status.rs:376-388`. This is a potential backpressure risk if a client stops reading, but the live probes showed delivered bursts rather than a permanently blocked stream.
- Listener starts the status stream before the request/reply socket in `/git/github.com/LiGoldragon/listener/src/daemon.rs:37-46`.
- Listener capture defaults to `LISTENER_CAPTURE_PROGRAM` or `parecord` with `--device=@DEFAULT_SOURCE@ --raw --format=s16le --rate=16000 --channels=1` in `/git/github.com/LiGoldragon/listener/src/capture.rs:271-284`.
- CriomOS-home sets `LISTENER_CAPTURE_PROGRAM` to the Nix `parecord` path in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:60-67`.
- Listener writes capture stdout through `CaptureWriter`, appends complete PCM payloads to the `.listenerlog`, then publishes the microphone level from each payload in `/git/github.com/LiGoldragon/listener/src/capture.rs:402-417` and `/git/github.com/LiGoldragon/listener/src/capture.rs:439-463`.
- The maximum record payload is `8192` bytes in `/git/github.com/LiGoldragon/listener/src/recording_log.rs:22`, which is about 256 ms of 16 kHz mono s16le audio. The live bursts delivered multiple 8192-byte payloads nearly at once after larger upstream buffering.
- Listener publishes a zero-level `recording` event on successful start in `/git/github.com/LiGoldragon/listener/src/runtime.rs:188-209`.
- During ordinary `stop`, Listener stops capture, recovers/exports the recording, transcribes, and delivers clipboard output in `/git/github.com/LiGoldragon/listener/src/runtime.rs:94-160`. This is why the live probe used service restart rather than `listener stop`.

### Listener QML/Noctalia Facts

- The Listener widget reads `XDG_RUNTIME_DIR + "/listener/status.sock"` in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:21-22`.
- It parses newline JSON, reads `event.state`, clamps `Number(event.level || 0.0)` to `0.0..=1.0`, and stores it in `microphoneLevel` in `BarWidget.qml:39-53`.
- Its state names match Listener's JSON states: `recording`, `transcribing`, `copied`, `error`, and `idle` in `BarWidget.qml:23-33`.
- Its reconnect logic mirrors the Whisrs plugin with `Socket`, `SplitParser`, and a 1 s timer in `BarWidget.qml:71-109`.
- During `recording`, bar height is purely `Math.round(4 + root.microphoneLevel * 16 * modelData)` in `BarWidget.qml:129-132`.
- During `transcribing`, a timer animates `activityTick` every 110 ms in `BarWidget.qml:111-116`, but no equivalent timer/decay/smoothing exists for `recording`.
- Bar height animation duration is 80 ms in `BarWidget.qml:141-146`.
- With observed quiet-room levels around `0.06`, the tallest recording bar height computes to roughly `5` px, only about 1 px above idle height.
- Whisrs QML uses the same socket parsing and 80 ms height behavior, but Whisrs' daemon provides continuous frames around every 50-55 ms during recording.

### Shortcut Facts

Current Whisrs bindings in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:296-318`:

- `Mod+V` -> `whisrs toggle-copy`
- `Mod+Shift+V` -> `whisrs toggle`
- `Mod+Alt+V` -> `whisrs-recall`
- `Mod+Ctrl+V` -> `whisrs cancel`

Current Listener binding in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:320-324`:

- `Mod+Alt+L` -> `listener-toggle-capture toggle`

Current lock binding in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix:419-420`:

- `Mod+L` -> `systemctl --user start criomos-lock-session.service`

Lock implementation surfaces:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix:104-111` defines `criomos-lock-session`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix:113-130` starts the lock listener loop.

Scoped searches found no existing `Mod+...M` binding under `modules/home/profiles/{min,med,max}` or checks.

### Cancel Contract/Command Facts

Committed and deployed shape:

- Listener CLI supports only `start`, `stop <session>`, and `status` in `/git/github.com/LiGoldragon/listener/src/command.rs:35-63`.
- The deployed CLI rejected `--version`; no `cancel` command is exposed.
- Listener runtime handles only `Input::Start`, `Input::Stop`, and `Input::Status` in `/git/github.com/LiGoldragon/listener/src/runtime.rs:72-79`.
- Listener `stop` necessarily runs transcription and delivery after capture stop in `/git/github.com/LiGoldragon/listener/src/runtime.rs:94-160`.
- Listener `Cargo.lock` pins `signal-listener` to committed revision `16b54472f43c9e3cf20b5bef726617156ce8b3a4` at `/git/github.com/LiGoldragon/listener/Cargo.lock:1198-1200`.
- The committed `signal-listener` parent `16b54472` has only `Start`, `Stop`, and `Status`, with `OperationKind [Start Stop Status]`, in `jj file show -r @- schema/lib.schema` lines 7-16 and 86-99.

In-progress local contract work:

- `/git/github.com/LiGoldragon/signal-listener` has a dirty working copy with changes to `ARCHITECTURE.md`, `Cargo.lock`, `Cargo.toml`, `README.md`, `build.rs`, `schema/lib.schema`, `src/lib.rs`, `src/schema/lib.rs`, and `tests/round_trip.rs`.
- That dirty working copy adds `Cancel CancelCapture`, `Cancelled CaptureCancelled`, `CancelCapture CaptureSession`, `CaptureCancelled { CancelledSession DurableAudioArtifact }`, and `OperationKind Cancel` in `schema/lib.schema`.
- Those dirty `signal-listener` edits are not proven committed, pushed, pinned by Listener, or deployed.

## Interpretations

### Is Listener `status.sock` Streaming Changing Levels?

Listener `status.sock` is not completely frozen. It did stream changing `level` values during recording.

However, its live cadence is stale/bursty enough to match the user-observed "stuck/frozen/not flowing" meter:

- prompt state transition to `recording level 0.0`;
- roughly 2.5 s gap;
- burst of 8 changing frames within milliseconds;
- another roughly 2.5 s gap;
- another burst.

By contrast, Whisrs emitted recording frames roughly every 50-55 ms for the whole capture window and cancelled back to idle cleanly.

### Likely Runtime Root Cause

Most likely failing boundary: Listener capture/PCM publication cadence before or at `CaptureWriter`, caused by external `parecord` stdout buffering and the current "publish only when PCM payloads are appended" design.

Evidence:

- The level calculation itself mirrors Whisrs and did produce plausible nonzero values.
- `StatusPublisher` and `StatusStreamLoop` broadcast promptly once `publish_recording_level` is called.
- Bursts contained multiple changing payload-level frames in a few milliseconds, implying the status socket received a backlog of PCM payload publications at once.
- The burst interval is much larger than the 25 ms status loop delay and much larger than the 8192-byte payload duration, so the dominant delay is upstream of broadcast.
- Runtime transcription actor and clipboard delivery are not in the recording path and were not involved during the live probes.

Secondary runtime risk: the status server writes to connected Unix streams using blocking `write_all`. A non-reading client could block the status thread. The live symptom observed here does not require that explanation, but `primary-zddv.3` should consider setting client streams nonblocking or isolating slow clients when touching the status server.

### Likely QML/Noctalia Contribution

The deployed QML path, socket path, parser, reconnect shape, and state names look correct. There is no evidence of stale activation or plugin instance mismatch.

The widget can still look frozen even when Listener emits bursty frames because:

- recording mode has no timer, smoothing, decay, or interpolation independent of incoming frames;
- 8 frames arriving inside 20-40 ms will be collapsed by an 80 ms height animation into one small movement;
- the observed `0.06` level maps to roughly one pixel of bar height change;
- after the burst, no new frames arrive for about 2.5 s, so the widget sits still.

The main fix should be runtime cadence. A small QML improvement is also justified: add a displayed-level smoother/decay or recording animation clock and adjust visual gain so quiet but real input is legible. That would make the widget resilient to minor cadence jitter, but it should not hide a multi-second producer stall.

## Recommended Fix Scope

For `primary-zddv.3` runtime:

- Prefer changing Listener capture-level publication so UI frames are pushed at a steady cadence comparable to Whisrs, ideally around 30-60 Hz.
- Best structural direction: move capture/level sampling closer to the input callback or use a capture backend that exposes callback-sized audio buffers instead of relying on `parecord` stdout flush behavior.
- If retaining `parecord`, investigate low-latency options or insert a separate level sampler that reads smaller chunks and publishes latest level at a timer cadence.
- Keep `.listenerlog` durability independent from UI status cadence; do not require an 8192-byte durable record append before the UI can move.
- Add focused tests around status event cadence/coalescing and backpressure behavior. Existing tests prove frames exist, not that cadence is usable.

For `primary-zddv.3` QML/CriomOS-home if runtime cadence alone is insufficient:

- Keep the socket path and parsing approach.
- Add a displayed-level property with a short timer/decay/smoothing loop while `recording`.
- Consider a higher visual gain or non-linear mapping so levels near `0.06` visibly move more than one pixel.
- Keep Whisrs untouched unless extracting a shared widget pattern is truly needed.

## Recommended Keybindings

Preserve all current Whisrs `V` bindings.

Move Listener away from the lock key family:

- Listener record/toggle: `Mod+Alt+M`
- Listener cancel: `Mod+Ctrl+Alt+M`

Rationale:

- avoids `Mod+L`, the lock binding;
- avoids the existing Whisrs `V` family;
- scoped source search found no current `Mod+...M` binding;
- `M` is mnemonic for microphone and keeps record/cancel as one key family.

Files/checks likely affected for shortcut implementation:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/listener-dictation-bindings/default.nix`
- possibly hotkey overlay titles in the same dictation module.

## Recommended Cancel Entry Points For `primary-zddv.2`

Committed/deployed Listener currently has no safe cancel. `listener stop <session>` is not cancel because it transcribes and delivers clipboard output.

`primary-zddv.2` should touch:

- `signal-listener/schema/lib.schema` if the dirty local Cancel work is not already owned/landed by another worker;
- generated `signal-listener/src/schema/lib.rs`, `signal-listener/src/lib.rs`, and round-trip tests;
- Listener dependency pin/lock to consume the committed Cancel contract;
- `/git/github.com/LiGoldragon/listener/src/command.rs` to add `listener cancel <session>`;
- `/git/github.com/LiGoldragon/listener/src/runtime.rs` to handle `Input::Cancel`;
- `/git/github.com/LiGoldragon/listener/src/capture.rs` only if `ActiveAudioCapture::stop` needs renaming/splitting so cancel can terminate capture and finalize the artifact without transcription;
- `/git/github.com/LiGoldragon/listener/tests/runtime.rs` for no-transcription/no-delivery cancel tests and status event expectations;
- README/ARCHITECTURE versioning if behavior changes.

Expected cancel semantics:

- require the active session, matching `stop` conflict semantics;
- terminate capture and retain the durable artifact;
- do not export raw PCM for transcription;
- do not call OpenAI/gopass transcription path;
- do not deliver to clipboard;
- return a typed `Cancelled` reply carrying the cancelled session and retained artifact;
- publish an appropriate UI-safe status event, likely `idle` directly or a short terminal `cancelled` state if the status vocabulary is intentionally extended.

Coordination requirement:

- `/git/github.com/LiGoldragon/signal-listener` is dirty with in-progress Cancel edits. A worker must not overwrite those changes. Coordinate/claim or use a separate worktree before implementing `primary-zddv.2`.

## Unknowns And Not Checked

- No private transcript text, clipboard text, audio contents, or secrets were read.
- No real physical microphone tap was performed by this scout. Live recording probes observed ambient/default microphone levels only.
- No OpenAI/API request was intentionally triggered. Listener probes aborted by service restart; Whisrs probe used `whisrs cancel`.
- No source tests were run; this was a read-only scout plus live status/control probing.
- I did not inspect `/nix/store` package contents beyond direct `readlink`/known active paths; no `/nix/store` filesystem search was run.
- I did not close or update tracker items.

## Bottom Line

The live Listener status socket changes, but its recording-level feed is delivered in multi-second bursts. The likely root cause is Listener's capture/PCM publication cadence from `parecord` stdout into `.listenerlog` append events, with QML making the burstiness look even more frozen because recording mode has no independent animation/smoothing and low observed levels barely move the bars. Whisrs demonstrates the expected shape: steady roughly 50 ms recording frames and safe cancel back to idle.
