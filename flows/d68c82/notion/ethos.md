# Ethos

## Referring to Rust types from ethos; a byte array shown in ethos

Context: comment on «The Source nexus», at the hash written as four Integers.

> I guess what you're saying is you're going to use 4 64-bit integers but Blake3 is already a type somewhere. This is interesting. We need a way to essentially refer to Rust types from Ethos, which I guess we already do. Maybe it's just a special import syntax: a special way to write syntax, which means this comes from Rust.
>
> Also if you felt compelled to use 4 integers instead of an array of bytes, then does that mean you thought the Ethos syntax didn't allow you to represent this as an array of bytes? Maybe we represent it in Ethos and then it also just corresponds to the Rust type so that we can see that's an array of bytes in Ethos. That sounds complicated and since we're trying to get started on all of the infrastructure, I wouldn't push too hard on that but it's worth just writing in [notion] I guess.

-- psyche, STT. Transcription corrected: "Notion" → "notion".

## New delimiters: vectors, and comments that can become code
"I want to consider possibly a notion of using a new delimiter that hasn't been used. Here are two separate notions, which involve using delimiters that haven't been used:
1. To define vectors without using the word "vector" since they're so common in ethos.
2. This would be more involved structurally but it's actually quite simple. Conceptually it's a delimiter for comments so that eventually comments can be used like code. The code extraction process would just sort of ignore them like comments for now. Later on they could be used to get a prose description, if you will, or help, some kind of documentation on the object that either probably precedes it or follows it. I'm guessing that it would be after the object that it describes.
But for now I'm more interested in the vector aspect so I would focus on that in terms of implementing any one of them first."
-- psyche, STT, 2026-10-12.
