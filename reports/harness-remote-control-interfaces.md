# Remote-Control / Programmatic-Drive Interfaces: pi, Claude Code, Codex

Read-only research lane. Purpose: map, per harness, whether an external process
can deliver a message into a RUNNING full-TUI interactive session at the agent's
next natural turn, and exactly how (interface, transport, auth, prerequisites).
Then design the smallest live tests that would prove the hook-in, flagged
safe-to-run vs. psyche-gated.

Context: building agent-to-agent messaging. A message must land in a live agent
session at its next natural turn. Goal is to stop relying on terminal-cell
(viewer-attach only, glitchy) and use interfaces the harness itself exposes.

## Headline Finding Per Harness

- pi — YES, proven path exists. Two distinct RPC surfaces. The one that reaches a
  live full-TUI interactive session is the `pi-intercom` broker over a local Unix
  domain socket; an external process speaks length-prefixed JSON and the recipient
  session's intercom extension injects the message at its next idle turn via the
  pi host API `pi.sendMessage(..., { triggerTurn: true })`. A second, separate
  surface (`pi --mode rpc`) is a JSON-stdin/stdout embedding protocol with a native
  `steer` verb, but it drives a pi the controller spawns itself, not a human's TUI.
- Claude Code — Conditionally YES. The documented push-into-live-TUI path is
  **Channels** (research preview): an MCP server carrying a `claude/channel`
  capability, spawned by the TUI under a launch flag, that emits
  `notifications/claude/channel` events the model reacts to; a local webhook can
  POST into it. Everything else (`-p`/SDK, `--resume`/`--continue`, standard MCP,
  most hooks) either starts a fresh headless process or only observes/annotates —
  it does not inject the next user turn into a live TUI. `--remote-control` exists
  but routes through Anthropic's cloud.
- Codex — YES for a controller-owned session, and the control plane is LOCAL, not
  hard-wired to OpenAI. `codex app-server` runs a JSON-RPC control daemon whose
  transport is selectable (`stdio://` default, `unix://PATH`, `ws://IP:PORT`);
  `codex app-server proxy --sock <PATH>` attaches an external stdio client to the
  running daemon's Unix control socket. Only model INFERENCE calls OpenAI, and that
  endpoint is itself redirectable via `config.toml` model-provider settings. A
  separate `codex remote-control` layer (pairing code) is the OpenAI/ChatGPT cloud
  relay and is NOT required for local drive. Whether app-server can attach to a
  session a human launched in the standalone TUI (vs. sessions the daemon itself
  owns) is an explicit unknown.

## Sources Consulted

Local (read-only inspection; pi-internals skill authority):
- pi wrapper `~/.pi/agent/bin/pi`; package `~/.local/share/criomos/pi/package`
  resolving to pi 0.80.6; `dist/rpc-entry.js`, `dist/modes/rpc/*` (rpc-mode,
  rpc-client, rpc-types), `dist/core/http-dispatcher.js`.
- `pi-intercom` 0.6.0 package source (broker/broker.ts, broker/client.ts,
  broker/framing.ts, broker/paths.ts, types.ts, index.ts, README.md).
- Live runtime: `~/.pi/agent/intercom/{broker.sock,broker.pid,config.json}` — a
  broker process is currently running (Unix socket present, mode `srwxr-xr-x`).
- `claude` 2.1.206 (`~/.nix-profile/bin/claude`) `--help`.
- `codex` 0.144.1 (`~/.nix-profile/bin/codex`) `--help` and subcommand help for
  `app-server`, `app-server daemon`, `app-server proxy`, `remote-control`;
  `~/.codex/config.toml` keys.

Web / docs:
- Claude Code docs (code.claude.com/docs) for Channels, Remote Control, hooks,
  MCP, headless/SDK, sessions — via claude-code-guide subagent, docs dated
  2026-07-11.
- Codex protocol/source research — via web-research subagent (see Codex section).

## pi

### Observation — two RPC surfaces

