<!-- to-the-living:start -->
Presentation.{ «Flow CLI, deployment, long term» }

# Flow CLI, deployment, long term

## Crystallization

### Proposal 1: Flow exposes the harness; Message makes use of it; Flow first

2026-09-24, `flows/88475f/vision/flow.md`, STT: «I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input. Flow basically exposes everything from the harness, and then message makes use of it. So Flow deploys first, and we can use it raw to send messages, even.»

2026-09-23, `flows/836818/vision/flowNexus.md`, STT: «We'll plug message into that after we deploy Flow and we can use it to start a session.»

2026-09-24, `flows/752e0f/vision/herdrSessions.md`, STT: «I want Flow to be our tool to send messages and stuff until it actually uses the Flow API through its socket to actually send messages more sanely.»

Sources: `flows/88475f/vision/flow.md`, 2026-09-24 (relayed by e51411; the same words, elided, at `flows/752e0f/vision/flowDeploy.md`, 2026-09-24); `flows/836818/vision/flowNexus.md`, 2026-09-23; `flows/752e0f/vision/herdrSessions.md`, 2026-09-24. The 88475f words open with an order, «Don't keep adding features … deployed now», which is no line. Landed: vision-flow L22 (Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery), L8–10 and L12 (Flow sets up and starts a flow; a flow the living asks for is launched). Nothing landed says that Flow exposes the harness, that Flow deploys first, or that a flow is stopped through Flow; 33752b «book 37» Proposal 2 («Flow launches, names, delivers to, stops and retires every flow») is pending.

File: `psyche-context/skills/vision-flow.md` («What it does», after L22; «until» is his mark)

```text
  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+
+ Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

The «until» clause; his 2026-09-24 words, `flows/752e0f/vision/herdrSessions.md`: «until it actually uses the Flow API through its socket to actually send messages more sanely»:
4. As shown: the second sentence is the short term, marked by his «until».
5. The first sentence alone; the raw use is not written:

File: `psyche-context/skills/vision-flow.md` (under choice 5, in place of the paragraph above)

```text
- Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
+ Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it.
```

«stop flows»; his 2026-09-24 words, `flows/88475f/vision/flow.md`: «start flows, stop flows, and send messages with Flow»; vision-flow has no stop line, and «book 37» Proposal 2 is pending:
6. «stopped» in the paragraph, as shown, his word; «book 37» Proposal 2 stands beside it.
7. «stopped» left to «book 37» Proposal 2:

File: `psyche-context/skills/vision-flow.md` (under choice 7, the added paragraph)

```text
- Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
+ Flow exposes everything from the harness, the bare input: a flow is started and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
```

### Proposal 2: a refresh needs a recent handover in the transcript; the old flow is verified inactive, exited, and its conversation archived

2026-09-24 14:32Z, `flows/d8df70/vision/flowLifecycle.md`, STT, book comment: «The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it.» «In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.»

2026-09-24 14:28Z, the same record: «A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived.»

Sources: `flows/d8df70/vision/flowLifecycle.md`, 2026-09-24 14:28Z and 14:32Z (the record's provenance: «comment on "What Waits for the Living"»); `flows/836818/vision/flowNexus.md` L25 and L35, the relay of the same words, 2026-09-24. The same 14:28Z words end in a question, «I'd also like to know what happens with archives and if they're searched differently», which is no line. Landed: vision-flow L52–54 (reaping belongs to the refresh event; the replaced end is taken out of receiving) and L58 (the metaflow locked while the refresh runs; the predecessor reaped in the same event). Pending, built on and not re-opened: «book 10» Proposal 2 choices 6 and 7 (who receives while both flows live); «book 06» Proposal 5 (the successor is checked; the predecessor hears only of failure). The handover in the transcript as the condition of a refresh, the verified inactivity, and the archived conversation are not landed.

File: `psyche-context/skills/vision-flow.md` («A replaced session is reaped by the refresh itself», after L58; the figure under it)

```text
  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ A flow is refreshed only when a recent flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
+
+ +----------------------+
+ | the old flow         |
+ +----------------------+
+    | writes, recently
+    v
+ +----------------------+
+ | the handover, in its |
+ | transcript           |
+ +----------------------+
+    | lets Flow refresh; Flow blocks until
+    v
+ +----------------------+
+ | the new flow, ready  |
+ | to receive           |
+ +----------------------+
+    | then, in the same swoop
+    v
+ +----------------------+
+ | the old flow,        |
+ | verified not active, |
+ | exited               |
+ +----------------------+
+    | its conversation goes into
+    v
+ +----------------------+
+ | the archive          |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

