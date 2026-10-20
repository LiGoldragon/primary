<!-- to-the-living:start -->
Presentation.{ «Metaflow roles» }

# Metaflow roles

Machine: development branch of Flow and of Curriculum; nothing is deployed. The living's words are in `flows/da2038/vision/flow.md`, the last three entries of 2026-10-16: role definition files; per-role subagent override; Illustrator and Publisher.

```
+--------------------------------------+
| role file                            |
| one role: its model and its skills   |
+---------+----------------------+-----+
          |                      |
          | read by              | generates
          v                      | (Curriculum)
+--------------------+           v
| Flow Nexus         |   +----------------+
| (meta wire)        |   | subagent file  |
+---------+----------+   +----------------+
          |
          | launches
          v
+--------------------------------------+
| seat                                 |
| with its model and its skills        |
+--------------------------------------+
```

Machine: a metaflow is one standing topic of work (an aspect and a topic, such as Field publishing). A seat is one running model session in a metaflow, at one layer. A role says which seat runs there: its layer, its model, its skills. Flow Nexus is the program that starts seats. Its meta wire is the control channel it is configured over. Datom is the plain-text data format; ethos is the language that says what shape a datom file has.

```
+--------------------+
| any sender         |
+---------+----------+
          |
          | sends to
          v
+----------------------------------------------+
| metaflow: Field publishing                   |
|                                              |
|  +-----------------+     +----------------+  |
|  | Publisher       |     | Illustrator    |  |
|  | Quaternary      |     | seat           |  |
|  | Haiku           |     | Tertiary       |  |
|  +--------+--------+     | Sonnet         |  |
|           |              +----------------+  |
|           | calls                            |
|           v                                  |
|  +-----------------+                         |
|  | Illustrator     |                         |
|  | subagent        |                         |
|  | Sonnet,         |                         |
|  | one rung up     |                         |
|  +-----------------+                         |
+----------------------------------------------+
```

Machine: the Publisher is a Haiku seat, so by the present rule it may call only models at its own rung, Haiku, and below. The living asked for one exception: it may call the Sonnet Illustrator, one rung up. A subagent is a model that a seat calls for one piece of work and that has no seat of its own.

## 1. A repository for metaflow definitions

Machine: roles and subagents are configuration data, not cluster data, so they leave the cluster repository (goldragon) and get a public repository of their own, typed by its own ethos library. The layout:

- `ethos/role.ethos` the library of types (proposal 2).
- `metaflows/<aspect>-<topic>.datom` one metaflow per file (proposal 3).
- `subagents/<name>.datom` one subagent per file (proposal 4).

Ruling: Name the repository.

a. `metaflow`
b. `metaflows`
c. `metaflow-roles`
d. No new repository.

## Crystallization

### Proposal 2: the role library · metaflow › ethos/role.ethos, a new file

Machine: a new file; nothing is removed. It imports Flow's shared leaf types (Aspect, Layer, Topic, Key) from `crates/flow-ethos/ethos/library.ethos` and is written in the proposed syntax: the file is an ordinary datom, `Library.` and then braced sections (imports, types, traits, associations). `⟦ T ⟧` means a list of T. The file was read by the proposed Ethos reader and is accepted.

```ethos
+ Library.
+ {
+ [ flow:[ Aspect Layer Topic Key ] ]  ; imports
+ [ RoleName.String                    ; types
+   SubagentName.String
+   Native.String
+   Effort.[ Low Medium High Xhigh ]
+   Duty.String
+   Modules.⟦ Key ⟧
+   Reach.⟦ Native ⟧
+   Role.{ RoleName Layer Native Effort Duty
+          Modules Reach }
+   Subagent.{ SubagentName Native Effort Duty
+              Modules }
+   Metaflow.{ Aspect Topic Contact.Layer
+              Roles.⟦ Role ⟧ } ]
+ [ Spelled.[ spelling.[ String ] ]    ; traits
+   Counted.[ count.[ Integer ] ]
+   Modelled.[ native.[ Native ]
+              effort.[ Effort ] ]
+   Dutiful.[ duty.[ Duty ] ]
+   Equipped.[ modules.[ Modules ] ]
+   Reaching.[ reach.[ Reach ] ]
+   Staffed.[ contact.[ Layer ]
+             roles.[ ⟦ Role ⟧ ] ] ]
+ [ RoleName.[ Spelled ]              ; links
+   SubagentName.[ Spelled ]
+   Native.[ Spelled ]
+   Effort.[ Spelled ]
+   Duty.[ Spelled ]
+   Modules.[ Counted ]
+   Reach.[ Counted ]
+   Role.[ Modelled Dutiful Equipped Reaching ]
+   Subagent.[ Modelled Dutiful Equipped ]
+   Metaflow.[ Staffed ] ] }
```

