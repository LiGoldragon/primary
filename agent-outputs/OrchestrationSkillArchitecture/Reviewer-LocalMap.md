# Orchestration Skill Architecture Local Map

## Review
- Correct: the source model already separates runtime skills, role roots, and role-only composition modules. Evidence: `/home/li/primary/repos/skills/manifests/module-dependencies.nota:3-4` defines `RuntimeSkill`, `RoleSource`, and generator-only `RoleComposition`; `/home/li/primary/repos/skills/README.md:36` says `RoleComposition` can be included in roles but cannot emit as skills.
- Correct: generated local surfaces are present and scoped: 55 `.agents` skills and 10 generated agents per harness. Active generated agent names are `general-code-implementer`, `intent-maintainer`, `intent-translator`, `nix-auditor`, `operating-system-implementer`, `repo-operator`, `repo-scaffolder`, `rust-auditor`, `scout`, `skill-editor`.
- Correct: `keep-working` is gone as a first-class/runtime skill. Evidence: `/home/li/primary/repos/skills/manifests/skills-roster.nota:74` marks it `Deleted NoEmission`; filesystem checks found no `/home/li/primary/.agents/skills/keep-working`, `/home/li/primary/.claude/skills/keep-working`, or `/home/li/primary/repos/skills/modules/keep-working`.
- Fixed: none. Review-only task; no source edits made. This report is the requested output artifact.
- Blocker: none found.
- Note: implementation recommendations and naming findings follow.

## Concrete map

### Skill vs agent naming pattern
Severity: info.

- `code-implementation` is the standalone runtime skill. Evidence: `/home/li/primary/repos/skills/manifests/active-outputs.nota:36` describes it as "Standalone ordinary code implementation discipline"; `/home/li/primary/.agents/skills/code-implementation/SKILL.md:10` gives generic local-fit implementation rules.
- `code-implementation-core` is role-only composition, not a first-class skill. Evidence: `/home/li/primary/repos/skills/manifests/module-dependencies.nota:9` marks it `RoleComposition`; `/home/li/primary/repos/skills/modules/code-implementation-core/full.md:6` says the worker owns local understanding, edits, and verification.
- The actual generated code worker is `general-code-implementer`, not `code-implementer`. Evidence: `/home/li/primary/repos/skills/manifests/active-outputs.nota:67` maps the role to `[agent-output-protocol edit-coordination-core code-implementation-core rust-core nix-core operating-system-operations]`; `/home/li/primary/repos/skills/roles/general-code-implementer/full.md:5` says it changes ordinary code and generator implementation.
- Recommendation: keep this three-layer pattern: runtime skill `code-implementation`; role composition `code-implementation-core`; agent role `general-code-implementer`. If user-facing docs say "code implementer agent", normalize them to `general-code-implementer` unless a narrower role is actually added.

### `intent-led-orchestration` rename question
Severity: medium naming/design risk.

- Current content is stricter than generic orchestration. Evidence: `/home/li/primary/.agents/skills/intent-led-orchestration/SKILL.md:10` says use only at fresh-context startup; line 12 says the orchestrator is an intent-only lane that never performs task work; line 26 forbids direct file/tool/status inspection; line 38 requires two explicit psyche approvals.
- Recommendation: do not rename it to plain `orchestration` unless the intended default orchestrator really has these strict intent-only constraints. If yes, `orchestration` is a good top-level name. If no, rename to `intent-only-orchestration` and create/compose a broader `orchestration` module for normal lead coordination.

### Human/psyche-facing orchestration-related skills
Severity: info, with medium consolidation opportunity.

They are still separate runtime skills, not agglomerated. Evidence: `/home/li/primary/repos/skills/manifests/module-dependencies.nota:61-70` lists `human-interaction`, `helper-context-transfer`, `intent-led-orchestration`, `context-maintenance`, `context-handover`, `context-maintenance-deep`, `intent-log`, `spirit-cli`, `intent-maintenance`, and `intent-clarification` as independent `RuntimeSkill` modules.

- `human-interaction`: psyche boundary, asking threshold, privacy, and folded mid-task continuation. Evidence: `/home/li/primary/.agents/skills/human-interaction/SKILL.md:10`, `:13`, `:21`, `:25`, `:29`, `:46`.
- `intent-clarification`: detailed ask-vs-proceed protocol. Evidence: `/home/li/primary/.agents/skills/intent-clarification/SKILL.md:16`, `:31`, `:39`, `:50`, `:64`.
- `helper-context-transfer`: worker/helper briefing and output skepticism. Evidence: `/home/li/primary/.agents/skills/helper-context-transfer/SKILL.md:10`, `:12`, `:23`, `:25`.
- `context-handover`: clean-session handoff, with psyche intent separated from matter context. Evidence: `/home/li/primary/.agents/skills/context-handover/SKILL.md:10`, `:17`, `:31`, `:41`.
- `session-lanes`: discipline vs lane identity and lane lifecycle/drain. Evidence: `/home/li/primary/.agents/skills/session-lanes/SKILL.md:10`, `:12`, `:14`, `:24`, `:26`, `:33`.
- `context-maintenance` and `context-maintenance-deep`: cleanup/disposition surfaces; deep is explicitly cross-lane. Evidence: `/home/li/primary/.agents/skills/context-maintenance/SKILL.md:10`, `:22`, `:24`, `:28`; `/home/li/primary/.agents/skills/context-maintenance-deep/SKILL.md:10`, `:20`, `:28`.
- Intent record modules (`intent-log`, `spirit-cli`, `intent-manifestation`, `intent-maintenance`) remain separate and should stay separate unless the default orchestrator is expected to perform Spirit capture/maintenance directly.

### `keep-working`
Severity: resolved.

