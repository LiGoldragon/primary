# 172 — Typed `Request<Payload, Intent>`, closed intents, and execution semantics

*Designer follow-up, 2026-05-15. Responds to DA's critique of `/171`.
All six findings are correct on the design level — none are migration
concerns. Settles the open type-shape and semantic-precision questions
that prevented `/171` from being implementation-ready. Becomes the
spec of record; `/171 §4` is superseded by the present report's §3–§7.
The verb spine remains six elementary verbs (Assert / Mutate /
Retract / Match / Subscribe / Validate), no `Atomic`; frames are
operation-batches with a consistency boundary.*

**Retires when**: the operator picks up implementation; the spec
absorbs into `signal-core/ARCHITECTURE.md`.

---

## 0 · TL;DR

DA's six findings on `/171`:

1. `Request<P>` typing doesn't match per-domain `BatchIntent`. Either
   make Request generic over both, or move intent into the payload.
2. `Custom(String)` in the intent enum violates closed-boundary
   discipline.
3. "Frame is the commit boundary" is too absolute — pure Match,
   Validate, or Subscribe frames don't commit.
4. Mixed-Validate semantics contradict operation-ordering — `/171`
   says both "strict ordered" and "phased."
5. Mixed Match + writes is ambiguous — pre-write / post-write /
   read-your-own-writes are different.
6. `BatchOutcome::Committed` doesn't fit non-write frames; the names
   should describe completion, not only commit.

All six are real. The settlements:

1. **`Request<Payload, Intent>`** generic over two type parameters.
   Each contract's macro invocation supplies its concrete types.
2. **No `Custom(String)`.** Intent enums are closed. Adding a new
   intent is a coordinated contract-version bump, same discipline as
   adding a request variant.
3. **The frame is an *operation batch* and a *consistency
   boundary*.** Writes inside it commit atomically; reads inside it
   observe one snapshot; subscribes inside it open at the snapshot.
   "Commit boundary" applies to the write subset only.
4. **Strict ordered execution.** Each op sees the cumulative effects
   of all prior ops in the same frame. This is more expressive than
   phased (preflight patterns work by putting Validates first;
   checkpoint patterns work by putting Validates after writes).
5. **Read-your-own-writes.** Each Match (and each later Mutate) sees
   the cumulative state including effects of prior ops in the same
   frame. No result binding (no variables); conditional writes use
   the existing `expected_rev` pre-condition pattern.
6. **`BatchOutcome::Completed` / `Aborted`.** Names describe
   completion; outcome works for any frame shape. Per-op replies
   carry the verb-specific result.

The corrected design is the `signal-core` and `Request`/`Reply` spec
of §3–§7 below. `/171`'s recommendation (the collapse) stands; the
shape is now precise enough to implement.

---

## 1 · The findings, taken in order

### 1.1 · `BatchIntent` can't live in `signal-core` ✓

`/171 §4` wrote:

```rust
pub struct Request<P> {
    pub intent: Option<BatchIntent>,
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<Op<P>>,
}
```

…and then said `BatchIntent` is per-domain. But `signal-core` doesn't
know domain-specific intent enums. The shape doesn't typecheck. Fix:
generic over both:

```rust
// signal-core
pub struct Request<Payload, Intent> {
    pub intent: Option<Intent>,
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<Op<Payload>>,
}
```

Each contract's `signal_channel!` invocation supplies concrete types:

```rust
// signal-persona-mind
signal_channel! {
    request MindRequest with intent MindBatchIntent {
        Assert SubmitThought(SubmitThought),
        Mutate StatusChange(StatusChange),
        // ...
    }
}

// Macro emits:
pub type MindFrame = Frame<MindRequest, MindBatchIntent, MindReply, MindBatchIntent>;
```

The intent type is part of the channel's typed identity, exactly
like the request payload enum.

### 1.2 · `Custom(String)` is a closed-boundary violation ✓

`/171 §4` ended the example intent enum with:

