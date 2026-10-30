
## Hunting unknowns, in waves (comment on «The missing pieces»)
"We almost want to hunt unknowns, obsessed over doubt. Essentially looking for unknowns is demonstrating doubt. It would be a sort of a cycle that reoccurs like a wave. At every stage we would certainly want to ask ourselves again: What is it we don't know?"
"There would be two modes of operation. Obviously sometimes we want to build a prototype, which means not blocking. In design we block and in prototype building we document assumptions."
"Well no one can know ahead of time that the pieces are enough to yield a system that essentially is the best version that we could come up with at the moment. The ideal system: everybody is contributing to the judgment. There really won't be a limit. The hardest part of a thinking machine to get is how to judge that an idea is complete or not. It's not going to be a simple answer."
"I think the first thing we need to do is investigate further the concept of an ideal system and its anatomy so that we can use that as a benchmark against which to ask, "What are we missing?""
-- psyche, STT (book comments), 2026-10-12.

## The Nexus parts are the machine's anatomy
"I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more.

I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. Let's do that."
Context: said after the second edition of «The missing pieces», on what the golden system is.
-- psyche, STT, 2026-10-12.

## Never build our abstraction inside someone else's
"Okay let's open this up because the idea that modifying somebody else's abstraction to create our own abstraction is the smallest change is so fucking stupid. I want you to talk to people about this and you guys figure out the million ways why this is stupid beyond fucking description."
Context: Field had called a restart policy inside Herdr (third-party software) "the smallest change" for keeping the committer alive; Fable had suggested looking at Herdr; d68c82 ordered it built.
-- psyche, STT, 2026-10-12.

## Nuts and bolts, not welding
"I'd really like this to go and to become something that we can use to ensure that machines don't try to put our ideas, put our system. It's like, "Why do you use nuts and bolts to put a car together and you don't just weld everything together?" Do you tell me why you use nuts and bolts and you don't just fucking weld everything together? Explain that to me and then translate that into why we don't just fucking weld everything together with other people's components."
Context: following the Herdr restart idea; "put our ideas, put our system" is an unfinished thought, read as: put our ideas or our system inside other people's components.
-- psyche, STT, 2026-10-12.

## A concept in the wrong component
"I'm not only talking about putting abstraction in other people's components. I'm talking about our components holding the abstraction in the wrong component. This is why I keep referring to the anatomy of a design of a system, because if you build it wrong then it won't be able to walk. Or maybe it can walk but it can't run, right? Or maybe it can run but it can't turn or it can't stop, which makes it fucking useless. ... At least now we know that we need to train the machine against doing something that incredibly fucking stupid."
-- psyche, STT, 2026-10-12.

## No values in the runtime
"Plus you were going to put a configurable feature. You were going to hardcode that feature in the code and not even expose it through configuration. It's like if you make a car that starts as soon as you put gas in it. Nobody has control so you can't leave gas in the car, right? The car just runs. As soon as it has gas it just fucking starts and it runs until the gas is out. That's the kind of car you're building.

There's no way to turn the car on or off. We never, ever, ever, ever, ever put something that we might want to change later into the code. The code only holds the machine that takes the configuration and turns it into the system as we want it to run. We never hardcode the configuration into the runtime. The runtime should be free of any kind of value. There should be no values in our runtime. All the values should be fed in, except things that are structural, like what defines the [proto's] language structure. Even then it's not worth creating an abstraction to create other languages. That's basically the only time when we would do that: when you're designing the actual language you're using to code, you have to create some kind of hard facts. That's where the language is, but anything else, we should have no values in the code.

I don't want you to take this and go so crazy that you start pulling out constants that actually somehow deserve their role. I have a strong suspicion that if somebody went auditing for that kind of stuff, we would find a lot of slop."
-- psyche, STT, 2026-10-12.
