<!-- to-the-living:start -->
Presentation.{ «CriomOS gets its vision» }

# CriomOS gets its vision

```
+------------------------------+
| package / flake input /      |
| option                       |
+------------------------------+
        | evaluates to
        v
+------------------------------+
| store path                   |
+------------------------------+
        | used by
        v
+------------------------------+
| Nix module                   |
| (names no store path)        |
+------------------------------+
```

### Proposal 1: CriomOS gets its vision · psyche-context › vision/criomos.md, a new file

+ ---
+ description: CriomOS, its hosts, fixes, hardware, services, Nix code or desktop, is being designed or judged.
+ dependencies: [vision-nix-builds]
+ ---
+
+ ## CriomOS
+
+ CriomOS is a declarative operating system: nobody edits a file on a host.
+
+ A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.
+ Every hotfix in place is removed and replaced by that fix.
+
+ CriomOS is made more modular; an anatomy of it shows what should be taken out.
+
+ ## Nix code
+
+ Every store path in Nix code is the output of evaluating a package, a flake input or an option; Nix code never names a store path.
+
+ ## Hardware
+
+ CriomOS has a hardware type, so that it supports several kinds of hardware, the Librem 5 Linux smartphone among them; a module may be gated on it.
+ A fix that only some hardware needs is a value in the cluster data, marked by the chip or part that makes it necessary.
+ A library reads the cluster's list of its hardware and answers, by processor, model and variant, which fixes a computer needs.
+
+ ## Harnesses
+
+ The harnesses and their desktop apps are kept stock in at least one version, under their ordinary executable names.
+
+ ## Services
+
+ A new service lives in CriomOS.
+ A service is updated by bringing it up at its latest version.
+
+ ## Desktop
+
+ A new artifact does not open a browser tab on its own.

Ruling: land, amend, or reject.

### Proposal 2: a running endpoint survives because its input stays pinned · field-context › compensation/update.md

  Retain an exact migration artifact that identifies every native consumer in scope and its resolved role mapping. It must prove that none resolves predecessor stable. Source declarations, staged paths, successful evaluation, or intended configuration do not prove migration.
  
- After the migration gate, promote by mapping stable to the already-running Next endpoint. Preserve its process, service, socket, state root, client route, and running sessions. Do not restart, recreate, rename, move, copy, or share its mutable state as part of promotion.
+ After the migration gate, promote by mapping stable to the already-running Next endpoint. A running endpoint survives an activation because the input that built it stays pinned.
  
  Create separate Next only after promotion. Give it a distinct process, state root, socket, and client route.

Ruling: land, amend, or reject.

### Proposal 3: the destroy-or-archive line leaves compensation · field-context › compensation/book-crystallization.md

  A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject. A skill line in the author's brief shows where a statement lands, never what it says; the brief marks machine-skill text as the machine's. A count or date claim about the records is made only when the author has witnessed it.
  
- A proposal to destroy or archive a record renders unmistakably apart from a landing: its own colour and a Destroy or Archive mark on the record it removes.
- 
  Before publishing, reconcile the relevant current direction and exclude what the living has voided. A new edition carries only what is unruled or changed since the living last read it; what he approved is landed, not shown again.

Ruling: land, amend, or reject.

### Proposal 4: how a removed record shows is open · mind-context › inquiry/book-record-removal.md, a new file

+ ---
+ description: A book proposes to destroy or archive a whole record, and how that shows is not settled.
+ dependencies: [vision-book]
+ ---
+
+ A book shows a line removed in red and a line added in green. Whether a whole record that is destroyed or archived shows apart from a removed line is open.
+
+ 1. Does a destroyed or archived record show as its lines removed in red, like any removal, or in a colour of its own?
+ 2. Does it carry a Destroy or Archive mark, so that the living sees whether its words are kept in the archive or gone?

Ruling: land, amend, or reject.

### Proposal 5: a module depends only on its own level or a higher one · psyche-context › vision/context-modules.md

  A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.
+ 
+ ## A module depends only on its own level or a higher one
+ 
+ A module depends only on modules of its own level or a higher one. Compensation may depend on vision or knowledge; vision never depends on compensation.

Ruling: land, amend, or reject.

### Proposal 6: four front matters stop depending on a lower level · psyche-context › vision/x11.md, intent/testing.md, intent/psyche-interaction.md, spirit/core.md

Vision x11 depended on compensation, a lower level; it now depends on the CriomOS vision. Intent testing and intent psyche-interaction depended on compensation; they now keep only what is at their level or above. Spirit core depended on compensation; it keeps only knowledge-vocabulary, subject to question (a).

  description: A CriomOS display or graphical-session choice touches X11.
- dependencies: [compensation-operating-system]
+ dependencies: [vision-criomos]

  description: A proof of concept is about to be tested and where it runs must be chosen.
- dependencies: [compensation-testing, vision-horizon]
+ dependencies: [vision-horizon]

  description: A main flow hears the living and must decide whether to relay it.
- dependencies: [compensation-psyche-interraction]
+ dependencies: []

  description: Every task.
- dependencies: [compensation-behavior, compensation-correction, knowledge-vocabulary, compensation-book-crystallization]
+ dependencies: [knowledge-vocabulary]

Ruling: land, amend, or reject.

### Proposal 7: question (a), does spirit rank above knowledge · psyche-context › spirit/core.md

Spirit is the highest level, the words every task begins from. Knowledge holds facts checked in code. If knowledge ranks below spirit, then by the rule in proposal 5 spirit may not lean on it, and spirit/core.md drops its last dependency. If knowledge ranks with spirit or above it, the line stays as proposal 6 leaves it, and this proposal is rejected.

  description: Every task.
- dependencies: [knowledge-vocabulary]
+ dependencies: []

Ruling: land, amend, or reject.

### Proposal 8: question (b), where does inquiry rank against vision · psyche-context › vision/crystallization.md

Inquiry holds what is still unclear, and vision holds what the living has decided. If inquiry ranks below vision, vision may not lean on it, and the dependency on the inquiry about crystallization goes. If inquiry ranks with vision or above it, the line stays and this proposal is rejected.

  description: A crystallization proposal is composed or judged, or a vision impurity is met in a psyche record.
- dependencies: [inquiry-psyche-crystallization]
+ dependencies: []

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
