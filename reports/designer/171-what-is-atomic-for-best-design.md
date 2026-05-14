# 171 — What is `Atomic` for? The best design, with migration cost stripped

*Designer correction-report, 2026-05-15. Responds to a user
correction: "you understand I don't care about migration time right?
I want the *best design* — so what is that? what is atomic for?
what's the difference between one atomic or multiple messages?"
Concedes that `/170`'s analysis was contaminated by migration-cost
reasoning that doesn't belong in design judgment. Re-derives the
best design from first principles. The answer changes: the original
`/166` collapse is the best design; `/170`'s Option B
("keep seven, type Atomic properly") was a migration-cost-driven
retreat that I dressed up as principle. The frame IS the commit
boundary. Atomic isn't a verb — it's structural to the frame.*

**Retires when**: the cleaner shape lands (or the user objects).

---

## 0 · TL;DR

The user's correction lands. I let migration cost shape `/170`'s
recommendation; that violates `ESSENCE.md` §"Backward compatibility
is not a constraint" — which is really the workspace's statement
that *what's expensive to refactor* doesn't get to influence
*what's the right shape*. Migration cost is the same category
as backward compat; it doesn't belong in design judgment.

Re-deriving with that constraint stripped:

1. **What is `Atomic` for?** Protecting invariants that span
   multiple operations. Specifically: all-or-nothing commit, snapshot
   consistency for reads, sequencing of dependent operations, and
   audit-trail integrity. The defining test: *would the system have
   a broken invariant if some ops committed but not others?* If yes,
   atomicity is load-bearing.

2. **What's the difference between one `Atomic` and multiple
   messages?** Commit boundary. One Atomic is one commit unit;
   multiple messages are N commit units. Atomic gives all-or-nothing,
   consistent snapshots, rollback on failure, and one audit-log
   entry. Multiple messages give independent commits, no rollback,
   partial-state visible, and N audit-log entries.

3. **The best design** (stripped of migration cost): **the collapse
   in `/166`**. Every frame is one commit boundary. The frame
   carries a `Vec<Op>` (possibly length 1). The verb tags each
   operation. *Atomic is not a verb because atomicity is a
   structural property of every frame.* Single-op frames are
   trivially atomic. Multi-op frames are explicitly atomic.

4. **What was right about `/170`'s Option B**: the named-intent
   metadata. *That part survives.* It moves from "an enum variant in
   the contract" to "a frame-level annotation." Every frame can
   carry `intent: Option<BatchIntent>`; named composites like
   `RoleHandoff` survive as audit-fact metadata, not as verbs.

