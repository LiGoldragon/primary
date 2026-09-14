# Messenger fixture integration

## Merged state

On 2026-09-14 the living directed: “test it again in a sandbox, merge, and then try to explain to me what deployment you think would look like” (`flows/6cc91b/log.md:71-73`). The three fixture branches were tested in isolated worktrees and merged without conflicts, in dependency order:

- `signal-message` main: `65d6e2e2fafe` merges fixture commit `5b932140b8c7` (`TypedPromptEnvelope` contract).
- `meta-signal-message` main: `9876f4ef62e8` merges fixture commit `11aca640423f` (the direct `signal-message` pin at `5b932140…`).
- `message` main: `735847c31ffb` merges fixture head `220bef242ab1` (durable relay, migration, and tests).

The Message manifest pins both producer commits by immutable public Git revision (`message/Cargo.toml:35-37`). The relay types belong to the producer contract: `PromptVariant`, `SourceEventIdentifier`, `RawPromptText`, interpretation selection, and `TypedPromptEnvelope` are declared in `signal-message/ethos/signal.ethos:5` and generated in `src/generated/signal.rs:456-479`.

## Sandbox evidence

All commands ran from the three isolated `messenger-fixture-34d94e` worktrees after their main merges.

- `signal-message`: `cargo test --all-targets --all-features` passed 3 contract tests.
- `meta-signal-message`: `cargo test --all-targets --all-features` passed 4 contract tests.
- `message`: `cargo test --all-targets --all-features` passed 29 tests, including 7 relay-fixture cases and 2 migration cases.
- Message Nix evaluation: `nix eval --no-write-lock-file --raw '.#checks.x86_64-linux.default.drvPath'` exited 0 with `/nix/store/g79fi2kiww32blng5m62zdx5fh1z8q9z-message-test-0.12.0.drv`.
- Message Nix build: `nix build --no-write-lock-file --max-jobs 0 '.#checks.x86_64-linux.default'` exited 0. It built remotely on the configured `ssh-ng://nix-ssh@prometheus.goldragon.criome` builder and returned the `message-test-0.12.0` result. `--max-jobs 0` prevented a local build.

The relay fixture demonstrates immutable raw text and origin, stable destination/event dedupe and conflict rejection, peer/receipt recording without forwarding, Busy and Dirty persistence without bytes, reopen behavior, ambiguous-write non-retry, and separate byte acceptance from recipient observation (`message/tests/relay_fixture.rs`). Migration tests preserve a genuine v4 ledger catalogue/row while adding the relay table (`message/src/tables.rs:847-936`).

## What merged does and does not deploy

`message` version `0.12.0` is source/package metadata (`message/Cargo.toml:1-8`). It does not say the currently running host unit was upgraded. This merge did not restart or activate any unit.

The existing `message-daemon` starts from one binary configuration path (`message/src/bin/message_daemon.rs:5-19`), opens ordinary and owner Unix listeners from that configuration (`message/src/daemon.rs:55-76`), and keeps its durable store path in that configuration (`message/src/config.rs:15-70`). The normal command still submits the existing producer `Query` through `MESSAGE_SOCKET` (`message/src/command.rs:36-39`). The fixture relay is an exported, reusable `Relay` with an injected `DeliveryPort` (`message/src/relay.rs:50-81`); it is not called by `Engine::submit`, the daemon, or either existing listener.

A later opt-in deployment would need a separately registered harness ingress or relay process that obtains its process identity from the existing Message origin policy, constructs the producer-owned typed envelope, opens the configured `messenger.sema`, and supplies one permitted destination `DeliveryPort`. The record must be admitted before readiness or a write; `InFlight`/`Unknown` mean it cannot retry an ambiguous write automatically (`message/src/relay.rs:57-80`). A `ByteAccepted` result is only the port write outcome; `recipient_observed` is a later explicit state transition (`message/src/relay.rs:84-90`).

The typed variant is routing data. The process connection determines `MessageOrigin` in the existing provenance policy (`message/src/provenance.rs:57-67`); this fixture does not establish that a caller-declared `HumanPrompt` is cryptographic proof of human origin. A live hook must therefore register the harness/relay process separately and be reviewed for the boundary between typed kind and process who.

No hook, service unit, socket, configuration writer invocation, terminal-cell attachment, or automatic forwarding is included in this merge. Those are the remaining implementation and deployment decisions for the separate integrated-path task.
