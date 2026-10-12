# Check of books 9 and 10 (33752b) against the living's records

Checked 2026-10-12, at the request of 33752b, by method of `flows/d68c82/reports/delegates-book-check-2026-10-12.md`. Sources compared: the two book sources, every record they cite, the d68c82 packet sections B and C (its full record lists), the records those lists name where they bear on a sentence, and psyche-skills at 9bba4bf (`vision-messaging`, `vision-aspects`, `vision-model-roles`, `vision-flow`, and commits 850fd27, c3f8eeb). Dates of undated records were taken from the commit that added them.

Verdicts: S supported by his words; M supported only by a machine skill; X exaggerated; O out of context; G garbled or contested record; Q contradicted or qualified by a record the book does not show; N count or date wrong.

## Book 9, «His words travel as psyche»

### Figure

| Statement | Verdict | Deciding record |
|---|---|---|
| "logged, then relayed" | S | e51411/vision/mainFlow.md 2026-09-25: "that flow should relay the new Psyche, even though it logged it itself, to a Psyche flow". Contested by 183ae0/vision/seats.md 2026-09-29 (see below). |
| "#psyche, context + whole verbatim" | S | 88475f/vision/message.md 2026-09-25 "first is the context and then the verbatim" (hedged "I guess"); b7da5d/vision/layerVocabularyAndReview.md 2026-09-26 "the context of what it was said in and the whole thing verbatim". |
| "no interpretation" | S, role-specific; Q | 4ddfe1/vision/messaging.md 2026-10-10 (STT, no context line) was said to a seat whose role is voice relay: 4ddfe1/vision/voice-relay.md "Your role is mostly just as a voice relay" (the packet itself marks it role-specific). Qualified by b81560/vision/operational-psychePropagation... 2026-09-19: the forwarder may add "Here's what I'm preparing to do in response"; b05237/vision/operational-standardMessagingSkill.md 2026-09-18: "make sure that it's clear that it's from you"; e51411/vision/messaging.md 2026-09-25: speech-to-text is corrected before it travels. |
| "#psyche ... straight to the flow that acts next" | O; Q | The source, d68c82/vision/messaging.md 2026-10-12, is about machine work (Mind messaging Sonnet for a book), not his words. His records send his words to a Psyche flow (e51411/vision/mainFlow.md 2026-09-25; landed intent-psyche-interaction), "up the chain" (0625c3/vision/relayUpChain.md 2026-09-20), to Psyche Medium (b05237 2026-09-18; 108ab0 2026-09-17), or to everyone (1ac573 2026-09-17; b7da5d 2026-09-26, for that one message). None says to the doer. |
| "#msg: only what acts, delivers, blocks" | S, already landed | vision-messaging «Only messages that act, deliver, or block»; 9fb0ad/vision/messaging.md 2026-10-03; bad807/vision/messaging.md 2026-10-04. |

### Context paragraph

| Statement | Verdict | Deciding record |
|---|---|---|
| "Thirty-one flows carry this from 2026-09-15 to today" | N/X | Recounted: the packet's subject B lists 50 records in 31 distinct flows, 2026-09-15 to 2026-10-12, so the number is the packet's and is exact for that list. But the list is wider than "this": it includes the packet's own impurities (b81560 naming/Herdr/disk, 1ac573 roster), mechanism records (cf7879, 840e42 first-six/last-six words), a notion (692df8/notion/logging.md), records covered elsewhere (9fb0ad, bad807, 445410 hub), the independent-review record e167d8/independentReview.md, cluster-mirroring records (fd0f97, 48cff7, 9993b5), and 183ae0/seats.md, which runs the other way. Same fault as book 8's "twenty-six flows". |
| "the machine messenger skill carries it" | S as a fact; book rule | field-skills compensation-messenger-clj carries "The living's words travel only as psyche ... never quoted ... inside a #msg body" (read in 33752b's brief B2 and in this flow's own context). A statement of how the system runs today, which vision-book keeps out of books. |
| "vision-messaging has only the line on which messages are sent" | S | psyche-skills 9bba4bf: the only section on this subject is «Only messages that act, deliver, or block». |
| Six record paths and dates | S | All six exist; 4ddfe1 added 2026-10-10 (da9eda), 28d847 messaging 2026-10-04 (9061fa); the rest carry their dates. |
| "A record of 2026-09-29 (183ae0) says a flow that hears you logs it and need not tell everybody" | X | Date right (added e5dee4, 2026-09-29). His words are of a Field seat: "if a field should tell psyche or mind what I'm saying ... They don't need to tell everybody; they just need to log it." The book widens "a field" to "a flow that hears you". |
| "it stands beside the relay to one Psyche flow and is not touched here" | G; unsurfaced | The record says a Field seat need not tell Psyche or Mind, which is against e51411/vision/mainFlow.md 2026-09-25 and d8df70/vision/messaging.md 2026-09-24. d68c82's packet calls it "a tension to surface, not to decide". The book decides it by its own reading ("stands beside") and asks no ruling. |

