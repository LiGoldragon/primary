# The type ethos

## Where things stand

Every ethos file today opens with one of four
roots, Library, Signal, Operation or Memory, and
holds its declarations in sections: imports first,
then the root's own sections. The type file is a
fifth kind of ethos file. Its head word is `type`,
it defines exactly one type, and every type that
one type needs is defined inline, in place, with
the inline import where a type comes from a source.
Its first use is the commit message written as a
datom.

```
┌──────────────────────────────────────────┐
│ the four roots today                     │
│ Library  Signal  Operation  Memory       │
│ each a file of sections:                 │
│ imports, then the root's own sections    │
└────────────────────┬─────────────────────┘
                     │ a fifth kind of file
                     ▼
┌──────────────────────────────────────────┐
│ the type file                            │
│ head: type                               │
│ one type                                 │
│ helper types inline, where used          │
│ imports inline, where a source is named  │
└────────────────────┬─────────────────────┘
                     │ first use
                     ▼
┌──────────────────────────────────────────┐
│ a commit message in datom                │
│ VisionDistillation.[ { ethos 081064 } ]  │
└──────────────────────────────────────────┘
```

Nothing of the type file is in production or in a
development branch, and no generator work is
ordered. The current generator refuses a file whose
head word is `type` as an unknown root, so nothing
below has been accepted by the current generator.

The living's words this serves are in
flows/081064/vision/ethos.md, 2026-10-10, "the type
ethos, and commit messages in datom" and "the
commit message as a variant with a struct". The
inline import it uses is the statement now in the
Imports section of psyche-skills/vision/ethos.md.

## The type file, on its first use

The file is
flows/081064/reports/type-ethos/commit.type.ethos.
Its whole text:

```
; the head: a type file, one type
type
; the one type: an enum, one variant per kind
CommitMessage.[
  ; a distillation's references: a vector
  VisionDistillation.Vector<
    ; of Reference, named and declared in place
    Reference.{
      ; type check: open book «The prototype name»
      Topic.String
      ; flow id: a String for now
      FlowId.String }>
  ; a mixed commit: a vector of the same enum
  Mixed.Vector<CommitMessage> ]
```

What each construct is, and why it is there:

`type` is the head word. It plays the part a root
plays (Library, Signal, Operation, Memory), but it
is lowercase, as the living spoke it. The flow
notes that a lowercase word fits the casing rule in
the open book «The prototype name»: a name that is
not a type or a trait is camelCase. That reading is
the flow's.

`CommitMessage.[ … ]` is the one type the file
defines. A bracket where a type is defined is an
enum, so CommitMessage is an enum and each variant
is one kind of commit. The living encourages one
variant per commit message.

`VisionDistillation.Vector<…>` is the variant whose
payload is declared inline. Here it is a vector:
the references of one vision distillation.

`Reference.{ Topic FlowId }` is a struct of two
positions, a topic and a flow id, declared in place
and named Reference. It has two fields, so it is
not a single-field struct, which the living has
ruled out. It is named because the current
generator refuses an unnamed struct inside a type
argument. Declaring the named struct inside the
angle brackets, rather than as a separate
declaration, is the flow's design; the current
generator has neither accepted nor refused it.

`Topic.String` is an alias declared in place. The
topic stays a String for now, with a comment line
saying its checked type is the question of the open
book «The prototype name».

The inline import, shown only as the flow's
illustration of the form and not a real source:
`FlowId.flow:FlowId` declares FlowId over the type
FlowId from a source named flow, with no imports
section.

`FlowId.String` is an alias declared in place. The
flow id stays a String for now.

`Mixed.Vector<CommitMessage>` holds a commit that
carries several kinds, as a vector of the same
enum. It names itself, as `Lock.{ … Option<Lock> }`
does in vision-ethos. Choosing a Mixed variant over
a top-level vector is the flow's choice; question 5
asks for the ruling.

## The datom under it

A commit message is one value of CommitMessage. The
commit of this book's landing would read:

```
; datom, in a position expecting CommitMessage
VisionDistillation.[ { ethos 081064 } ]
```

The hub's book «Sources in the commit message»
shows a commit message whose first line is
`vision-distillation`, then four lines, each a flow
id and a topic: `b675f3d9 visionImpurities`,
`acbb6006 distillation`, `b675f3d9 distillation`,
`ac1e9ec8 distillationNegatives`. Its datom
counterpart, the topic first as Reference orders
it:

```
; datom, in a position expecting CommitMessage
VisionDistillation.[
  { visionImpurities b675f3d9 }
  { distillation acbb6006 }
  { distillation b675f3d9 }
  { distillationNegatives ac1e9ec8 } ]
```

The canonical print would put the first reference
on the opening line and hang the others beneath it.
Here the first reference starts a new line so each
line stays within 52 characters.

A mixed commit, under the Mixed variant. Only
VisionDistillation is named so far, so this example
holds two distillations in one commit:

