# A feature carries its belief

Created by Fable 5.1, alone.

### Proposal 1: A feature carries its belief · psyche-belief › vision/flow-nexus-v1.md

::: comment
In the library of "The vocabulary of a definition", an effect gains a third kind, a belief module, and a feature carries several effects; a flow launched with a feature is told so by the module the feature names. ModuleName is the Belief Nexus's type, declared in vision:belief-nexus-v1 and already imported here. The second fence is added after the Define.Harness example in "Memory"; the feature name is a String, uncapitalized since the Nexus fixes none.
:::

::: shown
psyche-belief › vision/belief-nexus-v1.md
Library
[]
[ Path.String                        ; a directory holding
                                     ;   <type>/<subject>.md
  ModuleSource.[ Repository.Path     ; a git repository, watched:
                                     ;   main moving refurnishes
                 Directory.Path ]    ; a directory read as it
                                     ;   stands, watched by nobody
  Kind.[ Spirit Intent Vision
         Knowledge Role ]
  ModuleName.{ Kind Subject.String }
  Workspace.String                   ; the flow's directory
  Placement.[ SystemPrompt Skill ]   ; named in front matter;
                                     ;   default per Kind: meta
  Location.{ SystemPrompt.String     ; the bundle file written
             Skills.String } ]       ; the skills directory
[]
[]
:::

```ethos
  [ herdr:[ Pane ]
    belief:[ ModuleName ] ]
  ; what a feature does to the launch
  Effect.[ Flag.String
-          Environment.{ Name.String
-                        Value.String } ]
-  Feature.{ FeatureName Effect }
+          ; a variable, for the harness alone
+          Environment.{ Name.String
+                        Value.String }
+          ; a module composed into the flow's
+          ; prompt
+          ModuleName ]
+  ; one feature, every effect it has
+  Feature.{ FeatureName Vector<Effect> }
```

```datom
+ { noClaudeArtifacts
+   [ Flag.«--disallowedTools Artifact,
+           ArtifactComments,ArtifactData»
+     ModuleName.{ Knowledge
+                  no-claude-artifacts } ] }
```


### Proposal 2: The flow without Claude artifacts · psyche-belief › knowledge/no-claude-artifacts.md

::: comment
A new module, reached only through the noClaudeArtifacts feature; it says what the flow lacks, and nothing of how a page is published, which is every flow's knowledge in knowledge:flow-messaging.
:::

+ This flow runs in Claude without the Artifact tool, and publishes nothing itself.
