# Blocker Analysis

Task: read-only analysis of the two current blockers for epic `primary-5rzf`: tracker kill bead `primary-5rzf.5` and code kill bead `primary-5rzf.7`.

Scope limits followed: no tracker mutation, no close, no force-close, no claim, no commit, no push, no `/home/li/primary/private-repos` inspection, and no Spirit intent sweep. The only file written is this requested report.

## Evidence Consulted

Files read:

- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/TrackerKill-Evidence.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/CodeKill-Evidence.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/CodeKill-Audit.md`

Read-only tracker commands:

- `bd --readonly show primary-5rzf.5 primary-5rzf.7 primary-2chb primary-2y5 primary-pg6f --long --json`
- `bd --readonly show primary-2chb --long --json`
- `bd --readonly show primary-2y5 --long --json`
- `bd --readonly show primary-pg6f --long --json`

Initial concurrent `bd show` attempts hit the embedded tracker database lock for several ids. The successful evidence above came from serialized read-only commands.

## Blocker .5: `primary-2chb` Blocked By `primary-2y5`

Observed facts:

- `primary-5rzf.5` is still `in_progress`.
- `TrackerKill-Evidence.md` records that five of six confirmed tracker-kill entries were closed. The remaining entry is T6, `primary-2chb`.
- The attempted close of `primary-2chb` failed with: `cannot close primary-2chb: blocked by open issues [primary-2y5] (use --force to override)`.
- `primary-2chb` is open and titled `Deploy persona-orchestrate as workspace user service`.
- `primary-2chb` depends on `primary-2y5` (`in_progress`), `primary-c620` (`closed` as superseded by the schema-emission porting plan), and `primary-wvdl` (`closed` as superseded by the schema-emission porting plan).
- The body of `primary-2chb` says it should run after `primary-c620` lands and `primary-2y5` ships, and its constraints say not to deploy without the Persona supervisor.
- `primary-2y5` is the Persona daemon work: `EngineId socket setup, manager redb, spawn envelope`. It remains `in_progress`; its closed child beads show substantial progress, but the parent is not closed.

Interpretation:

- `primary-2y5` blocks `primary-2chb` because the old `primary-2chb` plan deploys `persona-orchestrate-daemon` as a Persona-supervised child, and that deployment requires the Persona daemon/supervisor to ship first.
- The verifier did not say `primary-2y5` is stale. It said `primary-2chb` is stale because its `/151` persona-orchestrate readiness/deploy framing was superseded by second-designer 162 consolidation and the schema-emission porting plan.
- A normal close of `primary-2chb` as completed would violate the tracker graph: its live prerequisite `primary-2y5` has not shipped.
- A force-close of `primary-2chb` as explicitly invalidated/superseded does not violate local bead discipline, because the bead discipline allows closure after acceptance passes or after the bead is explicitly invalidated. The close reason must make clear that the dependency edge is obsolete because the dependent work item is dead, not because `primary-2y5` is done.

Recommendation for `.5`:

- Do not resolve `primary-2y5` inside this weave; that is larger live Persona daemon work.
- An authorized non-read-only weave operator should force-close `primary-2chb` with a supersession/invalidation reason citing verifier T6, then close `primary-5rzf.5` if read-back confirms the six tracker-kill entries are closed.
- Consequence: `primary-2y5` remains open and truthful; the stale dependent deployment bead stops surfacing as live tracker work.

## Blocker .7: `primary-pg6f` Worktree Disposition

Observed facts:

- `primary-5rzf.7` is still `in_progress`.
- `CodeKill-Evidence.md` records C1, C2, and C4 changes in canonical/touched paths, and C3 changed only in isolated worktree `/git/github.com/LiGoldragon/lojix-primary-5rzf-7`.
- `CodeKill-Audit.md` says the `persona-message` fixed-output hash mismatch is unrelated to `.7`, but C3 remains unresolved in canonical `/git/github.com/LiGoldragon/lojix/README.md`.
- `CodeKill-Audit.md` says the isolated README has `horizon-leaner-shape`, while canonical `/git/github.com/LiGoldragon/lojix/README.md` still has `horizon-re-engineering`.
- `primary-pg6f` is open and says: `/git/github.com/LiGoldragon/lojix; branch/workspace primary-5rzf-7-code-kill; worktree /git/github.com/LiGoldragon/lojix-primary-5rzf-7; disposition needed: partial merge of README.md cleanup for primary-5rzf.7, or discard if closeout chooses another integration path.`

Interpretation:

- `primary-pg6f` already tracks the exact missing disposition. A new bead is not needed.
- `.7` should remain blocked on `primary-pg6f` until canonical `lojix/README.md` no longer points new work at `horizon-re-engineering`.
- It is not safe to close or force-close `.7` now: that would leave a verifier-confirmed stale code/docs reference in the canonical in-scope repo.
- The isolated work can be folded into this epic only through the `primary-pg6f` disposition path: either partially merge the README cleanup into canonical `lojix` under coordination, or discard the isolated worktree only after another integration path fixes the canonical README and verifies the grep.

Recommendation for `.7`:

- Follow `primary-pg6f`; do not force-close `.7`.
- Preferred disposition is a coordinated partial merge of the isolated README cleanup into canonical `/git/github.com/LiGoldragon/lojix/README.md`, followed by a canonical grep for `horizon-re-engineering`.
- If closeout chooses a different integration path, keep `primary-pg6f` open until that path is executed and the isolated worktree is explicitly discarded or otherwise resolved.

## Lowest-Risk Next Action

Lowest-risk path:

1. For `.5`, authorize a weave operator to force-close only `primary-2chb` as invalidated/superseded, not completed, then close `primary-5rzf.5` after read-back.
2. For `.7`, keep the bead open and follow existing bead `primary-pg6f` to land or discard the isolated `lojix` worktree change only after canonical `lojix/README.md` is corrected.
3. Do not stop the whole epic as permanently blocked. After `.5` is force-closed correctly, the material blocker is `primary-pg6f`.

Not recommended:

- Do not resolve `primary-2y5` inside this weave; it is live Persona daemon scope, not tracker-kill cleanup.
- Do not force-close `.7`; canonical C3 is still stale.
- Do not create another bead for `.7`; `primary-pg6f` already exists and is precise.

## Psyche Decision

No new stale-kill decision is required from the psyche for `.5` or `.7`; both are already verifier-gated. A psyche or repo-owner decision is only needed if the operator wants to discard the isolated `lojix` worktree without landing its README cleanup and use a different canonical integration path instead.
