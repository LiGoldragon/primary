Presentation.{ «The translator» Proposal }

# The translator

Created by Fable.

### Proposal 1: The translator of any Nexus · psyche-belief › vision/nexus/1.md

::: comment
You said the translator is not specified, and that it belongs to the Nexus architecture, since every Nexus has one. This replaces the module's section on it: its sockets, text coming in, an emission going out, and what comes back.
:::

- The following conceptual Ethos names composed single-reply observations at the connection boundary. Each translator declares its executable capability and how request preparation and fallible execution produce those observations. The Belief ordinary single-reply contract separates preparation from checked execution and retains native failure evidence in process.

- A Translator holds the socket of the Nexus it speaks for; a Caller is the connection's peer credentials, and a Call is what the translator sends in. An Outcome is Answered, one reply written back, Unreadable, the text was not an Input, or NexusDown.

+ ## The translator's connections

+ ```mermaid
+ flowchart TB
+     c["a CLI: one datom, one connection"] -- "text, to the translator's socket" --> t["translator"]
+     t -- "Call, signal, one connection per call" --> n["Nexus"]
+     n -- "Emitted, signal, on the standing connection" --> t
+     t -- "Observed, signal, on the standing connection" --> n
+     t -- "a program run, a file written, an Input of another Nexus" --> w["the world"]
+ ```

+ The translator opens one standing connection to its Nexus when it starts. Every emission comes down it and every outcome goes back up it.

+ ```ethos
+ Library
+ [ signal:[ Input Output ]
+   emission:[ Emission Outcome ] ]
+ [ ProcessId.Integer
+   UserId.Integer
+   Caller.{ ProcessId UserId }
+   Call.{ Caller Input }
+   EmissionId.Integer
+   Emitted.{ EmissionId Emission }
+   Observed.{ EmissionId Outcome } ]
+ []
+ []
+ ```

+ ## Text in

+ ```mermaid
+ flowchart TB
+     a["the CLI's text"] -- "protosize, datomize, compose" --> i["an Input"]
+     a -- "is no Input" --> u["Unreadable: the error, written back as text"]
+     k["the kernel: the connection's peer"] -- "its process and its login" --> c["Caller"]
+     i -- "with the Caller" --> cl["Call"]
+     c --> cl
+     cl -- "signal" --> n["Nexus"]
+     n -- "Output, signal" --> o["datomize, protosize, textualize"]
+     o -- "text, on the same connection" --> a
+ ```

+ ```rust
+ let input: Input = text.protosize()?.datomize()?.compose(&mut budget)?;
+ let call = Call { caller: connection.peer(), input };
+ let text = nexus.ask(call)?.datomize(Path::root()).protosize().textualize();
+ ```

+ A subscription keeps its connection: each pushed Output is written to it as one datom on one line.

+ ## An emission out

+ An emission is one call into the world. Its type bears Emittable, and its body is that call: a program run, a file written, or an Input sent to another Nexus.

+ ```ethos
+ Library
+ [ std:[ Answerable ] ]
+ [ ExitStatus.Integer
+   Run.[ Exited.{ ExitStatus Output.String }
+         Unstartable
+         Uncertain ]
+   Written.[ Done Unwritable ]
+   Reply.[ Answered Down Uncertain ] ]
+ [ Arguable.[ argv.[ Vector<String> ] ]
+   Writable.[ path.[ String ]
+              content.[ String ] ]
+   Translating.[ run.{ [ Arguable ] [ Run ] }
+                 write.{ [ Writable ] [ Written ] }
+                 ask.{ [ Answerable ] [ Reply ] } ]
+   Emittable.{ []
+               [ Outcome ]
+               []
+               [ emit.{ [ Translating ] [ Outcome ] } ] } ]
+ []
+ ```

+ Tentative in one place: Answered carries the Output that answers the Input asked.

