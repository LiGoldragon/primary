# DJI Mic Keepalive Repair

## Outcome

The DJI Mic 2 keepalive path is now declarative in `CriomOS-home`, deployed to the live home profile on `ouranos`, and running.

The active user service now creates a visible PipeWire/Pulse null sink named `dji_mic_keepalive` with the displayed description `DJI-Mic-Keepalive`, then runs `pw-loopback` from the DJI Bluetooth source into that sink. This keeps the DJI capture source hot for speech-to-text without requiring a manual route in the volume control panel.

## Cause

The old service was failing for two separate reasons:

1. It waited on BlueZ `ServicesResolved`, but the DJI device can expose a working PipeWire source while `ServicesResolved=false`.
2. It targeted the old source name `bluez_input.04_A8_5A_0B_EB_B0.headset-head-unit-msbc`; the live source is `bluez_input.04:A8:5A:0B:EB:B0`.

It also did not create a visible sink. The new version loads a PipeWire-compatible Pulse null sink and bridges audio into it.

## Changed

CriomOS-home commit:

- `0d7378e0` — `home: repair DJI mic keepalive`

Files:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/dji-keepalive/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`

## Verification

Static checks passed:

- `nix build .#checks.x86_64-linux.dji-keepalive --no-link --print-build-logs`
- `nix build .#checks.x86_64-linux.whisrs-dictation-bindings --no-link --print-build-logs`

Activation succeeded through the repo version of `lojix-cli`:

- `HomeOnly goldragon ouranos li ... Activate (Some prometheus) None`

Live checks after activation:

- `dji-keepalive.service` is `active`.
- `pactl list short sinks` shows `dji_mic_keepalive` as `RUNNING`.
- `pactl list short sources` shows `bluez_input.04:A8:5A:0B:EB:B0` as `RUNNING`.
- `wpctl status` shows `DJI-Mic-Keepalive` and the `dji-mic-keepalive-capture` / `dji-mic-keepalive-playback` loopback filter.

## Remaining Notes

The installed `lojix-cli` in the old profile was stale and rejected current bracket-string NOTA. Activation worked by running the `lojix-cli` source repo with `nix run /git/github.com/LiGoldragon/lojix-cli# ...`.

The `CriomOS-home` checkout still has one unrelated dirty file, `modules/home/profiles/min/default.nix`, from another lane's jj editor-safety change. It was not included in the DJI commit.
