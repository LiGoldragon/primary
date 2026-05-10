# 2 - data-bearing actors and the persona-actor cleanup

*Designer-assistant report. Triggered by Li's objection to
zero-sized actor marker types and by the ambiguity around
`persona-actor` in `reports/operator/102-actor-heavy-persona-mind-research.md`.*

---

## 0. Conclusion

Li's instinct is right: in this workspace, an actor noun should carry
data. A public `ClaimNormalize;` whose real life is hidden in a
separate `ClaimNormalizeState` is the wrong noun. It violates the
methods-on-types rule, weakens the actor as a thinking device, and
creates extra names to compensate for the hollow actor type.

`ractor` does not literally require its actor implementation type to be
zero-sized. Its current trait accepts a concrete `Self` value at spawn.
But its API shape splits behavior from mutable actor state:

- `Self` implements `ractor::Actor`.
- `Self::State` is the mutable state.
- lifecycle and handler hooks receive `&self` plus `&mut State`.

That shape strongly encourages the ZST behavior-marker pattern used in
`repos/lore/rust/ractor.md`. It is a poor raw modeling surface for this
workspace's philosophy.

`persona-actor` is not a real crate in the workspace. It is a proposed
name in `reports/operator/102-actor-heavy-persona-mind-research.md`.
The live direction in `reports/designer/101-extreme-actor-system-and-no-zst-actors.md`
renames the idea to workspace scope: `workspace-actor`. That rename is
correct. The stricter correction in this report is: even the private
ractor adapter does not need to be a ZST. Make the adapter host carry
runtime data too.

Recommendation:

1. Forbid public ZST actor nouns.
2. Forbid direct `impl ractor::Actor for DomainActor` in Persona-facing
   code.
3. Build `workspace-actor` as the public actor surface.
4. Put ractor behind a non-ZST private host:
   `RactorHost<A> { runtime, kind, path, trace, ... }`.
5. Treat `persona-actor` as retired vocabulary, not an implementation
   target.

---

## 1. What ractor actually forces

Current primary source: `ractor` 0.15.12 docs, fetched 2026-05-10:
<https://docs.rs/ractor/latest/ractor/actor/trait.Actor.html>.

The trait shape is:

```rust
pub trait Actor: Sized + Sync + Send + 'static {
    type Msg: Message;
    type State: State;
    type Arguments: State;

    fn pre_start(
        &self,
        myself: ActorRef<Self::Msg>,
        args: Self::Arguments,
    ) -> impl Future<Output = Result<Self::State, ActorProcessingErr>> + Send;

    fn handle(
        &self,
        myself: ActorRef<Self::Msg>,
        message: Self::Msg,
        state: &mut Self::State,
    ) -> impl Future<Output = Result<(), ActorProcessingErr>> + Send;
}
```

`ractor::Actor::spawn` takes `handler: Self`; therefore the handler can
have fields. So the narrow claim "ractor requires ZST actors" is false.

The stronger claim is true: ractor makes `Self` the behavior object and
`State` the mutable actor data. Because the hooks take `&self`, not
`&mut self`, putting ordinary mutable actor state in `Self` fights the
API. You can put immutable config or runtime handles in `Self`, but
the actor's changing state naturally lives in `State`.

That is why the older workspace lore says:

```rust
pub struct Engine;            // ZST behaviour marker
pub struct State { ... }      // owned state, private fields
pub struct Arguments { ... }
pub enum Message { ... }
```

That pattern is faithful to raw ractor, but it is no longer faithful to
the workspace's actor philosophy. The lore page should become a
framework-reference page, not the domain-facing actor pattern.

---

## 2. Why the ZST actor noun is wrong here

The actor is supposed to be the noun that owns a coherent plane:
configuration, in-flight work, child handles, resource handles,
metrics, trace identity, failure policy, and private state.

With the ZST marker pattern, the name that looks like the actor does
not own those qualities:

```rust
pub struct ClaimNormalize;       // the name, but hollow
struct ClaimNormalizeState {     // the real actor body
    policy: ClaimPolicy,
    metrics: ClaimMetrics,
    trace: TraceSink,
}
```

That creates exactly the problem Li named: the water bearer has no
buckets. The public noun is a label. The real object is elsewhere.

The data-bearing actor shape keeps the noun whole:

```rust
pub struct ClaimNormalize {
    policy: ClaimPolicy,
    in_flight: BTreeMap<RequestId, ClaimWork>,
    metrics: ClaimMetrics,
    trace: TraceSink,
}

impl workspace_actor::Actor for ClaimNormalize {
    type Argument = ClaimNormalizeArgument;
    type Message = ClaimNormalizeMessage;
    type Reply = ClaimNormalizeReply;
    type Failure = ClaimNormalizeFailure;

    async fn open(arguments: Self::Argument) -> Result<Self, Self::Failure> {
        Ok(Self {
            policy: arguments.policy,
            in_flight: BTreeMap::new(),
            metrics: arguments.metrics,
            trace: arguments.trace,
        })
    }

    async fn handle(&mut self, message: Self::Message)
        -> Result<Self::Reply, Self::Failure>
    {
        // verbs operate on the actor's own fields
    }
}
```

This does not mean one giant actor type with enum fields for unrelated
roles. Variation belongs in fields when the actor is the same noun with
different equipment, policy, or environment. A separate actor type is
still right when the message vocabulary, lifecycle, supervision policy,
or failure boundary changes.

Rule of thumb:

| Difference | Model it as |
|---|---|
| Same role, different policy/config/resource | fields on one actor type |
| Same role, different current condition | fields or internal enum state |
| Different mailbox vocabulary | different actor type |
| Different supervision/failure boundary | different actor type |
| Different architectural plane | different actor type |

---

## 3. Runtime survey for actor-as-Self

Sources fetched 2026-05-10:

- `ractor` 0.15.12 Actor docs:
  <https://docs.rs/ractor/latest/ractor/actor/trait.Actor.html>
- `kameo` 0.20.0 Actor docs:
  <https://docs.rs/kameo/latest/kameo/actor/trait.Actor.html>
- `kameo` Spawn docs:
  <https://docs.rs/kameo/latest/kameo/actor/trait.Spawn.html>
- `xtra` Actor docs:
  <https://docs.rs/xtra/latest/xtra/trait.Actor.html>
- `actix` Actor docs:
  <https://docs.rs/actix/latest/actix/trait.Actor.html>

| Runtime | Public actor shape | Fit for hard no-ZST actor rule |
|---|---|---|
| `ractor` | `Self` is behavior; mutable data is associated `State`; hooks receive `&self` and `&mut State`. | Poor raw fit. Good only behind a workspace adapter that makes `Self` carry data at the public layer. |
| `kameo` | `Actor::on_start(args, ActorRef<Self>) -> Self`; message path operates on `&mut self`; docs note `Args = Self` is common. | Best direct fit among checked runtimes. Actor data naturally lives on `Self`. |
| `xtra` | Actor lifecycle receives `&mut self`; handlers are implemented for the actor type. | Good philosophical fit, smaller/older ecosystem surface. |
| `actix` | Actors are objects with state and behavior; examples use `struct MyActor { val }`. | Good philosophical fit, but heavier and tied to Actix context conventions. |

Switching away from ractor is not required to enforce the hard rule.
But the survey changes the decision criteria:

- If the workspace keeps ractor, raw ractor must be hidden.
- If the adapter becomes complex or ugly, Kameo is the runtime to
  re-evaluate first because its current API already has actor-as-Self.

---

## 4. Strict workspace shape

`reports/designer/101-extreme-actor-system-and-no-zst-actors.md`
already proposes `workspace-actor`. Its main shape is right:

- public trait: `workspace_actor::Actor`
- actor data on `Self`
- public handle: `workspace_actor::Handle<A>`
- no raw `ractor::ActorRef` in consumers
- no raw ractor spawn in Persona-facing code

This report tightens one point: designer/101 permits a single internal
ZST `RactorAdapter<A>`. That is an acceptable compromise if the only
goal is "no public ZST actor nouns." It is not enough for a hard
zero-sized actor rule.

Use a non-ZST ractor host instead:

```rust
type BoxActorOpen<A> = Pin<Box<dyn Future<
    Output = Result<A, <A as workspace_actor::Actor>::Failure>,
> + Send>>;

struct RactorHost<A: workspace_actor::Actor> {
    runtime: RuntimeHandle,
    kind: ActorKind,
    path: ActorPath,
    trace: TraceSink,
    open_actor: fn(A::Argument) -> BoxActorOpen<A>,
}

impl<A: workspace_actor::Actor> ractor::Actor for RactorHost<A> {
    type Msg = HostMessage<A>;
    type State = A;
    type Arguments = A::Argument;

    async fn pre_start(
        &self,
        myself: ractor::ActorRef<Self::Msg>,
        arguments: Self::Arguments,
    ) -> Result<Self::State, ractor::ActorProcessingErr> {
        self.trace.actor_starting(&self.path, self.kind);
        (self.open_actor)(arguments).await.map_err(to_ractor_error)
    }

    async fn handle(
        &self,
        myself: ractor::ActorRef<Self::Msg>,
        message: Self::Msg,
        actor: &mut Self::State,
    ) -> Result<(), ractor::ActorProcessingErr> {
        self.trace.message_received(&self.path, message.kind());
        dispatch_to_workspace_actor(actor, message).await
    }
}
```

`RactorHost<A>` is not the actor noun. It is private framework hosting
machinery. It carries real runtime data: registry handle, trace sink,
actor kind, actor path, constructor function, and any scheduler/test
probe handle.

The domain actor remains `A`, and `A` carries the state.

---

## 5. Enforcing the rule

The rule should be testable, not merely stylistic.

Hard rule:

> Any type that implements `workspace_actor::Actor` must have non-zero
> runtime size and must expose its behavior through `&mut self`.

Recommended enforcement:

1. `workspace-actor` exposes a test helper that spawns every actor in a
   manifest and asserts `size_of_val(&actor) > 0` after `open`.
2. A `syn`-based architecture test rejects public `struct Name;` and
   `struct Name {}` items whose name ends in an actor noun or whose impl
   block implements `workspace_actor::Actor`.
3. A dependency/import test rejects direct `impl ractor::Actor for` in
   Persona-facing crates except inside the private adapter module.
4. A spawn test rejects `ractor::Actor::spawn`, `spawn_linked`, and raw
   `ActorRef` use outside `workspace-actor`.
5. Actor manifests record `ActorKind`, `ActorPath`, message edges, and
   whether the public actor type is data-bearing.

The test should allow standard-library marker machinery only when it is
inside a non-ZST host with real fields. It should not allow a
domain-facing actor type whose only "data" is `PhantomData`.

---

## 6. What to do about persona-actor

Local search found no `persona-actor` crate, repo, or Rust module.
The term appears in reports, especially
`reports/operator/102-actor-heavy-persona-mind-research.md`.

So:

- It is not an existing implementation.
- It is not evidence that a crate already exists.
- It was a proposed name for an adapter/discipline layer.
- The name is wrong because the rule is workspace-wide, not
  Persona-specific.

The live name should be `workspace-actor` if a crate is created.
`persona-actor` should be treated as retired vocabulary. Historical
reports can remain as history, but current plans, skills, lore, and
implementation tickets should not point agents at `persona-actor`.

Cleanup targets:

| Path | Needed change |
|---|---|
| `reports/operator/102-actor-heavy-persona-mind-research.md` | Treat `persona-actor` sections as superseded by designer/101 plus this report. |
| `reports/designer/101-extreme-actor-system-and-no-zst-actors.md` | Replace the "single permitted ZST adapter" with the non-ZST `RactorHost<A>` shape. |
| `skills/actor-systems.md` | Already has the correct public rule; can add "adapter host carries data too" if the hard rule is adopted. |
| `skills/rust-discipline.md` | Already points actors toward data-bearing nouns; can tighten the ZST carve-out after `workspace-actor` is pinned. |
| `repos/lore/rust/ractor.md` | Still shows the old ZST behavior-marker template; add a top warning or rewrite it as raw-framework reference only. |
| Open task `primary-186` | Rename from "Persona daemons adopt ractor" to "Persona daemons adopt workspace-actor over ractor" when implementation starts. |

---

## 7. Recommendation

Adopt this stricter design:

1. `workspace-actor` is a real crate proposal, not an invented existing
   crate. It is the public modeling surface.
2. `ractor` remains only as the first backend runtime.
3. No Persona-facing crate implements `ractor::Actor` directly.
4. No domain actor noun is zero-sized.
5. The private ractor host is also non-ZST because it carries runtime
   data.
6. Kameo becomes the first runtime to revisit if the ractor host feels
   like the wrong abstraction after a small prototype.

Short version: keep the actor with its buckets. If ractor wants a host,
the host carries the registry, trace, path, and scheduler. Nothing
domain-facing is hollow.
