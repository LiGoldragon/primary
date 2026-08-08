# Pi RPC programmatic prompt research — 2026-06-07

## Question

The psyche asked whether Pi has an API that can programmatically send a session a prompt while it is working. This matters for the Persona message e2e: the current daemon proof routes through `message-daemon`, `router-daemon`, and `harness-daemon`, but the receiving "agent" is still a terminal endpoint. A real Pi-backed harness needs a programmatic intake surface.

## Verdict

Pi has a supported programmatic intake surface. The right first target is **Pi RPC mode** (`pi --mode rpc`), with **JSONL commands over stdin** and **events/responses over stdout**. For Node/TypeScript code, Pi also exposes the same session object through the SDK (`createAgentSession` / `AgentSession`).

The specific answer to "send a prompt while it is working" is:

- Send `{"type":"steer","message":"..."}` to queue steering while the agent is running. Pi delivers it after the current assistant turn finishes executing tool calls and before the next LLM call.
- Or send `{"type":"prompt","message":"...","streamingBehavior":"steer"}`. This is equivalent at the prompt-command level.
- Send `{"type":"follow_up","message":"..."}` to queue work only after the agent fully finishes.
- Use streamed events, `get_messages`, or `get_last_assistant_text` to observe replies.

This is not a remote HTTP API. It is a local process API over stdio, which is a good fit for Persona: the harness daemon can supervise an RPC Pi process, own its stdin/stdout, and translate router `MessageDelivery` into Pi `steer`/`follow_up` commands.

## Evidence

Local installed Pi docs:

- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:1` says RPC mode is headless operation over JSON stdin/stdout.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:9` starts it with `pi --mode rpc`.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:22` defines commands on stdin, responses and events on stdout.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:30` says framing is strict LF-delimited JSONL.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:56` says a streaming prompt must specify `streamingBehavior`.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:62` defines `steer`: queue while the agent is running, delivered after current tool execution and before the next LLM call.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:80` documents the explicit `steer` command.
- `/home/li/.local/share/criomos/pi/package/docs/rpc.md:102` documents `follow_up`.
- `/home/li/.local/share/criomos/pi/package/docs/sdk.md:5` says the SDK provides programmatic access for embedding Pi and automated workflows.
- `/home/li/.local/share/criomos/pi/package/docs/sdk.md:75` documents `AgentSession.prompt`.
- `/home/li/.local/share/criomos/pi/package/docs/sdk.md:79` documents `AgentSession.steer` and `AgentSession.followUp`.

Local source:

- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-types.ts:19` defines the RPC command union.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-types.ts:21` includes `prompt` with optional `streamingBehavior`.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-types.ts:22` includes `steer`.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-types.ts:23` includes `follow_up`.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-types.ts:91` defines `RpcSessionState`, including `isStreaming`, `pendingMessageCount`, and queue modes.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-client.ts:196` exposes `RpcClient.prompt`.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-client.ts:203` exposes `RpcClient.steer`.
- `/home/li/.local/share/criomos/pi/package/src/modes/rpc/rpc-client.ts:210` exposes `RpcClient.followUp`.

Current public docs match the local package:

- <https://pi.dev/docs/latest/rpc> says RPC mode is headless JSON over stdin/stdout, with `prompt`, `steer`, and `follow_up`.
- <https://pi.dev/docs/latest/sdk> says Node/TypeScript integrations can use `createAgentSession` and `AgentSession` directly.

## Design consequence for Persona

The Persona harness should not treat Pi as only a PTY. A better first real-agent e2e path is:

1. `harness-daemon` gets a new Pi RPC adapter path for `HarnessKind::Pi`.
2. The adapter starts or attaches to `pi --mode rpc --session-dir <isolated-dir> --name <harness-name>`.
3. The adapter reads stdout as strict JSONL and records events into the harness transcript stream.
4. Router `MessageDelivery` becomes one of:
   - `steer` when Pi is currently streaming/working and the Persona message should influence current work.
   - `follow_up` when the message should wait until the current task is done.
   - `prompt` when Pi is idle.
5. The adapter observes the assistant reply through events or `get_last_assistant_text`.
6. For the e2e witness, the delivered prompt instructs Pi to reply by running the real `message` CLI back to the sender. That keeps the response on the real Persona message stack instead of scraping arbitrary assistant text.

The terminal-cell PTY lane remains valuable for live terminal-session witnesses, Codex/Claude terminal automation, and viewer behavior. It should not be the only Pi intake path now that Pi exposes RPC.

## Minimal smoke command shape

Start:

```bash
pi --mode rpc --session-dir /tmp/persona-pi-agent-b --name agent-b
```

Send an initial prompt:

```json
{"id":"msg-1","type":"prompt","message":"You are agent-b. When asked, respond by running the message CLI back to agent-a."}
```

While it is busy:

```json
{"id":"msg-2","type":"steer","message":"Incoming Persona message from agent-a: question from agent a. Reply through the message CLI to agent-a."}
```

If the desired semantics are "do not interrupt current work":

```json
{"id":"msg-3","type":"follow_up","message":"Incoming Persona message from agent-a: question from agent a. Reply through the message CLI to agent-a."}
```

The harness adapter should track `response` messages for command acceptance and streamed agent events for progress and transcript. It should not parse generic terminal text if the RPC event stream is available.

## Open implementation questions

1. **Delivery semantics in Persona:** Should ordinary routed messages to a busy Pi default to `steer` or `follow_up`? My lean: `follow_up` for normal messages, explicit higher-priority policy for `steer`.
2. **Pi process ownership:** Should `harness-daemon` always spawn the Pi RPC process, or should it support attaching to an existing RPC process? My lean: spawn first for a deterministic e2e; attach can be a later owner/meta operation.
3. **Reply capture:** For production, replies should be explicit tool calls through `message`, not inferred by scraping assistant prose. For the first e2e, prompt Pi to run `message "(Send agent-a [...])"` and witness the real return route.
4. **Adapter implementation language:** Pi RPC is TypeScript-native, but Persona components are Rust. The simplest Rust implementation is to spawn `pi --mode rpc` and implement a strict LF JSONL codec in Rust. A TypeScript sidecar is possible but adds another process/runtime boundary.

## Bottom line

I do not lack clarity anymore. The right next implementation is a Pi RPC harness adapter, not a PTY-only workaround. It should convert `MessageDelivery` into `prompt`/`steer`/`follow_up`, read JSONL events, and use the real `message` CLI for the response leg in the first live-agent e2e.
