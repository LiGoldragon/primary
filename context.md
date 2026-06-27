# Code Context

## Files Retrieved
1. `/home/li/primary/AGENTS.md` (lines 1-49) - confirms Pi startup instructions in this workspace and that only `skills/skills.nota` is intended as default discovery read.
2. `/home/li/primary/skills/skills.nota` (lines 1-92 shown by tool output) - large skill index explicitly required by AGENTS/user; about 17.9 KB raw text.
3. `/home/li/.local/share/criomos/pi/package/src/core/resource-loader.ts` (lines 1-180, 275-289 via grep) - AGENTS/CLAUDE context-file discovery, resource loader getters, and options including `noContextFiles`.
4. `/home/li/.local/share/criomos/pi/package/src/cli/args.ts` (lines 150-290) - CLI flags: `--no-context-files`, `--no-skills`, `--no-extensions`, etc.
5. `/home/li/.local/share/criomos/pi/package/src/core/system-prompt.ts` (lines 1-190) - exact system-prompt construction: default Pi prompt, context files, available skills, date/cwd.
6. `/home/li/.local/share/criomos/pi/package/src/core/agent-session.ts` (lines 760-840, 880-960, 2960-3035) - active tools are installed on agent, system prompt rebuilt from resource loader, context usage computation.
7. `/home/li/.local/share/criomos/pi/package/src/core/compaction/compaction.ts` (lines 120-200) - token usage calculation and estimates.
8. `/home/li/.local/share/criomos/pi/package/src/core/skills.ts` (lines 1-460) - skill discovery and `formatSkillsForPrompt` behavior.
9. `/home/li/.local/share/criomos/pi/package/src/core/package-manager.ts` (grep line locators around 158-205, 886-891, 2259-2489) - package manifests load extensions/skills/prompts/themes from configured packages and user/project dirs.
10. `/home/li/.pi/agent/settings.json` (lines 1-41) - installed packages and model/compaction settings; no secret values inspected.
11. `/home/li/.pi/agent/packages/*/package.json` (top manifest snippets via read-only Python) - package `pi` manifest resource lists.
12. `/home/li/.pi/agent/packages/pi-subagents/src/extension/index.ts` (grep snippets) - registers `subagent` tool with large description and parameter schema.
13. `/home/li/.pi/agent/packages/pi-web-access/index.ts` (grep snippets) - registers web/search/fetch tools with verbose parameter descriptions.
14. `/home/li/.pi/agent/packages/pi-linkup/src/extensions/*/*.{ts}` (grep snippets) - registers Linkup web tools.
15. `/home/li/.pi/agent/packages/*/skills/**/SKILL.md` (file-size/frontmatter snippets via read-only Python) - package skills and descriptions.

## Key Code

Confirmed system prompt injection path:

```ts
// /home/li/.local/share/criomos/pi/package/src/core/agent-session.ts:923-936
const loadedSkills = this._resourceLoader.getSkills().skills;
const loadedContextFiles = this._resourceLoader.getAgentsFiles().agentsFiles;
this._baseSystemPromptOptions = { cwd: this._cwd, skills: loadedSkills,
  contextFiles: loadedContextFiles, customPrompt: loaderSystemPrompt,
  appendSystemPrompt, selectedTools: validToolNames, toolSnippets, promptGuidelines };
return buildSystemPrompt(this._baseSystemPromptOptions);
```

```ts
// /home/li/.local/share/criomos/pi/package/src/core/system-prompt.ts:130-169
let prompt = `You are an expert coding assistant operating inside pi...`;
// appends <project_context> with full context file contents
// then appends <available_skills> if read tool is available
```

Confirmed AGENTS/CLAUDE loading:

```ts
// /home/li/.local/share/criomos/pi/package/src/core/resource-loader.ts:67-109
const candidates = ["AGENTS.md", "AGENTS.MD", "CLAUDE.md", "CLAUDE.MD"];
// load global context from agentDir, then cwd ancestor context files, unshifted root-to-leaf
```

Confirmed configurability:

```text
// /home/li/.local/share/criomos/pi/package/src/cli/args.ts:270
--no-context-files, -nc        Disable AGENTS.md and CLAUDE.md discovery and loading
```

Confirmed skills prompt does not include full skill bodies, only metadata:

```ts
// /home/li/.local/share/criomos/pi/package/src/core/skills.ts:330-344
<available_skills>
  <skill><name>...</name><description>...</description><location>...</location></skill>
</available_skills>
```

Confirmed context percentage display:

```ts
// /home/li/.local/share/criomos/pi/package/src/core/agent-session.ts:2995-3033
const contextWindow = model.contextWindow ?? 0;
const estimate = estimateContextTokens(this.messages);
const percent = (estimate.tokens / contextWindow) * 100;
```

