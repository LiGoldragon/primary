# Listener Runtime Implementation Evidence

## Task And Scope

Implemented approved tracker item `primary-qvud.4` in `/git/github.com/LiGoldragon/listener`.

Scope was limited to the runtime repo. Contract repos and the primary manifest were not edited. The implementation consumes the pushed `signal-listener` `0.2.0` contract at `e2a390b0` and `meta-signal-listener` `0.2.0` at `30ed2770`.

## Consulted Context

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/lore/AGENTS.md`
- `/git/github.com/LiGoldragon/listener/AGENTS.md`
- `/git/github.com/LiGoldragon/listener/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/listener/README.md`
- `/git/github.com/LiGoldragon/listener/skills.md`
- `/git/github.com/LiGoldragon/signal-listener/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-listener/src/schema/lib.rs`
- `/git/github.com/LiGoldragon/signal-listener/schema/lib.schema`
- Named doctrine loaded: component architecture, micro-components, Rust crate layout, Rust methods, Rust errors, naming, typed records over flags, contract repo, testing, code implementation, repo intent, Nix usage, edit coordination, version control, repository closeout.

## Changed Files

- `ARCHITECTURE.md`
- `README.md`
- `Cargo.toml`
- `Cargo.lock`
- `src/lib.rs`
- `src/error.rs`
- `src/configuration.rs`
- `src/command.rs`
- `src/daemon.rs`
- `src/capture.rs`
- `src/client.rs`
- `src/delivery.rs`
- `src/runtime.rs`
- `src/transcription.rs`
- `src/transport.rs`
- `tests/configuration.rs`
- `tests/runtime.rs`

## Implemented Behavior

- Added daemon-owned `ListenerRuntime` that handles `signal_listener::Input::{Start, Stop, Status}` and returns the structured `signal_listener::Output` contract replies.
- Added a blocking Unix-socket daemon server that receives length-prefixed `signal-listener` contract frames and sends length-prefixed contract replies.
- Updated the ordinary `listener` CLI to remain thin: it parses `start`, `stop <session>`, and `status`, sends a contract request to the daemon socket, and prints the contract reply.
- Added default environment-derived configuration with `OutputTargets::new(vec![OutputTarget::SystemClipboard])`.
- Added capture state and status reporting. `Status` returns `Idle` or `Capturing(ActiveCapture)` with the active session and durable artifact.
- Added process-backed capture using a parecord-compatible command. Default command is `parecord --device=@DEFAULT_SOURCE@ --raw --format=s16le --rate=16000 --channels=1`; stdout is streamed by the daemon into the durable artifact file as bytes arrive, without buffering the recording in RAM.
- Added a narrow `AudioCaptureBackend` / `ActiveAudioCapture` seam for later replacement or Whisrs harvesting.
- Added a narrow `BatchTranscriber` seam. `LISTENER_TRANSCRIPTION_PROGRAM` runs a batch command with the artifact path and uses stdout as transcript text. Without that variable, `HonestStubTranscriber` returns explicit not-configured text and does not claim real speech recognition.
- Added typed output-target dispatch. `OutputTargetDispatcher` currently handles `SystemClipboard` via `LISTENER_CLIPBOARD_PROGRAM` or default `wl-copy`, and returns one `DeliveryOutcome` per configured target.
- Updated docs from scaffold status to first vertical-slice status and documented environment knobs.

## Verification

All checks were run in `/git/github.com/LiGoldragon/listener`.

- `cargo fmt --check`: passed.
- `cargo test`: passed; includes configuration round-trip plus runtime tests for active durable artifact write before stop, stop result shape, output-target dispatch, and socket contract-frame status handling.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix flake check --print-build-logs`: passed for the supported local system set. Nix reported that `aarch64-linux` was omitted as incompatible in this run.

## Commit And Push

- Commit: `c2f5e33e6c2b` (`listener: implement first speech slice`)
- Bookmark: `main`
- Push: `main@origin` is at `c2f5e33e6c2b`
- Post-push status: clean working copy with empty `@` on top of `main`.

## Remaining Stubbed Or Configuration-Dependent Pieces

- Real speech recognition is configuration-dependent. Set `LISTENER_TRANSCRIPTION_PROGRAM` to a batch backend command; otherwise the daemon returns an explicit stub transcript.
- Clipboard delivery is configuration-dependent on `wl-copy` by default, or `LISTENER_CLIPBOARD_PROGRAM`.
- Capture depends on a parecord-compatible command available in the daemon environment. `LISTENER_CAPTURE_PROGRAM` can point at a compatible replacement.
- The daemon supports one active capture and a blocking local socket loop. Supervision, richer error contracts, multi-output contract variants, and later safeguards remain out of scope for this tracker item.

## Manual Microphone And Clipboard Test

1. Pick an isolated runtime and store:

   ```sh
   export LISTENER_SOCKET="$XDG_RUNTIME_DIR/listener-manual.sock"
   export LISTENER_CAPTURE_STORE="$HOME/.local/state/listener/manual-captures"
   export LISTENER_STUB_TRANSCRIPT="manual listener stub transcript"
   ```

2. Start the daemon in one terminal:

   ```sh
   cargo run --bin listener-daemon
   ```

3. In another terminal:

   ```sh
   cargo run --bin listener -- status
   cargo run --bin listener -- start
   cargo run --bin listener -- status
   cargo run --bin listener -- stop 1
   ```

4. Confirm the stop reply contains the durable artifact path, the explicit stub transcript unless a real `LISTENER_TRANSCRIPTION_PROGRAM` is configured, and one delivery outcome for `SystemClipboard`.

5. Confirm the artifact file exists under `LISTENER_CAPTURE_STORE` and that the clipboard contains the transcript if the clipboard command is available.
