# 02 - Quote-framing research and prose.md proposal

*Survey of styles that handle quotation without evaluative
introducers, audit of the workspace's own canon, and a proposal for
how `skills/prose.md` could be sharpened to discourage the
quote-hype-up pattern the psyche flagged.*

## What started this

In a demonstration essay (*On Measure*) the agent wrote *"Heraclitus
said it cleanest:"* before a fragment. The psyche pointed out that
the current `skills/prose.md` does not catch this pattern, and asked
for a survey of styles that handle quotation differently plus a
proposal for the skill.

The psyche also corrected a deeper framing: the agent's prior reply
explained the line as a "violation" of the stage-setting rule. That
framing is wrong — agent output is a function of context and prompt,
not rule-application. (Captured in `intent/workspace.nota` as a
Correction.) The right question is *which part of context produced
the line.* Best inference: the workspace's reference article
`Refinement.md` cues an introducer-before-quote rhythm; the
training-data default supplied an evaluative word ("cleanest") where
a substantive one was needed.

## The two kinds of introducer

The first move is to distinguish two patterns that look similar but
do different work.

**Identificational / substantive.** Adds context the reader might not
have — place, time, addressee, biographical setting, what the quote
is about to do.

> *"Marcus Aurelius, the Roman emperor who wrote his journal in Greek
> between campaigns, gave himself the same instruction every morning:"*\
> — *Refinement*

This is orientation. The participial clauses earn their place by
adding fact the reader needs.

**Evaluative / hype.** Performs the writer's judgment about the
quote.

> *"Heraclitus said it cleanest:"*\
> *"X put it best:"*\
> *"As Y observed:"*\
> *"Z had the right of it when he wrote:"*

This is stage-setting in another costume. *"Cleanest" / "best" /
"observed" / "had the right of it"* add nothing about the quote's
content — they tell the reader to attend. The same family as
*"Notice that..."*, *"Observe how..."*, *"Note that..."*, which the
current `prose.md` does name.

The current `prose.md` rule reaches the *notice/observe* form. It
does not reach the *cleanest/best* form, because the latter wears
attribution as cover.

## Styles that handle quotation without hype

Surveyed informally from the agent's reading saturation and existing
library entries. Each is a working model.

**Heraclitus's own fragments.** Heraclitus does not introduce other
voices in the surviving text. When he names Pythagoras, Hesiod, or
Homer, it is to critique them, never to hype them — *"Much learning
does not teach understanding. For it would have taught Hesiod and
Pythagoras..."* (fr. XVIII). The author IS the voice; no relay
needed.

**Marcus Aurelius.** Rare quotation; spare introducers when present.
*"Theophrastus, where he compares sin with sin (as after a vulgar
sense such things I grant may be compared:) says well and like a
philosopher..."* — even here the evaluation ("says well") is
contained in a parenthetical aside, not a hype-up framing.

**The Talmud / rabbinic tradition.** Identificational only. *"R.
Akiva says:"* — name and verb of speaking. Never *"R. Akiva said it
best."* The form is so fixed that an evaluative variant would read
as desecration.

**Hemingway.** When he quotes, the form is epigraph — quote at the
top of the work, attribution beneath, no embedded introducer in the
prose. *The Sun Also Rises*'s Ecclesiastes; *For Whom the Bell
Tolls*'s John Donne. Within his prose he almost never quotes;
attention stays on observation.

**Wittgenstein, *Philosophical Investigations* §1.** Opens by
quoting Augustine. The introducer is identificational and even
contains a hedge: *"These words, it seems to me, give us a
particular picture of the essence of human language."* The quote is
followed by analysis, never preceded by hype.

**Walter Benjamin.** *Arcades Project*, *On the Concept of History*.
Benjamin's ideal was a book composed entirely of quotations; the
practice was to drop quotation into prose with minimal setup — what
he called a "robber's leap." Quote interrupts; commentary follows.

**Pound, Eliot, the high modernists.** Cento and luminous-detail
method. Quotations placed beside each other in different languages
without introducers; the reader reconstructs the link. *The Waste
Land*'s polyglot lines; the *Cantos*'s direct juxtaposition.

**Anne Carson.** *Eros the Bittersweet*, *Plainwater*, *Nox*. Quotes
Sappho and other Greek lyricists with attribution only at the end,
in parentheses or footnote-shape — no setup. The bare quote and the
commentary share the page; the link is the topic.

