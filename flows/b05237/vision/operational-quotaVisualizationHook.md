# Operational: a hook that injects quota context and precomputed metrics into the next queued message, plus a quota visualization interface

## Do we want a hook that automatically injects context and quotas into the periodic message? It creates 4 or 5 useful metrics. Show me the anatomy of the quota visualization interface. Approved document means approved system, written and running

Context: artifact comments by the living on the Fable design artifact
(aec7d804), 2026-09-18. Recovered from cloud auto-reply thread.

> Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? That way, the model doesn't have to stop. The hook could even give it precomputed metrics, like how much time is left and how fast we've been burning it lately. It creates a few, like 4 or 5, useful metrics.
>
> Show me the anatomy of all that: the quota visualization interface. Let's keep that one of the artifacts, right? Claude artifacts, but they're like vision documents. It's a vision, say, a unified vision document. It involves multiple vision parts that might land in different skill files, but they're presented together as a whole because it modifies what already exists. It's like a proposal, right? It's going to be documented as the document, the ultimately approved version that became the implementation, as much as we knew back then. That's how we're going to proceed and create. An approved document means an approved system, written and running and ready to be deployed in production and tested in a near-production or actual-production emulation environment.

-- psyche, artifact comments on Fable design artifact aec7d804.
