# The Book of Sol — "Other Suns" Survey

Read-only sweep of `/home/li/primary/repos/TheBookOfSol` at the **current working-tree
state** (not HEAD). Working copy `unxvuuun ef054dca`, parent `rrpvkopt 87bf34d1 main`.
Uncommitted at survey time:

```
M _index.md
D cosmology/Computing_vs_Measuring_The_Curve.md
M cosmology/Horizon_Dip_vs_Altitude.md
M source-extracts/Dane_Rudhyar/astrological-houses.md
M source-extracts/Dane_Rudhyar/astrology-of-personality.md
M source-extracts/Dane_Rudhyar/astrology-of-transformation.md
M source-extracts/Dane_Rudhyar/practice-of-astrology.md
```

## The criterion applied

Author's words: *"it says the sun is a star, it doesnt say the stars are suns."*

- **NOT A HIT** — Sol placed among the lights; Sol called a star; Sol named inside a
  galaxy or a stellar field.
- **HIT** — the converse: a light other than Sol asserted to be itself a sun, or to
  carry its own world / planets / system; plural suns; plural solar systems; other
  earths; space as an open unbounded expanse holding further systems.

Direction test used on each candidate: *does this sentence assert that a light other
than Sol is itself a sun with its own world or system?*

## Coverage

All 130 `.md` / `.txt` files under the repo were swept (22,099 lines / 318,720 words).
Read in full: `_index.md`, `ARCHITECTURE.md`, `AGENTS.md`, `skills.md`, both files in
`cosmology/`, all 13 files in `sol-luna/` (the two 400–800-line degree-listings by
targeted grep on every cosmological term, then passage-read on each match), all nine
`source-extracts/Dane_Rudhyar/` files, `source-extracts/Arthur_Young/`,
`source-extracts/Plutarch_De_Facie/`, both `Hesiod_Homeric_Hymns/` files. Everything
else (`ayurveda/`, `diet/`, `chloride/` incl. `witnesses/`, `water/`, `ghee/`,
`political/`, `personal/`, `teasers/`, `yoga-tantra/`,
`research_yoga_ayurveda_lineage/`, remaining `source-extracts/`, `.substack-posts.json`)
was grep-swept on the full term list and every match was read in its surrounding
passage.

Term list run: `suns`, `other sun`, `star(s)`, `stellar`, `solar system(s)`,
`galax*`, `galactic`, `planet(s)`, `planetary`, `worlds`, `other worlds`,
`other earths`, `extraterrestrial`, `interstellar`, `light-year`, `constellation`,
`nebula`, `firmament`, `cosmos`, `cosmic`, `universe`, `empty space`, `outer space`,
`deep space`, `depths of space`, `infinite`, `boundless`, `countless`, `myriad(s)`,
`inhabited`, `habitable`, `orbit*`, `heliocentric`, `geocentric`, `astronom*`,
`telescope`, `alien`, `Milky Way`, `exoplanet`, `billions of`, `stars are`,
`another star`, `each star`, `every star`, `sun among`.

## OBSERVATIONS — HITS

### HIT 1

**Path / line:** `personal/Dharma_by_Annie_Besant.md:41`

**Verbatim sentence:**

> If we are tired of the earth, the telescope brings to our view the Beauty of myriads
> of suns, rushing and rolling through the depths of space.

**Voice:** QUOTED EXTERNAL SOURCE — Annie Besant, *Dharma*, Three Lectures delivered
at the Eighth Annual Convention of the Indian Section of the Theosophical Society,
Vārāṇasī, 25–27 October 1898; first lecture, "Differences", at printed page [10].
The whole file is a full verbatim reproduction of Besant's text carried in the repo as
a standalone document (title block at lines 1–5: `# **DHARMA**` / `**by Annie
Besant**`), not a block-quote embedded in project prose.

**Why it is a hit:** plural suns ("myriads of suns"), located in "the depths of
space" — the exact converse the criterion names. The telescope is named as the
instrument that shows them, so the claim is presented as observational, not
metaphorical.

**Separable or irreducible:** SEPARABLE as a sentence, with one concrete downstream
dependency inside the same paragraph.

**Concrete breakage, verified:**

