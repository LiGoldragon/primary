<!-- to-the-living:start -->
Presentation.{ «Idle panes stay open» }

# Idle panes stay open

## psyche-context › vision/flow.md

````markdown
## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt.

Flow is the Nexus that manages flows. A flow is one run of a metaflow; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

Flow is for starting flows cheaply: clean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.

A flow runs one model, linear and very limited, and the model is not always a language model: it may be a System 1 model, an audio model or a video model. An agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.

A topic is an open enum: the constant topics, core among them, are fixed, and the users and the machine extend the set with camelCase identifiers.

Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

A metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.

A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. The flow id stays the hash; its word form waits for a later version. Long term, the flow id is also written in three words, which convert back to the hash. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.

In the chat a flow is named by its metaflow, and the flow id almost disappears from it; the id is for the ledger and for finding the transcript.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow asleep is woken by an order, a question or the living's words and receives its whole queue, oldest first, in the first prompt, a result or a notice waiting there until a waking; a metaflow under refresh or waking queues what arrives until its successor or woken seat has started, while Flow keeps serving every other request. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.

A flow woken for a metaflow is almost always a fresh flow, an old one only when the new input is literally the continuation of that topic.

What has been queued for an idle metaflow, the vision touching its topic among it, is injected with the request that wakes it, so the flow knows it as soon as it wakes.
A metaflow is not woken each time something touching its topic accumulates.

Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.

A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.

A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.

A flow is specified whole, in Datom, by a domain-specific language in Ethos: its system prompt, its default context modules and its variations. The flow ethos holds the specification.

Short term, a Primary is not started without its Secondary, and the Secondary starts first.

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

## A replaced session is reaped by the refresh itself

Reaping belongs to the refresh event, not to a later sweep. A refreshed flow
takes the replaced end out of receiving messages, so a dead end is never
left registered and addressable.

Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

Compaction is an absolute emergency measure: a compaction request is refused while the context is below a threshold.

An ephemeral flow is a continuous job flow that does not wake back up: it takes jobs while it runs, up to a ceiling on its context, and past the ceiling it is given no new job and another ephemeral flow takes it. With Claude the ceiling is 300,000 tokens, and the flow is wound down at 250,000.
````

### Proposal 1: psyche-context › vision/flow.md

**Comment** Closing a pane when its flow is done is long term; for now a flow whose turn ends stays in its pane.

```
+------------------------------+
| turn ends, queue empty       |
+------------------------------+
   | short term:      | long term:
   | stays            | closes
   v                  v
+------------+   +-------------+
| pane open  |   | pane gone   |
| flow awake |   | flow asleep |
+------------+   +-------------+
   | pane closed      ^
   | by hand: sleeps  |
   +------------------+
```

- A metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.
+ Long term, a metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.
+ Short term, a flow whose turn ends stays in its pane; it sleeps only when its pane is gone.

Ruling: land, amend, or reject.

### Proposal 2: flow › crates/flow-nexus/src/waking.rs

**Comment** The idle-close path: with the queue empty and the lock free, a resting seat is put to sleep and its pane closed. The branch keeping idle panes open removes this call.

```rust
- match self.perform(Operation::Sleep(Sleep_Data {
-     address,
-     flow_node: node,
- })) {
-     Outcome::Slept => AtStop::Slept,
-     outcome => AtStop::Kept(
-         KeptAtStop::SleepRefused(
-             Box::new(outcome))),
- }
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
