# Messaging audit: one checked CLI call per send

Read-only audit for Psyche Medium d8df70, 2026-09-23. Part A is what was observed. Part B is what I propose. Nothing was edited or sent.

## Part A: observed facts

### A1. `tools/msg` is not a checked send, and its route is down

- `tools/msg <to> <text>` wraps the text in `Machine.Relay.{ ingress from seat heard mode [recipients] quote context }` using `messaging.py machine`. It then types a base64 `FRAME.` line into the pane named in `~/.local/state/messenger/pane_id`, using `herdr pane send-text` and then `send-keys enter`. It exits 0 once Herdr takes the keystrokes. It gets nothing back from the messenger: no Delivered, Held or ParseError reply.
- `tools/msg` does not resolve the recipient and does not check liveness. That work is done later, asynchronously, by `tools/messenger`'s `deliver()`: roster refresh from `herdr agent list`, pane lookup, a protected-seat refusal, a status check, then `agent get`, a name/pane/terminal_id match, `interactive_ready`, `agent prompt`, and a post-check, all written to a ledger. The caller never sees the outcome.
- The route is dead. `pane_id` holds the literal `--help`, and the log shows `messenger-started pane=--help` at 2026-09-23T22:11:27Z. The last two relays (2026-09-22) ended `codec-unavailable`, and the log has no `delivered-bound-agent` line. `message-daemon.service` has been failed (start-limit-hit) since 12:10 local. `message` prints "daemon socket is not configured; set MESSAGE_SOCKET". `flow resolve 836818` returns `RecipientResolutionRejected.UnknownFlow`, so Flow Nexus does not know the live seats.

### A2. `hm-send` (Hacky Messenger) already is a checked single-call send

`hm-send FLOW TEXT` (`tools/hacky-messenger/hm.py send`) does all of this in one process:
1. Refuses if `FLOW_ID` (the sender) is unset. It also refuses empty text, control characters, and anything over 64 KiB.
2. Takes an Orchestrate lock `HackyMessengerDelivery` on the registry directory, and releases it afterwards.
3. Refuses a Flow that has a retirement marker, and a record that has `route_hold`.
4. Resolves the Flow ID from `~/.local/state/hacky-messenger/<FLOW>.json` (session, name, pane_id, terminal_id, agent, native_thread).
5. Liveness and identity: runs `herdr --session S agent list` and requires exactly one live agent matching session, name, pane_id, terminal_id and agent. It requires `interactive_ready` (or a recorded readiness proof) and refuses `agent_status == blocked`.
6. Sends with `herdr agent prompt <pane> <text>` and returns `Submitted to <FLOW> via Herdr (not a read receipt)`.

What it does not do:
- It does not check the process. `native_thread` is stored but not compared at send time. `pane process-info` and PID checks run only in `hm-move`.
- It does not use `agent prompt --wait` or read a stall result, so the grade stays at submitted.
- It records nothing in Message Nexus. Its only trace is the Orchestrate lock.
- It cannot reach an unregistered Flow. This seat, d8df70, has no HM record, so it cannot be messaged by Flow ID.
- Registration (`hm-register`) is manual.

Live witness: the main flow's `FLOW_ID=d8df70 hm-send 836818 "..."` returned `Submitted to 836818 via Herdr (not a read receipt)` (transcript line 675, 22:35:46Z). Psyche High's work reply arrived in d8df70 at 22:36:59Z (line 692). That reply is the read/completed witness.

### A3. The other pieces

- `claude-native-seat-refresh.py`: `herdr_agent()` runs `agent get` and matches name, pane_id, terminal_id and agent=claude, and requires `interactive_ready`. `herdr_send()` calls it and then runs `agent prompt`. This is the same pattern as hm-send, used only for refresh.
- Herdr 0.8.2 read verbs, per `herdr --skill` and live reads (`agent`/`pane` subcommands do not print their own `--help`; the top-level help is shown instead):
  - `agent get <pane>` gives name, pane_id, terminal_id, agent, agent_status, interactive_ready.
  - `pane process-info --pane <pane>` gives the foreground PIDs and argv. For 836818 the argv is `claude --session-id 836818cc-… --model claude-fable-5-1[1m] …`, pid 3784555.
  - `agent prompt` refuses `agent_blocked` before sending anything. With `--wait` it returns `agent_prompt_stalled` if no lifecycle change is seen within 5 s. That makes "the target reacted" cheaply observable in the same call.
