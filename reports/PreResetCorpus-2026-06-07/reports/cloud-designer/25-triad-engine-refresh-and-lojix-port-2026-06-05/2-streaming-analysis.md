# Streaming / push subscriptions — resolve-or-explain (three-layer analysis)

Cloud-designer lane. 2026-06-05. Sub-report 2 of meta-report directory 25.

The lojix ordinary contract wants push subscriptions
(`WatchDeployments` / `WatchCacheRetention`) so a client can watch a
deploy progress live. Phase 1 reported "the schema-derived stack cannot
emit streams." This report investigates that claim precisely across
three layers and answers: is there a clear minimal fix, or a real
explanation? **There is a clear, honest answer, and it is more
encouraging than Phase 1 implied** — see the headline and the
recommendation.

All findings are read-only, cited `file:line`. The cloud component is
the working reference; everything below is grounded in source that is
checked in and (for cloud) builds end-to-end today.

## (a) What "streaming / push" even is, in plain English

A normal daemon call is a **question-and-answer over a phone line you
hang up immediately**. The client dials the daemon, says one thing
("give me the deploy status"), the daemon says one thing back, and the
line drops. That is *request / reply*. It is the only shape the cloud
daemon speaks today: in `cloud/src/daemon.rs:55-63` the daemon reads ONE
request frame, writes ONE reply frame, and `return`s — the connection is
finished. The client side mirrors it exactly
(`cloud/src/client.rs:55-71`): connect, send one, read one, done.

**Streaming / push is keeping the phone line OPEN and letting the daemon
keep talking after the first answer** — without the client asking again
each time. The client says once "watch this deployment," and then the
daemon sends a fresh little message every time something changes
("step 2 started"… "step 3 started"… "done"), all down the same open
line, for as long as the client stays connected. The client never
re-asks; the daemon decides when there's news and pushes it.

Why can't the current request-reply daemon do this? Three concrete
reasons, each at a different layer, and all three would have to change
together (or be bypassed) for push to work:

1. The daemon's loop is built to **answer once and hang up**. After it
   writes the reply it `return`s and forgets the connection. There is no
   place where it remembers "this client is still listening" and no
   later moment where it would send a second message.
2. The contract the client and daemon agree on has **no word for "an
   event"** — only "request" and "reply." A reply is the answer to a
   question; an event is unsolicited news. The schema language they're
   generated from can describe the first but has no grammar for the
   second.
3. Even the daemon's internal feature catalog (the Nexus schema) has no
   notion of "and also, whenever X changes, notify the watchers."

The good news, and the headline finding: **the lowest layer — the raw
wire kernel — already has the entire streaming machinery built and
sitting there unused.** The gap is not "streaming is impossible"; it is
"the schema-driven layers above the wire don't reach down to the
streaming machinery that already exists." That makes the honest fix much
smaller than Phase 1's framing suggested.

## (b) The problem decomposed by layer — what is missing at each

There are not three layers here but **four**, and naming the fourth is
the whole point. Phase 1 looked at three (schema grammar, emitter,
runtime) and concluded "cannot stream." It missed the wire kernel
underneath, where streaming is already implemented.

### Layer 0 — the wire kernel (`signal-frame`): streaming is ALREADY BUILT

This is the layer Phase 1 did not examine, and it changes the answer.
`signal-frame` already ships a complete streaming substrate:

- **A streaming frame body** with a dedicated daemon-initiated event
  variant: `StreamingFrameBody<RequestPayload, ReplyPayload,
  EventPayload>` with a `SubscriptionEvent { event_identifier, token,
  event }` arm (`signal-frame/src/frame.rs:65-84`). The comment is
  explicit: *"Frame body for a streaming channel — adds daemon-initiated
  subscription events"* (`frame.rs:61-64`). The event payload is a
  distinct type parameter from the reply payload, so events and replies
  cannot be confused on the wire.
- **A subscription event identity**: `StreamEventIdentifier`
  (`signal-frame/src/exchange.rs:119-138`) — *"an event is a stream
  item, not half of a request/reply pair"* — riding its own monotonic
  `LaneSequence` on the acceptor lane (`exchange.rs:53-90`), with the
  `sequence` field already reserved *"for future resume-from-N reconnect
  support"* (`exchange.rs:118`).
- **A subscription token**: `SubscriptionTokenInner`
  (`signal-frame/src/subscription.rs`) so a channel can be told "stop
  this particular subscription."
