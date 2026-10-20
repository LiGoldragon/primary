<!-- to-the-living:start -->
Presentation.{ «The Flow Nexus, whole: long term, then short term, 2nd edition» }

# The Flow Nexus, whole: long term, then short term

Flow is the Nexus that starts, wakes and refreshes flows, and its ethos is the current best example of ethos. You ruled what Flow is for and the paragraph that opens its ethos; this edition re-proposes the new-topic sentence smaller, and carries the rest of the ethos and the vision lines still open. The body the Flow ethos lines add to is proposed in «Flow: context modules and the prompt».

## Proposal 1: psyche-context › skills/vision-flow.md

+ A new topic starts a new flow.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

- A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+ A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket.
+ A launch names the metaflow and a brief of a small paragraph; the context modules composed into its prompts are the metaflow's, set in its configuration.
+ The Nexus composes the prompt from its module registry, checking each module's hash against its source.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-flow.md

+ Every harness hook is one standard call to Flow, carrying the hook's data and where it came from.
+ Flow decides from its memory where that notification goes and of what kind.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-flow.md

+ ## Short term: the Flow tool, derived from its ethos
+ The short-term Flow tool is derived from the Flow ethos: each ethos part becomes a Clojure namespace holding Malli schemas of the same names.
+ A signal is an EDN form its schema checks, and a record is an EDN map in the tool's own store.
+ A namespace that runs takes one EDN payload.

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › vision/flow-ethos.md, a new file

+ ---
+ description: The Flow Nexus in ethos, the current best example of ethos; its types, traits and layout are read or judged.
+ dependencies: [vision-ethos, vision-flow, vision-nexus]
+ ---
+ ```ethos
+ Priority.[ HardAbrupt.Request   ; a head on
+            MiddleAbrupt.Request ; the
+            Soft.Request ]       ; request
+ Brief.String
+ Module.{ Key             ; a context module
+          Prompt.[ System ; and its prompt
+                   First ] }
+ Binding.{ Address        ; binds its modules
+           Vector<Module> }
+ Entry.{ Key              ; a registered
+         Source }         ; module
+ LayerModel.{ Aspect      ; a layer's model
+              Layer
+              ModelName }
+ Configuration.[ Entry    ; set on the meta
+                          ; socket
+                 LayerModel
+                 Binding ]
+ Event.[ Began            ; from the hooks
+         Prompted         ; request entered
+         Working
+         Idle
+         Tokens           ; context size
+         HandedOver
+         Stopped ]
+ Tokens.Integer
+ Hook.{ Event             ; a harness hook
+        Data.String }     ; and what it carries
+ Origin.FlowId            ; where it came from
+ Kind.[ Notice            ; what a notification
+        Order             ; is: told, ordered
+        Result ]          ; or answered
+ ```

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › vision/flow-ethos.md, a new file

+ ```ethos
+ Signal                  ; ordinary socket
+ [ flow:[ FlowId         ; imports
+          Address
+          Key
+          Brief
+          Path
+          Priority
+          Event
+          Hook
+          Origin ] ]
+ [ Launch.{ Address      ; queries
+            Brief
+            Vector<Path> } ; training files
+   Send.{ Address        ; wakes if needed
+          Priority }     ; the headed request
+   Refresh.Address
+   Stop.Address
+   Report.{ Hook         ; one standard call
+            Origin }     ; per hook
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
+             ChangedModule.Key ] ]
+ []                      ; types
+
+ Signal                 ; the meta socket
+ [ flow:Configuration ] ; imports
+ [ Configure.Configuration ] ; queries
+ [ Configured           ; responses
+   Refused.[ StoreRefused ] ]
+ []                     ; types
+ ```

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › vision/flow-ethos.md, a new file

+ ```ethos
+ Operation               ; one per effect
+ [ flow:[ FlowId         ; imports
+          Address
+          Key
+          Brief
+          Path
+          Priority
+          Request
+          Event
+          Configuration
+          Hook
+          Origin
+          Kind ] ]
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
+   Store.Configuration
+   Route.{ Hook          ; reads Routing
+           Origin } ]
+ [ Composed.Prompts      ; outcomes
+   FlowStarted.FlowId
+   Delivered
+   Enqueued
+   Locked
+   Released
+   Recorded
+   Ended
+   Stored
+   Routed.{ Address      ; where it goes
+            Kind }       ; and of what kind
+   Failed.[ ChangedModule.Key ; hash differs
+            CapsuleRefused
+            StoreRefused ] ]
+ [ Capsule.{ CapsuleHome.String ; types
+             Login.Vector<String> }
+   Prompts.{ SystemPrompt.String ; composed
+             FirstPrompt.String } ]
+ ```

Ruling: land, amend, or reject.

## Proposal 8: psyche-context › vision/flow-ethos.md, a new file

+ ```ethos
+ Memory          ; what Flow keeps
+ [ flow:[ FlowId ; imports
+          Address
+          Metaflow
+          Event
+          Entry
+          LayerModel
+          Binding
+          Hook
+          Origin
+          Kind ] ]
+ [ Metaflow      ; record types
+   Flow.{ FlowId ; one run of it
+          Address
+          Vector<Event> }
+   Entry         ; module registry
+   LayerModel    ; model of a layer
+   Binding       ; modules of one
+   Routing.{ Hook   ; keyed by hook
+             Origin ; and origin
+             Address
+             Kind } ]
+ [ Succeeded ]   ; its answer
+ []              ; types
+ ```

Ruling: land, amend, or reject.

## Proposal 9: psyche-context › skills/vision-nexus.md

+ The Flow Nexus's ethos stands whole in the flow-ethos module; one Launch goes along the path:
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
- ```
- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
- Succeeded                                             ; 4 Memory's answer to Operation
- Started.7                                             ; 5 Outcome
- Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
- ```
+ ```
+ Launch.{ { Psyche nexus Primary } ; 1 Query,
+          «Draft the Nexus book»   ;   typed at
+          [] }                     ;   the CLI
+ Compose.{ { Psyche nexus Primary } «…» [] } ; 2
+ StartFlow.{ { Psyche nexus Primary } ; 3 from
+             { «…» [] }               ;   Signal's
+             { «…» «…» } }            ;   intend
+ Metaflow.{ { Psyche nexus Primary } ; 4 the
+            Awake.quietRiverStone    ;   Change
+            []                       ;   Operation
+            [] }                     ;   hands Memory
+ Succeeded                   ; 5 Memory's answer
+ FlowStarted.quietRiverStone ; 6 Outcome
+ Launched.quietRiverStone    ; 7 Response
+ ```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