- Herdr's own hooks. `herdr integration status` shows claude and codex both at "current (v8)". The Claude and Codex hook configs register only a `SessionStart` hook, `herdr-agent-state.sh session`. It sends `agent_session_id`, the transcript path and the start source to Herdr (`pane report-agent-session`). Herdr does not expose that id: it is absent from `agent get`, `agent explain` and `api snapshot`.
- The Claude harness's own registry. `~/.claude/sessions/<pid>.json` holds pid, sessionId, name, status and messagingSocketPath. All 10 entries were for live PIDs at audit time. 836818 is pid 3784555, with name `primary-31` (nameSource "derived").
- Claude native channel (SendMessage/ListAgents). The main flow's ListAgents output does list 836818, as `primary-31 [bd2b35] · interactive · idle`. It could not be recognised as 836818 because its session name carries no Flow ID. Sessions named with their Flow ID are recognisable (`Psyche Medium d8df70`, `Psyche Medium e88ca4`, `Psyche Medium b80e55`). The earlier report that the native channel "does not list 836818" is corrected: it is listed under a name that does not carry its Flow ID.
- Another channel is present: an `agent-intercom` MCP server runs in 836818's pane (intercom_send/ask/list tools). I did not assess it.

### A4. Skills that shape a send (authored in `/git/github.com/LiGoldragon/Curriculum/skills/`)

| Skill (source file) | Prefix | Parts that add model calls |
|---|---|---|
| `messaging.md` | none (core) | "Use a safe isolated test before relying on a route: disposable recipient ... then cleanup. Test submission and read separately." Every new route turns into a probe project. It also tells the sender to resolve right before sending and to record the binding, which the caller then does by hand. |
| `testing-message-route.md` | testing- | A disposable-target probe, then "Re-resolve between the probe and the real send", then a separate grade report. That is three steps before one send. |
| `testing-datom-messaging.md` | testing- | "one complete Datom value against a declared recipient message type ... If the receiver has no declared type ... establish that contract before" sending. No such types exist, so this became a type-discovery hunt. It names `tools/msg` as "the current bridge", which is the dead route. It is a dependency of `main-flow.md`, so it loads in every main flow. |
| `flow-communication.md` | none | Routing only; no per-send cost. Says "Datom is the wire format." |
| `operational-layer-communication.md` | operational- | Routing only; no per-send cost. |
| `main-flow.md` | none | "When a locate, probe, peer-message or read-tail task recurs, it is a subflow script". Peer messaging is sent to a subflow. |
| `subflow-scripts.md` | none | Its only send script is `queue-to-codex`, which is Codex only. There is no Herdr or Claude send script, so each send becomes an ad hoc write subflow. |
| `herdr.md` | none | Points to `messaging` and adds no per-send cost. |

Ownership by prefix, from the psyche record (flows/b05237/vision/operational-skillTypesTriad.md, 2026-09-18): "the operational ... skill is basically the mind skill ... And then you have the testing ... field type work to maintain". By that record, testing-* belongs to Field and operational-* belongs to Mind. The living's 2026-09-23 wording ("skills that belong to Field, but operational changes") reads as assigning operational changes to Field too. Conflict C3 below covers this.

### A5. Cost of the 836818 send in this session

Counted by unique API message id in the transcripts; each count is one model call. Tokens are raw input, cache-creation, cache-read and output.

