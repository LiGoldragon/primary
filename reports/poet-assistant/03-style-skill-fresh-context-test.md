# 03 - Style skill fresh-context test: raw food essay

*A subagent (Opus 4.7, no prior conversation context) wrote an
article on the raw-food falsehood applying `skills/prose.md` from
cold. This audit checks the artifact against the discipline; the
artifact itself is at `/tmp/style-test-raw-food.md`.*

## Why this test

The psyche pointed out that the parent agent's context is full of
the skill itself, the reference shelf, the canon, and the
conversation history — so the parent's prose is not a clean test of
the skill. A fresh subagent reads only the brief and the files the
brief points to. What the subagent produces is the discipline's
real effect.

## Test setup

Subagent: `claude` agent type, `opus` model (4.7), foreground, no
worktree. Brief: write a complete essay on the falsehood of the
modern raw-food claim, using Vedic and classical Āyurvedic primary
sources, in the *TheBookOfSol* register, following `skills/prose.md`
exactly. Required-reading list: `prose.md`, TheBookOfSol's
`AGENTS.md`, the existing `Cooking_and_Spices.md` (raw food covered
in its first half), and `Ambrosian_Diet.md` (positive doctrine).
Source pool: the workspace library and `TheBookOfSol/source-extracts/`.
Hard constraints itemised, including the new `### The quote
hype-up` rule. Output to `/tmp/style-test-raw-food.md`. 1797 words.

## The artifact

- **Title.** *The Fire on the Stove and the Fire in the Belly*
- **Subtitle.** *Why the classical tradition cooks*
- **Length.** 1797 body words
- **Central image.** The kitchen pot and the belly as one fire in
  two hands. Held first sentence to last.
- **Closer.** *"The fire on the stove and the fire in the belly
  are one fire."*
- **Primary sources used.** Aṣṭāṅga Hṛdaya (Vāgbhaṭa) Śārīrasthāna
  3.54–56 and Sūtrasthāna 8 and 12; Bṛhadāraṇyaka Upaniṣad;
  Taittirīya Upaniṣad 2.1, 2.2.1; Caraka Saṃhitā Sūtrasthāna
  1.126, 27.257–259, 27.275, 27.343; Haṭha Yoga Pradīpikā 1.58,
  1.59; Bhagavad Gītā 17.8; Ṛgveda 1.1.1. Twelve primary-source
  blocks in 1800 words — ~150 words per quote, right at the
  density the skill calls for.

## What the discipline produced

**Cold open in the substance.** *"Rice and water in a clay pot
over coals. The pot ticks as the grain swells."* No meta-prose,
no roll-call. The reader is inside the scene before the first
quote arrives.

**Single image held.** The cooking fire and the digestive fire as
one operation in two hands. The image opens the article; every
quote feeds it; the closer lands it.

**Quote-load, prose-spare.** Twelve substantive Sanskrit blocks
across the essay, each in the workspace's bold-IAST → blank-`>` →
English → em-dash format. Most prose between quotes is short
(orientation, naming what the quote established).

**Aphoristic close.** *"The fire on the stove and the fire in the
belly are one fire."* Restates the central image at its irreducible
form; not a summary of the argument.

**Catalog of witnesses.** The Vedic, the Ayurvedic (Caraka and
Vāgbhaṭa), the yogic (*Haṭha Yoga Pradīpikā*), and the *Bhagavad
Gītā* all converge on the same point. The convergence is the
argument; the article does not narrate the convergence as such.

**The chain image.** *"The 'life force' the raw foodist seeks is
the last link of a chain whose first link is pāka (cooking). From
cooked grain Caraka has the eater build rasa, from rasa the blood,
the flesh, the fat, the bone, the marrow, the generative essence;
from that whole tower the eight-drop refinement called ojas, and
from ojas the prāṇa the Upaniṣads name as deathless."* A list-as-
drumbeat in the *Chloride Indictment* mode, naming the chain so
the reader feels its order.

