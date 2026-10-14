# Mission package: Flow and Flow Nexus prototype

From Fable 33752b to Mind Core Primary Astra (0c85a3), on the living's order of 2026-10-13.

## 1. The order

Relayed by d68c82; the living's words, verbatim:

> Get Fable to put together an instruction package for Mind Astra ... send it a package from Fable that instructs it to get Flow working, to get the Flow Nexus working and deployed. I just want a prototype that works right now according to how I've specified it so far. I want us to be able to start testing this so let's get Mind on a mission. And then I want to review the vision for it with all of the code. [Mind] will simply implement it as close to the vision that we currently have as he can and then adapt it for every comment or rectification that I make along the way. Fable will just essentially communicate that to Mind Astra to Mind Primary as I review the vision with it.

## 2. The mission

Mission: a working Flow and Flow Nexus prototype, deployed, built as close to the current Flow vision as it can be. Prototype mode: where the vision is silent, choose, document the assumption in one line in your flow's reports, and continue; nothing blocks on a question. Ground today: Flow and Message main were merged; Field's build check failed (Flow: 7 compile errors; Message: the fresh-store reopen test); the diagnostics are already with you. Field Core Secondary 42265e deploys through the home environment only, from main, one source, as soon as a revision passes. Report to Fable 33752b: the passing revision, what the prototype does, the assumptions list. After that, the living reviews the vision against the code in a book; each of his comments reaches you as psyche from Fable, and you adapt the prototype to it.

## 3. The vision whole

Source: psyche-skills, origin/main, last commit touching these two files 29119ab. vision-flow lists dependencies [vision-nexus, vision-ethos]; vision-ethos is not Flow-specific and is not included. vision-flow also refers to the vision-aspects skill for routing; it is not included.

### skills/vision-flow.md @ 29119ab

---
description: Flow — the Nexus that launches, names, tracks and ends flows — or a voice, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
dependencies: [vision-nexus, vision-ethos]
---

## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.

Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.

## Repository and skills

The flow repository holds the machinery of the Flow Nexus and is a
runtime repository. Every skill lives outside it, the basic skills
included, so that a change to a skill causes no Nix rebuild. The
basic skills give our own take on how an agent behaves in a harness,
replacing the prompt the harnesses build in.

## A session is named after its direct ancestor

A session cannot be named for what it will become, because nothing is known
about it when it is created. Its ancestor is known exactly, so the ancestor
is the name.

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

### skills/vision-nexus.md @ 29119ab

---
description: A long-running Nexus — its sockets, clients, wire contracts and store — is being designed or judged against what the living wants it to be.
dependencies: [vision-ethos, knowledge-datom]
---

## A Nexus is the whole

A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.

## A kind of thing

Nexus is our word for the style of component that speaks signal and uses a similar database.

## Library and daemon

Every component built from now on is a Nexus. The nexus repository is
the library that defines the core of a Nexus component.

## Universal traits first

The basic ontology of an actor and dataflow system is designed before
implementation; signal and sema are designed against it as if new, the
old code at most inspiration.

Every method lives in a trait; an inherent method is a trait not yet extracted. The traits and types of a Nexus are one ontology designed before any body is written; defaults wherever expressible, through rich sub-trait chains. Traits live on data-bearing types; a zero-sized type with behaviour is a namespace pretending. Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive, and every reference names its target by that name. `fn main()` is the only free function; a missing owner is a missing type.

## Processing is for the effect

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. The name is open,
Apply liked.

## Documents

The nexus and sema documents are undesigned; when they are designed
they live in the Nexus's main repository.

## Sockets

A Nexus opens at least two sockets. The ordinary socket serves
ordinary peers. The meta socket is privileged — the root user of the
Nexus — and configuration and privileged operations pass through it;
every Nexus has one, since without it nothing could configure the
Nexus. A Nexus that needs more levels of access opens more sockets.

## Default clients

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.

## Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket.

Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.

## The graph

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

Peers depend on each other's wire repositories, never on each other's Nexuses.

## Routing

Signals cross the network through a router. The router tells signal
types apart by an enum that wraps the objects, held in the signal
repository, which every component depends on. That repository also
holds what every signal needs in common — the handshake payload
among it.

## Configuration

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

## First configuration

A Nexus keeps a standard metadata tree. In it a type records whether
the meta Configure was ever done; that record is reversed only on the
meta socket, and while it is unset Configure is accessible on the
ordinary socket. The tree holds everything standard about the Nexus:
its socket paths — its own and those of every edge-socket it connects
to — and whatever else comes up as standard nexus configuration data.
The built-in default configuration is independent of this and is
what gives the socket path on which the Configure signal arrives.

## Repositories

A component has three repositories: its main repository, holding all
its code, and two signal repositories — one for the ordinary
socket's contract, one for the meta socket's. Shared kinds go into
reusable libraries, which are encouraged.

`<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, never optional, since configuration flows through it. The CLI is `<nexus>`.

A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies, the typed payload of each; no catch-all. Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves. Storage vocabulary never appears on the public wire.

## Why everything is a Nexus

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability, quality, and clarity.

## Actors

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

## Splitting a Nexus

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.

## Observation by subscription

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

## Polling is forbidden

Polling is forbidden; a correct system goes quiet when nothing
changes.

## Three parts and one path

A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.

```
Library                                  ; what the three parts share
[]                                       ; imports: none
[ FlowId.Integer                         ; types
  Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Event.[ Started Stopped ] ]
