Presentation.{ «A request is cancelled by its id» Proposal }

# A request is cancelled by its id

Created by Fable 5.2.

### Proposal 1: Cancel · psyche-belief › vision/flow-nexus.md

::: comment
His words, 13 November: «We should get someone to find out what the problem is with the Flow Nexus, and also there should be functionality to cancel orders manually.» What happened: open requests that nothing could close were replayed to every fresh flow of a permaflow, which redid them. The cause is being found; this is the feature.
:::

::: shown
psyche-belief › vision/flow-nexus.md
A request is open from its delivery until the Result or Done that answers it, and it is the permaflow's, not the flow's: a successor's first prompt carries, after the handover, every request delivered to its predecessors and still open, each with the id it was delivered under, so the same Result or Done answers it. A Task's minutes keep running across the refresh.
:::

+ An open request is cancelled by its id. Anyone cancels: its sender, its recipient, another flow, the living at a shell. A cancelled request is closed: it is carried to no successor and takes no Result or Done, and a Task's reminder ends with it. Its sender and its recipient are each told once, unless they are the one who cancelled.

+ ```ethos
+ Signal
+ [ flow:[ RequestId ] ]              ; imports
+ [ Cancel.RequestId ]                ; inputs: closes the open request or the reminder of that id
+ [ Cancelled                         ; outputs: it is closed
+   Unresolved ]                      ;   the id names nothing open
+ []                                  ; types
+ ```

+ ```datom
+ ; the living, at a shell
+ Cancel.a1uw
+ Cancelled
+ ; what the sender and the recipient each receive
+ [ { Sender.Living Soft.Cancelled.a1uw } ]
+ ```

## Questions

1. Should the open requests of a permaflow also be listed, so that one can see what to cancel: a plain `Requests` answering each open id with its sender and first words?
