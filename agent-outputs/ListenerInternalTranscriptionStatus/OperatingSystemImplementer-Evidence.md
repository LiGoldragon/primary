# CriomOS-home Listener Status-Bar Integration Evidence

## Task And Scope

Tracker item: `primary-acmr.4`.

Implemented the CriomOS-home status-bar integration for Listener's internal
status stream, removed the production stopgap external OpenAI transcription
wrapper, and pinned the deployed Home source through CriomOS. No Listener Rust
source was edited, no secret values were read, no transcript text was read or
recorded, and no real spoken smoke test was run.

Target deployment context for a later safe activation:

- cluster/node/user: `goldragon` / `ouranos` / `li`;
- artifact kind: `UserEnvironment` through CriomOS/CriomOS-home;
- source revision policy: pushed immutable commits;
- builder choice: not submitted in this pass;
- rollback expectation: redeploy the previous CriomOS generation or previous
  CriomOS-home pin;
- activation evidence still required: Lojix current generation/profile state,
  `listener.service` status, Noctalia reload/restart state, and live widget
  observation.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/RustAuditor-ReAudit.md`
- `/home/li/primary/agent-outputs/PrimaryDkrt/OperatingSystemImplementer-Evidence.md`
- `bd show primary-acmr.4 --json`
- CriomOS-home `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `docs/ROADMAP.md`,
  and `skills.md`
- CriomOS `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, and `docs/ROADMAP.md`
- lore `AGENTS.md`
- QuickShell `Process` documentation for `Quickshell.Io` process invocation.

## Repos And Commits

Changed and pushed:

- `/git/github.com/LiGoldragon/CriomOS-home`
  - `a4adfc961f06cbbc84ebd59201c4a706e399c388`
  - commit subject: `CriomOS-home: add Listener status widget`
- `/git/github.com/LiGoldragon/CriomOS`
  - `731d999fb1fcc9f78b79e9cd92a0bff033377037`
  - commit subject: `CriomOS: pin Listener status home profile`

Pinned producer input:

- CriomOS-home `inputs.listener` now resolves to Listener
  `4080f8e89acc173ac124d814147e13dcb971a7a5`, the audited `0.4.0` revision.
- CriomOS `flake.lock` now pins CriomOS-home to
  `a4adfc961f06cbbc84ebd59201c4a706e399c388`.

## Files Changed

CriomOS-home:

- `flake.nix`
- `flake.lock`
- `modules/home/profiles/min/dictation.nix`
- `modules/home/profiles/min/sfwbar.nix`
- `modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml`
- `modules/home/profiles/min/noctalia-plugins/listener-level/manifest.json`
- `checks/listener-dictation-bindings/default.nix`
- `checks/listener-level-widget/default.nix`
- `skills.md`

CriomOS:

- `flake.lock`

## Implementation Summary

Stopgap removal:

- Removed the Nix `listenerOpenAiTranscribe` package that produced
  `listener-openai-transcribe`.
- Removed `listenerOpenAiTranscribe` from `home.packages`.
- Removed the Listener service wrapper export of
  `LISTENER_TRANSCRIPTION_PROGRAM`.
- Updated `listener/environment.example` so production transcription is
  described as Listener-owned internal behavior using runtime gopass access.
- Preserved `LISTENER_CAPTURE_PROGRAM` and `LISTENER_CLIPBOARD_PROGRAM`
  defaults and kept `EnvironmentFile=-%h/.config/listener/environment`.

Status-bar integration:

- Added Noctalia/QuickShell plugin `listener-level`.
- Enabled `plugin:listener-level` adjacent to the existing `plugin:whisrs-level`
  in the Noctalia right bar.
- Managed `listener-level` in `~/.config/noctalia/plugins.json`.
- Installed the Listener plugin manifest and `BarWidget.qml` through
  `xdg.configFile`.
- Added `pkgs.libnotify` to the status-bar profile so `notify-send` is
  available to the widget.

Widget behavior:

- Connects to `$XDG_RUNTIME_DIR/listener/status.sock`.
- Consumes newline JSON with `state` and `level`.
- Keeps transcript text out of the widget and notifications.
- Idle is muted.
- `recording` is red and drives five live level bars from `level`.
- `transcribing` is yellow and animates the bars while Listener works.
- `copied` is green and emits a generic desktop notification:
  `Transcription copied to clipboard`.
- `error` is red and emits a generic desktop notification:
  `Transcription failed`.
- Socket reconnect behavior mirrors the existing Whisrs plugin pattern.

Side-by-side preservation:

- Existing `whisrs-level` plugin remains installed and enabled.
- Existing Whisrs package, service, tray pin, status-bar plugin, and recall path
  remain intact.
- Listener keybinding remains `Mod+Alt+L`.
- Whisrs bindings remain:
  - `Mod+V` -> `whisrs toggle-copy`
  - `Mod+Shift+V` -> `whisrs toggle`
  - `Mod+Alt+V` -> `whisrs-recall`
  - `Mod+Ctrl+V` -> `whisrs cancel`

## Checks Run

In `/git/github.com/LiGoldragon/CriomOS-home` before commit:

- `nix run nixpkgs#nixfmt -- modules/home/profiles/min/dictation.nix modules/home/profiles/min/sfwbar.nix checks/listener-dictation-bindings/default.nix checks/listener-level-widget/default.nix flake.nix` passed, with the existing flake-registry warning.
- `nix build .#checks.x86_64-linux.listener-dictation-bindings --no-link --print-out-paths` passed.
- `nix build .#checks.x86_64-linux.listener-level-widget --no-link --print-out-paths` passed.
- `nix build .#checks.x86_64-linux.whisrs-level-widget --no-link --print-out-paths` passed.
- `nix build .#checks.x86_64-linux.whisrs-dictation-bindings --no-link --print-out-paths` passed.
- `nix flake check --no-build` passed for `x86_64-linux`; it reported only existing unknown-output and incompatible-system warnings.
- `nix eval .#homeConfigurations --apply builtins.attrNames --json` returned `[]`; direct activation-package build was therefore not available from this checkout without Lojix's projected inputs.
- Source grep outside `checks/listener-dictation-bindings/default.nix` found no remaining `LISTENER_TRANSCRIPTION_PROGRAM` or `listener-openai-transcribe`.

