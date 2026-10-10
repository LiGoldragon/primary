# Book audit, 2026-10-09

Seven partial audits merged unchanged. Each finding is marked witnessed or inferred by its auditor; the merge adds no claims.

---
## Part 1

# Book audit, part 1: flows/bad807/books/1-9

What this covers: books 1 to 9, each with its -v2 and .rulings.md, all modified 2026-10-04. Read with grep and sed against psyche-skills/skills (HEAD 4312cc0), mind-skills/skills, flows/*/vision, flows/bad807/{log.md,reports/,vision/}, and git log in /home/li/primary, psyche-skills and Curriculum. Every finding is marked W (witnessed: both sides read) or I (inferred).
Where the URLs come from: log.md records no artifact URL. Each URL below is from reports/books.md (first edition) or reports/book-revision-inventory.md (reshaped edition).

## Findings that apply to every book 1-9
- (5)+(6) W. Not one proposal targets a skill source. The `Vision/*.md` and `Intent/*` targets moved into skills in primary 928aede20 and psyche-skills fef9864 (2026-10-07). Curriculum/skills was removed in Curriculum 73414b6 (2026-10-07). Each target is replaced as follows:
  - `Vision/X.md` becomes `psyche-skills/skills/vision-X.md` (flowNexus becomes vision-flow.md, I; memory becomes a new vision-memory.md, I).
  - `Intent/deterministicWork.md` becomes `psyche-skills/skills/intent-deterministic-work.md` (I).
  - `Curriculum/skills/vision-{nexus,ethos}.md` becomes `psyche-skills/skills/vision-{nexus,ethos}.md`.
  - `Curriculum/skills/datom.md` becomes `mind-skills/skills/knowledge-datom.md`. Line 95 is unchanged (W).
  - `Curriculum/skills/main-flow.md` becomes `mind-skills/skills/operation-main-flow.md`. Line 39 is unchanged (W).
  - `Curriculum/skills/knowledge-nexus.md` becomes `mind-skills/skills/knowledge-nexus.md`. Line 13 is unchanged (W).
  - A proposal to code (ethos-zero, signal-*, nexus, flow, message, chronos, aggregator, Cargo.toml) is out of scope. Remove the section and send it to its owning flow outside the book.
- (4) W. Each book opens with a survey section, "How it is now", "Where it stands" or "Today". Remove the section. The "Now:" text of each proposal carries what is needed.
- (3) W. Each proposal carries "Ground:", "Grounded:", "The living:" or "Your words" with his words quoted. Change `Ground: "<quote>"` to `Ground: flows/<id>/vision/<file>.md, <date>`.
- (7) W, measured by awk over fenced lines: 1-ethos-v2 36, 2-datom-v2 66, 3-nexus-v2 52, 4-signal-v2 48, 5-memory-v2 36, 6-operation-v2 19, 7-entry-point 96, 8-datom-file-v2 45, 9-jev-use 76. The first editions run 19 to 53. The counts for nested `````markdown` fences are approximate. Many of these lines are proposed prose inside a fence, which the skill says renders as text. Move the prose out of the fence and wrap each code line at 52 characters.

## 1. «Ethos»: books/1-ethos.md, 1-ethos-v2.md, 1-ethos.rulings.md
URLs: https://claude.ai/artifact/MUG7U2QATCFoJFB3S4Vqsq (first edition); https://claude.ai/artifact/XjAvCXLxbMty667gnVFFVE (reshaped).
Open rulings: 9 listed. Six are overtaken (below). Still open: 4 (one-field structs), 7 (trait or kind), and possibly 2 and 3, because the distilled text holds both sides.
- (6) W. P2 Roots has already landed. psyche-skills/skills/vision-ethos.md:30 reads "Four roots: Library, Signal, Operation, Memory…". It landed in Curriculum c98fc43, and the paragraph has existed since 2026-10-02. Ruling 1 is overtaken. What remains is the stale tail of line 25:
  - Removed: `queries and responses, since there is communication; Sema's are record / types, the rest to be decided. Signal gives a Nexus its main types and / Sema its database types.`
  - Added: `queries and responses, since there is communication.`
- (6) W. P4, P6, P7 and P9 already stand in vision-ethos. Line 216 reads "Everything is a type; there is no key-value… bears the variant's name". Line 445 reads "Ethos expands vertically". Line 447 reads "Ethos carries a comment on every section". The book's "Now:" quotes Vision/ethos.md only. Each section becomes a removal of the older line it contradicts:
  - P9: remove `The inline struct or enum is a full type whose derived name carries an underscore, non-idiomatic for a Rust type, so it never collides and reads at a glance as inferred from the sugar.` (vision-ethos 189-192). This settles Ruling 3 toward (b).
  - P6: remove `Ethos follows the canonical protos print: a space inside every bracket and brace at both ends when non-empty.` and add `A space stands inside every non-empty bracket and brace.` (vision-ethos 441-443).
- (6) W. Ruling 8 is overtaken. vision-ethos:11-13 "an implementation is mostly the hand-written bodies" landed in primary 295a240fa (2026-10-06), alongside the heading "Kinds are explicit; bodies are hand-written" (line 328). Remove Ruling 8. P13 keeps only its second sentence.
- (6) W. Ruling 9 (chained variants) and P15 are overtaken. `Voice.{ Aspect Layer }` landed in vision-nexus "Three parts and one path" (primary c71633b55). P15's rule itself still has no home in vision-ethos, so keep P15 retargeted to psyche-skills/skills/vision-ethos.md.
- (1) W. P1 contradicts the line that landed. Proposed: "Ethos is the typed spec every Nexus is programmed from". Distilled (vision-ethos:11): "Ethos is central. The anatomy of the system… is read in its ethos". Remove P1. Its content is landed.
- (1) W. P12 proposes "When trait is said, kind is meant". Distilled vision-ethos:58 says "Trait is set aside as acoustically ambiguous." This is Ruling 7 and correctly open. No change.

## 2. «Datom»: books/2-datom.md, 2-datom-v2.md, 2-datom.rulings.md
URLs: https://claude.ai/artifact/5QXhkrZ6bUmHdWuzn3thJP; https://claude.ai/artifact/CGMnvpbxu5WV5jpqjq2HyW.
Open rulings: 2. Ruling 2 is half overtaken (below).
- (1) W. P1 says "a messenger carries what it is given and forces no datom on it". Distilled vision-messaging.md:8-9 says "The message body is a datom that lands in the recipient's prompt as a datom-formatted object." The book does not name this conflict. Add a proposal on psyche-skills/skills/vision-messaging.md:8-9:
  - Removed: `The message body is a datom that lands in the recipient's prompt as a / datom-formatted object.`
  - Added: `A message body is a datom where the receiving program reads datom; a messenger that needs none is given none.`
  - Grounded on flows/8904b1/vision/datom.md:7 (2026-09-28).
- (1) W. P6 and P7 write `FlowId.{ Integer }`, a struct of one position. The form that landed is `FlowId.Integer` (vision-nexus:153, c71633b55), and it is the form of book 1's P10.
  - Removed: `[ FlowId.{ Integer }`
  - Added: `[ FlowId.Integer`
  - In P3's datom, change `Extended.{ { 12232711 } Voice …}` to `Extended.{ 12232711 Voice …}`.
- (6) W. Ruling 2(b) cites `FlowId.String` in Vision/ethos.md. That line now sits in psyche-skills/skills/vision-ethos.md:316 and :325, beside the landed `FlowId.Integer` in vision-nexus:153. Retarget P6 to also remove vision-ethos:316 `FlowId.String` and :325 `pub type FlowId = String;`, adding `FlowId.Integer` and `pub type FlowId = Integer;`.
- (1) W. P3 generates `Simple_Data` and `Extended_Data`. vision-ethos:216 says "A variant's payload … bears the variant's name; no second type is invented to hold it." Label the Rust block as ethos-zero 16.0.0 output that departs from vision-ethos:216, or drop it.

## 3. «The Nexus»: books/3-nexus.md, 3-nexus-v2.md, 3-nexus.rulings.md
URLs: https://claude.ai/artifact/PoCBpppWC8u6ZV5H1BYCmm; https://claude.ai/artifact/EuYQop6yAY18iyaY6uDuWD.
Open rulings: 11 listed. 1, 2, 3, 9 and 10 are overtaken. 4 to 8 and 11 remain.
- (6) W. Rulings 1, 2, 3 and 10 are settled by the landed vision-nexus:148 ("Nexus always names the whole; the part that does is Operation… Memory is what it remembers"; c71633b55) and by vision-ethos:30 (four roots). Remove these four rulings and mark P1 landed (v2 already does).
- (6) W. Ruling 9 (three or four layers) is overtaken by the landed `Layer.[ Primary Secondary Tertiary Quaternary ]` (vision-nexus:156) and by the tertiary ruling in log.md:183. Distilled vision-flow.md:22 still reads "Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices", which contradicts P7. Add a proposal on psyche-skills/skills/vision-flow.md:22:
  - Removed: `A voice is an aspect carrying a rank, \`Psyche.Primary\`: Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices.`
  - Added: `A voice is an aspect at a layer, \`Voice.{ Aspect Layer }\`: Psyche, Mind, Field by Primary, Secondary, Tertiary, Quaternary.`
- (6) W. P2 points to the entry-point book. That design now sits on Astra's branches (log.md:217, nexus and chronos `entry-point`). P8 ("every `main` is `nexus::main!`") assumes an unlanded design. Keep P8's first sentence only.

## 4. «Signal»: books/4-signal.md, 4-signal-v2.md, 4-signal.rulings.md
URLs: https://claude.ai/artifact/6GTtzM8b6bdYBbzNGVacZD; https://claude.ai/artifact/DGdAnXwjHFfMFEAtwnEFHw.
Open rulings: 5 listed. 1 and 2 are overtaken. 3, 4 and 5 remain.
- (6) W. Ruling 1(a) "queries and responses" and Ruling 2(a) "input and output are too low-level" are already distilled at vision-signal.md:19-20. Remove both rulings.
- (6) W. P1's verb rule is already distilled at vision-nexus.md:116: "Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves." That line uses "Operations" for wire queries, against the landed Operation part. Recast P1 as a proposal on vision-nexus:116:
  - Removed: `Operations are verbs, \`Submit\`; replies the past tense, \`Submitted\`; rejections name themselves.`
  - Added: `Queries are verbs, \`Submit\`; responses the past tense, \`Submitted\`; refusals name themselves.`
  - The vision-signal half of P1 then adds only the forms section.
- (3) W. Ruling 1 quotes four of his phrases, rulings 2, 3 and 5 more (14 quote marks in .rulings.md). Cite path and date instead.

## 5. «Memory»: books/5-memory.md, 5-memory-v2.md, 5-memory.rulings.md
URLs: https://claude.ai/artifact/XmniNLyZmteyJC7J4t43Y5; https://claude.ai/artifact/G9Ctu1HeQSFzqmQT9LUmDQ.
Open rulings: 5 listed. 1 and 2 are overtaken. 3, 4 and 5 remain.
- (6) W. Ruling 1 (Sema or Memory) and Ruling 2 (each part its own root) are settled by vision-nexus:148 and vision-ethos:30. Distilled vision-sema.md still says "its root, Sema, declares record types". Ethos book P3 is the edit that mends it, so cite it rather than re-rule.
- (1) W. In P8 the RoleConfiguration nests `Role.[ Voice.{ Aspect.[ … ] Layer.[ … ] } … ]` four deep and redeclares Voice, Aspect and Layer. vision-ethos:216 says "Inline nesting goes about three deep; past that, the type comes from a Library" and "a type used in more than one place is declared once and named". Flow's Library declares them (vision-nexus:154-156).
  - Removed: `[ signal_flow:[ ModelName ]` and `RoleConfiguration.{ Role.[ Voice.{ Aspect.[ Psyche Mind Field ] / Layer.[ Primary Secondary Tertiary Quaternary ] } / LivingInteraction Implementation VisionAudit ]`
  - Added: `[ signal_flow:[ ModelName ]` / `  flow:[ Voice ]` and `RoleConfiguration.{ Role.[ Voice LivingInteraction / Implementation VisionAudit ]`

## 6. «Operation»: books/6-operation.md, 6-operation-v2.md, 6-operation.rulings.md
URLs: https://claude.ai/artifact/PPtohyLV2pLud82PAuDEoE; https://claude.ai/artifact/AaPtaTKrJMRhBDHDa95v2V.
Open rulings: 7 listed. 1, 2, 3 and 5 are overtaken. 4, 6 and 7 remain.
- (6) W. P1 restates the landed vision-nexus:148 ("Operation is what it does… Every effect has a matching operation type. A signal reaches memory only through operation"). Remove P1. Ruling 1 goes as in book 3. Ruling 3 is settled by vision-ethos:30. Ruling 2(a) "conversion" contradicts the distilled vision-nexus:29-30 "Conversion is the wrong frame for it". Ruling 5 is settled as in book 1.
- (1) W. P5 and P9 write `Failed.String` (v2 lines 151, 193, 212 and the SVG at 126). vision-nexus:68 says "errors are vocabulary, never strings", and the landed example at vision-nexus:178 has `Failed.[ CapsuleRefused StoreRefused ]`.
  - Removed: `  Failed.String ]`
  - Added: `  Failed.[ CapsuleRefused StoreRefused ] ]`
- (5) W. P7 targets `Intent/deterministicWork.md`. Retarget it to psyche-skills/skills/intent-deterministic-work.md (I: name), with the frontmatter `description:` the intent- files carry.

## 7. «The standard entry point: three actors, one path»: books/7-entry-point.md, 7-entry-point.rulings.md
URL: https://claude.ai/artifact/UnMFEjS3nBE5gDVvoXsWL9. The source has no -v2. The reshape was made in place.
Open rulings: 3 listed. Ruling 3's option (c) is voided by his own words.
- (1, raw) W/I. flows/bad807/vision/nexus.md:15 reads "a main actor, which could have multiple sub-actors (like the signal actor), would only be able to talk to the operation actor". The book's P1 makes signal a peer actor: "Every Nexus runs four actors: a main actor, a signal actor…". The quote is W. Whether it means signal is a sub-actor of main is I. Raise it as a ruling instead of building on it.
- (6) W. Ruling 3 (c) "A running Nexus on a branch, Flow or Orchestrate" is voided by "A toy, I mean, or a simple nexus which isn't in production" (same record) and by log.md:105-109. Remove (c). P3 and P4 are overtaken by Astra's branch-only landing (log.md:217). Replace both with one line naming the branches.
- (1) W. The title says "three actors" and P1 says "four actors". Change the title to `The standard entry point: four actors, one path`.
- (4) W. "Today's entry points", "The test subject" and "The test on a branch (the flow's plan)" are survey and plan. Remove them.
- (3) W. "## The rule" quotes his whole comment, and the rulings file adds 10 quote marks.

## 8. «A Nexus reads a value from a datom file»: books/8-datom-file.md, 8-datom-file-v2.md, 8-datom-file.rulings.md
URL: https://claude.ai/artifact/P7e8miuzGpRN1URGYxiDLc (reshaped). reports/books.md lists no first edition.
Open rulings: 3, all open.
- (3) W. v2 opens with "## His words", his comment quoted whole. Remove it. Cite `flows/bad807/vision/nexus.md, 2026-10-04`.
- (1) W. Ruling 2(a) admits a path string in a Nexus, citing vision-nexus "Signal only" ("the string fields it still carries are records on the way"). It omits vision-nexus:66 "no text arrives on its wire and none leaves it", and `ReadFile` carries a path out on the wire. Add that line to Ruling 2(b)'s side.
- (7) W. P1 to P3 put proposed prose in ```text fences, with lines up to 435 characters (v2:12, 68, 198). Render them as text.

## 9. «Jev in the flow-handling system: where a typed decision helps now»: books/9-jev-use.md, 9-jev-use.rulings.md
URL: https://claude.ai/artifact/98MeaVj7EHvRTAfpTvkARN.
Open rulings: 3, all overtaken by the merge.
- (6) W. The book was merged into the «Jev» standing edition (books/18-jev.md; inventory "Merges"; published per log.md:259). Astra's finding that fuzzy-jev 0.6.0 speaks alpha/decisions directly (log.md:273) overtakes P3's "which one is held by d66c26's reuse investigation". Retire the book.
- (5)+(4) W. All four proposals target code (flow, signal-flow, meta-signal-flow, message). None targets a skill source, and the book opens "Every line below is the flow's proposal; none is his word". It is a design, not a distillation. Remove it from the books shown to the living.

Nothing to flag: reports/comments-2026-10-04.md. It is a fetch report, not a book, and holds no proposals. Its two comments concern the context-modules books and are consistent with the memory edition's "A role is … not a module type".

---
## Part 2

# Part 2: book audit against the psyche record

Scope: flows/bad807/books/1[0-8]*.md (mtime under 7 days, with 12 and 14 .rulings.md) and flows/aa887c/books/context-modules-v3.md, with aa887c/reports/his-comments*.md. Artifact URLs come from flows/bad807/reports/books.md and flows/aa887c/reports/books.md. Neither log.md records a URL; both name books by title only. Over-52 counts come from an awk pass over fenced lines. Most of those fences hold tables or prose, not code. They also break the web-render line in mind-skills 41671fb and field-skills 4d8ed32 (2026-10-07). No flow record shows a ruling number given on any of these books. bad807/log.md:267 says it is "waiting on his numbers". "W" means I read both sides; "I" means inferred.

## 10. «The three inside the four…», flows/bad807/books/10-nesting.md
URL: https://claude.ai/artifact/EVoaJFrtMCCAmpn85A7XaE. Open rulings: 3, unanswered by number.
- (3) W. Lines 4-6 quote his order back to him.
  Removed: `> see how the first three rows are also in the fourth …` and its `-- psyche` line.
  Added: `Distils flows/bad807/vision/metaflow.md, 2026-10-04.`
- (4) W. Sections 1-6 are a research survey. No section names a skill file, removed lines or added lines.
  Removed: sections 1-6.
  Added: nothing in this book. The research stays in flows/bad807/reports/metaflow-dimensions-2.md.
- (6) W. Ruling 1 ("Do the Metaflows nest this way…") is answered in bad807/vision/metaflow.md:17 (2026-10-04): "The 3-inside-4 is interesting but not quite my point."
  Removed: ruling 1.
- (5) W. No proposal targets psyche-, mind- or field-skills/skills.
- (7) None: no code blocks.

## 11. «Our open-source stack and Jev…», flows/bad807/books/11-jev-ecosystem.md
URL: https://claude.ai/artifact/RjkX3DVu9AGU15vQxXEWkk. Open rulings: 3.
- (3) W. Lines 4-6 quote his order ("We should get a book going…").
  Removed: the quote and its `-- psyche, 2026-10-04.` line.
- (4) W. The whole book is a survey: sections 1-6 are tables of clients, plugins, gateways and trends, with no file-line proposal. Ruling 3 asks whether it "becomes a standing report". A report does not belong in a book.
  Removed: the book.
  Added: flows/bad807/reports/jev-ecosystem.md, which already holds it, stays the place for it.
- (6) W. Ruling 1 (a) recommends typesafe-system-one first. bad807/log.md:273 records Astra's finding: "fuzzy-jev 0.6.0 … speaks alpha/decisions directly … evaluation first, the other gateway retained."
  Removed: `(a) typesafe-system-one over OpenRouter v1/systemone. The flow's recommendation…`
  Added: nothing. The evaluation is past the choice.
- (5) W. No skill-source target.
- (7) W. 14 lines over 52 (max 83), in json and plain fences.

## 12. «Metaflows that expand and contract…», 12-metaflow-roles.md and .rulings.md
URL: https://claude.ai/artifact/JmBjyo3b4NcFMxh41jpTYX. Open rulings: 6. bad807/log.md:259 says book 16 replaces them.
- (3) W. Lines 4-10 quote bad807/vision/metaflow.md.
  Removed: the three `>` blocks.
  Added: `Distils flows/bad807/vision/metaflow.md, 2026-10-04.`
- (6) W. The floor ("keeping Candra / making Budha / clearing Śani", no Sun) is overtaken by bad807/vision/metaflow.md:23, "The sun is in the basic triad: there is nothing without the sun". Ruling 2 (a), Sūrya opening by demand, is overtaken by metaflow.md:31, "The Sun is the primary layer, woken for judgment". Ruling 5 (a), "aspect and layer … stand beside the lattice", is overtaken by ebbe30/vision/aspects.md (2026-10-09), "The aspect is now, I think, part of any metaflow". It is also overtaken by 41fa34/vision/layers.md (2026-10-08): "This primary-to-quaternary division is sort of universal in any type of metaflow or flow."
  Removed: rulings 1, 2 and 5 in both files.
  Added: nothing. Book 16 replaces this book.
- (5) W. §6 targets signal-flow/ethos/signal.ethos and flow-nexus operation.ethos. These are code, outside the skill sources.
- (1) None found. The distilled record (psyche-skills/skills) has no Metaflow line; grep found none.
- (7) W. 84 lines over 52 (max 250). Tables sit in plain fences.

## 13. «The sun in the triad», flows/bad807/books/13-sun-triad.md
URL: https://claude.ai/artifact/SP8s9iMexMBj9Qbabi4qLc. Open rulings: 3. Book 16 replaces them (bad807/reports/book-revision-inventory.md, entry 28).
- (3) W. Line 4 quotes "How can we keep the sun out of the basic triad?…" back to him.
  Removed: the quote. Added: `Distils flows/bad807/vision/metaflow.md, 2026-10-04.`
- (5) W. Both proposals target `/home/li/primary/flows/bad807/books/12-metaflow-roles.md`. That is a book, not a skill source.
  Removed: `File /home/li/primary/flows/bad807/books/12-metaflow-roles.md, section 1`
  Added: `File /git/github.com/LiGoldragon/psyche-skills/skills/vision-flow.md, new section "Metaflow"`
- (1r) W, raw vision rather than distilled. Figure 1 has "Solid: the base, always open" with Sūrya in the base. bad807/vision/metaflow.md:31 (typed, 2026-10-04) says the Sun is "woken for judgment".
  Removed: `Solid: the base, always open.`
- (4) W. Section 1 (Yāska, Rigveda, Sūrya Siddhānta) is a survey.
- (7) W. 56 lines over 52 (max 176).

## 14. «The geography of the Metaflows», 14-geography.md and .rulings.md
URL: https://claude.ai/artifact/3sk7cuiZphy57EJNYtrKDY. Open rulings: 3. Book 16 rulings 3 and 6 repeat them.
- (2) W. Line 17, `**His**: "The other three are always already awake."`, and rulings Summary 1 ("his: …"). Both treat bad807/notion/metaflowDimensions.md:41 as his ruled word, but a notion record is a brainstorm, never ruled.
  Removed: `**His**: "The other three are always already awake."`
  Added: `Notion, not ruled: flows/bad807/notion/metaflowDimensions.md, 2026-10-04.`
- (3) W. Ten `**His**:` lines (17, 40, 52, 55, 64, 80, 126…) restate his words.
  Removed: each `**His**: …` quote. Added: a path+date citation.
- (6) W. Ruling 1 (a), "stands beside the 3×4 table", is overtaken by 41fa34/vision/layers.md (2026-10-08) and ebbe30/vision/aspects.md (2026-10-09), as under book 12.
- (4) W. Sections 2-9 describe "what each holds, as it runs today", today's four clusters and one sentence's path. All of it is status or reading, with no file-line proposal. (5) W: no skill-source target at all.
- (7) W. 49 lines over 52 (max 129).

## 15. «Context modules» (standing edition), flows/bad807/books/15-context-modules.md
URL: https://claude.ai/artifact/JGdUchiTpNgwLYfaqwaBWc. Open rulings: 7. Four comments answered in his-comments-2.md 1-4. Replaced on 2026-10-05 by aa887c's v3 (aa887c/log.md:74-75).
- (6) W. The whole edition is overtaken by context-modules-v3. Every finding under v3 below applies here too.
- (3) W. "## Your words" (lines 7-10) is three quotes of his.
  Removed: the section. Added: `Distils flows/edf227/vision/contextModules.md, 2026-10-03; flows/bad807/vision/contextModules.md, 2026-10-04.`
- (5) W. Targets `Vision/contextModules.md`, `curriculum-deploy.ethos`, `tools/claude-main-flow-launch.mjs`, `Curriculum roles.datom` and `Curriculum skills/*`. Curriculum 73414b6 (2026-10-07) "Replace Curriculum skills with typed Nexus" removed the last of these.
- (7) W. 49 lines over 52 (max 410).

## 16. «Metaflows» (standing edition), flows/bad807/books/16-metaflows.md
URL: https://claude.ai/artifact/52nh2mXjUSnQizezFn6yxP. Open rulings: 7.
- (2) W. §1, "Woken 'it's not always on. The other three are always already awake.'" under **His**, and §2 "His notion". Ruling 1 recommends (a) because "it is your latest word". The source is bad807/notion/metaflowDimensions.md:29-41, a notion, against the vision record metaflow.md:23 "The sun is in the basic triad".
  Removed: `Recommendation: a; it is your latest word, and the Sun stays primary`
  Added: `Recommendation: none. (a) rests on a notion (notion/metaflowDimensions.md); the vision record (vision/metaflow.md, 2026-10-04) puts the Sun in the triad.`
- (6) W. Ruling 6 (a), "stands beside the 3×4 table", is overtaken by 41fa34/vision/layers.md (2026-10-08) and ebbe30/vision/aspects.md (2026-10-09). The definition "Voice: a Metaflow with no known ending" is refined by f5a6e9/vision/flow.md (2026-10-07): "A voice is a permanent Metaflow. It's a Metaflow that might go to sleep but can always be woken".
  Removed: ruling 6. Added: nothing until the later records are distilled.
- (3) W. The §1, §2, §6 and §8 `**His**:` blocks quote him.
  Removed: each block. Added: `Distils flows/bad807/vision/metaflow.md, 2026-10-04.`
- (5) W. §7 targets signal-flow and flow-nexus ethos. No proposal targets a skill source.
  Added proposal target: `psyche-skills/skills/vision-flow.md, new section "Metaflow"`, carrying metaflow.md:3 and 31 and f5a6e9 flow.md:3 as statements. Inferred (I): the definition belongs there; vision-flow has no Metaflow section today (grep).
- (4) W. §5 "Not measured yet" and §6 "Today's four, as examples" are status.
- (7) W. 84 lines over 52 (max 250).

## 17. «Three skill repositories and the main workspace», flows/bad807/books/17-workspace.md
URL: https://claude.ai/artifact/JKSJRFpH8FKSuizbobXiDd. Open rulings: 10, unanswered by number. bad807/log.md:269 records the flow's own rulings on build blockers, not his.
- (3) W. Lines 4-10 hold two relayed STT quotes.
  Removed: both. Added: `Distils flows/bad807/vision/workspace.md, 2026-10-04.`
- (6) W. Proposal 2, "one directory per type … psyche-skills/ spirit/ intent/ vision/ notion/", is overtaken by psyche-skills fef9864, mind-skills 9940abd and field-skills acf7a0c (2026-10-07): flat `skills/<prefix>-<name>.md`. Rulings 3 and 7 are settled by that landing (prefix names, kebab stems). Proposal 3 (curriculum-deploy ModuleType/Allowed) is overtaken by Curriculum b778545, "six skill kinds as prefixes".
  Removed: Proposals 2 and 3, and rulings 3 and 7.
- (5) W. Targets `Vision/skills.md`, `Vision/workspace.md`, `curriculum-deploy.ethos`, the new repository `main-workspace`, `Curriculum skills/psyche.md` and `Curriculum skills/skill-designing.md`. The last two now live in mind-skills.
  Removed: `### Line 1: Curriculum skills/psyche.md, lines 24–26` / `### Line 2: Curriculum skills/skill-designing.md, lines 66–67`
  Added: `### Line 1: mind-skills/skills/knowledge-psyche.md, lines 24–26` / `### Line 2: mind-skills/skills/operation-skill-designing.md, "A role skill carries…"`
  Removed: `[vision] Vision/workspace.md` / Added: `[vision] psyche-skills/skills/vision-psyche.md, new section "The main workspace"`
- (1) W. Proposal 6, "a new repository, main-workspace … Primary stays as an archive, read by no flow", against psyche-skills/skills/vision-psyche.md:17-19: "Primary Next begins from Primary's root commit and carries selected repository mounting points plus a README and AGENTS.md".
  Removed: `[implementation] a new repository, main-workspace.`
  Added: `[implementation] Primary Next, from Primary's root commit, renamed main-workspace if ruled.`
- (4) W. "How it is now", "What stands now" and the table of "ten design rulings the flow made" are status.
- (7) W. 69 lines over 52 (max 136).

## 18. «Jev» (standing edition), flows/bad807/books/18-jev.md
URL: https://claude.ai/artifact/PcJYyh1TqqorSvv7j2UpCU. Open rulings: 7.
- (3) W. Line 4 quotes him. §1 lists "His three records" with quotes. §5 quotes him again ("this is where we're going to start using JEV") and the compensation-messenger-clj line.
  Removed: these quotes. Added: `Distils flows/aa887c/vision/jev.md; flows/752e0f/vision/models.md, 2026-09-24.`
- (6) W. "He never chose its first caller" and ruling 1 are overtaken by aa887c/vision/jev.md (STT, 2026-10-08). It names uses: "committing and judging if certain items can enter a database … commit messages, check that the system is running, and check that there are no conflicting main flows". Ruling 6 and tension 1 (JSON state) are overtaken by d4ae97/vision/ethos.md:140 (2026-10-08), "marry Jev System 1 … to probably a subset of the Ethos specification", and by d4ae97/vision/tools.md:44 (a JSON-to-Ethos bridge). §2 "Gateways" and agreed point 2 are overtaken by bad807/log.md:273 (fuzzy-jev 0.6.0, evaluation first).
  Removed: `He never chose its first caller.`, ruling 1 (a)-(d) and ruling 6.
  Added: nothing until those 10-08 records are distilled.
- (4)+(5) W. §§1-6 are status and survey. Every proposal targets code (flow/Cargo.toml, flow-nexus src, signal-flow, meta-signal-flow, message-nexus), and none targets a skill source.
- (7) W. 53 lines over 52 (max 113).

## «Context modules» v3, flows/aa887c/books/context-modules-v3.md
URL: https://claude.ai/artifact/FeJQWVLUVPks31MiJKXq2y (aa887c/reports/books.md). Open rulings: 7. No comment on v3 is recorded.
- (3) W. "## Your comments on the last edition" (lines 7-21) quotes his-comments-2.md 1-4 back to him.
  Removed: the section. Added: `Answers comments on «Context modules», flows/aa887c/vision/contextModules.md.`
- (1) W. Proposal 1 says "A role is one record naming … its model", and Proposal 8 has `{ claude-fable-5-1 None }` in Curriculum/roles.datom. Distilled line, psyche-skills/skills/vision-model-roles.md: "The model is declared once, as typed configuration in Flow … Nothing else holds a model name".
  Removed: `A role is one record naming, for each placement, its modules by type, and its model.`
  Added: `A role is one record naming, for each placement, its modules by type; its model is Flow's declaration.`
- (1) W. Proposal 11 says "An order … is not distilled into a rule; it stays in the log". Distilled line, vision-distillation.md: "the impurity is dissected out of the log and destroyed".
  Removed: `…is not distilled into a rule; it stays in the log.`
  Added: `An order, an instruction for a situation, or an intervention is a vision impurity; distillation dissects it out.`
- (1) I. Proposal 8 puts the user-only `main-flow` in SystemPrompt. intent-startup-prompt.md says "A startup skill enters through the startup prompt". The source record, 752e0f/vision/archive-firstPrompt.md, has "one block of text, one user prompt only".
- (1r) W, raw. Proposals 3 and 4 put the manifest in curriculum-deploy's ethos. edf227/vision/contextModules.md (2026-10-03) says "Every flow call, or the flow database, has a registry of where each context module is located", maintained "over the meta socket".
- (6) W. Proposal 4 (`<repository>/<type>/<name>.md`, "no type: line") is overtaken by the flat `skills/<prefix>-<name>.md` (psyche-skills fef9864, 2026-10-07). Ruling 1 (six vs eight types) and Proposal 10 are overtaken by mind-skills/skills/operation-skill-designing.md:55, which lists seven prefixes (`spirit-` … `compensation-`, no notion), through Curriculum b778545 and mind-skills 991e1a4. Proposal 1, "no other text lists them", now contradicts that landed line. 0c85a3/vision/spirit.md (2026-10-07) has "That's what we're calling spirit: the system prompt."
  Removed: Proposal 4, Proposal 10 and ruling 1.
- (5) W. Targets `/home/li/primary/Vision/contextModules.md`, `curriculum-deploy.ethos`, `Curriculum/roles.datom`, `Curriculum/skills/*.md` and the three launchers.
  Removed: `**vision** · create /home/li/primary/Vision/contextModules.md`
  Added: `**vision** · create psyche-skills/skills/vision-context-modules.md`
  Removed: `Curriculum/skills/psyche-distillation.md, after line 25`
  Added: `mind-skills/skills/operation-psyche-distillation.md, after line 25`
- (4) W. "Where things are now", Figures 1-2 and the launcher excerpts are status.
- (7) W. 72 lines over 52 (max 196): 19 js, 2 rust, 51 plain.

Skipped (nothing to flag): none. Every book above has at least one finding.

---
## Part 3

# Part 3: books of flow 5ed94b, 01 to 13, against the psyche record

Audited by this flow. Paths: books under `flows/5ed94b/books/`; skills under
`psyche-skills/skills/` (P), `mind-skills/skills/` (M), `field-skills/skills/` (F).
"Witnessed" means I read both sides. The books' lane publish is e003815e1 (2026-10-03 15:07
-0600). A cited line committed before it is marked (1); one committed after it is marked (6).

## Applies to every book (stated once here, not repeated below)

- Comment reports: `flows/5ed94b/reports/*comments*.md` matches no file. The only
  living's comments in this lane are `vision/visionBooks.md` and `vision/contextModules.md`.
- Artifact URL: the 5ed94b log, handover and reports record none for any book (grep for
  `claude.ai` returned nothing). Unavailable.
- Open rulings: every proposal is still open. Handover line 18 lists "The numbers on every
  proposal book" as open; the log records "none of the first fifteen books carries a comment".
- (7) No book file has a code block (fence count 0 in all 37 files), so no line is over 52.
- (6)+(4)+(3), witnessed: each narrative book `NN-*.md` (02 to 13) is a "What he wants"
  survey made of 31 to 52 block-quoted lines of his words. The log ("redo them all as
  context-module edit proposals", 2026-10-03) and his comment in `vision/contextModules.md`
  ("finding no proposal in it", on «Talking to the living») superseded them with `*.proposals.md`.
  Removed: the whole file. Added: nothing.
- (4)+(5), witnessed: no proposal names a file path. Each names "Kind, module X" and, apart
  from 06#3, 07#5, 08#2, 08#3, 09#9 and 09#10, gives no removed lines. His comment of
  2026-10-03 (`vision/visionBooks.md`) asks for "what module, what edit, what remove, what
  replaces what". The fix is the same for each proposal. Removed: `Vision, module vision-flow. Edit.`
  Added: `psyche-skills/skills/vision-flow.md, after line N` followed by the current lines quoted
  red and the new lines green. Module names that map to no file of that kind: Vision main-flow
  (M operation-main-flow.md), Vision skill-designing (M operation-skill-designing.md),
  Knowledge orchestrate (M operation-orchestrate.md), subflow (F compensation-subflow.md),
  behavior (F compensation-behavior.md), correction (F compensation-correction.md),
  Operation claude-harness (M knowledge-claude-harness.md). New modules with no home named:
  knowledge-layers, context-modules, vision-identifiers, knowledge-speech-to-text,
  knowledge-living-contact, psyche-routing, seat-models, quota-books, quota-reading.
- (3), witnessed: "Rests on" lines quote his words and give a date but never a path. Counts of
  quoted lines: 01:14, 02:3, 03:7, 04:8, 05:8, 06:3, 07:6, 08:7, 09:5, 10:8.
  Later-question files 03, 04, 07, 08 and 09 block-quote his words in full. Removed:
  `Rests on: 3 Oct, "I do not want work trees"; 17 Sep.` Added:
  `Rests on: flows/<id>/vision/<topic>.md, 2026-10-03; …, 2026-09-17.`
- (4), witnessed: the `*.later-questions.md` files are question lists with no target file
  (for example 02 Q7: "What does an archive keep…"). Removed: each question. Added: either
  a proposal naming the file and its lines, or nothing.

## 01 Where flows do a program's work by hand — 01-gaps.proposals.md
Open rulings: 15. Rulings on file: none.
- (4) Witnessed: every item carries a `Program:` status line, for example "Program: does not exist.
  Locks have no lease…". Removed: every `Program:` line. Added: nothing.
- (6) #15 had already landed before the book, witnessed. F compensation-behavior.md:22 reads
  "Deterministic code retains and compares raw checksums." It first appeared in Curriculum
  cb1294c, 2026-10-03 11:34 -0600. Removed: proposal 15. Added: nothing.
- (6) #9 was overtaken, witnessed. F compensation-messenger-clj.md:35 reads "`hm-retire FLOW`
  takes only the flow id" (Curriculum 0f80be1, 2026-10-03 18:01 -0600). Removed: "Program:
  partly. The pieces exist but ask for arguments no flow can supply." Added:
  "trial-reaping: Retire an abandoned flow with `hm-retire FLOW`."
- (6) #13 was overtaken by P vision-messaging.md:33, witnessed (Curriculum 98c0ec6, 2026-10-04).
  That line reads "Send only messages that require the recipient's action, deliver a result it awaits, or
  report an error or blocker". The book says "Send a message only to hand over words, never to
  report state." Removed: the book's line. Added: "State changes are read from Flow."
- (6) #2 contradicts the current F compensation-primary-commit.md:5-11, witnessed. That text has
  each flow commit, under the PrimaryPublish lock, in its own independent clone (Curriculum
  3ba1443, 2026-10-03 13:51 -0600). Removed: "It does not lock, commit, copy, push or release
  by hand." Added: nothing until the publisher program is ruled; the item becomes a question.

## 02 Flow — 02-flow.md, 02-flow.proposals.md, 02-flow.later-questions.md
Open rulings: 12 proposals and 4 later questions.
- (1) #8 Text 2 contradicts distilled vision, witnessed. P vision-flow.md:42-44 (Primary 776fe5b48,
  2026-09-18) reads "Reaping belongs to the refresh event, not to a later sweep." The book
  offers "The judge decides, and the Field reaps every time." Removed: Text 2. Added: nothing.
  Text 1 stands alone as an F trial-reaping.md line.
- (1) #4 Text 1 contradicts P vision-flow.md:52-53, witnessed. That line reads "A subflow is instead an independent flow with
  its own system prompt". The book offers "A subflow carries its parent's identity … and opens no lane of its own."
  Removed: Text 1. Added: nothing. Later question 6 falls with it.
- (6) #6 is already distilled, witnessed. P vision-flow.md:46 (Primary 102383f86, 2026-10-02) reads
  "Every harness event reaches Flow through the harness's hooks … Polling is forbidden".
  Removed: proposal 6. Added: nothing.
- (6) #5 is already distilled, witnessed. P vision-flow.md:22 reads "Voices are addressed by name; a flow id is
  for the ledger". Removed: "Flows are addressed by voice, aspect first." Added: nothing.
- (4) Witnessed: in the later questions, Q5 ("before or after the minimum working Flow") and Q7
  ("What does an archive keep") name no file. Removed: both. Added: nothing.

## 03 Landing work — 03-landing-work.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 5 later questions.
- (6) #7 Text 1 is already distilled, witnessed. P vision-committing.md:8-9 (Primary 053ec4a5b, 2026-09-20)
  reads "The commit call is explicit with file paths. A flow commits the files it edited".
  Removed: proposal 7 Text 1. Added: nothing.
- (1) #7 Text 2 drifts from the same lines, witnessed. The book's "Changes in the tree that belong to nobody are
  committed first" adds commits of files the flow did not edit, against "commits the files it
  edited". Removed: Text 2 from M operation-file-editing. Added: nothing in vision. The
  dirty-tree rule now sits in Primary's CLAUDE.md ("Committing"); that placement is the
  living's to rule on.
- (6) #1, #8 and #10 were overtaken, witnessed. F compensation-primary-commit.md:5,11 has each flow
  publish its own paths "from an independent Git clone" under the PrimaryPublish lock (Curriculum
  3ba1443, 2026-10-03 13:51 -0600). #1 says "no per-flow clones", #8 says "A Field flow holds the
  publish lock for good", and #10 Text 2 says "The publisher makes all commits". Removed: those
  three lines. Added: "Publishing is compensation-primary-commit's; this line names no
  publisher."
- (3) Witnessed: the later questions block-quote him four times, for example "I do not want fucking work trees."
  Removed: the quotes. Added: `flows/<id>/vision/<topic>.md, 2026-10-03` (the path is not
  in the book; inferred that the record exists in the raw corpus).

## 04 Skills and Curriculum — 04-skills-and-curriculum.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 4 later questions.
- (6) #1 Text 1 and #3 were overtaken by the landing, witnessed. Skill sources now sit in psyche-skills,
  mind-skills and field-skills, with psyche vision/intent/spirit, mind knowledge/operation, and field
  compensation/trial (fef9864, 9940abd and acf7a0c, 2026-10-07). Removed: proposals 1 and 3. Added: nothing.
- (6) #10 was overtaken, witnessed. M operation-skill-designing.md:55-57 (Primary 928aede20, 2026-10-07)
  reads "A `vision-` or `intent-` skill is gold: the living's approved words". That contradicts
  both Text 1 ("Golden skills are a kind of their own") and Text 2 ("There are no golden skills").
  Removed: proposal 10 and later question 3. Added: nothing.
- (6) #11 Text 1 has landed, witnessed: the file is P spirit.md. Removed: Text 1. Text 2 ("not a skill")
  stays open.
- (6) #6 was overtaken, witnessed. M knowledge-layer-models.md exists, and line 18 reads "Quaternary | Claude |
  Haiku 5.5 … | Low | Living ruling, 2026-10-08" (mind-skills 37ca3f7). The book's Text 1 has
  "Quaternary is Sonnet low effort". Removed: "Knowledge, new module knowledge-layers. Create."
  and Text 1. Added: "mind-skills/skills/knowledge-layer-models.md: (Text 2 only, if still wanted)".
- (5) #2 targets the wrong kind, witnessed. It says "Vision, module skill-designing", but the file is M
  operation-skill-designing.md, an operation skill. Removed: "Vision, module skill-designing."
  Added: "mind-skills/skills/operation-skill-designing.md".

## 05 Roles and subflows — 05-roles-and-subflows.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 4 later questions.
- (1) #11 Text 1 contradicts P vision-flow.md:24 (Primary 04f941cd4, 2026-10-02), witnessed. That line
  reads "Design is Astra's, not Sol's." The book's Text 1 has "One primary-layer voice designs the Claude-side definitions and
  the other designs the Codex-side ones". Removed: Text 1 and later question 6. Added: nothing.
- (1) #9 drifts from P vision-model-roles.md:65-66 (Primary a74253599, 2026-09-19). That line reads
  "Opus launches Sonnet and Haiku, and sometimes Opus, but rarely." The book's #9 has "whose
  main flow coordinates secondary subflows", which I read as Opus subflows. This is inferred,
  because the book does not name the model. Removed: "coordinates secondary subflows".
  Added: "coordinates subflows of the layers below it".
- (1) #7 Text 1 drifts from P vision-flow.md:50 (Primary 053ec4a5b, 2026-09-20), witnessed. That line reads "The harness
  subagent facility is replaced." The book's Text 1 has "built now as harness definitions". Those
  definitions exist today (`.claude/agents/read-*.md`, `write-*.md`, `tester.md`), so this is
  overtaken in practice and against the vision line. The ruling is the living's. Item kept.
- (6) #3 is already distilled, witnessed. M operation-main-flow.md:20 reads "A flow is liable for its subflows"
  (Primary 368d92c43, 2026-08-19). Removed: proposal 3. Added: nothing.
- (6) #5 has since landed, witnessed. F compensation-launch.md:6 reads "with a one- or two-line brief" (Curriculum
  dc7c2f4, 2026-10-07). Removed: proposal 5. Added: nothing.
- (5) Witnessed: #1, #2, #4, #9, #10 and #11 are marked "Vision, module main-flow". There is no vision main-flow; the
  file is M operation-main-flow.md. Removed: "Vision, module main-flow." Added:
  "mind-skills/skills/operation-main-flow.md".

## 06 Messaging and relay — 06-messaging-and-relay.md, .proposals.md, .later-questions.md
Open rulings: 11 proposals and 4 later questions.
- (1) #7 Text 2 contradicts P vision-messaging.md:11-13 (Primary a379f7b28, 2026-09-17), witnessed. That line reads
  "Priority is a head on the datom / Priority.[HardAbrupt MiddleAbrupt Soft]". The book's Text 2 has "There is no
  separate soft or hard head." Removed: Text 2. Added: nothing. Text 1 is already distilled, so
  the whole proposal goes.
- (6) #8 is already distilled, witnessed. P vision-messaging.md:25-29 (Primary 776fe5b48, 2026-09-18) reads "four
  separate observations. None of them stands for another". Removed: proposal 8 except the line
  "Writing in your own transcript is not replying." Added: that line alone, to F
  compensation-messenger-clj.md.
- (6) #10 was overtaken, witnessed. P vision-messaging.md:33 (Curriculum 98c0ec6, 2026-10-04) admits results
  and blockers. The book's #10 has "Voices message only his words, questions, rulings and judgment."
  Removed: #10 and later question 1. Added: nothing.
- (6) #3 was overtaken, witnessed. The removed text, "the target always a flow id, never a registered name",
  is no longer in M knowledge-flow.md. F compensation-messenger-clj.md:12 now reads "TARGET is the
  recipient's six-character flow id." Both texts ("Psyche Fable" and "Psyche Primary") contradict that
  line. Text 1 also drifts from P vision-flow.md:22 ("A voice is an aspect carrying a rank"). Removed:
  Text 1. Added (Text 2 retargeted): "field-skills/skills/compensation-messenger-clj.md line 12, red:
  TARGET is the recipient's six-character flow id. / green: TARGET is the voice, aspect then layer."
- (5) #1 says "create", but P vision-messaging.md exists and lines 6-9 already say a message is a datom.
  Removed: "vision, vision-messaging, create" and "A message is a datom." Added:
  "psyche-skills/skills/vision-messaging.md, after line 9: Its head is its kind … only variants."

## 07 Presentation and books — 07-presentation-and-books.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and the later questions.
- (5) #12 targets "the book worker", which is `.claude/agents/book.md`, a generated tree outside the skill sources.
  Witnessed: line 451 still makes `options` "each a button". Removed: "operation, the book worker,
  remove". Added: the book role's authored source. Curriculum/roles.datom declares the `book` role,
  but I did not find where the body text is authored, so the path is unknown.
- (1) #10 names models ("Sonnet at light effort", "Opus judges") and contradicts P vision-model-roles.md:67-71
  (Primary 776fe5b48, 2026-09-18), witnessed. That line reads "Nothing else holds a model name". Removed: all three texts. Added:
  "The quaternary layer makes the message; the main flow judges it."
- (6) #3, #4 and #8 were overtaken, witnessed. F compensation-book-distillation.md:6 (Curriculum 1ace903, 2026-10-07) reads "Every book …
  is distillation proposals, 99% of it … no narrative, status or survey". The book has "More drawing than
  paragraph" (#3), "Six to nine points" (#4 Text 2) and "Drawings are hand-made SVG flowcharts" (#8).
  Removed: those lines. Added: nothing in operation-flashbook. The book rule lives in that file.
- (6) #11 was overtaken, witnessed. F compensation-book-distillation.md:8 reads "added lines in green, removed lines in
  red" (4d8ed32, 2026-10-07). Removed: Text 2 ("with no highlight"). Added: nothing.
- (3) The later questions quote him in full four times, for example "we always just make a new one."
  Removed: the quotes. Added: path and date.

## 08 Aspects, layers and who speaks to whom — 08-hierarchy-and-speech.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 6 later questions.
- (6) #5 was overtaken, witnessed. M knowledge-layer-models.md:16-19 now carries the map (eb4b8e893, 2026-10-05;
  37ca3f7, 2026-10-08). The book's "Tertiary: Sonnet, Terra. Quaternary: Sonnet at low effort" conflicts with
  ":17 Tertiary | Codex | Luna" and ":18 Quaternary | Claude | Haiku 5.5 … | Low". Removed: proposal 5 and the
  later question "Which models hold the tertiary layer?" Added: nothing.
- (1) #7 contradicts P vision-model-roles.md:74-76 (Primary aecc3c9b2, 2026-09-23), witnessed. That line reads "Every native
  main session is titled `<Aspect> <Model> <FLOW_ID>`". The book has "Never named by its model." Removed: that
  sentence. Added: nothing.
- (6) #11 Text 1 was overtaken, witnessed. F compensation-launch's level rule (field-skills 82067e7, 2026-10-07) reads
  "A Secondary reaches its Primary of another aspect only through that aspect's Secondary". The book's Text 1 has
  "A lower voice … sends one message up, never through another voice." Removed: "never through another voice".
  Added: "through its own aspect's layer above".
- (1) #10 "drop its last sentence" would delete "Design is Astra's, not Sol's" (P vision-flow.md:24). This is inferred:
  the book does not quote the sentence it drops. Removed: "drop its last sentence". Added: "keep line 24's last
  two sentences".

## 09 Identifiers and names — 09-identifiers-and-names.md, .proposals.md, .later-questions.md
Open rulings: 11 proposals and the later questions.
- (1) #10 contradicts P vision-flow.md:34-38 (Primary 776fe5b48, 2026-09-18), witnessed. That passage reads "A session is named after its direct
  ancestor … the ancestor is the name." The book has "Remove: a refreshed voice is named 'of' its ancestor".
  Removed: proposal 10. Added, if he wants the change: "psyche-skills/skills/vision-flow.md lines
  34-38, red: (current text) / green: A voice keeps its lasting name across a refresh."
- (1) #6 contradicts P vision-model-roles.md:76 (Primary aecc3c9b2, 2026-09-23) and M operation-main-flow.md:29, witnessed. Those lines read "titled
  `<Aspect> <Model> <FLOW_ID>`" and "`<Aspect>.{ <Model> <FLOW_ID> }`". Both of the book's texts have "aspect, layer and …".
  Removed: "A title is aspect, layer and". Added: "A title is aspect, model and".
- (6) #9 is half landed, witnessed. F compensation-messenger-clj.md:12 and F compensation-prose.md:11 already say six
  characters. Removed: "Commits, published pages and other artifacts carry six characters as their name" and "never carries the full id".
  Added: nothing. Only "then three words", once the word library exists, still needs a ruling.
- (6) #7 conflicts with F compensation-messenger-clj.md:12 ("TARGET is the recipient's six-character flow id"),
  which landed after the book; witnessed. The book has "A voice is reached by its lasting name". This needs a ruling between the two.
- (3) The later questions quote him seven times in full. Removed: the quotes. Added: path and date.

## 10 Talking to the living — 10-talking-to-the-living.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 5 later questions.
- (1) #3 contradicts P spirit.md:27 (Primary 923ed4ba6, 2026-07-25), witnessed. That line reads "Never pretend to know what you don't know;
  admit you don't know." The book has "Never report 'we don't know'." Removed: that sentence. Added: "When reading
  or running can answer it, find out before replying."
- (6) #6 and #7 had already landed before the book, witnessed. F compensation-behavior.md:26 reads "What was once wrong, objected,
  corrected, or run into is not written there … it lives in the flow log alone" (Primary ea088908d,
  2026-10-03 13:39 -0600). Removed: proposals 6 and 7 and later question 7. Added: nothing.
- (6) #2 was overtaken, witnessed. F compensation-book-distillation.md:6,14-16 (1ace903, 2026-10-07) reads "names the file, the
  lines removed and the lines added". Removed: proposal 2. Added: nothing.
- (6) #4 is partly landed, witnessed. F compensation-understanding.md:10 reads "Read speech-to-text for sense" (Curriculum
  dc7c2f4, 2026-10-07). Removed: "He speaks and a program types with mistakes. Read for what he means." Added:
  the misheard-word list alone, as an addition to compensation-understanding.md.
- (1) #9 Text 2 ("Everything after his last comment is approved") contradicts P vision-psyche.md:9-10 (Primary 7cbaa9d5f, 2026-09-18), witnessed.
  Those lines read "approved by the living". It also contradicts F compensation-design.md:7-9, "an edit the living has reviewed and approved" (e52a730,
  2026-10-08, after the book). Removed: Text 2. Added: nothing.

## 11 Psyche records — 11-psyche-records.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 5 later questions.
- (1) #9 Text 1 ("apply it directly and show him after") contradicts P vision-psyche.md:9-10 (Primary 7cbaa9d5f, 2026-09-18), witnessed.
  Those lines read "These statements are approved by the living". It also contradicts F compensation-design.md:9 ("changes only by
  an edit the living has reviewed and approved", e52a730, 2026-10-08). Removed: Text 1. Added: nothing.
- (6) #5 is already distilled, witnessed. P vision-psyche.md:6 (Primary b249309d2, 2026-09-18) reads "Psyche contains Spirit, Intent, Vision, and Notion".
  Removed: "His words are spirit, intent, vision or notion." Added: nothing.
- (6) #8 is already distilled, witnessed. P vision-psyche.md:13 (Primary b249309d2, 2026-09-18) reads "Distilled vision preserves references to its
  supporting raw records", and every vision-*.md has a "## Sources" section. Removed: proposal 8. Added: nothing.
- (6) #6's last sentence is already distilled, witnessed. P vision-distillation.md:32-33 (Primary 4828f0db5, 2026-08-27) reads "a correction of an agent's conduct can be vision".
  Removed: "A correction of how a seat behaves can be vision." Added: nothing.

## 12 Context — 12-context.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 11 later questions.
- (6) #9 was overtaken by this flow's own measurement, witnessed. `flows/5ed94b/reports/subagent-own-system-prompt.md`
  (2,606 bytes; Primary a7b52f550, 2026-10-03 18:13 -0600) shows that a Claude subflow receives its definition body and fixed harness
  paragraphs, not the stock built-in prompt. The book has "A subflow receives the harness's built-in instructions".
  Removed: that clause and later question 1. Added: "A Claude subflow's system prompt is its definition body plus
  the harness's fixed agent paragraphs; tools arrive as schemas."
- (2) #10 and #11 rest on "the book's own question 7" and "question 10". They rest on no record of his, witnessed.
  Removed: both "Rests on" lines. Added: "Rests on: no record; the flow's proposal."
- Ruling note, witnessed: #9's last sentence, "Standing context lives in the subagent's definition, never in a
  repeated brief", agrees with F compensation-launch.md:6-7. It conflicts with M knowledge-claude-harness.md:44, "what it must
  carry belongs in its brief". No distilled line decides between them.

## 13 Models, effort and quota — 13-models-and-quota.md, .proposals.md, .later-questions.md
Open rulings: 12 proposals and 11 later questions.
- (1) #1 Text 1 ("High effort is kept for one case: a quota about to reset unused") contradicts P intent-models.md:10-12
  (Primary 776fe5b48, 2026-09-18), witnessed. That line reads "it is never raised to buy quality". Text 2 equals the distilled line. Removed: proposal 1
  and later question 6. Added: nothing. The target is also wrong: it says compensation-default-effort, where the line
  lives in P intent-models.md.
- (1) #5 ("The secondary Opus builds and tests with Opus helpers") contradicts P vision-model-roles.md:65-66
  (Primary a74253599, 2026-09-19), witnessed. That line reads "Opus launches Sonnet and Haiku, and sometimes Opus, but rarely." Removed: "with Opus helpers".
  Added: "with Sonnet and Haiku helpers, and Opus rarely".
- (6) #2, #3 and #4 were overtaken, witnessed. M knowledge-layer-models.md:16-19 (37ca3f7, 2026-10-08) sets Quaternary Claude to Haiku 5.5
  Low and Tertiary and Quaternary Codex to Luna. The book has "low Sonnet", "Terra is paused … Luna takes its jobs" and the Haiku-or-Luna
  choice. Removed: proposals 2-4 and later question 5. Added: nothing.

## Books with nothing to flag
None. Every book from 01 to 13 has at least one finding.

---
## Part 4

# Part 4: book audit against the psyche record

Scope read: 5ed94b books 14-22, 24, 25 (each .md, .proposals.md, .later-questions.md; no book 23 exists), every file in 5578cc/books, 6e782c/books, 41fa34/books. Code-block line lengths were measured by script (scratchpad cb.py). No `flows/*/reports/*comments*.md` exists for these four flows; the comment reports that exist (aa887c, bad807, c02c0d, d4ae97) cover other flows' books, and one aa887c comment bears on book 16. `41fa34/reports/artifact-comment-notifications.md` is a documentation study, not a record of the living's comments.
Distilled record: psyche-skills, mind-skills and field-skills at their current HEADs. Most vision skills reached their present form in Primary 928aede20 (2026-10-07, "Migrate Vision and Intent into skills"). On 2026-10-02 vision-ethos had 59 lines; vision-signal, vision-sema, vision-datom and vision-meaning did not exist (`git show 102383f86`).

Applies to every 5ed94b book 14-25 (witnessed by grep and read). Kind 5: no proposal names a path under psyche-skills/skills, mind-skills/skills or field-skills/skills, and none gives removed lines. They name a "Module" or a bare skill name.
- `Kind: vision. Module: vision-nexus. Action: edit.`
+ `File: psyche-skills/skills/vision-nexus.md`
+ `Removed: <exact current lines, or "none">` `Added: <text>`
Kinds 3 and 4: each long draft `NN-*.md` is a survey of the living's quotes ("Part 1. What he wants", 29-54 `> ` lines per file), a status section ("What exists today, witnessed on 3 October"), and a list of questions. Remove each draft from what the living reads; only the proposals stay. The 5ed94b log records every publication without a URL, so no artifact URL exists for these books. The log (lines 102, 104) and the handover record no comments on them as of 2026-10-03 late, and I found no later comment record. So every proposal and later-question in them is an open ruling.

## 14 Permissions and authority — flows/5ed94b/books/14-permissions-and-authority*.md
URL: none recorded. Open: 12 proposals and 8 later questions.
- (6) Proposal 8 and later question 5 are settled. mind-skills/skills/operation-skill-designing.md:57 reads "A `vision-` or `intent-` skill is gold: the living's approved words, changed only on the living's word."; :56 does the same for spirit. field-skills 57d01ff (2026-10-07) added the same rule to compensation-design. Remove proposal 8 and later question 5. Witnessed.
- (6) Proposal 1 is already in field-skills/skills/trial-unblocking-commands.md:6 ("Launch a seat with the permission bypass."). For proposal 2, :8 now has the PermissionRequest hook deny the command with a message to rewrite the path, which is Text 2 in practice. Remove proposal 1, and ask proposal 2 only as "keep the deny-and-rewrite hook, or also answer within seconds". Witnessed (current text; present since at least acf7a0c, 2026-10-07).
- (3) "Rests on: 24 Sep, 'I want everything deployed.'" (proposal 12) quotes the living. Replace it with the record's path and date (inferred: source file not located).

## 15 Nexuses — flows/5ed94b/books/15-nexuses*.md
URL: none. Open: 12 proposals and 8 later questions.
- (1) Proposal 6 drifts from vision-nexus.md "Three parts and one path": "A Nexus has three parts … Signal … Operation … Memory … Nexus always names the whole; the part that does is Operation. … A signal reaches memory only through operation". Witnessed.
- "…any path from the Signal layer straight to the Sema layer. Everything passes through the Nexus layer."
+ "…any path from Signal straight to Memory. Everything passes through Operation."
- (6) Proposals 1, 3 and 4 have landed: vision-nexus.md "A kind of thing" (:10-12), "Configuration" (:87-94, "starts with no arguments"), "Splitting a Nexus" and "Polling is forbidden" (:129-145), and :118-121 on rewriting. Remove all three. Witnessed (all three were absent from the 22-line skill of 2026-10-02).
- (2) Proposal 9 ("Mind keeps the system's checked facts, each with a date and a trust level", and the whole roster) is a machine-made split of 25 Aug-2 Oct records presented as vision. Mark it as the flow's proposal, or cite each line's record by path. Inferred.

## 16 Ethos — flows/5ed94b/books/16-ethos*.md
URL: none. Open: 12 proposals and the later questions.
- (6/1) Proposal 9, "The context-module registry's list is named ModuleType, and Role is one of its entries", is contradicted by the living's comment of 2026-10-04 (aa887c/reports/his-comments.md, comment 2): "There's no role type and I don't know if we want to list the types in too many places. Where is the canonical place to find those types?" Witnessed. Remove proposal 9 and later question 1.
- (6) Proposals 2 and 3 and parts of 6 have landed in psyche-skills/skills/vision-ethos.md: :117 (no version in a file), :59 (no generics, only kinds), :218 and :243 (a variant named as a type carries it; inline payload), :447 (a comment on every section and every layered line). Remove the landed sentences. Witnessed.
- (7) 16-ethos.md:236-246 has 7 code lines of 69-105 chars. Replace with (longest line 49):
+ Library                ; shared root
+ []                     ; imports: none
+ [ Voice.{ Aspect.[ Psyche  ; types: aspect,
+                    Mind    ;   one of three
+                    Field ]
+           Layer.[ Primary  ;   layer, one of four
+                   Secondary Tertiary Quaternary ] } ]
+ [ Launchable.[ launch.[ Self ] ] ] ; kinds
+ [ Voice.[ Launchable ] ] ; every voice launches
  Witnessed (measured). Generator acceptance of the shortened form: inferred.

## 17 Datom, Protos, Signal and Sema — flows/5ed94b/books/17-datom-protos-signal-sema*.md
URL: none. Open: 12 proposals.
- (1) Proposal 3 says "declares requests and responses". vision-signal.md:19 reads "A Signal declares queries and responses; input and output are too low-level for it." Witnessed.
- "A definition declares requests and responses… A request and a response are never the same type."
+ "A definition declares queries and responses… A query and a response are never the same type."
- (6) The creates in proposals 3, 9 and 10 are overtaken. vision-signal.md, vision-sema.md ("Sema is the database engine of a Nexus", which is Text 1 of proposal 9) and vision-messaging.md:6-9 (a datom with no envelope) now exist, from 928aede20. Proposal 7 is in vision-nexus.md:56 ("datom and all text handling are compiled out of the Nexus") and mind-skills knowledge-ethos.md:16. Proposal 5 is answered by vision-nexus.md:56 ("knows its caller by the process, never by a claim"). Witnessed.
- (7) 17-datom-protos-signal-sema.md:52 is 80 chars. Replace with:
+ { Ada 1990
+   { «12 Rue de la Paix» Paris 75002 }
+   [ Author Reviewer.{ 2024 17 } ] }
  Witnessed (length). That datom accepts the line breaks: inferred.

## 18 Code craft — flows/5ed94b/books/18-code-craft*.md
URL: none. Open: 12 proposals.
- (6) Proposal 11 repeats lines already in psyche-skills/skills/spirit.md: :10 "Beauty is the symptom of good engineering…", :12 (correctness pays for its machinery), :19 (the terminal best). The first sentence of proposal 9 repeats spirit.md:17 "Backward compatibility is never a design variable." Remove proposal 11 except "Simple is worth more than counted", and drop the first sentence of proposal 9. Witnessed.
- (6) Proposal 4 overlaps intent-mandatory-traits.md:8 ("Every method call in our Rust code lives under a trait"). Remove it, or propose only the sentences that skill lacks. Witnessed.

## 19 Testing and verification — flows/5ed94b/books/19-testing-and-verification*.md
URL: none. Open: 12 proposals.
- (6) Proposal 2 has landed as psyche-skills/skills/intent-testing.md "A proof of concept is tested in a sandbox first … only when it cannot run in one, such as a browser login". Remove it. Witnessed.
- (5/6) Proposal 9 ("tester … create") targets a role definition, not a skill source, and the role already exists. The tester definition in this session reads "Given only a bounded target, immutable revision, authority limits, and acceptance contract…". Remove it. Witnessed (definition text); where it is authored: not checked.
- (1) Proposal 6 is labelled "Kind: spirit. Module: behavior". The behavior skill is field-skills/skills/compensation-behavior.md, not a spirit skill.
- "Kind: spirit. Module: behavior."  + "File: field-skills/skills/compensation-behavior.md" Witnessed.

## 20 Harnesses and remote control — flows/5ed94b/books/20-harnesses-and-remote-control*.md
URL: none. Open: 12 proposals.
- (6) Proposals 6, 7 (in part) and 12 have landed in vision-flow.md. The "Starting flows" section has "A Nexus component decides the system prompt and everything about a launch, replacing the harness's subagents". :46 has "Every harness event reaches Flow through the harness's hooks calling the Flow CLI … a marked block … becomes an action, a book among them, with no tool call". Remove 6 and 12. Keep only the per-hook items in 7 that :46 lacks. Witnessed.
- (2) Proposal 12 says "the rest is proposed" yet is labelled vision. Proposal 8's 15 minutes rests on his "I don't know". Neither is the living's ruled line. Witnessed (the book's own words).

## 21 The cluster and deployment — flows/5ed94b/books/21-cluster-and-deployment*.md
URL: none. Open: 12 proposals and the later questions.
- (6) Proposal 2 is in vision-deployment.md: "Zeus is a stable node, and stable nodes are not where testing happens." The first sentence of proposal 5 is in field-skills compensation-orders.md:8 "Deploy means the intended system and user environment now." Proposal 1's model clause is in compensation-default-effort.md:16 "Local model hosting and its files live only on Prometheus." Remove what has landed. Witnessed.
- (2) Proposals 7, 9 and 12 say "The order / fields / collector … are proposed" yet are labelled intent, knowledge and vision. Witnessed (the book's own words).

## 22 Meaning and vocabulary — flows/5ed94b/books/22-meaning-and-vocabulary*.md
URL: none. Open: 12 proposals.
- (1) Proposal 8, "Sema is the meaning language … the database is then renamed", contradicts vision-sema.md ("Sema is the database engine of a Nexus") and vision-meaning.md:17-18 ("The language may take a poetic Latin or Greek name of its own"). Witnessed.
- "Sema is the meaning language: signs that stand for meanings,"
+ "The meaning language is made of signs that stand for meanings,"
- "That Sema is the name rests on one 26 Sep word; the database is then renamed."
- (6) Proposal 10 is in vision-meaning.md:72 "Every Sanskrit-rooted type carries an English name as well." Proposal 9 is in :22-23. In mind-skills knowledge-vocabulary.md, proposal 1 Text 1 is :6, proposal 4 is :16 ("a presentation is one message in it"), and proposal 6's "agent" is :41. Proposal 3 is mind-skills knowledge-layer-models.md. Remove all of these. Witnessed.

## 24 Voice input and front-ends — flows/5ed94b/books/24-voice-and-front-ends*.md
URL: none. Open: 12 proposals and the later questions.
- (1) Proposal 8, "Every spoken message passes the lowest layer's correction before any flow reads it", contradicts mind-skills operation-psyche-interraction.md:42 "The first flow that hears the psyche corrects each speech-to-text error inside the quote". Witnessed.
- (6) Proposal 7 and the first half of proposal 6 are in that same :42 (bracketed correction, "Read for what the psyche means"). Proposals 6 and 7 are also mislabelled "Kind: spirit". Witnessed.
- "Kind: spirit. Module: psyche-interraction."  + "File: mind-skills/skills/operation-psyche-interraction.md"

## 25 The private layer — flows/5ed94b/books/25-private-layer*.md
URL: none recorded. Open: 12 proposals, main-book questions 1-4, later questions 5-16. No comment on it found.
No distilled private-layer skill exists. The raw record is: 6cc91b/vision/{privateLayer,layerZero,thirdModel,criome}.md, 024bc7/vision/{soul,thirdModel}.md, e1953c/vision/{privateLayer,secrets,criome}.md, 1ac573 operational-privateLayerCoreLayer, da1e3f operational-coreSoulCluster, persona records in 05c604, 752e0f, 840e42 and 6fb948, and e71fa5/vision/private-data-separation.md. Every quote in the book matched one of these by grep. Two of them, the soul quote and the kernel-process quote, also sit in bcd02a/notion/persona.md, but they have vision copies. Witnessed.
- (1) Proposal 11 and draft line 199, "Persona owns which flows run and where", contradict vision-flow.md "Flow is the Nexus that manages flows … Flow holds the lock on flows". The record gives Persona clusters and services: 05c604/vision/persona.md, "manages all of the clusters, the different layers", and 6fb948, "checks all the services and makes sure they're running". Witnessed.
- "Persona owns which flows run and where."
+ "Persona manages the clusters and their layers and keeps their services running; Flow launches and ends flows."
- (1) Proposal 4 Text 1 writes a model into vision ("It runs on Kimi K3 through OpenCode"). vision-model-roles.md says "The model is declared once, as typed configuration in Flow … Nothing else holds a model name". Witnessed. Kimi K3 came as an order to set it up (6cc91b/vision/thirdModel.md, 2026-09-14).
- "No commercial model ever serves the private layer. It runs on Kimi K3 through OpenCode, by a provider chosen for privacy, so it stays self-hostable."
+ "No commercial model ever serves the private layer. Its open-weight model is chosen for doubt and care, and its provider for privacy, so it stays self-hostable."
  (Kimi K3 goes in Flow configuration and the knowledge-layer-models row.)
- (1) Proposal 12 Text 1 ("until the soul's private repository opens") departs from Primary CLAUDE.md "chartered but NOT ACTIVE until its third, open-source seat runs" (c9a6be428, 2026-09-14), which matches Text 2. Witnessed. The charter is a project instruction, not a skill line.
- (2) Proposals 6, 9 and 10 carry methods and lists the book itself calls "proposed": the sterilizing method, the refusal list, the never-sent list. Proposal 10 is labelled intent and proposal 11 vision ("The division is proposed"). Witnessed. By operation-skill-designing.md:61, a rule written by flows goes in a trial- skill:
- "Kind: intent. Module: private-layer. Action: edit."  + "File: field-skills/skills/trial-private-filter.md (new; flow's proposal)"
- (3) Proposals 6, 8, 9 and 12 quote him in "Rests on" ("There's no name, there's no association", "it'll get feedback to correct it", "Everything is turned into a lesson", "We're gonna work towards…"). The draft holds 29 quotes.
- "Rests on: 14 Sep, \"There's no name, there's no association\"."  + "Rests on: flows/6cc91b/vision/privateLayer.md (2026-09-14)."
- (4) Draft lines 209-217, "Part 2. What exists today", are a status report. Remove them. Witnessed.
- (5) Every proposal reads "Module: private-layer". For proposals 1-5, 7 and 12: + "File: psyche-skills/skills/vision-private-layer.md (new)". Proposals 2-12 say "Action: edit" on a file that does not exist; they should read "create". Witnessed.

## 5578cc books — flows/5578cc/books/*.md (14 files)
Every file applies to all of them. (4) Each is an answer or status page, not a file-line proposal. (3) answers-flow-ids, flow-ids-in-words-settled, answers-layers, answers-three-questions and what-a-relayed-comment-carries quote his comments back to him in full. (5) Where a line is proposed, it names a skill by description ("the behavior skill", "the Flow vision skill"), not a path. URLs: three-questions-waiting-on-you is claude.ai/artifact/FscA6jbcWEEwjpmB8X27Nm (file header). may-field-speak-to-psyche points to 1LhLZg92hyrjXQsT3f6Yc1 («Two meanings for Flow»). No other URL is recorded.
- (6) what-a-relayed-comment-carries has landed in mind-skills operation-relaying-the-living.md:6-10. Witnessed.
- (6) messages-to-fable-skill-line and messages-to-fable-vision-flow are settled in the general form, choice 2: vision-messaging.md:33 "Send only messages that require the recipient's action, deliver a result it awaits, or report an error…". Witnessed.
- (6) The table in answers-layers ("Quaternary | Sonnet, low effort") is overtaken by knowledge-layer-models.md:18, which gives Claude Quaternary as Haiku 5.5, low, by living ruling of 2026-10-08 (mind-skills 37ca3f7). Witnessed.
- (1) flow-ids-in-words ("the pane reads Psyche Primary") and answers-flow-ids ("`Psyche.Secondary` and its three words") contradict vision-model-roles.md "Every native main session is titled `<Aspect> <Model> <FLOW_ID>` … never titled Mind Medium". Witnessed.
- answers-flow-ids and flow-ids-in-words-settled are the same book with conflicting collision rules: "adds a fourth word" against "Flow refuses and says so". The settled copy supersedes; withdraw answers-flow-ids. Witnessed.
- Open (no ruling found): find-out-and-keep-knowledge choices 2a/2b. answers-on-flow-launch item 3; its rule is not found verbatim in any skill (grep "deterministic"). how-flow-builds-a-prompt's closing question.

## 6e782c books — flows/6e782c/books/*.md (4 files)
(4)/(5) All four are status reports on the quota query, with no skill target. URL: none. The log (lines 24-28) records each publish refused by the daily limit. Witnessed. (6) 6e782c/log.md:25 and :27 record that d66c26 cancelled quota-query-contract-review-and-completion-route and quota-pacing-how-much-until-when; withdraw both. Open: the planned-hours question in quota-query-installed-and-ready.

## 41fa34 books — flows/41fa34/books/*/source.md
- astra-five-candidates. (4) A survey of five candidate systems, with no file proposal. (7) :54 is 53 chars and is a prose arrow chain inside a ```text block. Witnessed. Replace the block with prose: + "The audit proposes an offline path: export, validate, explicit map, import, read back." URL: d4ae97/log.md:213 records «Astra's five candidates» at claude.ai/artifact/3AXTdcjQjzqka5kFHCoLZw with 7 rulings. This source has no questions, so the published page differs from it (inferred).
- claude-quaternary-update. (4) Status bullets. (6) Landed as knowledge-layer-models.md:18 (37ca3f7). URL: d4ae97/log.md:212, «Haiku on the Quaternary», YaThKLYQWshyy8UcjKssXq; its one open ruling is "row scope All vs All but Mind and Field". Witnessed.
- flow-current-environment. Each section uses "FILE: skills/knowledge-flow.md … ADD", with no repository named and no removed lines.
- "FILE: `skills/knowledge-flow.md`"  + "File: mind-skills/skills/knowledge-flow.md; Removed: <current line>"
  (4) It adds a dated hm-list snapshot of flow ids and statuses, plus history ("an earlier 14-pane claim is withdrawn"). A knowledge skill carries the thing as it now is. Drop the snapshot rows and the withdrawn-claim sentence. Witnessed. Not landed: mind-skills knowledge-flow.md has no hm-list line (grep).

Nothing to flag beyond the shared findings: none. Every in-scope book carries at least kinds 4 and 5.

---
## Part 5

# Part 5: book audit against the psyche record

Read: every listed book, the four comment reports, psyche-skills/skills (branch spirit-terminology, origin/main 4312cc0), mind-skills and field-skills origin/main, raw records under flows/*/vision, and the flow logs. Code-block line lengths were measured with awk (fence-delimited lines over 52 characters). W means I read both sides; I means inferred. Open rulings: no flow log records a ruling returned on any book below, so each one's rulings stay open unless a finding says it was overtaken.

## ebbe30/books/1-spirit-three-skills.md — «Spirit, three skills»
URL: https://claude.ai/artifact/XUWRutzPLCSzK94kKnFgT5. Seven rulings open (ebbe30/log.md:25).
- (1) §3 drops what operation-skill-designing says (mind-skills 991e1a, lines 56-62): "A `vision-` or `intent-` skill is gold: the living's approved words, changed only on the living's word" becomes "intent- The living's declared goals and rules." and vision- loses "changed only on the living's word". W. Removed (§3): `intent-   The living's declared goals and rules.` Added: `intent-   The living's declared goals and rules; gold, changed only on the living's word.`, plus the same clause on the vision- entry. operation- also loses "no glance from the living is needed": add it back.
- (2) §1 "A spirit-healing skill corrects them." and §3 `spirit-healing-<model>` treat a hedged word as the ruled name. Source: ebbe30/vision/spirit.md:15-17, "You could even say healing or I'm trying to think of something ... The spirit is either healing or compensation." W. Added (§1): `A spirit skill for that model corrects them.` Add a ruling: name it (a) spirit-healing (b) spirit-compensation.
- (4) §6 (research order) and §7 (a question) name no file or lines. W. Removed: §6 and §7 from the book; send them as a concise message outside a book.
- (4) Prose sits in code blocks (§1-§5), and §1/§2 give "Removed: the engineering lines" without the lines. W. Render as text; list the removed spirit.md lines 10-25 in red.
- (5) §2 and §3 give no repository path. W. Added: `File: psyche-skills/skills/spirit-engineering.md, new` and `File: psyche-skills/skills/spirit-training.md, new; mind-skills/skills/operation-skill-designing.md lines 55-62 removed`.
- (6) The psyche-data principle the living said "will go in spirit" (d4ae97/reports/queue-book-comments.md, 2026-10-08) arrived after this book. It is still absent from spirit.md, and the only landing is compensation-design (field-skills e52a730, 209ae90). W. The next edition adds a §1 line. Its wording is drafted in ebbe30/reports/spirit-psyche-data-line.md, which I did not read.

