# Codex CLI Harness Research

Flow: 7b4d4c
Date: 2026-09-04
Subject: OpenAI Codex CLI, version 0.153.2 (installed)

## 1. Installed Version and Instruction Mechanisms

**Version**: codex-cli 0.153.2, installed at `/home/li/.nix-profile/bin/codex`.
Witnessed by running `codex --version` (output: `codex-cli 0.153.2`).

### Config Keys (config.toml)

All keys below witnessed in source at `codex-rs/config/src/config_toml.rs` (openai/codex, main branch, 2026-09-04):

| Key | Type | Role | Purpose |
|-----|------|------|---------|
| `instructions` | `Option<String>` | System (Responses API `instructions` field) | "System instructions." Fallback after `model_instructions_file` and inline `base_instructions`. |
| `model_instructions_file` | `Option<AbsolutePathBuf>` | System (Responses API `instructions` field) | Path to file replacing built-in base instructions. Strongly discouraged by source comment: "deviating from the instructions sanctioned by Codex will likely degrade model performance." |
| `developer_instructions` | `Option<String>` | Developer-role message | Additional developer instructions injected as a developer-role message. |
| `include_permissions_instructions` | `Option<bool>` (default true) | Developer-role message | Whether to inject the permissions developer block. |
| `personality` | `Option<Personality>` | Interpolated into base instructions | Communication style; interpolated into the model's `instructions_template` via a placeholder. |

**Precedence for base instructions** (witnessed in `codex-rs/core/src/config/mod.rs`, lines 3901-3914):
```
base_instructions = base_instructions  // from session/thread state
    .or(file_base_instructions)        // from model_instructions_file
    .or(cfg.instructions)              // from config.toml `instructions` key
```
When any of these is set, provenance is marked `Custom`. Otherwise, the model's `instructions_template` from the model catalog is used (provenance `Model`).

### CLI Flags

Witnessed from `codex --help` and `codex exec --help`:

- `-c, --config <key=value>`: Override any config.toml key, including `developer_instructions`, `instructions`, etc.
- `-m, --model <MODEL>`: Model selection.
- `-p, --profile <CONFIG_PROFILE_V2>`: Layer `$CODEX_HOME/<name>.config.toml` on top.
- `--ignore-user-config`: Do not load `$CODEX_HOME/config.toml`.
- `--ignore-rules`: Do not load `.rules` files.

### Environment Variables

No dedicated environment variable for base instructions or developer instructions was found. The harness reads `CODEX_HOME` (defaults to `~/.codex`) for config and AGENTS.md discovery. Witnessed from `codex exec --help` and source.

### AGENTS.md Discovery

Witnessed in `codex-rs/core/src/agents_md.rs` and `codex-rs/codex-home/src/instructions/mod.rs`:

1. **Global scope** (`$CODEX_HOME/`): Checks `AGENTS.override.md` first, then `AGENTS.md`. Uses only the first non-empty file. Injected as a user-role message.
2. **Project scope**: Walks from project root (found by `.git` or configured `project_root_markers`) down to cwd. At each directory level, checks `AGENTS.override.md`, then `AGENTS.md`, then `project_doc_fallback_filenames`. Concatenates all found files in root-to-cwd order. Each injected as a user-role message with directory annotation.
3. **Size limit**: `project_doc_max_bytes` (default 32 KiB, documented at learn.chatgpt.com).

### Debug Inspection

`codex debug prompt-input [PROMPT]` renders the model-visible prompt input as JSON, showing all injected messages. This is the primary witness mechanism for what the model sees. Witnessed from `codex debug prompt-input --help`. (On this machine, execution fails due to app-server remote config; this is an environmental issue, not a limitation of the command.)

## 2. Prompt Composition Architecture

### Source Files (open-source, github.com/openai/codex, MIT license)

**Base instructions default text**: `codex-rs/protocol/src/prompts/base_instructions/default.md` — included at compile time via `include_str!`. Witnessed in `codex-rs/protocol/src/models.rs` line 1504: `pub const BASE_INSTRUCTIONS_DEFAULT: &str = include_str!("prompts/base_instructions/default.md");`

**Per-model override**: The model catalog (served by backend, cached in `~/.codex/models_cache.json`) carries an `instructions_template` per model. When present, this template replaces the compiled-in default. A `{personality}` placeholder is interpolated with the configured personality. Witnessed in `codex-rs/protocol/src/openai_models.rs`, `get_model_instructions()`.

