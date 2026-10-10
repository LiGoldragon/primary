# Flow context injection

## A hook controls what is injected in the prompt and what goes through messaging; queued context rides in with the next message so a flow need not wake for every accumulation

Context: relayed by Mind d66c26 from flows/d66c26/vision/flow-context-injection.md.

> I'd like some of the flows, or maybe all of the flows, once we get a hook in place, where we control what gets injected in the prompt and what goes through messaging. Essentially we can inject more stuff along with the messages that are coming into a certain flow. We can use that opportunity to inject a bunch of other stuff that has been queued in preparation for that particular flow to be woken up, so that it would know all of this as soon as it woke up. Yet we wouldn't have to wake up every time some accumulation of vision or whatever that touches its lanes or its topics is coming into the system.

-- psyche, STT, 2026-10-04, relayed by d66c26.
