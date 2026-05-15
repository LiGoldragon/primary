# 115 — Context maintenance: typed Request thread end-state, 2026-05-15

## Scope

Hard context maintenance for the operator-assistant lane after the
typed-Request / `signal_channel!` thread converged on the
async-first frame-exchange shape. Captures the durable state so a
future operator-assistant session can pick up without rereading the
fifteen-report lineage from `/162`/`/166` onward.

This is a handover report. Repository state and the designer/operator/
designer-assistant reports listed below are the source of truth.

---

## Current canonical reports

| Report | Role | Status |
|---|---|---|
| `reports/designer/177-typed-request-shape-and-execution-semantics.md` | Designer spec for typed request semantics | Live, but `/177 §6 / §8` NOTA examples + `/177 §8.4` worked Reply still use pre-DA/60 shapes (lowercase intent heads, old `SubReply { status, payload }` struct, references to `RequestHeader`/`Intent`/`CorrelationId`). Awaits a designer pass to absorb DA/60. |
| `reports/designer/176-signal-channel-macro-redesign.md` | Designer spec for the `signal_channel!` macro | Live, but contains pre-`/175` shapes (illegal `impl ChannelRequest`, `custom_check`, `impl BatchPolicy for <RequestName>` on the payload enum, `with intent`/`intent { }` macro grammar, `single_tracked`/`single_named`/`batch_tracked` constructors). Awaits the same designer pass. |
| `reports/designer-assistant/61-signal-redesign-current-spec.md` | DA-side consolidated spec | **Current** — supersedes the DA chain `/50`–`/60`. Async-first frame-exchange shape with no `Intent`, no `CorrelationId`-in-payload, lane+sequence in handshake. |
| `reports/designer-assistant/62-signal-redesign-implementation-brief.md` | DA-side operator brief | **Current** — paired with DA/61. Names the signal-core target types, the connection runtime, what to remove. |
| `reports/operator/116-early-evaluation-typed-request-and-channel-macro.md` | Operator's first evaluation | Historical. Superseded by `/117`. |
| `reports/operator/117-post-175-signal-core-sema-engine-readiness.md` | Operator's wave-1 plan | Live for the wave-1 sequencing (signal-core + sema-engine together) and the legal `validate` / `validate_with_policy` API split, but its Frame shape now reads against DA/60 / DA/61. |
| `reports/operator-assistant/114-typed-request-shape-and-macro-redesign-evaluation.md` | This lane's third-party check on the thread | Historical confirmation. §0.0 banner already points readers to DA/57's gate; that gate is now further superseded by DA/61's spec. |
| `reports/operator-assistant/113-persona-engine-audit-2026-05-14.md` | The prior audit | The `SubscriptionToken` pending-user item from §13 Q3 is **now settled** per `/177 §7 Q5`: per-channel `<Channel>SubscriptionToken(SubscriptionTokenInner(u64))` newtype, per-channel `Retract SubscriptionRetraction(<Channel>SubscriptionToken)` variant. |

Designer's two context-maintenance commits (`a5f526b`, `523f568`)
retired reports `/160`, `/162`–`/175` (subset) and renumbered
`/172`→`/177`, `/174`→`/176`. The five preserved-and-current designer
reports in the typed-request chain are `/167`, `/176`, `/177`. DA-side
chain is `/55`–`/60` retired into `/61` + `/62`.

---

## What's settled

### Verb spine

Six elementary roots, no `Atomic`:

```rust
pub enum SignalVerb {
    Assert, Mutate, Retract, Match, Subscribe, Validate,
}
```

`Atomic` is structural: every request's `NonEmpty<Operation<Payload>>`
is the atomic unit. Settles `/166`'s collapse direction and the
seven-root → six-root migration.

### Request / Reply shape (per DA/60 + DA/61)

```rust
pub struct Operation<Payload> {
    pub verb: SignalVerb,
    pub payload: Payload,
}

pub struct Request<Payload> {
    pub operations: NonEmpty<Operation<Payload>>,
}

pub struct Reply<ReplyPayload> {
    pub outcome: RequestOutcome,
    pub per_operation: NonEmpty<SubReply<ReplyPayload>>,
}
```

