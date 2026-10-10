<!-- to-the-living:start -->
Presentation.{ «The metaflow record», second edition }

## 1. `flow/crates/flow-nexus/ethos/memory.ethos`, new file

Lines removed: none. Lines added, the whole file:

```
Memory
[  signal_flow:[ FlowId FlowAspect Event ] ]
[  Metaflow.{
      Name.[
         Voice.{                 ; permanent
            FlowAspect
            Layer.[
               Primary
               Secondary
               Tertiary
               Quaternary ] }
         Goal.String ]           ; camelCase; ends
      State.[
         Awake.FlowId            ; its current flow
         Asleep                  ; a request wakes it
         Ended ]
      Past.Vector<FlowId> }      ; oldest first
   Flow.{                        ; one per run
      FlowId
      Session.String             ; the harness's id
      Events.Vector<Event> } ]
```

Ruling 1: yes, or amend.

## 2. `psyche-skills/skills/vision-flow.md`, line 12

Line removed:

```
Flow is the Nexus that manages flows. A flow is one
run of a voice; the component is named for what it
manages. A flow the living asks for is launched,
properly and surely. Flow holds the lock on flows.
```

Lines added:

```
Flow is the Nexus that manages metaflows and the
flows that run them. The metaflow is the major
abstraction, the one spoken to and thought about;
a flow is one run, lower-level, almost never
user-facing. A voice is a permanent metaflow: it
may sleep, and a request meant for it wakes it,
spawning its flow with the right context modules.
A goal is a metaflow that ends when its goal is
met. A metaflow's memory holds its current flow and
its predecessors; a flow holds nothing of this. A
flow the living asks for is launched, properly and
surely. Flow holds the lock on metaflows.
```

Ruling 2: yes, or amend.

## 3. `psyche-skills/skills/vision-flow.md`, line 22, last sentence

Line removed:

```
A side flow is a job, not a voice: focused, not
long-lived, gone when its mission is done; a
message sent to it after that returns to its
sender with notice that the flow has ended.
```

Line added:

```
A goal is a metaflow that is not a voice: it ends
when its goal is met, and a request sent to it
after that returns to its sender with notice that
it has ended.
```

Ruling 3: yes, or amend.

## 4. `psyche-skills/skills/vision-messaging.md`, after line 33

Lines removed: none. Lines added:

```
## A request to a metaflow is typed; Message asks
## Flow for a time-bound lock

What is sent to a flow is a typed request, never a
letter; each request has its own behavior on
arrival, and a refresh request reaching a fresh
flow does nothing. Message addresses metaflows and
need not know flows. Before sending, Message asks
Flow for a lock on the metaflow, bounded in time;
with the lock it hands Flow the request, and Flow
places it. Flow holds no messages.
```

Ruling 4: yes, or amend.

## 5. `psyche-skills/skills/vision-ethos.md`, section Spacing, after line 439

Lines removed: none. Line added:

```
Indentation is three spaces per level.
```

Ruling 5: yes, or amend.
<!-- to-the-living:end -->
