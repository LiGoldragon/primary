# 128 — Signal executor and observation hole-finding

*Fresh hole-finding pass after the /243 implementations, considering
`reports/designer/244-hole-finding-after-243-implementations.md` and
`reports/designer/245-design-alternatives-for-244-holes.md`.*

## 0 · TL;DR

The foundation crates are compiling and their local tests pass, but
the current design is still not ready as the shared executor path for
real triad daemons.

The central issue is that the system has split public contract verbs
from Sema operations, but the executor has not yet grown the typed
command layer that must sit between them. `signal-executor` lowers
contract operations to `Vec<SemaOperation>`, but `SemaOperation` is
only a class tag (`Assert`, `Match`, etc.). It cannot say which table,
record, slot, pattern, read plan, or subscription target the engine
should execute.

The second issue is that observation was bolted to the macro and the
executor from opposite sides. The macro injects fixed `Observe` /
`Unobserve` operations and a low-level observer set; the executor owns
an unrelated `ObserverChannel` trait and only publishes operation and
effect events. No one owns the full open / close / publish / stream
delivery path.

The third issue is documentation drift. Some permanent skills and
architecture files now contradict the implemented direction or cite
ephemeral reports even though the workspace skills explicitly forbid
that. This matters because agents refresh skills before work; stale
skills will recreate the old universal-verb design.

## 1 · Sources refreshed

I refreshed the relevant workspace skills before auditing:

- `ESSENCE.md`
- `repos/lore/AGENTS.md`
- `skills/skills.nota`
- `orchestrate/AGENTS.md`
- `skills/designer.md`
- `skills/component-triad.md`
- `skills/contract-repo.md`
- `skills/abstractions.md`
- `skills/naming.md`
- `skills/language-design.md`
- `skills/beauty.md`
- `skills/micro-components.md`
- `skills/actor-systems.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`
- `skills/reporting.md`
- `skills/rust-discipline.md`
- `skills/rust/methods.md`
- `skills/rust/errors.md`
- `skills/rust/storage-and-wire.md`
- `skills/rust/parsers.md`
- `skills/rust/crate-layout.md`
- `skills/testing.md`
- `skills/push-not-pull.md`
- `skills/skill-editor.md`
- `skills/jj.md`

`ONBOARDING.md` is still referenced by `AGENTS.md`, but is not present
in `/home/li/primary`.

I then read:

- `reports/designer/241-signal-architecture-migration-guide.md`
- `reports/designer/243-reply-naming-observer-hook-executor-trait.md`
- `reports/designer/244-hole-finding-after-243-implementations.md`
- `reports/designer/245-design-alternatives-for-244-holes.md`
- `/git/github.com/LiGoldragon/signal-frame/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-frame/macros/README.md`
- `/git/github.com/LiGoldragon/signal-executor/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-sema/ARCHITECTURE.md`
- the implementation files in `signal-frame`, `signal-executor`, and
  `signal-sema` named in this report.

## 2 · Verification run

The current implementation passes its local test suites:

```text
/git/github.com/LiGoldragon/signal-executor
CARGO_BUILD_JOBS=1 cargo test --all-targets
18 tests passed

/git/github.com/LiGoldragon/signal-frame
CARGO_BUILD_JOBS=1 cargo test --all-targets
30 tests passed

/git/github.com/LiGoldragon/signal-sema
CARGO_BUILD_JOBS=1 cargo test --all-targets
30 tests passed
```

So the holes below are not "tests are red" findings. They are
architecture holes: the implemented slices are locally coherent, but
the design cannot yet be cleanly used by a real daemon.

## 3 · Hole A — the executor lowers to operation labels, not executable commands

`signal-executor/src/lowering.rs` currently defines:

```rust
fn lower(
    &self,
    operation: &Self::Operation,
) -> Result<Vec<SemaOperation>, Self::RejectionReason>;
```

`signal-executor/src/engine.rs` then executes:

```rust
fn execute_atomic(&mut self, ops: Vec<SemaOperation>) -> Result<Vec<SemaEffect>, Self::Error>;
```

This is the biggest hole. `SemaOperation::Assert` is not an
executable command. It does not carry the record to assert.
`SemaOperation::Match` does not carry a read plan. `Mutate` does not
carry slot, revision, target table, or replacement record.

The current tests hide this because `tests/counter/mod.rs` uses a
mock engine that maps bare class tags to canned effects. A real
daemon cannot use this to write a Sema table without a side channel.

Recommended shape:

```rust
trait Lowering {
    type Operation;
    type Reply;
    type Command;

    fn lower(&self, operation: &Self::Operation)
        -> Result<Vec<Self::Command>, Self::Reply>;

    fn operation_class(&self, command: &Self::Command) -> SemaOperation;
}

trait SemaEngine {
    type Command;
    type Error;

    fn execute_atomic(
        &mut self,
        commands: Vec<Self::Command>,
    ) -> Result<Vec<SemaEffect>, Self::Error>;
}
```