Single type parameter. No `Intent` generic. No `RequestHeader`,
no `ReplyHeader`, no `CorrelationId` in payload.

### `SubReply` typed sum (per `/177 §1.6` and DA/56 §1.6)

```rust
pub enum SubReply<ReplyPayload> {
    Ok        { verb: SignalVerb, payload: ReplyPayload },
    RolledBack{ verb: SignalVerb },
    Failed    { verb: SignalVerb, reason: SubFailureReason,
                detail: Option<ReplyPayload> },
    Skipped   { verb: SignalVerb },
}
```

Illegal states are unrepresentable.

### Execution semantics (`/177 §1.4`, `§1.5`)

Strict-ordered execution with read-your-own-writes. No result
binding (no variables); conditional logic is expressed via
`Validate` ops with typed predicates or `expected_rev`
pre-conditions on `Mutate`. Subscribe-must-be-last is a universal
rule enforced in `Request::validate`.

### Frame exchange protocol (per DA/60 + DA/61 + DA/62)

Async from v1. Handshake negotiates `ExchangeMode::LaneSequence
{ session_epoch, connector_lane, acceptor_lane }`. Each side mints
outgoing requests on its own lane with a monotonic `ExchangeSequence`.
Replies echo the exact `ExchangeIdentifier`.

```rust
pub struct ExchangeIdentifier {
    pub session_epoch: SessionEpoch,
    pub lane: ExchangeLane,
    pub sequence: ExchangeSequence,
}

pub enum FrameBody<RequestPayload, ReplyPayload> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request { exchange: ExchangeIdentifier, request: Request<RequestPayload> },
    Reply   { exchange: ExchangeIdentifier, reply: Reply<ReplyPayload> },
}
```

`session_epoch` is implicit-in-connection-state (omittable from
each frame). Uniqueness key on the wire is `(lane, sequence)`;
durable cross-engine logs may extend to `engine_id + component_id
+ connection_instance + session_epoch + lane + sequence`.

### Validation API (per `/177 §2` + DA/56 §1.4)

Four explicit methods (Rust forbids default generic type params
on methods):

```rust
impl<P> Request<P> where P: RequestPayload {
    pub fn validate(&self) -> Result<(), BatchVerbMismatch>;
    pub fn validate_with_policy<Policy: BatchPolicy<P>>(&self)
        -> Result<(), BatchVerbMismatch>;
    pub fn into_checked(self)
        -> Result<CheckedRequest<P>, (BatchVerbMismatch, Self)>;
    pub fn into_checked_with_policy<Policy: BatchPolicy<P>>(self)
        -> Result<CheckedRequest<P>, (BatchVerbMismatch, Self)>;
}
```

`BatchPolicy<P>` is implemented on a per-channel **unit struct**
(e.g., `pub struct MindRequestPolicy; impl BatchPolicy<MindRequest> for ...`),
not on the request enum directly. Methods are associated functions
(no `self` receiver) since the policy is a type-level marker.

### `NonEmpty<T>` codec (per `/177 §2` doc comment + DA/57 §1.3)

- rkyv: witnesses, not a specific attribute. `ArchivedNonEmpty<T>`
  satisfies the `CheckBytes` bounds `Frame::decode` expects; the
  mandatory `head: T` field guarantees non-emptiness structurally.
- NOTA: hand-written `NotaDecode for NonEmpty<T>` in signal-core
  that consumes the sequence, errors on empty with
  `NotaCodecError::EmptyNonEmpty`, splits remainder into head + tail.
- Tests: archived request with valid head decodes; empty NOTA
  sequence is rejected.

### `SubscriptionToken` (per `/177 §7 Q5`, settled)

- Field type: opaque `u64` counter.
- Scope: per-channel typed — each contract declares
  `<Channel>SubscriptionToken(SubscriptionTokenInner)` newtype.
