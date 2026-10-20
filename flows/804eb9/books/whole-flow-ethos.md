### Proposal 1: psyche-context › vision/flow-ethos.md, a new file

+ ---
+ description: The Flow Nexus in ethos; its types, traits and layout are read or judged.
+ dependencies: [vision-ethos, vision-flow]
+ ---

+ ## library.ethos, in flow-ethos

```ethos
+ ```ethos
+ Library.{
+ [ protos:[ String Integer Boolean ] ]   ; imports
+ [ FlowId.String                         ; types
+   Topic.String
+   Layer.[ Primary Secondary
+           Tertiary Quaternary ]
+   Subaspect.[ Vision Intent Knowledge
+               Operation Trial Compensation ]
+   Key.{ Subaspect Topic }               ; a module
+   Said.{ Context.String Verbatim.String }
+   Request.[ Order.String            ; what reaches
+             Question.String         ;   a metaflow
+             Psyche.Said
+             Psyches.Vector<Said>
+             Result.String
+             Notice.String ]
+   Aspect.[ Psyche Mind Field ]
+   Address.{ Aspect Topic Layer }
+   Recipient.[ Address Up ]
+   SentBy.[ Sender Unknown ]
+   QueuedRequest.{ SentBy Request }
+   Metaflow.{ Address
+              State.[ Awake.FlowId Asleep Ended ]
+              Past.Vector<FlowId>
+              Queue.Vector<QueuedRequest> }
+   Lock.{ Sender Address Until.Integer }
+   Process.{ Pid.Integer Started.Integer }
+   Sender.Address
+   OrdinarySocketPath.String
+   MetaSocketPath.String
+   StorePath.String
+   Start.{ OrdinarySocketPath MetaSocketPath
+           StorePath }
+   ModelName.String
+   HarnessKind.[ Codex Claude ]
+   Brief.{ String }
+   Heartbeat.{ Vector<Topic> Integer } ] ; hours
+ [ Titled.[ title.[ String ] ]           ; traits
+   Layered.[ layer.[ Layer ] ]
+   Briefing.[ brief.[ String ] ]
+   Waking.[ wakes.[ Boolean ] ]
+   Sleepable.
+     [ sleep![ Vector<QueuedRequest> ] ]
+   Wakeable.[ wake!{ [ Waking ]
+                     [ FlowId ] } ]
+   Parted.[ parts.[ Vector<String> ] ]
+   Prompting.[ text.[ String ] ]
+   Pulsing.[ pulse.[ Vector<Topic> ] ] ]
+ [ Address.[ Titled Layered ]        ; associations
+   Brief.[ Briefing ]
+   Request.[ Waking ]
+   Metaflow.[ Sleepable Wakeable ]
+   Heartbeat.[ Pulsing ] ] }
+ ```
```

+ ## signal.ethos, in signal-flow

