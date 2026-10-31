Presentation.{ «The harness in the context» }

# The harness in the context

Written by the Psyche core Secondary. An account, not a proposal: nothing here is to land.

## What this is

Everything Claude Code 2.1.294 writes into a flow's context besides our prompt and our modules, mapped so each piece can be named as a module, kept, replaced or blacklisted per metaflow. Codex 0.158 follows briefly. Sources are weighed by origin and marked in the appendix: **T** seen in our transcripts as it arrived, **C** seen in this flow's own context, **P** seen in a probe run today, **B** seen in the binary's text only, **D** stated by the official docs only.

The count: 75 distinct Claude Code items, in four kinds. 19 are system-prompt sections (our `--system-prompt-file` already removes 16 of them). 12 are tool-and-listing texts. 31 are reminders the harness attaches to user turns. 13 are wrappers and markers around tool results, notifications and compaction. Codex adds 22 items of its own.

## The layers, from base to prompt

```
+------------------------------------------+
| identity line (cliPrefix)                |
+------------------------------------------+
   | is followed by
   v
+------------------------------------------+
| system prompt body: stock, or our bundle |
+------------------------------------------+
   | keeps after it
   v
+------------------------------------------+
| survivors: WebSearch mode hint, appends  |
+------------------------------------------+
   | is sent beside
   v
+------------------------------------------+
| tool definitions, loaded and deferred    |
+------------------------------------------+
   | come before
   v
+------------------------------------------+
| session-start reminders: context, env,   |
| model, attribution, listings, mode steer |
+------------------------------------------+
   | come before
   v
+------------------------------------------+
| the prompt we write                      |
+------------------------------------------+
   | is followed by
   v
+------------------------------------------+
| turn traffic: tool results, reminders,   |
| notifications, hook text                 |
+------------------------------------------+
   | is folded, at the threshold, into
   v
+------------------------------------------+
| a compaction summary                     |
+------------------------------------------+
```

Only the second layer is ours today. The Flow Nexus launches Claude main flows with `--system-prompt-file` (flow-nexus `herdr/launch.rs:918`), which replaces the stock body. Everything else still arrives. The Primary's own transcript shows it: the system prompt is the line "You are Claude Code, Anthropic's official CLI for Claude.", then our 16,685-character bundle, then a 423-character WebSearch hint we never wrote; beside it are 14 tool definitions, the Artifact tool's description alone being 20,093 characters.

In 2.1.294 most of what used to be system prompt moved out of it: the environment, date, git status, CLAUDE.md, model line and attribution arrive as reminders in the first user turn. Replacing the system prompt does not touch them.

## When each piece enters a turn

```
+------------------------------------------+
| session starts                           |
+------------------------------------------+
   | attaches, before the first prompt:
   | context, env, model, date, attribution,
   | skills, agents, deferred tools, mode
   v
+------------------------------------------+
| prompt arrives                           |
+------------------------------------------+
   | gains: hook context, total_tokens,
   | date change, edited-file notes
   v
+------------------------------------------+
| model call                               |
+------------------------------------------+
   | asks for
   v
+------------------------------------------+
| tool runs                                |
+------------------------------------------+
   | returns its result with: audience
   | note, truncation banner, persisted
   | output, re-read notice
   v
+------------------------------------------+
| before the next call                     |
+------------------------------------------+
   | gains: batching line, silent-turn line,
   | queued messages, task notifications,
   | total_tokens, elapsed time
   v
+------------------------------------------+
| model call again, until no tool is asked |
+------------------------------------------+
   | ends in
   v
+------------------------------------------+
| Stop hook, then idle                     |
+------------------------------------------+
```

The four mid-turn lines the living has met, as they arrived (T):

- silent_turn_reminder: "The user hasn't heard from you in a while — say in a few words what you're doing, then continue." In 203 transcripts. The binary's own default wording is different ("As you continue, keep them updated when there's something to tell"); the wording that reached us was served from Anthropic's side by a remote flag (`tengu_hushed_lark_text`), with `CLAUDE_CODE_SILENT_TURN_REMINDER_TEXT` as a local override.
- batching_reminder: "First privately list what you need next; then request every item that doesn't depend on another's result in this one response." In 117 transcripts, after tool results.
- bash_output_audience_note: "Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply." In 93 transcripts, after Bash results. Interactive sessions only: two `claude -p` probes today got none.
- date: "The date has changed. Today's date is now 2026-10-31. No need to announce the new date — the user's own clock shows it." In 91 transcripts, after midnight.