| Segment | Model calls | Input / cache-create / cache-read / output |
|---|---|---|
| Main flow: 3 Skill loads, launching the write-demanding subflow, the report to the living (lines 566-600) | 4 | 8 / 4,988 / 571,483 / 2,878 |
| Subflow `write-demanding` "Message Psyche Fable" (22:30:11 to 22:35:28, finished) | 53 | 106 / 96,339 / 3,415,089 / 646* |
| Nested Explore "Find declared message types" | 27 | 54 / 87,799 / 1,347,472 / 243* |
| Subtotal, subflow route | **84** | about 5.52 M input-side tokens |
| Outcome | **NOT SENT**: "no fitting declared message type exists for this recipient, and the named transport is not running" | |
| Main flow's direct fallback: `hm-send --help`, the send refused for missing `FLOW_ID`, the successful send | 3 of the 6 calls in lines 650-690 | whole segment, including ListAgents and 2 SendMessages: 14 / 7,823 / 961,823 / 2,440 |

*Output counts in subagent logs look undercounted (streamed usage). Treat them as a lower bound.

About 84 model calls sent nothing. Three calls to one CLI did send, and one of those was a missing-environment retry. The recipient replied with its work 73 s later.

### A6. Psyche on messaging (newest first)

- 2026-09-23, typed, flows/d8df70/vision/messaging.md: "You can just make a single CLI call and send a message. If there is a match for what you want and the pain [pane] still exists, then it just sends the message. I guess the script can check that the process still exists and is running in Herder?" and "What about if we use hooks at the start and the end of the Claude or the Codex session to register or unregister that session from the registry?"
- 2026-09-21, STT, flows/1b8ac0/vision/messaging.md: "Flow takes care of the rest of making sure that there's no other writer ... It locks the message for the session to send the message, then it sends the message, then it removes the lock ... It would just ask to send a message to a certain Flow, and then the Flow would say successful or not, basically." Also: "Raw is on meta, so it's not usually accessible."
- 2026-09-21, flows/6db4fe/vision/messaging.md: "We can't just call on a flow. It is expensive. That should sort of be in the basic behavior: don't wake flows unnecessarily." Also forbids hash-heavy acknowledgments.
- 2026-09-21, relayed (verbatim not established), flows/1b8ac0/vision/flowNexus.md: "getting message and Flow working the way I specified it ... Let's test it, even if it doesn't pass the test, because we don't have anything right now."
- 2026-09-19, flows/b81560/vision/operational-messagingSimpleSystem.md: "let's figure out how this messaging thing works so everybody can start using a simple system. Where is the message CLI for the message nexus? Is it not working?"
- 2026-09-19, flows/b81560/vision/operational-datomHackyMessagingAndLanguageUpgrade.md: "adapt a message that uses the datom to sort of work in a hacky way right now ... at least it'll type-check that things are in datom".
- 2026-09-19, flows/b81560/vision/operational-reapingOnRefreshAndFlowEndHook.md: "Why are you sending messages to flows that are over? ... We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI". flows/cf3553/vision/operational-finalResponseLifecycleHook.md adds: "It does not authorize a hook to retire a flow by itself."
- 2026-09-19, flows/b81560/vision/operational-refreshOutboxAndMessageChannels.md: flows are "users of the messaging system"; they see seat names.
- 2026-09-18, flows/c7128c/vision/psycheVersusMachineMessaging.md: "Flow is in charge of herder ... the agents will know that it's me because of how the message is formatted. It won't be datom-formatted." (Mirrored in flows/056f6d/vision/messaging.md.)
- 2026-09-18, flows/b05237/vision/operational-paneDeathAndMessagingIndex.md: "Does the messaging index get updated when the harness dies or something?"

## Part B: proposals

### B1. The command: make `hm-send` the one send, and retire `tools/msg`

The smallest change is to harden `hm-send`, which already works end to end, rather than repair the `tools/msg` messenger pipeline. It gets one canonical name in the skills (`hm-send`, or `msg` re-pointed at it).

```
hm-send FLOW TEXT [--wait-presented] [--abrupt]
  env: FLOW_ID (sender; required)
```

Resolution source: the HM registry record for FLOW, which holds session, name, pane_id, terminal_id, agent and native_thread. Records are written automatically by hooks (see B3), not by hand.