- Retraction shape: per-channel `Retract SubscriptionRetraction(<Channel>SubscriptionToken)`
  variant on every subscribe-supporting channel.
- `<Channel>SubscriptionOpened` reply payload carries
  `{ token, kind }`.

signal-core provides `SubscriptionTokenInner(u64)` as the
workspace-shared inner type; contracts wrap it.

### Macro user-settled questions (per `/176 §8`, all settled)

- Q1: operation-kind enum name = `<RequestName>Kind` (e.g. `MindRequestKind`).
- Q2: `batch_policy { }` field list deferred until the first
  concrete consumer needs it; default `DefaultPolicy` is permissive.
- Q3: `BatchBuilder::build() -> Result<_, BatchBuilderError>`.
  No panics on the wire-construction path.
- Q4: proc-macro migration in wave 2 (one operator pass, alongside
  the macro redesign).
- Q5: macro auto-emits `<EnumName>Kind` for the request enum and
  the intent enum (when intent block is present — though intent
  retires entirely per DA/60).

### What retires under DA/60

`RequestHeader<Intent>`, `ReplyHeader<Intent>`, `Intent` generic
everywhere, `NoIntent`, `CorrelationId` for request matching,
`MindBatchIntent` (and the `with intent` / `intent { }` macro
clauses), `BatchHeaderShape`, the `(Batch (Anonymous|Tracked|Named)
[ops])` NOTA wrapping shape, the `single_tracked` /
`single_named` / `batch_tracked` constructors. The
`/177 §5` `CommitLogEntry { intent, correlation, ... }` fields
also retire — sema-engine commit log becomes pure operations +
snapshot.

NOTA single-op is the bare verb-rooted expression
(`(Assert (SubmitThought ...))`); multi-op is the bracketed
sequence (`[(Retract ...) (Assert ...)]`). No frame header in the
human surface.

---

## What's open

### Sub-decisions in DA/60 still unsettled

1. **Cancellation frame.** No `CancelExchange { exchange: ExchangeIdentifier }`
   variant is specified. Three options: explicit `CancelExchange`
   variant; soft-cancel (sender drops, receiver runs anyway);
   connection close. Most pragmatic: explicit variant with the
   receiver returning `RequestOutcome::Cancelled`. Affects the
   `FrameBody` enum variant set.
2. **Stream-event topology.** Subscribe opens a stream; subsequent
   events aren't request/reply. Cleanest model: `FrameBody` grows
   a `StreamEvent { token: SubscriptionToken, event: StreamEventPayload }`
   variant, routed by token (not by `ExchangeIdentifier`). Brings
   the type parameter count to three again, or stream events get a
   separate envelope. DA/60 and DA/61 don't address it.
3. **`ExchangeSequence` type width.** `u64` (never wraps in practice)
   vs `u32` (wraps in seconds under heavy load). Recommend `u64`.

### Substantive residues in `/177` and `/176` (designer-pass items)

`/177`:

- §6 NOTA CLI examples (lines ~1008/1014/1020) still lowercase
  `(intent X)` form; sweep to bare-verb / bracketed-sequence per
  DA/60 §6.
- §6 closing prose (~1041–1043) describes the keyword form.
- §8.3 wire forms (~1253, 1257) still lowercase.
- §8.4 worked Reply example (~1297–1309) still uses old
  `SubReply { verb, status, payload }` struct shape with `status`
  field; replace with typed-sum variants.
- §8.4 line 1325 references retired `SubStatus`.
- §1.6 line 275 references "/172's draft shape" (stale name).
- §2 line 519 references "/174 §2.1" (should be /176).
- §2 line 557 references "/177 §55" (broken rename; should be DA-55).

`/176`:

- §3.1 line 303 lists retired `SubStatus`.
- §3.1 line 312 still describes NOTA grammar as `[(intent X) (correlation Y) ...]`.
- §4.2 keeps `custom_check`. §8 Q2 acknowledges drop but §4.2 text
  contradicts.
