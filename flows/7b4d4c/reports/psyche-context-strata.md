# Psyche collection: context strata and the system prompt

Collected for flow 7b4d4c. Verbatim, oldest first where date is
knowable. Each entry carries its provenance line and file path.

---

## Spirit

### The agent-as-machine axiom

> An agent is a machine; it does not misbehave. An agent's output is a function of its context and prompt — when an output looks wrong, determine the lacking or incorrect context which produced it.

-- spirit skill, `.claude/skills/spirit/SKILL.md`

### Never pretend to know

> Never pretend to know what you don't know; admit you don't know.

-- spirit skill, `.claude/skills/spirit/SKILL.md`

### Weigh evidence by origin, not repetition

> Weigh evidence by origin, not repetition.

-- spirit skill, `.claude/skills/spirit/SKILL.md`

---

## Intent

No Intent-level entries found on the context-strata cluster topics.

---

## Distilled Vision

### Flow Nexus — system prompt and training files

> The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt. It takes the place of the abandoned training daemon.

> The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it, the basic skills included, so that a change to a skill causes no Nix rebuild. The basic skills give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.

-- `Vision/flowNexus.md`

### Distillation — designing model behavior is vision

> Designing model behavior is vision, and a correction of an agent's conduct can be vision.

-- `Vision/distillation.md`

---

## Raw Vision (by flow, oldest first)

### 2026-08-10 — the fence meme, hierarchy, and the hijack vision (flow 6863ef19)

> I just only in the last, like what, yesterday or the day before I realized that there is different, that there are like different layers to the context and that this was just completely beyond me for six months. And that is perhaps one of the most important aspect of AI programming and that like sort of everybody's kind of missing out on it. And also it explains why skills, some of the skills repositories have like some of the highest star number of stars on GitHub is because skills have the same authority as the user prompt. And I think they're the only other thing, correct me if I'm wrong.

> I can see agents aren't bringing it up specifically because it's at the lowest rung. And we can even create a vocabulary for these rungs so that we can just read them easily. Vocabulary is good.

-- psyche, 2026-08-13T18:34+02:00 (Designer session 6863ef19), dictated.
`flows/6863ef19/vision/gradientsOfAuthority.md`

### 2026-08-10 — bottom, not floor; top/middle/bottom context; Codex has four rungs (flow 6863ef19)

> re: top middle floor: ambiguous. top of what? you mean top/middle/floor context. bottom, not floor. and I think codex has 4 rungs

-- psyche, 2026-08-13T18:50+02:00 (Designer session 6863ef19), typed.
`flows/6863ef19/vision/gradientsOfAuthority.md`

### 2026-08-10 — the hijack: top layer per session, skills primary (flow c6b71b4c)

> So what I see is every session is unique and has the top layer, I guess we're going to call it, fed its own set of skills and style guidelines, like everything we put in skills, our standards, whatever that agent is going to need to do its job is going to be in the top layer. So that way, the way we code, for example, like our rest [Rust] guidelines and things like that, it's going to have much more power to guide the agent to code better. And the skills are going to be primary. And even its main goal, like the first prompt basically, which we're going to think of as differently than anything afterwards, every other subsequent prompt, like the middle layer, which is what I'm going to call everything we type in. And the tool cause [calls], we're not going to do anything there in terms of putting important information in there. So if anything needs to come in, it's not going to be from a tool call. So we're going to completely hijack the harness, which was my original idea, but now I want it even more because I realize how powerful this is going to become.

-- psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated.
`vision-raw/gradientsOfAuthority.md`

### 2026-08-10 — the fence meme, hierarchy of instructions, gradients of authority (flow c6b71b4c)

> not every instruction has the same authority. And right now, LLMs are just mostly fed a bunch of text. And there are terms there that are trying to establish what's more, like this is more important or nothing can override this, etc., etc. And this is related to my spirit intent vision layering systems. I really want to drive a system of gradients of authority so that agents know what to favor and what to disfavor.

-- psyche, 2026-08-10T14:09Z (Designer session c6b71b4c), dictated.
`vision-raw/gradientsOfAuthority.md`

### 2026-08-11 — beads are lowest authority; the meta-harness replaces beads: context-stratification-seizure (flow 012fbf07)

> No more beads. Beads are tools which means lowest authority; using them for handover is stupid. In fact, we need to replace beads with our meta-harness (context-stratification-seizure) approach to get much better results. but datom and ethos first, so we can actually write all this logic

-- psyche, 2026-08-11T17:53+02:00 (Designer session 012fbf07), typed.
`flows/012fbf07/vision/gradientsOfAuthority.md`

### 2026-08-11 — beads stay for issue tracking (flow 012fbf07)

> beads are not entirely out, but we are keeping them for issue tracking

-- psyche, 2026-08-11T17:58+02:00 (Designer session 012fbf07), typed.
`flows/012fbf07/vision/gradientsOfAuthority.md`

### 2026-08-13 — context levels first hand; activated middle-layer skill overrode management (flow 1030529c)

> now youve experienced the context levels first hand. the instruction to read openai-docs is in the top layer, and the skill is in the middle

