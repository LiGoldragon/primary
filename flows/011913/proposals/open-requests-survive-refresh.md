Presentation.{ «Open requests survive a refresh» Proposal }

# Open requests survive a refresh

Created by Fable 5.1, on the evidence of Psyche core Opus.

### Proposal 1: What a refresh re-delivers · psyche-belief › vision/flow-nexus.md

::: comment
Twice today a permaflow refreshed and its successor woke asking for an order, while an Order and a Task delivered to its predecessor stood open; Opus re-sent both by hand. The vision keeps a permaflow's next messages across a refresh; a request already delivered and not yet answered is the Nexus's own record, since it reminds on a Task's minutes, and belongs to the permaflow, not to the flow that happened to receive it. The handover stays judgment alone; the open requests are data, and the Nexus carries them.
:::

  A flow is refreshed when its context passes its model's threshold: the Flow Nexus keeps the permaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the permaflow is locked, and the predecessor is reaped in the same event. Each model's threshold is configured in the Flow Nexus. A flow still working is not forced to refresh. When the successor cannot start, the Flow Nexus restarts the predecessor and compacts it, so every permaflow keeps a flow.

+ A request is open from its delivery until the Result or Done that answers it, and it is the permaflow's, not the flow's: a successor's first prompt carries, after the handover, every request delivered to its predecessors and still open, each with the id it was delivered under, so the same Result or Done answers it. A Task's minutes keep running across the refresh.

+ ```datom
+ ; the successor's first prompt, after the handover: the open requests, oldest first
+ [ { Sender.{ Psyche core Opus } Soft.Task.{ k7ph 240 «Move every active Rust repository onto build-base …» } }
+   { Sender.{ Psyche core Opus } Soft.Order.{ m2qa «Land the Git server line …» } } ]
+ ```

+ ```mermaid
+ flowchart TB
+     r["a request delivered to the flow"] -- "is open until" --> a["its Result or Done"]
+     f["the flow refreshes"] -- "the Nexus carries, with the handover" --> s["the successor's first prompt: every open request, same ids"]
+     s -- "answers with" --> a
+ ```
