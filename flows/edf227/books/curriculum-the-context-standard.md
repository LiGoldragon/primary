Presentation.{ «Curriculum: the context standard» }

A design for the whole stack: how a piece of prompt is authored, registered, placed, and delivered into a flow's head — one standard, read by Flow at launch and by Curriculum's generator at build. Research is in my lane; what you ruled is built in: a module has a type, not a kind; a role is a module type; no repetition; the registry maps a name to a path; the name stays Curriculum.

## 1. The stack, in one picture

Drawing: five layers stacked, arrows downward. Top: *Curriculum* (authored Markdown modules and one manifest). Second: *the registry* (Flow's memory: type, name, location). Third, side by side: *Flow at launch* (composes system prompt and first prompt) and *curriculum-deploy at build* (generates the loadable skill trees and the agent definitions). Fourth: *the harness* (Claude Code, Codex). Bottom: *the flow's head* with three regions: system prompt, first prompt, loadable.

Curriculum is where humans and flows write. The registry is what the machine knows. Flow and the generator are the two readers of the same registry. The harness is what receives. Nothing is written twice.

## 2. A module

A module is one Markdown file with a typed head. Its type says who stands behind it and where it may go; its name is unique within its type; its body is the prompt text.

Drawing: one file card with a header strip (type, name, description) and a body; beside it eight small tiles, one per type: Spirit, Intent, Vision, Knowledge, Compensation, Trial, Operation, Role.

```
---
type: Vision
name: flow
description: Flow — the Nexus that launches, names, tracks and ends flows — is being designed or judged.
---
Flow is the Nexus that manages flows. ...
```

## 3. The registry and the manifest

Curriculum carries one manifest: the list of its modules with their locations. The generator registers each over Flow's meta socket; Flow's memory then holds the registry. A location is a path today; a repository and revision later.

```
Library
[]
[ ModuleType.[ Spirit
               Intent
               Vision
               Knowledge
               Compensation
               Trial
               Operation
               Role ]
  Name.String
  Location.[ Path.String ]
  Module.{ ModuleType
           Name
           Location }
  Manifest.Vector<Module> ]
[]
[]
```

One manifest, as datom:

```
[ { Spirit spirit skills/spirit.md }
  { Vision flow skills/vision-flow.md }
  { Knowledge nexus skills/knowledge-nexus.md }
  { Role psyche skills/role-psyche.md } ]
```

Drawing: the manifest as a table on the left, an arrow labelled *Register* to a box *Flow memory: registry* on the right, and from the registry two arrows out, labelled *Flow at launch* and *curriculum-deploy at build*.

## 4. Where a module can go: the three placements

A flow's head has three regions, and each has a different reach.

Drawing: a head in profile with three bands. Top band *System prompt*: "replaces the harness's own; reaches the main flow only — never its subagents." Middle band *First prompt*: "the launch turn; what the flow must do now." Bottom band *Loadable*: "the skill trees; loaded by name when a situation calls." A dashed box beside the head, *subagent*, with arrows showing only the loadable band reaching it.

```
Library
[]
[ Placement.[ SystemPrompt
              FirstPrompt
              Loadable ]
  Selection.{ ModuleType
              Vector<Name> }
  Placed.{ Placement
           Vector<Selection> } ]
[]
[]
```

This answers your question from the morning: a part of the system prompt that does not reach subagents exists by construction. What is placed in the system prompt reaches the main flow only; the harness does not pass it down. What a subagent must know is placed in its own role's definition.

## 5. A role's configuration

Each role — the twelve voices and the focused roles — has one record: for each placement, which names of which type, and the model. A subagent role is a role like any other; its configuration generates its agent definition, so the brief carries only the task.

```
Memory
[ flow:[ Role
         Placed
         Model
         Module ] ]
[ RoleConfiguration.{ Role
                      Vector<Placed>
                      Model }
  Registry.Vector<Module> ]
```

The Psyche voice at the Primary layer:

```
{ Voice.{ Psyche Primary }
  [ { SystemPrompt [ { Spirit [ spirit ] }
                     { Intent [ deterministicWork ] }
                     { Role [ psyche main-flow ] }
                     { Vision [ flow ethos nexus ] } ] }
    { FirstPrompt [ { Operation [ launch ] } ] }
    { Loadable [ { Knowledge [ nexus flow ethos ] }
                 { Compensation [ primary-commit messenger ] } ] } ]
  claude-fable-5-1 }
```

Drawing: a table, rows = roles (Psyche Primary, Mind Primary, Field Primary, Implementation, VisionAudit, SystemAudit, LivingInteraction, read-trivial, book), columns = the three placements, each cell a few type-tagged names. Role rows for subagents show their system-prompt cell feeding an *agent definition* file icon.

## 6. The launch

Drawing: a sequence, left to right. *Launch.Role* arrives at Flow → Flow reads the role's configuration → for each selection, resolves (type, name) in the registry to a path and reads the file → concatenates the system-prompt selections in order into one file, the first-prompt selections into one prompt → starts the harness with that file and that prompt → the flow runs; its loadable modules are already in the trees the generator wrote.

Flow does this with no model in the loop: resolving names, reading files, concatenating text, is deterministic code, as you intend. The order of modules in the prompt is the order of the selections; a type's modules stay together.

## 7. The harness mapping

Drawing: a two-column table, Claude Code and Codex, rows = the three placements and the subagent definition.

- System prompt: Claude, the system-prompt file flag replacing the stock prompt; Codex, the developer instructions.
- First prompt: both, the first turn's text.
- Loadable: Claude, the `.claude/skills` tree; Codex, the `.agents/skills` tree — both written by the generator from the same registry.
- Subagent definition: Claude, an agent file whose body is the role's system-prompt selections and whose `skills` field preloads its loadable ones; Codex, a custom agent with developer instructions.

The generator is the only thing that knows these four vendor shapes. Flow knows placements and roles; Curriculum knows modules.

## 8. Adding a skill

Drawing: a loop of five steps. Write the module file in Curriculum → add its line to the manifest → run the generator: it checks the files, writes the trees and definitions, and registers the module over the meta socket → change the roles that should carry it, over the meta socket → the next launch of those roles carries it.

Nothing else moves: no brief changes, no prompt is edited by hand, no flow is told.

## 9. What is left for your word

1. Build it as drawn: Curriculum keeps authoring and the manifest; the generator registers and generates; Flow composes at launch; roles are configured over the meta socket.
2. The loadable placement is served by Flow on demand instead of generated into trees — later, when subflows are flows.
3. Locations by repository and revision now, not later.
4. Comment what to change.
