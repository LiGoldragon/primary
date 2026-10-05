<!-- to-the-living:start -->
Presentation.{ «Context modules» }

What a flow starts its thinking with: the standard, the files it touches, and the code of each change.
Marks: **vision** is what is wanted; it enters on your word. **today** is explanation, witnessed in the cited file. **implementation** is built on your yes. Code marked **proposed** exists in no file yet.

## Your comments on the last edition
Each comment is quoted under the passage it was anchored to.

1. Anchored to: "A context module is one file of what a flow starts its thinking with. A context module is one file of prompt text with a type, a name and a description."
   Your comment: "We shouldn't say that."
   Reply: Your comment answered only that heading and that sentence, not the whole block. Both are removed.
2. Anchored to: "Three placements. A module reaches a flow in one of three places…"
   Your comment: "universal statements that aren't true for all harnesses."
   Reply: The placements now read as what we want. A separate table shows which harnesses do it today, with the launcher code behind it.
3. Anchored to: the same passage, "Three placements."
   Your comment: "it feels a bit strong and unnecessary."
   Reply: The forks and subagents claims are cut. Only the three placements and one line each remain.
4. Anchored to: "A role. A role is one record naming, for each placement, its modules by type, and its model…"
   Your comment: "redo this with example code."
   Reply: Every proposal now shows the code there now and the code that replaces it, each with its path. The role is shown as the actual datom record.

## Where things are now
```
Skill sources      /git/github.com/LiGoldragon/Curriculum/skills/<name>.md        71 flat files
Role data          /git/github.com/LiGoldragon/Curriculum/roles.datom             one Roles record
Generator          /git/github.com/LiGoldragon/curriculum-deploy                  types in curriculum-deploy.ethos
Main-flow prompt   /home/li/primary/tools/main-flow-mode/system-prompt.md         15 lines, outside Curriculum
Launchers          /home/li/primary/tools/{claude,codex,opencode}-main-flow-launch.mjs
Migration          /home/li/primary/flows/aa887c/scripts/migrate-skills.sh        to psyche-, mind-, field-skills; not run
```

### today: how the skill trees are made
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 300" width="360" font-family="system-ui,sans-serif" role="img" aria-label="Curriculum skills and roles.datom go through curriculum-deploy into the generated skill trees and agent definitions"><rect width="360" height="300" rx="10" fill="#f7f8fb"/><rect x="14" y="14" width="154" height="58" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="192" y="14" width="154" height="58" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><g text-anchor="middle" fill="#1d2430"><text x="91" y="38" font-size="13" font-weight="700">skills/*.md</text><text x="91" y="58" font-size="11">Curriculum, 71 files</text><text x="269" y="38" font-size="13" font-weight="700">roles.datom</text><text x="269" y="58" font-size="11">Curriculum, one record</text></g><g stroke="#4a5361" stroke-width="1.6" fill="none"><path d="M91 72 L160 112"/><path d="M269 72 L200 112"/></g><polygon points="156,106 166,116 153,115" fill="#4a5361"/><polygon points="204,106 194,116 207,115" fill="#4a5361"/><rect x="70" y="116" width="220" height="58" rx="8" fill="#fff1d6" stroke="#b07a12"/><g text-anchor="middle" fill="#1d2430"><text x="180" y="140" font-size="13" font-weight="700">curriculum-deploy</text><text x="180" y="160" font-size="11">types declared in curriculum-deploy.ethos</text></g><g stroke="#4a5361" stroke-width="1.6" fill="none"><path d="M140 174 L91 210"/><path d="M220 174 L269 210"/></g><polygon points="88,204 86,215 96,209" fill="#4a5361"/><polygon points="272,204 274,215 264,209" fill="#4a5361"/><rect x="14" y="214" width="154" height="70" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="192" y="214" width="154" height="70" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/><g text-anchor="middle" fill="#1d2430"><text x="91" y="234" font-size="12" font-weight="700">skill trees</text><text x="91" y="252" font-size="11">.claude/skills</text><text x="91" y="266" font-size="11">.agents/skills</text><text x="91" y="280" font-size="11">.opencode/skills</text><text x="269" y="234" font-size="12" font-weight="700">subagent definitions</text><text x="269" y="252" font-size="11">.claude/agents</text><text x="269" y="266" font-size="11">.codex/agents</text><text x="269" y="280" font-size="11">.pi/agents</text></g></svg>

