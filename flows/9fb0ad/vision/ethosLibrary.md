# An Ethos core library

## The word-id codec goes into a library all components reuse; manifest, registry, index; ask Fable questions, then a new flow designs
Comment on «Flow ids in words, and seats launched by Flow», thread at abandonAbilityAble.
> "This should go into a library that all components can reuse, so maybe some kind of Ethos core library or Ethos standard or something. This might mean needing to develop the way ethos is put together, like manifest, registry, index: where do dependencies, libraries, etc., come from? Let's get Fable to ask me some questions about that and then with the answers he can start on a new flow and design something."

-- psyche, typed, book comment, 2026-10-03T15:56Z, relayed by 5578cc.

## The word-id library is generic over hash sizes; a kind that yields words
Comment on «Questions on the Ethos library», point 1.
> "No the word ID library that I want is not implemented specifically for Flow ID. It's generic so we can use it for any hashes of any size. We could have a few different types. There's this 33-bit type. Maybe there's a situation in which we don't even need 33 bits. Maybe there's a situation in which we need more so it's a generic type. I don't know. Let's look at the Rust mechanics here and what we can do in terms of reusability. Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?"

-- psyche, typed, book comment, 2026-10-03T16:08Z.
