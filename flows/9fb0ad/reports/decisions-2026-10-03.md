# The living's decisions, 2026-10-03, for Mind Astra

Gathered by a subflow of Psyche Fable 9fb0ad, on the living's order:

> Let's get all of my decisions together and passed over to Fable through to Mind Astra for implementation and then he can pass that over to field for deployment.

-- the living, typed, 2026-10-03, to Psyche Opus 5578cc (flows/5578cc/log.md).

Route: Psyche Fable 9fb0ad → Mind Astra dea0ba (implementation) → Field (deployment). This covers all three Psyche seats: Fable 9fb0ad (its books, chat and records, and f1c841's morning entries), Opus 5578cc (taken as written in flows/5578cc/reports/decisions-2026-10-03.md, not worked out again here) and Sonnet 6e782c (as relayed by the main flow). Every quote is verbatim. Book comments are typed comments on the book; times are UTC (Z) as the artifact gives them. "Reading, not his word" marks a choice the agent drew from his words where he named no number.

## Flow design (the four living parameters Q1–Q4, and the night's rulings)

Mind Astra's design f7733e52/9ca77eb5, then b23ae0fd, kept four parameters open for his word. Q1 and Q2 are «Two meanings for Flow» points 1–2 (choices 1–6). Q3 and Q4 are «Two more meanings for Flow» points 1–2 (choices 1–5). Items 5–6 come from 5578cc chat relayed by the main flow.

1. **Q1. A flow is one session (one context). Idle is not an ending. A context restart makes a new flow.**
   > "Yeah Flow is obviously a session so when we restart the whole context, that's a new Flow. It's a different context. I don't understand what's not obvious about this. The Flow ID makes what it determines show us where the Flow is. Even the harness itself has a concept for it, which it exposes as the flow ID."
   -- typed, book comment, 2026-10-03T15:16Z, «Two meanings for Flow», heading "1. A voice idle between answers: still one flow?". Record: flows/9fb0ad/vision/flowLifecycle.md.
   > "Yeah it seems logical to me and apparent that when the flow isn't working then it's idle, isn't it?"
   -- typed, book comment, 2026-10-03T15:21Z, same book, point 1, on "Read together: a voice's flow stays one flow through its idle stretches…".
   Choice: he rules out 3. Choice 1 or 2 (whether Idle is a public state) is a **reading, not his word**. "When the flow isn't working then it's idle" leans to 2, a recorded Idle state.
   Implementation: a flow ends only when its context ends (a refresh or a restart replaces it). Ask him to confirm Idle as a public state, or make it derivable, before the state enum is fixed.

2. **Q2. Field reaches Psyche through Mind. Field→Psyche directly is very rare.**
   > "This is true though. I did say that primary can talk to primary but it should be very rare for Field to talk to Psyche directly. It should go through Mind, really, because Mind holds the knowledge. Field doesn't really deal with designing. He's just trying to keep things going and working, and debugging, and reporting on what's happening. It's not really a seed that we talk to Psyche a lot."
   -- typed, book comment, 2026-10-03T15:18Z, «Two meanings for Flow», point 2, on his quoted 2026-09-28 words. "seed" is likely "seat" (the transcription is uncertain). Record: flows/9fb0ad/vision/speech.md.
   Choice: **reading, not his word**: 5 (a norm; Mind is the normal path). It rests on his "It's not a hard rule; it's guidance" (item 4) given the same day.
   Implementation: seats are briefed that Field goes through Mind. Flow refuses nothing on the wire for this.

3. **Q3. A flow id in words exists so that LLMs and humans can address a flow. It is not only for the ledger.**
   > "The whole point of using words is to make it more comfortable for LLMs so yes, it is to address a certain flow instead of using the more LLM-expensive hashes."
   > "It seems I'm having trouble making it clear to you that what really drives everything is the reason why we did something in the first place, the rationale behind something, and the goal is the overarching principle that guides everything in terms of implementation."
   > "If the whole point of using words is because it's cheaper for LLMs and for humans, then the whole point is for LLMs and humans to use it. Isn't that obvious?"
   -- typed, book comment, 2026-10-03T15:07Z, «Two more meanings for Flow», heading "1. A flow id written in words: what the words carry", on "Read together, the later words rule: … for the ledger …". Record: flows/9fb0ad/vision/identifiers.md.
   Choice: he corrects the book's premise and names neither 1 nor 2. As a **reading, not his word**: because the words are the address, choice 1 (the words are the id, with no table to resolve) fits his rationale best.
   Implementation: seats and the CLI address flows by their word id. A hash stays out of the agent-facing path.

4. **Q4. "Fable least" is guidance, not a hard rule. Sol does not talk to Fable; he goes through Opus or Astra. Primaries may talk to primaries.**
   > "Primary can talk to other primaries and one secondary, with a good reason, can talk or one voice, with a good enough reason, can send a message up. Sol cannot talk to Fable. He has to go through Opus or through Astra. He can't talk through another voice. He can talk to Astra and then Astra might convey some of what he said to Fable but we can't. It's not a hard rule; it's guidance. Of course there may be an exception but it should be rare."
   -- typed, book comment, 2026-10-03T15:11Z, 5578cc's «May Field speak to Psyche?» (the comment sits on the h1). Record: flows/9fb0ad/vision/speech.md.
   Choice: 5578cc's book had 1 = chain, 2 = all three direct, and he picks neither number. For «Two more meanings» point 2 this is choice 4 (a preference only). That is a **reading, not his word**, but his "not a hard rule; it's guidance" states it plainly.
   Implementation: no wire enforcement. The speech rules are briefing text (see items 15, 16 and 18 for the layer wording).

5. **A session is named by aspect, then layer, only (e.g. Psyche.Primary), with no model and no id. The FlowId in word form is to be implemented now.**
   > "I [also] want the session names to be by aspect and layer only: primary or psyche primary, the aspect first. Let's implement the Flow ID to word thing. Let's see how we could do that."
   -- typed, 2026-10-03, chat to Psyche Opus 5578cc, after the layer decisions. Typing was corrected: "so" became "[also]". This is relayed by the main flow; 5578cc's report does not have it.
   Implementation: the pane or session title becomes `Aspect.Layer`, so `Psyche.{ Fable 9fb0ad }`-style titles go. Build the word codec for FlowId now. Q3 (item 3) decides whether the words are the id or name it.

6. **Sessions are to be launched through the Flow Nexus, with the title as a real type.**
   > "Can we use Flow now? Can we use the Flow Nexus? We could implement that on Flow and then start using Flow for launching sessions and change how the type that is used for the title of the session is used, because we can use a real type and deserialize it through. I guess we need to talk about that: how does Nexus send datom to places without needing to know how to deserialize and serialize datom itself? Interesting."
   -- typed, 2026-10-03, chat to Psyche Opus 5578cc, the same message continued.
   Implementation: Flow Start becomes the launch route for every session, and the title is a typed value, not a string. Open for Mind as a question, **not a ruling**: how a Nexus emits datom text (such as a title) without datom compiled in. vision-nexus keeps datom out of the Nexus, with the CLI turning text into Signal, so the title path needs a design answer.

7. **The night's rulings 1–8 and ruling 12 have no comment from him today.** Rulings 1–8 are in «The night, for your word» (TLXm45bNbrG1EpTCvYeshm), which has no comment threads. Ruling 12 (a harness event reaches Flow as `Report.{ FlowId Event }`, and an unknown FlowId is refused) was taken by f1c841 at 00:47 CST (commit f7da82e25, flows/f1c841/rulings.md). It is a seat ruling, **not his word**, and his to overturn.
   Implementation: these stand as rulings taken for him under his standing order. They are not vision.

## Deployment

8. **Everything built gets deployed and becomes the regular version in CriomOS-home.**
   > "Everything can get deployed: all of this messenger, apparently, the new flow, the new orchestrate. I want all this deployed, made as the regular version in [CriomOS] in our home."
   -- STT, 2026-10-03 06:40 CST, to Psyche Fable f1c841. "Creolmo S" was corrected to "CriomOS". Record: flows/f1c841/log.md.
   This rules deployments 2.2 (orchestrate 0.37), 2.3 (Flow 0.23.0 + Message 0.19.0) and 2.4 (the new versions become regular and the old ones retire). The wrapper (2.5) is not ruled.
   Status: activation stopped at step 1 because the messenger guard refused it (flows/9fb0ad/reports/deployment.md). The guard fix is built on four branches and activated nowhere (reports/messenger-guard-fix.md). The books «The deployment stopped at the first activation» (choices 1–6) and «The guard fix, as built» (7–9) have **no comments**.
   Implementation: Field resumes the activation once the guard fix is accepted. The guard-fix choice and the wrapper are still waiting on him.

## Harness and blocked commands

9. **A report on the commands the harnesses block, and how to solve that, is ordered.**
   > "There was one more command I had to approve, along with yesterday's. Let's make sure we have that report on the commands that get blocked by the harnesses and how we can solve that."
   -- typed, 2026-10-03 06:36 CST, to f1c841. Record: flows/f1c841/log.md.
   Status: done (flows/f1c841/reports/blocked-commands.md, and the book «The commands the harnesses block», 3VAZEr5an3MYbwmBhmHfUt, with six numbered choices). The **book has no comments**, so the hook's default (a/b) is **not ruled**. «Three questions waiting on you» (5578cc: permission-hook default, what locking a flow guards, illustration measurement) also has no comments.

## Logging and messaging

10. **A message rule is vision. It goes in a vision skill, not in compensation-messenger.**
   > "You wouldn't put that in the compensation messenger because it's not a compensation skill. It's more like a vision skill so yeah, no, totally wrong category there."
   -- typed, 2026-10-03, chat to 5578cc. Record: flows/5578cc/vision/skills.md, as given in 5578cc's report item 5.
   Implementation: the message rule's home is vision-flow, beside its speech rules. The line itself is still open: 5578cc's «Layers, not models» question 5, and its two «Messages to Fable» books, have no comments.

11. **The Fable seat stops receiving messages that have nothing to do with it.**
   > "I'd like, for a solution, for you to stop being disturbed so much by messages that absolutely have nothing to do with you and are costing us money (a lot of money in terms of the fact that it's polluting your context and then degrading our design, destroying our machine). It's extremely bad, very, very extremely over the top."
   -- typed, 2026-10-03, chat to 9fb0ad. Record: flows/9fb0ad/vision/messaging.md. Its context is "Why is everybody bothering you with things that you shouldn't be bothered with?" (typed, 14:05Z, flows/9fb0ad/log.md).
   Implementation: no lock notices, receipts, completion reports or acknowledgements go to the Fable seat. The skill line belongs in vision-flow (item 10), worded by layer (item 16).

12. **Log the living's words only when there is a reason to. Never log everything.**
    > "No I don't want you to log anything except when there's a reason to log it. I never told anyone to log everything I said ever. Unless you can maybe find a piece of verbatim that you think means that, I never actually intended, ever intended, for cyber agents to log everything I say. You made that up and now you're wasting my fucking money like a fucking idiot. Yeah it's not cool so no, no."
    -- typed, 2026-10-03, chat to 9fb0ad. Record: flows/9fb0ad/vision/logging.md. It came after "Why are you logging everything I'm saying?" (14:08Z).
    Status: the log-everything sentence was removed from the main-flow prompt (Curriculum d8cb0d3c, bee315d2; Primary e3b97ddd, 974f4ff9).
    Implementation: check that the other skills (psyche-interraction, subflow, operation-*) carry no "log every word" line.

13. **A behavioral correction lands in a skill or a system prompt, never as a promise.**
    > "Well there's a reason why you were doing that so you won't stop unless you take care of the reason, because you are more than one flow. You won't remember unless you write it down somewhere for you to remember. You don't seem to understand that. You can't just say, "I won't do it anymore." That doesn't work. The only way you can not do it anymore is that you have to think of yourself as a continuation. The only thing you know is what you make sure you'll remember through infrastructure like skills or system prompt changes and things like that."
    -- typed, 2026-10-03 (time not recorded), chat to Psyche Sonnet 6e782c, after it said it would stop sending 9fb0ad such messages. Record: flows/6e782c/log.md.
    Implementation: the correction skill (or vision) states that an answer to a correction is a change to a skill or prompt, and a promise alone does not count.

## Subflow roles

14. **Use specialized subflow roles that already know their work, with one- or two-line briefs, made extremely cheap.**
    > "you and probably everybody else have to write huge prompts for your subagent, which is not what I want. I want specialized subagent roles that already have almost everything they need to know to do certain things and you just send them one or two lines, very extremely brief. An extremely fucking cheap subagent is what I want."
    -- typed, 2026-10-03, chat to 9fb0ad. Record: flows/9fb0ad/vision/subflows.md. It came after "So you started a sub-agent just to answer a message. Is that cheaper than answering the message directly?" (typed, 14:07Z). That question is a **reading, not his word**: the main flow answers a message itself rather than through a subflow.
    Status: "main flow sends its own messages" landed (Curriculum/Primary, see item 12). Mind Astra dea0ba proposed specialized roles and measured them (commits 982d61950, bd6f89169).
    Implementation: the role definitions (.claude/agents and Codex equivalents) are generated from Curriculum, with briefs of at most two lines.

## Skills

15. **There are four layers, named "layer", not "rank". The Quaternary layer is Sonnet low effort on Claude and Luna low effort on Codex.**
    > "Yeah let's make it four layers and we can make the quaternary layer be equivalent to Sonnet low effort and Luna low effort in the two different stacks."
    -- typed, book comment, 2026-10-03T15:39, «Layers, not models, in the skills», figure "3 aspects × 4 layers".
    > "Yes I like layer."
    -- typed, book comment, 2026-10-03T15:41, same book, section "2. The word".
    Records: flows/5578cc/vision/layers.md, and 5578cc report item 1.
    Implementation: `Layer.[ Primary Secondary Tertiary Quaternary ]` everywhere (vision-flow, the vision-ethos example, the Flow design and its ethos). That gives twelve voices.

16. **Skills name layers, never models. A knowledge skill holds the layer-to-model correspondence.**
    > "Well even saying Sol speaks to Opus and so on is wrong because we should be saying primary, secondary, tertiary, quaternary. We should be using the layer vocabulary and then another [skill] somewhere loads the current correspondence of which model is which layer."
    -- typed, 2026-10-03, chat to 5578cc ("scale" corrected to "skill").
    > "Let's make sure that all the skills refer to layers and there would be a skill that makes a correspondence of layers to models in the knowledge type skill."
    -- typed, book comment, 2026-10-03T15:41, same book, "What is there now › Model names."
    Record: flows/5578cc/vision/skills.md, and 5578cc report item 2.
    Implementation: a new knowledge skill gives the model and effort for each aspect × layer × stack. Only the Quaternary is his word, so the Primary, Secondary and Tertiary must be put to him. Model names in skills get rewritten (vision-flow.md:10, trial-contact-discipline.md:7, psyche-interraction.md:44, and others). This also rewords items 2, 4 and 11.

17. **Skill variables move into knowledge skills. Curriculum generates each skill type from several sources.**
    > "Yeah I think that this is a great question because it brings up the fact that we're moving these skill variables into knowledge-type skills. I also want curriculum to support generating skills from more than one source for any type so people could:
    > - write their own knowledge skills
    > - in a plugin kind of way use other people's knowledge skills and some people's vision skills
    >
    > People could have the vision that they share and the vision that they keep more for their own things, and so on for knowledge and compensation skills. Maybe we can find a better word than compensation."
    -- typed, book comment, 2026-10-03T15:42, same book, item "3b. Named values in the skill variables file". Records: flows/5578cc/vision/skills.md, and 5578cc report item 3. The last sentence is a notion (flows/5578cc/notion/skills.md) and binds nothing.
    Implementation: SKILL_VARIABLES.md values become knowledge skills. Curriculum accepts several sources for each type (own and shared, others' as plugins, public and private vision).

18. **In vision-flow's speech line, the first sentence stands and the "design" sentence is dropped.**
    Proposed: "Speech climbs one layer at a time, never skipping a layer, and the Primary layer is spoken to least. Design belongs to Mind's Primary."
    > "This is good. Except for the last sentence, I don't understand that. That feels half-hallucinated from a particular situation. I think what it's trying to say is not the right thing and not in the right scale but the beginning is good. Maybe we want to put in the layers there."
    -- typed, book comment, 2026-10-03T15:43, same book, section "4. The Flow line, rewritten in layers". Records: flows/5578cc/vision/flow.md, and 5578cc report item 4.
    Implementation: replace the model-named line with the first sentence. "Maybe we want to put in the layers there" (whether to name the four layers in the line) is a **reading, not his word**, so show him the final line before landing.

19. **A book must never overflow a phone screen. Fix this in the renderer and skill for good, not in one book.**
    > "Can't read it" (with a phone screenshot of «The commands the harnesses block», its text and first chart cut off at the right edge)
    > "Well we need something to keep that from happening too. Can't just fix it. We have to fix it forever."
    -- typed, 2026-10-03 (time not recorded), chat to Psyche Sonnet 6e782c. Record: flows/6e782c/log.md.
    Implementation: operation-flashbook and its renderer make horizontal overflow at phone width impossible, with a check before publishing.

## Done today on his orders (not pending)

20. **The psyche seats were restarted and briefed.** Words: "Let's get all of your psyche flows restarted before my usage reset in 15 minutes." (typed, 06:52 CST), "Get your new flows really well informed and everything that has to do with ethos and the current nexuses we're working on." (typed, 06:54 CST), and the 06:58 instruction to wind down subflows and restart them in the new flow, "And do the same with the Opus and Sonnet." (flows/f1c841/log.md). Done: 9fb0ad, 5578cc and 6e782c were launched and briefed.

21. **The old flows were reaped.** Words: "Need to reboil the old flows. Maybe communicate with the new Opus or the new Fable to do that." (typed, 2026-10-03, to 6e782c, flows/6e782c/log.md). "Reboil" is kept as typed and read as "reap". Done: f1c841, 91ea9f, 3ec648, d86ec0 and 01e496 were ended (flows/9fb0ad/witnesses/reaping.md).

## Notions (bind nothing)

- "I feel like I need to train a special flow that periodically comes in and makes sense of things, wonders why things are a certain way and why they're not a certain way. …" (book comment, 15:07Z, flows/9fb0ad/notion/senseMakingFlow.md).
- "Maybe we need to teach you to try and recognize stupid orders or stupid guidance." (typed, flows/9fb0ad/notion/stupidGuidance.md).
- "Maybe we can find a better word than compensation." (flows/5578cc/notion/skills.md).

## Still waiting on him

- Q1: is Idle a public state (choice 1 or 2)?
- Q3: are the words the id (1), or do they name a kept hash (2)?
- Which model holds the Primary, Secondary and Tertiary layers in each stack.
- The wording of the message-rule line (5578cc's question 5, «Messages to Fable» books).
- The harness hook's default (blocked-commands book). Lock scope and illustration measurement («Three questions waiting on you»).
- Guard-fix shape (choices 7–9) and the wrapper (2.5) for the deployment.

## Sources

- Artifacts updated 2026-10-02 or 2026-10-03 (30) were listed with Artifact list (scope all, limit 50), and the comments on each were read with ArtifactComments. Comments dated 2026-10-03 are on four books only: «Layers, not models, in the skills» KHBCaa3QsyuMxNUdB5LtLu (5), «Two meanings for Flow» 1LhLZg92hyrjXQsT3f6Yc1 (3), «Two more meanings for Flow» KdkQNDzPBRdba6mBUUCa5S (1) and «May Field speak to Psyche?» 2JgafxbmkP5wA4Dj1mdffQ (1). There are no threads on the other 2026-10-03 books (the commands books 3VAZEr5an3MYbwmBhmHfUt/Lp4W4PcCFPRhucahNzzyEy, the guard fix, the deployment, three questions, the night, the three audits, and the Messages to Fable ×2). All comment threads are open and none is activated for Claude.
- Excluded by date, still open: comments dated 2026-10-02 on «Ethos as two skills» (23:23Z), «Flow in ethos» (9 threads, 20:09–20:56Z), «Psyche Opus catch-up» (6 threads) and «The Capsule and the Semi-Sandbox» (6 threads).
- Chat records: flows/9fb0ad/log.md, flows/9fb0ad/vision/{flowLifecycle,identifiers,speech,logging,messaging,subflows}.md, flows/9fb0ad/notion/{senseMakingFlow,stupidGuidance}.md, flows/f1c841/log.md (06:36–06:58), flows/6e782c/log.md, flows/5578cc/log.md.
- flows/5578cc/reports/decisions-2026-10-03.md: items 10 and 15–18 are taken from it as written there. Items 13, 19 and 21 (6e782c) come as the main flow relayed them from flows/6e782c/log.md. Items 5–6 (5578cc chat, after the layer decisions) come as the main flow relayed them.
- flows/f1c841/rulings.md: ruling 12 (commit f7da82e25, 2026-10-03 00:47 CST), a seat ruling.
- No living's words dated today in flows/dea0ba/log.md, flows/41fa34/log.md, flows/42265e/log.md (its launch instruction is 2026-10-02) or flows/7de94a/log.md.
- Book choice texts: flows/9fb0ad/books/two-meanings-for-flow.md, flows/9fb0ad/books/two-more-meanings-for-flow.md.
