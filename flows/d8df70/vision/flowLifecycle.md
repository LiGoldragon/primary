# Flow lifecycle

## A new flow starts receiving as soon as it has its start prompt; the old one stops receiving first and is killed, and its conversation archived

> A seat starts receiving. The old seat stops receiving first. That's how we get a lock. I'd rather use the word "flow" also, but do you mean something else by "seat"? A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently.

-- living, comment on "What Waits for the Living", 2026-09-24 14:28Z, on question 1 (when a new seat starts receiving).

## The old flow is closed when its replacement is ready; a refresh needs a recent flow handover in the transcript

> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it.
>
> In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

-- living, comment on "What Waits for the Living", 2026-09-24 14:32Z, on question 6 (when an old flow is closed).
