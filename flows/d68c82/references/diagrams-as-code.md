# Diagrams as code in documentation: forms, evidence, proposal

Research for vision/books.md, "Figures live as code in the vision source"
(psyche, typed, 2026-10-16T18:07) and "The model draws right the first
time" (18:10). Question: how can figures live as code in a text source, so
a text model reads, writes and edits them, and still render as good
figures for a person reading a book on a phone? Who has done it, and how
well did it go?

Evidence grades: **primary** = the source itself was read, though often
through a fetch tool's summary rather than the raw text; **secondary** =
an abstract, a search digest or an aggregator; **practitioner** = a blog or
forum post (anecdote); **measured** = run on Prometheus on 2026-10-16
(section 1). Where a claim could not be confirmed, the text says so.

## 1. Measured on Prometheus (model-free)

I wrote one figure in six forms: Mermaid, Graphviz DOT, D2, PlantUML, TikZ
and our own book-build EDN `figure` fence. It has 8 nodes, a branch, a
loop back (Check rejects to Writer) and a join. The files are in this
session's scratchpad and in `/tmp/dg-d68c82` on Prometheus. Nothing was
built locally.

Prometheus had no internet that day ("Network is unreachable" and DNS
failures to cache.nixos.org). Graphviz was already in its store. I relayed
D2, PlantUML and Mermaid from cache.nixos.org to Prometheus with
`nix copy --from https://cache.nixos.org --to ssh-ng://prometheus...`.
That copies only finished outputs, builds nothing, and leaves the local
store unchanged; I checked that afterwards. I did not try TikZ: tectonic
fetches its packages at run time, and a TeX Live scheme would have meant
relaying gigabytes.

| Form | Version | Closure | Renders | Output width / smallest text | Text at 360 px | Labels as | Accessibility in the SVG |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Graphviz DOT | 15.1.0 | 140 MiB | yes, about 1 s | 337 px / 14 px | 14 px (fits as drawn) | `<text>` | a `<title>` per node (tooltip only) |
| D2 (dagre) | 0.7.1 | 2.2 GiB (bundles Playwright Chromium) | yes, 0.12 s | 621 px / 16 px | about 9.3 px | `<text>` | none |
| D2 (ELK) | 0.7.1 | same | yes, 0.7 s | 534 px / 16 px | about 10.8 px | `<text>` | none |
| PlantUML | 1.2026.3 | 952 MiB (Java) | yes | 404 px / 13 px | about 11.6 px | `<text>` | none |
| Mermaid (mmdc) | 11.16.0 | 2.2 GiB (Chromium) | yes, about 5.5 s | 430 px | n/a (HTML labels) | `<foreignObject>` HTML | `<title>`, `<desc>`, aria from `accTitle`/`accDescr` |
| Mermaid, `htmlLabels:false` | same | same | yes | 432 px / 12 px | about 10 px | `<text>` | same |
| book-build EDN | in tree | none (babashka) | yes | 239 px / 12 px | 12 px or more | `<text>` styled by page CSS | none yet |

The "text at 360 px" column assumes the SVG is scaled to its container.
book-build's `sanitize-svg` does this (`width="100%"`).

What the renders showed:

- **Mermaid's default output loses every label in our books.** Its
  flowchart labels are HTML inside `<foreignObject>` (16 elements, 0
  `<text>`). book-build's `sanitize-svg` (tools/book-build.clj, line 822)
  deletes `foreignObject` for safety, so every box and arrow would come
  out blank. With `htmlLabels:false` it emits `<text>`. But in the
  rasterized copy, multi-word labels lost their spaces ("Writermodel",
  "parsedby"). That copy was rasterized with librsvg; I did not check
  whether a browser shows the same.
- **Mermaid rejects unquoted parentheses.** `A[Write (draft)]` stops with
  "Parse error on line 2". The writer must quote such labels. This matches
  the failure mode practitioners report (section 3).
- **PlantUML turned the figure upside down.** It put Check at the top and
  Writer under it, so the main flow reads from the bottom up. It drew all
  edges, but the reading order is lost. Its default look is grey and dated.
- **Graphviz** gave the most compact correct drawing. The loop goes up the
  side, and the join at Book is clean. It fits a phone at its natural size
  with 14 px node text. One flaw: edge labels used the default serif font,
  because `fontname` was set only on nodes, so one `edge [fontname=...]`
  line is owed.
- **D2** looked the best: a clear palette, a person shape, quiet edge
  labels. But it is drawn wide and loose. Scaled to a phone, its text is
  9 to 11 px, below our 12 px floor (visual-presentation.md, rule 19).
  Fixing that needs a scale or padding setting.
