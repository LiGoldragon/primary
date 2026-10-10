<!-- to-the-living:start -->
Presentation.{ «Flow, a passable vision» }

All proposals change `psyche-skills/skills/vision-flow.md`. The two proposals on its lines 12 and 22 in the books before this one are replaced by proposals 1 and 2 here.

## 1. Lines 8–14, section «What it does»

Lines removed:

```
The Flow Nexus sets up and starts a model flow: its
working directory, system prompt, training files and
instruction prompt. It takes the place of the
abandoned training daemon.

Flow is the Nexus that manages flows. A flow is one
run of a voice; the component is named for what it
manages. A flow the living asks for is launched,
properly and surely. Flow holds the lock on flows.

The Capsule is the component that makes where a flow
runs. Its first embodiment is the semi-sandbox: ...
```

Lines added, the Capsule paragraph kept as it is:

```
Flow is the Nexus that manages metaflows. A metaflow
is a chain of flows, each the ancestor of the next;
it is what is spoken to, thought about, woken,
refreshed and ended. A flow is one run of a model:
launched, filled, refreshed into its successor; it
is low-level and almost never user-facing. Flow's
registry holds, for each metaflow, its current flow,
the one that receives, and the chain behind it.

A metaflow is of one of four kinds. Psyche, Mind and
Field metaflows are voices: permanent, never ended;
a voice may sleep, and a request meant for it wakes
it, spawning its next flow with the context modules
the request calls for. An implementation metaflow is
a job of its own, one per implementation, and ends
when the job is done. Each metaflow has a layer,
Primary, Secondary, Tertiary or Quaternary, and the
layer decides the model.

A flow the living asks for is launched, properly and
surely.
```

Ruling 1: yes, or amend.

## 2. Line 22, section «Starting flows»

Line removed:

```
A voice is an aspect carrying a rank,
`Psyche.Primary`: Psyche, Mind, Field by Primary,
Secondary, Tertiary, nine voices. The model behind a
voice is configuration, declared once in Flow and
changed only over its meta wire; not every model is
exposed to every voice. Voices are addressed by
name; a flow id is for the ledger and the archive,
and is written in words. A side flow is a job, not a
voice: focused, not long-lived, gone when its
mission is done; a message sent to it after that
returns to its sender with notice that the flow has
ended.
```

Lines added:

```
A voice is an aspect carrying a layer,
`Voice.{ Psyche Primary }`. The model behind a layer
is configuration, declared once in Flow and changed
only over its meta wire; not every model is exposed
to every layer. Metaflows are addressed by name; a
flow id is for the ledger and the archive, and is
written in words. A thread's title names the
metaflow and the flow's words, never the model. A
request to an implementation that has ended returns
to its sender with notice that it has ended.
```

Ruling 2: yes, or amend.

## 3. Line 46, section «A replaced session is reaped by the refresh itself»

Line removed:

```
Every harness event reaches Flow through the
harness's hooks calling the Flow CLI, so Flow knows
each flow's state without polling; a marked block
landing in a transcript becomes an action, a book
among them, with no tool call by the flow; a flow
nearing its context limit is told, writes its
handover, and is refreshed as it goes idle. Polling
is forbidden; a poller that must exist is registered
and reported.
```

Lines added:

```
Every harness event reaches Flow through the
harness's hooks calling the Flow CLI, so Flow knows
each flow's state without polling; a marked block
landing in a transcript becomes an action, a book
among them, with no tool call by the flow. The hook
reports the flow's context at each stop. Between 20
and 40 percent of the model's window the flow is
told to write its handover; then Flow composes the
next link of the chain from the metaflow's context
modules and the handover as its brief, spawns it,
and reaps the predecessor. Only what is still
undecided passes in the handover; what was decided
went into context modules. No model decides any of
this. Polling is forbidden; a poller that must exist
is registered and reported.
```

Ruling 3: yes, or amend.

## 4. After line 46, new section

Lines removed: none. Lines added:

```
## Context modules make the flow

A flow starts from a brief of a small paragraph;
ninety-five percent or more of its context comes
from context modules, named at launch. Naming a
module loads its dependency chain, so a few names
call a whole context, at a leverage of a hundred to
a thousand to one between what the caller writes and
what the flow receives. A module is placed in the
system prompt, in the first prompt, or left
loadable; Flow keeps the registry of modules and
composes the launch from it, never from paths a
caller writes by hand.
```

Ruling 4: yes, or amend.

## 5. After proposal 4, new section

Lines removed: none. Lines added:

```
## Requests and the lock

What reaches a flow is a typed request, never a
letter; each kind of request has its own behavior
on arrival. Flow holds no messages. Before Message
sends, it asks Flow for a lock on the metaflow,
bounded in time; with the lock, it hands Flow the
request, and Flow places it in the current flow.
Message speaks in metaflows and need not know flows.
```

Ruling 5: yes, or amend.

## 6. Section «Sources», after line 85

Lines removed: none. Lines added:

```
d4ae97 flow
d4ae97 contextModules
f5a6e9 flow
bad807 metaflow
e5a0bc flow
```

Ruling 6: yes, or amend.
<!-- to-the-living:end -->
