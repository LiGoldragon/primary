# 173 — Does `signal_channel!` need a fundamental rethink?

*Designer research report, 2026-05-15. Audits the current
`signal_channel!` macro against `/172`'s new spec (typed Request /
Reply / Intent, NonEmpty ops, batch outcomes, two-phase staged
subscription open, verb-checked receive API). Answers the structural
question: does the macro need a fundamental rethink, or does it grow
along its current axis? Conclusion: **it grows; it does not need
fundamental rethinking**, but the new shape sits at the upper edge of
what `macro_rules!` should be asked to do, and a `proc-macro`
migration would be the cleaner long-term shape.*

**Retires when**: the macro lands its `/172`-shaped form (either by
extending the current `macro_rules!` or by migrating to a proc-macro),
and the spec absorbs into `signal-core/ARCHITECTURE.md`.

---

## 0 · TL;DR

The macro's *grammar* changes minimally: one optional clause (`with
intent <T>`) on the request block, one optional trailing block
(`intent <T> { ... }`). Today's two arms become two arms again (with
or without intent), or one arm with `$( ... )?` optional matching.

The macro's *emissions* grow more substantially: one new enum (the
intent type, or `NoIntent` as default), three new type aliases
(`ChannelRequest`, `ChannelReply`, and a batch-builder helper), the
existing per-variant From impls and NOTA codec impls, plus a new
`is_subscribe` helper for the position-check fast path. The bulk of
the new machinery (`Request<P, I>`, `Reply<P, I>`, `BatchOutcome`,
`SubReply`, `BatchVerbMismatch`, `into_ops_checked`, `NonEmpty`,
NOTA codec for batched frames) **does not live in the macro** —
it lives in `signal-core` and is parameterized over the
channel-supplied types.

This is **not a fundamental rethink**. The macro stays a thin
boilerplate-eliminator over signal-core's typed primitives. What
changes is that signal-core's primitives themselves grew.

That said, the new emissions push `macro_rules!` close to its
practical ergonomic limits. Today's macro is ~140 lines; the
`/172`-shaped version, written in `macro_rules!`, would be ~250–350
lines with multiple internal helper-macro arms to handle the optional
intent path. A `proc-macro` rewrite would be cleaner — better error
messages, simpler conditional emission, easier to extend with
per-receiver batch-policy declarations or `BatchValidator` derives
later. The migration is real but bounded: ~2 days of operator work,
no contract changes required.

**The verdict**: keep the macro architecture, grow its emissions,
optionally migrate to proc-macro. There's no architectural smell that
requires deeper re-think.

---

## 1 · What the current macro emits

`/git/github.com/LiGoldragon/signal-core/src/channel.rs:93-233`. One
arm:

```
signal_channel! {
    request <Name> { <Verb> <Variant> ( <Payload> ), ... }
    reply <Name> { <Variant> ( <Payload> ), ... }
}
```

Emissions (≈140 lines including derives):

| # | Emission | Purpose |
|---|---|---|
| 1 | `pub enum <ReqName>` with rkyv + Debug + Clone + Eq derives | the request payload enum |
| 2 | `pub enum <RepName>` with same derives | the reply payload enum |
| 3 | `pub type Frame = signal_core::Frame<ReqName, RepName>` | per-channel Frame alias |
| 4 | `pub type FrameBody = signal_core::FrameBody<ReqName, RepName>` | per-channel FrameBody alias |
| 5 | `impl RequestPayload for <ReqName>` with verb-mapping match | the verb witness; receiver-side validation depends on this |
| 6 | `impl <ReqName>` with `signal_verb()` and `into_signal_request()` | ergonomic helpers |
| 7 | per-variant `impl From<Payload> for <ReqName>` | so `payload.into()` works |
| 8 | `impl NotaEncode for <ReqName>` dispatching to variant payloads | text codec encode |
| 9 | `impl NotaDecode for <ReqName>` matching on head identifier | text codec decode |
| 10 | per-variant `impl From<Payload> for <RepName>` | reply-side same |
| 11 | `impl NotaEncode for <RepName>` | same |
| 12 | `impl NotaDecode for <RepName>` | same |

The macro is structurally one large emission block with repeating
patterns (`$( ... )*` over variants).

---

## 2 · What `/172` spec requires

The spec adds new types in signal-core:

| Type | Owner | Per-channel? |
|---|---|---|
| `NonEmpty<T>` | signal-core | no — generic |
| `Op<Payload>` | signal-core | no — generic |
| `RequestHeader<Intent>` | signal-core | no — generic |
| `Request<Payload, Intent>` | signal-core | no — generic |
| `Reply<Payload, Intent>` | signal-core | no — generic |
| `ReplyHeader<Intent>` | signal-core | no — generic |
| `BatchOutcome` | signal-core | no |
| `SubReply<R>` | signal-core | no — generic |
| `SubStatus` | signal-core | no |
| `BatchFailureReason` (with `SubscribeOutOfOrder`) | signal-core | no |
| `SubFailureReason` | signal-core | no |
| `BatchVerbMismatch` | signal-core | no |
| `CheckedRequest<P, I>` | signal-core | no — generic |
| `NoIntent` (uninhabited) | signal-core | no |
| `Request::into_ops_checked()` | signal-core impl on Request | no — generic |
| `Request::single(payload)` convenience | signal-core impl | no — generic |
| NOTA codec for `Request<P, I>` and `Reply<P, I>` | signal-core, parameterized over P+I | no — generic |
| Two-phase staged-open runtime logic | receiver-side runtime | per-receiver |
| `<ChannelIntentName>` enum (the per-channel intent type) | macro-emitted | yes |
| Type aliases for `Frame`/`FrameBody` parameterized over 4 types | macro-emitted | yes |

The split: **most new types are generic and live in signal-core**;
**the macro emits the channel-specific intent enum plus 4-parameter
type aliases**.

---

## 3 · Macro grammar extensions

Two extensions:

### 3.1 · Optional `with intent <T>` on the request block

```text
request <ReqName> with intent <IntentName> {
    <Verb> <Variant> ( <Payload> ), ...
}
```

…or, when no named intent is needed:

```text
request <ReqName> {
    <Verb> <Variant> ( <Payload> ), ...
}
```

The clause is optional and follows `$req_name`; if absent, the macro
substitutes `signal_core::NoIntent`.

### 3.2 · Optional trailing `intent <T> { ... }` block

```text
intent <IntentName> {
    <Variant1>,
    <Variant2>,
    ...
}
```

…or omitted, when no named intent is declared.

The intent enum is closed: variants are listed, no `Custom(String)`
escape hatch (per `/172 §1.2`). Variants may carry payloads or be
unit:

```rust
intent MindBatchIntent {
    RoleHandoff,
    SchemaUpgrade(SchemaUpgradeIntent),    // carries a typed payload
    ChannelMigration,
}
```

That handles both unit and tuple-style intent variants.

### 3.3 · `macro_rules!` viability

`macro_rules!` supports both extensions through optional matching:

```rust
macro_rules! signal_channel {
    (
        request $req_name:ident
            $( with intent $intent_name:ident )?
        {
            $( $req_verb:ident $req_variant:ident ( $req_ty:ty ) ),* $(,)?
        }
        reply $rep_name:ident {
            $( $rep_variant:ident ( $rep_ty:ty ) ),* $(,)?
        }
        $( intent $intent_decl_name:ident {
            $( $intent_variant:ident $( ( $intent_ty:ty ) )? ),* $(,)?
        } )?
    ) => {
        // ...
    };
}
```

`$( ... )?` matches 0 or 1 times. The challenge: conditionally
emitting different code based on whether the optional matched. The
standard trick is two arms — one matches the with-intent shape, the
other matches the without-intent shape and either substitutes
`NoIntent` or invokes a helper macro.

This works in `macro_rules!`, but the resulting macro is harder to
read than the current one-arm version. The duplication isn't
catastrophic; it's a clear tradeoff.

---

## 4 · Macro emissions extensions

The new emissions in order:

### 4.1 · Intent enum (new — when present)

```rust
// Emitted only when an `intent` block was provided.
#[derive(::rkyv::Archive, ::rkyv::Serialize, ::rkyv::Deserialize,
         ::nota_codec::NotaEnum, Debug, Clone, PartialEq, Eq)]
