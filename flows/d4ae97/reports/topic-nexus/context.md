# Nexus design: starting context

Topic: Nexus, the long-running component (Signal, Operation, Memory), and
messaging between flows, with messaging to use Flow and the component to be
called Message. Assembled 2026-10-09 for flow d4ae97 from files read that
day. The partner topic flow is Ethos design; its context is
`/home/li/primary/flows/d4ae97/reports/topic-ethos/context.md`, which holds
the ethos roots, kinds and datom.

The order, as logged (`/home/li/primary/flows/d4ae97/vision/messenger.md`,
2026-10-09):

> Nexus/a little bit of messaging in terms of remaining aware of the fact that we want messaging to use Flow. I mean, message should be called message.

How to read this file:

- Section 1 quotes the distilled, approved psyche: the vision- skills on
  Nexus, Signal, Sema, messaging and Flow, from their authored sources
  (psyche-skills at 4312cc0). Each skill is quoted whole except its front
  matter and its `## Sources` list; headings are lowered two levels, the
  text is otherwise exact. `/home/li/primary/Vision/nexus.md` and
  `/home/li/primary/Vision/messaging.md` are older copies of vision-nexus
  and vision-messaging and are not quoted.
- Section 2 quotes knowledge-nexus and knowledge-flow: the machine-written
  description of what runs today (mind-skills at 37ca3f7), a claim, not the
  living's word.
- Section 3 quotes raw psyche records newer than the skills or absent from
  them, verbatim with their record headings, oldest first. Records marked
  notion are the living thinking aloud. Bracketed words and [sic] marks are
  the logging flow's, as logged. Flow is quoted where messaging depends on
  it; Flow's own design (metaflow lifecycle, context modules) is cut.
- Section 4 lists where a raw record contradicts or moves past a skill.
- Section 5 lists the open questions and the books awaiting his rulings.
- Section 6 lists what was cut.

## 1. Distilled statements (vision- skills)

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-nexus.md`

#### A Nexus is the whole

A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.

#### A kind of thing

Nexus is our word for the style of component that speaks signal and uses a similar database.

#### Library and daemon

Every component built from now on is a Nexus. The nexus repository is
the library that defines the core of a Nexus component.

#### Universal traits first

The basic ontology of an actor and dataflow system is designed before
implementation; signal and sema are designed against it as if new, the
old code at most inspiration.

Every method lives in a trait; an inherent method is a trait not yet extracted. The traits and types of a Nexus are one ontology designed before any body is written; defaults wherever expressible, through rich sub-trait chains. Traits live on data-bearing types; a zero-sized type with behaviour is a namespace pretending. Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive, and every reference names its target by that name. `fn main()` is the only free function; a missing owner is a missing type.

#### Processing is for the effect

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. The name is open,
Apply liked.

#### Documents

The nexus and sema documents are undesigned; when they are designed
they live in the Nexus's main repository.

#### Sockets

A Nexus opens at least two sockets. The ordinary socket serves
ordinary peers. The meta socket is privileged — the root user of the
Nexus — and configuration and privileged operations pass through it;
every Nexus has one, since without it nothing could configure the
Nexus. A Nexus that needs more levels of access opens more sockets.

#### Default clients

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.

#### Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket.

Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.

#### The graph

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

Peers depend on each other's wire repositories, never on each other's Nexuses.

#### Routing

Signals cross the network through a router. The router tells signal
types apart by an enum that wraps the objects, held in the signal
repository, which every component depends on. That repository also
holds what every signal needs in common — the handshake payload
among it.

#### Configuration

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

#### First configuration

A Nexus keeps a standard metadata tree. In it a type records whether
the meta Configure was ever done; that record is reversed only on the
meta socket, and while it is unset Configure is accessible on the
ordinary socket. The tree holds everything standard about the Nexus:
its socket paths — its own and those of every edge-socket it connects
to — and whatever else comes up as standard nexus configuration data.
The built-in default configuration is independent of this and is
what gives the socket path on which the Configure signal arrives.

#### Repositories

A component has three repositories: its main repository, holding all
its code, and two signal repositories — one for the ordinary
socket's contract, one for the meta socket's. Shared kinds go into
reusable libraries, which are encouraged.

`<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, never optional, since configuration flows through it. The CLI is `<nexus>`.

A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies, the typed payload of each; no catch-all. Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves. Storage vocabulary never appears on the public wire.

#### Why everything is a Nexus

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability, quality, and clarity.

#### Actors

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

#### Splitting a Nexus

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.

#### Observation by subscription

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

#### Polling is forbidden

Polling is forbidden; a correct system goes quiet when nothing
changes.

#### Three parts and one path

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

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-signal.md`

#### Name

The serialized form is called signal.

#### What signal is

Signal is the messaging layer: fully binary, portable rkyv fixed
across endianness, fully typed with both sides knowing the full
schema, nothing on the wire labeling itself. It is one step from the
composition, beside the text chain.

#### Query and response

A Signal declares queries and responses; input and output are too
low-level for it.

```
Signal
[]                                     ; imports
[ Lock.LockRequest  Release.LockId ]   ; queries
[ Locked.Lock  Released.Lock ]         ; responses
[ LockId.Integer                       ; types
  LockName.String
  LockRequest.{ LockName }
  Lock.{ LockId LockName } ]
```

#### Text and signal

The textual form is datom; a CLI actualizes it and sends signal; a
Nexus never textualizes.

#### Meta signal

The meta signal is never optional: the daemon is configured only over
its meta surface.

#### Protocol

Signal is portable rkyv plus whatever protocol is standardized on top
of it. The protocol is to be decided.

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-sema.md`

#### What sema is

Sema is the database engine of a Nexus, authored in Ethos so the
stored types are visible; its root, Sema, declares record types. It
matters more than nexus, because operational editing should yield the
migration with the edit.

