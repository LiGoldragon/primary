# codex-hijack repository report

## What was stood up

Public repository `LiGoldragon/codex-hijack` at
https://github.com/LiGoldragon/codex-hijack, cloned to
`/git/github.com/LiGoldragon/codex-hijack`.

Purpose: documentation and replacement of the Codex CLI harness's stock context.
Continues the base-context replacement design of flow 2f6b1dc5.

## Extraction methods and revisions

- Codex CLI version witnessed: **0.149.1**
- Binary path: `/nix/store/a2hlxqhdyc642f8m6zhgkl5l2cbh2bks-codex-0.149.1/libexec/codex`
- Source: openai/codex repository, tag `rust-v0.149.1`, commit `980a6d12110b110d29ec13bdcbe14011100b3566`
- Extraction method: `git show rust-v0.149.1:<path>` for every prompt file and template, from a local clone of openai/codex at `/git/github.com/openai/codex`
- Context assembly code read from `codex-rs/core/src/context/` module tree and `codex-rs/codex-home/src/instructions/mod.rs`
- All text copied verbatim from source; no text written from memory

## Block inventory (17 blocks)

1. Base context (instructions slot) -- 8 model-variant prompt files
2. AGENTS.md (user-role message)
3. Permissions instructions (developer-role) -- 7 template variants
4. Environment context (developer-role, dynamic XML)
5. Collaboration-mode instructions (developer-role)
6. Multi-agent mode instructions (developer-role)
7. Multi-agent role instructions (developer-role)
8. Multi-agent collaboration prompt (developer-role)
9. Personality spec (developer-role)
10. Model-switch instructions (developer-role)
11. Token budget / context window (developer-role)
12. User instructions / developer_instructions (developer-role)
13. Server-catalog instructions template
14. Guardian classifier instructions (internal, not model-visible)
15. Compact/checkpoint prompt (context management)
16. Apps/Plugins/Environments instructions (developer-role, dynamic)
17. Skill instructions (developer-role)

## Flagged worst-offender candidates

Ranked by estimated misalignment with the psyche's stated direction:

1. **Personality and tone prescriptions** -- "concise, direct, friendly" imposed
   from highest-priority position, overriding authored character
2. **Autonomy and persistence directives** -- "persist until fully handled",
   "autonomously resolve" contradict the extension model
3. **Output formatting and verbosity rules** -- OpenAI's UX aesthetic imposed on
   every interaction
4. **Plan tool behavior prescriptions** -- micro-management of tool usage
5. **AGENTS.md precedence rules** -- stock context takes precedence over
   AGENTS.md, the primary authored-context mechanism
6. **Escalation and approval behavior** -- prescribes specific safety UX
   workflows

## Blockers

- Server-catalog `instructions_template` content (Block 13): fetched at runtime
  from OpenAI's servers. Only one template file found in source
  (`gpt-5.2-codex_instructions_template.md`); the actual templates served to
  each model at runtime are unknown. This means the real base context for any
  model could differ from the compiled-in fallback.
- Server-catalog `collaboration_mode` messages: not present in source tree;
  content unknown.

## Override verification at 0.149.1

Re-verified against the 0.148.0 witnesses (flow 2f6b1dc5):
- `config.toml` `instructions` and `model_instructions_file`: confirmed full
  replacement, unchanged from 0.148.0
- `SessionCreateParams.base_instructions`: confirmed highest priority, unchanged
- `developer_instructions`: confirmed separate developer-role message, unchanged
- AGENTS.md: confirmed user-role delivery, unchanged

## Edit coordination

The meta-orchestrate lane registration machinery did not accept the DOTOS
syntax attempted. The claim is advisory; this is noted and work proceeded
without a registered lane.

## Sources

- openai/codex, tag `rust-v0.149.1`, commit `980a6d12`
- Codex binary: `/nix/store/a2hlxqhdyc642f8m6zhgkl5l2cbh2bks-codex-0.149.1/libexec/codex`
- Prior verified witness: `verified/claude-code-context.md` (Codex 0.148.0 sections)
- Psyche vision: `flows/4ddc321d/vision/hijackRepositories.md`
- Psyche vision: `flows/2f6b1dc5/vision/systemPrompt.md`
