<!-- to-the-living:start -->
Presentation.{ «Roles that call roles» }

```
+--------------------------+
| Flow launch              |
+--------------------------+
             | composes, verifies
             v
+--------------------------+
| role files               |
| tmpfs .claude/agents     |
+--------------------------+
             | added with --add-dir to
             v
+--------------------------+
| Claude agent lookup      |
+--------------------------+
     | ranks first     | ranks second
     v                 v
+--------------+  +--------------+
| primary      |  | Flow's       |
| .claude/     |  | verified     |
| agents       |  | role files   |
+--------------+  +--------------+

+--------------------------+
| book role                |
+--------------------------+
             | dispatches
             v
+--------------------------+
| Flow guard               |
+--------------------------+
             | reads
             v
+--------------------------+
| RoleCall                 |
| { illustrator [ book ] } |
+--------------------------+
             | permits
             v
+--------------------------+
| illustrator role         |
+--------------------------+
```

### Proposal 1: Curriculum › README.md

Option (a): the rendered book agent is no longer installed in a working directory, and Flow alone gives it to Claude.

```markdown
- The deployment owner installs this output as generated `.claude/agents/book.md`
- within its existing transaction. The producer writes no files and accepts no
+ Flow alone gives this output to Claude, for one
+ launch; no working directory holds it in
+ `.claude/agents`. The producer writes no files
+ and accepts no
  prompt path or inline prose. It checks returned payload hashes and requires the
```

### Proposal 2: primary › .claude/agents/book.md, a deleted file

Option (a), with proposal 1: primary's installed book agent is deleted.

```yaml
- ---
- name: book
- description: "\nPublish a fresh living-messenger presentation from the calling flow's transcript.\n"
- model: sonnet
- effort: medium
- tools: [Read, Bash, Agent, Artifact]
- ---
```

### Proposal 3: primary › .claude/agents/illustrator.md, a deleted file

Option (a), with proposal 1: primary's installed illustrator agent is deleted.

```yaml
- ---
- name: illustrator
- description: "\nDraw the book's idea as one SVG by the illustration rules, with no tools or subdelegation.\n"
- model: sonnet
- effort: medium
- tools: []
- ---
```

### Proposal 4: flow › crates/flow-nexus/src/herdr/launch.rs

Option (b): after the roles are composed, Flow refuses the spawn when the working directory or any parent holds an agent file of a selected role's name.

```rust
                  })?;
+             // A project agent of a role's name
+             // outranks the added directory.
+             let root =
+                 self.configured_workspace_root()?;
+             for role in &role_files {
+                 let agent = format!(
+                     ".claude/agents/{}.md",
+                     role.agent_file_name
+                 );
+                 if let Some(found) = root
+                     .ancestors()
+                     .map(|dir| dir.join(&agent))
+                     .find(|path| path.exists())
+                 {
+                     return Err(format!(
+                         "{} shadows the role {}",
+                         found.display(),
+                         role.agent_file_name
+                     )
+                     .into());
+                 }
+             }
```

### Proposal 5: flow › crates/flow-nexus/src/herdr/launch.rs

Option (c): Flow opens a Claude pane in its runtime directory, which holds no project agents, and a Codex pane in the workspace as now.

```rust
              "--cwd".into(),
-             self.configured_workspace_root()?
+             match launch.harness_kind {
+                 // No project agent outranks the
+                 // added directory here.
+                 HarnessKind::Claude => self
+                     .role_root
+                     .as_deref()
+                     .and_then(Path::parent)
+                     .ok_or("no runtime root")?,
+                 HarnessKind::Codex => self
+                     .configured_workspace_root()?,
+             }
                  .to_str()
```

### Proposal 6: Curriculum › curriculum.ethos

A role call names a called role and the roles that may call it, and a composed role carries its calling roles.

