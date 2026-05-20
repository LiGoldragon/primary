# lojix signal design adjustments after /244 and /245

## Scope

This note reconciles the system-specialist `lojix` / `signal-lojix`
design thread with:

- `reports/designer/244-hole-finding-after-243-implementations.md`
- `reports/designer/245-design-alternatives-for-244-holes.md`
- `reports/operator/140-signal-frame-executor-hole-analysis.md`

It concerns the `horizon-leaner-shape` rewrite stack, not production
CriomOS deployment on `main`.

## Short conclusion

The Horizon projection boundary remains right:

```text
lojix CLI -> lojix-daemon -> Horizon projection -> Nix/build/activation effects
```

The Signal execution boundary needs adjustment before `lojix` should
depend on the new shared executor path. The current `signal-executor`
shape is not yet strong enough for real `lojix` work because it lowers
contract operations into bare `SemaOperation` tags. `Assert`, `Match`,
or `Mutate` alone cannot say which deployment record, table, slot,
revision, query, or subscription is involved.

Therefore, the next `lojix` migration should wait for or include the
executor redesign from `/245` plus the additional typed-command fix
from `/244` hole 6.

## What changes in my design

### 1. `signal-lojix` remains contract-local, but not Sema-shaped

`signal-lojix` should not expose `Assert`, `Mutate`, `Match`,
`Subscribe`, or `Retract` on its public request surface.

The likely public operation roots are:

- `Submit` for a deployment request;
- `Query` for generation, deployment, or cache state reads;
- `Watch` / `Unwatch` for long-running deployment observation streams;
- later owner-plane roots such as `Configure`, if an owner contract is
  added.

The exact nouns can be tuned during implementation, but the important
boundary is fixed: the caller speaks deployment-domain verbs, and
`lojix-daemon` lowers those into internal state and effect work.

### 2. Domain rejection is a contract reply, not kernel rejection

`lojix` must preserve typed rejection information on the wire.

Examples:

- invalid deployment request;
- unsupported local build;
- activation action not implemented;
- authorization denied by `criome-daemon`;
- builder unavailable;
- cache source unavailable.

Those are not frame-kernel failures. They should become
`signal-lojix` reply variants such as `SubmitRejected(...)` or
`QueryRejected(...)`, not `Reply::Rejected { Internal }`.

The `/245` shape is the better executor API:

```rust
fn lower(&self, operation: &Self::Operation)
    -> Result<Vec<Self::Command>, Self::Reply>;
```

The `Err` branch carries the contract reply directly.

`reports/operator/140-signal-frame-executor-hole-analysis.md`
sharpens the wire encoding: this contract reply should not become a
top-level kernel rejection. It should travel as the failed
per-operation detail inside an aborted accepted reply. Kernel
`Reply::Rejected` remains reserved for frame/version/decode failures.

### 3. The executor must lower into typed commands, not bare Sema verbs

For `lojix`, a lowered command must carry enough information to execute
against durable state or to coordinate an effect.

The shared executor should look more like:

```rust
trait Lowering {
    type Operation;
    type Command;
    type Reply;

    fn lower(&self, operation: &Self::Operation)
        -> Result<Vec<Self::Command>, Self::Reply>;

    fn command_sema_operation(&self, command: &Self::Command)
        -> signal_sema::SemaOperation;
}

trait SemaEngine {
    type Command;
    type Error;

    fn execute_atomic(&mut self, commands: Vec<Self::Command>)
        -> Result<Vec<SemaEffect>, Self::Error>;
}
```

The `SemaOperation` tag is still useful for observation and broad
classification. It is not executable by itself.

For `lojix`, candidate command families include deployment ledger
assertions, generation queries, observation registration, cache
retention state changes, and current-generation state transitions.

### 4. Keep deployment effects outside the Sema transaction

Nix builds, Arca replication, Criome authorization, Nix config edits,
store imports, and activation are not simple Sema table operations.

The executor can own durable state transitions around them, but the
external effects still belong to actors:

- `CriomeAuthorizationActor`;
- `DeploymentArtifactActor`;
- `BuildJobActor`;
- `CacheSourceActor`;
- `TargetActivationActor`;
- `NixDaemonConfigurationActor`.

The durable ledger records should describe the effect lifecycle. The
effects themselves should remain actor-owned, timeout-bounded, and
observable.

### 5. `lojix` should avoid multi-operation public requests for now

