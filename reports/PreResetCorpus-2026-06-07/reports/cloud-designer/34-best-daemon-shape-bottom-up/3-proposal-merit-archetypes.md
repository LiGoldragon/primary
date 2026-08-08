# 3 — Proposal C: merit-chosen archetypes

cloud-designer, 2026-06-07. One of three independent best-architecture proposals
under the zero-backward-compatibility mandate (Spirit `ax2k`, Maximum). Every
component is expected to change; non-disruption is never a virtue here. Built on
the ground facts in `33/1-3` (emitter internals, runtime seams, consumer shapes),
re-read against the GENUINE source of all five consumers, not their current code
shape.

## Philosophy

The emitter generates a **small fixed set of daemon archetypes**, and a component
gets an archetype because of **what it genuinely is**, never because of what it
already happens to be. The archetype is a schema-declared property of the
component's nature; the emitter reads that property and emits the whole spine for
it. The hand-written hook surface is then **mostly the real algorithm** — match a
typed input, make the decision, call the next typed interface, return a typed
output — because the archetype already supplied every byte of plumbing that
archetype's shape implies.

The merit claim is narrow and falsifiable: **two archetypes, not one and not
five.** One archetype (proposal A) forces a single shape onto components whose
natures genuinely differ on ONE axis. Five archetypes (one per component) is the
compat reflex wearing a new hat — it preserves each component's accident. The
right number is the number of GENUINELY-DISTINCT natures, and the reading below
finds **exactly two**.

## The single axis that actually divides the five

I read every consumer's real source (`33/3` plus the live trees). The striking
finding: on the concurrency-and-engine axis, **all five are the SAME**. None of
them genuinely wants a different request-execution model:

- **lojix** — `Arc<Store>`, fresh per-request `SchemaRuntime`, offloaded onto
  `BoundedWorkers`. Request/reply.
- **cloud** — `Arc<SchemaStore>`, fresh per-request `SchemaRuntime`. Identical to
  lojix MINUS the `BoundedWorkers` offload (serial today purely by omission, not
  by desire — `33/3` confirms cloud "would adopt almost verbatim").
- **message** — the brief calls it "a kameo actor daemon with its own actor
  concurrency." **It is not.** `message/Cargo.toml` has no `kameo`, no `tokio`, no
  actor dependency. The real source is `type Engine = Mutex<MessageEngine>` over
  the emitted **single-listener** spine, and `MessageEngine::handle` is a
  **synchronous blocking** stamp-and-forward: `RouterForwarder::forward` does
  `UnixStream::connect` + write + read to the router (`router.rs:58-63`) on the
  request thread. message has NO durable store and NO real concurrency. Its
  "actor" nature is aspirational. Today it is request/reply that BLOCKS on a
  downstream socket — the exact case `BoundedWorkers` exists to unblock. message
  genuinely WANTS concurrency it does not have.
- **spirit** — long-lived `Engine` over redb behind `&self`, request/reply. PLUS a
  subscription surface. The subscription surface is the one thing that looks like a
  second nature — examined next.
- **repository-ledger** — `Arc<Mutex<Store>>`, request/reply per listener thread,
  plus a 2-second spool-ingest background loop. Request/reply with a periodic
  side-task.

So four of five are pure request/reply-over-a-shared-store, and the fifth
(spirit) is request/reply PLUS something. The "something" is the only candidate
for a second archetype. Everything turns on what that something actually is.

### What spirit's streaming surface actually IS (the load-bearing reading)

The brief frames spirit as needing "a streaming subscription surface" as if that
implied a long-lived per-subscriber loop or an event-loop actor. **It does not.**
Reading the emitted streaming wiring (`spirit/src/schema/daemon.rs`,
`EmittedSubscriptions`) and `triad-runtime/src/streaming.rs`:

1. A `SubscribeIntent` request arrives on the **ordinary request/reply path** like
   any other request. The emitted `handle_working_stream` runs the normal
   decode→execute→encode, AND THEN: if the output yields a `subscription_token`,
   it `try_clone()`s the connection's writer and **registers the cloned writer in
   a shared `Mutex<SubscriptionState>`** owned by the runtime. The request thread
   then returns. There is no loop. The subscriber's socket is parked in a HashMap.
2. A later, unrelated `Record` request arrives on the request/reply path, commits,
   and produces an event via `published_event`. That request's thread calls
   `subscriptions.publish(event)`, which walks the registry and writes the event
   frame to every matching parked writer — **on the committing request's thread.**

