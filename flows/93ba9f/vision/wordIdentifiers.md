# Words instead of hashes

Context: same message.

> Let's bring it up on the design book also: the standard that we want to use to replace hashes with words, with a series of words, maybe two or three words, depending on how much entropy we need for these short ID things. They would become a PascalCase series of words instead of hashes, which would actually be lighter on LLMs. You can do research on that but I'm pretty sure it would be lighter than these alphanumeric hashes. We could start turning a lot of our hashes into actual word series like that.
>
> Let's come up with a name for this if somebody hasn't and start using them in different places, like Flow ID. There's a converter that can use this in field and all our tools would support it, so that it has an implementation for how to turn this name ID, this word ID, or this phrase ID basically into the hash. That will give us the link that we need, like the Codex transcript. We know which part of the hash we're using that's random, right?

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

Context: after 93ba9f dispatched research on word identifiers (BIP39, PGP word list and others).

> Yeah I think BIP-39 was the one we found to be most efficient but it would be cool to dig to see if somebody did some research on something like this for LLMs. If somebody tried to push the density by adding the maximum number of words and also even aiming to avoid homophones

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.
