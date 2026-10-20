<!-- to-the-living:start -->
Presentation.{ «The Ethos syntax, 2nd edition» }

# The Ethos syntax, 2nd edition

### Proposal 1: The file form, amending Proposal 1 of the last edition · psyche-context › vision/ethos.md

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
; associations
[ Sink.[ Summarizable Fillable ] ] }
```

Ruling: land, amend, or reject.

### Proposal 2: An ethos declares the traits its types bear · psyche-context › vision/ethos.md

+ An ethos declares the traits its types bear. Types that bear no trait describe a system that does nothing; such an ethos is not written.

```ethos
Library.
{
[]                                        ; imports
[ Sink.{ String Integer } ]               ; types
[ Fillable.[ create:[ Self ]              ; traits
             drain![ Vector<String> ] ] ]
; associations
[ Sink.[ Fillable ] ] }
```

Ruling: land, amend, or reject.

### Proposal 3: Every variant is capitalized, amending Proposal 4 of the last edition · psyche-context › vision/ethos.md

- Every variant is capitalized, a root's variant and `Type` included: Ethos reads only capitalized symbols as variants.
+ Every variant is capitalized: Ethos reads only a capitalized symbol as a variant.

```ethos
Library.
{
[]                                        ; imports
[ Layer.[ Primary Secondary               ; types
          Tertiary Quaternary ] ]
[ Titled.[ title.[ String ] ] ]           ; traits
; associations
[ Layer.[ Titled ] ] }
```

Ruling: land, amend, or reject.

### Proposal 4: A new datom is shown with its specification, replacing Proposal 8 of the last edition · psyche-context › vision/datom.md

+ A datom newly made, or proposed, is shown with its Ethos specification.

```ethos
Library.
{
[]                                        ; imports
[ Reply.[ Accepted.Integer                ; types
          Pending ] ]
[ Summarizable.[ summarize.[ String ] ] ] ; traits
; associations
[ Reply.[ Summarizable ] ] }
```

```datom
Accepted.42
```

Ruling: land, amend, or reject.

### Proposal 5: An enum has two variants or more · psyche-context › vision/ethos.md

+ An enum has two variants or more; an enum of one variant is refused.

```ethos
Library.
{
[]                                        ; imports
[ Outcome.[ Accepted.Integer              ; types
            Refused.String ] ]
[ Summarizable.[ summarize.[ String ] ] ] ; traits
; associations
[ Outcome.[ Summarizable ] ] }
```

Ruling: land, amend, or reject.

### Proposal 6: The traits of a Type ethos · psyche-context › vision/ethos.md

+ A Type ethos declares a type that bears only the two datom traits every declared type bears.
+ A type that bears any other trait is declared in a Library, where its traits and associations are written.

```ethos
Type.CommitMessage.[ Landing.Vector<String>
                     Fix.String ]
```

```ethos
Library.
{
[]                                        ; imports
[ CommitMessage.[ Landing.Vector<String>  ; types
                  Fix.String ] ]
[ Summarizable.[ summarize.[ String ] ] ] ; traits
; associations
[ CommitMessage.[ Summarizable ] ] }
```

Ruling: land, amend, or reject.

### Proposal 7: A line break after a dot keeps the structure whole · psyche-context › vision/protos.md

+ Whitespace after a separator never ends a structure: a head, its dot and the body on the next line are one structure, so `[ a. b ]` holds one structure, `a.b`, not two words.

```ethos
Library.
{
[]                                        ; imports
[ Record.{ String Integer } ]             ; types
[ Summarizable.                           ; traits
     [ summarize.[ String ] ] ]
; associations
[ Record.[ Summarizable ] ] }
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
