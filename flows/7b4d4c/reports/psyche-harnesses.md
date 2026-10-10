# Psyche collection: Harnesses

Cluster: the thinking-machine harnesses, their packaging, per-harness skills, wrapper executables, and universal removals.

---

## Spirit

No spirit entry addresses harnesses directly. The spirit skill's relevant lines are structural:

> The purpose of AI is to extend a psyche.

> Backward compatibility is never a design variable. Do not preserve an older shape for compatibility's sake; if the current system is not designed to do what we want, it is replaced -- every consumer updated -- never extended with a parallel compatibility path.

> An agent is a machine; it does not misbehave. An agent's output is a function of its context and prompt -- when an output looks wrong, determine the lacking or incorrect context which produced it.

Path: `.claude/skills/spirit/SKILL.md`

---

## Intent

No intent entry addresses harnesses directly. The closest is:

> `Intent/mandatoryTraits.md`

(Not harness-specific; not reproduced.)

---

## Distilled Vision

### Flow Nexus

> The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt. It takes the place of the abandoned training daemon.

> The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it, the basic skills included, so that a change to a skill causes no Nix rebuild. The basic skills give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.

Path: `Vision/flowNexus.md`

---

## Raw Vision (legacy vision-raw/)

Entries below are from `vision-raw/`, the undistilled corpus predating the flow system. Oldest first.

### 2026-08-06 — the textual form exists for editors, harnesses, and models

> So we agreed that there would be a different type for every kind of ethos object, even all the way down to ethos mirroring the types that are needed to contain the particular nomos types, for now anyway. So that's, you know, the serialized RKYV payload of that filled data type is the body. The encoded form is the code. So the encoded form of ethos is ethos. The textual form is there so that our editors, our current editors, and our current LLM harnesses and models can actually make sense of it. Does that answer the question?

-- psyche, 2026-08-06T21:53:42Z (Designer session 5abf3be8)

Path: `vision-raw/encodedFormIsTheCode.md`

### 2026-08-10 — the fence meme, instruction hierarchy, gradients of authority, search compulsion

> so you would need instructions for detecting faulty awareness files.
>
> There is a much bigger pattern here, and we can't really get that deep into it, but there was a good meme. It was an image of a guy painting a fence, and he had only painted halfway down the third picket of the fence. And then he handed the paint to an AI, and the AI painted the same pattern. And every time he got into the same number of picket, he would only paint that one halfway. So copying patterns is not always a good idea. And that's also why I prefer Opus 4.6 to Opus 5, because Opus 4.6 is much more likely to recognize that he doesn't know something. Yeah, I don't know. Has anybody looked at this problem and how to prevent AIs from just mindlessly repeating patterns? I guess you need some kind of way for them to judge whether or not the pattern is good. And I would like my agents to sort of do this almost universally. So if we need guidelines everywhere, we have to be careful that this doesn't become its own hell. We already have guidelines. Like you said, there was already a guideline in the awareness skill. So I think what we need is like a hard constraint, like something that's emphasized. You know, this is where the concept of the hierarchy of instructions. Like not every instruction has the same authority. And right now, LLMs are just mostly fed a bunch of text. And there are terms there that are trying to establish what's more, like this is more important or nothing can override this, etc., etc. And this is related to my spirit intent vision layering systems. I really want to drive a system of gradients of authority so that agents know what to favor and what to disfavor. Like in this case, it would have been to favor the instructions in the awareness skill over the patterns that are already found in the awareness file. So we need like, there's several angles here to look at. And maybe you want to send some research agents. I've been having a hard time. Also, this is another thing. Lately, my managing sessions seem to want to do web searches themselves, especially codecs [Codex], which is why I had to put an explicit line forbidding them to do web searches. But you can maybe also give me your opinion on what you think this is about.

-- psyche, 2026-08-10T14:09Z (Designer session c6b71b4c), dictated

Path: `vision-raw/gradientsOfAuthority.md`

### 2026-08-10 — the hijack: top layer per session, skills primary, built-in sub-agent disabled

> So what I see is every session is unique and has the top layer, I guess we're going to call it, fed its own set of skills and style guidelines, like everything we put in skills, our standards, whatever that agent is going to need to do its job is going to be in the top layer. So that way, the way we code, for example, like our rest [Rust] guidelines and things like that, it's going to have much more power to guide the agent to code better. And the skills are going to be primary. And even its main goal, like the first prompt basically, which we're going to think of as differently than anything afterwards, every other subsequent prompt, like the middle layer, which is what I'm going to call everything we type in. And the tool cause [calls], we're not going to do anything there in terms of putting important information in there. So if anything needs to come in, it's not going to be from a tool call. So we're going to completely hijack the harness, which was my original idea, but now I want it even more because I realize how powerful this is going to become. Of course, there's going to be a lot more sessions and the built in sub-agent tool is going to be disabled because then I'm sure the sub-agent kind of inherits the top layer of its parent, whatever harness. So we're going to have to have this tool that allows an agent to create sub-agents, quote unquote, which is not so much create sub-agent, then communicate with the meta harness that something needs to be done. I guess there won't be such or yeah, there could still be a hierarchy of agent, but it's not necessarily going to be every call cause an agent below that agent. It might just it might be an agent that has a similar sort of spot in the hierarchy of agents.

-- psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated

Path: `vision-raw/gradientsOfAuthority.md`

### 2026-08-10 — sessions are flows; the meta agent is composed of flows

> And I even want to use a different term than agents because it's misleading, because what I'm making this meta agent, if you will, is made up of all these smaller sessions. So we were just going to call it, I guess, a session or even then it sort of implies that there's an individual there, but it's more like a flow or a sub flow. ... But I think the terminology is really important, not just for me, but for the ... sub flows. To instinctively understand the concepts because they're named properly.

-- psyche, 2026-08-10T18:49Z (Designer session c6b71b4c), dictated; ellipses mark trims

Path: `vision-raw/flowsNotAgents.md`

### 2026-08-11 — training injected in the harness system prompt, higher authority

