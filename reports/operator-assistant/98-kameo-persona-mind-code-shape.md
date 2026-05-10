# 98. Kameo shape for persona-mind

## 1. Scope

This is a report, not an implementation. I did not create a
`CameoTest` repository, did not modify `persona-mind`, and did not
revive the retired `persona-actor` / `workspace-actor` abstraction
names.

The question here is narrow:

> If `persona-mind` were rewritten from direct `ractor` to direct
> `kameo`, what would the code look like in practice right now?

The answer is: it would become more data-bearing at the actor type
level, with less framework marker boilerplate, but it would also be a
real runtime switch. It would invalidate the current Ractor-only guard
and needs an explicit decision before code changes land.

## 2. Sources Read

- `reports/designer/102-kameo-deep-dive.md` — recent Kameo research
  report. It covers Kameo 0.20.0, compares it to ractor, and explicitly
  refuses to revive `persona-actor` / `workspace-actor`.
- `reports/operator/103-actor-abstraction-drift-correction.md` —
  correction report retiring the invented actor abstraction names.
- `skills/actor-systems.md` — current workspace actor discipline:
  direct `ractor` is the active default; no second wrapper layer.
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` —
  current direct-ractor architecture.
- Current `persona-mind` actor files:
  `src/actors/root.rs`, `src/actors/dispatch.rs`,
  `src/actors/domain.rs`, `src/actors/store.rs`,
  `src/service.rs`, `src/actors/manifest.rs`, and
  `src/actors/trace.rs`.
- Primary Kameo sources:
  - `https://docs.rs/crate/kameo/latest` — latest docs.rs crate page;
    Kameo is 0.20.0.
  - `https://docs.rs/kameo/latest/kameo/actor/trait.Actor.html` —
    `Actor` trait.
  - `https://docs.rs/kameo/latest/kameo/actor/trait.Spawn.html` —
    spawn extension trait.
  - `https://docs.rs/kameo/latest/kameo/actor/struct.ActorRef.html` —
    `ask`, `tell`, lifecycle, IDs, stream attachment.
  - `https://docs.rs/kameo/latest/kameo/message/trait.Message.html` —
    per-message handler trait.
  - `https://docs.rs/kameo/latest/kameo/all.html` — current item list.
  - `https://github.com/tqwewe/kameo` — source repository / README.

One correction to carry forward: the designer report mentions a
separate Kameo Query trait. Current docs.rs for Kameo 0.20.0 lists
`message::Message` but not a `Query` trait. For `persona-mind`, read
paths should therefore be modeled as ordinary typed messages and proved
read-only by our trace/topology tests.

## 3. Current `persona-mind` Shape

Current `persona-mind` is direct `ractor`.

Each actor has:

- a private or crate-private behavior marker such as
  `StoreSupervisor`;
- a separate `State` struct carrying actor data;
- an `Arguments` struct;
- a `Message` enum containing all accepted messages;
- explicit `RpcReplyPort` fields in message variants;
- `ActorRef<module::Message>` references to child actors;
- `pre_start` returning `State`;
- `handle(&self, ..., message, state: &mut State)`.

The current store shape is representative:

```rust
pub(super) struct StoreSupervisor;

pub struct State {
    memory: MemoryState,
}

pub struct Arguments {
    pub store: StoreLocation,
}

pub enum Message {
    ApplyMemory {
        envelope: MindEnvelope,
        trace: ActorTrace,
        reply_port: RpcReplyPort<PipelineReply>,
    },
    ReadMemory {
        envelope: MindEnvelope,
        trace: ActorTrace,
        reply_port: RpcReplyPort<PipelineReply>,
    },
}

#[ractor::async_trait]
impl Actor for StoreSupervisor {
    type Msg = Message;
    type State = State;
    type Arguments = Arguments;

    async fn pre_start(
        &self,
        _myself: ActorRef<Self::Msg>,
        arguments: Arguments,
    ) -> Result<Self::State, ActorProcessingErr> {
        Ok(State::new(arguments.store))
    }

    async fn handle(
        &self,
        _myself: ActorRef<Self::Msg>,
        message: Message,
        state: &mut State,
    ) -> Result<(), ActorProcessingErr> {
        match message {
            Message::ApplyMemory { envelope, trace, reply_port } => {
                let _ = reply_port.send(state.apply_memory(envelope, trace));
            }
            Message::ReadMemory { envelope, trace, reply_port } => {
                let _ = reply_port.send(state.read_memory(envelope, trace));
            }
        }
        Ok(())
    }
}
```

