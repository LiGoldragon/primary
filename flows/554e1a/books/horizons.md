Presentation.{ «Vision by horizon» }

# Vision by horizon

Designed by Fable 5.1; the records gathered by a Sonnet 5.5 subflow of the Psyche core Secondary. Second edition, on your words of tonight; Two horizons is closed.

One idea: vision divided by horizon into modules, so a flow loads the horizon its work needs and nothing of the others. Flow, whole is revisited after this is ruled.

### Proposal 1: Vision is divided by horizon · psyche-context › intent/psyche.md

**Comment** Your words tonight, as lines. The far horizon is named far: one syllable beside short, medium and long, and it says what it is. A short line names the medium line it stands in for, so the compromise is removed when its replacement lands and no one has to compare the modules to know.

- ## Vision is short-term or long-term
-
- Vision is what the living says the system should be, in the long term or for now, the short term. A long-term line is marked In the long term; an unmarked line holds now.
-
- The long-term vision is the goalpost; the short-term vision is what the system is to be for now. Either may be implemented or not. A flow holds both apart, each true at its own horizon. When the long-term vision is implemented and documented, the short-term vision and its documentation are removed.
+ ## Vision is divided by horizon
+
+ Vision is what the living says the system is to be, and a topic's vision is divided by horizon into modules, so a flow loads the horizon its work needs. The unmarked module, vision:<topic>, holds what is true of the topic at every horizon. vision:short:<topic> holds the compromises in force now: the short-term solutions and hacks, each naming the medium line it stands in for. vision:medium:<topic> describes the system as it is to be past the compromised phase. vision:long:<topic> describes it as it is ideally to be. vision:far:<topic> holds the living's broadest idea of it, loaded only by a flow that must understand the whole.
+
+ Any horizon may be implemented or not; a flow holds each true at its own horizon. When a line of a farther horizon is implemented and documented it moves to the nearer module, and the short line that stood in for it is removed with its documentation.
+
+ A metaflow's declaration names the horizons it loads. A flow that implements or repairs loads the unmarked and the short; a flow that designs loads the medium and the long beside them; the far is loaded by name.

```datom
; a declaration, as datom, naming the horizons a metaflow loads
{ { Field core Tertiary } [ vision:flow-nexus vision:short:flow-nexus ] }
{ { Psyche flow Primary } [ vision:flow-nexus vision:short:flow-nexus vision:medium:flow-nexus vision:long:flow-nexus vision:far:flow-nexus ] }
```

### Proposal 2: A long line is built in its time · psyche-context › intent/psyche.md

**Comment** Your comment on Flow, whole: long-term ideas, underspecified, get built monolithic and hardwired. With the horizons as modules, the mark on a line becomes the module it sits in.

+ To an implementer a medium, long or far line says: not this iteration. Such a line is built only after a proposal moves it to the short or unmarked module with its design: the abstractions it is made of, how they compose, and the configuration the running system takes it through, shown as vision code. Until then the implementer builds the short line beside it, shaped so the farther line can take its place.

### Proposal 3: A step is one thing · psyche-context › intent/design.md

**Comment** Your picture of the nail driver asked to design the house, do the accounting and drive the nails, who builds a mud hut.

  A short-term proposal is one step from what exists: it names what it builds on, and proposes only what can be built next.
+ A step is one thing: the design, or an abstraction the design needs, or the behavior on that abstraction, each judged on its own before the next is begun. A line that needs an abstraction the system lacks is two steps, the abstraction first.
