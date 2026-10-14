# Lines in machine skills that the living reviewed or approved

Heads read: mind-skills c054cec, field-skills 14269e9, psyche-skills b615e96
(all fetched 2026-10-13; mind and field moved during the search, line numbers
below are at these heads). None of the lines below is in psyche-skills at b615e96.

Strength marks: **A** = record or log quotes his approval of that text;
**C** = only a commit message or a flow log claims the approval;
**B** = blanket approval ("go with my suggestions", "trust"), text not shown read;
**≠** = current text differs from what was approved.

## 1. Skill catch-up wave (approved 1,2,4,5,6,9,10,13,14; flows/41fa34/vision/skill-catch-up-wave-approved.md, 2026-10-02; Curriculum 8dbd981)

1. A · compensation-behavior:22 (item 5) → vision-flow
   "A flow works until its order is done. When it cannot proceed, or an attempt repeats a failure, it stops and says what blocks it, what would unblock it, and the decision it needs; it never reports only that it is waiting."
   Same as approved. Conflict: none found.
2. A · knowledge-codex-harness:20 (item 13) → vision-model-roles
   "A launcher passes the role's model by family name, never a version number, and `model_reasoning_effort=medium` unless the role declares otherwise."
   Same as approved. Conflicts, newest first: flows/d68c82/vision/skills.md 2026-10-13T16:57 ("This negative instruction against using model numbers ... is totally unnecessary"); vision-model-roles "One declaration sets the model everywhere"; SKILL_VARIABLES holds versioned ids.
3. A · operation-design:9 (item 4) → vision-high-level-view
   "Show the psyche the high-level view routinely, as ethos, example datom and rendered flowcharts rather than paragraphs."
   Same as approved. Conflict: none; overlaps vision-high-level-view "looked at routinely".
4. A · operation-design:11 and operation-main-flow:40 (item 2) → vision-psyche-interaction (topic; no skill at b615e96)
   "Whatever the psyche must read, rule on or approve goes whole into the living messenger as a presentation; a proposal is revised there until the psyche approves a landing. Chat is unread."
   Same as approved. Conflict: its landing in vision-psyche-interaction was reverted (psyche-skills 630f73b) after the living said, 2026-10-13, "I need to be more clear about what the third proposal is exactly" (flows/d68c82/log.md).
5. A ≠ · operation-psyche-interraction:89 (item 2, third copy) → vision-psyche-interaction
   Now: "Whatever the living must read, rule on or approve goes whole into the living messenger; the chat is not read. He answers by comment, naming choices by number; a message he has commented on is never changed."
   Approved text = item 4's. Reworded by Curriculum 927d056 (2026-10-02, "Refine living messenger presentations"; no approval recorded).
6. A · operation-feature-development:6 (item 9) → vision-committing
   "Feature work happens in the repository's one shared checkout, under an edit-coordination lock."
   Same as approved. Conflict: none; flows/dea0ba/vision/publishing.md repeats "I do not want work trees".
7. A · operation-psyche-interraction:71 (item 1) → vision-psyche-interaction
   "When the psyche designs, ask about the anatomy of the idea: what composes it, its boundaries, its inputs and outputs, what it should not do; flesh it out before building. When the psyche orders, carry it out; an order is never asked back."
   Same as approved. Conflict: none found.
8. A · operation-secrets:15 (item 14) → vision-psyche-interaction
   "A secret or pairing code never appears in chat or the living messenger; it reaches the living only through its own device flow."
   Same as approved. Conflict: none found.
9. A ≠ · operation-nix-workflow:14 (item 10) → vision-deployment
   Approved: "Run Nix builds on the configured remote builder; build locally only while it is unreachable, and never on a host the cluster data excludes from building."
   Now: "Run Nix builds and tests only on the configured remote builder."
   Changed in Curriculum beb1dd1 (2026-10-07 11:03, unnamed snapshot; flows/d4ae97/log.md says a worker of f768df edited nix-workflow that hour). Related records: flows/504461/vision/cluster-builds.md and flows/b7da5d/vision/prometheusBuildPolicy.md (2026-09-25, "Of course you can fall back to local building"); compensation-temporary:8 carries local building.
