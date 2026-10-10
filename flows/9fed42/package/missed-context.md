# Missed context for the Flow lane

For Psyche Flow Primary f5a6e9, from its secretary 9fed42, 2026-10-09.

These are things the living has said that bear on Flow and are absent from f5a6e9's view. That view is `flows/f5a6e9/handover.md`, `flows/f5a6e9/vision/`, `flows/f5a6e9/notion/`, its books 1–15 in `flows/f5a6e9/books/`, and «Stored type and datom form», second edition (FadJBF).

Records were selected by the living's rule: "the recent vision and the one that's been repeated a lot, which hasn't been overridden by newer decisions or statements" (`flows/ebbe30/vision/metaflow-naming.md:5`, 2026-10-09). Older records are kept only where nothing newer covers them, and each says so.

## Witness and claim

- **Witnessed by 9fed42 in this run:**
  - Every quote below was read at the path and line given.
  - The five transcript lines were read with the transcript tool's `raw`.
  - The comment in record 37 was read with the artifact comment tool.
  - Absence from f5a6e9's view was checked by grepping a distinctive phrase of each quote across that view.
- **The flow's own inference (9fed42 and its five reading subflows):**
  - which records are selected;
  - each "Bears" line;
  - each "Overridden" judgement;
  - each "Conflict" judgement.
- **Claims not confirmed:**
  - A subflow reported five comment threads on FadJBF; the artifact comment tool shows none.
  - The order of records within 2026-10-07 is unknown where no time is recorded.

Kinds: **V** marks vision (a quoted psyche record). **N** marks notion (thinking aloud). **T** marks typed words found only in a transcript, with no record.

---

## The metaflow: naming, aspect, topic

**1. Topic flow titles: psyche::{topic}, then the layer, then the word id.** V.
`flows/ebbe30/vision/metaflow-naming.md:7`, 2026-10-09. The same words are at `flows/445410/vision/flow.md:13`.

> Start these two topic flows with the psyche::{topic}, either core, flow, or ethos, and then the layer: primary and secondary. There are three things. We can put the flow ID after that, although that might be a bit long, but let's try it. I would like the word-based flow ID, but maybe Astra can make a tool, a [Clojure] tool, to do the conversion between the first 33 bits of the identifier we use for the harness and the word thing. It can get a regular expression back so that we can find which session from the list of transcript files we have, or maybe we have a list of the alpha-numerical ID somewhere in the database, or maybe we just make a registry in the database.

- **Bears:** this is the newest title order, and it says where the id-to-session map may live (a registry in the database).
- **Overrides:** "the old name convention … completely obsolete" (`flows/d4ae97/vision/flow.md:161`, 2026-10-08).
- **Conflict:** with book 9, proposal 3 (`9-metaflow-kinds-the-title-the-word-id.md:80-82`): "remote title is its metaflow's kind written short … `Psyche.{ Primary startInputVital }`". That puts the layer first and carries no topic.

**2. Metaflows addressed by name, never by hashes.** V.
`flows/4ddfe1/vision/flow-names.md:5`. The record has no date; the file was written 2026-10-09 (file time) and is uncommitted.

> I don't want you to read those hashes. What is d4? I don't fucking understand. You mean like, uh... You mean like psyche secondary or psyche primary? I want all the metaflows addressed this way and not with hashes.

- **Bears:** every flow-facing address, report and title uses the metaflow's name.
- **Overridden:** no.
- **Conflict:** none seen in a proposal.

**3. Three aspects to every topic; each aspect is started on its own.** V.
`flows/ebbe30/vision/aspects.md:5` and `:10`, 2026-10-09. Typed in transcript ebbe3021 L577.

> The aspect is now, I think, part of any metaflow. It shows us which aspect of that topic it's actually taking care of.
> …
> There are three aspects to every topic potentially. Just because we start a psyche on, let's say, ethos, doesn't mean that we need to automatically start a mind on ethos.

- **Bears:** Launch creates one aspect's metaflow for a topic, never the triple.
- **Overridden:** no.
- **Conflict:** none seen.