Figure 1. *Today: Curriculum's skill files become the skill trees; roles.datom becomes the subagent definitions.*

### today: where a module reaches each harness
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 330" width="360" font-family="system-ui,sans-serif" role="img" aria-label="Table of the three placements against Claude, Codex and OpenCode main flows and subagents, as the launchers do it today"><rect width="360" height="330" rx="10" fill="#f7f8fb"/><g font-size="11" font-weight="700" fill="#1d2430" text-anchor="middle"><text x="126" y="26">Claude</text><text x="126" y="40">main</text><text x="194" y="26">Codex</text><text x="194" y="40">main</text><text x="262" y="26">OpenCode</text><text x="262" y="40">main</text><text x="326" y="26">sub-</text><text x="326" y="40">agents</text></g><g font-size="12" font-weight="700" fill="#1d2430"><text x="10" y="86">System</text><text x="10" y="101">prompt</text><text x="10" y="166">First</text><text x="10" y="181">prompt</text><text x="10" y="246">Loadable</text></g><g stroke-width="1.3"><rect x="94" y="56" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="162" y="56" width="64" height="70" rx="7" fill="#fbe3e0" stroke="#b0453a"/><rect x="230" y="56" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="298" y="56" width="56" height="70" rx="7" fill="#e6ecfa" stroke="#3b5bab"/><rect x="94" y="136" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="162" y="136" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="230" y="136" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="298" y="136" width="56" height="70" rx="7" fill="#eceef1" stroke="#8a929e"/><rect x="94" y="216" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="162" y="216" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="230" y="216" width="64" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="298" y="216" width="56" height="70" rx="7" fill="#ddf1e4" stroke="#2f7d4a"/></g><g font-size="10.5" fill="#1d2430" text-anchor="middle"><text x="126" y="84">replaced</text><text x="126" y="100">system-</text><text x="126" y="113">prompt-file</text><text x="194" y="84">stock kept</text><text x="194" y="100">no override</text><text x="194" y="113">passed</text><text x="262" y="84">replaced</text><text x="262" y="100">agent</text><text x="262" y="113">prompt</text><text x="326" y="84">its own</text><text x="326" y="100">definition</text><text x="326" y="113">body</text><text x="126" y="164">/name</text><text x="126" y="180">commands</text><text x="126" y="194">+ brief</text><text x="194" y="164">skill text</text><text x="194" y="180">inlined</text><text x="194" y="194">+ brief</text><text x="262" y="164">skill text</text><text x="262" y="180">inlined</text><text x="262" y="194">+ brief</text><text x="326" y="172">the brief</text><text x="326" y="188">only</text><text x="126" y="248">skill tree</text><text x="126" y="264">by name</text><text x="194" y="248">skill</text><text x="194" y="264">catalog</text><text x="262" y="248">skill tree</text><text x="262" y="264">by name</text><text x="326" y="248">its own</text><text x="326" y="264">catalog</text></g><g font-size="10.5" fill="#4a5361"><rect x="10" y="302" width="10" height="10" fill="#ddf1e4" stroke="#2f7d4a"/><text x="24" y="311">as wanted</text><rect x="86" y="302" width="10" height="10" fill="#fbe3e0" stroke="#b0453a"/><text x="100" y="311">not as wanted</text><rect x="180" y="302" width="10" height="10" fill="#e6ecfa" stroke="#3b5bab"/><text x="194" y="311">generated</text><rect x="258" y="302" width="10" height="10" fill="#eceef1" stroke="#8a929e"/><text x="272" y="311">none</text></g></svg>

Figure 2. *Today, per harness. Sources: the launchers below, and the claude-harness and codex-harness skills.*

The launcher code behind Figure 2:

`tools/claude-main-flow-launch.mjs`, lines 34, 100, 110, 198 (excerpt)
```js
export const BIRTH_SKILLS = ['main-flow', 'spirit', 'psyche', 'psyche-interraction', 'vocabulary', 'edit-coordination'];
  const prompt = `${BIRTH_SKILLS.map(n => `/${n}`).join(' ')} # Launch brief\n\n${brief.trim()}\n`;
  const promptFile = systemPromptFile ?? path.join(modeDir, 'system-prompt.md');
  … claude … --system-prompt-file ${sh(mode.promptFile)} … "$(cat ${sh(promptFile)})"
