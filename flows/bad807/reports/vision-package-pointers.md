# Pointers into the Fable package vision report

Source: `flows/28d847/reports/fable-package-vision.md`. Part A is copied by line extraction, not retyped. Part B is generated from the report's own headings, dates and sources; the gist is the report's heading as written (some are cut off in the report itself). Part C is written by the gathering agent from the report's section lead-ins and quote headings.

## A. Tensions T1-T5, T20, T22, T23 (verbatim, lines 2866-2965)

**T1. Where skills live: Curriculum or three repositories (psyche, mind, field).**
- 2026-10-03, `flows/28d847/vision/skills.md`: "We shouldn't be putting skills in curriculum"; "curriculum doesn't hold the skills. They're in other repositories ... psyche, mind, and field."
- 2026-09-29, `flows/183ae0/vision/skills.md`: skills are not to be in the curriculum anymore; "Curriculum is just the executable source code"; three skill repos, or scrap deploying skills for now.
- 2026-09-17, `flows/108ab0/vision/operational-skillLagsVisionObservability.md`: "Curriculum skills is good for now."
- State: `/home/li/primary/CLAUDE.md` says to regenerate from the Curriculum skills; the 28d847 handover says Primary is on Curriculum main with 70 skills and lists "which skills go to psyche, mind, field" as waiting on him; the 5ed94b handover says an approved line landed in Curriculum (d65062). Later: the 2026-10-03 words. The state still lands skills in Curriculum.

**T2. The name of the thing, and the word for the family of modules.**
- 2026-08-17, `flows/358f143a/vision/skillsRepository.md`: "curriculum is the wrong name; training is right", then "keep the name the same" and a new repo called training.
- 2026-10-03, `flows/edf227/vision/contextModules.md`: "Maybe the curriculum component is just called context. That's not a big deal." Later the same day, `flows/5578cc/vision/curriculum.md`: keep Curriculum, because "the word context is used a lot."
- 2026-10-03, `flows/5ed94b/vision/contextModules.md`: "Let's find a better word" for the family of vision, intent, spirit, knowledge, operation. State: the 5ed94b handover lists "faculties" as proposed and unanswered. Later: Curriculum stays; the family word is open.

**T3. System prompt or user prompt: where a module goes.**
- 2026-09-13, `flows/024bc7/vision/context.md`: his words go in the middle layer until distilled; the distillation goes in the top layer, the system prompt. 2026-09-14, `flows/6cc91b/vision/skills.md`: vision into the middle stratum; maybe the skill moves to the system prompt. 2026-09-15, `flows/fd0f97/vision/firstPrompt.md`: the primary's system prompt should hold all the vision it can. 2026-09-17, `flows/b49251/vision/systemPrompt.md`: vision in the injected prompt or in the system prompt. 2026-09-18, `flows/b05237/vision/operational-fableRestartWithRecoveredVision.md`: restart Fable with the vision in the middle prompt layer. 2026-09-24, `flows/d8df70/vision/mainFlowMode.md`: main-flow mode can only be held by the system prompt. 2026-09-25, `flows/e51411/vision/systemPrompt.md`: steady, distilled spirit, intent and vision go into the system prompt.
- 2026-10-03, `flows/5ed94b/vision/contextModules.md`: "I don't know enough about what difference modifying the system prompt makes over modifying the user prompt." The same day, `flows/5578cc/vision/flow.md`: he asks whether part of the system prompt can be withheld from the harness's subagents.
- Later: he states he does not know, so the placement is open; the order on 2026-10-04 is to load high-quality modules in the system prompt. Distilled, not his word: `Intent/startupPrompt.md` (startup skills enter through the startup prompt and are invisible to subflows).

**T4. Replace the harness's system prompt, or keep the harness stock.**
- 2026-08-23, `flows/2f6b1dc5/vision/systemPrompt.md`: "I want to replace claude and codex's system prompts." 2026-08-17, `flows/358f143a/vision/falseConfidence.md`: heavy modifications of the harness prompts. 2026-10-03, `flows/5578cc/vision/flow.md`: the system prompt is to be broken into modules.
- 2026-09-18, `flows/b05237/vision/operational-criomosModularHardware.md`: "keep the harnesses as stock as possible in one version ... the ordinary executable name and the desktop apps." This reads as the harness program, not its prompt, so the two may not conflict; the record does not say.

