# Psyche collection: how skills are made and landed

Collected by subflow 7b4d4ce2-93f3-4499-ae22-742fd6a34316 for flow 7b4d4c, 2026-09-04.

---

## Spirit

No spirit-level entries found on this cluster. The spirit skill carries the general principle that the context is the agent ("An agent is a machine; it does not misbehave. An agent's output is a function of its context and prompt — when an output looks wrong, determine the lacking or incorrect context which produced it"), which underpins the strata architecture but is not itself about skill process.

---

## Intent

No intent-level entries found on this cluster.

---

## Distilled Vision

### Vision/distillation.md — distillation process

> A working instruction logged as vision is a vision impurity. It may sit in a log beside valid vision; when distillation finds it, the impurity is dissected out of the log and destroyed, and the valid vision around it stays.

> Impurities come out in the course of distillation: a distillation proposal points out the impurities it dissects out, and the living rules on them with the statements.

> A distillation proposal says, for every statement, the topic it goes to; a statement under the wrong topic is corrected by a distillation edit of its own.

> A distilled statement carries what the psyche said and nothing beyond it. A small ruling makes a small statement.

> Designing model behavior is vision, and a correction of an agent's conduct can be vision.

> A distilled statement carries no useless negative.

> Vision is the psyche's; a distilled statement never says so of itself.

---

## Raw Vision (vision-raw/)

### vision-raw/skillDesigning.md — 2026-08-19

Design session e06e4c07:

> the skill. green on the batch, deploy it all

### vision-raw/skillsRepository.md — 2026-08-21

Design session 15b67974:

> re registration check: the problem is we should get rid of the manifest and generate whatever skills are present. curriculum went through a very elaborate phase that was abandonned. many of those things are now unwanted. like how some things were broken up into modules. new insights made me realize this was the bad approach.

### vision-raw/skillsRepoSourceOnly.md — 2026-08-10

> "I dont want to see any .claude or .agent in the skills repo"

Context: the generator had been writing output into the source checkout. Generated output belongs only in consumer workspaces (like primary), not in the skills source repo.

### vision-raw/skillVoice.md

Heading only: "Skill voice — 'You are X' versus 'X is …'". No content.

### vision-raw/skillTypes.md

Heading only. No content.

### vision-raw/context.md — 2026-08-17

> LLMs don't actually have any way to imagine; their context forces them into a thought. You would have to use a specialized flow, trained to imagine this sort of thing. Maybe we should just let the next flow mine its own handover with a specialized subflow.

Context: handover quality degrades with session complexity because the ending session must guess what the next session needs — a generation-from-imagination task LLMs are bad at. The starting session can read and extract (a reading task LLMs are good at). Pull beats push.

### vision-raw/managementDelegation.md — 2026-08-09

> "The manager doesn't get involved in implementation-level detail. So I would rather train subagents to escalate back to their parents if the way to proceed forward isn't clear than for parents to try to micromanage their children and end up burning out, essentially doing more work than if they were just doing it themselves."

> "the manager's context is gold. he has to keep his hands clean so he doesnt get oil and shit all over the blueprints"

### vision-raw/gradientsOfAuthority.md — 2026-08-10 (session c6b71b4c)

On per-session top layer and skill primacy:

> So what I see is every session is unique and has the top layer, I guess we're going to call it, fed its own set of skills and style guidelines, like everything we put in skills, our standards, whatever that agent is going to need to do its job is going to be in the top layer. So that way, the way we code, for example, like our rest [Rust] guidelines and things like that, it's going to have much more power to guide the agent to code better. And the skills are going to be primary.

On the context-strata skill description — 2026-08-19 (session 7c3f0c1d):

> the description is bad. and LLM should appear in the skill, possibly in the description, which should also indicate that this skill is rarely ever needed

### vision-raw/psycheLogStructure.md — 2026-08-09

> "psyche shouldnt be organized by aspect, but by topic and date"

— 2026-08-14 (session 06196cc7):

> lets reframe that to make new topic a psyche blocked thing, and lets create a list of topic which are allowed for now. Or maybe we just do merging passes to make it easier to log "safely", so the flow doesnt have to overthing where to write something down

> I think this also brings the subject of keeping the psyche clean; after a while too many entries will exist, many of which will be overruled statements. The cleaning/merging pass is the way. But it needs to be psyche assisted to avoid mistakes. So an agent makes proposal statements which are aimed at replacing a bunch of psyche records and the psyche pronounces on them, then the old records are archived. it should even be archived to link back to the record(s) that replace them, ostensibly with a short hash. How does that sound?