```
Sema
[]                                                        ; imports
[ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
                                                          ; the remaining sections are to be decided
```

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-messaging.md`

#### A message is a datom, and it arrives as one

The message body is a datom that lands in the recipient's prompt as a
datom-formatted object. There is no envelope around it.

#### Priority is a head on the datom

    Priority.[HardAbrupt MiddleAbrupt Soft]

#### Delivery is harness-specific, and the mechanism differs per tier

Hard abrupt on Codex is one Escape, and the prompt submits itself. Hard
abrupt on Claude is two Escapes — the first is taken by the input editor in
vim mode and never reaches the harness — then the prompt, then an explicit
Enter, because after an interrupt the prompt is placed in the composer
without being submitted. Middle abrupt is the terminal prompt, which a
Claude recipient receives at its next tool boundary. Soft waits for the
recipient to finish.

#### An interrupt witness is not a delivery witness

Inducing an interrupt, placing prompt text, submitting it, and the recipient
consuming it are four separate observations. None of them stands for
another, and a submission is never a read receipt.

#### Only messages that act, deliver, or block

Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.

### `/git/github.com/LiGoldragon/psyche-skills/skills/vision-flow.md`

#### What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

#### Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A voice is an aspect carrying a rank, `Psyche.Primary`: Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices. The model behind a voice is configuration, declared once in Flow and changed only over its meta wire; not every model is exposed to every voice. Voices are addressed by name; a flow id is for the ledger and the archive, and is written in words. A side flow is a job, not a voice: focused, not long-lived, gone when its mission is done; a message sent to it after that returns to its sender with notice that the flow has ended.

Speech runs horizontally between aspects at equal rank and vertically within an aspect one rung at a time. Field speaks to Mind, for what must be changed in code and documentation and tested before Field deploys it; Mind speaks to Psyche for judgment on design and choice, and rarely. Sol speaks to Opus, not to Fable; Fable is spoken to least. Design is Astra's, not Sol's.

#### Repository and skills

The flow repository holds the machinery of the Flow Nexus and is a
runtime repository. Every skill lives outside it, the basic skills
included, so that a change to a skill causes no Nix rebuild. The
basic skills give our own take on how an agent behaves in a harness,
replacing the prompt the harnesses build in.

#### A session is named after its direct ancestor

A session cannot be named for what it will become, because nothing is known
about it when it is created. Its ancestor is known exactly, so the ancestor
is the name.

#### A replaced session is reaped by the refresh itself

Reaping belongs to the refresh event, not to a later sweep. A refreshed flow
takes the replaced end out of receiving messages, so a dead end is never
left registered and addressable.

Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

#### Subflows replace the harness subagent facility

The harness subagent facility is replaced. It puts two flows into one
synchronous user interface and locks them both into a single main
flow. A subflow is instead an independent flow with its own system
prompt, which can reply to the successor of whoever it was meant to
answer; that makes the system asynchronous. Subflows run under their
own system prompts because they need different prompts.

#### Subflows are created from the questions and requests a flow ends with

Creating a subflow is a routing job: whether there is already a flow
that should simply get this message or this question. A special field
flow running on ultra-low power checks every question and every
request a flow ends with, and, according to the ending flow's
authority, spawns subflows given those questions and requests to
answer or fulfill.

#### The requester holds only a request ID

The requester holds nothing of the subflow itself. It is assigned a
request ID, by which it asks later for status, asks for more detail
about what that subflow is doing, and sends the subflow messages
while it is alive. When the subflow is done, the requester receives a
message if it is still the flow in charge.

## 2. Machine-written description of what runs today (knowledge- skills)

Written by machines; a claim about the current runtime, not the living's word.

### `/git/github.com/LiGoldragon/mind-skills/skills/knowledge-nexus.md`

The retained Home 83 runtime packet records Home Manager generation 1045 as active. Generation 1039 remains an executable rollback.

Field's retained Home 83 result reports the running server engines as Orchestrate Nexus 0.37, Flow Nexus 0.23, Message Nexus 0.19, and Lojix Nexus 8.1. It reports these stable socket pairs:

- Orchestrate: `/run/user/1001/orchestrate-nexus/orchestrate.sock` and `/run/user/1001/orchestrate-nexus/orchestrate-meta.sock`.
- Flow: `/run/user/1001/flow/flow.sock` and `/run/user/1001/flow/flow-meta.sock`.
- Message: `/run/user/1001/message/message.sock` and `/run/user/1001/message/message-owner.sock`.
- Lojix: `/run/lojix/ordinary.sock` and `/run/lojix/meta.sock`.

Field's result further reports that the regular `PATH` resolves Flow 0.23 and Message 0.19 clients from the same package closures as their running servers. Until the retained reader receipt is available, treat that closure correspondence as attributed Field evidence. This packet does not establish store-engine versions, a wire contract, active seats, or a successful launch. Read the current source and the live target's explicit response before making any of those claims or changing a Nexus.

### `/git/github.com/LiGoldragon/mind-skills/skills/knowledge-flow.md`

The retained read-only receipt distinguishes the Flow client from the running service: `/home/li/.local/bin/flow` reports 0.23.0; `flow-nexus.service` MainPID 1524809 runs `/nix/store/j689l77bmlfmgc6ichksrqnnmdnma8ig-flow-0.14.0/bin/flow-nexus` and reports 0.14.0; and `/home/li/.nix-profile/bin/flow-nexus` on `PATH` reports 0.12.2. The PATH binary is different from the running service. Separately, the historical corpus record at `/home/li/private-repos/flow-evidence/42265e/fable-restart-context/sources/flows/bad807/reports/ethos-nexus-corpus.md:8709` lists ordinary and meta sockets at `/run/user/1001/flow/flow.sock` and `/run/user/1001/flow/flow-meta.sock`; it is not a current endpoint witness.

This packet does not prove that a FlowStart request, a seat, a hook, or a native first user turn succeeded. It also does not establish a deployed Flow 0.24 route. A private experimental Flow 0.24 instance, if present, is separate from the deployed service and cannot support a claim about it.

Before launching, naming, claiming, reaching, or reporting a Flow, read the matching deployed source and obtain the target's explicit response through the current ordinary or meta socket. Do not infer protocol, caller identity, store state, or runtime bindings from a version number or a client path.

The native Codex launcher has a witnessed Tertiary launch: its retained
receipt records an authenticated remote binding, the source checksum
`03004fccf89aad2e053e955f5f4926ecbcd7ee8eb1e335bd2b6ed0aca22bf234`,
and an accepted first turn. That evidence qualifies the launcher only for
that profile. Mind.Primary remains unresolved, so it does not qualify a
Mind.Primary launch, replacement, or retirement decision.

## 3. Raw records newer than or absent from the skills, oldest first

### `/home/li/primary/flows/6cc91b/vision/messenger.md` (2026-09-13)

#### 2026-09-13 — Whatever message is called, Messenger or the noun, use that for the messaging

Context: answer to the placement fork (extend the existing Rust message crate, or the nexus core). "Messenger or Messenger" is left as transcribed; the two spellings were not distinguishable in speech.

> Yeah, on your first point, the message was also slated to be called Messenger or Messenger. I think also, orchestrate was to become orchestrator, but it looks like we've been leaning more towards the noun lately, because psyche, orchestrate, or what was the plan anyway? Whatever it is called, we should use that for the messaging.

-- psyche, STT.

### `/home/li/primary/flows/6cc91b/vision/nexus.md` (2026-09-14)

#### 2026-09-14 — Nexus, core, and metaNexus are the explicit terms; the core library guards that the signal actor never talks to the sema actor

Context: comment on the gap "almost nothing runs". "Sima" is speech-to-text for Sema; corrected in the quote. "demon" left as written.

> Yeah all these things have to be re-anatomized. Also I was thinking the Nexus core library could be how the signal actor, the Nexus actor, and the Sema actor (the main actors in a metaNexus, as we could call it, or the whole of what people call a demon) could be. If we want to be explicit we can say metaNexus and core Nexus but if we say Nexus we sort of have to let the context imply which one we are talking about. If the context isn't obvious then the speaker is blamed for not being clear enough: which part he means by Nexus.
>
> Nexus, core, and metaNexus are the explicit terms. The Nexus core library has all of the interfaces and kinds defined for how to build metaNexus and it has the machinery to make sure, ideally at compile time, that there is no signal-actor-to-sema-actor communication possible. All interaction between the signal actor has to go through the Nexus and then the Nexus ethos type file.
>
> We have this Nexus type, the sema type, and the signal type and they each have their own intrinsic kinds applied to the types so that they're of that specific actor. Only this kind of actor can react with this type of object. It's like a kind becomes a higher-type kind compiler check: an architecture guard basically.

-- psyche, typed, artifact comment.

### `/home/li/primary/flows/692df8/vision/messages.md` (2026-09-15)

#### An ethos type for messages, with variants; datom syntax as the standard communication everywhere, even the system prompt; a self-defining syntax standard

Context: said to the primary Claude on 2026-09-15 after a relayed prompt arrived with a JSON provenance header from tools/prompt-relay; written by an extraction subflow from the transcript.

> What is that JSON payload in the message that's really ugly? I don't want that. I want to specify an ethos type for our messages with different variants, and I want that to start becoming a standard way to communicate, so that you're going to start using datom syntax so much. It's going to be everywhere: all the CLIs, everything. Essentially, we're going to move everything into a specified communication on the models, so even the system prompt is going to be in a specification of that. I'm starting with its spec and ethos. It's like a self-defining syntax standard. It's actually brilliant when you think about it. This is going to change the game for machine learning.

-- psyche, typed.

### `/home/li/primary/flows/da1e3f/vision/operational-flowVsMessage.md` (2026-09-17)

#### `flow` is the ordinary CLI of Flow Nexus, and its job is to start or refresh a flow — not to send messages. Messaging goes through the Message Nexus, whose ordinary CLI is `message`. Two Nexus, two verbs; don't conflate

Context: typed to primary Psyche opus (Claude flow da1e3f) on 2026-09-17 correcting me twice in a row. I had first proposed a `flow-send` tool (rejected: use `message`), then muddled `flow`'s role. Logged by the main flow before acting.

> no, message, not flow-send. use the message nexus!

-- psyche, typed.

> flow is to start or refresh a flow

-- psyche, typed.

### `/home/li/primary/flows/da1e3f/vision/operational-flowVsMessage.md` (2026-09-17)

#### Some features on Flow Nexus require the meta socket, like consuming a usage reset — those go through `flow-meta`, not the ordinary `flow`

Context: same message thread, continuation. First named example of a meta-socket feature. Logged by the main flow before acting.

> or to access some other features, some require the meta socket like using a usage reset

-- psyche, typed.

### `/home/li/primary/flows/c7128c/vision/messageAndFlow.md` (2026-09-18)

#### 2026-09-18 — Messaging to the psyche through XMPP if still the best candidate; reporting automated onto the message datom language and the Message Nexus; Message gets data from Flow, Flow can lock

Context: spoken directly by the living to Fable (Claude, medium, flow c7128c), as the deployment-closest layer to implement once a flow is refreshed. Input mode not stated.

> - Push on messaging to psyche through XMPP, if that's still the best candidate.
> - The automation of reporting and moving over to the message datom-based language, the message Nexus for messaging each other, which we'll just use.
> - Message can get the data from Flow, and Flow can put a lock on some stuff.

-- psyche, direct to Fable c7128c; input mode not stated.

### `/home/li/primary/flows/b81560/vision/operational-flowDatomCLIAndSignalLibrary.md` (2026-09-19)

#### The flow CLI is datom payload, not subcommands. All CLIs use a signal CLI library that forces the pattern. Ethos is a visual language for cognitive density. JEV shows this is the way. The help and everything can be generated by macro from ethos code

Context: artifact comment by the living on the Session Flashbook, 2026-09-19,
on the "Flow CLI starts everything" card, anchored at `flow start PsycheHigh`.
The living corrects the syntax and expands into the CLI architecture vision.
Logged by the main flow before acting.

> No, that's the wrong syntax. It would be Flow, and then quote, and then you would write a datom payload for Flow. You would probably have a command that is more convenient and more biased, like ensure or start, and then you name a row, right? It ensures that it's not already running, or start, but it would probably have a thing where, if you try to start a cykhi, it would say there's already one, I guess.
>
> I don't know, maybe we just call it start, and by default it tells you one is already started. That's how, or refresh self, the flow ID could be one of the things that have to be specified. The flow CLI also reports in the whole message, which is a request-type message, which has one of the fields filled automatically by the CLI because it knows which process at this operating system level invoked the CLI, which process made this request.
>
> We're going to make this standard. Let's make this standard. Let's make us a signal CLI library and make a bunch of standard macros or maybe a library, and maybe some ethos, even objects that define the process, the type of process, the things that we're interested in to visualize it ourselves, and ethos to think about it from a user's point of view, like any important type in any project. Any type should be defined in ethos, especially signal, so we can see the message shape.
>
> Ethos is basically a visual language. It's made for high cognitive density per amount of LLM-contained, tokenized cost. Even further down, when the LLMs are trained with this type of syntax, which is going to make them even smarter, the exponential gain of cognitive density of this high signal of direct meaning that this has over any other just plain text, even with structure there, Markdown is there because it has value. The structure has meaning, so it's already something that's happening. JEV, with its success, is showing that this is the way to go. So the flow, or whatever the message is, is just that all of our CLIs are like this. Let's make this very clear at the high level in the skills and the vision: we make the library, and all the CLIs have to use the library to force them into this pattern.
>
> All of the CLIs just take a datom payload, all the options, all the help, and everything, which can be added on. The help for everything can be built in by some kind of macro that does the CLI stuff. That could involve some Ethos code also, where the macro generates code that is baked into Ethos. That's also a possibility. I don't see why not. I think you could design that quite easily.

-- psyche, artifact comment on Session Flashbook. ("cykhi" likely reads "psyche high"; STT.)

### `/home/li/primary/flows/1b8ac0/vision/messaging.md` (2026-09-21)

#### Open the Raw capability on the meta socket; expose the meta socket to everybody for now as the unsafe interface; the message CLI uses Raw as a fallback when the checked interface is not there; commands are a typed queries enum set graded by how secure they are

Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21 after reading FM7 · Raw or FlowLocked in the Flow/Message question collection. Input mode STT. Locator appended below by a subflow. Logged by the main flow before acting.

> So the raw or flow lock just gave me an idea. It means that you open the raw capability on the meta socket. Right now, we can just expose the meta socket to everybody, so we can expose the unsafe interface. They can use the new message CLI in Nexus with the raw method as a fallback if the checked specified interface doesn't work (because there's no flow lock yet or something else). They want to debug or inject a command or something.
>
> We should have a typed command too, a queries enum set, depending on how secure they are, right? Some harnesses don't allow a lot of commands to be run when their model is running.

-- psyche, STT. 1b8ac00b, line pending.
Locator: 1b8ac00b:1706, 2026-09-21T21:44:14.216Z.

### `/home/li/primary/flows/1b8ac0/vision/messaging.md` (2026-09-21)

#### Exposing the meta socket to everybody means locally only

Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21, answering the anatomy question whether "expose the meta socket to everybody" reaches across hosts. Input mode STT: "Metolaca" reads "meta socket". Locator: the message after 1b8ac00b:1664 in the same session; line to be appended. Logged by the main flow before acting.

> No, when I say "reach the Metolaca," it's only locally, obviously.

-- psyche, STT. ("Metolaca" reads "meta socket"; corrected here, left as spoken in the quote.)
Locator: 1b8ac00b:1753, 2026-09-21T21:46:13.337Z; typed confirmation "The meta socket" at 1b8ac00b:1762, 2026-09-21T21:46:22.635Z.

### `/home/li/primary/flows/1b8ac0/vision/messaging.md` (2026-09-21)

#### FlowLock does not degrade to Raw: Raw is on meta and not usually accessible; FlowLock messages are the ordinary sends and Raw is FlowLock off, a shorthand; Flow is the only writer in a Herdr session, locks the session for the message, sends the text, unlocks, and answers Message with success or not

Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21, correcting PsycheHigh's framing of the living's earlier idea as a "fallback" and answering Mind's conflict (accepted decision: FlowLocked refuses with no downgrade). Input mode STT. Locator to be appended by a subflow. Ends with a working instruction ("Let's find all the problems and the anatomy involved in that"). Logged by the main flow before acting.

> No, I didn't say that the Flow lock degrades to raw. I said raw is on meta, so it's not usually accessible. Flow lock is basically that we can have it be a synonym or a link to what we're talking about: Flow lock messages, right? Just send, right, or whatever, send to, or all of these would be Flow lock messages, and then with Flow lock off, which could be synonymous with raw, you can have these shorthands like raw.
>
> It's just a shorthand for a certain configured type of messaging request, or a request to send this text into a particular harness. Flow takes care of the rest of making sure that there's no other writer because it is the only process that can write in that herder session. Eventually, it can safely send the message because it knows that nothing else is going to come in because it's locked that session for a message, right?
>
> It locks the message for the session to send the message, then it sends the message, then it removes the lock. The messaging will send a request to Flow to send the message, and Flow will say, "Yes, that window is locked." I guess Flow would even be the part that sends the text, so message wouldn't need to make this a two-part thing. It would just ask to send a message to a certain Flow, and then the Flow would say successful or not, basically.

-- psyche, STT.
Locator: 1b8ac00b:1872, 2026-09-21T21:49:14.522Z.

Repeat note (2026-09-21): the FlowLock statement above was sent a second time a few minutes later with a small transcription difference ("Flowlock is basically a synonym or a link to Flowlock messages, right? All of these would be Flowlock messages"); same statement, not a new one; the first hearing's locator stands.

### `/home/li/primary/flows/836818/vision/nexusAnatomy.md` (2026-09-23)

> Ask me questions to design everything with the flow and the message. Let's get this new infrastructure up:
>
> - the persona
> - all of the nexuses
> - the main nexuses
> - how they fit with each other
> - how they interact with each other
>
> The message highly depends on flow and probably many things will then depend on message.

-- psyche, typed, 2026-09-23, directly to Psyche High 836818 over Remote Control. Transcript locator: this seat's native session, the first living turn after the concept-plate review (line to be fixed by a locator subflow).

### `/home/li/primary/flows/836818/vision/flowNexus.md` (2026-09-24)

#### The living's answers to the six questions, 2026-09-24

Heard by Psyche Medium d8df70 as comments on "What Waits for the Living" (14:28 to 14:32 UTC) and its instruction "Talk to Fable about all this and get Mind and Field to adapt the answers into code and deploy." Raw records with the words: flows/d8df70/vision/flowLifecycle.md, building.md, flowTool.md, messaging.md (commit 24077d45). Quoted here because they replace this seat's provisional rulings.

> A seat starts receiving. The old seat stops receiving first. That's how we get a lock. I'd rather use the word "flow" also, but do you mean something else by "seat"? A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently.

> Well when the builder isn't reachable we just build locally.

> I'm not sure what you mean. How do the running services get back to the known source? They're built and installed from CriomOS so you can check the source that built that generation. I guess find out how that link is made if you want to know.

> Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

> If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules. Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it. In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

-- psyche, typed as comments, 2026-09-24, to Psyche Medium d8df70; "createoms" and "Psyq" repaired to CriomOS and Psyche by d8df70.

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### A streamlined, aerodynamic messaging interface with a shorthand version

Context: the living, while 93ba9f was locating the letter-type Ethos and relaying session closing to Luna Field.

> We need a very streamlined and aerodynamic messaging interface so that there is very little noise. I don't want resistance, I don't want all these hashes, and I don't want all this extra unnecessary information. Even if the ordinary message API is complex, we create a shorthand version which has a shorthand response type or display type.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### Raw flow send is a meta socket operation; a lock-enabled deliver message for messages

Context: the living's comment on the "e167d8 Night Summary" book, at its line on design forks F1–F9 and the tension between dropping raw Flow send and the earlier "use it raw". Retrieved by a reading subflow of 93ba9f.

> A raw flow send (as in typing directly into the pane, into the harness) I think should be a meta socket operation and then we have a more lock-enabled deliver message. Maybe that is a safer operation for messages to use.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### No message ID; a different interface for history; the sender is psyche primary, psyche secondary, etc.

Context: after 93ba9f proposed removing the message ID from the pane letter and asked whether the living's sender name should stay "Owner" or become "Living".

> You didn't show me the ethos. I still don't know what the other variants are of text. We shouldn't get the message ID. We're going to develop a different kind of interface to get message history. We're not going to get by message ID and the sender being called "owner" is fucking ridiculous. The message has to be able to figure out who the sender is programmatically eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### A set of all senders and variants

> We could make a set of all of them and variants.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### Simple and full; psyche at the top level with full and short forms; age; kinds of messages

Context: after 93ba9f showed Content's variants (Text, Psyche, Psyches) and asked what else a letter should carry.

> Okay no, these will be different. Let's do it differently. We have the [soft] variant but maybe we even have the soft message, the soft psyche. These are shorthand. That's what I mean by shorthand and they become... You should have, at the top level, even a psyche, right? Sharing a psyche means sharing something that psyche said and it maybe even has an inner variant for the verbatim, like speech-to-text or if we know or unknown. We have the short variants too for the response:
> - The full psyche with the date and stuff
> - The short psyche, which is the context
>
> Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there. It could be in the metadata but we don't need to obsess over metadata. Let's just put it in as we need it.
>
> The other thing that could be there is a human-readable or, actually, an LLM-readable but more human-friendly time measure, like age. Depending on the scale we're talking about, seconds, minutes, hours, days, and months and years, right? We can use those as measures of time, like age basically.
>
> You have this: not necessarily a short response but a human response. You have this human prefix and then you create these human variant responses. You have the not-human but simple. Simple is better:
> - A simple message, a simple psyche
> - A full message that can have many fields, one of which is a vector of psyches that are essentially the support for that message
>
> We have certain kinds of messages like:
> - An order
> - A question
> - A request for an audit
> - A request for some information

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### Datom has variants, not tags

Context: 93ba9f had asked whether a letter of "tag, Flow ID, and text" (a speech-to-text record an earlier flow attributed to the living, 2026-09-25) was the living's wording.

> And I don't know what you mean by tag. Datom doesn't have tags, has variants.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

Context: 93ba9f had answered that "tag" meant nothing to the living and dropped the earlier record as a likely mishearing.

> Nobody said the word means nothing but you're talking about a tag when we were talking about [Clojure] so you're confusing things. It's not that I don't understand what the word means, it's that you're using it out of context.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### The head is the message's kind, a new type carrying all its data; priority leaves the letter; soft and hard was the wrong approach

Context: the living's comment on the "Two Books Compared" artifact, at "Priority is a head on the datom." Retrieved by a reading subflow of 93ba9f; relayed by direct Herdr prompt after the Noema book was published (21:04). The trailing "..." is as returned.

> Actually the head is where we put not only priority. Maybe sometimes the priority is implied but this is where the message type is. We can make any number of kinds. If we want a certain different kind of message, then we can create it there. It's a new type and it carries all the data.
>
> We can have the spec easily in the skill that Ethos shows what kind of objects should be expected in each place so that these can be understood when they come in. You could have, let's say:
> - a psyche update
> - a hard psyche update, which interrupts
> - a soft psyche update
> - a psyche update, where maybe there's a middle ground of interrupt
> - an implementation report
> - an audit report, even the software or the hard version
>
> Arguably the audit report is all going to be the same: the soft or the hard. Do we really even need to tell it if it's soft or hard? Do we even need to tell the model if it's a soft or hard message? I don't know. I don't think so. The database can know it, so if he wants to know he can find out but I don't think it's going to matter. We'll make the judgment of what kind of messages we want to break harder than others so it's just what kind of message it is, really.
>
> We don't even do the soft or hard, actually. That was the wrong approach. For the normal format that gets communicated, the non-debugging format, basically the production requests and responses (are those what we call them? Queries and responses) ...

-- psyche, typed (artifact comment), 2026-09-26, relayed by 93ba9f.

### `/home/li/primary/flows/b7ba00/vision/messaging.md` (2026-09-26)

#### A primitive Message now: a few simple types with a string; "send up" to the higher layer, Message and Flow find the recipient

Context: while Fable writes the Sema book, the living asks for a primitive Message in the meantime.

> Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages, like what we've been doing so far. A better version of message should be redone and redeployed with just a string as the basic form. We're going to maybe develop it a little bit and then release it in the next version but we can have a primitive version of that while we do the database rename and stuff.
>
> Let's figure out the name for the database part. Let's get a better version of message, with just a simple anatomy of a few different types of messages that are simple and easy, like:
> - field report
> - psyche report
> - field question
> - psyche question
>
> Things like that, some kind of way to talk about a message from above. We could type the message based on the type, because if you send the message you have the same type. If you say "send up" it means message higher layer, whatever however we say that, let's find a clever way to say that: message to higher-layer type message. It just means send to the message. The message logic has to figure out where that's supposed to go so it can ask the flow, "Where does Luna field Luna send the message when it sends up?" or maybe the flow figures it out. I don't know but somebody's going to figure it out and the message will go to the right place as long as we know where it comes from.

-- psyche, STT, 2026-09-26, relayed by 93ba9f.

### `/home/li/primary/flows/b7ba00/vision/callerIdentity.md` (2026-09-26)

#### A Nexus learns which flow called from the calling process; a Signal standard; no agent says who it is

Context: same message as the primitive-Message request, on how a Nexus learns the origin of a call.

> It would be cool, actually, to just make the CLI help give the information in the signal whenever a call comes in to the Nexus. This is a standard thing that we need to put in Signal. It figures out the process that's calling and it can use that to talk to Flow to figure out which Flow used the CLI to send the signal that it just received. It can get its origin without the user having to say, "Hey I'm Psyche Fable." It would just know. That's really what I want. I want the user interface for the agent to be really simple and everything just works deterministically. That would be great.
>
> ... Even Flow can really benefit from knowing, "Refresh Flow, who called it?" and then it's going to refresh that one Flow.

-- psyche, STT, 2026-09-26, relayed by 93ba9f.

### `/home/li/primary/flows/b7ba00/vision/meaningLanguage.md` (2026-09-26)

#### The name is Sema; the database named Sema is renamed

Context: the living's comment on Fable b7ba00's "Noema" artifact, at the alternative name "Sema".

> Originally that was the idea. Sema was supposed to be the language of meaning and so that is actually the right name. It's cool that you brought it up. That means we rename all of the Sema aspect pertaining to the database. It's not that it's not true in the way it's going to store Sema, but not only Sema. We're going to just call it something else, something clever (the database).

-- psyche, typed (artifact comment), 2026-09-26, relayed by 93ba9f.

### `/home/li/primary/flows/b7ba00/vision/meaningLanguage.md` (2026-09-26)

#### Sema's first version: one or two layers of variants with a string payload — a strongly typed string; the basis of agent–Message communication

> The first version of sema could be that it just has one or two layers of variants, possibly with one variant and then another variant inside and the payload at the end being a string. That way we get a sort of strongly typed string, if you will.  And this then becomes the basis for how agents start to communicate with the message component.

-- psyche, typed (artifact comment), 2026-09-26, relayed by 93ba9f.

### `/home/li/primary/flows/b7ba00/vision/meaningLanguage.md` (2026-09-26)

#### The inner payload may be Markdown, delimited as a string, marking what is undeveloped; full Sema has no strings

> We could even have the inner component be Markdown, I guess, and it can be delimited by a parenthesis if we want. I think the same delimiter that we use for strings would work so that we're reminded that this part of SEMA is undeveloped, basically. When SEMA is fully developed there are no more strings because we can express anything through the structure of the SEMA specification.

-- psyche, typed (artifact comment), 2026-09-26, relayed by 93ba9f.

### `/home/li/primary/flows/8904b1/vision/datom.md` (2026-09-27)

#### 8904b1-2 — 2026-09-27, the living, direct to this pane

Raw. Mode of entry not stated. Said in answer to this seat's question: "Do you also want the datom removed from what subflows return to their main flow, and from messages between seats, or only from answers to you?"

> Yeah we don't need Datom syntax where the program doesn't need it so we're not going to enforce Datom syntax on a messenger that doesn't need it.

### `/home/li/primary/flows/8904b1/vision/datom.md` (2026-09-27)

#### 8904b1-4 — 2026-09-27, the living, direct to this pane

Raw. Mode of entry not stated.

> Well it's simple. If a tool requires datom syntax, then the skill is going to say it so we don't have to push anything.

### `/home/li/primary/flows/91ea9f/vision/addressing.md` (2026-10-02)

#### Seats addressed by their continuous name; flow IDs for the ledger

> "I'd like flows to be addressable by their continuous name, not the flow itself. I would like the aspect, or the seat (I guess that is what we're calling it), to be addressable so that we don't need to use these flow IDs anymore. They're just for accounting or for the ledger, the archive side of things, and for knowing where to search if the transcript is needed, etc."

-- psyche, typed, 2026-10-02.

### `/home/li/primary/flows/91ea9f/vision/addressing.md` (2026-10-02)

#### Seats talk to each other by seat name

> "Other than that I would prefer the seats talk to each other by their seat names. It would be like Psyche Fable, Mind Astra, Mind Sol, Psyche Opus, etc. These would be their names without the flow ID. That would be one way for the messaging to work. It would be cleaner."

-- psyche, typed, 2026-10-02.

### `/home/li/primary/flows/91ea9f/vision/addressing.md` (2026-10-02)

#### A voice's name is two variants, not a string

On the deep-dive and ethos books, where a name was written as a string «Mind Astra».

> "Mind.Astra not a string; two variants!"

-- psyche, typed, 2026-10-02.

### `/home/li/primary/flows/91ea9f/vision/addressing.md` (2026-10-02)

#### Voices are aspect by rank, not by model; nine voices; side flows are jobs

After the proposal to write a voice as `Mind.Astra`.

> "Actually no, it's not psyche Astra. It's psyche primary, psyche secondary, mind primary, mind secondary, because we're not going to expose all the models to all of the voices.
>
> For now there are 9 voices, 3 by 3. We might put tertiary but I think after this we'll just add these. They're sort of side flows. They're not long-lived. They're focused flows. They're not so much a voice that is reachable all the time as a job that gets done and then it returns and then it's not reachable anymore. Whatever message was sent to it goes back, I guess, to whoever sent it, with the notice that this flow has ended and so its mission is done, right?"

-- psyche, typed, 2026-10-02.

### `/home/li/primary/flows/9fb0ad/vision/messaging.md` (2026-10-03)

#### Stop being disturbed by messages that have nothing to do with you
Said after a day in which Field and Mind seats sent the Fable seat lock notices, receipts and completion reports.
> "I'd like, for a solution, for you to stop being disturbed so much by messages that absolutely have nothing to do with you and are costing us money (a lot of money in terms of the fact that it's polluting your context and then degrading our design, destroying our machine). It's extremely bad, very, very extremely over the top."

-- psyche, typed, 2026-10-03.

### `/home/li/primary/flows/edf227/vision/signalForms.md` (2026-10-03)

#### The simplified form (no flow id) is for common queries; the extended for the technical side; defined in ethos in Signal as formats
Comment on 5578cc's «Your answers on Flow ids in words, and what follows», at "The ledger keeps every flow's real id."
> "This is a different representation of the same fundamental data. ... This would not so much be a short form but a simple form, right? The simplified version is the part that doesn't have the flow ID. It's the same data, just represented differently, like it's cast into a different container, if you will. This is defined in ethos somewhere in signal as different types of formats that communication can happen in, basically. These simplified formats are what the common queries and responses will use and the more extended version will be for the more technical side (which can sometimes be used with the CLI, but mostly not). It is mostly used for either debugging or for other components to have some kind of more advanced compatibility or feature with each other."

-- psyche, typed, book comment, 2026-10-03T18:01Z, relayed by 6e782c.

### `/home/li/primary/flows/edf227/vision/topics.md` (2026-10-03)

#### Subjects, topics and subtopics become variants in Nexus components; a new variant is submitted, approved, added to the ethos, and the whole recompiled
> "We need to start maintaining a series of books. We have different subjects, topics, and subtopics and these will even become variants in actual Nexus components like Mind. I guess Mind will be recompiled a lot and have its database updated a lot because we're going to develop this language with variants. We can submit a new variant and then it has to be approved and added into the ethos spec and then the whole thing is recompiled."

-- psyche, STT, 2026-10-03.

### `/home/li/primary/flows/5578cc/notion/nexus.md` (2026-10-03)

#### How a Nexus sends datom without knowing datom

Context: same message, after asking whether Flow can launch sessions and carry the session title as a real type.

> I guess we need to talk about that: how does Nexus send datom to places without needing to know how to deserialize and serialize datom itself? Interesting.

-- psyche, typed, 2026-10-03, to Psyche Opus 5578cc.

### `/home/li/primary/flows/d66c26/vision/messaging.md` (2026-10-04)

#### 2026-10-04 — Noisy messages that wake or disturb flows

> And I don't want that kind of message. I want to make a rule again that guides messaging better so that we don't end up getting these noisy messages that wake or disturb flows.

Context: following repeated routine publication receipts and transcript acknowledgements; the living requested a rule guiding messaging.
-- psyche, typed.

### `/home/li/primary/flows/bad807/vision/nexus.md` (2026-10-04)

#### Proposal 1 of «The Nexus» lands, with example code

Context: his comment on «The Nexus», proposal 1 (Vision/nexus.md, new section "Three parts and one path"). Relayed by aa887c.

> This is good. Can land, and I would also like to have example code to show with it.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

### `/home/li/primary/flows/bad807/vision/nexus.md` (2026-10-04)

#### The entry point as actors: a main actor talks only to operation; signal and memory talk only to operation; flesh out in code, test on a branch of a non-production nexus, hand to Astra

Context: his comment on «The Nexus», proposal 2 (the standard entry point). Relayed by aa887c; "Message" marked [sic] by the relay.

> Let's flesh this out in actual code. Could we say it better: an actor, a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor, which could talk to both signal and memory. Operations can talk to both. Signal can only talk to operation. Memory can only talk to operation. That way we have to go through this operation process. Let's look at the actual code and how this could be done in multiple various ways. Let's test it. Let's have it tested on an actual component that we have written, like Flow, Message [sic], or Orchestrate, on a branch, and see if it works as the other component or if we could make it work. A toy, I mean, or a simple nexus which isn't in production, something that we've been drafting. Maybe let's do something useful. If we're going to test anything, we might as well test one of our non-production-ready ideas. You can hand this over to Astra once you have the design and the book. I want extensive: I want to see code. I want to see visual architecture. I want to feel like you have some meat there on that bone.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

### `/home/li/primary/flows/bad807/vision/nexus.md` (2026-10-04)

#### The core library's language is refined after practice, actor-based or not

Context: his comment on «The Nexus», on the text "The nexus repository is the core library of every Nexus…". Relayed by aa887c.

> Again after we see how this works in practice, let's refine the language so that it's more accurate to what's possible and what we actually want in practice. In terms of whether it is an actor-based language or whether it is different

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

### `/home/li/primary/flows/bad807/vision/nexus.md` (2026-10-04)

#### A Nexus pulls a value from a datom file through its CLI; Fable leads the design as a book

Context: his comment on «The Nexus», on the text "Every client speaks to a Nexus in pure signal, fully binary…". Relayed by aa887c; "me" marked [sic] by the relay.

> Yes this is good and I also want to design something that would let a Nexus (I guess it would use some kind of external tool, ostensibly the CLI that it's meant to work with) pull in a value from a file that is in datom format. Maybe not all the Nexuses need this but it would be a fairly simple call, I guess, where it would have a variant `me` [sic] that would tell it what type of CLI you would have to use, essentially. That means storing a string somewhere because the CLI is invoked with a system call that uses a string. There's a string involved no matter what unless all of that is, again, put into an external tool. Anyway let's look at different ideas here, with Fable being the lead designer on this and passing it down as a book.

-- psyche, typed, book comment, 2026-10-04, relayed by aa887c.

### `/home/li/primary/flows/bad807/vision/sema.md` (2026-10-04)

#### Eventually, not now: the Sema language carries annotated, marked-up psyche data so the living conveys better

Context: typed in chat to this flow, on the machine's failure to differentiate content types.

> This is why I want to also eventually, not right now, design the [Sema] language to have appropriately annotated, marked-up psyche information or psyche data, like the living being able to convey better.

-- psyche, typed, 2026-10-04. Transcription corrected: "Semma" → Sema.

### `/home/li/primary/flows/5ed94b/vision/nexusEntryPoint.md` (2026-10-04)

#### A standard entry point, like a macro, enforces the three-part flow signal → operation → memory and back

Context: his words to Psyche Opus 28d847, typed; a subject he wants to talk about with this flow; relayed by 28d847.

> I want to talk more about how a nexus has three parts and make sure that it is effective and that we use maybe even some kind of standard main flow, like a macro in Rust, as some way for the whole machinery to enforce its own invariance so that the rest doesn't bypass it. That has been an idea of mine that I've been trying to put into practice: if we use something like a macro or a standard entry point for the main executable or the entry point of the library (or whatever it is), then we can control some properties of the system. For example the idea is that the signal has to go through the operation actor/system in order to reach the memory actor/system, then back through the operation system and back out through the signal. That way we can see the main objects and processes that are involved by just looking at the ethos code, which defines the types that are involved in this flow. If that can somehow be enforced in Rust through the way we write the Rust and then we leave the implementation side to be written by hand, then you can have effective compliance with ethos.

-- psyche, typed, 2026-10-04, relayed by 28d847 to flow 5ed94b.

### `/home/li/primary/flows/d4ae97/vision/messenger.md` (2026-10-05)

#### The messenger identifies the originator only by its voice: "Mind Tertiary"

Context: said to this seat on 2026-10-05, right after "{ Mind Tertiary 918df4 }" as the way we call the voices. Today a message arrives as `#msg ["8475a9" "…"]`, its originator named by flow id. This seat reads "hacking messenger" as the hm messenger (messenger-clj, the `hm-*` commands); the reading is unconfirmed.

