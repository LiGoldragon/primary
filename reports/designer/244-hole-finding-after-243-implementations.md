# 244 — Hole-finding after /243 implementations

*Both /243 implementations landed: `signal-frame` `observable`
block (commits `1610be7c` + `b86442ac` on `main`); `signal-executor`
crate created at `https://github.com/LiGoldragon/signal-executor`
(`57040d59`); skill edit to `skills/contract-repo.md` for the
reply-naming convention (`a7f3a0ee`). All tests pass; nix flake
check green via remote builder on all three. Now: holes found in
the implemented designs, by severity.*

## 0 · TL;DR

Five real holes ranked by severity:

| # | Hole | Severity |
|---|---|---|
| 1 | **Typed rejection reasons can't cross the wire.** Executor's typed `L::RejectionReason` lives in `ExecutorOutcome` daemon-side; the wire `Reply::Rejected` only carries the kernel-level `RequestRejectionReason::Internal`. Callers lose the typed cause. | High |
| 2 | **`Observe` verb collision** between the observable-block-injected `Observe(ObserverFilter)` and any contract author wanting `Observe` as their own one-shot-read verb (e.g., signal-persona-spirit). Macro rejects with compile-fail, forcing the contract author to rename their own verb. | High |
| 3 | **`publish_*` bridge between macro and executor isn't built.** The macro emits per-channel publish closures (`publish_<event_snake>(event, deliver)`); the executor exposes `ObserverChannel<Operation>` trait. Daemons need a hand-written adapter to wire them. No shared adapter crate. | High |
| 4 | **Filter-match trait impl is contract-author-trusted.** The macro generates the trait skeleton; the contract author writes the impl. A buggy impl can leak events to the wrong observers. No safety guarantee. | Medium |
| 5 | **No end-to-end worked example.** Macro generates observability; executor consumes it; nothing demonstrates the full path (contract crate → daemon with `Lowering` impl → executor → observer subscriber → wire frame). Phase-3 component refactors will guess. | Medium |

Plus six convention/edge-case items (§3).

**2026-05-20 operator-assistant addendum, after considering /245:**
after reading the landed `signal-frame`, `signal-executor`, and
`signal-sema` code and running targeted executor tests, four more
holes matter. `/245` improves the fix shape for holes 1, 2, 3, and 5;
the clean path is to combine those alternatives with the bigger
executor hole here: lowering must produce typed executable commands,
not bare `SemaOperation` tags (§4.1).

## 1 · The big three

### Hole 1 — Typed rejection reasons don't cross the wire

**What I see.** signal-executor's `ExecutorOutcome<L, S>` is a
three-variant sum:

```rust
pub enum ExecutorOutcome<L, S>
where L: Lowering, S: SemaEngine
{
    Accepted { reply: Reply<L::Reply>, … },
    LoweringRejected { reply: Reply<L::Reply>, reason: L::RejectionReason },
    EngineRejected { reply: Reply<L::Reply>, error: S::Error },
}
```

The daemon-side `outcome.reply()` is what goes on the wire. On
the rejection paths, that wire `Reply` has
`Reply::Rejected { reason: RequestRejectionReason::Internal }`.
The typed `L::RejectionReason` lives only in the executor's
return value — observers and the caller never see it.

**Why it's a hole.** A peer asking spirit `State(badStatement)`
gets back "Internal — daemon rejected this." It doesn't know
whether the rejection was "psyche identity not registered,"
"statement classification failed," or "policy denied." Three
different domain-level rejections that share one wire response.

The /243 reply-naming convention already says **Reply rejection
variants are verb-past-tense + `Rejected`** (`SubmitRejected`,
`StateRejected`). So contract-level rejections should be
**variants on the contract's `Reply` enum, not on
`RequestRejectionReason`.** The hole is in how the executor
maps `L::RejectionReason` → contract-reply-Rejected variant.

**What's missing.** The `Lowering` trait needs a third method:

```rust
fn reply_from_lowering_rejection(
    &self,
    operation: &Self::Operation,
    reason: &Self::RejectionReason,
) -> Self::Reply;
```

The executor calls it instead of returning `Reply::Rejected
{ Internal }` when `lower()` errors. Same for the engine
rejection path.

