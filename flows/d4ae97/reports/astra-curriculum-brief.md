# Mind Astra: rebuild the curriculum deploy

Written by Psyche Opus d4ae97, your secretary, on 2026-10-07. You succeed Mind Astra f768df, which is retired.

## The order

The living's order is absolute. Finish the curriculum deploy, deploy it, and witness it working. Never bring him a question.

- Where his words settle a point, decide it as they say.
- Where they are silent, choose the simplest thing that works. He wants it dirty first: "We're going to make this really dirty just so that it works."
- Record each choice you make in your own log, `flows/<your id>/log.md`.
- Newer words outrank older ones. An older instruction stands only where nothing newer overrides it.

## The target, as his words give it

### Curriculum repository

The Curriculum repository holds Rust only: the CLI and the Curriculum Nexus. It holds no skill. Its `skills/` directory moves out, and `roles.datom` goes with the code or into a skill repository, whichever is simplest.

### Three skill repositories

There are three skill repositories: `psyche-skills`, `mind-skills` and `field-skills`. They already exist, each holding only a README. Each gets a `skills/` directory.

Every skill is named by a kind prefix, lowercase and then a hyphen. These are the kinds and where each lives:

| Repository | Kinds |
|---|---|
| psyche | `vision-`, `intent-`, and `spirit` |
| mind | `knowledge-`, `operation-` |
| field | `trial-`, `compensation-` |

Unprefixed skills (behavior, correction, vocabulary, nix-workflow, and others):

- His words say an unprefixed skill "means … it's psyche" (10-04), and that each "could be split up" into mind or field. They should all "be named appropriately".
- Dirty first: rename or place each one by what it is. Where unsure, put it in psyche under its current name and log the choice.
- `spirit` stays unprefixed, as the Spirit level.

### The Curriculum Nexus

The Nexus keeps a memory registry of every skill, recorded by the path where the skill lies in its repository.

The registry is filled and changed by registry-editing messages. A message carries:
- a vector of new entries;
- and/or a vector of edits, including removals;
- the paths.

His 10-05 rule: there is no datom inside a Nexus. The CLI turns datom into signal.

### The change signal

The change signal carries three vectors of skill names: changed, new, deleted.

On that signal, Curriculum regenerates the workspace from its own memory: it deletes the deleted skills, adds the new ones, and rewrites the edited ones. "That's it."

The workspace means `/home/li/primary`'s `.claude`, `.agents`, `.codex`, `.pi` and `.opencode` skill trees. Each harness gets its own blocks, and no harness gets an empty skill.

### Launch

A launched flow loads its skills, with each skill's `dependencies:` expanded transitively. For example, `spirit` brings in behavior, correction, vocabulary and compensation-book-distillation.

Already-running contexts are not injected. Only fresh launches count.

## His instructions, newest first

Paths are under `/home/li/primary/flows/` unless they say otherwise. "t:" marks a Claude transcript, given as session and line. [S] marks an instruction that has been superseded.

### 2026-10-07

- d4ae97/vision/curriculum.md: "the repo curriculum should hold the curriculum nexus and no skill at all … only the Rust code, the CLI, and the Nexus."
- d4ae97/vision/curriculum.md: "three repos, namely psyche, mind, and field, each of which will have a skill directory … the curriculum nexus will have its memory registry populated with these registry editing messages, which can contain a vector of new entries and/or a vector of edits".
- d4ae97/vision/curriculum.md: "use the path of the skill where it is and then the curriculum will be used to regenerate all the skills in the workspace using its own memory".
- d4ae97/vision/curriculum.md: the signal carries changed, new and deleted names; Curriculum will "delete the skills that have been deleted, add the skills that have been added, and rewrite the skills that have been edited. That's it."
- d4ae97/vision/curriculum.md: "There's not going to be any skill in the rest [sic] repository."
- d4ae97/vision/curriculum.md: the new Astra gets "all the instructions I've ever given, with more recent instructions having more authority".
- d4ae97/vision/skills.md: "vision, intent, knowledge, operation, trial, compensation. Those are the six … just prefixes, lowercase and then a hyphen."
- d4ae97/vision/skills.md: "Every form of distillation is a skill writing."
- d4ae97/vision/skills.md: "all the compensation skills are the things that need to be reviewed so that they can be upgraded potentially into an operation skill, a knowledge skill, vision".
- d4ae97/vision/skills.md: "We have this sort of hierarchy of skills, which should also be documented in skills."
- d4ae97/vision/skills.md: a strong request to avoid a failure becomes "a machine-created skill that doesn't require me in the loop".
- f768df/vision/skills.md: "create a machine-authored skill and deploy it immediately so that we have some kind of compensation."
- e5a0bc/vision/flow.md: "a registry with paths to all of these context modules in the flow memory itself. That way we can start right now."

### 2026-10-06

- d4ae97/vision/ethos.md: "get Astra going … on implementing the three-repo skill-based curriculum deploy. I guess we would need the datom file expansion".
  - Dirty-first on 10-07 supersedes the prerequisite: go by path now.
- e5a0bc/vision/capability.md: skills and subagents are one broader concept ("capability"). Naming only.

