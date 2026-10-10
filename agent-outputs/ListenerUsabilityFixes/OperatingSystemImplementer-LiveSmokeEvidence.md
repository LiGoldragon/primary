# Listener Usability Live Smoke Evidence

## Task And Scope

Tracker item: `primary-zddv.8`.

Scope: live smoke test the activated Listener usability fixes on `goldragon` /
`ouranos` for user `li`, without exposing private content. The test covered
mic-level status cadence, typed cancel behavior, shortcut preservation, and
Whisrs side-by-side state. The normal transcription path was not run because no
operator-provided non-private spoken phrase and clipboard/visual observation
were available in this session.

No transcript text, clipboard contents, audio contents, OpenAI key, secret-store
output, or raw Nix store paths are recorded here. The retained capture artifact
was not read or deleted.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/OperatingSystemImplementer-ActivationEvidence.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/NixAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/RustAuditor-Review.md`
- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/ListenerLiveLevelResponsiveness/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerCancelSemantics/GeneralCodeImplementer-Evidence.md`
- `bd show primary-zddv.8 --json`
- `bd show primary-acmr.6 --json`
- `bd show primary-jwx0 --json`
- `bd show primary-c8w0 --json`
- `lojix "(Query (ByNode (goldragon ouranos None)))"` with paths redacted
- Active user service, Niri, Noctalia, Listener wrapper, status socket, and
  microphone source state

## Result

Blocked for full `primary-zddv.8` closure because the normal spoken
microphone-to-clipboard path was not run. Required remaining condition: an
operator must provide or speak a non-private test phrase and allow observation
of the Listener visual states and clipboard success without transcript
disclosure.

Passed live observations:

- Listener mic-level status cadence is responsive. During live capture, level
  frames flowed roughly every 50 to 101 ms with changing nonzero levels. The
  prior 2.5 second burst stall was not observed.
- Listener cancel used the deployed typed cancel wrapper, stopped capture,
  retained the `.listenerlog` artifact, emitted `cancelled`, returned to idle,
  and did not show transcribing/copied status.
- No clipboard-change event occurred after Listener start or cancel during the
  monitored window. The only clipboard watcher event occurred before Listener
  start and is interpreted as watcher initialization.
- Active shortcut state matches the deployed design: Listener capture is
  `Mod+Alt+M`, Listener cancel is `Mod+Ctrl+Alt+M`, no Listener `Mod+Alt+L`
  binding was found, and Whisrs bindings remain present.
- Whisrs remained active and idle.

Not observed:

- Direct visible widget movement was not visually confirmed by a human observer
  in this run. Status socket cadence is the objective evidence for level flow.
- Normal transcription and clipboard delivery were not tested because no
  non-private operator-spoken phrase was provided.

## Live Identity

Observed facts:

- Host/user/runtime: `ouranos`, `li`, `XDG_RUNTIME_DIR=/run/user/1001`.
- Lojix query after the smoke still included deployment `36` as
  `goldragon ouranos HomeOnly Switch Current`.
- `listener` and `listener-daemon` resolve to package version `listener-0.5.1`.
- `listener.service` and `whisrs.service` were active before and after the
  smoke.
- `listener status` was idle before the smoke and idle after cancel.
- `$XDG_RUNTIME_DIR/listener/status.sock` existed.
- Default microphone source was present, running, and not muted.

Commands:

```sh
lojix "(Query (ByNode (goldragon ouranos None)))"
systemctl --user show listener.service whisrs.service --property=Id,ActiveState,SubState,ExecMainPID,ExecStart,FragmentPath,EnvironmentFiles,LoadState --no-pager
listener status
whisrs status
pactl get-default-source
pactl list sources
```

## Mic-Level Cadence

Action sequence:

```sh
listener-toggle-capture toggle
listener status
listener-cancel-capture cancel
```

The status socket was observed with timestamps while the wrapper-controlled
capture was running.

Representative observed frames:

```text
1783003156.347 {"state":"idle","level":0.0}
1783003156.582 ACTION_START listener-toggle-capture toggle
1783003156.598 {"state":"recording","level":0.0}
1783003156.674 {"state":"recording","level":0.0681689}
1783003156.751 {"state":"recording","level":0.062684804}
1783003156.825 {"state":"recording","level":0.066112876}
1783003157.301 {"state":"recording","level":0.06409385}
1783003158.331 {"state":"recording","level":0.06536879}
1783003159.434 {"state":"recording","level":0.07110383}
1783003160.313 {"state":"recording","level":0.06666829}
1783003160.360 ACTION_CANCEL listener-cancel-capture cancel
1783003160.389 {"state":"cancelled","level":0.0}
1783003161.289 {"state":"idle","level":0.0}
```

Observed interpretation:

- First nonzero recording level arrived about 76 ms after the recording state.
- During the recording window, frames continued at approximately 50 to 101 ms
  spacing with changing nonzero values.
- No multi-second gap or burst delivery like the scout's Listener 0.4.0
  observation appeared.

## Cancel Behavior

Observed command results:

```text
(Started 8)
(Cancelled (8 /home/li/.local/state/listener/captures/capture-8.listenerlog))
```

Artifact metadata:

```text
Before cancel: capture-8.listenerlog existed, 18608 bytes.
After cancel:  capture-8.listenerlog existed, 99248 bytes.
```

The artifact path was:

```text
/home/li/.local/state/listener/captures/capture-8.listenerlog
```

