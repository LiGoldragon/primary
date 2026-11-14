Presentation.{ «Guidance» Proposal }

# Guidance

Created by Fable 5.1, on the living's words.

### Proposal 1: Three rungs, three kinds of belief · psyche-belief › vision/belief-modules.md

::: comment
The figure redrawn for the three rungs: Psyche being, Mind presence, Field becoming.
:::

```text
- flowchart TB
-     a["the living"] -- "reviews psyche proposals, line by line" --> b["Psyche: spirit, intent, vision"]
-     a -- "skims knowledge proposals" --> m
-     b -- "rules over Mind: a Mind line it contradicts is removed" --> m
-     subgraph m["Mind"]
-         direction TB
-         k["knowledge: facts verified in code"] -- "an audit for truth and currency finds a variation; it goes to" --> u["the type that holds what is unclear"]
-     end
-     m -- "rules over Field: a Field line it contradicts is removed" --> fl["Field"]
-     p["a periodic book or audit"] -- "reads it as a whole and checks it against Mind and Psyche" --> fl
```

```mermaid
+ flowchart TB
+     a["the living"] -- "reviews line by line: his will" --> p["Psyche, being: spirit, intent, vision"]
+     a -- "approves: how a thing is done now" --> m["Mind, presence: guidance"]
+     a -- "glances at a review that brings the cruxes forward" --> f["Field, becoming: knowledge, landed by the machine"]
+     p -- "rules over: a line it contradicts is removed" --> m
+     m -- "rules over: a line it contradicts is removed" --> f
```

### Proposal 2: Guidance is a kind · psyche-belief › intent/belief-modules.md

::: comment
The order gains the Mind's kind.
:::

- The module types stand in one order, highest first: spirit, intent, vision, knowledge. A module depends only on its own type or a higher one.
+ The module types stand in one order, highest first: spirit, intent, vision, guidance, knowledge. A module depends only on its own type or a higher one. Spirit, intent and vision are Psyche's, his will; guidance is Mind's, how a thing is done now, approved by him; knowledge is Field's, what the machine found, in flux.

### Proposal 3: An approved line is vision or guidance · psyche-belief › intent/psyche.md

::: comment
An approved line is placed by what it says.
:::

- Anything the living has reviewed is psyche: a line he approves is a vision statement at least, whatever module proposed it, and leaves the mind or field module it sat in. A line he has not reviewed is a machine line.
+ A line the living approves leaves the module it sat in: it is vision when it says what is wanted, and guidance when it says how a thing is done. A line he has not reviewed is a machine line.

### Proposal 4: A review brings the cruxes forward · psyche-belief › vision/review.md

::: comment
A machine-landed module passes by him for a glance; the review points to what matters.
:::

+ A review brings its cruxes forward: the lines a flow would act on differently, named first, so a glance is enough.

### Proposal 5: The belief modules · psyche-belief › modules/guidance:belief-modules.md

::: comment
A new module: what a name means, where a module lives, how one is proposed.
:::

+ ---
+ description: A belief module is named, placed or proposed.
+ dependencies: [intent:belief-modules]
+ ---

+ A module's name is its kind, its subject and, when it has one, its version, joined by colons: vision:lojix is the perennial vision of Lojix, vision:lojix:v1 its version 1. The name is one string wherever the module is named: its file, its skill, a dependency list. The modules of a repository live in one directory, modules, each file named as its module is. A change to a module is proposed as a presentation of the lines it adds and removes, under the module's path, and lands on the living's word.

```text
+ modules/vision:lojix.md       ; perennial
+ modules/vision:lojix:v1.md    ; version 1
```
