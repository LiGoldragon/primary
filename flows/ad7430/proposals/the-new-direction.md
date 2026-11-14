Presentation.{ «The new direction» }

# The new direction

Created by Fable. Material brought by read subflows and by the Psyche core Secondary 4a2631, Opus, who decided nothing of it. Second version: vision only. Every type a proposal names is defined in it, or named as already defined in a vision module.

Already defined, neither added nor removed, shown as they stand. The Flow Nexus's library, in vision:flow-nexus once Proposal 11 moves it there:

```ethos
Library
[]
[ FlowId.Integer
  Topic.String
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary
          Quaternary ]
  Address.{ Aspect Topic Layer }
  Event.[ Started Stopped ] ]
[]
[]
```

In vision:ethos, a Signal's first two sections generate its two enums, one variant per line:

```ethos
Signal
[]                                                     ; imports
[ Lock.LockRequest  Release.LockId ]                   ; inputs: the variants of Input
[ Locked.Lock  Released.Lock ]                         ; outputs: the variants of Output
[ … ]                                                  ; types
```

In vision:messaging:

```ethos
Priority.[ HardAbrupt MiddleAbrupt Soft ]
```

In vision:model-roles: the layer selects the model, through one declaration.

### Proposal 0: Vision refers only to vision · psyche-belief › vision/psyche.md, under Psyche

**Comment** Ruled today: "vision is vision and it's vision only." It separates what he sees far from what he pursues now; it documents nothing.

+ Vision is what is wanted; it is neither real nor unreal, and it documents nothing. Vision refers only to vision: every type a vision names is defined in a vision module. The horizons separate what he sees long term from what he pursues now so that it arrives more quickly.

### Proposal 1: The way out · psyche-belief › vision/translator.md, a new file

**Comment** The translator is the Nexus's fourth part, the one that speaks text: its own process and repository, started with the Nexus, speaking datom natively, so it needs no translator of its own. The Nexus holds no text: each thing it says to herdr is a typed emission, declared in a root of its own, and the translator makes the text and runs the tool. His comments on the first version, answered in the code: the exit status is the subprocess's, which the translator starts; a trait implementation is an interaction, and each is shown; nothing is named "never", the rule is `emit`; a pane is a `Pane`, defined here; every type is in this proposal.