1. The very next sentence, same paragraph, same line 41, reads: *"Then the microscope
   reveals to our wondering gaze the Beauty of the infinitely small, **as the telescope
   does of the infinitely great**: and thus a new door is opened to us for the
   contemplation of Beauty."* The clause "as the telescope does" back-references the
   telescope introduced only in the offending sentence. Removing the suns sentence
   orphans that clause.
2. The suns sentence is one item in a running list of Beauty-examples that runs
   ocean → wind-lashed sea → moonlit ripples → mountain lake → torrent → iceberg →
   mists → creeper → oak → forest → mountain peak → prairie → desert → meadow →
   *telescope/suns* → microscope → animal → man → woman → children. The list's rhythm
   is the paragraph's whole structure.
3. The file is presented under Besant's name as an 1898 lecture text. Any edit alters
   an attributed historical document rather than project prose.
4. Linked from the table of contents at `_index.md:140`
   (`- [Dharma, by Annie Besant](./personal/Dharma_by_Annie_Besant.md)`).
5. **Not** a Substack liability: `.substack-posts.json` contains no entry for this
   file (checked; no `Dharma`/`Besant` key). No front matter, no `publish:` flag.

This is the only occurrence of the word "suns" anywhere in the repository, and the
only astronomical passage in a 19,296-word file (the file's other `star` matches at
lines 11, 95, 105 are all "starving" / "starting").

## OBSERVATIONS — UNCERTAIN (over-reported borderline, reasoning stated)

### UNCERTAIN A — the nested-tori paragraph

**Path / lines:** `sol-luna/The_Toroidal_Heart.md:156` (and the dependent 158)

**Verbatim sentences:**

> The solar system is a torus, and the galaxy is one larger torus that holds it.

> Each scale has its own core and its own skin, its own equatorial plane, its own Two
> Lights.

> The solar system has the sun for a core and the heliopause for a skin.

**Voice:** AUTHOR'S OWN PROSE.

**Why uncertain:** by the stated rule this is NOT a hit — it places Sol's system inside
a galaxy, i.e. names Sol within a stellar field, and never says another light is a sun.
Three things pull the other way and I decline to resolve them silently:

1. The container hierarchy world → solar system → galaxy is the modern astronomical
   ladder, and the paragraph asserts the galaxy as a real physical torus with "its own
   core and its own skin, its own equatorial plane, its own Two Lights" — a galactic
   core that is not Sol.
2. "the heliopause for a skin" is the boundary of the solar wind against the
   interstellar medium. Naming the heliopause presupposes a beyond-the-solar-system
   space of the modern kind.
3. The same file earlier (line 15) builds a self-contained world-torus in which "the
   Sun and the Moon are the two driving Lights" moving through *this* field — so line
   156 layers a second, larger, non-solar cosmology over the first.

**Separable or irreducible:** the galaxy clause is SEPARABLE. Verified: line 158's
dependent claim names only *three* scales — "an individual body's core-and-skin within
the world's core-and-skin within the solar system's core-and-skin — three scales
pulsing in resonance, three Two-Lights" — the galaxy is not one of them. Removing "and
the galaxy is one larger torus that holds it" therefore breaks nothing at 158. The
"solar system is a torus" clause is IRREDUCIBLE to 158 (which counts the solar system
as scale three) and to line 156's own "The solar system has the sun for a core and the
heliopause for a skin."

### UNCERTAIN B — "man as a whole solar system"

**Path / line:** `source-extracts/Dane_Rudhyar/astrology-of-personality.md:27`

**Verbatim:**

> "Personality, in the largest sense, is the organic whole in which the physiological
> and the psycho-mental natures of man are progressively integrated. Therefore it
> represents the wholeness of the human being as a microcosm; man as a whole solar
> system operating on the background of, and in constant relationship to the zodiac or
> the galaxy."

**Voice:** QUOTED EXTERNAL SOURCE — Dane Rudhyar, *The Astrology of Personality*,
Preface (1936/1968).

**Why uncertain:** "a whole solar system" used as a count noun of which a man is an
instance implies solar systems are a class with more than one member. The direction
test says NO — the claim is explicitly a microcosm metaphor, and no other sun is
asserted. Reported because the phrasing is a plural-systems grammar even where the
assertion is not.

**Separable or irreducible:** IRREDUCIBLE as presented. The extract introduces this
block as "the definition of *personality* that the book has carried since 1936"
(line 25); it is the load-bearing quote of section I. Trimming the clause would edit a
verbatim quotation of Rudhyar.