So spirit's streaming is **request/reply PLUS a shared, request-outliving writer
registry**. Delivery is fan-out done synchronously by whichever request commits an
event. There is NO long-lived subscriber loop, NO event-loop, NO actor mailbox.
The "streaming archetype" is the request/reply archetype with ONE added owned
noun: a registry of parked writers that survives across requests.

This collapses the apparent second axis. Streaming is not a different concurrency
model; it is **a request/reply daemon that holds cross-request fan-out state.**

## The exact criterion: `RequestDisposition`

The schema-declared property that selects the archetype is the **disposition of a
request's reply** — does a request produce exactly one reply and then the
connection is done, or can a request **subscribe** the connection to a stream of
later events? This is a property of the component's CONTRACT, derivable from the
schema, not a build.rs accident:

```
RequestDisposition  [ReplyOnce ReplyThenSubscribe]
```

- **`ReplyOnce`** — every operation root maps input→one output, connection closes.
  The daemon holds no cross-request delivery state. → **REQUEST/REPLY archetype.**
- **`ReplyThenSubscribe`** — at least one operation root opens a subscription: its
  output carries a subscription token and the contract declares `streams` (the
  event payload type and the filter). The daemon must hold a cross-request writer
  registry and fan events out. → **STREAMING archetype.**

The criterion is **schema-derived, exactly as the existing `emits_stream` flag
already is** (`DaemonModule::new`, `daemon_emit.rs:155`:
`!schema.streams().is_empty()`). The precedent is in the emitter TODAY: the daemon
emitter already keys subscription plumbing off whether the schema declares
streams. Proposal C promotes that one derived bit to **the** archetype selector
and gives it a name. A component does not DECLARE its archetype in build.rs; the
emitter READS it from the contract schema. That is the readability thesis applied
to the selector itself: the schema names the interface, and the interface's shape
(does any root return a subscription token over a declared stream) names the
daemon archetype. No human chooses; the contract decides.

The criterion is NOT "does it have a meta tier" and NOT "does it run long
effects." Those are orthogonal:

- **Tiers are orthogonal to archetype.** Both archetypes support a working tier
  and an optional owner/meta tier. lojix (request/reply) has two tiers; message
  (request/reply) has one; spirit (streaming) has two. Tiering is a separate
  schema property (`meta_contract_module: Option<…>`), handled identically in both
  archetypes (see "Meta tier" below).
- **Effect duration is orthogonal to archetype.** lojix's multi-minute nix build
  is a request/reply request that happens to take minutes. It does not stream — it
  produces ONE reply when the build finishes. The thing that makes long effects
  bearable is **concurrency** (offload so the accept loop stays live), which BOTH
  archetypes carry as an always-on property (see "Concurrency" below), not the
  streaming archetype.

## Mapping all five consumers

| Consumer | Genuine nature | `RequestDisposition` | Archetype | Tiers | What it gains |
|---|---|---|---|---|---|
| **lojix** | per-request engine over `Arc<Store>`, long nix effects | `ReplyOnce` | **request/reply** | working + owner | drops its entire hand-written `daemon.rs`; the emitter emits the `BoundedWorkers` offload + two-typed-tier funnel it hand-wrote |
| **cloud** | per-request engine over `Arc<SchemaStore>` | `ReplyOnce` | **request/reply** | working + owner | gains the `BoundedWorkers` offload it lacks; drops hand-written `handle_meta_stream` for the typed meta tier |
| **message** | stamp-and-forward, blocking downstream call, no store | `ReplyOnce` | **request/reply** | working only | gains real concurrency (its blocking forward no longer serializes ingress); keeps its `Mutex<MessageEngine>` ONLY if it wants — see below |
| **spirit** | request/reply + cross-request subscription fan-out | `ReplyThenSubscribe` | **streaming** | working + owner | drops the `handle_meta_stream` escape hatch for a typed `Configure` meta tier; keeps the emitted registry/publish, now the archetype default |
| **repository-ledger** | request/reply over `Arc<Mutex<Store>>` + periodic spool ingest | `ReplyOnce` | **request/reply** | working + owner | joins the emitter for the first time; its spool-ingest periodic loop becomes a declared **maintenance task** the request/reply archetype hosts (see below) |

