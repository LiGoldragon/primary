# What fills the Psyche core Primary's context

Evidence only. Every figure below has its source next to it. Untested harness switches are marked untested.

## 1. The context by origin

Sources: `a78e9a30-….jsonl` (current) and `1add4b….jsonl` (predecessor), main chain only. Tokens are estimated as characters / 4. Script: `scratchpad/ctx.py` in session a78e9a's scratchpad.

The transcript holds about 98k of a78e9a's context. The last API call billed 181,724 input tokens. The gap of about 83k is the harness base prompt and the tool definitions, which no transcript entry records. For 1add4b the figures are 79k held against 139,342 billed, a gap of about 60k.

| origin | a78e9a count | a78e9a tokens | share of billed 181.7k | 1add4b tokens |
|---|---|---|---|---|
| harness base prompt + tool definitions (the gap; inferred) | — | ~83,400 | 45.9% | ~60,300 |
| startup prompt (first message + system-prompt snapshot) | 2 | 28,691 | 15.8% | 28,146 |
| Primary's tool calls (tool_use inputs) | 81 | 14,196 | 7.8% | 9,494 |
| results of its own tools: Bash | 23 | 12,915 | 7.1% | 6,985 |
| results of its own tools: ScheduleWakeup, ReadNotifications, ListAgents, others | 39 | 2,007 | 1.1% | 1,768 |
| harness system-reminders (incl. skill listing 5,775) | 170 | 12,422 | 6.8% | 10,001 |
| harness hook outputs | 134 | 7,049 | 3.9% | 5,068 |
| harness loop/timer wake-ups, meta entries | 33 | 1,120 | 0.6% | — |
| task notifications | 20 | 7,967 | 4.4% | 2,739 |
| … of which a repeat wake-up from an agent already reported | 3 | 1,138 | 0.6% | — |
| … of which also says still running / unchanged | 2 | 824 | 0.5% | — |
| subagent returns (Agent / SendMessage results) | 19 | 4,730 | 2.6% | 2,134 |
| peer messages from other flows | — | — | — | 6,547 |
| the Primary's own text | 57 | 3,708 | 2.0% | 2,690 |
| the Primary's thinking (stored redacted) | 37 | 63 | ~0 | 0 |
| the living's words (incl. one image ≈1.5k) | 19 | 3,395 | 1.9% | 2,518 |

The living's words plus the Primary's own text come to 7.1k in a78e9a, which is 3.9% of what is billed.

### The ten largest single items (both transcripts)

| origin | item | tokens |
|---|---|---|
| startup prompt | first user message, a78e9a | 24,316 |
| startup prompt | first user message, 1add4b | 23,784 |
| Bash result | a `wc`-style listing of transcript files | 6,472 |
| system-reminder | skill listing, a78e9a | 5,775 |
| system-reminder | skill listing, 1add4b | 5,775 |
| startup prompt | system-prompt snapshot | 4,376 |
| startup prompt | system-prompt snapshot | 4,362 |
| Bash result | a listing of `flows/*` reports | 3,536 |
| task notification | one agent's full result | 2,739 |
| the living's words | image | 1,723 |

## 2. What the harness offers (Claude Code 2.1.294)

Sources: `claude --help`, strings in the binary `/nix/store/4slw0czfvd70df8a2c7077aqdilf0hgy-claude-code-2.1.294/bin/.claude-wrapped`, and the code.claude.com docs (sub-agents, settings, hooks, env-vars). None of these was tested in a live session.

| switch | exists | what it does | source |
|---|---|---|---|
| `--tools <list>` | yes | sets which built-in tools are available; `""` gives none | --help |
| `--allowedTools` | yes | allow rules for permissions; does not narrow the set | --help |
| `--disallowedTools` | yes | deny rules; a bare tool name removes the whole tool | --help; sub-agents doc |
| `permissions.deny` / `allow` / `ask` | yes | the same rules, set in settings | settings doc |
| whether a deny removes the tool from the model's list | unknown | — | not found |
| agent frontmatter `tools:` / `disallowedTools:` | yes | per-agent allowlist and denylist | sub-agents doc |
| `--agent <name>`, settings `"agent"` | yes | the main session runs as that agent, with its tools, model and prompt | --help; sub-agents doc |
| `--agents <json>` | yes | agents defined inline at launch | --help |
| PostToolUse `updatedToolOutput` | yes | a hook replaces a tool's result; if the shape does not match, the original is kept | hooks doc; binary string |
| SubagentStop hook | yes | can block the stop or add context; no rewrite of the result is documented | hooks doc |
| a cap on a subagent's result, or routing it to a file | not found | — | — |
| a switch that silences task-notifications | not found | — | binary strings |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | yes | no `run_in_background` for Bash or subagents (Monitor is exempt) | env-vars doc |
| `CLAUDE_CODE_FORK_SUBAGENT=0` | yes | turns fork mode off, so a subagent can be waited for | env-vars doc |
| `CLAUDE_CODE_DISABLE_CRON=1` | yes | turns off `/loop` and scheduled tasks; whether it also stops ScheduleWakeup is unknown | env-vars doc |
| `BASH_MAX_OUTPUT_LENGTH` / `bashOutputMaxChars` | yes | caps Bash output (default 30,000 chars) | env-vars doc |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | yes | caps a Read (default 25,000) | env-vars doc |
| `MAX_MCP_OUTPUT_TOKENS`, `TASK_MAX_OUTPUT_LENGTH` | name in binary | semantics not read | binary strings |
| `CLAUDE_CODE_TODO_REMINDER_MODE`, `CLAUDE_CODE_TOASTY_THIMBLE` | yes | todo and batching reminders | harness-anatomy.md:266-267 |
| `--bare` | yes | skips hooks, auto-memory and CLAUDE.md | --help |

