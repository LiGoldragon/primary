# Bluetooth Recording Warning Scout Map

Task: map local, read-only facts for a system that warns through Bluetooth headphones when a Bluetooth microphone disconnects during recording, and reduces audio loss if the recorder crashes. Scope was host OS/audio stack and viable push-event surfaces. I did not change audio configuration, install packages, disconnect devices, play audio, or run a real recording.

Hardware addresses are intentionally redacted as `<bt-mac>`.

## Commands Consulted

- Intent: `spirit "(PublicTextSearch [bluetooth microphone recording warning crash audio polling])"` returned public record `c5nq`: build event surfaces, not polling.
- OS/services/tools: `uname -a`, `cat /etc/os-release`, `systemctl --version`, `systemctl --user status pipewire pipewire-pulse wireplumber pulseaudio`, `systemctl status bluetooth`, `pipewire --version`, `wireplumber --version`, `bluetoothctl --version`, `pactl --version`, `command -v ...`.
- Audio graph: `pactl info`, `wpctl status`, `pactl list short sources`, `pactl list short sinks`, `pactl list sources`, `pactl list cards`, `pactl list modules`, `pactl list source-outputs`, `pactl list sink-inputs`, `pw-link -l`, `pw-cli ls Node`, `wpctl inspect ...`, `pw-metadata -n default`.
- Event surfaces: `timeout 2 pactl subscribe`, `timeout 2 pw-mon --hide-props --hide-params --print-separator`, `timeout 2 pw-metadata -n default -m`, `busctl --system introspect ...`, `dbus-monitor --help`, `busctl --help`.
- Prototype tools: `pw-play --help`, `paplay --help`, `parec --help`, `pw-cat --help`, `ffmpeg -devices`, `ffmpeg -h muxer=segment`.

## Observed Facts

- OS is NixOS 26.05 Yarara: `/etc/os-release` reports `PRETTY_NAME="NixOS 26.05 (Yarara)"`, `BUILD_ID="26.05.20260422.0726a0e"`.
- Kernel is `Linux ouranos 7.0.1 ... x86_64 GNU/Linux` from `uname -a`; systemd is `260` from `systemctl --version`.
- Audio server is PipeWire with Pulse compatibility:
  - `pipewire.service`, `pipewire-pulse.service`, and `wireplumber.service` are active user services.
  - `pulseaudio.service` is present but inactive.
  - `pactl info` reports `Server Name: PulseAudio (on PipeWire 1.6.3)`.
  - Versions: PipeWire `1.6.3`, WirePlumber `0.5.14`, `pactl`/libpulse `17.0`.
- Bluetooth is BlueZ:
  - `bluetooth.service` is active and runs `bluez-5.86`/`bluetoothd`.
  - `bluetoothctl --version` reports `5.86`.
  - `bluetooth.service` logs include HFP/HSP-related failures such as `Hands-Free Voice gateway failed connect` and `ext_io_disconnected`, so headset voice transport instability has happened on this host.
- Current defaults are not Bluetooth:
  - `pactl get-default-source` and `pw-metadata -n default` both show built-in digital mic `alsa_input...HiFi__Mic1__source`.
  - `pactl get-default-sink` and `pw-metadata -n default` both show built-in speaker `alsa_output...HiFi__Speaker__sink`.
- Current graph has a Bluetooth audio device:
  - `wpctl status` shows BlueZ device `DJI-MIC2-0BEBB0`, Bluetooth source, and Bluetooth sink.
  - `pactl list cards` shows `bluez_card.<bt-mac>`, `device.api = "bluez5"`, active profile `headset-head-unit`, codec `msbc`, with one source and one sink available.
  - `pactl list sources` shows Bluetooth input `bluez_input.<bt-mac>` with `device.bus = "bluetooth"` and `api.bluez5.connection = "connected"`.
  - `wpctl inspect 151` shows Bluetooth sink `bluez_output.<bt-mac>.1`, `media.class = "Audio/Sink"`, `api.bluez5.profile = "headset-head-unit"`.
- BlueZ D-Bus state is more reliable than `bluetoothctl devices Connected` here:
  - `bluetoothctl devices Connected` returned no rows.
  - `busctl get-property ... org.bluez.Device1 Connected` for the same device returned `b true`.
  - `busctl get-property ... ServicesResolved` returned `b false`.
