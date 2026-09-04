# Design brief: anatomy of the 38dec9 proposal

Assembled from four psyche acquisition reports (flow 7b4d4c):
`psyche-harnesses.md`, `psyche-context-strata.md`, `psyche-vocabulary.md`, `psyche-skill-process.md`.

Each constraint is a verbatim psyche sentence (block-quoted), followed by its level, date, flow, and path. Superseded entries are marked. Forks and oddities follow each component.

---

## A. Vocabulary: "agent" becomes "machine" / "thinking machine"; where the word still stands

### Constraining entries

> The word 'agent' becomes 'machine' if the context allows it. Otherwise, 'thinking machine' to be more specific, but 'machine' is really just a short for 'thinking machine.'

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/agentToMachine.md`

> We don't use the word 'agent,' so let's try and also see where we can edit that.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/harnessVocabulary.md`

> in a sentence like this, thinking machine should be used specifically instead of the shortened machine, as the context makes it ambiguous.

-- raw Vision, flow 01a05487. `flows/01a05487/vision/thinkingMachine.md`

> the idea behind flow is simple; a flow of thought. An intelligence isnt a single flow of thought, it is a multitude of flows. so using the term "agent", which entails subjectivity, when speaking of a single flow does not correspond with reality.

-- raw Vision, 2026-08-26, flow 4ddc321d. `flows/4ddc321d/vision/flow.md`

> the machine is the term that I want to use, which is just basically a short for thinking machine.

-- raw Vision, flow 01a052b6. `flows/01a052b6/vision/vocabulary.md`

> An agent is a machine; it does not misbehave.

-- Spirit. `.claude/skills/spirit/SKILL.md`

> Use machine, not AI; use flow, not agent, except when reproducing an external name or quotation.

-- deployed vocabulary skill (distilled Vision level). `.claude/skills/vocabulary/SKILL.md`

### Where the word still stands (witnessed)

58 editable lines across entry files (19), authored skills (29), distilled Vision (6), plus 3 file names, 3 directory names, 1 skill name. Legacy raw vision (~156 lines) is historical record, not editable.

### Forks

- Whether the spirit line "An agent is a machine" should be reworded to "A flow is a machine" or left as-is since spirit predates the vocabulary ruling.
- Whether file and directory names (`AGENTS.md`, `NON_MANAGEMENT_AGENTS.md`, `.agents/`, `.claude/agents/`) change now or wait for a broader renaming pass.
- Whether the skill name `agent-harness-packaging` is renamed now.

### Oddities

The vocabulary report notes: the spirit line uses "agent" twice and the vocabulary skill rules "use flow, not agent" -- these stand in tension, with no ruling on which yields.

---

## B. Per-harness skills and the universal remainder

### Constraining entries

> Let's maybe create a Claude harness skill and a Codex harness skill, and move some of the harness-specific information that may already exist in some skills into those, and then start putting everything in there that we know: how to override the system prompt, which part of the system prompts cannot be overridden by that flag, how many strata each harness actually has (I believe Codex has 4 and Claude has 3), whether the system prompt is visible to the model or the machine, and not to me

-- transcript-only, 2026-09-04, flow 38dec9 L169.

> Give me a draft on how we would do all of this per harness skill and what we could keep that's universal. Maybe the strata or the context strata skill can still remain, but have only the high-level concepts, like the explanation of what these strata are in the entire field of thinking machines and so on.

-- transcript-only, 2026-09-04, flow 38dec9 L169.

> the description is bad. and LLM should appear in the skill, possibly in the description, which should also indicate that this skill is rarely ever needed

-- raw Vision, 2026-08-19, flow 7c3f0c1d. `vision-raw/gradientsOfAuthority.md`

> anyone who deals with designing or implementing anything that involves knowing about the strata

-- raw Vision, 2026-08-19, flow 7c3f0c1d. `flows/7c3f0c1d/vision/gradientsOfAuthority.md`

### Forks

- What material from the context-strata skill moves into per-harness skills vs. what stays as the "universal remainder" (field-wide concepts).
- Whether DeepSeek gets its own per-harness skill immediately or only after packaging (see G).

---

## C. Harness seizure: authoring/overriding the system prompt, what cannot be overridden, visibility

### Constraining entries

> I want to replace claude and codex's system prompts with a version that doesnt incentivize the sort of behavior im constantly steering against.

