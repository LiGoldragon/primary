# Deterministic work goes into code

## The model does not check the flow id; it gets it in its prompt; anything deterministic is code — to become intent
Comment on «How Flow launches a flow and builds its prompt» (5578cc), at "Flow picks the session id…".
> "In any case there's no reason for us to make the model check the flow ID. It should get it in its prompt because, if anything, we can start a session without launching its first prompt and we can get its session ID before it even starts. We don't have to pay for the LLM to do all of the work that a deterministic cheap program can do. Let's make this so we need something developed into intent: that we intend to do anything that is deterministic into code, to save the context, cost, and noise that making an LLM do it would incur."

-- psyche, typed, book comment, 2026-10-03T16:17Z, relayed by 5578cc.
