# Design: Vision is a series of versions

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file, in the in-place form, each touched module shown whole. Title: «Vision is a series of versions». Kind: Proposal. Signature line: Created by Fable 5.2; a worker assembled the page. Wording marked ADD, REMOVE, REPLACE or COMMENT is final. Modules: /git/github.com/LiGoldragon/psyche-belief.

His words, 12 November: «we don't really do short, long, and far. We just do version numbers. We start at 0. Whenever we start a new concept, that's version 0, and what follows after that is version 1. Once version 1 has already been spec'd out quite a bit, even though we might be on version 0, if I have new ideas that don't really fit in version 1 anymore (because we already have some implementation and it would sort of break things too much, or would try to put too much onto version 1), that's when version 2 comes in. Eventually, version 0 sort of becomes phased out, and we just keep going with the numbers. There's no more far and short. There's just a series of successively more capable visions. Each gets their own main branch, so to speak, on the repo that has the code, or the repos, plural, that have the code for this vision.»

---

## Proposal 1: Versions in place of horizons · psyche-belief › intent/psyche.md, vision/psyche.md, vision/belief-modules.md

REMOVE, the whole section «## Vision is divided by horizon»: its heading and its three paragraphs (beginning «Vision is what the living says the system is to be», «A line in a marked module is unimplemented by definition», «A medium, long or far line reaches an implementer»). Shown beside the ADD below, which makes it unnecessary.

COMMENT
His words, 12 November, later still: «I would say vision versioning is vision, not intent. Intent is like very hardly crystallized psyche that is meant to sort of become an integral part of how flows think.» So the section leaves the intent on psyche and nothing takes its place there; the versions are said in vision.

ADD, to psyche-belief › vision/psyche.md, a new section at the end of the module:
## Vision is a series of versions

Vision is what the living says the system is to be. A topic's vision is versioned as every belief module is, and each version is more capable than the one before. A new idea goes into the latest version until that version is specified and implemented so far that the idea would break it or put too much on it; then the next version begins, and the idea goes there. An earlier version is phased out as the later ones run, and the numbers go on.

Each version of a vision has its own main branch in each repository that holds its code. Several versions may be in implementation at once.

COMMENT
His words, 12 November, later: «The versioning of Vision is not specific to Vision. All belief modules can use versioning, because what if we have a knowledge module on the flow nexus? Then we need a knowledge module for each version, right? So all of the versioning stuff can live on in a module that is going to be shared by, that it will be a dependency of Vision. So when we make dependency modules, we have to make them focused on what they're about, right? So this is about belief modules, if I'm not mistaken.» «Vision can mention it, but in the context of Vision, right? So there's bits that are specific to how we version Vision, and there's bits that are specific to how we version knowledge.» So what is true of every type's versions goes to the vision on belief modules, and the section above keeps what is the vision's alone.

ADD, to psyche-belief › vision/belief-modules.md, a new section at the end of the module:
## A belief module is versioned

Every belief module is versioned, as software is. A topic's belief modules are a series of versions: a new concept starts at version 0, and what follows it is version 1. Each version has its own module, and every module's name is three fields, its type, its topic and its version number, `<type>:<topic>:<number>`; a topic with one module has it at version 0. A change to a module's lines is a revision of that version; a new number begins a version that stands beside the earlier one. A module of any type that is about one version of a thing carries that version: `vision:flow-nexus:1` says what the Flow Nexus, version 1, is to be, and `knowledge:flow-nexus:1` holds what is known of it as built.

---

## Proposal 2: The same word in the psyche vision · psyche-belief › vision/psyche.md

REPLACE, only the changed words marked:
was: The horizons separate what he sees long term from what he pursues now so that it arrives more quickly.
becomes: The versions separate what he sees further on from what he pursues now so that it arrives more quickly.

---

## Proposal 3: The version is a field of the name · psyche-belief › vision/

