# Live Wispr and Noctalia verification

## Preactivation preparation

Prepared 2026-09-05 while realization 196 was still `Building`. Realization 196 later terminated as `Failed (Build FlakeReferenceMalformed)`; its replacement activation attempt 197 was superseded by the user's request to deploy the Wispr change without the deferred Codex update. No microphone capture or hands-free control was attempted before the authorized Wispr-only activation 198. No profile mutation, deployment, build, reboot, or persistent override was performed by this verifier.

The pinned runtime package set has a cache available for `ydotool`/`ydotoold`; the current user can access `/dev/uinput` through the `uinput` group. The probe used a private temporary `ydotoold` socket and raw key sequence `125:1 45:1 45:0 125:0` (left Super plus X press/release). The daemon and socket were removed afterward. The exact `wispr-flow-status toggle-hands-free` target named by the active Niri `Mod+X` binding was also tried directly when the keyed stop did not settle promptly.

The bounded sequence after activation is:

1. Confirm the active user profile, Wispr process, Noctalia service, v2 status/control sockets, and the generated Niri binding. Read an initial status snapshot without opening capture.
2. Prepare a disposable Ghostty terminal running `cat` as a harmless transcription receiver and focus it through the supported Niri window-focus action. Start a passive newline status reader on the v2 status socket. Record the original default source, select the existing ALSA loopback source, and confirm with `wpctl` that it is the default before invoking any hands-free start. Play a generated `espeak-ng` phrase through its paired loopback sink for more than five seconds, and capture one transient desktop screenshot while the status is `recording`. Invoke the same toggle command to stop, collect the final lifecycle snapshots and receiver output, close the disposable receiver, and restore the original default source only after the capture has stopped.
3. Run a silence pass with the loopback source selected and confirmed as default, with no nonzero playback. Confirm that available microphone samples report `rms: 0` while recording, then stop and restore the original source.
4. Restart the Noctalia user service once, wait for its plugin list/status to return, prepare/focus the same disposable receiver, and repeat one short synthetic start/play/stop pass. Confirm that the status consumer reconnects and the five-bar widget is visible during recording.

The synthetic phrase contains no personal or private speech. Temporary audio, status captures, and screenshots remain under `/tmp` and are removed after observation. No transcript or credentials will be recorded.

## Live observations

Activation 198 was recorded as `Completed / Succeeded` at operation 5172. Restarting the existing `wispr-flow-first-run.service` made the v2 status and control sockets appear; the unit remained active. The generated Niri configuration was reloaded through `niri msg action load-config-file`, and its `Mod+X` binding pointed at the v2 toggle target.

The single disposable Ghostty receiver was focused before capture. Its first launch used an invalid separate `--title` argument and produced an owned Configuration Errors window; that window disappeared and the receiver itself remained as a `cat` process writing only to a temporary file. No transcript bytes were received. No second receiver was opened.

Noctalia reconnect succeeded through one restart of `noctalia-refresh.service`: the unit returned active, `criomos/wispr-status` loaded, and `wispr-status-service` started. A fresh desktop screenshot showed the existing idle `criomos/listener-level` five-dot indicator; the loaded Wispr BarWidget itself was not given a moving-level witness because capture remained unavailable. During the keyed probe the meter did not provide speech-driven movement; the user also observed the red recording icon persisting without moving waves.

With source `75` (the existing ALSA loopback) visibly confirmed as default before the keyed start, the transient ydotool daemon sent the actual Mod+X press/release sequence. The key path reached `state: recording` and later `transcribing` then `idle`, but `hands_free` stayed `false`; the stop key did not settle to idle within the bounded wait. The direct toggle target returned `control_result {ok:false,error:"unavailable"}`. The synthetic `espeak-ng` phrase measured 26.010204 seconds and was played to loopback sink `74` for more than five seconds. Every observed microphone sample remained `capture: unavailable, rms: null`; there was no PipeWire input stream and the receiver file stayed at 0 bytes. This does not verify truthful audio capture, non-private input response, or a moving five-bar level.

Read-only inspection of the active `.9` `app.asar` found the meter bootstrap order intact: the main process creates the v2 bridge and installs `ipcMain.on("wispr-flow-status-meter-v2", ...)` inside `app.whenReady`, while the renderer's recorder worklet emits only after its `AudioWorkletNode` is connected. The packaged renderer hub contains the v2 message callback and forwards valid capture/RMS values to that listener. There is no separate Linux recorder fallback in this path: worklet load retries three times, then recording aborts if the graph is absent. The distinct static defect is the hands-free hook: `setToggleHandsFree(...)` appears before `app.whenReady` creates the lazy bridge and is guarded by optional chaining, so no action is registered; this matches the live `control_result {ok:false,error:"unavailable"}`.

The intended silence pass was not run after the capture path reported unavailable. Source `152`, whose hardware label is `Wireless Microphone RX Analog Stereo`, is the final default, v2 status is idle, the scratch receiver and transient ydotool daemon are gone, and the temporary probe directory was removed. The final focused window was the pre-existing Claude window; no owned receiver or Configuration Errors window remains.

## Limits

- Activation 198 and terminal success are witnessed, but the live hands-free toggle and five-bar microphone meter are **failed / not verified**: `hands_free` never became true, control returned `unavailable`, and microphone samples stayed unavailable with `rms: null`.
- The ydotool path proved that a real Mod+X sequence can reach the recording lifecycle after the Niri config reload, but it did not prove the declared hands-free semantics or a reliable stop. The direct command target likewise returned an unavailable control result.
- The 26-second phrase was synthetic and routed only to ALSA loopback sink `74`; no personal speech was used. The receiver captured zero bytes, and no transcript text or credentials were retained.
- The status reader reported `recording` when the bounded script performed source restoration, although the microphone field was unavailable and no PipeWire input stream existed; therefore the required stop-before-restore ordering is not fully witnessed. Final state is idle with source `152` restored.
- Silence-zero (`rms: 0`) was not witnessed, and recording-time reconnect behavior was not witnessed. Noctalia reconnect was witnessed only at idle/plugin-service level, with the idle five-dot screenshot.
