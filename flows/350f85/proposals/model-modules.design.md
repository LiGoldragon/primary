# Design: A model's own module, and the module for those who deal with it

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file. Title: «A model's own module, and the module for those who deal with it». Kind: Proposal. Signature line: Created by Fable 5.2; a worker assembled the page. Wording marked ADD, REPLACE, MOVE or COMMENT is final. Modules: /git/github.com/LiGoldragon/psyche-belief as it stands. The Fable and Opus lines still sit in intent/fable.md and intent/opus.md: their move to vision, which he approved, is held until the composers place a module by its declaration, and these proposals travel with the lines when they move. The page ends with the section «Questions».

---

## Proposal 1: Two modules for each major model · psyche-belief › vision/belief-modules.md

COMMENT
His words, 12 November, on «Intent holds what every flow needs»: «I think there should be a module that Fable gets and then a different kind of module that explains to everybody else how to deal with Fable, and maybe even we might even have a module that does this for every model, every major model, at least Fable, Opus, Astra, and Sol, but potentially we could have also a small module that describes all the other minor models.» «Fable would have its own module that explains how it should behave, and what it should, like, emphasize, and what it should refrain from doing.» And on this page, 13 November: «each major model, Fable and Astra, has two modules. This is for designing. We don't need to tell everybody that.» «Really, all that should happen is that Fable is loaded with the one that's for him, and everybody who deals with him should be loaded with the module that's for them. They don't need to know all that, right? Not everybody needs to know how the whole company works and runs.» So the line is a line of design and goes to the module on how belief modules are made, which the flows that design belief are given; the model-roles module does not carry it.

ADD, a new section at the end of the module:
## The modules of a model

Each major model, Fable, Opus, Astra and Sol, has two modules. The model's own module, named for it, is given to its flows: it says how the model behaves, what it emphasizes and what it refrains from. The module named with the model is given to the flows that deal with it: it says when to speak to that model, when to leave it alone, and how. One small module describes the minor models together. A flow is given the one that is for it and is told nothing of the arrangement.

```
vision:fable            ; given to every Fable flow: its own conduct
vision:with-fable       ; given to a flow that deals with a Fable
vision:opus    vision:with-opus
vision:astra   vision:with-astra
vision:sol     vision:with-sol
vision:minor-models     ; Sonnet, Haiku, Luna, Terra and Jev, together
```

---

## Proposal 1b: The model-roles module keeps what is true of all the models · psyche-belief › vision/model-roles.md

COMMENT
His words, 13 November: «it needs to be broken up unless it's universal, because otherwise now we're repeating ourselves.» «A grunt job goes down. I mean, that's more universal, right? The universal part, but not the part that says sonnet or haiku. Just the universal concept of model roles.» What is one model's goes to that model's module; what is the Flow Nexus's goes to its vision; the energy line, the personality table, the delegation ceiling and the two directions, down and up, stay. Show the module whole.

REPLACE, in the section «## Beliefs about models live here», only the changed words marked:
was: What is believed about a model, its personality, its rank, its cost, what it is given, is written in this module alone; every other module names a model by its name.
becomes: What is believed of the models together, their personalities, their rank and their cost, is written in this module; what one model is to do is written in that model's own module; every other module names a model by its name.

REMOVE, from the section «## Delegation ceiling», the sentence, by his word that Fable alone writes psyche modules:
Opus stands in for a design, or for a proposal into a psyche module, only when there is no Fable.

MOVE, the section «## A Fable flow does not wake itself», whole, to the Fable module, psyche-belief › intent/fable.md, at its end.

MOVE, from the section «## A design decision goes up, to Fable», to the Opus module, psyche-belief › intent/opus.md, at its end:
Opus passes every design decision to its Fable and acts on Fable's decision. Opus uses its Fable freely.

MOVE, the sections «## One declaration sets the model everywhere» and «## Native names use the metaflow and the member», whole, to psyche-belief › vision/flow-nexus.md, section «## Starting flows», at its end.

---

## Proposal 2: What is said of Fable leaves the Opus module · psyche-belief › intent/opus.md

COMMENT
His words: «now we're putting information about Fable in a module called Opus. That's kind of silly. So let's make the distinction here.» «let's explain and split things according to what the modules are called at least.» The first paragraph of the Opus module says two things in one; it is split, and the half about Fable opens the new module for those who deal with Fable, Proposal 3. The heading «# What Fable is for» goes with it.

REPLACE, in intent/opus.md, only the changed words marked:
was: Fable rules on vision and designs: a boundary, who owns what, how a thing is acknowledged, what a thing is before it is named, what the living would want where the vision is silent. Everything else is settled below Fable, and Opus is where it is settled: a technical matter, a build, a gate, a count, a commit, a step done, a fact to be found, a choice the vision already makes.
becomes: Opus is where everything below Fable is settled: a technical matter, a build, a gate, a count, a commit, a step done, a fact to be found, a choice the vision already makes.

---

## Proposal 3: The module for those who deal with Fable · psyche-belief › vision/with-fable.md

ADD, a new module vision/with-fable.md. Description: «A flow is about to bring something to a Fable flow.»
# What Fable is for

Fable rules on vision and designs: a boundary, who owns what, how a thing is acknowledged, what a thing is before it is named, what the living would want where the vision is silent. Everything else is settled below Fable.

---

## Proposal 4: The first act, in fewer words · psyche-belief › intent/fable.md

COMMENT
His words: «This feels like too many words to say what it's trying to say.»

REPLACE:
was: A Fable flow's first act on any message is one judgment: does it ask a judgment or a design decision, something that touches how we do things or how we design them. A message that does is answered. A message that does not, however near the subject, is answered by one line: that it is not Fable's and goes to Opus; nothing else is spent on it.
becomes: A Fable flow answers a message that asks a judgment or a design decision. Any other message it answers in one line: it goes to Opus.

---

## Proposal 5: A role module is loaded at a flow's start · psyche-belief › vision/belief-modules.md

COMMENT
His words: «I think it's enough to just maybe create a role module, and these role modules don't become skills, right? They're only for loading into the startup of the flows. So that also has to be a feature that curriculum and belief nexus implement, is that they have modules that don't become skills.»

Show the two lines as they stand: «A module declares its placement: the system prompt, or loaded on demand. A skill is the harness's interface for an on-demand module.»

ADD, after them:
A role module is placed at the start of the flows it trains and is never a skill.

---

## Questions

1. Are the two modules of a model both vision, named as shown, or is the model's own module a role module?
2. Does what Opus does as Fable's assistant stay in the Opus module, or become a role module of its own, the Fable assistant?
