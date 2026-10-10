# Audit primary-ascl bundle

## Review
- Result: fail. The bundle is close, but one current generated handoff surface still names the retired `Repo Operator` role as an assignment target.
- Correct: approved active skill/role identifiers are present in source: `component-architecture`, `design-quality`, `version-control`, `work-tracking`, `intent-curator`, `repository-closeout`, and `tracker-weaver` appear in `repos/skills-primary-ascl-doctrine/manifests/active-outputs.nota:8,21,44,47,73-75`; matching module/role source entries appear in `manifests/module-dependencies.nota:19,33,54,57,84-86`.
- Correct: generated runtime directories use the new active names: `.agents/skills/component-architecture/SKILL.md:2,6`, `.agents/skills/design-quality/SKILL.md:3,6`, `.agents/skills/version-control/SKILL.md:6,8`, `.agents/skills/work-tracking/SKILL.md:6,8`, and generated role names under `.claude/agents`, `.codex/agents`, and `.pi/agents` use `intent-curator`, `repository-closeout`, and `tracker-weaver`.
- Correct: orchestration doctrine covers the required constraints: direct-work refusal and gates in `modules/orchestration/full.md:7-9,38-42`, read-only Spirit query exception and no Spirit writes in `:23-25`, batching/scope expansion in `:42`, weaver planning in `:46`, broad risk-class right-sizing in `:48`, distinct auditor in `:54`, and no firsthand-inspection synthesis in `:58`.
- Correct: psyche-attention doctrine exists in source and generated surfaces: `modules/human-interaction/full.md:27-30` and `.claude/skills/orchestration/SKILL.md:111-146` instruct concise psyche-facing output and explain hashes/Spirit/bead IDs only when relevant.
- Correct: read-only Spirit query module exists and is composed into judgment roles: `modules/spirit-query/full.md:5-7,33-37`; `manifests/active-outputs.nota:65-73,75` embeds `spirit-query` for judgment/tracker roles, while `intent-curator` retains `spirit-cli` at `:73` and `repository-closeout` remains the mechanical exemption at `:74`.
- Correct: editing-capable role packets include edit coordination and worker-owned commit/provenance: `manifests/active-outputs.nota:65-75` includes `edit-coordination-core`; generated `general-code-implementer.md:117-123` embeds Orchestrate claiming; `general-code-implementer.md:234-237` and `modules/repository-closeout/full.md:7` require worker-owned green commits and acting-model/thinking provenance when available.
- Correct: archived prior-workflow roles are marked deprecated in source, e.g. `skills/archive/operator.md:3`, `skills/archive/designer.md:3`, `skills/archive/assistant.md:3`, `skills/archive/counselor.md:3`, and related archive files.
- Correct: Claude/Codex/pi launch default orchestration is implemented with pre-first-turn injection and launch-time escape hatches: `repos/CriomOS-home/modules/home/profiles/min/default.nix:36-44` defines the default parent-orchestrator instruction; wrapper injection and bypass logic is at `:286-379`; direct commands are at `:287-289`; Codex non-orchestrator profile is at `:753-754`. The focused Nix check is wired in `repos/CriomOS-home/flake.nix:351` and checks key strings in `checks/ai-agent-launch-orchestration/default.nix:10-29`.
- Correct: README discovery found existing comparison output and correctly avoids broad influence labels. Evidence is in `agent-outputs/primary-ascl/readme-scale-repos-discovery.md`; the underlying draft in `agent-outputs/SkillBenchmark/PublicRepoComparison.md:93-109` supports references/similar systems and flags direct influence wording as needing care.
- Blocker: `repos/skills-primary-ascl-doctrine/roles/general-code-implementer/full.md:26-27` says final commit/push mechanics may be assigned to `Repo Operator`; generated public role packets repeat it in `.claude/agents/general-code-implementer.md:30-32`, `.pi/agents/general-code-implementer.md:30-32`, and `.codex/agents/general-code-implementer.toml:3`. This violates the requirement that old main-agent appellations no longer appear as current handoff roles/subagent destinations. The replacement should be `repository-closeout` wording, with regeneration from source.
- Note: tests cover many new constraints, but they missed the blocker because they check retired role identifiers (`intent-maintainer`, `repo-operator`, `weave-operator`) rather than title-case prose destinations such as `Repo Operator`; see `tests/generation.rs:444-447` and `flake.nix:241-255`.
- Note: `nix flake check path:/home/li/primary/repos/skills-primary-ascl-doctrine` passed, and `nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link` passed. `nix run path:/home/li/primary/repos/skills#check-skills -- /home/li/primary` passed against the current local skills source and generated surfaces. The same check against the clean `skills-primary-ascl-doctrine` worktree failed because current primary generated surfaces include later local source changes; this is residual workspace drift, not the main blocker.
- Note: no private content leakage was observed in the reports or generated public surfaces inspected. The primary-ascl reports mention private scopes only to say they were excluded or discarded.

