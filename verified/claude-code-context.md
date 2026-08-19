Subject: Claude Code context composition — how system prompt, system-reminders, and tool schemas are assembled for root sessions and subflows.

## In Claude Code 2.1.231, a subflow's system prompt is a harness-composed template: identity line, agent definition body, launcher-authority text, Notes block, environment and model line, deferred-tool info, scratchpad, and optional append text.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle, functions lIo, lOn, Cgv, $W, Bhe)
  Code read of the installed binary returned the assembly sequence: "identity line 'You are a Claude agent, built on Anthropic's Claude Agent SDK.' … then the agent definition body (getSystemPrompt()) … 'Messages from the agent that launched you…' → the Notes block (cwd reset, no report files, no emojis…) → `<env>` and model line → deferred-tool info → scratchpad → optional --append-subagent-system-prompt."

## In Claude Code 2.1.231, the subflow identity line is "You are a Claude agent, built on Anthropic's Claude Agent SDK.", chosen by the isNonInteractive branch of lIo, distinct from the main session's "You are Claude Code, Anthropic's official CLI for Claude".

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle, function lIo isNonInteractive branch)
  "identity line 'You are a Claude agent, built on Anthropic's Claude Agent SDK.' (chosen because subagents run non-interactive; the main session gets 'You are Claude Code, Anthropic's official CLI for Claude')"

## In Claude Code 2.1.231, a subflow's system prompt is different from and shorter than the main session's system prompt.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle) + probe (two subagents reproduced their system prompts verbatim)
  Code read confirmed different templates. Probe: both read-trivial (a generated packet) and built-in general-purpose reproduced their system prompts; both opened with harness text, then the packet body as one slice, then harness notes, env, model, scratchpad, git status, system-reminders. "Different template from the main session's, and shorter."

## In Claude Code 2.1.231, CLAUDE.md, git status, the current date, the skills list, and the sibling agent roster arrive as system-reminder messages, not in the system prompt; Explore and Plan agents omit CLAUDE.md and git status from system-reminders.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle)
  "CLAUDE.md, git status, date, the skills list and the sibling roster arrive as system-reminder messages, not in the system prompt (Explore and Plan omit CLAUDE.md and git status)."

## In Claude Code 2.1.231, tool schemas travel as the API's tools parameter, not in the system prompt.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle)
  "Tool schemas travel as the API's tools parameter."

## In Claude Code 2.1.231, --append-system-prompt and the SDK preset append reach a root flow's system prompt.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle)
  Session log of code-read result: "--append-system-prompt and the SDK's preset append add to a root flow's system prompt. Verified in code, Claude Code 2.1.231."
- 2026-07-28 · no session ID · method: code read (Claude Code 2.1.219 binary, --help output)
  "--append-system-prompt <prompt> appends to the default system prompt." (--help literal, ClaudeInjectedInstructions.md)

## The Claude Code docs line "Subagents receive only this system prompt plus basic environment details … not the full Claude Code system prompt" is contradicted by the Claude Code 2.1.231 code: subflows receive substantially more than their body plus environment details.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle) + probe (two subagents reproduced their system prompts)
  "The docs line is right that a subagent does not get the main session's prompt, and wrong that it gets 'only' its body plus environment details." Subflow system prompt includes harness notes, env, model, deferred-tool info, scratchpad — none authored by the packet body.

## In Claude Code 2.1.231, the "brief is your authority" paragraph in generated agent packets comes from Curriculum's SHARED_ROLE_BODY compiled at assembly.rs:453; its presence in the built-in general-purpose agent is unexplained.

- 2026-08-18 · session 358f143a · method: code read (Claude Code 2.1.231 bundle, assembly.rs:453)
  "The 'brief is your authority' paragraph is Curriculum's SHARED_ROLE_BODY (assembly.rs:453), put in every generated packet … Why the built-in general-purpose witness also showed it, no mechanism was found (no override file, no setting). Unknown; noted, not chased."
