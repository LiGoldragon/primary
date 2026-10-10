# Scout Situational Map

## Task And Scope

Tracker item: `primary-acmr.1`.

Scope: map the existing Whisrs visual/status cue and Listener's current public
and local state surfaces for internal transcription/status work. This scout did
not implement source changes, edit repos, read transcript text, or read audio
artifact contents.

## Commands And Files Consulted

Context files:

- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerFreshHandover/ContextHandover.md`
- `/home/li/primary/agent-outputs/ListenerDirectSttConfig/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/PrimaryJwx0/OperatingSystemImplementer-Evidence.md`

Tracker and intent:

- `bd show primary-acmr.1 --json`
- `spirit "(PublicTextSearch [Listener Whisrs status visual status bar transcription])"` returned `(Error [no matching record])`.

Repos and runtime probes:

- `/git/github.com/LiGoldragon/CriomOS-home`
- `/git/github.com/LiGoldragon/listener`
- `/git/github.com/LiGoldragon/signal-listener`
- `/git/github.com/LiGoldragon/meta-signal-listener`
- `/git/github.com/LiGoldragon/whisrs`
- `systemctl --user is-active listener.service whisrs.service`
- `systemctl --user show listener.service whisrs.service --property=Id,ActiveState,SubState,ExecMainPID,FragmentPath,LoadState`
- `listener status`
- `whisrs status`
- `timeout 2s nc -U /run/user/1001/whisrs/level.sock | sed -n '1,5p'`
- `ls -l /run/user/1001/whisrs`

## Observed Facts

### Whisrs Status-Bar Visual Cue

- CriomOS-home installs a Noctalia/QuickShell plugin named `whisrs-level`.
  The plugin manifest says it shows the Whisrs recording level in the Noctalia
  bar and uses `BarWidget.qml` as the bar widget entry point:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/manifest.json:2`,
  `:6`, `:7-9`.
- The widget keeps local properties `whisrsState` and `microphoneLevel`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/BarWidget.qml:16-17`.
- The widget reads `$XDG_RUNTIME_DIR/whisrs/level.sock`:
  `BarWidget.qml:19-20`.
- The widget expects newline-delimited JSON. `consumeLevelMessage` parses each
  line, reads `event.state`, and clamps `event.level` to `0.0..=1.0`:
  `BarWidget.qml:33-38`.
- Live socket evidence confirms the frame shape. `timeout 2s nc -U
  /run/user/1001/whisrs/level.sock | sed -n '1,5p'` emitted repeated lines
  like `{"state":"idle","level":0.0}`.
- The widget treats `recording` and `transcribing` as active:
  `BarWidget.qml:21`.
- The widget color is `Color.mSecondary` while `transcribing`,
  `Color.mPrimary` while `recording`, and a muted on-surface variant when idle:
  `BarWidget.qml:22-28`. This is theme-relative, not hard-coded red/yellow in
  the widget.
- The widget draws five small bars with tapered heights from
  `[0.48, 0.76, 1.0, 0.76, 0.48]`; height is
  `4 + active * microphoneLevel * 16 * taper`, with short animations on height
  and color: `BarWidget.qml:78-105`.
- The widget has reconnect logic through `scheduleReconnect`, a `Socket`, a
  `SplitParser`, and a one-second retry timer:
  `BarWidget.qml:44-75`.
- CriomOS-home enables the plugin in the Noctalia bar's right section before
  the tray: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/sfwbar.nix:34-51`.
- CriomOS-home enables the plugin in Noctalia's managed `plugins.json` state and
  sources the manifest and QML into `~/.config/noctalia/plugins`:
  `sfwbar.nix:64-87`.
- The check `checks/whisrs-level-widget/default.nix` validates reconnect-related
  QML strings but does not validate daemon-side socket production:
  `/git/github.com/LiGoldragon/CriomOS-home/checks/whisrs-level-widget/default.nix:3-14`.
- Whisrs also has its own tray implementation. It creates a ksni
  StatusNotifierItem and chooses grey idle, red recording, and yellow
  transcribing circle icons:
  `/git/github.com/LiGoldragon/whisrs/src/tray/service.rs:11-52`,
  `:64-105`.
