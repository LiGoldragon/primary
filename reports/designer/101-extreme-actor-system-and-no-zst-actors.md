# 101 — workspace-actor trait proposal

*Designer report. The actors-as-correctness-device principle
is workspace-wide (every system Li builds, in any language
with actor-shaped concurrency) — its canonical home is
`~/primary/skills/actor-systems.md`. That skill names a gap:
*"Persona-facing code should not model actors as public ZST
behavior markers ... [implement] the workspace actor trait
once that trait exists."* This report fills that gap with a
concrete trait + handle + ractor-adapter proposal at
workspace scope. It supersedes the prior framing of this
report (commit d354a67), which scoped the principle to
persona-mind and named the crate `persona-actor` — both
wrong-scoped per the user's correction.*

---

## 0 · TL;DR

The principle (actors as correctness device; density rule;
no-ZST shape; handle-as-public-surface) lives in
`~/primary/skills/actor-systems.md`. Read that first; this
report doesn't restate it.

The skill names a missing piece: **the workspace actor
trait**. This report proposes its concrete shape:

- **Crate**: `workspace-actor` (proposed; alternatives in §4).
- **Trait**: `workspace_actor::Actor` — `Self` carries the
  actor's data; `open(args) -> Result<Self, _>`
  self-constructs; `handle(&mut self, msg)` mutates `self`.
  No separate `State` type.
- **Public consumer surface**: `workspace_actor::Handle<A>`
  — typed; never raw `ractor::ActorRef`.
- **Single permitted ZST**: `RactorAdapter<A>` inside the
  crate, hidden from consumers — the *one* framework-glue
  ZST the skill's "When not to create an actor" carve-out
  permits. Never repeated per actor.

§1 — the trait declaration. §2 — the handle. §3 — the
ractor adapter (the framework boundary). §4 — naming
options. §5 — adoption order across the workspace's actor
work in flight. §6 — open questions.

---

## 1 · The trait

```rust
//! workspace-actor — the workspace's actor trait.
//!
//! Every actor in any system the workspace builds implements
//! this trait. The `Self` type carries the actor's data
//! (configuration, in-flight state, child handles, metrics);
//! the trait methods operate on `self` directly. No separate
//! State type, no public ZST behavior marker.
//!
//! For the principle and the density rule, see
//! `~/primary/skills/actor-systems.md`. This crate is the
//! mechanism.

pub trait Actor: Sized + Send + 'static {
    /// Construction input. Carries the configuration the
    /// actor needs to assemble its initial data.
    type Argument: Send;

    /// The closed message vocabulary this actor accepts.
    type Message: Send + 'static;

    /// The closed reply vocabulary this actor produces.
    type Reply: Send + 'static;

    /// Typed failure (per `~/primary/skills/rust-discipline.md`
    /// §"Errors") — never `anyhow`.
    type Failure: std::error::Error + Send + 'static;

    /// Build the actor's data from arguments. The returned
    /// Self IS the actor; no separate State type. May be
    /// async to allow IO during open (loading from sema,
    /// contacting a sibling).
    async fn open(arguments: Self::Argument)
        -> Result<Self, Self::Failure>;

    /// Handle one message. Operates on self's data directly.
    /// The reply travels back through the handle's reply port.
    async fn handle(&mut self, message: Self::Message)
        -> Result<Self::Reply, Self::Failure>;

    /// Optional cleanup before the actor's data drops.
    async fn close(self) -> Result<(), Self::Failure> {
        Ok(())
    }

    /// Stable typed identity for trace + manifest comparison
    /// (per skills/actor-systems.md §"Traces are required").
    fn kind() -> ActorKind {
        ActorKind::from_type_name::<Self>()
    }
}
```

What changes from ractor's shape:

- **One associated type fewer.** ractor: `State`,
  `Arguments`, `Msg`. workspace-actor: `Argument`, `Message`,
  `Reply`, `Failure` — the State collapses into `Self`.
- **`open` instead of `pre_start`.** The actor constructs
  itself; the framework hosts the result.
- **`handle` on `&mut self`, not on `(&self, state)`.** The
  data is on `self`; the verb attaches to its noun.
- **`Reply` is part of the trait.** ractor handles replies
  via `RpcReplyPort` per message; workspace-actor types the
  reply at the trait level so call sites see `Result<A::Reply,
  _>` from `Handle::ask`.
- **Typed `Failure` enum.** Per rust-discipline.md §"Errors";
  never erased to `anyhow`.

---

## 2 · The handle

