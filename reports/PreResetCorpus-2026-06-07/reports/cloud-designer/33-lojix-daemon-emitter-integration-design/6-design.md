# 6 — design: the concurrent-Nexus daemon emitter

cloud-designer, 2026-06-06. The final, adversarially-reviewed design for
integrating lojix's daemon needs into the core-crate emitter (Spirit `tj99`),
with fail-closed owner auth (Spirit `9v7h`). Grounded in `1`/`2`/`3`, drafted in
`4`, reviewed in `5`. **This is a proposal for psyche review before any emitter
code lands.**

## The shape of the change in one picture

The generated daemon today is **serial, single-typed-contract, escape-hatch
meta, unbounded transport, no peer auth**. lojix (and cloud) hand-wrote the
opposite. The change lets a component *declare* the lojix/cloud shape and have
the emitter generate it — **without touching the runtime shell and without
disturbing any existing consumer**.

The governing decisions, all confirmed by review:

- **Option B — emit concurrency into the runtime, never into the shell.** The
  `triad-runtime` `MultiListenerDaemon` accept loop and both
  `MultiListenerRuntime::handle_stream(&mut self, …)` signatures stay
  byte-identical. Concurrency comes entirely from the *emitted* runtime
  offloading inside its own `handle_stream` onto `BoundedWorkers` — exactly what
  lojix does by hand today. Option A (push offload into the shell, forcing
  `Arc<Self>+Sync`) is rejected: it would break `message`'s actor `&mut self`
  and double-concurrency actor daemons.
- **One opt-in bundle, not four flags.** The four properties are a single
  adoption unit (cloud already ships properties 2+3 together; lojix ships all
  four together; no component wants concurrency-without-bounds or
  typed-meta-without-fail-closed). They are declared as one `ConcurrentNexusTier`.
- **The mutual-exclusion invariant lives in the type.** The meta tier is ONE
  field carrying an enum of {escape-hatch, concurrent-Nexus}, so a component
  *structurally cannot* declare both shapes (revision 6).

## The schema-declaration surface (what a component author writes)

In the component's `build.rs` (NOT the `.schema` file — daemon topology is
build-declared, like `meta_socket_mode` today). All records are non-ZST
data-bearing nouns with positional typed `new(…)` constructors, full-English
field names, no labels, no flags:

```
NexusDaemonShape {
  process_name: String,
  working_tier: WorkingListenerTier,          // contract_module
  meta: Option<MetaTierShape>,                // revision 6: ONE field, not two Options
  frame_bounds: Option<FrameBounds>,          // serial-path hardening (revision 9)
}

enum MetaTierShape {                          // structurally one-of
  EscapeHatch(MetaListenerTier),              // today's shape — spirit keeps this
  ConcurrentNexus(ConcurrentNexusTier),       // the new lojix/cloud shape
}

ConcurrentNexusTier {
  meta_contract: MetaContractTier,
  concurrency:   SharedStoreConcurrency,
  frame_bounds:  FrameBounds,
}
MetaContractTier { contract_module: String, socket_mode: SocketModeBits, owner_authority: OwnerAuthority }
enum OwnerAuthority { SocketModeOnly, PeerCredential }      // peer_credential() = the 9v7h default
SharedStoreConcurrency { worker_capacity: usize }          // BoundedWorkers cap
FrameBounds { max_body_bytes: usize, read_timeout: Duration }   // R1 + R2
```

lojix's declaration:

```
NexusDaemonShape::new([lojix], WorkingListenerTier::new([signal_lojix]))
  .with_concurrent_nexus_tier(ConcurrentNexusTier::new(
      MetaContractTier::new([meta_signal_lojix], SocketModeBits::new(0o600), OwnerAuthority::peer_credential()),
      SharedStoreConcurrency::new(64),
      FrameBounds::new(8 * 1024 * 1024, Duration::from_secs(10))))
```

`spirit` keeps `with_meta_tier(MetaListenerTier::new(…))` (→ `EscapeHatch`) and
optionally adds `with_frame_bounds(FrameBounds::new(…))` to harden its serial
transport without adopting concurrency. `message` sets neither and regenerates
byte-identically.

The emitter's gating switches from the boolean `is_multi_listener()` to a
three-valued `listener_shape() -> ListenerShape { SingleSerial, MetaEscapeHatch,
ConcurrentNexus }` (revision 6); every one of the six gated emission sites
matches the enum and emits its own arm.

## The triad-runtime change (stage 1 — the only kernel edit)

Two additive, source-compatible changes to `triad-runtime`:

1. **`DaemonConfiguration::owner_user_id(&self) -> Option<u32> { None }`**
   (`process.rs:89-116`) — the owner uid is a deployment-specific runtime datum;
   follows the established defaulted-`None` accessor pattern
   (`meta_socket_path`/`trace_socket_path`/`meta_socket_mode`), so every existing
   impl keeps compiling.