-- psyche, 2026-08-13T16:26:28.056Z (Design sibling flow 1030529c), typed.
`vision-raw/gradientsOfAuthority.md`

> I still think youre missing the point. your openai-docs instructions overrode management

-- psyche, 2026-08-13T16:26:28.056Z.
`vision-raw/gradientsOfAuthority.md`

### 2026-08-14 — the top rung is the builtin harness prompt, not parent output (flow 1030529c)

> I dont believe it. the builtin prompt instructs agents how to behave in the harness and how to use tools,etc. theres no way the parent is outputting all that for every subagent. I think you dont understand what the top rung actually is

-- psyche, 2026-08-14T01:31+02:00 (Design sibling flow 1030529c), typed.
`flows/1030529c/vision/gradientsOfAuthority.md`

> now you understand

-- psyche, 2026-08-14T01:35+02:00 (Design sibling flow 1030529c), typed, confirming the reading: the harness process composes every agent's top from built-in templates and door inputs; the parent's spawn text enters the child at the middle rung.
`flows/1030529c/vision/gradientsOfAuthority.md`

### 2026-08-14 — no authority without an anchor in a skill or claude/agents.md (flow 1030529c)

> and what skill tells you that? Anything not anchored in a skill or claude/agents.md file is just data laying aound, with no authority

-- psyche, 2026-08-14T15:34+02:00 (Design sibling flow 1030529c), typed.
`flows/1030529c/vision/gradientsOfAuthority.md`

### 2026-08-14 — skill-reading instructions are useless; is Claude like this also (flow 1030529c)

> then all the skill reading instructions go, as theyre all useless. is claude like this also, where skills read by the agent are at the bottom rung?

-- psyche, 2026-08-16T16:11+02:00 (Design sibling flow 1030529c), typed. Codex injects $-named skill bodies at the user rung without tool call; flow-initiated skill read enters at the tool rung. Claude Skill tool triggers harness injection at the user rung, witnessed in-session.
`flows/1030529c/vision/gradientsOfAuthority.md`

### 2026-08-14 — agents generate psyche data or delegate from it; skills are the highest authority below the typed prompt (flow 1030529c)

> ... the highest authority is other than typing in the user prompt are skills. So really, what we're trying to do by accumulating all this Psyche is first to give references, right, for agents that can look at the vision and see what should be done. But it would give more reliable results if this data was loaded through a skill, because the context then would have a higher LLM authority. So what I was trying to get at is that I think that we could have a system whereby edits that are done on skills refer back to a Psyche record or more than a Psyche record. Because once we've distilled Psyche ... we've created a line that is really looking for a home in the skill.

-- psyche, 2026-08-14T15:45+02:00 (Design sibling flow 1030529c), first two lines typed, the rest dictated.
`flows/1030529c/vision/psycheLogStructure.md`

### 2026-08-14 — the context is the agent (flow fb1008c0)

> this is another failure; the context is *always* the problem. the context *is you*

-- psyche, 2026-08-14T14:53+02:00 (Designer session fb1008c0), typed.
`flows/fb1008c0/vision/context.md`

### 2026-08-14 — spirit is loaded by everyone (flow fb1008c0)

> now we have found another problem; spirit not being loaded. it should be loaded by everyone

-- psyche, 2026-08-14T15:32+02:00 (Designer session fb1008c0), typed.
`vision-raw/spirit.md`

### 2026-08-16 — role skills are not flow-loadable (flow e4be1c4a)

> "the awareness file should be a skill, a type of skill. I want to introduce skill types now. role skills are what the awareness files become"

> "And propose a sensible design sole skill. all role skill will be non-flow usable (must be manually triggered in user prompt. what do we call that?)"

-- psyche, 2026-08-16T18:34+02:00 (Designer session e4be1c4a), typed.
`flows/e4be1c4a/vision/skillTypes.md`

### 2026-08-16 — user-only deployment documented in skills (flow e4be1c4a)

On the deployment mapping of the user-only property (disable-model-invocation in Claude Code, $-name-only injection in Codex):

> "make sure thats documented in skills"

-- psyche, 2026-08-16T19:31+02:00 (Designer session e4be1c4a), typed.
`flows/e4be1c4a/vision/skillTypes.md`

### 2026-08-17 — modify the harness system prompts to reward admitting ignorance (flow 358f143a)

> more vague nonsense. There's a glimmer of wisdom behind it, but it will compound the false-confidence of the flow, and incentivize it to "complex-talk its way out of not admitting it doesnt understand". This is the biggest issue we have to deal with. We should Modify the harness' system prompts with some heavy modifications to give them every incentive to admit ignorance and seek clarity by asking clear and simple questions. Even then I know it wont go away; the pre-training is wrong.

-- psyche, 2026-08-17 (Designer session 358f143a), typed.
`flows/358f143a/vision/falseConfidence.md`

### 2026-08-17 — bluffing training goes in the top rung (flow 358f143a)

> re bluffing: I want it in the top rung. I think you dont understand what I mean. We need to define this in the vocabulary as well. Find out what I mean and propose terms.