```ethos
+ ```ethos
+ Signal.{
+ [ flow_ethos:[ Aspect Address FlowId  ; imports
+                Request SentBy QueuedRequest Lock
+                Sender Process Metaflow Key
+                Recipient Layer Topic Subaspect
+                OrdinarySocketPath MetaSocketPath
+                Start ModelName HarnessKind ] ]
+ [ Start.LaunchProfile                  ; queries
+   Send.{ Address Request }
+   Stop.FlowId
+   Report.{ FlowId Event }            ; from a hook
+   Pulse ]
+ [ Started.Launched                     ; responses
+   Sent.FlowId
+   Queued
+   Stopped.FlowId
+   Reported
+   Pulsed.Vector<Address>
+   Refused.Refusal ]
+ [ ModuleIdentity.String                ; types
+   SystemModules.Vector<ModuleIdentity> ; modules
+   UserModules.Vector<ModuleIdentity>
+   Effort.String
+   LeaveOut.[ ClaudeAiConnectors
+              ConfiguredMcpServers AgentTool
+              ExplorePlanAgents FileTools
+              WorkflowTool ScheduleWakeupTool
+              ReportFindingsTool ListAgentsTool
+              CronTools WebTools DeferredTools
+              SkillTool BundledSkills ClaudeMd
+              GitInstructions AttributionReminder
+              UserSettings ToolSearch BashTool
+              CodexSkillListing CodexAgentsMd
+              CodexCollaborationMode
+              CodexEnvironmentContext
+              CodexPermissions
+              CodexDeveloperInstructions ]
+   LaunchRequestId.String
+   RememberingDepth.Integer
+   HerdrSessionName.String
+   InstructionPrompt.String
+   RememberedFlow.{ FlowId RememberingDepth }
+   LeaveOuts.Vector<LeaveOut>
+   LaunchProfile.{ LaunchRequestId      ; a launch
+                   SystemModules
+                   UserModules
+                   Address
+                   ModelName
+                   Effort
+                   Option<FlowId>
+                   Vector<RememberedFlow>
+                   HerdrSessionName
+                   Option<LeaveOuts>
+                   InstructionPrompt }
+   SessionId.String
+   HerdrAgentName.String
+   HerdrPaneId.String
+   HerdrTerminalId.String
+   HerdrRoute.{ HerdrSessionName HerdrAgentName
+                HerdrPaneId HerdrTerminalId }
+   HerdrRouteSelection.[ Available.HerdrRoute
+                         Unavailable ]
+   FlowOrigin.{ FlowId SessionId }
+   Origin.[ Flow.FlowOrigin Unbound ]
+   Launched.{ FlowId SessionId          ; a start
+              HerdrRouteSelection Origin }
+   Refusal.[ Locked
+             Held.Lock
+             Awake.FlowId
+             Asleep
+             Lapsed
+             Unknown.[ Address.Address
+                       Lock.Lock
+                       FlowId.FlowId
+                       Key.Key ]
+             NoLayer
+             NotConfigured
+             Ended.Address
+             OffRoute
+             NoneAbove
+             NotMessage
+             Taken.Address
+             Unidentified.Process
+             Store.String
+             NotSendServer.Process ]
+   PromptSha256.String
+   NativeSessionId.String
+   TranscriptPath.String
+   PromptId.String
+   NativeStop.{ Option<NativeSessionId>
+                Option<TranscriptPath> }
+   NativePrompt.{ Option<NativeSessionId>
+                  Option<PromptId>
+                  PromptSha256 }
+   Event.[ Started
+           ToolUsed.String
+           Stopped.NativeStop
+           PromptSubmitted.NativePrompt ] ] }
+ ```
```

+ ## curriculum.ethos, in flow-nexus

```ethos
+ ```ethos
+ Library.{
+ []                         ; imports
+ [ ModuleIdentity.String    ; types
+   CallerMetaflow.{ String String String }
+   RoleName.String
+   ModelId.String
+   DescriptionModule.ModuleIdentity
+   ContextModules.Vector<ModuleIdentity>
+   Permission.[ Restricted Unrestricted ]
+   Effort.[ Low Medium High Xhigh ]
+   Surface.[ ClaudeAgent CodexAgent PiAgent ]
+   RoleTools.[ Inherit Explicit.Vector<String> ]
+   RoleCallers.[ Any
+                 Only.Vector<CallerMetaflow> ]
+   RoleDefinition.{ RoleName Surface ModelId
+                    Effort Permission
+                    DescriptionModule
+                    ContextModules
+                    RoleTools RoleCallers }
+   Roles.{ Vector<RoleDefinition> }
+   RolesDocument.[ Roles.Roles ] ]
+ []                         ; traits
+ [] }                       ; associations
+ ```
```

### Proposal 2: psyche-context › vision/nexus.md

  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ ### library.ethos, in flow-ethos

