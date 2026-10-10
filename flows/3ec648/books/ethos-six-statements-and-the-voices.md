Presentation.{ «Ethos, six statements and the voices» }

The books before this one («Ethos in three layers, redone», «Kinds and parameters, the deep dive») carry no comment from you, so nothing is answered here. 91ea9f put six distilled ethos statements to you in chat, which you do not read; here they are, in your running system, with the words you typed to 91ea9f on voices as it retired. Answer by naming numbers.

**1. A voice is an aspect carrying a rank; a side flow is a job.**

> "Actually no, it's not psyche Astra. It's psyche primary, psyche secondary, mind primary, mind secondary, because we're not going to expose all the models to all of the voices. For now there are 9 voices, 3 by 3. ... They're sort of side flows. They're not long-lived. They're focused flows. ... Whatever message was sent to it goes back, I guess, to whoever sent it, with the notice that this flow has ended and so its mission is done, right?" — psyche, typed, 2026-10-02, to 91ea9f.

This answers the `Mind.Astra` question before you: the model is not in the name. Statement for `Vision/voices`: *A voice is an aspect carrying a rank, `Psyche.Primary`; nine voices, three aspects by three ranks. A side flow is a job, not a voice: it ends, and a message sent to it after that returns to its sender with notice that its mission is done.*

In ethos, and Flow starting the primary Mind:

```
Voice.[ Psyche.Rank
        Mind.Rank
        Field.Rank ]
Rank.[ Primary Secondary Tertiary ]

Launch.{ Mind.Primary «design the single committer» }
```

**Ruling 1:** this statement. One thing it leaves open: a side flow is reached by its flow id, as flows are today, and the returned message carries `Ended.{ FlowId }` beside the original body. Say if that is not how you see it.

**2. Four roots: Library, Signal, Operation, Memory.**

> "Yeah the memory is good. That's what it is I guess: signal, operation, and memory." — psyche, typed, 2026-10-02.

Statement for `Vision/ethos file roots`: *An ethos file is one of four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says, Operation what it does, Memory what it remembers; Library declares what they share.* This replaces the skill's "Three roots: Library, Signal, Sema".

Statement for `Vision/nexus process and memory`: *The running actor at the heart of a Nexus is its Process; what the Process remembers is its Memory, held by the Sema engine; what crosses its sockets is Signal.* This replaces "The decision-making engine inside it is Nexus Core".

In the Flow Nexus: `Launch` and `Launched` are Signal; starting a harness and recording a hook's report are Operation; the flow record with its state is Memory. **Ruling 2:** these two statements.

**3. Types inline, laid out downward.**

> "I don't want this repetition of types, like where we invent another type to say what's inside a variant. ... unless a type is used in more than one place, it should be declared inline." — psyche, typed, 2026-10-02.
> "I want it to be a language that expands vertically. ... I don't want the closing delimiter to create a whole new line" — psyche, typed, 2026-10-02.

Statement for `Vision/type declaration and nesting`: *A type used once is declared inline where it is used; a type used twice is declared once in its section and named thereafter. A variant's payload is written in the variant, never as a type invented to hold it. Inline nesting goes about three deep; past that, a Library.*

Statement for `Vision/ethos vertical layout`: *Ethos is laid out vertically: a structure with more than one element opens on its line and its elements hang beneath the first, indented to align; the closing delimiter ends the last element's line. Nothing is written on one line that has a next layer.* This replaces "Ethos follows the canonical protos print".

A hook reporting, written that way:

```
Signal
[ Report.{ FlowId
           Event.[ Started
                   ToolUsed.String
                   Stopped ] } ]
[ Reported.FlowId ]
[ FlowId.Integer ]
```

`Event` is used once, so it lives inside `Report`; `FlowId` is used twice, so it is declared once below. **Ruling 3:** these two statements.

**4. A capability's inputs are kinds, never a concrete type.**

> "I don't understand how there's a specific type as an input for a kind. That shouldn't be, right? It should only be another kind because a type is too specific. ... The voice is launchable, right, so it uses self." — psyche, typed, 2026-10-02.

Statement for `Vision/capability input rule`: *A capability speaks in Self, the kind's own parameters, and other kinds; a concrete type in an input is a kind not yet named.*

What changes in the generator: a kind name in an input position becomes a parameter; a concrete type there is refused. The messenger resolving a name, today and after:

```
Resolvable.[ resolve.{ [ String ] [ Voice ] } ]          ; today: String is concrete, refused after

Resolvable.{ [] [ Name<Textualizable> ] []
             [ resolve.{ [ Name ] [ Self ] } ] }          ; after: the bearer says what a Name is
```

**Ruling 4:** this statement, and the generator change with it.