- Whisrs tray updates come from a `tokio::sync::watch::Receiver<State>`:
  `tray/service.rs:114-169`.
- Whisrs' local source state machine has only `Idle`, `Recording`, and
  `Transcribing` and transitions `Idle -> Recording -> Transcribing -> Idle`:
  `/git/github.com/LiGoldragon/whisrs/src/state.rs:1-61`.
- Whisrs audio capture computes a normalized RMS-derived level from i16 samples
  using `1.0 - exp(-rms * 18.0)`, clamped to `0.0..=1.0`:
  `/git/github.com/LiGoldragon/whisrs/src/audio/capture.rs:234-253`.
- Whisrs capture sends the computed level through an optional watch sender on
  every audio callback and resets it to `0.0` on stop:
  `capture.rs:197-204`, `:226-228`.
- Whisrs daemon constructs watch channels for state and level, passes state to
  tray, and passes state plus level to overlay when enabled:
  `/git/github.com/LiGoldragon/whisrs/src/daemon/main.rs:591-622`.
- Whisrs transitions to recording and sends state on start:
  `daemon/main.rs:852-863`.
- Whisrs transitions to transcribing on stop, sends state, and resets level:
  `daemon/main.rs:875-890`.
- Whisrs transitions back to idle after transcription, sends state, resets
  level, saves history, and may notify with a preview:
  `daemon/main.rs:917-960`.
- Whisrs cancel resets level and notifies cancellation:
  `daemon/main.rs:2011-2039`.
- Local Whisrs source search did not find the daemon code that serves
  `/run/user/1001/whisrs/level.sock`. The live socket exists and emits the
  expected frames; CriomOS-home pins `whisrs-src` to the `criomos` branch at
  rev `c32c8bcf793abbe4492398c2b10738950972f2e5`:
  `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:82-88`,
  `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:3156-3171`. The local
  `/git/github.com/LiGoldragon/whisrs` checkout is not proven to be that pinned
  source revision.

### Listener Current State Surfaces

- Listener's ordinary public wire contract currently exposes inputs `Start`,
  `Stop`, and `Status`:
  `/git/github.com/LiGoldragon/signal-listener/schema/lib.schema:7-9`.
- Listener's ordinary replies are `Started`, `Stopped`, `StatusReported`,
  `CaptureAlreadyActive`, `NoActiveCapture`, `CaptureSessionMismatch`, and
  `RequestUnimplemented`: `signal-listener/schema/lib.schema:10-16`.
- Current `CaptureStatus` is only `Idle` or `Capturing ActiveCapture`:
  `signal-listener/schema/lib.schema:53-59`.
- `CaptureStopped` includes the stopped session, audio artifact, transcript
  text, and delivery outcomes:
  `signal-listener/schema/lib.schema:69-84`. This is useful for CLI replies but
  unsafe as a bar feed because it can carry private transcript text.
- The ordinary contract crate documents that runtime capture, disk writes,
  transcription, and clipboard delivery live in the listener daemon:
  `/git/github.com/LiGoldragon/signal-listener/src/lib.rs:1-5`.
- The CLI supports only `start`, `stop <session>`, and `status`; it prints the
  daemon reply directly:
  `/git/github.com/LiGoldragon/listener/src/command.rs:27-63`.
