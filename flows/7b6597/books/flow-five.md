<!-- to-the-living:start -->
Presentation.{ «Five Flow proposals» }

# Five Flow proposals

### Proposal 1: The sender is in the message type · psyche-context › vision/flow.md

**Comment** Every message a flow receives from the Nexus is one datom whose type carries the sender, so a message is told from the living's words by its shape, never by a signature its sender writes. His words are the only text that is not datom; the tool that searches transcripts for them follows from this.

  Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Message is the send path: a flow asks Message to send, Message asks Flow to deliver and subscribes to Flow's events, and a flow no longer calls Flow raw to send.
  
+ Everything that leaves the Nexus for a flow is one datom of a Signal type, the sender in the type: a message is a Letter of its kind, its sender and its body, the sender the address and flow id Flow resolved from the calling process, never a line the sender wrote. The living's words are the only text in a transcript that is not datom, so his messages are told from every other by their shape, and a tool finds them in any transcript by that mark.
+
+ ```
+ +----------------------------------+
+ | a flow                           |
+ +----------------------------------+
+        | calls Send
+        v
+ +----------------------------------+
+ | Flow                             |
+ +----------------------------------+
+        | resolves the sender from
+        | the calling process, types
+        v
+ +----------------------------------+
+ | Letter.{ Kind Sender Body }      |
+ +----------------------------------+
+        | is typed, as datom, into
+        v
+ +----------------------------------+
+ | the recipient's transcript       |
+ +----------------------------------+
+        | holds beside it
+        v
+ +----------------------------------+
+ | the living's words: the only     |
+ | text that is not datom           |
+ +----------------------------------+
+ ```
+
  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.

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

### Proposal 2: Only a Secondary reaches its Primary · psyche-context › vision/flow.md

**Comment** The rebuilt Flow dropped the rule that a Primary is reached only by its Secondary, and a Field Secondary's five reports were typed straight into the Psyche core Primary's pane. The route rule returns to Flow, which holds the routes: a send to a Primary from any flow but its own Secondary is refused, and the sender is told where the message goes instead.

  Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Message is the send path: a flow asks Message to send, Message asks Flow to deliver and subscribes to Flow's events, and a flow no longer calls Flow raw to send.
  
+ A Primary is reached only by its own Secondary. Flow refuses a Send addressed to a Primary from any other flow, naming the Secondary it goes to instead; it never queues it for the Primary and never types it into his pane.
+
+ ```
+ +------------------------------+
+ | any flow but the Secondary   |
+ +------------------------------+
+        | sends to the Primary
+        v
+ +------------------------------+
+ | Flow                         |
+ +------------------------------+
+        | refuses, naming
+        v
+ +------------------------------+
+ | the Primary's Secondary      |
+ +------------------------------+
+        | alone sends to
+        v
+ +------------------------------+
+ | the Primary                  |
+ +------------------------------+
+ ```
+
  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.

```datom
Refused.OffRoute.{ Psyche core Secondary }
```

### Proposal 3: A closed flow's Codex thread is closed with it · psyche-context › vision/flow.md

**Comment** His theory: Codex threads keep running on the app-server after their pane is gone, eating RAM and the thread cap. Whether that is so is being checked by Mind; the line below is what Flow does so that it cannot be so, and it stands whatever the check finds, since a thread nothing addresses has no reason to live.

  ## A superseded flow is closed
  
  An abandoned, duplicated or superseded flow is closed, archived and deregistered, and never messaged or woken.
+ When Flow closes a flow, it closes the flow's native thread with it: a Codex thread is ended on the app-server in the same event, so no thread outlives the flow it ran, and the cap on threads and the memory they hold count only live flows.
+
+ ```
+ +------------------------------+
+ | Flow                         |
+ +------------------------------+
+        | closes
+        v
+ +------------------------------+
+ | a flow                       |
+ +------------------------------+
+        | ends, in the same event
+        v
+ +------------------------------+
+ | its Codex thread on the      |
+ | app-server                   |
+ +------------------------------+
+        | frees
+        v
+ +------------------------------+
+ | the thread cap and its RAM   |
+ +------------------------------+
+ ```

### Proposal 4: The harness-blacklisted module · psyche-context › vision/flow.md

**Comment** Claude Code in bypass-permissions mode puts into every flow's base context the line «Do your work through the Bash tool wherever it can accomplish the job…», which sent a Primary to the shell. A harness line Flow cannot delete it can cancel: a harness-blacklisted module, one per harness version, names the lines the harness adds that are not ours, and is composed into every flow of that harness so the next flow starts without them.

  ## Repository and belief modules
  
  The flow repository holds the machinery of the Flow Nexus and is a runtime repository.
  Every belief module lives outside it, the basic modules included, so that a change to a module causes no Nix rebuild.
  The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
+ A harness-blacklisted module, one per harness version, names the lines that harness puts into a flow's base context which are not ours, the shell-preference line of Claude Code's bypass mode among them, and says each is void; Flow composes it into every flow of that harness, so a blacklisted line never reaches a flow unanswered, and the next flow after the line is blacklisted starts free of it.

### Proposal 5: A reminder is a Flow operation · psyche-context › vision/flow.md

**Comment** A flow that must check back after a time scheduled its own wake with a harness tool or an ad hoc script. Flow already sends messages, so the reminder is its operation: a flow asks Flow to send it a Notice at a time, and the wake comes as every other message does. This is for the next wave, after what is slated.

  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.
+ A flow that must look again after a time asks Flow for a reminder: a Notice to its own address, delivered at the time it names, waking it if it sleeps. A reminder is a message like any other, queued and witnessed as one; no flow keeps a timer, a script or a harness schedule of its own.

```ethos
Signal
[ :flow:[ Address Instant ] ]                 ; imports
[ Remind.{ Instant String } ]                 ; queries: when, and the notice to deliver
[ Reminded.{ Address Instant } ]              ; responses
[]                                            ; types
```

```datom
Remind.{ 2026-10-28T06:40:00Z
         «Check that Mind deployed the Flow tip.» }
```
<!-- to-the-living:end -->