## 3. What Flow Nexus 0.44 configures for a metaflow

Flow sets no per-metaflow or per-layer tool list or blacklist today.

- The harness command line is built in `flow/crates/flow-nexus/src/herdr/launch.rs:864-934` (`start_native_harness`). For Claude it passes `--dangerously-skip-permissions`, `--remote-control`, `--system-prompt-file`, `--model` and `--effort`. It passes none of `--tools`, `--allowedTools`, `--disallowedTools`, `--agent`, `--settings` or `--append-system-prompt`, and Flow writes no settings file.
- The per-launch type is `LaunchProfile`, specified at `signal-flow/ethos/signal.ethos:156` (rev 2893bb7) and generated into `src/generated/signal.rs:120-134`. Its fields are request id, source vector, skill names, aspect, power level, harness kind, model, effort, flow id, remembered flows, Herdr session, system-prompt bundle and instruction prompt. None of them is a tool field. `ComposedLaunch` (ethos:159) wraps it. Profiles are built in `crates/flow-nexus/src/composition.rs:104-169`.
- `accounts/harness-anatomy.md` already mapped this:
  - :58 "Everything else still arrives … 14 tool definitions, the Artifact tool's description alone being 20,093 characters."
  - :233 lists tool definitions (Agent 3,047 chars, Artifact 20,093, ScheduleWakeup 3,148, SendFeedback 3,467) as switchable by `--tools`, `--disallowedTools` and per-tool env.
  - :153 and :289-297 list tool-result wrappers, persisted-output notices and "[Old tool result content cleared]" under "No switch found".
  - :161 notes that the bypass steer contradicts the Read and Edit descriptions.

## 4. The vision in force

vision-model-roles:
> within the system a Primary's input and output are the dearest, far above a Secondary's, and a Secondary's above its subflows'. A message that saves a cheaper flow's words and makes a dearer one fetch has cost more, not less.

> The most complex reasoning goes to a Primary. … A Primary is the costly layer and is main-flow only.

> a Primary launches Secondaries and Tertiaries, and Quaternaries for small jobs.

> In the long term, a Fable flow does only the work that needs Fable. Every errand around it — fetching, relaying, publishing, reporting, delivering — is done for it by the flows below it, unasked. … a subflow it launches does errands only.

vision-flow-nexus:
> A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.

> Short term, the Secondary starts first, then its Primary.

> Long term, a Primary is a simplified flow, used only to render judgment: guiding a design or posing questions.

> Where the harness allows it, a part of a main flow's system prompt is the main flow's alone and is not passed down to its subagents.

> The heartbeat reaches only a flow for which something changed that bears on it.

intent-main-flow (`.claude/skills/intent-main-flow/SKILL.md`):
> A main flow is a coordinator of subflows first: its own context is spent on dialogue, judgment and synthesis, and everything else is given to the flow whose topic it is or to a subflow with a brief; what they did, you did.

intent-fable:
> A subflow gathers; a Fable flow judges.

## 5. How other systems keep a reasoner's context clean

| pattern | what the source says | source |
|---|---|---|
| orchestrator with summarizing workers | each sub-agent "returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)" | anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| the same, in research | subagents explore in their own windows "before condensing the most important tokens for the lead research agent" | anthropic.com/engineering/multi-agent-research-system |
| results routed to files | subagents "store their work in external systems" and "pass lightweight references back to the coordinator" | anthropic.com/engineering/multi-agent-research-system |
| file system as context | a document is dropped from context "if its path remains available in the sandbox" | manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus |
| planner separated from executor | ReWOO "detaches the reasoning process from external observations" | arxiv.org/abs/2305.18323 |
| plan-and-execute | the planner generates a multi-step plan; executors "invoke 1 or more tools" | langchain.com/blog/planning-agents |

None of these sources says outright that a planner should have no tools.
