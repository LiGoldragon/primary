# Flow

## 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow
Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.

Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."

On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.

## 2026-10-28 — Codex threads may be left running on the app-server; Flow Nexus puts out the thread when it closes a flow
Context: the living, 2026-10-28 12:28, in the Psyche core Primary chat 046782; held until now only in that transcript, logged here on his order of 2026-10-29 to find what he meant.

Maybe this thread limit thing has to do with RAM consumption. Maybe all of the codex threads are still running even though they're not in the herder because they're running on a server, and we're just leaving them all. We didn't close them out. That's just the theory, but if that's the case, then we're going to have problems continually. Let's make sure we rule that out. If that's the case, we would need Flow Nexus to put out the thread when it closes it out, so that doesn't keep happening.

## 2026-10-29 — Codex threads are checked for accumulation; old ones are killed or archived
Context: the living, in the Psyche core Primary chat 554e1a, while reviewing Vision by horizon.

While I'm reviewing this, I'd like you to first find out what I mean exactly by referring to times when we talked about this. Have someone check to make sure that we aren't accumulating Codex threads anymore and that the old ones are being killed or archived (or whatever needs to happen to them), so that they don't accumulate and end up killing the system memory and even hitting the limit number of threads where we can't start new ones.
