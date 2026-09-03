# Protos

## The shared style

Protos is the style all our dialects share. Ethos, Datom, Nomos and
Logos are protos dialects. The fully decomposed engine, three
nexuses, is the protos engine; Datom is a protos dialect that takes
no part in the ethos to nomos to logos to Rust engine, being the
dialect for pure typed data.

## Text is data

A dot opens a delimiter. The textual form of a thing is itself data,
and so a type, and a type has exactly one protos representation.

```
; The prefix is the name; the dot opens the delimiter; what follows is data.
X.{ … }
Y.[ … ]
```

## Situation

Situation is the word for what a parse is in. A character has no
meaning of its own: the block being parsed gives it one, and a
character is free in every block that has not yet given it a
meaning.

```
[ signal-psyche:Object ]    ; in the import block the colon is the import form
[ create:[ Self ] ]         ; in a block of capabilities it marks no self
```

## Shape tells the type

Within its situation, a block's shape tells its type. The shape is:
whether the block opens with a head at all; the character between
the head and the body; the delimiter of the body; the number of
components inside. A block need not start with a head: a bare brace
block or a bare bracket block stands in a position whose situation
already knows its type; and where a head is present, its mere
presence can be what conveys the type. Several types may share one
position when their shapes differ; the shape is then what tells them
apart. Structures of different size are different types. The
character between a head and its body adds a type distinction for the
cost of one character.

```
X.{ … }              ; a struct: the brace after the head
Y.[ … ]              ; an enum: the bracket after the head
Z:Transform.[ … ]    ; a transformer: the character between head and body
{ … }                ; bare: the position already knows the type
```

## Anatomy

Protos is structural recognition of delineations and nothing more. A
Head is just a Head. The number of components in a brace block is
anatomical; in a bracket block it is not. Delineation is protos, and
so is anatomy: a shape is described independently of the type it
represents, and a type's anatomy belongs to its dialect. Structure is
the one word for a struct's field, an enum's variant, a vector's
element: every object is a structure. An enclosed structure holds a
vector of inner structures; an opaque structure holds none. A
Structural thing's capability, structure, returns its protos
structure and every structure it contains, recursively.

```
Head.{ a b }        ; protos sees: a head, a brace block of two components
Head.[ a b c ]      ; protos sees: a head, a bracket block; the count is not anatomy
“ a { b } c ”       ; opaque: no inner structure
```

## Struct, vector, angle brackets

A struct is one fixed shape: the same fields in the same order, each
field's type declared, any type allowed in any field. A vector is the
one variable-length form, and all its components share one type or
one kind. Angle brackets are a protos delimiter, and Datom and Ethos
keep them compatible, so that datom can one day be embedded in ethos
positions.

```
Sorted.{ Vector<Ordered> }    ; a struct of one field, a vector whose components share a kind
```

## Forms of a value

A value has an embodiment, its Rust value, the form the runtime uses;
a signal form, its bytes on the wire; and a textual form. Any concept
in Protos has an embodiment: a kind, a type, a datom value each have
a Rust value, and a kind declaration in ethos becomes an embodied Rust
value holding its name and the rest of its definition. Embodied is
our word over Sized. An embodiment has two textual forms: in the
headed form the head stands outside the block it opens; in the
contained form the name is the first position of a self-contained
block. The contained form is how the embodiment is specified, its
head a field of the Rust struct; the headed form is syntax sugar. A
capitalized bare symbol and an uncapitalized one are two different
types: the capitalized one is an embodiment, a corporal symbol; the
uncapitalized one is a reference, a path, a link. The words working,
real, code, encoded and transcodable are retired.

```
; The headed form of an ethos library: sugar.
Library.{0 1 0}
[]                            ; imports
[types]
[kinds]
[associations]

; The contained form: the same embodiment, self-contained.
Library.{
  {0 1 0}
  []                            ; imports
  [types]
  [kinds]
  [associations]
}
```

## Direction

Text arrives as a potential value and leaves as a value. Text is
Potential, and actualize reads it into its embodiment and may fault:
the text is potential until it matches its anatomy. The Embodied is
Textualizable, and textualize writes the embodiment into the textual
form and cannot fault: an embodied value is already whole. The two
capabilities sit on two different types: the text is never
textualized, the embodied is never actualized. Spans are found on the
way in and computed on the way out. Each direction is several passes,
and the type being embodied into is not known until later passes.

```rust
// Two capabilities on two types.
impl Potential<Library> for Text {
    fn actualize(self) -> Result<Library, Error> { /* may fault */ }
}
impl Textualizable for Library {
    fn textualize(&self) -> Text { /* cannot fault */ }
}
```

## Layers

Reading is layered: Text, Structure, Concept, Corpus. Structure is
the anatomical survey, which knows only that a protos object is
there; Concept is the dialect's reading, where a data-carrying enum
is first the concept of an enum, a vector; Corpus is the final form,
the embodiment. The kinds are Structural, Conceptual, Corporal, and
the capability that reaches a layer sits on the layer above:
structure on Text, conceive on Structure, incorporate on Concept. To
embody a layer is to get the layer below. Potential is the kind used
universally to go from one layer to the next, a rewording of Rust's
TryInto; actualize is its capability; Embodied is its bound. Text to
Potential<Protos> lives in protos; Protos to Potential<Datom> lives
in datom; the associations of different libraries are never mixed.

```
; Each library associates its own layer step, never another's.
Text.[ Potential<Protos> ]     ; in protos: text to its structure
Protos.[ Potential<Datom> ]    ; in datom: the structure to a datom
```

## Shape-defined types

A protos type is implemented as a match over the standard shapes,
each shape carrying its own situation; a complex type is a vector of
shapes. ShapeDefined names this. A big implementation is the sign of
a missing logic plane: every part stays simple, and the complexity
lives in the totality.
