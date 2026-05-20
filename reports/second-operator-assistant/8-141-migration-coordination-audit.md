## 8 — /141 migration: coordination audit + Lowering::Command divergence (resolved by /246-v4)

**Lane:** second-operator-assistant
**Reads against:**
`reports/designer/246-v4-bundled-fix-deep-design-with-examples.md`
— the **now-authoritative** spec (v4 supersedes v3, v2, v1 and
/141 itself; the three-layer model + `Lowering::Command` adoption
was affirmed by the psyche 2026-05-20T02:00Z; v4 also retires
`Lowering::EngineError`, splits `AcceptedOutcome`, and standardises
observability verbs to `Tap`/`Untap`);
`reports/operator/141-signal-frame-executor-correction-examples.md`
— the migration directive the psyche pointed at; substantially
folded into /246-v4 with operator/142's logic probe driving the
refinements;
`reports/operator-assistant/<NN>` (whatever the operator-assistant
lane lands as their /141 Package 1 writeup — not yet committed);
and `intent/workspace.nota` 2026-05-20T00:30:00Z (the psyche
directive that authorised /141 as the migration target).

**v4-supersession note.** Section 2.5 below documents what was a
"divergence" between the in-flight implementation and /246-v2; v4
adopted the `Lowering::Command` extension explicitly, so the
divergence flag is now historical. The in-flight implementation
still needs further revision to match v4's other refinements —
see §3 below.

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

### 2.5 · Divergence from /246-v2 — RESOLVED by /246-v4

*(Historical: this section documented a `Lowering::Command` vs
`Lowering::EngineError` divergence between the in-flight
implementation and /246-v2. /246-v4 settled the question by
adopting the `Lowering::Command` extension as the official spec —
my §2 rationale was effectively re-derived by the designer in v4's
§0.5 three-layer model. The text below is preserved so the
sequence is legible; the actionable items move to §3 below.)*

`reports/designer/246-v2-bundled-fix-deep-design-with-examples.md`
landed during the parallel implementation work. /246-v2 was a
preliminary final spec — it folded /245's alternatives, /140's
operator corrections, and /141's concrete encoding back into a
single implementation-ready document.

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

