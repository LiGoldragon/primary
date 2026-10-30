Landed, in psyche-context/vision/flow.md 2d9fbb.
## A context module is inserted in the system prompt or in the first prompt

Context: same message.

> The context modules need to be able to be inserted either in the system prompt or in the first prompt.

-- psyche, typed.

Landed, in psyche-context/vision/flow.md 53f68b.
## The lock: needed to roll a metaflow over into a new flow; later Message uses it to know whether a message can reach a flow

Context: same message.

> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

-- psyche, typed.