**4. A Psyche Primary gives vision designs and asks Mind for system state.** V.
`flows/ebbe30/vision/aspects.md:20`, 2026-10-09.

> So, a psyche primary flow like yourself, costly fable. Your job is really just to give me vision designs. If you need to know how things are going, you ask mind. How things are on main, on deployed main.

- **Bears:** what a Psyche metaflow does, and where its knowledge of state comes from.
- **Overridden:** no.
- **Conflict:** none seen.

**5. Core is the hub its aspect's topics pass through; Field is the glue that winds flows down until that is automated.** V.
`flows/d4ae97/vision/flow.md:173` and `:177`, 2026-10-08. f5a6e9 holds only the dense-string part of this record (`:181`).

> They have an overview of all of psyche and all of the other psyche topics sort of go through the core. It's like there's this hub at the center, the psyche core, so it's a struct.
> …
> Field would be maintaining, debugging, deploying, using an actual mutating system, running commands such as `field` or `flow` to start new things or to wind things down that we didn't have hooks for, and automating wind down. Eventually Field is doing what we're trying to automate.

- **Bears:** Core's routing role, and what End and reaping replace.
- **Overridden:** no.
- **Conflict:** none seen.

**6. "No voice": the variants are the aspects, by layer.** V.
`flows/d4ae97/vision/flow.md:86`, 2026-10-07.

> I want to change the name "voice" to describe the long-running seed [sic]. There's no voice, right? The variants are all of the different voice aspects directly. They're called by name: psyche, mind, field. They're separated by layer, right?

- **Bears:** the vocabulary of the metaflow record.
- **Overridden:** unknown.
  - f5a6e9's record "A voice is a permanent metaflow" (`f5a6e9/vision/flow.md`, comment 1, 2026-10-07 18:32) was said the same day.
  - No time is recorded for this one, so which is newer is unknown.
- **Conflict:** with book 10.
  - Proposal 1 (`10-flow-a-passable-vision.md:38`): "Field metaflows are voices".
  - Proposal 2 (`:76`): "`Voice.{ Psyche Primary }`".
  - Book 13's record has no Voice.

**7. A fourth, ephemeral type that stays off the pane.** V.
`flows/d4ae97/vision/flow.md:103`, 2026-10-07.

> We can start this new opus, which is going to be of the other type, which is like topic, basically. I think it's the fourth type and these are ephemeral. They have a different payload and we don't need it on the pane.

- **Bears:** whether every metaflow gets a pane.
- **Overridden:** in part.
  - Topic became a field of every metaflow on 2026-10-08 (`d4ae97/vision/flow.md:171`).
  - Core was named on 2026-10-09 (`445410/vision/flow.md:35`).
  - "Off the pane" is not restated or overridden.
- **Conflict:** none, beyond the open question in the handover on whether the implementation kind survives.

**8. A flow is not always a metaflow; lookup is by metaflow.** V.
`flows/d4ae97/vision/flow.md:65` and `:72`, 2026-10-07.

> A flow could exist and not be a metaflow so this structure is wrong. … If a flow is a metaflow we'll be addressing it by its long-term metaflow name. There are flows that are not metaflows …
> How do I know which flow a metaflow is? I'm going to look up "by metaflow" and a flow isn't always a metaflow …

