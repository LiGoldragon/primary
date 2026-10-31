Presentation.{ «The Translator» }

# The Translator

### Proposal 1: The Translator · psyche-belief › vision/translator.md, a new file

**Comment** The running Flow Nexus writes its output as strings shaped like datom. That text is made by hand, in the Nexus, and it is fake datom: no type stands behind it, so it has already carried a deep design flaw and incorrectness. A Nexus thinks in typed values and speaks signal alone; every string it writes is a bug waiting. The Translator takes the whole of text out of every Nexus. A Nexus emits a typed value; the Translator, the one place that holds a codec, turns it into datom text or into the system call it stands for. The same component turns datom text into signal on the way in, so the CLI becomes one of its users.

+ ---
+ description: The Translator, which carries datom to signal and signal to datom for every Nexus and the CLI, is being designed or judged.
+ dependencies: [vision-nexus, vision-ethos, vision-versioning]
+ ---
+
+ ## What the Translator is
+
+ The Translator is the component that carries datom to signal and signal to datom, given a target and a direction. It is shared: several Nexuses and the CLI use one Translator. It is not a Nexus: it keeps no domain and no Memory; it is compiled with the signal contracts it reads and writes, and it knows one more thing, how each output type leaves the system.

```mermaid
+ flowchart TB
+     cli["CLI: one inline datom"]
+     t["Translator"]
+     n["Nexus"]
+     w["the world: a Herdr pane, a terminal"]
+     cli -- "text" --> t
+     t -- "signal: the query" --> n
+     t -- "signal: an input" --> n
+     n -- "signal: an output" --> t
+     t -- "the effect: a system call, or datom text" --> w
```

+ ## Inbound: text becomes signal
+
+ A CLI takes one inline datom and hands it to the Translator with the contract it belongs to. The Translator actualizes it against that contract and sends the signal to the Nexus. Nothing of the text reaches the Nexus. The reply comes back as signal, and the Translator turns it into datom text for the CLI.
+
+ ## Outbound: a Nexus emits an output, never a command
+
+ An output is a typed value a Nexus emits toward the world that returns nothing to it: a prompt into a Herdr pane, an interrupt, a line for a terminal. An output is a Signal, of no special kind: the Flow Nexus declares Prompt and Interrupt among the responses of its ordinary Signal, and the Translator is the peer those responses are sent to, the one compiled with the body that makes each real. Those bodies are the spec of the system calls that exist; no other call is made. So the Flow Nexus never writes `herdr` as a string; it emits a Prompt, and the Translator knows what a Prompt is in this world.

```mermaid
+ flowchart TB
+     n["Flow Nexus"]
+     p["a Prompt"]
+     t["Translator"]
+     h["a Herdr pane"]
+     n -- "emits, as signal" --> p
+     p -- "goes to" --> t
+     t -- "delivers the datom text into" --> h
```

+ The Ethos, the Flow Nexus's Signal, its two outputs beside the other responses:

```ethos
+ Signal
+ ; imports
+ [ flow:[ FlowId Address Event
+          Pane Message ] ]
+ ; queries
+ [ Launch.{ Address Brief.String }
+   Report.{ FlowId Event } ]
+ ; responses
+ [ Launched.FlowId
+   Refused.[ NoCapsule
+             AddressBusy.Address ]
+   Reported
+   ; outputs, sent to the Translator: a message
+   ; delivered into a pane, as datom text
+   Prompt.{ Pane Message }
+   ; a pane interrupted, no text
+   Interrupt.Pane ]
+ ; types
+ []
```

+ The Rust generated for the Prompt:

```rust
+ #[derive(Datomizable, Compositional)]
+ pub struct Prompt_Data {
+     pub pane: Pane,
+     pub message: Message,
+ }
```

+ The one Translator trait an output type bears, its body hand-written in the Translator and nowhere else:

```rust
+ pub trait Emittable {
+     fn emit(&self) -> Result<Emitted, Refused>;
+ }
+ impl Emittable for Prompt_Data {
+     fn emit(&self) -> Result<Emitted, Refused> {
+         // the only place the datom text is made
+         let text = self
+             .message
+             .datomize(Path::root())
+             .protosize()
+             .textualize();
+         // the only place the pane is reached
+         self.pane.deliver(text)
+     }
+ }
```