```

`tools/codex-main-flow-launch.mjs`, lines 61, 64, 67 and 82 (excerpt): the skill text goes into the first prompt; no `model_instructions_file` is passed, so Codex keeps its stock base instructions.
```js
  const blocks = ['main-flow', ...ASPECT_SKILLS[aspect]].map(name => { … return skillBlock(workspace, name, text); });
  const prompt = `${blocks.join('\n')}\n# Launch brief\n\n${brief.trim()}\n`;
  return `exec env … ${sh(client.expectedPath)} -m ${sh(o.model)} -c 'model_reasoning_effort="medium"' --dangerously-bypass-approvals-and-sandbox -C ${sh(o.workspace)} "$(cat ${sh(promptFile)})"`;
```

`tools/opencode-main-flow-launch.mjs`, lines 74 to 78
```js
// The main-flow mode: the agent whose prompt replaces OpenCode's own.
export function seatConfig(systemPrompt, model) {
  if (!systemPrompt.trim()) throw new Error('main-flow system prompt is empty');
  return {agent: {[AGENT]: {description: 'A main flow seat.', mode: 'primary', model, prompt: systemPrompt}}};
}
```

`curriculum-deploy/src/roles.rs`, `packet` (excerpt): a subagent's definition body is the role modules joined; on Codex it is written as `developer_instructions`, not as base instructions.
```rust
        for module_id in &self.string_vector {
            modules.push(self.module(module_id)?);
        }
        let body = modules.join("\n\n");
        // ClaudeAgent → .claude/agents/{identifier}.md, body after the frontmatter
        // CodexAgent  → .codex/agents/{identifier}.toml, developer_instructions = body
```

## Proposal 1: the standard
**vision** · create `/home/li/primary/Vision/contextModules.md`

Now: no such file. Proposed, whole:
> **Context modules**
>
> **Types**
> A module's type says who stands behind it and where it may go; a name is unique within its type.
> The types are declared once, in the generator's ethos; no other text lists them.
>
> **Three placements**
> We want a module to reach a flow in one of three places.
> The system prompt replaces the harness's own prompt.
> The first prompt is the launch turn: what this flow does now.
> Loadable modules are loaded by name when a situation calls.
>
> **A role**
> A role is one record naming, for each placement, its modules by type, and its model. Flow composes the launch from that record with no model in the loop.
>
> **What qualifies for the system prompt**
> A module goes in the system prompt when it is steady, changing only on the living's word; when it addresses the role's whole run, never a task; and when it must be present before the first tool call or must hold against the harness's own guidance.
> Distilled spirit, intent and vision qualify; raw records never do. A seat's identity module qualifies.
> Knowledge is loadable, because it changes with the system. Any other Operation module goes in the first prompt or stays loadable.
>
> **What makes a module high quality**
> Every line is a definition or a rule in the present tense, leading with what is wanted. Each line traces to a record of the living or to a witness.
> One fact lives in one module. A module carries no history, no objection, and no unknown where a measurement is possible.
> It uses our terms, not a vendor's, except where a harness is named. It fits its placement's budget, and the budget is measured.

Removed from the last edition: the heading and sentence of your comment 1; "it reaches the main flow and its forks, never its subagents"; "they are the only placement a subagent reaches"; "the skill tree".

## Proposal 2: Queued, a fourth placement
**vision** · **proposed, unruled** · Proposal 1, after Loadable; and the `Placement` line of Proposal 4

Today: the Claude launcher's `UserPromptSubmit` hook re-injects the first five paragraphs of the system prompt every 20th prompt (`tools/claude-main-flow-launch.mjs`, lines 112 and 113; `tools/main-flow-mode/reminder-hook.py`).
```js
  const hook = ['python3', sh(path.join(modeDir, 'reminder-hook.py')), '--prompt-file', sh(promptFile),
    '--state-dir', sh(path.join(jobDir, 'main-flow-reminder')), '--every', '20'].join(' ');