> yes, thats the concept. soon the training will be injected in the harness system prompt, which has higher authority in the LLM context

-- psyche, 2026-08-11, steward session

Path: `vision-raw/trainingRepo.md`

### 2026-08-11 — until we design the meta-harness (persona) properly

> yes, until we design the meta-harness (persona) properly and all the data is passed along the right agent call, like magic (you are logging psyche right?)

-- psyche, 2026-08-11T20:18:14.611+02:00 (Realizer session 019ff178)

Path: `vision-raw/gradientsOfAuthority.md`

### 2026-08-13 — more Design flows, not more aspect names; what is a flow-with-a-harness; awareness authority in context

> These are pretty good, but I want to run something by you because I think that what I'm doing here is basically just reaching out for more names because I want to actually run more agents, more agent windows, more flows, more sessions. ... What would you call it when there's a harness, a terminal, and there's a starting prompt, a starting skill, and then once the context is getting too big, some files are edited, and then these files are sort of reused to start a new one, a new context from scratch. What I wanted to run by you is that the problem isn't really that I need more terms so much that I need to maybe... Because to me, in my mind, I'm designing. I don't need to reach for all these terms. I feel like it's just going to make things complicated, so maybe we don't do all of this. Because it just feels like I'm trying to create... I don't have a meta harness, so really they're just names to differentiate my sessions for now. But I really just need more than one design window. ...
>
> And so there's this internal dialogue that needs to happen between a bunch of different LLM flows to create the whole, which is the artificial being. And we basically need to keep the awareness files pure enough so that the agents don't start writing down, like taking notes on what they're working on specifically. Not that there's anything wrong with bringing understanding into the awareness. It's like broad understanding. But there's a few problems, one of which is that the awareness file is read as an ordinary file, which means that it has the lowest context priority. That's a problem. So the highest context priority, which we currently have access to before I start to actually launch custom harnesses with their own system prompts, is the middle layer. So I think that the awareness content should live, at least for now, in the skill. But it can't be an agent visible skill because then, you know, like all of this stuff is going to, well, geez, you can see it. I'm having a bunch of competing thoughts here because I understand what I want, but I can't just get there instantly. And that's why I kind of want to talk to a lot of designers right now.

-- psyche, 2026-08-13T15:51:58.913Z (session 019ffbd3), dictated

Path: `vision-raw/flowsNotAgents.md`

### 2026-08-13 — shards dont have authority; the meta harness is required for specialization

> 1. shards dont have authority. the name is mostly for recognizing different agents for now; the meta harness is required for shards to become more specialized. the association with steward is because I usually have agents work in pair (one claude one codex). Im not sure where to put this explanation.

-- psyche, 2026-08-13T16:08:20+02:00

Path: `vision-raw/attunement.md`

### 2026-08-13 — context levels first hand; openai-docs instruction overrode management

> now youve experienced the context levels first hand. the instruction to read openai-docs is in the top layer, and the skill is in the middle

-- psyche, 2026-08-13T16:26:28.056Z

> I still think youre missing the point. your openai-docs instructions overrode management

-- psyche, 2026-08-13T16:26:28.056Z

Path: `vision-raw/gradientsOfAuthority.md`

### 2026-08-13 — the overwhelm problem is why I want the meta-harness

> And I'd also like to better train the agents on being able to discern intent from vision. And there's so many things I'm going to do all at once, and I'm trying to be reasonable here, because if I overwhelm all the agents with all of my ideas at once, it's just going to be a mess, and that's been kind of my main problem, which is why I want to do this meta-harness.

-- psyche, 2026-08-13, Designer session 6863ef19, dictated

Path: `vision-raw/trainingRepo.md`

### 2026-08-17 — variables in their own setup-specific file; Codex-only material rides a codex conditional

> theyre not variables if they dont have a name, but that is rougly the idea

> right now its doing too much. variables should go in its own (AGENT_VARIABLES.md?) file, which is setup specific and therefore not in curriculum, but is documented in curriculum's agents.md file, so agents are made aware that those variables should be set and how.

-- psyche, 2026-08-17T19:01+02:00 (Design session 358f143a), typed

Path: `vision-raw/entryFiles.md`

### 2026-08-22 — spirit should start to live in entry-files; especially for Codex which doesn't put skills in the mid stratum

> I even think spirit should start to live in entry-files, which would guarantee higher stratum, especially for codex which apparently doesnt put skills in the mid stratum when it isnt entered in the prompt manually (with $ prefix). It could live in a top section of said files which also describes the absolute primacy of spirit context, to reinforce their authority with words, which does have some effect.

-- psyche, 2026-08-22T16:47+02:00 (Design session 15b67974), typed

Path: `vision-raw/spirit.md`

---

## Raw Vision (per-flow)

Entries are from `flows/<id>/vision/` files. Organized oldest first within each subject.

### Harnesses: experience, kept/abandoned

#### 2026-08-08 — agents communicating is desperately needed

> And you're going to we're also going to have to set up intercom, which has also been a thing that I've been really wanting so that agents can communicate directly because it's ridiculous right now that they can't. It's absolutely fucking crazy, ridiculous.

-- psyche, 2026-08-08T11:37:36.634Z (session 019fe121), dictated

Path: `flows/019fe121/vision/agentIntercom.md`

#### 2026-08-09 — Agent Intercom wrapped all executables and broke them; use different executable names

> There's two stacks here that you're talking about. One is the Agent Intercom, which is not from me and supposedly works. And then there's the other stack, which is Messenger and Orchestrator, which are not ready to be used yet, which is from me. But I want a solution that sort of works for us now, and Agent Intercom looks promising for us to get inter-agent communication sooner. And it was deployed, and there was a problem because all of the regular Codex CLI and Cloud CLI were wrapped with its logic, and it was defective, so I couldn't use my Agents anymore. So I had to roll that back. So I think we should redeploy it, but use different executable names. That way we can still use the normal Codex and normal Cloud, and then I can test the one that is wrapped with the Agent Intercom. So we're not going to be touching the Messenger and Orchestrator of our stack.

