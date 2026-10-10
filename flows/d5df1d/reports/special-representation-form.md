# The ethos form of a type with a special representation (design's own, for 445410's book)

A type with a special representation is declared like any type in the types section, and bound to its Representation in the associations section, where a trait's associated types are declared with the same period that declares a type anywhere.

```
Library
[ datom:[ Represented ] ]
[ Ticket.Integer Digit.Integer ]
[]
[ Ticket.[ Represented.{ Representation.Vector<Digit> } ] ]
```

Read: Ticket is a new type over Integer; it is associated with Represented, whose associated type Representation is declared as Vector<Digit>. The design's Digest: a declared storage type in the types section and `Digest.[ Represented.{ Representation.String } ]` in associations.

Expected Rust, on the items 1-2 set: the type as the set emits it, `pub struct Ticket(pub i64);`, with `#[derive(Represented)]` in place of the two datom derives, since Represented supplies Datomizable and Composing (the derive gate treats Represented as satisfying both); the association emits what associations emit today, a compile-time assertion, here pinning the associated type: a fn bound `T: Represented<Representation = Vec<Digit>>` instantiated on Ticket, so a hand-written impl with another Representation fails to compile. The impl itself, represent and from_representation, is hand-written in the sibling module (traits explicit, bodies hand-written); the generator emits no partial impl and no skeleton. The source name is emitted as the author wrote it, consistently in the derive and the assertion: `datom::Represented` in both when the import says `datom`.

Why it collides with nothing: a period followed by a brace after a name conception knows as a trait binds that trait's associated types; after a name it knows as a type it is a struct declaration, as today; the associations section holds only type-to-trait pairs, so the two never meet. No colon, so no segment reads as a source; written in place the import is `datom:Represented`. The variant-carries-type rule reads a bracket in the types section; the associations bracket is a list of traits and is never read as variants. No angle brackets after Represented, so the rule that a constraint is a trait, never a type, is untouched.

The generator's internal names are Binding, for an associated type bound in an association (Representation = Vec<Digit>, Rust's own term), and AssociatedTrait, for one entry of a type's associations section; AssociatedType remains the declaration side inside a trait.

Fork 3: a represented type's text is its Representation's text under both answers (witnessed in flows/1d0733/reports/representation-fork3.md); the answer changes only the Representation's own text when it is itself a new type.

Tests to pin: the form accepted in the association; `Represented.{ }` on a name that is not a trait refused with Expected.Trait; a hand-written impl naming another Representation fails the generated assertion (E0271); a Representation outside the trait's bounds fails at the impl itself (E0277), rustc enforcing the bounds there; the two datom derives absent when Represented is present; Ticket round-tripping as Vec<Digit> text under bare and braced.

Status: the design's own; lands nothing; goes to the living through 445410's «The special representation». Witnessed on Prometheus under the bare answer (cargo test and flake checks green, eight new tests, Ticket(42) printing [ 4 2 ]) per flows/1d0733/reports/ethos-represented.md; witnessed under both answers to Fork 3 on complete trees on 07714b (flows/1d0733/reports/fork3-complete.md); a known gap: a trait written in a field position is emitted as a type, listed, not built.
