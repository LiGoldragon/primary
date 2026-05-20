# signal-frame / signal-executor migration start from operator /141

## Scope

This report starts the migration requested from:

- `reports/operator/141-signal-frame-executor-correction-examples.md`

It also absorbs the earlier context from:

- `reports/operator/140-signal-frame-executor-hole-analysis.md`
- `reports/designer/244-hole-finding-after-243-implementations.md`
- `reports/designer/245-design-alternatives-for-244-holes.md`
- `reports/system-specialist/149-lojix-signal-design-adjustments-after-244-245.md`

This is foundation work for `signal-frame`, `signal-executor`, and
downstream `signal-lojix` / `lojix` on the rewrite stack.

## Coordination state

At migration start, the code repos are already locked by peer lanes:

- `second-designer-assistant` holds `/git/github.com/LiGoldragon/signal-frame`
  and `/git/github.com/LiGoldragon/signal-executor`.
- `second-operator-assistant` is specifically working on
  `signal-executor` Package 1: rejection semantics.

I did not edit those repos under active locks. I used the unblocked
slice from `/141`: settle the observer projection boundary that the
report says needs one more design pass before code.

## Package 1 — rejection semantics

This package is ready for code and is already claimed by
`second-operator-assistant`.

Correct shape:

```rust
pub trait Lowering {
    type Operation: RequestPayload;
    type Command;
    type Reply;

    fn lower(&self, operation: &Self::Operation)
        -> Result<Vec<Self::Command>, Self::Reply>;

    fn reply_from_effects(
        &self,
        operation: &Self::Operation,
        execution: OperationExecution<'_>,
    ) -> Self::Reply;
}
```

The important correction from `/141`: when `lower()` returns
`Err(contract_reply)`, the executor returns a frame-layer
`Reply::Accepted` with `AcceptedOutcome::Aborted`, not a kernel
`Reply::Rejected`.

The failed operation carries the typed detail:

```rust
SubReply::Failed {
    reason: OperationFailureReason::DomainRejection,
    detail: Some(contract_reply),
}
```

Earlier operations are `Invalidated`; later operations are `Skipped`.
Kernel `Reply::Rejected` stays reserved for frame/version/decode or
receiver-internal infrastructure failures that cannot produce a
contract reply.

### Required tests

- `lowering_rejection_returns_typed_failed_subreply`
- `multi_operation_lowering_rejection_invalidates_skips_and_fails`
- `kernel_rejection_does_not_carry_contract_reply`

## Package 2 — observable grammar

This package is ready for code and is part of the
`second-designer-assistant` repo lock.

Current `signal-frame` macro injects hard-coded `Observe` /
`Unobserve` operations. That violates the contract-local verb rule
because a domain contract may need its own `Observe(Selection)`.

Correct grammar:

```rust
observable {
    open Watch(ObserverFilter);
    close Unwatch;
    filter ObserverFilter;
    event OperationReceived;
    event SemaEffectEmitted;
}
```

The contract author owns the verbs `Watch` and `Unwatch`. The macro
owns the close payload and emits:

```rust
operation Watch(ObserverFilter) opens ObserverStream
operation Unwatch(<Channel>ObserverSubscriptionToken)
```

The author should not spell the close token type manually. The token
is generated stream machinery, not domain vocabulary.

### Required tests

- `observable_open_and_close_verbs_are_contract_authored`
- `observable_close_payload_is_macro_owned_token`
- `observable_allows_domain_observe_operation_when_watch_is_open_verb`

## Package 3 — observer projection boundary

This package is the design slice that was still open in `/141`.

The tempting `/245` simplification was:

> move `ObserverChannel<Operation>` to `signal-frame` and let the
> macro emit the impl.

That is not mechanically correct as stated. The two surfaces are
different:

```text
signal-executor publishes execution facts:
  Operation
  SemaEffect

signal-frame macro observer sets publish channel event records:
  OperationReceived
  SemaEffectEmitted
```

`signal-frame` cannot mention `signal-executor::SemaEffect` without
reversing the dependency. The bridge must preserve a projection
boundary.

### Correct ownership split