The command is the daemon/engine-specific executable plan. The
`SemaOperation` remains useful as the operation class for observation,
classification, policy, and metrics. It must not pretend to be enough
to execute state.

This sharpens /245: the `lower()` return should not be
`Result<Vec<SemaOperation>, Self::Reply>`; it should be
`Result<Vec<Self::Command>, Self::Reply>`, with a way to project each
command to a `SemaOperation` class.

## 4 · Hole B — domain rejection still collapses to `Internal`

`signal-executor/src/executor.rs` still returns this wire reply when
lowering rejects:

```rust
Reply::Rejected {
    reason: RequestRejectionReason::Internal,
}
```

The typed rejection reason survives only daemon-side in
`ExecutorOutcome::LoweringRejected { reason, .. }`.

That violates the new reply discipline. A contract-domain rejection
should cross the wire as a contract reply variant, e.g.
`SubmitRejected(SubmitRejectionReason)` or
`ConfigureRejected(ConfigureRejectionReason)`, not as kernel
`Internal`.

The clean fix is the same as Hole A: `lower()` returns
`Err(Self::Reply)`. Domain rejection is a reply payload chosen by the
contract. Kernel `Reply::Rejected { Internal }` remains for true
frame/protocol/pre-execution failures that are not domain replies.

## 5 · Hole C — observer open/close lifecycle has no owner

`signal-frame`'s macro emits:

- `Observe(Filter)` and `Unobserve(Token)` operations
- `ObserverStream`
- `ObserverSubscriptionOpened`
- `<Channel>ObserverSet::register`
- `<Channel>ObserverSet::unregister`
- `publish_<event>(event, deliver)`

`signal-executor` owns:

- `ObserverChannel<Operation>`
- `ObserverSet<Operation>`
- `publish_operation_received`
- `publish_sema_effect_emitted`

Those are not the same surface. The executor only knows how to
publish. It does not know that an inbound operation is the observer
open operation, it does not mint or return the macro-generated token,
and it does not unregister. The macro-generated observer set knows
how to register and publish, but it has no executor trait and no
production socket delivery policy.

/245's "move `ObserverChannel` to `signal-frame` and have the macro
emit the impl" is the right direction, but it needs to cover the full
lifecycle:

1. Open: contract-named observer-open operation registers a filter and
   returns the opened token.
2. Close: contract-named observer-close operation unregisters the
   token and returns a typed closed outcome.
3. Publish: execution events fan out to matching live subscribers.
4. Stream delivery: matching events become streaming frames on the
   right subscription token.

If the bridge only covers publish, every daemon will still hand-roll
open and close.

## 6 · Hole D — fixed `Observe` / `Unobserve` fights contract-local verbs

`signal-frame/macros/src/emit.rs` still injects fixed operation names:

```rust
let observe_variant_name = ident("Observe", span);
let unobserve_variant_name = ident("Unobserve", span);
```

`signal-frame/macros/src/validate.rs` rejects a contract that already
declares `Observe`.

That contradicts the contract-local verb direction. `Observe` is a
natural public domain verb; the macro should not reserve it globally
for its internal observation surface.

Recommended shape: the `observable` block names its open and close
operations explicitly:

```rust
observable {
    open Watch(ObserverFilter) opens ObserverStream;
    close Unwatch(ObserverSubscriptionToken);
    event OperationReceived;
    event SemaEffectEmitted;
}
```

The exact grammar can change, but the principle is clear: the contract
author names public verbs; the macro enforces shape.

## 7 · Hole E — effect-to-reply correlation is not reliable for real multi-operation requests

`Lowering::reply_from_effects` receives the full effect slice for
each operation:

```rust
fn reply_from_effects(
    &self,
    operation: &Self::Operation,
    effects: &[SemaEffect],
) -> Self::Reply;
```

For duplicate operations or operations that lower to different-length
command sequences, this is ambiguous. The current counter mock uses
helpers like "first wrote effect for Assert"; that is not a real
correlation strategy. Two identical operations can both find the first
matching effect and produce the same reply.

The executor needs to retain an execution plan that records which
source operation produced which command span, and then which command
span produced which effect span:

```rust
struct OperationExecution<'effects> {
    operation_index: usize,
    effects: &'effects [SemaEffect],
}
```

Then `reply_from_effects` becomes:

```rust
fn reply_from_execution(
    &self,
    operation: &Self::Operation,
    execution: OperationExecution<'_>,
) -> Self::Reply;
```

This makes zero-effect operations, multi-effect operations, and
duplicate operations explicit.

## 8 · Hole F — observer streams do not report terminal outcomes

