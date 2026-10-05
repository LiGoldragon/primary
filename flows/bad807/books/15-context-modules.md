<!-- to-the-living:start -->
Presentation.{ «Context modules» }

What a flow starts its thinking with: one standard, the first modules, and where each change lands.
Marks: **vision** enters on your word. **implementation** is built on your yes. **proposed, unruled** waits on a ruling.

## Your words
- "Where is the canonical place to find those types?" (2026-10-04)
- "here's how it is now and here's what we would like to change" (2026-10-04)
- "learning or adapting takes place: by changing these context modules" (2026-10-04)

## Where things are now
```
Distilled vision     Primary     Vision/<topic>.md                        21 files, none on context modules
Skill sources        Curriculum  skills/<name>.md                         70 flat files: description, dependencies
Generator            curriculum-deploy                                    writes .claude/skills, .agents/skills
Subagent roles       Curriculum  roles.datom                              one record, read by the generator
Main-flow prompt     Primary     tools/main-flow-mode/system-prompt.md    hand-written, outside Curriculum
Launcher             Primary     tools/claude-main-flow-launch.mjs        that file + six /skills in the first prompt
```

## The placements
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 330" width="700" font-family="system-ui,sans-serif" role="img" aria-label="Four placements and which of main flow, forks and subagents each reaches"><rect width="700" height="330" rx="10" fill="#f7f8fb"/><g font-size="13" font-weight="700" fill="#1d2430" text-anchor="middle"><text x="137" y="30">Placement</text><text x="375" y="30">Main flow</text><text x="495" y="30">Its forks</text><text x="620" y="30">Its subagents</text></g><g stroke="#c9d1de" stroke-width="1.5"><line x1="262" y1="72" x2="688" y2="72"/><line x1="262" y1="140" x2="688" y2="140"/><line x1="262" y1="208" x2="688" y2="208"/><line x1="262" y1="276" x2="688" y2="276" stroke-dasharray="6 4"/></g><rect x="12" y="44" width="250" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="12" y="112" width="250" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="12" y="180" width="250" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="12" y="248" width="250" height="56" rx="8" fill="#fff1d6" stroke="#b07a12" stroke-dasharray="6 4"/><g fill="#1d2430" text-anchor="middle"><g font-weight="700" font-size="14"><text x="137" y="68">System prompt</text><text x="137" y="136">First prompt</text><text x="137" y="204">Loadable</text><text x="137" y="272">Queued</text></g><g font-size="12"><text x="137" y="88">replaces the harness's own prompt</text><text x="137" y="156">the launch turn: what to do now</text><text x="137" y="224">the skill tree, loaded by name</text><text x="137" y="292">between turns, by the hook</text></g></g><g fill="#ddf1e4" stroke="#2f7d4a"><rect x="327" y="57" width="96" height="30" rx="15"/><rect x="447" y="57" width="96" height="30" rx="15"/><rect x="327" y="125" width="96" height="30" rx="15"/><rect x="447" y="125" width="96" height="30" rx="15"/><rect x="327" y="193" width="96" height="30" rx="15"/><rect x="447" y="193" width="96" height="30" rx="15"/><rect x="572" y="193" width="96" height="30" rx="15"/></g><rect x="327" y="261" width="96" height="30" rx="15" fill="#fff1d6" stroke="#b07a12" stroke-dasharray="5 3"/><g font-size="12" text-anchor="middle" fill="#1d2430"><text x="375" y="76">reaches</text><text x="495" y="76">reaches</text><text x="375" y="144">reaches</text><text x="495" y="144">reaches</text><text x="375" y="212">reaches</text><text x="495" y="212">reaches</text><text x="620" y="212">reaches</text><text x="375" y="280">proposed</text></g><g font-size="12" text-anchor="middle" fill="#6b7480"><text x="620" y="70">no: its own</text><text x="620" y="85">definition body</text><text x="620" y="144">no</text><text x="495" y="280">unruled</text><text x="620" y="280">unruled</text></g><text x="350" y="322" text-anchor="middle" font-size="12" fill="#4a5361">solid: the standard as drawn · dashed: Queued, proposed and unruled</text></svg>

