# Workspace cleanup batch plan — 2026-07-28

## Decision boundary

**No cleanup is authorized by this plan.** It is a read-only consolidation of
`estate-inventory-2026-07-28.md`, `recovery-map-2026-07-28.md`,
`workspace-cleanup-classification-a-2026-07-28.md`,
`workspace-cleanup-classification-b-2026-07-28.md`, and
`orchestrate-reliability-proposal-2026-07-28.md`, with a small read-only check
of the remaining workspace surfaces.

The classifications concern physical workspace retention only. They do not
retire a component, a remote branch, a bookmark, a deployment, or a commit.
All remote facts are last locally known: no fetch occurred.

## Corrected physical-extra workspace count

The actionable physical scope is **47 extra workspace-like directories**, not
215 worktrees. An *extra workspace-like directory* is a physical directory in
addition to its canonical repository root: a detached Jujutsu workspace, a
physical root backing a non-default primary registration, or the one linked
Git worktree tracked outside the primary Jujutsu repository.

| Physical-extra unit | Preserve | Owner decision | Conditionally cleanup-eligible after approval | Total |
| --- | ---: | ---: | ---: | ---: |
| Detached Jujutsu workspaces under `/git/github.com/LiGoldragon` | 7 | 12 | 23 | 42 |
| Physical roots backing non-default primary registrations | 0 | 4 | 0 | 4 |
| Linked Git worktree outside the primary Jujutsu repository | 0 | 1 | 0 | 1 |
| **Extra physical workspace-like directories** | **7** | **17** | **23** | **47** |

The 166 canonical repository roots are context, not extra workspaces: 164 are
ordinary preserved repository checkouts (including the five dirty roots), and
two stale Lojix roots need an owner decision because assessing their
working-copy state would require a state-changing refresh. Likewise, there are
six non-default primary *registry records*, but only four have a discovered
physical root; the other two are records without a discovered physical root.

### Withdrawn mixed tally

The earlier **“215 surfaces / 171 preserve”** arithmetic is withdrawn as a
workspace or physical-directory summary. It mixed unlike units: 215 was 166
canonical roots + 42 detached Jujutsu workspaces + 6 registry records + 1
Git-linked orphan; 171 was 164 canonical preserves + 7 detached-workspace
preserves. It may only be understood as that retired mixed inventory tally,
never as a count of physical worktrees or cleanup candidates.

### Preserve (7 physical extras; canonical context noted separately)

- Canonical-root context, excluded from the 47: all clean roots and the dirty
  `/git/github.com/LiGoldragon/{CriomOS-test-cluster,TheBookOfSol,meta-signal-mind,meta-signal-persona,schema}`.
- Stale canonical-root context, also excluded from the 47:
  `/git/github.com/LiGoldragon/{meta-signal-lojix,signal-lojix}` need a
  repair-versus-retire decision before refresh.
- Three detached dirty dotted-syntax pilots:
  `/git/github.com/LiGoldragon/{meta-signal-spirit-schema-dotted-syntax-pilot,signal-spirit-schema-dotted-syntax-pilot,spirit-schema-dotted-syntax-pilot}`. Their distinct `ARCHITECTURE.md` changes must be compared and deliberately dispositioned.
- Four detached C2 deployment/test-evidence workspaces:
  `/git/github.com/LiGoldragon/{CriomOS-spirit-domain-all,CriomOS-spirit-judge-deploy,CriomOS-home-spirit-domain-all,CriomOS-test-cluster-spirit-domain-all}`. Their parents have no canonical-main successor and retain fixed stack, judge-chain, deployment-check, or test-stack evidence.

### Owner decision required (17 physical extras; two canonical roots and two registry-only records are context)

- C1 unlanded Schema 0.3 migrations:
  `/git/github.com/LiGoldragon/{meta-signal-criome-mentci-contract-migration,meta-signal-mentci-client-mentci-signal-family-migration,meta-signal-mentci-mentci-signal-family-migration,signal-criome-mentci-contract-migration,signal-mentci-mentci-signal-family-migration}`.