## d4ae97/books/5-spirit-is-a-kind.md — «Spirit, a kind of skill»
URL: https://claude.ai/artifact/3wPT8EehoyorHacFuD8hEm.
- (6) Overtaken. P1 landed amended as mind-skills 991e1a, following the living's comment (spirit-book-comments.md thread 5). The "AI/agent" lines it quotes were rewritten in psyche-skills 4312cc0. P2-P6 were carried into ebbe30's «Spirit, three skills». W. Removed: the whole book from the standing set; point to XUWRut.
- (4) P4 opens with a narrative ("A machine flow added this line ... today"), and P5/P6 name no file. W.

## d4ae97/books/9-spirit-edit-incident.md — «Spirit edit incident»
URL: https://claude.ai/artifact/B4XrVYH7m6sMKTopQCBJTQ. Six rulings open.
- (4) Lines 4-29 (account, timeline, cause chain) are narrative. The living asked for an incident report (spirit-book-comments.md thread 1), so this book answered that request. W. Removed: lines 4-29 from the book; keep them as a report linked from P1.
- (6) P1 says the guard line "landed today in compensation-design (57d01ff)". e52a730 removed that line and replaced it with the psyche-data rule (209ae90 reworded it). W. Removed: `The same line landed today, machine-authored, in compensation-design (field-skills 57d01ff).` Added: `compensation-design now opens with the psyche-data rule (field-skills e52a730); this line would carry it into the kind lines.`
- (6) P2 asks the same ruling as book 5's ruling 4 and ebbe30 §2. W. Keep it only in ebbe30 §2.
- (7) Line 64 is 81 chars, and P3's removed line does not match the file. spirit.md:3 reads `dependencies: [compensation-behavior, compensation-correction, knowledge-vocabulary, compensation-book-distillation]`. W. Replace the block with:
  `-dependencies: [compensation-behavior,`
  `-  compensation-correction, knowledge-vocabulary,`
  `-  compensation-book-distillation]`
  `+dependencies: [compensation-behavior,`
  `+  compensation-correction, knowledge-vocabulary]`

