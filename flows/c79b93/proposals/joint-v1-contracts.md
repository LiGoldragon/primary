# Flow and Belief: joint contract draft
Astra — read-demanding subflow supplied source and line-range evidence.

Proposed contract changes for Fable judgment; no implementation authorization. The draft incorporates the four boundary rulings and the immediate Launch acknowledgement at the data-shape level; launch event delivery and publication-path ownership remain open below. Remaining decisions below are explicitly tentative. Source snapshots: Belief origin/main 4b70b19; ordinary contract 1a8bef4; meta contract 341ea8b. Protected Flow/Herdr working trees are untouched.

## Proposed destinations and exact corrections

- psyche-belief › vision/flow-nexus-v1.md: definition Library lines 25–64 gains a harness-owned layout template; Report semantics 122–132 and Signal 243–294 gain pre-identity reporting and Launching/Started; Emission 322–349 uses Workspace/Address before identity; Memory 351–369 owns workspace-to-run correlation. Examples returning Launched.FlowId become Launching.Address followed by Started.Identity. Existing Stop/Send/Hot/Broadcast FlowId positions remain post-identification operations, rather than being mechanically renamed.
- psyche-belief › vision/belief-nexus-v1.md: introductory Signal 10–37 is replaced by the retained ordinary contract extended below; Meta 53–70 retains placement/peer ownership and loses harness/layout policy; Library 73–94 and Emission 96–107 lose Harness and use supplied Layout; examples 118–124 supply paths. Existing-domain declarations 333–430 are updated in place, rather than leaving two competing contracts. Existing ordinary native-error/preparation/checked-service specification remains unchanged.
- Flow owns harness settings and resolves its relative layout template against the selected Workspace. Layout path validation and typed refusal evidence must be completed under judgment B. Belief receives the resulting two absolute paths, owns publication/recovery, and emits workspace publication receipts. Flow consumes these receipts through its own workspace-to-run mapping.

## Proposed shared translator vocabulary
These shared kinds are proposed for both contracts from the current translator vocabulary. Flow currently pins an older Place shape; joint adoption requires the current PlaceName-based shape shown here.
```ethos
Library
[] ; imports
[ UserId.Integer
  GroupId.Integer
  ProcessId.Integer
  Caller.{ ProcessId UserId } ; kernel caller credentials
  PeerIdentity.{ UserId ProcessId } ; admitted peer process
  PeerId.String
  PeerBinding.{ PeerId PeerIdentity } ; named admission
  PlaceName.String
  Runtime.String
  State.String
  Place.{ PlaceName Runtime State } ] ; startup location
[] ; traits
[] ; associations
```

## Proposed Flow definition and identity library
The namespace is flow. Herdr Pane retains its existing definition `{ Session.String PaneId.String }`; Herdr commands and outcomes remain that component's existing contract, not Flow-owned copies.
```ethos
Library
[ :belief:[ ModuleName Workspace Layout ]
  :herdr:Pane ] ; imports
[ MetaflowName.String
  FlowName.String
  HarnessName.String
  FeatureName.String
  Effect.[ Flag.String Environment.{ Name.String Value.String } ] ; configured launch effect
  Feature.{ FeatureName Effect } ; named feature
  RelativePath.String
  LayoutTemplate.{ SystemPrompt.RelativePath Skills.RelativePath } ; resolved within a workspace
  Harness.{ HarnessName Features.Vector<Feature> LayoutTemplate } ; furnishing paths belong to Flow
  ModelName.String
  Effort.[ Low Medium High ]
  Continuity.[ Permanent Ephemeral ]
  WorkspaceChoice.[ Path.String Temporary ]
  Missing.[ Refuse Notice ]
  Beliefs.{ Vector<ModuleName> Missing } ; missing-module policy belongs to the definition
  Tool.String
  Tools.[ HarnessDefault Restricted.{ Allow.Vector<Tool> Deny.Vector<Tool> } ] ; harness-enforced capabilities
  Route.[ Speaks.FlowName Metaflow.MetaflowName Living ]
  Member.{ FlowName HarnessName ModelName Effort Continuity WorkspaceChoice
           Beliefs Tools Features.Vector<FeatureName> Vector<Route> } ; one definition
  Metaflow.{ MetaflowName Vector<Member> Speaker.FlowName } ; one replaceable definition
  ComplexName.String
  Host.String
  Relationship.{ From.MetaflowName To.MetaflowName } ; permitted inter-metaflow route
  Complex.{ ComplexName Metaflows.Vector<MetaflowName>
            Relationships.Vector<Relationship> Features.Vector<FeatureName>
            Instances.Vector<Host> Speaker.MetaflowName } ; one replaceable definition
  Address.{ MetaflowName FlowName } ; one live run at this address
  FlowId.String
  NativeSession.String
  Identity.{ ComplexName Address FlowId } ; known after the first Report
  Roster.Vector<Address>
  RosterChange.[ Started.Address Stopped.Address ]
  Brief.String
  Priority.[ HardAbrupt MiddleAbrupt Soft ]
  Request.[ Order.String Question.String
            Living.{ Context.String Verbatim.String }
            Result.String Notice.String ] ; message content
  Sender.[ Flow.FlowId Living Nexus ]
  Message.{ Priority Sender Request } ; delivered message
  Waking.Vector<Message>
  Name.[ Metaflow.MetaflowName Harness.HarnessName Complex.ComplexName ]
  Event.[ Started Idle Working Ended Responded.String Warned Threshold ]
  Report.{ Address Pane NativeSession Event } ; caller/pane checked; first report establishes FlowId
  Threshold.{ ModelName Tokens.Integer Warning.Integer } ] ; per-model context policy
[] ; traits
[] ; associations
```

