# Logging

## A simple enum-based log with no string payload: integers, scalars, booleans, enums; string-matching maps messages to enums, an error to a string-error variant; the agent goes to the logs for the message while they exist; garbage-collectable, cheap, a thin storage layer, very specific about what is stored as a string

Context: said to the primary Claude 840e42 in the same message as the Flow-hooks statement, on what Flow records of the notifications. "no zero payload" is heard as "no string payload", given the sentence that follows; left as transcribed. Logged directly by the main flow before acting.

> It can have a simple enum-based log with no zero payload, just integers, scalar values, booleans, or enums. You can also do string match for enums. If you have certain kinds of errors or messages, you can say, "If it says error, then map it as a string error." If the logs are still there, the agent can use that and go find out what the message was.
>
> At least now we can garbage collect, and we have some collection of the fact that there was an error message there, which costs very little in terms of storage. Let's keep the storage layer thin. Let's be very specific about what we store as a string, which is expensive.

-- psyche, STT.