- `listener status` in the live session returned `(StatusReported Idle)`.
- The `listener-toggle-capture` OS wrapper currently parses the CLI's printed
  status strings: exact idle match `(StatusReported Idle)`, active match
  `(StatusReported (Capturing (`; it then starts or stops with the parsed
  session:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:129-163`.
- The client connects to the configured Unix socket and sends a single
  length-prefixed contract frame, then receives one output:
  `/git/github.com/LiGoldragon/listener/src/client.rs:28-33`.
- The daemon is a blocking Unix socket server. It binds the working socket,
  handles one request frame per connection, calls `ListenerRuntime::handle_input`,
  and sends one reply frame:
  `/git/github.com/LiGoldragon/listener/src/daemon.rs:69-90`.
- The transport uses `signal_listener::Frame` over a 4-byte
  length-prefixed frame with a 16 MiB default maximum:
  `/git/github.com/LiGoldragon/listener/src/transport.rs:31-80`,
  `:195-230`.
- Configuration defaults the working socket to `$XDG_RUNTIME_DIR/listener.sock`,
  the meta socket to `$XDG_RUNTIME_DIR/listener-meta.sock`, and capture storage
  to `$XDG_STATE_HOME/listener/captures` or
  `~/.local/state/listener/captures`:
  `/git/github.com/LiGoldragon/listener/src/configuration.rs:88-153`.
- Environment knobs are documented in the README: `LISTENER_SOCKET`,
  `LISTENER_META_SOCKET`, `LISTENER_CAPTURE_STORE`,
  `LISTENER_CAPTURE_PROGRAM`, `LISTENER_TRANSCRIPTION_PROGRAM`, and
  `LISTENER_CLIPBOARD_PROGRAM`:
  `/git/github.com/LiGoldragon/listener/README.md:36-43`.
- The meta CLI is scaffolded and returns not implemented:
  `/git/github.com/LiGoldragon/listener/src/meta.rs:25-33`.
- `meta-signal-listener` only defines a privileged `Configure` contract and is
  not a current UI status surface:
  `/git/github.com/LiGoldragon/meta-signal-listener/schema/lib.schema:1-36`.
- Runtime status returns `Idle` unless there is an active capture, in which case
  it returns `Capturing` with session and durable artifact:
  `/git/github.com/LiGoldragon/listener/src/runtime.rs:124-135`,
  `:234-239`.
- Runtime tests prove status over the socket returns a public
  `StatusReported Idle` frame with the matching exchange:
  `/git/github.com/LiGoldragon/listener/tests/runtime.rs:558-608`.
- Live user services are active and running. `systemctl --user show
  listener.service whisrs.service --property=...` reported both `ActiveState=active`,
  `SubState=running`; `listener.service` PID was `3789462`, `whisrs.service`
  PID was `3193790`.
- Live runtime socket/artifact surface exists: `/run/user/1001/listener.sock`
  exists with `srw-rw----`; `/home/li/.local/state/listener/captures` exists.
  Artifact filenames were observed but contents were not read.
- Current service units:
  - `listener.service` has optional `EnvironmentFile=-%h/.config/listener/environment`
    and `ExecStart=/nix/store/...-listener-daemon`.
  - `whisrs.service` has `ExecStart=/nix/store/...-whisrs-daemon`.

### Stopgap Listener Transcription Path

- CriomOS-home defines `listenerOpenAiTranscribe` as a Nix
  `writeShellScriptBin "listener-openai-transcribe"` in
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:20-78`.
- That wrapper expects one raw PCM input path, converts raw s16le 16 kHz mono
  PCM to a temporary WAV through ffmpeg, reads the provider key from gopass at
  runtime, calls OpenAI REST `/v1/audio/transcriptions` with
  `gpt-4o-transcribe`, and prints only transcript text:
  `dictation.nix:20-78`.
- The Listener service wrapper currently exports
  `LISTENER_TRANSCRIPTION_PROGRAM` to that separate command by default:
  `dictation.nix:119-127`, specifically `:124`.
- `listenerOpenAiTranscribe` is included in `home.packages`:
  `dictation.nix:165-170`.
- The example local override file documents the same external command path:
  `dictation.nix:200-207`.
- The check `checks/listener-dictation-bindings/default.nix` currently asserts
  that the generated Listener service wrapper contains
  `LISTENER_TRANSCRIPTION_PROGRAM=`, references `listener-openai-transcribe`,
  and does not mention Whisrs:
  `/git/github.com/LiGoldragon/CriomOS-home/checks/listener-dictation-bindings/default.nix:83-94`.
- Prior evidence records this as a stopgap and says the successor graph rejects
  the separate command/program production shape:
  `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/TrackerWeaver-WorkGraph.md`,
  "Observed facts" and "Dependency Order" sections.

### Listener Code Areas For primary-acmr.2