- Built-in fallback mics exist:
  - `pactl list sources` shows built-in `Digital Microphone` and `Stereo Microphone`.
  - `pactl list cards` shows built-in digital mic availability `unknown`; stereo mic availability `not available`.
- There is an existing live loopback path:
  - `pactl list modules` shows `libpipewire-module-loopback` named `DJI Mic Hot Capture`.
  - Its capture target is `bluez_input.<bt-mac>.0`; playback target is `dji_mic_hot_sink`.
  - `pw-link -l` shows `bluez_input.<bt-mac>.0:capture_MONO -> dji_mic_hot_capture:input_MONO -> dji_mic_hot_sink`.
  - This is live routing evidence only; it is not evidence of any on-disk or crash-recovery buffer.
- Installed prototype commands include `pactl`, `wpctl`, `pw-cli`, `pw-dump`, `pw-link`, `pw-mon`, `pw-metadata`, `pw-play`, `pw-cat`, `paplay`, `parec`, `bluetoothctl`, `busctl`, `dbus-monitor`, `journalctl`, and `ffmpeg`.
- `aplay`, `arecord`, and `speaker-test` were not found by `command -v` in the current PATH.
- FFmpeg is available as `8.0.1`; `ffmpeg -devices` shows `DE pulse`, and `ffmpeg -h muxer=segment` confirms the segment muxer is present.

## Push Event Surfaces

- Default source changes:
  - Best local CLI surface: `pw-metadata -n default -m`.
  - Evidence: `pw-metadata -n default -m` immediately printed `default.audio.source` and `default.configured.audio.source`; with `-m` it remains subscribed.
  - Application API equivalent: PipeWire metadata listener for the `default` metadata object and keys `default.audio.source` / `default.configured.audio.source`.
- Audio device/source/card/stream changes:
  - Pulse-compatible CLI: `pactl subscribe`.
  - Evidence: `timeout 2 pactl subscribe` emitted `Event 'new' on client #...`.
  - Use it to wake on `source`, `source-output`, `card`, and `server` changes, then refresh with `pactl list sources/cards/source-outputs` or native PipeWire state.
  - Application API equivalent: libpulse `pa_context_subscribe()` with masks for source, source-output, card, and server.
- Native PipeWire graph changes:
  - CLI: `pw-mon --print-separator` for object add/remove/change events; `pw-mon --hide-props --hide-params` is parseable but less informative.
  - Evidence: `timeout 2 pw-mon ...` printed current registry objects and a live `removed: id: 80` event.
  - Application API equivalent: PipeWire registry listener for `Node`, `Device`, `Port`, `Link`, and `Metadata` objects; filter for `media.class = "Audio/Source"`, `Audio/Sink`, `device.api = "bluez5"`, and node names matching the chosen source/sink.
- Bluetooth disconnects:
  - BlueZ D-Bus is the clean event surface.
  - Evidence: `busctl --system introspect ... org.freedesktop.DBus.Properties` shows `PropertiesChanged signal sa{sv}as`; `busctl --system introspect ... org.bluez.Device1` shows `Connected` with `emits-change` and a `Disconnected signal ss`.
  - Prototype commands:
    - Single object wait: `busctl --system wait /org/bluez/hci0/dev_<BT_MAC> org.freedesktop.DBus.Properties PropertiesChanged`
    - Diagnostic monitor: `dbus-monitor --system "type='signal',sender='org.bluez',interface='org.freedesktop.DBus.Properties',member='PropertiesChanged'"`
  - Caveat: raw `dbus-monitor` reported `unable to enable new-style monitoring ... AccessDenied` and fell back to eavesdropping on this host. Production code should subscribe normally with a D-Bus library such as `zbus`, not rely on bus-wide sniffing.
- Journald/log following is useful only as diagnostics:
  - `bluetooth.service` logs already contain headset voice gateway failures.
  - Do not make journald text parsing the primary event source when BlueZ D-Bus and PipeWire/Pulse events are available.

## Warning Playback

- If the Bluetooth output sink still exists, target it explicitly instead of relying on defaults:
  - `paplay --device='bluez_output.<bt-mac>.1' warning.wav`
  - `pw-play --target 'bluez_output.<bt-mac>.1' warning.wav`
- Evidence:
  - `paplay --help` supports `--device=DEVICE` and accepts sink/source names.
  - `pw-play --help` supports `--target` by node serial or name.
  - Current Bluetooth sink is `bluez_output.<bt-mac>.1`; current default sink is the laptop speaker, so explicit targeting is necessary if the warning must go to headphones.