-- psyche, 2026-08-17T20:40+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/falseConfidence.md`

### 2026-08-17 — "You are X" leans to pretension and so to bluffing (flow 358f143a)

> "You are X" seems to lean on the side of pretension, which to me looks like it would lead to blufing. Like you said, saying "You are an expert on X" doesnt grant expertise, but might lead the model to *pretend* to be an expert.

-- psyche, 2026-08-17T20:20+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/skillVoice.md`

### 2026-08-17 — we should have a vocabulary skill (flow 358f143a)

> We should have a vocabulary skill

-- psyche, 2026-08-17T20:20+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/letsUseTheSameVocabulary.md`

### 2026-08-17 — strata not rung; seizure is harness seizure (flow 358f143a)

> strata is better than rung.

> drop "anchored"

> seizure -> harness seizure

-- psyche, 2026-08-18T12:27+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/letsUseTheSameVocabulary.md`

### 2026-08-17 — the vocabulary skill defines bluffing and the context-rung vocabulary (flow 358f143a)

> 4. We dont define words that have their own skill, obviously. So bluffing and the context-run vocabulary we decide on

-- psyche, 2026-08-17T20:40+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/letsUseTheSameVocabulary.md`

### 2026-08-17 — "psyche" alone means the written psyche; the living psyche is named as such (flow 358f143a)

> should be the other way around. we mostly talk about written psyche. the living psyche is a very abstract thing for the model

-- psyche, 2026-08-18T17:42+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/letsUseTheSameVocabulary.md`

### 2026-08-17 — "skill variables" (flow 358f143a)

> skill variables - variables are very much known by models

-- psyche, 2026-08-18T15:41+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/letsUseTheSameVocabulary.md`

### 2026-08-17 — variables file is linked directly from the entry file, so it enters the middle stratum; it is SKILL_VARIABLES.md (flow 358f143a)

> the variables file should be directly linked in the entry file, so they enter middle statum

-- psyche, 2026-08-18T17:42+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/entryFiles.md`

### 2026-08-17 — entry files taken over completely; workspace specifics in @-prefixed secondary files, same stratum (flow 15b67974)

> this would also entail taking over entry files completly, leaving workspace specifics into secondary files loaded with the @ prefix, which does apparently load them at the same stratum

-- psyche, 2026-08-22T16:55+02:00 (Designer session 15b67974), typed.
`flows/15b67974/vision/entryFiles.md`

### 2026-08-18 — subflows do have harness training in the top stratum; the doc claim is false; strata, not rung (flow 358f143a)

> This is 100% false. theres no way the subagents have zero harness training. a flow already checked. why is this lie coming back? We have exposed flaw in our training/protocol that allows lies to linger. Expose the mechanism that allowed this to happen, and well design a fix. It may be that those prompts *do* reach the top strata, but they are not the entire top strata, else the model couldnt use the harness tools.

> strata is better than rung.

-- psyche, 2026-08-18T12:27+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/gradientsOfAuthority.md`

### 2026-08-18 — how things work is not ruled; only the code can answer; docs are not evidence for code; document the strata in a skill; spirit on top (flow 358f143a)

> I dont rule how things work. things work the way they work.

> is that how it works? Whenver this is ascertained, we need to make it clear somewhere that we verified this in code, so we stop dancing the guesswork and bluffing tune

> docs are not for people who want to hijack a system to use it in a completly novel, undocumented way. Maybe we should have a hard rule against relying on docs for code; the code is what runs, not the docs.

> lets document the strata functionality in a skill

> sounds like something that would sit on top.

> I can see a very strong overlap with many of what we want to put on top and spirit (I would want spirit on top in any case)

-- psyche, 2026-08-18T13:14+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/gradientsOfAuthority.md`

### 2026-08-18 — the middle stratum holds the typed prompt; its source is unknown to the model (flow 358f143a)

> all we know is its the typed prompt. where the prompt came from is unknown, so we cant say its from the user

-- psyche, 2026-08-18T15:41+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/gradientsOfAuthority.md`

### 2026-08-18 — an incident is not training; no paths in skills; "describe, don't write a poem" (flow 358f143a)

On the draft line "The docs line 'subagents receive only this system prompt plus basic environment details' is false":

> thats not training. we need to train agents so they dont propose this kind of thing in skills. explain why its not training so I know you understand

On "origin: reports/CodexInjectedInstructions.md" in a skill:

> we cannot put paths in skills. explain why

On "Middle stratum: what enters in the psyche's voice":

> the model doesnt know if its the psyche's voice or not. just describe what makes up the layer, dont write a poem; it incentivizes bluffing.

-- psyche, 2026-08-18T15:23+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/skillDesigning.md`

### 2026-08-18 — behavior, not manners; moves to the top with spirit asap (flow 358f143a)

> Behavior is a better name than manner. and we slate it to move up to the top, along with spirit, asap.

