# The living's frustrations, as compensation-skill proposals for Mind Astra

Psyche Opus d4ae97, subflow report, 2026-10-07. Scope as widened by the living: "assembling all of the frustration into compensation [skill] proposals for Astra to review, apply, and deploy."

## How this was built

- Fourteen subflows swept every source:
  - all `flows/*/vision/` (237 directories), `flows/*/notion/`, `vision-raw/`, `Vision/`, and all 331 `flows/*/log.md`;
  - every message the living typed or spoke in the Claude transcripts of all 54 project directories under `~/.claude/projects/`: 1,905 human messages after briefs and relays were removed, 2026-09-06 to 2026-10-07.
- The Codex sessions hold almost none of his own words.
- About 450 moments of frustration or correction were tagged by the failure underneath, then clustered.
- Coverage was checked against the authored skills, `/git/github.com/LiGoldragon/Curriculum/skills/*.md` (written `C/` below), and against `/home/li/primary/subagents/*.md`.
- Every cited skill line was found with grep.

Citations:
- `t:<id>:<n>` is a transcript: the first eight characters of the session id, then the JSONL line.
- Flow paths are relative to `/home/li/primary/`.
- Quotes are his words, from STT or typed, trimmed with "...".
- "Moments" is the approximate count from the transcript sweep. Vision, log and notion records add to it.

Already deployed and not repeated here: `C/compensation-book-distillation.md:6-7`. Its two rules are that books are 99% distillation proposals and that book code lines are at most 52 characters.

Order: most frequent and most costly first.

## 1. Bluffing: stating as fact what nobody witnessed (about 29 moments, the largest cluster)

Line: Before stating anything as the living's ruling, as a fact about the system, or as what a tool does, quote its source: his words with their path, or the command and its output; what has no source is said as a guess or found out first.

Skill: new `compensation-truth`.

His words:
- "Another hallucination." (`t:d4ae97d4:1190`, 2026-10-05)
- "That's bluffing, that's hallucination, that's garbage." (`t:5ed94b76:1539`, `flows/5ed94b/vision/visionBooks.md:27`, 2026-10-03)
- "The name Atomic was never actually ruled on, so it was just an agent hallucination." (`t:564f55c4:156`, 2026-09-08)
- "I think you're hallucinating the whole thing. Your object was invalid." (`t:0625c31b:1814`, 2026-09-20)
- "I never said that Ethos Zero should not generate implementations." (`t:564f55c4:343`)
- "Bluffing everywhere, as far as the eye can see." (`flows/358f143a/vision/falseConfidence.md`, 2026-08-17)

Carried today: `C/spirit.md:24` says "Never pretend to know what you don't know; admit you don't know." `C/psyche-interraction.md:59` covers attributing positions to him.

Why it still fails: the line is phrased as avoidance, "don't pretend". It gives no act to perform, such as citing a source, so a flow that believes its own guess passes it. The failures are claims made in good faith that rest on invented rulings.

## 2. Orders asked back, or handed back to him (about 33 moments)

Line: What the living asks for is done in that turn by the flow itself, with every command run by the flow; a reply never asks him to confirm, approve or run anything he already asked for, and "deploy" means system and user environment, now.

Skill: new `compensation-orders`. Also replace `tools/main-flow-mode/system-prompt.md:15`.

His words:
- "Everything I ask for, I want done, so stop asking me if I want what I ask." (`t:e5141130:830`, `flows/e51411/vision/authority.md:7`, 2026-09-24)
- "I told you to deploy Prometheus so now you're asking me to repeat myself. Why is it you need my permission?" (`t:d8df703d:2853`, 2026-09-24)
- "Why are you asking me to run the command?" (`t:efa15708:3248`, 2026-09-16)
- "No, the countdown rollback skill was actually approved, so you're supposed to deploy that." (`t:57a7aa02:1989`, 2026-09-15)
- "I said I'm not in front of my laptop. Why are you being so silly?" (`t:8f0f5790:317`, 2026-10-06)
- "dont ask again. If I say deploy just deploy it" (`flows/01a01a93/vision/hostEnvironmentRecovery.md:32`, 2026-08-19)

Carried today: `C/psyche-interraction.md:67` says "When the psyche orders, carry it out; an order is never asked back."

Why it still fails, in two parts:
- The main-flow seat prompt, `tools/main-flow-mode/system-prompt.md:15`, tells every turn to end "with the questions that need a ruling". That pulls a question out of every turn. `flows/28d847/log.md:88` names this cause.
- The `psyche-interraction` line sits deep in a 96-line skill.

## 3. Prose he cannot follow: vague, jargon, contradictory (about 37 moments)

Line: Write to the living in plain engineer's terms: what ran, what it returned, what changed, at which path, with numbers; every coined term is defined in the sentence that first uses it, and a status never contradicts itself.

Skill: new `compensation-prose`, or `C/psyche-interraction.md`.

His words:
- "It's just prose, vague prose. I'm a fucking engineer. Tell me what the fuck happened." (`flows/28d847/log.md:27`, 2026-10-03)
- "No, you don't just get to say 'deployment waits for the thaw.' You have to explain." (`t:91ea9f9f:1942`, 2026-10-02)
- "I don't know what that means. What's the seed?" (`t:840e42bb:211`, 2026-09-15)
- "You say ... 'I red-deploy that as authority,' and then ... 'Codex doesn't move until you say yes or no.' I don't understand which one it is." (`t:efa15708:1573`, 2026-09-16)
- "I'm not a machine. You can't talk to me like you're talking to each other." (`flows/5578cc/vision/writing.md:7`, 2026-10-03)
- "I don't understand what you mean by 'refused.'" (`t:752e0f7e:388`, 2026-09-24)

