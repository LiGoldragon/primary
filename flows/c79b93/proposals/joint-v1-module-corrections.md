# Flow and Belief: exact module-correction proposal
Astra — Fable judged the boundaries; read-demanding subflow supplied source checks.

Proposed psyche edits only. The following exact diffs are against the current authored files. The native single-reply Rust specification is retained. Additional spellings for drain control, watcher-stream separation and link observations express the judged behavior for line review.

## psyche-belief › vision/flow-nexus-v1.md — proposed corrections

```diff
--- psyche-belief/vision/flow-nexus-v1.md
+++ psyche-belief/vision/flow-nexus-v1.md
@@ -14,61 +14,88 @@
 Everything that can be configured is configuration. The Nexus holds the vocabulary a definition is written in, as Ethos types; the user writes definitions in datom, the way Nix defines an operating system; a running flow is a definition in action. A metaflow is named by the user, and the Nexus runs it without knowing its name beforehand. A definition is one datom of its own: it is added, replaced or removed alone; a complex is one of them, naming its metaflows. No role or anatomy is in the Rust.
 
 ## The vocabulary of a definition
+
 A metaflow is members, routes and a speaker. A member is one flow definition: its harness, model and effort; whether it is a permanent flow or ephemeral; its workspace, beliefs and tools; and whom it speaks to. The speaker is the member that receives what comes to the metaflow from outside. A harness is a definition like a metaflow: its name, its features, and each feature's effect on the launch, a flag or a variable; a member names its harness by name and the features its launch is composed with, so a feature adds to a launch as well as leaves out. The Nexus holds no harness and no effect of its own; a harness is added, replaced or removed alone, as a metaflow is. Its tools are the harness default, or a restriction the harness enforces: a launch naming Restricted for a harness that cannot enforce it is refused, with the harness named. A route names whom a member may address: another member, another metaflow, or the living; a message off the routes is refused. What a metaflow is made of is the user's to define: one main flow that speaks for it, or a filter run by a System 1 model in front of the designer, or a messenger on a regular model and harness; the Nexus decides none of it.
 
+### Harness-report events
+
 ```ethos
 Library
-[ herdr:[ Pane ]
-  belief:[ ModuleName ] ]
+[] ; imports
+[ EventKind.[ Started Idle Working Ended Responded Warned Threshold ]
+  Event.[ Started Idle Working Ended Responded.String Warned Threshold ] ] ; declared kinds and observed events
+[] ; traits
+[] ; associations
+```
+
+### Harness declaration
+
+Argument lives apart from member Effort and Belief Workspace types, so its capitalized placeholders carry no accidental payload. A harness declares EventKind values; a Report carries Event, including Responded.String. Flow substitutes member/layout values, composes configured Features, and writes the declared Report hooks during Settle. A harness whose Reports omit Started is refused as Unreportable.HarnessName.
+```ethos
+Library
+[ :flow_event:EventKind ] ; imports
+[ HarnessName.String
+  FeatureName.String
+  Effect.[ Flag.String Environment.{ Name.String Value.String } ] ; configured effect
+  Feature.{ FeatureName Effect } ; one feature
+  Executable.String
+  Argument.[ Literal.String Model Effort SystemPrompt Workspace ] ; literal or substitution slot
+  RelativePath.String
+  SystemPromptRelativePath.RelativePath
+  SkillsRelativePath.RelativePath
+  LayoutTemplate.{ SystemPromptRelativePath SkillsRelativePath } ; resolved by Flow
+  Harness.{ HarnessName Executable Template.Vector<Argument>
+            Features.Vector<Feature> Reports.Vector<EventKind> LayoutTemplate } ] ; configured launch and reporting
+[] ; traits
+[] ; associations
+```
+
+### Definitions and identity
+
+```ethos
+Library
+[ :belief:ModuleName
+  :flow_harness:[ HarnessName FeatureName ]
+  :flow_event:Event
+  :herdr:Pane ] ; imports
 [ MetaflowName.String
   FlowName.String
-  HarnessName.String
-  FeatureName.String
-  Effect.[ Flag.String                ; what a feature does to the launch
-           Environment.{ Name.String  ;   a variable, set for the harness alone
-                         Value.String } ]
-  Feature.{ FeatureName Effect }
-  Harness.{ HarnessName               ; a definition, as a metaflow is
-            Features.Vector<Feature> }
   ModelName.String
   Effort.[ Low Medium High ]
-  Continuity.[ Permanent  ; keeps its address
-               Ephemeral ]           ; one run, then gone
-  Workspace.[ Path.String
-              Temporary ]            ; made at launch, removed at end
+  Continuity.[ Permanent Ephemeral ]
+  WorkspaceChoice.[ Path.String Temporary ]
   Missing.[ Refuse Notice ]
-  Beliefs.{ Vector<ModuleName> Missing }
-  Tool.String                        ; the harness's name for it
-  Tools.[ HarnessDefault              ; the Flow Nexus imposes nothing
-          Restricted.{ Allow.Vector<Tool>   ; enforced by the harness
-                       Deny.Vector<Tool> } ]  ;   or the launch is refused
-  Route.[ Speaks.FlowName             ; a member of this metaflow
-          Metaflow.MetaflowName         ;   that metaflow's speaker
-          Living ]
-  Member.{ FlowName HarnessName ModelName Effort
-           Continuity Workspace Beliefs Tools
-           Features.Vector<FeatureName>  ; of its harness, composed into its launch beside its complex's
-           Vector<Route> }
-  Metaflow.{ MetaflowName Vector<Member>
-            Speaker.FlowName }
-  FlowId.String                       ; the hash of the native session id, six characters
-  Address.{ MetaflowName
-            FlowName }  ; a permanent flow's name
-  Roster.Vector<Address>             ; every hot flow, in every first prompt
-  RosterChange.[ Started.Address     ; pushed to every hot flow as a flow starts
-                 Stopped.Address ]   ;   or stops
-  Brief.String ]
-[]
-[]
-```
-
-```mermaid
-flowchart TB
-    c["metaflow: designer"] --> s["speaker: fable"]
-    s -- "Speaks.opus" --> o["member: opus"]
-    o -- "Metaflow.implementer" --> i["metaflow: implementer, its speaker"]
-    s -- "Living" --> l["the living"]
-    x["anything else"] -. "refused" .-> s
+  Beliefs.{ Vector<ModuleName> Missing } ; definition owns missing-module policy
+  Tool.String
+  Tools.[ HarnessDefault Restricted.{ Allow.Vector<Tool> Deny.Vector<Tool> } ] ; enforced by harness
+  Route.[ Speaks.FlowName Metaflow.MetaflowName Living ]
+  Member.{ FlowName HarnessName ModelName Effort Continuity WorkspaceChoice
+           Beliefs Tools Features.Vector<FeatureName> Vector<Route> } ; one member
+  Metaflow.{ MetaflowName Vector<Member> Speaker.FlowName } ; one replaceable definition
+  ComplexName.String
+  Host.String
+  Relationship.{ From.MetaflowName To.MetaflowName } ; one permitted route
+  Complex.{ ComplexName Metaflows.Vector<MetaflowName>
+            Relationships.Vector<Relationship> Features.Vector<FeatureName>
+            Instances.Vector<Host> Speaker.MetaflowName } ; one replaceable definition
+  Address.{ MetaflowName FlowName } ; one live run per address
+  FlowId.String
+  NativeSession.String
+  Identity.{ ComplexName Address FlowId } ; known after first Report
+  Roster.Vector<Address>
+  RosterChange.[ Started.Address Stopped.Address ]
+  Brief.String
+  Priority.[ HardAbrupt MiddleAbrupt Soft ]
+  Request.[ Order.String Question.String Living.{ Context.String Verbatim.String }
+            Result.String Notice.String ] ; delivered request
+  Sender.[ Flow.FlowId Living Nexus ]
+  Message.{ Priority Sender Request } ; delivered message
+  Waking.Vector<Message>
+  Name.[ Metaflow.MetaflowName Harness.HarnessName Complex.ComplexName ]
+  Report.{ Address Pane NativeSession Event } ; verified caller/pane/native session
+  Threshold.{ ModelName Tokens.Integer Warning.Integer } ] ; per-model context policy
+[] ; traits
+[] ; associations
 ```
 
 ## Default modules
@@ -77,12 +104,12 @@
 
 ```ethos
 Signal
