Presentation.{ «The active projects, and an example repository beside a module» Proposal }

# The active projects, and an example repository beside a module

Created by Fable 5.1, on the living's words to Psyche core Opus.

### Proposal 1: An example repository · psyche-belief › vision/belief-modules.md

::: comment
His words: «create a knowledge module on how to do this that is short and to the point, and explains really the main points that then any model can figure out the rest from. … we could have an example repository … that we can then marry with our belief modules.» The module carries the principles; the repository carries one complete, working instance of them.
:::

+ A knowledge module on a stack is short: the main points, from which a model works out the rest. It may be married to an example repository, a small, complete, working instance of what the module says, named in the module's front matter; the module carries the principles and the repository shows them whole, and when one changes the other follows in the same change.

### Proposal 2: The list of active projects · psyche-belief › knowledge/active-projects.md

::: comment
His words: «we agreed on a list, so maybe we should keep that list somewhere so that we don't waste our effort maintaining code we're not even using.» I do not hold the conversation where the list was agreed; this one is read from the lanes running now, for him to amend. A new module, shown whole.
:::

```markdown
+ ---
+ description: Which repositories are active: the ones worked on and run now, where effort on build, tests and upkeep is spent; every other repository is left as it is.
+ dependencies: []
+ ---
+
+ The active repositories, under github.com/LiGoldragon:
+
+ - protos, datom-codec, signal, meta-signal: the parsing and wire layers
+ - ethos-zero: the ethos generator
+ - flow: the Flow Nexus and its clients
+ - herdr-nexus, belief-nexus: the Nexuses of the complex, version 1
+ - sema: version 0
+ - criomos: the hosts
+ - psyche-belief, mind-belief, field-belief: the belief modules
+
+ A repository not on this list is not maintained; a change wanted in it begins by putting it on the list.
```
