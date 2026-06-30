# Scout Launch Brief

Task: get situated for launching epic `primary-5rzf`, Workspace staleness/deprecation sweep (P1), without doing sweep work.

Scope checked: the supplied handoff and tracker surfaces for `primary-5rzf` and its child beads. I did not inspect `private-repos/`, Spirit records, source repos, docs, skills, or code surfaces.

## Evidence Consulted

- Handoff: `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md` via `sed -n`.
- Tracker command availability: `command -v bd`, `bd --help`.
- Tracker state: `bd --readonly --json show primary-5rzf`, `bd --readonly --json children primary-5rzf`, `bd --readonly --json graph primary-5rzf`, `bd --readonly --json ready`.
- Output directory state: `ls -la /home/li/primary/agent-outputs/WorkspaceStalenessSweep`.
- Doctrine read because the task names bead tracker work: `/home/li/primary/.agents/skills/beads/SKILL.md` via `sed -n`.

Note: an initial parallel tracker read hit the embedded Dolt lock for some commands; the failed reads were retried serially with `--readonly` and succeeded.

## Observed Facts

- Epic `primary-5rzf` is open, priority 1, type `epic`, with nine child beads. `bd --readonly --json show primary-5rzf` reports `epic_total_children: 9`, `epic_closed_children: 0`, and `epic_closeable: false`.
- `bd --readonly --json ready` lists `primary-5rzf.1`, `primary-5rzf.2`, and `primary-5rzf.3` as ready child tasks with `dependency_count: 0`.
- `primary-5rzf.1`, `.2`, and `.3` are all open, priority 1, labeled `audit-readonly`, and each says it has no dependencies among the three Phase-1 sweeps and blocks the verifier bead.
- `primary-5rzf.4` is open and blocked by `.1`, `.2`, and `.3`; it is labeled `verification-gate` and is described as the only deletion gate.
- `primary-5rzf.5`, `.6`, `.7`, and `.8` are open and each depends on `.4`.
- `primary-5rzf.9` is open and depends on `.5`, `.6`, and `.7`, not `.8`.
- `ls -la /home/li/primary/agent-outputs/WorkspaceStalenessSweep` shows only `Handoff-CodexEpicHandoff.md`; no Phase-1 candidate files, verifier ledger, kill evidence, suspect-ruling, or closeout evidence exist yet.

## Interpretation

Ready to launch now: `primary-5rzf.1`, `primary-5rzf.2`, and `primary-5rzf.3`.

Blocked until Phase-1 output exists and dependencies close or are otherwise marked complete in the tracker: `primary-5rzf.4`.

Blocked until verifier ledger exists and `.4` is complete: `primary-5rzf.5`, `primary-5rzf.6`, `primary-5rzf.7`, and `primary-5rzf.8`.

Blocked until the three kill beads complete: `primary-5rzf.9`. The suspect-ruling bead `.8` does not block closeout.

The handoff and tracker agree on the graph, the evidence-anchored four-part rule, the read-only nature of Phase 1, the private boundary, and the verifier-only deletion gate. I found no contradiction between handoff and tracker state in the inspected surfaces.

## Worker-Facing Launch Boundaries For `.1`, `.2`, `.3`

Common boundaries for all three Phase-1 workers:

- Do read-only audit only. Produce no deletions, edits, tracker changes, claims, commits, or pushes.
- Do not inspect `private-repos/`. If a candidate seems to require private scope, flag the boundary in the output and stop there.
- Do not sweep Spirit intent records.
- Apply the evidence-anchored rule: a confirmed candidate must name all four parts: the new thing, the old thing it killed, a locator, and evidence. Evidence must be a rename, finished effort still described as active, explicit deprecate/replace/supersede statement, or landed work making the old shape dead.
- No hunches on the confirmed track. Anything missing one of the four parts goes to `SUSPECT`, not `CANDIDATES`.
- Keep `CANDIDATES` and `SUSPECTS` clearly separated in the output.
- Write output under `agent-outputs/WorkspaceStalenessSweep/` and state the commands/searches run.

`primary-5rzf.1` Tracker sweep:

- Surface: tracker only, using read-only `bd` queries across open and recently closed issues and epics.
- Find finished-but-open efforts, dead-name tracker items, superseded tracker items, and mystery items.
- For mystery items, include an origin trace: who created it, when, and what it links to or was discovered from.
- Output: `agent-outputs/WorkspaceStalenessSweep/TrackerSweep-Candidates.md`.
- Success criteria: file contains `CANDIDATES` entries with new thing, old thing, issue-id locator, and evidence; `SUSPECTS` entries for plausible but incomplete cases; origin traces for mystery items; and the `bd` queries run.

`primary-5rzf.2` Skills and docs sweep:

- Surface: skill source modules that generate runtime `.claude/skills/*`, `AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`, `README` files, and generated runtime skill surfaces.
- Generated surfaces may be inspected but not edited. Flag hits as source vs generated, because later edits must happen in source and then reconcile generated output.
- Find replaced or renamed terms and guidance describing dead shapes.
- Output: `agent-outputs/WorkspaceStalenessSweep/DocsSkillsSweep-Candidates.md`.
- Success criteria: file contains `CANDIDATES` and `SUSPECTS`, with new thing, old thing, path/section locator, evidence, source-vs-generated flag for each hit, and search commands run.

`primary-5rzf.3` Code sweep:

- Surface: tracked workspace code only.
- Report which repos were covered.
- Stop at `private-repos/`; do not enter it.
- Find deprecated APIs still present after replacement, old types/modules/paths left after a new shape replaced them, and dead consumers.
- Output: `agent-outputs/WorkspaceStalenessSweep/CodeSweep-Candidates.md`.
- Success criteria: file contains a `REPOS COVERED` list, `CANDIDATES` and `SUSPECTS` with new thing, old thing, repo/path/line-or-symbol locator, evidence, private-boundary flags if any, and commands/repos searched.

## Missing Authority Or Psyche Questions

No missing psyche authority blocks launching `.1`, `.2`, or `.3`. The handoff and tracker both state the audit authority and boundaries, and Phase 1 is read-only.

Deletion authority is intentionally absent from Phase 1 and should not be requested now. Deletion is gated only by `.4` after the verifier produces `agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`.

Unverified due to the scout boundary: I did not validate Spirit record `10pz`, did not inspect source repos/docs/code, and did not inspect tracker issues outside what `bd` returned for the epic and global ready list.
