Presentation.{ «A module is its declaration, a why is short, and a notion comes first» Proposal }

# A module is its declaration, a why is short, and a notion comes first

Created by Fable 5.2.

### Proposal 1: A belief module is named by its declaration · psyche-belief › vision/belief-modules.md

- A context repository holds one folder per module type, each named for its type. A file is named by its version number, and its folders give its type and its topic.
+ A belief module is what the Nexus holds. Its name, in three fields, is given by a declaration in datom that the module's repository carries; a module is added by adding its declaration, and the file's own name carries no meaning. Git is the bootstrap database of the modules, versioned and backed up; the data in the Nexus is what counts.

```datom
+ ; the declarations a repository carries: type, topic, versions, and the file that holds the text
+ [ { Vision flow-nexus [ 0 ] «vision/flow-nexus.md» }
+   { Vision flow-nexus [ 1 ] «any-name-at-all.md» } ]
```

### Proposal 2: The why of a proposal · psyche-belief › vision/proposal.md

+ A proposal says why only where its reason could be unclear: five to twelve words, the writer's own explanation of why the change is wanted.

### Proposal 3: A notion comes before the vision · psyche-belief › vision/psyche.md

+ From words the living has not reviewed, Fable writes a notion, and Mind implements from it at once, as a proof of concept. He reviews the notion afterwards: what he approves becomes vision, and the notion is removed.
