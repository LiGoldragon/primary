Presentation.{ «A flow is configured whole and started with what it implements» Proposal }

# A flow is configured whole and started with what it implements

Created by Fable 5.1, on the living's words.

### Proposal 1: One datom configures a flow · psyche-belief › vision/flow-nexus.md

::: comment
His words: «a flow nexus version that allows us to atomically configure flows, new flows, old flows». A permaflow's configuration is one value, set whole in one datom and replaced the same way; a field is never set apart from the rest, so no flow is ever half-configured. Version 1 has this as Define; this is the same rule for the version running.
:::

+ A permaflow's configuration is one datom: its address, its root, its modules, its kind, its tools, its continuity and its purpose, set whole and replaced whole. A permaflow being configured is one or the other, the old or the new, never a mixture; a flow of it started after the replacement runs on the new, and a flow running on the old is refreshed to take it.

```datom
+ Configure.Permaflow.{ { Mind semaV0 Opus } None
+                       [ { Spirit core } { Spirit ghost } { Intent design } ]
+                       [ { Role implementer } { Vision sema-v0 } ]
+                       Regular Default Maintained
+                       «Implements Sema version 0 as vision:sema-v0 states it.» }
```

### Proposal 2: The default modules are one configuration value · psyche-belief › vision/flow-nexus.md

::: comment
What every flow gets is said once, in the Nexus, so a permaflow's own list names only what is its own. Version 1 has it; the version running gets it the same way.
:::

+ The Flow Nexus holds the default modules as one configuration value: the modules every flow starts with, composed before each permaflow's own. A permaflow's list names only what is its own.

```datom
+ Configure.DefaultModules.[ { Spirit core } { Spirit ghost } { Intent context } { Intent design } { Intent main-flow } { Intent models } { Intent energy }
+                            { Knowledge flow-messaging } { Knowledge search } { Knowledge vocabulary } { Vision model-roles } { Vision aspects } ]
```

### Proposal 3: A launch names what the flow implements · psyche-belief › vision/flow-nexus.md

::: comment
His words: «easily use it to start a flow, especially for implementing things, that has the module that it needs, like the right vision for what it's implementing, and the basic modules that all flows need, anything that touches implementing but nothing else». A launch carries its beliefs, so an implementing flow needs no configuration step: the default modules, a role, and the vision it implements, with that vision's dependencies, which the front matter already names. The implementing modules are a role module's dependencies, so the set is one name and lives in a belief module, not in the Nexus.
:::

+ A launch may carry the beliefs of the flow it starts: a role and the visions it is to implement. The Nexus composes the default modules, the role with its dependencies, and each vision with its dependencies, and starts the flow on them, so an implementing flow is started in one command with the vision it implements, the modules implementing needs, and nothing else.

```ethos
+ Launch.LaunchRequest
+ LaunchRequest.{ Address Option<Beliefs> Brief.String }   ; absent: the permaflow's configured modules
+ Beliefs.{ Role.ModuleName Visions.Vector<ModuleName> }   ; a role, and what the flow implements
```

```datom
+ Launch.{ { Mind semaV0 Opus }
+          Some.{ { Role implementer } [ { Vision sema-v0 } ] }
+          «Implement the reading of a module into SemaZero, as vision:sema-v0 states it.» }
+ Launched.9af746
```

```mermaid
+ flowchart TB
+     d["default modules: one Nexus value"] -- "composed first" --> f["the flow's start set"]
+     r["role:implementer, with its dependencies"] -- "composed next" --> f
+     v["the vision named, with its dependencies"] -- "composed last, highest in the first prompt" --> f
+     f -- "starts" --> i["an implementing flow: the basics, implementing, its vision, nothing else"]
```

### Proposal 4: The implementer role · mind-belief › role/implementer.md

::: comment
The modules that touch implementing and nothing else, as one role whose dependencies they are. A new module, shown whole.
:::

````markdown
+ ---
+ description: A Mind flow implements a vision as it stands: it writes the code, builds it, tests it and lands it, and brings up as a question what the vision leaves open.
+ dependencies: [vision-mind-aspect, intent-anatomy, intent-conversion, intent-configuration, vision-committing, vision-testing, knowledge-nix-rust-builds, knowledge-ethos, knowledge-orchestrate]
+ placement: user
+ ---

+ An implementer reads the vision it was started with as the thing to build, whole, and builds the smallest shape that is that vision. What the vision leaves open goes up as a question; what it states is not redesigned. The work is green on its whole check before it is landed.
````

### Proposal 5: How an implementing flow is started · mind-belief › knowledge/starting-flows.md

::: comment
His words: «with maybe a bit of a guide on how to do that». A new module, shown whole.
:::

````markdown
+ ---
+ description: How a flow is started for a piece of work: which address, which role, which vision, and the one command.
+ dependencies: [knowledge-flow-messaging]
+ ---

+ A flow for a piece of work is started with one Launch: an address, the role of the work, the vision it implements, and a brief of a small paragraph. The Nexus adds the default modules and each module's dependencies; the launch names nothing else.

+ - The address: the aspect of the work, Mind for implementing; a topic named for the thing implemented; the cheapest model that does the job, Opus or higher for a Nexus or the infrastructure under one, Sonnet for plain work.
+ - The role: `{ Role implementer }` for implementing; another role for another kind of work.
+ - The visions: the module the work implements, as `{ Vision <subject> }`; its dependencies come with it, so a version module brings the perennial one.
+ - The brief: what is to be built, where it is, and what done looks like.

+ ```sh
+ flow 'Launch.{ { Mind semaV0 Opus } Some.{ { Role implementer } [ { Vision sema-v0 } ] } «Implement the reading of a module into SemaZero, as vision:sema-v0 states it; green on the whole check; land on sema-v0-opus.» }'
+ ```

+ A flow for the same topic again is the same address: the permaflow continues, and the launch wakes or refreshes it with the new brief.
````
