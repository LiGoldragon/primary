# Identifiers

## The word-based system is genius; BIP-39, or a newer list with more bit density that already exists; it need not be standard

Context: typed to the primary Claude 05c604 after Codex's measured table of word lists. The middle sentence is a question, answered in the reply. Logged directly by the main flow before acting.

> This is genius when we use this word-based system, BIP39. Is there a newer one that has more bit density? We can use that. We don't have to be standard. We can just use something that already exists, that maybe has a few users and has more density right from the get-go.

-- psyche, typed.

## Word ids are easier to represent and remember for humans and machines; an id gets its own separator so it is seen as an id at a glance; camel case for ids against Pascal case for typed objects, if the LLM tokenizes it efficiently

Context: typed to the primary Claude 05c604 right after the density answer. The questions on separator token cost are working instructions, answered by measurement (item 27 to Codex). Logged directly by the main flow before acting.

> The genius here is that this becomes easier to represent and remember for both humans and machines. How do we represent that for spaces? What is the token cost if we make camel case or Pascal case versus hyphen versus underscore-separated versus any other separator, like / for paths, like a colon? If you have a type which is going to be an identifier or a hash in Datom, in the ethos that defines it, it's going to know how to parse it. You can still use the colon or the period, but for us to visually identify it even better as, "Oh, this is an ID," just by seeing it, I think we should use its own separator between the words.
>
> How would that cost? Let's look at the LLM cost of that. What about just camel case? That would work too, or Pascal case, whatever works better. If your typed objects are whatever is Pascal case, I think it is the first capital, right? That would be how we write our symbols for our objects. They're all capitalized, and then camel case could be easily recognized as probably a hash or an idea of some sort. That could be a good idea. You get the visual differentiation, and that's how it's written. If the LLM can tokenize that efficiently, then it's golden.

-- psyche, typed.