Four request/reply, one streaming. The streaming archetype is a **strict superset**
of request/reply: it IS request/reply plus the writer registry. That superset
relationship is the heart of why two archetypes is beautiful rather than a fork
(see "Why two beats one and beats all-actor").

### message's `Mutex` is its choice, not the archetype's

Under the request/reply archetype the engine is built fresh per request over an
`Arc<Shared>`. message has no durable shared state, so its `Shared` is just the
router-client config and `build_request_engine` mints a fresh `MessageEngine` per
request — no `Mutex` needed, no contention. message's current `Mutex<MessageEngine>`
exists ONLY because today's emitted spine hands the engine as `&self`; the
request/reply archetype's per-request-engine factory removes that constraint
entirely. message LOSES the `Mutex` and GAINS true concurrency: N in-flight
blocking forwards no longer queue behind one lock. This is the zero-compat mandate
paying off — message is "offended" (its `Mutex` and its `&mut self` engine model
both go), and it is strictly better for it.

### repository-ledger's spool loop — the periodic-maintenance seam

repository-ledger is the one consumer with a genuine non-request side-task: a
2-second spool-ingest loop. This is NOT a third archetype — it is a **maintenance
task** any archetype can declare. The request/reply archetype gains an optional
schema-declared `maintenance` property naming a periodic interval; the emitter
spawns ONE maintenance thread that calls a `ComponentDaemon::run_maintenance(&shared)`
hook on that interval, sharing the same `Arc<Shared>` the request workers clone.
repository-ledger's `Arc<Mutex<Store>>` becomes the archetype's `Arc<Shared>`; its
hand-rolled two-listener `thread::spawn` loop and its spool loop both dissolve into
the emitted request/reply spine plus one declared maintenance task. (Maintenance is
orthogonal to the request-disposition axis, exactly like tiers and effect
duration — it does not need its own archetype.)

## The four always-on properties (both archetypes carry them)

Per the mandate, these are NOT opt-in. They are properties of EVERY generated
daemon, request/reply or streaming, because every daemon genuinely needs them:

1. **Concurrency** — every accepted connection offloads onto a `BoundedWorkers`
   the runtime owns; `handle_stream` dispatches and returns immediately, so the
   accept loop never blocks on a slow request (lojix's nix build, message's
   blocking forward, spirit's redb read). The runtime owns `Arc<Shared>` +
   `BoundedWorkers`, never a long-lived engine. (`33/2` proves `BoundedWorkers`
   already lives in triad-runtime, generic, and the offload belongs in the emitted
   runtime, not the shell — the shell stays `&mut self`/serial-call.)

2. **Per-request engine over `Arc<Shared>`** — the worker builds a fresh engine
   per request from the cloned `Arc`. The `ComponentDaemon` hook becomes
   `type Shared: Clone + Send + Sync + 'static` + `fn build_request_engine(shared:
   &Self::Shared, connection: &ConnectionContext) -> Self::Engine`. This is the one
   shape all five share (spirit's long-lived redb `Engine` becomes an `Arc<Engine>`
   the worker clones a handle from; redb is already `Send + Sync`).

3. **Transport bounds (R1 + R2)** — bounded `MaximumFrameLength` (8 MiB default,
   schema-overridable) instead of the 4 GiB `default()`, and `set_read_timeout`
   (10 s default) before every read. Baked into the emitted transport for BOTH
   tiers and BOTH archetypes. No daemon should pre-allocate 4 GiB for a hostile
   prefix or wedge on a connect-and-never-send.

4. **Peer-cred auth, always read, fail-closed on the owner tier** —
   `ConnectionContext::from_stream` is read on EVERY accepted connection (working
   and owner) and threaded to `build_request_engine` so any component MAY classify
   by it. On the owner/meta tier it is fail-closed: the emitted owner spine
   compares `user_id()` against `DaemonConfiguration::owner_user_id()` and REJECTS
   on mismatch BEFORE decode (Spirit `9v7h`). This replaces both cloud's and
   lojix's hand-written `validate_owner_socket_mode` socket-mode-only guard with a
   kernel-vouched peer-cred check, layered on top of socket mode.

## Meta/owner tier — ONE typed model, no escape hatch

The mandate forbids preserving the escape hatch. Under proposal C the meta tier is
the SAME typed decode→execute→encode as the working tier, in BOTH archetypes. The
component declares a second contract module (`meta_contract_module`); the emitter
emits a meta spine that decodes the meta `Input`, wraps it into the shared
`nexus::SignalInput::MetaInput`, drives the SAME per-request engine `execute`, and
re-splits the `SignalOutput` by tier — exactly lojix's hand-written `serve_owner` /
cloud's `handle_meta_stream`, now emitted. `ComponentDaemon::handle_meta_stream`
(the raw-`UnixStream` escape hatch) is **deleted from the trait.** spirit's
`Configure` becomes `MetaInput::Configure` in a typed `meta-signal-spirit`
contract; cloud's and lojix's owner contracts already have this shape. No daemon
hand-writes meta framing again.

The owner tier differs from the working tier in exactly TWO emitted ways, both
generic: the fail-closed uid check (property 4), and the socket mode default
(`0o600`). Everything else is the working spine reused.

## The hand-written hook surface — mostly the real algorithm

This is the ESSENCE clarity test. After proposal C, the entire `ComponentDaemon`
impl a component hand-writes is:

```rust
impl ComponentDaemon for LojixDaemon {
    type Configuration = DaemonConfiguration;
    type ConfigurationError = Error;
    type Shared = Arc<Store>;          // the durable thing, cloned per request
    type Engine = SchemaRuntime;       // the per-request brain
    type Error = Error;

    const PROCESS_NAME: &'static str = "lojix-daemon";

    fn load_configuration(path: &Path) -> Result<Self::Configuration, Self::ConfigurationError> { … }
    fn build_shared(configuration: &Self::Configuration) -> Result<Self::Shared, Self::Error> { … }
    fn build_request_engine(shared: &Self::Shared, _connection: &ConnectionContext) -> Self::Engine {
        SchemaRuntime::with_store(shared.clone())   // THE algorithm: open a request view
    }
    // working + meta both flow through ONE typed funnel the engine already owns:
    fn decide(engine: &mut Self::Engine, input: nexus::SignalInput) -> nexus::SignalOutput {
        engine.execute(NexusWork::signal_arrived(input)).into_root_reply()   // THE algorithm
    }
}
```

Every line is a typed decision or a typed handoff. The decode, the tier split, the
`BoundedWorkers` offload, the read timeout, the frame cap, the peer-cred read, the
owner fail-closed reject, the `nexus::SignalInput` wrap/unwrap, the
subscription-writer registry (streaming only) — all EMITTED. The hand-written code
names the Shared, names the Engine, and writes the one-line algorithm:
`SignalInput → SignalOutput` through the engine. That is the readability thesis
satisfied: types name the work, the schema names the interface, the generated Rust
names the objects/traits, the hand-written code is the real algorithm.

The streaming archetype adds exactly the four subscription hooks that ARE
component algorithm and cannot be emitted (they are domain decisions):
`subscription_filter(input) -> Option<Filter>`, `subscription_token(output) ->
Option<Token>`, `published_event(engine, output) -> Option<Event>`,
`event_matches_filter(filter, event) -> bool`. These are pure typed predicates over
the component's domain — exactly the "real algorithm" the hand-written layer should
hold. The registry, the writer map, the fan-out, the parked-socket lifecycle: all
emitted.

## Why two beats one (proposal A) and beats all-actor (proposal B), per ESSENCE

ESSENCE priority: **Clarity > Correctness > Introspection > Beauty.**

### Versus proposal A (one unified request/reply archetype, streaming bolted on)

Proposal A must put the subscription registry, the parked-writer map, the fan-out
machinery, and the four subscription hooks into the ONE archetype — which means
EVERY daemon (message, cloud, lojix, repository-ledger) carries dead streaming
scaffolding it never uses, OR the unified archetype grows internal `if emits_stream`
branches. The first is a **Correctness** smell: a `ReplyOnce` daemon should be
type-incapable of registering a subscriber; under proposal A it carries the
registry as dead weight and the four hooks as `unimplemented!`/default stubs.
The second is a **Clarity** loss: the one archetype reads as a request/reply daemon
with streaming `if`s threaded through it — the structure no longer IS its own
documentation, because half the structure is conditionally inert. Proposal C makes
the streaming machinery EXIST only in the streaming archetype: a `ReplyOnce`
daemon's generated code has no registry, no writer map, no subscription hooks in
its trait at all. The special case (streaming) does not pollute the normal case
(request/reply); it is a NAMED separate shape. That is the Beauty criterion
("special cases collapse into the normal case") read correctly: you do not collapse
streaming INTO request/reply by making request/reply carry it always-on; you keep
request/reply pure and name streaming as its own thing that is a clean superset.

The cost of proposal A's "one shape" is paid by the four request/reply components
forever carrying streaming they will never use. Proposal C's two shapes cost ONE
extra archetype in the emitter and ZERO dead weight in any daemon.

### Versus proposal B (the generated daemon IS a kameo actor system)

Proposal B honors the actor-density pin literally: every generated daemon is a
kameo actor, requests are messages, the engine is actor state. This fails the
ESSENCE order at the top:

- **Clarity.** The readability thesis says the hand-written code should be "match
  typed input, make the decision, call the next typed interface, return typed
  output." An actor daemon makes the hand-written surface a kameo `Actor` impl with
  `Message<T>` handlers, mailbox lifecycle, `ActorRef` plumbing, `on_start`/
  `on_stop`, and async `.await` points threaded through the engine. That is MORE
  framework plumbing in the hand-written layer, not less — the opposite of the
  thesis. The genuine algorithm (`SignalInput → SignalOutput`) is the same one
  line; proposal B wraps it in actor ceremony four of the five components do not
  need (none of them has concurrent mutable shared state that an actor's serialized
  mailbox would protect — they all use a fresh per-request engine over an `Arc`,
  which is ALREADY the cleanest possible concurrency story: no shared mutable state
  at all).
- **Correctness.** Actors serialize access to mutable state via the mailbox. But
  four of five components have NO shared mutable state — they have an immutable
  `Arc<Store>` (redb does its own locking) and a fresh per-request engine. An actor
  mailbox would serialize requests that are already safely concurrent, REDUCING
  correctness-relevant parallelism (lojix's whole point is that a nix build must
  NOT serialize behind other requests — an actor mailbox would do exactly the
  serialization lojix fought to remove).
- **Beauty.** Proposal B introduces an async runtime (tokio) and a mailbox per
  daemon to model what is, for four of five, a stateless request/reply. The special
  case (genuine actor concurrency) would be imposed as the normal case. That is the
  Beauty criterion inverted.

### Confronting the actor-density pin head-on

The pin (`protocols/active-repositories.md:174-176`) says: *"Actor runtime: direct
kameo today. Actor density is required: runtime roots are actors, public actor
nouns carry data, topology/trace tests prove real mailbox paths."*

My position on the pin, stated explicitly for the StructuredOutput truth-pin field:
**The generated daemon layer is the named exception to actor-density, and the pin
should be read as scoped to components whose runtime genuinely has concurrent
mutable shared state — which the schema-derived request/reply daemons do not.** The
argument, made with force against ESSENCE-Clarity-first:

1. The pin's OWN justification is "topology/trace tests prove real mailbox paths."
   A real mailbox path exists to **serialize and route concurrent access to mutable
   actor state**. The schema-derived daemons have NO such state: their concurrency
   story is "fresh per-request engine over an immutable `Arc<Shared>`" — strictly
   simpler and strictly more parallel than a mailbox. Forcing a mailbox onto them
   adds a topology that proves nothing real (the mailbox would be a pass-through to
   a stateless handler). An actor with a pass-through mailbox is the ZST-namespace
   anti-pattern at the runtime level: a mailbox whose job vanishes if you erase it.
2. The pin describes "direct kameo TODAY" — a statement of the CURRENT actor
   substrate, not a mandate that every daemon be an actor. message, the one
   consumer the brief calls an actor, is **empirically not** a kameo actor in
   source (no kameo dep). So the pin and the code already disagree; the honest
   reading is that the pin governs components that ARE actors (the persona/message
   routing runtime roots that hold live mutable session state), not the
   schema-derived stateless request/reply daemons.
3. Where genuine actor nature exists — a runtime root holding concurrent mutable
   in-memory state (e.g. a future router that multiplexes live sessions) — proposal
   C does NOT forbid it. Such a component would declare a THIRD archetype if and
   when one genuinely appears. Proposal C's discipline is "an archetype per
   genuinely-distinct nature." If a true stateful-actor nature appears among the
   emitter's consumers, that is the trigger for an actor archetype — on merit, not
   on a pin that predates the analysis. Today, zero of the five have it.

This is the merit argument the brief asked for: I am arguing, against the literal
pin, that the generated request/reply and streaming daemons are the named
exception — because actor-density's own justification (real mailbox paths over
mutable state) does not apply to stateless-per-request daemons, and imposing it
would directly violate ESSENCE-Clarity (more framework in the hand-written layer)
and ESSENCE-Correctness (serializing already-safe parallelism). **If the psyche
intends the pin to bind even stateless daemons, that supersedes this argument and
proposal B is the answer — this is the one sharp question the synthesis must
surface.** I do not infer it; I argue my position and flag the fork.

