Presentation.{ «The translator» }

# The translator

Created by Fable. Redoes the book of 2026-10-30 (0568e3) and the first of today: his comments folded in, one proposal.

### Proposal 1: The translator · psyche-belief › vision/translator.md, a new file

**Comment** The translator is the text-handling of the CLI broken out into a component every Nexus can use. It is not a Nexus: no domain, no Memory. The translator makes the system call, so a Nexus never types `herdr`; the CLI is a shim that sends its argument to the translator and waits for the reply.

+ ## What the translator is
+
+ The translator is the component that carries data
+ between datom text and signal, both ways. It holds
+ the codec; a Nexus holds none. Several Nexuses and
+ the CLI share one translator, built against their
+ contracts; a new set of contracts is a new translator,
+ named apart by a random suffix.
+
+ ```mermaid
+ flowchart TB
+     cli["CLI: one datom argument"]
+       -- "sends to the datom socket" --> t["translator"]
+     t -- "composes, sends signal" --> n["Nexus"]
+     n -- "answers in signal" --> t
+     t -- "textualizes the answer" --> cli
+     n -- "emits a typed output to the signal socket"
+       --> t
+     t -- "makes the system call" --> w["pane, harness"]
+ ```
+
+ ## The way in
+
+ ```mermaid
+ flowchart TB
+     a["Relay.Flow.Launch.{ … }  as text"]
+       -- "protosize" --> b["Protos"]
+     b -- "datomize" --> c["Datom"]
+     c -- "compose as flow:Input" --> d["Launch { … }"]
+     d -- "rkyv" --> e["signal to flow.sock"]
+     e -- "Launched.7 back as signal" --> f["Output"]
+     f -- "datomize, protosize, textualize"
+       --> g["Relayed.Ok.Flow.Launched.7  as text"]
+ ```
+
+ The datom socket's signal:
+
+ ```ethos
+ Signal
+ [ translator:[ Request Answer Error ] ]
+ [ Relay.Request ]
+ [ Relayed.Result<Answer Error> ]
+ []
+ ```
+
+ In, the CLI's one argument:
+
+ ```datom
+ Relay.Flow.Launch.{ { Psyche core Primary }
+                     Predecessors.2
+                     «Design the translator» }
+ ```
+
+ Out, the CLI's reply:
+
+ ```datom
+ Relayed.Ok.Flow.Launched.7
+ ```
+
+ A text that fails names the layer that refused it
+ and the path of the datom where it did:
+
+ ```datom
+ Relayed.Err.{ Compositional [ 0 1 ]
+               «Predecessors.x: x is not an integer» }
+ ```
+
+ ## The way out
+
+ ```mermaid
+ flowchart TB
+     n["Flow Nexus"]
+       -- "emits Emit.Flow.Prompt.{ 3 message }"
+       --> t["translator"]
+     t -- "textualizes message" --> x["datom text"]
+     x -- "the one body for Prompt" --> h["herdr send 3 «text»"]
+     h -- "exit status" --> t
+     t -- "Emitted" --> n
+ ```
+
+ The translator starts the subprocess: it is the one
+ place that knows what a Prompt is in this world. An
+ output a Nexus wants textualized and returned is
+ asked with Textualize.
+
+ The signal socket's signal:
+
+ ```ethos
+ Signal
+ [ translator:[ Answer Text Error ] ]
+ [ Textualize.Answer
+   Emit.Answer ]
+ [ Textualized.Result<Text Error>
+   Emitted.Result<Done Error> ]
+ []
+ ```
+
+ In, from the Flow Nexus, as signal:
+
+ ```datom
+ Emit.Flow.Prompt.{ 3 { { Psyche core Primary }
+                        Soft.Question.«Ruled?» } }
+ ```
+
+ Out:
+
+ ```datom
+ Emitted.Ok.Done
+ ```
+
+ ## The library
+
+ Request and Answer have one variant per Nexus,
+ carrying that Nexus's own Input or Output, so a
+ text names its type by its heads.
+
+ ```ethos
+ Library
+ [ :flow:[ Input Output ]
+   :orchestrate:[ Input Output ] ]
+ [ Text.String
+   Request.[ Flow:flow:Input
+             Orchestrate:orchestrate:Input ]
+   Answer.[ Flow:flow:Output
+            Orchestrate:orchestrate:Output ]
+   Layer.[ Textual Protosic Datomic
+           Compositional ]
+   Path.Vector<Integer>
+   Error.{ Layer Path String }
+   Done ]
+ [ Emittable.[ emit.[ Result<Done Error> ] ] ]
+ [ Prompt.[ Emittable ] ]
+ ```
+
+ The one hand-written body per output type:
+
+ ```rust
+ impl Emittable for Prompt {
+     fn emit(&self) -> Result<Done, Error> {
+         let text = self.message
+             .datomize(Path::root())
+             .protosize().textualize();
+         self.pane.send(text)
+     }
+ }
+ ```
+
+ ## Many translators
+
+ ```mermaid
+ flowchart TB
+     s["flow 0.44, stable"]
+       -- "is built against" --> ts["translator-a81f"]
+     x["flow 0.45, next"]
+       -- "is built against" --> tx["translator-c07e"]
+     ts -- "serves" --> s
+     tx -- "serves" --> x
+ ```
+
+ A Nexus is configured with its translator and
+ discovers nothing; the suffix only keeps them apart.

### Proposal 2: One line · psyche-belief › vision/nexus.md

**Comment** Under Signal only.

  A Nexus speaks only the signal contracts it is compiled with; two of these
  are its own, one per socket.
+ Text enters and leaves through the translator: a Nexus emits typed outputs and holds no codec.
