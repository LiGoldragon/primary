# The implied traits, a draft

Created by Fable. Draft: untested in any runtime; the ethosNexus Primary's design supersedes it.

Each Ethos root implies one trait on the types it declares, so a Nexus gets its traits without thinking about them: Answerable on an input, Deliverable on an output, Operable on an operation, Memorizable on a record. This draft says what each trait declares, what Ethos Zero generates and what stays hand-written, on one small example.

## The four traits, as a Library the roots import

```ethos
Library
[]                                                          ; imports
[ Destination.[ Caller Peer.Address Translator ] ]          ; types: where an output goes
[ Answerable.{ [] [ Answer<Deliverable> ] [] [] }           ; traits: an input names its one answer; no capability, the pairing is the trait
  Deliverable.[ destination.[ Destination ] ]               ;   an output knows where it goes
  Operable.{ [] [ Input<Answerable> Output<Deliverable> ]   ;   an operation acts on an input and yields outputs
             [] [ operate!{ [ Input ] [ Vector<Output> ] } ] }
  Memorizable.{ [] [ Previous<Memorizable> ] [ VERSION.Integer ]   ;   a record has a version and its upgrade from the previous shape
                [ upgrade:{ [ Previous ] [ Self ] } ] } ]
[]                                                          ; associations
```

```rust
pub trait Answerable  { type Answer: Deliverable; }
pub trait Deliverable { fn destination(&self) -> Destination; }
pub trait Operable    { type Input: Answerable; type Output: Deliverable; fn operate(&mut self, input: Self::Input) -> Vec<Self::Output>; }
pub trait Memorizable { type Previous: Memorizable; const VERSION: Integer; fn upgrade(previous: Self::Previous) -> Self; }
```

## The example: one input, its answers, one reaction

The pairing of an input with its answers is what Answerable needs from the ethos and what the roots do not yet say. The draft adds it as a Signal's fifth section, answers, placed like associations: the input's name, a dot, a bracket of the outputs that answer it. Every input appears there; an output in no bracket is a reaction.

```ethos
Signal
[ flow:[ FlowId Address Pane Message Brief ] ]   ; imports
[ Launch.{ Address Brief } ]                    ; inputs
[ Launched.FlowId                               ; outputs: the two answers to Launch …
  Refused.Address
  Prompt.{ Pane Message } ]                     ;   … and a reaction, to the Translator
[]                                              ; types
[ Launch.[ Launched Refused ] ]                 ; answers: Launch is answered by one of these
```

The Rust generated from it: the types, the answer enum, and every trait impl the ethos can fill.

```rust
#[derive(Datomizable, Compositional)] pub struct Launch { pub address: Address, pub brief: Brief }
#[derive(Datomizable, Compositional)] pub enum Output { Launched(FlowId), Refused(Address), Prompt(Prompt_Data) }
#[derive(Datomizable, Compositional)] pub enum LaunchAnswer { Launched(FlowId), Refused(Address) }   // from the answers section
impl Answerable for Launch { type Answer = LaunchAnswer; }                                             // generated whole
impl Deliverable for LaunchAnswer { fn destination(&self) -> Destination { Destination::Caller } }   // an answer goes to its caller: generated
impl Deliverable for Prompt_Data { fn destination(&self) -> Destination { Destination::Translator } } // a reaction's destination: hand-written
```

An operation on it. The ethos declares the actor and what it takes and yields; the body of operate is the one hand-written thing.

```ethos
Operation
[ flow:[ Launch LaunchAnswer Capsule ] ]   ; imports
[ Starter.{ Capsule } ]                    ; operations: the actor that starts flows, holding what it acts with
[]                                         ; types
[ Starter.{ Launch LaunchAnswer } ]        ; acts on: input and output of each operation
```

```rust
#[derive(Datomizable, Compositional)] pub struct Starter { pub capsule: Capsule }
impl Operable for Starter {
    type Input = Launch; type Output = LaunchAnswer;                       // generated from the acts-on section
    fn operate(&mut self, input: Launch) -> Vec<LaunchAnswer> { todo!() }  // hand-written: the only body
}
```

A record. The version lives in the manifest; the upgrade from the previous shape is the one hand-written body, and version 1 has none.

```ethos
Memory
[ flow:[ FlowId Address ] ]        ; imports
[ Flow.{ FlowId Address } ]        ; records
```

```rust
#[derive(Datomizable, Compositional)] pub struct Flow { pub flow_id: FlowId, pub address: Address }
impl Memorizable for Flow { type Previous = Flow; const VERSION: Integer = 1; fn upgrade(previous: Flow) -> Flow { previous } }  // generated at version 1
```

## What is generated and what is written

| trait | generated | hand-written |
|---|---|---|
| Answerable | the answer enum and the whole impl, from the answers section | nothing |
| Deliverable | the impl for every answer: Caller | destination of each reaction |
| Operable | Input and Output, the actor wiring | the body of operate |
| Memorizable | the impl at version 1; VERSION from the manifest | upgrade, from the second version on |

## Open

Whether the answers section is the right place for the pairing, or the input carries its answers some other way. Whether a reaction declares its destination in ethos, so Deliverable too is generated whole. How the Operation root declares what an operation acts on; the acts-on section here is the draft's.
