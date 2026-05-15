# 176 — `signal_channel!` proc-macro redesign

*Designer spec, 2026-05-15. Compact current-state record after the
DA/65 fold-in. Companion to `/177` (typed-request spec). Channel
declarations are now a typed relationship graph; the macro is a
small contract compiler.*

**Retires when**: the proc-macro lands in `signal-core/macros/` and
contract crates use it; the substance migrates to
`signal-core/ARCHITECTURE.md` and `signal-core/macros/ARCHITECTURE.md`.

---

## 0 · TL;DR

`signal_channel!` is one declaration per channel. It emits the
typed payload enums (request, reply, optionally event), the
per-variant `SignalVerb` witness, the auto-generated kind enums,
the frame aliases (exchange or streaming), the stream-relation
witnesses, and the NOTA codec for the payload layer.

The engine is **proc-macro**, not `macro_rules!`. The channel
declaration is a typed relationship graph (Subscribe → opens →
stream → token → event → close); cross-block name resolution and
span-pointed diagnostics are compiler work.

Two channel shapes:

- **exchange-only** — request + reply, no streams. Emits
  `ExchangeFrame<R, P>` aliases.
- **streaming** — adds `event` block + one or more `stream` blocks.
  Emits `StreamingFrame<R, P, E>` aliases.

