<!-- to-the-living:start -->
Presentation.{ «Flow: short term and long term» }

# Flow: short term and long term

Branch: main; Flow is not in production.

Marks used below: (read) is what this flow read in code or a report; (Mind) is Mind Core Primary's claim in its prototype report, not yet witnessed; (inference) is this flow's own reading.

## 1 Short term

```
+--------------------------------------------+
| EDN files: shared, one per aspect,         |
| one per metaflow                           |
+--------------------------------------------+
        | name the context modules,
        | system or user prompt
        v
+--------------------------------------------+
| the launcher, Claude or Codex              |
+--------------------------------------------+
        | starts
        v
+--------------------------------------------+
| a flow, lean, on its topic                 |
+--------------------------------------------+
        | a hook measures its context;
        | at the threshold it warns
        v
+--------------------------------------------+
| the flow, warned                           |
+--------------------------------------------+
        | writes
        v
+--------------------------------------------+
| its handover                               |
+--------------------------------------------+
        | Field compacts it, or restarts it
        v
+--------------------------------------------+
| a successor, clean context                 |
+--------------------------------------------+
        | work done:
        | spun down
        v
+--------------------------------------------+
| the topic, idle                            |
+--------------------------------------------+
        | new input wakes it
        v
+--------------------------------------------+
| a new flow, clean context                  |
+--------------------------------------------+
```

### What the prototype does

Mind Core Primary is building Flow and the Message link as one prototype, as close to vision-flow as it can, choosing where the vision is silent and writing each choice down, so you can test it and review the vision against its code.

- Flow's types already hold a metaflow: its three-field address, its state (awake with a flow, asleep, ended), its past flows, and its queue of requests (read).
- The request types are closed: order, question, your words, a result, a notice (read).
- Flow's operations cover a launch end to end: compose, reserve the id, open the pane, start the harness, bind, title, submit the first prompt, close, release (read).
- Message requests are queued durably by Flow; waking a flow and draining the queue into it are not yet proven (Mind).
- Flow still starts from an explicit start order, not from built-in defaults; part of launch composition still sits in the launcher tools (Mind).
- Checks are pending; no real Flow start and no deployment is claimed (Mind).

### The lean launch from EDN

The launcher now reads EDN (read, uncommitted in Primary):

- one shared file;
- one file per aspect: the harness, the model and effort of each layer, the context modules for the system prompt and for the user prompt;
- one file per metaflow, adding the modules that differ.

Three metaflow files exist so far: Psyche, Mind and Field core Primary (read). A Psyche seat today starts with four modules in its system prompt and fifteen in its user prompt (read). Lean, in your sense, is not reached yet (inference).

### Refresh

A hook measures one seat's context so far, Psyche Core Primary (read, uncommitted). On Claude it warns at two hundred thousand tokens; on Codex at half the model's window (read). The warning tells the flow the refresh procedure has started: write a handover of judgment only, name the topics to split off. Field Core Secondary receives the warning and, after reading the flow's occupancy afresh, compacts it or restarts it (read).

Flow itself does not yet refresh, lock the metaflow, or reap the predecessor: no such operation is in its source (read).

### Compaction

Compaction is done today by hand and by Field after the warning. The guarded request you asked for, refused when the flow is small or young, is not found in the hook or in Flow (read). Whether Mind Core Primary has it in progress is unknown.

### Spin-down and reactivation

Flow's metaflow can be asleep (read). No operation puts a flow to sleep or wakes one (read). Spin-down today is a closed pane; reactivation is a fresh launch from the same EDN (inference).

### Implemented and assumed

| part | state |
|---|---|
| EDN launch files | in use, uncommitted |
| refresh warning hook | in use, uncommitted |
| metaflow and queue types | in Flow source |
| launch operations | in Flow source |
| waking, draining | unproven (Mind) |
| guarded compaction | not found |
| sleep, wake | type only |
| refresh in Flow | not found |

### Addressing

The send command is to take the metaflow's three-field address now; the flow id is resolved at runtime (not yet witnessed).

### Ordered, not started

Ordered: measure, from past flows, when a predefined subflow costs fewer tokens than calling tools directly (not started, as far as read). (d68c82 flow, «Lean flows, cheap to start».)

## 2 Long term

```
+--------------------------------------------+
| you, a flow, a hook                        |
+--------------------------------------------+
        | send a request
        v
+--------------------------------------------+
| Message Nexus                              |
+--------------------------------------------+
        | asks Flow: deliver to
        | { Aspect topic Layer }
        v
+--------------------------------------------+
| Flow Nexus, holding the lock               |
+--------------------------------------------+
  |                           |
  | answers: sent             | composes the
  | or queued                 | prompt from the
  v                           | registry, hash
+--------------------+        | checked
| Message Nexus,     |        |
| subscribed to its  |        |
| events             |        |
+--------------------+        v
+--------------------------------------------+
| a flow, in its Capsule                     |
+--------------------------------------------+
        | hooks call the Flow CLI;
        | at the threshold: handover, lock
        v
+--------------------------------------------+
| the successor flow; predecessor            |
| reaped in the same event                   |
+--------------------------------------------+
        | work done:
        | spun down
        v
+--------------------------------------------+
| topic idle; a small model judges           |
| when to wake it                            |
+--------------------------------------------+
```

