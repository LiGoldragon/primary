# The anatomy

Everything designed so far, as four ethos roots of Flow, with a comment on every line that has a next layer saying what the machine reads there.

## 1. Library: the shared types

```
Library                              ; a Library root: types every component shares
[]                                   ; imports: none, every type is declared here
[ FlowId.String                      ; a flow's id: the harness's own session hash
  Role.[ Voice.{ Aspect.[ Psyche     ; a flow's role; a voice is an aspect and a layer
                          Mind
                          Field ]
                 Layer.[ Primary
                         Secondary
                         Tertiary
                         Quaternary ] }
         SystemAudit                 ; the focused roles run once and end
         LivingInteraction
         Implementation
         VisionAudit ]
  ModuleType.[ Spirit                ; what stands behind a context module
               Intent
               Vision
               Knowledge
               Compensation
               Trial
               Operation
               Role ]
  Name.String                        ; a module's name, unique within its type
  Location.[ Path.String ]           ; where the module's file is; a path for now
  Module.{ ModuleType                ; one registry entry: type, name, location
           Name
           Location }
  Selection.{ ModuleType             ; names of one type a role wants
              Vector<Name> }
  Placement.[ SystemPrompt           ; where a selection goes in the flow's head
              FirstPrompt
              Loadable ]
  Placed.{ Placement                 ; one placement with its selections
           Vector<Selection> }
  Model.String                       ; the model a role runs on
  Event.[ Started                    ; what the harness's hooks report
          ToolUsed.String
          Stopped ] ]
[]                                   ; kinds: none here
[]                                   ; associations: none
```

## 2. Memory: what Flow keeps

```
Memory                               ; a Memory root: what the Nexus remembers
[ flow:[ FlowId                      ; imported from the Library above
         Role
         Module
         Placed
         Model
         Event ] ]
[ RoleConfiguration.{ Role           ; one record per role: its placements and model
                      Vector<Placed>
                      Model }
  Registry.Vector<Module>            ; the registry: every module's type, name, location
  Flow.{ FlowId                      ; one record per flow
         Role
         State.[ Running              ; derived from the events
                 Idle
                 Ended ]
         Vector<Event> } ]
```

The Psyche voice at the Primary layer, as one configuration record:

```
{ Voice.{ Psyche Primary }                        ; the role
  [ { SystemPrompt [ { Spirit [ spirit ] }        ; placed in the system prompt
                     { Vision [ flow ethos ] } ] }
    { FirstPrompt [ { Operation [ launch ] } ] }  ; placed in the first prompt
    { Loadable [ { Knowledge [ nexus flow ] } ] } ] ; left loadable by name
  claude-fable-5-1 }                              ; the model
```

## 3. Signal: what anyone may ask

```
Signal                               ; a Signal root: the ordinary socket's vocabulary
[ flow:[ FlowId                      ; imported from the Library
         Role
         Event ] ]
[ Launch.Role                        ; queries: start a flow of this role
  Resolve.Role                       ;   which flow holds this role now
  Report.{ FlowId                    ;   a hook reporting one event
           Event } ]
[ Launched.FlowId                    ; responses, one per query
  Resolved.FlowId
  Reported
  Refused.[ UnknownRole.Role         ; refusals are vocabulary, never text
            Busy.Role
            UnknownFlow.FlowId
            NativeLaunchRefused ] ]
[]                                   ; types private to this signal: none
```

## 4. Meta signal: what the owner configures

```
Signal                               ; the meta socket's vocabulary
[ flow:[ Module
         Name
         RoleConfiguration
         Role ] ]
[ Register.Module                    ; add a module to the registry
  Forget.Name                        ; remove one
  Configure.RoleConfiguration ]      ; set what a role loads and runs on
[ Registered
  Forgotten
  Configured
  Refused.[ DuplicateModule.Name
            UnknownModule.Name
            UnknownRole.Role ] ]
[]
```

1. Build it as drawn.
2. Comment what to change.