**T5. What subflows and subagents receive from the main system prompt.**
- 2026-10-03, `flows/5ed94b/vision/visionBooks.md`: "There's no way they get nothing. They wouldn't know how to use the tools"; the answer was called bluffing. 2026-08-18, `flows/358f143a/vision/gradientsOfAuthority.md`: "I dont rule how things work ... Only the code can answer." 2026-10-03, `flows/5578cc/vision/flow.md`: he wants a part of the main flow's system prompt that subagents do not get.
- State, the 5ed94b handover (measurement by flow 42265e, `flows/42265e/reports/harness-context-measurement.md`): a Codex collaborator carries the parent's base instructions (21,420 characters), not its developer instructions; a Claude subagent carries its own definition body plus two fixed paragraphs; forks inherit replaced or appended prompts; tool schemas unmeasured.

**T20. Distilling: "just keep logging" or a constant flow of proposals.**
- 2026-09-03, `flows/e4a40e/vision/distillation.md`: "you can change the skill to say just keep logging" because no distillation had landed. 2026-10-01, `flows/04db2fd2/vision/rollingDistillation.md`: roll with distilling as we go. 2026-10-03, `flows/5ed94b/vision/skills.md`: a constant flow of small skill-edit proposals; vision distillation is skill editing. Later: proposals.

**T22. Skill variables: the variables file or knowledge skills.**
- 2026-08-17, `vision-raw/entryFiles.md`: variables go in their own setup-specific file. 2026-10-03, `flows/5578cc/vision/skills.md`: "we're moving these skill variables into knowledge-type skills." State: `/home/li/primary/CLAUDE.md` still says the variables are in `SKILL_VARIABLES.md`; knowledge skills such as knowledge-layer-models exist. Later: knowledge skills.

**T23. The kinds of skill and module.**
- 2026-09-24, `flows/752e0f/vision/layers.md`: vision, operation (Mind), compensation (Field). 2026-10-03, `flows/5ed94b/vision/contextModules.md`: vision, intent, spirit, knowledge, operation. 2026-10-03, `flows/5578cc/notion/skills.md` [NOTION]: "a better word than compensation". 2026-10-03, `flows/5578cc/vision/ethos.md`: role is missing from the registry's kinds and `kind` collides with ethos's `kind`. 2026-08-22, `vision-raw/spirit.md`: the spirit skill retires once entry files carry spirit.
- State: the installed skill names also use trial- and compensation-; his 2026-10-03 list has neither. Not resolved in any record.

---

## B. Pointers: number, date, source, gist (1.2 from #8, all of 1.3, all of 1.4)

### 1.2 Curriculum, per-harness generation, templating
- #8. Repository-level type and psyche storage — 2026-09-24 | 2026-09-24 | `flows/26c50c/vision/curriculum.md`
- #9. The curriculum generator is just a binary, a nexus with CLIs. Three types of skills from three repos, each with its own  | 2026-09-20 (file date, approximate) | `flows/b80e55/vision/curriculumAndTriadSkillGeneration.md`
- #10. 2026-09-16 — Curriculum has no authored surface for specialty subagents; roles.datom generates only permission×depth wor | 2026-09-16 | `flows/48cff7/vision/curriculumSubagentGap.md`
- #11. Skills live outside the runtime repository | 2026-09-10 (file date, approximate) | `flows/acbb6006/vision/archive-nexus.md`
- #12. 2026-08-25T00:14:33+02:00 | 2026-08-25 | `flows/01a035d3/vision/archive-rustCodeFromTheData.md`
- #13. 2026-08-22T12:56:32+02:00 — the only need is for an indication in the skill design skill to know about the template synt | 2026-08-22 | `flows/01a01bac/vision/skillDesigning.md`
- #14. 2026-08-22T12:43:17+02:00 — if the templates are only triggered by {% then there is no collision | 2026-08-22 | `flows/01a01bac/vision/skillDesigning.md`
- #15. 2026-08-21 — get rid of the manifest and generate whatever skills are present; the elaborate phase's breakup into module | 2026-08-21 | `vision-raw/skillsRepository.md`
- #16. 2026-08-17 — Curriculum is the wrong name; training is right; keep Curriculum, the rewrite is a new repo `training` | 2026-08-17 | `flows/358f143a/vision/skillsRepository.md`
- #17. 2026-08-17 — Curriculum is the wrong name; training is right; keep Curriculum, the rewrite is a new repo `training` | 2026-08-17 | `flows/358f143a/vision/skillsRepository.md`
- #18. 2026-08-17 — variables have names; they live in their own setup-specific file, documented in Curriculum's agents.md | 2026-08-17 | `vision-raw/entryFiles.md`