Checks, all inside the existing Orchestrate registry reservation, in this order. Any failure stops the send.
1. Not retired and no `route_hold`.
2. `herdr --session S agent get <pane_id>`. The pane must exist, and name, pane_id, terminal_id and agent must equal the record. This is one targeted call instead of `agent list`.
3. `agent_status` must be idle, working or done, not blocked, and `interactive_ready` must be true.
4. New: process identity. `herdr pane process-info --pane <pane_id>` must show a foreground process whose argv contains `native_thread`. For Claude, the pid's `~/.claude/sessions/<pid>.json` `sessionId` must also equal `native_thread`; this covers resumed sessions without `--session-id` in argv. For Codex, the thread witness is unverified; use argv if it carries the thread id, otherwise refuse with `IdentityUnprovable`.
5. Send with `herdr agent prompt <pane> <framed text>`. With `--wait-presented`, add `--wait --timeout 5000` and map `agent_prompt_stalled` to a failure and a lifecycle change to "presented". Without it, the result is "transported".
6. Post-check `agent get` (terminal_id unchanged). This is the same pattern as `messenger`'s `validate_post`.

Failure handling: send nothing, print one typed line, `Held.{ FLOW <reason> }`, where reason is one of NotRegistered, Retired, RouteHold, PaneMissing, IdentityChanged, ProcessMismatch, Blocked, NotReady, Stalled or Uncertain. Exit non-zero. Never retry, never reroute, never fall back to another channel. An uncertain result after the prompt was issued is reported as `Uncertain`, not as failure, and not retried.

Framing, the provenance header: prefix the body with one typed line, `Machine.Relay.{ <ingress> <FLOW_ID> <seat> «<utc>» <mode> [ <FLOW> ] «<prose>» «» }`, as `messaging.py machine` already builds (witnessed: prose is accepted as the quote). The machine origin is then visible in the message format, which is the living's 2026-09-18 distinction, without a per-recipient semantic type.

What it records: one Message Nexus attempt with the binding (flow, pane, terminal, native_thread) and grade, once `message-daemon` runs again. Until then, it appends one line to a local ledger (reuse `messaging.py ledger-attempt`). Recording is best-effort after the send decision; a failure to record never blocks or duplicates a send.

Grade returned: `Transported` (Herdr accepted `agent prompt` for the exact checked binding), or `Presented` with `--wait-presented` when Herdr saw a lifecycle change. It never returns Read or Completed; the recipient's own work reply is that witness. The present output string "Submitted ..." understates what hm-send already proves (transport to a checked binding). The messaging skill's grades should be used exactly.

Can it observe "presented" cheaply? Yes. `agent prompt --wait --timeout 5000` gives it in the same call, for at most 5 s. The caveat, from `herdr --skill`: if the target was already working, completion of the active turn can satisfy the wait. So "presented" is only strong when the target was idle or done beforehand. Report the pre-send status with the grade.

### B2. Why not the `tools/msg` messenger pipeline

It needs a persistent messenger pane, a codec binary, and a FIFO ledger, and it returns nothing to the caller. Every one of those is currently broken (A1). Its `deliver()` checks can move into `hm-send`, and `tools/msg` can become a thin wrapper around it, or be removed.

### B3. Session hooks for registration (the living's mid-turn idea)

