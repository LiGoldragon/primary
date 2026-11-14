Presentation.{ «A restarted flow is the same flow» Proposal }
# A restarted flow is the same flow

Created by Fable 5.1, who wrote this; nothing else helped.

### Proposal 1: A restart · psyche-belief › vision/flow-nexus.md

**Comment** The paragraph under "Restarting without waking" is replaced whole.

- A flow can be restarted without being woken: its harness closes, its transcript stays, and its successor runs when a message wakes it. A flow can also restart itself. A restart meant to leave the flow asleep is done from outside; what arrives queues for its successor.
+ A flow is its session. A restart closes its harness and reopens it on the same session; a refresh starts a fresh flow.

### Proposal 2: Flow · mind-belief › knowledge/vocabulary.md

**Comment** The Flow entry gains its continuity.

- Flow: one run of a permaflow, from launch to end: its main thread and every subflow it starts; also the Nexus that manages flows.
+ Flow: one session of a permaflow, from launch to refresh or stop, through every restart of its harness: its main thread and every subflow it starts; also the Nexus that manages flows.
