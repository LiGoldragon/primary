<!-- to-the-living:start -->
Presentation.{ «Curriculum, a vision in ethos» }

## 1. Open the vision with its prose

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none; this is a new file.

Added:

```markdown
# Curriculum

Curriculum's data schema is authored in Ethos.
Shared skill values live in `curriculum.ethos`.
Registry, roles, projection, client and runtime
types live in named Library files.
Each file stem is its import source name.

Signal declares the messages a Nexus speaks.
Operation declares each effect and its result.
Memory declares the state a Nexus remembers.
Library holds types shared by those roots.

Every semantic string has a named struct type.
Raw `String` appears only inside `Text`.
Each field's type names its meaning.
Named vector types name each collection.

The generated `Query` comes from Signal.
The generated `Operation` and `Outcome` come
from Operation. Signal carries those types.
The CLI request remains a Library type.
Datom and role configuration parsing stay at CLI.

Skill sources and role packets use distinct
path, name, body and instruction types.
Role packet targets use `RoleSurface`.
Skill outputs use `ProjectionSurface`.
Role output manifests remain structured data.
Projection surfaces name all five output trees.
```

Ruling 1: approve or amend this prose?

## 2. Add `curriculum.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum.ethos`:

```ethos
; Shared scalar and skill edit types.
Library
[] ; imports
[ Text.{ String } ; raw text leaf
  Identifier.{ Text } ; identifier text
  PathText.{ Text } ; path text
  AbsolutePath.{ PathText } ; absolute path
  RelativePath.{ PathText } ; relative path
  DiagnosticMessage.{ Text } ; diagnostic text
  SkillName.{ Identifier } ; skill identity
  SkillNames.Vector<SkillName> ; skill names
  SkillBody.{ Text } ; authored Markdown
  SkillDependencies.Vector<SkillName> ; edges
  SkillSourcePath.{ AbsolutePath } ; source file
  SkillRootPath.{ AbsolutePath } ; source root
  SkillRootPaths.Vector<SkillRootPath> ; roots
  WorkspacePath.{ AbsolutePath } ; workspace
  RuntimeDirectory.{ AbsolutePath } ; runtime
  ChangedSkillNames.Vector<SkillName> ; changed
  AddedSkillNames.Vector<SkillName> ; added
  DeletedSkillNames.Vector<SkillName> ; deleted
  NewSkillPaths.Vector<SkillSourcePath> ; new
  EditedSkillPaths.Vector<SkillSourcePath> ; edited
  RemovedSkillPaths.Vector<SkillSourcePath> ; remove
  SkillPathEdits.{ ; source path edits
    NewSkillPaths
    EditedSkillPaths
    RemovedSkillPaths }
  SkillChange.{ ; skill name changes
    ChangedSkillNames
    AddedSkillNames
    DeletedSkillNames }
  CurriculumFailure.{ DiagnosticMessage } ; failure
]
[] ; kinds
[] ; associations
```

Ruling 2: approve or amend this file?

## 3. Add `curriculum_registry.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_registry.ethos`:

```ethos
; Repository registry and typed errors.
Library
[ curriculum:[ SkillName SkillNames SkillBody
               SkillDependencies SkillSourcePath
               SkillRootPaths DiagnosticMessage ] ]
[ SkillEntry.{ SkillSourcePath SkillName SkillBody
               SkillDependencies } ; source entry
  ; dependency-ordered closure entry
  ResolvedSkill.{ SkillSourcePath SkillName
                  SkillBody SkillDependencies }
  SkillEntries.Vector<SkillEntry> ; entries
  ; name-indexed source registry
  SkillRegistry.{ SkillEntries SkillRootPaths }
  RegistryReadFailure.{ SkillSourcePath
                        DiagnosticMessage } ; read
  InvalidSkillSource.{ SkillSourcePath
                       DiagnosticMessage } ; invalid
  FirstDefinitionPath.{ SkillSourcePath } ; first
  SecondDefinitionPath.{ SkillSourcePath } ; second
  ; one name defined at two source paths
  DuplicateSkillDefinition.{ SkillName
    FirstDefinitionPath SecondDefinitionPath }
  MissingSkillName.{ SkillName } ; missing edge
  DependencyCycle.{ SkillNames } ; cycle chain
  SkillOutsideRoots.{ SkillSourcePath } ; outside
  RepeatedPathEdit.{ SkillSourcePath } ; repeated
  ConflictingPathEdit.{ SkillSourcePath } ; conflict
  RegistryError.[ ; errors
    Read.RegistryReadFailure
    InvalidSource.InvalidSkillSource
    DuplicateName.DuplicateSkillDefinition
    Missing.MissingSkillName
    Cycle.DependencyCycle
    OutsideSource.SkillOutsideRoots
    RepeatedEdit.RepeatedPathEdit
    ConflictingEdit.ConflictingPathEdit ]
]
[] ; kinds
[] ; associations
```

Ruling 3: approve or amend this file?

