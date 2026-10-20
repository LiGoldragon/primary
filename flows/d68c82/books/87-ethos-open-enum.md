<!-- to-the-living:start -->
Presentation.{ «Ethos: the open enum» }

# Ethos: the open enum

## psyche-context › vision/flow.md

````markdown
---
description: Flow — the Nexus that launches, names, tracks and ends flows — or a voice, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
dependencies: [vision-nexus, vision-ethos]
---

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

## Crystallization

### Proposal 1: psyche-context › vision/ethos.md

+ ## An open enum
+
+ An open enum is an Ethos object whose capitalized words are its fixed variants. A word that is not capitalized is its implied extensible variant, a camel ID: a word-based camel-case identifier, written bare, with no variant head before it. The name camel ID is temporary. A check that a word is a word-based camel-case identifier comes long term; short term, none is made.
+
+ The metaflow topic is an open enum: its fixed variants are a constant set, such as the core topic, and the users or the machine extend it with camel IDs as they need topics.
+
+ The same mechanism carries an object that is represented unconventionally, such as a word-based hash.
+
  ## Every declared type bears both traits
  
  Ethos Zero emits `Datomizable` and `Compositional` on every struct and

```
+--------------------------------------------+
| a word in an open enum's position          |
+--------------------------------------------+
        |                        |
        | capitalized            | uncapitalized
        v                        v
+----------------+     +---------------------+
| fixed variant  |     | camel ID            |
+----------------+     +---------------------+
        |                        |
        |                        | is checked
        |                        | long term as
        |                        v
        |             +---------------------+
        |             | word-based          |
        |             | camel-case          |
        |             | identifier          |
        |             +---------------------+
        | is a                   | is a
        v                        v
+--------------------------------------------+
| value of the open enum                     |
+--------------------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 2: psyche-context › vision/ethos.md

  The same mechanism carries an object that is represented unconventionally, such as a word-based hash.
+
+ A closed enum refuses a camel ID. Wrong: the topic lists only its fixed variants, and a written topic that is not one of them is refused.
+
```ethos
+ Library
+ []
+ [ Aspect.[ Psyche Mind Field ]
+   Topic.[ Core Ethos ]
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Address.{ Aspect Topic Layer } ]
+ []
+ []
```
```datom
+ ; refused: flowDesign is no variant of Topic
+ { Psyche flowDesign Secondary }
```
+
+ An open Topic accepts both cases. Right: the same fixed variants, and a marker that the enum is open. The marker here is the trait Extensible, one candidate among those in the inquiry.
+
```ethos
+ Library
+ []
+ [ CamelId.String
+   Aspect.[ Psyche Mind Field ]
+   Topic.[ Core Ethos ]
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Address.{ Aspect Topic Layer } ]
+ [ Extensible.[ extend:[ Self ] ] ]
+ [ Topic.[ Extensible ] ]
```
+
+ A fixed variant is capitalized and a camel ID is not, so the two never meet:
+
```datom
+ ; a fixed variant
+ { Psyche Core Secondary }
+ ; a camel ID, with no variant head
+ { Psyche flowDesign Secondary }
```
+
+ A camel ID written in any other way is wrong:
+
```datom
+ ; refused: capitalized, so a fixed variant
+ ; that Topic does not list
+ { Psyche FlowDesign Secondary }
+ ; refused by the check: not camel case
+ { Psyche flow_design Secondary }
+ ; wrong: a camel ID has no variant head
+ { Psyche Custom.flowDesign Secondary }
```

Ruling: land, amend, or reject.

### Proposal 3: mind-context › knowledge/ethos-layers.md, a new file

+ ---
+ description: The layers Ethos is made of, and how each reads an enum, a variant and a capital letter today, is needed to place a change.
+ dependencies: [knowledge-ethos, knowledge-datom, knowledge-protos]
+ ---
+
+ ## The layers, as the code stands
+
+ Witnessed in protos main 15b41da (0.32.2), ethos-zero main 07714b0 (17.0.0) and datom-codec main 4dff16b, read, not run, except where a line says it was run.
+
+ Ethos text is read by ethos-zero and becomes a Rust type; the type's derive, from datom-codec, reads and writes datom text through protos. Ethos-zero is the bootstrap and the generator in one crate: canonicalization, protosization, conception, checking and generation are its passes. Datom-codec is the Datom reader and writer. No registry of types exists in these repositories; the only registry in code is Curriculum's registry of skills.
+
```
+------------+          +------------+
| ethos file |          | datom text |
+------------+          +------------+
      |                       |
      | ethos-zero            | protos
      | generates             | reads
      |                       v
      |                 +------------+
      |                 | Protos     |
      |                 +------------+
      |                       |
      |                       | datom-codec
      |                       | forms
      |                       v
      |                 +------------+
      |                 | Datom form |
      |                 +------------+
      |                       |
      |                       | the derive
      |                       | composes
      v                       v
