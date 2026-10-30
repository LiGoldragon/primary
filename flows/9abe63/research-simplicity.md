# Research: simplicity for a Nexus that composes flows from belief

Order (9abe63/vision/curriculum.md, 2026-10-30): Curriculum keeps running, its development stops; a new Nexus is designed before any code; "simple... no haywire, duct tape, and exceptions... edge cases, and special scenarios."

Quote status: CONFIRMED = read in a primary text this session; SECONDARY = same wording in several secondary sources, book not opened; UNCONFIRMED = from memory or paraphrase.

# Part 1 — Thinkers, each an option the design can draw on

## Rich Hickey, "Simple Made Easy", Strange Loop 2011 (https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md)
- "Simplicity is a prerequisite for reliability." CONFIRMED.
- "the roots of this word are sim and plex, and that means one fold or one braid or twist." CONFIRMED. Simple is objective: count the folds.
- Complect: "It means to interleave or entwine or braid." CONFIRMED. Simple things have "one role", "one task or job", "one concept", "one dimension of the problem". CONFIRMED.
- Easy is "to lie near", "about being familiar". CONFIRMED. Easy is relative to the person; simple is not.
- Option for the Nexus: judge each part by what it is braided with, not by how familiar or quick it is. One role per part: compose a prompt, or track a flow, never both. Reaching for the familiar thing (a file, a flag, a git repo as data store) is "easy", and it is where braids come from.
- Test it gives: name the part's single role in one sentence without "and".

