---
description: How the installed Claude and Codex UserPromptSubmit hooks can add recurring reminders, and which model-context role receives them.
---

Both inspected harness versions offer a command hook at `UserPromptSubmit` that can return additional model context: Claude Code 2.1.294 and Codex 0.161.0-alpha.2. This is a capability of their hook interfaces, not a claim that a twentieth-prompt reminder is installed on any seat.

## Event, cadence and text

A command handler receives event JSON on stdin and returns output. `UserPromptSubmit` supplies the submitted prompt and session identity. An external handler can retain a session-keyed count and emit context only on selected invocations. The inspected interfaces do not provide a built-in “every twentieth prompt” scheduler or a prompt-count field. Such a cadence would count handler/event invocations according to its own state; it is not automatically the number of model requests, tool calls, assistant messages or successfully completed turns.

For the inspected JSON channel, the model-context text is the string `hookSpecificOutput.additionalContext`, with `hookSpecificOutput.hookEventName` set to `UserPromptSubmit` and a successful command exit. Empty/no context output adds no reminder. The hook supplies literal text; this interface is not itself an invocation of a named native skill loader. Printing a skill body adds that text under the hook's context route, without promoting it into the base system prompt.

## Claude Code: conversation user context

The installed hook runner builds input containing `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name` and `prompt`, with optional agent/prompt-related fields. The context result becomes a `hook_additional_context` attachment.

The model-facing converter turns that attachment into `Re({content: Ybe(...), isMeta: true})`. `Re` creates a message with `role: "user"`; `Ybe` escapes reminder delimiters in supplied text and wraps it as a system reminder. Thus the reminder is meta user conversation context, with a hook label and reminder wrapper. The wrapper's name does not make it a native system-role message or replace the main system prompt. It enters at the event's conversation position for the subsequent model request.

The current [Claude hook reference](https://code.claude.com/docs/en/hooks) corroborates additionalContext insertion. `systemMessage` is a different output field intended for user-facing warning/display behavior; its name does not establish system-prompt injection.

## Codex: developer conversation context

In the exact inspected source, `inspect_pending_input` runs `UserPromptSubmit` for `TurnInput::UserInput`; response items, function-call outputs and inter-agent communication take separate paths that do not run this event there. Consequently not every incoming record or model continuation increments this event.

Codex input includes `session_id`, `turn_id`, `cwd`, nullable `transcript_path`, `model`, `permission_mode` and `prompt`, with optional subagent fields. The handler's additional context is recorded through `HookAdditionalContext`. That fragment explicitly returns `role: "developer"` and content kind `hooks.additional_context`, with no enclosing marker text. It is developer conversation context, separate from base instructions. A hook notification or warning entry is not by itself evidence that this context was injected.

## Verification and limits

Claude bundled source SHA-256: `41cd529f8f75c5ee797d82f7416d7298795c86cca1457703b61e1d15ee993874`. Event construction is around byte 215315485; common input builder `xd` is at 215321106; context conversion is at 216796666, `Re` at 216713087, and reminder wrapping at 216769793. These are byte offsets in the installed 2.1.294 executable, not stable APIs.

Codex source: tag `rust-v0.161.0-alpha.2`, commit `5ccfcfe0fe510784521a3328b93f1c2fccc5e7a1`; `codex-rs/hooks/src/events/user_prompt_submit.rs`, its generated input/output schemas, `codex-rs/core/src/hook_runtime.rs`, `session/turn.rs`, and `context/hook_additional_context.rs`. This version's hook feature/configuration/trust gates remain prerequisites. Source inspection is not a new twenty-prompt native witness.

The original 2026-09-24 words are retained in `flows/d8df70/vision/mainFlowMode.md`: they ask about automatic loading every so many messages, without fixing twenty in that record. Twenty is the current inquiry's cadence. No past implementation, native skill reload, persistence through compaction or behavior improvement is inferred from the original question. Exact source fragments and the original record are retained in `/home/li/private-repos/flow-evidence/41fa34/periodic-hook-knowledge-20261013/`.
