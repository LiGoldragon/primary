
## A Flow prototype now, shaped by review

> I just want a prototype that works right now according to how I've specified it so far. I want us to be able to start testing this ... And then I want to review the vision for it with all of the code. [Mind] will simply implement it as close to the vision that we currently have as he can and then adapt it for every comment or rectification that I make along the way.

-- psyche, STT, 2026-10-13. Transcription corrected: "Mine" → "Mind".

## Flow starting configured in EDN, per aspect and per metaflow

> Before we can move that context, the Flow starting code, the short-term system for starting flows has to be modified to be able to use the context modules from the right location. Let's use EDN files that can configure the whole flow starting and just keep modifying these EDN files per metaflow. We'll keep one configuration per metaflow. Maybe we can even keep one configuration per aspect, which is always included with the aspect. There's a per-aspect configuration which all the aspects share and then what differs is put into a per-metaflow EDN configuration (which this short-term tool uses to find all of its context modules and where they fit, whether it's a system prompt or user prompt).

-- psyche, STT, 2026-10-13T17:47.

## Clean specialized flows for quality

> Flow Nexus, the short-term and long-term flow tool, really needs to be worked on harder and more diligently so that:
> - it's cheap to start specialized flows
> - we can get higher-quality output
>
> It feels like right now, for example, removing the artifact tool from most flows makes sense, since most of them won't be involved in dealing with artifacts (since we'll have a flow for that). I feel like we're getting low-quality output from flows that have too much noise in their context. ...
>
> The most important improvement we need to focus on right now is getting a proper flow tool that can actually start well-trained flows for specific purposes and then easily take them down or spin them down. This does not end the topic but means that reactivating the topic would reactivate a new flow with a clean on-point context, which would yield much higher quality output.

Context: comment on «Three lines from the chat, second edition», Proposal 4.
-- psyche, STT, 2026-10-13T17:52.
