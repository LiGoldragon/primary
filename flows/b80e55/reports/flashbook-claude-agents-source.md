# How to Make a Flashbook for Claude Agents

## The Pipeline

### Imagery
A mountain river flowing through three landscapes seen from above. At the
peak, a figure sketches on luminous paper — the sketches glow warm amber.
The paper floats downstream on the current. Midway, a second figure on a
stone bridge catches each sheet, reads it, adds marks in a deeper ink,
and releases it onward. At the river's mouth, a third figure in a
workshop by the sea takes each annotated sheet, and around them vivid
murals bloom on the workshop walls — the words becoming pictures. The
river is golden-brown, the peak is cold blue-grey, the workshop glows
with warm lamplight. Three stations, one flow of water carrying the work
downstream.

### Flowchart
```
Designer (Psyche)
    │ writes source in transcript
    ▼
Auditor (Fable / High)
    │ reviews, adds suggestions
    ▼
Illustrator (Sonnet / Low)
    │ renders as HTML artifact
    ▼
Published Flashbook
```
Comments: each station is a power tier. The source flows downstream
without being edited. The illustrator trusts the imagery descriptions
and produces them literally.

### Text
1. A flashbook starts as sections written in a designer's transcript
2. A high-power seat audits — catching gaps, adding suggestions
3. A low-power seat illustrates and renders the final artifact
4. The source text is never changed by the renderer

---

## The Source Format

### Imagery
A craftsman's workbench with three compartments carved into its surface,
each holding a different material. The left compartment holds a sheet of
translucent paper with a watercolor landscape visible through it — this
is the imagery description. The center compartment holds a brass
mechanism with interlocking gears and flowing channels — this is the
flowchart. The right compartment holds a small stack of cards, each with
a single sentence — these are the text items. Above the bench, a sign in
warm lettering reads the section name. The bench is old oak, the brass
is polished, the cards are cream with ink edges.

### Flowchart
```
Section
├── Imagery: one paragraph describing a literal picture
├── Flowchart: nodes, edges, comments, data flow
└── Text: 1–6 points, each covering one thing
```
Comments: each section becomes two pages — an illustration page from the
imagery, and a text page from the points. The flowchart may be woven
into the illustration or stand beside the text.

### Text
1. Each section has three parts: imagery, flowchart, text
2. The imagery paragraph is explicit — the renderer produces exactly what it says
3. Verbatim living quotes stay verbatim with provenance
4. Proposals go on the last page, numbered and checkable

---

## The Illustration

### Imagery
Two pictures side by side, divided by a vertical crack of light. On the
left, a stark diagram: grey boxes connected by thin straight arrows on a
white grid, labels in small sans-serif — clinical, lifeless, the kind of
chart nobody remembers. On the right, the same data transformed: the
boxes have become stone buildings on a hillside, the arrows are paths
winding between them with travellers walking, the labels are carved into
wooden signs. Trees grow between the buildings, light falls through
clouds, smoke rises from a chimney. Same information, one dead, one
alive. The crack of light between them pulses warm gold.

### Flowchart
```
Geometric diagram ──X──► Illustrated scene
    boxes                   buildings
    arrows                  winding paths
    labels                  carved signs
    grid                    hillside landscape
```
Comments: the X marks what we reject. An illustration IS a picture.
Curved SVG paths, gradients, layered shapes. 12px+ text. Self-describing.

### Text
1. Illustrations are pure inline SVG — the only image format we can generate
2. Organic shapes: curved paths, gradients, layered transparency, rounded strokes
3. An illustrated flowchart draws its connections as part of a scene
4. Self-describing — the image carries meaning without subtext
5. Never below 12px text at drawn scale, legible in both themes

---

## The Responsive Split

### Imagery
A single sheet of paper being folded into two shapes by invisible hands.
On the left fold, the paper becomes a tall narrow portrait — a waterfall
tumbling top to bottom, with nodes of the flowchart sitting in pools
along the falls, connected by the cascading water. On the right fold,
the same paper opens into a wide landscape — a river delta seen from
above, the same nodes sitting on islands, connected by branching
channels flowing left to right. Both folds show the same five nodes and
the same connections, but the water finds a different path for each
shape. The paper itself is cream; the water is teal and gold.

### Flowchart
```
Portrait (phone)              Landscape (desktop)
┌─────────┐                   ┌──────────────────────┐
│  Node A  │                   │ Node A ─── Node B    │
│    │     │                   │   │          │       │
│  Node B  │                   │ Node C ─── Node D    │
│    │     │                   │              │       │
│  Node C  │                   │          Node E      │
│    │     │                   └──────────────────────┘
│  Node D  │
│    │     │
│  Node E  │
└─────────┘
Top to bottom               Left to right
```
Comments: two SVGs per illustration, hidden/shown by container query.
Portrait: viewBox 390×750, fills viewport. Landscape: viewBox 960×540.

