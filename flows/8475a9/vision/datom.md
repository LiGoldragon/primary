# Datom

## Expanding: a special syntax that replaces an object with the datom payload in a file; a repo keeps a datom file indexing itself, so a deploy manifest is never recomposed by the model

Context: spoken to this flow, opening the design of datom expansion.

> One of the things I want to talk about is the concept of expanding. I would like Datom to be able to insert another Datom payload inside a certain file, like `replace`. It would be a special syntax, maybe a particular symbol just for that, since it's going to be quite unique. Let's review how we can make that system in an ideal architecture. What should it look like, with as many layers of correctness as correctness would allow or would warrant?
>
> I know that we've talked a lot about the ethos architecture but maybe Datom needs to also get a little bit of attention in how it actually works. That would allow us to have these sort of manifests. For deploying a skill curriculum, it would be kind of absurd to ask for the model to compose the entire registry of a certain skill repo every time the deploy happens. That repo could essentially just maintain a Datom file that indexes and specifies the entire repo.
>
> Wherever that payload is supposed to be, the agent could just use that special syntax. That means that this file, which would be a path, ought to be used to replace this object with the data in that file. Basically it's just a simple replace.
>
> We could also talk about what happens if we go the other way and we want to get a certain response with all of these values. I don't know if it's that useful but at least for the input that would be really useful.

-- psyche, STT, 2026-10-05.

## No Curriculum repo in the deploy; the skill repositories themselves are invoked

Context: his comment on «Datom expansion», the syntax example invoking curriculum-deploy with the Curriculum repository. Relayed by 8f0f57.

> Well with the new vision we wouldn't involve this curriculum repo. We would just directly invoke the particular repositories like mind, psyche, and field.

-- psyche, STT, book comment, 2026-10-05.

## No datom in any Nexus; string handling in a Nexus is forbidden

Context: his comment on the drawing's box «Nexus: no Expander, so @ is Forbidden». Relayed by 8f0f57.

> Well the Nexus has no datom so expand [it]. It doesn't even have datom. There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus.

-- psyche, STT, book comment, 2026-10-05.

## A reference path is not a string: no guillemets

Context: his comment on layer 1, "a bare string that begins with @ is written in guillemets". Relayed by 8f0f57.

> No it wouldn't use [guillemets] because that would make it a string, which it's not. It's a path. It's an expanding path or whatever the right term is here. Yeah it's a reference path so it's not a string so it's not going to have the string delimiter.

-- psyche, STT, book comment, 2026-10-05.

## Expansion is a step before the structure step, like the ethos rearranging step

Context: his comment on layer 2, "expansion happens at compose". Relayed by 8f0f57.

> So compose would be a step before the protos structure step, like finding the structure. There would be a step before that, kind of like how we have a step, or we should have a step in ethos to rearrange an ethos file so that it's a variant with a struct.

-- psyche, STT, book comment, 2026-10-05.

## Everything in Rust is a trait; a wrong trait design is a wrong anatomy

Context: his comment on the Rust block, whose compose was an inherent method. Relayed by 8f0f57.

> The trait is missing here. Everything should be done with a trait, right? Don't we have that rule? How we code in Rust: everything is a trait. Everything must fall under a trait. If the trait design is wrong then there's something wrong with the anatomy of the design of the system.

-- psyche, STT, book comment, 2026-10-05.
