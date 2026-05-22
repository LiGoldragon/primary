# 281 - Headless Pi research

*Investigation into whether Pi (Mario Zechner's `pi-coding-agent`,
now distributed as `@earendil-works/pi-coding-agent`) has a
headless / library / programmatic mode, and whether that mode
captures the I/O surface needed to integrate DeepSeek (and other
LLMs) into a "reusable library" shape per the psyche's
2026-05-22 direction. Designer lane; dispatched under the
parallel-subagents authorisation (psyche 2026-05-21).*

> **2026-05-22 update — wrapping decisions (post-research intent):**
> This report's TL;DR recommendation ("depend on `@earendil-works/pi-ai`
> directly") and §3 integration-shape sketch are SUPERSEDED by
> psyche corrections.
>
> Three distinct workspace concerns crystallised after this report:
>
> 1. **`persona-llm-client`** (spirit records 152 supersedes 151;
>    158): workspace-native lightweight LLM client library, Rust,
>    daemon-embeddable, talks DeepSeek/OpenAI-compatible APIs
>    directly. No Pi dependency. This is the workspace's LLM-call
>    layer. Bead `primary-lyc8` (PARKED).
> 2. **Rust RPC wrapper for headless Pi** (spirit record 175,
>    Medium): build a Rust client for Pi's `--mode rpc` (the
>    headless mode this report documents in §1.2) as a useful
>    baseline. This is for Pi-as-agent-runtime calls, NOT for LLM
>    calls. Open question: standalone library, part of persona-pi,
>    or part of persona-llm-client? Carried by bead `primary-u7gc`
>    pending clarification.
> 3. **`persona-pi` triad** (per /266): full Pi harness adaptation
>    with dual-path (terminal-cell + harness API). Distinct from
>    the Rust RPC wrapper; the triad is the workspace-shaped wrapper
>    of the full agent loop. Bead `primary-u7gc`.
>
> The findings in §1-§2 of this report on headless-Pi modes and
> capture surface remain valid as reference. The integration
> recommendation in §3 ("depend on pi-ai directly") should be
> read against the new three-concern split above, not taken as
> the workspace path.

## TL;DR

**Yes — headless Pi exists, and twice over.** Pi ships four
operational modes; two are headless. **(a) RPC mode** speaks
LF-delimited JSONL on stdin/stdout — language-agnostic, suitable
for non-Node callers. **(b) SDK mode** is a TypeScript/Node import
(`createAgentSession`, `AgentSession`) — direct in-process embedding.
**All five capture targets** (inputs, outputs, tool calls, tool
results, full inference trace) are first-class on both surfaces;
DeepSeek is already a supported provider via the shared `pi-ai`
unified LLM API. The recommended path for "DeepSeek as a reusable
library" is to depend on `@earendil-works/pi-ai` directly if pure
LLM-call reuse is wanted, or on `@earendil-works/pi-coding-agent`'s
SDK (Node) / RPC (any language) if the agent loop is wanted too.

## §1 Does headless Pi exist?

**Yes. Headless Pi is a documented, first-class mode pair.**

Pi's coding agent ships **four operational modes**:

| Mode | Invocation | Shape |
|---|---|---|
| Interactive | `pi` | Full TUI; psyche-at-keyboard |
| Print | `pi -p "prompt"` | Single-shot CLI, text-out, exits |
| RPC | `pi --mode rpc` | Headless. JSONL over stdin/stdout |
| SDK | `import { createAgentSession }` | Headless. Direct Node embedding |

The two headless modes are RPC and SDK. They are not afterthoughts —
each has dedicated documentation (`docs/rpc.md`, `docs/sdk.md`),
explicit factory entry points, and stable event surfaces.

### 1.1 SDK entry point (Node/TypeScript)

The canonical SDK shape (from `docs/sdk.md`):

```typescript
import {
  createAgentSession,
  SessionManager,
  AuthStorage,
  ModelRegistry,
} from "@earendil-works/pi-coding-agent";

const { session } = await createAgentSession({
  model: myModel,
  tools: ["read", "bash"],
  sessionManager: SessionManager.inMemory(),
});

session.subscribe((event) => { /* ... */ });
await session.prompt("What files are here?");
```

