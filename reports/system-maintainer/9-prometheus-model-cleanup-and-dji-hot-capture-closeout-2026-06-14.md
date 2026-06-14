# Prometheus model cleanup and DJI hot-capture closeout — 2026-06-14

## Result

Prometheus no longer has redundant manual model GC roots or duplicate large model downloads under `/home/li`. The deployed system generation still roots the large-AI model catalog, no large model-ish home-folder files remain, and the llama router stayed active after cleanup.

Ouranos now has a deployed Home fix for the DJI Mic / Whisrs path that does not poll. Whisrs resolves the `dji_mic_hot_sink.monitor` PipeWire source to its current `object.serial` once at daemon start and exports that serial as `PIPEWIRE_NODE`, because the PipeWire ALSA plugin ignored the Pulse monitor name but honored the source serial.

## Prometheus closeout

The manual model root directory `/nix/var/nix/gcroots/criomos-largeai-models` was removed after verifying the deployed system roots already protected the model catalog. Removing it exposed only non-model dead paths; a subsequent GC deleted 357 store paths and freed 87.2 MiB while `prometheus-llama-router.service` remained active.

The only large model-ish files under `/home/li` were two Qwen GGUF downloads in `Downloads`. Each was compared by basename and SHA-256 against a Nix-store copy before deletion. After removal, `/home/li/Downloads` reported size `0`, and no remaining large model-ish files were found under `/home/li`.

Final verification on 2026-06-14:

- manual model root directory: absent
- large model-ish files under `/home/li`: 0
- `/home/li/Downloads` size: 0
- dead Nix paths: 0
- model-ish dead Nix paths: 0
- `prometheus-llama-router.service`: active

## DJI / Whisrs source fix

The first no-polling replacement removed the old `dji-keepalive.service` polling loop and installed WirePlumber/PipeWire policy, but live testing showed Whisrs still captured from the moving public Bluetooth source after auto-connect and repeated start/stop. `PIPEWIRE_NODE=dji_mic_hot_sink.monitor` was present in the systemd unit but did not affect the PipeWire ALSA capture backend.

A short ALSA capture test showed the important distinction:

- `PIPEWIRE_NODE=dji_mic_hot_sink.monitor` still captured from the public Bluetooth source.
- `PIPEWIRE_NODE=<hot-source-object-serial>` captured from the hot virtual monitor source.

The durable Home fix therefore resolves the serial at Whisrs daemon startup through `pactl list sources`, requiring `dji_mic_hot_sink.monitor` to exist, then exports that serial as `PIPEWIRE_NODE` before `whisrsd` starts. There is no periodic inspection, retrying graph repair, or keepalive loop.

Source commits:

- `CriomOS-home` `23b6f001` — bind Whisrs to the DJI hot source and make the loopback target the internal DJI HFP source.
- `CriomOS-home` `1012a722` — update the rust-overlay channel pin so the Home profile Rust toolchain builds again.
- `CriomOS-home` `aa4e16c7` — resolve the DJI hot source serial for Whisrs at daemon start.
- `CriomOS` `b45afb8b` — pin `CriomOS-home` to the final Home fix for FullOS propagation.

Validation:

- `nix build .#checks.x86_64-linux.dji-keepalive` passed.
- `nix flake check --no-build` passed.
- `lojix-run` `HomeOnly goldragon ouranos li ... Activate None None` succeeded for `CriomOS-home` `aa4e16c7`.
- `whisrs.service`, `pipewire.service`, and `pipewire-pulse.service` were active; `dji-keepalive.service` was inactive.
- Two consecutive `whisrs toggle-copy` starts followed by `whisrs cancel` showed Whisrs source outputs on source `851623`, which was the live `dji_mic_hot_sink.monitor` source, not on the public `bluez_input.04:A8:5A:0B:EB:B0` source.
- Both validation captures were canceled, so no transcription request was sent.

## Session-slice addendum

The live PipeWire graph on Ouranos still contained the older ad-hoc loopback node names during the first validation because `systemctl --user restart pipewire.service pipewire-pulse.service` failed with `Unit session.slice not found`. The services stayed active and the final Whisrs fix was validated without a broad audio-stack restart.

A later non-disruptive check found the root cause: stale broken Home Manager symlinks at `~/.config/systemd/user/session.slice` and `~/.config/systemd/user/background.slice` shadowed the valid system unit files under `/etc/systemd/user`. Removing those broken symlinks and running `systemctl --user daemon-reload` made `session.slice` and `background.slice` load as static system units again. A dry-run PipeWire restart then produced no error.

The durable Home config contains the declarative loopback and policy. A later safe audio-session restart or login should replace the old ad-hoc node names with the declared `dji_mic_hot_capture` and `dji_mic_hot_playback` nodes.
