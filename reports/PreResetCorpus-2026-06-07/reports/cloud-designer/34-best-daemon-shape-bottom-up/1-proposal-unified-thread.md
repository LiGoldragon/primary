# Proposal A — the unified thread-per-request daemon

cloud-designer, session 34 (best daemon shape, bottom-up). Companion proposals in
this directory argue the actor and hybrid shapes; this file argues the ONE shape
should be sync thread-per-request for every component the emitter serves.

Pins read for facts: `schema-rust-next` daemon emitter (`daemon_emit.rs`),
`triad-runtime` (`daemon.rs`/`workers.rs`/`process.rs`/`frame.rs`), and all five
consumer daemons at their current checkouts. Ground truth on emitter internals,
runtime seams, and the four lojix properties is established in session 33 and is
NOT re-derived here.

**Mandate context (Spirit ax2k, Maximum).** ZERO backward compatibility. There is
no production to protect. I do NOT propose anything opt-in, I do NOT value
byte-stable regeneration, and I treat "this breaks spirit / message / cloud /
lojix / repository-ledger" as the EXPECTED outcome, not a cost. Session-33 report
3 framed every property as a defaulted-OFF `NexusDaemonShape` field to protect the
existing consumers; under ax2k that framing is RETIRED. The right shape is chosen
on merit and every consumer is rewritten to it.

## Philosophy: one synchronous spine, the engine is the only hand-written thing

A request daemon is a pure function lifted onto a socket: bytes arrive, decode to
a typed input, the engine decides, encode the typed output, bytes leave. Threads
exist only so a slow decision (a multi-minute `nix` build) does not stall the
next caller. Nothing about that needs cooperative scheduling, a mailbox, an
executor, or `async`. A blocking read on a kernel socket, handed to a worker
thread off a bounded pool, IS the natural runtime for unix-socket request/reply —
and it is the runtime a reader can hold entirely in their head.

So the single generated daemon is:

- **sync**, no `async` runtime anywhere in the stack;
- an **accept loop + `BoundedWorkers` thread-per-request** offload (the
  triad-runtime shell, unchanged);