`createAgentSession` is the **main factory**; `AgentSession` is
the runtime object. Source under `src/core/agent-session.ts`.

### 1.2 RPC entry point (any language)

The RPC mode opens `pi --mode rpc` as a subprocess and speaks
strict JSONL (LF-delimited) over stdin/stdout. Commands and
responses are JSON objects; events stream in real time.

```python
proc = subprocess.Popen(
    ["pi", "--mode", "rpc", "--no-session"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
)
proc.stdin.write(json.dumps({"type": "prompt", "message": "..."}) + "\n")
proc.stdin.flush()
for line in proc.stdout:
    event = json.loads(line)
    # dispatch on event.type
```

### 1.3 Package identity correction

Prior workspace research (`reports/designer/pi-api-surface-notes.md`)
cited the package as `@mariozechner/pi-coding-agent`. **The
canonical npm package is `@earendil-works/pi-coding-agent`.** The
GitHub canonical name is `earendil-works/pi` (formerly
`badlogic/pi-mono`; the old URL redirects). Mario remains the
primary author; Earendil Works is the publishing org. Future
references should use the `@earendil-works/` scope.

### 1.4 Monorepo structure

Pi is `pi-mono`, a monorepo. Four packages relevant here:

- **`@earendil-works/pi-coding-agent`** — the agent CLI + SDK
- **`@earendil-works/pi-agent-core`** — agent runtime (tool calling, state)
- **`@earendil-works/pi-ai`** — unified multi-provider LLM API
- **`@earendil-works/pi-tui`** — terminal UI library

The split matters for the integration shape (see §3): `pi-ai` is a
**standalone unified LLM client** that can be depended on without
pulling in the agent loop.

## §2 Capture surface

For each of the five capture targets, headless Pi exposes the
following.

### 2.1 Inputs (prompts, tool definitions, system messages)

**Available.** Multiple paths:

- **Prompts** — pass to `session.prompt(text, options?)` (SDK)
  or send `{"type":"prompt","message":"..."}` (RPC).
  Supports image payloads via `images` field.
- **Tool definitions** — passed at session creation as
  `tools: ["read","bash",...]` (built-ins) or `customTools: [...]`
  via `defineTool({name, description, parameters, execute})`.
  TypeBox schemas; same shape as Pi extensions.
- **System prompt** — overridable via
  `new DefaultResourceLoader({systemPromptOverride: () => "..."})`
  passed as `resourceLoader` to `createAgentSession`.
- **Resources / skills** — `DefaultResourceLoader` discovers and
  injects `cwd`/`agentDir` resources; can be configured or
  bypassed entirely.

**Evidence**: `docs/sdk.md` "Custom Tools" section;
`createAgentSession` options table; `DefaultResourceLoader`
export.

### 2.2 Outputs (agent text content)

**Available, streaming.** Subscribe to `message_update` events
and dispatch on `assistantMessageEvent.type`:

- `text_start` / `text_delta` / `text_end` — assistant text
- `thinking_start` / `thinking_delta` / `thinking_end` —
  reasoning/thinking tokens (when thinking level enabled)
- `toolcall_start` / `toolcall_delta` / `toolcall_end` — tool-use
  block deltas
- `start` / `done` / `error` — message lifecycle

Bulk recovery: `{"type":"get_last_assistant_text"}` (RPC) or
`session.messages` (SDK).

### 2.3 Commands (tool calls — names, arguments)

**Available.** The `tool_execution_start` event carries:

```json
{
  "type": "tool_execution_start",
  "toolCallId": "call_abc123",
  "toolName": "bash",
  "args": {"command": "ls -la"}
}
```

`toolName` and `args` are both first-class. The matching
`toolcall_start`/`toolcall_delta`/`toolcall_end` deltas inside
`message_update` give the model's tool-use blocks at the
streaming level.

### 2.4 Command outputs (tool results)

**Available, streaming + final.**

- `tool_execution_update` — streaming partial output during
  execution (`partialResult.content`).
- `tool_execution_end` — final result (`result.content`,
  `isError`).
- `ToolResultMessage` in the message history carries
  `toolCallId` (links to the call), `content`, and `isError`.

### 2.5 Full inference trace (LLM reasoning, all turns, all messages)

**Available, comprehensive.** Three complementary surfaces:

- **Per-event streaming**: `message_update` with
  `text_delta`/`thinking_delta`/`toolcall_delta` deltas during
  generation; `turn_start`/`turn_end` bracketing each
  LLM-call+tool-cycle pair; `agent_start`/`agent_end` bracketing
  the entire run.
- **Bulk recovery**: `{"type":"get_messages"}` (RPC) or
  `session.messages` (SDK) returns the entire conversation:
  - `UserMessage` — user prompts
  - `AssistantMessage` — model responses with thinking, text,
    and tool-call content blocks; includes `usage`
    (token counts), `stopReason`, `model`, `provider`, `api`
  - `ToolResultMessage` — tool execution results
  - `BashExecutionMessage` — direct bash executions
- **Session statistics**: `{"type":"get_session_stats"}` returns
  cumulative token counts (input/output/cacheRead/cacheWrite/total),
  cost, and context usage.

**The `AssistantMessage.content` array includes thinking blocks
alongside text and tool-call blocks**, which gives a faithful
reconstruction of the LLM reasoning chain at the message level.
Token-level streaming is available through the `thinking_delta`
delta type during generation.

### 2.6 Summary table

| Target | Status | Primary mechanism |
|---|---|---|
| Inputs (prompts, tools, system) | Available | `createAgentSession` options + `prompt()` |
| Outputs (text content) | Available | `message_update.text_delta` / `session.messages` |
| Commands (tool calls) | Available | `tool_execution_start` / `toolcall_*` deltas |
| Command outputs (tool results) | Available | `tool_execution_end` / `ToolResultMessage` |
| Inference trace (all messages) | Available | `get_messages` / `session.messages` |

All five targets are **first-class, documented, and available
without adaptation**. No "Available with adaptation" or "Not
available" cells.

## §3 Integration shape

Two distinct integration shapes are available depending on what
"reusable library" means concretely. The psyche statement —
"integrate DeepSeek calls into, make it like a easily reusable
library. Like, well, I guess we would use Pi for that. Because
you'd still want to harness and Pi just gives it to us." —
clearly wants the **harness path** (the agent loop), not pure
LLM-call reuse. Both options are sketched.

### 3.1 Option A — `pi-ai` direct (pure LLM client)

If the goal is "wrap a unified LLM client for DeepSeek + others"
with no agent loop, the cleanest dependency is
`@earendil-works/pi-ai` directly:

```typescript
import { ... } from "@earendil-works/pi-ai";
// One unified completion API; DeepSeek is a supported provider
// via DEEPSEEK_API_KEY + OpenAI-compatible base URL auto-detect.
```

DeepSeek is already a known provider in `pi-ai`; the library
auto-detects compatibility settings from `baseUrl` for known
OpenAI-compatible providers including DeepSeek. Auth via
`DEEPSEEK_API_KEY`.

**Pros**: smaller surface; no agent state to manage; works for
plain completion + tool-calling use cases.
**Cons**: no agent loop, no streaming-with-tool-execution, no
session persistence, no skill/resource layer. The psyche
explicitly said "you'd still want to harness" — this option
discards the harness.

### 3.2 Option B — `pi-coding-agent` SDK (in-process)

The psyche-leaning option. Embed Pi's `AgentSession` directly:

```typescript
import {
  createAgentSession,
  SessionManager,
  defineTool,
} from "@earendil-works/pi-coding-agent";
import { Type } from "@sinclair/typebox";

// 1. Configure the model (DeepSeek)
const model = await registry.getModel("deepseek", "deepseek-v4-pro");

// 2. (Optional) declare custom tools
const lookupTool = defineTool({
  name: "lookup",
  description: "Look up a value",
  parameters: Type.Object({ key: Type.String() }),
  async execute(toolCallId, params) {
    return {
      content: [{ type: "text", text: `value for ${params.key}` }],
      details: {},
    };
  },
});

// 3. Start the session
const { session } = await createAgentSession({
  model,
  tools: ["read", "bash"],
  customTools: [lookupTool],
  sessionManager: SessionManager.inMemory(),
});

// 4. Subscribe to capture EVERYTHING
const captured = {
  prompts: [] as string[],
  text: [] as string[],
  thinking: [] as string[],
  toolCalls: [] as Array<{name: string; args: unknown}>,
  toolResults: [] as Array<{name: string; result: unknown; error: boolean}>,
  messages: null as unknown,
};

session.subscribe((event) => {
  switch (event.type) {
    case "message_update": {
      const ev = event.assistantMessageEvent;
      if (ev.type === "text_delta") captured.text.push(ev.delta);
      else if (ev.type === "thinking_delta")
        captured.thinking.push(ev.delta);
      break;
    }
    case "tool_execution_start":
      captured.toolCalls.push({ name: event.toolName, args: event.args });
      break;
    case "tool_execution_end":
      captured.toolResults.push({
        name: event.toolName,
        result: event.result,
        error: event.isError,
      });
      break;
    case "agent_end":
      captured.messages = event.messages;
      break;
  }
});

// 5. Run
captured.prompts.push("Summarise this directory.");
await session.prompt("Summarise this directory.");

// 6. `captured` now holds the full I/O surface for this turn.
```

