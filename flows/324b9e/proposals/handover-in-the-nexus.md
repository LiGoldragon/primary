Presentation.{ «The handover lives in the Nexus» }

# The handover lives in the Nexus

Created by Fable, from his design of 2026-11-05: a flow is told, at a configurable share of its context and in a configurable message, to update its handover; the handover is a record in the Flow Nexus's Memory, a vector of sections each with a title, a short description and a body, so a flow gets a glance of it without reading the whole, adds or drops a section atomically, and any flow reads it; the Nexus marks when it was last updated and at what context, and refreshes a flow only once its handover is current, reminding it until then; the handover file in the repository goes. It stacks on the book Flow Nexus version 1.

### Proposal 1: The handover is a standing record of the permaflow · psyche-belief › vision/flow-nexus.md

**Comment** The concept, in the perennial module, after "What a refresh carries".

  ## What a refresh carries

  A refresh carries the flow's important presentations and illustrations, the raw psyche given to it, and the basic skills. The basic skills are everything a flow needs.

+ ## The handover lives in the Nexus
+
+ A permaflow's handover is a record in the Flow Nexus's Memory, kept under the address and outliving every flow of it: what the permaflow is still trying to do, as sections, each a title, a short description and a body. A flow keeps it as it goes, adding or dropping one section at a time; its successor inherits it and goes on editing it; any flow reads it, the titles and descriptions for a glance, a section's body when it needs it. The Nexus marks when the handover was last touched and how much context the flow had then, and refreshes a flow only once its handover is current, reminding it until then at a configured share of its context, in a configured message. Nothing of the handover is a file.
+
+ ```mermaid
+ flowchart TB
+     f["the flow"] -- "keeps, one section at a time" --> h["the handover: sections, in the Nexus's Memory, under the address"]
+     n["the Flow Nexus"] -- "reminds, at a configured share, in a configured message" --> f
+     n -- "refreshes, once the handover is current" --> s["the successor"]
+     h -- "inherited by" --> s
+     o["any flow"] -- "reads the glance: titles and descriptions" --> h
+ ```

### Proposal 2: The handover file goes · psyche-belief › vision/remembering.md

**Comment** The file and its figure leave; the successor's first prompt is the handover read from the Nexus.

- A flow is refreshed after its landings: what he approved is landed and live before the handover is written. A handover is a broad overview of what the flow is still trying to do, and only that: the flow's judgment, what a successor could get by no look-up. A revision landed, a file's path, the state of a build or a queue is what one command returns in a handful of tokens, and the successor fetches it; the handover's words are spent on inference alone. The successor starts with a fresh point of view. The raw logs pass to a flow so that it may write its handover; the Psyche core Fable, the flow that speaks with the living, is their main user. [-The flow writes the handover at flows/<id>/handover.md when the Flow Nexus warns it, and the successor's first prompt is that file.-]
+ A flow is refreshed after its landings: what he approved is landed and live before the handover is written. A handover is a broad overview of what the flow is still trying to do, and only that: the flow's judgment, what a successor could get by no look-up. A revision landed, a file's path, the state of a build or a queue is what one command returns in a handful of tokens, and the successor fetches it; the handover's words are spent on inference alone. The successor starts with a fresh point of view. The raw logs pass to a flow so that it may write its handover; the Psyche core Fable, the flow that speaks with the living, is their main user. [+The handover is the permaflow's record in the Flow Nexus, kept section by section as the flow goes, and the successor's first prompt is that record, read from the Nexus.+]

- ```mermaid
- flowchart TB
-     n["Flow Nexus"] -- "warns, before the threshold" --> f["the flow"]
-     f -- "writes" --> h["handover: its judgment on what it is still trying to do"]
-     h -- "first prompt of" --> s["the successor, fresh"]
- ```

### Proposal 3: The handover in version 1 · psyche-belief › vision/flow-nexus-v1.md