pub enum <IntentName> {
    <Variant1>,
    <Variant2>(<Payload>),
    ...
}
```

Plus codec derives. The `NotaEnum` derive handles the NOTA codec
generically (for unit-only enums). For tuple-style variants, the macro
emits a manual `NotaEncode`/`NotaDecode` impl similar to the existing
request-enum dispatch — but each intent variant is independent.

### 4.2 · `Frame` / `FrameBody` aliases — now 4-parameter

```rust
pub type Frame = $crate::Frame<<ReqName>, <IntentName>, <RepName>, <IntentName>>;
pub type FrameBody = $crate::FrameBody<<ReqName>, <IntentName>, <RepName>, <IntentName>>;
```

The intent type is repeated because both request and reply carry the
same intent vocabulary. (A future extension could allow them to
differ, but per the current spec, they're the same channel's intent.)

### 4.3 · Channel request/reply aliases (new)

```rust
pub type ChannelRequest = $crate::Request<<ReqName>, <IntentName>>;
pub type ChannelReply = $crate::Reply<<RepName>, <IntentName>>;
```

These let callers reach `ChannelRequest::single(payload)` etc. without
typing the full 2-parameter shape each time.

### 4.4 · `is_subscribe` helper on the request enum (new)

```rust
impl <ReqName> {
    /// Returns true if this variant's declared verb is Subscribe.
    /// Used by Request::into_ops_checked for the
    /// Subscribe-must-be-last position check.
    pub fn is_subscribe(&self) -> bool {
        matches!(self.signal_verb(), $crate::SignalVerb::Subscribe)
    }
}
```

Actually this can live on signal-core as a default-method on
`RequestPayload`:

```rust
pub trait RequestPayload {
    fn signal_verb(&self) -> SignalVerb;
    fn is_subscribe(&self) -> bool {
        self.signal_verb() == SignalVerb::Subscribe
    }
}
```

If we make it a default-method, the macro doesn't need to emit
anything for it.

### 4.5 · Everything else: unchanged

The existing emissions stay:

- Request/reply enum definitions with their derives
- `RequestPayload` impl with verb-mapping match (unchanged)
- Per-variant `From<Payload>` impls (unchanged)
- `NotaEncode`/`NotaDecode` per enum (unchanged)
- `signal_verb()` / `into_signal_request()` helpers (the latter wraps
  in a `Request::single()` now)

The total new emission is **roughly +50 lines per channel**:
~10 lines of intent-enum declaration, ~5 lines of the 4-parameter
type aliases, ~5 lines of channel request/reply aliases, ~30 lines if
the intent enum has tuple-style variants (manual codec impls), plus
the two-arm macro duplication for with/without intent.

---

## 5 · What does *not* live in the macro

Per `/172`'s spec, these all live in `signal-core` and are
parameterized over the channel-supplied types:

- `NonEmpty<T>` collection with `new(head: T)` / `cons(self, T)` /
  iteration / length
- `Op<Payload>` struct
- `RequestHeader<Intent>` enum (Anonymous / Tracked / Named)
- `ReplyHeader<Intent>` enum (same)
- `Request<Payload, Intent>` struct
- `Reply<Payload, Intent>` enum (Batch variant only)
- `BatchOutcome` enum (Completed / Aborted)
- `SubReply<R>` struct
- `SubStatus` enum
- `BatchFailureReason` enum (including the now-defined
  `SubscribeOutOfOrder`)
- `SubFailureReason` enum
- `BatchVerbMismatch` enum
- `CheckedRequest<P, I>` struct
- `NoIntent` uninhabited enum
- `Request::into_ops_checked()` impl
- `Request::single(payload)` convenience
- NOTA codec for `Request<P, I>` and `Reply<P, I>` (these parse the
  batch syntax `[(intent X) (correlation Y) (op) (op)]` and dispatch
  to per-payload codec impls that the macro emits)

The NOTA codec for batched frames is the trickiest part. It's
parameterized over the payload type `P` and the intent type `I`, both
of which have their own `NotaEncode`/`NotaDecode` impls (the macro
emits these). The batch codec doesn't know what the variants are; it
just knows that `P: NotaDecode + NotaEncode` and `I: NotaDecode +
NotaEncode`. The batch grammar is fixed across all channels:

```text
single-op:    (Variant payload...)
multi-op:     [ (intent X)? (correlation Y)? (Variant payload...) ... ]
```

The codec handles both top-level shapes. The macro doesn't need to
emit this codec per channel.

This is the cleanest split. Channel-specific concerns (the variant
list, the verb mapping, the intent vocabulary) stay in the macro; the
batch-mechanics concerns stay in signal-core.

---

## 6 · `macro_rules!` vs `proc-macro`

The new macro is reachable in `macro_rules!` but pushes the limits.
Comparing:

### macro_rules! pros / cons

**Pros**:

- No build-system change. `macro_rules!` is inline; no `[lib]
  proc-macro = true` crate split.
- The pattern-matching is exhaustive and Rust-syntactic.
- Already in place; growing it is incremental.

**Cons**:

- Conditional emission based on optional matches requires two macro
  arms or recursive helper macros. Code duplication.
- Error messages from `macro_rules!` failures are notoriously
  unhelpful; the user sees "no rules matched" or "expected
  identifier" without much hint about what went wrong.
- Extending the grammar (e.g., adding a `batch_policy { ... }` block,
  or per-variant attributes like `#[deprecated]`) gets harder with
  each addition.
