Presentation.{ «Flow» }

How a flow lives and ends, and Flow, the long-running program (a Nexus) that runs flows. Each design line rests on his words, quoted with their date. Lines marked **Proposed** fill between his words, and he can strike them.

## 1. What he wants

### A flow

A flow is one session. A new context is a new flow.

> "Yeah Flow is obviously a session so when we restart the whole context, that's a new Flow. It's a different context." (3 Oct)

A flow is either working or idle.

> "when the flow isn't working then it's idle, isn't it?" (3 Oct)

A subflow is a flow, and its parent counts as active while it waits.

> "a subflow also is a flow" … "a flow running a subflow is still active through its subflows." (26 Aug)

### Flow, the program

Flow sets up and starts flows.

> "Its flow, which will setup and start a model flow, with its own working directory, system prompt and training files, and its instruction prompt." (18 Aug)

First it has to launch flows and know each one's state through hooks (small triggers in the model's harness that report events).

> "Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow." (2 Oct)

Flow drives the terminal layer, and nobody touches it by hand.

> "Basically, Flow is in charge of herder. I shouldn't interact with it directly." (18 Sep)

### Starting flows

Flow has one full Start call, plus shorthands for the common cases.

> "It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed." (25 Sep)

Every kind of flow is declared ahead of time. A launch only names one of them and gives it a goal.

> "We should have a list of flows all programmed with their datom configuration. That's one of the inputs it gets, fed into a new flow, plus addendum things…" (26 Sep)

(A datom is our small structured text form.)

> "there's basically no argument to give except a small description of the goal" (17 Sep)

A flow is a record, and its role is one of its fields.

> "the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice." (3 Oct)

Any flow may call Flow. Flow learns who called from the calling process, and a flow refreshing itself needs no other authority.

> "Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it." (24 Sep)

A flow starts from a single prompt, kept lean. When he asks for a flow, it exists by the time he comes back.

> "All that matters is that everything comes in as one block." (24 Sep)

> "if I ask for a new flow, when I come back there's a new flow." (2 Oct)

### Identity given by code

Code gives a flow its identity as the flow starts. The model never claims or checks it.

> "We should not make it the subflow's job to claim an ID. That should be done for the flow as it started. … This could easily be done by code." (24 Sep)

For him, the identity is written as three words that convert back to the real one: "converting it into words because then we can go back." He approved that shape.

> "This looks perfect. That's exactly the user interface I was looking for." (3 Oct)

Subflows don't open lanes of their own.

> "I don't want subflows to start creating their own lanes. They just use their parents." (31 Aug)

**Proposed:** Flow puts the parent's identity into each subflow's launch, so a subflow never looks it up.

### Names, voices and the two registries

A session is named by aspect and layer, aspect first, followed by its three words.

> "I [also] want the session names to be by aspect and layer only … the aspect first." (3 Oct)

A voice is an aspect paired with a layer. Flows are addressed by voice. The real identity is kept for the record.

> "Voices not seats, right?" (3 Oct)

> "I'd like flows to be addressable by their continuous name … They're just for accounting or for the ledger, the archive side of things" (2 Oct)

There are two registries.

> "The true registry with the actual IDs … Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice, the current flow for that voice" (3 Oct)

Short jobs run as side flows. Each one ends, and anything sent to it afterwards goes back to the sender.

> "They're sort of side flows. They're not long-lived. … Whatever message was sent to it goes back, I guess, to whoever sent it, with the notice that this flow has ended" (2 Oct)

State is kept in Flow's records, never in pane titles.

> "using header pane titles for storing data is like you should just use a registry for that … That's what Flow's database should be." (24 Sep)

Flow locks sessions.

> "No, Flow locks the sessions and [Orchestrate] locks the files. Those are different things." (3 Oct)

### Working, idle, and hooks

Hooks report every state change to Flow. Nothing polls.

> "Essentially we want to avoid polling, which means we're going to make this hook-based." (30 Sep)

A hook at the end of the last reply sends that reply to Flow.

> "We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it." (19 Sep)

**Proposed:** the start hook marks a flow working, and the end-of-reply hook marks it idle.

### Refresh of a big context

A big context gets refreshed, and an abandoned flow gets reaped (closed down).

> "Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped." (26 Sep)

The threshold triggers it, not anyone's judgement.

> "When a model reaches a certain context window, whoever is in charge of refreshing should get a message that some flow needs to be refreshed." (26 Sep)

There is a floor below which a flow does not refresh.

> "Let's not restart a flow that only has less than 15% of its context used" (15 Sep)

