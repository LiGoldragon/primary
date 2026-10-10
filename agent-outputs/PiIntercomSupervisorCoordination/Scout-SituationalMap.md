# Scout Situational Map: pi-intercom Supervisor Coordination

Task: explain optional `pi-intercom` supervisor coordination around `nicobailon/pi-subagents`, using primary sources only. Scope was read-only inspection plus this assigned report file; no installs, no code edits, no live Pi run.

## Short Explanation

`pi-intercom` is a same-machine, direct message channel between running Pi sessions. Each intercom-enabled session registers with a local broker; sessions can list peers, send one-way messages, ask blocking questions, reply to pending asks, inspect pending asks, and check connection status.

The interesting `pi-subagents` integration is not ordinary chat switching. When `pi-subagents` launches a child and the intercom bridge is active, the child gets extra bridge instructions and tool access. `pi-intercom` then conditionally registers a child-only `contact_supervisor` tool if the child process has the required `PI_SUBAGENT_*` metadata. That tool knows the supervisor session target and run metadata, so the child can ask the parent/supervisor for a decision without guessing a target session name.

The coordination model is asymmetric by default:

- Any normal intercom-connected Pi session can use `intercom` for 1:1 session messaging.
- A delegated child with subagent bridge metadata can use `contact_supervisor`.
- `contact_supervisor({ reason: "need_decision" })` and `reason: "interview_request"` send a message to the supervisor and block until a reply arrives or the ask times out.
- `contact_supervisor({ reason: "progress_update" })` sends a non-blocking update.
- The supervisor replies with `intercom({ action: "reply", message: "..." })`; the child receives that reply as the blocking tool result and can continue in the same turn.
- The supervisor can also steer a live async child through `pi-subagents` management actions such as `resume` with a follow-up message, where the implementation interrupts the live child and delivers a follow-up over the child intercom target when reachable.

Compared with manually switching terminals or resuming another chat, this creates an agent-visible message in the recipient session, includes reply hints, can trigger an idle recipient turn, and can return the answer directly into the asking child’s tool result. The child does not need to expose a final answer that says "please ask the user"; it can pause at the decision point, ask the supervisor, then continue.

## Evidence Table