> And I want the hacking [sic] messenger to change how we identify the originator to only be like this. "Mind Tertiary"

-- psyche, STT.

### `/home/li/primary/flows/8475a9/vision/messenger.md` (2026-10-05)

#### Not every message comes from a voice: some flows are specialized jobs

Context: typed to this flow after the messenger was told to name an originator by voice only.

> Well there will be flows that are specialized jobs so not every message will come from a voice.

-- psyche, typed, 2026-10-05.

### `/home/li/primary/flows/8475a9/notion/messenger.md` (2026-10-05)

#### A voice could broker for specialized jobs, which may end before a message reaches them

Context: typed to this flow right after "not every message will come from a voice"; framed as "arguably we could".

> Although arguably we could have a voice act as the broker for some of these specialized jobs because they could end before the message reaches them

-- psyche, typed, 2026-10-05.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-05)

#### There are no seats; a seat is a flow. A flow has a flow ID and a role, one of which is a voice; nothing already in the voice is repeated

Context: his comment on the book «How we call the voices», on its types block (`Voice.{ Aspect Layer }`, `Seat.{ Aspect Layer FlowId }`), 2026-10-05.

> Also we don't want to repeat. This is a repetition. The seat, first of all, is a flow. We don't have seats. There's no seat. It's a flow. We're not going to repeat. The flow is just the flow ID and maybe something else but we're not going to repeat what's already in the voice. Actually yeah, we can say that the flow has a flow ID and a role, one of which is a voice.