This is legitimate ractor code, but the actor's noun is split across
two types: `StoreSupervisor` as framework marker and `State` as the
actual body.

## 4. Kameo's Load-Bearing Difference

Kameo collapses actor marker and state:

- `Actor::on_start(arguments, ActorRef<Self>) -> Self`;
- no associated `State`;
- lifecycle hooks and message handlers take `&mut self`;
- messages are separate types implemented through
  `impl Message<SpecificMessage> for SpecificActor`;
- `ActorRef<SpecificActor>` sends messages with `ask` / `tell`;
- replies are the `type Reply` associated with the message handler.

That means `persona-mind` actors would become data-bearing nouns:

```rust
pub struct StoreSupervisorActor {
    memory: MemoryState,
}

impl StoreSupervisorActor {
    pub fn from_store(store: StoreLocation) -> Self {
        Self {
            memory: MemoryState::open(store),
        }
    }

    fn apply_memory(&self, envelope: MindEnvelope, mut trace: ActorTrace) -> PipelineReply {
        trace.record(
            ActorKind::StoreSupervisorActor,
            TraceAction::MessageReceived,
        );
        WriteTrace::from_request(envelope.request()).record_into(&mut trace);

        let reply = self.memory.dispatch_envelope(envelope);

        trace.record(ActorKind::EventAppendActor, TraceAction::MessageReceived);
        trace.record(ActorKind::CommitActor, TraceAction::CommitCompleted);
        PipelineReply::new(reply, trace)
    }

    fn read_memory(&self, envelope: MindEnvelope, mut trace: ActorTrace) -> PipelineReply {
        trace.record(
            ActorKind::StoreSupervisorActor,
            TraceAction::MessageReceived,
        );
        trace.record(ActorKind::SemaReadActor, TraceAction::MessageReceived);

        let reply = self.memory.dispatch_envelope(envelope);

        PipelineReply::new(reply, trace)
    }
}

impl Actor for StoreSupervisorActor {
    type Args = Self;
    type Error = Infallible;

    async fn on_start(
        actor: Self::Args,
        _actor_reference: ActorRef<Self>,
    ) -> Result<Self, Self::Error> {
        Ok(actor)
    }
}
```

Message variants become message types:

```rust
pub struct ApplyMemory {
    pub envelope: MindEnvelope,
    pub trace: ActorTrace,
}

pub struct ReadMemory {
    pub envelope: MindEnvelope,
    pub trace: ActorTrace,
}

impl Message<ApplyMemory> for StoreSupervisorActor {
    type Reply = PipelineReply;

    async fn handle(
        &mut self,
        message: ApplyMemory,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.apply_memory(message.envelope, message.trace)
    }
}

impl Message<ReadMemory> for StoreSupervisorActor {
    type Reply = PipelineReply;

    async fn handle(
        &mut self,
        message: ReadMemory,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.read_memory(message.envelope, message.trace)
    }
}
```

That shape is closer to this workspace's Rust discipline: behavior
lives on the type carrying the data.

## 5. Dependency and Nix Shape

A Kameo switch would be a normal dependency switch, not a new component
repo and not a wrapper crate.

The dependency change would look approximately like:

```toml
[dependencies]
kameo = { version = "0.20", features = ["macros"] }
```

For production code I would use explicit `Actor` impls for core
supervisors, even if the macro remains available for low-risk leaf
actors. The explicit shape keeps lifecycle, restart, and startup
failure handling visible.

Nix would need the usual `Cargo.lock` update and `cargoHash` /
`outputHashes` refresh if the current crane setup detects dependency
changes. There is no special Kameo/Nix integration implied.