- Documenting the macro shape requires tracking the matchers
  manually; there's no signature for `rustdoc` to render.

### proc-macro pros / cons

**Pros**:

- Full Rust code generation. Conditional emission is a normal `if`.
- Custom error messages via `syn::Error::new_spanned(token, msg)`;
  the compiler points at the exact offending token with a helpful
  description.
- Easy to extend: add a new optional `batch_policy` block? Parse it
  in `syn`, emit the corresponding code; no macro-pattern gymnastics.
- Better tooling: `cargo expand` works on both, but proc-macros
  integrate more cleanly with IDE features like type-hover.
- Can derive items from the input — e.g., generate `is_subscribe()`
  by scanning variants tagged `Subscribe`, or generate
  `BatchPolicy::is_homogeneous()` checks per channel.

**Cons**:

- Requires a new crate (`signal-core-macros` or similar) with `[lib]
  proc-macro = true`. The main `signal-core` crate re-exports the
  macro.
- Adds `syn` and `quote` as build-time dependencies (these are
  ubiquitous in the Rust ecosystem; modest cost).
- One-time migration: rewrite the existing emissions in `quote!{}`
  blocks. ~2 days of operator work.

### Verdict on the macro engine

The macro **does not need to migrate right now**. The new shape is
reachable in `macro_rules!` with acceptable duplication. But each
future extension (batch policy, per-variant attributes, per-channel
validators) will make `macro_rules!` less ergonomic, and the
error-message gap is a real cost during contract authoring.

