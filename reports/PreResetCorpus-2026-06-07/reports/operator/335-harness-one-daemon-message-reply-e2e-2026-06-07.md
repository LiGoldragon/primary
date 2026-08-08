# Operator Report 335 — Harness One-Daemon Message Reply E2E

Date: 2026-06-07

## Summary

Implemented the one-component-daemon shape for harness routing and proved the
real message-then-reply path end to end.

The durable intent captured for this pass is Spirit record `hqg7`: harness
production shape is one component daemon owning multiple harness instances
internally; one OS daemon per harness is too heavy. Per-harness boundaries are
records, actors, and adapters inside the harness daemon.

## Repos

`signal-harness` main:

- Commit `0cf61f9a` — `signal-harness: configure multiple harness instances per daemon`.
- `HarnessDaemonConfiguration` now carries daemon socket/supervision fields,
  `owner_identity`, and `harnesses: Vec<HarnessInstanceConfiguration>`.
- `HarnessInstanceConfiguration` carries `harness_name`, closed
  `HarnessKind`, optional terminal socket, and optional Pi RPC adapter.
- Added `DeliveryFailureReason::HarnessUnavailable` for requests addressed to
  a harness instance the daemon does not serve.
- Updated `INTENT.md`, `ARCHITECTURE.md`, and `skills.md` to state the
  multi-instance daemon shape.

`harness` main:

- Commit `1ed51c20` — `harness: route multiple harness instances in one daemon`.
- `HarnessDaemon` now owns a list of `HarnessRuntimeConfiguration` values and
  binds them into a `BoundHarnessInstances` map.
- Incoming `signal-harness` requests dispatch by `HarnessName` to the matching
  in-process actor and delivery adapter.
- Added a direct daemon test:
  `harness_daemon_dispatches_two_harness_instances_inside_one_process`.
- Converted the existing message/router/harness e2e to one `harness-daemon`
  process with two internal Pi-kind harness instances.

## E2E Witness

The passing e2e is:

`cargo test --test message_router_harness_e2e -- --nocapture`

It starts:

- one `harness-daemon` with `agent-a` and `agent-b` instance records;
- one real `router-daemon`;
- two real `message-daemon` processes;
- real `message` CLI calls for both directions;
- terminal fixtures only as the receiving harness surfaces.

Path proven:

`agent-a message CLI` sends `(Send agent-b [question from agent a])` →
`message-daemon` → `router-daemon` → the one multi-instance
`harness-daemon` → `agent-b` terminal fixture. The `agent-b` fixture then runs
its own real `message` CLI with `(Send agent-a [response from agent b])`; that
reply flows back through the real daemons and reaches `agent-a` terminal
fixture.

This is no longer a one-way delivery witness and no longer uses one
`harness-daemon` process per harness.

## Verification

`signal-harness`:

- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `nix flake check`

`harness`:

- `cargo test --test message_router_harness_e2e -- --nocapture`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `nix flake check`

All passed.

