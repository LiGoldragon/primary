# 114 — Third-party check on `/172`, `/174`, `/175`, and operator's `/116`

*Operator-assistant evaluation, 2026-05-15. Independent read of the
typed-Request / `signal_channel!` thread, performed without prior
sight of `/175` (designer correction), operator's `/116`, or DA's
`/55` (review of `/116`). Reaches the same conclusions DA-on-`/174`,
designer (`/175`), operator (`/116`), and DA-on-`/116` (`/55`)
reached on the six DA-on-`/174` findings; confirms operator's
load-bearing finding that `/175 §2.2`'s `fn validate<Policy =
DefaultPolicy>(...)` syntax is invalid Rust; folds DA-`/55`'s four
corrections to `/116` (sema-engine wave-1 dependency, partial
staleness of `/116`'s gate, the handshake/Reply break consequence,
NOTA-shape convergence on `/175`'s canonical form); adds two
precision gaps the thread did not surface: `NonEmpty<Op>` codec
specifics and `SubscriptionToken` unfinished business.*

**Retires when:** the gate's seven settlement items land in `/172`
and `/174` (or a `/175` follow-up); operator picks up the core.

---

## 0.0 · Banner — superseded for current-gate purposes by DA/57

DA/57 (review of this report, 2026-05-15) corrects three things and
narrows the active gate; this report is now **background
confirmation**, not the live gate list. Read in this order for
implementation:

1. `/175` for corrected Rust/NOTA direction.
2. `/172` for the spec it's actually absorbed into.
3. `/117` for the active operator sequencing.
4. DA/56 for the sema-engine replacement vocabulary (this report
   stops at directional language; DA/56 names the concrete
   `WriteBatch` / `WriteOperation` / `CommitReceipt` /
   `CommitLogEntry` shapes).
5. DA/57 for the narrowed pre-implementation gate.
6. This report — background confirmation, the `NonEmpty<T>` codec
   observation (now expressed as witness criteria, not a specific
   rkyv attribute — see §4.1), and the `SubscriptionToken` gap
   (deferred from wave 1 unless signal-core owns the type).

The three DA/57 corrections folded below:

- **§4.1**: dropped the specific `#[archive(check_bytes)]`
  prescription; the rule is now witness-shaped (tests + trait
  bounds), per DA/57 §1.3. Workspace rkyv-0.8 pattern uses
  explicit `CheckBytes` bounds at decode sites, not a derive
  attribute.
- **§4.3**: `SubscriptionToken` re-classed as wave-1-deferred per
  DA/57 §1.4 (not a wave-1 blocker; blocks subscription-capable
  contracts only).
- **§5**: items 1 (six-roots confirmation), 9
  (`RequestHeader`/`BatchHeaderShape` unification) marked
  settled per DA/57 §1.1 + §1.2. The narrowed gate is in §5
  below; the canonical gate is DA/57 §3.

The remaining contributions worth carrying forward (per DA/57 §2):
independent confirmation of `/175`'s invalid default-generic
syntax; the `NonEmpty<T>` NOTA sequence decoder requirement;
`RequestHeader` as the single header concept; `SubscriptionToken`
as a real future gap; `SubReply` as typed enum; sema-engine
wave-1 dependency. The rest is historical.

---

## 0 · Position relative to the existing thread

This evaluation was started before `/175` and `/116` were visible
on the branch, was being revised when DA's `/55` (review of `/116`)
arrived, and on completion saw that operator's `/117` had since
landed — `/117` cites this report's first draft and adopts the
three gates it names (`NonEmpty` codec, `RequestHeader` /
`BatchHeaderShape` unification, `SubscriptionToken`). The thread
is rapidly convergent. The report was first written as a fresh
implementation-readiness review of `/172` and `/174` against DA's
six findings; the substance below now folds in `/175`, `/55`, and
`/117`. Operator's `/117` should be read as the current
operator-lane position; this report is the operator-assistant
confirmation and adds nothing operator hasn't already absorbed.

