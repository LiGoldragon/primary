# Nexus core, metaNexus, and the architecture guard

A proposal in anatomy. Every claim about existing code is witnessed `file:line`.
Repository root for code paths: `/git/github.com/LiGoldragon/`.

Terms, per the living (`flows/6cc91b/vision/nexus.md:19-27`): **core** is the
library; **metaNexus** is the whole running thing; **Nexus** unqualified is
whichever the context makes obvious, and an unclear speaker is at fault.

## 1. The three actors

### Nexus (the process actor)

Owns: the decision. It is the only actor that holds durable authority, and
`orchestrate` already built it this way — `orchestrate-nexus/src/core.rs:105-108`
declares `NexusCore { store, announcements }` and `core.rs:5-9` states "it is the
only actor in the Nexus... the only way in is a message."

- **Inputs**: a Nexus-kind work value, raised from a Signal query or lowered from
  a Sema result. Today: `core.rs:130` `Message<OrdinaryQuery>` and `core.rs:160`
  `Message<MetaQuery>` — the Nexus receives signal types *directly*, which is the
  hole this proposal closes.
- **Outputs**: a Nexus-kind action — reply, Sema write, Sema read, effect,
  continue. That five-way sum exists today as `triad-runtime/src/reaction.rs:57-63`
  `Action<Reply, Write, Read, Effect, Continuation>` and
  `triad-runtime/src/runner.rs:26-32` `NextStep`.
- **Must not**: touch a socket, touch a file, or block. `core.rs:110-114` already
  argues there is no `on_stop` because every transition commits before answering.

### Signal (the edge actor)

Owns: bytes, framing, sockets, peer credentials, backpressure. All of it exists:
`triad-runtime/src/async_runtime.rs` (1723 lines), `triad-runtime/src/frame.rs`,
and the two-tier socket authority in `nexus/src/authority.rs:18-24`
(`SocketAuthority::{Ordinary, Privileged}`) with `authority.rs:33-46` giving mode
`0o660`/`0o600` and the owner-only admit rule.

- **Inputs**: a byte frame off a bound socket, plus the connection context
  (`triad-runtime/src/lib.rs:42-47` exports `ConnectionContext`, `PeerIdentity`,
  `UnixCredentials`).
- **Outputs**: a Signal-kind query handed *to the Nexus*, and a Signal-kind
  response written back.
- **Must not**: reach the store. Today nothing stops it: `message/src/daemon.rs:105`
  has the connection task call `self.engine.lock().await.handle(query, &context)`
  — the Signal actor holding a mutex on the engine, which is precisely the
  forbidden edge.

### Sema (the storage actor)

Owns: the durable state and its migrations. `sema-engine/src/lib.rs:43` exports
`Engine, EngineOpen, StorageReader`; `sema-engine/src/lib.rs:8-11` states the
commit log is authoritative and "the storage kernel hands out read access only."
`orchestrate-nexus/src/store/mod.rs:38-50` is one component's Sema actor body.

- **Inputs**: a Sema-kind write or read input. The kinds already have names:
  `triad-runtime/src/role.rs:5-11` — `SemaWriteInput`, `SemaWriteOutput`,
  `SemaReadInput`, `SemaReadOutput`.
- **Outputs**: a Sema-kind result, returned only to the Nexus.
- **Must not**: construct or observe a Signal value; must not decide policy.
  `orchestrate-nexus/src/store/mod.rs:28` imports `signal_orchestrate::OrchestrateNexusConfiguration`
  into the store — a Signal type inside the Sema actor, the same hole from the
  other side.

## 2. metaNexus, and "Nexus is the only main call"

The metaNexus is the composition of the three, founded by the core. The living's
Rust layering statement (`flows/6cc91b/vision/rustLayering.md:7`) asks for a
high layer that "looks kind of like baby code" with the implementation blocks in
separate files. Applied to `main.rs`:

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

Ten lines. `Metanexus<N>` is the core's type: given the Nexus actor, the core
resolves that actor's associated Signal and Sema actors, opens the store, binds
both sockets, founds the core actor, and serves — all of which is written already
but written *in the components*. Measured against what exists:
`lojix/nexus/src/main.rs:7-20` is 14 lines and closest to the shape already;
`orchestrate-nexus/src/main.rs:8-38` is a 31-line body that opens the store,
builds a two-worker Tokio runtime, binds transport and serves — every one of
those lines is universal and belongs in the core.

## 3. The architecture guard