**2026-05-20 update after /245.** This is the incremental fix. The
cleaner fix is now §5 recommendation 1: make `lower()` return
`Result<Vec<Self::Command>, Self::Reply>`, so the contract-domain
rejection reply is produced directly.

**Severity**: High. Without this fix, every contract refactor
loses domain-level error information at the wire. The
reply-naming convention I just landed in `skills/contract-repo.md`
isn't operative.

### Hole 2 — `Observe` verb collision

**What I see.** `signal-frame`'s observable block injects
`operation Observe(ObserverFilter)` and `operation Unobserve(...)`.
A contract author who wants `Observe` as their own one-shot-read
verb (signal-persona-spirit currently has `operation
RecordObservation(...)` which under verb-form would become
`Observe(Selection)`) collides.

The macro catches this with the compile-fail fixture
`observable_operation_name_collision.rs` — but the resolution
forces the contract author to rename their own verb.

**Why it's a hole.** `Observe` is one of the most common
verb-form names for one-shot reads. Forcing every observable
contract to pick a different name for its read operations
defeats the contract-local-verb discipline.

**Resolution options**:
- **Rename the macro-injected verb**: `Watch` / `Unwatch` —
  but Watch is also already used (subscription opener for
  streaming reads). 
- **Use a less-natural name**: `Surveil` / `Tap` / `Snoop` —
  fewer collisions but reads worse.
- **Namespace the injected verb**: `MetaObserve` / `Probe` —
  least likely to collide.
- **Make the contract author opt the verb name**: `observable
  { operation_name MyObserveName; ... }` — flexible but
  ugly grammar.

My lean: rename to **`Probe`** (probe-the-channel-for-events)
or **`Tap`** (tap-the-channel-stream). Both read as
domain-appropriate for "subscribe to a debug stream of what's
happening" and neither collides with common one-shot-read or
streaming-read verbs.

**2026-05-20 update after /245.** Fixed `Probe` / `Tap` is still a
fallback, but the cleaner shape is §5 recommendation 2: let the
contract author name the observable open/close verbs.

**Severity**: High. Every observable contract will hit this.

### Hole 3 — Macro → executor publish-bridge

**What I see.** signal-frame's macro emits per-channel publish
closures with the shape:

```rust
impl LedgerObserverSet {
    fn publish_operation_received<F: FnMut(LedgerObserverSubscriptionToken, &OperationReceived)>(
        &self,
        event: &OperationReceived,
        deliver: F,
    ) { … }
}
```

signal-executor's `Executor::execute` calls
`self.observers.publish_operation_received(op)` and
`self.observers.publish_sema_effect_emitted(effect)` —
no closure, no token, no per-event method differentiation.
Different shapes.

**Why it's a hole.** The macro-emitted publish closure pattern
puts the *delivery side* (how an event reaches a subscriber's
socket) in the daemon's hands via the closure. The executor's
`ObserverChannel` trait abstracts away delivery — but it
doesn't have a slot for the closure.

**What's missing.** A bridge — likely a daemon-side adapter
that implements `ObserverChannel<Operation>` and wires through
the macro's publish closures. The adapter knows the channel's
wire layer; the executor doesn't.

Both agents flagged this as a reconciliation point. Neither
built the bridge. The first real daemon (signal-repository-ledger
pilot? signal-persona-spirit?) will have to invent it.

**2026-05-20 update after /245.** The better shape is to move the
observer-channel surface to `signal-frame` and have the macro emit the
impl. §4.2 adds that this must cover subscription lifecycle, not just
publish delivery.

**Severity**: High. Blocks every daemon that wants
observability.

## 2 · The two medium holes

### Hole 4 — Filter-match trait impl is contract-author-trusted

**What I see.** The macro emits:

```rust
pub trait LedgerObserverFilterMatch {
    fn matches_operation_received(&self, event: &OperationReceived) -> bool;
    fn matches_sema_effect_emitted(&self, event: &SemaEffectEmitted) -> bool;
}
```

The contract author writes `impl LedgerObserverFilterMatch for
LedgerObserverFilter { … }`. A buggy or malicious impl can:
- Always return `true` (every observer sees everything).
- Never return `false` for sensitive events (data leak).
- Panic (DoS the publishing daemon).

