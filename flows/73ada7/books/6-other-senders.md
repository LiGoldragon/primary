<!-- to-the-living:start -->
Presentation.{ «Who may send besides a voice» }

## The case

Message carries a request from one flow to another, and Flow checks the route with the Sender. In f5a6e9's buildable Flow design the Sender is a Metaflow and nothing else: `Sender.Metaflow`, where a Metaflow is one of the three aspects, Psyche, Mind or Field, carrying its topic, layer, state, past and queue. Flow answers Identify.Process with that metaflow or with Unidentified.Process. A side flow doing a job runs in no metaflow. Message's design refuses it with Refused.Unidentified.Process, for now, and leaves it as an open fork. The next Message and Flow are in development, none of it in production. vision-flow already rules that a side flow is a job, not a voice, gone when its mission is done, and that a message sent to it afterwards returns to its sender with notice that the flow has ended. What is open is whether a side flow may send at all, and in whose name its replies come back. That under the present Sender a side flow has no name to send in is this flow's reading of the Flow design.

## Distillation

### D1. Who sends besides a voice, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, the paragraph at line 22, in the section «Starting flows». It opens "A voice is an aspect carrying a rank, `Psyche.Primary`" and closes "a message sent to it after that returns to its sender with notice that the flow has ended." Nothing is removed; one sentence is added after the paragraph's last sentence.

**Option (a), only a voice sends, for now.**

Added: For now only a voice sends; a request from a side flow is refused.

Rests on: Message's design section 6 and fork F11 (flows/73ada7/reports/build/message-design.md:327-330 and 607-608), unruled; flows/8475a9/vision/messenger.md:7 (2026-10-05), on naming a message's originator by voice only; flows/b7ba00/vision/messaging.md:29 (2026-09-26), on the sender being Psyche Primary, Psyche Secondary and so on, for now. Those two records name senders by voice; reading them as refusing every other sender is this flow's inference.

**Option (b), a voice brokers for a side flow.**

Added: A side flow sends through a voice that brokers for it; the request carries that voice as its sender, and a reply returns to that voice.

Rests on: flows/8475a9/notion/messenger.md:7 (2026-10-05), a notion, on a voice acting as broker for specialized jobs because they could end before the message reaches them; flows/8475a9/vision/messenger.md:15 (2026-10-05), on not every message coming from a voice. Which voice brokers for which job is not said in either record; that the present `Sender.Metaflow` (flows/f5a6e9/reports/flow-buildable-design.md:81) would stand unchanged under this option is this flow's reading.

**Option (c), a side flow sends in its own name.**

Added: A side flow sends in its own name; a reply that reaches it after its mission is done returns to the one replying with notice that the flow has ended.

Rests on: flows/8475a9/vision/messenger.md:15 (2026-10-05), on not every message coming from a voice; the approved sentence itself, psyche-skills/skills/vision-flow.md:22 (landed by 2026-10-07); flows/3ec648/vision/voices.md:9 (2026-10-02), on a message sent to an ended side flow going back to whoever sent it with that notice. That Flow's Sender and Identify.Process (flows/f5a6e9/reports/flow-buildable-design.md:81 and 423-428) would then need a way to name a side flow, which a Metaflow cannot, is this flow's inference.

**Ruling D1.** (a) Only a voice sends. (b) A voice brokers. (c) A side flow sends in its own name. (d) Amend, by line.

## Voice

One choice. A side flow does a job and ends, so who may it send as? Message's design refuses it for now. On the 5th you said not every message will come from a voice, and turned over a voice brokering for jobs that could end before a message reaches them. vision-flow already sends a message to an ended side flow back with notice. A refuses side flows for now; B has a voice send for them and take their replies; C lets them send as themselves, with late replies bounced with that notice. Which one? This flow's reading: C needs Flow's Sender to name something that is not a metaflow.
<!-- to-the-living:end -->
