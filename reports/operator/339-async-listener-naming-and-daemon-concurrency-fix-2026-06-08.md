# 339 — async listener naming and daemon concurrency fix

operator, 2026-06-08.

## Trigger

The psyche flagged that the repo intent was incorrectly worded after Designer
verified that the listener shells were Tokio tasks named `Actor*`, not Kameo
actors. Designer report 556 also surfaced a separate correctness bug: generated
daemon bind code never set a request concurrency limit, so any long-lived
working-tier subscription on a component such as `terminal` could hold the only
default request permit and starve every other working request.

## What landed

### triad-runtime

Commit: `bedbb1db` — `triad-runtime: expose daemon request concurrency limit`.

Landed before that in the same cleanup line:

- `2025b3c9` — clarified `INTENT.md` / `ARCHITECTURE.md` so the listener and
  connection shells are async task-backed, not actors.
- The public runtime API now uses `Async*` listener names; `RequestGate` remains
  the Kameo actor.

This pass added `DaemonConfiguration::request_concurrency_limit()` with a
default of `RequestConcurrencyLimit::one()`. That preserves existing behavior
unless a component deliberately raises its listener admission cap.

### schema-rust-next

Commit: `aa4b80e1` — `schema-rust-next: emit daemon request concurrency limits`.

The daemon emitter now wires:

- `AsyncSingleListenerDaemon::new(...).with_concurrency_limit(configuration.request_concurrency_limit())`
- `AsyncMultiListenerDaemon::new(...).with_concurrency_limit(configuration.request_concurrency_limit())`

The generator also now emits `EngineStartFailure` / `EngineStopFailure` instead
of `ActorStartFailure` / `ActorStopFailure`, and the stale Nix guard was updated
to the engine names.

### Consumers

Pushed regenerated/updated consumers:

- `message` `56b4eca9` — async daemon stack refresh; fixed the source to await
  the generated async Nexus runner and async daemon hook.
- `router` `b5679e1f` — async daemon stack refresh.
- `terminal` `255610ba` — async daemon stack refresh plus
  `Configuration::request_concurrency_limit() == 64`.
- `orchestrate` `5c09dc5b` — async daemon stack refresh.
- `spirit` `84a2c2d9` — generated lifecycle failures renamed to engine failures
  through source, generated modules, and plane conversions.
- `repository-ledger` `be5bb2eb` — triad-runtime dependency refresh.

## Tests

Verified green:

- `triad-runtime`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `schema-rust-next`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `message`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `router`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `terminal`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `orchestrate`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `spirit`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- `repository-ledger`: `cargo fmt`, `cargo test`, `cargo clippy --all-targets -- -D warnings`

Also verified a grep over the touched runtime/generator/consumer repos found no
stale `ActorStartFailure`, `ActorStopFailure`, `ActorSingle*`, `ActorMulti*`,
`ActorListener*`, `ActorConnection*`, `actor-native`, or "independent Tokio
tasks" listener wording.

## Remaining

This fixed the naming truth and the immediate default-one starvation vector.
It did not remove the old `signal-executor` execution path from the remaining
offenders. `orchestrate` and `repository-ledger` still have tests that prove
the old executor path, and Designer report 555 has the correct removal list.

The deeper terminal lifecycle findings from report 556 remain: supervised root,
detached supervision thread, restart policy, blocking store I/O in async
handlers, typed meta tier, and a new-path subscription relay test. The
concurrency cap reduces the starvation blast radius now; moving long-lived
streams fully off request permits is still the streaming-runtime design slice.
