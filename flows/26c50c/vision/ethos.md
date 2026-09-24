
## Audit focus — 2026-09-24

> Or maybe you should just audit what someone else is doing, make suggestions, ask questions, and bring questions to me.  Focus on ethos specification and an anatomy of traits.

-- living, typed directly in this flow.

## Evidence for design — 2026-09-24

> Use these dispatched subflows in order to get enough data to help you design the ethos types, traits, and kinds.

-- living, typed directly in this flow.

## Kinds and compiled conversion boundaries — 2026-09-24

> Yeah I meant kinds not traits. If I say traits I mean kinds. They're kind of the same thing but we say kind because I think it's actually more accurate.
>
> I want you to design that aspect of everything, or look at the design of it, and look at how enforced the ethos code is. Look at how we make sure that it's the code that runs, that it is compiled in, and that it does what it's supposed to be doing. It makes the code able to lower and lower (and vice versa) from a datom string or from string syntax into a Rust value, or not, depending on whether it has that option turned on during compilation. That way the Nexus doesn't do the string conversion but the CLI does and eventually the user interface will have all of that conversion-to-string logic compiled in.

-- living, typed directly in this flow.

## Process objects and syntax — 2026-09-24

> And then show me the Ethos syntax of what we're working on, of the objects that are involved. I don't even know how much this is actually used in practice, but the Nexus and the SEMA code: we're defining the types of processes that have to run, like:
> - starting a flow as a process
> - locking a herder pane
> - locking a flow, which is a process
> - sending a message, which is a process
> - pasting the message into the pane and sending it, which is a process
>
>
> These are all Nexus objects that didn't have to be used. This is maybe too advanced but this is how I want things to go if we can get closer to that.

-- living, typed directly in this flow.
