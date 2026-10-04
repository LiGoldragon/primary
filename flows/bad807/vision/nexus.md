# The Nexus

## Proposal 1 of «The Nexus» lands, with example code

Context: his comment on «The Nexus», proposal 1 (Vision/nexus.md, new section "Three parts and one path"). Relayed by aa887c.

> This is good. Can land, and I would also like to have example code to show with it.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

## The entry point as actors: a main actor talks only to operation; signal and memory talk only to operation; flesh out in code, test on a branch of a non-production nexus, hand to Astra

Context: his comment on «The Nexus», proposal 2 (the standard entry point). Relayed by aa887c; "Message" marked [sic] by the relay.

> Let's flesh this out in actual code. Could we say it better: an actor, a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor, which could talk to both signal and memory. Operations can talk to both. Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process. Let's look at the actual code and how this could be done in multiple various ways. Let's test it. Let's have it tested on an actual component that we have written, like Flow, Message [sic], or Orchestrate, on a branch, and see if it works as the other component or if we could make it work. A toy, I mean, or a simple nexus which isn't in production, something that we've been drafting. Maybe let's do something useful. If we're going to test anything, we might as well test one of our non-production-ready ideas. You can hand this over to Astra once you have the design and the book. I want extensive: I want to see code. I want to see visual architecture. I want to feel like you have some meat there on that bone.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

## The core library's language is refined after practice, actor-based or not

Context: his comment on «The Nexus», on the text "The nexus repository is the core library of every Nexus…". Relayed by aa887c.

> Again after we see how this works in practice, let's refine the language so that it's more accurate to what's possible and what we actually want in practice. In terms of whether it is an actor-based language or whether it is different

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

## A Nexus pulls a value from a datom file through its CLI; Fable leads the design as a book

Context: his comment on «The Nexus», on the text "Every client speaks to a Nexus in pure signal, fully binary…". Relayed by aa887c; "me" marked [sic] by the relay.

> Yes this is good and I also want to design something that would let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this but it would be a fairly simple call, I guess, where it would have a variant `me` [sic] that would tell it what type of CLI you would have to use, essentially. That means storing a string somewhere because the CLI is invoked with a system call that uses a string. There's a string involved no matter what unless all of that is, again, put into an external tool. Anyway let's look at different ideas here, with Fable being the lead designer on this and passing it down as a book.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.