-- raw Vision, 2026-08-23, flow 2f6b1dc5. `flows/2f6b1dc5/vision/systemPrompt.md`

> Let's look at the most offensive base prompt blocks first, and design replacement for each, and work our way through the entire offensive corpus like this

-- raw Vision, 2026-08-23, flow 2f6b1dc5. `flows/2f6b1dc5/vision/systemPrompt.md`

> no, *you* can see it. I cant. We should make that clear in one of the skills

-- transcript-only, 2026-09-04, flow 38dec9 L135.

> seizure -> harness seizure

-- raw Vision, 2026-08-18, flow 358f143a. `flows/358f143a/vision/letsUseTheSameVocabulary.md`

> So we're going to completely hijack the harness, which was my original idea, but now I want it even more because I realize how powerful this is going to become.

-- raw Vision, 2026-08-10, flow c6b71b4c. `vision-raw/gradientsOfAuthority.md`

> It may be that those prompts *do* reach the top strata, but they are not the entire top strata, else the model couldnt use the harness tools.

-- raw Vision, 2026-08-18, flow 358f143a. `flows/358f143a/vision/gradientsOfAuthority.md`

> just show me the block that you think is most harmful, and well proceed through them like that one by one, marking them for replacement or deletion.

-- raw Vision, 2026-08-25, flow 4ddc321d. `flows/4ddc321d/vision/hijackRepositories.md`

### Forks

- The block-walk is in progress (some blocks marked delete or replace in flows 4ddc321d, ceb3b9fd); the remainder of the corpus has not been walked.
- Whether per-harness skills document what cannot be overridden (tool-use instructions baked into the harness) or whether this becomes part of the system prompt repository.

---

## D. Wrapper executables under other names

### Constraining entries

> I would probably just rename the executable of the wrapper something else so that we can still use the stock version, and call the wrapper something else, like Claude Light or Claude Unopinionated, or maybe Codec Unsafe if we take all the safety out and stuff, or Codec Bare where we have almost nothing.

-- raw Vision (transcript captured), 2026-09-04, flow 38dec9. `flows/38dec9/vision/perHarnessSkills.md`

> We should just create a separate repository that anyone could use to give modified versions with different names of Claude and Codex, with different takes on system prompts.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/systemPromptRepository.md`

> we were gating agent-intercom before because it would modify codex and claude, but now I only want different executables (different names) to be wrapped with the agent-intercom wrapped codex and claude, so we dont need a gate at all.

-- raw Vision, 2026-08-28, flow 01a048a6. `flows/01a048a6/vision/agentIntercomGraphical.md`

> I am no longer interested in heavily modifying those applications to achieve better functionality.

-- raw Vision, 2026-09-02, flow ea1e56. `flows/ea1e56/vision/desktopCodexIntegration.md`

### Forks

- Whether the wrapper names ("Claude Light", "Claude Unopinionated", "Codex Bare", "Codex Unsafe") are final or placeholders from a dictation session.
- Whether desktop applications (Claude Desktop, ChatGPT Desktop) get wrapper variants or only CLI executables, given the retracted interest in desktop modification.

---

## E. The system prompt repository (lineage in "codex-hijack" / "claude-hijack")

### Constraining entries

> let's start with a repository to do this work. Perhaps one for each harness; codex-hijack and claude-hijack. We'll start with codex which I believe is the worst offender. Make the repos public and start with a thorough documentation of their stock context, what each block is tied to, how it can be overriden, etc etc.

-- raw Vision, 2026-08-25, flow 4ddc321d. `flows/4ddc321d/vision/hijackRepositories.md`

> We should just create a separate repository that anyone could use to give modified versions with different names of Claude and Codex, with different takes on system prompts.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/systemPromptRepository.md`

> we dont care about anything but 5.6

-- raw Vision, 2026-08-25, flow 4ddc321d. `flows/4ddc321d/vision/hijackRepositories.md`

> I think an orca repo is smarter than cramming more stuff in the home repo

-- raw Vision, 2026-08-23, flow 01a02f23. `flows/01a02f23/vision/orca.md`

### Forks

- Whether the original two-repo design (codex-hijack + claude-hijack) is superseded by the 38dec9 single "separate repository" language, or the two coexist.
- Whether the repository is public (as ruled in 4ddc321d) or the 38dec9 "anyone could use" statement modifies this.