The executor currently publishes:

- operation received
- Sema effect emitted after successful commit

It does not publish:

- lowering rejected
- engine rejected
- request execution completed
- accepted zero-effect operation

From an observer's perspective, "operation received and then no
effect" can mean:

- the operation was accepted and intentionally had no state effect;
- lowering rejected it;
- the engine rejected the request;
- the daemon died before publishing more.

That is not enough for `persona-introspect` or any debugging agent
trying to understand a daemon's behavior.

The observable event set should include terminal outcome events. A
minimum set:

- `OperationLoweringRejected`
- `RequestEngineRejected`
- `RequestExecutionCompleted`

If the executor grows operation/effect span correlation, the terminal
events can also carry operation index and request exchange identity.

## 9 · Hole G — the observation authority and redaction model is still too casual

`reports/designer/243-reply-naming-observer-hook-executor-trait.md`
states that subscription on the public socket is fine because
observation is not security-sensitive. That can be true for a
development system or for event classes that carry only class labels,
but it is not universally true.

If observer events carry full inbound operations, those operations may
include messages, paths, configuration, persona state, or future auth
material. If they carry full Sema commands or effects, they may expose
private state transitions.

The design needs an event-class policy:

- public observable event classes: safe for the public component
  socket;
- owner observable event classes: only on the owner-signal socket;
- redacted event classes: public shape with sensitive fields removed;
- forbidden event classes: never emitted.

This does not need to block the development prototype, but the current
"observation is not security-sensitive" wording is too broad to be a
permanent invariant.

## 10 · Hole H — frame request/reply names still imply executor semantics

`signal-frame/ARCHITECTURE.md` correctly says database atomicity
belongs below the frame layer. But `signal-frame/src/request.rs` still
says:

```rust
/// One or more contract payloads that commit (or abort) as one unit.
/// ... Atomicity is structural ...
```

`signal-frame/src/reply.rs` still owns `AcceptedOutcome::Aborted` and
`OperationFailureReason`. That may be legitimate if frame replies
represent a generic ordered batch result, but the language still reads
like the frame layer owns commit/abort execution semantics.

This is a naming and responsibility smell:

- If `Request<Payload>` is only an ordered non-empty exchange unit,
  its docs should say ordered exchange unit, not commit unit.
- If `AcceptedOutcome::Aborted` is only for executor-style atomic
  processing, it may belong in `signal-executor`, not `signal-frame`.
- If every frame reply may carry per-operation partial failure, then
  the frame layer is not entirely execution-free and the architecture
  should say exactly what generic execution semantics it owns.

The current mixed language will confuse contract authors.

## 11 · Hole I — the macro observer set is a low-level primitive, not production daemon shape

The generated `<Channel>ObserverSet` stores a `Vec` and publishes by
iterating it while the caller-provided delivery closure runs:

```rust
for subscription in &self.subscriptions {
    if filter.matches(event) {
        deliver(subscription.token, event);
    }
}
```

That is acceptable as a low-level single-threaded primitive and a
macro witness. It is not enough as the recommended production daemon
shape. A real daemon will have concurrent socket tasks; holding the
observer registry while writing frames lets one slow subscriber block
registration, unregistration, and event delivery.

The production bridge should snapshot matching recipients under the
registry lock, release the lock, then deliver frames. If delivery is
fallible, the bridge must also decide whether failures unregister
subscribers, report terminal errors, or leave cleanup to the stream
owner.

The generated token uses `wrapping_add`. In practice wraparound is far
away, but the correct primitive should avoid issuing a duplicate token
or return a typed "observer capacity exhausted" rejection.

## 12 · Hole J — permanent guidance is split-brained and cites reports

The skill refresh exposed concrete contradictions:

- `skills/component-triad.md` still says the daemon external surface is
  exclusively `signal-core` frames and that each request enum variant
  carries one of six `SignalVerb` roots.
- `skills/skills.nota` still describes `contract-repo` as "Six-verb
  spine; signal_channel! macro".
- `skills/component-triad.md` still points at
  `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md`.
- `skills/contract-repo.md` has mostly moved to contract-local verbs,
  but still cites reports in its permanent "See also" section.
- `skills/subscription-lifecycle.md` still names `signal-core` macro
  paths.
- `signal-sema/ARCHITECTURE.md`, `signal-executor/ARCHITECTURE.md`,
  `signal-executor/src/lib.rs`, `signal-frame/AGENTS.md`, and README
  files cite reports as permanent references.

This violates the permanent-doc rule in `skills/architecture-editor.md`
and `skills/skill-editor.md`: architecture files and skills do not
cite reports. The load-bearing shape must be inlined into permanent
docs once it is current architecture.

This is a high-priority cleanup because it affects every agent's next
skill refresh.

