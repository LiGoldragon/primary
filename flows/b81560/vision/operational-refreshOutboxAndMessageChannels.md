# Operational: refresh outbox handling — messages go out but replies go to successor; flows are users of messaging, not admins; low-priority information channels below user prompt

## The block is so the new flow knows about messages sent after the lock. Messages still go out but metadata says the flow was replaced. Replies go to the new flow. Flows are users — they receive from Psyche High, not implementation details. Also: where are the channels for low-priority messaging that doesn't come in as a user prompt? Subscription-type tool calls, or an MCP server at tool-call strata?

Context: artifact comment by the living on the Session Flashbook, 2026-09-19,
on the "Flow block outbox" question. The living resolves: outbox isn't fully
blocked — messages still go out, but the successor must know about them.
Flows are treated as users of the messaging system, not admins. They receive
from seat names (Psyche High, Psyche Medium), not from flow internals. The
living also opens a new design subject: low-priority information channels
(quota, power usage) that come in below the user prompt — subscription-type
tool calls, or an MCP server at tool-call strata. Logged by the main flow
before acting.

> Well, I think it could block the outbox because the way we want to make the flow is that it'll trace back to its process so that the flow itself will know which flow this came from. It's just clearer for everybody.
>
> I guess maybe it doesn't block the outbox, but it kind of does in a way where it needs to make sure that the new flow would have to know about the message that was sent after the lock came in. That is what the block would be about, so that it could know that it told that to someone. It would just need to know about it.
>
> I guess we would still want the message to go out, right? We would need to modify the message metadata to say that this flow, where the message came from, was actually replaced. Actually, the message, when it came in, shouldn't even expose all of that, because let's consider the flows as users. They're users of the messaging system. They don't need to know everything about how it works. To them, they're just receiving the message from Psyche Medium or Psyche High, or Psyche Astra, even, which is fine enough. You can chime in there, but I think Psyche High is probably most stable and most universal and always true. It's just that Psyche might refer to them as models. They're interchangeable, and in terms of the CLI, they're probably going to be better off just saying Psyche High, Psyche Medium.
>
> We just need to make sure that it's fine. That's what the message and flow system are going to do: if the message does go out to its destination, then the reply will go to the new flow. The new flow also knows what the message was that was sent to another flow by its ancestor. I'm not sure you can. It doesn't have to come in as a user prompt, but it could. Let's also see what kind of channels we have. Where are the channels for low-priority messaging where it doesn't come in as a user prompt, so it's more just informational, like the quota: how much quota is left for the model? If we're over power usage or under power usage, we ever get that to certain flows, which could use it for their communication and their awareness, but it doesn't need to come in as a middle-layer user prompt because it's not that impactful on design and stuff. It's just more small, trivial information. Maybe you can think of suggestions of what could go in there, even. Let's design that with each harness. How do we have this sort of tool call-level information channel that can come in? It's a subscription-type tool call, maybe, where the call is just kept alive and something wakes up the flow about new and another object coming in. Or does it have to get, do we have an MCP server that can talk to the flow that would be like a tool call-level strata?

-- psyche, artifact comment on Session Flashbook.