The new flow forms its own view of the old one from the old transcript. A tool fetches the handover. Nothing is copied into a file.

> "the new flow needs to make its own view of the old" (21 Aug)

> "The handoff is in the transcript and the tool gets it from that" (24 Sep)

The refresh prompt is put together by a program.

> "Refresh yourself with a fresh key in the user prompt, programmatically injected, not output by an agent" (18 Sep)

### Succession

The new flow starts receiving and the old one stops, in a single step.

> "A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived." (24 Sep)

> "it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it." (24 Sep)

Messages wait for the new flow, and replies reach it.

> "The Messenger would keep the messages until you have a new delivery point" (21 Sep)

> "if the message does go out to its destination, then the reply will go to the new flow." (19 Sep)

The old flow is woken only if its successor fails to start.

> "it would get woken up by Flow if the new flow was unable to start" (15 Sep)

### Reaping and archiving

The refresh reaps the flow it replaces.

> "when we refresh a flow, it takes out that end from receiving messages, right?" (17 Sep)

Archiving starts as a script and becomes a feature of Flow.

> "Let's put that into a script and then into Flow as a feature to archive their session files." (18 Sep)

The reaper is forensic: it reports what it reaped, suspects, recommends, saved and archived.

> "the Reaper can see if something went wrong or if something was left unfinished. He's in the perfect position to do that" (18 Sep)

An archive keeps only the parts that matter.

> "just keeping the important parts of the exchanges, like the main responses and the most important parts of the prompts and the final responses" (13 Sep)

**Proposed:** reaping closes the pane, removes the voice route and records the flow as retired. The transcript stays.

### Configuration

Flow keeps its configuration in its own database. That includes a registry of where each context module is located, kept up to date over a separate channel he calls the meta socket.

> "It lives in its own database and its memory." (3 Oct)

### What Flow never does

> "No, Flow doesn't do any sandboxing for now" (3 Oct)

> "Why are we talking about orchestrate here? There's no reason to talk about orchestrate." (3 Oct)

> "It's not going to be where the memory lives" (17 Sep)

Flow doesn't lock files; Orchestrate, the file-locking program, does. Transcripts belong to "obviously another nexus" (19 Aug).

## 2. What exists today

Witnessed. Flow 0.23 runs as a stable and a next service, and Start, Replace and Retire exist in it. No seat is launched through Start. Seats are started by hand with launcher scripts, and each claims its own number. Retire was refused twice: Flow did not know the flow, and the messenger's wrapper wants eight hand-typed arguments. The seat was closed by hand. No harness hook calls Flow. Messages still go through the older hand-run messenger. Titles carry aspect, model and an old-style code, not layer and three words. Subflows receive no identity. Successor launches were refused by the launcher's guard, and some retired seats kept running.

Supposed: Flow's registry holds few of the live seats. That would explain why Retire cannot find them and why Replace never ran in earnest.

## 3. Questions

**1. Who delivers messages?** Say you tell a flow to send a note to the Mind voice.

> "I want to be able to start flows, stop flows, and send messages with Flow" (24 Sep)

> "flow is to start or refresh a flow" and "no, message, not flow-send. use the message nexus!" (17 Sep)

Answer 1 if Flow delivers messages too. Answer 2 if Flow only starts, refreshes and ends flows, and the Message Nexus (the separate message-delivery program) delivers.

**2. Who reaps the old flow after a refresh?** Say a Mind flow is refreshed at its limit.

> "Whenever you refresh a flow, you need to reap the ancestor, right?" (19 Sep)

> "You could have a field old Opus that takes care of judging if something is dead … and the field Luna can now reap" (18 Sep)

Answer 1 if the refresh reaps its predecessor on its own, and the judge and the Field (the aspect that keeps things running) reap only flows with no successor. Answer 2 if the judge decides and the Field reaps every time.

**3. When does a flow refresh?** Say a Fable flow sits at 35% of its context.

> "At a certain maximum, at 60%, the flow basically has to change over" (14 Sep)

> "start when you're getting to 30% of your context as a Fable agent" (16 Sep)

Answer 1 for one refresh point for every model. Answer 2 for one per model.

**4. During a changeover, who receives messages?** Say a message arrives while the new flow is starting.

> "messages essentially get passed on to both the new and the old flow until the old flow logs out to the new flow." (14 Sep)

> "The old seat stops receiving first. That's how we get a lock." (24 Sep)

Answer 1 if the old flow stops receiving first. Answer 2 if both receive until the old one logs out.
