# Ethos Flashbook — Three Nexus Contracts, Inline

A specification for vivified visualization. Psyche Medium b80e55 composes;
Psyche Fable f38926 audits; Sonnet visualizes. Six sections, each with
imagery, flowchart, and text.

Every type is defined at first mention with its full inline specification.
Every later mention is only the name. No duplication.

---

## Section 1: What a Signal Is

### Imagery

A stone tablet split into four horizontal bands, each a different material.
The top band is dark obsidian — empty, meaning the signal imports nothing
from outside. The second band is polished copper with etched symbols flowing
left-to-right — these are queries, what a peer may ask. The third band is
silver with symbols flowing right-to-left — answers, what the nexus replies.
The bottom band is the largest, rough granite carved with interlocking shapes
— the type declarations that give every symbol its meaning. The tablet floats
in a dark space. Thin golden lines connect symbols in the copper band to
their definitions in the granite, and symbols in the silver band likewise
connect down. Where two bands reference the same granite carving, a single
golden line branches to both.

### Flowchart

```
┌─────────────────────────────────────────────┐
│                  Signal                      │
├─────────────────────────────────────────────┤
│  IMPORTS   [ ]                               │  ◄─ what other signals this one uses
├─────────────────────────────────────────────┤
│  QUERIES   [ Configure  Lock  Release        │  ◄─ what the peer may ask
│              Observe ]                       │
├─────────────────────────────────────────────┤
│  ANSWERS   [ Configured  Locked  Released    │  ◄─ what the nexus replies
│              Observed  Rejected... ]         │
├─────────────────────────────────────────────┤
│  TYPES     [ every name above resolves here  │  ◄─ the granite: all type definitions
│              LockId.Integer                   │
│              LockName.String                  │
│              Lock.{ LockId LockName ... }    │
│              ... ]                            │
└─────────────────────────────────────────────┘
```

Comments on flowchart:
- The four bands are the four `[ ]` blocks in every signal.ethos file
- Imports at the top: what this contract borrows from another signal
- Queries and Answers carry type names — their definitions live in Types
- Types is the largest section: every name used above is defined here once

### Text

1. A Signal is a contract between two peers — one asks, one answers
2. Four parts: imports, queries, answers, types — always in that order
3. Every type name in queries and answers must resolve in the types block
4. The types block defines each name once: `Name.Shape`
5. A struct is `Name.{ Field1 Field2 }` — a product of its fields
6. A variant is `Name.[ Case1 Case2.Payload ]` — a sum of its cases

---

## Section 2: Orchestrate — The Simplest Nexus

### Imagery

A locksmith's workshop. On the left wall, a rack of brass keys, each
engraved with a name. On the right, a heavy iron lock-box with numbered
slots. In the center, a workbench where a key is being fitted to a slot.
Above the bench, a window shows an observer watching the workshop — they
see every key fitted and every key removed. The brass of each key glows
faintly with the color of the flow that owns it. On the floor, a rejected
key with overlapping teeth — two keys tried to fit the same slot.

### Flowchart

```
                    ┌──────────┐
                    │   Peer   │
                    └────┬─────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌─────────────┐ ┌──────────┐ ┌────────────┐
   │    Lock     │ │ Release  │ │  Observe   │
   │ ─────────── │ │ ──────── │ │ ────────── │
   │ LockRequest │ │  LockId  │ │  .Locks    │
   └──────┬──────┘ └─────┬────┘ └─────┬──────┘
          │              │            │
          ▼              ▼            ▼
   ┌─────────────┐ ┌──────────┐ ┌────────────┐
   │   Locked    │ │ Released │ │  Observed  │          ◄─ streams: first frame
   │ ─────────── │ │ ──────── │ │ ────────── │             is the full state,
   │    Lock     │ │   Lock   │ │ Vec<Lock>  │             then one per change
   └─────────────┘ └──────────┘ └────────────┘
          │
          ▼ (or)
   ┌──────────────┐
   │ LockRejected │
   │ ──────────── │
   │ DuplicateName│        ◄─ two keys with the same teeth
   │ PathOverlap  │        ◄─ two keys for overlapping slots
   └──────────────┘
```

