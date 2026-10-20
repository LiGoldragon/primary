<!-- to-the-living:start -->
Presentation.{ «Flow's vision, second edition» }

# Flow's vision, second edition

## psyche-context › vision/flow.md

````markdown
## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt.

Flow is the Nexus that manages flows. A flow is one run of a metaflow; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.

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

### Proposal 1: Replace, front matter · psyche-context › vision/flow.md

```text
  ---
- description: Flow — the Nexus that launches, names, tracks and ends flows — or a voice, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
+ description: Flow — the Nexus that launches, names, tracks and ends flows — or a metaflow, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
  dependencies: [vision-nexus, vision-ethos]
  ---
```

### Proposal 2: Replace, a flow's model · psyche-context › vision/flow.md

  Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.

- A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.
+ A flow runs one model, linear and very limited, and the model is not always a language model: it may be a System 1 model, an audio model or a video model. An agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.

```
+--------------------------------------------+
| metaflow { Aspect Topic Layer }            |
+--------------------------------------------+
                     |
                     | continues through
                     v
+--------------------------------------------+
| flows, one run after another               |
+--------------------------------------------+
                     |
                     | runs
                     v
+--------------------------------------------+
| a model                                    |
+--------------------------------------------+
    |           |            |           |
    | may be    | may be     | may be    | may be
    v           v            v           v
+---------+ +----------+ +---------+ +---------+
| language| | System 1 | | audio   | | video   |
| model   | | model    | | model   | | model   |
+---------+ +----------+ +---------+ +---------+
```

### Proposal 3: Add, the flow that finishes tells the flow that needs to know · psyche-context › vision/flow.md

  Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
+
+ A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.

```
+--------------------+
| flow that finishes |
+--------------------+
          |
          | messages
          v
+--------------------+
| flow that needs    |
| to know            |
+--------------------+
          |
          | continues
          v
+--------------------+
| its own work       |
+--------------------+
```

### Proposal 4: Add, the simplified flow, in its own book 85 · psyche-context › vision/flow.md

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, and its response is its message.

### Proposal 5: Alternative A, replace, simplified in the starting line · psyche-context › vision/flow.md

- Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.
+ Flow is for starting flows cheaply: clean simplified flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.

### Proposal 6: Alternative B, replace, the starting line names no kind · psyche-context › vision/flow.md

- Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.
+ Flow is for starting flows cheaply: clean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.

### Proposal 7: Add, the flow ethos, in its own book 86 · psyche-context › vision/flow.md

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ A flow is specified whole, in Datom, by a domain-specific language in Ethos: its system prompt, its default context modules and its variations. The flow ethos holds the specification.

### Proposal 8: Add, the topic as an open enum, in its own book 87 · psyche-context › vision/flow.md

  Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
+
+ A topic is an open enum: the constant topics, core among them, are fixed, and the users and the machine extend the set with camelCase identifiers.

### Proposal 9: Add, Flow is a Nexus of three parts · psyche-context › vision/flow.md

  Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.
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

### Proposal 10: Add, traits in ethos, long term · psyche-context › vision/flow.md

  Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.
+
+ ## Long term: traits in ethos
+
+ Long term, every trait Flow uses is declared in ethos; short term, Flow goes without declared traits.

### Proposal 11: Add, a fresh flow starts with one prompt · psyche-context › vision/flow.md

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ A fresh flow starts with one prompt: every context module its metaflow is bound to is in it, none left to load afterwards.

### Proposal 12: Add, no Primary without its Secondary · psyche-context › vision/flow.md

  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+
+ Short term, a Primary is not started without its Secondary, and the Secondary starts first.

### Proposal 13: Add, a main flow manages · psyche-context › vision/flow.md

  Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.
+
+ A main flow manages; its subflows do the work.

### Proposal 14: Remove, the subflow sections, long term, in their own book 91 · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

- ## Subflows replace the harness subagent facility
-
- The harness subagent facility is replaced. It puts two flows into one
- synchronous user interface and locks them both into a single main
- flow. A subflow is instead an independent flow with its own system
- prompt, which can reply to the successor of whoever it was meant to
- answer; that makes the system asynchronous. Subflows run under their
- own system prompts because they need different prompts.
-
- ## Subflows are created from the questions and requests a flow ends with
-
- Creating a subflow is a routing job: whether there is already a flow
- that should simply get this message or this question. A Field
- Quaternary flow checks every question and every
- request a flow ends with, and, according to the ending flow's
- authority, spawns subflows given those questions and requests to
- answer or fulfill.
-
- ## The requester holds only a request ID
-
- The requester holds nothing of the subflow itself. It is assigned a
- request ID, by which it asks later for status, asks for more detail
- about what that subflow is doing, and sends the subflow messages
- while it is alive. When the subflow is done, the requester receives a
- message if it is still the flow in charge.

### Proposal 15: Add, one line of the concept, long term · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ ## Long term: subflows replace the harness subagent facility
+
+ Long term, the harness subagent facility is replaced by subflows: independent flows, each under its own system prompt, that answer asynchronously.

### Proposal 16: Alternative A, add, a refreshed flow starts with a presentation · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ The first act of a refreshed flow is a presentation of its context.

### Proposal 17: Alternative B, add, a refreshed flow starts with a proposal or a question · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ The first act of a refreshed flow is a proposal or a question for the living, so that no flow starts with nothing to do.

### Proposal 18: Alternative A, add, the handover warning at 128,000 tokens · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ A flow is told to write its handover at 128,000 tokens.

### Proposal 19: Alternative B, add, the handover warning at 200,000 tokens · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ A flow is told to write its handover at 200,000 tokens.

### Proposal 20: Alternative A, add, compaction is an emergency measure · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ Compaction is an absolute emergency measure: a compaction request is refused while the context is below a threshold.

### Proposal 21: Alternative B, add, some flows may compact · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ Some flows may be allowed to compact.

### Proposal 22: Add, the ephemeral flow · psyche-context › vision/flow.md

  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ An ephemeral flow is a continuous job flow that does not wake back up: it takes jobs while it runs, up to a ceiling on its context, and past the ceiling it is given no new job and another ephemeral flow takes it. With Claude the ceiling is 300,000 tokens, and the flow is wound down at 250,000.

### Proposal 23: Alternative A, add, an old flow is resumed if not too large · psyche-context › vision/flow.md

  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice.
+
+ A sleeping metaflow whose transcript is not too large is resumed on that transcript; a larger one is started fresh.

### Proposal 24: Alternative B, add, a woken flow is almost always fresh · psyche-context › vision/flow.md

  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice.
+
+ A flow woken for a metaflow is almost always a fresh flow, an old one only when the new input is literally the continuation of that topic.

### Proposal 25: Add, the flow id almost disappears from the chat · psyche-context › vision/flow.md

  Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
+
+ In the chat a flow is named by its metaflow, and the flow id almost disappears from it; the id is for the ledger and for finding the transcript.

### Proposal 26: Alternative A, replace, the flow id also in three words · psyche-context › vision/flow.md

- A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id.
+ A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. The flow id is also written in three words, which convert back to the hash.

### Proposal 27: Alternative B, add, the flow id stays the hash · psyche-context › vision/flow.md

  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id.
+ The flow id stays the hash; its word form waits for a later version.

### Proposal 28: Remove, an empty heading · psyche-context › vision/flow.md

  The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
- ## A session is named after its direct ancestor
-

### Proposal 29: Alternative A, remove, Flow as an example of ethos · psyche-context › vision/ethos.md

- ## Flow, a current best example
-
- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
-

### Proposal 30: Alternative B, replace, Ethos and Nexus are infrastructure · psyche-context › vision/ethos.md

- ## Flow, a current best example
+ ## Ethos and Nexus are infrastructure
-
- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+
+ Ethos and Nexus are basic infrastructure, not examples: the wood houses are built from. Chronos is the example project built with them, short term.

### Proposal 31: Replace, the Flow example in Ethos, a flow's address in place of a voice · psyche-context › vision/nexus.md

  Reading a Nexus's ethos alone shows every object and process on that path.

```text
- Library                                  ; what the three parts share
- []                                       ; imports: none
- [ FlowId.Integer                         ; types
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
-   Aspect.[ Psyche Mind Field ]
-   Layer.[ Primary Secondary Tertiary Quaternary ]
-   Event.[ Started Stopped ] ]
- []                                       ; kinds
- []                                       ; associations
-
- Signal                                   ; what Flow says, on its ordinary socket
- [ flow:[ FlowId Voice Event ] ]          ; imports from the Library
- [ Launch.{ Voice                         ; queries
-            Brief.String }
-   Report.{ FlowId Event } ]
- [ Launched.FlowId                        ; responses
-   Refused.[ NoCapsule
-             VoiceBusy.Voice ]
-   Reported ]
- []                                       ; types
-
- Operation                                ; what Flow does: one operation for every effect
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Start.{ Voice Capsule }                ; operations
-   Record.{ FlowId Event } ]
- [ Started.FlowId                         ; outcomes
-   Recorded
-   Failed.[ CapsuleRefused StoreRefused ] ]
- [ Capsule.{ Home.String                  ; types
-             Login.Vector<String> } ]
-
- Memory                                   ; what Flow remembers
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Flow.{ FlowId                          ; record types
-          Voice
-          State.[ Running Ended ]
-          Vector<Event> } ]
```

The library, shared by the three parts:

```ethos
+ Library
+ []
+ [ FlowId.Integer
+   Topic.String
+   Aspect.[ Psyche Mind Field ]
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Address.{ Aspect Topic Layer }
+   Event.[ Started Stopped ] ]
+ []
+ []
```

Signal, what Flow says:

```ethos
+ Signal
+ [ flow:[ FlowId Address Event ] ]
+ [ Launch.{ Address Brief.String }
+   Report.{ FlowId Event } ]
+ [ Launched.FlowId
+   Refused.[ NoCapsule
+             AddressBusy.Address ]
+   Reported ]
+ []
```

Operation, what Flow does:

```ethos
+ Operation
+ [ flow:[ FlowId Address Event ] ]
+ [ Start.{ Address Capsule }
+   Record.{ FlowId Event } ]
+ [ Started.FlowId
+   Recorded
+   Failed.[ CapsuleRefused StoreRefused ] ]
+ [ Capsule.{ Home.String
+             Login.Vector<String> } ]
```

Memory, what Flow remembers:

```ethos
+ Memory
+ [ flow:[ FlowId Address Event ] ]
+ [ Flow.{ FlowId Address
+          State.[ Running Ended ]
+          Vector<Event> }
+   Answer.[ Succeeded Failed ] ]
```

### Proposal 32: Replace, the Flow path in Datom, a flow's address in place of a voice · psyche-context › vision/nexus.md

```text
- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
- Succeeded                                             ; 4 Memory's answer to Operation
- Started.7                                             ; 5 Outcome
- Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
```

```datom
+ ; 1 Query, typed at the CLI, sent as signal
+ Launch.{ { Psyche core Primary }
+          «Draft the Nexus book» }
+ ; 2 Operation, from Signal's intend
+ Start.{ { Psyche core Primary }
+         { /home/li/primary [] } }
+ ; 3 the Change Operation hands Memory
+ Flow.{ 7 { Psyche core Primary } Running
+        [ Started ] }
+ ; 4 Memory's answer to Operation
+ Succeeded
+ ; 5 Outcome
+ Started.7
+ ; 6 Response, from Signal's answer, to the CLI
+ Launched.7
```

### Proposal 33: Replace, the vocabulary of a flow · mind-context › knowledge/vocabulary.md

- Flow: one run of a voice, from launch to end: its main thread and every subflow it starts; also the Nexus that manages flows.
+ Flow: one run of a metaflow, from launch to end: its main thread and every subflow it starts; also the Nexus that manages flows.

### Proposal 34: Add, what a flow's model may be · mind-context › inquiry/flow-model-kinds.md, a new file

+ ---
+ description: Which models a flow may run besides a language model, and what a flow needs of each, is unresolved.
+ ---
+
+ - What does "a System 1 model" mean for a flow? The living said a flow's model "could be a system one also". vision/system-one.md describes a System 1 model such as Jev, which makes decisions a program would hard-code. Is a System 1 flow that model run as a flow, or a program started by Flow? To try: start one Jev decision as a flow under a metaflow address, and see what Flow needs of it. It is settled when one System 1 flow runs under Flow with no change to the address.
+ - Which layer does a non-language model take? vision/model-roles.md says the layer decides the model, from a table of language models only. To try: a table row for each of the System 1, audio and video models, and a single column beside the table of language models. It is settled by the living's ruling on whether layer applies to them.
+ - What is the system prompt, transcript, sleep and refresh of an audio or video flow? Flow's vision describes these for a language model alone. To try: the audio model run as a flow that is given one request and answers it. It is settled by the list of Flow's behaviors that the audio flow needs.
+ - Is "linear and very limited" true of them? The living said the claim is not necessarily true. It is settled by the living's wording of what a flow is, once one non-language flow has run.

### Proposal 35: Add, how the finishing flow knows who needs to know · mind-context › inquiry/flow-finish-message.md, a new file

+ ---
+ description: How the flow that finishes learns which flow needs to know, and what happens when that flow is asleep, is unresolved.
+ ---
+
+ - How does the finishing flow learn which flow needs to know? To try: the requester names itself in the request; Flow keeps the waiter on the request; the finishing flow is given the waiting metaflow in its brief. It is settled by the one way that leaves no flow waiting on a timer in a trial of several waiting flows.
+ - Which request type is the message: a result or a notice? vision/flow.md says a result or a notice waits for a waking and does not wake. A flow waiting on another flow needs waking. To try: the message as an order, and as a result that wakes the waiter. It is settled by the living's ruling on whether a waiting flow is woken by a result.
+ - What of a flow that already waits on a timer? To try: list the flows in a sleep loop and send each the message of the flow it waits for. It is settled when none of them sleeps on a timer.

### Proposal 36: Add, how an ephemeral flow's ceiling is set · mind-context › inquiry/ephemeral-flow.md, a new file

+ ---
+ description: The ceiling of an ephemeral flow for Codex and for other models, and how the next flow takes over, are unresolved.
+ ---
+
+ - What is the ceiling for Codex? The living said "some kind of smaller figure for Codex". vision/flow.md names Codex thresholds only for refresh, not for this kind of flow. To try: the Codex warning point as the wind-down point. It is settled by the living's figure.
+ - How does the flow that is wound down hand its place to another? To try: the job queue held by Flow, so the next job simply goes to the new flow; a handover written by the old flow. It is settled by a run of jobs that crosses the ceiling with none lost.
+ - Is the ephemeral flow a kind beside the simplified flow, or a property of any flow? To try: the Illustrator, which takes jobs in one flow, defined with the property. It is settled by the living's ruling.

<!-- to-the-living:end -->