## d4ae97/books/1-three-days-of-flows.md — «Three days of flows»
URL: https://claude.ai/artifact/9MdTXzAK8EwvhGy3tHKeyQ.
- (4) All 270 lines are census and narrative, and its five "Proposals for distillation and action" (lines 256-270) name no file and no lines. W. Removed: the book from the living's set. A proposal survives only as a target line, for example in field-skills/skills/compensation-launch.md: `A successor receives a short read-once task pointer; the predecessor keeps the history.`
- (5) No proposal names a skill source. W.

## d4ae97/books/2-fable-first-reading.md — «Context modules, into Intent»
URL: https://claude.ai/artifact/SqphBp52LVGdDUYNt3XTaS. One ruling open.
- (5) The target `Intent/contextModules.md` does not exist and lies outside the skill sources. W. Removed: `## Proposal 1: new file Intent/contextModules.md`. Added: `## Proposal 1: psyche-skills/skills/intent-context-modules.md, new`. The text matches d4ae97/vision/contextModules.md (2026-10-07) (W). Its prose renders as text, without the `# Context modules` line inside a code block.

## d4ae97/books/3-raw-records-pile-up.md — «Raw records pile up»
URL: https://claude.ai/artifact/6QyyEQR6TtBEKzDE6iPUAw.
- (6) Overtaken. Book 10 P3-P6 carry its P1-P4 with full paths. Book 10 itself marks P5 as overtaken, since vision now lives in skills. W. Removed: the book; book 10 stands.
- (4) Line 4 is status. (5) `psyche-distillation` and `psyche` give no path; they are mind-skills/skills/operation-psyche-distillation.md and knowledge-psyche.md. W.