- Limitation:
  - If the entire Bluetooth link or sink node is already gone, software cannot play through disconnected headphones. In that case the practical fallback is to warn through an available local sink, e.g. `paplay --device=@DEFAULT_SINK@ warning.wav`, and/or notify visually.
  - If only the Bluetooth microphone/source disappears while a Bluetooth sink remains, warning-through-headphones is viable.

## Fallback Versus Silence

- Fallback to laptop mic can be detected separately from silence by watching graph/routing identity, not signal amplitude.
- For a recorder using the default source:
  - Subscribe to `pw-metadata -n default -m`.
  - Treat `default.audio.source` changing from `bluez_input...` to `alsa_input...` as a fallback event.
  - Current host default is already `alsa_input...Mic1`, so a default-source recorder would currently use the laptop mic, not the Bluetooth mic.
- For a recorder pinned to a device:
  - Subscribe to `pactl subscribe` source-output events or native PipeWire link/node events.
  - Inspect the recorder’s source-output and link target; compare the actual input node to intended `bluez_input.<bt-mac>` or a known virtual source.
  - Current `pactl list source-outputs` shows the existing loopback stream has `target.object = "bluez_input.<bt-mac>.0"`; `pw-link -l` confirms the live link from Bluetooth input into the loopback.
- Silence alone is not enough:
  - Quiet speech, mute, dead transport generating zeros, and a fallback mic in a quiet room can all look like low amplitude.
  - Use silence/no-level detection only as a secondary symptom after graph/device identity says the expected source is still selected.

## Crash-Resilience Notes

- The audio stack will not recover samples lost while no process is capturing them. To avoid loss across recorder crashes, a separate supervised capture/buffer process must already be running, or the recorder must write in small durable chunks.
- Current loopback/hot-sink path can keep the Bluetooth source routed independently of one recorder, but it does not persist historical audio by itself.
- Practical prototype commands:
  - Segment to independent files so a crash loses at most the active segment:
    - `ffmpeg -f pulse -i 'bluez_input.<bt-mac>' -f segment -segment_time 10 -strftime 1 'rec-%Y%m%d-%H%M%S.wav'`
    - Or capture from the current virtual hot sink monitor: `ffmpeg -f pulse -i 'dji_mic_hot_sink.monitor' -f segment -segment_time 10 -strftime 1 'rec-%Y%m%d-%H%M%S.wav'`
  - Record raw PCM when final container headers are a risk:
    - `parec --raw --rate=48000 --format=s16le --channels=1 --device='bluez_input.<bt-mac>' > rec.raw`
  - PipeWire-native raw capture option:
    - `pw-cat --record --target 'bluez_input.<bt-mac>' --rate 48000 --channels 1 --format s16 rec.raw`
  - Supervise the recorder separately with a user service/process supervisor using restart-on-failure; the event monitor can warn on recorder process exit independently of mic disconnect.

## Likely Implementation Shape

- Maintain three separate subscriptions:
  - BlueZ D-Bus for `Connected=false`, `ServicesResolved`, and `Disconnected`.
  - PipeWire metadata/registry or `pactl subscribe` for source/default/source-output changes.
  - Recorder process supervision for crash/restart events.
- Keep separate identities for intended input and warning output:
  - Intended input: exact `bluez_input...` node or a deliberate virtual source/monitor.
  - Warning output: exact Bluetooth sink `bluez_output...` when present; fallback sink otherwise.
- Trigger warning when:
  - BlueZ reports device disconnected.
  - PipeWire removes/changes the Bluetooth source or its card/profile.
  - Recorder source-output/link moves from Bluetooth/virtual source to `alsa_input...`.
  - Recorder process exits unexpectedly.

## Unknowns / Not Checked

- I did not simulate a Bluetooth disconnect, profile switch, or recorder crash, so observed event payloads for those transitions are inferred from local introspection/help plus current graph state.
- I did not play a warning sound; command viability is from installed tools and help text.
- I did not inspect or change NixOS configuration files.
- I did not determine the user’s exact target headphones versus the currently connected BlueZ audio device; current evidence names one BlueZ headset-form-factor device with both source and sink.
- I did not inspect browser/portal-specific recording behavior; if the real recorder is a browser or conferencing app, source-output identification may need application properties from PipeWire/Pulse events.
- `ServicesResolved=false` while `Connected=true` needs live transition testing; it may be normal for this device state or a sign that BlueZ service discovery is incomplete.