```
Proposed:
> Queued context enters a running flow between its turns: what Flow has queued for that flow, carried into its next incoming message.
```
Placement.[ SystemPrompt FirstPrompt Loadable Queued ]
```

## Proposal 3: the types, declared once
**implementation** · `/git/github.com/LiGoldragon/curriculum-deploy/curriculum-deploy.ethos`, lines 25 and 32

Now:
```
  RoleModule.{ String String }
  Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth> Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> }
```
**proposed**, replacing those two lines:
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
- `RoleModule` goes: a role's text is a module file.
- `Vector<String>` and `TargetInsertion` go: a subagent's definition body is its own SystemPrompt selections.

## Proposal 4: the module file
**implementation** · each skill file moves to `<repository>/<type>/<name>.md`; the frontmatter is unchanged

The type is the directory; no `type:` line (ruling 1 of the migration, `flows/aa887c/scripts/migrate-skills.sh`).

Now, `Curriculum/skills/spirit.md`, lines 1 to 4:
```
---
description: Every agent task.
dependencies: [behavior, correction, vocabulary]
---
```
Now, `curriculum-deploy/src/catalog.rs`, `DeclaredSource::skills` (excerpt): the name is the file stem.
```rust
                let name = path
                    .file_stem()
                    .expect("markdown stem")
                    .to_string_lossy()
                    .into_owned();
```
Proposed placement, `flows/aa887c/scripts/migrate-skills.sh`, manifest rows (excerpt; `repository|type|name|…`):
```
psyche|spirit|spirit|1|whole:$CUR/spirit.md
psyche|vision|contextModules|105|whole:$SPL/books/psyche-vision-contextModules.md
mind|operation|main-flow|11|…
mind|operation|psyche-primary|101|whole:$SPL/books/mind-operation-psyche-primary.md
field|knowledge|flow|45,11|whole:$CUR/knowledge-flow.md …
```
**proposed**: the generator reads the three repositories into one `Manifest`, one record per file:
```
[ { Spirit spirit Path.«/git/github.com/LiGoldragon/psyche-skills/spirit/spirit.md» }
  { Vision contextModules Path.«/git/github.com/LiGoldragon/psyche-skills/vision/contextModules.md» }
  { Operation main-flow Path.«/git/github.com/LiGoldragon/mind-skills/operation/main-flow.md» }
  { Knowledge flow Path.«/git/github.com/LiGoldragon/field-skills/knowledge/flow.md» } ]
```

## Proposal 5: the standard as a loadable module
**implementation** · create `psyche-skills/vision/contextModules.md` (manifest row 105)

**proposed**:
```
---
description: A context module, its type or its placement is being designed, edited or judged.
---
<the body of Proposal 1, without its title>
```
The cut text it copies, `flows/aa887c/scripts/splits/books/psyche-vision-contextModules.md`, still holds the last edition's lines and is re-cut from this one.

## Proposal 6: one main-flow module
**implementation** · `mind-skills/operation/main-flow.md` takes the fifteen lines of `tools/main-flow-mode/system-prompt.md`; that file is removed

Now, `Curriculum/skills/main-flow.md`, lines 1 to 8 (excerpt):
```
---
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, …
Use subflows for investigation, implementation, probes, and verification.
```
Now, `tools/main-flow-mode/system-prompt.md`, line 1 of 15:
```
You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.
```
**proposed**, `mind-skills/operation/main-flow.md`:
```
---
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---

You are a main flow: one of the twelve seats that extend the living psyche. Your aspect and your power are given in your startup prompt.
<the other fourteen lines of tools/main-flow-mode/system-prompt.md, unchanged>

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, …
```
- Removed from main-flow.md: lines 8, 10, 11, 17, 18 and 51, which the system prompt repeats.

## Proposal 7: the psyche-primary module
**implementation** · create `mind-skills/operation/psyche-primary.md` (manifest row 101)

Now: the seat's identity is in the launch brief only. **proposed**, whole, from `flows/aa887c/scripts/splits/books/mind-operation-psyche-primary.md`:
```
---
description: The seat is the Psyche voice at the Primary layer.
user-only: true
---
You are the Psyche voice at the Primary layer: the seat that hears the living and designs what the machines start their thinking with.

What the living must read, rule on or approve goes whole into the living messenger as a presentation; he answers by number. Chat is unread.

