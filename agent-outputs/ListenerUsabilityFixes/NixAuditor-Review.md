# CriomOS-home Listener Usability Nix Audit

## Result

Pass for tracker item `primary-zddv.6`.

No blocking Nix, shortcut, wrapper, widget, pin, Whisrs-preservation, or check-coverage findings were found in the audited CriomOS-home commit:

- `/git/github.com/LiGoldragon/CriomOS-home` `406417507d6b767edb69b1dbc9cff098736d11ce`

`primary-zddv.7` can start if activation uses the pushed remote `406417507d6b` revision or a later audited successor. `primary-zddv.8` can start only after `primary-zddv.7` activates and reloads the user surfaces named below.

## Findings

None.

## Residual Risks And Operator Actions

- The local CriomOS-home working copy was not checked out at the audited tree: `jj status` showed the working copy parent at `e42ca632`, while `jj bookmark list --all-remotes` showed `main` and `main@origin` at `406417507d6b`. This is not a code defect, but activation must not deploy from the stale local working-copy parent. Use the pushed remote revision `406417507d6b` or first update the checkout to that bookmark.
- This audit did not run live activation or smoke tests by instruction. The activation worker should record the exact home source revision/generation, then run `systemctl --user daemon-reload`, restart `listener.service`, reload Niri config, and restart or reload Noctalia/QuickShell so the updated QML plugin is loaded.
- The live smoke item should still observe Listener status cadence and cancel behavior without exposing transcript text, clipboard contents, audio contents, or secrets.

## Scope And Context