1. `pi-intercom` broker (the live-TUI path).
   - Interface: a standalone local broker process (package `pi-intercom` 0.6.0)
     plus a per-session client (`IntercomClient`) loaded as a pi extension in each
     participating session. Package advertises 1:1 messaging between pi sessions on
     the same machine.
   - Transport: Unix domain socket at `~/.pi/agent/intercom/broker.sock` (named
     pipe on Windows). Wire format is length-prefixed JSON: 4-byte big-endian
     length header + UTF-8 JSON payload (`broker/framing.ts`).
   - Protocol (`types.ts`): client→broker messages are
     `register` / `unregister` / `list` / `send` / `presence`; broker→client are
     `registered` / `sessions` / `message` / `presence_update` / `session_joined` /
     `session_left` / `error` / `delivered` / `delivery_failed`. To deliver a steer:
     connect, send `{type:"register", session:{...}}`, receive
     `{type:"registered", sessionId}`, then send
     `{type:"send", to, message:{id,timestamp,content:{text,...}}}`; broker routes
     to the target and returns `delivered` / `delivery_failed`.
   - Auth: none beyond filesystem permissions. `broker.ts` `handleConnection` does
     no credential or token check; any process running as the same user can connect
     and register. Design is same-machine-only by intent (local IPC, no TCP).
   - How a steer reaches a live turn: the recipient session's intercom extension
     receives the `message` event and calls the pi host API
     `pi.sendMessage({ customType:"intercom_message", content, display:true, ...},
     { triggerTurn: true })` (`index.ts` ~line 594). If the session is idle it
     starts a new turn immediately; if busy, the message is queued and flushed when
     `ctx.isIdle()` becomes true (delivered as `followUp` for subsequent queued
     items). This is exactly "delivered at the agent's next natural turn."
   - Broker lifecycle: auto-spawns on first connection, exits ~5s after the last
     client disconnects; `brokerCommand`/`brokerArgs` in
     `~/.pi/agent/intercom/config.json` select the launcher (here: node + tsx).
   - Prerequisites for a target session to be steerable: the `pi-intercom`
     extension installed and loaded, `enabled != false` in config, session started
     after install, broker running/auto-startable.

2. `pi --mode rpc` (embedding protocol; NOT a human's TUI).
   - Entry `dist/rpc-entry.js` runs `main(["--mode","rpc", ...])`; `runRpcMode`
     documents "Headless operation with JSON stdin/stdout protocol ... for
     embedding the agent in other applications." Framing is strict LF-only JSONL.
   - The bundled `RpcClient` (`dist/modes/rpc/rpc-client.js`) spawns the agent in
     RPC mode and exposes typed methods including `prompt(message)`,
     `steer(message)` ("Queue a steering message to interrupt the agent mid-run"),
     `followUp(message)` ("processed after the agent finishes"), `abort()`,
     `newSession()`, `getState()`, `setModel()`.
   - This is a controller-owns-the-process model: the controller holds the pi
     process's stdin. It does not attach to a separately-launched interactive TUI
     (interactive vs rpc are distinct modes). It is the right surface when the
     messaging system launches pi itself.

### Interpretation — pi

- For the stated goal (steer a human-launched full-TUI pi session at its next
  turn), the intercom broker is the correct, already-working surface: it reaches a
  live interactive session and injects at the natural idle boundary. The native
  `steer` verb in `--mode rpc` is a cleaner protocol but only applies to a
  controller-spawned pi.
- An external non-pi process can drive intercom directly: reimplement the ~40-line
  length-prefixed-JSON client (register → send). No pi runtime needed on the
  sender side. This is likely what "RPC steer verified against real pi" already
  exercised (unverified which of the two surfaces the prior proof used — treat the
  exact prior mechanism as an unknown; both are real).

## Claude Code (v2.1.206 installed locally)

### Observation

- Channels (research preview): the one documented mechanism that pushes into an
  already-running interactive TUI. A channel is an MCP server that declares
  `capabilities.experimental['claude/channel']` and emits
  `notifications/claude/channel` notifications; Claude Code injects the payload as a
  `<channel>` tag in the model's context on its next model call. Transport is local
  stdio between the TUI and the spawned channel MCP subprocess. A local webhook
  server (bound to 127.0.0.1) can receive external POSTs and forward them into the
  channel. Two-way channels also expose a `reply` tool and can relay permission
  prompts (v2.1.81+). Enabled per-session with a launch flag
  (`claude --channels plugin:<name>@<marketplace>`) after installing the channel
  plugin; org policy gates `channelsEnabled` / `allowedChannelPlugins`. Docs:
  code.claude.com/docs/en/channels.md and channels-reference.md.
- Local build note (observation): `claude --help` on 2.1.206 surfaces
  `--remote-control [name]` and `--remote-control-session-name-prefix` but does NOT
  list a `--channels` flag in top-level help. Channels may be plugin-gated and not
  shown in `--help`; whether Channels is actually enabled/usable in this exact
  build is unverified.
- Remote Control: `claude --remote-control` / `claude remote-control` steer a
  running TUI from phone/browser, but the transport is HTTPS via Anthropic's cloud
  (api.anthropic.com), OAuth-authed. Not a local IPC path.
- Headless / SDK: `claude -p` runs once and exits. Agent SDK streaming-input mode
  (AsyncGenerator of `SDKUserMessage`) keeps a long-lived agent loop fed with new
  messages, but that loop is a library process the caller owns, not a terminal TUI,
  and cannot attach to an existing interactive session.
- `--resume` / `--continue`: start a NEW process that reads the persisted session
  transcript (`~/.claude/projects/<project>/<id>.jsonl`) and appends one turn. They
  do not attach to or IPC with a live TUI process.
- Hooks: cannot inject the next user turn into a running interactive session,
  except `SessionStart`'s `initialUserMessage` (which only applies to `-p`/headless
  startup). Other hooks (PreToolUse/PostToolUse/UserPromptSubmit/Stop) can block,
  redirect tool I/O, or add `additionalContext`, but not submit a fresh user turn.
