# 245 — Design alternatives for the /244 holes

*Rethinks for each of the five holes from `/244`. Some are
incremental tweaks; three are different-approach moves worth
considering before landing the incremental fixes. Plus four
bigger-picture rethinks for the workspace to weigh against the
current direction. Nothing here is landed; all are proposals.*

## 0 · TL;DR

Three of the five holes have a different-approach move that
reads cleaner than the incremental fix:

| Hole | Incremental fix | Different approach |
|---|---|---|
| 1 (typed rejection on wire) | Add `reply_from_lowering_rejection` to `Lowering` | **`lower()` returns `Result<Vec<SemaOperation>, Self::Reply>` — Err carries the contract reply variant directly.** |
| 2 (`Observe` verb collision) | Rename to `Probe` | **`observable` block lets the contract author NAME the open/close verbs.** |
| 3 (publish-bridge) | Hand-written daemon adapter | **Move `ObserverChannel` trait to `signal-frame`; macro emits the impl automatically.** No bridge needed. |
| 4 (filter-match impl is trusted) | Macro-generate closed-enum filter defaults | Same as incremental — closed-enum defaults are the right shape. |
| 5 (no end-to-end example) | Build a new example | **Use the pilot (signal-repository-ledger) as the example by adopting `observable` there.** |

Plus four bigger rethinks at the bottom (§5) worth a separate
read.

## 1 · Hole 1 — Reply variants ARE the rejection language

The /244 incremental fix adds two methods to `Lowering`:

```rust
fn reply_from_lowering_rejection(&self, op: &Self::Operation, reason: &Self::RejectionReason) -> Self::Reply;
fn reply_from_engine_rejection(&self, op: &Self::Operation, error: &S::Error) -> Self::Reply;
```

Three methods total. Auxiliary plumbing.

**The cleaner shape: rejection IS a reply variant.** Drop the
`RejectionReason` associated type entirely. `lower()` returns:

```rust
fn lower(&self, op: &Self::Operation) -> Result<Vec<SemaOperation>, Self::Reply>;
```

On the Err path, the contract author returns the exact
`Reply::SubmitRejected(SubmitRejectionReason { … })` variant
they want the caller to see. The executor doesn't need to
translate — it just passes the reply through.

```rust
impl Lowering for SpiritLowering {
    type Operation = SpiritOperation;
    type Reply = SpiritReply;

    fn lower(&self, op: &SpiritOperation) -> Result<Vec<SemaOperation>, SpiritReply> {
        match op {
            SpiritOperation::State(statement) => {
                if !self.policy.accepts(statement) {
                    return Err(SpiritReply::StateRejected(StateRejectionReason::PolicyDenied));
                }
                Ok(vec![SemaOperation::Assert(self.to_typed_entry(statement))])
            }
            // ...
        }
    }

    fn reply_from_effects(&self, op: &SpiritOperation, effects: &[SemaEffect]) -> SpiritReply {
        // ... success path
    }
}
```

The `Executor::execute` loop becomes:

```rust
for op in request.payloads() {
    self.observers.publish_operation_received(op);
    match self.lowering.lower(op) {
        Ok(ops) => sema_ops.extend(ops),
        Err(reply) => return wire_reply_with_single_subreply(reply),  // contract reply, not Reply::Rejected
    }
}
```

What this gives:
- **One method instead of three** on the `Lowering` trait.
- **The reply-naming convention in `/243` §1 actually operative on the wire**: the variant `SubmitRejected(SubmitRejectionReason)` reaches the caller intact.
- **`Reply::Rejected { reason: Internal }` is reserved for true kernel-level failures** — frame parse error, rkyv decode failure, version mismatch, etc. Daemon-level rejections live in the contract reply enum.
- **The engine error path** still exists for `SemaEngine::Error`, but it produces a kernel `Reply::Rejected { Internal }` — engine errors aren't contract-domain rejections.

Severity of replacing the incremental: high improvement.
Implementation cost: small (signal-executor change).

## 2 · Hole 2 — Contract author names the observable verbs

The /244 incremental: rename macro-injected `Observe` → `Probe`
(or similar). Avoids the spirit collision but introduces a
less-natural name for everyone else.