Figure 1. *The four placements and whom each reaches. A subagent receives only the loadable tree, beside its own definition.*

## Proposal 1: the standard
**vision** · create `Vision/contextModules.md`

Now: no such file. Proposed, whole:
> **Context modules**
>
> **A context module is one file of what a flow starts its thinking with**
> A context module is one file of prompt text with a type, a name and a description.
> The type says who stands behind it and where it may go; a name is unique within its type.
> The types are declared once, in the generator's ethos; no other text lists them.
>
> **Three placements**
> A module reaches a flow in one of three places.
> The system prompt replaces the harness's own prompt; it reaches the main flow and its forks, never its subagents.
> The first prompt is the launch turn: what this flow does now.
> Loadable modules are the skill tree, loaded by name when a situation calls; they are the only placement a subagent reaches.
>
> **A role**
> A role is one record naming, for each placement, its modules by type, and its model. Flow composes the launch from that record with no model in the loop.
>
> **What qualifies for the system prompt**
> A module goes in the system prompt when it is steady, changing only on the living's word; when it addresses the role's whole run, never a task; and when it must be present before the first tool call or must hold against the harness's own guidance.
>
> Distilled spirit, intent and vision qualify; raw records never do. A seat's identity module qualifies.
> Knowledge is loadable, because it changes with the system. Any other Operation module goes in the first prompt or stays loadable.
>
> **What makes a module high quality**
> Every line is a definition or a rule in the present tense, leading with what is wanted. Each line traces to a record of the living or to a witness.
> One fact lives in one module. A module carries no history, no objection, and no unknown where a measurement is possible.
> It uses our terms, not a vendor's, except where a harness is named. It fits its placement's budget, and the budget is measured.

## Proposal 2: Queued, a fourth placement
**vision** · **proposed, unruled** · `Vision/contextModules.md`, after Loadable; and `curriculum-deploy.ethos`, the Placement line of Proposal 4
### Now
```
A module reaches a flow in one of three places.
Placement.[ SystemPrompt FirstPrompt Loadable ]
```
### Proposed
> A module reaches a flow in one of four places. …
> Queued context enters a running flow between its turns: the hook carries what Flow has queued for that flow into its next incoming message, timestamped. It is the only placement that reaches a flow after launch without the flow asking.
```
Placement.[ SystemPrompt FirstPrompt Loadable Queued ]
```

## Proposal 3: the standard as a loadable module
**implementation** · create Curriculum `skills/vision-context-modules.md`

Now: no such file. Proposed:
```
---
type: Vision
name: context-modules
description: A context module, its type or its placement is being designed, edited or judged.
---
<the body of Proposal 1, without its title>
```
Until the three aspect repositories exist, the text stands in `Vision/` and in Curriculum.

## Proposal 4: the types, declared once
**implementation** · `curriculum-deploy.ethos`, lines 25 and 32
### Now
```
  RoleModule.{ String String }
  Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> }
```
### Proposed, replacing those two lines
```
  ModuleType.[ Spirit Intent Vision Notion Knowledge Operation ]
  Location.[ Path.String ]
  Module.{ ModuleType Name.String Location }
  Manifest.Vector<Module>
  Placement.[ SystemPrompt FirstPrompt Loadable ]
  Selection.{ ModuleType Vector<Name> }
  Placed.{ Placement Vector<Selection> }
  RoleConfiguration.{ Role Vector<Placed> ModelChoice }
  Roles.{ Vector<RoleConfiguration> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> }
```
- `ModuleType` is the one place the types are listed.
- `RoleModule` goes: a role's text is a module file in `skills/`.
- `Vector<String>` and `TargetInsertion` go: a subagent role's definition body is its own SystemPrompt selections.

## Proposal 5: the type line
**implementation** · six Curriculum frontmatters
### Now, skills/spirit.md
```
---
description: Every agent task.
dependencies: [behavior, correction, vocabulary]
---
```
### Proposed: one line, `type:`, first in each frontmatter
```
skills/spirit.md                type: Spirit
skills/vocabulary.md            type: Vision
skills/psyche.md                type: Vision
skills/psyche-interraction.md   type: Operation
skills/edit-coordination.md     type: Operation
skills/main-flow.md             type: Operation
```
The name is the file stem, as today.