| Claim | Evidence |
|---|---|
| `pi-intercom` is direct 1:1 same-machine messaging, not a shared chat room. | `pi-intercom` README describes direct 1:1 messaging and contrasts it with `pi-messenger`: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L5-L27 and https://github.com/nicobailon/pi-intercom/blob/main/README.md#L441-L451 |
| Sessions register with a local broker; only intercom-connected sessions appear. | README connection requirements and broker model: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L51-L59 and https://github.com/nicobailon/pi-intercom/blob/main/README.md#L395-L423 |
| Incoming messages render inline, include reply hints, can trigger a turn, and are stored in Pi session history. | README receiving-message behavior: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L105-L118. Source sends `customType: "intercom_message"` through `pi.sendMessage(..., { triggerTurn: true })`: https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L582-L699 |
| Normal intercom tool actions are `list`, `send`, `ask`, `reply`, `pending`, and `status`. | README tool reference: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L309-L349. Source registers the `intercom` tool and parameter enum: https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L1314-L1635 |
| `ask` blocks for a reply and returns it as a tool result; only one pending ask per session is allowed. | README `send` vs `ask`: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L207-L215. Source `replyWaiter` single-flight and wait handling: https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L430-L482 and https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L1459-L1563 |
| The broker routes plain messages and tracks ask edges to validate replies and prevent mutual-ask deadlocks. | README design decision says ask stays client-side: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L433-L439. Broker source tracks `askEdges` and refuses mutual asks: https://github.com/nicobailon/pi-intercom/blob/main/broker/broker.ts#L109-L315 |
| `contact_supervisor` is child-only and only appears when `pi-subagents` supplies child bridge metadata. | README subagent workflow and required environment variables: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L217-L240. Source reads the same env vars and only registers the tool when metadata exists: https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L21-L42 and https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L80-L96 and https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L1051-L1277 |
| `contact_supervisor` supports `need_decision`, `interview_request`, and `progress_update`; the first two block, the last does not. | README reason table and tool reference: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L232-L240 and https://github.com/nicobailon/pi-intercom/blob/main/README.md#L321-L335. Source branches `progress_update` as send-only and blocking reasons through `waitForReply`: https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L1152-L1277 |
| Supervisor messages include subagent run metadata, and supervisor replies can be plain text or structured JSON for interviews. | README supervisor-visible message and structured reply shape: https://github.com/nicobailon/pi-intercom/blob/main/README.md#L279-L307. Source formats run id, agent, child index, and optional child target: https://github.com/nicobailon/pi-intercom/blob/main/index.ts#L97-L112 |
| `pi-subagents` explicitly documents `pi-intercom` as optional; install it only if children should talk back to the parent while running. | Upstream README: https://github.com/nicobailon/pi-subagents/blob/main/README.md#L231-L267. Local installed README has the same section at `/home/li/.pi/agent/packages/pi-subagents/README.md:213`. |
| `pi-subagents` bridge adds instructions and tools when active. | Upstream config docs: https://github.com/nicobailon/pi-subagents/blob/main/README.md#L1152-L1172. Local source default instructions: `/home/li/.pi/agent/packages/pi-subagents/src/intercom/intercom-bridge.ts:37`. Local `applyIntercomBridgeToAgent` adds `intercom` and `contact_supervisor`: `/home/li/.pi/agent/packages/pi-subagents/src/intercom/intercom-bridge.ts:366`. |
| Bridge activation requires `pi-intercom` installed/enabled, a supervisor target, and extension allowlist compatibility. | Upstream docs: https://github.com/nicobailon/pi-subagents/blob/main/README.md#L1152-L1172. Local resolver checks mode, target, extension directory, and config enabled state: `/home/li/.pi/agent/packages/pi-subagents/src/intercom/intercom-bridge.ts:281`. |
| `pi-subagents` passes the metadata that `pi-intercom` requires. | Local spawn args set `PI_SUBAGENT_INTERCOM_SESSION_NAME`, `PI_SUBAGENT_ORCHESTRATOR_TARGET`, `PI_SUBAGENT_RUN_ID`, `PI_SUBAGENT_CHILD_AGENT`, and `PI_SUBAGENT_CHILD_INDEX`: `/home/li/.pi/agent/packages/pi-subagents/src/runs/shared/pi-args.ts:199`. |
| Child session names can be set to targetable intercom names. | Local prompt runtime calls `pi.setSessionName` from `PI_SUBAGENT_INTERCOM_SESSION_NAME`: `/home/li/.pi/agent/packages/pi-subagents/src/runs/shared/subagent-prompt-runtime.ts:203`. |
| Parent-side result delivery and attention notices can go over intercom. | Upstream `pi-subagents` README: https://github.com/nicobailon/pi-subagents/blob/main/README.md#L253-L259 and local README `/home/li/.pi/agent/packages/pi-subagents/README.md:237`. `pi-intercom` changelog records result relay and needs-attention relay: https://github.com/nicobailon/pi-intercom/blob/main/CHANGELOG.md#L53-L61 |
| Supervisor can steer a live async child by sending a follow-up through `subagent({ action: "resume", ... })` when reachable over intercom. | Local README: `/home/li/.pi/agent/packages/pi-subagents/README.md:928` and `/home/li/.pi/agent/packages/pi-subagents/README.md:939`. Local source interrupts live async child and delivers follow-up to `target.intercomTarget`: `/home/li/.pi/agent/packages/pi-subagents/src/runs/foreground/subagent-executor.ts:798`. |
| Local machine has `pi-subagents` configured, but not `pi-intercom` under `/home/li/.pi/agent/packages`. | `/home/li/.pi/agent/settings.json:37` lists `packages/pi-subagents`; `ls -ld /home/li/.pi/agent/packages/pi-intercom` returned "No such file or directory"; local `pi-subagents` package version is `0.31.0` from `package.json`. |
| Current npm versions observed without installing: `pi-intercom` 0.6.0 and `pi-subagents` 0.31.1. | Commands: `npm view pi-intercom version ... --json`; `npm view pi-subagents version ... --json`. |