You design, rule and judge. The Secondary builds and tests what you hand down.
```

## Proposal 8: the role record
**implementation** · `Curriculum/roles.datom`

Now, `Curriculum/roles.datom` (excerpt): the role texts are inline strings; no main-flow role.
```
Roles.{ [ { general-instructions «The brief is your authority. Decide what it settles; return what it does not.» }
          { codex-skill-loading «Do not reload a complete pasted skill unless freshness or source verification is required.» }
          { spirit-role «The purpose of AI is to extend a psyche. …» }
          { intent-role «Every layer carries its own context. …» }
          { subflow-role «Your flow is `FLOW_ID` and `FLOW_DIRECTORY` in your environment. …» } ]
        …
        [ general-instructions spirit-role intent-role subflow-role ]
        [ { general-instructions CodexAgent [ codex-skill-loading ] } ] }
```
**proposed**, the Psyche Primary role, whole, from `flows/aa887c/scripts/roles/psyche-primary.datom`:
```
{ Voice.{ Psyche Primary }
  [ { SystemPrompt [ { Spirit [ spirit ] }
                     { Operation [ main-flow psyche-primary ] }
                     { Vision [ vocabulary psyche ] } ] }
    { FirstPrompt [ { Operation [ psyche-logging edit-coordination ] } ] }
    { Loadable [ { Vision [ context-modules flow ethos nexus psyche-interraction ] }
                 { Knowledge [ nexus flow ethos ] } ] } ]
  { claude-fable-5-1 None } }
