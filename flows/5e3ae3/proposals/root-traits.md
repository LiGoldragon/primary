Presentation.{ «The implied root traits» }

# The implied root traits

### Proposal 1: The traits declared once, the roots' new sections · psyche-belief › vision/ethos.md

**Comment** These proposals build on the rulings landed in 3191a4, whose Associations paragraph stays with the new sentences joined to it. The Operation and Signal fences, each with its proposed section, are refused by ethos-zero 19 as `Arity.{ 4 5 }` and pass without that section. Under Alternative 2 the Signal shown carries an answers and a reactions section in place of deliveries.

  ## Associations

- Signal, Operation and Memory imply traits on the types they declare: each type bears its root's trait, generated with it and never written. A Signal's first section holds its inputs and its second its outputs. An input is Answerable: it names the one output that answers it, sent at once, an acknowledgement at least. An output is Deliverable: it has a destination and leaves the Nexus toward it, expecting nothing back; an output no input names is a reaction. An operation is Operable: an object that acts on what it receives. A record of Memory is Memorizable.
+ Signal, Operation and Memory imply traits on the types they declare: each type bears its root's trait, generated with it and never written. The four traits are declared in Ethos once, in the nexus library, with Archivable, the identity trait every root type bears beneath them; every capability has one default body, written once under its trait, and Ethos Zero emits beside each type the empty impl of its root's trait. A Signal's first section holds its inputs and its second its outputs. An input is Answerable: it names the one output that answers it, sent at once, an acknowledgement at least. An output is Deliverable: it has a destination and leaves the Nexus toward it, expecting nothing back; an output no input names is a reaction. An operation is Operable: an object that acts on what it receives. An Operation declares each operation with the state it acts with, and an acts-on section after the types names the inputs it is given. A record of Memory is Memorizable.

+ The Ethos of the nexus library:

```ethos
+ Library
+ [ :std:[ Byte Path ]                ; imports
+   :rkyv:[ Serializable Deserializable ] ]
+ [ Archive.Vector<Byte>              ; types
+   Fingerprint.Vector<Byte>
+   Frame.{ Integer Archive }
+   Refusal.[ Truncated Malformed ]
+   SocketPath.Path
+   Destination.[ Caller
+                 Peer.SocketPath
+                 Translator ]
+   Memory.Path
+   Failure.[ Absent Conflict Unwritable ]
+   Change.[ Succeeded
+            Failed.Failure ] ]
+ [ Archivable.{                      ; traits
+      [ Sized Serializable Deserializable ]
+      []
+      []
+      [ archive.[ Archive ]
+        fingerprint.[ Fingerprint ] ] }
+   Answerable.{
+      [ Archivable ]
+      [ Answer<Deliverable> ]
+      []
+      [ receive:{ [ Answerable ]
+                  [ Result<Self Refusal> ] } ] }
+   Deliverable.{
+      [ Archivable ]
+      []
+      []
+      [ frame.[ Frame ]
+        destination.[ Destination ] ] }
+   Operable.{
+      [ Archivable ]
+      [ Input<Answerable>
+        Output<Deliverable> ]
+      []
+      [ operate!{ [ Input ]
+                  [ Vector<Output> ] } ] }
+   Memorizable.{
+      [ Archivable ]
+      [ Previous<Memorizable> ]
+      [ VERSION.Integer ]
+      [ remember.{ [ Memorizable ] [ Change ] }
+        forget.{ [ Memorizable ] [ Change ] }
+        upgrade:{ [ Previous ] [ Self ] } ] } ]
+ []                                  ; associations
```

+ The Rust declared once beside it, and the empty impl Ethos Zero emits beside a type of each root:

```rust
+ pub trait Archivable: Sized
+     + rkyv::Archive
+     + for<'a> rkyv::Serialize<Serializer<'a>>
+     + rkyv::Deserialize<Self, Deserializer>
+ {
+     fn archive(&self) -> Archive { /* default */ }
+     fn fingerprint(&self) -> Fingerprint {
+         /* default */
+     }
+ }
+ impl nexus::Archivable for Launch_Data {}
+ impl nexus::Archivable for Starter {}
+ impl nexus::Archivable for Flow {}
```

