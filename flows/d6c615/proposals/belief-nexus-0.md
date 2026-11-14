Presentation.{ «The Belief Nexus, version 0» Proposal }

# The Belief Nexus, version 0

Created by Fable 5.2; Sonnet readers found the lines.

### Proposal 1: The Belief Nexus, retaken whole as version 0 · psyche-belief › vision/belief-nexus/0.md

::: comment
His words, 13 November: «I don't see that we are at belief nexus version 1 yet. I think we're still at version 0.» «No, curriculum is not belief. There, we renamed the concept, but that doesn't mean that belief version 0 is curriculum.» «Maybe we just make a belief nexus that can work now, that does this, and that has a version number all the time for everything.» «No, the belief nexus is not what furnishes the workspace. It's either the flow nexus or another nexus made for that, but the belief nexus furnishes beliefs, not workspaces.» And 12 November: «I'd also like to be able to configure everything. You could have the modules come from different repositories, so they're configured in the belief nexus.» «Subagents should be composed of the same modules as well. Composing a subagent should be the same thing as composing a flow. It just has a different kind of effect.» The module that stands holds two contracts that disagree; this one is written from his words as one concept with one contract. It takes in what «Belief is composed, for a flow or a subagent» and the three-field names of «Every belief module is versioned» proposed, so those lines are ruled here. The Operation and Memory parts are tentative in their names.
:::

```yaml
+ ---
+ description: The Belief Nexus, version 0, which holds the belief modules and furnishes a workspace it is handed with a composition of them, is being designed or judged against what the living wants it to be.
+ dependencies: [vision-nexus, vision-ethos]
+ ---
```

+ # The Belief Nexus

+ The Belief Nexus holds the belief modules and furnishes belief: it writes a composition of modules into the workspace it is handed, and makes no workspace. Belief is the word: what a model believes when it starts. Every belief is reached through the Belief Nexus, and everything about belief is its configuration.

```mermaid
+ flowchart TB
+     s["sources: a repository, or a directory"] -- "hold" --> m["modules, each named by kind, topic and version"]
+     m -- "are placed by" --> c["a composition, saved under its name"]
+     c -- "is written, for a flow or a subagent, into" --> w["the workspace the Belief Nexus is handed"]
+     s -- "a repository's main moves" --> r["every workspace it changed is furnished again"]
```

+ ## Library

+ A module's name is three fields, its kind, its topic and its version; a topic with one module has it at version 0. Modules come from several sources at once: a repository, the pure reference, or a directory, the quick one, for developing and debugging.

+ A composition is a saved configuration of belief: the modules, and for each its placement. A subagent is composed as a flow is, from the same modules; the effect differs, the composition being written as one subagent file for the flow of that workspace.

```ethos
+ Library
+ [ :flow:Harness ]                    ; imports: the harness, which names the skills directory
+ [ Path.String                        ; types: a directory holding <kind>/<topic>/<version>.md
+   Source.[ Repository.Path           ; a git repository, watched: its main moving furnishes again
+            Directory.Path ]          ; a directory, read as it stands at each furnishing
+   Kind.[ Spirit Intent Vision
+          Knowledge Role ]
+   Topic.String
+   Version.Integer
+   ModuleName.{ Kind Topic Version }  ; the three fields of every name
+   Placement.[ SystemPrompt           ; where a composition puts a module
+               StartupPrompt          ;   in the first prompt
+               VisibleSkill           ;   a skill the flow sees listed
+               HiddenSkill ]          ;   a skill it is not shown
+   Placed.{ ModuleName Placement }
+   CompositionName.String
+   Composition.{ CompositionName      ; a saved configuration of belief
+                 Vector<Placed> }
+   Workspace.String                   ; the directory the Belief Nexus is handed
+   SubagentName.String
+   Target.[ Flow                      ; written as a flow's prompts and skills
+            Subagent.SubagentName ]   ; written as one subagent file
+   Furnishing.{ Workspace Harness     ; what is asked: this composition,
+                CompositionName       ;   into this workspace,
+                Target }              ;   for a flow or a subagent
+   BundlePath.String                  ; the system prompt file written
+   StartupPath.String                 ; the first prompt file written
+   SkillsPath.String                  ; the harness's skills directory
+   SubagentPath.String                ; the subagent file written
+   Location.[ Flow.{ BundlePath       ; where the belief was written
+                     StartupPath
+                     SkillsPath }
+              Subagent.SubagentPath ] ]
+ []                                   ; traits
+ []                                   ; associations
```

+ ## Signal

+ A composition may name a module no source holds: the Belief Nexus answers which names are missing and writes the rest, and what is done about a missing module is the policy of the definition that asked. A definition in the Flow Nexus refers to a composition by its name.

+ A registered repository is watched: when its main moves, every workspace furnished with a module it changed is furnished again, and each subscriber is told, so the Flow Nexus knows which flows now run on old belief.