## Proposed Flow ordinary Signal
The default modules and thresholds remain meta values. Report has the native facts; the model need not invent its FlowId to report its start.
```ethos
Signal
[ :flow:[ Metaflow MetaflowName FlowName FlowId Address Brief
          Request Priority Harness HarnessName FeatureName Complex ComplexName
          Name Report Identity NativeSession ]
  :belief:ModuleName ] ; imports
[ Define.[ Metaflow Harness Complex ]
  Undefine.Name
  Describe.Name
  Definitions
  Launch.{ MetaflowName FlowName Brief }
  Rehearse.{ MetaflowName FlowName Brief }
  Stop.FlowId
  Send.{ FlowId Address Priority Request }
  Say.{ ComplexName Request }
  Hot
  Broadcast.Request
  Report
  Adopt.{ Address NativeSession }
  Subscribe ] ; inputs
[ Defined.Name
  Undefined.Name
  Described.[ Metaflow Harness Complex ]
  Listed.Vector<Name>
  Launching.Address
  Started.Identity
  Rehearsed.Command.String
  Stopped.FlowId
  Sent.[ Delivered Queued ]
  Said.[ Delivered Queued ]
  Hot.Vector<FlowId>
  Broadcast.Vector<FlowId>
  Reported.FlowId
  Adopted.FlowId
  Subscribed
  Refused.[ UnknownMetaflow.MetaflowName UnknownHarness.HarnessName
            UnknownComplex.ComplexName UnknownFlow.FlowName
            NoRoute.{ FlowId Address } NoBelief.Vector<ModuleName>
            Unenforceable.HarnessName UnknownFeature.{ HarnessName FeatureName }
            HerdrDown BeliefDown Running.Address AddressHeld.FlowId
            Unidentified ] ] ; outputs: Started is a pushed reaction
[] ; local types
```
Launch answers Launching.Address immediately after admitting the attempt. Started.Identity follows first valid Report. A queued/working launch is represented by Address and, once created, Pane. Source of FlowId is the native session; caller identity is verified, not trusted from payload text.

## Proposed Flow meta Signal
```ethos
Signal
[ :belief:ModuleName
  :flow:Threshold ] ; imports
[ Configure.Set ] ; inputs
[ Configured.Set ] ; outputs
[ Set.[ DefaultModules.Vector<ModuleName> Threshold ] ] ; one value per request
```

