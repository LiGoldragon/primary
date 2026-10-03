Presentation.{ «Context modules» }

## 1. What a context module is

A skill is a piece of prompt. The same piece can be placed in the system prompt, placed in the first prompt, or left for the flow to load. So a skill, a vision file, a spirit or intent statement are all one thing: a context module — a Markdown file with a kind and a name.

> "the system that we have for skill is really just like a prompt system, so we can use these either in the system prompt or in the prompt, or just let the agent have these skills available to load."
-- psyche, STT, 2026-10-03.

## 2. The registry, in Flow's memory

Flow keeps where every module is. For now a location is a file path; later a repository.

```
Library
[]
[ Kind.[ Spirit
         Intent
         Vision
         Knowledge
         Compensation
         Trial
         Operation
         Role ]
  Name.String
  Location.[ Path.String ]
  Module.{ Kind
           Name
           Location }
  Reference.{ Kind
              Name }
  Composition.{ SystemPrompt.Vector<Reference>
                FirstPrompt.Vector<Reference>
                Loadable.Vector<Reference> } ]
[]
[]
```

## 3. The launch

A launch names, for the system prompt and for the first prompt separately, the list of kind-and-name pairs to load, and which others stay loadable. Flow reads each file and inserts its text in that place. Nothing else composes a prompt.

> "We pass a list of which type and name for the context we want to load at each layer in the system prompt and in the origin startup prompt. They accept these values, and the flow nexus just inserts those values in the right places."
-- psyche, STT, 2026-10-03.

## 4. The meta socket

Adding a skill is adding a module to the registry, over Flow's meta socket.

```
Signal
[ context:[ Module Name ] ]
[ Register.Module
  Forget.Name ]
[ Registered
  Forgotten
  Refused.[ Duplicate.Name
            Unknown.Name ] ]
[]
```

Mind Astra has your words and the order to design and write this.

1. Build it as drawn.
2. Comment what to change.
