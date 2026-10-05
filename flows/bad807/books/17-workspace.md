<!-- to-the-living:start -->
Presentation.{ «Three skill repositories and the main workspace» }

> ... restart on actually using the repos psyche, mind, and field for their respective skills for their respective types, using different repos because it scales better. Migrate all of the vision and anything like the current vision, which ought to become a skill, and then merge that with whatever is in the skill now. ... We have to find the right place, the right home for everything, and [bootstrap] on this infrastructure.

-- psyche, STT, 2026-10-04, relayed; words omitted by the relay marked ` ... `.

> Maybe we don't call it primary because it conflicts with the layers. Maybe all we call it is main workspace.

-- psyche, STT, 2026-10-04, relayed.

One edition of three books: the workspace design, the placing, and the two lines. **[vision]** enters on your approval; **[implementation]** is built on your yes. Nothing is built yet.

## How it is now

```
psyche-skills, mind-skills, field-skills   README.md only, each ending:
                                           "The layout inside is not yet decided. Nothing is to be added until it is."
Curriculum skills/                         70 sources, one flat directory
                                           39 unprefixed · trial- 12 · compensation- 7 · knowledge- 5 · operation- 4 · vision- 3
Vision/                                    20 topic files, 18 sources
Intent/                                    10 topic files, 7 sources
vision-raw/                                90 files
flows/*/vision/, flows/*/notion/           the raw records
curriculum-deploy 0.9.0                    takes three sources, one per aspect; refuses a name defined twice
PRIMARY-SKELETON.md                        a new repository of nine tracked files, named primary
```

## What stands now

```
No Role type          no role/ directories; a seat's identity module is an Operation module of its aspect;
                      a role is the record that selects modules, not a module type
field/operation       the how-to of the running system, under plain names
compensation-, trial- prefixes for welds and trials, inside field/operation
Names                 unique by deployed name <type>-<stem>; a stem may recur under two types
bootstrap/manifest    operative: the bootstrap reads it, with a schema Mind writes
The migration         prepared: 100 rows, 125 writes, dry run only
                      parametric on your three answers (rulings 6, 7, 8)
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 370" width="700" font-family="sans-serif" font-size="13" role="img" aria-label="Three skill repositories feed the main workspace through curriculum-deploy"><defs><marker id="w1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3d4654"/></marker></defs><rect width="700" height="370" rx="10" fill="#f7f8fb"/><rect x="10" y="14" width="220" height="112" rx="8" fill="#e6e9f7" stroke="#4a55a8" stroke-width="2"/><rect x="240" y="14" width="220" height="112" rx="8" fill="#e1f0e4" stroke="#3c7a4a" stroke-width="2"/>
<rect x="470" y="14" width="220" height="112" rx="8" fill="#f7e5e1" stroke="#a8523f" stroke-width="2"/><g fill="#1d2430"><g font-weight="bold" font-size="16"><text x="24" y="40">psyche-skills</text><text x="254" y="40">mind-skills</text><text x="484" y="40">field-skills</text></g><text x="24" y="66">spirit/  intent/</text><text x="24" y="86">vision/  notion/</text><text x="254" y="66">operation/</text><text x="254" y="86">knowledge/</text><text x="484" y="66">operation/  knowledge/</text><text x="484" y="86">plain names; welds prefixed</text></g>
<g fill="#5d6762" font-size="12"><text x="24" y="114">what is wanted, and why</text><text x="254" y="114">how it is done; by design</text><text x="484" y="114">what runs now; what holds it</text></g><rect x="210" y="166" width="280" height="50" rx="8" fill="#ffffff" stroke="#3d4654" stroke-width="1.5"/><g fill="#1d2430" text-anchor="middle"><text x="350" y="187" font-weight="bold" font-size="14">curriculum-deploy</text><text x="350" y="206">one catalog, keyed by &lt;type&gt;-&lt;stem&gt;</text></g><g stroke="#3d4654" stroke-width="1.6" fill="none" marker-end="url(#w1)"><path d="M120,126 L270,164"/><path d="M350,126 V164"/><path d="M580,126 L430,164"/><path d="M350,216 V244"/></g><rect x="10" y="246" width="680" height="114" rx="8" fill="#f5efd5" stroke="#8a7a2a" stroke-width="2"/>
<g fill="#1d2430"><text x="24" y="272" font-weight="bold" font-size="16">main-workspace</text><text x="24" y="296">entry files, flake, bootstrap/manifest.datom naming the mounts</text><text x="24" y="318">mounts: psyche-, mind-, field-skills  ·  psyche-, mind-, field-logs  ·  flow-data</text><text x="24" y="340">generated: .claude  .agents  .codex  .pi</text></g><text x="676" y="340" fill="#5d6762" font-size="12" text-anchor="end">never edited by hand</text>
</svg>

*Three repositories hold the modules by type; the generator writes them into the main workspace.*

## Proposals

### 1. Where a module belongs
[vision] `Vision/skills.md`, a new file; home today, it migrates with the rest.

**Now:** no such file. The topic is placed as `psyche/vision/skills`, from skill-designing's Skill types.

**Proposed:**
```
Where a module belongs