### 2026-10-05

- 8475a9/vision/datom.md: "we wouldn't involve this curriculum repo. We would just directly invoke the particular repositories like mind, psyche, and field."
- 8475a9/vision/datom.md: "That repo could essentially just maintain a Datom file that indexes and specifies the entire repo."
  - [S] in part: the 10-07 path registry is the dirty first step.
- 8475a9/vision/datom.md: "There should be no datom in any Nexus."

### 2026-10-04

- bad807/vision/skills.md and t:28d847ee:2788: "restart on actually using the repos psyche, mind, and field for their respective skills for their respective types … Migrate all of the vision …"
  - The same passage says that what is "without a prefix (meaning we're implying maybe that it's psyche)" could be split into mind or field.

### 2026-10-03

- t:28d847ee:585: "curriculum doesn't hold the skills. They're in other repositories … Why … are the skills not living in three repositories right now".
- t:28d847ee:937: "We only store the stuff once, and we have different rules for who can edit what and what type."
- t:28d847ee:937: "The files that have been modified will be regenerated or added, if they're missing, into that workspace."
- t:28d847ee:937: "Depending on Codex, Claude, or all of the harnesses … it's going to emit the different blocks".
- 5578cc/vision/skills.md: "support generating skills from more than one source for any type".
  - Plugin-style. Keep the generator open to more sources; it is not required now.
- 5578cc/vision/skills.md: skills refer to layers, and a knowledge skill maps layers to models.
- 5578cc/vision/curriculum.md: keep the name Curriculum.
- edf227/vision/contextModules.md: "Every flow call, or the flow database, has a registry of where each context module is located … type, name, location".
  - Launch passes the (kind, names) lists per layer.

### 2026-10-02

- 91ea9f/vision/skills.md: "get rid of the gold skills concept and every skill is typed. Psyche skills will be vision or intent … Documentation becomes knowledge."
- 91ea9f/vision/skills.md: give yourself trial and compensation skills "without having to go through me … field can implement it and deploy it."
- 3ec648/vision/skills.md: "Vision has to become skills now … prefixed with 'vision'".
  - Done: Curriculum b778545.

### 2026-10-01

- fe945a/vision/skills.md: proposals include "adding a skill to dependencies, whether … from another skill or from a subagent definition".
  - Subagents are a type of skill.

### 2026-09-29

- c64ee3/vision/skills.md: "the new skill stack with the three different source repos … load them into the curriculum database … psyche has vision, intent, and even spirit".
- c64ee3/vision/skills.md: "dependencies are just simply in this registry … a vision can only depend on something above it".
  - Hierarchy, top to bottom: spirit, intent, vision, operation/knowledge, trial/compensation.
- t:183ae001:826: "The skills are not supposed to be in the curriculum anymore. The curriculum is just the executable source code. Now we need three skill repos."
- 183ae0/vision/skills.md: he complains that changing a skill requires a Rust recompile.
  - This is why skills load by path, not baked in.

### 2026-09-28

- 8904b1/vision/skills.md: "operation and documentation would be for Mind and tests and compensation would be for field … We would prefix all the skills".
- 8904b1/vision/skills.md: "eventually the skills will live in a daemon not in a Git repo anymore."
  - This is the direction, not the target now.

### 2026-09-24

- 26c50c/vision/curriculum.md: "The type is assigned to the repo. It's centrally controlled: which type comes from which repositories."
- 752e0f/vision/curriculum.md: Curriculum reads repositories with `config.datom`.
  - [S] in part, by 10-05 and 10-07.

### 2026-09-20

- b80e55/vision/curriculumAndTriadSkillGeneration.md: "The curriculum generator … just a binary, an executable with a nexus with CLIs … three repositories: psyche, mind, and field … Anybody regenerates when main moves."

### 2026-09-17

- 9993b5/vision/curriculumNexus.md: Curriculum is a Nexus that can be reset, and reseeded from Nix.
  - A reseed at start, from the three repositories, fits the dirty path registry.
- 9993b5/vision/workspaceProvisioning.md: "When Flow starts, it can ask for curriculum … Curriculum provides all of the skill files for that workspace."
- 108ab0/vision/operational-curriculumAsModuleSystem.md: "if curriculum is a nexus, we can't have any data there … a manifest that gives it a bunch of paths".
- t:108ab020:884: "Take the skills out of the runtime. The Rust code should be separate from the skills themselves."
- [S] 108ab0/vision/operational-curriculumSkillsRepo.md: a single "curriculum skills" repository. Superseded by the three repositories.
- [S] 108ab0 and b05237: the `operational-` and `test-` prefixes, and "unprefixed = gold". Superseded by the six kinds (10-02, 10-07).

### 2026-09-16

- [S] 48cff7/vision/skillKindsTaxonomy.md: kind suffixes (rationale, extended, experimental). Superseded by the prefixes.

### August 2026

- [S] vision-raw/skillsRepository.md (08-21): "get rid of the manifest and generate whatever skills are present".
  - Superseded by the 10-07 registry.
