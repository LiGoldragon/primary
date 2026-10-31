Presentation.{ «The implied traits, a draft» }

# The implied traits, a draft

### Proposal 1: The four traits with their capabilities · psyche-belief › vision/ethos.md

**Comment** Created by Fable. Draft: untested in any runtime; the ethosNexus Primary's design supersedes it. Checked with ethos-zero 19.0.0 (main, c9b48dd): it refuses the Library, Rejected at Peer.Address, Undeclared.Address, the Library importing nothing; it checks the Memory file.

  The code we design composes structs; a tuple appears only at a contact point that requires it (standard
  traits, dependencies), and in its one declared case, the newtype.

+ ## The four traits, as a Library the roots import
+
+ Each Ethos root implies one trait on the types it declares, so a Nexus gets its traits without thinking about them: Answerable on an input, Deliverable on an output, Operable on an operation, Memorizable on a record. This draft says what each trait declares, what Ethos Zero generates and what stays hand-written, on one small example.

```ethos
+ Library
+ ; imports
+ []
+ ; types: where an output goes
+ [ Destination.[ Caller
+                 Peer.Address
+                 Translator ] ]
+ ; traits: an input names its one answer;
+ ;   no capability, the pairing is the trait
+ [ Answerable.{ []
+                [ Answer<Deliverable> ]
+                []
+                [] }
+   ; an output knows where it goes
+   Deliverable.[ destination.[ Destination ] ]
+   ; an operation acts on an input
+   ;   and yields outputs
+   Operable.{ []
+              [ Input<Answerable>
+                Output<Deliverable> ]
+              []
+              [ operate!{ [ Input ]
+                          [ Vector<Output> ] } ] }
+   ; a record has a version and its upgrade
+   ;   from the previous shape
+   Memorizable.{ []
+                 [ Previous<Memorizable> ]
+                 [ VERSION.Integer ]
+                 [ upgrade:{ [ Previous ]
+                             [ Self ] } ] } ]
+ ; associations
+ []
```

```rust
+ pub trait Answerable {
+     type Answer: Deliverable;
+ }
+ pub trait Deliverable {
+     fn destination(&self) -> Destination;
+ }
+ pub trait Operable {
+     type Input: Answerable;
+     type Output: Deliverable;
+     fn operate(&mut self, input: Self::Input)
+         -> Vec<Self::Output>;
+ }
+ pub trait Memorizable {
+     type Previous: Memorizable;
+     const VERSION: Integer;
+     fn upgrade(previous: Self::Previous) -> Self;
+ }
```

+ A record. The version lives in the manifest; the upgrade from the previous shape is the one hand-written body, and version 1 has none.

```ethos
+ Memory
+ ; imports
+ [ flow:[ FlowId Address ] ]
+ ; records
+ [ Flow.{ FlowId Address } ]
```

```rust
+ #[derive(Datomizable, Compositional)]
+ pub struct Flow {
+     pub flow_id: FlowId,
+     pub address: Address,
+ }
+ // generated at version 1
+ impl Memorizable for Flow {
+     type Previous = Flow;
+     const VERSION: Integer = 1;
+     fn upgrade(previous: Flow) -> Flow {
+         previous
+     }
+ }
```

  ## Spacing

### Proposal 2: The answers section of Signal · psyche-belief › vision/ethos.md

**Comment** Lands after Proposal 1's lines, before Spacing. Open: Whether the answers section is the right place for the pairing, or the input carries its answers some other way. Whether a reaction declares its destination in ethos, so Deliverable too is generated whole. ethos-zero 19.0.0 cannot check this Signal: it reads a Signal of four sections and refuses the fifth, Arity.{ 4 5 }; the answers section is proposed syntax no ethos-zero yet reads.

+ ## The example: one input, its answers, one reaction
+
+ The pairing of an input with its answers is what Answerable needs from the ethos and what the roots do not yet say. The draft adds it as a Signal's fifth section, answers, placed like associations: the input's name, a dot, a bracket of the outputs that answer it. Every input appears there; an output in no bracket is a reaction.

```ethos
+ Signal
+ ; imports
+ [ flow:[ FlowId Address Pane Message Brief ] ]
+ ; inputs
+ [ Launch.{ Address Brief } ]
+ ; outputs: the two answers to Launch …
+ [ Launched.FlowId
+   Refused.Address
+   ; … and a reaction, to the Translator
+   Prompt.{ Pane Message } ]
+ ; types
+ []
+ ; answers: Launch is answered by one of these
+ [ Launch.[ Launched Refused ] ]
```

```mermaid
+ flowchart TB
+     c["a caller"]
+     i["an input: Launch"]
+     a["its answer: Launched or Refused"]
+     r["a reaction: Prompt"]
+     t["the Translator"]
+     c -- "sends" --> i
+     i -- "is answered at once by" --> a
+     a -- "goes back to" --> c
+     i -- "may set off, in no bracket" --> r
+     r -- "goes to" --> t
```

+ The Rust generated from it: the types, the answer enum, and every trait impl the ethos can fill.

```rust
+ #[derive(Datomizable, Compositional)]
+ pub struct Launch {
+     pub address: Address,
+     pub brief: Brief,
+ }
+ #[derive(Datomizable, Compositional)]
+ pub enum Output {
+     Launched(FlowId),
+     Refused(Address),
+     Prompt(Prompt_Data),
+ }
+ // from the answers section
+ #[derive(Datomizable, Compositional)]
+ pub enum LaunchAnswer {
+     Launched(FlowId),
+     Refused(Address),
+ }
+ // generated whole
+ impl Answerable for Launch {
+     type Answer = LaunchAnswer;
+ }
+ // an answer goes to its caller: generated
+ impl Deliverable for LaunchAnswer {
+     fn destination(&self) -> Destination {
+         Destination::Caller
+     }
+ }
+ // a reaction's destination: hand-written
+ impl Deliverable for Prompt_Data {
+     fn destination(&self) -> Destination {
+         Destination::Translator
+     }
+ }
```

  ## Spacing

### Proposal 3: The acts-on section of Operation · psyche-belief › vision/ethos.md

**Comment** Lands after Proposal 2's lines, before Spacing. Open: How the Operation root declares what an operation acts on; the acts-on section here is the draft's. ethos-zero 19.0.0 checks this Operation file.

+ An operation on it. The ethos declares the actor and what it takes and yields; the body of operate is the one hand-written thing.

```ethos
+ Operation
+ ; imports
+ [ flow:[ Launch LaunchAnswer Capsule ] ]
+ ; operations: the actor that starts flows,
+ ;   holding what it acts with
+ [ Starter.{ Capsule } ]
+ ; types
+ []
+ ; acts on: input and output of each operation
+ [ Starter.{ Launch LaunchAnswer } ]
```

```rust
+ #[derive(Datomizable, Compositional)]
+ pub struct Starter {
+     pub capsule: Capsule,
+ }
+ impl Operable for Starter {
+     // generated from the acts-on section
+     type Input = Launch;
+     type Output = LaunchAnswer;
+     // hand-written: the only body
+     fn operate(&mut self, input: Launch)
+         -> Vec<LaunchAnswer> {
+         todo!()
+     }
+ }
```

+ ## What is generated and what is written
+
+ | trait | generated | hand-written |
+ |---|---|---|
+ | Answerable | the answer enum and the whole impl, from the answers section | nothing |
+ | Deliverable | the impl for every answer: Caller | destination of each reaction |
+ | Operable | Input and Output, the actor wiring | the body of operate |
+ | Memorizable | the impl at version 1; VERSION from the manifest | upgrade, from the second version on |

  ## Spacing