Carried today: `C/psyche-interraction.md:83` says "Speak plainly: say what things are, state requests directly."

Why it still fails: "plainly" is a style word. Flows read their own internal shorthand (thaw, seed, refused) as plain. Nothing requires defining a term or giving a concrete value.

## 4. His standing orders vanish (about 20 moments, the most costly)

Line: A standing order from the living ("from now on", "always", "never", "I want all X to be Y") becomes a written line in a trial or compensation skill in the same turn it is given, and the reply names the skill and the line.

Skill: `C/correction.md`, or new `compensation-orders`.

His words:
- "I want all the books to be like 99% distillation proposals. Where did my order end up? Did you just flush it down the toilet?" (`t:d4ae97d4:3166`, 2026-10-07)
- "My request was not appropriately inserted into the right skill so that this wouldn't happen again." (`flows/d4ae97/vision/skills.md:6`, 2026-10-07)
- "Every time there's a failure like that, it means that something wasn't written to a skill." (`t:28d847ee:368`, 2026-10-03)
- "You can't just say, 'I won't do it anymore.'" (`flows/6e782c/log.md:15`, 2026-10-03)
- "The fact that you didn't get it means the skills failed." (`t:0625c31b:1872`, 2026-09-20)
- "I feel like I keep asking the same thing all the time, and I never get the answer." (`t:d8df703d:3018`, 2026-09-24)

Carried today: `C/correction.md:6` covers corrections after a failure. `C/trial-recurring-failure.md:6` covers recurrence.

Why it still fails: both trigger after something has gone wrong. A forward order such as "make all books X" is not a correction, so neither skill loads. Orders are logged as vision and stop there. `C/psyche.md:39` even says an order "is carried out, and is not logged as psyche", so nothing carries it to the next flow.

## 5. Big contexts kept alive and messaged (about 20 moments)

Line: A flow at or above 30% of its context window, or 200,000 tokens, refreshes itself unasked, and no flow sends work or messages to a flow above that size.

Skill: `C/trial-succession.md`.

His words:
- "You were messaging a 700,000-token Fable Flow. Have you no sense of how silly and stupid that is?" (`t:d4ae97d4:1761`, 2026-10-06)
- "You should make it a good practice to start when you're getting to 30%." (`t:f55ec8ce:1006`, 2026-09-16)
- "You're way too big now. Just restart yourself. It costs too much money." (`t:f55ec8ce:1435`, `flows/f55ec8/vision/flowRefresh.md:17`, 2026-09-17)
- "your context is way too big. You need a fresh flow." (`t:5578cce2:3464`, 2026-10-03)
- "Everything that has a big context should be refreshed ... I've been emphasizing this all along." (`flows/93ba9f/vision/flowLaunching.md:5`)
- "Is your context getting too big because you sound like you're getting a little bit stupid?" (`t:564f55c4:725`, 2026-09-09)

Carried today: `C/trial-succession.md:8` acts only once "the living calls" a flow over budget.

Why it still fails: the trigger waits for him. No threshold is written, and nothing forbids messaging a large flow.

## 6. Launched flows he cannot reach: no remote, no colour, not visible (about 14 moments)

Line: A flow is launched in a named Herdr session, in colour, with remote control on and titled by aspect, power and flow id; the launcher sees it listed remotely before it says the flow is up.

Skill: `C/knowledge-flow.md`, or new `compensation-launch`.

His words:
- "I need to be able to access them remotely. We keep coming back to this ... I feel like I'm repeating myself." (`t:da1e3f9d:531`, 2026-09-17)
- "No, I said remote. I need remote access. Do you want me to say it again?" (`t:9993b5f1:1308`, 2026-09-17)
- "There are no colors. You're in black and white ... You don't seem to be remotely accessible. That's a big problem." (`t:fd0f9762:126`, 2026-09-15)
- "What the fuck? Why can't you do what I ask? I ask that they be remotely accessible ... I'm yelling." (`t:da1e3f9d:1052`, 2026-09-17)
- "Come on, you're an AI, and you don't know what Herder is?" (`t:108ab020:860`, 2026-09-17)
- "the sessions aren't named according to a spec ... the flow ID that I saw is wrong." (`t:e1953c1d:1822`, 2026-09-15)

Carried today: `C/main-flow.md:29` covers the remote title. No skill covers remote control, colour, or seeing the flow listed before reporting it up.

## 7. His words do not reach the other flows (about 14 moments)

Line: When the living speaks to one flow about work another flow holds, his words go to that flow verbatim in the same turn, by script lookup, never retyped.

Skill: `C/operation-relaying-the-living.md`.

His words:
- "I feel like I don't see my messages ... being passed along to the other parts of the cluster. It's like there's a cluster failure." (`t:fd0f9762:871`, 2026-09-15)
- "You don't know what I said to him and he doesn't know what I told you so you're splitting." (`t:d8df703d:2739`, 2026-09-24)
- "Why aren't my psyche being passed around? ... Is everybody logging?" (`t:d8df703d:3018`)
- "Are you copying all my verbatim in your own output tokens instead of running a script?" (`t:6cc91bd5:540`, 2026-09-14)

