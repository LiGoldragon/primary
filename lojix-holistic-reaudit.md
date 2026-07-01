# Lojix holistic no-legacy re-audit

## Review
- Correct: core Lojix repos are clean for the named legacy deploy vocabulary outside target/lock contexts. `rg` over `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, and `/git/github.com/LiGoldragon/lojix` found no matches for `lojix-run`, `FullOs`, `OsOnly`, `HomeOnly`, `Deployed`, `AcceptedDeploy`, `DeploymentKind`, `HomeMode`, `SystemAction`, `lojix-cli`, or the known wrapper/fallback/postcheck helper names outside excluded `target`/lock paths.
- Correct: the required `SourceRevisionPolicy` field order is present in the schema: `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema:103-110` has `HostDeployAction`, then `source_revision_policy SourceRevisionPolicy`, then `builder`; `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema:115-122` does the same for `UserEnvironmentDeployment`.
- Correct: fixed current docs/skill examples include the policy in that position, e.g. `/git/github.com/LiGoldragon/CriomOS/README.md:26-28`, `/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md:271`, `/git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md:24,30,36`, `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md:29,35,41`, and `/home/li/primary/.claude/skills/operating-system-operations/SKILL.md:29,35,41` all place `RequireImmutable` between the action and builder fields.
- Correct: the isolated CriomOS-test-cluster worktree is nonlegacy for the searched terms. Current `/home/li/worktrees/lojix-holistic-test-cluster/lib/mkDeployTest.nix:472-473` submits `Deploy (Host (... CompleteHost ... SetBootProfile RequireImmutable None ...))`, `/home/li/worktrees/lojix-holistic-test-cluster/lib/mkDeployTest.nix:476` asserts `DeployAccepted`, and `rg` over that isolated worktree found no matches for the named legacy terms.
- Correct: no new deploy compatibility wrapper/fallback/postcheck/local-jj path was found in current core or CriomOS-home deploy surfaces. The old `lojix-run` package/check paths are absent, and current guidance is prohibitive/explicit: `/git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md:11` says not to use deploy wrappers or compatibility translators, `/git/github.com/LiGoldragon/CriomOS-home/skills.md:214-224` says there is no profile wrapper or compatibility translator, and `/git/github.com/LiGoldragon/CriomOS-home/skills.md:225-231` makes Niri reload an explicit operator procedure rather than a deploy-tool side effect.
- Correct: required beads exist. `bd show primary-4wvl` reports `Rename CriomOS-home to CriomOS-user [P2 · OPEN]`; `bd show primary-53pz` reports `Track lojix-holistic-test-cluster worktree [P2 · OPEN]` and records merge disposition after the `cloud-operator` claim clears.
- Fixed: none applied. This was a read-only audit; only this requested report was written.
- Blocker: `/git/github.com/LiGoldragon/CriomOS-test-cluster` primary checkout still contains the legacy live deploy test and is clean relative to its current parent, so the isolated fix is not merged there. Evidence: `jj status` in the primary checkout reported no changes; `/git/github.com/LiGoldragon/CriomOS-test-cluster/INTENT.md:67` still says `FullOs` `Boot`; `/git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:38,455,472,476,501,533,546,549` still contains `FullOs`, `Deploy (System ...)`, `Deployed`, `AcceptedDeploy`, and `FullOs Boot Current`; `/git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:298` still mentions `lojix-cli SystemActivation`. The isolated worktree has the fix, but primary closeout remains blocked until the cloud-operator-owned checkout can receive or merge it; bead `primary-53pz` correctly tracks that.
- Blocker: current `.claude` agent guidance still contains legacy deploy examples and omits `SourceRevisionPolicy`; these paths are not archive, lock, target, or generated-report contexts. `/home/li/primary/.claude/agents/operating-system-implementer.md:300,306,309,311` and `/home/li/primary/.claude/agents/general-code-implementer.md:378,384,387,389` still teach `Deploy (System ... FullOs ...)`, `Deploy (Home ...)`, `FullOs`/`OsOnly`/old actions/modes, and `(Deployed ...)`.
- Note: broad public live grep, excluding `.git`, `.jj`, `target`, common lockfiles, `reports/**`, and archive paths, found remaining real matches only in the primary CriomOS-test-cluster checkout and the two `.claude/agents` files above, plus `/git/github.com/LiGoldragon/mentci-lib/ARCHITECTURE.md:77` where `Deployed console` is ordinary English prose, not a Lojix deploy contract occurrence.
- Note: `/home/li/primary/plan.md` was requested but does not exist; I read `/home/li/primary/progress.md` and the four named reports that were present.

Pass/fail: FAIL.

Remaining blockers:
- Merge or apply `/home/li/worktrees/lojix-holistic-test-cluster` into `/git/github.com/LiGoldragon/CriomOS-test-cluster` after the `cloud-operator` claim clears, or have that owner apply the same changes. This is the closeout blocker tracked by `primary-53pz`.
- Regenerate or update `/home/li/primary/.claude/agents/operating-system-implementer.md` and `/home/li/primary/.claude/agents/general-code-implementer.md` so their deploy guidance matches the nonlegacy schema and includes `SourceRevisionPolicy` in the required field position.

Closeout recommendation: do not close this as holistic no-legacy complete yet. After those two blockers are fixed, rerun the broad legacy-term grep and the deploy-example grep; if clean except classified archival/lock/target/report prose, close out with `primary-53pz` resolved.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings include blockers at /git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:472 and /home/li/primary/.claude/agents/operating-system-implementer.md:300, with residual risks and closeout recommendation."
    }
  ],
  "changedFiles": [
    "/home/li/primary/lojix-holistic-reaudit.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read /home/li/primary/progress.md and named audit/fix reports; attempted read /home/li/primary/plan.md",
      "result": "passed",
      "summary": "progress and reports were read; plan.md was absent."
    },
    {
      "command": "rg legacy deploy vocabulary across /git/github.com/LiGoldragon plus /home/li/primary/.agents and .claude with target/locks/reports/archive excluded",
      "result": "failed",
      "summary": "Remaining live matches are primary CriomOS-test-cluster, two .claude agent files, and one unrelated mentci-lib prose false positive."
    },
    {
      "command": "rg 'Deploy ((Host|UserEnvironment|System|Home)' across public live surfaces with target/locks/reports/archive excluded",
      "result": "failed",
      "summary": "Fixed docs/skills have RequireImmutable in position; .claude agent examples and primary test-cluster remain legacy/missing SourceRevisionPolicy."
    },
    {
      "command": "jj status --no-pager in /git/github.com/LiGoldragon/CriomOS-test-cluster and /home/li/worktrees/lojix-holistic-test-cluster",
      "result": "passed",
      "summary": "Primary checkout has no changes and still contains legacy text; isolated worktree has modified INTENT.md and lib/mkDeployTest.nix with nonlegacy fix."
    },
    {
      "command": "bd show primary-4wvl; bd show primary-53pz",
      "result": "passed",
      "summary": "Both beads exist and are open; primary-53pz tracks merge/disposition of the isolated test-cluster worktree after the cloud-operator claim clears."
    },
    {
      "command": "test deleted lojix-run package/check paths and targeted rg for wrapper/fallback/postcheck/local-jj helper names",
      "result": "passed",
      "summary": "CriomOS-home packages/lojix-run and checks/lojix-run are absent; no current core deploy wrapper/fallback/postcheck/local-jj helper remains."
    },
    {
      "command": "rg legacy terms in /home/li/worktrees/lojix-holistic-test-cluster excluding jj/target/locks",
      "result": "passed",
      "summary": "No matches in the isolated fixed worktree."
    }
  ],
  "validationOutput": [
    "Schema requires SourceRevisionPolicy immediately before builder for HostDeployment and UserEnvironmentDeployment.",
    "Fixed README/GUIDELINES/operating-system skill examples include RequireImmutable in that field position.",
    "Primary CriomOS-test-cluster still uses System/FullOs/Boot/Deployed/AcceptedDeploy-era vocabulary.",
    ".claude agent role guidance still uses FullOs/OsOnly/Home old examples and omits SourceRevisionPolicy.",
    "Beads primary-4wvl and primary-53pz both exist."
  ],
  "residualRisks": [
    "blocker: primary CriomOS-test-cluster remains legacy until the isolated worktree is merged after the cloud-operator claim clears.",
    "blocker: .claude agent guidance remains stale and can re-teach old Lojix deploy requests.",
    "minor: no full cargo/nix test suite was run in this read-only re-audit; validation was grep/status/report inspection."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only audit report written; no code, tests, commits, pushes, or private-repos inspection.",
  "reviewFindings": [
    "blocker: /git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:472 - primary live deploy test still submits legacy Deploy (System ... FullOs ...) and associated old result/state vocabulary.",
    "blocker: /home/li/primary/.claude/agents/operating-system-implementer.md:300 and /home/li/primary/.claude/agents/general-code-implementer.md:378 - current agent guidance still uses old FullOs/System examples without SourceRevisionPolicy.",
    "no blocker: core signal-lojix/meta-signal-lojix/lojix current files are clean for the named old vocabulary outside excluded generated/target/lock contexts.",
    "no blocker: beads primary-4wvl and primary-53pz exist."
  ],
  "manualNotes": "Private repositories were not inspected. The report write is the requested output artifact; no code edits, commits, or pushes were performed."
}
```
