
## Field holds one context type

> I even think I want to remove the trial context type because there's very little difference between compensation and trial. They would create a sort of consistency in that psyche has three context types, mind has two, and field has one, which shows the sort of decrease in importance. The psyche is so important that we can divide it into three parts. The two in the field are really just all machine-generated stuff so there's no point in differentiating.

Context: comment on «Context modules», the figure's field box ("compensation, trial").
-- psyche, STT, 2026-10-13T17:06.

## Skill repositories become context repositories

> Let's rename all of these repos. Psyche skills becomes Psyche context and so on.

-- psyche, STT, 2026-10-13T17:07.

## The seat prompt is a psyche context module, not agent-visible

> This context is not living in the right place. It should be in the psyche and its vision or intent but it's a non-agent-visible context module. That's the only difference between most other modules and this one. It's not living in the right place so we have to modify the tool to use context modules from the context repos, which again should be renamed from skills to context.

Context: comment on «Three lines from the chat», target tools/main-flow-mode/system-prompt.md.
-- psyche, STT, 2026-10-13T17:27.

## Meta-flow context modules in the context repositories

> This is wrong. I want to crystallize a vision for a context module system. There are different types, more than whether it's spirit or intent, etc. There's, I guess, the regular module, which we can sort of draw a parallel with a skill, although the whole vocabulary of skills and things like that is inappropriately named. Those systems are quickly becoming obsolete by better harness infrastructure so I feel like the vocabulary is going to evolve a lot. Technically speaking we treat skill as sort of like a legacy system, which has uniform naming for things that are different.
>
> I just want to make that clear: we're recreating a more adequate vocabulary around this, around context, context modules, and context building. The type of context that you're proposing here needs to be yet another type as opposed to sort of correlating with skills. It sort of correlates with an agent's role, so metaflow. In this case this should also go in the context repo, one of them. In this case we're talking about psyche so it should go in the psyche context. By the way the mind context and the field context repos should also have been renamed from skills by now. Let's make sure they are.
>
> They'll contain another section, which could be several sections, one per layer. If we're in the psyche context repo, then we have primary, secondary, tertiary, quaternary, and maybe even some specialized topics. In the primary you have core.md, which is the prompt that goes to psyche by virtue of being in the psyche context, primary by virtue of being in the primary directory, and core topic by virtue of being the core-named file, and so on.
>
> We can have an ethos topic, although in that case it's almost certainly more appropriate to put it in a regular context module, like vision ethos for the ethos topic. Let's discuss that concept and recontextualize the proposal with that approach. These same sorts of flow-belonging context modules are what we should use to create the sub-agent specification files, like how we have sub-agent predefined: find sub-agent definitions, those sorts of low-specific. We could have a sub-agent directory in the context repo and in all of the context repos we could have a sub-agent directory which contains modules specific to specifically named sub-agent definitions. The idea is that all of these context modules are going to live in the context repos.

Context: comment on «Figures that move», the drawer's brief proposal (target: Primary, the book agent's figure procedure).
-- psyche, STT, 2026-10-13T18:01.

## Everything he reviews becomes psyche; compensation is Field's and unreviewed

> Those are all machine-generated and are not reviewed by me. ... It seems that you're saying this is in my context but it's a compensation and compensation is a field ... Let's find all these mistakes and locate all these context modules in the proper place and stop asking me to read machine-generated code. I don't review compensation skills. ... Everything I review becomes Psyche.

-- psyche, STT.

## As soon as he reviews something it becomes psyche

> Everything I review becomes psyche. ... Field is 100% agent-reviewed, 0% living-reviewed. As soon as I review something it becomes psyche.

-- psyche, STT.

## Books propose into any context module; he may review mind content

> the book is essentially always just a proposal. I wanted to come back a little bit and maybe retract the idea that I only review psyche. I could also review mind content. In the sense that if I'm asking a question and I want to be informed on something, then I'm asking for knowledge context to be assembled. ... Future flows that want to know about compaction could load this compaction skill from the knowledge type. ... We have different books now. Everything is a proposal to go into context modules.

-- psyche, STT.

## The unknown has its own type

> If there are things that are unclear, then it would land in a question type or an inquiry type. Maybe it's just called ignorance or uncertainty. Maybe uncertainty is better or ignorance. What we ignore, knowledge, what we know, or maybe something less direct and derogatory than ignorance, maybe something less offensive semantically.

-- psyche, STT.

## The hierarchy rules over contradictions

