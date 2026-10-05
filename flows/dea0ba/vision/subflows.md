
## Specialized subagent roles

> you and probably everybody else have to write huge prompts for your subagent, which is not what I want. I want specialized subagent roles that already have almost everything they need to know to do certain things and you just send them one or two lines, very extremely brief. An extremely fucking cheap subagent is what I want.

-- psyche, typed, 2026-10-03; relayed by 9fb0ad from flows/9fb0ad/vision/subflows.md.

> I think that the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice. The other variants are going to be all the other roles that we create: a system audit; live psyche voice interaction; an implementation; an implementer; a vision audit. These are actually things that are better done with the prompt perfectly aligned, and then they're just running right out of the door. They're just producing the best output based on the smallest, most concentrated, highest signal-to-noise context that we can assemble. That's why they're called main flows: they pass everything to a sub-agent, but eventually all the sub-agents will themselves be flows, so that we have a fully asynchronous system, I think.

-- psyche, STT, 2026-10-03 approximately19:15Z; relayedPsycheFableedf227, «Flow» book voice comment.


## Primary designs; Secondary implements and tests

> You're just going to manage the whole thing. That's what secondary is for. Primary deals with designs and ideas, and he passes them on to secondary. Secondary then implements and tests, because if Fable passes out an implementation job, it's going to be Opus. He can just talk to the Opus main flow, who will then coordinate it with Opus sub-agents to implement it. Fable and [Astra] can just deal with design and ideas and concepts and send it down to secondary.

— the living, to Psyche Opus tonight; relayed verbatim by Psyche Fable 5ed94b, 2026-10-03.
