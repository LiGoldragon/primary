# Flow Nexus anatomy: types and traits, defined and missing

Ordered by the main flow of 9519a1. One inventory of every type and trait the Flow Nexus needs across Library, Signal (ordinary and meta), Operation and Memory, by section, with what is defined in ethos and what is missing.

Marks. **W**: witnessed by this subflow, by reading the file at the named commit. **C**: a claim relayed from another flow's report, here always the records catalogue, with that flow's own W/I mark. **I**: this subflow's inference. Every table row of a defined type is W unless marked otherwise.

`FLOW_ID` and `FLOW_DIRECTORY` were empty in this subflow's environment; no PROVENANCE receipt was handed over, so no receipt handle is available.

## 0. What was read, in order

Short names used below.

| short | repository, branch, commit (date) | file |
|---|---|---|
| op | flow `main` 962ad12 (10-10) | crates/flow-nexus/ethos/operation.ethos |
| lib | flow `field/storepath-flow-9bdf3cd3cf64` 074437a (10-10 07:18), newest | crates/flow-ethos/ethos/library.ethos |
| nlib | same branch | crates/flow-nexus/ethos/library.ethos |
| sig | signal-flow `field/signal-aspect-store-e3ddf94ed9bb` d1358d3 (10-10 07:28), newest | ethos/signal.ethos |
| meta | meta-signal-flow `field/meta-aspect-store-1a1258b9873b` 6d07b7b (10-10 07:46), newest | ethos/signal.ethos |
| nx | nexus `field/nexus-process-implementation-b8b7688ddea9` eafe26a (10-12), newest | ethos/library.ethos |
| mmem, mop | message `field/message-memory-operation-746519b9b4c8` 87029e4 (10-10), newest | crates/message-nexus/ethos/memory.ethos, operation.ethos |
| b4 | «Flow, whole, in ethos, fourth edition», https://claude.ai/artifact/FNVZ9Lo9QXA5z4DRpW1zfM, version 1791822797-c881 | line numbers from its local source flows/875960/books/7-flow-whole-ethos-4.md; its 7 ethos blocks are byte-identical to the artifact's (compared by script, W) |
| des | Primary `origin/main` a589015 (file last changed 2d0a119, 10-10) | flows/f5a6e9/reports/flow-buildable-design.md |
| vf, vn, ve, vsig, vsema, vp | psyche-skills `origin/main` 5a18f9c (10-12) | skills/vision-flow.md, vision-nexus.md, vision/ethos.md (the vision-ethos source; there is no skills/vision-ethos.md), vision-signal.md, vision-sema.md, vision-persona.md |
| cat | Primary working tree, 845503 | flows/9519a1/reports/flow-ethos-records.md (searched: sections 1.1 and 1.2 read, section 3 not) |

The other branches, read and compared (W):

- flow: `operation.ethos` is the same file (same checksum) on main and all five field branches. `library.ethos` on `field/flow-storepath-source-fa8a85c44fba` 6bfbbfb differs from lib only in keeping two aspects (`FlowAspect.[ Psyche Mind Field ]` beside `Aspect`, `MetaAspects.Vector<FlowAspect>`). `field/flow-ethos-compile-6aa881f125da` 6aa881f and `field/flow-ethos-generation-41c6f836f9e9` a317334 are identical to each other: no Reason, StorePath, StoreRefusal, StartRefusal; `Start.{ OrdinarySocketPath MetaSocketPath }`. `field/flow-ethos-generation-fc358a5484cc` fc358a5 inlines `Source.{ Repository.String Hash.Blake3 Path.String }`. nlib exists only on the two storepath branches. flow `main` has no library.ethos.
- signal-flow: `main` 068f0ea (SignalFlow 11) declares its own FlowId, ModelName, FlowAspect, HarnessKind, has no Lock, Bind, Identify, Deliver, Release, End, Current, Metaflows, and refuses only `Refused.[ UnknownFlow.FlowId ]`. `field/storepath-signal-flow-7716894114fb` e69fdad and `field/signal-flow-leaf-8d6317564261` a991c14 are identical: they import `FlowAspect` (which lib no longer has) and keep `List`/`FlowList`/`ListRejection`; sig drops List, answers `Listed.Vector<Metaflow>`, adds `Refusal.Store.String`.
- meta-signal-flow: `main` 88f3759 has the older whole-Configuration `Configure.ConfigureRequest`, `FlowAspect`, `Activation.[ NexusRestartRequired ]` and declares the setup field types itself. `field/storepath-meta-signal-flow-47442fbc4ba7` 2d29532 and `field/meta-flow-leaf-422c75bbde1a` 991859f are identical to each other and precede meta.
- nexus: `main` c495f2a has no ethos file. `field/nexus-process-9fa56596749e` 9fa5659 has the same library.ethos as nx.
- message: `main` 6fa4d0c has no ethos file.

## 1. Library (flow-ethos crate)

### 1.1 Defined (lib, W)

