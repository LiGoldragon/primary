# Flow

## The context modules are indexed in a manifest or registry, possibly in more than one place; a registry of paths in Flow's memory lets us start now, without datom expansion

Context: typed to this flow on 2026-10-07, ordering the next Fable flow onto Flow design alone.

> All of the context modules will be indexed somewhere in some kind of manifest or registry, possibly in more than one place. We can still just feed this registry piece by piece so that we don't have to worry about datom expansion support right now. We can just have a registry with paths to all of these context modules in the flow memory itself. That way we can start right now.
>
> It's a little bit dirty because it addresses relative paths, which would probably break in some circumstances. If we just feed the text in the memory, that would solve the problem. There are pros and cons to each one.

-- psyche, typed.

## A context module is inserted in the system prompt or in the first prompt

Context: same message.

> The context modules need to be able to be inserted either in the system prompt or in the first prompt.

-- psyche, typed.

## The lock: needed to roll a metaflow over into a new flow; later Message uses it to know whether a message can reach a flow

Context: same message.

> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

-- psyche, typed.
