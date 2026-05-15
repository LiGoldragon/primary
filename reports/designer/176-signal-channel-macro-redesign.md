# 176 — `signal_channel!` macro redesign

*Designer spec, 2026-05-15. Compact current-state record after the
async-first correction (DA/60). Companion to `/177` (the typed-
request spec). Aligns with
`reports/designer-assistant/62-signal-redesign-implementation-brief.md`
§4 (the operator-facing macro section).*

**Retires when**: the proc-macro lands in `signal-core` and is
re-exported across contract crates; the substance migrates to
`signal-core/ARCHITECTURE.md`.

---

## 0 · TL;DR

`signal_channel!` is one declaration per channel. It emits the
typed payload enums, the per-variant `SignalVerb` witness, the
auto-generated kind enum, the channel type aliases, and the NOTA
codec impls. Nothing else. No `with intent` clause. No `intent
{ ... }` block. No `channel_policy { ... }` block (deferred — see
/177 §9 Q6). No correlation/header machinery. No `NoIntent`. No
multi-mode constructors per channel — the generic `RequestBuilder<P>`
in `signal-core` does that work.

The current `macro_rules!` engine in `signal-core/src/channel.rs`
stays for v1. After the intent/correlation/policy machinery is
gone, the remaining surface is well within `macro_rules!` reach.
Proc-macro extraction is on the table only when a future extension
earns it.

---

## 1 · Macro input grammar

```rust
signal_channel! {
    request <RequestName> {
        <Verb> <Variant>(<Payload>),
        ...
    }
    reply <ReplyName> {
        <Variant>(<Payload>),
        ...
    }
}
```

Both `request <RequestName> { ... }` and `reply <ReplyName> { ... }`
are required. No optional blocks in v1.

Verbs are exactly the six `SignalVerb` variants. Each request
variant lists its verb in the macro syntax; the macro emits the
`RequestPayload::signal_verb()` witness from this.

Worked example:

```rust
signal_channel! {
    request MindRequest {
        Assert SubmitThought(SubmitThought),
        Mutate StatusChange(StatusChange),
        Retract RoleRelease(RoleRelease),
        Match QueryThoughts(QueryThoughtsRequest),
        Subscribe SubscribeThoughts(SubscribeThoughtsRequest),
        Retract SubscriptionRetraction(MindSubscriptionToken),
        Validate ValidateProposal(ProposalCheck),
    }

    reply MindReply {
        Thought(ThoughtSummary),
        Status(ActivityAck),
        Released(RoleReleaseAck),
        ThoughtList(ThoughtList),
        SubscriptionOpened(SubscriptionOpenedAck),
        ValidationPassed(ValidationReceipt),
    }
}
```

---

## 2 · Macro emissions

For the worked example above, the macro emits:

```rust
// (1) Request payload enum with rkyv + NOTA derives.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum MindRequest {
    SubmitThought(SubmitThought),
    StatusChange(StatusChange),
    RoleRelease(RoleRelease),
    QueryThoughts(QueryThoughtsRequest),
    SubscribeThoughts(SubscribeThoughtsRequest),
    SubscriptionRetraction(MindSubscriptionToken),
    ValidateProposal(ProposalCheck),
}

// (2) Reply payload enum with the same derives.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum MindReply { /* variants */ }

// (3) RequestPayload impl with the verb-mapping match.
impl signal_core::RequestPayload for MindRequest {
    fn signal_verb(&self) -> signal_core::SignalVerb {
        match self {
            Self::SubmitThought(_)         => SignalVerb::Assert,
            Self::StatusChange(_)          => SignalVerb::Mutate,
            Self::RoleRelease(_)           => SignalVerb::Retract,
            Self::QueryThoughts(_)         => SignalVerb::Match,
            Self::SubscribeThoughts(_)     => SignalVerb::Subscribe,
            Self::SubscriptionRetraction(_) => SignalVerb::Retract,
            Self::ValidateProposal(_)      => SignalVerb::Validate,
        }
    }
}

// (4) Auto-generated kind enum (unit-only projection of the
// request variants). Retires hand-written enums like
// `MindOperationKind` in signal-persona-mind.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MindRequestKind {
    SubmitThought,
    StatusChange,
    RoleRelease,
    QueryThoughts,
    SubscribeThoughts,
    SubscriptionRetraction,
    ValidateProposal,
}

impl MindRequest {
    pub fn kind(&self) -> MindRequestKind { /* match */ }
}

// (5) Channel type aliases. Two-axis Frame; no Intent parameter.
pub type Frame        = signal_core::Frame<MindRequest, MindReply>;
pub type FrameBody    = signal_core::FrameBody<MindRequest, MindReply>;
pub type ChannelRequest = signal_core::Request<MindRequest>;
pub type ChannelReply   = signal_core::Reply<MindReply>;
pub type ChannelRequestBuilder = signal_core::RequestBuilder<MindRequest>;

// (6) Per-variant From<Payload> impls (request + reply) for
// ergonomic `.into()` at call sites.
impl From<SubmitThought> for MindRequest { /* ... */ }
// ... and so on for each variant.

// (7) NOTA codec impls for the payload enums (per-variant
// dispatch on the head identifier).
impl NotaEncode for MindRequest { /* match-and-encode */ }
impl NotaDecode for MindRequest { /* peek head, dispatch */ }
impl NotaEncode for MindReply { /* same */ }
impl NotaDecode for MindReply { /* same */ }

// (No channel-policy struct in v1 — universal rules only, per
// /177 §9 Q6. When a real channel needs stricter-than-universal
// rules, a typed channel-level policy lands then.)
```