| Crate / layer | Owns |
|---|---|
| `signal-frame` | frame replies/requests, stream token/fanout primitives, macro-generated observer set |
| `signal-executor` | execution ordering, `Lowering`, `SemaEngine`, executable command flow, `SemaEffect` facts |
| contract crate | channel event record types such as `OperationReceived` and `SemaEffectEmitted` |
| daemon or bridge | projection from executor facts into channel event records, plus delivery policy |

### Bridge shape

The bridge should be explicit and small:

```rust
pub trait ObservationProjection {
    type Operation;
    type OperationEvent;
    type EffectEvent;

    fn operation_event(&self, operation: &Self::Operation)
        -> Self::OperationEvent;

    fn effect_event(&self, effect: &SemaEffect)
        -> Self::EffectEvent;
}
```

A daemon then composes:

- the macro-generated `<Channel>ObserverSet`;
- the daemon's `ObservationProjection`;
- a delivery object that writes observer stream frames to subscribers.

The executor still calls an executor-facing observer trait. The bridge
receives those calls, projects the values, asks the macro-generated
observer set which subscribers match, snapshots recipients, releases
the observer-set lock, and then delivers frames.

The snapshot-before-deliver rule is important. A slow observer must not
hold the observer registry lock and block registration, unregistration,
or publication for every other observer.

### Where should the bridge live?

Do not add a new crate yet.

The first production bridge should live in the worked daemon pilot,
likely `repository-ledger`, because only that daemon can prove the
real delivery shape against a live contract. Extract a tiny bridge
crate only after two real daemons duplicate the pattern.

This preserves the workspace micro-component rule: extract when the
capability is real and repeated, not when the type sketch merely looks
general.

### Macro support

The macro can help by letting the observable block name event roles:

```rust
observable {
    open Watch(ObserverFilter);
    close Unwatch;
    filter ObserverFilter;
    operation_event OperationReceived;
    effect_event SemaEffectEmitted;
}
```

This is better than a generic `event` list when the executor bridge
needs to know which event records correspond to which publication
moment.

If the macro keeps `event <PayloadType>;` for arbitrary observer event
classes, add the role-specific forms alongside it rather than forcing
the bridge to infer roles from names.

### Required tests

In the first worked daemon:

- `executor_operation_fact_projects_to_observer_event`
- `executor_effect_fact_projects_to_observer_event`
- `observer_bridge_delivers_only_matching_subscriptions`
- `slow_observer_delivery_does_not_hold_subscription_registry`

## Typed commands are still required

`reports/designer/244` found a deeper blocker: current
`signal-executor` lowers to bare `SemaOperation` tags. That is still
insufficient.

The executor should lower to typed executable commands:

```rust
pub trait Lowering {
    type Command;

    fn lower(&self, operation: &Self::Operation)
        -> Result<Vec<Self::Command>, Self::Reply>;

    fn command_sema_operation(&self, command: &Self::Command)
        -> signal_sema::SemaOperation;
}

pub trait SemaEngine {
    type Command;
    type Error;

    fn execute_atomic(&mut self, commands: Vec<Self::Command>)
        -> Result<Vec<SemaEffect>, Self::Error>;
}
```

`SemaOperation` remains useful as an observation/classification tag.
It is not executable by itself.

For `lojix`, this matters directly: `Assert` does not say which
deployment row to assert, `Match` does not say which generation query
to run, and `Subscribe` does not say which stream to open.

## Downstream consequence for `lojix`

Do not migrate `signal-lojix` until the foundation has:

1. typed per-operation domain rejection detail;
2. contract-authored observable open/close verbs;
3. executable command lowering rather than bare `SemaOperation`;
4. operation-index / effect-span correlation for replies;
5. a proven observer projection bridge in the pilot daemon.

When those exist, `signal-lojix` can move off old `SignalVerb` roots
and onto deployment-domain operations such as `Submit`, `Query`, and
`Watch` / `Unwatch`.

## Current next action

The immediate unblocked action is coordination, not conflicting code:

- let `second-operator-assistant` finish Package 1 in
  `signal-executor`;
- let `second-designer-assistant` finish Package 2 in
  `signal-frame`;
- keep Package 3's projection boundary in this report so the first
  worked daemon does not flatten executor facts and contract event
  records into the wrong crate.