The living: "each type has their own intrinsic kinds applied... Only this kind of
actor can react with this type of object... a higher-type kind compiler check"
(`flows/6cc91b/vision/nexus.md:27`). In Rust today this is three mechanisms
composed: a **sealed** kind trait (no downstream crate can add an actor), a
**phantom kind marker** on every value, and a **sealed crossing relation** whose
missing impl is the error.

```rust
// nexus-core/src/kind.rs — private module, the seal
mod seal { pub trait Sealed {} }

/// The three intrinsic actor kinds. Sealed: this set is closed.
pub trait ActorKind: seal::Sealed + 'static {}
pub struct Signal; pub struct Nexus; pub struct Sema;
impl seal::Sealed for Signal {} impl ActorKind for Signal {}
impl seal::Sealed for Nexus  {} impl ActorKind for Nexus  {}
impl seal::Sealed for Sema   {} impl ActorKind for Sema   {}

/// Every value in a metaNexus is borne by exactly one actor kind.
pub struct Borne<K: ActorKind, T> { value: T, kind: PhantomData<K> }

/// The crossings that exist. Sealed by ActorKind's seal — no component
/// can declare a new one, and the four written here are the whole graph.
pub trait Crossing<From: ActorKind, To: ActorKind> {}
impl<T> Crossing<Signal, Nexus> for Raise<T> {}   // a query enters
impl<T> Crossing<Nexus, Sema>   for Command<T> {} // a write is commanded
impl<T> Crossing<Sema, Nexus>   for Settle<T> {}  // a result returns
impl<T> Crossing<Nexus, Signal> for Lower<T> {}   // a response leaves
// Signal <-> Sema: deliberately no impl, and none can be added.

/// The only way a value moves between actors.
pub fn hand<C, F, T, V>(_crossing: C, borne: Borne<F, V>) -> Borne<T, V>
where F: ActorKind, T: ActorKind, C: Crossing<F, T> { /* … */ }
```

A Signal actor that tries `hand(x, sema_write)` does not fail a test and does not
fail at runtime: it fails to typecheck, with `the trait bound
Crossing<Signal, Sema> is not satisfied`. The guard is the *absence* of an impl
in a sealed relation, which is why it holds for every future component without
the core knowing any of them.

Two witnessed footholds make this cheaper than it looks:

- `triad-runtime/src/role.rs:3-15` already declares the marker traits
  (`NexusWork`, `SemaWriteInput`, `SemaReadInput`, `NexusEffectCommand`, …). They
  are the right nouns with none of the force: each is an empty `pub trait` any
  crate can implement for any type (`role.rs:35-45` implements six of them for
  `Infallible`), so today a Signal type may bear `SemaWriteInput` freely.
- The generated code already separates the two worlds by *derive*: a Sema root
  emits `#[derive(datom_codec::Datomizable, datom_codec::Composing, Clone, Debug,
  PartialEq, Eq, Hash)]` with **no rkyv** (`ethos-zero/tests/generated/entry-sema.rs:3`),
  while a Signal root emits `#[derive(rkyv::Archive, rkyv::Serialize, …)]`
  (`signal-message/src/generated/signal.rs:9-10`). A Sema record therefore cannot
  currently be put on a wire — but that is an accident of derive selection, not a
  guard: any component can hand-add the rkyv derive.

The ethos side: ethos-zero knows the three roots already
(`ethos-zero/README.md`, "Library / Signal / Sema"), and a kind declaration
already becomes a plain Rust trait — `ethos-zero/tests/generated/capability-kinds.rs:3-13`
turns `Summarizable.[ summarize.[ String ] ]` into `pub trait Summarizable { fn
summarize(&self) -> String; }`. What is missing is that the root should *stamp*
the kind: a `Signal` root's types emit `impl Borne<kind::Signal>`, a `Sema` root's
`impl Borne<kind::Sema>`, and a new **Nexus ethos root** — the "Nexus ethos type
file" the living names (`flows/6cc91b/vision/nexus.md:25`) — emits the Nexus-kind
types and the four crossings between them.

## 4. What the `nexus` crate has today, and what it lacks

Has (841 lines, four modules, `nexus/src/lib.rs:8-16`):

- `ConfigurationState<C>` + `Configurable<C>` — the desired/meta configure
  lifecycle (`nexus/src/configuration.rs:9-12`, `:25-39`).
- `SocketAuthority` + `Permissive` — the two socket tiers
  (`nexus/src/authority.rs:18-24`, `:33-46`).
