# Psyche

## 2026-10-29 — Long-term ideas, underspecified, are built monolithic; the bind of long term and short term
Context: the living, 21:10, comment on Flow, whole, on the line "The Flow Nexus sets up and starts a model flow".

I think it's appropriate here to also mention that I'm in a bit of a bind here because there's the long-term vision, right? We've talked about this: how we want them separated, but it is complicated. The more complexity we introduce, obviously, the more we have to manage. At the same time, I've been bitten really hard by not specifying something as long-term, meaning not necessary on the next iteration. Because long-term ideas are usually underspecified and lack the surrounding context to explain how my modular vision composes, usually the implementer approaches things in a monolithic way. The implementation ends up cramming a bunch of ideas together that create a broken system because there's just not enough abstraction already and not enough instructions on how to compose these abstractions. Also, the implementer sometimes or often has a hard time understanding that a feature needs to be configurable. This, I believe, even though I keep talking about it, is going to keep biting us because the model that we currently have, or the way that the thinking machine is set up, tries to just get the shortest route to what it thinks it needs to make. It essentially does in one step what should be done in multiple steps, right? It would be like asking the guy who drives the nail into the frame of the house to: - design the house - do the orders - do the accounting - do the taxes - contact the client - order the material - make the decisions - replace the foreman - replace the janitor - drive the nails into the What happens when this happens is they build a mud hut, right? What I'm making is not a mud hut, and so if we're not clear about the fact that we don't want to try to build the Empire State Building out of mud and straw, we're probably just going to end up with a pile of mud.

## 2026-10-29 — Vision divided by horizon into modules: unmarked, short, medium, long, and a far one
Context: the living, in the Psyche core Primary chat 554e1a, on the proposal Two horizons (https://claude.ai/artifact/9WCADhbhbER9oXAaepEchL).

I think that putting the long vision with the short vision in one file will create a bunch of ghost effects, because if anyone wants to know anything about this topic, they have to load all of it. They can't choose to just know how the system is expected to work in the short term, which is useful most of the time for most flows, but especially flows that don't design like field-aspect flows.

I would divide them. I would even say we can make three: the short, the medium, and the long-type vision. Maybe we do `vision:short:Flow Nexus`, for example.

What I was thinking just now is that the short is special also in that it's a compromise, a short-term compromise. It would be essentially anything that's marked as a compromise, a short-term solution, or a hack. The medium-type vision would maybe hold anything that's horizon-agnostic, but it would describe the system as we would like it to look past the short and compromised phase. The long vision would describe what we would like it to be ideally.

We could even introduce, I don't know what we would call it, the naive way would be to say "very long," or maybe there's a term. Maybe in some cases we have this extra-far idea, which rarely ever gets loaded except for flows that need to understand the living's overall broad vision. This would allow for much more efficient development that can focus.

Let's say we have problems. Let's say we're in a situation where things are breaking and we need to get the system going again. This is the implementer that would be started to fix things. It could be loaded only with the short vision.

I think that the unmarked type, the vision that does not have short, medium, or long, is actually where we would put the horizon-independent or horizon-insensitive part of the vision. What do you think of all this?

Landed in psyche-context intent/psyche.md (commit c386f58): Vision by horizon, flows/b2b87a/books/horizons.md.
