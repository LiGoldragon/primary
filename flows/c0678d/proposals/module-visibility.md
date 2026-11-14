# A module has a visibility

Created by Fable 5.1, alone.

### Proposal 1: A module has a visibility · psyche-belief › vision/belief-nexus-v1.md

::: comment
In "Library": a module is more than its name. It is a record of the Belief Nexus, holding its name, its placement and its visibility: who may list it and load it. A module composed by a definition alone, the one that tells a Claude flow it has no Artifact tool among them, is listed to nobody and loadable by no harness; it reaches a flow only through the feature that names it. Kind gains Harness, for a module about what a harness gives or withholds. In "Signal", a flow asking the Belief Nexus what it may load is answered by visibility.
:::

```ethos
  Kind.[ Spirit Intent Vision
-        Knowledge Role ]
+        Knowledge Role Harness ]
  ModuleName.{ Kind Subject.String }
+ ; who may list the module and load it
+ Visibility.[
+    Visible
+    ; listed to nobody; reached only through
+    ; a definition
+    Invisible
+    ; listed, but loadable by no harness;
+    ; the Nexus alone composes it
+    HarnessInvisible
+    VisibleTo.Vector<HarnessName>
+    InvisibleTo.Vector<HarnessName> ]
+ ; the module itself
+ Module.{ ModuleName Placement Visibility }
```

```ethos
+ ; what a harness may load
+ List.HarnessName
+ ; the visible ones, for it
+ Listed.Vector<ModuleName>
```
