Presentation.{ «Variations of a call stand at the root; the permaflows listing» Proposal }

# Variations of a call stand at the root; the permaflows listing

Created by Fable 5.2; a worker assembled the page.

### Proposal 1: The variations of a feature stand at the root · psyche-belief › vision/nexus.md

::: comment
His words, 12 November: «You would have different root level calls. You don't make the variant after. You make you see the ethos of a signal, right? The inputs is a variance. You put all of the different variations of the same feature there at the root. So the plainly named one is like the brief one, and then you have the more complex ones, which are the more longer names like advanced or custom or verbose or whatever it is that accurately describes the variation. Because the goal is for the default behavior to be extremely brief.» «So we should make a general vision about how to design a nexus with like the variations of the same command at the root level, and then the variations of the outputs also at the root level, so that we have to maximize context efficiency, which means most of the time we have short commands, simple form, and the variations are like other variants and not just like a longer, because if you make the call more complicated for everybody, now everybody's paying, and there's really no reason to do that at all.» «We really have, I don't feel like you're pushing the concept enough that every functionality has more than one way to call it. Some of which are more verbose, both in their output and also possibly in their input, to take more options.»
:::

::: shown
psyche-belief › vision/nexus.md
## Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.
:::

+ ## The variations of a feature stand at the root

+ A feature of a Nexus is called in more than one variation. Each variation is an input of its own, at the root of the Signal's inputs, and its answer is an output of its own, at the root of the outputs. The plainly named input is the default: the briefest to write and the briefest answered, because most calls are that one. A variation that takes more or answers more bears a longer name that says accurately what it varies: verbose, custom, debug. So the cost of a variation is paid by its caller alone, and the default call stays as short as its name. The names below are an example, one feature of many.

+ ```ethos
+ Signal
+ []                                    ; imports
+ [ Records                             ; inputs: the default, plainly named, takes nothing
+   RecordsVerbose.Limit                ;   a variation: takes an option, answers more
+   RecordsDebug.Limit ]                ;   a variation: answers what the Nexus keeps for its own work
+ [ Records.Vector<Name>                ; outputs: the default answer, the names alone
+   RecordsVerbose.Vector<Record>       ;   each record whole
+   RecordsDebug.Vector<Stored> ]       ;   each record with its storage id
+ [ Name.String                         ; types
+   Limit.Integer                       ;   how many records at most
+   Size.Integer
+   StorageId.String
+   Record.{ Name Size }
+   Stored.{ Record StorageId } ]
+ ```

+ ```datom
+ ; the default: asked, then answered
+ Records
+ Records.[ «alpha» «beta» ]
+ ; the verbose variation: one option taken, more answered
+ RecordsVerbose.1
+ RecordsVerbose.[ { «alpha» 12 } ]
+ ; the debugging variation
+ RecordsDebug.1
+ RecordsDebug.[ { { «alpha» 12 } «0000a3» } ]
+ ```

### Proposal 2: Permaflows, metaflows and the listing · psyche-belief › vision/flow-nexus.md

::: comment
His words, 12 November: «I see all of the noise in there. There's all this logical delivery, and then 000000, like endless zeros. Super expensive, useless garbage, and not everybody needs to know about all the metaflows.» «We should have a command that's very brief so that it doesn't take much context. If anything, the topic should be pretty self-descriptive.» «I think the rename is good: Permaflows instead of Metaflow. A Metaflow is a composition of Permaflows, like a sector that is coherent together, like a fable and its assistant opus, and maybe some kind of small task-managing flow along with it. It doesn't have any other effect than to decide which other Permaflows are listed, and then we could have a way to list the Metaflows themselves. It's more like an information-based thing than a constraint-based thing. It doesn't constrain any flow or messaging. Let's keep the system open so that nothing blocks flows from messaging each other if they need to.»
:::

::: shown
psyche-belief › vision/flow-nexus.md
## A message

A message is a datom and lands in the recipient's prompt as one; the datom is the whole message. Its priority is a head on the request: HardAbrupt, MiddleAbrupt or Soft. A pressing message wakes its recipient; a message that only queues carries what may wait. A message is addressed to a permaflow and reaches the flow running when it arrives; a request to deliver a recipient's queue delivers every queued message, or nothing when none is queued.

A message carries what its reader acts on: what the sender intends, or what it has done. It carries no hash: a flow is named by its permaflow, a book by its title, a commit by what it landed.

Inducing an interrupt, placing prompt text, submitting it, and the recipient consuming it are four separate observations. None of them stands for another, and a submission is never a read receipt.

A task carries the minutes it is expected to take; the Flow Nexus reminds the sender when they pass, and the done reply names the task and cancels the reminder. A receiver going idle with a task open fires a notice to the flow waiting on it, so that nothing is forgotten. Any flow asks the Flow Nexus for a reminder after a number of minutes.
:::

+ ## Permaflows and metaflows

