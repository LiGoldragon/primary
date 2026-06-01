# Spirit-next Testing Trace Implementation

*Kind: implementation closeout · Topics: spirit-next, testing-trace, live-architecture-witness, positive-grep-cleanup · 2026-06-01 · operator lane*

## Scope

Implemented the first safe slice of Spirit records 1343-1345 in `spirit-next`:
an optional `testing-trace` feature that emits structured runtime events from
the live Signal/Nexus/SEMA call path. The slice deliberately stays in-process;
the CLI-facing log socket and schema-rust generated trace nouns remain next
work.

## Changed Behavior

When `testing-trace` is enabled, tests can inject a recording `TraceLog` into
`Engine::new_with_trace`. Runtime calls emit typed `TraceEvent` values from:

- Signal admission of accepted input.
- Signal rejection for invalid input.
- Signal reply for accepted and rejected input.
- Nexus execution entry and Nexus decision.
- SEMA write application through `SemaEngine::apply`.
- SEMA read observation through `SemaEngine::observe`.

Default and `nota-text` builds do not compile the trace module or exports.
Production daemon behavior is unchanged.

## Witnesses

`tests/instrumentation_logging.rs` proves the trace comes from real runtime
calls by driving `Engine::handle` with generated `Input` values and asserting
the event sequence and generated payloads:

- Record path: `SignalAdmitted`, `NexusEntered`, `NexusDecided` to SEMA
  write, `SemaWriteApplied`, `SignalReplied`.
- Observe path: `SignalAdmitted`, `NexusEntered`, `NexusDecided` to SEMA
  read, `SemaReadObserved`, `SignalReplied`.
- Rejection path: `SignalRejected` and `SignalReplied`; no Nexus or SEMA
  event.

The Nix check `test-testing-trace` runs this witness under
`cargo test --features testing-trace --test instrumentation_logging`.

## Positive-grep Cleanup

Applied the obvious safe cleanup from Spirit records 1340-1342 and
operator report 274 inside `spirit-next/flake.nix`:

- `nota-surface-is-opt-in` now keeps only daemon-side negative guards for
  `nota_next` / `NotaSource`; dependency-surface cargo tests provide the
  positive proof.
- `binary-boundary-test` now keeps only negative guards against hand-written
  rkyv codec calls in `transport.rs`; socket and process tests provide the
  positive proof.
- Removed the `nix-integration-witness` positive-grep anchor check; the
  `apps.nix-integration-tests` runner remains the real Nix-built process
  witness.
- Removed test-name greps from `operator-271-closed-claims`; literal schema
  spelling checks remain because that check is about authored syntax.

Remaining positive greps in `generated-schema-source-checked-in` and
`local-schema-source-patches` are follow-up candidates. Some are source
artifact spelling checks; others still look like live-use proxies and should be
split in a later cleanup.

## Verification

Commands run in `/git/github.com/LiGoldragon/spirit-next`:

- `cargo fmt`
- `cargo test --features testing-trace --test instrumentation_logging`
- `cargo test --features testing-trace --test instrumentation_logging -- --test-threads=1`
- `cargo test --no-default-features`
- `cargo test --features nota-text`
- `cargo check --no-default-features --bin spirit-next-daemon`
- `nix flake check`

A follow-up cleanup commit renamed the event variants from implementation
verbs (`SignalAdmission`, `NexusExecute`, `SemaApply`, ...) to event names
(`SignalAdmitted`, `NexusEntered`, `SemaWriteApplied`, ...). The behavior is
unchanged; the public testing trace vocabulary now reads as recorded facts.

## Remaining Gaps

- Trace events are hand-written in `spirit-next`, not emitted by
  `schema-rust-next` behind an instrumentation feature as Spirit 1346 and 1350
  ultimately want.
- Trace delivery is an in-process test sink, not the CLI-owned testing log
  socket from Spirit 1347.
- Testing-mode configuration is a Cargo feature plus test harness install,
  not a typed NOTA build/configuration struct from Spirit 1348.
- `schema-rust-next` still has multiple positive-grep Nix checks named in
  operator report 274; those need a separate claimed cleanup or emitter-level
  trace support.
