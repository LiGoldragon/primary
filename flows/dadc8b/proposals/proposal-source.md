Presentation.{ «How a proposal source is marked» Proposal }
# How a proposal source is marked

Created by Opus 5.5, who wrote this from the builder's code and tests.

### Proposal 1: How a proposal source is marked · mind-belief › knowledge/book.md, and mind-belief › knowledge/proposal-source.md, a new file

**Comment** The source-form lines leave knowledge:book, which keeps publishing alone, and open the new module knowledge:proposal-source; around them the new module says how each change is marked. The example leaves with them, replaced by the marks, since the checker refuses a `:::` move container.

+ ---
+ description: How a proposal source marks its changes so the builder renders them.
+ dependencies: [vision-presentation, vision-proposal]
+ ---
+

~ ## Source anatomy
~
~ The source begins with its Presentation line and its title. A module view is headed `## repo › path`; a proposal is headed `### Proposal N: title · repo › path`. The builder's documentation and checker hold the rest of the grammar.
~

+ ## The marks
+
+ A change is lines in the body of the source, each opening with its sign and a space: `+ ` for a line added, `- ` for a line removed, `+` or `-` alone for a blank line inside the run. A line replaced is its removed line followed by its added line, and the builder marks only the words that changed. A new module is headed `### Proposal N: title · repo › path, a new file`. A paragraph opening with `**Comment**` is the machine's word on the lines after it.
+
+ A line moved between modules opens with `~ `, in a proposal headed with both modules, `· repo › from.md, and repo › to.md`; the passage is written once.
+
+ A figure is its own `mermaid` fence, every line of it under the sign, the fence marks included; the bookmaker draws it as an SVG and the page shows only the drawing.
+
+ ```text
+ + ```mermaid
+ + flowchart TB
+ +     a["a"] -- "to" --> b["b"]
+ + ```
+ ```
+
+ A code block is its own fence labelled with its language, every line under the sign; its lines fit in 52 columns.
+
+ ```text
+ + ```ethos
+ + Waking.[ Woken Asleep ]
+ + ```
+ ```
+
+ A change never stands inside a `diff` fence: the builder reads such a fence as one code block, and the prose, figures and code in it are lost.

- One example of a line added, a line removed and a passage moved:
-
- ```text
- - Removed line
- + Added line
- ::: move proposed
- from: repo › old.md
- to: repo › new.md
-
- Moved passage, written once.
- :::
- ```

### Proposal 2: How a proposal source is marked · CriomOS-home › modules/home/profiles/min/flow-nexus-config/metaflows.datom

**Comment** Every permaflow whose modules hold vision:proposal gets knowledge:proposal-source beside it: Psyche core Primary and Secondary, Psyche codexManager, audit, garbageTests and flowAudit Secondary, and Mind versionOne, beliefNexus and obsidian, Primary and Secondary.

- ```datom
- [ … vision:proposal … ]
- ```
+ ```datom
+ [ … vision:proposal
+   knowledge:proposal-source … ]
+ ```
