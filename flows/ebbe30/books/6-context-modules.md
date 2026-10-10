<!-- to-the-living:start -->
Presentation.{ «Context modules» }

A context module is one piece of the text a flow
is made of. Where each piece enters:

```
   skills ──► Flow ──► the flow's context
                │
      ┌─────────┼──────────────┐
 system prompt  first prompt   loadable
 (replaces the  (the brief,    (by name, when
  harness's)     the launch)    a situation calls)
```

The placements and the role below are design.
Which placements are in production differs per
harness; a system prompt of our own is in
development, not yet in production.

## 1. Placements and the role

`psyche-skills/skills/vision-context-modules.md`, a new file.

```diff
+ ---
+ description: A context module, its placement,
+   or a launch's selection of modules is designed
+   or judged against what the living wants.
+ dependencies: [vision-flow]
+ ---
+
+ Learning and adapting take place by changing
+ context modules.
+
+ ## Placements
+
+ We want a module to reach a flow in one of three
+ places. The system prompt replaces the harness's
+ own prompt. The first prompt is the launch turn:
+ the brief, the first task of that flow. Loadable
+ modules are loaded by name when a situation calls.
+
+ ## A role
+
+ A module is named by its type and its name; Flow
+ maps each name to its path. A role is one record
+ naming, for each placement, its modules by type;
+ its model is Flow's declaration. Flow inserts
+ those modules in their places.
+
+ ## Sources
+
+ bad807 contextModules
+ aa887c contextModules
+ edf227 contextModules
+ dea0ba contextModules
+ dea0ba systemPrompt
+ d4ae97 contextModules
```

Distils flows/edf227/vision/contextModules.md, 2026-10-03; flows/dea0ba/vision/systemPrompt.md and contextModules.md, 2026-10-03; flows/d4ae97/vision/contextModules.md, 2026-10-07; flows/bad807/vision/contextModules.md, 2026-10-04; flows/aa887c/vision/contextModules.md. The model clause follows psyche-skills/skills/vision-model-roles.md, lines 69 to 71.

**Ruling 1.** (a) Land the file as shown. (b) Amend by line.

## 2. Small proposals, and what is an impurity

`mind-skills/skills/operation-psyche-distillation.md`, after line 25, and a Sources section at the end.

```diff
@@ after line 25 @@
+ A distillation proposal is small and
+ conservative: it stays general and infers
+ little. It is accepted whole or not at all.
+ An order, an instruction for a situation, or an
+ intervention is a vision impurity; distillation
+ dissects it out.
@@ end of file @@
+
+ ## Sources
+
+ bad807 distillation
```

Distils flows/bad807/vision/distillation.md, 2026-10-04. The impurity follows psyche-skills/skills/vision-distillation.md, line 8.

**Ruling 2.** (a) Land as shown. (b) Amend by line.
<!-- to-the-living:end -->
