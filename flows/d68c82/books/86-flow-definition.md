<!-- to-the-living:start -->
Presentation.{ «How a flow is defined» }

# How a flow is defined

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

### Proposal 1: Add · psyche-context › vision/flow.md

  Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.

+ ## A flow is specified whole, in Datom
+
+ A flow is specified whole, in Datom: its system prompt, which is the whole base context; how it works; its default context modules; and its variations. Flow controls the whole system prompt of every flow it starts. The specification is a Nix language for agents, in Datom.
+
+ The lean flow is one variant of the specification: a judgment-only call with no tools and no messenger, whose response is its message. It goes back and forth a few times with a supervising flow, which has the tools and finds out for it what it asks.
+
+ The shape of a definition, with an example, is in vision-flow-definition.

Ruling: land, amend, or reject.

### Proposal 2: Add · psyche-context › vision/ethos.md

  Traits are declared, never inferred; an association asserts the type bears it.

+ ## A specification groups its items by variant
+
+ A specification groups its items by variant: one vector for each variant, never one vector whose items each name theirs. A Signal's queries are one vector and its responses the next; a flow definition's main flows, subflows and lean flows are three vectors the same way.
+
+ Grouping saves repetition, so the syntax is succinct, dense and high in signal.
+
+ Not so good: one vector, each item naming its variant.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Effort.[ Low Medium High ]
+   Flow.[ Main.{ Model Effort }
+          Sub.{ Model Effort }
+          Lean.{ Model Effort } ]
+   Flows.{ Vector<Flow> } ]
+ []
+ []
```
```datom
+ Flows.{
+   [ Main.{ opus Medium }
+     Sub.{ sonnet Medium }
+     Sub.{ haiku Medium }
+     Lean.{ fable Medium } ] }
```
+
+ Good: one vector for each variant.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Effort.[ Low Medium High ]
+   Main.{ Model Effort }
+   Sub.{ Model Effort }
+   Lean.{ Model Effort }
+   Flows.{ Vector<Main> Vector<Sub>
+           Vector<Lean> } ]
+ []
+ []
```
```datom
+ Flows.{
+   [ { opus Medium } ]
+   [ { sonnet Medium } { haiku Medium } ]
+   [ { fable Medium } ] }
```

Ruling: land, amend, or reject.

### Proposal 3: Add · psyche-context › vision/flow-definition.md, a new file

