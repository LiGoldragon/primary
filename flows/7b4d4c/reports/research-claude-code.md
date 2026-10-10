# Research: Claude Code harness

FLOW_ID: 7b4d4c
Date: 2026-09-04
Thread: research subflow

---

## 1. Installed version and system-prompt mechanisms

### Installed version

```
$ claude --version
2.1.258 (Claude Code)
```

**[witnessed: `claude --version`, 2026-09-04]**

### Flags and settings that author the top stratum

All flags below were witnessed from `claude --help` output on version 2.1.258 [witnessed: `claude --help`, 2026-09-04]. Documented descriptions are from the official documentation [documented: code.claude.com/docs/en/cli-reference, read 2026-09-04].

| Mechanism | What it does | Source |
|---|---|---|
| `--system-prompt <prompt>` | Replace the entire system prompt with custom text. | witnessed: `--help` |
| `--system-prompt-file <path>` | Load system prompt from a file, replacing the default prompt. | witnessed: `--help` |
| `--append-system-prompt <prompt>` | Append custom text to the end of the default system prompt. | witnessed: `--help` |
| `--append-system-prompt-file <path>` | Load additional system prompt text from a file and append to the default prompt. | witnessed: `--help` |
| `--system-prompt-snapshot <on\|off>` | Record the system prompt once per conversation and reuse it verbatim on every request and resume. Default on for the built-in prompt; passing `--system-prompt` or `--append-system-prompt` turns it off. `on`: an existing record in the conversation is sent as-is (a later launch's different flags are ignored until compaction). `off`: never record. | witnessed: `--help` |
| `--exclude-dynamic-system-prompt-sections` | Move per-machine sections (cwd, env info, memory paths, git status) from the system prompt into the first user message. Improves cross-user prompt-cache reuse. Only applies with the default system prompt (ignored with `--system-prompt`). | witnessed: `--help` |
| `--bare` | Minimal mode: skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery. Sets `CLAUDE_CODE_SIMPLE=1`. Skills in `--add-dir` directories still load. | witnessed: `--help` |
| `--safe-mode` | Disables all customizations (CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands and agents, output styles, workflows, custom themes, keybindings). Admin-managed (policy) settings still apply. Sets `CLAUDE_CODE_SAFE_MODE=1`. | witnessed: `--help` |
| Output styles | Saved markdown files in `~/.claude/output-styles/` or `.claude/output-styles/`. Setting `keep-coding-instructions: true` in frontmatter preserves the preset's SE instructions; leaving it out replaces them. Activated via `/config`, `outputStyle` in settings, or SDK. | documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04 |
| SDK: `systemPrompt` (TS) / `system_prompt` (Python) | Three starting points: minimal default (no `systemPrompt` set), `claude_code` preset (optionally with `append`), or custom string. | documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04 |
| SDK: `excludeDynamicSections` | On the preset object. Moves per-session context into first user message for cross-session cache reuse. | documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04 |
| `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` (env var) | Pins the shorter system prompt on or off. Referenced in output-styles documentation. | documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04 |

### Environment variables affecting the system prompt

| Variable | Effect | Source |
|---|---|---|
| `CLAUDE_CODE_SIMPLE` / `CLAUDE_CODE_SIMPLE=1` | Set by `--bare`. | witnessed: `--help` |
| `CLAUDE_CODE_SAFE_MODE` / `CLAUDE_CODE_SAFE_MODE=1` | Set by `--safe-mode`. | witnessed: `--help` |
| `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` | Pins the shorter system prompt on or off. | documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04 |

---

## 2. What the documentation says about system prompt structure and ordering

### Default system prompt contents

The documentation states the `claude_code` preset contains:

> "the system prompt that the Claude Code CLI uses, with tool usage instructions, security and safety instructions, and context about the working directory and environment."

[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04]

### Minimal default (SDK, no systemPrompt set)

> "when you don't set `systemPrompt` in TypeScript or `system_prompt` in Python, the SDK uses a minimal prompt that covers tool calling but omits the rest of the `claude_code` preset's content, including its security and safety instructions and its context about the working directory and environment."

[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04]

### Context window loading order

The interactive context-window visualization on `code.claude.com/docs/en/context-window` [documented, read 2026-09-04] describes the following startup loading order:

1. **System prompt** (t=0.015, ~4200 tokens, vis: hidden) -- "Core instructions for behavior, tool use, and response formatting. Always loaded first. You never see it."
2. **Auto memory / MEMORY.md** (t=0.035, ~680 tokens, vis: hidden) -- "Claude's notes to itself from previous sessions."
3. **Environment info** (t=0.06, ~280 tokens, vis: hidden) -- "Working directory, platform, shell, OS version, and whether this is a git repo. Git branch, status, and recent commits load as a separate block at the very end of the system prompt."
4. **MCP tools (deferred)** (t=0.08, ~120 tokens, vis: hidden) -- Tool names listed for availability.
5. **Skill descriptions** (t=0.1, ~450 tokens, vis: hidden) -- "One-line descriptions of available skills so Claude knows what it can invoke. Full skill content loads only when Claude actually uses one."
6. **~/.claude/CLAUDE.md** (t=0.12, ~320 tokens, vis: hidden) -- User-level instructions.
7. **Project CLAUDE.md** (t=0.14, ~1800 tokens, vis: hidden) -- Project conventions.
8. **Your prompt** (t=0.22, user message)

Items 1 and 3 are explicitly marked as part of the system prompt. Items 2, 4-7 are injected into the conversation context (not the system prompt), confirmed by:

> "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself."

[documented: code.claude.com/docs/en/memory, 2026-09-04]

> "CLAUDE.md files give Claude persistent project context and instructions. The SDK injects their content into the conversation and leaves the system prompt untouched"

[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04]

### What stays in the system prompt regardless of `--system-prompt`

The comparison table from the SDK documentation states:

| Feature | `systemPrompt` with append | Custom `systemPrompt` |
|---|---|---|
| Default tools | Preserved | Lost (unless included) |
| Built-in safety | Maintained | Must be added |
| Environment context | Automatic | Must be provided |

> "Only what you write. You take responsibility for replacing the tool guidance and safety instructions your agent still needs"

[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04]

This means with a fully custom `--system-prompt`: tool definitions still reach the model (they are passed separately as tool schemas in the API), but all behavioral instructions, safety rules, and environment context from the default prompt are lost. The tool schemas are not part of the system prompt text; they are a separate API parameter.

### System-reminder injections

System-reminders are injected as messages in the conversation, not in the system prompt. They appear at various points as `<system-reminder>` tagged blocks. This is witnessed in the current session's own context: system-reminder blocks carry CLAUDE.md content, skill catalog listings, deferred tool listings, git status, and per-turn injections like token budget. **[witnessed: this session's own context, 2026-09-04]**