2. **`ListenerError::OwnerUidMismatch { expected: u32, actual: u32 }`** + its
   `thiserror` `#[error(…)]` arm (revision 2). `ListenerError` is single-variant
   today; this is a real (additive) variant on the shared kernel, source-compatible
   because it is matched non-exhaustively everywhere (`MultiListenerDaemonError`
   `From` impls, `message`'s `#[from] ListenerError`).

Everything else the four properties need — `BoundedWorkers`,
`ConnectionContext::from_stream`, `LengthPrefixedCodec`/`MaximumFrameLength` —
already exists at HEAD and stays generic and unchanged. `forbid(unsafe_code)`
holds (peer-cred read is the safe `rustix` wrapper).

## The emitter change (stages 2-3 — all token-based `quote!`/`ToTokens`)

New data-bearing `ToTokens` nouns composed in `DaemonModuleBody::to_tokens`,
selected by `listener_shape()`. On the `ConcurrentNexus` arm:

**Alternative hook trait (`ConcurrentHookTraitTokens`).** Replaces both
`handle_working_input` and `handle_meta_stream` with a single funnel:

```rust
pub trait ComponentDaemon: Sized + 'static {
    type Configuration: DaemonConfiguration;
    type Store: Send + Sync + 'static;
    type Engine: Send + 'static;                 // revision 8
    type Error: Display + Send + 'static          // revision 8
        + From<FrameError> + From<SignalFrameError> + From<MetaSignalFrameError>  // revision 1
        + From<ListenerError>;
    const PROCESS_NAME: &'static str;
    fn build_shared_store(&Configuration) -> Result<Arc<Store>, Error>;
    fn build_request_engine(Arc<Store>) -> Engine;
    fn execute_signal(&mut Engine, nexus::SignalInput, &ConnectionContext) -> Result<nexus::SignalOutput, Error>;
}
```

`SignalFrameError` (working) and `MetaSignalFrameError` (meta, imported under a
distinct ident) are both absorbed — revision 1. `nexus::{SignalInput,
SignalOutput}` are referenced from the schema-emitted nexus target, never
re-invented.

**Concurrent spine (`ConcurrentSpineTokens`).** `GeneratedDaemonRuntime` owns
`Arc<Store>` + a `Copy` `LengthPrefixedCodec` (built from `FrameBounds`) +
`BoundedWorkers` + `owner_user_id: Option<u32>` + `read_timeout` — **not** a
long-lived engine. `handle_stream(&mut self, …)` clones those into a
`GeneratedRequestWorker<Daemon>` (`PhantomData<fn()->Daemon>` type-binder,
legitimate), `workers.dispatch(move || worker.serve(...))`, returns `Ok(())`
immediately (back-pressured at the permit cap). The worker's `serve`:

1. `stream.set_read_timeout(Some(read_timeout))` (R2);
2. **meta path only:** `ConnectionContext::from_stream`; if
   `owner_user_id == Some(owner) && connection.user_id() != owner`, **construct
   `OwnerUidMismatch`, log it locally, drop the stream — before any
   read/decode/engine** (revision 3: this NOT-executing IS the fail-closed
   property; the error does not propagate cross-thread);
3. `read_body` with the R1 cap;
4. decode the tier's typed `Input`, wrap into `nexus::SignalInput::{OrdinaryInput |
   MetaInput}`;
5. `build_request_engine(store.clone())` → a fresh per-request engine;
6. `execute_signal`; re-split `nexus::SignalOutput` by **listener tier** (not by
   header byte — sidesteps the audit-R7 short-header collision); wrong tier → a
   typed error; `write_body` the reply.

**Transport (`WorkingTransportTokens`).** Parameterized by the configured
`MaximumFrameLength` + optional `read_timeout` constructed in `bind` (revision 9).
When neither tier nor `with_frame_bounds` is set, it emits the existing
`LengthPrefixedCodec::default()` body + no timeout **verbatim** (byte-stable —
the stage-3 regression gate asserts this).

**Bind-time fail-closed assertion.** When the shape declares
`OwnerAuthority::PeerCredential`, the emitted `DaemonBinder::bind` returns a typed
configuration `DaemonError` if `configuration.owner_user_id()` is `None` — a hard
startup failure, not a silent downgrade (revision 10).

**Emit-time exclusions.** `ConcurrentNexus` is mutually exclusive with
`emits_stream` (revision 7 — the per-request-worker model has nowhere to host the
long-lived `EmittedSubscriptions` registry); asserted at emit time alongside the
`syn::parse2` guard. Concurrent + streaming is a separate future design (the
registry would move into the shared-store plane).

## Fail-closed owner auth — precise semantics (9v7h)

The enforcement is **100% the edge reject**: the meta worker reads the peer uid
and, on mismatch, drops the connection before the engine is ever reached. The
"mint a real owner `OriginRoute`" idea is **cosmetic/forward-looking only** today
— `SchemaRuntime` underscore-ignores the route (`schema_runtime.rs:1419-1433`),
so route-minting changes nothing observable until a future engine change consumes
it (revision 4). This is defense-in-depth **on top of** the socket file-mode bind,
which stays.

## What lojix's `daemon.rs` collapses to (stage 4)

From ~280 lines to a small `ComponentDaemon` impl. **Deleted (all emitted):**
`LojixRuntime` + `MultiListenerRuntime` impl, `RequestWorker` +
`serve`/`serve_ordinary`/`serve_owner`, `ordinary_reply`/`meta_reply` re-split,
`invariant_rejection` (its bespoke `QueryRejected`/`DeployRejected` bodies move
into `execute_signal`'s invariant arm — engine policy), the
`MAXIMUM_CONCURRENT_REQUESTS`/`MAXIMUM_REQUEST_FRAME_BYTES`/`REQUEST_READ_TIMEOUT`
consts (now `ConcurrentNexusTier` fields), the two-socket bind / `ListenerRole`
enum / socket-mode validation / argv+exit plumbing (binder + `DaemonEntry`).

**Kept hand-written (the genuinely lojix-specific residue):** `Store`
(`ComponentDaemon::Store`, built by a ~3-line `build_shared_store`) and
`SchemaRuntime` — the nix-effect `NexusEngine`+`SemaEngine` decision plane —
unchanged; `build_request_engine` is a one-liner `SchemaRuntime::with_store`;
`execute_signal` is the ~6-line `with_origin_route`→`into_root()` match lifted
from `RequestWorker::execute`.

**Adoption plumbing the collapse adds (revision 5, previously undercounted):** a
`ListenerError` arm + `From<ListenerError>` impl on lojix's `Error` (absent
today); an `owner_user_id` field on lojix's `DaemonConfiguration` and an impl of
triad-runtime's `DaemonConfiguration` trait (lojix's is a plain rkyv struct
today, not the trait). Net is still a large deletion, but these are real items.

## cloud adoption (stage 5 — proves the shape is shared)

`cloud/src/schema_daemon.rs` is structurally **lojix minus the `BoundedWorkers`
offload**: identical `nexus::SignalInput::{OrdinaryInput,MetaInput}` funnel,
identical 8 MiB + 10 s bounds, identical per-request `SchemaRuntime::with_store`
engine — but `CloudRuntime::handle_stream` runs `serve_*` inline, so it is serial
today only because `MultiListenerDaemon` calls `handle_stream` serially. cloud
declares the identical `ConcurrentNexusTier` (its own module names + capacity),
collapses `CloudRuntime`, and **gains the offload it lacks** plus property 4
(same `OriginRoute(0)` seam, same fix). This second adopter is why the bundle is
sized for both from the start, not lojix-private.

## Consumer safety (verified)

- **`message`** (Kameo actor, `Mutex<MessageEngine>`, `&mut self`, no `Arc<Store>`,
  can't satisfy `Send+'static` without new work): sets no meta/concurrent tier →
  default single-listener serial spine, byte-identical. The proof concurrency must
  be opt-in.
