# 4 — design draft: the integrated lojix-shape daemon emitter

cloud-designer, 2026-06-06. Pins: `schema-rust-next` `6685e7b`, `triad-runtime`
`f9c38e2`, `lojix/triad-port` `c8c4353`. Builds on surveys 1 (emitter internals),
2 (runtime seams), 3 (consumer impact), and prior `32-…/7-overview`.

Psyche chose this integration (Spirit `tj99`); owner auth must FAIL CLOSED on uid
mismatch (Spirit `9v7h`). This file is the concrete, buildable draft: the exact
build.rs declaration a component author writes, the exact token-based emitter
change, the one triad-runtime seam, what lojix `daemon.rs` collapses to, and the
staged plan. All four properties plus fail-closed owner auth are addressed.

## The shape of the answer in one paragraph

Add ONE opt-in declaration to `NexusDaemonShape` — a `ConcurrentNexusTier` that
bundles all four properties as a coherent shape (concurrency model + the second
typed meta contract + frame bounds + owner authority), because surveys 2 and 3
proved they are not four independent flags but ONE shared cloud/lojix shape: a
per-request engine over `Arc<Store>` offloaded onto `BoundedWorkers`, two typed
contracts funneled into one `nexus::SignalInput` root, hardened transport, and a
fail-closed owner-uid edge check. When that field is present, the emitter selects
an ALTERNATIVE `GeneratedDaemonRuntime` spine (the lojix `LojixRuntime` +
`RequestWorker` shape, lifted into tokens) and an ALTERNATIVE `ComponentDaemon`
hook surface (`type Store` + `build_shared_store` + `build_request_engine`). When
it is absent, every emitted byte is identical to today — so `spirit` and
`message` regenerate byte-stable. The only triad-runtime change is one defaulted
`DaemonConfiguration::owner_user_id()` accessor; everything else the four
properties need already exists at triad-runtime HEAD.

## Why one bundled field, not four flags

Survey 3's consumer matrix is decisive. The two adopters of the new shape are
lojix and cloud, and cloud is "lojix minus only the `BoundedWorkers` offload" —
both want per-request-engine-over-`Arc<Store>` + two-typed-contracts-one-Nexus-
root + R1/R2 simultaneously. The two consumers that must NOT change (spirit,
message) want NONE of them. There is no consumer that wants property 2 without
property 1, or property 1 without a shared store. So the properties cluster: the
concurrent per-request-engine model REQUIRES the `type Store` hook (you cannot
build a fresh engine per worker without a shareable store), and the two-typed-
contract meta path REQUIRES the per-request execute spine that funnels both
contracts. Bundling them into one `ConcurrentNexusTier` matches the real adoption
unit and avoids illegal combinations (e.g. "concurrent but single long-lived
engine", which has no consumer and breaks the `Send + 'static` worker bound).

Property 3 (R1/R2 bounds) is the one genuinely separable piece: survey 3 notes it
is a strict improvement for everyone. But because the hostile-prefix pre-alloc and
the read-timeout both want a configurable bound, the cleanest move is to make the
bound a field that BOTH the default serial transport and the concurrent spine read
— defaulting to today's behavior on the serial path (see "Property 3" below for
the compat nuance).

## The build.rs declaration the component author writes

Today lojix never touches the emitter; under this design lojix's `build.rs`
declares the shape and the emitter produces what lojix hand-wrote. The author
writes a positional, typed declaration following the existing `new` + `with_*`
builder precedent (`daemon_emit.rs:49-61`). New types, all positional records:

```rust
// In lojix/triad-port/build.rs (the component author's hand-written declaration):
let shape = NexusDaemonShape::new(
        "lojix",                                  // process_name
        WorkingListenerTier::new("signal_lojix"), // the ordinary contract module
    )
    .with_concurrent_nexus_tier(ConcurrentNexusTier::new(
        // (1) the second typed contract module — the meta/owner leg:
        MetaContractTier::new(
            "meta_signal_lojix",                  // meta contract_module
            SocketModeBits::new(0o600),           // owner-only socket mode (kept)
            OwnerAuthority::peer_credential(),    // (4) fail-closed peer-cred edge check
        ),
        // (1) the shared-store concurrency model:
        SharedStoreConcurrency::new(64),          // BoundedWorkers capacity
        // (3) transport hardening bounds:
        FrameBounds::new(8 * 1024 * 1024, Duration::from_secs(10)), // R1 max body, R2 read timeout
    ));

GenerationPlan::new(/* … */)
    .with_module(ModuleEmission::daemon_module("daemon", shape));
```

