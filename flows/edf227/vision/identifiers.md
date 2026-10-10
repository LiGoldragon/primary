# Flow ids

## FlowId is a hash, not an integer; a word-to-hash ambiguity in the last character is acceptable; a collision is brought to the psyche; the minimum product first, the word id may come in a later version
Comment on «The anatomy», at FlowId.Integer.
> "First of all it's not an integer, it's a hash, right? To be precise I don't know how we want to approach that but the other problem is this: because the 33-bit might not correspond with the alphanumeric cutoff of characters, when converting from words to alphanumeric to find a transcript, we might end up with a bunch of possibilities for the last character. I'm guessing that's possible, maybe something to consider. I don't care. If 33 bits, for me, I think it is enough entropy. If there is a clash then the model can easily figure out, "Okay here are two matches," and that would be worth bringing up to the psyche: "Oh we've had a collision," and then see what we do. But other than that it's not a big deal. I would like to get the minimum [viable] product up first so if we let go of the word ID for now and then do that in a later version, that's okay."

-- psyche, typed, book comment, 2026-10-03T19:26Z. Transcription corrected: "YBro" → "viable".

## The flow id is a hash; its text forms are serialization, outside the Nexus; the Nexus thinks of it as a hash with traits
> "The flow ID is not a string, it's a hash. Why do you say integer and then string, or do you mean that an integer is a hash? I guess we need traits that allow us to switch back and forth, or I would like this to be a serialization and deserialization thing so that it's not actually in the Nexus. The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits. In the deserialization, we can have special implementations, maybe, so that a certain kind of thing is deserialized with a certain kind of algorithm that creates an alphanumeric hash from a string, from a hash which is an integer or whatever. Find out how this works and how we could do it."

-- psyche, STT, 2026-10-03.
