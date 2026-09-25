# Nexus anatomy: a deep dive

Date: 2026-09-25. A read-only subflow of Psyche Medium e51411. It answers the living's request for "the anatomy, the syntax, the structure, and the geometry" of the Nexus components "from an ethos point of view". Every quote from the living is marked with its source. Datom lines marked *witnessed* appear in a README, skill or test. Lines marked *constructed* I built by hand from the ethos, and nothing has run them. Contract text is from the revisions the deployed components pin (Flow 0.7.0 pins signal-flow `ab70332` and meta-signal-flow `a34bc65`; Message pins signal-message `7f2fc2d`). Other contracts are from local checkouts dated 2026-09-11 to 2026-09-21.

## 1. What a Nexus is: the shared anatomy

> "Nexus is our word for the style of component that speaks signal and uses a similar database." (Vision/nexus.md, distilled; sources e06e4c07, 01a03d6e, 564f55, fe34eb and others)

> "the ethos code can live with the component. like all components (component + 2 signal repos)" (psyche, typed, 2026-08-11, flows/012fbf07/vision/threeStacks.md)

Each Nexus has the same five parts:

| Part | Name | Carries |
|---|---|---|
| Body | `<x>` repo, binary `<x>-nexus` | Nexus Core (Kameo actors), traits, logic |
| Ordinary contract | `signal-<x>` | domain vocabulary for any authenticated peer |
| Meta contract | `meta-signal-<x>` | Configure and privileged operations; "never optional" |
| Clients | `<x>`, and a meta client usually named `<x>-meta` (Spirit's is `meta-spirit`; Message also ships `meta-message`) | one inline Datom in, one Datom out; text stops here |
| Memory | `<x>.sema` via sema-engine | policy and working state in one store |

The syntax, from Ethos. A Signal file is a sweet form with four sibling sections: imports, queries, responses, types. `Name.Type` is an alias, `Name.{ }` a struct (positional; each field is named after its type), and `Name.[ ]` an enum. A small complete example is Orchestrate's (signal-system's ordinary contract is smaller, 33 lines to 47):

```
Signal
[]
[ Configure.OrchestrateNexusConfiguration  Lock.LockRequest  Release.LockId  Observe.ObserveSelection ]
[ ConfigurationAccepted.ConfigurationReceipt  ConfigurationRefused.ConfigurationRejection
  Locked.Lock  Released.Lock  Observed.Observation  LockRejected.LockRejection  ReleaseRejected.ReleaseRejection ]
[ ... LockRequest.{ LockName FlowId Vector<LockPath> LockReason }
  Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }
  LockRejection.[ DuplicateName.Lock  PathOverlap.LockOverlap ]  Observation.[ Locks.Vector<Lock> ] ]
```

The grammar has these rules. A query is a verb (`Lock`, `Deploy`, `Send`). Its reply is the past tense (`Locked`, `Deployed`, `Sent`). A refusal names itself (`LockRejected`) and carries a closed enum of reasons, never a string. A meta contract imports the ordinary types it shares by identity (`signal_orchestrate:[ OrchestrateNexusConfiguration ConfigurationReceipt ]`), so a meta edge extends the ordinary vocabulary and never duplicates it.

Wire and store: "Signal is the messaging layer: fully binary, portable rkyv ... nothing on the wire labeling itself" (Vision/signal.md). Frames are a 4-byte big-endian length followed by one rkyv archive (the `signal` crate). "The textual form is datom; a CLI actualizes it and sends signal; a Nexus never textualizes" (Vision/signal.md). Sema: "Sema is the database engine of a Nexus ... It matters more than nexus, because operational editing should yield the migration with the edit" (Vision/sema.md).

## 2. The components

### 2.1 Flow Nexus (`flow`, `signal-flow`, `meta-signal-flow`)

Purpose:
> "The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt." (Vision/flowNexus.md)

> "It has to have a way to compose the prompts: the first prompt and eventually a way to compose the system prompt" (psyche, typed, 2026-09-23, flows/836818/vision/flowNexus.md)

> "the flow kind of personifies more like the field aspect" (psyche, flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md)