## 4. Add `curriculum_roles.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_roles.ethos`:

```ethos
; Role configuration and packet plans.
Library
[ curriculum:[ Identifier Text RelativePath
               SkillNames ] ]
[ RoleIdentifier.{ Identifier } ; role id
  ModelName.{ Identifier } ; model id
  RoleModuleIdentifier.{ Identifier } ; module id
  RestrictionInstructionText.{ Text } ; policy text
  DisciplineName.{ Identifier } ; discipline id
  RoleDepthName.{ Identifier } ; depth id
  RoleDescriptionText.{ Text } ; description
  RoleModuleText.{ Text } ; module instructions
  ModuleInstructions.{ Text } ; rendered modules
  ProcedureText.{ Text } ; procedure
  RoleOutputPath.{ RelativePath } ; output path
  RoleOutputPaths.Vector<RoleOutputPath> ; outputs
  ; module identity collection
  RoleModuleIdentifiers.Vector<RoleModuleIdentifier>
  ; module identifiers selected for every role
  UniversalRoleModuleIdentifiers.{
    RoleModuleIdentifiers }
  ; module text collection
  RoleModuleTexts.Vector<RoleModuleText>
  StandingSkillNames.SkillNames ; standing roots
  Provider.[ Claude ChatGpt ] ; provider
  ; instruction permission levels
  Permission.[ Restricted Unrestricted ]
  Effort.[ Low Medium High Xhigh ] ; effort
  ; role packet output targets
  RoleSurface.[ ClaudeAgent CodexAgent PiAgent ]
  ; selected model and optional reasoning effort
  ModelChoice.{ ModelName Option<Effort> }
  ClaudeModelChoice.{ ModelChoice } ; Claude choice
  OtherModelChoice.{ ModelChoice } ; other choice
  ; one named instruction module
  RoleModule.{ RoleModuleIdentifier RoleModuleText }
  RoleModules.Vector<RoleModule> ; module records
  ; provider model and supported effort choices
  Model.{ ModelName Provider Vector<Effort> }
  Models.Vector<Model> ; model records
  RolePermission.{ DisciplineName
                   RestrictionInstructionText
                   Permission } ; discipline access
  ; role access rules
  RolePermissions.Vector<RolePermission>
  RoleDepth.{ RoleDepthName ClaudeModelChoice
              OtherModelChoice } ; configured depth
  RoleDepths.Vector<RoleDepth> ; depths
  ; description for one discipline and depth
  RoleDescription.{ DisciplineName RoleDepthName
                    RoleDescriptionText }
  ; authored description set
  RoleDescriptions.Vector<RoleDescription>
  RoleAlias.{ RoleIdentifier DisciplineName
              RoleDepthName RoleDescriptionText
              Vector<RoleSurface> } ; alias
  RoleAliases.Vector<RoleAlias> ; aliases
  ; extra modules for one target and module
  TargetInsertion.{ RoleModuleIdentifier RoleSurface
                    RoleModuleIdentifiers }
  ; target-specific instruction insertions
  TargetInsertions.Vector<TargetInsertion>
  Roles.{ ; full role configuration
    RoleModules Models RolePermissions RoleDepths
    RoleDescriptions RoleAliases
    UniversalRoleModuleIdentifiers TargetInsertions
    StandingSkillNames }
  RolesDocument.[ Roles.Roles ] ; source document
  RolePacketPlan.{ ; output packet plan
    RoleSurface RoleOutputPath RoleIdentifier
    RoleDescriptionText ModelName Effort Permission
    ModuleInstructions ProcedureText }
  ; complete packet set
  RolePacketPlans.Vector<RolePacketPlan>
  ; previously managed output files
  PreviousRoleOutputPaths.RoleOutputPaths
  GeneratedRoleOutputPaths.RoleOutputPaths ; outputs
  ; currently generated output files
  RoleManifest.{ GeneratedRoleOutputPaths }
  ; stored manifest document
  RoleManifestDocument.[
    GeneratedRoleOutputs.RoleManifest ]
  ; complete inputs to one projection pass
  RolePlan.{ RolePacketPlans StandingSkillNames
             PreviousRoleOutputPaths RoleManifest }
]
[] ; kinds
[] ; associations
```

Ruling 4: approve or amend this file?

## 5. Add `curriculum_projection.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_projection.ethos`:

```ethos
; Harnesses and generated skill projections.
Library
[ curriculum:[ RelativePath WorkspacePath
               AbsolutePath DiagnosticMessage ] ]
[ Harness.[ Claude Codex Pi OpenCode ] ; renderer
  CodexPolicy.[ Required NotRequired ] ; policy
  ProjectionSurface.{ RelativePath Harness
                      CodexPolicy } ; output surface
  ProjectionReadFailure.{ AbsolutePath
                          DiagnosticMessage } ; read
  ; output path and filesystem failure
  ProjectionWriteFailure.{ AbsolutePath
                           DiagnosticMessage }
  ; output path or diagnostic-only mismatch
  ProjectionMismatch.[ Path.AbsolutePath
                      Diagnostic.DiagnosticMessage ]
  ProjectionError.[ ; projection failures
    Read.ProjectionReadFailure
    Write.ProjectionWriteFailure
    Different.ProjectionMismatch ]
  SkillProjector.{ WorkspacePath } ; writer
]
[] ; kinds
[] ; associations
```