+ ## The way out
+
+ ```mermaid
+ flowchart LR
+     n["Flow Nexus"] -- "Prompt.{ pane waking }, as signal" --> t["translator, the Nexus's fourth part"]
+     t -- "textualizes waking; runs herdr with pane and text as arguments" --> h["herdr subprocess"]
+     h -- "types text into" --> p["pane"]
+     h -- "exit status" --> t
+     t -- "Emitted.Outcome, as signal" --> n
+ ```
+
+ What the Flow Nexus emits into the world, the fourth root. Every emission bears Emittable, implied, generated with the type and never written, as a Signal's inputs bear Answerable; the interaction is hand-written in the translator.
+
+ ```ethos
+ Emission
+ [ flow:[ Pane Waking Keys Workspace Command ] ]           ; imports: defined below, in the Flow Nexus's library
+ [ Create.Workspace                                         ; emissions: make a pane in a workspace
+   Start.{ Pane Command }                                   ;   start a harness in it
+   Prompt.{ Pane Waking }                                   ;   type a waking into it
+   Press.{ Pane Keys } ]                                    ;   press keys in it
+ [ Created.Pane                                             ; outcomes: the pane herdr made
+   Started.Outcome
+   Emitted.Outcome
+   Pressed.Outcome ]
+ [ Outcome.[ Done                                           ; types: herdr did it, on the pane named
+             Uncertain                                      ;   herdr answered, for a pane not the one named
+             Refused.Refusal ]                              ;   herdr's exit status failed
+   Refusal.{ Code.Integer Message.String } ]
+ ```
+
+ What those inputs carry, in the Flow Nexus's library:
+
+ ```ethos
+ Library
+ [ nexus:[ FlowId Address ] ]                               ; imports: vision:nexus
+ [ Session.String                                           ; types: the herdr session
+   PaneId.String                                            ;   herdr's own name for a pane
+   Pane.{ Session PaneId }                                  ;   what addresses one pane
+   Root.String                                              ;   a directory
+   Environment.Vector<{ Name.String Value.String }>
+   Workspace.{ Session Root Environment }
+   ModelName.String
+   Effort.[ Low Medium High ]
+   SystemPrompt.String
+   Settings.String                                          ;   the harness's settings, as the harness reads them
+   Command.{ ModelName Effort SystemPrompt Settings }       ;   everything a harness is started with
+   Keys.Vector<String>
+   Sender.[ Flow.{ Address FlowId } Living Nexus ]
+   Request.[ Order.String Question.String Words.Vector<String> Result.String Notice.String ]
+   Message.{ Priority Sender Request }                      ;   Priority: vision:messaging
+   Waking.Vector<Message> ]                                 ;   one wake, oldest first
+ []
+ []
+ ```
+
+ The translator's own library: the one value it holds.
+
+ ```ethos
+ Library
+ []
+ [ HerdrPath.String                                         ; the one path the translator holds
+   Text.String                                              ; what herdr types; made from Waking, held by no struct
+   Translator.{ HerdrPath } ]
+ []
+ []
+ ```
+
+ The interaction, hand-written in the translator; the trait is generated with the root.
+
+ ```rust
+ pub trait Emittable { type Outcome; fn emit(&self, translator: &Translator) -> Self::Outcome; }   // generated
+
+ impl Emittable for Prompt {
+     type Outcome = Emitted;
+     fn emit(&self, translator: &Translator) -> Emitted {
+         // Only the waking becomes text. The pane goes into the arguments.
+         let text = Text(self.waking.datomize(Path::root()).protosize().textualize());
+         let output = Command::new(&translator.herdr_path.0)
+             .args(["--session", &self.pane.session.0, "agent", "prompt", &self.pane.pane_id.0, &text.0])
+             .output();
+         let Ok(output) = output else { return Emitted(Outcome::Refused(Refusal::could_not_start())) };
+         if !output.status.success() { return Emitted(Outcome::Refused(Refusal::from(&output))) }
+         Emitted(match Reply::from(&output).names(&self.pane) { true => Outcome::Done, false => Outcome::Uncertain })
+     }
+ }
+ ```
+
+ In, as signal; then what herdr types into the pane:
+
+ ```datom
+ Prompt.{ { main wQ:pT }
+          [ { Soft Flow.{ { Psyche core Primary } 7 } Order.«Land the messaging line» } ] }
+ ```
+
+ ```datom
+ [ { Soft Flow.{ { Psyche core Primary } 7 } Order.«Land the messaging line» } ]
+ ```

### Proposal 2: The way in · psyche-belief › vision/translator.md, the same file

**Comment** The CLI holds one socket path and no type. The connection is the correlation: one connection, one call, one reply; the kernel keeps the pairing and nobody mints a number.