- **Observer bookkeeping**: an `ObservableSet` and `ObservationProjection`
  (`signal-frame/src/observable.rs`, exported at `lib.rs:59`) — the
  register / unregister / publish-to-all-subscribers machinery, with
  per-channel `OperationEvent` / `EffectEvent` projection hooks.
- **Lane direction already modeled**: `ExchangeLane::{Connector,
  Acceptor}` (`exchange.rs:45-51`) — the daemon (acceptor) owns its own
  outbound lane on which it can mint event frames independently of the
  client's request lane. This is exactly the "daemon keeps talking"
  capability.

So Layer 0 is **not** missing streaming. It is missing nothing. The
types compile and are exported (`signal-frame/src/lib.rs:52-53, 59,
66`). What's missing is that nothing above uses them.

### Layer 1 — schema grammar (`schema-next`): no event/stream construct

Confirmed. A `.schema` file's root shape is exactly **three positional
sections: Input root enum, Output root enum, namespace** — and nothing
else. The reader (`schema-next/src/source.rs:80-89` exposing
`input()` / `output()` / `namespace()`; assembly at
`source.rs:127-131`) and the ARCHITECTURE both state it:
*"optional imports, input root enum, output root enum, and namespace"*
(`schema-next/ARCHITECTURE.md:26`), and the root positions *"are known by
the schema reader … position supplies `Input` and `Output`"*
(`ARCHITECTURE.md:227-230`). A word-boundary grep across
`schema-next/src` for `stream | subscribe | subscription | event |
fanout | push | watch | persistent | opens | belongs` returns **zero**
grammar constructs (only ordinary `Vec::push` calls). There is no third
root, no `event` section, no `opens` / `belongs` relation keyword. The
grammar can describe a request enum and a reply enum; it has no syntax
for "a stream of events the daemon emits on its own."

### Layer 2 — emitter (`schema-rust-next`): no event-frame emission

Confirmed. The emitter (`schema-rust-next/src/lib.rs`, 139 KB) has **zero**
streaming / event-payload emission. A grep for `streaming |
StreamingFrameBody | EventPayload | operation_event | effect_event |
subscribe | fanout` in `src/lib.rs` returns nothing. The six occurrences
of `event` in the whole file are all **trace** events (the
instrumentation hooks), not wire events. Emission targets are
`WireContract`, `ComponentRuntime`, `SignalRuntime`, `NexusRuntime`,
`SemaRuntime` (`src/lib.rs:398-422`) — every one of them targets the
request/reply `ExchangeFrameBody` shape; none targets
`StreamingFrameBody`. The `signal_channel!` macro that the contract
crates actually invoke generates an **exchange-only** channel: the macro
comment at `signal-frame/src/frame.rs:44-46` says exchange-only channels
use `ExchangeFrameBody`, and *"for streaming, use `StreamingFrameBody`
instead"* — but no emitter or macro path reaches the streaming variant.
`signal-cloud/src/lib.rs:327-339` is the proof: `signal_channel! { channel
Cloud { operation … } reply Reply { … } }` declares operations and
replies, with **no events block**, because there is no syntax for one.

### Layer 3 — runtime (`triad-runtime`): request/reply-only, no push

Confirmed, and this is the layer most people miss when they assume "it's
just a socket, surely it can push." It cannot, as written. The daemon
runner is structurally one-shot:

- `DaemonRuntime::handle_stream(&mut self, stream) -> Result<(),
  RequestError>` (`triad-runtime/src/daemon.rs:20`) — the contract is
  "take a stream, handle it, return." There is no "and keep it for
  later," no subscriber registry, no handle back to the connection after
  the method returns.
- `serve_streams` (`daemon.rs:149-161`) is a plain accept loop:
  accept a connection, call `handle_stream`, move to the next
  connection. It is single-threaded and **synchronous** — while it is
  inside one `handle_stream` it cannot be pushing to anyone else, and
  once `handle_stream` returns the stream is dropped.
- The cloud daemon's concrete handler proves the shape:
  `serve_ordinary_stream` reads a request and `return Ok(())` right after
  writing the single reply (`cloud/src/daemon.rs:55-63`). One request in,
  one reply out, connection closed.
