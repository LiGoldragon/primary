# 707-0 — mentci integration + worktree protocol: frame and method

## Trigger

Psyche: "take a look at operator's work, and research/develop a better integration
of both mentci cli and mentci gui to get better readability/testing out of
criome/spirit/router full-hosts (we have prometheus vms now to test things — we
can write tests for those in nix-derived scripts) in worktrees-branches. upkeep
any previous worktrees to be either merged, marked as archived (we need a manifest
for that for GC) or re-used/rebased-on-main/recycled for the new work. make this
standard worktree protocol for agents to register their worktree in the
orchestrate tool as well, which will keep a database of that. do all that in
parallel."

## Spirit gate

Captured **`eh5a`** (Decision, High): agents register every worktree in the
orchestrate tool (a database); standard lifecycle = merge / archive (manifest for
GC) / recycle (rebase on main). This *tools* the existing principle `kb4k`
[agents track every worktree they create… archive the branches and dismantle the
trees] and the `oust` feature-branch-worktree convention. The mentci architecture
is already settled intent (`7x5z` mentci is a state-bearing UI daemon triad,
mentci-lib the shared lib, mentci-egui a thin client; `xlrk`/`xen8` egui shape;
`t00s`/`p43g`/`gc0n` the criome approval/adjudication model) — so the
mentci-integration + VM-testing work is task execution against settled intent, no
new capture there.

## The three parallel streams

- **A — mentci CLI/GUI integration.** Review operator's recent work (criome
  client-approval runtime + witnesses; mentci-lib proposals/approval-subscriptions/
  psyche-approval-flow; mentci-egui daemon-signal connection + channel labels;
  router authorized-object projection/fanout), then design a better mentci CLI +
  GUI integration for readability/testing of criome/spirit/router as full-host
  daemons, with nix-derived VM tests on the new Prometheus VMs.
- **B — worktree upkeep.** Audit every worktree under `~/wt` (~50 across ~25
  repos), classify each merge / archive / recycle / keep-active with evidence
  (merged? unpushed work? stale? whose lane?), and propose the GC manifest.
  Non-destructive in this wave.
- **C — worktree protocol.** Design the orchestrate-tool worktree registry (the
  `orchestrate-cli` Rust binary behind `tools/orchestrate`): schema, register/
  list/update commands, and the archive manifest format (reconciled with B). Note
  the standing intent that lane management migrates from `tools/orchestrate` to
  the typed `persona-orchestrate` component (`w190`/`tz5j`/`udgu`) — build in
  orchestrate-cli now, flag the eventual migration.

## Method

A parallel **design + audit wave** (this report's sub-agents 1-3), all
non-destructive (read-only code inspection; reports + proposals only — no worktree
deletion, no primary commits by sub-agents, no premature orchestrate-cli build).
The orchestrator (me) then reconciles B's manifest with C's registry format,
ratifies the worktree classifications (guarding any unpushed work), and runs a
**build wave**: implement the registry in orchestrate-cli, execute the worktree
upkeep per the ratified classifications, and prototype the mentci integration +
VM tests on recycled worktree-branches.

Sub-reports land as 1-3 here; the synthesis as the highest-numbered file.
