# Lojix holistic blocker fixes

Task scope: fix holistic audit blockers outside the Lojix core repos; do not inspect private-repos; do not commit or push. I read the required audit, consumer deletion report, and redesign plan before editing.

## Coordination

- Observed Orchestrate roles before editing.
- Claimed exact paths for all direct edits and the required output/progress files.
- `/git/github.com/LiGoldragon/CriomOS-test-cluster` was already claimed by `cloud-operator`, so I did not edit that checkout. I created an isolated JJ workspace at `/home/li/worktrees/lojix-holistic-test-cluster`, claimed it, and recorded primary bead `primary-53pz` for final disposition/merge. The target repo had no beads database.
- No commit or push was performed.
- Private repositories were not inspected.

## Changed files

Directly edited live files:

- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS/README.md`
- `/git/github.com/LiGoldragon/CriomOS/devshell.nix`
- `/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md`
- `/git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md`
- `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md`
- `/home/li/primary/.claude/skills/operating-system-operations/SKILL.md`
- `/git/github.com/LiGoldragon/forge/README.md`
- `/git/github.com/LiGoldragon/forge/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/horizon-rs/skills.md`
- `/git/github.com/LiGoldragon/signal-forge/README.md`
- `/git/github.com/LiGoldragon/signal-forge/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-forge/src/lib.rs`
- `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-criome/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/chronos/AGENTS.md`
- `/git/github.com/LiGoldragon/chronos/skills.md`
- `/git/github.com/LiGoldragon/chroma/AGENTS.md`
- `/git/github.com/LiGoldragon/chroma/skills.md`
- `/git/github.com/LiGoldragon/CriomOS-pkgs/AGENTS.md`
- `/home/li/.pi/agent/sessions/--home-li-primary--/subagent-artifacts/progress/95d03bb3/progress.md`
- `/home/li/primary/lojix-holistic-blocker-fixes.md`

Edited in isolated worktree because the primary test-cluster checkout is claimed:

- `/home/li/worktrees/lojix-holistic-test-cluster/lib/mkDeployTest.nix`
- `/home/li/worktrees/lojix-holistic-test-cluster/INTENT.md`

Pre-existing dirty files not authored by this pass and left intact:

- `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`
- existing primary workspace added reports/agent outputs listed by `jj status` before this task.

## Implementation summary

- Updated live operator examples in CriomOS docs and operating-system skill surfaces so `SourceRevisionPolicy` is present in the schema-required field position before `builder`. Generic examples use `RequireImmutable`; the skill text also explains `ResolveAndRecord`.
- Rewrote current live `lojix-cli` guidance in the cited files and additional live public references found by broad grep (`forge` architecture, `signal-forge` README/architecture, `horizon-rs` skills/architecture, `chronos`, `chroma`, and `CriomOS-pkgs`).
- Updated `signal-criome` authorization scope from `deploy:zeus:FullOs` to `deploy:zeus:CompleteHost`.
- In the isolated CriomOS-test-cluster worktree, updated the deploy smoke from legacy `System`/`FullOs`/`Boot`/`Deployed`/`AcceptedDeploy` vocabulary to `Host`/`CompleteHost`/`SetBootProfile`/`RequireImmutable`/`DeployAccepted`, with durable query assertions expecting `CompleteHost BootProfile Current`.

## Validation

Commands run and results:

- `cargo test -q` in `/git/github.com/LiGoldragon/signal-criome`: passed; crate reported zero local tests for the default feature set.
- `nix flake check --no-build` in `/git/github.com/LiGoldragon/signal-criome`: passed; all flake outputs/check derivations evaluated.
- `cargo test -q` in `/git/github.com/LiGoldragon/signal-forge`: passed; crate reported zero local tests for the default feature set.
- `nix flake check --no-build` in `/git/github.com/LiGoldragon/signal-forge`: passed.
- `nix flake check --no-build` in `/git/github.com/LiGoldragon/forge`: passed.
- `nix flake check --no-build` in `/git/github.com/LiGoldragon/horizon-rs`: passed with existing crane/nixfmt evaluation warnings.
- `python3` parity check comparing `skills/modules/operating-system-operations/full.md` to generated `.agents` and `.claude` operating-system skill bodies: passed.
- `nix run .#check-skills -- /home/li/primary` in `/git/github.com/LiGoldragon/skills`: failed on unrelated stale generated output `/home/li/primary/.agents/skills/code-implementation/SKILL.md`; operating-system skill parity passed.
- `nix flake check --no-build` in `/git/github.com/LiGoldragon/CriomOS`: failed because the repo's default `system` flake input is intentionally a stub unless overridden by Lojix.
- `nix flake check --no-build` in `/home/li/worktrees/lojix-holistic-test-cluster`: failed before evaluating the edited test because a pinned Rust channel fixed-output derivation hash mismatched; this appears unrelated to the deploy vocabulary edits.
- Broad grep across public live repos for `lojix-run|FullOs|OsOnly|HomeOnly|Deployed|AcceptedDeploy|DeploymentKind|HomeMode|SystemAction|lojix-cli`, excluding `.jj`, `.git`, `target`, `node_modules`, result symlinks, lock files, `reports/**`, and `skills/archive/**`: remaining matches are the original claimed `/git/github.com/LiGoldragon/CriomOS-test-cluster` checkout and one unrelated `mentci-lib` prose heading `Deployed console`.
- Same broad grep over the edited set plus `/home/li/worktrees/lojix-holistic-test-cluster` and generated operating-system skills: no matches.
- `rg 'Deploy \((Host|UserEnvironment)'` over CriomOS docs, operating-system skill surfaces, and the isolated test-cluster worktree: every current deploy example includes `RequireImmutable` in the required field position.