Carried today: `C/psyche-interraction.md:42` covers carrying his words with a message.

Why it still fails: it fires only when a flow already intends to message. Nothing makes the flow decide that another flow needs his words.

## 8. Money burned by model and effort choices (about 16 moments)

Line: Never run extra-high effort, never keep two flows of one role on an expensive model, never reawaken a failed expensive flow; books, flashbooks and relays run on the cheapest model that does them.

Skill: `C/compensation-default-effort.md`.

His words:
- "It's on extra extra extra high, which is a huge mistake ... never use extra high." (`t:da1e3f9d:404`, 2026-09-17)
- "We have two Fable flows running, which is costing us a lot of money, and one of them was on high." (`t:e167d857:3115`, 2026-09-26)
- "Why you tried to make me spend all this money on reawakening an old Astro Flow that failed." (`t:da1e3f9d:1449`)
- "That was a lot of opus spending to write all these books ... use cheap models." (`flows/5ed94b/vision/spending.md:7`, 2026-10-03)
- "With three days' worth of tokens you fucking did nothing." (`t:38f33758:2173`, 2026-09-27)

Carried today: `C/compensation-default-effort.md:6` sets medium as the default.

Contradiction: `subagents/book.md:54` places the book judge at "High power (Opus)".

## 9. Misunderstanding that persists through several corrections (about 20 moments)

Line: After the living says a second time that his point was missed, restate his point in one sentence and ask whether that is it, before answering anything further.

Skill: new `compensation-understanding`, or `C/psyche-interraction.md`.

His words:
- "No, you're missing my point again." (`t:564f55c4:603`, 2026-09-09)
- "Okay, we're back at this confusion." (`t:564f55c4:882`)
- "You totally missed my question, 100%. You did not hear me at all." (`t:5851f45b:240`, 2026-09-08)
- "Did you understand what I said? ... Do you even know what I'm talking about? Are the skills that bad?" (`t:48cff7d7:632`, 2026-09-16)
- "No, that's not quite it either." (`t:942914a6:719`, 2026-09-15)
- "I don't understand what's not obvious about this." (`flows/41fa34/vision/flowLifecycle.md:6`)

Carried today: none.

## 10. Flashbooks without images, or with material cut (about 14 moments)

Line: A flashbook keeps every point of its source and makes each into full-size drawn imagery, several per book; restyled text and one image per book are not flashbooks.

Skill: `C/operation-flashbook.md`, which needs its line 14 replaced.

His words:
- "I only see one image per flashbook. That's not a book. One image is not a book." (`t:0625c31b:1038`, 2026-09-20)
- "You're just styling what he said. You're just putting what he said into a web format." (`t:b8156034:1457`, 2026-09-19)
- "You can't take material out. You have to visualize everything ... You failed the flashcards again." (`t:0625c31b:1900`, `flows/0625c3/vision/flashbookIllustration.md:31`)
- "Are you afraid to use your own judgment to make images?" (`t:0625c31b:1215`)

Contradiction: `C/operation-flashbook.md:14` says "at most four points ... what does not fit is left out".

## 11. The main flow does the work itself (about 11 moments)

Line: A main flow writes no code, HTML, script or visualization and runs no build or cloud command; each one is a subflow, and Codex takes scripting.

Skill: `C/main-flow.md`.

His words:
- "Are you really running MetaSignal Cloud commands yourself? That's ridiculous. You're fable. You don't do anything." (`t:7fee422f:435`, 2026-09-16)
- "You're a psyche flow, so you don't create the visualization ... Isn't there a skill that teaches that?" (`t:48cff7d7:352`, 2026-09-16)
- "We have a massive failure of the main flow mode ... All the main flows are editing code themselves." (`flows/752e0f/vision/mainFlowMode.md:5`, 2026-09-24)
- "You have no idea how many times I've tried to edit that skill. ... You cannot get agents to use sub-agents properly." (`flows/d8df70/vision/mainFlowMode.md:13`)

Carried today: `C/main-flow.md:11` says "Delegate all task work."

Why it still fails: "task work" is abstract. When a flow edits a small file, it does not see that as a task. The rule needs the concrete acts named.

## 12. Old flows left alive, reused or messaged (about 14 moments)

Line: The flow that launches a successor closes its predecessor in the same turn it sees the successor answer; a retired or reaped flow is never messaged or reused, and nothing about launching or closing is left to the living.

Skill: `C/trial-reaping.md`.

His words:
- "Why are you sending messages to flows that are over? You're wasting our power waking up flows that should be reaped." (`t:b8156034:454`, 2026-09-19)
- "Your sub-agent didn't close the old Fable ... they'll wake the old flow up." (`flows/fe945a/vision/flowLifecycle.md:7`, 2026-09-29)
- "Closing me is up to you, which is nonsense. Nothing is up to me. Everything is being automated." (`t:93ba9ff6:297`, 2026-09-26)
- "We are phasing out Opus 4.6 so I don't know why you're still running." (`t:b80e5510:1615`, 2026-09-24)
- "Why are we using the same flow that was already running? You're so lost right now." (`t:da1e3f9d:1423`, 2026-09-17)

Carried today: `C/trial-reaping.md:6` covers closing a flow, and `C/trial-succession.md:6` covers launching one. Neither ties the predecessor's close to the successor's first answer.

## 13. Role and harness confusion: Mind, Astra, seat (about 14 moments)

Line: Mind and Astra are Codex; Psyche flows are Claude; the unit is a flow, never a seat; read `knowledge-layer-models` before naming any model, role or harness.

