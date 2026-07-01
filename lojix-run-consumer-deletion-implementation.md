# lojix-run consumer deletion implementation

Task scope: implement the approved non-legacy consumer/deletion side for `lojix-run` without committing or pushing. Private repositories were not inspected. Core schema/runtime repos were not changed.

## Intent and context consulted

- Read `/home/li/primary/AGENTS.md` and repo guidance for CriomOS-home, CriomOS, skills, and lore.
- Read the redesign plan, deletion migration map, prior investigation, and audit reports named in the task.
- Queried public Spirit with `PublicTextSearch` and `Lookup 10pz`; relevant conclusion: public record `10pz` supports replacing legacy compatibility surfaces rather than preserving wrappers/translators.
- Observed orchestration roles and claimed exact edit paths before editing.

## Changed files

CriomOS-home:

- Deleted `packages/lojix-run/default.nix`.
- Deleted `packages/lojix-run/lojix-run.py`.
- Deleted `checks/lojix-run/default.nix`.
- Updated `flake.nix` to remove the `checks.lojix-run` attr.
- Updated `modules/home/profiles/min/default.nix` to remove the `lojix-run` package from `deploymentPackages` while keeping the direct `lojix` package.
- Updated `skills.md` to use `CompleteHost`, `UserEnvironment`, direct `meta-lojix` deploy admission, direct `lojix` typed observation, explicit operator Niri reload, and redaction helpers.
- Updated `RISK.md` to remove the wrapper activation path and name direct `meta-lojix` admission plus `lojix` observation.

skills and generated local skill surfaces:

- Updated `skills/modules/operating-system-operations/full.md` to remove wrapper/legacy deploy names and use `CompleteHost`, `BaseHost`, `UserEnvironment`, `DeployAccepted`, and `DeployHandle` with direct `meta-lojix`/`lojix` flow.
- Updated `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md` to match the source skill body.
- Updated `/home/li/primary/.claude/skills/operating-system-operations/SKILL.md` to match the source skill body.

CriomOS current docs/comments:

- Updated `README.md` to describe Lojix, `meta-lojix`, `lojix`, and the approved non-legacy artifact vocabulary.
- Updated `docs/GUIDELINES.md` to remove current `lojix-cli` examples and old deploy guidance.
- Updated `ARCHITECTURE.md` to describe Lojix as the deploy orchestrator instead of the retired CLI.
- Updated `modules/nixos/metal/default.nix` comment from the old home-off naming to `BaseHost`.

No tests were added or updated.

## Validation summary

- CriomOS-home package/check deletion was verified by filesystem test: `packages/lojix-run` and `checks/lojix-run` are absent.
- CriomOS-home flake attr checks verified `checks.x86_64-linux.lojix-run` is absent and `packages.x86_64-linux.lojix-run` is absent.
- `nix flake check --no-build` in CriomOS-home passed. This evaluated the flake and checks without building them.
- Live scoped grep found no remaining matches for `lojix-run`, `FullOs`, `FullOS`, `OsOnly`, `HomeOnly`, `lojix-cli`, `(Deployed`, or `AcceptedDeploy` in the touched live CriomOS-home, CriomOS, skills source, or generated local operating-system-operations surfaces.
- Generated skill parity check confirmed both local generated operating-system-operations skill files match the updated source skill body after frontmatter.
- `nix run .#check-skills -- /home/li/primary` from the skills repo failed on an unrelated stale generated agent output, not on operating-system-operations. I did not run generation because it would widen the change into unrelated already-dirty generated surfaces.

## Remaining occurrences and scope boundaries

- CriomOS-home live scoped grep: no remaining matches.
- CriomOS live current docs/comments scoped grep: no remaining matches.
- skills source and generated operating-system-operations scoped grep: no remaining matches.
- CriomOS archival reports still contain old deploy names in historical report files. They were left unchanged as archival material.
- Primary task plans/reports and historical agent-output reports still contain old names. They were left unchanged as task context or archival output.
- Core repos still contain old deploy vocabulary in live schema/runtime/docs surfaces owned by the separate core-schema/runtime worker. I read no private repos and made no core repo edits.

## Worktree state

- No commit or push was performed, per task instruction.
- No staged files: true. This workspace uses jj; no staging operation exists or was performed.
- Current relevant dirty state is the requested implementation plus one unrelated pre-existing primary `agent-outputs/ListenerDurabilityStrategy/GeneralCodeImplementer-Evidence.md` addition observed in `/home/li/primary`.

## Residual risks and follow-up