### 1.3 Skills as generated data, three repositories, vision distillation writes skills
- #1. The vision becomes the skills; the data is written where the curriculum tool generates them | 2026-10-03 | `flows/5ed94b/vision/visionBooks.md`
- #2. A recurring failure means a skill lacks the line | 2026-10-03 (file date, approximate) | `flows/28d847/vision/skills.md`
- #3. Skills live in their own repository, not in Curriculum | 2026-10-03 (file date, approximate) | `flows/28d847/vision/skills.md`
- #4. Skills live in three repositories: psyche, mind and field | 2026-10-03 (file date, approximate) | `flows/28d847/vision/skills.md`
- #5. Vision has to become skills | 2026-10-02 | `flows/3ec648/vision/skills.md`
- #6. Move every skill touching the work into the proper prefix skill | 2026-10-02 | `flows/3ec648/vision/skills.md`
- #7. A distillation is split into the right skills | 2026-10-02 | `flows/91ea9f/vision/distillation.md`
- #8. A question is a layer of mind, as spirit, vision and notion are layers of psyche; vision is skill | 2026-10-01 | `flows/fe945a/vision/questions.md`
- #9. 2026-10-01 — STT, to Psyche Opus fe945a, relayed to every psyche seat (corrections applied by fe945a) | 2026-10-01 | `flows/bd0019/vision/skillProposals.md`
- #10. Distill vision as we go; every second or third turn agents propose distillation; too much raw vision piles up and goes s | 2026-10-01 (file date, approximate) | `flows/04db2fd2/vision/rollingDistillation.md`
- #11. Distilled vision is automatically a skill | 2026-09-29 (file date, approximate) | `flows/183ae0/vision/skills.md`
- #12. Skills leave the Curriculum; three skill repos | 2026-09-29 (file date, approximate) | `flows/183ae0/vision/skills.md`
- #13. Three skill repos, and log repos beside them | 2026-09-29 (file date, approximate) | `flows/183ae0/vision/skills.md`
- #14. c64ee3-8 — the new skill stack: three source repos, three logs repos, skills loaded into the curriculum database | 2026-09-29 | `flows/c64ee3/vision/skills.md`
- #15. 8904b1-22 — 2026-09-28, the living, direct to this pane | 2026-09-28 | `flows/8904b1/vision/skills.md`
- #16. 8904b1-15 — 2026-09-28, the living, direct to this pane | 2026-09-28 | `flows/8904b1/vision/skills.md`
- #17. Vision, operation, compensation | 2026-09-24 | `flows/752e0f/vision/layers.md`
- #18. Whenever we write a vision, we should be writing a skill. There's a repo called Psyche where all the vision goes, that g | 2026-09-20 (file date, approximate) | `flows/b81560/vision/operational-visionIsSkillThreeRepos.md`
- #19. The skills should have a repository | 2026-09-18 | `flows/8393ca/vision/operational-herdrVoiceAccess.md`
- #20. Vision becomes its own repo: psyche data, mind data, field data. Primary workspace is a template. Harness takes vision d | 2026-09-18 (file date, approximate) | `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md`
- #21. Operational is the stuff the agents write. It lives in a different repo — a different module — with the `operational-` p | 2026-09-17 (file date, approximate) | `flows/108ab0/vision/operational-operationalSkillsRepo.md`
- #22. Unify. There is no separate Datom skill and Datom vision — same thing. A topic has faces: the core (named just by the to | 2026-09-17 (file date, approximate) | `flows/108ab0/vision/operational-skillIsVisionUnified.md`
- #23. Consider using Curriculum at runtime with vision files as one of the sources for skill generation — primary's vision as  | 2026-09-17 (file date, approximate) | `flows/108ab0/vision/operational-skillLagsVisionObservability.md`
- #24. What runs today is Vision, Intent, Spirit. Notion is below Vision — a distilled Notion that has not been done yet but sh | 2026-09-17 (file date, approximate) | `flows/108ab0/vision/operational-distillationHierarchy.md`
- #25. 2026-09-16 — composed skills become vision automatically; skill kinds are typed by their source layer (vision · mind · u | 2026-09-16 | `flows/48cff7/vision/skillSourceKinds.md`
- #26. 2026-09-16 — a path from distilled vision to skill; vision-as-skill, rationale as extended; spirit and intent in the top | 2026-09-16 | `flows/48cff7/vision/skillPromotionAndLayering.md`
- #27. 2026-09-16 — the kinds of skill and psyche-level; the future Curriculum-nexus generates them with deterministic names | 2026-09-16 | `flows/48cff7/vision/skillKindsTaxonomy.md`
- #28. 2026-09-16 — distillation is the output of the psyche; we are always distilling vision or intent | 2026-09-16 | `flows/48cff7/vision/psycheIsDistillation.md`
- #29. 2026-09-12 — When a topic involves gathering vision, distill what is still raw and propose the skill edit | 2026-09-12 | `flows/9e7c9f/vision/distillAnythingThatIsUsed.md`
- #30. 2026-09-03 — just keep logging | 2026-09-03 | `flows/e4a40e/vision/distillation.md`
- #31. 2026-09-03 — a proposal says where it goes and what it replaces, distilling with the distillate | 2026-09-03 | `flows/e4a40e/vision/distillation.md`
- #32. Vision carries the detail; a skill is its concentration; distilled vision must carry actual code, ethos beside the Rust  | 2026-08-30 (file date, approximate) | `flows/62022e8f/vision/distilledVision.md`
- #33. Working instructions logged as vision are impurities; found in distillation, they are destroyed, not archived | 2026-08-27 (file date, approximate) | `flows/b675f3d9/vision/archive-visionImpurities.md`
- #34. Every distillation refers to the raw psyche it came from; the references sit in one sources file per topic | 2026-08-27 (file date, approximate) | `flows/acbb6006/vision/archive-distillation.md`
- #35. 2026-08-26 — useless negatives are archived, and the archive is linked | 2026-08-26 | `flows/ac1e9ec8/vision/archive-distillationNegatives.md`
- #36. 2026-08-19 — propose the distillation skill; one unified statement for one subject | 2026-08-19 | `flows/7c3f0c1d/vision/psycheLogStructure.md`
- #37. 2026-08-19 — the distillation skill draft mixes the particular with universals; one statement is a falsehood | 2026-08-19 | `flows/7c3f0c1d/vision/psycheLogStructure.md`