### Text
1. Two complete SVG variants per illustration — portrait and landscape
2. CSS container queries select by aspect ratio, not pixel width
3. Portrait flowcharts run top-to-bottom; landscape runs left-to-right
4. The illustration fills the phone screen — no scrolling to see it
5. Container queries are more reliable than media queries inside artifact iframes

---

## The Template

### Imagery
A typesetter's case — a shallow wooden drawer divided into dozens of
compartments, each holding a different element. In the largest
compartments: three typefaces, each represented by a carved wooden block
showing its character. Fraunces is ornate and warm, its block dark
walnut. Source Serif 4 is steady and readable, its block lighter maple.
JetBrains Mono is precise, its block steel-inlaid. Smaller compartments
hold color swatches: cream grounds, warm inks, a single accent hue
(copper, teal, or moss — one per book). The drawer sits on a broad desk
beside a stack of cream paper. On the wall, two swatches show the same
page in light and dark theme.

### Flowchart
```
:root tokens
├── --ground   #F7F3EB / #1E1D1B
├── --ink      #3A3530 / #E8E2D8
├── --accent   (one per book)
├── --surface  #EFEBE2 / #2A2826
└── --border   #D8D2C6 / #3E3B36

Fonts
├── Fraunces      → display headings
├── Source Serif 4 → body prose, max 68ch
└── JetBrains Mono → code, labels
```
Comments: CSS custom properties on :root, redefined for dark theme.
Google Fonts loaded via stylesheet link. Body text uses clamp() for
responsive sizing.

### Text
1. CSS custom properties define the palette — one accent hue per book
2. Both themes: light tokens on bare :root, dark under prefers-color-scheme
3. Fraunces for display, Source Serif 4 for body, JetBrains Mono for code
4. Body text max 68 characters wide, sized with clamp()
5. CSS Grid for layout, dvh units for full-height pages

---

## The Quality Gate

### Imagery
A magnifying glass held over a small glowing rectangle — a phone screen.
Through the glass, every detail is sharp: the text is readable, the
illustration fills the frame, the colors are true. Around the magnifying
glass, a ring of checkmarks in warm green, each labelling a quality: "no
overlap," "text ≥ 12px," "one SVG showing," "no sideways scroll," "nav
visible." Below the phone, a terminal window shows the command that
captured the image, its cursor blinking. The whole scene is on a dark
desk surface, the phone's light casting a warm pool.

### Flowchart
```
Write HTML
    │
    ▼
Screenshot at 390×844
    google-chrome --headless=new --window-size=390,844 --screenshot=...
    │
    ▼
Read screenshot ──► glitch? ──► fix ──► screenshot again
    │ no
    ▼
Publish artifact
```
Comments: the quality gate runs before every publish. Phone-first. One
look, one fix pass, then ship. The live page is the review surface.

### Text
1. Headless Chrome screenshots at phone dimensions before publishing
2. Check: overlapping elements, unreadable text, wrong SVG variant showing
3. Check: horizontal scroll, navigation obscuring content, theme legibility
4. One fix pass after the screenshot, then publish — the live page is the review surface

---

## Subflows and Dispatch

### Imagery
A dispatcher's office with a large board on the wall. The board has
slots for tasks, each slot holding a card with a title and a colored
tag. A dispatcher sits at the desk, writing a brief on a card — it
names the source title, the flow ID, the illustration style, the
template, the screenshot command. They slide the card into a pneumatic
tube that whooshes it to the workshop below. Through a window in the
floor, the workshop is visible: an illustrator at a drawing table,
surrounded by finished pages pinned to the walls, working on a new SVG
with curves and gradients flowing from their pen. A finished flashbook
sits on a side table, its pages fanned open, glowing.

### Flowchart
```
Designer writes source in transcript
    │
    ▼
Designer writes subflow brief:
    - source title and location
    - flow ID and directory
    - illustration style guidance
    - template tokens to use
    - screenshot command
    - artifact title and favicon
    │
    ▼
Low-power subflow:
    - finds source by title
    - builds HTML with template
    - draws SVG illustrations
    - screenshots and checks
    - publishes artifact
    - reports URL back
```
Comments: the brief is specific. The subflow doesn't decide the style
or the subject — it renders what the brief describes.

### Text
1. The designer dispatches illustration to a low-power subflow
2. The brief names everything: source title, style, template, screenshot command
3. The subflow finds the source, builds, screenshots, publishes
4. One message back: title and URL — the flashbook is done