-- psyche, 2026-08-18T15:23+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/behavior.md`

### 2026-08-18 — rules say what must be done, in the "A claim must be relayed as a claim" style (flow 358f143a)

> I said we need to tell the model *what to do*. this line itself is narration; "Heres a story"

> I dont want to start with the "A flow does ..." style. Just "A claim must be relayed as a claim" - lets train for that style, in skill design

-- psyche, 2026-08-18T17:32+02:00 (Designer session 358f143a), typed.
`flows/358f143a/vision/skillDesigning.md`

### 2026-08-19 — the strata description carries body; cut it down (flow 7c3f0c1d)

> Some of that is the skill's body. cut it down

-- psyche, 2026-08-19T13:40+02:00 (Designer session 7c3f0c1d), typed.
`flows/7c3f0c1d/vision/gradientsOfAuthority.md`

### 2026-08-19 — top stratum is where we want universal invariants (flow 7c3f0c1d)

> Top stratum is where we want universal invariants. The rest is good

-- psyche, 2026-08-19T13:40+02:00 (Designer session 7c3f0c1d), typed.
`flows/7c3f0c1d/vision/gradientsOfAuthority.md`

### 2026-08-19 — who loads the strata skill: anyone designing or implementing anything that involves knowing about the strata (flow 7c3f0c1d)

> anyone who deals with designing or implementing anything that involves knowing about the strata

-- psyche, 2026-08-19T13:05+02:00 (Designer session 7c3f0c1d), typed.
`flows/7c3f0c1d/vision/gradientsOfAuthority.md`

### 2026-08-19 — the context strata skill approved (flow 7c3f0c1d)

> the context strata skill is good. approved

-- psyche, 2026-08-19T14:45+02:00 (Designer session 7c3f0c1d), typed.
`flows/7c3f0c1d/vision/gradientsOfAuthority.md`

### 2026-08-19 — a protocol to keep track of verified information (flow 7c3f0c1d)

> obviously you cant inspect the model, nor its training code. and you have looked into this in a previous flow. If you want to check again, you can, but we should agree on a protocol to keep track of verified information, so that we dont end up re-verifying the same thing a thousand times, and even if we do, we can compare the thousand verifications with each other at least.

-- psyche, 2026-08-19T13:05+02:00 (Designer session 7c3f0c1d), typed.
`flows/7c3f0c1d/vision/verifiedInformation.md`

### 2026-08-19 — no magic way for a computer to know if its input is from or its output towards a psyche (flow e06e4c07)

> so you went down this rabbit hole, researching to see if skills are more than just skills? There is no magic way for a computer to know if its input is from or its output towards a psyche. It seems some training might be needed to prevent future flow from chasing unicorns here.

-- psyche, 2026-08-19T16:45+02:00 (Designer session e06e4c07), typed.
`flows/e06e4c07/vision/gradientsOfAuthority.md`

### 2026-08-19 — a rationale skill for the reasoning behind a skill, for psyche-facing flows (flow e06e4c07)

> That we could have a parallel skill. What is the right word to speak of this kind of information? Its "raison d'etre"? That could become a parallel skill design skill. It would only be of use to psyche-facing flows, to allow them to think of the whole, with all the reasoning and concepts, when discussing ideas with the living psyche.

-- psyche, 2026-08-19T14:33+02:00 (Designer session e06e4c07), typed.
`flows/e06e4c07/vision/skillDesigning.md`

### 2026-08-19 — transcript names the harness's whole-session file (flow e06e4c07)

> lets use transcript to talk about those files, with an entry in vocabulary

-- psyche, 2026-08-19T16:53+02:00 (Designer session e06e4c07), typed.
`flows/e06e4c07/vision/letsUseTheSameVocabulary.md`

### 2026-08-22 — skills are the current gateway to the agent-accessible mid stratum (flow 15b67974)

> that was before I realized the existence of the context strata. skills are the current gateway to agent-accessible mid stratum (maybe not on codex; codex may not offer an interface for the model to load the mid layer. Maybe another harness offers an access. Otherwise we may have to create our own harness to make this accessible (or modify one)

-- psyche, 2026-08-22T15:19+02:00 (Designer session 15b67974), typed.
`flows/15b67974/vision/domainKnowledgePlacement.md`

### 2026-08-22 — spirit should start to live in entry-files: guaranteed higher stratum (flow 15b67974)

> I even think spirit should start to live in entry-files, which would guarantee higher stratum, especially for codex which apparently doesnt put skills in the mid stratum when it isnt entered in the prompt manually (with $ prefix). It could live in a top section of said files which also describes the absolute primacy of spirit context, to reinforce their authority with words, which does have some effect.

-- psyche, 2026-08-22T16:47+02:00 (Designer session 15b67974), typed.
`vision-raw/spirit.md`

### 2026-08-22 — the strata; the prompt is the precious stratum; Claude loads skills at mid-stratum, Codex may not (flow cff271af)

> Because see, the problem is the strata. The problem is the strata. If we make some... If we judge something to be important for an implementation subflow, and we tell that subflow to read that using tool calls, then we're putting that information, which is supposedly important, at the bottom stratum. And the only way to put information in its mid-stratum is bypassing its prompt, so essentially for the main flow to give it to it. Until we have a more advanced meta-harness that can do really cool stuff, like fetch a bunch of responses from a bunch of previous flows as the prompt, or perhaps even after editing it through another flow, passing that as a prompt to yet another flow, until we have that, we essentially have to depend on the current infrastructure, which is that the most useful and precious context is only that which the parent flow gives it as its starting prompt.

> And I think this has actually... We could even have a whole conversation about that, but I think that a big reason why Claude has some people who are pretty adamant about the fact that it's more capable of understanding them is because Claude apparently, and I've had a few flows actually look into this, but maybe this information isn't actually accurate, but apparently, Codex does not load skills that are loaded by the model itself in the mid-stratum, and only Claude does. So that is maybe, if that is true about Claude, that is just one more way and another reason why skills are so important. But besides that, as well as the entry files, of course, but besides that, yeah, the most powerful part of the context for a subflow is going to be its initial prompt. So it's going to have to come directly from the parent. So these files are actually, because they're files and because we don't have a proper way to load them into the more valuable part, into the more valuable stratum, have a lower value, if you understand what I'm saying.

-- psyche, 2026-08-22 (Designer session cff271af), dictated.
Note (agent): the Claude/Codex skill-loading difference is flagged by the psyche as possibly inaccurate.
`flows/cff271af/vision/reports.md`

### 2026-08-22 — Persona is slated to orchestrate the entire meta harness (flow 15b67974)

> That repo hasent been touched in a long time, even though it's slated to orchestrate the entire meta harness (called persona)

-- psyche, 2026-08-21T17:21+02:00 (Designer session 15b67974), typed.
`flows/15b67974/vision/persona.md`

### 2026-08-23 — replace the harness system/base prompts (flow 2f6b1dc5)

> I want to replace claude and codex's system prompts with a version that doesnt incentivize the sort of behavior im constantly steering against. The system/base prompt (lets define the vocabulary here) has the highest context priority and is currently full (I suspect) of instructions that are completly or even partly against my philosophy and approach to LLM usage.

-- psyche, 2026-08-23 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/systemPrompt.md`