No artifact contents were read and the artifact was not deleted.

Status evidence:

- `listener status` before start: `(StatusReported Idle)`.
- `listener status` during capture:
  `(StatusReported (Capturing (8 /home/li/.local/state/listener/captures/capture-8.listenerlog)))`.
- Status socket emitted `cancelled` immediately after the cancel action.
- `listener status` after cancel: `(StatusReported Idle)`.
- `listener status` final: `(StatusReported Idle)`.
- User journal for `listener.service` had no entries in the smoke window.

No-spend/no-clipboard evidence:

- Cancel wrapper syntax check passed.
- Focused wrapper search found the deployed wrapper execs
  `listener cancel "$session"`.
- Focused wrapper search found no `listener stop`, no transcription command, no
  OpenAI transcriber reference, no Whisrs reference, and no clipboard command.
- Status socket did not emit `transcribing` or `copied` during cancel.
- A clipboard watcher ran from before Listener start until after Listener cancel.
  It emitted one event at `1783003156.333`, before the Listener start action at
  `1783003156.582`, and emitted no event after start or cancel.
- Clipboard offered MIME types before and after were the same class of text
  types. Clipboard contents were not read.

## Shortcut And Whisrs Preservation

Active Niri config facts:

- `Mod+Alt+M` has title `Listener Capture` and spawns
  `listener-toggle-capture toggle`.
- `Mod+Ctrl+Alt+M` has title `Listener Cancel` and spawns
  `listener-cancel-capture cancel`.
- Focused search found no active Listener `Mod+Alt+L` binding.
- Whisrs bindings remain active:
  - `Mod+V` -> `whisrs toggle-copy`
  - `Mod+Shift+V` -> `whisrs toggle`
  - `Mod+Alt+V` -> `whisrs-recall`
  - `Mod+Ctrl+V` -> `whisrs cancel`

Checks:

```sh
rg -n 'Mod\+Alt\+M|Mod\+Ctrl\+Alt\+M|Mod\+Alt\+L|Mod\+V|Mod\+Shift\+V|Mod\+Alt\+V|Mod\+Ctrl\+V|listener-toggle-capture|listener-cancel-capture|whisrs' /home/li/.config/niri/config.kdl
niri validate
whisrs status
```

Observed results:

- `niri validate` reported the active config as valid.
- `whisrs status` was `idle` before and after the Listener smoke.
- Noctalia settings still place `listener-level` adjacent to `whisrs-level`.
- Listener Noctalia plugin still contains `cancelled`, `Capture cancelled`, and
  `visibleMicrophoneLevel` handling.

## Normal Transcription Path

Not run.

Reason: the task authorizes a real microphone-to-clipboard test only when the
operator provides or speaks a non-private phrase and observation is available.
No such phrase or visual/clipboard observation channel was available during
this run. Synthetic audio was not used and no success was simulated.

Remaining condition: an operator should speak a non-private test phrase while
Listener is started through `Mod+Alt+M` or `listener-toggle-capture toggle`,
then allow observation of recording, transcribing, clipboard delivery, and final
idle/copy status without recording transcript text in chat or reports.

## Tracker Impact

- `primary-zddv.8`: should remain open/blocked. Mic-level, cancel, shortcut,
  and Whisrs-preservation checks passed; normal spoken transcription remains
  unrun for lack of an operator-provided non-private phrase and observation.
- `primary-acmr.6`: cannot advance yet. It still requires the real
  operator-spoken microphone-to-clipboard smoke evidence.
- `primary-jwx0`: cannot advance yet for the same reason.
- `primary-c8w0`: cannot advance because `primary-jwx0` remains blocked.

## Checks Run

Passed:

- `bd show primary-zddv.8 --json`
- `bd show primary-acmr.6 --json`
- `bd show primary-jwx0 --json`
- `bd show primary-c8w0 --json`
- `lojix "(Query (ByNode (goldragon ouranos None)))"` with output path
  redaction for report use
- `systemctl --user show listener.service whisrs.service ...`
- `listener status`
- `whisrs status`
- `test -S "$XDG_RUNTIME_DIR/listener/status.sock"`
- `pactl get-default-source`
- `pactl list sources`
- live status socket observation during capture and cancel
- `listener-toggle-capture toggle`
- `listener-cancel-capture cancel`
- retained artifact `stat` checks
- clipboard-change watcher with no content reads
- active Niri binding search
- `niri validate`
- Noctalia plugin/config focused search
- `bash -n "$(command -v listener-cancel-capture)"`
- focused cancel-wrapper grep for typed cancel and absence of stop/transcribe,
  OpenAI, Whisrs, and clipboard references
- `journalctl --user -u listener.service --since '2026-07-02 16:39:00' --until '2026-07-02 16:39:30' --no-pager`

Not run:

- Direct widget visual confirmation: no human visual observer was available.
- Normal spoken microphone-to-clipboard transcription: no operator-provided
  non-private phrase and observation channel was available.

## Blockers And Follow-Up

Blocker: normal transcription path remains unproven after the usability-fix
activation because no operator-spoken non-private phrase was available. This
blocks `primary-zddv.8`, `primary-acmr.6`, `primary-jwx0`, and therefore
`primary-c8w0`.

No blocker remains for Listener mic-level responsiveness, typed cancel,
artifact retention, shortcut state, or Whisrs preservation based on this smoke
run.
