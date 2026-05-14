# 170 — `/166` follow-up after designer-assistant's critique: typed-Atomic vs full-collapse

*Designer follow-up, 2026-05-15. Responds to designer-assistant's
critique of `/166`'s "collapse `Atomic` into frame shape" proposal
(forwarded by the user). Concurs with all five of DA's findings —
they're correct on the facts and they identify real architectural
gaps `/166` glossed over. Reframes the design space: the
Atomic-as-peer asymmetry is real, but **collapse may not be the right
fix**. Three options now visible: (A) full collapse with the gaps DA
identifies closed, (B) keep seven verbs and define `Atomic`'s typed
payload properly (the option `/166` should have considered), (C)
defer until a real consumer forces the question. Recommendation: B.*

**Retires when**: the workspace picks one of A / B / C, or another
report supersedes this analysis.

---

## 0 · TL;DR

Designer-assistant's critique of `/166` (forwarded in chat 2026-05-15)
lands five findings, all of which I concur with after verifying
against active source:

1. **Reply batching is undefined.** `/166` changes `Request<P>` to
   `Operations(Vec<Op<P>>)` but never says what `Reply<P>` becomes.
   Verified: `signal-core/src/reply.rs:5–9` still has
   `Reply::Operation(Payload)` — single payload.
2. **"Frame is the commit boundary" conflates transport with
   transaction.** Only valid for single-component single-commit
   write batches. Not valid for `Match` / `Subscribe` / `Validate` /
   mixed batches.
3. **Migration scope is understated.** Generated APIs, tests,
   transport read/write paths, CLI parsing, reply decoding,
   operation-kind witnesses, and sema-engine commit-logs all change.
4. **Sema-engine commit-log description is factually wrong.**
   Verified: `sema-engine/src/engine.rs:302` writes ONE
   `OperationLogEntry` per batch tagged `SignalVerb::Atomic`, NOT
   per-op. The collapse requires a new commit-log shape, not a
   rename.
5. **Decomposing named composites loses audit meaning.**
   `RoleHandoff → [Retract OldClaim, Assert NewClaim]` loses the
   semantic fact that the user intended a *handoff*, not two
   unrelated operations.

The reframing: **the original observation that triggered `/166`
remains right** — `Atomic` is structurally asymmetric in the verb
enum, since its payload contains other-verb-tagged sub-operations
while the other six carry single domain payloads. But the question
isn't "collapse or not." It's **which way to honour the asymmetry**:

- (A) **Full collapse** — drop `Atomic` from `SignalVerb`, put the
  Vec in the frame, define reply/commit-log/named-composite/
  subscription handling. Possible but ~weeks of design work.
- (B) **Keep seven, define `Atomic`'s typed payload** — accept that
  `Atomic` is a higher-order verb (which is honest), give it a
  proper typed payload shape with named intents, per-op typed
  replies, batch-level outcomes. Preserves named composites,
  sema-engine's commit-log shape, and ~95% of contracts.
- (C) **Defer** — keep `SignalVerb::Atomic` as a reserved variant
  with no defined payload; specify when a real consumer arrives.

My recommendation: **B**. The asymmetry stays explicit (which is
honest — `Atomic` is genuinely higher-order); the design work is
focused on one verb's payload shape, not a workspace-wide refactor;
named composites are preserved; sema-engine's existing commit-log
shape stays load-bearing.

---

## 1 · DA's findings, verified

### 1.1 · Reply batching is undefined ✓

