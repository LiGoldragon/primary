<!-- to-the-living:start -->
Presentation.{ «Flow's vision» }

# Flow's vision

## psyche-context › vision/flow.md

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

### Proposal 1: Addition · psyche-context › vision/flow.md

  Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.
+
+ Flow is a Nexus of three parts, each its own ethos specification: its signal, its operation and its memory.
+ Short term, Flow runs as a prototype derived from that ethos; long term, it is the Nexus itself. Whatever is short term is marked, since it may go stale.

```
+------------+
| Flow ethos |
+------------+
      |
      +-- specifies -->+------------+
      |                | Signal     |
      |                +------------+
      |                 |asks  ^replies
      |                 v      |
      +-- specifies -->+------------+
      |                | Operation  |
      |                +------------+
      |                 |changes ^answers
      |                 v        |
      +-- specifies -->+------------+
                       | Memory     |
                       +------------+
```

### Proposal 2: Addition · psyche-context › vision/flow.md

  Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.
+
+ ## Long term: traits in ethos
+
+ Long term, every trait Flow uses is declared in ethos; short term, Flow goes without declared traits.

### Proposal 3: Addition · psyche-context › vision/flow.md

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ A flow's definition, and a subagent's, is a data object specified in ethos and written in datom: its role, the modules composed into it, and its brief.
+ A fresh flow starts with one prompt: every context module its metaflow is bound to is in it, none left to load afterwards.

### Proposal 4: Addition · psyche-context › vision/flow.md

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ Short term, a Primary is not started without its Secondary, and the Secondary starts first.

### Proposal 5: Addition · psyche-context › vision/flow.md

  answer the successor of whoever it was meant to answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.
+
+ A main flow manages; its subflows do the work.

### Proposal 6: Alternative A, addition · psyche-context › vision/flow.md

  own system prompts because they need different prompts.
+
+ A subflow is not the same kind of flow as a main flow: its kind depends on its use.

### Proposal 7: Alternative B, addition · psyche-context › vision/flow.md

  own system prompts because they need different prompts.
+
+ A main flow and its subflows are essentially the same thing; they differ in their training.

### Proposal 8: Alternative A, addition · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ The first act of a refreshed flow is a presentation of its context.

### Proposal 9: Alternative B, addition · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ The first act of a refreshed flow is a proposal or a question for the living, so that no flow starts with nothing to do.

### Proposal 10: Alternative A, addition · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ A flow is told to write its handover at 128,000 tokens.

### Proposal 11: Alternative B, addition · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ A flow is told to write its handover at 200,000 tokens.

### Proposal 12: Alternative A, addition · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ Compaction is an absolute emergency measure: a compaction request is refused while the context is below a threshold.

### Proposal 13: Alternative B, addition · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ Some flows may be allowed to compact.

### Proposal 14: Alternative A, addition · psyche-context › vision/flow.md

  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice.
+
+ A sleeping metaflow whose transcript is not too large is resumed on that transcript; a larger one is started fresh.

### Proposal 15: Alternative B, addition · psyche-context › vision/flow.md

  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice.
+
+ A flow woken for a metaflow is almost always a fresh flow, an old one only when the new input is literally the continuation of that topic.

### Proposal 16: Addition · psyche-context › vision/flow.md

  Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
+
+ In the chat a flow is named by its metaflow, and the flow id almost disappears from it; the id is for the ledger and for finding the transcript.

### Proposal 17: Alternative A, addition and removal · psyche-context › vision/flow.md

- A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id.
+ A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. The flow id is also written in three words, which convert back to the hash.

### Proposal 18: Alternative B, addition · psyche-context › vision/flow.md

  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id.
+ The flow id stays the hash; its word form waits for a later version.

### Proposal 19: Alternative A, removal · psyche-context › vision/flow.md

- ## A session is named after its direct ancestor
-

### Proposal 20: Alternative B, addition · psyche-context › vision/flow.md

  The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
- ## A session is named after its direct ancestor
+ ## A session is named after its direct ancestor
+
+ A new flow is named after its direct ancestor, the flow it succeeds; the future cannot be named.

### Proposal 21: Alternative A, removal · psyche-context › vision/ethos.md

- ## Flow, a current best example
-
- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
-

### Proposal 22: Alternative B, addition and removal · psyche-context › vision/ethos.md

- ## Flow, a current best example
+ ## Ethos and Nexus are infrastructure
-
- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+
+ Ethos and Nexus are basic infrastructure, not examples: the wood houses are built from. Chronos is the example project built with them, short term.

<!-- to-the-living:end -->