## Proposed Flow emission boundary and Memory identity
These declarations show the corrected boundary facts. Existing Herdr inputs/outcomes are consumed by the translator as binary signal. Full launch mechanics and terminal failure replies remain open below.
```ethos
Emission
[ :flow:[ Member Address FlowId Brief Waking Roster RosterChange Identity ]
  :belief:[ Workspace Layout ModuleName FurnishRequest Response ]
  :herdr:[ Pane Outcome ] ] ; imports
[ Furnish.FurnishRequest
  Settle.{ Workspace Member }
  Open.{ Member Address }
  Introduce.{ Pane Identity Roster Brief }
  Wake.{ Pane Waking }
  Tell.{ Pane RosterChange }
  Close.{ Pane Workspace } ] ; one typed external call per emission
[ Furnished.Response
  Settled.Outcome
  Opened.{ Pane Outcome }
  Introduced.Outcome
  Woken.Outcome
  Told.Outcome
  Closed.Outcome ] ; observed outcomes
[] ; local types
```
Open carries the member and its already-known Address; it contains no FlowId. FurnishRequest is Workspace, Layout, and module names. The existing Flow example `Furnish.{ Member FlowId }` is replaced rather than retained as a second path.
```ethos
Memory
[ :flow:[ Address Identity ]
  :belief:[ Workspace FurnishedWorkspace ]
  :herdr:Pane ] ; imports
[ Run.[ Preparing.{ Address Workspace }
        Opened.{ Address Workspace Pane }
        Identified.{ Identity Workspace Pane } ] ; identity evolves with observed facts
  FurnishedWorkspace ] ; workspace publication drives this Nexus's refresh mapping
```
Memory above is the correlation portion; existing definitions, queues and thresholds remain. A furnished receipt already names its workspace and is stored as that receipt.

## Proposed Belief ordinary contract
This extends the existing publication identities and applicable failure evidence; changed path ownership still requires a coherent recovery design. Directory-source additions are tentative pending the source-identity ruling below. Layout is supplied; no harness name crosses this boundary.
```ethos
Signal
[ :translator:[ Caller PeerBinding UserId PeerId ] ]  ; imports: shared authenticated identity
[ Register.ModuleSource                                ; inputs: repository and workspace effects
  Resolve.Vector<ModuleName>
  Furnish.FurnishRequest
  Subscribe ]
[ Registered.SourceState                         ; outputs: one answer, then subscribed updates
  Resolved.Resolution
  Furnished.FurnishedWorkspace
  Subscribed.Vector<FurnishedWorkspace>
  Changed.FurnishedWorkspace
  RefurnishFailed.RefurnishFailure
  CleanupFailed.CleanupFailure
  SubscriptionClosed.CloseReason                     ; terminal event on the subscribed connection
  MemoryAfterPublication.MemoryAfterPublication
  Refused.Refusal ]
[ Kind.[ Spirit Intent Vision Knowledge Role ]       ; types: a module name is its folder kind and subject
  Subject.String
  ModuleName.{ Kind Subject }
  RepositoryPath.String
  DirectoryPath.String
  Directory.DirectoryPath
  ModuleSource.[ Repository Directory ]
  Repository.RepositoryPath
  WorkspacePath.String
  Workspace.WorkspacePath
  RelativePath.String
  SourceRevision.String ; tentative Directory content-identity semantics: judgment A
  PublicationRevision.Integer
  GenerationId.String
  Path.String
  Layout.{ SystemPrompt.Path Skills.Path }
  Owner.[ Login.UserId Peer.PeerId ]                 ; durable authority, separate from Caller provenance
  SourceState.{ ModuleSource SourceRevision } ; tentative for Directory, pending judgment A
  Found.ModuleName
  Resolution.{ Vector<Found> Vector<ModuleName> }
  FurnishRequest.{ Workspace Layout Vector<ModuleName> }
  Placement.[ SystemPrompt Skills ]                  ; where one module is furnished
  FurnishedWorkspace.{ Workspace GenerationId PublicationRevision Layout Vector<Found> Vector<ModuleName> }
  ExecutablePath.String
  ContractDigest.String
  PeerList.Vector<PeerBinding>
  Call.{ Caller Query }                                ; Query is the Signal root's generated input enum
  SourceOperation.[ Registering Snapshotting Resolving Watching ]
  FileOperation.[ Reading Staging Linking Replacing Inspecting Cleaning ]
  MemoryOperation.[ Loading Recording BeginningPublication CompletingPublication
                    AfterPublication Recovering ]
  ExitStatus.Integer
  Diagnostic.{ ExecutablePath Option<ExitStatus> String }
  InvalidPlacement.[ Unknown.String NonScalar Duplicate ]
  InvalidModule.{ ModuleName RelativePath InvalidPlacement }
  SourceEvidence.[ NotRepository MainUnavailable RevisionUnavailable
                   InvalidModule
                   Ambiguous.{ ModuleName Vector<ModuleSource> }
                   Translator.Diagnostic ]
  SourceFailure.{ ModuleSource SourceOperation SourceEvidence }
  FileEvidence.[ OutsideBoundary.{ RelativePath RelativePath }
                 PermissionDenied
                 MissingRequired.RelativePath
                 Conflict.{ Option<PublicationRevision> Option<PublicationRevision> }
                 Translator.Diagnostic ]
  FileFailure.{ Workspace FileOperation FileEvidence }
  MemoryEvidence.[ Unavailable Corrupt Conflict ]
  MemoryFailure.{ MemoryOperation MemoryEvidence }
  RefusalKind.[ Source File Memory NotAuthorized SubscriberCapacityReached NotReady ]
  RefurnishFailure.{ Workspace RefusalKind }
  CleanupFailure.{ Workspace GenerationId PublicationRevision FileFailure } ; successful publication after which target cleanup failed
  CloseReason.[ QueueOverflow WriteTimeout ]
  MemoryAfterPublication.{ Workspace GenerationId PublicationRevision MemoryFailure }
  Refusal.[ Source.SourceFailure
            File.FileFailure
            Memory.MemoryFailure
            NotAuthorized.Caller
            SubscriberCapacityReached.Integer
            NotReady ] ]

```