- The Nexus action loop (`triad-runtime/src/runner.rs`) has exactly five
  next-step outcomes — `Reply`, `SemaWrite`, `SemaRead`, `RunEffect`,
  `Continue` (`runner.rs:21-28`) — and the loop **terminates by
  returning a single `Reply`** (`runner.rs:154-156`). There is no
  `Emit` / `PublishEvent` / `KeepWatching` outcome. The engine is a pure
  function from one input to one reply; it has no channel on which to
  emit a second, later message.
- `StreamingFrameBody` is **not referenced anywhere in
  `triad-runtime/src`** — grep is empty. The runtime is exclusively
  built on the request/reply `ExchangeFrameBody`.

So Layer 3 is genuinely request/reply-only. It has no push, no
persistent-connection handling, no event fanout. The streaming
machinery in Layer 0 is, from the runtime's point of view, dark.

### The decomposition in one sentence

Streaming is **fully built at Layer 0 (the wire kernel) and entirely
absent at Layers 1–3 (grammar, emitter, runtime).** The fix is not
"invent streaming"; it is "connect the schema-driven layers to the
streaming kernel that already exists" — or, more cheaply, "let one
specific daemon talk to the streaming kernel directly, bypassing the
schema layers, for this one capability."

## (c) The options, with honest effort and risk

### Option 1 — full schema-derived streaming (the "proper" path)

Teach the whole schema stack to emit streaming channels so that
`WatchDeployments` is a first-class schema construct, generated like any
other operation. Concrete changes, layer by layer:

- **schema-next grammar**: add a third root section (an `Event` root
  enum) or a relation keyword (e.g. `subscribe Operation -> Event`) to
  the `.schema` root shape. This is the large piece: the root shape is
  currently hard-coded to exactly Input + Output + namespace
  (`source.rs:80-131`), and the reader, the macro registry positions
  (`ARCHITECTURE.md:11-12`), the resolver, and every `.schema` round-trip
  test assume three sections. Adding a fourth root is a grammar change
  that ripples through the reader, the lowering, and the macro position
  dispatch.
- **schema-rust-next emitter**: add a `StreamingRuntime` emission target
  (or extend the existing ones) that emits the `StreamingFrameBody`
  channel instead of `ExchangeFrameBody`, projects the new `Event` root
  to the `EventPayload` type parameter, and emits the
  `ObservableSet`-backed publish surface. New emission code paths
  parallel to the entire existing channel emitter.
- **triad-runtime runtime**: add a sixth Nexus action
  (`EmitEvent` / `PublishToSubscribers`), a subscriber registry the
  daemon holds across connections, a per-connection writer handle that
  outlives `handle_stream`, and an event-fanout path on the acceptor
  lane. This is a real concurrency change: the current synchronous
  single-listener `serve_streams` (`daemon.rs:149-161`) cannot hold open
  connections AND accept new ones without either threads-per-connection
  or an async runtime. The runtime explicitly **defers** "actor mailbox,
  backpressure, runtime-control" work (component-triad.md §"Nexus
  mechanism substrate," citing Spirit 1483); persistent-connection
  fanout lands squarely in that deferred zone.

