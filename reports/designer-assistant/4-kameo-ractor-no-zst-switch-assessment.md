# 4 - Kameo, ractor, and the no-ZST actor rule

*Designer-assistant report. This is a companion to
`reports/designer/102-kameo-deep-dive.md`. That report is the API
survey; this report gives the missing switch judgment for
`persona-mind`. The only runtime choices considered here are direct
`ractor` and direct Kameo. No intermediate actor layer is proposed.*

---

## 0. Bottom line

Kameo fits Li's no-zero-sized-type actor philosophy better than
`ractor`.

That does **not** mean Kameo makes ZST actors impossible. Rust still
allows:

```rust
#[derive(kameo::Actor)]
struct Ping;
```

The real difference is where the framework wants state to live.

- In `ractor`, the actor implementer and actor state are split:
  `impl Actor for StoreSupervisor { type State = State; ... }`.
  This makes a ZST behavior marker mechanically normal, even when the
  actor is conceptually data-bearing.
- In Kameo, the actor value is the state: `on_start(args) -> Self` and
  message handlers take `&mut self`. A repository rule can require
  every runtime actor type to have fields without making framework
  exceptions for the normal case.

My recommendation:

1. If "actor types carry data" is a hard invariant, switch
   `persona-mind` to Kameo before the actor tree grows much larger.
2. If the current priority is minimum churn, keep direct `ractor`, but
   accept that the no-ZST rule can only be softened to "no public hollow
   actor nouns; real state must be data-bearing."
3. Do not run both runtimes in production. The decision is direct
   `ractor` or direct Kameo.

---

## 1. Why Kameo changes the ZST question

The primary Kameo fact is its `Actor` trait shape:

```rust
pub trait Actor: Sized + Send + 'static {
    type Args: Send;
    type Error: ReplyError;

    fn on_start(
        args: Self::Args,
        actor_ref: ActorRef<Self>,
    ) -> impl Future<Output = Result<Self, Self::Error>> + Send;
}
```

Kameo's own docs say the common case is `Args = Self`, which passes
the actor state directly into spawn. Its `Message<T>` handler then gets
exclusive mutable access to that same actor value:

```rust
fn handle(
    &mut self,
    msg: T,
    ctx: &mut Context<Self, Self::Reply>,
) -> impl Future<Output = Self::Reply> + Send;
```

That is the shape Li is describing: the hunter has a bow, arrows,
camouflage, and age-of-gear fields; the water bearer has buckets.
Different actor configurations become different values of one actor
type instead of more hollow marker types.

With direct `ractor`, the current `persona-mind` shape is normal
framework usage:

```rust
pub(super) struct StoreSupervisor;

pub struct State {
    memory: MemoryState,
}

impl ractor::Actor for StoreSupervisor {
    type State = State;
    type Arguments = Arguments;
    type Msg = Message;
}
```

This can be disciplined, but it cannot satisfy a hard "no runtime actor
ZSTs" rule without fighting the library's preferred shape. The honest
`ractor` rule is weaker: marker types stay private, and the data-bearing
state gets the real behavior.

---

## 2. Runtime fit

| Concern | Direct `ractor` | Direct Kameo |
|---|---|---|
| Actor carries data | No. Actor marker and `State` are split. | Yes. `Self` is the actor state. |
| Hard no-ZST actor rule | Awkward; requires framework exceptions or bans normal examples. | Practical; test concrete actor types for fields/nonzero size. |
| Message style | One `Msg` enum per actor, reply ports for calls. | One `Message<T>` impl per message kind, per-message reply type. |
| Supervision | Links/monitors and supervisor events; policy is explicit code. | Built-in restart policies, supervision strategies, restart limits. |
| Current workspace fit | Already implemented in `persona-mind`; docs/tests say direct `ractor`. | Better semantic fit for data-bearing actor nouns; requires deliberate switch. |
| Churn | Lowest now. | Moderate mechanical rewrite while `persona-mind` is still small. |
| Risk | Current dependency, more existing local tests. | Younger dependency and Tokio-only commitment; needs a spike. |

Kameo's design is closer to the actor philosophy. `ractor` is currently
the lower-risk runtime because the workspace just corrected its docs
and tests around direct `ractor`.

---

## 3. Persona-mind migration map

Current `persona-mind` facts:

- `Cargo.toml` depends on `ractor = { version = "0.15", features =
  ["async-trait"] }`.
- `MindRootHandle` stores `ractor::ActorRef<Message>` plus a Tokio join
  handle.
