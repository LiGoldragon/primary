## 2026-08-14 — input is not the same type as output; different fields are different things

> Something right off the bat, in your interface file, there's no
> way that input is the same type as the output or that anything
> is the same type as anything else. Because then why do we have
> different fields? Because they're different things. So right off
> the bat, there's something you don't understand, and you can go
> research our past sessions and then maybe ask me questions if
> you don't really understand what's supposed to happen there.

— psyche, 2026-08-14T18:40+02:00 (Designer session ba906ae2),
dictated, on the Designer's interface-file schema sketch whose
four operation sections shared one element type
(`Vec<VariantDeclaration>` four times). Ruled: no two section
fields carry the same type — different fields exist because they
are different things, each with its own type. The Designer's
operations-and-enum-variants unification proposal falls with
this. Sharing, where it exists, is not type identity; the Designer
is sent to research past sessions before asking further.

## 2026-08-14 — possibly one shape table; the differences live in the traits each section type implements

> possibly, but we need to talk about the differences. the
> trait(s) that inputdeclaration implements, as well as the
> others; output, etc.

> what is the capability which input needs? show me some code. You
> probably wont get it right but will go from there.

— psyche, 2026-08-14T18:54+02:00 (Designer session ba906ae2),
typed, answering the Designer's question whether the four
operation sections carry the same shape table. Carried: sameness
of the shape table is possible but not ruled; the real
differences between the section element types live in the traits
each implements. The conversation turns to the capability input
needs — the Designer is to propose code and iterate from
correction.
