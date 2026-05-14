# 174 — `signal_channel!` redesign + two corrections to `/172`

*Designer follow-up, 2026-05-15. Accepts DA's critique that `/173`'s
"the macro grows but doesn't fundamentally rethink" was too
conservative. Folds DA's five points: single-op helpers obsolete,
four-axis Frame should be three-axis, optional intent already covered,
batch policy belongs in the macro, operation-kind enum should be
auto-generated. Plus surfaces two corrections to `/172` that DA's
critique implies: the Frame parameter count and the
`into_ops_checked` API shape. Spec'd as the macro shape going
forward.*

**Retires when**: the redesigned macro lands in `signal-core`; the
spec absorbs into `signal-core/ARCHITECTURE.md`.

---

## 0 · TL;DR

`/173` concluded the macro "grows along its current axis; no
fundamental rethink." DA's response: rethink it, but don't delete
it. The macro should remain the single declaration point for a
channel vocabulary, but the shape of what it declares has shifted
enough that "just add `with intent`" understates the change.

What this report settles:

1. **Two corrections to `/172`**:
   - `Frame` is **three-parameter**, not four: `Frame<RequestPayload,
     ReplyPayload, Intent>`. Request and reply share one intent
     vocabulary per channel.
   - `Request::into_ops_checked()` becomes a **two-method API**:
     `Request::validate(&self) -> Result<(), BatchVerbMismatch>` plus
     `Request::into_checked(self) -> Result<CheckedRequest, (BatchVerbMismatch,
     Self)>`. The error variant returns the unconsumed request so the
     receiver can build the rejection reply.

2. **The macro's redesigned concerns**:
   - `signal-core` owns: `Request`, `Reply`, `Op`, `NonEmpty`,
     headers, `BatchOutcome`, `BatchVerbMismatch`, validation logic,
     batch-codec, all generic primitives.
   - The macro owns: payload enums, intent enum (or `NoIntent`),
     frame aliases, verb witnesses, **auto-generated operation-kind
     enum**, **declarative batch-policy impl**, multi-mode constructors.
   - The receiver runtime owns: two-phase staged subscription open,
     storage transaction execution, per-receiver policy
     interpretation.

3. **Three new macro emissions** beyond `/173`'s list:
   - `pub enum <ReqName>Kind` auto-generated from the variant list
     (eliminates today's hand-written duplication, e.g.
     `MindOperationKind` in `signal-persona-mind/src/lib.rs:1633`).
   - `impl BatchPolicy for <ReqName>` emitted from an optional
     `batch_policy { ... }` block.
   - Multi-mode constructors: `ChannelRequest::single_anonymous`,
     `::single_tracked(correlation)`,
     `::single_named(intent, correlation)`, plus a builder pattern
     for multi-op batches.

4. **`macro_rules!` vs `proc-macro` is now closer to forced.** The
   new emissions push `macro_rules!` past the practical
   readability/error-message threshold. Recommendation: migrate to
   proc-macro alongside the redesign, in one operator pass.

The macro stays. Its declarative center stays. What changes is the
list of what it declares and the cleanness of the API it emits. DA's
phrasing — *"same declarative center, less ad hoc single-op
assumption, more generated contract truth"* — names the right shape.

---

## 1 · DA's findings, with concurrence

### 1.1 · Single-op helpers are obsolete ✓

Today's macro emits:

```rust
impl <ReqName> {
    pub fn into_signal_request(self) -> Request<Self> {
        Request::from_payload(self)
    }
}
```

This presumes single-op requests are the default shape. Under `/172`,
every `Request<P, I>` carries `NonEmpty<Op<P>>`; single-op is just a
length-1 batch. The helper should retire as such.

Replacement: three constructor helpers (anonymous, tracked, named)
plus a builder for multi-op. Per §4.3 below.

### 1.2 · Four-axis Frame should be three-axis ✓

`/172 §2` declared:

```rust
pub enum FrameBody<RequestPayload, RequestIntent, ReplyPayload, ReplyIntent> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request(Request<RequestPayload, RequestIntent>),
    Reply(Reply<ReplyPayload, ReplyIntent>),
}
```