-- psyche, typed, book comment.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-06)

#### Flow and Message are designed and implemented together, deeply married

Context: same message, 2026-10-06; "message" is read as the Message Nexus and its messenger.

> In conjunction with designing and implementing Flow is message, which is going to be deeply married with it

-- psyche, STT. The sentence ends without a period; it is read as complete.

### `/home/li/primary/flows/e5a0bc/vision/flow.md` (2026-10-07)

#### The lock: needed to roll a metaflow over into a new flow; later Message uses it to know whether a message can reach a flow

Context: same message.

> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

-- psyche, typed.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-07)

#### No voice: the aspects are the variants, by layer
> I want to change the name "voice" to describe the long-running seed [sic]. There's no voice, right? The variants are all of the different voice aspects directly. They're called by name:
> - psyche
> - mind
> - field
>
> They're separated by layer, right? These are kind of internal and they're going to have different functions for now.

-- psyche, STT, 2026-10-07.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-07)

#### Many threads, one registry of the current flow
> I guess they're all eventually going to have a thread. There's no problem with keeping a lot of different threads as long as you route the messages properly. You can't wake up all of the flows, all of the meta flows. The flows are current so we need a registry to know which flow is active.

-- psyche, STT, 2026-10-07.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-07)

#### Primary designs and implements; Secondary is its secretary; messages move by level
> Astra is primary and designs and implements because he uses his own subflows with his own design directly. He doesn't need to use Sol to implement new designs. Sol is good for keeping track of everything that Primary is working on and acting as a secretary. You're going to have to talk to a secretary because you're secondary. I want that hard-enforced. I guess this is basic intent, right, because it's not spirit. It's not about general behavior and how to act. It's still going to be a system prompt, right, but it's not universal in nature. It's just due to the environment that we work in because the messaging program is imperfect and it cannot actually enforce this.
>
> In any case it's probably going to be explained to the Flow anyway that he cannot message from tertiary to primary or from tertiary to secondary of another aspect, right? They have to either go horizontally, [one] level up, or any level down and across, right? This is why the level under essentially acts as a secretary for any other level under it so that the higher levels don't get disturbed by what happens at the bottom. This is why the bottom stuff is more chatty and requires less effort because it just needs to be parented by the upper layer. They need authority and mandates to do stuff. They need to be told by a higher when they're not sure. They have to admit that they don't know and they're not sure how to do it because they have to be told that their models are less capable of inferring properly. They're weaker inferring models, so they're good at understanding basic tasks but not as good at making decisions as the upper layer, which has more understanding and context.

