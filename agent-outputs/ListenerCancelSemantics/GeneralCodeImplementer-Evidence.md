# Listener Cancel Semantics Implementation Evidence

## Task And Scope

Tracker item: `primary-zddv.2`.

Implemented typed Listener cancel semantics across the ordinary public contract,
Listener CLI, runtime lowering, status stream, tests, and docs. Scope stayed out
of CriomOS-home shortcuts, OS bindings, deployment, live microphone smoke tests,
OpenAI live calls, clipboard inspection, transcript content, audio contents, and
secrets.

## Context Consulted

- `/home/li/primary/agent-outputs/ListenerUsabilityFixes/TrackerWeaver-WorkGraph.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/RustAuditor-ReAudit.md`
- `/home/li/primary/agent-outputs/ListenerInternalTranscriptionStatus/Scout-SituationalMap.md`
- `bd show primary-zddv.2`
- Listener and signal-listener `AGENTS.md`, `ARCHITECTURE.md`, `README.md`,
  and repo `skills.md`

## Repos And Commits

Changed and pushed:

- `/git/github.com/LiGoldragon/signal-listener`
  - `9fce56075ed93381bfe897444f6207c9dd3f73ab`
  - `signal-listener: add typed cancel operation (Codex GPT-5)`
- `/git/github.com/LiGoldragon/listener`
  - `a4f1c28191cce8022a27732d98d938177f220769`
  - `listener: add typed cancel capture path (Codex GPT-5)`

Not changed:

- `/git/github.com/LiGoldragon/meta-signal-listener`
- CriomOS-home shortcut or widget configuration

## Files Changed

signal-listener:

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `build.rs`
- `schema/lib.schema`
- `src/lib.rs`
- `src/schema/lib.rs`
- `tests/round_trip.rs`

listener:

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `src/command.rs`
- `src/runtime.rs`
- `src/status.rs`
- `tests/runtime.rs`

## Behavior Added

Public contract:

- Added `Input::Cancel(CancelCapture)` and `OperationKind::Cancel`.
- Added `Output::Cancelled(CaptureCancelled)`.
- `CaptureCancelled` carries `CancelledSession` and `DurableAudioArtifact`.
  It carries no transcript text and no delivery outcomes.
- Existing typed conflict replies are reused for cancel:
  `NoActiveCapture` for idle cancel and `CaptureSessionMismatch` for
  wrong-session cancel.
- `RequestUnimplemented` can now report `OperationKind::Cancel` for
  implementation failures outside lifecycle conflicts.

CLI:

- Added `listener cancel <session>`.
- The CLI lowers cancel directly to the typed `signal-listener` cancel input.
  It does not parse daemon status strings or use OS shell text as the command
  surface.

Runtime:

- Cancel takes the active capture through the same active-capture shutdown path
  as stop, so the capture process/writer is stopped and the `.listenerlog`
  remains durable.
- Cancel returns the retained durable artifact in `Cancelled`.
- Cancel intentionally does not run `RecordingLog::recover`, does not export the
  normal stop-time raw PCM transcription input, does not call
  `BatchTranscriber::transcribe`, and does not call output delivery.
- Normal Start, Stop, Status, stop-time transcription, delivery behavior,
  exchange identity, typed conflict replies, internal OpenAI actor construction,
  and status socket privacy are preserved.

Status:

- Added local UI-safe status state `cancelled`.
- Status JSON remains only `state` and `level`; cancelled frames are shaped as a
  state-only terminal event with silent level.
- `cancelled`, like copied and error, returns to idle after the status stream's
  terminal-event delay.
- No transcript text is added to the status stream.

Versioning:

- `signal-listener` bumped from `0.3.0` to `0.4.0` because the public contract
  gained a new operation and reply.
- `listener` bumped from `0.4.0` to `0.5.0` because the CLI/runtime behavior and
  public contract dependency changed.

## Proof Points

Focused cancel test coverage in `listener/tests/runtime.rs` proves:

- active cancel returns `Output::Cancelled`;
- the returned session matches the active session;
- the returned artifact matches the active `.listenerlog`;
- the retained `.listenerlog` is recoverable/exportable after cancel;
- the normal stop-time raw PCM export path is absent after cancel;
- no transcription input was sent;
- no delivery target was invoked;
- public status returns idle after cancel;
- status events include `cancelled`;
- status events do not include transcript-shaped fields or transcript text;
- cancel does not publish transcribing or copied status;
- idle cancel returns `NoActiveCapture`;
- wrong-session cancel returns `CaptureSessionMismatch` and preserves the active
  capture.

Contract tests prove cancel request/reply binary and NOTA round trips, plus
`Input::operation_kind()` for `Cancel`.

CLI unit coverage proves `listener cancel <session>` builds typed
`Input::Cancel`.

## Checks Run

In `/git/github.com/LiGoldragon/signal-listener`:

- `SIGNAL_LISTENER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --all-features`
  passed and regenerated `src/schema/lib.rs`.
- `cargo fmt --check` passed.
- `cargo test --test round_trip --all-features` passed.
- `cargo test --all-features` passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix flake check --no-build --print-build-logs` passed as evaluation
  evidence.
- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy
  .#checks.x86_64-linux.fmt --no-link --print-out-paths` passed.

In `/git/github.com/LiGoldragon/listener`:

- `cargo fmt --check` passed.
- `cargo test --test runtime cancel_stops_capture_retains_artifact_and_skips_transcription_and_delivery`
  passed.
- `cargo test command::tests::cancel_command_builds_typed_cancel_input` passed.
- `cargo test --test runtime` passed.
- `cargo test` passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix build .#checks.x86_64-linux.test .#checks.x86_64-linux.clippy
  .#checks.x86_64-linux.fmt --no-link --print-out-paths` passed.

## Blockers And Follow-Up

No implementation blocker remains for `primary-zddv.2`.

Recommended audit scope for `primary-zddv.5`:

- verify contract compatibility and additive wire versioning;
- verify `listener cancel <session>` reaches the daemon through the typed
  contract;
- verify cancel cannot reach transcription/OpenAI/clipboard paths;
- verify retained artifact behavior and status event shape;
- verify normal Start/Stop/Status behavior and exchange identity remain intact;
- include `primary-zddv.3` live-level changes if that item lands before the
  audit.

Follow-up owner:

- `primary-zddv.4` should wire OS shortcuts after choosing the safer record
  binding and can target `listener cancel <session>` without fragile shell
  status parsing.