## Practical Implications

For your use case, the interesting part is that a subagent can stop at a real decision point and ask the parent/supervisor instead of guessing or ending with a clarification question. This is useful for long-running implementation, review, or research children where the parent has the global context and the child has local findings.

The bridge reduces target-selection friction. A child does not need to list sessions and infer which one is the parent; `pi-subagents` supplies the orchestrator target and run metadata, and `contact_supervisor` formats the message so the parent can see which run/agent/child is asking.

The supervisor can steer in two ways. The most direct path is replying to a blocking child ask; the reply becomes the child’s tool result. For async children, `pi-subagents` also has `resume`/nudge behavior that can deliver a follow-up to a still-reachable child over intercom.

It is not a full multi-agent project manager by itself. The intercom layer is a local 1:1 transport plus Pi message integration. `pi-subagents` supplies child spawning, run IDs, result artifacts, status, and bridge metadata. Without that specific metadata-producing subagent extension, normal `pi-intercom` still works, but `contact_supervisor` does not appear.

Install/config summary from sources:

- Install `pi-intercom` with `pi install npm:pi-intercom`, then restart Pi.
- A session is connected only if the extension is installed/loaded, not disabled in `~/.pi/agent/intercom/config.json`, started/reloaded after install, and can start/connect to the broker.
- `pi-subagents` itself works without intercom; install intercom only for child-to-parent live coordination.
- `pi-subagents` bridge config is `intercomBridge.mode` with `always` default, `fork-only`, or `off`; `instructionFile` can replace the default child guidance.
- Runtime intercom config supports `brokerCommand`, `brokerArgs`, `confirmSend`, `enabled`, `replyHint`, and `status`; default ask timeout is 10 minutes, overrideable by `PI_INTERCOM_ASK_TIMEOUT_MS` in source.

## Unknowns And Live-Test Items

No live Pi session was started, no broker was launched, and no package was installed. The following require a live Pi test:

- Whether this machine’s current Pi runtime loads the upstream `@earendil-works`-scoped `pi-intercom` source cleanly, given local `pi-subagents` is installed via a Nix/Home Manager symlink and `pi-intercom` is absent locally.
- The exact transcript rendering in the user’s current terminal theme and Pi version.
- Whether foreground parent tool-call detachment feels smooth in practice when a child calls `contact_supervisor`; local `pi-subagents` source supports detaching for intercom coordination, but this was not exercised.
- Whether the latest npm package contents exactly match GitHub `main`; observed `npm view pi-intercom` metadata and `main` package metadata differ slightly in dependency shape, likely due unreleased source changes.

## Commands Consulted

- `spirit "(PublicTextSearch [pi intercom supervisor coordination])"`: no task-specific directive record; relevant public intent reminded to keep claims grounded and ask rather than infer.
- `rg -n "pi-intercom|pi_subagents|pi-subagents|nicobailon" -S . --glob '!repos/**' --glob '!private-repos/**' --glob '!agent-outputs/**'`
- `rg --files /home/li/.pi/agent/packages/pi-intercom /home/li/.pi/agent/packages/pi-subagents`
- `sed`, `nl -ba`, and `rg` on local `/home/li/.pi/agent/packages/pi-subagents/...` files listed above.
- `curl -fsSL` against raw GitHub source files for `nicobailon/pi-intercom` and `nicobailon/pi-subagents`.
- `npm view pi-intercom ... --json` and `npm view pi-subagents ... --json`.

Not checked: private repositories, live Pi session behavior, GitHub issues beyond search-result awareness, or any non-primary social/media claims.