+ ## The way in
+
+ ```mermaid
+ flowchart LR
+     c["CLI: one socket path"] -- "datom text, then half-close" --> t["translator"]
+     t -- "Call.{ Caller Input }, signal, one connection per call" --> n["Nexus"]
+     n -- "Output, signal" --> t
+     t -- "datom text, then close" --> c
+ ```
+
+ ```ethos
+ Library
+ [ signal_flow:signal:[ Input Output ]                     ; imports: the Nexus's generated enums, Proposal 4
+   signal_flow:[ Call Caller ] ]                           ;   the envelope, in the signal repository
+ [ TranslatorSocket.String                                 ; types: the one path the CLI holds
+   NexusSocket.String                                      ;   the one path the translator holds for its Nexus
+   Outcome.[ Answered                                      ;   one reply written back, connection closed
+             Unreadable.Error                              ;   the text did not actualize as Input; the error is the reply
+             NexusDown ] ]
+ [ Serving.[ serve.{ [ Connection ] [ Outcome ] } ] ]      ; traits: one connection, one call, one reply
+ [ Translator.[ Serving ] ]
+ ```
+
+ In the signal repository, the envelope every Nexus decodes:
+
+ ```ethos
+ Caller.{ ProcessId.Integer UserId.Integer }               ; from the connection's peer credentials
+ Call.{ Caller Input }
+ ```
+
+ ```rust
+ impl Serving for Translator {
+     fn serve(&self, mut caller: UnixStream) -> Outcome {
+         let text = Text::read_to_end(&mut caller);                          // the CLI half-closed: EOF ends the request
+         let input: Input = match Potential::<Input>::from(text).actualize(&mut self.budget()) {
+             Ok(input) => input,
+             Err(error) => { caller.write_all(error.datomize(Path::root()).protosize().textualize().as_bytes()); return Outcome::Unreadable(error) }
+         };
+         let who = Caller::from(caller.peer_cred());
+         let Ok(mut nexus) = UnixStream::connect(&self.nexus_socket.0) else { return Outcome::NexusDown };
+         nexus.write_all(&Call { caller: who, input }.archive());           // rkyv, length-prefixed
+         let output: Output = Output::read(&mut nexus);                      // the one answer the Input names
+         caller.write_all(output.datomize(Path::root()).protosize().textualize().as_bytes());
+         Outcome::Answered                                                   // drop closes both
+     }
+ }
+ ```
+
+ The whole CLI:
+
+ ```rust
+ fn main() {
+     let mut translator = UnixStream::connect(TranslatorSocket::configured().0).unwrap();
+     translator.write_all(std::env::args().nth(1).unwrap().as_bytes()).unwrap();
+     translator.shutdown(Shutdown::Write).unwrap();
+     std::io::copy(&mut translator, &mut std::io::stdout()).unwrap();
+ }
+ ```

#### · psyche-belief › vision/nexus.md, under Default clients

- A CLI turns text into Signal: it takes one inline datom as its whole input; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process. A CLI speaks to one Nexus and stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ A CLI takes one inline datom as its whole input and writes it to its translator's socket on one connection, reading the reply on the same connection; the translator turns the text into Signal, identifies the calling process from the connection and carries that identity in the envelope, so a Nexus knows its caller by the process. A CLI holds one socket path and no type; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.

### Proposal 3: Four parts, in repositories of their own · psyche-belief › vision/nexus.md, under Three parts and one path, and under Repositories

**Comment** Ruled today: a part that needs a translator is not a Nexus; the translator is a part. A count of repositories is a fact the next part breaks, so the section says parts and names none.

- A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers.
+ A Nexus has four parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers, Emission is what it sends into the world. The translator is the part that carries Emission and turns text into Signal: its own process, speaking datom natively, so it needs no translator of its own.

- A component has three repositories: its main repository, holding all its code, and two signal repositories — one for the ordinary socket's contract, one for the meta socket's. Shared kinds go into reusable libraries, which are encouraged.
+ A Nexus's parts live in multiple repositories, each part in its own; the repository of a part is named where the part is defined. Shared kinds go into reusable libraries, which are encouraged.

#### · psyche-belief › vision/flow-nexus.md, under Configuration

+ The Flow Nexus emits through an Operation, an object that acts, whose outcome is the translator's answer carried back over the translator's socket.
+
+ ```ethos
+ Operation
+ [ emission:[ Prompt Emitted ] ]                          ; the Nexus's own Emission, Proposal 1
+ [ Emit.Prompt ]                                          ; the actor
+ [ Emitted.Emitted ]                                      ; its outcome
+ ```

