<!-- to-the-living:start -->
Presentation.{ «Flow: vision and production» }

# Flow: vision and production

Production branch. Where a row mentions work on a development branch, it says so.

Flow is the program that starts, puts to sleep and wakes the flows. Field has run it live, step by step, over the last days. It does what it was built to do for the flows it started itself. It does not yet look after the working flows you talk to.

A metaflow is one standing topic of work, such as Psyche core at the Secondary layer; a flow is one run of it. Flow keeps a list of metaflows and which of them are awake, asleep or ended. That list is the registry you asked for.

```
+------------------------------------+
| the living's working flows         |
| Psyche, Mind and Field topics      |
+-----------------+------------------+
                  |
                  | are not listed in
                  v
+------------------------------------+
| Flow's list of metaflows           |
| five Field test flows and Message  |
+-----------------+------------------+
                  |
                  | puts to sleep, wakes
                  v
+------------------------------------+
| Claude flows that Flow started     |
+------------------------------------+
```

A flow that is asleep keeps no harness, so it takes no memory. This is the first thing you asked Flow for.

```
+------------------------------------+
| Claude flows below Primary         |
+-----------------+------------------+
                  |
                  v
+--------------------+
| awake              |
| the turn is working|
+---------+----------+
          |
          | turn ends, nothing queued
          v
+--------------------+
| asleep             |
| window closed,     |
| session kept       |
+---------+----------+
          |
          | order, question or the
          | living's words arrive
          v
+--------------------+
| awake again        |
| small: resumed     |
| big: started fresh |
+--------------------+

+------------------------------------+
| never take this path:              |
| Codex flows and Primaries          |
+------------------------------------+
```

How a message reaches a flow that is asleep, and what it does there.

```
+--------------------+
| sender flow        |
+---------+----------+
          |
          | asks to send
          v
+--------------------+
| Message            |
+---------+----------+
          |
          | locks, hands over
          v
+--------------------+
| Flow's queue       |
+---------+----------+
          |
          | order, question or the
          | living's words wake it
          v
+--------------------+
| the sleeping flow  |
| gets the queue,    |
| oldest first       |
+--------------------+
```

## Vision against production

Each row says what production does and how that is known: seen in the source code (code), seen working by Field (live), or not witnessed (not seen). The evidence is kept in the reference file beside this book.

| Row | Status |
|---|---|
| Sessions not running keep no harness | partly |
| Registry, context size, resume against fresh | partly |
| The queue and what wakes | partly |
| Messages waking flows; the messaging bridge | done for flows Flow started |
| Old hm-send, and sessions not under Flow | not started |
| A needed flow is started; default task; no Primary without a Secondary | partly |
| Context from the three repositories only | partly |
| Title format | done |
| Flow id | contradicted by the later records |
| Roles, per-role models, thresholds | partly |
| Living messenger, Illustrator, Publisher | not started |
| Refresh | partly |
| Heartbeat | not started |
| Reports and books at the end of each task | not started |
| Hooks as events; no polling | partly |
| Who may message whom | not started |
| Ethos traits and the datom dialect | partly |
| Subflows replace the harness subagents | not started |
| The word seat | contradicted |

### Sessions not running keep no harness: partly

**Vision.** flows/da2038/vision/flow.md, 2026-10-15 (no harness for a session that is not running, because of memory); flows/44cda5/vision/sessions.md, 2026-10-15 (mark such sessions non-running in the registry).

**Production.** A Claude flow below Primary closes its window when its turn ends and nothing is queued for it; its metaflow is marked asleep and its session kept (code; live: test flows slept this way on 10-16 and 10-17). Codex flows never sleep: only a Claude flow counts as resumable, and Codex reports no turn end to Flow (code). A Primary is never put to sleep (code). On 10-15, 15 of 19 idle panes held 2.2 GB (witnessed by this flow); that stays true of every Codex flow and every flow outside Flow.

**Gap.** Codex sleeping is not started. Flows outside Flow are not covered (see the row on sessions not under Flow).

### Registry, context size, resume against fresh: partly