### Proposal 1, new section in vision-messaging

| Statement | Verdict | Deciding record |
|---|---|---|
| "travel between flows as psyche: the context first, then the whole verbatim, in the psyche message" | S | 88475f/vision/message.md 2026-09-25; b7da5d 2026-09-26; 445410/vision/messaging.md 2026-10-09 "We should use the psyche-type message". |
| "whole verbatim" | Q | e51411/vision/messaging.md 2026-09-25: "We shouldn't pass around verbatim speech to text that has not been corrected", corrections marked. The proposal does not say the verbatim is corrected. |
| "and never inside a machine message" | M/X | "Never" is compensation-messenger-clj's wording ("never quoted, paraphrased or summarized inside a #msg body"). His words: "We should use the psyche-type message ... and then use the message type to talk to each other" (445410 2026-10-09). |
| "The relaying flow relays; it does not interpret." | S, one record, role-specific; Q | As the figure's "no interpretation": 4ddfe1 2026-10-10 to a voice-relay seat; qualified by b81560 2026-09-19 (the planned response may go with it) and b05237 2026-09-18 (the relayer marks itself). |
| "The words enter the receiving flow's prompt, where they carry more than a record read later." | S | e51411/vision/messaging.md 2026-09-25 "It comes in the prompt, in the user prompt, so it reinforces the narrative better than just reading them". It is a reason, not a ruling. |
| (omitted) a message that rests on his words carries them | gap | e51411/vision/messaging.md and 88475f/vision/message.md 2026-09-25 ("spread it to whoever you're messaging, whenever you need to quote psyche"); 0625c3/vision/messagingVerbatimAuthorization.md 2026-09-20 "every time somebody sends a message, they need the Psyche verbatim that authorized it". The packet lists this; the proposal drops it while keeping only its reason. |
| (omitted) no size limit; a vector of psyches | gap | b7da5d / e167d8 2026-09-26; 88475f 2026-09-25 "remove the 800-character limit". b7da5d is cited as a record, but none of its content is proposed. |

### Proposal 2

| Statement | Verdict | Deciding record |
|---|---|---|
| "An order from the living is marked as an order when it is passed on, so every flow it reaches knows it as his." | S | 28d847/vision/messaging.md, typed, 2026-10-04 (9061fa): "an order should be marked as such when it's passed around so that it's recognized by all the flows involved as an order from the living". The proposal drops his "We could have this type of message", which is the message-type part. |

### Proposal 3

| Statement | Verdict | Deciding record |
|---|---|---|
| "Messages between flows are few and each is of use" | S | d68c82/vision/messaging.md, STT, 2026-10-12: "minimize the amount of messaging between flows and maximize their utility". |
| "work goes straight to the flow that acts on it next" | S | Same record, the example: Mind "could just message Sonnet directly instead of messaging you to publish it". |
| "not through a flow that only passes it on" | O; Q | In his example the flow skipped is the one that asked for the work (d68c82), not a pass-through. A general ban on pass-through flows conflicts with the secretary and hub he ruled: 28d847/vision/layers.md 2026-10-03 ("the one that gets all the messages in and out, and only you talk to Fable"); d4ae97/vision/flow.md 2026-10-07 ("You're going to have to talk to a secretary"); 445410/vision/messaging.md 2026-10-09 (hub messaging through the Secondaries, landed in vision-aspects); bad807/vision/gatedFlows.md 2026-10-04 (gated flows messaged only through a secretary); 0625c3 2026-09-20 (relay up the chain). It also conflicts with book 10's own proposal. |

## Book 10, «Aspects talk at the same layer, second edition»

