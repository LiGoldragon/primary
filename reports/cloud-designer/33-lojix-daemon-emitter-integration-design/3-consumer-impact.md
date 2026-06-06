# 3 — Consumer impact: every emitter/runtime consumer the lojix-concurrency design must not break

cloud-designer, ground area CONSUMER IMPACT. 2026-06-06.

The design goal grows four properties into the GENERATED daemon so lojix can
drop its hand-written `daemon.rs`. Property 1 (offload each request onto
`BoundedWorkers`, fresh per-request engine over `Arc<Store>`) is the one that
endangers other consumers — it changes the lifecycle assumption the emitted
spine makes about `Engine`. This report inventories every consumer of the
emitter and of `MultiListenerDaemon`, classifies the concurrency model each
has and needs, and states what the design MUST preserve. The headline finding
drives the whole design: **concurrency must be a DECLARED emitter option, never
forced into `MultiListenerDaemon` or the default emitted spine.**

## The consumer inventory (five consumers, three distinct integration modes)

| Consumer | File | Uses emitter? | Daemon primitive | Tiers | Engine lifecycle today |
|---|---|---|---|---|---|
| **lojix** (target) | `lojix/triad-port/src/daemon.rs` | NO — hand-written | `MultiListenerDaemon` direct | multi (Ordinary+Owner) | fresh `SchemaRuntime` per request over `Arc<Store>`, offloaded onto `BoundedWorkers` |
| **cloud** | `cloud/src/schema_daemon.rs` | NO — hand-written `CloudRuntime` | `MultiListenerDaemon` direct | multi (Ordinary+Owner) | fresh `SchemaRuntime::with_store(Arc<SchemaStore>)` per request — SERIAL (no `BoundedWorkers`) |
| **spirit** | `spirit/src/daemon.rs` + `build.rs` | YES — `daemon_module` | emitted `MultiListenerDaemon` | multi (Working+Meta) | one long-lived `Engine` behind `&self`; meta tier is the `handle_meta_stream` escape hatch |
| **message** | `message/src/daemon.rs` + `build.rs` | YES — `daemon_module` | emitted `SingleListenerDaemon` | single (Working only) | `Mutex<MessageEngine>`; engine `handle` takes `&mut self`, locked per request |
| **repository-ledger** | `repository-ledger/src/daemon.rs` | NO — raw `UnixListener` loop | none (own `thread::spawn` per listener) | multi (Ordinary+Meta, hand-rolled) | `Arc<Mutex<Store>>` shared, lock held per request; serial within each listener thread |

Three distinct integration modes, and the design touches each differently:

1. **Emitter consumers** (spirit single-engine multi-tier, message
   single-engine single-tier) — the design's blast radius. These get the
   regenerated `daemon.rs`. They must NOT change behavior unless they
   opt in.
2. **`MultiListenerDaemon`-direct consumers** (cloud, lojix) — they hand-write
   their `MultiListenerRuntime` and never see the emitter. The design's value
   to them is that the emitter grows to MATCH what they hand-wrote, so they can
   adopt it later. They are unaffected until they choose to migrate.
3. **Raw-loop consumer** (repository-ledger) — depends on neither the emitter
   nor `triad-runtime`. Completely outside the blast radius; mentioned only to
   confirm it is not an accidental consumer.

## Per-consumer detail

### lojix — the reference implementation (target of the design)

Hand-written `MultiListenerRuntime` (`LojixRuntime`) over a two-socket
`MultiListenerDaemon`. `handle_stream` builds a fresh `RequestWorker` carrying a
clone of `Arc<Store>` and offloads it onto a shared `BoundedWorkers`
(`MAXIMUM_CONCURRENT_REQUESTS` permits). Each `RequestWorker::execute` builds a
fresh `SchemaRuntime::with_store(self.store.clone())` — so the in-flight deploy
cursor is never shared across requests. R1 (8 MiB max-frame) + R2 (10 s
`set_read_timeout`) bounds live on the per-request path. BOTH `signal-lojix` and
`meta-signal-lojix` decode into ONE `nexus::SignalInput{OrdinaryInput,MetaInput}`.

This is exactly properties 1+2+3+4. The design's job is to make the emitter able
to emit this shape. lojix is the one consumer that WANTS the new behavior to be
the path it adopts.

### cloud — the second per-request-engine daemon, but SERIAL today

`cloud/src/schema_daemon.rs` confirms the brief's core question. cloud is
**structurally lojix minus the concurrency**: it hand-writes `CloudRuntime` over
a direct two-socket `MultiListenerDaemon`, and `CloudRuntime::execute` already
builds a fresh `SchemaRuntime::with_store(self.store.clone())` per request over a
shared `Arc<SchemaStore>` (`schema_daemon.rs:144-145`). It already funnels both
contracts into one `nexus::SignalInput::{OrdinaryInput,MetaInput}`
(`schema_daemon.rs:125,136`) — property 2, hand-written. It already carries R1
(8 MiB) + R2 (10 s `set_read_timeout`) (`schema_daemon.rs:36-40,122,133`) —
property 3, hand-written.

