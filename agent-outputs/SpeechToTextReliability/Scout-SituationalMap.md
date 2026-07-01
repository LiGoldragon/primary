# Speech-To-Text Reliability Situational Map

## Task And Scope

- Scope: map local facts for a reliable speech-to-text recording redesign after a lost long recording caused by Bluetooth microphone disconnect and in-memory capture.
- Constraints honored: no source edits, no raw `git`, no paid STT calls, no transcript/history contents inspected. One output file was written under `agent-outputs/SpeechToTextReliability/`.

## Commands And Evidence Consulted

- Workspace and coordination: `pwd`, `ls -la`, `jj status --no-pager`, `orchestrate "(Observe Roles)"`.
- Intent query: `spirit "(PublicTextSearch [speech transcription recording audio stt whisper])"` returned `(Error [no matching record])`.
- Search: `rg` and `find` across `/home/li/primary` and `/git/github.com/LiGoldragon` for STT/audio terms.
- Tool/runtime probes: `command -v whisrs whisrsd whisrs-recall`, `whisrs --help`, `whisrs spool --help`, `whisrs spool list`, `readlink -f`, `systemctl --user cat/show`, `pactl info`, `pactl get-default-source`, `pactl list short sources`, redacted `journalctl --user-unit=whisrs.service`.
- Version/source probes: `jj status`, `jj log`, `jj bookmark list --all`, `jj git remote list`, `jj file show -r c32c8bcf793abbe4492398c2b10738950972f2e5 ...`.
- Upstream web check: GitHub page for `https://github.com/y0sif/whisrs` via web search/open result; observed latest release `v0.1.19` dated June 21, 2026 and 222 commits on the public page.

## Observed Facts

- Daily STT tool is Whisrs:
  - `/git/github.com/LiGoldragon/CriomOS-home/skills.md:108` says "The daily STT path is Whisrs."
  - `/git/github.com/LiGoldragon/CriomOS-home/skills.md:110-112` names owners: `modules/home/profiles/min/dictation.nix`, `modules/home/profiles/min/sfwbar.nix`, and `packages/whisrs/`.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:66-88` installs `~/.config/whisrs/config.toml` with `backend = "openai"`, `language = "en"`, `device = "default"`, and `model = "gpt-4o-transcribe"`.
  - Live config exists at `/home/li/.config/whisrs/config.toml:1-21` with the same backend/model/device shape and no API key in the file.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:19-40` creates the daemon wrapper; lines 22 and 36 load/export `WHISRS_OPENAI_API_KEY` from `gopass`.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:90-119` defines `whisrs.service`, `Restart = "on-failure"`, and starts after PipeWire.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:212-231` binds `Mod+V` to `whisrs toggle-copy`, `Mod+Shift+V` to `whisrs toggle`, `Mod+Alt+V` to `whisrs-recall`, and `Mod+Ctrl+V` to `whisrs cancel`.

- Installed Whisrs is the active runtime:
  - `command -v` reports `/home/li/.nix-profile/bin/whisrs`, `/home/li/.nix-profile/bin/whisrsd`, and `/home/li/.nix-profile/bin/whisrs-recall`.
  - `readlink -f` resolves them to `/nix/store/lcpzgaz7jlhqnsii7g0nbzkvpzmzqskw-whisrs-0.1.11/bin/{whisrs,whisrsd,whisrs-recall}`.
  - `whisrs --help` reports version `0.1.11` and commands including `toggle-copy` and `spool`.
  - `whisrs spool --help` reports `list`, `retry`, and `drop`.
  - `systemctl --user show whisrs.service` reports `LoadState=loaded`, `ActiveState=active`, `SubState=running`, `ExecMainPID=3193790`.
  - `systemctl --user cat whisrs-spool-retry.service` shows `ExecStart=... whisrs spool retry --all --auto || true`; the unit is enabled but inactive after its oneshot.

- Current audio selection is not the Bluetooth source at probe time:
  - `pactl info` reports PipeWire `1.6.3`, default source `alsa_input...Mic1...source`.
  - `pactl list short sources` showed a BlueZ input source present but suspended, plus a DJI keepalive sink monitor running. The exact hardware address is omitted here.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:149-188` declares the DJI PipeWire keepalive loopback.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:190-205` declares WirePlumber source priority for the DJI source.
  - `/git/github.com/LiGoldragon/CriomOS-home/checks/whisrs-default-input/default.nix:28-29` asserts Whisrs must not hard-bind capture to a removable PipeWire source.