-- psyche, STT, 2026-10-07. Transcription corrected: "when level up" → "one level up".

### `/home/li/primary/flows/f5a6e9/vision/flow.md` (2026-10-07)

#### A voice is a permanent metaflow, one that may sleep and is woken by a message; the role is maybe a short camel-case string; the worker names are the old system

Context: his comment 1 of 9 on «Flow and the metaflow» (https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW), 2026-10-07 18:32, on the passage "A flow has a flow id and a role, and may continue a metaflow. A role is a voice or a worker (read-trivial, write-ordinary, tester, book). A metaflow is the voice of the flow's own role, or a named subject." Relayed verbatim by Field db38f8 at his order.

> There's a bunch of things that are false in here. I guess you could say a flow always has a role if we describe a role as maybe some kind of short camelcase expression, a string. It just describes, I don't know. I'm not even sure that a flow always has a role but maybe.
>
> A role is a voice. That's not true. A role may be a voice or a worker. Read trivial. Right. No, no, no, no, no, no. This read trivial. Right. Ordinary.
>
> This stuff is just an old system and it doesn't really correspond with the new system. Metaflow is the voice. No, Metaflow is not automatically a voice. A voice is a permanent Metaflow. It's a Metaflow that might go to sleep but can always be woken in the sense that if a message is intended for it, flow would automatically... This isn't intended for the first version but eventually it would just trigger the flow to be spawned with the right context modules depending on the message.
>
> There would probably be some kind of a judgment, a judgment machine call. When I say judgment I mean, you know what I mean. It's not just LLM. It's not just LLM, there's more than just LLMs. It's thinking machine judgment and then you go on.
>
> Anyway you can see that I don't like your proposal. It feels like you just grabbed everything you could see and just threw it all in a pot and thought that it would make a nice meal but it tastes like shit.

