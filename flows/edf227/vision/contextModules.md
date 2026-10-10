# Context modules: skills, system prompt and prompt from one registry

## Skills are a prompt system; the same modules go in the system prompt, the prompt, or stay loadable
> "Essentially, the system that we have for skill is really just like a prompt system, so we can use these either in the system prompt or in the prompt, or just let the agent have these skills available to load. So these would be different kinds of context modules, let's say. Maybe the curriculum component is just called context. That's not a big deal."

-- psyche, STT then pasted, 2026-10-03.

## Markdown files; Flow keeps a registry of type, name, location; a launch names pairs of type and name per place; Flow inserts them; the registry is maintained over the meta socket
> "The biggest problem is figuring out how we get that data, but since it's going to be passed in a string, it's okay. It's in a string already, so they can still just be in Markdown files. Every flow call, or the flow database, has a registry of where each context module is located. That sounds pretty reasonable for a prototype, minimum viable product. We just then have the vector of structs that have the context type and, in a string, I guess, or no, that's a known set: where it is. The name also is the part that's not set, right? We have: the vision type, the flow skill; the vision type, the psyche skill; the vision type, whatever skill, the behavior. That's another field: the name of it, and the third field would be the location of where it is, either just a local file path for now. Maybe later we can support Git repos and stuff like that. We pass a list of which type and name for the context we want to load at each layer in the system prompt and in the origin startup prompt. They accept these values, and the flow nexus just inserts those values in the right places. It's just a matter of giving a bunch, like a list of what we want to load, which is just a pair of the type and the name. We need to maintain this configuration in Flow that we have to update when we add a new skill to add it to the list. That would be the meta. We can make it the meta socket."

-- psyche, STT then pasted, 2026-10-03. His order after it: a book about this, then Mind designs it and writes the code. Transcription corrected: "Mike" → Mind.

## No repetition: a vector of selections, one per kind, carrying names; names map to paths elsewhere in the database
Comment on «Flow» (standing version), at the datom example of a role's configuration.
> "Actually, we need to avoid repetition. It would be essentially a field with each of the different types of prompt modules, or it's a vector. It could be a vector with the variant, like vision, and each of the variants contains all of the names of the modules that it wants. Somewhere else in the database, those module names correspond with the path, so that's configured separately, right? Let's look at all of it. I want to see the anatomy of everything that we're designing."

-- psyche, typed, book comment, 2026-10-03T19:02Z, relayed by 6e782c.

## `kind` is taken; role is a module type too; the meta socket is reasonable for now
Comments on «Context modules», at the registry's Kind enum and at the meta Signal.
> "I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic."

-- psyche, typed, book comment, 2026-10-03T19:05Z.

> "Yeah, that looks fairly reasonable for now."

-- psyche, typed, book comment, 2026-10-03T19:06Z.

## Fable designs the context-module system with the whole stack: research first, extensive, many visuals; a standard Flow uses and Curriculum implements; keep the name Curriculum
> "I would like Fable to design the context module side of things, along with the entire stack. I want to see lots of visuals. I want this to be extensive. I want him to do some research first and present me a very extensive design for this system that can both populate the skills and the system prompt. It's a standard for now that Flow can use and that we'll also implement in curriculum, which we could possibly rename context or maybe keep it curriculum (because the word context is used a lot so I think it's better to keep it curriculum)."

-- psyche, typed in chat to Psyche Opus 5578cc, 2026-10-03, relayed by 5578cc.