```
; datom, in a position expecting CommitMessage
Mixed.[ VisionDistillation.[ { ethos 081064 } ]
        VisionDistillation.[ { nexus 73ada7 } ] ]
```

## Wrong and right

Wrong: the helper types declared in a Library
elsewhere, and the type file importing them. The
type is then no longer read whole in its one file.

```
; flows.library.ethos
Library
[]                       ; imports
[ Reference.{ Topic      ; types
              FlowId } ]
[]                       ; traits
[]                       ; associations

; commit.type.ethos
type
CommitMessage.[ VisionDistillation.Vector<
                  flows:Reference> ]
```

Wrong: two types in one type file. The file
defines exactly one.

```
type
Reference.{ Topic.String
            FlowId.String }
CommitMessage.[ VisionDistillation.Vector<
                  Reference> ]
```

Wrong: an unnamed struct inside a type argument.
Refused by the current generator.

```
type
CommitMessage.[ VisionDistillation.Vector<{
                  Topic.String
                  FlowId.String }> ]
```

Right: one type, its helpers named and declared
inline where they are used.

```
type
CommitMessage.[ VisionDistillation.Vector<
                  Reference.{
                    Topic.String
                    FlowId.String }> ]
```

## Questions on the anatomy

1. The layout of the type file: sections, or a
   single declaration? The flow's file has no
   sections. After `type` comes the one
   declaration, and its helpers sit inside it.
   With sections, the file would read `type`, then
   `[]` for imports, then `[ CommitMessage.[ … ] ]`,
   one bracket holding one type. The flow infers
   that the canonical braced form of the
   single-declaration layout is
   `type.{ CommitMessage.[ … ] }`.

2. May a type file import from a Library by an
   imports section, or only inline? On the example:
   could `Reference` come in as
   `[ flows:Reference ]` in an imports section? Or
   is only the inline import, as in the illustration
   `FlowId.flow:FlowId`, allowed? The first wrong form above
   assumes inline only.

3. What does the generator yield for a type file?
   One answer is a Rust module with one public
   type, CommitMessage. The flow notes that the
   helpers must then be public as well: a field of
   type Reference in a public enum needs Reference
   to be public, and that includes the aliases
   Topic and FlowId. The other answer is nothing
   yet: the ethos shows, as the living said, and
   the generator waits.

4. Which commit-message variants beyond
   VisionDistillation should be named now? Three
   candidates: a landing of code, a book, a psyche
   record. Or are they left for later? On the
   example, each would be one more variant beside
   VisionDistillation in `CommitMessage.[ … ]`.

5. A mixed commit: a top-level vector of variants,
   or a Mixed variant? The flow's file uses
   `Mixed.Vector<CommitMessage>`, so a single-kind
   commit stays bare, as in
   `VisionDistillation.[ … ]`. A top-level vector
   would make every commit a vector,
   `[ VisionDistillation.[ … ] ]`, with one element
   encouraged. Or the file would have to define a
   second type, which a type file forbids. The
   Mixed form also allows a Mixed inside a Mixed,
   which nothing here needs.

## Proposal: the type file in vision-ethos

Target: psyche-skills/vision/ethos.md, a new section
"## The type file" between the end of "## Roots"
and "## Non-repetition".

Above, as it stands:

Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.

Added:

```diff
+## The type file
+
+A type file defines a single type. It starts with
+the head word `type`, then the one type; every type
+that one type needs is defined inline, where it is
+used, and a type from a source comes in by the
+inline import.
+
+```
+; the head: a type file, one type
+type
+; the one type: an enum, one variant per kind
+CommitMessage.[
+  ; a distillation's references: a vector
+  VisionDistillation.Vector<
+    ; of Reference, named and declared in place
+    Reference.{
+      ; type check: open book «The prototype name»
+      Topic.String
+      ; flow id: a String for now
+      FlowId.String }> ]
+```
+```
+; datom, in a position expecting CommitMessage
+VisionDistillation.[ { ethos 081064 } ]
+```
+
```

Below, as it stands:

## Non-repetition

The example omits the Mixed variant, which waits
on question 5, and the checked type of Topic waits on
«The prototype name».

## Distillation

- psyche-skills/vision/ethos.md: a new section
  "## The type file", with the statement, the
  ethos example and the datom line above, placed
  between the end of "## Roots" and
  "## Non-repetition".

It distils flows/081064/vision/ethos.md,
2026-10-10, "the type ethos, and commit messages in
datom" and "the commit message as a variant with a
struct". No Sources line is added to the skill. The
landing commit's message will list `081064 ethos`.

## Ruling

1. The statement "## The type file" lands in
   vision-ethos as proposed, or amended.
2. Question 1: a single declaration, or sections.
3. Question 2: inline imports only, or an imports
   section too.
4. Question 3: a Rust module with its helpers
   public, or nothing yet.
5. Question 4: the variants to name now, or later.
6. Question 5: a Mixed variant, or a top-level
   vector.
