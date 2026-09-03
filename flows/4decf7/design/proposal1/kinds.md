# Kinds

## Kind

Kind is the word for the bearer of capabilities: something that can
run is a runner, Runnable is its kind, and run is its capability, a
function the kind has. Trait is set aside as acoustically ambiguous.
In ethos there are no generics, only kinds. Declaring a new kind
declares a new trait in the Rust world and might imply more in the
ethos world.

```rust
// In the Rust world a kind is a trait and a capability is one of its
// functions: Runnable is the kind, run is the capability.
trait Runnable {
    fn run(&self) -> Outcome;
}
```
```
Library.{
  {0 1 0}
  []                                   ; imports
  [ Outcome.[ Done Failed ] ]          ; types
  [ Runnable.[ run.[ Outcome ] ] ]     ; kinds: the bracket after the head holds the capabilities
  []                                   ; associations
}
```

## Naming

Kinds are qualifier-named: Runnable, Textualizable, Structural,
Embodied. Run is not a kind. The verbs Rust imposes, Write and Read
among them, are tolerated as legacy, for cognitive ease while Rust
and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

```rust
// The kind says what its bearer is capable of; the capability is the verb.
trait Textualizable {
    fn textualize(&self) -> Text;
}
// Legacy: a verb Rust imposes stays as Rust spells it, until ethos is
// the authored language.
impl std::io::Write for Sink { /* … */ }
```
```
Library.{
  {0 1 0}
  [ protos:Text ]                              ; imports
  [ Sink.{ … } ]                               ; types
  [ Textualizable.[ textualize.[ Text ] ] ]    ; kinds
  [ Sink.[ Write ] ]                           ; associations: Sink bears Write, under Rust's name
}
```

## Identity

A kind is identified by its name and its constraints, the kinds its
positions require, written as one head: Processable<[Clonable
Sendable] Serializable>. What else the kind declares, its superkinds,
its associated types and constants, its capabilities, is its
definition, not its identity. Angle brackets hold the kinds standing
in a type's or a kind's positions, Vector<Ordered>,
Result<Vector<Sortable> Error>, a form chosen for token economy and
because it recycles Rust cognition; a kind declaration's position
holds a kind, never a type. The type that bears a kind is Self, as in
Rust.

```rust
// The identity parts: the name, and the generic parameters with their bounds.
trait Processable<A: Clone + Send, B: Serialize> { /* … */ }
```
```
Library.{
  {0 1 0}
  []
  [ Sorted.{ Vector<Ordered> } ]                            ; types: struct Sorted<Ordered: Ord>(Vec<Ordered>)
  [ Processable<[Clonable Sendable] Serializable>.[ … ] ]   ; kinds: the head is the identity
  []
}
```

## Declaration

The kind syntax is drawn from the anatomy of a Rust trait in its most
complex form, so that every kind can be expressed with the most
elegant syntax. A simple kind is a bracket block of capabilities; a
complex kind opens with a brace and carries fields such as its
superkinds. Ethos keeps separate blocks for types and kinds, and a
block of associations gives each type the kinds it bears. A
capability's yields are written in a bracket block, even a single
yield, and a bracket of several yields yields all of them; a
fallible yield is a Result. The head takes one separator, so its
options are mutually exclusive: `!` marks a mutable self, `:` no
self. Within a kind's capabilities, different structures may be
different types, told apart, as everywhere in ethos, by the
delimiter after the head.

```
Library.{
  {0 1 0}
  [ protos:Text ]                                             ; imports
  [ Sink.{ … } ]                                              ; types
  [ Textualizable.[ textualize.[ Text ] ]                      ; kinds: a yield is always bracketed
    Embodiable.[ embody.{ [Text] [Result<Self Error>] } ]      ;   inputs, then yields; Self bears the kind
    Fillable.[ push![ Count ]  create:[ Self ] ] ]             ;   the one separator: . self, ! mutable self, : no self
  [ Sink.[ Fillable ] ]                                       ; associations
}
```
