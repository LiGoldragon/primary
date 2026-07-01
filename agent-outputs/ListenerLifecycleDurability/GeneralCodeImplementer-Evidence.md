# Listener Lifecycle Durability Evidence

## Task And Scope

Fixed the Listener runtime durability bug where a daemon restart could allocate
`capture-1.listenerlog` again and truncate a crash-survived active recording.
Scope was limited to `/git/github.com/LiGoldragon/listener`; no contract repos
were edited.

## Consulted

- Local repo guidance: `AGENTS.md`, `ARCHITECTURE.md`, `README.md`,
  `skills.md`.
- Workspace guidance available in-session: primary `AGENTS.md`, lore
  `AGENTS.md`, and the named component/Rust/Nix/testing doctrines.
- Source paths: `src/runtime.rs`, `src/capture.rs`, `src/recording_log.rs`,
  `src/error.rs`, `src/lib.rs`, `tests/runtime.rs`,
  `tests/recording_log.rs`.

The lore-referenced workspace intent document and canonical orchestration
protocol were not present at the expected local paths; Orchestrate itself was
available and the Listener repository was claimed before writes.

## Files Changed

- `ARCHITECTURE.md`
- `README.md`
- `src/capture.rs`
- `src/error.rs`
- `src/lib.rs`
- `src/recording_log.rs`
- `src/runtime.rs`
- `tests/recording_log.rs`
- `tests/runtime.rs`

## Implemented Behavior

- `RecordingLogWriter` now opens new logs with exclusive creation
  (`create_new(true)`) and maps existing-path collisions to
  `Error::RecordingLogAlreadyExists`.
- `CaptureStore` discovers existing `*.listenerlog` paths, computes the next
  session value after existing `capture-<session>.listenerlog` names, and
  recovers regular-file logs through the existing idempotent recording-log
  recovery scanner.
- `ListenerRuntime::start` prepares the store, recovers idle orphan logs,
  advances the session sequence above discovered artifacts, and starts the next
  available capture.
- If exclusive creation reports a racing artifact collision, the runtime scans
  existing artifact names again and retries with the next session instead of
  failing or overwriting.
- `ListenerRuntime::status` performs the same orphan discovery/recovery while
  idle. It does not recover while this runtime has an active capture, so it does
  not truncate the current active writer's file.
- The public `signal-listener` frame shape is unchanged. Runtime library code
  exposes recovered orphan logs through `ListenerRuntime::orphaned_recordings`
  for notice and later export using the existing `RecoveredRecordingLog`
  surface.

## Tests Added

- `tests/recording_log.rs`:
  `create_refuses_existing_listenerlog_without_truncating`.
- `tests/runtime.rs`:
  `fresh_runtime_start_preserves_existing_listenerlog_and_allocates_next_artifact`.
- `tests/runtime.rs`:
  `start_retries_when_artifact_appears_after_allocation`.
- `tests/runtime.rs`:
  `idle_status_recovers_orphaned_listenerlog_idempotently_and_leaves_it_exportable`.

## Verification

- `cargo fmt`: passed.
- `cargo test --test runtime start_`: passed.
- `cargo test --test runtime idle_status_recovers_orphaned_listenerlog_idempotently_and_leaves_it_exportable`: passed.
- `cargo test --test recording_log create_refuses_existing_listenerlog_without_truncating`: passed.
- `cargo test`: passed.
- `cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `nix flake check`: passed. The command reported the expected dirty-tree
  warning during validation, app metadata warnings for the existing flake apps,
  and omitted incompatible `aarch64-linux` checks.

## Commit And Push

- Commit: `2aaca2d4` (`listener: preserve crash-survived capture logs`).
- `main` was moved to the commit.
- `jj git push --bookmark main` completed; a follow-up push reported
  `main@origin` already matches `main`.

## Remaining Durability Caveats

- Orphan discovery is intentionally minimal: it recovers logs and keeps them
  available through the runtime library surface, but no new public Start/Stop
  conflict replies or wire-level orphan-reporting contract were added.
- Session allocation remains based on existing `capture-<session>.listenerlog`
  names in the capture store. Removing old artifacts can allow lower session
  numbers to be reused later, but not while a same-named artifact exists.