If the workspace already plans further extensions to the macro
contract — and the open questions in `/172 §7` suggest it does
(batch policy, frame-size limits, cross-component correlation
lifecycle) — then a proc-macro migration done **once, alongside the
`/172` shape change**, is cheaper than `macro_rules!`-then-migrate.

If the workspace expects the macro to stabilize after `/172` and
not grow further, `macro_rules!` continues to be fine.

---

## 7 · What about the deeper question?

Is there a *fundamental* rethink we're missing? Reasons we might
rebuild the macro entirely:

### 7.1 · Should `signal_channel!` be one macro or multiple?

Today's macro does many things at once: declares request/reply
enums, emits codec impls, emits Frame/FrameBody aliases. A more
factored design might be:

- `signal_request_enum! { ... }` — just the request enum + codec + verb witness
- `signal_reply_enum! { ... }` — just the reply enum + codec
- `signal_intent_enum! { ... }` — just the intent
- `signal_channel! { request <X>, reply <Y>, intent <Z> }` — composes them

This is more compositional. Each piece can be tested independently.
But it's also more verbose at the call site; contracts that don't
need the factoring would prefer one-shot declaration.

Probably **not worth the change**. The unified macro matches how
people think about a channel: one wire boundary, one block of
declaration.

### 7.2 · Should the macro use a different IR?

Some workspaces define channels in a NOTA / Nexus-shaped
declarative file, not in Rust source:

```nota
(Channel signal-persona-mind
    (Request (Assert SubmitThought))
    (Request (Mutate StatusChange))
    ...
    (Reply Thought)
    (Reply Status)
    ...
    (Intent MindBatchIntent (RoleHandoff) (SchemaUpgrade)))
```

…and codegen generates the Rust source. This is the
nota-codec-derive pattern at the next level up. Pro: contracts are
language-neutral, easier to display in documentation, can be
cross-validated against persona-mind ARCH. Con: another build step,
another tool chain.

Probably **not for first prototype**. The macro stays Rust-syntactic;
if a NOTA-shaped channel-declaration language emerges, it'd be a
generator that *outputs* the macro form, not a replacement.

### 7.3 · Should runtime concerns live in the macro?

The macro could emit a default `BatchValidator` impl that enforces
the per-channel batch policy (homogeneous-writes-only, no
Subscribe-mid-batch, etc.). Today the receiver code does this
manually. Macro-emitting it would centralize the policy.

