# Listener Fix-Pass Rust Audit

Task: audit `/git/github.com/LiGoldragon/listener` after the Listener frame-boundary and durability fix pass. Scope was the two prior assigned findings plus regressions in contract compatibility, recovery correctness, sync semantics, tests, artifact metadata, transcription handoff, and user-facing claims. No source files were edited.

## Findings

### High: Crash-survived recordings can be overwritten on daemon restart

Files:

- `/git/github.com/LiGoldragon/listener/src/runtime.rs:50`
- `/git/github.com/LiGoldragon/listener/src/capture.rs:89`
- `/git/github.com/LiGoldragon/listener/src/recording_log.rs:474`

Risk: the recording log format now commits bounded records with `flush` plus `sync_data`, but the runtime does not preserve those crash-survived files across a daemon restart. `ListenerRuntime::with_dependencies` initializes `CaptureSessionSequence::new(1)` every process start (`src/runtime.rs:50`). `CaptureStore::artifact_for_session` deterministically maps that to `capture-<session>.listenerlog` (`src/capture.rs:89`). `RecordingLogWriter::create_with_durability` opens the path with `.create(true).truncate(true)` (`src/recording_log.rs:474-479`). After a crash during session 1, the next daemon process starts again at session 1; the next `Start` truncates `capture-1.listenerlog` before any recovery/export path sees it.

This means prior finding 2 is only partially resolved. Record-level persistence is much better than the previous clean-stop-only behavior, but the active capture is not yet end-to-end crash-resilient at the component lifecycle level. The accepted durable write can still be destroyed by the normal restart-and-start path.

Expected correction: make active capture artifact allocation non-colliding across process restarts and forbid overwrite of existing capture logs. A minimal fix would use `create_new(true)` or equivalent exclusive creation, a session identifier that is monotonic or globally unique across restarts, and a test that simulates a pre-existing `capture-1.listenerlog` before constructing a fresh runtime. A complete vertical-slice fix should also define how orphaned complete or torn logs are discovered and recovered/exported after daemon restart rather than relying only on in-memory `Stop`.

## Prior Finding Status

Prior finding 1, daemon transport did not use exported `signal_listener::Frame`: resolved.

Evidence: `src/transport.rs:7` imports `signal_listener::{Frame, FrameBody, Input, Output}`; `ContractFrameCodec::read_frame` reads the big-endian `u32` length prefix then calls `Frame::decode_length_prefixed` (`src/transport.rs:42-45`, `55-65`); `write_frame` uses `frame.encode_length_prefixed()` (`src/transport.rs:47-52`); server request admission accepts only `FrameBody::Request` (`src/transport.rs:89-105`); replies are emitted with `output.into_reply_frame(request.exchange())` (`src/transport.rs:220-222`). The runtime test `socket_server_answers_public_status_frame_with_matching_exchange` proves a public status request frame round-trips through the socket server with the same `ExchangeIdentifier` (`tests/runtime.rs:300-350`).

Prior finding 2, active capture clean-stop durable only, not continuously crash-resilient: partially resolved.

Resolved portion: active capture now writes a single growing `.listenerlog` during capture, not just on stop. `RecordingLogWriter::create_with_durability` writes and syncs the header, then fsyncs the parent directory (`src/recording_log.rs:474-492`). `append_record` writes a bounded frame-aligned payload record with header, payload, trailer, then calls the durability commit (`src/recording_log.rs:495-563`); the default policy flushes and `sync_data`s (`src/recording_log.rs:434-443`). The capture writer appends complete frame-aligned chunks as input arrives (`src/capture.rs:259-270`, `293-305`). Recovery accepts only the valid prefix and truncates the first incomplete or corrupt tail (`src/recording_log.rs:629-653`, `800-868`).

Unresolved portion: the daemon lifecycle can overwrite crash-survived logs after restart, as described in the High finding above.

## Acceptability

