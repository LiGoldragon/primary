# Live Wispr and Noctalia verification

## Preactivation preparation

Prepared 2026-09-05 while realization 196 was still `Building`. Realization 196 later terminated as `Failed (Build FlakeReferenceMalformed)`; its replacement activation attempt 197 was superseded by the user's request to deploy the Wispr change without the deferred Codex update. No microphone capture, hands-free control, profile mutation, deployment, build, reboot, or persistent override was performed by this verifier.

The live probe will run only after the integration flow records a successful `ActivateNow` for the newly authorized Wispr only candidate and its activation ID. The pinned runtime package set has a cache available for `ydotool`/`ydotoold`; the current user can access `/dev/uinput` through the `uinput` group. If that cache path and socket start remain available after activation, the probe will use a private temporary `ydotoold` socket and raw key sequence `125:1 45:1 45:0 125:0` (left Super plus X press/release), then repeat it to stop. The daemon and socket will be removed immediately afterward. If this transient path cannot start, the probe will exercise the exact `wispr-flow-status toggle-hands-free` executable named by the active Niri `Mod+X` spawn action and record the key-dispatch limit.

The bounded sequence after activation is:

1. Confirm the active user profile, Wispr process, Noctalia service, v2 status/control sockets, and the generated Niri binding. Read an initial status snapshot without opening capture.
2. Prepare a disposable Ghostty terminal running `cat` as a harmless transcription receiver and focus it through the supported Niri window-focus action. Start a passive newline status reader on the v2 status socket. Record the original default source, select the existing ALSA loopback source, and confirm with `wpctl` that it is the default before invoking any hands-free start. Play a generated `espeak-ng` phrase through its paired loopback sink for more than five seconds, and capture one transient desktop screenshot while the status is `recording`. Invoke the same toggle command to stop, collect the final lifecycle snapshots and receiver output, close the disposable receiver, and restore the original default source only after the capture has stopped.
3. Run a silence pass with the loopback source selected and confirmed as default, with no nonzero playback. Confirm that available microphone samples report `rms: 0` while recording, then stop and restore the original source.
4. Restart the Noctalia user service once, wait for its plugin list/status to return, prepare/focus the same disposable receiver, and repeat one short synthetic start/play/stop pass. Confirm that the status consumer reconnects and the five-bar widget is visible during recording.

The synthetic phrase contains no personal or private speech. Temporary audio, status captures, and screenshots remain under `/tmp` and are removed after observation. No transcript or credentials will be recorded.

## Live observations

Pending successful activation and execution of the sequence above.

## Limits

- Until the new Wispr only activation ID and terminal success are recorded, all live observations remain unwitnessed.
- A cache-only ydotool check found ydotoold and uinput access, but no key event will be sent until activation succeeds. If the postactivation daemon/socket probe fails, the exact command target is still exercised and the physical Meta+X dispatch limit is recorded.
- The v2 status contract exposes lifecycle and scalar microphone state, not transcript text. Response to the synthetic phrase will therefore be judged from control replies, recording/transcribing/idle lifecycle, and the visible runtime state; no private speech is needed.
