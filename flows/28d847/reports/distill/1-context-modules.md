# Distillation proposal: subject 1, context modules and the system prompt

Source: `flows/28d847/reports/fable-package-vision.md`, sections 1.1 to 1.4 (91 quoted records, 8,705 words of his text). Paths below are relative to `/home/li/primary/`. A quote is named by its package position (1.1.6 is section 1.1, entry 6), its date and its source record; "p2" names its second paragraph.

This is a proposal for the main flow of 28d847 to compose and bring to the living. Nothing here is approved, and nothing lands in `Vision/` before his explicit word. Each statement re-articulates; none quotes. Where records conflict, the statement carries both sides with their dates and the package's tension tag (T1 to T23); no tension is settled here. Tensions the package does not tag are marked "untagged".

Every statement names the Vision topic it would land in. Five topics are new: `skills`, `curriculum`, `contextModules`, `systemPrompt`, `harness`.

## Totals

| | Words |
|---|---|
| His words in subject 1 | 8,705 |
| Replaced by the 18 statements below | 7,223 |
| Words of the 18 statements (code blocks excluded) | 2,642 |
| Left verbatim (condense poorly, notions, impurity candidates, off subject) | 1,267 |
| Already distilled into Vision (no new statement) | 215 |

## Ranking

| Rank | Cluster | Lands in | Words replaced |
|---|---|---|---|
| 1 | Vision is skill | `Vision/skills.md` | 847 |
| 2 | Where a module enters: the top and middle context layers | `Vision/contextModules.md` | 792 |
| 3 | Skills live in the three aspect repositories, not in Curriculum | `Vision/skills.md` | 717 |
| 4 | One topic, several skill files with deterministic names | `Vision/skills.md` | 551 |
| 5 | Distillation rolls as the work goes, as small skill-edit proposals | `Vision/distillation.md` | 540 |
| 6 | The anatomy of the system prompt, classified line by line | `Vision/systemPrompt.md` | 534 |
| 7 | Context modules: the work is editing them | `Vision/contextModules.md` | 506 |
| 8 | Curriculum, the typed generator | `Vision/curriculum.md` | 447 |
| 9 | No compaction: restart on a fat first prompt | `Vision/flowNexus.md` | 393 |
| 10 | Flow's registry of modules and the launch list | `Vision/flowNexus.md` | 388 |
| 11 | The psyche's hierarchy: distilling upward, depending upward | `Vision/psyche.md` | 300 |
| 12 | A distillation proposal is tangible | `Vision/distillation.md` | 244 |
| 13 | Each aspect edits its own skills | `Vision/skills.md` | 239 |
| 14 | Vision, operation, compensation, usage | `Vision/skills.md` | 234 |
| 15 | Behavior modules are chosen at launch | `Vision/flowNexus.md` | 167 |
| 16 | A standard, Nix-defined harness home | `Vision/harness.md` | 165 |
| 17 | One source, emitted per harness by `{%` templates | `Vision/curriculum.md` | 116 |
| 18 | Setup variables | `Vision/curriculum.md` | 43 |

---

## 1. Vision is skill — 847 words

**Lands in:** `Vision/skills.md` (new topic).

**Proposed statement**

Vision is skill; there is no separation between them. A distilled vision file is a skill, so writing vision is writing a skill and vision distillation is skill editing. The vision data is written once, in the place Curriculum generates the skills from. The vision holds every detail an implementation needs; the skill is its concentration, the part one must know to understand the concept. The effort that went into writing skills belongs in reinforcing the distilled vision with actual code: the ethos, the Rust expected from it, and the invariant Rust that compiling an ethos or a Nexus executable yields, so that the flows touching a topic read it up front and in one place. Where a skill conflicts with the current distilled vision on the same topic, a path runs from the vision to a proposed update of the skill. This vision is what should carry the most important context a model is given.

**Replaces**

- 1.3.1, 2026-10-03, `flows/5ed94b/vision/visionBooks.md` (also `flows/28d847/vision/books.md`), 35
- 1.3.5, 2026-10-02, `flows/3ec648/vision/skills.md`, 33
- 1.3.8, 2026-10-01, `flows/fe945a/vision/questions.md`, 60
- 1.3.11, 2026-09-29 (file date), `flows/183ae0/vision/skills.md`, 63
- 1.3.18, 2026-09-20 (file date), `flows/b81560/vision/operational-visionIsSkillThreeRepos.md`, 114
- 1.3.20 p1, 2026-09-18 (file date), `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md`, 46
- 1.3.22 p1, 2026-09-17 (file date), `flows/108ab0/vision/operational-skillIsVisionUnified.md`, 54
- 1.3.25 p1, 2026-09-16, `flows/48cff7/vision/skillSourceKinds.md`, 73
- 1.3.26 p1, 2026-09-16, `flows/48cff7/vision/skillPromotionAndLayering.md`, 80
- 1.3.32, 2026-08-30 (file date), `flows/62022e8f/vision/distilledVision.md`, 231
- 1.2.1 p2, 2026-10-03, `flows/5ed94b/vision/skills.md` (also `flows/28d847/vision/skills.md`), 58

**Left out or in conflict**

- Untagged tension. 2026-08-30 (1.3.32) and 2026-09-14 (1.1.24, cluster 2): a skill differs from the vision; it teaches how to think about and use concepts, while the vision says what the end result ought to be. 2026-09-16 onward (1.3.25, 1.3.22, 1.3.11, 1.3.8, 1.3.1): they are one and the same. The statement keeps the difference as detail against concentration, the later records' unity as the rule, and settles neither.
- 1.3.25 p1: our composed skills are treated as vision for now, though some are fact and could be mind; the harness's stock skills are not. Left out of the rule; it feeds cluster 14.
- 1.3.8: a question is a layer of mind, as spirit, vision and notion are of psyche. Off this subject; stays for a distillation on questions.
- Impurity candidates (working instructions): 1.3.8's order to orchestrate the whole migration; 1.3.18's order to find a young psyche flow to gather the situation; 1.3.5's order for a document.
- T1 touches the "place Curriculum generates from" (cluster 3).

**Sources lines:** `5ed94b visionBooks`, `28d847 books`, `3ec648 skills`, `fe945a questions`, `183ae0 skills`, `b81560 operational-visionIsSkillThreeRepos`, `b05237 operational-threeDataReposAndPrimaryNext`, `108ab0 operational-skillIsVisionUnified`, `48cff7 skillSourceKinds`, `48cff7 skillPromotionAndLayering`, `62022e8f distilledVision`, `5ed94b skills`, `28d847 skills`.

---

## 2. Where a module enters: the top and middle context layers — 792 words

**Lands in:** `Vision/contextModules.md` (new topic). Terms: the top context layer is the harness's system prompt; the middle context layer is the user prompt, where skills also sit; a context module is defined in cluster 7.

**Proposed statement**

A model's context has context layers of differing authority, and this is among the most important things in programming with models. The system prompt, the top context layer, carries the highest authority; skills carry the same authority as the user prompt. The living's raw words go in the middle context layer until they are distilled, and the distillation goes in the top context layer, together with specialized expert guidance and a corrected version of the guidance the harness ships with. Steady, well-distilled spirit, intent and vision in the system prompt free room in the prompt, which is maxing out, and replace whatever conflicts with them there, even words of ours, for better behavior; intent distilled further goes the same way, and what is already being put directly in the system prompt keeps going there. The primary's system prompt holds the vision for most of its topics, if that can be done. What must hold against the harness's own guidance, as main-flow mode must, only the system prompt can hold; reloading a skill by hook every so many messages was raised as a fallback. Intent and vision, where they are skills, are highly positioned skills. Against the top-layer placement stand the middle-layer records: the middle context layer is the best, and a flow started with a perfect middle context layer gives perfect results; a context subflow gathers the vision and skill a piece of implementation needs, and that brief enters the implementing subflow's prompt; distilled vision is loaded into the middle stratum, and perhaps it is the skill that moves to the top; his whole psyche is injected into a new flow at the user level, so the flow has it from there and not from the bottom layer. Which kinds of module qualify for the system prompt, and what modifying it changes over modifying the user prompt, he has said he does not yet know.