**Pros**: full agent loop including tool execution, streaming,
multi-turn; explicit subscription to every capture target;
in-process Node speed; sub-agent-friendly (multiple sessions in
the same Node runtime).
**Cons**: Node-only; pulls in the entire coding-agent dependency
tree; bundles built-in tools (`read`, `bash`, etc.) that the
caller may or may not want active.

### 3.3 Option C — `pi-coding-agent` RPC (subprocess, language-agnostic)

If the caller isn't Node — Rust, Python, etc. — the RPC mode is
the contract:

```rust
// Sketch — Rust child process driving Pi's RPC mode
let mut child = Command::new("pi")
    .args(["--mode", "rpc", "--no-session"])
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .spawn()?;

let stdin = child.stdin.as_mut().unwrap();
writeln!(stdin, r#"{{"type":"prompt","message":"Summarise"}}"#)?;

let stdout = BufReader::new(child.stdout.as_mut().unwrap());
for line in stdout.lines() {
    let event: Value = serde_json::from_str(&line?)?;
    match event["type"].as_str() {
        Some("message_update") => { /* text_delta / thinking_delta */ }
        Some("tool_execution_start") => { /* name + args */ }
        Some("tool_execution_end") => { /* result + isError */ }
        Some("agent_end") => break,
        _ => {}
    }
}
```

**Pros**: works from any language; process isolation; natural fit
for the workspace's Rust-via-NOTA discipline.
**Cons**: per-prompt subprocess startup cost (unless reused);
JSON encoding/decoding overhead; loses TypeBox tool-definition
ergonomics (custom tools need to come from extension files on
disk loaded by Pi, not from the calling language directly — the
RPC mode does not let the parent process register tools over the
wire).

### 3.4 Seams the integration must own

For any of the three shapes:

- **Auth** — `AuthStorage` (SDK) or env vars + `~/.pi/agent/`
  config (RPC). DeepSeek wants `DEEPSEEK_API_KEY`.
- **Model selection** — `ModelRegistry.getModel(provider,
  model)` or `setModel(...)`. DeepSeek models live in the
  registry; the integration must pick a stable identifier.
- **Tool surface** — decide which Pi built-ins (`read`, `bash`,
  `edit`, `write`, `grep`, `find`, `ls`) stay active. Library
  callers may want `tools: []` and only custom tools.
- **System prompt** — Pi ships a ~1000-token default; library
  callers should consider overriding via `systemPromptOverride`.
- **Session lifecycle** — `SessionManager.inMemory()` for
  pure-library use; `SessionManager.create(cwd)` for
  persistence-to-disk.

## §4 Open questions / unknowns

The following could not be settled from public sources and are
either try-it-and-see or require psyche input.

### 4.1 Custom-tool registration over RPC

Could not confirm whether the RPC mode lets the parent process
register custom tools dynamically, or whether custom tools must
be declared as Pi extensions on disk and loaded by Pi at startup.
The Node SDK clearly supports in-process custom tools via
`defineTool` + `customTools`. The RPC contract appears not to
have a `register_tool` command. **For Rust-side workspace
integration where tools need to be the workspace's own typed
Signal verbs, this is decisive — try-it-and-see required.**

### 4.2 DeepSeek model identifier stability

