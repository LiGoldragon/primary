# References for «Flow: CLI, deployment, long term — third edition»

Unrendered. Beside the source `flows/55a2b4/books/12-flow-cli-deployment-long-term-3.md`; never passed to the builder. Authored by flow 55a2b4 (Psyche Flow Primary seat) on the order of its launcher.

## The edition

Third edition of the book whose second edition is `flows/df159a/books/12-flow-cli-deployment-long-term-2.md` (refs `…-2.refs.md`). Already landed and not shown: the vision-model-roles strikes (L52–55, L62–69) and the vision-flow L24 base sentence, psyche-context HEAD e3823d6 «vision-flow: L24 needed metaflow started running or not, approved 2026-10-14». Module lines quoted from that HEAD, read whole this session.

## His four comments of 2026-10-14 on the second edition

All in `flows/da2038/vision/flow.md`, STT, relayed by Psyche Core Secondary; mirrored in `flows/d68c82/vision/flow.md` L140–160. Read verbatim; not on the page.

- L36–42, on the L24 line: «Yeah that's good. If it doesn't have a task by default, that should be written somewhere else, I guess. … the default task is to create a proposal or a question.» — approves the base sentence (landed); grounds P4.
- L44–50, on choice 2 (L51 short-term): «This concept is not strictly short-term. What makes you think this is a short-term concept?» — grounds the L51 item below.
- L62–68, on choice 3: «… let's make sure that somewhere it's made clear that we don't start a primary without a secondary. In the short term anyway eventually, long term, … the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in so we can queue stuff). Queuing stuff is also a really important goal post …» — grounds P3: the short-term mark on the Secondary-first line and the long-term queue goal.
- L70–76, on choice 4: «I would say, with a still-young working transcript, let's have a proposal to explain what a young context is in terms of ratio and where average context size starts to degrade rapidly (around the 100,000-token point).» — grounds P1 («still-young») and P2.

## P1 — a still-young transcript is reawakened

- Base: the landed L24 sentence (his 2026-10-14 15:18 comment, second-edition refs). The inserted clause carries his «still-young working transcript» and «reawaken»; «with none, or an old one» is the machine's reading: a transcript that is not young takes the fresh-start branch his base sentence already names. Tagged on the page «Machine: the old-transcript branch.»
- Kin: `flows/d68c82/vision/flow.md` L114–128, 2026-10-14, STT: «restart that flow or start a fresh one»; `flows/6cc91b/vision/flowLifecycle.md`, 2026-09-14, STT: reawakening a concluded thread may be expensive because of cache lifetime.

## P2 — a young context

- The 100k point is his figure (L70–76 above), on the page as «about a hundred thousand tokens». The ratio is not his: he asks for one. Default «half the layer's refresh threshold» and choice 1 «a third of the model's context window» are the machine's two readings, set by the brief. The default is tagged on the page «Machine: the ratio.»; choice 1 carries only its differing words.
- Witnessed configuration, `config/context-refresh.json` (read this session): `warningWindowFraction` 0.5; Claude `warningTokens` 200000 (absolute); Codex windows gpt-6.1-sol 373000, gpt-6-astra/gpt-6-sol/gpt-6-luna 272000, threshold = floor(window × 0.5) per `tools/context-refresh-hook.mjs` `thresholdFor`. Half of these thresholds: Claude 100000; Codex 93250 and 68000. The threshold is set per harness and model in this file, not per layer; the module's «layer's threshold» (L62) is the vision. A third of a 200K window is about 66.7K, of 1M about 333K.
- Measurement witnessed (Mind, `/git/github.com/LiGoldragon/mind-context-module-size/skills/knowledge-compaction.md`, HEAD bd5fd6c), not on the page: L56 NoLiMa 2025, GPT-4o retrieval 99.3% short-context to 56.0% at 128K, 8K effective length; LongCodeBench 2025, Claude 3.5 Sonnet LongSWE 29/19/15/3% at 32K/64K/128K/256K, GPT-4o 11/6/5% at 32K/64K/128K; «These do not define a universal handover threshold.» L54: Claude Code compaction boundaries 200K (Sonnet/Opus 4.6 without extended context), about 967K for 1M models — configuration, not measured triggers. L23–26: four observed Claude compactions from 281,533–336,492 tokens to 21,803–26,396. L42: Codex automatic limit capped at 90% of the resolved window. No ~100k measured point exists there; the 100k figure stands on his words alone.
- «so only a young transcript is reawakened; an older one gives way to a fresh flow fed the metaflow's context modules»: the brief's «is refreshed, not reawakened» reworded. Refresh in L62 is the handover-and-replace at the layer threshold (200K for Claude); saying a context past 100K «is refreshed» would contradict L62, so the line scopes the 100K point to reawakening only.
- Kin: `flows/d68c82/vision/flow.md` L50–54, «A compaction request refuses a small or young flow», STT, 2026-10-13 (dated by its neighbour): young also «in time terms». A time bound is not proposed; open.

