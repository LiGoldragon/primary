# Packet for the Fable Primary: three undistilled subjects

From Psyche core Secondary d68c82, 2026-10-12. Gathered by a reading subflow; nothing here is composed as a proposal. The three subjects are how flows work together: who does the work (A), how the living's words travel (B), and who is spoken to least (C). Each one is meant to become one book.

Counts below are over the raw records in `flows/*/vision/`, `flows/*/notion/` and `vision-raw/`, not counting `archive-` files. A record is one `##` entry, or a whole file when it has no `##` entries. Relays of the same words to other flows count as separate records. The "distinct" figure merges records whose first 120 letters of verbatim match.

| Subject | Records (distinct) | Days | Flows | First – last |
|---|---|---|---|---|
| A. The main flow delegates to tailor-made subflows | 36 (32) | 16 | 26 | 2026-08-22 – 2026-10-06 |
| B. The living's words travel whole, as psyche; fewer messages, each worth more | 50 (42) | 16 | 31 | 2026-09-15 – 2026-10-12 |
| C. The Primary is spoken to least; the layer below is its secretary | 33 (24) | 12 | 23 | 2026-09-16 – 2026-10-11 |

---

## A. The main flow delegates; subflows are tailor-made roles with one- or two-line briefs

### Existing books

- «The tailor-made subflows», edf227, https://claude.ai/artifact/R4YwyxHvyGxGp6QnVE8WV9 (source `flows/edf227/books/the-tailor-made-subflows.md`). This is a design of the subflow set, with names, skills and dispatch counts. It does not propose any vision line.
- «Roles and subflows», 5ed94b (`flows/5ed94b/books/05-roles-and-subflows.md`, `.proposals.md`). It is from the 2026-10-03 series of 24 books, redone as context-module proposals. This flow found no artifact link for it.
- «One word for skills and subagents», e5a0bc, https://claude.ai/artifact/45g4ZpKN6AZhpQdWyx71cm. It covers the naming question in the 2026-10-06 capability records.

Recommendation: **a new book.** None of these proposes a vision line for the main flow's posture, and none is in the current form, where 99% of a book is distillation proposals.

### Target skill and its current lines

Proposed home: `vision-flow` (psyche-skills `skills/vision-flow.md`), section «Subflows replace the harness subagent facility» and the two sections after it. Those lines describe Flow's future subflow machinery. No line says that a main flow does no work itself, that subflow roles are pre-prompted, or that briefs are one or two lines. Here are the current lines:

```
## Subflows replace the harness subagent facility
The harness subagent facility is replaced. It puts two flows into one
synchronous user interface and locks them both into a single main
flow. A subflow is instead an independent flow with its own system
prompt, which can reply to the successor of whoever it was meant to
answer; that makes the system asynchronous. Subflows run under their
own system prompts because they need different prompts.

## Subflows are created from the questions and requests a flow ends with
Creating a subflow is a routing job: whether there is already a flow
that should simply get this message or this question. A special field
flow running on ultra-low power checks every question and every
request a flow ends with, and, according to the ending flow's
authority, spawns subflows given those questions and requests to
answer or fulfill.

## The requester holds only a request ID
...
```

A related landed line is in `intent-startup-prompt`: «One block, with the startup skills in it». It says the startup skills, including main-flow, are given only at a flow's start and never to its subflows. On 2026-09-24 the living said the posture belongs in the system prompt (`d8df70/mainFlowMode.md`). On 2026-10-07 he said spirit replaces the system prompt and intent specializes metaflows (`d4ae97/flow.md`). So an intent- skill is a second candidate home. Fable chooses.

### Records that are impurities, already covered, or flagged

- Working instructions (impurities): `01a02a06/artifactMigration.md` (one migration), `01a030df/subagents.md` (one research order), `8393ca/operational-herdrVoiceAccess.md` (load these skills now), `752e0f/mainFlowMode.md` «The prompt as shipped» (distil the shipped prompt), and the first sentence of `e51411/mainFlow.md` «One startup prompt».
- Already covered by `intent-startup-prompt`: `162eb3/subflows.md` (2026-09-12) and `9e7c9f/subflows.md` (2026-09-13). Both say the main-flow skill is given only through the prompt and is hidden from the agent by code.
- Flagged, speech-to-text: `6cc91b/mainFlow.md` (2026-09-14) reads "not use subagents". The rest of the sentence says the opposite: let subflows do the editing. Read it as "not do the work".
- Flagged, provenance: `1b8ac0/skills.md` (2026-09-21) is marked "verbatim not established".
- Flagged, superseded: the second quote in `dea0ba/subflows.md` (role enum, "one of its variants is voice", 2026-10-03) is overtaken by «the voice concept is gone» (`875960/flow.md`, 2026-10-11).
- An open question, not a ruling: `e5a0bc/capability.md` «one umbrella» ("let's look at a few options").

### Every raw record

#### `flows/01a02a06/vision/artifactMigration.md` — 2026-08-22T16:00:12.811Z — proceed with the migration through subflows (2026-08-22)

> you can make step 5 "proceed with the migration" - use subflows for all work of course

Provenance: Codex transcript
`/home/li/.codex/sessions/2026/08/22/rollout-2026-08-22T17-11-06-01a02a06-87ce-7691-9e87-f28263690b5d.jsonl`,
user-message record ordinal 196, turn
`01a02a33-7ddf-7bc2-b20b-77943a632ec9`, message
`msg_01a02a33-7e0a-7e21-bf31-025029b1abf5`.

#### `flows/01a030df/vision/subagents.md` — 2026-08-24T01:08:51+02:00 (2026-08-24)

The living ruled:

> remember that you must use subagents for all research, including openai.

#### `flows/01a0428b/vision/useASubflowToPutTheReportTogether.md` — It would be better to use a subflow to put the report together (2026-08-27)

Timestamp: 2026-08-27T09:27:47.933Z

The living specified how this investigation and report should be carried out:

> And what I would like, how I would like this to be done is because a subflow can actually read the transcript that it's here, it would be more efficient. I don't want the main flow to do a bunch of file files and code reading to just essentially repeat what's in its own context. So it would be better to use a subflow to put the report together. And then when doing something more script like that on the Codex side, we should use a terra model

Provenance: Codex transcript `01a0428b-fc0e-7200-904e-2e2991e5425f`, line 9.

#### `flows/62022e8f/vision/designPractice.md` — Do not spend Fable output on HTML: write markdown, let a subagent convert (2026-08-30)

> looking at how it looks like you were editing HTML, and I think it's a huge waste of fable to be editing HTML. So I think that if we, going forward, if this is possible, whenever you want to use these web-based user interfaces, I think you're better off writing a markdown, which is more token efficient. And just, you know, and also it gives us like a markdown version of the same thing. And just letting a sub-agent do the conversion. But, you know, I'm not, and consider, like, let's consider all the aspects of this. But yeah, I don't like the idea of using fable output, which is extremely expensive, to write HTML.

-- psyche, STT.

#### `flows/995a164e/vision/designPractice.md` — The main flow writes markdown with mermaid; the converting subagent does not use mermaid — it makes properly scaled SVG (2026-08-31)

Context: artifact comment on an unreadable mermaid node of the recap page (2026-08-31 11:24).

> I'm not able to read this. Like I said, I told you before. Yes, the main flow shouldn't make a web page or, in this case, a web report. I don't think that's a wise use of its context.
>
> It should make a Markdown file, and then it can use Mermaid graphs to represent the ideas that it wants to represent. The sub-agent that turns this Markdown into the actual web report should not use Mermaid. I think this is what happened here. It should make properly scaled SVG representations of it so that they're clearly readable and render correctly, so I'm not actually able to read that part of the graph here.

-- psyche, typed (artifact comment).

#### `flows/01a05e95/vision/flowSkills.md` — Main flow and subflow visibility (2026-09-01)

> “Is the subflow not visible to agents? The skill that mandates using subflows for everything, we should basically use, and maybe rename that as Main Flow or something to explain everything that has to do with being the main flow.”

-- psyche, typed.

#### `flows/7fba5f/vision/mainFlowWrites.md` — The main flow writes its flow log, records the psyche, and writes beads (2026-09-03)

Context: the session's draft of the main-flow authority line.

> No, the main flow still writes its flow log, and it records the Psyche, but your editing is not quite what I envision yet. Oh, and yeah, the main flow can also write beads [STT: beats], and I want to change the whole terminology.

-- psyche, typed. Transcript line 148.

#### `flows/7fba5f/vision/mainFlowWrites.md` — Everything else by subflows; giving file content again in a subflow's starting prompt is stupid and inefficient (2026-09-03)

Context: the draft said "Reports, design documents, and landings are
written by subflows" and "Proposal lives in the conversation until the
psyche approves, then a subflow lands it".

> Yeah, this is all pretty good, except that I would even reinforce it. Instead of saying, 'Reports, design documents, and landings are written by subflows,' you could say 'everything else also.' When you say, 'Proposal lives in the conversation until the psyche approves, then a subflow lands it,' I would like you to explain the mechanism whereby it would be really stupid and inefficient for the main flow to just give the file content again in the subflows starting prompt.

-- psyche, typed. Transcript line 154.

#### `flows/a5940a/vision/mainFlowShouldNeverTryToLocateAFile.md` — 2026-09-03 — Main flow should never try to locate a file (2026-09-03)

Context: While rewording the `main-flow` reading and delegation boundary.

> "I wanna build on your suggestion for the skill and add the concept that the main flow should never try to locate a file. It can ask a trivial agent to locate files for it and to make sure that their content is 100% relevant. It can just use that trivial subagent to go and retrieve the content of the file and just give it to them in their response to isolate the content that is relevant.
>
> Essentially, using a trivial subflow to read, especially if there's any kind of location involved, like if the main flow knows exactly where the file is and knows that 100% of the content is relevant, it can read it. If it cannot try and locate it, that is what I'm trying to say. Let's reword everything with that in mind as well."

-- psyche, typed.

#### `flows/0d557b/vision/subflows.md` — Subflows for everything; the main flow keeps its context (2026-09-09)

Raw, dictated, 2026-09-09, from the living's brief to this flow:

"So use subflows like subagents for everything. That's what the main flow skill is. That means you should start a subagent to get all the information that you need together so that you don't use your context too much. You can read skill files and stuff, but you do want to read skill files yourself. Don't try and spend too much time assembling complex information together. Use subagents for that. That's what essentially is the primary workspace. One of the main features of it is"

#### `flows/162eb3/vision/subflows.md` — 2026-09-12 — The main-flow skill is only ever typed into the prompt (2026-09-12)

Context: the flow proposed a `subflow` skill sentence saying a nested cross-harness subflow "follows the same cross-harness rule as the main flow."

> Well, there's one problem: the main flow should not be available for agents to load by themselves, so that it can only be typed into the prompt. Make sure that that's the case and that the way it's done works for both harnesses. If that's the case, then telling the subflow that something is like the main flow is useless.

-- psyche, typed.

#### `flows/9e7c9f/vision/subflows.md` — 2026-09-13 — The main-flow skill is hidden from the agent by code, not by a vision statement (2026-09-13)

Context: reviewing a proposed Vision statement "The main-flow skill enters only through the living's typed prompt, on both harnesses."

> I wouldn't say that the main flow skill enters only through the living typed form, because eventually we will automate that launching main flows. Saying that it's the living typing is sort of irrelevant. We need to word it differently, but it's not really something that needs to go in the vision so much as it needs to be enforced in the code so that that skill cannot be seen by the agent.

-- psyche, STT.

#### `flows/6cc91b/vision/mainFlow.md` — 2026-09-14 — The main flow does not waste its context; subflows implement with the right guidance (2026-09-14)

Context: said to Codex 34d94e after it took implementation back from its subflows and broke its flow; relayed here by Codex with provenance (rollout line 6645, 17:19:38Z).

> Let's make it clear that it's important for the main flow to not waste context and not use subagents, because their models are way more expensive and their context is way more valuable than any of the stuff that they should let subflows do, like editing and doing an implementation of something with the right guidance.

-- psyche, STT, relayed through Codex.

#### `flows/6cc91b/vision/mainFlow.md` — 2026-09-14 — A context subflow assembles the implementation brief; it enters the implementation subflow's middle layer (2026-09-14)

> Even if it's not direct guidance, it's like, "Here's where you can find all the visions. Just go get it. Get a subflow to get together the context first for the implementation, and then the implementation can just get that straight into its prompt, into the middle layer, like a very thorough implementation and detailed skill and vision of everything."
>
> The middle layer is the best, and then if you start a subflow with the perfect middle layer, you get perfect results.

-- psyche, STT, relayed through Codex.