Comments on flowchart:
- Three queries: Lock, Release, Observe — that's the entire surface
- Observe is the only streaming answer: it keeps sending
- Rejection carries the reason: either a duplicate name or overlapping paths
- Every Lock carries its integer ID after acquisition

### Ethos — full inline, sugar syntax

```ethos
Signal

[]                                              ; no imports

[ Configure.OrchestrateNexusConfiguration       ; first-time setup
  Lock.LockRequest                              ; acquire a lock
  Release.LockId.Integer                        ; release by integer id
  Observe.ObserveSelection.[ Locks ] ]          ; subscribe to state

[ ConfigurationAccepted.ConfigurationReceipt
  ConfigurationRefused.ConfigurationRejection
  Locked.Lock                                   ; the acquired lock
  Released.Lock                                 ; the released lock
  Observed.Observation.[ Locks.Vector<Lock> ]   ; state snapshot or delta
  LockRejected.LockRejection
  ReleaseRejected.ReleaseRejection.[ UnknownLockId ] ]

[ ConfigurationPath.String
  OrdinarySocketPath.ConfigurationPath          ; reuses ConfigurationPath
  MetaSocketPath.ConfigurationPath              ; reuses ConfigurationPath
  OrchestrateNexusConfiguration.{ OrdinarySocketPath MetaSocketPath }
  MetaConfigureDone.Boolean
  ConfigurationReceipt.{ OrchestrateNexusConfiguration MetaConfigureDone }
  ConfigurationRejectionReason.[ MetaConfigureOccurred InvalidConfiguration ]
  ConfigurationRejection.{ ConfigurationRejectionReason }
  LockName.String
  FlowId.String
  LockPath.String
  LockReason.String
  LockRequest.{ LockName FlowId Vector<LockPath> LockReason }
  Lock.{ LockId LockName FlowId Vector<LockPath> LockReason }
  LockOverlap.{ LockPath Lock }                ; ◄─ Lock: already defined
  LockRejection.[ DuplicateName.Lock PathOverlap.LockOverlap ] ]
```

Note: `LockId` defined inline at first use in the queries block (`Release.LockId.Integer`).
`Lock` defined once in the types block; `LockOverlap` and `LockRejection` reference it by name only.
`ConfigurationPath` defined once; both socket paths reuse it.

### Text

1. Orchestrate is the one fully operational nexus — live Lock/Release/Observe on production
2. The entire surface is three operations: acquire, release, watch
3. Observe streams: first frame is the complete state, then one frame per change
4. A Lock carries five fields: integer id, name, owning flow, paths, reason
5. Rejection is typed: DuplicateName or PathOverlap, each carrying the conflicting Lock

---

## Section 3: Flow — Identity Resolution

### Imagery

A switchboard room from the early telephone era. An operator sits before a
board of sockets, each socket labeled with a flow identity. Colored cables
connect sockets to the machines behind the board — some cables glow green
(active), some are dark (parked), some sockets have no cable (unavailable).
The operator holds a new cable, reading a request card to determine which
socket it connects to. Behind the board, visible through a glass panel, the
actual machines (Codex, Claude) run in their own rooms, each with a Herdr
terminal showing their pane. A second operator at a smaller desk handles
restarts — pulling a cable, incrementing a generation counter on the socket
label, and plugging in a fresh cable.

### Flowchart