---

## F. The invocation system: composing the harness call with the right top stratum

### Constraining entries

> One of the repositories, either harness or Flow, or maybe both of them are involved somehow, is going to actually create the system call with the right flag to invoke the harness with the right system prompt or the right top stratum.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/invocationSystem.md`

> In my vision, we're going to have different top stratums for different jobs. The top stratum will be programmable per flow.

-- raw Vision, 2026-08-30, flow ceb3b9fd. `flows/ceb3b9fd/vision/topStratum.md`

> a phase is its own flow, with its own top stratum

-- raw Vision, 2026-08-30, flow ceb3b9fd. `flows/ceb3b9fd/vision/topStratum.md`. **Superseded in part**: "phase" withdrawn 2026-09-03 (flow b9f4f6) -- "I don't know what you mean by 'phase.' Either we have to define what the phase is, or otherwise that's bluffing." The underlying vision (different top stratums for different jobs) stands.

> The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt.

-- distilled Vision. `Vision/flowNexus.md`

> yes for now. we will create our own custom harness in the future, which will be 100% typed datom messages going in and being expected out.

-- raw Vision, 2026-08-21, flow 15b67974. `flows/15b67974/vision/flowDaemon.md`

> That repo hasent been touched in a long time, even though it's slated to orchestrate the entire meta harness (called persona)

-- raw Vision, 2026-08-21, flow 15b67974. `flows/15b67974/vision/persona.md`

### Forks

- Which repository owns the invocation logic: the Flow Nexus repo, the system prompt repo, or both.
- Whether the persona repo is revived for this or whether the Flow Nexus subsumes it.
- Whether a top stratum per flow or per job is the unit (the "phase" term is withdrawn but the concept is not).

---

## G. The harness roster: kept, tested, packaged, abandoned, newly looked into

### Constraining entries

> yes, only codex and claude.

-- raw Vision, 2026-08-27, flow 01a0437d. `flows/01a0437d/vision/codexAndClaude.md`

> pi is slop

-- raw Vision (undated), flow 5a3ee4. `flows/5a3ee4/vision/pi.md`

> We should abandon the Pi harness also if we get into this, because I think it's falling out of favor now.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/piHarness.md`

> Why don't you look into the DeepSeek harness while you're out there? Apparently it's really good. Maybe we even want to package it in our environment and start testing out with ChatGPT because they do allow third-party harnesses

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/deepsekHarness.md`

> The defect is on openai for lacking the feature I want

-- raw Vision, 2026-09-02, flow cf0ed9. `flows/cf0ed9/vision/openaiLacksTheFeatureIWant.md`

> Let's see how pierce's system looks like in a specialized-harness system.

-- raw Vision, 2026-09-02, flow b9f4f6. `flows/b9f4f6/vision/topStratum.md`

### Forks

- Whether "only codex and claude" (2026-08-27) for the CriomOS package set is narrowed by the later DeepSeek interest (2026-09-04), or DeepSeek stays outside the core roster for now.
- Whether ChatGPT third-party harness support makes it a candidate for the per-harness-skill system or stays external.

---

## H. Harness packaging and installation

### Constraining entries

> all we need to do is get the codex derivation from the same place. declared once, used everywhere.

-- raw Vision, 2026-08-25, flow 01a038be. `flows/01a038be/vision/codexDerivation.md`

> we dont allow installing software statefully

-- raw Vision, 2026-08-25, flow 01a038be. `flows/01a038be/vision/installingSoftwareStatefully.md`

> we have to modify the Claude Desktop Nix code to force it to use our Claude code.

-- raw Vision, 2026-08-26, flow 01a03e02. `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md`

> Put durable packages and configuration in the declarative source that owns that environment.

-- deployed skill (distilled Vision level). `.claude/skills/agent-harness-packaging/SKILL.md`

> Do not run an upstream integration installer that mutates a configuration Nix owns; express the intended configuration in its declarative owner.

-- deployed skill (distilled Vision level). `.claude/skills/agent-harness-packaging/SKILL.md`

### Forks

- Whether desktop modification (Claude Desktop forced to use our Claude Code) is still pursued given the 2026-09-02 retraction of interest in "heavily modifying those applications."

---

## I. Transcript-landing practice as standard practice; whether it becomes a line in the main-flow skill

### Constraining entries

> If I approve them, you could set up some agent to just read your transcript and put these into files so we don't waste context for you to shuffle all this text around.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/skillLandingBySubflow.md`