Imports: none (L6). Traits: none (L72). Associations: none (L73).

| type | line | what it is for |
|---|---|---|
| FlowId.String | 7 | a flow's id |
| Topic.String | 9 | topic name; comment L8: `Topic:Name` not expressible in ethos-zero 16, camelCase checked at input |
| Blake3.String | 11 | comment L10: designed as `Bytes<32>`, carried as 64 hex characters |
| Layer.[ Primary Secondary Tertiary Quaternary ] | 12 | decides the model |
| Subaspect.[ Vision Intent Knowledge Operation Trial Compensation ] | 13 | a module's kind |
| Repository, Hash.Blake3, Path, Reason | 16-19 | Source's fields; Reason is StoreRefusal's |
| Source.{ Repository Hash Path } | 20 | where a module's text lives |
| Key.{ Subaspect Topic } | 21 | a module's key |
| Said.{ Context.String Verbatim.String } | 22 | the living's words, relayed |
| Request.[ Order Question Psyche.Said Psyches.Vector<Said> Result Notice ] | 23-28 | what reaches a metaflow |
| Aspect.[ Psyche Mind Field ] | 29 | one Aspect, shared by addresses, profiles and meta configuration (L2-3) |
| Address.{ Aspect Topic Layer } | 30 | names a metaflow |
| Recipient.[ Address Up ] | 31 | where a request goes |
| Metaflow.{ Address State.[ Awake.FlowId Asleep Ended ] Past.Vector<FlowId> Queue.Vector<Request> } | 32-35 | one per address |
| Lock.{ Sender Address Until.Integer } | 36 | Flow's time-bound lock |
| Process.{ Pid.Integer Started.Integer } | 37 | the calling process |
| Sender.Address | 38 | a Lock's sender |
| OrdinarySocketPath, MetaSocketPath, StorePath | 39-41 | start inputs |
| Start.{ OrdinarySocketPath MetaSocketPath StorePath } | 42 | the start datom |
| StoreRefusal.{ Path Reason }, StartRefusal.[ Store.StoreRefusal ] | 44-45 | the start refusal |
| SourceRoot, ClientPath, Home, ControlSocketPath, ModelName | 46-50 | setup fields |
| CodexEndpoint.{ ClientPath Home ControlSocketPath Vector<ModelName> }, StableCodex, NextCodex | 51-53 | the two Codex app-servers |
| HarnessKind.[ Codex Claude ] | 54 | how a flow is driven |
| KeyName, CommandSigil, InterruptKeys, SubmitKeys, HarnessProfile, HarnessProfiles | 55-60 | per-harness key profile |
| MetaAspects.Vector<Aspect> | 61 | who may use the meta socket |
| MessageNexusPath, MessageNexusBinary | 62-63 | Message's socket and executable identity |
| Nexus.{ SourceRoot StableCodex NextCodex HarnessProfiles MetaAspects MessageNexusPath MessageNexusBinary Lease.Integer } | 64-71 | the Nexus's setup payload; Lease is lock seconds, 60 by default |

nlib (L4): a second `Start.{ OrdinarySocketPath.String MetaSocketPath.String StorePath.String }` in the flow-nexus crate itself, comment L1-2: process identity at startup, not durable settings.

### 1.2 The shared nexus library (nx, W)

| type or trait | line | what it is for |
|---|---|---|
| Pid.Integer, Started.Integer | 9-10 | Started is /proc stat field 22, clock ticks since boot (L2) |
| Process.{ Pid Started } | 11 | a process identity |
| Ancestry.Vector<Process> | 12 | the caller first, namespace init last |
| Unidentified.[ PeerMismatch Vanished Reused Malformed ] | 13-17 | why a claimed chain cannot be trusted |
| trait Identifiable.[ identify.[ Result<Ancestry Unidentified> ] ] | 19-20 | re-observe a process and its whole parent chain |
| association Process.[ Identifiable ] | 22 | Process bears it |

This is the only trait declared in any ethos file of the five repositories, on any branch read (W).

### 1.3 Proposed (b4 L59-292)

Imports L63-64: `protos:Coinage`, `nexus:[ Instant Process ]`.

Types: Hash.Bytes<32> (L65), FlowId.Hash (L66), Topic.protos:Coinage (L69), Aspect, Layer, Address, Said, Request, Recipient (L71-97), Verdict.[ Wake.Layer Stay ] (L98-100), Lock.{ Address Until.Instant } (L101-103), Subaspect.[ Spirit Intent Vision Knowledge Operation Compensation Trial ] (L104-111), Key, Source.{ Repository.String Hash Path.String }, Module.{ Key Source } (L112-121), Effort.[ High Medium Low ] (L122-125), Model.{ Layer Harness.HarnessKind Native.String Effort } (L126-130), Threshold.{ Layer Handover Refresh } (L131), Event.[ Started ToolUsed.String ContextMeasured.{ Tokens Window } Stopped ] (L135-141), Notification.[ Entered.{ Address Request } Woken.{ Address FlowId } Refreshed.{ Address FlowId } Idled.Address ] (L142-152), Metaflow.{ Address State.[ Awake.FlowId Idle ] Modules.Vector<Key> Past Queue } (L153-160), Flow.{ FlowId Process Events.Vector<Event> } (L161-164), Refusal.[ Unknown.[ Address FlowId Key ] Awake.FlowId Idle Refreshing NoLayer NotConfigured HashMismatch OffRoute NoneAbove Unidentified.Process Taken.Address Store.[ NotOwn Unopenable Unwritable ] ] (L165-183).

