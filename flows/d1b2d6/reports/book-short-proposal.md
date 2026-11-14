---
description: A book's source, figures and publication.
dependencies: [vision-presentation]
---

## Duties

The author supplies the complete source and its path. The bookmaker obtains custom vector figures from the Illustrator, builds and checks the whole page, publishes it, and returns its title and link for the author to give the living. Only the bookmaker publishes. A redo replaces the same edition and resolves comment threads answered by the source. The subtitle names the creating model and each helper's work.

## What the source carries

Show removed lines beside what makes them unnecessary. Show replacements as removal and addition, marking changed words. Show a new module whole at its destination; show a deleted module whole under Destroy or Archive. Show both modules whole for comparison. Show changed dependencies in front matter. A moved passage appears once, naming source and destination.

Code is complete: every name and type is declared or shown in full; each method appears with its trait and that trait's Ethos. Mark unsettled code tentative. Show rules with the code that enforces them; alternatives give the exact lines each would land. Each versioned module is self-contained and names its version once.

Proofs, tests, milestones and work sequences belong in beads. Keep source records in one unrendered `references/` file per book; archive it with the accepted landing. An account is prose with its gist in the first paragraph; the account itself shows no module and lands nothing. Mark only an actual embedded proposal as a proposal.

## Source anatomy

Begin with the Presentation line and title. A module view uses `## repo › path`; a proposal uses `### Proposal N: title · repo › path`. Detailed grammar, including multiple locations and new/deleted modules, lives in the repository documentation and checker.

One example of added, removed and moved content:

```text
- Removed line
+ Added line
::: move proposed
from: repo › old.md
to: repo › new.md

Moved passage, written once.
:::
```

The margin alone carries change colour: green added, red removed, blue moved. Text keeps the page colour and code its language colours. Proposed changes use the light shade; landed changes and reviews use the dark shade.

## Figures and publication

Every figure is headed by the module it lives in and one of three states: as it stands, proposed added, or proposed removed. These annotations are a semantic review duty. A proposed figure appears under its module path as an added line; a replaced fence is shown as removed. Sizable presentations carry several figures.

Each figure asks one question. A box is a thing or collection; an arrow is a one-way relation carrying a verb. Nearness and enclosure express kinship; top-to-bottom expresses order; colour carries its role consistently.

The Illustrator draws custom vectors preserving every source box, label and directed relation, restacking vertically for phone readability. Inspect the WHOLE drawing: meaning, endpoints, labels, enclosure, order, colour, fit and clipping. The bookmaker checks every figure's placement and the complete built page before publication.

Build with the repository builder. A successful build establishes its mechanical checks, not semantic completeness or visual fitness. Those remain the author, Illustrator and bookmaker's explicit duties.
