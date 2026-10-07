<!-- to-the-living:start -->
Presentation.{ «Curriculum's ethos, and every Nexus's three roots» }

## What Curriculum's ethos is today
One file, `curriculum.ethos` (Curriculum main 73414b6). It has a Library root and nothing else: no Signal, no Operation, no Memory. The Nexus wires those three roles in Rust over the Library types: `Query` serves as both Signal query and Operation, `Outcome` as both response and outcome, and the memory is the Rust struct `SkillMemory` with `SkillSnapshot`.

```ethos
; Typed Curriculum registry protocol. Datom lives at the CLI boundary.

Library
[]
[ SkillPathEdits.{ Vector<String> Vector<String> Vector<String> }
  SkillEdits.{ SkillPathEdits RolePlan }
  SkillChange.{ Vector<String> Vector<String> Vector<String> }
  RolePacketPlan.{ Surface String String String String Effort Permission String String }
  RolePlan.{ Vector<RolePacketPlan> Vector<String> Vector<String> String }
  CliRequest.[ ResolveSkills.Vector<String>
               EditSkills.SkillPathEdits
               CheckSkills
               RebuildSkills ]
  Query.[ ResolveSkills.Vector<String>
          EditSkills.SkillEdits
          CheckSkills.RolePlan
          RebuildSkills.RolePlan ]
  Outcome.[ ResolvedSkills.Vector<String>
            SkillsChanged.SkillChange
            SkillsChecked.Vector<String>
            SkillsRebuilt.Vector<String>
            Rejected.String ]
  RoleManifest.{ Vector<String> }
  RoleManifestDocument.[ GeneratedRoleOutputs.RoleManifest ]
  Provider.[ Claude ChatGpt ]
  Permission.[ Restricted Unrestricted ]
  Effort.[ Low Medium High Xhigh ]
  Surface.[ ClaudeAgent CodexAgent PiAgent ]
  ModelChoice.{ String Option<Effort> }
  RoleModule.{ String String }
  Model.{ String Provider Vector<Effort> }
  RolePermission.{ String String Permission }
  RoleDepth.{ String ModelChoice ModelChoice }
  RoleDescription.{ String String String }
  RoleAlias.{ String String String String Vector<Surface> }
  TargetInsertion.{ String Surface Vector<String> }
  Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> Vector<String> }
  RolesDocument.[ Roles.Roles ] ]

[]
[]
```

Fourteen types the Nexus uses are written in Rust, not ethos: `Settings`, `SkillSnapshot`, `SkillMemory`, `SkillEntry`, `ResolvedSkill`, `SkillRegistry`, `RegistryError`, `Harness`, `Surface` (a second one, clashing with the ethos `Surface`, which lacks OpenCode), `ProjectionError`, `SkillProjector`, and three trait markers.

## Every Nexus's roots today

| Nexus | Signal | Operation | Memory |
|---|---|---|---|
| Curriculum | no | no | no |
| Flow | yes | yes | no |
| Orchestrate | yes | no | no |
| Message | yes | no | no |
| Lojix | yes | no | no |
| Horizon | yes | no | no |

No Nexus has a Memory root.

## Proposal 1: `vision-nexus`, three roots
Lines removed: none. Added:
```
Every Nexus has a Signal, an Operation and a
Memory root, each written in ethos; a type the
Nexus uses is declared in one of them, never
in Rust alone.
```

## Proposal 2: Curriculum first, then every Nexus
Mind Astra splits `curriculum.ethos` into Signal, Operation and Memory roots: `Query` and `Outcome` into Signal; the edit, check and rebuild operations into Operation; `SkillMemory` and `SkillSnapshot` into Memory; one `Surface` with OpenCode. Then Flow's Memory root, then Orchestrate, Message, Lojix and Horizon.

## Rulings
1. Proposal 1: (a) land (b) amend.
2. Proposal 2: (a) Astra does it now, in that order (b) Curriculum only for now (c) amend.
<!-- to-the-living:end -->
