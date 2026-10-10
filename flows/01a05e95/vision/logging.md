# Logging

## Rare, high-level flow logs

> “Logging should be rare. It should just be to give a very high-level summary. ... The transcripts are there. If we really need to know the details of what happened, we can look into the transcript. After not so long, those details are not really relevant anymore ... These logs are just gonna keep growing, and they're getting really big. A thousand lines of logging just for a single session is fucking insane.”

-- psyche, typed.

## Subflow logging

> “Well, it's because the sub flows are logging everything, it looks like. That's overkill. Maybe the sub flows should not really log, at least not in a way that the main flow is logging.”

-- psyche, typed.

## Subflow production and context

> “The point of a subflow is for it to edit what it edits and then return the final response. Like I said, the transcript is still there if we really need to know what happened. For it to do all of this logging doesn't just create a lot of all these log files, but it also pollutes this subflow's context. ... It distracts it from its main task by making it constantly add a line every stop. It adds this self-talk, the commentary, where agents' flows talk to themselves, which I don't know if it's useful at all. It just creates a whole lot of noise, and I think it will destroy or reduce the efficiency and the quality of the end result.”

-- psyche, typed.