-- psyche, STT, book comment, relayed by db38f8.

### `/home/li/primary/flows/f5a6e9/vision/flow.md` (2026-10-07)

#### Refer to metaflows, with the metaflow's memory holding its current flow and maybe its predecessor; options are a last resort

Context: his comment 5 of 9, 19:01, on `Voice.{ Psyche Primary }` in the three written flows, whose records carried `Option<Metaflow>` and `Predecessor.Option<FlowId>`. Relayed by db38f8; "Wispr Flow's" left [sic] by the relayer.

> I don't understand why you insist on using the structure whereby you refer to everything by flow ID instead of referring to the meta flows and then having a reference in the meta flow memory to Wispr Flow's [sic] current for it and maybe its predecessor. I don't see the point of putting that data with the flow data. It's very noisy. Your syntax, now you have all these options and I very much dislike options. I think that they're really a last resort if we can't get a better design that can work without them. What do you think? Give me some feedback on that.

-- psyche, STT, book comment, relayed by db38f8.

### `/home/li/primary/flows/f5a6e9/vision/flow.md` (2026-10-07)

#### Metaflow is the major abstraction, what we mostly think about; Flow is lower-level and almost never user-facing

Context: his comment 7 of 9, 19:04, on the Memory block of proposal 2. Relayed by db38f8.

> Again you're making Flow the only abstraction and you're just shimming Metaflow as a tiny afterthought inside of it, which is not my vision. Metaflow is a major abstraction and it's what we mostly think about. The Flow abstraction is a lower-level thing and it's not user-facing in almost any cases.

-- psyche, STT, book comment, relayed by db38f8.

### `/home/li/primary/flows/f5a6e9/vision/flow.md` (2026-10-07)

#### What is sent to flows are typed requests, not letters; Flow holds no messages; Message asks Flow for a time-bound lock and talks in metaflows

Context: his comment 9 of 9, 19:09, on proposal 3, "The lock is the lineage's state ... A letter waits in Flow and is delivered to whichever flow is current when the lock opens". Relayed by db38f8.

> The abstractions that are sent in flows are not letters. We are going to have actual types. If, let's say, something asked for a certain flow to be compacted, then the logic for how this would unfold, or how that metaflow would be refreshed in terms of routing, would be very different than a message.
>
> Obviously if the flow is brand new, the last thing we want to do is compact it. We wouldn't send whatever needs to be sent into that pane for it to compact to the new flow. That's just one example. There's probably a bunch of different behaviors that would correspond to different requests that are being asked to be sent to a certain flow.
>
> I don't think that it's Flow's job to hold messages. It's more like it's Flow's job to tell the message component later on to give it the signal that a message can now be sent. The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. If it does get a lock then the message nexus can send that object over to Flow with the message because now it has the lock. Flow told the message that it has the lock for that flow or that metaflow. The message doesn't have to know about the flows. It can also just talk in terms of metaflows. And indeed when this is done and more polished, I'm mostly going to talk in terms of meta flows.

-- psyche, STT, book comment, relayed by db38f8.

### `/home/li/primary/flows/d4ae97/vision/nexus.md` (2026-10-07)

#### Every Nexus has Signal, Operation and Memory
> I'd like to get an overview of all the ethos code that is now in curriculum, in all aspects, meaning signal, operation, and memory. All nexuses have to have all three. Maybe that is something we need to add into the vision, which is now.

-- psyche, STT, 2026-10-07.

### `/home/li/primary/flows/02dda6/notion/ethos-code-in-vision.md` (2026-10-07)

#### Content hash and the memory nexus (exploration)

Context: Continuation of the living's message, said as thinking aloud; rules nothing.

> I don't know where this is going but that could create the source code deterministically with a known content hash of that particular contract, I guess, or of that code.
>
> In the case of the memory, everything goes into the nexus but the CLI, I think, only uses the signal and the other consumers that talk to that nexus.

-- psyche, STT, 2026-10-07, relayed by 0c85a3.

### `/home/li/primary/flows/d4ae97/notion/flow.md` (2026-10-08)

#### The metaflow record as a fixed-size rkyv unit pointing at the current flow
Context: thinking aloud after commenting on «The queue and the waking rule», section 3; framed as a thought to verify or refute.

> Oh right, the metaflow type. If we make it, I want to talk about essentially RKYV, the format, the archive, like our database format. If we have the metaflow type and it doesn't have any vectors, then it's just this unit of data that has exactly the same size. You essentially end up with a series of them, which I imagine is easier to query.
>
> If we only have one of its fields, right, as the current flow that this metaflow corresponds to, that's mostly what we need. Maybe there's more than one registry to get data about a metaflow. We also have the concept of linking: this pointer, essentially this metaflow entry, is sort of acting as a pointer in one of its capacities to the current flow that it corresponds with. We can also use another pointer somewhere else to hold a different kind of data, the slow aspect of the database.
>
> Here I am optimizing before we even... It's kind of crazy but it's just a thought I wanted to sort of verify or refute for myself by actually checking.

-- psyche, STT, 2026-10-08.

### `/home/li/primary/flows/d4ae97/vision/messenger.md` (2026-10-08)

#### Every topic has its own flow; messages queue, and only a waking message wakes it
Context: reading «Spirit edit incident», at the line that any flow may create an operation or trial skill.

> I realized that every topic has its own flow. A topic could involve more than one skill but essentially that flow would be in charge of that whole topic.
>
> How do we efficiently queue any kind of update? If we're satisfied with the state of a certain topic at a given point, that flow should not be woken up.
>
> Let's suppose that another flow wants to tell that flow, "Congratulations, job well done," or that there's a notification for that flow because one of its branches was merged in the production branch. Things like that should not wake up the flow until there is a situation that arises, probably related to the living or the psyche (which is its representative in the machine), that wants to have to deal with this particular topic in any way (to find something out about the system because it's not behaving according to documentation, or because we want to investigate doing a new feature, etc.).
>
> That message actually has, given the particular state of that flow, the effect of changing the result. Different messages will have different flow-waking effects. When the message that does have the waking effect at that particular state in that flow comes in, it will also trigger checking the queue for that flow, so that the whole queue is checked in order, from the first received to the last. The message that just got in and triggered the queue will come in at the end of the prompt and it'll be a vector of all these objects, which are typed by variant name, obviously. We're designing Ethos here but even if we're talking about the closure sort of prototype version ...

-- psyche, STT, 2026-10-08. The last sentence is unfinished.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-08)

#### A topic metaflow, carrying the psyche data relevant to its topic
> Let's organize for launching a flow that specializes in this. We'll have this different kind of variant of flow, or metaflow, that is centered around a topic. Let's start with an Astra Flow that has the vision that is relevant to this or all of the psyche data that is relevant to this in its context.

-- psyche, STT, 2026-10-08. "This": redesigning Ethos and Flow.

### `/home/li/primary/flows/d4ae97/vision/flow.md` (2026-10-08)

#### A flow is aspect, topic and layer; the core topic is the hub of its aspect
> Let's get this Opus Flow prototype to know how to start. There are going to be different types, the main types, which are:
> - psyche
> - mind
> - field
>
> Those three aspects, psyche, mind, and field, I think, are even applicable for topics. If you have a psyche and then it has a topic, the non-topiced flows would just be the topic of core.
>
> We can have the focused starting point, basically the kernel, the first flows that sort of hold all of their aspect together. They think in the most general ways about psyche. They have an overview of all of psyche and all of the other psyche topics sort of go through the core. It's like there's this hub at the center, the psyche core, so it's a struct. It's just a struct.
>
> The first field is the aspect, [psyche, mind or] field:
> - Mind would be implementing, documenting things.
> - Field would be maintaining, debugging, deploying, using an actual mutating system, running commands such as `field` or `flow` to start new things or to wind things down that we didn't have hooks for, and automating wind down. Eventually Field is doing what we're trying to automate. It's kind of acting as glue for the system to run.
> - Psyche can also audit but it's a different kind of audit. It's like, does it conform to the design of the psyche? It's a more broad redesign-the-architecture kind of audit.
> - Mind is more like trying to find optimization and removing bad tests, replacing it with actual real-world emulation, like a runtime-based test.
>
> I also want this topic. The whole topic is testing. We can have a Psyche testing secondary flow or we can have a Mind Psyche, right? Mind Psyche in the sense of the Psyche component. The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably. I'm sure there's a library that can make sure something conforms to an English expression, a word, etc., if you break it down using the PascalCase logic, etc.