## Residual risks

- Blocker for final re-audit until merged: the primary `/git/github.com/LiGoldragon/CriomOS-test-cluster` checkout still contains the legacy live blocker because it is claimed by `cloud-operator`. The fix is present in `/home/li/worktrees/lojix-holistic-test-cluster`; bead `primary-53pz` tracks full merge after that claim clears.
- `CriomOS-test-cluster` Nix validation is blocked by an unrelated fixed-output Rust channel hash mismatch.
- `skills` global check remains blocked by unrelated stale generated output outside the operating-system-operations skill.
- Historical/archival reports and `skills/archive/**` still mention legacy names by design and were left unchanged.
- The broad grep term `Deployed` can match unrelated English prose; `mentci-lib/ARCHITECTURE.md` has `Deployed console`, which is not a Lojix deploy contract occurrence.

## Re-audit readiness

Ready for re-audit of the directly edited live docs/skill/contract-test surfaces and the isolated `CriomOS-test-cluster` worktree. Not ready for re-audit of the primary `CriomOS-test-cluster` checkout until the isolated worktree changes are merged into that claimed checkout.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings and severities are recorded: blocker remains only in the claimed primary CriomOS-test-cluster checkout until isolated worktree /home/li/worktrees/lojix-holistic-test-cluster is merged; unrelated residuals are classified separately."
    }
  ],
  "changedFiles": [
    "/git/github.com/LiGoldragon/CriomOS/AGENTS.md",
    "/git/github.com/LiGoldragon/CriomOS/README.md",
    "/git/github.com/LiGoldragon/CriomOS/devshell.nix",
    "/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md",
    "/git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md",
    "/home/li/primary/.agents/skills/operating-system-operations/SKILL.md",
    "/home/li/primary/.claude/skills/operating-system-operations/SKILL.md",
    "/git/github.com/LiGoldragon/forge/README.md",
    "/git/github.com/LiGoldragon/forge/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/horizon-rs/skills.md",
    "/git/github.com/LiGoldragon/signal-forge/README.md",
    "/git/github.com/LiGoldragon/signal-forge/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/signal-forge/src/lib.rs",
    "/git/github.com/LiGoldragon/criome/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/persona/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/signal-criome/tests/round_trip.rs",
    "/git/github.com/LiGoldragon/chronos/AGENTS.md",
    "/git/github.com/LiGoldragon/chronos/skills.md",
    "/git/github.com/LiGoldragon/chroma/AGENTS.md",
    "/git/github.com/LiGoldragon/chroma/skills.md",
    "/git/github.com/LiGoldragon/CriomOS-pkgs/AGENTS.md",
    "/home/li/worktrees/lojix-holistic-test-cluster/lib/mkDeployTest.nix",
    "/home/li/worktrees/lojix-holistic-test-cluster/INTENT.md",
    "/home/li/.pi/agent/sessions/--home-li-primary--/subagent-artifacts/progress/95d03bb3/progress.md",
    "/home/li/primary/lojix-holistic-blocker-fixes.md"
  ],
  "testsAddedOrUpdated": [
    "/git/github.com/LiGoldragon/signal-criome/tests/round_trip.rs"
  ],
  "commandsRun": [
    {
      "command": "orchestrate Observe Roles and exact Claim calls",
      "result": "passed",
      "summary": "Observed active cloud-operator claim on CriomOS-test-cluster; claimed all direct edit paths and isolated worktree paths."
    },
    {
      "command": "jj workspace add --name lojix-holistic-test-cluster-outside --revision main --message 'lojix-holistic-test-cluster' /home/li/worktrees/lojix-holistic-test-cluster",
      "result": "passed",
      "summary": "Created isolated CriomOS-test-cluster worktree because the primary checkout is claimed."
    },
    {
      "command": "bd create/update primary-53pz",
      "result": "passed",
      "summary": "Tracked isolated worktree and required final disposition in primary bead because the target repo has no beads database."
    },
    {
      "command": "cargo test -q (signal-criome)",
      "result": "passed",
      "summary": "Default-feature test harness completed successfully with zero local tests reported."
    },
    {
      "command": "nix flake check --no-build (signal-criome)",
      "result": "passed",
      "summary": "All exposed flake checks evaluated."
    },
    {
      "command": "cargo test -q (signal-forge)",
      "result": "passed",
      "summary": "Default-feature test harness completed successfully with zero local tests reported."
    },
    {
      "command": "nix flake check --no-build (signal-forge)",
      "result": "passed",
      "summary": "Flake outputs evaluated."
    },
    {
      "command": "nix flake check --no-build (forge)",
      "result": "passed",
      "summary": "Flake outputs evaluated."
    },
    {
      "command": "nix flake check --no-build (horizon-rs)",
      "result": "passed",
      "summary": "Flake outputs evaluated with existing warnings."
    },
    {
      "command": "python3 generated operating-system skill parity check",
      "result": "passed",
      "summary": "Generated .agents and .claude operating-system skill bodies match source."
    },
    {
      "command": "nix run .#check-skills -- /home/li/primary (skills)",
      "result": "failed",
      "summary": "Failed on unrelated stale generated code-implementation skill output, not on operating-system-operations."
    },
    {
      "command": "nix flake check --no-build (CriomOS)",
      "result": "failed",
      "summary": "Failed because the default system input is an intentional stub unless Lojix provides an override."
    },
    {
      "command": "nix flake check --no-build (/home/li/worktrees/lojix-holistic-test-cluster)",
      "result": "failed",
      "summary": "Failed on unrelated fixed-output Rust channel hash mismatch before edited deploy test evaluation."
    },
    {
      "command": "broad rg for legacy deploy/wrapper vocabulary across public live repos with locks/targets/reports/archive excluded",
      "result": "failed",
      "summary": "Remaining live Lojix matches are in the claimed primary CriomOS-test-cluster checkout; edited worktree and all other touched live files are clean."
    },
    {
      "command": "broad rg over edited set plus isolated CriomOS-test-cluster worktree",
      "result": "passed",
      "summary": "No legacy deploy/wrapper vocabulary remained outside locks/archives in edited scope."
    }
  ],
  "validationOutput": [
    "Operating-system skill source and generated outputs include RequireImmutable in all deploy examples and explain ResolveAndRecord.",
    "Edited worktree mkDeployTest uses Host CompleteHost SetBootProfile RequireImmutable and asserts DeployAccepted plus CompleteHost BootProfile Current.",
    "signal-criome authorization scope now uses deploy:zeus:CompleteHost.",
    "Broad edited-scope grep found no lojix-run, FullOs, OsOnly, HomeOnly, Deployed, AcceptedDeploy, DeploymentKind, HomeMode, SystemAction, or lojix-cli matches outside excluded locks/archives."
  ],
  "residualRisks": [
    "blocker: /git/github.com/LiGoldragon/CriomOS-test-cluster remains legacy in the primary checkout because cloud-operator owns the repo claim; fixed copy is in /home/li/worktrees/lojix-holistic-test-cluster and tracked by primary-53pz for full merge.",
    "unrelated: CriomOS-test-cluster flake check is blocked by a fixed-output Rust channel hash mismatch.",
    "unrelated: skills check-skills is blocked by stale generated code-implementation skill output.",
    "archival: CriomOS reports and skills archive still contain legacy vocabulary and were intentionally not rewritten.",
    "false-positive: mentci-lib/ARCHITECTURE.md contains unrelated prose 'Deployed console'."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added required SourceRevisionPolicy to live deploy examples, removed live lojix-cli guidance, updated signal-criome authorization scope, and prepared nonlegacy CriomOS-test-cluster deploy smoke changes in an isolated worktree.",
  "reviewFindings": [
    "blocker: /git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix and INTENT.md in the primary checkout still contain legacy Lojix vocabulary due to an active cloud-operator repo claim; merge /home/li/worktrees/lojix-holistic-test-cluster to clear.",
    "no blocker: edited live docs/skill/generated surfaces include SourceRevisionPolicy in deploy examples.",
    "no blocker: edited public live guidance no longer references lojix-cli.",
    "no blocker: signal-criome test authorization scope uses CompleteHost."
  ],
  "manualNotes": "No commit or push was performed. Private repositories were not inspected. Direct re-audit is ready for edited live files and the isolated test-cluster worktree, but the primary test-cluster checkout needs the tracked merge after the active claim clears."
}
```