---

## 3 · What the macro does NOT emit

Explicit non-emissions, to prevent regression as the macro evolves:

- No `Intent` type parameter on any emitted type.
- No `RequestHeader<Intent>` / `ReplyHeader<Intent>`.
- No `CorrelationId` field on requests or replies.
- No `with intent <T>` clause in the input grammar.
- No `intent <T> { ... }` block.
- No `NoIntent` substitution.
- No `<IntentName>Kind` projection (no intent enum exists).
- No `(Anonymous)` / `(Tracked ...)` / `(Named ...)` NOTA shapes.
- No `(Batch ...)` wrapper in NOTA.
- No `single_named` / `single_tracked` / `batch_tracked`
  per-channel constructors. Use the generic `RequestBuilder<P>` in
  `signal-core`.
- No exchange-id machinery. Exchange ids live at the
  `signal-core::FrameBody` level, not in the channel-specific
  types.
- No `channel_policy { ... }` block in v1 (deferred per /177 §9 Q6).
- No `Batch*` public names. The construction surface is named
  `RequestBuilder<P>` — see §6.

---

## 4 · Auto-generated `<RequestName>Kind` enum

The macro auto-generates a unit-only projection of the request
enum's variants. Retires hand-written enums like
`MindOperationKind` (currently in `signal-persona-mind/src/lib.rs`
around the lines that hand-list 24 request variant kinds).

```rust
// Auto-generated from the request enum's variant list:
pub enum MindRequestKind {
    SubmitThought, StatusChange, RoleRelease,
    QueryThoughts, SubscribeThoughts, SubscriptionRetraction,
    ValidateProposal,
}

impl MindRequest {
    /// Returns the unit-tag of this request variant. Useful for
    /// audit logs that don't need the full payload, dispatch tables,
    /// and metric labels.
    pub fn kind(&self) -> MindRequestKind { /* match */ }
}
```

The macro guarantees `MindRequestKind`'s variants stay in sync
with `MindRequest`'s variants — adding a new request variant
auto-adds its kind. The hand-written drift problem retires.

---

## 5 · Channel-policy block — not in v1

No `channel_policy { ... }` block in v1. The kernel ships with
universal rules only (verb/payload alignment + Subscribe position).
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

    // Default convenience methods — payload becomes a length-1
    // Request via these.
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
let request = MindRequest::SubmitThought(thought).into_request();

// Multi-op:
let request = signal_persona_mind::ChannelRequestBuilder::new()
    .with(MindRequest::RoleRelease(...))
    .with(MindRequest::RoleClaim(...))
    .build()?;
```

The per-channel `ChannelRequestBuilder` type alias from §2 emission
(5) specializes the generic builder to that channel's payload type.
All public names are `Request*`; "batch" survives nowhere as a
type/method name.

---

## 7 · Macro engine: `macro_rules!` for v1

The current `macro_rules!` engine in `signal-core/src/channel.rs`
stays. After the intent/correlation/policy machinery is gone, the
remaining surface (payload enums, verb-witness match,
auto-generated kind enum, type aliases, From impls, NOTA codec) is
well within `macro_rules!` reach — the `paste` crate handles
ident-concatenation for the kind enum.

Proc-macro extraction is on the table the day a real extension
needs it (custom per-variant attributes, span-aware error messages,
or a future `channel_policy { ... }` block). Don't add the crate
preemptively — DA/63 §F5 is right that a new crate without a v1
witness is a micro-component violation.

---

## 8 · See also

- `~/primary/reports/designer/177-typed-request-shape-and-execution-semantics.md`
  — the typed-request spec this macro serves.
- `~/primary/reports/designer-assistant/61-signal-redesign-current-spec.md`
  — the DA-side spec for the protocol shape.
- `~/primary/reports/designer-assistant/62-signal-redesign-implementation-brief.md`
  §4 — the DA-side operator brief for the macro.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  current `macro_rules!` form; replaced by proc-macro.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the upstream
  discipline this macro enforces.