- `MindRoot::pre_start` uses `Actor::spawn_linked` for children.
- `StoreSupervisor` is a ZST marker; real data lives in `State`.
- Request/reply flow uses `.call(...)` and `RpcReplyPort`.
- `tests/weird_actor_truth.rs` currently bans Kameo as a non-ractor
  actor dependency.

A direct Kameo switch would be mechanical but broad:

1. Replace the dependency with `kameo = "0.20"` and re-check the Rust
   toolchain requirement against the workspace pin.
2. Collapse each `Actor + State + Arguments` trio into a data-bearing
   actor struct where that makes semantic sense:
   `StoreSupervisor { memory: MemoryState }`,
   `MindRoot { ingress, manifest }`, etc.
3. Rewrite `pre_start(&self, ..., args) -> State` as
   `on_start(args, actor_ref) -> Self`.
4. Replace `handle(&self, ..., msg, &mut State)` with Kameo
   `Message<T> for Actor` handlers using `&mut self`.
5. Replace `RpcReplyPort` message fields with Kameo `type Reply` and
   `.ask(...)`.
6. Translate `spawn_linked` into Kameo supervision/spawn-link calls and
   declare restart policy explicitly where the actor tree needs it.
7. Keep `ActorManifest` and `ActorTrace` local to `persona-mind`; they
   are architectural witnesses, not an actor-runtime abstraction.
8. Rewrite the runtime-boundary truth test so it says "the chosen actor
   runtime is Kameo" rather than "the chosen actor runtime is ractor."
9. Add a new truth test that enumerates long-lived runtime actor types
   and fails if any are ZSTs.

Do this as a runtime replacement, not as a compatibility adapter.

---

## 4. What Kameo does not solve by itself

Kameo does not remove the need for discipline.

- ZSTs remain legal Rust. The repo still needs a hard architecture test.
- Topology witnesses remain workspace code. Kameo has actor IDs,
  links, refs, registry, and supervision, but no Persona-specific
  topology report.
- It does not provide deterministic scheduling for tests.
- It does not remove the need to keep blocking work in a named actor
  that owns that wait.
- Its per-message impl style can scatter a mailbox vocabulary unless
  file layout stays strict.

The win is narrower and important: Kameo aligns the **type** of an actor
with the **state** of that actor. That makes the no-ZST rule clean
instead of special-cased.

---

## 5. Decision criteria

Switch to Kameo if these are now workspace invariants:

- every meaningful actor noun must carry data in its own type;
- no framework-shaped ZST exception is acceptable;
- supervision policy should be declared at the runtime level, not
  mostly encoded manually around links and events;
- a moderate actor-runtime rewrite is acceptable before `persona-mind`
  grows.

Stay on direct `ractor` if these matter more:

- keep the already-implemented Phase 1 actor tree moving;
- preserve current docs/tests and dependency choice;
- avoid a younger dependency until direct `ractor` shows concrete pain;
- accept private marker structs as framework mechanics.

My lean: if Li wants the no-ZST rule to be hard, Kameo is a better fit
and the switch should happen soon. `persona-mind` is still small enough
that the migration is a contained rewrite, and postponing the decision
will make every additional `ractor` actor another small exception to
the actor-type-carries-data rule.

---

## Sources

- `reports/designer/102-kameo-deep-dive.md` — API survey of Kameo 0.20.
- `reports/operator/103-actor-abstraction-drift-correction.md` —
  correction that the current implementation is direct `ractor`, not an
  invented actor abstraction.
- `/git/github.com/LiGoldragon/persona-mind/Cargo.toml` — current
  direct `ractor` dependency and Rust pin.
- `/git/github.com/LiGoldragon/persona-mind/src/actors/store.rs` —
  current ZST marker plus `State` split.
- `/git/github.com/LiGoldragon/persona-mind/src/actors/root.rs` —
  current root spawn/call/link shape.
- `/git/github.com/LiGoldragon/persona-mind/tests/weird_actor_truth.rs`
  — current direct-`ractor` truth test.
- `https://docs.rs/kameo/latest/kameo/actor/trait.Actor.html` — Kameo
  actor lifecycle: `on_start(args, ActorRef<Self>) -> Self`, `Args =
  Self` common case, `&mut self` lifecycle hooks.
- `https://docs.rs/kameo/latest/src/kameo/message.rs.html` — Kameo
  `Message<T>` handler shape and sequential mutable state access.
- `https://docs.rs/kameo/latest/kameo/actor/trait.Spawn.html` — Kameo
  spawn, spawn-link, prepared actor, mailbox options.
- `https://docs.rs/ractor/latest/ractor/actor/trait.Actor.html` —
  `ractor` actor trait with associated `Msg`, `State`, and
  `Arguments`.