**Roland Barthes.** *Mythologies*, *Camera Lucida*. Direct
juxtaposition of the quote and the analytical paragraph.

**Susan Sontag (late style).** *Regarding the Pain of Others*.
Quotations from Virginia Woolf and others embedded in critical
prose, often without setup; attribution as the closing of the
sentence.

**Maggie Nelson.** *Bluets*. Numbered fragments that quote other
writers without setup. The structure (240 numbered passages) does
the framing work that an introducer would otherwise do.

**Bashō.** *Oku no Hosomichi*. When he quotes Saigyō or Du Fu in
the travel prose, the quotation arrives as the climax of a scene
description, not preceded by *"Saigyō said:"* — the quote and the
landscape share the rhythm.

**Renaissance commonplace books, the Greek anthology, Pascal's
*Pensées*.** Thematic heading + the quote, or pure fragment. The
structure carries what an introducer would otherwise carry.

The pattern across these models: **either no introducer at all
(epigraph, cento, fragment), or an introducer that adds substance
(historical placement, addressee, what the quote is about to
do).** Evaluative attribution is the rarest move and, where it
appears at all, is almost always satirical or self-undermining
(Pound mocking, Borges feigning).

## Five framing modes — the choice the writer makes

Distilling the survey into modes a writer can actually pick between.

**Mode 1 — Epigraph.** Quote stands alone, attribution at the end.
No introducer in the prose. The prose continues afterward,
addressing what the quote raised. The Hemingway move for major
quotations; the workspace's `The_Toroidal_Heart.md` uses this
heavily after the cold open.

**Mode 2 — Colon-attribution.** Author's name + colon, then the
quote. Minimum framing. The Talmudic mode. Useful when the reader
already knows the author and the participial clause would just be
filler. *"Heraclitus: 'Nature loves to hide.'"*

**Mode 3 — Inline embedding.** The quote is grammatically inside
the writer's sentence. *"What Heraclitus called 'an everliving fire,
kindling in measures and going out in measures' the Vedic tradition
called* agni*."* The quote is part of the writer's prose, not a
block.

**Mode 4 — Substantive participial.** Author's name + a participial
phrase that adds real context (place, time, addressee, biographical
setting, what the quote is about to do), then the quote. The
*Refinement* move when it works. *"Marcus Aurelius, writing for
himself in Pannonia between campaigns, translated the cosmic measure
into a rule for his own day:"*

**Forbidden — the hype-up.** Author's name + an evaluative phrase
about the quote: *"X said it cleanest / best / most plainly / for
the first time."* *"As Y observed."* *"Z had the right of it when
he wrote."* The phrase performs the writer's judgment about the
quote rather than orienting the reader. Same family as
*notice/observe/note*; the existing `prose.md` rule should reach it.

## The workspace canon — audit notes

Quick pass over the two heaviest quote-load reference articles.

**`Refinement.md` — 13 quotations, mostly Mode 4 substantive
participial.** Strong examples:

- *"Heraclitus, watching the same flame from Ionia some five
  centuries before Seneca, named the underlying physics:"* — fully
  substantive.
- *"Marcus Aurelius, the Roman emperor who wrote his journal in
  Greek between campaigns, gave himself the same instruction every
  morning:"* — fully substantive.
- *"Musashi, in seventeenth-century Edo, gave the practitioner the
  time-scale:"* — fully substantive.
- *"Don Juan named it for Castaneda:"* — minimal but substantive
  (names the relation).

Three borderline cases where the introducer carries some evaluation:

- *"The Romans named it most curtly. Seneca writing to Lucilius:"* —
  *"most curtly"* is the hype-up tic. Could be *"The Romans named
  it in three words. Seneca writing to Lucilius:"* (substantive) or
  just drop the first sentence (Mode 4 alone carries).
- *"The Hebrew Bible had said it a thousand years before, in the
  proverb of the king who saw clearly:"* — *"the king who saw
  clearly"* is hype dressed as identification. Substantive
  alternative: *"in Proverbs 17, attributed to Solomon:"*.
