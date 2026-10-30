# Flow

## 2026-10-29 — A reminder in Flow: a task message carries its expected minutes; the done reply names the task and cancels the reminder
Context: the living, in the Psyche core Primary chat b2b87a, after an evening in which Field and the book flow answered no order and nothing told the Primary how long to wait.

you need a function in flow that lets any metaflow (regardless of wether its refreshed) get a "reminder" so that it can check on stuff, using a per-situation timer, so it can be reminded if something is taking too long. it could even be a field in a certain kind of "task" message, which the receiver would see (a number of minutes) which would let the receiver know how long it is expected to take. then the task-done reply would let the sender indicate which task so that the reminder is cancelled when the message is received. what do you think?

## 2026-10-29 — Resiliency: a task's receiver going idle fires a notification; Flow installs hooks on every harness event, some carrying content, ephemeral; all configurable
Context: the living, in the Psyche core Primary chat b2b87a, after the book flow went idle on an order and nobody was told.

Hence why I'm talking about this reminder thing. Not only that, but here's another cool idea: somebody should have received a notification that this book flow went idle because we were waiting for something from him. Either he messages back, which cancels the notification, only when the message reaches a particular metaflow, or he goes idle, and then the notification fires.

That way, we need a system, essentially, where things never just get forgotten and someone just does nothing and never replies or fails. We need resiliency. The Flow Nexus needs to install hooks in every part of the system where it can get notified of anything that's happening to that particular flow, so that it knows and has the data to be able to act on and implement all these features.

Basically, all the hook does is say, "Such and such when idle." Maybe some of the hooks even deliver content, meaning they might deliver the last message because that might actually be useful as a feature to be passed on somewhere. We wouldn't necessarily store it in memory. It might be acted on, or it might not be acted on, and it might just disappear from the Nexus's memory. It might just be an ephemeral piece of data that is either acted on or thrown out.

Do you understand what I'm saying? Can you see how we can build a really resilient system? Maybe you want to get your Flow Nexus designer to investigate this in depth and/or have his secondary investigate all of these functionalities that the harness can deliver, and draft all of these cool features that we could do with this. That would be configurable, meaning they would be optional and we wouldn't necessarily have to use them, but they would be there for us to play with and create a much more resilient and reliable system from.

## 2026-10-29 — Usage and quotas accounted for; the system relogs in when tokens expire; a refresh never leaves the system without a core Primary
Context: the living, in the Psyche core Primary chat b2b87a, after the Primary's relaunch was refused by the composer. Parts of one message; the persona and ethos parts are in vision/persona.md and vision/ethos.md.

I know that you don't have a good track record so far of making a nexus that works. With everything that I've said about creating reliability and a way for things to not have you fall asleep (to not have things go into a flow that ends up doing nothing, not replying, or failing), we want to get to the point where, I think, at this point, if we created a loop, every time you have enough usage in your quota (and this is another thing), we need some kind of system, whether it's the Flow Nexus or another one, to start accounting for our usage and our quotas.

By the way, this is another aside: we need a way for the system to be able to relog in because the tokens seem to expire after a certain time.

And I hope that once you reach your context limit, your current flow doesn't get killed, and that this problem that is keeping you from starting a new flow doesn't prevent the new flow from starting (which would leave us without a primary core).
