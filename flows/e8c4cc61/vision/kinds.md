# Kinds

## A kind declaration's position holds a kind, not a type

Context: the flow wrote the declaration
`Prospective<Ethos>.[ prospect.[ Result<Ethos Fault> ] ]`.

> that doesnt work.  The kind declaration must use a kind, not a type. do we need a Type kind? or is there something equivalent which already exists in practice?

-- psyche, typed.

## The position of Prospective is bounded by Embodiable

Context: the flow proposed `Prospective<Embodied>` as the declaration,
with Embodied as a marker kind borne by Protos, Datom, Ethos.

> you mean Embodiable

-- psyche, typed.

## Embodiable keeps the embody capability

Context: the flow had proposed Embodiable as a marker kind with no
capability.

> and Embodiable still has the embody capability, to turn it into an embodied value (what is the terminology in rust for this? an in-memory value?)

-- psyche, typed.

## Prospective<Sized> is the declaration; TryInto is not a kind

Context: the flow had laid out TryFrom/TryInto, FromStr, serde,
syn, and bytecheck as neighbours of Prospective, recommending our own
kind bounded by Sized, Rust's implicit universal bound.

> TryInto just doesnt sound like a kind. lets go with Prospective<Sized>

-- psyche, typed.

## `:` for no self stands

> ok, `:` for no self stands

-- psyche, typed.