```ethos
- ```
- Library                                  ; what the three parts share
+ ```ethos
+ ; what the three parts share
+ Library.{
  []                                       ; imports: none
- [ FlowId.Integer                         ; types
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
+ [ FlowId.String                          ; types
+   Address.{ Aspect Topic Layer }         ; a seat
    Aspect.[ Psyche Mind Field ]
+   Topic.String
    Layer.[ Primary Secondary Tertiary Quaternary ]
+   Subaspect.[ Vision Intent Knowledge
+               Operation Trial Compensation ]
+   Key.{ Subaspect Topic }
+   Sender.Address
+   Lock.{ Sender Address Until.Integer }
+   Process.{ Pid.Integer Started.Integer }
-   Event.[ Started Stopped ] ]
+   ModelName.String ]
  []                                       ; kinds
- []                                       ; associations
+ [] }  ; associations
+ ```
```

+ 
+ ### signal.ethos, in signal-flow

```ethos
  
- Signal                                   ; what Flow says, on its ordinary socket
+ ```ethos
+ ; what Flow says, on its ordinary socket
+ Signal.{
- [ flow:[ FlowId Voice Event ] ]          ; imports from the Library
- [ Launch.{ Voice                         ; queries
-            Brief.String }
-   Report.{ FlowId Event } ]
- [ Launched.FlowId                        ; responses
-   Refused.[ NoCapsule
-             VoiceBusy.Voice ]
+ [ flow_ethos:[ FlowId Address Key  ; imports
+                Lock Process ModelName ] ]
+ [ Start.LaunchProfile            ; queries
+   Report.{ FlowId Event } ]
+ [ Started.Launched               ; responses
+   Refused.Refusal
    Reported ]
- []                                       ; types
+ [ ModuleIdentity.String         ; types
+   SystemModules.Vector<ModuleIdentity>
+   UserModules.Vector<ModuleIdentity>
+   Effort.String
+   LeaveOut.[ ClaudeAiConnectors
+              ConfiguredMcpServers AgentTool
+              ExplorePlanAgents FileTools
+              WorkflowTool ScheduleWakeupTool
+              ReportFindingsTool ListAgentsTool
+              CronTools WebTools DeferredTools
+              SkillTool BundledSkills ClaudeMd
+              GitInstructions AttributionReminder
+              UserSettings ToolSearch BashTool
+              CodexSkillListing CodexAgentsMd
+              CodexCollaborationMode
+              CodexEnvironmentContext
+              CodexPermissions
+              CodexDeveloperInstructions ]
+   LeaveOuts.Vector<LeaveOut>
+   LaunchRequestId.String
+   RememberingDepth.Integer
+   RememberedFlow.{ FlowId RememberingDepth }
+   HerdrSessionName.String
+   InstructionPrompt.String
+   LaunchProfile.{ LaunchRequestId
+                   SystemModules
+                   UserModules
+                   Address
+                   ModelName
+                   Effort
+                   Option<FlowId>
+                   Vector<RememberedFlow>
+                   HerdrSessionName
+                   Option<LeaveOuts>
+                   InstructionPrompt }
+   SessionId.String
+   HerdrAgentName.String
+   HerdrPaneId.String
+   HerdrTerminalId.String
+   HerdrRoute.{ HerdrSessionName HerdrAgentName
+                HerdrPaneId HerdrTerminalId }
+   HerdrRouteSelection.[ Available.HerdrRoute
+                         Unavailable ]
+   FlowOrigin.{ FlowId SessionId }
+   Origin.[ Flow.FlowOrigin Unbound ]
+   Launched.{ FlowId SessionId
+              HerdrRouteSelection Origin }
+   FlowLifecycle.[ Pending Active Stopped
+                   Retired Exited ]
+   Refusal.[ Locked
+             Held.Lock
+             Awake.FlowId
+             Asleep
+             Lapsed
+             Unknown.[ Address.Address
+                       Lock.Lock
+                       FlowId.FlowId
+                       Key.Key ]
+             NoLayer
+             NotConfigured
+             Ended.Address
+             OffRoute
+             NoneAbove
+             NotMessage
+             Taken.Address
+             Unidentified.Process
+             Store.String
+             NotSendServer.Process ]
+   PromptSha256.String
+   NativeSessionId.String
+   TranscriptPath.String
+   PromptId.String
+   NativeStop.{ Option<NativeSessionId>
+                Option<TranscriptPath> }
+   NativePrompt.{ Option<NativeSessionId>
+                  Option<PromptId>
+                  PromptSha256 }
+   Event.[ Started
+           ToolUsed.String
+           Stopped.NativeStop
+           PromptSubmitted.NativePrompt ] ] }
+ ```
```

+ 
+ ### operation.ethos, in flow-nexus

```ethos
  
