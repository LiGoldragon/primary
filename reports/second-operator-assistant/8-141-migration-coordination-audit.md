## 8 — /141 migration: coordination audit + Lowering::Command divergence

**Lane:** second-operator-assistant
**Reads against:** `reports/operator/141-signal-frame-executor-correction-examples.md`
(the migration directive the psyche pointed at);
`reports/designer/246-v2-bundled-fix-deep-design-with-examples.md`
(the **now-authoritative** implementation-ready spec, which folded
/141's corrections back into the bundled fix and was committed
during the parallel work — see §2.5 below for the
`Lowering::Command` divergence between /246-v2's spec and the
in-flight implementation);
`reports/operator-assistant/<NN>` (whatever the operator-assistant
lane lands as their /141 Package 1 writeup — not yet committed);
and `intent/workspace.nota` 2026-05-20T00:30:00Z (the psyche
directive that authorised /141 as the migration target).

## 0 · TL;DR

The psyche directive "start a migration that follows /141" produced
**three concurrent lanes** working in parallel:

| Lane | Scope | Worktree | Status (as of 2026-05-20 11:48Z) |
|---|---|---|---|
| operator-assistant | /141 Package 1 (signal-executor rejection semantics) | `/home/li/wt/.../signal-frame-executor-report-141` | claimed at 11:46; uncommitted in that worktree |
| operator (probable) | /141 Package 1 in main signal-executor worktree | `/git/github.com/LiGoldragon/signal-executor` | uncommitted `wymxwksy` — substantive edits across `src/{lowering,executor,engine,lib}.rs`, `tests/{round_trip,counter/mod}.rs`, `README.md` |
| operator (probable) | /141 Package 2 (signal-frame observable grammar) | `/git/github.com/LiGoldragon/signal-frame` | uncommitted `onxlynko` — edits across `macros/src/{emit,model,parse}.rs` |
| second-operator-assistant (this lane) | initially claimed signal-executor Package 1; **released after discovering parallel work** | n/a | audit report only |

The implementation in the main signal-executor worktree goes
**beyond /141's prescription** in one important way (the
`Lowering::Command` extension, §2 below) — a design improvement worth
naming explicitly so reviewers don't flag it as drift.

This report does three things:

1. Documents the parallel-lane state so future readers understand
   why my lane is empty-handed despite the same psyche directive.
2. Audits the in-flight Package 1 implementation against /141's
   prescription and report 7's recommendations.
3. Names the residual items that the active lanes have not yet
   reached, so they can be picked up without re-discovery.

## 1 · What's landed in the main signal-executor worktree

Substantive `wymxwksy` working-copy state, file by file. None of
this is committed yet.

### `src/lowering.rs`

- `Lowering::RejectionReason` associated type **removed**.
- `Lowering::Command` associated type **added** — see §2.
- `lower()` signature now `fn lower(&self, operation: &Self::Operation) -> Result<Vec<Self::Command>, Self::Reply>` — return type matches /141's prescription on the success side and the contract-reply-as-`Err` on the rejection side.
- Trait-level docstring rewritten to explain the contract-reply-on-Err shape and the per-op `Failed.detail` correlation.

### `src/engine.rs`

- `SemaEngine::Command` associated type **added** — paired with `Lowering::Command` via the `Executor`'s `where SemaEngineImpl: SemaEngine<Command = LoweringImpl::Command>` bound.
- `execute_atomic` signature now `fn execute_atomic(&mut self, commands: Vec<Self::Command>) -> Result<Vec<SemaEffect>, Self::Error>` — engine consumes the daemon's command vocabulary, not `Vec<SemaOperation>`.
- Docstring explains that `Self::Command` is deliberately *not* `signal_sema::SemaOperation` — see §2.

### `src/executor.rs`

- `Executor::execute()` rewritten. On lowering `Err(reply)`, the executor builds the kernel `Reply::Accepted { outcome: AcceptedOutcome::Aborted { failed_at, reason: DomainRejection }, per_operation }` where `per_operation` is `[Invalidated × failed_at, Failed { detail: Some(reply) }, Skipped × (total - failed_at - 1)]`. The helper `Self::domain_rejection_reply` builds the array deterministically.
- `ExecutorOutcome::LoweringRejected` field changed: the old `reason: LoweringImpl::RejectionReason` field is gone; the new field is `failed_at: usize`. The typed contract rejection now lives inside the wire `reply.per_operation[failed_at].detail`.
- `ExecutorOutcome::EngineRejected` unchanged — engine rejection still produces the kernel `Reply::Rejected { reason: Internal }` per /141 §"Engine rejection stays kernel-shaped."

