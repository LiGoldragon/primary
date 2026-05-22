# Review Persona Orchestrate Migration

Report kind: review
Topic: persona-orchestrate migration after lane-registry slice
Date: 2026-05-22
Lane: second-operator

## What This Review Supersedes

This report supersedes:

- `reports/second-operator/154-primary-hrhz-architecture-audit-2026-05-18.md`
- `reports/second-operator/157-persona-orchestrate-dynamic-role-mvp.md`
- `reports/second-operator/162-persona-orchestrate-signal-executor-migration-vision.md`
- `reports/second-operator/164-context-maintenance-current-situation-2026-05-22.md`

The older reports were correct for their moments. The current state has
moved: the dynamic-role MVP exists, the lane registry exists, the
contracts are on current `signal-frame`, and the remaining problem is
the executor-centered migration plus signal-tree cleanup.

The fresh lane-registry implementation result remains on disk as a
shipped-slice witness and audit source:
`reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`.

## Current Shipped Shape

The Orchestrate triad exists as a raw but useful prototype.

`signal-persona-orchestrate` now owns:

- dynamic role and claim vocabulary;
- role-vector lane vocabulary: `RoleToken`, `Role`, `LaneAuthority`,
  `LaneIdentifier`, `LaneRegistration`;
- ordinary observations for role and lane state;
- current `signal-frame` generated operation kind output.

`owner-signal-persona-orchestrate` now owns:

- dynamic role creation and retirement;
- repository index refresh;
- lane registration, lane retirement, and lane authority update;
- a `Retirement` sum so role retirement and lane retirement do not
  collide under the same owner root.

`persona-orchestrate` now owns:

- daemon-owned redb/sema state;
- ordinary and owner Unix sockets;
- a thin CLI that talks to daemon sockets and does not open the store;
- role records, claim records, repository refresh records, activity
  records, and lane records;
- lock-file projection as compatibility with the old shell helper;
- tests for dynamic role creation, repository refresh, CLI boundary,
  socket boundary, and lane registry behavior.

## Current Gap

The runtime is still service-direct, not executor-centered.

Today:

- `src/service.rs` matches directly on contract operations and mutates
  ledgers;
- `src/daemon.rs` decodes frames and calls the service directly;
- `src/lowering.rs` maps operations straight to payloadless
  `SemaOperation` labels;
- the crate does not yet depend on `signal-executor`;
- the CLI decodes as working first, then owner.

Target:

- contract operation lowers to daemon-local `Command`;
- command execution produces daemon-local `Effect`;
- `Command` implements `ToSemaOperation`;
- `Effect` implements `ToSemaOutcome`;
- the daemon executes through `signal-executor`;
- generic operation/effect observation is supplied through the
  standard observable surface;
- the CLI routes by generated operation head metadata.

This is the main work under bead `primary-c620`.

## Lane Registry Decision

Retired lane identifiers are not tombstoned for now. The registry is an
active table:

- retiring a lane removes the record;
- active lanes are not renamed;
- retired names are allowed to disappear;
- no persistent `(role, authority) -> next ordinal` counter is required
  in the current slice.

This removes the tombstone question from the next implementation pass.
If historical lane identity later becomes load-bearing for agent-run
audit trails, add tombstones then as a separate history feature.

## Watch And Tap

The ordinary contract still has `Watch(ObservationSubscription)` and
`Unwatch(ObservationToken)`. It also has architecture text saying every
Persona component should expose mandatory generic `Tap` and `Untap`.

The clean split:

- `Tap` and `Untap` are generic operation/effect introspection.
- `Watch` and `Unwatch`, if kept, are Orchestrate-domain streams.

Do not use `Watch` for generic Sema observation after `Tap` exists.
If the next slice cannot implement a domain stream, delete or defer
`Watch` rather than preserving a confused dual-purpose observer.

## Owner Signal Shape

The owner contract is now administratively useful but still not the
final policy surface.

Do not expand it by simply adding every authority idea to the current
root set. The next design pass needs to distinguish:

- role definitions;
- lane definitions;
- agent runs;
- jobs;
- repository management;
- scheduling policy;
- policy-programming hooks;
- downstream owner orders to Router and Harness.

The immediate executor migration can stay inside existing operations.
Broader owner-policy expansion should be a separate signal-tree pass.

## Implementation Order

Recommended next operator slice:

1. claim `primary-c620` and the Orchestrate triad repos.
2. add source tests that fail on service-direct daemon dispatch once
   the executor path is ready.
3. introduce `Command` and `Effect` enums in `persona-orchestrate`.
4. replace `OperationLowering` with working and owner lowerers that
   return command plans.
5. implement a shared command executor over the existing service or
   ledger modules first; do not rewrite the whole daemon actor shape
   in the same slice.
6. map command/effect to Sema observation traits.
7. route both daemon sockets through `signal-executor`.
8. keep batches conservative: reject multi-operation or multi-command
   execution before commit until Orchestrate has a real transaction
   boundary.
9. update the CLI dispatch only after generated head routing is
   available and tested.

## Constraint Tests To Keep Or Add

Keep:

- CLI does not import store/service/table/redb modules.
- ordinary and owner sockets reject each other's frames.
- daemon rejects non-Signal traffic.
- lane register, observe, set-authority, and retire are store-backed.

Add or refresh:

- `persona-orchestrate` depends on `signal-executor`.
- daemon request handling instantiates or calls the executor path.
- no direct `OrchestrateService::handle` call remains in socket
  handlers except behind the command executor.
- every accepted operation lowers to at least one explicit command.
- command and effect types implement Sema projection traits.
- engine errors after acceptance produce accepted batch-abort style
  replies, not pre-acceptance rejection.
- generic operation/effect observation uses `Tap` and `Untap` once the
  contract exposes them.
