Presentation.{ «Restart» Proposal }
# Restart

Created by Fable 5.1, who wrote this; Opus 5.5, Psyche restart Secondary, read it against its design and found it short in eight places, taken in.

### Proposal 1: Restart · psyche-belief › vision/flow-nexus.md

**Comment** The section "Restarting without waking" is replaced:

- ## Restarting without waking
-
- A flow can be restarted without being woken: its harness closes, its transcript stays, and its successor runs when a message wakes it. A flow can also restart itself. A restart meant to leave the flow asleep is done from outside; what arrives queues for its successor.
+ ## Restart
+
+ A restart closes a flow's harness and resumes the same native session: the transcript, the context and the flow id stay; only the process is new. A refresh is the other thing: a fresh flow, a handover. A restart is how a flow picks up what only a new process gets, hooks on a new socket, a changed launch, a new place, and how a flow is shut down without being woken.
+
+ ```mermaid
+ flowchart TB
+   f["a flow: one native session"]
+   s["a successor, fresh"]
+   r["the same flow, resumed"]
+   f -- "refresh: new session, handover" --> s
+   f -- "restart: same session, new process" --> r
+ ```
+
+ A restart is asked by the flow itself, or from outside by any caller the Nexus identifies; the Nexus owns it whole. It records the intent, locks the permaflow, closes the harness through the herdr Nexus at the flow's next Stop, since closing a turn kills it, resumes the session in a new pane whose environment is composed whole, and unlocks only at a verified bind: the same session and model, the new seat's own process identity, written with the unlock as one change. A late event of the old seat is fenced from then on. What arrives while the permaflow is locked queues and is delivered once, to the resumed seat. A flow asking from inside is answered RestartOwed at once and restarted at that turn's Stop, before any refresh or drain.
+
+ ```mermaid
+ flowchart TB
+   a["Restart.{ FlowId Waking }"]
+   l["permaflow locked"]
+   c["harness closed"]
+   p["new pane: harness resumes the session"]
+   u["bound and unlocked, one write;
+     the old seat fenced"]
+   r["the resumed seat"]
+   a -- "recorded in Memory" --> l
+   l -- "Close, through herdr" --> c
+   c -- "Resume, through herdr,
+     environment composed whole" --> p
+   p -- "verified bind: session, model,
+     the seat's own process" --> u
+   u -- "queue delivered once" --> r
+ ```
+
+ A restart names whether the flow is to wake: Woken resumes the harness now; Asleep closes it and records that the next waking message, an order, a question or the living's words, resumes it, a Soft message only queuing. A restart asked from inside is always Woken; Asleep may be asked of an awake flow.
+
+ ```mermaid
+ flowchart TB
+   k["Restart"]
+   w["harness resumed now; queue delivered"]
+   z["harness closed; session kept"]
+   k -- "Woken" --> w
+   k -- "Asleep" --> z
+   z -- "a waking message arrives" --> w
+ ```
+
+ Every case of a restart is proven by a test before it ships, and a case not proven is left out, since a restart is where a system turns half-broken. The cases, each one test named for it:
+
+ ```mermaid
+ flowchart TB
+   t["Restart"]
+   c1["the flow awake"]
+   c2["the flow asleep"]
+   c3["a message arriving mid-restart:
+     queued, delivered once"]
+   c4["the harness already dead: resume alone"]
+   c5["the resume failing: session, queue and
+     address kept, Failed answered,
+     retried or stopped by the owner"]
+   c10["the Nexus dying mid-restart: the phase
+     recorded, an unproven spawn Interrupted,
+     never respawned blindly"]
+   c11["an awake flow asked Asleep"]
+   c6["the resumed seat's hooks
+     reaching the live Nexus"]
+   c7["asked by the flow itself"]
+   c8["asked from outside"]
+   c9["asked Asleep"]
+   t --> c1
+   t --> c2
+   t --> c3
+   t --> c4
+   t --> c5
+   t --> c10
+   t --> c11
+   t --> c6
+   t --> c7
+   t --> c8
+   t --> c9
+ ```
+
+ At a cutover, a restart is the last step of the hand migration: the new Nexus adopts the running session under its address, then restarts it, so the resumed seat's hooks report to the new Nexus and nothing of the session is lost.
+
+ ```mermaid
+ flowchart LR
+   o["old Nexus, stopped"]
+   h["the native session"]
+   n["new Nexus"]
+   o -. "session kept in the harness" .-> h
+   n -- "Adopt.{ Address Session }" --> h
+   n -- "Restart, Woken" --> h
+   h -- "hooks report" --> n
+ ```
+
+ ```ethos
+ Signal
+ [ flow:[ FlowId ] ]
+ ; input: the flow, and whether it is to wake
+ [ Restart.{ FlowId Waking } ]
+ ; outputs: the same flow id, resumed
+ [ Restarted.FlowId
+   ; asked from inside: done at this turn's Stop
+   RestartOwed.FlowId
+   Refused.[ Unknown.FlowId
+             ; a restart or refresh already
+             ; under way
+             Busy.FlowId
+             ; nothing to resume
+             NoHeldSession.FlowId
+             ; herdr did not close it; retried,
+             ; never skipped
+             CloseRefused.FlowId
+             ; a spawn whose outcome is unproven
+             Interrupted.FlowId
+             ; session, queue and address kept;
+             ; retry or Stop
+             ResumeFailed.FlowId
+             ; a case not yet proven
+             Unsupported.FlowId ] ]
+ [ Waking.[ Woken Asleep ] ]
+ ```
+
+ ```ethos
+ Memory
+ [ flow:[ FlowId Address Waking ] ]
+ ; the intent, recorded before anything closes
+ [ Restart.{ FlowId Address Waking
+             ; recorded before each step, so a
+             ; Nexus death is read back
+             Phase.[ Opening Closing Spawning Bound
+                     Failed Interrupted ] } ]
+ ```
+
+ ```datom
+ Restart.{ 2632 Woken }
+ Restarted.2632
+ ; closed; the next message resumes it
+ Restart.{ 2632 Asleep }
+ ; asked from inside; done at this Stop
+ RestartOwed.2632
+ ; the harness did not come back;
+ ; session and queue kept
+ Refused.ResumeFailed.2632
+ ```

### Proposal 2: Restart · psyche-belief › vision/proposal.md

**Comment** The line "A proposal is usually drawn as well as written, and always when it has a shape; …" is replaced:

- A proposal is usually drawn as well as written, and always when it has a shape; a figure draws what is wanted, and nothing of what goes.
+ A proposal is drawn as much as it is written: one figure per mechanism, per sequence and per set of cases, so that he reads the shape before the words; a figure draws what is wanted, and nothing of what goes.