> This, I believe, is something that I wanted to develop into standard practice.

-- raw Vision, 2026-09-04, flow 38dec9. `flows/38dec9/vision/skillLandingBySubflow.md`

> We need a subflow that is specialized in being able to see what was approved in the transcript and extracting that from the transcript directly into the file. The whole point is to save the main flow's context

-- transcript-only, 2026-09-03, transcript deca2323, L154.

> Instead of saying, "Reports, design documents, and landings are written by subflows," you could say "everything else also."

-- transcript-only, 2026-09-03, transcript deca2323, L154.

> I want to go with you on the topics that it touched on in its last message ... about how the main flow shouldn't really be editing almost any files.

-- transcript-only, 2026-09-03, transcript deca2323, L10.

> subflows dont write skills

-- raw Vision, 2026-08-23, flow a60a9e85. `flows/a60a9e85/vision/skillDesigning.md`

### Forks

- "subflows dont write skills" (a60a9e85) vs. the 38dec9 transcript-landing vision where a subflow reads the approved content from the transcript and lands it in files. The skill-process report notes these are distinct: a60a9e85 addresses subflows *authoring* skill content (a wording task), while 38dec9 addresses subflows *landing* already-approved content (a mechanical task). Whether the main-flow skill must make this distinction explicit is undecided.
- Whether the practice goes in the main-flow skill or the subflow skill or both.

### Oddities

The skill-process report flags: "the file turned out to be better" (for a prompt the living pastes from phone, flow db97561c) alongside "Don't your instructions tell you to not try and show me something through a file?" (flow b9f4f6). The report resolves this as non-conflicting (different artifact types), but a skill line would need to distinguish them.

---

## J. Rules any new or edited skill must obey

### Constraining entries

> I dont want to start with the "A flow does ..." style. Just "A claim must be relayed as a claim" - lets train for that style, in skill design

-- raw Vision, 2026-08-18, flow 358f143a. `flows/358f143a/vision/skillDesigning.md`

> we cannot put paths in skills. explain why

-- raw Vision, 2026-08-18, flow 358f143a. `flows/358f143a/vision/skillDesigning.md`

> thats not training. we need to train agents so they dont propose this kind of thing in skills.

-- raw Vision, 2026-08-18, flow 358f143a. `flows/358f143a/vision/skillDesigning.md`

> Re: Manner skill: I dont want bullet style lines in skills

-- raw Vision, 2026-08-18, flow 358f143a. `flows/358f143a/vision/skillDesigning.md`

> guards are a symptom of bad instructions. if we need a guard then we have failed our positive instructions.

-- raw Vision, 2026-09-02, flow b2da01. `flows/b2da01/vision/skillDesigning.md`

> context does this. Removal is better than addition, when the expected behavior is the desired behavior.

-- raw Vision, 2026-08-26, flow 4ddc321d. `flows/4ddc321d/vision/skillDesigning.md`

> $skill-designing of course requires my reviewing any skill edit proposal first.

-- raw Vision, 2026-08-22, flow 01a02a34. `flows/01a02a34/vision/skillDesigning.md`

> Just make sure that the first line you're proposing is actually gonna replace a line, because there's already a line like it. Just make sure you're not just adding and bloating the skill.

-- raw Vision, 2026-09-03, flow b9f4f6. `flows/b9f4f6/vision/skillDesign.md`

> redraft the software design skill without any negative that wasnt explicitely and confidently worded by psyche. it should be almost all positive guidance.

-- raw Vision, 2026-08-23, flow a60a9e85. `flows/a60a9e85/vision/skillDesigning.md`

> the only need is for an indication in the skill design skill to know about the template syntax, nothing more. the checker is quackery

-- raw Vision, 2026-08-22, flow 01a01bac. `flows/01a01bac/vision/skillDesigning.md`

> I dont see any .claude or .agent in the skills repo

-- raw Vision, 2026-08-10. `vision-raw/skillsRepoSourceOnly.md`

> get rid of the manifest and generate whatever skills are present.

-- raw Vision, 2026-08-21. `vision-raw/skillsRepository.md`. Supersedes any earlier manifest architecture.

> A distilled statement carries what the psyche said and nothing beyond it. A small ruling makes a small statement.

