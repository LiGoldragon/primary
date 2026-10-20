<!-- to-the-living:start -->
Presentation.{ «A broken system is fixed» }

# A broken system is fixed

### Proposal 1: psyche-context › vision/flow.md

**Comment** The rule joins the flow vision beside the line that says the flow which finishes messages the flow that needs to know. The figure is proposed for the same module.

  A flow does not wait on a timer for another flow's work: the flow that finishes messages the flow that needs to know.
+
+ A broken system is never accepted. It is fixed whatever the cost, its cause is found, and the fix keeps it from breaking again.

```
+------------------+
| broken system    |
+------------------+
        | is fixed by
        v
+------------------+
| the flow that    |
| finds it         |
+------------------+
        | which finds
        v
+------------------+
| the cause        |
+------------------+
        | and prevents
        v
+------------------+
| the next break   |
+------------------+
```

### Proposal 2: psyche-context › vision/messaging.md

**Comment** The line enters the delivery section, after the paragraph that says how each harness receives a message.

  Soft waits for the recipient to finish.
+
+ A message reaches the flow it is for by whatever route works; a refused route is fixed, never left standing.

### Proposal 3: psyche-context › vision/messaging.md

**Comment** The line enters the section on which messages are sent, since a test is a sender of messages.

  Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.
+
+ A test sends only to a flow that needs the message, never to every flow. A Fable flow is never woken for testing.

### Proposal 4: field-context › compensation/behavior.md

**Comment** Vision in Proposal 1 says a broken system is fixed and its cause found; the line below stops at a repeated failure and reports. The living rules which alternative lands. Alternative 1 removes the line's second sentence whole, since Proposal 1 replaces it. Alternative 2 removes only the repeated-failure clause, so that a flow which cannot proceed still reports what blocks it.

**Alternative 1**

- A flow works until its order is done. When it cannot proceed, or an attempt repeats a failure, it stops and says what blocks it, what would unblock it, and the decision it needs; it never reports only that it is waiting.
+ A flow works until its order is done.

**Alternative 2**

- A flow works until its order is done. When it cannot proceed, or an attempt repeats a failure, it stops and says what blocks it, what would unblock it, and the decision it needs; it never reports only that it is waiting.
+ A flow works until its order is done. When it cannot proceed, it stops and says what blocks it, what would unblock it, and the decision it needs; it never reports only that it is waiting.

### Proposal 5: field-context › compensation/messenger-clj.md

**Comment** Proposal 2 says a refused route is fixed and a message reaches its flow by whatever route works; the last sentence of the line below says it already, so it leaves. The meanings of Held, RepairRequired and Uncertain describe what hm-send prints and stay.

- The typed reply is what hm-send itself prints; a flow never waits on or watches the target for an answer. What hm-send prints stays with the sender: it is acted on and logged, never forwarded. `Transported` is Herdr's acceptance for the checked binding. `Presented` includes the observed reaction of the target. `Held` means nothing was typed and the whole body is pending until an explicit supported delivery action; its printed reason names the refusal. `RepairRequired` means the recorded candidates must be judged and the route repaired with `hm-repair`. `Uncertain` means the envelope may have arrived: inspect the target and never retry blindly. A refused or undelivered send is reported to the sending flow and its route is mended.
+ The typed reply is what hm-send itself prints; a flow never waits on or watches the target for an answer. What hm-send prints stays with the sender: it is acted on and logged, never forwarded. `Transported` is Herdr's acceptance for the checked binding. `Presented` includes the observed reaction of the target. `Held` means nothing was typed and the whole body is pending until an explicit supported delivery action; its printed reason names the refusal. `RepairRequired` means the recorded candidates must be judged and the route repaired with `hm-repair`. `Uncertain` means the envelope may have arrived: inspect the target and never retry blindly.

## psyche-context › vision/messaging.md

````markdown
## A message is a datom, and it arrives as one

