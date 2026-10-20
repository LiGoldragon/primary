<!-- to-the-living:start -->
Presentation.{ «Flow's vision, third edition» }

# Flow's vision, third edition

### Proposal 1: Replace · psyche-context › vision/flow.md

```text
  ---
- description: Flow — the Nexus that launches, names, tracks and ends flows — or a voice, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
+ description: Flow — the Nexus that launches, names, tracks and ends flows — or a metaflow, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
  dependencies: [vision-nexus, vision-ethos]
  ---
```

### Proposal 2: Add · psyche-context › vision/flow.md

**Comment** A fresh flow's start is one model call, however many prompts the harness sees.

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ A fresh flow starts with every context module its metaflow is bound to, none left to load afterwards: much of it in its system prompt, the rest in its first prompt, or in as many prompts as it takes, sent one right after another, so that its start is one model call.

```
+------------------------------------------+
| a fresh flow's start: one model call     |
+------------------------------------------+
        |                        |
        | carries in             | carries in
        v                        v
+------------------+   +-------------------+
| its system       |   | its first prompt, |
| prompt: much of  |   | or several sent   |
| its modules      |   | one after another |
+------------------+   +-------------------+
```

### Proposal 3: Add · psyche-context › vision/flow.md

**Comment** The short-term line stays; this adds where the Primary is going.

  Short term, a Primary is not started without its Secondary, and the Secondary starts first.
+
+ Long term, a Primary is a simplified flow, used only to render judgment: guiding a design or posing questions.

### Proposal 4: Replace · psyche-context › vision/flow.md

**Comment** A flow past its threshold writes no handover and is told nothing; Flow simply stops sending to it. The threshold belongs to the model, not the layer. The last sentence of the refresh line is removed: the hooks line above already says every harness event reaches Flow through the CLI, and the flow-id line says every call is identified by the calling process.

- Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.
+ Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow past its context threshold is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+ A flow is refreshed when its context passes its model's threshold: it is told nothing and writes no handover; it is given no new message, Flow keeps the metaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Each model's threshold is configured in Flow; an OpenAI model's is lower than a Claude model's.

```
+------------------------------------------+
| Flow                                     |
+------------------------------------------+
        |                        |
        | sends no new           | keeps the next
        | message to             | messages for
        v                        v
+------------------+   +-------------------+
| the flow past    |   | the metaflow's    |
| its model's      |   | next flow         |
| threshold        |   +-------------------+
+------------------+
        |
        | is replaced
        | as it goes idle
        v
+------------------+
| reaped in the    |
| same event       |
+------------------+
```

### Proposal 5: Add · psyche-context › vision/flow.md

**Comment** A presentation is what a flow gives in place of a handover, at its first turn and at the end of every task from the psyche. The alternatives share all their text; they differ in one sentence. Alternative 1 leaves what a presentation holds to the flow's context and prompt. Alternative 2 adds that a flow's first presentation always carries a proposal or a question for the living, so that no flow starts with nothing to do.

```
+-------------+ +-------------+ +-------------+
| a flow's    | | a task from | | an update   |
| first turn  | | the psyche  | | from a flow |
+-------------+ +-------------+ +-------------+
       |               |               |
       | ends in       | ends in       | needs no
       v               v               v
+---------------------------------------------+
| a presentation                              |
+---------------------------------------------+
       ^                               ^
       | shapes                        | shapes
       |                               |
+-------------+                 +-------------+
| its loaded  |                 | its prompt  |
| modules     |                 |             |
+-------------+                 +-------------+
```

**Alternative 1**

  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.
+
+ A flow gives a presentation, a response that could fit into a book, whenever it is given significant new context to consider: its first turn ends in one, and so does every task, goal or question that originates in the psyche. A message from another flow that only updates it needs no full presentation. A presentation takes its form from the context modules the flow was loaded with and from its prompt, the one string given to that flow alone, which is no context module.

**Alternative 2**

  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.
+
+ A flow gives a presentation, a response that could fit into a book, whenever it is given significant new context to consider: its first turn ends in one, and so does every task, goal or question that originates in the psyche. A message from another flow that only updates it needs no full presentation. A presentation takes its form from the context modules the flow was loaded with and from its prompt, the one string given to that flow alone, which is no context module. A flow's first presentation carries a proposal or a question for the living, so that no flow starts with nothing to do.

### Proposal 6: Add · psyche-context › vision/flow.md

**Comment** The emergency line stays: below the threshold a compaction request is still refused. This adds that a flow at continuous work may compact, and that its compaction is a signal to look into.

  Compaction is an absolute emergency measure: a compaction request is refused while the context is below a threshold.
+
+ A flow that keeps working without being given more work may compact. Its compaction raises a warning, and a flow investigates why it worked so long, so that the trouble is brought to the living or Psyche reconsiders the approach and gives guidance.

```
+-----------------------------+
| a flow at continuous work   |
+-----------------------------+
              |
              | compacts, raising
              v
+-----------------------------+
| a warning                   |
+-----------------------------+
              |
              | starts
              v
+-----------------------------+
| an investigation            |
+-----------------------------+
        |               |
        | brings it to  | asks for guidance
        v               v
+-------------+ +-------------+
| the living  | | Psyche      |
+-------------+ +-------------+
```

### Proposal 7: Replace · psyche-context › vision/subflows.md

**Comment** This concept has two approved wordings, and one module holds it, so the choice is between them here. The landed line says the answers come back as messages. Alternative 1 keeps it and adds the two things the second wording says: each answering flow runs under its own system prompt, and the answers come back asynchronously. Alternative 2 takes the second wording whole, which names subflows and drops the questions and requests. Rejecting both keeps the line as it stands.

**Alternative 1**

  ## Long term: actual flows replace the harness subagent tool

- Long term, a flow does not call a subagent tool. Its questions and requests are answered and fulfilled by actual flows, and the answers return to it as messages.
+ Long term, a flow does not call a subagent tool. Its questions and requests are answered and fulfilled by actual flows, each under its own system prompt, and the answers return to it asynchronously, as messages.

**Alternative 2**

  ## Long term: actual flows replace the harness subagent tool

- Long term, a flow does not call a subagent tool. Its questions and requests are answered and fulfilled by actual flows, and the answers return to it as messages.
+ Long term, the harness subagent facility is replaced by subflows: independent flows, each under its own system prompt, that answer asynchronously.

### Proposal 8: Add · mind-context › inquiry/flow-model-kinds.md, a new file

**Comment** The open questions of the line that a flow's model may be a System 1, audio or video model.

+ ---
+ description: Which models a flow may run besides a language model, and what a flow needs of each, is unresolved.
+ ---
+
+ - What is a System 1 flow? vision/system-one.md describes a System 1 model, such as Jev, that makes the decisions a program would otherwise hard-code. Is a System 1 flow that model run as a flow, or a program Flow starts? To try: one Jev decision started as a flow under a metaflow address. It is settled when one System 1 flow runs under Flow with no change to the address.
+ - Which layer does a non-language model take? vision/model-roles.md maps layer to model in a table of language models only. To try: a row for each of the System 1, audio and video models, and a single column beside the table. It is settled by the ruling on whether layer applies to them.
+ - What are the system prompt, transcript, sleep and refresh of an audio or video flow? vision/flow.md describes them for a language model alone. To try: an audio model run as a flow that is given one request and answers it. It is settled by the list of Flow's behaviours the audio flow needs.
+ - Is a flow of a non-language model linear and very limited, as vision/flow.md says of every flow? It is settled by the wording of what a flow is, once one non-language flow has run under Flow.

### Proposal 9: Add · mind-context › inquiry/flow-finish-message.md, a new file

**Comment** The open questions of the line that the flow that finishes messages the flow that needs to know.

+ ---
+ description: How the flow that finishes learns which flow needs to know, and what happens when that flow is asleep, is unresolved.
+ ---
+
+ - How does the finishing flow learn which flow needs to know? To try: the requester names itself in the request; Flow keeps the waiter on the request; the finishing flow is given the waiting metaflow in its brief. It is settled by the one way that leaves no flow waiting on a timer in a trial of several waiting flows.
+ - Which request type is the message: a result or a notice? vision/flow.md says a result or a notice waits for a waking and does not wake. A flow waiting on another flow needs waking. To try: the message as an order, and as a result that wakes the waiter. It is settled by the ruling on whether a waiting flow is woken by a result.
+ - What of a flow that already waits on a timer? To try: list the flows in a sleep loop and send each the message of the flow it waits for. It is settled when none of them sleeps on a timer.

### Proposal 10: Add · mind-context › inquiry/ephemeral-flow.md, a new file

**Comment** The open questions of the ephemeral flow line.

+ ---
+ description: The ceiling of an ephemeral flow for a Codex model, how the next flow takes over, and what kind of flow it is, are unresolved.
+ ---
+
+ - What are the ceiling and the wind-down point of an ephemeral flow on a Codex model? vision/flow.md gives them for Claude alone, 300,000 and 250,000 tokens. To try: the Codex refresh threshold as the wind-down point. It is settled by the figure configured in Flow.
+ - How does the flow that is wound down hand its place to another? To try: the job queue held by Flow, so the next job simply goes to the new flow. It is settled by a run of jobs that crosses the ceiling with none lost.
+ - Is the ephemeral flow a kind beside the simplified flow, or a property of any flow? To try: the Illustrator, which takes all waiting jobs in one flow, specified with the property in the flow ethos. It is settled by the ruling on which it is.

<!-- to-the-living:end -->