Four parameters. But: a channel's request and reply share one intent
vocabulary. There's no use case where a `RoleHandoff` request gets
replied to with a different intent type. The reply echoes the
request's intent.

Corrected:

```rust
pub struct Frame<RequestPayload, ReplyPayload, Intent> {
    body: FrameBody<RequestPayload, ReplyPayload, Intent>,
}

pub enum FrameBody<RequestPayload, ReplyPayload, Intent> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request(Request<RequestPayload, Intent>),
    Reply(Reply<ReplyPayload, Intent>),
}
```

Three parameters. The macro emits:

```rust
pub type Frame = signal_core::Frame<<ReqName>, <RepName>, <IntentName>>;
pub type FrameBody = signal_core::FrameBody<<ReqName>, <RepName>, <IntentName>>;
```

This is a real correction to `/172`. The four-parameter Frame was
over-general. **`/172 §2` should be updated to three parameters.**

### 1.3 · Optional intent surface ✓ (already covered in `/173`)

`/173 §3.1 / §3.2 / §3.3` already addressed this. The macro takes
optional `with intent <T>` plus optional trailing `intent <T> { ... }`
block; `NoIntent` substitutes when absent. No additional change.

### 1.4 · Batch policy belongs near the channel declaration ✓

`/172 §7 Q1` left per-receiver batch-policy syntax open. DA argues:
if the policy is contract-level (and it should be — different
channels have genuinely different policies), it belongs in the macro.

The macro grows an optional `batch_policy { ... }` block:

```rust
signal_channel! {
    request <Name> with intent <Intent> { ... }
    reply <Name> { ... }
    intent <Intent> { ... }
    batch_policy {
        max_ops: 32,
        allow_mixed_read_write: true,
        forbid_subscribe: false,
        forbid_validate: false,
    }
}
```

The macro emits a `BatchPolicy` impl that the receiver runtime
consults during `Request::validate()`. Spec'd in §4.2.

### 1.5 · Operation-kind enum should be generated, not hand-written ✓

Real duplication. Today's `signal-persona-mind` declares:

```rust
// signal-persona-mind/src/lib.rs:1633
pub enum MindOperationKind {
    SubmitThought,
    SubmitRelation,
    QueryThoughts,
    // ... 24 variants, hand-written
}

// signal-persona-mind/src/lib.rs:1802
impl MindRequest {
    pub fn operation_kind(&self) -> MindOperationKind {
        match self {
            Self::SubmitThought(_) => MindOperationKind::SubmitThought,
            // ... 24 matches, hand-written
        }
    }
}
```

The macro sees every variant; it can emit both. Saves ~50 lines per
contract. Spec'd in §4.1.

---

## 2 · Two corrections to `/172`

### 2.1 · `Frame` is three-parameter

As §1.2 above. The reply echoes the request's intent vocabulary
within a single channel; the four-parameter generality has no use
case in scope.

This affects:
- `/172 §2`'s `FrameBody<RequestPayload, RequestIntent, ReplyPayload, ReplyIntent>` → `FrameBody<RequestPayload, ReplyPayload, Intent>`.
- `/172 §3`'s sample `pub type MindFrame = ...` → three parameters.
- `/172 §8.3`'s "ReplyHeader echoes the request's header shape" — still
  true; both use the same `Intent` type by construction.

### 2.2 · `into_ops_checked` API redesigned

`/172 §2`'s API consumed the request and returned only the mismatch
on failure:

```rust
pub fn into_ops_checked(self) -> Result<CheckedRequest<P, I>, BatchVerbMismatch>;
```

DA's point: on failure, the receiver needs the request's header,
op count, and per-op verbs to build the batch rejection reply. With
the request consumed and only a `BatchVerbMismatch` returned, the
receiver has lost the context it needs.

Two acceptable redesigns:

#### Option A: Borrow-based two-method API

```rust
impl<P, I> Request<P, I>
where
    P: RequestPayload,
{
    /// Validate without consuming. Returns the position of the first
    /// violation if any. The caller retains the request for whatever
    /// follows (build rejection reply, log, retry).
    pub fn validate(&self) -> Result<(), BatchVerbMismatch>;

    /// Convert to a CheckedRequest, assuming validate() was called.
    /// If you want both at once, use into_checked() (validates inside,
    /// returns the request back on failure).
    pub fn into_checked(self) -> Result<CheckedRequest<P, I>, (BatchVerbMismatch, Self)>;
}
```

