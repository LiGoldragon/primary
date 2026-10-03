
## Words for addressing

> The whole point of using words is to make it more comfortable for LLMs so yes, it is to address a certain flow instead of using the more LLM-expensive hashes. It seems I'm having trouble making it clear to you that what really drives everything is the reason why we did something in the first place, the rationale behind something, and the goal is the overarching principle that guides everything in terms of implementation. If the whole point of using words is because it's cheaper for LLMs and for humans, then the whole point is for LLMs and humans to use it. Isn't that obvious?

-- psyche, book comment, 2026-10-03 15:07Z; relayed by 9fb0ad from flows/9fb0ad/vision/identifiers.md.

> This looks perfect. That's exactly the user interface I was looking for.

-- psyche, book comment, 2026-10-03 15:54Z; on shape abandonAbilityAble, «Flow ids in words, and seats launched by Flow»; relayed9fb0ad, flows/9fb0ad/vision/identifiers.md.

> There are two registries:
> - The true registry with the actual IDs
> - Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice, the current flow for that voice
> 
> The syntax would be `psyche.primary` because it only has one. It's like a single-field data-carrying variant, right? We don't need the struct braces. It's kind of like a data-carrying variant that holds a variant essentially.

-- psyche, book comment, 2026-10-03 15:58Z; relayed9fb0ad from flows/9fb0ad/vision/identifiers.md.

> Well it seems to me that the first 33 bits of the actual ID we were using from the harness's ID is what we're using and then converting it into words because then we can go back. Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words. Is there anything that doesn't work with that in practice?

-- psyche, book comment, 2026-10-03 15:59Z; relayed9fb0ad from flows/9fb0ad/vision/identifiers.md.

> I don't think what you're saying is a misinterpretation of what I said in September. It was my vision all along that the words could be converted and give us the flow ID in return so that there's a correspondence between them.

-- psyche, book comment, 2026-10-03 16:05Z; relayed9fb0ad from flows/9fb0ad/vision/identifiers.md.