«a recent transcript not too old»; his words give no measure, and no word of his on a threshold exists; no machine threshold is written:
4. «recent», unmeasured, as shown.
5. The handover alone, its age unsaid:

File: `psyche-context/skills/vision-flow.md` (under choice 5, the added paragraph)

```text
- A flow is refreshed only when a recent flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
+ A flow is refreshed only when a flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
```

### Proposal 3: anybody may call Flow; a flow refreshes itself safely

2026-09-24 14:30Z, `flows/d8df70/vision/flowTool.md`, STT, book comment: «Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.»

Sources: `flows/d8df70/vision/flowTool.md`, 2026-09-24 14:30Z; `flows/836818/vision/flowNexus.md` L31, the relay. The same words answer the day's question on orphaned locks and on who owns the Flow source («break the locks», «Nobody in particular owns Flow Source»): answers, no line. Landed: vision-flow L20 («No flow declares its id: every call to Flow is identified by the calling process.»), L58 (the Flow CLI identifies the calling process), vision-nexus L56 (a CLI identifies the process that called it). Pending, built on: «book 06» Proposal 3 («Any flow can deploy any other: the structure is decentralized and respawns from any point»). That anybody may call Flow, and that a flow refreshes itself safely for that reason, is not landed.

File: `psyche-context/skills/vision-flow.md` (L20, a sentence after its last)

```text
- A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process.
+ A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
```

Ruling, one number from each group:

The sentence:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it stands; no word of his on this fork:
4. At L20, as shown, machine choice: the sentence follows the one it rests on.
5. After L58, machine choice: beside the refresh paragraph and Proposal 2's:

File: `psyche-context/skills/vision-flow.md` (under choice 5, after L58, in place of the change above; L20 stands, nothing changed)

```text
  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
```

### Proposal 4: an undelivered request tries a higher power, then lower; a crucial metaflow missing is started

2026-09-24 14:31Z, `flows/d8df70/vision/messaging.md`, STT, book comment: «If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules.» «Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.»

«Psyche Medium» and «Psyche High» are his older layer names: the Secondary and the Primary of today, the machine's reading.

His other words at the fork. 2026-09-19, `flows/b81560/vision/operational-verticalRoutingThroughPsycheFirst.md`, STT: «No, psyche high is not universal. In order to get to high, you have to be high, or you have to get to psyche, and then psyche has to... You didn't talk about the up-and-down communication. When something feels too important for a certain layer that they have to share up upstairs, then they send it up, and so on.» 2026-10-07, `flows/6aa08d/vision/fieldStack.md`, STT: «The field stack: when you go up, you go up your own stack, not another aspect. The psyche is not your aspect. You don't go up into another aspect. You go up in your aspect.»

Sources: `flows/d8df70/vision/messaging.md`, 2026-09-24 14:31Z; `flows/836818/vision/flowNexus.md` L33, the relay; `flows/b81560/vision/operational-verticalRoutingThroughPsycheFirst.md`, 2026-09-19; `flows/6aa08d/vision/fieldStack.md`, 2026-10-07. Landed: vision-flow L22 (Flow owns the lock and the delivery, answers sent or queued); vision-model-roles L51–55 (vertical routing advances to the next running layer in that direction) and L61–69 (no eligible cell yields an explicit undeliverable result). «crucial», a higher power and a lower one stand in no skill.