- **book-build EDN** handled the loop and the join, with orthogonal edges
  and a trunk at each fork. Its SVG takes colours from the page
  stylesheet, so a renderer outside the page draws it all black. That
  means its look can only be judged inside a book, and I did not judge it
  there. The EDN form has nodes, edges, verbs, `:note` and `:bare`. It
  has no shape, role, group or dashed "proposed" mark yet, which the
  colour and shape vocabulary in visual-presentation.md section 6 needs.
- **All four external tools were byte-identical across two runs**
  (Graphviz, D2, Mermaid, PlantUML). A regenerated SVG only changes when
  its source does.

## 2. Who has done it, and how it went

**Mermaid in Markdown** is the most widely adopted form.

- **GitHub** has rendered Mermaid fences in Markdown since 14 Feb 2022.
  Diagrams render only where JavaScript runs; other clients show the raw
  text. Primary.
  https://github.blog/developer-skills/github/include-diagrams-markdown-files-mermaid/
- **GitLab** renders Mermaid 11. PlantUML is on at GitLab.com, but a
  self-managed admin must enable it, and Kroki too. A
  `Cross-Origin-Resource-Policy` header makes Mermaid fail silently.
  Primary. https://docs.gitlab.com/ee/user/markdown.html
- **Kubernetes docs** adopted Mermaid. Primary.
  https://kubernetes.io/docs/contribute/style/diagram-guide/
  - For: the diagram is plain text in the pull request, and no separate
    tool is needed.
  - Against: no icons or artwork, hence the guide's advice "Keep it
    simple!".
  - The live editor's Mermaid version can differ from the site's, giving a
    syntax error or a blank figure. Their fallback is to commit an
    exported SVG beside the source.
- **MkDocs Material** has Mermaid with light and dark schemes. Theme
  adaptation covers only flowchart, sequence, class, state and ER
  diagrams. Its own docs say pie, gantt, journey, git and requirement
  diagrams "don't work well on mobile". Primary.
  https://squidfunk.github.io/mkdocs-material/reference/diagrams/

**Graphviz in the Linux kernel docs.** The kernel's Sphinx setup takes
inline DOT through `kernel-render` and recommends SVG for images. If
Graphviz is missing, the build still succeeds and the figures are
silently left out. Primary.
https://www.kernel.org/doc/html/latest/doc-guide/sphinx.html

**MediaWiki.**
- Wikimedia disabled its Graph extension (Vega) on all projects in April
  2023 over an XSS flaw. It was still off in March 2024, and has since
  been replaced by the Chart extension. Primary/secondary.
  https://www.mediawiki.org/wiki/Extension:Graph ;
  https://signpost.news/2024-03-29/Technology_report
- The Diagrams extension renders Graphviz, PlantUML and Mermaid through a
  render service.

**draw.io and Excalidraw** take a different approach: the editable scene
is embedded inside the exported SVG or PNG. By default the `.drawio`
scene is compressed, so it cannot be read in a line diff unless it is
saved uncompressed. Practitioner. https://www.innoq.com/en/blog/draw-the-diff

**Security cost of renderers that run in the reader's browser or on a
server.**
- Mermaid has had several XSS advisories: a bundled DOMPurify bug, and
  CVE-2025-54880 and CVE-2025-54881. Secondary.
  https://db.fluidattacks.com/adv/npm/mermaid/CVE-2025-54881
- PlantUML had an SSRF flaw, CVE-2023-3432. Secondary.
  https://www.wiz.io/vulnerability-database/cve/cve-2023-3432
- We render at build time and inline sanitized SVG, which avoids this
  class of problem. That is why the sanitizer strips `foreignObject`.

**Layout changing under the author.** Mermaid 12.0.0 made ELK the default
layout for several diagram types, which changes how existing diagrams
look unless `layout: dagre` is pinned. Secondary.
https://newreleases.io/project/github/mermaid-js/mermaid/release/mermaid@12.0.0

**Accessibility.** In 2022, Adrian Roselli found that a screen reader
read GitHub's Mermaid charts as run-on text, with no relationships and no
reading order. He advised a plain-text description beside the chart.
Practitioner.
https://adrianroselli.com/2022/03/maybe-dont-use-flow-charts-on-github.html
Mermaid has since added `accTitle` and `accDescr`, and the measured
output above confirms they become `<title>`, `<desc>` and aria
attributes. None of the forms makes the graph structure itself
accessible. A caption that states the claim, which is already rule 1 in
visual-presentation.md, does the work for every form.

