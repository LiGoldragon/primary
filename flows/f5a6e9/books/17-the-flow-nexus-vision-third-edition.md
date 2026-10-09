<!-- to-the-living:start -->
Presentation.{ «The Flow Nexus vision», third edition }

## Distillation

### 1. `psyche-skills/vision/flow-ethos.md`, new file

Lines removed: none. Lines added, the whole file:

```
---
description: The Flow Nexus vision, in ethos: the
metaflow record, what reaches a flow, and how a
flow starts; the code is brought into line with it.
dependencies: [vision-flow, vision-ethos]
---

## What Flow names

Library                         ; Flow's
[]
[  FlowId.String                ; unideal now; a
                                ; real id built on
                                ; the hash bits that
                                ; identify a flow is
                                ; needed
   Topic:Name                   ; inline import of
                                ; a core built-in:
                                ; camelCase, checked
                                ; where text enters;
                                ; core, flow, ethos
   Layer.[                      ; decides the model
      Primary
      Secondary
      Tertiary
      Quaternary ]
   Psyche.{                     ; his words, relayed
      Context.String            ; where it was said
      Verbatim.String }         ; the words whole
   Request.[                    ; reaches a flow
      Order.String              ; wakes
      Question.String           ; wakes
      Psyche                    ; wakes
      Psyches.Vector<Psyche>    ; wakes
      Result.String             ; a flow's answer:
                                ; delivered awake,
                                ; waits asleep
      Notice.String ] ]         ; a merge, thanks:
                                ; wakes nothing
[]
[]

A request is one layer of variants; a psyche carries
his words and their context and nothing of the
relaying flow's own. Delivered as one vector, oldest
first, the waking request last:

[  Notice.«branch flowRefresh merged»
   Result.«tests pass on the pushed revision»
   Order.«bring the refresh to production» ]

## The metaflow record

Memory                          ; Flow's
[  flow_ethos:[ FlowId Topic Layer Request ] ]
[  Metaflow.[                   ; the aspects are
      Psyche.Details            ; the variants; the
      Mind.Details              ; struct holds the
      Field.Details ]           ; details
   Details.{
      Topic                     ; core: the heart of
      Layer                     ; its aspect
      State.[
         Awake.FlowId           ; its current flow
         Asleep                 ; a request wakes it
         Ended ]
      Past.Vector<FlowId>       ; the last few only,
                                ; oldest first; the
                                ; whole history is
                                ; not kept
      Queue.Vector<Request> }   ; waiting, oldest
                                ; first
   Flow.{                       ; one per run
      FlowId
      Session.String            ; the harness's id
      Events.Vector<Event> } ]

Written, two metaflows:

Psyche.{
   core
   Primary
   Awake.startInputVital
   [ zooWrongYouth ]
   [ ] }

Mind.{
   flowRefresh
   Secondary
   Asleep
   [ ]
   [ Notice.«branch merged» ] }

A thread's title is the metaflow written short,
aspect, topic and layer, then the flow's words,
without the model: Psyche.{ flow Primary
startInputVital }.

## How a flow starts

Signal                          ; what Flow is asked
[  flow_ethos:[ Metaflow FlowId Request ]
   curriculum:[ Name ] ]
[  Launch.{                     ; a metaflow's first
      Metaflow                  ; flow; the metaflow
      Modules.Vector<Name>      ; written short
      Brief.String }            ; a small paragraph
   Wake.{                       ; a sleeping
      Metaflow                  ; metaflow's next
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
      Locked                    ; refresh under way
      Unknown.Name              ; a module
      NoLayer ] ]               ; no model for it
[]

Written, a launch of this flow:

Launch.{
   Psyche.{ flow Primary }      ; written short
   [ vision-flow
     knowledge-ethos ]
   «Design Flow's module registry.» }

A launch names a metaflow by its aspect, topic and
layer, this flow's own modules, and a brief. Flow
composes the system prompt and the first prompt from
the module registry and the layer's model; reserves
the flow id; opens the pane; spawns the harness;
binds the flow to the session the harness reports;
titles it; submits the first prompt once. The hook
reports Started. A wake launches the same way, with
the drained queue delivered with the first prompt,
the waking request last. A metaflow's record is
written at reservation, before any harness runs:
identity is a field of the request, not read off a
title or a model. None of this is in production:
today the Primary launch scripts start flows and
the bottom layer of each aspect runs the refresh.
```

Ruling 1: (a) yes. (b) amend the ethos. (c) amend the file's name or its split.

### 2. `psyche-skills/vision/flow.md`, line 3

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

### 3. Where a request lands in a running flow

A queue drained for a sleeping metaflow lands with the first prompt of its next flow. For a flow already awake, your records point two ways: at the end of the prompt, or as a tool-call return or asynchronous signal that every flow has running, outside the prompt. The ethos above does not fix it.

Ruling 3: (a) at the end of the prompt. (b) as a tool-call return, outside the prompt. (c) your word.
<!-- to-the-living:end -->
