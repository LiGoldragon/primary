Presentation.{ «The metaflow, version 1» }

# The metaflow, version 1

Created by Fable, at his word: "Imagine the whole thing running. Just take it all the way, with the herder and the belief thing." The whole on one host, fully developed within version 1, as I see it; landed unreviewed for his review and for Codex to build.

### Proposal 1: The metaflow · psyche-belief › vision/metaflow-v1.md, a new file

**Comment** The new module: what runs on one host, how it is configured, and how the Nexuses are started so several metaflows run side by side.

+ # The metaflow
+
+ Version 1. A metaflow is everything running on one host for one owner: three Nexuses, the definitions they run, and the flows running from them. A host may run several, each under its own name and directory.
+
+ ```mermaid
+ flowchart TB
+     d["definitions: one datom file per complex"] -- "Define, through the CLI" --> f["Flow Nexus"]
+     f -- "Furnish, signal" --> b["Belief Nexus"]
+     f -- "Create, Start, Prompt, signal" --> h["herdr Nexus"]
+     b -- "writes the bundle and the skills" --> w["workspace"]
+     h -- "runs herdr" --> p["pane: the harness, the flow"]
+     p -- "Report, through the CLI, from a hook" --> f
+     l["the living, at a CLI"] -- "Say" --> f
+ ```
+
+ ## A metaflow is a directory
+
+ A metaflow has a name and a directory, and nothing of it is read from the environment. The directory holds the sockets of its Nexuses, their memories and its definitions. A Nexus is started with one datom, its place; a CLI takes the metaflow's name and finds the sockets in the directory. Two metaflows are two directories, and the stable one keeps running while the next is tried.
+
+ ```ethos
+ Library
+ []
+ [ MetaflowName.String                ; main, next
+   Directory.String                   ; …/metaflow/main
+   Place.{ MetaflowName Directory } ] ; what every Nexus starts with
+ []
+ []
+ ```
+
+ ```datom
+ ; each Nexus, started by the metaflow's shell
+ { main /run/user/1001/metaflow/main }
+ ; the sockets it makes there
+ ; flow.sock  flow-meta.sock  flow-translator.sock
+ ; herdr.sock herdr-meta.sock herdr-translator.sock
+ ; belief.sock belief-meta.sock belief-translator.sock
+ ```
+
+ ```sh
+ # the CLI: the metaflow's name, then one datom
+ flow main 'Launch.{ designer fable «Read the book» }'
+ herdr main 'Prompt.{ { main wQ:pT } «hello» }'
+ ```
+
+ ## The metaflow is a Nix shell
+
+ The repository metaflow holds the Nix that builds the three Nexuses, their translators and CLIs, and a shell that starts them in a named directory under the owner's login. It is not a sandbox: a flow in it has the owner's credentials and files. A second shell with a second name is a second metaflow.
+
+ ```sh
+ nix develop github:LiGoldragon/metaflow -- metaflow start next
+ ```
+
+ ## Everything in a metaflow is a definition
+
+ The Nexuses hold vocabulary; the owner writes definitions in datom. A definition is one file, one datom, given to the Flow Nexus by Define and replaced the same way; the running set of definitions is the metaflow's memory, and a change to one definition touches no other. The Rust knows no layer, role, model name or topic.
+
+ ```datom
+ ; definitions/designer.datom: one complex
+ { designer
+   [ { fable Claude claude-fable-5-1 Medium Perma
+       Path.«/home/li/primary»
+       { [ { Spirit core } { Vision nexus-v1 } ] Refuse }
+       { [ Bash Edit ] [ Artifact ] }
+       [ Speaks.opus Speaks.Living ] }
+     { opus Claude claude-opus-4 Medium Ephemeral
+       Temporary
+       { [ { Spirit core } { Role worker } ] Notice }
+       { [] [] }
+       [ Speaks.fable Speaks.Complex.implementer ] } ]
+   fable }                            ; the speaker
+ ```

### Proposal 2: The complex, whole · psyche-belief › vision/flow-nexus-v1.md

**Comment** The complex grows from a list of members to the thing he described: members with routes, a speaker, continuity, tools, and a reader of responses.

  ## The vocabulary of a definition