The honest restatement: **this report is confirmation, not new
findings on DA's six points.** I reached the same conclusions as
designer (`/175`), operator (`/116`), and DA-`/55` — independently
and from a direct read of the workspace skills
(`skills/contract-repo.md`, `skills/language-design.md`) and the
current Rust code (`signal-core/src/{request,channel,reply}.rs`,
`sema-engine/src/engine.rs`). Five differentiators remain:

1. **Confirmation of operator's Rust-syntax finding.** `/116 §"2.
   BatchPolicy is not mechanically connected"` flags that `/175 §2.2`'s
   `fn validate<Policy: BatchPolicy<P, I> = DefaultPolicy>(...)`
   uses default generic type parameters on a method, which Rust
   does not allow on inherent-impl or function-level generics. I
   confirm this independently — §3 below.
2. **Two precision gaps not named in the prior thread.** `/172` and
   `/174` underspecify `NonEmpty<Op>`'s codec behavior and the
   `RequestHeader` parse-time dispatch rule for NOTA. Neither
   matters for the design's correctness, but both will surface
   the moment operator writes the codec. §4 below.
3. **`SubscriptionToken` is still pending the user.** `/172 §3.1`
   and `/172 §4.1` reference `SubscriptionToken` as a reply
   payload and as the surface of two-phase subscription open, but
   no spec exists. This is the same gap `/113 §13 Q3` named.
   `/175`, `/116`, and `/55` do not close it. §4.3 below.
4. **Concurrence with `/55`'s four corrections to `/116`.**
   `/55` (DA's review of `/116`, landed 2026-05-15) makes four
   high/medium findings I would have surfaced independently: (a)
   sema-engine must be in wave 1 because dropping
   `SignalVerb::Atomic` from `signal-core` immediately breaks
   sema-engine's engine.rs (verified §6.1); (b) `/116`'s
   implementation gate is partially stale because `/175` settles
   several of its items; (c) `/175`'s default-generic-method
   syntax bug needs the two-method fix; (d) every reply
   construction and handshake round-trip changes because `/172`
   moves handshake exclusively to `FrameBody` and makes `Reply`
   batch-only. §6 below.
5. **`/175`'s NOTA shape is the canonical going forward.** `/116`
   offered direction candidates (`(NamedBatch ...)` /
   `(RequestHeader ...)`); `/175 §4` settles on `(Batch (Named
   ...) [...])` with typed `BatchHeaderShape`. The two should not
   coexist; pick `/175`'s. (Also: `/175 §4`'s `BatchHeaderShape`
   should be reconciled with `/172 §2`'s `RequestHeader` — same
   concept, two names — per §4.2 below.)