Listener is acceptable for a normal-path manual vertical slice under narrow caveats: start capture, keep the daemon alive, stop capture, recover/export raw PCM, batch-transcribe, and deliver to clipboard. It is not yet acceptable as the full crash-resilient vertical slice because a daemon restart followed by another start can erase the prior active recording log.

Caveats for use:

- Do not treat crash survival as complete until artifact allocation is non-overwriting and restart recovery is defined.
- Ordinary Start/Stop state conflicts still return `RequestUnimplemented(NotBuiltYet)` through the catch-all error mapping (`src/runtime.rs:55-65`, `229-252`); this remains the known next item from the first audit.
- If post-stop recovery/export/transcription fails, the current public reply still collapses through the same `RequestUnimplemented` path rather than returning a typed stopped-with-artifact failure outcome.

## Checked Evidence

Files and guidance consulted:

- `/git/github.com/LiGoldragon/listener/AGENTS.md`
- `/git/github.com/LiGoldragon/listener/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/listener/README.md`
- `/git/github.com/LiGoldragon/listener/Cargo.toml`
- `/git/github.com/LiGoldragon/listener/src/transport.rs`
- `/git/github.com/LiGoldragon/listener/src/client.rs`
- `/git/github.com/LiGoldragon/listener/src/daemon.rs`
- `/git/github.com/LiGoldragon/listener/src/runtime.rs`
- `/git/github.com/LiGoldragon/listener/src/capture.rs`
- `/git/github.com/LiGoldragon/listener/src/recording_log.rs`
- `/git/github.com/LiGoldragon/listener/src/transcription.rs`
- `/git/github.com/LiGoldragon/listener/src/delivery.rs`
- `/git/github.com/LiGoldragon/listener/src/error.rs`
- `/git/github.com/LiGoldragon/listener/tests/runtime.rs`
- `/git/github.com/LiGoldragon/listener/tests/capture.rs`
- `/git/github.com/LiGoldragon/listener/tests/recording_log.rs`
- `/git/github.com/LiGoldragon/listener/tests/configuration.rs`
- Named doctrine: component architecture, contract repo, micro-components, Rust crate layout, Rust methods, Rust errors, testing, design quality, plus Nix and Jujutsu usage guidance for the commands actually run.

Spirit evidence: read-only public text searches for Listener-specific intent found no matching Listener record. A privacy constraint record (`k09z`) was observed but was not material to this public repo audit. The task brief’s approved Listener intent and constraints remained the controlling scope.

Commands run:

- `jj status` in `/git/github.com/LiGoldragon/listener`: working copy had no changes; parent commit was `5ee86c8e` on `main`.
- `cargo fmt --check`: passed.
- `cargo test`: passed; 9 integration tests passed across capture, configuration, recording log, and runtime tests.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix flake check`: passed locally. It reported app `meta` attributes missing for the flake apps and omitted `aarch64-linux`, but all local checks passed.

Additional source searches:

- No Whisrs/Whisper dependency or extension was found in the Listener repo.
- No `sync_file_range` use was found.
- No segment-rotation path was found.
- Default capture uses `parecord --device=@DEFAULT_SOURCE@`, so the implementation follows the system default source rather than hard-binding a removable node (`src/capture.rs:135-147`).

## Residual Next Work

1. Fix the restart overwrite risk with non-colliding capture artifacts, exclusive log creation, and a restart/orphan recovery witness test.
2. Add typed ordinary Start/Stop conflict replies in the `signal-listener` contract and lower `CaptureAlreadyActive`, `NoActiveCapture`, and `CaptureSessionMismatch` to those domain outcomes instead of `RequestUnimplemented(NotBuiltYet)`.
3. Decide whether post-stop failures should return a typed stopped/recovered-artifact outcome with transcription or delivery failure details, so a caller is not left with a generic unimplemented reply after capture has already been stopped.
4. Consider syncing the parent directory after raw PCM export creation if the export itself becomes a durable handoff artifact rather than a regenerable stop-time view.