- MCP (standard): pull-only; the model invokes tools. Only channel-capable MCP
  servers push. No documented local control socket/named pipe for a running `claude`
  TUI other than a channel server's own localhost HTTP.

### Interpretation — Claude Code

- The only clean external-push-into-live-TUI path is Channels, and it requires the
  target session to have been launched with the channel enabled — i.e. cooperative,
  not arbitrary attach to any already-running session. A messaging integration
  would ship its own channel MCP + a local webhook and require sessions to launch
  with `--channels <our-plugin>`.
- There is no local IPC to steer a claude TUI that was launched plainly. Absent
  Channels, the fallbacks are cloud (Remote Control) or "own the process" (SDK
  streaming / headless), matching pi's `--mode rpc` situation.

## Codex (codex-cli 0.144.1 installed locally)

### Observation — local subcommand surface (read from installed binary help)

- `codex app-server` [experimental] "Run the app server or related tooling", with
  `--listen <URL>` accepting `stdio://` (default), `unix://`, `unix://PATH`,
  `ws://IP:PORT`, or `off`. Subcommands:
  - `daemon` — manage the local app-server daemon: `start`, `restart`, `stop`,
    `bootstrap` ("Install durable local app-server management for SSH-driven use"),
    `enable-remote-control` / `disable-remote-control`, `version`.
  - `proxy --sock <SOCKET_PATH>` — "Proxy stdio bytes to the running app-server
    control socket." This is the external-client attach: pipe JSON-RPC over stdio
    through the proxy into the daemon's Unix control socket.
  - `generate-ts` / `generate-json-schema` — emit TypeScript bindings / JSON Schema
    for the app-server protocol (the protocol is introspectable/codegen-backed).
- `codex remote-control` [experimental] "Manage the app-server daemon with remote
  control enabled": `start`, `stop`, `pair` ("Create and print a short-lived manual
  pairing code"). The pairing code indicates this layer brokers to OpenAI/ChatGPT
  (mobile/web) — the cloud relay, distinct from the local control socket.
- `codex mcp-server` — start Codex itself as an MCP server (stdio).
- `codex exec` / `exec-server` — non-interactive run / standalone exec service.
- `codex resume` / `fork` — resume/fork a prior session from saved session files.
- Local config `~/.codex/config.toml`: `model = "gpt-5.5"`, no explicit
  `model_provider`/`base_url` override present (default OpenAI provider). User is
  ChatGPT-authed (`~/.codex/auth.json` present, mode 600). No app-server daemon is
  currently running (no `.sock` under `~/.codex`, no daemon process).

### Observation — protocol / redirect (web research, openai/codex main, mid-2026)

- Wire protocol: app-server speaks JSON-RPC 2.0 (the `"jsonrpc":"2.0"` field is
  omitted on the wire), bidirectional. Handshake is `initialize` request →
  `initialized` notification, then a Thread → Turn → Item model.