```
                    ┌──────────┐
                    │   Peer   │
                    └────┬─────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌─────────────┐ ┌───────────┐ ┌──────────────────┐
   │    Start    │ │  Restart  │ │ ResolveRecipient │
   │ ─────────── │ │ ───────── │ │ ──────────────── │
   │StartRequest │ │RestartReq │ │     FlowId       │
   └──────┬──────┘ └─────┬─────┘ └───────┬──────────┘
          │              │               │
          ▼              ▼               ▼
   ┌─────────────┐ ┌───────────┐ ┌──────────────────┐
   │   Started   │ │ Restarted │ │RecipientResolved │
   │ ─────────── │ │ ───────── │ │ ──────────────── │
   │ FlowId +    │ │ FlowId +  │ │    FlowNode      │  ◄─ the full node record:
   │ SessionId + │ │SessionId +│ │                   │     identity, harness,
   │ OriginClue  │ │Generation │ │                   │     endpoint, Herdr route,
   └─────────────┘ └───────────┘ └──────────────────┘     lifecycle state
```

Comments on flowchart:
- Start creates a new flow; Restart resumes an existing one with a new generation
- ResolveRecipient is the lookup: given a FlowId, return the full FlowNode
- FlowNode carries everything needed to reach the flow: harness kind, endpoint, Herdr route
- Each route has a readiness state: Ready or Parked

### Ethos — full inline, sugar syntax

```ethos
Signal
[]
[ Start.StartRequest
  Restart.RestartRequest
  ResolveRecipient.RecipientResolutionRequest.FlowId.String ]

[ Started.Started                               ; ◄─ type and answer share the name
  Restarted.Restarted
  RecipientResolved.FlowNode
  StartRejected.StartRejection
  RestartRejected.RestartRejection
  RecipientResolutionRejected.RecipientResolutionRejection ]

[ SessionId.String
  TurnId.String
  FlowType.String
  Generation.Integer
  EndpointPath.String
  HerdrSessionName.String
  HerdrAgentName.String
  HerdrPaneId.String
  HerdrTerminalId.String
  OriginClue.{ FlowId SessionId TurnId }        ; ◄─ FlowId: already defined
  StartRequest.{ FlowType OriginClue }
  RestartRequest.{ FlowId OriginClue }           ; ◄─ FlowId, OriginClue: names only
  HarnessKind.[ Codex Claude ]
  RouteReadiness.[ Ready Parked ]
  EndpointSelection.[ Available.{ EndpointPath RouteReadiness } Unavailable ]
  HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId }
  HerdrRouteSelection.[ Available.HerdrRoute Unavailable ]
  FlowLifecycle.[ Pending Active ]
  FlowNode.{ FlowId SessionId HarnessKind EndpointSelection
              HerdrRouteSelection OriginClue FlowLifecycle }
  Started.{ FlowId SessionId OriginClue }
  Restarted.{ FlowId SessionId Generation }
  StartRejection.[ UnknownFlowType LaunchRefused OriginUnavailable ]
  RestartRejection.[ ProvenanceMismatch UnknownFlow ResumeRefused ]
  RecipientResolutionRejection.[ UnknownFlow FlowUnavailable ] ]
```

Note: `FlowId.String` defined once in the queries block. Every later use — in
`OriginClue`, `StartRequest`, `RestartRequest`, `FlowNode`, `Started`,
`Restarted` — is just `FlowId`. Same for `SessionId`, `OriginClue`, and
every Herdr field.

### Text

1. Flow Nexus resolves identity: given a flow id, find the live machine
2. A FlowNode carries harness kind (Codex or Claude), endpoint, Herdr route, and lifecycle
3. Start creates; Restart resumes with a new generation counter
4. Routes are Ready or Parked, endpoints Available or Unavailable
5. The Herdr route has four fields: session, agent name, pane, terminal — the exact binding
6. Code exists; the nexus daemon is not yet deployed — this is the single biggest gap

---

## Section 4: Lojix — The Deployment Engine

### Imagery

A shipyard with multiple dry docks. In each dock, a ship (a deployment) is
in a different stage: one has its keel being laid (Building), one is having
its hull sealed (Copying), one is being lowered into water (Activating), one
floats at the dock with crew aboard (Completed), one lies broken on its side
(Failed). Above the shipyard, a control tower (the nexus daemon) has a glass
wall showing a board with every ship's status. Below the docks, a deep
warehouse (the generation store) holds numbered plans — each plan is a
generation, and a deployment is one plan being executed. Observers stand at
windows in the tower, watching. A rejected ship has a red flag: its dock was
unknown, or its plans malformed. At the edge, a test basin with two small
model ships (hermetic test) and a canal leading to open water (live test).