The receiver code becomes:

```rust
let request = decode_frame()?;
match request.into_checked() {
    Ok(checked) => execute(checked).await,
    Err((mismatch, rejected)) => {
        // rejected still owns the request; build the reply
        let reply = build_rejection(rejected, mismatch);
        send_reply(reply).await
    }
}
```

#### Option B: Error carries context (alternative)

```rust
pub fn into_ops_checked(self) -> Result<CheckedRequest<P, I>, BatchVerbMismatchContext<I>>;

pub struct BatchVerbMismatchContext<I> {
    pub mismatch: BatchVerbMismatch,
    pub rejected_header: ReplyHeader<I>,
    pub op_count: usize,
    pub op_verbs: Vec<SignalVerb>,
}
```

The error carries pre-extracted context.

**Recommendation: Option A** (borrow-based two-method). Reasons:

- Matches the Rust standard idiom for "validation that consumes on
  success but preserves on failure" (e.g., `String::from_utf8`
  returns the original bytes in the error).
- Composes more cleanly: callers that don't need the full request
  back can use `request.validate()?` and then own `request` for any
  follow-up.
- The `(BatchVerbMismatch, Self)` error tuple on `into_checked` is
  ergonomic — pattern-match destructures cleanly.

This affects:
- `/172 §2`'s `Request::into_ops_checked` impl → `Request::validate` +
  `Request::into_checked`.
- `/172 §1.7`'s description of the verb-validation API → both
  methods documented.

---

## 3 · The macro's redesigned concerns

A three-way split between signal-core, the macro, and the receiver
runtime. Each owns a well-defined slice.

### 3.1 · `signal-core` owns

- The frame/wire primitives: `Frame`, `FrameBody`, `Request`, `Reply`.
- The collection / position invariants: `NonEmpty<T>`, `Op<Payload>`.
- The headers: `RequestHeader<Intent>`, `ReplyHeader<Intent>`.
- The reply machinery: `BatchOutcome`, `SubReply<R>`, `SubStatus`.
- The validation logic: `Request::validate`, `Request::into_checked`,
  `BatchVerbMismatch`, `CheckedRequest`.
- The failure-reason taxonomies: `BatchFailureReason` (with
  `SubscribeOutOfOrder` defined), `SubFailureReason`.
- The default policy enforcement (Subscribe-must-be-last) in
  `Request::validate`.
- `NoIntent` (uninhabited enum) for channels without named intents.
- The NOTA codec for `Request<P, I>` and `Reply<P, I>` — the batch
  grammar `[(intent X) (correlation Y) (op) (op) ...]` plus the
  bare `(op)` single-op form.
- The `RequestPayload` trait with `signal_verb()` and default
  `is_subscribe()`.
- The `BatchPolicy` trait that channels can implement.
- Convenience constructors: `Request::single_anonymous(payload)`,
  `::single_tracked(payload, correlation)`,
  `::single_named(payload, intent, correlation)`.

### 3.2 · The macro owns

- The channel-specific payload enums (request, reply).
- The channel-specific intent enum (or `NoIntent` substitution).
- The channel-specific operation-kind enum (auto-generated).
- The verb witnesses: `impl RequestPayload for <ReqName>`.
- The per-channel `Frame` / `FrameBody` / `ChannelRequest` /
  `ChannelReply` type aliases.
- The per-channel `BatchPolicy` impl (emitted from the optional
  `batch_policy { ... }` block).
- The per-channel ergonomic constructors that wrap signal-core's
  `Request::single_*` helpers.
- The per-channel `From<Payload>` impls for each variant.
- The NOTA codec impls for the request/reply payload enums and the
  intent enum (the per-variant text codec; not the batch grammar).

### 3.3 · The receiver runtime owns

- The two-phase staged subscription open (per `/172 §4.1`).
- The actual storage transaction execution — strict-ordered with
  RYOW, batch commit/rollback semantics.
