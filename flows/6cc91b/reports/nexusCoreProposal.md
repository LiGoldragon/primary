# Nexus core, metaNexus, and the architecture guard

A proposal in anatomy. Every claim about existing code is witnessed `file:line`; code paths are
relative to `/git/github.com/LiGoldragon/`. Terms, per the living
(`flows/6cc91b/vision/nexus.md:19-27`): **core** is the library, **metaNexus** the whole running
thing, **Nexus** unqualified whichever the context makes obvious — an unclear speaker being at
fault.

## 1. The three actors

### Nexus (the process actor)

Owns the decision and all durable authority. `orchestrate` already built it so:
`orchestrate-nexus/src/core.rs:105-108` declares `NexusCore { store, announcements }`, and
`core.rs:5-9` states "it is the only actor in the Nexus... the only way in is a message."

- **In**: a Nexus-kind work value, raised from a Signal query or settled from a Sema result.
  Today `core.rs:130` is `Message<OrdinaryQuery>` and `core.rs:160` `Message<MetaQuery>` —
  the Nexus names Signal types *directly*, the hole this proposal closes.
- **Out**: a Nexus-kind action — reply, Sema write, Sema read, effect, continue. That
  five-way sum exists: `triad-runtime/src/reaction.rs:57-63` `Action<Reply, Write, Read,
  Effect, Continuation>`, `runner.rs:26-32` `NextStep`.
- **Never**: touch a socket, touch a file, or block.

### Signal (the edge actor)

Owns bytes, framing, sockets, peer credentials, backpressure — all of it written:
`triad-runtime/src/async_runtime.rs` (1723 lines), `src/frame.rs`, and the two tiers at
`nexus/src/authority.rs:18-24` (`SocketAuthority::{Ordinary, Privileged}`), `authority.rs:33-46`
giving `0o660`/`0o600` and the owner-only admit rule.

- **In**: a byte frame off a bound socket with its connection context
  (`triad-runtime/src/lib.rs:42-47`: `ConnectionContext`, `PeerIdentity`,
  `UnixCredentials`).
- **Out**: a Signal-kind query handed *to the Nexus*; a Signal-kind response back.
- **Never**: reach the store. Nothing stops it today — `message/src/daemon.rs:105` has the
  connection task call `self.engine.lock().await.handle(query, &context)`: the Signal actor
  holding a mutex on the engine, exactly the forbidden edge.

### Sema (the storage actor)

Owns the durable state and its migrations. `sema-engine/src/lib.rs:43` exports `Engine,
EngineOpen, StorageReader`; `lib.rs:8-11` makes the commit log authoritative and "the storage
kernel hands out read access only." `orchestrate-nexus/src/store/mod.rs:38-50` is one
component's Sema actor body.

- **In**: a Sema-kind write or read input — names that already exist at
  `triad-runtime/src/role.rs:5-11`.
- **Out**: a Sema-kind result, returned only to the Nexus.
- **Never**: construct or observe a Signal value, or decide policy.
  `orchestrate-nexus/src/store/mod.rs:28` imports
  `signal_orchestrate::OrchestrateNexusConfiguration` into the store — a Signal type inside
  the Sema actor, the same hole from the other side.

## 2. metaNexus, and "Nexus is the only main call"

The metaNexus is the composition of the three, founded by the core. The living's layering
statement (`flows/6cc91b/vision/rustLayering.md:7`) asks a high layer that "looks kind of like
baby code", implementation blocks in separate files:

```rust
mod ethos;   // generated: the Nexus ethos types and the crossings between kinds
mod nexus;   // impl NexusActor  — the decision blocks
mod sema;    // impl SemaActor   — the store blocks
mod signal;  // impl SignalActor — the contract blocks

use nexus_core::{Founding, Metanexus, Running};

fn main() -> std::process::ExitCode {
    Metanexus::<nexus::Orchestrate>::founded().run()
}
```