+ A complex is members, routes and a speaker. A member is one flow definition: its harness, model and effort; whether it is a perma flow or ephemeral; its workspace, beliefs and tools; and whom it speaks to. The speaker is the member that receives what comes to the complex from outside. A route names whom a member may address: another member, another complex, or the living; a message off the routes is refused.
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
+   Continuity.[ Perma                 ; continues through runs
+                Ephemeral ]           ; one run, then gone
+   Workspace.[ Path.String
+               Temporary ]            ; made at launch, removed at end
+   Missing.[ Refuse Notice ]
+   Beliefs.{ Vector<ModuleName> Missing }
+   Tool.String                        ; the harness's name for it
+   Tools.{ Allow.Vector<Tool> Deny.Vector<Tool> }
+   Route.[ Speaks.FlowName             ; a member of this complex
+           Complex.ComplexName         ;   that complex's speaker
+           Living ]
+   Member.{ FlowName Harness ModelName Effort
+            Continuity Workspace Beliefs Tools
+            Vector<Route> }
+   Complex.{ ComplexName Vector<Member>
+             Speaker.FlowName }
+   FlowId.Integer
+   Address.{ ComplexName FlowName }   ; a perma flow's standing name
+   Brief.String ]
+ []
+ []
+ ```
+
+ ```mermaid
+ flowchart TB
+     c["complex: designer"] --> s["speaker: fable"]
+     s -- "Speaks.opus" --> o["member: opus"]
+     o -- "Speaks.Complex.implementer" --> i["complex: implementer, its speaker"]
+     s -- "Speaks.Living" --> l["the living"]
+     x["anything else"] -. "refused" .-> s
+ ```
+
+ ## A message takes a route
+
+ A flow sends through the CLI; the Flow Nexus checks the route against the sender's definition, queues the message for the receiver, and delivers it through the herdr Nexus as a prompt when the receiver is idle or the priority is pressing. A perma flow asleep is woken by a pressing message and receives its whole queue in its first prompt. The living speaks to a complex with Say, which reaches its speaker.
+
+ ```ethos
+ Library
+ [ flow:[ FlowId Address ComplexName ] ]
+ [ Priority.[ HardAbrupt MiddleAbrupt Soft ]
+   Request.[ Order.String Question.String
+             Words.Vector<String>
+             Result.String Notice.String ]
+   Sender.[ Flow.FlowId Living Nexus ]
+   Message.{ Priority Sender Request }
+   Waking.Vector<Message> ]           ; a queue delivered whole
+ []
+ []
+ ```
+
+ ## The Nexus reads what a flow says
+
+ Every harness event reaches the Flow Nexus through a hook calling the CLI: Report carries the flow's state, and a flow's finished response. A response that actualizes as an Input of the Flow Nexus, a Send among them, is acted on as if the flow had typed it at the CLI; any other response is kept as the flow's word and acted on by nobody. So a member that only thinks and talks, with no tool, still sends, launches and stops by writing a datom.
+
+ ```mermaid
+ flowchart TB
+     r["flow's response, as text"] -- "Report, from the hook" --> t["translator"]
+     t -- "actualizes as Input?" --> y["yes: the Input, as signal"]
+     t -- "no" --> n["Heard: kept, nothing acted"]
+     y --> f["Flow Nexus acts"]
+ ```
+
+ ## A perma flow continues
+
+ A perma flow is refreshed when its context passes its model's threshold, configured per model in the Flow Nexus: the flow is told to write its handover, its successor is launched with the same definition, the handover as its first prompt, and the queue that gathered meanwhile; the predecessor ends. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.
+
+ ## Signal
+
+ ```ethos
+ Signal
+ [ flow:[ Complex ComplexName FlowName FlowId
+          Address Brief ModuleName Message
+          Request Priority Tool ] ]
+ [ Define.Complex                     ; add or replace one
+   Undefine.ComplexName
+   Launch.{ ComplexName FlowName Brief }
+   Stop.FlowId
+   Send.{ FlowId Address Priority Request }
+   Say.{ ComplexName Request }        ; the living, to a speaker
+   Report.{ FlowId Event }            ; from a harness hook
+   Subscribe ]                        ; events, as they happen
+ [ Defined.ComplexName
+   Undefined.ComplexName
+   Launched.FlowId
+   Stopped.FlowId
+   Sent.[ Delivered Queued ]
+   Said.[ Delivered Queued ]
+   Reported
+   Subscribed
+   Refused.[ UnknownComplex.ComplexName
+             UnknownFlow.FlowName
+             NoRoute.{ FlowId Address }
+             NoBelief.Vector<ModuleName>
+             HerdrDown BeliefDown
+             Running.Address ] ]
+ [ Event.[ Started Idle Working Ended
+           Responded.String            ; the response, whole
+           Threshold ] ]              ;   context past its mark
+ ```
+
+ ## Emission
+
+ The Flow Nexus runs nothing. Its translator is the client of two sockets: the Belief Nexus furnishes the workspace; the herdr Nexus makes the pane, starts the harness, types the prompt. The harness's command line and its settings file are types; the translator writes them.
+
+ ```ethos
+ Emission
+ [ flow:[ Member FlowId Brief Waking Tools ]
+   herdr:[ Pane Outcome ] ]
+ [ Furnish.{ Member FlowId }           ; beliefs into the workspace
+   Settle.{ Member FlowId }            ; the harness's settings file
+   Open.{ Member FlowId Brief }        ; pane made, harness started
+   Wake.{ Pane Waking }                ; the queue typed in
+   Close.{ Pane Workspace } ]          ; pane killed, Temporary removed
+ [ Furnished.Outcome
+   Settled.Outcome
+   Opened.{ Pane Outcome }
+   Woken.Outcome
+   Closed.Outcome ]
+ [ Settings.[ Claude.{ Tools Model.String }   ; what the translator writes
+              Codex.{ Tools Model.String } ] ]
+ ```
+
+ ## Memory
+
+ ```ethos
+ Memory
+ [ flow:[ Complex ComplexName FlowName FlowId
+          Address Message Event ]
+   herdr:[ Pane ] ]
+ [ Definition.Complex
+   Flow.{ FlowId Address Pane
+          State.[ Running Idle Ended ]
+          Vector<Event> }
+   Queue.{ Address Vector<Message> }
+   Threshold.{ Model.String Tokens.Integer }
+   Answer.[ Succeeded Failed ] ]
+ ```

### Proposal 3: The herdr Nexus, whole · psyche-belief › vision/herdr-nexus-v1.md

**Comment** Two additions: the Nexus watches its panes, and a pane is named by what runs in it.

  ## Signal

+ The herdr Nexus also observes: a pane's state is read from herdr and pushed to subscribers as it changes, so the Flow Nexus learns a harness has died without a hook. A pane carries a label, the address of the flow in it, so a listing reads as the metaflow does.
+
+ ```ethos
+ Signal
+ [ herdr:[ Session PaneId Pane Workspace
+           Command Text Keys Outcome Label ] ]
+ [ Create.Workspace
+   Start.{ Pane Command Label }
+   Prompt.{ Pane Text }
+   Press.{ Pane Keys }
+   Close.Pane
+   List.Session
+   Subscribe.Session ]
+ [ Created.Pane
+   Started.Outcome
+   Prompted.Outcome
+   Pressed.Outcome
+   Closed.Outcome
+   Listed.Vector<{ Pane Label State }>
+   Subscribed
+   Changed.{ Pane State } ]           ; pushed, each change
+ [ Label.String
+   State.[ Open Busy Idle Dead ] ]
+ ```

### Proposal 4: The Belief Nexus, whole · psyche-belief › vision/belief-nexus-v1.md

**Comment** One addition: belief changes live. The Nexus watches its repositories and refurnishes every workspace that holds a changed module; Curriculum's deploy step is gone.

  ## Signal

+ A registered repository is watched: when its main moves, every workspace furnished with a module it changed is furnished again, and the Flow Nexus is told which flows now run on old belief, so a perma flow can be refreshed on it. A module is named by kind and subject; its placement, system prompt or skill, is read from the module's own front matter.
+
+ ```ethos
+ Signal
+ [ belief:[ Repository ModuleName
+            Workspace Placement ] ]
+ [ Register.Repository
+   Resolve.Vector<ModuleName>
+   Furnish.{ Workspace Vector<ModuleName> }
+   Subscribe ]
+ [ Registered.Repository
+   Resolved.{ Vector<ModuleName>
+              Vector<ModuleName> }
+   Furnished.{ Placement Vector<ModuleName> }
+   Subscribed
+   Changed.{ Repository                ; pushed: main moved
+             Vector<ModuleName>        ;   modules changed
+             Vector<Workspace> }       ;   workspaces refurnished
+   Refused.[ UnknownRepository.Repository
+             Unwritable.Workspace ] ]
+ []
+ ```