## Daemon archetype count and the merit reason

**Two.** The count equals the number of genuinely-distinct request dispositions
the contract schema can express: `ReplyOnce` and `ReplyThenSubscribe`. Not one
(that forces streaming scaffolding onto stateless daemons or threads `if`s through
the one shape). Not five (that preserves each component's accident — the compat
reflex). Not three-for-the-actor (no consumer has genuine stateful-actor nature
today; that archetype is created WHEN one appears, not preemptively). Two is the
count of real natures, and the streaming archetype is a strict superset of the
request/reply archetype, so the two share one spine and differ by exactly the
writer-registry noun — maximal sharing, minimal forking.

## What each component loses (honest accounting)

- **lojix** loses its entire hand-written `daemon.rs` (the `LojixRuntime`,
  `RequestWorker`, `serve_ordinary`/`serve_owner`, the `BoundedWorkers` wiring, the
  socket-mode validation). All emitted. It keeps only the four-line
  `ComponentDaemon` impl. Net: ~280 lines → ~20.
- **cloud** loses its hand-written `CloudDaemon` meta escape hatch and gains the
  concurrency offload it lacked. Its `handle_meta_stream` (the only place it
  hand-writes framing) is deleted for the typed meta tier.
- **message** loses its `Mutex<MessageEngine>` and its `&mut self`-engine model
  entirely; gains per-request engine + real concurrency. message must restructure
  `MessageEngine` to be built fresh per request from an `Arc<RouterConfig>` Shared —
  a real change, and the right one. The "actor with its own concurrency" framing is
  abandoned as never-having-been-true.