A module belongs to the aspect whose question it answers.
Psyche answers what is wanted and why: Spirit, Intent, Vision and Notion live in the psyche repository and nowhere else.
Mind answers how a thing is done and what it is by design: Operation and Knowledge of design live in the mind repository.
Field answers what runs now and what holds it together: Knowledge of the running system,
and the Operation modules that are its how-to, live in the field repository; a weld or a trial there is named compensation- or trial-.
A seat's identity module is an Operation module of the seat's aspect.
A text that answers two questions is split, each part to its home.
The flows of an aspect edit the modules that are theirs; a change wanted in another aspect's repository is asked of that aspect.
```

### 2. The layout of each repository
[implementation] `psyche-skills`, `mind-skills`, `field-skills`.

**Now:** each holds `README.md` only: "The layout inside is not yet decided. Nothing is to be added until it is."

**Proposed:** one directory per type, one module per file, the file stem its name, frontmatter the description only.
```
psyche-skills/   spirit/  intent/  vision/  notion/
mind-skills/     operation/  knowledge/
field-skills/    operation/  knowledge/

deployed name    <type>-<stem>; Spirit deploys as spirit
example          field-skills/operation/compensation-messenger-clj.md  →  operation-compensation-messenger-clj
example          field-skills/operation/nix-workflow.md                →  operation-nix-workflow
```
Each README becomes two lines: the aspect in charge, and the rule of Proposal 1.

### 3. The generator's source type
[implementation] `curriculum-deploy/curriculum-deploy.ethos`. The types are declared here, once.

**Now:**
```
SkillSource.[ Psyche.String Mind.String Field.String ]
Configuration.{ String Vector<SkillSource> String }
```

**Proposed:**
```
ModuleType.[ Spirit Intent Vision Notion Knowledge Operation ]
Allowed.{ Aspect Vector<ModuleType> }
SkillSource.[ Psyche.Path Mind.Path Field.Path ]
Configuration.{ Path Vector<SkillSource> Path }

Psyche   [ Spirit Intent Vision Notion ]
Mind     [ Operation Knowledge ]
Field    [ Operation Knowledge ]
```
- Each source path is a repository root; the generator walks the type directories allowed to that aspect, and refuses any other.
- It keys its catalog by deployed name, and refuses one deployed name defined twice across the three.

### 4. The migration
[implementation] Primary's psyche and Curriculum's skills into the three repositories.

**Now:** 100 items in two places: 70 Curriculum skills, 20 Vision files, 10 Intent files.

**Proposed:** the placing table, as the flow ruled it. Modules by target, with ruling 6 at vision:
```
psyche/spirit       1        mind/operation     16        field/operation    33
psyche/vision      24        mind/knowledge      4        field/knowledge    11
psyche/intent      10        psyche-logs/legacy  1 (not a module)
```
- With ruling 6 at intent, five modules move: psyche/vision 19, psyche/intent 15.
- Twelve rows split; each part cites its source and lines, cut only.
- Six stems recur under two types: flow, nexus, ethos, messaging, orchestrate, testing.
- `vision-raw/` drains into `psyche-logs/` under the flow that heard each record, or `legacy/`; `flows/*/vision/` and `flows/*/notion/` move to `psyche-logs/<flow>/`.
- Dependency lists are rewritten to deployed names; one that maps to nothing refuses the run.

The ten design rulings the flow made on the doubtful items:

| Item | Question | Ruled |
|---|---|---|
| 1 | Thirteen how-to skills in field | stay in field/operation, plain names |
| 2 | Psyche procedures (acquisition, grasp, distillation's procedure) | mind/operation; their vision parts to psyche/vision |
| 4 | main-flow | mind/operation |
| 5 | design, realization | mind/operation |
| 7 | The two flow vision files | merged as vision/flow |
| 8 | datom and protos skills repeating the vision | the skill merges into the vision module |
| 9 | Vision and Intent sources | beside their modules, in psyche-skills |
| 11 | stale-lock | field/operation/stale-lock |
| 12 | A subject split across mind and field knowledge | the field part takes the running thing's name |
| 13 | psyche-interraction | the spelling stays |

### 5. The main workspace
[vision] `Vision/workspace.md`, a new file; home today.

**Now:** no such file.

**Proposed:**
```
Workspace