The four new positional+typed records (each a non-ZST data-bearing noun, methods
only, NOTA-dialect positional fields — no labels, no flags):

```rust
// ConcurrentNexusTier — the opt-in bundle. Its presence on NexusDaemonShape is
// the single branch the emitter reads to select the concurrent spine. Absent =
// today's serial single-contract escape-hatch-meta daemon, byte-for-byte.
pub struct ConcurrentNexusTier {
    meta_contract: MetaContractTier,      // (2)+(4)  — replaces MetaListenerTier
    concurrency: SharedStoreConcurrency,  // (1)
    frame_bounds: FrameBounds,            // (3)
}
impl ConcurrentNexusTier {
    pub fn new(meta_contract: MetaContractTier,
               concurrency: SharedStoreConcurrency,
               frame_bounds: FrameBounds) -> Self { /* … */ }
    pub fn meta_contract(&self) -> &MetaContractTier { /* … */ }
    pub fn concurrency(&self) -> &SharedStoreConcurrency { /* … */ }
    pub fn frame_bounds(&self) -> FrameBounds { /* … */ }
}

// MetaContractTier — the TYPED second leg. Carries the meta contract module
// (so the emitter emits a real decode->execute->encode spine into
// nexus::SignalInput::MetaInput), the socket mode (kept, defense in depth),
// and the owner authority policy.
pub struct MetaContractTier {
    contract_module: String,         // e.g. "meta_signal_lojix"
    socket_mode: SocketModeBits,     // kept from MetaListenerTier
    owner_authority: OwnerAuthority, // (4)
}

// OwnerAuthority — the fail-closed policy SELECTOR (not the uid datum). The uid
// is deployment-specific runtime config (DaemonConfiguration::owner_user_id),
// so this is an enum over how the edge check behaves, defaulting to the
// fail-closed peer-credential check intent 9v7h mandates.
pub enum OwnerAuthority {
    SocketModeOnly,            // legacy: file mode only, no peer check (NOT lojix)
    PeerCredential,            // 9v7h: read SO_PEERCRED, REJECT on uid mismatch
}
impl OwnerAuthority {
    pub fn peer_credential() -> Self { Self::PeerCredential }
    pub fn socket_mode_only() -> Self { Self::SocketModeOnly }
}

// SharedStoreConcurrency — the BoundedWorkers capacity (the only concurrency
// datum; the per-request-fresh-engine-over-Arc<Store> structure is fixed by the
// hook surface, not configurable).
pub struct SharedStoreConcurrency { worker_capacity: usize }

// FrameBounds — R1 max body bytes + R2 read timeout, positional.
pub struct FrameBounds { max_body_bytes: usize, read_timeout: Duration }
```

`with_concurrent_nexus_tier(self, tier) -> Self` is the new builder method,
mutually exclusive with `with_meta_tier` (escape-hatch meta stays available for
spirit; a component picks one). `is_multi_listener()` becomes
`meta_tier.is_some() || concurrent_nexus_tier.is_some()` — both multi-listener
paths share the binder's two-socket bind; they diverge only in the runtime spine.

## The emitter change (token-based, per-section ToTokens nouns)

All additions are new data-bearing `ToTokens` nouns composed in
`DaemonModuleBody::to_tokens` (`daemon_emit.rs:208-234`), each parameterized by
the shape, never string concatenation. Malformed output fails at `syn::parse2`
(`render`, `:182`). The `DaemonModuleBody` gains the `ConcurrentNexusTier`
reference and branches each section on its presence.

### Hook trait — ComponentDaemonTraitTokens (daemon_emit.rs:303-419)

The default serial trait is emitted UNCHANGED when there's no concurrent tier
(message/spirit safety). When the concurrent tier IS present, emit the ALTERNATIVE
hook surface — a fresh-per-request-engine shape, not a long-lived `&Engine`:

```rust
pub trait ComponentDaemon: Sized + 'static {
    type Configuration: DaemonConfiguration;
    type ConfigurationError: std::error::Error;
    // CONCURRENT VARIANT: a shareable Store + a per-request Engine, replacing
    // the single `type Engine` + one-shot build_runtime.
    type Store: Send + Sync + 'static;       // the Arc-shared durable state
    type Engine;                             // built fresh per request
    type Error: Display + From<FrameError> + From<SignalFrameError> + From<ListenerError>;
    const PROCESS_NAME: &'static str;

    fn load_configuration(path: &Path) -> Result<Self::Configuration, Self::ConfigurationError>;

    // Build the shared store ONCE at bind (replaces build_runtime's one engine):
    fn build_shared_store(configuration: &Self::Configuration)
        -> Result<std::sync::Arc<Self::Store>, Self::Error>;

    // Build a FRESH engine per request over a clone of the shared store
    // (lojix: SchemaRuntime::with_store(store)). Runs on the worker thread.
    fn build_request_engine(store: std::sync::Arc<Self::Store>) -> Self::Engine;

    // The ONE typed execute over the shared Nexus root. Both tiers funnel here.
    // `connection` is the verified peer (owner edge check already passed).
    fn execute_signal(
        engine: &mut Self::Engine,
        signal_input: nexus::SignalInput,
        connection: &triad_runtime::ConnectionContext,
    ) -> Result<nexus::SignalOutput, Self::Error>;
}
```

`execute_signal` is the single funnel — it replaces BOTH `handle_working_input`
(single-contract) AND `handle_meta_stream` (escape hatch) on the concurrent path.
This is property 2 expressed in the hook: the component implements ONE method over
`nexus::SignalInput`/`nexus::SignalOutput` (the schema-emitted nouns from the
nexus target — referenced, never re-invented), exactly lojix's
`RequestWorker::execute` body (`lojix daemon.rs:215-231`). For lojix this hook
becomes a ~6-line method: `SchemaRuntime::with_store` → `execute(NexusWork::
SignalArrived(input).with_origin_route(route))` → `.into_root()` match.

`&mut Self::Engine` (not `&Engine`) because the per-request engine is owned by the
worker and lojix's `execute` takes `&mut engine` (`lojix daemon.rs:220`). Owned-
per-worker means no `Send` bound is needed on `Engine` itself, only on `Store`
(which the `FnOnce + Send + 'static` worker captures via `Arc`).

### Runtime spine — GeneratedDaemonRuntimeTokens (daemon_emit.rs:741-860)

Emit the ALTERNATIVE concurrent spine. This is `LojixRuntime` + `RequestWorker`
lifted into tokens, fully generic over `Daemon: ComponentDaemon`:

```rust
pub struct GeneratedDaemonRuntime<Daemon: ComponentDaemon> {
    store: std::sync::Arc<Daemon::Store>,        // shared, cloned per request
    codec: LengthPrefixedCodec,                  // Copy; built from FrameBounds
    workers: triad_runtime::BoundedWorkers,      // capacity from SharedStoreConcurrency
    owner_user_id: Option<u32>,                  // read from config at bind (9v7h)
    read_timeout: std::time::Duration,           // R2, from FrameBounds
}

impl<Daemon: ComponentDaemon> MultiListenerRuntime for GeneratedDaemonRuntime<Daemon> {
    type Listener = ListenerTier;
    type StartError = Daemon::Error;
    type StopError = Daemon::Error;
    type RequestError = Daemon::Error;
    fn start(&mut self) -> Result<(), Daemon::Error> { Ok(()) }
    fn stop(&mut self) -> Result<(), Daemon::Error> { Ok(()) }

    // OPT-IN concurrency: offload, return immediately. &mut self borrow ends here;
    // the worker is 'static. Shell (MultiListenerDaemon) is UNCHANGED.
    fn handle_stream(&mut self, listener: ListenerTier, stream: UnixStream)
        -> Result<(), Daemon::Error>
    {
        let worker = GeneratedRequestWorker::<Daemon> {
            store: self.store.clone(),
            codec: self.codec,
            owner_user_id: self.owner_user_id,
            read_timeout: self.read_timeout,
            _daemon: PhantomData,
        };
        self.workers.dispatch(move || worker.serve(listener, stream));
        Ok(())
    }
}

struct GeneratedRequestWorker<Daemon: ComponentDaemon> {
    store: std::sync::Arc<Daemon::Store>,
    codec: LengthPrefixedCodec,
    owner_user_id: Option<u32>,
    read_timeout: std::time::Duration,
    _daemon: PhantomData<fn() -> Daemon>,   // legitimate ZST use: type binder
}

impl<Daemon: ComponentDaemon> GeneratedRequestWorker<Daemon> {
    fn serve(self, listener: ListenerTier, mut stream: UnixStream) {
        let result = match listener {
            ListenerTier::Working => self.serve_working(&mut stream),
            ListenerTier::Meta => self.serve_meta(&mut stream),  // typed, not escape hatch
        };
        if let Err(error) = result { /* eprintln typed RequestFailed tail */ }
    }

    fn serve_working(&self, stream: &mut UnixStream) -> Result<(), Daemon::Error> {
        stream.set_read_timeout(Some(self.read_timeout)).map_err(FrameError::Io)?; // R2
        let body = self.codec.read_body(stream).map_err(FrameError::from)?;        // R1 cap
        let connection = ConnectionContext::from_stream(stream).map_err(FrameError::Io)?;
        let (_route, input) = <#working::Input>::decode_signal_frame(body.bytes())?;
        let signal_input = nexus::SignalInput::OrdinaryInput(input);              // funnel
        let mut engine = Daemon::build_request_engine(self.store.clone());
        let output = Daemon::execute_signal(&mut engine, signal_input, &connection)?;
        let reply = Self::ordinary_reply(output)?;                                // re-split
        self.codec.write_body(stream, &FrameBody::new(reply.encode_signal_frame()?))
            .map_err(FrameError::from)?;
        Ok(())
    }

    fn serve_meta(&self, stream: &mut UnixStream) -> Result<(), Daemon::Error> {
        stream.set_read_timeout(Some(self.read_timeout)).map_err(FrameError::Io)?; // R2
        // (4) FAIL-CLOSED OWNER AUTH (9v7h): peer-cred BEFORE decode, BEFORE engine.
        let connection = ConnectionContext::from_stream(stream).map_err(FrameError::Io)?;
        if let Some(owner) = self.owner_user_id {
            if connection.user_id() != owner {
                return Err(ListenerError::owner_uid_mismatch(owner, connection.user_id()).into());
            }
        }
        let body = self.codec.read_body(stream).map_err(FrameError::from)?;        // R1 cap
        let (_route, input) = <#meta::Input>::decode_signal_frame(body.bytes())?;
        let signal_input = nexus::SignalInput::MetaInput(input);                  // funnel
        let mut engine = Daemon::build_request_engine(self.store.clone());
        let output = Daemon::execute_signal(&mut engine, signal_input, &connection)?;
        let reply = Self::meta_reply(output)?;                                    // re-split
        self.codec.write_body(stream, &FrameBody::new(reply.encode_signal_frame()?))
            .map_err(FrameError::from)?;
        Ok(())
    }

    fn ordinary_reply(output: nexus::SignalOutput) -> Result<#working::Output, Daemon::Error> {
        match output {
            nexus::SignalOutput::OrdinaryOutput(o) => Ok(o),
            _ => Err(/* typed wrong-tier error */),
        }
    }
    fn meta_reply(output: nexus::SignalOutput) -> Result<#meta::Output, Daemon::Error> {
        match output {
            nexus::SignalOutput::MetaOutput(o) => Ok(o),
            _ => Err(/* typed wrong-tier error */),
        }
    }
}
```

`#working` and `#meta` are the contract-module path idents the emitter
interpolates from `WorkingListenerTier::contract_module` and
`MetaContractTier::contract_module`. `nexus::{SignalInput, SignalOutput}` are
referenced from the schema-emitted nexus target (constraint: do not invent a
parallel enum). This is property 1 (offload + per-request engine over `Arc`) +
property 2 (both contracts → one Nexus root, re-split by tier) + property 4
(fail-closed meta edge check) in one spine.