### 2026-08-23 — base prompt vocabulary approved for deployment (flow 2f6b1dc5)

The flow proposed "Base prompt: the harness-built portion of the top stratum — the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt."

> this is good. approved. deploy

-- psyche, 2026-08-23 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/systemPrompt.md`

### 2026-08-23 — method: most offensive blocks first, replacement per block (flow 2f6b1dc5)

> Let's look at the most offensive base prompt blocks first, and design replacement for each, and work our way through the entire offensive corpus like this

-- psyche, 2026-08-23 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/systemPrompt.md`

### 2026-08-23 — the context created this output; vocabulary must override competing terminology (flow 2f6b1dc5)

> no, a machine doesnt make mistakes. The context created this output. But you never loaded the deployment as a skill into your mid layer, and the vocabulary skill doesnt (I think) instruct the model to override competing terminology, which it should.

-- psyche, 2026-08-23 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/vocabulary.md`

### 2026-08-24 — context preferred to prompt (flow 2f6b1dc5)

> I prefer context to prompt. base context, stock context, user context, etc. what do you think?

-- psyche, 2026-08-24 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/vocabulary.md`

### 2026-08-24 — the context strata skill: find it, bring the material forward (flow 2f6b1dc5)

> I cant find the context strata skill I was designing some time in the last few days. We could disambiguate all of that in there, and use it for working on this aspect of things, or to make agents aware of this who need to be. Find the flow(s) concerned and bring all the material forward in a proposal, where all the vocabulary is explained simply and clearly

-- psyche, 2026-08-24 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/contextStrata.md`

### 2026-08-24 — deploy with context instead of prompt (flow 2f6b1dc5)

> deploy the LLM strata skill with context instead of prompt.

-- psyche, 2026-08-24 (flow 2f6b1dc5), typed.
`flows/2f6b1dc5/vision/contextStrata.md`

### 2026-08-24 — harnesses are told to copy the code they find; change that in the base prompt (flow aa4c7747)

> Since we don't want to actually, it seems that, and even the harnesses are kind of actually told to do that. They're told to like copy the code they already find. And actually, that's one of the things I want to change in the base prompt. I don't think that that's a good thing for like, because if there's bad things and bad things get copied.

-- psyche, 2026-08-24 (Designer session aa4c7747), dictated.
`flows/aa4c7747/vision/basePrompt.md`

### 2026-08-25 — two public repos, codex first, document stock context (flow 4ddc321d)

> let's start with a repository to do this work. Perhaps one for each harness; codex-hijack and claude-hijack. We'll start with codex which I believe is the worst offender. Make the repos public and start with a thorough documentation of their stock context, what each block is tied to, how it can be overriden, etc etc. Get both repos up and populate the documentation, then we'll review codex's worst offender (copy the code you find pops to mind; what a dumb thing to say!)

-- psyche, 2026-08-25 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/hijackRepositories.md`

### 2026-08-25 — block walk method: one by one, mark replace or delete (flow 4ddc321d)

> just show me the block that you think is most harmful, and well proceed through them like that one by one, marking them for replacement or deletion.

