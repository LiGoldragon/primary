Presentation.{ «The translator» }

# The translator

Created by Fable.

### Proposal 1: The translator · psyche-belief › vision/translator.md, a new file

**Comment** The translator is the one process that holds datom-codec and every contract with the datom feature on. Everything else speaks pure signal. It has two doors: the datom door, where text comes in and text goes back, and the signal door, where a Nexus brings signal and says where its text is to go. The fd and system-call question is settled by one rule: the translator owns text, the caller owns the process. A descriptor is text's place, so the translator writes into it; a system call is a process, so the translator hands back the argument line and the caller, who has the identity, the capsule and the environment, starts the child.

+ ## What the translator is
+
+ The translator is the Nexus that carries data between
+ its textual form, datom, and its signal form. It is
+ compiled with every contract it translates, with the
+ datom feature on; it is the one process that holds
+ datom-codec. Every other Nexus speaks signal only.
+
+ ## Two doors
+
+ The datom socket is the door in: text arrives, is
+ composed into the target's input, sent, and the
+ target's answer comes back as text. The signal socket
+ is the door out: a Nexus brings signal and names where
+ the text goes. The meta socket configures it.
+
+ ```
+ text world            translator            signal world
+ CLI, hook  --datom--> [ compose ] --signal--> target Nexus
+            <--datom-- [ textualize ] <--signal--
+ Nexus      --signal-> [ textualize ] --text--> descriptor
+                                      --text--> reply
+ ```
+
+ ## The translator owns text; the caller owns the process
+
+ A request on the signal door wraps the object in its
+ destination. A reply or a descriptor is a place text
+ goes, and the translator writes there. A system call
+ is a process, and the Nexus that asked starts it,
+ since it holds the identity, the capsule and the
+ environment the child runs in; the translator gives it
+ the text, and the text is one argument. The descriptor
+ rides the socket beside the frame, as the socket layer
+ carries it; the request has no field for it.
+
+ ## The library
+
+ Every target is a variant carrying that target's own
+ input or output, so a text names its type by its heads
+ and holds no string inside a string.
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
+   Error.{ Layer Path String } ]
+ []
+ []
+ ```
+
+ ## The datom door
+
+ ```ethos
+ Signal
+ [ translator:[ Request Answer Error ] ]
+ [ Relay.Request ]
+ [ Relayed.Result<Answer Error> ]
+ []
+ ```
+
+ In, as the Flow CLI sends it:
+
+ ```datom
+ Relay.Flow.Launch.{ { Psyche core Primary }
+                     Predecessors.2
+                     «Design the translator» }
+ ```
+
+ Out:
+
+ ```datom
+ Relayed.Ok.Flow.Launched.7
+ ```
+
+ A text that fails names its layer and its path:
+
+ ```datom
+ Relayed.Err.{ Compositional [ 0 1 ] «x is not an integer» }
+ ```
+
+ ## The signal door
+
+ ```ethos
+ Signal
+ [ translator:[ Answer Text Error ] ]
+ [ Textualize.Answer
+   Write.Answer ]
+ [ Textualized.Result<Text Error>
+   Written.Result<Integer Error> ]
+ []
+ ```
+
+ In, from the Flow Nexus, with the harness's stdin
+ riding the socket:
+
+ ```datom
+ Write.Flow.Launched.7
+ ```
+
+ Out, the bytes written:
+
+ ```datom
+ Written.Ok.15
+ ```
+
+ For a system call the Flow Nexus asks Textualize, gets
+ `Textualized.Ok.«Launched.7»`, and starts the child
+ itself with that text as the one argument.
+
+ ## Memory
+
+ The translator remembers what it has read, keyed by
+ the hash of the normalized text, so a text met twice
+ is composed once.
+
+ ```ethos
+ Memory
+ [ translator:Request ]
+ [ Reading.{ Hash.String Request } ]
+ ```

**Alternative 1** The translator also starts the child: `Invoke.{ Executable Answer }` answered by `Invoked.Result<ExitStatus Error>`. Rejected in the comment above: the child would run as the translator, not as the Nexus that owns it.