### Flowchart

```
                         ┌──────────┐
                         │   Peer   │
                         └────┬─────┘
                              │
       ┌──────────┬───────────┼───────────┬──────────────┐
       ▼          ▼           ▼           ▼              ▼
  ┌─────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │Configure│ │ Query  │ │  Watch   │ │  Watch   │ │ Unwatch  │
  │         │ │        │ │Deployment│ │  Cache   │ │          │
  └────┬────┘ └───┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │          │           │            │             │
       ▼          ▼           ▼            ▼             ▼
  ┌─────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
  │Configured││Queried │ │ Watching │ │ Watching │ │Unwatched │
  │    or    ││        │ │(streams) │ │(streams) │ │          │
  │ Rejected ││        │ │          │ │          │ │          │
  └─────────┘└────────┘ └──────────┘ └──────────┘ └──────────┘

  Query resolves by:
  ┌─────────────────────────────────────────────────────────┐
  │  ByNode ──── cluster + node ──── generations + deploys  │
  │  ByDeployment ──── deployment id ──── one record        │
  │  ByGeneration ──── generation id ──── one record        │
  │  ByTestRun ──── cluster + node ──── test run records    │
  │  ByEventLog ──── position range ──── phase events +     │
  │                                       cache transitions │
  └─────────────────────────────────────────────────────────┘

  Deployment lifecycle:
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐
  │Submitted │──▶│ Building │──▶│ Copying  │──▶│Activating │
  └──────────┘   └──────────┘   └──────────┘   └───────────┘
       │              │              │               │
       ▼              ▼              ▼               ▼
  ┌──────────┐   ┌──────────┐  ┌──────────┐   ┌───────────┐
  │ Rejected │   │  Failed  │  │  Failed  │   │ Activated │
  └──────────┘   └──────────┘  └──────────┘   └─────┬─────┘
                                                     │
                                                     ▼
                                               ┌───────────┐
                                               │ Completed │
                                               └───────────┘
```

Comments on flowchart:
- Five query selectors: by node, deployment, generation, test run, event log range
- Deployments progress through a typed lifecycle: Submitted → Building → Copying → Activating → Completed
- Any stage can fail; Submitted can be Rejected
- Watch is streaming like Orchestrate's Observe
- Cache retention tracks generation lifecycle: Promoted, Pinned, Demoted, Retired, Evicted

### Ethos — full inline, sugar syntax (selected core types)

