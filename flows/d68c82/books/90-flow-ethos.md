<!-- to-the-living:start -->
Presentation.{ «Flow ethos» }

# Flow ethos

### Proposal 1: psyche-context › vision/flow.md

  Flow is the Nexus that manages flows. A flow is one run of a metaflow; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

- Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.
+ Flow is for starting flows cheaply: clean simplified flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system.

Ruling: land, amend, or reject.

### Proposal 2: psyche-context › vision/flow.md

  Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.

+ ## A flow is specified whole, in Ethos
+
+ A flow is specified whole, in Ethos: its system prompt, which is the whole base context; how it works; its default context modules; and its variations. Flow controls the whole system prompt of every flow it starts. The specification is a domain-specific language in Ethos.
+
+ The simplified flow is one variant of the specification: a judgment-only call with no tools and no messenger, whose response is its message. It goes back and forth a few times with a supervising flow, which has the tools and finds out for it what it asks.
+
+ The specification, with its complete worked example, is vision:flow-ethos.

```
+--------------------------------------------+
| a flow, specified whole in Ethos           |
+--------------------------------------------+
    |         |          |           |
    | holds   | holds    | holds     | holds
    v         v          v           v
+--------+ +-------+ +---------+ +------------+
| system | | how it| | default | | variations |
| prompt | | works | | modules | |            |
+--------+ +-------+ +---------+ +------------+
                                       |
                                       | includes
                                       v
                               +------------+
                               | simplified |
                               | flow       |
                               +------------+
```

Ruling: land, amend, or reject.

### Proposal 3: psyche-context › vision/ethos.md

  Terseness is in the low amount of noise, never in shortened words.

+ ## A specification groups its items by variant
+
+ A specification groups its items by variant: one vector for each variant, never one vector whose items each name theirs. A Signal's queries are one vector and its responses the next; a flow specification's main flows, subflows and simplified flows are three vectors the same way.
+
+ Grouping saves repetition, so the syntax is succinct, dense and high in signal.
+
+ Not so good: one vector, each item naming its variant. Flow is an enum of three variants: Main, a run of a metaflow; Sub, a named role; Simplified, a judgment-only call. Each carries the Models it may run on, a set written as a vector until Ethos has a set, and its Effort. Effort is how hard the model thinks, and has three variants: Low, Medium and High. Flows is a struct, so its Datom has no head.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Models.Vector<Model>
+   Effort.[ Low Medium High ]
+   Flow.[ Main.{ Models Effort }
+          Sub.{ Models Effort }
+          Simplified.{ Models Effort } ]
+   Flows.{ Vector<Flow> } ]
+ []
+ []
```
```datom
+ { [ Main.{ [ opus ] Medium }
+     Sub.{ [ sonnet ] Medium }
+     Sub.{ [ haiku ] Medium }
+     Simplified.{ [ fable ] Medium } ] }
```
+
+ Good: one vector for each variant. Main, Sub and Simplified are each their own struct, and Flows holds a vector of each, in that order. The variant is never written in the Datom, because the vector it sits in says it.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Models.Vector<Model>
+   Effort.[ Low Medium High ]
+   Main.{ Models Effort }
+   Sub.{ Models Effort }
+   Simplified.{ Models Effort }
+   Flows.{ Vector<Main> Vector<Sub>
+           Vector<Simplified> } ]
+ []
+ []
```
```datom
+ { [ { [ opus ] Medium } ]
+   [ { [ sonnet ] Medium }
+     { [ haiku ] Medium } ]
+   [ { [ fable ] Medium } ] }
```

```
+--------------------------------------------+
| a specification's items                    |
+--------------------------------------------+
        |                       |
        | are grouped into      | are each given
        v                       v
+---------------+      +-------------------+
| one vector    |      | one vector, each  |
| for each      |      | item naming its   |
| variant       |      | variant           |
+---------------+      +-------------------+
        |                       |
        | yields                | yields
        v                       v
+---------------+      +-------------------+
| dense syntax  |      | repeated names    |
+---------------+      +-------------------+
```

Ruling: land, amend, or reject.

### Proposal 4: psyche-context › vision/flow-ethos.md, a new file