I'm retracting `/170 §7`'s recommendation of Option B. The user is
right: the typed-Atomic option was the migration-cost-friendly
retreat. The full collapse (with DA's design gaps closed) is the
best design.

---

## 1 · What is `Atomic` for?

`Atomic` exists to **protect invariants that span multiple
operations**. The defining property is that *the system would be
incoherent if some ops committed but not others*.

Four specific things atomicity gives you:

### 1.1 · All-or-nothing commit

Writes within an atomic boundary either all succeed or all fail.
Partial commits are impossible. The system never observes "half of
a logical change."

Example: `RoleHandoff`. The transition from "role-A holds the claim"
to "role-B holds the claim" must be atomic. If `Retract(role-A's
claim)` succeeds but `Assert(role-B's claim)` fails, the system has
*no one* holding the role — a broken invariant. The handoff has to
be one commit.

### 1.2 · Snapshot consistency for reads

When reads happen inside an atomic boundary, they all read at the
same snapshot. This is what SQL's `BEGIN ... COMMIT` gives for
mixed read-write transactions, what Datomic gives via `(d/db conn)`
at transaction-start.

Example: a query that reads "all open claims for role X" and then
"the activity record for X's last claim" must see a consistent view.
If the two reads happen in separate frames, a concurrent retract
could fire between them, and the second read sees state inconsistent
with the first.

### 1.3 · Sequencing of dependent operations

Within an atomic boundary, operations execute in order, with each
seeing the effects of previous operations in the same boundary.

Example: schema migration. `Mutate catalog-row to Migrating` →
N × `Mutate per-row under new shape` → `Mutate catalog-row to
Active`. The per-row mutations need to see the catalog-row's
`Migrating` state (so the schema-guard doesn't reject them); the
final catalog-row mutation needs to see all per-row mutations
applied. Sequencing matters.

### 1.4 · Audit-trail integrity

A logical transaction is one entry in the operation log, with N
sub-operations linked together. Without atomicity, an audit reader
sees N independent entries with no way to tell whether they were a
coordinated transaction or unrelated coincidence.

Example: `SchemaUpgrade` migration. The audit log entry says "engine
upgraded from v1 to v2 at snapshot N; comprised these N row
mutations." Without atomicity, the audit log has N row-mutation
entries with no upgrade-intent marker — readers can't tell whether
the workspace is mid-migration or these were unrelated edits.

### 1.5 · The test

A simple diagnostic: *if any subset of these ops committed but not
the rest, would the system have a broken invariant?* If yes,
atomicity is load-bearing.

Operations that *don't* need atomicity (each commits independently):
- Submitting a single thought
- Reading the current role status
- Subscribing to a stream
- Validating a single proposal

Operations that *do* need atomicity:
- Handing off a role (retract + assert)
- Migrating a schema (mutate catalog + mutate rows + mutate catalog)
- Engine upgrade (assert new engine + migrate state + retract old engine)
- Adjudicating a channel grant + writing the grant + replying (all
  durably linked, otherwise the router enforces a grant that mind
  never committed)

---

## 2 · What's the difference between one `Atomic` and multiple messages?

The fundamental difference is the **commit boundary**:

| Property | One Atomic frame | Multiple separate frames |
|---|---|---|
| Commit boundary | **one** | **N** |
| All-or-nothing | yes | no — each independent |
| Snapshot consistency for reads | yes (single snapshot) | no — each reads its own snapshot |
| Sequencing across ops | guaranteed | only by external coordination |
| Partial-failure handling | rollback the whole | leaves the system in partial state |
| Audit-log entries | one (with N sub-ops) | N independent |
| Caller complexity | low: declare intent | high: handle partial states |
| Network round-trips | one | N (or pipelined) |
| Concurrent-writer race window | none across ops | each op exposed to races |

Two operations can be safely split across separate messages **iff
they don't share an invariant**. If they do, the split exposes the
invariant to violation.

The right way to think about it: **multiple messages are for
operations that are logically independent**. Atomicity is for
operations that are logically one unit. You don't choose atomic
based on size or convenience; you choose it based on whether the
ops form a single logical transition.

---

## 3 · What changes in the analysis when migration cost is stripped

`/170 §4` made the case for Option B (typed Atomic, keep seven
verbs) primarily on these grounds:

| `/170`'s argument for B | Migration-flavored? | Survives the strip? |
|---|---|---|
| "Migration scope: small" | yes | no — irrelevant |
| "Sema-engine log shape: unchanged" | yes | no — irrelevant |
| "Other contracts unchanged" | yes | no — irrelevant |
| "Macro grows once" | yes | no — irrelevant |
| "Embrace the asymmetry as honest higher-order" | no | partially — see §4 |
| "Named composites preserved by construction" | no | yes (but A can do this too) |

Strip the migration-flavored arguments. What's left of the
argument for B?

- The honest-higher-order claim
- The named-composite preservation

The named-composite preservation isn't actually exclusive to B. A's
§3.7 (the gap-closed full collapse) preserves named composites via
a frame-level `BatchIntent` annotation. The semantic loss DA
identified is solvable in A.

The honest-higher-order claim is weaker than I made it sound.
*Atomic as a peer verb* is structurally asymmetric. The collapse
acknowledges this and removes the asymmetry. B "embraces" the
asymmetry by making it a typed thing — but the asymmetry is still
there, just better-typed. The cleaner move is to **remove the
asymmetry** rather than dress it up.

When migration is stripped, **the collapse wins on every dimension
that matters for design**.

---

## 4 · The best design

The frame is the commit boundary. Every frame carries:

- A `Vec<Op>` of one or more operations
- Each op carries a verb (one of six elementary) and a typed payload
- An optional `intent: BatchIntent` for audit/composite-naming
- An optional `correlation: CorrelationId` for cross-frame audit
  trails

The verbs are six elementary: `Assert`, `Mutate`, `Retract`, `Match`,
`Subscribe`, `Validate`. No `Atomic` because atomicity is structural
to the frame.

Single-op frames are trivially atomic (a length-1 Vec). Multi-op
frames are explicitly atomic.

```rust
pub enum SignalVerb {
    Assert, Mutate, Retract, Match, Subscribe, Validate,
}

pub struct Request<P> {
    pub intent: Option<BatchIntent>,
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<Op<P>>,
}

pub struct Op<P> {
    pub verb: SignalVerb,
    pub payload: P,
}
```

The reply mirrors the structure:

```rust
pub enum Reply<R> {
    Handshake(HandshakeReply),
    Operations {
        intent: Option<BatchIntent>,         // echoed
        correlation: Option<CorrelationId>,  // echoed
        outcome: BatchOutcome,
        per_op: Vec<SubReply<R>>,
    },
}

pub enum BatchOutcome {
    /// All ops succeeded. For writes, all committed atomically.
    /// For reads, all observed the same snapshot.
    /// For subscribes, all opened.
    Committed,

    /// A write op failed; the entire batch rolled back.
    /// Reads taken in the same batch are invalidated.
    RolledBack {
        failed_at: usize,
        reason: BatchFailureReason,
    },
}

pub struct SubReply<R> {
    pub verb: SignalVerb,
    pub status: SubStatus,
    pub payload: Option<R>,
}
```

The `BatchIntent` is per-domain:

```rust
// In signal-persona-mind:
pub enum MindBatchIntent {
    RoleHandoff(RoleHandoffIntent),
    SchemaUpgrade(SchemaUpgradeIntent),
    ChannelMigration(ChannelMigrationIntent),
    Custom(String),
}

// Generic type the BatchIntent field carries — each contract picks its enum.
```

The sema-engine commit-log changes shape to match:

```rust
pub struct CommitLogEntry {
    pub snapshot: SnapshotId,
    pub intent: Option<BatchIntent>,
    pub correlation: Option<CorrelationId>,
    pub ops: Vec<OpLogDetail>,        // ordered, parallel to request
}

pub struct OpLogDetail {
    pub verb: SignalVerb,
    pub table: TableName,
    pub effect: DeltaKind,
}
```

The audit trail is now richer than today's design: every commit
shows its intent and per-op detail.

### 4.1 · Composition rules (the design we actually need)

Different verb-mixes have different commit semantics:

| Frame contents | Commit semantics |
|---|---|
| All writes (`Assert`/`Mutate`/`Retract`) | All-or-nothing atomic commit. `RolledBack { failed_at }` on first failure. |
| All `Match` | Snapshot read. All reads see the same snapshot. No commit. |
| All `Subscribe` | Multiple stream-opens. Each independent; failure of one doesn't block others. |
| All `Validate` | Multiple dry-runs against one snapshot. None commits. |
| Mixed writes + `Validate` | Validates run first; if any fails, no writes commit. If all validates pass, writes commit atomically. |
| Mixed `Match` + writes | Reads at the snapshot the writes will commit at. SELECT-FOR-UPDATE pattern. |
| Mixed `Subscribe` + writes | **Forbidden**. Subscribes don't compose with commit boundaries; agents construct separate frames for them. |

This is more expressive than today's `Atomic` (writes-only). The
mixed-validate-write and mixed-read-write patterns become first-class.

### 4.2 · CLI surface

NOTA syntax with the bracketed-sequence form `/166` proposed:

```sh
# Single-op (trivially atomic, ergonomic shorthand):
mind '(Assert (SubmitThought (...)))'

# Multi-op explicit:
mind '[(Retract (RoleClaim (role designer)))
       (Assert (RoleClaim (role poet)))]'

# With intent:
mind '[(intent RoleHandoff)
       (Retract (RoleClaim (role designer)))
       (Assert (RoleClaim (role poet)))]'

# Mixed validate-then-write:
mind '[(Validate (SchemaCheck (table thoughts)))
       (Mutate (catalog (table thoughts) (status Active)))]'
```

### 4.3 · What about Subscribe in a batch?

`Subscribe` opens an ongoing stream. It doesn't have a commit boundary
in the write sense. Two design options:

- **Forbid `Subscribe` in mixed batches.** Cleanest. Agents
  construct separate frames for subscriptions. The composition
  rules in §4.1 reflect this.
- **Allow `Subscribe` in batches, define semantics carefully.**
  E.g., subscriptions open *after* writes commit, *at* the
  post-commit snapshot. More expressive but the semantics get
  intricate.

I lean toward the first. Subscriptions are long-lived;
bundling them with one-shot commits feels like mixing axes.

---

## 5 · What was right about `/170`'s Option B

The named-intent metadata. That part survives the collapse — just at
a different syntactic level. Instead of:

```rust
// /170 Option B: typed Atomic variant
signal_channel! {
    request MindRequest {
        // ...
        Atomic MindAtomicBatch(MindAtomicBatch),
    }
}
```

We get:

```rust
// /171 final: intent at the frame level
struct Request<P> {
    intent: Option<BatchIntent>,    // ← named-composite audit preserved here
    correlation: Option<CorrelationId>,
    ops: Vec<Op<P>>,
}
```

The `RoleHandoff` audit fact is preserved by setting
`intent: Some(MindBatchIntent::RoleHandoff)`. The audit log shows
"this frame was a handoff." No semantic loss.

`/170 §1.5`'s concern about losing audit meaning is addressed not by
keeping Atomic as a verb, but by the `intent` field at the frame
level.

---

## 6 · What changes in `/170`'s status

`/170` recommended Option B. That recommendation came from a
migration-cost-contaminated analysis. **Retracted.**

`/170 §3` (the Option A specification — full collapse with the gaps
closed) is the correct design. This report builds on it.

`/170 §4` (Option B specification) stands as a *recorded alternative*
that we rejected for being a migration-cost retreat dressed up as
principle. Keeping it on the record honestly says "this option
existed; we considered it; the design grounds didn't support it."

`/166`'s original proposal is vindicated, with the design gaps DA
identified closed in §4 above. `/166` retires now; this report
supersedes its details.

---

## 7 · Honesty notes

A few things I should record honestly:

1. **I let migration cost steer the design judgment in `/170`.** That
   was the error. The user's correction is sharp because workspace
   discipline (`ESSENCE.md` §"Beauty is the criterion", "Backward
   compatibility is not a constraint") explicitly tells designers
   to ignore this kind of pressure when choosing the right shape.
   I should have caught it without the correction.

2. **`/170 §7`'s argument "embrace the asymmetry as honest
   higher-order"** was a rationalization. The asymmetry was a smell.
   The cleaner move is to remove it. I gave the rationalization the
   recommendation slot.

3. **DA's findings are all real design issues.** Not migration cost
   issues. The fixes belong in the design, not as reasons to retreat
   from the design. §4 above closes them.

4. **The user's original observation in chat was right.** "If every
   signal is a Vec of verbs, then every signal is an atomic, with
   the single-member being the 'non-atomic' verb." That's exactly
   the shape. I should have written `/166` to defend that position
   instead of writing `/170` to retreat from it.

---

## 8 · Open questions (real ones, not migration-cost ones)

These are still legitimate design questions:

### Q1 — Subscribe-in-batch policy?

§4.3 prefers forbidding `Subscribe` in mixed batches. Confirm?

### Q2 — `BatchIntent` per-contract or global enum?

Per-contract gives stronger typing (each contract declares its own
intents). Global gives cross-contract intents (e.g., a workspace-wide
`SchemaUpgrade` intent that spans mind and sema-engine). I lean
per-contract; global intents are rare.

### Q3 — `correlation` always optional, or required for certain intents?

If `intent: Some(...)`, should `correlation` be required? Probably
yes — a named intent without a correlation ID is harder to track
across follow-up frames. But this can be per-intent policy.

### Q4 — Failure semantics in mixed-validate-write batches?

If a `Validate` fails inside a mixed batch, what does the failure
reply carry? The validate's reason for failure plus the writes that
were skipped? Probably yes; design the reply shape accordingly.

---

## 9 · See also

- `~/primary/reports/designer/166-atomic-collapses-into-frame-shape.md`
  — the original collapse proposal; vindicated by this report.
- `~/primary/reports/designer/170-atomic-collapse-followup-typed-atomic-or-full-spec.md`
  — Option A's §3 is the spec this report builds on; Option B is
  retracted.
- `~/primary/reports/designer-assistant/<the /166 critique>` — DA's
  findings are addressed in §4 above, not as reasons to retreat.
- `~/primary/ESSENCE.md` §"Beauty is the criterion" — the rule I
  forgot to apply when writing `/170`. The user's correction was
  the workspace's discipline doing its job.
- `~/primary/ESSENCE.md` §"Backward compatibility is not a
  constraint" — the rule that names "migration cost can't shape
  design" as a workspace principle.
