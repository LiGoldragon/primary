Presentation.{ «A payload keeps the layout of the datom around it» Proposal }

# A payload keeps the layout of the datom around it

Created by Fable 5.1, on the living's words.

### Proposal 1: The margin · psyche-belief › vision/protos.md

::: comment
A Markdown module, or any text of many lines, placed inside a datom would flatten the datom to column zero, and the visual layout of the containing data would be lost. So the payload is indented like any element under its delimiter, and the margin is removed at the protosic layer, before any inner reading: what the conceptual layer and whatever library reads the text receive is the text as it stands in a file. The margin is a delimiter fact, known from the opening delimiter's column before a byte of the payload is read, so nothing is inferred from the content.
:::

+ ## Margin

+ An opaque structure, a string or a Meaning, may span lines. When its opening delimiter ends its line, the payload is indented: every payload line begins with the margin, the opening delimiter's column plus the one step at which the canonical print hangs an element under its delimiter, and the closing delimiter stands alone at the opening delimiter's column. Protos removes the margin as it reads and writes it as it prints, so the payload the conceptual layer receives is byte for byte the text as it stands in a file, and the datom around it keeps its layout. A blank line is exempt. A payload line indented less than the margin is an error. An opening delimiter followed by content on its own line opens an ordinary structure, with no margin.

```datom
+ ; a Meaning of several lines inside a struct: the opening delimiter ends its line,
+ ; the payload hangs two columns in, the closing delimiter stands at the opening one's column
+ { { Vision fieldAspect }
+   ⟪
+     # The Field aspect

+     A Field flow keeps the running system.

+     ```datom
+     Send.{ { Psyche core Fable } Soft.Notice.«The build is green.» }
+     ```
+   ⟫ }
+ ; what the conceptual layer receives: the payload at column zero
+ ; # The Field aspect
+ ;
+ ; A Field flow keeps the running system.
+ ; …
```

```mermaid
+ flowchart TB
+     t["text: the datom with its payload indented"] -- "protos: the delimiter, its column, the margin removed" --> s["one opaque structure, the payload flat"]
+     s -- "the conceptual layer: placed in its position" --> v["the value, a SemaZero or a String"]
+     v -- "the translator: the library that reads that text" --> r["the reading"]
```