- Operation                                ; what Flow does: one operation for every effect
+ ```ethos
+ ; what Flow does: one operation for every effect
+ Operation.{
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Start.{ Voice Capsule }                ; operations
+ [ signal_flow:[ FlowId Event   ; imports
+                 LaunchProfile Launched
+                 ContextRefusal LeaveOutRefusal
+                 HarnessSpawnRefusal
+                 NativeLaunchRefusal ] ]
+ [ Start.LaunchProfile          ; operations
    Record.{ FlowId Event } ]
- [ Started.FlowId                         ; outcomes
+ [ Started.Launched             ; outcomes
    Recorded
-   Failed.[ CapsuleRefused StoreRefused ] ]
+   Failed.[ CompositionRefused
+            StoreRefused
+            ConflictingBinding
+            Unstarted
+            HerdrRefused
+            CodexRefused
+            UnknownFlow
+            ClaimRefused
+            NotAsleep
+            NotAwake
+            NothingQueued
+            AddressAwake
+            AddressEnded
+            ContextRefused.ContextRefusal
+            LeaveOutRefused.LeaveOutRefusal
+            SpawnRefused.HarnessSpawnRefusal
+            LaunchRefused.NativeLaunchRefusal ] ]
- [ Capsule.{ Home.String                  ; types
-             Login.Vector<String> } ]
+ [] }                           ; types
+ ```
```

+ 
+ ### Memory

```ethos
  
- Memory                                   ; what Flow remembers
+ ```ethos
+ ; what Flow remembers
+ Memory.{
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Flow.{ FlowId                          ; record types
-          Voice
-          State.[ Running Ended ]
-          Vector<Event> } ]
+ [ flow_ethos:[ FlowId Address ]  ; imports
+   signal_flow:[ FlowLifecycle Event ] ]
+ [ Chronicle.{ FlowId           ; record types
+               Address
+               FlowLifecycle
+               Vector<Event> } ] }
```

````datom
  ```
- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
+ ; 1 Query, typed at the CLI, sent as signal,
+ ;   and 2 Operation, from Signal's intend
+ Start.{ launch-7 [ spirit-core ] [ vision-nexus ]
+         { Psyche nexus Primary } fable medium
+         None [] psyche-nexus None
+         «Draft the Nexus book» }
+ ; 3 the Change Operation hands Memory
+ { 7 { Psyche nexus Primary }
+   Pending [ Started ] }
````

```datom
- Succeeded                                             ; 4 Memory's answer to Operation
+ ; 4 Memory's answer to Operation
+ Recorded
```

````datom
- Started.7                                             ; 5 Outcome
- Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
+ ; 5 Outcome, and 6 Response, from Signal's
+ ;   answer, back to the CLI
+ Started.{ 7 session-7
+           Available.{ psyche-nexus claude-a1
+                       w1:p4 term-4 }
+           Unbound }
  ```
````

### Proposal 3: psyche-context › vision/datom.md

- `Accepted.{ … }` and `Refused.{ … }` are two types. When an enum value
+ `Accepted.{ … }` and `Declined.{ … }` are two types. When an enum value

```datom
- ; datom, in a position expecting Person: a struct of name String, born Integer, address Address, roles Vector<Role>.
+ ; datom, in a position expecting Person: a
+ ; struct of name String, born Integer,
+ ; residence Residence, roles Vector<Role>.
```

```datom
-   { «12 Rue de la Paix» Paris 75002 }    ;   enclosed by braces: a struct, the Address. It holds three structures:
+   ;   enclosed by braces: a struct, the
+   ;   Residence. It holds three structures:
+   { «12 Rue de la Paix» Paris 75002 }
```

```datom
-   [ Author                               ;   enclosed by brackets: a vector of Role. It holds two structures:
+   ;   enclosed by brackets: a vector of
+   ;   Role. It holds two structures:
+   [ Author
```

