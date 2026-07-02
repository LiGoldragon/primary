# Codex Child Runtime Situational Map

## Task And Scope

Read-only local inspection requested: determine whether the Codex harness/subagent API is designed to let a parent set a child agent's `model` and `reasoning_effort`, and whether local evidence shows the effective child runtime can differ from requested fields. Inspected only local tool/source/config surfaces under `/git/github.com/openai/codex`, `/home/li/.codex`, and `/home/li/primary/.codex`. No web browsing. No tests run.

## Commands Consulted

- `spirit "(PublicTextSearch [Codex subagent model reasoning_effort spawn_agent])"`: returned public intent records `n9fl` and `w312`, both broadly about agent-system direction/mechanism boundaries; no direct runtime-schema directive.
- `rg --files /git/github.com/openai/codex /home/li/.codex /home/li/primary/.codex`
- `rg -n "spawn_agent|reasoning_effort|reasoning effort|model" ...`
- Targeted `nl -ba ... | sed -n ...` reads of source/schema files listed below.

## Observed Facts

- The multi-agent v2 spawn handler accepts `model: Option<String>` and `reasoning_effort: Option<ReasoningEffort>` in `SpawnAgentArgs`: `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs:214-222`.
- The older multi-agent spawn handler accepts the same fields: `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs:184-190`.
- The spawn handlers emit a begin event using the requested fields or defaults: v2 at `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs:49-57`, v1 at `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs:49-58`.
- Requested overrides are applied by `apply_requested_spawn_agent_model_overrides`: it sets `config.model` and either requested or default reasoning effort for the selected model, or validates/sets reasoning effort against the current model when only effort is requested: `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:288-337`.
- Full-history forked agents reject `agent_type`, `model`, and `reasoning_effort` overrides and must inherit them: `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:241-249`.
- The v2 spawn tool description test states spawned agents inherit the current model by default and `model` should be set only for explicit override: `/git/github.com/openai/codex/codex-rs/core/src/tools/spec_tests.rs:720-728`.
- The child config starts from the parent turn's effective config/runtime state, including `turn.model_info.slug` and `turn.reasoning_effort` or model default, not merely static config: `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:198-238`.
- Runtime-only values such as approval policy, shell environment policy, sandbox executable, cwd, and permission profile are copied from the live turn to the child config: `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs:254-279`.
- After spawn, both v1 and v2 handlers query `get_agent_config_snapshot` for the new thread and use snapshot `model` and `reasoning_effort` in the spawn-end event when available, falling back to requested fields only if no snapshot exists: v2 at `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs:139-170` and `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs:172-184`; v1 at `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs:119-150` and `/git/github.com/openai/codex/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs:152-164`.
- `get_agent_config_snapshot` is a real `AgentControl` read of the live thread's config snapshot: `/git/github.com/openai/codex/codex-rs/core/src/agent/control.rs:783-794`.
- App-server thread history stores collab spawn begin/end events as `ThreadItem::CollabAgentToolCall` with `model` and `reasoning_effort` fields: `/git/github.com/openai/codex/codex-rs/app-server-protocol/src/protocol/thread_history.rs:603-618` and `/git/github.com/openai/codex/codex-rs/app-server-protocol/src/protocol/thread_history.rs:621-652`.
- Generated TypeScript schema documents these fields as requested fields for the spawned agent: `model: string | null` and `reasoningEffort: ReasoningEffort | null`: `/git/github.com/openai/codex/codex-rs/app-server-protocol/schema/typescript/v2/ThreadItem.ts:64-101`.
- Thread start/resume responses expose thread runtime metadata for that session: `model`, `modelProvider`, `serviceTier`, `cwd`, `instructionSources`, `approvalPolicy`, `approvalsReviewer`, `sandbox`, and `reasoningEffort`: `/git/github.com/openai/codex/codex-rs/app-server-protocol/schema/typescript/v2/ThreadStartResponse.ts:12-23` and `/git/github.com/openai/codex/codex-rs/app-server-protocol/schema/typescript/v2/ThreadResumeResponse.ts:12-23`.
- The `Thread` metadata itself includes `modelProvider` but not a `model` or `reasoningEffort` field in the read segment checked: `/git/github.com/openai/codex/codex-rs/app-server-protocol/schema/typescript/v2/Thread.ts:10-40`.
- A turn-context model switch can change reasoning effort when the current effort is unsupported by the new model, selecting a middle supported effort or the model default: `/git/github.com/openai/codex/codex-rs/core/src/session/turn_context.rs:141-172`.
- Role configs can lock model and reasoning effort; the spawn tool spec annotates such roles as not changeable: `/git/github.com/openai/codex/codex-rs/core/src/agent/role.rs:308-345`; test evidence at `/git/github.com/openai/codex/codex-rs/core/src/agent/role_tests.rs:720-741`.
- Installed global config requests `model = "gpt-5.5"` and `model_reasoning_effort = "medium"` for this environment: `/home/li/.codex/config.toml:1-5`.
- Installed workspace agent role files under `/home/li/primary/.codex/agents/*.toml` are role packets with `name`, `description`, and large `developer_instructions`; scoped search did not find top-level per-agent `model = ...` or `model_reasoning_effort = ...` outside embedded doctrine text. This is weak negative evidence because the TOML values are huge single-line strings and the search output truncates.

## Interpretations

1. Yes, the `spawn_agent` tool schema/handler surface is designed to allow a parent to request child `model` and `reasoning_effort` overrides, subject to mode and validation constraints. The strongest local evidence is the deserialized args structs and the override application function.
2. Yes, there is evidence that effective child runtime can differ from requested fields. The spawn-end event intentionally reports snapshot-derived `effective_model` and `effective_reasoning_effort` when the live child thread exists, not just the args. Also, model switches can adjust unsupported reasoning effort, full-history forks reject overrides, and role configs can lock model/effort.
3. The child session exposes effective runtime metadata at thread start/resume response surfaces. Parent-visible collab history also exposes model/effort on spawn tool-call items, and spawn-end is sourced from the child config snapshot when possible. I did not find evidence in the checked `Thread` object itself for persistent `model` or `reasoningEffort` fields.

## Direct Answers

1. Does the `spawn_agent` tool schema expose model and reasoning_effort overrides? Yes. Local handler schemas accept both `model` and `reasoning_effort`; generated thread-item schema records model/reasoning effort for spawn calls. Overrides are not universally accepted: full-history forks reject them, and role/model validation can constrain them.
2. Does the child session itself expose effective runtime metadata? Yes for session start/resume responses: they include effective `model` and `reasoningEffort`. Parent-visible spawn completion also reports model/effort from a live child config snapshot when available. The base `Thread` metadata checked does not itself include model/reasoning effort.
3. What should the parent report to avoid overclaiming? Report requested fields separately from observed/effective fields. Say "requested `model=X`, `reasoning_effort=Y` via `spawn_agent`" unless the parent has spawn-end/thread-start/thread-resume metadata showing the effective runtime. When available, say "effective child runtime reported by Codex was `model=X`, `reasoningEffort=Y`." Do not claim the child actually ran with requested values solely from the tool arguments.

## Unknowns And Not Checked

- Did not inspect private/auth files such as `/home/li/.codex/auth.json`.
- Did not run Codex tests or spawn a live child agent.
- Did not inspect session logs as evidence because they are noisy and may contain private runtime material.
- Did not inspect remote docs or browse the web by request.
