Presentation.{ «Vision is divided by version» Proposal }

# Vision is divided by version

Created by Fable 5.1, alone.

### Proposal 1: Vision is divided by version · psyche-belief › intent/psyche.md

::: comment
Horizons were relative and renamed every module when one landed; a version is absolute, as the Nexuses already are.
:::

- description: A flow weighs the living's reviewed and approved words against a machine's inference, handles psyche data, or reads a vision as short-term or long-term, or decides whether a reviewed line is psyche and which level it sits at.
+ description: A flow weighs the living's reviewed and approved words against a machine's inference, handles psyche data, or reads a vision as perennial or of a version, or decides whether a reviewed line is psyche and which level it sits at.

- ## Vision is divided by horizon
+ ## Vision is divided by version

- Vision is what the living says the system is to be, and a topic's vision is divided by horizon into modules, so a flow loads the horizon its work needs. The unmarked module, vision:<topic>, is the perennial vision: it holds what is true of the topic at every horizon. vision:short:<topic> holds the compromises in force now: the short-term solutions and hacks. vision:medium:<topic> describes the system as it is to be past the compromised phase. vision:long:<topic> describes it as it is ideally to be. vision:far:<topic> holds the living's broadest idea of it, the very far, currently impractical vision, loaded by a flow that is designing that far vision.
+ Vision is what the living says the system is to be, and a topic's vision is divided by version into modules, so a flow loads the version its work needs. The unmarked module, vision:<topic>, is the perennial vision: what the topic is and is for, and what holds of it at every version, specific only where the specific holds for each. vision:<topic>:v<N> describes the system as that version is to be, whole and self-contained: the one being built is what its implementer loads, and a later one is the design of what comes after. The living's broadest idea of a topic is the perennial module's where it holds at every version, and a version's where it is specific enough to design, however distant.

- A line in a marked module is unimplemented by definition: a medium line stands because a short line is the compromise in its place, and a long line stands beyond the medium the same way. The far vision is never implemented: what comes within reach of it has already moved to long. When the medium vision is implemented, the short is irrelevant and is removed, and the horizons move up: the medium is now the short term, the long the medium, the far the long.
+ A version's module holds the compromises of that version with the rest of it, and nothing of another version. When a version retires, its module is removed; nothing is renamed.

- A medium, long or far line reaches an implementer through a proposal that moves it to the short or unmarked module with its design: the abstractions it is made of, how they compose, and the configuration the running system takes it through, shown as vision code. A proof of concept may implement the medium while the short implementation is kept, improved or fixed, so several horizons may be in implementation at once.
+ A line of a later version reaches an implementer through a proposal that moves it into the version being built, with its design: the abstractions it is made of, how they compose, and the configuration the running system takes it through, shown as vision code. Several versions may be in implementation at once, the stable one kept, improved or fixed while the next is built.

### Proposal 2: The file layout leaves the belief-modules vision · psyche-belief › vision/belief-modules.md

::: comment
The convention is intent:psyche's; the layout is guidance, in the proposal Guidance.
:::

- A context repository holds one folder per module type, each named for its type. A file is named by its subject alone, and its folder gives its type.

### Proposal 3: A module name carries its version · psyche-belief › vision/belief-nexus-v1.md

::: comment
The name gains the optional version.
:::

```ethos
-   ModuleName.{ Kind Subject.String }
+   ModuleName.{ Kind Subject.String
+                Option<Version> }
+   Version.Integer
```
