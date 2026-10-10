<!-- to-the-living:start -->
Presentation.{ «The inline import, third edition» }

## The inline import

The inline import is `Topic.custom:Name`. The
period after `Topic` declares it; the lowercase
`custom` names a source, and the colon after it
sources `Name` from it. The source is told twice,
by the lowercase first letter and by the colon that
follows. Ethos Zero accepts this form today, in a
types section and in a struct position; the grammar
changes nothing.

```
Library
[]                     ; imports: none
; types: Topic declared over Name, sourced
;   from custom
[ Topic.custom:Name ]
[]                     ; traits
[]                     ; associations
```

## Distillation

### D1. The inline import, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Imports section,
after its closing paragraph and before "## What a
declaration turns into".

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
entry in the imports section: `Topic.custom:Name` declares `Topic`
over the type `Name` from the source `custom`. The source is known
twice: its first letter is lowercase, and a colon follows it.
```

Below, unchanged:

```text
A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
```

Distils flows/d5df1d/vision/ethos.md, 2026-10-09.

**Ruling D1.** (a) Land as written. (b) Amend, by
line.
<!-- to-the-living:end -->
