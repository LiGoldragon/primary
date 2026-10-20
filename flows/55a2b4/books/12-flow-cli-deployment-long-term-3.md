<!-- to-the-living:start -->
Presentation.{ «Flow: CLI, deployment, long term — third edition» }

# Flow: CLI, deployment, long term — third edition

File: `psyche-context/skills/vision-flow.md` (figure after L24)

Machine: the placement.

```figure
┌──────────────────────────┐
│ a request for a metaflow │
└────────────┬─────────────┘
             │ reaches
             ▼
┌──────────────────────────┐
│ Flow                     │
└────┬────────────────┬────┘
     │ running:       │ not running:
     │ delivers to    │ reads
     ▼                ▼
┌──────────┐ ┌──────────────────┐
│ the flow │ │ its transcript   │
└──────────┘ └───┬──────────┬───┘
                 │ young:   │ old or none:
                 │ wakes as │ gives way to
                 ▼          ▼
     ┌──────────────┐ ┌────────────────────┐
     │ the flow,    │ │ a fresh flow,      │
     │ reawakened   │ │ modules and prompt │
     └──────┬───────┘ └─────────┬──────────┘
            └─────────┬─────────┘
                      │ short-term:
                      │ if a Primary,
                      │ starts after
                      ▼
           ┌─────────────────────┐
           │ its Secondary, live │
           └─────────────────────┘
```

### Proposal 1: a still-young transcript is reawakened

File: `psyche-context/skills/vision-flow.md` («What it does», L24)

```text
- A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with a still-young working transcript its flow is reawakened from it; with none, or an old one, it is fed the metaflow's context modules and the prompt it is to get now.
```

Machine: the old-transcript branch.

### Proposal 2: a young context

File: `psyche-context/skills/vision-flow.md` (after L62, the refresh paragraph)

```text
  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ A context is young while it stays under half the layer's refresh threshold. Past about a hundred thousand tokens a context degrades fast, so only a young transcript is reawakened; an older one gives way to a fresh flow fed the metaflow's context modules.
```

Machine: the ratio.

1. A third of the model's context window.

### Proposal 3: a Primary starts after its Secondary; queuing is a long-term goal

File: `psyche-context/skills/vision-flow.md` («Starting flows», after L34)

```text
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+
+ Short-term: a Primary starts only after its Secondary is live; a launch that needs a Primary starts the Secondary first.
```

Machine: the second clause.

File: `psyche-context/skills/vision-flow.md` («What it does», L24)

```text
- A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; queuing is a long-term goal, for much higher output quality and efficiency: an interruption alone interrupts, and when it is done all of the queue that should go with it comes in; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
```

### Proposal 4: a flow launched without a brief has the default task

File: `psyche-context/skills/vision-flow.md` («Starting flows», after L34)

```text
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+
+ A flow launched without a brief has the default task: a proposal or a question.
```

Machine: the home.

2. The line lands in `intent-startup-prompt`, after its L8.
<!-- to-the-living:end -->