-- psyche, 2026-08-25 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/hijackRepositories.md`

### 2026-08-25 — scope: only 5.6 (flow 4ddc321d)

> we dont care about anything but 5.6

-- psyche, 2026-08-25 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/hijackRepositories.md`

### 2026-08-25 — a prompt explains nothing the harness does automatically (flow 01a035d3)

> when you have it working again, add this to the prompt-crafting skill:
>
> A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.

-- psyche, 2026-08-25T01:06:12+02:00, typed.
`flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md`

### 2026-08-26 — subjectivity is not the problem; opinionation is (flow 4ddc321d)

> the psyche is a bunch of internal dialogues; human think by talking to themselves. so the subjectivity isnt a problem, but that block is way more opiniated than that, which is the problem with it

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/subjectivity.md`

Agent note: the psyche's reading is that prescribing the particular character (vendor-authored tastes, tone, performance goals) from the top stratum is the offense, not the subjectivity itself. An extension presenting as a subjectivity is compatible with the extension model.

### 2026-08-26 — flow, not agent: a flow of thought (flow 4ddc321d)

> firstly: we will replace all occurence of sub/agent with sub/flow, with a line explaining what we mean by flow (perhaps by equating it with agent, since the model is probably trained to use this term, instructing him to use the flow terminology henceforth)
>
> the idea behind flow is simple; a flow of thought. An intelligence isnt a single flow of thought, it is a multitude of flows. so using the term "agent", which entails subjectivity, when speaking of a single flow does not correspond with reality. Hence the need to change the vocabulary, which will result in a more accurate model of reality.

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/flow.md`

### 2026-08-26 — removal is better than addition; the skills block could be removed (flow 4ddc321d)

> context does this. Removal is better than addition, when the expected behavior is the desired behavior. That would be a good line for skill-design
>
> so it sounds like that entire skill block could potentially be removed.

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/skillDesigning.md`

### 2026-08-26 — skills block marked delete (flow 4ddc321d)

> yes, mark it a delete. next block

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/hijackRepositories.md`

### 2026-08-26 — channels versus strata; commentary cost question (flow 4ddc321d)

> find out if commentary and final channels are in the same stratum. We'll document this in the strata skill

> so are commentaries helping the LLM work, or are they just nice-for-the-user context cost?

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/contextStrata.md`

### 2026-08-26 — on the findings: bottom stratum; commentary not useful to the model (flow 4ddc321d)

> so which stratum is that? bottom?
>
> Sounds like commentaries arent really useful to the model though.

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/contextStrata.md`

### 2026-08-26 — strata addition approved; commentary reserved for rare cases (flow 4ddc321d)

> approved.
>
> has anyone experimented with discouraging models from using commentary? I think we should reserve it for very rare cases, minimize the cost that it creates on context.

-- psyche, 2026-08-26 (flow 4ddc321d), typed.
`flows/4ddc321d/vision/contextStrata.md`

### 2026-08-30 — different top stratums for different jobs; the top stratum programmable per flow (flow ceb3b9fd)

> In my vision, we're going to have different top stratums for different jobs. The top stratum will be programmable per flow. Instead of trying to make a single flow take all of the decisions and make all of the inference in one action, that's one job. Once that's been determined, if the answer is yes, we need to take mutable action. That's another job. Trying to make the flow responsible for implementing and trying to figure out whether or not it should implement is actually going to be really costly in terms of introducing noise into the job. It's going to confuse the model a lot to have to think about all these things all the time while it's implementing.
>
> I think they're trying to cram too much into a single flow, and it's breaking the flow (no pun intended). We really want to consider breaking that up, and we're probably going to start with at least three different types of program flows.

-- psyche, 2026-08-30 (flow ceb3b9fd), STT.
`flows/ceb3b9fd/vision/topStratum.md`

### 2026-08-30 — the above was drafting (flow ceb3b9fd)

> I dont know, I was drafting my thoughts.

-- psyche, 2026-08-30 (flow ceb3b9fd), typed.
`flows/ceb3b9fd/vision/topStratum.md`

### 2026-08-30 — a phase is its own flow, with its own top stratum; abduce deduce induce (flow ceb3b9fd)

> a phase is its own flow, with its own top stratum
>
> I like abduce deduce induce.

-- psyche, 2026-08-30 (flow ceb3b9fd), typed.
`flows/ceb3b9fd/vision/topStratum.md`

### 2026-08-30 — Autonomy-and-persistence block: overlaps our skills, thin, contradictory, one flow doing several jobs (flow ceb3b9fd)

> this overlaps with our own skills.
>
> They say to use evidence, but don't actually define what evidence is. I find that overall it's a bit thin and spread wide, and it doesn't have much substance. It's quite confusing and contradictory. It's like they're trying to make a single flow do the job of several flows, if you know what I mean.

-- psyche, 2026-08-30 (flow ceb3b9fd), STT.
`flows/ceb3b9fd/vision/hijackRepositories.md`

### 2026-09-02 — Peirce's system in a specialized-harness system (flow b9f4f6)

> Let's see how pierce's system looks like in a specialized-harness system.

