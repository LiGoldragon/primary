# Cloud component design recap — frame and method

Role lane: `cloud-operator`.

User request: recap the current situation with cloud component design, use `skills/context-maintenance.md`, and use subagents.

## Method

This is a context-maintenance shaped recap: sweep the relevant working surfaces, keep the still-load-bearing substance, and put the recap in a role report instead of a large chat answer.

The relevant surfaces are:

- current live conversation context: the lane moved from `pi-operator` to `cloud-operator` and the report directory was renamed;
- old cloud/system reports that predate the lane rename;
- cloud component repositories and signal-contract repositories;
- Spirit intent records and workspace permanent guidance around component triads.

## Subagent fanout

Subagents are explicitly authorized by the user for this task. Children are read-only scouts. They may write only their configured output artifacts inside this report directory. They must not edit source/workspace files, mutate `jj`/`git`, or launch child subagents.

Expected files:

- `1-history-and-report-scout.md` — report-history read of cloud design.
- `2-repository-scout.md` — live repo/component-state read.
- `3-intent-and-guidance-scout.md` — Spirit/permanent-guidance read.
- `4-overview.md` — parent synthesis and handoff recap.