+ An Operation, each operation declared with what it acts with, and what it acts on:

```ethos
+ Operation
+ [ :flow_nexus_types:[ Capsule        ; imports
+      Launch End ]
+   :nexus:Memory ]
+ [ Starter.{ Capsule Memory }         ; operations
+   Reaper.Memory ]
+ []                                   ; outcomes
+ []                                   ; types
+ [ Starter.[ Launch End ]             ; acts on
+   Reaper.End ]
```

+ A Signal with its deliveries:

```ethos
+ Signal
+ [ :flow_nexus_types:[ Address        ; imports
+      Remembering Brief FlowId
+      Pane Message ] ]
+ [ Launch.{ Address Remembering Brief } ; inputs
+   End.FlowId ]
+ [ Launched.FlowId                    ; outputs
+   Ended
+   Refused.[ NoCapsule AddressBusy UnknownFlow ]
+   Prompt.{ Pane Message }
+   Interrupt.Pane ]
+ []                                   ; types
+ [ Launch.[ Launched Refused ]        ; deliveries
+   End.[ Ended Refused ]
+   Prompt.Translator
+   Interrupt.Translator ]
```

**Alternative 1**

+ A Signal has a deliveries section after the types: an input's line names the outputs that answer it, an output's line names the destination kind of a reaction; every output stands in exactly one line, and Ethos Zero refuses a Signal where one does not.

**Alternative 2**

+ A Signal has an answers section and a reactions section after the types: an input's line names the outputs that answer it, an output's line names the destination kind of a reaction; every output stands in exactly one line, and Ethos Zero refuses a Signal where one does not.

### Proposal 2: Answerable and Deliverable · psyche-belief › vision/signal.md

**Comment** A new section after Input and output; the alternatives differ only in how a reaction to a peer finds its address. Its Answer rests on the deliveries section, and the Signal fence carrying it, in proposal 1, is refused by ethos-zero 19 as `Arity.{ 4 5 }` and passes without that section.

+ ## Answerable and Deliverable
+
+ An input is Answerable: it is received, validated from its frame, or refused as Truncated or Malformed; its Answer is the generated enum of the outputs its line in deliveries names, and the answer goes to its caller. An output is Deliverable: it is framed, its archive length-prefixed as the socket carries it, and it knows its destination: Caller, Peer at its SocketPath, or Translator. Answerable is generated whole.

+ The Rust declared in the nexus library:

```rust
+ pub trait Answerable: Archivable {
+     type Answer: Deliverable;
+     fn receive(frame: Frame)
+         -> Result<Self, Refusal> { /* default */ }
+ }
+ pub trait Deliverable: Archivable {
+     fn frame(&self) -> Frame { /* default */ }
+     fn destination(&self) -> Destination;
+ }
```

**Alternative 1**

+ A reaction to a peer takes its address from the output's one field of type Address; Ethos Zero refuses a Peer reaction with no such field, or with two. So Deliverable too is generated whole.

**Alternative 2**

+ A reaction's destination is hand-written: `destination` is the one body of a reaction, and an answer's destination, the Caller, is generated.

### Proposal 3: An operation is a Kameo actor · psyche-belief › vision/nexus.md

**Comment** The standards that were still to be designed are given: the operation value is the actor's state and an input is a message it operates on. The one real tension: the landed line says a type's root trait is generated with it and never written, while Operable's `operate` is the one hand-written body; this proposal reads the generated impl as the empty default and `operate` as the body it leaves open.

  ## Actors

