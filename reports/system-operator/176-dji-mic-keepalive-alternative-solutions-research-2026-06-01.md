# DJI Mic Keepalive Alternative Solutions Research

## Frame

This is a follow-up to `reports/system-operator/175-dji-mic-keepalive-profile-churn-and-deploy-fix-2026-06-01.md`.
The question: have other Linux users found different solutions to Bluetooth
mic wake delay / profile churn, and should any of those change our current
CriomOS direction?

## External Patterns Found

### 1. Disable automatic headset-profile switching

Several users solve unwanted profile churn by disabling WirePlumber's automatic
switch to HSP/HFP when an application requests microphone input.

Sources:

- Ask Ubuntu answer for newer WirePlumber:
  https://askubuntu.com/questions/1481852/disable-auto-switch-of-bluetooth-device-profiles-specifically-input-when-apps
- ArchWiki snippet mirrored through search results:
  `bluetooth.autoswitch-to-headset-profile = false`
- Arch mailing list workaround for a recent crash:
  https://lists.archlinux.org/archives/list/arch-general%40lists.archlinux.org/message/WR6KBJJXXCHDDFAX4HTJXT6J4RSRAD2T/

Fit for us:

- Not sufficient by itself. We actually want the DJI mic in the headset profile
  for dictation. Disabling autoswitch is useful when a separate mic exists and
  Bluetooth should stay A2DP.
- It could still be useful as a per-device rule for normal headphones, but not
  as the DJI dictation fix.

### 2. Disable HSP/HFP roles entirely

Some users remove headset-profile support from WirePlumber by restricting
`bluez5.roles` to A2DP-only roles. This prevents accidental low-quality profile
selection and avoids some HSP/HFP crashes.

Sources:

- Ask Ubuntu answer shows the A2DP-only variant.
- WirePlumber documents `bluez5.roles` and the role set:
  https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/bluetooth.html
- PipeWire property reference lists the same role vocabulary:
  https://docs.pipewire.org/devel/page_man_pipewire-props_7.html

Fit for us:

- Wrong for DJI dictation because it removes the microphone path.
- Similar in spirit to our fix only at the role-boundary level: instead of
  removing HFP, we removed the wrong-direction roles and kept the host-as-audio-
  gateway role needed for the mic.

### 3. Disable PipeWire/WirePlumber node suspend

A common fix for delayed audio start, pops, or idle devices is setting
`session.suspend-timeout-seconds = 0` on matching nodes, often Bluetooth
sources/sinks. Official PipeWire docs say value `0` means the node will not be
suspended. WirePlumber docs show the same property as a Bluetooth node rule.

Sources:

- PipeWire property reference:
  https://docs.pipewire.org/devel/page_man_pipewire-props_7.html
- WirePlumber Bluetooth rules example:
  https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/bluetooth.html
- NixOS Wiki PipeWire page gives the same shape for NixOS:
  https://wiki.nixos.org/wiki/PipeWire

Fit for us:

- Worth considering as a second layer. It targets PipeWire's own suspend policy,
  while our current loopback targets the device/transport by keeping real capture
  active.
- It may not defeat device-firmware sleep if the DJI transmitter sleeps despite
  PipeWire keeping the node unsuspended. The PipeWire docs explicitly distinguish
  session-manager suspend from device behavior.

### 4. Keep a real loopback/capture stream active

This is our current family of fix. PipeWire's `pw-loopback` can create loopback
nodes and target a microphone. User reports around virtual devices and loopbacks
show the same instinct: isolate unstable physical devices behind a persistent
PipeWire object, or keep an active stream so applications do not directly bear
device/profile churn.

Sources:

- `pw-loopback` man page:
  https://www.mankier.com/1/pw-loopback
- PipeWire virtual-device discussion:
  https://www.reddit.com/r/pipewire/comments/1ozrflt/bluetooth_devices_come_and_go_trying_a_solution/
- EasyEffects issue noting loopback-device complications with Bluetooth mics:
  https://github.com/wwmm/easyeffects/issues/4297

Fit for us:

- Best fit for "make the mic hot before Whisrs starts".
- Our implementation is more direct than most forum fixes because it keeps a
  capture stream open against the actual DJI source and avoids BlueZ profile
  reconnects.

### 5. Force auto-connect / reconnect profile lists

Some users solve partial reconnects or missing profiles by setting
`bluez5.auto-connect` for several profiles. WirePlumber documents this as a
device property for startup and partial-profile reconnection.

Sources:

- WirePlumber Bluetooth docs:
  https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/bluetooth.html
- Debian bug thread with `bluez5.auto-connect` workaround:
  https://www.mail-archive.com/debian-bugs-dist%40lists.debian.org/msg2040130.html

Fit for us:

- Possibly useful after resume/reconnect, but risky if it reintroduces wrong-
  direction HFP probing.
- If used, it should be scoped to the DJI card and only to roles that match the
  host-as-gateway model.

### 6. Toggle profile, restart services, or re-pair

Forum users frequently mention manual profile toggles, restarting Bluetooth /
PipeWire / WirePlumber, or forgetting/re-pairing the device. This matches the
old human workaround.

Sources:

- Manjaro Jabra thread:
  https://forum.manjaro.org/t/jabra-headset-microphone-stops-working-after-exactly-5-minutes/70518
- Fedora discussion threads around HSP/HFP failures and updates.

Fit for us:

- Symptom management only. It matches the behavior the user wants to eliminate.

## Comparison Against Our Current Fix

Our current fix combines two of the better external ideas:

- Role-boundary correction: keep HFP/HSP available, but remove the wrong host-
  side roles that triggered BlueZ profile probing against a remote service the
  DJI device does not advertise.
- Keepalive stream: keep a real PipeWire capture stream open to the DJI source.

What we did not add yet:

- A `session.suspend-timeout-seconds = 0` rule for the DJI Bluetooth source.
- A device-scoped `bluez5.auto-connect` rule after resume/reconnect.
- A stronger virtual-source abstraction that makes Whisrs bind to a stable
  virtual mic instead of the changing physical DJI source.

## Recommendation

Do not replace the current fix. The outside research mostly confirms it.

Best next improvement if the problem returns:

1. Add a DJI-specific WirePlumber node rule setting
   `session.suspend-timeout-seconds = 0` and possibly `node.pause-on-idle =
   false` for `bluez_input.04:A8:5A:0B:EB:B0`.
2. Test whether that removes the need for a constantly running loopback. If not,
   keep both: the suspend rule prevents PipeWire policy sleep; the loopback
   prevents device/transport sleep.
3. Consider making Whisrs consume a stable virtual `DJI Dictation Microphone`
   source, with the keepalive daemon responsible for relinking it to the real
   DJI source after reconnect/profile churn.

Avoid:

- A2DP-only HFP removal for the DJI device.
- Reintroducing BlueZ `ConnectProfile` profile hammering.
- Global Bluetooth autoswitch disable as a DJI fix.
