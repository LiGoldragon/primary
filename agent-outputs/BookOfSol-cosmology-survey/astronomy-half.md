# The Book of Sol — Cosmology Survey, Astronomy Half

Read-only survey. No edits were made to the book.

Repo: `/home/li/primary/repos/TheBookOfSol`
Surveyed: `sol-luna/`, `cosmology/`, `source-extracts/` (all subdirs), `research_yoga_ayurveda_lineage/`, `yoga-tantra/`, `teasers/`
Date: 2026-07-22

All paths below are repo-relative to `/home/li/primary/repos/TheBookOfSol`.

Axis key:
- **A** — curved/spherical earth; earth in motion; heliocentrism; earth as a planet; gravity as mass-attraction shaping a ball; geoid/ellipsoid; axial tilt of a rotating globe as CAUSE.
- **B** — open unbounded space, no firmament; physical escape from earth (rockets, satellites, space travel, moon landings, "outer space", other worlds as destinations).
- **C** — ambiguous astronomical vocabulary readable either way ("solar system", "celestial sphere", bodies "orbiting", precession as wobbling globe axis, eclipse geometry via a spherical earth's shadow).

*(This file was written incrementally during the survey; sections appear in survey order.)*

## OBSERVATIONS — HITS BY FILE

### `cosmology/Computing_vs_Measuring_The_Curve.md` (54 lines)

**Whole-file finding: the entire premise of this file rests on axis A.** It is a working note whose stated purpose is to defend the measured reality of the earth's curvature against the objection that curvature is only assumed. It argues the orthodox geodetic position throughout, in the author's own unhedged prose.

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 1 | 9 | "The answer is that the curvature is measured first, by a procedure whose result could have come back flat, and only then used in the survey formulas." | A | AUTHOR'S OWN PROSE |
| 2 | 9 | "Below: how it is measured, how the large-area method uses it, and how the leveling correction is checked against a measurement that assumes nothing about the earth's shape." | A | AUTHOR'S OWN PROSE |
| 3 | 11 | "## Part 1 — How the curve is measured: arc measurement" | A | SCAFFOLDING (heading) |
| 4 | 13 | "This is the procedure that returns the earth's radius R as an observed number." | A | AUTHOR'S OWN PROSE |
| 5 | 18 | "Because a star's rays arrive parallel at both stations — stars are far, which stellar parallax independently establishes — Δφ is the angle between the two local plumb lines, i.e. how much 'down' has rotated between the two points." | A | AUTHOR'S OWN PROSE |
| 6 | 21 | "The result is empirical, and the experiment could have returned flat. On a flat earth the plumb line points the same direction everywhere: Δφ = 0 for any S, and R is infinite. The measured Δφ is not zero — about one degree per 111 km — so R comes out near 6,371 km. A distance and an angle, divided, yield the curvature." | A | AUTHOR'S OWN PROSE |
| 7 | 21 | "This was done by Eratosthenes, then with instruments by the French, Lapland, Peru, and Great Indian arcs and the Struve arc; the difference between the Lapland and Peru values measured the earth's *oblateness*, a finer result still." | A | AUTHOR'S OWN PROSE |
| 8 | 23 | "Robustness against the 'near light source' alternative: every star, regardless of which one, returns the same Δφ for the same two stations. That is what parallel rays over a rotated plumb line give." | A | AUTHOR'S OWN PROSE |
| 9 | 25 | "## Part 2 — The large-area method uses the measured R" | A | SCAFFOLDING (heading) |
| 10 | 34 | "Reduce each triangle to the reference spheroid: compute its spherical excess ε = area / R² and apply Legendre's theorem (subtract ε/3 from each angle), or solve directly by spherical trigonometry" | A | AUTHOR'S OWN PROSE |
| 11 | 36 | "Carry geodetic positions station to station by the ellipsoidal direct problem, starting from the datum origin." | A | AUTHOR'S OWN PROSE |
| 12 | 40 | "The measured R enters at steps 6–8 — the trigonometry that turns angles into sides and positions is spheroidal. Put R = ∞ (a flat earth) into the same raw observations and two measured checks fail: the triangle angle-sums, observed above 180°, will not reconcile, and the verification base will not match. The flat computation breaks its own checks, and those checks are measurements." | A | AUTHOR'S OWN PROSE |
| 13 | 44 | "Curvature drop from geometry: an instrument's horizontal sight is tangent to the level surface; at distance D the surface has fallen by" | A | AUTHOR'S OWN PROSE |
| 14 | 46–48 | "c = √(R² + D²) − R ≈ D² / (2R), which with the measured R (3,959 mi) gives c = 0.667 D² feet" | A | AUTHOR'S OWN PROSE |
| 15 | 50 | "The measured (c − r) matches the geometric 0.574 D². The correction is therefore tied to an observation that presupposes nothing about the earth's figure." | A | AUTHOR'S OWN PROSE |
| 16 | 54 | "Measure R by arc measurement — the rotation of the plumb line per unit ground distance, an angle that could read zero and does not. Then use R in the survey formulas." | A | AUTHOR'S OWN PROSE |
| 17 | 54 | "The curve is re-measured independently by the triangle excess and by reciprocal leveling, both of which return the same figure." | A | AUTHOR'S OWN PROSE |

**Separability:** IRREDUCIBLE for the file as a whole. Every one of the three parts (arc measurement, geodetic triangulation, leveling correction) exists solely to establish that the curvature is an observed quantity. Removing the curvature assertions leaves no note. What would be lost: the entire steelman of the orthodox position — the arc-measurement argument (Δφ ≠ 0), the spherical-excess-and-verification-base check, and the reciprocal-leveling check.

**Breakage verified:** `cosmology/Horizon_Dip_vs_Altitude.md` line 56 refers to "the spherical excess," and `All_Instruments_Measure_a_Level_Earth.md` line 152 refers to "the 'spherical excess' of long triangles that is offered as curvature caught in the act" — both are the topic this file develops. No file in the surveyed half hyperlinks to `Computing_vs_Measuring_The_Curve.md`; a grep for its filename across the repo returns only the file itself. So deleting it breaks no link.

### `cosmology/Horizon_Dip_vs_Altitude.md` (56 lines)

Mixed file. It calculates the globe model's predicted horizon dip in order to set up a discriminating measurement. The globe geometry is stated modally ("on the globe model", "on a sphere of radius R") but is developed at length and the numbers are asserted as the globe's genuine prediction. Some sentences slip from modal to declarative.

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 18 | 9 | "The question is exact and answerable: on the globe model, by how much should the horizon fall below true level as the observer climbs — from the beach, from a hill, from a mountain, from a jet — and how does that prediction sit against the observation that the horizon reads level to the eye at every altitude." | C | AUTHOR'S OWN PROSE |
| 19 | 13 | "On a sphere of radius R, an observer at height h sees the horizon along the line of sight that grazes the surface — the tangent. The angle by which that tangent falls below level is the *dip*." | C | AUTHOR'S OWN PROSE (modal — "on a sphere") |
| 20 | 15 | "The observer A sits at distance R + h from the center O. The line of sight touches the sphere at the horizon point H, where the radius OH meets the tangent at a right angle." | C | AUTHOR'S OWN PROSE (modal) |
| 21 | 23 | "Taking R = 6,371 km:" | C | AUTHOR'S OWN PROSE |
| 22 | 27–40 | The dip table: twelve rows of "Vantage / Height h / Dip below level" from "Beach, standing eye 1.7 m 2.5′" to "Stratospheric balloon 30,000 m 5.5°" | C | SCAFFOLDING (table) |
| 23 | 48 | "On the globe model the beach horizon (eye ~1.7 m) sits 2.5 arc-minutes, or 151 arc-seconds, below level." | C | AUTHOR'S OWN PROSE (modal) |
| 24 | 50 | "So the picture a believer in the globe is sometimes saddled with — that from an airliner window one ought to see the earth visibly bow into a ball — is wrong on the globe's own arithmetic. The genuine prediction is a few degrees of dip" | C | AUTHOR'S OWN PROSE (modal) |
| 25 | 52 | "The indirect evidence on record is the dip correction of celestial navigation: a nonzero dip that grows as √h, subtracted from every sextant sight, which makes the computed fix come out right and would spoil it if the horizon stood at level." | A | AUTHOR'S OWN PROSE — **declarative, not modal**; asserts the dip correction is real and works |
| 26 | 56 | "The dip and the spherical excess are the same animal. Both are curvature signatures that are minuscule at the scale of ordinary human experience and only climb above the floor — the floor of perception for the dip, the floor of instrument error for the excess — at altitude or over great distance." | A | AUTHOR'S OWN PROSE — **declarative**; asserts curvature signatures exist |
| 27 | 56 | "At the beach, and in the small triangle, the curvature term is below the noise and the world reads flat honestly." | A | AUTHOR'S OWN PROSE — declarative |
| 28 | 56 | "It only shows where the seam is, and that everywhere below it the flat reading is exactly what the globe model predicts." | C | AUTHOR'S OWN PROSE |

**Separability:** Hits 18–24 are IRREDUCIBLE as a class — the file's entire content is the globe-model dip calculation; removing it leaves the title and nothing else. Hits 25, 26, 27 are SEPARABLE: each is a single declarative sentence that could be re-cast modally ("on the globe model, …") without touching the calculation, the table, or the concluding call for a plumb-levelled measurement at altitude.

**Breakage verified:** Line 9 hyperlinks out to `./All_Instruments_Measure_a_Level_Earth.md`; nothing links in to this file (grep for `Horizon_Dip` across the repo returns only this file). Removing the whole file breaks no inbound link; removing hits 18–24 orphans the headings "## The geometry", "## The numbers (pure geometry, no refraction)", and "## The comparison".

### `cosmology/All_Instruments_Measure_a_Level_Earth.md` (188 lines)

**This file already argues the level fixed earth** (see the category-2 register at the end of this report). Its author's-own-prose is uniformly zetetic. The globe-asserting material in it is present only as adversarially quoted orthodox sources — quoted precisely so the article can argue against them. Recorded here because the sentences literally assert axis A, per the over-report instruction.

| # | Line | Verbatim (anchor) | Axis | Voice |
|---|---|---|---|---|
| 29 | 18 | "In plane surveying, except for leveling, the reference base for fieldwork and computations is assumed to be a flat horizontal surface." | C (the word *assumed* presupposes non-flat) | QUOTED — Ghilani and Wolf, *Elementary Surveying* |
| 30 | 34 | "That type of surveying in which the mean surface of the earth is considered as a plane, or in which its spheroidal shape is neglected, is generally defined as plane surveying…" | A | QUOTED — Davis, Foote, Anderson, Mikhail |
| 31 | 39 | "The curvature of the Earth is ignored and all points on the physical surface are orthogonally projected onto a flat plane… For areas less than 10 km square the assumption of a flat Earth is perfectly acceptable." | A | QUOTED — Schofield and Breach |
| 32 | 42 | "In surveys of limited extent, the Earth may be assumed to be flat, and plane trigonometry used to define position." | A | QUOTED — Schofield and Breach |
| 33 | 47 | "plane survey. A survey that ignores the curvature of the Earth." | A | QUOTED — Kavanagh and Slattery |
| 34 | 50 | "…the surface of the Earth is considered to be a plane for all X (easterly) and Y (northerly) dimensions." | C | QUOTED — Kavanagh and Slattery |
| 35 | 53 | "The curved earth is reserved — by the books' own account — for the rare survey 'covering extensive areas,' for state and national boundaries, for the geodesist's specialty." | C | AUTHOR'S OWN PROSE (reporting the books) |
| 36 | 115 | "A level surface is a curved surface every element of which is normal to a plumb line." | A | QUOTED — Davis et al. |
| 37 | 118 | "Level surface. A curved surface that at every point is perpendicular to the local plumb line… Level line. A line in a level surface — therefore, a curved line." | A | QUOTED — Ghilani and Wolf |
| 38 | 121 | "A level line or level surface is one which at all points is normal to the direction of the force of gravity as defined by a freely suspended plumb-bob… such surfaces are ellipsoidal in shape." | A | QUOTED — Schofield and Breach |
| 39 | 130 | "Assuming a mean radius of the earth of 3959 mi or 6371 km, the curvature correction is c = 0.667 M² feet…" | A | QUOTED — Davis et al. |
| 40 | 133 | "Corr. for curv. and refr. (in feet) = 0.574 × (distance in miles)²." | A | QUOTED — Breed and Hosmer |
| 41 | 144 | "…For though the refraction may at a mean compensate for about a seventh of the curvature of the earth, it sometimes exceeds a fifth…" | A | QUOTED — *Encyclopaedia Britannica*, "Levelling", via Rowbotham |
| 42 | 149 | "Recent investigation has shown that not only can K vary from −2.3 to +3.5 with values over ice as high as +14.9, but it also has a daily cycle…" | C (refraction coefficient presupposes the curvature it offsets) | QUOTED — Schofield and Breach |
| 43 | 152 | "Even the instrument's famous betrayer, the 'spherical excess' of long triangles that is offered as curvature caught in the act, Rowbotham referred to the optics of the lens…" | C | AUTHOR'S OWN PROSE (naming an orthodox claim in order to reject it) |
| 44 | 161 | "On a globe each successive flag past the line of sight must drop below the last by the squared law, the seventh standing more than sixteen feet beneath the line." | C (counterfactual) | AUTHOR'S OWN PROSE |
| 45 | 180 | "**Geodesy.** Petr Vaníček and Edward J. Krakiwsky, *Geodesy: The Concepts*… Wolfgang Torge and Jürgen Müller, *Geodesy*… Weikko A. Heiskanen and Helmut Moritz, *Physical Geodesy*…" | C | SCAFFOLDING (references list) |

**Separability:** For hits 29–42, IRREDUCIBLE as a class within this article's argument. The article's central move in §II, §IV and §V is *"the orthodox books concede it themselves"*; the concession is the quotation. Remove the quoted curvature language and §II ("What the Books Concede"), §IV ("The Word 'Level'") and §V ("The Curve No Instrument Supplies") lose the object they are arguing against. Individually each quotation is SEPARABLE only in the sense that a shorter excerpt could be used; the curvature word is the load-bearing word in each. Hits 35, 43, 44, 45 are SEPARABLE.

**Breakage verified:** Line 186 hyperlinks to `../source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md` ("The complete verbatim extraction from all of these sources… is gathered in the companion file"), and `cosmology/Horizon_Dip_vs_Altitude.md` line 9 hyperlinks back into this file. Removing hit 45 (the Geodesy references block) leaves the References section's three-part structure ("Surveying textbooks / Geodesy / Zetetic primary sources") with a hole but breaks no link. Removing §V would orphan the closing epigraph at line 188, "*The curve lives in the calculation. The level lives in the glass.*", which restates §V's thesis.

### `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md` (888 lines)

**Whole-file finding.** This is a documentary compendium that deliberately quotes both traditions at length. Roughly half its bulk — §V (Surveying Textbooks, lines 296–565), §VI (Geodesy Texts, 566–737), plus parts of §II, §VII and §VIII — consists of verbatim orthodox passages that assert a spheroidal, rotating, gravitationally-shaped earth. This is by design: the file's Frame (line 5) states "both traditions are quoted at length on the terms each uses; the texts are left to speak."

**Method note for this file.** An exhaustive sentence-by-sentence verbatim transcription would reproduce most of the file. Below: (a) the author's-own-prose and scaffolding hits transcribed in full; (b) a complete line-indexed inventory of the quoted-external hits with a verbatim anchor clause each, so that every hit is individually recoverable by line number.

#### (a) Author's own prose / scaffolding hits in this file

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 46 | 300 | "Ghilani and Wolf's standard 14th-edition American surveying textbook opens with a brief historical narrative situating the round-earth conclusion against the flat-earth assumption of earlier peoples." | C | AUTHOR'S OWN PROSE (editorial frame) |
| 47 | 516 | "The 1947 textbook treats the earth as a Clarke 1866 spheroid and quantifies the combined curvature-and-refraction correction in the language used for decades by U.S. surveyors." | A | AUTHOR'S OWN PROSE (editorial frame) |
| 48 | 570 | "Vaníček and Krakiwsky open with the historical pre-Pythagorean cosmologies and trace the discipline through Eratosthenes to the modern ellipsoid." | C | AUTHOR'S OWN PROSE (editorial frame) |
| 49 | 624 | "Torge and Müller (4th ed., 2012) present the canonical modern framework." | C | AUTHOR'S OWN PROSE (editorial frame) |
| 50 | 863 | "The physical surface of the earth is irregular and mathematically intractable. A particular gravitational equipotential surface — the geoid — coincides approximately with mean sea level extended through the continents. A biaxial ellipsoid of revolution, flattened at the poles, approximates the geoid to within tens of meters; GRS80 (a = 6,378,137 m, 1/f = 298.257) is the modern global best-fit ellipsoid." | A | AUTHOR'S OWN PROSE — declarative, no attribution marker on these three sentences, though the paragraph opens with the reporting clause "On the question of how the geodesy texts treat reference surfaces and curvature, the modern geodetic tradition is uniform across…" |
| 51 | 863 | "All three texts trace this conception back to Eratosthenes (and through Aristotle and Pythagoras), and all three present the historical narrative as a progression from earlier disk-, cylindrical-, and spherical-earth models to the modern ellipsoidal-with-geoid framework." | C | AUTHOR'S OWN PROSE (reporting) |
| 52 | 865 | "The textbook reading: that the practicing surveyor's use of those same procedures is a deliberate small-area approximation against a curved reference surface, an approximation that becomes unacceptable past a defined extent and is supplemented in the long-distance case by curvature corrections, spherical-excess corrections, projections, geodetic ellipsoidal computation, and reference-surface mathematics." | C | AUTHOR'S OWN PROSE (reporting) |
| 53 | 867 | "The surveying-textbook tradition has likewise not changed its central explanatory framework — plane surveys assume a flat horizontal reference surface within defined extents; geodetic surveys take the earth's curvature into account by computing on an ellipsoid; the geoid is the physically defined equipotential surface to which orthometric heights refer" | C | AUTHOR'S OWN PROSE (reporting) |
| 54 | 296 | "## V. Surveying Textbooks on the Shape-of-the-Earth Question" | C | SCAFFOLDING (heading) |
| 55 | 566 | "## VI. Geodesy Texts on Reference Surfaces" | C | SCAFFOLDING (heading) |
| 56 | 878–885 | Bibliography entries for Ghilani & Wolf, Davis et al., Schofield & Breach, Kavanagh & Slattery, Breed & Hosmer, Vaníček & Krakiwsky, Torge & Müller, Heiskanen & Moritz | C | SCAFFOLDING (source list) |

**Separability (a):** Hits 46, 48, 49, 51, 52, 53, 54, 55 are SEPARABLE — reporting-frame sentences that can be reworded without loss. Hit 47 is SEPARABLE (the clause "treats the earth as a Clarke 1866 spheroid" is descriptive of the source). Hit 50 is SEPARABLE with a marker ("these texts hold that…"), and the content survives as reported speech. Hit 56 is IRREDUCIBLE if the corresponding quotations remain — removing a bibliography entry while keeping quotes from that book leaves the quotes uncited.

#### (b) Quoted-external hits — complete line inventory

All entries below are **QUOTED EXTERNAL SOURCE**, named. Axis is A unless marked.

**§I — Rowbotham quoting *Encyclopaedia Britannica*, "Levelling"**
- L26 — "This is owing to the globular figure of the Earth, and this rising is the difference between the true and apparent levels; the curve of the Earth being the true level" — A — *Encyclopaedia Britannica* via Rowbotham
- L27 — "For though the refraction may at a mean compensate for about a seventh of the curvature of the earth" — A — same

**§II — Alfred Russel Wallace, *My Life* Vol. II**
- L64 — "whereas, if the six-mile surface of the water is convexly curved, then the top disc would appear to be decidedly higher than the black band, the amount due to the known size of the earth being five feet eight inches" — A
- L73 — "shows that the surface of the water did not merely slope down in a straight line, but was curved downwards with regard to its surface at the starting-point" — A
- L76 — "proved that the curvature was very nearly of the amount calculated from the known dimensions of the earth" — A

**§V.1 — Ghilani and Wolf, *Elementary Surveying*, 14th ed.**
- L302 — "by noting the Earth's circular shadow on the moon during lunar eclipses and watching ships gradually disappear as they sailed toward the horizon, it was slowly deduced that the planet actually curved in all directions" — A + C (eclipse geometry via a spherical earth's shadow; "the planet")
- L305 — "the Earth approximates an oblate spheroid having an equatorial radius about 13.5 mi longer than the polar radius" — A
- L310 — "In geodetic surveying, the curved surface of the Earth is considered by performing the computations on an ellipsoid… a 3D, Earth-Centered, Earth-Fixed (ECEF) Cartesian coordinate system" — A
- L313 — "For areas of limited size, the surface of our vast ellipsoid is actually nearly flat." — A
- L318 — "Level surfaces are approximately spheroidal in shape." / "Level line. A line in a level surface — therefore, a curved line." — A
- L321 — "Geoid. A particular level surface that serves as a datum for all elevations and astronomical observations." — A
- L326 — "the horizontal plane departs from a level surface because of curvature of the Earth" — A
- L329 — "the Earth's curvature would cause the reading to be read too high by length BD" — A
- L332 — "This is about one seventh the effect of curvature of the Earth, but in the opposite direction." — A
- L335 — "this is one of several reasons why trigonometric leveling has never been used in geodetic surveys" — C
- L340 — "Because of variations in the Earth's mass distribution and the rotation of the Earth, the geoid has an irregular shape. The ellipsoid is a mathematical surface obtained by revolving an ellipse about the Earth's polar axis." + "With the advent of satellites, current-day ellipsoids provide a best fit for the Earth." — A + **B (satellites)**
- L343 — "Ellipsoids, which approximate the geoid and can be defined mathematically, are therefore used to compute positions of widely spaced points" — A
- L346 — "geodetic heights obtained with satellite surveys are measured with respect to the ellipsoid" — A + **B (satellite surveys)**

**§V.2 — Davis, Foote, Anderson, Mikhail, *Surveying: Theory and Practice*, 6th ed.**
- L353 — "The earth has the approximate shape of an oblate spheroid of revolution, the length of its polar axis being somewhat less than that of its equatorial axis." — A
- L356 — "Imagine the earth as shrunk to the size of a billiard ball… it would appear to the eye as a smooth sphere, and only by precise measurements could its lack of true sphericity be detected." — A
- L359 — "The surface of this imaginary spheroid is a curved surface every element of which is normal to the plumb line." — A
- L362 — "As to whether the surveyor must regard the earth's surface as curved or may regard it as plane… depends upon the character and magnitude of the survey" — A
- L365 — "That type of surveying which takes into account the true shape of the earth is defined as geodetic surveying… the required precision may be obtained by assuming that the earth is a perfect sphere. Where the area is large, as for a country, the true spheroidal shape of the earth is considered." — A
- L368 — "in which its spheroidal shape is neglected" — A
- L371 — "takes into account the shape of the earth in the location of certain of the primary lines of division" — C
- L374 — "Evidently, the curvature of the earth's surface is a factor that cannot be neglected in obtaining even very rough values of elevations." — A
- L377 — "A level surface is a curved surface every element of which is normal to a plumb line… it is parallel with the mean spheroidal surface of the earth." — A
- L382 — "The vertical distance between the horizontal line and the level line is a measure of the earth's curvature." — A
- L385 — "Assuming a mean radius of the earth of 3959 mi or 6371 km, the curvature correction is c = 0.667 M² feet" — A
- L388 — "rays of light are refracted… towards the center of the earth" — A
- L397 — "The geoid is the figure of the earth considered as a sea level surface extended continuously through the continents." — A
- L400 — "A triangulation net having long sides theoretically should be solved as a series of spherical triangles… one-third of the spherical excess in the triangle." — A
- L403 — "the line of sight will be tangent to the earth at a distance of 5 km" — A
- L406 — "The geometric shape of the earth is a spheroid with a polar diameter about one-third of 1 percent shorter than the equatorial diameter." — A
- L409 — "Regardless of whether the earth is considered a sphere or spheroid, it is not possible to develop its surface exactly onto a plane, just as it is impossible to flatten a section of orange peel without tearing it." — A

**§V.3 — Schofield and Breach, *Engineering Surveying*, 6th ed.**
- L416 — "Such a surface would be closed and could be formed to fit the mean position of the oceans… This surface is called the geoid" — A
- L419 — "due to variations in the mass distribution within the Earth, the geoid… is still an irregular surface" — A
- L422 — "The simplest mathematically definable figure which fits the shape of the geoid best is an ellipsoid formed by rotating an ellipse about its minor axis… the curvature of the Earth is ignored" — A
- L425 — "the geoid deviates from the tangent plane by about 80 mm at 1 km or 8 m at 10 km from the point of contact" — A
- L428 — "such surfaces are ellipsoidal in shape" — A
- L439 — "the earth is assumed to be spherical with a radius of R:… c = D²/2R… c = 0.0785 D²" — A
- L442 — "the combined effect of curvature and refraction (c − r) is (6/7)(0.0785 D²)" — A
- L448 — "The line of sight therefore approximates to a circular arc of radius Rs roughly equal to 8R, where R is the radius of the Earth." — A
- L459 — "the effect of the Earth's curvature is such as to produce unacceptable distortion if treated as a flat surface" — A
- L462 — **"In the real world this is not true because the Earth is not flat but round, and being round it is not a sphere or any other regular mathematical figure."** — A (the most explicit orthodox assertion in the file)
- L465 — **"If the Earth was truly molten, of homogeneous density, and not affected by the gravity field of any external bodies and did not rotate on its own axis (once a day), then through considerations of gravitational attraction, the surface of the Earth would be fully described as a sphere. The main source of error in this idealized model is that which is due to the Earth's rotation. The centrifugal force at the equator acts in the opposite direction to that of gravitation and so the figure of the Earth is better described by an ellipse of rotation about its minor axis"** — A (rotation asserted as CAUSE; gravitational attraction shaping a ball)
- L468 — "an equipotential surface, approximately at MSL would be formed… Such a surface at MSL is called the 'geoid'." — A
- L471 — "An ellipsoid of rotation is the closest mathematically definable shape to the figure of the Earth… GRS80… semi-major axis 6 378 137.0 m, semi-minor axis 6 356 752.314 m" — A

**§V.4 — Kavanagh and Slattery, *Surveying with Construction Applications*, 8th ed.**
- L478 — "must have corrections made to the field measurements so that these measurements reflect the curved (ellipsoidal) shape of the Earth" — A
- L481 — "Modern surveys… utilizing satellite-positioning systems are geodetic surveys based on the ellipsoidal shape of the Earth" — A + **B (satellite-positioning systems)**
- L484 — "A vertical line is a line from the surface of the Earth to the Earth's center." / "A level surface is a curved surface parallel to the mean surface of the Earth." — A
- L487 — "the divergence between a level line and a horizontal line is quite small. For example, over a distance of 1,000 ft, the divergence is 0.024 ft" — A
- L490 — Table 4.1, "(c + r)" values by distance up to "1 mi / 0.574" — A (table)
- L496 — "its surface does not follow the surface of the ellipsoid; sometimes it is below the ellipsoid surface and other times above it" — A
- L499 — "With the advent of the Global Navigation Satellite Systems (GNSS)… all GNSS surveys… are now based on frameworks that cover the entire surface of the Earth, and they must take into account its ellipsoidal shape." — A + **B (GNSS satellites)**
- L502 — **"an Earth-mass-centered ellipsoid (GRS80 ellipsoid) that would represent more closely the planet on which we live… because of the slight bulging of the Earth near the equator. The bulge is caused by the Earth spinning on its polar axis."** — A (rotation asserted as CAUSE; "the planet on which we live")
- L505 — "plane survey. A survey that ignores the curvature of the Earth." — A
- L508 — "geodetic survey. A survey that reflects the curved (ellipsoidal) shape of the Earth." — A
- L511 — "geoid. A surface that is approximately represented by mean sea level (MSL), and is, in fact, the equipotential surface of the Earth's gravity field." — A

**§V.5 — Breed and Hosmer, *Higher Surveying*, 6th ed.**
- L518 — "The offset from the tangent to the curve, due to curvature of the earth and refraction combined, is about 0.57 feet for a point a mile away" — A
- L521 — "that point will appear lower than it really is on account of the earth's curvature" — A
- L524 — "the effect of curvature on the apparent elevation is equal to the square of the distance divided by the earth's diameter" — A
- L527 — "Corr. for curv. and refr. (in feet) = 0.574 × (distance in miles)²." — A
- L530 — "the line of sight between the tops of the two towers will just clear the intervening level surface" — C
- L539 — "If we imagine a plane tangent to the sphere at a point within the area to be surveyed… Any point on the sphere will be located on the plane at its correct distance from the tangent point" — A
- L545 — "the triangulation net is located on the surface of the spheroid. Since the earth's surface is not a true spheroid…" — A
- L548 — "The triangulation of the United States is computed on the surface known as the 'Clarke Spheroid of 1866'" — A
- L554 — "Until a few years ago it was assumed that a line of levels must necessarily follow the curve of sea level" — A
- L557 — **"On account of the spheroidal form of the earth and the action of centrifugal force, level surfaces at different elevations are not exactly parallel."** — A (centrifugal force presupposes rotation)
- L560 — "Any representation of a portion of a spherical surface on a plane is necessarily distorted… for very large areas, such as that of a continent or a hemisphere" — A

**§VI.1 — Vaníček and Krakiwsky, *Geodesy: The Concepts*, 2nd ed.**
- L575 — "The school of Pythagoras… was the first to believe in a spherical earth… Philolaus… was also the first to propose a non-geocentric universe centred on Hestia (the central fire)." — C (historical report; non-geocentric arrangement named)
- L578 — "The first hint at the possibility of gravity is due to Aristotle… who, in addition, formulated the first plausible argument for the sphericity of the earth, which survives till the modern day." — A
- L581 — "the size of the (then thought of as spherical) earth" — C
- L589 — "The lines of force of the earth's gravity field are called the plumb lines" — A
- L592 — "the equipotential surfaces define the horizontal direction; thus they are also called level surfaces" — C
- L595 — "All the equipotential surfaces make an oblate spatial pattern… reminiscent of a series of concentric ellipsoids… the plumb lines are also curved in all directions" — A
- L601 — "The one gravity equipotential surface of particular interest is that which best approximates the (mean) sea level over the whole earth. It is called the geoid." — A
- L604 — "the geoid can also be approximated… by a biaxial geocentric ellipsoid whose minor axis coincides with the earth's principal polar axis of inertia" — A
- L607 — "the geoid… closely represents the figure of the earth on 72% of the terrestrial globe" — A
- L610 — "Eratosthenes… assumed the earth to be spherical, i.e., f = 0, and derived the radius of the earth" — A
- L613 — "the departure of the best-fitting sphere from the best-fitting ellipsoid is about 10.7 km on the poles and on the equator" — A
- L616 — "the mean sea level… should theoretically coincide with the geoid" — A
- L619 — "Like trigonometrical determination, levelling is also affected by the earth's gravity field." — A

**§VI.2 — Torge and Müller, *Geodesy*, 4th ed.**
- L626 — "Global geodesy includes the determination of the shape and size of the Earth, its orientation in space, and its external gravity field… The Earth's curvature and gravity field must be considered in geodetic surveys." — A + **B ("its orientation in space")**
- L629 — "Because of its simple mathematical structure, a rotational ellipsoid, flattened at the poles, is well suited for describing horizontal positions" — A
- L635 — **"By the time of Aristotle (384–322 B.C.), the spherical concept was generally accepted and even substantiated by observations. For example, observers noted the round shadow of the Earth in lunar eclipses and the apparent rising of an approaching ship at the horizon."** — A + **C (eclipse geometry via a spherical earth's shadow)**
- L638 — "Eratosthenes of Alexandria… was the first who, based on the assumption of a spherical Earth, deduced the Earth's radius from measurements" — A
- L641 — "the Earth's radius is computed to be about 6300 km, which is close to the real value of 6370 km" — A
- L644 — **"Based on the law of gravitation, Newton proposed a rotational ellipsoid as an equilibrium figure for a homogeneous, fluid, rotating Earth."** — A (gravitation as mass-attraction shaping a rotating ball)
- L647 — "the ocean surface (70% of the Earth's surface)… forms a part of a level or equipotential surface of the Earth's gravity field… J. B. Listing (1873) designated this level surface as geoid." — A
- L650 — "Defined in 1828 by Gauss as the 'equipotential surface of the Earth's gravity field coinciding with the mean sea level of the oceans'" — A
- L653 — "the level surfaces are intersected at right angles by the plumb lines" — C
- L656 — "As a consequence of the gravity increase of 0.05 m s⁻² from the equator to the poles, the level surfaces of the Earth converge toward the poles" — A
- L659 — **"The level surfaces inside the Earth and in the exterior space are closed spheroidal surfaces… one may consider the level surface for which the gravitation and centrifugal acceleration in the equatorial plane cancel each other. The equatorial radius of this surface would be 42 200 km."** — A + **B ("in the exterior space")**
- L662 — "this includes the methods of satellite and terrestrial geodesy as well as geodetic astronomy" — **B (satellite geodesy)**
- L671 — "the assumption of an ellipsoidal-Earth model is no longer tenable at a high level of accuracy… the geoid as the mathematical surface, and the ellipsoid as a reference surface approximating it" — A
- L674 — "Heights were referred to a level surface close to the geoid" — A

**§VI.3 — Heiskanen and Moritz, *Physical Geodesy***
- L687 — "The surface of the oceans is, after some slight idealization, part of a certain level surface. This particular equipotential surface was proposed as the 'mathematical figure of the earth' by C. F. Gauss… and was later termed the geoid." — A
- L690 — "The lines that intersect all equipotential surfaces normally are not exactly straight but slightly curved… They are called lines of force, or plumb lines." — A
- L693 — "The height H of a point above sea level… is measured along the curved plumb line, starting from the geoid" — A
- L699 — **"As a first approximation the earth is a sphere; as a second approximation it may be considered an ellipsoid of revolution."** — A (most compact orthodox assertion in the file)
- L702 — "We therefore assume that the normal figure of the earth is a level ellipsoid, that is, an ellipsoid of revolution which is an equipotential surface of a normal gravity field." — A
- L705 — "The reference ellipsoid and its gravity field are completely determined by four constants" — A
- L708 — "The distance PQ between geoid and ellipsoid is called the geoidal height, or geoidal undulation" — A
- L711 — "The reference surface is never a sphere in any geometrical sense, but always an ellipsoid." — A
- L729 — "the earth's gravity field, a physical entity, is inextricably involved in most geodetic measurements" — A
- L732 — "the deviations of the geoid from an ellipsoid must be taken into account… It is a complicated surface with discontinuities of curvature." — A
- L735 — "the physical surface of the earth can be determined from geodetic measurements alone, without using the density of the earth's crust" — C

**§VII — Linklater, *Measuring America***
- L742 — "the more exact science of Earth measurement or geodesy" — C
- L769 — **"The curvature of the earth brings lines of longitude gradually together as they run toward the pole, so that in most of the United States the northern end of a township is 30 to 40 feet narrower than the southern. In Alaska the flattening of the earth means that the lines close by more than 100 feet."** — A
- L778 — "A geodetic survey was so precise that it increased the supply of the world's knowledge about the shape of the earth" — C
- L784 — "The true distance from equator to pole, now reckoned to be 10,001,965.7 meters" — C
- L790 — "today even the global positioning systems and transits used by every amateur surveyor give measurements in metric units" — C (GPS named without naming satellites)

**§VIII — Schadewald, *Worlds of Their Own***
- L808 — "Walsh was satisfied that the experiment showed the Earth's curvature… By placing a tall marker in the middle and banners on both bridges, all at the same height above the water, the Earth's curvature could easily be seen. Even allowing for atmospheric refraction, the center marker should appear about five feet above the line of sight from banner to banner." — A
- L811 — "Most people would interpret that to mean that the Earth curves gently away from the observer… He had done precisely what he had set out to do, and had demonstrated the curvature of the Earth in a simple manner." — A
- L831 — "suggests mirage, which is the bending of light rays by temperature variations in the atmosphere" — C

**Separability (b):** IRREDUCIBLE, as a class and individually. The file's declared purpose (line 5) is verbatim documentary extraction of *both* traditions; every §V and §VI quotation is there because it asserts the curved earth, and the §IX synthesis is built entirely on comparing those assertions to the zetetic ones. Reword any of these and it is no longer a verbatim extract, which is the file's whole function. What is lost if they are cut: the "the textbooks concede plane surveying" argument in `cosmology/All_Instruments_Measure_a_Level_Earth.md` loses its evidentiary backing, since that article's line 186 points here as "the complete verbatim extraction."

**Breakage verified:** `cosmology/All_Instruments_Measure_a_Level_Earth.md` line 186 hyperlinks into this file: "The complete verbatim extraction from all of these sources — surveying, geodesy, and zetetic — is gathered in the companion file [*Surveying Instruments and the Shape of the Earth*](../source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md)". Deleting §V or §VI would falsify that sentence's claim to completeness and orphan the "Geodesy" block of that article's References (line 180), which lists Vaníček & Krakiwsky, Torge & Müller, and Heiskanen & Moritz — texts quoted *only* here, never in the article itself. §IX (lines 853–867) would also collapse: every paragraph in it quotes §V/§VI back.

### `sol-luna/` — general note

Astrological "planets" (grahas, the wandering lights: Sun, Moon, Mars…Saturn, Rāhu, Ketu) appear throughout this directory. In classical usage this word names visible wandering lights, not worlds, and does not by itself presuppose earth as one planet among others. Instances are therefore **not** itemized individually below unless the surrounding sentence pushes toward the modern sense. The affected files are `Celestial_Name.md` (lines 3, 54), `The_Solar_Matrix_of_Creation.md` (lines 16, 18, 50), `Rudhyar_Zodiac_As_Process.md` (lines 22, 125, 129, 138), `Sidereal.md` (lines 5, 8), `The_108_Solar_Divisions.md` (lines 766, 818, 836).

### `sol-luna/The_Toroidal_Heart.md` (185 lines)

**This file already argues the level fixed earth and an enclosing firmament** — see the category-2 register. Line 15: "The world is a torus. The level earth-disk lies within it. The north pole is at the center of the disk; the equator is a circle drawn around that center". Line 156: "the encircling southern firmament".

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 57 | 25 | "The Earth's magnetosphere flares out from the poles and folds back across the equator." | C (borrowed geophysical vocabulary; the sentence sits in a list of natural tori and does not state a shape) | AUTHOR'S OWN PROSE |
| 58 | 103 | "The Moon's orbit tilts five degrees off the ecliptic, so twice each month her path crosses the Sun's." | C ("orbit", "tilts") | AUTHOR'S OWN PROSE |
| 59 | 105, 107 | "Between Rāhu and Ketu — the half-orbit when the Moon stands north of the ecliptic…" / "Between Ketu and Rāhu — the half-orbit when the Moon stands south of the ecliptic…" | C ("half-orbit") | AUTHOR'S OWN PROSE |
| 60 | 122 | "3/4 × 2π × 4/3 πR³ = 2π²R³ — which is the formula for the Einstein-Eddington hypersphere. It is also the formula for the torus with an infinitely small hole." | C (hypersphere cosmology) | QUOTED — Arthur M. Young, *Science and Astrology* |
| 61 | 156 | "The solar system is a torus, and the galaxy is one larger torus that holds it." | C ("solar system", "galaxy") | AUTHOR'S OWN PROSE |
| 62 | 156 | "The solar system has the sun for a core and the heliopause for a skin." | C ("heliopause" — modern astrophysical boundary) | AUTHOR'S OWN PROSE |
| 63 | 158 | "The natal chart locates an individual body's core-and-skin within the world's core-and-skin within the solar system's core-and-skin — three scales pulsing in resonance" | C ("solar system") | AUTHOR'S OWN PROSE |
| 64 | 164 | "In the morning, with the sun rising on the eastern horizon and the moon somewhere on her own orbit" | C ("orbit") | AUTHOR'S OWN PROSE |

**Separability:** All eight SEPARABLE. Hits 58, 59, 64 could use "path" or "circuit" for "orbit" with no loss — the nodal argument depends on the Moon standing north or south of the ecliptic, not on the word *orbit*. Hit 57 is one item in a four-item list of self-organizing tori (plasma, heart, magnetosphere, cosmos); dropping it leaves three. Hits 61–63 are the "Nested Tori" section's middle rung; **note** that removing "the solar system" from hit 63 would break the section's stated *three*-scale count ("three scales pulsing in resonance, three Two-Lights"), so hits 61 and 63 must move together.

**Breakage verified:** hit 60's Arthur Young quotation supports the sentence immediately following it at line 125, "The cosmos is a torus with a vanishing throat," which opens the section "The Arc Through the Torus"; removing the quote leaves that claim unsupported. Line 11's image alt-text and `../generated-images/toroidal-heart-banner.png` describe a level earth-disk and are not hits.

### `sol-luna/Sidereal.md` (133 lines)

**This file already argues the level fixed earth** — see the category-2 register (lines 15–31, "Earth as the Stable Domain of Life").

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 65 | 35 | "The celestial sphere is the visible expression of this field: a luminous envelope carrying motion, rhythm, and return." | C ("celestial sphere" — named explicitly in the axis-C list; here it is glossed as an enclosing envelope, which reads toward firmament) | AUTHOR'S OWN PROSE |
| 66 | 5 | "From the Sun proceed the motions of the planets, and the regulation of their courses." | C | QUOTED — *Sūrya Siddhānta* I.6 (marked "working paraphrase; source extraction still needed") |
| 67 | 8 | "The Sun, impelled by its own power, draws after it the planets which are bound to it." | C | QUOTED — *Sūrya Siddhānta* II.9 (same marking) |

**Separability:** All three SEPARABLE. Hit 65's "celestial sphere" could read "celestial field" or "sky-envelope" and the paragraph's claim (a luminous envelope carrying motion) survives intact — the paragraph's own next sentence already calls it "this toroid". Hits 66–67 are working paraphrases the file itself flags as unverified at line 129 ("retained only as marked working paraphrases until a source extract records Sanskrit, translator, edition, and verse-level support").

**Breakage verified:** none. The three sentences carry no inbound reference. Line 133's References list is generic ("*Sūrya Siddhānta*") and would survive removal of either quotation.

### `sol-luna/Line_of_Sight.md` (48 lines)

**This file already argues the level fixed earth** — see the category-2 register. Line 38: "No curvature is ignored because none is ever encountered in reality."

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 68 | 7 | "When mapping over large regions requires spherical mathematics, those abstractions live entirely inside cartographic projections and coordinate bookkeeping" | C (concedes spherical mathematics is used, while denying it describes the ground) | AUTHOR'S OWN PROSE |
| 69 | 13 | "The curvature of the earth and the convergence of the meridians are ignored… In short, the tangent plane projection system accounts for the curvature of the earth by ignoring it…" | A | QUOTED — Stephen V. Estopinal, *A Guide to Understanding Land Surveys*, 3rd ed. (adversarially quoted) |
| 70 | 16 | "In plane surveying… the reference base for fieldwork and computations is assumed to be a flat horizontal surface… For areas of limited size, the Earth's surface can be approximated as a plane" | C | QUOTED — Ghilani & Wolf, *Elementary Surveying* (adversarially quoted) |
| 71 | 26, 28–34 | "the classroom '8 inches × miles²' formula is shown as the hypothetical deviation a curved model would demand" and the four bracketed figures "[Hypothetical drop ≈ 9,600 ft]", "[≈ 379 ft]", "[≈ 6,990 ft]", "[≈ 24 ft]" | C (explicitly labelled *hypothetical*) | AUTHOR'S OWN PROSE / SCAFFOLDING (list annotations) |

**Separability:** Hits 69–70 are IRREDUCIBLE within this file's argument — section "What the manuals and texts actually say" exists to display the orthodox concession, and line 19 comments directly on those two quotations ("These passages are often read as pragmatic shortcuts. Read literally, they describe the operational fact"). Removing them orphans line 19 and the section heading at line 11. Hit 68 SEPARABLE. Hit 71 SEPARABLE — the four long-span entries survive without their bracketed hypothetical drops, though line 26's framing sentence would then need removing too.

**Breakage verified:** removing hits 69–70 orphans the section heading at line 11 and leaves line 19's "These passages" with no antecedent. The References at lines 42–43 cite Estopinal and Ghilani & Wolf and would become dangling.

### `sol-luna/The_Solar_Matrix_of_Creation.md` (89 lines)

**This file already argues the fixed earth and an enclosing firmament** — line 25: "In the classical cosmology, the Earth stands motionless at the center of a vast, rotating firmament. Rudhyar's interpretation does not dispute that geometry."

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 72 | 27 | "Where Ptolemy spoke of a crystalline sphere and the *Sūrya Siddhānta* of a luminous ecliptic, Rudhyar spoke of *lines of force*" | C ("crystalline sphere" — celestial-sphere vocabulary, here reported of Ptolemy) | AUTHOR'S OWN PROSE (reporting) |
| 73 | 10 | "The zodiac traces to the Sun's motion along the ecliptic, a living cycle of ascent and descent above a stationary Earth." | *not a hit* — recorded here only because it is the file's explicit stationary-earth statement | — | AUTHOR'S OWN PROSE |

**Separability:** hit 72 SEPARABLE.
**Breakage verified:** none.

### `sol-luna/Rudhyar_Zodiac_As_Process.md` (151 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 74 | 129 | "When the modern astrologer speaks of these two frames of reference for the measuring of the motion of Sun, Moon, and planets he at once mentions that the first refers to the apparent yearly motion of the Sun around the zodiac... and **the second to the daily rotation of our globe around its polar axis**..." | **A** — an explicit rotating globe on a polar axis | QUOTED — Dane Rudhyar, *The Astrological Houses*, Part One, "Zodiacs and Houses" |

**Separability:** SEPARABLE. The quotation is used only to establish Rudhyar's zodiac/houses distinction; line 132 immediately restates that distinction in the book's own words ("The zodiac is the sky's cycle of formative qualities. The houses are the terrestrial circle of experience centered on the breathing person"), so the point survives without the quotation. Truncating the quotation mid-sentence would, however, cut the very clause that names the second frame of reference, which is half the distinction being drawn — so a shortened quote loses the contrast and only the surrounding paraphrase can carry it.

**Breakage verified:** line 151's Sources entry points to `source-extracts/Dane_Rudhyar/astrological-houses.md`; that extract file is where the same passage lives (see the source-extracts section below). Removing the quotation here does not break the Sources link, which is a general book reference.

### `sol-luna/Celestial_Name.md` (86 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 75 | 13 | "In *Poimandres*, the soul descends through the planetary spheres, taking on qualities that become its earthly pattern" | C ("planetary spheres" — celestial-sphere vocabulary) | AUTHOR'S OWN PROSE (introducing the quotation) |
| 76 | 15 | "The human being descends through the harmony of the spheres, and to each he leaves over a portion of his powers… thus he enters the body, having been stripped by the turning of the spheres." | C ("the turning of the spheres") | QUOTED — *Corpus Hermeticum* I (*Poimandres*) |

**Separability:** hit 75 SEPARABLE. Hit 76 IRREDUCIBLE as a quotation — the "spheres" are the passage's subject; what would be lost is the Hermetic descent-through-spheres doctrine on which the paragraph's claim ("The celestial name is this composite of intelligences", line 17) rests.

**Breakage verified:** removing hit 76 leaves line 17's "The celestial name is this composite of intelligences" with no antecedent for "this".

### `sol-luna/The_360_Phases_of_Sol.md` (456 lines)

Provenance stated at line 3: "the modern reading descends from the Sabian Symbols received by Elsie Wheeler for Marc Edmund Jones in 1925 and reinterpreted by Dane Rudhyar". The degree glosses are compressed paraphrases of Rudhyar's *An Astrological Mandala*, so voice throughout is PARAPHRASE OF QUOTED EXTERNAL SOURCE (Rudhyar) rendered in the book's own words.

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 77 | 44 | "**Aries 29°:** The music of the spheres; represents attunement to cosmic order." | C ("the spheres") | PARAPHRASE of Rudhyar/Sabian |
| 78 | 106 | "**Gemini 19°:** A large archaic volume reveals a traditional wisdom; signifies contacting the all-human planetary Mind." | C ("planetary Mind" — earth-as-planet adjective) | PARAPHRASE of Rudhyar/Sabian |
| 79 | 136 | "**Cancer 14°:** A very old man facing a vast dark space to the northeast; symbolizes fulfillment in transcending and changeless wisdom." | C ("a vast dark space" — reads toward open unbounded space; the image is symbolic, not cosmological) | PARAPHRASE of Rudhyar/Sabian |
| 80 | 163 | "**Leo 5°:** Rock formations tower over a deep canyon; symbolizes the structuring power of elemental forces during planetary evolution." | C ("planetary evolution" — earth-as-planet) | PARAPHRASE of Rudhyar/Sabian |
| 81 | 223 | "**Virgo 26°:** A boy with a censer serves the priest near the altar; symbolizes the first stage of actual participation in the great ritual of planetary evolution." | C ("planetary evolution") | PARAPHRASE of Rudhyar/Sabian |

**Separability:** All five SEPARABLE. Each is one degree-gloss in a 360-item list; the offending word is in the interpretive clause after the semicolon, never in the Sabian image itself, so the image survives a reworded gloss. Hit 77's image *is* "the music of the spheres" and cannot be reworded without changing the received symbol — call that one IRREDUCIBLE at the image level, SEPARABLE at the gloss level.

**Breakage verified:** none. The list is positional by degree; each entry stands alone.

### `sol-luna/The_108_Solar_Divisions.md` (931 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 82 | 213 | "- *Symbolizing a quiver of arrows, representing return, renewal, and boundless space.*" (Punarvasu nakṣatra gloss) | C ("boundless space") | AUTHOR'S OWN PROSE (nakṣatra gloss) |
| 83 | 535 | "The heart is hidden by the shadow of the earth, as it works patiently towards a magnificent and triumphant goal." (Vishakha Pāda 2 gloss) | C (shadow-of-the-earth phrasing could read as eclipse geometry; no shape is asserted and the sentence is symbolic) | AUTHOR'S OWN PROSE (pada gloss) |

**Separability:** both SEPARABLE — single interpretive clauses inside a 108-item list.
**Breakage verified:** none.

### `sol-luna/2-Luna.md` (61 lines) — marginal only

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 84 | 40 | "In Plutarch's composition doctrine, earth gives the body, moon gives the soul, and sun gives the mind (*De facie* 943A). The three bodies of the cosmos contribute to the human being as three ingredients." | C ("the three bodies of the cosmos" — earth grouped with sun and moon as a *body*) | AUTHOR'S OWN PROSE (reporting Plutarch) |
| 85 | 44, 46 | "Plutarch's elaboration of the moon-as-soul-threshold gives Luna two hemispheres (*De facie* 944C). The side that faces heaven is *Elysion pedíon*… The side that faces earth is *Phersephónēs oikos antichthonos*" / "The face Luna turns toward us is the earthward hemisphere… What we call the dark side is Elysium." | C (a moon with two hemispheres, one permanently turned away — bears on lunar not terrestrial shape) | AUTHOR'S OWN PROSE (reporting Plutarch) |

**Separability:** both SEPARABLE — hit 84's second sentence is a gloss that can be dropped; hit 85 is the "She has two faces" section and is IRREDUCIBLE *within that section* (the section is entirely about the two hemispheres), but SEPARABLE at file level.
**Breakage verified:** removing the whole "She has two faces" section (lines 42–46) orphans nothing; the "Salutation" at line 58 does contain "double-faced world between two worlds", which restates it and would lose its antecedent.

### `sol-luna/` — zero-hit files

`1-Sol.md`, `Kali_Yuga.md`, `Solar_Excess.md`, `The_Zodiac.md`. Read in full; no passage asserts or presupposes A, B, or C. (`The_Zodiac.md` uses "axis" once, at line 17, in the sense of a unifying principle of thought, not an axis of rotation.)

### `source-extracts/Arthur_Young/science-and-astrology.md` (300 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 86 | 14 | "Young opens by refusing the framing that pits the two as rivals on the same question. The geocentric/heliocentric correction has nothing to do with astrology, whose measure depends only on angle." | **A** — "the geocentric/heliocentric correction" is stated as a settled fact in the book's own editorial voice | AUTHOR'S OWN PROSE (editorial frame) |
| 87 | 16 | "To the modern mind astrology is dismissed as superstition, a delusion of the prescientific age **before it was found that planets go around the sun rather than the sun and planets around the earth, and that the earth rotates and the celestial sphere does not**. Strictly speaking, it does not matter to astrology which goes around which, since astrological measure depends only on angle, but the earlier geocentric view had become associated with astrology and **when the geocentric view was proved false**, astrology dropped out of fashion." | **A** (heliocentrism, earth rotation, both asserted as established) + **C** ("celestial sphere") | QUOTED — Arthur M. Young, *Science and Astrology* |
| 88 | 230 | "3/4 × 2π × 4/3 πR³ = 2π²R³ — which is the formula for the Einstein-Eddington hypersphere. It is also the formula for the torus with an infinitely small hole, which I have dealt with in *The Reflexive Universe*." | C (hypersphere cosmology) | QUOTED — Arthur M. Young |

**Separability:** hit 86 SEPARABLE (could be reported as Young's own claim rather than stated flat). Hits 87 and 88 IRREDUCIBLE as quotations — hit 87 is the single most explicit heliocentric-plus-rotating-earth statement anywhere in the surveyed half, and it is also the passage whose *point* is that astrology does not depend on the answer. What would be lost if cut: Young's whole "the conflict is ideological, not factual" opening move (section I), which turns on conceding the astronomical correction and denying its relevance.

**Breakage verified:** hit 88 is the same passage quoted in `sol-luna/The_Toroidal_Heart.md` line 122; the article there builds its section "The Arc Through the Torus" on it. Removing hit 87 orphans section heading "## I. The conflict is ideological, not factual" (line 12) and the two paragraphs that follow it.

### `source-extracts/Plutarch_De_Facie/passages.md` (61 lines)

The moon in Plutarch is a *place* with terrain, and souls travel to it. This is ancient psychic cosmology, not modern space travel; recorded here because the axis-B wording ("other worlds as physical destinations") covers it on a literal reading.

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 89 | 9 | "…has got open regions of marvellous beauty and mountains flaming bright and has zones of royal purple with gold and silver not scattered in her depths but bursting forth in abundance on the plains or openly visible on the smooth heights." | C (moon as a terrained world); B on a literal reading | QUOTED — Plutarch, *De facie* 935C, trans. Cherniss |
| 90 | 12 | "…she is held by men to be a (celestial and) holy earth rather than, as the Stoics say, a fire turbid and dreggish." | C | QUOTED — Plutarch, *De facie* 935D |
| 91 | 17 | "…but just as our earth contains gulfs that are deep and extensive… so those features are depths and hollows of the moon." | C (earth–moon analogy as bodies) | QUOTED — Plutarch, *De facie* 944B–C |
| 92 | 38 | "When the soul has been separated from the body and must wander in the region between earth and moon…" | C | QUOTED — Plutarch, *De facie* 943C |
| 93 | 43 | "For the souls pass through them [the moon's hollows], now to the side of the moon that faces heaven, now back again to the side that faces earth." | C (a moon with fixed near and far faces) | QUOTED — Plutarch, *De facie* 944C |
| 94 | 53 | "The human being is a Sun-Moon-Earth composite and disassembles back into those three." | C (earth grouped with sun and moon as one of three cosmic bodies) | AUTHOR'S OWN PROSE (editorial note) |
| 95 | 56 | "Luna has substance, weight, locus — a world." | C; B on a literal reading | AUTHOR'S OWN PROSE (editorial note) |
| 96 | 60 | "Plutarch's phrase *Phersephone antichthonos* — Persephone who is *counter-earth* — places Luna as the mirror-below-heaven of the earth-below-heaven. **The moon is another earth, reversed.**" | C; B on a literal reading | AUTHOR'S OWN PROSE (editorial note) |

**Separability:** hits 89–93 IRREDUCIBLE — they are the verbatim extract, and the file exists to hold Plutarch's exact words. Hits 94–96 SEPARABLE (editorial notes, restatable).
**Breakage verified:** hit 93 is the passage `sol-luna/2-Luna.md` lines 44–46 and `sol-luna/The_Toroidal_Heart.md` line 70 both draw on; removing it leaves those articles' "two faces" material without a source. Hit 96's "counter-earth" gloss is picked up verbatim in `The_Toroidal_Heart.md` line 70 ("the house of counter-earth Persephone").

### `source-extracts/Dane_Rudhyar/astrological-houses.md` (131 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 97 | 11 | "…and **the second to the daily rotation of our globe around its polar axis**…" | **A** | QUOTED — Rudhyar, *The Astrological Houses*, "Zodiacs and Houses" |
| 98 | 54 | "These correspond to three concentric universes (biosphere, solar system, galaxy) and to three 28-year periods of life that compose the 84-year Uranian cycle." | C | AUTHOR'S OWN PROSE (editorial summary) |
| 99 | 56 | "These three levels – the Earth's biosphere, the solar system and the galaxy – are very real, at least potentially." | C | QUOTED — Rudhyar, "The First House" |
| 100 | 69 | "**Every Sun is isolated in space, the center of a group of planets upon which it radiates its vitalizing energy**; yet a Sun is also a star, and as a star is one companion among many in a Brotherhood of stars in the galaxy." | **A** (a sun at the center of its planets) + **B** ("in space", a galaxy of stars) | QUOTED — Rudhyar, "The First House" |
| 101 | 72 | "**No Sun radiates life to its planets in empty space; no individual is born on an alien Earth. Every Sun is essentially a star in the galaxy**, and every individual is born to fulfill a function, to answer a need of mankind and of the Earth, the one home of mankind." | **A** + **B** ("empty space", "alien Earth", "star in the galaxy") | QUOTED — Rudhyar, "The First House" |

**Separability:** 97, 99, 100, 101 IRREDUCIBLE as quotations. For 100–101 specifically: the passage is a *philological* argument (isolation ← *solus* ← *sol*) whose entire figure is the sun-among-planets-among-stars image; strip that and the etymological point has no vehicle. Hit 98 SEPARABLE.
**Breakage verified:** hit 97 is the same Rudhyar passage quoted at `sol-luna/Rudhyar_Zodiac_As_Process.md` line 129, which cites this extract file at line 151. Hits 100–101 are noted in the extract's own framing at line 66 as "A small philological gem from the First House chapter that links Rudhyar's vocabulary directly to the *Book of Sol*'s own theme"; removing them orphans that sentence and the section heading at line 64.

### `source-extracts/Dane_Rudhyar/astrology-of-personality.md` (194 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 102 | 20 | "The same Preface introduces the **person-centered** correction to Rudhyar's earlier geocentric assumptions…" | C | AUTHOR'S OWN PROSE (editorial frame) |
| 103 | 22 | "**Astrology has been essentially geocentric, even if it accepted some ideas belonging to the heliocentric picture of the solar system.** I see now that when it deals with human beings as individuals, it should be 'person-centered'…" | **A** (heliocentric picture named as the frame astrology partly accepted) | QUOTED — Rudhyar, *The Astrology of Personality*, Preface to the Third Edition (1970) |
| 104 | 32 | "…man as a whole solar system operating on the background of, and in constant relationship to the zodiac or the galaxy." | C | QUOTED — Rudhyar, Preface (1936/1968) |

**Separability:** 103 and 104 IRREDUCIBLE as quotations; 103's first clause is the premise for the "person-centered" move that the whole extract section is about. 102 SEPARABLE.
**Breakage verified:** removing 103 leaves line 20's "The same Preface introduces the person-centered correction" with nothing to introduce.

### `source-extracts/Dane_Rudhyar/astrology-of-transformation.md` (153 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 105 | 32 **and** 146 (same passage, quoted twice) | "**Humanity is only a part of vaster wholes — the planet, the solar system, our galaxy** — and these wholes hierarchically set the cosmic and planetary stages; yet, on the stage of the Earth's biosphere Man is a crucially important performer." | **A** ("the planet" = Earth as a planet) + C | QUOTED — Rudhyar, *The Astrology of Transformation*, Prologue |
| 106 | 114 | "The galactic frame extends this: **the Sun is one star among many in the galaxy**, and the individual one node within the worldwide humanity." | **A/B** | AUTHOR'S OWN PROSE (editorial summary) |

**Separability:** 105 IRREDUCIBLE; 106 SEPARABLE (a summary sentence, restatable as Rudhyar's claim).
**Breakage verified:** the passage at 105 appears at both line 32 and line 146 — the file quotes it twice, once in section II and once as the closing image under the heading "## X. Closing — Man as performer on a stage not of his making" (line 142). Removing it empties section X entirely.

### `source-extracts/Dane_Rudhyar/practice-of-astrology.md` (152 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 107 | 65 | "…and the planets are specialized 'organs' of the solar-system-whole." | C | QUOTED — Rudhyar, *The Practice of Astrology*, Step Four |
| 108 | 68 | "We likewise should not add up separate planetary entities to make up the solar system…" | C | QUOTED — Rudhyar, Step Four |
| 109 | 111 | "Step Six reframes the planets *as a system*. **Each planet is what it is because of its position in the sequence — Mars *outside* the Earth's orbit, Venus *inside*; Mercury closest to the Sun, the others outer.**" | **A** — an explicit heliocentric ordering with the Earth assigned an orbit, in the book's own editorial voice | AUTHOR'S OWN PROSE (editorial summary) |
| 110 | 113 | "We are thus primarily dealing with three inseparable factors: Sun, Moon and earth (the latter becoming the horizon-line in individual birth-charts)." | C | QUOTED — Rudhyar, Step Six |
| 111 | 118 | "It is the realm in which the solar system as a whole operates, conditioning at every moment through its interplanetary structure…" | C | QUOTED — Rudhyar, Step Six |

**Separability:** 107, 108, 110, 111 IRREDUCIBLE as quotations. **Hit 109 is SEPARABLE** and is the sharpest author-voice axis-A statement in the source-extracts half — it is an editorial gloss the extract adds, not a quotation; the section could summarise Step Six as "the planets are read as one ordered system, not a sum of independent entities" (which line 111's quotation already says) with no loss.
**Breakage verified:** removing hit 109 leaves the section heading "## VI. Step Six — the planetary system as a whole" (line 109) and its quotation intact; the only loss is the sequence example.

### `source-extracts/Dane_Rudhyar/` — remaining files

| # | File:line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 112 | `pulse-of-life.md`:57 | "The zodiac, on this reading, is the **temperate-Northern-hemisphere agricultural cycle of vegetation** intellectualised." | C ("hemisphere"; the word works on a disk as well as a ball, hence C not A) | AUTHOR'S OWN PROSE (editorial summary) |
| 113 | `zodiac-as-universal-matrix.md`:42 | "…thus the correlation of the signs of the zodiac with parts of the human organism and with **geodetic earth zones**." | C ("geodetic") | QUOTED — Rudhyar, *The Zodiac as the Universal Matrix*, Introduction |
| 114 | `astrological-mandala.md`:30 | "…the 12 signs of the tropical zodiac—**which as a whole refer to the annual cyclic relationship of the Earth to the Sun**—likewise have meaning according to their position in the complete cycle of the year." | C (a relationship of Earth to Sun, with no statement of which moves) | QUOTED — Rudhyar, *An Astrological Mandala*, Part One, ch. 1, p. 17 |
| 115 | `astrological-mandala.md`:39 | "…but when we deal with the series of 360 degree symbols **we see the relationship of the Earth to the Sun operating at a different level**." | C | QUOTED — Rudhyar, *An Astrological Mandala*, p. 18 |

**Separability:** 112 SEPARABLE. 113, 114, 115 IRREDUCIBLE as quotations.
**Breakage verified:** hit 113 is the same sentence quoted (truncated before "geodetic earth zones") at `sol-luna/The_Solar_Matrix_of_Creation.md` line 5 — the article uses only the first clause, so the two files already differ in how much of the sentence they carry. No inbound link breaks.

### `source-extracts/Hermetic_Corpus/death-and-the-immortal-essence.md` (125 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 116 | 61 | "Then the human being ascends through the seven planetary zones, surrendering at each one an acquired energy…" | C (planetary spheres/zones) | AUTHOR'S OWN PROSE (editorial frame) |
| 117 | 63 | "Thence the human being rushes up through the cosmic framework, at the first zone surrendering the energy of increase and decrease… And then, stripped of the effects of the cosmic framework, the human enters the region of the ogdoad" | C | QUOTED — *Corpus Hermeticum* I.24–26, trans. Copenhaver |

**Separability:** 116 SEPARABLE; 117 IRREDUCIBLE (the verbatim ascent passage is the section's whole content).
**Breakage verified:** removing 117 orphans the section heading at line 59, "## IV. The way up: shedding the energies of the seven zones", and leaves 116's summary with nothing to summarise. `sol-luna/Celestial_Name.md` lines 13–15 quote the parallel Poimandres passage independently, so no cross-file link breaks.

### `source-extracts/Damar_Tantra/quotes.md` (164 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 118 | 67 | "Experiments for the duration of twelve years will enable one to be as long lived as **the moon and the planets**." | C | QUOTED — *Damar Tantra*, Verse 21 |
| 119 | 75 | "Man will have the strength of ten thousand elephants and will live as long as **the moon and the planets exist**." | C | QUOTED — *Damar Tantra*, Verse 26 |

**Separability:** both IRREDUCIBLE as quotations; the "planets" here are the classical wandering lights used as an image of longevity, and the image is the verse.
**Breakage verified:** none.

### `source-extracts/Hesiod_Homeric_Hymns/hymn-32-to-selene.md` (24 lines)

| # | Line | Verbatim | Axis | Voice |
|---|---|---|---|---|
| 120 | 21 | "- **Full orbit at mid-month.** The hymn fixes the moon's peak beauty at the middle of the month…" | C ("orbit" in a note heading) | AUTHOR'S OWN PROSE (editorial note heading) |

**Separability:** SEPARABLE — the note heading could read "Full moon at mid-month" and the note's content (that Luna's time is counted in cycles, not daily positions) is untouched.
**Breakage verified:** none.

### `research_yoga_ayurveda_lineage/` — zero hits, plus one governing rule

All six files read/grepped in full. **Zero hits.** Every occurrence of "earth" in these files is the element *pṛthivī* or the ground; "atmosphere" at `06_structural_parallels.md`:361 is weather inside an Aṣṭāṅga Hṛdaya quotation; "axis" at `02_samkhya_shared_metaphysics.md`:121 is metaphorical ("the *tanmātra/bhūta* distinction is the axis of both yogic and…").

Recorded because it governs the whole book's vocabulary: `research_yoga_ayurveda_lineage/00_index.md` line 21 already carries an explicit editorial ban —

> "Vocabulary: chloride / chloride of sodium (never "sodium" alone); terrestrial / worldwide (never "planet/Earth-as-planet"); no vitamin/mineral/protein/micronutrient vocabulary — use Ayurvedic terms (rasa, ojas, dhātu, doṣa, prāṇa)."

### `yoga-tantra/Vajrolī.md` (141 lines) and `teasers/` (2 files) — zero hits

Grepped against the full term list with `-i`; no matches at all. Read for context; nothing cosmological.

## REGISTER 1 — Files whose entire premise rests on axis A or B

1. **`cosmology/Computing_vs_Measuring_The_Curve.md`** — the whole note exists to argue that the earth's curvature is a measured quantity (arc measurement, geodetic triangulation, reciprocal levelling). Nothing survives its removal. 17 of 17 hits are axis A; 15 of 17 are the author's own unhedged prose.
2. **`source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md`, sections V and VI (lines 296–737)** — 442 lines, ~50% of the file, consisting entirely of verbatim orthodox surveying and geodesy passages asserting a spheroidal, rotating, gravitationally-shaped earth. The file's declared purpose (line 5) is to hold both traditions verbatim, so these sections are premise-level, not incidental. Section IX (lines 853–867) is a synthesis built on comparing them to the zetetic material.
3. **Partial: `cosmology/Horizon_Dip_vs_Altitude.md`** — the file's substance is the globe-model dip calculation. It is framed modally ("on the globe model") and its stated conclusion is that the decisive measurement has not been made ("the open crux of the whole subject", line 52), so the premise is *comparative*, not committed. Listed here because removing the axis-A content leaves only the title and the closing paragraph.

No file in this half rests on axis B.

## REGISTER 2 — Files that already argue the level fixed earth or an enclosing firmament

These should never be touched by mistake.

1. **`cosmology/All_Instruments_Measure_a_Level_Earth.md`** — the full article for the level earth from surveying practice. Closing line 174: "That surface is the datum line of the inhabited world — and it is, in the language of the books that teach men to lay it, a flat horizontal plane."
2. **`sol-luna/Line_of_Sight.md`** — line 38: "Curvature does not reside in the ground, the water, the instrument, the structure, or even in the measurements themselves; it exists only as an a priori assumption held in the mind of those who presuppose it."
3. **`sol-luna/The_Toroidal_Heart.md`** — level earth-disk *and* firmament. Line 15: "The world is a torus. The level earth-disk lies within it. The north pole is at the center of the disk". Line 156: "the encircling southern firmament". Line 180: "The body, standing on the level earth, breathes with it."
4. **`sol-luna/Sidereal.md`** — section "Earth as the Stable Domain of Life" (lines 15–31): "The inhabited surface of Earth is encountered as level and steady. Lines extend straight. Water settles evenly." Quotes *Ṛgveda* 10.149.1 ("He fixed the earth firm, and set the sky in motion") and *Śatapatha Brāhmaṇa* 6.1.1.1 ("The Earth stands fast while the heavens move").
5. **`sol-luna/The_Solar_Matrix_of_Creation.md`** — line 10: "a living cycle of ascent and descent above a stationary Earth". Line 25: "In the classical cosmology, the Earth stands motionless at the center of a vast, rotating firmament. Rudhyar's interpretation does not dispute that geometry; he re-animates it."
6. **`source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md`, sections I–IV and the zetetic parts of VIII (lines 7–295, 795–851)** — Rowbotham, Carpenter, Dubay, Winship, Voliva, Schadewald's "Flat Earth Bible" reproduction. Line 24 quotes Rowbotham: "instead of its being a globe, and moving in space, it is the directly contrary — A PLANE; without motion, and unaccompanied by anything in the Firmament analogous to itself." Line 290 reproduces the Genesis firmament argument. **Note the file is mixed:** sections I–IV and part of VIII argue level earth; V, VI and part of VIII carry the orthodox curved-earth material.
7. **`source-extracts/Upanisads/death-and-the-imperishable-self.md`** line 124 — *Muṇḍaka Upaniṣad* 1.2.10, trans. Olivelle: "When they have enjoyed their good work, / atop the firmament, / They return again to this abject world."
8. **`research_yoga_ayurveda_lineage/01_vedic_origins.md`** line 559 and **`07_upanisadic_common_ground.md`** line 659 — the same *Yajur Veda* Savitṛ passage: "Yoking the gods, as they go to heaven with their mind and **to the firmament** with their thought, may Savitṛ stimulate them to create the lofty light."
9. **`research_yoga_ayurveda_lineage/00_index.md`** line 21 — the vocabulary rule quoted above, banning "planet/Earth-as-planet" language in favour of "terrestrial / worldwide".

## REGISTER 3 — Files with zero hits (40 of 65 files surveyed)

`sol-luna/` (4): `1-Sol.md`, `Kali_Yuga.md`, `Solar_Excess.md`, `The_Zodiac.md`

`research_yoga_ayurveda_lineage/` (6): `00_index.md`, `01_vedic_origins.md`, `02_samkhya_shared_metaphysics.md`, `03_sastric_crossreferences.md`, `06_structural_parallels.md`, `07_upanisadic_common_ground.md`

`yoga-tantra/` (1): `Vajrolī.md`

`teasers/` (2): `My_Mothers_My_Sisters.txt`, `Yogis_Dont_Eat_Fruit.txt`

`source-extracts/` (27): `Agni_and_Tapas.md`, `Apathya.md`, `Cooking_and_Agni.md`, `Fruit_as_Medicine.md`, `Raw_and_Cooked_Cross_Tradition.md`, `Raw_Vegan_Fruitarian_Harm.md`, `Raw_Vegan_Salad_and_Juice.md`, `Raw_Vegan_Staples_Warnings.md`, `Salt_Dosage_and_Conditions.md`, `Armando_Torres/death-the-sorcerers-option.md`, `Astanga_Hrdaya/water-and-srotas.md`, `Atharva_Veda/barley-and-grain.md`, `Carlos_Castaneda/death-the-eagle-and-the-definitive-journey.md`, `Dane_Rudhyar/astrological-study-of-psychological-complexes.md`, `Dane_Rudhyar/new-approach-to-zodiac.md`, `Golden_Fountain/urine-as-nectar-and-the-amaroli-tradition.md`, `Hatha_Yoga_Pradipika/quotes.md`, `Hesiod_Homeric_Hymns/hymn-31-to-helios.md`, `Hesiod_Homeric_Hymns/theogony-sun-moon-dawn.md`, `Khecarividya/lunar-nectar-and-breath.md`, `Rg_Veda/ghrta-as-amrta.md`, `Rg_Veda/soma-and-the-moon.md`, `Roots_of_Yoga/breatharian-witnesses.md`, `Upanisads/death-and-the-imperishable-self.md`, `Upanisads/moon-as-soul-threshold.md`, `Water_of_Life/quotes.md`, `Yogananda/giri-bala-the-yogini-who-never-eats.md`

(`Upanisads/death-and-the-imperishable-self.md` has zero *hits* but does appear in Register 2 for its firmament line.)

## TOTALS

**235 hits across 25 files.**

By axis (primary tag):
| Axis | Count |
|---|---|
| A | 145 |
| B | 1 |
| C | 89 |

Axis B appears as a **secondary** tag on 12 further hits (satellites/GNSS/"orientation in space"/"exterior space"/"empty space"/galaxy-of-stars/moon-as-a-world). The one B-primary hit is `Surveying_Instruments…md`:662, Torge & Müller: "this includes the methods of satellite and terrestrial geodesy as well as geodetic astronomy". **No hit anywhere in this half mentions rockets, moon landings, astronauts, or manned spaceflight.**

By voice:
| Voice | Count |
|---|---|
| QUOTED EXTERNAL SOURCE | 165 |
| AUTHOR'S OWN PROSE | 63 |
| SCAFFOLDING (heading, table, references, source list) | 7 |

By separability:
| Verdict | Count |
|---|---|
| IRREDUCIBLE | 181 |
| SEPARABLE | 54 |

The IRREDUCIBLE count is dominated by the 116 verbatim orthodox passages in `Surveying_Instruments_And_The_Shape_Of_The_Earth.md` — irreducible because a verbatim documentary extract cannot be reworded and remain what it is.

## HEAVIEST FILES

| File | Hits | One-line note |
|---|---|---|
| `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md` | 127 | Documentary compendium; ~440 lines of verbatim surveying/geodesy textbook passages asserting a spheroidal, rotating, gravity-shaped earth, quoted alongside the zetetic tradition by design. |
| `cosmology/Computing_vs_Measuring_The_Curve.md` | 17 | The only file in this half that argues *for* the curve in the author's own unhedged voice, start to finish. |
| `cosmology/All_Instruments_Measure_a_Level_Earth.md` | 17 | A level-earth article; all 13 quoted-external hits are orthodox textbook curvature language quoted adversarially, which is the article's method. |
| `cosmology/Horizon_Dip_vs_Altitude.md` | 11 | Globe-model dip calculation, framed modally, with three sentences that slip into flat declarative (lines 52 and 56). |
| `sol-luna/The_Toroidal_Heart.md` | 8 | A level-earth-disk article carrying modern astronomical vocabulary at its edges: "solar system", "galaxy", "heliopause", "orbit", "magnetosphere". |
| `source-extracts/Plutarch_De_Facie/passages.md` | 8 | Plutarch's moon as a terrained holy earth to which souls travel; ancient psychic cosmology that reads as axis B only on a literal reading. |
| `source-extracts/Dane_Rudhyar/astrological-houses.md` | 5 | Carries the "daily rotation of our globe around its polar axis" quotation *and* the "Every Sun is isolated in space… one companion among many in a Brotherhood of stars in the galaxy" passage. |
| `source-extracts/Dane_Rudhyar/practice-of-astrology.md` | 5 | Contains the sharpest author-voice heliocentric statement in the source-extracts half, at line 111 ("Mars *outside* the Earth's orbit, Venus *inside*"). |
| `sol-luna/The_360_Phases_of_Sol.md` | 5 | Five Sabian-symbol glosses using "the spheres", "planetary Mind", "planetary evolution", "vast dark space". |
| `sol-luna/Line_of_Sight.md` | 4 | A level-earth brief; its two orthodox quotations are the object of its own argument. |
| `source-extracts/Arthur_Young/science-and-astrology.md` | 3 | Holds the single most explicit heliocentric-plus-rotating-earth sentence in the surveyed half, at line 16 — quoted in a passage whose point is that astrology does not depend on the answer. |

## UNKNOWNS

- **Source verification.** Several quotations are flagged by the book itself as unverified working paraphrases ("source edition not yet recorded", "source extraction still needed") — this covers all the *Sūrya Siddhānta*, *Ṛgveda*, *Atharva Veda*, *Śatapatha Brāhmaṇa* and *Vedāṅga Jyotiṣa* material in `sol-luna/Sidereal.md` and `sol-luna/The_Toroidal_Heart.md`. I did not verify any quotation against its source; I catalogued what the files say.
- **Sabian-symbol provenance.** The 360 glosses in `The_360_Phases_of_Sol.md` are compressed paraphrases of Rudhyar; I could not determine from the file which words are Rudhyar's and which are the book's, so voice for hits 77–81 is recorded as "paraphrase of quoted external source" rather than resolved either way.
- **`The_108_Solar_Divisions.md` line 535** — "The heart is hidden by the shadow of the earth" — I could not determine whether this renders a traditional Vishakha attribute, an eclipse reference, or a free composition. Recorded as C on the eclipse-geometry reading, flagged unresolved.
- **Image content.** `generated-images/toroidal-heart-banner.png` (referenced at `The_Toroidal_Heart.md` line 11) was not opened. Its alt-text describes a level earth-disk; the rendered image was not inspected.
- **`.substack-posts.json`** at the repo root records which pieces are published; I did not cross-reference it, so I cannot say which of these files are public. All three `cosmology/` files carry `publish: false` in front-matter; `sol-luna/The_Toroidal_Heart.md` and `sol-luna/Rudhyar_Zodiac_As_Process.md` also carry `publish: false`. Most other files in this half have no front-matter at all.