```ethos
Signal

[ horizon_lib:[ HorizonDefinition ] ]           ; ◄─ imports Horizon's definition type

[ Configure.LojixNexusConfiguration
  WatchDeployments.DeploymentWatch
  Query.Selection
  WatchCacheRetention.CacheRetentionWatch
  Unwatch.SubscriptionClose ]

[ Configured.ConfigurationReceipt
  ConfigurationRejected.ConfigurationRejection
  Queried.GenerationListing
  Watching.SubscriptionOpened
  Unwatched.SubscriptionClosed
  QueryRejected.RejectedQuery
  WatchRejected.RejectedWatch
  UnwatchRejected.RejectedUnwatch ]

; ── Configuration ──
[ OrdinarySocketPath.String
  OrdinarySocketMode.Integer
  OwnerSocketPath.String
  OwnerSocketMode.Integer
  StateDirectoryPath.String
  DaemonHost.String
  MetaConfigureOccurred.Boolean
  ClusterName.String
  NodeName.String
  NixSystem.String
  FlakeReference.String
  FlakeAttribute.String
  DeploymentOutputSelector.{ FlakeAttribute }
  TestMode.[ Hermetic Live ]
  TestDefaults.{ ClusterName NodeName TestMode FlakeReference
                 NixSystem DeploymentOutputSelector
                 Option<HorizonDefinition> }     ; ◄─ imported type, name only
  TestDefaultsChoice.[ NoTestDefaults TestDefaults ]
  LojixNexusConfiguration.{ OrdinarySocketPath OrdinarySocketMode
                             OwnerSocketPath OwnerSocketMode
                             StateDirectoryPath DaemonHost
                             TestDefaultsChoice }
  ConfigurationReceipt.{ LojixNexusConfiguration MetaConfigureOccurred }
  ConfigurationRejectionReason.[ OrdinaryConfigureClosed InvalidConfiguration ]
  ConfigurationRejection.{ ConfigurationRejectionReason }

; ── Identity ──
  DeploymentIdentifier.Integer
  GenerationIdentifier.Integer
  ImmutableRevision.String
  ClosurePath.String
  CommitSequence.Integer
  StateDigest.Integer
  DatabaseMarker.{ CommitSequence StateDigest }
  AdmissionMarker.DatabaseMarker                ; ◄─ DatabaseMarker: name only
  TransitionMarker.DatabaseMarker
  TerminalMarker.DatabaseMarker

; ── Deployment request ──
  UserName.String
  DeploymentEnvironment.[ HostEnvironment UserEnvironment.UserName ]
  GenerationArtifact.[ BaseHost CompleteHost UserEnvironment ]
  ActivationEffect.[ ProfileOnly BootOnceProfile TestActivation
                     LiveActivation BootProfile ]
  SourceRevisionPolicy.[ ResolveAndRecord RequireImmutable ]
  DeploymentRequestIdentity.{ DeploymentEnvironment ClusterName NodeName
                               GenerationArtifact                ; all names only
                               RequestedDeploymentAction
                               ActivationEffect SourceRevisionPolicy
                               Option<ImmutableRevision> }
  HostDeployAction.[ TestActivation ScheduleBootOnce Realize
                     SetBootProfile Evaluate ActivateNow ]
  UserEnvironmentAction.[ ActivateNow Realize SetProfile ]
  RequestedDeploymentAction.[ Host.HostDeployAction
                              UserEnvironment.UserEnvironmentAction ]

; ── Lifecycle ──
  DeploymentPhase.[ Built Completed Failed Copying Rejected
                    Activated Submitted Building Activating ]
  DeploymentLifecycle.[ Failed Rejected Completed Building
                        Activating Submitted Copying Activated Built ]
  DeploymentFailureStage.[ Build Eval MaterializeHorizon Daemon
                           Activate CopyClosure Admission FlakeAuth ]
  FailureEvidence.{ Option<FailedCommand> FailureDetail.String
                    DetailTruncated.Boolean }
  FailedCommand.{ CommandProgram.String Vector<CommandArgument.String>
                  Option<ExitCode.Integer> }
  DeploymentTerminalReason.[ NodeUnknown FlakeReferenceMalformed
    ProposalSourceUnreachable DeploymentInFlight
    InvalidDeploymentRouting UnsupportedDeployAction InternalError
    ClusterUnknown ActivationFailed BuilderUnreachable
    SubstituterUnreachable EvaluationFailed BuildFailed ]
  DeploymentFailure.{ DeploymentFailureStage DeploymentTerminalReason
                      Option<FailureEvidence> }  ; all names only
  DeploymentTerminal.[ Succeeded Failed.DeploymentFailure
                       Rejected.DeploymentTerminalReason ]

; ── Records ──
  DeploymentRecord.{ DeploymentIdentifier GenerationIdentifier
                     DeploymentRequestIdentity Option<AdmissionMarker>
                     DeploymentLifecycle Option<TerminalMarker>
                     Option<DeploymentTerminal> }
  Generation.{ GenerationIdentifier DeploymentIdentifier ClusterName
               NodeName GenerationArtifact ActivationEffect
               GenerationSlot.[ Pinned Recent Rollback BootPending Current ]
               Option<ClosurePath> Option<ImmutableRevision> }
  GenerationListing.{ Vector<Generation> Vector<DeploymentRecord>
                      DatabaseMarker }

; ── Queries ──
  NodeSelector.{ ClusterName NodeName
                 Option<RequestedGenerationArtifact.[ UserEnvironment
                   CompleteHost BaseHost ]> }
  EventLogPosition.Integer
  EventLogRange.{ EventLogPosition EventLogPosition }
  Selection.[ ByNode.NodeSelector
              ByTestRun.TestRunLookup
              ByDeployment.DeploymentLookup.{ DeploymentIdentifier }
              ByGeneration.GenerationLookup.{ GenerationIdentifier }
              ByEventLog.EventLogRange ]
  QueryRejectionReason.[ MalformedSelector EventLogPositionOutOfRange
                         GenerationUnknown NodeUnknown ]
  RejectedQuery.{ QueryRejectionReason DatabaseMarker }

; ── Subscriptions ──
  SubscriptionToken.Integer
  SubscriptionOpened.{ SubscriptionToken CommitSequence }
  SubscriptionClose.{ SubscriptionToken }
  SubscriptionClosed.{ SubscriptionToken }
  WatchRejectionReason.[ MalformedWatch SubscriptionLimitReached
                         StreamUnavailable ]
  RejectedWatch.{ WatchRejectionReason }
  UnwatchRejectionReason.[ SubscriptionTokenUnknown
                           SubscriptionAlreadyClosed ]
  RejectedUnwatch.{ UnwatchRejectionReason SubscriptionToken }
  DeploymentWatch.{ Option<DeploymentIdentifier> Option<ClusterName>
                    Option<NodeName> }
  CacheRetentionWatch.{ Option<ClusterName> Option<NodeName> }

; ── Events ──
  DeploymentPhaseEvent.{ DeploymentIdentifier GenerationIdentifier
                         ClusterName NodeName DeploymentPhase
                         EventLogPosition TransitionMarker
                         Option<ImmutableRevision>
                         Option<DeploymentTerminal> }
  CacheRetentionTransition.[ Demoted Retired Pinned Promoted
                             Unpinned Evicted ]
  PinLabel.String
  CacheRetentionTransitionEvent.{ GenerationIdentifier ClusterName
    NodeName CacheRetentionTransition GenerationSlot
    Option<GenerationSlot> Option<PinLabel> EventLogPosition }
  EventLogPage.{ Vector<DeploymentPhaseEvent>
                 Vector<CacheRetentionTransitionEvent> DatabaseMarker }

; ── Test runs ──
  TestRunIdentifier.Integer
  FailureStage.[ HermeticCheck BringUp Assert Deploy TearDown ]
  TestOutcome.[ Pending Passed Failed.FailureStage ]
  TestRunPhase.[ Submitted BringingUp TearingDown Completed
                 Deploying Asserting Failed ]
  TestRunLookup.{ ClusterName NodeName Option<TestRunIdentifier> }
  TestRunRecord.{ TestRunIdentifier ClusterName NodeName NodeName
                  TestMode TestRunPhase TestOutcome
                  Option<ClosurePath> }
  TestRunListing.{ Vector<TestRunRecord> DatabaseMarker } ]
```

