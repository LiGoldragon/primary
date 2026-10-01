
## 2026-09-30 — unique service and socket suffix

> Okay, are we doing that and doing the rotation like I said, so that the next will have 6.1 Sol and this stable socket? Oh, maybe a little problem, though. Here's a clever thing: we would have to think of a clever way to do that, but each service is going to have this unique suffix.
>
> Maybe we can get the short version of the hash of the version of Codex that we're using for it, so that each socket will have a different name. That way, we can move the next to the stable without changing the socket name, so it doesn't break any of the sessions.
>
> Maybe we can do that in a hacky way, with a bunch of comments on how we're going to fix it next time. The current next can just stay called whatever it is, and the next next can have this new hash-suffixed version socket. That way, we don't break our current sessions.

-- psyche, input mode not established.

Context: exploratory design for channel rotation; preserve current sessions and distinguish stable/Next labels from persistent endpoint identity. This is a notion pending a concrete reviewed implementation proposal.
