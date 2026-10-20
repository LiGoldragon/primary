<!-- to-the-living:start -->
Presentation.{ «How Flow is used» }

# How Flow is used

Machine: production runs Flow 0.35.10; version 0.35.11 is published and awaits cutover. Everything here is read from Flow's main branch (0.35.11, whose wire is unchanged from 0.35.10) and from production records of 0.35.10. Nothing here is on a development branch.

```
+--------------------+  +---------------------+
| the living         |  | a running flow      |
+---------+----------+  +----------+----------+
          |                      |
          | sends a request      | sends a request
          | (through Message)    | (command or tool)
          v                      v
+--------------------------------------------+
| Flow                                       |
| starts, wakes, sleeps and addresses flows  |
+----------------------+---------------------+
                       |
                       | keeps one per address
                       v
+--------------------------------------------+
| metaflow                                   |
| address { Field publisher Quaternary }     |
| state: Awake, Asleep or Ended              |
| queue of requests, each with its sender    |
+----------------------+---------------------+
                       |
                       | is run, one at a time, by
                       v
+--------------------------------------------+
| flow  3ff3fe                               |
| one session in a terminal pane             |
+--------------------------------------------+
```

Machine: Flow is the program that starts model sessions, keeps track of them and carries requests to them. A metaflow is one standing address: an aspect (Psyche, Mind or Field), a topic (a camelCase word; `core` when nothing special) and a layer (Primary, Secondary, Tertiary or Quaternary). A flow is one run of a metaflow: one model session, Claude or Codex, in one terminal pane. Herdr is the program that holds those panes. A seat is a running flow in its metaflow. A flow's id is six characters, such as `3ff3fe`, and its pane is titled with its address and id: `{ Field send-proof-03510 Quaternary 3ff3fe }`.

```
+------------------+      +-------------------+
| flow command     |      | flow-meta command |
| anyone can run   |      | the owner, Message|
|                  |      | or a flow of an   |
|                  |      | allowed aspect    |
+--------+---------+      +---------+---------+
         |                          |
         | speaks on                | speaks on
         v                          v
+------------------+      +-------------------+
| ordinary wire    |      | meta wire         |
| Start  Stop      |      | Configure Refresh |
| Current Metaflows|      | Deliver Command   |
| Report           |      | Retire            |
+--------+---------+      +---------+---------+
         |                          |
         +-------------+------------+
                       |
                       | both reach
                       v
              +-----------------+
              | Flow            |
              +-----------------+
```

Machine: Flow has two doors, each a typed channel (a wire) written as datoms on a Unix socket, a local file that programs connect through. The `flow` command speaks the ordinary wire; the `flow-meta` command speaks the meta wire, which answers only the owner, the Message program, or a flow whose aspect the configuration allows.

```
+--------------------------------------------+
| metaflow Awake                             |
| a seat is running in a terminal pane       |
+----------------------+---------------------+
                       |
                       | turn ends, nothing queued
                       v
+--------------------------------------------+
| metaflow Asleep                            |
| pane closed, transcript kept               |
+----------------------+---------------------+
                       |
                       | an Order or
                       | Question is queued
                       v
+--------------------------------------------+
| wake                                       |
+----------+-----------------------+---------+
           |                    |
           | context is small   | context is large,
           |                    | or Refresh was
           |                    | asked
           v                    v
+--------------------+  +--------------------+
| resumed            |  | started fresh      |
| the old session    |  | from its modules   |
+---------+----------+  +----------+---------+
          |                        |
          +-----------+------------+
                      |
                      | hands over the queue,
                      | oldest first
                      v
+--------------------------------------------+
| metaflow Awake                             |
+--------------------------------------------+
```

Machine: an idle topic costs no running program. A seat that finishes its turn with nothing queued is put to sleep, and a queued request of the right kind wakes the metaflow with its whole queue.

## 1. What Flow is to its users

Machine: a metaflow is what people and flows address; its flows come one after another. It has a state, Awake as one flow, Asleep or Ended; a list of its earlier flows, Past; and a Queue of the requests that reached it, each kept with its sender.