+ ```mermaid
+ flowchart TB
+     n["Nexus: Emitted, an id and an emission"] --> t["translator: emit"]
+     t -- "run: the command line, from Arguable" --> p["a program"]
+     t -- "write: the content, from Writable" --> f["a file"]
+     t -- "ask: an Input, signal" --> b["another Nexus"]
+     p -- "exit status and output" --> o["the emission's own Outcome"]
+     f -- "written or not" --> o
+     b -- "its Output" --> o
+     o -- "Observed, the same id" --> n
+ ```

+ Emissions run side by side, each answered by its id.

+ ## What comes back

+ Every emission has an outcome type of its own, and each has the case of a call begun whose end was not seen.

+ ```mermaid
+ flowchart TB
+     e["a call begun"] -- "its end is seen" --> k["the outcome it had"]
+     e -- "the time allowed passes, or the connection drops" --> u["Uncertain"]
+     u -- "goes to the Operation, which decides" --> o["the attempt's outcome"]
+ ```

+ The translator emits an uncertain emission once. An emission that finds no translator connected ends its attempt as unavailable.

+ ## What a translator is configured with

+ ```ethos
+ Signal
+ []
+ [ Configure.Set ]
+ [ Configured.Set ]
+ [ Milliseconds.Integer
+   ProgramName.String
+   Path.String
+   PeerName.String
+   Set.[ CallTimeout.Milliseconds
+         Program.{ ProgramName Path }
+         Peer.{ PeerName Path } ] ]
+ ```

+ ```datom
+ Configure.Peer.{ capsule «/run/user/1001/nexus/main/capsule.sock» }
+ Configure.CallTimeout.20000
+ ```

### Proposal 2: The Flow Nexus's emissions · psyche-belief › vision/flow-nexus/1.md

::: comment
What is the Flow Nexus's own: each emission as the one call it is, the outcome each has, and the order a launch makes them in. The six emissions that stood each hid several calls and shared one outcome.
:::

- ```ethos
- Emission
- [ flow:[ Member Address FlowId Brief Waking Tools
-          Workspace HarnessName Roster RosterChange
-          ComplexName ]
-   herdr:[ Pane Outcome ] ]
- [ Furnish.{ Member FlowId }
-   Settle.{ Member FlowId }
-   Open.{ Member Identity Roster Brief }
-   Wake.{ Pane Waking }
-   Tell.{ Pane RosterChange }
-   Close.{ Pane Workspace } ]
- [ Furnished.Outcome
-   Settled.Outcome
-   Opened.{ Pane Outcome }
-   Woken.Outcome
-   Told.Outcome
-   Closed.Outcome ]
- [ Identity.{ ComplexName Address FlowId }
-   Settings.{ HarnessName Tools Model.String } ]
- ```

+ ```ethos
+ Emission
+ [ flow:[ FlowId Address Brief Waking Tools HarnessName
+          ModelName Effort FeatureName ModuleName
+          Roster RosterChange ComplexName ]
+   belief:[ Location ]
+   capsule:[ Pane Variable ] ]
+ [ MakeWorkspace.FlowId
+   Furnish.{ WorkspacePath HarnessName Vector<ModuleName> }
+   Settle.{ FlowId Settings }
+   CreatePane.{ WorkspacePath Vector<Variable> }
+   StartHarness.{ Pane Launch }
+   Type.{ Pane Prompt }
+   ClosePane.Pane
+   RemoveWorkspace.WorkspacePath ]
+ [ WorkspaceMaking.[ Made.WorkspacePath Unwritable ]
+   Furnishing.[ Furnished.{ Location Missing.Vector<ModuleName> }
+                BeliefRefused
+                BeliefDown ]
+   Settling.[ Settled.SettingsPath Unwritable ]
+   PaneCreating.[ Created.Pane CapsuleRefused CapsuleDown Uncertain ]
+   HarnessStarting.[ Started CapsuleRefused CapsuleDown Uncertain ]
+   Typing.[ Typed CapsuleRefused CapsuleDown Uncertain ]
+   PaneClosing.[ Closed CapsuleRefused CapsuleDown Uncertain ]
+   WorkspaceRemoving.[ Removed Unwritable ] ]
+ [ WorkspacePath.String
+   SettingsPath.String
+   SessionId.String
+   HookName.String
+   Identity.{ ComplexName Address FlowId }
+   Settings.{ HarnessName FlowId Tools ModelName Vector<HookName> }
+   Launch.{ HarnessName
+            SessionId
+            ModelName
+            Effort
+            Location
+            SettingsPath
+            Vector<FeatureName> }
+   Prompt.[ First.{ Identity Roster Brief Waking }
+            Waking
+            RosterChange ] ]
+ ```

