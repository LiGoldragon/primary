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

## Our own terminology over Sized: everything has an embodiment

Context: `Prospective<Sized>` had been ruled; the psyche reopens the
word.

> First let's step back even further. I think I would rather use our own terminology over sized. We have the sized kind and I don't know, it just doesn't flow very well in a sentence so I'd rather say an embodied object. I think it just sounds better. Any of our embodied, oh wait, that doesn't work either.
>
> Actually what I'm trying to say is any object that we have, like any concept basically in Protos, has an embodied conceptualization. A kind, you could say, has a type that holds the definition of that kind, if you follow me. Obviously that's not this is a rust value in practice.
>
> When I say embodied I guess I mean it has a rust value. A kind has an embodiment, a type has an embodiment, a datom [STT: datum] value has an embodiment in the sense that it fits into a certain kind of type. A kind declaration in ethos is going to translate into an embodied value in rust that's going to hold all of its different values, like its name etc., and it also has a default structure. This would be, I guess, or maybe it has an anatomy or a protosic [STT: protossic] representation, basically. It has a representation in Protos, like a text representation, and by default it's going to have its own way of being represented.

-- psyche, STT.

## Situation and Embodied stand

Context: the flow proposed Situation for the overloaded "context" and
Embodied as the universal kind in place of Sized.

> yes on situation. yes on Embodied

-- psyche, typed.

## Structural's capability returns the protos structure, recursively; Prospective stays

> I dont think the Structural capabilities include prospect. it would be a capability that returns its protos structure and all the recursive structures it contains (replacement for portions)
>
> nothing is replacing Prospective, especially since it's quite universal (maybe even universal beyond protos; a more aptly named TryInto<Sized> basically)

-- psyche, typed.

## No Embodiable; Embodied is an alias of Sized

> I dont think there is any Embodiable. It's just Embodied, which is an alias of Sized. Would that work? Or would it make everything more complicated than just using Sized?

-- psyche, typed.
