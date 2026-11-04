Presentation.{ «Version one» }

# Version one

Created by Fable. Records gathered by Sonnet; vocabulary hunted by Sonnet.

Four new modules, each suffixed v1 and self-contained, so a flow can be started on them alone: what a Nexus is, the herdr Nexus, the Flow Nexus, the Belief Nexus. Written against this session's words; older records are set aside where they differ.

### Proposal 1: A Nexus · psyche-belief › vision/nexus-v1.md, a new file

**Comment** What a Nexus is, whole, the translator included. The version is named here once.

+ # A Nexus
+
+ Version 1. Nexus is an architecture; a component built in it has four parts, each its own ethos. The translator is the process of the fourth, Emission.
+
+ ```mermaid
+ flowchart LR
+     s["Signal: what it says"] --> o["Operation: what it attempts"]
+     o --> m["Memory: what it remembers"]
+     m -- "succeeded or failed" --> o
+     o --> e["Emission: what it sends into the world"]
+     e -- "its process, the translator" --> w["world"]
+ ```
+
+ ## An operation is an attempt
+
+ A signal in is an attempt at something; the attempt is the operation. Operation declares one attempt per input, named as the doing, and the outcome each attempt ends in; Signal's output is made from that outcome.
+
+ ```mermaid
+ flowchart LR
+     i["Input: Prompt"] --> a["Attempt: Prompting"]
+     a --> m["Memory: the pane is known"]
+     a --> e["Emission: Herdr call"]
+     m --> r["Outcome: Prompted or Failed"]
+     e --> r
+     r --> o["Output: Prompted.Outcome"]
+ ```
+
+ ## The translator
+
+ The Nexus decodes signal and nothing else. The translator is the process in front of it that speaks text: a datom typed at the CLI comes in through it, and every emission goes out through it.
+
+ ```mermaid
+ flowchart LR
+     c["CLI: one datom"] -- "text" --> t["translator"]
+     t -- "Call.{ Caller Input }, signal" --> n["Nexus"]
+     n -- "Output, signal" --> t
+     t -- "text" --> c
+     n -- "Emission, signal" --> t
+     t -- "the call" --> w["world"]
+     w -- "exit status" --> t
+     t -- "Outcome, signal" --> n
+ ```
+
+ ```ethos
+ Library
+ [ signal:[ Input Output Caller Error ]
+   std:[ Connection ] ]
+ [ Translator.{ NexusSocket.String }   ; the one path it holds
+   Call.{ Caller Input }               ; what the translator sends in
+   Outcome.[ Answered                  ; one reply written back
+             Unreadable.Error          ; the text was not an Input
+             NexusDown ] ]
+ [ Serving.[ serve.{ [ Connection ] [ Outcome ] } ] ]
+ [ Translator.[ Serving ] ]
+ ```
+
+ ## A command line is a type
+
+ What a Nexus sends into the world is a typed value: a variant per subcommand, a field per argument, a String only where a user writes freely. The translator turns the value into the call; it is the one place that holds the words.
+
+ ```ethos
+ Emission
+ []
+ [ Command.{ Verb Vector<Argument> } ]  ; emissions
+ [ Outcome.[ Done Refused.Integer ] ]   ; outcomes
+ [ Verb.[ List Show ]                   ; types
+   Argument.[ Name.String Quiet ] ]
+ [ Arguable.[ argv.[ Vector<String> ] ] ]
+ [ Verb.[ Arguable ]
+   Argument.[ Arguable ]
+   Command.[ Arguable ] ]
+ ```
+
+ ```rust
+ impl Arguable for Verb {
+     fn argv(&self) -> Vec<String> {
+         match self {
+             Verb::List => vec!["list".into()],
+             Verb::Show => vec!["show".into()],
+         }
+     }
+ }
+ impl Arguable for Argument {
+     fn argv(&self) -> Vec<String> {
+         match self {
+             Argument::Name(s) => vec![s.clone()],
+             Argument::Quiet => vec!["--quiet".into()],
+         }
+     }
+ }
+ impl Arguable for Command {
+     fn argv(&self) -> Vec<String> {
+         let mut v = self.verb.argv();
+         for a in &self.argument_vector { v.extend(a.argv()) }
+         v
+     }
+ }
+ impl Emittable for Command {           // trait: generated
+     type Outcome = Outcome;
+     fn emit(&self, t: &Translator) -> Outcome {
+         t.call(&self.argv())
+     }
+ }
+ ```
+
+ ## Two Nexuses
+
+ ```mermaid
+ flowchart LR
+     c["CLI"] -- "datom" --> ta["translator A"]
+     ta -- "signal" --> a["Nexus A"]
+     a -- "Emission, signal" --> ta
+     ta -- "Input of B, signal" --> b["Nexus B"]
+     b -- "Emission, signal" --> tb["translator B"]
+     tb -- "the call" --> w["world"]
+ ```

