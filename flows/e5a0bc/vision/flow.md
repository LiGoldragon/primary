# Flow

## The context modules are indexed in a manifest or registry, possibly in more than one place; a registry of paths in Flow's memory lets us start now, without datom expansion

Context: typed to this flow on 2026-10-07, ordering the next Fable flow onto Flow design alone.

> All of the context modules will be indexed somewhere in some kind of manifest or registry, possibly in more than one place. We can still just feed this registry piece by piece so that we don't have to worry about datom expansion support right now. We can just have a registry with paths to all of these context modules in the flow memory itself. That way we can start right now.
>
> It's a little bit dirty because it addresses relative paths, which would probably break in some circumstances. If we just feed the text in the memory, that would solve the problem. There are pros and cons to each one.

-- psyche, typed.