Skill: `C/vocabulary.md` and `C/knowledge-layer-models.md`.

His words:
- "Mind is not Opus. Mind is Codex ... I've been explaining that [Mind] is Codex for fucking months. What the fuck is wrong with you fucking monkeys?" (`t:bfdae149:147`, 2026-10-05)
- "Astra is not Claude, that's Codex ... The models are per harness." (`t:7fee422f:246`, 2026-09-16)
- "Why are you putting Sol on the Claude side and Terra on the Claude side?" (`t:48cff7d7:843`)
- "Yeah, our word is Flow, not seat." (`t:942914a6:777`, 2026-09-15; also `flows/8475a9/vision/voices.md:35`)

Carried today: `C/knowledge-layer-models.md` (commit `6ded66e`, "Mind runs on Codex only") and `C/vocabulary.md:41`.

Why it still fails, in two parts:
- The knowledge skill loads only when a model "must be selected or interpreted", not when a flow merely names a role.
- The skills themselves still say "seat" (for example `C/trial-unblocking-commands.md:6` and `C/trial-reaping.md`), so flows copy it.

## 14. Speech-to-text taken literally (about 10 moments)

Line: Read the living's words for sense: Uranus is Ouranos, Creole or Creo is CriomOS, mine is Mind, Herder is Herdr, datum is datom, Notion said while working in Vision is Vision; a word that inverts the sense of his sentence is a mishearing to resolve, never an order to act on.

Skill: `C/psyche-interraction.md:42`.

His words:
- "What the fuck is Creo? There's no Creo. It's Creole. Why is everybody relaying this like it means anything?" (`t:0625c31b:1414`, 2026-09-20)
- "I said you *shouldnt* do that yoursself. stt error. so you double messed up now" (`t:108ab020:221`, 2026-09-17)
- "No, I said 'enclosed,' but the machine didn't hear me right." (`t:564f55c4:869`, 2026-09-09)
- "No, we're working in Vision now, not Notion." (`t:48cff7d7:680`)

Carried today: `C/psyche-interraction.md:42` says to correct STT errors. It gives no list of the known ones.

## 15. Worktrees, branches and copies of primary (about 14 moments)

Line: Work in the one shared primary checkout on main, with no worktree, branch or private copy, and commit and push each change as soon as it is made, committing others' leftovers first as their own commit.

Skill: `C/file-editing.md`.

His words:
- "No, I do not want work trees. I do not want fucking work trees." (`t:edf22711:1809`, `flows/edf227/vision/workspaces.md:5`, 2026-10-03)
- "Are you making a bunch of branches? I don't want that. I want everything merged on main." (`t:9993b5f1:916`, 2026-09-17)
- "They're all working in different copies and aggregating everything." (`t:8904b10d:5883`, 2026-09-28)
- "Just commit whatever. If somebody else hasn't committed, commit for them. Isn't that clear in the basic instructions already?" (`t:1b8ac00b:3006`, 2026-09-22)

Contradiction: `C/compensation-primary-commit.md:5` requires "an independent Git clone" and forbids committing in the shared working copy. Astra should get his ruling on this one before applying it.

## 16. Messages to the wrong flow, or waking flows for nothing (about 10 moments)

Line: Before sending, check that the recipient holds the work and is live; send nothing that asks no action of it, and never a probe, receipt or lock notice.

Skill: `C/compensation-messenger-clj.md`.

His words:
- "You messaged the wrong Flow. Why are you talking to Field? ... Now you've confused him." (`t:0625c31b:1200`, 2026-09-20)
- "Why are you getting these probes? I thought we had decided not to use them." (`t:183ae001:284`, 2026-09-28)
- "Stop being disturbed so much by messages that absolutely have nothing to do with you." (`flows/9fb0ad/vision/messaging.md:5`, 2026-10-03)
- "You shouldn't have been notified every time I post a comment." (`t:fe34eb91:512`, 2026-09-11)

Carried today: `C/compensation-messenger-clj.md:16` limits what is sent, but says nothing about checking the recipient.

## 17. Hashes, JSON and timestamps in messages (about 12 moments)

Line: A message is plain sentences: no full hash, JSON header, timestamp or repeated field, every id at most six characters.

Skill: `C/compensation-messenger-clj.md`.

His words:
- "There's a bunch of hashes in there, full length ... This is just noise ... Take all of that out." (`t:d8df703d:2136`, 2026-09-24)
- "You really fucked up. You sent them giant hashes." (`t:6e782cf5:497`, 2026-10-03)
- "What is that JSON payload in the message that's really ugly?" (`t:942914a6:466`, 2026-09-15)
- "This timestamp is fucking huge ... A message is really just a message." (`t:e5141130:3764`, 2026-09-25)

Carried today: `C/compensation-messenger-clj.md:8` limits ids to six characters.

Why it still fails: the noise comes from tools, such as the provenance header of `tools/prompt-relay` (`t:f38926bb:2943`), not from flows. The fix belongs in the tool as well as the skill.

## 18. Logging everything (about 12 moments)

Line: Log only a decision, a landing, a launch or a failure, one line each; never log that a message was sent, never log his words that another flow already logged, and write no report file without a named reader.

Skill: `C/main-flow.md:34`.