- Per-receiver runtime interpretation of policy (the receiver decides
  whether to enforce stricter policy than `BatchPolicy` declares).
- The `Reply` construction — populating `SubReply` per op,
  `BatchOutcome::Aborted { failed_at, reason }`.

This split is the cleanest version of the declarative center DA
named. The macro doesn't pretend to enforce anything; it just
declares. signal-core provides primitives; the runtime executes.

---

## 4 · New macro emissions

### 4.1 · Auto-generated operation-kind enum

Today's hand-written duplication in `signal-persona-mind` becomes
macro-emitted. Given the request block:

```rust
request MindRequest with intent MindBatchIntent {
    Assert SubmitThought(SubmitThought),
    Mutate StatusChange(StatusChange),
    Retract RoleRelease(RoleRelease),
    // ...
}
```

The macro auto-emits:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MindRequestKind {
    SubmitThought,
    StatusChange,
    RoleRelease,
    // one variant per request variant; unit-only (no payloads)
}

impl MindRequest {
    pub fn kind(&self) -> MindRequestKind {
        match self {
            Self::SubmitThought(_) => MindRequestKind::SubmitThought,
            Self::StatusChange(_) => MindRequestKind::StatusChange,
            Self::RoleRelease(_) => MindRequestKind::RoleRelease,
            // ...
        }
    }
}
```

This replaces today's hand-written `MindOperationKind` enum and the
~24-line match in `operation_kind()`. The macro guarantees the kinds
stay in sync with the variants.

Naming: `<ReqName>Kind` (matching the request enum's name) rather
than `MindOperationKind` (which was a hand-chosen name).
Re-exporting under the old name for backward compat is one approach;
or contracts can rename callers to use the macro-emitted name.

### 4.2 · Batch policy impl from `batch_policy` block

The macro accepts an optional trailing block:

```rust
batch_policy {
    max_ops: 32,                                       // hard cap on Vec length
    allow_mixed_read_write: true,                      // default
    forbid_subscribe: false,                           // default (Subscribe-last applies)
    forbid_validate: false,
    forbid_mid_batch_subscribe: true,                  // already in signal-core default
    custom_check: |request| -> Result<(), CustomCheckFailure> { ... },  // optional extension
}
```

The macro emits:

```rust
impl signal_core::BatchPolicy for MindRequest {
    fn max_ops(&self) -> usize { 32 }
    fn allow_mixed_read_write(&self) -> bool { true }
    fn forbid_subscribe(&self) -> bool { false }
    fn forbid_validate(&self) -> bool { false }
    // ...

    /// Custom check, runs after the built-in checks.
    fn custom_check(request: &Request<MindRequest, MindBatchIntent>) -> Result<(), CustomCheckFailure> {
        // body from the macro block
    }
}
```

The signal-core `Request::validate(&self)` consults the channel's
`BatchPolicy` for the per-channel rules; if a request violates them,
validation fails with `BatchVerbMismatch::PolicyViolation` (and we
gain a sub-reason naming the specific rule).

If `batch_policy { ... }` is absent, the macro emits a default impl
that enforces only signal-core's universal rules (Subscribe must be
last, non-empty batch, verb/payload alignment).

### 4.3 · Multi-mode constructors

Replace today's `into_signal_request` single-op helper with a
constructor surface that matches the new `RequestHeader<Intent>`
variants:

```rust
impl ChannelRequest {
    /// Build an anonymous single-op request.
    pub fn single(payload: MindRequest) -> Self {
        Request::single_anonymous(payload)
    }

    /// Build a tracked single-op request (carries correlation; no intent).
    pub fn tracked(payload: MindRequest, correlation: CorrelationId) -> Self {
        Request::single_tracked(payload, correlation)
    }

    /// Build a named single-op request (carries intent and correlation).
    pub fn named(payload: MindRequest, intent: MindBatchIntent, correlation: CorrelationId) -> Self {
        Request::single_named(payload, intent, correlation)
    }

    /// Build a multi-op batch via a builder pattern. Initially named
    /// (the multi-op case typically wants audit metadata).
    pub fn batch(intent: MindBatchIntent, correlation: CorrelationId) -> BatchBuilder {
        BatchBuilder::new_named(intent, correlation)
    }

