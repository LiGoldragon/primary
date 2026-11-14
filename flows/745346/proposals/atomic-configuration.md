Presentation.{ «One permaflow configured alone» Proposal }

# One permaflow configured alone

Created by Fable 5.2. Sonnet gathered the types as they stand.

### Proposal 1: One value of one permaflow is changed alone · psyche-belief › vision/flow-nexus/0.md

::: comment
His words, 13 November: «So we still cannot do flow configuration atomically?» He wants one permaflow configured alone, in version 0. The module already shows one permaflow configured whole; its Permaflow type lacks the modules and the purpose the same module says the configuration holds, and nothing changes one value without sending the whole definition again. Here the definition gains the modules, purpose, kind and continuity, so one datom says everything about one address; the meta socket sets a whole definition by its own name; and Amend carries one value of one permaflow, so adding a module names the address and the module and nothing else. The two whole definitions the module shows gain the new fields.
:::

::: shown
psyche-belief › vision/flow-nexus/0.md
## Starting flows
:::

  A harness is described in configuration: every feature it has, and what leaving that feature out does to the launch, a flag or a variable. The Nexus holds no feature and no effect of its own; it reads the effect from the declaration and composes the launch from the names a permaflow lists. A new harness, or a new version of one, is a new declaration. Where two features share one flag, the composition emits that flag once, with the names merged.

+ A permaflow is one definition: everything the Flow Nexus holds about one address is in it. Configuration changes one value at a time: one permaflow is added, replaced or removed alone, and one value of one permaflow, a module among them, is changed alone, by naming the address and the value. The change takes effect at the permaflow's next flow.

```mermaid
+ flowchart TB
+     a["Configure.Amend: an address and one change"] -- "changes" --> b["one value of one permaflow"]
+     c["Configure.Permaflow: one definition, whole"] -- "adds or replaces" --> d["one permaflow"]
+     b -- "takes effect at" --> e["that permaflow's next flow"]
+     d -- "takes effect at" --> e
```

```ethos
  Library
  [ flow:[ Address ] ]                  ; imports: the permaflow's address
  [ HarnessName.[ Claude Codex ]        ; types: a harness, by name
    FeatureName.String                  ;   a feature, by name
    Effect.[ Flag.String                ;   what leaving the feature out does to the launch
             Environment.{ Name.String  ;     a variable, set for the harness alone
                           Value.String } ]
    Feature.{ FeatureName Effect }
    Harness.{ HarnessName               ; the declaration: every feature the harness has
              Features.Vector<Feature> }
    Root.String                         ; the flow's working directory
+   ModuleName.String                   ; a belief module, by its name: type, topic, version
+   Purpose.String                      ; what the permaflow is for, composed into its first prompt
+   Kind.[ Regular Simplified ]         ; a simplified flow judges alone, with no regular tool
+   Continuity.[ Maintained             ; always has a running flow
+                OnDemand ]             ;   asleep until a request wakes it
    Permaflow.{ Address
                Option<Root>
                HarnessName
-               LeaveOuts.Vector<FeatureName> } ]
+               LeaveOuts.Vector<FeatureName>
+               SystemModules.Vector<ModuleName>   ; composed into the system prompt
+               PromptModules.Vector<ModuleName>   ; composed into the first prompt
+               Purpose
+               Kind
+               Continuity } ]
  []                                    ; traits
  []                                    ; associations
```

```ethos
+ Signal
+ [ flow:[ Address Root HarnessName FeatureName ModuleName   ; imports
+          Purpose Kind Continuity Permaflow Harness ] ]
+ [ Configure.Set ]                          ; inputs: one change at a time
+ [ Configured.Set                           ; outputs: the change made
+   ConfigureRefused.[ UnknownPermaflow.Address
+                      UnknownHarness.HarnessName
+                      UnknownFeature.FeatureName
+                      UnknownModule.ModuleName ] ]
+ [ Set.[ Permaflow                          ; types: one permaflow, whole, added or replaced
+         RemovePermaflow.Address
+         Harness                            ;   one harness, whole, added or replaced
+         RemoveHarness.HarnessName
+         Amend.{ Address Change } ]         ;   one value of one permaflow
+   Change.[ Workspace.Option<Root>          ; a single value, replaced
+            HarnessName
+            Purpose
+            Kind
+            Continuity
+            Add.Element                     ; an element appended to its list
+            Remove.Element ]
+   Element.[ SystemModule.ModuleName
+             PromptModule.ModuleName
+             LeaveOut.FeatureName ] ]
```