Ordinary queries: `Start.StartRequest Restart.RestartRequest ResolveRecipient.RecipientResolutionRequest Send.SendRequest Stop.StopRequest List.ListRequest`.

Replies: `Started LaunchPending StartAmbiguous Restarted RecipientResolved.FlowNode Sent.SendOutcome Stopped.FlowId Listed.FlowList`, plus six `*Rejected` enums.

Core records:
- `FlowAspect.[ Psyche Mind Field ]`
- `PowerLevel.[ High Medium Low UltraLow ]`
- `LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }`
- `FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle }`
- `FlowLifecycle.[ Pending Active Stopped ]`
- `LaunchAttemptPhase.[ Reserved NativeLaunchIntentRecorded NativeBound RegistrationAcknowledged PromptIntentRecorded PromptObserved PromptAmbiguous ]`. This is a write-ahead state machine written into the type.

Meta queries: `Configure.ConfigureRequest ConsumeReset.ResetRequest RegisterFlow.FlowNode MetaBindExisting.MetaBindExisting`. `FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }` is used for importing existing seats. `FlowBindingRefusalReason.[ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch ]`.

Datom examples:
- Request, *witnessed* (flow README): `flow 'Send.{ 00f95a «continue with the implementation» }'`
- Reply, *constructed*: `Sent.Presented.{ 00f95a w1:p2 flow-marker-7 1758790000000 }`
- Reply, *witnessed* (flow tests): `RecipientResolved.{ da1e3f da1e3f9d-full Claude Unavailable Available.{ messaging-build recipient w1:p2 term-current } { da1e3f da1e3f9d-full unavailable } Active }`

- **Store:** FlowStore in Sema (`FLOW_NEXUS_STORE`), holding durable Flow rows and launch attempts.
- **Callers:** every flow (self-restart), Field and Psyche seats (Start), and Message Nexus (`ResolveRecipient`).
- **Depends on:** Herdr panes, the Codex app-server (WebSocket JSON-RPC, outside the Signal boundary), Claude `state.json` and daemon sockets.

### 2.2 Message Nexus (`message`, `signal-message`, `meta-signal-message`)

Purpose:
> "The message body is a datom that lands in the recipient's prompt as a datom-formatted object. There is no envelope around it." (Vision/messaging.md)

> "The message highly depends on flow and probably many things will then depend on message." (psyche, typed, 2026-09-23, flows/836818/vision/nexusAnatomy.md)

The ordinary contract has 13 queries: `Submit SubmitStamped QueryInbox AssignAgentIdentity BindAgentEndpoint QueryAgentRegistry QueryThread SubscribeThread QueryThreads FlowDeliver FlowAnnounceIdle Deliver QueryDeliveryReceipts`. The newest core types:
- `ClusterMessage.[ Relay.ClusterRelay Peer.PeerEnvelope ]`
- `DeliveryRequest.{ SourceEventIdentifier ClusterMessage TargetFlows }`
- `ReceiptKind.[ Accepted TranscriptWitnessed Parked FileOnly ]`
- `DeliveryReport.{ SourceEventIdentifier RecipientReceipts }`
- `DeliveryReceiptState.[ Recorded.DeliveryReceiptRecord Missing.FlowIdentifier ]`

The meta contract is small: `Configure.MessageDaemonConfiguration`, answered by `ConfigurationApplied`, `ConfigurationRefused` or `OperationUnimplemented`.

Datom examples:
- Request, *witnessed* (message README): `message 'QueryDeliveryReceipts.{ event-42 [ target-a target-b ] }'`
- Reply, *constructed*: `DeliveryReceiptListing.{ event-42 [ Recorded.{ target-a Accepted false } Missing.target-b ] }`

- **Store:** `messenger.sema`, holding the ledger, inbox, thread index, agent registry, delivery outbox and receipt store.
- **Callers:** flows sending messages, and the `hm-*` messenger.
- **Depends on:** `signal-flow` (for `ResolveRecipient`), `signal-harness`, Herdr, the Claude attach protocol and Codex `turn/start`.

### 2.3 Orchestrate (`orchestrate`, `signal-orchestrate`, `meta-signal-orchestrate`)