+ The datom, what the Flow Nexus emits, shown as text though it travels as signal:

```datom
+ Prompt.{ 3
+   { { Psyche core Primary }
+     Soft.Question.«Is the fresh store ruled?» } }
```

+ ## The Translator is a peer
+
+ Starting and ending a harness in a pane are system calls as much as a prompt is, so they are reactions the Translator receives, and what the Translator witnesses returns to the Nexus as inputs, answered like any input. The Nexus owns the contract: every reaction and every witness is a type of the Nexus's own Signal, the Translator is compiled with that Signal, and the direction is given by which side sends. In its first embodiment the Translator is a library the CLI and the Nexus link; it becomes a process on a socket when two versions must run at once.
+
+ The Ethos, the Flow Nexus's Signal, the part the Translator speaks:
+
+ The answers section, the fifth, is proposed in The implied traits, a draft; Ethos Zero does not yet accept it, so this block is checked without it.

```ethos
+ Signal
+ ; imports
+ [ flow:[ Pane Capsule Login Message
+          Process ExitCode ] ]
+ ; inputs from the Translator: what it witnessed
+ [ Started.{ Pane Process }
+   Exited.{ Pane ExitCode }
+   Delivered.Pane ]
+ ; outputs to the Translator: reactions,
+ ; a system call each
+ [ Start.{ Pane Capsule Login }
+   Prompt.{ Pane Message }
+   Interrupt.Pane
+   End.Pane
+   ; the answer to every witness
+   Recorded ]
+ ; types
+ []
+ ; answers
+ [ Started.[ Recorded ]
+   Exited.[ Recorded ]
+   Delivered.[ Recorded ] ]
```

+ The datom, one exchange, shown as text though it travels as signal:

```datom
+ ; the Nexus reacts: a harness is to start
+ ; in pane 3
+ Start.{ 3 { /home/li/primary [] } }
+ ; the Translator witnessed it, with the process
+ Started.{ 3 3829245 }
+ ; the Nexus answers
+ Recorded
```

+ ## The Translator's own signal

```ethos
+ Signal
+ ; imports
+ [ translator:[ Text Name Version
+                Error Signal ] ]
+ ; queries: text to become signal under a contract
+ [ Actualize.{ Contract Text } ]
+ ; responses
+ [ Actualized.Signal
+   ; the Translator is not compiled with it
+   Refused.[ UnknownContract.Contract
+             ; the text did not match the contract
+             Malformed.Error ] ]
+ ; types
+ [ Contract.{ Name Version } ]
```

+ ## Many Translators run at once
+
+ A stable Nexus keeps the Translator it was built against while a next version runs with its own, because contracts change between versions. Each running Translator carries a unique suffix, a random hash; a Nexus is configured with the Translator it uses and discovers nothing. The suffix has no meaning at run time; it keeps the Translators apart.

```mermaid
+ flowchart TB
+     s["stable Nexus"]
+     x["next Nexus"]
+     ts["its Translator, one random suffix"]
+     tx["its own Translator, another suffix"]
+     s -- "is configured with" --> ts
+     x -- "is configured with" --> tx
```

### Proposal 2: Text through the Translator · psyche-belief › vision/nexus.md

  ## Signal only

- Every client speaks to a Nexus in pure signal, fully binary. A Nexus
- speaks only the signal contracts it is compiled with; two of these
- are its own, one per socket. A Nexus thinks in typed values — enums,
- structs, scalars — and the string fields it still carries are
- records on the way to a fully typed form.
+ Every client speaks to a Nexus in pure signal, fully binary. A Nexus
+ speaks only the signal contracts it is compiled with; two of these
+ are its own, one per socket. Text enters and leaves through the
+ Translator: a Nexus emits typed outputs and holds no codec. A Nexus
+ thinks in typed values — enums, structs, scalars — and the string
+ fields it still carries are records on the way to a fully typed form.