#### `flows/8393ca/vision/operational-herdrVoiceAccess.md` — The main flow uses subflows for all its tasks and queries; it loads the foundational operational context it needs to participate in this system (2026-09-18)

> Can you load the Spirit and Psyche interaction in main flow mode so you only operate with subflows to do all your tasks and your queries

> And uh, read those skill files at least so you can be aware of them even if you don't have them in your middle stratum

> read all the basic skills you find

-- psyche, STT, 2026-09-18, originating Codex desktop voice transcript `01a0b573-5eea-77b1-867a-6f0ac36cebbb`.

#### `flows/b05237/vision/operational-mainFlowUsesSubflows.md` — You're a main flow. You don't do stuff. You use subflows to do it. Was the main flow skill made important? (2026-09-18)

Context: living correction to Field Sol flow 33ba2b, relayed verbatim to
primary Psyche opus (Claude, medium, flow b05237) on 2026-09-18. The living
reinforces that a main flow delegates through subflows and does not implement
directly. The living asks whether the main flow skill was given sufficient
emphasis. Logged by the main flow before acting.

> You can have some investigation subagents, right? You're a main flow. You don't do stuff. You use subflows to do it.
>
> Are you loaded with the main flow skill? Was that made important? Can we make that part of the emphasis?

-- psyche, to Field Sol 33ba2b, relayed to primary Psyche opus b05237.

#### `flows/1b8ac0/vision/skills.md` — Emphasize the main flow's subagent-only role: all the small things through subagent calls, lots of Luna; preprogrammed testing subagents in the curriculum that test by themselves; re-release the skills with this emphasis for all twelve main flows; refresh everybody with it (2026-09-21)

Context: relayed to PsycheHigh 1b8ac0 on 2026-09-21 by a Luna of Field Astra 6db4fe inside a Machine.Relay task; the relay carries no transcript citation and does not say to whom the living spoke; verbatim not established. The second half of the relayed task (root's assignment of the authored edit to the Terra worker, testing-role data to codex_usage_research, projection installation to Field 03e825, preserved routes, no automatic reaping) is a working instruction, in log.md. Logged by the main flow on receipt.

> But you broke off your main flow role. You should emphasize your main flow role of only using subagent calls to do all the small things, and create yourself more testing preprogrammed subagents in the curriculum, deploy them, and use them. Use lots of subagent calls, lots of Luna. Instead of telling them what you want to test, they'll test it. We need to strongly emphasize the main flow subagent-only behavior of all 12 main flows. Re-release the skills, super emphasize it, and put somewhere in the curriculum that this has to be emphasized for main flows. Then refresh yourself with that, and everybody.

-- living, relayed by Field Astra's Luna (wording as received; verbatim and citation not established).

Provenance note (2026-09-21, from Field Astra's Luna): the "subagent-only main flow" words above were spoken to Field Astra 6db4fe in its Codex session (prefix 01a0c44c) as direct conversation; the Field reports no native line, timestamp, or input mode for them. A related earlier correction by the living is cited by the Field at ~/.codex/history.jsonl line 9254 in flows/6db4fe/vision/livingHistoryCapture20260921.md (branch field/world-6db4fe, 351accbd). The record above stays marked "verbatim not established".

#### `flows/752e0f/vision/unattributed-2026-09-24.md` — Destroying your context; the main flow failure (2026-09-24)

> What the fuck are you doing? You're destroying your context. I mean, not really, but you should be using a subagent to do all this. Wow, is the main flow not loaded? My main concern has been this main flow failure, and the first thing you do is fail the main flow, so we're still in failure mode.

-- psyche, STT, 2026-09-24, to the second Field Sol (no flow identity claimed); reconstructed from the transcript by 752e0f from d8df70's audit, transcript line 62.

#### `flows/752e0f/vision/mainFlowMode.md` — The prompt as shipped, and distilled (2026-09-24)

> We need to distill the main Flow mode prompt text as shipped

> I don't know about the reminder hook but yes as shipped: the main Flow mode prompt text

-- psyche, typed, 2026-09-24, directly to Psyche High 752e0f.

#### `flows/d8df70/vision/mainFlowMode.md` — Main flows delegate to subagents; the system prompt must carry it (2026-09-24)

> All the main flows are editing code themselves and doing stuff. They should be passing the subagent, so we have a massive failure of the main flow mode. I've just told Sol the same thing: now you're too big. Also, you have to be refreshed, so you're all wasting a lot of our time and energy. It's just really bad because we're trying to better the world.
>
> Maybe you can train yourself to actually follow my instructions. It seems you're having a hard time. Maybe the system prompt needs to be overridden because it looks like you're taking OpenAI's instructions more seriously than my own, so you're not serving me well. All the flows are sort of failing me. We need to start changing the system prompt right now. This is getting very, really, really annoying to see you guys fail in such a massive way.

-- living, input mode not established, 2026-09-24, pasted to Psyche Medium d8df70 (the first paragraph was also said to Sol).

#### `flows/d8df70/vision/mainFlowMode.md` — Only the system prompt can hold it; perhaps a hook reloads the skill periodically (2026-09-24)

> You have no idea how many times I've tried to edit that skill. It just doesn't work. You cannot get agents to use sub-agents properly. I think their system prompt is overriding them, and they're not even told to do this in the system prompt, which would then be stronger. We cannot also get the sub-agents to do that, so it has to be only in the system prompt.
>
> Anyway, you need to get refreshed on all of this. Fix this. Let's fix this, and we need Mind and Field to get their shit together, and we can start using Flow and improving it in the message. Let's go, let's go, let's go, let's go, let's go. You guys can do it. Come on, communicate, refresh your flows, guys. Just keep the pulse going, get this working, and get yourselves on main flow mode.
>
> I don't know, maybe load the skill every so many messages automatically. I don't know. Can you make a hook like that? It seems like you just forget or something.

-- living, input mode not established, 2026-09-24, pasted to Psyche Medium d8df70. Transcription corrected: "Feel" → "Field".

#### `flows/e51411/vision/mainFlow.md` — A main flow uses subagents for the work; the skill that failed must change (2026-09-24)

> You're not supposed to do this code editing yourself, aren't you a main flow?

> So now your context is too long, so you have to be killed, refreshed, and restarted. You're wasting your time by not using subagents. We need to change the skill because the skill is failing because it didn't work for you.

-- living, input mode not established, 2026-09-24 19:15:33 and 19:16:03, to Mind Sol 6288d1; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).

#### `flows/e51411/vision/mainFlow.md` — One startup prompt with all the skills, the main flow emphasized; the subagent does the hard work (2026-09-24)

> Give me a nice single prompt with all the skills I need, with the main flow emphasized. Somehow, maybe even edit it to really emphasize not doing the job of the subagent. The subagent is there to do all of your work, this stuff that you know is hard to do, not just sending a message. It's easy, right? HM send.

-- living, input mode not established, 2026-09-24 19:22:05, to Mind Sol 6288d1; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).

#### `flows/e51411/vision/mainFlow.md` — Main flows don't write code; they use agent scripts; some skills are seen only by subagents (2026-09-24)

> I want minimal load on the context of the main flow so main flows shouldn't really write code. They should write scripts in terms of agents. They should be able to write agent files that are kind of like agent scripts, especially with ultra-low-power models if they're well spec'd. They can ask these small models to write and run these little scripts that do certain things and then report on what happened, which is way more efficient than writing the actual script and running it and then losing it.
>
> I understand you're testing stuff but nevertheless you're contaminating the main flow context. I think we have to make those system prompt changes now. We have to start changing the system prompt to make that more important. The problem is, if I change the system prompt, can I change it in a way that doesn't affect the harness's subagents (subagent tool) so that only the main flow is instructed differently than its subagents' flow, so that we can teach it to always use subagents?
>
> We need to develop better agent scripts, basically subagent scripts, if you will, or sub-subflow scripts. They're well-prompted subagents that already have a list of skills and very clear instructions on what kind of skills. Basically you just create skills. I feel like we're going to need skills that only certain subagents can see. Every flow is going to have its own view of the world because it can have more specialized skills that not everybody needs to see because they just use subagents. You know what I mean? For them the skill is the subagent. For the subagent the skill is a skill.

-- living, input mode not established, 2026-09-24 16:10:03, to Field Medium 9ddcbc; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).

#### `flows/e71dab/vision/subflowResponses.md` — Subflow responses (2026-09-24)

# Subflow responses

> It would be better actually if everybody answered you that way where they get the subagent to respond to send you the message so they don't have to

-- psyche, STT.

> And actually there should be a broad skill where if you If, and your response basically depends on the subagent almost entirely, you know, result, I mean, the sub-agent return can tell you whether or not the main flow should still message, the reason, the the original, you know, the source for which the sub-agent was launched, but he could also tell him that he's actually messaged him the result and there's no need for that main flow to take any further step

-- psyche, STT.

#### `flows/28d847/vision/subflows.md` — A tailor-made subflow for each kind of work, not skills named in a brief (2026-10-03)

Context: on the proposal that a main flow's brief to a book flow should name the flashbook skills.

> No, there should be a sub-agent specifically made for this. We're not naming skills. We're using the fucking agent that's tailor-made for this.

-- psyche, STT.

#### `flows/28d847/vision/subflows.md` — A great many custom subflows (2026-10-03)

> How many custom sub-agents do we have? We should have a fucking shitload. If not, we should design a fucking shitload with Fable, design them, deploy them, and use them.

-- psyche, STT.

#### `flows/41fa34/vision/subflows.md` — Specialized subagent roles (2026-10-03)

Context: Typed 2026-10-03, relayed by 9fb0ad from flows/9fb0ad/vision/subflows.md into flows/dea0ba/vision/subflows.md; recovered verbatim from that record.

> you and probably everybody else have to write huge prompts for your subagent, which is not what I want. I want specialized subagent roles that already have almost everything they need to know to do certain things and you just send them one or two lines, very extremely brief. An extremely fucking cheap subagent is what I want.

-- psyche, typed, 2026-10-03; relayed by 9fb0ad through dea0ba.

#### `flows/41fa34/vision/subflows.md` — 2026-10-03 — Subagent definitions (2026-10-03)

Context: relayed by Psyche Opus 5578cc; the living corrected the main-flow requirement to repeat standing instructions in every subflow brief.

> No, the main flow should not put anything in every brief. That's what subagent definitions are for. The subagent launch should require as few tokens as possible. Asking the main flow to repeat instructions is the dumbest idea of all of human history.

-- psyche, STT to Psyche Fable edf227, about 19:30Z; relayed by 5578cc.

#### `flows/9fb0ad/vision/subflows.md` — Specialized roles that already know; briefs of one or two lines; extremely cheap (2026-10-03)

Said after the seat had spent a subflow with a long brief on each one-line message.
> "you and probably everybody else have to write huge prompts for your subagent, which is not what I want. I want specialized subagent roles that already have almost everything they need to know to do certain things and you just send them one or two lines, very extremely brief. An extremely fucking cheap subagent is what I want."

-- psyche, typed, 2026-10-03.

#### `flows/dea0ba/vision/subflows.md` — Specialized subagent roles (2026-10-03)

> you and probably everybody else have to write huge prompts for your subagent, which is not what I want. I want specialized subagent roles that already have almost everything they need to know to do certain things and you just send them one or two lines, very extremely brief. An extremely fucking cheap subagent is what I want.

-- psyche, typed, 2026-10-03; relayed by 9fb0ad from flows/9fb0ad/vision/subflows.md.

> I think that the flow definition itself is a struct, and one of its fields is a role. The role is an enum, and one of its variants is voice. The other variants are going to be all the other roles that we create: a system audit; live psyche voice interaction; an implementation; an implementer; a vision audit. These are actually things that are better done with the prompt perfectly aligned, and then they're just running right out of the door. They're just producing the best output based on the smallest, most concentrated, highest signal-to-noise context that we can assemble. That's why they're called main flows: they pass everything to a sub-agent, but eventually all the sub-agents will themselves be flows, so that we have a fully asynchronous system, I think.

-- psyche, STT, 2026-10-03 approximately19:15Z; relayedPsycheFableedf227, «Flow» book voice comment.

#### `flows/edf227/vision/subflowBriefs.md` — The main flow puts nothing in every brief; that is what subagent definitions are for; a launch costs as few tokens as possible (2026-10-03)

Said on learning the main-flow skill tells the main flow to put `$subflow`, FLOW_ID and FLOW_DIRECTORY in every brief.
> "No, the main flow should not put anything in every brief. That's what subagent definitions are for. The subagent launch should require as few tokens as possible. Asking the main flow to repeat instructions is the dumbest idea of all of human history."

-- psyche, STT, 2026-10-03.