Traits (L189-272) and what each is for, per its comment:

| trait | line | capabilities | for |
|---|---|---|---|
| Encodable | 189 | encode.[ String ], decode:{ [ String ] [ Result<Self Refusal> ] } | one bare run in datom, bytes in memory |
| Rememberable | 195 | complex: associated type Previous, constant VERSION, change!, upgrade: | the memory kind: standard change and upgrade from the former version |
| Identifiable | 206 | identify.{ [ Process ] [ Result<Address Refusal> ] }, bind! | who calls, from the process alone |
| Lockable | 215 | grant!{ [ Instant ] … }, free!, lapse! | Flow's own lock |
| Wakeable | 222 | judge., wake!, queue!, drain!, idle! | idling and waking |
| Lineal | 235 | launch!, refresh!, reap! | one run after another |
| Composable | 248 | compose., check. | modules into a prompt, hash check |
| Observable | 257 | report!, subscribe., notify. | state by subscription |
| Configurable | 263 | configure!, forget! | over the meta socket only |

Associations (L277-292): Hash, FlowId bear Encodable; Metaflow bears Lockable, Wakeable, Lineal, Observable, Rememberable; Flow bears Observable, Rememberable; Module bears Composable, Rememberable; Model, Threshold, Lock bear Rememberable; Nexus bears Configurable, Rememberable.

### 1.4 Design (des L16-184)

Library imports CodexEndpoint and HarnessProfile from meta_signal_flow (L17-21). Types as lib, with these differences: Topic:Name (L26), Blake3.Bytes<32> (L30), Lock.Until seconds since epoch (L93), Nexus declared once in Library (L112-125). No traits or associations in the block (L126-127); Encodable is given in prose (L169-177) and attributed to vision-datom.

### 1.5 Missing in the Library

| missing | named by | note |
|---|---|---|
| any trait in lib | ve L43-45, L361-365; vn L25; cat R1186, R1174, R1183 (C, I) | lib's trait and association sections are empty (W) |
| Instant | b4 L64, L103, L217 imports `nexus:Instant` | nx has no Instant on any branch; no `Instant` in any nexus ethos (W, by grep across all remote branches) |
| Coinage, the judged identifier | b4 L63, L69; vf L20, L32 | no Coinage, Moniker or Instant in any protos branch (W, by grep); the word check is not a type or trait anywhere |
| Bytes<N> intrinsic, Hash as a non-alias type | des L30, L183; b4 L65 | not expressible in ethos-zero today, per lib L10 and b4's closing note (C from those files) |
| HarnessKind in b4's Library | b4 L128 uses Harness.HarnessKind | b4's Library neither defines nor imports HarnessKind (W) |
| Nexus in b4's Library | b4 L291 associates Nexus | Nexus is declared in b4's meta Signal (L373), which the Library does not import (W) |
| CodexEndpoint, HarnessProfile in b4 | b4 L353-356, L373-380 import them from meta_signal_flow, the meta Signal's own crate | defined in no b4 block; defined in lib L51, L59 (W) |
| a fingerprint/identity trait | vn L25: "an encoded form fingerprints itself, by default the hash of its rkyv archive" | no trait in any source (W); Encodable is not it (I) |
| executable identity of a process | des L741-746, L762-768; sig L78-82 (Message gate compares the executable) | nx carries Pid and Started only; MessageNexusBinary is a String (W) |
| boot identity | nx L3-4: a persisted binding must be invalidated when the boot changes | no Boot type in nx or lib (W) |
| word-id codec / hash-based FlowId | vf L20; des L954-955; cat R0942, R1101, R1181 (C) | FlowId.String in lib; FlowId.Hash only in b4 |
| shared Source library or Source Nexus | cat R0984, R0987, R0988, R0999 (C) | Source and Key are Flow's own in lib L20-21 (W) |
| Role subaspect | cat R1100 (C, I) | no Role in any Subaspect (W) |

## 2. Signal, ordinary socket (signal-flow)

### 2.1 Defined (sig, W)

Imports L103: from flow_ethos, Aspect Address FlowId Request Lock Sender Process Metaflow Key Recipient Layer Topic Subaspect Source OrdinarySocketPath MetaSocketPath Start ModelName HarnessKind.

