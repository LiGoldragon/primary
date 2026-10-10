
> No the word ID library that I want is not implemented specifically for Flow ID. It's generic so we can use it for any hashes of any size. We could have a few different types. There's this 33-bit type. Maybe there's a situation in which we don't even need 33 bits. Maybe there's a situation in which we need more so it's a generic type. I don't know. Let's look at the Rust mechanics here and what we can do in terms of reusability. Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?

-- psyche, book comment, 2026-10-03 16:08Z; relayed9fb0ad from flows/9fb0ad/vision/ethosLibrary.md.
