# Messaging

Comment on «Flow, whole, in ethos», 2026-10-11 20:29, at the passage «A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the li…».

> I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock.
>
> If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective.
>
> Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that.
>
> Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

-- psyche, STT.