### Binder — DaemonBinder (daemon_emit.rs:489-551)

On the concurrent path the multi-listener `bind` builds the runtime from the
store + bounds + worker capacity + `configuration.owner_user_id()` instead of
`GeneratedDaemonRuntime::new(engine)`:

```rust
let store = Daemon::build_shared_store(&configuration)?;
let bounds = /* FrameBounds baked from the shape */;
let runtime = GeneratedDaemonRuntime::<Daemon> {
    store,
    codec: LengthPrefixedCodec::new(MaximumFrameLength::new(#max_body_bytes)),
    workers: BoundedWorkers::new(#worker_capacity),
    owner_user_id: configuration.owner_user_id(),    // runtime datum (9v7h)
    read_timeout: Duration::from_millis(#read_timeout_millis),
};
// same two-socket Vec<ListenerSocket<ListenerTier>> bind as today, socket_mode kept
```

The two-socket bind (Working at `socket_path()`, Meta at `meta_socket_path()` with
`socket_mode`) is unchanged — owner peer-cred is defense-in-depth ON TOP of the
mode bind (constraint, survey 1 §property-4).

### Transport — property 3 on the default path too

`FrameBounds` is read by the concurrent worker (above). For the DEFAULT serial
path, survey 3 wants R1/R2 as a strict improvement without breaking byte-stability
of spirit/message. Resolution: keep the default `WorkingTransport` emitting
`LengthPrefixedCodec::default()` and no timeout UNLESS the component opts into a
standalone `with_frame_bounds(FrameBounds)` on `NexusDaemonShape` (a second, also-
optional builder, independent of the concurrent tier). Default-absent = byte-
identical today; the concurrent tier carries its own bounds inline. This keeps
the "opt-in, default unchanged" contract absolute while letting spirit later
harden without adopting concurrency.

### Section composition

Add to `DaemonModuleBody::to_tokens` (`:208-234`): when `concurrent_nexus_tier`
is `Some`, emit `ConcurrentSpineTokens` (the runtime + worker section above) in
place of `GeneratedDaemonRuntimeTokens`, and `ConcurrentHookTraitTokens` in place
of the default `ComponentDaemonTraitTokens`. Each is its own `ToTokens` noun
parameterized by the shape. The imports section gains `#meta::{Input, Output}`,
`nexus::{SignalInput, SignalOutput}`, `BoundedWorkers`, `Arc`, `PhantomData`,
`Duration` ONLY on the concurrent path.

## The single triad-runtime change

One defaulted accessor on the `DaemonConfiguration` trait (`process.rs:89-116`):

```rust
/// The owner user id authorised on the meta tier. `None` leaves the meta tier
/// authorised by socket file mode only; `Some(uid)` makes the emitted meta path
/// reject any peer whose SO_PEERCRED uid differs (intent 9v7h).
fn owner_user_id(&self) -> Option<u32> { None }
```