**Replaces**

- 1.1.13, 2026-09-25, `flows/e51411/vision/systemPrompt.md`, 48
- 1.1.17 p1 and p3, 2026-09-24, `flows/d8df70/vision/mainFlowMode.md`, 99
- 1.1.18, 2026-09-24, `flows/752e0f/vision/psycheInjection.md`, 39
- 1.1.19, 2026-09-24, `flows/752e0f/vision/psycheInSkills.md`, 68
- 1.1.21, 2026-09-17 (file date), `flows/b49251/vision/systemPrompt.md`, 87
- 1.1.24, 2026-09-14, `flows/6cc91b/vision/skills.md`, 73
- 1.1.25, 2026-09-14, `flows/6cc91b/vision/mainFlow.md`, 82
- 1.1.27, 2026-09-13, `flows/024bc7/vision/context.md` (also `flows/bcd02a/vision/context.md`), 162
- 1.1.29, 2026-08-22 (file date), `vision-raw/trainingRepo.md`, 23
- 1.1.30, 2026-08-13, `flows/6863ef19/vision/gradientsOfAuthority.md`, 111

**Left out or in conflict**

- T3, both sides kept in the statement. Top: 2026-09-13, 09-15, 09-17, 09-24, 09-25. Middle: 2026-09-14 (twice), 09-24 (1.1.18). Open: 2026-10-03 (1.1.3, cluster 7), he does not know the difference. The package also points at `Intent/startupPrompt.md` (startup skills enter through the startup prompt, invisible to subflows), distilled, not his word.
- 1.1.27's list of grades for the stock guidance (good, bad, neither, confusing, unnecessary) goes to cluster 6.
- 1.1.30's request to be corrected if skills are not the only other thing at user-prompt authority: a question, left out.
- 1.1.19's questions (change how we write, update all skills, merge them) are the brief for a successor, not a ruling; left out. Its order to start a new flow and do the edit is an impurity candidate.
- 1.1.17 p2 (75 words, exhortation to refresh and get on main-flow mode) stays verbatim as an impurity candidate.
- 1.1.29 says the training (the skills repo) will soon be injected into the harness system prompt; carried as the top-layer side.

**Sources lines:** `e51411 systemPrompt`, `d8df70 mainFlowMode`, `752e0f psycheInjection`, `752e0f psycheInSkills`, `b49251 systemPrompt`, `6cc91b skills`, `6cc91b mainFlow`, `024bc7 context`, `bcd02a context`, `vision-raw trainingRepo`, `6863ef19 gradientsOfAuthority`.

---

## 3. Skills live in the three aspect repositories, not in Curriculum — 717 words

**Lands in:** `Vision/skills.md`. It would replace the target-shape line in `Vision/psyche.md` that the skills belong in a repository (that line was distilled from the same 8393ca record as 1.3.19). Terms: the three aspects are psyche, mind and field.

**Proposed statement**