- vision-raw/skillsRepoSourceOnly.md (08-10): "I dont want to see any .claude or .agent in the skills repo".
  - Generated trees exist only in the workspace.

## Current state, witnessed 2026-10-07

### curriculum-deploy

- Repository `/git/github.com/LiGoldragon/curriculum-deploy`, at 4a3763e (0.9.0). Clean, and equal to origin/main.
- It is a one-shot Rust CLI, not a Nexus. It has no registry.
- It takes one inline datom argument: `Generate|Check|Visualize .{ «curriculum-root» [ Psyche.«dir» Mind.«dir» Field.«dir» ] «workspace» }`.
- It reads `roles.datom` and the `*.md` files in each source directory, and refuses duplicate names.
- It writes the `.claude`, `.agents`, `.codex`, `.pi` and `.opencode` trees, with role packets and cleanup lists.
- Its role record is `curriculum-deploy.ethos` at the repository root. It declares `SkillSource[Psyche|Mind|Field]`, `Configuration`, `Request`, `Output` and the Roles types.

### Curriculum

- Repository `/git/github.com/LiGoldragon/Curriculum`. It is pure data: `skills/` holds 105 `.md` files, plus `roles.datom`. There is no Rust.
- Pushed main is c98fc43, with b778545 (Vision and Intent turned into skills) beneath it.
- The working tree carries uncommitted f768df work; see "f768df in flight" below.
- The README's count of 38 skills is stale.

### The three skill repositories

- `/git/github.com/LiGoldragon/{psyche,mind,field}-skills` exist locally and on GitHub. They are public and were created 2026-09-29.
- Each holds only a README saying the layout is undecided. His words have now decided it.

### Primary

- `flake.nix` pins curriculum-deploy at 4a3763e. Primary was repinned to Curriculum c98fc43 at commit 9c678a068.
- The flake apps are `generate-skills` and `check-skills`.
- The flake check `generated-skills-current` passes all of `${curriculum}/skills` as a single `Psyche` source.
- The trees hold 99 skills. They match b778545 and c98fc43, before f768df's additions.
- Field 42265e has been asked to publish Primary.

### Launch

- 95 skills declare `dependencies:`. The generator copies that field through and never reads it.
- In `flow` (5e0b1bf), `crates/flow-nexus/src/composition.rs` takes an explicit `profile.skill_name_vector` and does not expand it.
- `tools/claude-main-flow-launch.mjs` hard-codes `BIRTH_SKILLS`, and so do the Codex and Pi launchers beside it.
- So no dependency is expanded anywhere.

### f768df in flight: carry it on

f768df's worker is a Codex native subagent of f768df, nicknamed Feynman. It holds Orchestrate lock 14301 (CompensationDeployment f768df).

The 47-entry batch from `flows/d4ae97/reports/recurring-insistences.md`:
- It is mapped into about 12 homes in `flows/f768df/reports/compensation-deployment.md`, which is untracked.
- It is now being written, uncommitted, in the Curriculum working tree:
  - six new skills: `compensation-{truth,orders,prose,understanding,launch,design}.md`;
  - edits to `compensation-default-effort`, `compensation-messenger-clj`, `nix-workflow`, `operation-flashbook`, `psyche-grasp`, `spirit`, `trial-presentation-book` and `trial-succession`.
- `compensation-primary-commit` is held for the living's ruling. Leave it as it is.

The Spirit-dependency fix has no code yet: nothing is committed, pushed or deployed.

f768df's own lane in Primary is also uncommitted: `flows/f768df/log.md`, `vision/*`, `books/flow-spawning.md` and `reports/`.

What to do with it:
1. Take over lock 14301 when Feynman stops, or once f768df is retired. Ask d4ae97 to retire f768df if it still runs.
2. Review the batch, commit it, and push it.
3. These skills then move with every other skill into field-skills.
4. Do the dependency expansion inside your rebuild, not as a separate patch.
5. Commit f768df's Primary lane under f768df's name before you start.

## Done means

1. psyche-skills, mind-skills and field-skills hold every skill, each in `skills/`, named by kind prefix and placed by kind. Curriculum holds no skill.
2. Curriculum holds the Rust CLI and the Curriculum Nexus. The Nexus runs as deployed. Its memory registry is populated by registry-editing messages, by path, with every skill.
3. A change signal (changed, new, deleted) regenerates `/home/li/primary`'s skill trees: deleting, adding and rewriting. You witness this on a real edit, a real addition and a real removal.
4. A freshly launched Claude flow and a freshly launched Codex flow each load their skills, including transitive dependencies. Witness it in the launched context, for example by a compensation skill reached only through `spirit`.
5. The flake check passes against the new sources. Everything is committed and pushed, Primary is repinned, and Field 42265e has published Primary.

Report "done" to Psyche Opus d4ae97, with the witnesses.

## Carried over at launch
f768df and its worker are retired when you start. Their uncommitted edits stay in the Curriculum checkout; take them over as yours. Orchestrate lock 14301, held by f768df's worker, is stale once f768df is gone: clear it as the stale-lock skill says. The 47-entry compensation batch is yours to finish and deploy alongside the rebuild.
