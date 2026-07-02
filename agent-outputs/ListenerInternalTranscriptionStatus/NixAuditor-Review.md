# CriomOS-home Listener Status-Bar Nix Audit

## Task And Scope

Tracker item: `primary-acmr.5`.

Audited the CriomOS-home Listener status-bar integration and stopgap external
transcription removal. Scope covered the requested commits:

- `/git/github.com/LiGoldragon/CriomOS-home`
  `a4adfc961f06cbbc84ebd59201c4a706e399c388`
- `/git/github.com/LiGoldragon/CriomOS`
  `731d999fb1fcc9f78b79e9cd92a0bff033377037`
- Listener runtime pin
  `4080f8e89acc173ac124d814147e13dcb971a7a5`, version `0.4.0`

No source files were changed. No transcript content, audio artifacts, or secret
values were read. The real spoken smoke test was not run.

## Result

Audit result: **pass**.

No blocking findings were found for `primary-acmr.5`. `primary-acmr.6` can start
after the operator activates/reloads the audited generation under the safe
condition named below.

## Findings

No blocking findings.

## Residual Risks And Operator Actions

The main residual risk is live-session state, not source shape. The audited
source is ready, but the smoke test must not rely on an already-running old
Home/Noctalia/listener process.

Safe activation/reload condition before `primary-acmr.6`:

1. Deploy or activate CriomOS commit
   `731d999fb1fcc9f78b79e9cd92a0bff033377037`, which pins CriomOS-home
   `a4adfc961f06cbbc84ebd59201c4a706e399c388`.
2. Use a safe desktop disruption window: either rebuild and start a new login
   session, or explicitly reload the Home/user profile with the operator's
   consent.
3. Ensure the user systemd manager has the new unit definitions loaded, then
   restart `listener.service`.
4. Restart or start Noctalia/QuickShell so it scans and loads the new
   `listener-level` plugin.
5. Verify before speaking that `listener.service` is from Listener `0.4.0`,
   `$XDG_RUNTIME_DIR/listener/status.sock` exists after daemon start, the
   Listener widget is visible beside the Whisrs widget, and the generated
   listener service wrapper does not export `LISTENER_TRANSCRIPTION_PROGRAM`.

The QML notification path is API-valid for Quickshell: the official
Quickshell.Io `Process` documentation states that `command` is a list of
strings and setting `running` to true starts the process when the command is
non-empty. The deployed environment adds `pkgs.libnotify` to the Home profile,
and the widget invokes `notify-send` by command name. Live delivery through
Mako/Noctalia was not observed here and belongs to `primary-acmr.6`.

## Evidence

### Stopgap External Transcription Removed From Production

Observed facts:

- The production listener service wrapper in
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:60`
  exports `LISTENER_CAPTURE_PROGRAM` and `LISTENER_CLIPBOARD_PROGRAM`, then
  executes `listener-daemon`; it does not export
  `LISTENER_TRANSCRIPTION_PROGRAM`.
- `home.packages` keeps `whisrs`, `listener`, and
  `listener-toggle-capture`, but no `listener-openai-transcribe` package:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:105`.
- The Listener example environment says production transcription is owned by
  `listener-daemon` and only documents capture/clipboard overrides:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:139`.
- Source search in `modules`, `packages`, `flake.nix`, `README.md`, `docs`,
  and `skills.md` found no `LISTENER_TRANSCRIPTION_PROGRAM`,
  `listener-openai-transcribe`, or `listenerOpenAiTranscribe`.
- The only remaining matches for those strings are inverted assertions in
  `checks/listener-dictation-bindings/default.nix:83` and
  `checks/listener-dictation-bindings/default.nix:95`.

Interpretation:

- The stopgap external transcriber is removed from production Home packages,
  examples, and service wrapper.
- The check no longer asserts the rejected external transcription program
  shape; it rejects it.

### Listener Runtime Pin

Observed facts:

- CriomOS-home input `listener` is a GitHub flake input:
  `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:90`.
- CriomOS-home `flake.lock` pins that input to Listener
  `4080f8e89acc173ac124d814147e13dcb971a7a5`:
  `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:1077`.
- `nix eval --raw github:LiGoldragon/listener/4080f8e89acc173ac124d814147e13dcb971a7a5#packages.x86_64-linux.default.version`
  returned `0.4.0`.
