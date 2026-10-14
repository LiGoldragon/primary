---
description: Version-qualified differences between parent and child prompts and skill loading in Claude Code and Codex.
---

These facts were checked on 2026-10-13 against installed Claude Code 2.1.294 and Codex 0.161.0-alpha.2. Prompt inclusion and access to a shared file are different questions.

## Claude Code

An ordinary named custom agent has its own system prompt: its Markdown body becomes `getSystemPrompt`, and the agent runner builds the child request from that definition. The main thread's custom system prompt and append text are not automatically substituted for that body. Thus the main can receive system text that this child does not receive as system text. Shared project instructions, explicit task text, hooks and separately appended child instructions can still supply additional context.

The fork agent is different: it carries the parent conversation and prompt. The ordinary custom-agent separation is not a claim that every Claude child omits parent instructions.

An agent's `skills` field selects bodies preloaded into that agent's context as meta user messages. The inspected runner resolves each named skill, checks availability/policy and calls its prompt loader before adding the body. It need not preload that body into the main thread. This is selective context loading, not concealed existence or protected access: discovery metadata can be visible to the main, and a readable shared skill file is not made secret by naming it in a child definition. A successful preload also does not establish that another agent cannot invoke the skill.

## Codex

The inspected child configuration copies `session.get_base_instructions()` into the spawned child's base instructions. Its ordinary role override structure does not include a replacement base-instructions file. Consequently this route does not provide a main-only section of the literal base system prompt.

Developer instructions are separate. The parent-derived developer instructions can be replaced by a named role's `developer_instructions`; multi-agent V2 also has `subagent_developer_instructions`. This can give main and child different developer context without changing their shared base instructions. Full-history forks carry conversation history as well; a differing child configuration does not erase already carried text.

The role loader accepts skill overrides that disable inherited skills or instruction inclusion; it discards positive `enabled` entries and positive bundled/include-instructions overrides. It therefore does not establish a named-role mechanism that enables a skill hidden or disabled in the main. The remaining child-only skill-discovery and native isolation questions are in `inquiry-harness-contracts`.

## Evidence

Claude's installed bundled source: local agent parser `OQn` at byte 214479552, child prompt selection around 220272809, `pd` at 220292561, and skill preload around 220277154. The initialized scratch catalog recognizes the named fixture; no child/model turn was launched for that probe. The current [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents) corroborates custom prompts and distinguishes the fork route.

Codex source: exact tag `rust-v0.161.0-alpha.2`, commit `5ccfcfe0fe510784521a3328b93f1c2fccc5e7a1`, `codex-rs/core/src/agent/child_config.rs` and `agent/role.rs`. Source capability here is not a new live parent/child visibility experiment. Retained source and probe evidence: `/home/li/private-repos/flow-evidence/41fa34/harness-knowledge-20261013/`.
