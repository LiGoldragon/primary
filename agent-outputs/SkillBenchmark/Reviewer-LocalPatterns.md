# Local Skill and Role Corpus Audit

## Review

- Correct: Active generated surfaces are easy to identify. `skills/generated-role-outputs.nota:1` lists 10 generated roles across Claude/Codex/Pi (`intent-translator`, `scout`, `repo-scaffolder`, `general-code-implementer`, `criomos-implementer`, `rust-auditor`, `nix-auditor`, `skill-editor`, `intent-maintainer`, `repo-operator`). I inspected the active runtime skill copy under `.agents/skills` and the generated Claude role packets under `.claude/agents`.
- Correct: The current skill corpus is much shorter than a traditional how-to library. Local inspection found 55 generated runtime skills; 45 are at or under 60 lines, 52 are at or under 80 lines, and only `jj`, `rust-crate-layout`, and `typed-records-over-flags` exceed 80 lines. This aligns with external load-on-demand best practice.
- Correct: Several compact code blocks are load-bearing rather than decorative: `bead-weaver` shows exact `bd` commands at `.agents/skills/bead-weaver/SKILL.md:28`, `nix-usage` shows narrow Nix commands at `.agents/skills/nix-usage/SKILL.md:20`, `repository-management` shows `ghq`/`gh` command shapes at `.agents/skills/repository-management/SKILL.md:18`, and `typed-records-over-flags` shows Rust shapes at `.agents/skills/typed-records-over-flags/SKILL.md:46`.
- Correct: Generated roles are already born with composition modules. For example, `general-code-implementer` embeds `agent output protocol`, `edit coordination core`, `code implementation core`, `Rust core`, and `Nix core` in `.claude/agents/general-code-implementer.md:47`, `.claude/agents/general-code-implementer.md:117`, `.claude/agents/general-code-implementer.md:154`, `.claude/agents/general-code-implementer.md:194`, and `.claude/agents/general-code-implementer.md:245`. This supports moving more worker-only doctrine out of runtime skills.
- Fixed: No files were changed except this requested review artifact.
- Blocker: None for benchmarking. The audit can feed external synthesis as-is.
- Note: `/home/li/primary/plan.md` was absent; `/home/li/primary/progress.md` contained only a generic in-progress stub, so this review is based on the current generated corpus and the task directions.

## Comparison-ready summary

### Strengths versus external best-practice patterns

- The generated skills generally have good frontmatter triggers and concise bodies. Most skills use a direct `Rules` shape and avoid long tutorials.
- The corpus has shifted toward current operational discipline rather than provenance, status logs, or broad manuals. I did not find generated-file notices in the inspected runtime skills or roles.
- Role packets are substantially more competent than a pure runtime-skill model: worker roles carry workflow, boundaries, verification, output expectations, and composition modules.
- Compact examples remain where syntax is easy to get wrong (`jj`, `nix-usage`, `repository-management`, `spirit-cli`, `typed-records-over-flags`, `rust-crate-layout`). This matches the external pattern of using examples only when they prevent command or shape ambiguity.

### Weaknesses and concrete findings

- Medium: `.agents/skills/main-feature-integration/SKILL.md:8-10` contains a likely stale/local path claim: “This applies to code repos under `/git`, not primary.” The active workspace visible in this run uses `/home/li/primary/repos`, and the current direction says to avoid stale paths and host/config specifics. Recommendation: remove the path phrase or replace it with canonical repo-scope language.
- Medium: `.agents/skills/rust-crate-layout/SKILL.md:60-61` has a See-Also-style reference to `skills/micro-components.md` and `lore's rust/style.md`. The current generated runtime path is not that markdown path, and the direction says to avoid See Also and stale paths. Recommendation: inline the still-current dependency rule or cite skill names only if the runtime can resolve them.
- Medium: Generated role packets still carry repeated response/report boilerplate. Example: `.claude/agents/general-code-implementer.md:47-115` repeats the full `agent output protocol`, including chat-return rules at `.claude/agents/general-code-implementer.md:100-108`; `.claude/agents/skill-editor.md:31-99` repeats the same module. Recommendation: keep exact output-path obedience in the dispatch envelope and reduce the role composition module to a short evidence/output discipline.
- Low: `.agents/skills/intent-clarification/SKILL.md:52-56` references `skills/intent-log.md` and `skills/intent-maintenance.md`. That is a cross-reference/path pattern rather than self-contained runtime guidance. Recommendation: replace path references with direct operation names or compose the intent-maintenance module into the role that needs it.
- Low: `.agents/skills/spirit-cli/SKILL.md:14-17` includes a compact `Record` example, but the description promises query/Observe and maintenance shapes. Recommendation: either narrow the description to capture-only basics or add one compact Observe/maintenance example if this remains runtime.
- Low: `.agents/skills/abstractions/SKILL.md:10-19`, `.agents/skills/rust-methods/SKILL.md:8-12`, and `.agents/skills/rust-discipline/SKILL.md:10-14` all teach overlapping “behavior belongs on data-bearing types / typed errors” Rust doctrine. Recommendation: keep a compact Rust role module as the worker authority, then delete or demote overlapping runtime entries.

