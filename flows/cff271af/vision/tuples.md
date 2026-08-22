# Tuples

## 2026-08-22 — "don't we have a rule against tuples, as they represent poorly specified struct?"

Context (agent, brief): the mainFunction distillation's revised
creation statement carried the exemplar
`TryFrom<(Registry, AssemblyFile)> for ResolvedAssembly`. The psyche,
verbatim:

> what if every input is a defined type? don't we have a rule against
> tuples, as they represent poorly specified struct?

No ruling yet — a question opening the tuple encoding of multi-input
creation.

## 2026-08-22 — the old rules are poorly worded; how realistic is a struct for every complex implementation input?

Context (agent, brief): after the two old-module tuple rules were
recovered and shown. Verbatim:

> the old rules are poorly worded. how realistic is it to create a
> struct for every complex implementation input?

No ruling yet — the psyche asked for a realism assessment before
ruling the tuple/defined-type line.

## 2026-08-22 — "the map" is vague and overloaded; "grain?"

Context (agent, brief): on the proposed scoped wording ("A tuple
never crosses a signature the map shows… tuples are the language's
grain"). Verbatim:

> "the map" is very vague. Its also an overloaded term.
>
> > tuples are the language's grain.
>
> grain?

## 2026-08-22 — no tuples in the traits we design; do standard traits break the pattern?

Context (agent, brief): on the reworded rule ("a tuple in a trait
signature is a struct not yet named"). Verbatim:

> so we wont allow tuples in the traits we design. any standard
> trait that would break that pattern or can we assume the rule to
> hold even then?

Not yet ruled — the psyche testing the rule against the standard
library before ruling.

## 2026-08-22 — do we need to specify more than a single element?

Verbatim:

> do we need to specify that we mean tuples with more than a single
> element?

## 2026-08-22 — the newtype is allowed and must be mentioned; tuples are a form of un-specification

Context (agent, brief): on the tuple-struct edge (newtypes pass the
rule; multi-field tuple structs pass its letter with unnamed
fields). Verbatim:

> the newtype is allowed. the fact that its a tuple is unfortunate
> for us, so it would have to be mentionned in case.
>
> > A multi-field tuple struct, struct Pair(A, B), also passes the
> > rule's letter
>
> do we have to allow those? I really dont like tuples, they're a
> form of un-specification

Rulings carried: the newtype is allowed, and the rule must mention
it (because it is technically a tuple form). Multi-field tuple
structs: the psyche asked whether they must be allowed, inclining
against; "tuples are a form of un-specification" is the stated
rationale.
