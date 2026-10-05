
> Well that obviously won't do. We need way more configuration for the system prompt so that we'll have modules and then there are going to be different types. There could even be an overlap between what we call skills now and what these modules are that can go in the system prompt.
>
> The one thing I would really like to know is if it's possible that there's a part of the system prompt that doesn't get passed down to the subagents of that harness. I would like to be able to program the main flow a certain way but not its subagents in its system prompt.
>
> We need to break that down into modules. We can't just make this one thing. That's absurd. The system prompt is huge. It has several, many, many different parts that have many different subparts. We need to draw up the anatomy of this in ethos by studying all kinds of system prompts and splitting them up into:
> - what this is
> - is this behavior?
> - is this personality?
> - is this operational safety?
> - what each line even falls under in terms of what kind of training/guidance it is a part of

-- psyche, book comment, 2026-10-03 16:20Z; relayed9fb0ad from flows/9fb0ad/vision/systemPrompt.md.

> Essentially, the system that we have for skill is really just like a prompt system, so we can use these either in the system prompt or in the prompt, or just let the agent have these skills available to load. So these would be different kinds of context modules. ... Every flow call, or the flow database, has a registry of where each context module is located. ... the vector of structs that have the context type ... the name of it, and the third field would be the location of where it is, either just a local file path for now. ... We pass a list of which type and name for the context we want to load at each layer in the system prompt and in the origin startup prompt. They accept these values, and the flow nexus just inserts those values in the right places. ... We need to maintain this configuration in Flow that we have to update when we add a new skill to add it to the list. That would be the meta. We can make it the meta socket.

-- psyche, STT, 2026-10-03 approximately19:05Z; relayedPsycheFableedf227, ellipses retained as supplied. Order: book, then Mind design and code.
