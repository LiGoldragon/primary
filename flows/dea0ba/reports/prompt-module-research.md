# Prompt modules and their witnessed scope

This report separates delivered behavior from proposed Flow design. It does not
reproduce any hidden harness prompt.

## Current Claude evidence

An existing Claude Code 2.1.284 Haiku witness used harmless markers. A marker
in the main system prompt, whether the prompt was replaced or appended, was
visible to the main seat and absent from ordinary `general-purpose` and
`Explore` subagents. `CLAUDE.md` did reach `general-purpose`, did not reach
`Explore`, and an agent with `omitClaudeMd: true` did not receive it. The
published witness is [Answers on how Flow launches a seat](../../5578cc/books/answers-on-flow-launch.md).

This agrees with Claude's public account: ordinary subagents have their own
context and system prompt, while `CLAUDE.md` normally loads unless omitted;
Explore and Plan omit it. A fork is different because it copies the parent's
conversation and system prompt. The missing witness cases are therefore only:

1. whether a main-only marker reaches a fork;
2. whether an output-style marker reaches an ordinary subagent or a fork.

Field 42265e alone is authorized to run those cases. No repeat of the main
system-prompt, appended-prompt, `general-purpose`, Explore, `CLAUDE.md`, or
`omitClaudeMd` cases is warranted.

The procedure stays a harmless one-turn, no-tool disposable-fixture test. It
uses a marker and a direct-main positive control, captures `--print
--output-format stream-json`, the CLI version, and only the supplied fixture
files. An absent marker establishes the scoped behavior only after that direct
control and a subagent-definition positive control succeed. It does not read
credentials, hidden prompts, persistent settings, or production files.

## Public harness boundaries

Claude documents that `--append-system-prompt` adds to its default system
prompt. Its output styles are session-wide instruction layers for role, tone,
and response format; ordinary subagents run their own system prompts, while a
fork inherits the parent system prompt. Output style is guidance rather than
enforcement; hooks and permissions carry enforcement.

Codex's public CLI exposes `exec`, `agents`, sandbox and approval choices,
profiles/config overrides, JSONL output, and output schemas. Its open-source
configuration distinguishes system `instructions` from a separate
developer-role `developer_instructions`; its public prompt source describes
AGENTS.md as user-role context. No matching public Codex guarantee was found
for ordinary-subagent isolation of a main-only module. Treat Codex audience
selection as a launch-delivery policy until measured for the selected runtime.

Sources: [Claude subagents](https://code.claude.com/docs/en/sub-agents),
[Claude output styles](https://code.claude.com/docs/en/output-styles),
[Claude CLI](https://code.claude.com/docs/en/cli-usage),
[Codex config](https://github.com/openai/codex/blob/main/codex-rs/config/src/config_toml.rs),
and [Codex public prompt](https://github.com/openai/codex/blob/main/codex-rs/models-manager/prompt.md).

## Proposed module data

```ethos
Library
[]
[ PromptModuleName.String
  PromptModuleText.String
  PromptModuleClass.[ Purpose Behavior Personality OperationalSafety ]
  PromptAudience.[ MainFlow HarnessSubagent Both ]
  PromptProvenance.{ Source.String Revision.String }
  PromptModule.{ PromptModuleName PromptModuleClass PromptAudience
                 PromptModuleText PromptProvenance } ]
[]
```

Purpose states what the flow is and can do. Behavior gives work and
communication habits. Personality gives role, tone, and response form.
OperationalSafety governs tool authority, approval, isolation, and irreversible
actions. `Audience` states desired delivery scope, never proof that a harness
enforces it. `Provenance` stays separate from content and classification so a
module retains its source and revision.
