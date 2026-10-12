# Context contents experiment, 2026-10-12

Claude Code 2.1.294, model `haiku` (resolved to `claude-haiku-5-5`),
prompt `reply OK` unless stated. Every number below is the API usage
the harness recorded: `input + cache_creation + cache_read` of one
model call, here called "total". Main-session numbers come from the
`--output-format stream-json --verbose` stream (per assistant
message); subagent numbers come from the first assistant message in
the subagent transcript
`~/.claude/projects/<cwd-slug>/<session>/subagents/agent-*.jsonl`.

## Setup

All runs from a scratch directory outside Primary, a fresh `git init`
repository, so no Primary CLAUDE.md, hooks or settings applied.
User settings, user hooks and MCP servers were excluded by flags, held
constant in every run:

```
cd $SCRATCH/ctx
claude -p "$PROMPT" --model haiku \
  --output-format stream-json --verbose \
  --setting-sources project --strict-mcp-config \
  [VARIED FLAGS] </dev/null
```

Subagent definitions, in `$SCRATCH/ctx/.claude/agents/`:

```
---
name: probe-all
description: Probe subagent with every tool. Use only when asked by name.
model: haiku
---
You are a probe. Do exactly what the prompt asks.
```

`probe-read` is identical except `name: probe-read` and `tools: Read`.
Subagent runs used the main prompt: `Call the Agent/Task tool once, in
the foreground (run_in_background false), with subagent_type "<agent>"
and prompt "reply OK". Then reply OK.`

## Main session: tool set

| Run | Varied flags | Tools offered | in | cache create | cache read | total |
|---|---|---|---|---|---|---|
| a | none (default) | 24 | 2 | 3963 | 10778 | 14743 |
| a2 | none (repeat) | 24 | 2 | 4093 | 10778 | 14873 |
| b | `--tools Read` | 1 | 2 | 2450 | 1452 | 3904 |
| b2 | `--tools Read,Bash` | 2 | 2 | 5314 | 0 | 5316 |
| c | `--tools ""` | 0 | 2 | 2424 | 535 | 2961 |
| e1 | `--tools Read --system-prompt "You are a probe. Do exactly what the prompt asks."` | 1 | 2 | 1583 | 0 | 1585 |
| e0 | `--tools "" --system-prompt "<same>"` | 0 | 2 | 596 | 0 | 598 |

The 24 default tools: Task, Bash, CronCreate, CronDelete, CronList,
DesignSync, Edit, EnterWorktree, ExitWorktree, ListAgents, Monitor,
NotebookEdit, PushNotification, Read, RemoteTrigger, ReportFindings,
ScheduleWakeup, SendMessage, Skill, TaskStop, ToolSearch, WebFetch,
WebSearch, Write.

Observed:
- Tool descriptions take main-session context. Default set 14743-14873;
  no tools 2961. The default tool set costs about 11.8k tokens with
  deferral on.
- Read alone: 3904 - 2961 = 943 (default prompt); 1585 - 598 = 987
  (replaced prompt). Bash adds 5316 - 3904 = 1412.
- The default system prompt body, with tools off, is 2961 - 598 = about
  2.4k tokens more than a one-line replacement prompt.
- Run-to-run variation of the default run: 130 tokens (a vs a2).

## Main session: deferred tools (ToolSearch)

| Run | Env | Tools offered | total |
|---|---|---|---|
| d-nodefer | `ENABLE_TOOL_SEARCH=false` | 23 (no ToolSearch) | 30107 |
| d-defer | `ENABLE_TOOL_SEARCH=true` | 24 | 14852 |
| a2 | unset | 24 | 14873 |

Deferral is on by default and saves about 15.25k tokens on the first
call (30107 vs 14852). With deferral off the full tool set costs about
27.1k tokens (30107 - 2961).

Which tools are deferred was not observable in the stream; asked by
prompt (a claim by the model, not a witness), the main session named as
loaded Agent, Bash, Edit, ListAgents, Read, ReportFindings,
ScheduleWakeup, Skill, ToolSearch, Write, and as deferred CronCreate,
CronDelete, CronList, DesignSync, EnterWorktree, ExitWorktree, Monitor,
NotebookEdit, PushNotification, RemoteTrigger, SendMessage, TaskStop,
WebFetch, WebSearch.