Queries (L104-121): Start.StartRequest, Restart.RestartRequest, ResolveRecipient, Stop.FlowId, Replace.StartRequest, LaunchStatus.LaunchRequestId, Observe.ObserveSelection, ResolveCaller.Option<FlowId>, QueueTurnEnd.TurnEndRequest, Report.{ FlowId Event }, Lock.{ Sender Recipient }, Bind.{ Address Process }, Identify.Process, Deliver.{ Lock Request }, Release.Lock, End.Address, Current.Address, Metaflows.

Responses (L122-152): Started.Launched, LaunchPending, StartAmbiguous, Restarted, RecipientResolved.FlowNode, Stopped, Listed.Vector<Metaflow>, eight *Rejected variants, Replaced, LaunchInspected, CallerResolved.Caller, AgentObserved, TurnEndQueued, Reported, Locked.Lock, Bound.FlowId, Identified.Address, Delivered, Queued, Woken.FlowId, Released, Ended, Current.[ Awake.FlowId Asleep Ended Unknown ], Refused.Refusal.

Types (L153-281), grouped by purpose:

| group | lines | types |
|---|---|---|
| ids and scalars | 154-185 | SessionId, TurnId, FlowType, Generation, EndpointPath, Herdr* names and ids, LaunchRequestId, SourcePath, SourceSha256, SkillName, Effort.String (168), RememberingDepth, prompt and receipt hashes, transcript device/inode/offset, NativeSkillPath/Sha256 |
| launch pipeline | 186-212 | PowerLevel.[ High Medium Low UltraLow ] (186), LaunchSource, RememberedFlow, LaunchProfile (189), TargetReceiptRequest, FirstPromptPayload, ComposedLaunch, HerdrPaneBinding (193), NativeLaunchIntent, NativeLaunchBinding, RegistrationAcknowledgement, NativeTranscript{Cursor,Absence,Boundary}, NativeSkillSelection, PromptDeliveryIntent, NativeTargetReceipt, PromptDeliveryResult, LaunchAttemptPhase, LaunchAttempt (207), LaunchStatusOutcome, LaunchInspection, LaunchAttemptReservation |
| requests and routes | 213-227 | OriginClue, StartRequest, RestartRequest, RecipientResolutionRequest, StopRequest, RouteReadiness, EndpointSelection, HerdrRoute, HerdrRouteSelection, FlowLifecycle.[ Pending Active Stopped Retired Exited ] (224), FlowNode (225), Launched, Restarted |
| rejections | 238-262 | BindingRefusal, StartRejection, RestartRejection, RecipientResolutionRejection, StopRejection, ReplaceRejection, LaunchStatusRejection, CallerResolutionRejection, TurnEndRejection |
| observation | 250-253 | ObserveSelection.[ Launch Agent ], AgentState.[ Idle Working Blocked Done Unknown Gone ], AgentObservation |
| caller | 255 | Caller.{ FlowId Aspect PowerLevel ModelName } |
| book | 258-259 | Title.String, Presentation.{ Title } (no query or response carries it) |
| refusal | 263-277 | Refusal.[ Locked Held.Lock Awake.FlowId Asleep Lapsed Unknown.[ Address.Address Lock.Lock FlowId.FlowId Key.Key ] NoLayer NotConfigured Ended.Address OffRoute NoneAbove NotMessage Taken.Address Unidentified.Process Store.String ] |
| hook event | 278-280 | Event.[ Started ToolUsed.String Stopped ] |

### 2.2 Proposed (b4 L298-344)

Queries: Launch.{ Address Modules.Vector<Key> Brief.String }, Send.{ Recipient Request }, Subscribe.Address, Refresh.Address, Bind, Identify.Process, Report.{ FlowId Event }, Stop.FlowId, Show.Address, List. Responses: Launched, Sent, Queued, Woken, Subscribed.Vector<Metaflow>, Notified.Notification, Refreshed.{ FlowId FlowId }, Bound, Identified, Reported, Stopped, Shown.Metaflow, Listed, Refused.Refusal. Types: none of its own.

### 2.3 Design (des L276-400)

Queries Launch, Wake, Refresh, End, Current, Bind, Lock, Identify, Deliver, Release, Report, Observe.Agent.FlowId, Stop, Metaflows; Refused list as sig plus HashMismatch (L372). Removes Restart, ResolveRecipient, QueueTurnEnd, LaunchStatus, Observe.Launch (L604-607). Message's simple Send.{ Address Request } and extended Deliver.{ Lock Request } (L586-594).

### 2.4 Missing on the ordinary socket