+ ---
+ description: A flow is specified, or a specification is judged, in Ethos: its system prompt, how it works, its default context modules and its variants.
+ dependencies: [vision-flow, vision-ethos, vision-datom]
+ ---
+
+ ## A flow is a value of one specification
+
+ A flow is specified whole, in Ethos. The specification is the Library below: its system prompt is the modules an entry names, how it works is the entry's models, effort, tools and permission, its default context modules are the modules the entry carries, and its variations are its variants. A flow is one value of the specification, written in Datom.
+
+ The specification has three variants of flow: the main flow, the subflow and the simplified flow. Each is its own struct, and Flows groups them by variant: a vector of main flows, then a vector of subflows, then a vector of simplified flows. Each variant carries only the fields it has.
+
```ethos
+ Library
+ []
+ [ Module.String
+   Modules.Vector<Module>
+   Model.String
+   Models.Vector<Model>  ; a set, as a vector
+   Name.String
+   Tool.String
+   Tools.Vector<Tool>
+   Topic.String
+   Aspect.[ Psyche Mind Field ]
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Effort.[ Low Medium High Xhigh ]
+   Permission.[ Restricted Unrestricted ]
+   Address.{ Aspect Topic Layer }
+   Callers.[ Any Only.Vector<Address> ]
+   Main.{ Address Models Effort
+          SystemModules.Modules
+          UserModules.Modules }
+   Sub.{ Name Models Effort Permission
+         Modules Tools Callers }
+   Simplified.{ Name Models Effort Modules
+                Supervisor.Address }
+   Flows.{ Vector<Main> Vector<Sub>
+           Vector<Simplified> } ]
+ []
+ []
```
+
+ ## What each type and variant is
+
+ Flows is the one struct a specification is. It is not a variant, so its Datom has no head: braces holding the three vectors, in order.
+
+ The three variants of flow:
+
+ - Main: the flow of a metaflow. Its Address says which metaflow: an Aspect, a Topic and a Layer. SystemModules are composed into its system prompt, and UserModules into its first user message.
+ - Sub: a named role run as an independent flow under its own system prompt. Its Modules are that prompt, its Tools are what it may use, its Permission says whether it may change things, and its Callers say who may start it.
+ - Simplified: a named judgment-only call. It has no tools and no messenger, so it has no field for them; its response is its message. Its Supervisor is the address of the one flow it answers to, which has the tools and finds out for it what it asks.
+
+ The fields every variant shares:
+
+ - Models: the set of models a flow may run on, written as a vector of Model; one flow can be served by the same model with and without the million context. A Model is the model's name as the harness gives it.
+ - Effort: how hard the model thinks. Its variants are Low, Medium, High and Xhigh, from least to most.
+ - Modules: the context modules composed together, in order, each a Module name.
+
+ The enums, each variant stated:
+
+ - Aspect: Psyche, the aspect the living reviews, of spirit, intent and vision; Mind, of knowledge and inquiry; Field, of the machine-generated compensation.
+ - Layer: Primary, Secondary, Tertiary and Quaternary, the four layers every aspect has.
+ - Permission: Restricted, a subflow that reads and reports and does not edit or write; Unrestricted, a subflow that may.
+ - Callers: Any, a subflow any flow may start; Only, carrying the vector of Address that alone may.
+
+ The plain strings: a Topic is a camelCase word, core by default; a Name is a camelCase word naming a role; a Tool is a tool's name as the harness gives it.
+
+ ## A complete worked example
+
+ One main flow, two subflows and one simplified flow, each in the vector of its variant. The values are an example, not the deployed roles.
+
```datom
+ { [ { { Psyche core Secondary }
+       [ claude-opus-5-5
+         «claude-opus-5-5[1m]» ]
+       Medium
+       [ spirit-core intent-context
+         intent-main-flow vision-book
+         compensation-book-crystallization ]
+       [] } ]
+   [ { book [ sonnet ] Medium Unrestricted
+       [ spirit-core intent-context
+         role-book-publishing-procedure
+         vision-book
+         compensation-book-crystallization ]
+       [ Read Bash Agent Artifact ]
+       Only.[ { Psyche core Secondary } ] }
+     { illustrator [ sonnet ] Medium Restricted
+       [ spirit-core intent-context
+         role-illustrator-faithfulness
+         role-illustrator-svg
+         compensation-illustration ]
+       []
+       Any } ]
+   [ { fableDesign
+       [ claude-fable-5-1
+         «claude-fable-5-1[1m]» ]
+       Medium
+       [ spirit-core intent-context
+         vision-book ]
+       { Psyche core Secondary } } ] }
```
+
+ The main flow is the first vector's one entry. Its Address is Psyche, core, Secondary. It may run on claude-opus-5-5 or on the same model with the million context, at Medium effort. Five modules are composed into its system prompt, and none into its first user message, so its UserModules is the empty vector.
+
+ The subflows are the second vector's two entries. The book subflow may run on sonnet at Medium effort, is Unrestricted, composes five modules, uses Read, Bash, Agent and Artifact, and only the Psyche core Secondary metaflow may start it. The illustrator subflow is Restricted, has no tools, so its Tools is the empty vector, and Any flow may start it.
+
+ The simplified flow is the third vector's one entry, named fableDesign. It may run on claude-fable-5-1 or on the same model with the million context, at Medium effort, composes three modules, and answers to the Psyche core Secondary flow. It has no tools field.

```
+--------------------------------------------+
| Flows                                      |
+--------------------------------------------+
     |            |             |
     | groups     | groups      | groups
     v            v             v
+----------+ +----------+ +------------+
| main     | | sub      | | simplified |
| flows    | | flows    | | flows      |
+----------+ +----------+ +------------+
     |            |             |
     | compose    | compose     | compose
     v            v             v
+--------------------------------------------+
| default context modules                    |
+--------------------------------------------+
```