The current weird test would need a deliberate rewrite. It currently
contains a guard that forbids `kameo =` and `name = "kameo"` because
the approved runtime is direct ractor. If the runtime decision changes,
that guard should become a single-runtime guard instead:

```rust
#[test]
fn kameo_is_the_only_actor_library_boundary() {
    let forbidden_fragments = [
        ForbiddenFragment {
            text: "ractor =",
            reason: "old actor runtime dependency after Kameo switch",
        },
        ForbiddenFragment {
            text: "name = \"ractor\"",
            reason: "old actor runtime dependency after Kameo switch",
        },
        ForbiddenFragment {
            text: "persona-actor",
            reason: "invented actor abstraction name",
        },
        ForbiddenFragment {
            text: "workspace-actor",
            reason: "invented actor abstraction name",
        },
    ];

    // Same scan shape as the current weird test.
}
```

During an exploratory branch, the guard could be disabled in that branch
only. It should not be weakened on `main` without a runtime decision.

## 6. Runtime Facade Shape

Current ractor facade:

```rust
pub struct MindRuntime {
    root: MindRootHandle,
}
```

Kameo facade:

```rust
use kameo::actor::{ActorRef, Spawn};

pub struct MindRuntime {
    root: ActorRef<MindRootActor>,
}

impl MindRuntime {
    pub async fn start(store: StoreLocation) -> Result<Self> {
        let root = MindRootActor::spawn(MindRootArguments::new(store));
        root.wait_for_startup().await;
        Ok(Self { root })
    }

    pub async fn submit(&self, envelope: MindEnvelope) -> Result<MindRuntimeReply> {
        let root_reply = self
            .root
            .ask(SubmitEnvelope { envelope })
            .await
            .map_err(|error| Error::ActorCall(error.to_string()))?;

        Ok(MindRuntimeReply::from_root_reply(root_reply))
    }

    pub async fn manifest(&self) -> Result<ActorManifest> {
        self.root
            .ask(ReadManifest)
            .await
            .map_err(|error| Error::ActorCall(error.to_string()))
    }

    pub async fn stop(self) -> Result<()> {
        self.root
            .stop_gracefully()
            .await
            .map_err(|error| Error::ActorCall(error.to_string()))?;
        self.root.wait_for_shutdown().await;
        Ok(())
    }
}
```

The facade loses `MindRootHandle` as a ractor-specific wrapper. It may
still be worth keeping a handle type if we want to hide Kameo from the
public crate surface:

```rust
pub struct MindRootHandle {
    actor_reference: ActorRef<MindRootActor>,
}
```

That handle is not a new actor abstraction. It is a repo-local public
handle, the same pattern the current architecture already allows.

## 7. Root Actor Shape

The root becomes the data-bearing supervisor:

```rust
use kameo::actor::{Actor, ActorRef, Spawn};
use kameo::error::Infallible;
use kameo::message::{Context, Message};
use kameo::supervision::RestartPolicy;

pub struct MindRootActor {
    ingress: ActorRef<IngressSupervisorActor>,
    manifest: ActorManifest,
    runtime_topology: RuntimeTopology,
}

pub struct MindRootArguments {
    store: StoreLocation,
    runtime_identity: RuntimeIdentity,
}

pub struct SubmitEnvelope {
    pub envelope: MindEnvelope,
}

pub struct ReadManifest;

#[derive(Debug, Clone, kameo::Reply)]
pub struct RootReply {
    reply: Option<MindReply>,
    trace: ActorTrace,
}

impl Actor for MindRootActor {
    type Args = MindRootArguments;
    type Error = Infallible;

    async fn on_start(
        arguments: Self::Args,
        actor_reference: ActorRef<Self>,
    ) -> Result<Self, Self::Error> {
        let manifest = ActorManifest::persona_mind_phase_one();
        let mut runtime_topology = RuntimeTopology::new(arguments.runtime_identity.clone());

        let store = StoreSupervisorActor::supervise(
            &actor_reference,
            StoreSupervisorActor::from_store(arguments.store.clone()),
        )
        .restart_policy(RestartPolicy::Never)
        .spawn()
        .await;
        runtime_topology.record(
            ActorKind::MindRootActor,
            ActorKind::StoreSupervisorActor,
            store.id(),
        );

        let reply = ReplySupervisorActor::supervise(
            &actor_reference,
            ReplySupervisorActor::new(),
        )
        .restart_policy(RestartPolicy::Transient)
        .spawn()
        .await;

        let view = ViewSupervisorActor::supervise(
            &actor_reference,
            ViewSupervisorActor::new(store.clone()),
        )
        .restart_policy(RestartPolicy::Transient)
        .spawn()
        .await;

        let domain = DomainSupervisorActor::supervise(
            &actor_reference,
            DomainSupervisorActor::new(store),
        )
        .restart_policy(RestartPolicy::Transient)
        .spawn()
        .await;

        let dispatch = DispatchSupervisorActor::supervise(
            &actor_reference,
            DispatchSupervisorActor::new(domain, view, reply),
        )
        .restart_policy(RestartPolicy::Transient)
        .spawn()
        .await;

        let ingress = IngressSupervisorActor::supervise(
            &actor_reference,
            IngressSupervisorActor::new(dispatch),
        )
        .restart_policy(RestartPolicy::Transient)
        .spawn()
        .await;

        Ok(Self {
            ingress,
            manifest,
            runtime_topology,
        })
    }
}

impl Message<SubmitEnvelope> for MindRootActor {
    type Reply = RootReply;

    async fn handle(
        &mut self,
        message: SubmitEnvelope,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        let mut trace = ActorTrace::new();
        trace.record(ActorKind::MindRootActor, TraceAction::MessageReceived);

        let pipeline = self
            .ingress
            .ask(AcceptEnvelope {
                envelope: message.envelope,
                trace,
            })
            .await;

        match pipeline {
            Ok(mut pipeline_reply) => {
                pipeline_reply
                    .trace
                    .record(ActorKind::MindRootActor, TraceAction::MessageReplied);
                RootReply::new(pipeline_reply.reply, pipeline_reply.trace)
            }
            Err(_error) => {
                let mut trace = ActorTrace::new();
                trace.record(ActorKind::MindRootActor, TraceAction::MessageReceived);
                trace.record(ActorKind::ErrorShapeActor, TraceAction::MessageReplied);
                RootReply::new(None, trace)
            }
        }
    }
}

impl Message<ReadManifest> for MindRootActor {
    type Reply = ActorManifest;

    async fn handle(
        &mut self,
        _message: ReadManifest,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.manifest.clone()
    }
}
```

This is the main readability improvement: root supervision is now a
single data-bearing type. There is no separate `MindRoot` marker +
`State` split.

Two details need a compile spike:

- the exact return and error shape of `SupervisedActorBuilder::spawn`;
- whether every custom reply type should derive `kameo::Reply` or be
  wrapped in an already-supported reply type.

Those are mechanical API details, not architecture blockers.

## 8. Dispatch Actor Shape

Current dispatch uses one enum message. In Kameo it becomes one message
type:

