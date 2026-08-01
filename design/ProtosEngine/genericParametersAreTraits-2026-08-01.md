# Generic Parameters Are Traits — 2026-08-01

Ruling from the psyche vision session, answering the manager's question
"what is T?" posed against the SimpleGeneric worked example and the
three-layer naming ruling.

Agent text answered: the manager proposed that a generic parameter is not a
concept — no encoded name, identity purely local and positional, `T` merely
a visible name.

Psyche ruling [psyche-verbatim]: "youre right; and the answer is the
mandatory trait! so T would be a trait! and multiple trait in the
declaration would just adjust the emitted rust - remember for us rust is
assembly)"

## Seated meaning

- A generic parameter IS a contract (trait) reference. There is no type
  variable in the concept layer. What Rust spells as `T` is a generated
  visible name in the assembly projection, authored by no one.
- The parameter's identity is the referenced trait's encoded name, plus
  position within the declaration when the same contract parameterizes more
  than one slot.
- Multiple traits on one parameter are a contract list; they "just adjust
  the emitted Rust" — `<T: Ord + Clone>` is assembly spelling, not authored
  structure.
- Connects to the impls-under-traits standard (traits are the spec in
  code): generics parameterize by the spec itself. Full contractual
  specificity extends into parameterization.
- Rust-is-assembly corollary [agent-inference, consistent with the ruling]:
  monomorphization vs dynamic dispatch (`<T: C>` vs `dyn C` vs `impl C`)
  becomes an emission choice made by the Nomos object, not an authored
  concern.

## Open sub-question

The unbounded parameter (Rust's plain `Vec<T>`): under full contractual
specificity, is it (a) a reference to a trivial/universal contract, or
(b) simply not authorable — every parameter must name a real contract?
Unruled; to be put to the psyche when it first bites in real material.