Machine: what each type is, and why it is there.

- `Native` is the exact model id the Claude harness takes, such as `claude-haiku-5-5`. A seat's model is written once, in the role, as the harness needs it.
- `Effort` is how hard the model thinks, the same four levels Curriculum already uses.
- `Duty` is one sentence on what the role is for; the seat and the generated file both show it.
- `Role` is one seat of a metaflow: its name, its layer, its model, its effort, its duty, its `Modules` and its `Reach`. A module is a skill, named by a `Key`: a subaspect (Vision, Intent, Knowledge, Operation, Trial or Compensation) and a topic, so the skill `vision-book` is the key `Vision book`.
- `Reach` lists the subagent models the role may call beyond the default. By default a role calls the models at its own rung and below; the list is empty for most roles.
- `Subagent` is a model a seat calls for one piece of work: name, model, effort, duty, modules.
- `Metaflow` is one file's whole content: the aspect and topic, the `Contact` (the layer whose seat every sender reaches), and its roles.
- `Modules` and `Reach` are lists named once, because the syntax allows a position name to be declared in place only once in a file; `Role` and `Subagent` both hold `Modules` by name.

Machine: the traits and the associations that bear them are new in this proposal and part of it for the living's ruling. A trait says what a type does; each type bears at least one.

- `Spelled` gives the text of a name-like type: `RoleName`, `SubagentName`, `Native`, `Effort`, `Duty`.
- `Counted` gives how many entries a list holds: `Modules`, `Reach`.
- `Modelled` gives the model and its effort: `Role`, `Subagent`.
- `Dutiful` gives the duty: `Role`, `Subagent`.
- `Equipped` gives the modules: `Role`, `Subagent`.
- `Reaching` gives the reach: `Role`.
- `Staffed` gives the contact layer and the roles: `Metaflow`.

Ruling: Land the library as shown, or not.

a. Land it as shown, traits included.
b. Land it as shown, with the traits and associations sections empty.
c. Neither; it is redesigned.

### Proposal 3: the publishing metaflow · metaflow › metaflows/field-publishing.datom, a new file

Machine: a new file; nothing is removed. The ids `claude-sonnet-5-5` and `claude-haiku-5-5` are read from the usage ledger in `flows/d68c82/reports/flow-context-2026-10-14.edn` and from the layer-model table in `mind-context/skills/knowledge-layer-models.md`. Curriculum's `roles.datom` itself names only the aliases `sonnet` and `claude-haiku-4-5`; I did not find the deployed Flow configuration file, so the ids are not read there. The Publisher's modules are the standing skills the present `book` subagent file is composed with, as listed in `roles.datom`; of that list, `compensation-book-distillation` has no skill file I could find, and `spirit` has no subaspect to key it by (its text already reaches every subagent as the base `spirit-role`), so both are left out. `compensation-messenger-clj` becomes `Compensation messengerClj`, the topic in camelCase. The datom is a `Metaflow` value, so it is the braced struct alone, with no head. It was read as a `Metaflow` against the role library with the checker's Conform; the checker cannot read the imported types, so Aspect, Layer, Topic and Key were stood in by local declarations for the check, and the real file imports them.