> I don't think I'll review compensation skills but I could read a book about compensation skills in general periodically to make sure that nothing in there is getting out of hand. Or we could do an audit ... Mind is above field and psyche is above mind. Anything in field that is contradicted by mind would be ruled over. The contradictions would be removed from the field context and so on, like for mind and psyche.

-- psyche, STT.

## A knowledge proposal is verified fact only, audited for truth

> If I reviewed a knowledge proposal I wouldn't have to read the whole thing, obviously, because everything in the knowledge proposal is just hard facts that have been written. They have been actually verified in code. That's all I want to see in a knowledge proposal. We could even audit them from time to time to make sure that they're both true and up to date or that there are no variations in practice from what is stated in the knowledge. In that case this could go into ignorance/inquiry/question or whatever we call the other type, the ignorance type.

-- psyche, STT.

## A contradiction between knowledge and vision calls for implementation, not deletion

> If we're talking about a knowledge module which documents how things work, then if it's contradicted by the vision (in the sense that what we want is not what we have), it would be incorrect to remove the documentation. Removing the documentation would just hide how things work currently from the future flows. ... where there's a contradiction, it indicates that some action needs to be taken. Meaning if there is a contradiction between the documentation and the vision, that means we have to bring the vision into implementation so that the current system is replaced by a better system. That system is then documented ... We can't just wholeheartedly delete documentation because the way the system works now, it doesn't behave the way we want it to behave.

-- psyche, STT.

## No data lives in the code

> Part of the book seems to be suggesting that we put a context module in the code, which goes 100% against my instruction that no data lives in the code.

-- psyche, STT.

## A correction asks for a fix in the right place, psyche preferred

> every time I correct something, it means that I want a proposal for a fix in the right place? Unless I specify where, then the machine's judgment will be used to decide where and what kind of fix should be made, preferring psyche, right?

-- psyche, STT.

## A question asks for knowledge; an explanation of what he wants is vision or intent

> if I have a question, obviously I want knowledge. If I'm explaining what I want, then I want vision or intent, depending on how broad the guide/instruction is.

-- psyche, STT.

## 2026-10-14 — context modules are super dense and precise; no statement in two modules

> I want to go hard on reprogramming the behavior for this in many layers: from the whole concept that the context is super important and the context modules must be super dense and precise (especially the system stuff like spirit and intent), and from the point of view of the book and how it's presented.
>
> If the spirit context is long I would refocus on honing in on the whole concept of how to handle the user interface, how to communicate better.

> This would be a repetition so no, we're not going to repeat the same thing in two skills. Let's not do that. Let's skill ourselves against that somewhere.

-- psyche, STT, relayed by the Psyche Core Tertiary; the second quote is a book comment.

## 2026-10-14 — dense modules is intent

> This is great. Actually this is even intent. This is intent. This is system prompt vision, which is intent.

-- psyche, STT, book comment on «Dense and visual» P2.

## 2026-10-14 — a subject he reviews or asks about has a module to hold it; modules have an ideal size

> In review, anything that's thought to be relevant for me to review, especially if I ask questions concerning a subject, means that there should be a skill on that topic or broader topic that will hold it (and doesn't have so much content that it can hold more), right? We have a sort of ideal context module size also.

> A knowledge review is not so much a proposal but I'm reviewing knowledge and it can be knowledge that already exists.

-- psyche, STT.

## 2026-10-14 — a proposal checks the higher modules first; a separator between type and name

> Make sure that whenever someone does a proposal they should make sure that the more authoritative context modules, like psyche and such, are not already stating the same thing or almost the same thing (where it is effectively the same).

> Could we use something like a colon to separate the type, like vision or knowledge, from the name, which then uses hyphens, just so we can visually better see where the type is and what the name is? We would then train the models to be aware of this in the skill names.

> I guess you could make a long-term vision proposal. It's not a different type of skill. It's just that it goes in the long term, in an appropriately named or annotated section that says this is a long-term vision aspect or a short-term ...

-- psyche, STT, book comments on «Communicating with the living».

## 2026-10-14 — Inquiry; approve, review, glance

Context: same comment on the vision-flow L24 line.

> Let's also make sure that we mention that a question is a type and how it should be presented, essentially also as a context module, because we have the inquiry. Call it an inquiry so that we match, right? We either have a vision proposal or psyche, in more general terms, and then a mind proposal, which is either knowledge or, not a proposal, a review, right?
>
> In mind's terms we review. I review the knowledge. I review the inquiry. When it comes to feel it's more like a situation or glance. We glance, right? I approve psyche, I review mine, and I glance at field.
>
> Field shows me metrics and sort of gives me a feel for what the context modules are mostly about. It brings forward to me sort of oddities, seeming inconsistencies, and potential problems, especially in terms of misunderstanding or misinterpreting or overinterpreting certain instructions or if they conflict with higher levels of authority context modules.