### 1.4 Harnesses (per-harness setup)
- #1. A standard, Nix-defined setup for every Claude and Codex home | 2026-10-04 (file date, approximate) | `flows/28d847/vision/harness.md`
- #2. Understand subagents per harness; set up the open-source harness | 2026-10-03 | `flows/5ed94b/vision/harnesses.md`
- #3. All useful hooks on all harnesses documented; the open-source harness research completed | 2026-10-01 | `flows/fe945a/vision/hooks.md`
- #4. Keep harnesses stock, get an anatomy of CriomOS, see what should be taken out. Hardware type for Libre M5. Stable/next c | 2026-09-18 (file date, approximate) | `flows/b05237/vision/operational-criomosModularHardware.md`
- #5. The classifier-refusal-stop rule I proposed isn't spirit-level — it's harness-specific. Spirit is universal; different m | 2026-09-17 (file date, approximate) | `flows/da1e3f/vision/operational-harnessSpecificRules.md`
- #6. 2026-09-14 — A draft of the entirely self-authored open-source stack; be honest about how I work and ask me how work, la | 2026-09-14 | `flows/6cc91b/vision/openSourceStack.md`

## C. Two-line summaries, subjects 2-8

**2. Flow (70 quotes).** Covers who talks to whom (Opus as secretary, Fable spoken to rarely, speech climbs one layer at a time), Primary designing and Secondary building, and the layers, voices and model-per-layer words.
Also covers roles, flow launching and subflows replacing the harness's subagent facility; the report notes "seat" is his earlier word and "voice" his later (T6).

**3. Ethos and datom (36 quotes).** His words on ethos code and datom, latest first, beginning with the 2026-10-03 order for far more comments in ethos code.
Code shown as code and ethos/datom shown in presentations is kept in section 5.1; the three nexus parts are in section 4.

**4. The nexus (25 quotes).** Opens with the 2026-10-04 words for a standard, macro-like entry point enforcing the three-part flow signal, operation, memory and back.
Earlier records cover the three-part naming and whether every nexus gets a standard main (T15, T16).

**5. Presentations and books (41 quotes).** Series, code and ethos shown in books, and the rule that illustrations must convey information; drawings settled on SVG, no Mermaid (T11).
The words for what he reads shift among page, book, booklet and user interface or living messenger (T12).

**6. Deterministic work in code (13 quotes).** Mechanical work is done by code, never by the model, and the models judge.
He asked for this to be developed into Intent on 2026-10-03; Intent/ holds no such statement yet.

**7. Publishing and infrastructure (23 quotes).** Infrastructure (flows crippled by lack of it), publishing and version control (one shared tree, merge queue, orchestrate), and quotas, spending and accounting.
Tensions: shared checkout versus separate clone (T19), careful spending versus using idle quota (T18).

**8. Reading and answering the living (13 quotes).** Cross-cutting rules for how his words are read and how a seat answers him; an unknown is found out, then told.
The report marks it as not one of the requested subjects.

## Sources

- `/home/li/primary/flows/28d847/reports/fable-package-vision.md` (read in full for section 1, tensions and headings; sections 2-8 read by heading and lead-in only)
- Receipt handle: unavailable (no PROVENANCE handoff exists yet)