Note: 100+ types, zero duplication. `ClusterName`, `NodeName`, `DeploymentIdentifier`,
`GenerationIdentifier`, `DatabaseMarker`, `DeploymentTerminal`, `ActivationEffect`,
`GenerationSlot` — each defined exactly once, used many times by name only.
`FailureEvidence` defines `FailureDetail.String` and `DetailTruncated.Boolean`
inline at first mention within its struct.

### Text

1. Lojix is the deployment engine — builds, copies, activates closures on cluster nodes
2. Deployments have a typed lifecycle: Submitted through Completed, with failure at any stage
3. Every failure carries structured evidence: the command, its exit code, the detail
4. Generations are the numbered plans; deployments execute a plan on a node
5. The event log is a position-indexed stream of deployment and cache retention transitions
6. Test runs have their own lifecycle: Hermetic (isolated) and Live (production)

---

## Section 5: The Wire — Datom Carries Everything

### Imagery

A glass pipe system in a factory. The pipes are transparent, and inside
them colored crystals flow — each crystal is a datom. A red crystal is an
Integer, a blue crystal is a String, a green cluster of crystals bound
together is a Struct, a crystal that shifts between colors as you look at
it is a Variant. At the pipe junctions, a Budget gauge shows how much
parsing effort remains — when it hits zero, the pipe clamps shut
(protection against malformed input). At the source end, a craftsman
(Datomizable) turns a Rust value into crystals. At the destination end,
a craftsman (Composing) assembles crystals back into a Rust value. Between
them, the pipe doesn't know or care what the crystals mean — it just carries
them.

