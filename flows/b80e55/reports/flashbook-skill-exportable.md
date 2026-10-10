# Flashbook Skill — Full Stack

A flashbook is a short illustrated book on one subject, published as a
private HTML artifact. It is made from a specification a higher-power seat
writes in its transcript, then handed to a lower-power seat to illustrate
and render.

## Pipeline

1. **Psyche / designer** writes the flashbook source in its transcript under
   an exact heading. Each section has an imagery description, a flowchart
   definition, and 1–6 text items.
2. **High-power auditor** (Fable or equivalent) reviews, adds suggestions.
3. **Low-power illustrator** (Sonnet or equivalent) finds the source by
   title in the designer's transcript, takes the text from its heading to
   the next rule (`---`), and renders it as an HTML artifact. Never edits
   the source text.

## Source format

Write the source as Markdown under a level-1 heading. Each section has
three labelled parts:

```markdown
# Title of the Flashbook

## Section name

### Imagery
One paragraph describing a literal picture. Be explicit — the renderer
trusts these words and produces that image. Name the scene, the objects,
the colors, the feeling. A flowchart may be the illustration when its
connections are given style and drawn as part of the scene.

### Flowchart
An ASCII or structured description of the data flow. Nodes, edges,
comments. On mobile this runs top-to-bottom; on desktop left-to-right.

### Text
1. First point
2. Second point
3. Third point (max 6)

---
```

Verbatim living quotes stay verbatim with a provenance line
(`— living, to <seat>, <date>`). Marks, tensions, and inference notes
stay visible. Proposals on the last page, numbered and checkable.

## Page structure

First page is always an illustration. Pages alternate: illustration, then
at most a small paragraph or a few points (ideally with a flowchart), then
an illustration again. Never two bare charts in a row. Text is minimal; a
page covers one thing.

## Illustration technique

Illustrations are pure inline SVG — the only image format artifacts can
generate. They are literal pictures, not diagrams with labels.

**Style:** organic, artistic, rewarding to look at. Use curved paths
(`<path d="M...C..."/>`), radial and linear gradients, layered semi-
transparent shapes, varied stroke widths, `stroke-linecap: round`,
`stroke-linejoin: round`. No straight-line box-and-arrow diagrams.

**Illustrated flowcharts:** when a flowchart is the illustration, draw it
as a scene — connections become rivers, cables, roots, bridges. Nodes
become objects in a landscape. The data flow has a feeling, not just a
direction.

**Text in SVG:** a title or a few labels at most. Never below 12 px at
drawn scale. Legible in both themes — use `var(--ink)` and `var(--ink2)`.

**Self-describing:** the illustration carries the page's meaning through
imagery alone. No subtext or caption below it. Sometimes the image is
enough without any text.

## Responsive design

Two SVG variants per illustration, hidden/shown by container query:

```css
.svg-landscape { display: block; }
.svg-portrait  { display: none; }

@container page (max-aspect-ratio: 4/3) {
  .svg-landscape { display: none !important; }
  .svg-portrait  { display: block !important; }
}
```

**Portrait (phone):** viewBox ~390×750, `preserveAspectRatio="xMidYMin meet"`.
Flowcharts top-to-bottom. Illustration fills the viewport. 14 px+ font in SVG.

**Landscape (tablet/desktop):** viewBox ~960×540, `preserveAspectRatio="xMidYMid meet"`.
Flowcharts left-to-right. Denser, more context visible.

Use `container-type: size` on each `.page` element so container queries
fire per-page, not per-viewport (more reliable inside an artifact iframe).

## Layout

CSS Grid, not flexbox. `dvh` units for full-height illustration pages.

```css
.page {
  min-width: 100vw;
  height: 100dvh;
  display: grid;
  place-items: center;
  container-type: size;
  container-name: page;
  overflow-y: auto;
  overflow-x: hidden;
}
```

The book is a horizontal strip of pages; `transform: translateX()` slides
between them.

## Template tokens

```css
:root {
  --ground:   #F7F3EB;  --ink:      #3A3530;
  --ink2:     #7A7468;  --accent:   /* one warm hue per book */;
  --gold:     #C9945A;  --green:    #5B7E6B;
  --surface:  #EFEBE2;  --code-bg:  #E8E3D9;
  --border:   #D8D2C6;  --dot:      #C5BFB3;
  --dot-active: var(--accent);
}
```

Redefine only these tokens under `@media (prefers-color-scheme: dark)` guarded
as `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]`.
Body gets `background: var(--ground)`.

**Fonts:** Google Fonts link for Fraunces (display), Source Serif 4 (body),
JetBrains Mono (code). Body text `clamp(0.95rem, 2.2vw, 1.05rem)`, max
68 characters wide. Headings use Fraunces with `text-wrap: balance`.

## Navigation

Page dots, Prev/Next buttons, arrow keys, touch swipe. All in a fixed
bottom bar with a gradient fade from transparent to `var(--ground)`.

```js
// Swipe detection
book.addEventListener('touchstart', e => { tx = e.touches[0].clientX; });
book.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) go(current + (dx < 0 ? 1 : -1));
});
```

## Quality check

Before publishing, screenshot at phone size:

```sh
google-chrome --headless=new --disable-gpu \
  --window-size=390,844 \
  --screenshot=/tmp/flashbook-check.png \
  file:///path/to/flashbook.html
```

Read the screenshot. Fix any: overlapping elements, unreadable text (too
small or wrong color), horizontal scroll, SVG overflow, both-variants
showing, navigation obscuring content. Then publish.

## Subflow brief for the illustrator

```
Render a flashbook from the source titled "<TITLE>" in the transcript of
flow <FLOW_ID>. The source is at <exact heading>. Follow the flashbook
skill: first page is always an illustration. Pages alternate illustration
and text. Use CSS Grid, container queries, dvh units, the template tokens.
Two SVG variants per illustration (portrait and landscape). Illustrations
are organic inline SVG — curved paths, gradients, layered shapes, not
box-and-arrow diagrams. Screenshot at 390×844 before publishing. Publish
as a private artifact with favicon <EMOJI> and title "<TITLE>".
```

## Format variants

Three densities determine what each page shows:

| Density | Portrait | Landscape |
|---------|----------|-----------|
| Low     | Illustration only, full viewport | Illustration with title overlay |
| Medium  | Illustration + 3 key text items below | Illustration left, text right |
| High    | Illustration + full text + code excerpt | Full spread, all elements visible |

The HTML carries all content; CSS container queries select density by
available space. A phone in portrait gets low density. A tablet gets
medium. A desktop gets high.

## Artifact publishing

One private artifact per flashbook, titled by its source title. A
republish keeps its URL. The illustrator reports titles and URLs to the
requester in one message. Favicon is one or two emoji chosen for the
subject.