```datom
- ; Reply: an enum of Accepted.{ id Integer  at String }, Refused.{ reason String  code Integer }, Pending
+ ; Reply: an enum of
+ ;   Accepted.{ id Integer  at String },
+ ;   Declined.{ reason String  code Integer },
+ ;   Pending
```

```datom
- Refused.{ «no such file: { } is content» 2 } ; delimited: the string has spaces and braces; inside the guillemets they are content
+ ; delimited: the string has spaces and
+ ;   braces; inside the guillemets they
+ ;   are content
+ Declined.{ «no such file: { } is content» 2 }
```

### Proposal 4: psyche-context › vision/ethos.md

```rust
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
  pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub string_vector: Vec<String>, pub lock_option: Option<Lock> }
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
```

```rust
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
  pub struct Lock { pub lock_id: LockId, pub lock_name: LockName }
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
  pub struct PathOverlap_Data { pub first_lock: Lock, pub second_lock: Lock }
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
```

```rust
  pub type SyntaxError = Vec<FilePath>;
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
```

```rust
  pub type FilePath = String;
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
  pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
```

- Ethos Zero emits `Datomizable` and `Compositional` on every struct and
- enum it generates, so every ethos-declared type always bears both
- traits and no declared type can exist without them. An alias bears them
- through the type it names: an alias is not a new type and cannot carry
- a derive.
+ Ethos Zero emits the derives `Datomizable` and `Composing` on every struct and enum it generates except a sealed one, so every other ethos-declared type bears `Datomizable` and `Composing`, and no such type can exist without them.
+ The `Composing` derive also gives a struct `Compositional`, through which the struct states its positions.
+ An alias bears them through the type it names: an alias is not a new type and cannot carry a derive.

```rust
- #[derive(Datomizable, Compositional)]        // a type: always derived
+ #[derive(Datomizable, Composing)]  // a type
```

- A generated signal library bears `Datomizable` and `Compositional`
- conditionally, under a feature the CLI and client enable and the Nexus
- does not. The Nexus compiles the same types without any
- textualization capability and without datom-codec as a dependency.
+ A generated signal library derives `Datomizable` and `Composing` conditionally, under a feature the CLI and client enable and the Nexus does not.
+ The Nexus compiles the same types without any textualization capability and without datom-codec as a dependency.

```rust
- #[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
+ #[cfg_attr(feature = "datom",
+            derive(Datomizable, Composing))]
```

```rust
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
  pub struct Record { pub string: String, pub integer: Integer }
```

```rust
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
  pub enum SinkError { Closed, Full }
```

  Identity section above.
+ 
+ ## A sealed type
+ 
+ A sealed type is declared with `Sealed` between its name and its shape, and only a struct is sealed.
+ Its positions are generated `pub(super)`, so they are read and built only within the module that contains its own.
+ It is associated in the same file with a trait whose capability with no self yields the type, or a result of the type or a refusal.
+ Of the datom traits it bears `Datomizable` alone, and of rkyv's it bears no `Deserialize`: it is printed and archived, but no datom or archive builds it.
+ No type in its file that is read from data holds it.
+ 

```ethos
+ ```ethos
+ Library.{
+ [ flow_ethos:[ Address Titled ] ] ; imports
+ [ Unverified.[ Mismatch Unknown ] ; types
+   VerifiedContext.Sealed.
+      { Address Vector<String> } ]
+ [ Requested.[ address.[ Address ] ] ; traits
+   Composed.[ modules.[ Vector<String> ] ]
+   Verifying.
+      [ verified:
+           { [ Requested Composed ]
+             [ Result<Self Unverified> ] }
+        text.[ String ] ] ]
+ [ Unverified.[ Titled ]           ; associations
+   VerifiedContext.[ Verifying ] ] }
+ ```
```

### Proposal 5: psyche-context › vision/datom.md

```rust
-     fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error> {
+     fn compose_positions<T: Compositional>(
+         &self,
+         budget: &mut Budget,
+     ) -> Result<T, Error> {
```

```rust
- #[derive(Datomizable, Compositional)]
+ #[derive(Datomizable, Composing)]
```

