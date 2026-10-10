# Actor Library and Nexus Skill Review

Design session `15b67974`, 2026-08-21. Psyche direction in
`psyche/Vision/actorLibrary.md`.

## Part 1: The actor library in use

### Identity

The actor library is **kameo**, used via an organization fork at
`github.com/LiGoldragon/kameo` tracking upstream `tqwewe/kameo`.
The fork carries custom commits (lifecycle control, weak shutdown
helpers) on top of upstream version 0.20.0. The fork workspace
contains three crates: `kameo`, `kameo_macros`, `kameo_actors`.

A dedicated testing bed exists at `kameo-testing`, described as the
"source for the workspace's Kameo skill," depending on the fork via
git (branch `main`) with a `[patch.crates-io]` override.

### Dependency footprint

21 repos depend on kameo. All use direct `[dependencies]` entries
(no workspace-level dependencies) with a `[patch.crates-io]` redirect
to the fork.

**Branch `main` (14 repos):** terminal, introspect, harness, chroma,
terminal-cell, mentci, criome, system, repository-ledger, clavifaber,
persona, router, upgrade, mind.

**Pinned rev `f491b45` (4 repos):** triad-runtime, ethos-engine,
sema-storage, logos-engine. The pinned commit is "fix lifecycle fork
after upstream rebase."

**Feature branch `persona-lifecycle-terminal-outcome` (1 repo):**
persona-spirit.

**Upstream crates.io `"0.20"` (1 repo):** lojix.

One repo uses a different actor framework: **hexis** depends on
`ractor 0.15` with `async-trait` feature. No repos use actix, xactor,
stakker, or bastion. No homegrown actor crate exists; the fork of
kameo is the closest thing.

### Actor definitions

Actors are structs implementing `impl Actor for T`. All use
`type Error = Infallible` (one exception: `RecordStore` in
persona-spirit uses `crate::Error`).

**persona** (8 actors, `type Args = Self`):
`EngineManager` (src/manager.rs:262),
`ManagerStore` (src/manager_store.rs:904),
`EngineSupervisor` (src/supervisor.rs:278),
`DirectProcessLauncher` (src/direct_process.rs:1019),
`ComponentCommandResolver` (src/launch/resolver.rs:50),
`ComponentSocketReadiness` (src/readiness.rs:105),
`ComponentSupervisionReadiness` (src/supervision_readiness.rs:180),
`ComponentUnitManager` (src/unit.rs:47).

**persona-spirit** (11+ actors, `type Args = Arguments`):
`SpiritRoot` (src/actors/root.rs:625),
`DispatchPhase` (src/actors/dispatch.rs:701),
`RecordStore` (src/actors/store.rs:241),
`MetaPlane` (src/actors/meta.rs:107),
`ClockPlane` (src/actors/clock.rs:121),
`ClassifierPlane` (src/actors/classifier.rs:68),
`NotaDecoder` (src/actors/decoder.rs:50),
`ReplyShaper` (src/actors/reply.rs:148),
`ReplyTextEncoder` (src/actors/reply.rs:160),
`PolicyPlane` (src/actors/policy.rs:~107),
`SubscriptionPlane` (src/actors/subscription.rs:~164),
`IngressPhase` (src/actors/ingress.rs),
`StatePlane` (src/actors/state.rs).

### Message and reply patterns

Messages are plain structs. `Message` trait is implemented manually
via `impl Message<MessageType> for ActorType`. No derive macro for
messages; the derive macro is used only for replies.

**Reply patterns diverge between repos:**

- persona: most handlers return `Result<T>`, relying on kameo's
  blanket `Reply` impl. One manual `impl kameo::Reply` for
  `LauncherSnapshot` (src/direct_process.rs:138-154).
- persona-spirit: reply types use `#[derive(kameo::Reply)]`
  (e.g. `RootTextReply`, `PipelineReply`, `ClassificationResult`).
  Handlers return `Result<DeriveReplyType>`.