**Comment** The types. A section is kept or dropped by title, atomically; the glance is the record without bodies; the threshold carries, per model, the share at which the reminder starts, its message and its interval, and the window within which an update counts as current. The hard mark is tentative, pending his word: a share past which the refresh goes regardless.

  ## A permanent flow continues

- A permanent flow continues through runs under its address and is kept hot: it is not stopped between works, so no restart pays the full cost of starting again. It is warned when its context reaches the Warning share of its model's threshold, configured per model in the Flow Nexus: a HardAbrupt Notice naming its handover path, flows/<id>/handover.md. When the context passes the threshold its successor is launched with the same definition, that file as its first prompt, and the queue that gathered meanwhile; the predecessor ends. An absent file means the successor starts from its definition and the queue alone. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.
+ A permanent flow continues through runs under its address and is kept hot: it is not stopped between works, so no restart pays the full cost of starting again. From the Warning share of its model's threshold, configured per model in the Flow Nexus, it is reminded in the configured message, at the configured interval, until its handover is current: touched since its context entered the Window share below the threshold. When the context passes the threshold and the handover is current, its successor is launched with the same definition, the handover read from Memory as its first prompt, and the queue that gathered meanwhile; the predecessor ends. A handover not current holds the refresh and the reminders go on. An empty handover means the successor starts from its definition and the queue alone. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.

  ## Signal

```ethos
  [ Define.[ Metaflow Harness Complex ] ; add or replace one
+   Keep.{ Address Section }           ; the handover: a section added, or replaced by title
+   Drop.{ Address Title }             ;   a section removed
+   Glance.Address                     ;   titles and descriptions
+   Handover.Address                   ;   the whole, bodies included
```

```ethos
  [ Defined.Name
+   Kept.{ Address Title }
+   Dropped.{ Address Title }
+   Glanced.Vector<Heading>
+   Handover.Vector<Section>
```

```ethos
    Event.[ Started Idle Working Ended
            Responded.String            ; the response, whole
-           Warned                     ;   the handover asked
+           Reminded                   ;   the handover asked, in the configured message
            Threshold ] ]              ;   context past its mark
```

```datom
- ; the Nexus, to the flow, at the Warning share
- HardAbrupt.Notice.«Write your handover at
- flows/f54886/handover.md»
+ ; the flow, keeping one section
+ Keep.{ { designer fable }
+        { «The version 1 book»
+          «Published; he has not ruled»
+          «Eight proposals, each module whole. His word today removed the Fable gate; the source is current. Nothing lands until he rules.» } }
+ Kept.{ { designer fable } «The version 1 book» }
+ ; any flow, the glance
+ Glance.{ designer fable }
+ Glanced.[ { «The version 1 book» «Published; he has not ruled» }
+           { «The refresh fault» «With Mind; hooks reach 0.44» } ]
+ ; the Nexus, to the flow, from the Warning share, every Every minutes
+ HardAbrupt.Notice.«Your context is at 85%; keep your handover current.»
```

  ## Memory

```ethos
    Queue.{ Address Vector<Message> }
+   Handover.{ Address Vector<Section>  ; one per permaflow, outliving its flows
+              Touched.Option<Context> } ; the context the flow had at its last Keep or Drop
    Threshold.{ Model.String Tokens.Integer
-               Warning.Integer }        ; share left, 20
+               Warning.Share            ; where the reminders start, 15
+               Message.String           ; the reminder, as the flow reads it
+               Every.Minutes            ; the reminder's interval
+               Window.Share             ; a Keep inside it makes the handover current
+               Hard.Option<Share> }     ; tentative: past it, the refresh goes regardless
+   Title.String
+   Heading.{ Title Description.String }   ; the glance
+   Section.{ Title Description.String Body.String }
+   Context.Integer                      ; tokens
+   Share.Integer                        ; a percentage of the threshold
+   Minutes.Integer
```

```datom
+ Configure.Threshold.{ claude-fable-5-1 800000
+                       15 «Your context is at 85%; keep your handover current.»
+                       10 15 None }
```