**Why it's a hole.** Observability is "not security-sensitive"
per psyche intent on 2026-05-19T20:00Z ("seeing things is not
really a security concern"). So the safety bar is lower than
auth. But: a poorly-implemented filter still leaks all events
to all subscribers — defeating the *filter* mechanism even
without security implications.

**Mitigation options**:
- Macro-generate **default filter impls** for common shapes
  (`All`, `OnlyOperations { kinds: Vec<Kind> }`, etc.) so
  contract authors opt in via a closed enum rather than
  implementing a trait.
- Property test the trait — contract authors must provide a
  test that exercises the filter against a known event set.
- Leave as-is; document the trusted-impl pattern in the
  macro README.

My lean: macro-generates closed-enum defaults; contract
authors opt out only when they need custom predicates.

**Severity**: Medium. Real concern but not blocking.

### Hole 5 — No end-to-end worked example

**What I see.** signal-frame's observable block tests exist;
signal-executor's mock-Counter daemon test exists. Both verify
their own slice. Neither shows: a real contract using
`observable {…}`, with a real `Lowering` impl, an `ObserverChannel`
adapter bridging the macro's publish closures, a subscriber
attaching via `Observe`, and an event reaching the subscriber's
side via a wire frame.

**Why it's a hole.** Phase-3 component refactors will read the
two crates separately and guess how they fit. The guess will
vary across daemons.

**Resolution**: create a `signal-executor-examples/` directory
(or a separate `signal-counter-daemon` repo) with one
worked-end-to-end example. The pilot
(`signal-repository-ledger`) could itself become this example
once it adopts the observable block.

**2026-05-20 update after /245.** Prefer the pilot: make
`signal-repository-ledger` the canonical worked example instead of
creating a separate toy daemon.

**Severity**: Medium. Not blocking; future agents can figure
it out. But it'll waste time.

## 3 · Six smaller items

### A — Rust/NOTA naming divergence (signal-frame observable)

Rust types are channel-prefixed (`LedgerObserverSubscriptionToken`);
NOTA wire heads are uniform (`ObserverSubscriptionToken`). The
agent's reasoning is principled: Rust needs scoping when a
daemon has multiple observable channels; NOTA wants
workspace-uniform vocabulary for `persona-introspect` to
filter across. But a reader switching between Rust source and
NOTA logs sees different names for the same value. Worth
documenting in `skills/contract-repo.md` explicitly so future
agents don't "fix" the divergence by accident.

### B — `SemaEffectOutcome` closed enum may miss cases

signal-executor defines:

```rust
pub enum SemaEffectOutcome {
    Wrote { rows_written: u64, rows_matched: u64 },
    Read { rows_read: u64 },
    Stream { subscription_token: u64 },
    Validated { predicate_held: bool },
}
```

Mutate (write at stable identity) → `Wrote`; that's fine. But
Mutate might want to expose the **previous value** for
auditability (e.g., for the Mutate-Sema-Effect-Emitted observer
to log "X was at v3, now at v4"). The current closed enum
doesn't carry it. Either: extend `Wrote` with optional fields,
or accept that observers query separately for diffs.

### C — Atomicity is trait-contract, not compile-time

signal-executor's `SemaEngine::execute_atomic` documents
"all-or-none." Compile-time enforcement is impossible — the
trait says "must be atomic" and trusts the impl. A misbehaving
engine breaks the contract silently. Property tests in the
signal-executor crate help; the actual sema-engine crate would
need its own atomicity witnesses.

### D — `Lowering::reply_from_effects` correlation is implicit

The trait receives the full `&[SemaEffect]` for every op. The
contract author has to filter by index/position. Multi-op
requests where each op produces a known number of effects need
the author to compute offsets. Documented in /243; not enforced.
A typed correlation primitive (each effect tagged with its
source-op index) would make this safer.

### E — Stream block grammar change (multi-event)

Agent A relaxed `StreamBlockSpec` from one `event_variant: Ident`
to `events: Vec<Ident>` to support the observable block's
multi-event stream. Documented as backward-compatible. Existing
single-event stream blocks still work. But: every contract
currently using a stream block now sees a slightly more
permissive grammar. Worth a heads-up to component maintainers.

### F — `Observe` block opt-in has no enforcement

A daemon that should be observable (every Persona component,
per /243's intent) might forget the `observable` block. The
macro doesn't enforce anything; persona-introspect would just
fail to subscribe (cleanly). Convention enforcement, not
type enforcement. Maybe a lint or a workspace-level audit could
catch missing observability where it's expected.

## 4 · Operator-assistant addendum (2026-05-20)

I read:

- `signal-frame` `main` at `b86442ac`
- `signal-executor` `main` at `57040d59`
- `signal-sema` `main` at `d056fc5a`

I also ran these executor probes:

- `cargo test lowering_rejection_does_not_call_engine -- --exact`
- `cargo test empty_lowering_is_legal -- --exact`
- `cargo test observer_receives_operations_even_on_lowering_rejection -- --exact`

All passed. The tests support the holes below rather than refuting
them.

I then considered
`reports/designer/245-design-alternatives-for-244-holes.md`. Its
alternatives are better than the incremental fixes for the original
holes, but they do not remove the additional executor-command,
terminal-observation, effect-correlation, or daemon-concurrency holes
below.

### Hole 6 — Executor lowers to verb tags, not executable Sema commands

**What I see.** `Lowering::lower` returns
`Vec<signal_sema::SemaOperation>`, and `SemaEngine::execute_atomic`
accepts `Vec<SemaOperation>`. But `SemaOperation` is only:

```rust
Assert | Mutate | Retract | Match | Subscribe | Validate
```

It carries no table, record family, payload, slot, revision, pattern,
read plan, or subscription target. `signal-sema` owns useful
`PatternField`, `Slot`, and `Revision` primitives, but the executor
path does not carry them.

**Why it's a hole.** A real daemon cannot commit durable state from
`Vec<SemaOperation>` alone. `Assert` does not say what to assert.
`Match` does not say what to match. `Mutate` does not say which slot
or revision to mutate. The current executor can classify work and
test atomic ordering, but not execute real typed-record work without
a side channel outside the trait.

**Likely fix, updated after /245.** Combine `/245`'s "rejection is a
reply variant" move with typed executable commands. Make the executor
generic over a daemon/engine command type, while separately exposing
the lower Sema operation class for observation:

```rust
trait Lowering {
    type Command;
    fn lower(&self, operation: &Self::Operation)
        -> Result<Vec<Self::Command>, Self::Reply>;
    fn command_operation(&self, command: &Self::Command) -> SemaOperation;
}

trait SemaEngine {
    type Command;
    fn execute_atomic(&mut self, commands: Vec<Self::Command>)
        -> Result<Vec<SemaEffect>, Self::Error>;
}
```

The exact names can change, but the missing shape is a typed command
or plan that survives lowering all the way into the engine. Observers
can still receive the `SemaOperation` class derived from each command.
This also makes `/245`'s rejection design stronger: contract-domain
rejections cross the wire as ordinary contract reply variants, while
engine failures remain kernel/internal unless the daemon can safely
map them into a domain reply.

**Severity**: High. This blocks `signal-executor` from being the real
shared daemon executor rather than a class-tag coordinator.

### Hole 7 — Observer subscription lifecycle is not in the executor bridge

Hole 3 names the publish bridge gap: macro-generated
`publish_<event>(event, deliver)` does not match
`ObserverChannel<Operation>`.

There is a second lifecycle gap in the same boundary. The observable
block injects `Observe(Filter)` and `Unobserve(Token)` into the
contract operation enum. When the daemon feeds that request to
`Executor::execute`, those variants are just ordinary operations:
`Lowering::lower` must handle them. But the macro-generated
`<Channel>ObserverSet::register` / `unregister` is not owned by
`signal-executor::ObserverSet`, and `reply_from_effects` has no clean
access to register a filter and return `ObserverSubscriptionOpened`.

So the missing bridge is not only publish-side. It must handle all
three observer surfaces:

- `Observe(Filter)` registers a subscriber and returns the opened
  token.
- `Unobserve(Token)` unregisters it.
- `publish_*` delivers events to matching live subscriptions.

**Severity**: High. Without this, every daemon either hand-rolls
observable subscription handling or keeps two observer registries that
can drift.

`/245`'s proposal to move `ObserverChannel` to `signal-frame` and have
the macro emit the impl is the right direction, but it must include
this lifecycle path. Emitting only a publish trait impl would still
leave `Observe(Filter)` / `Unobserve(Token)` as ad hoc daemon work.

### Hole 8 — Observers do not see terminal outcomes

The executor publishes:

- `OperationReceived` before lowering.
- `SemaEffectEmitted` after a successful atomic commit.

It publishes no event for `LoweringRejected`, `EngineRejected`, or
accepted zero-effect operations.

The targeted tests confirm the edge:

- `observer_receives_operations_even_on_lowering_rejection` passes:
  observers see operation events and no Sema effects on lowering
  rejection.
- `empty_lowering_is_legal` passes: an accepted operation may also
  produce zero Sema effects.

From an observer stream, "operation received, then no effect" can mean
"accepted no-op," "lowering rejected," "engine rejected," or "daemon
died before publishing more." This is too weak for
`persona-introspect`.

**Likely fix.** Add terminal observation events, probably:

- `OperationLoweringRejected`
- `RequestEngineRejected`
- `RequestExecutionCompleted`

Names can be tuned, but the event stream needs an explicit terminal
outcome for each request/exchange.

**Severity**: Medium-high. It does not block state execution, but it
does block trustworthy introspection.

### Hole 9 — Reply/effect correlation is worse than §3D states

§3D says correlation is implicit. The code makes the problem sharper:
`reply_from_effects(&self, operation, effects)` receives neither the
operation index nor the effect span produced by that operation.

For duplicate or same-class operations, a pure implementation cannot
distinguish the first operation's effects from the second's. If the
request is:

```text
[Increment(1), Increment(1)]
```

then the two `reply_from_effects` calls receive equal `operation`
values and the same full `effects` slice. Without interior mutable
cursor state or re-lowering, they must return the same reply even if
the engine produced distinct effects.

**Likely fix.** The executor should compute an execution plan that
remembers, for each source operation, the effect index range it
produced:

```rust
reply_from_effects(operation, OperationExecution {
    operation_index,
    effects: &effects[start..end],
})
```

This also makes zero-effect operations explicit: their span is empty,
but known.

**Severity**: High if multi-operation requests are meant to be a real
atomic surface. Medium if the workspace decides to keep daemon
requests mostly single-operation.

### Hole 10 — Macro observer set is not daemon-concurrency shaped

The macro-generated observer runtime is a plain `Vec` with:

- `register(&mut self, filter)`
- `unregister(&mut self, token)`
- `publish_*(&self, event, deliver)`

That is fine as a compile-time and single-thread witness, but real
daemons have concurrent socket tasks. A daemon will wrap the set in a
`Mutex` or actor. If it holds that lock while the `deliver` closure
writes frames, one slow subscriber can block registration,
unregistration, and publication for every observer.

**Likely fix.** The bridge from hole 7 should own the concurrency
policy: snapshot matching recipients under lock, release the lock,
then deliver. The macro's raw set can remain a low-level primitive,
but the production bridge must be the documented path.

**Severity**: Medium. It will not show up in macro unit tests, but it
will show up immediately in a long-lived daemon.

### Smaller addendum items

- `LedgerObserverSet::register` increments tokens with
  `wrapping_add`. Wraparound is unlikely but produces duplicate tokens
  eventually. Prefer checked increment plus a rejected subscription
  reply, or skip occupied token values.
- The macro-injected reply variant
  `ObserverSubscriptionOpened(<Channel>ObserverSubscriptionOpened)`
  produces doubled NOTA heads:
  `(ObserverSubscriptionOpened (ObserverSubscriptionOpened ...))`.
  It is not wrong, but it is visually noisy and sits awkwardly beside
  the reply-naming convention.

### Operator/140 design check

`reports/operator/140-signal-frame-executor-hole-analysis.md` offers
better designs in three places:

1. **Typed rejection replies.** Operator/140 corrects `/245`'s
   "just pass the reply through" wording. A lowering rejection should
   not become top-level `Reply::Rejected`, because that variant has no
   contract payload and should remain kernel/pre-flight shaped. The
   better mechanical shape is `Reply::Accepted { outcome:
   AcceptedOutcome::Aborted { failed_at, reason:
   OperationFailureReason::DomainRejection }, per_operation: ... }`
   with the typed contract rejection reply in
   `SubReply::Failed { detail: Some(reply), ... }`.
2. **Observable grammar.** Operator/140's `observable { open
   Watch(Filter); close Unwatch; ... }` is cleaner than `/245`'s
   `operation_open` / `operation_close` form. The macro should own the
   observer token payload type; the contract author only names the
   open/close verbs.
3. **Publish bridge.** Operator/140 is right that moving
   `ObserverChannel` to `signal-frame` is not enough by itself.
   Something must project executor facts (`Operation`, `SemaEffect`)
   into channel event records (`OperationReceived`,
   `SemaEffectEmitted`) without making `signal-frame` depend on
   `signal-executor`. The bridge needs an explicit projection
   boundary.

Operator/140 does **not** supersede this addendum's hole 6. It does
not address the fact that `signal-executor` currently lowers to bare
`SemaOperation` tags instead of typed executable commands/plans.

## 5 · Recommendations

After `/245`, the best fix is one bundled shape change rather than a
sequence of incremental patches:

1. **Fix holes 1 and 6 together**: change `Lowering::lower` to return
   `Result<Vec<Self::Command>, Self::Reply>`. Drop
   `RejectionReason`; contract-domain rejection is a contract reply.
   `Self::Command` is the typed executable Sema command/plan. It can
   expose a `SemaOperation` class for observation, but it is not just
   the class tag. Encode lowering rejections as per-operation aborted
   replies with `SubReply::Failed.detail = Some(contract_reply)`, not
   as top-level kernel `Reply::Rejected`.
2. **Fix holes 2, 3, 7, and 10 together**: move the observer-channel
   surface toward `signal-frame`, but only with an explicit projection
   boundary from executor facts to channel event records; extend the
   `observable` block to `open <Verb>(Filter); close <Verb>;` so the
   contract author names the verbs while the macro owns token payloads;
   and make the production bridge own register/unregister, recipient
   snapshotting, and delivery outside locks.
3. **Fix hole 9 inside the executor plan**: carry source operation
   index and effect-span correlation through execution, so
   `reply_from_effects` receives only the relevant effects for that
   operation plus its index.
4. **Fix hole 8 before relying on `persona-introspect`**: publish
   terminal outcome events for accepted, lowering-rejected,
   engine-rejected, and zero-effect accepted requests.
5. **Adopt `/245`'s pilot recommendation**: make
   `signal-repository-ledger` the end-to-end example instead of
   creating a separate toy daemon.
6. **Adopt `/245`'s filter recommendation**: macro-generate
   closed-enum filter defaults, with custom filter impls as the escape
   hatch.
7. **Document the remaining convention items**: Rust/NOTA observer
   naming divergence, stream grammar broadening, opt-in observability
   audit expectations, token wrap behavior, and the doubled
   `ObserverSubscriptionOpened` NOTA head.

## 6 · References

- `reports/designer/243-reply-naming-observer-hook-executor-trait.md`
  — the designs that were implemented.
- `reports/designer/245-design-alternatives-for-244-holes.md`
  — cleaner alternatives for the original five holes; this addendum
  folds them into the forward recommendation.
- `reports/designer/242-hole-finding-spirit-migration.md`
  — the original hole inventory.
- `https://github.com/LiGoldragon/signal-frame` `1610be7c` +
  `b86442ac` — the macro `observable` block landing.
- `https://github.com/LiGoldragon/signal-executor` `57040d59`
  — the new executor crate.
- `skills/contract-repo.md` §"Reply discipline" `a7f3a0ee`
  — the reply-naming convention edit.
- `intent/component-shape.nota` 2026-05-19T20:00Z — observer
  hook is not security-sensitive (informs hole 4).
- `intent/naming.nota` — verb-form rule (informs hole 2).