-- distilled Vision. `Vision/distillation.md`

### Forks

- Whether the "no paths in skills" rule covers all absolute and relative paths or only report/witness paths (the Curriculum template syntax references file names).
- Whether "removal is better than addition" becomes a skill-designing line or stays implicit.

---

## K. How the living wants a proposal presented for annotation

### Constraining entries

> I want to be able to put comments from my phone. Essentially, I'm remote accessing Codex, which is running on my machine here, and then Codex would create a visual report. There would be a link I could open on my phone where I could actually put in all the comments one by one.

-- raw Vision, flow 01a052b6. `flows/01a052b6/vision/reportFeedback.md`

> the main flow shouldn't really be editing almost any files ... we're wasting a shitload of tokens on writing the same thing in the file as we're writing in the response.

-- transcript-only, 2026-09-03, transcript deca2323, L10.

> I'm not able to read this ... The sub-agent that turns this Markdown into the actual web report should not use Mermaid. I think this is what happened here. It should make properly scaled SVG representations of it so that they're clearly readable and render correctly

-- raw Vision, flow 995a164e. `flows/995a164e/vision/designPractice.md`

> Do not spend Fable output on HTML: write markdown, let a subagent convert

-- raw Vision, flow 62022e8f. `flows/62022e8f/vision/designPractice.md`

> Then create a markdown+subflow web report I can annotate of the whole proposal.

-- transcript-only, 2026-09-04, flow 7b4d4ce2 starting prompt.

> Don't your instructions tell you to wait until all the sub flows have returned to do your presentation and questions? Don't they tell you to not try and show me something through a file?

-- raw Vision, 2026-09-03, flow b9f4f6. `flows/b9f4f6/vision/presentation.md`

> I want lots of visuals, and that would also be a part of the skill. I very much like visuals.

-- transcript-only, session 77cca2bc starting prompt.

### Forks

- Whether the presentation skill line goes in the main-flow skill or becomes its own skill.
- Whether "not through a file" (the living reads the response, not a file) conflicts with the markdown+subflow web report pattern (the main flow writes markdown, a subflow converts it, the living reads the web report).

---

## Distillation density table

Subjects with the most raw entries, for the main flow to choose a distillation proposal.

| Subject | Raw entries (approx.) | Distilled `Vision/<topic>.md` exists? |
|---|---|---|
| Context strata / gradients of authority | 74 (psyche attributions in context-strata report) | No |
| Harness seizure / base prompt / hijack repositories | 42 (across harnesses + context-strata reports, unique) | No |
| Skill wording / skill-designing rules | 38 (across skill-process report) | No |
| Main-flow context economy (reports, logging, subflow output, token costs) | 22 (across skill-process report) | No |
| Vocabulary: flow/agent/machine | 52 (path attributions in vocabulary report) | No (vocabulary skill serves as governing doc) |
| Harness packaging and installation | 12 (in harnesses report) | No |
| Distillation process | 11 (in skill-process report) | Yes: `Vision/distillation.md` |
| Flow Nexus / invocation system | 8 (in harnesses report) | Yes: `Vision/flowNexus.md` |

---

## Sources

### Acquisition reports (flow 7b4d4c)
- `/home/li/primary/flows/7b4d4c/reports/psyche-harnesses.md`
- `/home/li/primary/flows/7b4d4c/reports/psyche-context-strata.md`
- `/home/li/primary/flows/7b4d4c/reports/psyche-vocabulary.md`
- `/home/li/primary/flows/7b4d4c/reports/psyche-skill-process.md`

### Flow 38dec9 vision files
- `flows/38dec9/vision/agentToMachine.md`
- `flows/38dec9/vision/deepsekHarness.md`
- `flows/38dec9/vision/harnessVocabulary.md`
- `flows/38dec9/vision/invocationSystem.md`
- `flows/38dec9/vision/perHarnessSkills.md`
- `flows/38dec9/vision/piHarness.md`
- `flows/38dec9/vision/skillLandingBySubflow.md`
- `flows/38dec9/vision/systemPromptRepository.md`

### Distilled Vision
- `Vision/flowNexus.md`
- `Vision/distillation.md`

### Spirit
- `.claude/skills/spirit/SKILL.md`

### Deployed skills
- `.claude/skills/vocabulary/SKILL.md`
- `.claude/skills/agent-harness-packaging/SKILL.md`
