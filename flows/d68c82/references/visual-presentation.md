# Visual presentation in books: evidence, draft guideline, vocabulary

Research for the guideline review and vision proposal requested 2026-10-16
(vision/books.md, "Let's get a good researcher on how to make better
flowchart illustrations"). Scope: flowcharts and diagrams in books a
thinking machine writes for one human reader, read mostly on a phone, each
book proposing changes the reader rules on.

Evidence grades used below: **primary** = the paper or standard itself was
read (abstract or full text); **secondary** = known through a course page,
summary or citing paper; **practitioner** = blog or forum, anecdotal. Where
only an abstract was read, that is said.

The psyche's own words already set three constraints this research must
serve (vision/visualization.md, vision/books.md): figures must branch and
link, not run in one straight line; nodes must hold abstracted concepts,
not sentences forced into boxes; "colored boxes around cryptic text" is not
a visual.

## 1. Visual variables and what they mean to the eye

### Bertin: which variable fits which kind of data

Bertin's *Sémiologie graphique* (1967; English 1983) names the visual
variables: two planar (x, y position) and retinal ones (size, value or
lightness, texture, colour hue, orientation, shape). His central rule is
that each variable suits a kind of data: size and value are ordered and
read as "more/less"; hue and shape are read as "different kind", not
"more". Grade: secondary (course notes, cartographic commentary).

- https://www3.cs.stonybrook.edu/~mueller/teaching/cse564/bertin.pdf
- https://www.mappingasprocess.net/blog/2021/8/20/some-thoughts-on-jacques-bertins-cartographic-semiology
- https://cartographicperspectives.org/index.php/journal/article/download/cp38-rod/pdf/3890

### Munzner: expressiveness and effectiveness

Munzner's *Visualization Analysis & Design* turns Bertin into two
principles. Expressiveness: ordered data must look ordered, and unordered
data must not imply an order (so hue for categories, lightness or size for
order). Effectiveness: the most important attribute gets the most effective
channel. Magnitude channels, best first: position on a common scale,
position on unaligned scales, length, angle/tilt, area, depth, luminance,
saturation, curvature, volume. Identity channels, best first: spatial
region, hue, motion, shape. Grade: secondary (author's own lecture slides).

- https://www.cs.ubc.ca/~tmm/talks/minicourse14/vad17canberra-afternoon.pdf
- https://cs.ubc.ca/~tmm/talks/vad/VAD-marks.pdf
- https://www.cs.ubc.ca/~tmm/courses/436V-20/slides/marks.pdf

### Cleveland and McGill: accuracy of reading quantities

"Graphical Perception" (JASA 79(387), 1984) measured error in reading
quantities: position on a common scale is most accurate, then position on
non-aligned scales, length, angle/slope, area, volume, and colour
saturation/hue last. Heer and Bostock (CHI 2010) largely replicated the
ranking by crowdsourcing; later work shows rankings shift with task and
individual. Implication: when a figure shows numbers, put them on a shared
baseline as lengths, never as areas, angles or colour intensity. Grade:
secondary for the 1984 ranking (course slides; replications cited by
arXiv papers).

- https://info3312.infosci.cornell.edu/slides/04-graphical-perception.html
- https://vis.pku.edu.cn/course/visclass_f25/material/Graphical_perception.pdf
- https://arxiv.org/pdf/2212.10533 (individual differences challenge the single ranking)

### Preattentive features (Healey, Treisman lineage; Ware)

Hue, intensity, orientation, size, shape, curvature, line length and motion
are detected in under about 200 ms, and detection time does not grow with
the number of elements, but only when the target differs in one feature.
Conjunctions (e.g. "the red one that is also large") lose this pop-out.
Implication: one accent, on one feature, makes "the thing that matters"
visible at a glance; several accents cancel each other. Ware's *Information
Visualization: Perception for Design* is the standard textbook on the same
ground. Grade: primary (Healey's survey page and the Healey–Enns review).

- https://www.csc2.ncsu.edu/faculty/healey/PP/index.html
- https://visionlab-psych.sites.olt.ubc.ca/files/2015/06/140_HealeyEnns_IEEE2011.pdf
- https://healey.csc.ncsu.edu/publications/15840.pdf (hue and orientation estimation, 1996)

### Gestalt grouping

Wagemans et al. (Psychological Bulletin 2012) review a century of grouping
research: proximity, similarity, continuity, closure, and figure-ground are
quantified and interact. Palmer (1992) added common region (things inside
one enclosure group, overriding proximity); Palmer and Rock (1994) added
uniform connectedness (things joined by a line or a uniform region group
most strongly). Implication: enclosure and connection are the strongest
grouping tools; a shaded region says "these belong together" without
words. Grade: primary (PubMed abstract and PMC full text available).

- https://pubmed.ncbi.nlm.nih.gov/22845751/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC3482144/
- https://en.wikipedia.org/wiki/Principles_of_grouping (citations to Palmer 1992, Palmer and Rock 1994)
- https://www.cambridge.org/core/journals/spanish-journal-of-psychology/article/does-the-relative-strength-of-grouping-principles-modulate-the-interactions-between-them/5EECC917DB4843AE4255EE22EB3EB075

### Colour: colour-blind safety

About 8% of men of Northern European descent have red-green deficiency
(Wong, Nature Methods 8:441, 2011). Okabe and Ito's Color Universal Design
gives eight colours distinguishable under the common deficiencies: black
#000000, orange #E69F00, sky blue #56B4E9, bluish green #009E73, yellow
#F0E442, blue #0072B2, vermillion #D55E00, reddish purple #CC79A7. Their
principles: never rely on colour alone; combine colour with shape, position,
line type or label; differ in lightness, not only hue. Grade: primary
(Wong column PDF, Okabe/Ito group PDF).

- https://nature.berkeley.edu/garbelottoat/wp-content/uploads/nmeth.1618.pdf-WT.pdf
- https://jfly.uni-koeln.de/color/ichihara_etal_2008.pdf
- https://siegal.bio.nyu.edu/color-palette/ (hex reference)

Contrast checked here (WCAG relative luminance, against white #FFFFFF and
near-black #121212):

| Colour | on white | on #121212 |
| --- | --- | --- |
| blue #0072B2 | 5.19 | 3.61 |
| sky blue #56B4E9 | 2.31 | 8.12 |
| bluish green #009E73 | 3.42 | 5.48 |
| vermillion #D55E00 | 3.87 | 4.84 |
| orange #E69F00 | 2.25 (fails) | 8.32 |
| darkened amber #A86F00 | 4.25 | 4.41 |
| reddish purple #CC79A7 | 3.06 | 6.12 |
| grey #6B7280 | 4.83 | 3.88 |
| grey #9CA3AF | 2.54 | 7.38 |
| yellow #F0E442 | 1.32 (fails) | 14.17 |

So: Okabe orange and yellow fail as strokes on a light page; the
vocabulary below darkens amber for light theme and drops yellow.

### Colour: contrast and colour-alone (WCAG)

WCAG 1.4.11 requires 3:1 contrast for graphical objects needed to
understand content (lines in graphs, icons). WCAG 1.4.1 forbids colour as
the only means of conveying information. WCAG 1.4.10 requires content to
reflow at 320 CSS px without two-dimensional scrolling. Grade: primary
(W3C Understanding documents).

- https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast
- https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- https://webaim.org/articles/contrast/

### Colour: meaning (semantics)

Lin, Fortuna, Kulkarni, Stone and Heer (EuroVis 2013, best paper):
semantically resonant colours (colours that match the concept) speed chart
reading versus a standard palette. Schloss and colleagues: viewers run
"assignment inference", choosing the colour-to-concept mapping that
maximizes total fit across all pairs, plus relational biases such as
"darker is more"; palettes whose intended mapping clearly wins are read
faster and more accurately. Cross-cultural: red/green valence associations
are broadly shared but stronger in Western groups (Kawai et al. 2022);
Adams and Osgood (1973, 23 cultures) found red and black carry strong
affect everywhere. Interface convention: red = cancel/error/decrease,
green = ok/success/add. Implication: a fixed vocabulary that matches
conventions (green added, red removed) needs no legend for this reader;
an arbitrary one forces a legend lookup every figure. Grade: primary for
Lin et al. and Schloss (abstracts); secondary for cross-cultural.

- https://idl.uw.edu/papers/semantically-resonant-colors
- https://diglib.eg.org/items/0fd760e2-967f-4361-81f1-9db03bea3655
- https://arxiv.org/pdf/2209.02782 (Schoenlein et al., direct and relational associations)
- https://schlosslab.discovery.wisc.edu/wp-content/uploads/2024/06/Schloss2024.pdf
- https://link.springer.com/article/10.1007/s00426-022-01697-5 (red/green valence across cultures)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7816258

Szafir (TVCG 2018) shows colour differences shrink with mark size: thin
lines and small points need larger colour differences than the big patches
colour standards assume. Implication for phones: coloured hairlines are
weak; carry colour on fills and thicker strokes.

- https://cmci.colorado.edu/visualab/VisColors/
- https://cmci.colorado.edu/visualab/VisColors/17-VIS-ModelingColorDifference.pdf

### Multimedia learning and cognitive load

Mayer's principles (Cambridge Handbook of Multimedia Learning; 2020
summary): coherence (cut extraneous material; 23 of 23 tests, median
d = 0.86), signaling (cue the essential organization; 24 of 28 tests,
d = 0.41), spatial contiguity (put words next to the picture part they
describe). Sweller's cognitive load theory: working memory holds few
interacting elements; extraneous load (e.g. split attention between a
legend and the figure) hurts most when the material is intrinsically
complex, which design proposals are. Grade: primary (Mayer 2020 PDF);
secondary for Sweller.

- https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf
- https://resolve-he.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/CD5B7AE1279A9AB81F8EEBB53DBEC86E
- https://twut.nd.edu:443/PDF/Principles-MultimediaLearning.pdf
- https://nielsolson.us/STLHE020409/SwellerVisualizationAndInstructionalDesign.pdf
- https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2019.00086/epub

### Why diagrams help at all

Larkin and Simon (Cognitive Science 1987): a diagram beats text when it
indexes information by location, so what an inference needs sits together
and the next step is found by looking, not searching. A straight chain of
boxes adds no such indexing over a sentence; branches, joins and
neighbourhoods do. This is the research form of the psyche's 2026-10-14
complaint about linear flowcharts. Grade: primary (full PDF).

- https://mechanism.ucsd.edu/bill/teaching/F12/cs200/Readings/larkin.whyadiagramissometimesworth.1987.pdf

Tversky (Visualizing Thought, Topics in Cognitive Science 2011): marks
carry meaning (dots = entities, lines = connection, boxes = containment,
arrows = order/direction/causality) but are ambiguous; spatial mappings
work best when congruent (up = more/good, left-to-right = time in
left-to-right readers). Heiser and Tversky (Cognitive Science 2006):
diagrams without arrows are read as structure, with arrows as function or
process; arrows are the switch. Grade: primary (PDFs).

- https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/2011_Tversky_VisualizingThoughts.pdf
- https://mechanism.ucsd.edu/bill/teaching/F12/cs200/Readings/tversky.visualizingthought.2010.pdf
- https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/sincomprehendingandproducingmechanicaldiagrams.PDF

## 2. Flowchart and diagram practice

### Notation design (Moody, Physics of Notations)

Moody (IEEE TSE 2009) gives nine principles for cognitively effective
notations, of which these apply directly: semiotic clarity (one symbol per
meaning, one meaning per symbol), perceptual discriminability (symbols
differ clearly), semantic transparency (appearance suggests meaning),
complexity management (split large diagrams), graphic economy (few symbol
types), dual coding (text plus graphics), cognitive fit. The principles
trade off: more symbol types hurt discriminability. Grade: secondary
(abstracts, reviews); the TSE paper itself was not read.

- https://blogs.adelaide.edu.au/acvt/?p=334
- https://researchportal.unamur.be/en/publications/visual-syntax-does-matter-improving-the-cognitive-effectiveness-o
- https://www.scitepress.org/Papers/2016/58958/pdf/index.html

### Graph layout: crossings matter most

Purchase (1997, "Which aesthetic has the greatest effect on human
understanding?"): of five layout aesthetics, minimizing edge crossings was
by far the most important; bends and symmetry mattered less. Later work:
crossing angle matters too (crossings at near-right angles hurt less);
grid alignment helps. Grade: secondary (citing papers, author's own later
paper).

- https://www.springerprofessional.de/en/which-aesthetic-has-the-greatest-effect-on-human-understanding/13633544
- https://www.cs.auckland.ac.nz/~beryl/publications/AUIC%202010%20Graph%20drawing%20aesthetics.pdf
- https://arxiv.org/pdf/0810.4431 (eye-tracking study of layout)
- https://opus.lib.uts.edu.au/bitstream/10453/16557/1/2010001394OK.pdf (VINCI 2010, crossing number and angle)
- https://arxiv.org/pdf/1609.07688 (limits of aesthetic metrics)

### Data-ink, small multiples, smallest effective difference (Tufte)

Remove non-data ink; repeat one design across panels to invite comparison
(small multiples); make each visual difference only as large as needed to
be seen, so the one strong difference stands out. Grade: secondary (course
notes).

- https://faculty.cc.gatech.edu/~stasko/4460/Notes/tufte.pdf
- https://websites.umich.edu/~mmmc/516/notes/TuftePrinciples.pdf

### Phone width

Brehmer, Horak, Aigner, Joshi, Tominski ("Responsive Visualization Design
for Mobile Devices", in *Mobile Data Visualization*, CRC 2021): desktop
techniques fail on phones through display size, aspect ratio and
interaction; they review ten responsive strategies (rescale, relayout,
re-encode, attentional cues). The portrait aspect favours vertical flow and
stacked panels over wide left-to-right graphs. Grade: secondary (chapter
abstract only).

- https://tableau.com/research/publications/responsive-visualization-design-mobile-devices

## 3. Showing change

Gleicher et al. (Information Visualization 2011) and Gleicher (2018,
"Considerations for Visualizing Comparison"): every comparison design is
juxtaposition (side by side), superposition (overlaid in one frame), or
explicit encoding (draw the difference itself), or a hybrid. Explicit
encoding is best when the difference is what matters; juxtaposition needs
identical layout so the eye can match parts. Hybrid example from the
literature: overlay two graphs and colour what changed. Kim et al.
(Comparative Layouts Revisited, 2020) reviewed 127 papers and 15 user
studies and refine these terms. Grade: secondary (summaries and the 2020
review).

- https://pages.graphics.cs.wisc.edu/VisSnacks/papers/comparison
- https://arxiv.org/pdf/2009.00192
- https://hcil.snu.ac.kr/research/comparative-layouts-revisited

Applied to a book proposal (inference from the above, not measured):

- Default form: one figure of the proposed state, with the change explicitly
  encoded (added parts green with "+", removed parts vermillion with
  strike or "−", unchanged parts grey). This is superposition plus explicit
  encoding: one frame, no eye travel between panels.
- When the structure itself moves (nodes re-parented, flow re-routed), use
  two stacked panels "Now" and "Proposed" with every unchanged node in the
  same position, the change highlighted only in the second panel.
- The single thing the reader must rule on carries the one accent (blue
  fill or thick outline); preattentive pop-out works only for one target
  (Healey).

## 4. Making a language model draw well

### Findings

1. **A high-level, typed representation beats raw primitives.**
   AutomaTikZ (Belouadi, Lauscher, Eger, ICLR 2024): generating vector
   graphics directly from low-level primitives is hard; a high-level
   language (TikZ) as intermediate representation makes it tractable;
   fine-tuned models beat GPT-4 and Claude 2, which "tend to generate more
   simplistic figures". DiagrammerGPT (COLM 2024): an LLM first writes a
   "diagram plan" of entities, relationships and bounding boxes, revised in
   a planner-auditor loop, then a separate renderer draws it. Feynman
   (2026): the agent writes simple declarative programs rendered by
   Penrose, whose optimization layout keeps semantics fixed. Penrose
   (SIGGRAPH 2020) itself separates what is said from how it is styled, so
   one style sheet draws many diagrams consistently. EvoDiagram (2026):
   an intermediate canvas schema separates semantic intent from rendering
   logic. Lee et al. (AIED 2025): SVG as intermediate representation works;
   a text-to-image model (DALL·E 3) instead produced unusable diagrams;
   observed SVG errors include misconfigured viewBox clipping the figure.
   Grade: primary (abstracts; Lee et al. full HTML).
   - https://arxiv.org/abs/2310.00367
   - https://arxiv.org/abs/2310.12128v2
   - https://github.com/aszala/DiagrammerGPT
   - https://arxiv.org/abs/2603.12597
   - https://penrose.cs.cmu.edu/siggraph20
   - https://arxiv.org/abs/2604.09568
   - https://arxiv.org/html/2503.07429v1

2. **Render, look, critique, repair.** EvoDiagram renders, then a
   vision-language agent compares image to input for missing content,
   style inconsistency and overlaps. Feynman aggregates yes/no judgements
   of vision-language judges on rendered variants. GVR-Coder (2026) uses a
   visual-feedback loop to fix element overlap in SVG. Bavisitter (IEEE VIS
   2024) checks the generated chart spec and its rendered image against
   known design guidelines and appends a concrete fix instruction to the
   prompt ("Change mark to bar"). PlotGen's multimodal self-reflection gave
   a modest 4 to 6% gain on MatPlotBench: the loop helps but is no
   substitute for a good spec. Grade: primary (abstracts) except PlotGen
   (secondary).
   - https://arxiv.org/pdf/2607.28073
   - https://aa.ieeevis.org/year/2024/program/paper_v-short-1064.html
   - https://idclab.skku.edu/assets/Bavisitter.pdf
   - https://arxiv.org/pdf/2602.20137 (do LLMs understand visualization rules)
   - https://cvpr.thecvf.com/virtual/2026/poster/39481 (visual feedback for layout)

3. **Examples and continuity.** Lee et al.: the prompt that worked had a
   task description, generation instructions, one in-context example from
   the same topic, then the target; using the previous diagram as an
   on-task demonstration scored best and kept diagrams continuous.
   EvoDiagram distils past execution traces into a memory of design
   guidelines retrieved by context. Grade: primary (Lee et al. full HTML;
   EvoDiagram abstract).

4. **Evaluation.** DiagramEval (EMNLP 2025) scores generated diagrams as
   graphs (labels as nodes, connections as edges) and finds existing
   metrics too coarse; MermaidSeqBench (2025) found large gaps between
   models on Mermaid generation. A structural check (did every intended
   node and edge appear, with no extras) is cheap and mechanical when the
   spec is typed. Grade: primary (abstracts).
   - https://arxiv.org/abs/2510.25761
   - https://aclanthology.org/2025.emnlp-main.640.pdf
   - https://arxiv.org/abs/2511.14967

5. **Practitioner consensus** (anecdotal): keep a text DSL (Mermaid,
   Graphviz, D2) as the source and SVG as generated output; LLMs produce
   valid Mermaid reliably but its default layout routes edges poorly;
   Graphviz gives more control for directed graphs; D2's TALA layout
   engine can take model-chosen positions while it routes connections.
   - https://blog.jonudell.net/2024/11/02/how-to-create-software-diagrams-with-chatgpt-and-claude/
   - https://yomotherboard.com/?p=585543
   - https://sharedcontext.ai/skills/external/msewell/rendering-clean-diagrams

**Gap:** no study found compares, on the same tasks, a typed spec rendered
by a layout engine against free SVG written by the model. The direction of
evidence (1, 2, 5) favours the typed spec, but this is inference across
studies, not a head-to-head result.

### Proposed pipeline for our books (inference from the findings)

1. The writer states the figure's claim in one sentence (becomes the
   caption).
2. The writer emits a typed spec: nodes (id, short label, role from the
   vocabulary: context, focus, added, removed, open, human, store,
   decision), edges (from, to, verb label, role: main or secondary,
   exists or proposed), groups (enclosures), and optional quantities.
3. Code validates the spec against the rules (node count, label length,
   one focus, every arrow labelled, roles from the closed set) and rejects
   with a concrete message.
4. A deterministic renderer applies layout (top-to-bottom, crossing
   minimization, e.g. Graphviz dot or ELK) and the fixed style sheet; the
   model never chooses colours or coordinates.
5. The rendered SVG is rasterized at 360 px width and a vision model checks
   it against a short yes/no list (overlaps, clipping, legibility, does it
   branch, does the focus pop out); failures go back as fix instructions.
6. The previous figures of the same book are given as the on-task example,
   so node positions and naming stay continuous across figures.

## 5. Draft guideline (20 rules)

1. One figure states one claim; write the claim as the caption first. (Mayer coherence; Tufte)
2. Draw only real structure: branches, joins, loops, containment or comparison; a straight chain is a sentence, not a figure. (Larkin and Simon 1987; psyche 2026-10-14)
3. Nodes hold 1 to 4 word noun labels; no sentences inside shapes. (Tversky 2011; Mayer coherence; psyche vision/books.md)
4. Put the verb on the arrow; label every arrow whose meaning is not obvious, and give arrows one meaning per figure. (Heiser and Tversky 2006; Tversky on mark ambiguity)
5. Flow top to bottom on the phone; use left-to-right only within three columns. (Brehmer et al. 2021; Tversky congruence)
6. At most nine nodes per figure; split larger ideas into a sequence of figures with one shared layout. (Sweller element interactivity; Moody complexity management; Tufte small multiples)
7. No edge crossings; if one is unavoidable, cross at a right angle. (Purchase 1997; VINCI 2010 crossing-angle study)
8. Show belonging by enclosure and proximity, not by extra lines. (Palmer 1992 common region; Wagemans et al. 2012)
9. Colour only from the fixed vocabulary below, same meaning in every book, so no legend is needed. (Moody semiotic clarity; Lin et al. 2013; Schloss assignment inference)
10. One accent per figure, on the one thing the reader rules on; everything else ink or grey. (Healey preattentive pop-out; Mayer signaling; Tufte smallest effective difference)
11. Never colour alone: pair each colour with a glyph (+, −, ?), dash, or word. (WCAG 1.4.1; Okabe and Ito; Wong 2011)
12. Every coloured stroke reaches 3:1 contrast with its background in light and dark themes. (WCAG 1.4.11)
13. Hue says kind; lightness and weight say importance; never use hue for order. (Bertin; Munzner expressiveness)
14. Two stroke weights only: thick for the main path, thin for the rest. (Bertin size is ordered; Munzner effectiveness)
15. Draw quantities as lengths on a shared baseline, to scale, with the number written on the mark; never as area, angle or shade. (Cleveland and McGill 1984; Heer and Bostock 2010)
16. Show a change in one frame: added green "+", removed vermillion struck "−", unchanged grey. (Gleicher explicit encoding and superposition)
17. When structure moves, stack "Now" over "Proposed" with unchanged nodes in the same place. (Gleicher juxtaposition; Kim et al. 2020)
18. Labels sit on or beside their mark; no keys, footnote letters or detached legends. (Mayer spatial contiguity; Sweller split attention)
19. Fits 360 px width with no horizontal scroll and text at least 12 px; colour on fills and thick strokes, not hairlines. (WCAG 1.4.10 reflow; Szafir 2018)
20. The machine writes a typed spec, code renders it with the fixed style, and the rendered image is checked against these rules before publication. (AutomaTikZ; DiagrammerGPT; Penrose and Feynman; EvoDiagram; Bavisitter)

## 6. Fixed colour and weight vocabulary (proposal)

Colours are Okabe-Ito, darkened where light-theme contrast fails. Each
colour has a second, non-colour cue so it survives colour blindness,
grayscale, and a glance.

| Mark | Light theme | Dark theme | Means | Second cue |
| --- | --- | --- | --- | --- |
| Ink | #1F2933 | #E5E7EB | ordinary node or edge; exists, in scope | none needed |
| Grey | #6B7280 | #9CA3AF | context, unchanged, out of scope | lighter fill, thin stroke |
| Blue | #0072B2 | #56B4E9 | focus: the one thing to rule on (one per figure) | thick outline or tinted fill |
| Green (bluish) | #009E73 | #009E73 | added, new, works, verified | "+" glyph |
| Vermillion | #D55E00 | #D55E00 | removed, broken, risk, refused | "−" glyph or strike-through |
| Amber | #A86F00 | #E69F00 | open question, needs the reader's decision, temporary | "?" glyph |
| Reddish purple | #CC79A7 | #CC79A7 | the human (the living, the reader) | person shape |
| Thick stroke (3 px) | | | main path the figure is about | |
| Thin stroke (1.25 px) | | | secondary relation | |
| Dashed stroke | | | does not exist yet: proposed, planned, optional | |
| Solid stroke | | | exists now | |
| Arrow | | | direction of flow, order or cause; verb label | |
| Enclosure (tinted rounded region) | | | one boundary: host, repository, component, flow | |
| Rectangle | | | thing or component | |
| Rounded rectangle | | | action or step | |
| Diamond | | | decision; must branch | |
| Cylinder | | | store | |

Excluded on purpose: yellow (1.32:1 on white), sky blue in light theme
(2.31:1), red-green pairs without glyphs, gradients, shadows, 3-D, size as
importance unless it is a drawn-to-scale quantity.