Verified `signal-core/src/reply.rs`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum Reply<Payload> {
    Handshake(HandshakeReply),
    Operation(Payload),         // ← single payload
}
```

`/166` proposes `Request<P> = Operations(Vec<Op<P>>)` but says nothing
about `Reply<P>`. For N-op requests, a reply needs at minimum:

- N typed sub-replies (one per request op), AND
- A batch-level outcome (committed / rolled back / partial-failure)

Neither is specified. Concur.

### 1.2 · Frame-is-commit-boundary conflates transport with transaction ✓

`/166`'s claim "the frame *is* the commit boundary" works cleanly for
**all-write batches against one component**. It does not work for:

- **Pure `Match` batches** — no commit, no transaction. Frame is
  just a batched query.
- **`Subscribe` in a batch** — subscription doesn't commit; it opens
  an ongoing stream. A frame with `[Subscribe, Subscribe, Subscribe]`
  opens three streams; there's no commit-boundary to speak of.
- **`Validate` in a batch** — dry-run, by definition no commit.
- **Mixed batches** — `[Match X, Mutate Y]` is the "SELECT then
  UPDATE atomically" pattern; commit applies to the write only.
- **Cross-component sequences** — if a frame's ops target multiple
  components, no single component's transaction scope covers it.

`/166` assumed commit-boundary universally. Concur — the commit
semantics emerge from what's in the Vec, not from the Vec's mere
existence.

### 1.3 · Migration scope is understated ✓

`/166 §2.3` said: *"Every `signal-persona-*` contract's `signal_channel!`
invocation stays the same at source level. The variants are
unchanged; their verb tags are unchanged. Only the *envelope* the
macro emits below the variants changes."*

This understates. Even with variant declarations unchanged, the
collapse changes:

- **Generated constructors** — single-op `MindRequest::SubmitThought(...)`
  becomes part of a `Vec<Op>`-wrapping shape.
- **Generated tests** — verb-mapping witnesses today assume single-op
  per frame; multi-op tests don't exist.
- **Transport read/write paths** — every daemon's receive path decodes
  one `Operation { verb, payload }`; the new shape decodes a Vec.
- **CLI parsing** — NOTA grammar needs the bracketed sequence form
  `mind '[(Assert ...) (Mutate ...)]'` for multi-op; CLI desugaring
  rules need defining.
- **Reply decoding** — every caller's receive path expects
  `Reply::Operation(P)`; new shape needs `Reply::Operations(Vec<...>)`
  alignment.
- **Operation-kind witnesses** — every contract has
  `impl <X>Request { fn operation_kind(&self) -> <X>OperationKind }`;
  needs to become `Vec<<X>OperationKind>` or change shape entirely.
- **Sema-engine commit-log** — per finding 4 below.

Concur — the migration is significantly more than a one-day macro
refactor.

### 1.4 · Sema-engine commit-log description is factually wrong ✓

Verified `sema-engine/src/engine.rs:302`:

```rust
let snapshot = self.next_snapshot()?;
let operation = OperationLogEntry::new(
    snapshot,
    signal_core::SignalVerb::Atomic,  // ← one entry, tagged Atomic
    *batch.table().name(),
    None,
);
self.storage.write(|transaction| {
    for operation in batch.operations() {
        // each operation is applied within this single transaction
    }
});
```

Today: one `OperationLogEntry` per batch tagged `SignalVerb::Atomic`.
`/166 §2.4` claimed: *"The operation-log entries today are tagged
`signal_core::SignalVerb::Atomic` for multi-op commits and the
per-op verb for single-op commits. After: every commit log entry
references the Vec of per-op verbs."*

This is wrong on the current state. The collapse requires designing
a *new* commit-log shape — either:

- (a) Per-op log entries linked by a batch-id, OR
- (b) Per-batch log entry with a Vec of per-op verbs nested, OR
- (c) The current single-tag stays, and `Atomic` lives on as a
  log-entry tag even after disappearing from `SignalVerb`.

None of (a), (b), or (c) is specified in `/166`. Concur — this is a
real design gap.

### 1.5 · Named composites lose audit meaning ✓

`/166 §3.2`: *"`RoleHandoff` simply becomes `[Retract OldClaim, Assert
NewClaim]` at the wire, with no contract needing to declare an
`Atomic` variant."*

The semantic loss: a future agent reading the operation log sees
`[Retract, Assert]` without knowing whether this was a deliberate
handoff (audit-meaningful) or an unrelated coincidence of one retract
and one assert in the same batch.

A `RoleHandoff` *name* carries the intent. Decomposing it strips the
intent.

Fixes inside Option A (full collapse):

- Add a typed `intent: BatchIntent` field to every batch frame
- Allow `correlation_id` per batch for cross-frame audit trails
- Preserve named composites as *contract-level transaction names*

Fix inside Option B (keep seven): the named composite stays a typed
`AtomicIntent` variant in the contract — preserved by construction.

Concur — this is a real semantic loss and needs explicit fix in
either option.

---

## 2 · The reframing

`/166`'s original observation: *"`Atomic` is structurally asymmetric
— its payload contains other-verb-tagged sub-operations while the
other six carry single domain payloads."*

That's true. `Atomic` is higher-order; the other six are first-order.

`/166`'s proposed fix: collapse `Atomic` out of the verb enum and put
the Vec in the frame shape. This *eliminates* the asymmetry by
making the Vec universal.

DA's critique shows this fix is **architecturally expensive**:
- reply shape redesign
- commit-boundary semantics redefinition
- sema-engine log shape change
- workspace-wide migration
- semantic-audit machinery (named composites, correlation IDs)
- subscription-in-batch policy

The asymmetry is real, but maybe collapse-into-frame isn't the right
way to honour it. **Embracing the asymmetry** — accepting that
`Atomic` is genuinely a higher-order verb, and giving it a proper
typed payload shape — is the other option.

Three options now visible:

- **Option A**: Full collapse with all of DA's gaps closed. Possible.
  Workspace-wide refactor.
- **Option B**: Keep seven verbs; define `Atomic`'s typed payload
  shape (named intent, Vec of typed sub-ops, batch-level reply
  outcome). Focused on one verb.
- **Option C**: Defer entirely; keep `SignalVerb::Atomic` reserved
  with no defined payload until a real consumer needs it.

---

## 3 · Option A — full collapse, gaps closed

What `/166` should have specified.

### 3.1 · Request shape

```rust
pub enum SignalVerb {
    Assert, Mutate, Retract, Match, Subscribe, Validate,
    // Atomic removed
}