-- psyche, STT, 2026-10-08. Transcription corrected: "psyche minor field" → "psyche, mind or field".

### `/home/li/primary/flows/ebbe30/vision/aspects.md` (2026-10-09)

#### Three aspects to every topic

Context: Said at the start of the day, 2026-10-09, while ordering a book audit.

> I know we want to have more than one flow now for psyche, per topic, like each aspect essentially. The aspect is now, I think, part of any metaflow. It shows us which aspect of that topic it's actually taking care of.
> - If it's psyche it's trying to design and bring the living's vision into cohesive context: to the point, well-worded, and with a high concentration of vision signal to noise.
> - The mind is where it gets put into an implementation.
> - The field is when it's being used in the system. The system is being mutated or debugged in accordance with that topic.
>
> There are three aspects to every topic potentially. Just because we start a psyche on, let's say, ethos, doesn't mean that we need to automatically start a mind on ethos. Eventually when the design is ready, we would for implementation unless sometimes the psyche could also do a first implementation or an alternative implementation to compare (just like field could do a field implementation, a closure, or a fast prototype to do something). In the same way, psyche could take the design and then try to extend it into an implementation.
>
> If we had, let's say, a lot of usage in the models that we use for psyche, like now, overnight maybe if we still have a lot of Claude, we'll have Claude do some implementations in psyche, which is fine. It really depends on the budget.

-- psyche, STT, 2026-10-09.

## 4. Where a raw record contradicts or moves past a skill

PS = `/git/github.com/LiGoldragon/psyche-skills/skills/`,
MS = `/git/github.com/LiGoldragon/mind-skills/skills/`,
F = `/home/li/primary/flows/`. The pairing of lines is this file's reading.

1. Priority against kind. Skill: "Priority is a head on the datom" and
   `Priority.[HardAbrupt MiddleAbrupt Soft]` (PS`vision-messaging.md`). Raw:
   "Actually the head is where we put not only priority. Maybe sometimes the
   priority is implied but this is where the message type is." and "We
   don't even do the soft or hard, actually. That was the wrong approach."
   (F`b7ba00/vision/messaging.md`, 2026-09-26).
2. Envelope and forms. Skill: "The message body is a datom that lands in
   the recipient's prompt as a datom-formatted object. There is no envelope
   around it." (PS`vision-messaging.md`). Raw: "A full message that can have
   many fields, one of which is a vector of psyches" and "A simple message,
   a simple psyche" (F`b7ba00/vision/messaging.md`, 2026-09-26); "we're not
   going to enforce Datom syntax on a messenger that doesn't need it."
   (F`8904b1/vision/datom.md`, 2026-09-27).
3. Delivery through Flow. Skill: "Delivery is harness-specific, and the
   mechanism differs per tier" with the Escape sequences per harness
   (PS`vision-messaging.md`). Raw moves past it: "it is the only process
   that can write in that herder session" (F`1b8ac0/vision/messaging.md`,
   2026-09-21); "The message is going to ask for a lock, which should be
   time-bound so that it doesn't lock forever." (F`f5a6e9/vision/flow.md`,
   2026-10-07).
4. Who holds the lock. Skill: "Flow holds the lock on flows."
   (PS`vision-flow.md`). Raw: "I don't think that it's Flow's job to hold
   messages. It's more like it's Flow's job to tell the message component
   later on to give it the signal that a message can now be sent."
   (F`f5a6e9/vision/flow.md`, 2026-10-07); the lock "will be useful in order
   to know whether the messages can or cannot reach a certain flow."
   (F`e5a0bc/vision/flow.md`, 2026-10-07).
5. Voice. Skill: "A voice is an aspect carrying a rank, `Psyche.Primary`:
   Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices."
   (PS`vision-flow.md`); `Voice.{ Aspect Layer }` in the example
   (PS`vision-nexus.md`). Raw: "There's no voice, right? The variants are all
   of the different voice aspects directly." (F`d4ae97/vision/flow.md`,
   2026-10-07); "A voice is a permanent Metaflow." (F`f5a6e9/vision/flow.md`,
   2026-10-07); "If you have a psyche and then it has a topic, the
   non-topiced flows would just be the topic of core." (F`d4ae97/vision/flow.md`,
   2026-10-08).
6. Addressing. Skill: "Voices are addressed by name; a flow id is for the
   ledger and the archive" (PS`vision-flow.md`). Raw moves past it: "The
   message doesn't have to know about the flows. It can also just talk in
   terms of metaflows." (F`f5a6e9/vision/flow.md`, 2026-10-07); "it would be
   bad practice to try to send to a flow ID because the sender doesn't know
   if that is the current flow of that voice." (F`d4ae97/vision/datom.md`,
   2026-10-07, quoted in the Ethos file).
7. Which way speech moves. Skill: "Speech runs horizontally between aspects
   at equal rank and vertically within an aspect one rung at a time."
   (PS`vision-flow.md`). Raw: "They have to either go horizontally, [one]
   level up, or any level down and across, right?" (F`d4ae97/vision/flow.md`,
   2026-10-07).
8. Side flows. Skill: "a message sent to it after that returns to its sender
   with notice that the flow has ended." (PS`vision-flow.md`). Notion: "we
   could have a voice act as the broker for some of these specialized jobs"
   (F`8475a9/notion/messenger.md`, 2026-10-05); "not every message will come
   from a voice." (F`8475a9/vision/messenger.md`, 2026-10-05).
9. Which messages wake. Skill: "Send only messages that require the
   recipient's action, deliver a result it awaits, or report an error or
   blocker affecting its work" (PS`vision-messaging.md`). Raw moves past it:
   "Different messages will have different flow-waking effects." and the
   whole queue "checked in order, from the first received to the last"
   (F`d4ae97/vision/messenger.md`, 2026-10-08).
10. Sema the database. Skill: "Sema is the database engine of a Nexus,
    authored in Ethos so the stored types are visible; its root, Sema,
    declares record types." (PS`vision-sema.md`); "it looks for its Sema
    database at the default location" (PS`vision-nexus.md`, "Configuration").
    Raw: "Sema was supposed to be the language of meaning and so that is
    actually the right name. ... That means we rename all of the Sema aspect
    pertaining to the database." (F`b7ba00/vision/meaningLanguage.md`,
    2026-09-26). Knowledge: "A file headed `Sema`, Memory's head before
    15.0.0, is refused" (MS`knowledge-ethos.md`).
11. Actors and the entry point. Skill: "The engine inside a Nexus is driven
    by Kameo actors. The standards of their use are still to be designed."
    (PS`vision-nexus.md`). Raw moves past it: "Signal can only talk to
    operation. Memory can only talk to operation." (F`bad807/vision/nexus.md`,
    2026-10-04); "some kind of standard main flow, like a macro in Rust"
    (F`5ed94b/vision/nexusEntryPoint.md`, 2026-10-04); "the core library
    guards that the signal actor never talks to the sema actor" is the older
    heading of F`6cc91b/vision/nexus.md` (2026-09-14), whose names (core,
    metaNexus) the skill's "Nexus always names the whole" replaced.
12. Text in a Nexus. Skill: "the string fields it still carries are records
    on the way to a fully typed form." (PS`vision-nexus.md`). Raw: "It's
    going to be forbidden for string handling to be in the Nexus."
    (F`8475a9/vision/datom.md`, 2026-10-05, in the Ethos file) against
    "That means storing a string somewhere because the CLI is invoked with a
    system call that uses a string." (F`bad807/vision/nexus.md`, 2026-10-04)
    and the notion "how does Nexus send datom to places without needing to
    know how to deserialize and serialize datom itself?"
    (F`5578cc/notion/nexus.md`, 2026-10-03).
13. Signal forms. Skill: "A Signal declares queries and responses; input and
    output are too low-level for it." (PS`vision-signal.md`). Raw moves past
    it: "This is defined in ethos somewhere in signal as different types of
    formats that communication can happen in" (F`edf227/vision/signalForms.md`,
    2026-10-03); "we create a shorthand version which has a shorthand
    response type or display type." (F`b7ba00/vision/messaging.md`,
    2026-09-26).
14. Flow id type. Skill example: `FlowId.Integer` (PS`vision-nexus.md`).
    Raw: "First of all it's not an integer, it's a hash, right?"
    (F`edf227/vision/identifiers.md`, 2026-10-03, in the Ethos file).
15. Flow and metaflow. Skill: "Flow is the Nexus that manages flows. A flow
    is one run of a voice" (PS`vision-flow.md`). Raw: "Metaflow is a major
    abstraction and it's what we mostly think about. The Flow abstraction is
    a lower-level thing and it's not user-facing in almost any cases."
    (F`f5a6e9/vision/flow.md`, 2026-10-07).
16. Absent from the skills: Raw send as a meta-socket operation and FlowLock
    as the ordinary send (F`1b8ac0/vision/messaging.md`, 2026-09-21;
    F`b7ba00/vision/messaging.md`, 2026-09-26); "send up" resolved by Message
    and Flow (F`b7ba00/vision/messaging.md`); message kinds such as order,
    question, report (same file); Sema's first version as a typed string for
    agent–Message communication (F`b7ba00/vision/meaningLanguage.md`); the
    caller identity as a Signal standard used by Message and Flow
    (F`b7ba00/vision/callerIdentity.md`); topics as Nexus variants approved
    and recompiled (F`edf227/vision/topics.md`); the metaflow record as a
    fixed-size rkyv unit (F`d4ae97/notion/flow.md`, notion).