The main workspace is a bare template that expects its repositories mounted in it.
It holds nothing of its own but its entry files, its Nix flake, and the generated trees the harnesses read.
The three skill repositories, the three logs repositories and the flow data are mounted in it, each a repository of its own.
A flow edits a module in the repository of its aspect; the generator writes the trees; nothing under a generated tree is edited by hand.
It is called main, not primary, because primary names a layer.
```

### 6. The repository main-workspace
[implementation] a new repository, `main-workspace`.

**Now:** `PRIMARY-SKELETON.md` draws it as primary, with `primary-records/psyche`, `primary-records/workspace` and `flow-data` beside it:
```
primary/
  .gitignore  README.md  ARCHITECTURE.md  SKILL_VARIABLES.md  AGENTS.md  CLAUDE.md
  bootstrap/manifest.datom
  bootstrap/skills/workspace-primary/SKILL.md  bootstrap/skills/provisioning-primary/SKILL.md
```
Its manifest is "proposed deployment data", with no consumer.

**Proposed:**
```
main-workspace/
  README.md  ARCHITECTURE.md  CLAUDE.md  AGENTS.md  flake.nix  flake.lock  .gitignore
  bootstrap/
    manifest.datom        names the mounts and their repositories; read by the bootstrap; schema by Mind
mounts
  psyche-skills  mind-skills  field-skills
  psyche-logs  mind-logs  field-logs
  flow-data               today's flows/: logs, reports, index
```
- `SKILL_VARIABLES.md` is not tracked; its values become Knowledge modules in field. Primary stays as an archive, read by no flow.
- Mind builds the generator change and the bootstrap; the secretary runs the migration.

## Two lines of your vision touched

Both follow from no Role type, and from "Where psyche lives" moving to Field's knowledge.

### Line 1: `Curriculum skills/psyche.md`, lines 24–26

**Now:**
```
"Psyche" alone means the written psyche, the records named under
Where psyche lives;
the living psyche is always called the living psyche, or the living.
```
**Proposed:**
```
"Psyche" alone means the written psyche, the records; the living psyche is always called the living psyche, or the living.
Where the records sit is in Field's knowledge module psyche-records.
```

### Line 2: `Curriculum skills/skill-designing.md`, lines 66–67

**Now:**
```
A role skill carries an aspect's identity and names its
dependencies. Mark role skills user-only.
```
**Proposed:**
```
A seat's identity module is an Operation module of the seat's aspect, marked user-only.
```

## Rulings

Each: the options. Answer by number.
```
1  The rule of belonging (Proposal 1)      yes, or amend by line
2  Knowledge                               a  split by what it knows: design to mind, the running system to field
                                           b  all Knowledge to mind
                                           the placing table is built on a
3  Deployed names                          a  <type>-<stem> for every type but Spirit
                                           b  psyche's modules deploy unprefixed, as the gold skills do today
4  The migration's first placing           yes: the hundred rows and the ten rulings above, as one; or name rows
5  The name main-workspace and its mounts  yes, or amend
6  The conduct rules                       behavior, correction, vocabulary, the rest of psyche-interraction, skill types
                                           a  vision/
                                           b  intent/
7  File stems                              Vision and Intent are camelCase; skills are kebab-case
                                           a  keep each as it is
                                           b  all kebab-case
                                           c  all camelCase
                                           the prepared script takes b or c; a needs one more value
8  The prefix paragraph of Vision/psyche   a  Proposal 1 supersedes it, and it goes
                                           b  it stays as written
9  Line 1, psyche.md 24–26                 yes, or amend
10 Line 2, skill-designing.md 66–67        yes, or amend
```
<!-- to-the-living:end -->