-- psyche, 2026-08-09T20:18:11.025Z (session 019fe728), dictated

Path: `flows/019fe728/vision/agentIntercom.md`

This is the earliest appearance of the "different executable names" / wrapper pattern.

#### 2026-08-16 — skill types introduced; role skills are not flow-loadable; deployment mapping per harness

> the awareness file should be a skill, a type of skill. I want to introduce skill types now. role skills are what the awareness files become

> And propose a sensible design sole skill. all role skill will be non-flow usable (must be manually triggered in user prompt. what do we call that?)

On the deployment mapping of the user-only property (disable-model-invocation in Claude Code, $-name-only injection in Codex):

> make sure thats documented in skills

-- psyche, 2026-08-16T18:34+02:00 and 2026-08-16T19:31+02:00 (Design session e4be1c4a), typed

Path: `flows/e4be1c4a/vision/skillTypes.md`

#### 2026-08-17 — modify the harness system prompts to reward admitting ignorance

> more vague nonsense. There's a glimmer of wisdom behind it, but it will compound the false-confidence of the flow, and incentivize it to "complex-talk its way out of not admitting it doesnt understand". This is the biggest issue we have to deal with. We should Modify the harness' system prompts with some heavy modifications to give them every incentive to admit ignorance and seek clarity by asking clear and simple questions. Even then I know it wont go away; the pre-training is wrong.

-- psyche, 2026-08-17 (Design session 358f143a), typed

Path: `flows/358f143a/vision/falseConfidence.md`

#### 2026-08-17 — role skills hold the awareness seat for now; the persona meta-harness will move this fast

> skills for now. It might evolve differently later. This will move quite fast as we build the persona meta-harness

-- psyche, 2026-08-17T19:01+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/workspace20.md`

#### 2026-08-17 — training is the right name; the harness system prompt has higher authority; Curriculum renamed to training

> I also think curriculum is the wrong name. I was warned against using training because of the clash with LLM training, but its LLM training that has the wrong term; what they call model training is model genesis, or creation, and post training is model modification. Training is what context does to the model. So we should call it training, and well change the industry's language around model creation when we get involved at that layer, after we raise billions of dollars from people tired of flawed, incorrectly generated models.

-- psyche, 2026-08-17T19:20+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/skillsRepository.md`

#### 2026-08-17 — the subagent problem is codex only

> the subagent problem is codex only, and @ references arent loaded recursively, apparently.

-- psyche, 2026-08-17 (Design session 358f143a), typed

Path: `flows/358f143a/vision/entryFiles.md`

#### 2026-08-17 — Athena is deployment specific; the successor is a Rust daemon

> We also have another problem; Athena is deployment specific. Curriculum should become a proper rust component (a daemon) which is configured for such variables, which it can keep in its database so regeneration can be done with a very terse datom interface.

-- psyche, 2026-08-17T19:20+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/trainingRepo.md`

**Superseded** by 2026-08-18 entry: "the new daemon I want to make isnt training anymore (abandonned). Its flow"

#### 2026-08-18 — behavior moves to the top with spirit asap

> Behavior is a better name than manner. and we slate it to move up to the top, along with spirit, asap.

Context (agent-authored): the skill is `behavior`; it and `spirit` are to move to the top stratum (the harness system prompt) as soon as possible.

-- psyche, 2026-08-18T15:23+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/behavior.md`

#### 2026-08-18 — subflows do have harness training in the top stratum; expose the mechanism that let the lie linger

> This is 100% false. theres no way the subagents have zero harness training. a flow already checked. why is this lie coming back? We have exposed flaw in our training/protocol that allows lies to linger. Expose the mechanism that allowed this to happen, and well design a fix. It may be that those prompts *do* reach the top strata, but they are not the entire top strata, else the model couldnt use the harness tools.

> strata is better than rung.

-- psyche, 2026-08-18T12:27+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/gradientsOfAuthority.md`

#### 2026-08-18 — how things work is not ruled; only the code can answer; docs are not evidence for code; spirit on top

> I dont rule how things work. things work the way they work. "What you had ruled" -> I still dont understand what you mean. So do subagents not get the builtin system prompt from the harness? Only the code can answer.

> is that how it works? Whenver this is ascertained, we need to make it clear somewhere that we verified this in code, so we stop dancing the guesswork and bluffing tune

> docs are not for people who want to hijack a system to use it in a completly novel, undocumented way. Maybe we should have a hard rule against relying on docs for code; the code is what runs, not the docs.

> lets document the strata functionality in a skill

> sounds like something that would sit on top.

> I can see a very strong overlap with many of what we want to put on top and spirit (I would want spirit on top in any case)

-- psyche, 2026-08-18T13:14+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/gradientsOfAuthority.md`

#### 2026-08-18 — the middle stratum holds the typed prompt; its source is unknown to the model

> all we know is its the typed prompt. where the prompt came from is unknown, so we cant say its from the user