Purpose:
> "I think it's better to think of the lock as the lock, and the lock returns like a certain structure which shows the paths." (psyche, typed, 2026-08-26, flows/01a03d6e/vision/locks.md)

> "The description becomes the commit message, so we ask them to write their Orchestrate lock as they would write their commit message" (psyche, flows/9993b5/vision/orchestrateCommitBinding.md)

> "Orchestrate is deployed unconditionally, in the home, for every user." (Vision/orchestrate.md)

The ethos is in §1. The meta contract adds `ReverseMetaConfiguration`, which reopens ordinary Configure, and `PeerRefused.PeerRejection`, where `PeerRejection.{ PeerUserId }`.

Datom examples:
- Request, *witnessed*: `orchestrate 'Lock.{ MyLock 6329f1 [ /absolute/path ] «why I hold it» }'`
- Reply, *constructed*: `Locked.{ 442 MyLock 6329f1 [ /absolute/path ] «why I hold it» }`
- Stream open, *witnessed* in tests: `Observed.Locks.[]`

- **Store:** one Sema store, identified by its file.
- **Callers:** every flow and subflow.
- **Depends on:** only `signal`. It has no other edges, which makes it the purest example of the form. It is also the only contract that carries the `signal` exchange layer: a handshake by contract digest, named exchanges, and `ExchangeFault.Lagged` for a subscriber that falls behind.

### 2.4 Lojix (`lojix`, `signal-lojix`, `meta-signal-lojix`)

Purpose:
> "you make a clean Lojix nexus that, for now, uses SSH on Ouranos." (psyche, flows/024bc7/vision/bootstrap.md)

> "The interface is lojix and meta-lojix CLI only." (psyche, flows/01a02b46/vision/zeusUpdate.md)

Ordinary queries: `Configure WatchDeployments Query WatchCacheRetention Unwatch`, which only observe. Owner queries: `Configure ReverseConfiguration Retire Pin Deploy Test Unpin`. Core types:
- `DeploySubmission.[ UserEnvironment.UserEnvironmentDeployment Host.HostDeployment ]`, with 14 positional fields each
- `DeploymentPhase.[ Built Completed Failed Copying Rejected Activated Submitted Building Activating ]` (source order; in lifecycle order: Submitted, Building, Built, Copying, Activating, Activated, Completed, with Failed and Rejected as ends)
- `GenerationSlot.[ Pinned Recent Rollback BootPending Current ]`
- `CacheRetentionTransition.[ Demoted Retired Pinned Promoted Unpinned Evicted ]`

Most replies carry a `DatabaseMarker.{ CommitSequence StateDigest }`, a causal cursor into the store. `Configured`, `ConfigurationRejected`, `Unwatched` and `WatchRejected` carry none, and `Watching.SubscriptionOpened.{ SubscriptionToken CommitSequence }` carries the sequence alone.

Datom examples: two unrelated examples (*witnessed*, lojix skill):
- The request `lojix-meta 'Pin.{ alpha node-1 42 keep }'`, which is answered by `Pinned.AppliedPin`.
- The Deploy reply `DeployAccepted.{ 13 { 263 263 } }`. This is admission only and does not prove completion.

- **Store:** Sema, schema v5, which refuses older stores. It holds deployments, generations, GC roots, the event log and test runs. A transition journal with an outbox gives exactly-once effects.
- **Callers:** Field and deploy flows.
- **Depends on:** Nix, SSH, `horizon-lib`'s `HorizonDefinition` (a `horizon-definition.datom` proposal file) and CriomOS.

### 2.5 Psyche Nexus (`psyche`; production donor `spirit`)

Purpose:
> "Psyche Nexus is going to replace how we log Psyche and Mind." (living, 2026-09-25, flows/e51411/vision/nexus.md; "and Mind" may be a slip, unconfirmed)

> "a new component which will include spirit, named psyche, which will hold spirit, intent and vision" (psyche, typed, 2026-08-11, flows/012fbf07/vision/threeStacks.md)

> "introduce a top-level enum; Spirit, Intent, Vision, which differentiates which layer records belong to" (same file, 2026-08-11)