- A request is one of six kinds: an Order (work for the target), a Question, a Result, a Notice (an error or blocker that touches its work), and the living's words, `Psyche` for one saying and `Psyches` for several.
- The layer decides the model. Flow holds one model per layer. Production declares Primary `claude-fable-5-1`, Secondary `claude-opus-5-5`, Tertiary `claude-sonnet-5-5` and Quaternary `claude-haiku-5-5`, read from the Primary configuration file and declared on 2026-10-17.
- Sleeping. When a Claude seat's turn ends, Flow notes how large its context was, waits for Herdr to show the seat at rest, and, if nothing is queued, closes its pane and records the metaflow Asleep; the flow joins Past and its transcript is kept. If something is queued, the oldest request is typed into the pane and the seat stays awake. A Primary is never put to sleep, and a Codex seat is not either, because only a Claude flow can be resumed.
- Waking. An Order, a Question or the living's words queued for an Asleep metaflow wake it. A Result or a Notice waits in the queue for the next wake. A Primary is never woken by Flow; what is queued for it waits. The wake hands the whole queue over in one prompt, oldest first. It resumes the last flow's session when that session's context at its last stop was under the layer's refresh threshold, or when no threshold is configured, which is production's state now. Otherwise, or when a Refresh was asked, the wake starts a fresh session at the layer's model and medium effort, from the module identities and leave-outs of the metaflow's last launch.
- The three context repositories. A flow's context is made of modules, plain-text skills, and they live only in `psyche-context`, `mind-context` and `field-context`, one per aspect. A launch names modules by identity; no path or text travels in it.
- A leave-out is a named part of a harness's startup that a flow goes without: a tool, an instruction block or a harness feature. A metaflow's configuration sets its default leave-outs, and a launch may name its own list instead.

## 2. The interfaces

Machine: every command takes exactly one datom and prints each reply as a datom. In a block of two or more datoms, the first is the request and the last is its reply. Long datoms are laid out on several lines here for the phone; on a command line each is one line, and the reader treats any whitespace the same.

## 2.1 The command lines

```bash
flow 'Current.{ Mind nexus Secondary }'
# Current.Asleep
flow 'Metaflows'
flow --version
flow-meta 'Refresh.{ Mind flow Secondary }'
flow-meta reset attempt-1
```

Machine: `flow` speaks on the ordinary socket and `flow-meta` on the meta socket. `FLOW_SOCKET` and `FLOW_META_SOCKET` name another Nexus's sockets. An error goes to standard error and the exit status is 2. The only commands that are not datoms are `flow --version`; `flow-meta reset <key> [credit]`, which asks the Codex app-server to use a reset credit (the key makes a retry safe); and `flow-meta register-claude|register-codex …`, which registers a session started before Flow.

## 2.2 The ordinary wire

Machine: Start launches a flow. It carries eleven things in order: a request id; the system modules; the user modules; the Address; the model; the effort; the predecessor, `None` for a new start or `Some.<flow id>`; the flows to remember, each with a depth; the Herdr session; the leave-outs, where `None` takes the metaflow's default and `Some.[ … ]` replaces it; and the brief, the one text a Start carries.

```datom
Start.{ request-7
  [ spirit-core ]
  [ operation-main-flow knowledge-flow ]
  { Field flow Primary }
  gpt-6-astra medium
  Some.836818
  [ { 1b8ac0 1 } ]
  messaging-build
  Some.[ SkillTool WorkflowTool ]
  «Carry this bounded launch request.» }
```

Machine: the reply is `Started`, as production returned it for a Codex flow: the flow id, its native session id, the Herdr route it runs in (session, pane name, pane, terminal), and its origin, `Unbound` when the caller was no flow, otherwise `Flow.{ id session }`.

```datom
Started.{ 3ff3fe
  01a1497a-7fba-7a13-b28a-2873ff3fe0bc
  Available.{ default
    codex-9f44235592816c2dbe28a6cb wN:p1
    term_65e0706826867a5 }
  Unbound }
```