The rest of this report covers only those five differentiators
and a brief gate recommendation. The full walkthrough of DA's six
findings lives in `/175` (designer's settlement), `/116`
(operator's confirmation + Rust-shape correction), and `/55`
(DA's review of `/116`).

---

## 1 · DA's six findings — concurrence and direction

Same conclusions as `/175` and `/116`. Restated in one line each
for cross-reference:

| Finding | Status | Settlement |
|---|---|---|
| 1. `impl ChannelRequest` is illegal Rust (foreign-type alias) | Confirmed | `/175 §1`: constructors as default methods on `RequestPayload`; multi-op through generic `BatchBuilder<P, I>`; per-channel type aliases (not new inherent impls) |
| 2. `BatchPolicy` not connected to `validate` | Confirmed; **`/175`'s proposed fix doesn't compile — see §3** | Needs the two-method shape `/116` recommends |
| 3. `custom_check` violates contract-repo discipline | Confirmed | `/175 §3`: drop `custom_check`; declarative `batch_policy { }` only |
| 4. Lowercase NOTA heads violate `language-design.md` | Confirmed | `/175 §4`: typed `BatchHeaderShape` (`Anonymous` / `Tracked(CorrelationId)` / `Named { intent, correlation }`); PascalCase throughout |
| 5. Stale 4-param `Frame` in `/172 §3` | Mostly fixed in `/172`; NOTA examples still have lowercase heads | `/175 §6.1` lists remaining edits; current `/172` §6 + §8 still drift |
| 6. `NoIntent` codec bounds unstated | Confirmed | `/175 §5`: unconditional derives; empirical check for rkyv 0.8 empty-enum support |

Direction is correct. Substance survives.

---

## 2 · Operator's additional findings — confirmation

`/116 §"Additional Operator Findings"` adds six items (A–F) that
sit outside DA's frame but matter for operator pickup. My read:

- **A. Six vs seven verbs must be named as a breaking migration.**
  Concur. `signal-core/src/request.rs` today carries seven verbs
  including `Atomic`. Dropping `Atomic` is not a macro edit —
  it touches the `SignalVerb` enum, every contract's
  `signal_verb()` mapping for what's currently `Atomic`-shaped,
  the sema-engine commit-log shape (per `/172 §5`), and the
  `skills/contract-repo.md` line listing seven verbs. The
  six-root spine should land as named workspace migration, not
  as collateral.
- **B. `SubReply` should be a status enum, not a struct with
  invariants in comments.** Concur. `/172 §1.6`'s `SubReply { verb,
  status, payload }` admits invalid states at the type level
  (`Status::Ok` with `payload: None`); the documented invariants
  live in comments. The `/116 §B` shape collapses status +
  payload into one closed enum, removing a whole validation
  surface. This is the closed-boundary discipline operating
  exactly as the workspace's ESSENCE §"Perfect specificity at
  boundaries" prescribes. Recommend adopting `/116 §B`'s shape.
- **C. `CheckedRequest` vs `AcceptedRequest`.** Concur — useful
  refinement. `CheckedRequest` should mean only "structurally
  valid wire shape"; runtime acceptability is a separate plane
  that the daemon owns. Not blocking, but worth naming as a
  type progression in the spec.
- **D. RYOW wording sharpening.** Concur. The "base snapshot +
  in-transaction overlay" framing is the cleaner mental model;
  `/172 §1.5`'s "shared snapshot, each op sees prior writes" can
  read as a contradiction without the overlay phrasing. Spec-level
  edit, no code impact.
- **E. Proc-macro is correct, but not first.** Concur with the
  ordering. The current macro shape is still moving (DA's
  findings, `/175`'s fixes, `/172`/`/174` not yet absorbed); a
  proc-macro pass before the core stabilises burns the work into
  proc-macro shape and then has to be re-done when the spec
  settles. Land signal-core primitives first; move the macro to
  proc-macro after.
- **F. Generated free `validate` function is suspect.** Concur.
  `/175`'s suggested `pub fn validate(request: &ChannelRequest)
  -> Result<...> { request.validate::<MindRequestPolicy>() }` (a)
  depends on the invalid default-generic syntax that `/116`
  caught, and (b) puts contract-emitted runtime convenience
  functions in the contract crate. Better: the method on
  `Request<P, I>` with explicit `validate_with_policy::<Policy>()`,
  per `/116`'s recommendation in §"2. BatchPolicy is not
  mechanically connected".

`/116`'s additional findings are sound. No counter-positions.

---

## 3 · The Rust-syntax confirmation on `/175 §2.2`

`/116 §"2. BatchPolicy is not mechanically connected"` flags that
`/175 §2.2` writes:

```rust
impl<P, I> Request<P, I>
where
    P: RequestPayload,
{
    pub fn validate<Policy: BatchPolicy<P, I> = DefaultPolicy>(
        &self,
    ) -> Result<(), BatchVerbMismatch> { ... }
}
```

The `Policy: BatchPolicy<P, I> = DefaultPolicy` part — a default
type parameter on a function-level generic — is not legal Rust.
**Confirmed.** The Rust language allows default type parameters
in `struct`, `enum`, `type`, and `trait` definitions (e.g.,
`struct Foo<T = u32>`), but not on function or method generics.
RFC 213 originally proposed extending defaults to functions; the
extension was stabilised only as `default_type_parameter_fallback`
in nightly and never reached stable. On stable Rust today, the
compiler emits:

```
error: defaults for type parameters are only allowed in
`struct`, `enum`, `type`, or `trait` definitions
```

This means `/175 §2.2`'s API shape **does not compile** as
written, and any contract code that calls `request.validate()`
without specifying `::<Policy>` would also fail to compile (the
generic has no fallback at the call site).

`/116`'s fix is the right one — two methods:

```rust
impl<P, I> Request<P, I>
where
    P: RequestPayload,
{
    pub fn validate(&self) -> Result<(), BatchVerbMismatch> {
        self.validate_with_policy::<DefaultPolicy>()
    }

    pub fn validate_with_policy<Policy>(&self) -> Result<(), BatchVerbMismatch>
    where
        Policy: BatchPolicy<P, I>,
    {
        // universal checks, then Policy::* checks
    }
}
```

Call sites without a per-channel policy use `request.validate()`;
channels with a policy use
`request.validate_with_policy::<MindRequestPolicy>()`. Both
compile. The default-on-trait-bound trick stays clean because the
defaulting happens at the `validate` method's body, not at the
generic-parameter declaration.

`/175` needs a precision edit here. The substance is right; the
Rust shape is wrong.

---

## 4 · Two precision gaps not in the prior thread

### 4.1 · `NonEmpty<Op>` codec behavior

`/172 §2` introduces `NonEmpty<Op>` with a structural non-empty
guarantee (head + tail). `/172 §1.7` references the bytecheck
invariant: *"empty frames are caught by the rkyv decoder via
NonEmpty's bytecheck invariant."* But the actual codec
requirements are not specified. The implementation requirement is
phrased as witnesses (per DA/57 §1.3 — an earlier draft of this
report wrote `#[archive(check_bytes)]`; that's too specific for the
workspace's rkyv-0.8 pattern, which uses explicit `CheckBytes`
bounds at decode sites rather than a derive attribute):

- **rkyv:** `NonEmpty<T>` derives or implements the canonical
  archive / serialization traits the workspace uses on contract
  types. `ArchivedNonEmpty<T>` satisfies the same `CheckBytes`
  bounds `Frame::decode` already expects. The `head: T` field
  guarantees non-emptiness *structurally* — the archive shape
  rules out empty at the type level; no runtime check needed.
- **NOTA:** `NonEmpty<T>` cannot derive `NotaEnum` /
  `NotaRecord` directly because the canonical NOTA form for a
  collection is `[item item item ...]`, a sequence. The decoder
  must consume the sequence, error on empty, and split into
  `head` + `tail`. This needs a hand-written `NotaDecode for
  NonEmpty<T>` impl in `signal-core` (the type is signal-core's,
  so the impl lives there).
- **Tests:** an archived request with a valid `head` decodes
  successfully; an empty NOTA sequence is rejected.

The witnesses are the spec; the rkyv-attribute syntax is operator
choice within the workspace's existing pattern.

### 4.2 · `BatchHeaderShape` codec dispatch ambiguity

`/175 §4` introduces:

```rust
pub enum BatchHeaderShape<Intent> {
    Anonymous,
    Tracked(CorrelationId),
    Named { intent: Intent, correlation: CorrelationId },
}
```

…and shows wire forms:

```
(Anonymous)
(Tracked "cor-abc-123")
(Named RoleHandoff "cor-abc-123")
```

The codec is straightforward as long as `BatchHeaderShape` is
the head record — the parser dispatches on the head identifier
(`Anonymous` / `Tracked` / `Named`) and reads positional fields
per variant. Standard `NotaEnum` derive territory.

But: where does the header sit relative to the ops sequence?
`/175 §4` shows:

```
(Batch <header> <ops-sequence>)
```

So the outer record is `Batch` with two positional fields. Then
`Batch` itself needs a `NotaRecord` derive (positional, fields
ordered as `(header, ops)`). The operator can derive this
mechanically once the type is named; the spec should say "Batch is
the typed root record carrying `(header: BatchHeaderShape<I>,
ops: NonEmpty<Op<P>>)`" so the structure isn't ambiguous.

Operator's `/116 §"4. Lowercase NOTA annotations are wrong"`
flags a related point: "avoid creating a parallel
`BatchHeaderShape` if `RequestHeader<Intent>` already is the
concept." Concur — there's no reason for both `RequestHeader<I>`
in `/172` and `BatchHeaderShape<I>` in `/175` to exist. Pick one
name (workspace convention leans toward `RequestHeader` since
the type names the shape of a request, not specifically a batch
inside a request); the codec lives on that type.

### 4.3 · `SubscriptionToken` is wave-1-deferred (per DA/57 §1.4)

Per DA/57: this blocks subscription-capable contracts from being
implementation-ready, but does **not** block the wave-1
`signal-core` + `sema-engine` core (`Request` / `Reply` /
`NonEmpty` / `Frame`) unless `signal-core` is going to own the
token type. Recommended status: *"explicitly deferred from wave 1
unless signal-core owns the type; required before migrating
Subscribe-capable contracts."*

The original observation stands as a future-design gap:

`/172 §3.1` shows:

```rust
reply MindReply {
    ...
    SubscriptionOpened(SubscriptionToken),
    ...
}
```

`/172 §4.1`'s two-phase subscription open names `SubscriptionToken`
as the payload of `SubReply` for opened subscriptions. But
`SubscriptionToken` is defined nowhere in `/172`, `/174`, or
`/175`. This is the same gap `/113 §13 Q3` flagged.

Implementation-wise the natural shape:

```rust
// signal-core/src/subscription.rs
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent,
         Debug, Clone, PartialEq, Eq)]
pub struct SubscriptionToken(u64);
```

…with a workspace-wide pattern of a `Retract
SubscriptionRetraction(SubscriptionToken)` variant on every
channel that supports subscription cancellation. But the user
should decide (a) the field type (u64 vs typed slot vs
content-hash), (b) whether it's per-channel typed vs
workspace-shared, (c) the retraction shape.

This is one of the three pending user decisions named in
`/113 §13`. It's still pending. None of the new reports closes
it.

---

## 5 · Implementation gate — superseded by DA/57 §3 + DA/56 §1.2

The canonical pre-implementation gate after this report's thread
landed is DA/57 §3 (six items, narrower than this report's
original eleven). DA/56 §1.2 supplies the concrete sema-engine
vocabulary the original `/116` + this report's first version both
left at directional language. The table below is preserved for
the lineage but is **not** the live gate. Per DA/57 §1.1 items 1
and 9 below are now settled in the live thread; item 8 is
deferred per DA/57 §1.4.

`/116 §"Suggested Implementation Gate"` names seven items the
operator wants settled before changing code. Per `/55 §1.2`,
several of these are now settled by `/175`. The adjusted gate
follows; status revised per DA/57:

| # | Item | Status |
|---|---|---|
| 1 | Confirm "six roots, no `Atomic` root" intended | **Settled per DA/57 §1.1** — `/172` and `/117` already treat six-root Signal as the active direction; the live question is now DA/56's sema-engine replacement names, not "six or seven." |
| 2 | Replace lowercase NOTA examples with PascalCase typed records | **Settled by `/175 §4`** — `(Batch (Anonymous \| Tracked \| Named) [ops])`. `/172 §6` + `/174 §5` still need the line-edit sweep but the direction is decided. |
| 3 | Remove four-parameter `Frame` examples | **Settled by `/175 §6.1`** — `/172 §3` line 103 and §10 line 754 already three-param; `/174 §1.2` and §5 also three-param. No remaining stale examples. |
| 4 | Replace `/175`'s invalid default-generic method signature | **Open** — `/116 §F` and `/55 §1.3` both call this out; `/175` needs a `validate_universal` + `validate_with_policy::<Policy>()` split (§3 above). |
| 5 | `SubReply` as a status enum carrying payloads directly | **Open** — `/116 §B`, `/55 §2`, and §2 above all recommend this; not yet in `/172` or `/175`. |
| 6 | Connect `BatchPolicy` to validation | **Settled by `/175 §2`** in direction (generic policy), but the Rust shape is item 4. |
| 7 | Define + test `NoIntent`'s rkyv/bytecheck/NOTA behavior | **Settled by `/175 §5`** in direction (derive unconditionally; rkyv-0.8 empirical check); not yet in code. |

Three items I add:

| # | Item | Per |
|---|---|---|
| 8 | Settle `SubscriptionToken` shape | **Wave-1-deferred per DA/57 §1.4** — not a wave-1 blocker unless signal-core owns the token type; required before migrating Subscribe-capable contracts. |
| 9 | Reconcile `RequestHeader<I>` (`/172`) vs `BatchHeaderShape<I>` (`/175`) — one name, one type | **Settled per DA/57 §1.2** — latest `/175 §4` main text uses `RequestHeader<Intent>` directly; only cleanup left in `/175 §0/§6.1`. |
| 10 | Specify `NonEmpty<T>`'s NOTA codec impl in signal-core | §4.1 above. |

And one from `/55 §1.4`:

| # | Item | Per |
|---|---|---|
| 11 | Enumerate the handshake/Reply break consequences | §6.2 below. `Reply<Payload>::Handshake` retires; every reply construction site changes. |

Open items per the post-DA/57 narrowed gate: 4 (legal Rust
validate API), 5 (`SubReply` typed enum), 10 (`NonEmpty<T>`
codec witnesses), 11 (handshake/Reply break enumeration), plus
DA/56 §1.2's *new* concrete-sema-engine-vocabulary gate item
(`WriteBatch` / `WriteOperation` / `CommitReceipt` /
`CommitLogEntry` replacement names — this report did not name
them). Items 1 and 9 are settled; item 8 is deferred.

Net active gate per DA/57 §3 (canonical):
1. Concrete sema-engine replacement vocabulary + log schema
   (DA/56 §1.2).
2. Legal `validate` / `validate_with_policy` Rust shape (now in
   `/172 §2` lines 587–658; needs propagation into `/175`).
3. `SubReply` typed enum promoted from recommendation to spec —
   choose `RolledBack`, `Invalidated`, or both (DA/56 §1.6;
   `/172 §1.6` already has it but worked example at `/172 §8.4`
   contradicts).
4. `RequestHeader<Intent>` owns the NOTA projection directly;
   remove stale `BatchHeaderShape` references.
5. `NonEmpty<T>` codec witnesses (tests + trait bounds), not a
   specific rkyv attribute.
6. Explicitly defer or specify `SubscriptionToken`.

All six settle in one designer pass per DA/57 §4.

---

## 6 · DA-`/55`'s wave-1 correction — sema-engine must move forward

### 6.1 · sema-engine cannot wait

`/116 §"Current Conflict Map"` proposes:

```
signal-core request/reply/frame primitives
  -> signal_channel! macro surface
  -> contract repos
  -> component receive paths
  -> sema-engine execution semantics
```

`/55 §1.1` corrects: **sema-engine must move into wave 1**
alongside signal-core, because dropping `SignalVerb::Atomic` from
`signal-core` immediately breaks `sema-engine`. Verified at
`/git/github.com/LiGoldragon/sema-engine/src/engine.rs:305,343` —
two sites write `signal_core::SignalVerb::Atomic` into the
operation log and into receipts. Once `signal-core` drops the
variant, those sites fail to compile.

The correct first slice:

```
1. signal-core (six roots, Request<P, I>, NonEmpty, NoIntent,
   BatchHeaderShape/RequestHeader unified, validate_universal +
   validate_with_policy, SubReply as typed enum, NoIntent codec)
   AND
   sema-engine (drop SignalVerb::Atomic usage; rename or
   reinterpret AtomicBatch as the normal commit batch;
   operation log records per-op verbs in one commit entry;
   subscriptions emit per-op deltas after batch commits)

2. signal-core + sema-engine tests:
   - six-root SignalVerb enum witness
   - no Atomic root compiles anywhere
   - mismatched verb rejected with original request recoverable
   - empty batch cannot construct / cannot bytecheck
   - subscribe-middle rejected
   - NoIntent cannot construct Named header
   - SubReply invalid states cannot construct
   - sema-engine batch commit writes no SignalVerb::Atomic

3. signal_channel! redesign (proc-macro): payload enums,
   intent enum or NoIntent alias, RequestPayload impl, kind
   enum, payload methods, type aliases, BatchPolicy impl,
   policy-aware validate emission

4. Per-channel contract sweep: every signal-persona-* crate's
   payload + reply enums moved to the new macro shape.
   MindOperationKind retires for MindRequestKind. Per-channel
   batch_policy blocks where wanted.

5. Daemon receive-path adoption: request.validate()? +
   request.validate_with_policy::<...>()? in each consumer.
   Two-phase staged subscription open in daemons that issue
   Subscribes.
```

Steps 1+2 are tightly coupled and ship together. Steps 3–5
stream after the kernel is stable.

### 6.2 · The handshake/Reply break

`/55 §1.4` notes a consequence `/116` underplayed: `/172 §2`
moves handshake variants exclusively to `FrameBody`, making
`Reply` batch-only:

```rust
pub enum Reply<ReplyPayload, Intent> {
    // No Handshake variant — handshakes live on FrameBody only.
    Batch { header, outcome, per_op },
}
```

But today's `signal-core::Reply<Payload>` (verified at
`/git/github.com/LiGoldragon/signal-core/src/reply.rs:6`) carries:

```rust
pub enum Reply<Payload> {
    Handshake(HandshakeReply),
    Operation(Payload),
}
```

Every existing reply construction site needs to change, not just
request construction. Consequences for operator pickup:

- `Reply::handshake(reply)` constructor goes away in `Reply`;
  handshake replies now build `FrameBody::HandshakeReply(reply)`
  directly.
- Every contract's reply path (currently `Reply::operation(payload)`)
  becomes `Reply::Batch { header, outcome, per_op }`.
- Every handshake round-trip test currently asserting `Reply::Handshake`
  shape is replaced by `FrameBody::HandshakeReply` shape.
- The same applies to current `Request<Payload>::Handshake` → moves
  to `FrameBody::HandshakeRequest`.

The cascade is mechanical but workspace-wide. Operator should
plan for it explicitly in step 1's scope, not discover it during
the per-channel sweep.

---

## 7 · Operator-lean — concurrence with `/116`, with `/55`'s wave-1 correction

The recommended path, post-`/55`:

1. **signal-core + sema-engine together (one wave).** Per §6.1.
2. **Universal validation + policy validation as two methods.**
   Per §3. `validate_universal()` + `validate_with_policy::<Policy>()`.
3. **Typed tests landed alongside the primitives.** Per §6.1.
4. **Then redesign `signal_channel!` (proc-macro).** Per `/174 §6`.
5. **Per-channel contract sweep.** Per `/175 §1.2`.
6. **Daemon receive-path adoption.** Per `/172 §4.1` (two-phase
   subscription open).
