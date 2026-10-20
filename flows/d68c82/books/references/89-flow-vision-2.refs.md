# References: Flow's vision, second edition

Records are the living's, as other flows logged them; paths are under /home/li/primary/flows/. The records are never shown in the book. Base module: psyche-context vision/flow.md at origin/main 1535807, which already carries commit a83cbd0 (two sentences removed, "a run of a metaflow"). The first edition is 80-flow-vision.md (refs: references/80-flow-vision.md); it stays unchanged because it has comments.

## Today's records (flows/d68c82/vision/flow.md unless named)

- Proposal 1 (voice out of the description line): "A flow is one run of a metaflow" (book comment 2026-10-19T17:27: "Let's get rid of that voice vocabulary. Consistency"); log.md 2026-10-19 17:26-17:33.
- Proposal 2 (a flow's model need not be an LLM): "A flow's model need not be an LLM" (17:28: "It could be a system one also ... an audio or a video model or whatever"). "System one" is read as System 1, psyche-context vision/system-one.md (Jev); that reading is unwitnessed and is the first question of Proposal 34.
- Proposal 3 (the finishing flow messages the flow that needs to know): "The flow that finishes tells the flow that needs to know" (typed; about book subflows sleeping on timers).
- Proposals 4, 5, 6 (simplified flow; renamed from lean flow by "A simplified flow", 17:47): "A lean flow: a judgment-only call whose response is its message"; "Lean flows: a system prompt, whole tools, a presentation as the only answer"; book 85 and its refs (references/85-lean-flow.refs.md). Proposals 5 and 6 are the alternatives of book 85's proposals 10 and 11 under the new name; the line 13 wording "clean lean flows" is the 2026-10-14 bootstrap record.
- Proposal 7 (the flow ethos, a domain-specific language in Ethos, no Nix-language analogy): "A flow is specified whole, in Datom" (typed); "No Nix-language analogy for the flow specification" (17:46); "Flow ethos, not flow definition" (17:47); book 86 and its refs. The module is the flow ethos (the existing vision-flow-ethos), never "flow-definition".
- Proposal 8 (the topic an open enum): flows/d68c82/vision/ethos.md "An open enum, and the camel ID" (17:33); book 87 and its refs.
- Proposal 14, 15 (subflow sections long term): "Subflows replacing the subagent tool is long term, stated broadly" (17:45). Book 91 «Subflows, long term» carries the same removal with its own alternatives; Proposal 14 repeats its removal lines so that this book is complete, and the two must land once.
- Proposal 22 (ephemeral flow): "The ephemeral flow: a continuous job flow with a context ceiling" (comment on «Refreshing the Illustrator» 3rd edition, 2026-10-17 19:03: 300,000 tokens maximum and 250,000 to wind down with Claude; a smaller figure for Codex; "some flows could even be allowed to compact"); "The Illustrator does all waiting jobs in one flow".
- Proposals 31, 32 (voice out of the Nexus vision): same 17:27 comment; psyche-context vision/nexus.md "Three parts and one path". Witnessed: the existing example in that section, run through the pinned ethos-zero (07714b0) as one block, is refused (Arity: four roots in one file); the new blocks are four files, each accepted. This follows d68c82/vision/ethos.md "One Ethos file holds one main object". Address.{ Aspect Topic Layer } is the name flow's library already uses (crates/flow-ethos/ethos/library.ethos, Address); Metaflow there is the record that Address keys. The living wrote "Metaflow, or the { Aspect Topic Layer } address"; Address is used; Metaflow in its place would be a one-word change. Answer.[ Succeeded Failed ] is added to the Memory block because the Datom example uses Succeeded and every variant it uses must be defined; it is the author's, not the living's.
- Proposal 33 (vocabulary): mind-context origin/main d581978, knowledge/vocabulary.md line 6.
- Proposals 34-36 (inquiry modules): the unknowns of Proposals 2, 3 and 22. Nothing in them is a witnessed result; "to try" lines are candidates.

## First-edition proposals carried (references/80-flow-vision.md has the records)

- Proposal 9 (was 1; the figure kept; the bootstrap sentence it followed was removed by a83cbd0, so its context line is the line now in the module). Overlaps psyche-context vision/nexus.md "Three parts and one path", which says every Nexus has the three parts; the first sentence is the part to lean out if the living rules it repeated.
- Proposal 10 (was 2); 11 (was 3, its second sentence only; the first is replaced by Proposal 7); 12 (was 4); 13 (was 5).
- Proposals 16, 17 (was 8, 9; CONFLICT); 18, 19 (was 10, 11; CONFLICT; 128,000 against 200,000; the ephemeral figures of Proposal 22 are for that kind only); 20, 21 (was 12, 13; CONFLICT; 21 is supported again by the 2026-10-17 19:03 record); 23, 24 (was 14, 15; CONFLICT; also 2026-10-14 "A still-young working transcript", around 100,000 tokens where average context degrades); 25 (was 16); 26, 27 (was 17, 18; CONFLICT).
- Proposal 28 (was 19, Alternative A). Dropped: the old Alternative B (give the heading a body naming a flow after its ancestor) is superseded: the landed dde8584 deleted the ancestor-naming sentence at the living's ruling (log.md: "ancestor sentence deleted"; "Heading ... now empty: ruling asked").
- Proposals 29, 30 (was 21, 22; CONFLICT; psyche-context vision/ethos.md). The existing section text names the "vision-flow-ethos skill", an ethos-named module.
- Dropped as moved to the subflow book (book 91): first-edition Proposals 6 and 7 (a subflow's kind: "depends on its use" against "essentially the same thing"), anchored in the subflow text that Proposal 14 removes. Their records: d68c82/vision/flow.md 2026-10-14 "A subflow's kind depends on its use"; da2038/vision/subflows.md 2026-10-14.

## Method

- Book source checked by tools/book-check.mjs; ethos blocks by the builder's pinned ethos-zero. Figures drawn by the illustrator agent and checked by a separate reader against the ASCII sources.
