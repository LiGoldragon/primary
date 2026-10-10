# Lojix Deploy Readiness Remediation Work Breakdown

Task and scope: create/update tracker coordination for remediation from `/home/li/primary/agent-outputs/LojixFullTestBackedAudit/OperatingSystemImplementer-Audit.md`; check local coordination and visible repo ownership before recommending implementation; do not edit code or run live/state-changing Lojix operations.

## Sources Consulted

- `/home/li/primary/agent-outputs/LojixFullTestBackedAudit/OperatingSystemImplementer-Audit.md`
- `orchestrate "(Observe Roles)"`
- `spirit "(PublicTextSearch [Lojix operating system deploy readiness])"`
- `bd --help`, `bd create --help`, `bd dep --help`, `bd note --help`
- `bd list --readonly --all --no-pager --long --title-contains lojix --limit 50`
- `bd list --readonly --all --no-pager --long --title-contains skills --limit 80`
- `bd show primary-3xwk`, `bd show primary-wgae`, `bd show primary-gss3`, `bd show primary-53pz`
- `jj status` in the likely involved repos listed below
- `bd list --readonly --no-pager --long --id primary-sjmr,primary-3nen,primary-04rx,primary-anr3,primary-agkc,primary-3xwk --limit 20`
- `bd dep list primary-agkc`, `bd dep list primary-anr3`, `bd dep list primary-3xwk`

Spirit query result: public intent search returned broad engineering principles including design toward the best end shape and replacing obsolete shapes rather than preserving parallel legacy. No private intent was read.

## Coordination And Busy Findings

Orchestrate ownership: no formal Orchestrate claims were visible on `/home/li/primary`, `/git/github.com/LiGoldragon/skills`, `/git/github.com/LiGoldragon/lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/CriomOS-test-cluster`, `/git/github.com/LiGoldragon/CriomOS`, or `/home/li/worktrees/lojix-holistic-test-cluster`. The only visible path claim was unrelated: `/git/github.com/LiGoldragon/cloud`.

Visible repo status:

- `/home/li/primary`: busy. `jj status` shows many untracked `agent-outputs/` and `worktrees/worker-landing-loop/` files. Doctrine/generation workers should not share this checkout casually; claim the exact primary path before editing generated surfaces or use an isolated JJ workspace/disposition bead if concurrent main work cannot be paused.
- `/git/github.com/LiGoldragon/skills`: busy. Dirty files: `flake.nix`, `manifests/skills-roster.nota`, `modules/orchestration/full.md`, `tests/generation.rs`. The doctrine worker should wait for this work to land or use an isolated main-based worktree/workspace with a disposition bead and explicit claim.
- `/git/github.com/LiGoldragon/lojix`: not visibly busy. `jj status` reports no changes. A store-inspection worker may claim this repo when assigned.
- `/git/github.com/LiGoldragon/meta-signal-lojix`: busy. Dirty files: `Cargo.lock`, `src/schema/lib.rs`. Avoid unless the store-inspection or fixture work proves a contract change is required; then wait or use an isolated workspace.
- `/git/github.com/LiGoldragon/signal-lojix`: busy. Dirty file: `src/schema/lib.rs`. Avoid unless contract changes are required; then wait or use an isolated workspace.
- `/git/github.com/LiGoldragon/CriomOS-test-cluster`: busy. Dirty files include `clusters/fieldlab.nota`, `fixtures/horizon/atlas.json`, `flake.nix`, `lib/nestedReachability.nix`, and `lib/nestedSpike.nix` on a `nested-vm-reachability` working copy. The VM smoke worker should wait for this branch/worktree to settle or use an isolated main-based worktree/workspace with a new disposition bead and claim.
- `/home/li/worktrees/lojix-holistic-test-cluster`: clean but already tracked by open bead `primary-53pz` for disposition. Do not reuse for new remediation unless that bead is explicitly updated to include the new scope.
- `/git/github.com/LiGoldragon/CriomOS`: not visibly busy. It was included because the audit referenced CriomOS docs. No remediation bead currently requires editing it.

## Tracker Mutations

Created:

- `primary-sjmr` open P1: Lojix deploy doctrine: regenerate Host/UserEnvironment operating-system guidance.
- `primary-3nen` open P1: CriomOS-test-cluster: update lojix deploy smoke to current contract.
- `primary-04rx` open P1: Lojix inspect-store: report sema table decode health read-only.
- `primary-anr3` open P1: Lojix legacy store fixture: prove migration-required diagnosis.
- `primary-agkc` open P1: Lojix VM quality gate: prove current deploy path before live remediation.

Updated:

- `primary-3xwk` remains open P3. Added an audit note that `GenerationUnknown (0 0)` is more likely generation/event-log table decode/schema/read health than wrong node/query shape, and that live reconciliation should wait for blockers `primary-04rx`, `primary-anr3`, and `primary-agkc`.

