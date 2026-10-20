<!-- to-the-living:start -->
Presentation.{ «Flow: context modules and the prompt, 3rd edition» }

# Flow: context modules and the prompt, 3rd edition

## Proposal 1: psyche-context › skills/vision-context-modules.md

+ The role module is a type of its own: it carries a flow's role.
+ In the short term every flow sees all skills the same way, and a role module is not loaded as a harness skill.
+ What is about a topic rather than a role goes in a regular module.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-context-modules.md

+ A subagent definition is a data object, specified in Ethos, that says which modules go where.
+ The subagent's payload is not in its definition: the definition names the role module and the other modules, and the place each one goes.
+ Its model choice and its permission are Curriculum's role types, imported in place.

```ethos
+ Library
+ []          ; imports
+ ; a subagent: its name, its role,
+ ;   its model and effort, what it
+ ;   may do, and its modules
+ [ SubagentDefinition.{
+     SubagentName.String
+     RoleName.String
+     curriculum:ModelChoice
+     curriculum:Permission
+     Vector<ModulePlacement> }
+   ; one module, and where it goes;
+   ;   OnDemand, as a harness skill
+   ModulePlacement.{
+     ModuleName.String
+     Placement.[ SystemPrompt
+                 FirstPrompt
+                 OnDemand ] } ]
+ []          ; traits
+ []          ; associations
```

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-flow.md

- A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+ A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+ The module registry is keyed by subaspect and topic, and keeps for each module its source and its path inside that source.
+ The registry is changed only through the meta signal.
+ Every context module is indexed in such a registry.
+ Keeping each source's hash, and checking it as each query comes in, is a long-term goal, ignored until the hashes can be updated efficiently on every edit.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › vision/ethos.md

- ## Flow, a current best example
- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+ ## Flow's ethos
+ Flow's ethos lives in the flow-ethos module, which carries the code.
+ Chronos is meant to be the first golden example, from which Flow is implemented properly.

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › skills/vision-nexus.md

+ A Nexus's vision stands in one module, and its code, its ethos, in a module of its own.
+ When the code module grows too big, it parts along the code: signal first, then memory, then one module for the rest.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › vision/ethos.md

+ ## Inline imports
+ A type is declared where it is used, and a type from a source is imported in place: that is an inline import.
+ A name with a capital first letter and no source is pulled directly from the core built-ins, declared in the core library of the language.
+ A name behind a lowercase source is pulled from that registry name, which depends on the Ethos environment loaded.
+ A registry of manifests says where every library lives, the core library and each environment's own.

```ethos
+ Library
+ []          ; imports
+ ; Count, a core built-in;
+ ;   Topic, Name from the
+ ;   registry name custom
+ [ Count.Integer
+   Topic.custom:Name ]
+ []          ; traits
+ []          ; associations
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