> lets create a new psyche skill. find a name and make a first proposal. and some of the vision should be transferred into skills. we should have a manifest then that links some skills to psyche archives. see my discussion with claude d2bb5f5f

The same entry also records: "agent annotations are not records" was never ratified — the psyche said "I dont understand" and moved on without approving or rejecting the principle.

### vision-raw/visuals.md — 2026-08-21

> I want to also train agents now to give me more visuals. There's something about everybody now is developing with flowcharts and graphs, because text gets tiring without a flow around it and a structure. So, yeah, I want to see more visuals all the time, maybe something in psych [psyche] interaction. And if they're printed in the response, it's ASCII, if they're in an artifact, it's a mermaid.

### vision-raw/entryFiles.md — 2026-08-17 (session 358f143a)

On skill variables:

> theyre not variables if they dont have a name, but that is rougly the idea

> right now its doing too much. variables should go in its own (AGENT_VARIABLES.md?) file, which is setup specific and therefore not in curriculum, but is documented in curriculum's agents.md file, so agents are made aware that those variables should be set and how.

### vision-raw/roleDescriptions.md — 2026-08-19 (session 7c3f0c1d)

On the read-critical tier description:

> this line "A missed detail changes the conclusion." is really bad then

---

## Flow-level raw Vision

### flows/e4be1c4a/vision/skillTypes.md — 2026-08-16

> "the awareness file should be a skill, a type of skill. I want to introduce skill types now. role skills are what the awareness files become"

> "And propose a sensible design sole skill. all role skill will be non-flow usable (must be manually triggered in user prompt. what do we call that?)"

### flows/e4be1c4a/vision/skillsRepository.md — 2026-08-16

> "I want to rename the skills repo to something else. Training comes to mind but im not crazy about it."

> "english name."

> "Curriculum is good. rename it, and any reference in our main entry files"

### flows/4ddc321d/vision/skillDesigning.md — 2026-08-26

> context does this. Removal is better than addition, when the expected behavior is the desired behavior. That would be a good line for skill-design
>
> so it sounds like that entire skill block could potentially be removed.

### flows/cff271af/vision/skillDesigning.md — 2026-08-22

> let's review it all then. I think nexus becomes software-design, as we design everything using a nexus going forward (the runtime part of course; libraries are still needed sometimes like with datom, and maybe others you can name (trait libraries))

— 2026-08-23:

> we said "the map" is broad and overloaded. but fine for now. include everything in the draft so I can review it. Acquire all the relevant context. you can even do some research into those unusual ideas to see if a clever way of saying parts of it comes up somewhere.

### flows/01a05487/vision/skillEditProposal.md

> "obviously you would replace one with the other in the skill, not write this line"

Context: a skill-edit proposal must present the resulting source edit, not a meta-instruction as though that instruction were new skill content.

### flows/acbb6006/vision/approval.md — 2026-08-27

> everything I commented past and didnt comment on was approved

> Like I said, anything I comment past is approved.

### flows/acbb6006/vision/distillation.md — 2026-08-27

On impurities in distillation proposals:

> 5. yes, impurity

> re impurities: yes, destroy them all

### flows/a60a9e85/vision/distillation.md — 2026-08-23

> lets go through one concept at a time. you are unable to do a synthesis because you didnt understand the concept themselves. Lets take this opportunity to understand each concept to distill the psyche at the same time; they are the same thing really; distillation is comprehension

### flows/62022e8f/vision/distilledVision.md

> the vision really is like a skill without, it's a bit more detailed, I think. So when we have like the vision of something together, it has sort of like all the details, which is good for implementing something. But from that, like concentrating the vision and just taking the parts that are sort of important to know to understand the concept is how we create skills. So by creating the vision, we sort of almost automatically create the skill.

> And it would make it obvious whenever if I said something that contradicted that, that we need to change the vision. And then we could sort of, we don't necessarily always have to work on raw vision when I speak. If what I'm talking about is something in the distilled vision, like obviously you can log what I say, but then you can also just apply what I say directly to the distilled vision, if you understand what I'm saying.

### flows/62022e8f/vision/designPractice.md

> Do not spend Fable output on HTML: write markdown, let a subagent convert

> I dont like those broken up bits of code. Use code blocks with comments.

> the subflow can also pick colors

