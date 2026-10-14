<!-- to-the-living:start -->
Presentation.{ «A guarded compaction request, second edition» }

# A guarded compaction request, second edition

## Crystallization

### Proposal 1: the guarded request, as a figure

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», a new heading after «A replaced session is reaped by the refresh itself».

Sources: 33752b flow; d68c82 flow.

Removed: none.

Added:

```
+ +------------------------------+
+ | compaction request           |
+ | naming a flow or a metaflow  |
+ +------------------------------+
+         | arrives at
+         v
+ +------------------------------+
+ | Flow                         |
+ +------------------------------+
+         | observes, for the flow
+         v
+ +------------------------------+
+ | context size                 |
+ | age since launch             |
+ | time since last compaction   |
+ +------------------------------+
+         | compares with
+         v
+ +------------------------------+
+ | configured size, age,        |
+ | interval                     |
+ +------------------------------+
+         |
+    +----+-----------+
+    | under a limit  | past every limit
+    v                v
+ +-------------+  +-----------------+
+ | refuses,    |  | compacts the    |
+ | naming the  |  | flow            |
+ | cause       |  |                 |
+ +-------------+  +-----------------+
```

### Proposal 2: the guarded request, its three values

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 1's figure.

Sources: 33752b flow; d68c82 flow.

Removed: none.

Added, with SIZE, AGE and INTERVAL left for you to fill:

+ Short term: a compaction request names a flow or a metaflow, and Flow accepts it when the flow's context holds at least SIZE tokens, the flow has run at least AGE since launch, and its last compaction is at least INTERVAL past; otherwise Flow refuses it, naming the cause.

A:

+ SIZE, AGE and INTERVAL are each one value for every flow.

B:

+ SIZE, AGE and INTERVAL are each set per layer.

Ruling: fill the three values, and choose A or B.

### Proposal 3: an unobserved context size

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 2's line.

Sources: 33752b flow.

Removed: none.

A:

+ When Flow cannot observe a flow's context size, as right after a compaction, it refuses a compaction request for that flow.

B:

+ When Flow cannot observe a flow's context size, as right after a compaction, it judges a compaction request for that flow by age and interval alone.

Ruling: A or B.

### Proposal 4: the same guard on a refresh request

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 3's line.

Sources: 33752b flow.

Removed: none.

A:

+ A request to refresh a flow by handover passes the same size and age guard as a compaction request.

B:

+ A request to refresh a flow by handover is guarded by the layer's refresh threshold alone.

Ruling: A or B.

### Proposal 5: compaction keeps noise

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 4's line.

Sources: 33752b flow; d68c82 flow.

Removed: none.

Added:

+ A compacted flow still carries noise; compaction serves while large contexts cannot be afforded.

Ruling: land, change, or drop.

### Proposal 6: Psyche Primary topic flows stay small

File: `psyche-context/skills/vision-flow.md`

Under: «Short term», after Proposal 5's line.

Sources: 33752b flow.

Removed: none.

A:

+ Each Psyche Primary topic flow keeps a small context.

B:

+ Psyche keeps few Primary topic flows.

Ruling: A or B.
<!-- to-the-living:end -->
