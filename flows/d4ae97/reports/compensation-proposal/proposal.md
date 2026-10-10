# Compensation proposal: his clearest repeated frustrations

Opus subflow of Psyche Opus d4ae97, 2026-10-08.

Sources read:
- `flows/*/vision` and `flows/*/notion` from 2026-10-05 to 2026-10-08;
- his transcript words from 2026-10-06 to 2026-10-08;
- `flows/d4ae97/reports/recurring-insistences.md`.

Checked against:
- `field-skills/skills/compensation-*.md` at e52a730;
- the standing set in `Curriculum/roles.datom`: spirit, book-distillation, truth, orders, prose, understanding, launch, design, default-effort and messenger-clj.

`F/` is `/git/github.com/LiGoldragon/field-skills/skills/`. `t:<id>:<n>` is a transcript: the session prefix, then the JSONL line. Flow paths are relative to `/home/li/primary/flows/`.

Entries 1 to 6 add something the deployed compensation does not carry, or replace a line that fails. Entries 7 to 10 soften or remove deployed lines.

## 1. His words do not reach skills or code

`F/compensation-orders.md` after line 11. Add:

> What the living says the system should be goes, in the same turn, into a proposed line for the skill it concerns, or to the flow that holds that skill or code. A log entry alone does not carry it.

Evidence:
- "The code hasn't been changed and the skills haven't been changed. My vision is getting lost" (`t:d4ae97d4:5448`, 2026-10-08)
- "I probably said it a hundred times" (that visions are now skills) (`t:d4ae97d4:3574`, 2026-10-07)
- "My request was not appropriately inserted into the right skill" (`t:d4ae97d4:3057`, `f768df/vision/skills.md:6`, 2026-10-07)
- "a lot ... that I've said ... hasn't actually been properly put into skills" (`d4ae97/vision/skills.md:13`, 2026-10-07)

Why: lines 10-11 load only for a "standing order". A ruling on how the system should be is logged as vision and stops there.

## 2. Designs miss what he named central

`F/compensation-design.md` after line 12. Add:

> A design starts from the living's records on its topic and leads with what he named central; what it leaves out of them, it names.

Evidence:
- metaflow: "part of my vision that's being missed" (`f768df/vision/flow.md:6`, 2026-10-06)
- metaflow: "I still don't see the meta flow" (`d4ae97/vision/ethos.md:7`, 2026-10-06)
- metaflow: "Again you're making Flow the only abstraction ... which is not my vision" (`f5a6e9/vision/flow.md:39`, 2026-10-07)
- metaflow: "Again you're centering this around Flow and not Metaflow" (`f5a6e9/vision/flow.md:47`, 2026-10-07)
- context modules: "the machine is almost completely missing my design" (`d4ae97/vision/contextModules.md:6`, 2026-10-07)

`psyche-skills/skills/vision-flow.md` still has no mention of metaflow.

## 3. Large flows are kept and messaged

`F/compensation-launch.md:17-19`. Remove:

> When Flow supplies a context-budget observation, refresh before the budget it reports is exhausted. Do not claim that this observation exists when it has not been supplied.

Add:

> A flow past about a third of its context window refreshes itself. New work and messages go to its fresh successor, not to the large flow.

Evidence:
- "You were messaging a 700,000-token Fable Flow" (`t:d4ae97d4:1761`, 2026-10-06)
- "you were at 44% compact context and that's too large" (`t:d4ae97d4:2821`, 2026-10-07)
- "It's more like 20% to 40%" (`d4ae97/vision/flow.md:81`, 2026-10-07)
- "The field Astra's context is way too large and so is yours" (`8475a9/vision/voices.md:51`, 2026-10-05)

Why: no tool supplies that observation, so the line never fires.

## 4. The designer is given housekeeping

`F/compensation-default-effort.md` after line 10. Add:

> Housekeeping, such as file layout, commits or reformatting a book, goes to the cheapest flow that can do it, not to the designer.

