# A delimiter for vectors

## Context

A vector in ethos is written with the word and angle brackets:
the element type inside `Vector<...>`. The generator knows
`Vector` as an intrinsic and writes a Rust `Vec` for it. This is
how it stands in production on the generator's main line; no
development branch touches delimiters.

The word is everywhere. Across the forty-nine repositories that
hold ethos it occurs 331 times, in 69 files; `Option<` occurs 324
times and `Result<` 16. Counted examples, verbatim from main:

```
  Locks.Vector<Lock>
```

```
  EventsRead.{ FlowId Vector<Event> }
```

```
  Outcome.[ ResolvedSkills.Vector<String>
            SkillsChanged.SkillChange
            SkillsChecked.Vector<String>
            SkillsRebuilt.Vector<String>
            Rejected.String ]
```

```
  Nested.Vector<Option<Result<String Integer>>>
```

```
  Form.[ Struct.Vector<Datom>
         Vector.Vector<Datom>
```

The last one is a variant named `Vector` carrying a vector: the
word does two jobs on one line.

Every bracket pair on the keyboard is already taken, by ethos and
by datom together:

```
{ }   struct                 (datom: struct)
[ ]   enum where types are   (datom: vector)
      defined
< >   type arguments
« »   string, opaque
( )   Meaning, opaque
;     comment to end of line
. ! : separators
```

Any other glyph is a name character today: `|`, `#`, `@`, `*` and
every non-ASCII bracket. None of the single ASCII glyphs opens
and closes with a different character, so none can nest.

A bracket after a dot already means an enum, witnessed on main:
`Items.[ Integer ]` generates a one-variant enum, not a vector.
A bare bracket in a position is refused as not a reference.

Unicode pairs the reader does not reserve, with their coverage in
the monospace fonts of this host:

```
⟦ ⟧   white square brackets        34 fonts
⟨ ⟩   mathematical angle brackets  34 fonts
‹ ›   single guillemets            35 fonts
⟪ ⟫   double angle brackets        34 fonts
⌈ ⌉   ceiling brackets             34 fonts
⦃ ⦄   white curly brackets         32 fonts
```

If the glyphs on the line above show as boxes on your phone, that
is the rendering answer for this book.

```
  source text
      |
      v
  reader: { } [ ] < > « » ( ) ;
      |            new pair joins here
      v
  Vector<T> = word + angles
      |
      v
  generator: std::vec::Vec<T>
```

One record bears on typing: on 2026-08-30 (flows/62022e8f,
ethosTypes, archived) the map type was written with `<<` because
guillemets could not be typed. The keyboard policy in CriomOS-home
is plain US with no compose key. Whether a non-ASCII pair can be
typed today is unknown.

One record competes for a pair: on 2026-09-19 (flows/b81560,
ethosEscapeDelimiter) an unused balanced delimiter was wanted to
hold ethos or logos inside datom. Its candidates were never
answered. A pair spent on vectors is one fewer for that.

## The candidates, shown

Each candidate rewrites the second and third examples above. The
spacing follows the canonical print of brackets and braces, a
space inside; whether a new pair prints tight like `< >` is
question 3.

Candidate 1, white square brackets:

```
  EventsRead.{ FlowId ⟦ Event ⟧ }
  Outcome.[ ResolvedSkills.⟦ String ⟧
            SkillsChanged.SkillChange
            SkillsChecked.⟦ String ⟧
            SkillsRebuilt.⟦ String ⟧
            Rejected.String ]
  Nested.⟦ Option<Result<String Integer>> ⟧
  Form.[ Struct.⟦ Datom ⟧
         Vector.⟦ Datom ⟧
```

Collides with nothing in datom, Nix, Rust or the shell. Machines
already use it as a placeholder in prose. Cannot be dictated.

Candidate 2, single guillemets:

```
  EventsRead.{ FlowId ‹ Event › }
  Outcome.[ ResolvedSkills.‹ String ›
            SkillsChecked.‹ String › ]
  Nested.‹ Option<Result<String Integer>> ›
```

Half the shape of the string delimiter `«`; two in a row read as
one `«` at phone size. Needs the same input route as `«`.

Candidate 3, mathematical angle brackets:

```
  EventsRead.{ FlowId ⟨ Event ⟩ }
  Outcome.[ ResolvedSkills.⟨ String ⟩
            SkillsChecked.⟨ String ⟩ ]
  Nested.⟨ Option<Result<String Integer>> ⟩
```

Nearly the shape of `< >`, which stays for `Option` and `Result`
on the same line.

Candidate 4, the ASCII bracket with no head. Not a new delimiter:
it is datom's own vector value. It works only where no dot
precedes it, since `Name.[ ... ]` is an enum:

```
  EventsRead.{ FlowId [ Event ] }
  drain![ [ String ] ]
```

```
  Locks.[ Lock ]            ; enum today
  ResolvedSkills.[ String ] ; enum today
```

The first, fourth and fifth examples of the context cannot be
written in candidate 4 without changing what a bracket after a
dot means.

## Questions on the vector

1. Which of the four candidates, or which other unused pair? If
   a pair cannot be typed, say so: the generator can accept a
   typable spelling and print the pair, but that is a second
   design and this book does not propose it.

