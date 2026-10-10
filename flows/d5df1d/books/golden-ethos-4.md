<!-- to-the-living:start -->
Presentation.{ «The golden ethos, fourth edition» }

## The vision of ethos as it stands

This is the current vision of ethos: it opens with Flow
as the best current example, then the graph of where the
golden ethos lives, and it says trait throughout. Its
opening lines:

```text
---
description: An ethos file is written, or a type,
trait or layout is judged against what the living
wants ethos to be.
dependencies: [knowledge-datom, knowledge-protos]
---

## Flow, a current best example

Flow is one of the best current examples of ethos;
its ethos lives in the vision-flow-ethos skill,
which carries the code.

## Where the golden ethos lives
```

```
┌──────────────────────────────────────────┐
│ vision-ethos                             │
│                                          │
│  what ethos is · its layout              │
│  its two anatomies: types and traits     │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ the ethos of ethos                 │  │
│  │ the types an ethos file is made of │  │
│  │ the first golden ethos             │  │
│  └────────────────────────────────────┘  │
└───────────────────┬──────────────────────┘
                    │ example
                    ▼
        ┌───────────────────────┐
        │ vision-flow-ethos     │
        │ the Flow Nexus, in    │
        │ ethos; its own skill  │
        └───────────────────────┘
```

```text
The anatomy of ethos lives in vision-ethos itself,
as the first golden ethos; Flow's ethos is one
example, in its own skill.
```

The inner box of the graph, the ethos of ethos, is the
one section not yet written. The proposal below writes it.

## Distillation

### 3. The ethos of ethos, in vision-ethos

Target: `psyche-skills/skills/vision-ethos.md`, a new
section after "## What Ethos is", before "## Why Ethos".

Removed: none.

Above, unchanged:

```text
## What Ethos is

Ethos is the schema language. Of the two main
syntaxes most agents will face, Ethos specifies the
types and Datom fills them with data.

Ethos is central. The anatomy of the system, every
type and every trait it uses, is read in its ethos;
an implementation is mostly the hand-written bodies.
```

Added, prose:

```text
## The ethos of ethos

The anatomy of an ethos file, written in ethos.
The first golden ethos; a draft.
```

Added, the block that follows that prose:

```
Library
[]                             ; imports: none
[  Name.String                 ; types
   ; 4b: core:Name, waiting on
   ;     the inline-import book
   Comment.String
   Names.[
      One.Name
      Several.Vector<Name> ]
   Import.{
      Name
      Names }
   Reference.{
      Name
      Vector<Reference> }
   Head.{
      Name
      Vector<Names> }
   Shape.[                     ; value, struct, enum
      Value.Reference
      Struct.Vector<Position>
      Enum.Vector<Variant> ]
   Position.[
      Reference
      Type ]
   Variant.{
      Name
      Option<Shape> }
   Type.{
      Option<Comment>
      Name
      Shape }
   Receiver.[
      Shared
      Mutable
      Absent ]
   Capability.{                ; inputs and yield
      Name
      Receiver
      Vector<Reference>
      Reference }
   Constant.{
      Name
      Reference }
   Complex.{
      Supertraits.Vector<Head>
      Associated.Vector<Head>
      Constants.Vector<Constant>
      Vector<Capability> }
   Body.[
      Simple.Vector<Capability>
      Complex ]
   Trait.{
      Option<Comment>
      Head
      Body }
   Association.{
      Name
      Vector<Head> }
   Imports.{
      Comment
      Vector<Import> }
   Types.{
      Comment
      Vector<Type> }
   Traits.{
      Comment
      Vector<Trait> }
   Associations.{
      Comment
      Vector<Association> }
   Library.{
      Imports
      Types
      Traits
      Associations } ]
[]                             ; traits: none yet
[]                             ; associations: none
```

Below, unchanged:

```text
## Why Ethos
```

What the types are. A Name is a word, a Comment its plain
text. Names is one name or a bracket of names, as an
import brings `protos:String` or `protos:[ String Integer ]`.
A Reference is a name with its angle arguments, as
`Vector<Name>`; a Head is a name with its constraints, as
a trait's identity. A Type is a name and a Shape: a value,
a struct of positions, or an enum of variants. A Trait is
a head and a body, simple (capabilities only) or complex
(supertraits, associated types, constants, capabilities).
A Library is its four sections, each a comment and its
declarations.

Every rule the block follows is already ruled: trait as
the word (flows/ebbe30/vision/ethos.md, 2026-10-09); a
type of one value written `Name.Type` is a new type, and
no struct holds one position (flows/ebbe30/vision/ethos.md,
2026-10-09; flows/d4ae97/vision/ethos.md, 2026-10-06);
three spaces of indentation (flows/f5a6e9/vision/ethos.md,
2026-10-07); each element on its own indented line, a
comment above or beside what it comments on
(flows/e5a0bc/vision/ethos.md, 2026-10-06 and 2026-10-07).

Four choices inside the block are open:

1. `Value.Reference`: the shape of a type written
   `Name.Type`, a new type over one reference, is named
   Value.
2. A comment is part of the anatomy: a Type and a Trait
   may carry one, and each of the four sections carries
   one.
3. The receiver of a capability is named Shared for `.`,
   Mutable for `!`, Absent for `:`.
4. Name, the type every name in the block uses:
   (4a) `Name.String`, as the block has it; (4b) Name as
   the core built-in reached by the inline import you
   opened, `core:Name`, a camelCaseExpression type checked
   when one is made (flows/d5df1d/vision/ethos.md,
   flows/445410/vision/flow.md, 2026-10-09). The block
   shows 4b on the comment line beneath `Name.String`;
   it waits on the inline-import book.

**Ruling 3.** Land the section as shown, or amend it by
the number of the choice.
<!-- to-the-living:end -->
