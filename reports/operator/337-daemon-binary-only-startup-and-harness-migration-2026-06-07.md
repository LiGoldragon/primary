# Operator Report 337 — Daemon Binary-Only Startup and Harness Migration

Date: 2026-06-07

## Summary

The daemon boundary is now implemented in the shared runtime and in the
recently touched harness path: daemons do not accept inline NOTA or `.nota`
startup/configuration files. They accept one pre-generated signal/rkyv startup
message/file. NOTA stays at CLI, authoring, deploy-tool, test, and report/debug
text edges.

Intent anchors:

- `pjvv` — daemons cannot understand or decode NOTA text; startup,
  configuration, and peer traffic are binary signal/rkyv surfaces.
- `ur16` — the virgin-daemon bootstrap model is ratified: a daemon's startup
  argument is a pre-generated rkyv Configure message, bootstrap depends on no
  manager, and restart self-resumes from persisted SEMA state.

## Implemented

`triad-runtime` main:

- `ComponentCommand::signal_file_argument()` rejects inline text and existing
  `.nota` paths before component-specific decode.
- The argument tests now pin `.nota` rejection for daemon startup.
- `INTENT.md` and `ARCHITECTURE.md` state the split: text clients use the NOTA
  classifier; daemons use the signal-file classifier.

Commit: `cdda1b1f` — `triad-runtime: reject NOTA daemon startup arguments`.

`signal-harness` main:

- `HarnessDaemonConfiguration` remains NOTA-round-trippable for authoring and
  tooling, but docs and source comments now state the live daemon consumes it
  only as binary rkyv.

Commit: `46b0f679` — `signal-harness: mark daemon startup as binary-only`.

`harness` main:

- `harness-daemon` no longer uses `nota_config::ConfigurationSource`.
- New `HarnessDaemonCommand` owns the process argument and calls
  `ComponentCommand::signal_file_argument()`.
- New `HarnessDaemonConfigurationFile` reads/writes binary rkyv startup
  configuration.
- Tests now prove binary config acceptance plus inline NOTA and `.nota`
  rejection.
- The strict real e2e now launches `harness-daemon` with `harness.rkyv` while
  preserving the same real message -> router -> harness -> reply -> message
  round trip.

Commit: `50a4f764` — `harness: require binary daemon startup configuration`.

Primary guidance:

- `AGENTS.md`, `ESSENCE.md`, `INTENT.md`, `skills/component-triad.md`,
  `skills/spirit-cli.md`, `skills/intent-log.md`, `skills/nota-comments.md`,
  and `skills/contract-repo.md` were updated away from daemon-NOTA wording.
- Report 336 was corrected: the daemon argument question is resolved, not open.

## Verification

`triad-runtime`:

- `cargo test` — passed.
- `cargo clippy --all-targets --all-features -- -D warnings` — passed.

`signal-harness`:

- `cargo test` — passed, 31 tests.
- `cargo clippy --all-targets --all-features -- -D warnings` — passed.

`harness`:

- `cargo test` — passed, including the message/router/harness e2e.
- `cargo clippy --all-targets --all-features -- -D warnings` — passed.
- Focused witness: `cargo test --test daemon` — 15 passed, including
  `harness_daemon_configuration_rejects_inline_nota_argument` and
  `harness_daemon_configuration_rejects_nota_file_argument`.
- Focused e2e: `cargo test --test message_router_harness_e2e -- --nocapture`
  — one real `message` CLI sends to another harness instance, that receiver
  replies through its real `message` CLI, and the reply returns to the first
  harness.

## Remaining Drift

This slice fixed the shared runtime and the active harness path. Older
hand-written daemon entrypoints still need migration when their component port
is picked up. Earlier grep found likely legacy NOTA startup paths in
`router`, `system`, `cloud`, `introspect`, `domain-criome`,
`repository-ledger`, and old production `persona-spirit` surfaces. The new
rule for each migration is clear: replace daemon-side NOTA config parsing with
the emitted/shared binary startup path, and keep authored NOTA only in the tool
that pre-generates the rkyv startup message.

Router remains legacy in the current message/harness e2e: the test still writes
`router.nota` because router's daemon has not yet been moved to the binary-only
startup path in this slice. That is the next concrete component to clean after
harness because it is already in the real message-passing e2e.
