# A flow is a struct with a role; voice is one variant of role

## Role is an enum: voice, system audit, live psyche interaction, implementer, vision audit; each runs on the smallest, highest-signal context
Comment on «Flow», at the voice.
> "I think that the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice. The other variants are going to be all the other roles that we create: a system audit; live psyche voice interaction; an implementation; an implementer; a vision audit. These are actually things that are better done with the prompt perfectly aligned, and then they're just running right out of the door. They're just producing the best output based on the smallest, most concentrated, highest signal-to-noise context that we can assemble."

-- psyche, STT then pasted, 2026-10-03.

## Main flows pass everything to subagents; eventually subagents are themselves flows, fully asynchronous
> "That's why they're called main flows: they pass everything to a sub-agent, but eventually all the sub-agents will themselves be flows, so that we have a fully asynchronous system, I think. Anyway, maybe some of them will still use sub-agents, but more trivially."

-- psyche, STT then pasted, 2026-10-03.

## Role names: living interaction, implementation, vision audit
Comment on «A flow and its role», at the ethos block.
> "Well either it's living interactor, an implementer, or vision auditor, or it's living interaction, implementation, and vision audit. I think that I prefer the latest."

-- psyche, typed, book comment, 2026-10-03 18:53.

## Voice is a struct of Aspect and Layer
Comment on «The anatomy», at the Voice variant, written as ethos by him.
> ```
> Voice.{ Aspect.[ Psyche Mind Field ]
>         Layer.[ Primary
>                 Secondary
>                 Tertiary
>                 Quaternary  }
> ```

-- psyche, typed, book comment, 2026-10-03T19:13Z.