- The docs now use the approved target vocabulary, while core Lojix schema/runtime compatibility removal is owned by another worker and may not be landed in every repo yet.
- Global skills `check-skills` remains blocked by unrelated stale generated agent output outside this task's claim scope.
- Historical reports still mention old names by design; only live/current surfaces were updated.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Deleted the CriomOS-home lojix-run package/check, removed its flake and home-profile references, updated only requested consumer docs/skill surfaces, and avoided core schema/runtime changes."
    },
    {
      "id": "criterion-2",
      "status": "satisfied",
      "evidence": "Report includes changed files, validation commands, grep results, Nix evaluation evidence, residual risks, and worktree state for independent review."
    }
  ],
  "changedFiles": [
    "/git/github.com/LiGoldragon/CriomOS-home/RISK.md",
    "/git/github.com/LiGoldragon/CriomOS-home/checks/lojix-run/default.nix",
    "/git/github.com/LiGoldragon/CriomOS-home/flake.nix",
    "/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix",
    "/git/github.com/LiGoldragon/CriomOS-home/packages/lojix-run/default.nix",
    "/git/github.com/LiGoldragon/CriomOS-home/packages/lojix-run/lojix-run.py",
    "/git/github.com/LiGoldragon/CriomOS-home/skills.md",
    "/git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md",
    "/home/li/primary/.agents/skills/operating-system-operations/SKILL.md",
    "/home/li/primary/.claude/skills/operating-system-operations/SKILL.md",
    "/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/CriomOS/README.md",
    "/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md",
    "/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "spirit '(PublicTextSearch [legacy compatibility wrappers lojix])' && spirit '(Lookup 10pz)'",
      "result": "passed",
      "summary": "Found public replacement-over-compatibility intent record 10pz."
    },
    {
      "command": "bd list --status open in CriomOS-home and CriomOS",
      "result": "failed",
      "summary": "Both repos reported no beads database found; this was a repository tracking limitation, not an implementation failure."
    },
    {
      "command": "orchestrate '(Observe Roles)' and exact path Claim calls",
      "result": "passed",
      "summary": "Observed active claims and claimed all edited implementation/report paths before editing."
    },
    {
      "command": "rm -rf /git/github.com/LiGoldragon/CriomOS-home/packages/lojix-run /git/github.com/LiGoldragon/CriomOS-home/checks/lojix-run",
      "result": "passed",
      "summary": "Removed the wrapper package and check directories."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix eval .#checks.x86_64-linux --apply 'checks: builtins.hasAttr \"lojix-run\" checks'",
      "result": "passed",
      "summary": "Returned false; the lojix-run check attr is absent."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix eval .#packages.x86_64-linux --apply 'packages: builtins.hasAttr \"lojix-run\" packages'",
      "result": "passed",
      "summary": "Returned false; the lojix-run package attr is absent."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/CriomOS-home && nix flake check --no-build",
      "result": "passed",
      "summary": "Flake outputs and check derivations evaluated successfully without building."
    },
    {
      "command": "targeted rg for lojix-run, FullOs, FullOS, OsOnly, HomeOnly, lojix-cli, Deployed, AcceptedDeploy in touched live surfaces",
      "result": "passed",
      "summary": "No remaining matches in scoped live CriomOS-home, CriomOS, skills source, or generated operating-system-operations files."
    },
    {
      "command": "python3 generated-skill body parity check",
      "result": "passed",
      "summary": "Both .agents and .claude operating-system-operations generated skill bodies match the updated skills source body."
    },
    {
      "command": "cd /git/github.com/LiGoldragon/skills && nix run .#check-skills -- /home/li/primary",
      "result": "failed",
      "summary": "Failed on an unrelated stale generated agent output outside the operating-system-operations skill."
    },
    {
      "command": "jj status --no-pager and jj diff --stat in CriomOS-home, skills, CriomOS, and primary",
      "result": "passed",
      "summary": "Confirmed expected dirty files and no commit/push."
    }
  ],
  "validationOutput": [
    "CriomOS-home checks.x86_64-linux hasAttr lojix-run: false.",
    "CriomOS-home packages.x86_64-linux hasAttr lojix-run: false.",
    "CriomOS-home nix flake check --no-build: all checks passed.",
    "Live scoped grep for legacy wrapper/deploy terms: no matches in touched live surfaces.",
    "Archival occurrences remain only in historical reports/task context; core schema/runtime occurrences remain out of scope for the separate core worker.",
    "Generated operating-system-operations .agents and .claude skill bodies match source."
  ],
  "residualRisks": [
    "Core Lojix schema/runtime rename/removal is out of scope and still needs the separate worker to land fully before every approved example is executable everywhere.",
    "skills check-skills has an unrelated stale generated agent-output blocker outside this task's claim scope.",
    "Historical reports still contain old names and were intentionally left unchanged."
  ],
  "noStagedFiles": true,
  "diffSummary": "Deleted lojix-run package/check implementation from CriomOS-home, removed package/check references, and updated current CriomOS-home, CriomOS, and operating-system-operations docs to direct typed Lojix vocabulary and observation guidance.",
  "reviewFindings": [
    "no blockers in the scoped implementation",
    "non-blocker: global skills check-skills fails on unrelated stale generated agent output"
  ],
  "manualNotes": "No commit or push was performed. Private repositories were not inspected. Claims should be released after this handoff."
}
```