Curriculum does not hold the skills; it is only the executable source that regenerates them, and its code is kept apart from the skill data so that a change to a skill does not rebuild it. The skill data lives in three repositories, one per aspect: psyche, mind and field, each named for its aspect. A repository has one type, assigned to it and controlled centrally: which type comes from which repository. The psyche repository holds vision, intent, spirit and notion and nothing else; mind's and field's hold theirs, and each may separate its own levels by directory, operation and documentation among them. Beside each skill repository stands a logs repository, psyche logs, mind logs and field logs, holding the raw records under their flow ids, so the distilled part stays apart from the raw; the logs repositories are symlinked into the workspace, and a small Clojure executable searches the raw vision across all three. The skills are loaded into Curriculum's database typed by their aspect, with each aspect's sub-variants (psyche's are vision, intent and spirit), and the generator prefixes each skill from its payload. The three repositories exist so the agents of an aspect can edit the skills that pertain to them easily. The primary workspace is a bare template that expects these repositories mounted in it.

**Replaces**

- 1.3.3, 2026-10-03 (file date), `flows/28d847/vision/skills.md`, 29
- 1.3.4, 2026-10-03 (file date), `flows/28d847/vision/skills.md`, 47
- 1.3.12, 2026-09-29 (file date), `flows/183ae0/vision/skills.md`, 47
- 1.3.13, 2026-09-29 (file date), `flows/183ae0/vision/skills.md`, 98
- 1.3.14, 2026-09-29, `flows/c64ee3/vision/skills.md`, 124
- 1.3.15 p2, 2026-09-28, `flows/8904b1/vision/skills.md`, 39
- 1.3.20 p3, first two sentences, 2026-09-18 (file date), `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md`, about 35
- 1.3.23, 2026-09-17 (file date), `flows/108ab0/vision/operational-skillLagsVisionObservability.md`, 73
- 1.2.8 p1 and p2, 2026-09-24, `flows/26c50c/vision/curriculum.md`, 121
- 1.2.9 p2, 2026-09-20 (file date), `flows/b80e55/vision/curriculumAndTriadSkillGeneration.md`, 55
- 1.2.12, 2026-08-25, `flows/01a035d3/vision/archive-rustCodeFromTheData.md`, 49

**Left out or in conflict**

- T1. Later (2026-10-03, 2026-09-29): skills out of Curriculum, into three repositories, or scrap deploying skills for now (2026-09-29). Earlier (2026-09-17, 1.3.23): Curriculum skills are good for now; feeding vision files to Curriculum at runtime as a source was asked and then set aside, since the vision cannot be written directly in the skill. State: Primary still regenerates from the Curriculum skills, and which skills go to which aspect waits on him. Both kept; the statement carries the later rule only because the earlier is explicitly "for now"; the main flow should bring this to him as T1 and not as settled.
- Untagged tension. 1.3.15 p2 (2026-09-28): perhaps one repository, Psyche Skills, with mind and field skills separated by directory. Against it, the three-repository records before and after. The statement keeps directories only within each repository.
- 1.2.8 p2: it is all spirit, all psyche and mind, the same. Unclear; left out.
- 1.2.9 p2: anybody regenerates when main moves; the primary space is shared, so every flow's skills change when one adds and redeploys. Carried only as a pointer to cluster 8; it is a deployment rule.
- 1.2.8 p3 (56 words: a raw database for now, to migrate to mind, or perhaps wasted effort) and 1.2.9 p3 (59 words: Primary Next, the old flow log divided into three sectors) stay verbatim.
- 1.3.20 p3's remainder (about 188 words: persona setup levels, Primary Next, history rewrite, data accumulation) stays verbatim; off subject 1, and `Vision/psyche.md` already carries Primary Next.

**Sources lines:** `28d847 skills`, `183ae0 skills`, `c64ee3 skills`, `8904b1 skills`, `b05237 operational-threeDataReposAndPrimaryNext`, `108ab0 operational-skillLagsVisionObservability`, `26c50c curriculum`, `b80e55 curriculumAndTriadSkillGeneration`, `01a035d3 rustCodeFromTheData`.

---

## 4. One topic, several skill files with deterministic names — 551 words

**Lands in:** `Vision/skills.md`.

**Proposed statement**

A topic does not have a skill and a vision side by side; it has one family of skill files. Its core, named by the topic alone, is the vision an agent loads first; an extended file carries the rationale and the general aspect of the topic; a subtopic file, named by its subtopic, gives an extensive view of one aspect. A vision too big for one file breaks into subsections that become their own skill files, so an agent loads only the layer it needs. The generator gives each kind a deterministic name: rationale, subject rationale, subject extended, subject experimental, subject undecided proposal, notion, vision. Every skill touching a piece of work sits under its proper prefix, and a distillation is split across the skills it concerns, not put in one.

```
datom              ; the core: the vision of datom, loaded first
datom-extended     ; rationale and the general aspect
datom-<subtopic>   ; one aspect, in full
```

**Replaces**

- 1.3.6, 2026-10-02, `flows/3ec648/vision/skills.md`, 47
- 1.3.7, 2026-10-02, `flows/91ea9f/vision/distillation.md`, 29
- 1.3.20 p2, 2026-09-18 (file date), `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md`, 144
- 1.3.22 p2, 2026-09-17 (file date), `flows/108ab0/vision/operational-skillIsVisionUnified.md`, 55
- 1.3.26 p2, 2026-09-16, `flows/48cff7/vision/skillPromotionAndLayering.md`, 150
- 1.3.27, 2026-09-16, `flows/48cff7/vision/skillKindsTaxonomy.md`, 126

**Left out or in conflict**

- 1.3.20 p2 names the levels psyche, psyche extended, psyche vision; 1.3.22 p2 names them Datom core (or just Datom), Datom extended, Datom subtopic; 1.3.27's list has rationale and extended as separate kinds. The statement keeps all names given; how rationale and extended differ is not said in any record.
- 1.3.20 p2: perhaps skill generation moves out of Curriculum into Harness, which takes vision data and creates the skills; Curriculum does it for now. Untagged tension with cluster 8; left out here, carried there.
- 1.3.26 p2's placement content (spirit and intent in the system prompt; all vision loadable as skills at the third layer, even in Codex with `$`; per-call optional skills for specialized behavior, never for knowledge) goes to clusters 2 and 15.
- 1.3.27's definitions of vision, intent and spirit go to cluster 11.
- 1.3.6's order to make ethos, the nexuses and Flow a case study is an impurity candidate.

**Sources lines:** `3ec648 skills`, `91ea9f distillation`, `b05237 operational-threeDataReposAndPrimaryNext`, `108ab0 operational-skillIsVisionUnified`, `48cff7 skillPromotionAndLayering`, `48cff7 skillKindsTaxonomy`.

---

## 5. Distillation rolls as the work goes, as small skill-edit proposals — 540 words

**Lands in:** `Vision/distillation.md`.

**Proposed statement**

Distillation rolls as the work goes. Whenever a topic involves gathering vision, the raw vision it touches is distilled then, with subagents sent to gather everything that remotely touches the subject; at every second or third turn an agent proposes distilling what has accumulated. Raw vision is not let pile up, go stale and contradict itself as the living changes his mind: his first expression is rough, and several passes make it clean. The output reaches him as a constant flow of concise proposals, small enough to answer yes quickly: a new skill; an edit or addition to a skill; a skill added to or removed from the dependencies of another skill or of a subagent definition. Each aspect a matter concerns makes its own proposal. A subagent definition is a type of skill: the skill a fresh flow is launched with. Most proposals edit a skill that already exists.

**Replaces**

- 1.2.1 p1, 2026-10-03, `flows/5ed94b/vision/skills.md` (also `flows/28d847/vision/skills.md`), 43
- 1.3.9, 2026-10-01, `flows/bd0019/vision/skillProposals.md` (also `flows/fe945a/vision/skills.md`), 139
- 1.3.10, 2026-10-01 (file date), `flows/04db2fd2/vision/rollingDistillation.md`, 236
- 1.3.29, 2026-09-12, `flows/9e7c9f/vision/distillAnythingThatIsUsed.md`, 93
- 1.3.30, 2026-09-03, `flows/e4a40e/vision/distillation.md`, 29

**Left out or in conflict**

- T20. 2026-09-03 (1.3.30): change the skill to say just keep logging, since no distillation had landed. 2026-09-12, 2026-10-01, 2026-10-03: distill as we go, as a constant flow of proposals. Both stand as records; the package marks the earlier as superseded by later words, and the main flow brings that reading to him, not this proposal.
- 1.3.9's wish that all the talk about training agents become proposals is carried by the proposal list itself.
- 1.2.1 p1's wish to modify the system prompt and use the new flow, and 1.2.1 p4 (13 words, pass all that to Fable), are impurity candidates; p4 stays verbatim.

**Sources lines:** `5ed94b skills`, `28d847 skills`, `bd0019 skillProposals`, `fe945a skills`, `04db2fd2 rollingDistillation`, `9e7c9f distillAnythingThatIsUsed`, `e4a40e distillation`.

---

## 6. The anatomy of the system prompt, classified line by line — 534 words

**Lands in:** `Vision/systemPrompt.md` (new topic).

**Proposed statement**

The system prompt is not one thing. It has many parts with many subparts, and its anatomy is drawn up in ethos by studying system prompts of every kind, the latest Claude's and Codex's among them, with the parts that change per model. Every line is classified: what it is; whether it is behavior, personality or operational safety; which kind of training or guidance it belongs to; and whether it is good, bad, neither, some of each, confusing or unnecessary. The result is data files, Markdown with Datom and Ethos syntax: the data specified, then shown. The stock prompts are suspected to be full of instructions partly or wholly against the living's philosophy of using models, which incentivize the behavior he keeps steering against; they are replaced by a corrected version, and a draft of the open-source stack, wholly self-authored, says what changes from the default harnesses' prompts. That draft is honest about how he works and asks him how he sees work, law and behavior, which today live in seed form in the skills and the vision. A rule specific to one model or harness, like stopping on a classifier refusal, is not spirit, which is universal; it goes in that model's or harness's own core part of the system prompt. The research into harnesses that did replace the system prompt is completed.

**Replaces**

- 1.1.10 p3, 2026-10-03, `flows/5578cc/vision/flow.md` (also `flows/9fb0ad/vision/systemPrompt.md`, `flows/dea0ba/vision/systemPrompt.md`), 93
- 1.1.14, 2026-09-25, `flows/e51411/vision/systemPrompt.md`, 103
- 1.1.15, 2026-09-25, `flows/e51411/vision/launch.md`, 86
- 1.1.28, 2026-08-23, `flows/2f6b1dc5/vision/systemPrompt.md`, 58
- 1.4.3, 2026-10-01, `flows/fe945a/vision/hooks.md`, 54
- 1.4.5, 2026-09-17 (file date), `flows/da1e3f/vision/operational-harnessSpecificRules.md`, 43
- 1.4.6, 2026-09-14, `flows/6cc91b/vision/openSourceStack.md`, 97

**Left out or in conflict**

- T4. 2026-08-23 (and 2026-08-17, 2026-10-03): replace the harness's system prompt. 2026-09-18 (1.4.4): keep the harnesses as stock as possible, the ordinary executable names and the desktop apps. The package reads the second as the program, not its prompt; the record does not say. Both kept.
- T13. 1.1.14 asks for Datom and Ethos syntax everywhere in these files; later records (2026-09-24, 2026-09-27) want Datom only where a program needs it. Both kept; the statement carries his 1.1.14 words for this one set of files.
- 1.1.15: the anatomy and ontology of all components, and the vocabulary, as the new Fable's first task, with the hacky tool changed to put spirit and vision in the system prompt; the merge of vision and skills (cluster 1) and the prompt maxing out (cluster 2). The task assignment is an impurity candidate.
- 1.1.14's assignment of the check to Mind Sol on a fresh flow is an impurity candidate.
- 1.4.3's hook documentation and update book feed cluster 16.

**Sources lines:** `5578cc flow`, `9fb0ad systemPrompt`, `dea0ba systemPrompt`, `e51411 systemPrompt`, `e51411 launch`, `2f6b1dc5 systemPrompt`, `fe945a hooks`, `da1e3f operational-harnessSpecificRules`, `6cc91b openSourceStack`.

---

## 7. Context modules: the work is editing them — 506 words

**Lands in:** `Vision/contextModules.md` (new topic).

**Proposed statement**

A context module is one of the things a thinking machine starts its thinking with: vision, intent, spirit, knowledge, operation, and role; together they are the aspects of its awareness, and the family still needs a better name than aspect, which is taken. The work is now editing context modules: creating, editing, removing, splitting and merging them. Every redirection, every book and every exchange with the living comes down mostly to that, and agents are told so at the level of the system prompt. Skills are a prompt system: the same module can go into the system prompt, into the prompt, or stay available for an agent to load. One standard for context modules populates both the skills and the system prompt; Flow uses it, and Curriculum implements it. The component keeps the name Curriculum, because context is too common a word. The concentration is on high-quality modules for the system prompt, and on launching flows educated from them.

**Replaces**

- 1.1.1, 2026-10-04 (file date), `flows/28d847/vision/curriculum.md`, 53
- 1.1.2, 2026-10-03, `flows/5ed94b/vision/contextModules.md`, 114
- 1.1.3, 2026-10-03, `flows/5ed94b/vision/contextModules.md`, 72
- 1.1.4, 2026-10-03, `flows/5578cc/vision/curriculum.md`, 107
- 1.1.5, 2026-10-03, `flows/edf227/vision/contextModules.md`, 64
- 1.1.10 p1, 2026-10-03, `flows/5578cc/vision/flow.md`, 52
- 1.2.16, 2026-08-17, `flows/358f143a/vision/skillsRepository.md`, 44

**Left out or in conflict**

- T2. 2026-08-17: Curriculum is the wrong name, training is right, yet keep the name and put the rewrite in a new repository called training. 2026-10-03 (edf227): maybe the component is just called context, no big deal; later the same day (5578cc): keep Curriculum, context is used a lot. The family word is open. All kept; the statement carries the latest naming word.
- T23. Role as a module type comes from 1.1.8 (cluster 10); the 2026-10-03 list (vision, intent, spirit, knowledge, operation) differs from the 2026-09-24 list (vision, operation, compensation; cluster 14). Both kept.
- T3. 1.1.3's second half (which modules qualify for the system prompt; what difference it makes) is carried in cluster 2.
- 1.1.4's order for Fable (research, then an extensive illustrated design of the whole stack) and 1.1.1's order to launch the Fable flow are impurity candidates. T10 (how much to show) touches 1.1.4.
- 1.2.16's direction to keep things manual while he rewrites with another flow is a past working instruction.

**Sources lines:** `28d847 curriculum`, `5ed94b contextModules`, `5578cc curriculum`, `edf227 contextModules`, `5578cc flow`, `358f143a skillsRepository`.

---

## 8. Curriculum, the typed generator — 447 words

**Lands in:** `Vision/curriculum.md` (new topic).

**Proposed statement**

Curriculum is a binary: a nexus with CLIs that regenerates the skills. It takes the repositories it is given and recognizes their special files, the Nix entry point among them and a Datom configuration such as `config.datom`, for which Curriculum defines its own ethos object. The skills are typed, never copied by directory name: the nexus has a fully typed specification of every input it takes, a schema perhaps in a datom file fed in through the CLI and turned into a signal to the generator. Every source signal can be its own repository, taken as a dependency, and a nexus library handles the rebuild: regenerating the ethos and rebuilding the CLI when a dependency or a source signal's ethos changes. Any type of skill can be generated from more than one source, so people write their own knowledge skills and take others' knowledge or vision skills like plugins, with vision they share and vision they keep for themselves, and the same for every other type. Curriculum generates whatever skills are present.

```
; illustrative only: the shape of Curriculum's own configuration, not a ruling on its fields
config.datom
```

**Replaces**

- 1.2.2, 2026-10-03, `flows/5578cc/vision/skills.md`, 93
- 1.2.6, 2026-09-29 (file date), `flows/183ae0/vision/skills.md`, 39
- 1.2.7, 2026-09-24, `flows/752e0f/vision/curriculum.md`, 159
- 1.2.9 p1, 2026-09-20 (file date), `flows/b80e55/vision/curriculumAndTriadSkillGeneration.md`, 50
- 1.2.15, 2026-08-21, `vision-raw/skillsRepository.md`, 55
- 1.3.15 p1, 2026-09-28, `flows/8904b1/vision/skills.md`, 51

**Left out or in conflict**

- Untagged tension on scope. 2026-09-20 (file date, 1.2.9): the generator should not change; it is just a binary. 2026-09-24 (1.2.7): revamp everything. 2026-09-16 (1.3.27): Curriculum gets more substantial, becomes a nexus. 2026-09-18 (file date, 1.3.20): perhaps the generation logic is rewritten into Harness, Curriculum doing it for now. All kept as records; the statement carries what they share (a binary, a nexus with CLIs).
- Untagged tension on the manifest. 2026-08-21 (1.2.15): get rid of the manifest, generate whatever is present; the earlier breaking into modules was the wrong approach. 2026-09-29 (1.2.5, cluster 11): a registry of everything, with dependencies. 2026-10-03 (1.1.6, cluster 10): Flow keeps a registry of modules. The package notes the comparison. Both kept.
- 1.2.7: the phrase about the Nexus not speaking Datom is unresolved in the record (it may mean the opposite, or the Nix entry point); left out. Its order to pass this to new Mind flows is an impurity candidate.
- The datom block above is a placeholder: no record gives the fields of `config.datom`, so no example code can be shown without adding to his words. The statement owes code once the type exists.
- 1.2.2's opening (skill variables move into knowledge skills) goes to cluster 18.
- 1.3.15 p1's question (what the skill-generation nexus is called; is it Curriculum) is left out; cluster 7 carries the name.

**Sources lines:** `5578cc skills`, `183ae0 skills`, `752e0f curriculum`, `b80e55 curriculumAndTriadSkillGeneration`, `vision-raw skillsRepository`, `8904b1 skills`.

---

## 9. No compaction: restart on a fat first prompt — 393 words

**Lands in:** `Vision/flowNexus.md`.

**Proposed statement**

A flow does not compact. When it grows too big, it restarts itself on a fresh flow with a really good first prompt, always a fat prompt, and never holds back from restarting. It carries its useful state forward in that prompt or in a custom system prompt holding the high-level intent, spirit, operational flow and operational rules. A flow changes over at 60 percent of its context at the most, and sooner when the conversation shifts hard, repopulating a fresh flow with context fitted to the new emphasis. A main designer flow's first prompt is big, with the vision for most of its topics. The old flow winds down and is marked, by its thread name or a status such as ancestor or concluded; a concluded flow can be woken to ask it something, but once its cache has lapsed that is expensive and better avoided.

**Replaces**

- 1.1.20, 2026-09-19 (file date), `flows/b05237/vision/operational-fatPromptAndCustomSystemPrompt.md`, 98
- 1.1.22, 2026-09-17 (file date), `flows/f55ec8/vision/flowRefresh.md`, 70
- 1.1.23, 2026-09-15 (file date), `flows/fd0f97/vision/firstPrompt.md`, 59
- 1.1.26, 2026-09-14, `flows/6cc91b/vision/flowLifecycle.md`, 166

**Left out or in conflict**

- 1.1.26's figures for a fresh flow (around 200,000 tokens; 20 to 30 percent for Claude; unknown for Astra) are unclear in the record; left out.
- 1.1.22 asks the flow both to put its state in its system prompt and to take all of that out of its system prompt; the record does not say what "that" is. Left out.
- 1.1.20's orders (pass all wisdom to the other Fable; start a new Fable; the three topics to refresh on) are impurity candidates. 1.1.22's cost and machine-load complaint is the reason for an order, not a rule.
- T3 touches the system-prompt half (cluster 2).

**Sources lines:** `b05237 operational-fatPromptAndCustomSystemPrompt`, `f55ec8 flowRefresh`, `fd0f97 firstPrompt`, `6cc91b flowLifecycle`.

---

## 10. Flow's registry of modules and the launch list — 388 words

**Lands in:** `Vision/flowNexus.md`. Terms: the origin startup prompt is the first prompt a flow is started with.

**Proposed statement**

Context modules stay Markdown files; they reach the model as a string anyway. Flow keeps in its database a registry of where every module is: its name and its location, for now a local file path, later perhaps a Git repository. That configuration is kept apart from launches, served through the meta wire, and updated whenever a skill is added. A launch names, for each place it loads into (the system prompt at each layer, and the origin startup prompt), the modules wanted, as a vector of module types in which each variant carries the names of its modules, so nothing repeats; Flow inserts each module in its place. Role is a module type. The field naming a module's type is not called kind, which ethos already uses for something more basic. This is the prototype, the minimum viable product.

```
; illustrative shape only, from his description; type and field names are placeholders
SystemPrompt.[ Spirit.[ spirit ] Vision.[ flow psyche behavior ] Role.[ main-flow ] ]
StartupPrompt.[ Vision.[ datom ] ]
; kept separately in Flow's registry: name to location
[ { flow «skills/flow.md» } { psyche «skills/psyche.md» } ]
```

**Replaces**

- 1.1.6, 2026-10-03, `flows/edf227/vision/contextModules.md` (also `flows/dea0ba/vision/systemPrompt.md`), 271
- 1.1.7, 2026-10-03, `flows/dea0ba/vision/contextModules.md` (also `flows/edf227/vision/contextModules.md`), 85
- 1.1.8, 2026-10-03, `flows/5578cc/vision/ethos.md` (also `flows/edf227/vision/contextModules.md`), 25
- 1.1.9, 2026-10-03, `flows/edf227/vision/contextModules.md`, 7

**Left out or in conflict**

- T23: the module types and the word kind. Untagged tension with cluster 8 (no manifest, 2026-08-21) against this registry (2026-10-03).
- 1.1.6 first describes each launch entry as carrying type, name and location, then 1.1.7 moves names to the variant and paths to a separate configuration. The statement carries the later shape only because 1.1.7 corrects 1.1.6 in the same exchange; the main flow should confirm that reading.
- 1.1.6's order after it (a book, then Mind designs and writes the code) and 1.1.7's wish to see the anatomy of everything are working instructions.
- The datom example adds placeholder names; no record gives the variant names or the registry's shape beyond name and location. It is marked as illustrative and is for him to correct.

**Sources lines:** `edf227 contextModules`, `dea0ba systemPrompt`, `dea0ba contextModules`, `5578cc ethos`.

---

## 11. The psyche's hierarchy: distilling upward, depending upward — 300 words

**Lands in:** `Vision/psyche.md` (the hierarchy) and `Vision/curriculum.md` (the struct and the registry); see the merge section.

**Proposed statement**

Distillation is the psyche's output; the psyche is always distilling vision or intent. Things move up by repeated distillation: vision is distilled often, intent is distilled out of vision, and spirit out of intent. Vision is what is seen clearly enough to try now; intent is where the project is going; spirit is how everything is approached, how the work is done and how one behaves. Notion sits below vision: distilled notion, less committal, keeps clear what might be wanted but is not yet decided, and it is owed too. The same hierarchy governs dependency, kept in a registry of everything: a module depends only on what is above it or on its own kind; a vision on another vision, an intent or the spirit; an operation on a vision or higher; and so on down through documentation and operation to trial at the bottom. Each variant is an ethos struct holding the skill's text as one field beside its metadata: title, description, whether it is visible to the user or the agent, its dependencies.

```rust
// illustrative: the fields he names, not a ruling on their types
pub struct Skill { pub title: Title, pub description: Description, pub visibility: Visibility, pub dependencies: Vec<SkillName>, pub text: Text }
```

**Replaces**

- 1.3.24, 2026-09-17 (file date), `flows/108ab0/vision/operational-distillationHierarchy.md`, 116
- 1.3.28, 2026-09-16, `flows/48cff7/vision/psycheIsDistillation.md`, 31
- 1.2.5, 2026-09-29, `flows/c64ee3/vision/skills.md`, 153

**Left out or in conflict**

- 1.2.5 says he forgot one level of the field's hierarchy; the statement does not fill it.
- 1.3.28's "division distillation" is left as the recorder left it (the distillation, or dividing records before distilling); the statement carries only the clause the record names directly.
- The definitions of vision, intent and spirit come from 1.3.27 (counted in cluster 4).
- `Vision/psyche.md` already says Psyche holds Spirit, Intent, Vision and Notion in descending authority; this statement extends it and does not restate that line.
- The Rust block is illustrative; the record names the fields, not their types.

**Sources lines:** `108ab0 operational-distillationHierarchy`, `48cff7 psycheIsDistillation`, `c64ee3 skills`.

---

## 12. A distillation proposal is tangible — 244 words

**Lands in:** `Vision/distillation.md`.

**Proposed statement**

A distillation proposal is tangible. It says which module, which edit, what is removed and what replaces what, and where each piece goes. It distills with the distillate: it reads the distilled vision it would land in, not the raw records alone. One subject gets one unified statement. Nothing in it is vague, padded, or supposed; what is not known is found out, not guessed and passed off. A report that only lines up what he said, one record after another, and never makes a point is not a proposal. Every flow distills the same way, by the skill.

**Replaces**

- 1.1.12 p1 and p4, 2026-10-03, `flows/5ed94b/vision/visionBooks.md`, 115
- 1.3.31, 2026-09-03, `flows/e4a40e/vision/distillation.md`, 108
- 1.3.36, 2026-08-19, `flows/7c3f0c1d/vision/psycheLogStructure.md`, 21

**Left out or in conflict**

- 1.1.12 p2 and p3 (110 words: subflows cannot receive none of the main system prompt, or they could not use the tools; saying so was bluffing) stay verbatim under T5. The measurement in the 5ed94b handover (a Codex collaborator carries the parent's base instructions but not its developer instructions; a Claude subagent carries its own definition plus two fixed paragraphs) bears on it; both stand.
- 1.3.37 (44 words, 2026-08-19, same record: the draft mixed the particular with universals; calling distillation one statement replacing a set of records is a falsehood) stays verbatim. It condenses poorly, and it sits in tension with 1.3.36 of the same day (one unified statement for one subject); untagged.

**Sources lines:** `5ed94b visionBooks`, `e4a40e distillation`, `7c3f0c1d psycheLogStructure`.

---

## 13. Each aspect edits its own skills — 239 words

**Lands in:** `Vision/skills.md`.

**Proposed statement**

Each aspect is in charge of its own skills, and the instructions on changing skills say where an agent's reach stops. When an agent sees a need to change a skill of another aspect, it messages that aspect, which weighs the suggestion on its merits; a suggestion bound for psyche is brought by Psyche to the living. The golden skills, the most trusted, live in their own repository, and changing them takes more approval. Operational skills are the ones agents write for themselves to help with their tasks without disturbing the psyche much: they live in their own repository under the operational prefix, are less reviewed by a human and less trusted, are good guidelines and good to know, and are more likely to be taken out than vision, since that knowledge need not be carried forever.

**Replaces**

- 1.3.15 p4, 2026-09-28, `flows/8904b1/vision/skills.md`, 87
- 1.3.16, 2026-09-28, `flows/8904b1/vision/skills.md`, 30
- 1.3.21, 2026-09-17 (file date), `flows/108ab0/vision/operational-operationalSkillsRepo.md`, 122

**Left out or in conflict**

- 1.3.21 calls operational skills operational Datom; left out as unclear.
- `Vision/psyche.md` already says operational vision skills carry the `operational-` prefix and iterate faster with an overview to the living; this statement agrees and adds trust and removal.
- T23: whether operational skills are Mind's (2026-09-24, cluster 14) or a separate agent-written set (2026-09-17) is not said.

**Sources lines:** `8904b1 skills`, `108ab0 operational-operationalSkillsRepo`.

---

## 14. Vision, operation, compensation, usage — 234 words

**Lands in:** `Vision/skills.md`.

**Proposed statement**

Skills are typed by the layer they come from. Vision describes what is wanted. Operation, Mind's, is what is being worked with. Compensation, Field's, is what is welded in place for now to make the system run, like a hotfix, owed a proper implementation designed in the psyche. Testing, putting something in live to see if it works, is a notion; it becomes compensation once it holds. These are the main layers, with probably some above and below; they are not always a total hierarchy, and the field holds domains of its own. Some knowledge, mind, is hooked into skills beside the vision. Usage skills say how to use something, a tool, with the language to speak to it. Each type comes from its own place.

**Replaces**

- 1.3.17, 2026-09-24, `flows/752e0f/vision/layers.md`, 147
- 1.3.25 p2, 2026-09-16, `flows/48cff7/vision/skillSourceKinds.md`, 87

**Left out or in conflict**

- T23, unresolved in any record. 2026-09-24: vision, operation (Mind), compensation (Field). 2026-10-03 (`flows/5ed94b/vision/contextModules.md`): vision, intent, spirit, knowledge, operation, with neither compensation nor trial; 2026-10-03 (notion, 1.2.3): perhaps a better word than compensation; installed skills also use trial- and compensation-. The statement carries the 2026-09-24 types as recorded and leaves the 2026-10-03 list in cluster 7; the main flow brings T23 to him.
- 1.3.25 p2's suffixing (knowledge or vision as suffix) is unclear in the record; left out.
- 1.2.3 (9 words, notion) stays verbatim.

**Sources lines:** `752e0f layers`, `48cff7 skillSourceKinds`.

---

## 15. Behavior modules are chosen at launch — 167 words

**Lands in:** `Vision/flowNexus.md`.

**Proposed statement**

Skills that alter how a flow behaves are behavior modules, features a flow is launched with: the main flow; an expert on a subject; a doubter or critic; a visualizer that makes visualizations; one that knows certain software and how to operate it; a browser that operates web apps for the user. A Flow command launches a flow with these particular skills entered through its startup prompt, and they need not be reachable by any other agent. Knowledge is never restricted so: any agent that wants to know anything can load it. The main flow's system prompt can carry a part its subagents do not receive, so the main flow is programmed one way and its subagents another; whether the harness allows that is to be found out.

**Replaces**

- 1.3.26 p3, 2026-09-16, `flows/48cff7/vision/skillPromotionAndLayering.md`, 113
- 1.1.10 p2, 2026-10-03, `flows/5578cc/vision/flow.md`, 54

**Left out or in conflict**

- T5 and T21. 1.1.10 p2 is a wish and a question; the measurement in the 5ed94b handover bears on it. 1.1.16 (76 words, 2026-09-25, `flows/e51411/notion/stack.md`, notion): whether replacing the subagent tool with a Flow subflow command, each subflow with its own system prompt, costs too much. Stays verbatim as a notion; `Vision/flowNexus.md` already says subflows replace the harness subagent facility, and 2026-10-03 words (subject 2) keep subagent definitions now and flows eventually.
- The restriction of behavior modules draws on 1.3.26 p2 (counted in cluster 4).

**Sources lines:** `48cff7 skillPromotionAndLayering`, `5578cc flow`.

---

## 16. A standard, Nix-defined harness home — 165 words

**Lands in:** `Vision/harness.md` (new topic).

**Proposed statement**

Every new Claude or Codex home gets a standard set of settings, all of them, set automatically with Nix, perhaps from a repository of its own that also documents the options each harness offers. With it a home can be stood up whole, even a semi-sandbox using a copy of the living's tokens to test things. How subagents work is understood harness by harness, and the open-source harness is set up.

**Replaces**

- 1.4.1, 2026-10-04 (file date), `flows/28d847/vision/harness.md`, 132
- 1.4.2, 2026-10-03, `flows/5ed94b/vision/harnesses.md`, 33

**Left out or in conflict**

- 1.4.2's last sentence is an order; carried as the target, the order itself an impurity candidate.
- 1.4.4 (366 words, 2026-09-18, `flows/b05237/vision/operational-criomosModularHardware.md`) stays verbatim: it is mostly CriomOS modularity, a stable and next Codex remote server, and hardware types, off subject 1; its sentence on keeping harnesses stock is T4 (cluster 6).

**Sources lines:** `28d847 harness`, `5ed94b harnesses`.

---

## 17. One source, emitted per harness by `{%` templates — 116 words

**Lands in:** `Vision/curriculum.md`.

**Proposed statement**

A skill is written once. Curriculum emits it into the workspace for each harness supported, regenerating modified skills and adding missing ones, with the blocks that differ by harness written in the Markdown templating language. A template is triggered only by `{%`, so it never collides with skill text. The skill on designing skills says the template syntax exists, and nothing more is needed: no checker.

```
{% if claude %}
Text only Claude's tree receives.
{% endif %}
{% if codex %}
Text only Codex's tree receives.
{% endif %}
```

**Replaces**

- 1.2.1 p3, 2026-10-03, `flows/5ed94b/vision/skills.md` (also `flows/28d847/vision/skills.md`), 70
- 1.2.13, 2026-08-22, `flows/01a01bac/vision/skillDesigning.md`, 33
- 1.2.14, 2026-08-22, `flows/01a01bac/vision/skillDesigning.md`, 13

**Left out or in conflict**

- The code is the syntax in use today in `repos/Curriculum/skills/main-flow.md` and `skills/skill-designing.md`, not new.
- 1.2.1 p3 says the templating is supposedly already implemented; it is (above).

**Sources lines:** `5ed94b skills`, `28d847 skills`, `01a01bac skillDesigning`.

---

## 18. Setup variables — 43 words

**Lands in:** `Vision/curriculum.md`.

**Proposed statement**

A value that differs between setups has a name and is not part of Curriculum; Curriculum's documentation tells agents that such values must be set, and how.

**Replaces**

- 1.2.18, 2026-08-17, `vision-raw/entryFiles.md`, 43

**Left out or in conflict**

- T22, where the values live. 2026-08-17: in their own setup-specific file. 2026-10-03 (1.2.2, cluster 8): skill variables are moving into knowledge-type skills. State: CLAUDE.md still points at `SKILL_VARIABLES.md`, and knowledge skills exist. The statement carries only what both share; the place is his to rule.

**Sources lines:** `vision-raw entryFiles`.

---

## Merge with the current Vision and Intent

Every `Vision/` and `Intent/` file was read for statements these 18 touch. Only these do: `Vision/psyche.md`, `Vision/flowNexus.md`, `Vision/distillation.md`, `Vision/modelRoles.md` (one section), `Intent/startupPrompt.md`, `Intent/context.md`. Nothing in `Intent/` speaks on skills, Curriculum or the system prompt except `startupPrompt.md`. A verdict is one of: new, extends (merged text given), replaces (both texts given), conflicts (both sides stated, nothing settled).

| Cluster | Verdict | Touches |
|---|---|---|
| 1 Vision is skill | New, consistent | `Vision/psyche.md` (unprefixed vision is gold) |
| 2 Top and middle layers | New; conflicts | `Intent/startupPrompt.md`; vocabulary with `Intent/context.md` |
| 3 Three aspect repositories | Replaces and extends | `Vision/psyche.md` (two paragraphs); consistent with `Vision/flowNexus.md` |
| 4 Skill files and names | New; conflicts | `Vision/psyche.md` (prefixes) |
| 5 Rolling distillation | Extends | `Vision/distillation.md` |
| 6 System prompt anatomy | New, consistent | `Vision/flowNexus.md` (basic skills replace the built-in prompt) |
| 7 Context modules | New | vocabulary with `Intent/context.md` |
| 8 Curriculum | New | none |
| 9 Restart, no compaction | Extends; conflicts | `Vision/flowNexus.md` (naming, reaping) |
| 10 Registry and launch list | Extends | `Vision/flowNexus.md`; `Vision/modelRoles.md` (meta wire) |
| 11 Psyche hierarchy | Extends | `Vision/psyche.md` (first line) |
| 12 Tangible proposal | Extends | `Vision/distillation.md` (destination) |
| 13 Edit rights | Extends | `Vision/psyche.md` (operational prefix) |
| 14 Skill types | Conflicts | `Vision/psyche.md` (testing prefix) |
| 15 Behavior modules | Extends; conflicts in part | `Intent/startupPrompt.md`; `Vision/flowNexus.md` |
| 16 Harness home | New | none |
| 17 Templating | New | none |
| 18 Setup variables | Extends; conflicts | `Vision/modelRoles.md` (skill variables) |

### 1. Vision is skill: new, consistent

`Vision/skills.md` does not exist. `Vision/psyche.md` says unprefixed vision is Psyche's most reliable, accepted gold; statement 1 agrees and adds that this gold is skill. No text changes in `psyche.md`.

### 2. Top and middle layers: new; conflicts with `Intent/startupPrompt.md`

- Current (`Intent/startupPrompt.md`): a flow starts from one startup prompt, a single block; startup skills are given to particular flows at their start, never to their subflows, and the harness is configured so the model cannot see or load them; a startup skill enters through the startup prompt.
- Statement 2: steady, distilled spirit, intent and vision go in the system prompt, the top layer; the middle-layer records say the prompt is the best place.
- Conflict, both sides: the Intent places the chosen skills in the startup prompt (middle layer); the top-layer records place distilled modules in the system prompt. They agree that a flow's start is where modules enter, and the Intent's invisibility to subflows matches his wish in statement 15. This is T3; the Intent is approved and later than all but the 2026-10-03 records, which say he does not know the difference. Not settled.
- Vocabulary: `Intent/context.md` uses layer for a level of abstraction (a value carries the context it makes sense in); the package's subject 2 uses layer for flow power levels (primary to quaternary). Statement 2 uses layer for context authority. For the whole to read as one, statement 2 says "context layer" wherever it means authority. Applied to statement 2 above: it replaced "layers of authority" with "context layers of differing authority", and "the top layer" and "the middle layer" with "the top context layer" and "the middle context layer".

### 3. Three aspect repositories: replaces and extends `Vision/psyche.md`

- Current (`Vision/psyche.md`, two paragraphs):
  - Psyche data belongs in a dedicated repository symlinked into Primary. Primary Next begins from Primary's root commit and carries selected repository mounting points plus a README and AGENTS.md explaining those relationships. Orchestrate coordinates concurrent work across those repositories.
  - The skills belong in a repository. This is a target shape, not authorization to create or migrate a repository (native desktop record, archive ordinal 1835).
- Proposed: the second paragraph is replaced by statement 3 (in `Vision/skills.md`), with its last sentence kept as its own guard, since it is part of the approved statement. The first paragraph is extended, and stays in `psyche.md`:
  - Merged text for `Vision/psyche.md`: Psyche data, vision, intent, spirit and notion and nothing else, belongs in a dedicated repository, beside its own logs repository, both symlinked into Primary. Primary Next begins from Primary's root commit and carries selected repository mounting points plus a README and AGENTS.md explaining those relationships. Orchestrate coordinates concurrent work across those repositories.
  - Merged text for `Vision/skills.md`, after statement 3: This is a target shape, not authorization to create or migrate a repository.
- Consistent: `Vision/flowNexus.md` already says every skill lives outside the flow runtime repository so a skill change causes no Nix rebuild; statement 3's clause on Curriculum's code kept apart from skill data matches it.
- T1 remains open (see cluster 3).

### 4. Skill files and names: new; conflicts with `Vision/psyche.md`

- Current (`Vision/psyche.md`): operational vision skills use the `operational-` prefix; testing skills use `testing-`; pure vision skills use neither prefix.
- Statement 4, from 2026-10-02 (1.3.5, 1.3.6): skills are prefixed with vision and something else; every skill sits under its proper prefix. The installed tree uses `vision-`, `knowledge-`, `operation-`, `trial-`, `compensation-`.
- Conflict, both sides: the approved Vision (from the 8393ca record, 2026-09-18) leaves pure vision unprefixed; his 2026-10-02 words prefix it with vision. Not settled; the main flow brings both.

### 5. Rolling distillation: extends `Vision/distillation.md`

`Vision/distillation.md` holds no statement on when distillation happens. Statement 5 lands as a new section, "Distillation rolls as the work goes", placed before "A proposal names each statement's destination". It agrees with "Impurities fall out through distillation" (impurities are not hunted; they fall as distillation rolls). Its "subagent is a type of skill" clause sits beside `Vision/flowNexus.md`'s rule that subflows replace the harness subagent facility; read together, a subagent definition is the skill a fresh flow is launched with. Applied to statement 5 above for homogeneity: "a subagent is a type of skill, one implemented by a fresh flow" became "a subagent definition is a type of skill: the skill a fresh flow is launched with".

### 6. System prompt anatomy: new, consistent

- Current (`Vision/flowNexus.md`): the basic skills give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
- Statement 6 says how the replacement is made (anatomy, classification, corrected version). Consistent; `flowNexus.md` keeps its line, and `Vision/systemPrompt.md` is new. `Intent/data.md` (everything is data) agrees with the prompt's parts kept as data files.

### 7. Context modules: new

`Vision/contextModules.md` does not exist. "Context" in `Intent/context.md` names what a value makes sense in; statement 7 uses "context module" for what a model starts its thinking with. These are two senses; statement 7 defines its term, which is enough for it to stand, and the word clash is one reason he kept the name Curriculum.

### 8. Curriculum: new

No Vision or Intent file speaks on Curriculum.

### 9. Restart, no compaction: extends `Vision/flowNexus.md`; conflicts in two places

- Current (`Vision/flowNexus.md`): "A session is named after its direct ancestor" (a session cannot be named for what it will become; its ancestor is the name) and "A replaced session is reaped by the refresh itself" (the refreshed flow takes the replaced end out of receiving messages, so a dead end is never left registered and addressable).
- Merged text (new section after the reaping section): **A flow restarts rather than compacts.** A flow does not compact. When it grows too big, at 60 percent of its context at the most or sooner when the conversation shifts hard, it restarts on a fresh flow with a fat first prompt carrying its useful state and the high-level intent, spirit, operational flow and operational rules; a main designer flow's first prompt holds the vision for most of its topics. The refresh reaps the replaced flow, as above.
- Conflict, both sides: statement 9 marks the old flow ancestor or concluded and lets a concluded flow be woken at a cost; the reaping section says a replaced end is never left addressable. Statement 9's marking (by thread name) also differs from naming after the ancestor, though the two may be one act seen from either side. Not settled. The merged text above leaves the marking and waking out until he rules.
- Also: `Vision/flowNexus.md` says session, statement 9 says flow; his 2026-10-04 words say flow (T6). Not changed here.

### 10. Registry and launch list: extends `Vision/flowNexus.md`

- Current: "What it does" (the Flow Nexus sets up a flow's working directory, system prompt, training files and instruction prompt) and "Starting flows" (a Nexus component decides the system prompt and everything about a launch).
- Merged text for "What it does": The Flow Nexus sets up and starts a model flow: its working directory, system prompt, context modules and startup prompt. It takes the place of the abandoned training daemon. It keeps a registry of every context module's name and location, served through the meta wire and updated when a skill is added; a launch names, per place, the module types and their names, and Flow inserts each in its place.
- "Training files" and "instruction prompt" become "context modules" and "startup prompt", the words of statement 10, statement 7 and `Intent/startupPrompt.md`. That rewording is itself a proposal and needs his word.
- Vocabulary: his 1.1.6 says meta socket; `Vision/modelRoles.md` says the model is mutated only through the meta wire. Both name one thing; the merged text uses meta wire to match the landed Vision. Statement 10 above now says meta wire.
- `Vision/modelRoles.md` (one declaration in Flow, typed, carried by skill variables) is consistent: the registry is more typed configuration in Flow.

### 11. Psyche hierarchy: extends `Vision/psyche.md`

- Current (first line): Psyche contains Spirit, Intent, Vision, and Notion, in descending authority.
- Merged text: Psyche contains Spirit, Intent, Vision, and Notion, in descending authority, and its output is distillation: vision is distilled often, intent out of vision, spirit out of intent, and notion is distilled too. Vision is what is seen clearly enough to try now; intent is where the project is going; spirit is how everything is approached, how the work is done and how one behaves. A module depends only on its own kind or what is above it, down to trial at the bottom.
- The ethos struct and the registry stay in statement 11, landing in `Vision/curriculum.md` beside statement 8, since they describe Curriculum's types, not the psyche. That moves part of statement 11's landing; its other part lands in `psyche.md` as merged above.

### 12. Tangible proposal: extends `Vision/distillation.md`

- Current ("A proposal names each statement's destination"): a distillation proposal says, for every statement, the topic it goes to; a statement under the wrong topic is corrected by a distillation edit of its own.
- Merged text: **A proposal is tangible and names its destination.** A distillation proposal says which module, which edit, what is removed and what replaces what, and for every statement the topic it goes to; a statement under the wrong topic is corrected by a distillation edit of its own. It distills with the distillate, reading the distilled vision it would land in. One subject gets one unified statement. Nothing in it is vague or supposed, and a list of what he said that makes no point is not a proposal.
- The untagged tension 1.3.36 against 1.3.37 stays; `Vision/distillation.md` has no line on it.

### 13. Edit rights: extends `Vision/psyche.md`

- Current: operational vision skills use the `operational-` prefix and support faster iteration with an overview to the living. Unprefixed vision is Psyche's most reliable, accepted gold.
- Merged text (in `Vision/skills.md`, with the `psyche.md` sentence moved there): Operational skills, the ones agents write for themselves, use the `operational-` prefix, iterate faster with an overview to the living, are less reviewed and less trusted, and are more likely to be taken out than vision. The golden skills, the most trusted, live in their own repository, and changing them takes more approval. Each aspect is in charge of its own skills; a change wanted in another aspect's skill goes by message to that aspect, and to the living through Psyche when it is psyche's.
- Whether the golden skills are the unprefixed vision of `psyche.md` is not said in any record.

### 14. Skill types: conflicts with `Vision/psyche.md`

- Current: testing skills use `testing-`.
- Statement 14 (2026-09-24): testing is a notion, and becomes compensation once it holds. The installed tree uses `trial-`, which neither names.
- Conflict, both sides: the approved Vision gives testing its own prefix as a kind of skill; the later record makes testing a notion, a stage before compensation. T23 also stands. Not settled.

### 15. Behavior modules: extends `Intent/startupPrompt.md`; conflicts in part

- Current (`Intent/startupPrompt.md`): startup skills are given to particular flows at their start and never to their subflows; the harness is configured so the model cannot see or load them; they enter through the startup prompt.
- Statement 15's behavior modules are these startup skills, named by what they do. Merged text (in `Intent/startupPrompt.md`, after its first paragraph; it is an Intent file, so this needs his explicit word to enter Intent): Startup skills are behavior modules: the main flow, an expert, a doubter or critic, a visualizer, an operator of some software, a browser of web apps. Knowledge is never a startup skill; any flow may load it.
- Conflict in part: statement 15 also wants a part of the main flow's system prompt its subagents do not receive; the Intent reaches the same end through the startup prompt, and `Vision/flowNexus.md` says subflows run under their own system prompts. Whether the system-prompt route is still wanted is T3 and T5. Not settled.
- Applied to statement 15 above for homogeneity: "loaded in its prompt" became "entered through its startup prompt".

### 16, 17. Harness home, templating: new

No Vision or Intent file speaks on harness homes or on Curriculum's templates.

### 18. Setup variables: extends `Vision/modelRoles.md`; conflicts

- Current (`Vision/modelRoles.md`): skill variables carry the model value by name into every skill, launcher and brief; nothing else holds a model name.
- Statement 18 is consistent and general: every setup-specific value has a name and lives outside Curriculum. Merged text (in `Vision/curriculum.md`): A value that differs between setups has a name and is not part of Curriculum; Curriculum's documentation tells agents that such values must be set, and how. Skill variables carry such a value by name into every skill, launcher and brief.
- Conflict, T22: the variables file (2026-08-17, and the present CLAUDE.md) against knowledge-type skills (2026-10-03). Not settled.

## Left verbatim (1,267 words)

| Quote | Date, source | Words | Why |
|---|---|---|---|
| 1.1.11 | 2026-10-03 (file date), `flows/dea0ba/vision/contextModules.md` | 55 | An order (full implementation shown as built; who choreographs). Impurity candidate. |
| 1.1.12 p2, p3 | 2026-10-03, `flows/5ed94b/vision/visionBooks.md` | 110 | T5, contested by measurement. |
| 1.1.16 | 2026-09-25, `flows/e51411/notion/stack.md` | 76 | Notion, a question. T21. |
| 1.1.17 p2 | 2026-09-24, `flows/d8df70/vision/mainFlowMode.md` | 75 | Exhortation. Impurity candidate. |
| 1.2.1 p4 | 2026-10-03, `flows/5ed94b/vision/skills.md` | 13 | An order. Impurity candidate. |
| 1.2.3 | 2026-10-03, `flows/5578cc/notion/skills.md` | 9 | Notion. T23. |
| 1.2.4 | 2026-09-29, `flows/c64ee3/notion/curriculum.md` | 44 | Notion: Curriculum as personality building or post-training. |
| 1.2.8 p3 | 2026-09-24, `flows/26c50c/vision/curriculum.md` | 56 | Uncertain (a raw database for now; migrate to mind; maybe wasted effort). |
| 1.2.9 p3 | 2026-09-20 (file date), `flows/b80e55/vision/curriculumAndTriadSkillGeneration.md` | 59 | Primary Next and the three log sectors, mixed with an order. |
| 1.2.10 | 2026-09-16, `flows/48cff7/vision/curriculumSubagentGap.md` | 65 | Unsure by his own words (whether Curriculum deletes absent files; a namespace maybe); go with how it works for now. |
| 1.2.17 | 2026-08-17, `flows/358f143a/vision/skillsRepository.md` | 90 | A claim about the industry's vocabulary (training is what context does to a model; model creation is genesis). Condenses poorly; T2. |
| 1.3.2 | 2026-10-03 (file date), `flows/28d847/vision/skills.md` | 17 | Already as short as a statement; the trial-recurring-failure skill carries it. |
| 1.3.20 p3, remainder | 2026-09-18 (file date), `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md` | about 188 | Persona levels, Primary Next, history rewrite, data growth. Off subject 1. |
| 1.3.37 | 2026-08-19, `flows/7c3f0c1d/vision/psycheLogStructure.md` | 44 | A correction of a draft's wording; condenses poorly; untagged tension with 1.3.36. |
| 1.4.4 | 2026-09-18 (file date), `flows/b05237/vision/operational-criomosModularHardware.md` | 366 | CriomOS, servers, hardware types; off subject 1. T4 sentence pointed at from cluster 6. |

## Already distilled (215 words, no new statement)

| Quote | Source | Words | Where it already stands |
|---|---|---|---|
| 1.2.11 | `flows/acbb6006/vision/archive-nexus.md` | 19 | `Vision/flowNexus.md`, Repository and skills |
| 1.3.19 | `flows/8393ca/vision/operational-herdrVoiceAccess.md` | 19 | `Vision/psyche.md` (the skills belong in a repository); cluster 3 would replace that line |
| 1.3.33 | `flows/b675f3d9/vision/archive-visionImpurities.md` | 45 | `Vision/distillation.md`, Vision impurities |
| 1.3.34 | `flows/acbb6006/vision/archive-distillation.md` | 86 | `Vision/distillation.md` and the skill; `Vision/sources/` |
| 1.3.35 | `flows/ac1e9ec8/vision/archive-distillationNegatives.md` | 46 | `Vision/distillation.md`, No useless negatives |

## Notes for the main flow

- The merge section changes no `Vision/` or `Intent/` file; it gives the merged texts for his approval. Merged text for an `Intent/` file (cluster 15) needs his explicit word to enter Intent.

- Statements 8, 10 and 11 carry illustrative code because they describe types. Their names and fields are placeholders built from his description; each says so. Statement 17's code is the syntax already in use.
- Clusters 2, 3, 7, 14 and 18 each hold an open tension (T3, T1, T2, T23, T22) that his words do not settle. The statements carry both sides; each tension is his to rule before its statement can stand as a rule.
- Untagged tensions found here: vision against skill (cluster 1); one repository against three (cluster 3); Curriculum's scope and the manifest against the registry (cluster 8); 1.3.36 against 1.3.37 (cluster 12).
