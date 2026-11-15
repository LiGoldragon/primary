The preview adds separate, neutral lettered cards; ordinary green addition margins remain inside them, with no fourth change colour.
All three flowcharts were visible in the earlier published edition; the preview redraws the same three diagrams with different SVG geometry and line wrapping.

# Reader-visible differences in the balancing alternatives

## Evidence

Earlier source: `flows/655f27/proposals/balancing-alternatives.md`. Converted source: `flows/ab4e4b/proposals/balancing-alternatives.md`. Preview: `/tmp/book-ab4e4b.gqmYkw/balancing-alternatives.html`; phone/desktop screenshots: `preview-390.png` and `preview-1200.png` alongside it.

The earlier published edition is [The balancing: alternatives for its first form](https://claude.ai/artifact/HkfGv1RjiRzTawcKzoC4rH), retained version `1794775236-3cef`. Its saved full HTML is `/home/li/.claude/projects/-home-li-primary/33d4c0c3-d4c0-5fb0-892e-4193ced31038/tool-results/artifact-87aac9c0-1794775236-3cef.html`, copied for comparison to `/tmp/book-ab4e4b.gqmYkw/published-earlier.html`. Psyche book Haiku confirmed all three diagrams were visible, the options were prose rather than cards, and no new edition has been published (`objd`).

The comparisons below now use that **actual saved publication**, the converted source and the preview. The separate reconstruction `/tmp/book-ab4e4b.gqmYkw/balancing-earlier-reconstructed.html` was useful for isolating layout, but is not substituted for the actual edition. Parsed visible-text/shape records are retained as `old-visible.json`, `new-visible.json`, `published-earlier-svg.json` and `balancing-alternatives-svg.json` beside the preview.

## Wording and headings

- The page title and the creator/researcher line are unchanged.
- The four questions, their numerical order, their target module and the order of all fourteen options are unchanged.
- Each earlier running-text prefix `A.`, `B.`, etc. is removed from the option body and becomes a separate circular letter badge in a new card heading. All words after that prefix are preserved exactly, in the same order. No option body is dropped or newly invented.
- Each card adds a **new bold heading** copied from the option's words before its first colon. If the option has no colon, its entire body is repeated as the heading. This duplicates wording that previously appeared once in running text. These headings are new reader-visible text even though their words were taken from the bodies.
- The question's module path was part of the same large heading, after `·`. It is now a separate, smaller target line beneath the question. Its spelling is unchanged. The question-number badge is now above the question rather than beside its original combined heading.

The new card headings are:

| Question | Letter | Added heading |
| --- | --- | --- |
| What it watches | A | Energy alone |
| What it watches | B | A, and the machine's resources |
| What it watches | C | B, and the whole body |
| How it judges | A | By measures |
| How it judges | B | By a System 1 model |
| How it judges | C | By both |
| What it may do by itself, at first | A | It tells |
| What it may do by itself, at first | B | It tells and it holds |
| What it may do by itself, at first | C | It stops what is failing and brings the earlier version back to life. |
| Its name | A | The balancing. |
| Its name | B | Homeostasis |
| Its name | C | Allostasis |
| Its name | D | Samāna |
| Its name | E | The steersman, from kybernētēs |

In particular, the first question's B card is headed with a phrase beginning **A**, and its C card with one beginning **B**. Those were cross-references inside the earlier sentences; the conversion promoted them into the most prominent text of the respective cards. The third question's C option and the fourth question's A option now repeat their entire sentences, once as a bold heading and once as body text.

## Order, grouping and reading path

- Previously, one numbered proposal sheet held the question, its diagram where present, and the lettered additions below. The actual earlier publication joins the adjacent `+ A.`, `+ B.`, `+ C.` source lines into **one prose paragraph under one green margin**, with the letters in that running text. The five name options also form one paragraph. The new page splits those four paragraphs into fourteen separate option bodies, each inside its own card and green margin.
- The preview instead has an outer question enclosure and a separate white, rounded proposal card for each option. Every card has its own heading, letter badge, padding and inner green margin. Added space and repeated headings make the same bodies occupy more vertical room.
- At phone width the cards read A, then B, then C vertically. At desktop width they form two columns: A and B share a row; C starts the next row on the left. For the name question the rows are A/B, C/D, then E. The last card can therefore have an empty space beside it.
- The outer question enclosure uses the page background and a neutral border; previously the entire numbered proposal was one sheet. White option-card surfaces now separate the choices from that outer enclosure and from one another.
- Option headings use the bold label/headline face, while their bodies keep the ordinary prose face and size. Earlier letters and option labels were ordinary prose within the addition. No option receives a different change colour; the colours key remains the ordinary one.

## Where the diagrams stand

- The original source already contains three Mermaid fences: the increasing scope of what it watches; measures/model/both; and tell/hold/stop-and-rollback. The name question has no diagram in either source.
- No Mermaid fence text, node label, arrow, arrow label, branch or direction was changed by the conversion. All three fences stay under their original question and before that question's options, in their original order.
- The preview's three SVG files were freshly drawn by the Illustrator from those fences. They are **not the earlier edition's SVG files**. Node/arrow wording and connections are preserved, but box dimensions, coordinates, spacing, label line breaks and aspect ratios differ, as detailed below.
- In the actual earlier publication, each diagram sits directly above the one green-margined paragraph containing all its lettered options, inside the same proposal sheet. In the preview it sits in the outer enclosure **above the whole card grid**, outside every individual card. It is not placed beside a particular option and no diagram node is connected to a card.
- The diagrams' first and third chains run vertically A → B → C. On a wide screen, the cards beneath them instead read A/B across one row and C on the next. The second diagram shows A and B joining C; the card grid uses the same two-column placement as for the other questions, rather than a diagram-specific layout.
- The first diagram names its B node “Energy and resources” and C node “The whole body”; the new prominent card headings instead say “A, and the machine's resources” and “B, and the whole body.” The diagram/body wording already differed in the earlier source, but those body phrases were not previously separate bold headings.
- The new outer enclosure's side padding is 12px instead of the earlier proposal's 16px. At fixed available page width, its diagrams receive 8px more width. Separately, their redraw changes height substantially: the first becomes taller in proportion to its width, the second slightly taller, and the third much shorter.


### The actual redrawn diagrams

| Diagram | Earlier SVG view box | Preview SVG view box | Height at equal displayed width |
| --- | --- | --- | --- |
| What it watches | 400 × 370 | 420 × 460 | About 18.4% taller |
| How it judges | 400 × 420 | 430 × 460 | About 1.9% taller |
| What it may do | 400 × 620 | 400 × 400 | About 35.5% shorter |

- In diagram 1, the boxes stay 300 SVG units wide but become 70 units high instead of 56, within a wider/taller canvas. Their x coordinate moves from 50 to 60; the later boxes move down, from y154/y288 to y190/y360. Node labels use authored size 20 instead of 18; arrow labels use 17 instead of 16, within the changed coordinate scale. The second arrow's text was three lines, “and rhythm,” / “what is left lying,” / “itself”; it is now two, “and rhythm, what is” / “left lying, itself.” No words change.
- In diagram 2, the top boxes are farther apart in the SVG coordinate system and are moved upward. Their size changes from 170 × 80 to 190 × 70. The bottom combined box changes from 300 × 120 to 410 × 150 and becomes nearly canvas-wide. The inherited label size falls from 16 to 15 SVG units. The B label changes from “B. A System 1” / “model on each beat” to “B. A System 1 model” / “on each beat.” The C label changes from “C. Both: measures for” / “what is counted,” / “the model for the rest” to “C. Both: measures for” / “what is counted, the model” / “for the rest.” No words or joins change.
- Diagram 3 is vertically compressed. The earlier canvas was 620 units high and the preview canvas is 400; its boxes, arrows and arrow labels move accordingly. Its three 340-unit-wide boxes shrink from heights 80/120/80 to 60/90/60; corner radii change from 8 to 6. Node labels remain 18 SVG units, while arrow labels fall from 18 to 16. B was wrapped as “B. It holds:” / “nothing ended, nothing lost”; it becomes “B. It holds: nothing” / “ended, nothing lost.” The original tall diagram also had more canvas beneath its final label; the preview has less. No option or “and may also” arrow is removed.
- Thus there are two independent visible changes: the options become cards, **and the figures are redrawn**. The preserved Mermaid text did not preserve the earlier figures' visual form.

### Whole-page length

Under the same headless-browser viewport and installed fonts, the actual saved earlier edition is 3,243px tall at phone width 390; the preview is 5,006px, about **54.4% longer**. At desktop viewport 1200 (1,185px of document width after the scrollbar), it grows from 3,754px to 5,171px, about **37.7% longer**. Both remain within the horizontal viewport. These are measured renders, not estimates from source length. The corresponding `earlier-390.png` and `earlier-1200.png` are beside the preview screenshots; `earlier-preview.log` records the earlier DOM measurements.

## Current disposition

Fable has not adopted the form. No other page is to use it. Makeshift-tools main remains **fd83f4431e392b57389847565ca80e9ed7a98971**, containing only the separately requested removed-only Ethos fix. The alternative grammar, renderer, authoring commands/tests and authored knowledge changes are now **uncommitted evidence** in the isolated branches/worktrees `/tmp/book-ab4e4b.gqmYkw/{tools,mind}`. The earlier form still works. No publication of this preview was requested from the bookmaker.