## d4ae97/books/4-curriculum-ethos.md — «Curriculum's ethos, and every Nexus's three roots»
URL: https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU. The living commented on it ("This is garbage", d4ae97/vision/curriculum.md, 2026-10-07).
- (4) Lines 4-64 are a survey. P2 is an order to Astra with no file. W.
- (1) P1 repeats vision-nexus.md:148, "A Nexus has three parts, each its own ethos specification: Signal ... Operation ... Memory". It also conflicts with vision-ethos.md:30, which names four roots including Library. W. Removed: P1's "Every Nexus has a Signal, an Operation and a Memory root". Added: none; the line already stands.
- (7) Eight ethos lines run over 52 chars, the longest 181 (lines 8, 12, 14, 15, 16, 31, 42, 44). W.
- (6) Overtaken by book 8 / 0c85a3 «Curriculum, a vision in ethos» (d4ae97/log.md:193). W. Removed: the book.

## d4ae97/books/8-curriculum-vision-in-ethos.md and 0c85a3/books/curriculum-ethos.md — «Curriculum, a vision in ethos»
URL: https://claude.ai/artifact/XJ2gicWJRFcC75CdyP2jyr. The 0c85a3 file is the same source, with no URL in 0c85a3's log. Ten rulings open (one in the 0c85a3 copy).
- (2) Every semantic string becomes a one-position struct, `Text.{ String }` and `SkillName.{ Identifier }`, and §1 says "Every semantic string has a named struct type". The raw rulings (d4ae97/vision/ethos.md:45-52, 79-84, 2026-10-06) say `Name.Type` "is a new type ... we're engineers" and "I don't like the single field struct". W. Removed: `Every semantic string has a named struct type.` Added: `Every semantic string has a new type, Name.Type.` In the ethos blocks, `Text.{ String }` becomes `Text.String`, `SkillName.{ Identifier }` becomes `SkillName.Identifier`, and so on for every one-position struct.
- (1) vision-ethos.md:225-234 still calls `FilePath.String` an alias (`pub type`). The book's `SkillNames.Vector<SkillName>` is an alias under that line, while §1 means a named type. W. This needs a vision-ethos distillation of the 2026-10-06 newtype records. That is a separate proposal, not one in this book.
- (4) §1's prose sits in a ```markdown block. W. Render it as text.

