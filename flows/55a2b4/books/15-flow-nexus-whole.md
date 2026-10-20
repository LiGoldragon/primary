<!-- to-the-living:start -->
Presentation.{ «The Flow Nexus, whole: long term, then short term» }

# The Flow Nexus, whole: long term, then short term

## Long term and universal

### Proposal 1: what Flow is for

File: `psyche-context/skills/vision-flow.md` («What it does», after its second paragraph)

```text
  Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.
+
+ Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A new topic on the costliest model is started freely, and a flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.
```

### Proposal 2: the Flow Nexus in ethos

File: `psyche-context/vision/flow-ethos.md` (builds on «Flow: context modules and the prompt», batch 06, Proposal 8, unruled: its module, its name and its body, Mind's `library.ethos`; the lines here add to them)

```text
  ---
  description: The Flow Nexus in ethos, the current best example of ethos; its types, traits and layout are read or judged.
- dependencies: [vision-ethos, vision-flow]
+ dependencies: [vision-ethos, vision-flow, vision-nexus]
  ---
+
+ ## The Flow Nexus in ethos
+
+ The Flow Nexus is specified whole in ethos: a Library its parts share, a Signal for each of its two sockets, an Operation and a Memory.
```

In the body's Library, after its Metaflow:

```ethos
    Said.{ Context.String Verbatim.String }
    Request.[ Order.String
              Question.String
              Psyche.Said
              Psyches.Vector<Said>
              Result.String
              Notice.String ]
    Aspect.[ Psyche Mind Field ]
    Address.{ Aspect Topic Layer }
    Recipient.[ Address Up ]
    Metaflow.{ Address
               State.[ Awake.FlowId Asleep Ended ]
               Past.Vector<FlowId>
               Queue.Vector<Request> }
+   Priority.[ HardAbrupt.Request   ; a head on
+              MiddleAbrupt.Request ; the
+              Soft.Request ]       ; request
+   Brief.String
+   Module.{ Key             ; a context module
+            Prompt.[ System ; and its prompt
+                     First ] }
+   Binding.{ Address        ; binds its modules
+             Vector<Module> }
+   Entry.{ Key              ; a registered
+           Source }         ; module
+   LayerModel.{ Aspect      ; a layer's model
+                Layer
+                ModelName }
+   Configuration.[ Entry    ; set on the meta
+                            ; socket
+                   LayerModel
+                   Binding ]
+   Event.[ Began            ; from the hooks
+           Prompted         ; request entered
+           Working
+           Idle
+           Tokens           ; context size
+           HandedOver
+           Stopped ]
+   Tokens.Integer
    Lock.{ Sender Address Until.Integer }
```

At the end of the body, each root with the file it lands in:

```ethos
  []
  []
+
+ ; signal-flow, ethos/signal.ethos
+ Signal                  ; ordinary socket
+ [ flow:[ FlowId         ; imports
+          Address
+          Key
+          Brief
+          Path
+          Priority
+          Event ] ]
+ [ Launch.{ Address      ; queries
+            Brief
+            Vector<Path> } ; training files
+   Send.{ Address        ; wakes if needed
+          Priority }     ; the headed request
+   Refresh.Address
+   Stop.Address
+   Report.Event          ; caller: its process
+   Subscribe.Address ]
+ [ Launched.FlowId       ; responses
+   Sent
+   Queued                ; for the next flow
+   Refreshed
+   Stopped
+   Reported
+   Subscribed
+   Observed.{ Address    ; an event seen
+              Event }
+   Refused.[ OffRoute    ; off the routes
+             NoSecondary ; short term
+             NoCapsule
+             Busy.FlowId ; already awake
+             ChangedModule.Key ] ]
+ []                      ; types
+
+ ; meta-signal-flow, ethos/signal.ethos
+ Signal                 ; the meta socket
+ [ flow:Configuration ] ; imports
+ [ Configure.Configuration ] ; queries
+ [ Configured           ; responses
+   Refused.[ StoreRefused ] ]
+ []                     ; types
+
+ ; flow-ethos crate: operation.ethos
+ Operation               ; one per effect
+ [ flow:[ FlowId         ; imports
+          Address
+          Key
+          Brief
+          Path
+          Priority
+          Request
+          Event
+          Configuration ] ]
+ [ Compose.{ Address     ; reads its Binding
+             Brief
+             Vector<Path> }
+   StartFlow.{ Address   ; starts a harness
+               Capsule
+               Prompts }
+   Deliver.{ FlowId      ; into its context
+             Priority }
+   Enqueue.{ Address     ; onto its queue
+             Request }
+   LockMetaflow.Address
+   ReleaseMetaflow.Address
+   Record.{ FlowId       ; an event
+            Event }
+   End.FlowId            ; stopped or reaped
+   Store.Configuration ]
+ [ Composed.Prompts      ; outcomes
+   FlowStarted.FlowId
+   Delivered
+   Enqueued
+   Locked
+   Released
+   Recorded
+   Ended
+   Stored
+   Failed.[ ChangedModule.Key ; hash differs
+            Busy.FlowId       ; awake
+            CapsuleRefused
+            StoreRefused ] ]
+ [ Capsule.{ CapsuleHome.String ; types
+             Login.Vector<String> }
+   Prompts.{ SystemPrompt.String ; composed
+             FirstPrompt.String } ]
+
+ ; flow-ethos crate: memory.ethos
+ Memory          ; what Flow keeps
+ [ flow:[ FlowId ; imports
+          Address
+          Metaflow
+          Event
+          Entry
+          LayerModel
+          Binding ] ]
+ [ Metaflow      ; record types
+   Flow.{ FlowId ; one run of it
+          Address
+          Vector<Event> }
+   Entry         ; module registry
+   LayerModel    ; model of a layer
+   Binding ]     ; modules of one
+ [ Succeeded ]    ; its answer
+ []              ; types
```

Machine: the Working event, the meta socket's Refused, the names Binding, Entry, NoSecondary, Busy, Began, StartFlow, FlowStarted, LockMetaflow, ReleaseMetaflow and CapsuleHome, Prompt's name First for the user prompt, Priority as an enum whose heads carry the Request, and the files operation.ethos and memory.ethos.

File: `psyche-context/skills/vision-flow.md` (L34: a launch names no modules; the metaflow's configuration binds them)

```text
- A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+ A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow and a brief of a small paragraph; the context modules composed into its prompts are the metaflow's, set in its configuration; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
```

File: `psyche-context/skills/vision-nexus.md` (L148–197: the Flow example struck, so the Flow ethos stands once, in flow-ethos; the path's trace aligned to it)

```text
  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
+
+ The Flow Nexus's ethos stands whole in the flow-ethos module; one Launch goes along the path:
```

```ethos
- ```
- Library                                  ; what the three parts share
- []                                       ; imports: none
- [ FlowId.Integer                         ; types
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
-   Aspect.[ Psyche Mind Field ]
-   Layer.[ Primary Secondary Tertiary Quaternary ]
-   Event.[ Started Stopped ] ]
- []                                       ; kinds
- []                                       ; associations
-
- Signal                                   ; what Flow says, on its ordinary socket
- [ flow:[ FlowId Voice Event ] ]          ; imports from the Library
- [ Launch.{ Voice                         ; queries
-            Brief.String }
-   Report.{ FlowId Event } ]
- [ Launched.FlowId                        ; responses
-   Refused.[ NoCapsule
-             VoiceBusy.Voice ]
-   Reported ]
- []                                       ; types
-
- Operation                                ; what Flow does: one operation for every effect
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Start.{ Voice Capsule }                ; operations
-   Record.{ FlowId Event } ]
- [ Started.FlowId                         ; outcomes
-   Recorded
-   Failed.[ CapsuleRefused StoreRefused ] ]
- [ Capsule.{ Home.String                  ; types
-             Login.Vector<String> } ]
-
- Memory                                   ; what Flow remembers
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Flow.{ FlowId                          ; record types
-          Voice
-          State.[ Running Ended ]
-          Vector<Event> } ]
- ```
-
```

```datom
- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
- Succeeded                                             ; 4 Memory's answer to Operation
- Started.7                                             ; 5 Outcome
- Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
```

```datom
+ Launch.{ { Psyche nexus Primary } ; 1 Query,
+          «Draft the Nexus book»   ;   typed at
+          [] }                     ;   the CLI
+ Compose.{ { Psyche nexus Primary } «…» [] } ; 2
+ StartFlow.{ { Psyche nexus Primary } ; 3 from
+             { /home/li/primary [] }  ;   Signal's
+             { «…» «…» } }            ;   intend
+ Metaflow.{ { Psyche nexus Primary } ; 4 the Change
+            Awake.7f3a2c             ;   Operation
+            []                       ;   hands
+            [] }                     ;   Memory
+ Succeeded            ; 5 Memory's answer
+ FlowStarted.7f3a2c   ; 6 Outcome
+ Launched.7f3a2c      ; 7 Response, to the CLI
```

Machine: the sentence, and the trace's values.

```figure
┌──────────────┐
│ the CLI      │
└──────┬───────┘
       │ sends Launch
       ▼
┌──────────────┐ refuses OffRoute
│ Signal       ├─────────────────────────┐
└──────┬───────┘ or NoSecondary          │
       │ intends Compose                 │
       ▼                                 │
┌──────────────┐ reads the  ┌────────┐   │
│ Operation    ├───────────▶│ Memory │   │
└──┬────────┬──┘ Metaflow in└────────┘   │
   │ Asleep:│ refuses Busy if            │
   │ starts │ Awake, ChangedModule       │
   │        │ if a hash differs          │
   ▼        ▼                            ▼
┌───────┐ ┌────────────────────────────────┐
│ a new │ │ Refused, answered to the CLI   │
│ flow  │ └────────────────────────────────┘
└───────┘
```

```figure
             ┌──────────────────┐
             │ Asleep           │◀──────┐
             └────────┬─────────┘       │
                      │ is woken        │ is
                      │ with its        │ stopped,
                      │ queue           │ goes
                      ▼                 │
             ┌──────────────────┐       │
  ┌─────────▶│ Awake            ├───────┘
  │          └────────┬─────────┘
  │ takes             │ passes the
  │ the queue,        │ layer's threshold,
  │ is now            │ is locked, starts
  │                   ▼
  │          ┌──────────────────┐
  └──────────┤ the successor    │
             └──────────────────┘
```

1. The topic a core:Name, as vision-flow has it, in place of the body's String:

```ethos
-   Topic.String
+   Topic.core:Name
```

2. Three modules now: flow-ethos keeps the Library and the Operation, signal-ethos takes the two Signals, memory-ethos the Memory; each root moves whole, its first two lines standing for it.

File: `psyche-context/vision/flow-ethos.md`

```ethos
- ; signal-flow, ethos/signal.ethos
- Signal                  ; ordinary socket
- ; meta-signal-flow, ethos/signal.ethos
- Signal                 ; the meta socket
- ; flow-ethos crate: memory.ethos
- Memory          ; what Flow keeps
```

File: `psyche-context/vision/signal-ethos.md` (a new module)

```text
+ ---
+ description: The Flow Nexus's two Signals in ethos are read or judged.
+ dependencies: [flow-ethos]
+ ---
```

```ethos
+ ; signal-flow, ethos/signal.ethos
+ Signal                  ; ordinary socket
+ ; meta-signal-flow, ethos/signal.ethos
+ Signal                 ; the meta socket
```

File: `psyche-context/vision/memory-ethos.md` (a new module)

```text
+ ---
+ description: The Flow Nexus's Memory in ethos is read or judged.
+ dependencies: [flow-ethos]
+ ---
```

```ethos
+ ; flow-ethos crate: memory.ethos
+ Memory          ; what Flow keeps
```

3. Launch of an awake metaflow is not refused, so Busy goes; figure 1's Busy fork goes with it:

```ethos
-             Busy.FlowId ; already awake
-            Busy.FlowId       ; awake
```

Machine: the two descriptions.

## Short term, derived from the ethos

### Proposal 3: the short-term tool is derived from the ethos

File: `psyche-context/skills/vision-flow.md` (a new section after «Short term: the configuration of starting flows»; builds on «Short-term prototypes: Clojure now?» Proposals 1 and 2)

```text
+ ## Short term: the Flow tool, derived from its ethos
+
+ The short-term Flow tool is derived from the Flow ethos: each ethos part becomes a Clojure namespace holding Malli schemas of the same names; a signal is an EDN form its schema checks, and a record is an EDN map in the tool's own store. A namespace that runs takes one EDN payload.
```

Machine: the namespace per part, and the last sentence.

```figure
        ┌───────────────────────────┐
        │ an ethos part: Library,   │
        │ Signal, Operation, Memory │
        └─────────────┬─────────────┘
                      │ is derived into
                      ▼
        ┌───────────────────────────┐
        │ a Clojure namespace       │
        └──────┬─────────────┬──────┘
         holds │       takes │
               ▼             ▼
   ┌───────────────┐ ┌─────────────────┐
   │ Malli schemas │ │ one EDN payload │
   │ of the same   │ └─────────────────┘
   │ names         │
   └──┬─────────┬──┘
 check│    check│
      ▼         ▼
┌──────────┐ ┌──────────────┐
│ a signal:│ │ a record: an │
│ EDN form │ │ EDN map in   │
└──────────┘ │ the store    │
             └──────────────┘
```

### Proposal 4: the Launch signal and the State variant, derived

Lands once Mind's Ethos-to-Clojure-and-EDN module is written.

File: `src/flow/signal.clj` (the Flow tool's repository; provisional machine pattern, every signal)

```clojure
+ (ns flow.signal
+   (:require [flow.library :as l]))
+
+ ;; Launch in EDN; the modules come from
+ ;; the metaflow's configuration:
+ ;; {:address {:aspect :Psyche
+ ;;            :topic "flow"
+ ;;            :layer :Primary}
+ ;;  :brief "Draft the Flow tool."
+ ;;  :path-vector ["<a training file>"]}
+
+ (def Launch
+   [:map
+    [:address l/Address]
+    [:brief l/Brief]
+    [:path-vector [:vector l/Path]]])
```

File: `src/flow/library.clj` (beside it; provisional machine pattern, every variant)

```clojure
+ (ns flow.library)
+
+ (def FlowId :string)
+
+ (def State
+   [:or [:= :Asleep]
+        [:= :Ended]
+        [:map [:Awake FlowId]]])
```

## The hooks

### Proposal 5: Flow decides where the hooks talk

File: `psyche-context/skills/vision-flow.md` (after L60)

```text
  Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.
+
+ Every harness hook is one standard call to Flow, carrying the hook's data and where it came from; Flow decides from its memory where that notification goes and of what kind.
```

File: `psyche-context/vision/flow-ethos.md` (Proposal 2's lines)

In the body's Library, after Proposal 2's Tokens:

```ethos
    Tokens.Integer
+   Hook.{ Event          ; a harness hook
+          Data.String }  ; and what it carries
+   Origin.FlowId         ; where it came from
+   Kind.[ Notice         ; what a notification
+          Order          ; is: told, ordered
+          Result ]       ; or answered
```

In the ordinary Signal:

```ethos
  ; signal-flow, ethos/signal.ethos
  Signal                  ; ordinary socket
-          Event ] ]
+          Event
+          Hook
+          Origin ] ]
-   Report.Event          ; caller: its process
+   Report.{ Hook         ; one standard call
+            Origin }     ; per hook
```

In the Operation:

```ethos
  ; flow-ethos crate: operation.ethos
  Operation               ; one per effect
-          Configuration ] ]
+          Configuration
+          Hook
+          Origin
+          Kind ] ]
-   Store.Configuration ]
+   Store.Configuration
+   Route.{ Hook          ; reads Routing
+           Origin } ]
    Stored
+   Routed.{ Address      ; where it goes
+            Kind }       ; and of what kind
```

In the Memory:

```ethos
  Memory          ; what Flow keeps
  [ flow:[ FlowId ; imports
           Address
           Metaflow
           Event
           Entry
           LayerModel
-          Binding ] ]
+          Binding
+          Hook
+          Origin
+          Kind ] ]
  [ Metaflow      ; record types
    Flow.{ FlowId ; one run of it
           Address
           Vector<Event> }
    Entry         ; module registry
    LayerModel    ; model of a layer
-   Binding ]     ; modules of one
+   Binding       ; modules of one
+   Routing.{ Hook   ; keyed by hook
+             Origin ; and origin
+             Address
+             Kind } ]
```

Machine: the names Hook, Data, Origin, Kind, Notice, Order, Result, Routing, Route and Routed, the shapes of Hook, Origin, Kind and Routing, and the comments.
<!-- to-the-living:end -->
