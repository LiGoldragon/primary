# Lojix Live Deployment Observation Streams

Role: system-specialist
Date: 2026-05-16
Repo: `lojix`
Branch: `horizon-re-engineering`
Commit: `e6f5b7cf24c8`

## Summary

The deployment-observation stream is now live-pushed over the daemon
socket. A `DeploymentObservationSubscription` sent as the only operation
on a socket connection opens a durable subscription, returns the normal
typed subscription-open reply, then keeps the connection open for
`SubscriptionEvent` frames. Closing happens through
`DeploymentObservationRetraction` with the typed token; client disconnect
also asks the runtime to close the subscription.

This is the stream slice that follows the sema-backed event-log slice in
`reports/system-specialist/127-lojix-sema-event-log-slice.md`.

## What Changed

- `EventLogActor` now owns active deployment-observation subscribers in
  memory while also persisting subscription records through
  `DeploymentEventLog`.
- Appending an observation still writes the sema-backed event log first,
  then pushes the observation to every matching active subscriber.
- Durable subscription records are retracted on typed close, and the
  socket-level test verifies no durable subscription remains after close.
- `RuntimeRoot` exposes a stream-opening message that registers a live
  subscriber channel with `EventLogActor`.
- `SocketServer` now distinguishes one-shot requests from a single
  `DeploymentObservationSubscription`. The stream path writes the
  subscription-open reply, then sends pushed `SubscriptionEvent` frames on
  the same socket until close.
- `ARCHITECTURE.md`, `README.md`, and `skills.md` now state that active
  deployment-observation subscribers receive pushed stream events.

## Witnesses

- `tests/socket.rs`:
  `deployment_observation_subscription_receives_live_stream_sequence_and_closes`
  opens one socket subscription, appends `Submitted`, `Building`, `Built`,
  and `Failed` observations through the real event-log actor, receives the
  same sequence as pushed `SubscriptionEvent` frames, sends typed
  retraction, and proves the durable subscription count is zero.
- `tests/event_log.rs`:
  `deployment_observation_subscription_retraction_removes_durable_record`
  proves the sema-backed subscription record is retracted.

## Verification

All commands were run with local parallelism constrained; Nix dispatched
the flake checks to `prometheus.goldragon.criome`.

```sh
cargo fmt --check
cargo test --jobs 1 --test event_log --test socket -- --test-threads=1
cargo clippy --jobs 1 --all-targets -- -D warnings
nix build --max-jobs 1 --cores 2 \
  .#checks.x86_64-linux.test-event-log \
  .#checks.x86_64-linux.test-socket \
  .#checks.x86_64-linux.clippy
```

All passed.

## Remaining Work

- The human-facing `lojix` CLI still follows the one-reply command shape;
  it can open a subscription and receive the open reply, but it does not
  yet render pushed stream events as a long-running watch command. That is
  a separate CLI surface decision.
- The cache-retention observation stream still uses the earlier
  subscription-open snapshot shape and has no live pushed event path yet.
- The deploy pipeline still implements the build-only slice. Copy,
  activation, rollback, live generation set, sema-backed GC-root records,
  container lifecycle observation, and cache retention remain to be built.
