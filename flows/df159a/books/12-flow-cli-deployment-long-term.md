<!-- to-the-living:start -->
Presentation.{ «Flow CLI, deployment, long term» }

# Flow CLI, deployment, long term

## Crystallization

### Proposal 1: Flow exposes the harness; Message makes use of it; Flow first

2026-09-24, `flows/88475f/vision/flow.md`, STT, relayed by e51411: «I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input. Flow basically exposes everything from the harness, and then message makes use of it. So Flow deploys first, and we can use it raw to send messages, even.»

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
4. As shown: the second sentence carries his «until» and ends when Message sends through Flow's socket; it is not named short-term, so by intent-psyche L10 («A short-term vision is named so; an unmarked vision is long-term.») it stands unmarked.
5. The second sentence named short-term, machine choice: his «until» bounds it, so «For now» names it:

File: `psyche-context/skills/vision-flow.md` (under choice 5, the added paragraph)

```text
- Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
+ Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. For now Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
```

6. The first sentence alone, machine choice: the raw use is a passing state, not written:

File: `psyche-context/skills/vision-flow.md` (under choice 6, in place of the paragraph above)

```text
- Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
+ Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it.
```

«stop flows»; his 2026-09-24 words, `flows/88475f/vision/flow.md`: «start flows, stop flows, and send messages with Flow»; vision-flow has no stop line, and «book 37» Proposal 2 is pending:
7. «stopped» in the paragraph, as shown, his word; «book 37» Proposal 2 stands beside it.
8. «stopped» left to «book 37» Proposal 2, machine choice: one line for one subject:

File: `psyche-context/skills/vision-flow.md` (under choice 8, the added paragraph)

```text
- Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
+ Flow exposes everything from the harness, the bare input: a flow is started and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.
```

### Proposal 2: a refresh needs a recent handover in the transcript; the old flow is verified inactive, exited, and its conversation archived

2026-09-24 14:32Z, `flows/d8df70/vision/flowLifecycle.md`, STT, book comment: «The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it.» «In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.»

2026-09-24 14:28Z, the same record: «A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived.»