Required evidence read:

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/OperatingSystemImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerCancelSemantics/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerLiveLevelResponsiveness/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/RustAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/TrackerWeaver-WorkGraph.md`
- `bd show primary-zddv.6 --json`

Intent query:

- `spirit "(PublicTextSearch [Listener shortcut cancel widget CriomOS home])"` returned no matching public record, so the tracker brief and repo/evidence surfaces were used as authority.

Source inspection used explicit commit reads with `jj file show -r 406417507d6b ...` because the working copy parent differed from the audited remote bookmark.

## Shortcut And Wrapper Audit

The Listener toggle binding moved away from the lock family:

- At commit `406417507d6b`, `modules/home/profiles/min/dictation.nix:353` defines `binds."Mod+Alt+M"` for Listener capture.
- `modules/home/profiles/min/dictation.nix:354` runs `listener-toggle-capture` with the `toggle` argument.
- `checks/listener-dictation-bindings/default.nix:74-84` asserts `Mod+Alt+M`, `Mod+Ctrl+Alt+M`, and absence of `Mod+Alt+L`.

The Listener cancel binding and wrapper reach typed cancel:

- `modules/home/profiles/min/dictation.nix:123-134` defines `listener-cancel-capture`, reads active Listener status, extracts only the active numeric session, exits `0` when no active capture is visible, and runs `listener cancel "$session"`.
- `modules/home/profiles/min/dictation.nix:69-88` accepts only the `(StatusReported (Capturing (...` status shape and rejects empty or non-numeric sessions.
- `modules/home/profiles/min/dictation.nix:359-360` binds `Mod+Ctrl+Alt+M` to `listener-cancel-capture cancel`.
- `checks/listener-dictation-bindings/default.nix:50-54` identifies the cancel wrapper command shape.
- `checks/listener-dictation-bindings/default.nix:112-132` syntax-checks the wrapper, requires `/bin/listener cancel "$session"`, and rejects stop/transcribe/OpenAI/clipboard paths from the cancel wrapper.

The idle and malformed-status behavior is safe for deployment: when the status string is absent, idle, or malformed, the cancel wrapper exits without starting Listener and without reaching stop/transcribe/copy behavior. The only fragile surface is textual CLI status parsing, but the parser is constrained to the active typed status projection and is covered by the Nix check.

## Whisrs Preservation Audit

Whisrs bindings remain intact:

- `modules/home/profiles/min/dictation.nix:329-350` keeps `Mod+V`, `Mod+Shift+V`, `Mod+Alt+V`, and `Mod+Ctrl+V` mapped to the existing Whisrs commands.
- `checks/listener-dictation-bindings/default.nix:66-72` and `checks/whisrs-dictation-bindings/default.nix:47-58` assert those bindings.

The Whisrs Noctalia plugin remains intact and side by side:

- `modules/home/profiles/min/sfwbar.nix:46-47` lists `plugin:listener-level` followed by `plugin:whisrs-level`.
- `modules/home/profiles/min/sfwbar.nix:73-80` keeps both Noctalia plugin states enabled.
- `modules/home/profiles/min/sfwbar.nix:91-98` installs both Listener and Whisrs plugin QML files.
- `checks/listener-level-widget/default.nix:12-16` asserts Listener plugin registration, libnotify availability, and Whisrs plugin presence.

## Pin And Service Wrapper Audit

The Listener input pin is coherent:

- `flake.lock:1077-1093` pins `listener` to `ea47f0b2fb3fcb4e9f77f693269b8bd66f9f2907`.
- `listener` `Cargo.toml:1-4` at `ea47f0b2fb3f` declares version `0.5.1`.
- `listener` `Cargo.lock:1197-1200` at `ea47f0b2fb3f` pins `signal-listener` `0.4.0` to `9fce56075ed93381bfe897444f6207c9dd3f73ab`.
- `signal-listener` `Cargo.toml:1-4` at `9fce5607` declares version `0.4.0`.
- `signal-listener` `schema/lib.schema:7-18`, `45-48`, and `89-95` at `9fce5607` expose the typed cancel input, cancelled output, and `OperationKind Cancel`.

The Listener service wrapper does not reintroduce the rejected transcription stopgap:

- `modules/home/profiles/min/dictation.nix:60-66` exports capture and clipboard programs and execs `listener-daemon`.
- `modules/home/profiles/min/dictation.nix:172-177` keeps the local environment example limited to capture and clipboard overrides.
- `checks/listener-dictation-bindings/default.nix:96-129` asserts the environment example lacks `LISTENER_TRANSCRIPTION_PROGRAM`, the service wrapper does not export `LISTENER_TRANSCRIPTION_PROGRAM`, the wrapper does not reference `listener-openai-transcribe`, and the service wrapper does not invoke Whisrs.

## Widget Audit

The Listener Noctalia widget supports the new cancelled state:

- `modules/home/profiles/min/noctalia-plugins/listener-level/BarWidget.qml:25-29` defines recording, transcribing, cancelled, active, and amplified microphone-level state.
- `BarWidget.qml:31-39` gives `cancelled` its own color.
- `BarWidget.qml:50-56` sends generic state notifications only, including `Capture cancelled`; no transcript content is read or rendered.
- `BarWidget.qml:160-170` displays `cancelled` as a terminal state like copied/error.

The quiet-level legibility change is reasonable and does not mask runtime stalls:

- `BarWidget.qml:29` applies a bounded `2.75` visual gain.
- `BarWidget.qml:61-66` updates visible level on recording frames and resets it outside recording.
- `BarWidget.qml:133-147` decays every `70` ms and switches to faster decay after `450` ms without level events, so short jitter is smoothed while multi-second producer stalls still visibly fall away.
- `checks/listener-level-widget/default.nix:23-35` asserts cancelled state support, level parsing, visual gain, visible-level smoothing, stall-age decay, and generic notification strings.
- `checks/listener-level-widget/default.nix:37-40` rejects transcript/text-shaped widget content.

## Checks Run

Passed against the pushed remote revision `github:LiGoldragon/CriomOS-home/406417507d6b767edb69b1dbc9cff098736d11ce`:

- `nix flake metadata --json ... | jq -r '.locks.nodes.listener.locked.rev'` returned `ea47f0b2fb3fcb4e9f77f693269b8bd66f9f2907`.
- `nix eval --raw --expr '(builtins.getFlake "...").inputs.listener.packages.x86_64-linux.default.version'` returned `0.5.1`.
- `nix eval --raw ...#checks.x86_64-linux.listener-dictation-bindings.drvPath` passed.
- `nix eval --raw ...#checks.x86_64-linux.listener-level-widget.drvPath` passed.
- `nix build ...#checks.x86_64-linux.listener-dictation-bindings ...#checks.x86_64-linux.listener-level-widget ...#checks.x86_64-linux.whisrs-dictation-bindings ...#checks.x86_64-linux.whisrs-level-widget --no-link --print-build-logs` passed.
- `nix flake check --no-build --print-build-logs ...` passed. It emitted only known unknown-output warnings and a formatter deprecation warning; all checks evaluated.

Not run:

- Live activation or live smoke tests, by instruction.
- Full `nix flake check` with builds. The focused check builds plus full no-build evaluation were sufficient for the Nix/UI audit surface and avoid running unrelated heavy checks.

## Tracker And Closeout

Recommended tracker action: close `primary-zddv.6` as passed with this report path after committing the report. This unblocks `primary-zddv.7`; `primary-zddv.8` remains blocked until activation is complete.
