Presentation.{ «Roles and subflows» }

How work is divided: what a main flow does, what it hands to subflows, how short a hand-off should be, what a role is, and how work passes from one layer's seats to the next. A main flow is the session that talks with you and judges. A subflow is a helper session it launches to do a piece of work. A layer is a rank, from Primary down to Quaternary, that sets how strong the model is.

## 1. What he wants

### A main flow judges; it does not do the work

A main flow keeps its own context clean. It decides, and subflows do the work.

> You can have some investigation subagents, right? You're a main flow. You don't do stuff. You use subflows to do it.

-- spoken to Field Sol, 18 September 2026

> but eventually all the sub-agents will themselves be flows, so that we have a fully asynchronous system, I think. Anyway, maybe some of them will still use sub-agents, but more trivially.

-- 3 October 2026

> the manager's context is gold. he has to keep his hands clean so he doesnt get oil and shit all over the blueprints

-- typed, 9 August 2026

When the way forward is unclear, the subflow asks back up. The main flow does not micromanage.

> I would rather train subagents to escalate back to their parents if the way to proceed forward isn't clear than for parents to try to micromanage their children and end up burning out, essentially doing more work than if they were just doing it themselves.

-- 9 August 2026

### What the main flow writes itself

The main flow writes its own log, records his words, and writes beads (small notes that track work). Everything else is done by subflows.

> Instead of saying, 'Reports, design documents, and landings are written by subflows,' you could say 'everything else also.'

-- typed, 3 September 2026

### A flow answers for its subflows

> what I meant is a flow is liable for its subflows. like a parent is liable for its child, so a flow cannot say "I didnt do it" if its subflow did, although it should be clear if asked to say "I did it through a subflow".

-- typed, 19 August 2026

### A tailor-made subflow for each kind of work

Each kind of recurring work gets its own subflow, built for that work. There should be many of them. The main flow does not name skills in a hand-off; it picks the right subflow.

> No, there should be a sub-agent specifically made for this. We're not naming skills. We're using the fucking agent that's tailor-made for this.

-- spoken, 3 October 2026

Such a subflow already knows almost everything its job needs.

> I want specialized subagent roles that already have almost everything they need to know to do certain things

-- typed, 3 October 2026

The subflow's own skills are hidden from the main flow. For the main flow, the subflow is the skill.

> Every flow is going to have its own view of the world because it can have more specialized skills that not everybody needs to see because they just use subagents. You know what I mean? For them the skill is the subagent. For the subagent the skill is a skill.

-- 24 September 2026

### The hand-off: one or two lines

A hand-off is one or two lines. Standing instructions belong in the subflow's definition, never repeated in each hand-off. The main flow does not copy file contents into a hand-off either.

> No, the main flow should not put anything in every brief. That's what subagent definitions are for. The subagent launch should require as few tokens as possible. Asking the main flow to repeat instructions is the dumbest idea of all of human history.

-- spoken, 3 October 2026

> When you say, 'Proposal lives in the conversation until the psyche approves, then a subflow lands it,' I would like you to explain the mechanism whereby it would be really stupid and inefficient for the main flow to just give the file content again in the subflows starting prompt.

-- typed, 3 September 2026

Proposed: a hand-off says what to act on and what to return. The definition says how, with which skills, under which rules, and on which model. Anything the hand-off leaves open goes back to the main flow as a question.

### Subflows become flows

In time, a subflow is a flow of its own. It runs on its own system prompt and does not keep the caller waiting. The caller holds a request number, and the answer comes back by message.

> if the subflow is independent and can reply to a successor of whoever it's supposed to respond to, then we have an asynchronous system. Plus, the subflows are going to be using their own system prompts because they're going to have different prompts.

-- 19 September 2026

> The requester doesn't hold anything. He gets a request ID assigned so he can ask for status again later if he wants to see what's going on. … If he's still the flow in charge when that flow is done, he'll get a message.

-- 19 September 2026

### The flow as a record with a role

A flow is a record, and role is one of its fields. Voice is one kind of role. The other roles are kinds of work: a system audit, live psyche voice interaction, an implementation, an implementer, a vision audit. Each is started with a prompt fitted to it.

> These are actually things that are better done with the prompt perfectly aligned, and then they're just running right out of the door.

-- 3 October 2026

> Well either it's living interactor, an implementer, or vision auditor, or it's living interaction, implementation, and vision audit. I think that I prefer the latest.

-- typed, book comment, 3 October 2026

A voice is an aspect (Psyche, Mind or Field) together with a layer (Primary, Secondary, Tertiary or Quaternary), as he wrote it in a book comment on 3 October 2026.

> Yeah let's make it four layers and we can make the quaternary layer be equivalent to Sonnet low effort and Luna low effort in the two different stacks.

-- typed, 3 October 2026