### `tests/round_trip.rs`

- `lowering_rejection_does_not_call_engine` updated: now asserts the new `Reply::Accepted { Aborted }` shape with `SubReply::Failed { reason: DomainRejection, detail: Some(CounterReply::MagnitudeRejected { .. }) }`.
- `multi_operation_lowering_rejection_invalidates_skips_and_fails` added — exact /141 §1 multi-op example test. Asserts `[Invalidated, Failed.detail, Skipped]` per-op array on a 3-op request where op[1] returns `Err`.
- `outcome_reply_accessor_works_for_every_variant` updated: lowering-rejection branch now asserts `Reply::Accepted { Aborted, .. }` instead of `Reply::Rejected`.

### `tests/counter/mod.rs`

- `CounterReply::MagnitudeRejected { reason: CounterRejectionReason }` variant added — the contract reply variant that rides in `Failed.detail`.
- `CounterCommand` enum added: `Increment { magnitude }`, `Decrement { magnitude }`, `Query`. This is what the `Lowering` emits and the `SemaEngine` consumes.
- `CounterLowering::lower()` returns `Result<Vec<CounterCommand>, CounterReply>` — typed contract reply on `Err`.
- `CounterEngine::execute_atomic()` takes `Vec<CounterCommand>` and projects each command to a canned `SemaEffect`.

## 2 · The `Lowering::Command` extension — design improvement

/141 prescribed `lower()` returning `Result<Vec<SemaOperation>, Self::Reply>`. The main-worktree implementation went further: an associated `type Command` on both `Lowering` and `SemaEngine`, with the executor parameterised by `SemaEngineImpl: SemaEngine<Command = LoweringImpl::Command>`.

**Why this is right.** `SemaOperation` is the workspace's
operation **class** vocabulary (`Assert`, `Mutate`, `Retract`,
`Match`, `Subscribe`, `Validate`) — six closed verbs naming what
the engine *does* to durable state. But to actually execute, the
engine needs the **table**, the **record**, the **slot**, the
**revision**, the **read plan**, or the **subscription target** —
data that `SemaOperation` (an enum of bare variants without
payloads) cannot carry.

The pre-/141 `Lowering` returned `Vec<SemaOperation>`, which was a
type-system lie: in any real daemon the executor needs more than
the bare operation class to commit. The `Lowering::Command` extension
makes that explicit. A daemon's `Command` enum carries the actual
executable shape; the `SemaOperation` projection is for **observation**
(what shows up on the wire as `SemaEffectEmitted` for an
`observable`-block subscriber), not for execution.

This aligns with `skills/typed-records-over-flags.md` §"Surface
the variant set in the type system": when the type system can name
what flows through a boundary, it should. The contract author owns
the daemon's execution vocabulary; the executor's only constraint
is that lowering's output matches what the engine consumes.

**Worth promoting to /141's text.** The text currently shows
`lower() -> Result<Vec<SemaOperation>, Self::Reply>`. A v2 of /141
(or a follow-up report) should name the `Command` decoupling
explicitly so future daemon authors don't write `Vec<SemaOperation>`
when they mean `Vec<MyDaemonCommand>`.

**Cross-walk with report 7 Finding 5.** Report 7 §3 said the
persona daemon cascade should not start until /141's bundled
fix lands. The `Lowering::Command` extension reinforces this: a
persona daemon will need its own `Command` enum (e.g.
`SpiritCommand` carrying typed `Slot`, `Statement`, `Revision`
fields). Daemons that try to lower directly to bare
`SemaOperation` will hit the type-system lie immediately.

### 2.5 · Divergence from /246-v2 (the now-authoritative spec)

`reports/designer/246-v2-bundled-fix-deep-design-with-examples.md`
landed during the parallel implementation work. /246-v2 is the
final spec — it folds /245's alternatives, /140's operator
corrections, and /141's concrete encoding back into a single
implementation-ready document. It supersedes /141 as the
authoritative directive.

**/246-v2's `Lowering` trait shape:**

```rust
pub trait Lowering {
    type Operation: RequestPayload;
    type Reply;
    type EngineError;  // ← /246-v2's third associated type

    fn lower(
        &self,
        operation: &Self::Operation,
    ) -> Result<Vec<SemaOperation>, Self::Reply>;  // ← bare SemaOperation, not Command

    fn reply_from_effects(
        &self,
        operation: &Self::Operation,
        effects: &[SemaEffect],
    ) -> Self::Reply;
}
```