-[ belief:[ ModuleName ]
-  flow:[ Threshold ] ]
-[ Configure.Set ]                    ; inputs: one value at a time
-[ Configured.Set ]                   ; outputs: the value set
-[ Set.[ DefaultModules.Vector<ModuleName> ; types: the modules every flow gets
-        Threshold ] ]                ;   one model's context mark
+[ :belief:ModuleName
+  :flow:Threshold ] ; imports
+[ Configure.Set Drain ] ; inputs
+[ Configured.Set Draining Drained ] ; outputs: immediate acknowledgements and drain completion
+[ StartTimeout.Integer
+  Set.[ DefaultModules.Vector<ModuleName> Threshold StartTimeout ] ] ; one owner value per request
 ```
 
 ```datom
@@ -96,24 +123,12 @@
     m["the member's own Beliefs"] -- "composed after" --> w
 ```
 
+
+StartTimeout bounds AwaitingReport. Drain acknowledges Draining, closes new launch admission, and pushes Drained after admitted launches have completed or failed. Existing reports remain admitted while the Nexus drains.
 ## A message takes a route
 
 A flow sends through the CLI; the Flow Nexus checks the route against the sender's definition, queues the message for the receiver, and delivers it through the herdr Nexus as a prompt when the receiver is idle or the priority is pressing. A permanent flow asleep is woken by a pressing message and receives its whole queue in its first prompt. The living speaks to a complex with Say, which reaches its speaker.
 
-```ethos
-Library
-[ flow:[ FlowId Address MetaflowName ] ]
-[ Priority.[ HardAbrupt MiddleAbrupt Soft ]
-  Request.[ Order.String Question.String
-            Living.{ Context.String    ; what his words were about
-                     Verbatim.String }  ; his words whole
-            Result.String Notice.String ]
-  Sender.[ Flow.FlowId Living Nexus ]
-  Message.{ Priority Sender Request }
-  Waking.Vector<Message> ]           ; a queue delivered whole
-[]
-[]
-```
 
 ```datom
 Send.{ 15c0ce { designer fable } Soft Living.{ «context» «verbatim» } }
@@ -121,7 +136,7 @@
 
 ## The Nexus reads what a flow says
 
-Every harness event reaches the Flow Nexus through a hook calling the CLI: Report carries the flow's state, and a flow's finished response. A response that actualizes as an Input of the Flow Nexus, a Send among them, is acted on as if the flow had typed it at the CLI; any other response is kept as the flow's word and acted on by nobody. So a member that only thinks and talks, with no tool, still sends, launches and stops by writing a datom.
+Every harness event reaches the Flow Nexus through a hook calling the CLI: Report carries Address, Pane, NativeSession and the observed event. Only Started establishes FlowId; an earlier different event receives AwaitingStarted. Reported returns the derived FlowId. Later reports carry the observed state or finished response. A response that actualizes as an Input of the Flow Nexus, a Send among them, is acted on as if the flow had typed it at the CLI; any other response is kept as the flow's word and acted on by nobody. So a member that only thinks and talks, with no tool, still sends, launches and stops by writing a datom.
 
 ```mermaid
 flowchart TB
@@ -216,16 +231,16 @@
 
 ## A running session joins any Flow Nexus
 
-A flow's identity is its own, not the Nexus's. A Nexus is replaced by starting the next version beside it and having every running flow join it; nobody restarts, no context is lost. A change to a Nexus is a new version, always.
+A flow's identity is its own, not the Nexus's. A Nexus is replaced after its launch admission drains: every admitted in-flight launch completes or fails on that Nexus. The next Nexus adopts identified flows by Address and NativeSession, preserving their harnesses and contexts. A change to a Nexus is a new version, always.
 
 ```ethos
 Signal
 [ flow:[ Address FlowId ] ]
-[ Adopt.{ Address Session } ]            ; input: a running session, under its address
+[ Adopt.{ Address NativeSession } ]            ; input: a running session, under its address
 [ Adopted.FlowId                         ; outputs
   Refused.[ AddressHeld.FlowId           ;   one live flow per address
             Unidentified ] ]             ;   the calling session is not the one named
