<!-- to-the-living:start -->
Presentation.{ «The golden ethos», third edition }

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
 │                                          │
 │  example ──► vision-flow-ethos           │
 └──────────────────────────────────────────┘
```

The anatomy of ethos lives in vision-ethos itself;
it is the first golden ethos. Flow's ethos is one
example, in its own skill, pointed to.

## 1. vision-ethos points to Flow

`psyche-skills/skills/vision-ethos.md`, after the
description, before "What Ethos is".

```diff
  dependencies: [knowledge-datom, knowledge-protos]
  ---
+
+ ## Flow, a current best example
+
+ Flow is one of the best current examples of
+ ethos; its ethos lives in the vision-flow-ethos
+ skill, which carries the code.

  ## What Ethos is
```

**Ruling 1.** (a) Land as shown. (b) Amend.

## 2. The Trait section finishes its rename

`psyche-skills/skills/vision-ethos.md`, lines 56
to 63. Long lines wrapped at 52 for display.

```diff
- ## Kind
+ ## Trait

  Trait is the word for the bearer of
  capabilities, the same word in ethos and in
  Rust; kind might be used to also mean traits.
- In ethos there are no generics, only kinds.
- Declaring a new kind
+ In ethos there are no generics, only traits.
+ Declaring a new trait
  declares a new trait in the Rust world and might
  imply more in the ethos world.

- A capability speaks in Self, the kind's own
- parameters and other kinds; a concrete type in
- an input is a kind not yet named.
+ A capability speaks in Self, the trait's own
+ parameters and other traits; a concrete type in
+ an input is a trait not yet named.
```

Fifteen further places in the file still say kind.

**Ruling 2.** (a) This section only. (b) Rename
every place. (c) Leave.

## 3. The ethos of ethos, in vision-ethos

`psyche-skills/skills/vision-ethos.md`, new section
"## The ethos of ethos" after "What Ethos is",
marked a draft until the Psyche::Ethos seat
finishes it. Its text:

```
The anatomy of an ethos file, written in ethos.
The first golden ethos; a draft.

Library
[]                          ; imports: none
[ Name.String               ; types
  Comment.String
  Names.[ One.Name Several.Vector<Name> ]
  Import.{ Name Names }
  Reference.{ Name Vector<Reference> }
  Head.{ Name Vector<Names> }
  Shape.[ Value.Reference   ; value, struct, enum
          Struct.Vector<Position>
          Enum.Vector<Variant> ]
  Position.[ Reference Type ]
  Variant.{ Name Option<Shape> }
  Type.{ Option<Comment> Name Shape }
  Receiver.[ Shared Mutable Absent ]
  Capability.{ Name         ; inputs and yield
               Receiver
               Vector<Reference>
               Reference }
  Constant.{ Name Reference }
  Complex.{ Supertraits.Vector<Head>
            Associated.Vector<Head>
            Constants.Vector<Constant>
            Vector<Capability> }
  Body.[ Simple.Vector<Capability> Complex ]
  Trait.{ Option<Comment> Head Body }
  Association.{ Name Vector<Head> }
  Imports.{ Comment Vector<Import> }
  Types.{ Comment Vector<Type> }
  Traits.{ Comment Vector<Trait> }
  Associations.{ Comment Vector<Association> }
  Library.{ Imports Types Traits Associations } ]
[]                          ; traits: none yet
[]                          ; associations: none
```

Three choices made without a record, for the
Psyche::Ethos seat: whether a one-value type is a
new type (`Value.Reference`); whether a comment is
part of the anatomy, and where; the receiver names
Shared, Mutable, Absent for `.`, `!`, `:`.

**Ruling 3.** (a) Land the draft section. (b) Hold
it until the Psyche::Ethos seat finishes it.
<!-- to-the-living:end -->