- Gone/folded. Runtime/source directories are absent, roster marks it deleted, and the behavior now appears in `human-interaction`: `/home/li/primary/.agents/skills/human-interaction/SKILL.md:21-23` says mid-task psyche messages add context and the agent should keep working unless explicitly stopped.
- The orchestration-specific variant is also in `intent-led-orchestration`: `/home/li/primary/.agents/skills/intent-led-orchestration/SKILL.md:22`.

## Recommended default orchestrator composition
Severity: medium architecture recommendation.

There is no generated default orchestrator role today. Evidence: active roles in `/home/li/primary/repos/skills/manifests/active-outputs.nota:65-74` omit an orchestrator, and `/home/li/primary/repos/skills/roles/intent-translator/full.md:35` says the lead/orchestrator is special and not a spawned worker role in this packet set.

Recommended composition for a default psyche-facing orchestrator:

1. Core: `human-interaction`, `intent-clarification`, `intent-led-orchestration` or renamed `orchestration`, `helper-context-transfer`, `session-lanes`, `reporting`, `privacy`.
2. Intent capture path when the orchestrator owns durable intent: `intent-log`, `spirit-cli`, `intent-manifestation`; add `intent-maintenance` only for maintenance tasks.
3. Continuation/cleanup: `context-handover` and `context-maintenance`; include `context-maintenance-deep` only for cross-lane sweeps.
4. Exclude from an intent-only orchestrator default: `code-implementation`, `edit-coordination`, `repository-closeout`, `jj`, and `testing`, because the current orchestration skill says the orchestrator must not inspect files/tools or perform task work.

Implementation path: create an `orchestrator` role source or `orchestrator-core` role composition that aggregates these modules, instead of making every worker load all psyche-facing runtime skills.

## Runtime skills for standalone non-orchestrator agents
Severity: info.

Keep these as standalone runtime skills:

- Baseline standalone work: `edit-coordination`, `code-implementation`, `repository-closeout`, `reporting`, `privacy`, `secrets`.
- Verification/repo mechanics as triggered by task: `testing`, `jj`, `beads`, `feature-development`, `repository-management`, `repo-intent`.
- Domain/topic skills as triggered by touched area: Rust, Nix, architecture, NOTA, Mermaid, Kameo, etc.
- `human-interaction` only for non-orchestrator agents that directly talk to the psyche.
- Do not load `intent-led-orchestration` or `helper-context-transfer` by default into ordinary spawned workers; they are lead/orchestrator skills unless a worker is explicitly assigned dispatch/lead duties.

## Naming inconsistencies and top rename candidates

1. Severity: medium. `intent-led-orchestration` says "intent-led" but the body enforces "intent-only" and a no-inspection orchestrator. Candidate: `intent-only-orchestration` if kept narrow; `orchestration` only if adopted as the default broad orchestrator name.
2. Severity: medium. "Role" is overloaded between generated worker roles and legacy lane/discipline roles. Evidence: generated agents are in `/home/li/primary/.claude/agents/*`, while `/home/li/primary/orchestrate/roles.list:28-45` still lists legacy lanes like `operator`, `designer`, `assistant`, and `counselor`. Candidate: document this split or rename one surface as lane disciplines vs generated worker agents.
3. Severity: low. `helper-context-transfer` is accurate but clunky and uses "helper" terminology. Candidate: `worker-briefing` or `worker-dispatch` if this becomes part of orchestrator core.
4. Severity: low. `context-handover` is really session/fresh-context handover. Candidate: `session-handover`.
5. Severity: low. `context-maintenance-deep` uses a vague depth suffix. Candidate: `cross-lane-context-maintenance`.

## Residual risks

- I audited local source/generated surfaces only; I did not inspect private repos.
- No source changes or tests were run because the task was review-only.
- The rename recommendation depends on the intended product semantics of the default orchestrator: strict intent-only vs broader lead coordination.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings cite local source and generated files, including active manifest lines, module dependency lines, generated skill lines, role source lines, and severity-labeled naming findings."
    }
  ],
  "changedFiles": [
    "/home/li/primary/agent-outputs/OrchestrationSkillArchitecture/Reviewer-LocalMap.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "test absence loop for keep-working runtime/source directories",
      "result": "passed",
      "summary": "Confirmed keep-working absent from .agents, .claude, and source modules."
    },
    {
      "command": "find counts for generated skills and agents",
      "result": "passed",
      "summary": "Counted 55 .agents skills and 10 generated agents per Claude/Codex/Pi surface."
    },
    {
      "command": "find generated Claude agent names",
      "result": "passed",
      "summary": "Listed active generated agent names; no orchestrator agent is present."
    }
  ],
  "validationOutput": [
    "keep-working absent from generated/runtime/source directories; skills-roster marks Deleted NoEmission.",
    "active manifests show separate RuntimeSkill, RoleSource, and RoleComposition surfaces.",
    "intent-led-orchestration body is strict intent-only orchestration, not generic orchestration."
  ],
  "residualRisks": [
    "No private repositories inspected.",
    "Rename recommendation depends on whether the desired default orchestrator is strict intent-only or broader lead coordination."
  ],
  "noStagedFiles": true,
  "diffSummary": "No source edits; wrote requested review report only.",
  "reviewFindings": [
    "no blockers",
    "medium: /home/li/primary/.agents/skills/intent-led-orchestration/SKILL.md:10 - current name is narrower/ambiguous relative to strict intent-only body; rename only with semantic decision.",
    "medium: /home/li/primary/orchestrate/roles.list:28 - legacy lane roles coexist with generated worker roles, overloading role terminology.",
    "resolved: /home/li/primary/repos/skills/manifests/skills-roster.nota:74 - keep-working is Deleted NoEmission and folded into human-interaction."
  ],
  "manualNotes": "Review-only task; report written to the authoritative output path."
}
```