- Spool/recovery state exists:
  - `find "$XDG_STATE_HOME/whisrs/spool"` found two local `.ogg` files: one rescue file around 430 KiB and one `spool_*.ogg` around 88 MiB. Contents were not inspected.
  - `whisrs spool list` reports one spooled recording awaiting retry.
  - `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:122-147` defines a network-online retry oneshot for spooled recordings.
  - `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/default.nix:60-72` wraps `whisrsd` with `ffmpeg-headless` in `PATH`, with a comment that ffmpeg is the daemon encoder for OPUS-in-OGG spool files.

## Source And Version Shape

- `CriomOS-home` packages the forked `criomos` branch, not the checked-out Whisrs `main` worktree:
  - `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:77-83` defines `whisrs-src.url = "github:LiGoldragon/whisrs?ref=criomos"`.
  - `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:2872-2887` pins that input to `LiGoldragon/whisrs` rev `c32c8bcf793abbe4492398c2b10738950972f2e5`, original ref `criomos`.
  - `jj log -r c32c8bcf793abbe4492398c2b10738950972f2e5` in `/git/github.com/LiGoldragon/whisrs` finds commit `c32c8bc...` with description `whisrs: add openai opus upload witness`.
  - `/git/github.com/LiGoldragon/whisrs` worktree status is clean, but `@` is empty over `af25e633 chore: release v0.1.11`; `main` and `main@origin` are `6a5cd1ac Merge pull request #26 from y0sif/fix/recovery-test-tempdir`.
  - `jj bookmark list --all` shows only `main`, `main@origin`, and `gh-pages@origin`; no local `criomos` bookmark is checked out.
  - `/git/github.com/LiGoldragon/whisrs/.git/config` has only remote `origin = ssh://git@github.com/LiGoldragon/whisrs.git`.

- Upstream evidence suggests a rebase/update may be needed before or during deeper work:
  - `Cargo.toml` at pinned rev `c32c8bc` has version `0.1.11` and `repository = "https://github.com/y0sif/whisrs"` (`/git/github.com/LiGoldragon/whisrs@c32c8bc:Cargo.toml:1-8`).
  - The pinned README points users to `https://github.com/y0sif/whisrs/releases/latest` (`/git/github.com/LiGoldragon/whisrs@c32c8bc:README.md:51-56`).
  - Public GitHub page for `y0sif/whisrs` observed latest release `v0.1.19` on June 21, 2026 and 222 commits, while local deployed package is `0.1.11`.
  - Interpretation: the local fork carries CriomOS patches on an older version. A rebase against upstream likely has to reconcile upstream changes since `0.1.11` with the CriomOS spool/status/recall patches.

## Memory Versus Disk Evidence

- Live capture still buffers audio in memory before normal transcription:
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/capture.rs:66` creates an unbounded `mpsc::unbounded_channel::<AudioChunk>()`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/capture.rs:201-207` cpal input callback sends each callback buffer as `data.to_vec()` into that channel.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/capture.rs:105-129` `stop_and_collect()` stops the stream, drains the channel, and appends chunks into `let mut all_samples = Vec::new()`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:1384-1399` batch dictation calls `cap.stop_and_collect().await?`, then logs the collected sample count.
  - Recent `journalctl --user-unit=whisrs.service` corroborates runtime behavior: entries show `captured N audio samples`, `collected N audio samples`, then `encoded Opus/Ogg: N bytes`, then transcription complete. No per-chunk disk path is logged.

- Encoding also happens from in-memory samples:
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/capture.rs:257-280` `encode_wav()` writes to a `Cursor<Vec<u8>>` and returns `Vec<u8>`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/capture.rs:283-342` `encode_opus_ogg()` copies `samples.to_vec()`, writes chunks to `ffmpeg` stdin, waits for output, and returns `output.stdout` as `Vec<u8>`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:1570-1595` chooses preferred upload encoding and returns a `Vec<u8>`.

- Existing spool is not incremental capture persistence:
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/recovery.rs:1-9` describes spool as audio saved when transcription fails, under `$XDG_STATE_HOME/whisrs/spool`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/audio/recovery.rs:123-170` `save_recovery_audio(samples)` creates the spool directory, encodes the entire `samples` slice to Opus/Ogg or WAV, then writes the completed bytes with `std::fs::write`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:1425-1454` spools only when transcription audio encoding fails.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:1459-1490` spools only when `transcribe(&audio_data, ...)` returns an error.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:160-245` clean shutdown tries to stop and collect an active batch recording and then spool it. Lines 207-212 warn that interrupted streaming recordings cannot be fully drained by this shutdown spool path.
  - Search of pinned `src` found `std::fs::write`, `rename`, `write_all`, and append `OpenOptions`, but no `sync_all` or `sync_data`; this is evidence that current spool writes are not explicitly fsynced.