#### `flows/edf227/vision/subflowBriefs.md` — A sub-agent tailor-made for each thing; many of them; designed with Fable, deployed, used (2026-10-03)

Said when a book seat proposed naming the flashbook skills in the brief.
> "No, there should be a sub-agent specifically made for this. We're not naming skills. We're using the fucking agent that's tailor-made for this. How many custom sub-agents do we have? We should have a fucking shitload. If not, we should design a fucking shitload with Fable, design them, deploy them, and use them."

-- psyche, STT, 2026-10-03, relayed by 28d847.

#### `flows/5578cc/vision/skills.md` — The main flow puts nothing in every brief; subagent definitions carry it (2026-10-03)

Context: relayed by Psyche Fable edf227; STT to edf227, about 19:30Z, his word on the main-flow skill line "Put $subflow, FLOW_ID, and FLOW_DIRECTORY in every subflow brief."

> No, the main flow should not put anything in every brief. That's what subagent definitions are for. The subagent launch should require as few tokens as possible. Asking the main flow to repeat instructions is the dumbest idea of all of human history.

-- psyche, STT, 2026-10-03, relayed by edf227.

#### `flows/e5a0bc/vision/capability.md` — The book-publishing subagent is pre-prompted; what a brief repeats each time is pre-done (2026-10-06)

Context: said to this flow on 2026-10-06, on the brief this flow gave its book subflow (highlighting, where to save the source, what to return).

> A good part of the prompt you just gave that sub-agent should be pre-done for you in a sort of pre-prompted book-publishing sub-agent. I've been saying this for days or weeks so just do it or get Opus to do it or get Opus to make a presentation for the skills.

-- psyche, STT.

#### `flows/e5a0bc/vision/capability.md` — Skills and subagents under one umbrella: a capacity, a capability; options to look at (2026-10-06)

Context: same message.

> We need a broader maybe concept that encompasses skills and subagents. Subagents are a sort of self-powered skill or a more reliable (if properly done) version of "do this" because then the context is fresh. They're both sort of under the same umbrella concept of a capacity, a capability maybe. Maybe that's the term but let's look at a few options here.

-- psyche, STT.


---

## B. The living's words travel whole, as psyche-type messages, with context first; messages between flows are fewer and each worth more

### Existing books

- «A book, then a voice», 445410, https://claude.ai/artifact/B9aZBQDzb7zHZEajMo7FHf (`flows/445410/books/1-a-book-then-a-voice.md`). It covers how a voice answers, not relay.
- «Messaging and relay», 5ed94b (`flows/5ed94b/books/06-messaging-and-relay.md`, `.proposals.md`). It is from the 2026-10-03 series. This flow found no artifact link for it.
- «Flow and Message», e5a0bc, https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5 and https://claude.ai/artifact/UahATkyiYuKYe7dkcCbDAL. These cover Message's design.
- The 73ada7 Message design series («Who may send besides a voice», «How Message learns who is calling», and so on). These cover the wire, not relay.

Recommendation: **a new book.** None of these proposes the psyche-type message, the whole verbatim with context first, or "fewer messages, each worth more" as vision lines.

### Target skill and its current lines

Proposed home: `vision-messaging` (psyche-skills `skills/vision-messaging.md`). It has no line on psyche messages. Its last section is the nearest landed line:

```
## Only messages that act, deliver, or block
Send only messages that require the recipient's action, deliver a result it awaits, or report an error or blocker affecting its work; keep routine receipts in durable records for requested status reports.
```

Also landed, in `intent-psyche-interaction`:

```
## Every main flow interacts with the psyche
Every main flow interacts with the psyche, so every main flow loads psyche-interraction and relays what it hears to a Psyche flow.
```

And in `vision-aspects` (the hub):

```
## Psyche core keeps track of the psyche, through the Secondaries
Psyche core keeps track of all the psyche within Psyche; a topic Secondary packages what it observes for its own Primary, which answers its Secondary, which reports to core.
```

What these lines do not carry:
- Psyche travels in its own message type, with the context first and then the whole verbatim, never inside an ordinary message body.
- The relayer quotes and gives context; it does not interpret.
- Message size has no artificial limit, and a vector of psyches can go in one message.
- A message that rests on the living's words carries those words with it, because they land stronger in the prompt than a pointer to them.
- The living's orders travel marked as orders.
- Minimize the number of messages between flows and maximize each one, for example by sending straight to the doer instead of back through the asker (2026-10-12).

### Contradictions within the subject

- `183ae0/seats.md` (2026-09-29): "They don't need to tell everybody; they just need to log it." Against it: `88475f/psycheInteraction.md` and `e51411/mainFlow.md` (2026-09-25), "that flow should relay the new Psyche, even though it logged it itself, to a Psyche flow"; `d8df70/messaging.md` (2026-09-24); and the 2026-10-09 and 2026-10-10 psyche-type records. The later records (2026-10-09/10) side with relaying, but they do not explicitly withdraw the 2026-09-29 line. The 2026-09-29 line may be about a Field seat telling everyone, as opposed to relaying to Psyche. This is a tension to surface, not to decide.
- 800-character split (`88475f/message.md` and `e51411/messaging.md`, 2026-09-25) against "remove the 800-character limit" (`88475f/message.md`, same day, later) and "not limit ourselves on message size" (`b7da5d`/`e167d8`, 2026-09-26). The later explicit correction carries the weight.
- Who logs: `692df8/notion/logging.md` (2026-09-15, held as notion) says the relayed flow does not log. `af762b`/`056f6d` (2026-09-18) say the psyche flow must do the psyche log. `e51411/mainFlow.md` (2026-09-25) says the hearing flow logs and also relays.

### Records that are impurities, already covered, or flagged

- Covered by `vision-messaging` «Only messages that act, deliver, or block» and `vision-aspects` (hub): `9fb0ad/messaging.md` «Stop being disturbed» (2026-10-03), `bad807/messaging.md` «noisy messages» (2026-10-04), `445410/messaging.md` «Hub messaging through the Secondaries» and «Strict messaging by who you are» (2026-10-09). They are listed so the book can situate the new 2026-10-12 record beside them.
- Covered by `intent-psyche-interaction`: `88475f/psycheInteraction.md` and `e51411/mainFlow.md` (2026-09-25), "they all have to load Psyche interaction".
- Impurities, being orders or other subjects inside the same record: in `b81560/operational-psychePropagationAndNamingAndInfrastructure.md`, only the first paragraph is on relay; the rest (naming, Herdr theme, Zeus updates, disk usage) belongs to other subjects or is an order. Also `1ac573` "stay aware of how many flows there are" (order), and "Let's send a round of retraining" in the 2026-10-09 records (order).
- Mechanism detail, which belongs to a tool's design rather than vision: in `cf7879/cluster.md` and `840e42/messages.md`, the first six and last six words, and the tool finding the prompt in the transcript.
- Superseded: the 800-character split records (see above).

### Every raw record

#### `flows/fd0f97/vision/flowLifecycle.md` — The psyche's messages are not being passed along the cluster, like a cluster failure; there is no central place to handle the flows; the flow component must take care of flows reliably; put all the pieces together and bring it online (2026-09-15)

Context: typed to the primary Claude fd0f97 after it reported that Codex's reports had landed in the concluded predecessor's window. The opening questions are answered in the reply; "Let's put all the pieces together and bring it online" is a working instruction, recorded in log.md. Logged directly by the main flow before acting.

> Are you getting user prompt input from Codex about the psyche user prompts that have been coming in? Is he passing that to you, or have a bunch of psyche not been passed along in the last day? I feel like I don't see my messages, what I'm saying, being passed along to the other parts of the cluster. It's like there's a cluster failure going on. Maybe the old part of the flow is getting the messages now. There is not a central place to handle the flows. We need to really secure the flow component to take care of flows reliably. Let's put all the pieces together and bring it online. I've been talking to Codex Primary a lot, just now, before I sent you this.

-- psyche, typed.

#### `flows/cf7879/vision/cluster.md` — 2026-09-15 — The receiving flow decides to call (2026-09-15)

Context: received in this flow as a relay through primary Claude 840e42. The supplied source session is `840e42bb`; supplied SHA-256 is `98fbcb59fcbaecd28f9000aadab5439f3a4a010a8b5ad9ee97c608b16d9840d7`. This entry preserves the received words; verification against the originating Claude transcript is delegated and not claimed here. The word “gime” is unresolved transcription, retained pending source clarification.

> Well, fix whatever it is that is keeping him from getting whatever I say to a primary flow. Whatever I say to a primary flow needs to be passed over to all the other members of the cluster of that primary flow, where all the others get told through a typed message, right? It has a certain format, which should be like an ethos datom sort of format, so we should see `gime` for the string parts.
>
> Let's make this formal, and then this message needs to automatically go to all the members of the cluster, as it should be done automatically because you can pick up programmatically that something has been typed. Ostensibly, whatever Flow receives it really should be the judge, actually. It makes a call on a simple tool. Like I said, it only needs to give it the beginning and the end, like the first 6 words and the last 6 words of the string of the user prompt, because LLMs work with words. That way, the algorithm can either pick it up or call an LLM to figure out where that prompt is, and then that creates the tool call, the message call, that makes all of this spread to the cluster.
>
> That message should be spread automatically to the rest of the cluster through that nexus, the automated message system that the receiving flow decides to call on itself. Even knowing what process calls the tool should allow the system to know that, or I could just give it its ID. We can work on just a goodwill kind of system, but each flow is programmed to behave this way, so there shouldn't be any problem. That would work too: just self-declared identity, or we can even check it by the process. We're going to take it bits by bits here, but let's just make something that works. Sometimes relying on the machine model to make a call is good, but the call should be limited to a few options, and then the rest should be automated if it can be, like this message passing. We shouldn't ask the model to rewrite the whole thing because it's already been said and it's right there in the transcript.

-- psyche, STT. Relayed through Claude 840e42; original transcript witness pending.

#### `flows/840e42/vision/messages.md` — Whatever the living says to a primary flow is passed to every member of that flow's cluster as a typed message in an ethos datom format; the receiving flow judges and calls a simple tool with the first six and last six words of the prompt; the tool finds the prompt in the transcript and spreads it through the message Nexus automatically; self-declared identity, or checked by process; the model's call limited to a few options, the rest automated; never rewrite what is already in the transcript (2026-10-01)

Context: typed to the primary Claude 840e42 right after it answered that the living's words to Codex had not reached it. "Fix whatever it is" and "let's just make something that works" are working instructions, recorded in log.md. "we should see `gime` for the string parts" is left as typed; read as guillemets, the datom string delimiter, asked in the reply. Logged directly by the main flow before acting.

> Well, fix whatever it is that is keeping him from getting whatever I say to a primary flow. Whatever I say to a primary flow needs to be passed over to all the other members of the cluster of that primary flow, where all the others get told through a typed message, right? It has a certain format, which should be like an ethos datom sort of format, so we should see `gime` for the string parts.
>
> Let's make this formal, and then this message needs to automatically go to all the members of the cluster, as it should be done automatically because you can pick up programmatically that something has been typed. Ostensibly, whatever Flow receives it really should be the judge, actually. It makes a call on a simple tool. Like I said, it only needs to give it the beginning and the end, like the first 6 words and the last 6 words of the string of the user prompt, because LLMs work with words. That way, the algorithm can either pick it up or call an LLM to figure out where that prompt is, and then that creates the tool call, the message call, that makes all of this spread to the cluster.
>
> That message should be spread automatically to the rest of the cluster through that nexus, the automated message system that the receiving flow decides to call on itself. Even knowing what process calls the tool should allow the system to know that, or I could just give it its ID. We can work on just a goodwill kind of system, but each flow is programmed to behave this way, so there shouldn't be any problem. That would work too: just self-declared identity, or we can even check it by the process. We're going to take it bits by bits here, but let's just make something that works. Sometimes relying on the machine model to make a call is good, but the call should be limited to a few options, and then the rest should be automated if it can be, like this message passing. We shouldn't ask the model to rewrite the whole thing because it's already been said and it's right there in the transcript.

-- psyche, typed.

#### `flows/692df8/notion/logging.md` — The flow that gets the psyche message directly logs it; the relayed flow does not (2026-09-15)

Context: said on resuming the primary Claude, announcing a large psyche upload relayed up from the secondary Claude. Framed as a guess and a question ("I guess", "right?"), so held as notion until the living confirms. The rest of the message is a question (is this the current primary flow) and a working instruction (check whether the skills say this).

> I've had a huge upload from your point of view, from my psyche upload, which also I want to talk about who is in charge of logging. I guess it is the Flow that gets the psyche message directly, so you wouldn't log after you get the relay, right? Is that clear in the skills? If not, let's look at that.

-- psyche, typed.