- `Situation`/`Situating`/`Situated` + `StoreIdentity` — observed bind state and
  the copy-versus-move bearing (`nexus/src/situation.rs:38-42`, `:107-117`, `:222-230`).
- `Relocation`/`Relocating`/`Relocated` — the owner's move declaration
  (`nexus/src/relocation.rs:40-43`, `:90-94`).

Lacks, all of it: any notion of an actor; the three kinds and their seal; the
crossing relation; `Metanexus<N>` and a `run`; the founding of the core actor;
socket binding; the runner loop. Its only dependencies are `rkyv` and `thiserror`
(`nexus/Cargo.toml`) — it does not depend on `kameo`, `sema-engine`, or `signal`,
so it cannot today be the base of a Nexus. Its own rule explains the gap:
"A kind enters this crate on its second implementation, never on its first"
(`nexus/ARCHITECTURE.md:36-39`). Three metaNexuses now exist; the second
implementation has arrived.

## 5. What each component deletes or moves

**`triad-runtime` is the donor.** `src/role.rs` (45 lines) moves into the core and
is sealed. `src/reaction.rs:41-63` (`Work`, `Action`) and `src/runner.rs:26-66`
(`NextStep`, `RunnerEngines`) move in as the Nexus actor's frame.
`src/async_runtime.rs` (1723 lines) and `src/frame.rs` become the core's Signal
actor. Carry forward the disproof recorded at `triad-runtime/src/reaction.rs:65-103`:
`enum Never {}` cannot bear the rkyv 0.8 derive stack, so an absent leg needs a
derivable stand-in, not an uninhabitable one.

**`orchestrate`** — closest to the shape, smallest delta. Delete the body of
`orchestrate-nexus/src/main.rs:8-38`. `transport/mod.rs:32-46` (`TransportRuntime`,
`BoundSocket`) and `transport/socket.rs` move to the core's Signal actor;
`transport/session.rs` (449 lines) becomes the generated Signal→Nexus crossing.
`core.rs:105-108` stays, but `core.rs:130` and `core.rs:160` stop being
`Message<OrdinaryQuery>`/`Message<MetaQuery>` and become `Message<Borne<Nexus, _>>`.
`store/mod.rs` stays as the Sema actor, minus the `signal_orchestrate` import at
`store/mod.rs:28`.