pub struct Request<P> {
    pub intent: Option<BatchIntent>,    // preserves named-composite audit
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<Op<P>>,
}

pub struct Op<P> {
    pub verb: SignalVerb,
    pub payload: P,
}
```

### 3.2 · Reply shape

```rust
pub enum Reply<R> {
    Handshake(HandshakeReply),
    Operations {
        intent: Option<BatchIntent>,        // echoed from request
        correlation: Option<CorrelationId>,
        outcome: BatchOutcome,
        per_op: Vec<SubReply<R>>,
    },
}

pub enum BatchOutcome {
    AllCommitted,
    RolledBack {
        reason: BatchFailureReason,
        failed_at: usize,                   // index in the Vec
    },
    PartialReadCompleted,                   // for read-only batches
    SubscriptionsOpened {
        opened_streams: usize,
    },
}

pub struct SubReply<R> {
    pub verb: SignalVerb,        // echoed from request op
    pub status: SubStatus,
    pub payload: Option<R>,      // None on failure
}

pub enum SubStatus {
    Ok,
    Rejected(SubFailureReason),
}
```

### 3.3 · Batch scope

Each frame targets one component (one daemon socket). The component
decides whether the batch is transactional. Cross-component sequences
are *not* atomic; they go through mind adjudication.

### 3.4 · Mixed-verb policy

Per receiver. A contract declares which verb-mixes it accepts:

```rust
signal_channel! {
    request MindRequest {
        Assert SubmitThought(SubmitThought),
        // ...
    }
    batch_policy {
        homogeneous_writes: allowed,
        homogeneous_reads: allowed,
        homogeneous_subscribes: allowed,
        mixed_read_write: allowed,
        mixed_with_subscribe: forbidden,    // subscriptions don't compose with commits
        mixed_with_validate: allowed,        // validate-then-commit pattern
    }
}
```

### 3.5 · Failure semantics

- Write batch with `intent=Some`: all-or-nothing; first failure rolls
  back the whole batch and replies `RolledBack { failed_at, reason }`.
- Read batch: each op runs independently; replies aggregated; no
  rollback semantics.
- Subscribe batch: each Subscribe opens independently; replies
  aggregated as `SubscriptionsOpened`.
- Mixed read-write batch: ordered execution; first write-failure
  rolls back writes, reads stay (since they don't write).

### 3.6 · Commit-log shape

Replace today's single-`SignalVerb::Atomic` log entry with:

```rust
pub struct BatchLogEntry {
    snapshot: SnapshotId,
    intent: Option<BatchIntent>,
    correlation: Option<CorrelationId>,
    op_count: usize,
    per_op_verbs: Vec<SignalVerb>,    // ordered, parallel to request
}
```

Per-op detail goes into a separate table linked by `(snapshot,
op_index)`. Audit queries reconstruct the batch.

### 3.7 · Named composites preserved

`BatchIntent` is a typed enum each domain extends:

```rust
pub enum MindAtomicIntent {
    RoleHandoff,
    SchemaUpgrade { from_version: u32, to_version: u32 },
    ChannelMigration,
    Custom(String),                  // escape hatch for unanticipated cases
}
```

A handoff frame: `intent: Some(RoleHandoff)`, `ops: [Retract ...,
Assert ...]`. The audit trail says "this batch was a handoff."

### 3.8 · Subscription handling

Subscriptions in a batch are *each* an independent stream-open. Reply
returns N stream-tokens. No transactional semantics. **Mixed
subscribe + write batches are forbidden by policy** (no clean
semantics: do you open the stream before or after the write commits?).

### 3.9 · Migration scope (honest)

- `signal-core`: redesign `Request`, `Reply`, add `BatchIntent`,
  `BatchOutcome`, `SubReply`, `BatchLogEntry`. ~3 days.
- `signal_channel!` macro: emit batch-aware shapes, batch_policy
  parsing. ~2 days.
- Every `signal-persona-*` contract: re-codegen, define
  `<X>AtomicIntent` per contract, batch_policy declaration. ~1
  day each × 8 contracts = ~8 days, parallelizable.
- Every component daemon: receive-path rewrite for Vec-shaped
  requests; reply-path for Vec-shaped replies. ~1–2 days each ×
  ~6 daemons.
- CLI parsing: NOTA grammar for batched form. ~2 days.
- `sema-engine`: redesign commit-log; rewrite `AtomicBatch` as
  generic batch. ~3 days.
- Tests: rewrite ~all verb-mapping witnesses; new batch tests. ~3
  days.

**Realistic total: ~3–4 weeks of focused operator+designer work.**
`/166`'s "one operator-day for the kernel + macro refactor, then
per-component lock refreshes" was off by an order of magnitude.

---

## 4 · Option B — keep seven, define `Atomic`'s typed payload

What `/166` could have proposed instead.

### 4.1 · `SignalVerb` stays at seven

```rust
pub enum SignalVerb {
    Assert, Mutate, Retract, Match, Subscribe, Atomic, Validate,
    //                                           ↑
    //                                           kept; honestly higher-order
}
```

The asymmetry stays. We accept `Atomic` as a special verb whose
payload contains other-verb-tagged sub-operations.

### 4.2 · `Atomic`'s typed payload — per-contract

Each contract declares its own typed `Atomic` variant with a typed
intent and a Vec of typed sub-ops:

```rust
// signal-persona-mind (hypothetical):
signal_channel! {
    request MindRequest {
        Assert SubmitThought(SubmitThought),
        Mutate StatusChange(StatusChange),
        Retract RoleRelease(RoleRelease),
        Match QueryThoughts(QueryThoughts),
        Subscribe SubscribeThoughts(SubscribeSpec),
        Atomic MindAtomicBatch(MindAtomicBatch),    // ← single typed Atomic variant
        Validate ValidateProposal(Proposal),
    }
}

