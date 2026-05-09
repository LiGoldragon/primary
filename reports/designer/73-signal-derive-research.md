# 73 · `signal-derive` research — should a derive macro own channel boilerplate?

> **STATUS as of 2026-05-08:** Decision deferred —
> `signal_channel!` macro_rules! macro shipped instead
> (see `reports/designer/76`). signal-derive expansion
> defers per `skills/rust-discipline.md` §"When to lift to
> a shared crate" until 2-3 contract repos crystallize
> their patterns. Read for research context only.

Status: research-only report (no code changes). Per user
request 2026-05-09: *"if we create a signal derive macro on
that top-level enum, then probably a lot of the logic on
how these messages are exchanged can be in that derive
macro. Look at this from this angle. Tell me if I'm right.
Tell me if I'm wrong."*

Author: Claude (designer)

---

## 0 · TL;DR — the user is partly right

**Partly right** in instinct: there IS boilerplate per
channel, and a macro can eliminate some of it.

**Wrong on which axis the boilerplate lives on**: the
per-channel boilerplate isn't on the request enum — it's on
the *channel pairing* (request enum + reply enum + transport
struct). A `#[derive]` on a single enum is the wrong shape
for "establish a connection." Derives work per-type; channels
are inherently per-pair.

**Wrong on what derive can usefully emit**: the biggest pain
point isn't generating envelope/transport code — it's the
**rkyv bound chain** that consumers repeat in every function
signature touching `Frame<R, P>`. A small marker trait + blanket
impl (no derive macro needed) collapses this. The transport,
dispatcher, and network code don't fit the derive shape.

**Recommendation** (§7-§8): defer signal-derive expansion until
2-3 channels ship and the actual repetition is visible. When
the time comes, the right shape is likely:

1. A **marker trait** `FrameEnvelopable` with blanket impl —
   collapses the rkyv bound chain at function-signature sites.
   No derive macro needed; one trait + one impl in
   signal-core.
2. A **function-style macro** `signal_channel!` that takes
   (channel name, request enum, reply enum) and emits the
   `Frame` type alias + maybe a transport-struct skeleton.
   Function-style macro, not derive — because channels are
   per-pair.
3. **Maybe** `#[derive(Signal)]` on the request enum that
   emits convenience constructors per variant — saves ~3
   lines per variant; small win, may not be worth a macro.