Default `None` keeps every existing consumer source-compatible. Plus a typed
constructor on `ListenerError` for the reject (`owner_uid_mismatch(expected,
actual)`), so the fail-closed rejection is a typed listener error that
`Daemon::Error: From<ListenerError>` already absorbs — no new error plumbing in
the emitter. `BoundedWorkers`, `ConnectionContext::from_stream`,
`LengthPrefixedCodec`, `MaximumFrameLength` stay generic and UNCHANGED; the
`MultiListenerDaemon` shell and both runtime-trait `handle_stream` signatures
(`&mut self`, bare `UnixStream`) stay UNCHANGED (survey 2's decisive option B).

## What lojix daemon.rs collapses to

Today lojix `triad-port/src/daemon.rs` is ~280 lines of hand-written daemon
boilerplate. After adoption, ALL of these DELETE because the emitter generates
them:

- `LojixRuntime` struct + `MultiListenerRuntime` impl (`:121-166`) — emitted as
  `GeneratedDaemonRuntime` + its impl.
- `RequestWorker` struct + `serve`/`serve_ordinary`/`serve_owner` (`:168-210`) —
  emitted as `GeneratedRequestWorker` + `serve`/`serve_working`/`serve_meta`.
- `ordinary_reply`/`meta_reply` tier re-split (`:262-274`) — emitted.
- `invariant_rejection` (`:233-260`) — emitted as the typed wrong-tier/`serve`
  error tail (the emitter's generic version returns a typed error; lojix's
  bespoke `QueryRejected`/`DeployRejected` rejection bodies move INTO
  `execute_signal`'s invariant arm, where they belong as engine policy).
- `MAXIMUM_CONCURRENT_REQUESTS` / `MAXIMUM_REQUEST_FRAME_BYTES` /
  `REQUEST_READ_TIMEOUT` consts — replaced by the `ConcurrentNexusTier` shape
  fields in `build.rs`.
- the two-socket `MultiListenerDaemon` bind, `ListenerRole` enum, socket-mode
  validation, argv/exit plumbing — emitted by the binder + `DaemonEntry`.

What REMAINS hand-written in lojix (the irreducible nix-effect plane + the store):

- `Store` (the `Arc<Store>` durable in-memory tables) — becomes
  `ComponentDaemon::Store`, built by a ~3-line `build_shared_store`.
- `SchemaRuntime` (the `NexusEngine` + `SemaEngine` impl — the actual nix-effect
  decision engine) — unchanged; `build_request_engine` is a one-liner
  `SchemaRuntime::with_store(store)`.
- the `ComponentDaemon` impl itself: `type Store = Store`, `type Engine =
  SchemaRuntime`, `execute_signal` (the ~6-line `with_origin_route` →
  `into_root()` match, lifted verbatim from `RequestWorker::execute`), and
  `build_shared_store`/`build_request_engine`.

Net: lojix `daemon.rs` collapses from ~280 lines to a ~40-line `ComponentDaemon`
impl + the `Store`/`SchemaRuntime` modules it already has elsewhere. The nix
effect plane (SchemaRuntime) and the durable Store are kept; everything that is
transport/concurrency/tier-routing boilerplate is generated. The origin-route
seam (`OriginRoute(0)` today) becomes a real owner route minted from the verified
`connection` inside `execute_signal` — the fail-closed edge check at the transport
guarantees the meta path only reaches the engine for the verified owner.

## Cloud adoption

cloud (`cloud/src/schema_daemon.rs`) is the SECOND adopter and the proof the shape
is not lojix-private. cloud already hand-writes properties 2+3 (one
`nexus::SignalInput` funnel, 8 MiB + 10 s bounds) and the per-request
`SchemaRuntime::with_store(Arc<SchemaStore>)` engine — it is structurally lojix
MINUS the `BoundedWorkers` offload (it runs `serve_ordinary`/`serve_owner` inline,
hence serial). Adopting the emitted concurrent spine gives cloud the offload it
lacks for free, plus collapses its hand-written `CloudRuntime`/transport/binder
the same way lojix's collapses. cloud declares the identical `ConcurrentNexusTier`
in its `build.rs` (its own contract module names, its own `worker_capacity`),
implements the same ~40-line `ComponentDaemon`, and deletes its hand-written
runtime. cloud also gains property 4 (it shares lojix's `OriginRoute(0)` hardcode
today). The design is sized for both from the start: the `ConcurrentNexusTier`
bundle IS the cloud/lojix shared shape.

## Consumer impact (the must-not-break set)

- spirit: emitter consumer, multi-tier, single long-lived `&self` engine + the
  `handle_meta_stream` escape hatch + full streaming. Does NOT set
  `with_concurrent_nexus_tier` (keeps `with_meta_tier`), so the emitter takes the
  UNCHANGED default multi-listener spine: serial, `&self` engine, escape-hatch
  meta. Regenerates byte-identically. Its meta is request/reply `Configure` over a
  component-owned transport, NOT a second `nexus::SignalInput` leg — the typed-meta
  funnel would break it, so it stays opt-in.
- message: emitter consumer, `SingleListenerDaemon`, `Mutex<MessageEngine>`, engine
  `handle` takes `&mut self`, no `Arc<Store>`, cannot satisfy `Send + 'static`
  without new work. No meta tier, no concurrent tier. Default single-listener spine
  UNCHANGED → byte-identical regeneration. This is the consumer that proves
  concurrency MUST be opt-in.
- cloud / lojix: `MultiListenerDaemon`-direct, hand-written, never see the emitter
  TODAY. Unaffected until they choose to adopt; adoption is the design's payoff.
- repository-ledger: depends on neither the emitter nor triad-runtime (raw
  `UnixListener` + `thread::spawn` over `Arc<Mutex<Store>>`). Entirely outside the
  blast radius; shares no surface; cannot break.

## Staged plan

1. triad-runtime seam (smallest, lowest risk): add the defaulted
   `DaemonConfiguration::owner_user_id() -> Option<u32> { None }` accessor +
   `ListenerError::owner_uid_mismatch` constructor. Default `None` is source-
   compatible for every consumer. Ship + bump pins. Operator-owned on main.
2. Emitter declaration types: add `ConcurrentNexusTier`, `MetaContractTier`,
   `OwnerAuthority`, `SharedStoreConcurrency`, `FrameBounds`, the standalone
   `with_frame_bounds`, and `with_concurrent_nexus_tier` builder + the
   `is_multi_listener()` extension. No emission behavior yet; pure declaration
   surface + tests that the builders construct. Existing components re-emit byte-
   stable (field absent).
3. Emitter concurrent spine: emit `ConcurrentHookTraitTokens` +
   `ConcurrentSpineTokens` (runtime + worker + tier re-split + fail-closed meta
   edge) gated on `concurrent_nexus_tier.is_some()`. Verify spirit + message
   regenerate byte-identically (the regression gate). Property 3 default-path
   bounds gated on `with_frame_bounds`.
4. lojix adoption: lojix `build.rs` declares the `ConcurrentNexusTier`; lojix
   `daemon.rs` collapses to the ~40-line `ComponentDaemon` impl; delete the
   hand-written runtime/worker/binder. Wire `owner_user_id()` into lojix's
   `DaemonConfiguration` impl and mint the real owner `OriginRoute` in
   `execute_signal`. This is the property-4 close (audit R3 + intent 9v7h).
5. cloud adoption (follow-on, same shape): cloud declares the identical bundle and
   collapses `CloudRuntime`; gains the `BoundedWorkers` offload it lacks.

## Risks

- The `ComponentDaemon` concurrent variant changes associated types (`type Store`
  + two build fns + `execute_signal`) vs the default trait (`type Engine` +
  `build_runtime` + `handle_working_input`). These are DIFFERENT trait shapes for
  the same trait name, selected by the shape — the emitter must emit one or the
  other, never both. Mitigation: the trait body is wholly inside the gated
  `ConcurrentHookTraitTokens`; a component cannot mix. But it means a component
  migrating from serial to concurrent rewrites its hook impl (acceptable — only
  lojix/cloud, both hand-written today, ever do this).
- `stop` does not drain in-flight workers (survey 2 open question 2): `BoundedWorkers`
  has no join surface; `stop` is a no-op and workers finish on their own threads
  after the accept loop exits. This matches lojix's current behavior — not a
  regression — but flag for cloud if it wants graceful drain. If drain is needed
  it is a triad-runtime `BoundedWorkers` addition, not an emitter change.
- Read timeout starts when the worker RUNS, not at accept; under backpressure
  (all permits held) a connection waits in the OS listen backlog without a
  timeout. Identical to lojix today; a known property, not a regression.
- The standalone `with_frame_bounds` for the serial path adds a second optional
  field on `NexusDaemonShape` — care needed that absent-both stays byte-stable
  (default codec, no timeout). Covered by the step-3 regression gate.
- Short-header tier collision (audit R7: meta `Deploy` == ordinary `Query` ==
  `0x0`) is a contract-side wart the `_route` discard hides; the typed re-split by
  LISTENER (not by header) sidesteps it in the daemon, but flag it for the
  contract bump.

## Report path

This draft: `/home/li/primary/reports/cloud-designer/33-lojix-daemon-emitter-integration-design/4-design-draft.md`