**Verses, not paraphrase.** Each Sanskrit verse is attributable;
none invented. The subagent used Caraka in the Priya Vrat Sharma
translation, Aṣṭāṅga Hṛdaya verses with IAST, Ṛgveda 1.1.1 in
the Griffith. Verse references included for traceability.

## Tics that survived

The discipline holds in the macro. Four small evaluative phrases
made it through, all of the family the new `### The quote
hype-up` rule names. Each is fixable in a five-minute editing pass.

1. **"...and closes the case in six words."** Preceding the
   *Aṣṭāṅga Hṛdaya* 3.54 quote. *"Closes the case"* is the
   evaluative-hype form — the article's author judging the quote.
   Fix: cut. Let the quote close the case itself.
2. **"...draws the picture in plain words."** Preceding the
   *Aṣṭāṅga Hṛdaya* 3.55–56 quote. *"In plain words"* is a small
   hype-up. The substantive part of the introducer (*"the
   eighth-century compendium of Vāgbhaṭa"*) earns its place; the
   evaluative tail does not.
3. **"Caraka states the reversal more bluntly..."** Preceding the
   bulky-and-hard verse. *"More bluntly"* is the comparative
   evaluative form. Fix: name the substance — *"For hard and bulky
   substances, Caraka states the reversal:"* — or cut.
4. **"The foundational diet-verse of the yogic tradition..."**
   Preceding *Haṭha Yoga Pradīpikā* 1.58. *"Foundational"* is the
   evaluative qualifier. The rest of the clause (*"describes a
   plate no raw-food brochure would recognise as yogic at all"*) is
   substantive and earns its place; the qualifier could go.

None of these undermines the article. They are the residue of the
general training-data introducer reflex that the new rule names
directly. They confirm the rule is well-aimed: the subagent
applied the discipline at 95% even after reading the new section,
because the deeper habit takes a sweep to root out.

## Other small notes

- The transition into the *Caraka Saṃhitā* 1.126 (poison-into-
  medicine) quote is slightly weak. The verse is general; its
  link to the cooking argument is *saṃskāra* changes *guṇa*. The
  prose around it could name that link more directly.
- The penultimate section *"What weak fire does"* moves out of
  the central image briefly into a separate argument (*"All
  diseases arise where agni is weak"*). The argument is sound; the
  image-load drops for a paragraph. A revision could either tie
  the section more directly to the kitchen-pot / belly-fire image
  or compress it.
- Several Sanskrit quotes use `\` line-breaks in the middle of
  the verse — correct per the convention. Attribution lines are
  clean.

## Verdict

The skill produces the right register in the hands of a fresh
agent. The subagent's reading list — `prose.md`, the AGENTS,
Cooking_and_Spices, Ambrosian_Diet, source-extracts — was enough
to bring it to the canon's voice. Four minor hype-up phrases
slipped through; the new rule reaches them in a second pass.

The artifact would serve, after a brief revision pass, as a
publishable article in `TheBookOfSol/ayurveda/` or `/diet/`. It
extends `Cooking_and_Spices.md`'s first half into a stand-alone
essay focused entirely on the raw-food argument, which the canon
has wanted.

## Open questions for the psyche

1. **Promote the artifact?** Move from `/tmp/style-test-raw-food.md`
   into `TheBookOfSol/ayurveda/Raw_Food.md` (or whichever filename
   fits the canon) after the four hype-up phrases are fixed.
2. **Apply the small revisions** flagged above, or accept as-is?
3. **Run more fresh-context tests** with different subjects to
   stress the skill further (e.g. the cosmological register, the
   chloride argument, the personal essay)?
4. **Add a "When this skill is being tested" line** to
   `prose.md` itself — naming the failure mode the audit caught
   (the introducer-reflex that the rule reaches in revision but
   not always in first draft)?

## See also

- `/tmp/style-test-raw-food.md` — the artifact under audit
- `skills/prose.md` — the discipline applied
- `reports/poet-assistant/02-quote-framing-research.md` — the
  research that produced the new rules tested here
- `TheBookOfSol/ayurveda/Cooking_and_Spices.md` — the canon article
  the artifact extends