### UNCERTAIN C — Plutarch's moon as another earth

**Path / lines:** `source-extracts/Plutarch_De_Facie/passages.md` — quoted Plutarch at
9, 12, 17, 43, 48; author's scaffolding notes at 56, 58, 60.

**Verbatim (the sharpest instances):**

> "It is in fact not incredible or wonderful that the moon … has got open regions of
> marvellous beauty and mountains flaming bright and has zones of royal purple with
> gold and silver not scattered in her depths but bursting forth in abundance on the
> plains or openly visible on the smooth heights." (line 9, *De facie* 935C, trans.
> Cherniss)

> "The honourable repute of the moon is surely not impaired nor is her divinity because
> she is held by men to be a (celestial and) holy earth rather than, as the Stoics say,
> a fire turbid and dreggish." (line 12, 935D)

> "Luna has substance, weight, locus — a world." (line 56, AUTHOR'S SCAFFOLDING)

> "The moon is another earth, reversed." (line 60, AUTHOR'S SCAFFOLDING)

> "The lunar inhabitants do not stay. They come down as oracle-guardians, as
> ritual-partakers, as saviours in war and at sea." (line 58, AUTHOR'S SCAFFOLDING)

**Voice:** mixed — QUOTED EXTERNAL SOURCE (Plutarch, *De facie quae in orbe lunae
apparet*, trans. Harold Cherniss, Loeb Classical Library 406) for 9/12/17/43/48;
AUTHOR'S SCAFFOLDING for the "Notes for The Book of Sol" at 53–61.

**Why uncertain:** the criterion's hit-list explicitly includes "other inhabited or
inhabitable worlds, other earths", and this passage asserts exactly that — the Moon is
an earth, with mountains, plains, metal veins, hollows, and inhabitants who descend and
return. But the direction test says NO: the Moon is not asserted to be a sun; the
extract states the reverse at line 25 — "the sun furnishes mind to man for the purpose
of his generation — even as it furnishes light to the moon herself." Plural worlds YES,
plural suns NO. The author's own call.

**Separable or irreducible:** IRREDUCIBLE. The moon-as-earth/inhabited-world doctrine
*is* the extract.

**Concrete breakage, verified by reading the dependents:**

- `sol-luna/2-Luna.md:40` — "In Plutarch's composition doctrine, earth gives the body,
  moon gives the soul, and sun gives the mind (*De facie* 943A). The three bodies of the
  cosmos contribute to the human being as three ingredients."
- `sol-luna/2-Luna.md:42–46` — the whole "She has two faces" section, built on 944C:
  "*Phersephónēs oikos antichthonos*, the house of counter-earth Persephone" and "the
  literal double-orientation of a world between two worlds".
- `sol-luna/2-Luna.md:58` — the closing salutation names her "double-faced world between
  two worlds".
- `sol-luna/The_Toroidal_Heart.md:70–72` — block-quotes 944C directly: "The half of the
  moon that faces heaven is the Elysian plain; the half that faces earth is the house of
  counter-earth Persephone."
- `source-extracts/Upanisads/moon-as-soul-threshold.md:75` — cross-references the
  Plutarch doctrine as the structural parallel to the Upaniṣadic pitṛyāna.
- `_index.md` carries `2-Luna.md` at line 10 and `The_Toroidal_Heart.md` at line 11.

### UNCERTAIN D — stellar spectrum classification

**Path / lines:** `source-extracts/Dane_Rudhyar/astrology-of-personality.md:47` and
`:49`

**Verbatim:**

> **The Animistic Stage** — astrology as personification of stars and planets; the
> *star-quality* is read from the quality of the light, a pre-spectrum-analysis
> intuition of the same data: (line 47, AUTHOR'S SCAFFOLDING)

> "Curiously enough, we are not so far from a classification of stars on the basis of
> spectrum analysis! Only instead of using a prism to determine the quality of the
> light, objectively and analytically, primitive man experienced subjectively this
> light, and projected back into the star the result of this psychic identification."
> (line 49, QUOTED — Rudhyar, *The Astrology of Personality*, "The Animistic Stage")

**Why uncertain:** stellar spectroscopy is the specific instrument by which stars came
to be held to be suns, and the scaffolding line endorses it as "the same data". But no
sentence here asserts a star is a sun; the claim is only that stars differ in the
quality of their light. Direction test: NO.

**Separable or irreducible:** the scaffolding phrase "a pre-spectrum-analysis intuition
of the same data" at line 47 is SEPARABLE. The quote at 49 is IRREDUCIBLE without
editing Rudhyar's words; it is the only quote carrying section II's Animistic Stage.

## OBSERVATIONS — NEAR-MISSES DECLINED

Every candidate below was generated by the term list and read in passage, then declined.
Grouped by why.

### (a) Sol named as a star / inside a galaxy — the criterion's paradigm not-a-hit

| Path:line | Verbatim | Voice |
|---|---|---|
| `source-extracts/Dane_Rudhyar/astrology-of-transformation.md:111` | "The galactic frame extends this: the Sun is one star among many in the galaxy, and the individual one node within the worldwide humanity." | AUTHOR'S SCAFFOLDING |
| `astrology-of-transformation.md:5, 107, 139`; `practice-of-astrology.md:139` | the cited Rudhyar book title *The Sun is Also a Star* (1975) | SCAFFOLDING (bibliographic) |
| `astrology-of-transformation.md:100, 107` | "the galactic frame"; ":120" — "the transindividual (or symbolically, the 'galactic') level" | SCAFFOLDING / QUOTED |
| `practice-of-astrology.md:139` | "the galactic dimension" | SCAFFOLDING |
| `source-extracts/Dane_Rudhyar/astrological-houses.md:54` | "These correspond to three concentric universes (biosphere, solar system, galaxy)" | AUTHOR'S SCAFFOLDING |
| `source-extracts/Dane_Rudhyar/new-approach-to-zodiac.md:15` | "transforming not only our approach to the zodiac, but our entire picture of the solar system and the universe as well." | QUOTED (Rudhyar) |
| `sol-luna/The_Toroidal_Heart.md:156` | see UNCERTAIN A | AUTHOR'S OWN PROSE |

Line 111 of `astrology-of-transformation.md` survived the prior cutting pass and is the
cleanest illustration of the boundary: it says the sun *is* a star and stops there.

### (b) Stars present but subordinated, symbolic, or explicitly denied agency

| Path:line | Verbatim (abridged where long) | Voice |
|---|---|---|
| `sol-luna/Rudhyar_Zodiac_As_Process.md:28`; `source-extracts/Dane_Rudhyar/pulse-of-life.md:59` | "The Zodiac which is used in our astrology has very little, if anything at all, to do with distant stars as entities in themselves." | QUOTED (Rudhyar, *Pulse of Life*) |
| `source-extracts/Dane_Rudhyar/practice-of-astrology.md:62` | "The signs of the zodiac have nothing to do whatsoever with actual stars and constellations, but are simply twelve phases of the cyclic relationship between the earth and the sun." | QUOTED (Rudhyar) |
| `source-extracts/Dane_Rudhyar/pulse-of-life.md:39` | "It uses the ordered pageant of planets (and to a lesser extent, of the stars) as a symbol…" | QUOTED (Rudhyar) |
| `source-extracts/Dane_Rudhyar/astrology-of-personality.md:164` | "The stars force nothing into us that we are not willing to take…" | QUOTED (Paracelsus, via Rudhyar) |
| `sol-luna/Celestial_Name.md:9` | "…are in terror at the very stars, and the whole heaven, and the night, and all the celestial appearances." | QUOTED (Plutarch, *De Superstitione*) |
| `source-extracts/Armando_Torres/death-the-sorcerers-option.md:59` | "the light of a candle against the glare of a billion stars." | QUOTED (Torres) |
| `sol-luna/The_360_Phases_of_Sol.md:165` | "**Leo 7°:** The constellations of stars shine brilliantly in the night sky; represents the power of basic spiritual values." | SCAFFOLDING (Sabian symbol listing) |
| `sol-luna/The_108_Solar_Divisions.md:3` | "twenty-seven *nakshatras* (lunar mansions, the fixed star-fields of the sidereal sky)" | AUTHOR'S OWN PROSE |
| `sol-luna/The_108_Solar_Divisions.md:37, 338` | "becoming a first lord of the stars"; "The soul travelling through the stars communicates its royal decree" | SCAFFOLDING (nakshatra listing) |
| `source-extracts/Rg_Veda/soma-and-the-moon.md:23` | "Thus Soma in the midst of all these constellations hath his place." | QUOTED (*Ṛgveda*, trans. Griffith) |
| `source-extracts/Upanisads/moon-as-soul-threshold.md:19` | "its coals the moon, its sparks the stars" | AUTHOR'S SCAFFOLDING (Pañcāgni-vidyā summary) |
| `source-extracts/Upanisads/moon-as-soul-threshold.md:55` | "There the sun does not shine, nor the moon and stars…" | QUOTED (Upaniṣadic refrain) |

### (c) Sentences that rank Sol *above* the stars — the opposite direction

| Path:line | Verbatim | Voice |
|---|---|---|
| `personal/Physical_Mortality_and_Essential_Immortality.md:240`; `source-extracts/Hermetic_Corpus/death-and-the-immortal-essence.md:98` | "…the confidence of his belief puts him as far from humanity as the sun outshines the stars." | QUOTED (*Asclepius* / Hermetic corpus) |
| `personal/Physical_Mortality_and_Essential_Immortality.md:243` | "The sun-and-stars image is identical across the three corpora." | AUTHOR'S SCAFFOLDING |
| `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md:290` | "Only on the fourth day were the sun, moon, and stars created, and they were placed 'in' (not 'above') the vault." | QUOTED (flat-earth / Hebrew-cosmology commentary) |
| `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md:874` | Rowbotham's full title: "*…Proving It a Plane, Without Axial or Orbital Motion; and the Only Material World in the Universe.*" | SCAFFOLDING (bibliography) — an explicit denial of plural worlds |

### (d) "Star" not astronomical

| Path:line | Verbatim | Voice |
|---|---|---|
| `sol-luna/Rudhyar_Zodiac_As_Process.md:78`; `source-extracts/Dane_Rudhyar/pulse-of-life.md:108` | "The new star asserts his right before the foot-lights of the human consciousness. Henceforth, the show will be his." | QUOTED (Rudhyar, "ARIES") — theatrical sense |
| `source-extracts/Hesiod_Homeric_Hymns/hymn-31-to-helios.md:5`; `theogony-sun-moon-dawn.md:10` | "the Son of Earth and starry Heaven"; "Astraeus (Starry)" | QUOTED / SCAFFOLDING — Ouranos epithet and Titan name |

### (e) "Worlds" = Sanskrit *loka*, not planets

`political/Poisonous_Music.md:11`; `chloride/Inorganic_Minerals.md:27`;
`chloride/Leaving_the_Chloridics.md:54`;
`personal/Physical_Mortality_and_Essential_Immortality.md:33, 204, 253`;
`research_yoga_ayurveda_lineage/01_vedic_origins.md:157, 159, 339, 442, 547`;
`research_yoga_ayurveda_lineage/07_upanisadic_common_ground.md:317`;
`sol-luna/Sidereal.md:114` ("The Sun has yoked his seven steeds; with them he encircles
the worlds"); `source-extracts/Upanisads/death-and-the-imperishable-self.md:138`;
`source-extracts/Agni_and_Tapas.md:37` ("Agni is the courier between worlds").
All are the three-loka / worlds-gained-by-action idiom.

### (f) "Worlds" in a cited book title

`cosmology/All_Instruments_Measure_a_Level_Earth.md:184` and
`source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md:795–847, 887` —
Robert Schadewald, *Worlds of Their Own* (17 occurrences, all attribution lines).

### (g) "Planets" = the visible planets

`source-extracts/Damar_Tantra/quotes.md:67, 75` ("lived as the moon and the planets…",
"as the moon and the planets exist"); all `sol-luna/` and `Dane_Rudhyar/` uses of
"planet" are the classical seven/ten chart bodies.

### (h) The extraterrestrial reading explicitly rejected

`personal/Age_of_Saturation.md:5` — "the experience is often misinterpreted as contact
with 'aliens.' The error lies in the cultural vocabulary used to explain the
perception; the perception itself is sound." AUTHOR'S OWN PROSE. This is the only
"alien" in the repo and it declines the extraterrestrial frame.

### (i) Plural *universes* across time, not plural systems in space

`personal/Dharma_by_Annie_Besant.md:35, 39` — "In what does the perfection of a Universe
consist?"; "as He has chosen to condition Himself for this particular universe whose
birth-hour is come." QUOTED (Besant). Theosophical successive-manvantara plurality, not
simultaneous star systems. Same file as HIT 1, different claim.

## OBSERVATIONS — ADJACENT MATERIAL, OUTSIDE THIS CRITERION

Not reported as hits or near-misses because they concern heliocentrism / Earth-as-planet
rather than other suns. Recorded because the working-tree diff shows the prior pass was
also cutting material of this kind (it removed `practice-of-astrology.md`'s "Mars
*outside* the Earth's orbit, Venus *inside*; Mercury closest to the Sun" and
`astrology-of-personality.md`'s "even if it accepted some ideas belonging to the
heliocentric picture of the solar system"), so surviving instances may be of interest.

| Path:line | Verbatim (abridged) | Voice |
|---|---|---|
| `source-extracts/Arthur_Young/science-and-astrology.md:16` | "…before it was found that planets go around the sun rather than the sun and planets around the earth, and that the earth rotates and the celestial sphere does not." (Young then adds: "it does not matter to astrology which goes around which, since astrological measure depends only on angle") | QUOTED (Young) |
| `source-extracts/Dane_Rudhyar/astrological-houses.md:11`; repeated in `sol-luna/Rudhyar_Zodiac_As_Process.md:129` | "…and the second to the daily rotation of our globe around its polar axis" | QUOTED (Rudhyar) |
| `source-extracts/Dane_Rudhyar/astrological-houses.md:59` | "The 84-year cycle is that of Uranus' revolution around the Sun" | QUOTED (Rudhyar) |
| `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md:302, 502` | "…it was slowly deduced that the planet actually curved in all directions"; "…represent more closely the planet on which we live" | QUOTED (Ghilani/Wolf; geodesy texts) — verbatim opposing-tradition quotes, contra the project rule at `AGENTS.md:110` "Earth is not a planet" |
| `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md:575` | "…Philolaus … was also the first to propose a non-geocentric universe centred on Hestia (the central fire)." | QUOTED (Vaníček & Krakiwsky) |

## HYPOTHESES

Stated as hypotheses, not findings.

1. The prior pass appears to have been cutting a *broader* class than the criterion I
   was given — the working-tree diff removed heliocentric and Earth-as-planet material
   (`practice-of-astrology.md`, `astrology-of-personality.md`) alongside the plural-suns
   material (`astrological-houses.md`'s "Every Sun is isolated in space, the center of a
   group of planets"; "No Sun radiates life to its planets in empty space"). If that
   broader class is still the working intent, section "Adjacent material" above is the
   remaining surface. If the narrow criterion is the intent, HIT 1 is the only finding.
2. HIT 1 survived the prior pass most plausibly because `personal/Dharma_by_Annie_Besant.md`
   is a bulk-imported full text rather than a curated extract, and grep attention has
   been concentrated on `sol-luna/`, `cosmology/`, and `source-extracts/Dane_Rudhyar/`.
   Unverified — I did not inspect the commit history of the prior pass.
3. The Theosophical lineage is the likeliest carrier of further plural-suns material if
   any more full texts are imported: Besant, Bailey (named at
   `source-extracts/Dane_Rudhyar/astrology-of-personality.md:5` as the dedicatee), and
   the Theosophical Publishing House imprint of *The Astrology of Transformation*
   (line 3 of that file). Rudhyar's own Theosophical foundation is stated at
   `_index.md:173`.

## UNKNOWNS

1. Whether the criterion intends Plutarch's inhabited-moon doctrine (UNCERTAIN C) to
   count as "other worlds". It is the single largest exposure in the repo if so, and
   irreducible if cut.
2. Whether "galaxy" as a container term (UNCERTAIN A, near-miss group (a)) is
   acceptable at all, or acceptable only when Sol is not being placed inside it.
3. Whether verbatim external texts (`Dharma_by_Annie_Besant.md`) and verbatim
   opposing-tradition quotes (`Surveying_Instruments_…`) are in scope for editing at
   all, or whether the scope is the project's own prose plus its scaffolding.
4. Whether `cosmology/Computing_vs_Measuring_The_Curve.md` (deleted in the working tree,
   still present at HEAD) is intended to stay deleted. Its arc-measurement argument
   contained "Because a star's rays arrive parallel at both stations — stars are far,
   which stellar parallax independently establishes" and "A single near source causing
   the angle by perspective would give different stations different values" — stellar
   distance and parallax as measured facts. That file is out of the current working
   tree, so it is not a hit; noted only so the deletion is not reverted unknowingly.