- a **fresh per-request engine** built over a shared `Arc<Shared>` (the durable
  store / outbound client / whatever the component's persistent thing is);
- **both authority tiers decoded into one typed `nexus::SignalInput` root**, one
  engine `execute`, the reply re-split by tier;
- **always-bounded transport** (max-frame + read-timeout baked in, never the 4 GiB
  default);
- **always-on `ConnectionContext`** on every accepted stream, with the owner tier
  **fail-closed** on uid mismatch (Spirit 9v7h) before the engine is ever reached.

The hand-written surface collapses to ONE method per component: `decide` — match a
typed `SignalInput`, run the component's algorithm, return a typed `SignalOutput`.
Everything else (decode, framing, peer-cred read, tier split, owner gate, worker
offload, encode, exit code) is emitted or lives in the shared runtime. That is the
CLARITY thesis from the ESSENCE made literal: the hand-written code is MOSTLY THE
REAL ALGORITHM.

## The single emitted hook trait

Today's `ComponentDaemon` (`daemon_emit.rs:419-456`) carries eight-plus methods
and an escape-hatch `handle_meta_stream(engine, raw_stream)` that hands the
component a naked `UnixStream`. That escape hatch is the defect: it is the one
place the contract is NOT typed, NOT peer-cred-gated, and NOT funneled through the
engine. Proposal A deletes it. The whole hook becomes:

```rust
/// The only daemon code a component hand-writes. Everything else — argv parsing,
/// peer-cred read, the owner gate, the two-tier decode/split, worker offload,
/// framing, exit code — is emitted or lives in triad-runtime.
pub trait ComponentDaemon: Sized + 'static {
    /// The durable, shared, cheaply-clonable thing the daemon owns across
    /// requests: a store handle, an outbound client, a connection pool. For a
    /// stateless ingress it is `()` or the outbound client; for a store-backed
    /// daemon it is `Arc<Store>`. MUST be `Clone + Send + Sync + 'static` so each
    /// worker thread gets its own handle.
    type Shared: Clone + Send + Sync + 'static;

    /// The per-request decision object built fresh per worker over `&Shared`.
    /// Holds request-local cursor state; never shared across requests. MUST be
    /// `Send` so it lives on the worker thread.
    type Engine: Send;

    type Configuration: DaemonConfiguration;
    type ConfigurationError: std::error::Error;
    type Error: DaemonComponentError;          // see "the error bound" below

    const PROCESS_NAME: &'static str;

    /// Open the durable shared state once, at bind time.
    fn open_shared(configuration: &Self::Configuration)
        -> Result<Self::Shared, Self::Error>;

    /// Build a fresh per-request engine over a clone of the shared handle. Called
    /// inside each worker thread; the returned engine owns its request-local view.
    fn build_engine(shared: &Self::Shared) -> Self::Engine;

    /// THE algorithm. Both authority tiers arrive here already decoded into the
    /// one Nexus root; the owner tier has ALREADY passed the fail-closed uid gate,
    /// so `origin` is a trusted, kernel-vouched route. Return the typed output;
    /// the emitted spine re-splits it onto the arriving tier and encodes it.
    fn decide(
        engine: &mut Self::Engine,
        signal: nexus::SignalInput,
        origin: RequestOrigin,
    ) -> Result<nexus::SignalOutput, Self::Error>;

    fn load_configuration(path: &Path)
        -> Result<Self::Configuration, Self::ConfigurationError>;
}
```

Five required items (`Shared`, `Engine`, `decide`, `open_shared`,
`build_engine`) plus the config glue. No `start`/`stop` (lifecycle is
`open_shared` returning the owned handle; teardown is `Drop`). No
`handle_meta_stream`. No `handle_working_input` split from a meta hook — there is
ONE decision method taking the ONE Nexus root. `RequestOrigin` is an emitted
schema noun carrying the tier tag plus the peer-cred uid/gid/pid, so the component
can mint provenance (message's genuine need) without re-reading the socket.

`decide` IS the readability claim. lojix's `decide` matches
`SignalInput::{Ordinary,Meta}`, runs the deploy or query, returns
`SignalOutput::{Ordinary,Meta}`. cloud's is the same minus the build effect.
message's matches `Submit/QueryInbox/SubmitStamped`, stamps with `origin`,
forwards, returns. The plumbing those three hand-wrote — `serve_ordinary`,
`serve_owner`, `RequestWorker`, `ordinary_reply`/`meta_reply`,
`invariant_rejection`, `validate_owner_socket_mode`, the codec construction, the
`set_read_timeout` calls — ALL move into emission. That is the right placement:
session-33 report 1 found every one of those is mechanical and identical across
lojix and cloud.

### Streaming as ONE more typed decision, not a second hook family

spirit's five streaming hooks (`subscription_filter`, `subscription_token`,
`published_event`, `event_matches_filter`, `subscription_event_short_header`) are
the streaming-only associated-type block in today's trait. Proposal A keeps the
emitted subscription registry + publish path exactly where session-33 placed it
(in the generated runtime, generic over a `SubscriptionToken`), but the
component-facing surface is NOT five extra trait methods. It is a single emitted
trait the component implements ONLY when the schema declares a stream:

```rust
// Emitted only when !schema.streams().is_empty(); a separate trait so the
// non-streaming daemons (lojix, cloud, message, repository-ledger) never see it.
pub trait ComponentSubscriptions: ComponentDaemon {
    type Filter: Clone + Send;
    type Event: StreamEvent;                      // rkyv bounds emitted, as today
    fn opens(input: &nexus::SignalInput) -> Option<Self::Filter>;
    fn event_of(engine: &Self::Engine, output: &nexus::SignalOutput)
        -> Result<Option<Self::Event>, Self::Error>;
    fn matches(filter: &Self::Filter, event: &Self::Event) -> bool;
}
```

The subscription TOKEN extraction and the event short-header are derived by the
emitter from the schema's stream declaration, not hand-supplied — the schema
already names the subscription-event root, so the header constant and the
token-from-output projection are emit-time facts. This drops spirit's hand-written
surface from five methods to three, and keeps the non-streaming components on the
bare `ComponentDaemon`. The streaming worker is the SAME thread-per-request worker:
it offloads, decides, and — when `event_of` yields an event — publishes to the
registry's writer set under the registry's own lock. No async, no actor; a
subscription writer is a `UnixStream` the registry holds and writes to on publish.

### The error bound

Today the `Error` bound is an ad-hoc `Display + From<FrameError> +
From<SignalFrameError> + From<ListenerError>`. Replace it with one emitted sealed
trait `DaemonComponentError` carrying those `From` bounds plus `Send` (workers are
`'static`). This is the typed-per-crate-Error discipline: the component declares
ONE error enum, the emitter requires exactly the conversions the spine performs,
and `Send` is stated once rather than rediscovered per consumer.