| missing | named by | in |
|---|---|---|
| Launch by Address, Wake, Refresh | des L281-288; vf L22, L30, L58 | not in sig (W); in b4 except Wake (b4 replaces Wake with Send) |
| Subscribe and a Notification stream for metaflow state | vf L22; vn L138; b4 L312, L142 | not in sig or des (W) |
| ContextMeasured event | des L247-251, L671-675; b4 L138 | sig Event L278-280 lacks it (W) |
| HashMismatch refusal | des L372 | not in sig Refusal (W) |
| the small-model wake judgment (Verdict) | vf L18; b4 L98 | not in sig or des; des L679-680 says no model decides any step (W) |
| a request carrying the Capsule | vf L14; vn L167-180 | no Capsule type in any Flow ethos (W) |
| marked transcript block becoming an action, a book | vf L56 | sig has Presentation.{ Title } (L259) and nothing carries it (W) |
| registered pollers | vf L56 | no type anywhere (W) |
| subflow request, request ID, status | vf L60-84; cat R0156, R0245 (C) | no type anywhere; LaunchRequestId is a launch id (I) |
| session named after its direct ancestor | vf L44-48; des L959 (title type undecided) | Past exists; no naming or title type (W) |
| frame envelope and protocol version | vn L116; vsig L43-46 | no envelope or version type in any Signal (W) |
| a shared routing enum and handshake payload | vn L81-85; cat R1228 (C) | no type anywhere (W) |
| caller ancestry carried in the message | vn L56; nx L12, L24-30 | sig's Identify carries one Process, not Ancestry (W) |
| working directory of a launch | cat R0004 (C) | only meta FlowBinding has WorkingDirectory (meta L118, W) |

## 3. Signal, meta socket (meta-signal-flow)

### 3.1 Defined (meta, W)

Imports L50-51: from signal_flow FlowNode FlowId Aspect PowerLevel ModelName HarnessKind NativeSessionId Herdr* Caller CallerResolutionRejection Event; from flow_ethos the setup field types, Key, Lease, Subaspect, Topic, Layer, Source.

Queries (L52-62): Configuration, Configure.ConfigurationChange, ConsumeReset.ResetRequest, RegisterFlow.FlowNode, MetaBindExisting, Retire.FlowId, Deliver.DeliveryRequest, Vet.DeliveryRequest, Command.CommandRequest, ResolvePeer.ProcessIdentity, ReadEvents.FlowId.

Responses (L63-85): Configured, Configuration.ConfigurationSnapshot, Unconfigured, ResetConsumed, FlowRegistered, the *Rejected variants, BoundExisting, FlowRetired, Delivered.Delivery, Vetted, Commanded, PeerResolved.Caller, MetaRefused.MetaRefusal, Refused.Refusal, EventsRead.{ FlowId Vector<Event> }.

| group | lines | types | for |
|---|---|---|---|
| configuration | 90-100 | NexusRuntimeSettings (90, "only for Flow's current internal launch defaults"), ConfigureModule.{ Key Source }, ConfigureModel.{ Layer Native.String }, ConfigureThreshold.{ Layer Handover Refresh }, ConfigureNexus, ConfigurationChange.[ Module Model Threshold Nexus ], ConfigurationSnapshot | Configure and its read |
| reset credit | 101-108 | IdempotencyKey, CreditId, CreditSelection, ResetRequest, ResetOutcome, ResetRejection | ConsumeReset |
| registration and binding | 109-130 | FlowRegistrationRejection, ProcessId, ProcessUserId, ProcessStartToken, ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken } (113), Herdr server identity, MetaFlowOwnerId, HerdrTabId, WorkingDirectory, FlowLifecycle.[ RegisteredUnconfirmed ] (119), FlowContainer, FlowBinding (121), MetaBindExisting, BoundFlowBinding, FlowBindingRefusalReason, RefusedFlowBinding, FlowBindingResult, BoundExisting, BindExistingRejection, RetireRejection | adopting running flows, retiring |
| pane delivery | 131-162 | DeliveryId, MessageId, CommandLine, ByteOffset, Sender.[ Flow.FlowId Owner ] (135), PsycheContext, PsycheVerbatim, Content, Letter, Message.[ HardAbrupt MiddleAbrupt Soft ], DeliveryRequest, InterruptWitness, DeliveryGrade, Delivery, BodyRefusal, DeliveryRejection | Flow as sole pane writer |
| commands | 163-167 | HarnessCommand.[ Compact Interrupt ], CommandRequest, CommandGrade, CommandOutcome, CommandRejection | harness commands |
| refusal | 168-170 | MetaRefusal.[ PeerUnknown PeerNotAuthorized.Caller ], Refusal.[ Store.String ] | |

### 3.2 Proposed (b4 L349-381) and design (des L446-500)

b4: Configure.[ Module Model Threshold Nexus ], Forget.Key, Show; Configured, Forgotten, Shown.{ Nexus Models Thresholds Modules }, Unconfigured, Refused.Refusal; type Nexus with MessageSocket.String in place of MessageNexusPath and no MessageNexusBinary (L373-381). des: same queries with Configuration in place of Show, Refused.[ NoSource.Path HashMismatch Conflict Unknown.Key Store.String ] (L489-497).

### 3.3 Missing on the meta socket

