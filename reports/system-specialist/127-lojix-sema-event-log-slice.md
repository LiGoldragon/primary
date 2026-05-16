# Lojix Sema Event Log Slice

Date: 2026-05-16
Role: system-specialist
Branch: `lojix` `horizon-re-engineering`
Worktree: `/home/li/wt/github.com/LiGoldragon/lojix/horizon-re-engineering`

## What Landed

The build-only Lojix runtime now opens a daemon-owned `sema-engine`
database at `<state-directory>/lojix.redb`.

The new `DeploymentEventLog` owns three typed record families:

- `deployment_identities`
- `deployment_events`
- `deployment_observation_subscriptions`

`RuntimeRoot` no longer mints deployment IDs or deployment-observation
tokens from in-memory counters. Deployment IDs and observation tokens
are derived from the durable sema snapshot sequence and asserted into
the event-log database. The remaining in-memory counter is the cache
retention observation token; cache retention is still a stubbed slice.

Deployment observations now persist as typed sema records and include
the cluster and node beside the `signal-lojix` observation. This fixes
the old snapshot filter shape, which could only filter by deployment
because the event row had no cluster/node data.

The daemon startup path now uses `RuntimeRoot::try_with_configuration`.
If durable state cannot open, `lojix-daemon` fails at startup instead
of hiding the problem behind an actor panic.

The default in-process test runtime now uses unique temp state and
GC-root directories. This matters because the event log is a real redb
file now; shared default test state would have created cross-test
database lock contention.

## Tests Added

`tests/event_log.rs` adds two source-level witnesses:

- `deployment_event_log_survives_reopen_through_sema_engine`
- `deployment_identifiers_do_not_reset_after_reopen`

`flake.nix` now exposes `checks.<system>.test-event-log`.

## Verification

Local cargo:

- `cargo fmt --check`
- `cargo test --jobs 1`
- `cargo clippy --jobs 1 --all-targets -- -D warnings`

Nix on Prometheus:

- `nix build --max-jobs 1 --cores 2 .#checks.x86_64-linux.test-event-log`
- Earlier in the same slice: `test-build-pipeline` and `clippy` also
  passed through Nix on Prometheus.

Real build smoke through the daemon/CLI boundary:

- Request:
  `(DeploymentSubmission goldragon zeus "/home/li/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering/datom.nota" "github:LiGoldragon/CriomOS/horizon-re-engineering" (FullOsDeployment Build) (NamedBuilder prometheus) [])`
- Reply:
  `(DeploymentAccepted deployment_1)`
- Final observation included `DeploymentBuilt` with:
  `/nix/store/qsz55smwzwl11i9p150ikkw5zisrmf6p-nixos-system-zeus-26.05.20260510.da5ad66`
- The built-output GC root pointed at the same store path.

## Remaining Work

Live pushed streams are not implemented yet. The current
`DeploymentObservationSubscription` path returns a subscription-open
snapshot over the sema-backed event log.

Opening a deployment-observation subscription records a durable
subscription token. In the current one-shot CLI polling shape, repeated
polls create repeated subscription records. That is acceptable only as
a transitional state because the wire grammar already treats the
operation as opening a stream; the next stream-delivery slice should
make subscriptions connection-owned and retraction-aware.

Cache retention remains a stub and still has an in-memory token
counter. It should not be treated as durable until its actor and sema
record families land.

The live generation set, sema-backed GC-root records, closure copy,
activation, rollback, and container lifecycle observation remain
unimplemented.