**Vision.** flows/44cda5/vision/sessions.md, 2026-10-15 (the context size is written; resume if not too big); flows/da2038/vision/flow.md, 2026-10-14 (a still-young transcript is reawakened; a proposal on what young means is owed).

**Production.** The registry holds each metaflow as awake, asleep or ended, with its past flows (code; live). The size of a flow's context is read from its transcript at each turn end and kept (code; live: seven sizes stored). A sleeping flow is resumed when its size is under its layer's refresh number, and started fresh when over (code). No layer has a refresh number in production, so every flow resumes, however large (live: Flow's database holds none; code: no number means resume).

**Gap.** The too-big half is switched off until numbers are declared. The proposal on what young means is made here, as proposal 4.

### The queue and what wakes: partly

**Vision.** flows/da2038/vision/flow.md, 2026-10-14 (queuing is a goal post; the whole queue comes in with the interruption); flows/44cda5/vision/sessions.md, 2026-10-15 (important enough: restart; otherwise queue).

**Production.** Each metaflow has a durable queue, oldest first. An order, a question or the living's words wake a sleeping metaflow, and the whole queue goes into its first prompt; a result or a notice waits there (code). A request that arrives during a wake is queued and typed in afterwards (code). Nothing ranks requests by importance beyond their type, and no small model judges whether to wake (code). After a Flow restart one retained order was delivered a second time; Field recorded that delivery is not exactly-once (live). Raw delivery into a pane still carries the three priority heads Soft, MiddleAbrupt and HardAbrupt (code); flows/b7ba00/vision/messaging.md, 2026-09-26, calls priority heads the wrong approach.

**Gap.** The raw priority heads contradict the 09-26 record (ruling 14). No importance ranking and no small-model judgment: not started.

### Messages waking flows; the messaging bridge: done for flows Flow started

**Vision.** flows/875960/vision/flow.md, 2026-10-11 (Flow owns the lock and delivers; Message subscribes to Flow's events); flows/da2038/vision/flow.md, 2026-10-14 (Flow exposes the harness, Message makes use of it).

**Production.** Message asks Flow for a lock and hands the request over; Flow queues it and wakes the recipient (code). Live: a Flow-started Claude flow sent with the message command, the request was queued, and the sleeping recipient was resumed in its own session; a Codex flow sent in its first turn through a send tool that Flow gives each Codex thread, and exactly one order arrived, marked with its sender. That tool knows which thread called, not who started the call (Field, live). Message subscribing to Flow's events: not seen.

**Gap.** The subscription part is not witnessed.

### Old hm-send, and sessions not under Flow: not started

**Vision.** No raw record speaks of sessions Flow did not start. The 2026-10-15 order about memory covers every session (flows/da2038/vision/flow.md).

**Production.** Flow can import an already running pane after checking it with Herdr (code); that an imported flow then sleeps is unverified. In production Flow lists six metaflows: five Field test flows and Message's own. None of your working Psyche, Mind or Field metaflows is among them (live: the list at the last cutover). Those keep running outside Flow and reach each other through the old hm-send messenger. Each flow Flow starts is also registered with that messenger; a flow that has already gone to sleep leaves the registration failing, and the adapter (the script that turns a launcher call into Flow's start) then treats a missing pane as queue-only (live, 10-16). An hm-send from an old pane to a sleeping Flow-started flow, end to end: not seen.

**Gap.** Adopting the working flows is not started.

### A needed flow is started; default task; no Primary without a Secondary: partly

**Vision.** flows/da2038/vision/flow.md, 2026-10-14, three entries: a needed flow is started whether or not it runs; a flow with no task defaults to a proposal or a question; no Primary is started without a Secondary in the short term.

**Production.** A sleeping metaflow wakes fresh from the module names of its last start, with its queue (code; live: a fresh wake with all 36 modules). A request to an address with no row is refused as unknown, not started (code). Flow keeps no table of its own binding a topic to its modules: the module-configuration table was retired empty (live: Flow's database listing); the binding is whatever the last start named. A start requires a task, and the adapter refuses an empty one; there is no default task (code). Nothing checks that a Secondary exists before a Primary starts; a Primary is never woken automatically, which is a different rule (code).

**Gap.** Starting a metaflow that has no row, the default task, and Secondary-first are not started.

### Context from the three repositories only: partly

**Vision.** flows/da2038/vision/flow.md, 2026-10-16: the flow starter injects every module's text; modules live only in the three aspect repositories, enforced in how the code is written; every removable startup part is a named module (a leave-out: a startup part a flow goes without).

**Production.** A start names modules only; no path or text travels in it. Flow asks the context composer (Curriculum) for the text, checks the answer it gets back, texts against their hashes, and refuses what the composer did not give (code). Started this way, a Claude flow received all 36 modules and a Codex flow 34, whole and once, then answered (live). Leave-outs: 26 named parts, defaults for 21 addresses, a start may override, and three are refused as indispensable (code; live: the 21 read back). Open: some Codex developer-instruction blocks cannot be removed (code); the move of about fifty outside context texts into the three repositories is an open order of Field and Mind; the launcher rows name raw record files by path, outside the three repositories (code; whether a start passes them: not seen); the guard type is hand-written, and a version generated from Ethos exists on a development branch.

**Gap.** Done for the starter and the guard; partly for the whole system.

### Title format: done

**Vision.** flows/7c89aa/vision/flow-ids.md and flows/da2038/vision/flow.md, 2026-10-16 (topic uncapitalized; one datom struct for every pane and tab, Claude and Codex alike).

**Production.** Every flow Flow starts is titled with one datom struct of aspect, topic, layer and flow id, for Claude and Codex alike, such as { Field flow Quaternary 2712d3 }: aspect and layer capitalised, topic lowercase (code; live: both titles read back in Herdr). Line 49 of the skill shows the same capitals. Flow lowercases the topic in the title only; it checks the form of a topic nowhere, and hyphenated proof topics and capitalised launcher-row topics exist.

**Gap.** The topic check is not started. You have not been asked whether aspect and layer stay capitalised (ruling 15).

### Flow id: contradicted by the later records

**Vision.** flows/01a05826/vision/flowIdentity.md, 2026-08-31 (six characters, lengthened on collision); flows/9fb0ad/vision/identifiers.md, 2026-10-03, and flows/d4ae97/vision/flow.md, 2026-10-07 (a word id); skill line 26 (the hash of the session id).

**Production.** A six-character lowercase hex alias claimed for the session by a helper. Flow chooses a Claude session's id before the harness starts and learns a Codex session's when it binds (code), as line 26 says. The word id has not been built.

**Gap.** The records split between six characters and words; production follows the earlier (proposal 2).

### Roles, per-role models, thresholds: partly

**Vision.** flows/da2038/vision/flow.md, 2026-10-16 (role definition files in datom, in a separate repository; per-role subagent models); flows/d68c82/vision/flow.md, 2026-10-13 (EDN, one configuration per metaflow).

**Production.** The model is set per layer: four entries with exact model ids (live: read back). A layer may carry a handover number and a refresh number, but none is set, and the handover number is read nowhere (code). Leave-outs are set per address. Roles are EDN rows in the launcher configuration of Primary, one file per metaflow: the launcher rows (code). There are no datom role files, no role repository and no per-role model exception; the book «Metaflow roles» is unruled.

**Gap.** Role files and the per-role exception are not started. The two formats disagree (ruling 12).

### Living messenger, Illustrator, Publisher: not started

**Vision.** flows/da2038/vision/flow.md, 2026-10-16, three entries; the last names the Field Tertiary the Illustrator and the Quaternary the Publisher, the one to contact.

**Production.** Launcher rows exist for a Field Illustrator (Sonnet, Tertiary) and a Field Publisher (Haiku, Quaternary) (code). Neither is in Flow's list (live). Field's order waits on the context composer and a native policy; the Sonnet-subagent exception exists nowhere in production code.

**Gap.** Not started in Flow.

### Refresh: partly

**Vision.** Skill lines 75 to 77; flows/da2038/vision/flow.md, 2026-10-16 (refresh reliably; the Illustrator as the practice metaflow).

**Production.** A refresh request marks a sleeping metaflow so that its next wake is a fresh start; it is refused when the metaflow is awake or ended (code; live: a fresh wake after the mark). Replacing a flow with a successor and stopping the predecessor after the successor starts exists with fixture tests (code); no live use seen. Not built: refreshing an awake flow, telling a flow it is near its limit, the handover, and the trigger at a size.

**Gap.** Partly: the fresh start works; the trigger and the handover do not exist.

### Heartbeat: not started

**Vision.** flows/da2038/vision/flow.md, 2026-10-16 (return to the important topics at an interval).

**Production.** No timer in Flow (code: none found). Field delivered a design to Core and enabled no timer (Field's order list).

**Gap.** Not started; the interval is unsettled (proposal 9).

### Reports and books at the end of each task: not started

**Vision.** flows/da2038/vision/flow.md, 2026-10-16, two entries (a report when a Secondary or Primary task ends; a book per context module type).

**Production.** Flow's protocol has a Presentation name and a turn-end request. Flow refuses the turn-end request, since it holds no turn-end queue, and nothing turns a marked block in a transcript into a book (code). The books you receive are made by the flows themselves.

**Gap.** Not started.

### Hooks as events; no polling: partly

**Vision.** Skill line 75; flows/55a2b4/vision/flow.md, 2026-10-14 (Flow decides where hooks talk).

**Production.** Claude's hooks call the Flow command, and Flow stores the event (code; live). Codex has no hook; Flow reads Codex's state through Herdr. Flow does not decide where a hook's notification goes. A launch waits in bounded loops, up to 40 tries at 250 ms for a title; no standing poller found (code).

**Gap.** Routing hook events is not started (proposal 7).

### Who may message whom: not started

**Vision.** Skill line 51; flows/d4ae97/vision/flow.md, 2026-10-07; flows/da2038/vision/flow.md, 2026-10-14 (only Secondaries reach Primaries, enforced in code).

**Production.** Flow lets any known sender lock any known recipient. The refusal for leaving the routes is named in the protocols of both Flow and Message, and nothing in either produces it except one flow ending another's address (code, searched in both). Only `up` is resolved by layer, and a Primary has none above (code).

**Gap.** Contradicts line 51 of the skill: not started.

### Ethos traits and the datom dialect: partly

**Vision.** flows/da2038/vision/flow.md, 2026-10-16 (all traits in Ethos long term, without in the short term; Flow accepts prompts and specialized flows from definitions in a datom dialect Ethos specifies).

**Production.** 48 of the 333 trait declarations sit in files generated from Ethos (the starter 41, the send tool 7); the others are hand-written (code, counted). Start and the other requests are datoms whose shape Ethos specifies. Flow takes no specialized-flow definition (see the row on roles).

**Gap.** As you ruled: short term without. Specialized-flow definitions: not started.

### Subflows replace the harness subagents: not started

**Vision.** Skill lines 79 to 103.

**Production.** None in Flow. This flow's subflows are harness subagents. A guard for the comment-relay subagent role sits on a development branch, unmerged.

**Gap.** Not started.

### The word seat: contradicted

**Vision.** flows/d4ae97/vision/flow.md, 2026-10-05 (there is no seat, it is a flow); Core's order, 2026-10-16 (metaflow and flow, not seat, in model-facing text).

**Production.** Flow's source comments, its protocol comments and the earlier books of this flow still say seat.

**Gap.** Wording only.

## Can we run off production Flow now?

**Not for the whole system yet. For the flows Flow starts itself, yes: that path has been run live end to end.**

### What works today, seen live by Field

- A Claude flow and a Codex flow start from module names; every module arrives whole, once; the flow answers at the intended model and effort, and its title reads back.
- A Claude flow below Primary sleeps when its turn ends and wakes when a message arrives, resumed in its own session, or fresh after a refresh mark, with the whole queue.
- A message from one Flow-started flow to another is queued and wakes it; a Codex flow can send in its first turn.
- Stopping a Codex flow closes exactly its own window and no other.
- Flow and Message restart cleanly; the store keeps every table, and the services ran with no restart through the last cutover.

### What blocks daily use, and who holds it

1. Your working flows are not in Flow. Held by: Field starts or adopts them; the Flow owner builds the adoption; you rule whether live panes are adopted or relaunched.
2. A flow sleeps at once, even while you are typing to it. Held by: You, in proposal 5; the Flow owner builds what you rule. This reads from the code and was not seen on a flow you were attached to.
3. Codex flows never sleep, and can send only when Flow started them. Held by: The Flow owner.
4. No size numbers are declared, so no flow is too big to resume, none is told to hand over, none is refreshed at a size. Held by: You, in proposal 3; the Flow owner, the trigger; Core, the refresh settings in the launcher rows.
5. The old hm-send messenger and Flow are not proven together: a send from an old pane to a sleeping Flow-started flow. Held by: Mind owns the messenger; Field qualifies.
6. Nothing stops a flow from messaging off its route; Primaries are protected by habit only. Held by: The Flow owner and Mind, for Message.
7. A restart can deliver a queued order twice. Held by: The Flow owner; Field disclosed it.

Missing, not blocking: reports at task end, the Publisher and Illustrator, the heartbeat, the default task.

### The shortest path to running on it

1. Rule proposal 5: when a flow sleeps.
2. Run one family through Flow for a few days: the Psyche Flow Secondary with its Tertiary and Quaternary helpers, started by the launcher scripts, which already call Flow's start, and messaged with the message command. Field starts them; the Flow owner watches. Whether a launcher has started a non-test topic flow this way: not seen.
3. Declare the size numbers once proposal 3 is ruled; that is configuration, not code.
4. Adopt the remaining working flows, by import or by relaunch, once the pilot holds.
5. Codex sleeping and the hm-send test run alongside; they gate only the Codex flows and the old-messenger flows.

## Where the vision disagrees with itself

Records of yours that disagree with each other, or with the skill. Each is settled by the proposal or ruling named.

- **Flow id form.** six characters (2026-08-31) against words (2026-10-03, 2026-10-07) against the skill's hash; flow ids to almost vanish from the chat (flows/7c89aa/vision/flow-ids.md, 2026-10-13). Settled by proposal 2.
- **Ancestor naming against the title struct.** skill lines 63 to 67 name a session after its ancestor; the title of 2026-10-16 is aspect, topic, layer and id, with no ancestor. Settled by proposal 1.
- **Refresh sizes.** 60 percent (2026-09-14), 30 percent (2026-09-16), 20 to 40 percent (2026-10-07), a floor of 15 percent, a Claude warning at 200,000 (2026-10-13), then a Claude warning at 128,000 and refresh at 200,000, Codex 96,000 and 150,000 to 160,000, and a young transcript at about 100,000 (2026-10-14). Settled by proposals 3 and 4.
- **Role and metaflow rows.** datom role files in their own repository (2026-10-16) against EDN rows, one per metaflow (2026-10-13; 2026-10-16 19:06). Settled by ruling 12.
- **Heartbeat.** a four-hour timer and a six-hour one in the same record; a Luna monitor (2026-09-16) against Codex-driven (2026-10-16). Settled by proposal 9.
- **First act of a flow.** a presentation of its context (2026-10-09); a proposal for crystallization on refresh, and a default task of a proposal or a question (2026-10-14). Settled by proposal 6.
- **Low-usage mode.** ordered 2026-10-14; the context of 2026-10-16 10:56 says it was ending; no record says it ended. Settled by ruling 13.
- **Raw priority heads.** kept in raw delivery; called the wrong approach on 2026-09-26. Settled by ruling 14.
- **Casing of aspect and layer.** his words of 2026-10-16 cover the topic only; a relayed all-lowercase ruling was withdrawn by Core. Settled by ruling 15.

## Crystallization

Every proposal lands in `psyche-context/vision/flow.md`, with the line numbers it names read from the file as it stands. The proposals follow the records read whole, with their later statements.

### Proposal 1: the title, and the ancestor naming · psyche-context › vision/flow.md

Line 49 gets the whole-struct wording of the title that every pane and tab now carries. Lines 63 to 67 say a session is named after its direct ancestor; the title names no ancestor, and production titles carry none (code).

```text
- Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
+ Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id, on every pane, tab and other representation, for every harness: { Psyche core Secondary <id> }.
  …
- ## A session is named after its direct ancestor
- A session cannot be named for what it will become, because nothing is known about it when it is created. Its ancestor is known exactly, so the ancestor is the name.
```

Ruling: Land the title wording and the removal.

a. As shown: the title is the struct, and the ancestor naming goes.
b. Land line 49 only; keep the ancestor naming as the harness's session name beside the title.
c. Land line 49, and carry the ancestor in the title.
d. Neither.

### Proposal 2: the form of a flow id · psyche-context › vision/flow.md

Line 26 says what a flow id is made from and not what it looks like. Production uses six characters, as the record of 2026-08-31 asked; the later records ask for words.

```text
- A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
+ A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
```

Ruling: Land the form of the id.

a. As shown: six characters, lengthened on a collision (what runs).
b. Three words that map back to the session id, in place of the added words.
c. Six characters in the ledger and three words wherever you read it.
d. Neither.

### Proposal 3: two sizes for a refresh, and one repeated sentence · psyche-context › vision/flow.md

Line 77 repeats the hook sentence of line 75; the edit drops the repeat. It also gives the two sizes your records name. The record of 2026-10-13 puts the Claude warning at 200,000 tokens; the later record of 2026-10-14 puts it at 128,000 and the refresh at 200,000. Production has two slots per layer and none is set.

```text
  …
- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+ A flow is refreshed when its context passes the layer's thresholds: at the first it is told and writes its handover, at the second it is replaced as it goes idle (Claude 128,000 and 200,000 tokens; Codex 96,000 and 150,000); while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
```

Ruling: Land the two sizes.

a. As shown, Codex replaced at 150,000.
b. As shown, Codex replaced at 160,000.
c. One pair per layer, set in the layer's configuration, with no numbers in the skill.
d. Neither.

### Proposal 4: what a young transcript is · psyche-context › vision/flow.md

The proposal your record of 2026-10-14 asked for. It replaces proposal 4 of the book «Flow: sleeping and waking seats», which waited on it. Production resumes a flow when its size is under the layer's refresh number, so it uses the refresh size as the measure of young; your record names about 100,000 tokens, apart from the refresh sizes.

```text
- A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no young transcript to reawaken (young: under about 100,000 tokens of context), it is fed the metaflow's context modules and the prompt it is to get now.
```

Ruling: Land what young means.

a. As shown: young is under about 100,000 tokens, apart from the refresh sizes.
b. Young is under the layer's refresh size, as production has it; no added words.
c. Young is a ratio of the harness's window, to be named.
d. Neither.

### Proposal 5: when a flow sleeps · psyche-context › vision/flow.md

Production closes a Claude flow's window when its turn ends and nothing is queued, whatever layer it is below Primary. From the code, that includes a flow you are typing to; this was not seen on an attached flow. Your record of 2026-10-14 speaks of a flow that has sat idle for some time; your record of 2026-10-15, of a session that is not running. This extends proposal 1 of the book «Flow: sleeping and waking seats» and adds Codex. If a is chosen, the idle time is a separate ruling.

```text
  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.
+ A session of any harness that is not running keeps no harness: once its turn has ended and the harness has stayed idle for a set time, with nothing waiting in its queue, the harness closes; the transcript stays and the metaflow is marked asleep in the registry. The timer is a poller, registered and reported.
```

Ruling: When a flow sleeps.

a. As shown: after a set idle time, any harness.
b. At once when its turn ends and nothing is queued (what Claude flows do now); no added words.
c. At once, except a flow you are typing into, which stays until you leave it; how that is known is not designed.
d. Neither.

### Proposal 6: the default task and the first act · psyche-context › vision/flow.md

Your 2026-10-14 comment approved a default task of a proposal or a question. Production requires a task with every start and has no default. The record of 2026-10-14 on refresh adds a first act of crystallization; the record of 2026-10-09 asked for a presentation of the context instead.

```text
  …with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A flow started with no task has the default task of making a proposal or asking a question.
```

Ruling: Land the default task.

a. As shown.
b. As shown, and add: a refreshed flow's first act is a proposal for the crystallization of what it carries.
c. Neither.

### Proposal 7: Flow decides where hooks talk · psyche-context › vision/flow.md

Your 2026-10-14 record. Today a hook reports only to Flow, and Flow does not route the event onward (code).

```text
  Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.
+ Flow decides where each hook's event goes: a hook is a standard call with the right data, and Flow's database says what notification goes where, by the hook and by where it came from.
```

Ruling: Land the line.

a. As written.
b. Neither.

### Proposal 8: lean flows · psyche-context › vision/flow.md

Your 2026-10-16 comment on the refresh study. Production already has it: 26 named leave-outs, defaults per address, a start may override. The skill says nothing of it.

```text
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+ Every removable part of a flow's startup is a named leave-out. A metaflow's row names the leave-outs it takes by default; a start may override them.
```

Ruling: Land the line.

a. As written.
b. Neither.

### Proposal 9: the heartbeat · psyche-context › vision/flow.md

Your 2026-10-16 record. One record gives a four-hour timer and, in the same breath, six hours, four times a day, which is the same as every six hours. Your 2026-09-16 records put the heartbeat on a Luna monitor; the later one says mostly Codex-driven, with Opus and Fable guiding. Nothing is built or enabled.

```text
  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.
+ A heartbeat brings the machine back to its important topics: at a set interval it checks that each is being worked on and wakes its owner when it is not, driven mostly by Codex, with Opus and Fable guiding.
```

Ruling: Land the heartbeat.

a. As shown, every six hours, four times a day.
b. As shown, every four hours.
c. Not yet.

### Proposal 10: reaching the living; reports at task end · psyche-context › vision/flow.md

Your three records of 2026-10-16; the last one names the roles. Nothing of it exists in Flow (row on reports). The book «Metaflow roles» lands only the reach line; this lands the roles and the report. Book types follow the context module type, as you said.

```text
  Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.
+ Reaching the living is a body function, done by a Field metaflow: its Tertiary is the Illustrator and its Quaternary the Publisher, the one every sender reaches. When a metaflow ends the task given to its Secondary or Primary and has no other, a report is made as a book, its type after the context module type of what it holds: vision, intent, knowledge, compensation or inquiry.
```

Ruling: Land the paragraph.

a. As written.
b. Land it in another skill, named in the ruling.
c. Neither.

### Proposal 11: two superseded records · flows › d8df70/vision/messaging.md

**Archive** flows/d8df70/vision/messaging.md

2026-09-24. Your 2026-10-14 comment called the old vision of undeliverable requests obsolete; the skill carries the later vision.

```text
## An undeliverable message escalates to a higher power, then lower; missing crucial flows are started; medium and high flows are crucial
If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules.
Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.
```

**Archive** flows/f5a6e9/vision/flow.md

2026-10-08, also at flows/d4ae97/vision/flow.md line 181. The next day's record corrects it: the topic is uncapitalized, a camelCaseExpression.

```text
## The topic is a dense string: PascalCase of a certain number of words, with a checker
The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.
```

Ruling: Archive the two superseded records.

a. Archive both.
b. Archive the first only.
c. Archive the second only.
d. Neither.

## Rulings without a landing

Ruling: Where do role and metaflow rows live now?

a. EDN rows in the launcher configuration for now, datom role files in their own repository later; the book «Metaflow roles» waits.
b. Datom role files now; the book «Metaflow roles» proceeds.
c. EDN rows stay.

Ruling: Is low-usage mode still in force? (flows/da2038/vision/flow.md, 2026-10-14)

a. Ended: the record is archived.
b. In force: every Fable call goes through you.
c. In force for Fable only, not for the lean Opus stack.

Ruling: Raw delivery into a pane carries the three priority heads; the record of 2026-09-26 calls them the wrong approach for the normal format.

a. Remove the heads from raw delivery too.
b. Keep them on the debugging raw path only.
c. Keep them as they are.

Ruling: Aspect and layer in a title: your words of 2026-10-16 cover the topic only.

a. Capitalised, as line 49 shows: { Psyche core Secondary 6f51ad }.
b. All lowercase: { psyche core secondary 6f51ad }.

<!-- to-the-living:end -->