### Figure

| Statement | Verdict | Deciding record |
|---|---|---|
| "PRIMARY, spoken to least" | S | 7328f4/vision/seats.md 2026-09-30 "diminish how much of the primary layer gets disturbed"; 5578cc/vision/flow.md 2026-10-03T15:43 ("the beginning is good" of "...the Primary layer is spoken to least"); caf622/vision/Fable.md 2026-09-28 (of Fable). |
| "judgments, rulings, design" | S for judgments and rulings; "design" unsettled | 7328f4 2026-09-30 "decisions and making rulings and judgments". The book's own text withholds design against implementation, yet the figure places "design" in the Primary box. |
| "aggregated, investigated" | S | 93ba9f/vision/primarySeats.md 2026-09-26. |
| "SECONDARY (secretary)" | S | d4ae97/vision/flow.md 2026-10-07; 28d847/vision/layers.md 2026-10-03. |
| "all messages in and out" | X; Q | See S3 of the proposal. |
| "coordinates the work" | S | 7328f4 2026-09-30 "use the layer underneath to coordinate the work". |

### Context paragraph

| Statement | Verdict | Deciding record |
|---|---|---|
| "The first edition's three proposals are landed." | S | psyche-skills c3f8eeb («vision-aspects: new; vision-model-roles: roles by layer»); both vision-aspects sections and «Roles are explained by layer, not by model» are present at 9bba4bf. |
| "since 2026-09-26 about the Primary layer has no landed line" | S for the landed claim; date start narrow | No psyche-skills line has "secretary" or "spoken to least" (grep at 9bba4bf). Earlier records on the subject exist: f55ec8/vision/layers.md 2026-09-16 (brainstorm, "Fable bothered as little as possible"), b81560 / b05237 2026-09-19, 0625c3 2026-09-20. |
| "the line that carried «spoken to least» was removed with «Speech across aspects»" | S, with nuance | 850fd27 (approved 2026-10-09) removed "...Sol speaks to Opus, not to Fable; Fable is spoken to least." That line said Fable, not the Primary layer. He approved the version without it (vision-aspects c3f8eeb, same day); the book does not say so. |
| "your comment of 2026-10-03 asked for the layers to be named" | S | 5578cc/vision/flow.md 2026-10-03T15:43 "Maybe we want to put in the layers there"; 41fa34/vision/speech.md 2026-10-03 "We should be using the layer vocabulary". |
| Six record paths and dates | S | d4ae97 entry dated 2026-10-07 in the record (the file was first added 2026-10-06); 28d847 layers and 41fa34 speech 2026-10-03; 7328f4 2026-09-30; caf622 2026-09-28; 93ba9f 2026-09-26. |
| "2026-10-03: the Primary designs, the Secondary implements; 2026-10-07: Mind's Primary designs and implements through its own subflows" | S; "Mind's" is inference | 28d847/vision/layers.md 2026-10-03; d4ae97 2026-10-07 says "Astra is primary", with no aspect. |

### Proposal 1, new section in vision-aspects