```ethos
+ Signal
+ [ :belief:[ Source ModuleName        ; imports
+             Composition CompositionName
+             Furnishing Workspace Location ] ]
+ [ Register.Source                    ; inputs: a source of modules
+   Compose.Composition                ;   a composition saved, or replaced, under its name
+   Furnish.Furnishing                 ;   a composition written into a workspace
+   Subscribe ]                        ;   the changes, as they happen
+ [ Registered.Source                  ; outputs
+   Composed.{ CompositionName
+              Missing.Vector<ModuleName> }   ; named, and held by no source
+   Furnished.{ Location
+               Missing.Vector<ModuleName> }  ; left out of what was written
+   Subscribed
+   Changed.{ Source                   ; a reaction: a repository's main moved
+             Vector<ModuleName>       ;   the modules it changed
+             Vector<Workspace> }      ;   the workspaces furnished again
+   Refused.[ UnknownSource.Source
+             UnknownComposition.CompositionName
+             Unwritable.Workspace ] ]
+ []                                   ; types
```

```datom
+ ; an example: the names are examples
+ Register.Repository.«/git/example/belief»
+ Registered.Repository.«/git/example/belief»
+ Compose.{ reviewer
+           [ { { Spirit core 0 } SystemPrompt }
+             { { Intent design 0 } SystemPrompt }
+             { { Vision ethos 0 } StartupPrompt }
+             { { Knowledge search 0 } VisibleSkill }
+             { { Vision absent 0 } VisibleSkill } ] }
+ Composed.{ reviewer [ { Vision absent 0 } ] }
+ Furnish.{ «/home/example/workspace» Claude reviewer Flow }
+ Furnished.{ Flow.{ «/home/example/workspace/.bundle»
+                    «/home/example/workspace/.startup»
+                    «/home/example/workspace/.claude/skills» }
+             [ { Vision absent 0 } ] }
+ Furnish.{ «/home/example/workspace» Claude reviewer Subagent.reviewer }
+ Furnished.{ Subagent.«/home/example/workspace/.claude/agents/reviewer.md»
+             [ { Vision absent 0 } ] }
```

+ ## Operation

```ethos
+ Operation
+ [ :belief:[ Source Composition       ; imports
+             Furnishing Location ModuleName ] ]
+ [ Registering.Source                 ; attempts, one per input
+   Composing.Composition
+   Furnishing                         ;   the furnishing asked, carried bare
+   Refurnishing.Source ]              ;   answers the event of a repository's main moving
+ [ Registered                         ; outcomes
+   Composed.Vector<ModuleName>        ;   the missing
+   Furnished.{ Location Vector<ModuleName> }
+   Failed.[ SourceUnreadable WorkspaceUnwritable MemoryRefused ] ]
+ []                                   ; types
```

+ ## Emission

+ Furnishing is writing. Each module's content is written between delimiters that name it, so the flow or subagent knows which module a belief comes from.

```ethos
+ Emission
+ [ :belief:[ Workspace Placed Target Location ]
+   :flow:Harness ]                    ; imports
+ [ Write.{ Workspace Harness Target   ; emissions: the files of one furnishing, written
+           Vector<Placed> } ]
+ [ Written.Location                   ; outcomes: what the translator observed
+   Unwritable ]
+ []                                   ; types
```

+ ## Memory

```ethos
+ Memory
+ [ :belief:[ Source ModuleName Composition Furnishing ] ]  ; imports
+ [ Held.{ Source Vector<ModuleName> } ; records: each registered source and the modules it holds
+   Composition                        ;   each composition, under its name
+   Furnishing                         ;   each furnishing, so a change finds the workspaces to furnish again
+   Answer.[ Succeeded Failed ] ]
```

### Proposal 2: The version 1 module is archived · psyche-belief › vision/belief-nexus-v1.md, a deleted file

::: comment
The concept part of the module, shown as it stands, is what Proposal 1 retakes. The rest of the module, from «The ordinary single-reply boundary» to its end, is the built service, and «The Belief Nexus vision keeps the concept» moves it to mind-belief › knowledge/belief-nexus.md. Mark: Archive.
:::

