# Messages

## A subflow's response reaches its parent and the peer in one swoop; a completion hook sends a flow's response automatically to the corresponding Claude of the cluster and more endpoints; no duplicated LLM output; take control of the flow

Context: said to the primary Claude 05c604 right after the living asked for many jobs to Codex with reports back. Logged directly by the main flow before acting. "There would be a tool that does that" and "Let's try and make this efficient now" are also working instructions, recorded in log.md.

> And you can even organize a protocol whereby, if Codex sends something that you send him to a subflow, the subflow can communicate directly to you as well as to him. Somehow, its response could tell the subflow to send you the response as well as him in one swoop. There would be a tool that does that.
>
> We want to try to avoid duplication of LLM token output, right? The flow's response is intended to go back to Claude, for example, from Codex. It could be set up so that when it's done, there's a hook that runs. We want to start taking control of the flow more, and it could send it automatically as a message back to the primary Claude or the corresponding Claude of that cluster, and potentially even more endpoints. Let's try and make this efficient now.

-- psyche, typed.