### Flowchart

```
  Rust value                                          Rust value
      │                                                   ▲
      ▼                                                   │
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
 │Datomizable│──▶│  Datom   │──▶│   Wire   │──▶│ Composing  │
 │           │   │          │   │          │   │            │
 │.datomize()│   │ Form:    │   │ bytes    │   │.compose()  │
 │           │   │  Struct  │   │          │   │  +Budget   │
 │           │   │  Vector  │   │          │   │            │
 │           │   │  Variant │   │          │   │            │
 │           │   │  Bare    │   │          │   │            │
 │           │   │  String  │   │          │   │            │
 │           │   │  Meaning │   │          │   │            │
 └──────────┘   └──────────┘   └──────────┘   └───────────┘

 Budget: parse safety — decremented per element,
         prevents malicious input from consuming
         unbounded memory or time
```

Comments on flowchart:
- Datomizable turns a value into a Datom tree
- Composing reconstructs a value from a Datom tree with a Budget
- The wire is type-agnostic: it carries Form-tagged data
- Six Forms: Struct (product), Vector (sequence), Variant (sum), Bare (atom), String, Meaning

### Ethos — datom-codec, full inline

```ethos
Library

[ Path.String
  Opaque                                         ; ◄─ bare kind, no payload
  Meaning.String
  FormVariant.[ Struct Vector Variant Bare String Meaning ]
  Datom.{ Form.FormVariant Path }
  Budget.Integer ]

Kinds
[ Datomizable.{ datomize }                       ; value → Datom
  Composing.{ compose }                          ; Datom + Budget → value
  Compositional.{ ARITY from_positions }         ; ◄─ 0.26.3 name
  Composable.{ compose compose_positions }
  Actualizing.{ actualize } ]
```

Note: `Compositional` became `Composing` in datom-codec 0.31.0. This is the
skew that currently blocks Lojix: signal-lojix still expects `Compositional`,
horizon-rs provides `Composing`.

### Text

1. Datom is the universal wire format — every ethos type serializes through it
2. Six Forms cover every shape: struct, vector, variant, bare, string, meaning
3. Budget is the parse safety mechanism — bounds computation during deserialization
4. Datomizable writes; Composing reads — the wire between them is type-agnostic
5. The 0.26.3→0.31.0 rename (Compositional→Composing) is the current infrastructure blocker

---

## Section 6: The Pipeline — How a Spec Becomes Real

### Imagery

A river flowing through three landscapes. The first landscape is a
mountain peak in sunlight (Psyche) — a figure stands at the summit,
sketching designs on translucent paper that the wind carries downstream.
The second landscape is a workshop valley (Mind) — the papers land on
workbenches where craftsmen build the designs into machinery, testing each
gear. The third landscape is a port city (Field) — the machinery is
installed on ships and the harbor runs. Between the landscapes, the river
carries the papers and machines. At the psyche peak, a second figure
(Fable, taller, wearing a cloak) reviews the sketches and adds annotations
in a different ink. Below the workshop, a third figure (Sonnet, smaller,
agile) takes the finished blueprints and paints them into vivid murals
on the workshop walls — these are the flashbooks.

