Presentation.{ «Flow» }

Flow is the program that starts flows, tracks them, and ends them. A flow is one session, and its life runs from a launch, through working and idle, to a refresh or a reaping. Every proposal below is one edit to one context module. Answer with the number, and with "1" or "2" where there are two texts.

**1. Define a flow**
Vision, module vision-flow. Edit.
> A flow is one session. A new context is a new flow. A flow is either working or idle. A subflow is a flow, and its parent counts as active while it waits.

Rests on: 3 Oct, 26 Aug.

**2. Launch by kind and goal**
Vision, module vision-flow. Edit.
> Every kind of flow is declared ahead of time. A launch names one kind and gives a small description of the goal. Flow has one full Start call and shorthands for the common cases.

Rests on: 26 Sep, 25 Sep, 17 Sep.

**3. Identity comes from code**
Vision, module vision-flow. Edit.
> Code gives a flow its identity as it starts. The model never claims or checks it. To him it is written as three words that convert back to the real one.

Rests on: 24 Sep, 3 Oct.

**4. A subflow's identity**
Vision, module vision-flow. Edit. His records pull two ways.
Text 1:
> A subflow carries its parent's identity, put in by Flow at launch, and opens no lane of its own.

Text 2:
> A subflow is a flow and carries its own identity.

Rests on: 31 Aug (text 1); text 2 from "a subflow also is a flow", 26 Aug.

**5. Voices**
Vision, module vision-flow. Edit.
> A voice is an aspect paired with a layer. Flows are addressed by voice, aspect first. The real identity is kept for the record, and the voice registry never holds it.

Rests on: 3 Oct, 2 Oct.

**6. Hooks, never polling**
Knowledge, module knowledge-flow. Edit.
> Hooks report every state change to Flow. Nothing polls. The end-of-reply hook sends the reply to Flow.

Rests on: 30 Sep, 19 Sep. The start hook marks working and the end hook marks idle is my fill between his words.

**7. Who delivers messages**
Vision, module vision-flow. Edit.
Text 1:
> Flow starts, refreshes, ends and delivers messages.

Text 2:
> Flow only starts, refreshes and ends flows. The Message Nexus delivers.

Rests on: 24 Sep (text 1); 17 Sep "use the message nexus" (text 2).

**8. Who reaps after a refresh**
Operation, module trial-reaping. Edit.
Text 1:
> A refresh reaps its predecessor on its own. The judge and the Field reap only flows that have no successor.

Text 2:
> The judge decides, and the Field reaps every time.

Rests on: 19 Sep (text 1); 18 Sep (text 2).

**9. When a flow refreshes**
Operation, module trial-succession. Edit.
Text 1:
> Every model refreshes at the same point. Below 15% of context used, a flow does not refresh.

Text 2:
> Each model has its own refresh point. Below 15% of context used, a flow does not refresh.

Rests on: 14 Sep, "at 60%"; 16 Sep, "30% as a Fable agent"; 15 Sep for the floor.

**10. Who receives during a changeover**
Operation, module trial-succession. Edit.
Text 1:
> The old flow stops receiving first. Messages wait until the new flow is ready.

Text 2:
> Both flows receive until the old one logs out to the new one.

Rests on: 24 Sep (text 1); 14 Sep (text 2).

**11. Refresh fails**
Operation, module trial-succession. Edit. One record forbids compaction and the other allows it.
Text 1:
> If a refresh fails, the flow does not compact. The old flow is woken.

Text 2:
> If a refresh fails, the flow may compact as a fallback.

Rests on: 15 Sep, the old flow is woken if its successor fails to start; the compaction records are in the later questions.

**12. What Flow never does**
Vision, module vision-flow. Edit.
> Flow does no sandboxing. It locks sessions, never files. Transcripts and memory are not where it lives.

Rests on: 3 Oct, 17 Sep, 19 Aug.
