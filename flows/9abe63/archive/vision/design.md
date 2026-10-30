# Design

## 2026-10-30 — The golden rule of design becomes intent; the symptoms of bad design listed; allergic to strings in code; discussion through proposals
Context: the living, in the Psyche core Primary chat 9abe63, on the Primary's account of simplicity (Hickey, Brooks, Hoare, Gall), after ordering a new Nexus designed to replace Curriculum.

Yes the way you're describing it there, I like that: not braided together. Any part can be understood on its own and changed without touching the rest.

Complexity is whatever makes a system hard to understand or to change and its surest symptom is the special case. Every "except when" and "unless" is a place where two concerns were tied into one knot and each knot is a place the next change will trip.

Simple as opposed to easy. Easy is near at hand. Simple is unentangled and the two are often at odds. The duct tape is always the easy move.

Conceptual integrity: a system that reflects one set of ideas held whole by one mind is better than a grab bag of better ideas that don't fit. Make it simple. Make it so simple there are obviously no deficiencies rather than so complicated that there are no obvious ones.

The rewrite is designed first and small. A complex system that works grew from a simple system that worked. Yeah you're onto something there. I didn't read all that but you're on to the right trail.

We need some extreme measures. First let's make that intent. Let's create this. Let's develop that into a manifesto. Okay I'm not going to use the word manifesto because you're probably going to invent some nonsense out of this but I'm using it to illustrate my point. Do not reuse the word manifesto anywhere please. I just can't come up with a better word.

This is the golden rule of design. Then we'll have these forbiddens or symptoms of bad design, like file paths, any kind of string really in the code. The code, technically especially in the Nexus, shouldn't have any strings. You know what I mean? The strings are in the datom, in a string field that is designed to hold a string. That's essentially the only place, and the datom encoding and decoding library obviously handles strings. We're going to become allergic to strings. That's one thing I can think of.

Maybe you can run with this and take it farther than me. I think we're going to have to start discussing this through proposals now because I can't keep up. Especially if you keep making these giant chat responses, I can't read all of this. The Flow Nexus proposal was massive. It would take me a whole day just to get through it all. I just went through the first paragraph and it was full of deviations from my vision.

## 2026-10-30 — The golden rule reconsidered for ghosts and misplaced content; a match is not a fallback chain; intent:design rewritten whole for cohesion; belief edited for cohesion, modules kept from growing messily
Context: the living, same chat, after reading The golden rule of design (https://claude.ai/artifact/EdaPwKiPzcqfLYxuCQJs37).

I've read the Golden Rule and it's not bad but I want you to reconsider everything for a ghost effect and for content that doesn't belong there. I've seen some stuff that could belong elsewhere (I can't remember now).

Another thing was the fallback chain. I'm sure it is a good bad symptom to look for but let's make sure we don't ghost effect the machine into thinking it's not allowed to use match statements. A match statement is like try this, then try this, then try this, right? We would have to be clear. I think we need to make sure that we're clear about what counts as a bad symptom. Every time we have to account for what could sound like that but isn't a bad symptom.

I'd like you to consider possibly and almost entirely rewriting that whole design module to make it cohesive. I'd like to also approach this belief editing in such a way that we keep cohesion at a maximum and that belief modules don't grow exponentially or in a messy way. Do you understand what I'm saying?

## 2026-10-30 — The golden rule approved, second version, the whole rewrite of intent:design
Context: the living, same chat, on The golden rule of design (https://claude.ai/artifact/EdaPwKiPzcqfLYxuCQJs37), the redone version.

Okay the golden rule is good and this is a module that goes in the system prompt, right? Or have we never gotten to the point where we can put things in the system prompt? I'm wondering now.

To be clear I accepted the second version of that proposal, which I saw in the artifact list.

Landed: intent:design, psyche-belief 728ffb.

---

## 2026-10-30 — Curriculum's development is abandoned; a new Nexus is designed first, simple, without duct tape, exceptions or special scenarios
Context: the living, in the Psyche core Primary chat 9abe63, right after the Slash and burn order on belief modules.

Oh and here's an idea: let's start a new Nexus. We can keep using it for now but we're going to abandon development of the curriculum Nexus. This will become more and more of a standard full rewrite, where obviously we're not writing anything now. We need to design something first.

You're going to help me to make sure that we look at every angle and design a system that will work, that will be simple, and that won't have a bunch of haywire, duct tape, and exceptions. Essentially an exception, I don't know how to explain myself. The system must be simple, in a way of speaking. Obviously code is never that simple but we can't have all of this complicatedness, edge cases, and special scenarios. Do you understand what I'm saying? Can you explain it eloquently?

I'm sure people have talked about this. You could probably go and find a bunch of really smart people that have talked about this. We have a really big problem on our hands and it's both my fault and yours.

Landed: intent:design, psyche-belief 728ffb (the design part of Curriculum, flows/9abe63/vision/curriculum.md).
