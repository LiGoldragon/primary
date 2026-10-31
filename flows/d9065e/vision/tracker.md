# Tracker

## 2026-10-29 — The tracker: a Field Quaternary (Haiku) that keeps the task list, assigned metaflows on beads, checks the assigned flow is active, and notifies without bothering expensive flows
Context: the living, in the Psyche core Primary chat d9065e, after telling the Primary to scour its predecessor flows for what needs doing.

I was going to say we should use tertiary right now, or quaternary even, maybe. I don't know, but as a to-do manager, as a reminder, he would get these hard beats maybe every 20 minutes. His job would be to keep this to-do list, this list of tasks, and he could keep track of who's in charge of what in a file somewhere. I don't think it would be in a different repository, because this would be really noisy, right? It would go crazy if we tried to commit this in the primary repo.

He could use a separate repo for that, and it would be like this to-do list or this task tracker, the tracker. Maybe even we use a Luna Flow. I think Haiku has a million-token context, so we could let him run large because he would always stay hot, and Haiku is cheap.

We could even make it so that we would just basically train all of the meta flows to log their tasks with him and message him about, "Okay, here's this new task. Who is intended to be in charge of this task?" It could be more than one metaflow.

Periodically, Haiku would check to see, "Okay, this task is still marked as open." It's the beads, right? Can we modify the beads to assign meta flows for them? Haiku could check and see, "Oh, this metaflow is assigned as the bead that's supposed to be being worked on right now." He could check to see if that metaflow is active, and if not, then he could message that metaflow, right?

The bead could also indicate the creator of the bead, or maybe it's a field that talks about somebody that needs to be notified when this task progresses, blocks, or is considered to be done, right? He would just make sure that the system stays alive, that the tasks don't get abandoned, and that the tasks that are marked as done, he wouldn't bother. He would be really careful about bothering, especially expensive flows, right?

If he does so, he would first try through secondary, but he would always verify by checking the transcripts. He could use subagents for this, right? If he tried to message primary, he could check that his message went to secondary and that he would be allowed to message secondary. He would have a special role. He would be like the tracker, and this would be a field role, right?

We would use Haiku. Like I said, we can start interchanging models, I think. This Haiku model would run in field. He would be quaternary. He's very low in terms of model strength, but he can message secondaries. In a full fallback, if it's absolutely not possible and primary said that he absolutely must be notified of this beat, for example, I could keep talking, but maybe you're already seeing where I'm going with this.

## 2026-10-29 — Implement the tracker heartbeat without him; two trackers, Codex and Claude, waking together and deciding between them who notifies whom
Context: the living, same chat, his last message before the night.

Implement this tracker heartbeat system without my assistance, and use it (even if I don't come back and this is my last message until tomorrow) to vehemently work through the night: at least fix the Flow Nexus so that it behaves according to the things that we needed to do right now for the system to be really stable and reliable.

I see a new book now. Good job. Get this tracker thing going. You could even have two trackers: you could have a Codex and a Cloud tracker, just in case one of them fails. They could talk to each other and wake up at the same time, then talk to each other and decide who should be notified of what and who's going to send the messages. I think two of them would be really cool.
