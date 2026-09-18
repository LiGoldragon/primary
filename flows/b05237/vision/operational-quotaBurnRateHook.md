# Operational: keep track of quotas and burn rates; a hook injects context and quotas with a timestamp into the next queued message, with precomputed metrics

## Let's all keep track of the quotas and the burn rates, estimated burn rates. Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? Show me the anatomy of all that: the quota visualization interface

Context: artifact comment by the living on Psyche Fable's report "The Vision
Dependency Picture, Whole" (subflow of b05237), 2026-09-18, in the same
comment as the full-signal-communication statement. The living names quota
and burn-rate tracking as something all flows keep, and floats a hook that
attaches context and quota metrics to the next queued message so the model
never has to stop to check. The hook is framed as a question ("do we even
want"); the anatomy is a direct request. Logged by the subflow before acting.

> Let's all keep track of the quotas and the burn rates, estimated burn rates.
>
> Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? That way, the model doesn't have to stop. The hook could even give it precomputed metrics, like how much time is left and how fast we've been burning it lately. It creates a few, like 4 or 5, useful metrics.
>
> Show me the anatomy of all that: the quota visualization interface.

-- psyche, artifact comment on the Vision Dependency Picture, Whole; input mode not stated.
