# Identifiers

## Identifiers are real types, not strings: an ethos library of identifier types on datom's own hashing types, a UTF-8 base legal in datom, bit-typed ids

Context: answer to the orchestrate Signal sketch, where FlowId and ClusterId were typed String. The opening sentences of the same message ruled the main-flow wording good and the word "Flow", not "seat"; those are recorded in log.md and vocabulary is the living's ruling. Logged directly by the main flow.

> Why are we saying that the ID is a string? It seems to me that we could maybe create an ethos library for this, but those are real types, like a SHA-256. Yes, in a way, it's a string when you print it, but it's not a string per se.
>
> Your flow ID is, let's say, what? Maybe we don't need to go hexadecimal. We can expand our bit range, our bit efficiency. Whatever is legal in datom is what we should use for our hashing base: a UTF-8 base for hashes. We should probably type them like, "This ID is a 36-bit identifier," or whatever we want to say that.
>
> We have our own protocol for all these identifiers, which uses datom's own standard hashing types that are in the library that we use to create these complex ID types.

-- psyche, typed.

## A readable alphabet, perhaps words, since the only cost is the token cost; security levels by how bad a collision is; what a legal symbol is, defined in Signal

Context: answer to the primary's alphabet, width, short-form and home questions. Logged directly by the main flow.

> The alphabet would be something that can be read. I was even thinking about how LLMs quantize or tokenize. If they tokenize as efficiently, because this is what I think is going on (for each character having essentially the same size as a small word when it's in a hash), then we might as well use words. The only cost we're worried about is the LLM token cost.
>
> Maybe we have a legible one because it's funny: the world is sort of leaning towards that too because they're more readable. They're more easily communicable in a speech-to-text context, and even cognitive. We think better in terms of words.
>
> How many bits do we need for safety in our context? We need to define different contexts properly, like three different levels of security in terms of how bad a collision is or how much control we have over it, because it's limited in nature. Local and private, then it's totally different. If it's a public namespace or something, then it's totally different.
>
> We should have both alpha-numeric, like readable, still readable, but alpha-numerics, sort of with symbols perhaps in, because these can still be said if they're commonly known. Obviously, colons and stuff like delimiters, dots and stuff are not going to be allowed, just like the bare string, basically. We should probably clarify what the bare string is. What would be a legal symbol, or I don't know, what do we mean by that? An ethos object identifier, right? What we can use as an identifier for an object. What is legal there as a symbol, basically, or what I call a symbol in ethos, something that symbolizes an object, like a data variant or whatever. That would probably live in ethos core or ethos standard, or I guess Signal could have it because we're going to think in terms of Signal. Essentially, sema is storing Signal, so it's all Signal. The data itself, we're going to refer to it as Signal when it's binary and it's typed. Signal is a good place to put that.

-- psyche, typed.