## Proposed Belief meta contract
Harness-independent publication storage replaces per-harness settings/layout ownership. This replacement is tentative pending the publication-link ruling below; the other current meta values, CAS and readiness are retained. Publication recovery will be reclosed against the chosen path ownership.
```ethos
Signal
[ :signal_belief_nexus:[ PeerList RelativePath ExecutablePath
                          Kind Placement Owner ]
  :translator:[ Caller UserId GroupId ProcessId Place ] ]             ; imports
[ Configure.ConfigureRequest ]                       ; inputs: set one field; an expected revision makes it conditional
[ Configured.ConfiguredState                         ; outputs: the one coherent configuration revision
  ConfigureRefused.ConfigurationRefusal ]
[ Keeper.[ Nexus Translator ]                        ; types
  ConfigurationRevision.Integer
  SettingName.[ RepositoryPolling SubscriberCapacity OrdinaryPeers MetaPeers PublicationLayout Placement.Kind GenerationRetention
                NexusFrameCapacity NexusTransportTimeout NexusSocket MetaNexusSocket
                CallTimeout OutputLimit TextBudget TranslatorFrameCapacity
                TranslatorTransportTimeout AllowedNexusPeers GitExecutable ]
  Readiness.[ Awaiting.Vector<SettingName> Ready ]
  Timeout.Integer
  ByteLimit.Integer
  NodeLimit.Integer
  DepthLimit.Integer
  Budget.{ NodeLimit DepthLimit }
  SocketPath.String
  OrdinarySocket.SocketPath
  MetaSocket.SocketPath
  OrdinaryTranslatorSocket.SocketPath
  MetaTranslatorSocket.SocketPath
  OrdinaryNexusSocket.SocketPath
  MetaNexusSocketPath.SocketPath
  EmissionTranslatorSocket.SocketPath
  MemoryFileName.String
  OwnedRoot.RelativePath
  GenerationsDirectory.RelativePath
  CurrentLink.RelativePath
  PositiveInteger.Integer
  RetentionPolicy.[ KeepAll KeepPrevious.PositiveInteger ]
  PublicationLayout.{ OwnedRoot GenerationsDirectory CurrentLink }
  PlacementDefault.{ Kind Placement }
  Set.[ RepositoryPolling.Timeout
        SubscriberCapacity.Integer
        OrdinaryPeers.PeerList
        MetaPeers.PeerList
        PublicationLayout
        Placement.PlacementDefault
        GenerationRetention.RetentionPolicy
        NexusFrameCapacity.ByteLimit
        NexusTransportTimeout.Timeout
        NexusSocket.SocketPath
        MetaNexusSocket.SocketPath
        CallTimeout.Timeout
        OutputLimit.ByteLimit
        TextBudget.Budget
        TranslatorFrameCapacity.ByteLimit
        TranslatorTransportTimeout.Timeout
        AllowedNexusPeers.PeerList
        GitExecutable.ExecutablePath ]
  ConfigureRequest.{ Option<ConfigurationRevision> Set } ; None is unconditional; Some is compare-and-set
  ConfiguredState.{ Set Keeper ConfigurationRevision Readiness }
  TranslatorConfiguration.{ ConfigurationRevision Vector<Set> Readiness }
  Invalid.{ Keeper SettingName String }
  StaleRevision.{ Option<ConfigurationRevision> ConfigurationRevision }
  ConfigurationRefusal.[ Invalid
                         StaleRevision
                         NotAuthorized.Caller
                         Unavailable ]
  MetaCall.{ Caller Query }
  MetaTransportInput.[ Call.MetaCall RestoreTranslatorConfiguration ]
  MetaTransportOutput.[ Answered.Response
                         Restored.TranslatorConfiguration
                         RestoreRefused.ConfigurationRefusal ]
  Admission.{ ByteLimit Timeout }
  PairedProcess.{ UserId GroupId ProcessId }
  PairedTranslator.{ UserId GroupId ProcessId }
  BootstrapOwner.Owner
  NexusBootstrap.{ OrdinarySocket MetaSocket EmissionTranslatorSocket Place MemoryFileName
                    Admission PairedTranslator BootstrapOwner }
  TranslatorBootstrap.{ OrdinaryTranslatorSocket MetaTranslatorSocket
                         OrdinaryNexusSocket MetaNexusSocketPath Admission PairedProcess }
  Bootstrap.[ Nexus.NexusBootstrap Translator.TranslatorBootstrap ] ]

```

