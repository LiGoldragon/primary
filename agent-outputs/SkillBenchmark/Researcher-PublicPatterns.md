# Research: Public AI skills/rules/agent-instruction patterns

## Summary
Influential public systems converge on a few patterns: keep a small always-loaded project contract, load task-specific instruction units just-in-time, and make units concrete with metadata, explicit triggers, examples, and source-of-truth links. The strongest models are Anthropic Claude Skills for runtime capability loading, Cursor/Windsurf/Continue for repo-local rule scoping, Aider for terse conventions plus examples, and OpenAI/Google/Microsoft guidance for operational guardrails and tool-use discipline.

## Findings
1. **Most influential public examples cluster into “skills,” “repo rules,” and “agent operating manuals.”** Anthropic’s Claude Skills define reusable folders containing a `SKILL.md` plus optional scripts/assets, giving a public pattern for capability modules that can be discovered and loaded only when relevant. [Anthropic Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/overview)

2. **Cursor popularized repo-local rule files with explicit scopes.** Cursor rules live under `.cursor/rules` and support project rules, always-applied rules, and agent-requested rules; this is a useful public precedent for separating universal doctrine from task-triggered packets. [Cursor Rules docs](https://docs.cursor.com/context/rules)

3. **Windsurf uses a similar “memories/rules” model but emphasizes persistent context and team conventions.** Its rule files are intended to preserve coding standards and project-specific behavior across sessions, which is valuable but risks stale instructions if not tied to source-of-truth files. [Windsurf Memories docs](https://docs.windsurf.com/windsurf/memories)

4. **Continue.dev demonstrates provider-agnostic prompt/rule composition.** Continue supports custom instructions, slash commands, context providers, and reusable assistant configuration in YAML, showing that instruction units should be composable and model/tool independent where possible. [Continue customization docs](https://docs.continue.dev/customize/overview), [Continue config docs](https://docs.continue.dev/reference)

5. **Aider’s conventions favor terse repo guidance and examples over elaborate policy prose.** Aider uses repo maps and optional convention files such as `CONVENTIONS.md` / `.aider.conf.yml`-style project configuration; its public guidance encourages adding concise, concrete examples of project style rather than long generic instructions. [Aider conventions](https://aider.chat/docs/usage/conventions.html), [Aider configuration](https://aider.chat/docs/config.html)

6. **OpenAI’s Agents/Codex guidance stresses tool clarity, sandboxing, and environment contracts.** The useful transferable pattern is not a “skill repo” but precise developer instructions: what tools can do, when to call them, how to validate results, and how to report uncertainty. [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/), [OpenAI Codex docs](https://platform.openai.com/docs/codex)

7. **Google and Microsoft agent guidance emphasizes agent roles, state, evals, and observability.** Google’s Agent Development Kit and Microsoft AutoGen/Semantic Kernel show mature patterns for agent capability boundaries, tool registration, orchestration separation, and evaluation; these map well to role packets and supervisor/worker separation. [Google ADK docs](https://google.github.io/adk-docs/), [Microsoft AutoGen docs](https://microsoft.github.io/autogen/), [Semantic Kernel docs](https://learn.microsoft.com/en-us/semantic-kernel/)

8. **Simon Willison’s LLM tooling is influential for plain-text, inspectable prompts and reproducible logs.** The `llm` ecosystem favors small templates/fragments, explicit model/tool invocations, and reproducible command history rather than hidden prompt magic. [llm project](https://llm.datasette.io/), [llm templates](https://llm.datasette.io/en/stable/templates.html)

9. **Widely starred “awesome” repos are best used as discovery indexes, not design authority.** Lists such as `e2b-dev/awesome-ai-agents`, `kyrolabs/awesome-agents`, and `steven2358/awesome-generative-ai` surface projects but rarely provide instruction-unit design norms. Keep them as source discovery only. [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents), [kyrolabs/awesome-agents](https://github.com/kyrolabs/awesome-agents), [steven2358/awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai)

10. **Instruction units are usually scoped by applicability, not topic breadth.** Best examples define a unit around a task boundary: “write a migration,” “review security-sensitive code,” “use this test runner,” or “format docs,” not broad categories like “engineering best practices.” Claude Skills and Cursor rules both work best when a name/description can act as a retrieval trigger. [Anthropic Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Cursor Rules docs](https://docs.cursor.com/context/rules)

11. **Naming patterns should optimize retrieval and operator inspection.** Public conventions favor short, hyphenated, noun-verb or domain-task names: `create-pdf`, `brand-guidelines`, `python-tests`, `release-notes`, `security-review`. Avoid cute names, internal mythology, or overloaded names unless there is a separate plain-English description.

12. **Descriptions are critical trigger metadata.** The most useful rule/skill units include a 1-3 sentence description saying when to use the unit, when not to use it, and what output it governs. Without this, systems drift toward always-loading too much context or missing the unit entirely.

13. **Size: effective units are small at load time and can reference larger assets.** Claude Skills explicitly allow optional files/scripts/assets adjacent to `SKILL.md`, which is a strong pattern: keep the prompt-facing file short and defer bulky examples, templates, scripts, or schemas to referenced files. [Anthropic Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills)

14. **Examples help when they are executable, style-defining, or disambiguating; they bloat when they restate policy.** Good examples include before/after code, canonical command invocations, expected output formats, or one minimal full workflow. Bad examples are long transcripts, generic “be careful” demonstrations, or stale file-tree snapshots.

15. **Runtime loading beats always-loaded rules for specialized behavior.** Always-loaded rules should be limited to safety, workspace invariants, delegation boundaries, and output contracts. Specialized skills should load by role, task trigger, repo path, or explicit user request. This is the shared lesson from Claude Skills, Cursor scoped rules, and Continue composable config. [Anthropic Claude Skills docs](https://docs.anthropic.com/en/docs/claude-code/skills), [Cursor Rules docs](https://docs.cursor.com/context/rules), [Continue customization docs](https://docs.continue.dev/customize/overview)

16. **Role/agent-specific packets remain valuable for orchestration boundaries.** Microsoft AutoGen and Google ADK both separate agent identity/capability/tooling from task state; this supports the local pattern of generated role packets for reviewers, researchers, implementers, and supervisors. [Microsoft AutoGen docs](https://microsoft.github.io/autogen/), [Google ADK docs](https://google.github.io/adk-docs/)

17. **Dependencies should be declared as references, not copied prose.** Strong public patterns keep generated outputs, scripts, schemas, and examples adjacent to the unit or linked as canonical references. Copying long upstream instructions into many rule files creates provenance and staleness risks.

18. **Avoid stale paths by using repository-relative references and validation hooks.** Rule files often rot because they mention moved files, commands, or branches. Prefer `path:` metadata, repo-relative links, and lightweight checks that verify referenced files exist.

19. **Generated outputs need provenance banners and regeneration commands.** If a skill/rule is generated, include source file, generator command, timestamp or source revision, and “do not edit generated section” boundaries. This is common in mature docs/tool ecosystems even if not uniformly present in AI rule repos.

20. **Source-of-truth should live outside prompts when possible.** Let prompts point to code, schemas, tests, ADRs, and package manager scripts. The prompt should state how to find truth and how to validate, not duplicate every current fact.

## Concrete recommendations for the local skills/role system
1. **Adopt a skill header schema.** For each skill/rule/role packet, require: `name`, `summary`, `use_when`, `avoid_when`, `inputs`, `outputs`, `dependencies`, `source_of_truth`, `validation`, and `last_reviewed`.
2. **Split always-loaded doctrine from task skills.** Keep only universal workspace invariants in always-loaded files like `AGENTS.md`; move topic/task details into triggerable skills or role packets.
3. **Use one screen of prompt-facing instruction.** Target roughly 200-800 words for the main skill body; move long examples, scripts, templates, and schemas to sibling files.
4. **Make triggers explicit.** Add concrete trigger phrases and path globs, e.g. `use_when: editing Rust crates`, `paths: crates/**`, `avoid_when: documentation-only change`.
5. **Prefer examples that prove format or workflow.** Include one minimal good example when output format, command order, or coding style is non-obvious; remove examples that merely repeat rules.
6. **Declare dependencies by path/URL.** Avoid copying canonical text. Reference repo-relative files and public docs, and include a simple existence check for local paths.
7. **Add staleness review fields.** Track `last_reviewed`, `owner`, and `review_after` for skills that mention tools, APIs, or file paths.
8. **Require provenance for generated instruction files.** Generated role packets should say what generated them and which source files/versions they include.
9. **Use role packets for capability boundaries.** Keep researcher/reviewer/implementer/supervisor responsibilities in role-specific generated packets rather than asking one always-loaded rule file to describe every mode.
10. **Build a lint/check command for the skill corpus.** Validate required headers, broken local links, oversized prompt bodies, duplicate names, missing trigger descriptions, and stale review dates.

## Patterns to avoid
1. **Avoid monolithic global rule files.** They hide conflicts, waste context, and make retrieval impossible.
2. **Avoid generic virtue rules.** “Be concise,” “write clean code,” and “think carefully” are low-value unless tied to a specific observable behavior.
3. **Avoid copied upstream docs.** Link to canonical docs instead; summarize only the local operational consequence.
4. **Avoid examples as transcripts.** Long chat transcripts are rarely reusable and quickly become misleading.
5. **Avoid path-heavy prose without validation.** File paths are useful only if they are repo-relative and checked.
6. **Avoid mixing supervisor policy into worker task instructions.** Keep orchestration authority separate from execution role packets.
7. **Avoid hidden magic triggers.** If a skill is loaded by a path, role, command, or phrase, document that trigger.

## Sources
- Kept: Anthropic Claude Skills docs (https://docs.anthropic.com/en/docs/claude-code/skills) — primary source for runtime skill packaging and `SKILL.md` pattern.
- Kept: Anthropic Claude Code overview (https://docs.anthropic.com/en/docs/claude-code/overview) — primary source for Claude Code operating model.
- Kept: Cursor Rules docs (https://docs.cursor.com/context/rules) — primary source for repo-local scoped rules.
- Kept: Windsurf Memories docs (https://docs.windsurf.com/windsurf/memories) — primary source for persistent rule/memory model.
- Kept: Continue customization docs (https://docs.continue.dev/customize/overview) — primary source for composable assistant customization.
- Kept: Continue reference docs (https://docs.continue.dev/reference) — source for configuration/reference patterns.
- Kept: Aider conventions docs (https://aider.chat/docs/usage/conventions.html) — primary source for concise project convention files.
- Kept: Aider configuration docs (https://aider.chat/docs/config.html) — source for project-level configuration behavior.
- Kept: OpenAI Agents SDK docs (https://openai.github.io/openai-agents-python/) — primary source for agent/tool/guardrail patterns.
- Kept: OpenAI Codex docs (https://platform.openai.com/docs/codex) — source for Codex agent guidance and environment contracts.
- Kept: Google ADK docs (https://google.github.io/adk-docs/) — source for role/tool/orchestration design patterns.
- Kept: Microsoft AutoGen docs (https://microsoft.github.io/autogen/) — source for multi-agent role/capability boundaries.
- Kept: Microsoft Semantic Kernel docs (https://learn.microsoft.com/en-us/semantic-kernel/) — source for skills/plugins/kernel separation.
- Kept: Simon Willison `llm` docs (https://llm.datasette.io/) — source for inspectable prompt/template practice.
- Kept: Simon Willison `llm` templates (https://llm.datasette.io/en/stable/templates.html) — source for small reusable template patterns.
- Dropped: Generic “top AI agents” blog posts — excluded because they are SEO-heavy and rarely expose instruction design.
- Dropped: Awesome lists as primary evidence — useful for discovery, but excluded from pattern conclusions unless they point to primary docs.
- Dropped: Vendor marketing pages without implementation docs — excluded because they do not show concrete instruction-unit structure.

## Gaps
- I did not have access to a live web-search tool in this runtime, so URLs and patterns are based on known public documentation rather than freshly fetched pages.
- Star counts and “most acclaimed” ranking were not verified live; treat acclaim as influence-by-adoption/documentation visibility rather than a current quantitative ranking.
- Next step: run a live pass over GitHub star counts and current docs for `.cursor/rules`, Claude Skills examples, Continue assistant configs, and popular public rules repositories.

## Supervisor coordination
No supervisor decision was needed. The only limitation was lack of live web-search access in this worker runtime.

## Acceptance report
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete sourced findings and recommendations are written to /home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md; review findings and residual risks are included."
    }
  ],
  "changedFiles": [
    "/home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Report written to the required output path. Live web validation was not possible because no web_search tool was available in this runtime."
  ],
  "residualRisks": [
    "No live web search/fetch was available; current star counts, newest docs changes, and exact latest repository structures were not independently verified."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added a research brief comparing public AI skills/rules/agent-instruction patterns and recommendations for the local skills/role system.",
  "reviewFindings": [
    "no blockers",
    "info: /home/li/primary/agent-outputs/SkillBenchmark/Researcher-PublicPatterns.md - live web-search requirement could not be satisfied in this runtime because no web_search tool was available"
  ],
  "manualNotes": "The brief prioritizes primary documentation and known public frameworks; recommend a follow-up live verification pass if exact current popularity/ranking matters."
}
```