```rust
pub struct DispatchSupervisorActor {
    domain: ActorRef<DomainSupervisorActor>,
    view: ActorRef<ViewSupervisorActor>,
    reply: ActorRef<ReplySupervisorActor>,
}

pub struct RouteEnvelope {
    pub envelope: MindEnvelope,
    pub trace: ActorTrace,
}

impl DispatchSupervisorActor {
    pub fn new(
        domain: ActorRef<DomainSupervisorActor>,
        view: ActorRef<ViewSupervisorActor>,
        reply: ActorRef<ReplySupervisorActor>,
    ) -> Self {
        Self {
            domain,
            view,
            reply,
        }
    }

    async fn route(
        &self,
        envelope: MindEnvelope,
        mut trace: ActorTrace,
    ) -> Result<PipelineReply> {
        trace.record(
            ActorKind::DispatchSupervisorActor,
            TraceAction::MessageReceived,
        );
        trace.record(
            ActorKind::RequestDispatchActor,
            TraceAction::MessageReceived,
        );

        let pipeline = match envelope.request() {
            MindRequest::Open(_)
            | MindRequest::AddNote(_)
            | MindRequest::Link(_)
            | MindRequest::ChangeStatus(_)
            | MindRequest::AddAlias(_) => {
                trace.record(ActorKind::MemoryFlowActor, TraceAction::MessageReceived);
                self.domain
                    .ask(ApplyMemory { envelope, trace })
                    .await
                    .map_err(|error| Error::ActorCall(error.to_string()))?
            }
            MindRequest::Query(_) => {
                trace.record(ActorKind::QueryFlowActor, TraceAction::MessageReceived);
                self.view
                    .ask(ReadMemory { envelope, trace })
                    .await
                    .map_err(|error| Error::ActorCall(error.to_string()))?
            }
            MindRequest::RoleClaim(_) => {
                self.unsupported(trace, ActorKind::ClaimFlowActor)
            }
            MindRequest::RoleHandoff(_) => {
                self.unsupported(trace, ActorKind::HandoffFlowActor)
            }
            MindRequest::ActivitySubmission(_) | MindRequest::ActivityQuery(_) => {
                self.unsupported(trace, ActorKind::ActivityFlowActor)
            }
            MindRequest::RoleRelease(_) | MindRequest::RoleObservation(_) => {
                self.unsupported(trace, ActorKind::ClaimFlowActor)
            }
        };

        self.reply
            .ask(ShapeReply {
                reply: pipeline.reply,
                trace: pipeline.trace,
            })
            .await
            .map_err(|error| Error::ActorCall(error.to_string()))
    }

    fn unsupported(&self, mut trace: ActorTrace, actor: ActorKind) -> PipelineReply {
        trace.record(actor, TraceAction::MessageReceived);
        trace.record(ActorKind::ErrorShapeActor, TraceAction::MessageReplied);
        PipelineReply::new(None, trace)
    }
}

impl Actor for DispatchSupervisorActor {
    type Args = Self;
    type Error = Infallible;

    async fn on_start(
        actor: Self::Args,
        _actor_reference: ActorRef<Self>,
    ) -> Result<Self, Self::Error> {
        Ok(actor)
    }
}

impl Message<RouteEnvelope> for DispatchSupervisorActor {
    type Reply = PipelineReply;

    async fn handle(
        &mut self,
        message: RouteEnvelope,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.route(message.envelope, message.trace)
            .await
            .unwrap_or_else(|_error| PipelineReply::new(None, ActorTrace::new()))
    }
}
```

Kameo does not remove the need for our own trace discipline. It just
makes actor state placement cleaner.

## 9. Store, Sema, and Restart Policy

Store is the risky actor to restart.

Today `StoreSupervisorActor` owns in-memory `MemoryState`. Until
`persona-sema` is the durable substrate, restarting that actor can lose
state. In Kameo, the tempting declarative restart policy should be
restrained:

```rust
let store = StoreSupervisorActor::supervise(
    &actor_reference,
    StoreSupervisorActor::from_store(arguments.store.clone()),
)
.restart_policy(RestartPolicy::Never)
.spawn()
.await;
```

After `persona-sema` owns durable tables, store restart can become
transient or permanent because `on_start` can reopen `mind.redb` and
reconstruct views:

```rust
impl Actor for StoreSupervisorActor {
    type Args = StoreSupervisorArguments;
    type Error = Infallible;

    async fn on_start(
        arguments: Self::Args,
        _actor_reference: ActorRef<Self>,
    ) -> Result<Self, Self::Error> {
        Ok(Self {
            memory: MemoryState::open(arguments.store),
        })
    }
}
```

Kameo makes restart policy easier to express. It does not make restart
semantics automatically safe.

## 10. Query Path Under Current Kameo 0.20.0

Current docs.rs Kameo 0.20.0 does not list a separate `Query` trait.
Read paths should be plain message handlers:

```rust
pub struct ReadMemory {
    pub envelope: MindEnvelope,
    pub trace: ActorTrace,
}

impl Message<ReadMemory> for ViewSupervisorActor {
    type Reply = PipelineReply;

    async fn handle(
        &mut self,
        message: ReadMemory,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        self.read_memory(message.envelope, message.trace)
            .await
            .unwrap_or_else(|_error| PipelineReply::new(None, ActorTrace::new()))
    }
}
```

The existing test remains the important proof:

- query trace includes `ViewSupervisorActor`;
- query trace includes `SemaReadActor`;
- query trace excludes `SemaWriterActor`;
- query trace excludes `CommitActor`.

If future Kameo reintroduces or exposes a read-only query trait, it can
be evaluated then. The report should not assume that API exists today.

## 11. Topology and Runtime Names

Kameo actor names are static type names by default. Current
`persona-mind` ractor code uses per-runtime prefixes to avoid global
name collisions in parallel tests.

With Kameo, do not depend on global registration for local topology.
Use owned `ActorRef` fields and `ActorRef::id()` for runtime witnesses:

```rust
#[derive(Debug, Clone)]
pub struct RuntimeTopology {
    runtime_identity: RuntimeIdentity,
    children: Vec<RuntimeChild>,
}

#[derive(Debug, Clone)]
pub struct RuntimeChild {
    parent: ActorKind,
    child: ActorKind,
    actor_id: kameo::actor::ActorId,
}

impl RuntimeTopology {
    pub fn new(runtime_identity: RuntimeIdentity) -> Self {
        Self {
            runtime_identity,
            children: Vec::new(),
        }
    }

    pub fn record(
        &mut self,
        parent: ActorKind,
        child: ActorKind,
        actor_id: kameo::actor::ActorId,
    ) {
        self.children.push(RuntimeChild {
            parent,
            child,
            actor_id,
        });
    }
}
```

`ActorManifest` remains the static architecture witness. `RuntimeTopology`
would be an optional runtime witness for tests that need to prove actual
spawned children and parallel-runtime isolation.

## 12. Test Shape

The existing test suite ports cleanly in concept.

Topology test:

```rust
#[tokio::test]
async fn topology_manifest_names_required_actor_planes() {
    let runtime = MindRuntime::start(StoreLocation::new("mind.redb"))
        .await
        .expect("kameo runtime starts");

    let manifest = runtime.manifest().await.expect("manifest is available");

    assert!(manifest.contains(ActorKind::MindRootActor));
    assert!(manifest.contains(ActorKind::StoreSupervisorActor));
    assert!(manifest.contains_edge(
        ActorKind::MindRootActor,
        ActorKind::StoreSupervisorActor,
    ));

    runtime.stop().await.expect("kameo runtime stops");
}
```

Write-path test:

```rust
#[tokio::test]
async fn open_item_runs_through_kameo_write_path() {
    let runtime = MindRuntime::start(StoreLocation::new("mind.redb"))
        .await
        .expect("kameo runtime starts");

    let response = runtime
        .submit(MindEnvelope::new(
            ActorName::new("operator-assistant"),
            MindRequest::Open(Opening {
                kind: Kind::Task,
                priority: Priority::High,
                title: Title::new("Implement kameo-backed mind"),
                body: Body::new("Kameo actor path"),
            }),
        ))
        .await
        .expect("submit succeeds");

    assert!(response.trace().contains_ordered(&[
        ActorKind::MindRootActor,
        ActorKind::IngressSupervisorActor,
        ActorKind::DispatchSupervisorActor,
        ActorKind::MemoryFlowActor,
        ActorKind::DomainSupervisorActor,
        ActorKind::StoreSupervisorActor,
        ActorKind::SemaWriterActor,
        ActorKind::CommitActor,
        ActorKind::ReplySupervisorActor,
    ]));

    runtime.stop().await.expect("kameo runtime stops");
}
```

Weird guard update:

