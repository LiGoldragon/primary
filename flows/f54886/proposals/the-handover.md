Presentation.{ «The handover» }

# The handover

*Created by Fable.*

A handover is a broad overview of what the flow is still trying to do, and only that. The Flow Nexus warns a flow before its threshold so it can write one; the successor starts from that file and a fresh point of view. Lands without his review, on his word; the Warning is for the version after 0.48.

### Proposal 1: A handover is an overview · psyche-belief › vision/remembering.md

**Comment** One paragraph replaced: the handover as a book, its composition by ancestor and its review go; the overview and the warning take their place. The logs still pass, and the module now says why.

- A flow is refreshed after its landings: what he approved is landed and live before the handover is written, and the handover holds only what is not landed. The flow that had the conversation writes it, in his words verbatim, composed in inline quotes into what he wants and nothing else, by ancestor, each section marked with the model and the process that made it. It is published as a book of its own kind, `Handover.{ «title» }`, which he reviews as he reviews psyche; the successor's first prompt is that file as reviewed.
+ A flow is refreshed after its landings: what he approved is landed and live before the handover is written. A handover is a broad overview of what the flow is still trying to do, and only that: the successor starts with a fresh point of view. The raw logs pass to a flow so that it may write its handover; the Psyche core Primary, the flow that speaks with the living, is their main user. The flow writes the handover at flows/<id>/handover.md when the Flow Nexus warns it, and the successor's first prompt is that file.

+ ```mermaid
+ flowchart TB
+     n["Flow Nexus"] -- "warns, before the threshold" --> f["the flow"]
+     f -- "writes" --> h["handover: what it is still trying to do"]
+     h -- "first prompt of" --> s["the successor, fresh"]
+ ```

### Proposal 2: The Nexus warns before the threshold · psyche-belief › vision/flow-nexus-v1.md

**Comment** The refresh paragraph gains the warning; Event gains Warned; Threshold carries the share at which the warning is sent.

- A perma flow is refreshed when its context passes its model's threshold, configured per model in the Flow Nexus: the flow is told to write its handover, its successor is launched with the same definition, the handover as its first prompt, and the queue that gathered meanwhile; the predecessor ends. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.
+ A perma flow is warned when its context reaches the Warning share of its model's threshold, configured per model in the Flow Nexus: a HardAbrupt Notice naming its handover path, flows/<id>/handover.md. When the context passes the threshold its successor is launched with the same definition, that file as its first prompt, and the queue that gathered meanwhile; the predecessor ends. An absent file means the successor starts from its definition and the queue alone. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.

```ethos
  [ Event.[ Started Idle Working Ended
            Responded.String            ; the response, whole
-           Threshold ] ]              ;   context past its mark
+           Warned                     ;   the handover asked
+           Threshold ] ]              ;   context past its mark
```

```ethos
-   Threshold.{ Model.String Tokens.Integer }
+   Threshold.{ Model.String Tokens.Integer
+               Warning.Integer }        ; share left, 20
```

```datom
+ ; the Nexus, to the flow, at the Warning share
+ HardAbrupt.Notice.«Write your handover at
+ flows/f54886/handover.md»
```

### Proposal 3: A proposal is Fable's · psyche-belief › vision/proposal.md

**Comment** The modules give a Secondary a proposals directory and a role that writes them, and no line says whose a proposal is; a book went up written by Opus and signed Fable. The line that says whose it is, by the model's name: the models have personality, and the configuration shows the model.

  ## A proposal is signed

+ A proposal is written by Fable; Opus publishes it and lands it.
