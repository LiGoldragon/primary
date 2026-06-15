# Every struct field has a distinct type — the dimensional principle (refining 638)

The psyche dissolved the "irreducible exception" `638` posed. They are right:
there is **no** struct with two fields of the same type. This corrects the
presentation and states the stronger principle — plus the few places the framing
needs a hair more precision.

## The correction

`638` called a symmetric homogeneous pair (`key`/`value`, `x`/`y`) an
"irreducible exception" that must keep position-names. **Wrong.** A symmetric
homogeneous pair is a **length-2 collection**, not a struct. Once you see that,
the exception is gone and the rule is absolute:

> A struct field's role **is** its type. Two fields of one struct can never share
> a type — if they seem to, you have either (a) under-typed two distinct roles,
> or (b) a collection, not a struct.

## The two cases, and both collapse

**(a) Distinct roles are distinct types.** A body's two arms are `LeftArm` and
`RightArm`, not two `Arm`s. A map entry's `key` and `value` are distinct roles →
distinct types. `source`/`target`, `min`/`max`, `numerator`/`denominator` — all
two-types, never one-type-twice. Reality individuates; the type system should
too.

**(b) Many of one kind is a collection — one field.** A wheel's spokes are not
36 `Spoke` fields; they are one field of type `(Vector Spoke)`. The struct has a
single field; the *collection* holds the repetition. No same-type fields appear.

## The real payoff: dimensional correctness

The deep reason `(a)` matters is not bookkeeping — it is **dimensional analysis,
generalized to every role**. `Height` and `Width` are both measured in metres,
yet they are distinct *types*. That distinction is exactly what makes the right
arithmetic typecheck and the wrong arithmetic impossible:

```
Height * Width  -> Area      ;; defined
Height * Depth  -> Area      ;; defined
Width  * Depth  -> Area      ;; defined
Height * Height -> (no rule) ;; a TYPE ERROR — you cannot make an area this way
```

In a normal language `height` and `height` are just numbers and "still
multiply" — silently giving a meaningless result. Role-as-type makes that a
compile error. This is the units-of-measure idea (F# UoM, Frink) lifted from
*units* to *every semantic role* — far stricter than any mainstream language, and
the strictness is the point.

## Collections: the only home for repetition

When you genuinely have many of a kind, it is a collection, and a collection's
elements are discriminated by **position or key**, not by a field name:

- `(Vector Spoke)` — ordinal position (`0, 1, 2, …`). Order *is* identity: keep
  the spokes in order and "which spoke loosened" stays answerable through tuning.
- `(Map SpokePosition Spoke)` — when identity is richer than an ordinal
  (drive-side / non-drive-side, a specific hub hole), key by a position *type*.

And these two are one idea: **a `Vector` is a `Map` keyed by an ordinal index**.
Your "they're naturally named from 0, 1, 2, 3" is literally the index *type*. So
repetition is always "a keyed collection," differing only in what the key is —
and it is always a single struct field, so it never tempts the rule.

## key/value, dissolved

`TypeReferencePair { key TypeReference value TypeReference }` looked like the
counterexample. It is not: a `Map` is a **collection primitive**, and `key`/
`value` are the primitive's two structural positions — like a vector's index, not
two same-typed fields of an ordinary struct. The pair is just the internal shape
of a map entry; the primitive owns those position-names. No ordinary struct ever
needs them.

## Where the framing needs a hair more precision

Three small sharpenings, in the spirit of "review where I'm not exactly right":

1. **It's a discipline, not a theorem.** "There's no such thing as two same-type
   fields" is true *because you commit to role = type* — a normative choice. Its
   justification is that reality genuinely individuates (left arm ≠ right arm),
   so the choice is well-founded. But it's a stance you adopt, not a fact that
   holds regardless; a sloppy modeller can always write `{ a Int b Int }`. The
   principle is: *don't* — and the type checker can then enforce it.
2. **"They still multiply" is the disease, not the design.** In an untyped world
   `height * height` multiplies and lies. The whole value of role-types is that
   it *stops* — becomes a type error. So the strictness isn't a side effect; it's
   the cure. (And area comes from any two *distinct* linear dimensions, never a
   repeated one.)
3. **Vector is a special Map.** Treating "ordered, named 0,1,2,3" and "keyed" as
   one mechanism (a collection over a key type) is cleaner than two concepts, and
   it's what your spoke example already implies.

## The synthesis

Put together: **role = type** (dimensional) and **repetition = a keyed
collection** ⇒ every struct field has a unique type ⇒ `Type *` (field-name =
type-name) is not a special case but the **default**, always valid; a same-type
collision is *structurally impossible*; and explicit position-names exist only
*inside* collection primitives, which own them. This is the aski vision stated
exactly, and it is coherent and strong.

It also lands cleanly here: it is the existing "newtype per domain value" rule
pushed to its endpoint — **a newtype per role** — and it feeds structural forms
directly (a struct stops carrying hand-written field names at all; the names are
a function of the types, so there is less data to write and nothing to drift).

## Recordable

This is a clear, durable design principle, distinct from (and sharpening) the
newtype rule. Proposed intent wording, for your approval before I record it:

> *A struct field's role is its type: no struct ever has two fields of the same
> type. Distinct roles are distinct types (dimensional correctness — `Height`
> and `Width` are both metres but cannot be interchanged or multiplied as
> like); repetition is a keyed collection (a `Vector` is a `Map` over an ordinal
> index), never repeated fields. Therefore field-name = type-name (`Type *`) is
> the default for every struct field; an explicit field name signals a missing
> type or a collection.*