- C2 unlanded/preserved-branch work:
  `/git/github.com/LiGoldragon/{signal-domain-schema-dotted-syntax-pilot,spirit-judge-hardening,pi-subagents-nested-roles-preference-training,pi-subagents-nicobailon-closeout,pi-subagents-nicobailon-optional-list-consistency}`. The two Pi paths with `node_modules` require an explicit cache-retention decision; the cache is rebuildable but substantial.
- Unclassified clean Mentci workspaces:
  `/git/github.com/LiGoldragon/{mentci-current-graph-integration,mentci-dependency-cascade}`. Each has an empty clean working copy whose parent equals that workspace's local `main`, but neither has the A/B artifact-and-owner proof. Do not promote either from this plan.
- Four physical primary-registration roots: existing substantial workspaces
  `/home/li/{mind-live-judge-eval-rerun,primary-worktrees/mind-judge-fixture-label-cleanup,primary-worktrees/MindJudgePromptRewrite-TargetedSecondPass,primary-worktrees/MindJudgePromptRewrite-NarrowThirdPass}` and two registrations without a discovered physical root, `primary-fix-audit-stale-repo-operator` and `primary-fix-audit-stale-repo-operator-v2`. The existing four contain retained `.beads`, reports, agent outputs, and source material even though their recorded `@` is empty; they need an owner/retention review.
- Orphan-like linked Git worktree:
  `/git/github.com/LiGoldragon/synchronizer-release-train-p0-p2`, including
  its linked metadata under
  `/git/github.com/LiGoldragon/synchronizer/.git/worktrees/synchronizer-release-train-p0-p2`.
  It has a Git branch identity, `release-train-p0-p2`, and contains `.agents`,
  `.beads`, reports, and agent outputs. That branch is fully merged into
  `main`, so the concern is retention of the leftover physical worktree and
  its retained material, not a missing identity. Do not prune its Git
  metadata or move it until owner and archive decision are known.

### Likely cleanup-eligible after approval

These 23 paths were clean with an empty recorded working copy, had no
workspace-only artifacts in the A/B checks, and had the exact parent change on
or ancestral to their canonical local main. This is evidence for later
reclamation, not present permission.

```text
/git/github.com/LiGoldragon/mentci-lib-cargo-migration
/git/github.com/LiGoldragon/mentci-lib-mentci-signal-family-migration
/git/github.com/LiGoldragon/meta-signal-criome-cargo-source-repair
/git/github.com/LiGoldragon/meta-signal-mentci-cargo-source-repair
/git/github.com/LiGoldragon/meta-signal-mentci-client-cargo-source-repair
/git/github.com/LiGoldragon/signal-criome-cargo-source-repair
/git/github.com/LiGoldragon/signal-mentci-cargo-source-repair
/git/github.com/LiGoldragon/signal-message-cargo-source-repair
/git/github.com/LiGoldragon/signal-persona-cargo-source-repair
/git/github.com/LiGoldragon/signal-router-cargo-source-repair
/git/github.com/LiGoldragon/signal-terminal-dependency-cascade
/git/github.com/LiGoldragon/terminal-cell-dependency-cascade
/git/github.com/LiGoldragon/schema-structural-pipe-retirement
/git/github.com/LiGoldragon/CriomOS-listener-criome-recovery
/git/github.com/LiGoldragon/CriomOS-home-laptop-colemak-merge
/git/github.com/LiGoldragon/CriomOS-home-listener-criome-recovery
/git/github.com/LiGoldragon/CriomOS-home-listener-zddv4
/git/github.com/LiGoldragon/lojix-inspect-store
/git/github.com/LiGoldragon/meta-signal-mind-mind-judge-diagnostic
/git/github.com/LiGoldragon/meta-signal-orchestrate-session-lane-clear
/git/github.com/LiGoldragon/mind-domain-all-repin
/git/github.com/LiGoldragon/orchestrate-session-lane-storage
/git/github.com/LiGoldragon/orchestrate-writer-ordering
```

## Cross-cutting risk and contradictions