### flows/995a164e/vision/designPractice.md

> I'm not able to read this. Like I said, I told you before. Yes, the main flow shouldn't make a web page or, in this case, a web report. I don't think that's a wise use of its context. It should make a Markdown file, and then it can use Mermaid graphs to represent the ideas that it wants to represent. The sub-agent that turns this Markdown into the actual web report should not use Mermaid. I think this is what happened here. It should make properly scaled SVG representations of it so that they're clearly readable and render correctly, so I'm not actually able to read that part of the graph here.

### flows/995a164e/vision/tokenCosts.md

> token costs are not qualified by size, but by necessity. a useless token cost must be eliminated

### flows/01a0428b/vision/useASubflowToPutTheReportTogether.md — 2026-08-27

> And what I would like, how I would like this to be done is because a subflow can actually read the transcript that it's here, it would be more efficient. I don't want the main flow to do a bunch of file files and code reading to just essentially repeat what's in its own context. So it would be better to use a subflow to put the report together. And then when doing something more script like that on the Codex side, we should use a terra model

> I didn't mean use terra for everything, I meant for the report writing

### flows/01a0428b/vision/codexOnlySkill.md — 2026-08-27

> Check a recent codex session for the web reporting procedure which we'll put in a codex only skill

### flows/01a04881/vision/subflows.md

> "youre the one who can best guess why you did it, not another flow with a different context than yours"

### flows/01a05826/vision/subflowIdentity.md — 2026-08-31

> I guess we could also use session hooks, but it couldn't be a hook that also gets triggered by subflows, because then they get the same ID, and that would create a tension. I don't want subflows to start creating their own lanes. They just use their parents.

### flows/01a05e95/vision/flowSkills.md

> "I think we should have some kind of a master flow or main flow skill that explains the part about using subflows. I think the skills are a bit misnamed. I think the flow skills should explain the whole protocol, both from the point of view of the parent and the child. They should be able to know that it's a child and how to behave."

> "Maybe the flow protocol should be called Flow Logging or Flow Directory. It's more than just logging, where reports go and stuff like Flow Files. It explains that part, or maybe it explains it for the main flow, and that skill is not visible for agents. There's another smaller skill that explains it from the point of view of the subflow, which is visible for agents and which this subflow is told to read."

> "Perhaps the job of the main flow is to give all subflows the actual flow ID that they're supposed to use, so that they know where to put their files if they want to put reports or witnesses. I'm not saying they 100% should not. I think it's the job, like you said, of the main flow to decide whether or not it should be logged, so they shouldn't really be logging. They might want to put a report or witness, and that's where it should go."

### flows/01a05e95/vision/subflows.md

> "I want subflows to use the parent flow directory ... We need to figure out how we can reliably create a situation where the subflows use the same flow ID as their parent for everything that they want to write."

### flows/01a05e95/vision/logging.md

> "Logging should be rare. It should just be to give a very high-level summary. ... The transcripts are there. If we really need to know the details of what happened, we can look into the transcript."

> "Well, it's because the sub flows are logging everything, it looks like. That's overkill. Maybe the sub flows should not really log, at least not in a way that the main flow is logging."

> "The point of a subflow is for it to edit what it edits and then return the final response. Like I said, the transcript is still there if we really need to know what happened. For it to do all of this logging doesn't just create a lot of all these log files, but it also pollutes this subflow's context. ... It distracts it from its main task by making it constantly add a line every stop."

### flows/cff271af/vision/reports.md — 2026-08-22

> Here's the thing. The living speaks to the main flow. So, if we have a bunch of artifacts, I mostly don't read reports. They're there for... To be honest, right now I'm wondering, in most cases, do we even need reports? Because if the audience is in the main flow, and in almost all the cases is not me, then what is really the intended audience?

> Yeah, there's some interesting things you've raised here, and there's something I want to point out, which is that if an agent's, sorry, if a subflow's output is only its response back to the main flow or to its parent, that data still sits in the transcript file. So making the subflow write a report and then making the main flow read the report just seems like useless churn. ... What is really important is the main flow's context and implementation workflows being essentially well-informed, which should not depend on a bunch of reports that subagents wrote, because the conceptualization of what the subflow really ought to do, that liability really falls on the main flow ... the most useful and precious context is only that which the parent flow gives it as its starting prompt.

Note: the same entry includes a claim about Claude loading skills in the mid-stratum while Codex does not, which the psyche flagged as possibly inaccurate.

