# Flow lifecycle

## A refresh replaces only its own flow in the cluster, a triad, not a pair; bookkeeping of flows, probably in orchestrate; a floor before restarting a flow

Context: correction of the primary's revised flow-refresh wording, which said the successor "takes over the pair". "That didn't work" is left as typed; its referent is not known. Logged directly by the main flow.

> No, that's not quite it either, because you said the successor claims it's only and takes over the pair. Well, first of all, it's not going to be a pair, right? We're going to be a triad, but it doesn't take over; it doesn't change the whole cluster. It only changes its own flow for a new one. In the cluster, its flow is replaced.
>
> We're going to have some kind of bookkeeping, probably in the orchestrate component, to keep track of those flows, unless there's a better place for it. That didn't work. Also, when you say that when a new flow is needed, we also should have a floor. Let's not restart a flow that only has less than 15% of its context used, at least, right, or maybe even 20

-- psyche, typed.
