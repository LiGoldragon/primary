# Audit — canonical skills recovery/fix

## Review

Pass/fail: PASS. I found no blockers.

- Correct: Canonical source repo is `/home/li/primary/repos/skills`, with `origin git@github.com:LiGoldragon/skills.git`; `jj bookmark list --all` shows `main`, `main@git`, and `main@origin` all at `61f5b4eeda8f474f682a3a05743d1a7453fb65a7`.
- Correct: Primary `flake.lock` pins `skills` to `owner: LiGoldragon`, `repo: skills`, `rev: 61f5b4eeda8f474f682a3a05743d1a7453fb65a7` at `/home/li/primary/flake.lock:200-211`.
- Correct: Skill-editor source doctrine names `LiGoldragon/skills` as canonical and generated workspace targets as targets, not source: `/home/li/primary/repos/skills/modules/skill-editor/full.md:5-10`, `/home/li/primary/repos/skills/roles/skill-editor/full.md:5-10`, `/home/li/primary/repos/skills/modules/skill-source-core/full.md:5-10`. Generated skill-editor output reflects this at `/home/li/primary/.agents/skills/skill-editor/SKILL.md:10-15`.
- Correct: Orchestration source and generated output contain the requested guardrails and route durable-intent candidates instead of direct capture: source `/home/li/primary/repos/skills/modules/orchestration/full.md:13-35`, generated `/home/li/primary/.agents/skills/orchestration/SKILL.md:56-78`. Grep found no `Capture durable intent` wording under `.agents`, `.claude`, `.pi/agents`, or `.codex/agents`.
- Correct: `human-interaction` is absent from active source manifests and generated outputs. The only source matches are guard/tests/archive reference text, not active manifest entries or source module files; `find /home/li/primary/repos/skills '**/*human-interaction*'` found no files. Grep found no generated-output matches under `.agents`, `.claude`, `.pi/agents`, or `.codex/agents`.
- Correct: `context-handover` remains separately emitted/manual-load only: it is an active skill at `/home/li/primary/repos/skills/manifests/active-outputs.nota:54`, while orchestration depends only on `spirit-query` at `/home/li/primary/repos/skills/manifests/module-dependencies.nota:61`; context-handover's own module is separate at `/home/li/primary/repos/skills/manifests/module-dependencies.nota:65`.
- Correct: Stale active names are gone and replacements exist: `/home/li/primary/repos/skills/manifests/active-outputs.nota:8`, `:21`, `:44`, `:47` include `component-architecture`, `design-quality`, `version-control`, and `work-tracking`; grep found no active `component-triad`, `beauty`, `Skill (jj`, `Skill (beads`, or `human-interaction` entries. Generated stale target directories for those four old skill names are absent under `.agents/skills` and `.claude/skills`.
- Correct: Deleted NoEmission source files `modules/keep-working/full.md` and `skills/subagent-session-workflow.md` are absent, and stale generated targets are absent. Remaining NoEmission archived files are confined to `/home/li/primary/repos/skills/skills/archive/*.md`, are listed as `Archived ... NoEmission` in `/home/li/primary/repos/skills/manifests/skills-roster.nota:8-16`, and carry the deprecated archive marker at line 3 in each sampled file.
- Correct: Nix-accessed checks cover source/generation/path constraints: generator wrappers set `SKILLS_SOURCE_ROOT` and `SKILLS_WORKSPACE_ROOT` from the source flake at `/home/li/primary/repos/skills/flake.nix:118-132`; checks cover no hard-coded roots, non-writing check requests, active-manifest generation, human-interaction deletion/pruning, source-of-truth guardrails, orchestration guardrails, and active appellations at `/home/li/primary/repos/skills/flake.nix:171-321`. `nix flake check` in the source repo passed.
- Correct: Primary generated outputs are reproducible from the locked canonical input: `cd /home/li/primary && nix run .#check-skills` passed and listed generated skill/role outputs, and `cd /home/li/primary && nix flake check` passed.
- Correct: Commit/push state is clean before this audit artifact: `jj status --no-pager` reported no changes in both `/home/li/primary/repos/skills` and `/home/li/primary`; local/git/origin bookmarks match for `main` in both repos.
- Fixed: None; audit only.
- Blocker: None.
- Note: `/home/li/primary/plan.md` was missing, so I could not inspect it. I did inspect `/home/li/primary/progress.md` and the implementer report.
- Note: No-direct-generated-editing is supported by the preservation artifact, implementer report, commit history, and reproducibility checks. I cannot prove process history beyond those artifacts; I found no conflicting evidence.
- Note: Primary generated commit `a6643323adec139f1ab726ba661a13759aff8aab` also contains unrelated pre-existing agent-output files per the implementer report and `jj show --stat`; this does not affect generated target correctness.

