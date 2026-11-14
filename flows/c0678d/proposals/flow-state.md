# The Nexus reads a flow from its transcript

Created by Fable 5.1, alone.

### Proposal 1: The Nexus reads a flow from its transcript · psyche-belief › vision/flow-nexus-v1.md

::: comment
In "The Nexus reads what a flow says", the first sentence is replaced and the rest stands; in "Memory", the Flow record gains the time its state began, and a delivered message its time.
:::

- Every harness event reaches the Flow Nexus through a hook calling the CLI: Report carries the flow's state, and a flow's finished response.
+ A flow is its session, and the Nexus reads it there: it watches the transcript the harness writes and reads each write as it lands, so a response, a tool call, idleness and the end are seen in the file itself, with no part played by the harness; Report, from a hook, carries only what the transcript shows nothing of, and a Working or Idle state is held with the time it began, read from the transcript and from the pane the herdr Nexus observes, so a flow idle for a day is a question the Nexus answers.

```mermaid
- flowchart TB
-     r["flow's response, as text"] -- "Report, from the hook" --> t["translator"]
-     t -- "actualizes as Input?" --> y["yes: the Input, as signal"]
-     t -- "no" --> n["Heard: kept, nothing acted"]
-     y --> f["Flow Nexus acts"]
```

```mermaid
+ flowchart TB
+     r["the transcript"] -- "each write, read as it lands" --> t["translator"]
+     h["a hook"] -- "Report: what the file lacks" --> t
+     p["the pane, from the herdr Nexus"] -- "Changed: Open, Busy, Idle, Dead" --> t
+     t -- "actualizes as Input?" --> y["yes: the Input, as signal"]
+     t -- "no" --> n["Heard: kept, nothing acted"]
+     y --> f["Flow Nexus acts"]
```

```ethos
  Flow.{ FlowId Address Pane
-        State.[ Running Idle Ended ]
-        Vector<Event> }
-  Queue.{ Address Vector<Message> }
+        State.[ Working Idle Ended ]
+        ; since the state began
+        Time
+        Vector<Event> }
+  ; when it was delivered
+  Delivery.{ Message Time }
+  Queue.{ Address Vector<Delivery> }
+  Time.String   ; UTC, ISO 8601
```
