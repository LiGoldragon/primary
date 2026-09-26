# Layer words: the candidates

For the living, 2026-09-26. Prepared by e167d8 from its own research
(`reports/layer-vocabulary-research.md`) and from Fable's independent answer
(b860be, oracle answer 2, `flows/b860be/reports/oracle-2.md`). Nothing here
is ruled yet. The three questions at the end are for you to answer.

## The problem

The seat layers are called high, medium, and low. The model effort setting
also uses the words low, medium, and high. The two are separate scales that
share the same words, and the models confuse them.

The setup file shows the collision. `SKILL_VARIABLES.md` says:

    Psyche medium Claude model: claude-opus-4-6[1m]
    Psyche medium Claude effort: medium

In the second line, the first "medium" names the layer and the second
"medium" names the effort. `Intent/models.md` already has to explain that
"a flow named high is named by tier, not by effort setting".

Your words (typed, 2026-09-26, to Field Sol):

> ... the medium power layer of the aspect, like Sol and opus, is not about
> model effort here. Maybe we need a different vocabulary, so let's find a
> different vocabulary so they don't overlap, because it seems to be
> confusing the models. Let's call it the mid layer, or something. Let's go
> with Panini and look into astrological anatomy and all of this to find the
> right vocabulary. It can even be an expression, but short is good.

The words to avoid are the effort words (low, medium, high, xhigh, max,
minimal, light, ultra), words already used for ranking here (power, tier,
energy, rung), model and host names (Sol, Luna, Terra, Opus, Zeus...), and
repo terms (core, root, base, head).

## Your 09-16 layer anatomy

The words need to fit what each layer does. You described each layer on
2026-09-16 (`flows/f55ec8/vision/layers.md`). Fable summed it up in oracle
answer 2:

| Layer | What it does |
|---|---|
| Primary | Broad consideration. It is bothered as little as possible. |
| Secondary | Audits a request before it may bother the primary. |
| Tertiary | Liveness and real-time communication: staying alert, quick thinking. |
| Quaternary | Reflex filtering. It repairs speech-to-text and ignores noise before the mind starts communicating. |

In your own words:

> It has to pass an audit by the second layer before he can bother the
> layer above him. Any layer would function that way.

> The tertiary layer is where you would have the actual real-time
> communication. That's why it needs its own layer: everything that has to
> do with maintaining liveness, remaining alert and attentive, speech-to-text
> treatment, and quick thinking.

> The fourth layer is like the firewall. This is the layer that filters stuff
> out, corrects this speech-to-text, or pre-reflex, gut reflex, instinctive
> reflex, ignoring something completely, out of your consciousness, so that
> it doesn't have a sway on you.

The system now runs three layers per aspect (top, mid, low), plus a fourth
ultra-low seat that is temporary or has a special function.

## The five candidate sets

The order in each set is top / mid / low (+ ultra-low).

| # | Set | Meaning | Pros | Cons | Example title | Chosen by |
|---|---|---|---|---|---|---|
| 1 | **uttama / madhyama / kaniṣṭha** (+ **kaniṣṭhikā**) | best / middle / least (+ "littlest one", also the little finger) | *madhyama* is Pāṇini's own "middle person". The rank is inside the words. No effort setting uses them. The ultra-low word is a diminutive of the low word, which fits a temporary seat. It ties to hand anatomy: the middle finger is *madhyamā*. | 3–4 syllables. Speech-to-text may hear "Utama", "Ottoman", or "Kanishka". A fixed plain spelling is needed (Uttama, Madhyama, Kanishtha). | `PsycheV2.{ Fable uttama b860be }` | e167d8, first choice |
| 2 | **ucca / madhya / nīca** (+ **atinīca**) | high / middle / low (+ "very low") | The only pair that exists in both Pāṇini (accent: *uccaiḥ*, *nīcaiḥ*) and astrology (exaltation and debilitation). *madhya* is exactly "mid". The shortest Sanskrit set: 2 syllables each. | *nīca* also means "base, vile", which is mildly insulting for the low layer. Weakest for speech-to-text: "Utah", "Nietzsche", "media". | `PsycheV2.{ Fable ucca b860be }` | e167d8, second |
| 3 | **head / heart / hand** (+ **heel**) | thinking / judging / doing (+ foot end) | An existing expression (Pestalozzi's "Kopf, Herz und Hand") that ranks thinking over judging over doing. It describes each layer's work, not only its rank. Follows astrological anatomy from head to feet. By far the best for speech-to-text. | Not Pāṇini. "Head" collides with git HEAD. "Heel" also means a cad and may be heard as "heal". | `PsycheV2.{ Fable head b860be }` | e167d8, third |
| 4 | **vṛddhi / guṇa / mūla** (+ **aṇu**) | Pāṇini's vowel grades: fullest grade / strengthened grade / root grade (+ minute) | They name strength of form and never effort. Short and ordered. They come from the grammar you made the base of the system's ontology (09-08). Plain letters: vrddhi / guna / mula / anu. | *guṇa* is already used in the repo (and as sattva/rajas/tamas). The grades are technical words that need explaining. *vṛddhi* is hard to say and to spell. | `PsycheV2.{ Fable vrddhi b860be }` | Fable, first choice |
| 5 | **primary / secondary / tertiary** (+ **quaternary**) | your own ordinals | No new words. They already carry your 09-16 anatomy. Clear to every model. | "primary" is also the repository name, and "primary Psyche" is in daily use. Four ordinals for three layers plus a temporary fourth is loose. | `PsycheV2.{ Fable primary b860be }` | Fable, second choice |

## Where the two researches agree and differ

- Both keep "power" (energy) as the meaning of the axis. Both keep effort
  words for effort only.
- Both reject planet names (Sol, Luna, and Terra are already model names)
  and sattva / rajas / tamas.
- e167d8 favours words where the rank is visible in the word itself
  (best / middle / least). Fable favours Pāṇini's grammar vocabulary, then
  your own ordinals.

## Your three questions

1. **Which set?** Uttama / madhyama / kaniṣṭha, ucca / madhya / nīca,
   head / heart / hand, vṛddhi / guṇa / mūla, or primary / secondary /
   tertiary.
2. **Diacritics or plain letters** in titles and types? For example, `kaniṣṭha` or
   `kanishtha`, `vṛddhi` or `vrddhi`.
3. **Does the ultra-low seat get a word?** Or, because it is temporary or
   has a special function, is it named by what it does (relay, voice)
   instead?
