<!-- to-the-living:start -->
Presentation.{ «Flow: CLI, deployment, long term — second edition» }

# Flow: CLI, deployment, long term — second edition

## Crystallization

### Proposal 4: a needed metaflow is started whether or not it is running; with no working transcript to reawaken, it is fed its context modules and its prompt — second edition

File: `psyche-context/skills/vision-flow.md` («What it does», L24, the last sentence added; the figure under it)

```text
- A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+
+ +----------------------+
+ | a request for a      |
+ | metaflow             |
+ +----------------------+
+    | reaches
+    v
+ +----------------------+
+ | Flow                 |
+ +----------------------+
+    | starts
+    v
+ +----------------------+
+ | a flow of it, with   |
+ | no working           |
+ | transcript to        |
+ | reawaken             |
+ +----------------------+
+    | is fed
+    v
+ +----------------------+
+ | the metaflow's       |
+ | context modules, and |
+ | the prompt it is to  |
+ | get now              |
+ +----------------------+
```

File: `psyche-context/skills/vision-model-roles.md` (L52–55, superseded)

```text
  Vertical communication stays within one aspect and normally advances one layer
- at a time. If the adjacent layer is absent or unavailable, routing advances to
- the next running layer in that direction, so a Tertiary may reach the Primary
- when the Secondary is not running. The missing layer is reported as a gap; it
- does not make the message disappear.
+ at a time.
```

File: `psyche-context/skills/vision-model-roles.md` (L62–69, superseded)

```text
  Horizontal routing selects the unique eligible cell in the target aspect at
- the sender's layer. Vertical routing selects the nearest eligible
- layer in the requested direction within the same aspect. Busy is still
- eligible. Missing or unavailable needs fresh lifecycle and route evidence.
- Multiple bindings for one cell are an unresolved conflict, never fanout. No
- eligible cell yields an explicit undeliverable result. Resolve the binding
- immediately before each attempt. A fallback has succeeded only when the exact
- recipient accepts it; an ambiguous attempt remains attached to that recipient
- and is reconciled instead of being resent to another layer.
+ the sender's layer.
+ Busy is still
+ eligible.
+ Multiple bindings for one cell are an unresolved conflict, never fanout.
+ Resolve the binding
+ immediately before each attempt.
```

Ruling, one number or none; the proposal as shown stands unless a number says otherwise:

1. The sentence and the figure land in vision-messaging, a new section «A needed metaflow is started» after L33, and vision-flow L24 stands unchanged.

2. The vision-model-roles lines stand, marked short-term:

File: `psyche-context/skills/vision-model-roles.md` (under choice 2, L51; L52–55 and L62–69 unchanged)

```text
- Vertical communication stays within one aspect and normally advances one layer
+ Short-term: vertical communication stays within one aspect and normally advances one layer
```

3. Machine choice, the vertical route said in vision-model-roles too, one sentence added after L52:

File: `psyche-context/skills/vision-model-roles.md` (under choice 3, after L52)

```text
+ A layer a request needs is started whether or not it is running.
```

4. A metaflow with a working transcript is reawakened from it; the sentence shown becomes:

File: `psyche-context/skills/vision-flow.md` (under choice 4, the added sentence)

```text
- A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A metaflow a request needs is started whether or not it is running: with a working transcript, its flow is reawakened from it; with none, it is fed the metaflow's context modules and the prompt it is to get now.
```
<!-- to-the-living:end -->
