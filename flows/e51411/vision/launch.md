# Launch

## A fresh flow starts from one prompt, with /main-flow in it

Context: said to Psyche Medium e51411 after it corrected who sent `/main-flow`. The launcher had sent `/main-flow` as a second prompt after the first one, because the harness does not let the model load it through the Skill tool.

> Well the real mistake was that the /main flow should have been in there. There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411. Reading note (inference): "the /main flow" is `/main-flow`, and "in there" is the first prompt.

## Skill commands belong in the original prompt; several /skill commands in one Claude prompt have worked

Context: follows the entry above. This seat had said that probably only a leading slash command expands in Claude.

> So the command should have been in the original prompt. Is there a problem with putting a bunch of skill commands in the Claude initial prompt, because there isn't in Codex?

> Well I was putting in the /skill command style in Claude for a long time and it was working. Do you want to test this with a haiku model or something?

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411, two consecutive messages. Tested afterward; see flows/e51411/reports/multi-skill-first-prompt.md and one-block-startup-prompt.md.

## A flow's ID is claimed for it by code as it starts, not by the flow or a subflow

> We should not make it the subflow's job to claim an ID. That should be done for the flow as it started. There's no reason. This could easily be done by code.

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411.

## Launch prompts are lean: not too much prompt, no hashes

> Let's refresh Psyche High and see how it went. ... Let's do a better job of it. Let's not give them too much prompt. Let's make sure there are no hashes, garbage, and stuff like that in there.

-- living, input mode not established, 2026-09-24 16:22:52, to Field Medium 9ddcbc; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).

## Skill order doesn't matter; everything comes in as one block

> It really doesn't matter if Spirit or Mainflow comes first. Why do you care?

> All that matters is that everything comes in as one block.

-- living, input mode not established, 2026-09-24 20:21:13 and 20:21:30, to Field Astra 5f38bc; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).

## Reword the invariant

> Yeah you should reword that of course.

-- psyche, typed, 2026-09-24, to Psyche Opus e51411; reconstructed from the transcript by 752e0f from d8df70's audit, transcript line 470.

## Every flow is started with dangerously-skip-permissions

Context: this seat had reported that Claude's auto-mode safety check allowed the Prometheus deploy only from d8df70's seat and had refused the launch of two Field seats.

> I don't understand the problem. Your all [sic] flows should be started with `dangerously skip permissions` so you weren't launched properly, so get relaunched.

-- psyche, STT (inferred), 2026-09-24 20:46Z, to Psyche Medium e51411; recovered by 88475f from e51411's transcript (session e5141130, line 1181). "Your all" kept [sic]; read as "all of you flows" (inference).

## The Flow tool's anatomy: one complex central Start call, plus shorthands for preconfigured minimal calls; the same pattern for every main feature

> Let's look at the anatomy, the ethos of this Flow tool. It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed. We like this idea of having these shorthands, I call them. I don't know if there's a canonical way to name them in the industry.
>
> Let's look at the anatomy, design it better, and make this complex central call, which, for any main function or any main feature, is what we would do. Let's get the pattern out of this into a vision that I'll review and let's start distilling more vision, more intent, more spirit, and even Notion. Let's clean up our data and when the mind is not busy it can start looking at doing the anatomy of psyche and mind and intent and ethos and doing some datom syntax examples, like proposal, as proposal, operation type, knowledge, or not operation but concept.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.

## Merge the vision and the skills; move Spirit and Vision into the system prompt; the prompt is maxing out

> You can maybe work with the new Fable when you get it started on developing this vocabulary better and all of this anatomy and ontology of all the components. That will be its first task and you can modify the Hacky tool to change the system prompt and put our spirit and stuff there and our vision. The stuff that's not in skills, we need to merge the vision and the skills. We need to make it more efficient. See we're maxing out the prompt now.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.

## Start with compensation skills; one documents the HM tools, is kept current, and is linked from the tool; HM gets its own repository, HackingMessenger

> We have an operational skill that teaches an operation skill or a compensation skill, more on the field side, or we should anyway. We can start with compensation. Do we have a compensation skill that documents how to use this HM panoply of tools and keeps it up? We need to keep it updated so we need to link it in the tool.
>
> You can make a repo for this HM or Hacking Messenger. Just call it Hacking Messenger in Pascal case and/or Hacking Message. Whatever it was, Hacking Messenger.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.

## HackingMessenger in Clojure: an object-oriented version of our Rust approach, typed with Malli; anatomy first; Sol writes it, then an audit

> Try to create an object-oriented version of our Rust approach. See how much we want to emulate. Typing using types with [Malli] is what we should do. Maybe you can rethink the whole anatomy first. Get Sol to write it and then audit it. It's this new [Clojure] version. What is it written in now?

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411. Transcription corrected: "Mali" → "Malli", "closure" → "Clojure".

## Not "Hacking": the repository is HackyMessenger, restarted on fresh history with no trace of "Hacking"

> No, not [hacking]. If that's the name, then the git has to be restarted on a fresh copy where all the names have been changed so there's no trace of that name in the history. That is a really bad name.

> HACKY not HACKING.

-- living, 2026-09-25, to Psyche Medium e51411; the first message by speech, the second typed. Transcription corrected: "hacky" → "hacking" in the first, per the living's typed second message. The earlier "Hacking Messenger" naming, which this seat followed, was itself a speech-to-text rendering of "Hacky Messenger".

## A new job starts on a fresh flow

> Yeah well, if his context is old and he's not going to be able to do a good job, when we start something like that we should start on a fresh flow with lots of related training.

-- psyche, STT, 2026-09-25, to e51411, on moving the Flow 0.7 deploy from Field Astra to Field Sol.

## The default effort is medium

Context: e51411 had launched the Psyche Sonnet companion 9c7514 at low effort, on its own choice.

> Well why is it on low effort? The default effort is medium. Why is it on low effort?

-- psyche, input mode not established, 2026-09-26 00:41Z, to Psyche Medium e51411; reconstructed from transcript by da88cf's psyche-recovery subflow (Claude session e5141130-9a4a-4b8f-b405-67d941a7b320, line 5932). The next entry, one minute later, is the living's clarification that "low" names Sonnet's power.

## "Low" is a power, not an effort

> No Sonnet is low-powered. I didn't say low effort. Low corresponds with Sonnet. You don't have that training. We need to fix that training because you don't understand what I mean by low then.

-- psyche, STT, 2026-09-25, to e51411, on e51411 launching the companion at low effort.