```rust
/// The consumer-facing surface of any actor of type `A`.
/// Constructed by `Handle::spawn_under(parent, args)`;
/// dropped to detach (the actor itself is supervised by
/// its parent and outlives any one handle).
pub struct Handle<A: Actor> {
    sender: ActorSender<A::Message>,
    join:   ActorJoin,
    kind:   ActorKind,
    path:   ActorPath,
}

impl<A: Actor> Handle<A> {
    /// Spawn `A` under `parent`'s supervision.
    pub async fn spawn_under(
        parent: &impl SupervisorRef,
        arguments: A::Argument,
    ) -> Result<Self, SpawnFailure<A::Failure>>;

    /// Send a message; await the typed reply.
    pub async fn ask(&self, message: A::Message)
        -> Result<A::Reply, AskFailure<A::Failure>>;

    /// Send a message; don't wait for reply (fire-and-forget).
    pub fn tell(&self, message: A::Message)
        -> Result<(), TellFailure>;

    /// Topology introspection — the actor's typed path in
    /// the supervision tree (per skills/actor-systems.md
    /// §"Test actor density").
    pub fn path(&self) -> &ActorPath { &self.path }

    /// Stable typed identity (per A::kind()).
    pub fn kind(&self) -> ActorKind { self.kind }
}
```

Consumers never name `ractor::ActorRef`. Spawning,
messaging, topology introspection — all through `Handle<A>`.

---

## 3 · The ractor adapter — the single permitted ZST

ractor's trait expects a ZST behavior marker. The adapter
provides one — *one*, internal to the crate, generic over
any `Actor`:

```rust
/// Internal — never imported by consumer crates. Carries no
/// data; bridges workspace_actor::Actor into ractor's
/// trait shape. The `state: A` parameter on ractor::handle
/// is the workspace actor's Self.
struct RactorAdapter<A: Actor>(PhantomData<A>);

impl<A: Actor> ractor::Actor for RactorAdapter<A> {
    type State     = A;                          // ← Self IS the state
    type Arguments = A::Argument;
    type Msg       = AdapterMessage<A>;

    async fn pre_start(
        &self,
        _myself: ActorRef<Self::Msg>,
        arguments: Self::Arguments,
    ) -> Result<Self::State, ActorProcessingErr> {
        A::open(arguments).await
            .map_err(|f| ActorProcessingErr::from(f))
    }

    async fn handle(
        &self,
        _myself: ActorRef<Self::Msg>,
        msg: Self::Msg,
        state: &mut Self::State,    // ← state IS A; methods on A run directly
    ) -> Result<(), ActorProcessingErr> {
        match msg {
            AdapterMessage::Ask { message, reply } => {
                let result = state.handle(message).await;
                let _ = reply.send(result);
                Ok(())
            }
            AdapterMessage::Tell { message } => {
                let _ = state.handle(message).await;
                Ok(())
            }
            AdapterMessage::Close => Ok(()),
        }
    }
}
```

This is the *only* ZST consumer code never sees. It satisfies
the skill's narrow ZST exception (framework-marker glue
delegating to a data-bearing partner type — here, `A` itself).

---

## 4 · Crate naming

Three viable names; user picks:

| Name | For | Against |
|---|---|---|
| **`workspace-actor`** | Matches the skill's wording (*"the workspace actor trait"*); descriptive | Slightly generic |
| `goldragon-actor` | Workspace-prefixed; explicit ownership | Ties the crate to the cluster name |
| `actor` | Cleanest at use site (`actor::Actor`) | Conflicts with `ractor::Actor` in code that imports both |

**Recommendation: `workspace-actor`.** The crate's name
matches the discipline it implements (per the skill); the
prefix honestly says "workspace-level, not project-specific."

Inside the crate, the trait is named simply `Actor`
(`workspace_actor::Actor`). At consumer use sites:

```rust
use workspace_actor::{Actor, Handle};

impl Actor for ClaimNormalize { … }
let handle: Handle<ClaimNormalize> = Handle::spawn_under(&parent, args).await?;
```