- The current live Worktree registry lists many active or abandoned worktrees
  under `/home/li/wt/...`; the A/B classifications found no record for their
  37 classified `/git/...` paths. The current observation implementation is
  itself not a durable, pure historical witness, so absence from a snapshot is
  not proof that a path is lifecycle-safe.
- Current `ConcludeWorktree Rejected` is unsafe for this task. Its source
  snapshots working-copy state, can describe it, creates and pushes a
  `discard/<branch>` bookmark, forgets the workspace, recursively removes its
  directory, and deletes local bookmarks. `Merged` can fetch, rebase, advance
  `main`, and push. Neither disposition is an acceptable cleanup primitive.
- The current registry reaps terminal rows and has filesystem-based stale-path
  behavior. Therefore it cannot provide the required durable mapping from an
  old physical path to a past owner or conclusion.
- Main-tracking divergence in several C1 canonical repositories, deleted
  bookmark markers elsewhere, and Pi's differing `upstream` are reconciliation
  questions only. This plan deliberately makes **no** bookmark, remote, fetch,
  push, merge, or prune action.

## Future batch sequence

Every batch is conditional on all preflight gates below. Execute paths one at
a time; a failed gate ends the batch with no action on later paths.

| Batch | Exact paths | Why this order |
| --- | --- | --- |
| B1 — first proposed batch (3) | `meta-signal-criome-cargo-source-repair`; `meta-signal-mentci-cargo-source-repair`; `meta-signal-mentci-client-cargo-source-repair` | The three strongest C1 cases: empty clean children; their two-file Cargo-source repairs are exactly canonical local main; no unique material found. |
| B2 (10) | `mentci-lib-cargo-migration`; `mentci-lib-mentci-signal-family-migration`; `signal-criome-cargo-source-repair`; `signal-mentci-cargo-source-repair`; `signal-message-cargo-source-repair`; `signal-persona-cargo-source-repair`; `signal-router-cargo-source-repair`; `signal-terminal-dependency-cascade`; `terminal-cell-dependency-cascade`; `schema-structural-pipe-retirement` | Remaining C1 candidates, after B1 validates the repaired procedure on the smallest low-retention set. |
| B3 (7) | `CriomOS-listener-criome-recovery`; `CriomOS-home-laptop-colemak-merge`; `CriomOS-home-listener-criome-recovery`; `CriomOS-home-listener-zddv4`; `lojix-inspect-store`; `meta-signal-mind-mind-judge-diagnostic`; `mind-domain-all-repin` | C2 candidates with a canonical successor, separated from the Orchestrate-owned paths and from preserved deployment evidence. |
| B4 (3) | `meta-signal-orchestrate-session-lane-clear`; `orchestrate-session-lane-storage`; `orchestrate-writer-ordering` | Run last, only after the state-only lifecycle repair and receipt witness have been independently proved. |

All paths in the table are relative to `/git/github.com/LiGoldragon/`.
No other path is in any batch. In particular, the two unclassified Mentci
workspaces, all dirty/stale paths, all primary workspaces, and the orphan-like
Git worktree remain out of scope.

## Per-path preflight and proof, immediately before any removal

For the one candidate currently being processed, capture a non-content
receipt/manifest outside the candidate, then stop if any condition is false:

1. Re-read the approved batch manifest and verify an exact path match; resolve
   the real path and reject a symlink, missing path, path outside
   `/git/github.com/LiGoldragon`, or unexpected workspace name.