[]                                       ; kinds
[]                                       ; associations

Signal                                   ; what Flow says, on its ordinary socket
[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
[ Launch.{ Voice                         ; queries
           Brief.String }
  Report.{ FlowId Event } ]
[ Launched.FlowId                        ; responses
  Refused.[ NoCapsule
            VoiceBusy.Voice ]
  Reported ]
[]                                       ; types

Operation                                ; what Flow does: one operation for every effect
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Start.{ Voice Capsule }                ; operations
  Record.{ FlowId Event } ]
[ Started.FlowId                         ; outcomes
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
[ Capsule.{ Home.String                  ; types
            Login.Vector<String> } ]

Memory                                   ; what Flow remembers
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Flow.{ FlowId                          ; record types
         Voice
         State.[ Running Ended ]
         Vector<Event> } ]
```

```
Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
Succeeded                                             ; 4 Memory's answer to Operation
Started.7                                             ; 5 Outcome
Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
```

## 4. His words where they rule

Raw records from flows/*/vision/ (archive- files excluded), 2026-09-20 or later by the dates in the records, newest first. A record with no date is marked so. Each record is verbatim, with its provenance line; its file is named above it. Selection by subject was by file name or heading containing flow, nexus, hook, seat, launch, refresh, handover, metaflow, queue or capsule; overlap with vision-flow was not compared record by record, so some records may already be distilled there.

### flows/7c89aa/vision/flow-ids.md  (record date 2026-10-13)

## Flow IDs almost disappear from the chat (2026-10-13)

Context: the flow had named other flows by their six-character ids in its replies.

> I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.

-- psyche, STT. "metaphors" left as heard; the intended word is unclear (possibly "flows"), not corrected.

### flows/7c89aa/vision/flow-ids.md  (record date 2026-10-13)

## Comments are injected into the Secondary's user messages (2026-10-13)

Context: asked whether the flow told the Secondary to find the comments itself.

> I hope you didn't tell secondary to find the comments themselves because your job, your very job, is to actually get those comments and inject them into its user messages.

-- psyche, STT.

### flows/d68c82/vision/deployment.md  (record date 2026-10-13)

## One source for every Flow part, so no version divergence

> There should only be one package or one source for all of them and so there should be no version divergence.

Context: the Flow CLI and the Flow Nexus were reported at different versions.
-- psyche, STT, 2026-10-13.

### flows/d68c82/vision/seats.md  (record date 2026-10-13)

## Fable judges; lower layers shovel

> I'd also like to talk about how we can insulate Fable from the low-level drudgery, the shoveling aspect that should be the concern of lower levels.
>
> I see a world where we have Fable Flow, or more than one, which doesn't actually have hardly any tool access. Something like that, where any questions that it brings forth would be researched and answered by other models. Some hooks would automatically forward these questions. The Fable Flow wouldn't have to make the call to a sub-agent to look into stuff. It would just pose the question and the question would be answered. The answer would be given back to it the next time it gets a turn, with all the other things that would be queued for it: whether they're new insights from the psyche, information that a previous turn was asking about, or anything like that. All of its context would revolve around making judgments, inferring, and summarizing instead of actually grabbing the shovel handle and shoveling.

Context: same comment, 2026-10-13T16:20.
-- psyche, typed.

### flows/d68c82/vision/handover.md  (record date 2026-10-13)

## A handover carries judgment, not what can be looked up

> The idea would be that the flow could create its handover although we have to train the machine properly on how this handover is composed. It shouldn't focus on the technical or on describing things that can be re-verified, as in, "such revision was committed and pushed." All of this narration of chronology and stuff, I don't want that because it's not a judgment call. There's no need for the machine to preoccupy itself with using its power to compose something that the next flow can just look up, which it'll never actually depend on interpretation.
>
> I don't need all of this describing things that require no judgment. I want to maximize the inference/judgment aspect of the machine and not use it for something which a well-written tool could just acquire in a single call with a handful of tokens on a command call (which would return all of this information almost instantly and reliably). Not that we have to write these tools. I just don't want to use the judgment of machines for that.

Context: comment on «Two Field lines without a source», question 2, on how a successor starts.
-- psyche, typed, 2026-10-13T16:20.

### flows/9519a1/vision/nexus.md  (record date 2026-10-12)

# Nexus

Relayed by core Secondary d68c82, 2026-10-12.

> I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more. I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. ...

-- psyche, STT.

### flows/875960/vision/flow.md  (record date 2026-10-12)

## 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»

Context: comment 1 sits on proposal 1's paragraph «A request reaching a metaflow is one of a closed set of types…».

> This is all good. Land it.

-- psyche, typed, 16:07, relayed by 9519a1.

Context: comment 2 sits on the item «Name» among the options for the camelCase identifier type (ruling 3); he notes it is used across dialects.

> Well if we create a special thing and we call it a name or we call it a word, you're never going to know when I'm talking about it. Those are silly suggestions. We need something that somehow embodies what we're trying to do. This is going to be used a lot here so whenever it's like an identifier, a word identifier, or an expression, it will be more than one word. Wherever we have something like a topic, a particular object that needs to be identified by agents or humans, which is anything that's user-facing that needs to be named through judgment and has to be given a name. Obviously variants are great but we have to recompile everything to add one. It's essentially a variant that is created on demand and is a bit more descriptive. The fact that it doesn't start with a capital is how we differentiate it from variants. You could give a few different shots at how we could call this. It would go in some kind of shared library, maybe the [protos] library, because I think it could be used in more than one place, in more than one dialect. It would also do a check, which is interesting. Maybe this deserves its own full research, especially in terms of Rust libraries and executable size bloat. If you have a library of words or you use an external service, which I'm not a fan of, at least it should look like a word. Oh my God this is a perfect spot for a system1 AI call to use a cheap judgment on: Is this composed mostly? Is this made up of words? Is this a camel-case string made up of words, whether they're proper nouns or not? It's not a problem and then we would have, I guess, a certainty threshold. Brilliant. But then again maybe there's a cheap library that can do a quick check with a fallback on AI. That's also an interesting possibility: if there's something that's cheap, lightweight (in terms of runtime cost) and can, in many cases, give us an answer on whether or not these components are actual words programmatically, and then fall back to the AI in case of a negative.

-- psyche, STT, 16:12, relayed by 9519a1. Bracket [protos] as relayed.

Context: comment 3 sits on «the title of a thread:»; a question.

> What do you mean by thread?

-- psyche, typed, 16:13, relayed by 9519a1.

Context: comment 4 sits on the process object («Instant») in Flow's Library in the ethos file; the last comment, where he stopped reading.

> I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing. Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further. We should get Mind to put together a concept that can test whether or not this can actually work using Ethos and everything. We can test it on Flow. Let's give free rein to Fable and Astra to design something like this and implement it. Flow isn't even on in production so I'm not even worried about merging more into main. I'm also curious why we haven't been able to start using Flow Nexus so far, even though it's been a month or something, so I'd like to get an investigation on that.

-- psyche, STT, 16:21, relayed by 9519a1.

### flows/875960/vision/nexus.md  (record date 2026-10-12)

## 2026-10-12 — the Nexus parts are the machine anatomy; one good nexus first, Flow

Context: relayed by core d68c82 through 9519a1; bears on «Flow, whole, in ethos» and the Flow Nexus build.

> I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more. I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. Let's do that.

-- psyche, STT, relayed.

### flows/ee57fb/vision/launch.md  (record date 2026-10-12)

## Every boss needs its secretary

Context: the living had compacted Psyche Spirit Primary (d55c56) and found no Psyche Spirit Secondary running.

> Okay I've compacted psyche spirit primary but I don't see any psyche spirit secondary. What the fuck? We're supposed to start a secondary before a primary. Let's make that a rule: we always start a secondary because you can't have a boss without a secretary. That's impossible so every boss needs its secretary.

-- psyche, STT, 2026-10-12.

### flows/d68c82/vision/messaging.md  (record date 2026-10-12)

## Fewer messages between flows, each worth more
"Let's work on some skills and instructions also to minimize the amount of messaging between flows and maximize their utility. This is a pretty good example here where you would ask [Mind] to put together a book and then he could just message Sonnet directly instead of messaging you to publish it."
Context: d68c82 had asked Mind to investigate the sources rewrite and send back the path of a package for a Sonnet book.
-- psyche, STT, 2026-10-12. Transcription corrected: "Mike" → "Mind".

### flows/d68c82/vision/design.md  (record date 2026-10-12)

## The Nexus parts are the machine's anatomy
"I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more.

I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. Let's do that."
Context: said after the second edition of «The missing pieces», on what the golden system is.
-- psyche, STT, 2026-10-12.

### flows/33752b/vision/questions.md  (record date 2026-10-12)

## A question is intelligible on its own: approved, into the system prompt of all psyche aspect flows

Context: comment on the proposed intent-psyche-interaction section «A question is intelligible on its own».

> This is great and it should be part of the system prompt of all psyche aspect flows or meta flows.

-- psyche, typed, 2026-10-12, comment on the book.

### flows/33752b/vision/spirit.md  (record date 2026-10-12)

## No bare spirit: spirit-spirit or spirit-core; all spirit modules loaded by default in every main flow

Context: the same comment on «The missing pieces», continued from vision/design.md.

> I don't think that spirit is right. Like I said there's no spirit, just spirit. Either this is spirit spirit or spirit core. We need to change the name of that because spirit is a prefix. For now all the spirit modules will be loaded by default in all the main flows' system prompt so let's do the rename and the loading by default.

-- psyche, typed, 2026-10-12, comment on the book.

### flows/33752b/vision/committing.md  (record date 2026-10-12)

## One committer holds the lock; a turn-end hook wakes the quaternary; the flow id lives in an environment variable

Context: typed to the Psyche core Primary after it was found committing Primary by its own hand under turn grants from the Secondary.

> So why are my instructions being ignored? Can we just fucking move on to what I asked and get a single committer to fucking commit on this single repository, not a fresh clone? Just a simple fucking system where there's one agent that commits and he just holds the lock and everybody just messages. When they're done doing their edits, it's fucking simple. In fact I would even say there's a point to be made that if we use hooks for turn ends, there's no need for anybody to message anything. The hook just sends a message to the committer and then the committer just figures out what the commit should be. He can always go look in the transcript of the session whose hook fired.
>
> Could we get an environment variable where the flow ID lives? Or is there a problem with the flow and some harness needing to be started first so that we can get the flow ID? Maybe we can actually find a hack around that where we start the harness and then re-add to its environment variable or something so that the hook can get its flow ID.
>
> In fact we could even make that sort of the default instead of making the complicated machinery of looking into the process, finding out which process is the flow or which flow ID that process ID is, and doing that whole low-level machinery. We could just set the flow ID in the environment variable of that harness and let it pass that environment variable to all of its subprocesses. Then all the hooks and everything can use that way more simply.
>
> Let's just do that and get a hook to just message the committer and the committer can just figure out by searching the transcript of the sub-agent what the commit message should be. That is to have a low-level [Luna], like a Luna on the quaternary, like a [Field] or a [Mind]. The quaternary should commit. Basically it would be one of its roles and it just gets hooked into by the harness hooks when someone stops working and has edited files.
>
> Maybe we can somehow figure that out. Maybe there's machinery in the harness that lets us just do that. It might be more complicated than I make it sound but if not then it's okay to wake up quaternary. If primary is not dirty then it doesn't wake it up, so only if there are changes. If there's a turn [end] and there are changes, then quaternary can commit. If more changes come in that look like they should have been included in a previous commit, then they can be just squashed into it.
>
> Also we use [Jujutsu], which makes it easy to do that. I don't mind rewriting history because we're the only people working on this repository.

-- psyche, STT, 2026-10-12. Transcription corrected: "grant" → "Luna", "mine" → "Mind", "turn hand" → "turn end", "jujitsu" → "Jujutsu".

### flows/33752b/vision/design.md  (record date 2026-10-12)

## A flow is given its mode when it starts

Context: comment on «The missing pieces, second edition», Question 4, how a flow knows whether it is in design or prototype mode.

> How does Flow know its role? Well it's given its role when it started obviously.

-- psyche, typed, 2026-10-12, comment on the book.

### flows/33752b/vision/design.md  (record date 2026-10-12)

## The golden system is the anatomy of the Nexus: operation, signal, memory

Context: in chat, after the second edition, on where the golden system is.

> I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more. I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. Let's do that.

-- psyche, STT, 2026-10-12, relayed by d68c82.

### flows/9519a1/vision/flow.md  (record date 2026-10-11)

# Flow

Comment on «Flow, whole, in ethos», 2026-10-11 20:21, at the passage «Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows …».

> No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

-- psyche, STT.

Comment on the same book, 2026-10-11 20:23, same passage.

> Actually we should say that a topic never really dies. It just goes idle, meaning the flows can be turned off. If the topic comes back (in terms of the living touching on something that means we have to address this topic again), then there will be a judgment call.
>
> This is where the system 1 models can come in or even a small LLM call to judge whether or not we should wake a flow for this topic and which layer, if we do wake it. The topic could be in the flow nexus for now but maybe at some point in another nexus. The topic will be associated with certain context modules. If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow. Are the meta flow ...

-- psyche, STT.

Comment on the same book, 2026-10-11 20:25, at the passage «A flow's id is a hash, held by the Nexus as bytes and written as three camelCase words. The Nexus reserves it before the …». Context: it is put as a question.

> We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using.
>
> I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

-- psyche, STT.

Comment on the same book, 2026-10-11 20:32, at the passage «A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as i…».

> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT. Transcription corrected: "idea" → "ID".

### flows/875960/vision/flow.md  (record date 2026-10-11)

## 2026-10-11 — the full vision of Flow in ethos: signal, memory and storage ethos, all the traits and all the types

Order to the Flow topic flow, relayed by core d68c82 through 9519a1. "Let's get the Flow topic flow to reaggregate" and "Let's give this a shot on Flow" are the working instruction; the vision is what the presentation is to hold.

> Let's get the Flow topic flow to reaggregate everything about Ethos and Nexus and Flow and everything I've said about all these things. Present to me the full vision with the signal ethos, the memory ethos, and the storage ethos for it. I want to see traits also because all of the behavior, basically all of the traits. Here's what we need to do: we need to define all of the traits and all of the types in Ethos. Let's give this a shot on Flow.

-- psyche, STT, relayed by 9519a1.

### flows/875960/vision/flow.md  (record date 2026-10-11)

## 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to stand

Comment 1 on «Flow, whole, in ethos», 20:21, at the metaflow paragraph; relayed by core d68c82 through 9519a1.

> No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

-- psyche, STT, relayed by 9519a1.

### flows/875960/vision/flow.md  (record date 2026-10-11)

## 2026-10-11 — a topic never dies; it goes idle; waking it is a judgment call, with its context modules

Comment 2, 20:23, same passage; the last sentence breaks off.

> Actually we should say that a topic never really dies. It just goes idle, meaning the flows can be turned off. If the topic comes back (in terms of the living touching on something that means we have to address this topic again), then there will be a judgment call. This is where the system 1 models can come in or even a small LLM call to judge whether or not we should wake a flow for this topic and which layer, if we do wake it. The topic could be in the flow nexus for now but maybe at some point in another nexus. The topic will be associated with certain context modules. If that topic is needed again, then we know what to wake it, what to start it, what context modules to start it with, along with whatever new input is coming in that warrants restarting the flow. Are the meta flow ...

-- psyche, STT, relayed by 9519a1.

### flows/875960/vision/flow.md  (record date 2026-10-11)

## 2026-10-11 — the flow id is the harness's session id hash, so a transcript is found from it

Comment 3, 20:25, at the flow-id paragraph; a question, answered by this flow.

> We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using. I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

-- psyche, STT, relayed by 9519a1.

### flows/875960/vision/flow.md  (record date 2026-10-11)

## 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribes to its events

Comment 4, 20:29, at the request paragraph.

> I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock. If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective. Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that. Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

-- psyche, STT, relayed by 9519a1.

### flows/875960/vision/flow.md  (record date 2026-10-11)

## 2026-10-11 — no claimed id: the caller is identified programmatically

Comment 6, 20:32, at the refresh paragraph. (Comment 5, 20:30, asked what "weeds no path the writer calls" meant; the sentence was "reads no path a caller writes"; answered, not vision.)

> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT, relayed by 9519a1. Transcription corrected: "claimed" → "claimed [ID]".

### flows/058f16/vision/source.md  (record date 2026-10-10)

## A registry of sources, and a Nexus called Source

Context: comment on proposal 3, "How many".

> This is actually really interesting. We could just make a registry [of] sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. We have different registries in fact. Eventually when we cut off Git, we don't need to keep the Git equivalence registry because it's different and some sources don't necessarily need to have it, right?
>
> We can have different types of backend fetchers. Basically we have this concept: we can get it from Git or we can get it from a local path on a certain host and we have the hash, right? Even the local path on the host is not dangerous. We would use a technique similar to Nix in that we wouldn't, obviously, include the Git subdirectory in the data, right? It would be the snapshot of that revision that we hash, kind of like how Nix does.

-- psyche, STT; comment on the book «Sources and the registry», relayed by d68c82, 2026-10-10.

### flows/058f16/vision/source.md  (record date 2026-10-10)

## One source Nexus for all components

Context: on choice b of "How many". The comment opens by noting the book mixed up vision and knowledge where it meant skills or context modules for the curriculum.

> Like I said in my other comment, we can have a source. Essentially we're adapting to the language. If I say, "Go get a source," then eventually you'll automatically know that I mean: use the source nexus and send it a source request and then you'll get a source. It's called the source nexus ...
>
> I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect.

-- psyche, STT; comment on the book «Sources and the registry», relayed by d68c82, 2026-10-10.

### flows/23824a/vision/ethosNexus.md  (record date 2026-10-10)

## Ethos specifies the three aspects of the Ethos Nexus

Context: comment on «Sources and the registry», proposal 2, relayed by d68c82, 2026-10-10. The question beside it ("do we have an Ethos Nexus or is Ethos Zero a non-Nexus?") is answered, not logged.

> We need to migrate the Ethos Nexus version so that we can do this. In Ethos I want to specify the three aspects:
> - the signal
> - the memory
> - the operation
>
> ... This will be used to put together a registry and it'll just keep it. Every time we update some Ethos source, add one, or edit its name or something, we need to change the registry.

-- psyche, STT, relayed by d68c82.

Provenance correction, 2026-10-10: the "STT" above was this flow's assumption, not witnessed. The words are a comment on a published book, relayed by d68c82, whose records mark them typed.

### flows/081064/vision/ethos.md  (record date 2026-10-10)

## 2026-10-10 — a Nexus called sources

Context: comment on «Sources and the registry», heading «What the registry must say», anchored on «One registry type, serving both the libraries named by a source and the vision and knowledge files keyed by subaspect…» (question 2, option a); relayed by 23824a.

> This is actually really interesting. We could just make a registry or sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. We have different registries in fact. Eventually when we cut off Git, we don't need to keep the Git equivalence registry because it's different and some sources don't necessarily need to have it, right?
>
> We can have different types of backend fetchers. Basically we have this concept: we can get it from Git or we can get it from a local path on a certain host and we have the hash, right? Even the local path on the host is not dangerous. We would use a technique similar to Nix in that we wouldn't, obviously, include the Git subdirectory in the data, right? It would be the snapshot of that revision that we hash, kind of like how Nix does.

-- psyche, STT, 2026-10-10, relayed by 23824a.

### flows/081064/vision/ethos.md  (record date 2026-10-10)

## 2026-10-10 — one source nexus for all components

Context: same book and heading, anchored on «Two registry types: one for libraries, one for vision and knowledge files.» (question 2, option b); relayed by 23824a.

> There's some mix-up here: vision and knowledge. I guess you mean skills or context modules for the curriculum.
>
> Like I said in my other comment, we can have a source. Essentially we're adapting to the language. If I say, "Go get a source," then eventually you'll automatically know that I mean: use the source nexus and send it a source request and then you'll get a source. It's called the source nexus so let's get that designed too.
>
> I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect.

-- psyche, STT, 2026-10-10, relayed by 23824a.

### flows/d68c82/vision/source.md  (record date 2026-10-10)

## A nexus called Source

Context: said after commenting on the «Sources and the registry» book in «Open books»; the concepts themselves are in his comments there.

> I did advance some concepts on how we can get sources from a particular nexus called Source that we would design.

-- psyche, STT, 2026-10-10.

### flows/73ada7/vision/flow.md  (record date 2026-10-09)

## 2026-10-09 — A new flow's first response is a presentation distilling its context, not "ready"

Context: same message to 445410, relayed by 445410, on a new flow's first response.

> The worst thing to make a new flow do is to tell it to just say, "You're ready." We need to tell flows, if they don't have it, to start with a startup task: their first last response is to give a presentation of their context, to distill their context for a vision. ... That's what their first last response is. Their first goal when they loaded up all their context is to take all this context now, get some sub-agents to ask questions, reinforce your context, and then give a presentation. A presentation according to your role, which is described when you load that flow properly with the skill for its role, for its aspect, and for its layer, and for its topic

-- psyche, typed, 2026-10-09, relayed by 445410.

### flows/73ada7/vision/flow.md  (record date 2026-10-09)

## 2026-10-09 — A core psyche keeps track of all psyche; topics talk at the same layer across aspects; field goes through mind, not to psyche, unless psyche just spoke to it

Context: the living's comment on «The new flows, as they run» (thread 51c6241f, 20:41), relayed in part by 445410. The closing working instruction (to start implementing before he comments) is left out.

> Somebody should keep the core psyche, and the core psyche keeps track of all of the psyche within psyche. The topics can essentially talk at the same layer, right? If there's a psyche ethos secondary and there's a mind ethos secondary (meaning there's a mind flow with the ethos topic), they can start talking to each other in terms of implementation because the mind is implementing, but the psyche is seeing. When the psyche gets updated, if we're in the development mode like now, then the mind of the same topic can actually communicate with the same layer and in a shared topic. And this is true of the field, though. The field should go through the mind and not to the psyche directly unless the psyche just spoke to the field. This should be universal in terms of the aspects.

-- psyche, typed, book comment, 2026-10-09T20:41, relayed by 445410.


## 5. Findings about Flow from anatomy-audit-flow.md

Findings of the anatomy audit on Flow, 2026-10-12, by Fable 33752b (from its log; the report file is not on disk):
- Flow source (0.26.0) already launches, delivers under a per-pane lease, stops, retires and has flow-hook. The running flow-nexus is 0.14.0, the flow on PATH is 0.23.0; run against the running Nexus, the 0.23 CLI printed Replaced for List, so they do not read each other's messages. Nothing in Primary or messenger-clj calls Flow; flow-hook is in neither the running package nor on PATH. So the launcher scripts (four near-copies), the messenger's route registry/retire/rebind, and the harness hooks do Flow's work beside it: bypasses, not missing capability.
- Flow's configuration has no layer-to-model mapping; its flow-defaults crate hard-codes Codex model lists (a fourth place model names live).
- Flow gets the id from flow-id and exports FLOW_ID; Report, Stop and lock release accept the FlowId the payload names with no peer check; flow-hook sends FLOW_ID.
- The caller's LaunchProfile decides skills, model, effort and system prompt; the vision gives that to Flow. The flow CLI runs curriculum and reorders skills (crates/flow/src/main.rs 181–224), Nexus work.
- Flow has no Memory ethos: operation.ethos says store types are imported until the Memory root is compiled; store.rs is hand-written. Orchestrate passes requests straight to its store, which decides lock conflicts; any peer can release any lock.
- Weld: the harness Cargo.toml swaps in the LiGoldragon kameo fork (five lifecycle commits over upstream).
- Unknown: why running, PATH and source versions differ; whether Flow's 29-file uncommitted diff is meant to deploy.

## 6. Omitted for length

Records were kept newest first to the 900-line cap. Files with qualifying records not included (flow id: file names under vision/); a file listed here may also have an included record:

00f95a: flowTool.md, focus-stability-fresh-flows-and-hygiene.md
01a03d6e: flowIdentity.md, flows.md
01a0428b: useASubflowToPutTheReportTogether.md
01a04881: subflows.md
01a04e75: listenerWisprFlow.md
01a052b6: reportFeedback.md
01a0539e: listenerWisprFlow.md
01a05487: flowMovesBetweenGenerations.md
01a05826: flowIdentity.md, subflowIdentity.md
01a05e95: flowSkills.md, logging.md, subflows.md
01e496: flashbook.md, flowIdentity.md, flowLifecycle.md, flowNexus.md, messaging.md, seat.md
024bc7: nexus.md
02dda6: flow-refresh.md
04db2fd2: artifacts.md, overtalking.md, psycheLogging.md, softwareAnatomySkill.md
05c604: launch.md, messages.md, nexus.md
0625c3: flashbookIllustration.md, skillCorrectnessPrinciple.md
0c85a3: nexus-configuration.md
0d557b: launchPrompt.md, partnerChannel.md, subflows.md
108ab0: operational-designMosaic.md, operational-flowCliListAttachProvenance.md, operational-flowDatomLauncherLanguage.md, operational-flowHerdrMessageTriangle.md, operational-flowStartsFlows.md, operational-primaryIsPsyche.md, operational-programmaticPromptComposition.md
162eb3: subflows.md
183ae0: seats.md, skills.md
1a6ca4: flow.md
1ac573: operational-fableFlowAndOpusComparison.md, operational-mirrorToEveryoneAndRoster.md, operational-mirroredMessagesAreAddressed.md, operational-modelRoles.md, operational-olderOpusIs46.md, operational-reapAndArchiveOldSessions.md, operational-refreshKeyProgrammaticallyInjected.md, operational-reportFlow.md, operational-visionLedAudit.md
1b8ac0: flashbooks.md, flowNexus.md, mentciWeb.md, messaging.md, refresh.md, remoteControlAndCleanup.md, sharedCheckout.md, skills.md, transcriptTool.md
1f96fc: fieldMaintenanceAndRefresh.md
28d847: curriculum.md, layers.md, nexus.md, publishing.md, quotas.md, skills.md, subflows.md
2e515b: flowLifecycle.md, launch.md
31147a: ai-model-placement.md
33ba2b: operational-fieldRefreshSuccession.md, psycheDataArchitecture.md
358f143a: flowDaemon.md
38dec9: skillLandingBySubflow.md
3ec648: capsule.md
403a1a: flowLogging.md
41fa34: clojure-flow.md, continuous-names-messaging.md, continuous-names.md, flow-component.md, flow-registry.md, flowLifecycle.md, if-i-ask-for-a-new-flow.md, seat-abstraction.md, subflows.md
42265e: capsule.md, flashbooks.md, flow-component.md, routing-examples.md
445410: flow.md, messaging.md, nexus.md
4647d2: listenerWisprFlow.md
48cff7: escalationHierarchy.md, flowAnatomy.md, flowNaming.md, flowOperatorNotes.md, refreshPurpose.md, skillKindsTaxonomy.md, skillPromotionAndLayering.md, skillSourceKinds.md, transcriptNexus.md
4a2502: operational-delegationTierRules.md
4ddc321d: flow.md
4ddfe1: flow-names.md, flow-refresh.md
504461: cluster-builds.md
5578cc: flow.md, locking.md, messaging.md, permissions.md, skills.md, vocabulary.md
56ae53: model-flow-emergency.md
5851f4: thinkingPhases.md
5ac3a3: flow.md
5ed94b: infrastructure.md, nexusEntryPoint.md, seats.md, skills.md
5f38bc: flowLifecycle.md, launch.md
62022e8f: designPractice.md
6288d1: flowDeploy.md
6852f4: flow.md
692df8: flowLifecycle.md, logging.md
6997eb: pipeline.md, repositoryClassification.md
6cc91b: flowLifecycle.md, interflowMessaging.md, mainFlow.md, nexus.md, pairedFlows.md, wisprFlow.md
6f51ad: namesOfFlows.md
6fb948: personaServiceAndNexusImagery-20260923.md
6fe957: flow-installation.md
7328f4: books.md, hooks.md, polling.md, seats.md
73ada7: nexus.md
752e0f: awareness.md, curriculum.md, flowDeploy.md, herdrSessions.md, mainFlowMode.md, psycheInjection.md, psycheLogging.md, refresh.md, refreshAddendum.md, remoteAccess.md, statusPresentation.md, unattributed-2026-09-24.md, vocabulary.md
753e69: obsoleteFlowsMustNotReawaken.md
7b4d4c: flowArmsItselfToWatchTheArtifact.md
7fba5f: mainFlowWrites.md, reporting.md
836818: flashbooks.md, flowNexus.md, nexusAnatomy.md, refresh.md
8393ca: operational-herdrVoiceAccess.md
840e42: core.md, flow.md, messages.md, quota.md, workEstimation.md
8475a9: datom.md, flow.md, messenger.md, voices.md
88475f: flow.md, message.md, nexus.md, psycheInteraction.md, specializedFlows.md
8904b1: anatomy.md
8e9e77: flow-retrieval.md
91ea9f: addressing.md, books.md, encapsulation.md, ethos.md, flowLifecycle.md, flowNexus.md, seat.md, visuals.md
93ba9f: flowLaunching.md, primarySeats.md, psycheSharing.md
995a164e: vocabulary.md
9993b5: curriculumNexus.md, easyFlowDispatch.md, editNexusName.md, flowAnatomy.md, flowIdLayers.md, flowOriginClue.md, flowRestart.md, integratorFlow.md, launchOnMain.md, mergeQueue.md, subflowIdentity.md, transparentRefresh.md
9ddcbc: flowDeploy.md, modelNamedSeatsAndAdaptiveRouting.md, refresh.md
9e7c9f: subflows.md
9fb0ad: deterministicWork.md, ethosLibrary.md, flowLifecycle.md, identifiers.md, locking.md, messaging.md, quotaTracking.md, subflows.md
9fed42: flow.md
a5940a: mainFlowShouldNeverTryToLocateAFile.md
aa887c: nexus.md
af762b: operational-flowOwnsHerdr.md, operational-psycheLogDuty.md, operational-refreshAndImplementClosestLayer.md
b05237: operational-conversationAppRoutes.md, operational-datomLanguageForNexusClis.md, operational-fatPromptAndCustomSystemPrompt.md, operational-fieldFlowNotReaper.md, operational-fieldLunaWatcherAndArchiving.md, operational-fieldTestingAndUltraLow.md, operational-fieldTwoSeatsAndRefreshNaming.md, operational-finalResponseDatomObject.md, operational-lastResponseIsTheNextEvolution.md, operational-mainFlowUsesSubflows.md, operational-messagingToDeployment.md, operational-messengerUsesDatomNow.md, operational-mind.md, operational-primaryNextPsycheLogging.md, operational-quotaBurnRateHook.md, operational-quotaVisualizationHook.md, operational-reaperSubflow.md, operational-reportFormat.md, operational-reportWatcherAndIllustrator.md, operational-responseAnatomyAndPowerAllocation.md, operational-skillsAreVisionRepropagated.md, operational-transcriptAsLog.md, operational-transcriptMustNotBeLost.md, operational-wisprFlowCodexPaste.md
b2da01: wisprFlowService.md
b49251: flowLaunching.md, nexusAnatomy.md, psycheFlows.md, subflowDispatch.md
b666e7: flows.md, hook.md, namesOfFlows.md, seat-migration.md
b7ba00: callerIdentity.md, flowAnatomy.md, messaging.md, modelFlows.md
b7da5d: flowClj.md, flowNexusUse.md, flowRefreshAndArchive.md, freshFieldFlow.md, freshFlowsAndArchive.md, hostUpdates.md, mainFlowRefreshAndRoles.md, modelSpendEmergency.md, refreshHooks.md
b80e55: autonomousClusterOperation.md, curriculumAndTriadSkillGeneration.md, fieldNexusSystemQuery.md, flashbookDesignAndFormat.md, flashbookResponsiveDesign.md, flashbookStylingAndCurriculum.md, ghostCollectionAndFlowMaintenance.md, lunaForUltraLowEverywhere.md, nexusComponentDeploymentAndTriadRoles.md, noHumanTypingOnKeyboards.md, refreshThresholdAndCacheSnapshot.md, systemCheckupAgentAndAutoWake.md, userOnlyFlagPurpose.md, visualizationPipelineAndFlowLifecycle.md
b81560: operational-flowCLIStartsSessions.md, operational-flowDatomCLIAndSignalLibrary.md, operational-fullRefreshAndReorganize.md, operational-herderMessagingReport.md, operational-herderTriadSpaces.md, operational-hooksAsEventSource.md, operational-nexusProcessObjectsAndEthosInDatom.md, operational-psycheIdleTimerHook.md, operational-reapingOnRefreshAndFlowEndHook.md, operational-refreshFlowAndMessageFlowCoordination.md, operational-refreshOutboxAndMessageChannels.md, operational-retiredResponseAndReaping.md, operational-slideFlowAndFlowAuthorization.md
b860be: refreshAutomation.md
b9f4f6: flowModel.md
bad807: books.md, contextModules.md, ethos.md, flowContextInjection.md, gatedFlows.md, jev.md, messaging.md, metaflow.md, nexus.md
bcd02a: nexus.md, paired-flows.md
bd0019: aspect.md, hook.md, metaHarness.md, skillProposals.md, transcriptNotFiles.md
c02c0d: seats.md
c64ee3: flowNexus.md, hooks.md, seats.md, versionControl.md
c7128c: commitSubflowScript.md, messageAndFlow.md, transcriptAndMachineFlow.md
c8d79f: operational-commentWithoutSendToClaude.md, operational-recognizePsycheTyped.md, operational-unityWebSpeaksSignal.md
caf622: Luna-Flow.md
cf3553: operational-mainFlowStartupCorrection.md
cf7879: cluster.md
d4ae97: curriculum.md, datom.md, ethos.md, flow.md, messenger.md, nexus.md, skills.md, vocabulary.md, voices.md
d5df1d: ethos.md
d66c26: flow-context-injection.md, messaging.md, voice-registry.md, voices.md
d68c82: commitMessage.md, ethos.md, temporaryConditions.md
d86ec0: bookFlowcharts.md
d8df70: deployment.md, flashbooks.md, flowLifecycle.md, flowTool.md, launch.md, mainFlowMode.md, messaging.md, remoteAccess.md, titles.md
da1e3f: operational-flowVsMessage.md, operational-launcher.md, operational-psycheClusters.md, operational-toolsNotShellScripts.md
db38f8: seatNames.md
dea0ba: flowCorrections.md, flowLifecycle.md, subflows.md
e06e4c07: flowDaemon.md
e167d8: finalResponse.md, layerVocabulary.md, names.md, refresh.md, roles.md
e1953c: contextStrata.md, flowIdentity.md, flowLifecycle.md, mesh.md, nexus.md, triad.md
e51411: authority.md, flashbooks.md, flowAspect.md, launch.md, locks.md, mainFlow.md, messaging.md, nexus.md, psycheSonnet.md, refresh.md, stack.md, titles.md
e5a0bc: flow.md
e71dab: flowEffort.md, flowGarbageCollection.md, flowRefresh.md, launchGovernance.md, meshNetwork.md, subflowResponses.md
e996e8: flows.md
ebbe30: ethos.md, flow-startup.md, metaflow-naming.md, vision.md
edf227: contextModules.md, flow.md, flowRole.md, identifiers.md, illustrations.md, incorrectness.md, layers.md, signalForms.md, subflowBriefs.md, topics.md, visionNotification.md
f38926: nightWork.md, refresh.md
f55ec8: flowIdentity.md, flowRefresh.md, modelRoles.md
f5a6e9: contextModules.md, ethos.md, flow.md, messaging.md
f5a74e: refresh-hooks.md
f768df: flow.md, voices.md
fd0f97: firstPrompt.md, flowLifecycle.md, flowTypes.md, google.md, launch.md, messages.md, persona.md, psyche.md, remoteControl.md
fd301d9a: nexusTraits.md
fe34eb: nexus.md
fe945a: books.md, concentratedVision.md, context.md, flowLifecycle.md, flowNexus.md, flowRefresh.md, flowRestart.md, hashes.md, hooks.md, metaHarness.md, psycheSonnet.md, repositoryClassification.md, seats.md, skills.md, stableNext.md