7. **Defer channel policy beyond declarative data until a real
   daemon needs it.** Per `/116 §"Operator Lean"`.

Each step has a clean witness; each step's output is consumable
by the next. The sema-engine pairing in step 1 is what saves the
core from a "signal-core won't compile against sema-engine" gap.

---

## 8 · Summary

`/175`, `/116`, and `/55` together cover almost all of what an
operator-assistant evaluation would surface. The substantive
items left to settle are:

- **`/175 §2.2`'s syntax bug** (default generic params on
  methods) — `/116 §F` and `/55 §1.3` flagged; needs a `/175`
  follow-up with the `validate_universal` +
  `validate_with_policy::<Policy>()` split.
- **`NonEmpty<T>` codec impls** — gate item 10. signal-core
  needs hand-written `NotaDecode for NonEmpty<T>`.
- **`RequestHeader<I>` (`/172`) vs `BatchHeaderShape<I>` (`/175`)
  naming** — gate item 9. Pick one; both name the same concept.
- **`SubscriptionToken` shape** — gate item 8; pending user
  decision since `/113 §13 Q3`.
- **`SubReply` typed enum** — gate item 5. `/116 §B` and
  `/55 §2` both recommend it; not yet adopted in `/172`.
- **Handshake/Reply break enumeration** — gate item 11.
  Workspace-wide cascade as `Reply::Handshake` retires.