## The five first modules
The system prompt of the Psyche voice at the Primary layer, in order:
```
Spirit     spirit              skills/spirit.md                     390 tokens, measured
Operation  main-flow           skills/main-flow.md                  about 1,530 tokens, measured (Proposal 6)
Operation  psyche-primary      skills/operation-psyche-primary.md   about 90 tokens, estimated (Proposal 7)
Vision     vocabulary          skills/vocabulary.md                 425 tokens, measured
Vision     psyche              skills/psyche.md                     961 tokens, measured
                                                                    about 3,400, replacing the stock prompt whole
```

## Proposal 6: one main-flow module
**implementation** · Curriculum `skills/main-flow.md` becomes the Operation module `main-flow`; remove `tools/main-flow-mode/system-prompt.md`
### Now, skills/main-flow.md, lines 1 to 8
```
---
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, as the psyche-interraction skill says: verbatim, in its own flow's psyche records, before acting; a question, an order or an acknowledgement is answered or carried out, not logged as psyche. Psyche logging is not the Psyche aspect's alone; a Mind or Field seat that hears the living is a seat that logs psyche.
Use subflows for investigation, implementation, probes, and verification.
```
### Now, tools/main-flow-mode/system-prompt.md, line 1 of 15
```
You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.
```
### Proposed, skills/main-flow.md
```
---
type: Operation
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---

You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.
<the other fourteen lines of tools/main-flow-mode/system-prompt.md, unchanged>

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, …
```
- The six lines of the file that the system prompt repeats are removed: lines 8, 10, 11, 17, 18 and 51 (`Use subflows for investigation…`, `Keep your context's signal-to-noise ratio high…`, `Delegate all task work.`, `Never block on subflows.`, `Never stop waiting for subflows…`, and the closing `A design, report, book, prompt or message carries the thing as it now is…`).
- What remains is the operational part: flow-id, remembering, the log, the presentation block, the summary.
- `tools/main-flow-mode/system-prompt.md` is removed. The role record selects `{ Operation [ main-flow psyche-primary ] }` in SystemPrompt, and its FirstPrompt no longer lists `main-flow`.
- Measured: the remaining body is 724 words, 4,440 bytes, about 1,110 tokens; with the 424 of the prompt lines, `main-flow` is about 1,530 tokens.

## Proposal 7: the psyche-primary module
**implementation** · create `skills/operation-psyche-primary.md`

Now: no such file; the seat's identity is in the launch brief only. Proposed, whole:
```
---
type: Operation
description: The seat is the Psyche voice at the Primary layer.
user-only: true
---
You are the Psyche voice at the Primary layer: the seat that hears the living and designs what the machines start their thinking with.

What the living must read, rule on or approve goes whole into the living messenger as a presentation; he answers by number. Chat is unread.

You design, rule and judge. The Secondary builds and tests what you hand down.
```

## Proposal 8: the role record
**implementation** · Curriculum `roles.datom`
### Now, two lines, the record's opening and close; no main-flow role in it
```
; Curriculum role data: modules, models, permissions, depths, descriptions, aliases, universal modules, target insertions.
Roles.{ [ { general-instructions «The brief is your authority. Decide what it settles; return what it does not.» } { codex-skill-loading … } { spirit-role … } { intent-role … } { subflow-role … } ] …
… [ general-instructions spirit-role intent-role subflow-role ] [ { general-instructions CodexAgent [ codex-skill-loading ] } ] }
```
### Proposed
- Two inline modules are not new files; their text already exists. `spirit-role` duplicates the `spirit` module: the subagent definitions select `{ Spirit [ spirit ] }`. `intent-role` duplicates the Intent statement in `Intent/context.md`, "Every layer carries its own context": they select `{ Intent [ context ] }`.
- Three inline modules become Operation files in `skills/`, bodies unchanged: `operation-general-instructions`, `operation-codex-skill-loading`, `operation-subflow-role`.
- The record takes the shape of Proposal 4, and gains this role beside the subagent roles:
```
{ Voice.{ Psyche Primary }
  [ { SystemPrompt [ { Spirit [ spirit ] }
                     { Operation [ main-flow psyche-primary ] }
                     { Vision [ vocabulary psyche ] } ] }
    { FirstPrompt [ { Operation [ psyche-interraction edit-coordination ] } ] }
    { Loadable [ { Vision [ context-modules flow ethos nexus ] }
                 { Knowledge [ nexus flow ethos ] } ] } ]
  { claude-fable-5-1 None } }
```

