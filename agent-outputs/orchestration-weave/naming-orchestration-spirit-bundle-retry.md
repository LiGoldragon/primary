# Naming, Orchestration, and Spirit Bundle Weave Retry

Task and scope: create the tracker/bead weave for the already-approved work bundle only. No source changes, implementation, audit, closure, commits, or pushes were performed.

Consulted:

- `/home/li/primary/AGENTS.md`
- dispatch text in this run
- `bd --help`, `bd create --help`, `bd dep --help`, `bd list --help`, `bd show --help`, `bd ready --help`
- existing tracker searches/lists for likely duplicate open orchestration/naming/Spirit beads

## Beads created

Parent epic:

1. `primary-ascl` — `Deliver approved naming, orchestration, Spirit, and README doctrine bundle`
   - Status: open.
   - Scope: parent for naming cleanup, launch-time orchestration injection, orchestration/attention/commit/edit-coordination doctrine, read-only Spirit query composition, and README scale-repo influence backlog.
   - Note: `bd` rejected making the task audit bead block this epic (`epics can only block other epics, not tasks`), so completion is represented by the parent/child hierarchy and the audit bead dependencies rather than a direct dependency edge into the epic.

Child beads:

2. `primary-ascl.1` — `Discover approved replacements for bad orchestration names`
   - Status: open, ready.
   - Purpose: find prior approved replacement proposals for `jj`, `beads`, `beauty`, and `component-triad`; if any are missing, pause renaming for psyche approval.

3. `primary-ascl.2` — `Implement approved naming cleanup across source and generated surfaces`
   - Status: open, dependency-blocked by `primary-ascl.1`.
   - Purpose: apply only approved replacements, edit source-of-truth first, regenerate derived/runtime surfaces, run Nix-accessed checks, commit/push by the editing worker.

4. `primary-ascl.3` — `Default Claude, Codex, and pi sessions into orchestration mode at launch`
   - Status: open, ready.
   - Purpose: programmatic pre-first-turn launch-time injection plus mandatory launch-time escape hatch for non-orchestrator roles/sessions.

5. `primary-ascl.4` — `Strengthen orchestration, attention, provenance, and edit-coordination doctrine`
   - Status: open, ready.
   - Purpose: encode refusal of direct work, dispatch gates, batching/scope expansion, broad model right-sizing, distinct auditor, weaver use for elaborate plans, read-only Spirit/no writes, psyche-attention discipline, commit-message provenance, and Orchestrate/edit-coordination preload for editing-capable roles.

6. `primary-ascl.5` — `Add read-only Spirit query module and role composition checks`
   - Status: open, ready.
   - Purpose: add narrow read-only Spirit query module, keep existing `spirit-cli` for write/maintenance roles, preload/query for orchestrators and judgment workers, exempt mechanical workers, verify `~/spirit-cli-usage.md` by testing, and add checks for generated role composition.

7. `primary-ascl.6` — `Investigate README scale repos and actual influence labels`
   - Status: open, ready, P3 backlog.
   - Purpose: first investigate whether comparison/list exists; list scale repos and label only actual influences; no README edits in this bead.

8. `primary-ascl.7` — `Audit completed naming, orchestration, Spirit, and README bundle`
   - Status: open, dependency-blocked by `primary-ascl.2`, `primary-ascl.3`, `primary-ascl.4`, `primary-ascl.5`, and `primary-ascl.6`.
   - Purpose: independent audit after implementation/discovery beads finish.

## Dependency graph

Created edges:

- `primary-ascl.1` blocks `primary-ascl.2`
- `primary-ascl.2` blocks `primary-ascl.7`
- `primary-ascl.3` blocks `primary-ascl.7`
- `primary-ascl.4` blocks `primary-ascl.7`
- `primary-ascl.5` blocks `primary-ascl.7`
- `primary-ascl.6` blocks `primary-ascl.7`

Attempted but rejected by `bd`:

- `primary-ascl.7` blocks `primary-ascl`
  - Result: failed with `epics can only block other epics, not tasks`.
  - Residual effect: parent epic remains open and child-linked, but not dependency-blocked by the audit task.

## Recommended assignment order

1. Dispatch immediately without another approval:
   - `primary-ascl.1` naming discovery.
   - `primary-ascl.3` launch-time orchestration injection implementation.
   - `primary-ascl.4` doctrine strengthening implementation.
   - `primary-ascl.5` read-only Spirit query/role composition implementation.
2. Dispatch `primary-ascl.6` when accepting lower-priority README backlog work, or before final audit if the parent bundle must close as one unit.
3. Dispatch `primary-ascl.2` only after `primary-ascl.1` finds approved replacements or psyche approves missing replacement names.
4. Dispatch `primary-ascl.7` only after `primary-ascl.2`, `primary-ascl.3`, `primary-ascl.4`, `primary-ascl.5`, and `primary-ascl.6` have closure evidence.

## Blockers and open questions

- Blocker for `primary-ascl.2`: approved replacements for one or more known bad names may be missing. `primary-ascl.1` must establish evidence or pause for psyche approval before renaming.
- Tracker graph limitation: `bd` rejected a task-to-epic blocking edge from the audit task to the parent epic. The audit is still properly blocked by implementation/discovery work; the parent epic closure must use child status and audit evidence manually.
- Coordination risk: `primary-ascl.3`, `primary-ascl.4`, and `primary-ascl.5` may touch overlapping generated-role/source-of-truth surfaces. Editing workers must claim paths/worktrees with Orchestrate before editing.

## Commands run

- `orchestrate "(Observe Roles)"` — passed; observed active claims.
- `orchestrate "(Claim (weave-operator [(Path /home/li/primary)] [create approved tracker weave for naming orchestration spirit bundle retry]))"` — passed; claimed workspace for tracker mutation.
- `bd --help`, `bd create --help`, `bd dep --help`, `bd list --help`, `bd show --help`, `bd ready --help` — passed; inspected narrow command usage.
- `bd list --title orchestration --status open,in_progress,blocked --long --no-pager -n 80` — passed; no matching open orchestration issues found by that title filter.
- `bd search naming`, `bd search "spirit query"`, `bd search "commit-message model provenance"` — passed; no actionable duplicate found from these searches.
- Seven `bd create ... --parent primary-ascl ...` commands and one parent `bd create ... -t epic ...` — passed; created `primary-ascl` through `primary-ascl.7`.
- `bd dep primary-ascl.1 --blocks primary-ascl.2` — passed.
- `bd dep primary-ascl.2 --blocks primary-ascl.7` — passed.
- `bd dep primary-ascl.3 --blocks primary-ascl.7` — passed.
- `bd dep primary-ascl.4 --blocks primary-ascl.7` — passed.
- `bd dep primary-ascl.5 --blocks primary-ascl.7` — passed.
- `bd dep primary-ascl.6 --blocks primary-ascl.7` — passed.
- `bd dep primary-ascl.7 --blocks primary-ascl` — failed; `bd` rejected task blocking epic.
- A parallel readback attempt using `/tmp/naming-orchestration-spirit-beads.ids` — failed because the creation script exited before writing the temp ID file after the rejected dependency; concurrent `bd` readbacks also hit the embedded-dolt lock. No mutation occurred in this failed readback.
- `bd list --parent primary-ascl --long --no-pager -n 20` — passed; confirmed all seven children are open under the parent.
- `bd dep list primary-ascl.1 primary-ascl.2 primary-ascl.3 primary-ascl.4 primary-ascl.5 primary-ascl.6 primary-ascl.7 primary-ascl` — passed; confirmed dependency edges.
- `bd ready --parent primary-ascl --explain -n 20` — passed; confirmed `primary-ascl.1`, `.3`, `.4`, `.5`, `.6` are dependency-ready and `.2`, `.7` are blocked.
- `bd show primary-ascl primary-ascl.1 primary-ascl.2 primary-ascl.3 primary-ascl.4 primary-ascl.5 primary-ascl.6 primary-ascl.7 --long` — passed; confirmed descriptions, labels, parent-child relations, and dependencies.
- `bd blocked | grep -E 'primary-ascl(\\.| )' || true` — passed; confirmed `.2` and `.7` as dependency-blocked.
- `jj status --no-pager` — passed; showed existing unrelated agent-output working-copy changes; no source changes from this task.
- `orchestrate "(Release weave-operator)"` — passed; released the workspace claim after tracker mutation and report writing.

