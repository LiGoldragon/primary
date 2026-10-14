<!-- to-the-living:start -->
Presentation.{ «Flow: short term and long term, second edition» }

# Flow: short term and long term, second edition

## Crystallization

### Proposal 1: the short term, as a figure

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», a new heading after «A replaced session is reaped by the refresh itself».

Sources: d68c82 flow.

Removed: none.

Added:

```
+ +--------------------------------------------+
+ | EDN files: shared, one per aspect,         |
+ | one per metaflow                           |
+ +--------------------------------------------+
+         | name the context modules,
+         | system or user prompt
+         v
+ +--------------------------------------------+
+ | the launcher                               |
+ +--------------------------------------------+
+         | starts
+         v
+ +--------------------------------------------+
+ | a flow, lean, on its topic                 |
+ +--------------------------------------------+
+         | a hook measures its context;
+         | at the threshold it warns
+         v
+ +--------------------------------------------+
+ | the flow, warned                           |
+ +--------------------------------------------+
+         | writes
+         v
+ +--------------------------------------------+
+ | its handover                               |
+ +--------------------------------------------+
+         | Field compacts it, or restarts it
+         v
+ +--------------------------------------------+
+ | a successor, clean context                 |
+ +--------------------------------------------+
+         | work done:
+         | spun down
+         v
+ +--------------------------------------------+
+ | the topic, idle                            |
+ +--------------------------------------------+
+         | new input wakes it
+         v
+ +--------------------------------------------+
+ | a new flow, clean context                  |
+ +--------------------------------------------+
```

### Proposal 2: the EDN launch

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 1's figure.

Sources: d68c82 flow.

Removed: none.

Added:

+ Short term: flow starting is configured in EDN files, one shared by every aspect, one per aspect, and one per metaflow holding what differs; from them the launcher finds each context module and whether it goes in the system prompt or the user prompt.

A:

+ When Flow takes over launching, the EDN files stay the authored source and are sent to Flow as configuration payloads on its meta socket.

B:

+ When Flow takes over launching, the EDN files are rewritten as datom files.

Ruling: land the first line, change, or drop; and A or B.

### Proposal 3: lean, specialized flows

File: `psyche-context/skills/vision-flow.md`

Under: «What it does».

Sources: d68c82 flow.

Removed:

- A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

Added:

+ Starting a specialized flow is cheap: it carries only the context modules and tools its purpose needs, so its output is of higher quality; when its work is done it is spun down, and waking its topic starts a new flow with a clean context.

Who spins a flow down, A, B or C:

A:

+ A flow spins itself down when its work is done.

B:

+ The flow that asked for a specialized flow spins it down when its work is done.

C:

+ Flow spins down a flow that has gone idle.

Who wakes an idle topic until Flow runs, A or B:

A:

+ Until Flow runs, a small model judges when new input wakes an idle topic.

B:

+ Until Flow runs, the Secondary that receives new input wakes the idle topic.

Ruling: land, change, or drop; then one of A, B, C, and one of A, B.

### Proposal 4: the refresh warning

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 2's line.

Sources: d68c82 flow.

Removed: none.

Added:

+ Short term: when a flow's context reaches a threshold, a hook warns the flow and Field. The flow is told its refresh procedure has started; it writes its handover and names what of its context goes to existing or new topic flows. Field compacts or restarts it.

Ruling: land, change, or drop.

### Proposal 5: the handover carries judgment

File: `psyche-context/skills/vision-flow.md`

Under: «A replaced session is reaped by the refresh itself», after its last paragraph.

Sources: d68c82 handover.

Removed: none.

Added:

+ A handover carries what needs judgment; what a tool returns in one call, such as which revision was pushed or the order of events, the successor looks up.

Ruling: land, change, or drop.

### Proposal 6: guarded compaction

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 4's line.

Sources: 33752b flow; d68c82 flow.

Removed: none.

Added:

+ Short term: a flow or a metaflow is compacted on request; Flow accepts the request when the flow's context has passed a set size and the flow has reached a set age, so it lands on a flow that has worked. A compacted flow still carries noise.

A:

+ The size and the age are each one value for every flow.

B:

+ The size and the age are each set per layer.

Ruling: land, change, or drop; and A or B.

### Proposal 7: the long term, as a figure

File: `psyche-context/skills/vision-flow.md`

Under: «Long term», a new heading after «Short term».

Sources: d68c82 deployment; d68c82 flow.

Removed: none.

Added:

```
+ +--------------------------------------------+
+ | the living, a flow, a hook                 |
+ +--------------------------------------------+
+         | send a request
+         v
+ +--------------------------------------------+
+ | Message Nexus                              |
+ +--------------------------------------------+
+         | asks Flow: deliver to
+         | { Aspect topic Layer }
+         v
+ +--------------------------------------------+
+ | Flow Nexus, holding the lock               |
+ +--------------------------------------------+
+   |                           |
+   | answers: sent             | composes the
+   | or queued                 | prompt from the
+   v                           | registry, hash
+ +--------------------+        | checked
+ | Message Nexus,     |        |
+ | subscribed to its  |        |
+ | events             |        |
+ +--------------------+        v
+ +--------------------------------------------+
+ | a flow, in its Capsule                     |
+ +--------------------------------------------+
+         | hooks call the Flow CLI;
+         | at the threshold: handover, lock
+         v
+ +--------------------------------------------+
+ | the successor flow; predecessor            |
+ | reaped in the same event                   |
+ +--------------------------------------------+
+         | work done:
+         | spun down
+         v
+ +--------------------------------------------+
+ | topic idle; a small model judges           |
+ | when to wake it                            |
+ +--------------------------------------------+
```

### Proposal 8: from short term to long term, as a figure

File: `psyche-context/skills/vision-flow.md`

Under: «From short term to long term», a new heading after «Long term». Red is what leaves the short term; green is what comes in its place.

Sources: 445410 nexus; d68c82 deployment.

```
- +--------------------------------------------+
- | EDN launch files                           |
- +--------------------------------------------+
          | are sent as datom payloads
          | on the meta socket
          v
+ +--------------------------------------------+
+ | Flow's configuration, in its Memory        |
+ +--------------------------------------------+
- +--------------------------------------------+
- | launcher scripts                           |
- +--------------------------------------------+
          | are replaced by
          v
+ +--------------------------------------------+
+ | Launch on Flow's socket                    |
+ +--------------------------------------------+
- +--------------------------------------------+
- | hook warns Field; Field compacts or        |
- | restarts                                   |
- +--------------------------------------------+
          | are replaced by
          v
+ +--------------------------------------------+
+ | Flow refreshes, locks, reaps,              |
+ | in one event                               |
+ +--------------------------------------------+
- +--------------------------------------------+
- | closed pane, fresh launch                  |
- +--------------------------------------------+
          | are replaced by
          v
+ +--------------------------------------------+
+ | Flow puts the metaflow asleep and          |
+ | wakes it                                   |
+ +--------------------------------------------+
```

Ruling: land, change, or drop.
<!-- to-the-living:end -->