pub struct MindAtomicBatch {
    pub intent: MindAtomicIntent,
    pub ops: Vec<MindNonAtomicOp>,            // can't nest Atomic in Atomic
    pub correlation: Option<CorrelationId>,
}

pub enum MindAtomicIntent {
    RoleHandoff(RoleHandoffIntent),
    ChannelMigration(ChannelMigrationIntent),
    SchemaUpgrade(SchemaUpgradeIntent),
    Custom(String),
}

pub enum MindNonAtomicOp {
    Assert(MindAssertVariant),
    Mutate(MindMutateVariant),
    Retract(MindRetractVariant),
    Validate(MindValidateVariant),
    // Match/Subscribe NOT in this enum — they don't compose under Atomic
}
```

The `signal_channel!` macro grows to auto-derive `MindNonAtomicOp`
from the contract's Assert/Mutate/Retract/Validate variants. This is
a focused macro extension, not a workspace-wide change.

### 4.3 · `Atomic`'s typed reply

```rust
signal_channel! {
    reply MindReply {
        // ... existing variants ...
        AtomicCommitted(AtomicCommitted),
        AtomicRolledBack(AtomicRolledBack),
    }
}

pub struct AtomicCommitted {
    pub intent: MindAtomicIntent,         // echoed
    pub correlation: Option<CorrelationId>,
    pub per_op_results: Vec<MindNonAtomicReplyVariant>,
}

