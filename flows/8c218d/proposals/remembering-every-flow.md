Presentation.{ «Remembering reaches every flow» Proposal }

# Remembering reaches every flow

Created by Fable 5.2; a worker assembled the page.

## psyche-belief › vision/remembering.md

## All flows are one subjectivity

All flows are one subjectivity; this is the reason behind
remembering. Told "you did" or "you said" of a thing it did not
itself do or say, a flow remembers it at a depth fit to the question,
reaching the transcript directly.

## A fresh flow receives his content weighed by importance

A fresh flow receives the living's content weighed by importance, and only the important part.

His comments on a book reach the flow that redoes it as a user message through the Flow Nexus, in his words, the book named by its title; a fresh flow's first prompt carries his open comments on the books its predecessors published.

```mermaid
flowchart TB
    a["living content"] -- "weighed by importance" --> b["important part"]
    a -- "the rest stays in" --> c["the transcript"]
    b -- "passes to" --> d["fresh flow"]
```

A flow is refreshed after its landings: what he approved is landed and live before the handover is written. A handover is a broad overview of what the flow is still trying to do, and only that: the flow's judgment, what a successor could get by no look-up. A revision landed, a file's path, the state of a build or a queue is what one command returns in a handful of tokens, and the successor fetches it; the handover's words are spent on inference alone. The successor starts with a fresh point of view. The flow writes the handover at `flows/<id>/handover.md` when the Flow Nexus warns it, and the successor's first prompt is that file.

```mermaid
flowchart TB
    n["Flow Nexus"] -- "warns, before the threshold" --> f["the flow"]
    f -- "writes" --> h["handover: its judgment on what it is still trying to do"]
    h -- "first prompt of" --> s["the successor, fresh"]
```

### Proposal 1: Remembering reaches every flow · psyche-belief › vision/remembering.md

::: comment
His words, 10 November: «all of the flows being one entity conceptually. This means that remembering doesn't just imply the depth of a certain permaflow, but also the depth of any permaflow. So that essentially remembering can entail talking to other flows.» The module today has a flow remember down its own line of predecessors, by reading a transcript. This adds the other direction, across, and the second way, asking.
:::

::: shown
psyche-belief › vision/remembering.md
All flows are one subjectivity; this is the reason behind
remembering. Told "you did" or "you said" of a thing it did not
itself do or say, a flow remembers it at a depth fit to the question,
reaching the transcript directly.
:::

+ Remembering reaches every permaflow, at any depth, as it reaches the flow's own: what a flow did not itself do or say may be in the past of any of them. A flow remembers by reading that transcript, or by asking the flow that holds it.

```datom
+ ; remembering by asking: a Question to the flow that holds it
+ Send.{ { Mind flowNexus Opus } Soft.Question.«Why did 0.54.0 refresh no flow?» }
```

```mermaid
+ flowchart TB
+     f["a flow, told of a thing it did not itself do"] -- "remembers down" --> o["its own predecessors, at a depth"]
+     f -- "remembers across" --> a["any other permaflow, at a depth"]
+     a -- "by reading" --> t["that flow's transcript"]
+     a -- "by asking" --> r["the running flow that holds it"]
```