```datom
+ {
+   Field publishing Quaternary
+   [ { Illustrator Tertiary
+       claude-sonnet-5-5 Medium
+       «Draws figures and illustrations for books.»
+       [ { Vision book }
+         { Compensation bookCrystallization } ]
+       [] }
+     { Publisher Quaternary
+       claude-haiku-5-5 Medium
+       «Publishes books; the contact.»
+       [ { Compensation truth }
+         { Compensation orders }
+         { Compensation prose }
+         { Compensation understanding }
+         { Compensation launch }
+         { Compensation design }
+         { Compensation defaultEffort }
+         { Compensation messengerClj } ]
+       [ claude-sonnet-5-5 ] } ] }
```

Machine: the last line is the Publisher's `Reach`: the one exception to the default. The topic word `publishing` is a choice.

Ruling: Land the file, with the topic word.

a. `publishing`
b. `books`
c. `illustration`
d. Neither.

### Proposal 4: the Illustrator subagent · metaflow › subagents/illustrator.datom, a new file

Machine: a new file; nothing is removed. It is the subagent file the Publisher calls. Its modules are the two figure-grammar skills of the book procedure. The rules for drawing a figure that the book subagent now copies into each figure brief live in `compensation-flashbook-illustration`; 4b adds that key. The datom is a `Subagent` value, braced with no head; it was read as a `Subagent` with Conform, the imported types stood in as in proposal 3.

```datom
+ {
+   Illustrator claude-sonnet-5-5 Medium
+   «Returns an illustration for each book figure.»
+   [ { Vision book }
+     { Compensation bookCrystallization } ] }
```

Ruling: Land the file.

a. Land it with the two keys shown.
b. Land it with a third key, `Compensation flashbookIllustration`.
c. Neither.

### Proposal 5: Flow reads metaflow definitions · meta-signal-flow › ethos/signal.ethos

Machine: the Flow Nexus reads a `Metaflow` over its meta wire as `Configure.Metaflow`, and a seat's model comes from its role, so the layer-only `ConfigureModel` is removed. The `Contact` makes a send addressed to the metaflow (aspect and topic, no layer) land on the Contact seat. In `crates/flow-nexus/src/waking.rs`, `start_fresh` now looks up the model by the address's layer in the configured models (lines 947 to 953); it would instead find the metaflow by aspect and topic, then the role at the address's layer, and take that role's `Native`, refusing as it does today when there is none. The lines below are as Flow pins them: `meta-signal-flow` at commit b6f8654, read with `git show b6f8654:ethos/signal.ethos` and put into the proposed syntax by changing only its head (`Signal.` and an opening brace) and its closing brace, where `ConfigureModel` is then at line 104, `ConfigurationChange` at lines 108 to 111 and `ConfigurationSnapshot` at line 112. The whole file, before and after the change, was read by the proposed Ethos reader and is accepted; only the changed lines are shown. Removed lines are wrapped at their positions for width; each is one row in the file. The new variant is written `Metaflow.Metaflow`, a variant named `Metaflow` that carries a `Metaflow`; a bare `Metaflow` would be a variant with no payload. A Signal file declares no traits, so the traits of `Metaflow` are those of proposal 2. Two consequences are not settled by this proposal. Every metaflow then needs a definition file, and only Field publishing is written here. Flow already has its own `Metaflow` record in its library (address, state, past, queue); 5b renames the definition type so the two never meet.

```ethos
  …
+   metaflow:Metaflow
  …
- ConfigureModel.{ Layer Native.String }
  …
-                         Model.ConfigureModel
+                         Metaflow.Metaflow
  …
- ConfigurationSnapshot.{ Nexus.ConfigureNexus
-   Models.Vector<ConfigureModel>
-   Thresholds.Vector<ConfigureThreshold>
-   Modules.Vector<ConfigureModule> }
+ ConfigurationSnapshot.{
+   Nexus.ConfigureNexus
+   Metaflows.Vector<Metaflow>
+   Thresholds.Vector<ConfigureThreshold>
+   Modules.Vector<ConfigureModule> }
```

Ruling: Read definitions on the meta wire.