Ten lines. `Metanexus<N>` is the core's type: given the Nexus actor it resolves that actor's
associated Signal and Sema actors, opens the store, binds both sockets, founds the core actor
and serves — all of it written already, but written *in the components*.
`lojix/nexus/src/main.rs:7-20` is 14 lines and closest already;
`orchestrate-nexus/src/main.rs:8-38` is a 31-line body opening the store, building a two-worker
Tokio runtime, binding transport and serving — every one of those lines universal, and the
core's.

## 3. The architecture guard

The living: "each type has their own intrinsic kinds applied... Only this kind of actor can
react with this type of object... a higher-type kind compiler check"
(`flows/6cc91b/vision/nexus.md:27`). In Rust today: a **sealed** kind trait (no crate can add an
actor), a **phantom kind marker** on every value, and a **sealed crossing relation** whose
missing impl is the error.

```rust
// nexus-core/src/kind.rs — private module, the seal
mod seal { pub trait Sealed {} }

/// The three intrinsic actor kinds. Sealed: the set is closed.
pub trait ActorKind: seal::Sealed + 'static {}
pub struct Signal; pub struct Nexus; pub struct Sema;
impl seal::Sealed for Signal {} impl ActorKind for Signal {}
impl seal::Sealed for Nexus  {} impl ActorKind for Nexus  {}
impl seal::Sealed for Sema   {} impl ActorKind for Sema   {}

/// Every value is borne by exactly one actor kind.
pub struct Borne<K: ActorKind, T> { value: T, kind: PhantomData<K> }

/// The whole crossing graph. Sealed by ActorKind's seal.
pub trait Crossing<From: ActorKind, To: ActorKind> {}
impl<T> Crossing<Signal, Nexus> for Raise<T> {}   // a query enters
impl<T> Crossing<Nexus, Sema>   for Command<T> {} // a write is commanded
impl<T> Crossing<Sema, Nexus>   for Settle<T> {}  // a result returns
impl<T> Crossing<Nexus, Signal> for Lower<T> {}   // a response leaves
// Signal <-> Sema: deliberately no impl, and none can be added.

pub fn hand<C, F, T, V>(_crossing: C, borne: Borne<F, V>) -> Borne<T, V>
where F: ActorKind, T: ActorKind, C: Crossing<F, T> { /* … */ }
```

A Signal actor that tries `hand(x, sema_write)` fails neither a test nor at runtime: it fails to
typecheck — `the trait bound Crossing<Signal, Sema> is not satisfied`. The guard is the
*absence* of an impl in a sealed relation, which is why it holds for every future component the
core never hears of.

Two witnessed footholds:

- `triad-runtime/src/role.rs:3-15` already declares the marker traits (`NexusWork`,
  `SemaWriteInput`, `SemaReadInput`, `NexusEffectCommand`, …) — the right nouns with none of
  the force: each is an empty `pub trait` any crate may implement for any type
  (`role.rs:35-45` implements six for `Infallible`), so a Signal type may bear
  `SemaWriteInput` freely today.
- Generated code already splits the worlds by *derive*: a Sema root emits `Datomizable,
  Composing, Clone, Debug, PartialEq, Eq, Hash` with **no rkyv**
  (`ethos-zero/tests/generated/entry-sema.rs:3`), a Signal root emits `rkyv::Archive,
  rkyv::Serialize, …` (`signal-message/src/generated/signal.rs:9-10`). So a Sema record
  cannot reach a wire today — an accident of derive selection, not a guard: any component
  can hand-add the rkyv derive.

Ethos-zero knows the three roots already (`ethos-zero/README.md`: Library, Signal, Sema) and a
kind declaration already becomes a plain Rust trait —
`ethos-zero/tests/generated/capability-kinds.rs:3-13` turns `Summarizable.[ summarize.[ String ]
]` into `pub trait Summarizable { fn summarize(&self) -> String; }`. Missing: the root should
*stamp* the kind — a `Signal` root's types emitting `impl Borne<kind::Signal>`, a `Sema` root's
`impl Borne<kind::Sema>`, and a new **Nexus ethos root**, the "Nexus ethos type file" the living
names (`nexus.md:25`), emitting the Nexus-kind types and the four crossings.

## 4. What the `nexus` crate has today, and what it lacks