Worth considering for `/172 §7 Q1` (per-receiver batch policy), but
**doesn't justify a fundamental rethink** — it's another emission
the macro grows to include if/when the batch-policy syntax is
specified.

---

## 8 · Verdict

The `signal_channel!` macro **does not need a fundamental rethink**.
It needs to grow:

- New optional `with intent <T>` clause on the request block.
- New optional trailing `intent <T> { ... }` block.
- Emission of the intent enum (or substitution of `NoIntent`).
- Emission of 4-parameter Frame/FrameBody aliases.
- Emission of `ChannelRequest` / `ChannelReply` shortcut aliases.
- Optional emission of `is_subscribe` helper (or default-method on
  `RequestPayload` trait).

Everything else (the batch shape, the verb-checked receive API, the
NOTA codec for batches, the two-phase staged-open) lives in
`signal-core` as generic primitives, not in the macro.

The macro engine choice (`macro_rules!` vs `proc-macro`) is the only
real architectural decision. My recommendation: **migrate to
proc-macro** alongside the `/172` shape change. Reasons:

1. The new shape pushes `macro_rules!` close to its ergonomic
   limits.
2. Future extensions (batch policy, per-variant attributes,
   subscription-validator derives, frame-size limits) will be
   significantly easier in a proc-macro.
3. Error messages from `proc-macro` are much better for contract
   authors.
4. The migration cost is bounded (~2 days) and one-time.

But this is the "would be cleaner" recommendation. `macro_rules!`
continues to work; the architectural shape of the macro is sound;
there's no smell that demands the rethink. Choose by preference.

---

## 9 · Open questions

### Q1 — When does the macro migration land?

Three options:

- (a) **Now**, alongside the `/172` extensions: one operator pass,
  proc-macro takes the new shape. Smoother extension over time.
- (b) **Later**, when batch-policy or another extension is added:
  the migration is triggered by a concrete need.
- (c) **Never**: stay in `macro_rules!` indefinitely, accept the
  ergonomic limits as the cost of avoiding a build-time dep.

If proc-macro happens, (a) is the natural moment. (b) defers the
decision. (c) is a stable position but means each future macro
extension is a `macro_rules!` puzzle.

### Q2 — Should `is_subscribe` be a `RequestPayload` default-method or macro-emitted?

Either works. Default-method is cleaner (one source of truth, no
duplication). Macro-emitted is slightly faster (no virtual dispatch
needed; the match is exhaustive). For a function called on every
incoming op, the perf is probably negligible.

Recommend: default-method on the trait. Less generated code.

### Q3 — Should the macro emit a `ChannelHeader::build_named(intent, correlation)` constructor?

For ergonomic frame construction with named intent. Today an agent
would write:

```rust
ChannelRequest {
    header: RequestHeader::Named { intent: MindBatchIntent::RoleHandoff, correlation: cor_id },
    ops: NonEmpty::from_vec(vec![
        Op { verb: SignalVerb::Retract, payload: MindRequest::RoleRelease(...) },
        Op { verb: SignalVerb::Assert, payload: MindRequest::RoleClaim(...) },
    ]),
}
```

With macro-emitted constructors:

```rust
ChannelRequest::named(MindBatchIntent::RoleHandoff, cor_id)
    .with(MindRequest::RoleRelease(...))
    .with(MindRequest::RoleClaim(...))
```

A builder pattern. Probably worth emitting; it's per-channel
ergonomics. ~10 lines of macro emission for the builder pattern.

### Q4 — Does the macro need to know about per-channel batch policy?

Per `/172 §7 Q1`. If yes, the macro grows a `batch_policy { ... }`
block; emissions include a `BatchPolicyImpl`. If no, the receiver
code enforces policy at runtime without macro support.

Deferring to per-receiver runtime is simpler now; if a pattern
emerges where many channels want the same policy declared
declaratively, fold it into the macro then.

---

## 10 · See also

- `~/primary/reports/designer/172-typed-request-shape-and-execution-semantics.md`
  — the spec the macro is being grown to support.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  current `signal_channel!` macro source (lines 93–233).
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the discipline the
  macro enforces; unchanged by the rewrite.
- `/git/github.com/LiGoldragon/nota-codec/src/lib.rs` — the
  `NotaEnum` / `NotaRecord` / `NotaTransparent` derives that the
  macro's emissions depend on.
