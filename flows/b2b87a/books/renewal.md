Presentation.{ «The renewal» }

# The renewal

Designed by Fable 5.1 from your words of tonight; the research on spirit and on the overview is out with the Psyche research pair and lands in the next edition.

One idea: the rest of this week's usage goes into bringing every important Nexus up to date, through specialized Primaries and Opus Secondaries, under heartbeats that keep the system awake, with the overview crystallized as the north star. You asked a name for it; I propose **renewal**: a Nexus is renewed, and the push is the renewal.

### Proposal 1: The renewal · psyche-context › vision/high-level-view.md

**Comment** Your words: Opus subflows and specialized Primaries go through all the important nexuses and create at least an improved version; Mind pairs on Claude harnesses, Psyche pairs to design; rewrite from scratch where the history outweighs the worth.

+ ## The renewal
+
+ A renewal is a push in which every important Nexus is brought up to date: its ethos in the current Ethos syntax, its anatomy redesigned, and the nexuses made to work together. Each Nexus gets a Psyche pair that designs it and a Mind pair that builds it, on Claude harnesses, a specialized Primary with an Opus Secondary, started by Flow with the modules of that Nexus. A Nexus whose history outweighs its worth is rewritten from its vision. The renewal spends usage that would otherwise go unused; raising effort is not how capability is bought.

```datom
; the pairs of one renewed Nexus, as metaflows
{ Psyche creo Primary }   ; designs, Fable
{ Psyche creo Secondary } ; Opus
{ Mind creo Primary }     ; builds, on a Claude harness
{ Mind creo Secondary }
```

### Proposal 2: The north star · psyche-context › vision/high-level-view.md

**Comment** Your words name these components; the order is my inference from how you spoke of them, for you to reorder. The psyche nexus you called super high; persona is further down the pipeline; the Unity app is to start design.

+ ## The north star
+
+ The components wanted now, in order: the psyche nexus, which feeds every flow its spirit, intent and vision and takes its records; the Flow Nexus, which starts flows properly; Creo, the authentication layer, simplified to majority-signature approval, adaptable to the security a thing needs; the Unity app, written in Slint, through which the Menchie is made, driven from its Nexus; Persona, the meta nexus that choreographs the others, starting them and keeping them running. Every renewal starts from this order.

### Proposal 3: Heartbeats keep the system awake · psyche-context › vision/flow.md

**Comment** Your words: a faster hard beat on the Tertiary, checking that enough Mind and Psyche flows are active or recently active, waking the Secondary when not; a longer hard beat on the Secondary, checking behavior, implementations and testing together. The thresholds are configuration.

+ ## Heartbeats
+
+ The Psyche core Tertiary carries a fast hard heartbeat: at each beat it counts the Mind flows and the Psyche flows that are active or recently active against a configured minimum of each; when the minimum holds it passes, and when it does not it wakes the Psyche core Secondary. The Secondary carries a slow hard heartbeat of its own: at each beat it checks that the system behaves, that the implementations make sense, and that the nexuses are tested together, and brings what fails to its Primary.

```datom
; the heartbeat configuration, as datom
{ Tertiary { Every.300 MinimumActive.{ Mind.3 Psyche.2 } Recent.1800 } }
{ Secondary { Every.3600 } }
```

### Proposal 4: The psyche nexus · psyche-context › vision/psyche.md

**Comment** Your words: Curriculum hooks into it, or Flow hooks into psyche directly; records are logged with it; its ancestor spirit reviewed each entry with an LLM and crystallized at the gate; Jev, the System 1 model, is the fit for that judge. The research on spirit fills the next edition.

+ ## The psyche nexus
+
+ The psyche nexus holds the psyche: spirit, intent, vision and the raw records. Flow feeds each new flow its spirit, intent and vision from it, and every record is logged into it. An entry is judged at the gate, as spirit, its ancestor, did: it is accepted, refused as already held or as covered by an existing subject, or merged into the entry it improves; so what enters is crystallized on entry. The judge is Jev, fed what is required and expected of an entry.

### Proposal 5: Compensation ends; Mind holds knowledge and practice · psyche-context › intent/belief-modules.md

**Comment** Your words: abandon the compensation modules and redefine what the mind beliefs are. My proposal of the redefinition: Mind holds knowledge, facts verified in code, and practice, how a thing is done here, machine-written and changed by a mechanism; what compensation held that is still needed becomes practice, the rest is deleted; Field keeps role modules only.

- The module types stand in one order, highest first: spirit, intent, vision, knowledge, compensation. A module depends only on its own type or a higher one.
+ The module types stand in one order, highest first: spirit, intent, vision, knowledge, practice. A module depends only on its own type or a higher one. Knowledge is fact verified in code; practice is how a thing is done here, written by the machine and changed by a mechanism, and it ends when the system does the thing itself. Compensation is no longer a type: what it held and is still needed is practice.

### Proposal 6: The repositories are named belief · psyche-context › vision/belief-modules.md

**Comment** Your words: rename the context repositories with belief, because that is what we call them now.

- The belief modules belong in a context repository; Psyche's is psyche-context.
+ The belief modules belong in a belief repository, one per aspect: psyche-belief, mind-belief, field-belief.