### Proposal 4: Each root has an implied namespace, and Ethos resolves imports itself · psyche-belief › vision/ethos.md, under Imports

**Comment** `Input` and `Output` are names no file writes. In their own namespace they reserve nothing in the file's, and the implication is stated once.

+ A root that generates types puts them in an implied namespace named for the root, beside the file's own namespace, which holds only what the file writes. A Signal exports `signal:[ Input Output ]`; Operation and Memory export `operation:` and `memory:` when they generate. Traits are exported by name like types, from the written namespace; the root-implied traits, Answerable, Deliverable, Operable and Memorizable, are defined once in the standard library.
+
+ ```ethos
+ Library
+ [ signal_flow:signal:[ Input Output ]                    ; the implied namespace: what the Signal root generated
+   signal_flow:[ Call Caller ] ]                          ; the written namespace: what the file declares
+ ```
+
+ ```rust
+ pub mod signal { pub enum Input { … } pub enum Output { … } }   // the implied namespace
+ pub struct Call { … }                                            // the written one
+ ```
+
+ Ethos resolves every import while it reads, from the ethos each dependency carries beside its crate, and refuses before any Rust exists; an unresolved import or a doubled name is an Ethos error naming the file and the name.
+
+ ```ethos
+ ImportError.[ UnknownNamespace.Namespace                 ; no such namespace in the registry
+               UnknownName.{ Namespace Name }             ; the namespace exists, exports no such name
+               Collision.{ Namespace Name } ]             ; two declarations of one name in one file
+ Namespace.String
+ Name.String
+ ```

### Proposal 5: The registry · psyche-belief › vision/long/ethos.md, a new section

**Comment** Drawn from his notion of today; placed long because he is not settled on it.

+ Ethos is a Nexus, and reads a file inside a registry, its Memory: each namespace bound to a source, each file known by its root. A source is a repository at a revision or a path. The declarative registry admits only the first, so its resolution is a function of its content alone and every build of it is the same; the development registry is a layer over it that rebinds some namespaces to paths.
+
+ ```ethos
+ Memory
+ []
+ [ Namespace.String
+   Revision.String
+   Source.[ Repository.{ Url.String Revision }
+            Path.String ]
+   Root.[ Library Signal Operation Memory ]
+   Binding.{ Namespace Source Root }
+   Registry.[ Declarative.Vector<Binding>                 ; every Source is Repository
+              Development.{ Declarative.Vector<Binding> Overrides.Vector<Binding> } ] ]
+ ```

### Proposal 6: Each metaflow has its workspace and its tools · psyche-belief › vision/flow-nexus.md, under Starting flows, and under Herdr holds the panes

+ A metaflow's configuration holds its workspace and the tools its flows are launched without; a metaflow that sets no workspace runs in the Nexus's. Curriculum projects a metaflow's skills into that metaflow's workspace, so a workspace holds the skills its flows need.
+
+ ```ethos
+ Tool.String
+ Metaflow.{ Address Option<Root> LeaveOuts.Vector<Tool> }     ; Root: the directory, Proposal 1
+ ```
+
+ ```datom
+ { { Psyche book Quaternary } Some.«/home/li/book» [] }        ; the bookmaker: its own workspace, every tool
+ { { Psyche core Primary } None [ Artifact ] }                 ; the Primary: the Nexus's workspace, no artifact tool
+ ```

- Herdr is the third-party terminal workspace every flow runs in, one pane per flow. Herdr is used as it is.
+ Herdr is the third-party terminal workspace every flow runs in, one pane per flow. Herdr is used as it is: a low-level tool that receives finished commands from the translator and holds no logic of ours; every fact about a launch is the Nexus's, decided on the Nexus's types.

### Proposal 7: A design topic is an organ · psyche-belief › vision/medium/flow-nexus.md, a new section, and vision/model-roles.md

