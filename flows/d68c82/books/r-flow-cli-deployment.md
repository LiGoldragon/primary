<!-- to-the-living:start -->
Presentation.{ «Flow: CLI, deployment, long term, 4th edition» }

# Flow: CLI, deployment, long term

This book is about how Flow starts the flow a request needs: when an earlier conversation is woken again, when a fresh one starts instead, and in what order a Primary and its Secondary start. It also names queuing as a long-term goal and gives a flow without a brief its default task.

## Proposal 1: psyche-context › skills/vision-flow.md

- A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice.
+ Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context.
+ A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A metaflow a request needs is started whether or not it is running.
+ With a still-young working transcript, its flow is reawakened from it; with none, it is fed the metaflow's context modules and the prompt it is to get now.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-flow.md

+ A context is young while it is small: past about a hundred thousand tokens a context degrades fast.
+ Only a young transcript is reawakened; an older one gives way to a fresh flow fed the metaflow's context modules.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-flow.md

+ Short term: a Primary starts only after its Secondary is live.
+ Queuing is a long-term goal, for much higher output quality and efficiency: an interruption alone interrupts, and when it is done, all of the queue that should go with it comes in.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-flow.md

+ A flow launched without a brief has the default task: a proposal or a question.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