`pi-ai` supports DeepSeek and the changelog mentions "V4
Flash/Pro models" — but the canonical model IDs as registered in
Pi's `ModelRegistry` were not confirmed verbatim. Integration
code that depends on a specific identifier should consult
`~/.pi/agent/models.json` or call `ModelRegistry.list()` at
runtime; don't hard-code.

### 4.3 Headless print-mode vs RPC-mode capture parity

Pi's print mode (`pi -p "..."`) and JSON mode (`pi --mode json`)
also stream output, but were not investigated in detail. RPC
mode is the documented headless interface; JSON mode appears to
be a one-way stream-events variant. Whether JSON mode offers any
capture target RPC mode does not is undetermined.

### 4.4 What the "reusable library" surface looks like in the workspace

The psyche said "make it like a easily reusable library" — this
report shows Pi is the substrate, but the *shape* of the
workspace's wrapping library (Rust crate? Nix-flake-built
binary? Signal-tree contract?) is open. Three candidates worth
naming:

- **A Rust crate** that spawns `pi --mode rpc` as a subprocess
  and presents a typed NOTA-shaped API. Natural fit for the
  Rust subset.
- **A Node library** that re-exports `createAgentSession` with
  workspace-shaped defaults (custom system prompt, no built-in
  tools, DeepSeek pre-configured). Cheaper, but adds a Node
  surface the workspace otherwise avoids.
- **A `signal-deepseek` triad** where the daemon embeds Pi's RPC
  subprocess and the signal contract exposes typed prompt /
  reply / tool-call payloads. Heaviest, but aligns with
  workspace component-triad discipline.

**Psyche input wanted on which shape is the target.** §3 of this
report has not picked one; the integration sketches are
illustrative for each option's seam set.

### 4.5 Relationship to persona-pi (existing design)

`reports/designer/266-persona-pi-triad-design.md` describes a
**persona-pi triad** with dual-path (terminal-cell + harness-API)
communication. That design assumed adapting Pi as a persona
component for the composite-designer flow. **The
DeepSeek-as-library direction is a different use case** — pure
library reuse, not persona-system composition. Whether persona-pi
and any DeepSeek-library should share a substrate, share the
RPC-mode spawning code, or live as independent integrations is
psyche-decidable. Designer lean: persona-pi is upstream of more
specific consumers; a DeepSeek-library could sit on top of
persona-pi, or be a sibling. **Not settled.**

### 4.6 Cost / token tracking under heavy library use

`get_session_stats` returns aggregate token counts and cost.
Whether this is per-session-only or whether per-call cost can be
extracted from individual `agent_end` events for fine-grained
attribution was not verified. Important if the workspace bills
or budgets per-prompt rather than per-session.

## See also

- **Pi SDK docs** —
  <https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/sdk.md>
- **Pi RPC docs** —
  <https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md>
- **Pi coding-agent README** —
  <https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md>
- **Pi monorepo** —
  <https://github.com/earendil-works/pi> (canonical;
  `badlogic/pi-mono` redirects)
- **pi-ai package** —
  <https://github.com/earendil-works/pi/tree/main/packages/ai>
- **DeepWiki: pi-coding-agent** —
  <https://deepwiki.com/badlogic/pi-mono/4-@mariozechnerpi-coding-agent>
- **DeepWiki: RPC mode** —
  <https://deepwiki.com/badlogic/pi-mono/4.5-rpc-mode>
- **Issue #272 (Agent SDK equivalent discussion)** —
  <https://github.com/badlogic/pi-mono/issues/272>
- **Prior workspace research** —
  `reports/designer/pi-api-surface-notes.md`
  (extension API surface; package scope is corrected to
  `@earendil-works/` by this report);
  `reports/designer/266-persona-pi-triad-design.md`
  (persona-pi triad, separate use case);
  `reports/designer/268-persona-pi-operator-input.md`
  (operator brief on persona-pi);
  `reports/second-system-assistant/3-mario-zechner-ai-agent-points.md`
  (Pi's why).

This report stands as the headless-Pi reference for the workspace.
It retires when (a) the psyche picks one of §4.4's three library
shapes and the operator opens implementation, OR (b) the
custom-tool-over-RPC unknown (§4.1) is resolved by a try-it-and-see
test and the report is superseded by a successor citing the
verified behaviour.
