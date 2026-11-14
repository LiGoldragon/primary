Presentation.{ «The Git server over two hosts» Proposal }

# The Git server over two hosts

Created by Fable 5.1, on the living's words of 2026-11-09, on research by a Sonnet flow briefed by Psyche core Opus, and on the two-host test run by Psyche criomos Opus.

### Proposal 1: Where a node runs · psyche-belief › vision/horizon.md

::: comment
The living: the cluster should know which nodes are on-premise, his own hardware, and which are in a cloud, and prefer the on-premise node. That is a fact of the node, beside its type and its capabilities.
:::

+ ## A node's premise

+ Every node declares its premise: on-premise, hardware the living owns and holds, or cloud, hardware rented from a provider. A capability that needs one writer among several nodes prefers the on-premise node while it is reachable.

+ ```ethos
+ Premise.[ OnPremise Cloud ]        ; whose hardware the node runs on
+ ```

### Proposal 2: One writer, a standby, and the move between them · psyche-belief › vision/git-server.md

::: comment
Two hosts cannot vote, and the writers are flows that push rarely, so the design is a single writer with a rule, not a consensus: the on-premise node writes, the cloud node copies and takes over after a timed absence, and the returning node pulls before it reclaims. The one thing designed carefully is the handback, so that no push lands in the gap. Tested on Prometheus and a stand-in cloud node: a push refused at the standby armed the timer, promotion after two minutes, two pushes accepted there, Prometheus returned, fetched them fast-forward and took the writer role back, a fourth push mirrored; no push lost. The delays are configuration.
:::

+ ## Two hosts

+ Several nodes may hold the GitServer capability, and one writes at a time: the on-premise node while it is reachable, a cloud node otherwise. The writer's receive hook pushes every accepted push to the standby and then to GitHub; a mirror push that fails is recorded and repeated with the next push. The standby refuses every push of its own and every non-fast-forward update. The cluster's Git name resolves to the writer.

+ Every move answers an event, and nothing polls. The writer's failure reaches the standby as a push it has to refuse, or as the mirror link dropping; that starts one timer of the failover delay; when it fires with the on-premise node still unreachable and the witness, GitHub, reachable, the standby becomes the writer: it records a new primary epoch, which its receive hook honours, and the name moves to it. The on-premise node returning announces itself to the standby and stays read-only, fetches the standby's refs, parks any ref that diverged under `refs/quarantine/<host>/<epoch>/` for a flow to merge, and after the settle delay reclaims the writer role: the standby stops accepting pushes first, the returning node fetches once more, then the name moves back. A planned move runs the same procedure as one command.

+ The accepted loss is the mirror lag: a push acknowledged by the writer and not yet mirrored when it dies waits in that node until it returns. A mirror push that blocks the acknowledgement closes the window at the cost of a slower push; which is chosen is configuration.

+ ```ethos
+ GitReplication.{ Failover.Minutes    ; unreachable this long before the standby writes
+                  Settle.Minutes      ; back this long before the on-premise node reclaims
+                  Mirror.[ Blocking Asynchronous ] }
+ Epoch.Integer                        ; the primary epoch: written by the node that becomes the writer, honoured by every receive hook
+ ```

+ ```datom
+ ; the cluster data; the names are an example
+ { builder OnPremise [ GitServer RemoteBuilder ] }
+ { cloud Cloud [ GitServer ] }
+ { 5 5 Asynchronous }
+ ```

+ ```mermaid
+ flowchart TB
+     w["on-premise node: the writer"] -- "receive hook pushes to" --> s["cloud node: the standby, read-only"]
+     w -- "then pushes to" --> g["GitHub: the backup and the witness"]
+     s -- "writer unreachable for the failover delay, witness reachable" --> p["standby writes, new epoch; the name moves"]
+     p -- "on-premise returns: fetches, quarantines divergence, settles" --> h["standby stops writing, one last fetch, the name moves back"]
+ ```
