# Terminal Emitted Daemon Migration — 2026-06-08

## Scope

Migrated the active `terminal-supervisor` process shell onto the shared
schema-rust-next / triad-runtime emitted daemon substrate. This is the
engine-facing terminal component process today; the older `terminal-daemon`
binary remains the one-PTY terminal-cell witness until the larger
terminal-cell consolidation lands.

## Landed Commits

- `signal-terminal` `e313a55f` — added meta socket path/mode to the binary
  `TerminalDaemonConfiguration`.
- `signal-terminal` `46c92b58` — documented that the launch record carries
  ordinary/meta/supervision sockets and is not a public operation.
- `terminal` `74ae5677` — emitted daemon module and process hook for
  `terminal-supervisor`.

## Implementation

- `terminal/build.rs` now emits `src/schema/daemon.rs` with a component-decoded
  working tier plus a meta tier.
- `terminal/src/config.rs` wraps `signal_terminal::TerminalDaemonConfiguration`
  and implements `triad_runtime::DaemonConfiguration`.
- `terminal/src/daemon.rs` implements `TerminalProcessDaemon` and
  `TerminalEngine`:
  - loads only binary rkyv configuration through the generated daemon command;
  - starts the existing supervision socket;
  - lazily starts the existing `TerminalSupervisor` actor;
  - decodes existing `signal-terminal` frames on the working socket;
  - decodes existing `meta-signal-terminal` frames on the meta socket;
  - forwards terminal worker lifecycle subscriptions through the shared
    length-prefixed async codec without converting back to std streams.
- `terminal/src/bin/terminal-supervisor.rs` now calls the generated
  `DaemonEntry`.

## Witnesses

- `tests/schema_generated.rs` asserts that `TerminalProcessDaemon` implements
  the generated `ComponentDaemon` surface and that the generated listener tiers
  are working/meta.
- `tests/terminal_supervisor.rs` now spawns a real `terminal-supervisor` binary
  from a binary rkyv config, verifies working/meta/supervision socket modes, and
  sends a real `meta-signal-terminal` `CreateSession` request through the meta
  socket. The current behavior honestly returns `MetaTerminalRequestUnimplemented`.
- The existing subscription test still passes and exercises snapshot-then-delta
  forwarding.
- `flake.nix` now keeps `schema/` in the clean Nix source so generated builds
  do not fail in the sandbox.

## Verification

In `signal-terminal`:

- `cargo fmt --check`
- `cargo test --all-targets --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`

In `terminal`:

- `cargo fmt --check`
- `TERMINAL_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --all-targets --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `nix build .#checks.x86_64-linux.terminal-supervisor-answers-component-supervision-relation --print-build-logs`

## Remaining

- The terminal meta behavior is still not built: `CreateSession` and
  `RetireSession` reach the meta socket and return typed `NotBuiltYet`.
- The durable end-state is still one consolidated `terminal-daemon` with
  internal terminal-cell session actors. This slice moved the active
  engine-facing process shell; it did not collapse the one-PTY witness binary.
- The async-runner commits named in system-operator report 204 exist locally,
  but current pushed `triad-runtime` and `schema-rust-next` main bookmarks are
  later router-era commits. Terminal therefore depends on the actual pushed
  main stack (`triad-runtime` `a3c92b68`, `schema-rust-next` `117bda3c`).
