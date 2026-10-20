<!-- to-the-living:start -->
Presentation.{ «Flow: messaging between flows, 2nd edition» }

# Flow: messaging between flows

This book is about what a flow is, what goes wrong when two flows of one metaflow are alive at once, and how a flow comes to know what the others know. It also proposes the intent you asked for: what is deterministic is done in code. How messages are sent through Flow is the machine's own work and went to its owner.

## Proposal 1: psyche-context › skills/vision-flow.md

+ Two flows of one metaflow alive at once split the psyche: what is said to one, the other does not know.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

+ A flow is a session: when the whole context is restarted, that is a new flow, a different context.
+ The harness itself has the concept, and exposes it as the flow's id.
+ A flow that is not working is idle.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/intent-deterministic-work.md, a new file

+ ## Deterministic work is done in code
+ We intend to do anything that is deterministic in code, to save the context, cost and noise that making a model do it would incur.
+ A model does not check its flow id: it gets it in its prompt.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-remembering.md

+ ## A flow knows what the flows concerned know
+ A discussion drips into every flow it concerns: a flow knows what the other knows, and vice versa.
+ The sharing is a skill, or a specialized subagent role that reads recent sessions for psyche rulings and insights that directly impact its parent flow.
+ Session files are made accessible and searchable for agents.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
