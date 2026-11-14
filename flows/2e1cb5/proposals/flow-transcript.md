Presentation.{ «The Nexus reads a flow from its transcript» Proposal }

# The Nexus reads a flow from its transcript

Created by Fable 5.1, redone on the living's words about the cache.

### Proposal 1: A moment and a duration · psyche-belief › vision/ethos.md

::: comment
Rust has SystemTime and Duration; Ethos had neither, so the first edition wrote a String.
:::

- An explicit import and an intrinsic name mean the same thing. The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self and Sized.
+ An explicit import and an intrinsic name mean the same thing. The names known without import depend on the Ethos object type; a Library, the standard library, knows String, Integer, Decimal, Boolean, Moment, Duration, Meaning, Vector, Option, Result, Self and Sized. A Moment is a point in time, written in datom as ISO 8601 in UTC, bare; a Duration is a span, written as an integer and its unit, s, m, h or d.

```rust
+ pub struct Moment(pub std::time::SystemTime);
+ pub struct Duration(pub std::time::Duration);
```

```datom
+ 2026-11-07T18:00:00Z   ; a Moment
+ 45m                    ; a Duration
```

### Proposal 2: The Nexus reads a flow from its transcript · psyche-belief › vision/flow-nexus-v1.md

::: comment
The cold moment is computed from the transcript's last call and a configured Warmth per harness; at cold minus the buffer the Nexus acts on an idle flow.
:::

- Every harness event reaches the Flow Nexus through a hook calling the CLI: Report carries the flow's state, and a flow's finished response.
+ A flow is its session, and the Nexus reads it there: it watches the transcript the harness writes and reads each write as it lands, so a response, a tool call, idleness and the end are seen in the file itself, with no part played by the harness; Report, from a hook, carries only what the transcript shows nothing of, and a Working or Idle state is held with the moment it began, read from the transcript and from the pane the herdr Nexus observes, so a flow idle for a day is a question the Nexus answers.

+ A flow's cache stays hot for a time after its last model call, set by its harness and its provider; the Nexus knows that time as a configured Warmth per harness, and reads the moment of the last call from the transcript, so the moment the cache goes cold is computed, never reported. A buffer before that moment, configured too, is when the Nexus acts on an idle flow while it is still warm: a message queued for it is delivered then, and a flow past its Warning share is asked for its handover then, so that it is refreshed from a hot context and a successor is started while the living sleeps, with no cache reheated.

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
+     r -- "the last call's moment" --> c["cold = last call + Warmth.Hot"]
+     c -- "at cold − Warmth.Buffer" --> a["deliver the queue; ask the handover"]
```

```ethos
  [ Set.[ DefaultModules.Vector<ModuleName>
-         Threshold ] ]
+         Threshold
+         ; one harness's cache: how long it
+         ; stays hot, and how early to act
+         Warmth ] ]
```

```ethos
  Flow.{ FlowId Address Pane
-        State.[ Running Idle Ended ]
-        Vector<Event> }
-  Queue.{ Address Vector<Message> }
+        State.[ Working Idle Ended ]
+        ; since the state began
+        Moment
+        ; the last model call
+        LastCall.Moment
+        Vector<Event> }
+  ; when it was delivered
+  Delivery.{ Message Moment }
+  Queue.{ Address Vector<Delivery> }
+  Warmth.{ HarnessName Hot.Duration
+           Buffer.Duration }
```

```datom
+ Configure.Warmth.{ claude 1h 5m }
+ Configured.Warmth.{ claude 1h 5m }
```
