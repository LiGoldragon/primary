# Research: Public AI skill/rules/prompt repository naming and structure patterns

## Summary
Public AI instruction systems mostly name reusable capabilities as task/domain nouns or verb phrases (`code-review`, `testing`, `docs`, `typescript`) and reserve role nouns (`reviewer`, `implementer`, `planner`) for agents, subagents, or workflow personas. The local direction, as visible from `/home/li/primary/AGENTS.md`, is unusually strong on operational doctrine, privacy boundaries, output discipline, and VCS/worktree rules; it should adopt external ecosystems' discoverable package metadata and concise README comparison language without adding broad prompt-library bloat.

Limitations: this run did not have a `web_search` or shell/clone tool available, so findings are based on accessible local files plus public documentation/repository knowledge through the model cutoff and canonical source URLs listed below. No public repositories were cloned or live-inspected in this run.

## Findings
1. **Skill names are usually task/domain nouns, while role names are used for agents/personas.** Claude Skills are packaged capabilities with a `SKILL.md` plus optional scripts/assets, so names tend to describe the capability or domain rather than the actor performing it. Cursor and Continue rules similarly tend to describe project guidance, framework conventions, or tasks. Agent frameworks such as AutoGen, Semantic Kernel, OpenAI Agents, and Google ADK model actors/agents separately from tools/instructions, so role-like names fit the agent layer, not the skill layer. [Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Cursor rules docs](https://docs.cursor.com/context/rules), [Continue docs](https://docs.continue.dev/), [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

2. **The strongest cross-ecosystem separation pattern is: global instructions -> project rules -> reusable skills/tools -> agents/roles -> runtime memory.** Cursor exposes Rules and Memories as distinct context surfaces; Windsurf similarly distinguishes rules/memories/user context; Claude Skills are reusable capability packages; Continue uses YAML/JSON config for models, context providers, slash commands, and rules; Aider uses repo conventions files and command-line/config settings; ADK/AutoGen/Semantic Kernel define agents, tools/plugins, memory, and orchestration as separate concepts. Local `/home/li/primary/AGENTS.md` already follows a similar split in prose: startup doctrine, doctrine loading, intent capture, output/report policy, hard boundaries, and VCS rules. [Cursor rules docs](https://docs.cursor.com/context/rules), [Windsurf docs](https://docs.windsurf.com/), [Continue config docs](https://docs.continue.dev/customize/overview), [Aider conventions](https://aider.chat/docs/usage/conventions.html), [Google ADK](https://google.github.io/adk-docs/), [Semantic Kernel agents](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/)

3. **Famous systems favor minimal, composable instruction files with explicit loading semantics.** Claude Skills use progressive disclosure: a short `SKILL.md` can point to scripts/assets that are loaded only when needed. Cursor rules support different applicability modes such as always, auto-attached, agent-requested, and manual. Continue uses central config and file-level context inclusion. Local doctrine loading has a similar intent: "Load additional doctrine only when the prompt, generated role packet, dispatch envelope, or local repo context explicitly requires it" in `/home/li/primary/AGENTS.md`. The local wording is directionally aligned with the best-known systems. [Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Cursor rules docs](https://docs.cursor.com/context/rules), [Continue config docs](https://docs.continue.dev/customize/overview), [`/home/li/primary/AGENTS.md`](../../AGENTS.md)

4. **Local categories that are unusually strong: hard operational boundaries, privacy/public-surface distinction, report discipline, and exact VCS command policy.** `/home/li/primary/AGENTS.md` has concrete policies that many public prompt/rules repos omit: do not inspect `private-repos/` without explicit authorization, no raw `git` except documented escape hatches, no `/nix/store` filesystem search, report only when the report itself is the requested or necessary working surface, and commit/push through `jj` with inline messages. These are stronger and more actionable than most public rule templates, which often stop at style/testing guidance. [`/home/li/primary/AGENTS.md`](../../AGENTS.md)

5. **Common categories in public repos that local may lack or could make more discoverable: skill package metadata, examples, test/validation recipes, language/framework-specific rules, security review checklists, and prompt-template libraries.** Claude Skills encourage a named directory containing `SKILL.md` plus scripts/assets; Cursor community rule repos often organize by language/framework; Continue configs advertise models/context providers/commands; Simon Willison's `llm` ecosystem uses named templates and plugins for repeatable prompts; Aider documents conventions for repo maps, architect/editor modes, lint/test commands, and conventions files. Local doctrine has strong process rules but, from the inspected file, lacks a public index of skill categories and examples. [Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Cursor Directory](https://cursor.directory/), [Aider docs](https://aider.chat/docs/), [llm templates](https://llm.datasette.io/en/stable/templates.html)

6. **Matt Pocock/Total TypeScript influence is best described as a documentation-grounded adversarial learning pattern, not a standard repository structure.** The public phrase "grill me with docs" appears associated with Total TypeScript-style interactive pedagogy: provide source docs and have the model quiz/challenge the learner from them. The transferable pattern for local skills is a `study-from-docs` or `docs-drill` task skill with inputs, expected behavior, and citation requirements, not a role named `griller`. Recommended naming: noun/task phrase such as `documentation-drill`, `docs-study`, or `source-grounded-quiz`. [Total TypeScript](https://www.totaltypescript.com/), [Matt Pocock site](https://www.mattpocock.com/)

7. **OpenAI/Google/Microsoft agent frameworks reinforce avoiding the word "skill" for everything.** OpenAI Agents SDK centers agents, tools, handoffs, guardrails, and tracing. Google ADK centers agents, tools, sessions, artifacts, memory, and evaluation. AutoGen and Semantic Kernel distinguish agents from tools/plugins/functions and group-chat/orchestration patterns. Local docs should preserve this separation: `skills` for reusable task capabilities, `agents` or `roles` for personas/workflow seats, `doctrine/rules` for durable constraints, `memory` for retained context, and `templates` for prompts. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), [Google ADK docs](https://google.github.io/adk-docs/), [AutoGen docs](https://microsoft.github.io/autogen/), [Semantic Kernel docs](https://learn.microsoft.com/en-us/semantic-kernel/)

8. **Public skill/rules repositories are useful as similarity references, but many are lower quality than the local doctrine.** Cursor rule directories and awesome lists provide breadth and examples, but many entries are SEO-heavy, duplicated, or framework-specific boilerplate. Anthropic, OpenAI, Google, Microsoft, Aider, Continue, and Simon Willison sources are better anchors for README influence language because they describe actual runtime semantics, not just prompt snippets. [Cursor Directory](https://cursor.directory/), [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules), [Anthropic docs](https://docs.anthropic.com/), [Aider docs](https://aider.chat/docs/)

## Comparison to local direction

| Area | Public/acclaimed pattern | Local observed pattern | Recommendation |
| --- | --- | --- | --- |
| Skill naming | Task/domain nouns: `testing`, `docs`, `typescript`, `code-review`; sometimes verb phrases | Local prompt asks whether to use `implementation` vs `implementer`; inspected `AGENTS.md` uses doctrine/policy names, not skill package names | Use nouns/task phrases for skills: `implementation`, `code-review`, `research`, `docs-drill`; use role nouns only for agents: `implementer`, `reviewer`, `researcher` |
| Skill vs agent separation | Skills/tools are reusable capabilities; agents are actors with instructions, tools, handoffs | Local generated worker packets and hard boundaries imply this split | Document it explicitly in README: "Skills are capabilities; agents/roles are execution personas" |
| Loading semantics | Progressive/contextual loading in Claude Skills, Cursor rule modes, Continue context providers | `AGENTS.md` explicitly says load extra doctrine only when required | Keep and promote this as a design principle |
| Memory/rules separation | Cursor/Windsurf distinguish rules from memories | Local distinguishes durable doctrine and intent capture; private info closed by default | Keep strict privacy language; add short definitions for rule, memory, doctrine, skill |
| Packaging | Claude uses `SKILL.md`; Continue uses config; Aider uses conventions files | Local inspected file is a root boot contract | If creating public skills, adopt `skills/<task>/SKILL.md` with optional `examples/`, `scripts/`, `fixtures/` |
| Categories | Language/framework, testing, security, docs, migrations, review, planning, debugging, release | Local visibly covers startup, output, privacy, VCS, doctrine loading | Add public index categories only where real local skills exist; avoid empty taxonomy |

## Naming answer

Use this convention:

- **Skills:** noun or task phrase, preferably singular capability names: `implementation`, `code-review`, `research`, `validation`, `documentation`, `migration`, `release`, `docs-drill`.
- **Agents/roles:** actor/persona names: `implementer`, `reviewer`, `researcher`, `planner`, `release-manager`.
- **Rules/doctrine:** constraint or scope names: `output-policy`, `privacy-boundaries`, `vcs-policy`, `doctrine-loading`.
- **Templates:** prompt/use-case names: `bug-report-triage`, `api-design-review`, `source-grounded-quiz`.
- **Memory:** fact domain names, never broad task names: `project-preferences`, `repo-topology`, `toolchain-notes`.

Avoid making every capability an `-er` role. `implementer` should be the agent who may invoke the `implementation` skill; `reviewer` should invoke `code-review` or `validation`.

## Categories famous repos have that local may lack

1. Language/framework rule packs: TypeScript, React, Python, Rust, Rails, Django, Tailwind, Next.js.
2. Security-specific checklists: threat modeling, dependency review, secrets handling, auth/session review.
3. Evaluation/benchmark recipes: expected outputs, golden tests, regression prompts, trace review.
4. Prompt templates: reusable named templates with arguments, as in Simon Willison `llm` templates.
5. Tool configuration examples: Continue model/context config, Aider lint/test commands, agent framework tool/plugin examples.
6. Skill package examples with assets/scripts, like Claude Skills.
7. Learning/study modes: docs-grounded quizzes, flashcards, adversarial review, "grill me from this source".

## Local categories that are unusual or strong

1. Explicit private/public boundary: `private-repos/` is closed by default.
2. Output/report discipline: reports only when needed as durable working surfaces.
3. Doctrine loading economy: load extra doctrine only when explicitly required.
4. Strong VCS policy: `jj` workflow, no raw `git`, no editor-opening commands.
5. Intent capture safeguards: avoids turning incidental utterances into durable intent.
6. Operational filesystem constraints: no `/nix/store` search.

These should be advertised as differentiators, not hidden in a long rules file.

## Wording/patterns to adopt without bloat

1. Add a compact glossary:
   - **Skill:** reusable task capability, named as a noun/task.
   - **Agent/role:** execution persona, named as an actor.
   - **Doctrine/rule:** durable constraint or policy.
   - **Memory:** retained context, governed by privacy policy.
   - **Template:** reusable prompt shape.

2. Add one package convention:
   - `skills/<skill-name>/SKILL.md` for capability instructions.
   - Optional `examples/`, `scripts/`, `fixtures/`, `references.md` only when used.
   - Keep `SKILL.md` short and load extra files only on demand.

3. Add naming guidance:
   - Prefer task nouns for skills: `implementation`, `validation`, `research`.
   - Prefer actor nouns for agents: `implementer`, `validator`, `researcher`.
   - Prefer policy nouns for rules: `privacy-boundaries`, `output-policy`.

4. Add a "not a prompt dump" sentence:
   - "This repository follows progressive disclosure: global boot rules stay small, and specialized doctrine/skills load only when the task asks for them."

5. Add examples only for categories actually present. Do not import large community rule packs unless local projects need them.

## Recommended README section: Similar repositories and influences

Suggested heading: **Similar repositories and influences**. This is safer than only "Influenced by" because some entries are parallels rather than direct inspirations.

Suggested entries:

- **Anthropic Claude Skills** — closest packaging analogy: small capability directories with `SKILL.md` and optional supporting files; useful precedent for noun/task skill names and progressive disclosure. https://docs.anthropic.com/en/docs/claude-code/skills
- **Cursor Rules and Memories** — useful distinction between project rules, user rules, and remembered context; supports making local `doctrine/rules/memory` boundaries explicit. https://docs.cursor.com/context/rules
- **Windsurf rules/memories** — parallel IDE-agent model for persistent instructions and memories; useful comparison for privacy and scope language. https://docs.windsurf.com/
- **Continue configuration** — good precedent for declarative config, context providers, slash commands, and model/tool configuration separate from prose rules. https://docs.continue.dev/
- **Aider conventions** — practical repository-level conventions for coding agents, including lint/test commands and project guidance files. https://aider.chat/docs/usage/conventions.html
- **OpenAI Agents SDK** — reinforces separating agents, tools, handoffs, guardrails, and tracing rather than calling everything a skill. https://openai.github.io/openai-agents-python/
- **Google Agent Development Kit** — agent/tool/session/artifact/memory/eval vocabulary useful for future agent runtime alignment. https://google.github.io/adk-docs/
- **Microsoft AutoGen and Semantic Kernel** — mature agent orchestration and plugin/tool abstractions; useful terminology for multi-agent roles vs reusable tools. https://microsoft.github.io/autogen/ and https://learn.microsoft.com/en-us/semantic-kernel/
- **Simon Willison `llm` templates** — strong example of named, reusable prompt templates with arguments, distinct from agents or rules. https://llm.datasette.io/en/stable/templates.html
- **Cursor community rule repositories** — broad examples of language/framework rules; useful for comparison, but should be treated as inspiration rather than quality baseline. https://cursor.directory/ and https://github.com/PatrickJS/awesome-cursorrules
- **Total TypeScript / Matt Pocock docs-grounded learning style** — useful influence for a `docs-drill` or `source-grounded-quiz` skill that quizzes users from supplied documentation. https://www.totaltypescript.com/

## Sources

- Kept: Anthropic Claude Skills documentation (https://docs.anthropic.com/en/docs/claude-code/skills) — primary source for skill packaging and progressive disclosure.
- Kept: Cursor Rules documentation (https://docs.cursor.com/context/rules) — primary source for rule scope/application patterns.
- Kept: Cursor Directory (https://cursor.directory/) — public examples of community rule naming/categories.
- Kept: Windsurf documentation (https://docs.windsurf.com/) — source for rules/memory-style IDE agent concepts.
- Kept: Continue documentation (https://docs.continue.dev/) — source for config/context/rules separation.
- Kept: Aider conventions documentation (https://aider.chat/docs/usage/conventions.html) — source for repo-level conventions and coding-agent practices.
- Kept: OpenAI Agents SDK docs (https://openai.github.io/openai-agents-python/) — primary source for agent/tool/handoff/guardrail separation.
- Kept: Google ADK docs (https://google.github.io/adk-docs/) — primary source for agent, tool, session, memory, artifact, eval vocabulary.
- Kept: Microsoft AutoGen docs (https://microsoft.github.io/autogen/) — primary source for multi-agent framework vocabulary.
- Kept: Microsoft Semantic Kernel docs (https://learn.microsoft.com/en-us/semantic-kernel/) — primary source for agents/plugins/functions terminology.
- Kept: Simon Willison `llm` templates docs (https://llm.datasette.io/en/stable/templates.html) — source for reusable named prompt-template pattern.
- Kept: Total TypeScript and Matt Pocock sites (https://www.totaltypescript.com/, https://www.mattpocock.com/) — source family for docs-grounded TypeScript teaching influence.
- Kept: Local `/home/li/primary/AGENTS.md` — direct evidence for local doctrine and unusual strengths.
- Dropped: Generic prompt-library and SEO-heavy rules pages — often duplicate community examples without runtime semantics.
- Dropped: Stale agent-framework blog posts — weaker than official docs for current terminology.
- Dropped: Unverified clones/live repository file claims — no shell/clone/web-fetch tool was available in this run.

## Gaps

- Could not run live `web_search`, clone public repos, or inspect current GitHub file trees because no such tools were available to this subagent.
- Could not enumerate the full local skill tree because only exact-path file reads were available; the only local file directly inspected was `/home/li/primary/AGENTS.md` plus the `CLAUDE.md` symlink target.
- The Matt Pocock/Total TypeScript "grill me with docs" phrasing should be verified with a targeted web search or transcript lookup before claiming direct influence.
- Suggested next steps: run a follow-up with web/clone access to sample 10-20 actual repos, record exact file paths such as `.cursor/rules/*.mdc`, `skills/*/SKILL.md`, `.continue/config.yaml`, `AGENTS.md`, `CLAUDE.md`, `.aider.conf.yml`, and compare local repository paths directly.

## Supervisor coordination

No supervisor escalation was possible or needed; the main blocker was missing web/clone/search tooling, disclosed above.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings include local file path `/home/li/primary/AGENTS.md`, output path `/home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md`, cited public source URLs, and severity-style residual risk notes for unavailable web/clone verification."
    }
  ],
  "changedFiles": [
    "/home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read /home/li/primary/AGENTS.md",
      "result": "passed",
      "summary": "Inspected local boot contract for local direction."
    },
    {
      "command": "read /home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md",
      "result": "passed",
      "summary": "Confirmed the report did not previously exist."
    },
    {
      "command": "write /home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md",
      "result": "passed",
      "summary": "Wrote the requested research brief to the authoritative output path."
    }
  ],
  "validationOutput": [
    "Report written to `/home/li/primary/agent-outputs/SkillBenchmark/PublicRepoComparison.md`.",
    "No live web search, clone, or shell validation was available in this subagent run."
  ],
  "residualRisks": [
    "medium: Public-source citations and repository patterns could not be live-verified because `web_search`/clone tools were unavailable.",
    "medium: Local comparison is based only on `/home/li/primary/AGENTS.md`; full local skill tree was not enumerable with available tools.",
    "low: Matt Pocock/Total TypeScript 'grill me with docs' influence requires targeted live verification before being framed as direct influence."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added a concise source-backed comparison report with recommendations, README influence section, gaps, and acceptance report.",
  "reviewFindings": [
    "no blockers: output report created at required path",
    "warning: live web/clone inspection was unavailable, so report flags verification gaps explicitly"
  ],
  "manualNotes": "Acceptance is attested with disclosed tooling limitations. No repository source files were modified beyond the requested report artifact."
}
```
