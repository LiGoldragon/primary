# 175 — Rust-shape and NOTA-syntax corrections to `/172` and `/174`

*Designer follow-up, 2026-05-15. Responds to DA's six findings on
`/174`. All six are correct on the design level. Settles the
implementation-ready Rust shape: constructors live on the
`RequestPayload` trait (not as inherent impls on type aliases — Rust
forbids that); `BatchPolicy` connects to `Request::validate` via a
generic parameter with `DefaultPolicy` as the default; `custom_check`
removed from the macro (validation pipelines belong in the daemon,
not the contract); NOTA syntax uses typed `BatchHeaderShape` records
instead of keyword-like lowercase heads; the stale 4-axis Frame
example in `/172` is corrected; `NoIntent` documents its required
derives.*

**Retires when**: `/172` and `/174` absorb these corrections; the
operator picks up implementation.

---

## 0 · TL;DR

DA's six findings, all concurred:

1. **Inherent impl on type alias is illegal Rust.** `/174 §4.3` wrote
   `impl ChannelRequest { ... }` where `ChannelRequest = Request<P,
   I>`. Rust forbids inherent impls on aliases to types defined in
   other crates. Fix: constructors live as default methods on
   `RequestPayload` in signal-core; multi-op uses `BatchBuilder`;
   per-channel ergonomics come from type aliases that resolve the
   generic parameters, not from new inherent impls.
2. **`BatchPolicy` not mechanically connected to `Request::validate`.**
   `/174` claimed the connection but `/172`'s validate signature
   doesn't accept policy. Fix: `validate<Policy: BatchPolicy<P, I> =
   DefaultPolicy>(&self)` takes the policy as a generic with a
   default; macro emits a per-channel unit struct that implements
   `BatchPolicy`.
3. **`custom_check` in the macro moves runtime logic into contract
   crates.** Conflicts with `skills/contract-repo.md`. Fix: drop
   `custom_check`; `batch_policy { ... }` stays purely declarative
   (max_ops, allow_mixed_read_write, etc.); custom checks live in
   daemon code.
4. **NOTA examples use lowercase keyword-like heads.** `(intent
   RoleHandoff)` and `(correlation cor-id)` at the top level violate
   PascalCase-for-record-heads. Fix: wrap in a typed
   `BatchHeaderShape` sum (`Anonymous` / `Tracked(CorrelationId)` /
   `Named { intent, correlation }`).
5. **Stale 4-axis Frame example in `/172 §8`.** Line 705's `pub type
   MindFrame = Frame<MindRequest, MindBatchIntent, MindReply,
   MindBatchIntent>;` contradicts `/174 §2.1`'s 3-axis correction.
   Fix: line edit to `Frame<MindRequest, MindReply,
   MindBatchIntent>`.
6. **`NoIntent` needs explicit codec derive bounds.** The
   `Request<P, I>` / `Reply<P, I>` codecs need `I: Archive +
   Serialize + Deserialize + NotaEncode + NotaDecode`. Fix:
   `NoIntent` derives all of these unconditionally; the impls are
   trivially satisfied (empty match on uninhabited enum), never
   called at runtime.

Updates to `/172` and `/174` listed in §7. The macro redesign in
`/174 §3–§5` stays the right direction; this report fixes the Rust
shape and NOTA syntax mistakes within it.

---

## 1 · The corrected constructor surface

DA's blocker: `impl ChannelRequest { fn single(...) }` where
`ChannelRequest = signal_core::Request<MindRequest, MindBatchIntent>`
is invalid Rust. You can't write inherent impls on type aliases to
types defined in other crates.

The right shape: constructors live in `signal-core` as **default
methods on the `RequestPayload` trait**, and **type aliases let
callers reach the generic methods** without spelling out the type
parameters.

### 1.1 · Construction lives in signal-core on `RequestPayload`

```rust
// signal-core/src/request.rs

pub trait RequestPayload: Sized {
    /// The per-variant verb the contract macro emits.
    fn signal_verb(&self) -> SignalVerb;

    /// Default method: payload becomes a Subscribe iff its verb is.
    fn is_subscribe(&self) -> bool {
        self.signal_verb() == SignalVerb::Subscribe
    }