+ ## A launch, call by call

+ ```mermaid
+ flowchart TB
+     l["Launch: the attempt Launching"] -- "the Nexus draws the session id; the flow id is its hash" --> w["MakeWorkspace, when the workspace is Temporary"]
+     w --> f["Furnish: the default modules, then the member's own"]
+     f -- "modules missing and the member says Refuse" --> r["Refused.NoBelief"]
+     f --> s["Settle: the settings file, its hooks naming the flow id"]
+     s --> c["CreatePane: the workspace, and the variables its features set"]
+     c --> h["StartHarness"]
+     h -- "Memory: the flow, Running" --> t["Type: the first prompt"]
+     t --> d["Launched.FlowId"]
+     h -- "any call after CreatePane fails" --> u["ClosePane, then RemoveWorkspace when Temporary"]
+ ```

+ Every prompt, the first one included, is typed into the pane by the one emission Type.

+ ## Furnish: an Input of the Belief Nexus

+ ```rust
+ impl Emittable for Furnish {
+     type Outcome = Furnishing;
+     fn emit(&self, translator: &impl Translating) -> Furnishing {
+         let furnish = belief::Input::Furnish(self.workspace_path.clone(), self.harness_name.clone(), self.module_name_vector.clone());
+         match translator.ask(furnish) {
+             Reply::Answered(belief::Output::Furnished(location, missing)) => Furnishing::Furnished(location, missing),
+             Reply::Answered(_) => Furnishing::BeliefRefused,
+             Reply::Down | Reply::Uncertain => Furnishing::BeliefDown,
+         }
+     }
+ }
+ ```

+ ## Settle: a file written

+ The settings file is the harness's own; it carries the tools, the model and one hook for each event the Flow Nexus is configured to hear. For the Claude harness:

+ ```json
+ { "model": "claude-fable-5-1",
+   "permissions": { "allow": [], "deny": [ "Bash" ] },
+   "hooks": { "Stop": [ { "hooks": [ { "type": "command", "command": "flow-hook 15c0ce Stop" } ] } ] } }
+ ```

+ ```rust
+ impl Emittable for Settle {
+     type Outcome = Settling;
+     fn emit(&self, translator: &impl Translating) -> Settling {
+         match translator.write(&self.settings) {
+             Written::Done => Settling::Settled(self.settings.path()),
+             Written::Unwritable => Settling::Unwritable,
+         }
+     }
+ }
+ ```

+ ## StartHarness: an Input of the Capsule Nexus

+ The command line is made from the harness's definition alone: its program, the flag of each slot, and the flag of each feature the member and its complex name. A feature whose effect is a variable is set on the pane at CreatePane.

+ ```ethos
+ Library
+ [ flow:[ HarnessName Feature ] ]
+ [ Program.String
+   SlotName.[ Session Model Effort SystemPrompt Settings ]
+   Slot.{ SlotName Flag.String }
+   Harness.{ HarnessName Program Vector<Slot> Features.Vector<Feature> } ]
+ []
+ []
+ ```

+ ```datom
+ Define.Harness.{
+    claude
+    «claude»
+    [ { Session «--session-id» }
+      { Model «--model» }
+      { Effort «--effort» }
+      { SystemPrompt «--system-prompt-file» }
+      { Settings «--settings» } ]
+    [ { ClaudeMd Environment.{ CLAUDE_CODE_DISABLE_CLAUDE_MDS 1 } } ] }
+ ```

