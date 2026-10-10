# Naming

## Registry names are independent of repository names; uncapitalized camelCase names made of words

Context: «Sources and the registry», proposal 3, "What the key reaches", 15:25.

> Well the name of the repo and the name in the registry, in our own memory, our own Nexus memory, doesn't have to be the same. Even I would say it seems we've gone with a hyphenated kebab case (I think it's called) for repo names, which maybe is more canonical or standard, and it's fine. I don't have any problem with it.
>
> In Protos languages like datom and [Ethos] for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants. If there's a string position in datom and it starts with a capital, that's okay because we have a different type that's kind of like a string but it has to be checked whenever we create a new one. This is the Prototypic name or whatever, the prototype name, which is an uncapitalized identifier. It's going to have to be composed of words so we need to put together some kind of fancy check. Well not that fancy, I guess.
>
> That would need a dedicated Nexus because it would need to have a database of words. If we're going to do the word-based identifiers, I'd like to get a book on the runtime size cost of having these things in a certain runtime and how it might be smarter to create a dedicated Nexus for that functionality. We could still just build it into whatever we're compiling into, whatever we're doing for now.

-- psyche, typed. Transcription corrected: "Esos" → "Ethos".