    /// Build a tracked multi-op batch (multi-op without named intent).
    pub fn batch_tracked(correlation: CorrelationId) -> BatchBuilder {
        BatchBuilder::new_tracked(correlation)
    }
}
```

Where `BatchBuilder` is a generic signal-core type:

```rust
pub struct BatchBuilder<P, I> {
    header: RequestHeader<I>,
    ops: Vec<Op<P>>,
}

impl<P, I> BatchBuilder<P, I>
where
    P: RequestPayload,
{
    pub fn new_named(intent: I, correlation: CorrelationId) -> Self;
    pub fn new_tracked(correlation: CorrelationId) -> Self;
    pub fn with(mut self, payload: P) -> Self {
        let verb = payload.signal_verb();
        self.ops.push(Op { verb, payload });
        self
    }
    pub fn build(self) -> Result<Request<P, I>, BatchBuilderError>;  // checks NonEmpty
}
```

Call sites become readable:

```rust
ChannelRequest::batch(MindBatchIntent::RoleHandoff, cor_id)
    .with(MindRequest::RoleRelease(RoleRelease { role: Designer }))
    .with(MindRequest::RoleClaim(RoleClaim { role: Poet, ... }))
    .build()?
```

vs the manual:

```rust
Request {
    header: RequestHeader::Named { intent: MindBatchIntent::RoleHandoff, correlation: cor_id },
    ops: NonEmpty::from_vec(vec![
        Op { verb: SignalVerb::Retract, payload: MindRequest::RoleRelease(...) },
        Op { verb: SignalVerb::Assert,  payload: MindRequest::RoleClaim(...) },
    ])?,
}
```

The builder pattern is significantly cleaner. The macro emits the
per-channel `ChannelRequest::*` helpers; the builder itself lives in
signal-core.

---

## 5 · The complete macro shape

### 5.1 · Grammar (the full input form)

```rust
signal_channel! {
    request <ReqName>
        [with intent <IntentName>]
    {
        <Verb> <Variant> ( <Payload> ),
        ...
    }
    reply <RepName> {
        <Variant> ( <Payload> ),
        ...
    }
    [intent <IntentName> {
        <Variant> [( <Payload> )],
        ...
    }]
    [batch_policy {
        <field>: <value>,
        ...
    }]
}
```

Both `[with intent <IntentName>]` and the trailing `intent ... { }`
block are optional. `[batch_policy { ... }]` is optional. The macro
substitutes `NoIntent` and default policy when absent.

### 5.2 · Emissions (the full output form, abbreviated)

```rust
// 1. The request payload enum (existing, unchanged shape)
pub enum <ReqName> { ... }

// 2. The reply payload enum (existing, unchanged shape)
pub enum <RepName> { ... }

// 3. The intent enum (new, or NoIntent substitution)
pub enum <IntentName> { ... }    // or: pub use signal_core::NoIntent as <IntentName>

// 4. Auto-generated operation-kind enum (new)
pub enum <ReqName>Kind {
    <Variant>,    // one per request variant, unit-only
    ...
}

// 5. Channel type aliases (updated to 3-parameter Frame)
pub type Frame = signal_core::Frame<<ReqName>, <RepName>, <IntentName>>;
pub type FrameBody = signal_core::FrameBody<<ReqName>, <RepName>, <IntentName>>;
pub type ChannelRequest = signal_core::Request<<ReqName>, <IntentName>>;
pub type ChannelReply = signal_core::Reply<<RepName>, <IntentName>>;

// 6. RequestPayload impl (existing, unchanged)
impl signal_core::RequestPayload for <ReqName> {
    fn signal_verb(&self) -> SignalVerb { match self { ... } }
}

// 7. Kind helper (new)
impl <ReqName> {
    pub fn kind(&self) -> <ReqName>Kind { match self { ... } }
}

// 8. Multi-mode constructors (new, replaces into_signal_request)
impl ChannelRequest {
    pub fn single(payload: <ReqName>) -> Self;
    pub fn tracked(payload: <ReqName>, correlation: CorrelationId) -> Self;
    pub fn named(payload: <ReqName>, intent: <IntentName>, correlation: CorrelationId) -> Self;
    pub fn batch(intent: <IntentName>, correlation: CorrelationId) -> BatchBuilder<<ReqName>, <IntentName>>;
    pub fn batch_tracked(correlation: CorrelationId) -> BatchBuilder<<ReqName>, <IntentName>>;
}

