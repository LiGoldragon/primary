```
    vision-ethos
    what ethos is, its layout, its two anatomies
         │
         ├── points to ──► vision-flow-ethos
         │                 the Flow Nexus in ethos:
         │                 a current best example
         │
         └── will carry ─► the ethos of ethos
                           the anatomy of an ethos
                           file, written in ethos
```

vision-ethos describes ethos; the code of an
example lives in that example's own skill. The
ethos of ethos below is a first draft: it is what
the golden standard will be, not yet ready.

## 1. vision-ethos points to Flow

`psyche-skills/skills/vision-ethos.md`, after the
description, before "What Ethos is". Shown with
the lines around it.

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
to 63, as they stand after today's landing. Long
lines are wrapped at 52 for display.

```diff
  enables — generator emission among it — comes in
  its time.

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

Fifteen further places in the file still say kind
(section order, examples' comments, the derive
lines, the Kind syntax section).

**Ruling 2.** (a) This section only; kind stays
elsewhere. (b) Rename every place. (c) Leave.

## 3. The ethos of ethos, a first draft

An ethos file whose types describe an ethos file.
Where it lands is the ruling; the draft is for
the Psyche::Ethos seat to finish.

```
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

Three things the draft had to choose without a
record: whether a one-value type is a new type
(here `Value.Reference`); whether a comment is part
of the anatomy, and where; the names of the three
receivers (Shared, Mutable, Absent for `.`, `!`,
`:`).

**Ruling 3.** Where it lands: (a) a section of
vision-ethos, "The ethos of ethos" (b) its own
skill, vision-ethos-anatomy (c) wait for the
Psyche::Ethos seat.
<!-- to-the-living:end -->