## Final tracker status

- Changed beads: `primary-ascl`, `primary-ascl.1`, `primary-ascl.2`, `primary-ascl.3`, `primary-ascl.4`, `primary-ascl.5`, `primary-ascl.6`, `primary-ascl.7`.
- Closed beads: none.
- Beads left open: all eight created beads.
- Dependency-ready child beads for immediate dispatch: `primary-ascl.1`, `primary-ascl.3`, `primary-ascl.4`, `primary-ascl.5`; `primary-ascl.6` is also ready but intentionally P3 backlog.
- Blocked child beads: `primary-ascl.2` by `primary-ascl.1`; `primary-ascl.7` by `primary-ascl.2`, `.3`, `.4`, `.5`, `.6`.

## Review findings

- medium: tracker `primary-ascl` graph — `bd` rejected `primary-ascl.7 -> primary-ascl`; parent epic is not dependency-blocked by audit, so final closure must inspect child/audit evidence manually.
- no source-code or documentation blockers were reviewed because this assignment was tracker setup only.

## Residual risks

- Naming cleanup may require a psyche approval turn if prior replacement proposals are absent.
- Immediate implementation beads may contend on shared generator/doctrine surfaces unless claims/worktrees are coordinated.
- Parent epic appears ready to `bd ready` because the rejected task-to-epic edge could not be represented; dispatchers should treat only child task readiness as actionable.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Created tracker weave primary-ascl through primary-ascl.7 and reported concrete tracker findings with IDs, dependency status, and severity where applicable."
    }
  ],
  "changedFiles": [
    "/home/li/primary/.beads/",
    "/home/li/primary/agent-outputs/orchestration-weave/naming-orchestration-spirit-bundle-retry.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "orchestrate observe/claim/release; bd help/search/list; bd create parent and seven children; bd dep edges; bd list/dep/show/ready/blocked; jj status",
      "result": "passed-with-one-expected-blocker",
      "summary": "Tracker weave created and verified; bd rejected the audit-task-to-parent-epic dependency edge."
    }
  ],
  "validationOutput": [
    "bd show confirmed primary-ascl parent with seven open children and dependencies.",
    "bd blocked confirmed primary-ascl.2 blocked by primary-ascl.1 and primary-ascl.7 blocked by primary-ascl.2-.6.",
    "bd ready showed primary-ascl.1, .3, .4, .5, and .6 dependency-ready; .6 is P3 backlog."
  ],
  "residualRisks": [
    "Naming cleanup may need psyche approval if prior replacement proposals are missing.",
    "Parent epic is not dependency-blocked because bd rejected task-to-epic blocking; closure must inspect child and audit evidence manually.",
    "Potential edit coordination conflicts among launch/doctrine/Spirit implementation beads."
  ],
  "noStagedFiles": true,
  "diffSummary": "Tracker database updated with one parent epic, seven child beads, and six dependency edges; report file written.",
  "reviewFindings": [
    "medium: tracker primary-ascl graph - bd rejected primary-ascl.7 blocking epic primary-ascl, leaving the parent open but not dependency-blocked.",
    "no source-code blockers reviewed; tracker setup only."
  ],
  "manualNotes": "No source implementation, audit, closure, commit, or push was performed. Existing unrelated jj working-copy changes were present under agent-outputs before this report was written."
}
```