## Proposed Belief emission contract
Settings-file effects move to Flow; generation/manifest and cleanup evidence remain Belief’s. Directory source evidence needs the exact additional variants decided below.
```ethos
; Proposed executable shape retains the current generator-supported Signal root.
; The conceptual Emission root remains a separate generator capability question.
Signal
[ :signal_belief_nexus:[ Layout ModuleName Placement ModuleSource SourceState Workspace RelativePath
                          SourceRevision PublicationRevision GenerationId Diagnostic FileFailure ]
  :meta_signal_belief_nexus:[ PublicationLayout RetentionPolicy ConfigurationRevision TranslatorConfiguration ] ] ; imports
[ Snapshot.ModuleSource                                 ; emissions: read one immutable main snapshot
  Publish.Publication                                 ;   or atomically replace one owned publication
  InspectPublication.InspectionRequest                ;   or observe owned recovery evidence
  Clean.CleanupRequest ]                              ;   or remove proven-owned superseded generations
[ Snapshotted.SourceSnapshot                          ; outcomes
  Published.PublicationState
  Inspected.PublicationInspection
  Cleaned.CleanupState
  CleanupRefused.FileFailure
  EmissionRefused.EmissionRefusal ]
[ EmissionAttempt.{ ConfigurationRevision TranslatorConfiguration Query } ; one immutable attempt snapshot
  EmissionAttemptOutcome.{ ConfigurationRevision Response } ; response revision equals its attempt
  Content.String                                      ; types
  AbsolutePath.String
  ModuleContent.{ ModuleName RelativePath Option<Placement> Content }
  SourceSnapshot.{ ModuleSource SourceRevision Vector<ModuleContent> }
  SkillFile.{ RelativePath Content }
  WorkspaceImage.{ Layout PublicationLayout Content Vector<SkillFile> }
  SourceStates.Vector<SourceState>
  FoundModules.Vector<ModuleName>
  MissingModules.Vector<ModuleName>
  PriorPublication.Option<PublicationRevision>
  IntendedPublication.PublicationRevision
  PublicationManifest.{ GenerationId IntendedPublication SourceStates
                         FoundModules MissingModules }
  Publication.{ Workspace GenerationId PriorPublication IntendedPublication
                 WorkspaceImage SourceStates FoundModules MissingModules RetentionPolicy }
  PublicationIdentity.{ GenerationId PublicationRevision }
  PublicationState.{ Workspace PublicationIdentity }
  InspectionRequest.{ Workspace PublicationIdentity Layout PublicationLayout }
  PublicationInspection.{ Workspace Option<PublicationIdentity> Option<PublicationManifest> }
  CleanupRequest.{ Workspace PublicationIdentity Layout PublicationLayout }
  CleanupOutcome.[ Removed AlreadyAbsent ]
  CleanupState.{ Workspace PublicationIdentity CleanupOutcome }
  SourceOperation.[ ReadingMain ReadingTree ] ; repository vocabulary; Directory variants await judgment A
  PublicationOperation.[ StagingGeneration WritingManifest
                          ReplacingPointer InspectingPointer InspectingManifest ]
  InvalidPlacement.[ Unknown.String NonScalar Duplicate ]
  InvalidModule.{ ModuleName RelativePath InvalidPlacement }
  SourceEvidence.[ NotRepository MainUnavailable RevisionUnavailable InvalidModule Translator.Diagnostic ]
  SourceRefusal.{ ModuleSource SourceOperation SourceEvidence }
  BoundaryRoot.AbsolutePath
  BoundaryCandidate.AbsolutePath
  BoundaryEvidence.{ BoundaryRoot BoundaryCandidate }
  ExpectedRevision.Option<PublicationRevision>
  ObservedRevision.Option<PublicationRevision>
  RevisionEvidence.{ ExpectedRevision ObservedRevision }
  PublicationEvidence.[ OutsideBoundary.BoundaryEvidence
                         DestinationUnavailable.AbsolutePath
                         PriorRevisionMismatch.RevisionEvidence
                         OwnedPointerMismatch
                         ManifestMismatch
                         PermissionDenied
                         Translator.Diagnostic ]
  PublicationRefusal.{ Workspace PublicationOperation PublicationEvidence }
  EmissionRefusal.[ Source.SourceRefusal Publication.PublicationRefusal ] ]

```

