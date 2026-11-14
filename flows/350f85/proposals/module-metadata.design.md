# Design: What a module is, in its metadata

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file. Title: «What a module is, in its metadata». Kind: Proposal. Signature line: Created by Fable 5.2; a worker assembled the page. Wording marked ADD or COMMENT is final. Modules: /git/github.com/LiGoldragon/psyche-belief. The page ends with the section «Questions».

---

## Proposal 1: A flow is given what its own work needs · psyche-belief › vision/belief-modules.md

COMMENT
His words, 13 November: «Not everybody needs to know how the whole company works and runs. They just need to know that this is their project, they're working on it, here's how to contact the people they're supposed to work with, and here's how they're supposed to work, not like, "Here's how the company works."» «I don't want all of these skills, this giant list of skills, because some agents are really eager to load skills.» «it would be cool to have a workspace per perma flow so that we can control it.»

ADD, a new section at the end of the module:
## A flow is given what its own work needs

A flow is given what its own work needs: what its project is, how to reach those it works with, and how it is to work. How the whole is arranged is given to the flows that design it.

---

## Proposal 1b: A workspace for each permaflow, in version 1 · psyche-belief › vision/flow-nexus-v1.md

COMMENT
His words, 13 November: «it would be cool to have a workspace per perma flow so that we can control it.» And then: «To be clear, each flow getting its own workspace is not for the current version, just so that agents don't try to slop-code this into the current Nexus.» And: «No, the belief nexus is not what furnishes the workspace. It's either the flow nexus or another nexus made for that, but the belief nexus furnishes beliefs, not workspaces.» So the line goes to the Flow Nexus, version 1, and nothing of it is built into what runs now.

ADD, at the end of the module:
Each permaflow has a workspace of its own, made by the Flow Nexus or by a Nexus made for that, and holding the modules that are for it and no others, so a flow sees only what it may take.

REPLACE, in the front matter of psyche-belief › vision/belief-nexus-v1.md, the description, only the changed words marked:
was: The Belief Nexus, version 1, which holds the belief modules and furnishes workspaces with them in place of Curriculum, is being designed or judged against what the living wants it to be.
becomes: The Belief Nexus, version 1, which holds the belief modules and writes them into the workspace it is handed, in place of Curriculum, is being designed or judged against what the living wants it to be.

REPLACE, in the body of psyche-belief › vision/belief-nexus-v1.md, only the changed words marked:
was: The Belief Nexus holds the belief modules and furnishes workspaces with them
becomes: The Belief Nexus holds the belief modules and writes them into the workspace it is handed; it makes no workspace

The rest of that module stands: its Furnish input writes modules into a workspace another Nexus made.

---

## Proposal 2: Given or offered · psyche-belief › vision/belief-modules.md

COMMENT
His words: «these modules might not be agent-loadable. We might not want to make them agent-loadable.» «Is this something that we want the machine to be able to load by itself? Things like that. That might help us to think more clearly about what this module is.» «There's probably more metadata for a belief module than what we're using now.» Two words are proposed for what he asks: a module is given, or offered.

Show the two lines as they stand: «A module declares its placement: the system prompt, or loaded on demand. A skill is the harness's interface for an on-demand module.»

ADD, after them:
A module declares whether it is given or offered. A given module is composed into the start of the flows it is for, and no flow takes it by itself. An offered module stands in the workspace of the flows it is for, and a flow takes it when its work calls for it.

```yaml
# the front matter of a module, with the two new fields
description: A Fable flow judges, designs and speaks to the living.
dependencies: []
taking: given            # given, or offered
subkind: behavior        # what kind of vision this is: Proposal 3
```

```ethos
Library
[]                                         ; imports
[ Taking.[ Given                           ; types: composed into a flow's start, taken by no flow itself
           Offered ] ]                     ;   stands in the workspace; a flow takes it when its work calls
[]                                         ; traits
[]                                         ; associations
```

---

## Proposal 3: The subkinds of vision · psyche-belief › vision/belief-modules.md

COMMENT
His words: «We can even have subvariants that don't need to be in the name of the module, like: This is a vision meta design. This is a vision software design. This is a vision behavior. This is behavior design.» «Maybe you want to make a proposal and do some research on what kind of subkinds of modules exist.» Four of the five below are his. The fifth, practice, comes from the gathering of all 57 vision modules as they stand (/home/li/primary/flows/730b25/subkinds-gathering.md): many say how one kind of work is done, a commit, a build, a test, a proposal, a page, whoever does it, and that is neither a component nor the conduct of a kind of flow. A language, Ethos, Datom, Protos or Sema, is read here as a software design. The gathering also shows seventeen modules doing two kinds at once, the Flow Nexus vision above all; splitting them is a proposal of its own, after these kinds are ruled. Tentative.

ADD, after the lines of Proposal 2:
A vision module declares its subkind, which is in its metadata and not in its name. A software design says what a component or a language is to be. A behavior says how a flow of some kind conducts itself, and is given to that flow. A practice says how one kind of work is done, and is for whichever flow does that work. A behavior design says how behaviors are made, and a meta design how belief itself is made; both are given to the flows that design. A module is of one subkind.

```ethos
Library
[]                                         ; imports
[ Subkind.[ SoftwareDesign                 ; types: what a component or a language is to be
            Behavior                       ;   how a flow of some kind conducts itself
            Practice                       ;   how one kind of work is done
            BehaviorDesign                 ;   how behaviors are made
            MetaDesign ] ]                 ;   how belief itself is made
[]                                         ; traits
[]                                         ; associations
```

---

## Questions

1. Given and offered: are these the words, for a module the machine may not, or may, load by itself?
2. Are the two fields for every type, or is the subkind the vision's alone?
