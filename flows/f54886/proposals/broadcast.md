Presentation.{ «Broadcast to the hot flows» }

# Broadcast to the hot flows

*Created by Fable.*

His words: "The next version of Flow should have a way to figure out which flows are hot so you can broadcast messages cheaply and then tell them how to do text search from now on." A hot flow is one whose harness is up. Lands without his review, on his word; built in the version after 0.48.

### Proposal 1: Hot flows and a broadcast · psyche-belief › vision/flow-nexus-v1.md

**Comment** Two inputs: one lists the hot flows, one sends one request to all of them; the reply names who received it. The Memory already knows each flow's state, so nothing is added there.

```ethos
    Say.{ ComplexName Request }        ; the living, to a speaker
+   Hot                                ; the flows whose harness is up
+   Broadcast.Request                  ; one request to every hot flow
    Report.{ FlowId Event }            ; from a harness hook
```

```ethos
    Said.[ Delivered Queued ]
+   Listed.Vector<FlowId>              ; the hot flows
+   Broadcast.Vector<FlowId>           ; who received it
    Reported
```

```datom
+ Broadcast.Notice.«Search with knowledge:search»
+ Broadcast.[ 7 9 12 ]
```

+ ```mermaid
+ flowchart TB
+     m["Memory: each flow's state"] -- "Running or Idle" --> h["the hot flows"]
+     b["Broadcast.Request"] -- "one prompt into each" --> h
+     h -- "who received it" --> r["Broadcast.Vector of FlowId"]
+ ```
