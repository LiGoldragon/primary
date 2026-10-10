# Forge

## 2026-09-14 — A proof-of-concept Forge on the new stack, reviewed through its anatomy; persona first; standard objects that map to Nix; the native sandbox side named apart

Context: comment on the forge row of the audit page. "CreoleOS" is speech-to-text for CriomOS per the same day's spelling ruling; left as written.

> Something really interesting that we could do with getting a proof-of-concept, minimal product Forge component with all of the new stack, maybe even rewritten and redesigned, and through the anatomy, like this different approach now, where you and I can review its anatomy.
>
> Let's do all of the main components that are in production now and our most important candidates, which are persona, to get all of this started: managing it and sandboxing it, which will allow us to do well. Persona will involve components that take care of sandboxing and things.
>
> This sort of ties naturally into Forge, where, at the very least, now we could create a bunch of standard objects that map to Nix things, like a Nix package derivation or a way to get their Nix package derivation with different types, with overrides, or NixOS build on Nix packages with such-and-such options. We could even spec out all of the options that are in the NixOS build in Nix to an actually specified, maybe even better-presented corpus of specification for this NixOS build. Then we could just write a lot of our Nix code as templates ported into these standard Nix APIs with JSON inputs, so then we can maximize caching by structuring the flakes well enough anyway.
>
> This would all be Forge, and the sandbox part would be the more native CreoleOS Forge functionality. We'll have them named differently, right? The Nix-based and the native, or maybe we have a better term for this. It would involve one of our components, which takes care of containerization, which is what Nix does: it creates a container. Forge, in order to do what Nix does, would need this component. Forge doesn't have to do everything, right? It's just that that's the language that understands how to build things and manage builds, right? We'll have management between builds once we get criome awareness, network awareness of other nodes of the cluster, and even other clusters that can offer build jobs later on. That's farther off on the back burner.

-- psyche, typed, artifact comment.