**Look comparisons.** I found no independent, rigorous comparison.
text-to-diagram.com is run by the D2 team. D2 ships dagre and ELK; its
TALA engine is separate, and I could not confirm whether TALA is
proprietary. https://d2lang.com/tour/layouts/

## 3. How well models write, read and edit each form

No study compares all the forms head to head. Where these findings rank
one form against another across studies, that is inference.

- **VGBench** is the only direct comparison found. It asked models
  questions about figures written as SVG, TikZ and Graphviz. GPT-4
  answered correctly 54.9% of the time from SVG, 81.0% from TikZ and
  84.5% from Graphviz; GPT-4o scored 60.3%, 75.0% and 75.0%. So models
  read raw SVG worst. On generation, GPT-4 had its best CLIP score but
  its worst FID on Graphviz. The study reports no rate of invalid output.
  Primary (full HTML, via a fetch summary). https://arxiv.org/html/2407.10972v2
- **DiagramAgent (CVPR 2025)** used LaTeX and DOT sources. GPT-4o's Pass@1
  was 49.8 for generating a diagram, 64.1 for coding and 92.4 for
  editing an existing one. Editing is much easier than drawing from
  scratch, which favours keeping a source and revising it. The paper
  gives no split by form. Secondary. https://arxiv.org/html/2411.11916v1
- **PlantUML.**
  - In one study, PlantUML class diagrams compiled more than 90% of the
    time for all models, and Claude 3.7 kept over 98% of the
    relationships. Secondary. https://arxiv.org/pdf/2506.00788
  - Code2UML reports 91 to 99% validity for common diagram types, but
    only 58% for C4 context diagrams, and that with an agent repairing
    the output. Secondary, numbers from a search summary.
    https://arxiv.org/pdf/2605.24453
- **Mermaid.**
  - MermaidSeqBench (132 sequence diagrams) found large gaps between six
    small open models. Secondary. https://arxiv.org/abs/2511.14967
  - A university project report says Mermaid validity rose from about 70%
    to about 95% when parse errors were fed back to the model, with at
    most three tries. Practitioner, search snippet only.
  - The failures reported are unquoted punctuation and parentheses, and
    syntax a given diagram type does not support. I reproduced the
    parenthesis failure (section 1).
- **TikZ.**
  - AutomaTikZ found GPT-4 and Claude 2 "tend to generate more simplistic
    figures". Secondary. https://arxiv.org/abs/2310.00367
  - DeTikZify needed feedback from compiling to beat them. Secondary.
    https://arxiv.org/abs/2405.15306
- **Raw SVG.**
  - SGP-Bench shows models can answer questions from SVG code. Secondary.
    https://arxiv.org/html/2408.08313v1
  - SVGEditBench v2 finds "massive room for improvement" in following an
    edit instruction. Secondary. https://arxiv.org/pdf/2502.19453
  - SVGenius says all models degrade as the task gets harder. Secondary.
    https://arxiv.org/abs/2506.03139
  - Overlap and clipping are practitioner reports. Lee et al. (AIED 2025)
    saw a wrong viewBox clip the figure (visual-presentation.md,
    section 4).
- **D2, Penrose, Excalidraw JSON.**
  - I found no benchmark for D2.
  - For Penrose, one researcher's forum comment says models do better
    with domain-specific code than with SVG. Practitioner.
  - Excalidraw JSON costs about ten times the tokens of Mermaid for the
    same small diagram, because it stores coordinates. Practitioner.
    https://dev.to/akari_iku/analyzing-the-best-diagramming-tools-for-the-llm-age-based-on-token-efficiency-5891

The pattern across studies is the same as visual-presentation.md
section 4 found. Models do better with a short, typed description of
meaning (nodes, edges, labels) than with geometry. A parser or compiler
error is a cheap check that needs no model and can be fed back to the
writer. This fits "the model draws right the first time" (psyche,
18:10): the check is code, not a model looking at the picture.

## 4. Pros and cons by form, for figures in vision sources and books

**Typed graph data (book-build EDN `figure` fence)**
- Pros:
  - It is already in the tree and tested, and needs no external
    dependency.
  - It renders inside the book's own CSS, so light and dark themes come
    for free. It is drawn for a 239 px column with text at 12 to 14 px.
  - It is pure data (an `intent-data` fit): reviewable line by line, and
    checked by code. `read-figure` already rejects an edge that names no
    node.
  - It carries meaning only, with no coordinates, so a model never picks
    positions or colours. Everyone who has done this successfully worked
    from such a description (AutomaTikZ, DiagrammerGPT, Penrose).