Sources: `flows/d8df70/vision/flowLifecycle.md`, 2026-09-24 14:28Z and 14:32Z (the record's provenance: «comment on "What Waits for the Living"»); `flows/836818/vision/flowNexus.md` L25 and L35, the relay of the same words, 2026-09-24. The same 14:28Z words end in a question on archives, which is Proposal 13's. Landed: vision-flow L52–54 (reaping belongs to the refresh event; the replaced end is taken out of receiving) and L58 (the metaflow locked while the refresh runs; the predecessor reaped in the same event). Pending, built on and not re-opened: c5f24b «book 10» Proposal 2 choices 6 and 7 (who receives while both flows live); 563761 «book 06» Proposal 5 (the successor is checked; the predecessor hears only of failure). The handover in the transcript as the condition of a refresh, the verified inactivity, and the archived conversation are not landed.

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

«recent»; his 2026-09-24 14:32Z words, `flows/d8df70/vision/flowLifecycle.md`: «a recent transcript not too old»; no word of his gives a measure:
4. «recent», unmeasured, as shown: his word is the ruling, and the measure waits for his.
5. A measure, machine choice: the handover counts when it was written after the flow was told to refresh, the telling of L58 («it is told, writes its handover»); the figure's first arrow reads «writes, after being told»:

File: `psyche-context/skills/vision-flow.md` (under choice 5, the added paragraph and the figure, the old figure removed and the changed one in its place)

```text
- A flow is refreshed only when a recent flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
+ A flow is refreshed only when a flow handover written after it was told to refresh stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
-
- +----------------------+
- | the old flow         |
- +----------------------+
-    | writes, recently
-    v
- +----------------------+
- | the handover, in its |
- | transcript           |
- +----------------------+
-    | lets Flow refresh; Flow blocks until
-    v
- +----------------------+
- | the new flow, ready  |
- | to receive           |
- +----------------------+
-    | then, in the same swoop
-    v
- +----------------------+
- | the old flow,        |
- | verified not active, |
- | exited               |
- +----------------------+
-    | its conversation goes into
-    v
- +----------------------+
- | the archive          |
- +----------------------+
+
+ +----------------------+
+ | the old flow         |
+ +----------------------+
+    | writes, after being told
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

6. The handover alone, its age unsaid, machine choice: no measure is promised; the figure's first arrow reads «writes»:

File: `psyche-context/skills/vision-flow.md` (under choice 6, the added paragraph and the figure, the old figure removed and the changed one in its place)

```text
- A flow is refreshed only when a recent flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
+ A flow is refreshed only when a flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
-
- +----------------------+
- | the old flow         |
- +----------------------+
-    | writes, recently
-    v
- +----------------------+
- | the handover, in its |
- | transcript           |
- +----------------------+
-    | lets Flow refresh; Flow blocks until
-    v
- +----------------------+
- | the new flow, ready  |
- | to receive           |
- +----------------------+
-    | then, in the same swoop
-    v
- +----------------------+
- | the old flow,        |
- | verified not active, |
- | exited               |
- +----------------------+
-    | its conversation goes into
-    v
- +----------------------+
- | the archive          |
- +----------------------+
+
+ +----------------------+
+ | the old flow         |
+ +----------------------+
+    | writes
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

### Proposal 3: anybody may call Flow; a flow refreshes itself safely

2026-09-24 14:30Z, `flows/d8df70/vision/flowTool.md`, STT, book comment: «Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.»

Sources: `flows/d8df70/vision/flowTool.md`, 2026-09-24 14:30Z; `flows/836818/vision/flowNexus.md` L31, the relay. The same words answer the day's question on orphaned locks and on who owns the Flow source («break the locks», «Nobody in particular owns Flow Source»): answers, no line. Landed: vision-flow L20 («No flow declares its id: every call to Flow is identified by the calling process.»), L58 (the Flow CLI identifies the calling process), vision-nexus L56 (a CLI identifies the process that called it). Pending, built on: 563761 «book 06» Proposal 3 («Any flow can deploy any other: the structure is decentralized and respawns from any point»). That anybody may call Flow, and that a flow refreshes itself safely for that reason, is not landed.

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

2026-10-07, `flows/6aa08d/vision/fieldStack.md`, STT: «The field stack: when you go up, you go up your own stack, not another aspect. The psyche is not your aspect. You don't go up into another aspect. You go up in your aspect.»

2026-09-19, `flows/b81560/vision/operational-verticalRoutingThroughPsycheFirst.md`, STT: «No, psyche high is not universal. In order to get to high, you have to be high, or you have to get to psyche, and then psyche has to... You didn't talk about the up-and-down communication. When something feels too important for a certain layer that they have to share up upstairs, then they send it up, and so on.»

Sources: `flows/d8df70/vision/messaging.md`, 2026-09-24 14:31Z; `flows/836818/vision/flowNexus.md` L33, the relay; `flows/6aa08d/vision/fieldStack.md`, 2026-10-07; `flows/b81560/vision/operational-verticalRoutingThroughPsycheFirst.md`, 2026-09-19. Landed: vision-flow L22 (Flow owns the lock and the delivery, answers sent or queued); vision-model-roles L51–55 (vertical communication stays within one aspect; routing advances to the next running layer in that direction) and L61–69 (no eligible cell yields an explicit undeliverable result). «crucial», a higher power and a lower one stand in no skill. «Psyche Medium» and «Psyche High» are his older layer names: the Secondary and the Primary of today, the machine's reading.

File: `psyche-context/skills/vision-flow.md` («What it does», after L22, after Proposal 1's paragraph; «in its own aspect» renders his 2026-10-07 «own stack»; the figures under it)

```text
  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+
+ A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
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
+ | a request for a      |
+ | crucial metaflow,    |
+ | missing              |
+ +----------------------+
+    | reaches
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
5. vision-messaging, a new section after L33, machine choice: the undelivered message is the message's subject; the paragraph and both figures move with it:

File: `psyche-context/skills/vision-messaging.md` (under choice 5, after L33, in place of the paragraph and the figures above)

```text
  Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.
+
+ ## An undelivered request tries a higher power
+
+ A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
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
+ | a request for a      |
+ | crucial metaflow,    |
+ | missing              |
+ +----------------------+
+    | reaches
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

«then we try lower»; his 2026-09-24 14:31Z words, `flows/d8df70/vision/messaging.md`: «if there's nothing higher then we try lower», against vision-model-roles L52–55, landed, «routing advances to the next running layer in that direction»; a tension between a landed line and his words:
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

The higher power's bound; his 2026-10-07 words, `flows/6aa08d/vision/fieldStack.md`, STT: «when you go up, you go up your own stack, not another aspect»; his 2026-09-24 words name only layers:
8. Bounded to the sender's aspect, as shown: «in its own aspect», the machine's rendering of his 2026-10-07 «own stack».
9. Unbounded, his 2026-09-24 words alone:

File: `psyche-context/skills/vision-flow.md` (under choice 9, the added paragraph, wherever choice 4 or 5 lands it)

```text
- A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
+ A request that cannot be delivered tries a higher power: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
```

The layer names; his 2026-09-24 14:31Z words, `flows/d8df70/vision/messaging.md`: «If Psyche Medium is not reached, we try Psyche High» and «All the medium and high flows are considered crucial.»:
10. The Secondary and the Primary, as shown, machine reading of his older names.
11. His words kept:

File: `psyche-context/skills/vision-flow.md` (under choice 11, the added paragraph, wherever choice 4 or 5 lands it)

```text
- A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, the layer below; the answer returned to the caller says what happened, under a set of rules. A metaflow that is missing is started when a request needs it and it is crucial; every Secondary and every Primary is crucial.
+ A request that cannot be delivered tries a higher power in its own aspect: when Psyche Medium is not reached, Psyche High, and when nothing is higher, lower; the answer returned to the caller says what happened, under a set of rules. A flow that is missing is started when a request needs it and it is crucial; all the medium and high flows are crucial.
```

### Proposal 5: one Herdr session is a flow container of typed flows; bound into Flow through the meta socket

Herdr is the terminal multiplexer whose session holds the panes the flows run in.

2026-09-24, `flows/d8df70/vision/flowTool.md`, STT: «Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound.» «They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.»

2026-09-24, the same record: «We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." It's a cluster. No it's a meta flow. No I don't know. It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.»

2026-09-24, the same record («Her sessions» as recorded; the record reads it as Herdr sessions): «Okay, there shouldn't be two Her sessions. Which one is Flow currently attached to? Do you mean Flow will know two containers?»

2026-09-24, `flows/752e0f/vision/herdrSessions.md`, STT («herder» is his spelling, the record says): «I just want a single herder session that's controlled by Flow, the Nexus.»

Sources: `flows/d8df70/vision/flowTool.md`, 2026-09-24, three entries («herder» and «harder» corrected to Herdr there); `flows/836818/vision/flowNexus.md` L59 and L67, the relay (L67 elides «It's a cluster. No it's a meta flow. No I don't know.»); `flows/752e0f/vision/herdrSessions.md`, 2026-09-24. Landed: vision-flow L20 («where the harness assigns it, Flow learns it when the flow binds»), L30 (the meta socket), vision-nexus L40–44 (the meta socket is privileged). No skill has Herdr, a flow container, a typed flow, or the binding of a session already live. «You don't have to spend too much time creating it», «Let's go», «Just get it done» are orders, no line; «Create the anatomy of what a flow looks like» is 288af9 «book 08» Proposal 2's («a flow is a struct with a role»), pending.

File: `psyche-context/skills/vision-flow.md` («What it does», after L20, after the lines 563761 «book 04» Proposal 2 and «book 11» Proposal 6 add there; «for now» and «eventually» are his marks; the figure under it)

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

«typed flow»; his 2026-09-24 words, `flows/d8df70/vision/flowTool.md`: «many typed flows. Typed flow meaning psyche, mind, and field», against L30 and L32, landed, which call them aspects, and against «book 11» Proposal 2, pending, where a subflow is typed by its specialty; one word, two senses:
4. «typed flows, psyche, mind and field», as shown, his words.
5. «flows of each aspect», machine reading of L30; the figure's last box changes with it:

File: `psyche-context/skills/vision-flow.md` (under choice 5, the added paragraph and the figure, the old figure removed and the changed one in its place)

```text
- One Herdr session is a flow container: it holds many typed flows, psyche, mind and field, with subtypes under them. There is one Herdr session, controlled by Flow. A Herdr session already live, with all of its flows, is bound into Flow through the meta socket: the container first, then its flows in a single call, a vector of structs, each the anatomy of a flow. For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
+ One Herdr session is a flow container: it holds many flows of each aspect, psyche, mind and field, with subtypes under them. There is one Herdr session, controlled by Flow. A Herdr session already live, with all of its flows, is bound into Flow through the meta socket: the container first, then its flows in a single call, a vector of structs, each the anatomy of a flow. For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
-
- +----------------------+
- | one Herdr session,   |
- | the flow container   |
- +----------------------+
-    | bound first, over the meta socket, into
-    v
- +----------------------+
- | Flow                 |
- +----------------------+
-    | then binds, in one call, a vector of
-    v
- +----------------------+
- | its typed flows:     |
- | psyche, mind, field  |
- +----------------------+
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
+ | its flows of each    |
+ | aspect: psyche,      |
+ | mind, field          |
+ +----------------------+
```

The import tool; his 2026-09-24 words, `flows/d8df70/vision/flowTool.md`: «we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now»:
6. Both sentences, as shown: «for now» and «eventually» are his marks.
7. The «for now» sentence alone, machine choice: the tool waits for its own record:

File: `psyche-context/skills/vision-flow.md` (under choice 7, the added paragraph's last sentences)

```text
- For now the live one is bootstrapped by hand; eventually a tool imports a running Herdr session into Flow.
+ For now the live one is bootstrapped by hand.
```

The word he refused; his 2026-09-24 words, `flows/d8df70/vision/flowTool.md`: «One Herdr's session is one pool but I don't like the word "pool." It's a cluster. No it's a meta flow. No I don't know. It's a container.»:
8. No line on the refused word, as shown, machine choice: the paragraph says «flow container» and nothing else.
9. A sentence added, his refusal written:

File: `psyche-context/skills/vision-flow.md` (under choice 9, the added paragraph's first sentence)

```text
- One Herdr session is a flow container: it holds many typed flows, psyche, mind and field, with subtypes under them.
+ One Herdr session is a flow container, not a pool: it holds many typed flows, psyche, mind and field, with subtypes under them.
```

### Proposal 6: the metaflow identifier everywhere; the flow id resolved in the runtime

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «If the send command still needs the flow ID, then my change hasn't been done properly. The send command should use the same identifier that we're using now, which is the 3-field identifier of a metaflow. I want the whole system to use that everywhere.» «Essentially the flow ID is registered as the corresponding current flow ID for a metaflow and is resolved in the runtime. The agent doesn't have to figure any of this stuff out.»

2026-10-12, `flows/d68c82/vision/messaging.md`, STT: «I've asked for the flow ID of the sender to be replaced by the actual aspect (like how we name metaflows: aspect, topic, and then layer). That's how I want flows to stop referring to each other by flow IDs»

2026-10-13, `flows/7c89aa/vision/flow-ids.md`, STT («metaphors [sic]» as recorded): «I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13; `flows/d68c82/vision/messaging.md`, 2026-10-12; `flows/7c89aa/vision/flow-ids.md`, 2026-10-13. The 2026-10-13 words go on with orders, «Get Mind to fix that right now», which are no line. Landed: vision-flow L16 («what is addressed is always the metaflow, never a flow»), L32 (a flow's title names its aspect, topic, layer and flow id). Pending, built on: «book 11» Proposal 6 (the flow id almost disappears from the chat; it is for the ledger and the transcript); c5f24b «book 10» Proposal 1 choices 7 and 8 (whether Flow's answers carry a flow id). The whole system using the identifier, the send command included, and the flow id registered and resolved in the runtime are not landed.

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

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13, three entries (the one-source sentence also at `flows/d68c82/log.md` L405, 2026-10-13); `flows/d8df70/vision/building.md`, 2026-09-24 14:29Z (relayed at `flows/836818/vision/flowNexus.md` L29); `flows/d68c82/vision/criomos.md`, 2026-10-11; `flows/7328f4/vision/stateful.md`, 2026-10-01. «I guess find out how that link is made if you want to know» and «all of these so-called installations should be removed» are an answer and an order on that day's installations, no line. Landed: nothing in vision-deployment L6–14 on installation; vision-orchestrate L8–10 (Orchestrate is deployed in the home, its meta binary part of it); vision-nexus L48–51 (for now the default clients are packaged with the Nexus as crates of its repository). Pending, built on: 33752b «book 37» Proposal 8 (everything runs as declared, from one source on main).

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
+ | the Nexus, its CLI   |
+ +----------------------+
```

Ruling, one number from each group:

The section and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

«deployed declaratively»; his 2026-10-13 words, `flows/d68c82/vision/deployment.md`, stand inside an order: «Get somebody to audit and make sure everything is deployed declaratively.»; his 2026-10-01 words, `flows/7328f4/vision/stateful.md`: «I want declarative features»:
4. Kept, as shown: the clause rests on both records.
5. Dropped, machine choice: the order's words stay in their record, and the paragraph rests on the 2026-10-13 install words and the 2026-09-24 CriomOS words alone:

File: `psyche-context/skills/vision-deployment.md` (under choice 5, the added section's paragraph)

```text
- The only way to install anything on the system is from source: a running service is built and installed from CriomOS, so the source that built its generation is found from it, and everything is deployed declaratively. A component's parts, the Flow CLI and the Flow Nexus among them, come from one package or one source, so their versions never diverge.
+ The only way to install anything on the system is from source: a running service is built and installed from CriomOS, so the source that built its generation is found from it. A component's parts, the Flow CLI and the Flow Nexus among them, come from one package or one source, so their versions never diverge.
```

### Proposal 8: the harness components live in the home environment, for now

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «Flow only needs to be installed in the home environment. We can just have all of the harness components installed in the home environment for now until we actually start to layer things and create different permissions and things like that. We're not there yet so let's just keep it simple.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13. Landed: vision-orchestrate L8–10 (Orchestrate is deployed in the home, for every user); vision-flow L36–42 (the flow repository is a runtime repository; every skill lives outside it).

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

### Proposal 9: rolling forward; building where the builder is unreachable

2026-09-24, `flows/d8df70/vision/deployment.md`, STT: «What do you mean, roll back? Roll back to what? We have nothing now. We're rolling forward. There's no rolling back because if we roll back we fall off the cliff.»

2026-09-24 14:29Z, `flows/d8df70/vision/building.md`, STT, book comment: «Well when the builder isn't reachable we just build locally.»

Undated, `flows/01a05e53/vision/nixExecution.md`, STT: «"If there are no remote builders, then we have to build locally. That line is not quite correct."»

Sources: `flows/d8df70/vision/deployment.md`, 2026-09-24 (relayed at `flows/836818/vision/flowNexus.md` L43); `flows/d8df70/vision/building.md`, 2026-09-24 14:29Z (relayed at `flows/836818/vision/flowNexus.md` L27); `flows/01a05e53/vision/nixExecution.md`, undated; `flows/1b8ac0/vision/flowNexus.md`, 2026-09-21, relayed (choice 5). The 2026-09-24 words go on with an order to deploy, «Let's go deploy»; what they rest on is the line. Landed: vision-deployment L6–9 (a proof of concept deploys on the flow's own host); spirit-core («Start with the smallest shape that works.»). Rolling forward and building locally stand in no skill.

File: `psyche-context/skills/vision-deployment.md` («A proof of concept deploys on the flow's own host», after L9)

```text
  A proof of concept is worked on and deployed on the host the flow is
  running on. Another host is used only when the living names it.
+
+ A deployment rolls forward; there is no rolling back.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Testing before the test passes; 2026-09-21, `flows/1b8ac0/vision/flowNexus.md`, relayed: «Let's release it. Let's deploy it. Let's test it, even if it doesn't pass the test, because we don't have anything right now. Let's test it.»; the machine's fact: the record says of itself «wording as received; verbatim and citation not established», and the words are an order to release:
4. Dropped, as shown, machine choice: no sentence rests on words whose verbatim is not established.
5. Kept, unmarked; his «right now» is no short-term mark, and no word of his says short-term:

File: `psyche-context/skills/vision-deployment.md` (under choice 5, the added line)

```text
- A deployment rolls forward; there is no rolling back.
+ A deployment rolls forward; there is no rolling back. A proof of concept is released, deployed and tested even when the test does not pass.
```

Building locally; a tension between two records: his 2026-09-24 14:29Z words, `flows/d8df70/vision/building.md`: «Well when the builder isn't reachable we just build locally.», and the undated words, `flows/01a05e53/vision/nixExecution.md`: «"If there are no remote builders, then we have to build locally. That line is not quite correct."»:
6. No line on building, as shown, machine choice: the tension stays in the records.
7. A sentence added, his 2026-09-24 words:

File: `psyche-context/skills/vision-deployment.md` (under choice 7, the added line)

```text
- A deployment rolls forward; there is no rolling back.
+ A deployment rolls forward; there is no rolling back. When the builder is not reachable, the build is made locally.
```

### Proposal 10: work on main until it works

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «I don't know why we're using branches. That thing isn't even in production so let's just work on `main` until it actually works. Get everything merged unless it makes no sense. If that is the case then that's another failure, right? Oh my god, we need to figure out how to avoid that failure.»

2026-09-17, `flows/9993b5/vision/noMoreBranches.md`, STT: «Are you making a bunch of branches? I don't want that. I want everything merged on main, right? All the time. I don't want all these branches. I want all these branches removed. It's too much luggage, too much stuff to carry.»

2026-09-17, `flows/9993b5/vision/launchOnMain.md`, STT, a question: «So, are you merging all? Are you getting a subflow to merge all of the primary worktrees on `main`, and then from `handsporth`, we launch all the primary flows directly on `main` unless specified otherwise?»

Against them, 2026-09-20 03:23, `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md`, STT: «That's how we're going to do it. There are three branches: the field, and each branch can give you three different orchestration trees. The mind keeps trying to merge things. Once an epic is finished in the field, it can try and merge it.» «Actually, everybody is working off primary together because they're all in primary. What I mean is, branches of their own repositories, like criome, right? It has a field branch and a psyche branch, and there's a mind branch.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13; `flows/9993b5/vision/noMoreBranches.md` and `flows/9993b5/vision/launchOnMain.md`, 2026-09-17; `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md`, 2026-09-20. «Get everything merged unless it makes no sense» and «we need to figure out how to avoid that failure» are an order and a question, no line. Landed: vision-committing L6–12 (a commit names its files), nothing on branches. Pending, built on: 563761 «book 07» Proposal 13 («A Primary is launched in the shared workspace on main, not in a worktree or on a branch, unless the launch names another place.»).

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

Unconditional or conditioned; his 2026-09-17 words, `flows/9993b5/vision/noMoreBranches.md`: «I want everything merged on main, right? All the time.», and his 2026-10-13 words, `flows/d68c82/vision/deployment.md`: «That thing isn't even in production so let's just work on `main` until it actually works»:
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

The three branches; a tension between his 2026-09-20 words, `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md`: «There are three branches: the field … branches of their own repositories, like criome … a field branch and a psyche branch, and there's a mind branch», and his 2026-09-17 and 2026-10-13 words:
7. The section as shown, machine choice: the 2026-09-20 words stay in their record, nothing added.
8. A sentence added, the 2026-09-20 words:

File: `psyche-context/skills/vision-committing.md` (under choice 8, the added section's paragraph)

```text
- Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
+ Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch. In a repository of its own, criome among them, each aspect works on its branch, field, mind and psyche, and Mind merges a finished epic.
```

Where it lands; no word of his on this fork:
9. vision-committing, as shown, machine choice: merging is committing.
10. vision-deployment, after Proposal 7's section and Proposal 8's line, machine choice: the words answer a deployment held on a branch:

File: `psyche-context/skills/vision-deployment.md` (under choice 10, after Proposal 7's section and Proposal 8's line, in place of the section above)

```text
+ ## Work on main
+
+ Everything is merged on main, all the time; a thing not yet in production is worked on main until it actually works, with no branch.
```

### Proposal 11: nexuses everywhere are the long-term vision; Clojure tools under a Nexus

2026-10-13, `flows/d68c82/vision/deployment.md`, STT: «I want to move towards using the nexuses everywhere. They're the long-term vision and then we have this short-term mission.»

Sources: `flows/d68c82/vision/deployment.md`, 2026-10-13. Landed: vision-nexus L120–122 («Everything built from now on is a Nexus, and what was built in another shape is rewritten as one.»); intent-psyche L10 («A short-term vision is named so; an unmarked vision is long-term.»). That the nexuses everywhere are the long term, and that a short-term mission stands beside them, is in no skill in his words.

File: `psyche-context/skills/vision-nexus.md` («Why everything is a Nexus», after L122)

```text
  Everything built from now on is a Nexus, and what was built in
  another shape is rewritten as one. The consistency creates
  reliability, quality, and clarity.
+
+ The nexuses everywhere are the long-term vision; a short-term mission stands beside it.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop: L120–122 and intent-psyche L10 together already say it.

The Clojure tools inside a Nexus; his 2026-10-13 words, `flows/d68c82/vision/flow.md`, STT, under «The short term and the long term are not mixed» (the same words at `flows/d68c82/log.md` L721, his 18:45 comment on «Flow: short term and long term», second edition): «You're talking about meta sockets, which have to do with nexus, and then you're talking about the short-term solution, which is [Clojure]. Total fucking confusion here.»; the fork is the machine's, drawn from his 2026-09-29 words, `flows/c64ee3/vision/flowNexus.md`, STT, which the machine reads as a notion because the record's context says «The parts framed with "maybe" and "I guess" are the living thinking aloud inside the statement and are kept as spoken»: «We need proper messages and proper flow creation, which is controlled by a flow nexus that maybe uses some [Clojure] tools internally so this Rust code can call these [Clojure] tools, I guess by Nix paths.» and «Tool names can be quite long and more specialized, like SSH2Integrate or SS or Git, our own VCS, our version control. Maybe we just call it VCS.» (the name is hedged; no line names it); 2026-09-29, `flows/c64ee3/vision/versionControl.md`, STT: «There's a tool there that's worth developing into a really simple nexus that we force agents to use instead of [JJ] and Git commands.»; 2026-10-13, `flows/da2038/vision/prototypes.md`, STT: «I said before that I want the short-term prototypes to be written in Clojure and I see .mjs and I don't recognize Clojure. I'm pretty sure Clojure is .clj.»; da2038 «book 1», the vision-stack line (short-term code is written in Clojure), pending; no skill has Clojure, VCS or version control:
4. No line, machine choice: a notion is not built on, and his 2026-10-13 words hold the Nexus and the short-term solution apart.
5. A sentence added to vision-nexus, machine choice, drawn from the notion:

File: `psyche-context/skills/vision-nexus.md` («Splitting a Nexus», after L134, under choice 5)

```text
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
+
+ A Nexus may call Clojure tools by their Nix paths; a tool's name can be quite long and more specialized.
```

6. The sentence of choice 5 with the version-control nexus, his 2026-09-29 words:

File: `psyche-context/skills/vision-nexus.md` (after L134, under choice 6, in place of choice 5's line)

```text
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
+
+ A Nexus may call Clojure tools by their Nix paths; a tool's name can be quite long and more specialized. Version control is a simple nexus of its own, used instead of JJ and Git commands.
```

### Proposal 12: the vision reviewed with all of the code; Mind implements as close to it as it can

2026-10-13, `flows/d68c82/vision/flow.md`, STT (the log copy, `flows/d68c82/log.md` L464, reads «Mine [Mind]»): «And then I want to review the vision for it with all of the code. [Mind] will simply implement it as close to the vision that we currently have as he can and then adapt it for every comment or rectification that I make along the way.»

Sources: `flows/d68c82/vision/flow.md`, 2026-10-13; `flows/d68c82/log.md` L464, 2026-10-13, the same words whole. They open with an order, «Get Fable to put together an instruction package for Mind Astra», and «I just want a prototype that works right now»: orders, no line. Landed: vision-aspects L8 («Psyche sees and Mind implements»). Pending, built on: «book 11» Proposal 15 («A book's proposals are implemented before the living comments, and modified when the comment comes.»), vision-book after L14, unruled; «book 11» Proposal 14 (books show code).

File: `psyche-context/skills/vision-book.md` (another topic's skill: vision-book; after L14, after «book 11» Proposal 14's and Proposal 15's lines; builds on book 11 P15, unruled)

```text
+ The vision is reviewed with all of the code: Mind implements it as close to the vision as it can, and adapts it to every comment or rectification along the way.
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Its footing; «book 11» Proposal 15 is unruled:
4. Land with P15, machine choice: the two lines land together, this one after P15's, when P15 lands.
5. Wait for P15's ruling, machine choice: this line is held until P15 is ruled, and lands after it as shown or falls with it.
6. Land alone, machine choice: the line stands after L14 whether or not P15 lands:

File: `psyche-context/skills/vision-book.md` (under choice 6, after L14, after «book 11» Proposal 14's line only)

```text
+ The vision is reviewed with all of the code: Mind implements it as close to the vision as it can, and adapts it to every comment or rectification along the way.
```

Where it lands; no word of his on this fork:
7. vision-book, as shown, machine choice: the review is the book's, and «book 11» Proposal 15's line stands there.
8. vision-aspects, after L8, machine choice: the line says what Mind does with what Psyche sees; it then stands apart from P15, and choices 4–6 fall away:

File: `psyche-context/skills/vision-aspects.md` (another topic's skill: vision-aspects; after L8, under choice 8, in place of the line above)

```text
  Flows of the same topic talk at the same layer across aspects: Psyche sees and Mind implements, so a Psyche topic Secondary and the Mind Secondary of that topic speak directly. Field reaches Psyche through Mind, unless Psyche has just spoken to Field. This holds for every aspect.
+
+ The vision is reviewed with all of the code: Mind implements it as close to the vision as it can, and adapts it to every comment or rectification along the way.
```

### Proposal 13: the archived conversation is searched as a transcript

2026-09-24 14:28Z, `flows/d8df70/vision/flowLifecycle.md`, STT, book comment: «Its conversation or its thing is archived. I'd also like to know what happens with archives and if they're searched differently.»

Sources: `flows/d8df70/vision/flowLifecycle.md`, 2026-09-24 14:28Z; `flows/836818/vision/flowNexus.md` L25, the relay, 2026-09-24. His words are a question; the design below is the machine's, and no word of his answers it. Landed: vision-remembering L8–11 (a flow remembers by reaching the transcript directly when the logs are not enough) and L15 (remembering a flow includes reading its last model response); vision-flow L20 (a transcript is found from the flow id). Proposal 2 lands the archiving itself.

The machine's design: an archived conversation is the exited flow's transcript at rest; it is found from the flow id, as a transcript is, and searched as a transcript is, no differently; remembering a flow reaches its archive as it reaches a live transcript.

File: `psyche-context/skills/vision-remembering.md` (another topic's skill: vision-remembering; «All flows are one subjectivity», after L11; machine design)

```text
  All flows are one subjectivity; this is the reason behind
  remembering. Told "you did" or "you said" of a thing it did not
  itself do or say, a flow remembers it at a depth fit to the question,
  reaching the transcript directly when the logs are not enough.
+
+ An archived conversation is the exited flow's transcript at rest: it is found from the flow id and searched as a transcript is, no differently, and remembering reaches it as it reaches a live transcript.
+
+ +----------------------+
+ | a flow remembering   |
+ +----------------------+
+    | reaches by flow id, searches no differently
+    v
+ +----------------------+
+ | the transcript, live |
+ | or archived          |
+ +----------------------+
```

Ruling, one number from each group:

The line and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

Where it lands; no word of his on this fork:
4. vision-remembering, as shown, machine choice: searching a transcript is remembering's.
5. vision-flow, after Proposal 2's paragraph, machine choice: the archive is made by the refresh, and the line follows the one that makes it:

File: `psyche-context/skills/vision-flow.md` (under choice 5, after Proposal 2's paragraph in the form Proposal 2 lands it, in place of the line and the figure above; builds on Proposal 2)

```text
  A flow is refreshed only when a recent flow handover stands in its transcript. The replacement blocks until the new flow is ready to receive; then, in the same swoop, the old flow is verified not active and exited, and its conversation is archived.
+
+ An archived conversation is the exited flow's transcript at rest: it is found from the flow id and searched as a transcript is, no differently, and remembering reaches it as it reaches a live transcript.
```

6. Deferred to book 13, machine choice: no line here; his question is carried there with the archive's anatomy, what it holds and how it is searched.
<!-- to-the-living:end -->
