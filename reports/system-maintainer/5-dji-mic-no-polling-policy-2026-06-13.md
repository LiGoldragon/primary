# DJI mic no-polling policy fix — 2026-06-13

## Finding

The old `dji-keepalive.service` was a shell watchdog around PipeWire state. It checked the DJI BlueZ card and source on fixed sleeps, then reasserted the headset profile after WirePlumber had already moved the card away from MSBC/headset mode.

The observed live state had two truths:

- Pulse/WirePlumber reported the card `Active Profile` as `headset-head-unit` when repaired.
- The BlueZ card property could still show `bluez5.profile = off`, and WirePlumber autoswitch could restore the active profile to `off` after capture links disappeared.

That explained the intermittent wake delay: speech-to-text sometimes arrived while the card was back at `off`, so PipeWire/WirePlumber had to rebuild the HFP/MSBC capture path.

## Fix

CriomOS-home commit `852ad939` replaces the polling service with policy-owned graph state:

- removes `dji-keepalive.service` and the shell polling script;
- adds a PipeWire declarative loopback graph under `pipewire/pipewire.conf.d/60-dji-mic-hot-capture.conf`;
- adds a WirePlumber policy fragment under `wireplumber/wireplumber.conf.d/60-dji-mic-policy.conf`;
- pins `bluez_card.04_A8_5A_0B_EB_B0` to `device.profile = headset-head-unit`;
- disables WirePlumber's Bluetooth autoswitch restore-to-off path;
- keeps the DJI capture source active through a graph stream into a dedicated null sink, not through a polling watchdog.

CriomOS commit `8762286b` updates the full OS lock to consume that CriomOS-home commit.

## Live Ouranos state after manual apply

The old polling unit is inactive. The live graph has:

- DJI card active profile: `headset-head-unit`;
- `device.profile = headset-head-unit` on the DJI BlueZ card;
- DJI input source `bluez_input.04:A8:5A:0B:EB:B0` in `RUNNING` state after idle;
- a loopback feeding `dji_mic_hot_sink`.

The live WirePlumber process had to be restarted manually because the current user systemd manager cannot restart services whose units are attached to the stale/not-loaded `session.slice`. That is separate from the DJI policy bug.

## Validation

- `nix build .#checks.x86_64-linux.dji-keepalive` passed in CriomOS-home.
- `nix flake check --no-build` passed in CriomOS-home.
- A short `pw-record` capture completed, and after capture the card stayed in `headset-head-unit` rather than restoring to `off`.
- After the live graph module was loaded, the DJI source remained `RUNNING` after idle with `dji-keepalive.service` inactive.