**Comment** Drawn from his words of today, as I read them: the designer's context is the topic and nothing else, and what reaches it has been judged worth its attention by something cheap. Placed medium; the layer words stay until he rules.

+ ## An organ
+
+ A design topic runs as an organ: a complex of flows named by role. The designer, a simplified flow, judges and designs. The assistant takes what needs hands and not design, landings, reports, bugs, and speaks to the designer only when a design question comes out of them. The gate is the Flow Nexus's delivery judgment, run by a System 1 model or a Quaternary on every message to the designer, with the designer's standing brief, answering one question: the designer's desk, the assistant's, or nowhere now. The designer's brief is its own output, a short standing statement of what it is working on.
+
+ ```mermaid
+ flowchart LR
+     m["message"] --> g["gate: System 1 / Quaternary, with the designer's brief"]
+     g -- "design" --> d["designer: Fable, simplified flow"]
+     g -- "hands" --> a["assistant: Opus"]
+     g -- "nowhere now" --> q["queue"]
+     a -- "a design question" --> d
+     d -- "its standing brief" --> g
+ ```
+
+ ```ethos
+ Role.[ Designer Assistant Gate Worker ]
+ Brief.String                                                 ; the designer's standing statement
+ Organ.{ Topic Brief Vector<{ Role Layer Option<Root> }> }    ; Layer selects the model: vision:model-roles
+ ```

### Proposal 8: Each topic rolls its context over on its own · psyche-belief › vision/medium/flow-nexus.md, under An organ

**Comment** His words of today: "each topic will have its own context rollover. We can still have the flow ID separation but the flow IDs would be separated by topics."

+ The unit that refreshes is the topic: each topic's context rolls over on its own, with its own chain of flow ids, and a fresh flow of a topic remembers that topic's records.
+
+ ```ethos
+ Rollover.{ Topic Vector<FlowId> }                            ; one topic's chain, oldest first
+ ```

### Proposal 11: A Nexus vision carries no Nexus's code · psyche-belief › vision/nexus.md, under Three parts and one path, moving to vision/flow-nexus.md

**Comment** vision:nexus says how a Nexus is envisioned, nothing of one in particular. The Flow Nexus's four ethos blocks, Library, Signal, Operation and Memory, and the six-step datom walk under them, move whole from vision:nexus into vision:flow-nexus, where they are that Nexus's vision; one line stays behind.

~ Moved: from vision/nexus.md, under Three parts and one path, to vision/flow-nexus.md, a section The Flow Nexus's parts: the Library, Signal, Operation and Memory blocks and the datom walk, unchanged.

+ Examples are found in the vision of an actual Nexus.

### Proposal 10: What a proposal shows · psyche-belief › vision/proposal.md, under A proposal

**Comment** His rules on the proposal itself, from his comments on "The way out" and from today.

+ Every type a proposal names is in the proposal: added to the module it lands in, added to another module, or shown as it already stands in its vision module, its definition in full; naming a type is not showing it.
+
+ What can be expressed in code is shown as code, with a comment where the code needs one; prose is the comment on the code. A method is shown with the trait it belongs to and that trait's ethos, so its inputs and its yield are read. Code not yet settled is marked tentative. A "never" or an "always" is code: the rule is shown as the code that enforces it.
+
+ ```ethos
+ Text.String                                   ; what herdr types; made from Waking, held by no struct
+ ```
+
+ ```rust
+ let text = Text(self.waking.datomize(Path::root()).protosize().textualize());   // only the waking becomes text
+ ```

### Proposal 9: A flowchart in a proposal is a proposed line · psyche-belief › vision/proposal.md, under A proposal

- A proposal is usually drawn as well as written, and always when it has a shape: what it adds, removes and keeps, in one frame.
+ A proposal is usually drawn as well as written, and always when it has a shape: what it adds, removes and keeps, in one frame. A flowchart in a proposal is a proposed line like any other: it stands under the addition margin of the proposal it belongs to, which names the module it goes to.