- §4.2 line 419 emits `impl BatchPolicy for MindRequest`; should
  be on a unit struct.
- §4.2 lines 420–424 use `&self` receivers; should be associated
  functions.
- §4.2 line 433 references single-method validate signature.
- §4.3 lines 449–475 illegal `impl ChannelRequest` on alias to
  foreign generic.
- §5.2 emissions #8 and #9 same illegal patterns.
- No mention of `SubscriptionToken` macro emissions or
  `Retract SubscriptionRetraction` workspace pattern.
- Under DA/60: entire `Intent`-related grammar and constructor surface
  retires beyond these issues.

Both reports need substantive rewrites, not line-edits, if DA/60
is accepted.

### Workspace-wide cascade

Per `/117 §"Handshake And Reply Break"` + `/177 §1.9`:

- `signal-core::Reply<Payload> { Handshake, Operation }` retires.
- Every existing reply construction site changes:
  - `Reply::handshake(reply)` → `FrameBody::HandshakeReply(reply)`.
  - `Reply::operation(payload)` → `Reply::Batch { ... }` (or the
    DA/60 successor shape).
  - `Request<Payload>::Handshake` → `FrameBody::HandshakeRequest`.
- sema-engine `engine.rs:305,343` currently writes
  `SignalVerb::Atomic`; these break the moment signal-core drops
  the variant. Wave 1 must move sema-engine with signal-core.

---

## Wave-1 plan (post-DA/60)

Per `/117 §"Corrected Implementation Order"` and DA/62 §1, adjusted
for async-first:

**Wave 1 — together:**

- `signal-core`:
  - Six-root `SignalVerb` (drop `Atomic`).
  - `Operation<Payload>`, `Request<Payload>`, `NonEmpty<T>` with
    rkyv + NOTA codec.
  - `Reply<ReplyPayload>` (`RequestOutcome` + `NonEmpty<SubReply>`).
  - Typed `SubReply` sum.
  - `RequestOutcome` (renamed from `BatchOutcome`), `BatchFailureReason`,
    `SubFailureReason`.
  - `BatchPolicy<P>` trait + `DefaultPolicy` unit struct.
  - Four-method validate / into_checked API.
  - `CheckedRequest<P>`, `BatchVerbMismatch`.
  - `RequestPayload` trait (`signal_verb()`, `is_subscribe()`).
  - `BatchBuilder<P>` with `build() -> Result<_, BatchBuilderError>`.
  - `ExchangeLane`, `ExchangeSequence`, `SessionEpoch`,
    `ExchangeIdentifier`, `ExchangeMode`, `ExchangeHandshake`.
  - `Frame<Req, Rep>` + `FrameBody<Req, Rep>` two-parameter.
  - `SubscriptionTokenInner(u64)`.
  - Connection runtime: pending-exchange map, lane bookkeeping,
    handshake negotiation.
- `sema-engine`:
  - Remove `SignalVerb::Atomic` usage at `engine.rs:305,343`.
  - Rename `AtomicBatch` → `WriteBatch` (or designer's chosen name
    per DA/56 §1.2).
  - `OperationLogEntry` schema change: drop top-level `SignalVerb`;
    one `SnapshotId` + `NonEmpty<CommitLogOperation>`; per-op verb
    is `Assert`/`Mutate`/`Retract` only.
  - `AtomicReceipt` → `CommitReceipt`.
  - `Engine::atomic` → `Engine::commit` (or named per designer).

**Wave-1 witnesses** (per DA/62 §6, supplemented):

- Six-root `SignalVerb` enum; no `Atomic` compiles anywhere.
- `Request` cannot be empty (NonEmpty type-enforced).
- Mismatched verb rejected with original request recoverable
  (the `(BatchVerbMismatch, Self)` error tuple).