**Prompt struct** (`codex-rs/core/src/client_common.rs`):
```rust
pub struct Prompt {
    pub input: Vec<ResponseItem>,         // conversation items
    pub(crate) tools: Arc<[ToolSpec]>,    // tool definitions
    pub base_instructions: BaseInstructions, // maps to Responses API `instructions`
    pub output_schema: Option<Value>,
    ...
}
```
Witnessed in source.

### How It Maps to the API

Witnessed in `codex-rs/core/src/client.rs`, `build_responses_request()`:

**Standard path** (non-responses-lite): `prompt.base_instructions.text` is sent as the `instructions` field of the OpenAI Responses API request — the top-level system-prompt equivalent. Developer-role and user-role messages are sent in the `input` array.

**Responses-lite path**: `base_instructions.text` is converted into a developer-role `BaseInstructionsFragment` message and prepended to the `input` array. The API `instructions` field is set to an empty string.

### Message Ordering in the Input Array

The input array is built by the session's conversation history plus context fragments. Each fragment type has a role and content kind. The ordering, witnessed from the context module (`codex-rs/core/src/context/`) and turn builder:

1. **Base instructions** — developer role, content kind `model.base_instructions` (only in responses-lite; otherwise in the API `instructions` field)
2. **Permissions instructions** — developer role (via `codex_prompts::PermissionsInstructions`)
3. **Skill catalog** (`AvailableSkillsInstructions`) — developer role, content kind `skills.catalog`
4. **Plugin instructions** — developer role
5. **Apps instructions** — developer role
6. **Environment context** — user role
7. **Developer instructions** (`DeveloperInstructions`) — developer role, content kind `generic.developer_instructions`
8. **AGENTS.md** (`UserInstructions`) — user role, content kind `agents_md.instructions`, wrapped in `# AGENTS.md instructions` / `</INSTRUCTIONS>` markers, with directory annotation
9. **Personality spec** — developer role
10. **Guardian policy** — developer role (injected into the guardian's review session, not the main session)
11. **Conversation turns** — user/assistant/tool messages

### What Stays Regardless of Override

When `model_instructions_file` or `instructions` replaces the base instructions, the following are still injected as separate developer-role or user-role messages (not part of base instructions):

- Permissions instructions (developer role)
- Skill catalog and usage instructions (developer role)
- Plugin instructions (developer role)
- Apps instructions (developer role)
- Environment context (user role)
- Developer instructions from config (developer role)
- AGENTS.md content (user role)
- Guardian policy (in the separate guardian review session)
- Tool definitions (sent as tool specs, not messages)
- Sandbox and approval-policy enforcement (handled by the guardian, a separate model session)

Witnessed in source: each of these is a separate `ContextualUserFragment` implementation with its own `role()` and `content_kind()`, assembled independently of `base_instructions`.

## 3. Model Visibility vs. Living Visibility

### Can the Model See Its Base Instructions?

**Yes.** The base instructions are the model's system prompt. In the standard Responses API path, they are the `instructions` field, which the model receives and acts on. In responses-lite mode, they are a developer-role message in the conversation. Witnessed in `build_responses_request()`.

### Can the Living See the Base Instructions?

**Partially.** The living has several avenues:

1. **Source code**: The compiled-in default is at `codex-rs/protocol/src/prompts/base_instructions/default.md` in the open-source repo. Documented (github.com/openai/codex, MIT license, read 2026-09-04).
2. **Per-model overrides**: The model catalog is cached at `~/.codex/models_cache.json`, which contains the `instructions_template` for each model. The living can read this file. Witnessed by file existence at `~/.codex/models_cache.json` (286 KiB).
3. **`codex debug prompt-input`**: Renders the complete model-visible input as JSON, including all injected messages. When this command works (requires no remote app-server config), it shows everything. Documented in `codex debug prompt-input --help`.
4. **Session logs**: Stored in `~/.codex/logs_2.sqlite`. The living can query these for the actual prompts sent.

**What the living cannot easily see**: The per-model `instructions_template` served by the backend may differ from what is cached locally, and the living cannot inspect the backend's authoritative catalog without network access. The `personality` interpolation result is only visible through `debug prompt-input` or session logs.

## 4. Stratum Analysis

Using the three-stratum model from context-strata:

### Top Stratum: Base Context

| Mechanism | Placement | Evidence |
|-----------|-----------|----------|
| Base instructions (default.md or model template) | Top — Responses API `instructions` field | Witnessed: `build_responses_request()` sends `base_instructions.text` as `instructions` |
| Personality interpolation | Top — baked into base instructions | Witnessed: `get_model_instructions()` replaces `{personality}` placeholder |
| `model_instructions_file` override | Top — replaces default base instructions | Witnessed: config/mod.rs line 3901 |
| `instructions` config key | Top — fallback for base instructions | Witnessed: config/mod.rs line 3912 |

### Middle Stratum: Typed Prompt, Injections, Skill Loads

| Mechanism | Placement | Evidence |
|-----------|-----------|----------|
| `developer_instructions` config key | Middle — developer-role message | Witnessed: `DeveloperInstructions` fragment, role `"developer"` |
| Permissions instructions | Middle — developer-role message | Witnessed: `PermissionsInstructions`, re-exported |
| Skill catalog (available skills list) | Middle — developer-role message | Witnessed: `AvailableSkillsInstructions`, role `"developer"`, kind `skills.catalog` |
| Selected skill body (when loaded by model via `skills.read`) | Middle — user-role message | Witnessed: `SkillInstructions`, role `"user"`, kind `skills.selected_skill_instructions` |
| Plugin instructions | Middle — developer-role message | Witnessed: `PluginInstructions` fragment |
| Apps instructions | Middle — developer-role message | Witnessed: `AppsInstructions` fragment |
| AGENTS.md content | Middle — user-role message | Witnessed: `UserInstructions`, role `"user"`, kind `agents_md.instructions` |
| Multi-agent mode instructions | Middle — developer-role message | Witnessed: `MultiAgentModeInstructions` fragment |
| User's typed prompt | Middle — user-role message | Witnessed: `response_item_from_user_input()` |

### Bottom Stratum: Fetched Text, Own Output

| Mechanism | Placement | Evidence |
|-----------|-----------|----------|
| Tool call results (shell output, apply_patch results) | Bottom — tool-role messages | Witnessed: standard tool message flow |
| Model's own output | Bottom — assistant-role messages | Witnessed: standard conversation flow |
| Skill body read by tool (not the harness injection) | Bottom — tool result | Inferred: `skills.read` tool returns content as tool output |

### Does "Codex Has Four Strata" Hold?

**No, not in a meaningful sense.** The three-stratum model applies cleanly:

1. **Top**: The `instructions` field (base instructions) — this is the system prompt. It is a single text block, not further subdivided by the API.
2. **Middle**: All developer-role and user-role context messages — developer_instructions, AGENTS.md, skill catalog, permissions, plugins, apps, the user's typed prompt.
3. **Bottom**: Tool results, model output, fetched content.

A case for "four" could be made by splitting the top stratum: the API `instructions` field is technically separate from developer-role messages, and a developer-role message outranks a user-role message in OpenAI's precedent hierarchy. But this is a distinction within the middle stratum, not a fourth stratum. The OpenAI Responses API has one `instructions` field (top) and one `input` array (middle and bottom). Within `input`, the `developer` vs `user` role distinction is a priority signal, not a separate delivery mechanism — both live in the same array.

**More precisely**: The `instructions` field (top stratum) is architecturally separate from the `input` array. Within `input`, developer-role messages (middle-high) and user-role messages (middle-low) carry different authority, but they share the same delivery channel. This gives Codex a **top + middle-high + middle-low + bottom** layering, which is three strata with the middle having a developer/user sub-ranking. This matches the context-strata model rather than requiring a fourth stratum.

## 5. Running with Fully Replaced Base Instructions

### Known Consequences

Witnessed from source (`codex-rs/config/src/config_toml.rs`, lines 249-253):
> "Users are STRONGLY DISCOURAGED from using this field, as deviating from the instructions sanctioned by Codex will likely degrade model performance."

### What Persists Outside the Prompt

1. **Guardian (safety) layer**: The guardian is a separate model session with its own policy prompt. It reviews proposed tool calls before execution. Replacing base instructions does NOT affect the guardian's policy. Witnessed in `codex-rs/core/src/guardian/prompt.rs` — the guardian builds its own context independently.

2. **Sandbox enforcement**: The sandbox (read-only, workspace-write, danger-full-access) is enforced at the OS level (Linux sandbox binary), not by the prompt. Changing instructions cannot bypass sandbox restrictions. Witnessed: `codex_linux_sandbox_exe` config key, `--sandbox` CLI flag.

3. **Approval policy**: The approval policy (`approval_policy`, `--approve-for-me`, `--dangerously-bypass-approvals-and-sandbox`) is enforced by the harness runtime, not by the prompt. Witnessed: these are CLI flags and config keys, not prompt text.

4. **Tool definitions**: Tool specs are generated by the harness and sent separately from instructions. They define what tools are available. Replacing instructions does not change the tool set. Witnessed: `Prompt.tools` field is independent of `base_instructions`.

5. **Permissions instructions**: When `include_permissions_instructions` is true (default), permissions guidance is injected as a separate developer-role message regardless of base instructions content. Witnessed: separate `ContextualUserFragment` implementation.

### Community Experience

A GitHub discussion (github.com/openai/codex/discussions/7296, "Pro Tip: Use a custom system prompt with codex") documents users replacing base instructions. The main findings: custom instructions work for specialized workflows but can cause degraded tool use (especially `apply_patch`) when the base instructions' tool-use guidance is lost. Documented (discussion #7296, read 2026-09-04).

A closed feature request (github.com/openai/codex/issues/12926) proposed `developer_instructions_file` as a safer alternative to replacing base instructions, noting that AGENTS.md "is not consistently followed enough for strict workflows." The request was closed as not planned. Documented (issue #12926, read 2026-09-04).

## Sources

1. `codex --version`, `codex --help`, `codex exec --help`, `codex debug prompt-input --help` — witnessed 2026-09-04 on installed codex-cli 0.153.2
2. `~/.codex/config.toml` — witnessed 2026-09-04
3. `codex-rs/protocol/src/models.rs` — github.com/openai/codex, main branch, read 2026-09-04
4. `codex-rs/protocol/src/prompts/base_instructions/default.md` — github.com/openai/codex, main branch, read 2026-09-04
5. `codex-rs/core/src/context/base_instructions.rs` — github.com/openai/codex, main branch, read 2026-09-04
6. `codex-rs/core/src/context/developer_instructions.rs` — github.com/openai/codex, main branch, read 2026-09-04
7. `codex-rs/core/src/context/user_instructions.rs` — github.com/openai/codex, main branch, read 2026-09-04
8. `codex-rs/codex-home/src/instructions/mod.rs` — github.com/openai/codex, main branch, read 2026-09-04
9. `codex-rs/core/src/agents_md.rs` — github.com/openai/codex, main branch, read 2026-09-04
10. `codex-rs/core/src/client.rs` (`build_responses_request`) — github.com/openai/codex, main branch, read 2026-09-04
11. `codex-rs/core/src/client_common.rs` (Prompt struct) — github.com/openai/codex, main branch, read 2026-09-04
12. `codex-rs/config/src/config_toml.rs` — github.com/openai/codex, main branch, read 2026-09-04
13. `codex-rs/core/src/config/mod.rs` — github.com/openai/codex, main branch, read 2026-09-04
14. `codex-rs/ext/skills/src/fragments.rs` — github.com/openai/codex, main branch, read 2026-09-04
15. `codex-rs/ext/skills/src/catalog_prompt.rs` — github.com/openai/codex, main branch, read 2026-09-04
16. `codex-rs/core/src/guardian/prompt.rs` — github.com/openai/codex, main branch, read 2026-09-04
17. Configuration Reference — https://learn.chatgpt.com/docs/config-file/config-reference, read 2026-09-04
18. AGENTS.md documentation — https://learn.chatgpt.com/docs/agent-configuration/agents-md, read 2026-09-04
19. Discussion #7296 — https://github.com/openai/codex/discussions/7296, read 2026-09-04
20. Issue #12926 — https://github.com/openai/codex/issues/12926, read 2026-09-04
21. `codex-rs/core/src/prompt_debug.rs` — github.com/openai/codex, main branch, read 2026-09-04
22. `codex-rs/core/src/session/turn.rs` (`build_prompt`) — github.com/openai/codex, main branch, read 2026-09-04
