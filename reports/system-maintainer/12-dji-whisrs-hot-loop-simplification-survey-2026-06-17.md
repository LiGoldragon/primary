# DJI / Whisrs hot-loop simplification survey — 2026-06-17

## Frame

The immediate user symptom is that dictation stays bound to the DJI hot virtual source when the DJI mic is not usable. The user explicitly asked not to let this turn into a larger pile of mic-specific code, and to survey the current state before changing more.

Spirit capture: `1vj5` records the durable constraint that the CriomOS-home dictation microphone path should prefer reducing or deleting brittle DJI/PipeWire policy over adding more keepalive code.

No code changed in this pass. The new intent was manifested into `/git/github.com/LiGoldragon/CriomOS-home/INTENT.md` under Dictation.

## Current live state

- `whisrs.service` is active and idle.
- The process environment contains `PIPEWIRE_NODE`, so Whisrs is not simply following the current PipeWire/Pulse default source.
- The current default source is `dji_mic_hot_sink.monitor`.
- The DJI Bluetooth source and the hot virtual source both had measurable signal during the survey, while one laptop internal mic source also had signal.
- Whisrs logs show prior silent recordings, including a skipped transcription for a silent recording on 2026-06-17.

The live graph can work when the DJI source is alive. The failure mode is that the graph is always present and Whisrs is hard-bound to it, so absence or silence of the real DJI source becomes silence for dictation instead of allowing fallback.

## Current declared shape

Main file: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`.

DJI-specific footprint in that file:

- `whisrsServe` resolves `dji_mic_hot_sink.monitor` by PipeWire object serial and exports `PIPEWIRE_NODE` before starting `whisrsd`.
- A PipeWire fragment creates `dji_mic_hot_sink` and a loopback from the DJI Bluetooth input to that sink.
- A WirePlumber fragment pins the DJI BlueZ card and matching nodes into HFP/MSBC and disables idle suspension for those nodes.
- The WirePlumber setting `bluetooth.autoswitch-to-headset-profile = false` is global, even though the DJI card rules themselves are MAC-specific.

Approximate nonblank footprint:

- Whisrs hard binding: 15 lines.
- PipeWire hot sink and loopback: 37 lines.
- WirePlumber DJI policy: 41 lines.
- Check file `/git/github.com/LiGoldragon/CriomOS-home/checks/dji-keepalive/default.nix`: 100 nonblank lines.

The check currently locks the system into the DJI-specific architecture: it asserts the PipeWire loopback, WirePlumber fragment, and `PIPEWIRE_NODE` serial binding exist. A simplification must change the check, or the check will force the brittle shape back in.

## Diagnosis

The current design made the DJI mic a mandatory dictation substrate. That is too strong for a removable Bluetooth accessory.

The original goal was legitimate: avoid losing the first seconds of speech while Bluetooth HFP wakes or profile-churns. But the current implementation solves that by making a virtual always-on mic the source of truth. That creates these consequences:

1. If the real DJI source is absent, muted, or silently wedged, the virtual source still exists and Whisrs records silence.
2. System default-source changes do not reliably fix Whisrs because the daemon wrapper exports `PIPEWIRE_NODE` directly.
3. The hot virtual node can survive device churn and become misleading; earlier live recovery found a stale loopback feeding the hot sink from its own monitor after reconnect.
4. The check suite now protects the workaround rather than the user outcome.

This is not yet an unmanageable pile of code, but it is pointed in that direction: every new symptom invites another graph repair, reconnect hook, fallback probe, or Bluetooth rule unless the dependency is weakened.

## Recommended subtractive path

First pass should delete the hard dependency rather than add a watcher.

Recommended operator change:

1. Remove the `PIPEWIRE_NODE` serial-resolution block from `whisrsServe`.
2. Let Whisrs use its configured/default input path again.
3. Remove the always-created `dji_mic_hot_sink` and DJI loopback unless the wake-delay problem is re-proven as worse than the fallback failure.
4. Remove or rewrite `checks/dji-keepalive/default.nix` so it protects the simpler contract: Whisrs must not be hard-bound to a removable accessory; dictation keybindings and service startup remain valid.
5. Keep only the ordinary Whisrs service, keybindings, history/privacy setup, and status UI as the stable core.

Expected deletion: roughly 90 lines from `dictation.nix` plus most or all of the 100-line DJI keepalive check.

## If DJI fast-start remains important

If the first-seconds-loss problem is still important after the subtractive pass, add the smallest explicit mechanism rather than restoring ambient always-on capture:

- Prefer a user-visible source choice: ordinary dictation follows the system default; DJI dictation is a separate explicit mode or command.
- If automatic fallback is required, put it behind one small source-selection boundary, not in scattered PipeWire, WirePlumber, systemd, and check glue.
- Avoid signal-level probing loops. Presence checks at recording start are acceptable only if they replace the hard bind and remain in one place.

The key criterion: a disconnected DJI mic must not make ordinary speech-to-text unusable.

## Immediate operational note

Changing the system default source alone is probably insufficient while the service wrapper exports `PIPEWIRE_NODE`. A durable fix needs a Home profile change and `whisrs.service` restart through activation. Do not restart PipeWire or WirePlumber as the primary fix; the problem is the declared binding, not a stuck daemon alone.

## Coordination note

`tools/orchestrate claim` could not run because the local helper tried to fetch an unavailable pinned `nota-codec` revision. I checked visible lock projections before editing; no lane projected a claim on `/git/github.com/LiGoldragon/CriomOS-home/INTENT.md`. The report itself is exempt from claims.

## Open question for the psyche

Should the next implementation intentionally sacrifice DJI wake-latency optimization in exchange for reliable ordinary laptop-mic fallback?

My recommended answer is yes for the next pass: delete the hard DJI hot-loop dependency first, verify ordinary dictation works without the DJI connected, then reintroduce only a much smaller explicit DJI path if the wake delay is still unacceptable.
