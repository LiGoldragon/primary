<!-- to-the-living:start -->
Presentation.{ «The metaflow's ethos» }

## 1. `flow/crates/flow-nexus/ethos/memory.ethos`, the `Metaflow` record of «The metaflow record», second edition

Lines removed:

```
   Metaflow.{
      Name.[
         Voice.{                 ; permanent
            FlowAspect
            Layer.[
               Primary
               Secondary
               Tertiary
               Quaternary ] }
         Goal.String ]           ; camelCase; ends
      State.[
         Awake.FlowId            ; its current flow
         Asleep                  ; a request wakes it
         Ended ]
      Past.Vector<FlowId> }      ; oldest first
```

Lines added:

```
   Metaflow.[                    ; one variant per
      Psyche.Details             ; aspect; the struct
      Mind.Details               ; holds its details
      Field.Details ]
   Details.{
      Layer.[                    ; decides the model
         Primary
         Secondary
         Tertiary
         Quaternary ]
      Topic                      ; Core when it has
                                 ; no topic of its own
      State.[
         Awake.FlowId            ; its current flow
         Asleep                  ; a request wakes it
         Ended ]
      Past.Vector<FlowId>        ; oldest first
      Queue.Vector<Request> }    ; waiting, oldest
                                 ; first
   Topic.Dense                   ; a new type
   Dense.String                  ; PascalCase, one to
                                 ; four words, letters
                                 ; only; checked on
                                 ; the way in
```

Written, two metaflows:

```
Psyche.{
   Primary
   Core                          ; the heart of its
   Awake.startInputVital         ; aspect
   [ zooWrongYouth ]
   [ ] }

Mind.{
   Secondary
   FlowRefresh
   Asleep
   [ ]
   [ Notice.«branch merged» ] }
```

Ruling 1: the shape, yes or amend; and the name of the topic's string type: (a) Dense. (b) ShortName. (c) Annex. (d) your word.
<!-- to-the-living:end -->
