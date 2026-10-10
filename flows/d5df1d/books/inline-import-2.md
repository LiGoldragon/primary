<!-- to-the-living:start -->
Presentation.{ «The inline import, second edition» }

## The import syntax today

A source is the library a type comes from, written
before a colon. The imports section is a root's
first section, listing every name the file takes
from a source. A sourced reference is a source, a
colon and a name, written where a type is used.
These forms are in production in Ethos Zero, on
its main branch.

The grammar holds two rules today:

- a period after a name declares it, or types it:
  `Topic.Name` declares `Topic` over `Name`;
- a colon after a name sources what follows from
  it: `protos:Text` is `Text` from `protos`.

The imports section, in its three forms:

```
Library
; imports: one name, several, a rename
[ protos:Text
  flow:[ Voice Brief ]
  protos:[ Words.Text ] ]
; types: one struct using all four
[ Record.{ Text Voice Brief Words } ]
[]                     ; traits
[]                     ; associations
```

`protos:Text` takes one name; `flow:[ Voice Brief ]`
takes several from one source; `protos:[ Words.Text ]`
declares the name `Words` for protos's `Text`, the
period declaring as everywhere.

A sourced reference, with no imports section:

```
Library
[]                     ; imports: none
; types: a field of protos's Text
[ Record.{ protos:Text } ]
[]                     ; traits
[]                     ; associations
```

A sourced reference, declared in place:

```
Library
[]                     ; imports: none
; types: Field declared over protos's Text
[ Record.{ Field.protos:Text } ]
[]                     ; traits
[]                     ; associations
```

What each emits: the fully qualified name, the
source joined to the name, written at every use;
nothing is shortened by an import at the top of
the generated file. The rename emits the source's
own name, `Text`, wherever `Words` stands. The
declared-in-place form also makes `Field` a name of
the file, standing for protos's `Text`.

## The three forms for declaring Topic over custom's Name

Each was given to Ethos Zero in a types section and
in a struct position.

### 1. `Topic:custom.Name`

```
Library
[]                     ; imports: none
; types: Topic is the source; custom is
;   declared over Name, inside it
[ Topic:custom.Name ]
[]                     ; traits
[]                     ; associations
```

Read by today's rules: the colon after `Topic` makes
`Topic` the source; the period after `custom` then
declares `custom` over `Name`. A declaration cannot
stand after a source, so the file is refused in both
places. It breaks at the first colon: the name meant
to be declared sits where the source goes, and the
name meant as the source is the one declared.

What the grammar must change: a colon followed by a
period reads as "the first name is declared, the
middle name is its source", so the colon declares
here, and what either sign means depends on the sign
that follows it.

### 2. `Topic:custom:Name`

```
Library
[]                     ; imports: none
; types: a two-segment source, Topic then
;   custom, and the name Name
[ Record.{ Topic:custom:Name } ]
[]                     ; traits
[]                     ; associations
```

Read by today's rules: two colons, a source path of
two segments. The grammar holds one segment: in a
struct position the reader keeps `Topic` as the
source of `Name` and loses `custom`; in a types
section it is refused, since nothing is declared.

What the grammar must change: a source becomes a
path of segments, each colon one step; and to
declare `Topic`, the first colon must declare rather
than source, or `Topic` is a source, not a type.

### 3. `Topic.custom:Name`

```
Library
[]                     ; imports: none
; types: Topic declared over Name, sourced
;   from custom
[ Topic.custom:Name ]
[]                     ; traits
[]                     ; associations
```

Read by today's rules: the period after `Topic`
declares it; the colon after `custom` sources `Name`
from it. Ethos Zero accepts it in a types section
and in a struct position, where it is the
declared-in-place form above.

What the grammar must change: nothing.

Which form declares `Topic` over custom's `Name`:
1, 2 or 3?

## Distillation

### D1. The inline import, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Imports section,
after its closing paragraph and before "## What a
declaration turns into". Held until a number is
picked above; ⟨the form he picks⟩ is replaced by
that form.

Removed: none.

Above, unchanged:

```text
The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.
```

Added, prose:

```text
A type may be declared over a type from a source in place, with no
entry in the imports section: ⟨the form he picks⟩ declares `Topic`
over the type `Name` from the source `custom`.
```

Below, unchanged:

```text
## What a declaration turns into

A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
```

The Sources list gains one line at its end:

```diff
  e51411 ethos
  88475f ethos
+ d5df1d ethos
```

Distils flows/d5df1d/vision/ethos.md, 2026-10-09.

**Ruling D1.** (a) Land with the number picked.
(b) Amend, by line.
<!-- to-the-living:end -->