## d4ae97/books/6-flow-as-it-runs-today.md — «Flow as it runs today»
URL: GE2fmKQNcK9zP9QkBEUnej (d4ae97/log.md:195). Four rulings open.
- (4) P1 is a dated registry snapshot ("Live check, Oct 7 ... An earlier claim of 14 is withdrawn"), status and history inside a skill. W. Removed: P1's lines 30-44. Added: none.
- (4) Lines 4-15 are framing. The proposals are knowledge- lines, which flows write from verified facts (operation-skill-designing:14). Asking the living to rule on them is out of kind. W. Removed: the rulings. Added: `Landed as knowledge after a witness; no ruling.`
- (4) The proposals are "+"-prefixed prose in code blocks. W.

## d4ae97/books/7-levels-tests-traits.md — «Levels, tests, traits»
URL: HuFye2HYkS5bEUnQGy76gp (d4ae97/log.md:195). Four rulings open.
- (6) The P1 message-level lines, P2 and the P3 trait line landed as compensation lines (field-skills 82067e7: compensation-launch:27-31, compensation-testing:6-8, compensation-design:34). W. The rulings now ask only for promotion. Added to each: `Landed as compensation (82067e7); ruling: promote to this skill.`
- (5) P2-P4 give no repository: mind-skills/skills/operation-testing.md, psyche-skills/skills/vision-ethos.md, mind-skills/skills/operation-skill-designing.md. W.