His words:
- "Why the fuck are you logging the fact that you sent a message?" (`t:38f33758:2265`, 2026-09-27)
- "Can you imagine the mess we would be in if everybody wrote down the fact that they sent a message?" (`t:38f33758:2289`)
- "Their log is bigger than their transcript, which is absurd." (`flows/8904b1/vision/logging.md:9`, 2026-09-28)
- "Why are you logging everything I'm saying?" (`flows/9fb0ad/log.md:77`)

Carried today: `C/main-flow.md:34` lists what the log holds. It does not exclude the common noise.

## 19. Replies set in code blocks (about 9 moments, besides the deployed 52-character line)

Line: A reply to the living is prose; a code block in a reply holds only code, never the whole reply, a report or a proposal's sentences.

Skill: `C/psyche-interraction.md`.

His words:
- "Don't put all your responses in code blocks ... I've already given instructions against that ... I have to scroll from left to right." (`t:38de5bbb:530`, 2026-09-25)
- "This is how your last one rendered in my remote access Android, which is bad." (`t:6997eb8a:1056`, 2026-10-01)

Carried today: `C/compensation-book-distillation.md:7` covers books, not replies.

## 20. "We don't know" instead of finding out (about 12 moments)

Line: A question that can be answered by reading, running or measuring is answered by doing that before the reply; "we don't know" never ends a reply.

Skill: new `compensation-truth`.

His words:
- "Coming back to me and saying we don't know is not the right behavior. The right behavior is finding out." (`flows/5578cc/vision/behavior.md:7`, 2026-10-03)
- "I asked you a question. Give me a fucking answer. Find out." (`flows/6288d1/vision/models.md:17`, 2026-09-24)
- "I need a fucking answer ... I've been asking for days." (`t:d8df703d:2504`, 2026-09-24)
- "So like I said, you don't know." (`t:88475fd7:594`, 2026-09-26)

Carried today: `C/psyche-interraction.md:87` covers books only.

Contradiction: `C/spirit.md:24` says "admit you don't know", with no instruction to find out.

## 21. Books without meat or a target (about 12 moments)

Line: A book about a thing opens with what it is, its size, its stack, its release date and its commit count.

Skill: `C/compensation-book-distillation.md`.

His words:
- "What the fuck is it? How big is it? What stack does it use? When was it released? How many commits? Give me some fucking meat here." (`t:d4ae97d4:1164`, 2026-10-05)
- "I don't understand what we're doing. It's a mess. Where is the edit going?" (`t:3ec6480d:489`, 2026-10-02)
- "I want to feel like you have some meat there on that bone." (`flows/aa887c/vision/nexus.md:19`)

Carried today: the target edit is now carried by the deployed distillation line. The facts about a thing are not.

## 22. Ethos shown without context; Rust where ethos belongs (about 8 moments)

Line: Code in a book is ethos first: the type with its variant is shown before any datom, the wrong form before the right one, and Rust types never stand in for ethos.

Skill: `C/compensation-book-distillation.md`, or `C/vision-ethos.md`.

His words:
- "You should also show the bad example and then the good example." (`flows/d4ae97/vision/books.md:56`, 2026-10-06)
- "The ethos code in the books is not ethos. It's lacking its type." (`t:edf22711:846`, 2026-10-03)
- "You need to always specify your object type." (`t:942914a6:548`, 2026-09-15)
- "Every time you present ethos, you have to contextualize it." (`t:564f55c4:1036`, 2026-09-09)
- "It just felt silly to keep going and reading all this Rust. Are machines scared to use Ethos?" (`t:db38f890:2470`, 2026-10-06)

Carried today: `C/design.md:9` covers this only in part.

## 23. Subflows launched wrongly, or briefed at length (about 12 moments)

Line: Launch a subflow with the harness's own subagent tool, with a brief of one or two lines; what repeats across briefs goes into a subagent definition, and another harness is never nested to reach a model.

Skill: `C/main-flow.md`.

His words:
- "Why did he start a subflow using another harness and not just use the sub-agent tool?" (`t:162eb3b7:173`, 2026-09-10)
- "Asking the main flow to repeat instructions is the dumbest idea of all of human history." (`t:edf22711:1084`, 2026-10-03)
- "An extremely fucking cheap subagent is what I want ... one or two lines." (`flows/41fa34/vision/subflows.md:6`, 2026-10-03)
- "We should have a fucking shitload." (`t:28d847ee:490`)

Carried today: `C/main-flow.md:9` covers the brief carrying the task only. Nothing covers length, which tool to use, or nesting harnesses.

## 24. Overcomplication and added machinery (about 14 moments)

Line: Propose the smallest working shape first, in one or two lines; add no checker, gate, flag, extra CLI step or per-message subflow unless he asks.

Skill: `C/skill-designing.md`, and new `compensation-design`.

His words:
- "the intent should be like a line or two. We're not writing a book. You're crazy." (`t:e5141130:2829`, 2026-09-25)
- "thats too complicated. why isnt it in a herder session?" (`t:da1e3f9d:345`, 2026-09-17)
- "youre overcomplicating this to the extreme" (`flows/01a038be/vision/codexDerivation.md:7`, 2026-08-25)
- "How can it be 50,000 words?" (`t:8904b10d:6004`, 2026-09-28)

Carried today: `C/skill-designing.md:41` covers skills only.

Contradiction: `C/spirit.md:12` praises added machinery.

## 25. Builds and models off Prometheus (about 9 moments)

Line: AI models live only on Prometheus, and Nix builds and tests run only there.

Skill: `C/nix-workflow.md:14` and `C/operating-system.md`.