## What reaches each item

```
+------------------------------------------+
| harness text in the context              |
+------------------------------------------+
   | part is removed by
   v
+------------------------------------------+
| a documented flag, setting or env:       |
| body, git, CLAUDE.md, memory, skills,    |
| tools, MCP, attribution, compaction      |
+------------------------------------------+
   | part only by
   v
+------------------------------------------+
| an undocumented env override, untested:  |
| silent-turn, audience note, batching,    |
| total_tokens, task nudges, announcement  |
+------------------------------------------+
   | part only by
   v
+------------------------------------------+
| a blunt mode that takes much else:       |
| DISABLE_ATTACHMENTS, --bare              |
+------------------------------------------+
   | the rest by
   v
+------------------------------------------+
| nothing: identity line, notification and |
| message framing, interrupt marks, the    |
| compaction prompt, served wording        |
+------------------------------------------+
```

Switched off today by a documented switch (D, most also B): the stock body (`--system-prompt-file`, in use); git status and commit instructions (`includeGitInstructions: false` or `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`); CLAUDE.md (`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `claudeMdExcludes`); auto memory (already off here); each skill in the listing (`skillOverrides`, `disable-model-invocation`); built-in agents (`CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS`); each tool with its description (`--tools`, `--disallowedTools`, per-tool env); MCP text (`--strict-mcp-config`); the commit and PR trailers (`attribution`); the version fingerprint block (`CLAUDE_CODE_ATTRIBUTION_HEADER=0`); compaction (`DISABLE_AUTO_COMPACT=1`); hook text (our hooks).

Present in the binary as an env override but undocumented and not yet tested: `CLAUDE_CODE_SILENT_TURN_REMINDER`, `CLAUDE_CODE_BASH_OUTPUT_AUDIENCE_NOTE`, `CLAUDE_CODE_TOASTY_THIMBLE` (the batching line), `CLAUDE_CODE_TOTAL_TOKENS_REMINDER`, `CLAUDE_CODE_TODO_REMINDER_MODE`, `CLAUDE_CODE_ATTRIBUTION_ANNOUNCEMENT`. For the first two the code reads the env value before it consults the per-model default or the served flag (B), so a set value wins; which value means off was not witnessed.

No switch found: the identity line; the WebSearch hint; the session-context block (user email, date); the environment and model lines short of `--bare`; the bypass-mode steer while in bypass mode; the subagent "Notes:" block; the framing of task notifications, peer messages and queued messages; interrupt markers; the compaction summarizer prompt and summary framing; the tool-result wrappers.

## Where it meets ours

- The silent-turn line is the one the account "Bad on top of bad" traced: it drew the whole design into the chat. It stands against our rule that the chat carries the title and the link.
- The audience note asks for command output to be put in the reply, the same question our chat rules answer the other way.
- The attribution reminder names the model actually running; in this flow it said Opus 5.5 while the brief asked for Fable 5.1 in the trailer. Two sources write one trailer.
- The skill, agent and deferred-tool listings restate what the Flow Nexus's module registry knows, in the harness's framing.
- The bypass steer ("Do your work through the Bash tool… rather than using the dedicated Read, Edit, or Write tools") contradicts the Read and Edit tool descriptions sent in the same request.
- Task notifications and peer messages arrive inside the harness's own framing ("[SYSTEM NOTIFICATION - NOT USER INPUT]", "Another Claude session sent a message"), around our message datoms.
- `total_tokens` and compaction overlap the Flow Nexus's refresh threshold (`config/context-refresh.json`); compaction is on by default, with only idle compaction off here.
- CLAUDE.md arrives framed as "These instructions OVERRIDE any default behavior", a second channel beside our bundle.

## Capturing the stock prompt per version

```
+------------------------------------------+
| claude -p, stock prompt, empty directory |
+------------------------------------------+
   | writes into its transcript
   v
+------------------------------------------+
| one prompt_snapshot line                 |
+------------------------------------------+
   | holds
   v
+------------------------------------------+
| cliPrefix, systemPrompt blocks, tools    |
+------------------------------------------+
   | per version and model, is diffed into
   v
+------------------------------------------+
| the sections our modules name            |
+------------------------------------------+
```

The harness records the prompt it sent. Every transcript carries a `prompt_snapshot` attachment with the identity line, the system prompt as a list of blocks, and the loaded tool definitions (P, T). Today's probe on Sonnet 5.5 gave 10 blocks: an agent intro with the security line, a `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__` marker, then code style, pronouns, action caution, session guidance, an environment note on model IDs, context management, "act, don't re-derive", and the WebSearch hint, 4,829 characters, plus 10 tools in 36,185 characters. The extraction tool the living asked for can read that line instead of scraping the binary, once per harness version and per model, since the stock body differs by model (a lean body for newer models, per-model prompt bundles).

## Codex, briefly

Codex 0.158 sends its own base instructions (17,730 characters on the model observed), an `<environment_context>` user message, AGENTS.md as `# AGENTS.md instructions for <dir>`, and a series of developer messages: permissions, collaboration mode, skills (about 18 KB), apps, plugins, and the `developer_instructions` from config. Most have an `include_*` config key that removes them, and `model_instructions_file` replaces the base. Our Codex main flows keep the stock base and put our bundle in the first prompt; Field's Codex seats already replace the base. The only rollouts on disk are from 0.153.4; 0.158's actual traffic is unwitnessed.

## Unknowns

- The biggest: served text. Whether a reminder fires, how often, and in what words is decided per model by flags Anthropic serves at run time, so the context can change with no new harness version. A diff of versions cannot see it; only transcripts can, through the rendered text of each attachment.
- Which env values switch the undocumented overrides off: read in code, not tried.
- Whether any CLI path removes the identity line (`skipSystemPromptPrefix` exists inside; no flag reaches it was found).
- What gates the WebSearch hint that survives a custom prompt.
- Codex 0.158's per-turn injections, and the bodies of `current_time_reminder` and the multi-agent notices.

## Appendix: Claude Code items

### System prompt

| Item | Excerpt | Enters | Switch | Seen |
|---|---|---|---|---|
| identity line (cliPrefix) | "You are Claude Code, Anthropic's official CLI for Claude." / "You are a Claude agent, built on Anthropic's Claude Agent SDK." | first system block | none found; chosen by interactive vs `-p` | T P C B |
| intro and security line | "You are an agent working with the user toward their goals…" "IMPORTANT: Assist with authorized security testing…" | body | `--system-prompt` | P B |
| dynamic boundary | `__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__` | body | `--system-prompt` | P |
| system (full body) | "# System… Tools are executed in a user-selected permission mode…" | body, full prompt only | `--system-prompt`; `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` | B |
| doing tasks | "# Doing tasks… Don't add features… beyond what the task requires" | body | `--system-prompt`; an output style without keep-coding-instructions | B |
| code style | "Write code that reads like the surrounding code…" | body | `--system-prompt` | P |
| executing actions with care | "Carefully consider the reversibility and blast radius…" | body | `--system-prompt` | B |
| using your tools | "Prefer dedicated tools over Bash…" | body | `--system-prompt` | B |
| tone and style | "Only use emojis if the user explicitly requests it…" | body | `--system-prompt` | B |
| communicating / turn updates | "Before you start, say in a line what you're about to do…" | body | `--system-prompt`; served `turn_updates` | B |
| pronouns | "When you use a pronoun for someone… use they/them." | body | `--system-prompt` | P |
| action caution | "For actions that are hard to reverse or outward-facing, confirm first…" | body | `--system-prompt` | P |
| session guidance | "# Session-specific guidance… When the user types `/<skill-name>`…" | body | `--system-prompt` | P |
| environment note | "# Environment… The most recent Claude models are the Claude 5 family…" | body | `--system-prompt` | P |
| context management | "# Context management… some or all of the current context is summarized" | body | `--system-prompt` | P |
| act, don't re-derive | "When you have enough information to act, act…" | body | `--system-prompt`; `CLAUDE_CODE_ACT_DONT_REDERIVE` | P B |
| model-specific sections | Fable identity, delivering work, corrections, background session | body | `--system-prompt`; per-model gates | B |
| WebSearch mode hint | "WebSearch takes a `mode`. Use \"standard\" by default…" | after the body, survives a custom prompt | none found | T P |
| subagent Notes block | "Agent threads always have their cwd reset… Do NOT Write report/summary/findings/analysis .md files" | subagent system prompt | none found | C B |

### Tools and listings

| Item | Excerpt | Enters | Switch | Seen |
|---|---|---|---|---|
| tool definitions | Agent 3,047 chars, Artifact 20,093, ScheduleWakeup 3,148, SendFeedback 3,467… | request tools | `--tools`, `--disallowedTools`, per-tool env | T P |
| git commit and PR instructions | in the Bash tool description | tools | `includeGitInstructions: false` | B D |
| attribution lines in Bash description | used when the announcement is off | tools | `attribution` | B |
| skill_listing | "The following skills are available for use with the Skill tool:" | first turn reminder | `skillOverrides`, `disable-model-invocation`, `--disable-slash-commands` | T C |
| dynamic_skill | "New skills discovered in {dir}…" | mid-session | none found | B |
| agent_listing_delta | "Available agent types for the Agent tool:" | first turn, on change | built-in agent env vars; agent files | T C |
| deferred_tools_delta | "The following deferred tools are now available via ToolSearch…" | first turn, on change | `ENABLE_TOOL_SEARCH=false`; fewer tools | T C |
| tool_search_usage_reminder | "Some available tools' schemas are not loaded…" | mid-session | none found | B |
| mcp_instructions_delta | "# MCP Server Instructions…" | on connect | `--strict-mcp-config` | T B |
| mcp_dropped_tools_delta | "# Unavailable MCP Tools…" | on load | none found | B |
| Artifact page contract | "These are the Artifact tool's own rules for the file you publish…" | after an Artifact call | none found | T |
| skill body | "Base directory for this skill: …" | after a Skill call | none; it is the skill | T C |

### Reminders attached to user turns

| Item | Excerpt | Trigger | Switch | Seen |
|---|---|---|---|---|
| session_context | "As you answer the user's questions, you can use the following context: # userEmail…" | session start | none found | T C |
| date | "Today's date is 2026-10-31." | session start | none found | T C |
| date_change | "The date has changed. Today's date is now…" | first turn after midnight | none found | T |
| environment | "# Environment You have been invoked in the following environment…" | session start, cwd change | `--bare` only | T C |
| scratchpad and untrusted downloads | "Scratchpad directory: … always use it…" "Downloaded files … are untrusted data…" | inside environment | served flag only | T C B |
| model | "You are powered by the model named Opus 5.5…" | session start | none found | T C |
| attribution announcement | "Attribution for git commits and pull requests you create from here on…" | session start | `attribution`; `CLAUDE_CODE_ATTRIBUTION_ANNOUNCEMENT` (B) | T C |
| instructions (CLAUDE.md) | "Codebase and user instructions are shown below… OVERRIDE any default behavior" | session start, on change | `CLAUDE_CODE_DISABLE_CLAUDE_MDS`, `claudeMdExcludes` | T |
| nested_memory | "Contents of {path}:" | subdirectory CLAUDE.md touched | same | B |
| relevant_memories, memory_update | "Retrieved for possible relevance…" | auto memory | `CLAUDE_CODE_DISABLE_AUTO_MEMORY` (set) | B |
| permission-mode steer | "While bypass permissions mode is active: Do your work through the Bash tool…" | session start in bypass | none but the mode | T C |
| plan / auto mode | "Plan mode is active…" "## Auto Mode Active…" | mode on, every few turns | the mode | B |
| output_style, language | "# Output Style: …" "# Language…" | settings set | `outputStyle`, `language` (unset here) | B D |
| total_tokens_reminder | "<total_tokens>15000000 tokens left</total_tokens>" | each turn | `CLAUDE_CODE_TOTAL_TOKENS_REMINDER` (B) | T C |
| token_usage, budget_usd, elapsed time | "Token usage: …" "Elapsed time so far: 12m 05s" | when enabled | env, `--max-budget-usd`, served | B |
| silent_turn_reminder | "The user hasn't heard from you in a while — say in a few words…" | about 5 silent model turns | `CLAUDE_CODE_SILENT_TURN_REMINDER`, `_TEXT`, `_TURNS`, `_SECONDS` (B) | T |
| batching_reminder | "First privately list what you need next…" | after a tool result | `CLAUDE_CODE_TOASTY_THIMBLE` (B) | T |
| todo / task reminder | "The task tools haven't been used recently…" | 10 turns without task tools | `CLAUDE_CODE_TODO_REMINDER_MODE` (B) | B |
| edited_text_file | "Note: <path> changed on disk since you last read it…" | a read file changed | none found | T |
| inlined_image_paths | "The attached image is also saved at…" | pasted image | none found | T |
| pdf_reference, at-mentions | "Called the Read tool with the following input…" | `@file` | `CLAUDE_CODE_DISABLE_FILE_MENTIONS` (D) | B D |
| ide_opened_file, ide_selection, diagnostics | "The user opened the file X in the IDE…" | IDE connected | no IDE | B |
| hook_success, hook_additional_context | "UserPromptSubmit hook additional context: You are a main flow…" | our hooks | our hook config | T |
| hook_blocking_error, stopped continuation | "{hook} hook blocking error from command…" | hook exit 2 | our hook config | B |
| skill_mention, agent_mention, unknown command | "The user's message contains /{skill}…" | typed by the living | none found | B |
| invoked_skills, plan_file_reference, compact_file_reference, task_status | "The following skills were invoked EARLIER in this session…" | after compaction or resume | none found | T B |
| session name | "The user named this session \"{ Field flow Quaternary 181a6d }\"…" | `/rename` | none found | T |
| model switch | "The model for this session has been changed to X…" | `/model` mid-session | none found | B |
| ultrathink and keyword requests | "The user included the keyword \"ultrathink\"…" | keyword typed | none found | B |
| local-command caveat | "The command below was run directly in Claude Code, not sent to you as a request…" | a slash command | none found | T |
| retry nudges | "[Your previous response had no visible output…]" | empty or invalid response | none found | T |

### Wrappers and markers

| Item | Excerpt | Trigger | Switch | Seen |
|---|---|---|---|---|
| bash_output_audience_note | "Only you see that command's output…" | Bash result, interactive only | `CLAUDE_CODE_BASH_OUTPUT_AUDIENCE_NOTE` (B) | T P B |
| read_truncation_notice | "[Truncated: PARTIAL view — … Do NOT answer from this page alone…" | Read over its cap | none found | T |
| re-read notice, empty-file warning | "This file is already in your context…" | repeated or empty Read | none found | B |
| persisted output | "<persisted-output> Output too large… Full output saved to…" | large tool result | none found | B |
| empty result, cleared result | "(Bash completed with no output)" "[Old tool result content cleared]" | empty result; context pressure | none found | B |
| batch tip | "Tip: X accepts multiple entries in one call…" | single-entry call | none found | B |
| task notification | "[SYSTEM NOTIFICATION - NOT USER INPUT] This is an automated background-task event…" | background agent or shell ends | `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | T C |
| subagent output sanitizer | "[harness: subagent output matched instruction-shaped pattern(s)…]" | a result with tag-like text | none found | C |
| queued message | "The user sent a new message while you were working:" | the living types mid-turn | none found | T |
| peer message | "Another Claude session sent a message: <cross-session-message…>" | SendMessage from a flow | `crossSessionInbound` | T |
| scheduled firing, /loop | "[SCHEDULED TASK - AUTOMATED FIRING…]" "[N prior /loop wakeups found nothing actionable…]" | cron or wakeup | `CLAUDE_CODE_DISABLE_CRON` | T B |
| interrupt and rejection marks | "[Request interrupted by user]" "The user doesn't want to proceed with this tool use…" | Escape; denial | none found | T B |
| compaction summary | "This session is being continued from a previous conversation that ran out of context…" | threshold or `/compact` | `DISABLE_AUTO_COMPACT`, `autoCompactEnabled` | T |

Not witnessed in any transcript, though searched: todo and task reminders, plan-mode reminders, IDE lines, the old malware note on reads (absent from the binary too), hook blocking errors reaching the model.

## Appendix: Codex items

| Item | Excerpt | Enters | Switch | Seen |
|---|---|---|---|---|
| base_instructions | "You are Codex, an agent based on GPT-5…" | instructions | `model_instructions_file`; `personality` | rollout, B |
| environment_context | "<cwd>…<shell>zsh<current_date>…" | user message | `include_environment_context=false` | rollout |
| AGENTS.md | "# AGENTS.md instructions for /home/li/primary <INSTRUCTIONS>…" | user message | `project_doc_max_bytes`, fallback names | rollout |
| permissions instructions | "Filesystem sandboxing defines which files can be read or written…" | developer | `include_permissions_instructions=false` | rollout |
| collaboration_mode | "# Collaboration Mode: Default…" | developer | `include_collaboration_mode_instructions=false` | rollout |
| skills_instructions | "## Skills A skill is a set of local instructions…" | developer | `include_skills_usage_instructions` (B) | rollout |
| apps_instructions | "## Apps (Connectors)…" | developer | `include_apps_instructions=false` | rollout |
| plugins_instructions | "## Plugins A plugin is a local bundle…" | developer | `include_plugin_usage_instructions` (B) | rollout |
| developer_instructions | our de-duplication paragraph in config.toml | developer | config | config |
| launcher developer message | "This session is a disposable recipient seat…" | developer | ours | rollout |
| turn_aborted | "The user interrupted the previous turn on purpose…" | user | none found | rollout |
| multi-agent notices | `<subagent_notification>`, `<multi_agent_mode>` | inferred developer | `features.multi_agent` | B |
| current_time_reminder | tag only | inferred mid-turn | feature key | B |
| context_window_guidance | "You have unknown tokens left in this context window." | developer | feature flags | B |
| model_switch, token_budget, persistent_mode, git_attribution | tags | developer | feature flags | B |
| compaction prompt | "You are performing a CONTEXT CHECKPOINT COMPACTION…" | user, to the summarizer | `compact_prompt`, `experimental_compact_prompt_file` | B |
| compaction prefix | "Another language model started to solve this problem…" | user | none found | B |
| review prompt | "Output all findings that the original author would fix…" | reviewer thread | `review_model` | B |
| guardian classifier | "Do not infer permission from missing evidence." | separate call | `approvals_reviewer` (user here: off) | B |
| tool descriptions | apply_patch "*** Begin Patch", update_plan, exec_command | tools | `[tools]`, feature flags | B |
| hook prompts | `hook_prompt`, `additionalContext` | appended | `features.hooks` | B |
| memories | "# Raw Memories…" | inferred | `[memories]` | B |

The `codex` on PATH is a wrapper that sets `CODEX_HOME=/home/li/.codex-next` and talks to a running app server, so flows read `~/.codex-next/config.toml`.

## Appendix: sources

| Source | Where |
|---|---|
| binary text | strings of `/nix/store/4slw0czfvd70df8a2c7077aqdilf0hgy-claude-code-2.1.294/bin/.claude-wrapped` |
| transcripts | 445 files under `~/.claude/projects/-home-li-primary/` |
| probe | two `claude -p` runs today in an empty scratch directory |
| docs | code.claude.com/docs: cli-reference, env-vars, settings-reference, hooks, memory, skills, sub-agents, mcp, context-window, agent-sdk/modifying-system-prompts |
| our launchers | flow-nexus `herdr/launch.rs`, `composition.rs`; `tools/primary-committer/codex-birth.mjs`, `seat-process.mjs` |
| Codex | strings of codex 0.158.0-alpha.9; rollouts 0.153.4 in `~/.codex/archived_sessions` |