### Proposal 2: The herdr Nexus · psyche-belief › vision/herdr-nexus-v1.md, a new file

**Comment** The first Nexus to build. It owns the pane; nothing else runs herdr. Usable by hand through its CLI, so it stands on its own before the Flow Nexus exists.

+ # The herdr Nexus
+
+ The herdr Nexus owns every pane. It is the one component that runs herdr; when herdr changes, it changes, and nothing else does. It is built first, because it proves the translator and the CLI alone, and it is kept usable by hand: any flow, or the living, drives a pane through `herdr-nexus 'Prompt.{ … }'`.
+
+ ## Signal
+
+ ```ethos
+ Signal
+ [ herdr:[ Session PaneId Pane Workspace
+           Command Text Keys Outcome ] ]
+ [ Create.Workspace                   ; inputs
+   Start.{ Pane Command }
+   Prompt.{ Pane Text }
+   Press.{ Pane Keys }
+   Close.Pane ]
+ [ Created.Pane                       ; outputs
+   Started.Outcome
+   Prompted.Outcome
+   Pressed.Outcome
+   Closed.Outcome ]
+ []
+ ```
+
+ ## Library
+
+ ```ethos
+ Library
+ []
+ [ Session.String                     ; the herdr session
+   PaneId.String                      ; herdr's name for a pane
+   Pane.{ Session PaneId }
+   Root.String                        ; a directory
+   Variable.{ Name.String Value.String }
+   Workspace.{ Session Root
+               Vector<Variable> }
+   Command.{ Program.String
+             Vector<String> }         ; what starts in the pane
+   Text.String                        ; what is typed
+   Keys.Vector<String>
+   Outcome.[ Done
+             Uncertain
+             Refused.{ Code.Integer
+                       Message.String } ] ]
+ []
+ []
+ ```
+
+ ## Operation
+
+ One attempt per input. An attempt reads and writes Memory and sends one Emission; it ends in its outcome.
+
+ ```ethos
+ Operation
+ [ herdr:[ Pane Workspace Command Text Keys ] ]
+ [ Creating.Workspace                 ; attempts
+   Starting.{ Pane Command }
+   Prompting.{ Pane Text }
+   Pressing.{ Pane Keys }
+   Closing.Pane ]
+ [ Created.Pane                       ; what each ends in
+   Ended                              ;   the emission went out
+   Failed.[ Unknown.Pane              ;   not in Memory
+            StoreRefused ] ]
+ []
+ ```
+
+ ## Emission
+
+ The herdr command line, as a type. The translator turns it into the call.
+
+ ```ethos
+ Emission
+ [ herdr:[ Session PaneId Workspace
+           Command Text Keys Outcome ] ]
+ [ Herdr.{ Session Verb } ]           ; emissions: one call
+ [ Outcome ]                          ; outcomes
+ [ Verb.[ WorkspaceCreate.Workspace   ; types
+          AgentStart.{ PaneId Command }
+          AgentPrompt.{ PaneId Text }
+          Keys.{ PaneId Keys }
+          Kill.PaneId ] ]
+ ```
+
+ ```rust
+ impl Emittable for Herdr {
+     type Outcome = Outcome;
+     fn emit(&self, t: &Translator) -> Outcome {
+         let mut argv = vec!["--session".into(),
+                             self.session.0.clone()];
+         argv.extend(self.verb.argv());
+         t.call(&t.herdr_path, &argv)
+     }
+ }
+ ```
+
+ ## Memory
+
+ ```ethos
+ Memory
+ [ herdr:[ Pane Workspace ] ]
+ [ Known.{ Pane Workspace
+           State.[ Open Closed ] }
+   Answer.[ Succeeded Failed ] ]
+ ```
+
+ ```datom
+ ; typed at the CLI
+ Prompt.{ { main wQ:pT } «Land the messaging line» }
+ ; the reply
+ Prompted.Done
+ ```