-[ Session.String ]                       ; the harness's session id, verified by the caller's process
+[ NativeSession.String ]                       ; the harness's session id, verified by the caller's process
 ```
 
 ```datom
@@ -242,156 +257,131 @@
 
 ## Signal
 
+Memory and Hot use the same Run type. Before the first Started report, Address and then Pane identify the attempt. Failure ends it as Failed. Introducing follows identification and retains that known Identity if it fails. Expired is the observed StartTimeout event. Opened carries the raw Herdr Outcome for Settling, Opening or Introducing; LaunchPhase records which act yielded it.
+```ethos
+Library
+[ :flow:[ Address Identity ]
+  :belief:[ Workspace Response ]
+  :herdr:[ Pane Outcome ] ] ; imports
+[ LaunchPhase.[ Furnishing Settling Opening Introducing AwaitingReport ]
+  Evidence.[ Furnished.Response Opened.Outcome Expired ] ; peer outcome or observed timeout
+  RunState.[ Running Idle Ended ]
+  LaunchFailed.{ Address LaunchPhase Evidence } ; pushed terminal launch failure
+  Run.[ Preparing.{ Address Workspace LaunchPhase }
+        Opened.{ Address Workspace Pane LaunchPhase }
+        Identified.{ Identity Workspace Pane RunState }
+        Failed.{ Address Workspace Option<Pane> Option<Identity> LaunchPhase Evidence } ] ] ; retained failed attempt
+[] ; traits
+[] ; associations
+```
+
+Launch admission answers Launching.Address immediately. Started.Identity and LaunchFailed are pushed on the existing Flow subscription surface, correlated by Address. HerdrDown and BeliefDown are immediate pre-admission Launch refusals only; after Launching, peer failure produces the correlated LaunchFailed event. Hot reports current runs at their known stages; failed attempts remain recorded in Memory. Replacement waits for admitted in-flight launches to complete or fail; only identified flows are adopted.
 ```ethos
 Signal
-[ flow:[ Metaflow MetaflowName FlowName FlowId
-         Address Brief ModuleName Message
-         Request Priority Tool
-         Harness HarnessName FeatureName
-         Complex ComplexName ] ]
-[ Define.[ Metaflow Harness Complex ] ; add or replace one
+[ :flow:[ Metaflow MetaflowName FlowName FlowId Address Brief Request Priority
+          Complex ComplexName Name Report Identity NativeSession ]
+  :flow_harness:[ Harness HarnessName FeatureName ]
+  :flow_run:[ Run LaunchFailed ]
+  :belief:ModuleName ] ; imports
+[ Define.[ Metaflow Harness Complex ]
   Undefine.Name
-  Describe.Name                      ; one definition, read back
-  Definitions                        ; the names defined
+  Describe.Name
+  Definitions
   Launch.{ MetaflowName FlowName Brief }
-  Rehearse.{ MetaflowName FlowName Brief } ; a Launch as a dry run: nothing runs
+  Rehearse.{ MetaflowName FlowName Brief }
   Stop.FlowId
   Send.{ FlowId Address Priority Request }
-  Say.{ ComplexName Request }       ; the living, to a complex's speaker
-  Hot                                ; the flows whose harness is up
-  Broadcast.Request                  ; one request to every hot flow
-  Report.{ FlowId Event }            ; from a harness hook
-  Subscribe ]                        ; events, as they happen
+  Say.{ ComplexName Request }
+  Hot
+  Broadcast.Request
+  Report
+  Adopt.{ Address NativeSession }
+  Subscribe ] ; inputs
 [ Defined.Name
   Undefined.Name
   Described.[ Metaflow Harness Complex ]
   Listed.Vector<Name>
-  Launched.FlowId
-  Rehearsed.Command.String           ; the shell command, whole
+  Launching.Address
+  Started.Identity
+  LaunchFailed
+  Rehearsed.Command.String
   Stopped.FlowId
   Sent.[ Delivered Queued ]
   Said.[ Delivered Queued ]
-  Hot.Vector<FlowId>                 ; the hot flows
-  Broadcast.Vector<FlowId>           ; who received it
-  Reported
+  Hot.Vector<Run>
+  Broadcast.Vector<FlowId>
+  Reported.FlowId
+  Adopted.FlowId
   Subscribed
-  Refused.[ UnknownMetaflow.MetaflowName
-            UnknownHarness.HarnessName
-            UnknownComplex.ComplexName
-            UnknownFlow.FlowName
-            NoRoute.{ FlowId Address }
-            NoBelief.Vector<ModuleName>
-            Unenforceable.HarnessName     ; Restricted, harness cannot
-            UnknownFeature.{ HarnessName FeatureName } ; named by the member or its complex, absent from the harness
-            HerdrDown BeliefDown
-            Running.Address ] ]
-[ Name.[ Metaflow.MetaflowName         ; a definition, by name
-         Harness.HarnessName
-         Complex.ComplexName ]
-  Event.[ Started Idle Working Ended
-          Responded.String            ; the response, whole
-          Warned                     ;   the handover asked
-          Threshold ] ]              ;   context past its mark
-```
-
-```datom
-; the Nexus, to the flow, at the Warning share
-HardAbrupt.Notice.«Write your handover at
-flows/f54886/handover.md»
-```
-
-```datom
-Broadcast.Notice.«Search with knowledge:search»
-Broadcast.[ 15c0ce 9af746 a030fc ]
-```
-
-A launch can be rehearsed: the same input, asked as a dry run, answers with the whole command the Flow Nexus would run and runs nothing. From that command an agent starts the flow by hand, changed however the Flow Nexus does not yet support. The answer is one string, the command line as the shell is to receive it, quoted for the shell inside.
-
-```datom
-Rehearse.{ designer fable «Read the version one book» }
-Rehearsed.«herdr --session main agent start … -- --system-prompt-file /…/bundle --model claude-fable-5-1 --effort medium»
-```
-
-```mermaid
-flowchart TB
-    m["Memory: each flow's state"] -- "Running or Idle" --> h["the hot flows"]
-    b["Broadcast.Request"] -- "one prompt into each" --> h
-    h -- "who received it" --> r["Broadcast.Vector of FlowId"]
+  Refused.[ UnknownMetaflow.MetaflowName UnknownHarness.HarnessName
+            UnknownComplex.ComplexName UnknownFlow.FlowName
+            NoRoute.{ FlowId Address } NoBelief.Vector<ModuleName>
+            Unenforceable.HarnessName Unreportable.HarnessName
+            UnknownFeature.{ HarnessName FeatureName }
+            HerdrDown BeliefDown Running.Address AddressHeld.FlowId
+            Unidentified AwaitingStarted Draining ] ] ; outputs, including pushed Started and LaunchFailed
+[] ; local types
 ```
 
 ## Emission
 
