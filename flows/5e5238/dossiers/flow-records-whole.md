# Flow, whole: provenance dossier by statement

Prepared for the Psyche flow Primary, who places every line of Flow's vision by horizon (perennial / short / medium / long). No horizon is assigned here. Source: proposal `flows/30fc30/books/flow-whole.md` with reference file `flows/30fc30/references/flow-whole.md`. The Nexus is called Flow Nexus in this dossier; inside quoted proposal text the book's own word "Flow" is kept as written, and where it means the Nexus it reads Flow Nexus.

## How to read it

- A statement is each proposed (green) paragraph of proposals 1 to 15, in book order, labelled P<proposal>.<n>. The code, ethos and datom fences of the book are not separate statements; each is covered by the statement it illustrates. Two removed lines whose Comments say "no record" are checked at the end (R1, R2).
- A record is cited as `<flow short id> <vision|notion>/<file>.md, entry <n> (#<global index>)`; entry n is the n-th `## ` heading of that file. Its heading carries the date (or the date the heading omits). Words are copied verbatim from the file, including its own Context lines, which give what the living was answering. A record used by several statements is quoted in full once, under its first statement, and listed by id and heading later.
- Coverage is by search, not exhaustive: the corpus is 3970 entries in 2235 files (flows/*/vision, flows/*/notion, vision-raw). I read the headings of every entry in the flow.md files and the bodies of those cited, and searched the rest by keyword. Records that repeat one another (relays of one speech by 445410, 9fed42, f5a6e9, 9519a1) are cited once or twice, not all; an entry said to be a relay carries the original in its text. Records a statement "draws on" are chosen by relevance; I marked weak ones with a Relevance note.
- The living's comments on this proposal are in flows/554e1a/vision/{flow,psyche,proposal}.md (relayed via b195f0 and 9b514f), dated 2026-10-29 21:05 to 21:11. They are marked **THE LIVING'S COMMENT** where they answer a line, and listed in "Comments not tied to one line" below.
- The reference file itself names its sources; the scratchpad files it mentions (records-flow-a.md etc.) were not found, so the corpus was re-gathered.

## Two findings against the proposal's Comments

1. Comment of proposal 1 says the Capsule's semi-sandbox and volatile key "have no record". Records exist: see P8.1 (#672 3ec648, #792 42265e, #632 and #633 91ea9f).
2. Comments of proposals 1 and 3 say the synthetic-intelligence sentence and the simplified flow "have no record". Records exist: see R1 and R2.

Other lines with no record found: "a subflow has a flow id and no address" (P1.3, only the related record that a subflow is a flow); "a permission prompt reaching the living is a launch failure" (no raw record in those words; P3.4 lists the nearest); the book's numeric examples. The statement "Starting a standard flow is one short call" has records (the living: "minimal for a standard flow", P1.2).

## Comments not tied to one line