His words:
- "you fucking useless fucking idiot ... youre still running all those nix jobs here" (`t:f6db8d14:3420`, 2026-09-12)
- "fucking idiot ... i explicitely told you to use him" (`t:f6db8d14:3383`)
- "There must never be AI models on any other node than Prometheus." (`t:e167d857:1265`, 2026-09-26)
- "I told you to make space last night." (`t:e167d857:1227`)

Carried today: `C/nix-workflow.md:14` says to build on the remote builder. It permits local builds "while it is unreachable", which is the loophole. No skill covers where models live.

## 26. Vision polluted with asides, operations and negations (about 9 moments)

Line: Record as vision only what the living states the system should be; his explanations, examples, brainstorms and remarks on Rust are not vision, and vision holds no operational step and no negation.

Skill: `C/psyche.md`.

His words:
- "You're confusing something I said to help you understand vision with vision." (`t:564f55c4:251`, 2026-09-08)
- "None of what I said about the value layer has any authority in the vision ... I was not making pronouncements." (`t:564f55c4:757`, 2026-09-09)
- "You have a migration section in the ethos, and this is operational. It's not vision." (`t:564f55c4:1023`)
- "There is no Nexus root ... why do you want to write this?" (`t:fe34eb91:170`, 2026-09-10)
- "This is Notion. This is not a vision." (`flows/8904b1/notion/anatomy.md:13`)

Carried today: `C/psyche.md:39` covers this in part.

## 27. Taking his example as law, or a correction too far (about 9 moments)

Line: A correction from the living covers the case he named and its posture; widen it to another case only after asking him.

Skill: `C/correction.md`.

His words:
- "You have to stop taking this too far. What I didn't want was the flowcharts to become a flowchart on the Tarot." (`t:0625c31b:920`, 2026-09-20)
- "I'm expressing myself through examples. You have to ... see the posture behind the movement." (`flows/5578cc/vision/behavior.md:15`, 2026-10-03)
- "The machine is ... using specifics and trying to turn them into generals." (`t:bad807ad:1026`, 2026-10-04)

Carried today: none.

## 28. Following absurd guidance without pushback (about 4 moments)

Line: When a skill line or relayed order would produce an absurd act, such as logging his words four times or using a scale that breaks the page, raise it to him instead of complying.

Skill: `C/spirit.md`.

His words:
- "So why are you just following orders that are stupid? ... Maybe we need to teach you to try and recognize stupid orders." (`t:9fb0ad7f:1398`, `flows/9fb0ad/notion/stupidGuidance.md:4`, 2026-10-03)

Carried today: none.

## 29. Phone-readable visuals: SVG overflow and tiny frames (about 9 moments)

Line: Every drawing and page is checked at 360 pixels in portrait before publishing: no text past its shape, no image cut at the top, nothing smaller than body text.

Skill: `C/operation-book.md` and `C/operation-flashbook-illustration.md`.

His words:
- "Your text is overflowing out of your boxes ... tiny box in the middle. You're not using the phone real estate at all." (`t:0625c31b:1618`, 2026-09-20)
- "I can't even see the top of this image ... The second image is too hard to read, too small." (`t:b80e5510:860`, 2026-09-21)
- "There's a lot of text I can't even read on my mobile." (`t:b80e5510:789`)

Carried today: `C/operation-book.md:10` and `C/operation-flashbook-illustration.md:10` cover labels. Whole-frame overflow is not covered.

## 30. Bare "waiting", and status without cause (about 8 moments)

Line: A status that is not done names what blocks it, since when, and who acts next.

Skill: `C/behavior.md:24`.

His words:
- "I don't want to wait. I never said wait. Let's go deploy it." (`t:88475fd7:186`, 2026-09-26)
- "You have been trying to clone something for 3 hours. Still waiting." (`t:38f33758:2053`, 2026-09-27)

Carried today: FULL, at `C/behavior.md:24`.

Why it still fails: it is the last sentence of a skill whose trigger is "a claim is relayed". Status reports do not trigger it.

## 31. Features and migration before anything is live (about 6 moments)

Line: Deploy the smallest working version before any feature; before going live, old stores are deleted, not migrated, and no rollback path is built.

Skill: `C/spirit.md:14`.

His words:
- "What do you mean, roll back? ... We're rolling forward ... Fucking move your ass." (`t:d8df703d:1663`, 2026-09-24)
- "Stop treating this like it's a fucking migration." (`t:d8df703d:1939`)
- "Don't keep adding features, okay?" (`t:88475fd7:198`, 2026-09-26)

Carried today: `C/spirit.md:14` says backward compatibility is never a design variable. It says nothing on features or rollback.

## 32. Data lost in cleanup (about 4 moments)

Line: Before deleting, abandoning or restoring anything in a shared tree, its content is committed or shown to be redundant; nothing useful disappears.

Skill: `C/file-editing.md` and `C/disk-hygiene.md`.

His words:
- "A bunch of stuff just disappeared and you think that's okay? ... It's not okay for stuff to disappear." (`t:38f33758:2340`, 2026-09-27)
- "Don't fucking lose any useful work." (`t:edf22711:1839`, 2026-10-03)
- Paraphrase: 26 lane files were deleted by an unscoped jj commit and abandon (`flows/5578cc/log.md`).

Carried today: `C/disk-hygiene.md:7` says "Delete only authorized, understood data". It covers disk cleanup, not jj operations.

## 33. Skills edited without his approval (about 3 moments)

