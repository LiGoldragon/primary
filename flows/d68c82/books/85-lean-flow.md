<!-- to-the-living:start -->
Presentation.{ «The lean flow» }

# The lean flow

## psyche-context › vision/flow.md

````markdown
## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.

A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.

Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

A metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.

A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow asleep is woken by an order, a question or the living's words and receives its whole queue, oldest first, in the first prompt, a result or a notice waiting there until a waking; a metaflow under refresh or waking queues what arrives until its successor or woken seat has started, while Flow keeps serving every other request. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.

What has been queued for an idle metaflow, the vision touching its topic among it, is injected with the request that wakes it, so the flow knows it as soon as it wakes.
A metaflow is not woken each time something touching its topic accumulates.

Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.

To the Nexus, a module's location is nothing but its registry entry.

The system prompt is not one thing: it is composed of modules of several types, and what a harness calls a skill overlaps with them.
Its anatomy is drawn up in ethos from a study of system prompts of every kind, each line placed by what it is and by the kind of guidance it belongs to.
Where the harness allows it, a part of a main flow's system prompt is the main flow's alone and is not passed down to its subagents.

Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.

## Long term: modules checked by hash

Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.

## Repository and context modules

The flow repository holds the machinery of the Flow Nexus and is a runtime repository.
Every context module lives outside it, the basic modules included, so that a change to a module causes no Nix rebuild.
The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.

## A session is named after its direct ancestor

## A replaced session is reaped by the refresh itself

Reaping belongs to the refresh event, not to a later sweep. A refreshed flow
takes the replaced end out of receiving messages, so a dead end is never
left registered and addressable.

Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

## Subflows replace the harness subagent facility

The harness subagent facility is replaced. It puts two flows into one
synchronous user interface and locks them both into a single main
flow. A subflow is instead an independent flow with its own system
prompt, which can reply to the successor of whoever it was meant to
answer; that makes the system asynchronous. Subflows run under their
own system prompts because they need different prompts.

## Subflows are created from the questions and requests a flow ends with

Creating a subflow is a routing job: whether there is already a flow
that should simply get this message or this question. A Field
Quaternary flow checks every question and every
request a flow ends with, and, according to the ending flow's
authority, spawns subflows given those questions and requests to
answer or fulfill.

## The requester holds only a request ID

The requester holds nothing of the subflow itself. It is assigned a
request ID, by which it asks later for status, asks for more detail
about what that subflow is doing, and sends the subflow messages
while it is alive. When the subflow is done, the requester receives a
message if it is still the flow in charge.
````

## psyche-context › vision/model-roles.md

````markdown
## Roles are explained by layer, not by model

Roles are explained by layer, not by model; one skill maps layer to model.

| Layer | Claude (Psyche) | OpenAI (Mind, Field) |
|---|---|---|
| Primary | Fable | Astra |
| Secondary | Opus | Sol |
| Tertiary | Sonnet | Luna |
| Quaternary | Haiku | Luna, low effort |

Every metaflow runs at medium effort, except the OpenAI Quaternary.

## Delegation ceiling

Each layer has a ceiling on what subflows it may launch. Conservative by
default: prefer the lower layer.

### OpenAI side

Luna launches only Luna. Sol is not
launched lightly; it is getting expensive. Astra launches Sol and Luna — try Luna first. Astra is main-flow only: no flow ever
launches an Astra subflow.

### Claude side

Sonnet launches Sonnet and Haiku. Opus launches
Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
ever launches a Fable subflow.

## One declaration sets the model everywhere

The model is declared once, as typed configuration in Flow, mutated only
through the meta wire. Skill variables carry that value by name into every
skill, launcher and brief. Nothing else holds a model name, so a launcher
never writes one by hand and no flow is started in a metaflow by accident.

## Native names use aspect, topic and layer

Every native main session is titled `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`.
The layer selects the configured model through the table above, so the
title names the layer, never the model.

Horizontal communication joins aspects at the same layer.
Vertical communication stays within one aspect and normally advances one layer
at a time.

Aspect, topic, layer, exact model identifier, Flow ID, and native binding
remain separate typed facts. The title grants none of the identity,
authority, availability, or routing those facts establish.

Horizontal routing selects the unique eligible cell in the target aspect at
the sender's layer.
Busy is still
eligible.
Multiple bindings for one cell are an unresolved conflict, never fanout.
Resolve the binding
immediately before each attempt.
````

### Proposal 1: Alternative A, the lean flow has no tools · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ ## The lean flow
+
+ A lean flow is a kind of flow with no tools and no messenger: it looks nothing up, and its response is its message back. When it wants to know more, it asks.

