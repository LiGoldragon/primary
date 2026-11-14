# Design: Permaflows, listed briefly; metaflows, as cohesion

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file, in the in-place form, each touched module shown whole. Title: «Permaflows, listed briefly». Kind: Proposal. Signature line: Created by Fable 5.2; a worker assembled the page. Wording marked ADD, REPLACE, QUESTION or COMMENT is final. The page ends with the section «Questions», exactly as written at the end of this file. Modules: /git/github.com/LiGoldragon/psyche-belief.

His words, 12 November: «I see all of the noise in there. There's all this logical delivery, and then 000000, like endless zeros. Super expensive, useless garbage, and not everybody needs to know about all the metaflows.» «We should have a command that's very brief so that it doesn't take much context. If anything, the topic should be pretty self-descriptive.» «I think the rename is good: Permaflows instead of Metaflow. A Metaflow is a composition of Permaflows, like a sector that is coherent together, like a fable and its assistant opus, and maybe some kind of small task-managing flow along with it. It doesn't have any other effect than to decide which other Permaflows are listed, and then we could have a way to list the Metaflows themselves. It's more like an information-based thing than a constraint-based thing. It doesn't constrain any flow or messaging. Let's keep the system open so that nothing blocks flows from messaging each other if they need to.» «I want all of the default commands to not show this. We can have debug versions of the same commands that can show this more backend-related information.»

---

## Proposal 1: The listing · psyche-belief › vision/flow-nexus.md

ADD, a new section after the section «## A message»:
## Permaflows and metaflows

A permaflow is one address. A metaflow is a cohesion of permaflows that work together, as a Fable, the Opus that assists it and a small flow that keeps their tasks: it has a name, a camelCase expression that says what it is for, and it is configuration, changed while the Nexus runs. A metaflow informs: it decides which permaflows a member is shown. It constrains nothing: any flow messages any flow.

A topic says what its permaflow is for, in its name.

The listing is brief. A flow asking for the permaflows is shown those of its own metaflows and those of its own topic, each as its address and whether it is awake; the Nexus knows the caller by its process, so the flow names nothing. A flow that carries messages between concerns lists the metaflows themselves.

```ethos
Signal
[ flow:[ Address ] ]                        ; imports
[ Permaflows.Scope                          ; inputs: the permaflows, briefly
  Metaflows ]                               ;   the metaflows, each with its members
[ Permaflows.Vector<Listed>                 ; outputs
  Metaflows.Vector<Metaflow> ]
[ Scope.[ Mine                              ; types: those of the caller's metaflows and of its topic
          All ]
  State.[ Awake Asleep ]
  Listed.{ Address State }
  MetaflowName.String                       ;   a camelCase expression: psycheCore
  Metaflow.{ MetaflowName Vector<Address> } ]
```

```datom
Permaflows.Mine
Permaflows.[ { { Psyche core Opus } Awake }
             { { Psyche core Sonnet } Asleep } ]
Metaflows
Metaflows.[ { psycheCore [ { Psyche core Fable } { Psyche core Opus } { Psyche core Sonnet } ] } ]
```

The owner arranges the metaflows over the meta socket, one value at a time, and a launch may name the metaflows its permaflow joins:

```ethos
Signal
[ flow:[ Address MetaflowName Metaflow ] ]  ; imports
[ Configure.Set ]                           ; inputs
[ Configured.Set ]                          ; outputs
[ Set.[ Metaflow                            ; types: a metaflow added or replaced, whole
        Join.{ MetaflowName Address }       ;   one permaflow added to it
        Leave.{ MetaflowName Address }
        Dissolve.MetaflowName ] ]
```

What the Nexus keeps for its own work, a queue's storage ids among it, is shown by the debugging form of a query and by no other.

---

## Proposal 2: The word, in the vocabulary · knowledge › vocabulary.md

REPLACE:
was: Metaflow: several flows arranged together: members, routes and a speaker; addressed by Launch and Send.
becomes: Metaflow: a named cohesion of permaflows that work together; it informs, and constrains nothing.

---

## Proposal 3: Questions stand in the proposal · psyche-belief › vision/proposal.md

COMMENT
His words, 12 November: «Instead of asking me here, let's make a special section, and it has to be short, like extremely short. You can ask me questions in the proposal.»

ADD, to the section «## A proposal», after the line «A question between alternative lines shows each alternative as its own proposal, with the exact lines it lands; the living rules land, amend or reject.»:
A proposal's questions to the living stand in a section of their own at its end, each a line or two.

---

## Questions

1. Version 1's vision says a metaflow has routes and a message off them is refused. Should version 1 take this meaning too, a cohesion that informs and refuses nothing, until recovery is solid?
2. Should a listing still show a permaflow's purpose on request, or does the purpose leave the listing entirely, the topic's name being enough?