No `Infallible` filler. No `(Assert ...)` wrapping at the channel
layer (that's `signal-core` per /177 §8.1). No `channel_policy`.
No auto-`From<Payload>` impls.

---

## 1 · Macro input grammar

### Exchange-only channel

```rust
signal_channel! {
    channel <ChannelName> {
        request <RequestName> {
            <Verb> <Variant>(<Payload>),
            ...
        }
        reply <ReplyName> {
            <Variant>(<Payload>),
            ...
        }
    }
}
```

### Streaming channel

```rust
signal_channel! {
    channel <ChannelName> {
        request <RequestName> {
            <Verb> <Variant>(<Payload>),
            ...
            Subscribe <Variant>(<Payload>) opens <StreamName>,
            ...
            Retract <Variant>(<TokenType>),
            ...
        }
        reply <ReplyName> {
            <Variant>(<Payload>),
            ...
        }
        event <EventName> {
            <Variant>(<Payload>) belongs <StreamName>,
            ...
        }
        stream <StreamName> {
            token <TokenType>;
            opened <OpenedReplyVariant>;
            event <EventPayloadVariant>;
            close <RetractRequestVariant>;
        }
        // one stream block per declared stream
    }
}
```

The `channel <ChannelName> { ... }` wrapper exists because the macro
emits names derived from the channel (`<ChannelName>Frame`,
`<ChannelName>StreamKind`, etc.).

Worked example — terminal channel with one stream:

```rust
signal_channel! {
    channel Terminal {
        request TerminalRequest {
            Assert TerminalConnection(TerminalConnection),
            Assert TerminalInput(TerminalInput),
            Mutate TerminalResize(TerminalResize),
            Retract TerminalDetachment(TerminalDetachment),
            Match TerminalCapture(TerminalCapture),
            Subscribe SubscribeTerminalWorkerLifecycle(
                SubscribeTerminalWorkerLifecycle
            ) opens TerminalWorkerLifecycleStream,
            Retract TerminalWorkerLifecycleRetraction(
                TerminalWorkerLifecycleToken
            ),
        }

        reply TerminalReply {
            TerminalReady(TerminalReady),
            TerminalInputAccepted(TerminalInputAccepted),
            TerminalResized(TerminalResized),
            TerminalCaptured(TerminalCaptured),
            TerminalDetached(TerminalDetached),
            TerminalRejected(TerminalRejected),
            TerminalWorkerLifecycleSnapshot(TerminalWorkerLifecycleSnapshot),
        }

        event TerminalEvent {
            TerminalWorkerLifecycleEvent(TerminalWorkerLifecycleEvent)
                belongs TerminalWorkerLifecycleStream,
        }

        stream TerminalWorkerLifecycleStream {
            token TerminalWorkerLifecycleToken;
            opened TerminalWorkerLifecycleSnapshot;
            event TerminalWorkerLifecycleEvent;
            close TerminalWorkerLifecycleRetraction;
        }
    }
}
```

Verbs are exactly the six `SignalVerb` variants.

---

## 2 · Macro emissions (streaming example)

```rust
// (1) Request payload enum with rkyv + NOTA derives.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum TerminalRequest {
    TerminalConnection(TerminalConnection),
    TerminalInput(TerminalInput),
    TerminalResize(TerminalResize),
    TerminalDetachment(TerminalDetachment),
    TerminalCapture(TerminalCapture),
    SubscribeTerminalWorkerLifecycle(SubscribeTerminalWorkerLifecycle),
    TerminalWorkerLifecycleRetraction(TerminalWorkerLifecycleToken),
}

// (2) Reply payload enum.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum TerminalReply { /* variants */ }

// (3) Event payload enum (only when stream blocks exist).
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum TerminalEvent {
    TerminalWorkerLifecycleEvent(TerminalWorkerLifecycleEvent),
}

// (4) RequestPayload impl with the verb-mapping match.
impl signal_core::RequestPayload for TerminalRequest {
    fn signal_verb(&self) -> SignalVerb {
        match self {
            Self::TerminalConnection(_)               => SignalVerb::Assert,
            Self::TerminalInput(_)                    => SignalVerb::Assert,
            Self::TerminalResize(_)                   => SignalVerb::Mutate,
            Self::TerminalDetachment(_)               => SignalVerb::Retract,
            Self::TerminalCapture(_)                  => SignalVerb::Match,
            Self::SubscribeTerminalWorkerLifecycle(_) => SignalVerb::Subscribe,
            Self::TerminalWorkerLifecycleRetraction(_) => SignalVerb::Retract,
        }
    }
}

// (5) Auto-generated kind enums (unit-only projections).
pub enum TerminalRequestKind { /* one variant per request variant */ }
pub enum TerminalReplyKind   { /* one variant per reply variant */ }
pub enum TerminalEventKind   { /* one variant per event variant */ }

impl TerminalRequest { pub fn kind(&self) -> TerminalRequestKind { /* match */ } }
impl TerminalReply   { pub fn kind(&self) -> TerminalReplyKind   { /* match */ } }
impl TerminalEvent   { pub fn kind(&self) -> TerminalEventKind   { /* match */ } }

// (6) Stream relation witnesses.
pub enum TerminalStreamKind {
    TerminalWorkerLifecycleStream,
}

impl TerminalRequest {
    /// Returns the stream this request variant opens, if any.
    /// Driven by `opens <StreamName>` annotations on Subscribe variants.
    pub fn opened_stream(&self) -> Option<TerminalStreamKind> {
        match self {
            Self::SubscribeTerminalWorkerLifecycle(_) =>
                Some(TerminalStreamKind::TerminalWorkerLifecycleStream),
            _ => None,
        }
    }

    /// Returns the stream this request variant closes, if any.
    /// Driven by the `close <RetractVariant>` field of stream blocks.
    pub fn closed_stream(&self) -> Option<TerminalStreamKind> {
        match self {
            Self::TerminalWorkerLifecycleRetraction(_) =>
                Some(TerminalStreamKind::TerminalWorkerLifecycleStream),
            _ => None,
        }
    }
}

impl TerminalEvent {
    pub fn stream_kind(&self) -> TerminalStreamKind {
        match self {
            Self::TerminalWorkerLifecycleEvent(_) =>
                TerminalStreamKind::TerminalWorkerLifecycleStream,
        }
    }
}

// (7) Frame aliases. Streaming channels use StreamingFrame.
pub type TerminalFrame =
    signal_core::StreamingFrame<TerminalRequest, TerminalReply, TerminalEvent>;
pub type TerminalFrameBody =
    signal_core::StreamingFrameBody<TerminalRequest, TerminalReply, TerminalEvent>;
pub type TerminalChannelRequest = signal_core::Request<TerminalRequest>;
pub type TerminalChannelReply   = signal_core::Reply<TerminalReply>;
pub type TerminalRequestBuilder = signal_core::RequestBuilder<TerminalRequest>;

// (8) NOTA codec impls for the payload enums (per-variant
// dispatch on the head identifier). Verb-wrapping ((Assert ...))
// and request-sequence brackets ([(Assert ...) (Match ...)]) live
// at the kernel layer in signal_core::Operation and
// signal_core::Request NOTA codecs (/177 §8.1).
impl NotaEncode for TerminalRequest { /* match-and-encode */ }
impl NotaDecode for TerminalRequest { /* peek head, dispatch */ }
impl NotaEncode for TerminalReply   { /* same */ }
impl NotaDecode for TerminalReply   { /* same */ }
impl NotaEncode for TerminalEvent   { /* same */ }
impl NotaDecode for TerminalEvent   { /* same */ }
```

Exchange-only channels emit the same shape minus event/stream
pieces and use `ExchangeFrame` / `ExchangeFrameBody` aliases:

```rust
pub type MessageFrame =
    signal_core::ExchangeFrame<MessageRequest, MessageReply>;
pub type MessageFrameBody =
    signal_core::ExchangeFrameBody<MessageRequest, MessageReply>;
```

---

## 3 · What the macro does NOT emit

Explicit non-emissions, to prevent regression:

- No `Intent` type parameter on any emitted type.
- No `RequestHeader<Intent>` / `ReplyHeader<Intent>`.
- No `CorrelationId` field on requests or replies.
- No `with intent <T>` clause / `intent <T> { ... }` block /
  `NoIntent`.
- No `(Anonymous)` / `(Tracked ...)` / `(Named ...)` /
  `(Batch ...)` NOTA shapes.
- No `single_named` / `single_tracked` / `batch_tracked`
  per-channel constructors. Use `signal_core::RequestBuilder<P>`.
- No exchange-id machinery in channel-specific types; lives in
  `signal-core` frame-layer types.
- No `channel_policy { ... }` block in v1 (deferred per /177 §9 Q6).
- No `Batch*` public names. `RequestBuilderError` carries
  `EmptyRequest`, never `EmptyBatch`.
- No blanket `From<Payload>` impls. Variant constructors are
  ergonomic; auto-From conflicts on duplicate payload types
  (per /177 §9 Q14). Channels may hand-write `From` for unambiguous
  payloads.
- No `(Assert ...)` wrapping at the channel codec layer. The
  channel's `NotaEncode/NotaDecode` covers only the payload enum.
  Operation/Request wrapping is owned by `signal_core::Operation`
  and `signal_core::Request` NOTA codecs (see /177 §8.1).
- No `Infallible` filler. Exchange-only channels use
  `ExchangeFrame`; streaming channels use `StreamingFrame`. Two
  distinct frame types.
- No runtime actors, sockets, storage, routing, or policy
  closures. The macro emits typed vocabulary and static facts
  about the relation; daemons own runtime behaviour.

---

## 4 · Compile-time diagnostics

The proc-macro validates the channel declaration as a typed
relationship graph. Span-pointed errors include:

- **unknown root verb** — `"Create" is not a SignalVerb; expected
  Assert, Mutate, Retract, Match, Subscribe, Validate`.
- **duplicate variant name** across request / reply / event blocks.
- **duplicate payload type** within a single block (would conflict
  with hand-written `From` impls; macro flags it pre-emptively).
- **duplicate NOTA record head** across variants — uniqueness is
  checked by the **NOTA head identifier** the codec dispatches on,
  not by the Rust type string. `domain_a::Status` and
  `domain_b::Status` both decode under the head `Status` and must
  be flagged as a collision even though their Rust paths differ
  (per DA/67 F3).
- **`opens <StreamName>` on a non-`Subscribe` request variant** —
  the `opens` annotation is meaningful only on Subscribe.
- **`belongs <StreamName>` on a variant whose stream block doesn't
  name it** — reverse cross-reference: a stream block's
  `event <Variant>` must point at a variant whose `belongs` points
  back to the same stream. The two halves of the relation must
  agree.
- **orphan stream block** — a `stream` block exists but no
  Subscribe variant opens it. Either delete the stream or add the
  opener.
- **event block without stream block** — events must belong to a
  declared stream.
- **`Subscribe ... opens <StreamName>`** where `<StreamName>` has
  no corresponding `stream` block.
- **stream block references missing variant** — `opened`, `event`,
  or `close` names a variant that doesn't exist in its block.
- **stream `close` variant's payload type ≠ stream `token` type**.
- **channel with at least one Subscribe but no `stream` block** —
  Subscribe semantics aren't declared.
- **channel with `event` block but no Subscribe variants** — event
  payloads exist but no operation creates a stream.
- **streaming-shaped declaration emitting `ExchangeFrame`** (or
  vice versa) — internal consistency.

The list above is the spec's required validation set. Each
diagnostic should land with a matching compile-fail test in
`signal-core/macros/tests/` so the validator regresses loudly
when a check is dropped.

`macro_rules!` can generate syntax but cannot comfortably resolve
cross-block name references with these error messages.

---

## 5 · Channel-policy block — not in v1

No `channel_policy { ... }` block in v1. The kernel ships with
universal rules only (verb/payload alignment + Subscribe suffix).
When a concrete channel needs stricter-than-universal rules, a
typed channel-level policy lands then. See `/177 §9 Q6`.

---

## 6 · Construction surface (lives in `signal-core`, not in the macro)

Channel-specific constructors are not macro-emitted. The generic
`RequestBuilder<P>` and `RequestPayload` default methods in
`signal-core` handle construction:

```rust
// signal-core/src/request.rs
pub trait RequestPayload: Sized {
    fn signal_verb(&self) -> SignalVerb;

    fn into_request(self) -> Request<Self> {
        Request {
            operations: NonEmpty::single(Operation {
                verb: self.signal_verb(),
                payload: self,
            }),
        }
    }
}

pub struct RequestBuilder<P> {
    ops: Vec<Operation<P>>,
}

impl<P> RequestBuilder<P>
where P: RequestPayload,
{
    pub fn new() -> Self { Self { ops: Vec::new() } }

    pub fn with(mut self, payload: P) -> Self {
        let verb = payload.signal_verb();
        self.ops.push(Operation { verb, payload });
        self
    }

    pub fn build(self) -> Result<Request<P>, RequestBuilderError> {
        NonEmpty::from_vec(self.ops)
            .map(|operations| Request { operations })
            .ok_or(RequestBuilderError::EmptyRequest)
    }
}

pub enum RequestBuilderError {
    EmptyRequest,
}
```

Call sites:

```rust
// Single-op:
let request = TerminalRequest::TerminalInput(input).into_request();

// Multi-op:
let request = TerminalRequestBuilder::new()
    .with(TerminalRequest::TerminalDetachment(detach))
    .with(TerminalRequest::TerminalConnection(connect))
    .build()?;
```

The per-channel `<Channel>RequestBuilder` type alias from §2
emission (7) specializes the generic builder.

---

## 7 · Macro engine: proc-macro

Crate shape:

```text
signal-core/macros/
├── Cargo.toml          # proc-macro = true
└── src/
    ├── lib.rs          # #[proc_macro] signal_channel
    ├── parse.rs        # syn parser for channel declaration
    ├── model.rs        # ChannelSpec, StreamSpec, VariantSpec
    ├── validate.rs     # semantic checks + diagnostics
    └── emit.rs         # quote! output
```

`signal-core` re-exports:

```rust
pub use signal_core_macros::signal_channel;
```

Dependencies: `syn`, `quote`, `proc-macro2`. Runtime code does not
depend on macro internals.

Implementation pipeline:

1. **`parse.rs`** — read the channel declaration into a
   `ChannelSpec` tree (request variants with verb tags, reply
   variants, event variants with `belongs` refs, stream blocks
   with cross-references).
2. **`validate.rs`** — semantic checks per §4 diagnostics. Each
   check returns `syn::Error::new_spanned(...)` pointing at the
   offending input.
3. **`emit.rs`** — `quote!` output per §2 emissions. Conditional
   on whether stream blocks exist (exchange-only vs streaming
   channel).

The migration lands as one operator pass: introduce
`signal-core/macros/` crate, replace the current `macro_rules!`
engine in `signal-core/src/channel.rs` with a re-export, sweep
contract crates' `signal_channel!` invocations to the new grammar
(channel wrapper, stream blocks, opens/belongs annotations).

---

## 8 · See also

- `~/primary/reports/designer/177-typed-request-shape-and-execution-semantics.md`
  — the typed-request spec this macro serves.
- `~/primary/reports/designer-assistant/61-signal-redesign-current-spec.md`
  — the DA-side spec for the protocol shape.
- `~/primary/reports/designer-assistant/62-signal-redesign-implementation-brief.md`
  §4 — the DA-side operator brief for the macro.
- `~/primary/reports/designer-assistant/64-signal-channel-macro-gap-research.md`
  — the gap research that surfaced the missing stream relation.
- `~/primary/reports/designer-assistant/65-signal-channel-proc-macro-shape.md`
  — the proc-macro shape sketch this spec adopts.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  current `macro_rules!` engine; replaced by proc-macro.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the upstream
  discipline this macro enforces.