- Inject-a-user-turn methods (current "v2"):
  - `thread/start` — create a thread (emits `thread/started`).
  - `turn/start` — add user input and begin generation. Primary "submit a user
    turn" call.
  - `turn/steer` — append user input to the currently in-flight turn without
    starting a new one.
  - `turn/interrupt` — cancel an in-flight turn.
  - `thread/inject_items` — append raw Responses-API items to a loaded thread's
    model-visible history without a user turn (pure context injection).
  - `thread/resume` / `thread/fork` — reopen or branch a stored thread, then post
    turns. Legacy v1 names on older builds: `newConversation`, `sendUserMessage`,
    `sendUserTurn`. Legacy core ops: `Op::UserInput` / `Op::SteerInput` /
    `Op::Interrupt`. MCP path: the `codex` tool starts a session, `codex-reply`
    continues one by `threadId`.
- Unix control-socket transport: websocket-over-unix, default path
  `$CODEX_HOME/app-server-control/app-server-control.sock`; internal `StdioToUds`
  relays stdio to that socket (this is what `app-server proxy` does).
- Auth: the LOCAL stdio control channel has NO auth (client and server share a
  process boundary) — driving it needs no OpenAI login at the transport level. The
  WebSocket transport requires bearer-token auth before remote exposure. Producing
  model output needs provider creds (`CODEX_API_KEY` → `OPENAI_API_KEY` env
  fallback on the local stdio no-account path, else the ChatGPT token at
  `~/.codex/auth.json`), unless pointed at a no-auth local provider.
- Model-endpoint redirect surface: `openai_base_url` / `OPENAI_BASE_URL` /
  `[model_providers.<id>].base_url`; `--oss` (Ollama/LM Studio, e.g.
  `http://localhost:11434`); `wire_api = "responses"` (current) vs legacy `"chat"`
  (version-dependent). Codex also ships an internal `responses-api-proxy` and honors
  `CODEX_CA_CERTIFICATE`, so redirecting/terminating the model channel locally is
  config-supported.
