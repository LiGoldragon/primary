# Ethos

## Voice is a struct of aspect and layer; structs over chained variants

Context: his comment on the book «The Nexus», on the code block "The anatomy in code" (Voice.[ Psyche.Layer …).

> There are two things that are not really related but kind of meet:
> 1. There's a missing variant called `field`.
> 2. Now I'm seeing a syntax or a pattern in Ethos that I would like to develop because it allows for a certain cool-looking datom syntax: a series of variants one after another. There possibly could be many of those although I think the most common use is for two variants in a row, because after that you might as well use a struct. One could argue that one could use a struct from the beginning and I think that might be simpler.
>
> I think we're going to abandon this idea that we wouldn't have an enum where each data-carrying variant carries the same type, because it creates this repetition that you can see now: `[psyche].layer`, `[mind].layer`, `.layer` is being repeated. I think rather the voice is a struct that contains the aspect and the layer, and the flow has a role, one of which is a voice. We can start leaning more on [structs] than on chaining up [variants], which ends up in an ugly Ethos pattern.

-- psyche, STT. Transcription corrected: "seq" → "psyche"; "mine" → "mind"; "strokes" → "structs"; "variance" → "variants".
