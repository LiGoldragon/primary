# 1 — emitter internals: where the four lojix properties must land

cloud-designer ground survey of the schema-rust-next DAEMON EMITTER, 2026-06-06.
Pins: `schema-rust-next` `6685e7b`, `triad-runtime` `f9c38e2`, `lojix/triad-port`
`c8c4353`. Companion to the design report (forthcoming `2-…`) and prior survey
`reports/cloud-designer/32-core-crate-refresh-for-lojix/`.

This report maps the emitter's internals to the four properties the generated
daemon must grow (concurrency, two-typed-contracts-one-Nexus-root, transport
hardening, fail-closed owner auth). It pinpoints the EXACT lines that are the
seam for each, and the exact declaration site where new shape options would be
read. It proposes nothing yet — it is the precise substrate the design rests on.

## The emission pipeline, end to end

The daemon module is one of several `ModuleEmission`s in a component's
`GenerationPlan` (built in the component's `build.rs`). The switch is a single
declaration:

- `ModuleEmission::daemon_module(module, daemon_shape)`
  (`schema-rust-next/src/build.rs:129-136`) — off by default; ON only when a
  component passes a `NexusDaemonShape`. It sets the emission target to
  `RustEmissionTarget::SignalRuntime` and stashes `daemon_shape: Some(shape)`.
- `GeneratedModule::from_emission` (`build.rs:403-438`) branches on
  `emission.daemon_shape()`: `Some(shape)` lowers the named module's `.schema`
  to a `Schema` and calls
  `DaemonModule::new(shape.clone(), &schema, "schema-rust-next").to_generated_file()`
  (`build.rs:416-425`); `None` runs the ordinary `RustEmitter`.
- `DaemonModule::render` (`daemon_emit.rs:180-188`) builds the whole body as ONE
  `proc_macro2::TokenStream` (`DaemonModuleBody`), parses it through
  `syn::parse2::<syn::File>` (malformed emitted Rust fails HERE, at emission
  time), and pretty-prints once via `prettyplease`. The `// @generated` header is
  prepended as text (prettyplease drops non-doc comments). Output path is the
  fixed `src/schema/daemon.rs` (`daemon_emit.rs:165`).

Every emitted section is its own `ToTokens` data-bearing noun, composed in
`DaemonModuleBody::to_tokens` (`daemon_emit.rs:208-234`): imports, hook trait,
command, binder, transport, optional subscriptions, runtime, error, exit. The
token-first discipline is load-bearing: **any new emitted code is `quote!`
tokens, never string concatenation** (the discipline brief and the module doc
both restate this).

## How the daemon shape is DECLARED today (the read sites for new options)

The shape is three types in `daemon_emit.rs:42-139`. New declared options
(`concurrent?`, `two-typed-contracts?`, `owner-uid auth?`, `frame bounds?`)
would be NEW positional fields on these:

- `NexusDaemonShape` (`daemon_emit.rs:42-78`): `process_name: String`,
  `working_tier: WorkingListenerTier`, `meta_tier: Option<MetaListenerTier>`.
  `is_multi_listener()` (`75-77`) returns `meta_tier.is_some()` — the single vs
  multi switch ALL sections branch on. Builder: `new(process_name, working_tier)`
  + `with_meta_tier(meta_tier)`. **This is the type a concurrency flag and a
  frame-bounds value attach to** (e.g. `concurrency: ConcurrencyShape`,
  `frame_bounds: FrameBounds`), read by the binder + runtime + transport sections.
- `WorkingListenerTier` (`daemon_emit.rs:82-97`): `contract_module: String` —
  the single signal module whose `Input`/`Output` root the spine drives. **This
  is where a SECOND typed contract for the meta tier would attach** (turning the
  meta tier from an escape hatch into a typed `meta_contract_module`).
- `MetaListenerTier` (`daemon_emit.rs:103-116`): `socket_mode: SocketModeBits`
  only. **This is where an owner-uid auth policy would attach** (e.g.
  `owner_authority: OwnerAuthority`).
- `SocketModeBits` (`daemon_emit.rs:119-139`): wraps `u32`; `octal_literal()`
  emits the `0o600`-form `syn::LitInt` the binder default uses.

These are constructed in the COMPONENT's `build.rs`, NOT in the `.schema` file —
the survey's "declared in build.rs" finding is confirmed. The `emits_stream`
flag is the one piece derived from the schema (`DaemonModule::new`,
`daemon_emit.rs:155`: `!schema.streams().is_empty()`), so the precedent exists
for deriving shape from schema, but the daemon TIER topology is explicitly
build.rs-declared, not schema-derived (fork-2 rationale, `daemon_emit.rs:37-41`).

## EXACT signatures of the emitted surfaces

### `ComponentDaemon` hook trait (`daemon_emit.rs:367-416`)

The only daemon code the component hand-writes. Associated types + the
load-bearing methods:

```rust
pub trait ComponentDaemon: Sized + 'static {
    type Configuration: DaemonConfiguration;
    type ConfigurationError: std::error::Error;
    type Engine;
    type Error: std::fmt::Display + From<FrameError> + From<SignalFrameError> + From<ListenerError>;
    // (streaming-only associated types when emits_stream)
    const PROCESS_NAME: &'static str;

    fn load_configuration(path: &std::path::Path) -> Result<Self::Configuration, Self::ConfigurationError>;
    fn build_runtime(configuration: &Self::Configuration) -> Result<Self::Engine, Self::Error>;
    fn start(engine: &mut Self::Engine) -> Result<(), Self::Error> { … }
    fn stop(engine: &mut Self::Engine) -> Result<(), Self::Error> { … }

    // THE working hook — connection already threaded (6685e7b):
    fn handle_working_input(
        engine: &Self::Engine,
        input: Input,
        connection: &triad_runtime::ConnectionContext,
    ) -> Result<Output, Self::Error>;

    // meta hook — emitted only when meta_tier.is_some() (daemon_emit.rs:339-345):
    fn handle_meta_stream(engine: &Self::Engine, stream: UnixStream) -> Result<(), Self::Error>;
    // (streaming hooks when emits_stream)
}
```

Two facts the design hinges on:

1. **`handle_working_input` already takes `&Engine` (shared, not `&mut`) and a
   `&ConnectionContext`** (`daemon_emit.rs:412`). The ConnectionContext seam for
   working requests is ALREADY THREADED (commit `6685e7b`). What is missing is
   that this is a SINGLE-contract hook (`Input`/`Output` of one module), not the
   two-contract `nexus::SignalInput::{OrdinaryInput,MetaInput}` funnel.
2. **The meta tier is `handle_meta_stream(engine, stream)` — a raw
   read/handle/write escape hatch** (`daemon_emit.rs:343`). It takes the whole
   `UnixStream`, NOT a decoded typed input, and returns `()` not a typed Output.
   It does NOT receive a `ConnectionContext`. This is property-2's and
   property-4's defect site: the owner tier is neither typed-into-the-Nexus-root
   nor peer-cred-guarded.

### `GeneratedDaemonRuntime` — the decode→execute→encode spine (`daemon_emit.rs:825-857`)

```rust
pub struct GeneratedDaemonRuntime<Daemon: ComponentDaemon> {
    engine: Daemon::Engine,                 // ONE long-lived engine
    // subscriptions: EmittedSubscriptions<Daemon>,  // emits_stream only
}

impl<Daemon: ComponentDaemon> GeneratedDaemonRuntime<Daemon> {
    fn new(engine: Daemon::Engine) -> Self { … }

    fn handle_working_stream(&self, stream: UnixStream) -> Result<(), Daemon::Error> {
        let connection = ConnectionContext::from_stream(&stream).map_err(FrameError::Io)?; // :843
        let mut transport = WorkingTransport::new(stream);                                  // :844
        // (subscription_writer clone when emits_stream)
        let frame = transport.read_frame()?;                                                // :846
        let (_route, input) = Input::decode_signal_frame(&frame)?;                          // :847
        // (subscription_filter when emits_stream)
        let output = Daemon::handle_working_input(&self.engine, input, &connection)?;       // :849
        transport.write_frame(output.encode_signal_frame()?)?;                              // :850
        // (subscription_publish when emits_stream)
        Ok(())
    }
}
```

The runtime-trait impl (`daemon_emit.rs:767-815`) wires `handle_stream` to this:

- Multi-listener (`767-794`): `impl MultiListenerRuntime`, `type Listener =
  ListenerTier`, `handle_stream(&mut self, listener, stream)` matches —
  `ListenerTier::Working => self.handle_working_stream(stream)` (**:789**),
  `ListenerTier::Meta => Daemon::handle_meta_stream(&self.engine, stream)`
  (**:790**).
- Single-listener (`796-813`): `impl DaemonRuntime`, `handle_stream(&mut self,
  stream)` → `self.handle_working_stream(stream)` (**:811**).

### `DaemonBinder` (`daemon_emit.rs:489-551`)

A default-method trait `impl<Daemon: ComponentDaemon> DaemonBinder for Daemon {}`.
The `bind` method is shape-selected:

- Multi (`498-523`): builds engine, `GeneratedDaemonRuntime::new(engine)`, a
  `Vec<ListenerSocket<ListenerTier>>` starting with `ListenerTier::Working` at
  `configuration.socket_path()`, then pushes `ListenerTier::Meta` at
  `configuration.meta_socket_path()` with
  `configuration.meta_socket_mode().unwrap_or_else(|| SocketMode::new(#socket_mode))`
  (the octal default from `MetaListenerTier`). Returns
  `MultiListenerDaemon::new(sockets, runtime, RequestErrorLog::new(PROCESS_NAME))`.
- Single (`525-537`): `SingleListenerDaemon::new(configuration.socket_path(),
  runtime, …)`.

`bind` is where the per-request shared-store handoff would be set up if the
runtime grew a `BoundedWorkers` + `Arc<Store>` instead of an owned engine.

### `WorkingTransport` (`daemon_emit.rs:558-595`)

```rust
struct WorkingTransport { stream: UnixStream }
impl WorkingTransport {
    fn new(stream: UnixStream) -> Self { … }
    fn read_frame(&mut self) -> Result<Vec<u8>, FrameError> {
        Ok(LengthPrefixedCodec::default().read_body(&mut self.stream)?.into_bytes()) // :575
    }
    fn write_frame(&mut self, frame: Vec<u8>) -> Result<(), FrameError> {
        LengthPrefixedCodec::default().write_body(&mut self.stream, &FrameBody::new(frame))?; // :582
        self.stream.flush()?; Ok(())
    }
    fn try_clone_stream(&self) -> Result<UnixStream, FrameError> { … }
}
```

This is property-3's defect site (see below).

### `DaemonCommand` / `DaemonError` / `DaemonEntry`

- `DaemonCommand<Daemon>` (`daemon_emit.rs:431-469`): `from_environment()`,
  `from_arguments(..)`, `configuration() -> Result<Daemon::Configuration, …>`
  (single-argument rule: exactly one rkyv `SignalFile`; `InlineNota`/`NotaFile`
  rejected), `run()` → `Daemon::bind(self.configuration()?)?.run()`.
- `DaemonError<Daemon>` (`daemon_emit.rs:936-963`): enum `Argument(ArgumentError)
  | Configuration(Daemon::ConfigurationError) | Listener(ListenerError) |
  Component(Daemon::Error)`; `From<ArgumentError>` + a shape-selected
  `From<{Single,Multi}ListenerDaemonError<Daemon::Error, Daemon::Error>>`
  (`905-935`).
- `DaemonEntry` (`daemon_emit.rs:975-983`): default `run_to_exit_code() ->
  ExitCode` = `ExitReport::new(PROCESS_NAME).from_result(DaemonCommand::<Self>::from_environment().run())`.

## The four properties: precise seam locations

### Property 1 — concurrency (request offloaded onto BoundedWorkers, fresh per-request engine over `Arc<Store>`)

**Where work runs synchronously today:** `GeneratedDaemonRuntime::handle_working_stream`
(`daemon_emit.rs:842-853`) runs the entire decode→execute→encode INLINE, and it is
invoked from the runtime trait's `handle_stream` (`:789` / `:811`).

**Why that is serial — the binding constraint from triad-runtime:**
`MultiListenerDaemon` (`triad-runtime/src/daemon.rs:96-104`) calls
`runtime.handle_stream(listener, stream)` ONCE PER ACCEPTED STREAM inside
`try_serve_next_stream` (`daemon.rs:368-380`), and `handle_stream` takes
`&mut self` (`MultiListenerRuntime`, `daemon.rs:40-44`; `DaemonRuntime`,
`daemon.rs:23`). The accept loop (`serve_streams` → `serve_next_stream` →
`try_serve_next_stream`) is single-threaded and blocks on each
`handle_stream` return. So a long `handle_working_input` blocks BOTH sockets.

**The reference fix (lojix daemon.rs:151-166):** `handle_stream` does NOT run the
request — it builds a `RequestWorker { store: self.store.clone(), codec }` and
calls `self.workers.dispatch(move || worker.serve(listener, stream))`, returning
`Ok(())` immediately. `BoundedWorkers::dispatch` (`triad-runtime/src/workers.rs:41-50`)
acquires a permit (backpressure at the cap) and runs on its own thread.

**The two constraints this imposes on the emitter design:**
1. The runtime must own a `BoundedWorkers` + an `Arc<Store>`-equivalent, NOT an
   owned `Daemon::Engine`. Today `GeneratedDaemonRuntime` holds `engine:
   Daemon::Engine` (`:830`) and `new(engine)` (`:835`). lojix instead holds
   `store: Arc<Store>` and the worker builds a fresh `SchemaRuntime::with_store`
   PER REQUEST (`lojix daemon.rs:220`). The `ComponentDaemon` trait would need a
   shared-state associated type (e.g. `type Shared: Clone + Send + Sync` /
   `Arc<Store>`) and a `build_engine(&shared) -> Engine` factory, replacing the
   one-shot `build_runtime`.
2. The dispatched closure is `FnOnce() + Send + 'static` (`workers.rs:42-43`), so
   the per-request engine and everything it captures must be `Send + 'static`.
   The emitted `handle_working_input` takes `&Engine`; under concurrency it must
   instead take an OWNED fresh engine (or `&mut`), built per request.

`should_continue()` default-true (`daemon.rs:32-34`) keeps the accept loop alive;
the offload model relies on it.

### Property 2 — two typed wire contracts → one Nexus root

**Where the meta tier is an escape hatch today:** `ComponentDaemon::handle_meta_stream`
(`daemon_emit.rs:343`) + its dispatch `ListenerTier::Meta =>
Daemon::handle_meta_stream(&self.engine, stream)` (`daemon_emit.rs:790`). It hands
the raw stream to the component and emits NO decode/encode for the meta tier.

**The reference shape (lojix):** ONE Nexus root `nexus::SignalInput` with two
variants (`lojix/triad-port/src/schema/nexus.rs:34-37`, declared in
`schema/nexus.schema:48`):
```
SignalInput  [(OrdinaryInput OrdinaryInput) (MetaInput MetaInput)]
SignalOutput [(OrdinaryOutput OrdinaryOutput) (MetaOutput MetaOutput)]
```
Both sockets decode their OWN contract then wrap into the shared root:
- ordinary (`lojix daemon.rs:189-199`): decode `signal_lojix…Input`, wrap
  `nexus::SignalInput::OrdinaryInput(input)`, run, unwrap `ordinary_reply`.
- owner (`lojix daemon.rs:201-210`): decode `meta_signal_lojix…Input`, wrap
  `nexus::SignalInput::MetaInput(input)`, run, unwrap `meta_reply`.

Both go through ONE `RequestWorker::execute` (`lojix daemon.rs:215-231`):
`engine.execute(nexus::NexusWork::SignalArrived(signal_input).with_origin_route(…))`,
then `.into_root()` → `nexus::NexusAction::ReplyToSignal(output)`. The reply is
re-split by tier and the WRONG-tier output is a typed error (`Error::UnexpectedFrame`,
`ordinary_reply`/`meta_reply`, `lojix daemon.rs:262-274`).

**Emitter implication:** the emitter must learn a SECOND contract module on the
meta tier (a `meta_contract_module` on `WorkingListenerTier` or a richer tier
type), emit a `decode_signal_frame` for the meta `Input`, wrap both into a
shared `SignalInput`-shaped enum, drive ONE engine `execute`, and re-split the
`SignalOutput` by tier. This replaces `handle_meta_stream` with a second typed
spine sharing the working spine's structure. The `Input`/`Output` import
(`daemon_emit.rs:293`) is currently single-module
(`crate::schema::#working::{Input, Output, …}`); it would gain the meta module's
roots and the shared `nexus::{SignalInput, SignalOutput, NexusWork, NexusAction}`.
Note `decode_signal_frame` already returns `(_route, input)` (`:847`) — the route
slot is discarded today but is exactly where origin/tier would attach.

### Property 3 — transport hardening (R1 max-frame + R2 read-timeout)

**Where the bound would apply today:** `WorkingTransport::read_frame`
(`daemon_emit.rs:574-578`) and `write_frame` (`580-586`) use
`LengthPrefixedCodec::default()`. `LengthPrefixedCodec::default()`
(`triad-runtime/src/frame.rs:73-77`) = `MaximumFrameLength::maximum_for_u32_prefix()`
= **`u32::MAX` (4 GiB)** — i.e. the codec will pre-allocate up to 4 GiB for a
hostile length prefix (`read_body`, `frame.rs:105-113`, `vec![0u8; length]`).
There is NO read timeout: `WorkingTransport` never calls
`stream.set_read_timeout`, so a connect-and-never-send wedges the (serial) accept
loop forever.

**The reference fix (lojix):**
- R1 max-frame: `LengthPrefixedCodec::new(MaximumFrameLength::new(8 * 1024 * 1024))`
  (`lojix daemon.rs:25,131`) — 8 MiB, far below 4 GiB.
- R2 read-timeout: `stream.set_read_timeout(Some(Duration::from_secs(10)))?`
  before each `read_body` (`lojix daemon.rs:190,202,30`).

**Emitter implication:** `WorkingTransport` must carry a configurable
`MaximumFrameLength` (passed into `LengthPrefixedCodec::new`, not `::default()`)
and call `set_read_timeout` on its stream before `read_frame`. The values are
new `NexusDaemonShape` fields (a `FrameBounds { max_body_bytes, read_timeout }`
positional record) read at emission and baked into the generated transport, OR
read at runtime from `DaemonConfiguration` (precedent: `meta_socket_mode()` is a
runtime-config read at `daemon_emit.rs:509-511`). Both primitives already exist
in triad-runtime (`MaximumFrameLength::new`, `frame.rs:32`; the codec accepts it
via `LengthPrefixedCodec::new`, `frame.rs:80-84`); `set_read_timeout` is std on
`UnixStream`. The `WorkingTransport::new(stream)` constructor (`:570`) would gain
the bounds parameter.

### Property 4 — fail-closed owner auth (ConnectionContext on owner socket; uid mismatch = REJECT, intent 9v7h)

**Where ConnectionContext is / isn't threaded today:**
- Working stream: `ConnectionContext::from_stream(&stream)` IS read
  (`daemon_emit.rs:843`) and passed to `handle_working_input`
  (`daemon_emit.rs:849`). But nothing REJECTS on it — the component "may" classify
  by it (trait doc, `daemon_emit.rs:406-411`).
- Meta stream: `handle_meta_stream(&self.engine, stream)` (`daemon_emit.rs:790`)
  receives NO `ConnectionContext` at all. The owner tier — the privileged one —
  is the one tier with NO peer-cred read. Its authority rests ENTIRELY on the
  socket file mode (the `MetaListenerTier::socket_mode` baked into the binder,
  `daemon_emit.rs:491-516`).

**The current (insufficient) guard in lojix:** `validate_owner_socket_mode`
(`lojix daemon.rs:99-104`) rejects a mode granting any "other" access, but there
is NO peer-credential check — exactly audit R3, which prior survey report 7 and
intent 9v7h call to close.

**The primitive that closes it:** `ConnectionContext::from_stream`
(`triad-runtime/src/process.rs:55-62`) reads the kernel-vouched `SO_PEERCRED`
uid/gid/pid via the safe rustix wrapper (`forbid(unsafe_code)` preserved).
`ConnectionContext::user_id()` (`process.rs:65`) is the uid to compare.

**The decided policy (intent 9v7h):** FAIL CLOSED — uid mismatch REJECTS the
connection. This contrasts with survey-7's open question ("reject vs tag a
non-owner OriginRoute"); 9v7h selects REJECT. So the emitted meta spine must:
read `ConnectionContext::from_stream`, compare `user_id()` against the configured
owner uid(s), and on mismatch CLOSE the stream (drop / typed listener error)
WITHOUT reaching the engine.

**The seam for the owner uid policy:**
1. Declaration: an `OwnerAuthority` field on `MetaListenerTier`
   (`daemon_emit.rs:103-116`) carrying the allowed uid(s) — OR a runtime read from
   `DaemonConfiguration` (a new `owner_user_id()` accessor alongside
   `meta_socket_mode()`, `process.rs:113-115`). Runtime-read is the better fit:
   the owner uid is deployment-specific, not a compile-time constant, and the
   `DaemonConfiguration` trait is the established home for such values.
2. Enforcement point: the emitted meta spine (replacing `handle_meta_stream`),
   BEFORE decode — mirror `handle_working_stream`'s
   `ConnectionContext::from_stream` (`:843`) but ADD the uid comparison and the
   reject branch.
3. The defense-in-depth layering: this is ON TOP OF the socket-mode guard, not
   instead of it (survey-7); the `MetaListenerTier::socket_mode` bind stays.

**Note on the engine-side route:** lojix today hardcodes `OriginRoute(0)`
(`lojix daemon.rs:222`) and the engine reads `input.origin_route()` in `decide`
(`schema_runtime.rs` `decide`, via `nexus::nexus::Nexus`). `OriginRoute(pub
Integer)` (`schema/nexus.rs:1114`) threads through
`apply_sema_write`/`observe_sema_read` (`schema/nexus.rs:1253-1254`). With
fail-closed REJECT at the transport edge, the engine-side route can stay a
trusted owner route once the connection is admitted — the auth decision is made
BEFORE the engine, not delegated to it. (The alternative tag-and-let-engine-refuse
model 9v7h rejected would instead mint the route from the uid.)

## Constraints the design MUST respect

1. **Token-first.** All emitted code is `quote!`/`ToTokens`; new sections are new
   data-bearing `ToTokens` nouns composed in `DaemonModuleBody::to_tokens`
   (`daemon_emit.rs:208-234`). No string building. Malformed tokens fail at
   `syn::parse2` in `DaemonModule::render` (`:182`).
2. **`handle_stream` is `&mut self` and called serially** by
   `MultiListenerDaemon::try_serve_next_stream` (`triad-runtime/daemon.rs:372`).
   Concurrency MUST come from offloading inside `handle_stream` (the
   `BoundedWorkers` model), NOT from changing the accept loop. The dispatched
   task is `FnOnce + Send + 'static` (`workers.rs:42-43`) — per-request engine
   must be `Send + 'static`.
3. **Single-argument rule.** The daemon binary takes exactly one rkyv
   `SignalFile` configuration (`DaemonCommand::configuration`,
   `daemon_emit.rs:455-463`); new options are NOTA schema fields on the
   configuration or positional `NexusDaemonShape` fields — NEVER flags.
4. **New shape fields are positional + typed** (NOTA-dialect discipline): a new
   `ConcurrencyShape` / `FrameBounds` / `OwnerAuthority` is a positional record,
   constructed in the component's `build.rs`. `NexusDaemonShape` builder pattern
   (`new` + `with_*`) is the precedent (`daemon_emit.rs:49-61`).
5. **Single vs multi branch is `is_multi_listener()`** (`daemon_emit.rs:75-77`,
   = `meta_tier.is_some()`). Every section reads it. A two-typed-contract meta
   tier and owner auth live on the multi-listener path only.
6. **Schema-emitted types ARE the nouns.** The shared `SignalInput`/`SignalOutput`
   Nexus root is schema-declared (`nexus.schema:48-49`) and emitted by the nexus
   target; the daemon emitter REFERENCES those nouns, it does not invent a parallel
   enum. The two-contract funnel reuses `nexus::{SignalInput, SignalOutput}`.
7. **Backward compatibility.** The current single-contract,
   serial, escape-hatch-meta daemon is in use by emitted components; new behavior
   must be OPT-IN via shape fields (default = today's behavior) so existing
   components re-emit byte-stable unless they declare the new options.
8. **`forbid(unsafe_code)` in triad-runtime stays** — peer-cred read uses the safe
   rustix wrapper already in `ConnectionContext::from_stream` (`process.rs:55-62`).