- TUI attach: a plain interactive `codex` TUI does not listen on any socket for
  external control (issue #11166 requests exactly this). `codex remote-control` +
  the app-server-daemon (issue #25552) run a shared app-server that a refactored
  thin TUI can connect to over the control socket — so attaching to a shared
  app-server you launched is supported/experimental, but attaching to an arbitrary
  human-launched plain TUI is not the current model. `codex resume`/`fork` replay
  stored session files; they are not live attach.
- Sources: codex-rs/app-server/README.md; codex-rs/docs/codex_mcp_interface.md;
  codex-rs/cli/src/main.rs; learn.chatgpt.com/docs/app-server.md, config-reference,
  auth; developers.openai.com/codex/{app-server,mcp,config-advanced,auth}; GitHub
  issues #11166 and #25552; openai.com/index/unlocking-the-codex-harness.

### Interpretation — Codex

- The crux is settled from the installed binary: Codex's CONTROL protocol is local
  by construction. `app-server --listen unix://PATH` (or default stdio) plus
  `app-server proxy --sock` is a fully local drive path; the `daemon bootstrap ...
  for SSH-driven use` framing shows external drive is a first-class use case. Only
  model inference calls OpenAI, and that call is redirectable through legitimate
  `config.toml` model-provider config (no interception needed to run the control
  plane locally).
- `codex remote-control` (pairing) is the OpenAI cloud path and is optional; it is
  NOT the interface to use for local A2A steering.
- Open question mirroring Claude/pi: whether app-server drives only
  daemon-owned sessions or can also attach to a session a human started in the
  plain `codex` TUI. If the TUI does not register with the daemon, the clean path
  is "start the session through app-server," same shape as pi `--mode rpc` and
  Claude SDK.

## Proposed Live Tests

Each: what it proves, setup, and SAFE-NOW vs PSYCHE-GATED. No test below is run in
this lane.

1. pi intercom loopback steer — SAFE TO RUN LOCALLY NOW.
   - Proves: an external non-pi process can push a message over `broker.sock` and a
     live interactive pi TUI injects it at its next turn.
   - Setup: launch one interactive pi TUI with `pi-intercom` enabled and `/name`
     it; run a tiny standalone script (any language) that opens
     `~/.pi/agent/intercom/broker.sock`, writes framed `{type:"register",...}`,
     waits for `registered`, then writes `{type:"send", to:"<name>",
     message:{...}}`; observe the message render and a new turn fire in the TUI.
   - Safe: local Unix socket, same user, no vendor traffic, no interception. This
     is the primary proof and should be the first test.

2. pi `--mode rpc` native steer — SAFE TO RUN LOCALLY NOW.
   - Proves: the native `steer`/`prompt` verbs drive a controller-spawned pi.
   - Setup: spawn `pi --mode rpc` (or use the bundled `RpcClient`), send a
     `prompt` then a `steer` JSONL command, observe streamed events. Confirms the
     embedding path for sessions the messaging system launches itself.
   - Safe: local process the tester owns; model calls use existing pi auth exactly
     as normal pi use (no redirect).

3. Codex app-server local drive — SAFE TO RUN LOCALLY NOW (control plane only).
   - Proves: the Codex control protocol runs and accepts a submitted user turn over
     a purely local transport, with no cloud remote-control/pairing.
   - Setup: `codex app-server daemon start` (control socket at
     `$CODEX_HOME/app-server-control/app-server-control.sock`), or `codex app-server
     --listen unix://<path>`; attach with `codex app-server proxy --sock <path>`.
     Handshake `initialize` → `initialized`, then `thread/start`, then `turn/start`
     with a trivial user message (mid-turn variant: `turn/steer`; context-only:
     `thread/inject_items`); observe the JSON-RPC responses/events. Confirm exact
     method set for the installed build via `codex app-server generate-json-schema`.
     Do NOT run `enable-remote-control` / `remote-control pair`.
   - Safe caveat: the CONTROL plane is local and safe to exercise. Model inference
     for any turn that actually runs will hit OpenAI under existing ChatGPT auth —
     that is ordinary Codex usage, not interception. Keep the test to protocol
     handshake + one trivial turn (or an `--oss`/local model) to avoid confusion.

4. Codex model-endpoint redirect / interception — NEEDS PSYCHE AUTHORIZATION.
   - Proves (would prove): whether Codex's model inference can be pointed at a local
     endpoint (config `model_provider` base_url) or intercepted via a local
     proxy/MITM, e.g. to observe/inject on the inference channel.
   - Setup (design only): set a custom `model_provider` with a local `base_url`, or
     front the OpenAI endpoint with a local reverse proxy. This redirects/intercepts
     vendor traffic.
   - GATED: any redirect or interception of OpenAI/vendor traffic is psyche-gated.
     Do not attempt. Flagged explicitly. Note: this test is NOT needed to prove
     local control-plane drive (test 3 already does that); it is only relevant if
     the inference channel itself must be observed/injected.

5. Claude Code channel push (optional, if Channels usable on this build) — SAFE
   TO RUN LOCALLY NOW if it works; otherwise blocked by feature availability.
   - Proves: a local webhook + channel MCP injects a message into a running claude
     TUI at its next model call.
   - Setup: install/enable a minimal channel plugin, launch `claude --channels
     plugin:<name>`, POST to the channel's localhost webhook, observe the `<channel>`
     content reach the model. First verify Channels is actually enabled on 2.1.206
     (not shown in `--help`).
   - Safe: local stdio/localhost only. Do NOT use `--remote-control` for this proof
     (that path is cloud/OpenAI-relayed).

## Decision Items For The Psyche

- Codex inference-channel interception (test 4) is the only vendor-traffic
  redirect on the table and is explicitly gated. Confirm whether local control-plane
  drive (test 3) suffices for the messaging goal, or whether inference interception
  is actually wanted — if the latter, it needs explicit authorization for the exact
  redirect (endpoint, proxy, rollback owner, risk).
- Claude Code A2A likely requires cooperative session launch (`--channels`) rather
  than arbitrary attach. Decide whether requiring a launch flag on claude sessions
  is acceptable, or whether the cloud Remote Control path is off-limits (it routes
  through Anthropic).

## Explicit Unknowns

- Which pi surface the prior "RPC steer verified against real pi" used (intercom
  broker vs `--mode rpc`). Both are real; the exact prior mechanism is unconfirmed.
- Whether Channels is enabled/usable on the locally installed claude 2.1.206 (flag
  not surfaced in `--help`).
- Codex app-server on the installed 0.144.1 build: whether it exposes the current
  v2 method set (`thread/start` / `turn/start` / `turn/steer`) or legacy v1
  (`newConversation` / `sendUserMessage` / `sendUserTurn`) — confirm via
  `codex app-server generate-json-schema` against this binary (not yet run).
- Attaching to an arbitrary human-launched plain `codex` TUI is NOT the current
  model (issue #11166 is the open request); only sessions the daemon owns or a
  `remote-control`-mode app-server are drivable. Whether the standalone TUI here can
  be made to register with a daemon is untested.
- Claude Code Channels org-policy state on this host (whether `channelsEnabled` is
  permitted).
