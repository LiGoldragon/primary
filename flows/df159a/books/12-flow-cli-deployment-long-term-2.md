<!-- to-the-living:start -->
Presentation.{ «Flow: CLI, deployment, long term — second edition» }

# Flow: CLI, deployment, long term — second edition

Second edition of «Flow: CLI, deployment, long term» (its first edition, Version 3), carrying only what his 2026-10-14 comments changed: Proposal 4, rewritten; Proposals 1 and 3, approved, are landed and not shown again.

## Crystallization

### Proposal 4: a needed metaflow is started whether or not it is running; with no transcript to restart, a fresh flow is fed its context modules and its prompt — second edition

File: `psyche-context/skills/vision-flow.md` («What it does», L24, the last sentence added; the figure under it)

```text
- A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running: with a working transcript, its flow is restarted from it; with none, a fresh flow is fed the metaflow's context modules, along with the prompt it is to get now.
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
+    | starts, none of it running
+    v
+ +----------------------+
+ | a fresh flow of it   |
+ +----------------------+
+    | is fed
+    v
+ +----------------------+
+ | the metaflow's       |
+ | context modules, and |
+ | the request as its   |
+ | prompt               |
+ +----------------------+
```

File: `psyche-context/skills/vision-model-roles.md` (L51–55, the route when a layer is not running; superseded)

```text
  Vertical communication stays within one aspect and normally advances one layer
- at a time. If the adjacent layer is absent or unavailable, routing advances to
- the next running layer in that direction, so a Tertiary may reach the Primary
- when the Secondary is not running. The missing layer is reported as a gap; it
- does not make the message disappear.
+ at a time. If the adjacent layer is not running, Flow starts it, so a Tertiary
+ reaches the Secondary whether or not it is running.
```

File: `psyche-context/skills/vision-model-roles.md` (L61–69, the nearest running layer, the undeliverable result and the fallback to another layer; superseded)

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
+ the sender's layer. Vertical routing selects the adjacent layer in the
+ requested direction within the same aspect; a layer not running is started.
```

Ruling, one number from each group:

The sentence, the figure and the struck lines:
1. Land.
2. Land with changes the living names.
3. Drop.

Where the sentence and the figure land:
4. vision-flow L24, as shown, machine choice: starting a flow and delivering to it are Flow's, L8–10, L20 and L24; vision-messaging holds the message's form, priority, per-harness delivery and witness.
5. vision-messaging, a new section «A needed metaflow is started» after L33, the same sentence and figure, machine choice: the request that finds no flow running is the message's subject.

The first edition's base, an undelivered request trying a higher power, then lower, and a crucial metaflow started:
6. Wholly superseded, as shown: no line, in no skill.
7. Survives beside start-on-demand, machine choice, for a request whose metaflow Flow cannot start; one sentence added after the sentence shown, wherever choice 4 or 5 lands it:

File: `psyche-context/skills/vision-flow.md` (under choice 7, after the added sentence)

```text
+ A request whose metaflow cannot be started tries the layer above in its own aspect, and when nothing is higher, the layer below; the answer returned to the caller says what happened.
```

vision-model-roles L51–55 and L61–69, landed, reaching the next running layer:
8. Changed, as shown: the running layer is no longer the condition.
9. Stand unchanged, marked short-term, machine choice: they describe the routing in place today, and a short-term vision is named so (intent-psyche L8) until start-on-demand is implemented; the one word added to L51:

File: `psyche-context/skills/vision-model-roles.md` (under choice 9, L51)

```text
- Vertical communication stays within one aspect and normally advances one layer
+ Short-term: vertical communication stays within one aspect and normally advances one layer
```

A metaflow with a working transcript:
10. Restarted from it, as shown: the flow is restarted, or a fresh one started.
11. Only the fresh start; the sentence shown becomes:

File: `psyche-context/skills/vision-flow.md` (under choice 11, the added sentence, wherever choice 4 or 5 lands it)

```text
- A metaflow a request needs is started whether or not it is running: with a working transcript, its flow is restarted from it; with none, a fresh flow is fed the metaflow's context modules, along with the prompt it is to get now.
+ A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, a fresh flow is fed the metaflow's context modules, along with the prompt it is to get now.
```
<!-- to-the-living:end -->
