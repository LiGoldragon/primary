# Review Persona Engine Backlog

Report kind: review
Topic: old Persona engine implementation residue after May 16 sweeps
Date: 2026-05-22
Lane: second-operator

## What This Review Supersedes

This report supersedes the old May 15-16 engine and phase-3 reports:

- `reports/second-operator/121-readiness-audit-resolution-2026-05-15.md`
- `reports/second-operator/125-persona-engine-implementation-audit-2026-05-15.md`
- `reports/second-operator/126-nota-config-scaffold-2026-05-16.md`
- `reports/second-operator/127-persona-message-daemon-typed-config-migration-2026-05-16.md`
- `reports/second-operator/128-persona-system-audit-2026-05-16.md`
- `reports/second-operator/129-persona-introspect-gap-close-2026-05-16.md`
- `reports/second-operator/129-persona-message-gap-close-2026-05-16.md`
- `reports/second-operator/131-kernel-stack-audit-2026-05-16.md`
- `reports/second-operator/131-persona-router-gap-close-2026-05-16.md`
- `reports/second-operator/132-signal-persona-contracts-gap-close-2026-05-16.md`
- `reports/second-operator/134-persona-manager-gap-close-2026-05-16.md`
- `reports/second-operator/135-phase3-push-subscription-chains-2026-05-16.md`
- `reports/second-operator/136-phase3-terminal-control-data-plane-2026-05-16.md`
- `reports/second-operator/137-phase3-event-sourcing-snapshots-2026-05-16.md`
- `reports/second-operator/139-kameo-spawn-in-thread-supervised-shutdown-bug-2026-05-16.md`
- `reports/second-operator/139-phase3-closed-sums-sweep-2026-05-16.md`
- `reports/second-operator/140-phase3-actor-supervision-audit-2026-05-16.md`
- `reports/second-operator/141-phase3-typed-config-sweep-2026-05-16.md`
- `reports/second-operator/142-handover-2026-05-16.md`
- `reports/second-operator/143-persona-engine-meta-testing-audit-2026-05-16.md`

Their landed commits and architecture edits are the durable record for
the completed work. This report keeps only the still-actionable
residue.

## Current Meaning Of The Old Phase-3 Work

The old phase-3 wave proved a lot of runtime shape:

- typed daemon configuration through `nota-config`;
- source witnesses against production daemons reading control-plane
  environment variables;
- router observation queries and closed status enums;
- terminal control/data socket split;
- event-sourced manager snapshots;
- actor-density and no-shared-lock tests;
- subscription lifecycle discipline;
- architectural truth tests as Nix checks.

That is no longer active desk context. The rules live in skills,
architecture files, tests, and commits.

## Still-Actionable Residue

### Persona Manager

The old manager reports leave three useful items:

- a stronger Nix-chained restart witness would prove manager snapshots
  rebuild from disk across process boundaries;
- fixture-only environment-variable consumption may still exist where
  `persona-component-fixture` stands in for real daemons;
- bounded readiness probing remains acceptable only as a reachability
  probe until children can push explicit `SocketBound` supervision
  events.

This is not the current second-operator task unless bead `primary-2y5`
becomes active again.

### Persona Introspect

The old introspect gap was that peer clients were supervised but not
yet queried. The important current target is bead `primary-devn.1.4`:
prototype observation slices for manager, terminal, message, and
harness.

The boundary remains: introspect should query component contracts and
ordinary observation surfaces; it should not open component stores.

### Persona Router

Router observation shape landed earlier, but deeper channel state still
belongs to the Mind/Router authority chain:

- outbox persistence should be tied to durable launch-path discipline;
- channel triples and adjudication state should not remain loose
  stringly records;
- Router owner authority belongs under `owner-signal-persona-router`
  and is reached through Orchestrate, not directly from Mind.

The detailed policy context is in
`reports/second-operator/168-review-mind-router-policy-2026-05-22.md`.

### Persona System

The component is still paused. The old audit's durable lessons are:

- no polling for state changes;
- push-only backend discipline;
- focus subscription close should be reply-side
  `SubscriptionRetracted` when the live event stream lands;
- privileged actions need a policy decision before implementation.

No unpause work is active in this lane.

### Terminal Stack

The terminal control/data split is no longer current desk context. The
remaining principle is stable: control is Signal, data is a separate
stream, and tests must prevent actor/control code from leaking onto the
data plane.

### Sema And Kernel Stack

Old `signal-core` and `sema-engine` witness reports are historical.
The current migration target is the newer `signal-frame`,
`signal-sema`, and `signal-executor` stack.

One old lesson still matters: resource-owner restart tests need to
prove resources are actually released, not just that a mailbox closed.
That discipline is now skill-level and should not live as a report.

## Not The Current Pickup

This backlog should not distract from `primary-c620`. Use it only when
the user routes second-operator back to the Persona engine,
introspection, manager, terminal, or system components.

