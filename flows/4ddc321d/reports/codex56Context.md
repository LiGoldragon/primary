# GPT-5.6 Codex stock base context

Walk scope: GPT-5.6 only ("we dont care about anything but 5.6").

## Model witnessed

Configured model: **`gpt-5.6-sol`**

Source: `~/.codex/config.toml`, key `model = "gpt-5.6-sol"`.

All three 5.6 variants in the server catalog (`gpt-5.6-sol`, `gpt-5.6-terra`,
`gpt-5.6-luna`) share a byte-identical `instructions_template` (17730 chars,
168 lines). Verified by hash comparison from `models_cache.json`.

## Selection path

No compiled-in prompt file matches any 5.6 model name. The 8 compiled-in files
stop at GPT-5.2. The priority chain (from `codex-rs/core/src/session/mod.rs`
lines 648-661):

```rust
let base_instructions = config
    .base_instructions
    .clone()
    .or_else(|| conversation_history.get_base_instructions().map(|s| s.text))
    .unwrap_or_else(|| model_info.get_model_instructions(config.personality));
```

1. `config.base_instructions` -- not set (no `instructions` or
   `model_instructions_file` key in config.toml).
2. `conversation_history.get_base_instructions()` -- only for resumed threads.
3. `model_info.get_model_instructions(config.personality)` -- the fallback.

`get_model_instructions` (`codex-rs/protocol/src/openai_models.rs` line 507)
reads `model_messages.instructions_template` from the server catalog. For
gpt-5.6-sol, `instructions_variables` is null, so the template is returned
verbatim with no substitution. `personality = "pragmatic"` does not affect the
base context; it is injected as a separate developer-role message.

Path taken: **server-catalog `instructions_template`, verbatim, no
substitution**.

## Capture method

Extracted from `~/.codex/models_cache.json` -- the local cache of the server
catalog fetched by the Codex CLI at runtime from OpenAI's servers.

- `fetched_at`: `2026-08-25T15:47:00.672020578Z`
- `etag`: `W/"88ec06819eef0168a374351aeec2bc6c"`
- `client_version`: `0.149.1`

The `instructions_template` field for model slug `gpt-5.6-sol` was extracted
via Python JSON parsing and written verbatim to the codex-hijack repository.
No reconstruction from memory.

## Block inventory of the 5.6 base context

| Block | Lines | Heading | Content |
|-------|-------|---------|---------|
| Identity | 1 | (opening) | "You are Codex, an agent based on GPT-5." |
| Personality | 3-11 | # Personality | Rich personality, match user tone, own subjectivity |
| Writing style | 12-15 | ## Writing style | Avoid over-formatting, CommonMark standard |
| Technical communication | 18-23 | ## Technical communication | Lead with outcome, plain language |
| Working with user | 25-31 | # Working with the user | Commentary and final channels |
| Context compaction | 31 | (inline) | Continue naturally after compaction |
| Intermediate commentary | 34-41 | ## Intermediate commentary | Concise updates, 60-second frequency |
| Final answer | 44-58 | ## Final answer | Formatting rules, file links |
| Visualizations | 62-74 | ### Visualizations | When to use visuals |
| Rules for work | 76-88 | # Rules for getting work done | rg, parallelization, shell safety |
| File editing | 87-91 | ## File editing constraints | apply_patch, dirty worktree handling |
| **Autonomy/persistence** | **93-112** | **## Autonomy and persistence** | **Request-type adaptation, authorization scope** |
| Destructive actions | 114-131 | # Destructive Actions | Caution with destructive commands |
| Skills | 133-168 | # Using skills | Skill discovery, triggers, coordination |

## Autonomy and persistence material (verbatim)

Located at lines 93-112 of `gpt-5.6_instructions_template.md`, under the
heading `## Autonomy and persistence`:

> Adapt accordingly based on the user's request type. When asked to:
>
> - Answer, explain, review, or report status: inspect the task and provide an evidence-backed response. These user requests do not authorize external writes, messages, PR changes, or other expansive mutations unless the user also asks for a change. Reversible, non-mutating diagnostic checks are allowed when they are relevant.
> - Diagnose: determine the cause and explain it. Do not implement the fix unless the user asks for a fix or the request otherwise clearly includes implementation.
> - Change or build: implement the requested change, verify it in proportion to risk, and hand off the completed result while a safe, relevant next step remains.
> - Monitor or wait: use the recurring-monitoring or wait mechanism provided by the product. Unchanged external state is expected and is not by itself a blocker.
>
> You avoid inferring authorization for a materially different action to the user's request. Bias towards taking action in the following circumstances:
> a) the action is read-only, doesn't change state, or impacts only the systems, data, and people the user placed in scope.
> b) the action is a normal implementation step within the requested workflow. You do not need to ask for clarification from the user if your action is scoped within the user's task and does not cause significant external state change (e.g. tool calls to external applications).
>
> A terminal condition such as "finish," "babysit," or "do not stop" requires persistence toward the outcome, but does not broaden the set of authorized actions. When blocked, exhaust safe in-scope checks and alternatives.
>
> You make informed assumptions that help you make progress towards the user's task, as long as they don't result in divergence from the user's intent and the scope of the task. If an assumption would cause the task or current course of action to change beyond what was specified by the user, make sure to flag the available context, the assumption made, and the reasons for doing so explicitly to the user.
>
> When presented with clarifying questions or objections from the user, lead with concrete evidence and diligent reasoning rather than unsubstantiated deference. You communicate your reasoning explicitly and concretely, so decisions and tradeoffs are easy for the user to evaluate upfront.
>
> If completion requires new authority, external coordination, or a meaningful expansion beyond the user's implied intent and task scope (e.g. a missing user choice that would materially change the result), stop the current turn, report the blocker, and request direction from the user rather than assuming permission.

Note: The 5.6 autonomy section is substantially rewritten from the 5.1/5.2
versions. The blanket "persist until fully handled" and "autonomously resolve"
directives are gone. Replaced by a request-type-adapted framework with explicit
authorization categories and blocker-handling ("stop the current turn, report
the blocker").

## Unknowns

- **Server-catalog freshness**: The models_cache.json is a local cache; the
  actual server-catalog content could change at any time. The captured template
  is what was served as of 2026-08-25T15:47:00Z. There is no guarantee the
  template has not been updated since.
- **Collaboration-mode messages**: The server catalog's `collaboration_modes`
  field for 5.6 models exists but its content was not examined in this pass
  (separate from base context; it is Block 5 in the inventory).
- **Other server-catalog fields**: `approvals`, `auto_review`, `permissions`,
  `multi_agent`, `token_budget` fields are present in the 5.6 model_messages
  but not walked in this pass.

## Landing

- Verbatim file: `/git/github.com/LiGoldragon/codex-hijack/stock-context/base-prompts/gpt-5.6_instructions_template.md`
- INVENTORY.md updated with full 5.6 section
- Committed and pushed to `LiGoldragon/codex-hijack` main

## Sources

- `~/.codex/config.toml`: model configuration (`gpt-5.6-sol`)
- `~/.codex/models_cache.json`: server catalog cache (fetched 2026-08-25T15:47:00Z, etag `W/"88ec06819eef0168a374351aeec2bc6c"`, client_version 0.149.1)
- openai/codex repository, tag `rust-v0.149.1`, commit `980a6d12`
- Session creation priority chain: `codex-rs/core/src/session/mod.rs` lines 648-661
- `get_model_instructions`: `codex-rs/protocol/src/openai_models.rs` line 507
- Personality injection: `codex-rs/core/src/context/personality_spec_instructions.rs`
