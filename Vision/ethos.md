# Ethos

## What Ethos is

Ethos is the schema language. Of the two main syntaxes most agents
will face, Ethos specifies the types and Datom fills them with data.

## Why Ethos

Existing text data formats and existing programming languages both
fail. Rust is the new assembly, read in full by no one; Ethos is the
concise, dense, cognitively concentrated language for writing code
with AI agents — easy to read and write, showing the interfaces: the
main types and the main traits. Behavior falls under traits, which
creates an ontology in code.

## Generation

Ethos generates the Rust. Rust generated from ethos is committed, so
ordinary tooling — language servers — works normally; a freshness
mechanism is deliberately left open.

## Non-repetition

Any repetition in ethos syntax is an implementation failure. Ethos
aims to be the most terse, non-repetitive syntax ever made.

## Self-description

A datom object's basic CLI help emits the Ethos that describes its
anatomy. The wanted mechanism extends this: point at any object —
CLI now, Mentci later — and its Ethos prints, self-describing and
self-evident. The schema syntax serves two audiences: it trains
agents to use things properly, and it shows where the design is
lacking.

## Horizon

Ethos will eventually replace everything, Rustlang becoming its
assembly layer. Designs are chosen for that horizon; what it
enables — generator emission among it — comes in its time.

## Kind

Kind is the word for the bearer of capabilities: something that can
run is a runner, Runnable is its kind, and run is its capability, a
function the kind has. Trait is set aside as acoustically ambiguous.
In ethos there are no generics, only kinds. Declaring a new kind
declares a new trait in the Rust world and might imply more in the
ethos world.

## Naming

Kinds are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a kind. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

## Identity

A kind is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. A constraint is a kind, or a bracket of kinds: what
Rust writes as a generic parameter with its bounds, ethos writes as
the bounds alone, since in ethos there are no generics, only kinds; a
constraint in a kind declaration is a kind, never a type. Two heads
that differ in a constraint are two kinds. Which constraints belong
to the identity is not a decision to make: the ethos compiles to
Rust, and what identifies the trait identifies the kind. What else a
kind declares, its superkinds, its associated types and constants,
its capabilities, is its definition. Angle brackets hold the
constraints; they are a protos delimiter, recycled from Rust as
Result and Self are.

```
Library.{
  {0 1 0}
  [ protos:[Text Textualizable] ]                             ; imports
  [ Record.{ Text Integer }                                   ; types: a struct of two fields
    Report.{ Text Vector<Integer> } ]                         ;   another
  [ Processable<[Clonable Sendable] Serializable>.[ … ] ]     ; kinds: the head is the identity, the name and two constraints,
                                                              ;   the first a bracket of two kinds, the second one kind;
                                                              ;   the bracket after the dot holds its capabilities, its definition
  [ Report.[ Textualizable ] ]                                ; associations: Report bears Textualizable
}
```
```rust
// The target Rust of the library above.
struct Record(Text, Integer);
struct Report(Text, Vec<Integer>);
// The trait's identity: its name and its constraints, two generic parameters with their bounds.
// What ethos writes as the bounds alone, Rust writes as a named parameter carrying them;
// the parameter names are Rust's need, not the kind's.
trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
impl Textualizable for Report { /* … */ }
```
