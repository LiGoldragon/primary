# Operational: the requester holds nothing — gets a request ID, can check status, send messages, and gets notified when done if still in charge

## The requester doesn't hold anything. He gets a request ID so he can ask for status later. He can ask for more detail about what the subflow is doing. He can send messages if it's still alive. If he's still the flow in charge when it's done, he gets a message

Context: spoken by the living to Psyche Fable f38926 on 2026-09-19, relayed
to primary Psyche opus b81560 with psyche propagation. Mid-turn continuation
on the async subflow architecture. The requester is fully decoupled: no
blocking, no held state. A request ID is the only handle. The requester can
poll status, get detail, send messages to the subflow, and receives a
completion message only if it is still the flow in charge (not replaced by
a successor). Fable appended to flows/f38926/vision/subflows.md. Logged by
the main flow before acting.

> The requester doesn't hold anything. He gets a request ID assigned so he can ask for status again later if he wants to see what's going on. He can ask for more detail, and he can get detail about what that subflow is doing. Obviously, he can send that subflow messages if it's still alive. If he's still the flow in charge when that flow is done, he'll get a message.

-- psyche, to Psyche Fable f38926, relayed to primary Psyche opus b81560. Input mode not established.
