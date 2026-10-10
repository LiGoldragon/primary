# The Visual Idea Publication

*An idea book about idea books. Four boxes. The charts are the flow of the idea; the pictures are made from the charts. This one is run through its own pipeline.*

---

## 1 · The idea is spoken

A psyche speaks an idea out loud. It arrives as words: a little rough, in order of thought, with a shape inside it that the words only half show. The first job is not to draw it. The first job is to find the shape: how many steps, what turns into what, where it loops.

```mermaid
flowchart LR
  V["spoken words\n(rough, in order of thought)"] --> S["the shape inside\nsteps · turns · loops"]
```

---

## 2 · The biggest model writes the book

The biggest model writes a slide book in plain Markdown: one slide per beat, a short paragraph each, and under each paragraph a Mermaid chart. The chart is not decoration. The chart *is* the flow of the idea, the main idea of the meme, drawn as boxes and arrows. Four steps become four boxes. A cycle becomes a ring. The book is already readable here, chart and text inline, before any picture exists.

```mermaid
flowchart TB
  M["biggest model"] --> B["Markdown slide book"]
  B --> P1["slide 1\ntext + chart"]
  B --> P2["slide 2\ntext + chart"]
  B --> P3["slide 3\ntext + chart"]
  B --> P4["slide 4\ntext + chart"]
```

---

## 3 · Two illustrators, one brief, compared

The same book goes to two illustrators: Codex and Opus 5. Each turns every slide's chart plus its text into one picture: a comic panel, a ring of four seasons, four boxes with arrows, whatever the chart's shape asks for. Neither sees the other's work. Then the two books of pictures are laid side by side and the better illustration of each idea is kept. The skill learns from which one was kept.

```mermaid
flowchart LR
  B["the Markdown book"] --> C["Codex\nillustrates"]
  B --> O["Opus 5\nillustrates"]
  C --> K{"compare\nkeep the best"}
  O --> K
  K --> Sk["the skill\nlearns"]
```

---

## 4 · Two ways to read it

The result reads two ways. In the Markdown, with the pictures inline, the idea is a document: text, chart, picture, next. As slides on their own, it is a deck to show. Both are the same book. This page is the first run: written by the biggest model, sent to both illustrators, and the pictures you see beside it are whichever won.

```mermaid
flowchart TB
  Bk["one book"] --> D["read as a document\ntext · chart · picture inline"]
  Bk --> Sl["shown as slides\npictures on their own"]
```

---

*Source: the living's words of 2026-09-16 in flows/f55ec8/vision/visualPublication.md.*