- Cons:
  - It has no shapes, roles, groups or dashed "proposed" mark yet, so the
    fixed colour and shape vocabulary still has to be added.
  - It is our own format: no outside tooling, and no benchmark of how
    well models write it. They write EDN data readily, but that is
    inference.
  - It covers box-and-arrow figures only, not quantities.
  - Its layout engine is ours to maintain.

**Graphviz DOT**
- Pros:
  - It has been stable for decades and is small (140 MiB closure).
    Output is deterministic.
  - It had the best model reading score in VGBench (84.5%).
  - It drew the best phone-width layout in our test.
  - It can output layout positions only (`-Tjson`, `-Tplain`), so it can
    serve as the layout engine behind our own styling.
- Cons:
  - Its default look is plain or dated, and edge-label placement is
    crude.
  - Its accessibility is only a `<title>` per node.
  - Styling must be imposed, or the model ends up choosing colours.

**Mermaid**
- Pros:
  - It is the most widely adopted form (GitHub, GitLab, Kubernetes,
    MkDocs) and the one models have seen most.
  - Its `accTitle` and `accDescr` give the best accessibility markup.
  - It has many diagram types.
- Cons:
  - The default HTML labels are deleted by our sanitizer (measured), and
    the text mode lost spaces in our raster.
  - Writers trip over its quoting rules (measured).
  - It needs a 2.2 GiB Chromium closure, and has a history of XSS
    advisories.
  - The layout default changed in version 12.
  - Its edge routing is weak on larger graphs (practitioner).
  - Its own users report mobile problems.

**D2**
- Pros:
  - It has the best default look, a readable syntax, and shapes such as
    person and cylinder.
  - It is deterministic and lets you choose the layout engine.
- Cons:
  - It draws wide, so text falls to 9 to 11 px on a phone (measured).
  - The nixpkgs package pulls in 2.2 GiB of Playwright browsers.
  - There is no model benchmark.
  - Its best engine, TALA, is separate and its licence is unconfirmed.

**PlantUML**
- Pros:
  - It has the best measured compile rates for UML types.
  - It is mature, with many diagram types.
- Cons:
  - Our flow came out upside down (measured).
  - Its look is dated.
  - It needs Java (952 MiB).
  - It has an SSRF history when run as a server.
  - It is UML-shaped rather than shaped for ideas.

**TikZ**
- Pros:
  - It gives full control and print quality.
  - Models read it well (VGBench 81%).
- Cons:
  - The model places coordinates by hand, and its figures come out
    simplistic (AutomaTikZ).
  - It needs a large TeX toolchain.
  - It does not adapt to the phone or the theme.
  - Not measured here.

**Hand-written SVG (today's Illustrator output)**
- Pros:
  - Anything can be drawn, and browsers render it natively.
- Cons:
  - Models read it worst (VGBench 55 to 60%) and edit it poorly
    (SVGEditBench v2).
  - Its geometry carries no meaning, and it suffers overlap and clipping.
  - Diffs show coordinate churn, not changes in meaning.
  - It drifts from the text, because nothing ties a box back to a
    concept.
  - Good as generated output, poor as source.

**Penrose, and Excalidraw or draw.io scene JSON**
- Penrose separates meaning from style, which is the right idea, but has
  little evidence and a small ecosystem.
- Excalidraw and draw.io store coordinates. That is ten times the tokens,
  diffs that are hard to read, and editing meant for people with a
  mouse, not for models.

## 5. Ranking for our use, and proposal

Our use is figures that live in vision source files and render in books
read on a phone. Ranked:

1. book-build EDN graph
2. Graphviz DOT
3. D2
4. Mermaid
5. PlantUML
6. TikZ
7. hand-written SVG
8. Excalidraw or draw.io

Proposal (inference from sections 1 to 4):

- **The source.** The figure lives in the vision source file as a
  fenced `figure` EDN block beside the words it illustrates. It holds
  nodes with short labels and a role from the closed vocabulary, edges
  with a verb, groups, and a "proposed" flag.
- **Checking.** book-build validates the block by code before drawing:
  every edge names a node, at most nine nodes, every label short, roles
  from the closed set. A failure goes back to the writer as a concrete
  message. No model looks at the drawing.
- **Drawing.** book-build draws the SVG with the fixed style.
  - Its own layout is kept where it suffices.
  - Graphviz `-Tjson` is the fallback layout engine (140 MiB,
    deterministic, best phone fit in the test). Graphviz only gives
    positions; book-build keeps the styling.
- **What is generated.** The SVG is output, regenerated on each build
  and never edited by hand. The caption states the claim and is the text
  alternative.
- **What is owed.** The vocabulary must be added to the EDN form, the
  first time this proposal is used.
