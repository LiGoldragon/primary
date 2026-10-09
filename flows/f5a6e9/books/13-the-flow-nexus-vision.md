<!-- to-the-living:start -->
Presentation.{ «The Flow Nexus vision» }

## 1. `psyche-skills/skills/vision-flow-ethos.md`, new file

Lines removed: none. Lines added, the whole file:

```
---
description: The Flow Nexus vision, in ethos: the
metaflow record and how a flow starts, judged or
written; the code is brought into line with it.
dependencies: [vision-flow, vision-ethos]
---

## The metaflow record

Memory                          ; Flow's
[  flow:[ FlowId Request ] ]
[  Metaflow.[                   ; one variant per
      Psyche.Details            ; aspect; the struct
      Mind.Details              ; holds its details
      Field.Details ]
   Details.{
      Layer.[                   ; decides the model
         Primary
         Secondary
         Tertiary
         Quaternary ]
      Topic                     ; Core when it has
                                ; no topic of its own
      State.[
         Awake.FlowId           ; its current flow
         Asleep                 ; a request wakes it
         Ended ]
      Past.Vector<FlowId>       ; oldest first
      Queue.Vector<Request> }   ; waiting, oldest
                                ; first
   Topic.Dense
   Dense.String                 ; PascalCase, one to
                                ; four words, letters
                                ; only; checked on
                                ; the way in
   Flow.{                       ; one per run
      FlowId
      Session.String            ; the harness's id
      Events.Vector<Event> } ]

Written:

Psyche.{
   Primary
   Core                         ; the heart of its
   Awake.startInputVital        ; aspect
   [ zooWrongYouth ]
   [ ] }

## How a flow starts

Signal                          ; what Flow is asked
[  flow:[ Metaflow FlowId Request ]
   curriculum:[ Name ] ]
[  Launch.{                     ; a metaflow's first
      Metaflow                  ; flow; the metaflow
      Modules.Vector<Name>      ; written short
      Brief.String }            ; a small paragraph
   Wake.{                       ; a sleeping
      Metaflow                  ; metaflow's next flow
      Request }                 ; the waking request
   Refresh.Metaflow             ; the next link
   End.Metaflow
   Current.Metaflow ]
[  Launched.FlowId
   Woken.FlowId
   Refreshed.{
      FlowId                    ; the successor
      FlowId }                  ; the predecessor
   Ended
   Current.[
      Awake.FlowId
      Asleep
      Ended
      Unknown ]
   Refused.[
      Locked                    ; a refresh under way
      Unknown.Name              ; a module
      NoLayer ] ]               ; no model for it
[]

Written, a launch of this seat:

Launch.{
   Psyche.{ Primary Core }      ; written short
   [ vision-flow
     knowledge-ethos ]
   «Design Flow's module registry.» }

A launch names a metaflow by its aspect, layer and
topic, this flow's own modules, and a brief. Flow
composes the system prompt and the first prompt from
the module registry and the layer's model; reserves
the flow id; opens the pane; spawns the harness;
binds the flow to the session the harness reports;
titles it; submits the first prompt once. The hook
reports Started. A wake launches the same way, with
the drained queue at the end of the first prompt,
the waking request last. A metaflow's record is
written at reservation, before any harness runs:
identity is a field of the request, never read off
a title or a model.
```

Ruling 1: (a) yes. (b) amend the name of the file or its split. (c) amend the ethos.

## 2. `psyche-skills/skills/vision-flow.md`, line 3

Line removed:

```
dependencies: [vision-nexus, vision-ethos]
```

Line added:

```
dependencies: [vision-nexus, vision-ethos,
vision-flow-ethos]
```

Ruling 2: yes, or amend.
<!-- to-the-living:end -->