What cloud does NOT have: `BoundedWorkers`. `CloudRuntime::handle_stream`
(`schema_daemon.rs:192-198`) runs `serve_ordinary`/`serve_owner` inline on the
accept loop. Because `MultiListenerDaemon::serve_streams` calls `handle_stream`
SERIALLY (`triad-runtime/daemon.rs:368-380`, the `try_serve_next_stream`
accept-then-handle loop), cloud is serial today.

**Does cloud want exactly lojix's concurrency model?** Almost. cloud's
per-request-engine-over-`Arc<Store>` shape (properties 2+3) is IDENTICAL to
lojix's; the ONLY gap is the `BoundedWorkers` offload. So a single emitter
option that delivers "fresh per-request engine over `Arc<Store>` +
`BoundedWorkers` offload + R1/R2 transport" produces the daemon cloud would
adopt almost verbatim — cloud is the second proof that this shape is reusable,
not lojix-private. The design should treat cloud as the SECOND adopter and
size the option to fit both: the per-request-engine + `Arc<Store>` + concurrency
+ R1/R2 + two-typed-contracts-one-Nexus-root bundle is exactly the cloud/lojix
shared shape.

(One genuine difference, not a blocker: cloud's `nexus::NexusWork::SignalArrived`
uses `OriginRoute(0)` hardcoded today, same as lojix's pre-hardening seam. Both
want property 4 to mint a real owner `OriginRoute`. Same seam, same fix.)

### message — the consumer the design MUST NOT break (engine needs `&mut self`)

This is the load-bearing constraint. The brief frames message as "the Kameo
actor daemon with its own concurrency"; the *current source* is not literally
Kameo, but the underlying constraint the brief points at is real and is the
reason concurrency must be opt-in:

- message uses the emitted `SingleListenerDaemon` path
  (`build.rs:49`, no `with_meta_tier`).
- `MessageEngine::handle` takes **`&mut self`** (`engine.rs:82-83`) — it builds a
  `MessageRequestEngine::new(self, connection)` that drives the Nexus runner with
  exclusive mutable access.
- Because the emitted `handle_working_input` hook hands the engine as `&Self::Engine`
  (shared), message sets `type Engine = Mutex<MessageEngine>` and locks per request
  (`daemon.rs:61,81-82`). The engine's own model is "one request per connection on
  its own call stack" (`engine.rs` `FORWARD_ORIGIN_ROUTE` doc) — a single mutable
  engine serialized by a `Mutex`, NOT a fresh-per-request engine over a shared store.

If property 1 were forced into the emitted spine (every emitted daemon offloads
onto `BoundedWorkers` and builds a fresh per-request engine), message breaks in
two ways:

1. **Lifecycle mismatch.** message has NO `Arc<Store>` to clone — it has one
   `Mutex<MessageEngine>` that is the durable thing. "Fresh per-request engine
   over a shared store" has no meaning for it; there is nothing to share. Forcing
   it would demand message restructure into a store + per-request engine split it
   does not have and does not want (message owns no durable state — it is
   stamp-and-forward, `engine.rs:1-3`).
2. **Concurrency it does not want.** message serves one request per connection by
   design and guards mutation with a `Mutex`. Thread-per-connection offload would
   just contend on that one `Mutex` — pure overhead, zero throughput gain, plus
   `Send + 'static` bounds on `MessageEngine` it is not required to satisfy today.

**What the design MUST preserve for message:** the DEFAULT emitted spine stays
exactly as it is — serial `handle_working_stream`, `engine: &Self::Engine` shared
hook, no `Send`/`'static` engine bound, no `Arc<Store>` assumption, `SingleListenerDaemon`
on the no-meta-tier path. message must regenerate `daemon.rs` byte-identically
(modulo unrelated churn) after this change lands. message is the proof that the
answer to the brief's framing question is:

> **'concurrency as a declared emitter option' is correct; 'concurrency forced
> into `MultiListenerDaemon`' is wrong.** message is a single-listener consumer
> that would be damaged by either forcing concurrency into the spine OR forcing it
> into `MultiListenerDaemon` (message would inherit nothing it wants and lose the
> simple `Mutex` model). The option must be declared per-component in the
> `NexusDaemonShape`, defaulting OFF.

### spirit — emitter consumer, multi-tier, single long-lived engine

spirit uses `daemon_module` with `with_meta_tier` (`build.rs:57-58`), so it gets
the emitted **multi-listener** spine. Its `type Engine = Engine` is one
long-lived engine behind `&self`; `handle_working_input` calls
`engine.handle(input).root().clone()` (`daemon.rs:118-124`). It uses the meta
tier as the `handle_meta_stream` escape hatch (`daemon.rs:130-137`) and the full
streaming hook set (filter/token/event). spirit has a durable redb `Store` opened
in `build_runtime`, but the engine wraps it — there is no `Arc<Store>` exposed for
per-request cloning.

