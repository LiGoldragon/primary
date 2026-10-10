# Audit C: psyche flows 6997eb and 91ea9f

Ordered by the living, typed, 2026-10-03 morning, relayed in f1c841's brief: "Do a complete audit and use all of the psyche flows to report on everything that's been done, everything that's not been done, and why."

Method. I read each flow's log, summary, successor brief, reports, vision, evidence and witnesses. I read the comment threads on every book with ArtifactComments, so the comments below are observed, not taken from logs. I checked landings against the remote repositories (`git branch -r --contains`, `git grep` on origin/main), after a fetch on 2026-10-03 around 06:25 CST. I grepped the logs of later flows for each handed-over item. I did not open transcripts; a quote whose only source is a transcript line is cited by that line, as the flows recorded it.

Labels: **[obs]** I witnessed it in this audit. **[claim]** the flow's record says so and I did not check it. **[unknown]** nothing settles it.

---

## Flow 6997eb, Psyche.{ Fable 6997eb }, 2026-10-01 to 2026-10-02

### 1. What the living asked of it (verbatim, with provenance)

- The task at launch [claim, log line 3, not verbatim]: two presentations of at most four points each, on short-term fixes and on next steps for the meta harness, presented to the living and then made into a book by Sonnet bd0019.
- Repository classification (STT, 2026-10-01, `6997eb/vision/repositoryClassification.md`): "Let's create a nexus that classifies our repositories. Let's think of a name and it will sort of be the basis for a top-down structural organization of everything, giving things types. … Let's do some research into that field also. What have other people done? … talk about this to Opus also".
- Questions (STT, 2026-10-01, `vision/questions.md`): "I want my questions to be assembled together, even if the speech-to-text misses the fact that I'm asking a question. … I want these questions gathered and brought into a book with either answers or proposals for an answer, or proposals for counter questions."
- Three kinds of logging (STT, 2026-10-01, `vision/logging.md`): "We could even have three different types of logging. Whenever the living is touching on one of the three aspects".
- Marking his block (STT, 2026-10-01, `vision/presentation.md`): "We're going to train all of the main flows to, whenever they want to talk to the living, mark that block as intended for the living at the beginning and at the end. … Talk to Astra about how you would do this and practice and then let's make a book about this."
- Commentary (STT, 2026-10-01, `vision/commentary.md`): "We have to stop doing that because it's a huge waste of context. We have to actually train the model to minimize unnecessary commentaries."
- Pipeline (STT, 2026-10-01, `vision/pipeline.md`): "Let's design a pipeline that automates things through hooks when a certain pattern is detected. Then it can be sent to Sonnet for either a new book or for editing an already existing one."
- Interfaces (STT, 2026-10-01, `vision/interfaces.md`): "let's maybe review, extend, and re-verify this in terms of what other user interfaces are available."
- Involvement (STT, corrected typed "Claude not cloud", 2026-10-01, log 23–24): "We have quite a bit of [Claude] usage for the next 2 days so you, Opus, and Sonnet can remain, or should remain, quite involved today and tomorrow in guiding, advising, and bringing things to me through the books."
- Rulings on the marker and metadata, all on 2026-10-01 (`vision/presentation.md`): "Astra's vision is better." / "I'm not taking out the markers here." / "That wasn't a question. I said it is bad." / "Yeah the metadata is one datom line. That's brilliant. I love it. Let's do it." He also asked for the book: "put together a book now that you've wrapped your head around this way of separating the psyche or the living directed output from the more machine- and intent-free output".
- Rendering, relayed by Opus fe945a (STT, 2026-10-01, log 71): "the books become the user interface. It's not a question anymore". He called calling an LLM to render "ridiculous" and said "Get Fable on that to research and propose alternatives". The quotes are fragments as the log holds them.
- Wired network, relayed by Field Astra (STT, 2026-10-01, log 74): find the fault and fix it, then Mind designs and Fable audits. "We favor solutions that decrease the codebase … A solution that would change things dramatically in terms of the code but solve a lot of problems is the best."
- Blocked command (typed, 2026-10-02, log 101): "Your command blocked. I want a report on that and previous incidents like it".
- Meta harness (typed, 2026-10-02, `vision/metaHarness.md`): "Get a full grasp of everything and re-question this: the current implementations and skills, … and restart the whole psyche stack with a fresh well-concentrated psyche context on making the meta harness more usable. … Present everything in books and then restart your flows after you've done all that. … All of the old codex flows, or all of the codex flows with large context, should be restarted".
- **Book comments [obs, read from the artifacts]**
  - On «Two kinds of output» (4hNGTG…), 19:34: "Is there a reason why you're suggesting a YAML block? Is it because it doesn't render right if you use the real front matter? …". At 19:36: "Overall this is good. … let's make another book that details the anatomy … Is this Flow, or is it Transcript, or is it something else?" Both are logged in 6997eb.
  - On «Your questions since 28 September» (Xq4EK3…), 20:27: "This is an example of a good or decent illustration which could be made from a flowchart accompanied by prose. … You could call that an illustrated flowchart." At 20:29: "So a question is one of the different layers of mind, as spirit, vision, and notion are to psyche. Let's make this vision, right now, into an appropriate vision file. And to be clear, now vision is skill. Let's make that whole migration. Let's orchestrate that whole vision-to-skill merging, migration, and deployment, and the new infrastructure for all of it."
  - **6997eb's log does not record either comment on «Your questions» [obs].** The 20:29 comment is logged only in `fe945a/vision/questions.md`, by Opus.

