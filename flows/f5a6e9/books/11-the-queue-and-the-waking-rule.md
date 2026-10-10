<!-- to-the-living:start -->
Presentation.{ «The queue and the waking rule» }

## 1. `signal-flow/ethos/signal.ethos`, after line 220 (the `Event` type)

Lines removed: none. Lines added:

```
Request.[                 ; what reaches a flow
   Order.String           ; from the living or the
                          ; psyche: wakes
   Question.String        ; wakes
   Result.String          ; a flow's answer:
                          ; delivered awake, waits
                          ; asleep
   Notice.String ]        ; a merge, thanks: never
                          ; wakes
```

Delivered, at the end of the prompt, as one vector, oldest first, the waking request last:

```
[  Notice.«branch flowRefresh merged»
   Result.«tests pass on 0.25.0»
   Order.«bring the refresh to production» ]
```

Ruling 1: (a) these four kinds. (b) your kinds.

## 2. `flow/crates/flow-nexus/ethos/memory.ethos`, the `Metaflow` record of «The metaflow record», second edition

Line removed:

```
      Past.Vector<FlowId> }      ; oldest first
```

Lines added:

```
      Past.Vector<FlowId>        ; oldest first
      Queue.Vector<Request> }    ; waiting, oldest
                                 ; first
```

Ruling 2: yes, or amend.

## 3. `psyche-skills/skills/vision-messaging.md`, after line 33

Lines removed: none. Lines added:

```
## The queue and the waking rule

Every topic has its own metaflow, in charge of the
whole topic. A request to it has an effect that
depends on the metaflow's state. Awake: the request
is delivered now. Asleep: an order or a question
wakes it, a result or a notice waits in its queue
and wakes nothing. Ended: the request returns to
its sender. A waking request drains the queue: all
waiting requests are delivered in the order
received, oldest first, as one vector typed by
variant at the end of the prompt, the waking
request last. A metaflow satisfied with its topic
sleeps until a request changes what it must do.
```

Ruling 3: yes, or amend.

## 4. `psyche-skills/skills/vision-flow.md`, after the section «Requests and the lock» of «Flow, a passable vision»

Lines removed: none. Lines added:

```
Every topic has its own metaflow; a topic may span
several skills, and that metaflow answers for the
whole of it. Flow keeps each metaflow's queue and
applies the waking rule: it spawns the sleeping
metaflow's next flow only for a request that wakes,
and hands the drained queue to that flow as the
end of its first prompt.
```

Ruling 4: yes, or amend.
<!-- to-the-living:end -->
