# The anatomy

Everything designed so far, as four ethos roots of Flow. The parts carry no repetition: a kind is named once, a name maps to a path once, a role is configured once.

## 1. Library: the shared types

```
Library
[]
[ FlowId.Integer
  Layer.[ Primary
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
  Location.[ Path.String ]
  Module.{ Kind
           Name
           Location }
  Selection.{ Kind
              Vector<Name> }
  Placement.[ SystemPrompt
              FirstPrompt
              Loadable ]
  Placed.{ Placement
           Vector<Selection> }
  Model.String
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
[]
[]
```

## 2. Memory: what Flow keeps

A module's name maps to its path once. A role's configuration says, for each placement, which names of which kind. A flow is its id, its role, its state and its events.

```
Memory
[ flow:[ FlowId
         Role
         Module
         Placed
         Model
         Event ] ]
[ RoleConfiguration.{ Role
                      Vector<Placed>
                      Model }
  Flow.{ FlowId
         Role
         State.[ Running
                 Idle
                 Ended ]
         Vector<Event> } ]
```

The Psyche voice at the Primary layer, as one configuration record:

```
{ Voice.Psyche.Primary
  [ { SystemPrompt [ { Spirit [ spirit ] }
                     { Vision [ flow ethos ] } ] }
    { FirstPrompt [ { Operation [ launch ] } ] }
    { Loadable [ { Knowledge [ nexus flow ] } ] } ]
  claude-fable-5-1 }
```

## 3. Signal: what anyone may ask

The simple form names a role; the extended form carries the flow id. Common queries use the simple form.

```
Signal
[ flow:[ FlowId
         Role
         Event ] ]
[ Launch.Role
  Resolve.Role
  Report.{ FlowId
           Event } ]
[ Launched.FlowId
  Resolved.FlowId
  Reported
  Refused.[ UnknownRole.Role
            Busy.Role
            UnknownFlow.FlowId
            NativeLaunchRefused ] ]
[]
```

## 4. Meta signal: what the owner configures

Adding a skill is registering a module. Changing what a role loads is configuring the role.

```
Signal
[ flow:[ Module
         Name
         RoleConfiguration
         Role ] ]
[ Register.Module
  Forget.Name
  Configure.RoleConfiguration ]
[ Registered
  Forgotten
  Configured
  Refused.[ DuplicateModule.Name
            UnknownModule.Name
            UnknownRole.Role ] ]
[]
```

Not yet drawn, each its own book when you ask: the vision relay by topic, the accounting of quota and priority, the word rendering of FlowId.

1. Build it as drawn.
2. Comment what to change.