**Ask pattern** (both repos): `actor_ref.ask(SomeMessage).await`
with match arms for `Ok(value)`, `Err(SendError::HandlerError(..))`,
and `Err(error)` (infrastructure failure).

### Spawning and runtime

Both repos run on **tokio multi-thread runtime**.

**persona:** direct `Self::spawn(Self::new(...))` followed by
`reference.wait_for_startup().await`
(e.g. src/manager.rs:89-92). `ManagerStore` uses
`spawn_in_thread` for blocking I/O (src/manager_store.rs:691).
Child actors spawned inline in constructors without supervision
links (src/supervisor.rs:47-54).

**persona-spirit:** supervised spawning via
`ChildActor::supervise(&parent_ref, args).spawn().await`,
all children linked to `SpiritRoot` in `on_start()`
(src/actors/root.rs:629-712). `RecordStore` uses
`spawn_in_thread()` for blocking I/O (src/actors/root.rs:639).
Also provides `submit_text_blocking` with its own 2-thread runtime
(src/actors/root.rs:600-604).

### Supervision and lifecycle

**persona:** no kameo supervision links. Lifecycle is manual:
`EngineManager::on_stop()` calls `stop_gracefully().await` +
`wait_for_shutdown().await` on children (src/manager.rs:273-282).
`ManagerStore::on_stop()` closes storage tables
(src/manager_store.rs:919-926).

**persona-spirit:** full kameo supervision tree. All actors are
supervised children of `SpiritRoot`. Graceful shutdown via
`stop_gracefully().await` + `wait_for_shutdown().await` on the
root (src/actors/root.rs:144-150).

### Wrapper layers and conventions

**ActorTrace** (persona-spirit, src/actors/trace.rs:74-125): a
`Vec<TraceEvent>` threaded through every message and reply,
recording `MessageReceived` / `MessageReplied` per actor. Provides
observability of exact message paths.

**PipelineReply / FramePipelineReply** (persona-spirit,
src/actors/pipeline.rs:7-19): reply wrappers carrying domain reply
plus `ActorTrace`, with `into_parts()`.

**SpiritActorRuntime** (persona-spirit, src/actors/root.rs:523-623):
wraps the `SpiritRoot` actor ref, providing a typed non-actor-aware
public API (`submit_text`, `submit_request`), hiding `.ask()`
machinery.

**PersonaEngine** (persona, src/daemon.rs:47-51): wraps the
`EngineManager` actor ref with `PersonaFrameCodec` and optional
supervisor ref; provides `serve_connection` translating wire frames
into `.ask()` calls.

**ComponentDaemon trait** (persona, src/daemon.rs:133-159):
generated trait providing `build_runtime` (actor spawning) and
`handle_working_connection` (driving `.ask()` per connection) hooks.

### Arc<Mutex> observations in production source

**persona** -- one occurrence:
`type StopHandoff = Arc<Mutex<Option<oneshot::Sender<StopComponentReceipt>>>>`
(src/direct_process.rs:202). The doc comment at lines 191-201
explicitly states this is coordination between a single actor
(`DirectProcessLauncher`) and its own detached watcher task, not
shared state between two actors. The mutex is held briefly.

**persona-spirit** -- one occurrence:
`trace: Arc<Mutex<ActorTrace>>` in `SharedTrace`
(src/actors/dispatch.rs:62). Used within a single actor's
(`DispatchPhase`) internal engine state; not shared between distinct
actors.

Both occurrences are intra-actor coordination, not inter-actor shared
state.

### The grep-based test

`persona/tests/actor_discipline_truth.rs` (109 lines) contains two
tests. `actor_source_does_not_share_locks_between_actors` (line 42)
scans every `.rs` file under `src/` for `Arc<Mutex`, `Arc < Mutex`,
and `RwLock` patterns, explicitly exempting the `StopHandoff` line.
The header doc comment references a skill document at
`~/primary/skills/actor-systems.md`. The psyche's direction is to
review the actor library instead of relying on this approach.