    /// Default method: wrap a single payload into an anonymous
    /// batch (length-1 batch with no audit metadata).
    fn into_anonymous<Intent>(self) -> Request<Self, Intent> {
        Request::single_anonymous(self)
    }

    /// Default method: wrap a single payload into a tracked batch.
    fn into_tracked<Intent>(self, correlation: CorrelationId) -> Request<Self, Intent> {
        Request::single_tracked(self, correlation)
    }

    /// Default method: wrap a single payload into a named batch.
    fn into_named<Intent>(self, intent: Intent, correlation: CorrelationId) -> Request<Self, Intent> {
        Request::single_named(self, intent, correlation)
    }
}
```

These are default methods on the trait; they don't require any
per-channel emission. Every contract that derives `RequestPayload`
(via the `signal_channel!` macro) inherits the construction surface.

Call sites:

```rust
let req = MindRequest::SubmitThought(thought).into_anonymous::<MindBatchIntent>();
let req = MindRequest::RoleClaim(claim)
    .into_named(MindBatchIntent::RoleHandoff, cor_id);
```

The turbofish `::<MindBatchIntent>` on `into_anonymous` is needed
because there's no payload context to infer `Intent` from. Type
ascription on the binding (`let req: ChannelRequest = ...`) can also
drive inference.

### 1.2 · Multi-op uses `BatchBuilder` in signal-core

```rust
// signal-core/src/request.rs

pub struct BatchBuilder<P, I> {
    header: RequestHeader<I>,
    ops: Vec<Op<P>>,
}

impl<P, I> BatchBuilder<P, I>
where
    P: RequestPayload,
{
    pub fn new_anonymous() -> Self;
    pub fn new_tracked(correlation: CorrelationId) -> Self;
    pub fn new_named(intent: I, correlation: CorrelationId) -> Self;

    pub fn with(mut self, payload: P) -> Self {
        let verb = payload.signal_verb();
        self.ops.push(Op { verb, payload });
        self
    }

    pub fn build(self) -> Result<Request<P, I>, BatchBuilderError>;
}

pub enum BatchBuilderError {
    /// build() was called with zero ops; NonEmpty requires ≥1.
    EmptyBatch,
}
```

The builder is generic. Per-channel ergonomics come from a type
alias:

```rust
// macro-emitted (in signal-persona-mind)

pub type ChannelRequest = signal_core::Request<MindRequest, MindBatchIntent>;
pub type ChannelReply = signal_core::Reply<MindReply, MindBatchIntent>;
pub type ChannelBuilder = signal_core::BatchBuilder<MindRequest, MindBatchIntent>;

// NOTE: no `impl ChannelRequest { ... }` blocks — that's the illegal
// shape DA's finding 1 caught. The aliases only let callers reach
// generic methods on the underlying types without typing
// <MindRequest, MindBatchIntent> at every call site.
```

Call sites:

```rust
let req = ChannelBuilder::new_named(MindBatchIntent::RoleHandoff, cor_id)
    .with(MindRequest::RoleRelease(old_claim))
    .with(MindRequest::RoleClaim(new_claim))
    .build()?;
```

`ChannelBuilder::new_named` works because `ChannelBuilder` is a type
alias to `BatchBuilder<MindRequest, MindBatchIntent>`; Rust's path
resolution looks through aliases to find associated functions on the
underlying type. **No inherent impl needed.**

---

## 2 · `BatchPolicy` connection to `validate`

DA's finding 2: `/174` said `validate` consults the channel policy,
but the validate signature in `/172` (with the `/174 §2.2`
correction) only requires `P: RequestPayload` and runs universal
rules only. The policy is dangling.

### 2.1 · `BatchPolicy` trait

```rust
// signal-core/src/batch_policy.rs

pub trait BatchPolicy<P, I>
where
    P: RequestPayload,
{
    /// Maximum number of ops in one batch. Default: no cap.
    fn max_ops() -> usize { usize::MAX }

    /// Whether `Match` and write ops may appear in the same batch.
    /// Default: permitted (per `/172 §4`).
    fn allow_mixed_read_write() -> bool { true }

    /// Whether `Subscribe` ops are allowed at all in this channel.
    /// Default: permitted (the universal rule that Subscribes
    /// must be last is enforced by `signal-core::Request::validate`
    /// regardless of channel policy).
    fn forbid_subscribe() -> bool { false }

    /// Whether `Validate` ops are allowed in this channel.
    /// Default: permitted.
    fn forbid_validate() -> bool { false }
}