## Evidence checked
- Worker reports: `launch-default-orchestration.md`, `doctrine-spirit-role-composition.md`, `naming-discovery.md`, `readme-scale-repos-discovery.md`, and `tracker-advance-after-initial-workers.md`.
- Source repos: `repos/skills-primary-ascl-doctrine`, `repos/skills`, `repos/CriomOS-home`, and primary generated surfaces under `.agents`, `.claude`, `.codex`, and `.pi`.
- Tracker: `bd show primary-ascl primary-ascl.2 primary-ascl.6 primary-ascl.7 primary-ascl.8 --long` and final `bd show primary-ascl primary-ascl.7 --long`.

## Tracker closeout status
- Not closed. `primary-ascl.7` and parent `primary-ascl` remain open because of the blocker above.
- I did not mutate tracker state because the audit failed and this role is constrained not to implement fixes.

## Required follow-up beads
- Fix the stale `Repo Operator` handoff prose in `roles/general-code-implementer/full.md`, regenerate primary role surfaces, rerun `check-skills`, and commit/push source plus generated outputs.
- Add a guard that rejects retired title-case/current-destination prose such as `Repo Operator`, `Weave Operator`, and `Intent Maintainer` in active source/generated role packets, not only retired output identifiers.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Severity-labeled findings cite source and generated paths, including blocker at repos/skills-primary-ascl-doctrine/roles/general-code-implementer/full.md:26-27 and generated mirrors under .claude/.pi/.codex general-code-implementer."
    }
  ],
  "changedFiles": [
    "/home/li/primary/agent-outputs/primary-ascl/audit-primary-ascl-bundle.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "bd show primary-ascl primary-ascl.2 primary-ascl.6 primary-ascl.7 primary-ascl.8 --long",
      "result": "passed",
      "summary": "Confirmed all dependencies closed and audit/parent still open before audit closeout."
    },
    {
      "command": "jj log/status inspections in repos/skills, repos/skills-primary-ascl-doctrine, primary, and repos/CriomOS-home",
      "result": "passed",
      "summary": "Verified reported commits exist; noted local dirty source/generated drift in primary and repos/skills."
    },
    {
      "command": "nix flake check path:/home/li/primary/repos/skills-primary-ascl-doctrine",
      "result": "passed",
      "summary": "Skills source checks passed, including active-appellations and Spirit/orchestration guardrails."
    },
    {
      "command": "nix run path:/home/li/primary/repos/skills#check-skills -- /home/li/primary",
      "result": "passed",
      "summary": "Current local skills source reconciles with current primary generated surfaces."
    },
    {
      "command": "nix run path:/home/li/primary/repos/skills-primary-ascl-doctrine#check-skills -- /home/li/primary",
      "result": "failed",
      "summary": "Failed on stale generated rust-crate-layout against the clean c2306 worktree due later local source/generated drift."
    },
    {
      "command": "cd /home/li/primary/repos/CriomOS-home && nix build .#checks.x86_64-linux.ai-agent-launch-orchestration --no-link",
      "result": "passed",
      "summary": "Launch orchestration wrapper check built."
    },
    {
      "command": "rg/grep searches for retired active identifiers and title-case retired role destinations in source/generated surfaces",
      "result": "failed",
      "summary": "Found current handoff prose naming retired Repo Operator in source and generated general-code-implementer packets."
    },
    {
      "command": "bd show primary-ascl primary-ascl.7 --long",
      "result": "passed",
      "summary": "Verified tracker remains open after failed audit; no tracker mutation performed."
    }
  ],
  "validationOutput": [
    "PASS for launch default orchestration and Nix launch check.",
    "PASS for approved active skill/role identifiers and generated directories.",
    "PASS for orchestration, psyche-attention, Spirit-query, edit-coordination, and commit-provenance doctrine presence.",
    "FAIL for appellation-deprecation: retired Repo Operator remains a current generated handoff destination."
  ],
  "residualRisks": [
    "Current primary generated surfaces reconcile with local dirty repos/skills, not with the clean c2306 skills-primary-ascl-doctrine worktree; keep source/generated closeout coordinated after the blocker fix.",
    "Existing checks do not reject retired title-case role prose in active/generated role packets."
  ],
  "noStagedFiles": true,
  "diffSummary": "Audit report only; no source or tracker mutation.",
  "reviewFindings": [
    "blocker: repos/skills-primary-ascl-doctrine/roles/general-code-implementer/full.md:26-27 and generated .claude/.pi/.codex general-code-implementer packets still assign final mechanics to retired Repo Operator.",
    "note: flake/tests cover active identifiers but miss title-case retired role destination prose.",
    "note: no private leakage observed in inspected public reports/generated surfaces."
  ],
  "manualNotes": "Do not close primary-ascl.7 or parent primary-ascl until the Repo Operator prose is replaced from source, generated surfaces are reconciled, and a guard prevents recurrence."
}
```