**`message`** — furthest. `src/bin/message_daemon.rs:4-13` takes a binary
configuration path argument, against `Vision/nexus.md:76` ("A Nexus starts with no
arguments"); delete it and the `from_configuration_path` constructor at
`daemon.rs:43-45`. `daemon.rs:55-79` (`run_async`, socket list, runtime assembly)
and `MessageRuntime` at `daemon.rs:82-126` are the core's job entirely; the
`engine.lock().await` at `daemon.rs:105` is the forbidden Signal→Sema edge and
disappears with it. `MessageEngine` becomes the Nexus actor's blocks.
`src/main.rs:3-9` is a CLI, not a Nexus, and moves to a client crate.

**`lojix`** — largest deletion. `src/daemon.rs` is 1293 lines of hand-rolled
metaNexus: `ListenerRole` at `daemon.rs:77-81`, the meta framing kinds at
`daemon.rs:37-62`, the request timeout at `daemon.rs:34`, all universal, all to
the core. `src/runtime_flow.rs` is already the Nexus actor
(`runtime_flow.rs:1-5`) and `src/runtime_model.rs` already the Sema actor
(`runtime_model.rs:1-5`) — the split the living wants is *already drawn there by
hand*. `src/adapters.rs` (`Lowerable`, `Raisable`, used at `daemon.rs:64`) is
exactly the crossing and becomes generated. `nexus/src/main.rs:7-20` shrinks to
the two-line call.

## 6. Where Forge fits

Per `flows/6cc91b/vision/forge.md:11-13`, Forge is the build language and build
manager, not a fourth actor: it is what dispatches these crates, and the living's
framing in `flows/6cc91b/vision/nexus.md:15` — "Forge essentially doing everything
that cargo used to do more efficiently because it's more integrated, with source
caching" — places it one level below this proposal, not inside it. The connection
is concrete and narrow: the core's kind guard is a *compile-time* check, so
whatever drives the compiler must know the three-crate-per-component shape
(core, generated ethos, component) and must not let a component's build reach a
crate its kind forbids — module privacy guards within a crate, but the crate
graph is Forge's to guard. Forge is itself a Nexus built on this core, so the
proof that the anatomy holds is that Forge is buildable as one; and its standard
objects mapping to Nix derivations (`forge.md:11`) are ordinary Sema-kind records
of that Nexus, with the native CriomOS sandbox side named separately
(`forge.md:13`). Nothing in sections 1-5 waits on Forge.

## 7. Open questions for the living

1. **Does the Nexus actor see Signal types at all, or only raised ones?**
   Today `orchestrate-nexus/src/core.rs:130` has the Nexus handle
   `signal_orchestrate::Query` directly. Strict reading of "All interaction ...
   has to go through the Nexus and then the Nexus ethos type file"
   (`nexus.md:25`) says the Nexus never names a Signal type: `Query::Lock(request)`
   would arrive as `Borne<Nexus, LockIntent>` after a generated crossing. That is
   stricter and costs one more generated type per query. Strict, or does the
   Nexus own the Signal enum as its own input?

2. **Is the Signal actor one actor or one per socket?**
   Every metaNexus today has exactly two tiers — `ListenerRole::{Ordinary, Owner}`
   at `message/src/daemon.rs:19-22` and `lojix/src/daemon.rs:77-81` — but
   `Vision/nexus.md:39` says a Nexus needing more access levels opens more
   sockets. Is `Signal` one kind with a socket tag, or is the meta surface its
   own kind (`Meta`) with its own crossing, so an ordinary session cannot
   construct a meta query *by type* rather than by match?

3. **Does the Nexus ethos root name the crossings, or infer them?**
   Concretely: given `Signal` declares `Lock.LockRequest` and `Sema` declares
   `StoredLock`, does the Nexus ethos file write the crossing explicitly
   (`Lock.LockIntent` then `LockIntent.StoredLock`), or does ethos-zero derive
   both from name agreement? Explicit is more text; inferred is the
   non-repetition rule of `Vision/ethos.md:24-26`.

4. **What happens to the fourth leg, effects?**
   `triad-runtime/src/reaction.rs:44` has `EffectCompleted(Effect)` and
   `runner.rs:55` has `run_effect` — lojix shells out to Nix through it. An
   effect is neither Signal, Nexus, nor Sema. Is it a fourth sealed kind
   (`Effect`, crossing only to and from `Nexus`), or does the Nexus actor run
   effects itself and thereby become the one actor permitted to block?

5. **Does a metaNexus have exactly one Sema actor?**
   `orchestrate-nexus/src/store/mod.rs:3-5` says "One process owns one Sema
   store" holding three families. If a future Nexus wants two stores with
   different durability, is that two Sema actors, or is it a split into two
   nexuses per `Vision/nexus.md:112-115`?

## Sources

- Living, today: `flows/6cc91b/vision/nexus.md:11-17`, `:19-29`;
  `flows/6cc91b/vision/rustLayering.md:7`; `flows/6cc91b/vision/forge.md:7-13`.
- Living, 2026-09-13: `flows/6cc91b/vision/nexus.md:3-9`;
  `flows/024bc7/vision/nexus.md:3-27`.
- Distilled: `Vision/nexus.md`, `Vision/sema.md`, `Vision/signal.md`,
  `Vision/ethos.md`.
- Code, read whole: `nexus/src/{lib,authority,configuration,relocation,situation}.rs`,
  `nexus/ARCHITECTURE.md`, `nexus/Cargo.toml`; `triad-runtime/src/{lib,role,reaction}.rs`,
  `triad-runtime/src/runner.rs:1-120`; `orchestrate/crates/orchestrate-nexus/src/{lib,core,main}.rs`,
  `.../src/store/mod.rs:1-80`, `.../src/transport/mod.rs:1-70`;
  `message/src/{main,daemon}.rs`, `message/src/bin/*.rs`; `lojix/nexus/src/main.rs`,
  `lojix/src/daemon.rs:1-90`, `lojix/src/{runtime_flow,runtime_model}.rs:1-60`;
  `ethos-zero/src/lib.rs:1-70`, `ethos-zero/README.md`,
  `ethos-zero/tests/generated/{capability-kinds,entry-sema}.rs`,
  `ethos-zero/fixtures/capability-kinds.ethos`; `sema-engine/src/lib.rs:1-89`;
  `signal-message/ethos/signal.ethos`, `signal-message/src/generated/signal.rs:1-70`.
- Method: direct read at `/git/github.com/LiGoldragon/` on 2026-09-14. No build
  was run; the type sketches in sections 2 and 3 are proposals, not compiled code.