- Capture start/stop:
  - `src/runtime.rs:69-121` controls start/stop lifecycle.
  - `src/runtime.rs:149-178` allocates the next capture and calls the capture backend.
  - `src/runtime.rs:207-244` models the active capture and stop handoff.
  - `src/capture.rs:237-367` owns the process capture backend and kill/wait stop.
  - `src/capture.rs:370-449` writes raw PCM into `.listenerlog`.
- Transcription dispatch:
  - `src/runtime.rs:96-111` recovers the log, exports raw PCM, builds
    `BatchTranscriptionInput`, and calls `self.transcriber.transcribe(...)`.
  - `src/transcription.rs:85-143` is the current external command seam through
    `LISTENER_TRANSCRIPTION_PROGRAM`.
  - `src/transcription.rs:146-170` is the honest not-configured stub.
- Clipboard/output delivery:
  - `src/runtime.rs:112-120` dispatches transcript output and includes outcomes
    in `CaptureStopped`.
  - `src/delivery.rs:38-79` routes configured output targets.
  - `src/delivery.rs:81-158` implements `wl-copy`-style clipboard delivery via
    `LISTENER_CLIPBOARD_PROGRAM`.
- Daemon/public state:
  - `src/runtime.rs:19-28` holds daemon state fields, currently
    `active_capture` and `orphaned_recordings` but no transcribing/copied/error
    phase.
  - `src/daemon.rs:69-90` is the blocking request/reply daemon surface.
  - `signal-listener/schema/lib.schema:7-16`, `:53-84` are the public contract
    extension points.

### Listener Code Areas For primary-acmr.4

- CriomOS-home dictation module:
  - `modules/home/profiles/min/dictation.nix:119-127` Listener service wrapper.
  - `dictation.nix:129-163` `listener-toggle-capture`.
  - `dictation.nix:241-266` `listener.service`.
  - `dictation.nix:354-388` Niri bindings for Whisrs and Listener.
- Noctalia bar integration:
  - `modules/home/profiles/min/sfwbar.nix:34-51` bar placement and tray.
  - `sfwbar.nix:64-87` plugin enable/source management.
  - `modules/home/profiles/min/noctalia-plugins/whisrs-level/BarWidget.qml`
    is the closest existing widget pattern to copy or generalize for Listener.
- Checks to update:
  - `checks/listener-dictation-bindings/default.nix` currently enforces the
    stopgap external transcriber and should be inverted or replaced once
    Listener owns internal transcription.
  - `checks/whisrs-level-widget/default.nix` is a model for a lightweight QML
    smoke check but currently only covers reconnect strings.

## Interpretations

- The status-bar mechanism to preserve is the Noctalia plugin path, not Waybar.
  Waybar is present in `modules/home/profiles/min/waybar.nix`, but the active
  Whisrs cue is declared in Noctalia through `sfwbar.nix`.
- The simplest visual compatibility target for Listener is the same newline
  JSON shape as Whisrs' live `level.sock`: `{"state":"idle|recording|transcribing|copied|error","level":0.0..1.0}`.
  This would let primary-acmr.4 adapt the existing QML pattern with minimal UI
  invention.
- Listener needs a status/event surface beyond current request/reply `status`.
  Polling `listener status` can only show `Idle` or `Capturing`; it cannot show
  transcribing, copied, terminal error state, or live mic activity. A pushed
  local stream/socket is a better match for the existing Whisrs bar and the
  workspace's push-oriented dictation guidance.
- `CaptureStopped` should not be the bar feed because it carries
  `TranscriptText`. A status indicator should receive only phase, session if
  needed, level/RMS, and redacted error class/message, never transcript text.
- The internal transcription implementation should replace
  `ConfiguredBatchTranscriber`/`BatchTranscriptionCommand` as the production
  path, while keeping a test seam or explicit dev override only if the
  implementer decides it is still useful outside normal production.
- The runtime currently does all stop work synchronously inside
  `ListenerRuntime::stop`. To expose `transcribing` and `copied` in real time,
  primary-acmr.2 likely needs to split stop into state changes around capture
  stop, transcription dispatch, and delivery completion, then publish events.