| missing | named by | in |
|---|---|---|
| Forget.Key and Forgotten | des L478, L481; b4 L362 | not in meta (W) |
| Effort on Model | b4 L130; cat R0193, R0264 (C) | ConfigureModel is { Layer Native.String } (meta L92, W) |
| Harness on Model | des L466-471; b4 L128 | not in ConfigureModel (W) |
| NoSource, HashMismatch, Unknown.Key refusals | des L489-497 | meta Refusal is only Store.String (L170, W) |
| first-configuration record and ordinary-socket Configure before it | vn L96-105 | no type in meta or sig (W); mmem L5 has MetaConfigured.Boolean, b4 Memory has Configured.Boolean |

## 4. Operation

### 4.1 Defined (op, W)

Imports L30-31: from signal_flow the launch types, FlowNode, Caller, Launched, Event; from flow_nexus `LaunchOutcome` and `Replacement`, "the store's own types, imported from the Nexus crate until the Memory root is compiled" (L26-27): Rust types with no ethos.

Operations (L32-57) and outcomes (L58-80):

| operation | outcome | for (op comment L7-24) |
|---|---|---|
| Compose.LaunchProfile | Composed.ComposedLaunch | write the bundle copy, compose the first prompt |
| Reserve.{ ComposedLaunch OriginClue } | Reserved.{ LaunchAttemptReservation Option<FlowId> } | open the attempt, claim the FlowId (Claude) |
| Record.[ Intent Binding Acknowledgement Delivery Delivered Active Stopped Retired Exited Replacing Withdrawn Settled Harness ] | Recorded | one journal or lifecycle entry; Harness appends a Report's event |
| Register.{ FlowNode Caller } | Registered.FlowNode | bind a flow's row and role |
| Confirm.FlowId | Started.Launched | Pending to Active |
| Open.ComposedLaunch | Opened.HerdrPaneBinding | the pane |
| Spawn.PaneLaunch | Spawned | the harness |
| Bind.PaneLaunch | Bound.NativeLaunchBinding | claim identity from the harness report |
| Title | Titled | name the flow |
| Submit | Submitted.PromptDeliveryResult | type the first prompt once |
| Continue.FlowId | Continued | the brief continuation |
| Close.FlowNode | Closed | close a pane |
| Prune.LaunchRequestId | Pruned | remove the bundle copy |
| Release.FlowId | Released | give back a refused launch's hold |
| | Failed.[ CompositionRefused StoreRefused ConflictingBinding Unstarted HerdrRefused CodexRefused BundleRefused UnknownFlow ClaimRefused ] | |

Type (L81): PaneLaunch.{ ComposedLaunch HerdrPaneBinding Option<FlowId> }.

### 4.2 Proposed (b4 L386-444)

Spawn, Judge, Rouse, Enqueue, Place, Succeed, Attach, Grant, Free, Note, Notify, Reap, Register.Module, Unregister.Key; outcomes Spawned … Failed.Refusal. Its outcomes use Verdict (Judged.Verdict) and Lock (Granted.Lock), which its import list (L387-393) does not name (W).

### 4.3 Design

des has no Operation root (L11: "One Library, two Signals, one Memory", W).

### 4.4 Missing in Operation

| missing | named by | note |
|---|---|---|
| the Operation root in the design | ve L57-62; vn L148; cat R0794, R0813, R0937, R1236 (C, W) | |
| operations for sig's newer queries: Lock grant, Deliver placement, Release, Identify, End, Current, Metaflows | sig L114-121 | op has none of them (W); mop has Message's side of Lock, Deliver, Release, Bind, Identify |
| operations for meta's queries: Configure, Retire, Deliver into a pane, Command, MetaBindExisting, ConsumeReset | meta L52-62; vn L148 "every effect has a matching operation type" | op has none of them (W) |
| wake judgment, queue, drain, refresh, reap as operations | des L635-687 | op has none (W); b4 L394-444 has them |
| typed Failed for store failure | vn L68 | op Failed.StoreRefused is a unit; sig Refusal.Store.String carries a string (W) |

## 5. Memory

### 5.1 Defined

No Memory ethos file exists in the flow repository on any branch read (W). op L26-27 says the store types stay Rust "until the Memory root is compiled".

### 5.2 Proposed (b4 L449-462) and design (des L200-236)

b4 records: Metaflow, Flow, Lock, Module, Model, Threshold, Nexus, Configured.Boolean; imports Nexus from meta_signal_flow. des records: Flow.{ FlowId Session.String Process Events.Vector<Event> }, Module.{ Key Source Checked.Boolean }, Model.{ Layer Harness Native }, Metaflow, Lock, Nexus, Threshold; no Configured record.

### 5.3 Missing in Memory

