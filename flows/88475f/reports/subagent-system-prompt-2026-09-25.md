# Claude Code 2.1.280: how a subagent system prompt is built (subflow read of the installed bundle)

- Preamble sentence chosen at request layer (jRn): interactive → "You are Claude Code, Anthropic's official CLI for Claude."; non-interactive → "You are a Claude agent, built on Anthropic's Claude Agent SDK." (or the "running within the Claude Agent SDK" variant with an append). Background subagents are forced non-interactive.
- Myt wraps every Task-tool subagent prompt: agent body + fixed "Messages from the agent that launched you…" sentence + Notes block + attachment/reminder section. String literals, no parameters.
- Custom .claude/agents/*.md body = the agent part (plus memory if set).
- Levers: --append-subagent-system-prompt[-file] (appends to every subagent, nested too; --print only; env CLAUDE_CODE_ENABLE_APPEND_SUBAGENT_PROMPT); agent body / --agents JSON prompt; subagent_type "fork" passes the parent's whole prompt, bypassing Myt; CLAUDE_CODE_DISABLE_ATTACHMENTS / CLAUDE_CODE_SIMPLE drop the reminder section; CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS.
- Not found: any key or setting that removes or replaces the preamble or Notes.
- A project/user agent named general-purpose, Explore or Plan overrides the built-in (later sources win in merge IW).