-The Flow Nexus runs nothing. Its translator is the client of two sockets: the Belief Nexus furnishes the workspace, the default modules first and the member's own Beliefs after them; the herdr Nexus makes the pane, starts the harness, types the prompt. The harness's command line and its settings file are types; the translator writes them, composing the command line from the member's harness definition: each feature the member names and each its complex names, its effect, a flag or a variable.
-
-A flow knows itself at launch: its Identity, the name of the complex it runs in, its Address and its FlowId, is composed into its first prompt or its system prompt, so it names itself in Send and Report, finds its handover path, and knows which being it is part of; the Roster is composed into the first prompt beside it. The place it runs in is the Nexus's, named at the CLI, never the flow's.
-
+Order: Furnish → Settle → Open → start-hook Report → derive FlowId and push Started.Identity → Introduce Identity/Roster/Brief → Wake. Only a Started report establishes identity from verified Address, Pane and NativeSession; Reported.FlowId supplies the derived identity. A different event arriving before Started is refused as AwaitingStarted. These boundary capabilities are lowered to the existing typed peer calls; each actual external call remains its own emission.
 ```ethos
 Emission
-[ flow:[ Member Address FlowId Brief Waking Tools
-         Workspace HarnessName Roster RosterChange
-         ComplexName ]
-  herdr:[ Pane Outcome ] ]
-[ Furnish.{ Member FlowId }           ; beliefs into the workspace
-  Settle.{ Member FlowId }            ; the harness's settings file
-  Open.{ Member Identity Roster Brief } ; pane made, harness started
-  Wake.{ Pane Waking }                ; the queue typed in
-  Tell.{ Pane RosterChange }          ; a flow started or stopped, typed in
-  Close.{ Pane Workspace } ]          ; pane killed, Temporary removed
-[ Furnished.Outcome
+[ :flow:[ Member Address Brief Waking Roster RosterChange Identity ]
+  :belief:[ Workspace FurnishRequest Response ]
+  :herdr:[ Pane Outcome ] ] ; imports
+[ Furnish.FurnishRequest
+  Settle.{ Workspace Member }
+  Open.{ Member Address }
+  Introduce.{ Pane Identity Roster Brief }
+  Wake.{ Pane Waking }
+  Tell.{ Pane RosterChange }
+  Close.{ Pane Workspace } ] ; typed boundary capabilities
+[ Furnished.Response
   Settled.Outcome
   Opened.{ Pane Outcome }
+  Introduced.Outcome
   Woken.Outcome
   Told.Outcome
-  Closed.Outcome ]
-[ Identity.{ ComplexName Address FlowId }   ; composed into the first prompt
-                                             ;   or the system prompt
-  Settings.{ HarnessName Tools Model.String } ] ; what the translator writes
+  Closed.Outcome ] ; observed results
+[] ; local types
+```
+
+```mermaid
+flowchart TB
+    a["Launch"] -- "answers immediately" --> b["Launching: Address"]
+    b -- "furnishes and settles" --> c["Open: Address and Pane"]
+    c -- "reports native session" --> d["Started: Identity"]
+    d -- "introduces" --> e["Identity, roster and brief"]
+    e -- "delivers" --> f["queued messages"]
 ```
 
 ## Memory
 
-Definitions persist: the Memory lives in the Flow Nexus's State directory and survives a restart.
+Definitions and run state persist in the Flow Nexus’s State directory. Flow owns workspace-to-run correlation; a Changed.FurnishedWorkspace receipt identifies which run its refresh policy applies to. Memory records failed launch attempts and launch-admission state.
 
 ```ethos
 Memory
-[ flow:[ Metaflow MetaflowName FlowName FlowId
-         Address Message Event Complex ]
-  herdr:[ Pane ]
-  belief:[ ModuleName ] ]
+[ :flow:[ Metaflow Complex Address Message Threshold ]
+  :flow_harness:Harness
+  :flow_run:Run
+  :belief:[ ModuleName FurnishedWorkspace ] ] ; imports
 [ Definition.[ Metaflow Harness Complex ]
-  DefaultModules.Vector<ModuleName>  ; the modules every flow gets
-  Flow.{ FlowId Address Pane
-         State.[ Running Idle Ended ]
-         Vector<Event> }
+  DefaultModules.Vector<ModuleName>
+  Run
+  FurnishedWorkspace
   Queue.{ Address Vector<Message> }
-  Threshold.{ Model.String Tokens.Integer
-              Warning.Integer }        ; share left, 20
-  Answer.[ Succeeded Failed ] ]
-```
-
-```datom
-; the user defines a metaflow: one datom, added alone
-Define.Metaflow.{
-   designer
-   [ { fable claude claude-fable-5-1 Medium
-       Permanent
-       Path.«/home/li/primary»
-       { [ { Spirit core } { Vision nexus-v1 } ] Refuse }
-       HarnessDefault []
-       [ Living ] } ]
-   fable }
-Defined.Metaflow.designer
-; defines the harness its member names: one datom, added alone
-Define.Harness.{
-   claude
-   [ { Bash
-       Flag.«--disallowedTools Bash» }
-     { ClaudeMd
-       Environment.{
-          CLAUDE_CODE_DISABLE_CLAUDE_MDS
-          1 } } ] }
-Defined.Harness.claude
-; and launches a flow of it
-Launch.{ designer fable «Read the version one book» }
-Launched.15c0ce
-```
+  Threshold
+  Admission.[ Accepting Draining Drained ]
+  Answer.[ Succeeded Failed ] ] ; records and change outcomes
+```
+
+```datom
+; a defined harness declares Started among its report events
+; launch admission is answered before native identity exists
+Launch.{ designer fable «Read the book» }
+Launching.{ designer fable }
+; after the verified Started report, the subscription receives
+Started.{ main { designer fable } 15c0ce }
+```
```