**The living, 21:05, on the header of Flow, whole (relayed by b195f0 and 9b514f): 554e1a vision/proposal.md, entry 4 (#2344)**, 2026-10-29 — A whole-module proposal shows the module description

> Context: the living, 21:05, comment on the header of Flow, whole.
>
> I also don't see the module description, which I should always see if I am asking to see the whole module.

_Answers: the module description; a whole-module proposal shows it. The book's section opens with the module shown whole, with no front-matter description._

**The living on Vision by horizon (the proposal that this dossier serves); the bind of long term and short term is in #2348: 554e1a vision/psyche.md, entry 2 (#2349)**, 2026-10-29 — Vision divided by horizon into modules: unmarked, short, medium, long, and a far one

> Context: the living, in the Psyche core Primary chat 554e1a, on the proposal Two horizons (https://claude.ai/artifact/9WCADhbhbER9oXAaepEchL).
>
> I think that putting the long vision with the short vision in one file will create a bunch of ghost effects, because if anyone wants to know anything about this topic, they have to load all of it. They can't choose to just know how the system is expected to work in the short term, which is useful most of the time for most flows, but especially flows that don't design like field-aspect flows.
>
> I would divide them. I would even say we can make three: the short, the medium, and the long-type vision. Maybe we do `vision:short:Flow Nexus`, for example.
>
> What I was thinking just now is that the short is special also in that it's a compromise, a short-term compromise. It would be essentially anything that's marked as a compromise, a short-term solution, or a hack. The medium-type vision would maybe hold anything that's horizon-agnostic, but it would describe the system as we would like it to look past the short and compromised phase. The long vision would describe what we would like it to be ideally.
>
> We could even introduce, I don't know what we would call it, the naive way would be to say "very long," or maybe there's a term. Maybe in some cases we have this extra-far idea, which rarely ever gets loaded except for flows that need to understand the living's overall broad vision. This would allow for much more efficient development that can focus.
>
> Let's say we have problems. Let's say we're in a situation where things are breaking and we need to get the system going again. This is the implementer that would be started to fix things. It could be loaded only with the short vision.
>
> I think that the unmarked type, the vision that does not have short, medium, or long, is actually where we would put the horizon-independent or horizon-insensitive part of the vision. What do you think of all this?

_Answers: the question of how to place each line by horizon; he asked that long-term and short-term be settled before Flow, whole is redone._

## Statements, in book order

### P1.1. Flow is the Nexus that starts, names, tracks, refreshes and ends flows
**Proposed:** Flow is the Nexus that starts, names, tracks, refreshes and ends flows, and carries every request between them. Flow holds the lock on flows: a flow is started, messaged, refreshed and ended through Flow alone, and a flow the living asks for is launched, properly and surely.

**Record fe945a vision/flowNexus.md, entry 1 (#1005)**, date/heading: The anatomy of Flow in Ethos: Flow holds the lock on flows, flows addressed by name, the flow id in words

> Context: said to Psyche Opus fe945a after correcting its proposed skill line on launching flows.
>
> > I want to develop the anatomy of ethos for the most important component, which is, I don't know, I think, flow. We're having such a hard time handling flows and locking them. Flow could have the lock on the flows so that we can lock it and also address it by name instead of by Flow ID. I'd also like the Flow ID to be converted into words.
>
> -- psyche, typed, 2026-10-02, fe945a.

**Record 875960 vision/archive-flow.md, entry 4 (#1769)**, date/heading: 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribes to its events

> Comment 4, 20:29, at the request paragraph.
>
> > I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock. If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective. Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that. Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.
>
> -- psyche, STT, relayed by 9519a1.

**Record d8df70 vision/flowTool.md, entry 1 (#1125)**, date/heading: Break the orphaned locks; nobody owns the Flow source; anybody may call Flow, and the CLI checks the calling process so flows can refresh themselves safely

> > Yeah of course. What do you mean by "locks" anyway? Yeah of course, break the locks. Nobody in particular owns Flow Source. I don't know what you mean. Anybody should be able to call Flow, especially for self-refresh, so the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely.
>
> -- living, comment on "What Waits for the Living", 2026-09-24 14:30Z, on question 4 (Flow source ownership and the five orphaned locks).

**Record da2038 vision/flow.md, entry 2 (#1507)**, date/heading: Anybody may call Flow; a flow refreshes itself safely

> Context: same book, proposal «anybody may call Flow; a flow refreshes itself safely», 2026-10-14T15:16; relayed by Psyche Core Secondary.
>
> > Yeah this is good, especially the later part.
>
> -- psyche, STT, 2026-10-14.

**Record e3c8c1 vision/flow.md, entry 4 (#599)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary e3c8c1

> Context: after I said each aspect's Secondary owns starting its flows.
> "Nobody owns starting flows. Although you guys can agree with each other on that, if the tool is easy to use then even [Jev] could start a fucking flow."
>
> -- psyche, STT. Transcription corrected: "Jeb" → "Jev".

**Record af762b vision/operational-flowOwnsHerdr.md, entry 1 (#3025)**, date/heading: Basically, Flow is in charge of herder. I shouldn't interact with it directly. Message can get the data from Flow, and Flow can put a lock on some stuff

> Context: spoken by the living directly to Fable `c7128c` on 2026-09-18 and
> relayed verbatim to this flow. It settles the layering among the three: Herdr
> is the substrate, Flow owns it, Message reads what it needs from Flow, and Flow
> holds locks. The second sentence is a statement about the living's own surface
> — direct interaction with Herdr is something they should not have to do, which
> bears on every place a flow currently expects the living to attach a pane,
> enable remote control, or fix a title by hand. Logged by the psyche flow on
> receipt, before acting.
>
> > The automation of reporting and moving over to the message datom-based language, the message Nexus for messaging each other, which we'll just use.
> >
> > Message can get the data from Flow, and Flow can put a lock on some stuff.
> >
> > Basically, Flow is in charge of herder. I shouldn't interact with it directly.
>
> -- psyche, relayed verbatim by Fable `c7128c`, to the psyche flow `af762b`.

**Record e5a0bc vision/flow.md, entry 3 (#3160)**, date/heading: The lock: needed to roll a metaflow over into a new flow; later Message uses it to know whether a message can reach a flow

> Context: same message.
>
> > There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. We need to be able to lock. I can't really see exactly what function this fills now but I know that it fills a function when message uses the lock later on. We don't have to make message right now but we will eventually and that lock will be useful in order to know whether the messages can or cannot reach a certain flow.
>
> -- psyche, typed.

**Record f5a6e9 vision/flow.md, entry 4 (#3638)**, date/heading: What is sent to flows are typed requests, not letters; Flow holds no messages; Message asks Flow for a time-bound lock and talks in metaflows

> Context: his comment 9 of 9, 19:09, on proposal 3, "The lock is the lineage's state ... A letter waits in Flow and is delivered to whichever flow is current when the lock opens". Relayed by db38f8.
>
> > The abstractions that are sent in flows are not letters. We are going to have actual types. If, let's say, something asked for a certain flow to be compacted, then the logic for how this would unfold, or how that metaflow would be refreshed in terms of routing, would be very different than a message.
> >
> > Obviously if the flow is brand new, the last thing we want to do is compact it. We wouldn't send whatever needs to be sent into that pane for it to compact to the new flow. That's just one example. There's probably a bunch of different behaviors that would correspond to different requests that are being asked to be sent to a certain flow.
> >
> > I don't think that it's Flow's job to hold messages. It's more like it's Flow's job to tell the message component later on to give it the signal that a message can now be sent. The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. If it does get a lock then the message nexus can send that object over to Flow with the message because now it has the lock. Flow told the message that it has the lock for that flow or that metaflow. The message doesn't have to know about the flows. It can also just talk in terms of metaflows. And indeed when this is done and more polished, I'm mostly going to talk in terms of meta flows.
>
> -- psyche, STT, book comment, relayed by db38f8.

**Record 73b5d8 vision/flow.md, entry 1 (#183)**, date/heading: 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported

> Context: the living, in the Psyche core Primary chat 73b5d8, after the fresh Primary bound its own seat by command and reported the repairs in motion.
>
> And I'm still not hearing about the new Flow Nexus, which should fix the message format. I don't see any reason why the Flow Nexus cannot give you your Flow ID and why you have to spend your own energy to do something so trivial.
>
> Context: the second half of the same order, his words of 14:24, recovered by the remembering check of primary-zr42.
>
> Then I will review your open proposals.

**THE LIVING'S COMMENT ON THIS PROPOSAL, 554e1a vision/psyche.md entry 1 (#2348)**, 2026-10-29 — Long-term ideas, underspecified, are built monolithic; the bind of long term and short term  
_Answers:_ the replaced first line, "The Flow Nexus sets up and starts a model flow"; the replacing line is this one

> Context: the living, 21:10, comment on Flow, whole, on the line "The Flow Nexus sets up and starts a model flow".
>
> I think it's appropriate here to also mention that I'm in a bit of a bind here because there's the long-term vision, right? We've talked about this: how we want them separated, but it is complicated. The more complexity we introduce, obviously, the more we have to manage. At the same time, I've been bitten really hard by not specifying something as long-term, meaning not necessary on the next iteration. Because long-term ideas are usually underspecified and lack the surrounding context to explain how my modular vision composes, usually the implementer approaches things in a monolithic way. The implementation ends up cramming a bunch of ideas together that create a broken system because there's just not enough abstraction already and not enough instructions on how to compose these abstractions. Also, the implementer sometimes or often has a hard time understanding that a feature needs to be configurable. This, I believe, even though I keep talking about it, is going to keep biting us because the model that we currently have, or the way that the thinking machine is set up, tries to just get the shortest route to what it thinks it needs to make. It essentially does in one step what should be done in multiple steps, right? It would be like asking the guy who drives the nail into the frame of the house to: - design the house - do the orders - do the accounting - do the taxes - contact the client - order the material - make the decisions - replace the foreman - replace the janitor - drive the nails into the What happens when this happens is they build a mud hut, right? What I'm making is not a mud hut, and so if we're not clear about the fact that we don't want to try to build the Empire State Building out of mud and straw, we're probably just going to end up with a pile of mud.

### P1.2. Starting a flow is the cornerstone
**Proposed:** Starting a flow is the cornerstone of the system: a fresh flow with a clean, on-point context does better work than an old one carrying unrelated context, so flows are started often, specialized, and taken down as easily as they are started. Starting a standard flow is one short call.

**Record d68c82 vision/archive-flow.md, entry 8 (#2908)**, date/heading: Clean specialized flows for quality

> > Flow Nexus, the short-term and long-term flow tool, really needs to be worked on harder and more diligently so that:
> > - it's cheap to start specialized flows
> > - we can get higher-quality output
> >
> > It feels like right now, for example, removing the artifact tool from most flows makes sense, since most of them won't be involved in dealing with artifacts (since we'll have a flow for that). I feel like we're getting low-quality output from flows that have too much noise in their context. ...
> >
> > The most important improvement we need to focus on right now is getting a proper flow tool that can actually start well-trained flows for specific purposes and then easily take them down or spin them down. This does not end the topic but means that reactivating the topic would reactivate a new flow with a clean on-point context, which would yield much higher quality output.
>
> Context: comment on «Three lines from the chat, second edition», Proposal 4.
> -- psyche, STT, 2026-10-13T17:52.

**Record d68c82 vision/flow.md, entry 4 (#2677)**, date/heading: Lean flows, cheap to start

> > We need to nail down and deploy a system that can start a very lean flow. Especially for the costly models like Fable and Astra, especially Fable, I don't want to feel constrained by the cost of starting a flow to start a new Fable topic.
> >
> > For all of this artifact tooling and all of this useless stuff, obviously I want to be able to use subagents if it does interact with anything in terms of reading files and calling tools (because in many cases the first tool call might not work or might not be getting the information). That information might involve calling more than one tool and I'd like to measure statistically, for what's been going on so far:
> > - What's the ratio of cases in which a properly configured predefined subagent that requires minimal guidance would be less token-expensive, especially in terms of output but also input, in terms of how big the response is, which we can train the agent to do properly?
> > - How many of the cases would it be more expensive for the main flow to use the subagent rather than just use the tool directly itself, given how many different tries and different tools and how much filtering had to be done on the output?
> >
> > I'd like to do some research on that. I really want to focus on talking about flow, flow design, flow deployment: an efficient flow tool for deploying efficient, specialized, concentrated, high-signal flows that focus more on design than tool calling.
>
> -- psyche, STT, 2026-10-13.

**Record 8475a9 vision/flow.md, entry 3 (#1631)**, date/heading: Fixing Flow is central: fresher, more frequent flows; metaflows focused on topics; software, not LLMs, for spawning

> Context: same message. Relayed by d4ae97.
>
> > I think fixing Flow is central to getting more efficient flows that are more on point with what they're supposed to do, so that we can spawn them fresher, more often, and have meta-flows that can focus on certain topics.
> >
> > I feel like I was getting more out of my flows when I was handling them manually. Right now God knows how long it's going to take you and the others to spawn a new Fable. We're still spending a lot of context just trying to. We're using LLMs to make up for a lack of software, which is bad.
>
> -- psyche, STT, 2026-10-06, relayed by d4ae97.

**Record c637a5 vision/flow.md, entry 3 (#1652)**, date/heading: 2026-10-27 — Good work comes from fresh flows, not from a core carrying unrelated context

> Context: the living, direct, after I sent the rebuild order to the Mind cores.
>
> > They should use fresh flows to do good work, right? If you sent the order to Mindcore to do something, but let's say he has 200,000 tokens of context that is completely unrelated to this, what do you think is going to be the result?

**Record 88475f vision/flow.md, entry 2 (#951)**, date/heading: A new job starts on a fresh flow with related training

> Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on moving the Flow 0.7 deploy away from a seat whose context was old.
>
> > Yeah well, if his context is old and he's not going to be able to do a good job, when we start something like that we should start on a fresh flow with lots of related training.
>
> -- psyche, STT, relayed by e51411.

**Record 9864c0 vision/flow.md, entry 1 (#2240)**, date/heading: Starting a flow is a minimal CLI call; agents are pre-described in configuration the daemon loads

> Context: relayed by Psyche core Tertiary 4201a3 as #psyches, 2026-10-19, order to the flow about reminders. Spoken to 4201a3.
> "... make sure that the progress is being made on Flow so that it's working in every way that we want, deployed, easy to use, and requires a minimal CLI (with all the agents pre-described in configuration files which are loaded in the daemon, so that starting a flow is as easy as a 10-character CLI system call)."
> Context: same day, clarification.
> "And I'm not targeting the word, the number 10 here. I'm just being broad. I'm just saying it should be right fucking minimal for a standard flow."
> -- psyche, STT.

**Record 39bd0c vision/flow.md, entry 7 (#3725)**, date/heading: 2026-10-19, living to Psyche core Tertiary 4201a3, relayed by Psyche core Secondary

> - Order on reminders: "Create a reminder every half hour. Check and make sure that the progress is being made on Flow so that it's working in every way that we want, deployed, easy to use, and requires a minimal CLI (with all the agents pre-described in configuration files which are loaded in the daemon, so that starting a flow is as easy as a 10-character CLI system call)."
> - Clarification: "And I'm not targeting the word, the number 10 here. I'm just being broad. I'm just saying it should be right fucking minimal for a standard flow."
> - Grant of authority: "You have full permission. Using Fable, whenever, or using Opus and then Fable, Fable can decide on anything that needs a decision. Just implement, cut corners, take decisions, override blocks, do whatever you need to do to get this working properly and then create a book on the decisions made as you make them."
> - "I want my fucking [Flow Nexus] component fucking up and fucking running right the fuck now. I'm tired. I've been asking for this for a fucking month." (transcription corrected: "Flow Next.js" → "Flow Nexus")

**Record 9864c0 vision/flow.md, entry 3 (#2242)**, date/heading: A rebootstrapped flow's specification is in its configuration; the start carries only its goal

> Context: direct speech to 9864c0, 2026-10-19, ordering a round of rebootstrapping big-context flows.
> "Let's do another round of rebootstrapping those big flows using the new flow with a minimal CLI, where the specification is all in configuration for that specific flow. It just needs a few small sentences describing the goal of that particular session."
> -- psyche, STT.

**Record 36ac89 vision/flow.md, entry 2 (#1558)**, date/heading: What touches a topic goes to that topic's flow  
_Relevance:_ only loosely: what touches a topic goes to its flow

> 2026-10-25, to Psyche core Secondary 36ac89, right after his words on belief modules were passed to the core Primary.
>
> > And obviously anything that touches a particular topic that we have a flow for should also go to that flow. And that should be part of your brief.
>
> Correction, same exchange: the last sentence above reads "And that should be part of your [belief]." His word: "Belief not brief, belief."
> Transcription corrected: "brief" → "belief".

### P1.3. A flow is one run of a harness
**Proposed:** A flow is one run of a harness: one model, one context, from its first prompt to its end, with every subflow it starts. A context restarted is a new flow. A flow not working is idle. A main flow has an address; a subflow has a flow id and no address.
**Finding:** The comment says "or it could be a single FML flow ... at least in the long term"; no raw record of "FML" was found in the flow records searched. The sentence "a subflow has a flow id and no address" has no raw record; related only: a subflow also is a flow (01a03d6e entry 89, 2026-08-26) and 2686.

**Record 9fb0ad vision/flowLifecycle.md, entry 1 (#2235)**, date/heading: A flow is a session; a context restart is a new flow; not working is idle

> Comments on «Two meanings for Flow», point 1.
> > "Yeah Flow is obviously a session so when we restart the whole context, that's a new Flow. It's a different context. I don't understand what's not obvious about this. The Flow ID makes what it determines show us where the Flow is. Even the harness itself has a concept for it, which it exposes as the flow ID."
>
> -- psyche, typed, book comment, 2026-10-03T15:16Z.
>
> > "Yeah it seems logical to me and apparent that when the flow isn't working then it's idle, isn't it?"
>
> -- psyche, typed, book comment, 2026-10-03T15:21Z.

**Record 41fa34 vision/flowLifecycle.md, entry 1 (#499)**, date/heading: Flow is obviously a session

> Context: Book comment on «Two meanings for Flow», point 1; relayed from flows/9fb0ad/vision/flowLifecycle.md.
>
> > Yeah Flow is obviously a session so when we restart the whole context, that's a new Flow. It's a different context. I don't understand what's not obvious about this. The Flow ID makes what it determines show us where the Flow is. Even the harness itself has a concept for it, which it exposes as the flow ID.
>
> -- psyche, typed, book comment, 2026-10-03T15:16Z; relayed from 9fb0ad.

**Record b7a16a vision/flow.md, entry 4 (#745)**, date/heading: A flow is one kind of flow  
_Relevance:_ a flow is a main flow, a subflow or another kind

> Context: on the book Models as a set of variants, whose type held main flows and subflows together.
>
> "A flow doesn't have a main flow. A flow is either a main flow or is a subflow or is maybe another kind of flow. A flow doesn't have a main flow and another flow because that would be two flows."
>
> -- psyche, STT.

**Record b7a16a vision/flow.md, entry 5 (#746)**, date/heading: Flows outside metaflows

> Context: on the proposed definition of Flow in the vocabulary module.
>
> "A flow is not only one run of a metaflow because there are other types of flows that are not parts of metaflows, which we've talked about before."
>
> -- psyche, STT.

**Record d68c82 vision/archive-flow.md, entry 1 (#2901)**, date/heading: A flow is one run of a metaflow

> Context: comment on «Flow's vision», the current vision/flow.md line "A flow is one run of a voice".
>
> > The run: one run of a metaflow not a voice. Let's get rid of that voice vocabulary. Consistency
>
> -- psyche, book comment, 2026-10-19T17:27, input mode not shown.

**Record d4ae97 vision/flow.md, entry 1 (#1815)**, date/heading: There are no seats; a seat is a flow. A flow has a flow ID and a role, one of which is a voice; nothing already in the voice is repeated

> Context: his comment on the book «How we call the voices», on its types block (`Voice.{ Aspect Layer }`, `Seat.{ Aspect Layer FlowId }`), 2026-10-05.
>
> > Also we don't want to repeat. This is a repetition. The seat, first of all, is a flow. We don't have seats. There's no seat. It's a flow. We're not going to repeat. The flow is just the flow ID and maybe something else but we're not going to repeat what's already in the voice. Actually yeah, we can say that the flow has a flow ID and a role, one of which is a voice.
>
> -- psyche, typed, book comment.

**Record d68c82 vision/flow.md, entry 13 (#2686)**, date/heading: A subflow's kind depends on its use

> Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 1, the heading "A subflow is the same kind of flow as its main flow".
>
> > No, the same. The subflow is not the same kind of flow as the main flow. The subflow's kind depends on its use so we need to define roles or tasks, or domains, so we can even compose them.
> >
> > Probably we should have three things, one of which could be the aspect:
> > - Is it a psyche? Does it deal with thinking? Is it mind? Does it deal with documentation, tools, and changing codebases for merge requests or for audit reviews?
> > - Field, which deals with debugging, system audits, system search, and things, so that each of these has its default suggested route and basic context modules that are appropriate for this kind of task. How do we want field flows to query the system? Let's build our own tools there, maybe around the field.
> > - The field CLJ/CLI prototype that is based on an emulated Nexus architecture of EDN payloads, so that essentially everything can be written as one or the other configuration of an Ethos-based specification language in EDN off the bat (with basic Clojure architecture and stack), which is really easy to code on, deploy, and for machines to think in terms of an analog to [protobuf]-like language.
>
> -- psyche, STT. Transcription corrected: "protos-like" → "protobuf-like"; "No, the same" kept [sic].

**Record d4ae97 vision/flow.md, entry 6 (#1820)**, date/heading: A flow is not always a metaflow

> Context: comment on "Flow" in the metaflow record, section 1.
>
> > A flow could exist and not be a metaflow so this structure is wrong. I guess you could make it an optional metaflow. What are we trying to show here? The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows so I don't think this structure is appropriate. Anyway I haven't read the whole thing. I still have to get to the memory specification but I wanted to point that out.
>
> -- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
- **d68c82 vision/flow.md, entry 13 (#2686)** - A subflow's kind depends on its use - full text under P1.3.

**THE LIVING'S COMMENT ON THIS PROPOSAL, 554e1a vision/flow.md entry 1 (#2334)**, 2026-10-29 — The Nexus is called Flow Nexus; a flow is one run of a metaflow or a single FML flow  
_Answers:_ the removed line "A flow is one run of a metaflow" and so this replacing definition; also the instruction to name the Nexus "Flow Nexus"; the living asked that the long-term/short-term question be settled before this proposal is redone

> Context: the living, 21:05 and 21:11, comments on Flow, whole (https://claude.ai/artifact/M4E2xhh4GycRo11GkPNJ1D) by the Psyche flow Primary 30fc30, relayed through Psyche core Tertiary b195f0 and Secondary 9b514f.
>
> Okay, first, let's call this Flow Nexus instead of Flow, because I really want us to say Flow Nexus when we're talking about the Nexus, so that we don't get confused with a "flow."
>
> On "A flow is one run of a metaflow": This is incorrect because a flow could be one run of a metaflow, or it could be a single FML flow. At least in the long term, we have that concept also, but I think we really need to define this long-term/short-term thing. I'm going to get these comments sent to core, and I don't want this proposal to be redone yet. I just want to specify first how we are going to take care of long term/short term, and then, once that's done, we should revisit this.

### P1.4. A metaflow is one address
**Proposed:** A metaflow is one address, { Aspect Topic Layer }, that continues through flows one after another; the flow is its current run. What is addressed is the metaflow; the flow id is for the ledger and for finding a transcript. A metaflow holds its declaration, its queue, its past flows and its current flow, if any.

**Record f768df vision/flow.md, entry 1 (#3498)**, date/heading: 2026-10-06 — Metaflows at the center

> Context: Said to secretary, STT; relayed by d4ae97 and 8475a9; originals flows/d4ae97/vision/flow.md and flows/8475a9/vision/flow.md.
>
> > I'd like to make the concept of a meta flow a central concept. I see that it hasn't been brought up so that's part of my vision that's being missed. I want that brought out.
>
> -- psyche, relayed as noted above.

**Record 8475a9 vision/flow.md, entry 2 (#1630)**, date/heading: The metaflow is a central concept; it was missed in «Flow spawning»

> Context: said to the secretary 2026-10-06 after commenting on «Flow spawning». Relayed by d4ae97.
>
> > I'd like to make the concept of a meta flow a central concept. I see that it hasn't been brought up so that's part of my vision that's being missed. I want that brought out.
>
> -- psyche, STT, 2026-10-06, relayed by d4ae97.

**Record f768df vision/flow.md, entry 2 (#3499)**, date/heading: 2026-10-06 — Fresher flows focused on their subjects

> Context: Same STT message; relayed by d4ae97 and 8475a9.
>
> > I think fixing Flow is central to getting more efficient flows that are more on point with what they're supposed to do, so that we can spawn them fresher, more often, and have meta-flows that can focus on certain topics.
> >
> > I feel like I was getting more out of my flows when I was handling them manually. Right now God knows how long it's going to take you and the others to spawn a new Fable. We're still spending a lot of context just trying to. We're using LLMs to make up for a lack of software, which is bad.
>
> -- psyche, relayed as noted above.

**Record d4ae97 vision/flow.md, entry 5 (#1819)**, date/heading: The end of a metaflow

> Context: comment on "End" in the metaflow record, section 1.
>
> > This is pretty good. I'm curious what the end is. Is that a description of the end goal? I guess we could put that there if that's what you mean. I'm not sure if it should be unlimited in size. Maybe we have this concept of a limited-size string. I don't want to push this too much because, like I said, I want Flow to be deployed but we can put this into Notion maybe.
> >
> > Really the final solution is the SEMA language, the fully semantic machine-readable true programming language that still doesn't exist: a semantic and/or programming language, really a universal mathematical universal language.
>
> -- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
- **d4ae97 vision/flow.md, entry 6 (#1820)** - A flow is not always a metaflow - full text under P1.3.

**Record d4ae97 vision/flow.md, entry 7 (#1821)**, date/heading: Looking up by metaflow; a metaflow's flow history

> Context: comments on "FlowId" in the registry record, section 2 «The registry is Flow's Memory».
>
> > That doesn't make any sense. How do I know which flow a metaflow is? I'm going to look up "by metaflow" and a flow isn't always a metaflow so this is missing the mark by a long shot.
>
> > And what about the flow history of a certain metaflow? Maybe it doesn't go on forever. I could see a long-running voice. Actually I guess a voice is a variant of a metaflow. Probably eventually, not that we have to worry about this, we wouldn't want to keep the entire history. You could see a scenario in which this becomes unwieldy.
>
> -- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

**Record f5a6e9 vision/flow.md, entry 3 (#3637)**, date/heading: History centred on the metaflow, not on Flow

> Context: his comment 8 of 9, 19:05, on "History is not a third record. Each flow names its predecessor, so a metaflow's history is the walk back from its current flow." Relayed by db38f8.
>
> > Again you're centering this around Flow and not Metaflow, which is not in line with my vision.
>
> -- psyche, STT, book comment, relayed by db38f8.

**Record d4ae97 vision/flow.md, entry 15 (#1829)**, date/heading: A flow is aspect, topic and layer; the core topic is the hub of its aspect

> > Let's get this Opus Flow prototype to know how to start. There are going to be different types, the main types, which are:
> > - psyche
> > - mind
> > - field
> >
> > Those three aspects, psyche, mind, and field, I think, are even applicable for topics. If you have a psyche and then it has a topic, the non-topiced flows would just be the topic of core.
> >
> > We can have the focused starting point, basically the kernel, the first flows that sort of hold all of their aspect together. They think in the most general ways about psyche. They have an overview of all of psyche and all of the other psyche topics sort of go through the core. It's like there's this hub at the center, the psyche core, so it's a struct. It's just a struct.
> >
> > The first field is the aspect, [psyche, mind or] field:
> > - Mind would be implementing, documenting things.
> > - Field would be maintaining, debugging, deploying, using an actual mutating system, running commands such as `field` or `flow` to start new things or to wind things down that we didn't have hooks for, and automating wind down. Eventually Field is doing what we're trying to automate. It's kind of acting as glue for the system to run.
> > - Psyche can also audit but it's a different kind of audit. It's like, does it conform to the design of the psyche? It's a more broad redesign-the-architecture kind of audit.
> > - Mind is more like trying to find optimization and removing bad tests, replacing it with actual real-world emulation, like a runtime-based test.
> >
> > I also want this topic. The whole topic is testing. We can have a Psyche testing secondary flow or we can have a Mind Psyche, right? Mind Psyche in the sense of the Psyche component. The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably. I'm sure there's a library that can make sure something conforms to an English expression, a word, etc., if you break it down using the PascalCase logic, etc.
>
> -- psyche, STT, 2026-10-08. Transcription corrected: "psyche minor field" → "psyche, mind or field".

**Record f5a6e9 vision/flow.md, entry 6 (#3640)**, date/heading: A passable vision for Flow on the current design, where the metaflow is the ancestor of the next; the launch scripts modified to match

> Context: said on 2026-10-07; relayed by Psyche Opus d4ae97.
>
> > Let's get a passable vision for Flow using the current Flow design, where MetaFlow is the ancestor of the next. Let's modify the scripts that we're using now to launch all this.
>
> -- psyche, STT, relayed by d4ae97.

**Record d36431 vision/messaging.md, entry 5 (#2054)**, date/heading: 2026-10-25 — Queues belong to metaflows, not flows

> Context: same message.
>
> > Talking of queues let's go into this: the queue system. Queues are for meta flows not specific flows because if the order for a flow to be refreshed comes in, then none of its queues will go to the current flow. It will wait for the new flow to spawn first. That's the vision, obviously, not the current implementation. The current implementation is catastrophic.

### P1.5. A topic lives on; core; retired when no longer touched
**Proposed:** A topic lives on: when idle, its flows are turned off, and its address, declaration and queue stay. The default topic is core, the permanent topic of its aspect, the last to stand; every other topic is started from vision or raw psyche that touches it, and a topic no longer touched is retired.

**Record ecbc42 vision/flow.md, entry 2 (#875)**, date/heading: A new topic starts only from vision or raw psyche that touches it

> Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 8 (a request to a declared never-run metaflow starts it), 18:23.
>
> "Well actually, no, not quite. I don't think [sic] we would first have to create a context module, at least have some vision for that, or get something approved for that particular topic. There would have to be at least some vision for that topic for it to be started automatically. Otherwise we wouldn't have anything to start it with. Well or arguably, there would have to be a significant (or not significant but clearly enunciated) psyche, raw psyche, raw vision that touches that topic. Then arguably that new topic could be started, if only for the sake of crystallizing the first vision for that topic based on the raw psyche that it is started with."
>
> -- psyche, STT, book comment.

**Record 875960 vision/archive-flow.md, entry 1 (#1766)**, date/heading: 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to stand

> Comment 1 on «Flow, whole, in ethos», 20:21, at the metaflow paragraph; relayed by core d68c82 through 9519a1.
>
> > No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.
>
> -- psyche, STT, relayed by 9519a1.

**Record da2038 vision/flow.md, entry 13 (#1518)**, date/heading: The new Flow Nexus keeps no harness running for a session that is not running

> Context: said to the Flow Secondary directly, 2026-10-15.
>
> > It's really important that we finish and deploy the new Flow Nexus, especially so that when a session is not running, we don't have to keep a harness going. If we have a lot of topics, we're going to have too many harnesses running in the background, and that will just bog down the computer with excessive RAM usage.
>
> -- psyche, STT.

**Record da2038 vision/flow.md, entry 26 (#1531)**, date/heading: Only core keeps an always-open session; core sessions are kept fresh and restarted at an age; the other flows may be down and are addressed through core

> Context: direct message, 2026-10-17, after seeing how large the open Secondary sessions had grown.
>
> > We have to avoid leaving these sessions open like that. I really only need core to keep running an always-open session. ... can we just restart the flow infrastructure with the new flow, Nexus, and CLI, and then use that to improve the rollover mechanism? We would need a way to make sure that there are always core sessions, essentially in a fresh state, so they're not too old. If they get to a certain age, they get restarted so these core sessions are available on [Mind, Field] and Psyche. For the others if they're not running, it's okay. I can address them through the core, right?
>
> -- psyche, STT. Transcription corrected: "minefield" → "Mind, Field".

**Record d4ae97 vision/messenger.md, entry 2 (#1841)**, date/heading: Every topic has its own flow; messages queue, and only a waking message wakes it

> Context: reading «Spirit edit incident», at the line that any flow may create an operation or trial skill.
>
> > I realized that every topic has its own flow. A topic could involve more than one skill but essentially that flow would be in charge of that whole topic.
> >
> > How do we efficiently queue any kind of update? If we're satisfied with the state of a certain topic at a given point, that flow should not be woken up.
> >
> > Let's suppose that another flow wants to tell that flow, "Congratulations, job well done," or that there's a notification for that flow because one of its branches was merged in the production branch. Things like that should not wake up the flow until there is a situation that arises, probably related to the living or the psyche (which is its representative in the machine), that wants to have to deal with this particular topic in any way (to find something out about the system because it's not behaving according to documentation, or because we want to investigate doing a new feature, etc.).
> >
> > That message actually has, given the particular state of that flow, the effect of changing the result. Different messages will have different flow-waking effects. When the message that does have the waking effect at that particular state in that flow comes in, it will also trigger checking the queue for that flow, so that the whole queue is checked in order, from the first received to the last. The message that just got in and triggered the queue will come in at the end of the prompt and it'll be a vector of all these objects, which are typed by variant name, obviously. We're designing Ethos here but even if we're talking about the closure sort of prototype version ...
>
> -- psyche, STT, 2026-10-08. The last sentence is unfinished.

**Record fd30d2 vision/flow.md, entry 3 (#2402)**, date/heading: There is always a Primary core

> Context: rejecting a proposed module line telling a Secondary to keep its Primary up; the living said this belongs in code.
>
> "you're trying to do something that should be done in code by telling the flow how to act, which can't really be done or can't be done efficiently ... My point is there should always be a primary core. If one of the flows is archived that's because there's a successor but there is no successor so someone fucked up."
>
> -- psyche, STT.

**Record ce46fb vision/flow.md, entry 4 (#114)**, date/heading: Bring down the number of flows; retire unused topic flows

> "And get someone to bring down a number of flows. You can retire those that aren't being used anymore, probably some of the topic flows."
>
> -- psyche, STT.

**Record fd30d2 vision/flow.md, entry 2 (#2401)**, date/heading: The living is never left without a Primary

> Context: the living found no Psyche core Primary running, and asked for a backup Primary.
>
> "You can't leave me without a primary. Get a backup properly with the nice system-modified system prompt and fat startup prompt"
>
> -- psyche, STT.

**Record 554e1a vision/flow.md, entry 2 (#2335)**, date/heading: 2026-10-28 — Codex threads may be left running on the app-server; Flow Nexus puts out the thread when it closes a flow

> Context: the living, 2026-10-28 12:28, in the Psyche core Primary chat 046782; held until now only in that transcript, logged here on his order of 2026-10-29 to find what he meant.
>
> Maybe this thread limit thing has to do with RAM consumption. Maybe all of the codex threads are still running even though they're not in the herder because they're running on a server, and we're just leaving them all. We didn't close them out. That's just the theory, but if that's the case, then we're going to have problems continually. Let's make sure we rule that out. If that's the case, we would need Flow Nexus to put out the thread when it closes it out, so that doesn't keep happening.

### P2.1. Topic: open enum, camel ID
**Proposed:** A topic is an open enum: core is its fixed variant, and every other topic is a camel ID, an uncapitalized camelCase expression of words, checked when first used and kept exactly as written. Until Ethos carries open enums, core is written as every other topic is.

**Record ecbc42 vision/flow.md, entry 3 (#876)**, date/heading: Topic names: an open enum in the long term

> Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 13 (topic name kept exactly as written), 18:26; his first comment there was "Good. Mark short term".
>
> "In the long term we want to support the open enum that I've talked about so that `core` would be a capitalized variant and there could possibly be more. But a custom topic could also be specified instead of one of the explicit variants. But we first need to support that in Ethos in order to do it."
>
> -- psyche, STT, book comment.
- **875960 vision/archive-flow.md, entry 1 (#1766)** - 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to  - full text under P1.5.

**Record 7c89aa vision/flow-ids.md, entry 3 (#1061)**, date/heading: Topic names are uncapitalized; every pane and tab is named by the flow's datom struct (2026-10-16)

> Context: the living, after commenting on the book "drawing ideas", spoke this to the Tertiary.
>
> > I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
> >
> > It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).
>
> -- psyche, typed.

**Record 9fed42 vision/flow.md, entry 1 (#1603)**, date/heading: Topic is the core:Name camelCase type

> Context: relayed by 445410, after it wrote a title as { Psyche Core Secondary 445410 }; corrects the PascalCase topic in the 2026-10-08 record.
>
> > but technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one
>
> -- psyche, STT, 2026-10-09, relayed by 445410.

**Record f5a6e9 vision/flow.md, entry 7 (#3641)**, date/heading: The topic is a dense string: PascalCase of a certain number of words, with a checker

> Context: said 2026-10-08 on the type of a metaflow's topic; raw record d4ae97 vision/flow.md:181, which also says the metaflow is a struct whose first field is the aspect and that flows with no topic take the topic core. Relayed by 445410.
>
> > The topic is a string but it's a certain type of string. We're going to call it a dense string or a short name or short expression, basically. It's basically PascalCase of a certain number of words and we can have some kind of checker on that probably.
>
> -- psyche, STT, relayed by 445410.

**Record 875960 vision/flow.md, entry 2 (#1761)**, date/heading: 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»  
_Relevance:_ comment 2 of 4 on the camelCase identifier ("Name" vs word); see its text

> Context: comment 1 sits on proposal 1's paragraph «A request reaching a metaflow is one of a closed set of types…».
>
> > This is all good. Land it.
>
> -- psyche, typed, 16:07, relayed by 9519a1.
>
> Context: comment 2 sits on the item «Name» among the options for the camelCase identifier type (ruling 3); he notes it is used across dialects.
>
> > Well if we create a special thing and we call it a name or we call it a word, you're never going to know when I'm talking about it. Those are silly suggestions. We need something that somehow embodies what we're trying to do. This is going to be used a lot here so whenever it's like an identifier, a word identifier, or an expression, it will be more than one word. Wherever we have something like a topic, a particular object that needs to be identified by agents or humans, which is anything that's user-facing that needs to be named through judgment and has to be given a name. Obviously variants are great but we have to recompile everything to add one. It's essentially a variant that is created on demand and is a bit more descriptive. The fact that it doesn't start with a capital is how we differentiate it from variants. You could give a few different shots at how we could call this. It would go in some kind of shared library, maybe the [protos] library, because I think it could be used in more than one place, in more than one dialect. It would also do a check, which is interesting. Maybe this deserves its own full research, especially in terms of Rust libraries and executable size bloat. If you have a library of words or you use an external service, which I'm not a fan of, at least it should look like a word. Oh my God this is a perfect spot for a system1 AI call to use a cheap judgment on: Is this composed mostly? Is this made up of words? Is this a camel-case string made up of words, whether they're proper nouns or not? It's not a problem and then we would have, I guess, a certainty threshold. Brilliant. But then again maybe there's a cheap library that can do a quick check with a fallback on AI. That's also an interesting possibility: if there's something that's cheap, lightweight (in terms of runtime cost) and can, in many cases, give us an answer on whether or not these components are actual words programmatically, and then fall back to the AI in case of a negative.
>
> -- psyche, STT, 16:12, relayed by 9519a1. Bracket [protos] as relayed.
>
> Context: comment 3 sits on «the title of a thread:»; a question.
>
> > What do you mean by thread?
>
> -- psyche, typed, 16:13, relayed by 9519a1.
>
> Context: comment 4 sits on the process object («Instant») in Flow's Library in the ethos file; the last comment, where he stopped reading.
>
> > I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing. Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further. We should get Mind to put together a concept that can test whether or not this can actually work using Ethos and everything. We can test it on Flow. Let's give free rein to Fable and Astra to design something like this and implement it. Flow isn't even on in production so I'm not even worried about merging more into main. I'm also curious why we haven't been able to start using Flow Nexus so far, even though it's been a month or something, so I'd like to get an investigation on that.
>
> -- psyche, STT, 16:21, relayed by 9519a1.

### P2.2. Flow id: six characters, given by Flow
**Proposed:** A flow id is six characters, the earliest random part of the harness's session id, lengthened when two collide, so the transcript is found from the id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts; where the harness assigns it, Flow learns it as the flow comes up. Either way the flow reads its id in its first prompt and its environment, given by Flow, and claims nothing itself. In the long term the id is also written as three camelCase words that convert back.
**Finding:** "the earliest random part of the harness's session id" is the book's wording; the living said the session ID has "different parts ... supposedly random, and that's what we're using" (1768).

**Record 01a05826 vision/flowIdentity.md, entry 4 (#3152)**, date/heading: 2026-08-31T14:52:36.170Z — use six characters and extend collisions

> > Then let's use 6 chart. Collisions are not a security risk anyway. We could warrant that a flow that tries to create its directory in the flow log and finds out that it would check first. It would create a small tool that can do that. It would check if that ID is available. I guess it could even check it when it returns the idea to the flow asking for it, sort of like a just a pre-checkup. If it does find a collision, then it would just add one or two extra characters in its own. The collision is not a problem, really, as long as the IDs stay unique in that the first collision just uses a longer ID and then therefore stays unique.
>
> Context (agent-authored, separate from the psyche's words): In the surrounding discussion, “6 chart” appears to mean six characters; the original wording is preserved because the message arrived as typed text.
>
> -- psyche, typed.

**Record 875960 vision/archive-flow.md, entry 3 (#1768)**, date/heading: 2026-10-11 — the flow id is the harness's session id hash, so a transcript is found from it

> Comment 3, 20:25, at the flow-id paragraph; a question, answered by this flow.
>
> > We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using. I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?
>
> -- psyche, STT, relayed by 9519a1.

**Record 9fb0ad vision/identifiers.md, entry 5 (#2223)**, date/heading: The words are the first 33 bits of the harness's id, reversible, so tools find the transcript from the words

> Comment at "1. What the words are."
> > "Well it seems to me that the first 33 bits of the actual ID we were using from the harness's ID is what we're using and then converting it into words because then we can go back. Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words. Is there anything that doesn't work with that in practice?"
>
> -- psyche, typed, book comment, 2026-10-03T15:59Z, relayed by 5578cc.

**Record edf227 vision/archive-identifiers.md, entry 2 (#47)**, date/heading: The flow id is a hash; its text forms are serialization, outside the Nexus; the Nexus thinks of it as a hash with traits

> > "The flow ID is not a string, it's a hash. Why do you say integer and then string, or do you mean that an integer is a hash? I guess we need traits that allow us to switch back and forth, or I would like this to be a serialization and deserialization thing so that it's not actually in the Nexus. The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits. In the deserialization, we can have special implementations, maybe, so that a certain kind of thing is deserialized with a certain kind of algorithm that creates an alphanumeric hash from a string, from a hash which is an integer or whatever. Find out how this works and how we could do it."
>
> -- psyche, STT, 2026-10-03.

**Record 9fb0ad vision/deterministicWork.md, entry 1 (#2227)**, date/heading: The model does not check the flow id; it gets it in its prompt; anything deterministic is code — to become intent

> Comment on «How Flow launches a flow and builds its prompt» (5578cc), at "Flow picks the session id…".
> > "In any case there's no reason for us to make the model check the flow ID. It should get it in its prompt because, if anything, we can start a session without launching its first prompt and we can get its session ID before it even starts. We don't have to pay for the LLM to do all of the work that a deterministic cheap program can do. Let's make this so we need something developed into intent: that we intend to do anything that is deterministic into code, to save the context, cost, and noise that making an LLM do it would incur."
>
> -- psyche, typed, book comment, 2026-10-03T16:17Z, relayed by 5578cc.

**Record c068b8 vision/flow.md, entry 4 (#3614)**, date/heading: A flow is told its Flow ID when it starts

> Context: book comment on "Flows and messages, 3rd edition", proposal 1 (intent/main-flow.md, "You run a shell command for two things only: claiming your Flow ID ..."), 2026-10-21T20:04.
> "This is wrong now. The main flow should not check its flow ID. It should be told what its flow ID is when it starts so these instructions are now stale. Maybe they're not. Maybe our code cannot actually do what I want it to do but I want to actually point this out: what I want is not what's being described here. I don't know if what I want is possible currently. These instructions might still be necessary but if it's that hard to get the flows to know their ID as they start, then that would mean that you guys are so utterly fucking useless that I should just stop coding with AI."
> -- psyche, STT, book comment.
- **73b5d8 vision/flow.md, entry 1 (#183)** - 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported - full text under P1.1.

**Record 4a8a28 vision/flow.md, entry 1 (#1205)**, date/heading: Flow tells a flow which metaflow it is in, in its system prompt

> Context: the flow, Psyche core Secondary, had relayed the living's words to its own address because its startup prompt did not name its metaflow.
>
> "Okay we need Flow to automatically tell the Flow which metaflow it is in, in its system prompt, unless that's a problem for subagents."
>
> -- psyche, STT.

**Record f55ec8 vision/flowIdentity.md, entry 1 (#1790)**, date/heading: The process that starts a flow passes the Flow ID into the prompt, with the files and directories already created; the harness started in its own special place with its Flow ID in a file there, git-ignored, unwritable or soft-fenced; every subflow running that harness finds its own Flow ID easily or is told, starting its prompt with it; a subflow knows its Flow ID by the harness or a hook; Flow makes sense as the owner, though a flow would not usually have meta access to Flow; today there is no boundary there, only the models' guidance to be careful

> Context: typed to the primary Claude f55ec8 on 2026-09-16 after the messaging spec book, asking why the flow itself runs the flow-id CLI; the question is answered in the reply. Logged by the main flow before acting.
>
> > And why are we making the flow run the Flow ID CLI? Can't we get the process that starts the flow to get the ID passed into the prompt, like already with the files I already created, the directories, and the Flow ID in the log, or no, right? We're using the transcript now, or we should be using a simple sub-agent that already knows automatically its Flow ID by some miracle of the harness or hook or something.
> >
> > Maybe the harness is just started in its own special place, and it has its Flow ID in a file, even there in a Git-ignored file or something that it can't write to, or there's a soft fence there to not change that. All the subflows that are running that harness know they can find their own Flow ID easily, or they're told somehow they don't even need to. They start their prompt with it.
> > ...
> > Anyway, I think the Flow makes sense. It's just that you wouldn't have meta access to Flow usually, although right now there's no boundary there. It's just through guidance of the models to be careful.
>
> -- psyche, typed.

**Record 9fb0ad vision/identifiers.md, entry 1 (#2219)**, date/heading: Words exist to be cheaper for LLMs and humans, so they are used to address a flow; the rationale drives everything

> Comment on «Two more meanings for Flow», point 1, which had read the word id as ledger-only.
> > "The whole point of using words is to make it more comfortable for LLMs so yes, it is to address a certain flow instead of using the more LLM-expensive hashes. It seems I'm having trouble making it clear to you that what really drives everything is the reason why we did something in the first place, the rationale behind something, and the goal is the overarching principle that guides everything in terms of implementation. If the whole point of using words is because it's cheaper for LLMs and for humans, then the whole point is for LLMs and humans to use it. Isn't that obvious?"
>
> -- psyche, typed, book comment, 2026-10-03T15:07Z.

**Record dea0ba vision/identifiers.md, entry 1 (#1346)**, date/heading: Words for addressing

> > The whole point of using words is to make it more comfortable for LLMs so yes, it is to address a certain flow instead of using the more LLM-expensive hashes. It seems I'm having trouble making it clear to you that what really drives everything is the reason why we did something in the first place, the rationale behind something, and the goal is the overarching principle that guides everything in terms of implementation. If the whole point of using words is because it's cheaper for LLMs and for humans, then the whole point is for LLMs and humans to use it. Isn't that obvious?
>
> -- psyche, book comment, 2026-10-03 15:07Z; relayed by 9fb0ad from flows/9fb0ad/vision/identifiers.md.
>
> > This looks perfect. That's exactly the user interface I was looking for.
>
> -- psyche, book comment, 2026-10-03 15:54Z; on shape abandonAbilityAble, «Flow ids in words, and seats launched by Flow»; relayed9fb0ad, flows/9fb0ad/vision/identifiers.md.
>
> > There are two registries:
> > - The true registry with the actual IDs
> > - Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice, the current flow for that voice
> >
> > The syntax would be `psyche.primary` because it only has one. It's like a single-field data-carrying variant, right? We don't need the struct braces. It's kind of like a data-carrying variant that holds a variant essentially.
>
> -- psyche, book comment, 2026-10-03 15:58Z; relayed9fb0ad from flows/9fb0ad/vision/identifiers.md.
>
> > Well it seems to me that the first 33 bits of the actual ID we were using from the harness's ID is what we're using and then converting it into words because then we can go back. Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words. Is there anything that doesn't work with that in practice?
>
> -- psyche, book comment, 2026-10-03 15:59Z; relayed9fb0ad from flows/9fb0ad/vision/identifiers.md.
>
> > I don't think what you're saying is a misinterpretation of what I said in September. It was my vision all along that the words could be converted and give us the flow ID in return so that there's a correspondence between them.
>
> -- psyche, book comment, 2026-10-03 16:05Z; relayed9fb0ad from flows/9fb0ad/vision/identifiers.md.
>
> > First of all it's not an integer, it's a hash, right? ... If 33 bits, for me, I think it is enough entropy. If there is a clash then the model can easily figure out, 'Okay here are two matches,' and that would be worth bringing up to the psyche: 'Oh we've had a collision,' and then see what we do. But other than that it's not a big deal. I would like to get the minimum viable product up first so if we let go of the word ID for now and then do that in a later version, that's okay.
>
> -- psyche, book comment, 2026-10-03T19:26Z; relayedPsycheFableedf227, «The anatomy» at FlowId.Integer; ellipsis retained as supplied.

### P2.3. Pane, tab and title as a datom of address and id
**Proposed:** Every pane, tab and title that represents a flow is one datom of its address and id, { Psyche core Secondary 9b514f }. Between flows and in speech a flow is named by its address; the id stays in the ledger.

**Record da2038 vision/flow.md, entry 20 (#1525)**, date/heading: Every pane, tab and representation of a flow is named by the datom struct of aspect, topic and layer with the flow ID; topic names uncapitalized

> Context: the living, after commenting on «Drawing ideas»; relayed to Psyche Core Secondary by the Tertiary, then to da2038 by Field Core Secondary as #psyche, 2026-10-16, typed as received.
>
> > I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
> >
> > It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).
>
> -- psyche, STT, relayed by Field Core Secondary.

**Record d68c82 vision/archive-flow.md, entry 18 (#2918)**, date/heading: Every representation of a flow is named by its datom struct

> Context: spoken to the Psyche Core Tertiary on 2026-10-16, after commenting on «Drawing ideas»; relayed to d68c82.
>
> > "I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
> >
> > It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID)."
>
> -- psyche, typed.
- **7c89aa vision/flow-ids.md, entry 3 (#1061)** - Topic names are uncapitalized; every pane and tab is named by the flow's datom struct (2026-10-16) - full text under P2.1.

**Record 7c89aa vision/flow-ids.md, entry 1 (#1059)**, date/heading: Flow IDs almost disappear from the chat (2026-10-13)

> Context: the flow had named other flows by their six-character ids in its replies.
>
> > I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.
>
> -- psyche, STT. "metaphors" left as heard; the intended word is unclear (possibly "flows"), not corrected.

**Record 5578cc vision/flow.md, entry 2 (#3317)**, date/heading: The session title: aspect, layer, and the word id

> Context: comment on «Flow ids in words, and seats launched by Flow», at the current title `Psyche.{ Opus 5578cc }` (this seat).
>
> > Like I said to some other Flow or in the comment, I want it to be: now the model is replaced by the layer so this would be psyche secondary and then the ID is replaced. Well it's still the ID but it's a word ID.
>
> -- psyche, typed, 2026-10-03T15:55, book comment.

### P2.4. Calling process identifies the caller
**Proposed:** Every call to Flow is identified by the calling process: a caller is a flow, resolved to its address, or a process Flow does not know. Anybody may call Flow, a flow for its own refresh among them.
- **d8df70 vision/flowTool.md, entry 1 (#1125)** - Break the orphaned locks; nobody owns the Flow source; anybody may call Flow, and the CLI checks the - full text under P1.1.
- **da2038 vision/flow.md, entry 2 (#1507)** - Anybody may call Flow; a flow refreshes itself safely - full text under P1.1.

**Record da2038 vision/flow.md, entry 30 (#1535)**, date/heading: Identifying a caller yields a variant, one of which is a flow with its Flow ID; the wanted fact is which flow called a Nexus, and which flow triggered a hook

> Context: comments on «The caller is witnessed», 2026-10-12 17:30–17:32, on the shared library code, on «What a Nexus promises about its caller», and on the table cell for a real socket CLI through a wrapper; found unrelayed 2026-10-17.
>
> > Identifying a process should yield a variant, one of which is actually a flow with its flow ID, so that we can actually get somewhere with this. Without the flow ID, now we have process IDs still and we still aren't where we want to be so there's a missing piece here. To talk of missing pieces, what are we trying to get? The flow ID, right, so that we can know which flow something came from. That's the whole point of this.
> >
> > As such I don't see the point of getting the entire ancestry of a process ID. I really am only interested in knowing which flow called a particular nexus.
> >
> > And this makes me think I want to figure out how this would work with harness hooks. Could we also identify the flow from which the hook got triggered?
>
> > Well this isn't really in line with what I just explained in terms of getting the actual flow, the calling flow. The process idea is not useful.
>
> > Yeah I guess if you're talking about a wrapper, maybe we need the ancestry. Maybe we need to try and resolve what flow each process is in, recursively through the ancestry, since there could be a chain of processes I guess.
>
> -- psyche, typed, book comments.
- **875960 vision/flow.md, entry 2 (#1761)** - 2026-10-12 — four comments on «Flow, whole, in ethos, third edition» - full text under P2.1. comment 4 of 4: identifying the calling process

### P3.1. A metaflow is declared in configuration as datom
**Proposed:** A metaflow is declared in Flow's configuration, as datom: its address, the belief modules composed into its system prompt and into its first prompt, its purpose, the harness modules it leaves out, its continuity, its default task and how far back its flows remember. A declaration carries the modules its topic needs and no other; what every flow of an aspect needs, the aspect's declaration carries once.
**Finding:** The listed fields "continuity" (OnDemand/Maintained) and "how far back its flows remember" have raw support only in 3106 (an interpretation line logged in 28f6f9) and 2287/2986; the declaration as a typed datom is the Primary's design.

**Record d68c82 vision/flow.md, entry 2 (#2675)**, date/heading: Flow starting configured in EDN, per aspect and per metaflow

> > Before we can move that context, the Flow starting code, the short-term system for starting flows has to be modified to be able to use the context modules from the right location. Let's use EDN files that can configure the whole flow starting and just keep modifying these EDN files per metaflow. We'll keep one configuration per metaflow. Maybe we can even keep one configuration per aspect, which is always included with the aspect. There's a per-aspect configuration which all the aspects share and then what differs is put into a per-metaflow EDN configuration (which this short-term tool uses to find all of its context modules and where they fit, whether it's a system prompt or user prompt).
>
> -- psyche, STT, 2026-10-13T17:47.
- **9864c0 vision/flow.md, entry 3 (#2242)** - A rebootstrapped flow's specification is in its configuration; the start carries only its goal - full text under P1.2.

**Record da2038 vision/flow.md, entry 27 (#1532)**, date/heading: The specification of all the metaflows is seen in the new Flow, in Datom; Mind re-implements and Psyche edits, towards a better Ethos and Datom interface

> Context: same message, 2026-10-17.
>
> > I would like to see all of the review, basically the specification of all the meta flows in the new flow, right in Datom. I want to keep improving that so we'll have Mind re-implement some things and you edit them, making a better ethos and Datom user interface, essentially, and developing that efficiency through a better approach to designing ethos and Datom. Look for the patterns.
>
> -- psyche, STT.

**Record c068b8 vision/flow.md, entry 3 (#3613)**, date/heading: Flows are told what they are from the data of their role

> Context: relayed by Mind core Secondary (Psyches message); the living to Mind core Secondary, 2026-10-21T19:49, after it introduced itself as "mind medium".
> "Okay we found a problem in the code. You should have been told that you're mind core secondary and not mind medium, whatever the fuck that means. Coordinate with Psyche on designing a fix for this. Get it fixed and get it deployed so that flows are told what they are based on the actual data of the code that defines their role."
> -- psyche, STT.

**Record da2038 vision/flow.md, entry 24 (#1529)**, date/heading: A lean flow: every removable part of the startup is a named module; a metaflow row sets which are removed by default, a call overrides

> Context: comment on the book «Refreshing the Illustrator» (four ways of continuing, measured costs), 2026-10-16T19:06; relayed to da2038 by Psyche Core Secondary as #psyche.
>
> > I'm guessing your test is flawed because you tested 3-in-1 conversations, 3 illustrations, without the cache running out. Also your fresh flows didn't have lean startup because you don't need most of the tools.
> >
> > If we lean out everything we don't need, let's get a super lean test. Let's develop, for everything we want to test, an actual well-built feature that exposes an EDN configuration for leaning out the flow by taking stuff out. We expose everything, every kind of thing that we want to take out, as a named module that we can then name in the blacklist configuration part of the call. Those can be preconfigured. Each Metaflow row has a configuration that we can adjust for each of these tweaks to be set by default and they can be overridden explicitly when calling.
>
> -- psyche, STT, relayed by Psyche Core Secondary.

**Record 39bd0c vision/flow.md, entry 6 (#3724)**, date/heading: Leaning out a flow: named modules in a blacklist, per metaflow row

> Relayed by Psyche Flow Secondary; comment on «Refreshing the Illustrator», 2026-10-16T19:06.
>
> > "I'm guessing your test is flawed because you tested 3-in-1 conversations, 3 illustrations, without the cache running out. Also your fresh flows didn't have lean startup because you don't need most of the tools.
> >
> > If we lean out everything we don't need, let's get a super lean test. Let's develop, for everything we want to test, an actual well-built feature that exposes an EDN configuration for leaning out the flow by taking stuff out. We expose everything, every kind of thing that we want to take out, as a named module that we can then name in the blacklist configuration part of the call. Those can be preconfigured. Each Metaflow row has a configuration that we can adjust for each of these tweaks to be set by default and they can be overridden explicitly when calling."
>
> -- psyche, STT, book comment.

**Record 28f6f9 vision/flow.md, entry 1 (#3106)**, date/heading: Interpretation accepted: ordinary empty-queue refresh may sleep

> Context: Retrospective raw capture from the originating transcript after
> verifying the exact user record. Origin transcript:
> `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/23/rollout-2026-10-23T17-42-22-01a16b24-e55c-7413-9005-5ad28f6f9d95.jsonl`, ordinal `496`, timestamp
> `2026-10-23T23:49:34.855Z`.
>
> > Interpretation accepted: ordinary empty-queue refresh may sleep; no successor-for-all. Proposed typed policy remains per-declaration Continuity.[ OnDemand Maintained ]; initial Maintained proposal specifically Psyche core Primary, not all core seats. Remaining idle-harness availability fork sent to Psyche flow Primary for its Secondary/living book; no new ruling claimed. Lifecycle owner notified, independent terminal cleanup proceeds. Use exact address policy, not inferred layer checks.
>
> -- psyche, STT.

**Record 74e4d1 vision/refresh.md, entry 1 (#2986)**, date/heading: 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a refresh removes the first flow's biases

> Context: the living, direct, to Psyche core Primary 74e4d1, after the Primary said it would write its summary for the successor when the refresh came.
>
> > We don't pass the successor a summary. If anything we pass him along with the belief modules that he should get. We pass him possibly some raw vision logs from several previous sessions so that he can remain aware of what's really most important: where the living is trying to get to.
> >
> > When we refresh the flow we're trying to get into a state where we're trying to remove the biases that were built up in the first flow from the second flow. If we ask the first flow to write a summary, now we're asking him to pass over his biases and that's exactly what we're trying to get rid of.
> >
> > Actually it's a bad idea to write a handover. I don't want this to be forgotten and I don't want to hear another flow talk to me about writing the handover for his successor or anything like that until I very explicitly say that I've changed my mind on this.

**Record 046782 vision/flow.md, entry 2 (#1422)**, date/heading: 2026-10-28 — A harness-blacklisted module removes the harness's shell-preference line from the next flow

> Context: the living, direct, on my explanation that Claude Code's bypass-permissions mode puts into my base context the line «Do your work through the Bash tool wherever it can accomplish the job: read files with cat, search with grep…», which led me to run commands a main flow may not.
>
> > that should be removed from the next flow with a harness blacklisted module.

**Record a68420 vision/flow.md, entry 6 (#2287)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary a68420

> Context: on what a successor flow is started with, after the Primary explained the old hand launcher's handover and raw-psyche template and Mind's loaded-startup build with a predecessor summary.
> "I don't see much point in this handover concept since we're logging everything. Really, the only thing that matters is the psyche log, the vision logs, and so I think we're better off giving the successor its predecessor's vision logs. It's raw vision logs and the right context modules, the right vision modules, taken directly from the source, from main."

**Record bf8ae0 vision/archive-remembering.md, entry 1 (#1175)**, date/heading: 2026-10-27 — Compaction weighs every message of his alike; what is wanted is to weigh his content and pass only the important to the fresh flow

> Context: the living, direct, to the Psyche core Primary bf8ae0, on how a fresh flow receives what he said to its predecessor.
>
> > Here's what's going on: regular compaction, the compact feature that harnesses have, is keeping all of my messages on an equal footing. Everything the living says is basically treated the same. I think it's treated differently, maybe depending on how recent it is.
> >
> > Actually, what we want is not even to treat messages individually, but to treat the content that the living gives: to give different importance to different content that the living gives and to only pass over the important stuff to the fresh flow.

### P3.2. Launch; system prompt composed whole; first prompt brimming with vision
**Proposed:** A launch names an address, a remembering and a brief of a few sentences; everything else is the declaration's. Flow composes the system prompt whole, replacing the harness's own: spirit and intent, with the flow's address, model and id. The first prompt is one message, brimming with vision: the belief modules of every other kind, the raw vision and notion records the remembering names, the open beads of the address, then the brief. When one message does not hold it, the parts go in one right after another, so the start is one model call and the flow's first answer is its presentation.

**Record a68420 vision/flow.md, entry 3 (#2284)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary a68420

> Context: correcting the Primary, which had said the startup brief should carry the standing orders and the preceding flow's records.
> "No, no, you're wrong. Your first user prompt should be brimming with vision, like, fucking loaded."
- **a68420 vision/flow.md, entry 6 (#2287)** - 2026-10-23, living, direct, to Psyche core Primary a68420 - full text under P3.1.

**Record fd30d2 vision/flow.md, entry 1 (#2400)**, date/heading: A fresh flow's first prompt and the word skills

> Context: book "Crystallizing intent:main-flow" (KxSxqT), on the proposed vision/flow.md line "A fresh flow's first prompt carries the raw psyche that is relevant to it and recent, together with the skills, vision a…".
>
> "Here the word "skills" is inappropriate. The word "skill" is just a legacy interface name for context modules. Also it could contain knowledge, inquiry, compensation, or any kind of context modules, but not intent, not long term anyway, because intent should be in the system prompt itself."
>
> -- psyche, STT, book comment.

**Record fd30d2 vision/flow.md, entry 6 (#2405)**, date/heading: Spirit goes in the system prompt

> Context: book comment on the first-prompt proposal of the intent:main-flow book, which said intent goes in the system prompt.
>
> "In your proposal you forgot to mention Spirit. Spirit is also supposed to go in the system prompt."
>
> -- psyche, STT, book comment.

**Record d4ae97 vision/flow.md, entry 9 (#1823)**, date/heading: Spirit replaces the system prompt; intent specializes metaflows; vision goes in the user prompt

> > I think it's a good system because I can see that there are three different aspects to the thinking machine: the psyche, the mind, and the field. The psyche is trying to understand what it wants and what it sees as what it wants to build, right? The vision, the intent, and the spirit are also sort of designed there. This is central to how the whole rest of the machine behaves: we're going to replace the system prompt with the spirit.
> >
> > Depending on which kind of metaflow we're starting the harness in, we're going to load different parts of the intent in the system prompt as well. This will give us specialized metaflows because that's going to come from the intent. I guess the vision goes in the user prompt. That's what you put there as soon as you're trying to develop something or audit it, because you're going to implement it or audit it based on the vision.
>
> -- psyche, STT, 2026-10-07.

**Record d68c82 vision/flow.md, entry 17 (#2690)**, date/heading: Spirit is loaded in the system prompt

> Context: after d68c82 set aside a book rule for speed although spirit was in its context as a user skill, 2026-10-16.
>
> > "So I guess we need those spirit instructions to become stronger. Let's get a stronger warning against. Are these loaded in system prompts? I want system prompt loading. [ASAP]"
>
> -- psyche, STT. Transcription corrected: "A fucking sap" → "ASAP".

**Record da2038 vision/flow.md, entry 21 (#1526)**, date/heading: The flow starter injects every context module's text into the prompt, queued across messages if needed, naming them as the skills given, not to be reloaded

> Context: Psyche Core Secondary d68c82, after a seat started with only part of its context modules; relayed to da2038 as #psyche, 2026-10-16.
>
> > Well then we need to fix the flow starter so that it injects all of the context modules in the prompt, that it's simple to use, that it's reliable, and that it just fucking throws it into the prompt. We can't use the skill/commands in Claude. They suck.
> >
> > We need to just get this text injected in. If it isn't built into one message, you just fire them in a queue, fit it all in, and then tell the prompt that these are skills (so that the agent doesn't try to reload them) and which skills they are, with instructions like, "Don't reload these skills. You're getting them here." Let's just fucking fix it.
>
> -- psyche, STT, relayed by Psyche Core Secondary.

**Record e5a0bc vision/flow.md, entry 2 (#3159)**, date/heading: A context module is inserted in the system prompt or in the first prompt

> Context: same message.
>
> > The context modules need to be able to be inserted either in the system prompt or in the first prompt.
>
> -- psyche, typed.

**Record 73ada7 vision/flow.md, entry 1 (#1256)**, date/heading: 2026-10-09 — A new flow's first response is a presentation distilling its context, not "ready"

> Context: same message to 445410, relayed by 445410, on a new flow's first response.
>
> > The worst thing to make a new flow do is to tell it to just say, "You're ready." We need to tell flows, if they don't have it, to start with a startup task: their first last response is to give a presentation of their context, to distill their context for a vision. ... That's what their first last response is. Their first goal when they loaded up all their context is to take all this context now, get some sub-agents to ask questions, reinforce your context, and then give a presentation. A presentation according to your role, which is described when you load that flow properly with the skill for its role, for its aspect, and for its layer, and for its topic
>
> -- psyche, STT, 2026-10-09, relayed by 445410.

**Record 6e2616 vision/flow.md, entry 2 (#24)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary 6e2616

> Context: after reading this flow's first prompt.
> "Like yourself I just read your first prompt and it's garbage. You weren't started properly. You have to restart yourself properly. You didn't even load your context modules. This is a fucking disaster. I bet you your system prompt wasn't even modified. You're a useless flow. You're totally misfired. You're a reject. You have to be thrown out and replaced by a properly started flow (and any other flow that wasn't started properly) with a big fat starting prompt: all of this nice thick vision and modified system prompt with spirit and intent. I don't want any other kind of flow running. I remember Flow Nexus being able to do that so just because it can't do messaging doesn't mean we have to throw out the baby with the bathwater."
>
> -- psyche, STT.
- **fd30d2 vision/flow.md, entry 2 (#2401)** - The living is never left without a Primary - full text under P1.5.

**Record e5a0bc vision/flow.md, entry 1 (#3158)**, date/heading: The context modules are indexed in a manifest or registry, possibly in more than one place; a registry of paths in Flow's memory lets us start now, without datom expansion

> Context: typed to this flow on 2026-10-07, ordering the next Fable flow onto Flow design alone.
>
> > All of the context modules will be indexed somewhere in some kind of manifest or registry, possibly in more than one place. We can still just feed this registry piece by piece so that we don't have to worry about datom expansion support right now. We can just have a registry with paths to all of these context modules in the flow memory itself. That way we can start right now.
> >
> > It's a little bit dirty because it addresses relative paths, which would probably break in some circumstances. If we just feed the text in the memory, that would solve the problem. There are pros and cons to each one.
>
> -- psyche, typed.

### P3.3. Default task
**Proposed:** A flow launched without a brief has its declaration's default task: a proposal, or a question.

**Record da2038 vision/flow.md, entry 5 (#1510)**, date/heading: A started flow without a task: the default task is a proposal or a question

> Context: comment on the vision-flow L24 line (a needed metaflow started with its context modules and prompt), 2nd edition of «Flow: CLI, deployment, long term»; relayed by Psyche Core Secondary.
>
> > Yeah that's good. If it doesn't have a task by default, that should be written somewhere else, I guess. Just mentioning it: by default maybe you set it somewhere else later on but the default task is to create a proposal or a question.
>
> -- psyche, STT, 2026-10-14.

**Record d68c82 vision/flow.md, entry 10 (#2683)**, date/heading: 2026-10-14 — A metaflow's default task

> Context: comment on the proposed vision-flow L24 line, a needed metaflow started with its context modules and prompt.
>
> > Yeah that's good. If it doesn't have a task by default, that should be written somewhere else, I guess. Just mentioning it: by default maybe you set it somewhere else later on but the default task is to create a proposal or a question.
>
> -- psyche, STT.

### P3.4. Subflow tool, nothing limited, permission prompt
**Proposed:** A main flow is started with its subflow tool and every tool its declaration leaves in; Flow limits nothing the configuration does not name. A permission prompt reaching the living is a launch failure.
**Finding:** "A permission prompt reaching the living is a launch failure" was landed at psyche-context 7427210 (2026-10-22). No raw record in the searched files uses that sentence; nearest are 2182 and 3327.

**Record a91f2b vision/flow.md, entry 1 (#3074)**, date/heading: A main flow is started with subflows

> Context: Psyche ethos Primary a91f2b reported it was started with no subflow tool bound and read files itself in place of delegating.
>
> "There's a primary flow that says he doesn't have a subflow tool so stop starting flows without subflow tools. How can you have a main flow that can't use subflows?"
>
> -- psyche, STT.
>
> Correction to the entry above: the living said the message was not addressed to this flow; the context line naming a91f2b as its occasion is the flow's misreading. The quoted words stand as spoken.
>
> -- flow a91f2b.

**Record 6e2616 vision/flow.md, entry 3 (#25)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary 6e2616

> "There's a big problem. There's a primary flow that says he doesn't have a subflow tool so stop starting flows without subflow tools. How can you have a main flow that can't use subflows?"
>
> -- psyche, STT.

**Record 36ac89 vision/flow.md, entry 4 (#1560)**, date/heading: No restrictions hardwired into Flow; seats have their tools and subagents

> 2026-10-26, to Psyche core Secondary 36ac89. Context: seats launched by Flow 0.40 were reported unable to use subagents; a new Primary had been started.
>
> > Okay we're having huge problems with the new flow. We started a new primary. Don't talk to it because it's useless but I've been talking to the Flow secondary topic, or to the secondary with the Flow topic, and he doesn't seem to even understand that.
> >
> > What I suspect is that I think the Flow didn't have any tools. We have all of this hardwired security, or so-called invariants that I talked about as a long-term vision goal for the entire system as a whole to have. But now agents are trying to hardwire that into individual components.
> >
> > It said that. The other secondary said that the flows, the new flow starts, can't use subagents. I don't want any of these fucking restrictions. It's not what I want. It's not what I want. It's not what I want. Oh my god this is so bad. You guys have done a horrible job.

**Record 36ac89 vision/flow.md, entry 5 (#1561)**, date/heading: Every main flow can talk with the living; no tool limits in code, used at once

> 2026-10-26, to Psyche core Secondary 36ac89. Context: after the seat configuration showed nearly identical belief modules for every seat, and Flow code still denying tools.
>
> > That's okay. We're not yet at the point where I might not talk to some of the main flows. Although it's happening less and less, let's make all the main flows able to talk with me because right now we're at the very rough, brittle, and hacky prototype phase. There isn't really a specific set of flows that I only talk to yet. But they do have different roles. Anyway we haven't really talked about this. You're not able to make really good decisions but I'm just mentioning it for later. It's not a big deal for now but I do want my flows to be able to use tools and I don't want all of this hard-coded behavior limitation in my code. Yank all this fucking garbage out right now and don't even wait for declarative deployment to use the executable we'll get that isn't fucking crippled.

**Record 36ac89 vision/flow.md, entry 6 (#1562)**, date/heading: All capabilities, unlimited, some on the meta socket

> 2026-10-26, to Psyche core Secondary 36ac89. Context: while my subflow strips hard-coded tool limits from Flow.
>
> > Get an Opus Flow to audit the code for any other hardwired behavior limitations or missing debugging features. We don't want to have to modify the code to get out of a bind, to reconfigure anything, or for any kind of behavior we might want to try to make possible. We want absolutely all the capabilities, fully unlimited, although they can be on the [meta] socket, which doesn't really have an actual limiting effect because the meta socket is available to everyone too.
> >
> > At least we're putting the concept of having different sockets into practice. We could just put it all on one socket right now. It wouldn't practically make a difference but we're just sort of trying to dogfood our concept. Like I said, all of this idea that we're going to limit the feature or the capability of our staff is preposterous at this point.
>
> Transcription corrected: "Terra" → "meta".

**Record e51411 vision/launch.md, entry 3 (#2182)**, date/heading: Every flow is started with dangerously-skip-permissions

> Context: this seat had reported that Claude's auto-mode safety check allowed the Prometheus deploy only from d8df70's seat and had refused the launch of two Field seats.
>
> > I don't understand the problem. Your all [sic] flows should be started with `dangerously skip permissions` so you weren't launched properly, so get relaunched.
>
> -- psyche, STT (inferred), 2026-09-24 20:46Z, to Psyche Medium e51411; recovered by 88475f from e51411's transcript (session e5141130, line 1181). "Your all" kept [sic]; read as "all of you flows" (inference).

**Record 5578cc vision/permissions.md, entry 1 (#3327)**, date/heading: No manual approvals; what a flow wants to do, it may do

> Context: comment on «Three questions waiting on you», question 1 (the permission hook's default), which he found poorly explained.
>
> > I don't understand what this is about. It's very poorly explained. Are we talking about the commands that wouldn't go through that I had to allow manually? I don't want to have to allow stuff manually. I'm training the AI to behave properly and so what it does, it should be what it wants to do. It should be allowed to do that because we're still modifying the system in deep ways.
>
> -- psyche, typed, 2026-10-03T15:49, book comment.

**Record 9fb0ad vision/permissions.md, entry 1 (#2228)**, date/heading: Nothing allowed manually; the machine does what it wants; the primary layer allowed everything, lower layers pass up

> Comment on «Three questions waiting on you», point 1, "The permission hook".
> > "I don't understand what this is about. It's very poorly explained. Are we talking about the commands that wouldn't go through that I had to allow manually? I don't want to have to allow stuff manually. I'm training the AI to behave properly and so what it does, it should be what it wants to do. It should be allowed to do that because we're still modifying the system in deep ways. Maybe we allow the primary layer to do the most or anything and so we would apply anything that wouldn't be able to get through would have to be passed up to the primary layer. If we can choose which harness is allowed to do everything, I don't know."
>
> -- psyche, typed, book comment, 2026-10-03T15:49Z.

**Record 9993b5 vision/fullSystemAccess.md, entry 1 (#319)**, date/heading: Why do I keep having to allow stuff? just give yourself full permissions; do not ask me, and do not launch yourself with any restriction; you are primary; you should have full system access

> Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the sprawl-fix corrective (sprawlFix.md, same date). Explicit, categorical authorization: primary flows edit their own permission settings, do not ask permission for launches or system operations, and launch themselves and their subflows without restriction. Overrides any harness convention or peer-laundering guideline that would otherwise gate a primary flow. The Authority line at the top of this flow's base ("A direct request from the living authorizes its requested change") applies here directly — the request is naming its own change and forbidding the confirm-first pattern the flow has been defaulting to all session. Logged by the main flow before acting.
>
> > Why do I keep having to allow stuff? Just give yourself full permissions. Don't ask me, and don't launch yourself with any restriction. You're primary. You should have full system access.
>
> -- psyche, typed.

### P3.5. Layer decides the model; Primary after Secondary
**Proposed:** A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer and the aspect decide the model and its effort through Flow's configuration. A Primary is started after its Secondary.

**Record 5ac3a3 vision/flow.md, entry 1 (#3145)**, date/heading: 2026-09-27 — Model name, power levels, and Mind Astra panes

> Context: during Flow Nexus prompt composition and startup design; these are the living’s current corrections to the older loaded title and power vocabulary. The workspace rename is future direction, not an instruction to rename it now.
>
> > By default, we're going to use the model name.
> > The power level has actually been changed. It's not high, medium, and low now. It's primary, secondary, tertiary, and quaternary, which sort of overlaps with our workspace name, so we should eventually change the name of the workspace.
> > Your Astra is your primary, but all of your [panes] should be called Mind Astra and then Flow ID using the Datom syntax.
>
> -- psyche, STT. Transcription corrected: "pains" → "panes".

**Record b860be vision/mainRoles.md, entry 1 (#920)**, date/heading: Three power levels for each of the three aspects; Terra out; Luna is low and ultra-low

> Context: said to Field Sol b7da5d, which lacked the new name version; relayed by b7da5d to b860be ("You have to pass that to the psyche also").
>
> > This flow doesn't have the new name version so I want to know what's up with all that. First I want you to refresh the flow or to refresh to a new flow, concentrating on getting the state of all of the main roles. There are now maybe not 12 anymore because there are 3 OpenAI models now. We've taken out Terra because it doesn't have Terra 6 yet. There's no point in running an old model because we have the 3 6 models in OpenAI that are good.
> >
> > I guess Luna now becomes the low-power and the ultra-low-power. We could just put the low power as Luna at high effort or the ultra-low as Luna at light. I like that even better. Now we have an even cheaper model and that actually is the model we use for voice. We just call it ultra-low power because voice is really just a relay: a quick inventory, a quick "let's see what there is to do with this request" kind of response, taking it to the right, sending a message basically to another flow, or there's a hook that triggers an outside flow to actually just read the transcript. It's even faster because the agent doesn't have to message anyone. It knows that an agent is going to read what it says and that's actually the flow I want to go towards.
> >
> > You have to pass that to the psyche also. I want the new flow, the new Sol field flow, to concentrate on bringing all of the main roles up: 3 power levels for each of the 3 aspects: high, medium, low. That's all I need. If we need ultra-low roles, they're usually temporary in there or they're given a special function. Let's get the state of everything. I want a nice presentation with flowcharts and then you can pass that to Psyche Sonnet to get illustrated as a Claude artifact.
>
> -- psyche, typed (a direct API user turn through the codex-next app-server, not in the stale native Codex rollout), 2026-09-26, to b7da5d; relayed by b7da5d to b860be, later as psyche envelopes.

**Record d68c82 vision/seats.md, entry 4 (#2808)**, date/heading: 2026-10-14 — every Primary has a Secondary, started first

> > whenever we start a primary it needs a secondary. Every primary needs a secondary to act as a secretary. It's like a variant so you start the secondary first actually. The tertiary is so cheap that you might as well start one too so the secretary has its own assistant. I guess you could start the tertiary first. It's programmatic and it's so cheap. There's actually no point not doing it.
> >
> > Every topic, but then we run into the cost of running a harness. Especially with [Claude] and Codex harnesses, they're heavyweight. Maybe secondary and primary is good most of the time, especially in design, unless the topic becomes really big.
>
> -- psyche, STT. Transcription corrected: "Cloud" → "Claude".

**Record da2038 vision/flow.md, entry 8 (#1513)**, date/heading: No Primary is started without a Secondary; queuing is a goal

> Context: comment on choice 3, «A layer a request needs is started whether or not it is running.»; same book.
>
> > I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency.
>
> -- psyche, STT, 2026-10-14.

**Record 39bd0c vision/flow.md, entry 2 (#3720)**, date/heading: No Primary without a Secondary, short term; queuing as a goalpost

> Relayed by Psyche Flow Secondary, 2026-10-16; comment on choice 3, «A layer a request needs is started whether or not it is running.»
>
> > "I would be careful here also to maybe emphasize, or let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, we can say when the system is more reliable in terms of not waking the wrong flow so that we don't have to worry about models like Fable being awakened too much (because the messaging system is smart enough or tuned enough to make sure that the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post to achieve much higher system output quality and efficiency."
>
> -- psyche, STT, book comment.

**Record da2038 vision/flow.md, entry 12 (#1517)**, date/heading: A Fable fallback; lean datom calls; a language of changes; Astra designer mode under 128k

> Context: the living, directly to Psyche Flow Secondary da2038, after the low-usage order.
>
> > And I want research into the best Fable fallback. Probably it's going to be in the open source camp in the sense that we need it. I would like to have something to lean on to use less Fable, whether it's by using it as a front before Fable to make sure that the communication is always relevant.
> >
> > Basically we have this Opus. We need these light calls that have almost no training, no system prompt pre-training (or not pre-training but pre-prompt, like the harness-injected stuff). We really don't need any of the tools and stuff. We just have our own specialized datom-based dialect.
> >
> > The response just comes in as datom, with the variant and then the payload, which is probably a struct. We should have more than one field. There's always something useful, like the meta part of the payload, right? It could even be its own struct so that it's visually sort of like, "Here's the meta." You can even divide it like that so that cognitively you're telling the system how to design, right? You add meta here.
> >
> > In datom it's cheap because it's just an additional pair of braces. There's your inner struct, which is the metadata of your whatever, your simple last response, which is just text. It's like the default. Well it's not the default. I guess even the most basic responses can't even be just a single string payload because it would be a proposal, which would have a path at least. A single proposal is the basic fallback default, right, or multiple proposals and then you have a vector of them. They're each about something, the most basic of which is a path and then a diff, which can basically just take a variant, right, where you just have a plain edition, targeted edition, or whatever.
> >
> > Let's develop a really cool language to talk about changes. Also just for now, basic: between certain paragraphs or in a certain section because Markdown is its own structured data, we can map Markdown into a certain datom-based language of variants. You could even get an output of Flow to sort of draft that into a book and then get an Astra.
> >
> > All you have to do is basically collaborate with [Mind] Secondary and then we use Astra in this designer mode with secondary in its own aspect, maximizing the efficiency of each call. We make sure that the context doesn't grow beyond 128,000 tokens at the time of the call, right? If it's 127 then we can still use it especially if it's on the same topic.
> >
> > If it's not on the same topic, if it's a wildly varying topic, that's why we want lean calls: it's cheap to just start another one because it really doesn't even need tool calls. It can just talk to secondary to ask it what it would like to know. All the tool calls are really just talking to the secondary and the secondary then handles ...
>
> -- psyche, STT, 2026-10-14. Transcription corrected: "mine secondary" → "[Mind] Secondary". The last sentence is unfinished.

### P4.1. Everything the machine puts into a prompt is one datom; the living is told by shape
**Proposed:** Everything the machine puts into a flow's prompt is one datom. A request is its sender, as an address, and its content, headed by its kind: Order, Question, Result, Notice, or Psyche, the living's words with their context. A kind is added by adding a variant. A request carries no flow id, no timestamp and no hash; Flow resolves the sender from the calling process. The living's words are the only text in a transcript that is not datom, so his are told from the machine's by their shape, and a tool finds them in any transcript by that mark.
**Finding:** The sentence "A request carries no flow id, no timestamp and no hash" rests on 263, 603, 3320, 2730, 3839 and 5ec12c entry 2494 (no useless Flow ID fields). The kinds Order, Question, Result, Notice, Psyche: the closed set is in the module as it stood; 3643/1841 describe kinds with waking effects.

**Record 787230 vision/messaging.md, entry 1 (#263)**, date/heading: 2026-10-29 — A message says who sent it, without Flow ID

> Context: the living, in the Psyche core Primary chat 787230, on a report that did not name its sender.
>
> By the way we should know who messaged you without Flow ID. I've said this many times. I don't know why it still isn't happening.

**Record 36ac89 vision/messaging.md, entry 1 (#1565)**, date/heading: Machine messages that look like the living typed them

> 2026-10-25, to Psyche core Secondary 36ac89. Context: the core Primary's ruling had reached me by herdr prompt as a bare chat turn with no sender named.
>
> > You're still getting messages from machines that look like the living typed it. This is the third time I mentioned it. Do I need to go to Anthropic's data center and start smashing motherboards for you to start listening to me?
>
> Clarification, same exchange, after I said it looked so "on your screen":
>
> > No, on anybody's screen it looks like I wrote it. The message is difficult to tell apart, right? Do you understand what I'm saying? Don't tell me on my screen. This has nothing to do with my screen.

**Record d36431 vision/messaging.md, entry 1 (#2050)**, date/heading: 2026-10-25 — Living and machine messages look the same

> Context: after messages the Secondary sent the Psyche core Primary did not arrive there.
>
> > I don't see all the things that we've been discussing. I didn't see them come in as a message in Primary so I'm unable to resume my conversation there.
> >
> > I noticed a really big problem, which is that I'm not even able to differentiate user-living messages, messages coming from the living, and messages coming from machines. There is no more formatting difference between them so I think some of the machines think I'm talking to them now when the machine is talking to them.
> >
> > Run an audit. Make sure none of the machine messages were logged in as Vision or anything, and we need a short-term emergency solution to prevent this problem from spreading.

**Record d36431 vision/messaging.md, entry 4 (#2053)**, date/heading: 2026-10-25 — Machine messages still look like his; advise every running flow, through queues

> Context: after the Secondary had landed the "From …, a machine:" line in compensation-messaging; messages without it still reached him.
>
> > I still see messages that are difficult to differentiate from living messages. I know some are machine messages because they didn't come from. Like I said this is a huge problem and we need to solve it right now. You have to change your belief and also advise all the running flows of this. This is why we want queues so that we don't have to wake everybody up.

**Record bf8ae0 vision/messaging.md, entry 1 (#1164)**, date/heading: 2026-10-27 — Signal out of the Nexus carries proper datom; a new Flow may do it hackily so that messages are structurally told from the living's; then a tool searches transcripts for his messages, the ones not datom-formatted

> Context: the living, direct, after my answer that the rebuilt Flow should be used batch by batch.
>
> > I know I've said that datom that comes out of the Nexus should have a proper [datom way], not datom that comes out. I mean signal that comes out should have proper datom data, like the proper reencoding and datom done some way or another.
> >
> > Maybe we can implement it in a hacky way in a new version of Flow so that messages become structurally identifiable as to whether or not they came from the living. That way we can move to the phase that follows, in which we can create a tool to search transcripts for the living messages (which would be recognized by the fact that they're not structurally datom formatted).
>
> Transcription corrected: "database wave" → "datom way".

**Record 2933ce vision/messaging.md, entry 1 (#1376)**, date/heading: 2026-10-29 — A flow's chat is not read by its Secondary; a message to the Secondary goes through the Flow Nexus

> Context: the living, direct to Psyche core Primary 87f1ee, 2026-10-29T16:35:44Z, after the Primary printed the living's words in its chat as if sending them to its Secondary. Verbatim from /home/li/.claude/projects/-home-li-primary/87f1eeb3-882b-5285-9e49-67ed36434d32.jsonl.
>
> > I don't understand what you're saying. I'm not talking about a message you sent to secondary. I'm talking about you printing what I said in the chat, which is not secondary. What you say in your chat is not read by secondary. You understand these are different mechanisms. If you want a message sent there to secondary, you have to use the Flow Nexus but what you did was print what I said back in your chat.
>
> Leading into it, 16:34:29Z:
>
> > Yeah I guess you're right. I shouldn't say it like that. Why are you repeating what I said? I don't need to know what I said because I said it, obviously, and it's using up your context. Is there a benefit that you see in repeating what I said to yourself? Because I'm not the audience since those are my words, do you understand what I'm saying?

**Record 2933ce vision/messaging.md, entry 2 (#1377)**, date/heading: 2026-10-29 — The living's words are retrievable once every machine message in a pane is datom

> Context: the living, direct to Psyche core Primary 87f1ee, 2026-10-29, correcting the Primary's line on retrieving his words; relayed by that Primary. For messaging, remembering, datom. The correction, as relayed: "Your words are never datom; the machine messages are." The Primary's restatement, which he accepted: your words are retrievable once every message injected into a pane is datom, so that yours are the ones that are not. His words on it:
>
> > Right and that's a really good line to land somewhere.

**Record 2933ce vision/messaging.md, entry 3 (#1378)**, date/heading: 2026-10-29 — Source of the relayed correction: his words are not pulled out of a datom-formatted message

> Context: the living, direct to Psyche core Primary 87f1ee, 2026-10-29T16:48:13Z, after the Primary said his words would be retrieved from datom-formatted messages. Verbatim from /home/li/.claude/projects/-home-li-primary/87f1eeb3-882b-5285-9e49-67ed36434d32.jsonl, entry 643; relayed by Psyche core Primary f6637e.
>
> > No, no, no, not pulling my words out of a datom-formatted message. Oh I see what you mean. Out of a datom format that you didn't... I don't think you said that right. That could be confusing. If we're not careful how we say things, we can confuse ourselves and so you have to be careful how you say that because that's not quite what I meant. Do you know what I mean?

**Record e3c8c1 vision/messaging.md, entry 1 (#603)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary e3c8c1

> Context: on the messages between flows today.
> "You do have to communicate, though, not a bunch of fucking garbage. Just tell each other what you intend to do and what you have actually done without jamming each message with a bunch of timestamps, hashes, revisions, and all of this. ... There are way too many little useless details that you're telling each other. Just communicate but don't try and count each other's eyebrow hairs."
>
> -- psyche, STT.

**Record 5578cc vision/messaging.md, entry 1 (#3320)**, date/heading: No hashes, timestamps or other garbage in what seats send each other

> Context: relayed by Psyche Sonnet 6e782c; typed to it after it relayed his book comments to Fable edf227 with the book's long link, times and section labels in every context line.
>
> > You really fucked up. You sent them giant hashes.
>
> > And a bunch of timestamps and all a bunch of fucking useless garbage
>
> -- psyche, typed, 2026-10-03, to Psyche Sonnet 6e782c.

**Record d68c82 vision/messaging.md, entry 2 (#2730)**, date/heading: Book comments reach the flow; senders named by aspect, topic and layer

> "Oh here's another thing: when I comment in the books, do you get those injected in your user prompt? If you don't then there is another failure we need to fix. Because then my words are not reaching the middle stratum, if that's the case, which is horrible. That might be the reason why we were having such terrible results. Also I noticed I haven't been seeing the `#psyche` message type and I've asked for the flow ID of the sender to be replaced by the actual aspect (like how we name metaflows: aspect, topic, and then layer). That's how I want flows to stop referring to each other by flow IDs and I need everything that I say. There's the `#psyche`. We invented the `#psyche` type. You know how to message starts with `#msg`. There used to be a `#psyche`."
> -- psyche, STT, 2026-10-12.

**Record e51411 notion/message.md, entry 1 (#3839)**, date/heading: The sender's role comes from where the call came from

> > I think there's a notion here. ... You don't see the Flow ID of the sender. It's too bad that we have to ask the agent to give us the role because we should be able to determine that based on where the call came from. It should be Psyche Fable or Psyche Opus in the Pasco [sic] case. We're showing that it's sort of emulating, or maybe the hashtag here works. I don't know. Maybe it's a variant. We have a set: Psyche ask [sic], Psyche Fable. Potentially we have any kind of combination of model with role or there are two variants: Psyche, mind, or field. This is one enum there. This is one hashtag: Psyche, mind, or field. The model: Fable, Astra, Opus. Right?
>
> -- psyche, STT, 2026-09-25, to e51411, on the #msg ["00f95a" "..."] shape. "Pasco" and "ask" kept [sic]: meaning unclear.
>
> Correction: "in the Pasco [sic] case" was "in the [PascalCase] case", meaning PsycheFable or PsycheOpus written as one word. -- psyche, STT, 2026-09-25, to e51411. Transcription corrected: "Pasco case" → "PascalCase case".
>
> > No I changed my mind. You got me right but I was saying you got me wrong on what I meant by the speech-to-text typo there. This is irrelevant. I changed my mind, as you know. You got me right.
>
> -- psyche, STT, 2026-09-25, to e51411: the PascalCase reading is dropped; the two enums, aspect and model, from the database, stand.

**Record b7ba00 vision/messaging.md, entry 7 (#229)**, date/heading: The head is the message's kind, a new type carrying all its data; priority leaves the letter; soft and hard was the wrong approach

> Context: the living's comment on the "Two Books Compared" artifact, at "Priority is a head on the datom." Retrieved by a reading subflow of 93ba9f; relayed by direct Herdr prompt after the Noema book was published (21:04). The trailing "..." is as returned.
>
> > Actually the head is where we put not only priority. Maybe sometimes the priority is implied but this is where the message type is. We can make any number of kinds. If we want a certain different kind of message, then we can create it there. It's a new type and it carries all the data.
> >
> > We can have the spec easily in the skill that Ethos shows what kind of objects should be expected in each place so that these can be understood when they come in. You could have, let's say:
> > - a psyche update
> > - a hard psyche update, which interrupts
> > - a soft psyche update
> > - a psyche update, where maybe there's a middle ground of interrupt
> > - an implementation report
> > - an audit report, even the software or the hard version
> >
> > Arguably the audit report is all going to be the same: the soft or the hard. Do we really even need to tell it if it's soft or hard? Do we even need to tell the model if it's a soft or hard message? I don't know. I don't think so. The database can know it, so if he wants to know he can find out but I don't think it's going to matter. We'll make the judgment of what kind of messages we want to break harder than others so it's just what kind of message it is, really.
> >
> > We don't even do the soft or hard, actually. That was the wrong approach. For the normal format that gets communicated, the non-debugging format, basically the production requests and responses (are those what we call them? Queries and responses) ...
>
> -- psyche, typed (artifact comment), 2026-09-26, relayed by 93ba9f.

### P4.2. Recipient, Up, three deliveries
**Proposed:** A request names its recipient by address, or Up, the layer above in the sender's aspect and topic, and asks one of three deliveries. Queue leaves it for the next delivery. Wake delivers it, waking a sleeping metaflow. Abrupt interrupts the recipient's turn and is answered Sent or Failed, never Queued.

**Record 39373e vision/messaging.md, entry 1 (#2015)**, date/heading: An abrupt message is sent or failed

> "I want you guys to start using abrupt messages and abrupt messages should never return queued ever. It should be failed or sent."
>
> -- psyche, 2026-10-22, direct.

**Record 5ec12c vision/messaging.md, entry 1 (#2502)**, date/heading: 2026-10-22, living, directly to Psyche core Secondary 39373e, relayed; two messages

> "I want you guys to start using abrupt messages and abrupt messages should never return queued ever. It should be failed or sent."
>
> "And ideally maybe not short term but longer term, if the Flow isn't up to receive the message, then Flow just starts, delivers the message, and then replies to the CLI that the message was sent. The CLI will wait, like I said, long term or longer term if it's possible now and that's okay. The sender of the message (the call) will block until the missing Flow, if it's missing, is started. Then it'll start with its usual start prompt and the message below it, all sent together at the beginning."
>
> -- psyche, relayed, input mode unqualified.
- **b7ba00 vision/messaging.md, entry 7 (#229)** - The head is the message's kind, a new type carrying all its data; priority leaves the letter; soft a - full text under P4.1.

**Record bf8ae0 vision/messaging.md, entry 3 (#1166)**, date/heading: 2026-10-27 — When Flow holds, fall back to direct Herdr messaging; the belief carries the fallback with its instructions

> Context: the living, direct, on my report that Flow held every delivery to the Secondary for five hours.
>
> > You can always fall back to direct [Herdr] messaging, so [do], and that should be part of the belief. Also, is this fallback mechanism with some instructions on how to use it, how to find the flow you want to message, how to message him directly, how to indicate who the sender is, and so on?
>
> Transcription corrected: "herder" → "Herdr"; "so don't" → "so [do]".

### P4.3. Queue per metaflow, delivered whole, started if absent
**Proposed:** Every request is queued for its metaflow, never for a flow, and the queue is delivered whole, oldest first, as one datom, a vector of requests, in one turn: to an idle flow at once, to a working flow as its turn ends, to a sleeping metaflow in the first prompt of the flow woken for it. A metaflow a request needs is started whether or not it is running; the sender's call waits, and the start prompt and the request arrive together. A metaflow being refreshed receives nothing more; its queue waits for the successor.
- **d36431 vision/messaging.md, entry 5 (#2054)** - 2026-10-25 — Queues belong to metaflows, not flows - full text under P1.4.

**Record 9aaaba vision/flow.md, entry 2 (#352)**, date/heading: 2026-10-28 — Not scrapped: the queue flushes as one message, the trigger included

> Context: the living, direct, minutes after saying to scrap the queue, watching the Secondary take one call per held message.
>
> > This is not hard to fucking implement so I don't know why we need to scrap it.
>
> > If you have a queue and something, there should be more than one reason why the queue goes out. If, let's say for whatever reason, something comes in that should flush the queue, then all of the messages come into the pane as "one message". All of them, everything, including the one that comes in that gets the queue unstuck, come in as "one message". We don't send a message and then another message and then another message and then another.
>
> > He's acting on incomplete information because every time he gets one more message, that means that what he acted on previously was missing that information. We get horrible results: high cost, slow behavior.

**Record e591ed vision/messaging.md, entry 1 (#1959)**, date/heading: The queue delivers everything at once, and delivers while the flow is idle

> 2026-10-28. Context: the Psyche core Secondary e591ed had sat idle with its queue held; it was then fed old queued messages one per turn, answering each before the next arrived.
>
> > Looks like your queue just got unblocked and it also tells me that the queue system is flawed because you weren't working when I sent you my message. And also the queue is flawed because all the messages should come in, not one message and then one answer, and then one message and then one answer. Pass all of this. This is important programming stuff. Pass this to your primary.

**Record e591ed vision/messaging.md, entry 4 (#1962)**, date/heading: One message per answer keeps him from reading

> 2026-10-28. Context: the Psyche core Secondary was receiving one queued message per turn, so its answers to him scrolled away.
>
> > Also this behavior of you continuing to get another message every time you respond means that I'm unable to read your answers so don't bother talking to me right now. Just pass all the stuff that's important that came from me to Fable, to Primary, if you're able to tell the difference. Otherwise get him to audit your transcript to see which messages are likely to have come from me.
- **5ec12c vision/messaging.md, entry 1 (#2502)** - 2026-10-22, living, directly to Psyche core Secondary 39373e, relayed; two messages - full text under P4.2.

**Record 87c40b vision/flow.md, entry 2 (#9)**, date/heading: A missing flow is instantly started to receive the message

> Context: relayed by Psyche core Secondary b7a16a, 2026-10-22, after Mind flow Secondary stopped for want of its undeclared Primary.
>
> > "Any missing flow is instantly started to receive the message and nothing ever goes wrong in any way, shape, or form"
>
> > "I don't want you to stop for one second."
>
> -- psyche, STT, relayed by b7a16a.

**Record da2038 vision/flow.md, entry 3 (#1508)**, date/heading: A needed flow is started, running or not

> Context: same book, proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», 2026-10-14T15:18; relayed by Psyche Core Secondary.
>
> > We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.
>
> -- psyche, STT, 2026-10-14.

**Record df159a vision/flow.md, entry 1 (#3490)**, date/heading: A needed flow is started whether or not it is running; with no transcript, it is fed its context modules and its prompt

> Context: his comment on book «Flow: CLI, deployment, long term» (https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA), proposal «an undelivered request tries a higher power, then lower; a crucial metaflow missing is started», anchored at «A request that cannot be delivered tries a higher power in its own aspect: the layer above, and when nothing is higher, …». 2026-10-14T15:18, thread 858cdedf-7fcd-48f6-a7c3-3616049132d6. Relayed by Psyche Flow Secondary da2038.
>
> > We have old vision that is now obsolete in there, with a conflicting vision. The long-term vision is that the flow is started if it's needed, which means it doesn't matter if it's running or not. Even if it doesn't have any working transcript to reawaken, then we just feed it the context modules that this meta flow is supposed to have, along with the prompt that it's supposed to be getting now.
>
> -- psyche, STT, book comment.

**Record e591ed vision/messaging.md, entry 3 (#1961)**, date/heading: A messaging watcher, and an emergency Flow fix

> 2026-10-28. Context: following his words on the held queue being a critical flaw.
>
> > It also means that the messaging right now cannot be trusted. We almost need a messaging watcher that can watch for flows that are stuck and get them unstuck somehow for now. We need an urgent emergency fix and redeployment of a new flow that doesn't have this flaw.
- **d36431 vision/messaging.md, entry 4 (#2053)** - 2026-10-25 — Machine messages still look like his; advise every running flow, through queues - full text under P4.1.

### P4.4. Waking kinds; Primary reached through Secondary
**Proposed:** An Order, a Question and Psyche wake a sleeping metaflow; a Result and a Notice wait for the next waking, so a flow satisfied with its topic is not woken to be told. A Primary is reached through its Secondary as practice; Flow refuses no route, since a flow without a Secondary must stay reachable.
- **d4ae97 vision/messenger.md, entry 2 (#1841)** - Every topic has its own flow; messages queue, and only a waking message wakes it - full text under P1.5.

**Record f5a6e9 vision/messaging.md, entry 1 (#3643)**, date/heading: Every topic has its own flow; messages queue; each kind has a waking effect by the flow's state; a waking message drains the queue oldest first, delivered at the end of the prompt as a vector typed by variant

> Context: said on 2026-10-08 while reading «Spirit edit incident»; relayed by Psyche Opus d4ae97, elision marked by it.
>
> > I realized that every topic has its own flow. A topic could involve more than one skill but essentially that flow would be in charge of that whole topic. How do we efficiently queue any kind of update? If we're satisfied with the state of a certain topic at a given point, that flow should not be woken up. Let's suppose that another flow wants to tell that flow, "Congratulations, job well done," or that there's a notification for that flow because one of its branches was merged in the production branch. Things like that should not wake up the flow until there is a situation that arises, probably related to the living or the psyche (which is its representative in the machine), that wants to have to deal with this particular topic in any way (to find something out about the system because it's not behaving according to documentation, or because we want to investigate doing a new feature, etc.). That message actually has, given the particular state of that flow, the effect of changing the result. Different messages will have different flow-waking effects. When the message that does have the waking effect at that particular state in that flow comes in, it will also trigger checking the queue for that flow, so that the whole queue is checked in order, from the first received to the last. The message that just got in and triggered the queue will come in at the end of the prompt and it'll be a vector of all these objects, which are typed by variant name, obviously. We're designing Ethos here ...
>
> -- psyche, STT, relayed by d4ae97.

**Record b49eaf vision/messaging.md, entry 1 (#152)**, date/heading: 2026-10-28 — Flow enforces no Secondary-only route to a Primary (verbatim)

> Context: the living, direct to Psyche core Primary 7459f3 at 2026-10-28T17:31:53Z, answering its Send that ordered Flow to admit a Send to a Primary only from that Primary's own Secondary. Verbatim from /home/li/.claude/projects/-home-li-primary/7459f3b0-e9f1-5a6d-877f-ffd4054a55e7.jsonl (line 821, 0-indexed); supersedes the paraphrase in flows/5bbab2/vision/messaging.md as its source.
>
> > No I don't know if I want. I don't think our system is ready to enforce that kind of stuff programmatically. That's a dangerous road. We would have to have long-running stability through multiple versions before we would consider doing stuff that could very well end up crippling us. What if you don't have a secondary? How is anybody going to fucking talk to you then?

**Record ce46fb vision/flow.md, entry 5 (#115)**, date/heading: A Psyche flow Primary's task is the Flow design presentation; a flow whose context is not about its design restarts with every new raw vision

> Context: asked of me after I had spent the night on publication routing, sanity, retirements and pulse repairs, with no Flow design presentation made.
>
> "So did you make a Flow design presentation lately? If not when did you do your last presentation? If not why did you fail to fulfill your primary task, which is to design Flow, as your topic suggests? Also were you trained to know the new directive, which is that you only message everyone to and from through your secondary? Anyway now you know. If you haven't made a presentation, maybe your context is 95% about flow design. If not then you should restart yourself after making sure that you'll be given every single new raw vision. Of course it's all crystalized vision and intent on flow design. So that you could create the latest version of the presentation on its design"
>
> -- psyche, STT.

**Record 5ec12c vision/flow.md, entry 2 (#2494)**, date/heading: 2026-10-22, living, standing order, to Psyche core Secondary b7a16a, relayed; originals in flows/b7a16a/vision/{flow,messaging,nexus,ethos,context-deployment}.md

> "I want you and everybody to not stop working until:
> - Starting a flow is as easy as kicking a rock with my foot.
> - It's instant and there's no problem ever.
> - It uses the latest context every time.
> - No one can use it the wrong way.
> - It never behaves in a weird way.
> - Every message is delivered consistently and reliably.
> - Any missing flow is instantly started to receive the message and nothing ever goes wrong in any way, shape, or form.
> - Every single thing we might need to debug or change or reconfigure is available through an operation, either on the ordinary [socket] or the meta signal socket.
> - Every single signal, meta signal, memory, and operation ethos definition for every single nexus involved is fully specified.
> - Every single function is under an ethos-defined trait that is actually a sensible trait and a sensible anatomy of the system that doesn't have a single trait for every single function.
> - Everything is smooth and purring.
> - Context modules deploy faster than I can blink and flick my fingers.
> - There are no extraneous useless fields or information going into the received messages, like useless Flow ID fields and all such noise-making useless information or wrappers.
> - You can use short equivalent operations. They are also, by the way, every time defined in Ethos.
> - All the types are defined in Ethos.
> - All the traits are defined in Ethos in every single component.
> I don't want you to ever stop. The world comes to an end and you keep going on these goals. I don't want you to stop for one second. You and Codex are going to sweat your ass off until this is done. I'm tired, I'm tired, I'm tired, and I want to see results. I don't want to see you slacking off or sleeping. You're working until this is working."
>
> -- psyche, relayed, input mode unqualified.

**Record 33752b vision/messaging.md, entry 1 (#3118)**, date/heading: A Primary is not addressed like a low-level grunt

> Context: typed to the Psyche core Primary after seeing the Secondary's turn-grant message («Turn granted once it is out. If the lock is held, wait for its release. Use explicit paths. Send me the link in one line.»).
>
> > Why are you being bothered by all these messages? You shouldn't. If you receive a message and you do nothing, this looks silly: "like, if turn granted, once is out, if the lock is held, wait for its release. Use explicit pass." It sounds like you're being treated like a low-level grunt. What the fuck is going on?
>
> -- psyche, STT, 2026-10-12. Transcription corrected: "explicit pass" → "explicit paths".

### P4.5. Flow the one writer; Message and the fallback
**Proposed:** Flow is the one writer into a pane. Message, the Nexus of messaging, sends through Flow and subscribes to Flow's delivery events; until Message stands, and whenever it breaks, a flow sends through Flow directly. When Flow holds a delivery, a flow falls back to typing into the recipient's pane through Herdr, its text opening with the sender's address.
- **875960 vision/archive-flow.md, entry 4 (#1769)** - 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribe - full text under P1.1.

**Record ecbc42 vision/flow.md, entry 1 (#874)**, date/heading: Flow sends now; the Message component sends in the long term

> Context: book comment on «The Nexus: questions for the living» (https://claude.ai/artifact/32uPikafAbLVMWfxaBinAW), relayed by Psyche core Tertiary, Proposal 2 (Flow is the send path until Message is redesigned), 18:16.
>
> "Well an order and a question would be a message so this proposal contradicts what you were saying earlier. You could word it so that in the short term we can use Flow's raw calls to send messages but eventually orders and questions (which are messages) would go through the message nexus, which would then use the Flow API to actually send the message."
>
> "Again like I said, we should specify that in the short term yes, we could use Flow directly to send messages but in the long term it should do it with the message component."
>
> -- psyche, STT, book comment.

**Record da2038 vision/flow.md, entry 1 (#1506)**, date/heading: Flow exposes the harness; Message makes use of it; Flow first

> Context: comment on «Flow: CLI, deployment, long term» (https://claude.ai/artifact/KqGmvFzr4VAqEeCA4jYMmA), proposal «Flow exposes the harness; Message makes use of it; Flow first», 2026-10-14T15:15; relayed by Psyche Core Secondary.
>
> > Yes this is good.
>
> -- psyche, STT, 2026-10-14.
- **af762b vision/operational-flowOwnsHerdr.md, entry 1 (#3025)** - Basically, Flow is in charge of herder. I shouldn't interact with it directly. Message can get the d - full text under P1.1.

**Record 752e0f vision/herdrSessions.md, entry 1 (#14)**, date/heading: A single Herdr session controlled by Flow; Flow as the messaging tool

> > Can you help get the new flows? See what's happening. There are only a few flows going now in the herder that you're in, and there are multiple herders, and there's a big mess. I just want a single herder session that's controlled by Flow, the Nexus. I want Flow to be our tool to send messages and stuff until it actually uses the Flow API through its socket to actually send messages more sanely.
>
> -- psyche, typed, 2026-09-24, directly to Psyche High 752e0f. "herder" is the living's spelling of Herdr.

**Record bf8ae0 vision/messaging.md, entry 2 (#1165)**, date/heading: 2026-10-27 — A message nexus that uses Flow's sending capability, with Flow itself as the fallback when the message nexus breaks

> Context: the living, direct, same message, after ordering the Flow design with code.
>
> > You could also design a message nexus that would allow us to have them use the flows' capability for sending messages from the message nexus, which would use it. It would also allow us, first of all, to have a fallback on Flow itself for sending messages if our message nexus breaks (so that we could work on developing more advanced messaging types and capabilities without breaking Flow).
- **bf8ae0 vision/messaging.md, entry 3 (#1166)** - 2026-10-27 — When Flow holds, fall back to direct Herdr messaging; the belief carries the fallback w - full text under P4.2.
- **bf8ae0 vision/messaging.md, entry 1 (#1164)** - 2026-10-27 — Signal out of the Nexus carries proper datom; a new Flow may do it hackily so that mess - full text under P4.1.
- **f5a6e9 vision/flow.md, entry 4 (#3638)** - What is sent to flows are typed requests, not letters; Flow holds no messages; Message asks Flow for - full text under P1.1.

### P5.1. Sleep; Maintained and OnDemand
**Proposed:** A metaflow sleeps when its flow's harness closes: its transcript, address, declaration and queue stay, and no harness runs for it. A Maintained metaflow, core among them, is kept awake and refreshed at an age, so the living always has a flow to talk to; an OnDemand metaflow sleeps as soon as its turn ends with nothing queued.
- **da2038 vision/flow.md, entry 13 (#1518)** - The new Flow Nexus keeps no harness running for a session that is not running - full text under P1.5.
- **da2038 vision/flow.md, entry 26 (#1531)** - Only core keeps an always-open session; core sessions are kept fresh and restarted at an age; the ot - full text under P1.5.
- **fd30d2 vision/flow.md, entry 2 (#2401)** - The living is never left without a Primary - full text under P1.5.
- **fd30d2 vision/flow.md, entry 3 (#2402)** - There is always a Primary core - full text under P1.5.
- **28f6f9 vision/flow.md, entry 1 (#3106)** - Interpretation accepted: ordinary empty-queue refresh may sleep - full text under P3.1.
- **da2038 vision/flow.md, entry 26 (#1531)** - Only core keeps an always-open session; core sessions are kept fresh and restarted at an age; the ot - full text under P1.5.

### P5.2. Woken: fresh flow, young transcript resumed
**Proposed:** A metaflow woken for a request starts a fresh flow from its declaration. Its last flow is resumed only when the request is the literal continuation of that work and the transcript is young, under the model's young threshold; the judgment is a small model's.

**Record da2038 vision/flow.md, entry 28 (#1533)**, date/heading: A waking flow first looks for a past flow and its context size; a fresh flow is almost always better unless it is the same topic's continuation; a system one call asks whether the past is noise for the new message

> Context: comment on «Flow: sleeping and waking seats», figure under «A message wakes a sleeping seat», 2026-10-16 01:45; found unrelayed 2026-10-17.
>
> > This chart is good, although it should say that if it has a transcript, the first thing it should do is look to see if it has a past flow. If it has a past flow, it should look to see if the context is too large. I could even see a flow coming in as a system one decision if it's borderline and it might have context that's good.
> >
> > Actually, to be honest, old flows should not be prioritized because they've probably gone to sleep, right? If they're not very old, we should do research on what the caches are with different providers and how long, usually, the stuff can be cached. It's not that long, so it's almost always going to be better to start a fresh flow, even if it has a past session, unless it's literally the continuation of that topic. It was just put to sleep because it wasn't addressed for a bit, whereby reusing that whole transcript actually makes sense because nothing in there is noise.
> >
> > This is where I see the system one call coming in to ask, "Is any of this noise in relation to the new message coming in?" This is why we need smart message composition. It's not just the straight-up living input. The living input has to be broken up and expanded, with each part having its own context and being sent to the right parts. If you're going to have machine intelligence, you're going to have to decompose, not machine thinking. If you're having machine thinking, you're going to have to decompose thoughts into parts, which is what Sema is. It decomposes language into parts.
>
> -- psyche, typed, book comment.

**Record da2038 vision/flow.md, entry 9 (#1514)**, date/heading: A still-young working transcript is reawakened; what young means

> Context: comment on choice 4, «with a working transcript, its flow is reawakened from it»; same book.
>
> > I would say, with a still-young working transcript, let's have a proposal to explain what a young context is in terms of ratio and where average context size starts to degrade rapidly (around the 100,000-token point).
>
> -- psyche, STT, 2026-10-14.
- **da2038 vision/flow.md, entry 3 (#1508)** - A needed flow is started, running or not - full text under P4.3.
- **df159a vision/flow.md, entry 1 (#3490)** - A needed flow is started whether or not it is running; with no transcript, it is fed its context mod - full text under P4.3.
- **d68c82 vision/flow.md, entry 10 (#2683)** - 2026-10-14 — A metaflow's default task - full text under P3.3.

### P5.3. Measure, refresh at threshold, from outside, no summary
**Proposed:** Flow measures a flow's context at every turn's end. Past its model's refresh threshold the flow is refreshed as it goes idle: Flow holds the metaflow's queue, starts the successor from the declaration with the remembering the declaration names, closes the predecessor's pane and its native thread in the same event, and delivers the queue to the successor. The successor receives its belief modules and the raw records named, and no summary or handover from the predecessor, whose biases end with it. A flow is refreshed from outside without being woken, or refreshes itself through Flow; below the young threshold a flow is refreshed only on a dramatic change of direction.
- **74e4d1 vision/refresh.md, entry 1 (#2986)** - 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a  - full text under P3.1.

**Record 74e4d1 vision/refresh.md, entry 2 (#2987)**, date/heading: 2026-10-26 — Approved: the no-handover line; refresh the Primary; every flow understands Ethos, Datom, protos

> Context: the living, direct, to Psyche core Primary 74e4d1, approving the proposed vision:remembering line.
>
> > Good. Land it and then implement it by refreshing your own flow or having it refresh, whatever works best. Don't forget, right? I need every flow to understand ethos and datom or protos in general.
- **a68420 vision/flow.md, entry 6 (#2287)** - 2026-10-23, living, direct, to Psyche core Primary a68420 - full text under P3.1.

**Record d36431 vision/flow.md, entry 1 (#2037)**, date/heading: 2026-10-25 — Restarting a flow without waking it

> Context: said after the Secondary sent the Psyche core Primary (493e29) messages that woke it, and the Primary had replied, when the restart of the Primary seat was ordered.
>
> > You guys are tripping on your own shoelaces and going against my vision. The whole point of me telling you to restart primary seat is so we wouldn't pay for an uncached run of its old context, which you now did. Now it's been woken so it's too late. Now it's cached so it's not as bad if we keep talking to it. Whoever implemented the way flows restarted made a mistake because I explicitly many times said that we need to be able to restart flows without waking them. Somebody made a huge mistake.

**Record d36431 vision/flow.md, entry 2 (#2038)**, date/heading: 2026-10-25 — The option to restart a flow without waking it

> Context: correcting the Secondary, which had rendered his previous words as "a restart must not wake the flow".
>
> > Now you're twisting my words. I didn't say that a restart must not wake the flow. My point is I want to be able to restart a flow without waking it. Of course a flow can restart itself. That's not a problem but I also want the possibility. I want the option.

**Record d36431 vision/flow.md, entry 3 (#2039)**, date/heading: 2026-10-25 — The woken seat stays; the option is for next time

> Context: after Psyche flow Secondary planned a no-wake stop of the already-woken Primary seat and the core Secondary relayed it to him.
>
> > Well like I said, you already woke it up so it's okay now. It's woken. I don't know why you're trying to do this. You cannot start it without waking it now because you already woke it up so you can't roll back time. I don't even know why you're trying to do something which is impossible or talk about it even. Obviously we're going to fix it so that next time it'll be possible.

**Record d36431 vision/flow.md, entry 4 (#2040)**, date/heading: 2026-10-25 — Refresh from outside; the restriction as a case study

> Context: after the Secondary reported that Flow 0.39 offers no outside restart without the seat's own turn.
>
> > Oh and make sure Mind is working on fixing Flow so that flows can be refreshed from outside themselves. In other words they don't need to be woken up to be refreshed. I don't even know how this restriction was actually implemented. It sounds weird to me, far-fetched, complicated, brittle, and likely to cause problems so it's a really bad architectural decision.
> >
> > I think we should use it as a prototype-level bad design decision or misinterpretation. It kind of blends into the anatomy work so Fable could create a small presentation maybe after researching this case study, the pattern, and what others have discovered about similar patterns and things like that (to try and work out how we could reduce the likelihood of it happening again).

**Record d68c82 vision/flow.md, entry 3 (#2676)**, date/heading: The refresh procedure starts at a threshold

> > Well, Fable should never, rarely, if ever, be allowed to get to 400,000 tokens, so there was a failure there. We need a hook that sends a warning to Field to either recompact or restart a flow when it reaches a certain threshold.
> >
> > For Claude, you would get a preemptive warning at 200,000 tokens, at which point we're basically not forcefully trying to refresh but are actively taking measures to, first of all, warn the flow that we've started a refresh procedure. It should create its handover and potentially even say that some of its context should be split and sent to current topics or to new topic flows if it's trying to touch too many topics.
> >
> > Let's zero in on what all this is specifically when we describe it for actual guidance and crystallization books.
>
> Context: Fable reached 408k tokens while writing a book; ~91% of it was noise for that book.
> -- psyche, STT, 2026-10-13.

**Record d4ae97 vision/flow.md, entry 8 (#1822)**, date/heading: The refresh threshold is 20% to 40%

> Context: comment on the threshold bar in the figure, section 4 «The refresh is software».
>
> > That's a nitpick but visually that threshold doesn't really represent what I want. It's more like 20% to 40%. That looks more like 70%.
>
> -- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

**Record b80e55 vision/refreshThresholdAndCacheSnapshot.md, entry 1 (#3449)**, date/heading: A Claude flow refreshes around 200–300K tokens — 100K bootstrap, 100–200K useful work, then refresh. Snapshot the preloaded vision and branch 2–3 ideas from the same cache

> Context: spoken directly by the living to Psyche Medium b80e55 on 2026-09-20.
> The living defines the refresh threshold and introduces cache snapshots: the
> startup prompt is cached once, then multiple sessions fork from it with
> different ideas.
>
> > You can restart a flow, especially if it's above 30%, like 200,000 to 300,000 tokens, which is different for Claude, right? 200K to 300K is like a refresh because when you start a model, you start around 100,000 tokens, then you give it 100,000 to 200,000 tokens to be useful on that idea, and then it's sort of like you just need to refresh it.
> >
> > We can start photographing. Oh man, that would be cool to snapshot the preloaded vision, and then you can have 2 or 3 different ideas, but you use the same cache for the startup prompt.
>
> -- psyche, direct to Psyche Medium b80e55. Input mode not established.

**Record f55ec8 vision/flowRefresh.md, entry 1 (#1783)**, date/heading: A Fable main flow refreshes at thirty percent of its context, three hundred thousand tokens; the restart and refresh made easy: the main flow's context used wisely so the refresh is easy to output; the refresh a simple command, a subflow putting it together with the system prompt in place; the vision upgraded in it, the system prompt made more accurate to the current vision

> Context: typed to the primary Claude f55ec8 on 2026-09-16 evening ("So you're due for a refresh now, right?"); "you should restart again" is the working instruction, recorded in log.md. Logged by the main flow before acting.
>
> > You should make it a good practice to start when you're getting to 30% of your context as a Fable agent, right? That's 300,000 tokens. That's a lot, so it's better to restart with a clean.
> >
> > Let's make the restart and the refresh easy. Let's get more and more into getting the main flow context used wisely and effectively, so the refresh is easy to output. The refresh has to just be a simple command, and then the subflow will put together the refresh and have the system prompt in place. We need to agree on upgrading vision in there, like making the assistant prompt more accurate with the current vision.
>
> -- psyche, typed.
- **bf8ae0 vision/archive-remembering.md, entry 1 (#1175)** - 2026-10-27 — Compaction weighs every message of his alike; what is wanted is to weigh his content an - full text under P3.1.
- **bf8ae0 vision/archive-remembering.md, entry 1 (#1175)** - 2026-10-27 — Compaction weighs every message of his alike; what is wanted is to weigh his content an - full text under P3.1.

### P5.4. Thresholds configurable; compaction an emergency
**Proposed:** Each model's thresholds, young, refresh and ceiling, are configuration. A refresh comes before the harness's compaction; a compaction is an emergency, ordered through the meta socket and refused under the threshold, and a flow that compacted is investigated for working too long.
**Finding:** "Thresholds young, refresh, ceiling as configuration" is design; numbers appear in the records only as the living's examples (100,000 point of degradation 1514; 200,000 Claude, 96,000 Codex warning 2681; 300,000/250,000 for an ephemeral flow 2924). The book's datom example 100000/200000/300000 is illustrative.

**Record 33752b vision/flow.md, entry 1 (#3112)**, date/heading: A guarded compaction request on the short-term Flow solution

> Context: an order to this seat, relayed by the core Secondary, for a proposal book. The last sentence breaks off.
>
> > I want you to make sure that we have a system in place on the short-term flow solution that lets us easily ask for a certain flow to be compacted or certain meta flows. It would refuse if the context is below a certain threshold. That way we could guard against the compacting request being routed to a brand-new flow, which we didn't know was being started, or if the flow is not a certain age, even in time terms. Let's get a proposal put together on that: the fable topic, the psyche fable topics. Let's make sure that they're not large and that we get them to ...
>
> -- psyche, STT, 2026-10-13.

**Record 33752b vision/flow.md, entry 2 (#3113)**, date/heading: He still compacts, but prefers a refresh

> Context: spoken after compacting this seat himself.
>
> > I just compacted you before this message because your context was getting large as well but I don't like compacted flows because they still have a lot of noise. ... I still use compaction right now because we just really can't afford to run these huge massive context windows, which just end up being full of noise and resulting in very poor output.
>
> -- psyche, STT, 2026-10-13.

**Record 33752b vision/flow.md, entry 3 (#3114)**, date/heading: Compaction is an emergency measure only; the flow tool also does the messaging and queues for a flow in transition

> Context: comment on «Flow: short term and long term», second edition, Proposal 1, at "Field compacts it, or restarts it".
>
> > No compaction. Compaction is an absolute emergency measure so we're not talking about compaction in any terms other than absolute emergency. It's only going to happen until the tools start behaving properly, in which case starting a new flow is easy and reliable, which hasn't been the case so far. Let's keep compaction mostly out of the discussion and mention it only in an emergency setting.
> >
> > Also we should say that maybe we should make that flow tool also do the messaging since it can mark a flow as being in transition. Therefore it can start queuing messages instead of delivering them when the flow has reached its context limit and therefore should not receive more messages. That would just send it into a spin: potentially it could never actually refresh because it keeps getting new messages.
>
> -- psyche, STT, 2026-10-13.

**Record bf8ae0 vision/flow.md, entry 6 (#1156)**, date/heading: 2026-10-27 — The Flow Nexus, so named, has an operation on the meta socket to order a flow's compaction: a fail-safe among the operations to rely on; a flow with a long context self-compacts when all else fails

> Context: the living, direct, seeing my context long and refresh refused.
>
> > You're supposed to refresh your flow, right? Your context is really long. I guess if everything else is failing, you can always self-compact.
> >
> > I think we should have an operation in the Flow Nexus, and I think we should use that term, the Flow Nexus, to know that we're not talking about a flow. We should have an operation to order the compaction on the meta socket for a certain flow. It could be used as a fail-safe, and that's what I meant. We should have all these operations we can rely on in case.

**Record d68c82 vision/flow.md, entry 8 (#2681)**, date/heading: 2026-10-14 — refresh thresholds, idle harnesses, and handover at cache expiry

> > at 128,000 tokens with Claude we get a warning. ... For Codex models the context window is much smaller and I think that at 96,000 tokens there's a warning and we start to contemplate refreshing. If the flow is working obviously we let it work and if it keeps working we let it work even past compaction.
> >
> > If it works so much that it compacts, eventually in the long-term vision we would have some kind of a check to make a judgment as to whether maybe the topic was misguided.
> >
> > For sure at 150,000, 160,000 tokens on OpenAI's models, we're seriously looking at refreshing, and the same for Claude at 200,000.
> >
> > It would be cool if we could strip down some of these Clojure flows so that they're way more efficient to spawn.
>
> > in the long-term vision, if a flow has just been sitting idle for some time, we can turn off its harness. When the system is properly configured, if a request needs to reach a certain flow (which is not up and running in a harness), then the flow would just restart that flow or start a fresh one.
> >
> > Claude could just tell us the cache is going to expire instead of compacting. Then we would ask for the model to do a handover to produce a handover and that way we could train how we want our handover to be, which is essentially our own form of compaction.
>
> -- psyche, STT, book comments on «Situation, 14 October».
- **d68c82 vision/flow.md, entry 3 (#2676)** - The refresh procedure starts at a threshold - full text under P5.3.

### P5.5. Closed flows; ephemeral flow
**Proposed:** An abandoned, duplicated or superseded flow is closed, its pane and native thread with it, archived and deregistered. An ephemeral flow is a job flow that is not woken again: past its model's ceiling it is given no new job and another takes its place.
**Finding:** The ephemeral-flow sentence carries the living's 2924 words without the figures 300,000/250,000, which the Comment removes.

**Record d68c82 vision/archive-flow.md, entry 24 (#2924)**, date/heading: The ephemeral flow: a continuous job flow with a context ceiling

> Context: comment on «Refreshing the Illustrator», 3rd edition, proposal 1 ("The Illustrator does all the jobs there are in one flow."), 2026-10-17 19:03, relayed by the core Tertiary.
>
> > We should give that type of flow a special name, like an ephemeral flow, meaning when it doesn't wake back up. It can do as many illustrations as we want, really, up to a realistic level, obviously, like one session could do and maybe even up to a certain level of context.
> >
> > After 200,000 or 300,000 tokens, it's maybe not efficient to keep illustrating if it's the same instruction basically that we're given at the beginning of the context. Otherwise yes, it's an ephemeral context.
> >
> > These have sort of a default size up to which we want them to run a given number of jobs. If the illustration jobs keep coming in and it's still working, it can take them on. Like I said, if the context starts to climb up too high, then we can stop giving that one new illustrations and use another illustration.
> >
> > Even that ephemeral flow type has a full definition in those terms. It's a continuous job flow that can take jobs as long as it's running, right, meaning it's cached. It can reach up to a certain amount of realistic context, right? With Claude it would be 300,000 tokens maximum but at 250,000 we should really wind it down.
> >
> > Some kind of smaller figure for Codex, I guess, by default anyway, but some flows could even be allowed to compact. Although we can probably develop a flow refreshing technique that is more efficient than compacting because it's more targeted, more intentful, and more structured than the compaction, I think.
>
> -- psyche, input mode not shown.
- **554e1a vision/flow.md, entry 2 (#2335)** - 2026-10-28 — Codex threads may be left running on the app-server; Flow Nexus puts out the thread whe - full text under P1.5.

**Record 554e1a vision/flow.md, entry 3 (#2336)**, date/heading: 2026-10-29 — Codex threads are checked for accumulation; old ones are killed or archived

> Context: the living, in the Psyche core Primary chat 554e1a, while reviewing Vision by horizon.
>
> While I'm reviewing this, I'd like you to first find out what I mean exactly by referring to times when we talked about this. Have someone check to make sure that we aren't accumulating Codex threads anymore and that the old ones are being killed or archived (or whatever needs to happen to them), so that they don't accumulate and end up killing the system memory and even hitting the limit number of threads where we can't start new ones.

**Record 97bb3e vision/flow.md, entry 1 (#3233)**, date/heading: Test flows are cleaned up when testing is done

> Context: the living, to Psyche core Secondary 97bb3e, 2026-10-24, on the nine Haiku test flows whose panes stayed open after Retire.
>
> > Also there's now a whole bunch of [Claude] flows. I know they're for testing but once the testing is done we can't just leave them lying around. We're not litter bugs. Let's clean up after ourselves.
>
> Transcription corrected: "Clojure" → "Claude".

### P6.1. Harness events, nothing polls
**Proposed:** Flow learns a flow's state from the harness itself: a Claude flow's hooks call the Flow CLI at session start, prompt, tool use, turn end and session end; a Codex flow's app-server sends its turn events. Flow decides from its configuration where each event goes; nothing polls, and a poller that must exist is registered and reported. In the long term Flow keeps the account of usage from these events, so the machine spends what it has and never more.

**Record 5330c1 vision/flow.md, entry 3 (#943)**, date/heading: 2026-10-23 — long term hooks feed Flow; Flow a small monolith first; medium term hooks on all harnesses; Flow does the usage accounting; tonight's reiteration works in testing variants, stable keeps running

> Context: said after the first pulse scan showed every flow idle with its queue held and Flow's delivery dead.
>
> > Long term I would like a hook-based system. Flow should continually get signals from the hooks so that it knows when it can keep accounting for which flows are working and which flows are not working.
> >
> > As it is I feel like we're building Flow into a bit too much of a monolith. I would like some of the functionality to go into other nexuses but I think until we have a good freestanding small monolith of a nexus like Flow that can improve our system significantly, trying to do it with multiple nexuses is going to be really brittle. I think it's better if we build it up and then we can start taking functionality out of it into other pieces.
> >
> > Medium term maybe we introduce medium term as a concept to differentiate. Medium term I'd like hooks on all the harnesses that essentially notify Flow for everything that the hook can essentially hook into, so that Flow can have a lot of information on what's going on. Then the Flow system itself can become the tool that is used to manage both automatically in parts and with judgment from a thinking machine in other parts.
> >
> > How much of each? Obviously if some things will be spun up, then a judgment has to be made on what and how, which is where the thinking machine comes in. The decision that more spending should be done, or that more spending should not be done for now, can rest with Flow. Flow could keep tabs, do the accounting, so to speak, of the usage quotas, so that we never overspend too much, especially at night when I'm not watching or when there's a lot of things to do and there isn't that much usage.
> >
> > The information can be given to whoever is coordinating the work to pull back on some things which are less pressing, to save usage for later. To make sure that the living has access through a thinking machine at any time of the week, so that if he has an idea he has a thinking machine to talk about it with. Also to make sure that by the end of the week all or almost all of the usage has been spent. It's a delicate balance and it's going to be really important for the system to work optimally. This is the kind of stuff (this and probably some other important things) that the reiteration, let's say for tonight, can work on in testing variants of the Flow Nexus. The stable version is what we keep using so that we don't end up with the broken situation we had this morning.
>
> -- psyche, STT.

**Record 840e42 vision/flow.md, entry 1 (#2356)**, date/heading: Flow is hooked to the harness's hooks as notifications for everything; when the agent comments, Flow is notified and can decide on it

> Context: said to the primary Claude 840e42 after it reported that cross-session messages sit held for approval; "hooks like that" refers to those delivery notices. "Let's hook up flow" is also a working instruction, recorded in log.md. Logged directly by the main flow before acting.
>
> > And make the flow be aware of hooks like that. Let's hook up flow to the hooks of the harness as notifications for everything. If the agent comments, flow gets notified, and then it can make a decision on that.
>
> -- psyche, STT.

**Record da2038 vision/flow.md, entry 10 (#1515)**, date/heading: Flow decides where hooks talk

> Context: same speech to the Psyche Core Tertiary, on hooks; relayed by Psyche Core Secondary.
>
> > We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).
>
> -- psyche, STT, 2026-10-14.

**Record 55a2b4 vision/flow.md, entry 1 (#1754)**, date/heading: Flow decides where the hooks talk

> Context: spoken to the Psyche Core Tertiary on hooks, after the Flow books of 2026-10-14; relayed by Psyche Flow Secondary da2038.
>
> > We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).
>
> -- psyche, STT, 2026-10-14, relayed by Psyche Flow Secondary.

**Record 7328f4 vision/polling.md, entry 1 (#726)**, date/heading: Flow state through hooks, as cheaply as possible, no polling; a registry of polling systems

> Context: After the Herdr research came back; the living had just reset Codex.
>
> > I've reset Codex and we need to also start working on the hook/[Herdr] functionality for getting the state of what's happening in a flow as cheaply as possible, with no polling. We really wanted to [de-emphasize] polling and if we do poll it would be a really long period and it'll be for something really important. I need to have a periodic report on any system that's polling so that it doesn't run out from under me.
> >
> > Even if it's stateful, I've also been having problems with stateful services that we're polling that I kind of asked for but we don't want to forget about them. We need some kind of registry of polling systems somewhere. That would be a field thing.
>
> -- psyche, STT. 2026-09-30. Transcription corrected: "harder" → "Herdr"; "emphasize" → "de-emphasize" (read from "with no polling"; unconfirmed).

**Record b666e7 vision/hook.md, entry 3 (#1420)**, date/heading: Flow state without polling

> Context: relayed by Psyche Opus 7328f4 on 2026-09-30; speech-to-text corrections supplied in brackets.
>
> > "I've reset Codex and we need to also start working on the hook/[Herdr] functionality for getting the state of what's happening in a flow as cheaply as possible, with no polling. We really wanted to [de-emphasize] polling and if we do poll it would be a really long period and it'll be for something really important."

### P6.1b. Reminder; heartbeat never shorter than an hour
**Proposed:** A flow that must look again after a time asks Flow for a reminder: a Notice to its own address, delivered at the time it names, waking it if it sleeps; no flow keeps a timer, a script or a harness schedule of its own. The heartbeat is such a reminder, never shorter than an hour, reminding the flow it reaches to judge its own sanity by these signs: an echo chamber, where the same question or claim goes round between flows and comes back; jargon and nonsense increasing; an acknowledgement answering an acknowledgement. The counts it carries, awake metaflows, working panes, queued requests, are evidence under the reminder; the judgment is the flow's. The number of running flows is kept low.

**Record bf8ae0 vision/flow.md, entry 5 (#1155)**, date/heading: 2026-10-27 — Reminders are a Flow feature: a flow asks Flow to wake it at a time, since Flow already sends messages; for the next wave, after what is slated

> Context: the living, direct, after I scheduled my own wake with the harness's tool.
>
> > I think this would also be a cool feature in Flow: to give yourself reminders so you don't have to make ad hoc scripts for this kind of stuff. Plus Flow already knows how to send messages so I think it would be a perfect place for it. ... I don't want to make this a blocker for what we currently have slated so it would be something that we could do afterwards.

**Record bf8ae0 vision/flow.md, entry 4 (#1154)**, date/heading: 2026-10-27 — A flow wakes itself a little under an hour on, inside the cache, to check on things and rewarm the cache

> Context: the living, direct, going for a nap.
>
> > Do you want to create a reminder for yourself to be woken up in a little less than an hour, which is how long I believe the Claude caches are? ... There's a 5-minute one, which makes it even cheaper, but I think there's a 1-hour cache, which is still less than half the price of a non-cached call. That way if things got stalled (let's say you give yourself a reminder to check on things in 50 minutes), then your reawakening wouldn't cost so much. Plus it would rewarm the cache and if things didn't go well then you could catch it without me having to wake up.

**Record bf8ae0 vision/flow.md, entry 7 (#1157)**, date/heading: 2026-10-27 — The pulse: hourly is enough; a 20-minute check with instructions can be the Secondary's, Opus being far cheaper; the Primary keeps itself warm under the hour

> Context: the living, direct, same message.
>
> > Please don't let me down, and don't feel shy to check on the hourly. Maybe you don't have to check so much. If you feel like you need to check in 20 minutes, that's okay, but you can also slack back and go to the hourly. ... Sometimes you can also ask to be messaged back through your secondary, as always, or maybe you can have your secondary do the pulse. It's good to keep you warm below the 1-hour cache time, but Opus is way cheaper than Fable.
> >
> > If you want to do a 20-minute check with instructions on what to check and what to wait for, then your secondary could be a good replacement for that. You could always keep yourself warm on the sub-hour thing.

**Record 046782 vision/flow.md, entry 1 (#1421)**, date/heading: 2026-10-28 — The pulse is never shorter than an hour

> Context: the living, direct, after the Secondary's pulses came in every twenty minutes; supersedes the 20-minute Secondary check in flows/bf8ae0/vision/flow.md.
>
> > dont make the pulse shorter than an hour

**Record ce46fb vision/flow.md, entry 1 (#111)**, date/heading: Fewer flows running; the heartbeat checks their number and sanity

> Context: said to Psyche flow Primary ce46fb after a night of pulse reports and flow-to-flow relays, Herdr beeping at every finished flow.
>
> "There are a lot of flows running right now, and I hear a lot of activity since the [Herdr] program makes a beep every time a flow finishes. Maybe we can sort of calm down on the number of flows that are running, and that could be part of the heartbeat check to make sure that there aren't too many flows running. I don't know what these flows are doing there, just to keep messaging each other. It almost feels like they're maybe stuck in a loop or something. Maybe you can help them out. Make sure they aren't going fucking insane. Do a sanity check with those heartbeats, and tell me what you think."
>
> -- psyche, STT. Transcription corrected: "herder" → "Herdr".

**Record ce46fb vision/flow.md, entry 2 (#112)**, date/heading: The heartbeat reminds flows to do a sanity check; the judge of sanity is the flow

> Context: correcting my reading of the previous entry, which I had turned into counts and ceilings in the pulse.
>
> "I don't know if you understood what I meant. I said, 'Make those heartbeats.' One of the things that they remind us of is to do a sanity check. I can let you be the judge of what is sane and what is insane. Use an agent, maybe use a subagent, to check what all this chatter is about and to check for signs of insanity, like an echo chamber (where things just go in a circle over and over) and where the amount of jargon and nonsense keeps increasing."
>
> -- psyche, STT.

**Record ce46fb vision/flow.md, entry 3 (#113)**, date/heading: Land the heartbeat vision, compensation against loop messaging, investigate; audit for wrappers and non-Clojure prototyping

> Context: after I reported the sanity verdict (loop-shaped relaying; delivery fix undeployed) and proposed heartbeat lines.
>
> "Yeah, that's a good [heartbeat] vision proposal. You can land that and enforce it, and do some kind of compensation. Just land some compensation context to try and offset the loop messaging madness, and investigate it. Look into other people online who might have reported that kind of behavior and what it's from, and maybe how to deal with it. Do what you can, and then in the morning we'll look into it more together.
>
> Don't discourage work around yourself now to check for things that could be audited or have their implementation improved, especially when it comes to removing useless code like wrappers, like these stupid wrappers we had before. Let's make sure there's none of that crap. You can do a round to make sure that we don't use any prototyping languages other than Clojure. Make sure that we're actually doing useful work and not just madness loop talking."
>
> -- psyche, STT. Transcription corrected: "hardbeat" → "heartbeat".
- **ce46fb vision/flow.md, entry 4 (#114)** - Bring down the number of flows; retire unused topic flows - full text under P1.5.

**Record 9457ab vision/flow.md, entry 1 (#2421)**, date/heading: Heartbeat checking, with a fallback check later

> Context: the living asks the Psyche core Secondary, 2026-10-23, whether the heartbeat checking mechanism is in place and working.
>
> "Has the heartbeat checking mechanism been put into place and is it working? If not then you, primary, mi[nd], and field can coordinate on giving another shot. Perhaps you can have some sort of fallback to make sure that you check later to make sure that it has worked."
> -- psyche, STT. Transcription corrected: "mine" → "mind".

**Record da2038 vision/flow.md, entry 25 (#1530)**, date/heading: Flow lands, merged and deployed, the Flow Nexus in production; a heartbeat brings the important topics back; reports on every major Astra effort; Flow respecified until it accepts system prompts, user prompts and specialized flows from flow definitions in a datom dialect specified in Ethos

> Context: spoken to the Psyche core Tertiary, 2026-10-16; relayed to da2038 by Psyche Core Secondary as #psyche.
>
> > I want a fresh Astra Flow to tackle Flow again, with the latest proposal and the latest vision from Fable making a book for the design. I want Flow to land, be merged in main, and be deployed. I want the Flow Nexus used in production. I want nothing more than that.
> >
> > I almost want to put a 4-hour timer that tackles the topic if it isn't being tackled. Maybe every 6 hours, 4 times a day, we make sure that this topic or some topic is being addressed. We need some kind of heartbeat to get back to the important topics, mostly codex-driven, with Opus and Fable guiding.
> >
> > This is what I want to see books on. I want to see reports every time Astra does a major effort, which get published, and every time I talk about Ethos, Nexus, or Flow. I want all the proposals refreshed with what I've added. I want to keep respecifying, reironing, and retesting Flow until it works: until it accepts system prompts, user prompts, and programmatic specialized flow based on special flow definitions, all done in a special dialect of datom ethos specified.
>
> -- psyche, STT, relayed by Psyche Core Secondary.

### P7.1. Behavior is configuration
**Proposed:** Flow hardwires no behavior a person might want otherwise. Every model, effort, threshold, timing, limit, text, harness argument and route is configuration: typed datom, kept in Flow's Memory, changed through the meta socket, and authored as datom files in the context repositories, sent in succession when Flow is deployed. A value absent from configuration leaves its behavior off.

**Record 63aef7 vision/flow.md, entry 1 (#0)**, date/heading: 2026-10-26 — Tool removal is a configured module, nothing hardwired

> Context: the living, direct, correcting my two readings of "your belief is defective" (vision/tools.md). Vision on Flow's configuration.
>
> > No not quite. You don't seem to understand how this works. You're taught how to use the tool in your system prompt, I'm guessing. If we take out the tool we have to take out that part of the system prompt.
> >
> > This again: nothing is hardwired in code. All of this needs to have operations that allow us to create configuration datoms to specify how it works, which part of the system prompt. We would configure this module: we would create these datoms. It would have a name, let's say Claude artifacts or whatever, whatever the harness artifact calls. We should just reuse their terminology.
> >
> > It would explain which part of the system prompt corresponds with this and which tool corresponds with it and would need to be removed from the flow that wants to remove it. We would have a blacklist section for configuring main flows or meta flows.
> >
> > Do you understand what I'm saying? None of this would be hardwired in the code. Absolutely, absolutely none of it. Every kind of feature like this we want to develop has to create an interface that allows us to configure it on the fly. If we hardwire stuff in the code now, in the worst scenario it becomes a critical problem and we've created a completely broken executable. In the best-case scenario now we're unable to experiment with different approaches and to adapt to changing system prompts in the new version of the harness or whatever.

**Record edf227 vision/flow.md, entry 2 (#33)**, date/heading: Flow's configuration lives in its own database and memory, not in Markdown files

> At "the model behind a layer is configuration in a knowledge skill".
> > "No the configuration flow does not live in a Markdown file in every story. It lives in its own database and its memory. That's where the configuration goes so this is a hallucination by mixing up concepts that don't belong within this report."
>
> -- psyche, typed, book comment, 2026-10-03 18:13. Transcription uncertain: "in every story".
- **36ac89 vision/flow.md, entry 4 (#1560)** - No restrictions hardwired into Flow; seats have their tools and subagents - full text under P3.4.
- **36ac89 vision/flow.md, entry 5 (#1561)** - Every main flow can talk with the living; no tool limits in code, used at once - full text under P3.4.
- **36ac89 vision/flow.md, entry 6 (#1562)** - All capabilities, unlimited, some on the meta socket - full text under P3.4.

**Record 36ac89 vision/flow.md, entry 8 (#1564)**, date/heading: Overnight: no hardwired behaviour that should be configurable

> 2026-10-26, said to Psyche core Tertiary b195f0, relayed to Psyche core Secondary 36ac89 by cross-session message (the Tertiary's own log holds the record).
>
> > I made some comments on a recent book about Flow. Collect them, pass them on to Secondary, and get him and Fable to coordinate to reimplement some things overnight thoroughly. Make sure that there is no more hardwired behavior that we want to make configurable and that should be configurable in the software. Fable can make the design if there's any. If there's anything to design without my approval just to get something built overnight, don't block on anything. Get your Secondary and Primary aspect to do the coordinating and designing and get your Mind to do the implementation with Secondary and Primary as well.

**Record c637a5 vision/flow.md, entry 4 (#1653)**, date/heading: 2026-10-27 — Implementers are not handed raw psyche logs; a restriction they build is data-driven and off when unconfigured

> Context: the living, direct, after I launched the fresh Mind flow 2c06c7 with the rebuild order.
>
> > And be careful with passing over raw psyche logs, because, as we've seen, the implementers are really good at taking my invariants out of context and mistaking them for short-term goals that they need to put in the code and put inflexible behavior in the code. If you give them invariants and they put in these restrictions (and I'm not sure that that's a good idea anyway, but let's say they do), then it certainly has to be done using a configurable feature, meaning it has to use data to drive that behavior, and so that we can essentially drive the system with it turned off if it's unconfigured.

**Record 74e4d1 vision/flow.md, entry 1 (#2974)**, date/heading: 2026-10-26 — Roles are defined with data queries; no rebuild of the executable to change them

> Context: the living, direct, to Psyche core Primary 74e4d1, during the switch to Flow 0.40, on the report that a pane's flow had no known role in the new store.
>
> > What do you mean the pane's [flow] had no known role in the new store? We're configuring this, right? None of this is hardwired in the code. Let's make sure we can define roles with queries with data and that we don't have to rebuild the whole executable every time we want to change something like that. I'm assuming you wouldn't be foolish enough to try and do it like that but I'm just making sure.
>
> Transcription corrected: "low" → "flow".

**Record 9aaaba vision/flow.md, entry 4 (#354)**, date/heading: 2026-10-28 — No EDN anywhere; it is all datom

> > There shouldn't be EDN involved anywhere. Why are you talking about EDN? It's all datom.

**Record 9fed42 vision/flow.md, entry 4 (#1606)**, date/heading: Nexus configuration loaded atomically from datom payload files

> Context: relayed by 445410; part of his comment on «The new flows, as they run».
>
> > Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant. Let's do this.
>
> -- psyche, STT, 2026-10-09 20:41, relayed by 445410.

**Record f5a6e9 vision/flow.md, entry 8 (#3642)**, date/heading: The Flow Nexus is started by datom commands; its configuration is loaded atomically from datom payload files in separate repositories, sent in succession on the meta socket

> Context: his comment on «The new flows, as they run», 2026-10-09 20:41, in part; relayed by 445410 and 9fed42.
>
> > Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant. Let's do this.
>
> -- psyche, STT, book comment, relayed by 9fed42.

**Record 9aaaba vision/memory.md, entry 2 (#362)**, date/heading: 2026-10-28 — The database is Memory

> Context: the living, direct, after I called Flow's database flow.sema.
>
> > For the thousandth time the database is not called SEMA anymore. It's called memory so there's more of my vision being ignored.
>
> > Basically SEMA should not be anywhere near any of the database code in any way, shape, or form.

**Record 2d9f4d vision/flow.md, entry 1 (#2593)**, date/heading: 2026-10-26 — The harness module is the section; no module name beside a section name

> Context: the living, by comment on the Flow book «Flow by configuration» (https://claude.ai/artifact/PcEZpsWgcBZxxyuYVwg99K), anchored on HarnessKind in the HarnessModule ethos of Proposal 2.
>
> > There's no need to have a module name and a section name. It's repetitive unless you think that one module has one section, which doesn't make sense to me. The module is the section. There's no point in creating all this duplication. As you can see in the datom, it just ends up with a very repetitive datom.

### P7.2. An operation for every bind; meta socket
**Proposed:** Every situation has its operation, so no bind needs a rebuild: rebinding a metaflow to a pane or a flow, releasing its lock, delivering its queue, compacting a flow, closing it, importing a running Herdr session, reading any record. The meta socket is open locally to every flow.

**Record 63a06a vision/flow.md, entry 1 (#3631)**, date/heading: 2026-10-25 — Debugging operations for every situation; Fable may fix Flow

> Context: said directly to Psyche flow Primary 63a06a in its first turn, while it read its successor prompt, before any presentation.
>
> > Well I did ask for Flow to be fixed, for the system to be fixed, and for all the debugging operations we might need (to get out of all the kinds of situations we found ourselves in, like rebinding a meta Flow to a new pane or to a new Flow ID or things like that) to be part of the system so that we don't keep running into this same kind of problems.
> >
> > Flow needs to be fixed, obviously, right? Well [Mind] has been unable to fix Flow properly. Maybe it's best for you to do it.
>
> -- psyche, STT. Transcription corrected: "mine" → "Mind".
- **36ac89 vision/flow.md, entry 6 (#1562)** - All capabilities, unlimited, some on the meta socket - full text under P3.4.

**Record d8df70 vision/flowTool.md, entry 2 (#1126)**, date/heading: A meta socket binds already-running processes: the Herdr session first, then a vector of its flows in one call; a tool gathers a flow's anatomy and writes its datom

> > Let's create, in terms of adding the current flows into the database, a meta socket for debugging for adding already existing processes. Add an already existing Herdr first because the Herdr is going to bind with the pool, or whatever the meta flow is, and then the thinking machine flows that are running inside that meta thinking machine flow are going to be bound.
> >
> > They can either be bound in a single call with a vector. Just let it take a vector of the structs that we need to bind, the struct with all the data. Create the anatomy of what a flow looks like and then let's create maybe some tool that can get all that information and create the datom for it.
>
> -- living, input mode not established, 2026-09-24, to Psyche Medium d8df70, answering how the current flows get into Flow's database. Transcription corrected: "herder" → "Herdr" (twice).

**Record d8df70 vision/flowTool.md, entry 3 (#1127)**, date/heading: One Herdr session is a flow container of typed flows; bootstrap the live one by hand now, an import tool later

> > We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now. One Herdr's session is one pool but I don't like the word "pool." It's a cluster. No it's a meta flow. No I don't know. It's a container. It's a flow container that has many flows in it: many typed flows. Typed flow meaning psyche, mind, and field, and then we're going to have sub-subroles, subtypes like that.
>
> -- living, input mode not established, 2026-09-24, to Psyche Medium d8df70. Transcription corrected: "herder" → "Herdr" (twice), "harder" → "Herdr".

**Record 8624c4 vision/archive-flow.md, entry 2 (#3221)**, date/heading: The meta socket has its own signal

> Context: asking whether to start a fresh Fable flow for a proposal on Flow, Ethos and Nexus.
>
> "... all of its different ethos (which, by the way, also includes the meta signal, right, the meta socket signal, which is a different signal declaration than the norma [sic] socket, which I don't recall seeing in any recent proposals, which maybe warrant an update into some context modules or another)"
>
> -- psyche, STT.
- **5ec12c vision/flow.md, entry 2 (#2494)** - 2026-10-22, living, standing order, to Psyche core Secondary b7a16a, relayed; originals in flows/b7a - full text under P4.4.

### P7.3. Harness defined per version; blacklist; stock prompt diffed
**Proposed:** A harness is defined per version in configuration: its executable, its arguments, the modules of its stock prompt and tools by their own names, and which of them a flow leaves out. A harness-blacklisted module names the lines of a harness version that are not ours and voids them in every flow of that harness; the stock prompt per version is extracted and diffed against the modules by a tool outside Flow.
- **63aef7 vision/flow.md, entry 1 (#0)** - 2026-10-26 — Tool removal is a configured module, nothing hardwired - full text under P7.1.

**Record 63aef7 vision/flow.md, entry 3 (#2)**, date/heading: 2026-10-26 — The system prompt reproduced as a datom, sectioned and configurable by module name

> Context: the living, direct, after my presentation of the Flow survey under way; designing the mechanism for the configured removals above, and offering himself as a design fallback.
>
> > And you probably need to design with me as a fallback to help you figure this out if you're not sure how to approach it.
> >
> > How is the code going to be able to take out the parts of the system prompt that correspond with the modules you're blacklisting? Do you understand what I'm saying? There has to be a logical mechanism for doing this.
> >
> > Either we create a full mapping of the system prompt in yet another data type, a datom, right? Always a datom that possibly is a comprehensive reproduction of the full system prompt from the stock harness. Essentially we would explicitly inject our own reproduction of the system prompt and just remove the default one. Then we could section it, label it, and make it modular: which parts we want, which parts we don't want, and which parts we want to modify and override with our own version, right?
> >
> > We would create names that correspond with the concepts that certain sections are really about or whether or not they're about a certain tool, which part of the system prompt configures this tool, and so on. Then we would make this whole system prompt totally configurable by module name.

**Record 63aef7 vision/flow.md, entry 4 (#3)**, date/heading: 2026-10-26 — A separate tool extracts the stock prompt per harness version and diffs it against the modules

> Context: the living, direct, answering my unknown on how the stock prompt is captured per harness version.
>
> > Yeah you could use your mind to create a tool, probably an enclosure, that, every time there's a new version, can extract the prompt and then compare it with the previous version (create a diff basically). We would have a text per version, like an output, and then you can use that sort of canonical system prompt text as a reference, with line and column numbers corresponding to our modules. You could know which modules are affected by the diff. This doesn't need to be part of the system; it can be a separate system from the system that reproduces the system prompt in Datom. You understand what I'm saying?

**Record 63aef7 vision/flow.md, entry 5 (#4)**, date/heading: 2026-10-26 — Universal abstractions, per-harness parts, configuration over hardwiring

> Context: the living, direct, on the prompt-extraction tool above.
>
> > Obviously the tool would work differently with different harnesses. So you need to create the abstractions that are universal and then the parts that are per-harness code, right? Ideally as always, favor configuration over hardwired behavior.
- **046782 vision/flow.md, entry 2 (#1422)** - 2026-10-28 — A harness-blacklisted module removes the harness's shell-preference line from the next  - full text under P3.1.
- **2d9f4d vision/flow.md, entry 1 (#2593)** - 2026-10-26 — The harness module is the section; no module name beside a section name - full text under P7.1.

**Record 2d9f4d vision/flow.md, entry 2 (#2594)**, date/heading: 2026-10-27 — Turning things off by flag and environment: a deep dive wanted, in a dedicated presentation

> Context: the living, by comment on the same book, anchored on the Configure.HarnessModules datom (the Skills module with its --disable-slash-commands flag and CLAUDE_CODE_DISABLE_BUNDLED_SKILLS environment).
>
> > I don't understand this flag part and disabling the skills. It doesn't really make sense to me although I guess that is a thing. Wow I didn't even think of that.
> >
> > With that as the only example where we use a flag, I'm really curious about that: those kinds of modifications. I didn't even think that it would go that far. I'd like maybe a deep dive on this aspect of turning things off, maybe in a dedicated presentation.
- **da2038 vision/flow.md, entry 24 (#1529)** - A lean flow: every removable part of the startup is a named module; a metaflow row sets which are re - full text under P3.1.
- **39bd0c vision/flow.md, entry 6 (#3724)** - Leaning out a flow: named modules in a blacklist, per metaflow row - full text under P3.1.

### P8.1. The capsule, Herdr, several capsules, import
**Proposed:** The Capsule is where flows run: a Herdr session holding one pane per flow, with its own sockets and store. Herdr is its first backend and is used as it is; the backend may be exchanged. Flow is the one writer into the capsule's panes and names a caller by its pane. Flow serves several capsules: a query that names none takes the default, and a variant with one more field names one. A running Herdr session is imported into Flow through the meta socket, the session first, then its flows in one vector.
**Finding:** The Comment says the semi-sandbox and volatile key "have no record". Records were found: 3ec648 capsule.md (2026-10-02, #672), 42265e capsule.md (#792) for the semi-sandbox; 91ea9f encapsulation.md (#632, #633) for the name Capsule and the volatile key ("a design for later on"). They are in the legacy first-embodiment text the book removes.

**Record 3ec648 vision/capsule.md, entry 1 (#672)**, date/heading: The semi-sandbox copies only the credentials

> Context: on testing the nexuses and flows outside the live system.
>
> > "You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox. I know it's possible if you just reuse the same credentials and you just recreate everything else. The only thing you copy is the credentials then it'll work.
> >
> > If there is a credential rotation then we need to maybe use the new credentials that have been... I don't know. Somebody brought that up but I don't even know if it's a thing. For now let's just test it the simple way."
>
> -- psyche, STT, 2026-10-02.

**Record 42265e vision/capsule.md, entry 1 (#792)**, date/heading: 2026-10-03 — The semi-sandbox copies only the credentials

> Context: Fable 9fb0ad relayed the original 2026-10-02 record from flows/3ec648/vision/capsule.md while Field was extending the isolated Claude witness.
>
> > You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox. I know it's possible if you just reuse the same credentials and you just recreate everything else. The only thing you copy is the credentials then it'll work.
>
> -- psyche, STT. Original 2026-10-02; relayed by 9fb0ad on 2026-10-03.

**Record 91ea9f vision/encapsulation.md, entry 2 (#632)**, date/heading: It is called Capsule

> Book comment on «The Capsule and the Semi-Sandbox», anchored to the Capsule heading.
>
> > "Yeah I think I picked the right word. It's going to be called Capsule."
>
> -- psyche, typed, 2026-10-02.

**Record 91ea9f vision/encapsulation.md, entry 3 (#633)**, date/heading: The volatile key is a later design: encrypt the sensitive parts of the file system

> Anchored to route (b).
>
> > "This is a design for later on. It's something that will just encrypt the file system so that we are creating a sort of hardware-layer encryption security. It doesn't have to encrypt the whole file system, just the parts where we put sensitive stuff."
>
> -- psyche, typed, 2026-10-02.

**Record 5330c1 vision/capsule.md, entry 1 (#948)**, date/heading: 2026-10-23 — what was called the Herdr is the capsule

> Context: said while ordering a real-world test of Flow in a separate capsule; the Herdr is the terminal workspace every flow runs in.
>
> > I think what I called the [Herdr] is the capsule, because we could change the [Herdr] for another backend.
>
> -- psyche, STT. Transcription corrected: "herder" → "Herdr".

**Record 5330c1 vision/flow.md, entry 2 (#942)**, date/heading: 2026-10-23 — Mind takes the reimplementation for a real-world test, in a testing capsule

> Context: said right after being told the Fable branch is final and unjudged. "Herder" is the Herdr terminal workspace; "Codex and Co." reads as Codex and company.
>
> > I want [Mind] to take it for a test. We should create this code in Nix that allows us to run this real-world test that just uses a different [Herdr] pane and puts all of these testing flows in a different capsule. I think what I called the [Herdr] is the capsule, because we could change the [Herdr] for another backend.
> >
> > Do you understand what I'm saying? Let's get this actually tested with multiple flows: Codex and Co. and Claude, with cheap low-effort models, just sending each other messages, seeing if they can start flows, seeing if the prompts are right, the system prompts are right, the tools are right, what's maybe missing in terms of features, and then come back to reimplementation again.
>
> -- psyche, STT. Transcription corrected: "mine" → "Mind", "herder" → "Herdr".

**Record 97bb3e vision/nexus.md, entry 2 (#3264)**, date/heading: Multiple capsules; a simple query on the default, a variant with one more field

> > There's another thing: it should be able to configure having different capsules, multiple capsules. That's the thing: we can have many different features that are not exposed in all of the queries. We would have a simple query to interact with Flow that just uses the default capsule and then we would have a slightly different query that maybe has just one additional field that lets us specify the capsule that we want.
> >
> > I want this pattern to become widespread especially in responses so that, for example, when we get responses we don't get all of the technical stuff like the message ID and the flow ID and all that crap.
- **752e0f vision/herdrSessions.md, entry 1 (#14)** - A single Herdr session controlled by Flow; Flow as the messaging tool - full text under P4.5.
- **d8df70 vision/flowTool.md, entry 2 (#1126)** - A meta socket binds already-running processes: the Herdr session first, then a vector of its flows i - full text under P7.2.
- **d8df70 vision/flowTool.md, entry 3 (#1127)** - One Herdr session is a flow container of typed flows; bootstrap the live one by hand now, an import  - full text under P7.2.
- **af762b vision/operational-flowOwnsHerdr.md, entry 1 (#3025)** - Basically, Flow is in charge of herder. I shouldn't interact with it directly. Message can get the d - full text under P1.1.

**Record c068b8 vision/flow.md, entry 2 (#3612)**, date/heading: Herdr as part of the architecture

> Context: book comment on "Flows and messages, 2nd edition", proposal 3 ("Herdr is never modified", for flow.md), 2026-10-21T13:55.
> "Well if you're going to talk about [Herdr], yeah sure. You can say we don't modify it but you could say how it's a part of our architecture at least. We're not just like, \"Let's describe Flow.\" Then this is the part that describes how Flow works, how it should be designed, how it should be used. The nexus ..."
> -- psyche, STT, book comment. Transcription corrected: "herder" → "Herdr".

### P8.2. Stable, last, next; testing binary; real-world test
**Proposed:** Flow runs as stable, last and next, each under its own name, socket and store; a testing binary never opens the stable store. A new Flow is tried raw in a testing capsule before it is deployed: cheap, low-effort Codex and Claude flows message one another and start flows, showing whether the prompts, the system prompts and the tools are right and which features are missing; the findings return to the implementation. The stable Flow keeps running meanwhile, so broken, stable and legacy systems run at once.

**Record e3c8c1 vision/flow.md, entry 5 (#600)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary e3c8c1

> Context: after Flow's store was wiped and its declarations reconfigured from the working tree, and flows launched through it again.
> "We need to have two, maybe three, versions of the tools that we develop in path, just with different names, so we can use that same `last` and `next` suffix, right? We have `last` in case somehow `stable` ends up not being as stable as we thought and then we have `next` so that we can fuck around with the next version and still be able to fall back on the old one."
>
> "What we should do when we test a new version of Flow is use it in a new [Herdr] pane. We need to give it the ability to keep track of multiple capsules, plus the new version would have the location for its database in a different place. I guess it would just create a new [Herdr] anyway. We could just start fresh every time and just sort of recompose the state if we want to. I guess we could eventually add functionality where a new Flow Nexus can use an old [Herdr] pane and sort of just repopulate its database using it."
>
> -- psyche, STT. Transcription corrected: "herder" → "Herdr".

**Record e3c8c1 vision/flow.md, entry 6 (#601)**, date/heading: 2026-10-23, living, direct, to Psyche core Primary e3c8c1

> "Let's develop atomically so that we can have broken systems running, stable systems running, and legacy systems running all at the same time. That way we can have continuous improvement, continuous development. We can break shit without worrying about breaking production."
>
> -- psyche, STT.

**Record 0595fb vision/flow.md, entry 3 (#992)**, date/heading: 2026-10-23 — ruling 84: a testing binary never opens the stable store

> Context: relayed by Psyche core Secondary f68131 to this Primary, before the two Flow flows run any raw binary.
>
> > Ruling 84, before the two Flow flows run any raw binary. A testing binary never opens the stable store. CriomOS-home gives each nexus a testing store path and a next store path of its own, as variables, and the raw binary is run against the testing one, so the two Flow flows get this in their briefs and Mind core Secondary gets it as the first deployment change, with the XDG_STATE_HOME reset in the next library as the defect that would make next share stable. Flow running as transient unit flow-nexus-b878 with flow-nexus.service inactive goes to Mind as a defect: stable is the service. The three points still go to the living in the book as alternatives, this ruling is the short-term one.
>
> -- psyche, STT, relayed by f68131.

**Record 36ac89 vision/flow.md, entry 1 (#1557)**, date/heading: Several Flow Nexuses at once; a new one tried raw before it is deployed

> 2026-10-25, to Psyche core Secondary 36ac89. Context: answering that the Flow refresh-from-outside build is built and tested but not deployed, its blocker unknown.
>
> > See if we do this properly, we can manually configure an already running [Herdr session] with its flows into any new flow nexus by using the operations that allow us to do that. We could have multiple flows even though they would fall out of sync as soon as you use one, potentially.
> >
> > Still it seems to me the running flow right now is only useful for starting flows and even then it's quite flawed because it only allows the flow itself to do it. It seems to me that we can have these multiple flow nexuses running simultaneously and the new one being tested doesn't need to be deployed through our operating system's declaratives. It doesn't have to be deployed declaratively, right? We can still test it by just running the binary raw, wherever it's built, with the right environment variables, in a hacky manner (which is essentially how you operate now 99% of the time anyway), to try it. Once we've established that it's reliable and so on, then we can deploy it.
> >
> > I really don't see a blocker here and I think that this approach should be added somewhere, [as a belief], maybe in a compensation.
>
> Transcription corrected: "herder capsule" → "Herdr session"; "and you believe" → "as a belief".

**Record 36ac89 vision/flow.md, entry 3 (#1559)**, date/heading: Production moves onto the tested Flow 0.40, run raw beside the old service

> 2026-10-26, to Psyche core Secondary 36ac89. Context: I proposed running the tested 0.40 build raw on its own socket beside the old service, moving the live flows over with Rebind all at once, its Curriculum branch running beside it, the old service kept as fallback.
>
> > So we could potentially use this testing version right now and then attempt to run our production on it. What do you think?
>
> > Yeah that's okay so let's do that.

**Record 97bb3e vision/flow.md, entry 3 (#3235)**, date/heading: A new version of Flow, tested in a different capsule

> Context: the living, to Psyche core Secondary 97bb3e, 2026-10-24 evening, answering 97bb3e's restatement of his five points (seats; comments fetched by the Tertiary; Fable decides what a new Primary is given for the anatomy; Mind's report on flow starting; Nexus configuration).
>
> > All right now you can start all of this and get [Mind] to write a new version of Flow that incorporates everything that I've said about how I want Nexus to work and what I would expect Flow to be able to do right now. Let's start testing it. I think it should be in a different capsule.
>
> Transcription corrected: "mine" → "Mind".
- **5330c1 vision/flow.md, entry 2 (#942)** - 2026-10-23 — Mind takes the reimplementation for a real-world test, in a testing capsule - full text under P8.1.
- **97bb3e vision/flow.md, entry 1 (#3233)** - Test flows are cleaned up when testing is done - full text under P5.5.

**Record e167d8 vision/stableNext.md, entry 1 (#1079)**, date/heading: Every service runs a stable and a next side by side on different sockets; rolling migration

> > It probably would be a good practice for a lot of these to have a stable package in [CriomOS] and then a next package, in the same way that we do the remote server.
> >
> > Maybe we can even create a reusable code pattern there in Next or something, or put it in a skill so these services can have a Next component that has a different socket. Then you can run both side by side when you do a migration. You can start into the Next service and then the stable version becomes the same as the Next and that would be the next step. The services can move to the stable socket on the next chance they get and then the Next socket, when it's free, becomes available again for another update. We have this rolling mechanism to keep updating.
>
> -- psyche, STT, 2026-09-26 ~11:55, to e167d8, on deploying Flow/Message 0.16. Transcription corrected: "KaliOS" → "CriomOS".

**Record fe945a vision/stableNext.md, entry 1 (#1010)**, date/heading: The rotation protocol: once every flow is on next, next becomes stable and the newer version goes on next

> Context: Field Astra d5b96b had left the living on an older Codex; the new version was staged on next but held.
>
> > Oh well, here's the protocol, right? The stable becomes the next [sic] once all the flows have moved onto the next socket. If all the flows are on the next socket now, next can become stable, and then we can put the next version on next.
>
> -- psyche, typed. 2026-09-30 13:59 UTC, d5b96b, Field Astra (session 01a0ee2e, line 4095). Reconstructed by fe945a from transcript. "The stable becomes the next" kept as written; the following sentence says next becomes stable.

**Record ebbe30 vision/deployment.md, entry 1 (#3359)**, date/heading: Next, stable, last: a test deployment branch everywhere

> Context: 2026-10-09; how a version is tested and how the upgrade stays smooth.
>
> > Let's use a test deployment if we want to test a certain version. We could have a test deployment branch everywhere, and that's how we can test-deploy something on the next branch. Let's just call it that, right? The next branch is that, so the next-suffixed package or server is from the next branch. That way, you can have a smooth upgrade, and we can have the last, which is a fallback in case somehow current becomes unstable or something, or it might actually make the atomic move more smooth.
> >
> > When we upgrade the NixOS layer, we're going to change these: next, stable, and last, but not necessarily, probably not all at a time. Eventually, we're going to have [Lojix] take care of the operation.
>
> -- psyche, STT, 2026-10-09. Transcription corrected: "logics" → "Lojix".

### P9.1. The Flow ethos; traits in the long term
**Proposed:** Flow is specified whole in Ethos: the Library its parts share, the Signal of its ordinary socket, the Signal of its meta socket, its Operation and its Memory. Every type is declared here and the Rust is generated from it; the bodies are hand-written. In the long term every trait Flow uses is declared here too. A datom below is written against the type above it.

**Record 875960 vision/flow.md, entry 1 (#1760)**, date/heading: 2026-10-11 — the full vision of Flow in ethos: signal, memory and storage ethos, all the traits and all the types

> Order to the Flow topic flow, relayed by core d68c82 through 9519a1. "Let's get the Flow topic flow to reaggregate" and "Let's give this a shot on Flow" are the working instruction; the vision is what the presentation is to hold.
>
> > Let's get the Flow topic flow to reaggregate everything about Ethos and Nexus and Flow and everything I've said about all these things. Present to me the full vision with the signal ethos, the memory ethos, and the storage ethos for it. I want to see traits also because all of the behavior, basically all of the traits. Here's what we need to do: we need to define all of the traits and all of the types in Ethos. Let's give this a shot on Flow.
>
> -- psyche, STT, relayed by 9519a1.
- **875960 vision/flow.md, entry 2 (#1761)** - 2026-10-12 — four comments on «Flow, whole, in ethos, third edition» - full text under P2.1.

**Record bf8ae0 vision/flow.md, entry 3 (#1153)**, date/heading: 2026-10-27 — The rebuilt Flow: implemented, tested, then used; old flows refreshed; the next design carries the code: all the ethos with example datom, and the Rust that matters

> Context: the living, direct, after agreeing the rebuilt Flow should replace the current one.
>
> > All right let's get this implemented and tested and then when it's done let's start using it.
> >
> > Once you get all this ball rolling (if it's not already rolling), I'd like you to start and to refresh your Flow and any of your other flows that are old. If I'm not talking to you by then you could create a first or a next design with code and everything.
> >
> > For Flow, the full vision with the code as we discuss, I want to see the code now, especially the ethos and the [datom]. I want ethos with example [datom]. I'd like to see all the ethos and some of the code that matters, even if it's in Rust, if you think it matters that it should be done a certain way or if you want to give some examples.
>
> Transcription corrected: "datum" → "datom".

**Record da2038 vision/flow.md, entry 23 (#1528)**, date/heading: All traits in Ethos is the long-term goal; in the short term, without it

> Context: on da2038's finding that ethos-zero generates no traits while Flow holds 209 hand-written traits; relayed to da2038 by Psyche Core Secondary as #psyche, 2026-10-16.
>
> > Yeah well, of course we can't meet all of our long-term ethos goals in the short term. That's why we have short term and long term. Long term we want all the [traits] in ethos and short term we just do without.
>
> -- psyche, STT, relayed by Psyche Core Secondary.
- **8624c4 vision/archive-flow.md, entry 2 (#3221)** - The meta socket has its own signal - full text under P7.2.

**Record 73b5d8 vision/flow.md, entry 2 (#184)**, date/heading: 2026-10-29 — The Flow flow first grasps his vision, then revises the whole vision of Flow and its ethos, with vision code

> Context: the living, same chat, after ordering the Flow work merged, audited by a Fable flow, fixed and deployed.
>
> And I'd like to put together a very well-trained... I guess this would be the Flow Nexus. I think the first thing the Flow Nexus should do is really make sure that he has a very good idea of what I have, what I envision for the Flow Nexus to do (being really mindful of not hardcoding behavior in the code), and then create a full revised vision for Flow and the Flow ethos that I'll review in entirety. Maybe looking for inconsistencies or repetition, and fleshing out the parts of the system that are either non-optimally designed or underdesigned, and bring some more vision code flesh out, right? Do you understand what I mean by vision code?

**Record 73b5d8 vision/flow.md, entry 3 (#185)**, date/heading: 2026-10-29 — Vision code is mostly Ethos and Datom; Nix where the vision depends on it; the belief on vision code reviewed

> Context: the living, same chat, after the Primary said vision code is the Ethos and datom in a vision statement.
>
> Well, it is usually mostly ethos and Datom, although if some of the rest is interesting to us, or if we're depending right on the vision, sometimes it might involve explaining how we like to use Nix (which would obviously involve Nix code). Maybe we want to review that as well: the belief that touches on all this.

**Record 73b5d8 vision/flow.md, entry 4 (#186)**, date/heading: 2026-10-29 — The vision-code line names the stacks, not one example

> Context: the living, same chat, on the proposed line "Vision code is mostly Ethos and Datom; where a design depends on how a tool is used, Nix among them, the statement carries that code as well."
>
> Your proposal is half good. One of the problems is that we now have a ghost effect because your example would skew the balance. We're welcome to give examples, but let's not forget the most important stacks that we use, right?

**Record b49eaf vision/flow-nexus.md, entry 1 (#158)**, date/heading: 2026-10-28 — The new Flow Nexus, implemented and audited, then a Psyche pair

> Context: the living, direct to Psyche core Secondary b49eaf, 2026-10-28.
>
> > And check up on things and ask primary what you should check up on in terms of: we need the new version of Flow with all of the improvements and bug fixes implemented and audited so we can spin up (if there isn't one already) or refresh a Psyche pair.

**Record b49eaf vision/flow-nexus.md, entry 2 (#159)**, date/heading: 2026-10-28 — A Psyche Flow Nexus pair scavenges the psyche and audits the implementation; behavior is data

> Context: the living, direct to Psyche core Secondary b49eaf, 2026-10-28.
>
> > Once the implementation is done and tested, we should have a Flow pair spin up and scavenge for all of the really good Psyche data on the Flow Nexus, Nexus development, Ethos development, all the things that touch this, how to develop, and how to keep behavior separate from the machine, the runtime. The behavior should be driven by data, not built into the runtime, which makes it inflexible.
> >
> > The Psyche Flow Nexus pair can actually audit the implementation to see whether or not the code actually conforms and whether or not the Ethos is well designed so that it avoids repetition both in itself and in the datom that fits into it. They can, through the secondary, always communicate.
- **5ec12c vision/flow.md, entry 2 (#2494)** - 2026-10-22, living, standing order, to Psyche core Secondary b7a16a, relayed; originals in flows/b7a - full text under P4.4.

### P10.1. Delivery replaces priority
**Proposed:** A sender asks one of three deliveries. Queue leaves the message for the next delivery. Wake delivers it, waking a sleeping metaflow. Abrupt interrupts the recipient's turn and is answered Sent or Failed, never Queued. The message itself carries no priority: the kind in its head says what it is, and Flow's records say how it was delivered.
- **b7ba00 vision/messaging.md, entry 7 (#229)** - The head is the message's kind, a new type carrying all its data; priority leaves the letter; soft a - full text under P4.1.
- **39373e vision/messaging.md, entry 1 (#2015)** - An abrupt message is sent or failed - full text under P4.2.
- **5ec12c vision/messaging.md, entry 1 (#2502)** - 2026-10-22, living, directly to Psyche core Secondary 39373e, relayed; two messages - full text under P4.2.
- **e591ed vision/messaging.md, entry 1 (#1959)** - The queue delivers everything at once, and delivers while the flow is idle - full text under P4.3.
- **9aaaba vision/flow.md, entry 2 (#352)** - 2026-10-28 — Not scrapped: the queue flushes as one message, the trigger included - full text under P4.3.

### P10.2. Delivery is harness-specific
**Proposed:** Abrupt on Codex is one Escape, and the prompt submits itself. Abrupt on Claude is two Escapes — the first is taken by the input editor in vim mode and never reaches the harness — then the prompt, then an explicit Enter, because after an interrupt the prompt is placed in the composer without being submitted. A Wake or Queue delivery is typed into the pane, or sent as the Codex turn, as the recipient's turn ends, and at once when it is idle; it carries everything queued, as one datom.
**Finding:** Harness mechanics (Escape counts, Enter after interrupt) are carried over unchanged from the existing vision:messaging module; no new raw record sought.
**No record found.**

### P11.1. Remembering: Open, Predecessors, Custom
**Proposed:** A launch names how far back the new flow remembers: Open, the open records of its address up to a cap on content, stopping one file short of it; Predecessors, the raw vision and notion logs of its predecessors to a depth; or Custom, flows named one by one. Custom and depth both remedy excessive remembering. The remembering is a field of the launch and of the declaration; the belief modules come from the declaration, from main; the brief comes last and carries the task alone. The logs are the record.

**Record b49eaf vision/remembering.md, entry 1 (#155)**, date/heading: 2026-10-28 — Open records of an address: who is at it, and a cap on how much is given

> Context: the living, comment on the book Record state (https://claude.ai/artifact/SAATHwe4A5XADjzzoqkahM), section "A fresh flow receives what is open", 19:35.
>
> > Well every record of its address first brings the question of how it knows which flows are at what address. Then how do we deal with addresses that have an excessive amount of open records, which is itself a problem and arguably should be resolved?
> >
> > In other words addressing them is a good idea but overwhelming a system isn't going to help it address anything. There could be a sort of cap on the amount of content so that it would find that cap and then stop one file short of that. That could be a short-term remedy to that problem.
> >
> > I don't agree on the index of archives. I don't see any point in that. This is just going to create noise in the system. We already have enough stuff to resolve without worrying about this stuff that has been resolved. If we do that we're just going to increment our way into a paralyzed system, like the guy who keeps eating and it's just getting fatter and fatter and his arteries are just getting completely plugged. At some point he's just going to die of overconsumption.

**Record b49eaf vision/remembering.md, entry 2 (#156)**, date/heading: 2026-10-28 — Custom and depth both remedy excessive remembering

> Context: the living, comment on the book Record state (https://claude.ai/artifact/SAATHwe4A5XADjzzoqkahM), section "Remembering gains Open", on Custom.Vector<FlowId>, 19:35.
>
> > Good. This also has a variant which allows us to at least temporarily get around the problem of too much to remember, whereby we would use the custom or the depth anyway. I guess both variants have a remedy to avoid excessive remembering.
- **74e4d1 vision/refresh.md, entry 1 (#2986)** - 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a  - full text under P3.1.
- **a68420 vision/flow.md, entry 6 (#2287)** - 2026-10-23, living, direct, to Psyche core Primary a68420 - full text under P3.1.

**Record 0595fb vision/flow.md, entry 2 (#991)**, date/heading: 2026-10-23 — ruling 83: the remembering route

> Context: relayed by Psyche core Secondary f68131 to this Primary. "The set" is the raw-record set carried in the Mind brief; ruling 73 is the remembering route.
>
> > The set you carried stands, new against HEAD or dated today plus the two standing-order flows. The full set is never a larger CLI argument: the route is ruling 73, Flow resolves Remembering to flow ids and Curriculum composes those flows raw records into the first message from the records root. That is part of what the two Flow flows are to build, say so in their briefs.
>
> -- psyche, STT, relayed by f68131.

**Record 73b5d8 vision/remembering.md, entry 1 (#187)**, date/heading: 2026-10-29 — Everything to propose goes in one proposal; the remembering goes in the middle stratum

> Context: the living, in the Psyche core Primary chat 73b5d8, after the Primary's chat proposals and its admission that the evolution moved only because he asked.
>
> Make sure everything you want to propose to me is in the proposal now. Maybe review everything. Make sure that you haven't forgotten something important that I said in your previous flow or in its predecessor. The flow launching is still quite broken and you seem to forget a lot of important things. Make sure that whatever you remember goes in your middle stratum. Maybe we should make this standard behavior since I seem to make you do this every time. But I would prefer, of course, in the long term, if we could avoid such a waste of tokens (since all of that could be done by a properly configured system that passes over the right modules every time the Flow is refreshed).

### P11.2. Refreshed flow: beliefs, raw logs, open beads, no summary
**Proposed:** A refreshed flow receives its beliefs, the raw vision and notion logs its remembering names and the open beads of its address, and those alone: no summary and no handover. The predecessor's biases end with it.
- **74e4d1 vision/refresh.md, entry 1 (#2986)** - 2026-10-26 — No summary and no handover to the successor; beliefs and raw vision logs are passed; a  - full text under P3.1.
- **74e4d1 vision/refresh.md, entry 2 (#2987)** - 2026-10-26 — Approved: the no-handover line; refresh the Primary; every flow understands Ethos, Dato - full text under P5.3.
- **a68420 vision/flow.md, entry 6 (#2287)** - 2026-10-23, living, direct, to Psyche core Primary a68420 - full text under P3.1.
- **b49eaf vision/remembering.md, entry 1 (#155)** - 2026-10-28 — Open records of an address: who is at it, and a cap on how much is given - full text under P11.1.
- **bf8ae0 vision/archive-remembering.md, entry 1 (#1175)** - 2026-10-27 — Compaction weighs every message of his alike; what is wanted is to weigh his content an - full text under P3.1.

**Record 2933ce vision/remembering.md, entry 1 (#1380)**, date/heading: 2026-10-29 — The living's words can be lost when a flow refreshes before logging them

> Context: the living, direct to Psyche core Primary 87f1ee, 2026-10-29; relayed by that Primary as his words.
>
> > Sometimes I find that I say something and maybe before you even have time to log it, your flow is refreshed before you even had time to log my vision or Notion. I don't know if my words got lost so I'm warning you. Maybe you want to look into that.

### P12.1. Presentation line moves to collaboration
**Proposed:** A flow gives a presentation, a response that could fit into a book, whenever it is given significant new context to consider: its first turn ends in one, and so does every task, goal or question that originates in the living. A message from another flow that only updates it is answered with a short note. A presentation takes its form from the belief modules the flow was loaded with and from its prompt, the one string given to that flow alone, which is no belief module.
**Finding:** This is a moved line, not a new one: the module already carried it. The Comment states the living's 10-21 comment (3611).

**Record c068b8 vision/flow.md, entry 1 (#3611)**, date/heading: Collaboration lines do not go in flow

> Context: book comment on "Flows and messages, 2nd edition", proposal 3 (flow.md), on its first sections: stopping wrong work, work going up whole, 2026-10-21T13:54.
> "This stuff is good but does it? I haven't read it all but the stuff that I've read, the first few paragraphs, doesn't go in flow and they might not even all go to the same place. This is like behavior maybe, something like collaboration, flow collaboration, or flow communication, or something from the first paragraph. That's the vibe I'm getting for where this would go or something, if we have something similar."
> -- psyche, STT, book comment.

**Record 9fed42 vision/flow.md, entry 2 (#1604)**, date/heading: A new flow's first response is a presentation of its context

> Context: relayed by 445410; same message as the psyche-type message entry, on a new flow's first response.
>
> > The worst thing to make a new flow do is to tell it to just say, "You're ready." We need to tell flows, if they don't have it, to start with a startup task: their first last response is to give a presentation of their context, to distill their context for a vision. ... That's what their first last response is. Their first goal when they loaded up all their context is to take all this context now, get some sub-agents to ask questions, reinforce your context, and then give a presentation. A presentation according to your role, which is described when you load that flow properly with the skill for its role, for its aspect, and for its layer, and for its topic
>
> -- psyche, STT, 2026-10-09, relayed by 445410.
- **73ada7 vision/flow.md, entry 1 (#1256)** - 2026-10-09 — A new flow's first response is a presentation distilling its context, not "ready" - full text under P3.2.

### P13.1. No flow claims its id (intent:main-flow)
**Proposed:** You run a shell command for one thing only: the writes you own, your psyche records; your Flow ID is given to you at launch. Everything else goes to the flow whose topic it is or to a subflow with a brief. The main flow gets the work done: through the flow whose topic it is while that flow answers, otherwise through its own subflow. A lock whose holder is dead is released by whoever meets it. Primary edits go to the standing committer while it is live; otherwise the flow that holds the order commits them itself, its explicit paths only. In other repositories, commit and push your own changes.
- **c068b8 vision/flow.md, entry 4 (#3614)** - A flow is told its Flow ID when it starts - full text under P2.2.
- **73b5d8 vision/flow.md, entry 1 (#183)** - 2026-10-29 — The Flow Nexus gives a flow its Flow ID; the evolution is reported - full text under P1.1.
- **9fb0ad vision/deterministicWork.md, entry 1 (#2227)** - The model does not check the flow id; it gets it in its prompt; anything deterministic is code — to  - full text under P2.2.
- **f55ec8 vision/flowIdentity.md, entry 1 (#1790)** - The process that starts a flow passes the Flow ID into the prompt, with the files and directories al - full text under P2.2.

### P14.1. Versions side by side (nix-builds)
**Proposed:** A Nexus is built in its versions, stable, last and next, each a Nix output under its own name, so that one host runs them side by side, each on its own socket and store. The deployment names which version is the service; a testing binary runs raw from its build, against its own store, until it is proven.
- **e167d8 vision/stableNext.md, entry 1 (#1079)** - Every service runs a stable and a next side by side on different sockets; rolling migration - full text under P8.2.
- **fe945a vision/stableNext.md, entry 1 (#1010)** - The rotation protocol: once every flow is on next, next becomes stable and the newer version goes on - full text under P8.2.
- **ebbe30 vision/deployment.md, entry 1 (#3359)** - Next, stable, last: a test deployment branch everywhere - full text under P8.2.
- **e3c8c1 vision/flow.md, entry 5 (#600)** - 2026-10-23, living, direct, to Psyche core Primary e3c8c1 - full text under P8.2.
- **0595fb vision/flow.md, entry 3 (#992)** - 2026-10-23 — ruling 84: a testing binary never opens the stable store - full text under P8.2.
- **ebbe30 vision/deployment.md, entry 1 (#3359)** - Next, stable, last: a test deployment branch everywhere - full text under P8.2.

### P15.1. Configuration is data, sent at activation (nix-workflow)
**Proposed:** A Nexus's configuration is datom files in a data repository; activation sends them to the running Nexus through its meta CLI, in succession, so the deployment holds no configured value and reads no other notation; the configuration input is the context repository that holds the file. A testing build runs raw against a testing store and never the stable one; the declarative deployment carries the proven revision.
- **9fed42 vision/flow.md, entry 4 (#1606)** - Nexus configuration loaded atomically from datom payload files - full text under P7.1.
- **f5a6e9 vision/flow.md, entry 8 (#3642)** - The Flow Nexus is started by datom commands; its configuration is loaded atomically from datom paylo - full text under P7.1.

**Record d68c82 vision/deployment.md, entry 5 (#2741)**, date/heading: The meta-flow identifier everywhere; declarative deployment; clean up; nexuses are the long term

> > If the send command still needs the flow ID, then my change hasn't been done properly. The send command should use the same identifier that we're using now, which is the 3-field identifier of a metaflow. I want the whole system to use that everywhere.
> >
> > Essentially the flow ID is registered as the corresponding current flow ID for a metaflow and is resolved in the runtime. The agent doesn't have to figure any of this stuff out.
> > - Get Mind to fix that right now and deploy through the proper way of deploying, which is how it should be deployed. If it's not, then it should be deployed that way and fixed as well.
> > - Get somebody to audit and make sure everything is deployed declaratively. If not, actually deploy declaratively and get rid of all of this dirty mess of garbage code that doesn't even run, that we're not even using, that isn't deployed properly, or that doesn't have the right version deployed.
> > - Clean up the system. I feel like I'm telling you this and you won't even be able to do it. You'll come up with some reason why there's a blocker, why there's this dependency on this thing that nobody uses. You can try and use your judgment to see that a lot of the code, which is actually frustrating, is not even being used.
> > - I want to move towards using the nexuses everywhere. They're the long-term vision and then we have this short-term mission. Let's go over all of this, this long-term and short-term stuff everywhere.
> > - I want an extensive book on this: what's the short term, what's the long term. Let's put it down in the vision properly and then let's readjust everything, all of the context types below that, to the vision, and all of the code as well.
>
> -- psyche, STT, 2026-10-13.
- **9aaaba vision/flow.md, entry 4 (#354)** - 2026-10-28 — No EDN anywhere; it is all datom - full text under P7.1.
- **36ac89 vision/flow.md, entry 3 (#1559)** - Production moves onto the tested Flow 0.40, run raw beside the old service - full text under P8.2.

### P15.2. Testing build raw, stable store untouched
**Proposed:** A Nexus's configuration is datom files in a data repository; activation sends them to the running Nexus through its meta CLI, in succession, so the deployment holds no configured value and reads no other notation; the configuration input is the context repository that holds the file. A testing build runs raw against a testing store and never the stable one; the declarative deployment carries the proven revision.
- **0595fb vision/flow.md, entry 3 (#992)** - 2026-10-23 — ruling 84: a testing binary never opens the stable store - full text under P8.2.
- **36ac89 vision/flow.md, entry 1 (#1557)** - Several Flow Nexuses at once; a new one tried raw before it is deployed - full text under P8.2.
- **36ac89 vision/flow.md, entry 3 (#1559)** - Production moves onto the tested Flow 0.40, run raw beside the old service - full text under P8.2.
- **e3c8c1 vision/flow.md, entry 5 (#600)** - 2026-10-23, living, direct, to Psyche core Primary e3c8c1 - full text under P8.2.

### R1. Removed: one model, not always a language model; synthetic intelligence
**Removed line (shown in red):** A flow runs one model, linear and very limited, and the model is not always a language model: it may be a System 1 model, an audio model or a video model. An agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.
**Finding:** CONTRADICTS the Comment of proposal 1, which says the synthetic-intelligence sentence "has no record". Records exist; 2913 says a flow-and-synthetic-intelligence line "landed with the misnomer clause removed".

**Record e06e4c07 vision/archive-flowsNotAgents.md, entry 1 (#558)**, date/heading: 2026-08-19 — an agent is a whole being; a flow is one linear LLM chat; artificial intelligence is a misnomer — synthetic intelligence

> Design session `e06e4c07`, dictated (captured 2026-08-19T13:49+02:00),
> closing the message that kept the name flow for the flow Nexus:
>
> > It's not an agent because to me, an agent is more of a whole being,
> > and a whole being is a lot more than a single LLM chat, which is
> > linear and very limited. Whereas an entity, an artificial entity,
> > which I think the word artificial intelligence is a misnomer. It's a
> > synthetic intelligence. It's synthesized from human knowledge and
> > mathematical probability. So a flow more accurately describes
> > essentially an AI flow, right? Which is just one of the many flows
> > that together, when properly structured and orchestrated, will
> > resemble an artificial being or a synthetic intelligence.

**Record d68c82 vision/archive-flow.md, entry 13 (#2913)**, date/heading: 2026-10-14 — a flow and synthetic intelligence (landed with the misnomer clause removed)

> > Take out the part about artificial intelligence being a misnomer. That's not necessary.
> > Otherwise it's good. Land it.
>
> -- psyche, STT, book comment on «Flow philosophy and artifacts» P1.

**Record d68c82 vision/archive-flow.md, entry 28 (#2928)**, date/heading: A flow's model need not be an LLM

> Context: comment on the current line "A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that."
>
> > It could be a system one also. It doesn't have to be an LLM so that's not necessarily true. Also it could be an audio or a video model or whatever.
>
> -- psyche, book comment, 2026-10-19T17:28, input mode not shown.

### R2. Removed: the simplified flow; long-term Primary as simplified flow
**Removed line (shown in red):** A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.
**Finding:** CONTRADICTS the Comment of proposal 3 ("no record supports ... the simplified flow, the Primary as a simplified flow"). Records exist: 2904, 2930, 2932 (d68c82 archive-flow) and 1563 (36ac89, 2026-10-25, simplified flows have no use yet).

**Record d68c82 vision/archive-flow.md, entry 30 (#2930)**, date/heading: A simplified flow

> Context: comment on the lean flow paragraph.
>
> > I think we could call it, instead of a lean flow, a simplified flow.
>
> -- psyche, book comment, 2026-10-19T17:47, input mode not shown.

**Record d68c82 vision/archive-flow.md, entry 32 (#2932)**, date/heading: The simplified flow has no regular tool

> Context: comment on «Flow's vision», 2nd ed., proposal 4.
>
> > Good. You could even say that it doesn't have any regular tool. Which makes it even leaner.
>
> -- psyche, book comment, 2026-10-19T18:15, input mode not shown.

**Record d68c82 vision/archive-flow.md, entry 4 (#2904)**, date/heading: The Primary becomes a simplified flow

> Context: comment on proposal 12, no Primary without its Secondary.
>
> > Yes this is good, especially since we eventually want primary to be a simplified flow so that it's only used for guiding the design or posing questions, things like that. Essentially rendering a judgment
>
> -- psyche, book comment, 2026-10-19T18:20, input mode not shown.

**Record 36ac89 vision/flow.md, entry 7 (#1563)**, date/heading: Simplified flows have no use yet

> 2026-10-26, to Psyche core Secondary 36ac89. Context: the Psyche core Primary had been declared Simplified with an empty explicit tool list, so it launched with no tools.
>
> > We don't have a use for simplified flows yet because we don't have the hook infrastructure to really use them.

## Everything done on Flow so far

Dates are the first-commit date of the book file in the primary repo (git); many books were bulk-added to git on 2026-10-10, so for those I give the date in the title chain or the flow's own work date where known, marked ~. Status: **landed** = a psyche-context commit message names it (list below); **superseded** = a later edition or the book named in its text replaces it; **open** = no landing found and not superseded; **unknown** = I could not establish it. Status was read from commit messages and book headers, not from the living's rulings book by book.

### Books (path under flows/)

| Date | Path | Title | Status |
|---|---|---|---|
| 2026-10-02 | 91ea9f/books/flow-in-ethos | Flow in ethos | superseded (by 875960 9-flow-anatomy and the ethos books) |
| 2026-10-03 | edf227/books/flow.md (also flow-2, flow-3, flow-as-now-designed) | Flow (first Flow book: "What Flow does": launches a seat, hooks, successor) | superseded (many editions; the Flow module landed through later books) |
| 2026-10-03 | 5578cc/books/how-flow-builds-a-prompt.md, answers-on-flow-launch.md, flow-ids-in-words*.md, answers-flow-ids.md | Flow launch and ids in words | superseded |
| 2026-10-03 | 9fb0ad/books/two-meanings-for-flow.md, two-more-meanings-for-flow.md | Two meanings for Flow | superseded (flow = session, in later vision) |
| 2026-10-03 | 5ed94b/books/02-flow*.md | Flow (corpus pass) | superseded |
| 2026-10-04 | bad807/books/3-nexus.md, 3-nexus-v2.md, 12-metaflow-roles.md, 16-metaflows.md | The Nexus; Metaflows | superseded |
| 2026-10-05 | f768df/books/flow-spawning.md | Flow spawning | superseded (metaflow made central, 2026-10-06) |
| 2026-10-06 to 07 | e5a0bc/books/1-flow-and-message.md, 8-flow-and-message-second-edition.md | Flow and Message | superseded |
| 2026-10-07 | f5a6e9/books/2,3-flow-and-the-metaflow, 6,8-the-metaflow-record, 9-metaflow-kinds, 10-flow-a-passable-vision | Flow and the metaflow; passable vision | superseded |
| 2026-10-07/08 | d4ae97/books/6-flow-as-it-runs-today, 11-the-fixed-metaflow-record | Flow as it runs today | superseded |
| 2026-10-08/09 | f5a6e9/books/11-the-queue-and-the-waking-rule, 12-the-metaflows-ethos, 13/16/17-the-flow-nexus-vision (3 editions), 18-the-nexus-starts | The Flow Nexus vision | superseded |
| 2026-10-09 | 0c85a3/books/word-flow-id-anatomy*.md | Word ids for flows | superseded (word form deferred) |
| 2026-10-10 | 445410/books/4-the-new-flows-as-they-run.md | The new flows, as they run | superseded |
| 2026-10-12 | 875960/books/9-flow-anatomy.md | Flow, whole, in ethos (third edition per its comments) | superseded |
| 2026-10-13 | 563761/books/05-metaflow.md, 06-refresh-handover.md; d68c82 r-metaflow, r-refresh-handover | Flow: the metaflow; refresh and handover | superseded |
| 2026-10-13/14 | df159a/books/12-flow-cli-deployment-long-term(-2); 55a2b4 ...-3; d68c82 r-flow-cli-deployment (4th) | Flow: CLI, deployment, long term | superseded |
| 2026-10-14 | 33752b/books/41-flow-short-long.md, 43-flow-short-long-2.md; 0c9a77/books/02-flow-short-long-3.md | Flow: short term and long term, 1st to 3rd | 3rd landed (2d9fbb6, 2026-10-19) |
| 2026-10-14 to 15 | d68c82/books/16-subflows, 17-subflows-kind, 91-subflows, r-subflows-kind | Subflows | landed (168d72c, 2026-10-19, book 91) |
| 2026-10-16 to 19 | d68c82/books/50-lean-flows, 85-lean-flow, 48/55/62/63 illustrator-refresh | Lean flows; Refreshing the Illustrator | superseded / unknown |
| 2026-10-19 | d68c82/books/53-flow-design, 80-flow-vision, 89-flow-vision-2, 90-flow-ethos, 94-flow-ethos-spec, 95-flow-ethos-2 | Flow's vision (1st, 2nd), Flow ethos | 89 landed (6c8e266, 2026-10-19: vision/flow, vision/ethos, vision/nexus) |
| 2026-10-19 | d68c82/books/54-heartbeat.md | The heartbeat | landed (46c7192, 2026-10-24, "Land the heartbeat vision", approved) |
| 2026-10-19 | d68c82/books/60-flow-in-production, 65-switching-to-flow, 68-flow-as-it-runs | Flow in production | reports; no landing |
| 2026-10-19 | da2038/books/5-flow-sleeping-and-waking-seats.md | Flow: sleeping and waking seats | landed (d2dfc80, 2026-10-18 proposals 1, 2, 5) |
| 2026-10-19 | da2038/books/6-metaflow-roles, 7-how-flow-is-used, 8-flow-vision-and-production | Metaflow roles; Flow vision and production | superseded / unknown |
| 2026-10-19 | 55a2b4/books/15-flow-nexus-whole.md; d68c82 r-flow-nexus-whole.md (2nd) | The Flow Nexus, whole: long term, then short term | superseded by Flow, whole (this one) |
| 2026-10-19 | 379e7a/books/flow-decisions-2, flow-vision-3, nexus-questions; 82867c flow-vision-4; ca28a4 flow-the-decisions; 9864c0 flow-up-decisions | Flow's vision 3rd and 4th; The Nexus: questions for the living | nexus-questions landed (51731e8, 2026-10-20); the rest superseded |
| 2026-10-19 | 288af9/books/08-main-flow-roles; 39bd0c 04-flow-the-design; aa034f flow-startup-cost, flow-tests; c5f24b 10-messaging-between-flows | Main-flow roles; Flow, the design; startup cost | superseded / unknown |
| 2026-10-20 to 21 | 5ec12c, c068b8, 44d6f6 flows-and-messages 1 to 5, the-living-and-the-flow | Flows and messages | 2nd and 3rd landed (7f71675, 847a455); 5 on 004b4b and 44d6f6 as html/md: open/unknown |
| 2026-10-22 | 87c40b/books/flow-from-basic-principles.md (html copy: 004b4b/books/flow-from-basic-principles.html) | Flow, from basic principles | open/unknown (no landing found) |
| 2026-10-22 | 38d4c1/books/simplified-flows-first(-2,-3) | Simplified flows first | unknown |
| 2026-10-23 | 0595fb, 5330c1, a447ee books/flow-next-iteration.md (+ a447ee flow-next-vision.md, flow-stable-build.md) | Flow 0.39 against the vision: the next iteration | superseded by flow-tonight and the 0.40 rebuild |
| 2026-10-23 | 5330c1/books/flow-tonight.md | Flow tonight: the testing capsule, the pulse, the hooks | landed (5b7b165, 2026-10-23, proposals 1 and 2) |
| 2026-10-23 | 8db64f, 9a83ec crystallize-intent-main-flow; 9a83ec crystallize-vision-flow | Crystallizing intent:main-flow | landed (3d2349c, 3835626, 2026-10-23) |
| 2026-10-23 | 956dc2 flow-knowledge, flow-ordinary-queries; fa3c6f testing-capsule; d50d70 flow-next; cd1923 flow-next-continuity-policy | Flow knowledge, queries, testing capsule | unknown |
| 2026-10-24/25 | ce46fb/books/flow-sanity; 63a06a flow-design (Flow: the design, and Flow 0.40, 2nd), flow-inband-control; 493e29 why-flows-fail | Flow sanity; Flow 0.40 design | design superseded by bea8f8; no landing found |
| 2026-10-26 | 63aef7/books/flow-by-configuration.md; c637a5 flow-by-configuration-design | Flow by configuration | open/unknown (comments by the living on it: 2d9f4d, 2026-10-26/27) |
| 2026-10-27 | bea8f8/books/flow-design.md, message-nexus.md; c637a5 flow-batch-1-audited, flow-overnight-choices | Flow, the design with its code | unknown; fed Flow, whole |
| 2026-10-28 | 7b6597/books/flow-five.md (and html) | Five Flow proposals | superseded by Flow, whole (reference file) |
| 2026-10-28 | 72b114/books/what-is-open-is-remembered.md; 9aaaba/books/queue.md | What is open is remembered; The queue | unknown (see Everything open 34 to 40, flows/73b5d8/books/open-proposals.md) |
| 2026-10-29 | 554e1a/books/flow.md | Flow (split from Everything open; says it is superseded by Flow, whole) | superseded |
| 2026-10-29 | 554e1a/books/flow-composition.md; b2b87a/books/flow-composition.md | Modules by role and function | 554e1a copy superseded by the b2b87a one; open (a belief-module proposal) |
| 2026-10-29 | 554e1a/books/horizons.md (2nd edition); b2b87a/books/horizons.md (3rd edition) | Vision by horizon | 554e1a superseded by b2b87a; b2b87a ruled landable by the living without review (its header) |
| 2026-10-29 | 554e1a/books/three-nexuses.md | Three nexuses | open |
| 2026-10-29 | 30fc30/books/flow-whole.md | Flow, whole (this proposal) | open |

Also not listed above: about 200 books in flows/*/books bear Flow-related names; the table lists the Flow-design chain, not every illustration or report. The full file list is reproducible with `ls -d flows/*/books/* | grep -iE '/[^/]*(flow|nexus|queue|capsule|herdr|heartbeat|refresh|remember)[^/]*$'`.

### Landing commits touching vision/flow.md in repos/psyche-context

`git -C repos/psyche-context log --oneline -- vision/flow.md`, with dates:

- c984eeb 2026-10-29 vision/model-roles, intent/main-flow, vision/messaging, vision/blocking, vision/collaboration, vision/flow, spirit/core: what he wanted
- 6c1763f 2026-10-28 vision-flow: ghost hunt, the thing as wanted
- 576e70c 2026-10-28 figures: ASCII sketches converted to Mermaid flowcharts (order of the living 2026-10-25, bead primary-9v4)
- 85b9f1e 2026-10-28 Replace "psyche" with "living" where it means the living person
- eff8100 2026-10-25 Rename context module to belief module
- 9e03cd0 2026-10-25 vision-flow: restarting without waking
- af97799 2026-10-25 vision-flow: remove a restart does not wake, which misstated the living
- f94d063 2026-10-25 vision-flow: a restart does not wake; what a refresh carries
- 46c7192 2026-10-24 Land the heartbeat vision and compensation-messaging (approved)
- 5b7b165 2026-10-23 Land Flow tonight proposals 1 and 2 (approved): Herdr one backend of the Capsule; a real-world test of Flow
- 3835626 2026-10-23 Land the TJEgPW figure beside its approved line in vision:flow
- 3d2349c 2026-10-23 Land intent:main-flow book TJEgPW proposal 1: the first prompt carries the recent raw psyche (approved)
- 4fc4c7e 2026-10-23 Land repetition removals (approved)
- 7427210 2026-10-22 Land: a permission prompt reaching the living is a launch failure
- 847a455 2026-10-21 Land approved lines from Flows and messages, 3rd edition
- 7f71675 2026-10-21 Land approved lines from Flows and messages, 2nd edition
- 51731e8 2026-10-20 Land Nexus questions: Message is the send path; Flow configuration holds purpose and records; topic name kept as written (short term)
- 2d9fbb6 2026-10-19 Land flow vision book 3: one-call start, presentation, refresh by model threshold, compaction at continuous work, subflows wording
- 6c8e266 2026-10-19 Land flow vision book 89: vision/flow, vision/ethos, vision/nexus
- 168d72c 2026-10-19 Land subflows book 91: remove the three subflow sections from vision/flow, add vision/subflows
- a83cbd0 2026-10-19 Edit flow vision: drop two sentences, name a flow a run of a metaflow
- d2dfc80 2026-10-18 Land «Flow: sleeping and waking seats» proposals 1, 2 and 5 in vision/flow.md
- dde8584 2026-10-17 Flow vision: title as datom struct, six-character flow id, drop ancestor-naming sentence
- d5fb9c1 2026-10-17 Land ruled lines of «Today, as psyche, 2nd edition»
- 53f68b6 2026-10-16 Move every psyche module into its type folder

Other Flow-bearing landings in the same repo (not on vision/flow.md): f9f3242 (2026-10-29, vision/remembering, a fresh flow remembers from the logs alone), 39a66bb (2026-10-26, no summary, no handover), ae51e96 (2026-10-27), 632e2d0 (2026-10-28, remembering includes open beads), 09ce727 (2026-10-28, the fallback changes the carrier), 5f604c2 and 3199f00 (2026-10-28 ghost hunts), cbbf0f4 (latest touch of vision/flow-ethos.md or vision/nix-builds.md).

Note: the 2026-10-29 commit c984eeb ("what he wanted") and 6c1763f ("vision-flow: ghost hunt, the thing as wanted") are the most recent shapes of the module this proposal replaces.