| Statement | Verdict | Deciding record |
|---|---|---|
| "The Primary layer is spoken to least" | S | As in the figure. |
| "it is the most expensive" | X; Q | caf622/vision/Fable.md 2026-09-28 says it of Fable, the model: "because it's the most expensive model". Moving a model's cost onto the layer conflicts with landed vision-model-roles «Roles are explained by layer, not by model». It is also an explanation, not a ruling. |
| "kept for hard problems, decisions, rulings and judgments" | S; Q | 7328f4 2026-09-30 (his words are "your own higher aspect, or a higher aspect or more primary aspect", read here as layer: G, ambiguous). Qualified by d68c82/vision/model-roles.md 2026-10-11 ("all the books should be made by Fable unless ... trivial") and ebbe30/vision/aspects.md 2026-10-09 (the psyche Primary's job is "to give me vision designs"). The Primary also does book and design work. |
| "A flow aggregates its thoughts and investigates before it speaks to a Primary." | X (mild) | 93ba9f 2026-09-26: "They should usually aggregate some thoughts together and investigate". "Usually" is dropped. |
| "The Secondary is its Primary's secretary" | S | d4ae97 2026-10-07; 28d847 layers 2026-10-03; d68c82 model-roles 2026-10-11 "You're just the secretary". |
| "every message to the Primary goes in through it" | X; Q | 28d847 layers 2026-10-03 was a role given to one seat at a restart, and the same record says "Fable can talk to Astra". 41fa34/vision/speech.md 2026-10-03T15:11: "Primary can talk to other primaries". d4ae97 2026-10-07 binds a Secondary ("you're secondary") and the levels below, not every sender. The living speaks to Primaries himself. |
| "and every message out comes through it" | Q | d4ae97 2026-10-07: Astra "uses his own subflows ... doesn't need to use Sol", and messages go "any level down". ebbe30/vision/aspects.md 2026-10-09: the psyche Primary "ask[s] mind". Only 445410/vision/messaging.md 2026-10-09 ("responds back to its secretary") supports the outbound half, and only for the topic answer. |
| "it coordinates the work below" | S; "below" is the book's | 7328f4 2026-09-30 "the layer underneath to coordinate the work"; d4ae97 "keeping track of everything that Primary is working on". |
| Home: vision-aspects | Q | d4ae97 2026-10-07, in the very passage that says "hard-enforced": "I guess this is basic intent ... It's still going to be a system prompt". The book does not show that he placed the secretary rule at intent. |

### Ruling 2

| Statement | Verdict | Deciding record |
|---|---|---|
| "on 2026-10-03 you said of speech between layers «It's not a hard rule; it's guidance»" | S; book rule | 41fa34/vision/speech.md 2026-10-03T15:11 (said of Sol not reaching Fable, which is cross-aspect and cross-layer). Quoting him back breaks vision-book: "A book does not restate the living's words." |
| "on 2026-10-07, of the secretary, «I want that hard-enforced»" | S; book rule | d4ae97/vision/flow.md 2026-10-07. The same passage says the messenger "cannot actually enforce this" and calls it intent. Not shown. |
| (omitted) 2026-10-03 17:49 "I never meant that ... I'm expressing myself through examples" | Q | 41fa34/vision/speech.md 2026-10-03 17:49 (from 5578cc/vision/behavior.md). This is his strongest word against rule-form, and the book does not show it. |
| "The section above states the secretary as a rule and the rest as posture." | wrong of its own text | The section is four flat declaratives in one register. Nothing in its wording marks one sentence as a rule and the others as posture. |

## Omitted records with direct bearing

- bad807/vision/gatedFlows.md 2026-10-04: a high-cost design flow is gated, messaged only through a secretary, and its input is reviewed. This supports "in through it" and adds a review, but neither book shows it.
- 4ddfe1/vision/voice-relay.md and 445410/vision/messaging.md 2026-10-09 «Design and review talk reaches Opus through the relaying seat»: the living talks to a Secondary through a relaying Quaternary. This bears on both books.

## Sources

- `/home/li/primary/flows/33752b/books/9-words-travel-as-psyche.md`, `/home/li/primary/flows/33752b/books/10-aspects-same-layer-2.md`
- `/home/li/primary/flows/33752b/reports/packet-2-brief.md`
- `/home/li/primary/flows/d68c82/reports/fable-packet-undistilled-2026-10-12.md`, sections B (lines 367–880) and C (881–1197)
- `/home/li/primary/flows/d68c82/reports/delegates-book-check-2026-10-12.md` (method)
- Records read in full: d68c82/vision/messaging.md, model-roles.md; 4ddfe1/vision/messaging.md, voice-relay.md; 445410/vision/messaging.md; 28d847/vision/messaging.md, layers.md; b7da5d/vision/layerVocabularyAndReview.md; e51411/vision/messaging.md; 183ae0/vision/seats.md; d4ae97/vision/flow.md; 41fa34/vision/speech.md, layers.md; 7328f4/vision/seats.md; caf622/vision/Fable.md; 93ba9f/vision/primarySeats.md; bad807/vision/gatedFlows.md; ebbe30/vision/aspects.md; 5578cc/vision/flow.md (all under /home/li/primary/flows/)
- `/git/github.com/LiGoldragon/psyche-skills` at 9bba4bf: skills/vision-messaging.md, vision-aspects.md, vision-model-roles.md; commits 850fd27, c3f8eeb
- Record add dates: `git log --diff-filter=A` in /home/li/primary
- Provenance receipt: unavailable, because no PROVENANCE handoff exists for this thread.