## Exact retained behavior and open judgments

- Retained: ordinary preparation preserves native codec errors and checked execution owns native failure evidence, as already specified in vision:belief-nexus-v1. Subscribe and meta remain separate paths. The design draft does not replace these in-process Rust types with serializable diagnostic strings.
- Retained: Belief Subscribe yields initial furnished-workspace receipts, then Changed.FurnishedWorkspace and its existing typed failure/closure messages. Flow subscribes, correlates Workspace to its run, and applies the existing refresh policy; Belief neither names nor stops a flow.
- Retained: sources may be ambiguous; existing typed Ambiguous evidence reports that state. No new implicit source precedence is introduced.
- Judgment A (tentative): Directory registration/furnishing reads a standing directory without a watcher. Propose an immutable per-attempt snapshot, with SourceRevision naming that snapshot's content; exact content identity and directory-specific SourceEvidence/SourceOperation variants remain to be settled together. The proposed ModuleSource extension is not frozen without these.
- Judgment B (tentative): Flow owns the two public paths and harness settings. The shown PublicationLayout is a proposed private-generation storage setting, NOT an approved boundary ruling: decide whether Belief may configure this private storage, or whether all path policy belongs to Flow. It is distinct from the removed harness layout. Public paths must be safely connected to the one atomic current generation, with typed ownership/refusal evidence. Decide whether public-link creation is part of Belief publication or separately performed by Flow; atomic publication/recovery must remain one design.
- Judgment C: Flow's immediate Launching acknowledgement requires a terminal pushed failure for a launch that fails before first Report. Define its typed phase/evidence, rather than using HerdrDown or BeliefDown as a late uncorrelated reply. Startup timeout/cancellation and the client that receives these events require explicit contract lines.
- Judgment D: the loaded Harness definition names features but has no executable/argument template describing model, effort, hook/report installation, tools enforcement or initial identity delivery. Settle its configuration vocabulary before a no-hardcoded-harness implementation is admitted. Introduce currently assumes the harness can start and Report before the full initial prompt; that capability must be declared or the launch protocol amended.
- Judgment E: pre-identity address/pane state needs explicit observer/adoption semantics during Nexus replacement; current Hot.Vector<FlowId> names identified flows only. Decide the opening-state observation and recovery contract instead of losing an admitted launch.
- Unknown: generator support for true Emission/Memory roots and generic native-error traits. These are lowering questions; the supplied native-error Rust contract remains specified.

## Scope and ownership

This is design source only. No canonical repository edits, workers, publication reservations, deployments or protected-branch reconciliation are authorized. Existing joint design owner: this Astra flow; choreography: Mind flowNexus Sol. Core/Field/Herdr respondents reported no current v1 draft or implementation owner; their statements do not release foreign claims. Fresh narrowly composed implementation flows begin only after Fable judges the finished contract.