Evidence:
- "We're making Fable mop the floor when it should be directing empires." (`t:d4ae97d4:3248`, `d4ae97/vision/books.md:211`, 2026-10-07)
- "here we are again, making Fable mop the floor" (`t:d4ae97d4:3490`, 2026-10-07)
- "You better not make Fable mop the fucking floor again." (`t:d4ae97d4:3511`, 2026-10-07)

## 5. What he ordered is reported as waiting on him

`F/compensation-orders.md:6-7`. Remove:

> Carry out the living's order in this turn. Run the commands needed for it; do not ask the living to confirm, approve, or run what he ordered.

Add:

> Carry out the living's order in this turn and run the commands it needs. A reply does not ask him to confirm, approve or run what he ordered, or list it as waiting on him; it names what blocks it.

Evidence:
- "I asked you to do it so don't say it's waiting for me." (`t:8f0f5790:268`, 2026-10-06)
- "What do you mean, waiting on answers from me?" (`t:d4ae97d4:3574`, 2026-10-07)
- "Don't ask me a single goddamn fucking question" (`t:d4ae97d4:3656`, 2026-10-07)

## 6. Code in books without its types, and too little of it

`F/compensation-book-distillation.md` after line 7. Add:

> Code in a book is ethos with its types and what they are for. A rule is shown as the wrong form first, then the right one.

Evidence:
- "Well those are the types for what? ... You can't just throw uncontextualized ethos code around." (`d66c26/vision/books.md:11`, `d4ae97/vision/books.md:148`, 2026-10-05)
- "you should also show the bad example and then the good example" (`d4ae97/vision/books.md:197`, 2026-10-06)
- "It just felt silly to keep going and reading all this Rust." (`t:db38f890:2470`, 2026-10-06)
- "there's very little code and there should be a lot more" (`aa887c/vision/books.md:7`)

## 7. Overbroad: "Never tell the living what he said"

`F/compensation-book-distillation.md:10`. Remove:

> Never tell the living what he said: no quote, paraphrase, summary or restatement of his words appears in anything he reads, and no section opens by recalling them.

Add:

> A book does not restate the living's words to him. A proposal cites the record it distils by path and date.

Why: as written, the line also bars the evidence a proposal needs, including the evidence asked for in this report.

His words: "quote blocks of what I had said ... I know what I said" (`e5a0bc/vision/books.md:15`, 2026-10-07). His objection is to restatement, not to citation.

## 8. Duplicates in book-distillation

`F/compensation-book-distillation.md:11-12`. Remove:

> Everything the living reads is a proposal: a change to a named file, shown as the lines removed and the lines added, with a ruling; a text that proposes nothing is not sent.

> Work moves forward through distillation: a book carries the raw records it would distil into a named skill, as that skill's new lines.

Why:
- Line 6 already carries the 99% proposal form.
- Lines 13-15 already carry the distillation-into-a-skill rule.
- Line 11 is also overbroad. It would forbid a result, a blocker, or the evidence `compensation-orders.md:13` requires.

## 9. "Never" in default-effort, which no program enforces

`roles.datom` still offers `Xhigh` for every model.

`F/compensation-default-effort.md:8-10`. Remove:

> Choose the least costly model and effort that can do the work. Never choose extra-high effort, keep duplicate expensive flows for one role, or reawaken a failed expensive flow without an explicit ruling.

Add:

> Choose the least costly model and effort that can do the work. Extra-high effort, a second expensive flow in one role, or reawakening a failed expensive flow waits for his ruling.

`F/compensation-default-effort.md:13-14`. Remove:

> Read configured layer and model values; never infer either from a title.

Add:

> Read configured layer and model values rather than inferring them from a title.

## 10. "Never" three times in the psyche-data rule

`F/compensation-design.md:9-12`. Remove:

> A flow never edits it on an order, report, review or contradiction list from another flow, never copies it elsewhere to edit there, and never moves it out of its place; it writes the change as a proposal in a book.

Add:

> An order, report or review from another flow does not license an edit, a copy to edit elsewhere, or a move. The change is written as a proposal in a book.

Why: the content stays as it is (his golden rule, `d4ae97/vision/psyche.md:117`, 2026-10-08). Only the "never" wording is removed, because nothing programmatic enforces the rule yet.
