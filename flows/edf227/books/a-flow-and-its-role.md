# A flow and its role

## 1. A flow is a struct; its role is an enum

A flow is one run with a role. A voice is one role among the roles we make; each other role runs once, on the smallest, most concentrated context that can be assembled for it, and is gone when done.

> "the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice."
-- psyche, STT, 2026-10-03.

## 2. In ethos

```
Library
[]
[ Layer.[ Primary
          Secondary
          Tertiary
          Quaternary ]
  Role.[ Voice.[ Psyche.Layer
                 Mind.Layer
                 Field.Layer ]
         SystemAudit
         LivingInteraction
         Implementer
         VisionAudit ]
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
[]
[]

Memory
[ flow:[ FlowId Role Event ] ]
[ Flow.{ FlowId
         Role
         State.[ Running Idle Ended ]
         Vector<Event> } ]
```

## 3. What a role carries

A role names its context modules: which go in the system prompt, which in the first prompt, which stay loadable. Launching a role is naming it; Flow assembles the rest.

## 4. Where this goes

Main flows hand everything to subflows today. The direction is that each subflow becomes a flow with a role of its own, so the whole runs asynchronously; some trivial work may stay a subagent.

1. Build it as drawn.
2. Comment what to change — more roles, or a different name for one.
