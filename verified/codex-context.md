Subject: Codex context composition — how base instructions, developer instructions, AGENTS.md, and subagent context are assembled in Codex 0.145.0.

## In Codex 0.145.0, session base instructions are resolved in strict order: (1) config.base_instructions, (2) saved session base_instructions, (3) selected model catalog entry with fallback to the compiled product default.

- 2026-07-28 · no session ID · method: code read (rust-v0.145.0, core/src/session/mod.rs:614-631; report: CodexInjectedInstructions.md)
  "Session::new resolves the base block in this strict order (core/src/session/mod.rs:614-631): 1. config.base_instructions … 2. A saved rollout/session history session_meta.base_instructions. 3. The selected model catalog entry, whose fallback is BASE_INSTRUCTIONS_DEFAULT."

## In Codex 0.145.0, initial context is assembled as: developer_instructions, personality fragment, skills metadata, plugin suggestions, extension contributors, world state, then: assembled developer message, isolated developer messages, multi-agent-v2 hint, multi-agent-mode block, contextual user message.

- 2026-07-28 · no session ID · method: code read (rust-v0.145.0, core/src/session/mod.rs:3207-3464; report: CodexInjectedInstructions.md)
  "Session::build_initial_context_with_world_state_and_mcp … assembles a developer-section vector and a contextual-user-section vector. In observed source order it: 1. Adds a model-switch instruction … 2. Adds the effective developer_instructions … 4. Discovers skills … 8. Emits the assembled developer message, then isolated developer messages, then a multi-agent-v2 usage hint, then the multi-agent-mode block, then the contextual user message."

## In Codex 0.145.0, AGENTS.md workspace instructions are wrapped as "# AGENTS.md instructions for <directory>\n\n<INSTRUCTIONS>\n<file contents>\n</INSTRUCTIONS>" before being added to context.

- 2026-07-28 · no session ID · method: code read (rust-v0.145.0, context/user_instructions.rs:UserInstructions::body; report: CodexInjectedInstructions.md)
  "context/user_instructions.rs:UserInstructions::body wraps each selected file as: '# AGENTS.md instructions for <directory>\n\n<INSTRUCTIONS>\n<file contents>\n</INSTRUCTIONS>'"

## In Codex 0.145.0, the AGENTS.md loader caps each file's content at 32 KiB.

- 2026-07-28 · no session ID · method: code read (rust-v0.145.0, core/src/config/mod.rs:202-205; report: CodexInjectedInstructions.md)
  "The loader cap is 32 KiB (core/src/config/mod.rs:202-205)."

## In Codex 0.145.0, a spawned subagent copies the parent session's base instructions into its own config.base_instructions and then uses the same composition path.

- 2026-07-28 · no session ID · method: code read (rust-v0.145.0, tools/handlers/multi_agents_common.rs:build_agent_spawn_config; report: CodexInjectedInstructions.md)
  "tools/handlers/multi_agents_common.rs:build_agent_spawn_config copies the parent base instructions into config.base_instructions; the child then uses the same composition path."