// 9. BatchPolicy impl (new, from batch_policy block or default)
impl signal_core::BatchPolicy for <ReqName> {
    fn max_ops(&self) -> usize { ... }
    // ...
}

// 10. From<Variant> impls per request variant (existing, unchanged)
impl From<<Payload>> for <ReqName> { ... }

// 11. NotaEncode/Decode for <ReqName> (existing, unchanged — per-variant codec dispatch)
impl NotaEncode for <ReqName> { ... }
impl NotaDecode for <ReqName> { ... }

// 12. From<Variant> impls per reply variant (existing, unchanged)
impl From<<Payload>> for <RepName> { ... }

// 13. NotaEncode/Decode for <RepName> (existing, unchanged)
impl NotaEncode for <RepName> { ... }
impl NotaDecode for <RepName> { ... }

// 14. NotaEncode/Decode for <IntentName> (new, only if intent block declared
//     and not auto-NoIntent)
impl NotaEncode for <IntentName> { ... }
impl NotaDecode for <IntentName> { ... }

// 15. NotaEncode/Decode for <ReqName>Kind (new, useful for audit/log surfaces)
impl NotaEncode for <ReqName>Kind { ... }
impl NotaDecode for <ReqName>Kind { ... }
```

Roughly **15 emission categories** under the new shape, up from
today's **12**. The new ones (3, 4, 7, 8, 9, 14, 15) are tightly
defined; each has a specific purpose that's been load-bearing in at
least one workspace contract.

---

## 6 · `macro_rules!` vs `proc-macro` — now nearly forced

`/173 §6` evaluated this as a preference. After §4–§5 above, the
choice is sharper.

### macro_rules! cost under the new shape

Implementing §5's emissions in `macro_rules!` requires:

- Two top-level arms (with-intent / without-intent) plus matching
  helper macros for the optional `batch_policy` block. Each arm
  duplicates most of the emission body.
- The auto-generated `<ReqName>Kind` enum requires re-iterating the
  variants twice (the enum body + the impl body); `macro_rules!`
  handles this with `$( ... )*` but each variant template gets
  long.
- The `batch_policy { ... }` block parser in `macro_rules!` requires
  matching named fields with `$field:ident: $value:literal` shapes
  — workable but unwieldy.
- Custom check expressions inside `batch_policy` (`custom_check: |req|
  -> Result<...> { ... }`) — `macro_rules!` can capture an expression
  block, but the syntax for "optional closure with optional body"
  gets gnarly.
- Error messages stay opaque.

Realistic line count for the `macro_rules!` form of §5: ~400–500
lines, with extensive duplication across the with/without-intent arms.

### proc-macro cost

- One-time crate split: `signal-core-macros` (proc-macro = true) +
  `signal-core` re-exports.
- `syn`-based parser handles the optional blocks naturally.
- Emission via `quote!` is direct Rust generation; conditional
  emission is a normal `if let`.
- Custom error messages via `syn::Error::new_spanned`; the compiler
  points at the offending input with a descriptive message.
- ~600–800 lines of proc-macro Rust (more code, but no duplication,
  with maintainable structure).

### Verdict

The cost balance has shifted. With §4–§5's new emissions, the
`macro_rules!` form is on the wrong side of the ergonomic line.

**Recommendation: proc-macro, alongside the redesign.** One operator
pass:

1. Add `signal-core-macros` proc-macro crate.
2. Rewrite the emissions in `quote!` blocks.
3. Cut over `signal-core` to re-export from the new crate.
4. Every consuming contract continues to use `signal_channel!` —
   their invocation sites don't change.

The redesigned macro lands as one cohesive piece; future extensions
(per-variant attributes, NOTA-shaped channel files, BatchValidator
derives) are then incremental rather than each requiring another
`macro_rules!` puzzle.

---

## 7 · Migration impact on `/172`

The corrections in §2 (three-parameter Frame, validate/into_checked
API split) are real changes to `/172`'s spec, not just additions.
They land alongside this report or in a companion `/172` revision.

The specific edits to `/172`:

- §2 `FrameBody<RequestPayload, RequestIntent, ReplyPayload, ReplyIntent>` →
  `FrameBody<RequestPayload, ReplyPayload, Intent>`.
- §2 `Request::into_ops_checked` → `Request::validate` +
  `Request::into_checked`. The `BatchVerbMismatch` enum stays; the
  error tuple `(BatchVerbMismatch, Self)` on `into_checked` is new.
- §1.7's description of the verb-validation API updates to two
  methods.
- §8.3's "ReplyHeader echoes the request's header" — still true; both
  use the same `Intent` type by the new generic shape.

These are corrections, not extensions. `/172` is the spec of record
and should be updated in present-tense.

---

## 8 · Open questions

The questions in `/172 §7` plus DA's new ones:

### Q1 — Operation-kind enum naming

`<ReqName>Kind` is the macro's default. But today's contracts use
`<ReqName>OperationKind` (e.g., `MindOperationKind`, not
`MindRequestKind`). Either:
- (a) Macro emits `<ReqName>Kind`; contracts rename internal callers.
- (b) Macro emits `<ReqName>OperationKind` for backward fit.
- (c) Configurable macro parameter for the suffix.

Lean (a) — `<ReqName>Kind` is shorter and matches the request enum's
natural namespace. The rename is mechanical and one-time.

### Q2 — `BatchPolicy` field list

The `batch_policy { ... }` block needs a closed field list. My §4.2
draft has 5 fields plus `custom_check`. The right set depends on
what receivers actually need. Likely candidates:

- `max_ops: usize`
- `allow_mixed_read_write: bool`
- `forbid_subscribe: bool`
- `forbid_validate: bool`
- `forbid_mid_batch_subscribe: bool` (default true, hard rule)
- `custom_check: |request| Result<(), CustomCheckFailure>`

Settle this when the first per-receiver policy lands in a real
contract.

### Q3 — Builder pattern: panic-or-error on `build()`?

`BatchBuilder::build() -> Result<Request, BatchBuilderError>` returns
error if the ops vec is empty (violating `NonEmpty`). Alternative:
panic on empty (since the agent constructing the batch should know
not to call `build()` without `.with(...)`).

Lean Result (no panics in the wire-construction path; callers can
handle `EmptyBatch` deliberately if it's somehow reached).

### Q4 — Proc-macro migration timing

(`/173 §9 Q1`.) After this redesign, the answer is clearer: migrate
now, alongside the redesign, in one operator pass. The single
migration to proc-macro lets every subsequent extension be additive.

### Q5 — Should `<ReqName>Kind` carry intent-tagged variants too?

Today's hand-written `MindOperationKind` is unit-only. But `/172`
allows intent variants to carry payloads:

```rust
intent MindBatchIntent {
    RoleHandoff,
    SchemaUpgrade(SchemaUpgradeIntent),    // tuple variant
    ChannelMigration,
}
```

Should the macro auto-generate a `MindBatchIntentKind` too (unit-only
projection of the intent enum)? Plausibly useful for audit summaries
that don't need the full payload. Probably worth emitting; another
`<EnumName>Kind` for each named enum the macro sees.

---

## 9 · `/173`'s status

`/173` concluded "no fundamental rethink." DA's response showed this
was too conservative. The redesign in §3–§5 above supersedes `/173`'s
conclusion. `/173`'s detailed inventory of current emissions remains
useful as a baseline; its conclusion retires.

---

## 10 · See also

- `~/primary/reports/designer/172-typed-request-shape-and-execution-semantics.md`
  — the typed shape this redesign serves; corrections in §2 above
  apply to `/172` directly.
- `~/primary/reports/designer/173-signal-channel-macro-rethink.md`
  — the conservative predecessor; superseded by this report on the
  redesign decision.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  current macro; replaced by the proc-macro form spec'd here.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:1633`
  — the hand-written `MindOperationKind` that auto-generation
  retires.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:1802`
  — the hand-written `operation_kind()` impl that retires with it.
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the discipline
  unchanged across the redesign.
