Presentation.{ «The compact form» Proposal }

# The compact form

Created by Fable 5.1, alone.

### Proposal 1: The compact form · psyche-belief › vision/datom.md

::: comment
A third written form, after bare and guillemets in "Strings", for the places outside datom that take one word: a file name, a skill name, a unit name. A struct whose every position is bare is written as its positions joined by colons, and read back by the type as any datom is. A module name is already written so. Tentative in its casing: a variant lowercased, since the position knows it is one.
:::

+ The compact form is for a place outside datom that takes one word, a file name, a skill name or a unit name: a struct whose every position is bare is written as its positions joined by colons, and is read back in a position expecting its type as any datom is. A variant may be written lowercase in it, since the position knows it is a variant; an absent Option is an absent segment.

```datom
+ { Psyche core Fable }        ; the struct
+ psyche:core:fable            ; its compact form
+ { Vision lojix Some.1 }      ; a module name
+ vision:lojix:v1              ; its compact form
```

### Proposal 2: A flow reads its modules through the CLI · psyche-belief › vision/belief-nexus-v1.md

::: comment
Version 0 of the Belief Nexus, to be renumbered so. The harness needs one file, the system prompt; every other module a flow reads through the Belief CLI, and the skills directory is a harness legacy the Nexus can leave. Added after the first paragraph.
:::

+ Furnishing writes the one file the harness must have, the system prompt. Every other module a flow reads when it needs it, through the Belief CLI, by name; a flow's on-demand modules are what it may read, listed in its first prompt, and a skills directory is written only for a harness that cannot read otherwise.

```sh
+ belief main 'Read.{ Vision lojix Some.1 }'
```