| missing | named by | note |
|---|---|---|
| the Memory root itself | ve L57-62; vn L66, L148; cat R1242 (C) | absent (W) |
| per-record version and upgrade from the former form | ve L62; cat R0781, R0935, R0937 (C) | des L861-872: no migration code; b4 Rememberable only (W) |
| first-configuration flag | vn L98-100 | b4 Configured.Boolean; des none (W) |
| storage for LaunchOutcome, Replacement and the launch journal | op L26-31 | Rust only (W) |
| Flow memory in Mind | cat R1246 (C, I, "possibly superseded") | des and b4 give Flow its own store (W) |

## 6. Message, Flow's peer (W)

mmem L1-5: Memory, imports message_library:Configuration, record Standard.{ Configuration MetaConfigured.Boolean }.
mop L6-41: Operation, imports from signal_flow FlowId Address Request Lock Sender Recipient Process; operations Bind, Identify, Lock, Deliver, Release, Store; outcomes Bound, Identified, Locked, Delivered, Woken, Queued, Released, Stored, Failed with Flow's refusals mirrored plus FlowUnreachable and StoreRefused. mop is the only Operation root that names Flow's Lock/Deliver path. It rests on sig's Lock/Deliver, which b4 replaces with Send (I).

## 7. Conflicts between sources (all W unless marked)

1. **Roots.** vn L148 and ve L57-62: four roots. des L11: no Operation. Repos: Operation, no Memory. vsema L8-18 names the store root Sema, ve L57-60 says Sema too, ve L62 and vn say Memory.
2. **Process.** Three shapes: lib L37 Process.{ Pid Started }; nx L11 Process.{ Pid Started } with Ancestry; meta L113 ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken.String }. b4 imports Process from nexus.
3. **Identifiable.** nx L19-20: identify yields Result<Ancestry Unidentified>, borne by Process. b4 L206-214: identify takes a Process and yields Result<Address Refusal>, plus bind!. b4 L54 says "Flow declares none of it", while its own Library declares Identifiable.
4. **Who identifies the caller.** vf L20: no flow declares its id, every call is identified by the calling process. sig L111 ResolveCaller.Option<FlowId>, sig L113 and b4 L318 Report.{ FlowId Event } carry a claimed FlowId.
5. **FlowId.** lib L7 String; b4 L66 Hash of the session id (vf L20 agrees); cat R0032-R0037: six-character random part of the native session id (C).
6. **Topic.** lib L9 String; des L26 `Topic:Name`; vf L32 `core:Name`; ve L191 `Topic.custom:Name`; b4 L69 `protos:Coinage`, which does not exist.
7. **Start.** lib L42, nlib L4, des L102-105: a Start datom of three paths. vn L89-94: no arguments, configuration constant. b4 ruling 5 proposes no arguments.
8. **Store refusal.** vn L68: errors are never strings. sig L277, meta L170, des L398, L497: Store.String. b4 L180-183: Store.[ NotOwn Unopenable Unwritable ].
9. **Metaflow state.** lib L33 and des L82-85: Awake, Asleep, Ended. b4 L155-157: Awake, Idle, and no Ended or End query. vf L18: a topic never dies, it goes idle.
10. **Lifecycle names.** sig L224 FlowLifecycle.[ Pending Active Stopped Retired Exited ] and meta L119 FlowLifecycle.[ RegisteredUnconfirmed ]: one name, two types.
11. **Sender.** lib L38 Sender.Address; meta L135 Sender.[ Flow.FlowId Owner ]. b4's Lock drops Sender.
12. **Lock.** lib L36 { Sender Address Until.Integer }; b4 L101-103 { Address Until.Instant }.
13. **Effort and power.** sig L168 Effort.String; sig L186 PowerLevel.[ High Medium Low UltraLow ]; b4 L122 Effort.[ High Medium Low ] on Model; des Model has none.
14. **Subaspect order and members.** lib L13 Vision first, Trial before Compensation, no Spirit; b4 L104-111 Spirit first, Compensation before Trial; cat R1113 supports b4 (C).
15. **Wake judgment.** vf L18 and b4 L98: a small model judges. des L679-680: no model decides any step.
16. **Aspect.** lib (074437a) has one Aspect; the signal-flow leaf/storepath branches and meta-signal-flow main import or declare FlowAspect; fa8a85 keeps both.
17. **Nexus payload.** lib L62-63 and des L118-122: MessageNexusPath and MessageNexusBinary. b4 L379: MessageSocket.String, no MessageNexusBinary, though sig L78-82 and des L741-746 depend on it.
18. **Import direction.** des L17-21 Library imports CodexEndpoint and HarnessProfile from meta_signal_flow; lib defines them and meta imports from lib (meta L51); b4 meta Signal imports them from its own crate.
19. **vn's example (L150-188).** FlowId.Integer, Voice.{ Aspect Layer }, Capsule.{ Home Login }, Memory Flow.State.[ Running Ended ]: it matches no other source.
20. **ve L8 points to a vision-flow-ethos skill.** No such file in psyche-skills 5a18f9c; b4 proposes it.
21. **Lock and Deliver vs Send.** sig and mop use Lock.{ Sender Recipient } then Deliver.{ Lock Request }; b4 replaces them with Send.{ Recipient Request }; vf L22 says Message asks Flow to send and Flow owns the lock.