### 2. What it did and what landed

- **Marker paragraph in the main-flow skill.** Curriculum e833f1 is on origin/main [obs]. The regenerated Primary tree 958455 is on main [obs].
- **The block's rules.** The comment-pair markers, the `Presentation.{ «title» }` datom line, and "not every reply" are all ruled. These are claims carried into the successor brief; the rule text lives in the skills.
- **signal-flow 6.3.0** declares `Presentation`, `TurnEndRequest` and `QueueTurnEnd` (eba281). eba281 is on signal-flow origin/main, and `QueueTurnEnd` is present in `ethos/signal.ethos` and in `tests/presentation_turn_end.rs` at main 10.0.0 [obs]. It was declared only, with no hook and no consumer [claim].
- **Small fixes ruled to Mind Sol.** All of these are on Primary main [obs]: the messenger skill (Curriculum c99253), the manifest sentence (Primary b39328), the launcher socket fix (6d860), the launcher gpt-6.1-sol fix (edb450), the five dead tools removed (4a6bfd), and the Field refresh rule withdrawn (fc4eec). The messenger retire guard a9fe62 (0.2.9) and its red test d2f821 are on messenger-clj origin/main [obs].
- **Wired network (USB sharing).** It ran from design through audit to a red-then-green test. The 6997eb tester witnessed the schema-refusal test red on a36de1 and green on 3f7c33 and 94d8b6 [claim, the flow's own witness]. All the code is **only on the review branches `usb-sharing-5104af`** of CriomOS (989ccd, d4123e), lojix (b93b51, cea66f), horizon-rs (12b2a2) and goldragon (df4528), and is not on main [obs]. The converter qualification (lojix-test b01492, 5aece4) is on lojix-test main [obs]. The chain green at 989ccd was corroborated by Field Sol [claim]; the 6997eb tester could not witness it (log 100).
- **Research reports landed in the lane**: repository classification, interface research, the psyche since 28 September, the questions since 28 September (100 questions, 33 answered) [obs, files present].
- **Seven books published by Sonnet bd0019** (see 5).
- **Blocked-command report.** It was presented in a marked block. The cause it found: an `rm` with a glob directly under a shell variable triggers a dialog in every mode [claim, from transcripts and vendor docs].
- **Restart of the stack.** The Codex successions landed: Field Astra 7de94a, Field Sol 42265e, Mind Sol 41fa34 [claim, Opus via 91ea9f log 26]. 6997eb was succeeded by 91ea9f and retired [claim, `91ea9f/evidence/registration.md`].
- **Successor brief** `6997eb/successor-brief.md`. Its commit 1676b6 is not resolvable in Primary today [obs]; the history was rewritten at the thaw. The file itself is present.

### 3. What was not done, and the reason recorded

- **Repository classification Nexus.** Not built and not named. The research landed; the log shows no presentation of a name and no ruling. Reason: **none recorded**. The subject drops from the log after line 13, when the living moved to questions. No later flow took it up as work [obs, grep "classif"; the hits are unrelated].
- **Hook-to-book pipeline.** It stopped at design. Flow-or-Transcript was presented and **never answered**. The hook was "prepare, do not install". The recorded reason: no ruling from the living, and the Transcript Nexus is unbuilt (91ea9f `reports/6997eb-open-work.md` §3).
- **Eight rulings presented after its 2026-10-02 order, unanswered.** Reason: "The living typed nothing to 6997eb after line 2294" (91ea9f report). They are: the two handoff/subflow tensions; stale seats restarted on idle; succession automatic on old context; ephemeral sessions as Flow objects; the handoff tension; the restart word and its order; whether 6997eb stays until the network audit; and the roster's "Say if you meant fewer".
- **Earlier rulings also left open**: the overlap-subnet policy; built-in ports as upstream candidates; downstream through recovery Wi-Fi; fixed or DHCP DNS; the permission hook's default; `question/` as the record; four skill proposals; pulldown-cmark / Mentci display Nexus / tailnet app first; remote control off. Reason: presented, no answer recorded.
- **Wired network merge and deployment.** Not merged. Reason recorded: the final audit waits on the overlap ruling and the Wi-Fi overlap fixture; deployment is gated on Field (log 109–110, successor brief).
- **The dropped-spaces fault in Astra's messages.** Unplaced. Reason: the sender's bodies are not retained on the Codex side (log 68–69).
- **Build-directory garbage collection** (meta-harness order). Zero bytes reclaimed. Reason: "no safe disposable candidate found" (log 132).
- **His 20:29 «Your questions» order** ("a question is one of the different layers of mind … make this vision … vision is skill. Let's make that whole migration"). 6997eb records no action; reason **none recorded**. The file it asks for was made by fe945a, not by 6997eb.

### 4. Handed over, and whether a successor took it

The handover was `6997eb/successor-brief.md`, received by 91ea9f, which wrote `reports/6997eb-open-work.md`.

| Item | Taken? |
|---|---|
| Flow-or-Transcript, the hook | Partly. f1c841 built a flow-hook binary and Report in flow 0.21.0 (f1c841 log 00:55–01:25) [claim]. Flow main is now 0.23.0, but the installed CLI is **0.12.2** and `~/.claude/settings.json` has no Stop hook [obs]. The Flow-or-Transcript question was put into f1c841's morning-book inputs [claim]. Never ruled. |
| Wired network final audit | Not closed. Field Sol's log (42265e) still lists "overlap-policy ruling, guard qualification, final Fable audit" as the gate order [obs, grep]. The branches are unmerged [obs]. |
| Codex successions | Done by Opus 01e496 [claim]. |
| Overlap, DNS, ports, Wi-Fi rulings | No successor log shows a ruling [obs, grep]. |
| Permission-hook default | Unruled. The same failure recurred in 3ec648 ("stopped this seat at a permission prompt on an rm with a possibly-empty variable"). Only fe945a's log mentions a PermissionRequest hook [obs, grep]. |
| pulldown-cmark / Mentci / tailnet | No later log mentions pulldown [obs]. Not taken. |
| `question/` record; questions pipeline | Not built. The question layer appears in 3ec648's ruling 1 as the `question-` skill prefix [obs, `3ec648/rulings.md`]. |
| Stale-seat, ephemeral and succession rulings | No hit for "restarted on idle" [obs]. Not taken. |
| Sonnet's book receipts | Kept in `6997eb/reports/book-receipts.md` [obs]. |

### 5. Books, and whether he commented [obs from the artifacts]

| Book | URL | Comments |
|---|---|---|
| «Marking a presentation for the living», later edited into «Two kinds of output» | claude.ai/artifact/4hNGTGzPpibhR4BN1qsTwB | 2 (YAML question; anatomy request) |
| «The anatomy of the book pipeline» | claude.ai/artifact/BejUZBhgGcvqmeW9QZVQwv | none |
| «Your questions since 28 September» | claude.ai/artifact/Xq4EK3FjUWzhhc2UxZQ6as | 2 (illustrated flowchart; question as a layer of mind and the vision-to-skill migration) |
| «Handling skills» | claude.ai/artifact/Pmpj8s1faBVmH6dppX35WY | none |
| «Six questions on sessions, re-asked» | claude.ai/artifact/1HgDScoM6YtMFXCM4DK7LV | none |
| «The restart of the stack» | claude.ai/artifact/5rC2icGkE7WtAbXit6dLyB | none |

The four uncommented books carry most of 6997eb's open rulings. That is consistent with "The living typed nothing to 6997eb after line 2294", but that is my inference.

---

## Flow 91ea9f, Psyche.{ Fable 91ea9f }, 2026-10-02

### 1. What the living asked of it (verbatim, all 2026-10-02; typed unless marked)

- Capsule (STT): "Maybe when we start Fable we ask him what would best represent the name of this component that basically handles the encapsulation side of things." Testing (STT): "We can have a Nix-written sort of semi-sandbox. Again we have to iron out how we move my credentials into a sandbox so that you can test stuff with small cheap models."
- Flow: "Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow."
- Addressing: "I'd like flows to be addressable by their continuous name … so that we don't need to use these flow IDs anymore."
- Seat: "Let's create the abstraction of a seat. I don't think I like the word "seat." … Maybe a better term".
- Skills: "make sure whenever you have a presentation or Opus has a presentation, the signal is sent or the bookmaker role is used … Give yourself trial and compensational skills". Also: "Bring me things that are in skills that need my approval and are in conflict with what I want … Like an emergency skill catch-up wave".
- Visuals: "I want to see the ethos and the architecture with flowcharts. I want a lot of visuals actually." Books: "we need to properly render the flowchart. … Let's do a few trials with the books … and then I'll rate what I see".
- Flow ethos: "I want you to design the "What are your most important questions?" proposition and design ethos for Flow. … I want to see the ethos and the example datom". Also: "Make that into a book but let's look at revamping ethos and then describing the signal, process, and storage parts in ethos of Flow".
- Ethos: "Now we need the actual ethos of the three layers … Let's distill the vision for this and start putting out example syntaxes". Also: "Yes let's make a book with Astra and with the ethos of all three layers: signal, storage, and operation."
- Corrections and rules: "There's no page that's mine. That's a confused concept." / "Stop saying "page." … It's the user interface. It's the living messenger." / "we can't reuse a book that I've commented on" / "Design should be done by Astra and not Sol." / "I only read the presentations so why didn't you put that into a presentation? … Talk back to me in the book." / "No, you don't just get to say "deployment waits for the thaw." You have to explain."
- Priority: "Actually I just want a simple working system that we can use now to improve our lives".
- Merge and worktrees: "Tell Opus to just figure it out and just make it work. Solve the conflict and use common sense." Also: "Let's merge. Why do we have, what, 30 GB of work trees? I want all these work trees gone so let's get to it."
- Deep dive: "I want the whole thing about kinds and parameters in Rust to go into an extensive deep dive into this, with visuals, flowcharts, and Rust internal flowcharts. I want to understand this because I feel like we're talking past each other." Also: "To me the profile profiled doesn't make any sense and I don't relate to your examples."
- Succession: "Maybe you want to start yourself. Let's distill all of the vision that you think is most important about this and then start you on a new flow with this." Then: "What distillation? I didn't approve anything. Psyche distillation needs my approval."
- Distillation: "When I distill I distill everything not just today's. … Let's distill one thing at a time." Also: "You have to split up the vision into the right skills." Approval: "your distillation skill editing is good. Let's land it through" (log 85).
- Voices, after succession: "it's psyche primary, psyche secondary, mind primary, mind secondary … For now there are 9 voices, 3 by 3." Also: "Mind.Astra not a string; two variants!"
- **Book comments [obs, read from the artifacts]**
  - «The Capsule and the Semi-Sandbox» has 6 threads, 7 comments: "Yeah I think I picked the right word. It's going to be called Capsule." / route (b) "is a design for later on. It's something that will just encrypt the file system" / "Yes that's right. You have it right here." / "This is a great example of the visual flowcharts I want to see. Let's make sure that the skill has distilled guidance" / "I can see this comment showing up on all the pages now …" / "I don't want this swipe-left-to-right type of web UI anymore." / "It's ridiculous to ask me where things are."
  - «Skill catch-up wave» has 6 threads, 8 comments: "Yes exactly. This is exactly what I mean." / "We need to absolutely forbid this kind of UI." / "Yeah I think I want to get rid of the gold skills concept and every skill is typed. …" / "Code blocks are fine." / "I don't like using these `never` commands." / item 7 "I'm not comfortable allowing this." / item 12 "This is not vision. This is just a direct order" and "If this was logged as vision … it has to be removed."
  - «Flow in ethos» has 9 comments: "Yes they're going to be called voices." / "the word you used, "run," is "flow."" / "I don't want these Sonnet comments anymore." / "Yeah the memory is good. That's what it is I guess: signal, operation, and memory. … I want a whole document on this aspect of how the anatomy is developed in signal … and in operation" / "We don't have key-value in Ethos anymore. Everything is a type." / "What the hell is a question 4 here?" / "we went more towards the qualifier `launchable`" / "I want it to be a language that expands vertically. …" / "I don't understand how there's a specific type as an input for a kind. … Do some actual real-world Rust checks".
  - All 24 are logged verbatim in 91ea9f's vision files [obs, matched]. Two of its vision records were later judged impurities by the flow itself: the checkmark question was removed (log 67), and the orders in `flowNexus.md` and `ethos.md` are framed as orders.

### 2. What it did and what landed

- **6997eb retired** through the messenger retirement import, with immutable evidence [claim, `evidence/registration.md`, its own witness].
- **Book agent fixed.** curriculum-deploy fb171e3b carries the authored subagent procedure, and it is on origin/main [obs]. Curriculum 2898f80a makes book "write demanding" (Opus) and is on origin/main [obs]. The flow itself said this "had no word of his behind it and is to be put back to Sonnet" (log 45). **No record shows it was put back** [unknown]. The test from this session was inconclusive (`witnesses/book-agent-regeneration.md`).
- **Vocabulary.** The Living messenger line is landed. Curriculum origin/main `skills/vocabulary.md:16` reads "Living messenger: the user interface through which a flow reaches the living, asynchronous to the chat; a presentation is one message in it." [obs]. This is the later four-skill refinement (Curriculum 927d05, via 3ec648) [claim].
- **trial-presentation-book and compensation-primary-commit** both exist in Curriculum skills/ on origin/main [obs].
- **Vision definition in the psyche skill.** Present: "Vision is what the living says the system should be. A question, an order, …" at psyche.md:39 [obs].
- **No swipe and no checkboxes.** Present in operation-flashbook.md:12 [obs]. That line is worded "Never use horizontal swipe or paging", against his "I don't like using these `never` commands" [obs; the tension is my own reading].
- **Catch-up wave.** He approved 1, 2, 4, 5, 6, 9, 10, 13 and 14. They are landed, together with twelve non-gold sources; unapproved gold 3, 7, 8, 11, 12 and 15–18 are not landed [claim, Mind Sol via 3ec648 log].
- **Capsule named.** Route (a) was approved by his comment. The semi-sandbox was built later by 3ec648 (`3ec648/reports/semi-sandbox.md`) [claim].
- **Ownership rulings.** Mind Astra designs Flow, Mind Sol reviews, Field Sol builds. Mind Astra dea0ba was launched [claim].
- **Reboot vision entry removed** on his word (`witnesses/vision-impurity-removal.md`) [claim].
- **Worktree inventory**: 87 worktrees, 28.9 GB. Removal was ordered to Field.
- **Six books published** (see 5).

### 3. What was not done, and the reason recorded

- **A working Flow with hooks, name addressing, and the seat abstraction.** Not done in 91ea9f. Reason: assigned as design to Mind Astra (log 37–43). Today, Flow main is 0.23.0 but the installed CLI is 0.12.2 and there is no Stop hook in `~/.claude/settings.json` [obs]. Seats still start from the Node launchers in `tools/` on Primary main [obs]. "Flow Start becomes the route and the launcher is deleted" is **not done** [obs, the launchers are present].
- **operation-book retirement** ("operation-book to be retired", summary item 7). `skills/operation-book.md` is still on Curriculum origin/main [obs]. Reason: **none recorded**; 41fa34's log records a later review keeping it.
- **His rulings on the ethos book (6), the deep dive (4), and the typed-skills shape.** Unanswered at handover. The reason recorded by 3ec648: the six ethos statements "were put to him in chat only … so he has not read them". 3ec648 then took them as "Rulings taken for the living by recency and emphasis" on his STT order (`3ec648/rulings.md`). Ruling 1 (gold retired) is flagged "for his confirmation" [obs].
- **"I want a whole document on this aspect of how the anatomy is developed in signal … and in operation"** and the summary's "three-layer anatomy document he asked for in full". Listed as unfinished; reason: **none recorded** beyond the session ending. 3ec648's «Ethos as two skills, the case study» and the ethos-zero 15/16 work touch it [claim]; no book by that subject is recorded.
- **Worktrees gone.** Not done. Field Sol "stopped all worktree cleanup" after a subflow deleted an unpreserved worktree (3ec648 log) [claim]. By a different measure (git worktree `.git` files at depth 5 or less under /git, /home/li and /tmp), 16 remain [obs]. That is not comparable to the 87, which counted jj workspaces too.
- **The flowchart-rating trial** ("I'll rate what I see"). One trial book was made, and he praised it. No rating scale was set; reason: **none recorded**.
- **The successor launch.** Refused by the launcher ("main is not an ancestor of @"); it was done after the thaw by Opus's route [claim]. 3ec648 later fixed the launcher (6f7f3d) [claim].
- **Its last send** (the four-skill landing to Field) failed on a FLOW_ID validation error. It passed through 3ec648, and Field landed it as Curriculum 927d05 [claim, 3ec648 log].

### 4. Handed over (`91ea9f/successor-brief.md` and log 87), and whether 3ec648 took it

| Item | Taken? |
|---|---|
| Six ethos distillation statements | Yes: re-presented as a book, then ruled by 3ec648 on his "play the role of the psyche" order; vision-ethos and knowledge-ethos landed (Curriculum b5dc86) [claim]. |
| Mind.Astra form / voices | Yes: ruling 6, `Aspect.Rank` [obs, rulings.md]. |
| Four-skill living-messenger landing | Yes: Curriculum 927d05 [claim]; the vocabulary line is on main [obs]. |
| Three books out | Witnessed by 3ec648, uncommented [claim]; I confirm none of them has comments [obs]. |
| Worktree removal at Field | Stopped by Field after a loss; flake pair reconstructed, not byte-exact [claim]. |
| Typed skills (gold retired) | Ruling 1 by 3ec648, flagged for his confirmation [obs]. |
| Flow Start, hooks, name addressing | Partly: Flow repinned, Report/flow-hook in 0.21.0 by f1c841 [claim]. Not deployed; CLI 0.12.2 installed [obs]. |
| Three-layer anatomy document | No book by that title in later logs [obs, grep "three layers"; the hits are unrelated flows]. |

### 5. Books, and whether he commented [obs from the artifacts]

| Book | URL | Comments |
|---|---|---|
| Bookmaker trial (unwanted new page) | claude.ai/artifact/3pbbY8tZDXcZxzUUnoGGtJ | none |
| «The Capsule and the Semi-Sandbox» | claude.ai/artifact/VhgcBp3G4u5Hiaj8bugmGm | 7 (6 threads) |
| «Skill catch-up wave» | claude.ai/artifact/3tjcr5uX5k1yLJrJCksfoJ | 8 (6 threads); approvals given in chat (log 66) |
| «Flow in ethos» | claude.ai/artifact/EHdSy5fb4bZ3gDSNaSgNkN | 9 |
| «Ethos in three layers, redone» | claude.ai/artifact/YRFL5EyVzx7GUFPVSaZ7vq | none |
| «Kinds and parameters, the deep dive» | claude.ai/artifact/U3x2EkXN8YL9oDTGieBDcX | none |

The two books he asked for most pointedly, the redone ethos and the deep dive, carry no comment. Whether he read them is unknown.

---

## Asked by the living, and done by no flow (across both flows and their successors as far as the logs show)

- A repository-classification Nexus with a name.
- A questions pipeline, a central record of his questions, and the `question/` record. Only a skill prefix was ruled, by 3ec648 on his behalf.
- Three logging types with descriptions and examples, as a landed skill or record. Proposed in a block and not ruled [claim, log 21]; no landing found.
- Commentary minimized and turned into system logging. No landing recorded.
- Interface alternatives acted on: pulldown-cmark renderer, display Nexus, remote control off. Researched only.
- "All of these work trees gone".
- A working Flow that launches flows with harness hooks, deployed. Built pieces exist on main; nothing is installed.
- The anatomy document on signal and operation; the flowchart rating scale.

## Sources

- /home/li/primary/flows/6997eb/log.md; successor-brief.md; reports/book-receipts.md; reports/repository-classification-research.md (presence only); vision/*.md
- /home/li/primary/flows/91ea9f/log.md; summary.md; successor-brief.md; reports/6997eb-open-work.md; evidence/registration.md; evidence/retirement-6997eb.md; witnesses/book-agent-regeneration.md; witnesses/vision-impurity-removal.md; vision/*.md
- /home/li/primary/flows/3ec648/log.md; /home/li/primary/flows/3ec648/rulings.md; /home/li/primary/flows/f1c841/log.md; greps over /home/li/primary/flows/*/log.md (42265e, 41fa34, dea0ba, fe945a, 7de94a hits)
- /home/li/primary/flows/fe945a/vision/questions.md (location of the 20:29 comment)
- ArtifactComments read, 2026-10-03, on the twelve artifact URLs listed in the two book tables
- git, after fetch, 2026-10-03: Curriculum (e833f1, c99253, 2898f80a, 250c48 on origin/main; 1ce183 not found; skills/ listing; vocabulary.md:16; psyche.md:39; operation-flashbook.md:12); signal-flow (eba281 on main; QueueTurnEnd grep; version 10.0.0); CriomOS, lojix, horizon-rs, goldragon (cited commits only on origin/usb-sharing-5104af); lojix-test (b01492, 5aece4, fe9d85 on main); curriculum-deploy fb171e3b; messenger-clj a9fe62, d2f821; flow origin/main Cargo.toml 0.23.0; Primary (edb450, 4a6bfd, fc4eec, 958455, b39328, 6d860 on main; 1676b6 not found; tools/*launch*.mjs present)
- Host: `flow --version` → 0.12.2; `grep -c '"Stop"' ~/.claude/settings.json` → 0; `find /git /home/li /tmp -maxdepth 5 -name .git -type f | wc -l` → 16