## How the daemon shape is declared (no opt-in flags)

`NexusDaemonShape` keeps `process_name` + `working_tier`, and the meta tier
becomes a TYPED second contract, never an escape hatch:

```
NexusDaemonShape       [process_name working_tier meta_tier? frame_bounds]
WorkingListenerTier    [contract_module]
MetaListenerTier       [contract_module socket_mode owner_authority]
FrameBounds            [max_body_bytes read_timeout_millis]
OwnerAuthority         [Required | SocketModeOnly]
```

Positional, typed, constructed in the component's `build.rs` (the established
home, session-33 report 1). There is NO `concurrent?` flag and NO
`per_request_engine?` flag — because under proposal A there is no alternative
spine to select. Every emitted daemon is thread-per-request. The concurrency
"option" session-33 invented existed only to spare message and spirit; ax2k
removes the reason for it. `frame_bounds` is always present with a real bound (8
MiB / 10 s default in the shape constructor); the 4 GiB codec default is never
emitted. `owner_authority` defaults to `Required` — fail-closed is the floor, and
a component must affirmatively declare `SocketModeOnly` to weaken it (and none
should).

## The five consumers, rewritten

### lojix — the reference; becomes pure `decide`

lojix today IS this shape hand-written (session-33 report 3). Under proposal A its
entire `daemon.rs` (276 lines) deletes. `Shared = Arc<Store>`, `Engine =
SchemaRuntime`, `open_shared` builds the store, `build_engine` is
`SchemaRuntime::with_store(shared.clone())`, `decide` is the 15-line match that
wraps each tier into `SignalInput`, runs `engine.execute(...).into_root()`, and
returns `SignalOutput`. The owner gate, the 8 MiB / 10 s bounds, the two-tier
split, the `invariant_rejection` fallback — all emitted. lojix loses its
hand-written `validate_owner_socket_mode` because the emitted owner gate is
strictly stronger (peer-cred fail-closed, not mode-only). **This is a pure win and
the proof the shape is real.**

### cloud — gains concurrency for free; meta stops being an escape hatch

cloud today is lojix-minus-`BoundedWorkers` plus a hand-written
`handle_meta_stream` (`schema_daemon.rs:93-107`) that re-implements the read /
decode / handle / write the emitter already does for the working tier. Under
proposal A that escape hatch is DELETED: the meta tier is a typed
`SignalInput::MetaInput` arriving at the same `decide`, and cloud picks up the
worker-pool offload it lacked. cloud's `decide` is `match SchemaRuntime::reply_to_signal(...)`,
identical for both tiers. cloud's `MAXIMUM_REQUEST_FRAME_BYTES` /
`REQUEST_READ_TIMEOUT` constants delete (they become `FrameBounds`). cloud is the
SECOND proof the shape is not lojix-private.

### message — the actor framing is a target, not its genuine need; it fits cleanly

This is the load-bearing argument, so I take it head-on. The brief says "message
IS a kameo actor daemon." The SOURCE says otherwise: message's daemon is
`Mutex<MessageEngine>` behind the emitted single-listener spine
(`daemon.rs:55-84`), and its actual work per request (`engine.rs:82-97`,
`router.rs:330-343`) is:

1. read the typed `Input` off the socket;
2. classify the connection by `SO_PEERCRED` uid into a `MessageOrigin`
   (`router.rs:273-284` — owner uid → internal harness instance, else non-owner);
3. stamp the submission with that origin + an ingress timestamp;
4. **synchronously `UnixStream::connect` to the router and block on its reply**
   (`router.rs:58-65`);
5. translate the reply to a typed `Output` and return it.

That is request → peer-cred → stamp → blocking outbound call → reply. It is a
TEXTBOOK thread-per-request handler. The `Mutex<MessageEngine>` exists ONLY because
today's emitted hook hands the engine as `&Self::Engine` (shared) and message's
`handle` wants `&mut self`; under proposal A `build_engine` yields a FRESH
`MessageEngine` per worker, so the `Mutex` and the whole `MessageRequestEngine`
borrow dance (`engine.rs:59-62,169-199`) DELETE. message's `Shared` is its
`RouterForwarder` (the outbound client + owner identity, already `Clone`,
`router.rs:299-303`); `decide` is the `decide_signal` match it already wrote
(`engine.rs:127-142`), now taking the trusted `origin` directly instead of
re-deriving it. The stamp-and-forward is a synchronous effect on the worker
thread, which is exactly where a blocking `UnixStream::connect` belongs.

