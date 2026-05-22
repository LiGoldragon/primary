# Pi API Surface Notes

Research feed for the parallel persona-pi triad design report (`/266`).
Grounds that report in Pi's actual extension surface so the triad
adaptation is principled, not invented. Date: 2026-05-21. Designer lane.

> **2026-05-22 correction:** Package scope is `@earendil-works/`
> (GitHub canonical: `earendil-works/pi`), **not** `@mariozechner/`
> as referenced below. Mario Zechner is still the author; the
> package was moved to the `earendil-works` org and the monorepo
> split into `pi-coding-agent`, `pi-agent-core`, `pi-ai`, `pi-tui`.
> The `pi-ai` package can be depended on standalone for pure
> LLM-call reuse without the agent loop. See
> `reports/designer/281-headless-pi-research.md` for the full
> research (including documented headless RPC + SDK modes and
> pi-ai's DeepSeek auto-detect).

## What Pi is

**High confidence**: Pi is the open-source coding-agent harness by
Mario Zechner, packaged as `pi-mono` (npm:
`@mariozechner/pi-coding-agent`; domain `pi.dev`). Not Inflection AI's
Pi chatbot.

Prior workspace research on Mario's broader thesis covers *why* Pi
exists (see `reports/second-system-assistant/3-mario-zechner-ai-agent-points.md`);
this report covers *what* the API looks like.

Design philosophy (per docs and Mario's retrospective): maximum
extensibility around a minimum core — four built-in tools, a system
prompt under ~1000 tokens, no built-in plan mode, MCP, subagents, or
background processes. Everything beyond that lives in TypeScript
extensions, skills, prompt templates, and themes, distributed as
"Pi packages" via npm or git.

## Pi's API surface

### Built-in tools

Flat snake_case namespace callable by the model: `read`, `write`,
`edit`, `bash`. (Docs also mention `grep`, `find`, `ls`, `user_bash`
as widely-used names; the four above are the canonical core.)

### Extension entrypoint

Every Pi extension is a TypeScript module whose default export (which
may be `async`) receives a single `ExtensionAPI` argument named `pi`
by convention. State lives as ordinary closure variables — no
harness-provided state container.

```typescript
export default function (pi: ExtensionAPI) {
  pi.registerTool({ ... });
  pi.registerCommand("stats", { ... });
  pi.on("tool_call", async (event, ctx) => { ... });
}
```

### ExtensionAPI methods (the `pi.*` flat surface)

All methods sit directly on a single `pi` object. Grouped here for
reading clarity only.

- Tools: `pi.registerTool(definition)`, `pi.getAllTools()`,
  `pi.getActiveTools()`, `pi.setActiveTools(names)`.
- Messages / session: `pi.sendMessage()`, `pi.sendUserMessage()`,
  `pi.appendEntry(customType, data?)`.
- Commands / shortcuts / flags: `pi.registerCommand(name, options)`,
  `pi.registerShortcut(shortcut, options)`,
  `pi.registerFlag(name, options)`, `pi.getCommands()`.
- UI / rendering: `pi.registerMessageRenderer(customType, renderer)`.
- Model / providers: `pi.setModel(model)`, `pi.registerProvider()`,
  `pi.unregisterProvider()`, `pi.getThinkingLevel()`,
  `pi.setThinkingLevel(level)`.
- Execution / session metadata: `pi.exec(command, args, options?)`,
  `pi.setSessionName()`, `pi.getSessionName()`, `pi.setLabel()`.
- Events: `pi.on(event, handler)` (lifecycle subscription),
  `pi.events` (shared inter-extension event bus).

### Event surface (what `pi.on` listens to)

- Lifecycle: `session_start`, `session_shutdown`,
  `session_before_switch`, `session_before_fork`,
  `session_before_compact`, `session_compact`,
  `session_before_tree`, `session_tree`, `resources_discover`.
- Agent loop: `before_agent_start`, `agent_start`, `agent_end`,
  `turn_start`, `turn_end`.
- Messages: `message_start`, `message_update`, `message_end`.
- Tools: `tool_call`, `tool_result`, `tool_execution_start`,
  `tool_execution_update`, `tool_execution_end`.
- Input / model: `input`, `user_bash`, `model_select`,
  `thinking_level_select`.
- Provider: `before_provider_request`, `after_provider_response`,
  `context`.

### Tool registration concrete shape

```typescript
pi.registerTool({
  name: "greet",
  label: "Greet",
  description: "Greet someone by name",
  parameters: Type.Object({
    name: Type.String({ description: "Name to greet" }),
  }),
  async execute(toolCallId, params, signal, onUpdate, ctx) {
    return {
      content: [{ type: "text", text: `Hello, ${params.name}!` }],
      details: {},
    };
  },
});
```

`name` is snake_case by convention; `label` is human-facing display;
`parameters` uses TypeBox schemas; `execute` returns
`{ content, details }`.

### The shared-state canonical example (highly relevant)

The docs' canonical multi-tool extension shape — three sibling tools
that close over a shared connection:

```typescript
export default function (pi: ExtensionAPI) {
  let connection = null;
  pi.registerTool({ name: "db_connect", ... });
  pi.registerTool({ name: "db_query", ... });
  pi.registerTool({ name: "db_close", ... });
  pi.on("session_shutdown", async () => {
    connection?.close();
  });
}
```

This is the prototype Mario uses to teach the model that a tool with
held resources lives as multiple flat sibling tools, coordinated by
closure state and a `session_shutdown` hook. **Almost certainly what
the psyche was verbally referencing.**

## The "query negative database from behind" reference

**Most likely**: STT mangling of the canonical `db_query` example.
The verbal phrase decomposes onto Pi's docs:

- "query" -> `db_query`
- "database" -> `db_` prefix
- "from behind" -> STT misrender of "db_" or background filler
- "negative" -> almost certainly STT garbling; no real Pi tool name
  contains "negative". Candidates the psyche may actually have said:
  "the *example* database", "the *extensions* docs" example.

Secondary candidate (low probability): a third-party extension (e.g.
`jayshah5696/pi-agent-extensions`, `can1357/oh-my-pi`). No direct
evidence; the docs example matches the verbal shape closely enough
to take as the working hypothesis.

**Recommendation for `/266`**: cite `db_connect`/`db_query`/`db_close`
as the canonical Pi example and the likely referent. Don't quote
"query_negative_database_from_behind" as if it were a real Pi
function. Ask the psyche if it matters.

## Concrete flat-function namespace examples

Pi-style names that a triad design will want to translate into a
typed Nota record tree:

- Built-ins: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`.
- Shared-state docs example: `db_connect`, `db_query`, `db_close`.
- Dynamic-tools docs example: `reload_runtime`.
- Observable extension tool names (from the 70+ examples in
  `packages/coding-agent/examples/extensions/`): `web_search`,
  `notify`, `bookmark`, `handoff`, `auto_commit_on_exit`,
  `confirm_destructive`, `dirty_repo_guard`, `protected_paths`,
  `permission_gate`, `git_checkpoint`, `inline_bash`,
  `github_issue_autocomplete`, `trigger_compact`, `summarize`,
  `interactive_shell`, `subagent`, `plan_mode`, `prompt_customizer`,
  `model_status`, `working_indicator`, `status_line`, `minimal_mode`,
  `mac_system_theme`, `snake`, `tic_tac_toe`, `space_invaders`,
  `doom_overlay`.

## Where Pi diverges from workspace discipline

1. **Flat tool namespace vs typed-noun records.** Pi's universe is a
   single bag of snake_case tool names — `db_connect`, `db_query`,
   `db_close` are siblings, not methods on a `Database` noun. The
   workspace's "methods on nouns" discipline (`ESSENCE.md`,
   `skills/component-triad.md`) puts the noun first and the verb on
   it. **The primary design fork**: does persona-pi mirror Pi's flat
   verbs, or rebuild them as methods on triad nouns?

2. **`pi.*` flat method bag vs typed record API.** The ExtensionAPI
   itself is the same flat-method shape: `pi.registerTool`,
   `pi.setModel`, `pi.exec`, `pi.events` are peer methods on one
   object. Workspace discipline would split these onto distinct
   nouns — `ToolRegistry`, `ModelSelector`, `EventBus`, etc.
   Translation isn't mechanical: `setSessionName`/`getSessionName`
   is obviously a `Session` noun; `appendEntry` sits awkwardly.

3. **Closure state vs typed signal types.** Pi's idiom is
   TypeScript closure variables (`let connection = null`). The
   workspace component-triad discipline keeps state in typed records
   passing through daemon + working-signal + owner-signal. A
   persona-pi triad must choose where Pi-extension closure state
   lands — typed signal payload, daemon-side persistent record, or
   in-process adapter bridging Pi state into the signal shape.

4. **Single-argument NOTA rule vs free-form TypeScript.** Pi
   extensions take whatever TypeScript shape they want. Workspace
   component binaries take exactly one argument: a NOTA string, NOTA
   file path, or rkyv-encoded signal-file path. The surface Pi-style
   code calls into has to land cleanly on the single-argument
   contract.

5. **npm distribution vs Nix-flake + triad-flake.** Pi packages ship
   through npm; workspace components ship as Nix-flake-built daemons
   + CLIs. Either persona-pi's working surface stays in TypeScript
   and bridges to the triad over a socket, or persona-pi is a
   "Pi-shaped API exposed by a Nix-built daemon" rather than literal
   Pi extensions. The triad design must declare which.

6. **System prompt as user-owned text vs designer-owned protocol.**
   Pi puts the full system prompt within reach of every user as a
   <1000-token editable artifact. Workspace protocol/spirit
   discipline keeps that surface designer-owned and structured. Does
   persona-pi inherit Pi's "user sees and edits everything" stance
   or constrain it?

## Open psyche-clarification questions

1. **Was the psyche's verbal `db_query` reference the docs' canonical
   example or a specific third-party extension?** Working assumption:
   docs example. Confirm so `/266` quotes correctly.

2. **Does persona-pi mean "expose Pi's tool surface in our triad
   shape" or "embed Pi as the engine inside a triad and front it
   with a triad signal tree"?** Different designs.

3. **Flat-vs-typed-noun tension (divergence 1): mirror Pi's flat
   namespace so a Pi user feels at home, or translate to typed-noun
   methods so workspace discipline dominates?** Largest single fork.

4. **Are Pi extensions expected to be writable in TypeScript inside
   persona-pi, or will it only consume already-built Pi packages?**
   Affects whether the triad needs a TypeScript runtime leg.

5. **Should persona-pi cover Pi's full ExtensionAPI surface
   (commands, shortcuts, flags, providers, UI renderers, thinking
   level, event bus), or only tools-and-events?** Scope choice.

## Sources

- [Pi Coding Agent (pi.dev)](https://pi.dev/)
- [pi-mono on GitHub](https://github.com/badlogic/pi-mono)
- [Extensions docs](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md)
- [SDK docs](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/sdk.md)
- [Examples folder](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent/examples/extensions)
- [pi.dev extensions](https://pi.dev/docs/latest/extensions)
- [Mario's retrospective](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)
- [npm package](https://www.npmjs.com/package/@mariozechner/pi-coding-agent)
- Workspace prior research: `reports/second-system-assistant/3-mario-zechner-ai-agent-points.md`