**The cleaner shape: let the contract author name the open/close
verbs in the `observable` block.** The macro accepts:

```rust
signal_channel! {
    channel Spirit {
        operation State(Statement),
        operation Observe(Selection),         // contract author's own one-shot read
        // ...
    }
    reply SpiritReply { … }
    observable {
        operation_open Watch(Filter) opens ObserverStream,    // ← author picks
        operation_close Unwatch(ObserverToken),                // ← author picks
        filter Filter;
        event OperationReceived;
        event SemaEffectEmitted;
    }
}
```

The macro still owns:
- Token type generation.
- ObserverStream block injection.
- Filter-match trait skeleton.
- ObserverSet bookkeeping.
- Publish-function emission.

The contract author owns:
- The two verb names (`Watch`/`Unwatch`, `Subscribe`/`Unsubscribe`,
  `Tap`/`Untap`, `Probe`/`Unprobe`).
- The filter type.
- The event types.

What this gives:
- **No collisions.** Each contract picks the verbs that fit its
  domain. Spirit can have its own `Observe(Selection)` AND
  `Watch(Filter)` for observability.
- **Verb reuse across contracts naturally**: most contracts
  pick `Watch`/`Unwatch`; some pick differently when their
  domain prefers other words.
- **One less workspace-uniform constraint to maintain.** The
  event class names (`OperationReceived`, `SemaEffectEmitted`)
  stay workspace-uniform; the verb names don't need to be.

Severity of replacing the incremental: high improvement;
removes the rename-as-collision-mitigation pattern entirely.

## 3 · Hole 3 — Move `ObserverChannel` to signal-frame

The /244 incremental: a hand-written daemon adapter bridges
the macro's publish closures to the executor's
`ObserverChannel` trait.

**The cleaner shape: move `ObserverChannel<Operation>` from
signal-executor to signal-frame.** The macro emits the impl
automatically.

Current state:
- `signal-frame` owns the macro. The macro emits
  `LedgerObserverSet` with `publish_operation_received(event,
  deliver_closure)` and `publish_sema_effect_emitted(event,
  deliver_closure)`.
- `signal-executor` owns the `ObserverChannel<Operation>` trait
  used by `Executor::execute`.
- The two don't match shape.

Move:
- Define `ObserverChannel<Operation>` in `signal-frame` (it's
  conceptually frame-side — the channel surface owns its
  observers).
- The macro emits the impl on `LedgerObserverSet` directly:
  `impl ObserverChannel<LedgerOperation> for LedgerObserverSet`.
  The publish methods become trait methods.
- `signal-executor` depends on `signal-frame` (already does) and
  uses the trait.

No bridge crate. No hand-written adapter. Daemon code just:

```rust
let observers = LedgerObserverSet::new();
let executor = Executor::new(LedgerLowering::new(), sema_engine, observers);
```

Severity: high improvement; removes friction for every daemon.

## 4 · Hole 4 — Closed-enum filter defaults

Same as the incremental fix. The macro emits a menu of
closed-enum filter variants the contract author opts into:

```rust
observable {
    filter MyFilter = ObserverFilter::{All, OnlyOperations { kinds }, OnlyEvents { classes }};
    // ...
}
```

The macro generates the impl for the predicate variants;
contract authors only write custom impls when none of the
preset filters fit.

No different approach here — the incremental is the right
shape. Note: combine with hole 2 (`observable` block expands)
since both change the same grammar.

## 5 · Hole 5 — Pilot IS the worked example

The /244 incremental: build a new example daemon (a
`signal-counter-daemon` or `signal-executor-examples/`).

**The cleaner move: don't write a separate example. Adopt
`observable` in `signal-repository-ledger` and let the pilot
be the canonical end-to-end example.** Its existing tests
already exercise:
- A real contract with operations + replies.
- An external consumer (the gitolite hook + `ouranos` service).
- Real daemon dispatch (`repository-ledger` daemon).

Add an `observable` block to the contract; have the daemon use
`signal-executor` with a real `Lowering` impl; have one test
subscribe to the observer stream and assert events flow.