```ethos
- ; ID-only in-memory composition. No caller paths, source bodies or file projection.
+ ; ID-only in-memory composition. No caller
+ ; paths, source bodies or file projection.
  Library
  []
  [ ModuleIdentity.String
    RepositoryName.String
    SourceRevision.String
    SourceRoot.String
    SourceRelativePath.String
    ModuleType.String
    ModuleSubject.String
    DeclaredPlacement.String
    SourceSha256.String
    BodySha256.String
    RenderedSha256.String
    Target.[ Claude Codex Pi OpenCode ]
    CallerMetaflow.{ String String String }
    StartupPlacement.[ System User ]
    SystemModules.Vector<ModuleIdentity>
    UserModules.Vector<ModuleIdentity>
    SystemText.String
    UserText.String
    SystemPayloadSha256.String
    UserPayloadSha256.String
-   StartupSelection.{ CallerMetaflow Target SystemModules UserModules }
-   ContextProvenance.{ ModuleIdentity RepositoryName SourceRevision SourceRelativePath SourceSha256 BodySha256 RenderedSha256 StartupPlacement Integer }
-   StartupComposition.{ SystemText UserText SystemPayloadSha256 UserPayloadSha256 Vector<ContextProvenance> }
-   ResolvedModule.{ ModuleIdentity RepositoryName SourceRevision SourceRoot SourceRelativePath ModuleType ModuleSubject DeclaredPlacement SourceSha256 BodySha256 String Vector<String> }
+   StartupSelection.{ CallerMetaflow Target
+                      SystemModules UserModules }
+   ContextProvenance.{ ModuleIdentity
+                       RepositoryName
+                       SourceRevision
+                       SourceRelativePath
+                       SourceSha256 BodySha256
+                       RenderedSha256
+                       StartupPlacement Integer }
+   StartupComposition.{ SystemText UserText
+                        SystemPayloadSha256
+                        UserPayloadSha256
+                        Vector<ContextProvenance> }
+   ResolvedModule.{ ModuleIdentity RepositoryName
+                    SourceRevision SourceRoot
+                    SourceRelativePath ModuleType
+                    ModuleSubject DeclaredPlacement
+                    SourceSha256 BodySha256 String
+                    Vector<String> }
    RoleName.String
    ModelId.String
    DescriptionModule.ModuleIdentity
    ContextModules.Vector<ModuleIdentity>
    DescriptionText.String
    ContextText.String
    DescriptionPayloadSha256.String
    ContextPayloadSha256.String
    Permission.[ Restricted Unrestricted ]
    Effort.[ Low Medium High Xhigh ]
    Surface.[ ClaudeAgent CodexAgent PiAgent ]
    RoleTools.[ Inherit Explicit.Vector<String> ]
    RoleCallers.[ Any Only.Vector<CallerMetaflow> ]
-   RoleDefinition.{ RoleName Surface ModelId Effort Permission DescriptionModule ContextModules RoleTools RoleCallers }
-   Roles.{ Vector<RoleDefinition> }
+   RoleDefinition.{ RoleName Surface ModelId Effort
+                    Permission DescriptionModule
+                    ContextModules RoleTools
+                    RoleCallers }
+   Roles.{ Vector<RoleDefinition>
+           Vector<RoleCall> }
    RolesDocument.[ Roles.Roles ]
    RoleSelection.{ RoleName Surface }
-   RoleComposition.{ RoleName Surface ModelId Effort Permission DescriptionText ContextText RoleTools RoleCallers Vector<ContextProvenance> DescriptionPayloadSha256 ContextPayloadSha256 }
-   CliRequest.[ ResolveSkills.Vector<ModuleIdentity>
-                ResolveSources.Vector<ModuleIdentity>
-                ComposeStartup.StartupSelection
-                ComposeRole.RoleSelection ]
+   CallingRoles.Vector<RoleName>
+   RoleCall.{ RoleName CallingRoles }
+   RoleComposition.{ RoleName Surface ModelId
+                     Effort Permission
+                     DescriptionText ContextText
+                     RoleTools RoleCallers
+                     CallingRoles
+                     Vector<ContextProvenance>
+                     DescriptionPayloadSha256
+                     ContextPayloadSha256 }
+   CliRequest.[
+     ResolveSkills.Vector<ModuleIdentity>
+     ResolveSources.Vector<ModuleIdentity>
+     ComposeStartup.StartupSelection
+     ComposeRole.RoleSelection ]
    Query.[ ResolveSkills.Vector<ModuleIdentity>
            ResolveSources.Vector<ModuleIdentity>
            ComposeStartup.StartupSelection
            ComposeRole.RoleSelection ]
    Outcome.[ ResolvedSkills.Vector<ModuleIdentity>
              ResolvedSources.Vector<ResolvedModule>
              StartupComposed.StartupComposition
              RoleComposed.RoleComposition
              Rejected.String ] ]
  []
  []
```

### Proposal 7: Curriculum › roles.datom

The illustrator may be called by the book role.

```datom
- ] }
+ ]
+ [ { illustrator [ book ] } ] }
```
<!-- to-the-living:end -->