Dependency graph:

```text
primary-3nen  -> primary-agkc
primary-04rx  -> primary-agkc
primary-04rx  -> primary-anr3
primary-agkc  -> primary-3xwk
primary-anr3  -> primary-3xwk
```

Readback confirmed:

- `primary-agkc` depends on `primary-04rx` and `primary-3nen`.
- `primary-anr3` depends on `primary-04rx`.
- `primary-3xwk` depends on `primary-agkc` and `primary-anr3`.
- All six affected beads are open; none were closed.

## Recommended Worker Split

1. Doctrine/generation worker: `primary-sjmr`.
   Repo scope: `/git/github.com/LiGoldragon/skills` and `/home/li/primary`.
   Should wait or use an isolated workspace because both repos are visibly dirty. Claim exact paths/workspace before editing. Acceptance is generated operating-system doctrine using `Host`/`UserEnvironment`, `SourceRevisionPolicy`, and `DeployAccepted`, with `generated-skills-current` passing.

2. VM smoke worker: `primary-3nen`.
   Repo scope: `/git/github.com/LiGoldragon/CriomOS-test-cluster`; touch `lojix`, `signal-lojix`, or `meta-signal-lojix` only if the test cannot consume current interfaces otherwise.
   Should wait or use a new isolated main-based worktree/workspace because the main test-cluster checkout is dirty and an existing clean worktree has open disposition bead `primary-53pz`. Acceptance is a current `Host`/`UserEnvironment` VM smoke proving `DeployAccepted` and activation/profile/query evidence.

3. Store inspection worker: `primary-04rx`.
   Repo scope: `/git/github.com/LiGoldragon/lojix`; avoid dirty signal/meta repos unless contract decode changes are required.
   May proceed after claiming `/git/github.com/LiGoldragon/lojix` because it is clean and unclaimed. Acceptance is a read-only inspect-store command/helper reporting table decode health and row counts without mutating the inspected store.

4. Legacy fixture diagnosis worker: `primary-anr3`.
   Repo scope: `/git/github.com/LiGoldragon/lojix`, after `primary-04rx`.
   Should wait for the inspect-store shape. Acceptance is fixture-backed proof that legacy/incompatible generation/event-log state yields a precise migration-required/schema-mismatch diagnostic instead of `GenerationUnknown (0 0)`.

5. Current VM quality-gate worker: `primary-agkc`.
   Repo scope: `/git/github.com/LiGoldragon/CriomOS-test-cluster` plus `/git/github.com/LiGoldragon/lojix` only for a local package/test hook.
   Must wait for `primary-3nen` and `primary-04rx`. Acceptance is a contained VM check exercising current deploy input, `SourceRevisionPolicy`, `DeployAccepted`, activation/profile evidence, `ByNode` query evidence, and read-only inspection evidence.

6. Live reconciliation worker: existing `primary-3xwk`.
   Repo/state scope: live `/var/lib/lojix/lojix.sema` and current Lojix tooling.
   Must wait for `primary-agkc` and `primary-anr3`, then still needs explicit live-state approval and backup before any state-changing remediation.

## Coordination Constraints

- No implementation worker should run live deploys or state-changing Lojix operations as part of these beads unless a later dispatch explicitly authorizes that scope.
- Dirty repos without Orchestrate claims still count as busy. Workers should not share those checkouts; either wait, or create an isolated main-based worktree/JJ workspace, claim it, and file/update a disposition bead.
- Contract repos `signal-lojix` and `meta-signal-lojix` are dirty. Treat them as off-limits unless a worker proves they are required for the assigned acceptance criteria.
- The clean `/home/li/worktrees/lojix-holistic-test-cluster` path is not free capacity by default because `primary-53pz` still tracks its disposition.

## Commands Run For Tracker Mutation

- `bd create "Lojix deploy doctrine: regenerate Host/UserEnvironment operating-system guidance" ...`
- `bd create "CriomOS-test-cluster: update lojix deploy smoke to current contract" ...`
- `bd create "Lojix inspect-store: report sema table decode health read-only" ...`
- `bd create "Lojix legacy store fixture: prove migration-required diagnosis" ...`
- `bd create "Lojix VM quality gate: prove current deploy path before live remediation" ...`
- `bd dep primary-3nen --blocks primary-agkc`
- `bd dep primary-04rx --blocks primary-agkc`
- `bd dep primary-04rx --blocks primary-anr3`
- `bd dep primary-agkc --blocks primary-3xwk`
- `bd dep primary-anr3 --blocks primary-3xwk`
- `bd note primary-3xwk "..."`

No code, docs, live deploy state, or Lojix store files were changed.