## psyche-belief › vision/belief-nexus-v1.md — proposed corrections

```diff
--- psyche-belief/vision/belief-nexus-v1.md
+++ psyche-belief/vision/belief-nexus-v1.md
@@ -8,120 +8,239 @@
 The Belief Nexus holds the belief modules and furnishes workspaces with them. Belief is the word: what a model believes when it starts. It replaces Curriculum. Its memory is its own; a definition in the Flow Nexus refers to a module by name only, and a name may resolve to nothing: the Belief Nexus answers which names are missing, and what is done about it is the definition's policy, never the Nexus's.
 
 ## Signal
-The owner registers a belief repository at the Belief Nexus's own CLI, by his login, as he defines a complex at the Flow Nexus. A peer the meta peer list names furnishes over any registered repository.
-
-A registered repository is watched: when its main moves, every workspace furnished with a module it changed is furnished again, and the Flow Nexus is told which flows now run on old belief, so a perma flow can be refreshed on it. A module is named by kind and subject; its front matter names its placement, system prompt or skill. The skills directory is the harness's.
-
+
+Register accepts Repository and Directory. Each Directory use takes an immutable per-attempt snapshot; SourceRevision is its content hash in the same String position used for a repository commit. NotDirectory and Unreadable.RelativePath retain source evidence. Repository main movement is observed through refs-change notifications. Directory is unwatched. The receipt returns the supplied Layout rather than maintaining a second path vocabulary.
 ```ethos
 Signal
