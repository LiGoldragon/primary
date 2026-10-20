### Proposal 5: Type is no exception, amending Proposal 3 · psyche-context › vision/ethos.md

A single-field variant carries its type's own form; `Type` carries one declaration, so it needs no brace and breaks no rule. The exception the living wants gone is gone by reading, not by a second syntax.

- It is the one ethos with no braces after its variant.
+ `Type` is a single-field variant carrying one declaration, so its payload is the declaration's own form, as any single-field variant's is; it is no exception to the datom.

```ethos
+ Type.                  ; a single-field variant
+   CommitMessage.       ; carrying one declaration
+     [ Landing.{ Topic Vector<Source> }
+       Fix.String ]
```

Ruling: land, amend, or reject.

### Proposal 6: Whitespace after a separator is the reader's rule, beside Proposal 2 · psyche-context › skills/vision-protos.md

Protos owns the only reader, so the line break after the dot is its rule; datom and ethos inherit it, and Proposal 2 keeps its example.

+ Whitespace, a line break included, may follow a separator; the body is the next structure read.

```
+ Head.body
+ Head.
+   body
```

Ruling: land, amend, or reject.

### Proposal 7: When the print breaks after the dot, open · psyche-context › vision/ethos.md

Open: the living allowed the break; where the canonical print makes it is unruled. Written at one default: a body that spans more than one line opens on the line after its dot; a one-line body stays on the dot's line.

+ The canonical print breaks after a dot when the body spans more than one line, and keeps a one-line body on the dot's line.
+ A chain of dots indents by two spaces per link.

```ethos
+ Fix.String                 ; one line: stays
+ Landing.                   ; many lines: breaks
+   { Topic
+     Vector<Source> }
+ Type.                      ; a chain: two
+   CommitMessage.           ;   spaces per link
+     [ Fix.String ]
```

Ruling: land, amend, or reject.

### Proposal 8: A new datom shows its specification · psyche-context › skills/vision-datom.md

+ A datom newly made, or proposed, is shown with its Ethos specification. A datom in production is shown alone: its specification lives in a knowledge module.

```ethos
+ Reply.[ Accepted.Integer   ; the specification,
+         Pending ]          ;   shown with a new datom
```
```
+ Accepted.42                ; the datom
```

Ruling: land, amend, or reject.

### Proposal 9: What can go stale is marked short-term · psyche-context › skills/intent-psyche.md

Intent, so it enters only on your word. Chronos as the golden example, and Flow as what it is built for, are the first lines so marked.

+ A statement that will become stale as the system moves on is marked short-term, in its heading, and is removed when it no longer holds.

```
+ ## Short term: Chronos is the golden example
```

Ruling: land, amend, or reject.