+--------------------------------------+
| a Rust type, with its derive         |
+--------------------------------------+
```
+
+ ## Capital letters today
+
+ Protos has no test of case: a run with a separator becomes a headed structure, any other run a bare one. Datom-codec's step from Protos to the Datom form is case-blind too. Case is read only by the type that composes the form: a derived enum matches a bare form against its unit variants by their exact spelling, and routes any other form to its payload variants by spelling.
+
+ Ethos-zero requires a capital letter on the name of a declared type or trait, and on no variant. Run against ethos-zero 07714b0, an enum `Topic.[ core ethos ]` is checked and accepted.
+
+ An alias is a Rust alias, transparent, never a new type: `Topic.String` is a `String`. A type reaches a custom text form through a hand-written reader and writer of its own, as Decimal has, or through an import of a Rust type that has one.
+
+ ## Topic and flow id today
+
+ Flow's library declares `Topic.String`; the camel-case check on a topic is a comment there ("check camelCase at input"), and no check in Rust was found. A flow id is `FlowId.String`; the title code accepts six characters, each a hexadecimal digit. A word-based id is a design in a flow's vision and in no code.
+
+ ## Syntax on a branch
+
+ The white braces and white square brackets of Ethos are on the branch ethos-proposals of ethos-zero, protos and datom-codec, and on no main.

Ruling: land, amend, or reject.

### Proposal 4: mind-context › inquiry/ethos-open-enum-layer.md, a new file

+ ---
+ description: At which Ethos layer an open enum lands, the reader, the type system, the generated derive or an imported type, is unresolved.
+ ---
+
+ ## At which layer the open enum lands
+
+ At which layer is an uncapitalized word in a typed position told apart from a variant, and by what is it carried into a Rust value? What would settle it: one open enum, the Topic of the metaflow address, taken through each alternative to the datom `{ Psyche flowDesign Secondary }` and back, and the work each needed counted. The alternatives, with what each touches and costs:
+
+ - Alternative a, the reader. Protos or the Datom form tells a capitalized word from another, so the Datom form gains a kind for an identifier. It touches the Datom form and every composition that reads a bare form, and protos, which several dialects share, would learn the Ethos rule of case. It makes every typed position able to see a camel ID.
+ - Alternative b, the type system. Ethos-zero's declaration gains a kind of enum that is open: its model, conception, checking and generation, and the files it generates for itself, change. The definition says what the enum is, in Ethos, where the living wants the model written. The spelling of the declaration is itself open; the marker trait in the examples is one spelling.
+ - Alternative c, the derive. The derived reader's final arm, which today refuses an unknown spelling, hands an uncapitalized word to a variant that carries a camel ID. The Rust enum has the variant, and the text omits its head. Ethos declares that variant:
+
```ethos
+ Library
+ []
+ [ CamelId.String
+   Topic.[ Core Ethos Custom.CamelId ] ]
+ []
+ []
```
+ - Alternative d, an imported type. A Rust type with its own reader and writer is imported into the library, as Decimal is read today. Ethos is unchanged and cannot show the fixed variants of the type; the Ethos object is not the whole definition.
+
```
+-------------------------------------------------+
| an uncapitalized word in a typed position       |
+-------------------------------------------------+
    |           |           |           |
    | is told   | is        | is        | is read
    | apart in  | declared  | routed by | by a hand
    v           v           v           v
+----------+ +----------+ +----------+ +----------+
| a:       | | b:       | | c:       | | d:       |
| reader   | | ethos-   | | derive   | | imported |
|          | | zero     | |          | | type     |
|          | | spec     | |          | |          |
+----------+ +----------+ +----------+ +----------+
    |           |           |           |
    | yield     | yield     | yield     | yield
    v           v           v           v
+-------------------------------------------------+
| the same camel ID value in the Rust type        |
+-------------------------------------------------+
```
+
+ ## The registry as a layer
+
+ The living counts a registry among the layers. In the code read, it is not a layer of Ethos. Does a camel ID need a registry: the set of topics a user or the machine has created, kept somewhere, so that a topic is checked when it is created? Alternatives: the check is of form only, and the set of live topics is Flow's memory; or the open enum's extensions are recorded in the registry the library is addressed by.

Ruling: land, amend, or reject.

### Proposal 5: mind-context › inquiry/ethos-open-enum.md, a new file

+ ---
+ description: The name of the camel ID, how a word is checked, the constant topics and the representation of a hash in an open enum are unresolved.
+ ---
+
+ ## The final name of the camel ID
+
+ What is the final name of the camel ID? The living calls it temporary. Three names for one idea stand in the context today: a camelCase identifier (vision flow), a camelCaseExpression of the type core:Name (vision flow), and camel ID. What would settle it: the living choosing one name, then every module using it. The alternatives:
+
+ - Alternative a: keep camel ID.
+ - Alternative b: word ID, which names what it is made of, as the word-based hash does.
+ - Alternative c: open variant, which names the place it takes in the enum.
+ - Alternative d: camelCaseExpression, the name already in the Flow vision.
+
+ ## How a word is checked
+
+ What makes a word a word-based camel-case identifier? Which words, from which list; whether a digit or an acronym is allowed; whether the check is a form only or a membership of a word list. The living asked for the check long term, and none exists now. Which first version of it would settle it: form only, a lowercase first letter, and capitals only at word starts.
+
+ ## The constant topics: Core or core
+
+ The living wrote the constant topic as `core`, uncapitalized, and defined a fixed variant as capitalized. Is the constant written `Core` as a fixed variant, or is `core` a camel ID that the set reserves? Alternatives:
+
+ - Alternative a: the constants are fixed variants, so `core` becomes `Core` in a datom and the flow vision's lowercase name is a spelling for text.
+ - Alternative b: the constants are reserved camel IDs, and the fixed variants of Topic are none.
+
+ A topic then has two spellings in alternative a if a camel ID `core` is also written: is it refused?
+
+ ## A hash in an open enum
+
+ A word-based hash has no fixed variant. Is it an open enum with an empty set of fixed variants, or another object with the same reading? And does an open enum's fixed variant ever carry a payload, or is a camel ID the only one without a head?

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