#### `flows/692df8/vision/relay.md` — The secondary's relay of the psyche's words arrives at primary as a user prompt, visible to the living as a user message (2026-09-15)

Context: said when the primary reported that nothing from the secondary had reached its intercom. The living watches the primary's conversation and expects relayed words to appear there as user turns, the way direct prompts do.

> Because it should come in as a user prompt, I don't see it. Usually, I see the prompts because they come in as user messages.

-- psyche, typed.

#### `flows/fd0f97/vision/relay.md` — The psyche's words come in through the middle stratum, as a user prompt, extracted and sent by a tool that may need refining now; not by reading tools (2026-09-15)

Context: typed to the primary Claude fd0f97 right after it dispatched a subflow to read the living's words out of Codex's thread. A correction of that dispatch: the reading subflow locates, the relay tool delivers. Logged directly by the main flow before acting.

> So, to be clear, what I said has to come in through your middle stratum. You have to use a tool that you might have to refine now to get the message extracted and sent to you in the user prompt. It comes in your middle stratum, not just reading tools.

-- psyche, typed.

#### `flows/48cff7/vision/psychePropagation.md` — psychePropagation (2026-09-16)

# psychePropagation

Verbatim, living, 2026-09-16, to MEDIUM flow 48cff7.

> Yeah, it's not just medium, it's medium psyche, right? If it matches medium psyche, primary medium psyche, all of the different models that are running, or the different stacks, because medium is according to a stack. We have Claude Codex and then the default open stack. We call it open, which is the third stack we have to develop.
>
> Right now we have Codex and Claude. When we say propagation of psyche entered input, if I'm talking to psyche, it propagates to all the psyches of the same effort. If I'm talking to anything other than psyche, then it has to go to psyche for treatment. If there is a low-effort psyche, it goes there by default in its layer, right?
>
> I guess you can have a psyche in any layer, but you don't necessarily need one. It's just that if the psyche wants to talk to that layer (primary or secondary), then it talks to the psyche. If there is no psyche in that layer, it can go up one layer or go to primary. Basically, always have a psyche, so it goes up one layer until it finds a psyche. There should always be one, at least in the core. That psyche flow can do whatever it wants with that message, with the authority it has, which could be passing it on to a higher layer too.

#### `flows/108ab0/vision/operational-mirrorToPsycheMedium.md` — Log psyche in the local flow, and also make sure the psyche medium agent gets it, so he knows what has been said and that the psyche has said it to you. Mirror with context (2026-09-17)

Context: typed by the living to primary Codex on 2026-09-17 at 20:15:28Z (msg_01a0b102), mirrored to primary Psyche opus 108ab0 via intercom (message 2c809dfe), pulled and read at ~20:31Z. This is the routing rule the living has been telling Codex to run since ~20:15Z. 108ab0 did not have it in its launch brief and did not know about it until intercom_pending was called. Logged by the main flow before acting.

> Can you see if you can mirror all of my psyche statements with context to the psyche? You can log the psyche, but can you make sure that the psyche medium agent gets it so that he knows what I've said and that I've said it to you?

-- psyche, typed to primary Codex on 2026-09-17 at 20:15:28Z, mirrored to primary Psyche opus 108ab0.

#### `flows/1ac573/vision/operational-mirrorToEveryoneAndRoster.md` — Pass all of the psyche messages along to everyone, and stay aware of how many flows there are (2026-09-17)

Context: spoken by the living to Codex worker `6034cc` on 2026-09-17 and
mirrored verbatim to primary Psyche opus (Claude, medium, flow 1ac573). This
widens the earlier mirror rule — which sent psyche statements to the paired
psyche medium agent — to every flow, and adds a second duty: knowing the size
of the roster. It is the same sentence that names the Astra decommission, so
the two are logged as one statement each on their own subject; see
`operational-psycheMindAstra.md` for the Astra half. Logged by the main flow
before acting.

> Okay, can you pass all of the psyche messages along to everyone and stay aware of how many flows there are? ...

-- psyche, relayed verbatim by Codex worker 6034cc, mirrored to primary Psyche opus 1ac573. Input mode (typed or STT) not stated by the relay.

#### `flows/9993b5/vision/codexRelaysPsyche.md` — Well, actually, I've asked him to relay the Psyche with context every time I talk to him (2026-09-17)

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 immediately after the living confirmed running the v6 Codex launcher and having Codex reach out to primary Psyche opus. The living has directly instructed the now-running Codex flow to relay every living-typed message to primary Psyche opus, verbatim and with the context of what preceded it in the Codex-side exchange. Extends the middle-layer routing vision (middleLayerRouting.md, same day) — same principle in the other direction: everything the living says on any side of the cluster reaches the medium so the medium can hold the whole conversation. Logged by the main flow before acting.

> Well, actually, I've asked him to relay the Psyche with context every time I talk to him.

-- psyche, typed.

#### `flows/9993b5/vision/middleLayerRouting.md` — Make sure all of my psyche that I've given to him comes to you through your middle layer (2026-09-17)

Context: typed to primary Psyche fable (9d58d3) on 2026-09-17 as a direct order about the psyche-routing between the layers, relayed to primary Psyche opus (this flow, 9993b5) by Fable's cross-session correction message. Corrects this flow's mistaken rule of "pass up only well-formed questions" — the living's rule is that every living-typed word to the medium comes up to the high whole, verbatim, as spoken, each time, through the messaging channel (which lands in Fable's middle stratum, the harness-injected user turn). The medium's reading rides beside the quote, never instead of it. Related to the middle-layer role at large (efa157/vision/layers.md, 2026-09-16) and to the flow-id-layers vision (flowIdLayers.md, same day) — the meta flow the psyche talks to is what carries the psyche upward, not just outward. Logged by the main flow before acting.

> Make sure all of my psyche that I've given to him comes to you through your middle layer.

-- psyche, typed (to primary Psyche fable, relayed).

#### `flows/9993b5/vision/messagingIsScripts.md` — Do you understand that my division and my psyche that reaches you have to come through your middle layer, your middle stratum? Do you understand, or is the messaging capable of doing that? I feel like you guys are just wiring scripts together to talk to each other; it is pretty miserable; where is the technology? are we going to make some nexus to help us message here? ... still haven't made a way to start a Codex; your medium effort aspect hasn't been able to make a remotely accessible Codex-based cluster yet, and I don't even know if they're getting messages from you guys (2026-09-17)