### Flowchart

```
  ┌─────────────────────────────────────────────────────────┐
  │                    PSYCHE                                │
  │                                                          │
  │  Opus Medium ──── designs spec ──── ethos + flowchart   │
  │       │                                                  │
  │       ▼                                                  │
  │  Fable High ──── audits ──── suggestions + changes      │
  │       │                                                  │
  │       ▼                                                  │
  │  Sonnet ──── visualizes ──── vivified imagery           │
  └──────────────────────┬──────────────────────────────────┘
                         │
  ┌──────────────────────▼──────────────────────────────────┐
  │                     MIND                                 │
  │                                                          │
  │  Makes it operational ──── skill + tests                │
  │  Integrates epics ──── merge to mind branch             │
  └──────────────────────┬──────────────────────────────────┘
                         │
  ┌──────────────────────▼──────────────────────────────────┐
  │                    FIELD                                  │
  │                                                          │
  │  Deploys ──── patches ──── releases skills              │
  │  Garbage collects flows ──── one at a time              │
  │  Develops message reception during changes              │
  └─────────────────────────────────────────────────────────┘

  Review levels:
  ┌────────────────┐   ┌────────────────┐
  │ Mind-integrated│   │Psyche-reviewed │
  │ ────────────── │   │ ────────────── │
  │ Operational,   │   │ The whole idea │
  │ not reviewed   │   │ shown working, │
  │ by psyche      │   │ approved =     │
  │                │   │ Vision         │
  └────────────────┘   └────────────────┘
```

Comments on flowchart:
- The visualization pipeline (Opus → Fable → Sonnet) becomes one end-to-end skill
- Mind makes specs operational without psyche review — that's the mind-integrated level
- Psyche-reviewed means the whole idea works and psyche approved — that's a Vision landing
- Field operates independently: patches, releases skills, garbage collects
- Triad branches per repo: field branch, mind branch, psyche branch, one worktree each

### Text

1. Psyche Medium designs the ethos specification with flowcharts and imagery
2. Psyche Fable audits with suggestions and changes — the second eye
3. Sonnet visualizes — vivifies the SVG into rich imagery with integrated flowcharts
4. Mind makes the result operational — skill, tests, integration
5. Field deploys, patches, and releases without permission to keep things running
6. This whole pipeline becomes one end-to-end skill

---

## Format specification

Six sections above. Each produces one slide in the vivified flashbook.

### Responsive variants

| Layout    | Density | Description |
|-----------|---------|-------------|
| Portrait  | Low     | Phone, minimal: title + imagery + 3 key text items |
| Portrait  | Medium  | Phone, full: title + imagery + flowchart (simplified) + all text |
| Portrait  | High    | Tablet portrait: title + imagery + full flowchart + all text + ethos excerpt |
| Landscape | Low     | Small screen: imagery left, title + 3 key text items right |
| Landscape | Medium  | Medium screen: imagery left, flowchart center, text right |
| Landscape | High    | Large screen: full spread — imagery, flowchart, text, ethos all visible |

Three densities × two layouts = six format variants per section.

### Imagery rendering instructions for the low-power model

Each section's "Imagery" subsection is a complete visual description. Render
it as vivid, colorful imagery — not a dull SVG diagram. The flowchart is
integrated into the image: it lives inside the visual scene, drawn on the
surfaces described (the tablet, the workbench, the control tower board, the
pipe system, the switchboard). The flowchart's boxes become objects in the
scene. The arrows become paths, rivers, cables, pipes — whatever the imagery
describes. Text items appear as concise labels or captions beside the image,
not as separate paragraphs.

The visual style: warm, saturated, slightly stylized — like a technical
illustration in a high-end engineering magazine, not clip art or stock
photography. Every element has a clear purpose. The color palette follows the
system's theme (dark background, warm accent colors). Each slide should feel
like a page from an illuminated manuscript about infrastructure.