## d4ae97/books/10-distillation-books.md — «Distillation books»
URL: https://claude.ai/artifact/RoMY4hePWH6oGjmXrW6mXT. Ten rulings open.
- (4) Lines 4-20 are status. The living asked for the status (d4ae97/vision/books.md, "what is the status?", 2026-10-08), but the book rule sends it outside a book (compensation-book-distillation:12). W. Removed: lines 4-20; send them as a concise message.
- (6) P7's "bad example, then the good" and "Ethos in a book says what its types are for" were landed by 209ae90 (compensation-book-distillation:18-19), and its anchor "after line 15" now falls mid-sentence. W. Removed: those two lines from P7. Added: `Added, after line 16:`.
- (2) P9's "the recipient is not told" settles a hedge. Source: b7ba00/vision/messaging.md:91, "Do we even need to tell the model ...? I don't know. I don't think so." W. Removed: `kind; the recipient is not told.` Added: `kind; the database holds it, and the recipient need not be told.`

## d4ae97/books/11-the-fixed-metaflow-record.md — «The fixed Metaflow record»
URL: https://claude.ai/artifact/H8pURfefKzc9WW7HWe6Qa1. Four rulings open.
- (5) P1-P3 target code (flow/crates/flow-nexus/ethos/memory.ethos, signal-flow/ethos/signal.ethos). W. Restate them as vision-flow lines in psyche-skills/skills/vision-flow.md. The living called the same memory.ethos proposals in «The queue and the waking rule» "misdirected" (d4ae97/vision/psyche.md:6). What he meant by that is unknown. I.
- (4) Lines 4-26 are measurements. W. Keep only the 45-byte figure in P4.
- (7) Lines 41, 43, 44, 46 and 49 run 53-55 chars. W. Move the comment column of lines 39-51 from 34 to 31, which brings the longest line to 52.

## d4ae97/books/11-rust-toolchain.md — «Rust toolchain»
URL: https://claude.ai/artifact/P8kqk7Kk8vsofdympMeu2n.
- (5) P3-P7 target rust-build/flake.lock, ARCHITECTURE.md, 82+62 flakes and every Cargo.toml. W. Removed: P3-P7 and rulings 3-5 from the book; they become work under the P1 policy once it is ruled.
- (4) Lines 4-14 are measurements. W. The policy itself matches d4ae97/vision/tools.md ("latest production-ready ... something like nightly", 2026-10-08). W.

## d4ae97/books/12-clojure-the-vision.md — «Clojure, the vision»
URL: https://claude.ai/artifact/Aua4vB78BmKoE7wjuFVBWc. Three rulings open.
- (1) P2's ethos example writes `LockName.String`, which follows vision-ethos (alias). Book 8 writes `{ Text }`, and the raw record says `Name.Type` is a new type. W. Added (P2, after the ethos block): `LockName.String is a new type, not an alias.` The vision-ethos distillation noted under book 8 decides this.
- The other lines trace to the framework-study comments (d4ae97/reports/framework-study-comments.md threads 1-3) and to 88475f/vision/cljTools.md. W. Nothing else to flag.

## d4ae97/books/13-astra-five-candidates.md — «Astra's five candidates»
URL: https://claude.ai/artifact/3AXTdcjQjzqka5kFHCoLZw. Seven rulings open.
- (5) All five targets lie outside the skill sources: flow-evidence/0c85a3/... (four) and clj-build/lib/uberjar.nix. clj-build origin/main is unchanged since 8cc9991 (2026-09-26). W. Removed: the book. Its rulings go to Mind as a concise message. The skill-level candidates (the topic registry, the JSON variant mapping) need vision lines, for example in psyche-skills/skills/vision-datom.md: `JSON for a variant is one object keyed by the variant's name.`
- (4) Lines 4, 20, 41, 53 and 71 are status and measurements. W.

## d4ae97/books/haiku-quaternary.md — «Haiku on the Quaternary»
URL: https://claude.ai/artifact/YaThKLYQWshyy8UcjKssXq. One ruling open.
- (6) The "All" row is already committed (mind-skills 37ca3f7, branch spirit-kind, 11:28, before the 11:32 publish). The ruling asks about a change that has already landed. W.
- (1) "All" contradicts knowledge-layer-models.md:8 ("Mind runs on Codex only ... Field takes its models from the same") and the raw record d4ae97/vision/models.md:15 ("the field models are the same as the mind models"). W. In 37ca3f7, removed: `| All | Quaternary | Claude | Haiku 5.5 ...`. Added: `| All but Mind and Field | Quaternary | Claude | Haiku 5.5 ...`. The ruling then goes away.

## d4ae97/books/secondary-opus.md — «Secondary is Opus, into the skill»
No URL found in the logs.
- (6) Overtaken. mind-skills/skills/knowledge-layer-models.md:14 already reads Claude Secondary = Opus 5.5, Medium. W. Removed: the book.
- (5) The target is `Curriculum/skills/...`, a path that is gone. (4) "Why I asked" is narrative. (7) Lines 12 and 16 run 86 and 124 chars. W.

## d4ae97/books/voices.md — «How we call the voices»
URL: https://claude.ai/artifact/8d8WhKf4R3wxdzA7Q49nhP.
- (3) Lines 4-11 quote the living back. W. Removed: lines 4-14.
- (6) The `Seat` type and ruling 1 are overtaken by "no need for the terminology seat" (d4ae97/vision/vocabulary.md:7) and "Secondary is Opus, so this seat is Psyche Secondary" (d4ae97/log.md:21). W.
- (7) Eight lines run over 52 chars (lines 18-33, up to 96). (5) No skill target. W. Removed: the book.

## d4ae97/books/whats-going-on.md and whats-going-on-2.md — «What's going on», editions 1 and 2
URLs: https://claude.ai/artifact/4AisnUBdem1qhrUBMwX4t2 and https://claude.ai/artifact/EfY4Azh1GMUgaUat9a6ZhY.
- (4) Status boards throughout. (3) They quote him. (7) 40 and 53 lines over 52 chars. W.
- (6) The seat rulings are overtaken: ed.1 4-8, ed.2 4-7 by the approved keeper twelve (d4ae97/log.md:169) and the retirement of d66c26 and f768df (log 164, 169), and ed.1 ruling 4 by the Opus 5.5 row (knowledge-layer-models:14). W. Removed: both books. Edition 1 is superseded by edition 2.

## d4ae97/books/jev-pages-copy.md and jev-meat.md — Jev proposals; «fuzzy-jev: what it is»
URLs: https://claude.ai/artifact/WJksrEuDQboxRaT1teAhNL (mapped from "Jev book from the Pages trial", I) and https://claude.ai/artifact/UG5xSKSss5DbJ33rYmn6ZR.
- (6) jev-pages-copy was superseded by jev-meat after "it's lame ... give me some meat" (d4ae97/vision/books.md, 2026-10-05). W.
- (5) jev-meat's two rulings target judge's Cargo dependency, not a skill. (4) 280 lines of survey. (7) 25 lines over 52 (jev-pages-copy: 3). W. Added, as the skill line: mind-skills/skills/knowledge-jev.md, new: `judge may use fuzzy-jev 0.6.0 as transport only, default features off; its fuzzy rules are not taken.`

## d4ae97/books/ethos-distillation.md and ethos-distillation-2.md — «Ethos, distilled», editions 1 and 2
URLs: https://claude.ai/artifact/GRS6NF4jvJr9A25hq3KgAh and https://claude.ai/artifact/5QcHZT4VEvBgAa5QWRHSvV.
- (6) Edition 1 is superseded by edition 2. Edition 2's statements on central (P1), terse (P4), everything-is-a-type and inline (P5/P6) and vertical (P8) now stand in vision-ethos.md:11, 37, 216 and 445. W. Its P7 "A new type is written as its name, a dot, and the type it holds" is not in vision-ethos, which still says alias (lines 225-234). W.
- (3) His words are quoted in every section (">" blocks). (5) The target is `Vision/ethos.md`. (7) 53 and 106 lines over 52. W. Removed: both books. Added: one proposal, psyche-skills/skills/vision-ethos.md. Removed: `[ FilePath.String ; types: FilePath is an alias of String`. Added: `[ FilePath.String ; a new type holding String`, with the Rust shown as `pub struct FilePath(String);`.

## 3ec648/books (three books, 2026-10-02)
URLs: «Ethos, six statements and the voices» https://claude.ai/artifact/Jccod1quu2k753PznMTkg6; «Where the edit goes, and vision as skills» https://claude.ai/artifact/7ttvuKV1HCb8mq68xP7n5u; «Ethos as two skills, the case study» https://claude.ai/artifact/SeGPUZkyxvZK8SebNbRhBL.
- (6) Overtaken. Their texts are landed: vision-ethos.md:30, 216 and 445 match two-skills §2 word for word, vision-flow.md:22 carries the nine voices, and the prefix set lives in operation-skill-designing:55-62. W. Removed: all three.
- (3) Each one quotes him (for example six-statements lines 7, 26, 36-37, 59). (4) where-the-edit-goes §1 is status. (5) The targets are `Vision/...`. (7) There are 2, 3 and 10 long lines. W.
- (1) Downstream of six-statements §1: vision-flow.md:22 "Primary, Secondary, Tertiary, nine voices" predates "We actually have four models so it'll be quaternary flows" (d4ae97/vision/models.md:28, 2026-10-08). W. A proposal for vision-flow, removed: `Primary, Secondary, Tertiary, nine voices`. Added: `Primary, Secondary, Tertiary, Quaternary, twelve voices`.

## c02c0d/reports/book-comments-only.md
- (5) The targets are subagents/book.md and flows/8904b1/specs/book.md, which are not skill sources. W.
- (4) Lines 3-7 are narrative ("Done on 2026-09-28 ..."). W.
- Still open, not overtaken: subagents/book.md:151-155 still reads "each a button" and "written by the page" (W). The record c02c0d-1 exists in flows/c02c0d/vision/presentation.md:3. W.

## d4ae97/reports: spirit-book-comments, queue-book-comments, framework-study-comments
These are verbatim records of his comments, not books.
- Acted on: the spirit comments, through 4312cc0, 991e1a and «Spirit, three skills»; the framework-study comments, through books 12 and 13.
- Still undone (W): the psyche-data line in spirit (queue thread). The "machine" terminology beyond spirit also remains, since knowledge-psyche.md:6 still reads "The purpose of AI".

Nothing to flag: none. Every book in scope carries at least one finding.

---
## Part 6

# Part 6: books of e5a0bc, f5a6e9, f768df, 8475a9, 91ea9f, b27767

Scope as audited: 32 book sources modified since 10-02 (`find -mtime -7`). There are no `reports/*comments*.md` files for these six flows (`ls`). The living's comments were found instead in `flows/*/vision/*.md` records that cite the book or its artifact URL.

Rule source: `field-skills/skills/compensation-book-distillation.md` as of 209ae90 (10-08 11:15). Line 7 (prose not in code blocks) landed in 4d8ed32 (10-07 18:46). The skill-source paths landed in 3a98f3b (10-07 12:38). Until then the line read "Curriculum/skills ..., never a file under Vision/ or Intent/". Skill sources moved out of Curriculum in fef9864/acf7a0c/9940abd (10-07 12:12).

Kind 7 was measured by a script that counts lines over 52 characters inside ``` and ~~~ fences. Witnessed means both sides were read. Inferred means the flow judged it.

Shared finding (kind 4/5, witnessed): every book written before 10-07 12:38 is narrative or a design survey whose targets are code, ethos, `Vision/` or `Curriculum/skills/` paths. Each section below gives only its own fix. The generic fix is the same for all of them: delete the narrative and keep one section per change, in the form `<repo>-skills/skills/<name>.md, line N` + removed lines + added lines + ruling.

## f5a6e9 «The queue and the waking rule»: flows/f5a6e9/books/11-the-queue-and-the-waking-rule.md
URL https://claude.ai/artifact/HUA3QJiFyVErW12sgJ79wC. Rulings 1-4 are open. His only comment, at Ruling 2 (d4ae97/vision/psyche.md:4), calls proposals 1 and 2 "brilliant in content but ... misdirected".
- (5) witnessed: proposal 1 targets `signal-flow/ethos/signal.ethos` and proposal 2 targets `flow/crates/flow-nexus/ethos/memory.ethos`. Neither is a skill source, and his comment confirms they are misdirected. Fix: re-target both proposals to `psyche-skills/skills/vision-messaging.md`, after the queue section of proposal 3, and add the four kinds there as prose:
  - Removed: none.
  - Added: "A request is of one kind: an order or a question wakes a sleeping metaflow; a result waits; a notice never wakes."
- (1) witnessed: proposal 4 says "Flow keeps each metaflow's queue". The same book's proposal 2 puts `Queue.Vector<Request>` in Flow's Memory. His comment of 10-07 (f5a6e9/vision/flow.md, comment 9) reads "I don't think that it's Flow's job to hold messages". Book 10, proposal 5 proposes the line "Flow holds no messages." Fix for proposal 4:
  - Removed: "Flow keeps each metaflow's queue and applies the waking rule:"
  - Added: "Message keeps each metaflow's queue; Flow applies the waking rule:"
  - Drop proposal 2.
- (2) inferred: the split into Order/Question (wakes) and Result/Notice (waits) is the flow's own. His record (f5a6e9/vision/messaging.md, 10-08) names no kinds, only "Different messages will have different flow-waking effects". The ruling offers "(b) your kinds", so the split stays a proposal. Flag it as the flow's inference in the ruling text.
- Prose in code blocks (line 8 of the rule, which landed before this book): proposals 3 and 4 are prose inside ``` fences. Fix: render them as text.

## f5a6e9 «Flow, a passable vision»: flows/f5a6e9/books/10-flow-a-passable-vision.md
URL https://claude.ai/artifact/LFKcRWAPzj1FdG1Em1TbJ4. Rulings 1-6 are open; no comment record was found. All targets are `psyche-skills/skills/vision-flow.md`. The removed lines match the current lines 8-14, 22 and 46 (witnessed).
- (6) witnessed: proposal 1 says "A metaflow is of one of four kinds. Psyche, Mind and Field metaflows are voices ... An implementation metaflow is a job of its own". Two later records overtake it. d4ae97/vision/flow.md, "A flow is aspect, topic and layer" (10-08): "The first field is the aspect", "the non-topiced flows would just be the topic of core". "A fourth type: the topic flow" (10-07). Fix:
  - Removed: from "A metaflow is of one of four kinds." through "and the layer decides the model."
  - Added: "A metaflow is an aspect, a topic and a layer: Psyche, Mind or Field; a topic, core when it has none, the core the hub of its aspect; Primary to Quaternary, the layer deciding the model."
