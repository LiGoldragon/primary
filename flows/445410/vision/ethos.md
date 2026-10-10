## The special representation

Context: relayed by Psyche Fable ebbe30, from the living's comment on «The golden ethos». The words in between, which order a Fable on Ethos, are left out.

> ... the special representation is basically an implementation for a special way to decode and encode, so that the representation has a different type than the type when it's read into the Rust runtime. What would that look like? It would be a trait, a special representation, like a custom Datom conversion, basically. We need to be short, but we need to also describe what the trait is. It's a custom Datom, I guess, custom Datom, meaning a custom representation, encoding and decoding, and that needs to be implemented. In Ethos, we're going to describe the real type, the real Rust type that it has, and then the special representation is going to implement the representation type. We could maybe even somehow describe that type in Ethos, what that representation type is, which would be interesting because then we would force the input and output types, and we would let Rust do the implementation.

-- psyche, STT, 2026-10-09, relayed by ebbe30.

## Invariants the code enforces

Context: the same comment.

> There are some invariants that we want to enforce in the code.

-- psyche, STT, 2026-10-09, relayed by ebbe30.