```rust
pub enum MindBatchIntent {
    RoleHandoff(...),
    SchemaUpgrade(...),
    ChannelMigration(...),
    Custom(String),    // ← violates closed-boundary discipline
}
```

`Custom(String)` is the same shape as the `Unknown` variant `/163`
rules out — an open escape hatch that makes the enum no-longer-closed
and the audit-trail no-longer-typed. Either an intent matters (so
it's a closed variant) or it doesn't matter (so the frame goes
without an intent, `intent: None`).

Fix:

```rust
pub enum MindBatchIntent {
    RoleHandoff,
    SchemaUpgrade,
    ChannelMigration,
    // No Custom. Adding a new intent is a coordinated contract bump.
}
```

This matches the discipline used for the request payload variants
themselves. The intent enum participates in the same versioning
contract as the variant enum.

### 1.3 · "Commit boundary" overstates ✓

`/171` claimed "the frame IS the commit boundary" universally. But:

- A frame of only `Match` ops does not commit; it reads at a snapshot.
- A frame of only `Subscribe` ops does not commit; it opens streams.
- A frame of only `Validate` ops does not commit; it dry-runs.

These frames are still bounded — they share a snapshot, they reply
together — but they don't commit. The honest framing:

> The frame is an **operation batch** and a **consistency
> boundary**. All ops within the frame share one snapshot. Write
> effects inside the batch commit atomically when the batch contains
> writes. Read effects observe the shared snapshot. Subscribe
> effects open at the post-commit snapshot (or, if no writes, the
> shared snapshot). Validate effects dry-run against the shared
> snapshot (including any prior writes in the same batch).

This is precise. "Commit boundary" applies to the write subset, not
to the frame as a whole.

### 1.4 · Ordered vs phased execution — pick one ✓

`/171` said both:

- "Within an atomic boundary, operations execute in order, with each
  seeing the effects of previous operations in the same boundary"
  (strict ordered, §1.3)
- "Mixed validate + writes: validates run first; if any fails, no
  writes commit. If all validates pass, writes commit atomically."
  (phased, §4.1 table)

These are different models. The strict-ordered model is more
expressive (you can validate intermediate states); the phased model
is simpler.

Settlement: **strict ordered execution**.

```text
- Ops execute in declared order.
- Each op observes the cumulative effects of all prior ops in the
  same batch.
- A Validate at position N checks invariants against state including
  prior writes at positions 1..N-1.
- A Mutate at position N+1 reads the state including writes at
  positions 1..N (read-your-own-writes).
- Failure of any op at position K rolls back writes at positions
  1..K-1; ops at positions K+1..N are skipped (SubStatus::Skipped).
```

Both useful patterns work in this model:

- **Preflight pattern**: put Validates first.
  `[Validate Constraint, Assert RecordA, Assert RecordB]` — if
  validation fails (position 0), no writes execute.
- **Checkpoint pattern**: put Validates after writes.
  `[Mutate Catalog→Migrating, Mutate Row1, Validate Integrity,
  Mutate Catalog→Active]` — the Validate at position 2 sees the
  effects of prior Mutates.

Strict-ordered covers both. Phased only covers the first.

This matches Datomic's `d/with` and SQL's transaction semantics: each
statement sees the cumulative effect of prior statements in the same
transaction.

### 1.5 · Mixed Match + writes — pick semantics ✓

DA's three possibilities:

- **Pre-write snapshot**: reads see state *before* writes in the
  batch.
- **Post-write snapshot**: reads see state *after* all writes commit.
- **Read-your-own-writes**: each read sees the cumulative state
  including prior ops in the batch.

Settlement: **read-your-own-writes** (RYOW), as a direct consequence
of §1.4's strict-ordered execution. Each Match at position N sees:

- The pre-batch snapshot, PLUS
- The cumulative effects of any writes at positions 1..N-1 within the
  same batch.

This is the natural reading of strict-ordered + atomic-write-commit:
the batch is one transaction; within it, each op sees the
transaction's accumulated state.

**Result binding** — using the value from a Match in a later Mutate
— is **not** supported. Frames are not procedural in the
variable-binding sense. Each op's payload is self-contained. If a
later op needs to react conditionally to a prior op's result, the
agent uses:

- **The expected-state pre-condition pattern** (per
  `sema-engine::MutateOperation`'s existing `expected_rev` field):
  the Mutate carries a pre-condition; if state changed, the Mutate
  fails and the batch aborts.
- **A separate Validate op** that fails when a condition isn't met:
  `[Match X, Validate (assert X.value > 5), Mutate ...]` — the
  Validate checks the condition; failure aborts the batch.

This is cleaner than result binding for two reasons. (a) No need to
extend the wire grammar with variables. (b) The
constraint-check-and-mutate logic stays expressible via existing
typed records, not via a new procedural sub-language.

### 1.6 · Reply outcome names — completion, not commit ✓ (with the refinement from DA's second round below)

`/171` had `BatchOutcome::Committed` which doesn't fit pure
Match/Validate/Subscribe frames. Fix:

```rust
pub enum BatchOutcome {
    /// All ops completed successfully. For writes: committed.
    /// For reads: observed the snapshot. For validates: passed.
    /// For subscribes: opened. For mixed: each op completed in
    /// its mode.
    Completed,

    /// An op at the given position failed; the batch was aborted.
    /// Writes that would have committed did not. Subscribes that
    /// would have opened did not. Per-op replies say which is which.
    Aborted {
        failed_at: usize,
        reason: BatchFailureReason,
    },
}
```

Per-op detail lives in the `SubReply`:

```rust
pub struct SubReply<ReplyPayload> {
    pub verb: SignalVerb,         // echoed from request
    pub status: SubStatus,
    pub payload: Option<ReplyPayload>,
}

pub enum SubStatus {
    /// Op completed successfully. Payload carries the per-verb result.
    Ok,
    /// Op was not attempted because an earlier op in the batch failed.
    Skipped,
    /// Op was attempted and failed.
    Failed(SubFailureReason),
}
```

`Completed` + `Ok` per op = clean reads / clean writes / clean
subscribes / clean validates.

`Aborted` + per-op `Skipped`/`Failed` = the failure case, with the
exact position and reason recorded.

---

### 1.7 · DA's second round (after a draft of this report)

After §1.1–§1.6 were drafted, DA reviewed the draft and flagged five
further design issues. All five are folded into the spec below; the
findings are restated here for completeness:

- **Subscription batching coherence** — subscribes are external
  ongoing side effects; rolling back a stream-open is awkward. The
  spec now requires Subscribes to come last in a batch (per §4
  composition rules and §8.1 worked example). A Subscribe in the
  middle of a batch is rejected at receive-time as
  `BatchFailureReason::SubscribeOutOfOrder`.
- **Aborted-batch speculative-read leak** — read-your-own-writes
  with strict ordering means a Match can observe writes that later
  get rolled back. The spec now requires `Status::RolledBack` to
  cover both rolled-back writes *and* invalidated reads, with
  `payload: None` in both cases (per §1.6's refined SubStatus and
  its invariants block).
- **Non-empty batch invariant** — `Vec<Op>` allows empty batches
  with no semantics. The spec now uses `NonEmpty<Op>` to encode
  non-emptiness at the type level (per §2's signal-core block).
- **No-result-binding example contradiction** — `/171 §6`'s example
  used a Match's result in a later Mutate's pre-condition, silently
  violating the no-result-binding rule. Fixed in §6 — the Match is
  for the caller's read; the Mutate's pre-condition is self-contained;
  the conditional logic lives in a Validate that runs its own typed
  predicate.
- **Handshake duplication** — `/171` put handshake variants on both
  FrameBody and Reply. The spec now keeps them on FrameBody only;
  `Reply` has no Handshake variant (per §2's signal-core block).

All five settlements are structural; none should change the
implementation work an operator picks up from this spec.

---

## 2 · The corrected design — `signal-core` primitives

```rust
// signal-core/src/request.rs

pub enum SignalVerb {
    Assert,
    Mutate,
    Retract,
    Match,
    Subscribe,
    Validate,
    // No Atomic. Atomicity is structural to every batch.
}

/// A non-empty sequence — guaranteed at the type level to hold at
/// least one element. Empty batches have no semantics; the type
/// rules them out at construction.
pub struct NonEmpty<T> {
    head: T,
    tail: Vec<T>,
}

pub struct Request<Payload, Intent> {
    pub header: RequestHeader<Intent>,
    pub ops: NonEmpty<Op<Payload>>,
}

/// The request header carries the closed-set of valid (intent,
/// correlation) combinations. Named frames (with an intent) require
/// a correlation id; anonymous and tracked frames do not.
pub enum RequestHeader<Intent> {
    /// No audit metadata. Most one-shot reads, single-op writes.
    Anonymous,

    /// Correlation id only; no named intent. Used for follow-up frames
    /// that continue a tracked conversation.
    Tracked { correlation: CorrelationId },

    /// Named intent with correlation. Used for batches whose audit
    /// meaning matters (RoleHandoff, SchemaUpgrade, etc.).
    Named { intent: Intent, correlation: CorrelationId },
}

pub struct Op<Payload> {
    pub verb: SignalVerb,
    pub payload: Payload,
}

// Frame envelope owns the handshake variants exclusively — Reply has
// no Handshake variant (per `/172 §1.5` settling DA's "handshake is
// duplicated" finding).
pub enum FrameBody<RequestPayload, RequestIntent, ReplyPayload, ReplyIntent> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request(Request<RequestPayload, RequestIntent>),
    Reply(Reply<ReplyPayload, ReplyIntent>),
}
```

```rust
// signal-core/src/reply.rs

pub enum Reply<ReplyPayload, Intent> {
    // No Handshake variant — handshakes live on FrameBody only.
    Batch {
        header: ReplyHeader<Intent>,
        outcome: BatchOutcome,
        per_op: Vec<SubReply<ReplyPayload>>,
    },
}

/// Reply header echoes the request's header shape.
pub enum ReplyHeader<Intent> {
    Anonymous,
    Tracked { correlation: CorrelationId },
    Named { intent: Intent, correlation: CorrelationId },
}

pub enum BatchOutcome {
    Completed,
    Aborted {
        failed_at: usize,
        reason: BatchFailureReason,
    },
}

pub struct SubReply<ReplyPayload> {
    pub verb: SignalVerb,
    pub status: SubStatus,
    pub payload: Option<ReplyPayload>,
}

pub enum SubStatus {
    /// Op ran and committed/completed. Payload carries the result.
    /// Only set when the entire batch reached `BatchOutcome::Completed`.
    Ok,

    /// Op ran inside a batch that subsequently aborted. For writes: any
    /// durable effects were rolled back. For reads or validates that
    /// ran: their result may have observed speculative state that did
    /// not commit; the result is no longer authoritative. **Payload is
    /// always `None`** — the caller should re-issue if it still wants
    /// the value.
    RolledBack,

    /// Op was attempted and failed; this is the cause of the batch
    /// abort. Exactly one op per aborted batch has this status, at
    /// `BatchOutcome::Aborted::failed_at`.
    Failed(SubFailureReason),

    /// Op was never attempted because an earlier op in the batch
    /// failed. Payload is always `None`.
    Skipped,
}

// Status invariants:
//
// - BatchOutcome::Completed ⇒ every SubReply.status == Ok and
//   SubReply.payload == Some(result).
// - BatchOutcome::Aborted { failed_at, .. } ⇒
//     * positions 0..failed_at have status RolledBack, payload None.
//     * position failed_at has status Failed(reason).
//     * positions failed_at+1..n have status Skipped, payload None.
// - Status::Ok ⟺ payload is Some.
// - Status::RolledBack | Skipped ⇒ payload is None.
// - Status::Failed(_) → payload may be Some (with failure detail) or
//   None depending on the per-verb failure convention.

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum BatchFailureReason {
    /// The op at `failed_at` was rejected by the receiver.
    OpRejected,
    /// The batch violated a receiver-policy rule (e.g. mixed-with-Subscribe).
    PolicyViolation,
    /// The batch failed a Validate op at `failed_at`.
    ValidationFailed,
    /// A receiver-internal error.
    Internal,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum SubFailureReason {
    /// The verb/payload mismatch caught at receive time.
    SignalVerbMismatch,
    /// The op's pre-condition (expected_rev, etc.) failed.
    PreconditionFailed,
    /// The validation rule the op was checking did not hold.
    ValidationFailed,
    /// Domain-specific failure; receiver-side detail in the payload.
    DomainRejection,
}
```

---

## 3 · The corrected design — `signal_channel!` macro

The macro grows to accept an `intent` declaration alongside the
request/reply enums:

```rust
signal_channel! {
    request MindRequest with intent MindBatchIntent {
        Assert SubmitThought(SubmitThought),
        Mutate StatusChange(StatusChange),
        Retract RoleRelease(RoleRelease),
        Match QueryThoughts(QueryThoughts),
        Subscribe SubscribeThoughts(SubscribeSpec),
        Validate ValidateProposal(Proposal),
    }
    reply MindReply {
        Thought(ThoughtSummary),
        Status(ActivityAck),
        Released(RoleReleaseAck),
        ThoughtList(Vec<Thought>),
        SubscriptionOpened(SubscriptionToken),
        ValidationPassed(ValidationReceipt),
        // Plus per-domain failure variants if the channel needs them.
    }
    intent MindBatchIntent {
        RoleHandoff,
        SchemaUpgrade,
        ChannelMigration,
    }
}
```

Macro emissions:

- The `MindRequest` and `MindReply` payload enums (as today).
- The `MindBatchIntent` enum.
- Per-variant `SignalVerb` mappings (as today).
- `pub type MindFrame = Frame<MindRequest, MindBatchIntent, MindReply, MindBatchIntent>;`
  — though intent type can differ for request vs reply; usually
  the same.
- Per-channel constructor helpers for both single-op and batched
  frames.
- The NOTA codec impls (with the new bracketed `[...]` form for
  batches).

The intent enum participates in the same compile-time discipline as
the request enum: adding a variant is a coordinated contract bump;
no `Custom(String)` escape hatch.

---

## 4 · Composition rules (now precise)

Strict-ordered execution + read-your-own-writes gives clean
semantics for every verb mix:

| Frame contents | Behaviour |
|---|---|
| All Assert/Mutate/Retract (pure writes) | All-or-nothing atomic commit. Each write sees prior writes' effects. First failure aborts at `failed_at`; subsequent ops are `Skipped`. |
| All Match (pure reads) | All reads observe one shared snapshot. Failure of one op aborts; others are `Skipped`. |
| All Subscribe | All Subscribes open at the shared snapshot. First failure aborts the batch and no streams open. |
| All Validate | All validates dry-run against the shared snapshot. First failure aborts. |
| Validate + writes | Strict-ordered: a Validate at position N sees the cumulative state including writes at 1..N-1. The preflight pattern (Validates first) works; the checkpoint pattern (Validates after writes) also works. |
| Match + writes | Strict-ordered: a Match at position N reads cumulative state including writes at 1..N-1. The SQL `SELECT FOR UPDATE` pattern works; result binding (using a Match's result in a later op) does not — see §5 and §10.4 below. |
| Subscribe + any non-Subscribe op | **Subscribes must come last in the batch.** All non-Subscribe ops execute first in strict order; if any fails, the batch aborts and no streams open. If all succeed, writes commit and subscribes open at the post-commit snapshot. A Subscribe in the middle of a batch is rejected at receive-time as `BatchFailureReason::SubscribeOutOfOrder`. |

The "Subscribe + writes forbidden" policy is per-receiver; a domain
that has a clean semantics for it can override.

---

## 5 · Sema-engine commit-log shape (corrected)

Today: one `OperationLogEntry { snapshot, verb: SignalVerb::Atomic,
table, .. }` per atomic batch. After collapse:

```rust
pub struct CommitLogEntry {
    pub snapshot: SnapshotId,
    pub intent: Option<SerializedIntent>,    // serialized typed intent for cross-domain audit
    pub correlation: Option<CorrelationId>,
    pub op_count: usize,
    pub ops: Vec<OpLogDetail>,
}

pub struct OpLogDetail {
    pub verb: SignalVerb,                    // per-op
    pub table: TableName,
    pub effect: DeltaKind,                   // Assert / Mutate / Retract (Match/Subscribe/Validate don't write)
    pub key: SerializedKey,
}
```

The log is now richer than today — every batch shows its intent and
per-op detail. Audit queries reconstruct the logical transaction.

Two flavors of log entry exist:

- **Write-bearing entries** (`CommitLogEntry` above) — for batches
  that committed at least one write.
- **Read/subscribe/validate-only entries** — for batches that didn't
  commit. These can be omitted from the durable log entirely
  (they're not durable state changes), or kept in a separate
  read-audit log if read-trace is needed.

Default: only commit-bearing batches are durably logged.

---

## 6 · CLI surface (the NOTA grammar)

Bracketed-sequence form for batches; bare form as ergonomic
shorthand for length-1:

```sh
# Bare single-op (sugar for length-1 batch):
mind '(Assert (SubmitThought (...)))'

# Explicit batch (length-N):
mind '[(Mutate (Catalog (...)))
       (Mutate (Row (...)))
       (Mutate (Catalog (status Active)))]'

# Batch with intent:
mind '[(intent SchemaUpgrade)
       (Mutate (Catalog (status Migrating)))
       (Mutate (Row (...)))
       (Mutate (Catalog (status Active)))]'

# Strict-ordered with preflight Validate:
mind '[(intent RoleHandoff)
       (Validate (RoleHandoff (from designer) (to poet)))
       (Retract (RoleClaim (role designer)))
       (Assert (RoleClaim (role poet)))]'

# Strict-ordered with checkpoint Validate (sees post-Mutate state):
mind '[(intent SchemaUpgrade)
       (Mutate (Catalog (status Migrating)))
       (Mutate (Row (...)))
       (Validate (Integrity (table thoughts)))
       (Mutate (Catalog (status Active)))]'

# Mixed Match + write — Match is for caller's read access; the Mutate's
# pre-condition is SELF-CONTAINED (does NOT reference the Match's
# result). No result binding; each op's payload carries its own
# inputs.
mind '[(Match (ClaimSnapshot (role designer)))                ; for caller's read
       (Validate (ExpectedRevision (table claims) (key designer) (revision 5)))
       (Mutate (RoleClaim (role designer) (expected_rev 5) (...)))]'

# If the agent wants to *act conditionally* on a value, the conditional
# is expressed as a Validate with its own typed predicate. The Validate
# re-runs the read against the shared transactional state; on failure,
# the batch aborts. The Mutate that follows is unconditional from its
# own perspective — it just trusts the Validate's promise.
```

The NOTA grammar gains the bracketed-sequence form `[ op op ... ]`.
The `intent` and `correlation` annotations live at frame-head
position; they parse before the ops.

---

## 7 · What's still open

The present spec settles most of `/171`'s open questions. What
remains:

### Q1 — Per-receiver batch policy overrides

The default policy of §4 covers the common cases. A contract that
needs stricter rules (e.g., refusing mixed read+write because its
storage backend can't serve consistent reads) declares so in its
`signal_channel!` invocation. Macro syntax for batch-policy
overrides is not yet specified.

### Q2 — Frame-size limits

How many ops per batch? How many bytes per frame? Defaults likely
~256 ops per batch and ~1 MiB per frame, with per-receiver overrides
via batch policy.

### Q3 — Cross-component sequences

A frame targets one component. Cross-component logical transactions
(e.g., a `persona-router` channel-grant linked to a `persona-mind`
adjudication record) happen as separate frames coordinated through
mind adjudication. Same answer as today; restated.

### Q4 — Correlation ID lifecycle

A correlation id is generated at the originating frame; echoed in
all replies; carried in follow-up frames that logically continue the
same conversation. TTL-based garbage collection. Spec doesn't pin
down details beyond the generation/echo rule.

---

## 8 · Worked examples for the four `/171 §8` open questions

The user's earlier four open questions land cleanly under the
present spec. Each is shown concretely.

### 8.1 · `/171 Q1` — Subscribe-in-batch policy (now: Subscribes must be last)

```sh
# Allowed: Subscribe-only batch
mind '[(Subscribe (ThoughtFilter (kind Decision)))
       (Subscribe (RoleFilter (role designer)))]'
# Both subscribes open at the shared snapshot. SubReply carries
# SubscriptionToken per op.

# Allowed: non-Subscribe ops followed by Subscribes
mind '[(Mutate (Catalog (table thoughts) (status Active)))
       (Subscribe (ThoughtFilter (kind Decision)))]'
# Mutate executes first; if it commits, Subscribe opens at post-commit
# snapshot. If Mutate fails, Subscribe never opens, batch aborts.

# Rejected at receive: Subscribe in the middle
mind '[(Subscribe (ThoughtFilter (...)))
       (Assert (SubmitThought (...)))]'
# → Reply::Batch {
#     outcome: Aborted { failed_at: 0, reason: SubscribeOutOfOrder },
#     ...
#   }
```

Rationale: a subscription is an external ongoing side-effect (the
client now has an open stream); if a later op fails, the spec must
either roll back the stream-open (awkward — the client may have
already received events) or keep it open despite the batch failure
(also awkward — the audit record says the batch aborted, but the
side-effect persists). Forcing Subscribes to the end of the batch
collapses both edge cases into "subscribes only open after everything
else succeeds." Clean.

### 8.2 · `/171 Q2` — `BatchIntent` per-contract via the generic

Each contract owns its own intent enum, scoped through the
`Request<Payload, Intent>` generic:

```rust
// signal-persona-mind:
signal_channel! {
    request MindRequest with intent MindBatchIntent {
        Assert SubmitThought(SubmitThought),
        // ...
    }
    intent MindBatchIntent {
        RoleHandoff,
        SchemaUpgrade,
        ChannelMigration,
    }
}

// signal-persona-message:
signal_channel! {
    request MessageRequest with intent MessageBatchIntent {
        Assert MessageSubmission(MessageSubmission),
        Mutate MessageMarkRead(MarkRead),
        // ...
    }
    intent MessageBatchIntent {
        BulkSubmission,
        ConversationClose,
    }
}
```

Cross-contract intents are not allowed at the type level —
`signal-persona-mind` cannot use `MessageBatchIntent`. If a workspace
needs cross-contract audit (e.g., "this schema upgrade spanned mind
and sema-engine"), it lives at the orchestration layer (correlation
ids linking frames across contracts), not at a global intent enum.

### 8.3 · `/171 Q3` — Correlation required when intent is set (now: type-enforced)

The `RequestHeader::Named` variant bundles intent + correlation; the
type system rejects an intent without a correlation:

```rust
// Allowed shapes:
RequestHeader::Anonymous                                                     // no audit
RequestHeader::Tracked { correlation: cor_abc }                              // tracked only
RequestHeader::Named { intent: RoleHandoff, correlation: cor_abc }           // both

// Disallowed at the type level — no `Named { intent: X }` variant
// exists without correlation. The bad shape cannot be constructed.
```

NOTA wire forms:

```sh
# Anonymous:
mind '(Assert (SubmitThought (...)))'

# Tracked (correlation only):
mind '[(correlation cor-abc-123)
       (Match (QueryThoughts (limit 10)))]'

# Named (both):
mind '[(intent RoleHandoff) (correlation cor-abc-123)
       (Retract (RoleClaim (role designer)))
       (Assert (RoleClaim (role poet)))]'

# This shape — intent without correlation — is impossible to
# construct (no constructor accepts it):
#   mind '[(intent RoleHandoff) (Retract ...) (Assert ...)]'
# The NOTA parser rejects it as missing the required correlation.
```

### 8.4 · `/171 Q4` — Failure-reply shape in mixed validate-write batches

Concrete failure trace for a schema-upgrade batch where the
checkpoint Validate fails:

**Request:**

```sh
mind '[(intent SchemaUpgrade) (correlation cor-xyz-789)
       (Mutate (Catalog (table thoughts) (status Migrating)))    ; op 0
       (Mutate (Row 1 (new-shape ...)))                           ; op 1
       (Mutate (Row 2 (new-shape ...)))                           ; op 2
       (Validate (Integrity (table thoughts)))                    ; op 3 — fails
       (Mutate (Catalog (table thoughts) (status Active)))]'      ; op 4
```

**Reply:**

```rust
Reply::Batch {
    header: ReplyHeader::Named {
        intent: MindBatchIntent::SchemaUpgrade,    // echoed
        correlation: cor_xyz_789,                  // echoed
    },
    outcome: BatchOutcome::Aborted {
        failed_at: 3,                              // the Validate that failed
        reason: BatchFailureReason::ValidationFailed,
    },
    per_op: vec![
        // op 0: ran, committed, then rolled back when batch aborted.
        SubReply { verb: Mutate,   status: RolledBack, payload: None },
        // op 1: same.
        SubReply { verb: Mutate,   status: RolledBack, payload: None },
        // op 2: same.
        SubReply { verb: Mutate,   status: RolledBack, payload: None },
        // op 3: the failure. Payload carries the validate's reason.
        SubReply {
            verb: Validate,
            status: Failed(SubFailureReason::ValidationFailed),
            payload: Some(MindReply::ValidationDetail(integrity_check_failure_detail)),
        },
        // op 4: never ran.
        SubReply { verb: Mutate,   status: Skipped,    payload: None },
    ],
}
```

The reply carries:

- **The batch-level reason** (`ValidationFailed` at position 3) so the
  caller can act on the failure category.
- **The validate's specific detail** (in op 3's payload) so the caller
  can render exactly which integrity check failed.
- **The status of every other op**: which were attempted-but-undone
  (`RolledBack`), which never ran (`Skipped`).
- **No payloads for `RolledBack` or `Skipped` ops** per the invariants
  in §1.6 — the caller can't trust observed values that didn't commit.

The four-state `SubStatus` (Ok / RolledBack / Failed / Skipped) plus
the position-keyed `failed_at` give the caller everything needed to
understand the failure, retry intelligently, or surface a precise
error to the user.

---

## 9 · `/171`'s status

`/171 §4` (the design spec) is superseded by §2–§5 above. The
correction record in `/171 §3` and `/171 §7` (admitting migration
cost contaminated `/170`) stands.

`/170 §3` (the Option A specification) is also superseded by the
present report, which closes its remaining gaps.

`/166` retires. Its substance lives in:

- `/171` (the correction of `/170`'s recommendation)
- This report (the implementation-ready spec)

---

## 10 · See also

- `~/primary/reports/designer/171-what-is-atomic-for-best-design.md`
  — answers what Atomic is for; correction record. Superseded by
  this report on the type-shape and semantic-precision points.
- `~/primary/reports/designer-assistant/<the /171 critique>` —
  DA's six findings whose settlements are §1.1–§1.6 above.
- `~/primary/reports/designer/170-atomic-collapse-followup-typed-atomic-or-full-spec.md`
  — Option A's §3 is the antecedent; the present report closes its
  remaining gaps.
- `/git/github.com/LiGoldragon/signal-core/src/request.rs` — what
  this spec replaces.
- `/git/github.com/LiGoldragon/signal-core/src/reply.rs` — what
  this spec replaces.
- `/git/github.com/LiGoldragon/signal-core/src/channel.rs` — the
  macro that grows to support `with intent <X>` syntax.
- `/git/github.com/LiGoldragon/sema-engine/src/engine.rs` — the
  commit-log shape that changes per §5.
- `~/primary/reports/designer/163-seven-verbs-no-structure-eighth.md`
  — the closed-boundary discipline that rules out
  `Custom(String)` in §1.2.