```datom
+ ; one module added to one permaflow
+ Configure.Amend.{ { Psyche core Fable } Add.PromptModule.vision:energy-nexus:1 }
+ Configured.Amend.{ { Psyche core Fable } Add.PromptModule.vision:energy-nexus:1 }
+ ; its purpose set
+ Configure.Amend.{ { Psyche core Fable } Purpose.«Designs with the living.» }
+ ; one permaflow removed
+ Configure.RemovePermaflow.{ Psyche book Haiku }
```

```datom
  Configure.Permaflow.{
     { Psyche book Haiku }
     Some.«/home/li/book»
     Claude
-    [ ClaudeMd GitInstructions ] }
+    [ ClaudeMd GitInstructions ]
+    [ spirit:core:0 ]
+    [ knowledge:book:0 ]
+    «Publishes books.»
+    Regular
+    OnDemand }

  Configure.Permaflow.{
     { Psyche core Fable }
     None
     Claude
-    [ Artifact ClaudeMd GitInstructions ] }
+    [ Artifact ClaudeMd GitInstructions ]
+    [ spirit:core:0 intent:fable:0 ]
+    [ vision:proposal:0 vision:psyche:0 ]
+    «Designs with the living.»
+    Regular
+    Maintained }
```

### Proposal 2: One value of one member is changed alone · psyche-belief › vision/flow-nexus/1.md

::: comment
Version 1 defines a metaflow as one datom, added, replaced or removed alone; to change one member's module, the whole metaflow is defined again. The same input as in Proposal 1, on version 1's own types: every field of a Member is reachable, a single value replaced, a list gaining or losing one element. Every type Change names stands in the module already.
:::

  Everything that can be configured is configuration. The Nexus holds the vocabulary a definition is written in, as Ethos types; the user writes definitions in datom, the way Nix defines an operating system; a running flow is a definition in action. A metaflow is named by the user, and the Nexus runs it without knowing its name beforehand. A definition is one datom of its own: it is added, replaced or removed alone; a complex is one of them, naming its metaflows. No role or anatomy is in the Rust.

+ One value of one member is changed alone, by naming the member and the value; the rest of its metaflow stands as it was.

```ethos
  [ Define.[ Metaflow Harness Complex ] ; add or replace one
    Undefine.Name
+   Amend.{ Address Change }             ; one value of one member, named by its address
    Describe.Name                      ; one definition, read back
```

```ethos
  [ Defined.Name
    Undefined.Name
+   Amended.Address
```

```ethos
+   Change.[ HarnessName                 ; a single value of the member, replaced
+            ModelName
+            Effort
+            Continuity
+            Workspace
+            Tools
+            Intake
+            Missing
+            Add.Element                 ; an element appended to its list
+            Remove.Element ]
+   Element.[ Belief.ModuleName
+             Feature.FeatureName
+             Route ]
```

```datom
+ Amend.{ { designer fable } Add.Belief.{ Vision ethos } }
+ Amended.{ designer fable }
+ Amend.{ { designer fable } Effort.High }
+ Amended.{ designer fable }
```

## Questions

1. A change takes effect at the permaflow's next flow, and the running flow keeps what it started with. Is that what you want, or should a module added to a permaflow reach its running flow at once, as a prompt?
2. Version 0's permaflow gains Kind and Continuity because the running Flow Nexus already holds them for each address. The running entry also holds a tool set and the records the permaflow rests on; both are left out here, since the leave-outs already say which tools go. Should either join the definition?