File: `psyche-context/skills/vision-flow.md` («What it does», after L22, after Proposal 1's paragraph; the figures under it)

```text
  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+
+ A request that cannot be delivered tries a higher power: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
+
+ +----------------------+
+ | Message              |
+ +----------------------+
+    | asks Flow to deliver to
+    v
+ +----------------------+
+ | the metaflow         |
+ +----------------------+
+    | not reached: Flow tries
+    v
+ +----------------------+
+ | the layer above      |
+ +----------------------+
+    | none higher: Flow tries
+    v
+ +----------------------+
+ | the layer below      |
+ +----------------------+
+    | the answer says what happened, to
+    v
+ +----------------------+
+ | the caller           |
+ +----------------------+
+
+ +----------------------+
+ | a request            |
+ +----------------------+
+    | needs a crucial metaflow, missing
+    v
+ +----------------------+
+ | Flow                 |
+ +----------------------+
+    | starts
+    v
+ +----------------------+
+ | a flow of it         |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figures:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it lands; no word of his on this fork:
4. vision-flow, as shown, machine choice: the delivery is Flow's, L22.
5. vision-messaging, a new section after L33, machine choice: the undelivered message is the message's subject:

File: `psyche-context/skills/vision-messaging.md` (under choice 5, after L33, in place of the paragraph above)

```text
  Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.
+
+ ## An undelivered request tries a higher power
+
+ A request that cannot be delivered tries a higher power: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
```

«then we try lower» against vision-model-roles L52–55, landed, «routing advances to the next running layer in that direction»; a tension between a landed line and his 2026-09-24 words; his 2026-10-07 words, «you go up your own stack, not another aspect», say nothing of down:
6. L52–55 stand, nothing changed there; the paragraph stands beside them.
7. L52–55 changed:

File: `psyche-context/skills/vision-model-roles.md` (another topic's skill: vision-model-roles; L52–55, under choice 7)

```text
  Vertical communication stays within one aspect and normally advances one layer
- at a time. If the adjacent layer is absent or unavailable, routing advances to
- the next running layer in that direction, so a Tertiary may reach the Primary
- when the Secondary is not running. The missing layer is reported as a gap; it
- does not make the message disappear.
+ at a time. If the adjacent layer is absent or unavailable, routing advances to
+ the next running layer in that direction, so a Tertiary may reach the Primary
+ when the Secondary is not running; when nothing is higher, the layer below is
+ tried. The missing layer is reported as a gap; it does not make the message
+ disappear.
```

«Psyche Medium», «Psyche High», «All the medium and high flows»:
8. The Secondary and the Primary, as shown, machine reading.
9. His words kept:

File: `psyche-context/skills/vision-flow.md` (under choice 9, the added paragraph)

```text
- A request that cannot be delivered tries a higher power: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
+ A request that cannot be delivered tries a higher power: when Psyche Medium is not reached, Psyche High, and when nothing is higher, lower; the answer returned to the caller says what happened, under a set of rules. A flow that is missing is started when a request needs it and it is crucial; all the medium and high flows are crucial.
```

### Proposal 5: one Herdr session is a flow container of typed flows; bound into Flow through the meta socket

Herdr is the terminal multiplexer whose session holds the panes the flows run in.

2026-09-24, `flows/d8df70/vision/flowTool.md`, STT: «Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound.» «They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.»

2026-09-24, the same record: «We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." It's a cluster. No it's a meta flow. No I don't know. It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.»

2026-09-24, the same record («Her sessions» as recorded; the record reads it as Herdr sessions): «Okay, there shouldn't be two Her sessions. Which one is Flow currently attached to? Do you mean Flow will know two containers?»

2026-09-24, `flows/752e0f/vision/herdrSessions.md`, STT («herder» is his spelling, the record says): «I just want a single herder session that's controlled by Flow, the Nexus.»

Sources: `flows/d8df70/vision/flowTool.md`, 2026-09-24, three entries (the record's provenance: «input mode not established»; «herder» and «harder» corrected to Herdr there); `flows/836818/vision/flowNexus.md` L59 and L67, the relay (L67 elides «It's a cluster. No it's a meta flow. No I don't know.»); `flows/752e0f/vision/herdrSessions.md`, 2026-09-24. Landed: vision-flow L20 («where the harness assigns it, Flow learns it when the flow binds»), L30 (the meta socket), vision-nexus L40–44 (the meta socket is privileged). The binding vocabulary stands in meta-signal-flow's `ethos/signal.ethos` (`FlowContainer`, `MetaBindExisting`) and is handled on flow main d190e10 in `crates/flow-nexus/src/lib.rs`, the machine's. No skill has Herdr, a flow container, a typed flow, or the binding of a session already live. «You don't have to spend too much time creating it», «Let's go», «Just get it done» are orders, no line; «Create the anatomy of what a flow looks like» is «book 08» Proposal 2's, pending.

File: `psyche-context/skills/vision-flow.md` («What it does», after L20, after the lines «book 04» Proposal 2 and «book 11» Proposal 6 add there; «for now» and «eventually» are his marks; the figure under it)

```text
  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process.
+
+ One Herdr session is a flow container: it holds many typed flows, psyche, mind and field, with subtypes under them. There is one Herdr session, controlled by Flow. A Herdr session already live, with all of its flows, is bound into Flow through the meta socket: the container first, then its flows in a single call, a vector of structs, each the anatomy of a flow. For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
+
+ +----------------------+
+ | one Herdr session,   |
+ | the flow container   |
+ +----------------------+
+    | bound first, over the meta socket, into
+    v
+ +----------------------+
+ | Flow                 |
+ +----------------------+
+    | then binds, in one call, a vector of
+    v
+ +----------------------+
+ | its typed flows:     |
+ | psyche, mind, field  |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

«typed flow», his word for psyche, mind and field, against L30 and L32, landed, which call them aspects, and against «book 11» Proposal 2, pending, where a subflow is typed by its specialty; one word, two senses:
4. «typed flows, psyche, mind and field», as shown, his words.
5. «a flow of each aspect», machine reading of L30:

File: `psyche-context/skills/vision-flow.md` (under choice 5, the added paragraph)

```text
- One Herdr session is a flow container: it holds many typed flows, psyche, mind and field, with subtypes under them. There is one Herdr session, controlled by Flow. A Herdr session already live, with all of its flows, is bound into Flow through the meta socket: the container first, then its flows in a single call, a vector of structs, each the anatomy of a flow. For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
+ One Herdr session is a flow container: it holds many flows of each aspect, psyche, mind and field, with subtypes under them. There is one Herdr session, controlled by Flow. A Herdr session already live, with all of its flows, is bound into Flow through the meta socket: the container first, then its flows in a single call, a vector of structs, each the anatomy of a flow. For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
```

The import tool; his words: «we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now»:
6. Both sentences, as shown: «for now» and «eventually» are his marks.
7. The «for now» sentence alone; the tool waits for its own record:

File: `psyche-context/skills/vision-flow.md` (under choice 7, the added paragraph's last sentences)

```text
- For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
+ For now the live one is bootstrapped by hand.
```

«Her sessions»; the record's own inference:
8. Herdr sessions, as shown.

### Proposal 6: the metaflow identifier everywhere; the flow id resolved in the runtime

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «If the send command still needs the flow ID, then my change hasn't been done properly. The send command should use the same identifier that we're using now, which is the 3-field identifier of a metaflow. I want the whole system to use that everywhere.» «Essentially the flow ID is registered as the corresponding current flow ID for a metaflow and is resolved in the runtime. The agent doesn't have to figure any of this stuff out.»

2026-10-12, `flows/d68c82/vision/messaging.md`, STT: «I've asked for the flow ID of the sender to be replaced by the actual aspect (like how we name metaflows: aspect, topic, and then layer). That's how I want flows to stop referring to each other by flow IDs»

2026-10-13, `flows/7c89aa/vision/flow-ids.md`, STT («metaphors [sic]» as recorded): «I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13; `flows/d68c82/vision/messaging.md`, 2026-10-12; `flows/7c89aa/vision/flow-ids.md`, 2026-10-13. The 2026-10-13 words go on with orders, «Get Mind to fix that right now», which are no line. Landed: vision-flow L16 («what is addressed is always the metaflow, never a flow»), L32 (a flow's title names its aspect, topic, layer and flow id). Pending, built on: «book 11» Proposal 6 (the flow id almost disappears from the chat; it is for the ledger and the transcript); «book 10» Proposal 1 choices 7 and 8 (whether Flow's answers carry a flow id). The whole system using the identifier, the send command included, and the flow id registered and resolved in the runtime are not landed. The send command's own change goes to its owner outside the book.

File: `psyche-context/skills/vision-flow.md` («What it does», after L16, after the line «book 11» Proposal 7 adds there; the figure under it)

```text
  Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
+
+ The whole system uses the metaflow's three-field identifier, { Aspect Topic Layer }, everywhere, the send command included: the flow id is registered as the metaflow's current flow id and resolved in the runtime, and no agent has to figure it out.
+
+ +----------------------+
+ | a flow               |
+ +----------------------+
+    | sends to { Aspect Topic Layer }
+    v
+ +----------------------+
+ | Flow                 |
+ +----------------------+
+    | resolves, from its registry
+    v
+ +----------------------+
+ | the current flow id  |
+ +----------------------+
+    | delivers to
+    v
+ +----------------------+
+ | the flow of it       |
+ +----------------------+
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

A mirror line in vision-messaging; no word of his on this fork:
4. vision-flow alone, as shown, machine choice: the resolution is Flow's.
5. A line in vision-messaging too, machine choice: the message's address is the message's subject:

File: `psyche-context/skills/vision-messaging.md` (under choice 5, after L9, beside the paragraph above)

```text
  The message body is a datom that lands in the recipient's prompt as a
  datom-formatted object. There is no envelope around it.
+
+ A message is addressed to a metaflow, { Aspect Topic Layer }, and names its sender the same way.
```

### Proposal 7: installed from source; one source for every part; deployed declaratively

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «Well the only way to install anything on our system is to install it from source. If none of them are installed from source, then none of them are installed properly anyway and all of these so-called installations should be removed because that's not how we install anything.»

2026-10-13, the same record: «There should only be one package or one source for all of them and so there should be no version divergence.»

2026-10-13, the same record, inside an order: «Get somebody to audit and make sure everything is deployed declaratively.»

2026-09-24 14:29Z, `flows/d8df70/vision/building.md`, STT, book comment: «They're built and installed from CriomOS so you can check the source that built that generation.»

His earlier words on the declared system. 2026-10-11, `flows/d68c82/vision/criomos.md`, STT: «Well first of all nobody edits files anymore. People do not edit files anymore. That never happens anymore, ever, ever, ever, ever, ever.» 2026-10-01T00:47, `flows/7328f4/vision/stateful.md`, STT, book comment: «I don't want stateful stuff. I want declarative features and then the [nodes] use the features and the behavior is predictable.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13, three entries (the one-source sentence also at `flows/d68c82/log.md` L405, 2026-10-13); `flows/d8df70/vision/building.md`, 2026-09-24 14:29Z (relayed at `flows/836818/vision/flowNexus.md` L29); `flows/d68c82/vision/criomos.md`, 2026-10-11; `flows/7328f4/vision/stateful.md`, 2026-10-01. «I guess find out how that link is made if you want to know» and «all of these so-called installations should be removed» are an answer and an order, no line. Landed: nothing in vision-deployment L6–14 on installation; vision-orchestrate L8–10 (Orchestrate is deployed in the home, its meta binary part of it); vision-nexus L48–51 (for now the default clients are packaged with the Nexus as crates of its repository). Pending, built on: 33752b «book 37» Proposal 8 (everything runs as declared, from one source on main).

File: `psyche-context/skills/vision-deployment.md` (a new section after L14; the figure under it)

```text
  Zeus is a stable node, and stable nodes are not where testing
  happens.
+
+ ## Installed from source, from one source, declared
+
+ The only way to install anything on the system is from source: a running service is built and installed from CriomOS, so the source that built its generation is found from it, and everything is deployed declaratively. A component's parts, the Flow CLI and the Flow Nexus among them, come from one package or one source, so their versions never diverge.
+
+ +----------------------+
+ | one source           |
+ +----------------------+
+    | builds
+    v
+ +----------------------+
+ | the CriomOS          |
+ | generation           |
+ +----------------------+
+    | installs, at one version
+    v
+ +----------------------+
+ | the Nexus and its CLI|
+ +----------------------+
```

Ruling, one number from each group:

The section and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

«all of these so-called installations should be removed»; his 2026-10-13 words:
4. Not in the line, as shown, machine reading: an order on the installations of that day.
5. A sentence added:

File: `psyche-context/skills/vision-deployment.md` (under choice 5, the added section's paragraph)

```text
- The only way to install anything on the system is from source: a running service is built and installed from CriomOS, so the source that built its generation is found from it, and everything is deployed declaratively. A component's parts, the Flow CLI and the Flow Nexus among them, come from one package or one source, so their versions never diverge.
+ The only way to install anything on the system is from source: a running service is built and installed from CriomOS, so the source that built its generation is found from it, and everything is deployed declaratively. An installation not from source is not an installation and is removed. A component's parts, the Flow CLI and the Flow Nexus among them, come from one package or one source, so their versions never diverge.
```

### Proposal 8: the harness components live in the home environment, for now

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «Flow only needs to be installed in the home environment. We can just have all of the harness components installed in the home environment for now until we actually start to layer things and create different permissions and things like that. We're not there yet so let's just keep it simple.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13. Landed: vision-orchestrate L8–10 (Orchestrate is deployed in the home, for every user); vision-flow L36–42 (the flow repository is a runtime repository; every skill lives outside it). The home generation's declarations go to their owner outside the book.

File: `psyche-context/skills/vision-deployment.md` (after Proposal 7's section; builds on it; «for now» and «until» are his marks)

```text
+ For now the harness components, Flow among them, are installed in the home environment, until things are layered and permissions differ.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it lands; no word of his on this fork:
4. vision-deployment, as shown, machine choice: where a thing is installed is deployment.
5. vision-flow, «Repository and skills», machine choice: the line names Flow:

File: `psyche-context/skills/vision-flow.md` (under choice 5, after L42, in place of the line above)

```text
  basic skills give our own take on how an agent behaves in a harness,
  replacing the prompt the harnesses build in.
+
+ For now the harness components, Flow among them, are installed in the home environment, until things are layered and permissions differ.
```

### Proposal 9: rolling forward; tested before it passes; building where the builder is unreachable

2026-09-24, `flows/d8df70/vision/deployment.md`, STT: «What do you mean, roll back? Roll back to what? We have nothing now. We're rolling forward. There's no rolling back because if we roll back we fall off the cliff.»

2026-09-21, `flows/1b8ac0/vision/flowNexus.md`, STT, relayed (the record: «wording as received; verbatim and citation not established»): «Let's release it. Let's deploy it. Let's test it, even if it doesn't pass the test, because we don't have anything right now. Let's test it.»

2026-09-24 14:29Z, `flows/d8df70/vision/building.md`, STT, book comment: «Well when the builder isn't reachable we just build locally.»

Undated, `flows/01a05e53/vision/nixExecution.md`, STT: «"If there are no remote builders, then we have to build locally. That line is not quite correct."»

Sources: `flows/d8df70/vision/deployment.md`, 2026-09-24 (relayed at `flows/836818/vision/flowNexus.md` L43); `flows/1b8ac0/vision/flowNexus.md`, 2026-09-21; `flows/d8df70/vision/building.md`, 2026-09-24 14:29Z (relayed at `flows/836818/vision/flowNexus.md` L27); `flows/01a05e53/vision/nixExecution.md`, undated. The 2026-09-24 words are an order to deploy, «Let's go deploy», and the 2026-09-21 words an order to release; what they rest on is the line. Landed: vision-deployment L6–9 (a proof of concept deploys on the flow's own host); spirit-core («Start with the smallest shape that works.»). Rolling forward, testing before the test passes, and building locally stand in no skill.

File: `psyche-context/skills/vision-deployment.md` («A proof of concept deploys on the flow's own host», after L9; his «right now» is the mark of the second sentence)

```text
  A proof of concept is worked on and deployed on the host the flow is
  running on. Another host is used only when the living names it.
+
+ A deployment rolls forward; there is no rolling back. A proof of concept is released, deployed and tested even when the test does not pass, while nothing else stands, right now.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

The second sentence's mark; his 2026-09-21 words, «because we don't have anything right now»:
4. «while nothing else stands, right now», as shown.
5. The second sentence dropped; the first stands alone:

File: `psyche-context/skills/vision-deployment.md` (under choice 5, the added paragraph)

```text
- A deployment rolls forward; there is no rolling back. A proof of concept is released, deployed and tested even when the test does not pass, while nothing else stands, right now.
+ A deployment rolls forward; there is no rolling back.
```

Building locally; a tension between two records: his 2026-09-24 words, «Well when the builder isn't reachable we just build locally.», and the undated words, «"If there are no remote builders, then we have to build locally. That line is not quite correct."»:
6. No line on building, as shown; the tension stays in the records.
7. A sentence added, his 2026-09-24 words:

File: `psyche-context/skills/vision-deployment.md` (under choice 7, the added paragraph)

```text
- A deployment rolls forward; there is no rolling back. A proof of concept is released, deployed and tested even when the test does not pass, while nothing else stands, right now.
+ A deployment rolls forward; there is no rolling back. A proof of concept is released, deployed and tested even when the test does not pass, while nothing else stands, right now. When the builder is not reachable, the build is made locally.
```

### Proposal 10: work on main until it works

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «I don't know why we're using branches. That thing isn't even in production so let's just work on `main` until it actually works. Get everything merged unless it makes no sense. If that is the case then that's another failure, right? Oh my god, we need to figure out how to avoid that failure.»

2026-09-17, `flows/9993b5/vision/noMoreBranches.md`, STT: «Are you making a bunch of branches? I don't want that. I want everything merged on main, right? All the time. I don't want all these branches. I want all these branches removed. It's too much luggage, too much stuff to carry.»

2026-09-17, `flows/9993b5/vision/launchOnMain.md`, STT, a question: «So, are you merging all? Are you getting a subflow to merge all of the primary worktrees on `main`, and then from `handsporth`, we launch all the primary flows directly on `main` unless specified otherwise?»

Against them, 2026-09-20 03:23, `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md`, STT: «That's how we're going to do it. There are three branches: the field, and each branch can give you three different orchestration trees. The mind keeps trying to merge things. Once an epic is finished in the field, it can try and merge it.» «Actually, everybody is working off primary together because they're all in primary. What I mean is, branches of their own repositories, like criome, right? It has a field branch and a psyche branch, and there's a mind branch.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13; `flows/9993b5/vision/noMoreBranches.md` and `flows/9993b5/vision/launchOnMain.md`, 2026-09-17; `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md`, 2026-09-20. «Get everything merged unless it makes no sense» and «we need to figure out how to avoid that failure» are an order and a question, no line. Landed: vision-committing L6–12 (a commit names its files), nothing on branches. Pending, built on: «book 07» Proposal 13 («A Primary is launched in the shared workspace on main, not in a worktree or on a branch, unless the launch names another place.»).

File: `psyche-context/skills/vision-committing.md` (a new section after L12; «until it actually works» is his mark)

```text
  while the whole repository is locked, when nobody else may be
  editing.
+
+ ## Work on main
+
+ Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
```

Ruling, one number from each group:

The section:
1. Land.
2. Land with changes the living names.
3. Drop.

Unconditional or conditioned; his 2026-09-17 words, «I want everything merged on main, right? All the time.», and his 2026-10-13 words, «That thing isn't even in production so let's just work on `main` until it actually works»:
4. Both sentences, as shown.
5. Unconditional, the 2026-09-17 words alone:

File: `psyche-context/skills/vision-committing.md` (under choice 5, the added section's paragraph)

```text
- Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
+ Everything is merged on main, all the time, with no branch.
```

6. Conditioned, the 2026-10-13 words alone:

File: `psyche-context/skills/vision-committing.md` (under choice 6, the added section's paragraph)

```text
- Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
+ A thing not yet in production is worked on main until it actually works, with no branch.
```

The three branches; a tension between his 2026-09-20 words, «There are three branches: the field … branches of their own repositories, like criome … a field branch and a psyche branch, and there's a mind branch», and his 2026-09-17 and 2026-10-13 words:
7. The section as shown; the 2026-09-20 words stay in their record, nothing added.
8. A sentence added, the 2026-09-20 words:

File: `psyche-context/skills/vision-committing.md` (under choice 8, the added section's paragraph)

```text
- Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
+ Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch. In a repository of its own, criome among them, each aspect works on its branch, field, mind and psyche, and Mind merges a finished epic.
```

Where it lands; no word of his on this fork:
9. vision-committing, as shown, machine choice: merging is committing.
10. vision-deployment, after Proposal 7's section, machine choice: the words answer a deployment held on a branch:

File: `psyche-context/skills/vision-deployment.md` (under choice 10, after Proposal 7's section, in place of the section above)

```text
+ ## Work on main
+
+ Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
```

### Proposal 11: nexuses everywhere are the long-term vision; Clojure tools under a Nexus

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «I want to move towards using the nexuses everywhere. They're the long-term vision and then we have this short-term mission.»

Landed: vision-nexus L120–122, «Everything built from now on is a Nexus, and what was built in another shape is rewritten as one.», and intent-psyche L10, «A short-term vision is named so; an unmarked vision is long-term.»: the nexuses everywhere are the long-term vision already, by the two landed lines together; context, no line.

The unlanded part. 2026-09-29, `flows/c64ee3/vision/flowNexus.md`, STT (the record's context: the parts framed with «maybe» and «I guess» are the living thinking aloud, kept as spoken; «[Clojure]» is the record's correction): «We need proper messages and proper flow creation, which is controlled by a flow nexus that maybe uses some [Clojure] tools internally so this Rust code can call these [Clojure] tools, I guess by Nix paths. Otherwise in testing, I don't know, in the paths, I guess, and so you can make the [Clojure] scripts. Tool names can be quite long and more specialized, like SSH2Integrate or SS or Git, our own VCS, our version control. Maybe we just call it VCS.»

Against it, 2026-10-13, `flows/d68c82/vision/flow.md`, STT: «You're talking about meta sockets, which have to do with nexus, and then you're talking about the short-term solution, which is [Clojure]. Total fucking confusion here.» and 2026-10-13, `flows/da2038/vision/prototypes.md`, STT: «I said before that I want the short-term prototypes to be written in Clojure and I see .mjs and I don't recognize Clojure. I'm pretty sure Clojure is .clj.»

At the fork, 2026-09-29, `flows/c64ee3/vision/versionControl.md`, STT: «There's a tool there that's worth developing into a really simple nexus that we force agents to use instead of [JJ] and Git commands.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13; `flows/c64ee3/vision/flowNexus.md` and `flows/c64ee3/vision/versionControl.md`, 2026-09-29; `flows/d68c82/vision/flow.md`, 2026-10-13; `flows/da2038/vision/prototypes.md`, 2026-10-13. Pending: da2038 «book 1», the vision-stack line (short-term code is written in Clojure). No skill has Clojure, VCS or version control. The 2026-09-29 words are a notion, not ruled; the choices are the machine's.

Ruling, one number from each group:

The Clojure tools inside the Nexus:
1. No line; vision-nexus L120–122 and intent-psyche L10 stand, nothing changed.
2. A sentence added to vision-nexus:

File: `psyche-context/skills/vision-nexus.md` («Splitting a Nexus», after L134, under choice 2)

```text
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
+
+ A Nexus may call Clojure tools by their Nix paths; a tool's name is long and specialized.
```

3. The sentence of choice 2 with the version-control nexus, his 2026-09-29 words:

File: `psyche-context/skills/vision-nexus.md` (after L134, under choice 3, in place of choice 2's line)

```text
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
+
+ A Nexus may call Clojure tools by their Nix paths; a tool's name is long and specialized. Version control is a simple nexus of its own, used instead of JJ and Git commands.
```

The name «VCS»; his words: «Maybe we just call it VCS.»:
4. No line: the name is hedged.

### Proposal 12: the vision reviewed with all of the code; Mind implements as close to it as it can

2026-10-13, `flows/d68c82/vision/flow.md`, STT (the log copy, `flows/d68c82/log.md` L464, reads «Mine [Mind]»): «And then I want to review the vision for it with all of the code. [Mind] will simply implement it as close to the vision that we currently have as he can and then adapt it for every comment or rectification that I make along the way.»

Sources: `flows/d68c82/vision/flow.md`, 2026-10-13; `flows/d68c82/log.md` L464, 2026-10-13, the same words whole. They open with an order, «Get Fable to put together an instruction package for Mind Astra», and «I just want a prototype that works right now»: orders, no line. Landed: vision-aspects L8 («Psyche sees and Mind implements»). Pending, built on: «book 11» Proposal 15 («A book's proposals are implemented before the living comments, and modified when the comment comes.»), vision-book after L14; «book 11» Proposal 14 (books show code).

File: `psyche-context/skills/vision-book.md` (another topic's skill: vision-book; after L14, after «book 11» Proposal 14's and Proposal 15's lines; builds on Proposal 15)

```text
+ The vision is reviewed with all of the code: Mind implements it as close to the vision as it can, and adapts it to every comment or rectification along the way.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it lands; no word of his on this fork:
4. vision-book, as shown, machine choice: the review is the book's, and «book 11» Proposal 15's line stands there.
5. vision-aspects, after L8, machine choice: the line says what Mind does with what Psyche sees:

File: `psyche-context/skills/vision-aspects.md` (another topic's skill: vision-aspects; after L8, under choice 5, in place of the line above)

```text
  Flows of the same topic talk at the same layer across aspects: Psyche sees and Mind implements, so a Psyche topic Secondary and the Mind Secondary of that topic speak directly. Field reaches Psyche through Mind, unless Psyche has just spoken to Field. This holds for every aspect.
+
+ The vision is reviewed with all of the code: Mind implements it as close to the vision as it can, and adapts it to every comment or rectification along the way.
```
<!-- to-the-living:end -->