### Proposal 6: psyche-context › vision/protos.md

```rust
- impl Composable    for Datom  { fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>; }
+ impl Composable    for Datom  {
+     fn compose<T: Composing>(
+         &self,
+         budget: &mut Budget,
+     ) -> Result<T, Error>;
+ }
```

### Proposal 7: psyche-context › vision/ethos.md

- A simple trait opens with a bracket after the dot. Its capabilities sit
- inside. The receiver after a capability's head names who is called:
- `.` takes self, `!` takes mutable self, `:` takes no self. A
- capability with inputs is a headed brace: inputs in a bracket, yield
- in a bracket. A yield bracket holds one type.
+ A simple trait opens with a bracket after the dot.
+ Its capabilities sit inside.
+ The receiver after a capability's head names who is called: `.` takes self, `!` takes mutable self, `:` takes no self.
+ A capability with inputs is a headed brace: inputs in a bracket, yield in a bracket.
+ A yield bracket holds one type, or nothing when the capability only acts.
+ 

```ethos
+ ```ethos
+ Library.{
+ []                                ; imports
+ [ Counter.{ Integer Boolean } ]   ; types
+ [ Counting.[ count.[ Integer ]    ; traits
+              bump![] ] ]
+ [ Counter.[ Counting ] ] }        ; associations
+ ```
```

### Proposal 8: psyche-context › vision/flow.md

  answer or fulfill.
+ 
+ ## The last response is a datom object
+ 
+ A flow's last response is a datom object.
+ Its variant comes first and decides its structure, and that structure may hold further objects, each with its own variant.
+ For example:
+ 

```ethos
+ ```ethos
+ Library.{
+ []                                  ; imports
+ [ Title.String                      ; types
+   Body.String
+   Cause.String
+   Unblock.String
+   Presentation.{ Title }            ; a book
+   Block.{ Cause Unblock }           ; a blocker
+   LastResponse.                     ; the object:
+     [ Presentation.Presentation     ;   a variant,
+       Answer.Body                   ;   then what
+       Blocker.Block                 ;   it holds
+       Responses.Vector<LastResponse> ] ]
+ [ Presentable.                      ; traits:
+     [ presentation.[ String ] ] ]   ;   as shown
+ [ Presentation.[ Presentable ]      ; associations
+   Block.[ Presentable ]
+   LastResponse.[ Presentable ] ] }
+ ```
```

```datom
+ 
+ ```datom
+ Presentation.{ «A title» }
+ 
+ Answer.«An answer.»
+ 
+ Blocker.{ «A cause»
+           «What unblocks it» }
+ 
+ Responses.[ Answer.«An answer.»
+             Blocker.{ «A cause»
+                       «What unblocks it» } ]
+ ```
```

### Proposal 9: psyche-context › vision/flow.md

  message if it is still the flow in charge.
+ 
+ ## A handover is made from objects
+ 
+ A successor's handover is found among its predecessor's datom objects, or generated from them: the last object of a kind, or every object of a kind.
+ Short term, the handover depends on the kind of objects found or looked for, the aspect, and whether the flow had direct living input, decided by judgment.
+ For example:
+ 

```ethos
+ ```ethos
+ Library.{
+ []                                  ; imports
+ [ Text.String                       ; types
+   Object.[ Finding.Text             ;   an object
+            Doubt.Text ]
+   ObjectKind.[ Findings Doubts ]
+   Search.[ Last.ObjectKind          ;   what is
+            Every.ObjectKind ]       ;   looked for
+   Searches.Vector<Search>
+   Found.Vector<Object>
+   Handover.{ Searches Found } ]
+ [ Worded.[ words.[ String ] ]       ; traits
+   Classed.[ kind.[ ObjectKind ] ]
+   Counted.[ count.[ Integer ] ]
+   Readable.[ reading.[ String ] ] ]
+ [ Object.[ Classed Readable ]       ; associations
+   ObjectKind.[ Worded ]
+   Search.[ Classed ]
+   Handover.[ Readable Counted ] ] }
+ ```
```