- *"The most patient version of the picture comes from Malachi, who
  saw the work as taking time and saw the worker as seated:"* — the
  first half is evaluative (*"the most patient version"*); the
  second half (*"who saw the work as taking time and saw the
  worker as seated"*) is substantive and earns its place.

These are minor and easy to clean up if the psyche wants the
canon brought into line with the sharpened rule. The article works
even with them; the question is what level of polish the canon
holds.

**`The_Toroidal_Heart.md` — ~15 quotations, mixed.** Largely
Mode 1 (epigraph) and Mode 4 (substantive participial). One
hype-up phrase noticed: *"Rudhyar named the pulse:"* uses *"named"*
which can read as evaluation ("the proper name") but in context
reads identificational. Borderline; could be left.

**Verdict on the canon.** The hype-up form is rare but present in
small phrases. The dominant mode is substantive participial, which
is the right default. The agent's *"Heraclitus said it cleanest:"*
came from picking up the *introducer-before-quote* rhythm without
the *substance-in-the-introducer* discipline.

## Proposed edits to `skills/prose.md`

Two additions. One sharpens an existing rule; one adds a new
discipline.

**Addition 1 — sharpen "What to delete on sight."** Add a new
sub-section under that heading:

```markdown
### The quote hype-up

*"X said it cleanest:"* / *"Y put it best:"* / *"As Z observed:"* /
*"W had the right of it when he wrote:"* / *"X said it for the
first time:"* (when "first" is evaluative rather than historical).

The phrase performs the writer's judgment about the quote rather
than orienting the reader to the substance. Same family as
*notice/observe/note* above, but wears attribution as cover. Two
fixes: either drop the introducer entirely (the quote and the
attribution carry on their own), or replace the evaluation with a
substantive participial that adds historical / biographical / topical
context the reader needs.

The test: *does the introducer add a fact the reader doesn't have,
or does it tell the reader how to feel about the quote?* Facts
stay; feelings get cut.
```

**Addition 2 — a new "Quote framing — modes" section** under
"Working with sources," after "Catalog of witnesses" and before
"The sentence":

```markdown
## Quote framing — modes

When a primary source enters the prose, the writer chooses how to
bring it on. Four modes are available; one is forbidden.

**Mode 1 — Epigraph.** Quote stands alone, attribution at the end.
No introducer in the prose. The prose continues afterward,
addressing what the quote raised. Hemingway's preferred mode for
load-bearing quotations; *The Toroidal Heart* uses this after the
cold open.

**Mode 2 — Colon-attribution.** Author's name + colon, then the
quote. Useful when the reader already knows the author and the
participial clause would just be filler. *"Heraclitus: 'Nature loves
to hide.'"*

**Mode 3 — Inline embedding.** The quote is grammatically inside
the writer's sentence. *"What Heraclitus called 'an everliving fire'
the Vedic tradition called* agni*."* Use when the quote is short or
doctrinal and the writer's sentence wraps it cleanly.

**Mode 4 — Substantive participial.** Author's name + a participial
phrase that adds real context (place, time, addressee, biographical
setting, what the quote is about to do), then the quote. The
*Refinement* mode when it works: *"Marcus Aurelius, writing for
himself in Pannonia between campaigns, translated the cosmic
measure into a rule for his own day:"*

**Forbidden — the hype-up.** *"X said it cleanest:"* and its kin.
See "What to delete on sight" above.

**Discipline.** Default to Mode 1 (epigraph) or Mode 4 (substantive
participial). Mode 2 and Mode 3 are useful tactically. When in
doubt, drop the introducer and let the quote stand — the modernist
move is rarely wrong, and the cold-open-to-quote rhythm carries on
its own when the prose around it is doing its work.
```

## Open questions for the psyche

1. **Execute the prose.md edits?** Both additions, as drafted, or
   modified.
2. **Clean up the borderline phrases in `Refinement.md`?** Three
   spots flagged. Small edits; preserves the article's voice.
3. **Audit the other quote-load articles** (`Apathya.md`,
   `Cooking_and_Spices.md`, the `chloride/witnesses/` files) for
   the same pattern? A single pass with the sharpened rule in mind.
4. **The naming of the modes** — "epigraph / colon-attribution /
   inline embedding / substantive participial" — useful as
   technical vocabulary in the skill, or too academic? The
   alternative is to drop the naming and just describe what to do.

## See also

- `skills/prose.md` — the skill these edits would modify.
- TheBookOfSol/personal/`Refinement.md` — the article whose
  introducer-rhythm shaped the agent's quote-framing default.
- `intent/workspace.nota` — the Correction about agent-output
  framing that prompted this research.