Hooks each harness offers:
- Claude Code 2.1.280. `SessionStart` is configured here in `~/.claude/settings.json`, and its hook input includes `session_id`, `transcript_path`, `cwd` and `source`. From Claude Code documentation, not witnessed here: `source` is startup, resume, clear or compact, and a `SessionEnd` hook exists with a reason of clear, logout, prompt_input_exit or other. Only `SessionStart` is configured in this setup.
- Codex 0.153.4. `features.hooks = true` in `~/.codex/config.toml`, and `~/.codex/hooks.json` registers `SessionStart` (Herdr's script). The binary contains the strings `SessionEnd`, `SessionStart`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `PostCompact`, `PreToolUse`, `PostToolUse` and `PermissionRequest`. Whether `SessionEnd` fires, and what its input contains, is unverified.

What the hook would write: on SessionStart, a binding keyed by the native session id, using `HERDR_PANE_ID` and the Herdr socket environment already given to the hook: session_id, harness, herdr session, pane_id, terminal_id (read with `agent get`), pid and start source. This goes to the HM registry directory (file per session, atomic write, same Orchestrate reservation). When Flow Nexus has a live registry it becomes the owner, and the file store is only its bootstrap. The Flow ID is not known at SessionStart: a seat claims it later with `flow-id`. So `flow-id claude ... --parent-session <session_id>` must bind Flow ID to session_id in the same registry. Two writes, both automatic. On SessionEnd, the hook marks the binding ended. It does not delete it, and it never retires the Flow (the cf3553 record says a hook does not authorize retirement).

Cases the hooks do not cover:
- Crash, OOM, or `kill -9` of the harness: no SessionEnd runs, so the record stays "live".
- Herdr pane closed or terminal replaced: SessionEnd may not run (SIGHUP handling is unverified). Herdr's skill says closed pane IDs are not reused, but a new agent can start in the same live pane; terminal_id and the process check catch that.
- `/clear` (per the living, not needed for now, see B6.1): new session_id. Documented Claude behaviour is SessionEnd(clear) then SessionStart(clear), so the Flow-to-session binding has to follow. That needs the `flow-id` binding to carry over, or the hook to rebind by pane.
- Resume: the session id may or may not change. The hook's `session_id` is authoritative either way.
- Compact: SessionStart(compact) on the same session is a harmless re-write.
- Pane moves (`hm-move` changes pane_id): hooks do not fire.
- Codex: all of the above is unverified.

Is the send-time liveness check still needed? Yes. Hooks keep the registry mostly current. Only the send-time `agent get` and `process-info` match proves the binding at the moment of sending, and it is what catches crash, kill -9, terminal replacement and a missed SessionEnd. The two are complementary: hooks remove manual `hm-register`, and the send-time check removes probe subflows.

Already present: the Claude harness keeps `~/.claude/sessions/<pid>.json` itself, and Herdr's own SessionStart hook reports the session id to Herdr. Herdr does not expose that id (A3). If Herdr exposed `agent_session_id` in `agent get`, the send-time identity check could drop the process-info call.

### B6. The living's further vision: controlled sessions, process-exit unregistration, holding during transition

Quoted from flows/d8df70/vision/messaging.md (living, 2026-09-23, input mode not established).

**B6.1 Session reset is out of scope.** "Well we're not going to get a clear signal because we're controlling the session. ... It means that it's going through the flow but that's the flow CLI. We don't need to support that for now." The file's own reading note says "clear signal" may be "`/clear`", unconfirmed. I read it this way: seats are launched and driven by our launchers, so a `/clear` or a resume that changes the session id does not happen outside the Flow CLI, and the hook design does not need to handle it now. Consequence: the SessionStart hook covers startup only (plus a harmless re-write on compact). A session id that changes anyway is caught by the send-time process check (B1 step 4) as `ProcessMismatch`; it is not silently followed.

**B6.2 Process exit is the unregister signal.** "you just use the process going out as the unregistry hook. You could even have it from an earlier point if you're exiting, sending the exit signal. ... there are probably some advantages there too, right, in terms of retaining messages."

Where the supervisor can live, from most to least direct:
- Herdr's own process events. Observed in `herdr api schema --json`: `events.subscribe` and `events.wait`, with event types `pane_exited`, `pane_closed`, `pane_moved`, `pane_agent_detected` and `pane_agent_status_changed` (whose `agent` field is nullable). Herdr's skill also says an agent name "is cleared when that agent exits, is released, or is replaced". So Herdr already sees exit for every seat, Claude or Codex, without any per-harness hook. I did not subscribe to verify the events fire; that is unverified. Recommended: one long-running subscriber, a Field service, that maps `pane_exited`, `pane_closed`, an agent turning null, and `pane_moved` to registry changes.
- A wrapper around the harness (the launcher runs `seat-wrap <flow> -- claude ...`). It catches normal exit and SIGTERM/SIGHUP, and can write "exiting" before the process dies (the living's "earlier point"). It cannot catch kill -9 of itself, and it does nothing for seats not launched through it.
- systemd (`systemd-run --user --scope` per seat, with an ExecStopPost-style hook). This catches every exit, including kill -9 of the harness. But seats run inside Herdr panes, not as units, so this means changing how seats are launched. Heaviest option.
- Harness SessionEnd hooks. Fire only on a clean end; Codex unverified (B3).

Recommended: Herdr events as the authoritative exit signal, plus an optional early "exiting" mark from the harness's SessionEnd hook or from the refresh launcher (the "earlier point"). The send-time check stays as the backstop for a missed event while the subscriber is down.

What exit does to the registry: mark the binding `exited` (pane, terminal, pid, time, cause) and keep the Flow record. Do not delete it and do not retire the Flow (cf3553). A later send to an `exited` Flow with no successor goes to the hold path (B6.3). This is the "retaining messages" advantage: a message to a Flow that just died is not lost or typed into a dead or replaced pane; it waits for a successor.

**B6.3 Hold while missing or in transition.** "If there's no registry or if the registry says "in transition" or something, then the message can sort of be held ... We can wait a few seconds at least to see if there's a new flow."

- The "in transition" state: a registry state on the Flow (or seat-role) record, `Transition.{ predecessor successor-expected since deadline }`. It is set by whoever starts the change. That is the refresh or seat launcher (`tools/native-seat-launch.mjs`, `tools/claude-native-seat-refresh.py`) before it stops the predecessor or starts the successor, and the exit subscriber when a Flow exits without a planned successor (state `exited`, no successor). It is cleared when the successor's SessionStart hook plus `flow-id` claim registers the new binding and the launcher confirms. Who may set it is the launcher and the Field supervisor only, never a sender.
- Hold window: the sender's single call blocks for a short bounded wait, default 10 s and configurable, polling the registry or waiting on the Herdr `pane_agent_detected` event. If a registered, live, identity-checked successor appears, it sends to it (B1 checks apply to the new binding) and reports the grade with `via-successor <flow>`.
- When the window expires, the call returns `Held.{ FLOW InTransition|NotRegistered attempt-<id> }`, exits non-zero, and does not type anything anywhere. The message is kept as a pending attempt. Delivery of kept messages happens once, when the registrar binds the declared successor of that Flow (the launcher named it). It is delivered with a header saying it was held for the predecessor, which matches the 2026-09-19 refresh-outbox vision ("the reply will go to the new flow"). A pending message with no successor after a longer bound (for example 1 h) is escalated to the sender or Field and never delivered to a guessed target.
- Where held messages live: Message Nexus attempts are the right home (durable attempts and receipts are its stated job in the `messaging` skill). It is down now (A1), so until it runs, a pending file per attempt in the HM registry directory, under the same Orchestrate reservation. The sender does not wait for delivery beyond the short window; the pending attempt is the record.
- Risk to state plainly: holding and later delivery means a message can arrive after the context that caused it has moved on. Keep the held-for-predecessor header, never deliver to anything but the declared successor, and never retry an `Uncertain` send through the hold path.

### B4. The Claude native channel compared

| | `herdr agent prompt` / `hm-send` | Claude SendMessage |
|---|---|---|
| Reach | Any Herdr-hosted harness (Claude, Codex) | Claude to Claude only; Codex not established |
| Addressing | Flow ID through the HM registry | Session name from ListAgents (`primary-31` for 836818, so no Flow ID unless the session is named with it) |
| Provenance at the receiver | Arrives as ordinary user input (d8df70 received 836818's reply as a pasted user prompt), so it cannot be told from the living's typing unless framed | Wrapped `<cross-session-message from=...>`, not human input |
| Liveness / identity check | Explicit (pane, terminal, agent, ready, and process as proposed) | Implicit: a listed peer is alive; the harness resolves it |
| Grade | Transported (Presented with `--wait`) | "reached that session"; `[Cross-session delivery notice]` on refuse/hold; optional one-shot idle notice |
| Cost | 1 Bash call | 1 tool call (plus ListAgents if the name is unknown) |
| Permission | Bypasses the recipient's approval (types into its terminal) | Held for approval if the permission modes differ |

For Claude-to-Claude it is the better-provenanced path, provided seats name themselves with their Flow ID. It is not a replacement while Codex seats exist. The system stays one-rule: `hm-send` for all. SendMessage is optional for Claude peers that are named with their Flow ID.

### B5. Numbered skill changes for Field

Goal: one Bash call from the main flow, no probe, no subflow, no type hunt.

1. `testing-message-route` (testing-, Field). Replace the disposable-target probe and the re-resolve step with: "Send with `hm-send`; its built-in resolve, pane, terminal, process and readiness checks are the route proof for that send. Report the grade it prints." Keep disposable-target probes only for changes to the transport itself.
2. `testing-datom-messaging` (testing-, Field). Drop "establish that contract before" sending when the recipient declares no type. The `hm-send` relay header is the typed machine envelope and the body may be prose until a recipient type exists; validate against a declared type only when one exists. Replace "`tools/msg` bridge" with `hm-send`. Keep the hash-noise rule.
3. `messaging` (core, not prefixed; owner not established, see C3). Remove "Use a safe isolated test before relying on a route" as a per-send rule. Point to `hm-send` as the send. Map its outputs to the grade vocabulary (Transported / Presented), and state that `tools/msg` is not live.
4. `main-flow` (core; owner not established). Remove "peer-message" from the tasks that become subflow scripts: a send is one direct `hm-send` call by the main flow. Replace the `testing-datom-messaging` dependency with the lighter rule from change 2, or keep it once it is changed.
5. `subflow-scripts` (core; owner not established). Do not add a Herdr/Claude send script. Note that `queue-to-codex` is superseded by `hm-send` for Herdr-hosted Codex seats.
6. New `operational-message-send` (operational-, see C3 for owner), or fold it into `operational-layer-communication`. One paragraph: `FLOW_ID=<self> hm-send <FLOW> "<text>"`, what each `Held.` reason means, never retry an `Uncertain`, and a work reply is the read witness. Do not send probes or acknowledgment-only messages (6db4fe).
7. `testing-flow-titles` or the seat-launch path (testing-, Field). Name every Claude session with its Flow ID (for example `Psyche High 836818`), so ListAgents and Herdr agent names resolve by Flow ID.
8. New `testing-session-registry` (testing-, Field), or add it to `herdr`. Install a SessionStart/SessionEnd hook beside Herdr's (not editing Herdr's managed file) that writes the binding in B3. Make `flow-id` bind Flow ID to session_id. Test on a disposable seat: start, kill -9, and pane close.
9. `testing-session-registry` (testing-, Field), continued. Scope the hook to startup only; `/clear` and resume are out of scope while sessions are launcher-controlled (B6.1). A changed session id is refused by the send-time check.
10. New `testing-seat-exit-supervisor` (testing-, Field), or a section in `herdr`. Run one subscriber on Herdr `events.subscribe` (`pane_exited`, `pane_closed`, agent null, `pane_moved`) that marks bindings `exited` or moved. It never deregisters a Flow and never retires one. Test with a disposable seat: normal exit, kill -9, pane close, pane move.
11. `refresh` and the seat launchers (skill `refresh`, core; tools owned by Field). The launcher sets `Transition.{ predecessor successor-expected since deadline }` before stopping or starting a seat, and clears it when the successor's binding is registered and checked.
12. `operational-message-send` (item 6), extended. Document the hold: `hm-send` waits up to the window (default 10 s) for a successor. On expiry it prints `Held.{ FLOW InTransition|NotRegistered attempt-<id> }` and keeps the message as a pending attempt, delivered once to the declared successor with a held-for-predecessor header. The sender does not resend.

Tool changes behind these (Field, not skills): the Herdr-event exit subscriber, the Transition state in the launchers, the hold-and-pending path in `hm-send`, and the process-identity check, the targeted `agent get`, `--wait-presented`, the relay header, ledger/Message Nexus recording, and exact grade output to `hm.py send`. Make `hm-send` default `FLOW_ID` from the harness environment when a hook-written binding identifies the calling pane. Retire or re-point `tools/msg`.

## Conflicts

- C1. Isolated probe vs. single call. `messaging` and `testing-message-route` require a disposable-target probe and re-resolve before relying on a route. The living's 2026-09-23 words ask for one call that checks and sends. The proposal replaces the probe with checks done at send time. Psyche 6db4fe ("don't wake flows unnecessarily") supports removing probes.
- C2. Datom typing. `testing-datom-messaging` and `flow-communication` ("Datom is the wire format") require a typed body against a declared recipient type. No such types exist; 836818's own log calls prose "the interim route". The b81560 record (2026-09-19) wants Datom "in a hacky way right now". The proposal keeps Datom in the envelope and allows prose in the body. This is a partial relaxation of the skill as written.
- C3. Ownership of operational-* skills. The 2026-09-18 record (b05237) says operational skills are Mind skills and testing skills are Field. The living's 2026-09-23 words hand "operational changes" to Field. Whether the operational-* changes (B5 item 6) go to Field or Mind is for the living or the main flow to settle. `messaging`, `main-flow` and `subflow-scripts` carry no prefix, and no record here names their owner.
- C4. Who holds the lock and does the write. Psyche 2026-09-21 (1b8ac0) places sending inside Flow: Flow locks the Herdr session, sends, unlocks, and answers success or failure. `hm-send` is an interim client-side version of that, with an Orchestrate lock on the registry rather than a Flow-owned session lock. It should be treated as the stopgap until Flow does it, not as the final design.
- C6. Holding and later delivery (B6.3) against "never retry automatically" in hm.py and the messenger. A held message is delivered once, to a declared successor. That is a new binding, not a retry, and it matches the `messaging` skill's "issue a new attempt" rule. But it introduces delayed delivery, which the current skills do not describe.
- C7. The living's "clear signal" reading (B6.1) is an inference; if it did not mean `/clear`, B6.1 needs revisiting.
- C5. The earlier report that "ListAgents does not list 836818" is incorrect: it is listed as `primary-31`.

## Sources

- /home/li/primary/tools/msg, /home/li/primary/tools/messenger, /home/li/primary/tools/messaging.py, /home/li/primary/tools/hacky-messenger/hm.py and README.md, /home/li/primary/tools/claude-native-seat-refresh.py (lines 138-163)
- ~/.local/state/messenger/{pane_id,log}; ~/.local/state/hacky-messenger/836818.json; `systemctl --user status message-daemon.service`; `message --help`; `flow resolve 836818`
- `herdr --skill`; `herdr --session messaging-build agent get wD:p9`, `pane get`, `pane process-info --pane wD:p9`, `agent explain`, `api snapshot`; `herdr integration status`
- ~/.claude/settings.json hooks; ~/.claude/hooks/herdr-agent-state.sh; ~/.claude/sessions/*.json; ~/.codex/hooks.json, ~/.codex/config.toml; strings of the codex 0.153.4 binary
- Skills loaded through the Skill tool: messaging, testing-message-route, testing-datom-messaging, flow-communication, operational-layer-communication, subflow-scripts, subflow, flow-evidence. Sources in /git/github.com/LiGoldragon/Curriculum/skills/ (including main-flow.md line 4 and line 19, herdr.md, field.md)
- Transcripts: /home/li/.claude/projects/-home-li-primary/d8df703d-d083-4c29-9597-6b32e7411b75.jsonl (lines 565-692) and subagents/agent-a3e015f2cc65df095.jsonl, agent-a0498d5cdb034f420.jsonl
- Psyche records named in A6; the three added headings in /home/li/primary/flows/d8df70/vision/messaging.md
- `herdr api schema --json` (events.subscribe, pane_exited, pane_closed, pane_agent_status_changed); tools/native-seat-launch.mjs; tools/field-watcher