## Fred Brooks, The Mythical Man-Month (1975); "No Silver Bullet" (1986/87)
- "I will contend that conceptual integrity is the most important consideration in system design." SECONDARY (Mythical Man-Month, 1975). It follows that design proceeds "from one mind, or from a very small number of agreeing resonant minds". SECONDARY.
- "The essence of a software entity is a construct of interlocking concepts." CONFIRMED (https://www.cgl.ucsf.edu/Outreach/pc204/NoSilverBullet; UNC TR86-020, IEEE Computer Apr 1987).
- "I believe the hard part of building software to be the specification, design, and testing of this conceptual construct, not the labor of representing it." CONFIRMED (first half; second half SECONDARY).
- "The complexity of software is an essential property, not an accidental one." CONFIRMED. Complexity "makes overview hard, thus impeding conceptual integrity." CONFIRMED.
- Option: spend the design on the essence (belief -> composed prompt for an address) and refuse accidental machinery (rebuild triggers, reseeding, per-harness templating as separate paths). One concept set, owned by one designer (the living plus the Primary), written before code.
- Test it gives: every proposed feature is sorted essential or accidental; an accidental one is removed, or placed outside the Nexus.

## John Ousterhout, A Philosophy of Software Design (2018), ch. 2-4, 9
- "Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system." SECONDARY (several summaries; book not opened). Two causes: dependencies and obscurity. SECONDARY.
- Deep module: "small interface, lots of functionality" CONFIRMED in his Stanford CS190 notes (https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign); same notes: "Pull complexity down into modules", "make classes somewhat generic".
- Special cases as a symptom: the book's argument is that special cases come from a too-specific interface and are removed by a more general one; exact sentence UNCONFIRMED.
- Option: one narrow entry ("compose the prompt for this address") with the hard work behind it; the caller carries no mode flags. A special case in the caller is read as a missing generality in the module.
- Test it gives: count the things a caller must know to use the part; if the number grows with each use, the module is shallow.

## C.A.R. Hoare, "The Emperor's Old Clothes", Turing lecture 1980, CACM 24(2), 1981
- "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult." CONFIRMED via a quoting page (https://www.unix-ag.uni-kl.de/~guenther/hoare-on-software-design.html); lecture text itself not opened.
- Option: the acceptance criterion is that a reader can see the design is right by reading it. A design whose correctness needs a test matrix, an exception list or a history to explain is the second kind.
- Cost it names: the simple way is harder and slower; the design stage must be given the time.

## John Gall, Systemantics (1975; later "The Systems Bible")
- "A complex system that works is invariably found to have evolved from a simple system that worked." SECONDARY (https://lawsofsoftwareengineering.com/laws/galls-law/); not established as verbatim from the book. Its companion: a complex system designed from scratch does not work and cannot be patched into working. SECONDARY.
- Option: the Nexus begins as the smallest one that works end to end (one address in, one composed prompt out) and grows only by adding what the working one demands. It is rewritten whole, not grown from Curriculum (this fits "full rewrite").
- Tension to surface: Gall says grow from a working simple system; the living orders a full rewrite. The reconciliation is that the simple system is new and small, and Curriculum is not its ancestor.

## Edsger Dijkstra
- "Simplicity is prerequisite for reliability." CONFIRMED via Wikiquote (https://en.wikiquote.org/wiki/Edsger_W._Dijkstra), EWD498, 1975. "Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it." CONFIRMED via Wikiquote, EWD896, 1984.
- Separation of concerns: "the only available technique for effective ordering of one's thoughts, that I know of"; attending to one aspect "does not mean ignoring the other aspects... the other is irrelevant" from that aspect's point of view. CONFIRMED, EWD447 "On the role of scientific thought", 1974 (https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD447.html).
- Option: separate what the Nexus says (signal), does (operation) and remembers (memory) exactly as nexus.md already splits them; hold each concern in its own text so a reader attends to one at a time.
- Cost it names: simplicity needs hard work and education; a design review is a teaching act for the model flows that will read it.

## David Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules", CACM 15(12), 1972
- Decompose starting from "a list of difficult design decisions or design decisions which are likely to change." CONFIRMED (https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html).
- "Every module in the second decomposition is characterized by its knowledge of a design decision which it hides from all others." CONFIRMED. "Its interface or definition was chosen to reveal as little as possible about its inner workings." CONFIRMED.
- "It is almost always incorrect to begin the decomposition of a system into modules on the basis of a flowchart." CONFIRMED. Do not cut the Nexus along the processing order (read belief, assemble, send).
- Option: list what is likely to change (harness, model, belief repository layout, module kinds, prompt shape, the Capsule backend) and hide each behind one part. The things that change often become configuration (spirit-core: configurable over hardwired).
- Test it gives: a change to one decision touches one part.

## Alan Perlis, "Epigrams on Programming", ACM SIGPLAN Notices 17(9), Sept 1982 (https://cs.yale.edu/homes/perlis-alan/quotes.html; epigram numbers not confirmed)
- "Simplicity does not precede complexity, but follows it." CONFIRMED.
- "Fools ignore complexity. Pragmatists suffer it. Some can avoid it. Geniuses remove it." CONFIRMED.
- "Symmetry is a complexity-reducing concept (co-routines include subroutines); seek it everywhere." CONFIRMED.
- "You can't communicate complexity, only an awareness of it." CONFIRMED.
- "In seeking the unattainable, simplicity only gets in the way." CONFIRMED (a counterweight: simplicity is a means, not the goal).
- Option: the simple form is found after the complexity is understood, so the design starts from every angle the living asked for, then removes. Prefer one symmetric shape for all addresses (Psyche, Mind, Field; four layers) over per-aspect branches; removal over addition (matches belief-modules.md: "Removal comes before addition").

## Cross-cutting reading for the Nexus (inference, not a quote)
Five questions the sources share: What is the one role? What changes, and is it hidden? Is the correctness visible by reading? What can be removed? Is there a working small version? An "exception" in the living's sense is a place where the answer to one of these is "it depends".

# Part 2 — Vision records, by subject

Raw record ids are flow id / file / heading. Quotes are verbatim and short.

## Curriculum
- 9abe63 / vision/curriculum.md / 2026-10-30 "Curriculum's development is abandoned; a new Nexus is designed first, simple, without duct tape, exceptions or special scenarios": "we're going to abandon development of the curriculum Nexus. This will become more and more of a standard full rewrite, where obviously we're not writing anything now. We need to design something first." and "The system must be simple, in a way of speaking."
- 9abe63 / vision/belief-modules.md / 2026-10-30 "Slash and burn": "curriculum doesn't use anything outside of the three belief repositories: nothing, zero." and "That's data and code, which is forbidden." and "Hashes do not go."; types per role: "a main flow type and a subflow type".
- 9993b5 / vision/curriculumNexus.md / 2026-09-17: "this is where we want to go towards curriculum being a nexus... we can reset it through Nix, of course, or repopulate it, reseed it from Nix."
- 108ab0 / vision/operational-curriculumAsModuleSystem.md / 2026-09-17: "if curriculum is a nexus, we can't have any data there because it's going to keep rebuilding it... It's like a manifest that gives it a bunch of paths... and gives the type of each."
- 108ab0 / vision/operational-curriculumSkillsRepo.md / 2026-09-17: "Just give them a name for what they are: curriculum skills."
- 48cff7 / vision/curriculumSubagentGap.md / 2026-09-16: "Maybe there's a namespace for different elements to generate different skills, but we're just going to go with how it works for now." (Curriculum deletes files not authored in it; roles.datom is permission x depth only.)
- 752e0f / vision/curriculum.md / 2026-09-24: "Curriculum takes different repositories that have special files that we recognize... Every signal can be a different repo... You should create kind of a library, a nexus library, to handle all of this" (the revamp the living now abandons).
- 26c50c / vision/curriculum.md / 2026-09-24 (two entries): "We're going to have different types... One of its queries is going to be by type: generate or regenerate the skills in the target repository"; "The type is assigned to the repo. It's centrally controlled".
- 28d847 / vision/curriculum.md / undated headings: "Edits in the workspace regenerate per harness"; "I want to concentrate on creating better context modules... and continue developing Flow."
- 5578cc / vision/curriculum.md / 2026-10-03 "One standard for context modules, populating both skills and the system prompt; the name stays Curriculum": "a standard for now that Flow can use and that we'll also implement in curriculum".

## Psyche nexus
- 97bb3e / vision/psyche-nexus.md / 2026-10-24 "Psyche, the nexus that manages the machines' context, is reanimated": "a psyche component, a nexus, software that was the original approach to managing the machines' context." Also "The file-based approach is failing; Psyche nexus is back on the table"; "every flow only knows what it's told"; "The judge is going to not just be one thing. It's going to be several things in several places".
- b49eaf / vision/psyche.md / 2026-10-28 "The Psyche Nexus is a parallel, independent implementation; hard cuts over incremental change": "a completely parallel and independent implementation of Psyche. It would not in any way reuse the legacy system or be compatible with it in any way."
- b49eaf / vision/vocabulary.md / 2026-10-28: "Flow Nexus, Mind Nexus, Psyche Nexus, to differentiate".
- b2b87a / vision/renewal.md / 2026-10-29 (also archived): "the psyche nexus, which is super high on my list... Curriculum would hook up into that, or maybe Flow hooks up directly into psyche instead, to feed the new flows with their psyche, with their vision, with their intent, with their spirit"; ancestor Spirit "had a review process that would call an LLM... forcing it to crystallize right out of the gate"; "I think we should abandon the compensation modules".
- e51411 / vision/nexus.md / undated heading "The tools are the nexuses": "Psyche Nexus is going to replace how we log Psyche and Mind."
- 827b1d / archive/vision/psyche.md / 2026-10-28 "Long term, the records live in the psyche nexus": "the long term is the psyche nexus obviously." Landed in repos/psyche-belief vision/psyche.md (3a12dc).
- d68c82 / vision/psyche.md / 2026-10-12: "This is why I want to develop the Psyche Nexus, which then, when a machine uses the Psyche tool, can get that content loaded into its middle stratum."
- d9065e / vision/records.md / 2026-10-29: "this is all going to be solved by a well-functioning psyche nexus."
- 9993b5 / vision/psycheVsMind.md / 2026-09-17: "if you're searching Psyche, you want to search all layers."
- b81560 / vision/operational-refreshFlowAndMessageFlowCoordination.md: "there's going to be a psyche nexus" (date not read).
- Crystallized: repos/psyche-belief vision/psyche.md "A settled record moves to the archive" ends "In the long term the records live in the psyche nexus and the state is a field."; vision/psyche-aspect.md (core Secondary is the hub); vision/nexus.md (a Nexus is the whole; Signal / Operation / Memory; "Universal traits first"; "Why everything is a Nexus").

## Flow composing prompts
- Crystallized, repos/psyche-belief vision/flow.md "Starting flows": "A launch names the metaflow, the belief modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry."; "A fresh flow's first prompt carries the raw psyche relevant to it and recent, together with the belief modules relevant to it, of any kind except spirit and intent, which sit in the system prompt."; "A flow is specified whole, in Datom, by a domain-specific language in Ethos"; "A fresh flow starts with every belief module its metaflow is bound to"; "To the Nexus, a module's location is its registry entry."; "Long term: modules checked by hash... short term, no check is made."; "Every belief module lives outside it [the flow repository]... so that a module changes live."
- Crystallized, vision/belief-modules.md: "A module declares its placement: the system prompt, or loaded on demand." (the Slash and burn record of 2026-10-30 above reverses part of this: "no hashes, data or code").
- 554e1a / vision/belief-modules.md / 2026-10-29: "the flow designing the Flow Nexus has zero need to know how to make a book"; "A flow's brief and default work are composition, not remembering"; "Make sure all of the flows are configured with the proper modules that they should have when they start."
- a68420 / vision/flow.md / 2026-10-23 (book comment): "The word 'skill' is just a legacy interface name for context modules... not intent, not long term anyway, because intent should be in the system prompt itself."; same flow: "you only have 60,000-token context right now... This is a total failure."
- aa887c / vision/fableContext.md / "The first prompt is not the whole corpus": "That's way too much. It would make the context too big from the first prompt."
- d68c82 / vision/context-modules.md / 2026-10-16: "I don't want any context modules to live anywhere else except these three repos. I want this enforced... categorically"; 2026-10-16 11:29: "They have to be composed with all of their context modules in there so they can just be generated depending on which context module they should have."
- 836818 / vision/flowNexus.md / 2026-09-23: "It has to have a way to compose the prompts: the first prompt and eventually a way to compose the system prompt but we can start with the prompt."
- 108ab0 / vision/operational-programmaticPromptComposition.md / 2026-09-17: "We can programmatically compose, essentially, a prompt for something simple to access now to easily compose agents."
- 108ab0 / vision/operational-promptMosaicComposition.md / 2026-09-17: the successor's prompt "an amazing mosaic".
- 108ab0 / vision/operational-skillTypes.md / 2026-09-17: "decompose your sub-agent prompt building into these types of personality, behavior..." (types as decomposition; heading read).
- 108ab0 / vision/operational-flowDatomLauncherLanguage.md / 2026-09-17: "launch flows with a simple Flow Datom language, with all the preconfigured defaults for a short version."
- 38dec9 / vision/invocationSystem.md (undated): "create the system call with the right flag to invoke the harness with the right system prompt or the right top stratum."
- b05237 / vision/operational-fatPromptAndCustomSystemPrompt.md: "a fat first prompt, maybe even a custom system prompt" (superseded in size by aa887c; dates not read).
- 5851f4 / vision/thinkingPhases.md: "creating specialized system prompts, essentially creating differently programmed harness calls" (date not read).