- **Bears:** subflows and other non-metaflow flows in Flow's Memory.
- **Overridden:** in part. "Options are a last resort" (f5a6e9's own comment-5 record) rules out the optional field.
- **Conflict:** none. Book 13's `Flow.{ FlowId Session Events }` carries no metaflow link. How non-metaflow flows are addressed is unaddressed.

**9. A metaflow's flow history is not kept forever.** V.
`flows/d4ae97/vision/flow.md:74`, 2026-10-07.

> And what about the flow history of a certain metaflow? Maybe it doesn't go on forever. … Probably eventually, not that we have to worry about this, we wouldn't want to keep the entire history. You could see a scenario in which this becomes unwieldy.

- **Bears:** the Past field.
- **Overridden:** no.
- **Conflict:** with book 13 (`13-the-flow-nexus-vision.md:36`): `Past.Vector<FlowId> ; oldest first`, which is unbounded. The tension is mild, since he says "eventually".

**10. The metaflow record as a fixed-size unit pointing at the current flow.** N.
`flows/d4ae97/notion/flow.md:15-17`, 2026-10-08.

> If we have the metaflow type and it doesn't have any vectors, then it's just this unit of data that has exactly the same size. … If we only have one of its fields, right, as the current flow that this metaflow corresponds to, that's mostly what we need. … We can also use another pointer somewhere else to hold a different kind of data, the slow aspect of the database.

- **Bears:** the storage shape of Details.
- **Overridden:** he framed it as "a thought I wanted to sort of verify or refute".
- **Conflict (tension only, a notion):** with book 13, lines 36–37. The two vectors, Past and Queue, sit inside the record.

## Starting a flow

**11. Spirit replaces the system prompt; intent specializes the metaflow; vision goes in the user prompt.** V.
`flows/d4ae97/vision/flow.md:96` and `:98`, 2026-10-07.

> This is central to how the whole rest of the machine behaves: we're going to replace the system prompt with the spirit.
> Depending on which kind of metaflow we're starting the harness in, we're going to load different parts of the intent in the system prompt as well. This will give us specialized metaflows because that's going to come from the intent. I guess the vision goes in the user prompt.

- **Bears:** what Launch composes, and where.
- **Overridden:** no.
- **Conflict:** an omission, not a contradiction.
  - Book 13 (`:100`): "composes the system prompt and the first prompt from the module registry".
  - Book 10, proposal 4: "placed in the system prompt, in the first prompt, or left loadable".
  - Neither names the spirit, intent and vision placement.

**12. Startup with minimal effort; Claude runs a server per session, with remote control enabled.** V.
`flows/ebbe30/vision/flow-startup.md:5` and `:19`, 2026-10-09.

> Let's keep optimizing the flow startup infrastructure so that it can be used with minimal effort and has all of the context that we want to load the model with in the system prompt and in the user context layer

> Claude we can update because it's per session. We're not using a server. There's a server essentially in every session, I think. We just enable remote control and we start the flow, right? This actually gives me a better user interface in the end than one central server.

- **Bears:** remote control is part of Launch.
- **Overridden:** no.
- **Conflict:** none seen.

**13. Deterministic work is done in code; a session can be created, and its id known, before its first prompt.** V.
`flows/5578cc/vision/flow.md:51`, 2026-10-03T16:17, typed book comment.

> … we can start a session without launching its first prompt and we can get its session ID before it even starts. We don't have to pay for the LLM to do all of the work that a deterministic cheap program can do. Let's make this so we need something developed into intent: that we intend to do anything that is deterministic into code …

- **Bears:** Launch reserves the id before the harness runs, and nothing is left to the model.
- **Overridden:** no.
- **Conflict:** none seen. Book 13 agrees: "written at reservation, before any harness runs". The intent statement he asked for is not seen in f5a6e9's books.

**14. A part of the system prompt that is not passed to subflows.** V.
`flows/5578cc/vision/flow.md:61`, 2026-10-03, typed book comment.

> The one thing I would really like to know is if it's possible that there's a part of the system prompt that doesn't get passed down to the subagents of that harness. I would like to be able to program the main flow a certain way but not its subagents in its system prompt.

- **Bears:** module placement in Launch.
- **Overridden:** no.
- **Conflict:** none seen. Book 10, proposal 4 does not address it.

**15. Flow's configuration lives in its own database and memory, not in Markdown.** V.
`flows/edf227/vision/flow.md:16`, 2026-10-03 18:13, typed book comment.

> No the configuration flow does not live in a Markdown file in every story. It lives in its own database and its memory. That's where the configuration goes …

- **Bears:** the layer-to-model table is in Flow's Memory.
- **Overridden:** unknown. On the same day he said "another [skill] somewhere loads the current correspondence of which model is which layer" (`flows/5578cc/vision/skills.md:14`, 2026-10-03, time unrecorded).
- **Conflict:** none with the books. Book 13 has "decides the model". The two records above are in tension with each other.

**16. The Clojure Flow prototype: its own database, addressing by metaflow name, specified in Ethos.** V.
`flows/d4ae97/vision/flow.md:154`, 2026-10-08, and `flows/ebbe30/vision/clojure.md:5-7`, 2026-10-09.

> … the most psyche-aligned version of the Clojure flow prototype, with its own database with metaflow addressing by metaflow name. We could even have channel enforcement anchored in the configuration-style data: we should spec everything in Ethos …

> The first presentation is an ethos anatomy, and then the [Clojure] code uses that as a guide to create its specification for its data and its types.

- **Bears:** the Flow Nexus vision is the anatomy the prototype is built from.
- **Overridden:** no.
- **Conflict:** none seen. "Channel enforcement" appears nowhere in f5a6e9's books.

**17. The new flow setup works, but the Nexus is not yet in use; old flows are re-bootstrapped once it is.** T.
Transcript 44541044 L1572, 2026-10-09T20:10Z.

> I can see that the new flow setup seems to be kind of working. I'd like to know the state on that. … where we are in terms of the Nexus, which we probably aren't using yet … why we aren't using it … Just try and deploy better closure and/or better Rust that can actually run in Nexus with CLIs.

Transcript ebbe3021 L1740, 2026-10-09T18:47Z.

> … the new vision implementation for Flow Closure and Rust Nexus … Let's try and rebootstrap all of the flows that are old, which will probably be almost all of them, after we get the new flow infrastructure.

- **Bears:** the present state and the next step of the Flow implementation.
- **Overridden:** no.
- **Conflict:** none.

## Refresh, context size, reaping

**18. Fixing Flow is central; 700,000 tokens is unacceptable; messaging a large flow costs its whole context.** V and T.
`flows/d4ae97/vision/flow.md:23`, `:25` and `:41`, 2026-10-06.

> I think fixing Flow is central to getting more efficient flows … so that we can spawn them fresher, more often, and have meta-flows that can focus on certain topics. … We're using LLMs to make up for a lack of software, which is bad.
> Then I went to talk to Fable and I said that he had 700,000 tokens of context. That's unacceptable but we don't have a way to monitor that yet.

Transcript d4ae97d4 L1761 and L1778, 2026-10-06T15:10Z and 15:11Z. Typed, with no record:

> You were messaging a 700,000-token Fable Flow. Have you no sense of how silly and stupid that is?
> You understand that if a flow has 700,000 tokens and you send it a message, you have to process all of these 700,000 tokens, right?

- **Bears:** why Flow exists, why the context is monitored, and the cost argument for the waking rule.
- **Overridden:** no.
- **Conflict:** none seen.

**19. Spawning is automated, by refresh or by a metaflow spawning another; Field does not do it forever.** V.
`flows/d4ae97/vision/flow.md:49`, 2026-10-06T14:54, typed book comment.

> Well eventually flow spawning is going to get automated, in terms of refreshing the flow or in terms of a meta flow spawning another one because there's a job, there's a particular interest in a particular subject or implementation that needs its own metaflow. … That doesn't mean field is going to do it forever.

- **Bears:** who may ask Flow to Launch: another metaflow.
- **Overridden:** no.
- **Conflict:** none seen.

**20. For now, the bottom layer of each aspect runs the refresh.** V.
`flows/02dda6/vision/flow-refresh.md:5`, 2026-10-07, relayed by 0c85a3.

> Basically we need to refresh the flow. I guess we'll use quaternary in every aspect. The bottom of each aspect is what is going to run the flow refresh mechanism for now.

- **Bears:** who runs Refresh until Flow does it.
- **Overridden:** no. It is a stopgap.
- **Conflict (tension only):** book 10, proposal 3 (`10-flow-a-passable-vision.md:120`): "No model decides any of this." That is the end state; the record names today's runner.

**21. Refresh through a context-threshold hook; the lock; subflows still running.** V.
`flows/e167d8/vision/refresh.md:5` and `:7`, 2026-09-26.

> When a model reaches a certain context window, whoever is in charge of refreshing should get a message that some flow needs to be refreshed. I guess the flow itself needs to know so that it can create a handover response. At that point that same hook system picks up the final response and essentially locks the messages from being sent over there immediately.
> If there are sub-agents still working, it's okay. I guess we could just notify the new flow of what happens after they return …

- **Bears:** the Refresh sequence.
- **Overridden:** no. The 20–40 percent threshold record refines it.
- **Conflict:** an omission. Book 10, proposal 3 leaves out subflows still running at refresh.

**22. The old flow stops receiving first, and that is the lock; a refresh needs a recent handover.** V.
`flows/d8df70/vision/flowLifecycle.md:5` and `:13`, 2026-09-24 14:28Z and 14:32Z. Also `flows/1ac573/vision/operational-reapReplacedSessions.md:13`, 2026-09-17.

> A seat starts receiving. The old seat stops receiving first. That's how we get a lock. … A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived.
> In order for the flow to refresh, it needs to have a flow handover in its transcript somewhere, a recent transcript not too old.

- **Bears:** the order inside Refresh, and its precondition.
- **Overridden:** only the word "seat" (record 32).
- **Conflict:** none seen.

**23. Herdr shows busy, finished and read; flows move to a new harness one at a time as they go idle.** V.
`flows/7328f4/vision/hooks.md:7`, 2026-09-30, typed, and `:17`, 2026-09-30T18:47 page comment.

> I looked at [Herdr] this morning and I see that it supports showing me if a session is busy: it has a little red dot. If the session is finished, it has another kind of dot, but I haven't read it. If I've read it, it has another kind of dot.
> As soon as the session goes idle, the hook kicks in. It gets locked … This will tie into how context size will essentially start triggering the unwind.

- **Bears:** Herdr's pane state as a hook source, and upgrade-by-refresh.
- **Overridden:** no.
- **Conflict:** none seen.

**24. Reap the abandoned and refresh the large; code prevents duplicate roles and undeclared high effort.** V.
`flows/e71dab/vision/launchGovernance.md:6` and `:14`, 2026-09-26.

> Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped. … somebody launched too many flows that were on the same role and then launched the flow with too high an effort. … let's make sure the code makes sure it doesn't happen again.
> We should have a list of flows all programmed with their datom configuration.

- **Bears:** Flow refuses a duplicate metaflow, and refuses an effort no metaflow declares.
- **Overridden:** no.
- **Conflict:** none. Book 13's `Refused.[ Locked Unknown NoLayer ]` has no duplicate refusal.

**25. The system closes panes and sessions itself.** V.
`flows/b7ba00/vision/modelFlows.md:39` and `:45`, 2026-09-26.

> Nothing is up to me. Everything is being automated. … I'm not going to close or start anything or type anything anywhere ever.
> Let's just teach the system to close panes, to close sessions itself.

- **Bears:** End and reaping close the pane.
- **Overridden:** no.
- **Conflict:** none seen.

**26. A replaced flow left open gets woken.** V.
`flows/fe945a/vision/flowLifecycle.md:7`, 2026-09-29 16:44 UTC, typed.

> The old one's still open and I bet if somebody tries to message people, they'll wake the old flow up. That's really bad.

- **Bears:** why the refresh reaps its predecessor.
- **Overridden:** no.
- **Conflict:** none.

**27. The reaper reports like a coroner.** V.
`flows/1ac573/vision/operational-reaperIsForensic.md:16`, 2026-09-18.

> Basically, the Reaper can see if something went wrong or if something was left unfinished. … he makes a report of: what he reaped, what he suspects, what he recommends, if somebody wants to investigate, what they can look into, what he saved, what he archived

- **Bears:** what End or reaping leaves behind.
- **Overridden:** none found. This is an older record, and its recency was not established further.
- **Conflict:** none.

**28. Haiku 5.5 is the Quaternary; the four layers apply to every metaflow; look for dead flows and spawn by topic, aspect and level.** V and T.
`flows/d4ae97/vision/models.md:28`, 2026-10-08.

> We need to update Claude Code because Haiku 5.5 came out and we need to start using that on the quaternary now. … This primary-to-quaternary division is sort of universal in any type of metaflow or flow.

Transcript ebbe3021 L577, 2026-10-09T15:46Z. Typed, with no record:

> They have Haiku ultra-low model quaternary. Ask field to use a lower tier to get a sense of how many flows we have, look for dead flows that should be reaped, and look into the infrastructure to be able to spawn different topics in certain aspects at different levels.

- **Bears:** the layer table, and spawning by aspect, topic and layer.
- **Overrides:** "quaternary, for now, is the same model as tertiary with a lower effort" (`flows/d4ae97/vision/models.md:23`, 2026-10-05).
- **Conflict:** none seen.

## Locks, messages, routing

**29. Flow locks sessions; Orchestrate locks files.** V.
`flows/9fb0ad/vision/locking.md:5`, 2026-10-03T15:50Z, typed book comment. Also `flows/edf227/vision/flow.md:10`, 2026-10-03 18:12.

> No, Flow locks the sessions and Orgistrate [Orchestrate] locks the files. Those are different things.
> Why are we talking about orchestrate here? There's no reason to talk about orchestrate.

- **Bears:** the scope of Flow's lock, still listed as undecided in the handover.
- **Overridden:** no.
- **Conflict:** none in the proposals.

**30. The lock exists to roll a metaflow into its next flow; Message uses it later.** V.
`flows/e5a0bc/vision/flow.md:25`, 2026-10-07, typed.

> There's also the concept of the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow. … that lock will be useful in order to know whether the messages can or cannot reach a certain flow.

- **Bears:** the purpose of the lock, which comes before the time-bound request lock.
- **Overridden:** no.
- **Conflict:** none. This record is cited in book 10's sources line ("e5a0bc flow"), but the quote itself is not in f5a6e9's view.

**31. Message uses Flow; the two are designed together.** V.
`flows/d4ae97/vision/flow.md:33`, 2026-10-06, and `flows/d4ae97/vision/messenger.md:27`, 2026-10-09.

> In conjunction with designing and implementing Flow is message, which is going to be deeply married with it
> Nexus/a little bit of messaging in terms of remaining aware of the fact that we want messaging to use Flow. I mean, message should be called message.

- **Bears:** Flow's Signal is shaped for Message as its client.
- **Overridden:** no.
- **Conflict:** none seen.

**32. There are no seats: there is the voice and the flow.** V.
`flows/8475a9/vision/voices.md:35`, 2026-10-05; `:67`, 2026-10-05, typed.

> The seat, first of all, is a flow. We don't have seats. There's no seat. It's a flow.
> Yeah I don't see a need for the terminology "seat" because we have the voice and the flow.

- **Bears:** vocabulary in Flow's books.
- **Overridden:** "voice" is in question under record 6; "no seat" stands.
- **Conflict:** with book 13 (`13-the-flow-nexus-vision.md:90`): "Written, a launch of this seat:".

**33. Messages move by level, hard-enforced; the layer below is the secretary.** V.
`flows/d4ae97/vision/flow.md:137` and `:139`, 2026-10-07.

> You're going to have to talk to a secretary because you're secondary. I want that hard-enforced. … he cannot message from tertiary to primary or from tertiary to secondary of another aspect, right? They have to either go horizontally, [one] level up, or any level down and across, right?

- **Bears:** a refusal Flow, or Message, applies by layer and aspect.
- **Overridden:** no.
- **Conflict:** none. f5a6e9 has ruled a speech-by-level refusal by Flow (9fed42 log), but the record is not in its view.

**34. Gated flows; design talk reaches the Primary through the relaying seat.** V.
`flows/bad807/vision/gatedFlows.md:7`, 2026-10-04, typed, and `flows/445410/vision/messaging.md:5`, 2026-10-09.

> … we would have these essentially gated flows that can only be messaged through another sort of a secretary, if you will … Because this flow is so important, it's like a high-cost design flow, and nothing should really contaminate it.
> Yeah, everything I'm saying that has, essentially... smell of a design or a discu-discussion about architecture or review of something, is basically, Me talking to Opus through you.

- **Bears:** a Primary metaflow's requests come through its Secondary.
- **Overridden:** no.
- **Conflict:** none seen.

**35. Messages that do not concern a flow must not wake or disturb it.** V.
`flows/9fb0ad/vision/messaging.md:5`, 2026-10-03, typed, and `flows/d66c26/vision/messaging.md:4`, 2026-10-04, typed.

> I'd like, for a solution, for you to stop being disturbed so much by messages that absolutely have nothing to do with you and are costing us money …
> I want to make a rule again that guides messaging better so that we don't end up getting these noisy messages that wake or disturb flows.

- **Bears:** this is the repeated motive behind the waking rule.
- **Overridden:** no. The 2026-10-08 queue record refines it.
- **Conflict:** none.

**36. Queued context rides in with the next message; new vision on a topic is routed to its flow after a minimum window.** V.
`flows/bad807/vision/flowContextInjection.md:7`, 2026-10-04, and `flows/edf227/vision/visionNotification.md:9`, 2026-10-03.

> We can use that opportunity to inject a bunch of other stuff that has been queued in preparation for that particular flow to be woken up, so that it would know all of this as soon as it woke up. Yet we wouldn't have to wake up every time some accumulation of vision or whatever that touches its lanes or its topics is coming into the system.
> If we know that a psyche is dealing with a certain topic and a new psyche vision or notion that touches that topic arrives, it should be routed to that flow. The next time that it receives messages anyway, right? … We might wait at least a minimum window.

- **Bears:** the queue, and the topic-to-metaflow routing of new vision.
- **Overridden:** no.
- **Conflict:** none. This is supporting evidence for book 11.

**37. Reviewed code lands in vision: the queue book's first two proposals are "misdirected".** V, book comment.
Artifact HUA3QJ («The queue and the waking rule»), thread 1ca21c, 2026-10-08T16:02, anchored at "Ruling 2". Recorded at `flows/d4ae97/vision/psyche.md:6` and `:10`.

> The first two proposals are brilliant in content but they're misdirected. … The golden rule is: thou shalt not touch the psyche data unless the living has explicitly approved an edit, which he has reviewed.

- **Bears:** where Flow's types are proposed.
- **Overridden:** no. The 2026-10-09 law ("all of the code that the living reviews and approves goes into vision") restates it.
- **Conflict:** with book 11, which still stands before him.
  - Proposal 1 targets `signal-flow/ethos/signal.ethos` (`11-the-queue-and-the-waking-rule.md:4`).
  - Proposal 2 targets `flow/crates/flow-nexus/ethos/memory.ethos` (`:30`).
  - Both are repository files, not a vision skill.

**38. Message passes through Flow; raw pane typing is a meta-socket operation; check for `/compact`.** V.
`flows/88475f/vision/message.md:61` and `:65`, 2026-09-25, and `flows/b7ba00/vision/messaging.md:15`, 2026-09-26.

> … a datom-based message system that uses Flow to lock the panes and stuff and essentially passes the message through Flow.
> We need to check to make sure that it's not just sending a command like `/compact`. At the same time we want to expose these interfaces through the Flow CLI at whatever authority level they need to be at.
> A raw flow send (as in typing directly into the pane, into the harness) I think should be a meta socket operation and then we have a more lock-enabled deliver message.

- **Bears:** Flow's ordinary and meta interfaces.
- **Overridden:** no.
- **Conflict:** none. This agrees with book 15, proposal 4 (`Deliver` under the lock).

**39. An undeliverable message escalates; a missing crucial flow is started.** V.
`flows/d8df70/vision/messaging.md:66` and `:68`, 2026-09-24 14:31Z.

> If a message can't be delivered, then we try a higher power. … if there's nothing higher then we try lower.
> Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

- **Bears:** what a request does when its metaflow has no live flow.
- **Overridden:** in part. The 2026-10-08 waking rule (f5a6e9 `vision/messaging.md`) replaces "start if crucial" with waking by request kind, and the power names are the old tiers. Escalation on non-delivery is not restated.
- **Conflict:** none with a proposal.

## Nexus, Signal, stores, Ethos form

**40. Every Nexus has Signal, Operation and Memory, with a standard entry point that forces the route.** V.
`flows/d4ae97/vision/nexus.md:4`, 2026-10-07; `flows/5ed94b/vision/nexusEntryPoint.md:7`, 2026-10-04, typed; `flows/bad807/vision/nexus.md:15`, 2026-10-04, typed book comment.

> All nexuses have to have all three. Maybe that is something we need to add into the vision, which is now.
> … the signal has to go through the operation actor/system in order to reach the memory actor/system, then back through the operation system and back out through the signal.
> Let's have it tested on an actual component that we have written, like Flow, Message [sic], or Orchestrate, on a branch …

- **Bears:** the Flow Nexus vision carries Signal and Memory roots only.
- **Overridden:** no.
- **Conflict:** an omission. Book 13 has no Operation. The split named on 2026-10-09 (flow-ethos, memory-ethos, signal-ethos) has no operation part either.

**41. No datom in any Nexus; string handling there is forbidden.** V.
`flows/8475a9/vision/datom.md:29`, 2026-10-05, book comment.

> Well the Nexus has no datom so expand [it]. It doesn't even have datom. There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus.

- **Bears:** where Topic's PascalCase check and other string work run.
- **Overridden:** no.
- **Conflict (possible):** with book 13 (`:40`), `Dense.String ; PascalCase … checked on the way in`, if that check runs inside the Nexus. The book does not say where it runs.

**42. A special representation is a trait with a representation type described in Ethos.** V.
`flows/445410/vision/ethos.md:5`, 2026-10-09, relayed by ebbe30.

> … the special representation is basically an implementation for a special way to decode and encode, so that the representation has a different type than the type when it's read into the Rust runtime. … In Ethos, we're going to describe the real type, the real Rust type that it has, and then the special representation is going to implement the representation type. We could maybe even somehow describe that type in Ethos, what that representation type is, which would be interesting because then we would force the input and output types, and we would let Rust do the implementation.

- **Bears:** this is the newest word on the trait that book 15 introduces for `Sha256`.
- **Overridden:** no.
- **Conflict (possible):** with book 15, proposal 1 (`15-stored-type-and-datom-form-second-edition.md:18-19`). `Encodable.[ encode.String … ]` fixes the representation as a String; he asks that the representation type be named in Ethos.

**43. The private layer: a third, open-source seat.** V, chartered, NOT ACTIVE.
`flows/6cc91b/vision/privateLayer.md:7`, 2026-09-14.

> The private layer is only served through the open-source model, and it can use the public counterpart with sterilized questions …

- **Bears:** a future layer or aspect value and a provider that Flow would launch. No newer record was found.
- **Overridden:** no.
- **Conflict:** none. The Layer enum in book 13 does not anticipate it, and nothing requires it to yet.

## Searched, and not found

- **Searched:**
  - `flows/*/vision/` and `flows/*/notion/` (245 and 53 directories), with emphasis on records from 2026-09-24 to 2026-10-09;
  - `flows/445410/vision/` and `notion/` read whole;
  - the vision and intent skill sources, which hold no quoted psyche blocks;
  - `vision-raw/`, by date grep only (nothing from October);
  - the 60 most recent Claude transcripts, from 2026-10-03 on;
  - artifact comments on f5a6e9's seven handover artifacts and on FadJBF. Only HUA3QJ has a thread.
- **Not searched:** Codex transcripts, and Claude transcripts before 2026-10-03.
- **Horizon:** no record after 2026-09-26 bears on Flow.
- **Sema:** the stores records found concern the meaning language, not Flow's Memory, and none was kept.