Has (841 lines, four modules, `nexus/src/lib.rs:8-16`):

- `ConfigurationState<C>` + `Configurable<C>` — the desired/meta configure lifecycle
  (`configuration.rs:9-12`, `:25-39`).
- `SocketAuthority` + `Permissive` — the two socket tiers (`authority.rs:18-24`, `:33-46`).
- `Situation`/`Situating`/`Situated` + `StoreIdentity` — observed bind state, and the
  copy-versus-move bearing (`situation.rs:38-42`, `:107-117`, `:222-230`).
- `Relocation`/`Relocating`/`Relocated` — the owner's move declaration
  (`relocation.rs:40-43`, `:90-94`).

Lacks: any notion of an actor; the three kinds and their seal; the crossing relation;
`Metanexus<N>` and a `run`; the founding of the core actor; socket binding; the runner loop. Its
only dependencies are `rkyv` and `thiserror` (`nexus/Cargo.toml`) — not `kameo`, `sema-engine`,
`signal` — so it cannot today be the base of a Nexus. Its own rule explains the gap: "A kind
enters this crate on its second implementation, never on its first"
(`nexus/ARCHITECTURE.md:36-39`) — and with three metaNexuses standing, it has arrived.

## 5. What each component deletes or moves

**`triad-runtime` is the donor.** `src/role.rs` (45 lines) moves into the core, sealed;
`src/reaction.rs:41-63` (`Work`, `Action`) and `src/runner.rs:26-66` (`NextStep`,
`RunnerEngines`) become the Nexus actor's frame; `src/async_runtime.rs` (1723 lines) and
`src/frame.rs` become the Signal actor. Carry the disproof at `reaction.rs:65-103` forward:
`enum Never {}` cannot bear the rkyv 0.8 derive stack, so an absent leg needs a derivable
stand-in.

**`orchestrate`** — smallest delta. Delete the body of `orchestrate-nexus/src/main.rs:8-38`.
`transport/mod.rs:32-46` (`TransportRuntime`, `BoundSocket`) and `transport/socket.rs` move to
the Signal actor; `transport/session.rs` (449 lines) becomes the generated Signal→Nexus
crossing. `core.rs:105-108` stays, but `core.rs:130` and `:160` stop being
`Message<OrdinaryQuery>`/`Message<MetaQuery>` and become `Message<Borne<Nexus,_>>`.
`store/mod.rs` stays as the Sema actor, minus its `signal_orchestrate` import
(`store/mod.rs:28`).

**`message`** — furthest. `src/bin/message_daemon.rs:4-13` takes a configuration path argument,
against `Vision/nexus.md:76` ("A Nexus starts with no arguments"); delete it with the
`from_configuration_path` constructor (`daemon.rs:43-45`). `daemon.rs:55-79` (`run_async`,
socket list, runtime assembly) and `MessageRuntime` (`daemon.rs:82-126`) are the core's job
entirely, and the `engine.lock().await` at `daemon.rs:105` — the forbidden Signal→Sema edge —
goes with them. `MessageEngine` becomes the Nexus actor's blocks; `src/main.rs:3-9` is a CLI,
not a Nexus, and moves to a client crate.

**`lojix`** — largest deletion. `src/daemon.rs` is 1293 lines of hand-rolled metaNexus:
`ListenerRole` (`daemon.rs:77-81`), the meta framing kinds (`:37-62`), the request timeout
(`:34`) — all universal, all to the core. `src/runtime_flow.rs` is already the Nexus actor
(`:1-5`) and `src/runtime_model.rs` already the Sema actor (`:1-5`): the split the living wants
is *already drawn there by hand*. `src/adapters.rs` (`Lowerable`, `Raisable`, used at
`daemon.rs:64`) is exactly the crossing, and becomes generated. `nexus/src/main.rs:7-20` shrinks
to the call.

## 6. Where Forge fits

