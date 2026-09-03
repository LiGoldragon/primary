# Kinds

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

A kind is identified, as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. Angle brackets hold the kinds standing in a type's or
a kind's positions, Vector<Ordered>, Result<Vector<Sortable> Error>,
a form chosen for token economy and because it recycles Rust
cognition; a kind declaration's position holds a kind, never a type.
The type that bears a kind is Self, as in Rust.

## Declaration

The kind syntax is drawn from the anatomy of a Rust trait in its most
complex form, so that every kind can be expressed with the most
elegant syntax. A simple kind is a bracket block of capabilities; a
complex kind opens with a brace and carries fields such as its
superkinds. Ethos keeps separate blocks for types and kinds. A
capability's yields are written in a bracket block, even a single
yield. The head takes one separator, so its options are mutually
exclusive: `!` marks a mutable self, `:` no self. Within a kind's
capabilities, different structures may be different types, told
apart, as everywhere in ethos, by the delimiter after the head.