```rust
#[test]
fn raw_kameo_spawn_cannot_escape_mind_root() {
    let violations = SourceTree::new()
        .source_files()
        .into_iter()
        .filter(|file| file.relative_name() != "src/actors/root.rs")
        .flat_map(|file| {
            file.violations_for(&ForbiddenFragment {
                text: "::spawn(",
                reason: "raw Kameo spawn outside MindRootActor",
            })
        })
        .collect::<Vec<_>>();

    assert!(
        violations.is_empty(),
        "raw Kameo spawn violations:\n{}",
        violations
            .iter()
            .map(SourceViolation::summary)
            .collect::<Vec<_>>()
            .join("\n")
    );
}
```

That test would need a whitelist for `MindRuntime::start` if the text
scan is too broad. A syntax-aware scan would be better once the code
settles.

## 13. What Gets Better

Kameo directly addresses the awkward part of current direct-ractor code:

| Current ractor shape | Kameo shape |
|---|---|
| ZST behavior marker plus separate `State` | one actor struct carrying state |
| `Message` enum per actor | message type per operation |
| explicit `RpcReplyPort` in every message | `type Reply` per message impl |
| child refs are `ActorRef<Message>` | child refs are `ActorRef<ActorType>` |
| dynamic ractor spawn names | static type names plus `ActorId` runtime witness |
| supervision by linked spawn and manual policy | explicit restart policy builder |

The biggest benefit is not fewer lines. It is that the noun carrying
behavior is the same noun carrying state. That aligns with
`skills/rust-discipline.md` without treating ractor's framework shape as
a design failure.

## 14. What Gets Worse or Remains Unknown

1. **It is a real runtime switch.** Current architecture, docs, and weird
   tests say direct ractor. Changing that requires an explicit decision.
2. **The current Kameo API should be compiled in a spike.** The code in
   this report is shaped from docs, but exact builder return types and
   custom reply derive bounds need compiler verification.
3. **Read-only queries are not framework-enforced in current docs.** We
   still need trace tests for read/write separation.
4. **Store restarts are unsafe until sema persistence lands.** Kameo's
   restart policies are useful only once the actor can reconstruct state.
5. **Topology export remains our responsibility.** Kameo exposes
   `ActorId`, but `ActorManifest` and trace witnesses are still local
   architecture-test machinery.
6. **Macros are a tradeoff.** `#[derive(Actor)]` and `#[derive(Reply)]`
   reduce boilerplate. For supervisors, explicit impls are clearer.
7. **The existing Ractor-only guard would have to change.** This is not a
   quick dependency swap on `main`.

## 15. Minimal Spike Plan If Approved

Do not start by porting every actor.

1. Create a branch in `persona-mind`.
2. Replace `ractor` with `kameo` in `Cargo.toml`.
3. Rewrite only:
   - `src/service.rs`;
   - `src/actors/root.rs`;
   - `src/actors/store.rs`;
   - `src/actors/reply.rs`;
   - the minimum ingress/dispatch/domain/view path needed for one
     `MindRequest::Open`.
4. Keep `MemoryState`, `ActorManifest`, `ActorTrace`, and contract types
   unchanged.
5. Rewrite the weird actor-library guard from Ractor-only to Kameo-only
   in that branch.
6. Make these checks pass:
   - `nix develop -c cargo fmt`;
   - `nix develop -c cargo clippy --all-targets -- -D warnings`;
   - `nix develop -c cargo test`;
   - `nix build .#checks.x86_64-linux.weird-actor-truth -L`;
   - `nix flake check -L`.

The spike should answer only one question: does Kameo make the
`persona-mind` actor code materially clearer without losing topology,
trace, and no-blocking proofs?

## 16. Bottom Line

Kameo is real and worth evaluating. The retired wrapper-library names are
not.

If Kameo were used, `persona-mind` would look like a set of data-bearing
actor structs with per-message impls. The code would likely be cleaner
than ractor for small actor-heavy planes because Kameo's native shape
puts state and behavior on the same type. The cost is a full runtime
decision, a guard rewrite, and a compile-tested migration spike.

My recommendation is not to change `main` yet. The useful next step, if
the user wants evidence, is a short-lived `persona-mind` branch that ports
the existing `Open` vertical slice to Kameo and compares the diff against
the current direct-ractor implementation.