COMMENT
His words, 12 November: «we can't separate the version number from the topic using a separator that is used in the topic itself. Do we really need the v there? Essentially, we're separating fields in a struct, so we can use the colon to separate all of the fields.» A module's name is three fields, type, topic and version, the colon between them; its file is the version under a folder of its topic. Every module that carries a version or a horizon in its name takes the form. The content is unchanged; each description drops «far», «long» or «short-term», since the name now carries the version, and the worker shows each as it would read.

ADD, to vision/belief-nexus-v1.md (itself renamed below), in the Library ethos, replacing the ModuleName line; shown as a REPLACE:
was:
  ModuleName.{ Kind Subject.String }
becomes:
  Version.Integer
  ModuleName.{ Kind Subject.String   ; type, topic and version: the three fields of every name
               Version }             ;   0 for a topic with a single module

```datom
{ Vision flow-nexus 1 }              ; vision:flow-nexus:1, the file vision/flow-nexus/1.md
{ Vision proposal 0 }                ; vision:proposal:0, the file vision/proposal/0.md
```

COMMENT
His words, 13 November: «I think it would be more consistent if all the belief modules were versioned.» «Maybe we just make a belief nexus that can work now, that does this, and that has a version number all the time for everything. When I'm reading the proposal and I see no version numbers, we should think of everything as software, essentially. If we think of belief modules as software, then they need to be versioned, I think.» So no name is without its number: every module of every type that has no version today becomes version 0 of its topic, `<type>/<topic>.md` becoming `<type>/<topic>/0.md`, in psyche-belief, mind-belief and field-belief alike; vision/flow-nexus.md becomes vision/flow-nexus/0.md. The modules already versioned are listed below.

REPLACE, module paths (the skill name follows: vision/flow-nexus/1.md is vision:flow-nexus:1):
vision/flow-nexus-v1.md becomes vision/flow-nexus/1.md
vision/far-flow-nexus.md becomes vision/flow-nexus/2.md
vision/nexus-v1.md becomes vision/nexus/1.md
vision/long-nexus.md becomes vision/nexus/2.md
vision/sema-v0.md becomes vision/sema/0.md, the lines of vision/short-sema.md moved to its end
vision/long-sema.md becomes vision/sema/1.md
vision/far-sema.md becomes vision/sema/2.md
vision/short-ethos.md becomes vision/ethos/0.md
vision/long-model-roles.md becomes vision/model-roles/1.md
vision/far-versioning.md becomes vision/versioning/1.md
vision/belief-nexus-v1.md becomes vision/belief-nexus/0.md, by his word of 13 November: «I don't see that we are at belief nexus version 1 yet. I think we're still at version 0.» «No, curriculum is not belief. There, we renamed the concept, but that doesn't mean that belief version 0 is curriculum.» The Belief Nexus is a concept of its own and begins at 0
vision/complex-v1.md becomes vision/complex/1.md
vision/energy-nexus-v1.md becomes vision/energy-nexus/1.md
vision/herdr-nexus-v1.md becomes vision/herdr-nexus/1.md

---

## Proposal 4: The horizon words that remain · psyche-belief › intent/design.md, vision/psyche.md, vision/proposal.md

COMMENT
Added by Psyche beliefReview Fable, from the belief review: three lines elsewhere that still speak in horizons, or of one vision where there is now a series.

REPLACE, in intent/design.md, only the changed words marked:
was: A short-term proposal names what it builds on and proposes only what can be built next.
becomes: A proposal for the version being built names what it builds on and proposes only what can be built next.

REPLACE, in vision/psyche.md, only the changed words marked:
was: there is one vision, the one in the module now, and nothing refers to a past one.
becomes: each version has one vision, the one in its module now, and nothing refers to a past one.

REPLACE, in vision/proposal.md, only the changed words marked:
was: A versioned module is self-contained: everything true of that version is in it, and the version is named once, in its description. Another version is not mentioned.
becomes: A versioned module is self-contained: everything true of that version is in it, and the version is named once, in its name. Another version is not mentioned.
