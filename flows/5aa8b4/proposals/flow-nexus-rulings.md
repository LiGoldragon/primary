Presentation.{ «Flow Nexus rulings of 2026-11-05» }

# Flow Nexus rulings of 2026-11-05

Created by Fable, from his words of today: flows closed at idle and he could talk to nobody; the close-at-idle was a long-horizon thing; the default can never be hardwired into the runtime; a closed flow comes back as itself, not as a new one; and the Fable gate takes his spoken word through the machine, since he never operates the sockets himself.

### Proposal 1: Sleeping at idle is far vision · psyche-belief › vision/flow-nexus.md, and psyche-belief › vision/far/flow-nexus.md

**Comment** His word of 2026-11-05: closing a flow at idle was a long-horizon thing. The line leaves the perennial module for the far one, where a flow designing that horizon loads it; version 0 keeps every idle flow's harness.

::: move proposed
from: psyche-belief › vision/flow-nexus.md
to: psyche-belief › vision/far/flow-nexus.md

A permaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.
:::

#### psyche-belief › vision/flow-nexus.md

+ An idle flow keeps its harness, so that the living finds the flow he was talking to.

### Proposal 2: The continuity default is configured · psyche-belief › vision/flow-nexus-v1.md

**Comment** His word of 2026-11-05: "The default can never be hardwired into the runtime. We have to be able to set the default any way we want without rewriting the runtime." The Flow Nexus holds the default continuity as one meta value beside the default modules; a member whose definition names no continuity takes it.

  ## Default modules

- The Flow Nexus holds one configuration value, the default modules: the modules every flow gets.
+ The Flow Nexus holds two configuration values: the default modules, the modules every flow gets, and the default continuity, what a member whose definition names none does when its flow ends or idles.

```ethos
  Signal
  [ belief:[ ModuleName ]
    flow:[ Threshold Continuity ] ]
  [ Configure.Set ]                    ; inputs: one value at a time
  [ Configured.Set ]                   ; outputs: the value set
  [ Set.[ DefaultModules.Vector<ModuleName> ; types: the modules every flow gets
-         Threshold ] ]                ;   one model's context mark
+         Threshold                    ;   one model's context mark
+         DefaultContinuity.Continuity ] ] ; what a member names none of
```

```datom
+ Configure.DefaultContinuity.Permanent
+ Configured.DefaultContinuity.Permanent
```


### Proposal 3: The Fable gate takes his word through the machine · psyche-belief › vision/model-roles.md

**Comment** His word: "I never operate this kind of stuff ... I just talk to the machine, and the machine does the things." The gate stays; what it admits is his word, carried by the flow he talks to. Launch, Refresh and Resume pass one gate.

  ## A Fable flow starts on the living's word

- A Fable flow starts only on the living's own Say: the Flow Nexus refuses a launch or a refresh whose model is Fable unless the Say comes from the living himself. No brief, no flow and no refresh starts a Fable.
+ A Fable flow starts only on the living's word. A Launch, Refresh or Resume whose model is Fable is admitted when the caller, known by its process, is a flow the Nexus holds whose own model is Fable, the flow he talks to, and the request carries his words whole; the meta socket, the root, admits it as it admits everything. Any other caller is refused.

```ethos
- Refused.[ FableNeedsTheLiving.Address ]   ; a Launch or a refresh successor whose model is Fable, not said by the living
+ Living.{ Context.String Verbatim.String }   ; what his words were about, and his words whole
+ LaunchRequest.{ Address Remembering Brief.String Option<Living> }
+ RefreshRequest.{ Address Option<Living> }
+ ResumeRequest.{ FlowId Option<Living> }
+ Refused.[ FableNeedsTheLiving.Address ]   ; a Fable Launch, Refresh or Resume without his words from the flow he talks to
```

```datom
- Launch.{ { Psyche audit Fable } { Predecessors.0 [] } «Audit the next module» }   ; from a flow's process
- Refused.FableNeedsTheLiving.{ Psyche audit Fable }
+ Launch.{ { Psyche audit Fable } Predecessors.0 «Audit the next module» None }   ; from any flow: refused
+ Refused.FableNeedsTheLiving.{ Psyche audit Fable }
+ Launch.{ { Psyche audit Fable } Predecessors.0 «Audit the next module»
+          Some.{ «the audit» «Start a Fable on the audit, please» } }           ; from the Fable he talks to: admitted
+ Launched.9af746
```

### Proposal 4: A closed flow comes back as itself · psyche-belief › vision/flow-nexus-v1.md

**Comment** His word: "make sure you're not starting a new one." Launch starts a new flow; Resume brings back a flow the Nexus holds, from its own transcript, in a pane herdr starts under the flow's name. Memory records who started every flow.

  ## A permanent flow continues

+ A flow the Nexus holds, ended with its transcript kept, is brought back as itself by Resume: its harness is started again on its own transcript, in a pane under the flow's name, under its address; its context is intact, and the first turn pays a cold cache when the hour has passed. A wake starts a new flow; a Resume starts none.

```ethos
  [ Launch.{ MetaflowName FlowName Brief }
+   Resume.ResumeRequest               ; a held flow, back as itself
    Rehearse.{ MetaflowName FlowName Brief } ; a Launch as a dry run: nothing runs
```

```ethos
  [ Launched.FlowId
+   Resumed.FlowId
    Rehearsed.Command.String           ; the shell command, whole
```

```ethos
    Refused.[ UnknownMetaflow.MetaflowName
+             UnknownFlow.FlowId             ; no such flow held
+             Awake.FlowId                   ; already running
+             NoTranscript.FlowId            ; nothing to resume from
```

```ethos
  [ Definition.[ Metaflow Harness Complex ]
    DefaultModules.Vector<ModuleName>  ; the modules every flow gets
+   DefaultContinuity.Continuity       ; what a member names none of
    Flow.{ FlowId Address Pane
           State.[ Running Idle Ended ]
+          StartedBy.[ Living.FlowId   ; the flow that carried his words
+                      Flow.FlowId     ; any other flow
+                      Meta ]          ; the root socket
           Vector<Event> }
```

```datom
+ Resume.{ 087053 None }
+ Resumed.087053
```

A member whose definition names no continuity takes the configured default; a launch with neither is refused NotConfigured, and the definition is accepted, since configuration arrives one value at a time.

```ethos
    Member.{ FlowName HarnessName ModelName Effort
-            Continuity Workspace Beliefs Tools
+            Option<Continuity> Workspace Beliefs Tools
```