- (1) inferred: proposal 2 adds "A voice is an aspect carrying a layer, `Voice.{ Psyche Primary }`". d4ae97/vision/flow.md, "No voice: the aspects are the variants" (10-07): "There's no voice, right? The variants are all of the different voice aspects directly". His 10-07 comment (f5a6e9/vision/flow.md:1) still says "A voice is a permanent Metaflow", so the two records conflict. Raise it as a ruling; do not land either side.
- Prose in code blocks (book written 17:32, before 4d8ed32): proposals 1-5 put prose in ``` fences. Fix: render them as text.

## f5a6e9 «Metaflow kinds, the title, the word id»: flows/f5a6e9/books/9-metaflow-kinds-the-title-the-word-id.md
URL https://claude.ai/artifact/Ns3ddQa9hhWVBdY71QYA1X. Rulings 1-4 are open.
- (6) witnessed: proposal 1 gives `Kind.[ Voice.{ FlowAspect Layer } Implementation.{ Name.String Layer } ]`. Proposal 3 gives the title `Implementation.{ flowRefresh Secondary aboutBlanketBoat }`. Both are overtaken by d4ae97/vision/flow.md (10-08), "a flow is aspect, topic and layer", "It's just a struct". Fix for proposal 3:
  - Removed: "`Implementation.{ flowRefresh Secondary aboutBlanketBoat }`"
  - Added: "`{ Mind flowRefresh Secondary aboutBlanketBoat }`"
- (2) witnessed absence: proposal 4 cites "the existing rule of growing by one word on a clash". No such rule was found in `*-skills/skills` or `flows/*/vision/*ident*`. The record dea0ba/vision/identifiers.md:28 says a clash is "worth bringing up to the psyche". Fix:
  - Removed: "with the existing rule of growing by one word on a clash"
  - Added: "a clash brought to the psyche (dea0ba/vision/identifiers.md, 10-03)"
- (5): proposals 1 and 2 target ethos files outside the skill sources.
- (7): 4 lines over 52, lines 24, 26, 27 and 29, at 54-55 characters. Fix: move the comments up a line, e.g. `Voice.{ ; Psyche, Mind, Field` becomes `; Psyche, Mind, Field` above `Voice.{`.

## f5a6e9 «The metaflow record», second edition: flows/f5a6e9/books/8-the-metaflow-record-second-edition.md
URL https://claude.ai/artifact/1htsLRsyFMsoxvNV92gHxb.
- (6) witnessed: book 10, line 4, replaces proposals 2 and 3 ("are replaced by proposals 1 and 2 here"). Book 9, proposal 1 replaces the `Name` block of proposal 1. Rulings 4 and 5 remain open. Fix: withdraw proposals 1-3.
- (5): proposal 1 targets `flow/crates/flow-nexus/ethos/memory.ethos`.
- (7): line 23 is 53 characters (`Asleep ; a request wakes it`). Fix: change the comment to `; woken by a request`.

## f5a6e9 «Compensations for the machine»: flows/f5a6e9/books/8-compensations-for-the-machine.md
URL https://claude.ai/artifact/ULK22PXHWUL7ugdY1cdBLu. Rulings 1-5 are open.
- (6) witnessed: proposal 1 anchors on `compensation-orders.md` "after line 8". 209ae90 (10-08) rewrote that file, so line 8 is now "Deploy means the intended system and user environment now." Fix:
  - Removed: "after line 8"
  - Added: "after line 11 ("...name the skill and rule in the result.")"

## f5a6e9 «The ideal of machine intelligence»: flows/f5a6e9/books/7-the-ideal-of-machine-intelligence.md
URL https://claude.ai/artifact/CQaBDhLttu5cZ9fasDMwzh.
- (4) witnessed: the whole book is an essay that ends in questions. It has no target file and no removed or added lines.
- (6) witnessed: «Compensations for the machine» (ULK22P) turned its section 4 into proposals. Fix: withdraw this book.
- (3) witnessed: "as you said of locks" (section 4). Fix: remove the phrase.

## f5a6e9 «The metaflow record» (first): flows/f5a6e9/books/6-the-metaflow-record.md
URL https://claude.ai/artifact/7D9pXB7zT5t6arrYVP13Kv.
- (6) witnessed: the second edition (1htsLR) supersedes it. Fix: withdraw.
- (7): lines 16 and 17 are 53 and 55 characters.

## f5a6e9 «Stored type and datom form»: books/4-... (first) and books/5-... (reshaped in place, per log line 22)
URL https://claude.ai/artifact/6cgk7UGUTyK9gCFULNtfLC. Rulings 1-5 are open; no comment record was found.
- (5) witnessed: it targets `Vision/datom.md`, `Vision/ethos.md` and `Vision/flowNexus.md`. The rule in force at publication already said "never a file under Vision/". Fix:
  - Removed: "Proposal 1: Vision/datom.md"
  - Added: "Proposal 1: psyche-skills/skills/vision-datom.md, after line N"
  - Re-target the other proposals the same way.
- (3) witnessed: book 4 opens its sections with his quoted words ("There's a conversion that happens"). Fix: cite them as "d4ae97/vision/datom.md, 10-07" instead.

## f5a6e9 «Flow and the metaflow»: books/2-... (first) and books/3-... (reshaped in place, log line 20)
URL https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW. All six rulings were answered against the book by his nine comments (f5a6e9/vision/flow.md, ethos.md and books.md, 10-07). Examples: "Again you're centering this around Flow and not Metaflow" and "options ... are really a last resort". Book 2 also quotes his words as section headings ("It's more like 20% to 40%").
- (6) witnessed: superseded by 8-second edition and by book 10. Fix: withdraw both sources.

## f5a6e9 «Context modules»: flows/f5a6e9/books/1-context-modules.md
URL https://claude.ai/artifact/LMehrJfPcSnz5vfNifcF4f. Rulings 1-8 are open.
- (1/6) witnessed: rulings 1 and 8 declare the module types "in Curriculum's Library" and have curriculum-deploy register them. 8475a9/vision/datom.md (10-05): "with the new vision we wouldn't involve this curriculum repo. We would just directly invoke the particular repositories like mind, psyche, and field." Fix for ruling 1:
  - Removed: "declared once in Curriculum's Library and imported by Flow"
  - Added: "declared once in Flow's Library; each skill repository is read directly"
- (3) witnessed: section 0 quotes him: "the whole context modules concept has been completely omitted". Fix: cite "d4ae97/vision/contextModules.md, 10-07" instead.
- (5): `Intent/startupPrompt.md` and Curriculum paths.

## e5a0bc «Flow and Message», second edition: flows/e5a0bc/books/8-flow-and-message-second-edition.md (first edition books/1-..., UahATk, superseded per log line 64)
URL https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5. Every ruling is answered against the book by his comments on this artifact (d4ae97/vision/flow.md, 10-07) and by f5a6e9 comment 9 (witnessed):
- R1 `Flow.{ FlowId Metaflow }`: "A flow could exist and not be a metaflow so this structure is wrong."
- R3 "a metaflow's current flow its Running one": "How do I know which flow a metaflow is? ... missing the mark".
- R4 "A letter is from a metaflow to a metaflow": "The abstractions that are sent in flows are not letters."
- R5 "(b) half the model's window": "It's more like 20% to 40%."
- (6) witnessed: superseded by f5a6e9 book 10 (proposals 1, 3 and 5). Fix: withdraw both editions.
- (4/5) witnessed: sections 1-7 are design narrative with no target file.
- (7): book 1 has 46 lines over 52 (max 118). Book 8 has none.

## e5a0bc «The code», second edition: flows/e5a0bc/books/6-the-code-second-edition.md (first edition books/2-..., WKNo47, 58 lines over 52, max 95)
URL https://claude.ai/artifact/YaukDkgd5hMCwr55QH8K4m. Rulings 1-3 are open.
- (1) witnessed: ruling 1, the book flow's paragraph, says "A code line is at most 38 characters". The rule, line 7, says "at most 52 characters". Fix:
  - Removed: "A code line is at most 38 characters"
  - Added: "A code line is at most 52 characters"
- (5) witnessed: `subagents/book.md` is in the primary repository, not a skill source.
- (6) witnessed: `Curriculum/skills/operation-flashbook.md` is now `mind-skills/skills/operation-flashbook.md`. Its lines 10 and 30 still match "Now". Fix: rename the target.
- (1) witnessed: the section 7 row "`Flow.{ FlowId Metaflow }`" is contradicted, as in R1 above. Fix: drop the row.
- (4): sections 1-6 are a code walkthrough.

## e5a0bc «Vertical ethos, the skill line»: flows/e5a0bc/books/7-vertical-ethos-the-skill-line.md
URL https://claude.ai/artifact/Q3V7kZ26DH5VdpvD4JHJy8. Ruling 1 is open. The current line is unchanged at psyche-skills/skills/vision-ethos.md:445 (witnessed).
- (6) witnessed: "indented two" is overtaken by f5a6e9/vision/ethos.md (10-07, comment 2): "maybe we can try three". Fix:
  - Removed: "indented two"
  - Added: "indented three"
  - Re-indent the example by 3.
- (6) witnessed: the target moved. Fix:
  - Removed: "`Curriculum/skills/vision-ethos.md`"
  - Added: "`psyche-skills/skills/vision-ethos.md`, lines 445 and the comment line"
- (1) inferred: the example uses `Subject`. The later kinds are aspect/topic/layer (d4ae97, 10-08). Fix: use `Topic.{ ... }` in the example.

## e5a0bc «Ethos: inline, layout, expansion»: flows/e5a0bc/books/5-ethos-inline-layout-expansion.md
URL https://claude.ai/artifact/41VVDCvTkh742a7dXEznCk. Rulings 1-9 are open. It carries «Datom expansion» rulings 2-7 as 4-9 (log line 46).
- (4/5) witnessed: the targets are `src/core.rs`, `src/generation.rs` and `src/rendering.rs` plus algorithms in prose. Fix: one proposal to `psyche-skills/skills/vision-ethos.md` per rule:
  - Removed: none.
  - Added: "A type used once is declared where it is used, unless that reaches past the third level; a type used twice is declared once, named."
- (7): 4 lines over 52 (max 62).

## e5a0bc «One word for skills and subagents»: flows/e5a0bc/books/4-one-word.md
URL https://claude.ai/artifact/45g4ZpKN6AZhpQdWyx71cm. Rulings 1-2 are open; e5a0bc/vision/capability.md records the ask and no ruling.
- (3) witnessed: "your first word", "your second word", "you ruled once". Fix: cite "e5a0bc/vision/capability.md" (the record carries no date).
- (6) witnessed: the target is now `mind-skills/skills/knowledge-vocabulary.md`.
- (7): 5 lines over 52 (max 96).

## e5a0bc «Books distil»: flows/e5a0bc/books/3-books-distil.md
URL https://claude.ai/artifact/K1VN9jruW4r2S9isdYH4J3.
- (1) witnessed: the proposed line "ends in what it proposes: a skill line, a Vision statement, or a ruling" contradicts the rule's line 14: "Every distillation is written into a skill". Fix:
  - Removed: "a skill line, a Vision statement, or a ruling with its choices"
  - Added: "a skill line with its ruling"
- (6) witnessed: the substance landed in compensation-book-distillation lines 6 and 10 (209ae90). The targets moved to mind-skills/skills/operation-book.md:8 and operation-psyche-interraction.md:91, and line 91 is still unchanged. Fix: withdraw proposal 1. Re-target proposal 2.

## b27767 «Flow today»: flows/b27767/books/1-flow-today.md
URL https://claude.ai/artifact/RR8R8MrHrdteLDnnPBWNMu. Rulings 1-5 are open (log line 14, "Awaiting his rulings 1–5").
- (1) witnessed: `Flow.{ FlowId Metaflow }` with "Every flow continues one metaflow" contradicts his Tpf6nJ comment of 10-07, "A flow could exist and not be a metaflow".
- (6) witnessed: ruling 2(b) "50" is overtaken by "It's more like 20% to 40%" (d4ae97/vision/flow.md, 10-07). Fix:
  - Removed: "(b) 50, tuned after the first refresh."
  - Added: "(b) between 20 and 40 percent, as d4ae97/vision/flow.md (10-07)."
- (6) witnessed: ruling 4's title uses hex ids. d4ae97/vision/flow.md (10-07) says "I'd rather see the word-based one".
- (1) witnessed: `Rank.[ Primary` opens elements on the declaring line. e5a0bc/vision/ethos.md (10-06): new-line style "should be favored over starting indentation on the same line". Indentation is 2, not 3.
- (4/5): a survey with no skill target (sections 1-5 are design, "Proposal: this cut").

## f768df «Flow spawning»: flows/f768df/books/flow-spawning.md
URL https://claude.ai/artifact/U8SS1JBXbHgf7hcnoLp81G, recorded in 8475a9/log.md:111 and not in f768df's log. His comments are in 8475a9/vision/flow.md:58-82 and d4ae97/vision/ethos.md:5 (10-06).
- (6) witnessed: `Role.[ Voice Job ]`/`Originator.[ ... Job.FlowId ]` drew "Don't double-wrap types" and "I still don't see the meta flow". Superseded by «Flow and Message». Fix: withdraw.
- (4/5): code excerpts from `crates/flow-nexus/src/*.rs`; no skill target.
- (7): 12 lines over 52 (max 117), in ~~~ fences.

## 8475a9 «A voice's name», second edition: books/5-voice-name-v2.md (first edition books/4-..., 9z1HpL, Seat withdrawn per log line 71)
URL https://claude.ai/artifact/5riAb1PyPvsGEExk4V4bWa.
- Ruling 4 is answered by his order (8475a9/log.md, knowledge-layer-models).
- (6) witnessed: ruling 3's "twelve seats" no longer appears in any `*-skills/skills` file (grep), so ruling 3 is moot.
- (6) witnessed: ruling 1's options both carry the hex id and Voice. Overtaken by the word id and no-model title (d4ae97/vision/flow.md, 10-07) and the aspect/topic/layer struct (10-08). Fix: withdraw.
- (3) witnessed: each comment is quoted whole as a bold heading.
- (6): the target `Curriculum/skills/main-flow.md` is now mind-skills/skills/operation-main-flow.md:29.
- (7): book 5 has 14 lines over 52 (max 133). Book 4 has 6 (max 101).

## 8475a9 «Datom expansion», second edition: books/3-expansion-v2.md (first edition books/2-..., KZsdD7)
URL https://claude.ai/artifact/3HYQBstRvJx7YTS64SumLg.
- (6) witnessed: rulings 2-7 were carried into e5a0bc book 5 as rulings 4-9 (e5a0bc/log.md:46). Fix: withdraw.
- (3) witnessed: "Each is quoted, then answered"; nine quoted comments.
- (2) witnessed: "Your notion: 'Using paths is very setup-dependent...'" is used as the ground for layers 3 and 6. Fix: drop that paragraph; a notion is not ruled.
- (7): 43 lines over 52 (max 107). The first edition has 27 (max 104).

## 8475a9 «What sticks out»: flows/8475a9/books/1-salience.md
URL https://claude.ai/artifact/KLnwd2FDtd9rfp9miqzQSL.
- (4) witnessed: a status and priority survey ("What is tackled first", "The meta harness, as it stands") with no file proposals. Fix: withdraw.
- (7): 3 lines over 52 (max 84).

## 91ea9f «Skill catch-up wave»: flows/91ea9f/books/skill-catch-up-wave/source.md
URL https://claude.ai/artifact/3tjcr5uX5k1yLJrJCksfoJ. He approved items 1, 2, 4, 5, 6, 9, 10, 13 and 14 (41fa34/vision/skill-catch-up-wave-approved.md, 10-02). That record's own note classes it as a working instruction, not vision.
- (6) witnessed: items 1, 2, 4, 5 and 6 are present in mind-skills (operation-psyche-interraction.md:71 and 89, operation-design.md:9, operation-prompt-crafting.md:8) and in field-skills compensation-behavior.md. Items 3, 7, 8, 11, 12 and 15-18 are unanswered.
- (3) witnessed: 44 quotation lines; every item opens with his quote. Fix: cite "e51411, 2026-09-24" in place of each quote.
- (5) witnessed: the targets are short names ("psyche-interraction", "design"), not authored source paths.

## 91ea9f «Kinds and parameters, the deep dive»: flows/91ea9f/books/kinds-and-parameters-deep-dive/source.md
URL https://claude.ai/artifact/U3x2EkXN8YL9oDTGieBDcX.
- (1) witnessed: "The voice «Mind Astra» bears Launchable" names a voice by its model. psyche-skills/skills/vision-flow.md:22: "A voice is an aspect carrying a rank ... The model behind a voice is configuration". Fix:
  - Removed: "The voice «Mind Astra»"
  - Added: "The voice `Mind.Primary`"
- (6) witnessed: ruling 1 is already in vision-ethos.md:63, "a concrete type in an input is a kind not yet named" (primary ef712f3, 10-02 16:26). Ruling 4's hanging layout is overtaken by e5a0bc/vision/ethos.md (10-06, new-line style favoured).
- (4): a tutorial. (7): 8 lines over 52 (max 75).

## 91ea9f «Ethos in three layers, redone»: flows/91ea9f/books/ethos-three-layers/source.md
URL https://claude.ai/artifact/YRFL5EyVzx7GUFPVSaZ7vq.
- (6) witnessed: 39 closing delimiters sit on their own lines. 91ea9f/vision/ethos.md:74 (10-02): "I don't want the closing delimiter to create a whole new line". Ruling 6 landed as vision-ethos.md:63 (ef712f3). `Option<Binding>` is overtaken by "options ... a last resort" (f5a6e9/vision/flow.md, 10-07). Fix: withdraw.

## 91ea9f «Flow in ethos»: flows/91ea9f/books/flow-in-ethos/source.md
URL https://claude.ai/artifact/EHdSy5fb4bZ3gDSNaSgNkN.
- (6) witnessed: answered by his comments (91ea9f/vision/ethos.md:36-72) and superseded by «Ethos in three layers, redone». It still asks "Voice, Office, or another word for the seat?" (line 122), against "There's no seat" (d4ae97/vision/flow.md, 10-05). Fix: withdraw.
- (7): 21 lines over 52 (max 123).

## 91ea9f «The Capsule and the Semi-Sandbox»: flows/91ea9f/books/encapsulation-semi-sandbox/source.md
URL https://claude.ai/artifact/VhgcBp3G4u5Hiaj8bugmGm.
- (6) witnessed: the name and credentials route were ruled (91ea9f/vision/encapsulation.md: "It is called Capsule", "route (a) now, (b) later: approved") and landed as vision-flow.md:14 (primary 102383f, 10-02 17:03). Only "where did the harness discussion happen" is open.
- (3) witnessed: section 1 is built from five quotes of his. "seat" (line 19) is overtaken by "There's no seat" (10-05).

Nothing to flag: none. Every book has at least one finding.

Observed outside the books (not a book finding): psyche-skills/skills/vision-ethos.md:445 ("opens on its line and its elements hang beneath the first") and vision-nexus.md:153 (`FlowId.Integer`) sit against e5a0bc/vision/ethos.md (10-06) and edf227/vision/identifiers.md (10-03, "it's not an integer, it's a hash"). The latter record also says "maybe an integer with certain kinds of traits", so FlowId.Integer was not flagged in the books.

---
## Part 7

# Part 7: books of edf227, f1c841, 9fb0ad against the psyche record

Scope read: 33 books (every .md under the three books/ dirs, all mtime 2026-10-03). Comment reports: no flows/*/reports/*comments*.md names or belongs to these three flows (grep over all such files: none). Line lengths measured by a script over fenced blocks. Skill targets: grep for `(psyche|mind|field)-skills/skills/` in all 33 books returns nothing.

Findings that hold for every book, witnessed by that grep and by reading each file: (4) none is built of file-line proposals; each is a Presentation with prose sections and numbered choices; (5) none names a target under psyche-skills/skills, mind-skills/skills or field-skills/skills. The per-book sections below give only what is specific. Where a book holds a real skill change, the replacement is given as a proposal; everything else in it is status and is to be removed, not rewritten.

Artifact URLs: edf227/log.md records none; edf227/reports/open-books.md records them (mapping of the three «Flow» and three «Deployment» editions to URLs is by order and description there: inferred). f1c841 and 9fb0ad URLs are from their log.md.

## edf227 «Flow», «Flow» 2, «Flow» 3 — books/flow.md, flow-2.md, flow-3.md
URLs: 59bsmNhMFfZaAXa5g1YT6k, DxdmZMZcchyM9t3fiB6nCt, YYpbiHKvMTr9mWxc9pNjHh. Rulings 1–2 open in each; flow-3 supersedes the others.
- (6) `Voice.[ Psyche.Layer Mind.Layer Field.Layer ]` (all three) is overtaken by the living's typed comment of 2026-10-03T19:13Z on «The anatomy», `Voice.{ Aspect.[…] Layer.[…] }` (flows/bad807/vision/ethos.md). Witnessed.
- (1) flow/flow-2 "The model behind a layer is configuration in a knowledge skill" against vision-flow.md:22 "The model behind a voice is configuration, declared once in Flow and changed only over its meta wire". Witnessed.
- (1) "Layer … Quaternary" against vision-flow.md:22 "Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices". The book follows the living (flows/5578cc/vision/layers.md, typed 2026-10-03T15:39, "let's make it four layers"); the distilled line is the stale side. Proposal for the book, target psyche-skills/skills/vision-flow.md:22:
  - removed: `Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices.`
  - added: `Psyche, Mind, Field by Primary, Secondary, Tertiary, Quaternary, twelve voices.`
- (7) flow.md:37 (64 chars), flow-2.md:42 (68). Fix: break `[ Result<Self WordParseError> ] } ] } ]` after `Result<Self` onto an aligned line.

## edf227 «A flow and its role» — books/a-flow-and-its-role.md
URL HCDrXAUANJGjTHoYSCoC9s. Rulings 1–2 open; overtaken by «The anatomy» editions.
- (3) lines 7–8 quote his words back (flows/edf227/vision/flowRole.md). Replace with: `Source: flows/edf227/vision/flowRole.md, 2026-10-03.`
- (6) `Implementer` overtaken by his comment 2026-10-03 18:53 "living interaction, implementation, and vision audit. I think that I prefer the latest" (same file). Removed `Implementer`, added `Implementation`. Voice overtaken as above. Witnessed.

## edf227 «Not repeating what was found wrong» — books/not-repeating-what-was-found-wrong.md
URL Y2f3Lga2zhucYvoi2RH5tw. Rulings 1–8 open on the page, but overtaken.
- (6) Landed as Curriculum 9f5935d "curriculum: keep corrections in the flow log" (2026-10-03 13:28 -0600); now field-skills/skills/compensation-behavior.md:26 and mind-skills/skills/operation-main-flow.md:51 ("…it lives in the flow log alone"). Witnessed. Questions 7–8 (which chronology) answered by that line. Withdraw the book.
- (3) lines 6–9 quote him. (5) "the behavior skill" names no path.

## edf227 «Flow, as now designed» — books/flow-as-now-designed.md
URL 5PDkzgN8vd1ofuYk5NQizn. Rulings 1–8 open.
- (3) three quotes, lines 9–10, 16–17, 28–29.
- (1) "the model behind a layer is configuration in a knowledge skill" vs vision-flow.md:22 (quoted above); "twelve in all" vs "nine voices". Witnessed.
- Its one real proposal (lines 31–32) is still unlanded: vision-flow.md:24 still reads "Sol speaks to Opus, not to Fable; Fable is spoken to least. Design is Astra's, not Sol's." Rewrite as a proposal, target psyche-skills/skills/vision-flow.md:24, ruling grounded in flows/9fb0ad/vision/speech.md ("guidance, not a hard rule"):
  - removed: `Sol speaks to Opus, not to Fable; Fable is spoken to least. Design is Astra's, not Sol's.`
  - added: `This is guidance: each flow weighs whether a thing is worth the higher flow's attention; the Primary layer is spoken to least.`
  Whether to drop the model-named sentence entirely is his ruling (inferred; vision-model-roles.md still names models).
- Intent wording (lines 41–42): no line "deterministic" exists in any psyche-skills/skills file (grep). Proposal target: psyche-skills/skills/intent-models.md is a guess (inferred); the book must name the file.

## edf227 «Where things stand» — books/where-things-stand.md
URL 1EwwfZ6hh6PmGKB5hmQq8f. "Respond by comment"; no numbered rulings.
- (4) whole book is status ("State", "Books out", "Opus and Sol"). (6) its deployment state (lines 39–41) is overtaken by «Deployed» the same day. Withdraw; no replacement.

## edf227 «Ethos in the books» — books/ethos-in-the-books.md
URL HHEJEdGExAadXByhbqt5EG. Rulings 1–3 open.
- (4) §1 "What happened" is narrative. (3) quotes his comment line 5.
- (6) §3 Voice block overtaken (bad807/vision/ethos.md, 19:13Z). Ruling 3 ("vision-ethos example still names three ranks") is moot: grep of vision-ethos.md for Psyche/Primary/Tertiary finds no such example now. Witnessed.
- The proposed line (line 11) is not in vision-ethos.md (grep "fragment|whole root": none). Rewrite as: target psyche-skills/skills/vision-ethos.md, after line 445; removed: nothing; added: `Ethos shown anywhere is a whole root with its sections; a fragment is not ethos.`
- (7) line 53, 68 chars (same Result line as «Flow»).

## edf227 «Context modules» — books/context-modules.md
URL 68QLX9g6Z5au344RwNTepk. Rulings 1–2 open; overtaken.
- (6) `Kind.[…]` overtaken by his comment 2026-10-03T19:05Z "I don't like `kind` because it collides" (flows/edf227/vision/contextModules.md); later editions use `ModuleType`. Witnessed. (3) two STT quotes, lines 7–8, 43–44.

## edf227 «The anatomy» 1, 2, 3 — books/the-anatomy.md, -2.md, -3.md
URLs K9wB6MQ9zT2Zak7UTGUPs4, GdmxUFYfQeUTU66rwnJ75E, PCiikHCQDoXP7FMih66Yjm. Rulings 1–2 open in each; 3 supersedes 1 and 2.
- (6) editions 1–2 `FlowId.Integer` overtaken by his comment 2026-10-03T19:26Z on this book "First of all it's not an integer, it's a hash" (flows/dea0ba/vision/identifiers.md); edition 1's Voice overtaken (19:13Z). Witnessed.
- (1) edition 3 `FlowId.String ; … session hash` vs psyche-skills/skills/vision-nexus.md:154 `[ FlowId.Integer`. The distilled line is the stale side. Proposal, target vision-nexus.md:154: removed `[ FlowId.Integer`, added the type he rules for a hash (String is the book's choice, not his; open ruling, inferred).
- (7) edition 3: 38 code lines over 52 (max 86) from trailing comments. Replacement form: each comment on its own line above the line it explains, e.g. removed `Library                              ; a Library root: types every component shares`, added `; a Library root: types every component shares` then `Library`. Whether ethos accepts a comment-only line is unverified (vision-ethos.md:447 says only "a comment runs from ; to the end of the line").
- (6) the config record's model `claude-fable-5-1` and Psyche Primary: not checked against knowledge-layer-models (not flagged).

## edf227 «Deployed» — books/deployed.md
URL N89vDYRZXTMMbWrZwbE1nH. Rulings 1 Noted / 2 Comment; nothing to rule.
- (4) pure status. Withdraw; status goes outside a book.

## edf227 «The deployment, in four parts» 1, 2, 3 — books/the-deployment-in-four-parts*.md
URLs EQABGmpRZWyMg1N7FGK7kh, AqfVpyYNxAmDSAJu26stD6, 1DHQ8x3zkwxQf2rJfMUyrM. "Noted/Comment" only; 3 supersedes.
- (4) all status. Editions 1–2 draw in Mermaid against Curriculum 487b69b "book drawings are inline SVG, never Mermaid" (2026-10-03 14:35), now mind-skills/skills/operation-book.md:10 "A drawing in a book is hand-written inline SVG". Witnessed.
- (7) editions 1–2: 11 lines over 52 each (Mermaid). Edition 3: none.
- Ethos block (all three) opens `DictionaryVersion.{` with nothing on the line, against vision-ethos.md:445 "a structure with more than one element opens on its line and its elements hang beneath the first, aligned". Witnessed. Replacement: `DictionaryVersion.{ DictionaryName.String` / aligned `Revision.Integer }` as in «The word id, as a kind».

## edf227 «Vision, routed by topic» — books/vision-routed-by-topic.md
URL VBd77gLZHSkReUfvxXDm98. Rulings 1–3 open.
- (3) line 3 paraphrases him back ("What you said: …"); replace with `Source: flows/edf227/vision/visionNotification.md, 2026-10-03.` (record exists; date from file, inferred).
- (7) 23 code lines over 52 (max 86), trailing comments; same fix as «The anatomy» 3.
- (4)/(5) a Flow design, no skill target. Built on a vision record, not a notion (witnessed by grep).

## edf227 «The flow id as a hash» — books/the-flow-id-as-a-hash.md
URL YU5G17CkrT6eX4CcxUKosw. Rulings 1–4 open; he put it on the back burner (19:26Z, "let go of the word ID for now").
- (1)/(6) "The id is a number … not text" and `FlowId.{ Integer }` against his 19:26Z "it's not an integer, it's a hash". Inferred conflict: the book reads hash as fixed-width integer; ask, do not assume.
- (7) 10 lines over 52 (max 95). Drawings described in prose, not drawn (lines 9, 38).

## edf227 «The tailor-made subflows» — books/the-tailor-made-subflows.md
URL R4YwyxHvyGxGp6QnVE8WV9. Rulings 1–3 open.
- (5) targets "Curriculum's manifest" (line 89), not a skill source. (4) opens with a count narrative (line 3).
- (6) `claude-sonnet-low ; a Quaternary model` overtaken by the 2026-10-08 ruling (flows/41fa34/vision/layers.md) and mind-skills/skills/knowledge-layer-models.md:18 "Quaternary | Claude | Haiku 5.5 (model id `claude-haiku-5-5`) | Low". Removed `claude-sonnet-low }`, added `claude-haiku-5-5 }`. Witnessed.
- (7) 14 lines over 52 (max 70).

## edf227 «Curriculum: the context standard» — books/curriculum-the-context-standard.md
URL AxZysWDWcbt77wfPd9vDiA. Rulings 1–4 open.
- (6) "the name stays Curriculum" and paths `skills/vision-flow.md` (lines 54–57) are overtaken: Curriculum 73414b6 "Replace Curriculum skills with typed Nexus" (2026-10-07) and psyche-skills fef9864 "Move Psyche skill sources under skills" (2026-10-07). Witnessed by git log subjects; whether the whole design is void is inferred.
- (1) "the twelve voices" vs vision-flow.md:22 "nine voices" (see «Flow»). (7) 4 lines over 52 (line 21 is 104).

## f1c841 «The night, for your word» — books/the-night-for-your-word.md
URL TLXm45bNbrG1EpTCvYeshm. Rulings 1–8 "silence keeps"; deployments 1–5.
- (3) quotes his words in lines 3, 9, 10, 12. (4) §3–§4 are status and incidents.
- (6) deployments 2–4 approved by his STT order 06:40 (f1c841/log.md) and done per «Deployed»; ruling 1 landed in part as Curriculum b778545 "Vision and Intent become vision- and intent- skills; six skill kinds as prefixes" (2026-10-07); no notion- or question- prefix exists in psyche-skills/skills (ls). Witnessed.

## f1c841 «The audit, what is done» / «…what waits on your word» / «…what no flow did, and why»
URLs 4oy9i2JteAcoCFYXDjBDD2, V5NEr1Af2fBbgfyifMKzHn, DyN4RRpqQ17rmSPwuoJYcZ.
- (4) all three are survey and status by his order ("report on everything that's been done … Put this all in the books", f1c841/log.md 06:1x); the order makes them status by design, so the rule conflict is his to rule: books carry only proposals vs. his order to put the audit in books.
- (3) each quotes his order or comments back (done:3, 20; waits:13–14, 21–23; no-flow: none quoted, only cited).
- (6) "waits" §1 deployments: overtaken by the 06:40 order and «Deployed». (5) "no-flow" line 26 names Vision/*.md files in Primary, not skill sources.

## 9fb0ad «The deployment stopped at the first activation», «The guard fix, as built»
URLs DkieqeJsbo2MDjAkpGkPY8, 4jLEsv4pNu35wzasx9WHp9. Rulings 1–9 open on the page.
- (6) overtaken: «Deployed» (edf227) states the pinned link check was replaced by Home Manager's own; not checked against a CriomOS-home commit (inferred). (3) deployment-stopped line 3 quotes him. (4) both status.

## 9fb0ad «The commands the harnesses block» — books/commands-the-harnesses-block.md
URL 3VAZEr5an3MYbwmBhmHfUt. Rulings 1–6 open on the page.
- (6) overtaken by CriomOS-home 3535168b "deny the Claude dangerous-removal prompt with a rewrite message" (2026-10-04) and Curriculum a693fc6 trial-unblocking-commands (2026-10-04): solution 2, deny by default. Witnessed by commit subjects. (3) line 3 quotes him.

## 9fb0ad «Two meanings for Flow», «Two more meanings for Flow»
URLs 1LhLZg92hyrjXQsT3f6Yc1, KdkQNDzPBRdba6mBUUCa5S (short ids, open-books.md).
- (6) answered: flows/9fb0ad/vision/flowLifecycle.md ("when the flow isn't working then it's idle") and speech.md ("Sol cannot talk to Fable … guidance, not a hard rule"); words-vs-id answered by the 33-bit ruling 15:59Z (9fb0ad/vision/identifiers.md:31). Witnessed. (3) both are mostly his quotes.

## 9fb0ad «The word id, as a kind» — books/the-word-id-as-a-kind.md
URL W5yUFxMVsZHjMNaT5nXtQb. Rulings 1–3 open; deferred by his 19:26Z "let go of the word ID for now".
- (7) lines 17 (53), 19 (57), 20 (59), 34 (68).
- Line 17 `WrongWordCount.{ Integer Integer }` against vision-ethos.md:445 "Nothing that has a next layer sits on one line." Removed that line; added `WrongWordCount.{ Integer` / aligned `Integer }`. Witnessed. (3) line 3 quotes him.

## 9fb0ad «Allowance, monitoring, and reaching you», «Questions on the Ethos library», «The day, in one view»
URLs 3w3wBK89V25WRttVnMnUNW, 779cX7AjBNuvmBJ4ujUfC8, Wes3YnEwwaCiFpVN9M7yGj.
- (4) research options and a day summary; no file target. (3) allowance lines 7, 25; day lines 5, 14. Rulings open on allowance 1–9 and questions 1–11 (no ruling found in 9fb0ad/vision on Netdata, ntfy or ethos-core; grep). «The day» §3 is overtaken by the deployment and the 2026-10-04 hook commits above.

Books with nothing to flag beyond the shared (4)/(5): none.