2. Use Jujutsu's non-snapshotting reads only: `jj -R <path> --ignore-working-copy
   status`, `log -r @`, `log -r @-`, parent-to-canonical-main ancestry, and
   `diff --summary`. Re-run the A/B no-extra-material comparison. A non-empty
   `@`, working-copy modification, changed parent, non-ancestor, untracked or
   ignored material, or unexpected bookmark stops the path.
3. Use the repaired **pure** lifecycle history to map the exact path,
   repository, owning lane, and prior disposition. Any active/unknown record,
   another open claim, a conflicting owner, or lack of a durable receipt stops
   the path. Do not use the current reconciliating observer as this proof.
4. Confirm the owner disposition names this exact path and says the underlying
   change is retained on canonical main. Confirm no archive is needed. The
   only planned archive is the receipt bundle: path, real path, Jujutsu IDs,
   status/diff summaries, file-list comparison result, lifecycle receipt ID,
   time, and executor. Do not copy source or private artifacts into a report.
5. Reconfirm that no command will fetch, push, set/delete a bookmark, alter a
   remote, merge/rebase, update a stale workspace, mutate beads, or touch a
   non-listed path.

The current classifications make a content archive unnecessary for the 23
eligible paths **only if this immediate proof repeats successfully**. If that
proof finds material, archive/retention becomes a new owner decision, not a
batch exception.

## Two future routes

### A. Recommended: after the state-only Orchestrate repair is deployed

This route begins only after the reliability proposal's pure control-plane and
append-only lifecycle receipts are deployed and an authorized disposable
Request → Claim → Release → Rejected-conclusion witness proves that the daemon
performed no filesystem, bookmark, fetch, or push effect.

For each approved path: record a state-only `Rejected` conclusion with the
exact immutable main-successor reference; preserve its receipt; then have the
authorized executor perform the local Jujutsu workspace detachment and a
recoverable filesystem move to the approved trash/quarantine destination.
The executor must not delete a bookmark. The physical move is a distinct,
explicitly approved action, not an Orchestrate side effect.

Rollback before emptying trash/quarantine is limited but straightforward:
restore the directory to its exact path and re-add/re-register the workspace
at the recorded revision under the repaired lifecycle. After trash is emptied,
rollback relies on the canonical main ancestor and the Jujutsu operation/store
history; it cannot reconstruct unrecorded workspace-only files. This is why
the immediate file-material proof is a stop gate.

### B. Current manual Jujutsu-only route: not permitted by current doctrine

No compliant manual escape is presently available. The active local protocol
directs worktree lifecycle through Orchestrate and says to conclude a rejected
worktree; the deployed conclusion has the unsafe filesystem and remote effects
described above. The version-control doctrine requires Jujutsu for ordinary
history but does not independently authorize bypassing the lifecycle/owner
boundary. Therefore do **not** substitute `jj workspace forget`, direct
directory removal, Git worktree pruning, or bookmark manipulation today.

An explicitly approved policy amendment could create a manual Jujutsu-only
route, but must first state its owner/receipt requirements, exact allowed
workspace operations, recoverable removal mechanism, no-bookmark/no-remote
rule, and rollback retention. Until then, B1–B4 have no executable manual
route.

## Stop conditions

Stop the current path and the rest of its batch on any of the following:

- missing or mismatched explicit approval; owner changes their disposition;
- current dirty/non-empty/stale state, unexpected artifact, or failed
  canonical-main ancestry proof;
- absent/ambiguous lifecycle receipt, active claim/lane, or registry conflict;
- any request/reply that is not demonstrably state-only;
- any proposed fetch, push, bookmark operation, merge/rebase, Git metadata
  prune, stale-workspace update, or beads mutation;
- inability to use a recoverable quarantine/trash action; or
- any path outside the exact batch manifest.

## Exact approval text

> I authorize **only cleanup plan B1** for these exact paths:
> `/git/github.com/LiGoldragon/meta-signal-criome-cargo-source-repair`,
> `/git/github.com/LiGoldragon/meta-signal-mentci-cargo-source-repair`, and
> `/git/github.com/LiGoldragon/meta-signal-mentci-client-cargo-source-repair`.
> This authorization is effective only after the repaired state-only
> Orchestrate lifecycle and its disposable rejected-conclusion witness are
> proved. For each path, repeat the plan's immediate preflight, record the
> receipt bundle, require a clean empty workspace with no unique material and
> a canonical-main successor, record a state-only Rejected disposition, then
> detach and move only that workspace to the approved recoverable quarantine.
> Do not fetch, push, merge, rebase, create/set/delete any bookmark, prune Git
> metadata, update stale workspaces, modify beads, or touch any other path.
> Stop the whole batch on the first failed gate. No later batch is authorized.

Without this (or a narrower) approval, **no cleanup is authorized**.