Reads cleanly. No prefix on the trait name (per
`~/primary/skills/naming.md` §"Anti-pattern: prefixing type
names with the crate name") — `WorkspaceActor` would repeat
the namespace.

---

## 5 · Adoption order

The skill applies workspace-wide; `workspace-actor` is the
mechanism. Adoption sequence across in-flight work:

1. **Ship `workspace-actor` crate.** Designer creates the
   contract repo (mirror of `signal-persona-orchestrate`'s
   shape per `~/primary/skills/contract-repo.md`); operator
   implements the adapter + handle. Tests cover trait
   conformance + adapter round-trip. Ship before any consumer
   adopts.

2. **Persona-mind Phase 1 uses `workspace-actor` from day
   one** — addresses operator-assistant/97 (`reports/operator-assistant/97-persona-mind-actor-density-compliance-review.md`)
   compliance gap. The compliance review's "add ractor to
   persona-mind" recommendation becomes "add workspace-actor
   to persona-mind." Every actor in operator/101's tree
   implements `workspace_actor::Actor`. No raw `ractor::Actor`
   impls in `persona-mind`.

3. **persona-router, persona-message, persona-system actor
   work** — when those components reach actor-shaped
   implementation per the skill, they adopt workspace-actor
   directly. The compliance review's deferral order
   (operator-assistant/97 §"Defer until mind Phase 1
   visible") still applies.

4. **Future systems** (criome long-running daemons,
   chroma, chronos, mentci) — adopt workspace-actor for any
   actor-shaped component from the start.

5. **`~/primary/repos/lore/rust/ractor.md`** — system-specialist
   adds a section: *"In Persona components and any
   workspace-built daemon, don't use ractor's Actor trait
   directly — use `workspace_actor::Actor` instead. ractor
   stays the runtime; workspace-actor is the discipline."*

6. **`~/primary/skills/rust-discipline.md` §"No ZST method
   holders"** — system-specialist or designer removes the
   "ractor actor behaviour markers" carve-out from the
   legitimate-ZST list; replaces with a pointer to
   workspace-actor's adapter. The carve-out becomes one
   adapter ZST inside one crate, not a per-actor pattern.

---

## 6 · Open questions

1. **Async `open` cost.** `async fn` in traits requires
   `async-trait` or trait fn returning impl Future. ractor
   already pulls in tokio; `async-trait` is the path of least
   resistance for v1. Pin in the crate.

2. **Reply type for fire-and-forget.** Actors that only
   accept `tell` (no reply) set `type Reply = ();`. The
   handle's `tell()` discards the unit reply. Simpler than
   splitting the trait into ask/tell variants.

3. **Sync actors.** Some actors (id mint, encode) are
   pure-CPU and sync would be enough. Either: keep `async
   fn` everywhere (uniform); add a sync sibling trait
   (`workspace_actor::SyncActor`) with a sync adapter. Defer
   until profile shows real cost.

4. **Virtual actors.** The skill's worked actor table doesn't
   yet include virtual-activation patterns
   (operator/102 §3.3 — Orleans-style activate-on-message
   for items/roles). A future `workspace_actor::VirtualActor`
   trait probably wraps `Actor` with a `load_from(ItemId)
   -> Self` constructor and a deactivation policy. Defer
   until virtual actors land.

5. **Topology dump format.** `ActorPath` and `ActorKind` are
   typed; the topology dump (skill §"Test actor density":
   topology manifest test) needs a wire format. Probably
   NOTA-projectable typed records. Pin when the test fixture
   lands.

---

## See also

- `~/primary/skills/actor-systems.md` — the canonical home
  for the actors-as-correctness principle, density rule,
  no-ZST shape, blocking rule, supervision rule, traces, and
  test families. This report's trait + handle + adapter are
  the mechanism the skill names but doesn't pin.
- `~/primary/reports/operator/102-actor-heavy-persona-mind-research.md`
  — operator's framework survey + `persona-actor` crate
  proposal. This report renames the crate to `workspace-actor`
  (not Persona-specific) and pins the trait shape.
- `~/primary/reports/operator-assistant/97-persona-mind-actor-density-compliance-review.md`
  — compliance audit naming the "add ractor to persona-mind"
  step; should become "add workspace-actor to persona-mind"
  per §5 adoption order.
- `~/primary/reports/operator/101-persona-mind-full-architecture-proposal.md`
  — the actor-dense Persona-mind architecture; every actor in
  its tree implements workspace_actor::Actor per §5.
- `~/primary/reports/designer/100-persona-mind-architecture-proposal.md`
  §3 — caller-identity mechanism (`CallerIdentityActor` +
  `EnvelopeActor`); both implement `workspace_actor::Actor`.
- `~/primary/skills/rust-discipline.md` §"No ZST method
  holders" — the rule §5.6 proposes updating to remove the
  ractor exception once workspace-actor ships.
- `~/primary/skills/contract-repo.md` — the repo discipline
  workspace-actor's contract crate follows.
- `~/primary/skills/naming.md` §"Anti-pattern: prefixing type
  names with the crate name" — the rule §4 follows in
  naming the trait `Actor` not `WorkspaceActor`.
- `~/primary/repos/lore/rust/ractor.md` — current ractor
  reference; §5.5 proposes adding the *"use workspace-actor
  instead"* note.
