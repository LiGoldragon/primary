# System psyche: hooks, events, and the meta harness

Delegated by Psyche Opus 7328f4 on 2026-10-01 (UTC). Gathered from `Intent/`, `Vision/`, `flows/*/vision/`, `flows/*/notion/`, `vision-raw/`, and the living's typed messages in Claude and Codex transcripts. All dates are covered, with most weight on 2026-09-24 to 2026-10-01. The living's words are quoted as the records hold them. Where a record corrected a transcription in brackets, the brackets are kept. Where a quote comes straight from a transcript and no log holds it, the entry says "transcript only".

Dates are the record's own, or the transcript timestamp in UTC. Records 7328f4 dates 2026-10-01 are UTC and fall on the living's evening of 30 September.

How to read the marks:
- **SETTLED**: the living ruled it, or it stands in distilled Vision or Intent, and nothing later reopens it.
- **OPEN**: the direction is given, but the mechanism, shape or scope is still undecided, or the living framed it as a question.
- **CORRECTS**: later words that correct earlier ones. Both are kept.
- **TENSION**: two records point different ways and no ruling settles it. This flow does not resolve these.

No credential, pairing code or token is reproduced here.

## Intent

All of these are distilled and approved.

**Startup prompt** (`Intent/startupPrompt.md`)
> A flow starts from one startup prompt: a single block of text. Some skills are startup skills: they are given to particular flows at their start and never to their subflows, and the harness is configured so the model cannot see or load them itself. Each harness has a facility for this, and that facility is what is used. A startup skill enters through the startup prompt; if one was left out, it is put in afterward, as a repair of the startup prompt.

**Psyche interaction** (`Intent/psycheInteraction.md`)
> Every main flow interacts with the psyche, so every main flow loads psyche-interraction and relays what it hears to a Psyche flow.

**Models** (`Intent/models.md`)
> Capability comes from choosing a better model, not from raising a model's effort setting. ... Harness calls go out at medium effort by default.

**Context** (`Intent/context.md`)
> A value at any layer carries the context it makes sense in, and no layer carries a fact that belongs to another.

**Anatomy** (`Intent/anatomy.md`)
> Code is written anatomically and directly: the logic is read through the ontology of the trait system. Datom and Ethos Zero are the parts that must be solid.

**Data** (`Intent/data.md`)
> Everything is data. Code is data: a type is declared with code, so a type is data; a trait is data; an impl is data.

## Vision

### 1. An event-based infrastructure from hooks: a marked transcript message becomes an action

**Distilled Vision**, `Vision/nexus.md`: **SETTLED**
> ## Observation by subscription
> State is observed by subscription: the subscriber receives the state on open, then each change as it happens.
>
> ## Polling is forbidden
> Polling is forbidden; a correct system goes quiet when nothing changes.

**2026-10-01, heard by 7328f4, typed** (`flows/7328f4/vision/hooks.md`; transcript 7328f4ba line 898)
> Let's focus on hooks and using hooks to do an event-based infrastructure in terms of sending notifications that there's a certain kind of message that has landed in the transcript somewhere. Maybe that means it needs to be made into a book, or maybe it means that there's an update to an existing book.
> We can do all of this without requiring the flow to make tool calls because the hook will just pick up the output and create actions based on that. I'm really excited by that.

**2026-09-30, heard by 7328f4, typed** (`flows/7328f4/vision/hooks.md`)
> I see the hooks. I really want to plug into the hooks. I looked at [Herdr] this morning and I see that it supports showing me if a session is busy: it has a little red dot. If the session is finished, it has another kind of dot, but I haven't read it. If I've read it, it has another kind of dot. That means there's some kind of interface there or hooks, or what's happening.

**2026-09-29, heard by c64ee3, STT** (`flows/c64ee3/vision/hooks.md`, c64ee3-6)
> Then we would use that hook to know that something that a model just made needs to be made into an artifact. And we can have more intricate artifact building by better models that gather even more context and make a more elaborate report with more [psyche] verbatims, or distilled vision, intent, spirit, and even some notion to go on to possible venues. Let's make all of this into a series of skill testing, basically like a pipeline.

**2026-09-28, heard by 8904b1, STT** (`flows/8904b1/vision/presentation.md`, 8904b1-32)
> I would like to design something efficient and then eventually we'll turn that into some kind of hook that just gets triggered when some kind of event comes out of the harness. What kind of events?
>
> Also let's get somebody to look at what we can hook into the harness instead. I see a world where everything is a hook and an event and triggers something so that it's not really the decision of "Do I spawn a subagent?" It's like, "I would like a subagent." Here's the vision, right? Or here's how it would look. The flow would just give its final answer and eventually everything will be datom-specified, like an ethos. It'll come out with this final answer that implies that some subagents could be called on certain things. It'll be up to some other mechanism, probably some kind of token accounting mechanism, to decide if subagents are launched, which ones, and how much, which model, and how much effort they're each going to be.

**2026-09-26, heard by b7da5d, typed** (`flows/b7da5d/vision/mainFlowRefreshAndRoles.md`)
> ... voice is really just a relay: a quick inventory, a quick "let's see what there is to do with this request" kind of response, taking it to the right, sending a message basically to another flow, or there's a hook that triggers an outside flow to actually just read the transcript. It's even faster because the agent doesn't have to message anyone. It knows that an agent is going to read what it says and that's actually the flow I want to go towards.

**2026-09-19, heard by b81560, direct** (`flows/b81560/vision/operational-hooksAsEventSource.md`)
> Yeah, and the way we hook into the harness: we put hooks to give us event updates with some data when the hooks get triggered in the harness.

**2026-09-19, heard by b81560, direct** (`flows/b81560/vision/operational-retiredResponseAndReaping.md`; transcript b8156034 line 695)
> We watch all the final responses. We put hooks in, and these create automated messaging. It might just send them, not even the whole payload. It might only send the response if it's only a certain size or whatever. We can filter on that.

**2026-09-18, typed to c7128c** (transcript c7128cb2 line 614; logged under `flows/c7128c/vision/visualization.md`)
> So somehow, whenever a major model ends its turn, I would like for a hook to run a job to create a visualization of that last response with a proper vectorization of the flowcharts.

**2026-09-18, heard by b05237** (`flows/b05237/vision/operational-reportWatcherAndIllustrator.md`)
> One hook checks for the report and then finds that it's there and makes a backup of it, maybe into the log. The flow archive is what it is, so he creates the flow archive of it and marks it as what it is: either a main flow or a subflow report, and then can send a job to the most qualified flow to illustrate it.

**2026-09-15, heard by 840e42, typed** (transcript 840e42bb line 432; transcript only)
> And make the flow be aware of hooks like that. Let's hook up flow to the hooks of the harness as notifications for everything. If the agent comments, flow gets notified, and then it can make a decision on that.

**2026-09-15, heard by 05c604, typed** (`flows/05c604/vision/messages.md`)
> It could be set up so that when it's done, there's a hook that runs. We want to start taking control of the flow more, and it could send it automatically as a message back to the primary Claude or the corresponding Claude of that cluster, and potentially even more endpoints.