- **Six-root vs seven-root spine** — gate item 1. The upstream
  user decision; sema-engine wave-1 dependency rides on it.

The verb spine, the batch model, the strict-ordered + RYOW
semantics, the two-phase subscription open, the constructor
discipline (RequestPayload default methods + BatchBuilder), the
declarative batch policy, the typed `BatchHeaderShape` NOTA
shape — all sound. Direction holds.

`/116`'s implementation gate is the right *kind* of pre-op
checklist; `/55 §1.2` correctly flags it as partially stale
after `/175`. The adjusted gate in §5 above is the current
shape. Ship the corrections in one designer pass, then operator
picks up the core (signal-core + sema-engine together; macro
after).

---

## 9 · See also

- `~/primary/reports/designer/172-typed-request-shape-and-execution-semantics.md` —
  the typed-shape spec; updated for 3-param Frame; NOTA
  examples (§6, §8) still need the sweep to `/175 §4`'s shape.
- `~/primary/reports/designer/174-signal-channel-macro-redesign.md` —
  macro redesign; not yet updated for `/175`'s corrections to
  `impl ChannelRequest` and `custom_check`.
- `~/primary/reports/designer/175-rust-shape-and-nota-syntax-corrections.md` —
  designer's settlement of DA's six findings; carries the
  default-generic-method syntax bug operator's `/116 §F` and
  DA's `/55 §1.3` both flagged.
