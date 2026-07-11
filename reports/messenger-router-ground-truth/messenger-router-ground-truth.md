# Messenger / Router ground truth — route-back and the local Send path

Read-only scout map of landed code, verified against source (no redesign, no
recommendations). Every load-bearing claim carries a `file:line`. Facts are
separated from the few interpretations, and open unknowns are named at the end.

Repos read (local clones under `/home/li/primary/repos/`): `message`
(component "messenger"), `router`, `orchestrate`, `harness`, `terminal-cell`.
Contract crates `signal-message`, `signal-router`, `signal-harness` were read
where the wire vocabulary lives.

## Headlines

- Route-back is discovered, stored, and resolved entirely by **orchestrate**,
  not the messenger. At `RegisterAgent`, orchestrate walks `/proc` ancestry from
  the SO_PEERCRED caller pid, matches an ancestor against terminal-cell session
  directories, stores the session's `data.sock` path, and pushes it to the
  router as a `RegisterActor`. A later Send resolves the minted identity through
  the router's in-memory actor registry.
- The believed mechanism in the brief is **confirmed** in code, with two
  precisions: the persisted address is the terminal-cell `data.sock` path (plus
  pid and process start-time pin), and the actor registry that resolves it is
  **in-memory in the router**, not durable.
- The **local Send hop chain** is: `message` CLI → messenger daemon → router
  daemon → recipient endpoint. For a terminal-cell agent the last hop is the
  router writing a `'P'` programmatic-input frame to the cell's `data.sock`,
  which injects into the live PTY session. Every hop exists in landed code.
- The messenger is a **stateless stamp-and-forward ingress** — it owns no
  durable state at all. The router owns the inbox/message store, delivery,
  the actor registry, remote forwarding, channel/adjudication machinery, mirror
  policy, cryptographic peer sessions, and component supervision.
- The split the psyche suspects is visible in code: the router accretes several
  subsystems beyond routing, and the messenger has been reduced to provenance
  stamping. Stated as observations with evidence in "Ambiguous seams".

## Messenger (message component) surfaces

### CLI

`message/src/command.rs:14` — the CLI `Input`:

```
pub enum Input {
    Send(RecipientName, String, ThreadSelection),
    Inbox(RecipientName),
}
```

The "4-field positional Send" is the NOTA arity including the head atom `"Send"`;
the decoder enforces exactly 4 slots (head + recipient + body + thread) at
`message/src/command.rs:67-73`. The three payload fields are `RecipientName`
(`message/src/surface.rs:17`), the `String` body, and `ThreadSelection`
(`message/src/surface.rs:65`: `None | Named(ThreadName)`).

There is no distinct wire "Send" operation. CLI `Send` maps to a wire `Submit`
carrying `MessageKind::Send` (`message/src/command.rs:33-40`); `Inbox` maps to
`QueryInbox`.

### Daemon

The messenger daemon holds **no durable state**. `MessageEngine` carries exactly
one field, a `RouterForwarder` (`message/src/engine.rs:44-46`); the header states
"Message owns no durable state: it is a stamp-and-forward ingress"
(`message/src/engine.rs:6`) and the SEMA (state) plane returns `Stateless` for
every read/write (`message/src/engine.rs:227-243`). Meta/live-reconfig is stubbed
to an Unimplemented reply (`message/src/daemon.rs:90-94`).

What the daemon does with a Send: `decide_signal` turns a `Submit` into a
`ForwardToRouter` effect (`message/src/engine.rs:139-158`); the effect runner
calls `RouterForwarder::forward` (`message/src/engine.rs:114-130`), which opens a
`UnixStream` to the router socket and submits a **published `signal-message`**
frame (`message/src/router.rs:63-70`, `332-345`).

Provenance is minted here (not threads): the message origin is derived from the
connection's SO_PEERCRED peer credentials via `OriginPolicy`
(`message/src/router.rs:265-286`) and a daemon ingress timestamp is stamped
(`message/src/router.rs:367-377`); origin is never taken from the payload
(`message/src/router.rs:364-366`). The wire request sent to the router is
`SignalMessageInput::SubmitStamped(StampedMessageSubmission)` or `QueryInbox`
(`message/src/router.rs:352-360`).