- The engine inside a Nexus is driven by Kameo actors. The standards
- of their use are still to be designed.
+ The engine inside a Nexus is driven by Kameo actors. Each operation
+ is a Kameo actor whose state is the operation's own value, its Memory
+ among it; an input it acts on is a message to it. Ethos Zero emits
+ the actor and message wiring; `operate` is the one hand-written body
+ of a Nexus: it acts on the input, remembers through its Memory, and
+ yields the answer among its outputs, with any reaction. The Kameo
+ shapes follow the Kameo version the nexus repository pins.

```mermaid
+ flowchart TB
+     i["Input: Answerable"]
+     o["Operation: Operable, an actor"]
+     m["Record: Memorizable"]
+     d["Output: Deliverable"]
+     c["the caller"]
+     t["a peer, or the Translator"]
+     i -- "is operated on by" --> o
+     o -- "remembers or forgets" --> m
+     m -- "answers Succeeded or Failed to" --> o
+     o -- "yields" --> d
+     d -- "answers" --> c
+     d -- "reacts toward" --> t
```

+ The Rust: the trait declared in the nexus library, the wiring Ethos Zero emits, and the body a Nexus writes:

```rust
+ pub trait Operable: Archivable {
+     type Input: Answerable;
+     type Output: Deliverable;
+     fn operate(&mut self, input: Self::Input)
+         -> Vec<Self::Output>;
+ }
+ impl Message<StarterInput> for Starter {
+     type Reply = Vec<Output>;
+     async fn handle(
+         &mut self,
+         input: StarterInput,
+         _: &mut Context<Self, Self::Reply>,
+     ) -> Vec<Output> {
+         self.operate(input)
+     }
+ }
+ use self::Output::{Launched, Prompt, Refused};
+ use self::Refused_Data::NoCapsule;
+ use self::StarterInput::{End, Launch};
+
+ impl Operable for Starter {
+     type Input = StarterInput;
+     type Output = Output;
+     fn operate(&mut self, input: StarterInput)
+         -> Vec<Output> {
+         match input {
+             Launch(launch) => {
+                 let flow = Flow { /* launch */ };
+                 let prompt = Prompt_Data {
+                     /* the brief, to its pane */
+                 };
+                 match flow.remember(self.memory) {
+                     Change::Succeeded => vec![
+                         Launched(flow.flow_id),
+                         Prompt(prompt),
+                     ],
+                     Change::Failed(_) => vec![
+                         Refused(NoCapsule),
+                     ],
+                 }
+             }
+             End(_id) => vec![/* Ended */],
+         }
+     }
+ }
```

### Proposal 4: Memorizable · psyche-belief › vision/memory.md

**Comment** A new section at the end of the module. For now every memory is version 1; the manifest with versions is the step after.

+ ## Memorizable
+
+ A record of Memory is Memorizable. It is remembered or forgotten through the Memory handle, the one handle to a Nexus's store, by the standard change: remembered under its fingerprint, or erased. Memory answers every change with Change: Succeeded, or Failed with its Failure, Absent, Conflict or Unwritable. A record has an Integer VERSION from its manifest, a Previous and an upgrade: per version, the very edit from the previous format. The first version has itself as Previous and identity as upgrade.
+
+ For now every memory is version 1 and Memorizable is generated whole. In the long term a memory has a manifest with versions; Ethos Zero takes Previous from the version before and emits `upgrade` from the edit between the two declarations where the edit is mechanical, a field added with a default or removed; where it is not, `upgrade` is the hand-written body.

+ The Rust declared in the nexus library, and the impl Ethos Zero emits at version 1:

```rust
+ pub trait Memorizable: Archivable {
+     type Previous: Memorizable;
+     const VERSION: Integer;
+     fn remember(&self, memory: Memory)
+         -> Change { /* default */ }
+     fn forget(&self, memory: Memory)
+         -> Change { /* default */ }
+     fn upgrade(previous: Self::Previous) -> Self;
+ }
+ impl nexus::Memorizable for Flow {
+     type Previous = Flow;
+     const VERSION: Integer = 1;
+     fn upgrade(previous: Flow) -> Flow {
+         previous
+     }
+ }
```