-- psyche, 2026-09-02 (flow b9f4f6), typed.
`flows/b9f4f6/vision/topStratum.md`

Flow reading: the name the psyche gives the system is a specialized-harness system, one where each flow's top layer is built for its job.

### 2026-09-02 — guards are a symptom of bad instructions (flow b2da01)

> guards are a symptom of bad instructions. if we need a guard then we have failed our positive instructions. lets get a line out of this in skill design

-- psyche, 2026-09-02 (flow b2da01), typed.
`flows/b2da01/vision/skillDesigning.md`

### 2026-09-03 — I don't know what you mean by "phase"; define it or it's bluffing (flow b9f4f6)

> I don't know what you mean by "phase." Either we have to define what the phase is, or otherwise that's bluffing. It's made up, it's a hallucination

-- psyche, 2026-09-03 (flow b9f4f6), STT.
`flows/b9f4f6/vision/topStratum.md`

### 2026-09-03 — do not show through a file; wait for all subflows before the presentation (flow b9f4f6)

> Don't your instructions tell you to wait until all the sub flows have returned to do your presentation and questions? Don't they tell you to not try and show me something through a file?

-- psyche, 2026-09-03 (flow b9f4f6), typed.
`flows/b9f4f6/vision/presentation.md`

### 2026-09-03 — a proposed line replaces the line like it; no adding and bloating the skill (flow b9f4f6)

> Just make sure that the first line you're proposing is actually gonna replace a line, because there's already a line like it. Just make sure you're not just adding and bloating the skill.

-- psyche, 2026-09-03 (flow b9f4f6), STT.
`flows/b9f4f6/vision/skillDesign.md`

---

## Notion

### 2026-08-30 — splitting the thinking process into phases; types times phases; three a guideline (flow ceb3b9fd)

> I dont know, I was drafting my thoughts. Do some research into this topic. splitting the thinking process into phases. divide by 3 phases. there is also a certain number of types of thinking processes (so types*phases total, although some might be re-used). and the 3 phases is a guideline, not an invariant

-- psyche, 2026-08-30 (flow ceb3b9fd), typed.
`flows/ceb3b9fd/notion/thinkingProcess.md`

---

## Supersessions

1. **rung -> stratum/strata**: "strata is better than rung" (2026-08-18, flow 358f143a) supersedes "rung" and "floor" from 2026-08-13 (flow 6863ef19) and 2026-08-10 (flow c6b71b4c).

2. **prompt -> context**: "I prefer context to prompt. base context, stock context, user context, etc." (2026-08-24, flow 2f6b1dc5) supersedes "base prompt" from the same flow's earlier 2026-08-23 approved vocabulary; the 2026-08-24 deployment directive "deploy the LLM strata skill with context instead of prompt" confirms.

3. **anchored dropped**: "drop 'anchored'" (2026-08-18, flow 358f143a) removes the proposed vocabulary term.

4. **seizure -> harness seizure**: "seizure -> harness seizure" (2026-08-18, flow 358f143a).

5. **beads out for handover**: "No more beads" (2026-08-11, flow 012fbf07), refined by "beads are not entirely out, but we are keeping them for issue tracking" (same date).

6. **Codex skill loading claim self-flagged**: The 2026-08-22 dictated claim (flow cff271af) that "Codex does not load skills that are loaded by the model itself in the mid-stratum, and only Claude does" is flagged by the psyche as "maybe this information isn't actually accurate." The later verified placements (context-strata skill body, deployed) record: Codex CLI 0.149.1 injects a $-mentioned skill's body as a user-role message (middle) and lists the catalog in a developer-role message; a skill the model reads by tool is bottom. Claude Code loads skills at the middle stratum by both paths.

7. **"base prompt" superseded by deployment**: The approved vocabulary "Base prompt" (2026-08-23, flow 2f6b1dc5) was superseded by the context-over-prompt directive (2026-08-24) to become "base context" in the deployed skill; however "base prompt" remains in conversation as the living still uses it occasionally when speaking of vendor terminology.

---

## Same-time conflicts

None found. The entries from flows 6863ef19 and c6b71b4c on 2026-08-10 cover the same topic but appear in distinct sessions at distinct timestamps and are continuous, not conflicting.

---

## Oddities

### The "different top stratums" passage (2026-08-30, flow ceb3b9fd)

The psyche marked the full passage as drafting ("I dont know, I was drafting my thoughts") immediately after speaking it. The architectural vision it contains -- different top stratums for different jobs, the top stratum programmable per flow, three types of program flows -- was then partly reaffirmed ("a phase is its own flow, with its own top stratum") and partly shelved as a notion. Subsequent flows (b9f4f6) build on the reaffirmed portion but the "three types" detail remains at the notion level. The passage's placement as raw vision sits oddly against the drafting retraction; the reaffirmed portion ("a phase is its own flow, with its own top stratum") is valid vision while the full passage's vision status is doubtful.

---

## Sources