State today: `psyche` is "an intentionally empty quick-new MVP component scaffold" (psyche/ARCHITECTURE.md). `signal-psyche` and `meta-signal-psyche` exist, but neither has an ethos file. The live vocabulary is `signal-spirit`:
- `Entry.{ Domains Kind Description Importance }`
- `Kind.[ Correction Principle Decision Constraint Clarification ]`
- `RecordRequest.{ Entry Justification }`
- `GuardianRejectionReason.[ Duplicate Contradiction Compound NonIntent NegativeGuideline Matter UnclearDomain ClarifyTramples ClarifyLosesMeaning SupersedeTargetMissing RetrievalInsufficient MissingTestimony TestimonyFabricated InsufficientWarrant ImportanceUnsupported HarnessUnavailable HarnessMalformed HarnessTimedOut ]` (18 members)

The guardian is an admission gate for meaning. The meta surface is `ObserveHead Configure ReverseMetaConfiguration ObserveHeadObject Import`.

- **Request, *constructed*:** `spirit 'Record.{ { [ Nexus ] Principle «A Nexus never textualizes» <Importance> } <Justification> }'`. The Importance and Justification shapes are not expanded here.
- **Store:** spirit storage schema 14, an append-style versioned log head (`VersionedLogHead`).
- **Callers:** Psyche flows and the hijacked LLM calls (the living's aim).
- **Depends on:** `signal-domain`, Criome and a mirror.

### 2.6 Mind Nexus (`mind`, `signal-mind`, `meta-signal-mind`)

Purpose:
> "The mind will kind of replace all this reporting and keeping track of which repositories are involved, what kind of knowledge and witnesses ... essentially the memory of the system is going to go in mind" (psyche, STT, flows/1a6ca4/vision/mind.md)

> "Mind Nexus is going to replace how we log the Mind and the field, not just log, but how the Mind interacts with the system, how the field interacts with the system, and how Psyche interacts with the system." (living, 2026-09-25, flows/e51411/vision/nexus.md)

This is the largest ordinary contract (22 KB).
- Queries: `SubmitThought SubmitRelation QueryThoughts QueryRelations SubscribeThoughts SubscribeRelations`, the Technical-node family, `AdjudicationRequest`, `StatusChange` and `AliasAssignment`.
- `ThoughtKind.[ Observation Memory Belief Goal Claim Decision Reference ]`
- `RelationKind.[ Implements Realizes Requires Supports Refutes Supersedes Authored References Decides Considered ... ]`
- `Thought.{ RecordIdentifier ThoughtKind ThoughtBody ActorName TimestampNanos }`

The meta contract (`AuthorityMode.[ ObserveOnly IssueOrders ProposeOrders ]`, `ChoreographyMode.[ Decide Recommend RecordOnly ]`) is still in the pre-Signal `Interface.{1 0 0}` form.

- **Request, *constructed*:** `mind 'SubmitThought.{ Observation «Flow Send promotes Pending rows» }'`
- **Reply:** `ThoughtCommitted.{ ... }`
- **Store:** `mind.sema`, the target, via sema-engine. It is a typed graph of thoughts and relations with post-commit subscription deltas.
- **Callers:** Mind flows and Field.
- **Depends on:** `signal-persona` and `signal-domain`. The implementation dates from 2026-07-31, so the contract is ahead of the body.

### 2.7 The rest of the estate (one line each)

| Nexus | Its words / role | Signature types |
|---|---|---|
| Persona | "the persona component manages all of the clusters, the different layers" (psyche, flows/05c604/vision/persona.md) | `Announce.Presence Stop.ComponentName`; `ComponentNotReadyReason.[ RecoveringFromCrash NotYetBound AwaitingDependency ]` |
| Criome | "a cryptographic biome" (psyche, typed, 2026-09-14, flows/6cc91b/vision/criome.md) | identity registration, `AuthorizeSignalCall`, quorum rounds, parked-request intercept (meta `AnswerParkedRequest`) |
| Router | "Signals cross the network through a router" (Vision/nexus.md) | peer sessions, cross-host forwarding; "no envelope, no exchange identifier" |
| Harness | adapter to Claude and Codex | `MessageDelivery InteractionPrompt WatchHarnessTranscript`; `HarnessCrashed` |
| Terminal | pane I/O | `AcquireInputGate WriteInjection RegisterPromptPattern` |
| System | OS observation | `WatchFocus`; `SystemTarget.[ NiriWindow.NiriWindowId ]` |
| Upgrade / Version-handover | live handover between versions | `AskHandoverMarker ReadyToHandover Mirror Divergence` |
| Mentci | "the Mensch [Mentci] nexus that can pretty much talk to everything if it has the right permission" (psyche, flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md; the record notes "'Mensch' reads 'Mentci'; corrected") | compiled with every signal |

Also present: agent, aggregator, cloud, introspect, listener, mirror, repository-ledger and domain-criome, each with signal and meta-signal repos.

## 3. Ontology: what kinds of things exist

- **Nexus:** a vertex. A long-running whole with ≥2 sockets, its compiled contracts, and one Sema store. "A Nexus deals with a domain." (Vision/nexus.md:114)
- **Contract (signal repo):** an edge. A closed vocabulary of queries and responses, versioned by its own crate's semver. There is an ordinary edge between every connected pair and a meta edge between only some.
- **Signal:** the value in motion, one rkyv archive per frame, unlabeled.
- **Datom:** the same value as text, living only at the CLI edge. "A datom is a form at a path" (Vision/datom.md).
- **Ethos:** the type text. Its roots are Signal (wire), Sema (records) and Library (kinds, meaning traits).
- **Sema:** the value at rest, a record in the Nexus's own store.
- **Kind:** a bearer of capabilities (a trait). "In ethos there are no generics, only kinds." (Vision/ethos.md:48)
- **Flow:** a live model seat with identity (`FlowId`), aspect, power and lifecycle.
- **Aspect:** Psyche, Mind or Field. This is the authority layer of a flow, and it is also becoming the domain of a Nexus: Psyche Nexus, Mind Nexus, and Flow as Field.
- **Power:** the capacity tier of a flow (High, Medium, Low, UltraLow).
- **Lock:** a claim on paths by a flow, with a reason that becomes the commit message.
- **Deployment / Generation:** Lojix's unit of change to a node and its result.
- **Receipt / Marker:** proof records such as `DatabaseMarker`, `PresentationReceipt` and `CompactReceipt`. Proof is itself typed, and each receipt is graded to what it proves (Presented is not Read; Accepted is not Delivered).
- **Rejection:** a first-class noun, since errors are vocabulary.

## 4. Geometry: how the parts relate

1. **Two concentric rings per Nexus.** The ordinary socket (0660 or 0600) is the domain face. The meta socket (0600, peer-UID checked) is root. Configuration enters only through meta, except during first boot. Until the meta Configure has happened once (`MetaConfigureDone`), Configure is open on the ordinary socket. `ReverseMetaConfiguration` reopens it. The result is a one-way latch: bootstrap authority is handed to the owner and never taken back by accident.
2. **The Nexus graph.** Peers depend on each other's contract crates, never on each other's Nexus: "The contract is the whole relationship" (Curriculum `nexus` skill). Observed edges: Message→Flow (`ResolveRecipient`), Message→Harness, Flow→Herdr and Codex (outside Signal), Lojix→Horizon, Mind→Persona, Criome→`signal` taxonomy, Spirit→Domain. Mentci and the Router are the hubs compiled with every contract: "If we add a new thing to the cluster of nexuses, then everybody has to recompile …" (psyche, flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md).
3. **A text membrane.** Text exists at exactly one place, the CLI. Inside the membrane everything is typed binary, and the Nexus compiles its contracts without the `datom` feature.
4. **Aspect tiers above the graph.** Psyche (meaning), Mind (memory), Field (acting). The authority order is Spirit > Intent > Vision > Notion (Vision/psyche.md). These tiers are becoming nexuses themselves, so the organisational hierarchy is being made concrete as components.
5. **Data flow.** Datom text goes to the CLI, then the Signal frame to Nexus Core (actors), then a durable intent in Sema, then the effect (pane, Nix, SSH), then a typed receipt, and subscribers receive the delta. Flow and Lojix both write the intent before the effect. Lojix, for example, stores "a durable correlation record plus a pending transition intent".
6. **Observation.** "State is observed by subscription ... Polling is forbidden; a correct system goes quiet when nothing changes." Orchestrate makes the stream the connection. Lojix and Mind issue tokens.

## 5. Recurring structural patterns

- Verb, then past tense, then named rejection with a closed reason enum.
- Configure appears in both contracts, and the receipt carries the latch state.
- Durable intent before effect (write-ahead), then graded receipts.
- A `DatabaseMarker` or commit sequence on replies, so a caller can place an answer in time.
- Admission is not completion: `DeployAccepted`, `Sent.Accepted` and `ReceiptKind.Accepted` each mean only "taken in". A later record proves the outcome.
- The same-shaped record is reused across edges: Message routes on `FlowNode`. Imported and launched flows do not share one shape: launched flows register as `FlowNode`, imported seats bind as `FlowBinding` (13 fields), answered by `BoundFlowBinding.{ FlowId FlowLifecycle }`, and meta-signal-flow's `FlowLifecycle.[ RegisteredUnconfirmed ]` is a second lifecycle enum, disjoint from signal-flow's `[ Pending Active Stopped ]`.
- A stream opens with the full state, even when empty (`Observed.Locks.[]`).
- Structural paths are always absolute, and positional fields are named only by type.

## 6. Inconsistencies found

1. **`ComponentKind`** in `signal` and `signal-standard` lists Message, Router, Criome, Mind, Spirit, Persona, Agent, Mirror, Introspect, Harness, Terminal, System, Lojix and Orchestrate. It has no Flow and no Psyche, even though the router enum is meant to cover every Nexus.
2. **Framing has split three ways.** Orchestrate uses the exchange handshake with a contract digest and multiplexed exchanges. Router and Message use "no envelope ... one connection carries one request and one reply". Lojix transports `Signal<Query>`.
3. **Zero-argument start is not uniform.** Vision says "A Nexus starts with no arguments …" (Vision/nexus.md:76). Message "receives one binary configuration path as its only argument", and Lojix needs a `lojix-write-configuration` archive and has "no default path" for either socket.
4. **Flags survive.** `flow-meta reset <idempotency-key> [<credit-id>]` is positional-flag style, against "exactly one positional argument ... datom" (Curriculum `nexus` skill).
5. **Pins disagree.** Message pins signal-flow `968ae3b`, while Flow 0.7.0 ships `ab70332`. Two contract generations are live on one edge.
6. **Vocabulary drift.** "Owner" (Lojix, Spirit, Message) vs "meta". "Daemon" in `MessageDaemonConfiguration`, `message-daemon` and `DaemonHost`, against "call it a Nexus, never a daemon" (Curriculum `nexus` skill). Spirit's README still says "NOTA/DOTOS". Lojix's readiness line `(LojixNexusReady …)` is in old parenthesised syntax.
7. **`meta-signal-mind`** is still `Interface.{1 0 0}`, a versioned pre-Signal root, against "An ethos file carries no version".
8. **Psyche** has signal repos with no ethos, while Spirit's contract is live. The migration path is not written, and "Any future dependency ... requires a separate ruling" (psyche/ARCHITECTURE.md).
9. **Lojix inverts the ethos of meta.** Everyday work (Deploy) sits on the owner socket, while in Flow and Orchestrate everyday work is ordinary. This is defensible, since deploying is root-level, but it is the one Nexus where "ordinary" means read-only.
10. **Strings in the core.** Flow carries about 30 `String` aliases (`ModelName`, `Effort`, `HerdrPaneId`), and Message has `Error.ErrorReport` with `ErrorMessage`. Vision tolerates these as "records on the way to a fully typed form" (Vision/nexus.md:57).
11. **Streaming is not uniform.** It is the connection in Orchestrate, a `SubscriptionToken` with `Unwatch` in Lojix, and `SubscriptionRetraction` in Mind.

## 7. Real-world comparisons

- **Actor model / Erlang-OTP.** Matches: Nexus Core runs on Kameo actors; replies are typed messages; "let it crash" appears as `HarnessCrashed` and `RecoveringFromCrash`. Differs: there is no supervision tree between Nexuses yet. Persona is meant to supervise, but it is a stub, and OTP's restart strategies have no Nexus equivalent. OTP's messages are dynamically typed terms, while Signal is closed and compiled in.
- **Capability systems (seL4, Capsicum, E).** Matches: a socket is a capability, the meta socket is the root capability, and Criome's `AuthorizeSignalCall` points toward object capabilities by digest. Differs: authority is a Unix file mode plus peer UID, so it is ambient per user and not unforgeable per object. Flow's own DESIGN admits it "does not distinguish processes with the same UID".
- **Kubernetes controllers.** Lojix closely matches the reconcile loop: a desired proposal, observed generations, phase events, and a watch API with resource-version markers (`DatabaseMarker` ≈ `resourceVersion`). It differs in being imperative (Deploy is a verb) rather than declarative (desired state applied repeatedly).
- **Datomic / Datalog.** Matches: the name, append-style facts, and Mind's thought and relation graph as an entity-relation store. Differs: "Datomic names the conceptual layer abstractly; it is not a term of the code" (Vision/datom.md). A datom here is a text form, not an entity-attribute-value-time tuple, and there is no Datalog query language. Queries are closed verbs.
- **Plan 9.** Matches: each service has its own small protocol endpoint, and a thin client does the textualizing. Differs: Plan 9 made everything a file with one generic protocol (9P). Here every Nexus has its own typed protocol and nothing is generic.
- **systemd.** Matches: socket-bound long-running units, readiness announced on stdout (like `sd_notify`), and "never on a clock". Differs: configuration is in the Nexus's own store through meta, not in unit files.
- **Unix pipes.** The CLI is a filter: one value in, one value out. It differs in that values are typed and positional, not byte streams, and there is no composition operator between CLIs yet.
- **gRPC / protobuf.** Closest in shape (a schema repo per service, generated code). Differs: no field numbers, no optional-by-default fields, closed enums, and semver per contract crate instead of wire-evolution rules.

## 8. Illustration subjects for a flashbook

1. A walled city with two gates: a busy market gate (ordinary socket) and a small iron door with one keyholder (meta socket), and a vault (Sema) at its heart.
2. An interpreter standing at a border post, turning a handwritten letter (datom) into a sealed metal cylinder (signal) that passes a gate where no one reads.
3. A constellation of glowing stars (nexuses) joined by threads, each thread a scroll of written treaty (contract), with a few threads doubled in gold (meta edges).
4. A cartographer's office with a key-rack of labelled brass keys on hooks, each tag a list of paths and a reason (Orchestrate locks).
5. A shipyard foreman handing out launch tickets, where each ticket shows a phase stamped in sequence: Reserved, Bound, Prompt Observed (a Flow launch attempt).
6. A postal sorting room where a clerk checks each letter's address against a living registry book before dropping it through a pane-shaped slot (Message consulting Flow).
7. A shipwright's dry-dock with numbered hulls on slipways, some pinned with chains, one sliding into the water (Lojix generations and deploy).
8. Three figures around a loom (Psyche weaving meaning, Mind keeping the ledger of threads, Field working the treadle), with the loom itself as the body of the machine.

## Sources

- Vision: /home/li/primary/Vision/nexus.md, flowNexus.md, signal.md, sema.md, messaging.md, orchestrate.md, psyche.md, datom.md
- Raw vision:
  - flows/e51411/vision/nexus.md
  - flows/836818/vision/nexusAnatomy.md and flowNexus.md
  - flows/012fbf07/vision/threeStacks.md
  - flows/01a03d6e/vision/locks.md
  - flows/9993b5/vision/orchestrateCommitBinding.md
  - flows/024bc7/vision/bootstrap.md
  - flows/01a02b46/vision/zeusUpdate.md
  - flows/1a6ca4/vision/mind.md
  - flows/05c604/vision/persona.md
  - flows/6cc91b/vision/criome.md
  - flows/b81560/vision/operational-refreshFlowAndMessageFlowCoordination.md
  - flows/b49251/vision/nexusAnatomy.md
- Contracts (/git/github.com/LiGoldragon/):
  - signal-flow@ab70332 and meta-signal-flow@a34bc65 ethos/signal.ethos
  - signal-message@7f2fc2d and meta-signal-message
  - signal-orchestrate and meta-signal-orchestrate
  - signal-lojix and meta-signal-lojix
  - signal-spirit and meta-signal-spirit
  - signal-mind and meta-signal-mind (interface.ethos)
  - signal-persona, signal-criome, meta-signal-criome, signal-router, signal-harness, signal-terminal, signal-system, signal-upgrade
  - signal and signal-standard ethos/signal.ethos
- Bodies: flow/README.md and DESIGN.md (0.7.0, 812053c); message README (origin/main 9330640); orchestrate/README.md; lojix/README.md; psyche/ARCHITECTURE.md; spirit/README.md; mind/README.md; persona/README.md
- Skills: nexus, ethos, lojix
- Prior e51411 reports: reports/nexus-open-design-questions.md and reports/flow-message-basics.md
## Corrections, 2026-09-25

Made after the review by 38de5b (`flows/38de5b/reports/ethos-review.md`), each checked again against the live contracts under /git/github.com/LiGoldragon/ and the psyche records; the text above is fixed in place.

- **§1:** "The smallest complete example is Orchestrate's" → "A small complete example"; signal-system's ordinary contract is smaller (33 lines to 47).
- **§1 table, Clients:** the meta client is usually `<x>-meta`, not always: Spirit ships `meta-spirit`, and Message also ships `meta-message`.
- **§2.3:** `PeerRefused.{ PeerUserId }` → `PeerRefused.PeerRejection`, with `PeerRejection.{ PeerUserId }`.
- **§2.4:** `DeploymentPhase` now printed in its source order, with the lifecycle order stated separately.
- **§2.4:** "Every reply carries a `DatabaseMarker`" → "Most replies"; `Configured`, `ConfigurationRejected`, `Unwatched` and `WatchRejected` carry none, and `Watching` carries a `CommitSequence` only.
- **§2.4:** the Pin request and `DeployAccepted` are two unrelated examples; Pin is answered by `Pinned.AppliedPin`.
- **§2.5:** `GuardianRejectionReason` has 18 members, not the 9 printed; all 18 are now listed.
- **§2.6:** the Mind Nexus quote was cut without a mark and lost its scope; it is restored in full, with "how the field interacts with the system, and how Psyche interacts with the system".
- **§2.7:** the Mentci quote now shows the raw word, "the Mensch [Mentci] nexus", with the record's own correction note and the full file citation.
- **§4.2:** the recompile quote is marked as cut ("…") and cited by file.
- **§3, §4.2, §6.4, §6.6:** "The contract is the whole relationship", "call it a Nexus, never a daemon" and "exactly one positional argument … datom" are cited to the Curriculum `nexus` skill, not Vision or psyche.
- **§3, §6.3, §6.10:** citations added for "A Nexus deals with a domain" (Vision/nexus.md:114), "In ethos there are no generics, only kinds" (Vision/ethos.md:48), "A Nexus starts with no arguments …" (Vision/nexus.md:76, cut marked) and "records on the way to a fully typed form" (Vision/nexus.md:57; the review placed this at Vision/signal.md:56-57, where it is not).
- **§5:** "imported and launched flows share one shape" was wrong: launched flows register as `FlowNode`, imported seats bind as `FlowBinding` (13 fields) → `BoundFlowBinding`, and meta-signal-flow's `FlowLifecycle.[ RegisteredUnconfirmed ]` is disjoint from signal-flow's.
- **Omitted, now noted:** meta-signal-flow `a34bc65`/`4748cfa` imported `RecipientDisposition` from signal-flow, which defines no such type at any revision. meta-signal-flow `f715883` (6.0.1) drops it.
- **Revisions have moved since:** signal-flow is at `5ca97ce` (4.0.0: `Replace`, `LaunchStatus` and `Observe` added; 8 `*Rejected`), flow at `28a78d2` (0.9.0) pins it, and Message still pins signal-flow `968ae3b`. The contract excerpts above stay at the revisions the report names.
