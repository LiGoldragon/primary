# His comments on the bad807 books (read 2026-10-04)

Fourteen books read in publication order. Eight comments in all, six of them new. Every other book has no comment.
"Recorded" means under flows/bad807/.

## «Context modules: where each proposal lands» (2026-10-04)

1. Anchored to: "A context module is one file of prompt text with a type, a name and a description. The type says who stands behind it…"
   His comment: "This is partly hallucination. The work is vague. This specific has been hallucinated into a general so it's bluffing. It's misplaced context."
   Recorded: reports/comments-2026-10-04.md; vision/contextModules.md and log.md (the cut of "the work is editing context modules").

2. Anchored to: the same passage.
   His comment: "There's no role type and I don't know if we want to list the types in too many places. Where is the canonical place to find those types?"
   Recorded: reports/comments-2026-10-04.md; vision/contextModules.md and log.md (no Role type; types declared once in curriculum-deploy's ethos).

## «The Nexus» (2026-10-04)

3. Anchored to: the shape drawing (a box in the three-part figure).
   His comment: "This is a good visual. I would like it to become an actual distilled vision. Let's talk about how we deal with distilling vision: data-wise, format-wise, version control-wise. What kind of format is this? What's the best format we want to use, something that both the machine can use as context and that humans can easily perceive?"
   Recorded: new.

4. Anchored to: "1. [vision] Vision/nexus.md, new section "Three parts and one path"…" (proposal 1).
   His comment: "This is good. Can land, and I would also like to have example code to show with it."
   Recorded: new.

5. Anchored to: the code block "Library ; what the three parts share [] ; imports: none [ FlowId.Integer ; types Voice.[ Psyche.Layer …" (The anatomy in code).
   His comment: "There are two things that are not really related but kind of meet:
   1. There's a missing variant called `field`.
   2. Now I'm seeing a syntax or a pattern in Ethos that I would like to develop because it allows for a certain cool-looking datom syntax: a series of variants one after another. There possibly could be many of those although I think the most common use is for two variants in a row, because after that you might as well use a struct. One could argue that one could use a struct from the beginning and I think that might be simpler.

   I think we're going to abandon this idea that we wouldn't have an enum where each data-carrying variant carries the same type, because it creates this repetition that you can see now: `seq.layer`, `mine.layer`, `.layer` is being repeated. I think rather the voice is a struct that contains the aspect and the layer, and the flow has a role, one of which is a voice. We can start leaning more on strokes [structs?] than on chaining up variance [variants], which ends up in an ugly Ethos pattern."
   Recorded: new.

6. Anchored to: "2. [vision] Vision/nexus.md, new section "The standard entry point"…" (proposal 2).
   His comment: "Let's flesh this out in actual code. Could we say it better: an actor, a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor, which could talk to both signal and memory. Operations can talk to both. Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process.

   Let's look at the actual code and how this could be done in multiple various ways. Let's test it. Let's have it tested on an actual component that we have written, like Flow, Message, or Orchestrate, on a branch, and see if it works as the other component or if we could make it work. A toy, I mean, or a simple nexus which isn't in production, something that we've been drafting.

   Maybe let's do something useful. If we're going to test anything, we might as well test one of our non-production-ready ideas. You can hand this over to Astra once you have the design and the book. I want extensive: I want to see code. I want to see visual architecture. I want to feel like you have some meat there on that bone."
   Recorded: new. [?] "Message" may be Messenger or a component name misheard.

7. Anchored to: "Proposed: > The nexus repository is the core library of every Nexus. It defines the kinds of the three parts and the sta…"
   His comment: "Again after we see how this works in practice, let's refine the language so that it's more accurate to what's possible and what we actually want in practice. In terms of whether it is an actor-based language or whether it is different"
   Recorded: new.

8. Anchored to: "Proposed: > Every client speaks to a Nexus in pure signal, fully binary. A Nexus speaks only the signal contracts it is …"
   His comment: "Yes this is good and I also want to design something that would let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this but it would be a fairly simple call, I guess, where it would have a variant `me` [?] that would tell it what type of CLI you would have to use, essentially. That means storing a string somewhere because the CLI is invoked with a system call that uses a string. There's a string involved no matter what unless all of that is, again, put into an external tool. Anyway let's look at different ideas here, with Fable being the lead designer on this and passing it down as a book."
   Recorded: new.

## Books with no comment

«Context modules: the standard and the first system-prompt modules»; «Context visibility: every flow's context and quota on one screen»; «Datom»; «Flows per topic: a notion and what others have done»; «Signal»; «Three skill repositories and the main workspace»; «Operation»; «Context modules: your two comments answered»; «Ethos»; «Memory»; «Placing the skills: three questions»; «Two lines of your vision touched by the placing».