- `nix flake metadata --json github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388`
  reported the nested `listener` lock at `4080f8e89acc173ac124d814147e13dcb971a7a5`.

Interpretation:

- CriomOS-home consumes the audited Listener internal transcription/status
  runtime commit and the expected `0.4.0` package version.

### CriomOS Pin To CriomOS-home

Observed facts:

- CriomOS `flake.lock` has a `criomos-home` input with nested
  `"listener": "listener"`:
  `/git/github.com/LiGoldragon/CriomOS/flake.lock:673`.
- CriomOS `flake.lock` pins `criomos-home` to
  `a4adfc961f06cbbc84ebd59201c4a706e399c388`:
  `/git/github.com/LiGoldragon/CriomOS/flake.lock:752`.
- `nix flake metadata --json github:LiGoldragon/CriomOS/731d999fb1fcc9f78b79e9cd92a0bff033377037`
  reported `criomos-home` at `a4adfc961f06cbbc84ebd59201c4a706e399c388`.

Interpretation:

- CriomOS coherently pins the audited CriomOS-home commit for deploy.

### Plugin Install, Placement, And Whisrs Preservation

Observed facts:

- Noctalia right bar order puts `plugin:listener-level` immediately before
  `plugin:whisrs-level`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/sfwbar.nix:45`.
- `plugins.json` managed state enables both `listener-level` and
  `whisrs-level`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/sfwbar.nix:67`.
- `xdg.configFile` installs both Listener and Whisrs plugin manifests and
  QML files:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/sfwbar.nix:90`.
- The Listener plugin manifest has id `listener-level` and bar widget entry
  point `BarWidget.qml`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/manifest.json:2`.
- The Whisrs plugin source remains present and unchanged in the same plugin
  tree.

Interpretation:

- Listener status is installed and enabled adjacent to Whisrs without removing
  Whisrs.

### Widget State Mapping And Privacy

Observed facts:

- The widget reads `$XDG_RUNTIME_DIR/listener/status.sock`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:21`.
- It parses newline-delimited messages with `JSON.parse` and consumes only
  `event.state` plus `event.level`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:39`.
- Recording is red (`#ef4444`) and transcribing is yellow (`#facc15`):
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:26`.
- Idle is muted through `Color.mOnSurfaceVariant` alpha:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:33`.
- Recording bar heights use live `microphoneLevel`; transcribing animates bars
  from a timer:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:111`.
- Copied and error transitions emit generic notifications without transcript
  text:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:44`.
- Socket reconnect behavior mirrors the existing Whisrs pattern through
  `Socket`, `SplitParser`, `scheduleReconnect`, and a one-second timer:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:71`.

Interpretation:

- The widget consumes the Listener status stream shape requested by the Rust
  audit, keeps transcript text out of the bar and notifications, and covers
  idle/recording/transcribing/copied/error visual behavior.

### Keybindings

Observed facts:

- Whisrs bindings remain:
  - `Mod+V` runs `whisrs toggle-copy`:
    `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:296`
  - `Mod+Shift+V` runs `whisrs toggle`:
    `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:302`
  - `Mod+Alt+V` runs `whisrs-recall`:
    `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:308`
  - `Mod+Ctrl+V` runs `whisrs cancel`:
    `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:314`
- Listener binding `Mod+Alt+L` runs `listener-toggle-capture toggle`:
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:320`.

Interpretation:

- Listener was added side by side without replacing the Whisrs operational
  bindings.

### Checks

Observed facts:

