# The anatomy

Everything designed so far, as four ethos roots of Flow. A voice is an aspect and a layer; `kind` stays an ethos word, a module has a module type; a name maps to a path once; a role is configured once.

## 1. Library: the shared types

```
Library
[]
[ FlowId.Integer
  Role.[ Voice.{ Aspect.[ Psyche
                          Mind
                          Field ]
                 Layer.[ Primary
                         Secondary
                         Tertiary
                         Quaternary ] }
         SystemAudit
         LivingInteraction
         Implementation
         VisionAudit ]
  ModuleType.[ Spirit
               Intent
               Vision
               Knowledge
               Compensation
               Trial
               Operation
               Role ]
  Name.String
  Location.[ Path.String ]
  Module.{ ModuleType
           Name
           Location }
  Selection.{ ModuleType
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
{ Voice.{ Psyche Primary }
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