Not found in the messenger: any thread minting/derivation (a `ThreadSelection`
including `None` is forwarded verbatim, `message/src/router.rs:395-402`), any
thread index, topic table, recipient registry, or store.

## Router surfaces

### Wire operations

Primary runtime enum `RouterInput` (`router/src/router.rs:4537`): `RegisterActor`,
`RouteMessage`, `Status`, `GrantChannel`, `RetractChannel`,
`InstallStructuralChannels`, `ApplyMindChannelGrant`, `ApplyMindAdjudicationDeny`.
The published `signal-message` contract path arrives separately as
`ApplySignalMessage(SignalMessageInput)` → `apply_signal`
(`router/src/router.rs:2390-2406`): `SubmitStamped` →
`apply_stamped_message_submission`, `QueryInbox` → `signal_inbox`. Inbound tailnet
forwards arrive as `ApplyForwardedMessage` after attestation verify
(`router/src/router.rs:1668`).

### Actor registration and storage

`RegisterActor` wraps `Actor { name: ActorIdentifier, pid: u32, endpoint:
Option<EndpointTransport> }` (`router/src/message.rs:92`, `127`). `EndpointKind`
= `Human | HarnessSocket | PtySocket | ComponentSocket`
(`router/src/message.rs:145`). Registered actors live in an **in-memory**
`HashMap<ActorIdentifier, HarnessRegistration>` inside the `HarnessRegistry`
Kameo actor (`router/src/harness_registry.rs:10-14`); insertion is last-wins and
reports `EndpointUpdated` vs `Registered` (`router/src/harness_registry.rs:27-37`,
`router/src/router.rs:2697-2705`). The registry is **not** persisted — `RouterStore`
has no actor table (`router/src/tables.rs:52-62`).

### Local delivery (resolve + deliver)

`apply_stamped_message_submission` (`router/src/router.rs:2628-2654`): assigns a
slot, persists the message to the durable `messages` log, persists an outbound
backlog row, pushes onto the in-memory `pending` queue, then drives
`retry_pending`. `retry_pending` asks the registry for the endpoint by recipient
identity (`ReadHarnessDeliveryTarget`, `router/src/router.rs:2973-2985`); a miss
falls to remote-route resolution or parks (`:2986-3055`); a hit hands the stored
`Actor` to the `HarnessDelivery` actor via `DeliverHarness`
(`router/src/router.rs:3079-3087`).

`HarnessDelivery::deliver` (`router/src/harness_delivery.rs:35-57`) connects to
`endpoint.target` and dispatches by kind:
- `PtySocket` → `UnixStream::connect(path)`, writes `b"P"` + big-endian length +
  NOTA message text, reads one acceptance byte `b'A'`
  (`router/src/harness_delivery.rs:59-69`).
- `HarnessSocket` → connects and writes a `signal-harness`
  `HarnessRequest::MessageDelivery` frame, reads a `HarnessEvent`
  (`router/src/harness_delivery.rs:71-102`).
- `ComponentSocket` → writes routed objects (`:130-146`); `Human` → not delivered.

### Local authorization vs network crossing

Local delivery is **default-authorized by locality** — confirmed. The
`ChannelAuthority::check` / `NeedsAdjudication` / `MindAdjudicationOutbox::record`
machinery is **never invoked on the delivery path** (verified by absence of any
caller outside its defining files); the inline comment states a locally-registered
actor needs no per-pair channel grant and that the channel authority, adjudication
requests, and mind outbox "stay wired … but no longer gate the normal
local-delivery path" (`router/src/router.rs:3056-3065`, `3109-3112`). Channels are
still granted/persisted via meta ops, just not consumed on delivery.

Network crossing keeps a separate ceremony: outbound `resolve_remote_route` →
`DeliverRemote` off-mailbox with a durable backlog (`router/src/router.rs:3020-3054`);
inbound `handle_forward` verifies a criome attestation before applying
(`router/src/router.rs:388-419`, `forward_attestation.rs`, `criome_client.rs`,
`peer_session.rs`, `identity_proof.rs`).

## The local Send hop chain (traced from code)

1. `message '(Send <recipient> <body> <thread>)'` — CLI encodes a wire `Submit`
   (`message/src/command.rs:33-40`) and connects to the messenger socket
   (`message/src/command.rs:24-27`).