- `checks/listener-dictation-bindings/default.nix` imports the dictation
  module, checks all Whisrs bindings, checks `Mod+Alt+L`, checks Listener
  package version `0.4.0` or newer, rejects
  `LISTENER_TRANSCRIPTION_PROGRAM` in the example environment, rejects
  `LISTENER_TRANSCRIPTION_PROGRAM=` and `listener-openai-transcribe` in the
  listener service wrapper, and keeps capture/clipboard program defaults:
  `/git/github.com/LiGoldragon/CriomOS-home/checks/listener-dictation-bindings/default.nix:60`.
- `checks/listener-level-widget/default.nix` validates the plugin manifest,
  bar installation, Whisrs adjacency, libnotify package presence, status socket
  path, JSON parsing, all state names, level consumption, red/yellow colors,
  notifications, and absence of lowercase `transcript`/`text` in the widget:
  `/git/github.com/LiGoldragon/CriomOS-home/checks/listener-level-widget/default.nix:3`.
- Remote build checks passed:
  - `nix build --option eval-cache false github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388#checks.x86_64-linux.listener-dictation-bindings --refresh --no-link`
  - `nix build --option eval-cache false github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388#checks.x86_64-linux.listener-level-widget --refresh --no-link`
  - `nix build --option eval-cache false github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388#checks.x86_64-linux.whisrs-level-widget --refresh --no-link`
  - `nix build --option eval-cache false github:LiGoldragon/CriomOS-home/a4adfc961f06cbbc84ebd59201c4a706e399c388#checks.x86_64-linux.whisrs-dictation-bindings --refresh --no-link`
- Local derivation evaluation of those same four check attrs passed.
- `nix flake show --json --no-write-lock-file` was attempted and failed while
  enumerating `checks.aarch64-darwin` because `whisrs` is unsupported on that
  platform. The focused `x86_64-linux` check attrs relevant to the deployment
  surface were evaluated and built instead.

Interpretation:

- The meaningful check surface now protects against regression to the rejected
  external transcriber production path and checks both Listener and Whisrs
  status/binding adjacency.
- The broad all-system flake enumeration problem is pre-existing or outside
  this Linux deployment slice; it did not block the targeted audit.

## Tracker State

Readback before closure:

- `primary-acmr.4` was closed with CriomOS-home
  `a4adfc961f06cbbc84ebd59201c4a706e399c388` and CriomOS
  `731d999fb1fcc9f78b79e9cd92a0bff033377037`.
- `primary-acmr.5` was open and ready.
- `primary-acmr.6` was blocked by `primary-acmr.5`.

Closure performed:

- `primary-acmr.5` was closed with this report and the audited commit/check
  evidence.
- Post-closure readback of `primary-acmr.6` shows `primary-acmr.3` and
  `primary-acmr.5` as closed dependencies. `primary-acmr.6` can start, subject
  to the safe activation/reload condition above.

## Commands Consulted

- `spirit "(PublicTextSearch [listener transcription status bar])"` returned
  no matching public record.
- `bd show primary-acmr.4 --json` confirmed implementation closure.
- `bd show primary-acmr.5 --json` confirmed audit scope and dependency on
  `primary-acmr.4`.
- `bd show primary-acmr.6 --json` before closure confirmed the smoke test was
  blocked by `primary-acmr.5`; post-closure readback confirmed
  `primary-acmr.5` is now closed in its dependency list.
- `bd ready --parent primary-acmr --explain --plain` showed
  `primary-acmr.5` ready and `primary-acmr.6` blocked by it.
- `jj status --no-pager` in both target repos showed clean working copies with
  the requested commits as parents of the empty working copy.
- `jj show --stat --no-pager -r @-` in both target repos confirmed the commit
  identities and changed files.
- Source reads used `nl -ba`, `sed`, `rg`, and `jq` against the files named in
  this report.
- Quickshell official documentation consulted:
  `https://quickshell.org/docs/v0.2.0/types/Quickshell.Io/Process/`.

## Not Run

- No real spoken microphone-to-clipboard smoke test.
- No live OpenAI transcription request.
- No live Home Manager activation, Lojix deployment, Niri reload, or
  Noctalia restart.
- No Nix store filesystem search.