### flows/04db2fd2/vision/artifacts.md

> I dont see the point of creating a multitude of directories for "subtypes of reports" - sounds like we need a skill for subflows to know where to put artifacts, although I want file artifacts to be discouraged; a subflow's ultimate production should be its final response. We consider transcripts searchable artifacts, and want to develop that approach over writing a lot of files. The failure was not using the flow's directory; all file artifacts should go in a flow's directory (if we exclude work on repos of course)

### flows/04db2fd2/vision/psycheLogging.md

> when we log psyche, I've noticed ... that often the log will contain like the entire, because now I'm doing this huge speech to text ... So there's going to be several things that come out of this text. And I've noticed, it seems that the model tries to just ... reuses that whole text in all of the different logs ... But what should really happen is it should ... only include the bits in the text that concern that particular entry ... And then the spaces in between is just a triple dot notation ... Because the original is in the transcript. So we don't need to try and preserve the original text, the whole thing.

> no, no timestamps, and the location of the logging (in the flow's directory) means the session id is already implied, so it isnt a concern at all.

### flows/04db2fd2/vision/rollingDistillation.md

> I want us to roll with distilling that vision. So as we go, so whenever we touch like this datum [Datom] subject ... you can sort of take something we've touched upon like heavily and send your sub-agents like, okay, you go look for anything that might remotely like touch this, and let's distill it, because I think we're accumulating too much raw vision, and we need to start distilling it faster. So we can almost start making this like an ongoing process that agents could almost at every second or third turn propose the distillation of the vision that's been accumulating so far

> design and psyche-distillation skill edit is good.

### flows/04db2fd2/vision/overtalking.md

> I havent read your last response. Stop making all those file reports, I dont ever read them. Talk to me here. Reprint whatever you think I should address. Try not to overtalk so I dont fall behind on your responses

> the skill edits are all good, but the "dont elaborate when subflows are running" only goes in psyche-interraction

### flows/01a052b6/vision/reportFeedback.md

> I want to be able to put comments from my phone. Essentially, I'm remote accessing Codex, which is running on my machine here, and then Codex would create a visual report. There would be a link I could open on my phone where I could actually put in all the comments one by one. I would be able to put in comments without triggering the session every time I put a comment. I could potentially put multiple comments and then go back to the session and tell it that I commented on the report. It would be able to see all the comments and what they refer to. ... I'm describing the flow that I have developed with Claude, and that's the kind of flow I'm looking to get with Codex.

### flows/01a052b6/vision/visualCollaboration.md

> I was looking for something that would allow me now to start collaborating with the machine through drawing. ... I want, I would like something that sort of fulfills my need right now that we could set up in a few minutes or in a few hours at most.

> The workflow that I would like that I could see possible right now is that I would have some kind of pen tablet and ... I would be able to express some ideas visually, and then the machine would be able to see that. And then it would be able to sort of do edits on that. So we would have some kind of version control of like the evolution of that visually augmented thought or concept. And then I could do my own like back and forth editing

### flows/b9f4f6/vision/presentation.md — 2026-09-03

> Don't your instructions tell you to wait until all the sub flows have returned to do your presentation and questions? Don't they tell you to not try and show me something through a file?

> I don't know if your wording is strong enough. ... You just don't listen to what I want. I voiced this desired outcome before, and I still get the same problem

### flows/db97561c/vision/context.md

> so you wasted tokens and destroyed your context by printing the same thing twice. propose a fix to this behavior

### flows/358f143a/vision/skillVoice.md — 2026-08-17

> Thats not what I was considering. Rather I was considering "You are
> X" vs "X is (actionable information; reasons, standards,
> explanation".
> "You are X" seems to lean on the side of pretension, which to me
> looks like it would lead to blufing. Like you said, saying "You are
> an expert on X" doesnt grant expertise, but might lead the model to
> *pretend* to be an expert.

> 1. Yes
> — (approving rewrite of role skills into information form)

### flows/01a02fe5/vision/skillTraining.md — 2026-08-24/25

> We need better skill training

> it doesnt matter why. those variables are confusing. we should rely on good training instead of trying to hardwire which node all situations should use, which is obviously wrong

> remove those hard wired deployment variables and propose skill training that explains how the cluster works

> way too complex. start with ultra minimal

> ok approved. and we have removed the static deployment variables?

### flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md — 2026-08-25

> when you have it working again, add this to the prompt-crafting skill:
>
> ▎ A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.

### flows/db97561c/vision/promptCrafting.md

> never tell stuff like that to an implementer
> — (on "Rust syntax is the target: recycle it")

> actually the file turned out to be better, as I can't copy the prompt from your response when working remotely from my phone.

> your remember prompt is too complicated. don't convey any design! just give the minimum to guide the remembering; let the other flow remember the data!

Note: "the file turned out to be better" (for a prompt the living will paste from a phone) is a different artifact type than a proposal shown for judgment — no conflict with "don't show me through a file."

### flows/15b67974/vision/domainKnowledgePlacement.md — 2026-08-22

> that was before I realized the existence of the context strata.
> skills are the current gateway to agent-accessible mid stratum
> (maybe not on codex; codex may not offer an interface for the model
> to load the mid layer. Maybe another harness offers an access.
> Otherwise we may have to create our own harness to make this
> accessible (or modify one)

### flows/15b67974/vision/flowKnowledge.md — 2026-08-22

> Iv assumed a lot in the last few months. I thought agents would
> carry on momentum. that is now thoroughly disproven.

### flows/b9f4f6/vision/topStratum.md — 2026-09-02/03

> Let's see how pierce's system looks like in a specialized-harness
> system.

> I don't know what you mean by "phase." Either we have to define
> what the phase is, or otherwise that's bluffing. It's made up, it's
> a hallucination

### flows/e4a40e/vision/distillation.md — 2026-09-03

> I don't understand what your proposal is. Where are you proposing to put what here? ... Did you take the consideration to look at what you might be distilling into? Are you just distilling with the distillate, or are you just distilling the raw by itself without considering the already distilled vision? ... Why is it that every flow seems to have his own idea of how to do vision distillation?

> You're not going to show me the whole topic again. You're going to show me what you're changing ... You get the distillate at the end, so I want to see the distillate and where it's going. ... I just want to see the vision. I'll read it, and if I agree with it, then it lands. That's it.

> It's okay, you can change the skill to say just keep logging because, as our experience shows, you guys seem unable to get me any kind of distillation landed.

### flows/ad19b1/vision/distillation.md — 2026-09-04

> Does that even make sense to you? Does that sentence even look like it remotely makes sense to you? Why would you even repeat this nonsense?

> the distillation skill line should be made more universal.

> Well, it will be as soon as I fucking approve this. Now I can't approve it because you're basically saying that I can't approve it by saying it's not decided. You're deciding for me ahead of time that I can't agree to this design.

### flows/cff271af/vision/distillation.md — 2026-08-22

> It's always better to distill. If you're going to bother, if you're going to bother the living, then increase the value. Distilled psyche ... distilled psyche has more value than raw psyche because the raw psyche is always archived, so it's always still there, and it's referenced by the new distillation. But it's more clear and it's more compact, so it offers more signal to noise.

> never is a very strong word ... when I run into something like that, I prefer to not give too much of my energy to the rest because if I find a flaw like that, then it's a sign that I'm quite out of alignment with the flow's current perspective. But I do agree with the proposal for Psyche distillation.

> what manifest? Distilled vision has to be up to date! There is no more manifest. This vision is stale

### flows/b675f3d9/vision/archive-distillation.md — 2026-08-27

> dont give me blocks of proposal without telling me where it goes, since "The signal interfaces tell an enum from a struct by the delimiter after the head" is ethos vision, *not* protos, so I cant say yes or no to your proposal. propose a distillation edit for this as well.

### flows/04db2fd2/vision/softwareAnatomySkill.md — 2026-08-27

> two things will come out of the work we're doing here. One is the actual implementation of datum [Datom] ... we're going to work out how to essentially how to work out the anatomy of a program by breaking down its components ... we're both defining, so we're going to be writing out of this, a skill on how to design software.

### flows/62022e8f/vision/designPractice.md (additional entries)

> This document is really good. Most of the examples and the explanations that I find in here are almost word for word ready to go as vision. ... maybe you even want to express like the approach that you took to try to understand the meaning behind my meaning ...

> I don't really want to use reports in the way that we've used them now, which is like where you try to answer my question in the report ... I like the report better before when it was only about, like, it was just raw. There was no back and forth explanation or questions ... it was more raw, good, like almost vision-ready content.

### flows/2f6b1dc5/vision/contextStrata.md — 2026-08-24

> I cant find the context strata skill I was designing some time in the last few days. We could disambiguate all of that in there, and use it for working on this aspect of things, or to make agents aware of this who need to be. Find the flow(s) concerned and bring all the material forward in a proposal, where all the vocabulary is explained simply and clearly

> deploy the LLM strata skill with context instead of prompt.

### flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md — 2026-08-25

> I want to migrate curriculum stack to datom instead of dotos

### flows/e4a40e/vision/witnesses.md — 2026-09-03

> Your skill edit proposal is too narrow, and we had already verified how traits naming behaves in Rust many times before. What is keeping us from being able to reuse these verifications without having to run them all over again? How can we be more efficient with our witnesses?

> Well, that's not what I remembered. I remembered creating the flow protocol whereby there was a witness or witnesses or witnessed directory in each flow, where witnesses would be stored so that they could easily be found because they all have the same directory structure, right?

### flows/5c8be3ca/vision/flowArtifacts.md — 2026-08-21 / 2026-08-22

> there's no handoff file; the flow *reads its previous flow(s)* - it's the inverse of push dont pull, since LLM flows are totally different than regular software

> no of course not! the directory gives the flow. only subflows need to indicate their id

> a lot of your negative rules are context confusion. dont involve the refusals with the composition. See you understand with a skill design proposal, and repropose the protocol; I need to see the skill proposal itself

> this is just noise. models will do this naturally
>
> great, let's land this

---

## Transcript-only

### 38dec9a9 L246 (flow 38dec9, 2026-09-04)

The statement that the subflow-landing practice should become standard:

> If I approve them, you could set up some agent to just read your transcript and put these into files so we don't waste context for you to shuffle all this text around. Whatever you print in your response can be used by a subagent to create or modify the actual skill files and deploy them.
>
> This, I believe, is something that I wanted to develop into standard practice, so you can have an agent check out and see if that's actually the case.

### 38dec9a9 L169 (flow 38dec9, 2026-09-04)

The per-harness skill architecture with universal remainder:

> Let's maybe create a Claude harness skill and a Codex harness skill, and move some of the harness-specific information that may already exist in some skills into those, and then start putting everything in there that we know: how to override the system prompt, which part of the system prompts cannot be overridden by that flag, how many strata each harness actually has (I believe Codex has 4 and Claude has 3), whether the system prompt is visible to the model or the machine, and not to me

> Give me a draft on how we would do all of this per harness skill and what we could keep that's universal. Maybe the strata or the context strata skill can still remain, but have only the high-level concepts, like the explanation of what these strata are in the entire field of thinking machines and so on. We would have it per harness skill that gets more into the details of how that particular harness and those particular thinking machine models actually behave.

### deca2323 L148 (2026-09-03)

> No, the main flow still writes its flow log, and it records the Psyche, but your editing is not quite what I envision yet. Oh, and yeah, the main flow can also write beats, and I want to change the whole terminology. Somehow, the whole parent and child thing came in and took over. I want to just stick with main flow and sub-flow, so let's change all these terms

### deca2323 L154 (2026-09-03)

The full mechanism for transcript-landing by subflow:

> Yeah, this is all pretty good, except that I would even reinforce it. Instead of saying, "Reports, design documents, and landings are written by subflows," you could say "everything else also." When you say, "Proposal lives in the conversation until the psyche approves, then a subflow lands it," I would like you to explain the mechanism whereby it would be really stupid and inefficient for the main flow to just give the file content again in the subflows starting prompt. It would just be writing the file and then starting a subflow, which would be extremely stupid.
>
> We need a subflow that is specialized in being able to see what was approved in the transcript and extracting that from the transcript directly into the file. The whole point is to save the main flow's context, so we don't care if we have to use a subflow to retrieve the transcript and then copy that into a file. Just identify the part of the transcript that was the proposal that was approved. There isn't really anything to fail on for any recent thinking machine model. They would never fail to do that, so they would just go from the end of the transcript, find where the approval happened, see what was approved, and land that.
>
> If it's a composed approval, just use a more capable model, but it'll be more than capable of putting the pieces together, seeing what was modified, finding the original proposal, and then applying the modifications that were then applied further in the conversation. Essentially, the main flow doesn't have to reprint the whole approved content as a single shot. It can just trust that the subflow will piece it back together correctly and put it in the file.

### deca2323 L10 (2026-09-03)

> I want to go with you on the topics that it touched on in its last message, which it called prompt one, about how the main flow shouldn't really be editing almost any files. I want to make this really strong because we're wasting a shitload of tokens on writing the same thing in the file as we're writing in the response.
>
> Let's also look at the skill design skill to make that clear. I've had a lot of suggestions for skill editing that were suggesting lines that were actually repeating some of the lines already in this skill. Any proposal should remain acutely aware of the current skills so that we aren't just bloating the skill with repetition. Repetition is really, really bad. Essentially, it's the greatest source of inefficiency we're facing with the thinking machines right now.

### c346913e (starting prompt, typed)

> Do a survey of the recent flows and what they seem to have left unaddressed. Using that list that you put together, see what has and hasn't been addressed in fact by looking, and then give me a summary with a visual: a nice web report that you'll get a subflow to make from a Markdown file version that you'll create yourself. You don't have to do HTML coding. You just write it in Markdown, and this is how I also want to do things, so we can talk about that skill. Do a thorough investigation and a thorough survey of the facts, and then put it all together in the report and get a subagent to render it in a nice Claude web report.

### 77cca2bc (starting prompt, typed)

> Find out about the methods that I have prescribed for creating web cloud reports through the main flow, creating a Markdown file, and see if that's what the skill prescribes already. If that's the behavior I would get if I didn't explicitly demand it, then show the proposal for the skill that would probably get that behavior without demanding it in any case.
>
> Of course, this is cloud-side only until we have the infrastructure in place for Codex to be able to do something similar, so it would be cloud-gated. Once you have all that figured out, put everything that I've asked for to be shown to me in that final web report, in the way that I just described:
> - A subagent actually renders the web report
> - You only create it as a Markdown file that the subagent then uses and recreates all of the charts in proper SVG so that they render properly
>
> I want lots of visuals, and that would also be a part of the skill. I very much like visuals. They're soothing to the mind, and they create a better dynamic between man and machine.

### b9a334a4 (starting prompt, typed)

> create a web report of the situation using the markdown + subagent approach, and let me know if this approach is standard and would be expected to happen even if I didnt explicitely demand it

### 7b4d4ce2 (starting prompt — this session's parent, typed)

> Then create a markdown+subflow web report I can annotate of the whole proposal.

---

## Supersessions and conflicts

1. **Terminology**: "parent/child" terminology → superseded by "main flow / sub-flow" (deca2323 L148, 2026-09-03).

2. **Reports**: the ruling at flows/cff271af 2026-08-22 ("do we even need reports?") and flows/04db2fd2 ("Stop making all those file reports, I dont ever read them") supersede any earlier default of subflows producing file reports. The surviving form is: a subflow's ultimate production is its final response; file artifacts are discouraged; when needed they go in the flow directory.

3. **Web report procedure**: the pattern solidified across sessions c346913e → 77cca2bc → b9a334a4 → 7b4d4ce2 (this session). The living asks for it in increasingly fewer words, and in b9a334a4 explicitly asks whether it is "standard and would be expected to happen even if I didn't explicitly demand it." This is a consistent, repeated request, not a one-off.

4. **Manifest vs. generate-from-presence**: vision-raw/skillsRepository.md (2026-08-21) says "get rid of the manifest and generate whatever skills are present," superseding any earlier manifest-based architecture.

---

## Oddities

- **flows/cff271af/vision/reports.md**: the psyche's claim that "Codex does not load skills that are loaded by the model itself in the mid-stratum, and only Claude does" is flagged by the psyche itself as possibly inaccurate ("maybe this information isn't actually accurate"). This should not be built upon.

- **vision-raw/psycheLogStructure.md**: "agent annotations are not records" was presented as a principle but the psyche said "I dont understand" and never ratified it. It stands unratified.

- **flows/e4a40e/vision/distillation.md**: "just keep logging" (2026-09-03) is a pragmatic concession born of frustration ("you guys seem unable to get me any kind of distillation landed"), not a revision of the desired state. It sits oddly against "It's always better to distill" (2026-08-22, cff271af) and "rolling distillation" (2026-08-27, 04db2fd2). The desired state remains rolling distillation; the concession is a fallback until flows can reliably execute it.

- **flows/db97561c/vision/promptCrafting.md**: "the file turned out to be better" (for a prompt the living pastes from a phone) sits alongside "don't show me through a file" (b9f4f6, 2026-09-03). Not a conflict — different artifact types: a consumable prompt vs. a proposal for judgment.

---

## Sources

### Flow 38dec9 vision files (in main flow's hands — listed, not reprinted)
- `flows/38dec9/vision/agentToMachine.md`
- `flows/38dec9/vision/deepsekHarness.md`
- `flows/38dec9/vision/harnessVocabulary.md`
- `flows/38dec9/vision/invocationSystem.md`
- `flows/38dec9/vision/perHarnessSkills.md`
- `flows/38dec9/vision/piHarness.md`
- `flows/38dec9/vision/skillLandingBySubflow.md`
- `flows/38dec9/vision/systemPromptRepository.md`

### Distilled Vision
- `Vision/distillation.md`

### vision-raw/
- `vision-raw/skillDesigning.md`
- `vision-raw/skillsRepository.md`
- `vision-raw/skillsRepoSourceOnly.md`
- `vision-raw/skillVoice.md` (empty)
- `vision-raw/skillTypes.md` (empty)
- `vision-raw/context.md`
- `vision-raw/managementDelegation.md`
- `vision-raw/gradientsOfAuthority.md`
- `vision-raw/psycheLogStructure.md`
- `vision-raw/visuals.md`
- `vision-raw/entryFiles.md`
- `vision-raw/roleDescriptions.md`

### Flow-level raw vision
- `flows/e4be1c4a/vision/skillTypes.md`
- `flows/e4be1c4a/vision/skillsRepository.md`
- `flows/4ddc321d/vision/skillDesigning.md`
- `flows/cff271af/vision/skillDesigning.md`
- `flows/cff271af/vision/reports.md`
- `flows/01a05487/vision/skillEditProposal.md`
- `flows/acbb6006/vision/approval.md`
- `flows/acbb6006/vision/distillation.md`
- `flows/a60a9e85/vision/distillation.md`
- `flows/62022e8f/vision/distilledVision.md`
- `flows/62022e8f/vision/designPractice.md`
- `flows/995a164e/vision/designPractice.md`
- `flows/995a164e/vision/tokenCosts.md`
- `flows/01a0428b/vision/useASubflowToPutTheReportTogether.md`
- `flows/01a0428b/vision/codexOnlySkill.md`
- `flows/01a04881/vision/subflows.md`
- `flows/01a05826/vision/subflowIdentity.md`
- `flows/01a05e95/vision/flowSkills.md`
- `flows/01a05e95/vision/subflows.md`
- `flows/01a05e95/vision/logging.md`
- `flows/01a052b6/vision/reportFeedback.md`
- `flows/01a052b6/vision/visualCollaboration.md`
- `flows/b9f4f6/vision/presentation.md`
- `flows/db97561c/vision/context.md`
- `flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md`
- `flows/2f6b1dc5/vision/contextStrata.md`
- `flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md`
- `flows/e4a40e/vision/witnesses.md`
- `flows/5c8be3ca/vision/flowArtifacts.md`
- `flows/04db2fd2/vision/artifacts.md`
- `flows/04db2fd2/vision/psycheLogging.md`
- `flows/04db2fd2/vision/rollingDistillation.md`
- `flows/04db2fd2/vision/overtalking.md`
- `flows/fb1008c0/vision/context.md`
- `flows/358f143a/vision/skillVoice.md`
- `flows/01a02fe5/vision/skillTraining.md`
- `flows/db97561c/vision/promptCrafting.md`
- `flows/15b67974/vision/domainKnowledgePlacement.md`
- `flows/15b67974/vision/flowKnowledge.md`
- `flows/b9f4f6/vision/topStratum.md`
- `flows/e4a40e/vision/distillation.md`
- `flows/ad19b1/vision/distillation.md`
- `flows/cff271af/vision/distillation.md`
- `flows/b675f3d9/vision/archive-distillation.md`
- `flows/04db2fd2/vision/softwareAnatomySkill.md`

### Transcripts
- `38dec9a9-71a6-4d33-a85d-b98879027b41` (flow 38dec9) — L169, L246
- `deca2323-cd63-4cb5-a239-1272a1ea69cd` — L10, L148, L154
- `c346913e-e195-4c2c-8fe7-336acdb62479` — starting prompt
- `77cca2bc-6e44-4fa3-91a5-44c4c649ba3f` — starting prompt
- `b9a334a4-f2fc-4c10-836e-f1d454c71fef` — starting prompt
- `7b4d4ce2-93f3-4499-ae22-742fd6a34316` (this session's parent) — starting prompt