**Does the router's stamp-and-forward genuinely fit thread-per-request? Yes,
better than it fits an actor.** An actor would force the synchronous outbound
router call to either block the actor's mailbox (serializing all forwards behind
one in-flight call — strictly worse than today) or spawn a detached task (an
executor message has no reason to carry). Thread-per-request gives each forward its
own stack and its own blocking outbound socket, with `BoundedWorkers` capping the
fan-out. The actor framing buys message nothing its genuine need wants.

### spirit — multi-tier + streaming, both onto the one spine

spirit's `Configure` meta escape hatch (`daemon.rs:130-137`,
`meta_transport.rs`) is the same defect as cloud's: a hand-written
read/decode/handle/write that the emitted two-tier spine already does. DELETE it;
`Configure` becomes `SignalInput::MetaInput(Configure)` arriving at `decide`.
spirit's `MetaSignalTransport` (104 lines) deletes — the meta wire is just the
second leg of the one Nexus root. spirit's streaming surface moves to the
three-method `ComponentSubscriptions`. spirit's `Shared = Arc<Store>` (the redb
handle), `Engine` a per-request view, `decide` the `engine.handle(input)` match.
spirit loses its `Mutex`-free single long-lived `&self` engine — and that is FINE
under ax2k: a fresh per-request engine over the shared redb is the correct shape
(redb is the durable, briefly-locked point), and it removes the "no `Arc<Store>`
to clone" special case session-33 had to carve out.

### repository-ledger — adopts the emitter; its hand-rolled threads delete

repository-ledger today is two `thread::spawn`ed listener loops over
`Arc<Mutex<Store>>` (`daemon.rs:42-49,124-148`) plus a 2-second spool-ingest poll
loop. It uses neither the emitter nor triad-runtime. Under proposal A it becomes a
`ComponentDaemon`: `Shared = Arc<Store>` (the lock moves inside the store's own
methods, as it already half-is), the two raw listeners become the emitted
two-tier `MultiListenerDaemon`, `serve_ordinary_stream`/`serve_meta_stream`
collapse into one `decide` over `SignalInput`. **Does the ledger's hook genuinely
fit?** Its request handling does — it is already lock-per-request over a shared
store, the degenerate hand-rolled form of exactly this spine. The ONE thing that
does NOT fit the request/reply mold is the **2-second spool-ingest background
loop** (`daemon.rs:51-56`): that is a timer-driven task with no socket, no
request, no reply. Proposal A's honest answer: the daemon owns ONE background
worker the emitter spawns from a schema-declared `BackgroundTick` (interval +
the typed work it runs), distinct from the request workers. This is a real
addition to the shape — see "what this forces" below — but it is a SMALL, named
addition, and the ledger's per-request handling is otherwise a clean fit.

## The pivotal fork: retire kameo from the generated daemon layer

I take the hard position: **the schema-derived daemon layer is sync
thread-per-request, and kameo does NOT belong in it.** The reasoning, against the
actor-density pin, stated with force:

1. **Not one of the five consumers has a genuine actor need at the DAEMON
   boundary.** lojix, cloud, spirit, repository-ledger are store-backed
   request/reply. message — the supposed actor — is peer-cred-stamp + blocking
   outbound forward, which an actor mailbox would make WORSE (serialize forwards or
   spawn detached). The actor density the truth-pin wants ("runtime roots are
   actors, public actor nouns carry data, topology/trace tests prove real mailbox
   paths") describes an INTERNAL fan-out topology — the `internal` schema category
   in INTENT.md (the "actor mailbox" channel, line 377), the spirit
   actor-schema plane (INTENT.md 451). That is a property of what the engine does
   INSIDE a request, NOT of how the daemon accepts sockets. The generated DAEMON
   is the socket-to-typed-input lift; the actor topology, where a component has
   one, lives BELOW `decide`, in the engine the component still owns. Proposal A
   does not forbid an engine from being an internal kameo actor system — it forbids
   the SOCKET ACCEPT layer from being one.

2. **The accept layer being sync is upstream of CLARITY, the top ESSENCE
   criterion.** An async/actor accept layer drags an executor, `async fn` coloring,
   pinning, and mailbox lifecycle into the ONE piece of code every component shares
   and every reader must understand. A blocking accept + bounded thread pool is a
   page of code with no hidden scheduler. When CLARITY and the actor-density pin
   conflict here, ESSENCE says CLARITY wins — and the brief explicitly invites the
   argument that the generated daemon layer is the exception. **It is the
   exception**: the pin governs runtime-internal topology, the generated daemon is
   the transport edge, and the edge is clearest sync.

3. **The honest scope of the concession.** I am NOT arguing kameo is wrong for
   message's broader runtime, nor that the actor-density intent is wrong. I am
   arguing the SINGLE BEST GENERATED daemon — the thing the emitter stamps for five
   components — is sync thread-per-request, and any actor topology a component
   wants is BELOW the `decide` boundary in its own engine, reached the same way for
   every component. If message's router fan-out later wants real mailboxes, that
   lives in message's engine and is proven by message's own topology/trace tests;
   it does not pull an executor into the generated accept loop that lojix and the
   ledger also run.

## What this design forces every component to give up (honest accounting)

- **spirit loses its single long-lived `&self` engine and its `Configure`
  escape-hatch + `MetaSignalTransport`.** Its meta tier becomes a typed Nexus leg;
  its engine becomes per-request over the shared redb. If any spirit operation
  genuinely needs cross-request engine state that is NOT in the durable store, it
  must move that state into `Shared` — a real constraint, and the one place spirit
  could resist.
- **message loses the `Mutex<MessageEngine>` and the actor framing.** If message's
  future genuinely wants internal actor fan-out (one inbound request → many router
  sends with independent mailboxes), that topology must live in message's engine
  below `decide`, not in the daemon. Proposal A asserts message does not need it at
  the daemon boundary today; a future that proves otherwise is the honest risk to
  this proposal.
- **repository-ledger must express its spool-ingest loop as a declared
  `BackgroundTick`** rather than a free `thread::spawn` + `sleep`. Any component
  with a non-request background job pays this: background work becomes a typed,
  schema-declared shape, not an ad-hoc thread. This is the single place
  thread-per-request does NOT cover the ledger's genuine need, and proposal A
  answers it with a named addition rather than pretending request/reply covers it.
- **cloud and lojix lose nothing** — they gain emission of what they hand-wrote.
- **Every component's engine must be `Send`** and built fresh per request. A
  component whose engine holds a `!Send` resource (a raw FFI handle, a
  thread-affine connection) must restructure. None of the five do today.
- **Streaming components accept a registry that lives in the shared runtime, not in
  their code.** spirit gives up owning its subscription hub (it already did, per
  `subscription.rs`); any component wanting bespoke subscriber lifecycle loses that
  freedom.

## Why this is the most beautiful per the ESSENCE order

CLARITY: one spine, one `decide`, zero escape hatches. The structure documents
itself — a reader sees accept → worker → decode → gate → decide → encode and knows
the whole daemon. CORRECTNESS: every boundary is typed — the one `SignalInput`
root names both tiers, `RequestOrigin` names the trusted peer identity, the
`SignalOutput` re-split names the reply tier; the untyped raw-`UnixStream` hatch is
gone. INTROSPECTION: every request is a thread with a name and a worker-pool permit
count; the bounded pool's permit gauge IS the live-load readout, observable without
an executor's opaque task graph. BEAUTY: the meta escape hatch, the streaming hook
family, the per-consumer concurrency special-cases, and the `Mutex<Engine>`
workaround ALL collapse into the normal case — one engine, one decision, one
worker. Four special shapes become one named pattern. That is the test for done.

## Open questions

- `BackgroundTick` is a genuine new shape leg the brief did not name; proposal B/C
  should weigh whether a timer-driven background worker belongs in the generated
  daemon at all or stays hand-written below it.
- Worker drain on shutdown: `BoundedWorkers` has no join surface (session-33 report
  2, open seam 2). Fresh-per-request engines make abrupt worker termination
  survivable for stores with their own durability (redb, the ledger), but a
  half-written outbound forward (message) on SIGTERM is a real edge — does the
  shape need a drain, or is best-effort acceptable?
- `RequestOrigin` as a schema noun vs a triad-runtime type: it carries the tier tag
  + peer creds; is the tier an emit-time enum (one per component's tier set) or a
  generic `Working | Owner`? The owner-gate emission depends on the answer.