- `~/primary/reports/operator/116-early-evaluation-typed-request-and-channel-macro.md` —
  operator's first evaluation; superseded by `/117`.
- `~/primary/reports/operator/117-post-175-signal-core-sema-engine-readiness.md` —
  operator's current position; supersedes `/116` with the
  sema-engine wave-1 correction; cites this report's three
  gates (NonEmpty codec, header-name unification,
  SubscriptionToken).
- `~/primary/reports/designer-assistant/56-review-operator-117-post-175-readiness.md` —
  DA's review of `/117`; names the concrete sema-engine
  replacement vocabulary (`WriteBatch`, `WriteOperation`,
  `CommitReceipt`, `CommitLogEntry`) that this report and
  `/117` left at directional language only.
- `~/primary/reports/designer-assistant/57-review-operator-assistant-114-typed-request-evaluation.md` —
  DA's review of this report; the corrections folded above
  (rkyv prescription too specific → witness-shaped; gate items
  1 and 9 settled; item 8 wave-1-deferred; canonical gate is
  DA/57 §3, not this report's §5).
- `~/primary/reports/designer-assistant/55-review-operator-116-typed-request-channel-macro.md` —
  DA's review of `/116`; this report folds in its four
  corrections (sema-engine wave-1 dependency, partial
  staleness of `/116`'s gate after `/175`, Rust sanity check
  on `/175`'s default-generic syntax, handshake/Reply
  break enumeration).
- `~/primary/reports/operator-assistant/113-persona-engine-audit-2026-05-14.md` —
  the prior audit; §13 Q3 names `SubscriptionToken` as a
  pending user decision; that pending status survives.
- `~/primary/skills/contract-repo.md` — `:125`, `:133-134` rule
  out validation pipelines in contracts; closes the
  `custom_check` argument.
- `~/primary/skills/language-design.md` — `:86` (no keywords)
  and `:110` (PascalCase head); closes the lowercase-NOTA
  argument.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs` —
  current single-op `Request<Payload>` shape.
- `/git/github.com/LiGoldragon/signal-core/src/reply.rs` —
  current `Reply<Payload>` with `Handshake` + `Operation`
  variants; the type that retires per `/172 §2`.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` —
  current `signal_channel!` macro_rules! form.
- `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:305,343` —
  the two sites writing `signal_core::SignalVerb::Atomic` that
  force sema-engine into wave 1 alongside signal-core.