**Impact:** spirit is on the multi-listener path that property 2 reshapes (owner
tier from escape hatch to typed Nexus path). The design MUST keep spirit's current
behavior available: if spirit does NOT opt into the concurrency option, the
emitted multi-listener spine keeps the serial `&self` engine and the
`handle_meta_stream` escape hatch. The property-2 "two typed contracts into one
Nexus root" reshape is ALSO an opt-in: spirit's meta tier is a different shape
(a request/reply `Configure` over a component-owned `MetaSignalTransport`, NOT a
second leg of one `nexus::SignalInput`), so forcing the typed-Nexus-root owner
path would break spirit's escape-hatch design. spirit must keep the escape hatch
unless it declares the typed-meta-root shape. Critically, spirit's engine is
single long-lived behind `&self` — the same "no `Arc<Store>` to clone, no `Send`
bound today" constraint as message — so property 1 must NOT touch the default
multi-listener path either.

### repository-ledger — not a consumer; outside the blast radius

`repository-ledger/Cargo.toml` depends on neither `triad-runtime` nor
`schema-rust-next`. Its `daemon.rs` is a fully hand-written daemon: it binds two
raw `UnixListener`s, `thread::spawn`s one listener thread each, and serves
`signal-frame` `ExchangeFrame`s over an `Arc<Mutex<Store>>` (one lock per
request). It has its own (non-`triad-runtime`) two-listener-thread concurrency
and a spool-ingest background loop. It does NOT use the emitted daemon, does NOT
use `MultiListenerDaemon`, and is unaffected by any change to either. Listed only
to close the question: it is not an accidental consumer. (Separate, pre-existing
migration target — out of scope here.)

## The design constraint this report establishes

The four properties cannot be unconditional emitter changes. The blast radius is
the two EMITTER consumers (spirit, message), and BOTH would be damaged by a
forced concurrency/lifecycle change:

- **message** (single-tier, `Mutex<engine>`, `&mut self` engine, no store to share)
- **spirit** (multi-tier, single long-lived `&self` engine, escape-hatch meta,
  full streaming)

Neither has an `Arc<Store>` to clone per request; neither wants thread-per-connection;
message's engine cannot even satisfy the `Send + 'static` bound `BoundedWorkers`
needs without new work. Therefore:

**Property 1 (concurrency + per-request engine over `Arc<Store>`) MUST be a NEW,
defaulted-OFF field on `NexusDaemonShape`** (e.g. a `ConcurrencyModel` /
`PerRequestEngine` declaration in `build.rs`), selecting an ALTERNATIVE emitted
spine. The existing `Engine: &self` + serial `handle_working_stream` path stays
the default. When a component declares the per-request-engine model, the emitter
emits: (a) a `build_runtime` that yields a shared store handle the spine clones
per request (the `ComponentDaemon` hook surface changes shape for THAT path
only — e.g. `type Store` + `fn build_request_engine(store) -> Engine`), and (b)
`handle_working_stream` offloads onto a `BoundedWorkers` the runtime owns.

**Property 2 (two typed contracts into one Nexus root)** is similarly opt-in,
gated on the meta tier being declared as a TYPED second contract module rather
than the current escape-hatch `MetaListenerTier`. spirit keeps the escape hatch;
lojix/cloud declare the typed-meta-root.

**Properties 3 (R1/R2 transport bounds) and 4 (fail-closed owner auth)** are the
lowest-risk. R1/R2 can be unconditional additions to the emitted `WorkingTransport`
(every consumer benefits from a bounded max-frame + read-timeout; today the emitted
`WorkingTransport` uses `LengthPrefixedCodec::default()` with NO timeout — a
strict improvement for spirit and message). The only caution: a max-frame default
must be generous enough not to truncate spirit's largest legitimate frame, so it
should be a `NexusDaemonShape` field with a safe default (e.g. 8 MiB) rather than
a hardcoded constant. Property 4 (fail-closed owner uid check) attaches to the
meta/owner tier and is only reachable on consumers that HAVE an owner tier
(spirit, lojix, cloud) — message has none, so it is untouched; the owner-uid
policy must be a declared `NexusDaemonShape` field (which uid(s) count as owner),
and on mismatch the spine REJECTS before decode (intent 9v7h, fail-closed).

## Verdict on the brief's framing question

**Concurrency as a declared emitter option — correct.** message is the
counterexample that rules out the alternatives:

- "Forced into `MultiListenerDaemon`" is wrong: message is `SingleListenerDaemon`
  and gains nothing; and forcing `BoundedWorkers` into `MultiListenerDaemon`'s
  `serve_streams` would change behavior for spirit (long-lived `&self` engine) and
  cloud (which deliberately controls its own offload absence) without their consent.
- "Forced into the default emitted spine" is wrong: message and spirit both have a
  single long-lived engine with no shareable store and no `Send` bound; the lifecycle
  flip breaks them.
- "Declared per-component, defaulting OFF" is right: lojix and cloud opt in (and get
  the shape they each already hand-wrote, cloud minus only the offload); spirit and
  message regenerate unchanged.

The concurrency primitive (`BoundedWorkers`) already lives in `triad-runtime` and
its own doc states the rule the design follows: *"Daemons with their own
concurrency model (e.g. an actor runtime) simply do not use it"*
(`workers.rs:13`). The emitter must honor the same opt-in: the per-request-engine
+ `BoundedWorkers` spine is emitted ONLY when the shape declares it.