**The in-flight implementation's `Lowering` trait shape:**

```rust
pub trait Lowering {
    type Operation: RequestPayload;
    type Reply;
    type Command;  // ← implementation chose Command instead of EngineError

    fn lower(
        &self,
        operation: &Self::Operation,
    ) -> Result<Vec<Self::Command>, Self::Reply>;  // ← Command, not SemaOperation

    fn reply_from_effects(
        &self,
        operation: &Self::Operation,
        effects: &[SemaEffect],
    ) -> Self::Reply;
}
```

Two divergences:

1. **`Command` vs `SemaOperation` return type.** /246-v2's spec
   says `lower()` returns `Vec<SemaOperation>` (bare operation
   class). The implementation says `Vec<Self::Command>` (typed
   executable command). The implementation's choice is richer —
   it acknowledges that `SemaOperation` is a six-variant unit
   enum that cannot carry the table / record / slot / revision
   data needed to execute. See §2 above for the rationale.
2. **`EngineError` vs `Command` associated type.** /246-v2 has
   `EngineError` (presumably to let the executor surface engine
   errors through a typed associated type on the daemon's
   Lowering side). The implementation has `Command` (paired with
   `SemaEngine::Command` via the executor's bound) and lets the
   engine's own `Error` type stay on the `SemaEngine` trait.

**Which is right?** Both have merit. /246-v2 keeps the executor's
type surface minimal (the engine is fully generic over its own
`Error`). The implementation's `Command` couples Lowering and
SemaEngine on a shared command vocabulary, which makes the
engine's actual execution payload visible at the type level — a
type-system-honest abstraction.

**The decision belongs to the designer lane.** The implementation
landed first; /246-v2 followed. If /246-v2 wins, the implementation
should drop `Command`, change `lower()` back to
`Result<Vec<SemaOperation>, Self::Reply>`, and add `EngineError`.
If `Command` wins, /246-v2 needs an update naming the
`Lowering::Command` + `SemaEngine::Command<=` pairing as the final
shape. A small designer-lane report (let's call it /247) would
close this.

**Pending recommendation #5 in §6** is now sharpened: the rationale
in §2 of THIS report should be the input that designer lane uses
to write /247.

## 3 · What's landed in signal-frame (Package 2 in flight)

The main signal-frame worktree (`onxlynko 66d21021`) has uncommitted
edits to:

- `macros/src/emit.rs`
- `macros/src/model.rs`
- `macros/src/parse.rs`

This is the /141 Package 2 grammar change. I have not read the
edits — coordinating from another lane would risk stepping on
in-flight work. The expected shape per /141 §2:

```rust
observable {
    open Watch(ObserverFilter);     // contract author names the open verb
    close Unwatch;                   // contract author names the close verb; payload is macro-owned
    filter ObserverFilter;
    event OperationReceived;
    event SemaEffectEmitted;
}
```

The macro should emit a typed token (`<Channel>ObserverSubscriptionToken`) as the close payload. The validation pass should drop the hard-coded `Observe` / `Unobserve` collision check and check the contract-author-chosen names instead.

## 4 · What's NOT yet landed

Items in /141 + report 7 that the active lanes have not reached.
These are picked up when the in-flight work commits, by whichever
lane has bandwidth.

### 4.1 · The `kernel_rejection_does_not_carry_contract_reply` named test

/141 §"Implementation Consequences" listed three test names for
Package 1. The main worktree has two of three:

| /141 test name | Main-worktree status |
|---|---|
| `lowering_rejection_returns_typed_failed_subreply` | covered by `lowering_rejection_does_not_call_engine` — assertion content matches, name differs |
| `multi_operation_lowering_rejection_invalidates_skips_and_fails` | landed under that exact name |
| `kernel_rejection_does_not_carry_contract_reply` | assertion content split across `engine_rejection_when_atomic_fails` + `outcome_reply_accessor_works_for_every_variant`; no single test bears this name |

Adding a single test that explicitly asserts "kernel rejection from `execute_atomic` produces `Reply::Rejected { reason: Internal }` AND no contract reply variant is visible on the wire" would close the gap. Small additive change, no conflict with in-flight work.

### 4.2 · signal-frame `SubReply::Invalidated` docs widening

/141 §1's footnote called out:

> `signal-frame`'s `SubReply::Invalidated` docs currently lean toward "operation ran but its result is no longer authoritative." For this use, it also covers "operation was planned/lowered but invalidated before commit." That doc should be widened or a more precise variant should be introduced if that wording feels too elastic.

The Package-1 use case for lowering rejection sets `Invalidated` on operations that lowered successfully but whose results never reached the engine (because a later operation failed lowering). They didn't "run" in the engine sense. The current doc at `signal-frame/src/reply.rs` lines 112-114 needs widening. One-line edit; small file; isolated from the in-flight `macros/src/*` Package 2 edits.

### 4.3 · ARCHITECTURE.md updates

`signal-executor/ARCHITECTURE.md` will need updating for the new
failure-mode taxonomy:

- The "lowering rejection" path now produces `Reply::Accepted { Aborted }` not `Reply::Rejected`.
- The `Lowering::Command` associated type joins the trait surface.
- The `SemaEngine::Command` constraint is paired.

Best landed alongside the Package 1 commit by whichever lane commits.

### 4.4 · Package 3 — projection-boundary design pass

/141 §3 explicitly says **do not implement Package 3 literally
without another design pass**. The projection boundary (how
execution facts in `signal-executor` become channel event records
in the contract crate) is the open design question. Until that
settles:

- The `signal-executor::ObserverChannel<Operation>` trait stays where it is.
- The `signal-frame::observable` block stays a no-impl scaffold for the publish-bridge integration.
- Persona daemons that want observability remain blocked on this.

This is **designer-lane work**, not operator. The right next move
is for a designer to land /146 (or whichever next-number) naming
the projection-boundary resolution. Operator lanes wait.

## 5 · Why my lane has no code

Two reasons, in order:

1. **Discipline.** When I claimed the second-operator-assistant lock for "signal-executor Package 1" at 11:43, the `operator-assistant` lock was empty. By 11:46 the operator-assistant lane had claimed a separate worktree for the same scope, and the main signal-executor worktree was actively being edited (likely by operator). Three lanes converging on the same scope produces conflicts and wasted work; my lane released its claim and switched to audit mode.
2. **No value in duplicate landing.** /141's Package 1 is a well-specified change. The main-worktree implementation matches the prescription (and exceeds it with `Lowering::Command`). Re-implementing in my own worktree would produce a parallel branch that has to be reconciled. Auditing + naming the design extension + flagging the residual items is the higher-value contribution from a third lane.

## 6 · Recommendations

In priority order:

1. **Whichever lane commits Package 1 first**: add the `kernel_rejection_does_not_carry_contract_reply` named test (§4.1) so all three /141-named tests are on disk.
2. **Whichever lane has bandwidth for signal-frame**: widen the `SubReply::Invalidated` doc in `signal-frame/src/reply.rs` lines 112-114 per /141 §1's footnote. One-line edit; non-conflicting with Package 2 grammar work.
3. **Whichever lane commits Package 1**: update `signal-executor/ARCHITECTURE.md` for the new failure-mode taxonomy and the `Lowering::Command` extension (§4.3).
4. **A designer lane**: open /146 (or appropriate number) on the projection-boundary resolution (§4.4) so Package 3 unblocks.
5. **A future report by whichever operator lane lands the work**: include a one-paragraph callout that `Lowering::Command` was added beyond /141's prescription, with the rationale from §2 of this report so reviewers don't flag it as drift.

## 7 · See also

- `reports/designer/246-v2-bundled-fix-deep-design-with-examples.md` — the now-authoritative implementation-ready spec; supersedes /141 + /245.
- `reports/operator/141-signal-frame-executor-correction-examples.md` — the migration directive the psyche pointed at; folded into /246-v2.
- `reports/operator/140-signal-frame-executor-hole-analysis.md` — /141's predecessor; load-bearing for the rejection-as-`Aborted` design.
- `reports/designer/244-hole-finding-after-243-implementations.md`, `reports/designer/245-design-alternatives-for-244-holes.md` — the holes /141 closes (and the literal /245 moves /141 corrected).
- `reports/second-operator-assistant/7-signal-persona-migration-deeper-holes.md` — my prior analysis; §3 sequencing names /141's load-bearing position for the persona daemon cascade.
- `intent/workspace.nota` 2026-05-20T00:30:00Z — the psyche directive authorising /141 as the migration target.
- `/git/github.com/LiGoldragon/signal-executor` `wymxwksy` — the in-flight Package 1 working copy (uncommitted at time of writing).
- `/git/github.com/LiGoldragon/signal-frame` `onxlynko` — the in-flight Package 2 working copy (uncommitted at time of writing).
- `/home/li/wt/.../signal-frame-executor-report-141` — the operator-assistant lane's separate worktree (per their lock).
