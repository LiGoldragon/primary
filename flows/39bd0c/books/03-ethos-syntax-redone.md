### Proposal 1: Every example is real code · psyche-context › skills/intent-context-modules.md

Intent, so it enters only on your word. This is the line that was missing when the last edition's examples were written: nothing said an example must be whole and real, only that a statement about code carries code.

+ Every example in a module or a book is real code: whole, canonical, and exactly what the reader accepts. A fragment, a mixture, or a line that would not read is never written.

```ethos
Library.
{
[]                                        ; imports
[ Record.{ String Integer } ]             ; types
[ Summarizable.[ summarize.[ String ] ] ] ; traits
[ Record.[ Summarizable ] ] } ; associations
```

Ruling: land, amend, or reject.

### Proposal 2: An ethos declares the traits its types bear · psyche-context › vision/ethos.md

+ An ethos declares the traits its types bear. Types that bear no trait describe a system that does nothing; such an ethos is not written.

```ethos
Library.
{
[]                                        ; imports
[ Sink.{ String Integer } ]               ; types
[ Summarizable.[ summarize.[ String ] ]   ; traits
  Fillable.[ create:[ Self ] ] ]
[ Sink.[ Summarizable Fillable ] ] } ; associations
```

Ruling: land, amend, or reject.

### Proposal 3: The file form, amending Proposal 1 of the last edition · psyche-context › vision/ethos.md

- The braces open on their own line, under the variant; the first section sits on the brace's line.
+ The dot cares nothing for what follows it: no space, a space, a tab, a line break, any amount.
+ A file's usual form is a break after the dot and a break after the brace, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement. A file that holds a single thing breaks nowhere.

```ethos
Library.
{
[]                                        ; imports
[ Sink.{ String Integer } ]               ; types
[ Summarizable.[ summarize.[ String ] ]   ; traits
  Fillable.[ create:[ Self ] ] ]
[ Sink.[ Summarizable Fillable ] ] } ; associations
```

Ruling: land, amend, or reject.

### Proposal 4: Every variant is capitalized, amending Proposal 4 of the last edition · psyche-context › vision/ethos.md

- Every variant is capitalized, a root's variant and `Type` included: Ethos reads only capitalized symbols as variants.
+ Every variant is capitalized: Ethos reads only a capitalized symbol as a variant.

```ethos
Library.
{
[]                                        ; imports
[ Reply.[ Accepted.Integer                ; types
          Pending ] ]
[ Summarizable.[ summarize.[ String ] ] ] ; traits
[ Reply.[ Summarizable ] ] } ; associations
```

Ruling: land, amend, or reject.

### Proposal 5: A new datom is shown with its specification, replacing Proposal 8 of the last edition · psyche-context › skills/vision-datom.md

+ A datom newly made, or proposed, is shown with its Ethos specification.

```ethos
Library.
{
[]                                        ; imports
[ Reply.[ Accepted.Integer                ; types
          Pending ] ]
[ Summarizable.[ summarize.[ String ] ] ] ; traits
[ Reply.[ Summarizable ] ] } ; associations
```
```
Accepted.42
```

Ruling: land, amend, or reject.