-- psyche, STT. Transcription corrected: "feel" → "[Field]"? kept as heard; "review mine" read as "review Mind".
Correction to the 2026-10-14 "Inquiry; approve, review, glance" entry: Transcription corrected: "feel" → "[Field]"; "I review mine" → "I review [Mind]".

## 2026-10-14 — Subagents as the same layer; a contextualizing subagent

Context: same speech to the Psyche Flow Secondary.

> Please check all this new psyche edition context psyche here. We also need to talk about how to context psyche properly and how main flow should probably call at least a lower-layered subagent. Let's define the basic subagents as the same kind of layer actually because the subagents are just non-main-flow variants, right? Unless they're specialized, create a table of all the most useful specialties right now and redefine how the subagents are using the same data, right?
>
> The main flow and the subflows are just the main flow and subagent, the main session and subagent version, and are essentially the same thing. They don't indirectly interact with the living so they don't need to have that. They probably just have asymmetrical training in respect to understanding what that means in any way from their point of view and why they're not directly interacting with the living. They're not logging the living but they might be judging.
>
> The skill: we should probably tell main flow to probably use a specialized subagent that we'll define here that specializes in helping to contextualize any raw living entry logging. Before the log there should probably be a subagent call. Let's define that subagent so it's really cheap. It basically is just saying, "contextualize this entry," and then it maybe just uses the first few and last words of the entry or something.

-- psyche, STT.

## 2026-10-14 — Compensation reviewed, positive; a small core

Context: spoken to the Psyche Flow Secondary; relayed for coordination. One sentence [sic] as spoken.

> Use compensation skills. Review all the compensation skills yourself with the subagent to make sure that nothing conflicts. All skills, but compensation skills need to keep getting, so make sure we remove in compensation skills. [sic]
>
> Try to remove negative guidance and come up with positive guidance on what we actually want. Avoid terms like "never" and "always" unless you're certain, which is why we also want System 1 models to make certainty calls on things. But make sure compensation skills are there, with some compensation core for a standard system prompt addition to all of the main flows. I don't know. The meta flow is a main flow or maybe more so, so let's review that.
>
> Some of it could even go in vision (vision core). Core would be the default for everything. Let's make this core standard in knowledge core and vision core. That part needs to be kept small and if it grows too big it has to be brought up.
>
> In compensation we have to be careful about harmful stuff. Knowledge will be pretty standard and vision, of course, is always reviewed by the living. Let's make sure the compensation skills are well adapted to and defaulted on everything in the core stuff: how not to message other aspects or aspects that are in low-power mode right now (like Fable), unless only the secondary psyche can ask permission and propose what Fable will be woken by and whether or not it'll be a new flow (before it can actually wake it up for any reason).

-- psyche, STT.

## A stateful, specified part of context

Relayed by Mind Core Secondary, 2026-10-14, within the stable/next Codex server request.

> The agent can use this as some kind of compensation context. We could even start having a more stateful part of the context infrastructure that can be changed, which is like a specified configuration. One of those is which [Codex] server we're using currently. ... [Tell] agents [what] to use. Let's say they're told that right now we need to use Next, right, because that's where the server we're using lives.

-- psyche, STT. Transcription corrected: "codec server" → "Codex server"; "Tail agents to use" → "Tell agents what to use".

## The directory names the type; no "skill" in our language

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-15 on «The Flow Nexus», Proposal 2, on the file name psyche-context/vision/flow-ethos.md.

> You see the name here. There's the direction [sic] directory called `vision` so it tells you which type of skill it is. You don't have to say it at the beginning of the skill file name. We don't need to say `skill` anywhere here in this repository or any of those repositories.
>
> `skill` doesn't even need to enter our language at that layer. The skill is just the interface on which we plug into and harness but we break it up more than just skills. For us they're all context modules and they have different types. All of those files in the `vision` folder are made into skills so they're all objects with different types.
>
> The fact that there are two folders means that either the code is bad in that it puts the source code for the same thing in two places, or the code is bad in that it doesn't make skills with all of the files. If it only makes skills from the `skill` directory, then we're missing skills in `harness`. All of this either goes into a system prompt or, in which case, it doesn't appear as a skill unless possibly eventually we might have modules that become skills if they're not in that particular system prompt. That's long term.

-- psyche, STT.
