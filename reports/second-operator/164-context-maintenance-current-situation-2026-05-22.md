# Context Maintenance Current Situation

Report kind: context maintenance
Topic: second-operator lane situation after restored reports
Date: 2026-05-22
Lane: second-operator

## Headline

The `second-operator` lane now has the restored old
`operator-assistant` reports plus the current lane-registry result.
This is useful history, but it is not all live context. The live
operator surface is much narrower:

- `reports/second-operator/157-persona-orchestrate-dynamic-role-mvp.md`
  is the implementation baseline for the raw Orchestrate MVP.
- `reports/second-operator/162-persona-orchestrate-signal-executor-migration-vision.md`
  is the current migration vision, but parts are now superseded.
- `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`
  is the latest shipped slice.
- bead `primary-c620` (migrate persona-orchestrate triad to current
  foundation) remains open and is still the right broad work item.
- bead `primary-ao1q` (lane-registry slice) is closed.

I did not retire or delete restored reports in this pass. The user
just restored and renumbered them, and the workspace worktree is clean,
so this report records the maintenance decision surface without
destroying restored context.

## Current Workspace State

Primary workspace:

- clean working copy at the start of this report pass.
- `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`
  is the renamed lane-registry result report.
- `reports/operator-assistant/` no longer exists locally.
- `reports/second-operator/` contains 32 reports and 7853 lines,
  over the report soft cap.

Relevant component repos are clean:

- `signal-frame`: `main` at `653773b7`, clean macro boilerplate.
- `signal-executor`: `main` at `63d3732f`, atomic and reply mapping
  contract docs.
- `signal-persona-orchestrate`: `main` at `5863d339`, current
  signal-frame alignment plus lane registry vocabulary.
- `owner-signal-persona-orchestrate`: `main` at `5e6e8cc`, lane
  registry owner operations.
- `persona-orchestrate`: `main` at `50ed6f78`, lane retirement
  missing-record rejection.
- `persona-mind`, `signal-persona-mind`, `owner-signal-persona-mind`,
  and `owner-signal-persona-router` are also clean in the checked
  local worktrees.

Open or in-progress beads visible during the sweep:

- `primary-c620`: persona-orchestrate triad migration to current
  foundation.
- `primary-devn.1.4`: prototype introspection observation slices.
- `primary-hj4.1.4`: persona-mind post-commit graph subscription
  delta delivery.
- `primary-2y5`: persona daemon EngineId socket setup, manager redb,
  spawn envelope.
- `primary-vhb6`: horizon re-engineering and lojix daemon.
- `primary-a61`: CriomOS router Wi-Fi policy and SAE secret.
- `primary-a18`: persona-engine-sandbox provider auth smoke.

One `bd show primary-c620` attempt failed while another `bd` command
held the embedded Dolt writer lock; the retry succeeded.

## What Changed Since Report 162

Report 162's diagnosis was correct when written, but the lane-registry
implementation moved several items forward:

- `signal-persona-orchestrate` no longer uses the old
  `UnknownKindForVerb` error name; residual manual decoders now use
  `UnknownVariant`.
- `signal-persona-orchestrate` is now pinned to current
  `signal-frame` on branch `main` and emits clean macro names.
- manual `OperationKind` definitions are no longer owned by hand code;
  the compatibility `operation_kind()` method delegates to generated
  kind output.
- `owner-signal-persona-orchestrate` now includes owner operations for
  lane registration, lane retirement, and lane authority changes.
- `persona-orchestrate` has a real `lane_registry` table and an
  ordinary `Observe(Lanes)` read path.

The following parts of report 162 are still live:

- `persona-orchestrate` still does not depend on `signal-executor`.
- daemon sockets still dispatch through `OrchestrateService` directly
  instead of `Executor::execute`.
- `OperationLowering` still maps operations directly to
  `signal_sema::SemaOperation` labels instead of lowering to
  daemon-local commands and effects.
- the CLI still tries to decode the request as working first, then
  owner, instead of using generated head routing.
- `signal-persona-orchestrate` still has domain `Watch` and `Unwatch`
  plus `ObservationSubscription.include_sema_effects`.
- the mandatory generic `Tap` / `Untap` observable surface is still
  architecture text, not implemented contract surface.
- owner `RequestUnimplemented` still carries the operation kind
  redundantly.
- the deeper role, agent, job, run, and policy-programming model is
  not settled in code.

## Report Inventory

### Active For This Lane

Keep these in immediate context for the next `second-operator`
implementation pass:

- `reports/second-operator/157-persona-orchestrate-dynamic-role-mvp.md`
  - what the raw MVP currently promises.
- `reports/second-operator/162-persona-orchestrate-signal-executor-migration-vision.md`
  - the current migration target, with stale points noted above.
- `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`
  - latest shipped slice and current unresolved lane-id tombstone
  question.
- `reports/designer-assistant/137-persona-orchestrate-triad-audit-2026-05-21.md`
  - upstream audit still referenced by `primary-c620`.
- `reports/second-designer/3-lane-registry-test-implementation-proposal-2026-05-21.md`
  - useful only for verifying the already-shipped lane-registry slice.

### Related But Not Immediate

These can stay on disk but do not need to be loaded for the next
Orchestrate executor migration unless their topic comes up:

- `reports/second-operator/158-signal-frame-executor-v4-reconciliation.md`
  - mostly superseded by current `signal-frame` and `signal-executor`
  commits, but still useful as historical context for the v4 design
  transition.
- `reports/second-operator/159-persona-mind-signal-tree-owner-contract-vision.md`
  - relevant when the Mind/Spirit/Orchestrate policy chain resumes.
- `reports/second-operator/160-owner-signal-persona-router-channel-authority.md`
  - relevant when Router owner authority or Mind channel policy resumes.
- `reports/second-operator/161-signal-sema-observable-vocabulary-cleanup.md`
  - relevant to observable vocabulary and old event-head compatibility.
- `reports/second-operator/150-criome-authorization-slot-identity-follow-up-2026-05-17.md`
  through `reports/second-operator/152-criome-authorization-expiry-replay-guard-2026-05-18.md`
  - relevant to Criome/Lojix auth, not current Orchestrate work.
- `reports/second-operator/154-primary-hrhz-architecture-audit-2026-05-18.md`
  - relevant to horizon/lojix work and bead `primary-vhb6`, not current
  Orchestrate work.

### Historical Witnesses

These old implementation reports should normally not be loaded for
current Orchestrate work. Their enduring value should be in commits,
repo architecture files, skills, and beads:

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
- `reports/second-operator/138-persona-mind-gap-close-2026-05-16.md`
- `reports/second-operator/139-kameo-spawn-in-thread-supervised-shutdown-bug-2026-05-16.md`
- `reports/second-operator/139-phase3-closed-sums-sweep-2026-05-16.md`
- `reports/second-operator/140-phase3-actor-supervision-audit-2026-05-16.md`
- `reports/second-operator/141-phase3-typed-config-sweep-2026-05-16.md`
- `reports/second-operator/142-handover-2026-05-16.md`
- `reports/second-operator/143-persona-engine-meta-testing-audit-2026-05-16.md`

The May 16 handover (`142`) says the report lane was already over cap
then. Restoring the old lane into `second-operator` brings that debt
forward rather than resolving it.

## Current Operator Situation

The next useful operator pass should not start by rereading every old
report. It should start from `primary-c620`, report 162, report 163,
and the three Orchestrate repos.

Current objective:

1. refresh the Orchestrate migration vision after the lane-registry
   slice;
2. decide whether `Watch` / `Unwatch` remains a domain stream or is
   deleted after generic `Tap` / `Untap` lands;
3. migrate `persona-orchestrate` runtime from service-direct dispatch
   to `signal-executor` with local `Command` and `Effect` types;
4. replace the CLI working-first-owner-second decode path with
   generated head routing;
5. add the constraint tests named in report 162, updated for the
   lane-registry state.

The most important unresolved design point exposed by the shipped
lane registry is retired lane identity:

- current behavior: retired lanes are removed from the active table;
  active lanes do not rename; a later registration may reuse a retired
  identifier if the active registry shape permits it;
- stricter alternative: keep tombstones or a persistent ordinal counter
  so retired lane identifiers are never reused;
- this matters before the lane registry becomes the durable source of
  truth for report lanes, claim identity, or historical agent runs.

## Recommended Maintenance Action

Keep this report and reports 157, 162, 163 as the immediate
`second-operator` context.

Do not load the historical May 15-18 reports unless their component
topic is explicitly in scope. They should be candidates for retirement
after one more pass verifies their permanent substance already lives in
repo commits, `ARCHITECTURE.md`, skills, and current beads.

If the user wants the lane back under the report soft cap now, the next
maintenance action is a retirement commit that removes the historical
witnesses listed above while preserving this report as the index of why
they are no longer active context.
