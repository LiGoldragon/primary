# Single-field structs

## 2026-09-08 — Those should be new types

> Also, there's another recent flow which you might want to look into, where we talked about single-field structs, which are an aberration and which we need to sort of train against, or possibly even refuse. I think we should possibly even refuse single-field struct types and ethos, and instruct against them even in Rust, because those should be new types.

-- psyche, typed.

## 2026-09-08 — This should be a new type

Context: Responding to the description of `X.{ T }` as an Ethos one-position product, and its generated Rust tuple struct.

> Which, as I was talking in the other flow, is something that I want to make illegal now because it's absurd. This should be a new type and not a struct with just a single element in it.
>
> Then the implementation is wrong because a new type should be just the name of the type and then the separator, which is a period, and then the name of the contained type. If it's an inline type declaration, then it's just that: a type declaration. Never mind that. That's what it is. It would be absurd to make a new type that contains another complex type. A new type generally is like `name.string`, `age.integer`, or whatever we use: `int`.

-- psyche, typed.