## Subagent: tool set

| Run | Agent | Env | Request | first call total |
|---|---|---|---|---|
| s-all | probe-all | unset | background | 9374 |
| s2-probe-all | probe-all | unset | foreground | 10691 |
| s3-all-rep | probe-all | unset | foreground | 10857 |
| s4-list | probe-all | unset | foreground, longer prompt | 11011 |
| s3-all-nodefer | probe-all | `ENABLE_TOOL_SEARCH=false` | foreground | 26106 |
| s2-probe-read | probe-read (`tools: Read`) | unset | foreground | 2248 |
| m0-nomarker | probe-read | unset | foreground, longer prompt | 2413 |
| s3-gp | built-in general-purpose | unset | foreground | 11294 |

Observed:
- Tool descriptions take subagent context the same way. All tools:
  10691-10857 foreground; `tools: Read`: 2248. Restricting the
  subagent to Read saves about 8.5k tokens on every subagent call.
- Deferral applies inside the subagent: off 26106, on 10857, a saving
  of about 15.25k, the same as in the main session.
- A background subagent started about 1.3k smaller (9374) than a
  foreground one; the cause was not isolated.
- Asked by prompt (a claim), the probe-all subagent listed the same
  loaded and deferred tools as the main session, minus ScheduleWakeup.

## Subagent: what of the main system prompt reaches it

Marker prompt sent to probe-read: quote any string starting
`APPEND-MARKER` or `CLMD-MARKER`, state the working directory, say
whether a gitStatus or environment section is present, say whether
`padding0` or `padding1499` is visible. Padding was 1500 words
`padding0 ... padding1499` after the marker.

| Run | Varied | Main first call total | Subagent first call total | Subagent answer |
|---|---|---|---|---|
| m0 | nothing | 15224 | 2413 | NONE; cwd given; env and gitStatus present; no padding |
| m1 | `--append-system-prompt "APPEND-MARKER-QV7K3. <padding>"` | 21770 (+6546) | 2443 (+30) | NONE; no padding |
| m2 | `CLAUDE.md` in cwd with `CLMD-MARKER-H4P2.` + padding | 21964 (+6740) | 9153 (+6740) | quoted CLMD-MARKER-H4P2; padding seen |

Observed:
- `--append-system-prompt` text does not reach a custom subagent:
  the main call grew 6546 tokens, the subagent call 30 (the prompt text
  of the two runs differs by a few words), and the subagent could not
  quote the marker.
- Project CLAUDE.md does reach the subagent: the same +6740 tokens in
  both main and subagent, and the subagent quoted the marker.
- The subagent receives its own working directory, an environment
  section and a gitStatus block.
- The default main system prompt body does not appear to reach a
  custom subagent: probe-read (agent body + Read + env + gitStatus)
  totals 2248, against 3904 for the main session with Read and the
  default prompt, and 1585 for the main session with Read and a
  one-line prompt. This is an inference from token arithmetic; the
  subagent's system text itself was not observed.

## Limitations

- Totals are the API's count of the whole request; the split between
  system prompt, tool schemas and user-message context is inferred by
  difference, not observed.
- The harness's request body was not captured; which tools were
  deferred, and the subagent's exact system text, rest on differences
  and on the models' own answers.
- One or two runs per condition; observed run-to-run noise is about
  100-170 tokens.
- Skills (none in the scratch project) and user settings were excluded
  by `--setting-sources project`; with user settings, skills and
  plugins, both main and subagent totals would grow by what those add.
- Only haiku was measured. Tool-schema token counts depend on the
  tokenizer and could differ for other models.
- Only custom agents and general-purpose were tested as subagents;
  the fork subagent type, which inherits the parent's context, was not.

Temporary files (scratch directory and the scratch-run transcripts
under `~/.claude/projects/` and `/tmp/claude-1001/`) were removed after
the runs.