10. Gone · operation-prompt-crafting:8 (item 6), "A prompt carries its content, never references to read: the concentrated vision of the last three flows ...". Deleted today in mind-skills c054cec. Conflict that preceded it: the living rejected the same sentence in trial-succession, 2026-10-13 (flows/d68c82/log.md).
11. Item 9's second half: main-feature-integration retired; no line remains.

## 2. Stale lock (Curriculum dd14ce7, 2026-09-25, "Land stale-lock text as the living approved it")

12. C ≠ · operation-stale-lock:6 → vision-orchestrate
   Approved: "A lock whose holder is stale may be released by any flow. The holder is stale when hm-list shows its binding STALE or exited, Herdr has no live pane for it, and one hm-send to it comes back Held. Before release: Observe.Locks, and record the lock, its paths and the holder's state in a receipt; commit any uncommitted work under its paths as found, naming the holder; then release by ID and take your own lock. A live holder is messaged, never unlocked. The living: "break the locks. Nobody in particular owns Flow Source.""
   Now: Held clause gone (Curriculum restoration of 2026-09-28, note "probes wake seats"); "outside Primary" and "In Primary, leave those bytes in place and send the exact holder and path evidence to the sole standing committer for publication; do not commit them yourself." added (mind-skills aa9e6dc, 2026-10-12, a relayed order). No approval record found; only the commit subject.
   Later record: flows/8904b1/vision/skills.md 8904b1-25 (2026-09-28): a lock held by another flow → "Communicate what you're wanting that lock for".

## 3. Earlier approvals whose text still stands

13. A · compensation-behavior:6-7, 13-14, 16-18 → vision-flow (no vision-behavior exists)
   "A claim must be relayed as a claim; a thing is verified only by a witness." / "Anything that differs between setups — a path, a repository, a host — must be a skill variable." / "The account of why something was done must give what was read and what was written, in order, and then the possible causes — there is almost always more than one."
   flows/358f143a/vision/behavior.md, 2026-08-18 ("the skill-design and behavior proposal are good enough"). Conflict: none found.
14. A · operation-skill-designing:46, same approval → vision-flow
   "A line must hold beyond the document, tool, or incident that prompted it."
15. A (log) · compensation-behavior:9-11 → vision-flow
   "A synthesis carries each claim's origin, who found it, where, and whether it was witnessed, and marks the flow's own inference as the flow's."
   flows/b9f4f6/log.md (2026-09-02, "the skill edits are good."); Curriculum ae972e7.
16. A (log) · operation-psyche-interraction:85, same approval → vision-psyche-interaction
   "Assume the psyche knows their vision, not the code or agent-created terms. Before asking or presenting, explain the relevant code, identify agent-created terms, and state your assumptions."
17. A · knowledge-vocabulary:37 → vision-psyche
   "A defined term overrides competing terminology in the flow's own words."
   flows/2f6b1dc5/vision/vocabulary.md, 2026-08-24 ("good. approved."); Curriculum 40a0d87.
18. A ≠ · knowledge-vocabulary:31 → vision-psyche
   Now: "Base context: the harness-built portion of the top stratum — the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt."
   Approved 2026-08-23 as "Base prompt: ..." (flows/2f6b1dc5/vision/systemPrompt.md); his next record, 2026-08-24, "I prefer context to prompt" — a preference, the reworded line not shown approved.
19. A · operation-testing:18-23 → new vision-testing (intent-testing holds only the sandbox rule)
   "A new test is seen failing once before it is trusted." / "The expected value comes from outside the code under test; a test that computes it through the tested path confirms nothing." / "A test waits on the tested event, never on the clock." / "Tests share no mutable state — no process environment, no working directory, no order between them."
   vision-raw/testTravesties.md, 2026-08-21 ("this is good, we can land it"); Curriculum 3629e2c.