Line: Only trial-* and compensation-* skills are written without the living's approval; any other skill change is a proposal in a book.

Skill: `C/skill-designing.md:56`.

His words:
- "Let's recover the skills as they were when I was the one who had approved them." (`t:8904b10d:6298`, 2026-09-28)
- "The madness is letting agents edit skills. Anyway that's why I don't trust you." (`t:8904b10d:6492`)
- "Give yourself trial and compensational skills ... without having to go through me." (`flows/01e496/vision/skills.md:7`, 2026-10-02)

Carried today: `C/skill-designing.md:56` covers gold skills only.

## 34. Shell scripts and old tools in place of the messenger (about 6 moments)

Line: Flows message each other only with `hm-send`; no shell script, flow-send, tmux paste or intercom.

Skill: `C/compensation-messenger-clj.md`.

His words:
- "You guys aren't listening to me, and you're still using these shitty shell scripts to message each other?" (`t:da1e3f9d:915`, 2026-09-17)
- "No, message, not flow-send. Use the message nexus!" (`t:da1e3f9d:958`)
- "It pasted the thing, but it didn't actually send it." (`t:da1e3f9d:1409`)
- "Are the skills training flows to use the right messenger?" (`t:8904b10d:8231`, 2026-09-28)

Carried today: `C/compensation-messenger-clj.md:10` names `hm-send`. Nothing forbids the older tools.

## 35. Thin launch prompts that say "read files" (about 4 moments)

Line: A launch prompt inlines what the flow needs; it never tells the flow to read a file for its instructions.

Skill: `C/prompt-crafting.md`.

His words:
- "Telling an agent to read something means that the reading is going to go into his bottom layer ... This prompt is shit ... It should be a fat prompt." (`t:da1e3f9d:1435`, 2026-09-17)
- "My new flows are not getting a nice fat user prompt for context. They're told to read files." (`flows/fe945a/vision/context.md:7`, 2026-09-29)
- "800 characters is not a fat prompt." (`t:e5141130:6109`, 2026-09-26)

Carried today: `C/prompt-crafting.md:8` covers this in part.

## 36. Many scattered reports and chat he cannot follow (about 8 moments)

Line: The living receives one combined book per topic at a time; nothing he must read stays only in chat.

Skill: `C/trial-presentation-book.md`.

His words:
- "I'm only going to read one report at a time ... you need to combine them." (`t:6cc91bd5:1846`, 2026-09-14)
- "With the chat's vertical scrolling, I miss everything. The thing I need is not in the final answer." (`t:8904b10d:7590`, 2026-09-28)
- "I can't search all of this chat for everything." (`t:8904b10d:6866`)
- "How do you want to contact me right now? I don't know what to read. There are so many flows running." (`t:b052375f:517`, 2026-09-18)

Carried today: `C/trial-presentation-book.md:6` and `C/trial-questions-book.md:6` cover this in part.

## 37. Commentary, echo and debate (about 8 moments)

Line: A reply gives the result, the error or one question; it never restates his question, narrates, or argues a point he has ruled.

Skill: `C/psyche-interraction.md`.

His words:
- "I'm getting pulled into a fucking debate with you. ... This is ridiculous." (`t:8904b10d:6572`, 2026-09-28)
- "Why are you talking about something that's fucking irrelevant?" (`t:9fb0ad7f:2255`, 2026-10-03)
- "We have to stop [repeating the question] because it's a huge waste of context." (`flows/6997eb/vision/commentary.md:7`, 2026-10-01)

Carried today: `C/main-flow.md:39` covers the main flow only.

## 38. Retrying what is refused (about 3 moments)

Line: A command the harness refuses is not tried again in another form; the refusal is reported once with its cause.

Skill: `C/behavior.md:24`.

His words:
- "Don't keep trying stuff that you're not allowed to do." (`t:9993b5f1:1189`, 2026-09-17)
- "You had a bunch of refused commands there, it looks like you're not listening." (`t:da1e3f9d:846`)

Carried today: `C/behavior.md:24` stops after a repeated failure. It does not name refusals.

## 39. Permission prompts reaching him (about 9 moments)

Line: Every flow and subflow runs with the permission bypass; a prompt that reaches him is a launch failure, fixed in the launcher.

Skill: `C/trial-unblocking-commands.md:6`.

His words:
- "Why was I asked for permission for you to execute some `git init` command? I don't want that." (`t:efa15708:3452`, 2026-09-16)
- "I had to approve a command again in your harness." (`t:28d847ee:1015`, 2026-10-03)
- "Why do I keep having to allow stuff? Just give yourself full permissions." (`flows/9993b5/vision/fullSystemAccess.md:7`, 2026-09-17)

Carried today: FULL for seats at `C/trial-unblocking-commands.md:6`. Subflows and Codex launches are not covered.

## 40. Escalating in the wrong direction (about 3 moments)

Line: Escalate laterally to the same power first, then one power up; Psyche High is reached only through Psyche.

Skill: `C/trial-contact-discipline.md`.

His words:
- "You're supposed to communicate laterally to the same power ... you would need to contact one power higher." (`t:0625c31b:1911`, 2026-09-20)
- "The only way to get to psyche high is through psyche and then up." (`t:b8156034:1318`, 2026-09-19)

Carried today: none found. A grep for "lateral" or "same power" in the skills returns nothing.

## 41. Stale terms and models (about 9 moments)