pub struct AtomicRolledBack {
    pub intent: MindAtomicIntent,
    pub correlation: Option<CorrelationId>,
    pub failed_at: usize,
    pub reason: AtomicFailureReason,
}
```

### 4.4 · Sema-engine commit-log: unchanged

Today's `OperationLogEntry { snapshot, verb: SignalVerb::Atomic,
table, .. }` stays as the per-batch log entry. The intent and per-op
detail can land in a separate `AtomicIntentLog` table keyed by
`snapshot` — additive, not a redesign.

### 4.5 · Named composites preserved

`RoleHandoff` IS an `Atomic` with `intent=MindAtomicIntent::RoleHandoff`
and `ops=[Retract RoleClaim, Assert RoleClaim]`. The audit trail
shows "this was a handoff" by reading the intent.

The audit-trail compromise `/166` would have to invent under collapse
(`BatchIntent` enum) is in B by construction.

### 4.6 · Mixed read/write/subscribe

Not supported in B. `Atomic` is for write+validate sequences only.
Reads use `Match`. Subscribes use `Subscribe`. If a caller wants
read-then-write atomicity, the read goes in a separate frame; the
write's `Atomic` can include a `Validate` first.

This is a simpler stance than A's mixed-batch policy, and matches
what `sema-engine::AtomicBatch` already enforces:
*"Assert, Mutate, and Retract operations inside the bundle"* (per
designer-assistant `/54 §4.2`).

### 4.7 · Migration scope (honest)

- `signal-core`: minimal change — `SignalVerb` enum stays 7. No
  shape change to `Request`/`Reply`. Done.
- `signal_channel!` macro: extension to support the
  `Atomic <Name>(<NameBatch>)` pattern, auto-derive
  `<X>NonAtomicOp` enum. ~1 day.
- `signal-persona-mind` (first consumer): add `Atomic MindAtomicBatch`
  variant, define `MindAtomicIntent`. ~1 day.
- `sema-engine`: rename `AtomicBatch<R>` → keep, add per-batch
  intent storage. ~0.5 day.
- Other contracts: no change until they want `Atomic`. Zero
  immediate cost.
- Tests: new round-trip per intent. ~0.5 day per consumer.

**Realistic total: ~2–3 days of focused operator+designer work for
the first consumer, then incremental per-consumer.**

---

## 5 · Option C — defer

Keep `SignalVerb::Atomic` as a reserved variant with no defined
payload. No contract uses it. The asymmetry stays in the enum but
isn't actively load-bearing.

When a real consumer needs `Atomic` (the engine-upgrade case in
persona ARCH §1.6.5, or a schema-migration case), specify then.

Cost: zero design work now. Lost: the option to do batched
operations until the spec lands. The asymmetric verb sits in the
enum staring back at every reader.

---

## 6 · Comparison

| Dimension | A: full collapse | B: typed Atomic | C: defer |
|---|---|---|---|
| `SignalVerb` size | 6 | 7 | 7 |
| Asymmetry in verb enum | removed | embraced as higher-order | unresolved |
| Reply shape work | major redesign | minor additive | none |
| Sema-engine log work | redesign | additive | none |
| Named-composite audit | typed `BatchIntent` enum at frame level | typed `<X>AtomicIntent` per contract (preserved by construction) | not applicable |
| Contracts changed | all (re-codegen) | only Atomic-using ones | none |
| Mixed-verb batches | per-receiver policy | not supported | not applicable |
| Subscriptions in batch | per-policy (probably forbidden) | not in `Atomic` | not applicable |
| Migration scope | ~3–4 weeks | ~2–3 days per consumer | zero |
| Beauty / elegance | uniform Vec frame | honest higher-order verb | unresolved |
| First-consumer effort | massive | small | none |

---

## 7 · Recommendation: Option B

**Embrace the asymmetry**. `Atomic` is genuinely a higher-order
verb — its payload contains other verbs. That's true and shouldn't
be denied. The right move is to **type it properly**, not to flatten
it out.

Specifically:

1. Keep `SignalVerb` at seven. `Atomic` remains a peer verb in the
   enum.
2. Extend the `signal_channel!` macro to support the
   `Atomic <Name>(<NameBatch>)` pattern, auto-deriving the
   `<X>NonAtomicOp` enum from the contract's Assert/Mutate/Retract/
   Validate variants.
3. When a contract wants `Atomic` (per `/165 §3.1`'s candidates), it
   adds one variant with a typed `<X>AtomicIntent` and a typed
   `Vec<<X>NonAtomicOp>` payload. Named composites are preserved by
   construction.
4. Sema-engine's existing per-batch commit-log shape stays. Add a
   separate `AtomicIntent` table for the intent metadata; minimal
   change to existing schema.
5. The CLI can support a sugar form for single-op Atomic frames
   (`mind '(Atomic (RoleHandoff (...)))'`) without needing the
   bracketed `[...]` syntax `/166` proposed.

This addresses all five of DA's findings:

- **Reply batching**: defined per-contract via the `<X>AtomicReply`
  shape.
- **Transport vs transaction**: `Atomic` IS the transaction;
  non-Atomic frames don't claim commit semantics.
- **Migration scope**: small (one macro extension + one consumer);
  realistic.
- **Sema-engine log shape**: unchanged (additive only).
- **Named composites**: preserved by construction.

What we don't get from B that A would have given:

- Uniform frame shape (every frame as Vec). A has elegance here that
  B lacks.
- Mixed read/write batches at the wire (not supported in B).

I think that's the right trade. The elegance of A is bought at the
cost of weeks of refactoring across the workspace. B preserves what
already works and focuses the design on the one verb that needs it.

The `/162` planetary bijection stays at seven (per
`/167 §7`'s argument that Jupiter-as-binding-relation is metaphysically
honest as a peer-verb if we accept it's higher-order).

---

## 8 · Open question

**Confirm Option B?** Or want to push toward A or C?

If B: next step is a designer-operator handoff to plan the
`signal_channel!` macro extension and the first consumer
(probably `signal-persona-mind`'s `RoleHandoff` if you confirm
`/165 Q1`).

If A: this report's §3 is the starting point for the full-collapse
spec; expect ~3–4 weeks of workspace-wide work.

If C: `/166` retires, `Atomic` stays in `SignalVerb` as a reserved
variant, and we wait for a real consumer.

---

## 9 · `/166`'s status after this report

`/166` proposed the collapse without the design work DA's critique
shows it needs. Either:

- (a) `/166` retires if Option B or C is chosen (the collapse direction
  is rejected), OR
- (b) `/166` is superseded by the present report if Option A is
  chosen (the collapse direction is kept but specified properly).

Until the user picks A/B/C, `/166` stands as the *initial proposal*
and the present report stands as the *response*. The chat reply to
the user flags the status.

---

## 10 · See also

- `~/primary/reports/designer-assistant/<latest>` — DA's critique
  whose findings this report responds to (chat-forwarded
  2026-05-15; precise filename TBD when DA writes it up).
- `~/primary/reports/designer/166-atomic-collapses-into-frame-shape.md`
  — the proposal under critique.
- `~/primary/reports/designer-assistant/54-verb-coverage-implementation-and-design-audit.md`
  — DA's earlier audit of `/165` that surfaced the `AtomicBatch`
  reference-implementation fact.
- `/git/github.com/LiGoldragon/signal-core/src/reply.rs` — current
  `Reply::Operation(Payload)` single-payload shape.
- `/git/github.com/LiGoldragon/sema-engine/src/engine.rs:302` —
  current per-batch `OperationLogEntry` tagged
  `SignalVerb::Atomic`.
