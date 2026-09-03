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
; The same kind in ethos: the capability and its yield.
Runnable.[ run.[ Outcome ] ]
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
Textualizable.[ textualize.[ Text ] ]
Sink.[ Write ]                          ; the association keeps Rust's name
```

## Identity

A kind is identified by its name and its positions, as a Rust trait
is identified by its name and its generic parameters:
Convert<Integer> and Convert<Boolean> are two kinds, and one type may
bear both.
What a position requires, the superkinds, the associated types and
constants, and the capabilities are the kind's definition, not its
identity. The declaration head writes the name with its positions
and what each requires: Processable<[Clonable Sendable]
Serializable>. Angle brackets hold the kinds standing in a type's or
a kind's positions, Vector<Ordered>, Result<Vector<Sortable> Error>,
a form chosen for token economy and because it recycles Rust
cognition; a kind declaration's position holds a kind, never a type.
The type that bears a kind is Self, as in Rust.

```rust
// Identity is the name and the generic parameters, nothing else.
trait Convert<Target: Clone> {      // Target is a position; `: Clone` is what it requires
    fn convert(&self) -> Result<Target, Error>;   // a capability: definition, not identity
}
impl Convert<Integer> for Text { /* … */ }   // one trait
impl Convert<Boolean> for Text { /* … */ }   // another trait, same name
```
```
; The same in ethos: the position holds a kind; the capability yields it.
Convert<Clonable>.[ convert.[ Result<Clonable Error> ] ]
Text.[ Convert<Integer>  Convert<Boolean> ]      ; two kinds, one bearer
; The declaration head: the name, then each position with what it requires.
Processable<[Clonable Sendable] Serializable>
; Positions hold kinds.
Sorted.{ Vector<Ordered> }        ; struct Sorted<Ordered: Ord>(Vec<Ordered>)
Result<Vector<Sortable> Error>
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
; A simple kind: a bracket block of capabilities; a yield is always bracketed.
Textualizable.[ textualize.[ Text ] ]
; Inputs, then yields; Self is the type that bears the kind.
Embodiable.[ embody.{ [Text] [Result<Self Error>] } ]
; The one separator: `.` self, `!` mutable self, `:` no self.
Sink.[ push![ Count ]  create:[ Self ] ]
```
