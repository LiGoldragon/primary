# Flow ids

## FlowId is a hash, not an integer; a word-to-hash ambiguity in the last character is acceptable; a collision is brought to the psyche; the minimum product first, the word id may come in a later version
Comment on «The anatomy», at FlowId.Integer.
> "First of all it's not an integer, it's a hash, right? To be precise I don't know how we want to approach that but the other problem is this: because the 33-bit might not correspond with the alphanumeric cutoff of characters, when converting from words to alphanumeric to find a transcript, we might end up with a bunch of possibilities for the last character. I'm guessing that's possible, maybe something to consider. I don't care. If 33 bits, for me, I think it is enough entropy. If there is a clash then the model can easily figure out, "Okay here are two matches," and that would be worth bringing up to the psyche: "Oh we've had a collision," and then see what we do. But other than that it's not a big deal. I would like to get the minimum [viable] product up first so if we let go of the word ID for now and then do that in a later version, that's okay."

-- psyche, typed, book comment, 2026-10-03T19:26Z. Transcription corrected: "YBro" → "viable".