```ts
// /home/li/.local/share/criomos/pi/package/src/core/compaction/compaction.ts:136-137
return usage.totalTokens || usage.input + usage.output + usage.cacheRead + usage.cacheWrite;
```

## Architecture

Pi builds a base system prompt at session creation/active-tool changes from:

1. Core Pi default system prompt (`system-prompt.ts`) unless a custom prompt is supplied.
2. One-line prompt snippets/guidelines from active tools.
3. Full contents of discovered context files (`AGENTS.md`/`CLAUDE.md`) from `~/.pi/agent` and cwd ancestors.
4. Available skill metadata from user/project/package skills, as XML containing name, description, and absolute location only.
5. Current date and working directory.

Separately, `agent.state.tools` holds full tool definitions (`name`, `description`, `parameters` schema). These tool schemas are sent to the provider as tools/function declarations by the underlying agent layer and are included in provider input-token accounting even though they are not printed in the visible system prompt. This is inferred from `AgentSession.setActiveToolsByName` placing full `AgentTool`s on `agent.state.tools` and export/session code preserving `tools: {name, description, parameters}`; exact provider serialization was not fully traced in this read-only pass.

Configured packages in `/home/li/.pi/agent/settings.json` are loaded by package manager resource discovery. Current enabled packages are:

- `packages/pi-criomos`: theme switcher extension; one `gws` skill.
- `packages/pi-linkup`: 4 extensions, 3 registered web tools, one skill.
- `packages/pi-web-access`: one extension, 3 visible heavy web tools plus commands, one skill.
- `packages/pi-subagents`: one extension, subagent tool(s), prompts, one skill.
- `packages/pi-continue`: one extension, commands/no package skill in manifest.

Confirmed/inferred relative contribution estimates for first-agent-launch bloat:

- Confirmed visible project prompt: `/home/li/primary/AGENTS.md` is 2,771 chars, roughly 700-1,000 tokens after XML wrapping. Severity: low/medium.
- Confirmed mandatory first tool-read output: `/home/li/primary/skills/skills.nota` is 17,903 chars, roughly 4,500-6,000 tokens, and appears in conversation history before first subagent because AGENTS/user require reading it. Severity: high for Pi-vs-plain-Codex comparison if Codex does not do this read.
- Confirmed package skill *metadata* in system prompt: only descriptions/locations, not full bodies. Likely <1,500 tokens total, except long `pi-subagents` description may be a few hundred tokens. Severity: low/medium.
- Inferred tool schema overhead: likely large. Enabled extension tools include `subagent`, Linkup search/answer/fetch, `web_search`, `fetch_content`, `get_search_content`, plus built-ins. `pi-web-access` and `pi-subagents` have very verbose descriptions/parameter schemas; this can plausibly dominate hidden provider input tokens. Severity: high.
- Confirmed package skill bodies are not automatically injected. `pi-subagents/SKILL.md` is 57,616 chars, but only its frontmatter description/location enters the prompt unless the model reads the skill. Severity: not a startup cause.
- No image attachment metadata found in current startup path. Package manifests include image/video URLs (`pi-continue`, `pi-linkup`, `pi-web-access`), but these are package metadata, not evidence of LLM prompt image attachments. Severity: not confirmed.
- Prior messages/session history: only if `--continue`, `--resume`, `--session`, or existing chosen session is used. This task did not inspect session logs for secret-minimization reasons beyond listing non-secret paths. Severity: conditional.

Top likely bloat causes, ranked:

1. Extension tool schemas, especially `pi-subagents` and `pi-web-access` (inferred high). They add long tool descriptions and JSON schemas to every provider call when enabled.
2. The workspace boot contract forces reading `skills/skills.nota` (confirmed high). This is not startup system-prompt injection by Pi core, but it is in context before/around first subagent launch in normal primary workflow.
3. Full `AGENTS.md` injection by Pi core (confirmed medium/low). Core behavior, configurable with `--no-context-files` / `-nc`.
4. Available skill metadata from packages/project (confirmed low/medium). Not full skill files.
5. Subagent launch prompts may add parent/developer/runtime bridge instructions and child-specific tool schemas (confirmed current child prompt is large; core source indicates subagent extension owns launch prompt construction, but exact serialization not fully traced). Likely significant around first subagent launch.

Answers to specific questions:

- How Pi computes/displays context percentage: `getContextUsage()` uses model `contextWindow`, estimates context tokens from messages via `estimateContextTokens`, and computes `tokens/contextWindow*100`; after assistant responses it can use provider usage (`totalTokens` or input+output+cacheRead+cacheWrite), and after compaction it reports unknown until a post-compaction assistant usage exists. Footer displays this percentage with one decimal and context window.
- Exact startup injected content: default Pi system prompt; active tool one-line snippets/guidelines; full AGENTS/CLAUDE context files from global agent dir and cwd ancestors; available skills XML metadata for loaded skills; date and cwd. Full tool schemas are attached as active tools outside visible system prompt. Package skills are listed by metadata only. Prior messages only on resume/continue. No confirmed image attachment metadata.
- Which installed packages likely contribute most: `pi-subagents` and `pi-web-access` via tool schemas; `pi-linkup` next; `pi-criomos` low; `pi-continue` mostly commands/events and likely lower startup tool-schema cost unless it modifies prompts on events.
- Is AGENTS.md default loading core or configurable: core default behavior in `resource-loader.ts`; configurable per run with `--no-context-files`/`-nc` and resource-loader `noContextFiles` option.
- Are subagent extension/tool schemas a major part: likely yes. `pi-subagents` registers a `subagent` tool with a long action matrix and schema; child sessions may also register `structured_output`. This is a top suspect, but exact token count needs measurement using provider/debug serialization or a session export.
- How to measure without mutating state: use `--no-session` and disable combinations of resources/tools, or construct an SDK in-memory session and print `systemPrompt.length`, active tool names, and JSON serialized tool definition sizes. Avoid auth/log secrets.

## Start Here

Open `/home/li/.local/share/criomos/pi/package/src/core/system-prompt.ts` first. It shows exactly what Pi injects into the visible system prompt and separates visible prompt bloat from hidden tool-schema bloat.

## Safe next investigative commands/edits for later implementation phase

Commands (read-only/no session mutation):

- `pi --no-session --no-extensions --no-skills --no-context-files --no-tools --print "ping"` with provider usage shown, then add flags back one at a time.
- `pi --no-session --no-context-files --print "ping"`, then compare to default.
- `pi --no-session --no-extensions --print "ping"`, then compare to default to isolate extension tool schemas.
- Use a small Node/TS script importing Pi SDK with `SessionManager.inMemory()` to instantiate sessions and print:
  - `session.systemPrompt.length`
  - `session.getActiveToolNames()`
  - `JSON.stringify(session.getAllTools().map(({name,description,parameters})=>...)).length`
  No prompt to model required.
- Run `pi list` / `pi config` only for inspection if it does not rewrite settings; otherwise inspect `settings.json` as done here.

Candidate implementation edits for later (not performed):

- Add a built-in `pi doctor context`/`pi context-breakdown --dry-run` that reports visible system prompt chars/tokens, context-file sizes, skill metadata sizes, and tool schema sizes without sending a model request.
- Add per-package/tool contribution listing and a `--no-package <name>` or package resource disable UX if missing.
- Trim verbose extension tool descriptions/schemas, especially in `pi-subagents` and `pi-web-access`, or move usage guidance from tool descriptions to optional skills loaded on demand.
- Consider making `AGENTS.md` context-file loading explicit in startup UI with byte/token estimate and reminding users about `-nc`.

## Best next psyche question

When you compare Pi to plain Codex, are you comparing the number after Pi has already obeyed primary’s boot instruction and read `skills/skills.nota`, or immediately at the first assistant turn before any tool reads? That determines whether the main fix target is workspace boot reads or hidden extension tool schemas.

## Supervisor coordination

No supervisor contact used. Investigation was read-only except for the required output report at `/home/li/primary/context.md`.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings cite Pi core files, user settings, package manifests, and package extension sources with severity-ranked bloat causes."
    }
  ],
  "changedFiles": [
    "/home/li/primary/context.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read AGENTS.md and skills/skills.nota",
      "result": "passed",
      "summary": "Loaded required workspace boot files."
    },
    {
      "command": "grep/find/read targeted Pi source, user settings, and installed packages under allowed paths",
      "result": "passed",
      "summary": "Located context prompt construction, resource loading, context percentage calculation, package resources, and extension tool registrations."
    },
    {
      "command": "python3 read-only package/settings/file-size inspection",
      "result": "passed",
      "summary": "Counted relevant file sizes and package resource/tool registration counts without mutation."
    }
  ],
  "validationOutput": [
    "Report written to /home/li/primary/context.md. Read-only investigation; no source/config edits, commits, or pushes."
  ],
  "residualRisks": [
    "Exact provider-side token contribution of hidden tool schemas was inferred from active tool definitions, not measured by serialized API payload.",
    "Session logs were not inspected to avoid accidental secret exposure; prior-message contribution remains conditional."
  ],
  "noStagedFiles": true,
  "diffSummary": "Only required scout report file written.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "Top suspects: extension tool schemas (pi-subagents/pi-web-access) and mandatory skills.nota read before first subagent."
}
```