**Network-passability** (the user's "back burner") doesn't
need a derive at all — `encode_length_prefixed` already
produces network-passable bytes. Cross-machine work is
handshake/auth/back-pressure/version-skew at the network
layer, separate from per-message generation. Tracked in
`primary-uea` (signal-network design).

---

## 1 · Current state — what's already in signal-core

`signal-core::Frame<RequestPayload, ReplyPayload>` is the
universal envelope (per `signal-core/src/frame.rs`):

```rust
pub struct Frame<RequestPayload, ReplyPayload> {
    auth: Option<AuthProof>,
    body: FrameBody<RequestPayload, ReplyPayload>,
}

pub enum FrameBody<RequestPayload, ReplyPayload> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request(Request<RequestPayload>),
    Reply(Reply<ReplyPayload>),
}
```

The Frame is **generic over the channel's payload types**.
Each channel instantiates it:

```rust
// signal-persona/src/lib.rs:19
pub type Frame = signal_core::Frame<PersonaRequest, PersonaReply>;
```

That's **one line per channel** — type alias.

### 1.1 · `Frame::encode_length_prefixed` already exists

Per `signal-core/src/frame.rs:62-78`:

```rust
impl<RequestPayload, ReplyPayload> Frame<RequestPayload, ReplyPayload>
where
    RequestPayload: Archive + for<'archive> RkyvSerialize<...>,
    ReplyPayload:   Archive + for<'archive> RkyvSerialize<...>,
{
    pub fn encode(&self) -> Result<Vec<u8>, FrameError> {
        rkyv::to_bytes::<rkyv::rancor::Error>(self)
            .map(|bytes| bytes.to_vec())
            .map_err(|_| FrameError::ArchiveValidation)
    }

    pub fn encode_length_prefixed(&self) -> Result<Vec<u8>, FrameError> {
        let archive = self.encode()?;
        let length = u32::try_from(archive.len()).map_err(|_| FrameError::LengthMismatch { ... })?;
        let mut framed = Vec::with_capacity(4 + archive.len());
        framed.extend_from_slice(&length.to_be_bytes());
        framed.extend_from_slice(&archive);
        Ok(framed)
    }
}
```

The wire-frame logic (rkyv archive + 4-byte big-endian
length prefix) **already lives in signal-core**. It's
generic; every channel inherits it via the type alias.

`decode_length_prefixed` is the symmetric inverse, also in
signal-core, also generic.

### 1.2 · Tests prove the round-trip works

`signal-persona/tests/frame.rs` has 4 tests that round-trip
real records (Message, Lock, Delivery, Mutation, Retraction)
through `Frame::encode_length_prefixed` →
`Frame::decode_length_prefixed`. They pass.

Example (lines 36-53):

```rust
#[test]
fn commit_reply_returns_store_minted_message_slot() {
    let reply = signal_persona::Reply::operation(
        PersonaReply::ok(CommitOutcome::Message(Slot::new(1024)))
    );
    let frame = Frame::new(FrameBody::Reply(reply));
    let bytes = frame.encode_length_prefixed().expect("frame encodes");
    let decoded = Frame::decode_length_prefixed(&bytes).expect("frame decodes");
    // assertions
}
```

### 1.3 · No persona daemon actually USES Frame yet

Operator/67 §5 (Wire-format Gap) confirms: persona-router,
persona-message, etc. **don't use Frame on their actual
sockets today**. The Frame primitive is built; the daemons
haven't adopted it yet. That's the load-bearing gap (per
designer/72 Phase 5 + `primary-2w6`).

Implication: **the per-channel boilerplate hasn't been
written yet, because no one's written a per-channel
production user**. We can't see "the boilerplate that hurts"
because nothing painful has been built.

---

## 2 · The user's proposal restated

> "If we create a signal derive macro on that top-level
> enum, then probably a lot of the logic on how these
> messages are exchanged can be in that derive macro."

The mental model:

```rust
#[derive(Signal)]
pub enum MessageRequest {
    Submit(SubmitMessage),
    Inbox(InboxQuery),
    Tail(TailRequest),
}

#[derive(Signal)]
pub enum MessageReply {
    SubmitOk(SubmitReceipt),
    SubmitFailed(FailureReason),
    InboxResult(InboxRecords),
    TailEvent(TailFrame),
}
```

…and the macro emits **the connection / exchange logic**
for the channel.

The instinct is to compress per-channel work. The question
is *what code can a derive on a single enum reasonably
emit?*

---

## 3 · What `#[derive]` macros do well — by analogy with rkyv

`#[derive(Archive)]` + `#[derive(Serialize)]` +
`#[derive(Deserialize)]` (from rkyv) emit, **per type**:

| Derive | Emits |
|---|---|
| `Archive` | An `Archived<T>` zero-copy view type with the same field layout but `#[repr(C)]` and atomically-readable types |
| `Serialize<S>` | `impl Serialize<S> for T where S: ...` — turns a `T` into bytes via `Serializer` |
| `Deserialize<T, D>` | `impl Deserialize<T, D> for Archived<T> where D: ...` — turns the archived view back into an owned `T` |

These are **per-type**. Each derive looks at the type's
fields and emits the required impl. No cross-type knowledge,
no transport, no connection. Pure code generation from the
type's own structure.

`nota-derive`'s macros (`NotaRecord`, `NotaEnum`, `NotaSum`,
`NotaTransparent`, `NotaTryTransparent`) follow the same
shape — per-type emission of `NotaEncode` + `NotaDecode`
impls.

**Derive macros work when:** the code-to-be-emitted depends
*only on the type's own fields/variants*.

**Derive macros don't work when:** the code-to-be-emitted
needs cross-type information (e.g. *both* the request enum
*and* the reply enum to define a Frame), or per-deployment
state (a connection, a path, a service name).

### 3.1 · The "boilerplate" today, line by line

If `signal-persona-message` is created tomorrow, the
boilerplate is:

```rust
// 1. Type alias for the channel's Frame (1 line)
pub type Frame = signal_core::Frame<MessageRequest, MessageReply>;

// 2. Request enum (domain-specific; can't be auto-generated)
pub enum MessageRequest {
    Submit(SubmitMessage),
    Inbox(InboxQuery),
    Tail(TailRequest),
}

// 3. Reply enum (domain-specific; can't be auto-generated)
pub enum MessageReply {
    SubmitOk(SubmitReceipt),
    SubmitFailed(FailureReason),
    InboxResult(InboxRecords),
    TailEvent(TailFrame),
}

// 4. Round-trip tests (5-10 lines per variant)
#[test]
fn submit_round_trips() {
    let frame = Frame::new(FrameBody::Request(Request::assert(
        MessageRequest::Submit(...)
    )));
    let bytes = frame.encode_length_prefixed().expect("encode");
    let decoded = Frame::decode_length_prefixed(&bytes).expect("decode");
    // assertion
}
// ... per variant ...
```

Per-channel boilerplate is **small**: one type alias + the
enums (which are domain work, not boilerplate) + round-trip
tests. The transport, dispatcher, and connection state
**aren't in the contract repo at all** — they live in the
consumer crates (persona-router, message-cli) which use the
contract.

### 3.2 · The actually-painful boilerplate — bound chains

Where the rkyv bounds bite is **at function signatures**
that take `Frame<R, P>`:

```rust
// In persona-router/src/handler.rs (hypothetical):
pub fn handle_frame<R, P>(frame: Frame<R, P>) -> Result<Reply, Error>
where
    R: Archive
        + for<'a> Serialize<Strategy<Serializer<...>, rancor::Error>>,
    R::Archived: Deserialize<R, HighDeserializer<rancor::Error>>
        + for<'b> CheckBytes<...>,
    P: Archive + for<'a> Serialize<...>,
    P::Archived: Deserialize<P, ...> + for<'b> CheckBytes<...>,
{ ... }
```