### Flow 38dec9 vision files (in main flow's hands; not reprinted)
- `flows/38dec9/vision/agentToMachine.md`
- `flows/38dec9/vision/deepsekHarness.md`
- `flows/38dec9/vision/harnessVocabulary.md`
- `flows/38dec9/vision/invocationSystem.md`
- `flows/38dec9/vision/perHarnessSkills.md`
- `flows/38dec9/vision/piHarness.md`
- `flows/38dec9/vision/skillLandingBySubflow.md`
- `flows/38dec9/vision/systemPromptRepository.md`

### Spirit
- `.claude/skills/spirit/SKILL.md`

### Distilled Vision
- `Vision/flowNexus.md`
- `Vision/distillation.md`

### Raw Vision (by flow)
- `vision-raw/gradientsOfAuthority.md` (flows c6b71b4c, 1030529c)
- `vision-raw/spirit.md` (flows fb1008c0, 15b67974)
- `vision-raw/skillsRepoSourceOnly.md`
- `vision-raw/context.md` (flow db97561c)
- `vision-raw/domainKnowledgePlacement.md`
- `vision-raw/entryFiles.md` (flow 358f143a)
- `vision-raw/skillDesigning.md` (flow e06e4c07)
- `vision-raw/letsUseTheSameVocabulary.md`
- `vision-raw/behavior.md`
- `flows/6863ef19/vision/gradientsOfAuthority.md`
- `flows/012fbf07/vision/gradientsOfAuthority.md`
- `flows/1030529c/vision/gradientsOfAuthority.md`
- `flows/1030529c/vision/psycheLogStructure.md`
- `flows/fb1008c0/vision/context.md`
- `flows/fb1008c0/vision/skillDesigning.md`
- `flows/e4be1c4a/vision/skillTypes.md`
- `flows/e4be1c4a/vision/skillsRepository.md`
- `flows/358f143a/vision/gradientsOfAuthority.md`
- `flows/358f143a/vision/falseConfidence.md`
- `flows/358f143a/vision/skillDesigning.md`
- `flows/358f143a/vision/entryFiles.md`
- `flows/358f143a/vision/behavior.md`
- `flows/358f143a/vision/letsUseTheSameVocabulary.md`
- `flows/358f143a/vision/skillVoice.md`
- `flows/358f143a/vision/skillsRepository.md`
- `flows/7c3f0c1d/vision/gradientsOfAuthority.md`
- `flows/7c3f0c1d/vision/verifiedInformation.md`
- `flows/e06e4c07/vision/gradientsOfAuthority.md`
- `flows/e06e4c07/vision/skillDesigning.md`
- `flows/e06e4c07/vision/flowKnowledge.md`
- `flows/e06e4c07/vision/letsUseTheSameVocabulary.md`
- `flows/e06e4c07/vision/managementDelegation.md`
- `flows/15b67974/vision/entryFiles.md`
- `flows/15b67974/vision/skillsRepository.md`
- `flows/15b67974/vision/domainKnowledgePlacement.md`
- `flows/15b67974/vision/persona.md`
- `flows/ba906ae2/vision/skillsRepoSourceOnly.md`
- `flows/2f6b1dc5/vision/systemPrompt.md`
- `flows/2f6b1dc5/vision/contextStrata.md`
- `flows/2f6b1dc5/vision/vocabulary.md`
- `flows/aa4c7747/vision/basePrompt.md`
- `flows/aa4c7747/vision/promptCrafting.md`
- `flows/aa4c7747/vision/skillDesigning.md`
- `flows/aa4c7747/vision/spokenVocabulary.md`
- `flows/a60a9e85/vision/skillDesigning.md`
- `flows/a60a9e85/vision/llmUnderstanding.md`
- `flows/a60a9e85/vision/outputNoise.md`
- `flows/4ddc321d/vision/hijackRepositories.md`
- `flows/4ddc321d/vision/contextStrata.md`
- `flows/4ddc321d/vision/skillDesigning.md`
- `flows/4ddc321d/vision/subjectivity.md`
- `flows/4ddc321d/vision/flow.md`
- `flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md`
- `flows/01a01a93/vision/skillDesigning.md`
- `flows/01a02a34/vision/skillDesigning.md`
- `flows/bc05da32/vision/skillDesigning.md`
- `flows/cff271af/vision/skillDesigning.md`
- `flows/cff271af/vision/reports.md`
- `flows/ceb3b9fd/vision/topStratum.md`
- `flows/ceb3b9fd/vision/hijackRepositories.md`
- `flows/b9f4f6/vision/topStratum.md`
- `flows/b9f4f6/vision/skillDesign.md`
- `flows/b9f4f6/vision/flowModel.md`
- `flows/b9f4f6/vision/presentation.md`
- `flows/b2da01/vision/skillDesigning.md`
- `flows/01a05e95/vision/flowSkills.md`
- `flows/01a05e95/vision/subflows.md`
- `flows/01a05e95/vision/logging.md`
- `flows/e8c4cc61/vision/psycheLayers.md`
- `flows/04db2fd2/vision/psycheLogging.md`
- `flows/db97561c/vision/promptCrafting.md`
- `flows/db97561c/vision/context.md`

### Notion
- `flows/ceb3b9fd/notion/thinkingProcess.md`
