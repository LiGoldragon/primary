<!-- to-the-living:start -->
Presentation.{ «The Ethos syntax» }

# The Ethos syntax

### Proposal 1: An ethos file is an ordinary datom, in Declaration: File · psyche-context › vision/ethos.md

- An ethos file is written in the sweet form: the root's head, then the sections as siblings, the outer braces omitted.
- The braced form — the root's head opening braces that hold every section — is the canonical form.
- The sweet form is kept out of the main logic run: before the text is read as ethos at all, the file is converted mechanically to the canonical form, so the ethos reader sees only proper ethos.
+ An ethos file is one ordinary datom: its root's variant, the dot, then the braces that hold every section.
+ The braces open on their own line, under the variant; the first section sits on the brace's line.
+ Each root's variant carries its own shape.
- ; the sweet form, as a file is written: the head, then the sections as siblings
- ; the canonical form the reader sees, after the mechanical conversion

```ethos
- Library
- [ protos:String ]               ; imports
- [ Record.{ String Integer } ]   ; types
- []                              ; traits
- []                              ; associations
-
- Library.{
-   [ protos:String ]
-   [ Record.{ String Integer } ]
-   []
-   []
- }
```

```ethos
+ Library.
+ { [ protos:String ]             ; imports
+   [ Record.{ String Integer } ] ; types
+   []                            ; traits
+   [] }                          ; associations
```

Ruling: land, amend, or reject.

### Proposal 2: A dotted form may break onto the next line, in the dot as separator · psyche-context › skills/vision-datom.md

- the dot is the separator, written right after the head, and it opens the body's delimiter.
+ the dot is the separator, written right after the head.
+ A space and a line break may follow the dot, so the body opens on the next line and nesting goes down instead of to the right.
+ Where dotted variants follow one another, each may take a new line, indented under the one before.

```ethos
+ Observed.Locks.[]     ; on one line
+ Observed.             ; or going down
+    Locks.
+       []
```

Ruling: land, amend, or reject.

### Proposal 3: The type ethos, a new section after Declaration: File · psyche-context › vision/ethos.md

+ A type ethos is the variant `Type`, the dot, then the one type it defines: the type's name and its specification.
+ It is the one ethos with no braces after its variant.
+ Every type it needs is declared inline, where it is used; a type from a source comes in by the inline import.
+ A type ethos may carry one or more examples of its datom.

```ethos
+ Type.
+    CommitMessage.[         ; one variant
+       VisionDistillation.  ;   per kind
+          Vector<Reference.{ Topic.String
+                             FlowId.String }> ]
```

```ethos
+ ; datom, a CommitMessage
+ VisionDistillation.[ { ethos 000000 } ]
```

Ruling: land, amend, or reject.

### Proposal 4: Every variant is capitalized, added to Naming · psyche-context › vision/ethos.md

+ Every variant is capitalized, a root's variant and `Type` included: Ethos reads only capitalized symbols as variants.

```ethos
+ Type.       ; a variant: capitalized
+ Library.    ; a root's variant: capitalized
```

Ruling: land, amend, or reject.

### Proposal 5: Type is no exception, amending Proposal 3 · psyche-context › vision/ethos.md

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

+ Whitespace, a line break included, may follow a separator; the body is the next structure read.

```text
+ Head.body
+ Head.
+   body
```

Ruling: land, amend, or reject.

### Proposal 7: When the print breaks after the dot · psyche-context › vision/ethos.md

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
+ Reply.[ Accepted.Integer ; the specification,
+         Pending ]        ; shown with a new datom
```
```text
+ Accepted.42                ; the datom
```

Ruling: land, amend, or reject.

### Proposal 9: What can go stale is marked short-term · psyche-context › skills/intent-psyche.md

+ A statement that will become stale as the system moves on is marked short-term, in its heading, and is removed when it no longer holds.

```text
+  ## Short term: Chronos is the golden example
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
