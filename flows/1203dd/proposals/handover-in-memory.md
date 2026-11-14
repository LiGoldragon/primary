Presentation.{ «The handover lives in the Flow Nexus» Proposal }
# The handover lives in the Flow Nexus

Created by Fable 5.1, who wrote this from his design of Nov 5 and 6 and his comments of Nov 6; a Sonnet found his words.

### Proposal 1: The handover · psyche-belief › vision/flow-nexus.md

**Comment** A new section after "What a refresh carries".

+ ## The handover lives in the Flow Nexus
+
+ A permaflow's handover is a record in the Flow Nexus's Memory, kept under the address through the permaflow's flows and archived past a configured count. It is a vector of sections, each a title, a short description and a body. Any flow may read another's handover.
+
+ ```mermaid
+ flowchart TB
+     f["the flow"]
+     m["Memory: the permaflow's handover,
+         a vector of sections"]
+     o["any flow"]
+     f -- "Keep: a section added,
+         or replaced by its title" --> m
+     f -- "Drop: a section removed
+         by its title" --> m
+     o -- "Glance: titles and
+         descriptions" --> m
+     o -- "Read: the whole, bodies included" --> m
+ ```
+
+ The refresh window is the share of a flow's context from the warning share to its threshold. The Nexus marks when the handover was last touched and at what context; a handover touched inside the refresh window is the flow's green light, and the Nexus refreshes the flow at its threshold. A handover untouched in the window holds the refresh, and the Nexus reminds the flow at a configured interval.
+
+ ```mermaid
+ flowchart TB
+     n["Flow Nexus"]
+     f["the flow"]
+     s["the successor"]
+     n -- "handover untouched in the refresh
+         window: reminds, every
+         configured interval" --> f
+     f -- "Keep or Drop inside the window:
+         the green light" --> n
+     n -- "at the threshold, refreshes" --> s
+     n -- "composes the first prompt: belief
+         modules, then the handover last"
+         --> s
+ ```
+
+ The successor's first prompt holds the belief modules first and the handover last, so the vision frames the handover and the handover is what the successor acts on first.
+
+ ```mermaid
+ flowchart TB
+     m["Memory: a permaflow's handovers"]
+     a["the archive repository:
+         one file per flow"]
+     m -- "more than the configured count" --> a
+     a -- "leaves" --> m
+ ```
+
+ ```ethos
+ Library
+ ; as they stand in vision:flow-nexus:
+ ; Address.{ Aspect Topic Model }, FlowId.String
+ [ flow:[ Address FlowId ] ]
+ [ Title.String
+   Heading.{ Title Description.String }
+   Section.{ Title Description.String Body.String }
+   ; tokens in a flow's context
+   Context.Integer
+   ; a percentage of the threshold
+   Share.Integer
+   Minutes.Integer ]
+ []
+ []
+ ```
+
+ ```ethos
+ Signal
+ [ handover:[ Address FlowId Title
+             Heading Section ] ]
+ ; a section added, or replaced by its title
+ [ Keep.{ Address Section }
+   ; a section removed
+   Drop.{ Address Title }
+   ; titles and descriptions
+   Glance.Address
+   ; the whole, bodies included
+   Read.Address ]
+ [ Kept.{ Address Title }
+   Dropped.{ Address Title }
+   Glanced.Vector<Heading>
+   Handover.Vector<Section> ]
+ []
+ ```
+
+ ```ethos
+ Memory
+ [ handover:[ Address Section Context
+             Share Minutes ] ]
+ [ ; one per permaflow; Context: the tokens
+   ; when last kept
+   Handover.{ Address Vector<Section>
+              Touched.Option<Context> }
+   Threshold.{ Model.String Tokens.Integer
+               ; the share left at which the
+               ; reminder begins
+               Warning.Share
+               ; what the reminder says
+               Message.String
+               ; how often it repeats until the
+               ; handover is current
+               Every.Minutes }
+   ; how many handovers a permaflow keeps in
+   ; Memory before the oldest is archived
+   HandoverCount.Integer ]
+ ```
+
+ ```datom
+ Keep.{ { Psyche core Fable }
+        { «0.53.1»
+          «In build; deploys 19:30 his time»
+          «Hold versionZero to its hour.» } }
+ Kept.{ { Psyche core Fable } «0.53.1» }
+ Glance.{ Psyche core Fable }
+ Glanced.[ { «0.53.1»
+             «In build; deploys 19:30 his time» } ]
+ HardAbrupt.Notice.«Your context is at 85%;
+ bring your handover current.»
+ Configure.Threshold.{ claude-fable-5-1 280000 15
+   «Your context is at 85%; bring your handover
+   current.» 10 }
+ Configure.HandoverCount.3
+ ```

### Proposal 2: The handover · psyche-belief › vision/remembering.md

**Comment** The file sentence and its figure go; the paragraph points to vision:flow-nexus.

- The flow writes the handover at flows/<id>/handover.md when the Flow Nexus warns it, and the successor's first prompt is that file.
+ The handover is the permaflow's record in the Flow Nexus, kept section by section as the flow goes, and the successor's first prompt ends with it.

- ```mermaid
- flowchart TB
-     n["Flow Nexus"] -- "warns, before the threshold" --> f["the flow"]
-     f -- "writes" --> h["handover: its judgment on what it is still trying to do"]
-     h -- "first prompt of" --> s["the successor, fresh"]
- ```

### Proposal 3: The file lines · psyche-belief › vision/flow-nexus-v1.md

**Comment** Under "A permanent flow continues", the file path and the absent-file case go; the Notice example goes; "finds its handover path" goes.

- It is warned when its context reaches the Warning share of its model's threshold, configured per model in the Flow Nexus: a HardAbrupt Notice naming its handover path, flows/<id>/handover.md. When the context passes the threshold its successor is launched with the same definition, that file as its first prompt, and the queue that gathered meanwhile; the predecessor ends. An absent file means the successor starts from its definition and the queue alone.
+ It is reminded while its context is inside its refresh window and its handover untouched there, the window configured per model in the Flow Nexus; at its threshold, its handover touched in the window, its successor is launched with the same definition, the handover ending its first prompt, and the queue that gathered meanwhile; the predecessor ends.

- ```datom
- ; the Nexus, to the flow, at the Warning share
- HardAbrupt.Notice.«Write your handover at
- flows/f54886/handover.md»
- ```
+ ```datom
+ ; the Nexus, to the flow, at the Warning share
+ HardAbrupt.Notice.«Your context is at 85%;
+ bring your handover current.»
+ ```

- A flow knows itself at launch: its Identity, the name of the complex it runs in, its Address and its FlowId, is composed into its first prompt or its system prompt, so it names itself in Send and Report, finds its handover path, and knows which being it is part of; the Roster is composed into the first prompt beside it.
+ A flow knows itself at launch: its Identity, the name of the complex it runs in, its Address and its FlowId, is composed into its first prompt or its system prompt, so it names itself in Send, Report and Keep, and knows which being it is part of; the Roster is composed into the first prompt beside it.

### Proposal 4: The flow directory · psyche-belief › intent/scratch.md

**Comment** The handover leaves the list of what the flow directory holds.

- The primary workspace and the flow directory hold only what is landed or what the living reads, a proposal or a handover.
+ The primary workspace and the flow directory hold only what is landed or what the living reads, a proposal among it.