Proposed: each work role (implementation, vision audit, system audit, living interaction, and the ten missing kinds in part 2) is one tailor-made subflow definition. Its model follows from its layer.

### How work passes between the layers

The primary layer, Fable and Astra, works on design and ideas. Implementation goes down to the secondary layer, Opus, whose main flow coordinates Opus subflows to build and test it.

> Primary deals with designs and ideas, and he passes them on to secondary. Secondary then implements and tests, because if Fable passes out an implementation job, it's going to be Opus. He can just talk to the Opus main flow, who will then coordinate it with Opus sub-agents to implement it. Fable and [Astra] can just deal with design and ideas and concepts and send it down to secondary.

-- spoken, 3 October 2026

> Fable's job is to design and think not sweep the floor.

-- spoken, 26 September 2026

> Astra does the designing and the orchestrating and the big decisions and Sol does the implementation and the testing.

-- spoken, 26 September 2026

The primary layer is disturbed as little as possible. The layer beneath it coordinates.

> Let's try to diminish how much of the primary layer gets disturbed and use the layer underneath to coordinate the work. Use your own higher aspect, or a higher aspect or more primary aspect, to solve hard problems, like answering decisions and making rulings and judgments on things.

-- typed, 30 September 2026

Field talks to Mind at its own layer. Mind takes design questions to Psyche.

> There's sort of this hierarchy: fields talk to mind and only to its own level, right? Primary, secondary, tertiary, and they need to have a good reason, right? … When Mind contacts Psyche, it is when there is a need to get feedback on design, on choice, on judgment, and not just to talk.

-- spoken, 28 September 2026

Each layer may launch subflows only up to a set ceiling. Nobody launches a Fable or Astra subflow.

> On the Fable side, nobody ever launches a Fable subflow. … Opus can launch Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and Sonnet often, and Haiku to do small jobs.

-- typed, 18 September 2026

### Field keeps things working

> Make sure everything is deployed, fixed, and running well, because you're the field. You're there to keep things working.

-- spoken to Field Sol, 18 September 2026

> the field Luna should reap the old flows, archive them, respawn, and restart your own flow.

-- typed, 29 September 2026

## 2. What exists today

Witnessed. The eleven subflow definitions across the three harnesses are general: six sized by difficulty (read or write; trivial, ordinary or demanding), three more general ones on Codex, plus the tester and the book. None carries skills loaded in advance or a job's know-how. A two-week count by another subflow: 2,108 launches, a middle hand-off of about 1,660 characters, the longest about 26,000, nearly all opening with the same identity lines. Ten recurring kinds of work have no tailor-made subflow: sending a message, relaying his words, publishing books, searching his records, publishing files to shared history, launching flows, registering and retiring seats, landing skill lines, reading his comments on books, deploying and freeing disk space.

Supposed: no flow record has a role field yet, and subflows that are flows of their own do not run.

## 3. Questions

**1. Build the tailor-made subflows now, inside the harness's own subagent tool?** Say the first one is the sender of a single message.

> I can see already that we're going to get rid of the subagents facility and the harnesses because it puts them in a synchronous user interface. It locks both flows into one main flow

-- 19 September 2026

> How many custom sub-agents do we have? We should have a fucking shitload. If not, we should design a fucking shitload with Fable, design them, deploy them, and use them.

-- spoken, 3 October 2026

Answer 1 to build them now as harness definitions and move them later. Answer 2 to build them only once Flow can launch them as flows.

**2. Does a main flow still write its log, record his words and write beads itself?** Say he speaks and his words must be recorded.

> the main flow still writes its flow log, and it records the Psyche … the main flow can also write beads

-- typed, 3 September 2026

> That's why they're called main flows: they pass everything to a sub-agent

-- 3 October 2026

Answer 1 if the main flow keeps writing those itself. Answer 2 if recording his words goes to a tailor-made subflow too.

**3. Where does the detailed context for an implementation go?** Say an implementation is about to start.

> Get a subflow to get together the context first for the implementation, and then the implementation can just get that straight into its prompt, into the middle layer, like a very thorough implementation and detailed skill and vision of everything.

-- 14 September 2026

> and you just send them one or two lines, very extremely brief. An extremely fucking cheap subagent is what I want.

-- typed, 3 October 2026

Answer yes if the standing know-how lives in the implementer's definition, and the gathered context reaches it some other way than the hand-off.

**4. Is a role a kind of work, with a seat being a voice?** Say a flow is started to audit a vision.

> The only roles we have right now are 12fold. We have 3 aspects and 4 power levels.

-- 20 September 2026

> I think that the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice. The other variants are going to be all the other roles that we create: a system audit; live psyche voice interaction; an implementation; an implementer; a vision audit.

-- 3 October 2026

Answer yes if "role" is kept only for kinds of work, and a seat (one aspect and one layer) is a voice. Answer no to keep "role" for seats as well.
