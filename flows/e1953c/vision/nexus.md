# Nexus

## Nexus objects describe the processes; "process" is implied by being a Nexus object, usable only with a Nexus meta-actor; the flow is the actor inside the runtime

Context: follows the Mesh answer in the same message.

> We can break processes into sub-processes, right? In the Nexus objects, you're going to describe all the processes. I don't think you need to say "process" all the time, but it's kind of included or implied by being a Nexus object, which means it can only be used with a Nexus meta-actor, meta-process, or meta-flow, basically. It's like the same concept as the flow is the actor inside the runtime.

-- psyche, STT.

## The metaNexus is the whole daemon; the Nexus, Sema, and Signal meta-actors each hold sub-actors that must run inside them; the trait enforces it at the compiler

Context: correction of this flow's reading of the previous entry. "SEMA" is speech-to-text for Sema, corrected in the quote; "demon" is left as transcribed, as the earlier nexus record left it. Ends with a question to be answered: whether the compiler can enforce the separation.

> Well, what I meant was that the MetaNexus is the whole demon, right? That is what we replace the concept of demon with. What I meant was that there's a meta actor also: the Nexus meta actor, the Sema, and the Signal. We talked about this, but we never actually reviewed it together: how the trait enforces that it can only be used inside of a particular meta actor, like either the Signal actor, the main Signal actor, or the Nexus actor. The Nexus actor, the Sema actor, and the Signal actor have their sub-actors, or possibly their implementations, that need to run inside these actors.
>
> We can prioritize which part of the three we should eventually be able to do, but also because it forces a certain part of the logic in a certain actor, where it's declared. We have the processes in the Nexus runtime that act as the only way to a Sema transformation. We separate the logics in the code, and we enforce it on the compiler. Is that possible?

-- psyche, STT.