The pilot is already half-built. Finishing it is cheaper than
writing a fresh example, and it doubles as the Phase-3 reference.

## 6 · Bigger rethinks worth considering

Four moves the workspace could weigh against the current
direction. None are needed; all are worth thinking about
before the per-component refactors cascade.

### A — Make observability **universal**, not opt-in

Every signal channel emits observer events automatically.
Drop the `observable` opt-in block. The macro always injects
the observer surface; daemons that genuinely don't need it
pay the trait-impl cost (small).

Cost: every daemon needs the bookkeeping. Even leaf utilities.
Benefit: `persona-introspect` knows EVERY component is
observable; cross-component patterns work uniformly.

My lean: opt-in is right; observability has real cost for
small/simple daemons. But the bar for opting in should be low.

### B — Push the executor into the macro

Instead of a separate `signal-executor` crate, the macro
generates the `Executor<L>` type for each channel
automatically. The contract author writes a `Lowering` impl;
the macro emits a `LedgerExecutor<L: Lowering<Operation =
LedgerOperation, Reply = LedgerReply>>` newtype around it.

Cost: macro grows. Benefit: no separate crate to maintain;
the contract crate emits the executor pattern in-place.

My lean: keep the separate crate. The macro is already large;
adding the executor pattern crosses a complexity threshold.

### C — Drop the kernel `Reply` entirely

Each contract owns its full reply enum including all failure
variants. The kernel becomes purely frame mechanics; no
`Reply<ReplyPayload>` wrapper, no `RequestRejectionReason`.

Cost: every contract has to re-implement common reply
patterns. No `Internal` variant for kernel failures — every
contract picks its own. Benefit: maximum contract-locality;
no kernel cross-cutting concerns.

My lean: keep `Reply<ReplyPayload>` for the wire shape. The
kernel still needs a way to express "frame parse failed" or
"version skew" — those are not contract-domain rejections.
But narrowing `RequestRejectionReason` to only those true
kernel failures (as proposed in hole 1's different approach)
is the right move.

### D — Make Sema operations contract-extensible

Instead of a fixed 6-verb Sema vocabulary, daemons can
register their own Sema verbs (e.g., a fulltext-index daemon
adds `Reindex` as a Sema verb).

Cost: major rethink of `signal-sema`; the 6-verb spine no
longer universal at the execution layer. Benefit: daemons
with specialized state effects (fulltext indexes, blob
storage, etc.) name their effects in their domain rather
than fitting into Match/Mutate/etc.

My lean: don't do this yet. The 6-verb spine has held up for
the contracts we've audited. Wait for a real component where
the verbs feel forced.

## 7 · Recommendations

Combine the cleaner-shape moves into one bundled fix:

1. **Hole 1**: `lower()` returns `Result<Vec<SemaOperation>,
   Self::Reply>`. Drop `RejectionReason` from `Lowering`.
2. **Hole 2**: `observable` block accepts `operation_open
   <Verb>(Filter)` and `operation_close <Verb>(Token)` —
   contract author names the verbs.
3. **Hole 3**: move `ObserverChannel<Operation>` from
   signal-executor to signal-frame. The macro emits the impl.
4. **Hole 4**: macro-generates closed-enum filter defaults.
5. **Hole 5**: adopt `observable` in signal-repository-ledger
   as the canonical worked example.

These five changes together:
- Drop one associated type from `Lowering` (RejectionReason).
- Drop one trait from signal-executor's public surface
  (ObserverChannel moves to signal-frame).
- Grow the macro grammar by ~3 lines (open/close operation
  names).
- Make every component's refactor simpler.

If you want, I'll dispatch agents to land the bundled fix.

## 8 · References

- `reports/designer/244-hole-finding-after-243-implementations.md`
  — the holes this rethinks.
- `reports/designer/243-reply-naming-observer-hook-executor-trait.md`
  — the designs that were implemented.
- `reports/designer/241-signal-architecture-migration-guide.md`
  — the migration spec.
- `intent/component-shape.nota` — the broader architecture
  intent.
- `intent/naming.nota` — verb-form rule.