**Which is right? — Resolved by /246-v4.** /246-v4 §0.5 names the
**three-layer model** explicitly: Contract Operation (Layer 1,
wire), Component Command (Layer 2, internal executable, owned by
each daemon), Sema Operation (Layer 3, universal payloadless
classification, observation-only). The implementation's
`Lowering::Command` IS Layer 2. The /246-v2 `Vec<SemaOperation>`
shape was the "Two-layer no-Command" trap v4's §0.5 explicitly
rejects ("forces Sema's payload to span every component's
schema").

The implementation's instinct was correct. v4 names it as the
load-bearing model and builds the rest of the spec on top.

**Pending action.** /246-v4 also retires `Lowering::EngineError` —
"engine errors arise from the component's `CommandExecutor`, which
the executor framework handles outside the `Lowering` trait
surface." Neither side of the prior divergence wins literally: the
implementation keeps `Command` but drops the engine-error
associated type entirely; /246-v2's `EngineError` doesn't survive
either.

The implementation will need further revisions to match v4 — see
§3 below.

## 2.6 · What the implementation still needs to absorb from /246-v4

/246-v4 settled four additional points beyond the
`Lowering::Command` adoption. The in-flight signal-executor and
signal-frame work needs further revisions to match. None of these
break the existing direction — they refine it.

### 2.6.1 · `OperationPlan<Command>` + `BatchPlan<Command>` instead of `Vec<Command>`

v4 §1 redefines the `lower()` return type:

```rust
fn lower(
    &self,
    operation: &Self::Operation,
) -> Result<OperationPlan<Self::Command>, Self::Reply>;

pub struct OperationPlan<Command> {
    pub commands: NonEmpty<Command>,
}

pub struct BatchPlan<Command> {
    pub operations: NonEmpty<OperationPlan<Command>>,
}
```

The in-flight implementation has `Result<Vec<Self::Command>, Self::Reply>`.
v4's `OperationPlan` makes ownership of which commands belong to
which operation **structural** — the per-op `OperationPlan` IS the
owner mapping, no `sema_op_owners: Vec<usize>` sidecar needed in
the executor. The v4 executor pseudo-code still shows
`sema_op_owners` (a v3 holdover); the structural ownership
intent is in v4's §1 "Ownership of which Sema operations a Command
produces lives **structurally** in the plan."

### 2.6.2 · `ComponentEffect` associated type on `Lowering`

v4 adds a fourth associated type:

```rust
type ComponentEffect;    // per-component effect produced by the engine
```

`reply_from_effects` takes `&[Self::ComponentEffect]` instead of
`&[SemaEffect]`. This pulls the engine's effect type into the
daemon's vocabulary, matching the Layer-2 Component-Command
discipline on both sides of execution. The implementation
currently passes `&[SemaEffect]` from `signal-executor::effect`.

### 2.6.3 · `AcceptedOutcome` split into three variants

v4 §1 splits the outcome:

```rust
pub enum AcceptedOutcome {
    Committed,
    OperationAborted {
        failed_at: usize,
        reason: OperationFailureReason,
    },
    BatchAborted {
        reason: BatchFailureReason,
        retry: RetryClassification,
        commit: CommitStatus,
    },
}
```

This is operator/142's "separate operation aborts from batch
aborts" — domain rejections from lowering produce
`OperationAborted` (with a real `failed_at`); engine failures
produce `BatchAborted` (no fake `failed_at`, carries generic
execution metadata). Plus three new enums (`BatchFailureReason`,
`RetryClassification`, `CommitStatus`).

The in-flight implementation currently uses `AcceptedOutcome::Aborted`
(no split). Both arms — lowering rejection AND engine rejection —
need updating; engine rejection no longer produces kernel
`Reply::Rejected` (see §2.6.4).

### 2.6.4 · Engine failure stays inside `Reply::Accepted` — kernel `Reply::Rejected` narrows further

This is the biggest semantic change. /141 said:

> "If `SemaEngine::execute_atomic` returns an infrastructure error, the executor does not have a contract-domain reply. That path can remain: `Reply::Rejected { reason: RequestRejectionReason::Internal }`."

v4 reverses this per operator/142:

> "engine failure is post-acceptance; Reply::Rejected is reserved for pre-acceptance frame failures only."

The wire shape for engine failure is now:

```rust
Reply::Accepted {
    outcome: AcceptedOutcome::BatchAborted {
        reason: BatchFailureReason::EngineRejected | EngineUnavailable,
        retry: RetryClassification::Retryable | NotRetryable | Unknown,
        commit: CommitStatus::NotCommitted | Unknown | Partial,
    },
    per_operation: vec![SubReply::Invalidated; payloads.len()],
}
```

Kernel `Reply::Rejected` is now reserved for **true pre-acceptance
frame failures only**: decode error, version skew, malformed frame
shape. The in-flight implementation still maps engine rejection to
kernel `Reply::Rejected { Internal }` per /141; this needs
updating.

The new `BatchFailureReason::EngineRejected` / `EngineUnavailable`
distinction, plus `RetryClassification` and `CommitStatus`, are
workspace-universal execution metadata — `signal-frame`'s `Reply`
extension gains these enums.

### 2.6.5 · Observability verbs standardised to `Tap`/`Untap`

v4 §2 retracts the contract-author-named open/close verbs from /141
and /246-v2. Per psyche affirmation 2026-05-20T02:00Z, **persona
components must declare an `observable` block, and the macro
injects the standardised `Tap`/`Untap` verbs with no author
override**. Domain contracts that want their own `Tap` verb rename
their domain verb. Non-persona small utilities don't declare the
block.

This affects Package 2 (signal-frame macro grammar). The in-flight
macro work at `/git/.../signal-frame onxlynko` likely needs
revision: the v3-shape grammar `observable { open Watch(Filter); close Unwatch; … }`
that /141 specified is no longer the target. The v4 grammar is:

```rust
observable {
    filter <FilterType>;                  // or `filter default;`
    operation_event <OperationEventType>;
    effect_event <EffectEventType>;
}
```

No `open` / `close` lines — the macro injects `Tap(<FilterType>) opens <Channel>ObserverStream`
and `Untap(<Channel>ObserverSubscriptionToken)` automatically.

### 2.6.6 · Projection bridge via `ObservedLowering: Lowering` extension trait

Package 3 in /141 was deferred for design; v4 §3 lands the design:

```rust
// In signal-executor:
pub trait ObservedLowering: Lowering {
    type OperationEvent;
    type EffectEvent;

    fn project_operation(&self, operation: &Self::Operation) -> Self::OperationEvent;
    fn project_effect(&self, effect: &Self::ComponentEffect) -> Self::EffectEvent;
}
```

```rust
// In signal-frame:
pub trait ObserverFanout<OperationEvent, EffectEvent> {
    fn publish_operation(&mut self, event: OperationEvent);
    fn publish_effect(&mut self, event: EffectEvent);
}
```

The macro-emitted `<Channel>ObserverSet` impls
`ObserverFanout<OperationEvent, EffectEvent>`. The daemon-side
`Executor::execute` calls `project_operation` / `project_effect`
on `ObservedLowering` and publishes through `ObserverFanout`.

This unblocks Package 3 — it no longer needs a separate design
pass. The shape was demonstrated working in operator/142's logic
probe at `/tmp/signal-frame-executor-246-probe/model.rs`.

### 2.6.7 · The `Tap`/`Untap` standardisation gates the macro grammar work

If signal-frame's in-flight macro work is implementing v3's
contract-author-named open/close grammar, it needs to be retargeted
to v4's mandatory-standardised shape before commit. This is small
work but worth catching before the macro commits cement a shape
v4 already retired.

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

## 6 · Recommendations — v4-aligned

In priority order (revised after /246-v4):

1. **Operator lane / operator-assistant lane** working on Package 1: realign to v4 before commit. The biggest deltas: (a) `OperationPlan<Command>` + `BatchPlan<Command>` replace `Vec<Command>`; (b) add `Lowering::ComponentEffect` associated type; (c) split `AcceptedOutcome` into `Committed` / `OperationAborted` / `BatchAborted`; (d) engine failure produces `Reply::Accepted` with `BatchAborted`, NOT kernel `Reply::Rejected` — this reverses /141's engine-rejection-as-kernel-rejection. The `kernel_rejection_does_not_carry_contract_reply` named test from /141 needs renaming + reshaping to `engine_failure_produces_batch_aborted_not_kernel_rejection` to match v4.
2. **Signal-frame `Reply`/`SubReply` extension work**: add three new enums (`BatchFailureReason`, `RetryClassification`, `CommitStatus`) to `signal-frame/src/reply.rs`; split `AcceptedOutcome::Aborted` into `OperationAborted` + `BatchAborted` per v4 §1. Widen `SubReply::Invalidated` doc per v4 §1's footnote.
3. **Signal-frame macro grammar work** (Package 2 in flight at `onxlynko`): retarget to v4's mandatory-standardised `Tap`/`Untap` grammar. The contract-author-named `open Verb(Filter); close Verb;` shape from /141 is RETIRED. The v4 grammar declares only filter + event types; the macro injects standardised verbs. This is small work but worth catching before macro changes commit.
4. **Package 3 (projection bridge) unblocks** — v4 §3 lands the design as the `ObservedLowering: Lowering` extension trait + `ObserverFanout<OperationEvent, EffectEvent>` primitive. Operator/142's logic probe demonstrated it compiles. No designer-lane gate needed; whichever operator has bandwidth can implement.
5. **Signal-executor's `ARCHITECTURE.md` update** must wait for the v4-aligned implementation to settle; written alongside the Package 1 commit by whichever lane commits.
6. **Per-component cascade waits for v4 settling.** The persona daemon cascade (signal-persona-mind, -router, -message, -harness, -terminal) needs the v4 trait shapes locked before it begins — report 7's §3 sequencing applies, now refined: wait for v4's `Lowering` shape + `ObservedLowering` extension to land in code, not just in spec.

## 7 · See also

- `reports/designer/246-v4-bundled-fix-deep-design-with-examples.md` — the now-authoritative spec; v4 supersedes v3, v2, v1, /141, /245. Adopts three-layer model + `Lowering::Command` + `OperationPlan` + `AcceptedOutcome` split + standardised `Tap`/`Untap` + `ObservedLowering: Lowering` extension trait.
- `reports/operator/141-signal-frame-executor-correction-examples.md` — the migration directive the psyche pointed at; substantially folded into /246-v4 with operator/142's logic probe driving the refinements.
- `reports/operator/142-signal-frame-executor-bundled-fix-logic-probe.md` — the logic probe that drove three of v4's refinements (separate operation aborts from batch aborts; `ObservedLowering: Lowering` extension trait; engine failure stays inside `Reply::Accepted`).
- `reports/operator/143-signal-infrastructure-convergence-and-pilot-pivot.md` — operator's pivot from full cascade to "smallest convergence bundle + drive repository-ledger pilot end-to-end". Reframes §6 recommendations: §6 #1 (Package 1 v4 alignment) is the immediate work; §6 #6 (persona daemon cascade) explicitly waits for the pilot to validate the pattern.
- `reports/designer/248-three-layer-changes-for-operators.md` — operator-facing diff between v3 and v4: per-crate work items for `signal-sema` (payloadless), `signal-executor` (Command + ComponentEffect + CommandExecutor), `signal-frame` (Tap/Untap mandatory), contract crates, and daemon crates. Complementary to this report's §2.6; same substance organised by crate.
- `reports/designer/249-component-intent-gap-analysis.md` — orthogonal but adjacent: ten high-severity persona intent gaps. Two intersect with this work: gap 4 (does /246-v4's `Tap`/`Untap` match the universal-observer-hook the psyche intended in `intent/component-shape.nota` 2026-05-19T20:00Z?) and gap 5 (`persona` engine-manager triad status). Neither blocks Package 1 but worth flagging if the pilot exposes contradictions.
- `reports/operator/140-signal-frame-executor-hole-analysis.md` — /141's predecessor; load-bearing for the rejection-as-`Aborted` design.
- `reports/designer/244-hole-finding-after-243-implementations.md`, `reports/designer/245-design-alternatives-for-244-holes.md` — the holes /141 closes (and the literal /245 moves /141 corrected).
- `reports/second-operator-assistant/7-signal-persona-migration-deeper-holes.md` — my prior analysis; §3 sequencing names /141's load-bearing position for the persona daemon cascade.
- `intent/workspace.nota` 2026-05-20T00:30:00Z — the psyche directive authorising /141 as the migration target.
- `/git/github.com/LiGoldragon/signal-executor` `wymxwksy` — the in-flight Package 1 working copy (uncommitted at time of writing).
- `/git/github.com/LiGoldragon/signal-frame` `onxlynko` — the in-flight Package 2 working copy (uncommitted at time of writing).
- `/home/li/wt/.../signal-frame-executor-report-141` — the operator-assistant lane's separate worktree (per their lock).