**Effort: large** (weeks, touching three core repos that every component
depends on). **Risk: high to the whole workspace** — it changes the
schema grammar and the shared runtime, so a mistake regresses *every*
component, not just lojix. **Reward: this is the architecturally right
end-state** and matches the workspace's own `Subscribe` Sema class and
push-not-pull intent (`component-triad.md` §3 Sema table:
*"Subscribe | observer ↔ producer | initial state + commit-deltas
(push, not poll)"*). But it is a workspace-platform project, not a lojix
port task.

### Option 2 — pragmatic non-schema-derived push (hand-written, on the existing kernel)

Keep the schema-derived request/reply for everything else, and
hand-write ONE streaming path for the watch operations, built directly
on the `StreamingFrameBody` machinery that **already exists** in
`signal-frame`. The contract still does the normal handshake; the watch
operation is a request that, instead of returning one reply and hanging
up, switches the connection into "keep emitting `SubscriptionEvent`
frames" mode.

What it would look like, concretely:

- The lojix daemon, for the `WatchDeployments` request only, does NOT
  `return` after the first reply. Instead it keeps the `UnixStream` and,
  on its acceptor lane, writes `StreamingFrameBody::SubscriptionEvent {
  event_identifier, token, event }` frames
  (`signal-frame/src/frame.rs:78-83`) as deploy steps progress — exactly
  the variant the kernel already provides.
- It uses `StreamEventIdentifier` (`exchange.rs:119-138`) for event
  identity and `SubscriptionTokenInner` (`subscription.rs`) for the
  client's "stop watching" retraction — both already built.
- It registers the watching connection in an `ObservableSet`
  (`observable.rs`, already exported) and publishes deploy-step events to
  all current watchers.
- The lojix-cli's watch command opens the connection and loops reading
  `SubscriptionEvent` frames until the deploy finishes or the user
  interrupts — a hand-written read loop, not the generated single-reply
  client.

**Is it feasible? Yes — and this is the load-bearing finding.** Every
wire primitive it needs is already implemented and exported in
`signal-frame`. The hand-written part is: (1) a daemon-side branch that
keeps the connection and emits events (this DOES need a thread per
watching connection or a small async island, because the synchronous
`serve_streams` can't hold-open-and-accept simultaneously — see Layer 3),
and (2) a client-side read loop. No grammar change, no emitter change, no
change to the shared runtime that other components depend on.

**Effort: small-to-moderate** (days, in the lojix repo only — the
deploy-watch daemon handler plus the cli watch loop, plus the
threads-per-watcher or async-island concurrency for the daemon's
hold-open path). **Risk: low and contained** — it lives entirely in
lojix; if it's wrong, only lojix watch is affected. **Cost: it's a
carve-out.** The watch path is hand-written and not visible in the
schema feature catalog, which is a real (acknowledged) violation of the
"every feature is a declared Nexus verb" rule (record `z6qu`). That
carve-out is honest and documentable, and it is the same shape as the
named data-plane carve-out the workspace already permits
(`component-triad.md` §"Named carve-outs" #2: high-bandwidth byte paths
get a separate socket outside the schema-framed triad).

### Option 3 — poll-only (client repeatedly Queries)

Don't stream at all. The lojix-cli `watch` command becomes a loop:
`Query(DeploymentStatus)` every N seconds, print the diff, repeat until
the deploy reaches a terminal state. This needs **zero** new
infrastructure — it uses the request/reply path that already builds and
works today (`cloud/src/client.rs:55-71` is the exact shape, already
green).

**Does it suffice for deploy-watch?** For the deploy-watch use case
specifically — **yes, comfortably.** A deploy is a coarse-grained,
minutes-long, monotonic-progress process (build → push → activate →
done). A human watching a deploy does not need sub-second push; a 1–2
second poll renders an indistinguishable "live" experience and is how
most real deploy CLIs (terraform, kubectl rollout status without
`--watch`, many CI dashboards) actually work under the hood. The only
real cost is a query every second or two while a deploy runs, which is
trivial load for a Unix-socket daemon.

**Effort: trivial** (hours, lojix-cli only). **Risk: none** — uses the
proven path. **Cost: it's poll, not push** — slightly more daemon
queries, and it does not satisfy the long-term push-not-pull intent. But
for *this* use case the user-visible difference is essentially nil.

## (d) Recommendation

**Ship Option 3 (poll) now for the cutover; design toward Option 2
(hand-written push on the existing kernel) as the near-term improvement;
treat Option 1 (full schema-derived streaming) as a separate
workspace-platform project, not part of the lojix port.**

Reasoning:

1. **It does not block cutover, because lojix-cli — the thing being
   replaced — has no streaming either.** The current lojix-cli watches a
   deploy by inheriting/capturing the unit's stdout/stderr as it runs
   (`lojix-cli/src/activate.rs:22, 130`; `lojix-cli/src/process.rs:56-99,
   186-214`) — i.e. it watches a *child process's pipe*, which is a local
   stdout stream, not a daemon push-subscription at all. There is **no
   `WatchDeployments` / `WatchCacheRetention` push subscription in the
   tool being replaced.** So the new daemon does not regress anything by
   launching without push. The watch feature is an *enhancement the new
   contract aspires to*, not parity the cutover requires. This removes
   all urgency from the streaming question and is the single most
   important fact for the psyche: **streaming is not on the cutover
   critical path.**

2. **Poll is genuinely adequate for deploy-watch** (Option 3 rationale
   above): a deploy is minutes-long and coarse; a 1–2s poll is
   indistinguishable from push for a human, and it runs on the path that
   already builds green today.

3. **When push is actually wanted, Option 2 is small and self-contained,
   because the hard part is already done.** Phase 1's "the schema-derived
   stack cannot emit streams" is true but incomplete: the *wire kernel*
   can, and it's fully built (`StreamingFrameBody`, `StreamEventIdentifier`,
   `SubscriptionTokenInner`, `ObservableSet`). A hand-written watch path
   in lojix, on top of that kernel, is a days-scale, lojix-only change
   with low blast radius — the same carve-out shape the workspace already
   blesses for data-plane sockets. We should not block cutover on it, but
   it is a clear, cheap follow-up when someone wants true live push.

4. **Option 1 is the right end-state but the wrong scope for now.** Full
   schema-derived streaming is the architecturally pure answer and aligns
   with the workspace's own `Subscribe` Sema class and push-not-pull
   intent — but it changes the schema grammar and the shared runtime that
   *every* component depends on, with high blast radius, and it lands in
   the explicitly-deferred deeper-runtime zone (Spirit 1483). It deserves
   its own designed project with the psyche's sign-off, not a quiet
   inclusion in a port.

Concrete steps for the recommended path:

- **Now (cutover):** in lojix-cli's new client, implement `watch` as a
  poll loop over the existing request/reply `Query` operation — terminal
  state ends the loop. No schema change, no daemon change beyond having a
  status query (which the contract already wants). Ships on the green
  path.
- **Near-term (when live push is wanted):** add a hand-written
  `WatchDeployments` streaming handler in the lojix daemon built on
  `signal-frame`'s `StreamingFrameBody` + `ObservableSet`, with a
  thread-per-watcher (or a small async island) so the daemon can
  hold the watch connection open while still accepting new connections;
  add the matching read-loop in the cli. Document it as a named
  streaming carve-out in lojix's ARCHITECTURE, exactly parallel to the
  data-plane carve-out precedent.
- **Long-term (platform):** if/when multiple components want push, open a
  designer project for Option 1 — schema-grammar event root +
  `StreamingRuntime` emission target + the sixth Nexus `EmitEvent` action
  and subscriber registry in triad-runtime — as a deliberate workspace
  upgrade with the psyche's authority.

## (e) What I am unsure about — open questions for a human to weigh

1. **Is the wire kernel's streaming substrate intended to be reached via
   schema, or is it pre-positioned for a future grammar?** `signal-frame`
   has the full streaming machinery built and exported but unused by any
   schema-driven path. I cannot tell from source whether this is (a)
   scaffolding deliberately laid down ahead of a planned Option-1 grammar
   change, or (b) leftover from an earlier design. If (a), Option 1 may
   be more partially-done than I've credited, and someone with the intent
   history should say so. **This is the question whose answer most
   changes the effort estimates above.**

2. **Does lojix actually need live push, or is poll the permanent
   answer?** I'm assuming deploy-watch is the only streaming use case and
   that poll suffices for it. If `WatchCacheRetention` (or a future
   capability) needs genuinely high-frequency or low-latency push, Option
   3 stops being adequate and Option 2 becomes near-term-required rather
   than optional. The psyche knows the real watch use cases; I'm
   inferring from the contract names.

3. **Concurrency model for the Option-2 daemon hold-open path.** The
   current `serve_streams` is synchronous single-listener
   (`daemon.rs:149-161`). Holding a watch connection open while accepting
   new connections needs either thread-per-watcher or an async island,
   and the workspace has explicitly deferred the deeper async-runtime
   work (Spirit 1483). I'm unsure which the workspace would prefer for a
   one-off carve-out, and whether even a contained thread-per-watcher in
   lojix is considered acceptable given that deferral. A platform-owner
   call.

4. **Whether a hand-written push carve-out is acceptable at all given
   record `z6qu`.** The Nexus-feature-catalog rule says every internal
   feature must be a declared schema verb. Option 2's watch path would be
   hand-written and schema-invisible. I've argued it's the same shape as
   the blessed data-plane carve-out, but whether the psyche accepts a
   *control-plane* push carve-out (vs. only data-plane byte carve-outs)
   is a judgment I can't make for them.

5. **Whether the `sequence` resume-from-N reconnect field implies a
   durability expectation.** `StreamEventIdentifier`'s sequence is
   reserved "for future resume-from-N reconnect support"
   (`exchange.rs:118`). If watch subscriptions are expected to survive a
   client reconnect (replay missed events), that's a stateful-subscription
   feature well beyond Option 2's fire-while-connected model, and it would
   pull the design back toward Option 1. I don't know if reconnect-resume
   is a requirement or just a reserved-for-later field.