2. **Messenger daemon** decides `ForwardToRouter`, stamps provenance from
   SO_PEERCRED + ingress time, and submits `SubmitStamped` to the router
   (`message/src/engine.rs:139-158`, `message/src/router.rs:352-377`).
3. **Router** `apply_stamped_message_submission` persists to the `messages` log,
   assigns a slot, enqueues, and runs `retry_pending`
   (`router/src/router.rs:2628-2654`).
4. Router resolves the recipient identity in the **in-memory actor registry**
   (`router/src/router.rs:2973-2985`) and hands the endpoint to `HarnessDelivery`.
5a. Terminal-cell recipient (`PtySocket`): router writes a `'P'` programmatic-input
   frame to the cell's `data.sock`; **terminal-cell** handles
   `PROGRAMMATIC_INPUT_REQUEST = b'P'` (`terminal-cell/src/socket.rs:33`,
   `102-106`) and injects it as `InputSource::Programmatic` into the live PTY
   session, replying `ACCEPTANCE_REPLY = b'A'` (`terminal-cell/src/socket.rs:41`).
   These bytes match the router frame exactly.
5b. Harness-managed pi recipient (`HarnessSocket`): router writes a
   `MessageDelivery` frame to the **harness daemon** socket
   (`router/src/harness_delivery.rs:71-102`); the harness injects into pi either
   by writing a JSON `steer`/`prompt` command to the pi child's stdin
   (`harness/src/pi.rs:188-236`) or by writing PTY input to a terminal socket
   (`harness/src/terminal.rs:150-201`), selected by instance config
   (`harness/src/daemon.rs:482-492`).

Every hop exists in landed code. Path 5a is proven coherent across router +
terminal-cell source. Path 5b is exercised by the harness e2e tests (see
Unknowns for which path the tests use).

## Route-back: discovery, storage, resolution

Discovery (`orchestrate/src/agent_reachability.rs`): at `RegisterAgent`,
orchestrate reads the peer's kernel-vouched pid from SO_PEERCRED
(`orchestrate/src/daemon.rs:112-124`), then walks `/proc/<pid>/stat` parent links
up toward pid 1 (`agent_reachability.rs:137-158`) and matches each ancestor
against terminal-cell session directories under
`$TERMINAL_CELL_RUNTIME_DIR/terminal-cell` (`:203-221`). A session directory
`session-<stem>-<millis>` holds `child.pid` / `daemon.pid`; the walk matches an
ancestor pid against those (`:238-262`).

Stored address (`orchestrate/src/tables.rs:199-204`,
`agent_reachability.rs:92-108`): `StoredAgentReachability { endpoint_kind:
TerminalCell, target: <session>/data.sock, harness_pid, harness_start_time }`.
The `harness_start_time` (from `/proc` stat field 22) pins the process generation
so a recycled pid is disambiguated (`tables.rs:194-204`). Reachability is `None`
at registration and populated only by discovery; a TCP peer or no `/proc` match
leaves the agent registered without reachability (`tables.rs:180-192`,
`execution.rs:4852-4869`).

Router propagation (`orchestrate/src/router_registration.rs`): on a discovered
match, orchestrate opens the router working socket and sends
`Input::RegisterActor(Actor)` with the minted identity as `ActorIdentifier`, the
harness pid as the process, and `EndpointTransport { PtySocket, data.sock path }`
(`router_registration.rs:52-95`; `TerminalCell` → `PtySocket` at `:90-95`). This
leg is best-effort — a down/refusing router is recorded as a divergence, never a
registration failure (`execution.rs:4884-4919`).

Resolution: a later Send resolves the recipient's minted identity through the
router's in-memory registry (`router/src/router.rs:2973-2985`) to that stored
endpoint, and delivers as in the hop chain above.

The believed mechanism in the brief is confirmed. Precisions: the persisted
"endpoint" is the terminal-cell `data.sock` path (not a live socket handle), and
the resolving registry is ephemeral router memory — a router restart drops all
route-back targets until agents re-register.

## Ownership map

Messenger owns: nothing durable. Per-request it mints provenance (origin +
ingress timestamp) and forwards (`message/src/engine.rs:6`, `44-46`;
`message/src/router.rs:234-286`).

