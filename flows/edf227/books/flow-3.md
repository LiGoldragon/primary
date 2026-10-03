Presentation.{ «Flow» }

## 1. What Flow does

Flow launches a flow: it assembles the flow's system prompt and first prompt from its role's configuration, starts the harness, and hears every event through the harness's hooks calling the Flow CLI. When a flow nears its context limit, Flow builds its successor and ends it. Its configuration lives in its own memory.

## 2. A flow and its role

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
         Implementation
         VisionAudit ]
  Kind.[ Spirit
         Intent
         Vision
         Knowledge
         Compensation
         Trial
         Operation ]
  Name.String
  Reference.{ Kind
              Name }
  Composition.{ SystemPrompt.Vector<Reference>
                FirstPrompt.Vector<Reference>
                Loadable.Vector<Reference> }
  Model.String
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
[]
[]
```

## 3. What a role carries, in Flow's memory

Each role has one configuration record: which context modules go in the system prompt, which in the first prompt, which stay loadable, and the model. Launching a role is naming it.

```
Memory
[ flow:[ FlowId
         Role
         Composition
         Model
         Event ] ]
[ RoleConfiguration.{ Role
                      Composition
                      Model }
  Flow.{ FlowId
         Role
         State.[ Running
                 Idle
                 Ended ]
         Vector<Event> } ]
```

One record, as datom, for the Psyche voice at the Primary layer:

```
{ Voice.Psyche.Primary
  { [ { Spirit spirit }
      { Vision flow }
      { Vision ethos } ]
    [ { Operation launch } ]
    [ { Knowledge nexus }
      { Knowledge flow } ] }
  claude-fable-5-1 }
```

## 4. The id in words

A flow id is 33 bits of the harness's own session id, rendered as three words, reversible: from the words, tools find the transcript.

1. Build it as drawn.
2. Comment what to change.