## P3 — a Primary starts after its Secondary; queuing is a long-term goal

- Short-term mark: his «In the short term anyway» (L62–68). Mark form per intent-psyche L10: «A short-term vision is named so; an unmarked vision is long-term.»
- «a launch that needs a Primary starts the Secondary first» is the machine's: his words name the order, not the launch. Tagged on the page «Machine: the second clause.»
- The queue clause is worded as his goal, not a present mechanism: «queuing is a long-term goal, for much higher output quality and efficiency: an interruption alone interrupts, and when it is done all of the queue that should go with it comes in». Ground: his «eventually, long term … the interruptions only were the interruptions and that, when they're done, all of the queue that also should go with it comes in … Queuing stuff is also a really important goal post». His reason about costly wakes (Fable) is not carried on the page.
- Earlier record, same subject: `flows/d68c82/vision/seats.md` L21–27, «every Primary has a Secondary, started first», STT, committed 2026-10-14 09:25 (233036d), unqualified. The later comment adds the short-term qualifier; the later explicit words carry the weight. Tension worth his eye: the earlier record reads as standing structure (the Secondary as secretary), the later one as a guard against costly wakes.
- Field already enforces the start order: `/git/github.com/LiGoldragon/field-context/skills/compensation-launch.md` L7–10 (HEAD 5070467): «A Primary starts only after a live Secondary for the same aspect and topic is verified; when none exists, the launcher starts that Secondary first and verifies its native binding before starting the Primary.» Not on the page.
- Both P1 and P3 rewrite L24; each pair quotes L24 as it stands at e3823d6. Landing both makes one line carrying both insertions. P3's `+ ` line shows only its own insertion; the page's File: line carries no cross-reference.

## P4 — a flow launched without a brief has the default task

- His L36–42 words; «written somewhere else» read as: not in the L24 sentence. Default home vision-flow after L34, beside «a brief of a small paragraph». Choice 2 is worded on the page as «The line lands in `intent-startup-prompt`, after its L8.», placed under P4's lines and tagged «Machine: the home.» (the brief's «choice 1» for P4, renumbered so the page's rulings carry distinct numbers): `psyche-context/skills/intent-startup-prompt.md` after L8; an intent module, entered only on his explicit word.
- The `+ ` line carries his «a proposal or a question» and nothing beyond it; a qualifier «where no proposal stands» had no ground in his words and is not on the page. Choice 2 carries only the differing placement; «an intent module» stands here: intent enters only on his explicit word, which his ruling of choice 2 would be.
- This seat's held book «Flow: the first response» (`flows/55a2b4/books/01-flow-first-response.md`, held) P1 builds on this line: its first-response sentence assumes the default task.

## The second edition's figure under L24

The second edition proposed an ASCII figure under the L24 sentence. The landing at e3823d6 carries the sentence only; the figure did not land, and his comments on the second edition name it nowhere (read: `flows/da2038/vision/flow.md`, the six 2026-10-14 records). This edition's figure is proposed for vision-flow after L24, per vision-book L8's «a figure in it is a figure proposed for a module»; the page heads it with its own File: line. The placement is the machine's, tagged on the page «Machine: the placement.» Open for his eye: whether L24 carries this figure.

## L51 — vertical communication, short-term marker: nothing lands

vision-model-roles L51 carries no short-term marker at HEAD e3823d6, and his L44–50 words reject the marker the second edition offered as choice 2. No record grounds a marker. Nothing proposed.

## Figure

One branching figure: request → Flow → running: delivered / not running: transcript → young: reawakened / old or none: «a fresh flow, modules and prompt» → the two joined into one edge «short-term: if a Primary, starts after» → its Secondary, live. The edge carries P3's Short-term mark. Width 44. Drawn from P1 and P3; proposed for vision-flow after L24.

Drawn SVG (scratchpad `gen12.py`, spliced in place of the ASCII): 7 boxes, 6 arrowheads, 12 label lines, matching the sketch's 7 boxes, 6 arrows and 12 label lines; the two lower boxes' bottoms join into one line that carries the single arrow and the single label.

## Witnessed

`node tools/book-check.mjs` → `{"checked":true,…}`; `bb tools/book-build.clj … --code tools/book-code.html` exit 0; trailing whitespace 0 on md, html and refs; the forbidden-word grep 0; every `- ` and context line unchanged from the edition read whole at e3823d6. Headless Chrome through scratchpad `wrap12-320.html` / `wrap12-375.html`, light and dark (`witness-12-v2/`): scrollWidth 305 ≤ innerWidth 320 and 360 ≤ 375 in both schemes; dark reported true under forced dark. The `## Crystallization` heading is removed; `tools/book-check.mjs` no longer requires it. Not witnessed: publication.