The message body is a datom that lands in the recipient's prompt as a
datom-formatted object. There is no envelope around it.

## Priority is a head on the datom

    Priority.[HardAbrupt MiddleAbrupt Soft]

## Delivery is harness-specific, and the mechanism differs per tier

Hard abrupt on Codex is one Escape, and the prompt submits itself. Hard
abrupt on Claude is two Escapes — the first is taken by the input editor in
vim mode and never reaches the harness — then the prompt, then an explicit
Enter, because after an interrupt the prompt is placed in the composer
without being submitted. Middle abrupt is the terminal prompt, which a
Claude recipient receives at its next tool boundary. Soft waits for the
recipient to finish.

## An interrupt witness is not a delivery witness

Inducing an interrupt, placing prompt text, submitting it, and the recipient
consuming it are four separate observations. None of them stands for
another, and a submission is never a read receipt.

## Only messages that act, deliver, or block

Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.

## A hash or an identifier is six characters

A hash or an identifier in a message is its first six characters.
````

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

A flow gives a presentation, a response that could fit into a book, whenever it is given significant new context to consider: its first turn ends in one, and so does every task, goal or question that originates in the psyche. A message from another flow that only updates it needs no full presentation. A presentation takes its form from the context modules the flow was loaded with and from its prompt, the one string given to that flow alone, which is no context module.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.

A fresh flow starts with every context module its metaflow is bound to, none left to load afterwards: much of it in its system prompt, the rest in its first prompt, or in as many prompts as it takes, sent one right after another, so that its start is one model call.

A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.

A flow is specified whole, in Datom, by a domain-specific language in Ethos: its system prompt, its default context modules and its variations. The flow ethos holds the specification.

Short term, a Primary is not started without its Secondary, and the Secondary starts first.

Long term, a Primary is a simplified flow, used only to render judgment: guiding a design or posing questions.

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

Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow past its context threshold is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

A flow is refreshed when its context passes its model's threshold: it is told nothing and writes no handover; it is given no new message, Flow keeps the metaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Each model's threshold is configured in Flow; an OpenAI model's is lower than a Claude model's.

Compaction is an absolute emergency measure: a compaction request is refused while the context is below a threshold.

A flow that keeps working without being given more work may compact. Its compaction raises a warning, and a flow investigates why it worked so long, so that the trouble is brought to the living or Psyche reconsiders the approach and gives guidance.

An ephemeral flow is a continuous job flow that does not wake back up: it takes jobs while it runs, up to a ceiling on its context, and past the ceiling it is given no new job and another ephemeral flow takes it. With Claude the ceiling is 300,000 tokens, and the flow is wound down at 250,000.
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

## mind-context › knowledge/flow.md

````markdown
Before launching, naming, claiming, reaching, or reporting a Flow, read
the matching deployed source and obtain the target's explicit response
through the current ordinary or meta socket. Do not infer protocol,
caller identity, store state, or runtime bindings from a source version
or client path.

## Stated configuration and launch contract

These are the authorized contracts; this section does not establish deployed runtime behavior while the configuration rewrite is pending.

The tool that starts flows merges its configuration files in order, shared, aspect, metaflow, map into map, so a later file's value wins at each key.

A context is young while it stays under half the layer's refresh threshold.

A launch that needs a Primary starts its Secondary first.
````

## field-context › compensation/default-effort.md

````markdown
A second expensive flow in one role, or reawakening a failed expensive
flow, requires an explicit ruling.

Routine housekeeping, such as file layout, commits, or book reformatting,
goes to the least costly capable flow; substantive design goes to the
designer.

Local model hosting and its files live only on `Local model host`, the
setup variable in `SKILL_VARIABLES.md`. This does not constrain vendor
inference.

A Fable flow is launched or woken only on the living's word.
A Fable flow sleeps once its work is handed on; a message that needs no Fable decision goes to its Secondary instead of waking it.
````

<!-- to-the-living:end -->