/// The default policy — permissive on everything channel-specific.
/// Used when a channel doesn't declare a `batch_policy { ... }` block.
pub struct DefaultPolicy;
impl<P, I> BatchPolicy<P, I> for DefaultPolicy
where
    P: RequestPayload,
{
    // Inherits all defaults from the trait.
}
```

### 2.2 · `Request::validate` is generic over policy

```rust
impl<P, I> Request<P, I>
where
    P: RequestPayload,
{
    /// Validate without consuming. Universal rules + channel policy.
    /// `Policy` defaults to `DefaultPolicy` (permissive).
    pub fn validate<Policy: BatchPolicy<P, I> = DefaultPolicy>(
        &self,
    ) -> Result<(), BatchVerbMismatch> {
        // 1. Universal rules (per /172 §1.7):
        //    - Subscribe-must-be-last (BatchVerbMismatch::SubscribeOutOfOrder)
        //    - Verb/payload alignment (BatchVerbMismatch::OpMismatch)
        //    - NonEmpty is type-enforced; can't fail here.
        self.validate_universal()?;

        // 2. Channel policy:
        if self.ops.len() > Policy::max_ops() {
            return Err(BatchVerbMismatch::PolicyViolation {
                rule: "max_ops",
                limit: Policy::max_ops(),
            });
        }
        if Policy::forbid_subscribe() && self.contains_subscribe() {
            return Err(BatchVerbMismatch::PolicyViolation {
                rule: "forbid_subscribe",
                limit: 0,
            });
        }
        // ... other policy rules ...

        Ok(())
    }

    /// Convert to a CheckedRequest, validating along the way.
    /// On failure, returns the unconverted request for reply-building.
    pub fn into_checked<Policy: BatchPolicy<P, I> = DefaultPolicy>(
        self,
    ) -> Result<CheckedRequest<P, I>, (BatchVerbMismatch, Self)> {
        if let Err(reason) = self.validate::<Policy>() {
            return Err((reason, self));
        }
        let (header, ops) = self.into_parts();
        Ok(CheckedRequest { header, ops })
    }
}
```

The `BatchVerbMismatch` enum gains a `PolicyViolation` variant
carrying the named rule and any threshold:

```rust
pub enum BatchVerbMismatch {
    OpMismatch { index: usize, expected: SignalVerb, got: SignalVerb },
    SubscribeOutOfOrder { index: usize },
    PolicyViolation { rule: &'static str, limit: usize },
}
```

Call sites without an explicit policy use the default:

```rust
request.validate()?;
let checked = request.into_checked()?;
```

Channels with a specific policy spec the turbofish:

```rust
request.validate::<MindRequestPolicy>()?;
let checked = request.into_checked::<MindRequestPolicy>()?;
```

Or the macro emits per-channel free functions for further ergonomics:

```rust
// macro-emitted in signal-persona-mind
pub fn validate(request: &ChannelRequest) -> Result<(), BatchVerbMismatch> {
    request.validate::<MindRequestPolicy>()
}
```

Call site: `signal_persona_mind::validate(&request)?`. Clean.

### 2.3 · Macro emits the channel's policy

```rust
// macro-emitted (from the `batch_policy { ... }` block)

pub struct MindRequestPolicy;

impl signal_core::BatchPolicy<MindRequest, MindBatchIntent> for MindRequestPolicy {
    fn max_ops() -> usize { 32 }
    fn allow_mixed_read_write() -> bool { true }
    fn forbid_subscribe() -> bool { false }
    fn forbid_validate() -> bool { false }
}
```

A unit struct (not an impl on the request enum), implementing the
`BatchPolicy` trait. The receiver passes `MindRequestPolicy` as the
`Policy` type parameter to `validate`.

If the contract has no `batch_policy { ... }` block, the macro
substitutes `DefaultPolicy` (or emits a unit struct that defers to
defaults — same effect).

---

## 3 · `custom_check` is removed

DA's finding 3: `custom_check: |request| -> Result<...> { ... }`
moves runtime validation pipeline logic into contract crates,
conflicting with `skills/contract-repo.md` §"What goes in a contract
repo" (contracts own typed records, not validation pipelines).

Fix: drop `custom_check` from the macro. `batch_policy { ... }`
stays purely declarative — fields that name a closed set of rules,
no closures, no expressions:

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

The closed declarative field list is the contract surface. **Daemon
code** that needs custom checks does so in its receive path, after
`request.validate::<MindRequestPolicy>()`. The custom check stays
in the runtime, not the contract.

If a check is universal enough to be expressed declaratively, it
gets a new `BatchPolicy` field (a coordinated macro extension). If
it's runtime-shaped (depends on database state, requires policy
actor consultation, etc.), it lives in the daemon.

---

## 4 · NOTA syntax — typed `BatchHeaderShape` records

DA's finding 4: examples like `(intent RoleHandoff)` and
`(correlation cor-id)` at the top level of a batch violate
`skills/language-design.md` §"PascalCase = type, camelCase =
instance" (record heads must be PascalCase). They read as
keyword-prefixed annotations rather than typed records.

Fix: encode the header as a typed sum. The right type already
exists — `RequestHeader<Intent>` from `/172 §2`. **Use it directly**
for the NOTA encoding rather than introducing a parallel
`BatchHeaderShape` type (per operator/117 §"NOTA Shape: Use /175
Canon" — "prefer deriving this projection from the real
`RequestHeader<Intent>` … avoid parallel projection-only types if
the real domain type can own the NOTA representation directly").
An earlier draft of this report proposed a separate
`BatchHeaderShape`; that's redundant and dropped.

```rust
// signal-core (already in /172 §2 — re-shown here for the NOTA codec):
pub enum RequestHeader<Intent> {
    Anonymous,
    Tracked { correlation: CorrelationId },
    Named { intent: Intent, correlation: CorrelationId },
}
```

NOTA encoding (positional per `skills/language-design.md`
§"Records are positional; field names live in the schema"):

- `(Anonymous)` — unit variant
- `(Tracked "cor-id")` — single positional field
- `(Named RoleHandoff "cor-id")` — two positional fields (intent, correlation)

The batch frame is then:

```text
(Batch <header> <ops-sequence>)
```

Worked examples:

```sh
# Anonymous (no audit metadata):
mind '(Batch (Anonymous) [(Assert (SubmitThought (...)))])'

# Tracked (correlation only):
mind '(Batch (Tracked "cor-abc-123") [(Match (QueryThoughts (limit 10)))])'

# Named (intent + correlation):
mind '(Batch (Named RoleHandoff "cor-abc-123")
              [(Retract (RoleClaim (role Designer)))
               (Assert  (RoleClaim (role Poet)))])'