20. A (log) · operation-testing:24 → vision-testing
   "A run that may exhaust memory or time is bounded (a memory cap and a timeout) so that it cannot take the harness down with it."
   flows/1a6ca4/log.md, 2026-09-05 ("approve the testing skill line and the OOMPolicy change"); Curriculum 7eab1b7.
21. A · compensation-breaking-upgrades:6-8 → vision-deployment
   "Document how to deploy each breaking change in the repository's `UPGRADES.md`." / "Land the documentation with the breaking change." / "If deployment fails or partially fails, correct the documentation before continuing."
   flows/01a02b46/vision/zeusUpdate.md, 2026-08-23 ("great, approved. land the skill").
22. C · operation-psyche-distillation:27 and operation-psyche-interraction:14, 32 → vision-distillation (27), vision-psyche (14, 32)
   "A statement about code carries the code: a distilled statement on a syntax, a type, a kind, or a wire form shows example code, because machines think in code and the next machine to read it must understand." / "Thinking out loud, bouncing ideas, and any words the psyche frames as exploration rather than pronouncement are Notion, the same as brainstorm." / "What the psyche says to help the flow understand vision is context, not vision: it is kept beside the quoted words, never logged or distilled as a statement of its own."
   Curriculum ae69122 (2026-09-09, "three psyche-handling lines approved by the living"); flows/564f55/log.md line 26.
23. C · knowledge-codex-harness:15-18 → vision-model-roles
   "A Codex session's model and reasoning effort come from `~/.codex/config.toml` at launch and change without notice. A launcher that must pin a model passes `-m <model> -c model_reasoning_effort=<effort>` rather than inheriting them."
   flows/564f55/log.md 2026-09-10 ("yes on the codex harness skill"). Conflict: vision-model-roles, a launcher never writes a model name by hand.
24. C · operation-psyche-distillation:43 → vision-distillation
   "What the living says fresh while a distillation is being composed is logged as a raw record as it is spoken, like any other psyche, and the distillation draws on it like any other record."
   Curriculum 9c5af51 (2026-09-03, "Land approved psyche-distillation line"); no record found. Not in psyche-skills.
25. A ≠ · operation-design:13-16 and operation-psyche-distillation:40-41 → vision-distillation
   design 13-16 now: "Every second or third turn, check whether a subject touched heavily in this flow has raw vision accumulating across flows. When it does, dispatch a subflow to gather all records on that subject, then compose a distillation presentation for the psyche's approval."
   distillation 40-41: "Distillation is proposed on encounter, dispatched proactively by the flow working a subject, or done in dedicated passes."
   flows/04db2fd2/vision/rollingDistillation.md 2026-08-27 ("design and psyche-distillation skill edit is good."). Line 16 was reworded in 8dbd981 (was "a distillation proposal in the main flow for the psyche's approval before any Vision/ change"), outside the catch-up items.
26. A (log) · operation-psyche-interraction:8, 16, 18, 19, 20, 24, 34 → vision-psyche
   8 "Log psyche in the flow's own `vision/<topic>.md`: what the psyche envisions, in the psyche's words. Never a ruling or an instruction." · 16 "Log psyche as it is spoken." · 18 "When the psyche speaks vision, log it before acting on it." · 19 "Psyche not logged in the moment is psyche at risk of drift." · 20 "Do not batch — each statement is one write." · 24 opens "Record the psyche's vision, whatever it designs — a machine, a" (paragraph 24-31; only "vision"/"it designs" changed) · 34 "A ruling — the psyche deciding what the flow does — is an instruction, not psyche."
   flows/674a4dab/log.md 2026-08-29 ("you only log psyche not rulings"); Curriculum 1d44d7f. Tension: vision-distillation "a correction of an agent's conduct can be vision"; flows/d68c82/vision/skills.md 2026-10-13 "if I approve it, its value has gone up to psyche".