`/244` hole 9 matters for `lojix`: reply/effect correlation is not
safe enough for real multi-operation atomic requests until the executor
tracks operation index and per-operation effect spans.

For the near term, a deployment submission should be one high-level
operation. Internally it may create many durable records and actor
effects, but the public request should not rely on a multi-operation
Signal frame to express one deployment.

### 6. Observation needs two separate surfaces

`lojix` already has domain observation: deployment streams that a user
or automation expects to consume.

The new universal observer hook is a second surface: introspection of
inbound operations, emitted Sema effects, and terminal outcomes. It
should not replace deployment-domain streams.

The `/245` alternative is correct for the macro: the observable block
should let the contract author name open/close verbs. For `lojix`,
`Watch` / `Unwatch` read naturally for both domain deployment streams
and, if needed, internal observer streams. The contract must keep the
two stream nouns distinct.

The operator report improves the concrete grammar: the close operation
should name only the verb, because the macro owns the observer token
payload. In other words, prefer `close Unwatch;` over making every
contract author spell the token type.

The operator report also corrects an over-simple reading of `/245`:
moving `ObserverChannel` to `signal-frame` is not complete by itself.
The executor publishes execution facts (`Operation`, `SemaEffect`);
the macro-generated channel publishes contract event records
(`OperationReceived`, `SemaEffectEmitted`). A projection boundary is
still needed between those two shapes.

For `lojix`, the production-safe shape is:

- `signal-frame` owns observer subscription/fanout primitives;
- `signal-executor` owns execution ordering and execution facts;
- the contract or daemon supplies projection from execution facts into
  channel event records;
- the bridge snapshots matching subscribers before delivery, so a slow
  observer cannot hold the observer registry lock.

### 7. Terminal observation events are required for deploy debugging

`persona-introspect` and future deploy monitoring need to distinguish:

- accepted no-op;
- lowering rejected;
- engine rejected;
- effect actor failed;
- request completed.

For `lojix`, this is not optional polish. A deployment can fail before
Nix starts, while building, while importing, or during activation. The
observer stream needs terminal outcome events so "operation received,
then silence" is never treated as a meaningful state.

## What does not change

- The CLI remains a text adapter with one peer: `lojix-daemon`.
- The daemon derives the `Viewpoint`; the CLI does not talk to
  Horizon.
- Criome owns authorization. `lojix-daemon` asks `criome-daemon` to
  authorize the canonical `signal-lojix` request object.
- Arca remains the right artifact plane for content-addressed inputs,
  plans, topology snapshots, authorization objects, and generated Nix
  inputs.
- Nix remains the first implementation's build/store/activation
  substrate.

## Implementation order I would use

1. Stabilize `signal-frame` and `signal-executor` around the `/245`
   alternatives plus the operator refinements:
   - `lower()` returns `Result<Vec<Command>, Reply>`;
   - lowering rejection is encoded as aborted per-operation detail, not
     kernel rejection;
   - observable open/close verbs are contract-authored;
   - close operation grammar lets the macro own the token payload;
   - the observer bridge has an explicit projection boundary between
     execution facts and channel event records;
   - filters use macro-generated closed-enum defaults where possible.
2. Add the `/244` typed-command correction:
   - executor commands carry real table/query/slot/payload data;
   - `SemaOperation` is derived from commands for observation only.
3. Add operation-index and effect-span correlation before supporting
   real multi-operation atomic public requests.
4. Use the pilot contract, likely `signal-repository-ledger`, as the
   worked example before moving `signal-lojix`.
5. Migrate `signal-lojix` from old `signal-core::SignalVerb` to
   contract-local operations.
6. Update `lojix` runtime/socket tests to assert:
   - no `SignalVerb` dependency;
   - typed rejection replies cross the wire;
   - deployment-domain watch streams still work;
   - observer streams emit terminal outcomes;
   - CLI still has exactly one runtime peer.

## Open questions

1. Should `signal-lojix` use `Submit` for all deployment submissions,
   or should it split operation roots into `Build`, `Activate`,
   `Deploy`, and `Rollback`? My current preference is `Submit` with a
   typed deployment request noun until the operation set proves too
   broad.
2. Should the universal observer hook be present in `signal-lojix`
   immediately, or should the first migration preserve only the
   existing deployment-domain observation stream and add introspection
   after the pilot proves the bridge?
3. Should `lojix` typed commands be specific to deployment ledger
   state, or should there be a shared `sema-engine` command type that
   all daemon executors use? My current preference is daemon-specific
   command types plus shared Sema classification.