From pushed CriomOS-home commit `a4adfc961f06cbbc84ebd59201c4a706e399c388`:

- `nix build github:LiGoldragon/CriomOS-home/a4adfc961f06#checks.x86_64-linux.listener-dictation-bindings --refresh --no-link --print-out-paths` passed.
- `nix build github:LiGoldragon/CriomOS-home/a4adfc961f06#checks.x86_64-linux.listener-level-widget --refresh --no-link --print-out-paths` passed.

In `/git/github.com/LiGoldragon/CriomOS`:

- `nix flake lock --update-input criomos-home` updated only `flake.lock` to the pushed CriomOS-home commit and nested Listener `4080f8e8`.
- `nix flake check --no-build` was attempted and failed at the expected repo boundary: the default `system` input is a throwing stub unless Lojix provides a projected system input. No source evaluation regression was inferred from that direct command.

Version-control checks:

- CriomOS-home `jj status --no-pager` after push: clean.
- CriomOS `jj status --no-pager` after push: clean.

## Deployment And Activation Status

No live Lojix deployment or Home Manager activation was submitted in this pass.
Reason: the change touches Noctalia/Niri-visible status-bar and keybinding
surfaces, and CriomOS-home repo guidance says live Home activations with
compositor/input changes risk the active session. The pushed immutable inputs
are ready for a safe Lojix user-environment or full-host deployment window.

No `niri msg action load-config-file` was run. No real microphone, OpenAI, or
clipboard smoke test was run; that remains assigned to `primary-acmr.6` after
the Nix/UI audit.

## Tracker State

`primary-acmr.4` should be closed with this evidence after the tracker command
succeeds. `primary-acmr.5` is the next audit item.

## Blockers And Follow-Up

No source implementation blocker remains for `primary-acmr.4`.

Follow-up audit scope for `primary-acmr.5`:

- Review CriomOS-home commit `a4adfc961f06cbbc84ebd59201c4a706e399c388`.
- Review CriomOS pin commit `731d999fb1fcc9f78b79e9cd92a0bff033377037`.
- Verify the `listener-level` QML loads in the deployed Noctalia/QuickShell
  version and that `Process` invocation of `notify-send` is accepted.
- Verify `listener/status.sock` reconnection and state transitions against a
  live Listener `0.4.0` daemon without reading transcript text.
- Confirm the check coverage is sufficient for the removed
  `LISTENER_TRANSCRIPTION_PROGRAM` production path and preserved Whisrs
  bindings/plugins.
- Decide whether `listener-level` should be visually distinguished further from
  `whisrs-level` after live observation.
- Keep `primary-acmr.6` as the only real spoken microphone-to-clipboard smoke
  test and do not fold that live paid/API path into the audit.
