# Nexus

## 2026-09-13 — A nexus that can create these attachments; no Python

Context: the living saw the reverse relay arrive through the pty injector written in Python by flow 024bc7 and asked why the nexus was not used.

> So, you didn't use the nexus, or maybe it was an ancestor to a nexus concept, because maybe the asynchronicity of the actor and the way it was written, I guess, made it impossible. There should be a way to have a nexus where it can create these attachments. Maybe, or should we just use Herder, because that was glitchy? I don't want to use Python.

-- psyche, STT.

## 2026-09-14 — Nexus the only main call, then Nexus loads up the signal; Forge doing everything cargo used to do

Context: comment on the gap "the nexus library is not the base of the nexuses". Asks to be shown what this could look like.

> Yeah, this is what I was saying in the other comment: we need to make Nexus sort of the only main call, and then Nexus loads up the signal. You can show me what you think this could look like, potentially. There's the whole cargo build system and all this to take into account: how each library is dispatched and how we want to make this deterministic and smart, so that we can reuse cargo but also create a system that is maybe more future-proof, oriented towards Forge essentially doing everything that cargo used to do more efficiently because it's more integrated, with source caching and everything.

-- psyche, typed, artifact comment.

## 2026-09-14 — Nexus, core, and metaNexus are the explicit terms; the core library guards that the signal actor never talks to the sema actor

Context: comment on the gap "almost nothing runs". "Sima" is speech-to-text for Sema; corrected in the quote. "demon" left as written.

> Yeah all these things have to be re-anatomized. Also I was thinking the Nexus core library could be how the signal actor, the Nexus actor, and the Sema actor (the main actors in a metaNexus, as we could call it, or the whole of what people call a demon) could be. If we want to be explicit we can say metaNexus and core Nexus but if we say Nexus we sort of have to let the context imply which one we are talking about. If the context isn't obvious then the speaker is blamed for not being clear enough: which part he means by Nexus.
>
> Nexus, core, and metaNexus are the explicit terms. The Nexus core library has all of the interfaces and kinds defined for how to build metaNexus and it has the machinery to make sure, ideally at compile time, that there is no signal-actor-to-sema-actor communication possible. All interaction between the signal actor has to go through the Nexus and then the Nexus ethos type file.
>
> We have this Nexus type, the sema type, and the signal type and they each have their own intrinsic kinds applied to the types so that they're of that specific actor. Only this kind of actor can react with this type of object. It's like a kind becomes a higher-type kind compiler check: an architecture guard basically.

-- psyche, typed, artifact comment.