+ A permaflow is one address. A metaflow is a cohesion of permaflows that work together, as a Fable, the Opus that assists it and a small flow that keeps their tasks: it has a name, a camelCase expression that says what it is for, and it is configuration, changed while the Nexus runs. A metaflow informs: it decides which permaflows a member is shown. It constrains nothing: any flow messages any flow.

+ A topic says what its permaflow is for, in its name.

+ The listing of the permaflows is one feature in three variations, each an input at the root. Permaflows, the default, takes nothing: the Nexus knows the caller by its process, and answers the permaflows of the caller's own metaflows and of its own topic, each as its address and whether it is awake. PermaflowsVerbose takes a scope and answers, for each permaflow, its purpose, its metaflows and how many messages wait for it as well. PermaflowsDebug answers what the Nexus keeps for its own work besides: the flow id and the storage ids of the queue. A flow that carries messages between concerns lists the metaflows themselves.

+ ```ethos
+ Signal
+ [ flow:[ Address FlowId ] ]                  ; imports
+ [ Permaflows                                 ; inputs: the default, the caller's own, nothing taken
+   PermaflowsVerbose.Scope                    ;   a scope taken, more answered
+   PermaflowsDebug.Scope                      ;   what the Nexus keeps for its own work
+   Metaflows ]                                ;   the metaflows, each with its members
+ [ Permaflows.Vector<Brief>                   ; outputs: each variation answered by its own
+   PermaflowsVerbose.Vector<Entry>
+   PermaflowsDebug.Vector<Internal>
+   Metaflows.Vector<Metaflow> ]
+ [ Scope.[ Mine                               ; types: those of the caller's metaflows and of its topic
+           All ]
+   State.[ Awake Asleep ]
+   Purpose.String
+   Waiting.Integer                            ;   messages queued for the permaflow
+   StorageId.String
+   MetaflowName.String                        ;   a camelCase expression: psycheCore
+   Brief.{ Address State }
+   Entry.{ Address State Purpose Vector<MetaflowName> Waiting }
+   Internal.{ Entry FlowId Vector<StorageId> }
+   Metaflow.{ MetaflowName Vector<Address> } ]
+ ```

+ ```datom
+ ; the default, as a flow calls it
+ Permaflows
+ Permaflows.[ { { Psyche core Opus } Awake }
+              { { Psyche core Sonnet } Asleep } ]
+ ; the verbose variation, every permaflow
+ PermaflowsVerbose.All
+ PermaflowsVerbose.[ { { Psyche core Opus } Awake «Choreographs, publishes and lands for Psyche.» [ psycheCore ] 0 }
+                     { { Mind curriculum Astra } Asleep «Rebuilds Curriculum version 1.» [ mindCurriculum ] 2 } ]
+ ; the debugging variation
+ PermaflowsDebug.Mine
+ PermaflowsDebug.[ { { { Psyche core Opus } Awake «Choreographs, publishes and lands for Psyche.» [ psycheCore ] 0 }
+                     «a41c07»
+                     [] } ]
+ ; the metaflows
+ Metaflows
+ Metaflows.[ { psycheCore [ { Psyche core Fable } { Psyche core Opus } { Psyche core Sonnet } ] } ]
+ ```

+ The owner arranges the metaflows over the meta socket, one value at a time, and a launch may name the metaflows its permaflow joins:

+ ```ethos
+ Signal
+ [ flow:[ Address MetaflowName Metaflow ] ]  ; imports
+ [ Configure.Set ]                           ; inputs
+ [ Configured.Set ]                          ; outputs
+ [ Set.[ Metaflow                            ; types: a metaflow added or replaced, whole
+         Join.{ MetaflowName Address }       ;   one permaflow added to it
+         Leave.{ MetaflowName Address }
+         Dissolve.MetaflowName ] ]
+ ```

### Proposal 3: The word, in the vocabulary · mind-belief › knowledge/vocabulary.md

::: shown
mind-belief › knowledge/vocabulary.md
Permaflow: one persistent address, { Aspect topic Model }, with its succession of flows.

Metaflow: several flows arranged together: members, routes and a speaker; addressed by Launch and Send.
:::

- Metaflow: several flows arranged together: members, routes and a speaker; addressed by Launch and Send.
+ Metaflow: a named cohesion of permaflows that work together; it informs, and constrains nothing.

### Proposal 4: Questions stand in the proposal · psyche-belief › vision/proposal.md

::: comment
His words, 12 November: «Instead of asking me here, let's make a special section, and it has to be short, like extremely short. You can ask me questions in the proposal.»
:::

::: shown
psyche-belief › vision/proposal.md
A question between alternative lines shows each alternative as its own proposal, with the exact lines it lands; the living rules land, amend or reject.
:::

+ A proposal's questions to the living stand in a section of their own at its end, each a line or two.

## Questions

1. Version 1's vision says a metaflow has routes and a message off them is refused. Should version 1 take this meaning too, a cohesion that informs and refuses nothing, until recovery is solid?