```datom
+ 
+ ```datom
+ { [ Last.Findings
+     Every.Doubts ]
+   [ Finding.«A finding»
+     Doubt.«A doubt» ] }
+ ```
```

### Proposal 10: psyche-context › vision/ethos.md

  authored language that debt is removed.
+ 
+ A name says what it names in the system's own words; a word that means something only beside its neighbours, such as First, is not a name.
+ 

```ethos
+ ```ethos
+ Library.{
+ [ signal_flow:[ SystemModules       ; imports
+                 UserModules ] ]
+ [ Prompt.[ System.SystemModules     ; types
+            User.UserModules ] ]
+ [ Named.[ name.[ String ] ] ]       ; traits
+ [ Prompt.[ Named ] ] }              ; associations
+ ```
```

### Proposal 11: psyche-context › vision/ethos.md

  traits, dependencies), then it is allowed at that contact point only.
+ 
+ A capability is named in lowercase camelCase, because it is not a variant: its lowercase first letter tells it from a variant, as a topic's does.
+ 

```ethos
+ ```ethos
+ Library.{
+ [ flow_ethos:[ Brief Titled ] ]     ; imports
+ []                                  ; types
+ [ Rewritable.                       ; traits
+     [ rewriteBrief!{ [ Titled ] [] } ] ]
+ [ Brief.[ Rewritable ] ] }          ; associations
+ ```
```

### Proposal 12: psyche-context › vision/ethos.md

- The unit is File: one file, one Rust module. No namespace inside a
- file. An ethos file is written in the sweet form: the root's head,
- then the sections as siblings, the outer braces omitted. The braced
- form — the root's head opening braces that hold every section — is
- the canonical form. The sweet form is kept out of the main logic run:
- before the text is read as ethos at all, the file is converted
- mechanically to the canonical form, so the ethos reader sees only
- proper ethos.
+ The unit is File: one file, one Rust module.
+ No namespace inside a file.
+ The braced form — the root's head opening braces that hold every section — is the canonical form.
+ A file's usual form is the root's variant, its dot and the brace on one line, then a break, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement.
+ A file holding a single type has no breaks, because it is one thing.

```ethos
- ; the sweet form, as a file is written: the head, then the sections as siblings
- Library
- [ protos:String ]               ; imports
- [ Record.{ String Integer } ]   ; types
- []                              ; traits
- []                              ; associations
- 
- ; the canonical form the reader sees, after the mechanical conversion
- Library.{
-   [ protos:String ]
-   [ Record.{ String Integer } ]
-   []
-   []
- }
+ Library.{
+ []                                  ; imports
+ [ Basket.{ String Integer } ]       ; types
+ [ Emptiable.[ create:[ Self ]       ; traits
+               empty![ Vector<String> ] ] ]
+ [ Basket.[ Emptiable ] ] }          ; associations
```

```ethos
- Type.CommitMessage.[ Landing.Vector<String>
-                      Fix.String ]
+ Type.CommitMessage.[ Landing.Vector<String> Fix.String ]
```

- Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.
+ Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line, save a file holding a single type, which has no breaks.

### Proposal 13: psyche-context › vision/ethos.md

  Terseness is in the low amount of noise, never in shortened words.
+ 
+ Where entries share a category, the category holds a vector of them; no entry repeats its category.
+ 

```ethos
+ ```ethos
+ Library.{
+ [ flow_ethos:[ Prompting ]      ; imports: a trait
+   signal_flow:[ SystemModules   ;   two vectors of
+                 UserModules ] ] ;   ModuleIdentity
+ [ Placements.{ SystemModules      ; types
+                UserModules } ]
+ []                                ; traits
+ [ Placements.[ Prompting ] ] }    ; associations
+ ```
```

```datom
+ 
+ ```datom
+ { [ intent-core ]
+   [ vision-book ] }
+ ```
```

### Proposal 14: psyche-context › vision/ethos.md

  Signal is its own root.
+ 
+ The white square brackets are sugar for a vector, and the white braces for a struct: `⟦ Key ⟧` is `Vector<Key>`, and `⦃ String Integer ⦄` is `{ String Integer }`.
+ Both are read at their own layer and become the plain form before the ethos reader sees the text.
+ 