# Single-op anonymous sugar (CLI desugars to `(Batch (Anonymous) [...])`):
mind '(Assert (SubmitThought (...)))'
```

All record heads are PascalCase. Field positions are schema-named,
not text-named. The `[ ... ]` brackets are sequences, which are the
universal NOTA structural primitive (per
`skills/language-design.md` §"Delimiters earn their place"). No
new sigils, no keywords.

`/172 §6`'s NOTA grammar block needs to be rewritten with this
shape. `/174 §5.1`'s grammar sketch needs the same fix.

---

## 5 · `NoIntent` codec derives

DA's finding 6: the `Request<P, I>` / `Reply<P, I>` codecs need
trait bounds on `I`. When `I = NoIntent`, the bounds need to be
satisfiable.

Fix: `NoIntent` derives the necessary traits unconditionally:

```rust
// signal-core/src/intent.rs

#[derive(
    ::rkyv::Archive,
    ::rkyv::Serialize,
    ::rkyv::Deserialize,
    ::nota_codec::NotaEnum,
    Debug,
    Clone,
    PartialEq,
    Eq,
)]
pub enum NoIntent {}
```

Empty-enum derives generate trivial impls that match on
`!`-typed unreachable expressions. They satisfy the trait bounds
without ever being called at runtime — the type is uninhabited, so
no `NoIntent` value can be constructed, so no codec impl ever
executes.

This needs verification against rkyv 0.8's empty-enum support;
older rkyv versions had issues with `Archive` on empty enums.
Operator should confirm during implementation. If rkyv 0.8 doesn't
support empty enums, the fallback is a phantom-data wrapper:

```rust
pub struct NoIntent(::core::marker::PhantomData<!>);
```

…or a single-variant private enum that can never be constructed.
But the cleaner uninhabited `enum NoIntent {}` should work if
codec derives accept it.

---

## 6 · Updates required to `/172` and `/174`

### 6.1 · `/172` updates

| Section | Change |
|---|---|
| §2 | `Request::validate` signature gains `<Policy: BatchPolicy<P, I> = DefaultPolicy>`. `Request::into_checked` same. |
| §2 | `BatchVerbMismatch` gains `PolicyViolation { rule, limit }` variant. |
| §2 | `BatchHeaderShape` enum added as the on-wire shape (Anonymous / Tracked / Named). |
| §2 | `NoIntent` documents its derive set (rkyv + NotaEnum + Debug/Clone/Eq). |
| §6 | NOTA examples rewritten to use `(Batch (Header) [ops])` shape; no lowercase top-level annotations. |
| §8 | Worked examples (Q3, Q4) rewritten to use the typed Batch/Header records. |
| §8.3 line 103 | `pub type MindFrame = Frame<MindRequest, MindBatchIntent, MindReply, MindBatchIntent>` → `Frame<MindRequest, MindReply, MindBatchIntent>`. |
| §8.4 line 705 | Same fix. |

### 6.2 · `/174` updates

| Section | Change |
|---|---|
| §4.3 | Drop `impl ChannelRequest { ... }`; replace with: (a) reference to `RequestPayload` default methods in signal-core; (b) per-channel type aliases for `ChannelBuilder`. |
| §4.2 | Drop `custom_check` from the `batch_policy` block. Declarative-only fields. |
| §4.2 | `BatchPolicy` impl is on a unit struct (`MindRequestPolicy`), not on the request enum. |
| §5 | NOTA grammar examples updated per §4 above. |
| §5.2 emissions | Remove `impl ChannelRequest`; add `pub struct MindRequestPolicy; impl BatchPolicy for ...`; add type alias `pub type ChannelBuilder = BatchBuilder<...>`. |

---

## 7 · Open questions

The questions surviving from `/172 §7` and `/174 §8` plus DA's
implementation-readiness ones:

### Q1 — Does `NoIntent` actually derive cleanly under rkyv 0.8?

Empirical question; operator confirms during implementation. If
not, fall back to phantom-data wrapper.

### Q2 — Should the macro emit a per-channel `validate` free function?

`/175 §2.2` mentioned this as further ergonomics:
```rust
pub fn validate(request: &ChannelRequest) -> Result<(), BatchVerbMismatch> {
    request.validate::<MindRequestPolicy>()
}
```

Lean yes — saves the turbofish at every call site. Add to the macro
emissions list.

### Q3 — How does the receiver know which `Policy` type to apply?

If the contract emits `MindRequestPolicy`, the receiver code that
imports the contract gets the policy type. Receivers always know the
channel's contract; the type follows the import. Settled.

### Q4 — Default policy for channels without `batch_policy { ... }`?

Two paths:
- Macro substitutes `signal_core::DefaultPolicy`.
- Macro emits a unit struct (`<Channel>DefaultPolicy`) that defers
  to defaults.

The first is simpler; lean toward it.

---

## 8 · See also

- `~/primary/reports/designer/172-typed-request-shape-and-execution-semantics.md`
  — updated per §6.1 above.
- `~/primary/reports/designer/174-signal-channel-macro-redesign.md`
  — updated per §6.2 above.
- `~/primary/skills/contract-repo.md` §"What goes in a contract
  repo" — the discipline that rules out `custom_check`.
- `~/primary/skills/language-design.md` §"PascalCase = type,
  camelCase = instance" + §"Records are positional; field names
  live in the schema" — the NOTA discipline this report's §4
  honors.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  current macro source; what the redesign replaces.