-[ belief:[ ModuleSource ModuleName    ; imports
-           Workspace Location ]
-  flow:[ Harness ] ]
-[ Register.ModuleSource              ; inputs: a module source
+[ :translator:[ Caller PeerBinding UserId PeerId ] ]  ; imports: shared authenticated identity
+[ Register.ModuleSource                                ; inputs: repository and workspace effects
   Resolve.Vector<ModuleName>
-  Furnish.{ Workspace Harness        ; the harness's
-            Vector<ModuleName> }     ;   skills directory
+  Furnish.FurnishRequest
   Subscribe ]
-[ Registered.ModuleSource            ; outputs
-  Resolved.{ Vector<ModuleName>      ; found
-             Vector<ModuleName> }    ; missing
-  Furnished.{ Location
-              Vector<ModuleName> }   ; missing, left out
-  Subscribed
-  Changed.{ ModuleSource              ; pushed: main moved
-            Vector<ModuleName>        ;   modules changed
-            Vector<Workspace> }       ;   workspaces refurnished
-  Refused.[ UnknownSource.ModuleSource
-            Unwritable.Workspace ] ]
-[]
-```
-
-```datom
-Register.Repository.
-  /git/github.com/LiGoldragon/psyche-belief
-Registered.Repository.
-  /git/github.com/LiGoldragon/psyche-belief
-Register.Directory./home/li/psyche-belief-edits
-```
-
-```sh
-belief-nexus main '
-  Register.
-    /git/github.com/LiGoldragon/psyche-belief'
+[ Registered.SourceState                         ; outputs: one answer, then subscribed updates
+  Resolved.Resolution
+  Furnished.FurnishedWorkspace
+  Subscribed.Vector<FurnishedWorkspace>
+  Changed.FurnishedWorkspace
+  RefurnishFailed.RefurnishFailure
+  CleanupFailed.CleanupFailure
+  SubscriptionClosed.CloseReason                     ; terminal event on the subscribed connection
+  MemoryAfterPublication.MemoryAfterPublication
+  Refused.Refusal ]
+[ Kind.[ Spirit Intent Vision Knowledge Role ]       ; types: a module name is its folder kind and subject
+  Subject.String
+  ModuleName.{ Kind Subject }
+  RepositoryPath.String
+  DirectoryPath.String
+  Directory.DirectoryPath
+  ModuleSource.[ Repository Directory ]
+  Repository.RepositoryPath
+  WorkspacePath.String
+  Workspace.WorkspacePath
+  RelativePath.String
+  SourceRevision.String
+  PublicationRevision.Integer
+  GenerationId.String
+  Path.String
+  Layout.{ SystemPrompt.Path Skills.Path }
+  Owner.[ Login.UserId Peer.PeerId ]                 ; durable authority, separate from Caller provenance
+  SourceState.{ ModuleSource SourceRevision }
+  Found.ModuleName
+  Resolution.{ Vector<Found> Vector<ModuleName> }
+  FurnishRequest.{ Workspace Layout Vector<ModuleName> }
+  Placement.[ SystemPrompt Skills ]                  ; where one module is furnished
+  FurnishedWorkspace.{ Workspace GenerationId PublicationRevision Layout Vector<Found> Vector<ModuleName> }
+  ExecutablePath.String
+  ContractDigest.String
+  PeerList.Vector<PeerBinding>
+  Call.{ Caller Query }                                ; Query is the Signal root's generated input enum
+  SourceOperation.[ Registering Snapshotting Resolving Watching ReadingDirectory ]
+  FileOperation.[ Reading Staging Linking Replacing Inspecting Cleaning ]
+  MemoryOperation.[ Loading Recording BeginningPublication CompletingPublication
+                    AfterPublication Recovering ]
+  ExitStatus.Integer
+  Diagnostic.{ ExecutablePath Option<ExitStatus> String }
+  InvalidPlacement.[ Unknown.String NonScalar Duplicate ]
+  InvalidModule.{ ModuleName RelativePath InvalidPlacement }
+  SourceEvidence.[ NotRepository NotDirectory Unreadable.RelativePath MainUnavailable RevisionUnavailable
+                   InvalidModule
+                   Ambiguous.{ ModuleName Vector<ModuleSource> }
+                   Translator.Diagnostic ]
+  SourceFailure.{ ModuleSource SourceOperation SourceEvidence }
+  FileEvidence.[ OutsideBoundary.{ RelativePath RelativePath }
+                 PermissionDenied
+                 MissingRequired.RelativePath
+                 Conflict.{ Option<PublicationRevision> Option<PublicationRevision> }
+                 Translator.Diagnostic ]
+  FileFailure.{ Workspace FileOperation FileEvidence }
+  MemoryEvidence.[ Unavailable Corrupt Conflict ]
+  MemoryFailure.{ MemoryOperation MemoryEvidence }
+  RefusalKind.[ Source File Memory NotAuthorized SubscriberCapacityReached NotReady ]
+  RefurnishFailure.{ Workspace RefusalKind }
+  CleanupFailure.{ Workspace GenerationId PublicationRevision FileFailure } ; successful publication after which target cleanup failed
+  CloseReason.[ QueueOverflow WriteTimeout ]
+  MemoryAfterPublication.{ Workspace GenerationId PublicationRevision MemoryFailure }
+  Refusal.[ Source.SourceFailure
+            File.FileFailure
+            Memory.MemoryFailure
+            NotAuthorized.Caller
+            SubscriberCapacityReached.Integer
+            NotReady ] ]
+
 ```
 
 ## Meta
 
-A module's front matter names its placement; the default per Kind is a meta setting, set one value at a time, never in the Rust. The meta peer list names the peers admitted to Furnish, each bound by kernel credentials as a Nexus's peers are.
-
+PublicationLayout is one Belief-owned private-storage template, applied inside each workspace; retention remains Belief-owned. Flow supplies only two absolute public paths. Belief owns public-link creation and both links’ transition as one atomic publication/recovery design. No harness name or harness settings are retained here. Polling, sockets, transport and bootstrap fields are absent from owner Set; those startup facts are Place/private typed runtime data.
 ```ethos
 Signal
-[ belief:[ Kind Placement ] ]        ; imports
-[ Configure.Set ]                    ; inputs: one value at a time
-[ Configured.Set ]                   ; outputs: the value set
-[ Set.[ Placement.{ Kind             ; types: the default
-                    Placement }      ;   placement per Kind
-        Peer.PeerBinding             ;   a peer admitted to Furnish
-        RemovePeer.PeerId ]          ;   a peer removed
-  UserId.Integer                     ; a login
+[ :signal_belief_nexus:[ PeerList RelativePath Kind Placement ]
+  :translator:Caller ] ; imports
+[ Configure.ConfigureRequest ] ; inputs: one owner value, optionally revision-conditional
+[ Configured.ConfiguredState
+  ConfigureRefused.ConfigurationRefusal ] ; outputs
+[ ConfigurationRevision.Integer
+  Keeper.[ Nexus Translator ]
+  SettingName.[ SubscriberCapacity OrdinaryPeers MetaPeers PublicationLayout Placement.Kind GenerationRetention ]
+  Readiness.[ Awaiting.Vector<SettingName> Ready ]
+  OwnedRoot.RelativePath
+  GenerationsDirectory.RelativePath
+  CurrentLink.RelativePath
+  PublicationLayout.{ OwnedRoot GenerationsDirectory CurrentLink } ; one private-storage meta value
+  PositiveInteger.Integer
+  RetentionPolicy.[ KeepAll KeepPrevious.PositiveInteger ]
+  PlacementDefault.{ Kind Placement } ; default module placement
+  Set.[ SubscriberCapacity.Integer OrdinaryPeers.PeerList MetaPeers.PeerList
+        PublicationLayout Placement.PlacementDefault GenerationRetention.RetentionPolicy ]
+  ConfigureRequest.{ Option<ConfigurationRevision> Set } ; preserves configuration compare-and-set
+  ConfiguredState.{ Set Keeper ConfigurationRevision Readiness } ; one coherent revision
+  TranslatorConfiguration.{ ConfigurationRevision Vector<Set> Readiness } ; policy snapshot for emission
+  Invalid.{ Keeper SettingName String }
+  StaleRevision.{ Option<ConfigurationRevision> ConfigurationRevision }
+  ConfigurationRefusal.[ Invalid StaleRevision NotAuthorized.Caller Unavailable ] ] ; typed refusals
+```
+
+## Library
+
+```ethos
+Library
+[] ; imports
+[ UserId.Integer
+  GroupId.Integer
   ProcessId.Integer
-  PeerId.String                      ; a peer's name
-  PeerIdentity.{ UserId ProcessId }  ; checked by kernel credentials
-  PeerBinding.{ PeerId PeerIdentity } ]
-```
-
-## Library
-
-```ethos
-Library
-[ sema:[ Document Block Edit Place Outline ] ]
-[ Path.String                        ; a directory holding
-                                     ;   <type>/<subject>.md
-  ModuleSource.[ Repository.Path     ; a git repository, watched:
-                                     ;   main moving refurnishes
-                 Directory.Path ]    ; a directory read as it
-                                     ;   stands, watched by nobody
-  Kind.[ Spirit Intent Vision
-         Knowledge Role ]
-  ModuleName.{ Kind Subject.String }
-  Workspace.String                   ; the flow's directory
-  Placement.[ SystemPrompt Skill ]   ; named in front matter;
-                                     ;   default per Kind: meta
-  Location.{ SystemPrompt.String     ; the bundle file written
-             Skills.String } ]       ; the skills directory
-[]
-[]
+  Caller.{ ProcessId UserId } ; kernel caller credentials
+  PeerIdentity.{ UserId ProcessId } ; admitted peer process
+  PeerId.String
+  PeerBinding.{ PeerId PeerIdentity } ; named admission
+  PlaceName.String
+  Runtime.String
+  State.String
+  Place.{ PlaceName Runtime State } ] ; startup location
+[] ; traits
+[] ; associations
 ```
 
 ## Emission
 
-Furnishing is writing: each module into the workspace's system-prompt bundle or the harness's skills directory, as its placement says.
-
-```ethos
-Emission
-[ belief:[ Workspace ModuleName Location ]
-  flow:[ Harness ] ]                   ; imports: the harness names the skills directory
-[ Write.{ Workspace Harness Vector<ModuleName> } ] ; emissions: the bundle and the skills, written
-[ Written.Location ]                   ; outcomes
-[]
+Repository watching uses the separate streaming edge below; unary EmissionAttempt remains single-reply. The Nexus snapshots and refurnishes when that stream reports main movement. Snapshot.Directory performs one read without registering a watch. Public links, generation storage, manifest inspection, replacement and cleanup stay in one Belief publication/recovery design. The temporary Signal-root spelling preserves the currently available generator; it does not redefine what an emission means.
+```ethos
+; Proposed executable shape retains the current generator-supported Signal root.
+; The conceptual Emission root remains a separate generator capability question.
+Signal
+[ :signal_belief_nexus:[ Layout ModuleName Placement ModuleSource SourceState Repository Workspace RelativePath
+                          SourceRevision PublicationRevision GenerationId Diagnostic FileFailure ]
+  :meta_signal_belief_nexus:[ PublicationLayout RetentionPolicy ConfigurationRevision TranslatorConfiguration ] ] ; imports
+[ Snapshot.ModuleSource                                 ; emissions: read one immutable main snapshot
+  Publish.Publication                                 ;   or atomically replace one owned publication
+  InspectPublication.InspectionRequest                ;   or observe owned recovery evidence
+  Clean.CleanupRequest ]                              ;   or remove proven-owned superseded generations
+[ Snapshotted.SourceSnapshot                          ; outcomes
+  Published.PublicationState
+  Inspected.PublicationInspection
+  Cleaned.CleanupState
+  CleanupRefused.FileFailure
+  EmissionRefused.EmissionRefusal ]
+[ EmissionAttempt.{ ConfigurationRevision TranslatorConfiguration Query } ; one immutable attempt snapshot
+  EmissionAttemptOutcome.{ ConfigurationRevision Response } ; response revision equals its attempt
+  Content.String                                      ; types
+  AbsolutePath.String
+  ModuleContent.{ ModuleName RelativePath Option<Placement> Content }
+  SourceSnapshot.{ ModuleSource SourceRevision Vector<ModuleContent> }
+  SkillFile.{ RelativePath Content }
+  WorkspaceImage.{ Layout PublicationLayout Content Vector<SkillFile> }
+  SourceStates.Vector<SourceState>
+  FoundModules.Vector<ModuleName>
+  MissingModules.Vector<ModuleName>
+  PriorPublication.Option<PublicationRevision>
+  IntendedPublication.PublicationRevision
+  PublicationManifest.{ GenerationId IntendedPublication Layout PublicationLayout SourceStates
+                         FoundModules MissingModules }
+  Publication.{ Workspace GenerationId PriorPublication IntendedPublication
+                 WorkspaceImage SourceStates FoundModules MissingModules RetentionPolicy }
+  PublicationIdentity.{ GenerationId PublicationRevision }
+  PublicationState.{ Workspace PublicationIdentity }
+  InspectionRequest.{ Workspace PublicationIdentity Layout PublicationLayout }
+  LinkTarget.String
+  LinkObservation.[ Absent Symlink.LinkTarget Other Unreadable.RelativePath ]
+  PublicLinks.{ SystemPrompt.LinkObservation Skills.LinkObservation }
+  PublicationInspection.{ Workspace Option<PublicationIdentity> Option<PublicationManifest> PublicLinks }
+  CleanupRequest.{ Workspace PublicationIdentity Layout PublicationLayout }
+  CleanupOutcome.[ Removed AlreadyAbsent ]
+  CleanupState.{ Workspace PublicationIdentity CleanupOutcome }
+  SourceOperation.[ ReadingMain ReadingTree ReadingDirectory ]
+  PublicationOperation.[ StagingGeneration WritingManifest
+                          ReplacingPointer InspectingPointer InspectingManifest ]
+  InvalidPlacement.[ Unknown.String NonScalar Duplicate ]
+  InvalidModule.{ ModuleName RelativePath InvalidPlacement }
+  SourceEvidence.[ NotRepository NotDirectory Unreadable.RelativePath MainUnavailable RevisionUnavailable InvalidModule Translator.Diagnostic ]
+  SourceRefusal.{ ModuleSource SourceOperation SourceEvidence }
+  BoundaryRoot.AbsolutePath
+  BoundaryCandidate.AbsolutePath
+  BoundaryEvidence.{ BoundaryRoot BoundaryCandidate }
+  ExpectedRevision.Option<PublicationRevision>
+  ObservedRevision.Option<PublicationRevision>
+  RevisionEvidence.{ ExpectedRevision ObservedRevision }
+  PublicationEvidence.[ OutsideBoundary.BoundaryEvidence
+                         DestinationUnavailable.AbsolutePath
+                         PriorRevisionMismatch.RevisionEvidence
+                         OwnedPointerMismatch
+                         ManifestMismatch
+                         PermissionDenied
+                         Translator.Diagnostic ]
+  PublicationRefusal.{ Workspace PublicationOperation PublicationEvidence }
+  EmissionRefusal.[ Source.SourceRefusal Publication.PublicationRefusal ] ]
+
+```
+
+### Repository-change subscription
+
+The Nexus subscribes to its translator's refs-change notification service for a registered repository. This connection stays open; it does not pass through the unary EmissionAttempt envelope. Directory sources never enter this edge.
+```ethos
+Signal
+[ :belief:[ Repository SourceFailure ] ] ; imports
+[ Subscribe.Repository ] ; inputs: one registered repository
+[ Subscribed.Repository
+  Changed.Repository
+  Refused.SourceFailure ] ; outputs: acknowledgement, changes or typed failure
+[] ; local types
 ```
 
 ## Memory
 
+Memory holds source snapshots, furnished-workspace receipts, pending publication intent, publication manifests, cleanup requests and coherent configuration revisions. The manifest records the supplied Layout and private PublicationLayout. Inspection records the shared current-generation pointer and both public links. Belief prepares the generation, manifest and both link projections before atomically switching that one pointer; recovery judges recorded intent against those observations.
+
 ```ethos
 Memory
-[ belief:[ ModuleSource ModuleName ] ]
-[ Source.{ ModuleSource Vector<ModuleName> } ; records: each registered source and the modules it holds
-  Answer.[ Succeeded Failed ] ]
-```
-
-```datom
-Furnish.{ /home/li/primary Claude
-          [ { Spirit core } { Vision nexus-v1 }
-            { Vision none } ] }
-Furnished.{ { /home/li/primary/.bundle
-              /home/li/primary/.claude/skills }
-            [ { Vision none } ] }
+[ :belief:[ FurnishedWorkspace MemoryFailure ]
+  :belief_emission:[ SourceSnapshot Publication PublicationManifest CleanupRequest ]
+  :meta_belief:ConfiguredState ] ; imports
+[ SourceSnapshot
+  FurnishedWorkspace
+  Publication
+  PublicationManifest
+  CleanupRequest
+  ConfiguredState
+  Answer.[ Succeeded Failed.MemoryFailure ] ] ; source, publication, recovery and policy records
 ```
 
 ## The ordinary single-reply boundary
@@ -329,105 +448,3 @@
 ```
 
 The standard-library I/O and UTF-8 errors and the rkyv native error remain opaque dependency-owned evidence. This module specifies their placement and ownership, not their private representation.
-
-### Existing ordinary domain contract
-
-The domain vocabulary is retained. This is its existing Ethos, including the declarations needed by Query and Response. The service types above use the compiled ordinary contract as `public`.
-
-```ethos
-Library
-[]                                      ; imports
-[ UserId.Integer                        ; types: authenticated identity
-  GroupId.Integer
-  ProcessId.Integer
-  Caller.{ ProcessId UserId }            ; caller credentials
-  PeerIdentity.{ UserId ProcessId }      ; peer binding identity
-  PeerId.String
-  PeerBinding.{ PeerId PeerIdentity }    ; named peer
-  Principal.[ Login.UserId               ; authenticated owner
-              Peer.PeerId ] ]
-[]                                      ; traits
-[]                                      ; associations
-```
-
-```ethos
-Signal
-[ :translator:[ Caller PeerBinding UserId PeerId ] ] ; imports
-[ Register.Repository                   ; inputs
-  Resolve.Vector<ModuleName>
-  Furnish.FurnishRequest
-  Subscribe ]
-[ Registered.RepositoryState            ; outputs
-  Resolved.Resolution
-  Furnished.FurnishedWorkspace
-  Subscribed.Vector<FurnishedWorkspace>
-  Changed.FurnishedWorkspace
-  RefurnishFailed.RefurnishFailure
-  CleanupFailed.CleanupFailure
-  SubscriptionClosed.CloseReason
-  MemoryAfterPublication.MemoryAfterPublication
-  Refused.Refusal ]
-[ Kind.[ Spirit Intent Vision Knowledge Role ] ; types
-  Subject.String
-  ModuleName.{ Kind Subject }            ; module identity
-  RepositoryPath.String
-  Repository.RepositoryPath
-  WorkspacePath.String
-  Workspace.WorkspacePath
-  RelativePath.String
-  SourceRevision.String
-  PublicationRevision.Integer
-  GenerationId.String
-  Harness.[ Claude Codex ]               ; harness choice
-  Owner.[ Login.UserId Peer.PeerId ]      ; workspace owner
-  RepositoryState.{ Repository SourceRevision } ; observed source
-  Found.ModuleName
-  Resolution.{ Vector<Found> Vector<ModuleName> } ; found and missing
-  FurnishRequest.{ Workspace Harness Vector<ModuleName> } ; request
-  Placement.[ SystemPrompt Skills ]      ; destination kind
-  SystemPromptPath.String
-  SkillsPath.String
-  FurnishedPaths.{ SystemPromptPath SkillsPath } ; published paths
-  FurnishedWorkspace.{                   ; publication receipt
-     Workspace GenerationId PublicationRevision FurnishedPaths
-     Vector<Found> Vector<ModuleName> }
-  ExecutablePath.String
-  ContractDigest.String
-  PeerList.Vector<PeerBinding>
-  Call.{ Caller Query }                  ; authenticated input
-  SourceOperation.[ Registering Snapshotting Resolving Watching ] ; source act
-  FileOperation.[ Reading Staging Linking Replacing Inspecting Cleaning ] ; file act
-  MemoryOperation.[ Loading Recording BeginningPublication ; Memory act
-                    CompletingPublication AfterPublication Recovering ]
-  ExitStatus.Integer
-  Diagnostic.{ ExecutablePath Option<ExitStatus> String } ; external diagnostic
-  InvalidPlacement.[ Unknown.String NonScalar Duplicate ] ; placement error
-  InvalidModule.{ ModuleName RelativePath InvalidPlacement } ; source error
-  SourceEvidence.[ NotRepository MainUnavailable RevisionUnavailable ; evidence
-                   InvalidModule
-                   Ambiguous.{ ModuleName Vector<Repository> }
-                   Translator.Diagnostic ]
-  SourceFailure.{ Repository SourceOperation SourceEvidence } ; source failure
-  FileEvidence.[ OutsideBoundary.{ RelativePath RelativePath } ; evidence
-                 PermissionDenied
-                 MissingRequired.RelativePath
-                 Conflict.{ Option<PublicationRevision>
-                            Option<PublicationRevision> }
-                 Translator.Diagnostic ]
-  FileFailure.{ Workspace FileOperation FileEvidence } ; file failure
-  MemoryEvidence.[ Unavailable Corrupt Conflict ] ; Memory evidence
-  MemoryFailure.{ MemoryOperation MemoryEvidence } ; Memory failure
-  RefusalKind.[ Source File Memory NotAuthorized ; refusal class
-                SubscriberCapacityReached NotReady ]
-  RefurnishFailure.{ Workspace RefusalKind } ; refurnish failure
-  CleanupFailure.{ Workspace GenerationId PublicationRevision FileFailure } ; cleanup
-  CloseReason.[ QueueOverflow WriteTimeout ] ; existing stream terminal reason
-  MemoryAfterPublication.{                ; Memory failure after publication
-     Workspace GenerationId PublicationRevision MemoryFailure }
-  Refusal.[ Source.SourceFailure         ; domain refusals
-            File.FileFailure
-            Memory.MemoryFailure
-            NotAuthorized.Caller
-            SubscriberCapacityReached.Integer
-            NotReady ] ]
-```
```