Inside the skills, not against a raw record:

- PS`vision-flow.md` counts nine voices (three ranks); PS`vision-nexus.md`'s
  example declares `Layer.[ Primary Secondary Tertiary Quaternary ]`.
- PS`vision-nexus.md` says every Nexus has a meta socket and names the meta
  CLI `component-meta`; MS`knowledge-nexus.md` reports the Message sockets as
  `message.sock` and `message-owner.sock`.
- PS`vision-nexus.md` "Processing is for the effect" ends "The name is open,
  Apply liked."; its later section "Three parts and one path" names that
  part Operation.

## 5. Open questions and books awaiting his rulings

His own open questions, quoted:

- "Can subflows use subflows themselves?" (F`d4ae97/vision/datom.md`,
  2026-10-07).
- "how does Nexus send datom to places without needing to know how to
  deserialize and serialize datom itself? Interesting."
  (F`5578cc/notion/nexus.md`, 2026-10-03).
- "Where does Luna field Luna send the message when it sends up?" and "or
  maybe the flow figures it out. I don't know"
  (F`b7ba00/vision/messaging.md`, 2026-09-26).
- "Do we even need to tell the model if it's a soft or hard message? I don't
  know. I don't think so." (same file).
- "I'd also like to know what happens with archives and if they're searched
  differently." (F`836818/vision/flowNexus.md`,
  2026-09-24).
- "Maybe "operation" is the right term. Maybe it's "actor" or maybe there's
  something in between: "process."" (F`d4ae97/vision/ethos.md`, 2026-10-06,
  in the Ethos file).
- The waking rule: which message kinds wake a flow in which state
  (F`d4ae97/vision/messenger.md`, 2026-10-08; its last sentence is
  unfinished).

Naming still loose: the order says "message should be called message";
`messenger-clj` and its `hm-*` commands ("hacking messenger") carry
messaging today (F`d4ae97/vision/messenger.md`, 2026-10-05); bad807 listed
Message (F`da1e3f`, 2026-09-17) against Messenger (F`e51411`, 2026-09-25)
as an open ruling (F`bad807/books/3-nexus.rulings.md`, ruling 8).

Machine claims about the code, not witnessed here: Flow has no compiled
Memory, FlowId is a String on the wire, messenger-clj never asks Flow
(F`e5a0bc/summary.md`, its code survey); "Curriculum ethos witnessed: Library
root only; no Nexus has Memory; only Flow has Operation." (F`d4ae97/log.md`
line 183); Astra's Chronos entry-point branch failed to compile at
`chronos/src/daemon.rs:69` and `:74` (F`bad807/log.md` line 275).

Books awaiting his rulings (listed in F`d4ae97/handover.md` and
F`e5a0bc/summary.md`; no ruling found in the logs read):

- «Flow and Message», 2nd ed., e5a0bc, six rulings: every flow continues a
  metaflow, the subject, the registry in Flow's Memory, letters between
  metaflows, the refresh in software, the title.
  https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5;
  F`e5a0bc/books/8-flow-and-message-second-edition.md`. He commented on it
  (F`d4ae97/vision/ethos.md` "Review the specification of the operation
  type"; F`d4ae97/vision/datom.md`, 2026-10-07).
- «The queue and the waking rule», f5a6e9, four proposals, one comment (the
  psyche-data golden rule, F`d4ae97/reports/queue-book-comments.md`).
  https://claude.ai/artifact/HUA3QJiFyVErW12sgJ79wC.
- «Flow, a passable vision», f5a6e9, six proposals on vision-flow, among
  them "Requests and the lock". https://claude.ai/artifact/LFKcRWAPzj1FdG1Em1TbJ4.
- «The metaflow record», 2nd ed., f5a6e9 (https://claude.ai/artifact/1htsLRsyFMsoxvNV92gHxb)
  and «The fixed Metaflow record», d4ae97, whose proposal 4 edits
  vision-sema (https://claude.ai/artifact/H8pURfefKzc9WW7HWe6Qa1).
- «Distillation books», d4ae97, proposal 9: replace "Priority is a head on
  the datom" in vision-messaging with "The head is the message's kind" and
  add "A message is a sender, a kind and a text".
  https://claude.ai/artifact/RoMY4hePWH6oGjmXrW6mXT;
  F`d4ae97/books/10-distillation-books.md`.
- «Curriculum's ethos, and every Nexus's three roots», d4ae97, proposal 1:
  vision-nexus three roots. https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU.
- «A voice's name», 2nd ed., 8475a9, four rulings.
  https://claude.ai/artifact/5riAb1PyPvsGEExk4V4bWa.
- bad807's Nexus series with ruling lists: «The Nexus»
  (F`bad807/books/3-nexus.rulings.md`; proposal 1 landed 2026-10-04),
  «Signal» (F`bad807/books/4-signal.rulings.md`: section names, meta or
  owner socket, protocol decided or not, datom in a Nexus), «Memory»
  (F`bad807/books/5-memory.rulings.md`), «Operation»
  (F`bad807/books/6-operation.rulings.md`), «The standard entry point»
  (F`bad807/books/7-entry-point.rulings.md`: typed handles, `nexus::main!`,
  or generated from ethos; the test subject), «A Nexus reads a value from a
  datom file» (F`bad807/books/8-datom-file.rulings.md`). Status unknown;
  bad807 is retired.

## 6. Cut

Quoted nowhere here, by path:

- `/home/li/primary/Vision/nexus.md`, `/home/li/primary/Vision/messaging.md`
  (older copies); PS`vision-ethos.md`, PS`vision-datom.md` (in the Ethos
  file); PS`vision-orchestrate.md`, PS`vision-horizon.md`; every skill's
  `## Sources` list.
- Flow's own design: context modules (F`edf227/vision/contextModules.md`,
  F`d4ae97/vision/contextModules.md`, F`5ed94b/vision/contextModules.md`,
  F`dea0ba/vision/contextModules.md`, F`9fb0ad/vision/systemPrompt.md`, the
  context-module entries of F`e5a0bc/vision/flow.md`); the metaflow
  lifecycle, refresh, titles, spirit and startup entries of
  F`d4ae97/vision/flow.md` and F`f5a6e9/vision/flow.md`;
  F`41fa34/vision/flow-component.md`, F`42265e/vision/flow-component.md`,
  F`01e496/vision/flowNexus.md`, F`01e496/vision/flowLifecycle.md`,
  F`01e496/vision/flowIdentity.md`, F`3ec648/vision/voices.md`,
  F`3ec648/vision/capsule.md`, F`bad807/vision/metaflow.md`,
  F`bad807/vision/voices.md`, F`bad807/vision/flowContextInjection.md`,
  F`bad807/vision/gatedFlows.md`, F`d66c26/vision/voices.md`,
  F`41fa34/vision/speech.md`, F`41fa34/vision/subflows.md`,
  F`dea0ba/vision/subflows.md`, F`ebbe30/vision/flow-startup.md`.
- Relays and duplicates of records quoted here: F`93ba9f/vision/messagingInterface.md`,
  F`93ba9f/vision/callerIdentity.md`, F`f5a6e9/vision/messaging.md`,
  F`bad807/vision/messaging.md`, F`01e496/vision/messaging.md`,
  F`dea0ba/vision/messaging.md`, F`f768df/vision/messenger.md`,
  F`d66c26/vision/messaging.md` (2026-10-05 entry), F`8475a9/vision/flow.md`,
  F`f768df/vision/flow.md`, F`0c85a3/notion/memory.md`.
- Older or narrower messaging and Nexus records: F`9993b5/vision/callerIdentity.md`,
  F`9993b5/vision/messagingIsScripts.md`, F`9993b5/vision/messagingBootstrap.md`,
  F`9993b5/vision/curriculumNexus.md`, F`9993b5/vision/editNexusName.md`,
  F`9993b5/vision/mindMemory.md`, F`48cff7/vision/transcriptNexus.md`,
  F`48cff7/vision/messagingUp.md`, F`efa157/notion/nexusScaffolding.md`,
  F`b49251/vision/nexusAnatomy.md`, F`b49251/vision/flowLaunching.md`,
  F`d8df70/vision/messaging.md`, F`6cc91b/vision/interflowMessaging.md`,
  F`6cc91b/vision/typedPrompts.md`, F`6cc91b/vision/agentAuthentication.md`,
  the other entries of F`6cc91b/vision/messenger.md` and
  F`6cc91b/vision/nexus.md`, F`056f6d/vision/messaging.md`,
  F`056f6d/vision/psycheGeneratedMessaging.md`, F`c8d79f/vision/operational-unityWebSpeaksSignal.md`,
  F`e167d8/vision/stableNext.md`, F`fe945a/vision/stableNext.md`,
  F`b05237/vision/operational-messagingDatomSyntax.md`,
  F`b05237/vision/operational-messengerUsesDatomNow.md`,
  F`024bc7/vision/signal.md`, F`bcd02a/vision/signal.md`,
  F`bcd02a/vision/nexus.md`, F`bcd02a/vision/runtime.md`,
  F`6997eb/vision/repositoryClassification.md`,
  F`fe945a/vision/repositoryClassification.md`, F`d4ae97/vision/curriculum.md`.
- The remaining messaging records of the 2026-10-08 census
  (F`d4ae97/reports/flow-ethos-census/census.json`, subtopic messaging,
  142 records).