**Status.** The direction is **SETTLED**: hooks and events, no polling, and no tool call needed from the flow. It has been repeated from 09-15 to 10-01 and is backed by distilled Vision. The mechanism is **OPEN**: which harness events, how a "marked" message is recognized (see Notion: begin and end markers), and where the hook reports (Flow, per the 09-15 and 09-19 words).

### 2. Turn state of a seat by hooks; no polling; a registry of what polls

**2026-09-30, heard by 7328f4, STT** (`flows/7328f4/vision/polling.md`)
> I've reset Codex and we need to also start working on the hook/[Herdr] functionality for getting the state of what's happening in a flow as cheaply as possible, with no polling. We really wanted to [de-emphasize] polling and if we do poll it would be a really long period and it'll be for something really important. I need to have a periodic report on any system that's polling so that it doesn't run out from under me.
>
> Even if it's stateful, I've also been having problems with stateful services that we're polling that I kind of asked for but we don't want to forget about them. We need some kind of registry of polling systems somewhere. That would be a field thing.

The transcript (7328f4ba line 552) reads "emphasize polling". The log's "[de-emphasize]" is that flow's reading and is not confirmed.

**2026-09-29, Codex (d5b96b), typed** (`flows/d5b96b/notion/session-reaping.md`, held as notion; transcript rollout-2026-09-29T11-20-29 line 105)
> I'd like to talk about a system with Fable to use hooks so that we can know when a session is finished so that it can be reaped.

**2026-09-19, relayed verbatim by cf3553** (`flows/b81560/vision/operational-reapingOnRefreshAndFlowEndHook.md`; `flows/cf3553/vision/operational-finalResponseLifecycleHook.md`)
> We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it. In the last response, possibly we should also send that to Flow, and then Flow would send it to the reaping agent to decide if that's the end of Flow and if it should be reaped. The Flow nexus should also be aware if there's a successor already up, and it could take a screenshot, even of that, and send it to the reaper to judge if the new Flow is up.

**2026-09-23, heard by d8df70, typed** (transcript d8df703d line 776; transcript only)
> If a process goes missing we could have a hook there in the system. If one of the processes ends prematurely from us unregistering it through our exit hook, then you just use the process going out as the unregistry hook.

**2026-09-18, observed in 3b1574 and relayed by 33ba2b** (`flows/b05237/vision/operational-fieldLunaWatcherAndArchiving.md`)
> Field Luna is going to watch and have a timer, or maybe you can think of some hook that he could use. He'll be watching for sessions to be archived and put taken out of herder, so we don't accumulate these ghost sessions

