# Listener Contract Vertical Slice Evidence

## Task And Scope

Implemented approved tracker items `primary-qvud.2` and `primary-qvud.3` for the Listener contract family.

Owned repos edited:

- `/git/github.com/LiGoldragon/signal-listener`
- `/git/github.com/LiGoldragon/meta-signal-listener`

Repo explicitly not edited:

- `/git/github.com/LiGoldragon/listener`

Approved scope kept narrow: start, stop, status/reporting for one active capture session; durable audio artifact path; transcript text; typed delivery targets and delivery outcomes. Deferred safeguards such as redundant capture, Bluetooth disconnect handling, silence alarms, watchdogs, alerts, and typing into a window were not added.

## Context Consulted

- Primary workspace `AGENTS.md` supplied in the dispatch.
- Local repo guidance: `AGENTS.md`, `skills.md`, `ARCHITECTURE.md`, `README.md`, `Cargo.toml`, `flake.nix`, `schema/lib.schema`, `build.rs`, `src/lib.rs`, and `tests/round_trip.rs` in both repos.
- Loaded doctrine: contract-repo, micro-components, rust-crate-layout, rust-methods, rust-errors, naming, typed-records-over-flags, versioning, edit-coordination, version-control, code-implementation, testing, repository-closeout.
- Coordination: claimed both repo roots with Orchestrate lane `contract-implementation-worker`; no prior claims overlapped either repo.

## Changed Files

### signal-listener

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `build.rs`
- `schema/lib.schema`
- `src/lib.rs`
- `src/schema/lib.rs`
- `tests/round_trip.rs`

### meta-signal-listener

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `build.rs`
- `tests/round_trip.rs`

`meta-signal-listener/src/schema/lib.rs` did not change because the meta schema imports `signal_listener::ListenerDaemonConfiguration` by alias; the imported type changed in `signal-listener`.

## Final Contract Shape

`signal-listener` is now version `0.2.0`.

Ordinary operations:

- `Start(StartCapture)`
- `Stop(StopCapture)`
- `Status(StatusRequest)`

Ordinary replies:

- `Started(CaptureStarted)`
- `Stopped(CaptureStopped)`
- `StatusReported(CaptureStatusReport)`
- `RequestUnimplemented(RequestUnimplemented)`

Configuration now carries `OutputTargets(Vector OutputTarget)` instead of a single `OutputTarget`. `OutputTarget` currently has `SystemClipboard` as the first supported target and can later grow typed variants such as a Mentci target without boolean flags or string dispatch.

`CaptureStopped` now carries:

- `StoppedSession`
- `DurableAudioArtifact(AudioArtifactPath(WirePath))`
- `TranscriptText`
- `DeliveryOutcomes(Vector DeliveryOutcome)`

`DeliveryOutcome` is a typed enum:

- `Delivered(DeliveredTo(OutputTarget))`
- `Failed(DeliveryFailure { target: OutputTarget, reason: DeliveryFailureReason })`

`StatusReported` carries `CaptureStatusReport(CaptureStatus)`, where `CaptureStatus` is either `Idle` or `Capturing(ActiveCapture)`. `ActiveCapture` names the active session and the durable audio artifact being written.

`meta-signal-listener` is now version `0.2.0`; its build expects `signal-listener` schema version `0.2.0`, and its lockfile points at pushed `signal-listener` commit `e2a390b0`.

## Verification

### signal-listener

- `SIGNAL_LISTENER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --all-features` passed.
- `cargo fmt --check` initially failed on import wrapping; `cargo fmt` applied; rerun passed.
- `cargo test --features nota-text --test round_trip` passed: 4 tests.
- `cargo test --all-features` passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix flake check` passed for `x86_64-linux`; Nix reported `aarch64-linux` omitted as an incompatible system.

### meta-signal-listener

- `cargo update -p signal-listener` updated the lockfile to the pushed ordinary contract.
- `META_SIGNAL_LISTENER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --all-features` passed.
- `cargo fmt --check` passed.
- `cargo test --features nota-text --test round_trip` passed: 3 tests.
- `cargo test --all-features` passed.
- `cargo clippy --all-targets --all-features -- -D warnings` passed.
- `nix flake check` passed for `x86_64-linux`; Nix reported `aarch64-linux` omitted as an incompatible system.

## Commit And Push Status

`signal-listener`:

- Commit: `e2a390b0` (`signal-listener: define vertical slice contract`)
- Bookmark: `main`
- Push: `jj git push --bookmark main` completed successfully.
- Final status: clean working copy.

`meta-signal-listener`:

- Commit: `30ed2770` (`meta-signal-listener: consume listener vertical slice contract`)
- Bookmark: `main`
- Push: `jj git push --bookmark main` completed successfully.
- Final status: clean working copy.

## Runtime Worker Notes

- Use `ListenerDaemonConfiguration.output_targets` as the configured delivery target list. For the first vertical slice, populate it with `OutputTargets::new(vec![OutputTarget::SystemClipboard])`.
- `Start` should create one daemon-owned active capture session and begin continuously writing to a durable audio artifact path. The current `Started` reply returns the session; `Status` exposes the active session plus artifact path while capture is running.
- `Stop` should close the session, finish the durable audio artifact, run batch transcription, deliver the transcript to each configured output target, and return `Stopped` with the artifact path, transcript text, and one `DeliveryOutcome` per attempted target.
- Delivery failure is represented inside `DeliveryOutcome::Failed`; it does not require stringly errors or a new boolean field.
- The contract does not add out-of-scope reliability safeguards; runtime implementation should not infer watchdog, alert, RMS/silence, Bluetooth guard, redundant-track, or active-window typing requirements from this contract.

## Blockers And Unknowns

No blockers remain for the contract handoff. The runtime still needs to choose concrete durable artifact naming and audio format policy inside `/git/github.com/LiGoldragon/listener`; that is intentionally outside this contract change.