- **`spirit`** (`with_meta_tier` escape hatch + streaming): keeps `EscapeHatch` →
  unchanged default multi-listener spine, byte-identical. Its meta is request/reply
  `Configure` over a component-owned transport, NOT a `nexus::SignalInput` leg, so
  the typed funnel stays opt-in. May later add `with_frame_bounds` alone.
- **`repository-ledger`** (raw `UnixListener` + `thread::spawn`, no emitter/runtime
  dep): outside the blast radius; shares no surface.

## Staged plan

| Stage | Repo | Work |
|---|---|---|
| 1 | triad-runtime | `owner_user_id()` accessor + `ListenerError::OwnerUidMismatch` variant. Ship + pin-bump. |
| 2 | schema-rust-next | The declaration records + builders + `listener_shape()` selector. No emission behavior yet; existing components re-emit byte-stable. |
| 3 | schema-rust-next | Emit the concurrent hook trait + spine + parameterized transport + bind-time assertion, gated on `ConcurrentNexus`; serial `with_frame_bounds`. **Regression gate: `spirit` + `message` regenerate byte-identically.** Emit-time exclusions (concurrent×stream, escape-hatch×concurrent). Emission test asserts the `Send+'static` bounds. |
| 4 | lojix | Declare the tier; collapse `daemon.rs`; add the `ListenerError`/`DaemonConfiguration`-trait plumbing; close audit R3 + 9v7h. |
| 5 | cloud | Declare the identical tier; collapse `CloudRuntime`; gain the offload + property 4. |

## Carried uncertainties (for psyche / future design)

- **Graceful drain.** `stop` does not join in-flight workers (`BoundedWorkers` has
  no join surface) — matches lojix today (not a regression). If cloud wants
  graceful drain, that is a future `BoundedWorkers` addition, not an emitter change.
- **Backpressure + read timeout.** The read timeout starts when the worker *runs*;
  under full backpressure a connection waits in the OS backlog untimed (identical
  to lojix today).
- **Audit R7.** The short-header tier collision (meta `Deploy` == ordinary `Query`
  == `0x0`) is sidestepped inside the daemon by re-splitting on *listener tier*,
  but remains a contract-side wart worth fixing in the contract bump.
- **Concurrent streaming.** Deferred by construction (revision 7); revisit when the
  streaming surface stabilizes and the subscription registry can live in the
  shared-store plane.