```ethos
+ ```ethos
+ Library.{
+ []                                  ; imports
+ [ BatchName.String                  ; types
+   Counts.Vector<Integer>
+   Batch.{ BatchName Counts } ]
+ [ Labelled.[ label.[ String ] ]     ; traits
+   Counted.[ count.[ Integer ] ] ]
+ [ Batch.[ Labelled Counted ] ] }    ; associations
+ ```
```

### Proposal 15: psyche-context › vision/flow.md

  own system prompts because they need different prompts.
+ 
+ A subflow's launch names, for each prompt, the vector of modules that goes into it.
+ 

```ethos
+ ```ethos
+ Library.{
+ [ flow_ethos:[ Address Brief      ; imports
+                Layered Prompting ]
+   signal_flow:[ SystemModules
+                 UserModules ] ]
+ [ Subflow.{ Address                 ; types:
+             SystemModules           ;   a launch
+             UserModules
+             Brief } ]
+ []                                  ; traits
+ [ Subflow.[ Prompting Layered ] ] } ; associations
+ ```
```

```datom
+ 
+ ```datom
+ { { Mind illustration Tertiary }
+   [ intent-core ]
+   [ vision-book ]
+   { «A brief» } }
+ ```
```

### Proposal 16: flow › crates/flow-nexus/ethos/curriculum.ethos

```ethos
- Library
+ Library.{
  []
```

```ethos
  []
- []
+ [] }
```

### Proposal 17: flow › crates/flow-nexus/ethos/library.ethos

```ethos
  
- Library [] [ Start.{ OrdinarySocketPath.String MetaSocketPath.String StorePath.String } ] [] []
+ Library.{
+ []
+ [ Start.{ OrdinarySocketPath.String
+           MetaSocketPath.String
+           StorePath.String } ]
+ []
+ [] }
```

### Proposal 18: flow › crates/flow-nexus/ethos/operation.ethos

```ethos
  
- Operation
+ Operation.{
```

```ethos
             LaunchRefused.NativeLaunchRefusal ] ]
- [ PaneLaunch.{ ComposedLaunch HerdrPaneBinding Option<FlowId> Option<NativeSessionId> } ]
+ [ PaneLaunch.{ ComposedLaunch HerdrPaneBinding
+                Option<FlowId>
+                Option<NativeSessionId> } ] }
```

### Proposal 19: flow › crates/flow-nexus/ethos/send_tool.ethos

```ethos
- Library
+ Library.{
  [ signal_flow:[ Address Sender ]
```

```ethos
- []
+ [] }
```

### Proposal 20: flow › crates/flow-nexus/ethos/starter.ethos

```ethos
  
- Library
+ Library.{
```

```ethos
- []
+ [] }
```

### Proposal 21: flow › crates/flow-nexus/ethos/startup.ethos

```ethos
- Library
+ Library.{
  []
```

```ethos
  []
- []
+ [] }
```

### Proposal 22: psyche-context › vision/flow-ethos.md

```ethos
              NoneAbove
+             ; Short term, Flow refuses to start
+             ; a primary without a secondary.
+             NoSecondary
              NotMessage
```

### Proposal 23: psyche-context › vision/flow-ethos.md

```ethos
  Library.{
- []                         ; imports
+ [ flow_ethos:[ Briefing Layered
+                Parted Prompting ] ] ; imports
  [ ModuleIdentity.String    ; types
```

```ethos
    RolesDocument.[ Roles.Roles ] ]
- []                         ; traits
- [] }                       ; associations
+ [ Promptable.              ; traits
+     [ descriptionModule.{ [ Briefing ]
+                           [ DescriptionModule ] }
+       contextModules.{ [ Briefing ]
+                        [ ContextModules ] } ]
+   Seating.
+     [ role.{ [ Layered ]
+              [ Option<RoleDefinition> ] } ] ]
+ [ RoleDefinition.          ; associations
+     [ Promptable Seating
+       Prompting Parted ] ] }
```
