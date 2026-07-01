# Rust Auditor Review - Listener Lifecycle Durability Fix

## Task And Scope

Final targeted audit for Listener lifecycle durability fix at `/git/github.com/LiGoldragon/listener`.

Reviewed commit `2aaca2d44c0b0dc304a1756b69f6cc563e5e27e9` on `main`, change `listener: preserve crash-survived capture logs`.

Audit focus:

- whether the prior high lifecycle overwrite finding is resolved;
- regressions to the public signal frame boundary;
- record-level durability and recovery behavior;
- residual next work for first vertical slice readiness.

Spirit grounding: public `spirit` text searches for Listener crash/durable recording intent did not return a Listener-specific record. The approved intent and constraints in the brief were treated as governing. General design-review intent records observed were `10pz` and `t5qr`, supporting active design judgment but not adding Listener-specific requirements.

## Findings

No blocking or high-severity findings.

No public frame boundary regression found. The lifecycle fix commit touches only `ARCHITECTURE.md`, `README.md`, `src/capture.rs`, `src/error.rs`, `src/lib.rs`, `src/recording_log.rs`, `src/runtime.rs`, `tests/recording_log.rs`, and `tests/runtime.rs`; it does not touch `Cargo.toml`, `Cargo.lock`, `src/transport.rs`, or the `signal-listener` contract schema. Runtime still consumes and returns `signal_listener::Input` and `signal_listener::Output` in `src/runtime.rs:1`, and the socket boundary still encodes/decodes the shared `signal_listener::Frame` in `src/transport.rs:6`.

No record-level durability regression found in the audited path. `RecordingLogWriter::create_with_durability` creates logs with `create_new(true)` and maps `AlreadyExists` to typed `RecordingLogAlreadyExists` at `src/recording_log.rs:474`. Header creation is followed by the durability commit and parent directory fsync at `src/recording_log.rs:493` and `src/recording_log.rs:494`. Each payload record writes header, payload, trailer, then flushes and `sync_data`s through the durability policy at `src/recording_log.rs:549` and `src/recording_log.rs:553`. Recovery scans only valid records and truncates an incomplete/corrupt tail with `set_len` plus `sync_all` at `src/recording_log.rs:640`.

## Lifecycle Status

Status: lifecycle overwrite finding resolved.

The original high bug was that a restarted runtime reset session IDs and could reuse/truncate `capture-1.listenerlog`. The current code prevents that in two independent ways:

- Existing log paths are no longer opened with truncating creation. `RecordingLogWriter` uses exclusive creation at `src/recording_log.rs:474` and returns `RecordingLogAlreadyExists` at `src/error.rs:69`.
- Idle `start` first prepares the capture store, recovers existing logs, and advances the in-memory session sequence to at least the scanned next session value at `src/runtime.rs:79` and `src/runtime.rs:144`.
- Session allocation is derived from existing `capture-<session>.listenerlog` names in `src/capture.rs:194`, with generated artifact names in `src/capture.rs:98`.
- If a collision appears after allocation, `ListenerRuntime::start_next_available_capture` catches `RecordingLogAlreadyExists`, rescans the store, advances the sequence, and retries at `src/runtime.rs:171`.

The regression tests directly witness the fixed behavior:

- `tests/recording_log.rs:83` proves an existing listener log is refused without truncation.
- `tests/runtime.rs:294` proves a fresh runtime preserves `capture-1.listenerlog` and starts `capture-2.listenerlog`.
- `tests/runtime.rs:330` proves the allocation-to-create race retry path.
- `tests/runtime.rs:365` proves idle status recovery is idempotent and leaves the orphan exportable.

## Acceptability

Listener is acceptable as the first vertical slice under the stated caveats. The first-slice requirement to preserve active recordings across daemon/process restart without rotating tiny segment files is met for valid `.listenerlog` artifacts that have reached the durable header/record boundary.

The implementation is intentionally still a first vertical slice: conflicts and operational failures are still collapsed into `RequestUnimplemented` replies rather than a typed conflict vocabulary, and crash durability has not yet been tested against real OS/process-kill/power-failure scenarios.

## Residual Risks And Next Work

Typed Start/Stop conflict replies remain next work. `CaptureAlreadyActive`, `NoActiveCapture`, and `CaptureSessionMismatch` still become `RequestUnimplemented` through `Error::into_unimplemented_reply` in `src/runtime.rs:274`. That preserves the current public frame shape but is not the final typed lifecycle contract.

Real crash testing remains required. The tests prove logical recovery and fsync call placement, but not kernel/filesystem behavior across forced daemon kill, machine power loss, mount options, or device writeback. Add an OS-level harness that starts a real daemon, begins capture, kills the process at controlled points, restarts, and verifies the prior artifact is still present, not reused, and exportable.

The pre-header crash window is still an operational caveat. If a process dies after exclusive path creation but before a complete durable header, recovery will return `InvalidRecordingLog` rather than classify the file as an unrecoverable placeholder and advance past its `capture-<session>` name. That does not reintroduce overwrite, but it can make idle `start`/`status` report store unavailable until the artifact is handled. Real crash testing should decide whether to keep that operator-intervention policy or add an explicit invalid-orphan path that still advances session allocation.

Capture-store trust is assumed. The recovery scanner uses directory entries and ordinary `Path::is_file`/`File::open` behavior in `src/capture.rs:180` and `src/recording_log.rs:632`; if the capture directory is ever writable by another principal, add an explicit regular-file/no-symlink policy before recovery is allowed to mutate a path.

## Verification Evidence

Commands inspected or run from `/git/github.com/LiGoldragon/listener`:

- `spirit "(PublicTextSearch [Listener first vertical slice preserve active recordings crash daemon process listenerlog])"`: no Listener-specific intent returned.
- `spirit "(PublicTextSearch [active recordings crash preserve process daemon])"`: no Listener-specific intent returned.
- `orchestrate "(Observe Roles)"`: no active claim on the Listener repo observed.
- `jj status`: clean working copy, empty `@` child of `main`.
- `jj log -r 'main | @' --no-graph ...`: confirmed `main` at `2aaca2d4`, working copy empty child.
- `jj show --stat -r main`: confirmed pushed commit metadata and changed-file summary.
- `jj diff --name-only -r main`: confirmed changed files are the nine files named in the brief.
- `jj diff --git -r main Cargo.toml Cargo.lock`: empty output, confirming no dependency or lockfile changes in this commit.
- Source inspection of `src/recording_log.rs`, `src/capture.rs`, `src/runtime.rs`, `src/error.rs`, `src/lib.rs`, `src/transport.rs`, `tests/recording_log.rs`, `tests/runtime.rs`, `ARCHITECTURE.md`, and `README.md`.
- `cargo fmt --check`: passed.
- `cargo test --test recording_log --test runtime`: passed, 11 tests.
- `cargo test`: passed, 13 integration tests plus crate/bin/doc test targets.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix flake check`: passed. It evaluated package and check derivations and reported all checks passed; it emitted only app metadata warnings and the standard omitted `aarch64-linux` warning.