- Current default backend is batch OpenAI REST:
  - `/home/li/.config/whisrs/config.toml:1-21` and `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix:66-88` set `backend = "openai"`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:555-558` maps `"openai"` to `OpenAIRestBackend`.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/transcription/openai_rest.rs:64-121` sends the complete encoded byte buffer as multipart form data.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/transcription/mod.rs:94-107` default `transcribe_stream()` also collects chunks into `Vec<i16>` unless a backend overrides it.

- Command mode also buffers in memory:
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:2102-2108` command mode uses `let mut all_samples: Vec<i16> = Vec::new()` and extends it per chunk.
  - `/git/github.com/LiGoldragon/whisrs@c32c8bc:src/daemon/main.rs:2169-2175` then encodes the full sample buffer for transcription.

## Obvious Implementation Surfaces

- Primary code surface: `/git/github.com/LiGoldragon/whisrs` pinned/deployed `criomos` branch at `c32c8bc...`, not the current `main` worktree.
- Capture surface:
  - `src/audio/capture.rs` owns all cpal capture, chunk creation, stop signaling, and sample collection.
  - A crash-resilient design would likely introduce a data-bearing recording writer here or adjacent to it, because every live audio chunk passes through `run_capture()` and the callback at `capture.rs:201-207`.
- Spool/persistence surface:
  - `src/audio/recovery.rs` already owns `$XDG_STATE_HOME/whisrs/spool/`, ID/path helpers, migration, and retry-visible files.
  - It can be reshaped from "post-failure save whole buffer" into "active recording journal/spool writer" with temp/current files, finalize/rename, and explicit `sync_data`/`sync_all`.
  - Current `std::fs::write` in `recovery.rs:144-162` is the obvious first durability weak point if keeping the existing whole-buffer fallback.
- Daemon state surface:
  - `src/daemon/main.rs:41-75` in the checked-out source and pinned `daemon.rs:55-75` hold `audio_capture`, `recording_window_id`, `recording_started_at`, and output mode. This is where an active persisted-recording handle or path would be tracked.
  - `src/daemon/main.rs:908-1092` handles start/stop of normal dictation and chooses streaming versus batch.
  - `src/daemon/main.rs:1384-1490` is the normal batch stop/transcribe/spool-on-failure path.
  - `src/daemon/main.rs:1724-1865` already lists/retries/deletes spool entries and appends successful retries to history and clipboard.
  - `src/daemon/main.rs:2060-2178` is the command-mode in-memory capture path.
- Transcription surface:
  - `src/transcription/mod.rs:51-74` already has an `AudioUploadFormat` abstraction.
  - `src/transcription/openai_rest.rs:92-103` detects `OggS` versus `RIFF` bytes and sets multipart file name/MIME. This should make retrying persisted `.ogg` files through OpenAI REST plausible.
  - Any persisted-file design needs either a backend API that accepts a path/reader or a controlled read of finalized bytes before upload.
- Nix/deploy surface:
  - `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/default.nix` packages the source and already provides ffmpeg to `whisrsd`.
  - `/git/github.com/LiGoldragon/CriomOS-home/flake.lock` must be updated to the new fork revision after Whisrs changes.
  - `/git/github.com/LiGoldragon/CriomOS-home/checks/whisrs-default-input/default.nix` is the place for policy checks ensuring the redesign does not reintroduce hard binding to a removable Bluetooth source.

## Unknowns And Blockers

- The exact failure event was not reconstructed. I inspected only the last 80 Whisrs journal lines; they showed normal recordings and cancels, not the lost 20-minute incident.
- I did not inspect transcript contents in `~/.local/share/whisrs/history.jsonl` or audio contents in spool/rescue files.
- I did not fetch remotes with Jujutsu because that would mutate local repo metadata. The upstream check is from the public GitHub page, not a local fetched ref.
- I did not inspect upstream `v0.1.19` source or diff it against `c32c8bc`; rebase risk is inferred from local version `0.1.11`, upstream latest release `v0.1.19`, and fork metadata.
- The local `/git/github.com/LiGoldragon/whisrs` worktree is not on the deployed `criomos` branch. Implementers should use `jj file show -r c32c8bc...` for current deployed source evidence, or explicitly create/switch to an isolated branch/workspace before editing.
- No tests were run; the brief asked for scouting facts, and tests were not necessary to establish the persistence/buffering shape.