```
+--------------------------------------------+
| supervising flow, which has the tools      |
+--------------------------------------------+
     |                          ^
     | sends context            | answers with
     | and a request            | its response
     v                          |
+--------------------------------------------+
| simplified flow: no tools, no messenger    |
+--------------------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 5: mind-context › inquiry/flow-ethos.md, a new file

+ ---
+ description: The set in Ethos, a simplified flow's reply, where default modules live, how a variation overrides, which fields each variant has and where specifications live are unresolved.
+ ---
+
+ ## A set in Ethos
+
+ Ethos has no set: its intrinsic types are String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result and Self. A flow's models are a set, and flow-ethos writes Models as a vector of Model, in which order and a repeat carry no meaning. How is a set declared in Ethos and written in Datom? What would settle it: the specification of flow-ethos decoded by datom-codec with Models as a set.
+
+ - Alternative a: a Set intrinsic, written as a bracket as a vector is, and refused by the reader when an item repeats. It touches the Ethos reader, the generation of Rust, and datom-codec.
+ - Alternative b: the vector stays, and a repeat is refused by whatever consumes the specification. Ethos and datom-codec are unchanged, and the type does not say it is a set.
+
+ Tools and the Only vector of Callers are sets in the same way.
+
+ ## What a simplified flow answers
+
+ The living said its response is its message, questions and designs, and maybe a third thing. Is the reply a closed type, or only text? What would settle it: one simplified flow run to completion with each alternative. The third kind of reply is unknown.
+
+ - Alternative a: a closed reply, one variant for each kind.
+
```ethos
+ Library
+ []
+ [ Reply.[ Question.String
+           Design.String ] ]
+ []
+ []
```
+ - Alternative b: no type; the response is the message, as text.
+
+ ## Where the default modules live
+
+ Where do the default modules of a variant live, so they are not copied into every entry? What would settle it: a specification with both alternatives, and the number of lines each needs for the same flows.
+
+ - Alternative a: the specification opens with the default modules, and each entry adds to them.
+
```ethos
+ Library
+ []
+ [ Module.String
+   Modules.Vector<Module>
+   Model.String
+   Models.Vector<Model>
+   Main.{ Models Modules }
+   Flows.{ Modules Vector<Main> } ]
+ []
+ []
```
+ - Alternative b: named groups of modules, and an entry names the groups it takes.
+
```ethos
+ Library
+ []
+ [ Module.String
+   Modules.Vector<Module>
+   Model.String
+   Models.Vector<Model>
+   Name.String
+   Group.{ Name Modules }
+   Main.{ Models Vector<Name> }
+   Flows.{ Vector<Group> Vector<Main> } ]
+ []
+ []
```
+
+ ## How a variation overrides a default
+
+ How does a variation by layer, aspect or model override its default? What would settle it: the same set of variations written three ways.
+
+ - Alternative a: each entry carries its variations.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Models.Vector<Model>
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Variation.{ Layer Models }
+   Main.{ Models Vector<Variation> }
+   Flows.{ Vector<Main> } ]
+ []
+ []
```
+ - Alternative b: the variations are a vector of their own, grouped like the variants.
+
```ethos
+ Library
+ []
+ [ Model.String
+   Models.Vector<Model>
+   Layer.[ Primary Secondary Tertiary
+           Quaternary ]
+   Variation.{ Layer Models }
+   Main.{ Models }
+   Flows.{ Vector<Main>
+           Vector<Variation> } ]
+ []
+ []
```
+ - Alternative c: nothing overrides; every variation is a full entry in its variant's vector. Conditions inside a module's text stay as they are.
+
+ ## Which fields each variant has
+
+ - Does a main flow carry tools and permission, as a subflow does in flow-ethos, or does it not? One flow of each variant started from its entry alone would settle it.
+ - Is the harness a field of an entry, or derived from the model? A model served by both harnesses would settle it.
+
+ ## Where specifications live and are generated
+
+ - Models are named today in Curriculum's roles.datom, in Primary's config/main-flow EDN files and in SKILL_VARIABLES.md. Does one specification replace them, and does the layer's model, which Flow configures, move into it? Starting one flow of each variant from the one specification, with the other sources removed, would settle it.
+ - In which repository does the specification live? The living said it is a different repository from the cluster data.
+ - Who writes the agent files? Alternatives: Curriculum reads the specification and renders the agent files; or Flow reads the specification and starts every flow itself, with no agent file.

```
+--------------+ +-------------+ +-------------+
| roles.datom  | | main-flow   | | SKILL_      |
| (Curriculum) | | EDN         | | VARIABLES   |
|              | | (Primary)   | |             |
+--------------+ +-------------+ +-------------+
       |                |               |
       | names          | names         | names
       v                v               v
+--------------------------------------------+
| the model of a flow                        |
+--------------------------------------------+
       ^
       | would name once
       |
+--------------------------------------------+
| one flow specification                     |
+--------------------------------------------+
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