That's the real pain — and it appears **at every function
signature** that touches a generic Frame. Not per channel
(per channel it's a single type alias) but per consumer
function.

The fix isn't a derive macro. It's a **marker trait + blanket
impl**:

```rust
// signal-core/src/lib.rs (proposed)
pub trait FrameEnvelopable: Archive
    + for<'a> Serialize<Strategy<Serializer<AlignedVec, ArenaHandle<'a>, Share>, rancor::Error>>
where
    Self::Archived: Deserialize<Self, HighDeserializer<rancor::Error>>
        + for<'b> CheckBytes<Strategy<Validator<ArchiveValidator<'b>, SharedValidator>, rancor::Error>>,
{
}

impl<T> FrameEnvelopable for T where
    T: Archive
        + for<'a> Serialize<...>,
    T::Archived: Deserialize<T, ...> + for<'b> CheckBytes<...>,
{
}
```

Then function signatures collapse to:

```rust
pub fn handle_frame<R: FrameEnvelopable, P: FrameEnvelopable>(
    frame: Frame<R, P>,
) -> Result<Reply, Error> { ... }
```

**No derive macro needed.** Just a marker trait + blanket
impl.

This is the same pattern sema's `Table<K, V: Archive>`
should have used (audit 66 §1 didn't catch it) — collapse
the gnarly bounds into a marker.

---

## 4 · What a derive macro CAN'T do well for channels

### 4.1 · The Frame is paired

The `Frame<R, P>` type binds **two** types together. A
derive runs on one type at a time. To declare the channel's
Frame, you need both R and P at the same time:

```rust
pub type Frame = signal_core::Frame<MessageRequest, MessageReply>;
```

A derive on `MessageRequest` doesn't know `MessageReply`
exists. A derive on `MessageReply` doesn't know
`MessageRequest`. The only way a single derive could emit
the Frame alias is by attribute-passing:

```rust
#[derive(Signal)]
#[signal(reply = "MessageReply")]
pub enum MessageRequest { ... }
```

…which adds a brittle string-name dependency. If you rename
`MessageReply`, the attribute string drifts silently. You'd
also need the same on the reply side, with the same problem
in reverse.

**Better shape** (function-style macro, not derive):

```rust
signal_channel! {
    name: Message,
    request: MessageRequest,
    reply: MessageReply,
}
```

Function-style macros take *multiple* type names; they're
the natural shape for paired declarations.

### 4.2 · Transport doesn't fit

A derive on `MessageRequest` can't know:
- Where the daemon's UDS lives (`/run/persona/router.sock`?)
- How reconnection works
- How to handle timeouts
- Which authorization to attach
- Whether to encrypt (for cross-machine)

These are **deployment concerns**, not type concerns. They
belong in a transport struct that the consumer crate
declares — not in a derive on a contract crate's enum.

### 4.3 · Dispatcher doesn't fit either

A "dispatcher" pattern that handles each variant via a trait
method:

```rust
// hypothetical derive output
trait MessageRequestHandler {
    fn handle_submit(&mut self, msg: SubmitMessage) -> SubmitReceipt;
    fn handle_inbox(&mut self, query: InboxQuery) -> InboxRecords;
    fn handle_tail(&mut self, request: TailRequest) -> TailFrame;
}
```

This **could** be derived (one method per variant), but it
constrains the consumer to the trait's exact shape. A real
router actor wants async, error returns, ractor message-passing
— things the derive would have to bake in. Each consumer's
needs differ; derive lock-in is the wrong trade.

### 4.4 · Network code doesn't fit

The user's "back burner" — making frames network-passable.
The bytes from `encode_length_prefixed` are *already*
network-passable. What cross-machine adds is:
- Handshake across the wire (signal-core has HandshakeRequest/Reply but no transport)
- Auth across the wire (LocalOperatorProof is the local form; remote needs different)
- Back-pressure / flow control
- TLS / mTLS / QUIC selection
- Cross-machine version-skew detection

None of these are per-channel. They're **per-fabric** —
one set of decisions for the whole signaling family. They
belong in `signal-network` (`primary-uea` design task) or
`signal-core`'s extension, not in per-channel derives.

---

## 5 · What `signal-derive` could usefully emit (small wins)

If we wanted a derive on the request/reply enums tomorrow,
these would be the candidates:

### 5.1 · Convenience constructors per variant

Today, `signal-core::Request<Payload>` provides:

```rust
impl<Payload> Request<Payload> {
    pub fn assert(payload: Payload) -> Self { Self::operation(SemaVerb::Assert, payload) }
    pub fn subscribe(payload: Payload) -> Self { ... }
    // ... 12 verbs total ...
}
```

Per `signal-core/src/request.rs:36-83` — these are
hand-written. A derive on a per-channel request enum could
emit:

```rust
#[derive(Signal)]
pub enum MessageRequest {
    Submit(SubmitMessage),
    Inbox(InboxQuery),
}

// Derive emits:
impl MessageRequest {
    pub fn submit(payload: SubmitMessage) -> Self { Self::Submit(payload) }
    pub fn inbox(payload: InboxQuery) -> Self { Self::Inbox(payload) }
}
```

**Savings**: ~3 lines per variant. **Cost**: a procedural
macro to maintain.

For 5 variants × 5 channels = 75 lines total. The macro is
~50 lines. Break-even point is the third channel; afterwards
it's net positive but small.

### 5.2 · Marker trait impls

If we adopt `FrameEnvelopable` (§3.2), each channel's
request/reply enum needs the impl. Either:

- Auto via blanket impl (no derive needed; the blanket
  catches any type that satisfies the bounds)
- Or per-type via derive (more explicit but redundant)

Blanket impl is enough.

### 5.3 · Round-trip test scaffolds

A `#[derive(SignalRoundTrip)]` could emit one test per
variant. Cost: each test is ~5 lines hand-written; a
4-variant enum saves 20 lines. Worth a derive only if
applied to many enums.

Counterargument: examples-first round-trip discipline
(`skills/contract-repo.md`) wants the **canonical text
example** to be a hand-authored artifact for each record
kind. The test harness can be derived; the example data
can't be.

### 5.4 · `From<Variant>` impls

```rust
impl From<SubmitMessage> for MessageRequest {
    fn from(payload: SubmitMessage) -> Self { Self::Submit(payload) }
}
```

Trivially derivable per variant. `derive_more` does this
already; we could either use it or hand-emit. Small win.

---

## 6 · The pattern the user is reaching for — `signal_channel!` macro

The substantive boilerplate is around the **channel** as a
unit, not around the request enum alone. A function-style
macro fits:

```rust
// hypothetical signal_channel! macro

signal_channel! {
    name: Message,
    request: MessageRequest {
        Submit(SubmitMessage),
        Inbox(InboxQuery),
        Tail(TailRequest),
    },
    reply: MessageReply {
        SubmitOk(SubmitReceipt),
        SubmitFailed(FailureReason),
        InboxResult(InboxRecords),
        TailEvent(TailFrame),
    },
}
```

…emits:

```rust
pub enum MessageRequest { ... }      // the request enum
pub enum MessageReply { ... }        // the reply enum
pub type Frame = signal_core::Frame<MessageRequest, MessageReply>;
pub type FrameBody = signal_core::FrameBody<MessageRequest, MessageReply>;

impl MessageRequest {
    pub fn submit(payload: SubmitMessage) -> Self { Self::Submit(payload) }
    // ... per variant ...
}

impl MessageReply {
    pub fn submit_ok(receipt: SubmitReceipt) -> Self { Self::SubmitOk(receipt) }
    // ... per variant ...
}

// optionally: round-trip test scaffolds
```

This is **substantively** more boilerplate-eliminating than
`#[derive(Signal)]` because it knows about both sides of the
channel. The `Frame` type alias gets emitted once
automatically. The convenience constructors emit on both
sides.

Cost: a function-style macro is harder to write than a
derive (no `syn::DeriveInput` shortcut; you parse your own
DSL). But the surface is small.

**Verdict**: signal_channel! is the right shape if we want
macro-driven boilerplate elimination. NOT a derive.

---

## 7 · What signal-derive should and shouldn't try to do

| Candidate | Shape | Verdict |
|---|---|---|
| Per-variant convenience constructors | `#[derive(Signal)]` on request enum | Maybe; small win; defer |
| `From<Variant>` impls | `#[derive(SignalFrom)]` or use `derive_more` | Use existing tool |
| Marker trait impl for FrameEnvelopable | Blanket impl in signal-core | Yes — no derive needed |
| Frame type alias | `signal_channel!` function-style macro | Right shape; defer until 2-3 channels exist |
| Transport struct | Per-consumer crate; not in contract | NO — deployment concern |
| Dispatcher trait | Per-consumer crate; not in contract | NO — locks in consumer's shape |
| Round-trip test scaffolds | `signal_channel!` could optionally emit | Maybe; tests are small enough hand-written |
| Network/handshake/auth | `signal-network` (separate crate, future) | NO — per-fabric, not per-channel |

---

## 8 · Recommendation

**Don't add anything to signal-derive yet.** The current
`signal-derive` (268 LoC, `#[derive(Schema)]`) is a criome
remnant; leave it dormant per designer/72 §12.

**When the time comes** (after 2-3 channels ship per
designer/72's phased plan):

### 8.1 · Land the marker trait first

In `signal-core`, add a `FrameEnvelopable` marker trait with
blanket impl. **No derive macro.** This is the biggest pain
point and the simplest fix. ~30 lines in signal-core.

### 8.2 · Reassess after channel 3

After `signal-persona-message` + `signal-persona-store` +
`signal-persona-system` ship by hand:
- Read the three contract repos side by side.
- Identify what's *actually* repeated (not what's predicted to be).
- If the per-variant constructors + From impls + Frame alias
  add up to substantive boilerplate, write `signal_channel!`
  (function-style macro).
- If not, leave it hand-written.

### 8.3 · Defer the network back burner

Cross-machine signaling (`primary-uea`) is its own design
task. `encode_length_prefixed` already produces wire bytes;
what cross-machine needs is a *transport*, not a different
encoding. Wait for the network design to settle before
considering whether any of it benefits from a derive.

---

## 9 · A worked example — what 2 channels look like by hand vs with `signal_channel!`

### 9.1 · By hand (the today shape)

```rust
// signal-persona-message/src/lib.rs

use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};
use signal_persona::{Message, ...};

#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum MessageRequest {
    Submit(SubmitMessage),
    Inbox(InboxQuery),
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum MessageReply {
    SubmitOk(SubmitReceipt),
    InboxResult(InboxRecords),
}

pub type Frame = signal_core::Frame<MessageRequest, MessageReply>;
pub type FrameBody = signal_core::FrameBody<MessageRequest, MessageReply>;

impl MessageRequest {
    pub fn submit(payload: SubmitMessage) -> Self { Self::Submit(payload) }
    pub fn inbox(payload: InboxQuery) -> Self { Self::Inbox(payload) }
}

impl MessageReply {
    pub fn submit_ok(receipt: SubmitReceipt) -> Self { Self::SubmitOk(receipt) }
    pub fn inbox_result(records: InboxRecords) -> Self { Self::InboxResult(records) }
}
```

≈ 30 lines.

### 9.2 · With `signal_channel!` (proposed)

```rust
// signal-persona-message/src/lib.rs

use signal_core::signal_channel;

signal_channel! {
    name: Message,
    request: MessageRequest {
        Submit(SubmitMessage),
        Inbox(InboxQuery),
    },
    reply: MessageReply {
        SubmitOk(SubmitReceipt),
        InboxResult(InboxRecords),
    },
}
```

≈ 12 lines.

**Savings per channel**: 18 lines. Across 5 channels: 90 lines.

The macro itself: ~80-120 LoC. **Break-even at channel 5**.

If the macro also emits the round-trip tests (4 per channel
× 5 channels = 20 tests × 5 LoC = 100 LoC saved), the
break-even is at channel 3.

**Conclusion**: the macro pays back if we ship at least 3
channels. Per designer/72 we're shipping 5. Worth doing
*after* the first 2-3 are hand-written so the actual shape
of the macro is clear.

---

## 10 · What this means for `designer/72`

Designer/72 §12 says "defer signal-derive expansion until
2-3 channel contracts ship." This research **confirms that
recommendation**. The refinement:

- "signal-derive expansion" was the wrong framing — derive
  isn't the right shape for channel boilerplate.
- The right shape is `signal_channel!` (function-style macro)
  + a `FrameEnvelopable` marker trait in signal-core.
- Both can wait until 2-3 channels are hand-written.

Phase 3 of designer/72 lands `signal-persona-message` by
hand — that's the first channel. Phase 7+ lands the
remaining 4. After channel 3, reassess and write
`signal_channel!` if the boilerplate is real.

---

## 11 · Architectural-truth tests for any future macro

Per `skills/architectural-truth-tests.md`, when
`signal_channel!` lands (later), it should ship with:

| Test | Witness |
|---|---|
| `macro_emits_correct_frame_alias` | the `Frame` type alias resolves to `signal_core::Frame<R, P>` for the named R + P |
| `macro_constructors_match_variants` | `MessageRequest::submit` exists for every `Submit(_)` variant; same for reply |
| `macro_output_round_trips` | Apply macro to a small example; verify hand-written round-trip succeeds |
| `marker_trait_blanket_catches_payload` | `MessageRequest: FrameEnvelopable` resolves at compile time without explicit impl |

---

## 12 · See also

- `~/git/github.com/LiGoldragon/signal-core/src/frame.rs`
  — the Frame type, `encode_length_prefixed`,
  `decode_length_prefixed` (rkyv + 4-byte BE length)
- `~/git/github.com/LiGoldragon/signal-core/src/request.rs`
  — `Request<Payload>` + 12-verb convenience constructors
  (the pattern the per-channel macro could mirror)
- `~/git/github.com/LiGoldragon/signal-persona/src/lib.rs`
  — `pub type Frame = signal_core::Frame<PersonaRequest, PersonaReply>` (the type alias pattern)
- `~/git/github.com/LiGoldragon/signal-persona/tests/frame.rs`
  — 4 round-trip tests; the shape `signal_channel!` could
  emit
- `~/git/github.com/LiGoldragon/signal-derive/src/lib.rs`
  — the existing `#[derive(Schema)]` for criome's
  schema-introspection pattern; "role under review" status
- `~/git/github.com/LiGoldragon/nota-derive/src/lib.rs`
  — the analogous derive crate pattern (per-type emission)
- `~/primary/reports/designer/72-harmonized-implementation-plan.md`
  §12 — "signal-derive expansion — defer"; this report
  refines the why
- `~/primary/reports/designer/68-architecture-amalgamation-and-review-plan.md`
  §3.4 + §11 — primary-uea (signal-network) for the
  cross-machine work
- `~/primary/reports/operator/67-signal-actor-messaging-gap-audit.md`
  §5 (Wire-format Gap) — confirms no persona daemon uses
  Frame today
- `~/primary/skills/architectural-truth-tests.md` — the test
  pattern for the eventual macro

---

*End report. Recommendation: leave signal-derive alone for
now; reassess after Phase 3 of designer/72 ships 2-3
channels.*