a. As shown, the type named `Metaflow`.
b. As shown, the definition type renamed `MetaflowDefinition` in proposal 2 and here.
c. Neither.

### Proposal 6: subagent definitions leave Curriculum · Curriculum › roles.datom

Machine: the five role aliases (default, explorer, worker, tester, book) and the six read and write depth descriptions become eleven subagent files in the new repository. Curriculum keeps only generation: it reads each `subagents/*.datom` and composes the file with the skills of its modules. The marked removals are archived apart, not destroyed. Not settled here: the `Subagent` type of proposal 2 has no permission (read or write) and no surface (which harness), which an alias carries today; 6b adds both to the type. Whether the depth ladder and permissions then also leave Curriculum is not proposed. The two removed vectors are each one row of the whole `roles.datom`; here each is wrapped at its datom positions, one element per row, and a string is never broken, so it is the same row and the same datom. The second file of this proposal is `Curriculum/curriculum.ethos`, shown after the first. The ethos row removed there is wrapped the same way. The datom lines shown are the whole file, before and after, was read as `Roles` against the whole `curriculum.ethos` with Conform and conforms (every type is declared in that file). Both whole ethos files were read by the proposed Ethos reader and are accepted. `curriculum.ethos` declares no traits today and none is proposed here, so the `Roles` it keeps carries none.

```datom
  …
- [ { read trivial
-     «The answer is in one known place. You are fetching it, not finding it.» }
-   { read ordinary
-     «You know what you are looking for but not where it is.» }
-   { read demanding
-     «The answer is written nowhere. Assemble it from how the parts behave.» }
-   { write trivial
-     «The change is fully specified. No decisions remain.» }
-   { write ordinary
-     «The approach is known. Applying it is the work.» }
-   { write demanding
-     «The approach has to be chosen.» } ]
  …
- [ { default write ordinary
-     «General-purpose sub-agent for the Codex orchestrator»
-     [ CodexAgent ] }
-   { explorer read ordinary
-     «Read-only exploration sub-agent for the Codex orchestrator»
-     [ CodexAgent ] }
-   { worker write demanding
-     «Implementation sub-agent for the Codex orchestrator»
-     [ CodexAgent ] }
-   { tester write trivial
-     «Independent testing worker. Given only a bounded target, immutable revision, authority limits, and acceptance contract, choose the procedure, fixtures, negative cases, and independent oracle; return evidence grades and gaps.»
-     [ CodexAgent ClaudeAgent ] }
-   { book write ordinary
-     «Publish a fresh living-messenger presentation from the calling flow's transcript.»
-     [ ClaudeAgent ] } ]
  …
```

```ethos
  …
- RoleDescription.{ String String String }
- RoleAlias.{ String String String String
-   Vector<Surface> }
  …
- Roles.{ Vector<RoleModule> Vector<Model>
-   Vector<RolePermission> Vector<RoleDepth>
-   Vector<RoleDescription> Vector<RoleAlias>
-   Vector<String> Vector<TargetInsertion>
-   Vector<String> }
+ Roles.{
+   Vector<RoleModule> Vector<Model>
+   Vector<RolePermission> Vector<RoleDepth>
+   Vector<String> Vector<TargetInsertion>
+   Vector<String> }
```

**Archive, on approval:** the five aliases and six descriptions removed above, and the `RoleAlias` and `RoleDescription` types, each into its archive file.

Ruling: Move the subagent definitions.

a. As shown.
b. As shown, and the `Subagent` type gains `Permission` and `Surfaces`.
c. Neither.

### Proposal 7: how far a role may reach · psyche-context › skills/vision-flow.md

Machine: the line lands in the vision-flow skill after the paragraph on layers and models, where the layer decides the model. That paragraph says the model is declared once in Flow as configuration; if proposal 5 lands, it is stale and needs its own edit, which is not proposed here.

```text
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+
+ A role declares the subagent models it may call: by default those at its own rung and below; a role may name models above it in its reach.
  
  Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect.
```

Ruling: Land the line.

a. As written.
b. Neither.
<!-- to-the-living:end -->