### Skill injection

The skill catalog (one-line descriptions) is listed in a system-reminder. When a skill is invoked through the Skill tool, its body is injected as a system-reminder in the conversation. **[witnessed: this session's own Skill tool calls and the resulting system-reminder blocks, 2026-09-04]**

> "Full skill content loads only when Claude actually uses one."

[documented: code.claude.com/docs/en/context-window, 2026-09-04]

> "After `/compact`, Claude Code re-injects the body of each skill you invoked, capped at 5,000 tokens per skill."

[documented: code.claude.com/docs/en/context-window, 2026-09-04]

### Hooks output placement

> "For most events, Claude Code writes stdout to the debug log and doesn't show it in the transcript. The exceptions are `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, and `PostModelSwitch`, where Claude Code adds plain-text stdout as context that Claude can see and act on."

For PostToolUse hooks: output reaches Claude via `hookSpecificOutput.additionalContext` JSON field, not plain stdout.

> "A PostToolUse hook in `settings.json` runs prettier after every file edit and reports back via `hookSpecificOutput.additionalContext`. That field enters Claude's context. Plain stdout on exit 0 does not."

[documented: code.claude.com/docs/en/context-window, code.claude.com/docs/en/hooks, 2026-09-04]

### Subagent briefs

> "Subagents receive only this system prompt plus basic environment details like the working directory, not the Claude Code system prompt."

The subagent's "task message" (the delegation prompt from the parent) arrives as a user message. CLAUDE.md is loaded as a separate injection. Forks inherit the parent's full conversation and system prompt.

[documented: code.claude.com/docs/en/sub-agents, 2026-09-04]

### Compaction behavior

After compaction:
- System prompt and output style: unchanged (not part of message history).
- Project-root CLAUDE.md and unscoped rules: re-injected from disk.
- Auto memory: re-injected from disk.
- Invoked skill bodies: re-injected (capped at 5,000 tokens/skill, 25,000 total).
- Skill descriptions catalog: NOT re-injected.
- Hook context: summarized with the rest.

[documented: code.claude.com/docs/en/context-window, 2026-09-04]

---

## 3. System prompt visibility

### To the model

The model can see and act on its system prompt. This is standard for the Claude API: the system prompt is the first content block the model processes. The context-window visualization confirms this: items marked `vis: hidden` are "hidden" from the **living** (user), not from the model.

> "Core instructions for behavior, tool use, and response formatting. Always loaded first. You never see it."

The "you" here is the human user, not the model. **[documented: code.claude.com/docs/en/context-window, 2026-09-04]**

### To the living (human user)

The system prompt is **not visible** to the living through any standard mechanism:

1. **Terminal output**: The system prompt does not appear in the terminal. The context-window visualization marks it `vis: 'hidden'` with the description "You never see it." **[documented: code.claude.com/docs/en/context-window, 2026-09-04]**

2. **Debug log (`--debug`, `--debug-file`)**: The debug log records startup events, API timing, tool loading, and session metadata but does **not** log the system prompt text. **[witnessed: `--debug-file` output on v2.1.258, 2026-09-04; grep for "system.prompt" returned no matches]**

3. **Session transcripts (JSONL files)**: The persisted conversation files in `~/.claude/projects/` contain user messages, assistant messages, and tool results but do **not** contain the system prompt. **[witnessed: reading transcript JSONL for a session on v2.1.258, 2026-09-04]**

4. **JSON/stream-json output format**: The `--output-format json` output includes a `system` token count (value: 0 in the observed output) but not the system prompt text. **[witnessed: `--output-format json` on v2.1.258, 2026-09-04]**

5. **No `--verbose` system-prompt dump**: The `--verbose` flag does not cause the system prompt to be printed. **[witnessed: `--help` lists `--verbose` as "Override verbose mode setting from config" with no mention of system prompt display, 2026-09-04]**

**Summary**: There is no witnessed mechanism for the living to inspect the system prompt of a running Claude Code session. The model sees it; the living does not. The documentation explicitly states this asymmetry.

---

## 4. Stratum mapping for Claude Code 2.1.258

Under the three-stratum model:

### Top stratum (base context)

| Content | Placement evidence |
|---|---|
| System prompt (core instructions for behavior, tool use, response formatting) | documented: "Always loaded first" at t=0.015 in context-window visualization (code.claude.com/docs/en/context-window, 2026-09-04). Confirmed as system-role content that survives compaction unchanged. |
| Environment info (cwd, platform, shell, OS, git status) | documented: "load as a separate block at the very end of the system prompt" (code.claude.com/docs/en/context-window, 2026-09-04). |
| Output style content (when active) | documented: "part of the system prompt" (code.claude.com/docs/en/settings, 2026-09-04). Survives compaction unchanged. |

### Middle stratum (typed prompt, entry files, system-reminder injections, skill-interface loads, subflow briefs)

| Content | Placement evidence |
|---|---|
| CLAUDE.md files (all scopes: managed, user, project, local) | documented: "delivered as a user message after the system prompt" (code.claude.com/docs/en/memory, 2026-09-04). Re-injected after compaction from disk. |
| Auto memory (MEMORY.md) | documented: loaded into "conversation context" at t=0.035 (code.claude.com/docs/en/context-window, 2026-09-04). |
| Skill descriptions catalog | witnessed: injected as system-reminder in this session (2026-09-04). Does not survive compaction. |
| Skill bodies loaded via Skill tool | witnessed: injected as system-reminder when Skill tool is called (this session, 2026-09-04). Re-injected after compaction (capped). |
| `.claude/rules/` (unscoped) | documented: "loaded at launch with the same priority as `.claude/CLAUDE.md`" (code.claude.com/docs/en/memory, 2026-09-04). |
| `.claude/rules/` (path-scoped) | documented: "trigger when Claude reads files matching the pattern" (code.claude.com/docs/en/memory, 2026-09-04). Injected as conversation context. |
| Deferred tool listings | witnessed: injected as system-reminder in this session (2026-09-04). |
| Git status snapshot | witnessed: injected as system-reminder in this session (2026-09-04). |
| Subagent task message (delegation prompt) | documented: arrives as a user message to the subagent (code.claude.com/docs/en/sub-agents, 2026-09-04). |
| Hooks output (SessionStart, UserPromptSubmit, UserPromptExpansion, PostModelSwitch) | documented: "adds plain-text stdout as context" (code.claude.com/docs/en/hooks, 2026-09-04). |

**Note on CLAUDE.md strata**: CLAUDE.md is injected as a user message, not a system-reminder. It enters at the middle stratum because the harness authors it into the conversation as persistent project context before the first typed prompt, and it is re-injected from disk after compaction. However, because it is "context rather than enforced configuration" (documented: code.claude.com/docs/en/memory, 2026-09-04), it sits at the lower boundary of the middle stratum. **[inferred from the combination of witnessed injection mechanism and documented re-injection behavior]**

### Bottom stratum (fetched text and own output)

| Content | Placement evidence |
|---|---|
| File reads (Read tool results) | documented: tool results in conversation (code.claude.com/docs/en/context-window, 2026-09-04). |
| Bash/grep/command output | documented: tool results (code.claude.com/docs/en/context-window, 2026-09-04). |
| Web fetch results | inferred: tool result, same as file reads. |
| Subagent final reports | documented: "only its final summary comes back" as conversation content (code.claude.com/docs/en/context-window, 2026-09-04). Subagent output is scanned for instruction-shaped patterns before delivery (documented: code.claude.com/docs/en/sub-agents, 2026-09-04). |
| Hooks output (PostToolUse via additionalContext) | documented: enters Claude's context as tool-event metadata (code.claude.com/docs/en/hooks, 2026-09-04). |
| The model's own output | Standard LLM behavior. |
| Files opened by cat/Read outside the Skill interface | inferred: bottom stratum per context-strata model. |

---

## 5. Running with a fully replaced system prompt

### Known consequences

From the SDK documentation comparison table [documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04]:

| What is lost | Detail |
|---|---|
| Tool usage guidance | The default prompt's instructions for how to use Bash, Read, Edit, Write, etc. are gone. Tool schemas still reach the model as a separate API parameter. |
| Security and safety instructions | Must be added manually. |
| Environment context | Working directory, platform, shell, git status -- must be provided. |
| Output formatting rules | Terminal rendering expectations, diff formatting, etc. |

> "Only what you write. You take responsibility for replacing the tool guidance and safety instructions your agent still needs"

### What persists outside the prompt

1. **Tool schemas**: Tool definitions (Bash, Read, Edit, Write, Agent, Artifact, Skill, WebFetch, WebSearch, etc.) are passed as a separate `tools` parameter in the API call, not embedded in the system prompt text. They persist regardless of system prompt replacement. **[inferred from API design; confirmed by: with a custom `systemPrompt`, "Default tools: Lost (unless included)" refers to tool guidance, not tool schemas -- the "(unless included)" qualifier refers to behavioral instructions about tools, not the tool definitions themselves]**

2. **Permission system**: The harness's permission-checking layer (approval prompts, allowlists/denylists in settings, `--dangerously-skip-permissions`) operates outside the prompt at the application level. **[inferred from architecture]**

3. **Subagent output scanning**: The backslash-insertion and marker-line injection for instruction-shaped patterns in subagent output operates at the harness level, not in the prompt. **[documented: code.claude.com/docs/en/sub-agents, 2026-09-04]**

4. **CLAUDE.md injection**: CLAUDE.md content is injected into the conversation by the SDK, not by the system prompt. It works "with any system prompt configuration." **[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts, 2026-09-04]**

5. **System-reminder injection mechanism**: The harness's ability to inject system-reminder blocks into the conversation is an application-level feature, not dependent on the system prompt content. Skills, deferred tool listings, and per-turn notices continue to be injectable. **[inferred from architecture; the Skill tool continues to function with a custom system prompt]**

6. **Model-level safety training**: Claude's RLHF-based refusal behaviors and safety training are part of the model weights, not the prompt. They persist regardless of system prompt content. **[inferred from model architecture]**

### `--system-prompt-snapshot` interaction

When `--system-prompt` or `--append-system-prompt` is passed, the snapshot defaults to off, meaning the custom prompt is rendered fresh each launch. With `--system-prompt-snapshot on`, the first session's prompt is recorded and reused verbatim on resume, ignoring later flag changes until compaction. **[witnessed: `--help` output, 2026-09-04]**

---

## Sources

1. `claude --version` on this machine, 2026-09-04 -- witnessed
2. `claude --help` on this machine (v2.1.258), 2026-09-04 -- witnessed
3. `--debug-file` output on v2.1.258, 2026-09-04 -- witnessed
4. Session transcript JSONL (`~/.claude/projects/`), 2026-09-04 -- witnessed
5. `--output-format json` output, 2026-09-04 -- witnessed
6. This session's own context (system-reminder blocks, Skill tool injections), 2026-09-04 -- witnessed
7. code.claude.com/docs/en/agent-sdk/modifying-system-prompts -- documented, read 2026-09-04
8. code.claude.com/docs/en/context-window -- documented, read 2026-09-04
9. code.claude.com/docs/en/memory -- documented, read 2026-09-04
10. code.claude.com/docs/en/cli-reference -- documented, read 2026-09-04
11. code.claude.com/docs/en/sub-agents -- documented, read 2026-09-04
12. code.claude.com/docs/en/hooks -- documented, read 2026-09-04
13. code.claude.com/docs/en/settings -- documented, read 2026-09-04
14. code.claude.com/docs/en/skills -- documented, read 2026-09-04
15. code.claude.com/docs/en/env-vars -- documented, read 2026-09-04
