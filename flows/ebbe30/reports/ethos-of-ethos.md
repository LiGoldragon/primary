# ethos-of-ethos

First draft: a Library whose types describe an ethos
Library file. Source only; not read by ethos-zero.

~~~
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
  Complex.{ Supertraits.Vector<Head> ; complex trait
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
~~~

## What each part instantiates

P is psyche-skills skills/vision-ethos.md at HEAD
f9d74b, with the kind-to-trait rename of trait-
rename.md read into it; line numbers are HEAD's.

- Library root, sweet form, section order imports,
  types, traits, associations: P:25, P:30,
  P:107-114, P:119-121.
- Name.String: P:64-67 (names are words);
  Comment.String: P:446.
- Names, one name or a bracket of names: P:142-143
  (`protos:String`, `protos:[ String Integer ]`),
  P:76 (a constraint is a trait or a bracket of
  traits).
- Import.{ Name Names }, the source then what it
  brings: P:142-145.
- Reference.{ Name Vector<Reference> }, a name with
  its angle arguments: P:172, P:363, P:144-145
  (intrinsics need no import).
- Head.{ Name Vector<Names> }, a name with its
  constraints: P:74-80, P:403-404; also an
  associated type with its constraints: P:379,
  P:389.
- Shape.[ Value Struct Enum ]: P:161-165, P:171-173,
  P:244-246, P:303-304 (where types are defined a
  bracket is an enum).
- Position.[ Reference Type ], a struct position
  holding a type by name or declaring one in place:
  P:188, P:215, P:219-220 (a bare variant named as a
  defined type carries it).
- Variant.{ Name Option<Shape> }, bare or carrying:
  P:219-220, P:244-246.
- Type.{ Option<Comment> Name Shape }: P:161-165,
  P:446.
- Receiver.[ Shared Mutable Absent ]: P:354-355.
- Capability.{ Name Receiver Vector<Reference>
  Reference }: P:353-357, P:62.
- Constant.{ Name Reference }: P:380-381, P:390.
- Complex.{ supertraits, associated types,
  constants, capabilities }: P:378-381.
- Body.[ Simple Complex ]: P:353, P:378.
- Trait.{ Option<Comment> Head Body }: P:74-86,
  P:327-331.
- Association.{ Name Vector<Head> }: P:328-329,
  P:407-412.
- Imports, Types, Traits, Associations, each a
  Comment and its declarations: P:119-121, P:446.
- Empty traits and associations sections: P:327-331
  (traits are declared, never inferred).
- Layout, spacing and comments of the block itself:
  P:440-446.

## Open questions

1. Alias or new type. The brief asks for a new type
   over one value; P:269-271 says an alias is not a
   new type and carries no derive. The block names
   the variant Value. Which is it, and what is its
   name?
2. In-place declaration in a struct position
   (`Supertraits.Vector<Head>`,
   `Constants.Vector<Constant>`). P:188-191 shows
   inline types only as variant payloads with a
   derived underscore name; the named in-place form
   comes from knowledge-ethos (deployed ethos-zero),
   not from vision. Does vision take it?
3. Used-once types declared by name. P:215 says a
   type used once is declared inline; the block
   names Import, Position, Variant, Receiver,
   Constant, Complex, Body, Trait, Association and
   the four section types, because inline nesting
   inside 52 characters does not fit. Which wins,
   the inline rule or the width?
4. A variant payload declared apart. Body.[
   Simple... Complex ] carries Complex by the
   defined-type rule (P:219-220), while P:215 says a
   payload is written in the variant and no second
   type holds it.
5. Comment as anatomy. Vision says where comments go
   in text (P:446) but not whether a comment is data
   in the anatomy, which elements carry one, or its
   position. The block gives every section a
   required Comment first and every type and trait
   an optional one first; variants, positions,
   capabilities and associations carry none.
6. Receiver variant names. Vision names only the
   glyphs `.`, `!`, `:` (P:355); Shared, Mutable and
   Absent are the draft's.
7. One capability anatomy. P:356-357 gives two text
   forms; the block holds one shape and leaves the
   print to choose the bracket form when the inputs
   are empty. A capability yielding nothing is not
   covered (P:357 a yield bracket holds one type).
8. Supertraits by head or by name. P:378-379 shows
   names only (`[ Fillable ]`); the block takes
   heads, so a supertrait may carry constraints.
9. An association naming a constrained trait.
   P:408-409 shows bare trait names; the block takes
   heads, after the identity rule P:74-80.
10. Constant names are upper case (P:380); Name does
   not carry case. Where is case held?
11. Roots. Only Library is described; Signal,
   Operation and Memory (P:25-30, P:301-306) and a
   sum over the roots are not.
12. Sweet and canonical form. The block describes
   the anatomy both forms share; whether the ethos
   of ethos also describes the sweet form, or only
   the canonical one the reader sees (P:111-114), is
   open.
13. A type named Library declared inside a Library
   root: does a declared name colliding with a root
   head matter?
14. The anatomy's own traits. The traits and
   associations sections are empty; which traits the
   ethos anatomy bears (text reading and printing
   among them) is open.
15. "Next layer" (P:444). The block keeps flat one-
   element-deep structures with angle arguments on
   one line, as P:172 does, and comments only lines
   whose structure continues onto the next line. Is
   that the reading?

