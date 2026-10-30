
## Several Flow Nexuses at once; a new one tried raw before it is deployed

2026-10-25, to Psyche core Secondary 36ac89. Context: answering that the Flow refresh-from-outside build is built and tested but not deployed, its blocker unknown.

> See if we do this properly, we can manually configure an already running [Herdr session] with its flows into any new flow nexus by using the operations that allow us to do that. We could have multiple flows even though they would fall out of sync as soon as you use one, potentially.
>
> Still it seems to me the running flow right now is only useful for starting flows and even then it's quite flawed because it only allows the flow itself to do it. It seems to me that we can have these multiple flow nexuses running simultaneously and the new one being tested doesn't need to be deployed through our operating system's declaratives. It doesn't have to be deployed declaratively, right? We can still test it by just running the binary raw, wherever it's built, with the right environment variables, in a hacky manner (which is essentially how you operate now 99% of the time anyway), to try it. Once we've established that it's reliable and so on, then we can deploy it.
>
> I really don't see a blocker here and I think that this approach should be added somewhere, [as a belief], maybe in a compensation.

Transcription corrected: "herder capsule" → "Herdr session"; "and you believe" → "as a belief".

## No restrictions hardwired into Flow; seats have their tools and subagents

2026-10-26, to Psyche core Secondary 36ac89. Context: seats launched by Flow 0.40 were reported unable to use subagents; a new Primary had been started.

> Okay we're having huge problems with the new flow. We started a new primary. Don't talk to it because it's useless but I've been talking to the Flow secondary topic, or to the secondary with the Flow topic, and he doesn't seem to even understand that.
>
> What I suspect is that I think the Flow didn't have any tools. We have all of this hardwired security, or so-called invariants that I talked about as a long-term vision goal for the entire system as a whole to have. But now agents are trying to hardwire that into individual components.
>
> It said that. The other secondary said that the flows, the new flow starts, can't use subagents. I don't want any of these fucking restrictions. It's not what I want. It's not what I want. It's not what I want. Oh my god this is so bad. You guys have done a horrible job.

## Every main flow can talk with the living; no tool limits in code, used at once

2026-10-26, to Psyche core Secondary 36ac89. Context: after the seat configuration showed nearly identical belief modules for every seat, and Flow code still denying tools.

> That's okay. We're not yet at the point where I might not talk to some of the main flows. Although it's happening less and less, let's make all the main flows able to talk with me because right now we're at the very rough, brittle, and hacky prototype phase. There isn't really a specific set of flows that I only talk to yet. But they do have different roles. Anyway we haven't really talked about this. You're not able to make really good decisions but I'm just mentioning it for later. It's not a big deal for now but I do want my flows to be able to use tools and I don't want all of this hard-coded behavior limitation in my code. Yank all this fucking garbage out right now and don't even wait for declarative deployment to use the executable we'll get that isn't fucking crippled.

## All capabilities, unlimited, some on the meta socket

2026-10-26, to Psyche core Secondary 36ac89. Context: while my subflow strips hard-coded tool limits from Flow.

> Get an Opus Flow to audit the code for any other hardwired behavior limitations or missing debugging features. We don't want to have to modify the code to get out of a bind, to reconfigure anything, or for any kind of behavior we might want to try to make possible. We want absolutely all the capabilities, fully unlimited, although they can be on the [meta] socket, which doesn't really have an actual limiting effect because the meta socket is available to everyone too.
>
> At least we're putting the concept of having different sockets into practice. We could just put it all on one socket right now. It wouldn't practically make a difference but we're just sort of trying to dogfood our concept. Like I said, all of this idea that we're going to limit the feature or the capability of our staff is preposterous at this point.

Transcription corrected: "Terra" → "meta".

## Simplified flows have no use yet

2026-10-26, to Psyche core Secondary 36ac89. Context: the Psyche core Primary had been declared Simplified with an empty explicit tool list, so it launched with no tools.

> We don't have a use for simplified flows yet because we don't have the hook infrastructure to really use them.