- Because the current daemon is blocking, an async actor path will likely touch
  `src/daemon.rs`, `src/runtime.rs`, and the capture/transcription/delivery
  seams together rather than only adding fields to `StatusReported`.

## Minimal State/Events To Expose

Recommended non-transcript event/state payload for primary-acmr.2:

- `idle`: no active capture/transcription/delivery. Include no transcript.
- `recording`: include active session, optional artifact path only if needed by
  trusted CLI; bar feed does not need artifact path.
- `mic_activity`: while recording, publish normalized `level` or `rms` in
  `0.0..=1.0`. Whisrs' existing compressor is a proven local formula:
  RMS over i16 PCM, then `1.0 - exp(-rms * 18.0)`.
- `transcribing`: emitted after capture stops and before OpenAI request starts
  or while it is in flight. Bar target color: yellow.
- `copied`: emitted after system clipboard delivery succeeds. Also trigger a
  desktop notification from CriomOS-home or Listener without transcript text.
- `error`: emitted for capture, transcription, and delivery failures. Include a
  coarse kind such as `capture`, `transcription`, `clipboard`, and a redacted
  diagnostic suitable for logs/status, not secrets or transcript text.

Status-bar mapping for primary-acmr.4:

- idle: muted bar.
- recording: red bar with live level.
- transcribing: yellow bar, no mic level or a deterministic shimmer if the UI
  wants motion.
- copied: short success state and desktop notification, then idle.
- error: visible error state or notification, then idle/error until next event
  depending on runtime semantics.

## Constraints

- Preserve Whisrs side by side:
  - Keep Whisrs bindings `Mod+V`, `Mod+Shift+V`, `Mod+Alt+V`, and
    `Mod+Ctrl+V`; current checks assert these:
    `checks/listener-dictation-bindings/default.nix:58-69` and
    `checks/whisrs-dictation-bindings/default.nix:47-58`.
  - Keep Listener on `Mod+Alt+L` unless the operator changes the binding:
    `dictation.nix:383-387`.
  - Do not reuse `/run/user/1001/whisrs/level.sock`; use a Listener-owned
    socket/path such as `$XDG_RUNTIME_DIR/listener/status.sock` or a typed
    contract subscription.
  - Keep Whisrs service and `whisrs-level` plugin intact during Listener trial.
- Keep secrets private:
  - Source and evidence show provider credentials are read through runtime
    secret plumbing; no secret values were read or reported by this scout.
  - Listener's future internal OpenAI path should read credentials at runtime
    from the secret store or service environment and must not include values in
    commits, status events, notifications, or reports.
  - Do not expose transcript text through the status bar, event stream,
    notification body, logs, or scout/audit evidence. Current `CaptureStopped`
    carries `TranscriptText`, so UI integration must avoid subscribing to that
    as its ordinary feed.
- Avoid private artifacts:
  - `.listenerlog`, `.raw.s16le`, and Whisrs history are local/private runtime
    artifacts. This scout listed paths but did not read contents.

## Open Unknowns And Blockers

- The exact source implementation of the live `/run/user/1001/whisrs/level.sock`
  server was not found in the local Whisrs checkout inspected under
  `/git/github.com/LiGoldragon/whisrs`. The live socket and QML consumer prove
  the deployed surface shape. A future worker needing the daemon source should
  inspect the pinned `whisrs-src` revision
  `c32c8bcf793abbe4492398c2b10738950972f2e5` directly, without treating the
  local checkout as authoritative.
- The desired Listener status subscription contract is not settled. The two
  likely shapes are:
  - extend `signal-listener` with typed status/event subscription frames; or
  - add a local UI-only newline JSON status socket analogous to Whisrs.
- Current Listener has no async daemon/actor runtime. primary-acmr.2 must decide
  how far to move from the blocking request/reply loop while preserving the
  existing CLI and tests.
- Current checks intentionally assert the stopgap external transcriber. They
  will fail until primary-acmr.4 updates them after internal transcription lands.

## Checks Not Run

- No Nix build/check was run.
- No source files or repository files were edited.
- No capture, transcription, clipboard read, or smoke test was run.
- No Whisrs history or Listener audio/transcript artifact contents were read.