27. C · operation-psyche-interraction:17 → vision-psyche
   "Order each topic log oldest first, with the most recent entry last."  Curriculum f52dc24 (2026-08-11, "apply approved ... doctrine"); no record found.
28. C ≠ · operation-main-flow:17 → vision-flow
   Now: "Locating is subflow work whatever tool would do it: listing a directory, searching git or jj history, grepping an index. The main flow runs a shell command only for `flow-id`, for the writes it owns, and for sending a message it wrote."
   Curriculum 9fe5599 (2026-09-03, "land approved clarification"); the closing "and for sending a message it wrote" was added later. No record found.
29. A ≠ · operation-nix-workflow:16-17 → vision-deployment
   16 "Test with binaries and scripts packaged by Nix." · 17 "A Rust runtime has its own Rust-only repository, holding only what compiling its executable or library needs; mutable data and content live in separate data inputs or repositories, so data changes do not invalidate Rust compilation. Do not modify what is not Rust in a Rust executable repository."
   flows/8904b1/vision/skills.md 8904b1-31, 2026-09-28 comment ("Yeah this is important. Also we don't want to be modifying things that are not Rust ..."); Curriculum 61e0b4b. The sentences of 17 that render his comment were written afterwards, not shown to him.
30. C · operation-nix-workflow:9-10 → vision-deployment
   "Keep `flake.nix` readable as an index." / "Keep substantial check and build implementations and long shell programs out of `flake.nix`."  Curriculum 0382ef9 (2026-07-22, "apply approved doctrine rulings"); no record found.

## 4. Whole bodies landed as approved (verbatim not repeated here; at the heads above)

31. C (log) · knowledge-context-strata:6-31; knowledge-claude-harness:6-16, 18-23, 54-63; knowledge-codex-harness:6-13, 22-29, 59-65 → topic harness (vision-harness was reverted today, 630f73b)
   flows/7b4d4c/log.md, 2026-09-05: "The living approved the four skill drafts as they stand"; Curriculum d9dfeeb; landing subflow found "no deviation from the approved wording". Context-strata's earlier form was approved 2026-08-19 and 2026-08-26 (flows/7c3f0c1d/vision/gradientsOfAuthority.md, flows/4ddc321d/vision/contextStrata.md).
32. B · knowledge-datom:6 8 17 19 21 25 32-34 39 53 66 72 80 81 86 90 95 98 99 102; knowledge-protos:6 10 18-20 22-24 31 35 39 43 57-60 62-67 69-71 73 78 86; operation-lojix: 35 lines first landed by Curriculum 2ef2b53 → vision-datom, vision-protos, topic lojix
   2ef2b53 (2026-09-12) "Apply the approved skill proposals from flow f6db8d"; the record is flows/f6db8d/log.md:97 ("go with my suggestions"), and the commit says the text was "corrected against released ... where the released code differs". Restored 2026-09-28 as "the approved dialect bodies" (Curriculum b7a74f9). Lines already duplicated in vision-datom/vision-protos are excluded.

## 5. Unknowns

- operation-psyche-grasp:6-7 and the levels. No record shows him reviewing this text. It came from a Primary commit, 6973354ca (2026-08-08). The only nearby trace is bead primary-hqu.26.1, which cites a psyche approval on 2026-08-07 marking a site "slightly-reviewed". On 2026-10-13 he said "We've reviewed that together with the living" (flows/d68c82/log.md, STT) and "We can review the first concept" (flows/d68c82/vision/skills.md). Both are ambiguous. Today's c054cec kept the module.
- operation-main-flow:12-13 (mind-skills 2d86e36, "Core living 2026-10-12"). The log line "Living: landed the seat-prompt amendment" (flows/d68c82/log.md:363) does not show whether he read this text.
- No current line was found from the 5c8be3ca flow-artifacts skill (approved 2026-08-22), the 1030529c awareness lines, or the 8904b1-25 lock sentence.
- The method finds a line only if it matches exactly, so a wrapped paragraph whose wrapping changed after approval can be missed. Commits after 2026-10-07 were read only in mind-skills and field-skills.