- ---
- description: The Belief Nexus, version 1, which holds the belief modules and furnishes workspaces with them in place of Curriculum, is being designed or judged against what the living wants it to be.
- dependencies: [vision-ethos]
- ---
-
- # The Belief Nexus
-
- The Belief Nexus holds the belief modules and furnishes workspaces with them. Belief is the word: what a model believes when it starts. It replaces Curriculum. Its memory is its own; a definition in the Flow Nexus refers to a module by name only, and a name may resolve to nothing: the Belief Nexus answers which names are missing, and what is done about it is the definition's policy, never the Nexus's.
-
- ## Signal
- The owner registers a belief repository at the Belief Nexus's own CLI, by his login, as he defines a complex at the Flow Nexus. A peer the meta peer list names furnishes over any registered repository.
-
- A registered repository is watched: when its main moves, every workspace furnished with a module it changed is furnished again, and the Flow Nexus is told which flows now run on old belief, so a perma flow can be refreshed on it. A module is named by kind and subject; its front matter names its placement, system prompt or skill. The skills directory is the harness's.
-
```ethos
- Signal
- [ belief:[ ModuleSource ModuleName    ; imports
-            Workspace Location ]
-   flow:[ Harness ] ]
- [ Register.ModuleSource              ; inputs: a module source
-   Resolve.Vector<ModuleName>
-   Furnish.{ Workspace Harness        ; the harness's
-             Vector<ModuleName> }     ;   skills directory
-   Subscribe ]
- [ Registered.ModuleSource            ; outputs
-   Resolved.{ Vector<ModuleName>      ; found
-              Vector<ModuleName> }    ; missing
-   Furnished.{ Location
-               Vector<ModuleName> }   ; missing, left out
-   Subscribed
-   Changed.{ ModuleSource              ; pushed: main moved
-             Vector<ModuleName>        ;   modules changed
-             Vector<Workspace> }       ;   workspaces refurnished
-   Refused.[ UnknownSource.ModuleSource
-             Unwritable.Workspace ] ]
- []
```
-
```datom
- Register.Repository.
-   /git/github.com/LiGoldragon/psyche-belief
- Registered.Repository.
-   /git/github.com/LiGoldragon/psyche-belief
- Register.Directory./home/li/psyche-belief-edits
```
-
```sh
- belief-nexus '
-   Register.
-     /git/github.com/LiGoldragon/psyche-belief'
```
-
- ## Meta
-
- A module's front matter names its placement; the default per Kind is a meta setting, set one value at a time, never in the Rust. The meta peer list names the peers admitted to Furnish, each bound by kernel credentials as a Nexus's peers are.
-
```ethos
- Signal
- [ belief:[ Kind Placement ] ]        ; imports
- [ Configure.Set ]                    ; inputs: one value at a time
- [ Configured.Set ]                   ; outputs: the value set
- [ Set.[ Placement.{ Kind             ; types: the default
-                     Placement }      ;   placement per Kind
-         Peer.PeerBinding             ;   a peer admitted to Furnish
-         RemovePeer.PeerId ]          ;   a peer removed
-   UserId.Integer                     ; a login
-   ProcessId.Integer
-   PeerId.String                      ; a peer's name
-   PeerIdentity.{ UserId ProcessId }  ; checked by kernel credentials
-   PeerBinding.{ PeerId PeerIdentity } ]
```
-
- ## Library
-
```ethos
- Library
- [ sema:[ Document Block Edit Place Outline ] ]
- [ Path.String                        ; a directory holding
-                                      ;   <type>/<subject>.md
-   ModuleSource.[ Repository.Path     ; a git repository, watched:
-                                      ;   main moving refurnishes
-                  Directory.Path ]    ; a directory read as it
-                                      ;   stands, watched by nobody
-   Kind.[ Spirit Intent Vision
-          Knowledge Role ]
-   ModuleName.{ Kind Subject.String }
-   Workspace.String                   ; the flow's directory
-   Placement.[ SystemPrompt Skill ]   ; named in front matter;
-                                      ;   default per Kind: meta
-   Location.{ SystemPrompt.String     ; the bundle file written
-              Skills.String } ]       ; the skills directory
- []
- []
```
-
- ## Emission
-
- Furnishing is writing: each module into the workspace's system-prompt bundle or the harness's skills directory, as its placement says.
-
```ethos
- Emission
- [ belief:[ Workspace ModuleName Location ]
-   flow:[ Harness ] ]                   ; imports: the harness names the skills directory
- [ Write.{ Workspace Harness Vector<ModuleName> } ] ; emissions: the bundle and the skills, written
- [ Written.Location ]                   ; outcomes
- []
```
-
- ## Memory
-
```ethos
- Memory
- [ belief:[ ModuleSource ModuleName ] ]
- [ Source.{ ModuleSource Vector<ModuleName> } ; records: each registered source and the modules it holds
-   Answer.[ Succeeded Failed ] ]
```
-
```datom
- Furnish.{ /home/li/primary Claude
-           [ { Spirit core } { Vision nexus-v1 }
-             { Vision none } ] }
- Furnished.{ { /home/li/primary/.bundle
-               /home/li/primary/.claude/skills }
-             [ { Vision none } ] }
```
-

## Questions

1. Version 0 admits any caller, by «A Nexus keeps nobody out» in the Nexus vision; the version 1 module admitted to Furnish only the peers a meta list named. Is any caller right?
2. The module's directory, and the component's name in paths: belief-nexus, or BeliefNexus?
3. A fifth placement was proposed, a module held in the Belief Nexus and read from it on demand. Version 0 leaves it out, since it needs an input of its own. Left for version 1?
