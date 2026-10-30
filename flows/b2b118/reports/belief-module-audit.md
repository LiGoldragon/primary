Artifact URL of Modules by role and function (flows/554e1a/books/flow-composition.md, commit a9b29b): https://claude.ai/artifact/MnGEHWjFRXgsFu2mtkbc9y
[W] flows/554e1a/publications/a9b29bbfacbf7fc367f17a10cdbe4432bf2fe8762d3ec7d4c85ef002d63e674f/publication lines 1-2 (`source .../books/flow-composition.md`, `url https://claude.ai/artifact/MnGEHWjFRXgsFu2mtkbc9y`).

# Belief module audit, 2026-10-29

Tertiary audit for b2b118. Marks: [W] witnessed (file:line or command), [I] inferred.

## Scope, and what the audit could not settle

- [W] The Primary's local checkout (HEAD 9ca5f1b41) and origin/main (790aae4d0 when read) have diverged: `git rev-list --count origin/main..HEAD` = 57, `HEAD..origin/main` = 42. Records the Secondaries wrote (for example flows/046782/vision/*, flows/9aaaba/vision/belief-modules.md, flows/7459f3/vision/*, flows/2933ce/vision/energy.md and proposal.md, flows/87f1ee/what-he-wanted.md) are in the local history and absent from origin/main (`ls` on a worktree at origin/main). Record paths below are local-HEAD paths; "(not on origin/main)" marks the ones I checked.
- [W] The Curriculum checkouts under /home/li/.local/state/curriculum-context/ are at psyche-context 6f70281, mind-context 95c90eb, field-context f02af7a, each equal to its `refs/remotes/origin/main`. A module's identity is its path: `intent/living-interaction.md` is `intent:living-interaction`. The only registry file in the checkouts is field-context/roles.datom (subflow roles, hyphen IDs); the served module set is the file tree. 151 module files: 40 vision, 16 intent, 2 spirit, 44 knowledge, 34 role, 11 compensation, 4 evidence.
- [W] The declarations live in the Flow Nexus Configuration, not in a repository file. repos/flow has no declaration; repos/flow-data holds a README only; the local CriomOS-home checkout is at 437455a4 (2026-10-22), 21 commits behind origin and lacks the source commits named in configuration-today.md (`git cat-file -t c1a0b09...` fails). So the live declarations come from /home/li/primary/flows/b2b118/reports/configuration-today.md (it was present when I looked; no wait was needed), and the pre-today baseline is /home/li/.local/state/curriculum-040/flow-040-configuration-before-2026-10-27.datom. "Since the declaration was ruled" is read as "since that 10-27 snapshot"; the date the living ruled each row is not recorded anywhere I found [I].
- Sections 1 and 2 cover what I read: the commit log of the three context repos since 2026-10-28 and the records those commits trace to. There are 184 dated headings from 10-28/29 in flows/*/vision, archive, notion. Stage 3 (after the origin/main reconciliation, which brought in the local-only records) read in full the half first read by heading only: 2933ce {belief-modules,book,energy,evolution,messaging,psyche,remembering,vocabulary} and notion/messaging; 554e1a {belief-modules,collaboration,flow,remembering,proposal}; 73b5d8 {belief-modules,evolution,flow,proposal,psyche,remembering}; 787230 {anatomy,evolution,messaging,model-roles,proposal}; 7b6597/design; 827b1d {book,flow,living-interaction,main-flow,proposal}; b2b87a {field,design,messaging,belief-modules} and notion/belief-modules; b49eaf {archive-messaging,book,energy,ethos,flow-nexus,main-flow,model-roles,psyche,remembering,spirit,vocabulary}, all under flows/<id>/vision/. 177 dated 10-28/29 headings are in the tree at origin/main (8202485) after the archive moves. "Source not located" means I did not find his approving words; it does not mean none exist.

## 1. Lines the living approved since 2026-10-28

Landing commit is the context-repo commit (`git log` in the checkout). Approval is where his words are recorded.

### Psyche context (psyche-context)

| Line (text, short) | Approved where | Landed |
|---|---|---|
| A higher module type never depends on a lower one; spirit least of all on compensation | flows/046782/vision/belief-modules.md:3 (direct, 10-28), commit messages say ruled/approved 10-28 [W] | 95b41c8 (spirit), 150e598 (belief-modules) |
| Orders are beads, opened on receipt, closed when the doing is witnessed; remembering includes open beads; psyche-interaction renamed living-interaction | flows/7b6597/vision/belief-modules.md:8 "Those are approved."; records.md:3 [W] | 632e2d0; the psyche-to-living rename 5b0a0b5/85b9f1e (psyche-context), mind-context 5b0a0b5, 6a6c128, fbbc49a, field-context e5b5a78 |
| What he asks to be checked is an order, not vision | commit message "approved by the living 2026-10-28"; his words not located | be2e92d |
| What a Fable flow thinks it writes itself or hands to another Fable flow, never down | flows/046782/vision/belief-modules.md:8 (approving the line) [W] | f2b0047 |
| intent:fable, a new module | flows/9aaaba/vision/belief-modules.md:10 "The first one is good."; flows/7b6597/vision/model-roles.md:8 [W] | d8a1b83 |
| The fallback changes the carrier, never the address | commit message "approved by the living 2026-10-28"; related words flows/b49eaf/vision/messaging.md:3 and flows/5bbab2/vision/messaging.md:3 (practice, not enforced) [W]; approving words not located | 09ce727 |
| His words are relayed in his words | flows/b49eaf/vision/messaging.md:9; flows/72b114/archive/vision/living-interaction.md:2 [W] | 31655ef |
| A proposal is signed with the models that made it; the stand-in is marked | flows/b49eaf/vision/proposal.md:13 "The signed proposal is approved." [W] | 5d81baa |
| Model beliefs; models named by layer; the asymmetric line stays | flows/7459f3/vision/archive-model-roles.md lines 3-18 (last: "approving the book Model beliefs"); (not on origin/main) [W] | 6642b8c |
| The system is understood energetically | flows/72b114/archive/vision/model-roles.md:5 [W] | 3354a1f |
| A settled record moves to the archive | flows/827b1d/archive/vision/psyche.md:3 ("Landed: vision/psyche.md, 3a12dc") [W] | 3a12dc5 |
| Chat answers are short, long goes to a presentation; a belief change goes to him as a proposal | flows/7459f3/vision/archive-living-interaction.md:5,10 (not on origin/main) [W] | ba3989c |
| The ghost effect as spirit; the ghost hunt over modules | flows/7459f3/vision/archive-spirit.md:5,10 (not on origin/main) [W]; the hunt commits (about 30, "ghost hunt, the thing as wanted") match line 10 [I] | 0ed3ad8; ghost-hunt series 10-28 |
| No EDN anywhere, it is all datom | flows/9aaaba/vision/flow.md:26 (not on origin/main) [W] | 661f31f (psyche), 75cc9d1 and 2635970 (mind) |
| No ASCII figures; a flowchart language rendered as a graphic | flows/9aaaba/vision/book.md:3 [W] | 1d3c853, 576e70c (mind 0abb408) |
| The database is Memory, never sema | flows/9aaaba/vision/memory.md:8 [W] | mind-context 536a903 |
| Delete compensation:psyche-interraction | commit message "by the living's order 2026-10-28"; words not located | 4292773, field-context 4e327b1 |
| The chat carries the link and one sentence (later replaced by the link alone) | commit message "correction by the living 2026-10-28" | 46138f6; replaced by a6fd92d |
| A text is measured by the energy it costs (intent:energy) | flows/87f1ee/energy-second.md:7 says "You found the energy line good"; this is a flow's account of his ruling, his own words not located [W] | 0162bb2 |
| A text for the living is as small as its point; a chat he does not read is empty | flows/2933ce/vision/proposal.md:3 "Briefness to the Living is good in entirety and can be landed." (not on origin/main) [W] | 02990c0 |
| Anger sensed in the living is named at once and the rest waits | flows/2933ce/vision/living-interaction.md "Comments on the book Anger, second edition", Proposal 2, 17:17 "Good" [W] | a836e1c |
| A hard word from the living is a truth, not anger | flows/2933ce/vision/living-interaction.md "Comments on the book Hard words are truths", 18:33 "Good"; flows/787230/archive/vision/living-interaction.md:10 [W] | 52aae3f |
| The living is answered where he speaks; the module keeps only what his words hold | words not located. flows/554e1a/vision/living-interaction.md:3 and flows/87f1ee/answers-to-comments.md (Proposals 1-5) are the nearest [I] | a6fd92d |
| What he wanted: messaging, blocking, collaboration, flow compaction, main-flow lines, "A thinking machine keeps acting" | flows/87f1ee/answers-to-comments.md Proposals 1, 2, 4 say "lands for now"; the comments themselves not located [W/I] | c984eeb |
| The implementation-detail line is removed from main-flow | flows/787230/vision/belief-modules.md:40 [W] | 228c47e |
| A fresh flow remembers from the logs alone | flows/73b5d8/archive/vision/remembering.md:5 [W] | f9f3242 |
| The core Primary reaches a topic Primary directly | flows/554e1a/archive/vision/model-roles.md:3 [W] | d7c8268 |
| Vision code names the stacks; a landing archives its records; a superseded record is archived (P1, P2, P4, without the emphasis line) | flows/b2b87a/archive/vision/crystallization.md:5,12,21 [W] | 08643f3 |
| A vision record is made from his words alone (P3) | flows/b2b87a/vision/crystallization.md:5 "good" [W] | bb73fbe |
| Vision divided by horizon; a long line built in its time; a step is one thing | flows/b2b87a/vision/psyche.md:3-30 (seven comments, landable without his review); flows/554e1a/archive/vision/psyche.md:3,8; flows/b2b87a/vision/design.md:3 "good" [W] | c386f58 |
| The unmarked vision is the perennial vision | flows/b2b87a/vision/psyche.md:56 [W] | 6f70281 |

### Mind context (mind-context)

| Line | Approved where | Landed |
|---|---|---|
| Evolution is the dynamic procedure of improvement and redeployment | flows/2933ce/vision/vocabulary.md:3 (his word); flows/2933ce/vision/living-interaction.md "Comments on the book Anger, and the word evolution", 17:10 "Good" [W] | 2eff0f9 |
| Obsidian sync, comments, hosts, self-hosted sync, app (five modules) | flows/554e1a/vision/proposal.md "Proposals are written and commented in Obsidian, not Claude artifacts" and "A fresh Psyche pair, then a Mind pair, on Obsidian" (his order) [W]; his approval of the module texts not located | b6af9b8, 95c90eb |
| Curriculum context serving route (knowledge/nexus.md) | not located; reads as a Mind report, not an approval [I] | 35a46aa |

### Field context (field-context)

| Line | Approved where | Landed |
|---|---|---|
| Landing archives each drawn-on record in its commit | follows from the approved P2 above [I] | 76fe780 |
| Comment relay: each comment byte for byte, the older preserve clause goes | not located | 1194e49, f02af7a |
| psyche-core-primary-presentation: the pane answers the living | not located; he asked for its removal (flows/2933ce/archive/vision/living-interaction.md, "Comments on the book Hard words are truths", 18:37, 18:38) | 77feb34; removed in b31f587 |
| Typed configuration discovery and routed notifications | not located | 0ccd7b0 |

### Approved or ordered, unlanded in the checkouts

| Line | Where | State |
|---|---|---|
| The pulse is never shorter than an hour | flows/046782/vision/flow.md:3 "dont make the pulse shorter than an hour" | UNLANDED by the stage 2 lander: his words fix the content but not the line or the module; the line and intent/main-flow.md come from the machine's flow-composition proposal 3, which has no recorded approval |
| Everything is urgent | flows/7b6597/vision/belief-modules.md:15 "Oh, you're wrong. Everything is urgent." | UNLANDED: no line or destination in his words; proposal 3's wording is the machine's |
| A harness-blacklisted module removes the harness's shell-preference line | flows/046782/vision/flow.md:8 | UNLANDED: his words name a mechanism, not a module or its text; proposal 11's text is the machine's |
| Remove the psyche-core-primary-presentation module (2933ce, 18:37 and 18:38) | flows/2933ce/archive/vision/living-interaction.md | LANDED: field-context b31f587 deleted role/psyche-core-primary-presentation.md; served by Curriculum (role-psyche-core-primary-presentation: missing module) |
| Anger as a core belief | flows/2933ce/archive/vision/living-interaction.md, "make this part of the core belief"; "Good" on the redone line (Four spirit lines, Anger yields nothing good) | LANDED: psyche-context 2dc7d42 spirit/core.md "Anger yields nothing good, between any two beings." |
| Energy is the measure; the implementation is retaken; address to the whole self; a fault in conduct is a fault in belief | flows/b2b87a/archive/vision/spirit.md (five rulings, 23:01-23:03; the two to intent, one to spirit:psyche, two good) | LANDED: psyche-context 2dc7d42 (spirit/core.md, new spirit/psyche.md, intent/living-interaction.md, intent/belief-modules.md); spirit-psyche served at 2dc7d42 |
| His words are retrievable once every machine message in a pane is datom | flows/2933ce/vision/messaging.md "Right and that's a really good line to land somewhere" | unlanded; the line's destination is not in his words |
| Every flow starts with the proper modules; modules that do not serve a flow leave it; the Artifact tool and its prompt leave every Claude flow but the publishing one | flows/554e1a/vision/belief-modules.md (three sections, orders) | unlanded as belief; an order carried by the configuration work |
| The system never freezes; better to break things than stop acting | flows/b49eaf/vision/spirit.md, flows/827b1d/vision/flow.md | the spirit line "A thinking machine keeps acting" is in spirit/core.md (c984eeb) [I]; whether it holds his "high-level spirit" request fully is not settled |
| Only the Psyche core Secondary messages the Psyche core Primary | flows/b2b87a/vision/messaging.md:3 | order; the line in vision/messaging.md and model-roles keeps the practice wording |
| A proposal's signature names each model with its version | flows/2933ce/vision/proposal.md:3 | vision/proposal.md:39 names "the model"; version number not checked [I] |
| Mind Primary writes the code; Secondary is its secretary | flows/b49eaf/vision/model-roles.md:8 | not in a landed module; proposal 9 of flow-composition |
| Modules by aspect and layer; flows start with the right modules | flows/b2b87a/vision/belief-modules.md:3 (the 2026-10-29 words) | the vision is open; flow-composition is the proposal, unlanded |

## 2. Records the landings drew on

Archived (in flows/<id>/archive/vision/, [W] on origin/main and local):
- flows/554e1a/archive/vision/{belief-modules,model-roles,psyche}.md
- flows/72b114/archive/vision/{living-interaction,model-roles}.md
- flows/73b5d8/archive/vision/{belief-modules,remembering}.md
- flows/787230/archive/vision/living-interaction.md
- flows/827b1d/archive/vision/psyche.md
- flows/b2b87a/archive/vision/{crystallization,design,flow,psyche,spirit}.md (spirit added in 8202485, landed 2dc7d42)
- flows/73b5d8/archive/vision/spirit.md and the anger, anger-second-edition and hard-words sections of flows/2933ce/archive/vision/living-interaction.md (8202485; landed 2dc7d42 and b31f587)

Not archived though a line of it landed:
- flows/b2b87a/vision/crystallization.md (P3, landed bb73fbe)
- flows/b2b87a/vision/psyche.md (perennial, landed 6f70281; also holds unlanded words on the Flow redo)
- flows/2933ce/vision/vocabulary.md (evolution 2eff0f9); the rest of flows/2933ce/vision/living-interaction.md holds unlanded words
- flows/2933ce/vision/proposal.md (Briefness 02990c0); flows/2933ce/vision/energy.md
- flows/7b6597/vision/{belief-modules,records,model-roles}.md (beads, fable; 632e2d0, d8a1b83)
- flows/046782/vision/belief-modules.md (150e598, f2b0047)
- flows/9aaaba/vision/{belief-modules,flow,book,memory}.md (d8a1b83, 661f31f, 1d3c853, 536a903)
- flows/b49eaf/vision/{messaging,proposal,model-roles}.md (31655ef, 5d81baa); flows/b49eaf/vision/{energy,psyche}.md (comments behind 0162bb2 and the 2dc7d42 implementation line; the energy comments also hold unlanded long-term Fable words) [W, read in full in stage 3]
- flows/7459f3/vision/archive-{model-roles,living-interaction,spirit}.md (6642b8c, ba3989c, 0ed3ad8): file names say archive-, the directory is vision/, not archive/vision/
- flows/787230/vision/belief-modules.md (228c47e)
- flows/554e1a/vision/living-interaction.md
- Read in full in stage 3 and holding no approval beyond the above: 2933ce {belief-modules,book,energy,evolution,psyche,remembering}, 554e1a {collaboration,flow,remembering,proposal}, 73b5d8 {belief-modules,evolution,flow,proposal,psyche,remembering}, 787230 {anatomy,evolution,messaging,model-roles,proposal}, 7b6597/design, 827b1d {book,flow,living-interaction,main-flow,proposal}, b2b87a {field,messaging}, b49eaf {archive-messaging,book,ethos,flow-nexus,main-flow,vocabulary}: his words, orders and comments awaiting a proposal, not approvals [W].
- Books and answers carrying approvals: flows/87f1ee/{answers-to-comments,energy-second,what-he-wanted}.md.
[W] by `ls` at local HEAD; the b2b87a archive of psyche/design/flow was confirmed on origin/main. [I] "Not archived" for the rest: the rule that a landing archives its records (08643f3) came on 10-29 and these landings mostly precede it.

References of Modules by role and function (flows/554e1a/references/flow-composition.md, unlanded proposal): flows/73b5d8/vision/{spirit,evolution,flow,proposal,psyche,belief-modules,remembering}.md; flows/787230/vision/{anatomy,belief-modules,evolution,messaging,model-roles,proposal}.md and notion/belief-modules.md; flows/2933ce/vision/*.md (10-29) and notion/messaging.md; the books it supersedes (787230 placement-design, placement-design-2, composition-design, nexuses-design, hard-words-design; f6637e energy-third, strata, book-role, anger-second, only-the-link; 9aaaba/books/night-rulings.md; 7b6597/books/flow-five.md; 87f1ee/record-state-open.md); flows/554e1a/remembering.md and vision/proposal.md.

## 3. Registry against the declarations

Method [W]: module IDs read from the 151 files; module tokens read from the 10-27 snapshot and from the 16:56 live read in configuration-today.md; compared by script. Every module in every live row is in the registry. Of the 10-27 snapshot, only two tokens left the registry: `intent:psyche-interaction` (renamed `intent:living-interaction`, 632e2d0) and `compensation:psyche-interraction` (deleted, 4292773/4e327b1); also `inquiry:psyche-crystallization` (all inquiry modules deleted, d702b0b and mind-context 1850d49). Today's declarations carry none of them [W].

Registry changes since the baseline [W: `git log --name-status -M`]:
- New: intent:energy (0162bb2), intent:fable (d8a1b83), spirit:ghost (0ed3ad8), vision:account, vision:proposal (10-27), mind knowledge:obsidian-{sync,comments,hosts,self-hosted-sync,app}, field role:psyche-core-primary-presentation (f99396c, 10-26).
- Renamed: intent:psyche-interaction to intent:living-interaction.
- Removed: compensation:psyche-interraction; inquiry modules; vision:inquiry.
- Split: none in the three repositories. The splits the living asked for (main-flow, horizons vision:short:/medium:/long:/far:) are unlanded: no `vision:short:*` file exists [W].

Rows. "Delta" is the change from the 10-27 snapshot to the live read. "Lacks" is registry-new modules the row does not carry. "Unused" is inferred from the row's role, and each item is a question, not a ruling.

| Metaflow | Delta since 10-27 | Lacks (new in registry) | Carries, probably no use for [I] |
|---|---|---|---|
| Field core Primary | +living-interaction, ghost, flow, beads; -inquiry, psyche-interaction, vision:book | energy, fable, account, proposal | none obvious |
| Field core Secondary | same | same | none obvious |
| Field core Tertiary | +living-interaction, ghost; -inquiry, psyche-interaction (untouched by today's audit) | energy, fable, account, proposal | vision:book (no crystallization module; unclear if it makes books) |
| Field flow Secondary | like Field core Primary | same | none obvious |
| Field publisher Quaternary | +living-interaction, ghost (untouched today) | energy, fable, account, proposal | none obvious (it publishes books, so vision:book is used) |
| Mind core Primary | +living-interaction, ghost, flow, beads; -book-crystallization, vision:book, inquiry, psyche-interraction | energy, fable, account, proposal | none obvious |
| Mind core Secondary | same | same | none obvious |
| Mind core Tertiary | +living-interaction, ghost (untouched today) | same | vision:book, compensation:book-crystallization |
| Mind flow Primary / Secondary | like Mind core, plus vision:flow, vision:subflows | same | none obvious |
| Mind obsidian Primary / Secondary | new row (10-29 16:36); carry five knowledge:obsidian-* | energy, fable, account | none obvious |
| Psyche book Tertiary | +living-interaction, ghost, flow, beads (kept book modules) | energy, fable, account, proposal | compensation:behavior and correction, vision:ethos, vision:datom, knowledge:protos, knowledge:datom, knowledge:orchestrate (it publishes) |
| Psyche core Primary | rebuilt: now 10 system, 12 user; -book-crystallization, vision:book, vision:ethos, vision:datom; +belief-modules, energy, crystallization, proposal, psyche, collaboration, aspects, messaging, flow, beads | fable (Fable model), account | none obvious |
| Psyche core Secondary | +energy, proposal, flow, beads; -book modules | fable, account | vision:criomos, vision:ethos, vision:datom, knowledge:protos, knowledge:datom (it commits records, not code) |
| Psyche core Tertiary / Quaternary | +flow, beads; -book modules | energy, fable, account, proposal | vision:ethos, vision:datom, protos, datom, orchestrate, compensation:behavior and correction |
| Psyche flow Primary / Secondary | +vision:nexus, vision:signal, vision:remembering, flow, beads; -vision:subflows, book modules | energy, fable, account, proposal | none obvious (it designs Flow) |
| Psyche records Secondary | +flow, beads; -book modules | energy, fable, account, proposal | vision:criomos, vision:ethos, vision:datom, protos, datom |
| Psyche obsidian Primary / Secondary | new (10-29 16:19) | fable, account | none obvious |
| Psyche research Primary / Secondary | new row; -vision:book, compensation:book-making today | energy, account, proposal (the Primary carries intent:fable; the Secondary lacks it) | vision:psyche-aspect (proposal 10 folds it away); compensation:messaging |
| Psyche test Quaternary | +spirit:ghost only | n/a | none (minimal row) |

Notes:
- [W] The metaflows.clj runtime-rows in the local CriomOS-home checkout (437455a4, stale) still name `:intent-psyche-interaction` and `:intent-context-modules`; the live Psyche core Primary row no longer does. That checkout cannot tell whether the source on origin matches the live rows.
- [W] Declarations name no horizon module; intent/psyche.md (c386f58) says a declaration names the horizons it loads. This follows from the fact that no `vision:short:*` file exists; every row is complete with respect to the registry.
- [I] intent:energy is carried by Psyche core Primary/Secondary and Psyche obsidian only; its text says what reaches a dearer reader must carry what that reader would spend itself to get, which concerns every flow that writes to a dearer one (flow-composition proposal 8 lists intent:energy for every Psyche layer).

## 4. What Mind core changed in the Configuration today, and what each row lacks

[W] from /home/li/primary/flows/b2b118/reports/configuration-today.md, a Mind core Secondary report that witnesses only changes from 15:59 on.

Changes:
- 16:00 Psyche core Primary rebuilt (system 14 to 10, user 0 to 10, 12 after 16:30; drops vision:ethos, vision:datom, vision:book, book-crystallization; adds crystallization, proposal, psyche, belief-modules, collaboration, flow, beads, psyche knowledge).
- 16:03 audit of 16 rows: book and presentation modules removed from non-publishing rows; knowledge:flow and knowledge:beads added; Psyche flow rows swapped vision:subflows for vision:nexus and vision:signal and gained vision:remembering; Psyche research rows lost vision:book and compensation:book-making.
- 16:19 new rows Psyche obsidian Primary/Secondary. 16:36 new rows Mind obsidian Primary/Secondary with Codex leave-outs. 16:25 Fable refresh threshold 200000 to 280000. 16:30 vision:aspects and vision:messaging added to Psyche core Primary user modules.
- The report itself says it cannot see changes before 15:59, and that source commits do not prove a live mutation.

What each row still lacks (inferred from the living's words and the table above):
- Every row: no horizon modules (none exist); the modules the living said are for a role (intent:primary, secondary, tertiary, quaternary; vision:composition; intent:conduct; the aspect modules of flow-composition proposals 6 to 9) do not exist yet.
- Psyche core Primary: intent:fable (the Fable layer's own module), vision:account.
- Psyche core Secondary: intent:fable, vision:account; no vision:book (it passes books down to a Tertiary, so this may be right [I]).
- Rows not touched by the 16:03 audit (Field core Tertiary, Field publisher Quaternary, Mind core Tertiary, Psyche test Quaternary) still carry the pre-audit book modules and lack knowledge:flow and knowledge:beads (Tertiary and Quaternary of Field and Mind).
- Psyche core Tertiary/Quaternary, Psyche book Tertiary: no intent:energy (a Tertiary reaches a Secondary); I cannot say if the living wants it there.
- Psyche research Primary: has intent:fable but not vision:proposal or intent:energy, which Psyche core Primary has.
- Mind obsidian rows lack intent:energy and vision:account.
- vision:proposal was missing from Psyche core Primary (flows/2933ce/vision/proposal.md:8 finds the cause); it is present after 16:00 [W: configuration-today.md 16:00 After].