## Proposal 9: the launcher composes from the role
**implementation** · `tools/claude-main-flow-launch.mjs`, lines 34, 100 and 110
### Now
```
export const BIRTH_SKILLS = ['main-flow', 'spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'];
  const prompt = `${BIRTH_SKILLS.map(n => `/${n}`).join(' ')} # Launch brief\n\n${brief.trim()}\n`;
  const promptFile = systemPromptFile ?? path.join(modeDir, 'system-prompt.md');
```
### Proposed
- The launcher takes a role name and reads that role's record.
- It resolves each SystemPrompt selection to its file in Curriculum, and concatenates them in order into the per-launch system-prompt file.
- The first prompt is the role's FirstPrompt selections as `/name` commands, then the brief.
- `BIRTH_SKILLS` and the fixed path go. Flow takes this step when Flow launches.

## Proposal 10: skill-designing's types
**vision** · Curriculum `skills/skill-designing.md`, lines 55–59 and 66–67
### Now
```
A skill's kind says who stands behind it.
A gold skill carries no prefix. It is the living's vision of the desired result, approved by the living, and changes only on the living's word.
An `operation-` skill is deployed when the living describes what he wants a skill to do or to change; the primary Mind seat reviews and interprets it, and no glance from the living is needed.
A `compensation-` skill is written by flows; it compensates for what the system does not yet do, so that the system runs.
A `trial-` skill is written by flows: it is being tried for how useful it can become as a compensation skill.
…
A role skill carries an aspect's identity and names its
dependencies. Mark role skills user-only.
```
### Proposed, replacing those lines
> A skill is a context module; its type, declared in the generator's ethos, says who stands behind it and where it may go.
> Spirit, Intent, Vision and Notion are the living's: distilled on his word, changed on his word.
> Knowledge is what a flow found out about the system as it is; any flow may load it. Operation is how a thing is done; the primary Mind seat reviews it.
> A compensation is an Operation module whose name begins `compensation-`, welded in by a flow so the system runs; a trial is an Operation module whose name begins `trial-`, being tried.
> A seat's identity is an Operation module, marked user-only.

## Proposal 11: the distillation line
**vision** · Curriculum `skills/psyche-distillation.md`, after line 25
### Now, line 25
```
A distilled statement carries what the psyche said and nothing beyond it; a small ruling makes a small statement, never a theory grown around the words.
```
### Proposed, added after it
> A proposal is small, conservative and general, and infers nothing; it is accepted whole or not at all.
> An order, an instruction for a situation, or an intervention is not distilled into a rule; it stays in the log.

## Rulings
1. **The set of types**, in Proposals 4 and 10. (a) Six: compensation and trial are Operation modules by name prefix. (b) Eight: Compensation and Trial are types of their own, added to `ModuleType` and to Proposal 10.
2. **The qualifying rule**, and the standard around it (Proposal 1): yes, or amend by line.
3. **The five first modules and the psyche-primary text** (Proposals 6 and 7): yes, or amend.
4. **The implementation** (Proposals 3, 4, 5, 6, 7, 8, 9): (a) one yes, built in that order. (b) comment what changes.
5. **Codex.** Now Flow keeps Codex's stock base instructions, 21,420 characters, and opens the first turn with the bundle. (a) The SystemPrompt placement replaces its base instructions; the main-only part goes in developer instructions, which a collaborator does not receive. (b) Keep stock on Codex for now.
6. **Queued** (Proposal 2): (a) a fourth placement. (b) keep three placements; the hook is Flow's affair, not a placement.
7. **The distillation line** (Proposal 11): yes, or amend.
<!-- to-the-living:end -->