2. Does the word go away entirely, or does `Vector<T>` stay valid
   beside the pair for a time? The spirit says no parallel
   compatibility path; the question is whether the 331 sites are
   rewritten in one landing.

3. Tight or spaced? Angles print tight, `Vector<Lock>`; braces
   and brackets print spaced, `{ FlowId }`. The candidates above
   are shown spaced.

4. The generated field name comes from the word today: a position
   `Vector<String>` becomes the Rust field `string_vector`. With
   the word gone from the source, the name must come from the
   pair. Shown:

```
  Capsule.{ Home.String Vector<String> }
  ; Rust today: pub string_vector: Vec<String>
```

   Does the derived name stay `string_vector`, or become
   `strings`, or must a vector position always be named?

5. Datom writes a vector value as `[ 1 2 3 ]`. Ethos would write
   the vector type as `⟦ Integer ⟧` while datom keeps `[ ]` for
   the value. Is that split wanted, or does datom take the same
   pair for values?

6. `Option<T>` and `Result<T E>` keep the word and angles under
   every candidate here. Is that so?

7. The escape-delimiter record wants an unused balanced pair too.
   Do vectors take one of the pairs listed, leaving the rest for
   that, or is that want to be answered first?

## Comments, the smaller section

A comment today runs from `;` to the end of the line. The reader
drops it before anything is built: there is no comment node, so
the canonical print carries no comment and generated Rust carries
none. Witnessed on main: a file with a trailing `; comment` after
a position generates the struct and nothing of the comment.

```
  Record.{ String  ; trailing
           Integer }
  ; Rust: pub struct Record
  ;       { pub string: String,
  ;         pub integer: i64 }
```

Of 161 ethos files on main, 57 carry comments, on 455 of 4978
lines. The vision asks for a comment on every section.

Records on where a comment sits: on 2026-10-07 (flows/e5a0bc,
ethos) the comment belongs above or beside the thing, lined up
with its indentation, and the question was raised whether anyone
comments below. The notion of 2026-10-12 guesses the description
follows the object. Beside is also after on the line.

A documentation delimiter would be a balanced pair the reader
keeps as a node, so that later it can be read as the object's
description and, further on, as code. Shown with one unused pair,
after the object:

```
  Record.{ String Integer }
  ⟪ one string and one integer ⟫
```

Beside the object:

```
  Record.{ String Integer } ⟪ a pair ⟫
```

8. After, meaning below on the next line, or beside on the same
   line?

9. Kept as a node the print carries, while `;` stays the dropped
   comment? That is two kinds of comment; is that wanted?

10. Does the documentation pair get chosen now, with the vector
    pair, so the two are chosen from the same free list, or does
    it wait?

## Distillation

Target file, authored source:
`/git/github.com/LiGoldragon/psyche-skills/vision/ethos.md`

Two proposals, each one line, each shown as a question's answer
would land it. Nothing lands before a ruling.

### Proposal 1: the vector delimiter

Line 338, the sentence as it stands, with the line above and
below:

Above, as it stands:

Each section has its own parsing context; placement carries the
meaning. Head then symbol is a variant of `Query` or `Response` in
a Signal's first two sections, an alias in the types section.

As it stands:

Where types are defined a bracket is an enum, never a vector.

Added after it, one of three; the pair is the ruling of
question 1 and the spacing of question 3:

Side a, white square brackets:

```
+ A vector is its element type inside ⟦ ⟧:
+ `Names.⟦ String ⟧`. The word Vector is not
+ written.
```

Side b, single guillemets:

```
+ A vector is its element type inside ‹ ›:
+ `Names.‹ String ›`. The word Vector is not
+ written.
```

Side c, mathematical angle brackets:

```
+ A vector is its element type inside ⟨ ⟩:
+ `Names.⟨ String ⟩`. The word Vector is not
+ written.
```

Below, as it stands:

Ethos may generate default implementations for Query and Response,
which is why Signal is its own root.

Line 177 then loses the word from the intrinsics list, under any
side:

```
- Integer, Decimal, Boolean, Meaning, Vector,
- Option, Result, Self.
+ Integer, Decimal, Boolean, Meaning, Option,
+ Result, Self.
```

Removed lines: the one shown, only when the word goes away whole
(question 2).

Impurities discarded: none.

Ruling asked:

1. Land side a, b or c as written.
2. Another pair; name it.
3. Amend by line.
4. Keep `Vector<T>`; close the notion.

### Proposal 2: the documentation comment

Line 480, as it stands, with the line above and below:

Above, as it stands:

Ethos expands vertically: a structure with more than one element
opens on its line and its elements hang beneath the first, aligned;
the closing delimiter ends the last element's line. Nothing that
has a next layer sits on one line.

As it stands:

Ethos carries a comment on every section and on every line that
has a next layer, saying in plain words what the machine reads
there; a comment runs from ; to the end of the line.

Added after it, the pair being a placeholder until question 10
is ruled:

```
+ A description of an object is a balanced pair
+ the reader keeps, after the object:
+ `Record.{ String Integer } ⟪ a pair ⟫`.
```

Below, as it stands:

## Zero

Removed lines: none.

Impurities discarded: none.

Ruling asked:

1. Land as written, naming the pair.
2. Hold until the vector pair is landed.
3. Amend by line.