-- psyche, 2026-08-18T15:41+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/gradientsOfAuthority.md`

#### 2026-08-18 — "seizure" is "harness seizure"

> seizure -> harness seizure

-- psyche, 2026-08-18T12:27+02:00 (Design session 358f143a), typed

Path: `flows/358f143a/vision/letsUseTheSameVocabulary.md`

#### 2026-08-19 — "transcript" names the harness's whole-session file

> lets use transcript to talk about those files, with an entry in vocabulary

Context: after the Designer reported the harness session files (Claude Code `~/.claude/projects/<cwd>/<uuid>.jsonl`, Codex rollouts, Pi sessions)

-- psyche, 2026-08-19T16:53+02:00 (Design session e06e4c07), typed

Path: `flows/e06e4c07/vision/letsUseTheSameVocabulary.md`

#### 2026-08-19 — the context-strata skill description is bad; LLM should appear in the skill; the skill is rarely ever needed

> the description is bad. and LLM should appear in the skill, possibly in the description, which should also indicate that this skill is rarely ever needed

-- psyche, 2026-08-19T12:19+02:00 (Design session 7c3f0c1d), typed

Path: `vision-raw/gradientsOfAuthority.md`

### Harness packaging and installation

#### 2026-08-14 — shared parent workspace per aspect; CLAUDE.md and agents.md loaded recursively

> And this is even making the point even more for each flow having its own workspace, and therefore its own, well, or maybe actually flows that share the same aspect, like the design aspect, should have, I think, a shared parent workspace, and then they can live in a sort of sub workspace inside that shared workspace. And if I understand correctly, the way cloud works anyway, and you can see if codex is similar, because codex uses agents.md and cloud uses cloud.md, is that they will recursively load any parent cloud.md files. ... I even want the sub agents to have a different, we'll call it view or even the system prompt, right?

-- psyche, 2026-08-14T00:27+02:00 (Design sibling flow 1030529c), dictated

Path: `flows/1030529c/vision/workspace20.md`

#### 2026-08-21 — persona untouched for a long time, yet slated to orchestrate the entire meta harness

> That repo hasent been touched in a long time, even though it's slated to orchestrate the entire meta harness (called persona)

-- psyche, 2026-08-21T17:21+02:00 (Design session 15b67974), typed

Path: `flows/15b67974/vision/persona.md`

#### 2026-08-21 — flow launches an existing harness for now; our own custom harness later, 100% typed datom messages

> yes for now. we will create our own custom harness in the future, which will be 100% typed datom messages going in and being expected out.

-- psyche, 2026-08-21T17:21+02:00 (Design session 15b67974), typed

Path: `flows/15b67974/vision/flowDaemon.md`

#### 2026-08-22 — progression: meta-harness, syntax, and skill changes proceed incrementally

> So we have to take one bite at a time here.

Context: The schema, meta-harness, data-evolution, syntax, and skill changes proceed incrementally rather than as one coupled realization.

-- psyche, 2026-08-22T17:32:33.328Z, typed (Codex session 01a02a34)

Path: `flows/01a02a34/vision/progression.md`

#### 2026-08-23 — replace the harness system/base prompts

> I want to replace claude and codex's system prompts with a version that doesnt incentivize the sort of behavior im constantly steering against. The system/base prompt (lets define the vocabulary here) has the highest context priority and is currently full (I suspect) of instructions that are completly or even partly against my philosophy and approach to LLM usage.

-- psyche, 2026-08-23 (flow 2f6b1dc5), STT

Path: `flows/2f6b1dc5/vision/systemPrompt.md`

#### 2026-08-23 — base prompt vocabulary approved

> this is good. approved. deploy

Context: the flow proposed "Base prompt: the harness-built portion of the top stratum -- the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt."

-- psyche, 2026-08-23 (flow 2f6b1dc5)

Path: `flows/2f6b1dc5/vision/systemPrompt.md`

#### 2026-08-23 — method: most offensive blocks first, replacement per block

> Let's look at the most offensive base prompt blocks first, and design replacement for each, and work our way through the entire offensive corpus like this

-- psyche, 2026-08-23 (flow 2f6b1dc5)

Path: `flows/2f6b1dc5/vision/systemPrompt.md`

#### 2026-08-23 — an orca repo is smarter than cramming more stuff in the home repo

> I think an orca repo is smarter than cramming more stuff in the home repo

-- psyche, 2026-08-23T18:15:03+02:00

Path: `flows/01a02f23/vision/orca.md`

#### 2026-08-24 — the context strata skill: find it, bring the material forward

> I cant find the context strata skill I was designing some time in the last few days. We could disambiguate all of that in there, and use it for working on this aspect of things, or to make agents aware of this who need to be. Find the flow(s) concerned and bring all the material forward in a proposal, where all the vocabulary is explained simply and clearly

-- psyche, 2026-08-24 (flow 2f6b1dc5)

Path: `flows/2f6b1dc5/vision/contextStrata.md`

#### 2026-08-24 — deploy the LLM strata skill with context instead of prompt

> deploy the LLM strata skill with context instead of prompt.

-- psyche, 2026-08-24 (flow 2f6b1dc5)

Path: `flows/2f6b1dc5/vision/contextStrata.md`

#### 2026-08-24 — harnesses are told to copy the code they find; change that in the base prompt

> Since we don't want to actually, it seems that, and even the harnesses are kind of actually told to do that. They're told to like copy the code they already find. And actually, that's one of the things I want to change in the base prompt. I don't think that that's a good thing for like, because if there's bad things and bad things get copied.

-- psyche, 2026-08-24 (flow aa4c7747), STT

Path: `flows/aa4c7747/vision/basePrompt.md`

#### 2026-08-24 — must use subagents for all research, including openai

> remember that you must use subagents for all research, including openai.

-- psyche, 2026-08-24T01:08:51+02:00 (flow 01a030df)

Path: `flows/01a030df/vision/subagents.md`

### Harness hijack repositories

#### 2026-08-25 — two public repos, codex first, document stock context

> let's start with a repository to do this work. Perhaps one for each harness; codex-hijack and claude-hijack. We'll start with codex which I believe is the worst offender. Make the repos public and start with a thorough documentation of their stock context, what each block is tied to, how it can be overriden, etc etc. Get both repos up and populate the documentation, then we'll review codex's worst offender (copy the code you find pops to mind; what a dumb thing to say!)

-- psyche, 2026-08-25 (flow 4ddc321d)

Path: `flows/4ddc321d/vision/hijackRepositories.md`

#### 2026-08-25 — block walk method: one by one, mark replace or delete

> just show me the block that you think is most harmful, and well proceed through them like that one by one, marking them for replacement or deletion.

-- psyche, 2026-08-25 (flow 4ddc321d)

Path: `flows/4ddc321d/vision/hijackRepositories.md`

#### 2026-08-25 — scope: only 5.6

> we dont care about anything but 5.6

-- psyche, 2026-08-25 (flow 4ddc321d)

Path: `flows/4ddc321d/vision/hijackRepositories.md`

#### 2026-08-25 — a prompt explains nothing the harness does automatically

> when you have it working again, add this to the prompt-crafting skill:
>
> A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.

-- psyche, 2026-08-25T01:06:12+02:00 (flow 01a035d3)

Path: `flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md`

#### 2026-08-25 — we dont allow installing software statefully

> which shouldnt even show up: we dont allow installing software statefully

-- psyche, 2026-08-25T17:54:08+02:00 (flow 01a038be)

Path: `flows/01a038be/vision/installingSoftwareStatefully.md`

#### 2026-08-25 — all we need is the codex derivation from the same place

> all we need to do is get the codex derivation from the same place. declared once, used everywhere. youre overcomplicating this to the extreme

-- psyche, 2026-08-25T14:22:12+02:00 (flow 01a038be)

Path: `flows/01a038be/vision/codexDerivation.md`

#### 2026-08-25 — medium graphical nodes should have codex and claude desktop

> I would like medium graphical nodes to have codex and claude desktop apps installed.

-- psyche, 2026-08-25T00:38:33+02:00 (flow 01a0338f)

Path: `flows/01a0338f/vision/mediumGraphicalNodes.md`

#### 2026-08-25 — don't explain what the harness does automatically (prompt crafting)

> dont explain things that the harness does automatically; agents.md is builtin to the harness. dont explain what everybody knows

-- psyche, 2026-08-25 (flow aa4c7747)

Path: `flows/aa4c7747/vision/promptCrafting.md`

#### 2026-08-26 — implement ChatGPT Wayland override as approved

> Remember 01a038be and implement its last suggestion as approved.

Context: override the deployed ChatGPT package with `commandLineArgs = "--ozone-platform=wayland"`.

-- psyche, 2026-08-26T13:19:36.237Z (flow 01a03e39)

Path: `flows/01a03e39/vision/lastSuggestion.md`

#### 2026-08-26 — force Claude Desktop to use our Claude Code

> Okay, so this shows two things. One, the Claude Desktop is trying to use an obsolete version of Claude code, which means the Claude Desktop might be outdated. And yeah, we cannot allow the desktop to try to use something that it's installing statefully. So we have to modify the Claude Desktop Nix code to force it to use our Claude code.

-- psyche, 2026-08-26T14:54:23+02:00 (flow 01a03e02), STT

Path: `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md`

#### 2026-08-26 — remote control all the codex TUI sessions I create

> Find out if there is a way for me to allow me to remote control all the codex tui sessions I create. Right now, it doesnt allow me to connext to sessions that have an "active writer", but I am able to do it with claude code, by enabling remote control in that session, then my remote messages just appear in the terminal session. I would like to do the same with codex

-- psyche, 2026-08-26T20:19:21+02:00 (flow 01a03f49)

Path: `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md`

#### 2026-08-26 — commentary versus strata; the commentary cost question

> find out if commentary and final channels are in the same stratum. We'll document this in the strata skill

> so are commentaries helping the LLM work, or are they just nice-for-the-user context cost?

> so which stratum is that? bottom?

> Sounds like commentaries arent really useful to the model though.

> has anyone experimented with discouraging models from using commentary? I think we should reserve it for very rare cases, minimize the cost that it creates on context.

-- psyche, 2026-08-26 (flow 4ddc321d), typed

Path: `flows/4ddc321d/vision/contextStrata.md`

#### 2026-08-26 — Codex stock context skills block marked delete

> this is definitely a removal.

(on "Do not carry skills across turns unless re-mentioned.")

> yes, mark it a delete. next block

-- psyche, 2026-08-26 (flow 4ddc321d)

Path: `flows/4ddc321d/vision/hijackRepositories.md`

#### 2026-08-27 — only codex and claude

> yes, only codex and claude.

Context: Asked whether the CriomOS-owned package collection should cover only Codex and Claude or replace `llm-agents` generally.

> great. approved.

Context: CriomOS-home was proposed as owner of the canonical Codex and Claude engine packages and the derived ChatGPT and Claude Desktop packages.

-- psyche, 2026-08-27 (flow 01a0437d)

Path: `flows/01a0437d/vision/codexAndClaude.md`

#### 2026-08-27 — Codex-only skill for web reporting procedure

> Check a recent codex session for the web reporting procedure which we'll put in a codex only skill

-- psyche, 2026-08-27T10:16:44.427Z (Codex session 01a0428b)

Path: `flows/01a0428b/vision/codexOnlySkill.md`

#### 2026-08-27 — Claude remote control: session 01a03f49 has the right design

> session 01a03f49 has the right design for how we want to do this on codex side. try to aim for the same design with claude (see if its possible)

-- psyche, typed (flow 01a04524)

Path: `flows/01a04524/vision/claudeRemoteControl.md`

#### 2026-08-28 — one server for everything, both Claude and Codex; rooted in primary; not a nexus

> Keep working on the one server for everything solutions, both for Claude and codex

> Yes, the code server should be rooted in primary.

> I dont want to start a nexus for this; we just need the server running for codex and claude, and the desktop apps using it locally.

-- psyche, typed (flow 01a047d2)

Path: `flows/01a047d2/vision/remoteControl.md`

#### 2026-08-28 — AgentIntercom follows Claude and Codex presence; different executables, not a gate

> We don't need to gate agent intercom, it should be on any node that has Claude/codex

> we were gating agent-intercom before because it would modify codex and claude, but now I only want different executables (different names) to be wrapped with the agent-intercom wrapped codex and claude, so we dont need a gate at all. so differentiate what is gated by this now totally inappropriate flag, which must be removed, so we can gate what needs to be gated with the right variables

-- psyche, typed (flow 01a048a6)

Path: `flows/01a048a6/vision/agentIntercomGraphical.md`

This refines the 2026-08-09 wrapper-executable ruling: the wrapper pattern is now the standing approach, the old gating flag removed.

#### 2026-08-28 — full access permission for Bird's ChatGPT Desktop

> her chatgpt desktop app doesnt start a new codex session with "full access" permission, as I want it to be

-- psyche, typed (flow 01a05d17)

Path: `flows/01a05d17/vision/fullAccessPermission.md`

#### 2026-08-30 — Working-with-the-user block marked replace

> mark as replace, at least in parts.

-- psyche, typed (flow ceb3b9fd)

Path: `flows/ceb3b9fd/vision/hijackRepositories.md`

#### 2026-08-30 — Autonomy-and-persistence block: overlaps our skills, thin, contradictory

> this overlaps with our own skills.
>
> They say to use evidence, but don't actually define what evidence is. I find that overall it's a bit thin and spread wide, and it doesn't have much substance. It's quite confusing and contradictory. It's like they're trying to make a single flow do the job of several flows, if you know what I mean.
> ...
> I think they're trying to cram too much into a single flow, and it's breaking the flow (no pun intended).

-- psyche, STT (flow ceb3b9fd)

Path: `flows/ceb3b9fd/vision/hijackRepositories.md`

#### 2026-08-30 — different top stratums for different jobs; the top stratum programmable per flow

> In my vision, we're going to have different top stratums for different jobs. The top stratum will be programmable per flow. Instead of trying to make a single flow take all of the decisions and make all of the inference in one action, that's one job. Once that's been determined, if the answer is yes, we need to take mutable action. That's another job. Trying to make the flow responsible for implementing and trying to figure out whether or not it should implement is actually going to be really costly in terms of introducing noise into the job. It's going to confuse the model a lot to have to think about all these things all the time while it's implementing.
>
> I think they're trying to cram too much into a single flow, and it's breaking the flow (no pun intended). We really want to consider breaking that up, and we're probably going to start with at least three different types of program flows.

-- psyche, STT (flow ceb3b9fd)

Path: `flows/ceb3b9fd/vision/topStratum.md`

The refinement that followed was marked by the psyche as drafting: "I dont know, I was drafting my thoughts."

#### 2026-08-30 — a phase is its own flow, with its own top stratum

> a phase is its own flow, with its own top stratum

-- psyche, typed (flow ceb3b9fd)

Path: `flows/ceb3b9fd/vision/topStratum.md`

**Note**: The subsequent flow b9f4f6 found this term "phase" problematic:

> I don't know what you mean by "phase." Either we have to define what the phase is, or otherwise that's bluffing. It's made up, it's a hallucination

-- psyche, STT (flow b9f4f6, 2026-09-03)

Path: `flows/b9f4f6/vision/topStratum.md`

#### 2026-08-31 — flow ID: cut out the 01a0 prefix from Codex sessions; one simple tool per harness

> And it looks like all the codex sessions start with 01a0 - so far anyway, so we should mandate the ID to cut out that prefix. see if you can detect a pattern in claude IDs as well, or if the ID patterns are documented either for codex or claude. I want to use the most random earliest part of the ID.

> we should also make a small tool that lets a flow get its ID easily if it doesnt automatically get it from the harness, as codex seems to always run a convoluted shell script to get its ID from an env var, which also returns the whole ID which is wasting a lot of context in the end.

> If there is a part in the ID which is actually random, wherever it is, we can use that, and we could maybe design this: just a small, simple tool in Python or whatever, whatever is easier for the thinking machine, most natural for it. Maybe one for Claude, one for Codex, that checks the ID and sees if the directory already exists.

-- psyche, 2026-08-31 (flow 01a05826), typed

Path: `flows/01a05826/vision/flowIdentity.md`

### Pi harness

#### Pi is slop

> pi is slop

-- psyche, typed (flow 5a3ee4)

Decision: mark Pi as deprecated, phase it out. pi-models.nix deprecated.

Path: `flows/5a3ee4/vision/pi.md`

(Date not recorded in the vision file. The flow short-id `5a3ee4` is a Claude Code session.)

### OpenAI / ChatGPT

#### 2026-09-02 — the defect is on openai for lacking the feature I want

> The defect is on openai for lacking the feature I want

-- psyche, typed (flow cf0ed9)

Path: `flows/cf0ed9/vision/openaiLacksTheFeatureIWant.md`

### Desktop integration

#### 2026-09-02 — no longer interested in heavily modifying desktop applications

> I am no longer interested in heavily modifying those applications to achieve better functionality.

Context: inventory the local implementations and hacks used to connect the desktop application to the persistent Codex server so their removal can be considered.

-- psyche, typed (flow ea1e56)

Path: `flows/ea1e56/vision/desktopCodexIntegration.md`

### Thinking machine terminology

#### "thinking machine should be used specifically"

> in a sentence like this, thinking machine should be used specifically instead of the shortened machine, as the context makes it ambiguous.

-- psyche, typed (flow 01a05487)

Path: `flows/01a05487/vision/thinkingMachine.md`

### Specialized-harness system

#### 2026-09-02 — Peirce's system in a specialized-harness system

> Let's see how pierce's system looks like in a specialized-harness system.

Flow reading: the name the psyche gives the system -- a specialized-harness system, one where each flow's top layer is built for its job.

-- psyche, typed (flow b9f4f6)

Path: `flows/b9f4f6/vision/topStratum.md`

### Witness reuse across flows

#### The key problem: every session lacks access to what's been done before

> We need to design some kind of witness indexing by topic, a natural language approach.

> I'm not literally meaning caching in the way it's been traditionally used in software. I'm more using caching in a thinking machine kind of way, whereby a cheap thinking machine model would compare.

> The key problem: every session doesn't have good access to what's already been done before.

-- psyche, STT (flow 78c93c)

Path: `flows/78c93c/vision/witness-reuse.md`

### Machine-generated content

> Whenever something is machine-generated, whether I say so explicitly or maybe we could even ask the machine to guess that something was machine-generated, that something was pasted in. In other words, that another machine, another thinking machine, had generated that. This none of the content in it should be logged as psyche.

-- psyche, typed (flow 78c93c)

Path: `flows/78c93c/vision/machine-generated-content.md`

---

## Notion

### Rolling Codex services

> Maybe we can define two services:
> 1. One pointing to the old executable so that it doesn't restart
> 2. The updated one
>
> We could use this to sort of roll through. I don't know, it's just a thought. You can see what you think about that.

> Is it possible to run multiple servers on the same host? Like you say, just leave the old sessions connected to the former server. On my phone, I can have multiple remotes or multiple servers that I connect to, so I would just add the new one as yet another server. ... we probably will get to a point where there's always going to be a flow going, so we can never actually wait for the motive to finish. ... create this continual new remote server kind of situation where I would have an ever-growing number of servers on my remote clients. Is there a clean way to actually do this?

-- psyche, typed (flow 01a05487)

Path: `flows/01a05487/notion/rollingCodexServices.md`

### Psyche layers: the bottom layer is Notion

> Brainstorm (maybe, not sure yet - lets make that part of a skill so the word brainstorm is recognized as a key for something: maybe a lower layer in psyche: Thought? Idea? Possibility? Give me more options on this. We would thus have 4 layers of psyche, and the following is on the bottom layer. Interesting aside: chatgpt apparently has 4 strata of context)

-- psyche, typed (flow e8c4cc61)

Path: `flows/e8c4cc61/vision/psycheLayers.md`

(The "chatgpt apparently has 4 strata of context" remark is a passing observation, not a ruling.)

---

## Transcript-only

Content from the living's typed or dictated words in transcripts that was not captured in any vision or notion file.

### 38dec9, line 135 — the system prompt flag exists; witness reuse; "jump into the sea" pushback

> no, *you* can see it. I cant. We should make that clear in one of the skills

> I believe what you're saying is not really what you're saying. I think what you're trying to say is that we haven't actually implemented a use of this flag, which does exist, right? There is a system front flag, I've been told. Hopefully, we can also figure out a better way for Flows to reuse already performed witnesses, so that something like this, which has been ascertained (we know that it has been tested that the system prompt flag does override the system prompt), we don't want other flows to be confused about that and have to constantly check.

> Well, if that were true, then we should all just jump into the sea and give up on life forever, because it would mean that nothing could ever change. I am not in the gloom-and-doom camp, and I hope that I can train you to leave that kind of mentality in the future.

-- psyche, STT; transcript: `/home/li/.claude/projects/-home-li-primary/38dec9a9-71a6-4d33-a85d-b98879027b41.jsonl`, line 135

The first sentence ("*you* can see it, I cant") addresses the fact that the model sees the top stratum but the living does not; a skill should make this explicit. The "system front flag" is a dictation artifact for "system prompt flag". The pushback against "the injected system prompt cannot be removed" is a philosophical position: nothing is permanent, gloom-and-doom mentality is to be trained away.

### 38dec9, line 169 — the central per-harness-skill proposal (transcript-only fragments)

The following fragments from the same message are NOT in the 38dec9 vision files:

> I wouldn't modify the harness all the time and everywhere, because I also wouldn't modify it the same way all the time.

> I believe maybe the repository, and we're not going to go into this, but we can just talk about how we want to do this. One of the repositories, either harness or Flow, or maybe both of them are involved somehow, is going to actually create the system call with the right flag to invoke the harness with the right system prompt or the right top stratum.

(The second fragment IS captured in `flows/38dec9/vision/invocationSystem.md`.)

> Why don't you look into the DeepSeek harness while you're out there? Apparently it's really good. Maybe we even want to package it in our environment and start testing out with ChatGPT because they do allow third-party harnesses, and we can start documenting that one as well.

(This IS captured in `flows/38dec9/vision/deepsekHarness.md`.)

> We should abandon the Pi harness also if we get into this, because I think it's falling out of favor now. It's pretty sloppy. I've had a really hard time with it when I was using it. It was just a catastrophe, actually.

(This IS captured in `flows/38dec9/vision/piHarness.md`.)

The genuinely transcript-only fragment is:

> I wouldn't modify the harness all the time and everywhere, because I also wouldn't modify it the same way all the time.

This states the principle behind per-harness skills: the modification varies by harness and by purpose, so no single universal modification suffices.

-- psyche, STT; transcript: `/home/li/.claude/projects/-home-li-primary/38dec9a9-71a6-4d33-a85d-b98879027b41.jsonl`, line 169

### 38dec9, line 246 — system prompt repository; a separate repository for modified versions

> So, to your first question, where does the new system prompt live? We've made this repository. Maybe there's more than one where we were reviewing the system prompt and deciding what to do with them, so we would, I think, have a flake there. We should just create a separate repository that anyone could use to give modified versions with different names of Claude and Codex, with different takes on system prompts.

(The repository sentence IS captured in `flows/38dec9/vision/systemPromptRepository.md`. The "maybe there's more than one" / "we would have a flake there" is transcript-only.)

> And to your second question, I do have some broad ideas. I'm sure you could probably infer some of them, but I would like to review the drafts for all of the skills.

(Transcript-only: the psyche wants to review skill drafts before they land; has broad ideas for the per-harness skills but wants the flow to propose first.)

-- psyche, STT; transcript: `/home/li/.claude/projects/-home-li-primary/38dec9a9-71a6-4d33-a85d-b98879027b41.jsonl`, line 246

---

## Supersessions and conflicts

### Superseded entries

1. **Training daemon superseded by flow daemon** (2026-08-18): "the new daemon I want to make isnt training anymore (abandonned). Its flow" (`flows/358f143a/vision/trainingRepo.md`) supersedes the 2026-08-17 "Curriculum should become a proper rust component (a daemon)" in the same file.

2. **"Phase" terminology withdrawn** (2026-09-03): "I don't know what you mean by 'phase.' Either we have to define what the phase is, or otherwise that's bluffing" (`flows/b9f4f6/vision/topStratum.md`) supersedes the 2026-08-30 "a phase is its own flow, with its own top stratum" (`flows/ceb3b9fd/vision/topStratum.md`) in the sense that the term is withdrawn until defined; the underlying vision (different top stratums for different jobs) stands.

3. **Desktop modification interest retracted** (2026-09-02): "I am no longer interested in heavily modifying those applications to achieve better functionality" (`flows/ea1e56/vision/desktopCodexIntegration.md`) does not conflict with the wrapper-executable vision (which is about the CLI, not the desktop apps), but marks a shift away from deep desktop-app customization.

### No same-time conflicts detected

The entries proceed chronologically with each refining or superseding the last. No two simultaneous entries on the same subject give contradictory rulings.

### Entries that sit oddly

1. **Pi deprecation vs. the per-harness-skill proposal**: The 38dec9 per-harness-skill proposal mentions creating skills for each harness including potentially Pi, yet `flows/5a3ee4/vision/pi.md` says "pi is slop" and marks it deprecated. These are consistent (the proposal says "abandon"), but the pi.md file has no date, making the temporal relationship uncertain.

2. **"chatgpt apparently has 4 strata of context"** (`flows/e8c4cc61/vision/psycheLayers.md`): This is a parenthetical aside while discussing psyche layers. It sits oddly only in that it is an unverified claim about ChatGPT's architecture made in passing during an unrelated topic. It should not be treated as witnessed.

---

## Agent-harness-packaging skill

The `agent-harness-packaging` skill (`.claude/skills/agent-harness-packaging/SKILL.md`) is a deployed skill:

> Treat an external harness manager as distinct from the Claude or Codex harnesses it coordinates.

> Obtain current release, packaging, installation, and integration facts from authoritative upstream sources before choosing or changing an integration.

> Put durable packages and configuration in the declarative source that owns that environment.

> Put a distinct reusable package in its own public package repository; a home-environment source consumes a pinned package output.

> Give an agent manager a package and executable name that cannot collide with an unrelated existing package; StablyAI Orca is `orca-ide`, not GNOME `orca`.

> Do not run an upstream integration installer that mutates a configuration Nix owns; express the intended configuration in its declarative owner.

> Evaluation is not package proof: build the artifact and behavior-smoke every claimed CLI, GUI, and headless surface.

Path: `.claude/skills/agent-harness-packaging/SKILL.md`

---

## Sources

### Already in the main flow's hands (flow 38dec9 vision files)

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

### Legacy vision-raw/

- `vision-raw/attunement.md`
- `vision-raw/encodedFormIsTheCode.md`
- `vision-raw/entryFiles.md`
- `vision-raw/flowsNotAgents.md`
- `vision-raw/gradientsOfAuthority.md`
- `vision-raw/spirit.md`
- `vision-raw/trainingRepo.md`

### Per-flow raw vision

- `flows/019fe121/vision/agentIntercom.md`
- `flows/019fe728/vision/agentIntercom.md`
- `flows/01a02a34/vision/progression.md`
- `flows/01a02f23/vision/orca.md`
- `flows/01a030df/vision/subagents.md`
- `flows/01a0338f/vision/mediumGraphicalNodes.md`
- `flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md`
- `flows/01a038be/vision/codexDerivation.md`
- `flows/01a038be/vision/installingSoftwareStatefully.md`
- `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md`
- `flows/01a03e39/vision/lastSuggestion.md`
- `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md`
- `flows/01a0428b/vision/codexOnlySkill.md`
- `flows/01a0437d/vision/codexAndClaude.md`
- `flows/01a04524/vision/claudeRemoteControl.md`
- `flows/01a047d2/vision/remoteControl.md`
- `flows/01a048a6/vision/agentIntercomGraphical.md`
- `flows/01a05487/vision/flowMovesBetweenGenerations.md`
- `flows/01a05487/vision/thinkingMachine.md`
- `flows/01a05826/vision/flowIdentity.md`
- `flows/01a05d17/vision/fullAccessPermission.md`
- `flows/1030529c/vision/workspace20.md`
- `flows/15b67974/vision/flowDaemon.md`
- `flows/15b67974/vision/persona.md`
- `flows/2f6b1dc5/vision/contextStrata.md`
- `flows/2f6b1dc5/vision/systemPrompt.md`
- `flows/358f143a/vision/behavior.md`
- `flows/358f143a/vision/entryFiles.md`
- `flows/358f143a/vision/falseConfidence.md`
- `flows/358f143a/vision/gradientsOfAuthority.md`
- `flows/358f143a/vision/letsUseTheSameVocabulary.md`
- `flows/358f143a/vision/skillDesigning.md`
- `flows/358f143a/vision/skillsRepository.md`
- `flows/358f143a/vision/trainingRepo.md`
- `flows/358f143a/vision/workspace20.md`
- `flows/4ddc321d/vision/contextStrata.md`
- `flows/4ddc321d/vision/hijackRepositories.md`
- `flows/5a3ee4/vision/pi.md`
- `flows/78c93c/vision/machine-generated-content.md`
- `flows/78c93c/vision/witness-reuse.md`
- `flows/aa4c7747/vision/basePrompt.md`
- `flows/aa4c7747/vision/dispatches.md`
- `flows/aa4c7747/vision/promptCrafting.md`
- `flows/b9f4f6/vision/topStratum.md`
- `flows/cf0ed9/vision/openaiLacksTheFeatureIWant.md`
- `flows/ceb3b9fd/vision/hijackRepositories.md`
- `flows/ceb3b9fd/vision/topStratum.md`
- `flows/e4be1c4a/vision/skillTypes.md`
- `flows/e8c4cc61/vision/psycheLayers.md`
- `flows/ea1e56/vision/desktopCodexIntegration.md`
- `flows/e06e4c07/vision/letsUseTheSameVocabulary.md`

### Per-flow notion

- `flows/01a05487/notion/rollingCodexServices.md`

### Skills

- `.claude/skills/agent-harness-packaging/SKILL.md`

### Transcripts

- `/home/li/.claude/projects/-home-li-primary/38dec9a9-71a6-4d33-a85d-b98879027b41.jsonl` (flow 38dec9), lines 135, 169, 246