Machine: other ordinary queries. `LaunchStatus.<request id>` answers one snapshot of a launch; `Observe.Launch.<request id>` keeps answering at each phase change until the launch settles. `Stop.<flow id>` closes a flow's pane. `Report.{ <flow id> <event> }` is what a Claude hook sends, with the event `Started`, `ToolUsed.<tool>` or `Stopped`; the reply is `Reported`.

```datom
Report.{ f1c841 Stopped }
```

Machine: reading the state. `Current.<Address>` answers `Current.Awake.<flow id>`, `Current.Asleep`, `Current.Ended` or `Current.Unknown`. `Metaflows` lists every metaflow.

```datom
Listed.[
  { { Psyche flow Primary }
    Ended
    [ past-1 ]
    [ { Sender.{ Mind flow Tertiary }
        Order.continue }
      { Unknown Notice.kept } ] } ]
```

Machine: `ResolveCaller.None` names the flow that is calling, from the process the kernel reports, never from the request.

```datom
ResolveCaller.None
CallerResolved.{ 38de5b Psyche High
                 claude-opus-5-5 }
```

Machine: four requests are the Message program's alone: Identify (which address a process runs in), Lock (reserve a recipient for a lease), Deliver (queue a request under the lock) and Release. Any other caller is answered `Refused.NotMessage`. The recipient of a Lock may also be `Up`, the layer above in the sender's aspect and topic. The two numbers in Identify are a process id and its start time.

```datom
Identify.{ 40211 1792234100 }
Identified.{ Psyche nexus Secondary }
```

```datom
Lock.{ { Psyche nexus Secondary }
       { Mind nexus Secondary } }
Locked.{ { Psyche nexus Secondary }
         { Mind nexus Secondary }
         1792234200 }
```

```datom
Deliver.{ { { Psyche nexus Secondary }
            { Mind nexus Secondary }
            1792234200 }
          Order.«Run the tier tests.» }
Queued
```

## 2.3 The meta wire

Machine: Configure declares one family of settings whole, replacing what was there in one commit; an entry left out of the declaration is removed. The reply is `Configured.Replaced`, or `Configured.Unchanged` when nothing differed. The families are Models (one model per layer), Thresholds (per layer, two numbers), LeaveOuts (per metaflow Address) and Nexus (sockets, Codex endpoints and the Message program).

```datom
Configure.Models.[
  { Primary claude-fable-5-1 }
  { Secondary claude-opus-5-5 }
  { Tertiary claude-sonnet-5-5 }
  { Quaternary claude-haiku-5-5 } ]
Configured.Replaced
```

```datom
Configure.Thresholds.[
  { Primary 600000 700000 } ]
```

Machine: of the two threshold numbers, this build reads only the second, the refresh threshold, when it decides to resume or start fresh; I found no reader of the first. Production has declared none.

```datom
Configure.LeaveOuts.[
  { { Field publisher Quaternary }
    [ ClaudeAiConnectors ExplorePlanAgents
      WorkflowTool SkillTool BundledSkills
      ScheduleWakeupTool ReportFindingsTool
      ListAgentsTool CronTools DeferredTools
      ClaudeMd GitInstructions ] } ]
```

Machine: that entry is production's default for the Field publisher; declared alone it would remove every other entry. The Nexus family has the source root, two Codex endpoints (client, home, control socket, models), the keys each harness takes, the aspects allowed on this wire, the Message socket and program, and the lease in seconds. It is shown here with placeholder paths. A running Nexus reads its endpoints when it opens, so a changed endpoint is served from the next start.

```datom
Configure.Nexus.{ /srv/source
  { stable-client /srv/codex
    /srv/codex/control.sock
    [ gpt-5.6-sol gpt-5.6-luna ] }
  { next-client /srv/codex-next
    /srv/codex-next/control.sock
    [ gpt-6-sol gpt-6-luna gpt-6-astra ] }
  [ { Claude [ / «!» # ] [ esc esc ] [ enter ] }
    { Codex [ / «!» ] [ esc ] [] } ]
  [ Psyche ]
  /srv/message-nexus.sock
  /srv/message-nexus
  60 }
```

