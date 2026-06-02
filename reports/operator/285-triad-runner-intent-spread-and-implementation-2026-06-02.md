# Triad Runner Intent Spread And Implementation

*Kind: implementation report · Topics: spirit-next, schema-rust-next, triad-engine, daemon-runner, record-1419 · 2026-06-02*

## Intent Applied

Spirit record 1419 says triad wiring should move toward a programmatic
schema-generated substrate: daemon `main` should be tiny, domain logic should
live in non-default implementations of generated Signal / Nexus / SEMA engine
traits, Nexus owns heavier decisions, SEMA owns durable state/indexes, and
Signal owns communication.

## What Landed

`schema-rust-next` commit `dd944233`:

- Updated `INTENT.md` and `ARCHITECTURE.md` to record the generated component
  runner target.
- Kept the wording honest: runner emission is the next target, not a current
  code landing in `schema-rust-next`.

`spirit-next` commit `7c350679`:

- Added `DaemonCommand`, a data-bearing library noun that owns daemon startup
  argument handling, single binary configuration loading, and daemon
  construction.
- Reduced `src/bin/spirit-next-daemon.rs` to the allowed tiny entrypoint:
  construct `DaemonCommand::from_environment()` and run it.
- Added `tests/daemon_command.rs`, proving the command reads a real rkyv
  `Configuration` file and rejects missing/extra arguments.
- Updated `INTENT.md` and `ARCHITECTURE.md` to name `DaemonCommand` as the
  live step toward the generated runner and to clarify Nexus/SEMA/Signal
  ownership for topic-discovery-style algorithms.

The async subagent could not be freshly spawned because the harness thread
limit is still reached, so the same maintenance brief was queued to an
existing subagent. The main agent did not wait on it.

## Verification

Ran in `spirit-next`:

- `cargo test --test daemon_command`
- `cargo test --no-default-features`
- `cargo test --features nota-text`
- `cargo test --features nota-text,testing-trace`
- `cargo fmt --check`
- `cargo clippy --all-targets --features nota-text,testing-trace -- -D warnings`

No code changed in `schema-rust-next`, so no Rust test rerun was needed there.

## Current Focus

The next deeper implementation is still in `schema-rust-next`: emit a real
component-runner surface from schema data. `spirit-next::DaemonCommand` is a
manual pilot of the shape that a future generated runner should replace or
wrap.
