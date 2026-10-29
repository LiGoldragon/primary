Presentation.{ «Flow» }

# Flow

Designed by Fable 5.1, inventory by Opus 5.5, extraction by Sonnet 5.5; split by 554e1a.

Superseded: every proposal here is carried in Flow, whole, by the Psyche flow Primary; read that one.

### Proposal 1: the sender is in the message type · psyche-context › vision/flow.md

**Comment** Your line "we should know who messaged you without Flow ID", and "every message injected into a pane is datom". Flow 0.40.6 implements it; it does not yet compile.

  Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it.
+ Everything that leaves the Nexus for a flow is one datom of a Signal type, the sender in the type: a message is a Letter of its kind, its sender and its body, the sender the address Flow resolved from the calling process, never a line the sender wrote; in the pane the sender reads as its address. The living's words are the only text in a transcript that is not datom, so his messages are told from every other by their shape, and a tool finds them in any transcript by that mark, so that nothing he says is lost when a flow refreshes before logging it.

```ethos
Signal
[ :flow:[ Address FlowId ] ]            ; imports
[ Send.{ Address Delivery Message } ]   ; queries
[ Letter.{ Kind                         ; responses: what a flow receives
           Sender
           Body } ]
[ Kind.[ Order                          ; types
         Question
         Result
         Notice
         Psyche ]
  Sender.{ Address FlowId }
  Body.String ]
```

```datom
Letter.{ Order
         { { Psyche core Secondary } e591ed }
         «Review the source packet.» }
```

### Proposal 2: the sender is an address · psyche-context › vision/flow.md

**Comment** Amends proposal 1 of Flow, whose type still carries a Flow ID where you said "without Flow ID".

- Sender.{ Address FlowId }
+ Sender.Address

```datom
Letter.{ Order
         { Psyche core Secondary }
         «Review the source packet.» }
```

### Proposal 3: Flow gives a flow its id · psyche-context › vision/flow.md

**Comment** Your word of today: no flow spends its energy binding itself.

  Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds.
+ A flow is given its id by Flow at launch, in its prompt, and binds nothing itself; a flow that must bind itself is a flow Flow failed to launch.

### Proposal 4: only a Secondary reaches its Primary · psyche-context › vision/flow.md

+ A Primary is reached only by its own Secondary. Flow refuses a Send addressed to a Primary from any other flow, naming the Secondary it goes to instead; it never queues it for the Primary and never types it into his pane.

```datom
Refused.OffRoute.{ Psyche core Secondary }
```

### Proposal 5: a closed flow's Codex thread is closed with it · psyche-context › vision/flow.md

  An abandoned, duplicated or superseded flow is closed, archived and deregistered, and never messaged or woken.
+ When Flow closes a flow, it closes the flow's native thread with it: a Codex thread is ended on the app-server in the same event, so no thread outlives the flow it ran.

### Proposal 6: a reminder is a Flow operation · psyche-context › vision/flow.md

  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.
+ A flow that must look again after a time asks Flow for a reminder: a Notice to its own address, delivered at the time it names, waking it if it sleeps. A reminder is a message like any other, queued and witnessed as one; no flow keeps a timer, a script or a harness schedule of its own.

```ethos
Signal
[ :flow:[ Address Instant ] ]                 ; imports
[ Remind.{ Instant String } ]                 ; queries: when, and the notice to deliver
[ Reminded.{ Address Instant } ]              ; responses
[]                                            ; types
```

### Proposal 7: a fresh flow receives what is open · psyche-context › vision/remembering.md

**Comment** Your words of today: the next flow starts whole; short term the review is standard; long term the system passes the right modules at every refresh.

  A fresh flow receives the living's content weighed by importance, and only the important part.
+ A remembering of Open gives a fresh flow the open records of its address. The Flow Nexus knows which flows held the address, so the flow searches nothing. Open carries a cap on content; the remembering fills toward the cap and stops one file short of it.
+
+ A fresh Primary begins with a review of what its predecessors were told and what of it is still owed, and the review's result enters its middle stratum. In the long term, the Flow Nexus passes a flow every module and record it needs at launch and at every refresh, and the review is removed.

```ethos
  RememberingDepth.Integer
+ ContentCap.Integer
- Remembering.[ Predecessors.RememberingDepth Custom.Vector<FlowId> ]
+ Remembering.[ Open.ContentCap
+               Predecessors.RememberingDepth
+               Custom.Vector<FlowId> ]
  Launch.{ Address Remembering InstructionPrompt }
```

### Proposal 8: his words without a line

**Comment** One thing you said that I have no line for; it is a question, intelligible on its own.

+ "I don't have time to keep up with the speed at which everything is scrolling by." Is the pane to carry only what you read, every machine message to a flow going to its transcript and not to the pane you watch?