+ ```rust
+ impl Emittable for StartHarness {
+     type Outcome = HarnessStarting;
+     fn emit(&self, translator: &impl Translating) -> HarnessStarting {
+         let start = capsule::Input::Start(self.pane.clone(), self.launch.command(), self.launch.label());
+         match translator.ask(start) {
+             Reply::Answered(capsule::Output::Started(capsule::Outcome::Done)) => HarnessStarting::Started,
+             Reply::Answered(_) => HarnessStarting::CapsuleRefused,
+             Reply::Down => HarnessStarting::CapsuleDown,
+             Reply::Uncertain => HarnessStarting::Uncertain,
+         }
+     }
+ }
+ ```

+ ```datom
+ Rehearse.{ designer fable «Read the version one book» }
+ Rehearsed.«claude --session-id 15c0cea2-aa34-508b-8e20-ece1ab7823f4 --model claude-fable-5-1 --effort medium --system-prompt-file /home/example/work/.bundle --settings /home/example/state/flows/15c0ce/settings.json»
+ ```

+ ## Type: text made from a typed prompt

+ ```rust
+ impl Emittable for Type {
+     type Outcome = Typing;
+     fn emit(&self, translator: &impl Translating) -> Typing {
+         let text = capsule::Text(self.prompt.datomize(Path::root()).protosize().textualize());
+         match translator.ask(capsule::Input::Prompt(self.pane.clone(), text)) {
+             Reply::Answered(capsule::Output::Prompted(capsule::Outcome::Done)) => Typing::Typed,
+             Reply::Answered(_) => Typing::CapsuleRefused,
+             Reply::Down => Typing::CapsuleDown,
+             Reply::Uncertain => Typing::Uncertain,
+         }
+     }
+ }
+ ```

+ A typing that ends Uncertain is not typed again: the text may be in the pane.

### Proposal 3: A hook's report and a flow's response · psyche-belief › vision/flow-nexus/1.md

::: comment
How what the harness announces becomes an Input, and how a flow that only writes still acts. The hook also carries the context size, which the vision left with no source.
:::

+ ## The hook

+ ```mermaid
+ flowchart TB
+     h["the harness runs: flow-hook 15c0ce Stop, the event as JSON"] --> k["flow-hook"]
+     k -- "SessionStart" --> a["Report: Started"]
+     k -- "UserPromptSubmit" --> b["Report: Working"]
+     k -- "Stop: the last message" --> c["Report: Responded"]
+     k -- "Stop: the usage of the transcript's last answer" --> d["Report: Context"]
+     k -- "Stop" --> e["Report: Idle"]
+     k -- "SessionEnd" --> f["Report: Ended"]
+     a --> t["the translator's socket, as text"]
+     b --> t
+     c --> t
+     d --> t
+     e --> t
+     f --> t
+ ```

- ```ethos
-   Event.[ Started Idle Working Ended
-           Responded.String
-           Warned
-           Threshold ] ]
- ```

+ ```ethos
+ Types
+ [ Tokens.Integer
+   Event.[ Started Idle Working Ended
+           Responded.String
+           Context.Tokens ] ]
+ ```

+ ```datom
+ Report.{ 15c0ce Responded.«Reviewed; green.» }
+ Report.{ 15c0ce Context.183950 }
+ Report.{ 15c0ce Idle }
+ ```

+ The Nexus holds each model's threshold and compares; the warning and the replacement are its own acts.

+ ## A response that is an Input

+ ```mermaid
+ flowchart TB
+     r["Report: Responded, the response whole"] --> t["translator"]
+     t -- "the Report itself" --> n["Nexus: the response is kept"]
+     t -- "the response, read as one datom of Input" --> q["is it an Input?"]
+     q -- "yes: a second Call, the same Caller" --> n
+     q -- "no" --> x["nothing more"]
+ ```

+ ```rust
+ if let Input::Report(_, Event::Responded(response)) = &input {
+     if let Ok(written) = response.protosize().and_then(|protos| protos.datomize()).and_then(|datom| datom.compose::<Input>(&mut budget)) {
+         nexus.ask(Call { caller: caller.clone(), input: written })?;
+     }
+ }
+ ```