**Status.** "No polling" is **SETTLED** (distilled Vision). A long-period poll for "something really important" is allowed, and a polling registry with periodic reports is a new ruling, **SETTLED** but not yet built. How turn state is read (Herdr's busy, finished-unread and read dots; Claude and Codex hook events) is **OPEN**: the living asked for research.

### 3. Restarting flows: refresh, handover, succession

**2026-10-01, heard by 7328f4, typed** (`flows/7328f4/vision/metaHarness.md`)
> The most important thing we need now is to improve the meta harness: how easy it is to restart flows, how easy it is to deploy skills, and how much it becomes the implementation that we want with the correctness and the anatomy that we want.

**2026-09-30, page comment, STT** (`flows/7328f4/vision/hooks.md`; relayed to `flows/b666e7/vision/hook.md`)
> Essentially we want to avoid polling, which means we're going to make this hook-based. When an order comes in, this will be controlled by Flow obviously. When that order comes in, we need to upgrade the harness. Then sessions can be reloaded in the new harness one at a time as they go idle.
>
> As soon as the session goes idle, the hook kicks in. It gets locked for the next order tab update [sic], which essentially locks it from getting sync messages, right? It would wait until it stops because the restart will happen and then the message will just come through. This will tie into how context size will essentially start triggering the unwind. Then we'll have a whole way of passing the right transcript, either passing it over or selecting what transcript to pass depending on what the next flow will specialize in.

**2026-09-30, to c64ee3, typed** (transcript c64ee3f5 line 1672; transcript only)
> Let's agree on whether all of the seats will restart, whether we refresh all the flows, or whether we'll resume some of them from the newer harness. I'll need to get remote access to the new harness server before we rotate.

**2026-09-29, to 183ae0, typed** (transcript 183ae001 line 1280; transcript only)
> Can you refer to your own transcript and tell him what you want passed in as a user prompt again? This has been missed now for the last couple of days. My new flows are not getting a nice fat user prompt for context. They're told to read files, which yields lower-quality context.

**2026-09-28, page comment** (`flows/8904b1/vision/skills.md`, 8904b1-31)
> Until we have a proper flow tool to respawn a flow easily, the skill is not very useful. Although that's the goal, I eventually don't want flows to compact because compacting is a short-term remedy to a problem that requires a much more refined approach to reorganize the context in a new flow.

**2026-09-26, to b7da5d, typed** (`flows/b7da5d/vision/refreshHooks.md`; also in `f5a74e`, `b860be`, `e167d8`)
> We need some way to automate the refresh call. When a model reaches a certain context window, whoever is in charge of refreshing should get a message that some flow needs to be refreshed. I guess the flow itself needs to know so that it can create a handover response. At that point that same hook system picks up the final response and essentially locks the messages from being sent over there immediately.
>
> If there are sub-agents still working, it's okay. I guess we could just notify the new flow of what happens after they return, and/or what they returned or whatever. ... We're not going there yet. I'm just talking about this hook principle we can use in many ways like that.

**2026-09-26, to 93ba9f, STT** (`flows/93ba9f/vision/flowLaunching.md`; `flows/e71dab/vision/launchGovernance.md`)
> Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped. ... We should have a list of flows all programmed with their datom configuration. That's one of the inputs it gets, fed into a new flow, plus addendum things that are added into the prompt from files

> Give everybody the authority to come down on things like the high-effort model and make sure these flows are stopped and that all of their context is given to whoever carries the torch for them. If there isn't one then they have to restart a new flow. Let's keep field Luna on that. She has all the authority to stop and start flows. As long as she's told, she doesn't have the authority to decide.

**2026-09-26, to 93ba9f** (`flows/93ba9f/vision/automation.md`; `flows/e71dab/vision/paneLifecycle.md`)
> Nothing is up to me. Everything is being automated. ... I'm not going to close or start anything or type anything anywhere ever. No one is. The user interface is going to be Unity and these harnesses are just going to be a background mechanism.

> Let's just teach the system to close panes, to close sessions itself.

**2026-09-24, page comments** (`flows/d8df70/vision/flowLifecycle.md`, `flows/d8df70/vision/flowTool.md`, `flows/836818/vision/flowNexus.md`)
> A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived.

> The old flow is closed when it has a replacement, at which point it shouldn't be reachable anymore because the lock took that route away for the replacement. In fact it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. ... In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

> Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.

**2026-09-24, to Mind Astra 47764b** (`flows/e51411/vision/refresh.md`)
> The handoff is in the transcript and the tool gets it from that with the help of the AI. It locates the block and everything and logs that as the thing that the tool then uses to get the text from the transcript. The tool gets the right block of text because it has the right reference so we don't need to make a copy of anything. It just fetches it programmatically.

> I would like, eventually, the flows to just automatically refresh and we're going to get into the nitty-gritty of making the initial call way more efficient and concise by changing the system prompt.

> Why can't anybody deploy anyone? What if we only have one flow, and he has to be able to redeploy everyone? It's a decentralized structure. It can respawn itself from any point.

**2026-09-25, to e51411** (`flows/e51411/vision/refresh.md`, `flows/88475f/vision/flow.md`)
> If we can't refresh the flow, we can just compact and then reload the main skills we want and give it a new prompt.

> Yeah well, if his context is old and he's not going to be able to do a good job, when we start something like that we should start on a fresh flow with lots of related training.

**2026-09-24, launch** (`flows/e51411/vision/launch.md`)
> There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

> We should not make it the subflow's job to claim an ID. That should be done for the flow as it started. There's no reason. This could easily be done by code.

**2026-09-24, psyche injection** (`flows/752e0f/vision/psycheInjection.md`)
> Main flow, priority somehow: can you get all my psyche together and then inject it in a new flow at the user level so it understands what I want and hasn't just read it from the bottom context layer?

> Give him the raw that's relevant and recent

**2026-09-18, to 33ba2b** (`flows/33ba2b/vision/operational-fieldRefreshSuccession.md`)
> The terminology is field Sol - of meaning: descendant of, and then the ID of your ancestor.

**2026-09-17** (`flows/9993b5/vision/flowRestart.md`, `transparentRefresh.md`, `easyFlowDispatch.md`)
> It just needs to be a command sent to Flow, and if the flow ID matches the flow's provenance, then we can restart it. That's all the authority you need.

> The whole refreshing of the flow is going to happen a lot more transparently, essentially, or without the user having to notice, really.

> Flow needs to be really easy to restart a Flow and to start a new one. Let's predefine them so that there's basically no argument to give except a small description of the goal

**Distilled Vision**, `Vision/flowNexus.md`: **SETTLED**
> A session cannot be named for what it will become, because nothing is known about it when it is created. Its ancestor is known exactly, so the ancestor is the name.

> Reaping belongs to the refresh event, not to a later sweep. A refreshed flow takes the replaced end out of receiving messages, so a dead end is never left registered and addressable.

**Status.** These parts are **SETTLED**:
- the handover lives in the transcript and is fetched by reference;
- the replacement takes the route by lock, and the old flow is closed and archived;
- any flow may call Flow, which checks the calling process;
- a launch is one startup prompt, with a fat user-level injection of recent raw psyche;
- reaping belongs to the refresh;
- flows are configured from datom.

The hook-driven cascade (upgrade the harness, then reload each seat as it goes idle, with a lock and held messages) is **SETTLED in direction**. The living himself says the detail "will take shape as the implementation gets more sophisticated", so its detail is **OPEN**. Also **OPEN**: when context size triggers the unwind; how the transcript is chosen for a specialized successor; and whether seats restart, refresh or resume (asked on 09-30 and partly answered on 10-01, see §4).

### 4. Harness migration and rotation (Codex next/stable)

**2026-10-01, heard by 7328f4, typed** (`flows/7328f4/vision/seats.md`)
> Actually, I would really like to migrate Codex to the new harness. Maybe we can even resume the sessions on a new server so that it has Sol 6.1. Unless the context is old, then we should just start a new flow for them and reparse the old one. Let's get everything sort of revitalized.

**2026-09-30, Codex (d5b96b thread), typed** (transcript rollout-2026-09-29T11-20-29 lines 4095–4151; transcript only, no psyche log found)
> Oh well, here's the protocol, right? The stable becomes the next once all the flows have moved onto the next socket. If all the flows are on the next socket now, next can become stable, and then we can put the next version on next.

> This becomes a compensational skill.

> I mean compensation codex. Because it's a principle we can apply to more than one thing, we can maybe mention it in a compensation codex, but I think it's better just like compensation update. Or something like that.

> Maybe we can get the short version of the hash of the version of Codex that we're using for it, so that each socket will have a different name. That way, we can move the next to the stable without changing the socket name, so it doesn't break any of the sessions.
>
> Maybe we can do that in a hacky way, with a bunch of comments on how we're going to fix it next time. The current next can just stay called whatever it is, and the next next can have this new hash-suffixed version socket. That way, we don't break our current sessions.

**2026-09-29, Codex (Mind Astra 6f51ad), typed** (transcript rollout-2026-09-28T10-23-01 line 9848; the Clojure part is logged in `flows/6f51ad/notion/clojure.md`)
> We should automate some stuff. We should talk about that, about automating these codex and Claude updates. I'm sure we could find the pattern.

**Status.** The rotation protocol (stable becomes next once every flow has moved; a hash-suffixed socket name) is **SETTLED** as spoken, and he wants it to become a compensation skill. The skill name is **OPEN** ("compensation update" leaning). Resume-or-new-flow by context age is **SETTLED** (10-01). Automating Codex and Claude updates is **OPEN**.

### 5. Deploying skills: typed skills, skill repositories, the Curriculum Nexus

**2026-09-29, heard by 183ae0, typed** (`flows/183ae0/vision/skills.md`)
> The skills are not supposed to be in the curriculum anymore. The curriculum is just the executable source code. Now we need three skill repos so we need to finish designing that or we just scrap the whole idea of deploying skills for now. I don't know.

> No the skills will be typed. Just copying the directory name is dirty. We make a nexus that has a fully typed specification for the different types of inputs that it can take. Let's do the anatomy of that.

> I mean, to edit the skill or create one, the models don't seem to understand that distilled vision is automatically a skill. There's no more separation. We have to make that clear: that vision is automatically a skill, because otherwise it's not very useful. It's just a file. My vision is what should imbue some of the most important context of the model.

> I would like [agents] to be able to edit skills that pertain to them easily. That's why the three repos. Each of these repos is actually where I think we should keep the distilled part separate. We could have another repo for psyche logs, mind logs, and field logs for the actual logs.

**2026-09-29, heard by c64ee3, STT, CORRECTS the rebuild premise** (`flows/c64ee3/vision/skills.md`, c64ee3-1)
> It's not. Those weren't my words. I was told that this is how it works by Opus so they're not my words. I'm just repeating what he said.

This answers the 183ae0 entries "You see the skills can't be with the Rust code because then we rebuild the whole executable every time we change a skill" and "It is too bad that changing any skill requires recompiling the entire Rust binary". Their premise is withdrawn. The wish to keep skills apart from the Rust stands.

**2026-09-29, heard by c64ee3, STT** (c64ee3-8, c64ee3-17)
> Bring the new skill stack with the three different source repos, each for a different aspect to be in charge of, with the corresponding logs repos (psyche logs, mind logs, and field logs) to be created and to start being used in this new skill-building pipeline that prefixes skills based on the payload itself.
>
> All of the skills are loaded. We're just going to load them into the curriculum database with their different variables being either psyche, mind, or field, and then with the sub-variants being each different, where psyche has vision, intent, and even spirit.

> Let's use ethos to specify all of this. Each variant then eventually has a struct, probably, that holds the skill or the struct has the description, like the text of the skill, as one of its fields, and then it has all the other metadata, like the title, the description, whether it is user- or agent-visible, and whatever else, like dependencies and stuff like that. The dependencies are just simply in this registry. We have to make a whole registry of everything because a vision can only depend on other vision or intent. ... Operation can depend on vision or anything higher and this goes all the way down: documentation, operation, and then whatever the hierarchy is in the field, which is trial at the bottom, and I forgot the other one.

**2026-09-28, heard by 8904b1** (`flows/8904b1/vision/skills.md`, `anatomy.md`)
> We need one or more repos to hold the skill texts themselves and a schema to define their type, maybe in a datom file that is fed in through the CLI, which can translate it into a signal to the skill generator. Whatever are we calling the nexus for skill generation?

> Field would be told that he's in charge of the field skills. If he wants to change, if he has a suggestion or a need for a change in any other skill, he has to message the corresponding aspect so that that aspect can investigate and analyze the merits of the suggestion. If that suggestion is toward Psyche, then obviously Psyche is going to have to bring it up to the Living.

> Well eventually the skills will live in a daemon not in a Git repo anymore. That's why it's a daemon.

> We need to make a nexus to deploy skills. Why should it be right? Is it curriculum nexus?
>
> You just give it a new bunch, maybe a repo, or a target and a destination and then it just generates the skills and changes the ones that have the same name. That sounds simple to me. ... I think I've been underestimating the value of simple, which is why now we're stuck in mud up to our necks.

> I want one workspace. I want everybody, and I want the skills to be fucking recommitted when they're changed and regenerated.

> Well the madness is letting agents edit skills.

> Approving a skill edit: a gold skill changes only on your word. Yes. ... Operation skills can be deployed when, if on my word ... The primary mind has to review them ... I want to point out that operation and documentation would be for Mind and tests and compensation would be for field. ... We would prefix all the skills and then we would know what all skills are.

> And we're going to use a trial prefix so that you understand the concept after that.

On "Every skill prefixed by the generator" (page comment, 8904b1-42):
> Yeah that's a good minimum viable product.

**2026-09-24, heard by 26c50c, typed** (`flows/26c50c/vision/curriculum.md`)
> We're going to have different types. We're going to have the vision type so you can make curriculum. One of its queries is going to be by type: generate or regenerate the skills in the target repository

> No but that's what I mean. All the skills are going to be of one type. That's how we're moving. There's just going to be a repository of a certain type. The type is assigned to the repo. It's centrally controlled: which type comes from which repositories.

**2026-09-24, heard by 752e0f, typed** (`flows/752e0f/vision/curriculum.md`)
> Curriculum takes different repositories that have special files that we recognize: Nix files, obviously. Our entry point, but we can also have our own Datom syntax right there, like config.datom, right? We create our own ethos object for that in curriculum ... You should create a kind of library, a nexus library, to handle all of this: rebuilding, regenerating the ethos, and rebuilding the CLI when you have a change of dependencies or the ethos changes in the source signal.

**2026-09-17, heard by 9993b5 and 108ab0, typed** (`flows/9993b5/vision/curriculumNexus.md`; `flows/108ab0/vision/operational-curriculumAsModuleSystem.md`, `operational-curriculumSkillsRepo.md`)
> Basically, this is where we want to go towards curriculum being a nexus and taking it in so it can be... We take control of that state, and we can reset it through Nix, of course, or repopulate it, reseed it from Nix. There's a reseed service part that recreates a basic seeded curriculum.

> if curriculum is a nexus, we can't have any data there because it's going to keep rebuilding it. We need curriculum data. It can just be given. It's like a manifest that gives it a bunch of paths with some file names, Markdown, and gives the type of each.

**Distilled Vision**, `Vision/flowNexus.md` and `Vision/psyche.md`: **SETTLED**
> Every skill lives outside it, the basic skills included, so that a change to a skill causes no Nix rebuild.

> Operational vision skills use the `operational-` prefix and support faster iteration with an overview to the living. Testing skills use `testing-`. Pure vision skills use neither prefix.

**Status.** These are **SETTLED**:
- skills live outside the executable code;
- skills are typed (no directory-name hack);
- distilled vision is a skill;
- a Curriculum Nexus holds the skills as state, reseeded from Nix;
- golden (vision) skills change only on the living's word;
- every aspect owns its own skills and routes change requests to the owning aspect;
- a generator that prefixes every skill is accepted as the minimum viable product.

These are **OPEN**:
- whether there are three per-aspect repos or skill deployment is scrapped for now ("I don't know");
- how a datom payload drawn from several places reaches the Nexus (Notion);
- the full prefix taxonomy (the living is "torn", and the trial kind and one Field kind are unnamed).

**TENSION (a).** On where a skill's type sits: 09-24 "The type is assigned to the repo" (a correction of a per-skill proposal), against 09-29 "prefixes skills based on the payload itself" and "Each variant then eventually has a struct ... with all the other metadata". The earlier 09-17 wording put the type in the Markdown header.

**TENSION (b).** On prefixes: distilled `Vision/psyche.md` says "Pure vision skills use neither prefix", against 09-28 "I think we should prefix all the skills but maybe not" and "We would prefix all the skills and then we would know what all skills are."

### 6. Books made from a marked presentation in the transcript

**2026-09-30, heard by 7328f4, typed** (`flows/7328f4/vision/books.md`)
> We'll ask the primary aspects, the primary seats, when they do something: their eventual output is a response in their transcript that they marked with a beginning and an end as the object that we wanted. They can tell the tertiary layer, or whatever is available, the secondary, to get that turned into the result of their presentation and then we can turn that into a book.
>
> The primary layer's most important work is their view of something. The presentation is what they're there for. That's their main output and then we can turn that into books or a new version of a book and we always just make a new one. We pass that down to Sonnet to look at and compare it with the psyche, a little bit if he can, as a double or triple check, and then make a book.
>
> ... It's up to the flow itself to make sure that the presentation is simple. That's the skill. Sonnet should sort of concentrate on knowing the psyche because that's what his aspect is. He could put notes that compare. They're specially colored and they bring any kind of agreement, a strong agreement or strong disagreement, to the front in a small note in reference to a psyche and how old the psyche is.

> Create a more direct, visual, and simple presentation of the most central simple concepts that we need to investigate and resolve, presented very simply and with only a few of them. I don't want to be showered with too much data. ... I want the next generation of the book skill to be changed so that this is emphasized. We'll do another generation of 3 to 6 books, or maybe 1 to 6 books, but I think probably around 3, or 1 for each aspect.

**2026-09-29, heard by c64ee3, STT** (`flows/c64ee3/vision/presentation.md`, `recording.md`, `vocabulary.md`)
> Can you link to your transcript so you would print the presentation [mid-turn] because we are not even concerned anymore about putting the most important part of your output in your final answer? We're moving away from that or we're not concerned with it.
>
> You could call on either the subagent or the other main flow and give them very minimal information, just enough for them to find that. If you can't give them a link you could just describe the first few and the last few words or the first bit of string and the last bit of string

> Whatever you print out, don't reprint it.

> Booklet or book, those are the terms we use. ... let's make all of the skill say that if I say "page" then I mean a book and that's that.

**2026-09-28, heard by 8904b1** (`flows/8904b1/vision/skills.md` 8904b1-31; `presentation.md` 8904b1-34, -36, -45)
> I want the call to cost the main flow that calls it as little as possible so that it knows everything. It doesn't even need the markdown. It should be able to get it from the transcript. ... It just says, "In my transcript I said something that I want to make into a book."

> It would just be a single sub-agent with almost no arguments, no prompt made by the main flow, and then it would just make a book or a page, whatever, from the transcript.

> The thing I need is not in the final answer. That's my whole point. We need to make a page from everything, where contradiction is won by the most recent output or input or whatever.

> Would there be a way to resume a book update sub-agent so that it would know from where, which part of the transcript to consider to modify the page? Giving someone an HTML for context is really bad.

**2026-09-17, heard by 9993b5** (`flows/9993b5/vision/transcriptSelfReference.md`, `transcriptOverFiles.md`)
> How much can they tell about pointing to a thing they said without saying it again, so that they can refer to their own transcript efficiently in telling a tool that this is the input for whatever?

> Actually, the report becomes everything is in the transcript. We don't want to make files anymore.

**Status.** These are **SETTLED**:
- the primary's marked presentation in its transcript is its main output;
- a lower tier turns it into a book, and a new version each time;
- Sonnet compares it with the psyche in coloured notes;
- there are few, simple books;
- the transcript is the source and nothing is reprinted;
- "book" is the word.

How the marker is written and recognized, and the hook that fires on it, are **OPEN** (see §1 and the Notion section).

**CORRECTS.** 09-29 "we are not even concerned anymore about putting the most important part of your output in your final answer" moves away from the final-response-as-report of 09-18 ("your final response is your report with your visual flowcharts") and 09-24 ("The handoff should be your last response, right? It might not be your last but it's in one of your last responses").

### 7. Seats: who disturbs whom

**2026-09-30, heard by 7328f4, typed** (`flows/7328f4/vision/seats.md`, `Fable.md`)
> No we should try to avoid talking to Fable.

> No we're going to limit the communication to Fable and Astra also. Let's try to diminish how much of the primary layer gets disturbed and use the layer underneath to coordinate the work. Use your own higher aspect, or a higher aspect or more primary aspect, to solve hard problems, like answering decisions and making rulings and judgments on things. That's the vision.

**2026-09-29, Codex, typed** (transcript rollout-2026-09-28T15-00-37 line 3840)
> Anyway, let Fable make the decision on what to do. Send him everything verbatim

**2026-09-28, heard by c02c0d** (`flows/c02c0d/vision/seats.md`, `skills.md`)
> We should really minimize how much Fable is talked to because it's the most expensive model.

> There's sort of this hierarchy: fields talk to mind and only to its own level, right? Primary, secondary, tertiary, and they need to have a good reason, right? ... When Mind contacts Psyche, it is when there is a need to get feedback on design, on choice, on judgment, and not just to talk.

> Let's just stick to a skill that is not agent-visible and that is loaded manually for every aspect.

**2026-09-28, heard by 183ae0** (`flows/183ae0/vision/seats.md`)
> They don't need to tell everybody; they just need to log it.

**2026-09-26, heard by 93ba9f** (`flows/93ba9f/vision/primarySeats.md`)
> We should make it clear that models should refrain from talking to the primary models. They should usually aggregate some thoughts together and investigate before talking to it. It's like a preparation ritual to talk to the high priest.

**Status.** **SETTLED**, and repeated three times. **CORRECTS**: 09-30 "No we should try to avoid talking to Fable" answers whether 09-29 "Send him everything verbatim" lifted the 09-28 ruling. It did not.

**TENSION (c).** On the same day (09-30 17:10, page comment, §8) the living asked for an ethos package to go "to Fable on a new flow" and for Fable and Astra to agree. That may be the sanctioned case: a fresh flow for a hard ruling, which matches "use ... a more primary aspect, to solve hard problems". It is not confirmed.

### 8. Ethos shape

**2026-09-30, page comment, STT** (`flows/7328f4/vision/ethos.md`)
> On the syntax we don't want to do something like there's too much indirection. I already said, for example, if you have a skill type and one of the variants is psyche, that psyche object: the rule of ethos is that if there's another type called psyche with the same name, that's what data that variant carries. You don't need to write psyche type.
>
> We don't really need something like the collection because submit is too short. Using just an indirection to put a simple struct there, I think, is bad form. I think we can just have the definition of that struct be what comes right after the submit. The submit variant has, for data, a struct and its name will just be derived deterministically by ethos. I think that, for a variant, you can have a variant and a struct name be the same thing so I don't even think that's a problem.
>
> When we say stuff like skill name, I think it should just be name. Maybe not. Maybe that's appropriate. ...
>
> Like I said don't use psyche type. Just type psyche. ... I want all of [the vision] to be edited to take that into account. Let's put a package together for this and give it to Fable on a new flow to help design this properly so he can send sub-agents to look at the current state and make his design proposition. Astra makes his and then we'll combine them. Fable and Astra Mind will agree after they've done their own design proposal on what it should actually look like. And then Mindester [sic] will implement it on a fresh flow.

> If you're only listing types then you can use the `types` type. We should make sure that that's in the code, in the spec, and in the vision anyway.

**Distilled Vision**, `Vision/ethos.md`: **SETTLED**
> ## A variant named as a defined type carries that type
> When a variant's name is a type already defined in the library, that type is the data the variant carries. Nothing further is written.

> ## A variant may declare its payload inline
> Instead of naming a defined type, a variant may declare what it carries in place: a vector, a struct, or an enum, each a full type with a derived name, recursively.

> Any repetition in ethos syntax is an implementation failure. Ethos aims to be the most terse, non-repetitive syntax ever made.

**2026-09-29, heard by c64ee3, STT** (`flows/c64ee3/vision/ethos.md`)
> Whenever ethos is written, this block is not ethos because it's lacking a type so it's invalid. Ethos always has to be correctly written; otherwise it's out of context, which means we don't know what it is.

> The step to change the data is the same as the edit that's made to the source code because, in ethos, we're going to specify ethos in its own ethos language. The ethos language will then have its structure for how it stores itself in the nexus, so those will be ethos versions. ... eventually ethos would just compile to a full Rust program.

**2026-09-26, heard by 93ba9f, artifact comment** (`flows/93ba9f/vision/ethosNames.md`)
> Ultimately everything becomes a type because everything is a variant of a set. ... There are these open-ended variants, which we call names. ... The key-value map is out of our syntax because it's really just a poorly specified struct

**2026-09-26, heard by 93ba9f, STT** (`flows/93ba9f/vision/flowLaunching.md`)
> a lot of this data that you're spreading over this single [struct] actually is data that belongs in the data portion of a variant. When you're talking about the effort, there are different effort levels for different models so it's a property, the data of the model variant.

**2026-09-25, to e51411** (`flows/e51411/vision/ethos.md`, `systemPrompt.md`)
> But within a few months I would like to develop Ethos to the point where we can just write the whole program directly in Ethos.

> This is our go-to language. We want to make that central: these skills, this Ethos, and this Datom way of thinking about data, data specification, and data itself in an instance aspect.

**2026-09-24, heard by 26c50c** (`flows/26c50c/vision/ethos.md`)
> That way the Nexus doesn't do the string conversion but the CLI does and eventually the user interface will have all of that conversion-to-string logic compiled in.

**Status.** These are **SETTLED** (distilled and re-ruled 09-30):
- a variant named as a type carries it;
- an inline payload has a derived name, with no indirection struct;
- no `psyche type` is written, only `type psyche`;
- a written block must be whole, valid ethos;
- the Nexus carries no text conversion.

The living reports that the *implementation* still violates these ("I feel like I've been fixing for days"). These are **OPEN**:
- whether to write `skill name` or plain `name`;
- the `types` type (asked to be added to code, spec and vision);
- the redesign process: Fable and Astra proposals, then a fresh Mind flow implements.

### 9. Datom: where it is used

**2026-09-27, heard by 8904b1** (`flows/8904b1/vision/datom.md`)
> Yeah we don't need Datom syntax where the program doesn't need it so we're not going to enforce Datom syntax on a messenger that doesn't need it.

> Well it's simple. If a tool requires datom syntax, then the skill is going to say it so we don't have to push anything.

**2026-09-28, heard by 8904b1** (8904b1-17)
> 8. Datom and status messages: we're going to use Datom when the tool actually uses Datom.

**2026-09-26, heard by 93ba9f** (`flows/93ba9f/vision/datomVocabulary.md`)
> And I don't know what you mean by tag. Datom doesn't have tags, has variants.

**2026-09-19, to b81560, typed** (transcript b8156034 line 695)
> We're going to program it in the system prompt of all our machine calls, and everything is going to be Datom. Everything, comments, everything is going to be specified

**CORRECTS.** 09-27 and 09-28 "we're going to use Datom when the tool actually uses Datom" narrow the 09-19 "everything is going to be Datom". The long horizon ("eventually everything will be datom-specified", 09-28 §1) still stands. **SETTLED** for now.

### 10. Meta harness anatomy: Flow, nexuses, subflows, version control

**Distilled Vision**, `Vision/flowNexus.md`: **SETTLED**
> A Nexus component decides the system prompt and everything about a launch, replacing the harness's subagents with specialized harnesses launched with specialized system prompts.

> The harness subagent facility is replaced. ... A subflow is instead an independent flow with its own system prompt, which can reply to the successor of whoever it was meant to answer; that makes the system asynchronous.

> A special field flow running on ultra-low power checks every question and every request a flow ends with, and, according to the ending flow's authority, spawns subflows given those questions and requests to answer or fulfill.

**2026-09-25, to e51411** (`flows/e51411/vision/launch.md`)
> Let's look at the anatomy, the ethos of this Flow tool. It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed.

**2026-09-25** (`flows/e51411/vision/nexus.md`, `flows/88475f/vision/nexus.md`)
> I guess we need better tools. We know what the tools are, right? They're the nexuses. Psyche Nexus is going to replace how we log Psyche and Mind. Mind Nexus is going to replace how we log the Mind and the field, not just log, but how the Mind interacts with the system

**2026-09-24, to e51411** (`flows/88475f/vision/flow.md`)
> I want to be able to start flows, stop flows, and send messages with Flow because it gives me the bare input. Flow basically exposes everything from the harness, and then message makes use of it. So Flow deploys first

**2026-09-28, page comment** (8904b1-31)
> We need to have this optional compilation with some parts of the code so that there's no datom logic in the nexus. ... It identifies the process that causes the CLI and passes it into the message.

> But yeah it's really important that we don't put any extra logic for handling deserialization and serialization of text in the Nexus because the Nexus has to stay small.

**2026-09-28, heard by 8904b1** (8904b1-5, -6)
> I think the idea to break up more nexuses is pretty good: writing specialty tools like Nexus for Herder, a Nexus for Nix, and, I guess you called it Reach, for deploying something.

> Once we develop these tools we're redoing Unix with nexuses that tell binary signal instead of text. ... You can see how the skill generation and all of this stuff will eventually become a workspace-generating tool, which the tool that manages machine flows will use to generate the workspaces.

**2026-09-26, to b7da5d** (`flows/b7da5d/vision/mainFlowRefreshAndRoles.md`)
> We need that field tool, either Field Nexus or the Field CLJ, whichever is most ready, to be able to interact with all of the system: getting transcript stuff; getting the state of Herder and the pains and all that; just making a library of the calls that we want ... We created our own index of the APIs, and we organize it in Ethos syntax.

> We're going to have a field that is going to have a different API also for different harnesses.

**2026-09-29, heard by c64ee3** (`flows/c64ee3/vision/flowNexus.md`, `versionControl.md`, `priorities.md`)
> We need proper messages and proper flow creation, which is controlled by a flow nexus that maybe uses some [Clojure] tools internally

> There's a tool there that's worth developing into a really simple nexus that we force agents to use instead of [JJ] and Git commands. ... The call can just wait for the other commit to go through and be pushed and for `main` to move, for the next commit to go through.

> My biggest concern is: starting to record things better; moving to a better workspace; developing, eventually, the nexuses that will take it to the next step, which is psyche, mind, and field

**2026-09-24 and 2026-09-25, system prompt** (`flows/d8df70/vision/mainFlowMode.md`, `flows/e51411/vision/systemPrompt.md`, `mainFlow.md`)
> I think their system prompt is overriding them ... so it has to be only in the system prompt.

> Also if we put all of our steady, well-distilled vision, intent, and spirit in the system prompt instead of in the prompt, then we have more room.

> For them the skill is the subagent. For the subagent the skill is a skill.

**Status.** The anatomy is **SETTLED**:
- Flow owns launch and system prompt;
- subflows replace subagents;
- the Nexus stays small, with no text;
- the caller is identified by its process;
- one central Start call plus shorthands.

These are **OPEN**: splitting into Herdr, Nix and deploy nexuses ("pretty good"); the VCS nexus; and the Psyche, Mind and Field nexuses ("we have to be realistic").

**TENSION (d).** On the tooling layer: 09-25 "Well if we're using Flow then we don't need Flow CLJ", against 09-29 (Codex, logged as Notion in `flows/6f51ad/notion/clojure.md`) "Instead of making these nexuses just write some tools in Clojure because it's easier for you. ... Eventually we'll move all of this onto a nexus".

### 11. Stateful versus declarative

**2026-10-01, page comment, STT** (`flows/7328f4/vision/stateful.md`)
> I don't want stateful stuff. I want declarative features and then the [nodes] use the features and the behavior is predictable. ... Let's make sure there's nothing specifically tuned on any of the hosts manually. I've been seeing all this stateful stuff come up and I don't like it. I need to be captain of any stateful hack basically.

**2026-09-29, relayed by caf622, typed** (`flows/b666e7/vision/stateful.md`)
> We don't do stateful unless we do it in a single call. We don't install anything statefully, not really.

**Status.** **SETTLED.** It bears on hooks: a watcher or poller is stateful machinery the living wants listed (§2 registry).

## Notion

**Hooks: the model marks the beginning and end of a reply.** 2026-09-29, c64ee3, STT (`flows/c64ee3/notion/hooks.md`; relayed into `b666e7`, `bd0019`). **OPEN.** The 09-30 books ruling in §6 adopts the "marked with a beginning and an end" part as vision.
> Whenever you say something important, this is why I want the hook. Maybe the hook could recognize something, a pattern. I think the best way is to make the model conscious of the beginning and end of giving a reply and use that as the object so that it has to pass the structure of that home [sic] syntax. Basically the tool has to be able to recognize it for the hook to work.

**Hooks: insert into an incoming message.** 2026-10-01, 7328f4, typed (`flows/7328f4/notion/hooks.md`). **OPEN** (he calls it research).
> Maybe even if there are hooks that could insert stuff when a new message comes in, kind of like waiting for a message to wake up the flow to add more into that message. I don't know if that's possible, but that would be more like psyche research.

**Psyche injected with a message.** 2026-09-29, 183ae0, typed (`flows/183ae0/notion/psyche.md`). **OPEN**, "long term".
> Later on I have an idea for how the psyche can be injected along with a message so that we don't wake up a model twice. We take the opportunity that something is coming in to give it the update on all the psyche that's been logged that's relevant to what it's doing. That's long term.

**A logging hook on user input.** 2026-09-15, 692df8, typed (`flows/692df8/notion/logging.md`). **OPEN.**
> Actually, it could almost even be automated, like a hook on the user input that starts a subflow with a small agent that logs if there's something to log.

**Quota hook.** 2026-09-18, b05237 (`flows/b05237/vision/operational-quotaBurnRateHook.md`; framed as a question). **OPEN.**
> Do we even want a hook that automatically injects the context and the quotas into the periodic message that gets queued in the model, and that attaches itself into the next message with a timestamp? That way, the model doesn't have to stop.

**Datom payload from several places.** 2026-09-29, 183ae0, typed (`flows/183ae0/notion/datom.md`). **OPEN.**
> in one version we find a way for datom to be able to use a path in some places instead of the actual payload ... I don't think it's very pure. Using paths is very setup-dependent so it's not a very good idea for a system that wants to be correct.
>
> The other way is to simply not use it. Conceptually you would have the datom file there and next to it would be the compiled signal file so that then the Nexus could load it because it's already signal.

**A single writer for main.** 2026-09-28, 183ae0, typed (`flows/183ae0/notion/commits.md`). **OPEN.** It became the VCS-nexus vision of 09-29 (§10).
> Do we not just need a single long-lived nexus that has a single writer logic?

**Curriculum as post-training.** 2026-09-29, c64ee3 (`flows/c64ee3/notion/curriculum.md`). **OPEN.**
> The curriculum maybe is an even more advanced concept: the concept of personality building or the post-training.

**Subflows started by Flow.** 2026-09-25, e51411 (`flows/e51411/notion/stack.md`). Later distilled into `Vision/flowNexus.md` (SETTLED there).
> The subflow command would be one of the queries for Flow, to start a certain kind of subflow so that the system prompt can be modified.

**Harness logic in its own Nexus.** 2026-09-27, 8904b1, marked "This is Notion" (`flows/8904b1/notion/anatomy.md`). **OPEN.**
> I think it would be better if the harness logic, maybe even the herder logic, would live in another Nexus. Then we would create an API through Ethos, through the Ethos signal of that Nexus

**Clojure tools before nexuses.** 2026-09-29, 6f51ad (`flows/6f51ad/notion/clojure.md`). **OPEN.** See TENSION (d).

## Summary of rulings

| Subject | Settled | Open |
|---|---|---|
| Event and hook infrastructure | Hooks and events, no tool call by the flow; polling forbidden (Vision) | Which harness events; how a mark is recognized; the insert-on-message hook (Notion) |
| Seat turn state | No polling; a polling registry with periodic report | Herdr dots and Claude/Codex hook surface (research asked) |
| Restart and succession | Handover in the transcript; lock takes the route; reap on refresh; self-refresh via Flow with process check; one startup prompt; fat user-level psyche | Idle-triggered cascade detail; context-size unwind; transcript selection for a specialized successor |
| Harness migration | Resume unless the context is old; stable/next socket rotation | Name of the compensation skill; automated Codex and Claude updates |
| Skill deployment | Out of the Rust; typed; vision is a skill; Curriculum Nexus reseeded from Nix; aspect ownership; prefix-all as minimum viable product | Three repos or scrap for now; per-repo or per-payload type (TENSION a); prefix taxonomy (TENSION b) |
| Books | Marked presentation as main output; lower tier makes it; Sonnet compares; few books | The marker and the hook |
| Seat hierarchy | Disturb the primary layer less; Field to Mind to Psyche | Fable on a new flow for the ethos design (TENSION c) |
| Ethos shape | Variant carries same-named type; inline struct with derived name; whole valid ethos | `name` or `skill name`; `types` type; redesign by Fable and Astra, then a Mind flow implements |
| Datom | Only where the tool needs it; variants, not tags | Payload drawn from several places |
| Meta harness anatomy | Flow owns launch and system prompt; subflows replace subagents; small Nexus | Splitting nexuses; VCS nexus; Clojure first (TENSION d) |

## Sources

Psyche records read:
- `Intent/`: `startupPrompt.md`, `psycheInteraction.md`, `models.md`, `context.md`, `anatomy.md`, `data.md`
- `Vision/`: `nexus.md`, `flowNexus.md`, `ethos.md`, `datom.md`, `psyche.md`, `distillation.md`, `messaging.md`, `deployment.md`, `committing.md`
- `flows/7328f4/vision/`: `hooks.md`, `polling.md`, `metaHarness.md`, `seats.md`, `books.md`, `ethos.md`, `Fable.md`, `stateful.md`, `network.md`, `secrets.md`
- `flows/7328f4/notion/hooks.md`
- `flows/b666e7/vision/`: `hook.md`, `stateful.md`, `declarative-features.md`, `triad.md`, `flows.md`
- `flows/b666e7/notion/`: `hook.md`, `watching-skill.md`
- `flows/bd0019/vision/`: `hook.md`, `books.md`, `userPromptLayer.md`, `aspect.md`
- `flows/c64ee3/vision/`: `hooks.md`, `skills.md`, `ethos.md`, `flowNexus.md`, `versionControl.md`, `priorities.md`, `presentation.md`, `recording.md`, `vocabulary.md`, `aspects.md`, `network.md`
- `flows/c64ee3/notion/`: `hooks.md`, `curriculum.md`
- `flows/183ae0/vision/`: `skills.md`, `seats.md`, `messaging.md`, `presentation.md`, `proposals.md`
- `flows/183ae0/notion/`: `datom.md`, `psyche.md`, `commits.md`
- `flows/c02c0d/vision/`: `seats.md`, `skills.md`, `presentation.md`
- `flows/8904b1/vision/`: `skills.md`, `anatomy.md`, `presentation.md`, `datom.md`, `deployment.md`, `logging.md`
- `flows/8904b1/notion/anatomy.md`
- `flows/b7da5d/vision/`: `refreshHooks.md`, `mainFlowRefreshAndRoles.md`, `flowRefreshAndArchive.md`
- `flows/f5a74e/vision/refresh-hooks.md`; `flows/b860be/vision/refreshAutomation.md`; `flows/e167d8/vision/refresh.md`
- `flows/e51411/vision/`: `refresh.md`, `nexus.md`, `ethos.md`, `stack.md`, `infrastructure.md`, `systemPrompt.md`, `versioning.md`, `mainFlow.md`, `launch.md`
- `flows/e51411/notion/`: `stack.md`, `v2.md`
- `flows/88475f/vision/`: `ethos.md`, `nexus.md`, `flow.md`, `waiting.md`
- `flows/93ba9f/vision/`: `ethosNames.md`, `automation.md`, `flowLaunching.md`, `primarySeats.md`, `datomVocabulary.md`
- `flows/e71dab/vision/`: `flowRefresh.md`, `launchGovernance.md`, `paneLifecycle.md`, `flowGarbageCollection.md`, `voiceLuna.md`
- `flows/d8df70/vision/`: `flowLifecycle.md`, `launch.md`, `flowTool.md`, `mainFlowMode.md`
- `flows/836818/vision/flowNexus.md`
- `flows/752e0f/vision/`: `curriculum.md`, `ethosNextGeneration.md`, `flowDeploy.md`, `refresh.md`, `refreshAddendum.md`, `psycheInSkills.md`, `psycheInjection.md`, `mainFlowMode.md`
- `flows/26c50c/vision/`: `curriculum.md`, `ethos.md`
- `flows/9ddcbc/vision/`: `flowDeploy.md`, `refresh.md`, `wake.md`
- `flows/6288d1/vision/flowDeploy.md`
- `flows/9993b5/vision/`: `curriculumNexus.md`, `flowRestart.md`, `harnessReplacement.md`, `transparentRefresh.md`, `transcriptSelfReference.md`, `transcriptOverFiles.md`, `easyFlowDispatch.md`, `distillEveryTurn.md`, `typedString.md`, `datomStructuralEditing.md`, `harnessBlockDocumentation.md`, `editNexusName.md`
- `flows/108ab0/vision/`: `operational-skillTypes.md`, `operational-skillIsVisionUnified.md`, `operational-curriculumAsModuleSystem.md`, `operational-curriculumSkillsRepo.md`, `operational-skillsAreVision.md`, `operational-visionIsSkill.md`
- `flows/b05237/vision/`: `operational-skillTypesTriad.md`, `operational-quotaBurnRateHook.md`, `operational-quotaVisualizationHook.md`, `operational-reportWatcherAndIllustrator.md`, `operational-fieldLunaWatcherAndArchiving.md`, `operational-typedMessagesDistinguishPsyche.md`, `operational-fableRestartWithRecoveredVision.md`
- `flows/b81560/vision/`: `operational-hooksAsEventSource.md`, `operational-psycheIdleTimerHook.md`, `operational-reapingOnRefreshAndFlowEndHook.md`, `operational-retiredResponseAndReaping.md`
- `flows/cf3553/vision/operational-finalResponseLifecycleHook.md`
- `flows/33ba2b/vision/operational-fieldRefreshSuccession.md`
- `flows/b80e55/vision/systemCheckupAgentAndAutoWake.md`
- `flows/05c604/vision/messages.md`; `flows/692df8/notion/logging.md`; `flows/f55ec8/vision/flowIdentity.md`
- `flows/6cc91b/vision/`: `typedPrompts.md`, `skills.md`, `openSourceHarness.md`, `nexus.md`, `notifications.md`
- `flows/6cc91b/notion/`: `datomMcp.md`, `harnessPurity.md`, `orchestrator.md`, `persona.md`
- `flows/d5b96b/notion/session-reaping.md`; `flows/6f51ad/notion/clojure.md`; `flows/7b4d4c/vision/flowArmsItselfToWatchTheArtifact.md`; `flows/753e69/vision/harnessVisualIndicatorsAndRemoteControl.md`; `flows/1a6ca4/vision/personaMetaHarness.md`

Transcripts searched. Typed user messages were extracted from every Claude session under `~/.claude/projects` (subagent sidechains excluded) and every Codex session under `~/.codex/sessions` and `~/.codex-next/sessions`. They were filtered to drop agent relays and briefs, then searched for hook, poll, idle, event, refresh, restart, successor, curriculum, skill deployment, datom and ethos. Transcript-only quotes in this report:
- `~/.claude/projects/-home-li-primary/7328f4ba-d5c4-440f-aa68-7e1d969deab8.jsonl` lines 442, 552, 898
- `~/.claude/projects/-home-li-primary/c64ee3f5-0732-4315-936e-7ffc63e3000b.jsonl` line 1672
- `~/.claude/projects/-home-li-primary/183ae001-cb84-40ed-8a1f-f07a76f0d1f4.jsonl` line 1280
- `~/.claude/projects/-home-li-primary--claude-worktrees-flow-840e42/840e42bb-b2cd-42eb-a9ec-7659a5b13ded.jsonl` line 432
- `~/.claude/projects/-home-li-primary/d8df703d-d083-4c29-9597-6b32e7411b75.jsonl` line 776
- `~/.claude/projects/-home-li-primary/b8156034-b845-43c4-890a-49a73d806ee1.jsonl` line 695
- `~/.codex-next/sessions/2026/09/29/rollout-2026-09-29T11-20-29-01a0ee2e-a52e-7c92-98c7-9a5d5b96b3f3.jsonl` lines 105, 4095, 4103, 4139, 4151
- `~/.codex-next/sessions/2026/09/28/rollout-2026-09-28T10-23-01-01a0e8d3-aace-7712-aae2-3ce6f51adad5.jsonl` line 9848
- `~/.codex-next/sessions/2026/09/28/rollout-2026-09-28T15-00-37-01a0e9d1-d20f-7b43-98b0-15bb666e70e1.jsonl` line 3840

The `transcript` command named by the transcript-search skill is not installed on this host. The search used a direct JSONL reader instead, so a living message sent through a relay channel with an unusual prefix may have been missed.