## 8. Decisions for the living

1. Does every Nexus have all four roots, with Flow's Operation and Memory both written in ethos now? Example: today the flow repository has `operation.ethos` and no `memory.ethos`, and the design has `memory` and no `operation`.
2. Is the store root called Memory or Sema? Example: vision-sema writes `Sema [] [ Lock.{ … } ]`, and vision-nexus writes `Memory … [ Flow.{ … } ]`.
3. Which Process shape is the shared one? Example: `Process.{ Pid Started }` in nexus, or `ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken }` in meta-signal-flow.
4. Does Identifiable yield the witnessed chain, with Flow finding the address, or the address itself? Example: `identify.[ Result<Ancestry Unidentified> ]` in nexus, against `identify.{ [ Process ] [ Result<Address Refusal> ] }` in the fourth edition.
5. Does Report still carry a FlowId, or is the hook's flow found from its calling process too? Example: `Report.{ FlowId Event }`, against `Report.Event`.
6. What is FlowId? Example: `FlowId.Hash` over the session id, or six characters taken from the native session id.
7. Does Flow start with no arguments, or with a Start datom? Example: `flow-nexus 'Start.{ … }'`, against `flow-nexus` with its paths fixed in the executable.
8. Does a metaflow ever end? Example: `State.[ Awake.FlowId Asleep Ended ]` with an End query, against `State.[ Awake.FlowId Idle ]` with no End.
9. Does a small model judge whether a request wakes a metaflow? Example: `Judge` answering `Verdict.[ Wake.Layer Stay ]`, against the design's "no model decides any step".
10. Does Message reach Flow by lock and deliver, or by send and subscribe? Example: `Lock.{ Sender Recipient }` then `Deliver.{ Lock Request }`, against `Send.{ Recipient Request }` with `Subscribe.Address`.
11. Is effort part of a model's configuration, and with which values? Example: `Model.{ Layer Harness Native Effort.[ High Medium Low ] }`, against `PowerLevel.[ High Medium Low UltraLow ]` on a launch.
12. Does the shared nexus library also carry time and the executable identity? Example: an `Instant` for a lock's lapse, and the canonical executable path for the Message gate, beside Process.
13. Do the Capsule, subflows with request IDs, pollers, and a marked transcript block that becomes a book belong to Flow's types now? Example: `Launch.{ Address Capsule … }` or a `Subflow.{ RequestId … }` query.
14. Do Source and the module registry stay in Flow, or move to a shared sources library or Source Nexus? Example: `Source.{ Repository Hash Path }` in flow-ethos, against `sources:Source` imported by every Nexus.

## 9. Inferences, kept apart

- I: everything on the ordinary socket of sig except Lock, Bind, Identify, Deliver, Release, End, Current and Metaflows is the 0.25.0 launch surface the design removes, and the launch-pipeline types L154-227 would leave with it.
- I: b4's import gaps (Verdict, Lock in Operation; HarnessKind, Nexus in Library) look like drafting gaps rather than intended shapes. Whether the generator would reject them was not run.
- I: Persona (vp L8-12: restart every metaflow with the right context, backups, monitors, backup model) needs a metaflow listing and a restart effect from Flow; no Flow type serves a Persona caller.
- Unknown: whether the living has ruled on any of the fourth edition's rulings since the artifact version read. No psyche records after the catalogue's 88bc733 cut were searched.

## Sources

- flow 074437a crates/flow-ethos/ethos/library.ethos and crates/flow-nexus/ethos/library.ethos; flow 962ad12 crates/flow-nexus/ethos/operation.ethos; library.ethos at 6bfbbfb, 6aa881f, a317334, fc358a5
- signal-flow d1358d3, e69fdad, a991c14, 068f0ea ethos/signal.ethos
- meta-signal-flow 6d07b7b, 2d29532, 991859f, 88f3759 ethos/signal.ethos
- nexus eafe26a, 9fa5659 ethos/library.ethos; nexus c495f2a (no ethos)
- message 87029e4 crates/message-nexus/ethos/memory.ethos and operation.ethos; message 6fa4d0c (no ethos)
- https://claude.ai/artifact/FNVZ9Lo9QXA5z4DRpW1zfM version 1791822797-c881, read with the Artifact tool; flows/875960/books/7-flow-whole-ethos-4.md (working tree, untracked) for line numbers
- Primary a589015 flows/f5a6e9/reports/flow-buildable-design.md
- psyche-skills 5a18f9c skills/vision-flow.md, vision-nexus.md, vision-signal.md, vision-sema.md, vision-persona.md, vision/ethos.md
- flows/9519a1/reports/flow-ethos-records.md at 845503, sections 1.1 and 1.2
- protos, all remote branches, searched for Coinage, Moniker, Instant: no match
- Receipt handle: none available; no PROVENANCE handoff was received.