## Runtime skill classification recommendations

### Keep as rare main/lead runtime skills, or lead-agent RoleComposition

- `human-interaction`: Keep as the main psyche-boundary module. It contains the durable intent/matter split at `.agents/skills/human-interaction/SKILL.md:13-19`, ask/act boundary at `.agents/skills/human-interaction/SKILL.md:21-26`, and privacy boundary at `.agents/skills/human-interaction/SKILL.md:42-43`.
- `intent-led-orchestration`: Do not leave as a general worker runtime skill. Keep only as a specialized lead/orchestrator mode or RoleComposition. Its distinctive content is orchestration gating and delegation, not general human interaction: fresh-start-only at `.agents/skills/intent-led-orchestration/SKILL.md:10`, no direct task work at `.agents/skills/intent-led-orchestration/SKILL.md:12-20`, and explicit approval gates at `.agents/skills/intent-led-orchestration/SKILL.md:28-35`.
- `intent-clarification`: Keep main/lead-facing or compose into intent-maintainer/lead roles. It decides when to ask the psyche versus proceed.
- `context-handover`, `context-maintenance`, `context-maintenance-deep`: Keep lead-facing. These are session/lane stewardship skills rather than worker task skills.
- `helper-context-transfer`: Keep lead-facing only. It is about briefing helpers and reading helper outputs, not about a subagent doing its own work.
- `session-lanes`: Keep lead/operator-facing. It covers lane registration/lifecycle, not ordinary task execution.
- `privacy` and `secrets`: Keep as safety-triggered runtime skills or compose into roles with relevant authority; they are rare but high-risk.

### Move to RoleComposition-only for spawned workers

- Implementation/review doctrine: `rust-discipline`, `rust-methods`, `rust-errors`, `rust-storage-and-wire`, `rust-crate-layout`, `abstractions`, `enum-contact-points`, `typed-records-over-flags`, `architectural-truth-tests`, `testing`, `naming`, `beauty`, `versioning`.
- Nix doctrine: `nix-discipline`, `nix-usage`.
- Repo/coordination doctrine: `jj`, `feature-development`, `main-feature-integration`, `repository-management`, `beads`, `bead-weaver`.
- Skill-system doctrine: `skill-editor`; the generated `skill-editor` role already contains the rule set at `.claude/agents/skill-editor.md:8-29` and the source module at `.claude/agents/skill-editor.md:138-174`.
- Intent operations: `intent-log`, `intent-maintenance`, `intent-manifestation`, `spirit-cli`, `repo-intent`; these fit the `intent-maintainer` role better than runtime discovery for arbitrary workers.
- Engine/design doctrine: `engine-analysis`, `engine-report`, `actor-systems`, `kameo`, `component-triad`, `contract-repo`, `micro-components`, `push-not-pull`, `structural-forms`, `nota-design`, `nota-comments`, `nota-schema-docs`, `mermaid`, `prose`, `library`, `architecture-editor`.

### Deletion or consolidation candidates

- `keep-working`: Recommendation: do not keep as general runtime. Its only plausible reader is the lead/main agent when a new psyche message arrives mid-task. Subagents should not need it because parent messages should arrive as explicit brief updates, and workers are already expected to complete their assigned task. Fold `.agents/skills/keep-working/SKILL.md:10-16` into `human-interaction` or a lead-agent RoleComposition; then delete the runtime skill.
- `reporting`: Recommendation: delete as a runtime skill after role/output modules are condensed. Its guidance at `.agents/skills/reporting/SKILL.md:10-27` overlaps the generated role output protocol, while role packets repeat even more detailed output rules.
- `engine-report`: Recommendation: consolidate into `engine-analysis` or a report-template module. It is an artifact shape while `engine-analysis` already includes output guidance at `.agents/skills/engine-analysis/SKILL.md:34-36`.
- `rust-discipline`: Recommendation: delete runtime index after ensuring Rust roles compose the needed modules. It is mostly an index/summary and duplicates concrete Rust skills.
- `abstractions` plus `rust-methods`: Recommendation: merge the shared “verb belongs to noun” rule into one Rust/core design module; keep only one runtime-facing version if any.
- `context-maintenance-deep`: Recommendation: fold into `context-maintenance` as an advanced lead-only section unless external synthesis finds strong value in two separate triggers.

## Specific answers

### Why would an agent read `keep-working`?

Only a psyche-facing lead/main agent would read it when the user sends a mid-task message and the model might incorrectly stop or ask whether to continue. The actual rules are concise and useful (`.agents/skills/keep-working/SKILL.md:10-16`), but the delivery vehicle is wrong for subagents: a spawned worker should receive new constraints through its parent/brief, not discover a runtime skill about human interruptions. Recommendation: fold it into `human-interaction` or lead-agent RoleComposition; delete or demote the standalone runtime skill after that migration.

### Should `intent-led-orchestration` absorb or depend on `human-interaction`?

