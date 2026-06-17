# DJI / Whisrs simplification and medium video tools — 2026-06-17

## Result

The DJI hot-loop dependency was removed from `CriomOS-home`, deployed to Ouranos through `HomeOnly Activate`, and cleaned out of the live PipeWire session without restarting PipeWire or WirePlumber.

Medium-sized Home nodes now carry the videographer test tool additions that were missing after reading the latest videographer reports: Node.js, pnpm, the Whisper CLI, and a no-conflict `faster-whisper-python` wrapper for Python scripts needing `faster_whisper` word timestamp support.

## Intent records

- `1vj5` — simplify the DJI / Whisrs mic path rather than growing a pile of keepalive code.
- `tve6` — proceed with the subtractive implementation, prioritizing ordinary laptop-mic fallback over the DJI wake-latency optimization.

## Code changes

`CriomOS-home` final main commit: `865c47e15410` — avoid video Python profile collisions.

Substance across the pushed `CriomOS-home` commits:

- Removed the `PIPEWIRE_NODE` source-serial binding from `modules/home/profiles/min/dictation.nix`.
- Removed the declared `dji_mic_hot_sink` PipeWire null sink and loopback.
- Removed the DJI-specific WirePlumber Bluetooth policy fragment from the ordinary dictation profile.
- Replaced `checks/dji-keepalive/default.nix` with `checks/whisrs-default-input/default.nix`, which guards against reintroducing a hard bind to a removable PipeWire source.
- Added medium-profile video tools in `modules/home/profiles/med/default.nix`:
  - `nodejs`
  - `pnpm`
  - `python3Packages.openai-whisper` for the `whisper` CLI
  - `faster-whisper-python`, a wrapper around a Python environment containing `faster_whisper`

The first attempted video addition used `python3Packages.whisperx`, but deployment proved it broken at the current nixpkgs pin because a fixed-output dependency hash no longer matched. It was replaced before final activation. A later attempt to put a full Python environment in `home.packages` conflicted with the existing Python binary in the Home profile; the final wrapper exposes only a unique command name and avoids that collision.

`CriomOS` final main commit: `6646275dbe31` — pin simplified CriomOS-home dictation profile.

The `CriomOS` lock now points at the final `CriomOS-home` commit so a future FullOS switch does not restore the old Home input.

## Validation

Local/repo checks:

- `nix flake check --no-build` passed in `CriomOS-home` before the final video-tool wrapper adjustment.
- Focused checks passed after each relevant adjustment:
  - `checks.<system>.whisrs-default-input`
  - `checks.<system>.whisrs-dictation-bindings`
- Focused formatting passed for the new check file. The repository still has pre-existing formatter drift in unrelated files.
- Direct `CriomOS` `nix flake check --no-build` is not a valid witness without lojix-projected `system`; it fails on the repo’s intentional stub-input guard.

Deploy/runtime checks:

- `lojix-run` `HomeOnly goldragon ouranos li ... Activate None None` succeeded after the final wrapper fix.
- `whisrs.service` is active and running.
- `whisrs status` reports `idle`.
- The running `whisrs.service` environment no longer contains `PIPEWIRE_NODE`.
- The removed Home-managed files are absent:
  - `~/.config/pipewire/pipewire.conf.d/60-dji-mic-hot-capture.conf`
  - `~/.config/wireplumber/wireplumber.conf.d/60-dji-mic-policy.conf`
- The live default source was switched to the laptop mic source.
- A two-second PipeWire recording from the laptop mic showed signal.
- A Whisrs start/cancel smoke test opened the laptop mic source and canceled without transcription.
- The stale live DJI null sink and loopback modules from the earlier manual session repair were unloaded without restarting PipeWire or WirePlumber.

Video tool checks after activation:

- Present in the Home profile: `ffmpeg`, `ffprobe`, `wf-recorder`, `yt-dlp`, `mpv`, `magick`, `mediainfo`, `mkvmerge`, `piper`, `espeak-ng`, `scenedetect`, `whisper`, `node`, `pnpm`, `faster-whisper-python`.
- `faster-whisper-python -c 'import faster_whisper'` succeeded.

## Remaining notes

The removed DJI hot loop means ordinary dictation now follows the default input path. If DJI fast-start becomes important again, it should return as an explicit small mode or source-selection boundary, not as an always-present virtual source that can make a disconnected Bluetooth accessory the mandatory dictation substrate.

The videographer report asked for WhisperX specifically because it gives word-level timestamps. At the current nixpkgs pin, WhisperX is not deployable without fixing its dependency hash chain. The activated fallback gives two practical surfaces now: `whisper` as a CLI and `faster_whisper` as an importable Python library for scripts that need word timestamps.