Machine: `Configuration` reads the committed values back as one record of four parts in this order: the Nexus, the models, the thresholds and the default leave-outs. It never returns defaults, and answers `Unconfigured` before a Nexus was declared; it returns the models sorted by layer name, not in the order declared.

Machine: Refresh asks that a metaflow's next wake start a fresh session; the mark clears when the metaflow is recorded awake again. Only an Asleep metaflow is accepted, and a second Refresh answers the same.

```datom
Refresh.{ Field startup-proof-0355 Quaternary }
Refreshed.{ Field startup-proof-0355 Quaternary }
```

Machine: MetaBindExisting registers sessions started before Flow, after checking each binding against Herdr. The container names a Herdr session, its server and an owner; each binding names a flow, its aspect, power, model, harness, native session, workspace, pane, tab, terminal, agent, process and working directory.

```datom
MetaBindExisting.{
  { messaging-build /run/user/1001/herdr.sock
    { 4100 1001 server-token } owner-flow }
  [ { psyche-flow Psyche High claude-opus
      Claude psyche-native workspace wD:p9
      wD:t9 psyche-terminal psyche-agent
      { 4200 1001 psyche-token } /srv/work } ] }
```

Machine: the rest of the meta wire. `Deliver` types a message into a flow's pane, in one of three tiers (`Soft`, `MiddleAbrupt`, `HardAbrupt`) whose name heads the pane text; `Vet` answers what Deliver would refuse and types nothing; `Command` types a harness command (`Compact` or `Interrupt`); `Retire.<flow id>` takes a flow out of receiving; `ReadEvents.<flow id>` reads the events its hook reported.

```datom
Deliver.{ m-81b0e4:7d41e0:0 7d41e0
  HardAbrupt.{ m-81b0e4 Owner
    Text.«Stop the build now.» } }
```

```datom
Command.{ 7d41e0 Compact }
Commanded.{ 7d41e0 Compact Transported }
```

```datom
ReadEvents.f1c841
EventsRead.{ f1c841
  [ Started ToolUsed.Bash Stopped ] }
```

## 2.4 The Codex send tool

```
+--------------------------------------------+
| Codex flow                                 |
+----------------------+---------------------+
                       |
                       | calls send:
                       | target, kind, body
                       v
+--------------------------------------------+
| Flow                                       |
| finds the sender in its own records        |
+----------+-----------------------+---------+
           |                    |
           | target can take it | no live sender,
           |                    | no target, or
           |                    | lock held
           v                    v
+--------------------+  +--------------------+
| target's queue     |  | Refused.reason     |
| reply: Queued      |  |                    |
+---------+----------+  +--------------------+
          |
          | wakes the target if it sleeps
          v
+--------------------------------------------+
| target metaflow                            |
+--------------------------------------------+
```

Machine: every Codex flow Flow opens is given one tool, `send`. A Claude flow sends through Message instead. The flow passes the target address, a kind and a body, and never says who it is: Flow takes the sender from its own records of the calling thread.

```json
{
  "target": {
    "aspect": "Field",
    "topic": "startup-proof-0355",
    "layer": "Quaternary"
  },
  "kind": "Order",
  "body": "Run the tier tests."
}
```

Machine: the kinds are `Order`, `Question`, `Result` and `Notice`; the living's words are not among them. The reply is one datom, and the call counts as a success only when it was queued. Production returned this for a first-turn call:

```datom
Queued.{ { Field send-proof-03510 Quaternary }
         { Field startup-proof-0355 Quaternary } }
```