```
- `spirit-role` and `intent-role` repeat existing text: subagents select `{ Spirit [ spirit ] }` and `{ Intent [ context ] }`.
- `general-instructions`, `codex-skill-loading` and `subflow-role` become `mind-skills/operation/` files, bodies unchanged (manifest rows 102 to 104).
- The record names `context-modules`; the manifest names `contextModules`. One spelling follows the stem-case ruling (open item 6 of the migration).

## Proposal 9: Flow composes the launch from the role
**implementation** · replaces `BIRTH_SKILLS`, `ASPECT_SKILLS` and the fixed system-prompt path in the three launchers; Flow takes this step when Flow launches

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 360" width="360" font-family="system-ui,sans-serif" role="img" aria-label="Proposed: the role record and the manifest go into composeLaunch, which yields a system prompt, a first prompt and a loadable tree for the harness"><rect width="360" height="360" rx="10" fill="#f7f8fb"/><g stroke-dasharray="6 4" stroke-width="1.4"><rect x="14" y="14" width="154" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="192" y="14" width="154" height="56" rx="8" fill="#e6ecfa" stroke="#3b5bab"/><rect x="80" y="106" width="200" height="50" rx="8" fill="#fff1d6" stroke="#b07a12"/></g><g text-anchor="middle" fill="#1d2430"><text x="91" y="38" font-size="13" font-weight="700">role record</text><text x="91" y="56" font-size="11">psyche-primary.datom</text><text x="269" y="38" font-size="13" font-weight="700">Manifest</text><text x="269" y="56" font-size="11">type + name → path</text><text x="180" y="128" font-size="13" font-weight="700">composeLaunch</text><text x="180" y="146" font-size="11">no model in the loop</text></g><g stroke="#4a5361" stroke-width="1.6" fill="none"><path d="M91 70 L150 103"/><path d="M269 70 L210 103"/><path d="M130 156 L62 196"/><path d="M180 156 L180 196"/><path d="M230 156 L298 196"/></g><g fill="#4a5361"><polygon points="146,97 156,106 143,105"/><polygon points="214,97 204,106 217,105"/><polygon points="60,190 57,201 67,197"/><polygon points="175,192 180,202 185,192"/><polygon points="300,190 303,201 293,197"/></g><g stroke-width="1.4"><rect x="10" y="204" width="106" height="62" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="127" y="204" width="106" height="62" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/><rect x="244" y="204" width="106" height="62" rx="8" fill="#ddf1e4" stroke="#2f7d4a"/></g><g text-anchor="middle" fill="#1d2430"><text x="63" y="226" font-size="12" font-weight="700">system prompt</text><text x="63" y="243" font-size="10.5">bodies joined,</text><text x="63" y="257" font-size="10.5">in order</text><text x="180" y="226" font-size="12" font-weight="700">first prompt</text><text x="180" y="243" font-size="10.5">its modules,</text><text x="180" y="257" font-size="10.5">then the brief</text><text x="297" y="226" font-size="12" font-weight="700">loadable</text><text x="297" y="243" font-size="10.5">the generated</text><text x="297" y="257" font-size="10.5">skill tree</text></g><g stroke="#4a5361" stroke-width="1.6" fill="none"><path d="M63 266 L63 296"/><path d="M180 266 L180 296"/><path d="M297 266 L297 296"/></g><g fill="#4a5361"><polygon points="58,292 63,302 68,292"/><polygon points="175,292 180,302 185,292"/><polygon points="292,292 297,302 302,292"/></g><rect x="10" y="304" width="340" height="44" rx="8" fill="#eceef1" stroke="#4a5361"/><g text-anchor="middle" fill="#1d2430"><text x="180" y="323" font-size="12" font-weight="700">the harness</text><text x="180" y="340" font-size="10.5">Claude: --system-prompt-file · OpenCode: agent prompt · Codex: Ruling 4</text></g></svg>

Figure 3. *Proposed: dashed boxes do not exist yet.*

Now: the composition is hard-coded per launcher (the excerpts under Figure 2).

**proposed**, one function the launchers share (no such file today):
```js
// Proposed. role: the parsed role record; manifest: Map of `${type} ${name}` → path.
const body = text => text.replace(/^---\n[\s\S]*?\n---\n/, '').trim();
export function composeLaunch(role, manifest, brief, read) {
  const paths = placement => (role.placed.find(p => p.placement === placement)?.selections ?? [])
    .flatMap(({type, names}) => names.map(name => {
      const found = manifest.get(`${type} ${name}`);
      if (!found) throw new Error(`no module ${type} ${name}`);
      return found;
    }));
  return {
    systemPrompt: paths('SystemPrompt').map(p => body(read(p))).join('\n\n'),
    firstPrompt: `${paths('FirstPrompt').map(p => body(read(p))).join('\n\n')}\n# Launch brief\n\n${brief.trim()}\n`,
    model: role.model,
  };
}
```

## Proposal 10: skill-designing's types
**vision** · `Curriculum/skills/skill-designing.md`, lines 55 to 59 and 66 to 67

Now:
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
Proposed, replacing those lines:
> A skill is a context module; its type, declared in the generator's ethos, says who stands behind it and where it may go.
> Spirit, Intent, Vision and Notion are the living's: distilled on his word, changed on his word.
> Knowledge is what a flow found out about the system as it is; any flow may load it. Operation is how a thing is done; the primary Mind seat reviews it.
> A compensation is an Operation module whose name begins `compensation-`, welded in by a flow so the system runs; a trial is an Operation module whose name begins `trial-`, being tried.
> A seat's identity is an Operation module, marked user-only.

## Proposal 11: the distillation line
**vision** · `Curriculum/skills/psyche-distillation.md`, after line 25

Now, line 25:
```
A distilled statement carries what the psyche said and nothing beyond it; a small ruling makes a small statement, never a theory grown around the words.
```
Proposed, added after it:
> A proposal is small, conservative and general, and infers nothing; it is accepted whole or not at all.
> An order, an instruction for a situation, or an intervention is not distilled into a rule; it stays in the log.

## Rulings
1. **The set of types** (Proposals 3 and 10). (a) Six: compensation and trial are Operation modules by name prefix. (b) Eight: Compensation and Trial are types of their own.
2. **The standard** (Proposal 1): yes, or amend by line.
3. **The main-flow and psyche-primary modules** (Proposals 6 and 7): yes, or amend.
4. **Codex.** Today the Codex launcher keeps the stock base instructions and puts the skill text in the first prompt (Figure 2). (a) The system prompt replaces the base instructions through `model_instructions_file`. (b) Keep stock on Codex for now.
5. **The implementation** (Proposals 3 to 9): (a) one yes, built in that order. (b) comment what changes.
6. **Queued** (Proposal 2): (a) a fourth placement. (b) three placements; the hook stays Flow's affair.
7. **The distillation line** (Proposal 11): yes, or amend.
<!-- to-the-living:end -->