Ruling 5: approve or amend this file?

## 6. Add `curriculum_client.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_client.ethos`:

```ethos
; CLI requests and client boundary failures.
Library
[ curriculum:[ SkillNames SkillPathEdits Text
               AbsolutePath DiagnosticMessage ]
  curriculum_roles:[ RolePlan ] ]
[ CliArgumentText.{ Text } ; CLI argument
  CliArguments.Vector<CliArgumentText> ; arguments
  SocketPath.{ AbsolutePath } ; Nexus socket
  ; configured roles source
  RoleConfigurationPath.{ AbsolutePath }
  ; invalid command-line arguments
  ClientArgumentFailure.{ DiagnosticMessage }
  DatomRequestFailure.{ DiagnosticMessage } ; datom
  RolePlanFailure.{ DiagnosticMessage } ; role plan
  ; socket path and connection failure
  ClientConnectionFailure.{ SocketPath
                            DiagnosticMessage }
  ClientFrameFailure.{ DiagnosticMessage } ; frame
  ClientEncodeFailure.{ DiagnosticMessage } ; encode
  ClientDecodeFailure.{ DiagnosticMessage } ; decode
  ; typed failures from a CLI exchange
  ClientError.[ Arguments.ClientArgumentFailure
                Datom.DatomRequestFailure
                Roles.RolePlanFailure
                Connect.ClientConnectionFailure
                Frame.ClientFrameFailure
                Encode.ClientEncodeFailure
                Decode.ClientDecodeFailure ]
  CliRequest.[ ResolveSkills.SkillNames
               EditSkills.SkillPathEdits
               CheckSkills RebuildSkills ] ; input
  CurriculumClient.{ CliArguments } ; CLI adapter
]
[] ; kinds
[] ; associations
```

Ruling 6: approve or amend this file?

## 7. Add `curriculum_runtime.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_runtime.ethos`:

```ethos
; Runtime configuration and Nexus markers.
Library
[ curriculum:[ SkillRootPaths WorkspacePath
               RuntimeDirectory ] ]
[ Settings.{ SkillRootPaths WorkspacePath
             RuntimeDirectory } ; settings
  CurriculumOperation.{ } ; operation adapter
  CurriculumSignal.{ } ; signal adapter
  CurriculumNexus.{ } ; Nexus wiring
]
[] ; kinds
[] ; associations
```

Ruling 7: approve or amend this file?

## 8. Add `curriculum_operation.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_operation.ethos`:

```ethos
; Operations and their results.
Operation
[ curriculum:[ SkillNames SkillPathEdits SkillChange
               CurriculumFailure ]
  curriculum_roles:[ RolePlan ] ] ; imports
[ ; expand dependency closure
  ResolveSkills.SkillNames
  ; apply source edits
  EditSkills.SkillEdits
  ; compare generated projections
  CheckSkills.RolePlan
  ; regenerate generated projections
  RebuildSkills.RolePlan ]
[ ResolvedSkills.SkillNames ; resolved closure
  SkillsChanged.SkillChange ; changed names
  SkillsChecked.SkillNames ; checked names
  SkillsRebuilt.SkillNames ; rebuilt names
  Rejected.CurriculumFailure ] ; outcomes
[ SkillEdits.{ SkillPathEdits RolePlan } ; input
]
```

Ruling 8: approve or amend this file?

## 9. Add `curriculum_signal.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_signal.ethos`:

```ethos
; Nexus messages carry typed operations/results.
Signal
[ curriculum_operation:[ Operation Outcome ] ]
[ Invoke.Operation ] ; query variants
[ Complete.Outcome ] ; response variants
[] ; signal types
```

Ruling 9: approve or amend this file?

## 10. Add `curriculum_memory.ethos`

File: `/git/github.com/LiGoldragon/psyche-skills/skills/vision-curriculum.md`

Removed: none.

Added, under the heading `curriculum_memory.ethos`:

```ethos
; Remembered state for the skill registry.
Memory
[ curriculum:[ SkillRootPaths SkillChange
               CurriculumFailure ]
  curriculum_registry:[ SkillRegistry ]
  curriculum_projection:[ SkillProjector ] ]
[ LastFailure.Option<CurriculumFailure> ; last error
  LastChange.Option<SkillChange> ; last edit
  ; registry, roots, projector and last result
  SkillState.{ SkillRegistry SkillRootPaths
               SkillProjector LastFailure
               LastChange }
  SkillSnapshot.{ SkillState } ; copied read view
  SkillMemory.{ SkillState } ] ; live actor state
```

Ruling 10: approve or amend this file?
<!-- to-the-living:end -->
