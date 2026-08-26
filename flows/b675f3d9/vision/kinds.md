# Kinds

## Qualifier form; Kind is the word; a kind is a trait; no generics in Ethos

2026-08-26, the psyche, typed (answering the surfaced tension "infinitive vs qualifier trait names"):

> 1. qualifier. Write isnt a kind. we say kind now, not trait. declare a new kind = declare a new trait, in Ethos world, which will imply some things which arent in rust world (tbd). so in Ethos there are no generics, only kinds.

## Capability is a function a kind has

2026-08-26, the psyche, typed (answering the surfaced tension "'trait' disliked, no replacement sealed"):

> 4. capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)

## The kind syntax proposal is inappropriate; start from the anatomy of a Rust trait

2026-08-26, the psyche, dictated, on the four-section kinds/capabilities proposal f426777b had shown:

> Your kind syntax proposal is very... is completely inappropriate. So start by looking at a rust trait, which is what our kind essentially becomes, and in its most complex form, and doing the anatomy of a rust trait. And then you'll see how many different kinds, how many different types of things are in a trait. Which means you're almost, I'm like, I can guarantee you that you're going to need a struct to fit it all in. Or maybe even a root enum to differentiate between different kinds of kinds or different types of kinds or maybe an enum in the struct or like we'll look at different possibilities for essentially to maximize elegance, the elegance of the syntax and yet achieve the level of expression required to express any different kinds that we might want to express.