It should depend on or compose with `human-interaction`, not absorb it wholesale. `human-interaction` owns the general psyche boundary: intent capture criteria, ask/act decisions, privacy, and real-world blocker handling at `.agents/skills/human-interaction/SKILL.md:13-43`. `intent-led-orchestration` owns a special high-ceremony startup mode: no direct file/tool inspection, explicit approval gates, worker dispatch, and synthesis from worker outputs only at `.agents/skills/intent-led-orchestration/SKILL.md:10-43`. Keep those separate in source if the mode remains, but emit them together only into the lead/orchestrator role packet.

## Code block / example recommendations

- Keep compact code examples in `jj`, `nix-usage`, `repository-management`, `spirit-cli`, `typed-records-over-flags`, `rust-errors`, `rust-crate-layout`, `nota-comments`, `nota-schema-docs`, and `bead-weaver`; they are syntax-bearing.
- Add a small code example to `enum-contact-points`: a nested match or trait contact point would make the rule at `.agents/skills/enum-contact-points/SKILL.md:10-16` more executable.
- Add a small before/after to `rust-methods`: lines `.agents/skills/rust-methods/SKILL.md:10-12` are important and compact, but a tiny free-function-to-method example would prevent misapplication.
- Consider adding a compact actor/message shape to `actor-systems` or `kameo` only if external benchmark examples show agents repeatedly miswriting actor state or replies. Otherwise the prose is already dense enough.

## Residual risks

- I inspected generated runtime skills and generated roles, not the generator source repository. Recommendations should be applied at source surfaces, not patched directly into `.agents` or `.claude` generated outputs.
- I did not run generator checks or role emission tests because this was a no-edit audit.
- I did not inspect private repositories.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings include exact file paths and line numbers for stale path, cross-reference, boilerplate, duplication, and example-gap observations."
    }
  ],
  "changedFiles": [
    "agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read /home/li/primary/plan.md",
      "result": "failed",
      "summary": "File was absent; review proceeded from progress and current corpus."
    },
    {
      "command": "read /home/li/primary/progress.md",
      "result": "passed",
      "summary": "Progress file contained only a generic In Progress stub."
    },
    {
      "command": "find/list/read generated skills and roles under .agents/skills, .claude/agents, .codex/agents, .pi/agents, and skills/generated-role-outputs.nota",
      "result": "passed",
      "summary": "Identified 55 generated runtime skills and 10 generated roles across active targets."
    },
    {
      "command": "python3 line-count/code-block summary for /home/li/primary/.agents/skills/*/SKILL.md",
      "result": "passed",
      "summary": "Found 55 skills; 45 <=60 lines, 52 <=80 lines, 3 >80 lines, 10 with code blocks."
    },
    {
      "command": "nl -ba selected skill and role files",
      "result": "passed",
      "summary": "Collected line-number evidence for keep-working, intent-led-orchestration, human-interaction, generated role modules, and candidate stale/cross-reference paths."
    },
    {
      "command": "git -C /home/li/primary status --short -- selected audit paths",
      "result": "passed",
      "summary": "Initial status check showed no listed changes before writing the requested report."
    },
    {
      "command": "git -C /home/li/primary status --porcelain=v1 -- agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md; git -C /home/li/primary diff --cached --name-only -- agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md",
      "result": "passed",
      "summary": "Report file is unstaged; cached diff for the report path is empty."
    }
  ],
  "validationOutput": [
    "Review artifact written to /home/li/primary/agent-outputs/SkillBenchmark/Reviewer-LocalPatterns.md.",
    "No code, source skills, generated roles, commits, or pushes were modified."
  ],
  "residualRisks": [
    "Generator source was not inspected; apply recommendations at source surfaces rather than generated outputs.",
    "No generator checks were run because this was a no-edit audit.",
    "plan.md was absent."
  ],
  "noStagedFiles": true,
  "diffSummary": "Requested review report only; no source corpus edits.",
  "reviewFindings": [
    "medium: .agents/skills/main-feature-integration/SKILL.md:8-10 - stale/local /git path language should be removed or made canonical.",
    "medium: .agents/skills/rust-crate-layout/SKILL.md:60-61 - See-Also-style references to skills/micro-components.md and lore rust/style.md conflict with self-contained runtime guidance.",
    "medium: .claude/agents/general-code-implementer.md:47-115 and .claude/agents/skill-editor.md:31-99 - repeated output/response boilerplate bloats role packets.",
    "low: .agents/skills/intent-clarification/SKILL.md:52-56 - internal skill path references should be replaced by direct guidance or role composition.",
    "low: .agents/skills/spirit-cli/SKILL.md:14-17 - description promises Observe/query/maintenance but only Record example is present.",
    "low: overlapping Rust doctrine across .agents/skills/abstractions/SKILL.md:10-19, .agents/skills/rust-methods/SKILL.md:8-12, and .agents/skills/rust-discipline/SKILL.md:10-14 should be consolidated into role modules."
  ],
  "manualNotes": "No blockers. Strongest strategic recommendation: make runtime skills lead/main-only and migrate worker doctrine into RoleComposition modules, with keep-working folded into human-interaction or lead-agent composition."
}
```