The long term is the nexuses, used everywhere. Every component is a Nexus: Signal is what it says, Operation what it does, Memory what it remembers, its own store, an ordinary socket and a meta socket, pure signal on the wire, state observed by subscription, no polling (vision-nexus).

Flow is the first nexus to make whole. It launches, names, delivers to, refreshes and reaps flows; it knows each caller by its process, so no flow declares its id (vision-flow). Message asks Flow to deliver and learns from Flow's events when a request entered a flow's context (vision-flow).

Configuration lives in Flow's Memory and changes only over its meta socket.

## 3 From short term to long term

```
+--------------------------------------------+
| EDN launch files                           |
+--------------------------------------------+
        | are sent as datom payloads
        | on the meta socket
        v
+--------------------------------------------+
| Flow's configuration, in its Memory        |
+--------------------------------------------+
  - - - - - - - - - - - - - - - - - - - - - -
+--------------------------------------------+
| launcher scripts                           |
+--------------------------------------------+
        | are replaced by
        v
+--------------------------------------------+
| Launch on Flow's socket                    |
+--------------------------------------------+
  - - - - - - - - - - - - - - - - - - - - - -
+--------------------------------------------+
| hook warns Field; Field compacts or        |
| restarts                                   |
+--------------------------------------------+
        | are replaced by
        v
+--------------------------------------------+
| Flow refreshes, locks, reaps,              |
| in one event                               |
+--------------------------------------------+
  - - - - - - - - - - - - - - - - - - - - - -
+--------------------------------------------+
| closed pane, fresh launch                  |
+--------------------------------------------+
        | are replaced by
        v
+--------------------------------------------+
| Flow puts the metaflow asleep and          |
| wakes it                                   |
+--------------------------------------------+
```

Short term: Flow is started by sending its configuration files, one after another, as datom payloads on its meta socket (your records of 9 October, 445410 nexus).

When each long-term part runs and is documented, its short-term part and its documentation are removed (intent-psyche). For Flow that removes, in my reading (inference):

- the EDN launch files and the launcher scripts that read them;
- the refresh hook and its warning to Field (d4ae97 flow, 7 Oct);
- Field's hand compaction and restarts;
- the guarded compaction request.

## 4 Questions for the living

1. The compaction guard. A compaction request is refused when the flow's context is below a size or the flow is younger than an age. Is each limit one value for all flows, or set per layer?

2. The EDN files. Do they stay as the authored source, sent to Flow as Configure payloads on its meta socket, or are they rewritten as datom files when Flow takes over launching?

3. Spin-down. Who decides a specialized flow's work is done and spins it down: the flow itself, the flow that asked for it, or Flow when the flow has been idle?

4. Lean. A Psyche seat now starts with nineteen context modules. Which ones does every flow carry whatever its topic, so the rest come only with a topic?

5. Waking. Until Flow runs, who wakes an idle topic when new input arrives: a small model, or the Secondary that receives the input?

## Crystallization

All five land in psyche-context `skills/vision-flow.md`. Proposal 2 replaces one line; the others remove none.

### Proposal 1: the EDN launch, short term

Rests on d68c82 flow (13 October, 17:47).

Above, «Starting flows», as it stands: A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.

Added after it:

Short term: flow starting is configured in EDN files, one per aspect and one per metaflow holding what differs; from them the launcher finds each context module and whether it goes in the system prompt or the user prompt.

Below, as it stands: Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect.

Ruling: land, change, or drop.

### Proposal 2: lean, specialized flows

Rests on d68c82 flow, «Clean specialized flows» and «Lean flows, cheap to start» (13 October).

In «What it does», this line is replaced.

REMOVE:

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

ADD in its place:

Starting a specialized flow is cheap: it carries only the context modules and tools its purpose needs, so its output is of higher quality; when its work is done it is spun down, and waking its topic starts a new flow with a clean context.

Below, as it stands: A topic's name is a camelCase identifier, uncapitalized.

Ruling: land, change, or drop.

### Proposal 3: the refresh warning, short term

Rests on d68c82 flow, «The refresh procedure starts at a threshold» (13 October).

Above, as it stands: A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.

Added after it:

Short term: a hook warns at a threshold, two hundred thousand tokens on Claude. The flow is told the refresh procedure has started; it writes its handover and names what of its context should go to existing or new topic flows. Field recompacts or restarts it.

Ruling: land, change, or drop.

### Proposal 4: the handover carries judgment

Rests on d68c82 handover (13 October, 16:20).

Added after Proposal 3's line:

A handover carries only what needs judgment; what a tool returns in one call, such as which revision was pushed or the order of events, is left for the successor to look up.

Below, as it stands: «Subflows replace the harness subagent facility».

Ruling: land, change, or drop.

### Proposal 5: guarded compaction, short term

Rests on 33752b flow and d68c82 flow (13 October). The long-term direction behind it: 6cc91b flowLifecycle, «No compaction: re-bootstrap on a fresh flow» (14 September).

Added after Proposal 4's line:

Short term: a flow or a metaflow is compacted on request. The request is refused when the flow's context is under a threshold or the flow is younger than a set age, so it never lands on a flow just started. A compacted flow still carries noise.

Ruling: land, change, or drop.
<!-- to-the-living:end -->
