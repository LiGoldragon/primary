<!-- to-the-living:start -->
Presentation.{ «Flow: refresh and handover, 2nd edition» }

# Flow: refresh and handover

This book is about how a flow is replaced by a fresh one when its context grows full. It covers when a refresh starts, who runs it, how the old flow hands over, and what the new flow receives. Compaction stays an emergency measure only.

## Proposal 1: psyche-context › skills/vision-flow.md

- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+ A flow's context has three marks, set in Flow's configuration for each layer's model: the floor, below which no refresh is asked for; the warning, at which the flow is told that its refresh has begun and writes its handover; and the ceiling, which a flow is never allowed to reach.
+ The flow is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

+ Below the floor, a request to refresh a flow is refused, as is one for a flow younger than a set age, so that a request routed to a flow just started changes nothing.
+ A flow below the floor is still replaced when its direction changes dramatically: a new job starts on a fresh flow, with the training that job needs.
+ That judgment is named in the request, by the living or by a flow above the one refreshed.
+ Short term: a flow at its threshold is refreshed, not compacted; a compacted flow keeps its noise, and a successor on a fresh flow with a good first prompt does better.
+ Short term: compaction is an absolute emergency measure only, taken when a flow cannot be refreshed; a request to compact a flow or a metaflow meets the same guard as a request to refresh it.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-flow.md

+ The refresh is standard at every layer of every aspect, part of every flow's instruction.
+ Any flow can deploy any other: the structure is decentralized and respawns from any point, so one flow left standing redeploys the rest.
+ Short term: the hook warns Field beside the flow, and Field runs the refresh mechanism for every aspect's flows.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-flow.md

+ A flow warned has a switch-over time to write its handover and go idle; Flow checks that its turn is done, and a flow still turning past that time is sent an interrupt asking it to end its flow now.
+ The living need not notice a refresh.
+ Short term: the hook warns once, records when, and at the end of a later turn past the switch-over time types the interrupt.

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › skills/vision-flow.md

+ Flow keeps track of a refresh: whether the successor started and is working, judged by a small model and recorded.
+ The predecessor is not woken to be told that it has a successor; it is woken only when the successor fails to start, told that its flow could not be refreshed, and then finds the fault or asks for it to be fixed.
+ A refresh replaces only its own flow in the cluster.
+ Short term: the launcher, having started the successor, checks once after a set wait that it registered with the messenger; failing that, it messages the predecessor that its refresh failed.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › skills/vision-flow.md

+ Two flows of one metaflow share everything with each other, and one cedes.
+ The earlier cedes: the metaflow has one current flow, and the later is the one started on purpose.

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › skills/vision-flow.md

+ A refresh is made so that the successor is smarter and better equipped than its predecessor, for the problem at hand and in general.
+ Besides the handover, the successor receives the flow's presentations, the raw psyche it was given, the basic skills, and the best of the layers below it, gathered on refresh.
+ What has been merged into files since the last refresh is carried by the files, never again by a handover, so a lineage does not accumulate.
+ The successor's first goal is a presentation of the current state, its open questions and undecided design, and of the design as it understands it, with figures and examples.
+ The bootstrap is the same for every flow of one layer, so its cache is shared among them.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