## Part 2: Nexus skill documentation of the actor library

### What the nexus skill says

The nexus skill (`nexus.md`) and its rationale (`nexus-rationale.md`)
at `/git/github.com/LiGoldragon/Curriculum/skills/` do not document
the actor library. The word "actor" appears once, in a negative
context: wire type repos have "no runtime, no actors, no async
machinery" (nexus.md, wire type repos section, line 72). This
describes what wire type repos exclude, not how actors are used.

The skills cover: daemon structure, wire contracts (rkyv binary,
signal), socket topology (ordinary + meta), CLI shape, trait
discipline, identity, inter-nexus topology, and the rationale for
each design choice. The trait discipline section is thorough
(traits first, no free functions, no zero-sized-type namespaces).

### What the nexus skill does not say

The following aspects of actor usage witnessed in the codebase have
no corresponding documentation in the nexus skill:

1. **Actor library identity**: kameo is not named. The fork, its
   relationship to upstream, and the version are not mentioned.

2. **Actor definition conventions**: the `impl Actor` pattern,
   `type Args`, `type Error = Infallible` convention, and the
   distinction between `Args = Self` (persona) vs `Args = Arguments`
   (persona-spirit) are not documented.

3. **Message definition pattern**: manual `impl Message<M> for A`
   without derive macros, message naming conventions, and the
   ask/reply contract are not covered.

4. **Reply patterns**: the split between `Result<T>` returns and
   `#[derive(kameo::Reply)]` types is not documented.

5. **Spawning conventions**: `spawn` vs `spawn_in_thread`, the
   `wait_for_startup` pattern, and when to use each are absent.

6. **Supervision model**: kameo's `supervise()` API, supervision
   trees, the difference between persona's manual lifecycle and
   persona-spirit's supervised tree are not documented.

7. **Actor discipline**: what constitutes a breach (e.g.
   `Arc<Mutex>` shared between actors vs. within one actor), where
   the boundary lies, and how exemptions are noted are not in the
   skill.

8. **Wrapper layer conventions**: `ActorTrace`, `SpiritActorRuntime`,
   `PipelineReply`, `PersonaEngine` -- these recurring patterns built
   on top of kameo have no skill documentation.

9. **Runtime requirements**: tokio multi-thread, the relationship
   between the actor runtime and the daemon's event loop, are not
   specified.

### Divergences between skill text and witnessed usage

The nexus skill's trait discipline section says "every method call
lives in a trait; an inherent method is a trait not yet extracted."
The witnessed actor code uses inherent methods extensively (e.g.
`EngineManager::start()` at src/manager.rs:85, `SpiritRoot::start()`
at src/actors/root.rs:114). Whether these are considered traits not
yet extracted, or whether actor construction methods are a recognized
exception, is not stated in the skill.

The nexus skill says "no free functions" except `fn main()`. The
witnessed code in both repos follows this; actor modules are
struct-and-trait organized.

### Summary of coverage

The nexus skill is thorough on wire contracts, daemon shape, trait
discipline, and inter-nexus topology. It is silent on the actor
concurrency model that runs inside the daemon. The entire actor layer
-- library identity, definition patterns, message contracts,
supervision, spawning, discipline boundaries, and wrapper conventions
-- is undocumented in the skill.

## Unknowns

- Whether the 4 repos pinned to rev `f491b45` are intentionally
  behind `main` or awaiting a coordinated update.
- Whether hexis's use of `ractor` instead of kameo is intentional
  divergence or a legacy state.
- Whether the `~/primary/skills/actor-systems.md` referenced by the
  grep test exists or existed; it was not found in the current skill
  tree.
- The full actor inventory across all 21 kameo-dependent repos (this
  review witnessed persona and persona-spirit in detail; the others
  were checked for dependency only).