+ ---
+ description: A flow's definition, its prompt, modules, model, tools and variants, is written, generated or judged.
+ dependencies: [vision-flow, vision-ethos, vision-datom]
+ ---
+
+ ## A flow definition
+
+ A flow definition groups flows by variant: a vector of main flows, then a vector of subflows, then a vector of lean flows. Each variant carries only the fields it has.
+
+ A main flow is addressed by { Aspect Topic Layer }; it carries its model, its effort, and the modules of its system prompt and of its first user message. A subflow is a named role: its model, effort, permission, modules, tools and callers. A lean flow is a named judgment call: its model, effort and modules, and the one supervising flow it answers to; it has no tools.
+
```ethos
+ Library
+ []
+ [ Module.String
+   Modules.Vector<Module>
+   Model.String
+   Name.String
+   Tools.Vector<String>
+   Topic.String
+   Aspect.[ Psyche Mind Field ]
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Effort.[ Low Medium High Xhigh ]
+   Permission.[ Restricted Unrestricted ]
+   Address.{ Aspect Topic Layer }
+   Callers.[ Any Only.Vector<Address> ]
+   Main.{ Address Model Effort
+          SystemModules.Modules
+          UserModules.Modules }
+   Sub.{ Name Model Effort Permission
+         Modules Tools Callers }
+   Lean.{ Name Model Effort Modules
+          Caller.Address }
+   Definition.{ Vector<Main> Vector<Sub>
+                Vector<Lean> } ]
+ []
+ []
```
+
+ A Secondary main flow, the book subflow, and a lean design flow, each in the vector of its variant:
+
```datom
+ Definition.{
+   [ { { Psyche core Secondary }
+       claude-opus-5-5 Medium
+       [ spirit-core intent-context
+         intent-main-flow vision-book
+         compensation-book-crystallization ]
+       [] } ]
+   [ { book sonnet Medium Unrestricted
+       [ spirit-core intent-context
+         role-book-publishing-procedure
+         vision-book
+         compensation-book-crystallization ]
+       [ Read Bash Agent Artifact ]
+       Any } ]
+   [ { fableDesign claude-fable-5-1 Medium
+       [ spirit-core intent-context
+         vision-book ]
+       { Psyche core Secondary } } ] }
```
+
```
+--------------------------------------------+
| flow definition                            |
+--------------------------------------------+
     |            |             |
     | groups     | groups      | groups
     v            v             v
+----------+ +----------+ +----------+
| main     | | sub      | | lean     |
| flows    | | flows    | | flows    |
+----------+ +----------+ +----------+
     |            |             |
     | compose    | compose     | compose
     v            v             v
+--------------------------------------------+
| default context modules                    |
+--------------------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 4: Add · mind-context › inquiry/flow-definition.md, a new file

+ ---
+ description: Which fields a flow definition has, how a variation overrides a default, and where definitions live and are generated, are unresolved.
+ ---
+
+ ## Which fields a flow definition has
+
+ - Does a main flow carry tools and permission, or only the leave-outs of its harness's startup? A subflow role carries both today; a main flow's launch carries leave-outs and no tools. One flow of each variant started from its definition alone, behaving as it does today, would settle it.
+ - Is the harness a field of a definition, or derived from the model, as Flow derives it today from the models its Codex endpoints serve? A model served by both harnesses would settle it.
+ - What does a lean flow answer? It answers with questions and designs, and perhaps a third thing. The alternatives:
+
+ Alternative a: a closed reply, one variant for each kind.
+
```ethos
+ Library
+ []
+ [ Reply.[ Question.String
+           Design.String ] ]
+ []
+ []
```
+
+ Alternative b: no type; the response is the message, as text.
+
+ ## How a variation overrides a default
+
+ - Where do the default modules of a variant live, so they are not copied into every entry, as roles.datom copies the common subflow list into every role today? Alternatives:
+
+ Alternative a: the definition opens with the default modules; each entry adds to them.
+
```ethos
+ Library
+ []
+ [ Module.String
+   Modules.Vector<Module>
+   Model.String
+   Main.{ Model Modules }
+   Definition.{ Modules Vector<Main> } ]
+ []
+ []
```
+
+ Alternative b: named groups of modules; an entry names the groups it takes.
+
```ethos
+ Library
+ []
+ [ Module.String
+   Modules.Vector<Module>
+   Model.String
+   Group.{ String Modules }
+   Main.{ Model Vector<String> }
+   Definition.{ Vector<Group>
+                Vector<Main> } ]
+ []
+ []
```
+
+ - How does a variation by layer, aspect or model override its default? Alternatives:
+
+ Alternative a: each entry carries its variations.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Variation.{ Layer Model }
+   Main.{ Model Vector<Variation> }
+   Definition.{ Vector<Main> } ]
+ []
+ []
```
+
+ Alternative b: the variations are a vector of their own, grouped like the variants.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Variation.{ Layer Model }
+   Main.{ Model }
+   Definition.{ Vector<Main>
+                Vector<Variation> } ]
+ []
+ []
```
+
+ Alternative c: nothing overrides; every variation is a full entry in its variant's vector, as each role and harness is spelled out in roles.datom today. Conditions inside a module's text stay as they are.
+
+ ## Where definitions live and are generated
+
+ - Does one definition replace roles.datom in Curriculum, the per-aspect and per-metaflow EDN files in Primary, Flow's model table by layer, and the model variables in SKILL_VARIABLES.md, which state models in four places today? Starting one flow of each variant from the one definition, with the four sources removed, would settle it.
+ - In which repository does the definition live? The living said it is a different repository from the cluster data.
+ - What writes the agent files of the roles that no current program writes? Alternatives: Curriculum reads the definition and renders the agent files, serving the startup and role texts as it does now; or Flow reads the definition and starts every flow itself, with no agent file.
+
```
+--------------+ +-------------+ +------------+
| roles.datom  | | main-flow   | | Flow's     |
| (Curriculum) | | EDN         | | layer      |
|              | | (Primary)   | | table      |
+--------------+ +-------------+ +------------+
       |                |               |
       | names          | names         | names
       | model of       | model of      | model of
       v                v               v
+--------------+ +-------------+ +------------+
| subflows     | | main flow   | | a woken    |
|              | | launches    | | main flow  |
+--------------+ +-------------+ +------------+
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