Ruling: land, amend, or reject.

### Proposal 2: Alternative B, the lean flow has whole tools · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ ## The lean flow
+
+ A lean flow is started with a system prompt of its own and the harness's whole tools, not stripped down. It is used only to respond with a presentation when given everything it needs, or to ask questions, which are its way of quoting or searching the file system, answered by another model.

Ruling: land, amend, or reject.

### Proposal 3: Addition, assembling the context · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ The supervising flow assembles all the variables and all the context for the one design presentation it asks of the lean flow.

Ruling: land, amend, or reject.

### Proposal 4: Alternative A, questions and designs only · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ A lean flow's response is a question or a design.

Ruling: land, amend, or reject.

### Proposal 5: Alternative B, a third kind: verdict · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ A lean flow's response is a question, a design or a verdict: its choice among options the supervising flow laid before it.

Ruling: land, amend, or reject.

### Proposal 6: Alternative C, a third kind: objection · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ A lean flow's response is a question, a design or an objection: that the context given cannot support the design asked.

Ruling: land, amend, or reject.

### Proposal 7: Alternative D, a third kind: assumptions · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ A lean flow's response is a question, a design or its assumptions: what it took as given where the context was silent.

Ruling: land, amend, or reject.

### Proposal 8: Addition, the exchange with the supervising flow · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ A lean flow goes back and forth a few times with a supervising flow that has tools. When the lean flow asks, the supervising flow finds things out for it and answers; the lean flow itself calls no subagent and sends no message.
```
+------------------+
| files and tools  |
+------------------+
         ^
         | finds out in
         |
+--------------------------------------+
| supervising flow, with tools         |
+--------------------------------------+
     |                         ^
     | sends context           | asks questions,
     | and answers             | returns designs
     v                         |
+--------------------------------------+
| lean flow, no tools, no messenger    |
+--------------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 9: Addition, what it is used for · psyche-context › vision/flow.md

  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.

+ A lean flow is used entirely for judgment and design, on Fable and on Astra. What can be automated, calling subagents and sending messages, is the supervising flow's, so the model spends itself on judgment.

Ruling: land, amend, or reject.

### Proposal 10: Alternative A, a lean start and a lean flow · psyche-context › vision/flow.md

  Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.
+ A lean start leaves parts of a harness's start out. A lean flow is a kind of flow, not a degree of start.

Ruling: land, amend, or reject.

### Proposal 11: Alternative B, lean flow names only the kind · psyche-context › vision/flow.md

- Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.
+ Flow is for starting flows cheaply: clean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.

Ruling: land, amend, or reject.

### Proposal 12: Addition, the open questions · mind-context › inquiry/lean-flow.md, a new file

+ ---
+ description: The lean flow's response, context, rounds, supervisor and way to the living are unsettled.
+ ---
+
+ - What is a lean flow's response made of, beyond a question and a design? The living named questions and designs "and maybe a third thing" he could not name. Candidates: a verdict among options laid before it; an objection that the context cannot support the design; the assumptions it took where the context was silent. Tried: past design requests answered by a lean flow, noting what the supervising flow had to ask again. Settled by his ruling on a candidate, or by the one kind of response the trials kept needing.
+ - What is a design in the response: presentation text, or datom proposals each a path and a diff? Tried: one past book design drawn both ways. Settled by which the supervising flow lands without rewriting.
+ - How does the supervising flow tell a question from a design in a response? Tried: a marker as the response's first word, and a datom variant. Settled by a response read correctly every time without a human.
+ - Which variables and context does the supervising flow assemble for the one design presentation, who chooses them, and where does the size stop? Tried: the requester's brief only, a module list set on the metaflow, and the supervising flow's own selection. Settled by a design as good with the smaller assembly as with the larger.
+ - How does a round end, and how many rounds does a lean flow get? Tried: ending when a response holds a design and no question, and a fixed cap with a last round that must design. Settled by the number of rounds past designs needed before a question stopped being new.
+ - Which supervising flow, at which layer and on which model, drives a lean flow? The records name the Secondary and "a supervising flow that does have tool calls"; vision/model-roles.md says no flow launches a Fable or an Astra subflow. Tried: a Secondary as supervisor starting the lean Fable or Astra through Flow, and a main flow as supervisor. Settled by his ruling whether a lean flow is a subflow.
+ - How does the lean flow's output reach the living, which has no messenger? Tried: the supervising flow relays the design as a presentation in its own name, and the response is delivered as the message with the lean flow as sender. Settled by his ruling on who the living sees.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