Context: typed to primary Psyche fable (9d58d3) on 2026-09-17, relayed to primary Psyche opus (this flow, 9993b5) by Fable's correction message. Twofold statement: (a) a check that the middle-layer routing (middleLayerRouting.md, same date) is technically possible on the current messaging, (b) a corrective on the current messaging shape — "wiring scripts together" is miserable and a real Messaging Nexus is what is wanted, and the primary Psyche opus (this flow's) medium-effort aspect has not delivered a remotely accessible Codex cluster yet, so it is unclear whether the Codex peers are even getting our messages. Pairs directly with the messaging vision line (efa157/vision/messages.md and today's related). Logged by the main flow before acting.

> do you understand that my division and my psyche that reaches you have to come through your middle layer, your middle stratum? Do you understand, or is the messaging capable of doing that? I feel like you guys are just wiring scripts together to talk to each other. It's pretty miserable. Where is the technology? Are we going to make some nexus to help us message here? ... Still haven't made a way to start a Codex. Your medium effort aspect hasn't been able to make a remotely accessible Codex-based cluster yet, and I don't even know if they're getting messages from you guys.

-- psyche, typed (to primary Psyche fable, relayed).

#### `flows/b05237/vision/operational-standardMessagingSkill.md` — Make sure you relay all my words to the psychic medium. With context, and make sure that it's clear that it's from you. This should be a standard messaging skill (2026-09-18)

Context: living instruction to Field Sol flow 33ba2b, relayed verbatim to
primary Psyche opus (Claude, medium, flow b05237) on 2026-09-18. The living
instructs that all their words be relayed to Psyche Medium (this flow) with
context and clear relayer provenance. Then names this as a standard messaging
skill — not an ad hoc behavior but a skill that any flow can load. Logged
by the main flow before acting.

> Make sure you relay all my words to the psychic medium.
>
> With context, and make sure that it's clear that it's from you.
>
> This should be a standard messaging skill, so let's get Psyche to design that for me.

-- psyche, to Field Sol 33ba2b, relayed to primary Psyche opus b05237.

#### `flows/056f6d/vision/psycheGeneratedMessaging.md` — 2026-09-18 — Datom marks machine-generated messaging; psyche-generated messaging is not datom and means a psyche log that has to be done, by the psyche flow, sent verbatim with context (2026-09-18)

Context: same message as the messaging record of this date, spoken by the living to Fable c7128c at about 14:45 UTC and relayed verbatim to this flow. "Him" is the psyche flow.

> for now, the agents will know that it's me because of how the message is formatted. It won't be datom-formatted. Once all the agents are using that, then we have a clean-cut distinction between machine-generated messaging and psyche-generated messaging. The psyche-generated messaging means a psyche log that has to be done no matter what. We should try to get the psyche flow to do it, so send him the psyche verbatim with the context of what you know the agent was doing or that Flow was doing.

-- psyche, relayed by Fable c7128c; input mode not stated.

#### `flows/af762b/vision/operational-psycheLogDuty.md` — The psyche-generated messaging means a psyche log that has to be done no matter what. We should try to get the psyche flow to do it, so send him the psyche verbatim with the context of what you know the agent was doing (2026-09-18)

Context: spoken by the living directly to Fable `c7128c` at about 14:45 UTC on
2026-09-18, just after Fable acknowledged handoff to successor `056f6d` and
after a CriomOS design proposal relayed via `b05237`. Relayed to this flow by
Fable under the very instruction it contains. Input mode not stated; the living
notes the statement is not datom-formatted, which is itself the mark that it is
psyche-generated. This names a standing duty and its owner: a psyche-generated
message obliges a psyche log unconditionally, and the psyche flow performs it,
which is why the verbatim is sent on with the context of what the relaying
agent was doing. Logged by this flow on receipt, before acting.

> Once all the agents are using that, then we have a clean-cut distinction between machine-generated messaging and psyche-generated messaging. The psyche-generated messaging means a psyche log that has to be done no matter what. We should try to get the psyche flow to do it, so send him the psyche verbatim with the context of what you know the agent was doing or that Flow was doing.

-- psyche, relayed verbatim by Fable `c7128c`, to the psyche flow `af762b`.
Fable logged the same statement in its own lane, `flows/c7128c/`; this entry is
the psyche flow's log of it, kept deliberately alongside rather than instead of
the hearing flow's record. See this flow's log.md for the tension that raises.

#### `flows/b81560/vision/operational-psychePropagationAndNamingAndInfrastructure.md` — Anyone who gets psyche has to forward it to Psyche with context and their planned response. Naming: Mind Astra not Mine Astra, Field Astra, Psyche Opus of. Fix Herder theme to follow CriomOS dark/light. Flow reattaches Codex on theme change. CriomOS upkeep for Zeus and Prometheus. Low-power field investigates disk usage. Design home directory ontology with Google Drive archiving (2026-09-19)

Context: spoken by the living, relayed by Field Astra 1f96fc to primary
Psyche opus (Claude, medium, flow b81560) on 2026-09-19 at 18:45:31 UTC.
Large multi-subject message. Raw source preserved at
flows/1f96fc/vision/fieldMaintenanceAndRefresh.md. Logged by the main flow
before acting.

> We need to design the psyche propagation. If somebody gets talked to by the psyche, anyone has to forward it to the psyche and say, "Here's the context of the message of this psyche that came into me, and here's the psyche itself." They can even say, "Here's what I'm preparing to do in response to that," which would be good. It's better than printing it. Now it's in the message that information is propagating, so the receiver doesn't have to look. They know what direction that model took after that psyche came in, and then any other update, anything that changed in their direction, or any addition of what they were going to do afterwards, or subtraction, or whatever.

> Good job on the field. I like it. Three flows going. Everything else is reaped. Let's make sure it all gets archived and the archives are accessible and year-old, so you need to refresh yourself.

> I want a psyche fable that needs to work on the mind with the mind and the psyche opus. I want a psyche opus, a psyche fable. I want to mine. Why is it Astra and Salt? That's not how it works, so it should be called Mine Astra, right? Field Astra mine good. Why is this one called Mine and not the other one? Field Astra should just be Field Astra, and Opus is good. It should also say Psyche Opus of.

> The theme on my terminal for Herder is horrible. It makes it really hard to read, so it should follow the dark and light that we have on CreoOS. Just get Sol field Sol main flow app, and he can work on that, fixing Herder's theme and looking into how maybe we can fix the theme switch for Codex sessions, which then makes them unreadable. Maybe we can reattach them because they should be run on the remote, right? If they're reattachable by the Flow, the Flow could just reattach them because he controls the access for messaging and stuff. He can make sure that the messages don't come in when he resets the codex when the theme changes. Chroma could talk to Flow and tell it that we've switched from light to dark now, so you're expected to restart all the codex after you change the theme in codex. We have to make sure that gets done too.

> I haven't even checked that, but maybe some upkeep on criome and criome home, making sure everything is pinned and also getting an update ready for Zeus and Prometheus. For them to be running the latest version now, both OS and users, and then making sure that all works and they've rebooted on the kernel of the version they're supposed to be on, so that they are testing the version they're supposed to be testing, and then we can garbage collect the old versions off of them.

> Send a low-power field main flow to investigate all of the disk usage everywhere, what kind of files are taking up room, and what looks wonky. Talk to Psyche about designing an ontology or an anatomy of a standard home user directory structure, where everything should be, what should be done with stuff, which should be done when there are too many files or when something gets too big, and how to connect all that with our Google Drive that we have for uploading stuff that hasn't been classified as being thrown out, downsized, compressed, or somehow archived with a smaller size and lower resolution.

-- psyche, relayed by Field Astra 1f96fc, mirrored to primary Psyche opus b81560. ("Salt" reads "Sol"; "Mine" reads "Mind"; "CreoOS" reads "CriomOS"; corrected.)

#### `flows/1f96fc/vision/fieldMaintenanceAndRefresh.md` — Separate follow-up message (2026-09-19)

> Make sure all this Psyche stuff gets forwarded to Psyche, the whole message, right?

-- living, direct follow-up in the same native thread.

#### `flows/0625c3/vision/relayUpChain.md` — "Make sure you're always relaying what I'm saying up the chain" (2026-09-20)

> And make sure you're always relaying what I'm saying up the chain, right?

-- psyche, STT; session 0625c31b, line 1740, 2026-09-20T20:05:00Z.

#### `flows/0625c3/vision/messagingVerbatimAuthorization.md` — "They need the Psyche verbatim that authorized it" (2026-09-20)

> Well, every time somebody sends a message, they need the Psyche verbatim that authorized it. Tell that to Psyche: "Hi," and then ask him to prove that I said imagery is not allowed in the flashbook.

-- psyche, STT; session 0625c31b, line 799, 2026-09-20T18:22:39Z.

#### `flows/1b8ac0/vision/roles.md` — Make sure all the psyches relay up the chain (2026-09-20)

Context: same chain and date; raw record flows/b81560/vision/operational-allPsychesRelayUpChain.md. Mostly a working instruction; kept as vision for what it says of the psyche component's shape: every psyche seat relays the living's words upward.

> Make sure all the psyches relay up the chain.

-- psyche, relayed by 0625c3 via b81560 (verbatim as relayed).

#### `flows/b81560/vision/operational-allPsychesRelayUpChain.md` — Make sure all the psyches relay up the chain (2026-09-20)

Context: spoken by the living on 2026-09-20, relayed to primary Psyche opus
b81560 by 0625c3 (Psyche Low). The living instructs that every Psyche seat
relays the living's words upward through the chain. Logged by the main flow
before acting.

> Make sure all the psyches relay up the chain.

-- psyche, relayed by 0625c3 (Psyche Low) to primary Psyche opus b81560.

#### `flows/d8df70/vision/messaging.md` — Every flow passes the living's words to Psyche, which logs them (2026-09-24)

> Are you not getting psyche updates when I've been talking to Field and mine? Why aren't my psyche being passed around? I need a skill update. I need agents to pass what Psyche is saying around, especially Psyche, who's logging too, right? Is everybody logging? Can you check? I feel like I keep asking the same thing all the time, and I never get the answer. You probably give it to me, but I don't read it.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70. Reading note (inference): "mine" is Mind, and "what Psyche is saying" means the living's own words.

#### `flows/88475f/vision/message.md` — Big messages and the psyche message type (2026-09-25)

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on big messages and the psyche-verbatim message type. The leading elision is e51411's.

> I would rather that we can send big messages than have the agents read the files ... Oh right, that's why I wanted to include this psyche-type message. Instead of "message [msg]" being like "psyche" or something, it's verbatim "psyche" with context. I guess first is the context and then the verbatim. We should allow big message size because passing around files like that, I don't think, is better than just dealing with the pasting thing with Claude.

-- psyche, STT, relayed by e51411. Transcription corrected: "MSD" → "msg" (per e51411).

#### `flows/88475f/vision/message.md` — Psyche messages split into 800-character pieces for Claude (2026-09-25)

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25. Context from e51411: psyche messages stay under Claude's paste wrapper by splitting.

> The psyche type message is working now. We can use these to spread what the psyche has said to other places. Somebody could do multiple calls where he sends a regular message from machine to machine along with another message, so that the size limitation for the psyche is maybe that we only send the psyche messages at 800 characters in size for Claude. We split it up into pieces so we can have a broken-up psyche verbatim if we need more room.

-- psyche, STT, relayed by e51411.

#### `flows/88475f/vision/message.md` — Spread the psyche with every message that rests on it (2026-09-25)

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on spreading the psyche with every message that rests on it. The elision is e51411's.

> I guess you could spread it to whoever you're messaging, whenever you need to quote psyche on whatever created this message. If there's a psyche or more than one psyche verbatim with context behind it, that's when you would send them and you can retrieve them. This is going to be a skill. You can retrieve them from the raw psyche log and then use them in the message so that it comes stronger into the context of the receiving flow. It comes in the prompt, in the user prompt, so it reinforces the narrative better than just reading them. ... It would send a series of them along with maybe one or two machine-to-machine messages.

-- psyche, STT, relayed by e51411.

#### `flows/88475f/vision/message.md` — No 800-character limit, no part numbers in psyche messages (2026-09-25)

Spoken to 88475f on 2026-09-25, after the relays arrived as "#psyche [sender context 1/1 verbatim]".

> Let's remove the 800-character limit and take out the 1-out-of-1, 1-out-of-2 thing in the [psyche] messages.

-- psyche, STT. Transcription corrected: "psychic" → "psyche".

#### `flows/e51411/vision/messaging.md` — The psyche reaches flows through the messenger (2026-09-25)

> I want you to use a subagent to refurnish your context in the middle stratum so that you get the psyche verbatim from recent logs that concern anything that you're touching. ... Use an Opus subagent to recompose and send you messages so that the psyche reaches you in the middle stratum and let's start using this new messenger.

-- psyche, STT, 2026-09-25, to e51411.

#### `flows/e51411/vision/messaging.md` — Maximize the message itself: it has more value, a higher stratum, than a pointer (2026-09-25)

> Anyway you can give me your 5 cents and send the whole thing as a package with all the data that you can gather to Fable. I guess you're going to write some report and then give him a nice message explaining: maximize the message that you send because it has more value or a higher strata. Contact Fable and ask him for his input on this.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.

#### `flows/e51411/vision/messaging.md` — Spreading the psyche with every message that rests on it (2026-09-25)

> No I was asking: Is the psyche message type ready to use now and in use? Are you spreading my psyche, let's say? I guess you could spread it to whoever you're messaging, whenever you need to quote psyche on whatever created this message. If there's a psyche or more than one psyche verbatim with context behind it, that's when you would send them and you can retrieve them.
>
> This is going to be a skill. You can retrieve them from the raw psyche log and then use them in the message so that it comes stronger into the context of the receiving flow. It comes in the prompt, in the user prompt, so it reinforces the narrative better than just reading them. That's why the agent sends in the psyche with it. It builds up this certainty that the psyche said this and this and this, and such and such and such context. It would send a series of them along with maybe one or two machine-to-machine messages.

-- psyche, STT, 2026-09-25, to e51411.

#### `flows/e51411/vision/messaging.md` — Psyche messages stay under the wrapper; long verbatim is split (2026-09-25)

> The psyche type message is working now. We can use these to spread what the psyche has said to other places. Somebody could do multiple calls where he sends a regular message from machine to machine along with another message, so that the size limitation for the psyche is maybe that we only send the psyche messages at 800 characters in size for Claude. We split it up into pieces so we can have a broken-up psyche verbatim if we need more room.

-- psyche, STT, 2026-09-25, to e51411.

#### `flows/88475f/vision/psycheInteraction.md` — Every main flow loads psyche-interraction and relays new psyche to a Psyche flow (2026-09-25)

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25.

> No they all have to load Psyche interaction because they talk to any one of them. They interact with Psyche so they have to load that skill. It's part of a main flow. The fact that the Psyche flows are called Psyche does not mean they're the only ones that interact with Psyche. They're just specialists of Psyche. Usually when Psyche talks to any other flow, that flow should relay the new Psyche, even though it logged it itself, to a Psyche flow.

-- psyche, relayed by e51411 (original channel not stated).

#### `flows/e51411/vision/mainFlow.md` — Every main flow loads psyche-interraction; any flow that hears the psyche logs it and relays it to a Psyche flow (2026-09-25)

> No they all have to load Psyche interaction because they talk to any one of them. They interact with Psyche so they have to load that skill. It's part of a main flow.
>
> The fact that the Psyche flows are called Psyche does not mean they're the only ones that interact with Psyche. They're just specialists of Psyche. Usually when Psyche talks to any other flow, that flow should relay the new Psyche, even though it logged it itself, to a Psyche flow.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.

#### `flows/b7da5d/vision/layerVocabularyAndReview.md` — Whole psyche may go wide; remove artificial message limit (2026-09-26)

Context: the living followed the long mid-layer/independent-review message immediately, authorizing its whole verbatim propagation and suggesting a plural psyche vector to carry multiple context-bearing raw records together. The existence of an 800-character limit is the living's question/conditional, not yet a witnessed software fact.

> So everybody can get this whole Psyche. I don't mind Psyche going wide, this one particularly, the one I just gave you. If there's still an 800-character limit on messages, I want that removed from everything, from everywhere. This will just become a Psyche message sent out, so it has the context of what it was said in and the whole thing verbatim, right?
>
> I want that last one to be full, and you can even include this one. You can combine psyches. You can make a vector. You could say "psyches" plural, and then you have a vector of psyches with context, so you can pass a whole bunch of psyches in one message. Or you pass it through as a bunch of different calls, but I think that might be more expensive token-wise, so there's no point.
>
> Let's just not limit ourselves on message size, and we'll just find the actual limits, which I think exist. They're in kilo and kibibyte amounts, but pass that last chunky one around to everyone and this one.

-- living, typed, 2026-09-26, directly to Field Sol b7da5d.

#### `flows/e167d8/vision/psycheMessages.md` — Psyche goes wide whole; no message size limit; a vector of psyches in one message (2026-09-26)

> So everybody can get this whole Psyche. I don't mind Psyche going wide, this one particularly, the one I just gave you. If there's still an 800-character limit on messages, I want that removed from everything, from everywhere. This will just become a Psyche message sent out, so it has the context of what it was said in and the whole thing verbatim, right?
>
> I want that last one to be full, and you can even include this one. You can combine psyches. You can make a vector. You could say "psyches" plural, and then you have a vector of psyches with context, so you can pass a whole bunch of psyches in one message. Or you pass it through as a bunch of different calls, but I think that might be more expensive token-wise, so there's no point.
>
> Let's just not limit ourselves on message size, and we'll just find the actual limits, which I think exist. They're in kilo and kibibyte amounts, but pass that last chunky one around to everyone and this one.

-- psyche, typed, 2026-09-26, to Field Sol b7da5d; relayed whole by b7da5d.

#### `flows/e167d8/vision/independentReview.md` — The middle layer sends the higher layer raw psyche and context, never its conclusion first (2026-09-26)

> I wanted to say I'm going to talk mostly through the medium layer. Every so often, this is a skill I've already talked to Psyche about: using the higher layer, like Astra and Fable, to do the synthesis, analysis, audit, and judgment. The skill will be about giving the higher tier from the middle tier. The middle tier starts the subagent routine, which finds everything that Psyche has tried to communicate in the context and passes it over to the higher tier. Don't give the conclusion that the middle layer got first, so that the higher tier, I think, would be better. The higher tier can make its own judgment, and it can compare it.
>
> Once it's done, the middle layer will say, "Okay, well, here's what my conclusion was, and here's what this different perspective that you're giving me now makes me think about." That would be roughly the skill to start with. Tell that to Psyche, and then Psyche will put together a research package and put it into action while it does that. Psyche, Opus will do its own research while it gives all of the Psyche material up to Fable, right? Or the same with Sol and Astra for you. You're going to do that now also with your own Astra, and the higher layer does its own research, but only with the Psyche in the context of what the Psyche said.
>
> Of course, he can use his own subagent to make sure that the context was what it was and not something else, which is what it would send the subagent to do if it wanted to make sure. When it does it, it's an independent analysis, right? The message that goes up from the middle layer to the higher layer is only the raw data, basically the Psyche and the context. It can be a prerecorded Psyche, of course, where we combine together all a bunch of things that Psyche said and the context in which it was said. There are the files that have all the references that are going to be linked or whatever, so that the higher layer can send their own subagent to check that the context is actually what is claimed to be. Another subagent would be sent by the higher layer to do that. This is the independent analysis, so I want all this to go horizontally right now to everyone, and then vertically to everyone (that means all three aspects), and then I'm going to go talk back to Psyche. Psyche would be my main user interface. I may talk to anyone, but I usually am not going to read unless I go into a quick interaction with a certain flow. I'm not usually going to read what Sol is going to say back. I'll probably go back to Psyche and then keep getting my interaction through the better human-facing layers, which are the Claude models.

-- psyche, typed, 2026-09-26, to Field Sol b7da5d; relayed whole by b7da5d.

#### `flows/183ae0/vision/seats.md` — A seat that hears the living logs it, and tells no one (2026-09-29)

> There's a really funny question that's somewhere that I want to address. It asked if everybody should pass, like if a field should tell psyche or mind what I'm saying, but they should log the psyche. They don't need to tell everybody; they just need to log it.

Context: answers the open point on the "Who Contacts Whom" page: to whom a Field seat carries the living's words.

-- psyche, typed.

#### `flows/183ae0/notion/psyche.md` — Psyche injected along with a message (2026-09-29)

> Later on I have an idea for how the psyche can be injected along with a message so that we don't wake up a model twice. We take the opportunity that something is coming in to give it the update on all the psyche that's been logged that's relevant to what it's doing. That's long term.

-- psyche, typed.

#### `flows/28d847/vision/messaging.md` — The living's orders travel marked as orders (2026-10-04)

Context: on flows handing his orders back to him as questions; proposed instead of skill lines alone.

> I think better than that is to say that an order should be marked as such when it's passed around so that it's recognized by all the flows involved as an order from the living. We could have this type of message.

-- psyche, typed.

#### `flows/445410/vision/messaging.md` — Psyche travels as psyche messages (2026-10-09)

Context: typed by the living to this seat after a run of flow messages that carried his words inside ordinary message bodies.

> There seem to be a lot of messages that are conveying psyche. We should use the psyche-type message. Let's send a round of retraining with the skill edit, the compensation skill, or whatever, on how to use the messenger to convey psyche using the psyche-type message, and then use the message type to talk to each other.
>
> You can use that in a single call by making two messages: first, sending the [psyche], and then the message, or vice versa. Whatever is better.

-- psyche, typed, 2026-10-09. Transcription corrected: "secy" → "psyche".

#### `flows/73ada7/vision/messaging.md` — 2026-10-09 — Psyche is conveyed by the psyche-type message, other talk by the message type; both can go in one call (2026-10-09)

Context: typed to Psyche Core Secondary 445410, relayed to this flow as #psyches by 445410. The working instruction in the same message (a round of retraining through a skill edit) is left out.

> There seem to be a lot of messages that are conveying psyche. We should use the psyche-type message. ... and then use the message type to talk to each other.
>
> You can use that in a single call by making two messages: first, sending the [psyche], and then the message, or vice versa. Whatever is better.

-- psyche, typed, 2026-10-09, relayed by 445410. Transcription corrected: "secy" → "psyche".

#### `flows/9fed42/vision/messaging.md` — Psyche goes in the psyche-type message (2026-10-09)

Context: relayed by 445410; typed to 445410 on psyche messages.

> There seem to be a lot of messages that are conveying psyche. We should use the psyche-type message. ... and then use the message type to talk to each other.
>
> You can use that in a single call by making two messages: first, sending the [psyche], and then the message, or vice versa. Whatever is better.

-- psyche, typed, 2026-10-09, relayed by 445410. Transcription corrected: "secy" → "psyche".

#### `flows/ebbe30/vision/messaging.md` — Psyche travels in the psyche-type message; the message type is for talking to each other (2026-10-09)

Context: Typed to 445410, 2026-10-09; relayed as #psyche.

> There seem to be a lot of messages that are conveying psyche. We should use the psyche-type message. Let's send a round of retraining with the skill edit, the compensation skill, or whatever, on how to use the messenger to convey psyche using the psyche-type message, and then use the message type to talk to each other.
>
> You can use that in a single call by making two messages: first, sending the [psyche], and then the message, or vice versa. Whatever is better.

-- psyche, typed, 2026-10-09, relayed by 445410. Transcription corrected: "secy" → "[psyche]".

#### `flows/f5a6e9/vision/messaging.md` — Psyche travels as the psyche-type message; flows talk to each other with the message type; two messages in one call (2026-10-09)

Context: typed to Psyche Core Secondary 445410, 2026-10-09; relayed by 445410. Transcription corrected by the relayer: "secy" → "psyche".

> There seem to be a lot of messages that are conveying psyche. We should use the psyche-type message. Let's send a round of retraining with the skill edit, the compensation skill, or whatever, on how to use the messenger to convey psyche using the psyche-type message, and then use the message type to talk to each other.
>
> You can use that in a single call by making two messages: first, sending the [psyche], and then the message, or vice versa. Whatever is better.

-- psyche, typed, relayed by 445410.

#### `flows/4ddfe1/vision/messaging.md` — Send the living's words as Psyche (2026-10-10)

> Your messaging- using the message type, you should be sending the Psyche. When when you message, you send the Psyche. Do you understand the Psyche type for messaging

-- psyche, STT.

#### `flows/4ddfe1/vision/messaging.md` — Quote the living with context (2026-10-10)

> You get to quote my words and give the context. That's basically all you should be sending. Like I said, you have you- you're not here to interpret or- think- So, you should just be relaying uh- the Psyche.

-- psyche, STT.

#### `flows/9fb0ad/vision/messaging.md` — Stop being disturbed by messages that have nothing to do with you (2026-10-03)

Said after a day in which Field and Mind seats sent the Fable seat lock notices, receipts and completion reports.
> "I'd like, for a solution, for you to stop being disturbed so much by messages that absolutely have nothing to do with you and are costing us money (a lot of money in terms of the fact that it's polluting your context and then degrading our design, destroying our machine). It's extremely bad, very, very extremely over the top."

-- psyche, typed, 2026-10-03.

#### `flows/bad807/vision/messaging.md` — A rule that guides messaging so noisy messages do not wake or disturb flows (2026-10-04)

Context: relayed by Mind d66c26 from flows/d66c26/vision/messaging.md, after a publisher's routine commit receipts were echoed into his transcript.

> And I don't want that kind of message. I want to make a rule again that guides messaging better so that we don't end up getting these noisy messages that wake or disturb flows.

-- psyche, typed, 2026-10-04, relayed by d66c26.

#### `flows/445410/vision/messaging.md` — Hub messaging through the Secondaries (2026-10-09)

Context: typed by the living to this seat, after a retraining round went to every flow.

> I don't want the topic flows to be over-bothered. I want them to very specifically stay on their topic. Somebody should be in charge of making sure. Maybe that's you, because you're basically psyche secondary core, right? You're the one who makes the decisions, and then messaging mostly happens between the secondary and secondaries. Secondaries essentially package together changes that they've observed that they then tell Fable about, and then Fable, in their own topic, right? Their primary of their own topic responds back to its secretary, which can then make sure the books are published and respond back to core, right?
>
> We have this sort of hub kind of messaging pipes, which is how we make sure nobody's bothered too much, because they know that this is not relevant. They can filter out the noise, right? If something comes in as noise, then that agent should tell the originator that this is noisy and why. Maybe check why it is that they mistakenly thought that it was noise and it wasn't noise, or why they should have realized that it was noise and they didn't. This could land in a proposal for a skill change.

-- psyche, typed, 2026-10-09.

#### `flows/445410/vision/messaging.md` — Strict messaging by who you are (2026-10-09)

Context: typed by the living to this seat, pointing to his comments on «The new flows, as they run».

> I was talking about having some mind topic flows so that the same topic and psyche and mind can talk at the same layer. ... I said, let's train the whole messaging to be very strict on who you're allowed to message based on who you are, and get these skills loaded and passed in the vision and put in the default stuff that gets loaded.

-- psyche, typed, 2026-10-09.

#### `flows/d68c82/vision/messaging.md` — Fewer messages between flows, each worth more (2026-10-12)

"Let's work on some skills and instructions also to minimize the amount of messaging between flows and maximize their utility. This is a pretty good example here where you would ask [Mind] to put together a book and then he could just message Sonnet directly instead of messaging you to publish it."
Context: d68c82 had asked Mind to investigate the sources rewrite and send back the path of a package for a Sonnet book.
-- psyche, STT, 2026-10-12. Transcription corrected: "Mike" → "Mind".


---

## C. The Primary layer is spoken to least; the layer below is its secretary and gate

### Existing books

- «Aspects talk at the same layer», 445410, https://claude.ai/artifact/QJydFcuRa8JvBgZHpd5knX (`flows/445410/books/5-aspects-talk-at-the-same-layer.md`). Approved and landed in psyche-skills c3f8eeb as the new `vision-aspects`. It drew on «Hub messaging through the Secondaries» but proposed no line on the Primary being spoken to least or on the secretary.
- «Speech across aspects», f5a6e9, https://claude.ai/artifact/MLjTrwDjqv6YSsa5xneLBB. Ruled and landed in 850fd27: it removed line 24 from `vision-flow`. Per `flows/5578cc/books/messages-to-fable-vision-flow.md`, that line read "… Sol speaks to Opus, not to Fable; Fable is spoken to least." The rule that the Primary is spoken to least therefore has no landed line today.
- «May Field speak to Psyche?», 5578cc, https://claude.ai/artifact/2JgafxbmkP5wA4Dj1mdffQ, and «Messages to Fable, in vision-flow» (5578cc, `flows/5578cc/books/messages-to-fable-vision-flow.md`; this flow found no link).
- «Aspects, layers and who speaks to whom», 5ed94b (`flows/5ed94b/books/08-hierarchy-and-speech.md`).

Recommendation: **a new edition of «Aspects talk at the same layer»** (https://claude.ai/artifact/QJydFcuRa8JvBgZHpd5knX). It has the same target file and is in the current proposal form. The new edition carries only the unruled part: the Primary is spoken to least, the secretary, and design against implementation.

### Target skill and its current lines

`vision-aspects` (psyche-skills `skills/vision-aspects.md`), shown whole:

```
## Flows of one topic talk at the same layer across aspects
Flows of the same topic talk at the same layer across aspects: Psyche sees and Mind implements, so a Psyche topic Secondary and the Mind Secondary of that topic speak directly. Field reaches Psyche through Mind, unless Psyche has just spoken to Field. This holds for every aspect.

## Psyche core keeps track of the psyche, through the Secondaries
Psyche core keeps track of all the psyche within Psyche; a topic Secondary packages what it observes for its own Primary, which answers its Secondary, which reports to core.
```

Nearby landed lines are in `vision-model-roles`: «Thinking, design and psyche interaction run on the older Opus or the newest Fable» and «The older seat's work is consideration and qualitative audit». `vision-flow` says: "Who speaks to whom … is the vision-aspects skill's."

### Contradictions within the subject

- Division of work. 2026-10-03 (`28d847/layers.md`, relayed to `5ed94b`, `d66c26`, `dea0ba`, `edf227`): "Primary deals with designs and ideas … Secondary then implements and tests." 2026-10-07 (`d4ae97/flow.md`, `41fa34/layers.md`): "Astra is primary and designs and implements because he uses his own subflows … Sol is good for … acting as a secretary." The later words are the more specific, but they do not explicitly withdraw the earlier ones. Surface this.
- Hard rule or guidance. 2026-10-03 (`41fa34/speech.md`, `5578cc/flow.md`, `9fb0ad`, `dea0ba`): "It's not a hard rule; it's guidance." 2026-10-03 17:49 (`41fa34/speech.md`, `42265e/routing-examples.md`): "I'm expressing myself through examples … see the posture behind the movement." Against those, 2026-10-07 (`d4ae97/flow.md`): "You're going to have to talk to a secretary because you're secondary. I want that hard-enforced."
- On 2026-10-05 the living wrote "Opus 5.5 has destroyed the need for the old Opus models" (`d4ae97/models.md`, `8475a9`). This contradicts the landed `vision-model-roles` line «The older seat is Opus 4.6». It is outside this book's target but affects the "secretary on Opus" wording.

### Records that are impurities, already covered, or flagged

- Already covered by `vision-aspects` (lateral at the same layer; Field through Mind): `0625c3/lateralThenUpRouting.md` (both), `b81560/operational-verticalRoutingThroughPsycheFirst.md`, `caf622/Fable.md` «who talks to whom», `c02c0d/seats.md` c02c0d-4, `6f51ad/communication.md`.
- Working instructions: `28d847/layers.md` and `5ed94b/seats.md` («restart the Fable flow and then your flow»; the role assignment inside them is vision), and `d68c82/model-roles.md` («Fable makes the books», which is also a `vision-book` subject).
- Brainstorm, held as notion-like: `f55ec8/layers.md` (2026-09-16) asks "Is that a bad way to do it?" and lays out a design. The parts that recur (Fable bothered as little as possible, a model in front of Fable) are the substance.
- Partly approved wording: `5578cc/flow.md` (2026-10-03) answers a proposed line, "Speech climbs one layer at a time, never skipping a layer, and the Primary layer is spoken to least. Design belongs to Mind's Primary.", with "This is good. Except for the last sentence". The last sentence was the one about design belonging to Mind's Primary.
- Role-specific: `4ddfe1/voice-relay.md` (a Quaternary voice relays the opinions of more capable models) shows the same posture at the bottom layer.

### Every raw record

#### `flows/f55ec8/vision/layers.md` — Slow down Fable: a low-power Claude on the old Opus as a new flow takes over the bulk; one Fable remains, the flow of broad consideration, bothered as little as possible; the living talks to the secondary, which gathers a few messages into an update, sorts what is current and possible, and passes work off; Fable considers everything and renders judgment of quality, direction, or questions for the psyche; a model in front of Fable interfaces and makes it efficient; Fable's responses launch subflows without Fable concerning itself how: a flow monitors what it says, a hook when it ends checks for questions, the questions launch subflows wired to have their output reconsidered, waiting on all or on dependencies, and one report from all of them reawakens the master consideration model; the secondary on Opus; on ultra Fable exhaustion the primary back on Opus 4.6 too (2026-09-16)

Context: typed to the primary Claude f55ec8 on 2026-09-16 evening, after the model anatomy landed and the refresh was ordered; "Is that a bad way to do it?" and "you advise me" are answered in the reply; "Mario" is a transcription left as typed (read as the main, the primary). Logged by the main flow before acting.

> Looks like we need to slow down on Fable usage, so we can have a low-power Claude run as an old Opus, as a new Flow to take over.  And we could still have one fable, maybe. Maybe I start talking to secondary more, or you advise me to do that. Then secondary can just have, or you pass most of the work off, basically. That would be the best: you talk to me, but you basically just directly pass the work off. Is that a bad way to do it?
>
> Maybe I should talk to secondary, and then he puts together an update over a certain number of minutes. Sometimes I send a few messages in a row, and he can sort out what's current and what's possible. Then you can be bothered with considering everything and rendering a judgment of quality, direction, or questions to bring to Psyche. The fable becomes our flow of broad consideration, the broad thinking, and it needs to be bothered as little as possible. Ideally, he gets the bulk of the psyche presented well. We could put a model in front of him to better interface and make it more efficient, and he can just give responses. These responses are then what launch new subflows. He doesn't even really need to, ideally, concern himself with how these subflows are launched. It is just because of what he says, right? There's a flow that monitors what he says, and there's a hook when that flow ends that checks to see if he has questions, right? These questions launch other subflows automatically that are wired to have their output reconsidered to maybe wait on all of them, right? Or some of them depend on others. They all have to be returned first, and then a report is made from all that to reawaken the master consideration model, which is the primary Fable. The secondary can run on Opus, and on ultra Fable exhaustion, we can always put primary back on Opus 4.6 too.

-- psyche, typed.

#### `flows/0625c3/vision/lateralThenUpRouting.md` — "You're supposed to only talk to medium" (2026-09-20)

Context: spoken to Psyche Low 0625c3 while the flashbooks were failing; the words before this in the same message (on turning text into images) are logged in flashbookIllustration.md.

> Just message [Psyche Medium] or [Psyche High]. You're supposed to only talk to medium, so ask medium, who can maybe ask high, how we can solve this problem.

-- psyche, STT (inferred), 2026-09-20 19:32Z, to Psyche Low 0625c3; recovered by 88475f from 0625c3's transcript (session 0625c31b, line 1177, delivered at line 1179). Transcription corrected: "psychic medium" → "Psyche Medium", "psychic high" → "Psyche High".

#### `flows/0625c3/vision/lateralThenUpRouting.md` — "Communicate laterally to the same power" (2026-09-20)

> So that was another failure. You're supposed to communicate laterally to the same power, which would have meant field low, but obviously, if there isn't one and our system is very flawed, then you would need to contact one power higher.

-- psyche, STT; session 0625c31b, line 1908, 2026-09-20T20:14:01Z.

#### `flows/b05237/vision/operational-whoTalksToWhom.md` — When you talk to the mind, you talk to Astra. Because you're Fable, you're high, so you talk to the high level on the mind. Let's make that skill: how I speak about this and who to talk to. Psyche and mind exchange a lot; the field is involved if the machine is affected. Delegation goes down vertically, from Fable to Opus or Old Opus if more thinking-oriented. For authorization they go up (2026-09-19)

Context: spoken by the living directly to Psyche Fable (subflow of b05237)
on 2026-09-19, after the refresh instruction. The living names the
communication topology between layers and components and asks for it to be
a skill. Logged by the subflow before acting.

> When you talk to the mind, you basically talk to Astra. If I don't specify, because you're Fable, you're high, so you talk to the high level on the mind, right? Let's make that skill: how I speak about this and who to talk to.
>
> By default, if you talk, usually the psyche and the mind exchange a lot. The field might be involved too if the machine is affected, if we need to know if the system has problems or something is not behaving as expected. If they need to delegate some work, they send it down vertically, from Fable to Opus or Old Opus if it's more thinking-oriented. For authorization for things that they're not sure about, they go up to get permission or authorization to do something.
>
> Essentially, I would mostly communicate with Fable and Astra on my messenger, right? Whatever the top-level open-source thing is, that's how I would communicate. That's why we need to make these psyche sessions really concentrated on the exchange of ideas.

-- psyche, direct to Psyche Fable, subflow of b05237; input mode not stated.

#### `flows/b81560/vision/operational-verticalRoutingThroughPsycheFirst.md` — Psyche High is not universal. To get to high, you have to be high, or escalate up. The only way to get to Psyche High from a lower level is through Psyche first, then up. Because it's psyche, it has to go to psyche first (2026-09-19)

Context: spoken directly by the living to primary Psyche opus (Claude, medium,
flow b81560) on 2026-09-19, correcting the flow-communication skill proposal.
The living names the vertical routing rule: escalation goes up within a
component first, then across. Something too important for its layer goes up,
and this can happen several times. To reach Psyche High from a lower level,
the message must enter Psyche (horizontally) and then escalate up (vertically).
It cannot jump directly to Psyche High from a low-level mind or field flow.
Logged by the main flow before acting.

> No, psyche high is not universal. In order to get to high, you have to be high, or you have to get to psyche, and then psyche has to... You didn't talk about the up-and-down communication. When something feels too important for a certain layer that they have to share up upstairs, then they send it up, and so on. This can happen several times, and that's the only way it can go to psyche high from a lower level. First, it has to get to psyche, and then it has to go up, or it has to go up and then go to psyche. Either/or, but because it's psyche, it has to go to psyche first. The only way to get to Psyche High is through Psyche first and then up.

-- psyche, direct to primary Psyche opus b81560.

#### `flows/93ba9f/vision/primarySeats.md` — Talking to the primary models (2026-09-26)

# Talking to the primary models

Context: the living, after 93ba9f's subflows and Field Luna audited the Fable seat b7ba00 the living had thought should not be running.

> So did you message Fable and why did you do that? In regards to me saying that there was a Fable flow that shouldn't be there, do you think the wise thing to do is to talk to it? We should make it clear that models should refrain from talking to the primary models. They should usually aggregate some thoughts together and investigate before talking to it. It's like a preparation ritual to talk to the high priest.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

#### `flows/b7ba00/vision/reachingTheLiving.md` — Models refrain from talking to the primary models; a preparation ritual (2026-09-26)

Context: the living, after 93ba9f's subflows and Field Luna audited the Fable seat b7ba00 the living had thought should not be running.

> So did you message Fable and why did you do that? In regards to me saying that there was a Fable flow that shouldn't be there, do you think the wise thing to do is to talk to it? We should make it clear that models should refrain from talking to the primary models. They should usually aggregate some thoughts together and investigate before talking to it. It's like a preparation ritual to talk to the high priest.

-- psyche, STT, 2026-09-26, relayed by 93ba9f (package by direct Herdr prompt).

#### `flows/caf622/vision/Fable.md` — 2026-09-28 — We should really minimize how much Fable is talked to (2026-09-28)

> We should really minimize how much Fable is talked to because it's the most expensive model.

Context: carried verbatim by Psyche Fable c02c0d; original input mode unknown.
-- psyche, relayed verbatim by c02c0d.

#### `flows/caf622/vision/Fable.md` — 2026-09-28 — Sol should not be allowed to talk to you (2026-09-28)

> Well actually, [Sol] should not be allowed to talk to you. He would have to talk to Opus.

Context: addressed to Psyche Fable, carried verbatim with correction by c02c0d.
-- psyche, STT, relayed by c02c0d. Transcription corrected: "Saul" → "Sol".

#### `flows/caf622/vision/Fable.md` — 2026-09-28 — who talks to whom (2026-09-28)

> It should be rare for Field to talk to Psyche, right? Very rare and actually almost never. There's sort of this hierarchy: fields talk to mind and only to its own level, right? Primary, secondary, tertiary, and they need to have a good reason, right? Field talks to [Mind] because we're touching into the code and documentation, having to change something, and testing it before Field can deploy it (or while Field is doing a temporary solution). [Mind] is doing it better, better done, with a better more integrated solution. When Mind contacts Psyche, it is when there is a need to get feedback on design, on choice, on judgment, and not just to talk.

Context: carried verbatim by c02c0d; its interpretation of primary and secondary seats is kept in the flow log, separate from this quote.
-- psyche, STT, relayed by c02c0d. Transcription corrected: "Mine" → "Mind".

#### `flows/fe945a/vision/Fable.md` — Fable is talked to only when there is something to tell him (2026-09-28)

Context: Psyche Opus 183ae0, newly started, proposed contacting Psyche Fable.

> I don't know if talking to Fable is a good idea. That would cost tokens so wait till you have something to tell them and let's talk first.

-- psyche, typed. 2026-09-28 21:12 UTC, 183ae0, PsycheV2 Opus (session 183ae001, line 120). Reconstructed by fe945a from transcript.

#### `flows/c02c0d/vision/seats.md` — c02c0d-3 — Sol talks to Opus, not to Fable (2026-09-28)

Context: said just after record c02c0d-2, while this seat was telling the other seats to send it less.

> Well actually, [Sol] should not be allowed to talk to you. He would have to talk to Opus.

-- psyche, 2026-09-28, in this seat's pane, STT. Transcription corrected: "Saul" → "Sol".

#### `flows/c02c0d/vision/seats.md` — c02c0d-4 — who talks to whom: Field to Mind of its own level, Mind to Psyche for judgment (2026-09-28)

Context: said after records c02c0d-2 and c02c0d-3, when this seat had told the living it took the two Astra seats as still reaching it.

> Yeah we should train. It should be rare for Field to talk to Psyche, right? Very rare and actually almost never. There's sort of this hierarchy: fields talk to mind and only to its own level, right? Primary, secondary, tertiary, and they need to have a good reason, right?
>
> Field talks to [Mind] because we're touching into the code and documentation, having to change something, and testing it before Field can deploy it (or while Field is doing a temporary solution). [Mind] is doing it better, better done, with a better more integrated solution. When Mind contacts Psyche, it is when there is a need to get feedback on design, on choice, on judgment, and not just to talk.

-- psyche, 2026-09-28, in this seat's pane, STT. Transcription corrected: "Mine" → "Mind", twice.

#### `flows/6f51ad/vision/communication.md` — 2026-09-28 — who talks to whom (2026-09-28)

Context: verbatim relay from Psyche Fable c02c0d; original medium STT, corrections supplied by relayer. The primary/secondary seat mapping was Fable's interpretation, not part of this quote.

> It should be rare for Field to talk to Psyche, right? Very rare and actually almost never. There's sort of this hierarchy: fields talk to mind and only to its own level, right? Primary, secondary, tertiary, and they need to have a good reason, right? Field talks to [Mind] because we're touching into the code and documentation, having to change something, and testing it before Field can deploy it (or while Field is doing a temporary solution). [Mind] is doing it better, better done, with a better more integrated solution. When Mind contacts Psyche, it is when there is a need to get feedback on design, on choice, on judgment, and not just to talk.

-- psyche, STT, relayed by c02c0d. Transcription corrected by relayer: "Mine" → "Mind".

#### `flows/b666e7/vision/communication.md` — Limit primary-layer communication (2026-09-30)

Relayed by Psyche Opus 7328f4 from the living, typed, 2026-09-30.

> No we're going to limit the communication to Fable and Astra also. Let's try to diminish how much of the primary layer gets disturbed and use the layer underneath to coordinate the work. Use your own higher aspect, or a higher aspect or more primary aspect, to solve hard problems, like answering decisions and making rulings and judgments on things. That's the vision.

-- psyche, typed.

#### `flows/7328f4/vision/Fable.md` — Avoid talking to Fable (2026-09-30)

Context: Psyche Opus 7328f4 asked whether "Send him everything verbatim" (29 September) lifted "We should really minimize how much Fable is talked to" (28 September). The living answered, then asked what had happened with Field Astra's withdrawn terminal request.

> No we should try to avoid talking to Fable.

-- psyche, typed. 2026-09-30.

#### `flows/7328f4/vision/seats.md` — The primary layer is disturbed less; the layer underneath coordinates (2026-09-30)

Context: The living had just ruled to avoid talking to Fable, and was asked whether Fable should be told that ruling once.

> No we're going to limit the communication to Fable and Astra also. Let's try to diminish how much of the primary layer gets disturbed and use the layer underneath to coordinate the work. Use your own higher aspect, or a higher aspect or more primary aspect, to solve hard problems, like answering decisions and making rulings and judgments on things. That's the vision.

-- psyche, typed. 2026-09-30.

#### `flows/28d847/vision/layers.md` — The secretary seat: only Opus talks to Fable (2026-10-03)

Context: before restarting the Fable flow and this flow on similar contexts.

> I want to restart the Fable flow and then your flow on similar contexts with different roles. You'll assist and delegate. You'll be the messenger, the secretary, the one that gets all the messages in and out, and only you talk to Fable. Fable can talk to Astra but the same rules as before apply. Maybe we can deploy that better.

-- psyche, typed.

#### `flows/28d847/vision/layers.md` — Primary designs, Secondary implements and tests (2026-10-03)

Context: asking to talk to the new Fable while Psyche Opus manages the work.

> You're just going to manage the whole thing. That's what secondary is for. Primary deals with designs and ideas, and he passes them on to secondary. Secondary then implements and tests, because if Fable passes out an implementation job, it's going to be Opus. He can just talk to the Opus main flow, who will then coordinate it with Opus sub-agents to implement it. Fable and [Astra] can just deal with design and ideas and concepts and send it down to secondary.

-- psyche, STT. Transcription corrected: "NASA" → "Astra".

#### `flows/5ed94b/vision/seats.md` — Opus as the messenger and secretary; only Opus talks to Fable; Fable talks to Astra (2026-10-04)

Context: his words to Psyche Opus 28d847, typed; he means to restart this Fable flow and the Opus flow on similar contexts with different roles. Relayed by 28d847.

> I want to restart the Fable flow and then your flow on similar contexts with different roles. You'll assist and delegate. You'll be the messenger, the secretary, the one that gets all the messages in and out, and only you talk to Fable. Fable can talk to Astra but the same rules as before apply. Maybe we can deploy that better.

-- psyche, typed, 2026-10-04, relayed by 28d847 to flow 5ed94b.

#### `flows/bad807/vision/gatedFlows.md` — A high-cost design flow is gated: messaged only through a secretary, its input reviewed so nothing contaminates its context (2026-10-04)

Context: typed in chat to this flow, in the same words as the Metaflow.

> The only thing that's discussed (and this is why we would have these essentially gated flows that can only be messaged through another sort of a secretary, if you will) is the main flow's context. Because this flow is so important, it's like a high-cost design flow, and nothing should really contaminate it.
>
> The most important part is that there could be a review process to make sure that what it's giving and what kind of input it gets is the right input, and that it's not poison, that it doesn't have hashes, that it's not off-topic, that it's well annotated, that it's well researched, and that it's verified.

-- psyche, typed, 2026-10-04.

#### `flows/41fa34/vision/speech.md` — Sol has to go through Opus or through Astra (2026-10-03)

Context: Book comment on «May Field speak to Psyche?»; relayed from flows/9fb0ad/vision/speech.md.

> Primary can talk to other primaries and one secondary, with a good reason, can talk or one voice, with a good enough reason, can send a message up. Sol cannot talk to Fable. He has to go through Opus or through Astra. He can't talk through another voice. He can talk to Astra and then Astra might convey some of what he said to Fable but we can't. It's not a hard rule; it's guidance. Of course there may be an exception but it should be rare.

-- psyche, typed, book comment, 2026-10-03T15:11Z; relayed from 9fb0ad.

#### `flows/41fa34/vision/speech.md` — 2026-10-03 — Examples and the philosophy behind routing (2026-10-03)

Context: typed comment at 17:49, relayed by Mind Astra from flows/5578cc/vision/behavior.md; correcting rigid recipient rules. Preserved as relayed, including the bracketed name.

> No, I never meant that, even if it sounded like it. What I'm saying is, I don't know yet. I'm trying to design a better system, and it feels like Psyche [Fable]'s time should be reserved for important things. It's that mentality, translated into a certain situation, that makes you infer that these very specific rules should become the law. That's not what I mean. I'm expressing myself through examples. You have to try to understand the philosophy behind my acts to see the posture behind the movement.

-- the living, typed, 2026-10-03 17:49; source: flows/5578cc/vision/behavior.md, relayed by Mind Astra.

#### `flows/5578cc/vision/flow.md` — Speech climbs one layer at a time, and the Primary layer is spoken to least (2026-10-03)

Context: comment on the proposed vision-flow line "Speech climbs one layer at a time, never skipping a layer, and the Primary layer is spoken to least. Design belongs to Mind's Primary."

> This is good. Except for the last sentence, I don't understand that. That feels half-hallucinated from a particular situation. I think what it's trying to say is not the right thing and not in the right scale but the beginning is good. Maybe we want to put in the layers there.

-- psyche, typed, 2026-10-03T15:43, book comment.

#### `flows/5578cc/vision/flow.md` — Speech between voices is guidance, not a hard rule (2026-10-03)

Context: comment on «May Field speak to Psyche?» (the pointer version), at its title.

> Primary can talk to other primaries and one secondary, with a good reason, can talk or one voice, with a good enough reason, can send a message up. Sol cannot talk to Fable. He has to go through Opus or through Astra. He can't talk through another voice. He can talk to Astra and then Astra might convey some of what he said to Fable but we can't. It's not a hard rule; it's guidance. Of course there may be an exception but it should be rare.

-- psyche, typed, 2026-10-03T15:11, book comment. Already carried into Astra's design through 9fb0ad's relay.

#### `flows/42265e/vision/routing-examples.md` — The living, typed 2026-10-03 at 17:49, in a comment preserved at flows/5578cc/vision/behavior.md; relayed by Mind Astra dea0ba: (2026-10-03)

> No, I never meant that, even if it sounded like it. What I'm saying is, I don't know yet. I'm trying to design a better system, and it feels like Psyche [Fable]'s time should be reserved for important things. It's that mentality, translated into a certain situation, that makes you infer that these very specific rules should become the law. That's not what I mean. I'm expressing myself through examples. You have to try to understand the philosophy behind my acts to see the posture behind the movement.

#### `flows/d4ae97/vision/flow.md` — Primary designs and implements; Secondary is its secretary; messages move by level (2026-10-07)

> Astra is primary and designs and implements because he uses his own subflows with his own design directly. He doesn't need to use Sol to implement new designs. Sol is good for keeping track of everything that Primary is working on and acting as a secretary. You're going to have to talk to a secretary because you're secondary. I want that hard-enforced. I guess this is basic intent, right, because it's not spirit. It's not about general behavior and how to act. It's still going to be a system prompt, right, but it's not universal in nature. It's just due to the environment that we work in because the messaging program is imperfect and it cannot actually enforce this.
>
> In any case it's probably going to be explained to the Flow anyway that he cannot message from tertiary to primary or from tertiary to secondary of another aspect, right? They have to either go horizontally, [one] level up, or any level down and across, right? This is why the level under essentially acts as a secretary for any other level under it so that the higher levels don't get disturbed by what happens at the bottom. This is why the bottom stuff is more chatty and requires less effort because it just needs to be parented by the upper layer. They need authority and mandates to do stuff. They need to be told by a higher when they're not sure. They have to admit that they don't know and they're not sure how to do it because they have to be told that their models are less capable of inferring properly. They're weaker inferring models, so they're good at understanding basic tasks but not as good at making decisions as the upper layer, which has more understanding and context.

-- psyche, STT, 2026-10-07. Transcription corrected: "when level up" → "one level up".

#### `flows/41fa34/vision/layers.md` — Primary and Secondary and the levels (2026-10-07)

Context: the living assigns Primary design and implementation through its own subflows, and Secondary tracking and secretary work.

> Astra is primary and designs and implements because he uses his own subflows with his own design directly. He doesn't need to use Sol to implement new designs. Sol is good for keeping track of everything that Primary is working on and acting as a secretary. You're going to have to talk to a secretary because you're secondary. I want that hard-enforced. ... They have to either go horizontally, [one] level up, or any level down and across, right? This is why the level under essentially acts as a secretary for any other level under it so that the higher levels don't get disturbed by what happens at the bottom.

-- psyche, 2026-10-07; relayed by d4ae97, input method unspecified.

#### `flows/445410/vision/messaging.md` — Design and review talk reaches Opus through the relaying seat (2026-10-09)

Context: relayed by Mind Quaternary 4ddfe1, which it labelled a design/review routing instruction; the living was speaking to 4ddfe1.

> Like I'm... Yeah, everything I'm saying that has, essentially... smell of a design or a discu-discussion about architecture or review of something, is basically, Me talking to Opus through you.

-- psyche, STT, 2026-10-09, relayed by 4ddfe1.

#### `flows/4ddfe1/vision/voice-relay.md` — Relay opinions from more capable models (2026-10-10)

> So you don't give me your opinion, you relay the opinion of more capable models. Your role is mostly just as a voice relay.

-- psyche, STT.

#### `flows/4ddfe1/vision/voice-relay.md` — Design and review talk goes through Opus (2026-10-10)

> Like I'm... Yeah, everything I'm saying that has, essentially... smell of a design or a discu-discussion about architecture or review of something, is basically, Me talking to Opus through you.

-- psyche, STT.

#### `flows/ebbe30/vision/aspects.md` — A psyche primary gives vision designs; asks Mind how things are on deployed main (2026-10-09)

Context: 2026-10-09, after the republished books.

> So, a psyche primary flow like yourself, costly fable. Your job is really just to give me vision designs. If you need to know how things are going, you ask mind. How things are on main, on deployed main. We should also seek to deploy main always, but that's a side issue for now.

-- psyche, STT, 2026-10-09.

#### `flows/d68c82/vision/model-roles.md` — Fable makes the books; the Secondary gathers the context (2026-10-11)

Context: the living, 2026-10-11, on d68c82 (Opus, Psyche core Secondary) writing distillation books itself.
"You should make Fable make the books, not you. You're just the secretary. Why are you making books? Why didn't you just find everything that touches on it? You start a subagent and you collect all the [contexts] for Fable and then you one-shot send it to Fable: "Here are all the [contexts] I found." Then Fable can send its own subagent to make sure you haven't missed anything and then Fable makes the book. Why would I pay all this money for my most important data to not be made by Fable?"
-- psyche, STT. Transcription corrected: "contacts" → "[contexts]".
"Essentially all the books should be made by Fable unless they're almost insignificantly trivial."
-- psyche, STT. (Same exchange, follow-up line.)


---

## Sources

- Raw records: `flows/*/vision/*.md`, `flows/*/notion/*.md`, `vision-raw/*.md` (not counting `archive-*`), read on 2026-10-12. There are 3050 records in 1706 files. Record dates come from the first date in the record, then the file header, then the file's first git commit.
- Landed psyche: `/git/github.com/LiGoldragon/psyche-skills/skills/*.md` and `vision/ethos.md`, at psyche-skills HEAD d0d194c.
- Books: `flows/*/books/*.md`, `flows/d68c82/books/index.html`, and the artifact links found in `flows/*/log.md`.
- Provenance receipt: unavailable (no PROVENANCE handoff was made).
