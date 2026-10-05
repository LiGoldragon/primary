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