Per `flows/6cc91b/vision/forge.md:11-13`, Forge is the build language and build manager, not a
fourth actor: it dispatches these crates, and the living's framing at
`flows/6cc91b/vision/nexus.md:15` — "Forge essentially doing everything that cargo used to do
... with source caching" — puts it one level below this proposal, not inside it. The connection
is narrow: the kind guard is a compile-time check, so whatever drives the compiler must know the
three-crate-per-component shape (core, generated ethos, component) and must not let a build
reach a crate its kind forbids — module privacy guards within a crate, the crate graph is
Forge's to guard. Forge is itself a Nexus on this core, so the proof the anatomy holds is that
Forge is buildable as one; its standard objects mapping to Nix derivations (`forge.md:11`) are
ordinary Sema-kind records of that Nexus, the native CriomOS sandbox side named apart
(`forge.md:13`). Nothing in sections 1-5 waits on Forge.

## 7. Open questions for the living

1. **Does the Nexus actor see Signal types at all, or only raised ones?**
   `orchestrate-nexus/src/core.rs:130` has the Nexus handle `signal_orchestrate::Query`
   directly. Read strictly, `nexus.md:25` says it never names a Signal type:
   `Query::Lock(request)` would arrive as `Borne<Nexus, LockIntent>` through a generated
   crossing — one more generated type per query. Strict, or may the Nexus own the Signal
   enum as its input?

2. **Is the Signal actor one actor or one per socket?** Every metaNexus has exactly two
   tiers today — `ListenerRole::{Ordinary, Owner}` at `message/src/daemon.rs:19-22` and
   `lojix/src/daemon.rs:77-81` — but `Vision/nexus.md:39` allows more sockets. Is `Signal`
   one kind with a socket tag, or is the meta surface its own kind with its own crossing, so
   an ordinary session cannot construct a meta query *by type* rather than by match?

3. **Does the Nexus ethos root name the crossings, or infer them?** Given `Signal` declares
   `Lock.LockRequest` and `Sema` declares `StoredLock`, does the Nexus ethos file write the
   crossing explicitly (`Lock.LockIntent`, then `LockIntent.StoredLock`), or does ethos-zero
   derive it from name agreement? Explicit is more text; inferred serves
   `Vision/ethos.md:24-26`.

4. **What happens to the fourth leg, effects?** `triad-runtime/src/reaction.rs:44` has
   `EffectCompleted(Effect)` and `runner.rs:55` `run_effect` — lojix shells out to Nix
   through it, and an effect is neither Signal, Nexus, nor Sema. A fourth sealed kind
   crossing only to and from `Nexus`, or does the Nexus run effects and become the one actor
   that blocks?

## Sources

- Living, today: `flows/6cc91b/vision/nexus.md:11-17`, `:19-29`;
  `flows/6cc91b/vision/rustLayering.md:7`; `flows/6cc91b/vision/forge.md:7-13`.
- Living, 2026-09-13: `flows/6cc91b/vision/nexus.md:3-9`;
  `flows/024bc7/vision/nexus.md:3-27`.
- Distilled: `Vision/nexus.md`, `Vision/sema.md`, `Vision/signal.md`, `Vision/ethos.md`.
- Code, read 2026-09-14 under `/git/github.com/LiGoldragon/`: `nexus/` entire `src/`,
  `ARCHITECTURE.md`, `Cargo.toml`; `triad-runtime/src/{lib,role,reaction}.rs`, `runner.rs:1-120`;
  `orchestrate/crates/orchestrate-nexus/src/{lib,core,main}.rs`, `store/mod.rs:1-80`,
  `transport/mod.rs:1-70`; `message/src/{main,daemon}.rs`, `src/bin/*.rs`; `lojix/nexus/src/main.rs`,
  `src/daemon.rs:1-90`, `src/{runtime_flow,runtime_model}.rs:1-60`; `ethos-zero/src/lib.rs:1-70`,
  `README.md`, `fixtures/capability-kinds.ethos`, `tests/generated/{capability-kinds,entry-sema}.rs`;
  `sema-engine/src/lib.rs:1-89`; `signal-message/{ethos/signal.ethos,src/generated/signal.rs:1-70}`.
- Method: direct read, no build run. Sections 2 and 3 are proposals, not compiled code.