Machine: `Queued` means in the target's queue, never delivered. The refusals are `UnknownTool`, `Malformed`, `ThreadUnowned` (no flow of Flow's runs the thread), `FlowEnded`, `NotAwake` (the sender's metaflow moved on), `KeyReused`, `UnknownRecipient`, `RecipientEnded` and `Held` (Message holds a lock on the target). A call is recorded under its thread, turn and call, so a replay is answered from the record and queued once. A launch's first turn may call the tool before its flow exists; then the sender is the launching metaflow.

## 2.5 What a woken flow reads

Machine: a woken or drained flow gets the queued requests in its prompt, oldest first, each with its sender. The prompt opens with the line «Work queued for this metaflow while no flow of it was running, oldest first, each with who sent it:» and then gives one datom per request. A request queued before Flow kept senders reads `Unknown`.

```datom
{ Sender.{ Mind alpha Tertiary } Order.«Carry on.» }
{ Unknown Notice.kept }
```

## 2.6 Typed refusals

Machine: a refusal is a short typed word, not a sentence. These are the ones a user meets. The first block is what a Start answers, each name after the head `StartRejected.`; the second is the replies of the other requests, whole, and the last line is a send-tool answer.

```datom
AddressAwake
AddressEnded
LeaveOutRefused.Indispensable.ToolSearch
LeaveOutRefused.NeedsWorkflowLeftOut.SkillTool
ContextRefused.ModuleTooLarge
NativeLaunchRefused.{ Receipt ModelOrEffortDiffers }
```

```datom
Refused.NotMessage
Refused.Unknown.FlowId.0a0a0a
RefreshRejected.Awake
RefreshRejected.NoLaunchProfile
ConfigureRejected.DuplicateEntry
ConfigureRejected.CodexModelsOverlap
MetaRefused.PeerNotAuthorized.{
  da88cf Field Medium gpt-5.5 }
DeliveryRejected.RecipientWorking
DeliveryRejected.BodyRefused.HarnessCommand./compact
CallerResolutionRejected.CallerMismatch.{
  fac697 Mind Medium gpt-6-sol }
Refused.ThreadUnowned
```

- `NotMessage`: a request only the Message program may make, from any other caller.
- `Unknown.FlowId`: a hook report for a flow Flow did not launch; Flow never adopts one.
- `AddressAwake`, `AddressEnded`: a Start whose Address a live seat holds, or an ended one, is refused before anything launches.
- `Indispensable`, `NeedsWorkflowLeftOut`: leave-outs that may not be used; see section 4.
- `ModuleTooLarge`: one module with its part header does not fit one message.
- `ModelOrEffortDiffers`: the model the session reported is not the string the launch named; production met it with `haiku` against `claude-haiku-5-5`.
- `Awake`: only an Asleep metaflow can be refreshed. `NoLaunchProfile`: its last flow has no recorded launch to compose from.
- `DuplicateEntry`: a declaration names one key twice. `CodexModelsOverlap`: a model is named under both Codex endpoints.
- `PeerNotAuthorized`: the meta caller is a flow whose aspect is not allowed; the reply names that flow.
- `RecipientWorking`: a Soft message needs the recipient Idle or Done. `HarnessCommand`: a message whose first line is a harness command is refused; use `Command`.
- `CallerMismatch`: the flow id claimed is not the caller's; the reply carries the true caller.
- `ThreadUnowned`: a send-tool call from a thread no flow of Flow's runs.

## 3. How it is used

```
+--------------+ +-------------+ +--------------+
| psyche-      | | mind-       | | field-       |
| context      | | context     | | context      |
+------+-------+ +------+------+ +------+-------+
       |                |               |
       +----------------+---------------+
                        |
                        | hold the modules,
                        | by identity
                        v
+--------------------------------------------+
| Curriculum                                 |
| finds each named module, returns its text  |
+----------------------+---------------------+
                       |
                       | returns the composed
                       | context
                       v
+--------------------------------------------+
| Flow                                       |
| a Start names modules by id; Flow checks   |
| the answer and opens a terminal pane       |
+----------------------+---------------------+
                       |
                       | types the context,
                       | then the brief
                       v
+--------------------------------------------+
| new flow                                   |
+--------------------------------------------+
```

## 3.1 Starting a new flow

Machine: the caller sends one Start. Flow first checks the Address: a metaflow Awake as a live flow, or named by another unsettled launch, is refused `AddressAwake`, and an Ended one `AddressEnded`. It checks the effective leave-outs, the Start's own or else the metaflow's default. It has Curriculum, the composer, find the named modules and verifies the answer; the harness is Codex when a configured Codex endpoint serves the model and Claude otherwise. It opens a pane in the named Herdr session, starts the session, and records the metaflow Awake as the new flow. The first message is the modules followed by the brief; when it does not fit one message it is sent in parts split where modules begin, each after the seat answered the one before, and the modules are named as the skills given, not to be reloaded. Flow waits for the receipt, that every part was seen in order and the seat answered at the intended model and effort, and then answers `Started`. A launch that ends refused gives the metaflow back as it was found. The caller may follow with `Observe.Launch.<request id>`; a repeated Start of the same request id may answer `LaunchPending` while the first runs.

## 3.2 A flow going to sleep

Machine: the hook of a Claude flow reports `Stopped`. Flow records how large the context was, gives Herdr a bounded wait to show the seat Idle or Done, and then, with nothing queued, closes the pane and records the metaflow Asleep; the flow joins Past and its transcript stays. With something queued, it types the oldest request into the pane and the seat goes on. The metaflow's address, queue and past stay in Flow's store; `flow 'Current.{ … }'` now answers `Current.Asleep`.

## 3.3 A message waking it fresh

Machine: an Order reaches the Asleep metaflow, by a Lock and Deliver from Message or by a send-tool call, and is queued with its sender. After the commit that queued it, Flow reads its own records and, finding the metaflow due a wake, wakes it. On 2026-10-17 production did this for `{ Field startup-proof-0355 Quaternary }` after a Refresh: a new Claude session at `claude-haiku-5-5` and medium effort, with all 36 modules (9 system, 27 user) whole, the sender-attributed Order as the brief, and the answer it was asked for; Flow then slept it, recorded it in Past and emptied its queue. The queue leaves only in the write that records the new flow Awake, so a Nexus that dies mid-wake loses none, and on start wakes every metaflow still holding work.

## 3.4 A Codex flow sending

Machine: the Codex flow calls `send` with a target, a kind and a body. Flow finds the thread's flow in its records, queues the request for the target as a Lock and Deliver would, and answers `Queued.{ sender target }`. If the target sleeps and the kind is an Order or a Question, it wakes. In the 0.35.10 production proof, the first turn of a new Codex flow made exactly one call and received the Queued reply above; the target held one matching Order, with the sender shown.

## 3.5 Refreshing a metaflow

Machine: `flow-meta 'Refresh.{ Field startup-proof-0355 Quaternary }'` answers `Refreshed.{ … }` and marks the metaflow. Nothing starts at that moment. The next wake starts a fresh session from the modules and leave-outs of the metaflow's last launch, however small the old context was, and the wake clears the mark. An Awake metaflow is answered `RefreshRejected.Awake`; one with no recorded launch, `NoLaunchProfile`.

## 3.6 Changing the configuration

Machine: on 2026-10-17 the production model registry was changed from aliases to exact ids. The caller sent one `Configure.Models.[ … ]` with all four layers and got `Configured.Replaced`; the other families were unchanged and no wake was triggered. The next fresh wake used the new ids. Reading it back with `Configuration` returned the four models sorted by layer name, which is not the order sent. Models and leave-outs take effect at the next wake or launch; a Nexus family change takes effect when the Nexus next starts.

## 4. What a user must know that is not obvious

- Model ids are exact. A Start or a Configure must name the string the harness reports, `claude-haiku-5-5`, not `haiku`; a launch that names the alias is refused at the receipt as `ModelOrEffortDiffers`, which production met. A model that no configured Codex endpoint lists is launched on Claude. One model named under both Codex endpoints makes a Configure fail `CodexModelsOverlap`.
- Some leave-outs cannot be used. `ToolSearch` and `BashTool` are refused as `Indispensable`: without the first every deferred tool's schema loads, without Bash a flow cannot message, commit or build. `SkillTool` and `BundledSkills` are refused unless `WorkflowTool` is left out too. A Claude leave-out in a Codex Start, or the reverse, is refused `NotForHarness`.
- A Configure declares its family whole. An entry you do not repeat is removed.
- `Queued` is not delivery. A Result or a Notice does not wake a sleeping metaflow, and nothing wakes a Primary; its queue waits.
- Only a Claude flow sleeps. A Codex flow stays running, and a Refresh is accepted only while the metaflow is asleep.
- Sender attribution has a same-user limit. On the send tool, Flow attributes a call to the metaflow its records bind to the thread; it does not prove who started the turn, and any process of the same user can start a turn on a thread. On Message's path the sender in a Lock is what the bound Message process asserts. Both sockets are owner-only, which stops accidents, not another process of the same user.
- Lock, Deliver and Release are accepted only from the one process that bound itself as Message, and a bind as Message is accepted only from the configured Message executable. The Message program's own test says an Identify from a plain client is answered; the Flow code at this commit refuses it as well with `NotMessage`. I did not run either.

## Crystallization

Machine: three proposals. The first lands lines the living's own records already say and Flow now does; the second lands the interface reference as a knowledge module the machines write and keep; the third points the older knowledge module to it. The older module `knowledge-flow` also holds three paragraphs of dated observations of version 0.24; this book leaves them to a separate ruling.

### Proposal 1: three lines Flow now does · psyche-context › vision/flow.md

Machine: the lines come from the records of 2026-10-16 on the lean flow, on the three context repositories and on injecting the modules; Flow's behavior matches each. The existing lines around them stay.

```text
  To the Nexus, a module's location is nothing but its registry entry.
+
+ A flow starts lean: every part of a harness's startup that can be left out is a named leave-out. A metaflow's configuration sets which are left out by default, and a launch may name its own list, which replaces that default.
+
+ A flow's first message carries the text of every module it was launched with and says that these are its skills, given there, not to be reloaded. A context too long for one message is sent as consecutive parts, split where modules begin.
  …
  Every context module lives outside it, the basic modules included, so that a change to a module causes no Nix rebuild.
+ Context modules, raws included, live only as raw modules in the three aspect context repositories, Psyche, Mind and Field, and nowhere else. A launch names a module by its identity alone, never by a path or a text.
```

Ruling: Land the three lines.

a. Land them as written.
b. Land them with changes.
c. Land none.

### Proposal 2: the interface reference · mind-context › skills/knowledge-flow-interface.md, a new file

Machine: a new file, written and kept by the machines from Flow's source and from production replies; nothing is removed. It carries the command lines, the datoms and the send tool as sections 2 and 4 of this book show them, one example each. The lines are as they would be in the file.

```text
+ ---
+ description: A flow is started, stopped, woken, refreshed, sent to or configured, or a Flow reply or refusal is read, and the command line, datom or tool argument is needed.
+ dependencies: [knowledge-flow]
+ ---
+
+ ## Command lines
+
+ `flow '<datom>'` speaks on the ordinary socket and `flow-meta '<datom>'` on the meta socket. Each takes exactly one datom and prints each reply as a datom; an error goes to standard error with exit status 2. `FLOW_SOCKET` and `FLOW_META_SOCKET` name another Nexus's sockets. The meta socket answers `MetaRefused` unless the peer is the owner, the Message program, or a flow whose aspect is in the configured MetaAspects. Lock, Deliver, Release and Identify are answered `Refused.NotMessage` to any other caller.
+
+ ## Start
+
+ Start carries, in order: a request id, the system modules, the user modules, the Address, the model, the effort, the predecessor (`None` or `Some.<flow id>`), the flows to remember, the Herdr session, the leave-outs (`None` takes the metaflow's default, `Some.[ … ]` replaces it), and the brief. Modules are named by identity; a path or a text is refused. Example: `Start.{ request-7 [ spirit-core ] [ operation-main-flow knowledge-flow ] { Field flow Primary } gpt-6-astra medium Some.836818 [ { 1b8ac0 1 } ] messaging-build Some.[ SkillTool WorkflowTool ] «Carry this bounded launch request.» }`. The reply is `Started.{ <flow id> <session id> Available.{ <Herdr session> <pane name> <pane> <terminal> } <origin> }`.
+
+ ## Reading state
+
+ `Current.{ Mind nexus Secondary }` answers `Current.Awake.<flow id>`, `Current.Asleep`, `Current.Ended` or `Current.Unknown`. `Metaflows` answers `Listed.[ … ]`, each metaflow as `{ <Address> <state> [ <past flows> ] [ <queue> ] }`, a queued request as `{ Sender.<Address> <request> }` or `{ Unknown <request> }`. `ResolveCaller.None` answers `CallerResolved.{ <flow id> <aspect> <power> <model> }` for the caller.
+
+ ## Configuring
+
+ `Configure.<family>.[ … ]` on the meta socket declares the whole family and removes any entry it leaves out; the reply is `Configured.Replaced` or `Configured.Unchanged`. Families: Models `[ { <Layer> <model> } … ]`, Thresholds `[ { <Layer> <handover> <refresh> } … ]` (only the second number is read for resuming), LeaveOuts `[ { <Address> [ <leave-out> … ] } … ]`, and Nexus. Models and leave-outs apply from the next wake or launch. `Configuration` reads the four families back, the models sorted by layer name.
+
+ ## Refresh
+
+ `Refresh.{ Mind flow Secondary }` answers `Refreshed.<Address>`, and the next wake of that Asleep metaflow starts a fresh session instead of resuming. An Awake metaflow answers `RefreshRejected.Awake`.
+
+ ## Sleeping and waking
+
+ A Claude seat at rest with nothing queued is put to sleep; a Codex seat and a Primary are not. An Order, a Question or the living's words queued for an Asleep metaflow below Primary wake it; a Result or a Notice waits. The wake resumes the session when its context is under the layer's refresh threshold or none is configured, else starts fresh at the layer's model and medium effort from the last launch's modules and leave-outs.
+
+ ## The Codex send tool
+
+ A Codex flow Flow opens has the tool `send` with `target` (`aspect`, `topic`, `layer`), `kind` (`Order`, `Question`, `Result` or `Notice`) and `body`. The sender is read from Flow's records, never passed. The answer is `Queued.{ <sender> <target> }` or `Refused.<reason>`. Queued is not delivered. A woken flow reads each queued request as `{ Sender.<Address> <request> }`.
+
+ ## Exact names
+
+ A model is named by the string its harness reports, such as `claude-haiku-5-5`; an alias is refused at the receipt as `ModelOrEffortDiffers`. A model no configured Codex endpoint lists is launched on Claude. `ToolSearch` and `BashTool` cannot be left out; `SkillTool` and `BundledSkills` only with `WorkflowTool` left out; a leave-out of the other harness is refused.
+
+ ## Limits
+
+ Attribution of a send-tool call is by thread, from Flow's records, and of a Lock by what the bound Message process asserts. It does not authenticate who started a turn; any process of the same user can.
```

Ruling: Land the module.

a. Land it as written, kept by the machines.
b. Land it, with the Nexus family left out until its paths settle.
c. Do not land it.

### Proposal 3: the older module points to it · mind-context › skills/knowledge-flow.md

Machine: one line added at the end of the older module, after its reading rule; nothing is removed.

```text
  caller identity, store state, or runtime bindings from a source version
  or client path.
+
+ The command lines, datoms, send tool and refusals Flow takes are in `knowledge-flow-interface`.
```

Ruling: Add the line.

a. Add it as written.
b. Add it and rule on the three dated paragraphs next.
c. Do not add it.
<!-- to-the-living:end -->
