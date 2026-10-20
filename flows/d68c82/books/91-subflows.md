<!-- to-the-living:start -->
Presentation.{ «Subflows, long term» }

# Subflows, long term

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


### Proposal 1: Remove · psyche-context › vision/flow.md

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

```
+--------------------------------------------+
| the three subflow sections of flow.md      |
+--------------------------------------------+
        |                       |
        | give way to           | pass their open
        |                       | questions to
        v                       v
+----------------+   +-----------------------+
| one broad      |   | inquiry module:       |
| long-term      |   | subflows              |
| statement      |   +-----------------------+
+----------------+
```

Ruling: land, amend, or reject.

### Proposal 2: Add, alternative a · psyche-context › vision/flow.md

  Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

+ ## Long term: actual flows replace the harness subagent tool
+
+ Long term, the harness subagent tool is replaced by actual flows. A subflow is an independent flow with its own system prompt, so the system is asynchronous: the subflow replies when it is done, and the flow that asked is not locked into waiting.

```
+--------------------------------------------+
| harness subagent tool                      |
+--------------------------------------------+
                    |
                    | is replaced by
                    v
+--------------------------------------------+
| a subflow: an actual, independent flow     |
+--------------------------------------------+
        |                       |
        | runs under its        | replies to
        | own                   |
        v                       v
+----------------+   +-----------------------+
| system prompt  |   | the asking flow or    |
|                |   | its successor         |
+----------------+   +-----------------------+
```

Ruling: land, amend, or reject.

### Proposal 3: Add, alternative b · psyche-context › vision/flow.md

  Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

+ ## Long term: actual flows replace the harness subagent tool
+
+ Long term, the harness subagent tool is replaced by actual flows that Flow starts. Each is a specialized flow with the system prompt its work needs, instructed as a subflow and not as a main flow.

Ruling: land, amend, or reject.

### Proposal 4: Add, alternative c · psyche-context › vision/flow.md

  Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

+ ## Long term: actual flows replace the harness subagent tool
+
+ Long term, a flow does not call a subagent tool. Its questions and requests are answered and fulfilled by actual flows, and the answers return to it as messages.

Ruling: land, amend, or reject.

### Proposal 5: Add, alternative a, in its own module · psyche-context › vision/subflows.md, a new file

+ ---
+ description: Subflows, the actual flows that replace the harness subagent tool long term, are being designed or judged.
+ ---
+
+ ## Long term: actual flows replace the harness subagent tool
+
+ Long term, the harness subagent tool is replaced by actual flows. A subflow is an independent flow with its own system prompt, so the system is asynchronous: the subflow replies when it is done, and the flow that asked is not locked into waiting.

Ruling: land, amend, or reject.

### Proposal 6: Add, alternative b, in its own module · psyche-context › vision/subflows.md, a new file

+ ---
+ description: Subflows, the actual flows that replace the harness subagent tool long term, are being designed or judged.
+ ---
+
+ ## Long term: actual flows replace the harness subagent tool
+
+ Long term, the harness subagent tool is replaced by actual flows that Flow starts. Each is a specialized flow with the system prompt its work needs, instructed as a subflow and not as a main flow.

Ruling: land, amend, or reject.

### Proposal 7: Add, alternative c, in its own module · psyche-context › vision/subflows.md, a new file

+ ---
+ description: Subflows, the actual flows that replace the harness subagent tool long term, are being designed or judged.
+ ---
+
+ ## Long term: actual flows replace the harness subagent tool
+
+ Long term, a flow does not call a subagent tool. Its questions and requests are answered and fulfilled by actual flows, and the answers return to it as messages.

Ruling: land, amend, or reject.

### Proposal 8: Add · mind-context › inquiry/subflows.md, a new file

+ ---
+ description: What a subflow needs, once actual flows replace the harness subagent tool, is unresolved.
+ ---
+
+ ## Who decides a subflow is started
+
+ - Is a subflow started by the flow that needs it, through a command to Flow, or from the questions and requests a flow ends with, by a small routing flow? The living has said both; he now doubts the second is still relevant. Whichever way, the first act is a routing job: is there already a flow that should simply get this message or this question? One subflow started each way, with the same work, would settle it.
+
+ ## What the asking flow holds
+
+ - Does the asking flow hold a request ID, by which it asks later for status and for more detail about what the subflow is doing, sends it messages while it is alive, and is told when it is done if it is still the flow in charge? Or does the answer return as a message with nothing held? A subflow run under each, while the asking flow continues other work, would settle it.
+
+ ## What a subflow costs
+
+ - Is a separate harness process for every subflow too costly against the subagent tool? The living asked it of Codex, of a Clojure call and of another harness. Starting both on the same task and comparing the tokens each costs would settle it.
+ - In how many cases does a minimal predefined subagent cost fewer tokens than the main flow using the tool itself? The living wants it measured from the flows so far; the measure would show which work a subflow must be cheap for.
+
+ ## Who can see a subflow
+
+ - Does a subflow appear in the queries for which flows exist, or only in the messenger? The living thought it could be reachable by message without appearing among the main flows. A query for main flows, run with a subflow alive, would settle it.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