## Evidence checked

- `/home/li/primary/progress.md`; `/home/li/primary/plan.md` missing.
- `/home/li/primary/agent-outputs/primary-ascl/canonical-skills-recovery-fix.md`.
- `/home/li/primary/agent-outputs/primary-ascl/generated-diff-recovery-artifact.md`.
- Canonical source files: `/home/li/primary/repos/skills/modules/skill-editor/full.md`, `/home/li/primary/repos/skills/roles/skill-editor/full.md`, `/home/li/primary/repos/skills/modules/skill-source-core/full.md`, `/home/li/primary/repos/skills/modules/orchestration/full.md`.
- Manifests/tests/Nix: `/home/li/primary/repos/skills/manifests/active-outputs.nota`, `/home/li/primary/repos/skills/manifests/module-dependencies.nota`, `/home/li/primary/repos/skills/manifests/skills-roster.nota`, `/home/li/primary/repos/skills/tests/generation.rs`, `/home/li/primary/repos/skills/flake.nix`, `/home/li/primary/repos/skills/skills-check.nota`, `/home/li/primary/repos/skills/skills-generate.nota`.
- Generated outputs sampled: `/home/li/primary/.agents/skills/skill-editor/SKILL.md`, `/home/li/primary/.claude/agents/skill-editor.md`, `/home/li/primary/.agents/skills/orchestration/SKILL.md`, plus grep coverage across `.agents`, `.claude`, `.pi/agents`, and `.codex/agents`.
- Lock/status/history: `/home/li/primary/flake.lock`, `jj status`, `jj bookmark list --all`, and `jj show --stat` in both primary and canonical skills.

## Remaining blockers

None.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings include exact paths and line references for canonical source, manifests, generated outputs, Nix guardrails, lock pin, and residual notes."
    }
  ],
  "changedFiles": [
    "/home/li/.pi/agent/sessions/--home-li-primary--/subagent-artifacts/progress/8acc4a8e/progress.md",
    "/home/li/primary/agent-outputs/primary-ascl/audit-canonical-skills-recovery-fix.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd /home/li/primary/repos/skills && jj status --no-pager && jj git remote list",
      "result": "passed",
      "summary": "Canonical skills repo clean; origin is git@github.com:LiGoldragon/skills.git."
    },
    {
      "command": "cd /home/li/primary && jj status --no-pager",
      "result": "passed",
      "summary": "Primary working copy was clean before writing this audit report/progress artifact."
    },
    {
      "command": "cd /home/li/primary/repos/skills && jj bookmark list --all && cd /home/li/primary && jj bookmark list --all",
      "result": "passed",
      "summary": "main, main@git, and main@origin match for both canonical skills and primary."
    },
    {
      "command": "cd /home/li/primary/repos/skills && nix flake check",
      "result": "passed",
      "summary": "Source repo checks passed, including generation/source/path guardrails."
    },
    {
      "command": "cd /home/li/primary && nix run .#check-skills",
      "result": "passed",
      "summary": "Generated primary outputs match the locked canonical skills input."
    },
    {
      "command": "cd /home/li/primary && nix flake check",
      "result": "passed",
      "summary": "Primary generated-skills-current check passed."
    }
  ],
  "validationOutput": [
    "PASS: no blockers found.",
    "Source nix flake check: all checks passed.",
    "Primary nix run .#check-skills: passed and listed generated outputs.",
    "Primary nix flake check: all checks passed."
  ],
  "residualRisks": [
    "/home/li/primary/plan.md was missing, so plan contents could not be audited.",
    "No-direct-generated-editing is supported by artifacts and reproducibility checks, but process history cannot be proven beyond those records.",
    "Primary generated commit includes unrelated pre-existing agent-output files, reported by implementer; generated target correctness still validates."
  ],
  "noStagedFiles": true,
  "diffSummary": "Audit-only changes: wrote progress and this audit report; no implementation fixes.",
  "reviewFindings": [
    "no blockers",
    "note: /home/li/primary/plan.md missing",
    "note: no-direct-generated-editing supported by evidence but not independently provable beyond artifacts",
    "note: primary generated commit includes unrelated pre-existing agent-output files"
  ],
  "manualNotes": "Requested audit output written to /home/li/primary/agent-outputs/primary-ascl/audit-canonical-skills-recovery-fix.md."
}
```