- Subscribe-in-middle rejected as `SubscribeOutOfOrder`.
- Empty NOTA sequence rejected with `EmptyNonEmpty`.
- `NoIntent` cannot construct (it retires per DA/60; no test needed).
- `SubReply` invalid states cannot construct (typed-sum).
- sema-engine batch commit writes no `SignalVerb::Atomic`.
- Reply `Handshake` variant no longer exists.
- **Async witness:** two requests in flight on one connection
  receive replies out of order and resolve to the correct pending
  exchange (DA/60 §9 item 10).
- Handshake negotiates `ExchangeMode::LaneSequence`; peer rejects
  requests on the wrong lane.

**Wave 2:** macro redesign (proc-macro, alongside the redesign per
`/176 §8 Q4`), per-channel contract sweep, daemon receive-path
adoption with `validate_with_policy::<MindRequestPolicy>()`.

---

## Dirty workspace warning

At the time of writing, working copy is dirty from concurrent
designer / designer-assistant / operator activity:

- `D reports/designer/172-typed-request-shape-and-execution-semantics.md`
- `D reports/designer/174-signal-channel-macro-redesign.md`
- `M reports/designer/177-typed-request-shape-and-execution-semantics.md`
- `D reports/designer-assistant/50-…-54-…` (consolidated by DA/61, DA/62)
- `A reports/designer-assistant/61-signal-redesign-current-spec.md`
- `A reports/designer-assistant/62-signal-redesign-implementation-brief.md`
- Plus pre-existing unrelated dirty files
  (`.claude/scheduled_tasks.lock`, `primary.code-workspace`,
  `system-assistant.lock`).

This report commits **only** its own file at
`reports/operator-assistant/115-context-maintenance-typed-request-thread-2026-05-15.md`
via explicit-path commit. Other lanes' uncommitted changes are not
bundled.

---

## Next session targets (operator-assistant lane)

1. Read DA/61 and DA/62 before any work in this lane — they are the
   live spec.
2. If a designer pass has absorbed DA/60 into `/177` and `/176`,
   read the post-absorption shapes before referencing the residues
   listed in §"What's open" above (they may be fixed).
3. If operator picks up wave-1 implementation, the operator-assistant
   role is audit: per `skills/operator-assistant.md`, default
   shape on high-risk paths (`signal-core`, sema-engine) is
   operator first pass, operator-assistant review. Check witnesses,
   architectural-truth tests, no string dispatch where closed enum
   belongs, contract-repo discipline.
4. The first operator-assistant audit target after wave-1 lands
   should be the async-witness test from DA/62 §6 / DA/60 §9 item 10:
   verify the two-requests-out-of-order resolution actually works
   end-to-end, since async-from-v1 is the largest architectural
   change in this thread.
5. Coordinate with system-assistant if the wave-1 work touches
   deployment surfaces — they currently hold the `horizon-re-engineering`
   step-6 lane and won't release until that lands.

---

## Pointers for the next agent

| If you need… | Read |
|---|---|
| The current signal-core protocol shape | `reports/designer-assistant/61-signal-redesign-current-spec.md` |
| The operator implementation brief | `reports/designer-assistant/62-signal-redesign-implementation-brief.md` |
| The execution semantics + composition rules | `reports/designer/177-typed-request-shape-and-execution-semantics.md §1–§5` (skip the still-stale §6/§8 examples) |
| Wave sequencing + sema-engine pairing | `reports/operator/117-post-175-signal-core-sema-engine-readiness.md` |
| Why `Intent` and `CorrelationId` retired | `reports/designer-assistant/59-frame-metadata-and-correlation-correction.md` + `60-async-first-signal-exchange-protocol.md` |
| The full lineage (historical) | `reports/operator-assistant/114-…-evaluation.md §0.0` banner |
| The `SubscriptionToken` settlement | `reports/designer/177-…-execution-semantics.md §7 Q5` |

Workspace skills relevant to this lane: `skills/operator-assistant.md`,
`skills/contract-repo.md` (rules out `custom_check`),
`skills/language-design.md` (rules out lowercase NOTA heads),
`skills/typed-records-over-flags.md` (rules out the old
`SubReply { status, payload: Option }` shape).