### Proposal 3: The Flow Nexus, version 1 · psyche-belief › vision/flow-nexus-v1.md, a new file

**Comment** Vocabulary first, then the smallest Flow Nexus that launches a flow from a complex the user defined. Layers do not exist in it. Routes between flows are version 2.

+ # The Flow Nexus, version 1
+
+ ## Vocabulary
+
+ A flow is one run of a model in a harness. A perma flow is a flow that continues through a succession of runs, one entity across them. A flow complex, said complex, is several flows defined together: each flow's model, harness, workspace and beliefs, and which flow speaks to which. A metaflow is every complex running on one host, with that host's keys and roles; a laptop runs one, a server may run several.
+
+ ## The machine is defined, never built in
+
+ Everything that can be configured is configuration. The Nexus holds the vocabulary a definition is written in, as Ethos types; the user writes definitions in datom, the way Nix defines an operating system; a running flow is a definition in action. A complex is named by the user, and the Nexus runs it without knowing its name beforehand. A definition is one datom of its own: it is added, replaced or removed alone, and the metaflow is the set of them. No layer, role or anatomy is in the Rust.
+
+ ## The vocabulary of a definition
+
+ ```ethos
+ Library
+ [ herdr:[ Pane ]
+   belief:[ ModuleName ] ]
+ [ ComplexName.String
+   FlowName.String
+   Harness.[ Claude Codex ]
+   ModelName.String
+   Effort.[ Low Medium High ]
+   Workspace.[ Path.String             ; a directory that exists
+               Temporary ]             ; made for this run
+   Missing.[ Refuse                     ; what to do when
+             Notice ]                   ;   a belief is absent
+   Beliefs.{ Vector<ModuleName> Missing }
+   Member.{ FlowName Harness ModelName
+            Effort Workspace Beliefs }
+   Complex.{ ComplexName Vector<Member> }
+   FlowId.Integer
+   Brief.String ]
+ []
+ []
+ ```
+
+ ## Signal
+
+ ```ethos
+ Signal
+ [ flow:[ Complex ComplexName FlowName
+          FlowId Brief ModuleName ] ]
+ [ Define.Complex                     ; add or replace one
+   Launch.{ ComplexName FlowName Brief }
+   Stop.FlowId ]
+ [ Defined.ComplexName
+   Launched.FlowId
+   Refused.[ UnknownComplex.ComplexName
+             UnknownFlow.FlowName
+             NoBelief.Vector<ModuleName>
+             HerdrDown
+             BeliefDown ]
+   Stopped.FlowId ]
+ []
+ ```
+
+ ## Emission
+
+ The Flow Nexus runs nothing itself. Its way out is two sockets: the Belief Nexus composes the flow's beliefs into its workspace, the herdr Nexus makes the pane and starts the harness in it. Its translator is the client of both.
+
+ ```ethos
+ Emission
+ [ flow:[ Member Brief FlowId ]
+   herdr:[ Pane Outcome ] ]
+ [ Furnish.{ Member FlowId }           ; beliefs into the workspace
+   Open.{ Member FlowId Brief } ]      ; pane made, harness started
+ [ Furnished.Outcome
+   Opened.{ Pane Outcome } ]
+ []
+ ```
+
+ ## Memory
+
+ ```ethos
+ Memory
+ [ flow:[ Complex FlowId ComplexName FlowName ]
+   herdr:[ Pane ] ]
+ [ Definition.Complex
+   Flow.{ FlowId ComplexName FlowName Pane
+          State.[ Running Ended ] }
+   Answer.[ Succeeded Failed ] ]
+ ```
+
+ ```datom
+ ; the user defines a complex: one datom, added alone
+ Define.{ designer
+          [ { fable Claude claude-fable-5-1 Medium
+               Path.«/home/li/primary»
+               { [ spirit:core vision:nexus-v1 ] Refuse } } ] }
+ Defined.designer
+ ; and launches a flow of it
+ Launch.{ designer fable «Read the version one book» }
+ Launched.7
+ ```