Router owns (durable, `router/src/tables.rs:52-62`): the `messages` inbox log,
`delivery_attempts`, `delivery_results`, granted `channels`,
`adjudication_pending`, `mirror_switch`, `outbound_backlog`, `remote_routes`.
Router owns (in-memory child actors): the actor registry
(`harness_registry.rs:10-14`), channel map + adjudication queue (`channel.rs`,
`adjudication.rs`), remote-router registry (`remote_router.rs`), the `pending`
delivery queue, trace, and sequence counters. Threads are carried as a plain
field on each stored message record (`router/src/tables.rs`, `StoredMessageRecord`
thread field), not as an indexed entity.

Orchestrate owns: the minted agent identity, the topic tree and agent registry
(`orchestrate/src/tables.rs`), and the **reachability discovery + router
registration** logic (`agent_reachability.rs`, `router_registration.rs`).

Terminal-cell owns: the live PTY session, its `control.sock` and `data.sock`, and
the programmatic-input injection path (`terminal-cell/src/socket.rs`,
`lifecycle_cli.rs`).

## Ambiguous seams (observations, not recommendations)

- Route-back logic lives in **orchestrate**, not the messenger: discovery
  (`agent_reachability.rs`), the persisted endpoint (`tables.rs:199-204`), and the
  router `RegisterActor` push (`router_registration.rs`). The messenger is not
  involved in making an agent reachable.
- The messenger is reduced to a provenance stamper: no store, no thread minting,
  no registry, meta stubbed (`message/src/engine.rs:6`, `227-243`;
  `message/src/daemon.rs:90-94`). The inbox it exposes (`QueryInbox`) is a pass-through
  to the router's `messages` store (`message/src/router.rs:356-360`;
  `router/src/router.rs:2401-2404`).
- The router carries subsystems beyond local routing: durable inbox/delivery
  bookkeeping (`tables.rs`), an actor-name→endpoint registry
  (`harness_registry.rs`), a per-pair channel-grant + mind-adjudication policy
  engine that is wired and persisted but not consulted on local delivery
  (`channel.rs`, `adjudication.rs`, `router.rs:3056-3065`), mirror/routed-object
  origination behind an owner switch (`router.rs:2752-2765`, `mirror_switch`
  table), cryptographic peer sessions + attestation verification (`peer_session.rs`,
  `identity_proof.rs`, `criome_client.rs`, `forward_attestation.rs`), and a
  component-supervision responder on its own socket (`supervision.rs`).
- The channel/adjudication/mind machinery is present-but-dormant on the local
  path: it can grant, persist, and record, but no code path gates local delivery
  through it (`router.rs:3056-3065`; no caller of `ChannelAuthority::check`).

## Unknowns / not verified

- **Two route-back topologies coexist and only one is tested end-to-end.**
  Orchestrate's discovery produces a `PtySocket`/terminal-cell `data.sock`
  endpoint (`router_registration.rs:90-95`). The harness repo's e2e tests instead
  register a `HarnessSocket` endpoint pointed at the harness daemon
  (`harness/tests/message_router_harness_pi_steer_e2e.rs:345-349`,
  `message_router_harness_e2e.rs:293-296`). I did not find a test that exercises
  the orchestrate-discovered `PtySocket`→terminal-cell path end-to-end; its
  coherence is established by matching source (router `'P'` frame ↔ terminal-cell
  `PROGRAMMATIC_INPUT_REQUEST`), not by a passing e2e.
- Which delivery topology is the intended default for a real registered agent
  (terminal-cell PtySocket vs harness-daemon HarnessSocket) is not settled in the
  code I read; orchestrate hard-maps discovery to `PtySocket`, while the harness
  suite drives `HarnessSocket`.
- Thread ownership: threads are a stored field on router message records, not an
  indexed entity. Whether the router, messenger, or a future component owns a
  thread index is undecided in code (matches the design report's "deliberately
  open"). Not further verified.
- The messenger↔router `signal-message` contract compatibility and the exact
  `MessageSubmission`/`StampedMessageSubmission` wire fields were read only where
  cited; I did not audit the full contract crate.
- The harness `Steer` behaviour is a pi stdin-JSON command `type`, not a harness
  wire operation; `InteractionPrompt`/`DeliveryCancellation` are accepted but
  unimplemented (`harness/src/daemon.rs:1495-1500`). Not exercised beyond the
  cited tests.
</content>
</invoke>