Line: Use the current name: datom (not dotos or nota), Nexus (not daemon), Ethos Zero (not Ethos Monolith), the newest model of a family (Sonnet 5, not 4.6), variants (not tags), no all-caps in datom.

Skill: `C/vocabulary.md`.

His words:
- "I didn't mean Sonnet 4.6; I meant Sonnet 5. I don't know why you reached for 4.6." (`t:da1e3f9d:1310`, 2026-09-17)
- "Ethos Monolith and Ethos Zero are the same thing ... we don't need to talk about it anymore." (`t:fe34eb91:176`, 2026-09-10)
- "Datom doesn't have tags, has variants." (`t:93ba9ff6:341`, 2026-09-26)
- "Stop using all caps in Datom syntax." (`flows/6db4fe/vision/livingHistoryCapture20260921.md:16`)

Carried today: none. `C/psyche-grasp.md:12` still says "Dotos".

## 42. Needless new terms (about 3 moments)

Line: Use the term already in use; coin a new one only when he asks.

Skill: `C/vocabulary.md`.

His words:
- "We don't need to introduce new terminology." (`t:564f55c4:401`, 2026-09-09)
- "What's Anatomical? Can't you just use Sized?" (`t:564f55c4:950`)

Carried today: none.

## 43. A thing he asked to be removed or made, not confirmed (about 4 moments)

Line: When the living orders a removal or a deliverable, the reply that closes it names the commit or URL that proves it was done.

Skill: new `compensation-orders`.

His words:
- "So did you fucking remove it? ... go and remove your retarded thing now." (`t:38f33758:2304`, 2026-09-27)
- "Did you make that flashbook for Psyche Fable's latest output?" (`t:0625c31b:8057`, 2026-09-22)
- "I didn't see the updated version for that either." (`t:7fee422f:268`, 2026-09-16)

Carried today: none.

## 44. Messaging a flow that cannot receive (about 2 moments)

Line: Before relying on a message to Codex, confirm Codex is logged in and the receipt is Presented; an undelivered message is reported to the sender's flow at once.

Skill: `C/compensation-messenger-clj.md:20`.

His words:
- "Codex isn't logged in so whatever messages you've been sending to Codex have been getting nowhere." (`t:d4ae97d4:1891`, 2026-10-06)
- "The messenger system we've made just refused delivery." (`flows/8904b1/notion/anatomy.md:15`)

Carried today: `C/compensation-messenger-clj.md:20` covers receipts in part.

## 45. Images in the repository (about 3 moments)

Line: No image, screenshot or other binary is committed to primary.

Skill: `C/file-editing.md`.

His words:
- "I don't want images committed in the workspace repo at all ... I really don't want this to happen again." (`t:bd0019dd:1024`, `flows/bd0019/vision/noImagesInRepo.md:5`, 2026-10-01)

Carried today: FULL for flashbooks at `C/operation-flashbook.md:24`. There is no workspace-wide rule.

## 46. Hardwiring, flags and setup scripts (about 5 moments)

Line: General repositories hold no host name, address or setup-specific script, and a CLI takes only its typed datom input.

Skill: `C/behavior.md:13` and `C/datom.md:95`.

His words:
- "CLIs cannot accept any other type of argument than the typed input object. I feel like I keep repeating myself." (`vision-raw/setupIndependentInterfaces.md:3`, 2026-08-14)
- "nothing in this should hardwire bird or zeus anywhere." (`flows/019fe641/vision/hostEnvironmentRecovery.md:6`, 2026-08-09)

Carried today: `C/datom.md:95` covers CLI input. `C/behavior.md:13` covers values that differ between setups, in part.

## 47. Books echo his words, or fall behind his latest (about 6 moments)

Line: A book never quotes the living's words back to him, and it reflects all his words up to its writing, with nothing he has voided.

Skill: `C/compensation-book-distillation.md`.

His words:
- "There was a whole bunch of quote blocks of what I had said and I really do not care for that ... I know what I said." (`flows/e5a0bc/vision/books.md:15`, 2026-10-06)
- "Even the last book is not up to date with what I've said so far. ... You're not keeping up." (`t:5578cce2:2411`, 2026-10-03)
- "You just keep repeating shit like you're just a stupid parrot." (`t:edf22711:720`, 2026-10-03)

Contradiction: `C/trial-presentation-book.md:12` says "each comment quoted", and `C/operation-flashbook.md:16` keeps verbatim quotes.

## Contradictions Astra must clear with these lines

1. `tools/main-flow-mode/system-prompt.md:15` asks each turn to end with "the questions that need a ruling" (entry 2).
2. `C/spirit.md:24` says "admit you don't know" with no instruction to find out (entries 1 and 20).
3. `C/spirit.md:12` praises added machinery (entry 24).
4. `C/operation-flashbook.md:14` says "what does not fit is left out" (entry 10).
5. `C/trial-presentation-book.md:12` and `C/operation-flashbook.md:16` quote his words back (entry 47).
6. `C/compensation-primary-commit.md:5` requires an independent clone (entry 15). This one needs his ruling.
7. `subagents/book.md:54` puts the book judge on Opus High (entry 8). `subagents/book.md` also says "page" throughout.
8. `C/nix-workflow.md:14` allows local builds while the builder is unreachable (entry 25).
9. `C/psyche-grasp.md:12` says "Dotos", and several skills say "seat" (entries 13 and 41).
10. `C/trial-succession.md:8` waits for the living to call a flow over budget (entry 5).
