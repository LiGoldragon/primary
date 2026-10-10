# CriomOS-home Listener Shortcut And Widget Evidence

## Task And Scope

Tracker item: `primary-zddv.4`.

Implemented the CriomOS-home side of the Listener usability fix: package pin,
safer Listener shortcut, Listener cancel shortcut, cancel wrapper, Noctalia
widget support for the `cancelled` state, and focused checks. This run did not
run live activation, did not run a paid transcription/API path, did not inspect
clipboard contents, did not read transcript text, and did not read audio
contents.

## Context Consulted

Required evidence:

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerCancelSemantics/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerLiveLevelResponsiveness/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/OperatingSystemImplementer-LiveActivationEvidence.md`
- `bd show primary-zddv.4 --json`

Repository and doctrine context:

- CriomOS-home `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `docs/ROADMAP.md`, and dictation section of `skills.md`
- CriomOS `AGENTS.md`
- lore `AGENTS.md`
- operating-system, Nix, edit-coordination, work-tracking, testing, version-control, and repository-closeout doctrine

Coordination:

- `orchestrate "(Observe Roles)"` showed `/git/github.com/LiGoldragon/CriomOS-home` was already claimed by `system-operator` for emergency Colemak recovery.
- This implementation used isolated JJ workspace `/git/github.com/LiGoldragon/CriomOS-home-listener-zddv4`, claimed by `system-maintainer`.
- Worktree tracking bead: `primary-gm89`.

The local CriomOS-home worktree `.beads` database was absent in the isolated
workspace, so the supplied primary tracker item was used.

## Changed Repo And Commit

Changed and pushed:

- `/git/github.com/LiGoldragon/CriomOS-home`
- commit `406417507d6b`: `CriomOS-home: wire Listener cancel shortcut`

No CriomOS pin commit was made. This task did not perform live deployment, and
the later activation item can deploy the exact pushed CriomOS-home revision
directly. Reboot-persistence work remains a deployment/planning concern for the
activation path.

## Files Changed

- `flake.lock`
- `modules/home/profiles/min/dictation.nix`
- `modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml`
- `checks/listener-dictation-bindings/default.nix`
- `checks/listener-level-widget/default.nix`
- `skills.md`

## Behavior Implemented

Pin:

- CriomOS-home now pins Listener to `ea47f0b2fb3fcb4e9f77f693269b8bd66f9f2907`.
- The pinned Listener package evaluates and builds as version `0.5.1`.
- The built Listener closure uses `signal-listener` `0.4.0` at revision `9fce5607`.

Bindings:

- Listener toggle moved from `Mod+Alt+L` to `Mod+Alt+M`.
- Listener cancel added at `Mod+Ctrl+Alt+M`.
- Whisrs bindings remain side by side:
  - `Mod+V` -> `whisrs toggle-copy`
  - `Mod+Shift+V` -> `whisrs toggle`
  - `Mod+Alt+V` -> `whisrs-recall`
  - `Mod+Ctrl+V` -> `whisrs cancel`

Cancel wrapper:

- Added Nix-managed `listener-cancel-capture`.
- The wrapper reads `listener status`, accepts only the typed active-capture
  status shape, extracts only a numeric active session, and calls
  `listener cancel "$session"`.
- The cancel wrapper does not call `listener stop`, does not call any
  transcription command, does not reference the rejected external transcription
  stopgap, and does not reference clipboard delivery.
- If no active capture is visible, the wrapper exits without starting Listener
  or invoking stop/transcribe/copy paths.

Widget:

- Listener Noctalia widget now supports `listenerState === "cancelled"`.
- Cancelled state gets a UI-safe notification body: `Capture cancelled`.
- Notifications still contain no transcript text.
- Recording level display now applies a modest `2.75` visual gain into a
  `visibleMicrophoneLevel` value.
- The visual level decays on a 70 ms timer and fades faster once no level event
  has arrived for more than 450 ms, so quiet real mic movement is easier to see
  without hiding multi-second runtime stalls.

Repository note:

- `skills.md` now documents the current Listener `Mod+Alt+M` and
  `Mod+Ctrl+Alt+M` bindings.

## Checks Run

Passed:

- `nix eval --raw --impure --expr '(builtins.getFlake "path:/git/github.com/LiGoldragon/CriomOS-home-listener-zddv4").inputs.listener.packages.x86_64-linux.default.version'`
  returned `0.5.1`.
- `nix eval .#checks.x86_64-linux.listener-dictation-bindings.drvPath --raw`
  passed.
- `nix eval .#checks.x86_64-linux.listener-level-widget.drvPath --raw`
  passed.
- `nix run .#formatter -- --check checks/listener-dictation-bindings/default.nix checks/listener-level-widget/default.nix modules/home/profiles/min/dictation.nix`
  passed.
- `nix build .#checks.x86_64-linux.listener-dictation-bindings .#checks.x86_64-linux.listener-level-widget .#checks.x86_64-linux.whisrs-dictation-bindings .#checks.x86_64-linux.whisrs-level-widget --no-link --print-build-logs`
  passed.
- `nix flake check --no-build --print-build-logs` passed.
- Static searches verified no Listener `Mod+Alt+L` binding remains under the
  touched binding/check surfaces.

Formatter note:

- Plain `nix fmt` returned a formatter invocation error with an empty-input
  parse message. The direct formatter check over the changed Nix files passed.

## Tracker Impact

- `primary-zddv.4` is ready to close with CriomOS-home commit
  `406417507d6b` and this evidence file.
- `primary-gm89` can close as the isolated worktree was fully pushed to
  `main`.
- `primary-zddv.6` is unblocked for audit.

## Activation Requirements

Later activation/smoke work should use the exact pushed CriomOS-home revision
`406417507d6b` or a later audited successor. For live desktop refresh, activation
should account for:

- Home deployment through the current deployed Lojix `Home` request shape unless
  Lojix itself has been upgraded.
- `systemctl --user daemon-reload`
- `systemctl --user restart listener.service`
- `niri msg action load-config-file`
- Noctalia/QuickShell restart or reload so the updated plugin QML is loaded.

Rollback path: use the previous Lojix Home generation or previous pushed
CriomOS-home revision. This task did not activate a generation.

## Recommended Audit Scope For `primary-zddv.6`

Audit should verify:

- `flake.lock` pins Listener `ea47f0b2fb3f` and the built closure uses
  `signal-listener` `9fce5607` / `0.4.0`.
- `Mod+Alt+M` is the only Listener toggle binding and `Mod+Alt+L` is absent for
  Listener.
- `Mod+Ctrl+Alt+M` targets `listener-cancel-capture`.
- `listener-cancel-capture` only obtains a numeric active session from the
  active-capture status and calls typed `listener cancel <session>`.
- The cancel wrapper cannot reach stop/transcribe/OpenAI/clipboard paths.
- Whisrs bindings and `whisrs-level` plugin remain intact.
- The Listener widget handles `cancelled`, does not carry transcript text, and
  the visual-gain/decay rule makes quiet levels legible without masking stalled
  status frames.
- The focused checks cover these invariants and the activation item owns live
  tap/cancel observation.

## Blockers And Unknowns

No implementation blocker remains for `primary-zddv.4`.

Live activation, mic-tap observation, cancel observation, and normal
record/transcribe/copy smoke remain intentionally out of scope for this task and
belong to later audited activation/smoke items.