- **spirit** loses its `handle_meta_stream` `Configure` escape hatch for a typed
  `meta-signal-spirit` contract; loses its long-lived-`&self`-engine model for the
  `Arc<Engine>`-cloned-per-request model (redb already supports concurrent handles).
  Keeps its four subscription hooks (now the streaming archetype's defining hooks)
  and the emitted registry/publish (now archetype-default, not opt-in).
- **repository-ledger** loses the MOST: its entire hand-rolled raw-`UnixListener` +
  `thread::spawn` + `Arc<Mutex<Store>>` daemon and its `frame_io` hand-codec. It
  joins the emitter, adopts the request/reply archetype with two tiers, and its
  spool loop becomes a declared maintenance task. It must define a `signal-*`
  contract schema if it lacks the daemon-shape inputs. Largest blast radius;
  entirely the point.

## The emitter changes this implies

1. Promote the schema-derived `emits_stream` bit to the named `RequestDisposition`
   archetype selector; the daemon emitter branches the runtime struct on it
   (registry present iff `ReplyThenSubscribe`).
2. Replace `ComponentDaemon`'s `Engine`-owned model with `Shared` + `Engine` +
   `build_shared` + `build_request_engine`; delete `handle_meta_stream`; add the
   typed meta spine driven by `meta_contract_module`.
3. Make `BoundedWorkers` offload, R1/R2 transport bounds, always-read peer-creds,
   and owner fail-closed reject UNCONDITIONAL in BOTH archetypes (no shape flags
   for these — they are properties of the one best daemon).
4. Add the orthogonal optional `maintenance` declaration (periodic task hook) to
   both archetypes for repository-ledger's spool ingest.
5. `DaemonConfiguration` gains `owner_user_id() -> Option<u32>` (the only
   triad-runtime addition; the fail-closed POLICY is emitted against it).

The shell (`MultiListenerDaemon`/`SingleListenerDaemon`, `BoundedWorkers`,
`ConnectionContext`, `LengthPrefixedCodec`) is UNCHANGED — `33/2` proves every
primitive the design needs is already generic in triad-runtime. The whole design
is emitter + the five components re-conforming.

## The one open fork (for the synthesis)

Whether the actor-density pin binds even stateless schema-derived daemons. My
position: it does not — they are the named exception, on merit (Clarity +
Correctness). If the psyche intends the pin to bind universally, proposal B wins
and the generated daemon becomes a kameo actor. This is the load-bearing
psyche question the synthesis must surface, not infer.
