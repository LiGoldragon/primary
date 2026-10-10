# Flow lifecycle

## A recycle: the Flow component keeps track of the flow's progression and whether the successor launched and works, checked by a small model and put in the database; the old flow is not reawakened to learn it has a successor, its last thing is "I've sent the recycle signal"; Flow wakes it only if the new flow could not start, and it can say "fix that and let me know"

Context: typed to the primary Claude fd0f97 after it concluded 05c604 by editing the predecessor's log and index line by hand. "This goes in persona, maybe" and "Flow keeps track ... so that's where it goes" place the check in the Flow component. Anatomy questions are asked in the reply. Logged directly by the main flow before acting.

> We need a way for the system to know. I guess I don't want to reawaken an old flow just to tell it that it has a successor. We need a component to just keep track of whether success has been launched now and it's working, which could be checked by a small model making sure that the flow is working properly. That check gets put in the database.
>
> This goes in persona, maybe. Flow keeps track of the flow's progression, so that's where it goes. There's a check, and the new flow knows that it's the current flow. The old flow doesn't need to think that it has become the new flow. It now knows that the flow is continued somewhere else, so it exists somewhere else. It doesn't need to go back in its past.
>
> That session is just left with its last thing being flow. What do we call it? The recycle, right? It's a new cycle, a recycle, and then it should just say, "I've sent the recycle signal." I think what would happen is it would get woken up by Flow if the new flow was unable to start, and tell it, "There seems to be a problem with your flow. Unable to recycle your flow." Then I could wake it back up, which would ensure a kind of continuity.
>
> Maybe the old flow could figure out what's wrong and why it can't launch. Maybe it didn't send the command properly, or it can actually send the message, "Here, I'm having trouble again. Fix that and let me know when it's fixed." Right? That's reliability.

-- psyche, typed.

## The psyche's messages are not being passed along the cluster, like a cluster failure; there is no central place to handle the flows; the flow component must take care of flows reliably; put all the pieces together and bring it online

Context: typed to the primary Claude fd0f97 after it reported that Codex's reports had landed in the concluded predecessor's window. The opening questions are answered in the reply; "Let's put all the pieces together and bring it online" is a working instruction, recorded in log.md. Logged directly by the main flow before acting.

> Are you getting user prompt input from Codex about the psyche user prompts that have been coming in? Is he passing that to you, or have a bunch of psyche not been passed along in the last day? I feel like I don't see my messages, what I'm saying, being passed along to the other parts of the cluster. It's like there's a cluster failure going on. Maybe the old part of the flow is getting the messages now. There is not a central place to handle the flows. We need to really secure the flow component to take care of flows reliably. Let's put all the pieces together and bring it online. I've been talking to Codex Primary a lot, just now, before I sent you this.

-- psyche, typed.
