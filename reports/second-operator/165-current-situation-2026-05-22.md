# Current Situation

Report kind: situation
Topic: second-operator current working surface after heavy context maintenance
Date: 2026-05-22
Lane: second-operator

## Where We Are

The lane is back to a small active report set. The old
`operator-assistant` reports were restored under `second-operator`,
then re-read and folded forward. The active context after this pass is:

- `reports/second-operator/165-current-situation-2026-05-22.md`
  - this report, the desk-level current state.
- `reports/second-operator/166-review-persona-orchestrate-migration-2026-05-22.md`
  - the current Orchestrate implementation and migration target.
- `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`
  - fresh implementation result retained as an audit source for the
  lane-registry slice.
- `reports/second-operator/167-review-persona-engine-backlog-2026-05-22.md`
  - the old Persona engine phase-3 residue, repackaged against current
  state.
- `reports/second-operator/168-review-mind-router-policy-2026-05-22.md`
  - Mind, Router, channel authority, and owner-signal shape.
- `reports/second-operator/169-review-criome-lojix-authorization-2026-05-22.md`
  - Criome/Lojix authorization residue.

Everything else in this lane was a working witness or transitional
handover. Its live substance is now in the six reports above, current
repo commits, architecture files, skills, or beads.

## Main Work Now

The main second-operator target is still bead `primary-c620`: migrate
the `persona-orchestrate` triad to the current foundation.

The lane-registry slice is done. Bead `primary-ao1q` is closed. The
current code state is:

- `signal-persona-orchestrate` has role-vector lane vocabulary,
  `Observation::Lanes`, and clean current `signal-frame` macro output.
- `owner-signal-persona-orchestrate` has lane `Register`, lane
  `Retire`, and `SetAuthority`.
- `persona-orchestrate` has a `lane_registry` table and owner/ordinary
  handlers for the lane registry.
- the CLI still talks only to the daemon, and the constraint tests
  protect that boundary.

The next useful implementation is not more report cleanup. It is the
Orchestrate executor migration:

1. add daemon-local `Command` and `Effect` types;
2. route ordinary and owner socket execution through `signal-executor`;
3. project commands and effects through `ToSemaOperation` and
   `ToSemaOutcome`;
4. replace the CLI's working-first-owner-second decode path with
   generated head routing when the macro surface is ready;
5. add constraint tests proving the daemon no longer bypasses the
   executor path.

## Cleared Question

Retired lane identifiers do not need tombstones right now. The current
active-table behavior is acceptable: retiring a lane removes it, active
lanes are not renamed, and the system does not reserve retired names
forever.

If later history preservation requires tombstones, that is a new design
problem attached to durable agent runs or report-lane history, not a
blocker for the current lane-registry slice.

## Open Decisions That Actually Matter

`Watch` and `Unwatch` need a decision during the Orchestrate migration.
Generic operation/effect introspection belongs to mandatory `Tap` and
`Untap`. `Watch` and `Unwatch` should survive only if they become a
domain stream for Orchestrate facts such as role, lane, claim, activity,
and agent-run changes.

The owner signal still needs a deliberate signal-tree pass before it
grows beyond role, lane, repository, and immediate administration
operations. The next expansion should not blindly add abstract-job or
policy-programming verbs to the existing root set.

The live role model is not fully split yet. The code has roles and
lanes. The design direction still wants separate role definition, agent
run, job, and policy records. Do not hide those types in strings.

## Workspace State

The relevant component worktrees checked during this pass were clean:

- `signal-frame`
- `signal-executor`
- `signal-persona-orchestrate`
- `owner-signal-persona-orchestrate`
- `persona-orchestrate`
- `persona-mind`
- `signal-persona-mind`
- `owner-signal-persona-mind`
- `owner-signal-persona-router`

The primary workspace had an unrelated `second-designer` report in the
working copy during this pass. This lane did not touch or commit it.

## Not Current Work

The old May 15-18 Persona engine reports are no longer the active desk.
The substance that still matters is summarized in:

- `reports/second-operator/167-review-persona-engine-backlog-2026-05-22.md`
- `reports/second-operator/168-review-mind-router-policy-2026-05-22.md`

Criome/Lojix authorization is real but not the current second-operator
pickup unless the user switches topics. Its current packet is:

- `reports/second-operator/169-review-criome-lojix-authorization-2026-05-22.md`