## 13 · Hole K — `signal-sema`'s scope is underspecified

`signal-sema/ARCHITECTURE.md` says it owns the Sema execution
vocabulary: operations, pattern primitives, and identity values. The
current crate owns operation class tags plus a few primitives. It does
not own executable operation payloads.

That may be exactly right, but then the wording needs to be precise:
`signal-sema` is the vocabulary of Sema operation classes and shared
Sema wire primitives. It is not the universal typed command language
for every Sema engine operation.

If the intended direction is stronger — if `signal-sema` should become
the typed command/plan contract used by `signal-executor` and
`sema-engine` — then it needs a larger design:

- table or record-family identity;
- typed command records for assert/mutate/retract;
- read plan records for match/subscribe;
- validation plan records;
- effect records that can cite record identities and spans;
- a compatibility story with per-component typed payloads.

My recommendation is conservative: keep `signal-sema` small for now
and make `signal-executor` generic over a daemon-specific `Command`.
Let the command project to a `SemaOperation` class for shared
observation.

## 14 · Read of /245 alternatives

I agree with /245's broad direction, with one structural correction:

- /245 Hole 1 is right that rejection should be a contract reply, but
  the success path must return typed executable commands, not bare
  `SemaOperation` tags.
- /245 Hole 2 is right that observable open/close verbs should be
  contract-author named.
- /245 Hole 3 is right that `ObserverChannel` belongs closer to
  `signal-frame` and the macro should emit the integration surface.
  It must include open/close lifecycle, not only publish.
- /245 Hole 4 is right that filters should default to macro-generated
  closed enums when possible.
- /245 Hole 5 is right that the pilot should be the worked example.
  A toy daemon would be less useful than making `signal-repository-ledger`
  prove the full contract -> daemon -> executor -> observer path.

The bigger rethink I would add: define the execution plan shape before
any more contract migrations. Otherwise each first daemon will invent a
different command side channel around the executor.

## 15 · Implementation order I recommend

1. Update permanent guidance first:
   `skills/component-triad.md`, `skills/skills.nota`,
   `skills/contract-repo.md`, and `skills/subscription-lifecycle.md`
   should stop teaching the old signal-core / universal-verb model and
   stop citing reports.
2. Redesign `signal-executor`:
   `Lowering::lower -> Result<Vec<Self::Command>, Self::Reply>`,
   typed command projection to `SemaOperation`, operation/effect span
   correlation, and terminal observer events.
3. Redesign observable macro integration:
   contract-named open/close operations, macro-emitted observer
   lifecycle trait/impl, production bridge with snapshot-then-deliver.
4. Clean permanent docs:
   remove report references from architecture and skills, replacing
   them with self-contained current-shape prose.
5. Use `signal-repository-ledger` as the pilot:
   make it the first real daemon that proves public contract
   operation -> typed command lowering -> Sema execution -> typed
   reply -> observer stream.

## 16 · Questions that need psyche/design attention

### Q1 — Is `signal-sema` a small vocabulary crate or the full typed command language?

The current code makes it a small vocabulary crate: operation class
tags plus shared pattern/identity primitives. /244 and /245 talk as if
the executor can execute `SemaOperation`, but that is not enough for a
real engine.

My recommendation: keep `signal-sema` small and make each daemon's
lowering produce a typed `Command` understood by its Sema engine
adapter. The command projects to `SemaOperation` for observation.

### Q2 — Should frame-level multi-payload replies own abort semantics?

`signal-frame` says it is only frame mechanics, but its `Reply` type
still has `AcceptedOutcome::Aborted`, `SubReply::Invalidated`,
`SubReply::Failed`, and `OperationFailureReason`.

My recommendation: either move abort/partial-failure semantics into
`signal-executor`, or state clearly that `signal-frame` owns a generic
ordered-batch reply algebra even though database atomicity lives below
it. The current wording splits the difference.

### Q3 — How broad is observer visibility allowed to be?

If observer events carry full operations and full Sema command/effect
records, the public socket can reveal sensitive state. If observation
is dev-mode transparency only, say so. If it is a permanent system
surface, event classes need authority/redaction policy.

My recommendation: keep dev-mode observation broad, but design the
macro/contract shape so each event class can be public, owner-only,
redacted, or forbidden.

## 17 · Destination of this report's substance

The substance should migrate into:

- `skills/component-triad.md` and `skills/contract-repo.md` for the
  current contract-local verb / triad guidance;
- `signal-executor/ARCHITECTURE.md` for typed commands, rejection
  replies, correlation, and terminal outcome events;
- `signal-frame/ARCHITECTURE.md` and macro README for observable
  open/close naming and production observer bridge shape;
- `signal-sema/ARCHITECTURE.md` for the clarified scope of
  operation-class vocabulary versus executable command records.