### Proposal 4: The Belief Nexus, version 1 · psyche-belief › vision/belief-nexus-v1.md, a new file

**Comment** Curriculum, rewritten as a Nexus and renamed for what it makes: what a model believes when it starts. Useful on its own at once, as the skill generator for every workspace, and the Flow Nexus's second socket.

+ # The Belief Nexus, version 1
+
+ The Belief Nexus holds the belief modules and furnishes workspaces with them. Belief is the word: what a model believes when it starts. It replaces Curriculum. Its memory is its own; a definition in the Flow Nexus refers to a module by name only, and a name may resolve to nothing: the Belief Nexus answers which names are missing, and what is done about it is the definition's policy, never the Nexus's.
+
+ ## Signal
+
+ ```ethos
+ Signal
+ [ belief:[ Repository ModuleName
+            Workspace Placement ] ]
+ [ Register.Repository                ; a module source
+   Resolve.Vector<ModuleName>
+   Furnish.{ Workspace Vector<ModuleName> } ]
+ [ Registered.Repository
+   Resolved.{ Vector<ModuleName>       ; found
+              Vector<ModuleName> }     ; missing
+   Furnished.{ Placement
+               Vector<ModuleName> }    ; missing, left out
+   Refused.[ UnknownRepository.Repository
+             Unwritable.Workspace ] ]
+ []
+ ```
+
+ ## Library
+
+ ```ethos
+ Library
+ []
+ [ Repository.String                  ; a path holding
+                                      ;   <type>/<subject>.md
+   Kind.[ Spirit Intent Vision
+          Knowledge Role ]
+   ModuleName.{ Kind Subject.String }
+   Workspace.String                   ; the flow's directory
+   Placement.{ SystemPrompt.String    ; the bundle file written
+               Skills.String } ]      ; the skills directory
+ []
+ []
+ ```
+
+ ## Emission
+
+ Furnishing is writing: the spirit and intent modules into one system-prompt bundle, every other module into the harness's skills directory of the workspace.
+
+ ```ethos
+ Emission
+ [ belief:[ Workspace ModuleName Placement ] ]
+ [ Write.{ Workspace Vector<ModuleName> } ]
+ [ Written.Placement ]
+ []
+ ```
+
+ ## Memory
+
+ ```ethos
+ Memory
+ [ belief:[ Repository ModuleName ] ]
+ [ Source.{ Repository Vector<ModuleName> }
+   Answer.[ Succeeded Failed ] ]
+ ```
+
+ ```datom
+ Furnish.{ /home/li/primary
+           [ { Spirit core } { Vision nexus-v1 }
+             { Vision none } ] }
+ Furnished.{ { /home/li/primary/.bundle
+               /home/li/primary/.claude/skills }
+             [ { Vision none } ] }
+ ```

### Proposal 5: The translator stands in the Nexus module · psyche-belief › vision/translator.md, a deleted file

**Comment** Everything about the translator is in Proposal 1; a separate module no longer holds it.

**Destroy** vision/translator.md: its content stands in vision/nexus-v1.md.
